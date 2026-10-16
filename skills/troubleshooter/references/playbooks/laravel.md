# Playbook: Laravel

Load when dependencies and runtime/project structure prove Laravel on the causal path. Generic PHP
uses `discovery.md` without this playbook.

This is conditional diagnostic guidance, not a recommendation to select this framework. Project
contracts and installed-version evidence govern applicability. Candidate origins below are
non-exhaustive hypotheses; neither a framework name nor an error shape establishes a cause.

## Reading the traceback

- The deepest relevant frame under `app/` anchors the symptom; it does not establish the root cause.
  Trace state through application and framework frames to the producer or ownership boundary.
- For `Call to a member method … on null`, trace how the accessed value was produced and whether
  the relevant contract permits null; do not assume its producer is a model, relation or binding.
- `BindingResolutionException` / `Target [X] is not instantiable` means the service container
  could not build a dependency. Inspect the reported dependency, binding and construction path
  before attributing the defect to a binding or excluding the consuming class.

## Candidate origins to inspect

1. **Eloquent relations & lazy loading.** `$model->relation` returning `null` (no related row)
   or a `Collection` where a model was expected; `find()` vs `findOrFail()`; N+1 masking a
   relation that's sometimes empty; `firstOrNew` returning an unsaved new model when absent,
   while `firstOrCreate` inserts the missing record.
   `rg -n -- '->find\(|firstOrNew|firstOrCreate|->first\(\)|hasMany|belongsTo' <relevant-scope>`
2. **Service container & DI.** A constructor type-hint with no binding; an interface bound only
   in one service provider; `app()->make()` / `resolve()` for something not registered;
   a singleton holding stale state across requests in queue workers.
   `rg -n 'bind\(|singleton\(|->make\(|resolve\(|interface '`
3. **Request & validation.** `$request->input('x')` returning `null` for an absent key;
   reading validated data before `$request->validate()`; `$request->user()` null when the auth
   middleware didn't run on that route. `rg -n -- '->input\(|->validate\(|->user\(\)|FormRequest' <relevant-scope>`
4. **Middleware & route model binding.** Implicit binding (`Route::get('/{post}')`) silently
   404ing or injecting the wrong model; middleware ordering leaving a value unset; a global
   middleware that runs only on the `web` group, not `api`. Check `app/Http/Middleware/` and
   the route group.
5. **Config & env.** `env()` called outside `config/` returns `null` once config is cached
   (`config:cache`); a `config('x.y')` key that doesn't exist returning `null`.
   `rg -n "env\(|config\("`
6. **Facades hiding the real call.** A facade (`Auth::`, `DB::`, `Cache::`) resolving to a
   manager whose underlying driver may be misconfigured. Trace the resolved manager, driver and
   configuration; do not attribute a null to the facade or driver without evidence.

## Masking mechanics to distrust

Inspect the actual path before treating any of these patterns as causal masking:

- `optional($x)->y` and the `?->` operator deferring the crash to the next hard access.
- `try { … } catch (\Throwable $e) {}` or a catch that logs and returns a default, swallowing
  the real exception. `rg -n 'catch\s*\(.*\)\s*\{'`
- `@` error suppression on a call (`@$arr['key']`) hiding the warning that explains the null.

## Local development reproduction

Run relevant `php artisan` checks and focused tests in a verified local development copy under the
[common authority rules](../../SKILL.md#authority-and-local-reproduction). Resolve database, cache, queue, and
external-delivery targets before migration, `tinker`, or worker probes; use disposable test data for
data-changing checks.

Persistence semantics: [Laravel 13 Eloquent guide](https://laravel.com/docs/13.x/eloquent#retrieving-or-creating-models).
Resolve the installed framework version before applying version-sensitive advice.
