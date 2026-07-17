# Project documentation placement

This example uses `docs/tasks/` because the repository's `docs/` tree is already the home for an actual project's context and delivery material. `docs/PROJECT.md` remains durable project knowledge; `docs/tasks/` contains operational execution state.

Initialize this placement with:

```text
python skills/okf-task-lifecycle/scripts/okf_tasks.py init-bundle --root . --placement docs
```

Use `--bundle docs/tasks` for subsequent lifecycle commands.
