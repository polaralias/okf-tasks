# OKF Tasks

OKF Tasks is an independent profile of the [Open Knowledge Format (OKF) v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/ee67a5ca27044ebe7c38385f5b6cffc2305a9c1a/okf/SPEC.md) for portable, repository-local task records.

It defines how tasks, workstreams, lifecycle state, evidence, relationships, and external tracker mappings can be represented as human- and agent-readable Markdown with YAML frontmatter. A task bundle works on its own or alongside an existing repository knowledge system.

This project is not affiliated with or endorsed by Google Cloud.

## What is included

- [`SPEC.md`](./SPEC.md) — the OKF Tasks v0.2 profile.
- [`schemas/`](./schemas/) — versioned JSON Schemas for task, workstream, and time-entry frontmatter.
- [`skills/okf-task-lifecycle/`](./skills/okf-task-lifecycle/) — a portable agent skill and deterministic CLI.
- [`examples/`](./examples/) — standalone, knowledge-linked, and tracker-synchronised bundles.
- [`conformance/`](./conformance/) — a shared positive/negative fixture manifest and exhaustive lifecycle matrix.
- [`implementations/typescript/`](./implementations/typescript/) — an independent validator that cross-checks the same manifest.
- [`tests/`](./tests/) — Python reference implementation tests.

## Quick start

Install the reference CLI dependency:

```text
python -m pip install PyYAML
```

Create, track time, and validate a task bundle:

```text
python skills/okf-task-lifecycle/scripts/okf_tasks.py init-bundle --root .
python skills/okf-task-lifecycle/scripts/okf_tasks.py create --root . --slug first-task --title "First task" --description "Deliver the first observable result."
python skills/okf-task-lifecycle/scripts/okf_tasks.py set-status --root . --task first-task --status ready
python skills/okf-task-lifecycle/scripts/okf_tasks.py start-time --root . --task first-task --actor agent
# Perform the work, then close the session:
python skills/okf-task-lifecycle/scripts/okf_tasks.py stop-time --root . --task first-task --actor agent
python skills/okf-task-lifecycle/scripts/okf_tasks.py validate --root .
```

The default bundle location is `tasks/`. Use `--bundle <path>` to select another repository-relative bundle root.

Prepare a task body for an external tracker without leaking secrets or local paths:

```text
python skills/okf-task-lifecycle/scripts/okf_tasks.py prepare-export --root . --source tasks/first-task/task.md --output .okf-exports/first-task.md
```

Repository-relative links are converted to credential-free GitHub or GitLab links pinned to the current commit. Unsafe or unresolved content stops the export.

## Design boundary

OKF Tasks governs execution truth. It links to product requirements, architecture, decisions, runbooks, and other canonical knowledge, but does not prescribe how a repository creates or governs that knowledge.

External issue trackers are projections or upstream sources according to an explicit sync authority. Provider-specific APIs remain outside the core profile, while adapter trust boundaries, egress checks, and portable-link behavior are normative.

## Verify the release bar

```text
python -m unittest discover -s tests -v
python conformance/generate_fixtures.py --check
npm ci
npm test
python scripts/check_release.py
```

## Status

Version 0.2 adds secure external-artifact preparation and repository-link portability. Normative changes require fixtures and agreement between the Python and TypeScript implementations; see [`GOVERNANCE.md`](./GOVERNANCE.md).

## License

Apache License 2.0. See [`LICENSE`](./LICENSE).
