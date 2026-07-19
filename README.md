<p align="center">
  <img src="OKF%20Tasks%20Banner.png" alt="OKF Tasks banner" width="960" />
</p>

# OKF Tasks

OKF Tasks is an independent profile of the [Open Knowledge Format (OKF) v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/ee67a5ca27044ebe7c38385f5b6cffc2305a9c1a/okf/SPEC.md) for portable, repository-local task records.

It defines how tasks, workstreams, lifecycle state, evidence, relationships, and external tracker mappings can be represented as human- and agent-readable Markdown with YAML frontmatter. A task bundle works on its own or alongside an existing repository knowledge system.

This project is not affiliated with or endorsed by Google Cloud.

## What is included

- [`SPEC.md`](./SPEC.md) — the OKF Tasks v0.1 profile.
- [`schemas/`](./schemas/) — versioned JSON Schemas for task, workstream, embedded time-entry, and Tracker Profile frontmatter.
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
okf-tasks --version
okf-tasks --help
```

The console command is provided by this repository's Python package. Agent skills also bundle the same `scripts/okf_tasks.py` implementation as a zero-install fallback; they do not silently install or upgrade the package. See [`docs/CLI_SETUP.md`](./docs/CLI_SETUP.md) for the supported setup and verification contract.

Create, track time, and validate a task bundle:

```text
okf-tasks init-bundle --root .
okf-tasks create --root . --slug first-task --title "First task" --description "Deliver the first observable result."
okf-tasks set-status --root . --task first-task --status ready
okf-tasks start-time --root . --task first-task --actor agent --activity implementation
# Perform the work, then close the session:
okf-tasks stop-time --root . --task first-task --actor agent
okf-tasks validate --root .
```

When the repository already contains governed concepts, connect a new task as part of creation with repeatable `--depends-on <task-concept-path>` and `--related <repository-relative-markdown-path>` arguments. `--related` validates that the target exists inside the repository and writes the correct source-relative Markdown link.

Validation also audits the repository's governed Tasks, Workstreams, and typed durable OKF knowledge documents as one resolved local link graph. Incoming links count, while runbooks, handoffs, temporary material, generated output, and Tracker Profiles are excluded.

The default bundle location is `tasks/`. Use `--bundle <path>` to select another repository-relative bundle root.

For a repository whose `docs/` tree already contains an actual project's context and delivery material, initialise the optional project-documentation placement:

```text
okf-tasks init-bundle --root . --placement docs
okf-tasks create --root . --bundle docs/tasks --slug first-task --title "First task" --description "Deliver the first observable result."
```

This creates `docs/tasks/`; it does not turn operational task records into canonical requirements or architecture.

Initialise a first-class tracker connection from a live provider API. Credentials are read only from the runtime environment and are never written to the profile:

```text
okf-tasks tracker init --root . --tracker github-main --system github --scope owner/repository --mode bidirectional --authority repository
okf-tasks tracker init --root . --tracker gitlab-platform --system gitlab --scope group/project --mode bidirectional --authority repository
okf-tasks tracker init --root . --tracker linear-engineering --system linear --scope ENG --mode bidirectional --authority repository --default
okf-tasks tracker init --root . --tracker clickup-delivery --system clickup --scope 123456789 --mode bidirectional --authority repository
```

The default credential variables are `GITHUB_TOKEN`, `GITLAB_TOKEN`, `LINEAR_API_KEY`, and `CLICKUP_API_TOKEN`. Use `--api-base` for GitHub Enterprise or self-managed GitLab. For reviewed or offline setup, pass a normalised provider snapshot with `--discovery-file`.

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

## Visualise a bundle

The first-class visualiser follows the consumer pattern demonstrated by Google's [OKF reference visualiser](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf): the Markdown/YAML bundle remains canonical and visualisation is a derived view.

Generate the focussed bundle, full examples browser, and relationship review page from the shared workspace template:

```text
python scripts/generate_complex_examples.py --root .
python scripts/generate_complex_examples.py --root . --check
python scripts/generate_local_docs.py --mermaid
python scripts/generate_local_docs.py --mermaid --check
```

The maintained review set includes three generated stress-test workspaces. `okf-tasks-complex-task-portfolio.html` contains [forty linked Tasks, five coordinating Workstreams, mixed lifecycle states, and embedded time evidence](./examples/complex-task-portfolio/README.md). `okf-tasks-architecture-knowledge-base.html` contains [twenty ADRs plus detailed architecture, service, interface, quality-attribute, and implementation records](./examples/architecture-knowledge-base/README.md). `okf-tasks-combined-workspace.html` [joins both surfaces through an explicit programme map](./examples/combined-delivery-architecture/README.md) so delivery and architecture can be reviewed as one connected graph. Their Markdown/YAML source remains tracked under those example directories; regenerate it through `generate_complex_examples.py` rather than hand-editing generated records.

OKF 0.1 does not define a universal importance or reading-order field, so this profile uses the optional `navigation` extension documented in `SPEC.md`. `navigation.role` distinguishes `entry-point`, `foundational`, `supporting`, and `reference` concepts, while sparse `navigation.order` values establish a first-reading sequence within a role. This does not replace links or Task `priority`: links remain the relationship and hierarchy model, and Task priority remains execution urgency. In the graph, ADRs have their own visual class, entry points and foundational records carry stronger prominence, the reading selector highlights a chosen role, and every type key acts as a click-to-highlight filter without removing the rest of the graph.

Generate a custom interactive HTML graph and a GitHub-rendered Mermaid graph:

```text
python scripts/visualize_bundle.py \
  --bundle examples/visualization/tasks \
  --name "OKF Tasks visualization example" \
  --html local-docs/okf-tasks-visualization.html \
  --mermaid
```

Open the HTML file locally as the definitive three-view OKF workspace. Graph presents the complete document relationship mesh and isolates a selected document's neighbourhood without hiding the surrounding repository context. Its type key and reading-role selector highlight chosen classes while retaining graph context; ADRs, entry points, and foundational records are deliberately more prominent than ordinary supporting material. Its right panel turns that neighbourhood into a compact vertical Incoming → Selected → Outgoing focus view with clickable relationship cards, temporal and effort context, and a Reader shortcut instead of a full document rendering. Board provides lifecycle columns or compact rows for Tasks, with nested Workstreams, embedded effort evidence, estimates, tracker context, and exact temporal values. Reader provides a searchable repository tree, full Markdown document surface, contextual ancestry, connections, and heading navigation. Light mode is the default, dark mode persists locally, and timestamp comparison can flag possible drift across existing relationships without claiming that older content is stale. Embedded `Task.time[]` entries contribute evidence and effort to their Task. Small graphs use compact layout bounds and always fit the complete node set into the initial viewport. The generated file embeds pinned Cytoscape, Marked, and DOMPurify builds and loads pinned Mermaid for strict diagram rendering; task and document data are embedded as a sanitised JSON payload.

`--mermaid` without a path writes `<html-name>.mermaid.md` beside the HTML. The report avoids a single unbounded chart: it generates a connected-area overview, complete diagrams for manageable components, area slices with boundary context for large components, focussed neighbourhoods for high-connectivity concepts, and a lower-weight list of true isolates.

Temporal controls compare relationships through the declared `timestamp`, `created`, `started`, or `finished` event. Drift review highlights a linked source whose selected time is newer than its target and carries that signal into Board cards and rows. That ordering is a prompt to review the relationship, not proof of stale or incorrect content. A current bundle contains current record bodies; historical fact reconstruction requires retained historical concepts or repository history.

The visualisation is derived, never a second task database. Markdown/YAML records remain authoritative, every meaningful record edit advances `timestamp`, and the generated pages are rebuilt through the checked-in script rather than hand-edited.

The visualiser remains in this repository while its payload, CLI, and rendering semantics are evolving with the Tasks profile. A future `okf-visualizer` extraction is reasonable when it serves multiple OKF profiles, has an independently versioned payload/renderer contract, needs a separate release cadence, or gains consumers that should not depend on OKF Tasks. Until one of those thresholds is met, the in-repository implementation and release checks are the authoritative visualisation process.

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

Version 0.1 establishes portable reading prominence and first-reading order alongside embedded addressable time entries, first-class provider setup, and scoped external bindings. Normative changes require fixtures and agreement between the Python and TypeScript implementations; see [`GOVERNANCE.md`](./GOVERNANCE.md).

## Licence

Apache License 2.0. See [`LICENSE`](./LICENSE).
