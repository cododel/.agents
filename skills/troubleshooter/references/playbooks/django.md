# Playbook: Django / Python

Load only for a Python traceback (Django or plain). This lists where Django *manufactures*
bad state that obvious project code never shows. Use it with `discovery.md`, not instead.

## Reading the traceback

- The deepest project frame owns the wrong assumption; frames inside `site-packages/`,
  `django/`, `rest_framework/` are the path the bad state travelled, not its source.
- `AttributeError: 'NoneType' object has no attribute …` and `KeyError` are the dominant
  shapes — both mean *something assumed a value that was never guaranteed*. Find where it was
  supposed to be set.
- For 500s without a clean trace, the real exception is often wrapped — look for the
  `During handling of the above exception, another exception occurred` chain and read the
  *first* one.

## Where bad state is born (in likelihood order)

1. **DRF serializers.** `.data` accessed before `.is_valid()`; `SerializerMethodField`
   returning `None`; `source=` pointing at a missing attr; `required=False` fields read as if
   present; nested serializer fed a queryset vs. instance.
   `rg -n 'class \w+Serializer|SerializerMethodField|source=|is_valid\(' `
2. **QuerySet laziness & `.get()`.** `.first()` / `.filter().first()` returning `None` used
   downstream as an object; `.get()` raising `DoesNotExist`/`MultipleObjectsReturned`; a
   queryset evaluated in a template/`if` when the code expected a model. Bad state appears far
   from the query because querysets are lazy.
   `rg -n '\.get\(|\.first\(\)|\.filter\(|DoesNotExist'`
3. **Request lifecycle & middleware.** `request.user` is `AnonymousUser` (not `None`) when
   unauthenticated; `request.data` vs `request.POST`; a middleware that sets an attr only on
   some paths; `get_object_or_404` masking the real lookup bug.
4. **Settings & env.** `os.environ[...]` vs `os.getenv(...)` (the former raises, the latter
   silently `None`); a setting read at import time before `.env` is loaded; `DEBUG`-dependent
   behavior. `rg -n 'os\.environ|getenv|settings\.'`
5. **Signals & `save()` side effects.** A `post_save`/`pre_save` signal, an overridden
   `save()`, or `@receiver` mutating or clearing state out of band — invisible at the call
   site. `rg -n '@receiver|post_save|pre_save|def save\('`
6. **Migrations / model drift.** Field exists in the model but not in the DB (unapplied
   migration), or vice versa — `column does not exist` / `no such column`. Check
   `*/migrations/` against the model.

## Masking mechanics to distrust

- A bare `except Exception:` (or `except:`) swallowing the real error and re-raising something
  generic. `rg -n 'except\b.*:\s*$|except Exception'` — read what it hides.
- `getattr(obj, name, default)` and `dict.get(key)` quietly producing the `None` that crashes
  three frames later.
- Mutable default arguments (`def f(x=[])`) carrying state between calls.

## A read-only repro is still a mutation

Running `pytest`, `manage.py shell`, `manage.py migrate`, or any management command can touch
the database, fixtures, or migration state. Per the gate, write the exact command and ask the
user to run it — don't execute it to "just check".
