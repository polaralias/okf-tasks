# Conformance fixtures

Fixtures are repository roots whose `tasks/` subdirectories exercise OKF Tasks v0.1. `manifest.json` is the shared contract consumed independently by the Python and TypeScript implementations.

Hand-authored fixtures cover the minimal document, base OKF failure, and bad time rollup. Deterministic fixtures under `generated/` cover task fields and headings, workstreams, time methods, estimates, points, sync authority, external uniqueness, reopening history, unknown concepts, broken-link warnings, and generated indexes.

`transitions.json` enumerates every normal lifecycle edge. Tests evaluate all 64 source/target pairs, including idempotent same-state updates.

Run the fixtures through the reference implementation:

```text
python skills/okf-task-lifecycle/scripts/okf_tasks.py validate --root conformance/valid/minimal
python skills/okf-task-lifecycle/scripts/okf_tasks.py validate --root conformance/invalid/missing-type
```

Regenerate and verify the generated corpus:

```text
python conformance/generate_fixtures.py
python conformance/generate_fixtures.py --check
```
