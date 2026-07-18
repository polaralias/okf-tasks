<p align="center">
  <img src="OKF%20Tasks%20Banner.png" alt="OKF Tasks banner" width="960" />
</p>

# OKF Tasks

OKF Tasks is an independent profile of the [Open Knowledge Format (OKF) v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/ee67a5ca27044ebe7c38385f5b6cffc2305a9c1a/okf/SPEC.md) for portable, repository-local task records.

It defines how tasks, workstreams, lifecycle state, evidence, relationships, and external tracker mappings can be represented as human- and agent-readable Markdown with YAML frontmatter. A task bundle works on its own or alongside an existing repository knowledge system.

This project is not affiliated with or endorsed by Google Cloud.

## What is included

- [`SPEC.md`](./SPEC.md) — the OKF Tasks v0.4 profile.
- [`schemas/`](./schemas/) — versioned JSON Schemas for task, workstream, time-entry, and Tracker Profile frontmatter.
- [`skills/okf-task-lifecycle/`](./skills/okf-task-lifecycle/) — a portable agent skill and deterministic CLI.
- [`examples/`](./examples/) — standalone, knowledge-linked, and tracker-synchronised bundles.
- [`docs/VISUALIZATION.md`](./docs/VISUALIZATION.md) — a generated Mermaid task graph that renders directly in GitHub.
- [`docs/VISUALIZATION_GUIDE.md`](./docs/VISUALIZATION_GUIDE.md) — interactive viewer features, generation, and review workflow.
- [`docs/TRACKER_INTEGRATION.md`](./docs/TRACKER_INTEGRATION.md) — provider setup, project-default selection, and live integration evidence.
- [`conformance/`](./conformance/) — a shared positive/negative fixture manifest and exhaustive lifecycle matrix.
- [`implementations/typescript/`](./implementations/typescript/) — an independent validator that cross-checks the same manifest.
- [`tests/`](./tests/) — Python reference implementation tests.

## Quick start

Install the project in editable mode to expose the `okf-tasks` command:

```text
python -m pip install -e .
okf-tasks --help
```

Create, track time, and validate a task bundle:

```text
okf-tasks init-bundle --root .
okf-tasks create --root . --slug first-task --title "First task" --description "Deliver the first observable result."
okf-tasks set-status --root . --task first-task --status ready
okf-tasks start-time --root . --task first-task --actor agent
# Perform the work, then close the session:
okf-tasks stop-time --root . --task first-task --actor agent
okf-tasks validate --root .
```

The default bundle location is `tasks/`. Use `--bundle <path>` to select another repository-relative bundle root.

For a repository whose `docs/` tree already contains an actual project's context and delivery material, initialize the optional project-documentation placement:

```text
okf-tasks init-bundle --root . --placement docs
okf-tasks create --root . --bundle docs/tasks --slug first-task --title "First task" --description "Deliver the first observable result."
```

This creates `docs/tasks/`; it does not turn operational task records into canonical requirements or architecture.

Initialize a first-class tracker connection from a live provider API. Credentials are read only from the runtime environment and are never written to the profile:

```text
okf-tasks tracker init --root . --tracker github-main --system github --scope owner/repository --mode bidirectional --authority repository
okf-tasks tracker init --root . --tracker gitlab-platform --system gitlab --scope group/project --mode bidirectional --authority repository
okf-tasks tracker init --root . --tracker linear-engineering --system linear --scope ENG --mode bidirectional --authority repository --default
okf-tasks tracker init --root . --tracker clickup-delivery --system clickup --scope 123456789 --mode bidirectional --authority repository
```

The default credential variables are `GITHUB_TOKEN`, `GITLAB_TOKEN`, `LINEAR_API_KEY`, and `CLICKUP_API_TOKEN`. Use `--api-base` for GitHub Enterprise or self-managed GitLab. For reviewed or offline setup, pass a normalized provider snapshot with `--discovery-file`.

Choose the scope that belongs to the current project, prompt when more than one repository, project, team, or List is plausible, and save the chosen profile with `--default` or `tracker set-default`. An explicit `--tracker` takes precedence; otherwise create, import, sync, and link commands use the saved default or the sole profile. Multiple profiles without a default stop with a candidate list instead of guessing.

```text
okf-tasks tracker set-default --root . --tracker clickup-delivery
```

Inspect configuration and detect provider drift without silently remapping fields or statuses:

```text
okf-tasks tracker inspect --root . --tracker linear-engineering
okf-tasks tracker refresh --root . --tracker linear-engineering --discovery-file discovery.json
okf-tasks tracker refresh --root . --tracker linear-engineering --discovery-file discovery.json --accept
```

Link a task using the provider-global object ID and separate human-facing key:

```text
okf-tasks link-external --root . --task first-task --tracker linear-engineering --id <issue-uuid> --key ENG-123 --url https://linear.app/example/issue/ENG-123
```

Create and verify a remote record from a local task, import a remote record to work from it locally, or reconcile an existing binding:

```text
okf-tasks tracker create --root . --task first-task
okf-tasks tracker import --root . --remote-key 123 --slug imported-issue
okf-tasks tracker sync --root . --task first-task --direction push
okf-tasks tracker sync --root . --task first-task --direction pull
```

Creation and push perform the same deterministic egress and repository-link checks as `prepare-export`. A remote revision change stops push until it is explicitly resolved. Provider writes are read back before the binding base advances.

Prepare a task body for an external tracker without leaking secrets or local paths:

```text
okf-tasks prepare-export --root . --source tasks/first-task/task.md --output .okf-exports/first-task.md
```

Repository-relative links are converted to credential-free GitHub or GitLab links pinned to the current commit. Unsafe or unresolved content stops the export.

## Visualize a bundle

The optional visualizer follows the consumer pattern demonstrated by Google's [OKF reference visualizer](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf): the Markdown/YAML bundle remains canonical and visualization is a derived view.

Generate both review pages—the focused visualization and the full examples browser—from the shared viewer template:

```text
python scripts/generate_local_docs.py
python scripts/generate_local_docs.py --check
```

Generate a custom interactive HTML graph and a GitHub-rendered Mermaid graph:

```text
python scripts/visualize_bundle.py \
  --bundle examples/visualization/tasks \
  --name "OKF Tasks visualization example" \
  --html local-docs/okf-tasks-visualization.html \
  --markdown docs/VISUALIZATION.md
```

Open the HTML file locally for search, type filters, switchable layouts, readable relationship labels, light/dark themes, fullscreen graph review, a complete Markdown document tree, GitHub-style sanitized Markdown, Mermaid diagrams, backlinks, and collapsible raw YAML/source. Both `local-docs/okf-tasks-visualization.html` and `local-docs/okf-tasks-examples.html` are generated from the same renderer. The HTML loads pinned Cytoscape, Marked, DOMPurify, and Mermaid browser libraries from jsDelivr; task and document data are embedded in the generated file.

GitHub renders the Mermaid diagram directly in [`docs/VISUALIZATION.md`](./docs/VISUALIZATION.md). For a hosted interactive graph, publish the generated HTML through GitHub Pages; ordinary GitHub file views do not execute committed HTML.

## Design boundary

OKF Tasks governs execution truth. It links to product requirements, architecture, decisions, runbooks, and other canonical knowledge, but does not prescribe how a repository creates or governs that knowledge.

External issue trackers are projections or upstream sources according to an explicit direction and authority. Versioned Tracker Profiles capture provider scope, stable status and field IDs, discovery state, and mapping policy for GitHub, GitLab, Linear, and ClickUp. Authentication and webhook deployment remain runtime concerns.

## Verify the release bar

```text
python -m unittest discover -s tests -v
python conformance/generate_fixtures.py --check
npm ci
npm test
python scripts/check_release.py
```

## Status

Version 0.4 defines first-class provider setup and scoped external bindings. Normative changes require fixtures and agreement between the Python and TypeScript implementations; see [`GOVERNANCE.md`](./GOVERNANCE.md).

## License

Apache License 2.0. See [`LICENSE`](./LICENSE).
