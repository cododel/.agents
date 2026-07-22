# Playbook: Laravel / PHP

Load only for a Laravel / PHP traceback. Where the framework manufactures bad state that the
controller/model code doesn't show. Use with `discovery.md`.

## Reading the traceback

- The deepest frame under `app/` owns the wrong assumption; frames in `vendor/laravel/` and
  `vendor/symfony/` are the path it travelled.
- `Call to a member method … on null` is the dominant shape — a model/relation/binding that
  resolved to `null` and was used as an object. Find where it was supposed to resolve.
- `BindingResolutionException` / `Target [X] is not instantiable` means the service container
  couldn't build a dependency — the bad state is a missing or mis-registered binding, not the
  class that asked for it.

## Where bad state is born (in likelihood order)

1. **Eloquent relations & lazy loading.** `$model->relation` returning `null` (no related row)
   or a `Collection` where a model was expected; `find()` vs `findOrFail()`; N+1 masking a
   relation that's sometimes empty; `firstOrNew`/`firstOrCreate` returning an unsaved model.
   `rg -n '->find\(|firstOrNew|firstOrCreate|->first\(\)|hasMany|belongsTo'`
2. **Service container & DI.** A constructor type-hint with no binding; an interface bound only
   in one service provider; `app()->make()` / `resolve()` for something not registered;
   a singleton holding stale state across requests in queue workers.
   `rg -n 'bind\(|singleton\(|->make\(|resolve\(|interface '`
3. **Request & validation.** `$request->input('x')` returning `null` for an absent key;
   reading validated data before `$request->validate()`; `$request->user()` null when the auth
   middleware didn't run on that route. `rg -n '->input\(|->validate\(|->user\(\)|FormRequest'`
4. **Middleware & route model binding.** Implicit binding (`Route::get('/{post}')`) silently
   404ing or injecting the wrong model; middleware ordering leaving a value unset; a global
   middleware that runs only on the `web` group, not `api`. Check `app/Http/Middleware/` and
   the route group.
5. **Config & env.** `env()` called outside `config/` returns `null` once config is cached
   (`config:cache`); a `config('x.y')` key that doesn't exist returning `null`.
   `rg -n "env\(|config\("`
6. **Facades hiding the real call.** A facade (`Auth::`, `DB::`, `Cache::`) resolving to a
   manager whose underlying driver is misconfigured — the null comes from the driver, not the
   facade.

## Masking mechanics to distrust

- `optional($x)->y` and the `?->` operator deferring the crash to the next hard access.
- `try { … } catch (\Throwable $e) {}` or a catch that logs and returns a default, swallowing
  the real exception. `rg -n 'catch\s*\(.*\)\s*\{'`
- `@` error suppression on a call (`@$arr['key']`) hiding the warning that explains the null.

## A read-only repro is still a mutation

`php artisan` commands, `migrate`, `tinker`, queue workers, and the test suite hit the
database, cache, and queue. Per the gate, write the exact command for the user to run — don't
execute `artisan` to "just check".
