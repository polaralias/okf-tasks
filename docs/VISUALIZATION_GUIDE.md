# Interactive visualization guide

The OKF Tasks viewer is a derived, read-only consumer. Markdown/YAML files remain canonical.

## Generate the review pages

From the repository root:

```text
python scripts/generate_local_docs.py --mermaid
```

This creates the ignored local review artifacts:

- `local-docs/okf-tasks-visualization.html` from `examples/visualization/tasks/`;
- `local-docs/okf-tasks-examples.html` from the complete `examples/` tree;
- `local-docs/okf-tasks-relationships.html` from the complete `examples/` tree, with stable source-bundle lanes and every explicit relationship retained as a labelled edge.
- sibling `*.mermaid.md` reports for the primary visualization and examples workspaces.

Use the relationship map when topology is the question: it groups records for spatial orientation but does not infer or replace relationships. The ordinary example page remains the neutral record browser.

All three pages use `scripts/visualize_bundle.py` and therefore share the same HTML, styling, interaction, security, and Markdown-rendering behavior. Verify that generated files are current with:

```text
python scripts/generate_local_docs.py --mermaid --check
```

Use `--output-dir <directory>` to generate disposable outputs for tests or review. Use the lower-level renderer when a different bundle or Mermaid output is required:

```text
python scripts/visualize_bundle.py \
  --bundle examples/visualization/tasks \
  --name "OKF Tasks visualization example" \
  --html local-docs/okf-tasks-visualization.html \
  --mermaid
```

With `--html`, a pathless `--mermaid` writes `<html-name>.mermaid.md` beside the interactive workspace. Pass `--mermaid <path>` when the report belongs elsewhere. `--markdown <path>` remains an explicit-path synonym for checked documentation workflows.

The Mermaid report scales by separating concerns: an area-level map shows how connected repository regions relate; manageable connected components render in full; large components split into area diagrams with dashed boundary context; the highest-connectivity concepts receive focused neighbourhood diagrams; and true isolates are listed rather than drawn with equal weight. Every connected node and edge remains represented without forcing the repository into one oversized diagram.

## Freshness and authority

The viewer labels each record's `timestamp` as **Last meaningful change** and shows `created`, `started`, and `finished` separately when present. The portable timestamp comes from OKF frontmatter; the viewer does not infer freshness from filesystem metadata or the generated HTML date.

The viewer is a derived consumer. The source Markdown/YAML bundle remains authoritative, and both generated pages must be regenerated from the shared renderer after a meaningful record or renderer change.

## Viewer behavior

- Graph, Board, and Reader are first-class tabs over one embedded bundle.
- Graph presents the complete document mesh. Compact document chips use class-colored borders, folder trails remain visible beneath them, and selecting a chip fades unrelated documents while revealing labels on its direct relationships.
- The Graph panel presents those direct relationships vertically as Incoming → Selected → Outgoing. Connected cards recenter the graph; the selected summary includes concise temporal and effort context plus a Reader shortcut, without duplicating the full Markdown document.
- The temporal selector compares Last meaningful change, Created, Started, or Finished. Drift review highlights relationships whose source has a newer selected value than its target. Treat every highlight as a review prompt only; timestamp order cannot prove semantic drift.
- Board groups Tasks into lifecycle columns or compact rows, nests their Workstreams, and displays estimates, recorded effort, embedded-time evidence, tracker context, link counts, and the selected temporal value.
- Embedded `Task.time[]` entries remain individually addressable through `#time:<id>` fragments and appear within their Task's evidence surfaces.
- Board selections use the detailed record pane with identity, status, description, temporal fields, Workstream and time evidence, connections, rendered Markdown, and collapsed raw source.
- The document browser includes every Markdown file below the selected source tree, including files that are not OKF records.
- The viewer opens in light mode on first use and persists a later light or dark choice locally.
- Every button exposes a hover label as well as an accessible name, including graph controls whose icons are otherwise ambiguous.
- Reader renders the selected file at near-full width with a persistent searchable tree on the left and ancestry, connection, metadata, and heading context on the right.
- Shared search filters Graph, Board, or Reader according to the active view. Graph fitting uses node-count-aware bounds and minimum desktop zoom for small bundles; Board layout, Board sorting, temporal comparison, and drift review remain independent controls.

## GitHub-style Markdown

The viewer enables Marked's GitHub-flavored Markdown mode for autolinks, tables, strikethrough, and task lists. It preserves sanitized HTML disclosure elements such as `<details>` and `<summary>`, and converts fenced `mermaid` blocks into diagrams.

All rendered HTML passes through DOMPurify. Mermaid runs with `securityLevel: strict`. If Marked or DOMPurify cannot load, the viewer displays the Markdown source as plain text rather than leaving the inspector empty. If Mermaid cannot load, its fenced source remains readable.

The generated HTML currently loads pinned browser builds from jsDelivr:

- Cytoscape `3.31.2`;
- Marked `16.1.2` using `lib/marked.umd.js`;
- DOMPurify `3.2.6`;
- Mermaid `11.10.1`.

Internet access is therefore needed for the interactive libraries when opening a generated file. The embedded repository content itself remains local.

## Temporal interpretation limits

The viewer operates on the current bundle. Selecting a temporal field compares the current values attached to records; it does not reconstruct the body or frontmatter that existed at an earlier time. Historical facts require retained superseded/versioned concepts or repository history. Plain Markdown documents without OKF temporal metadata remain available in Reader but cannot participate in timestamp drift comparison.
