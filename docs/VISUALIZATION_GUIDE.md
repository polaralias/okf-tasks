# Interactive visualization guide

The OKF Tasks viewer is a derived, read-only consumer. Markdown/YAML files remain canonical.

## Generate the review pages

From the repository root:

```text
python scripts/generate_local_docs.py
```

This creates the ignored local review artifacts:

- `local-docs/okf-tasks-visualization.html` from `examples/visualization/tasks/`;
- `local-docs/okf-tasks-examples.html` from the complete `examples/` tree;
- `local-docs/okf-tasks-relationships.html` from the complete `examples/` tree, with stable source-bundle lanes and every explicit relationship retained as a labelled edge.

Use the relationship map when topology is the question: it groups records for spatial orientation but does not infer or replace relationships. The ordinary example page remains the neutral record browser.

All three pages use `scripts/visualize_bundle.py` and therefore share the same HTML, styling, interaction, security, and Markdown-rendering behavior. Verify that generated files are current with:

```text
python scripts/generate_local_docs.py --check
```

Use `--output-dir <directory>` to generate disposable outputs for tests or review. Use the lower-level renderer when a different bundle or Mermaid output is required:

```text
python scripts/visualize_bundle.py \
  --bundle examples/visualization/tasks \
  --name "OKF Tasks visualization example" \
  --html local-docs/okf-tasks-visualization.html \
  --markdown docs/VISUALIZATION.md
```

## Freshness and authority

The viewer labels each record's `timestamp` as **Last meaningful change** and shows `created`, `started`, and `finished` separately when present. The portable timestamp comes from OKF frontmatter; the viewer does not infer freshness from filesystem metadata or the generated HTML date.

The viewer is a derived consumer. The source Markdown/YAML bundle remains authoritative, and both generated pages must be regenerated from the shared renderer after a meaningful record or renderer change.

## Viewer behavior

- Graph, Kanban, and Documents are first-class tabs over one embedded bundle. Selecting a connected record, Topology node, or Kanban card opens the same detailed preview.
- Graph opens in Focus mode with the selected record between readable incoming and outgoing relationship cards. Selecting a connected card recentres the explorer without losing the shared preview.
- Topology mode retains the complete bundle overview. Grid is its initial layout for routine review, while Timeline lays record types into lanes and orders them by the selected temporal field.
- The temporal rail can filter the current Graph and Kanban records through Last meaningful change, Created, Started, or Finished. Exact RFC 3339 values remain available in titles while the control uses friendly local dates.
- Drift review highlights relationships whose source has a newer selected timestamp than its target. Treat these as possible review signals only; timestamp order cannot prove semantic drift.
- The Kanban view groups Tasks and Workstreams by lifecycle status, includes edited dates and recorded effort, and carries timestamp-drift hints into the board when drift review is active.
- The shared context rail summarizes recorded time by Workstream so commitment across concurrent work remains visible while Graph or Kanban is active.
- Focus cards expose type, lifecycle status, edited date, effort, connection count, description, document availability, and the complete record identifier without forcing that detail into topology labels.
- Topology uses one bounded node shape with a class-colored border. Its compact title and type/status label are truncated before rendering so text cannot escape node boundaries.
- Topology relationship labels are revealed for the selected record and its neighbours. Focus mode keeps the same labels readable at all times on direct relationship cards.
- The shared preview presents summarized record metadata, rendered Markdown, incoming and outgoing relationships, then collapsed raw YAML and complete-source disclosures.
- The document browser includes every Markdown file below the selected source tree, including files that are not OKF records.
- The viewer opens in dark mode on first use and persists a later light or dark choice locally.
- Every button exposes a hover label as well as an accessible name, including graph controls whose icons are otherwise ambiguous.
- The Documents view renders the selected file at near-full width with a persistent searchable tree on the left and a generated heading outline on the right.
- Graph and Documents expose separate fullscreen controls through the browser Fullscreen API. Graph resizes and refits when fullscreen changes.
- Search, type filters, Focus/Topology switching, topology layout selection, graph fitting, and reset remain independent controls in the Graph tab.

## GitHub-style Markdown

The viewer enables Marked's GitHub-flavored Markdown mode for autolinks, tables, strikethrough, and task lists. It preserves sanitized HTML disclosure elements such as `<details>` and `<summary>`, and converts fenced `mermaid` blocks into diagrams.

All rendered HTML passes through DOMPurify. Mermaid runs with `securityLevel: strict`. If Marked or DOMPurify cannot load, the viewer displays the Markdown source as plain text rather than leaving the inspector empty. If Mermaid cannot load, its fenced source remains readable.

The generated HTML currently loads pinned browser builds from jsDelivr:

- Cytoscape `3.31.2`;
- Marked `16.1.2` using `lib/marked.umd.js`;
- DOMPurify `3.2.6`;
- Mermaid `11.10.1`.
- Material Design Icons Webfont `@mdi/font` `7.4.47`, licensed Apache-2.0 by Pictogrammers.

Internet access is therefore needed for the interactive libraries when opening a generated file. The embedded repository content itself remains local.

## Temporal interpretation limits

The viewer operates on the current bundle. Moving the time control earlier shows which current records have a selected event at or before that point; it does not reconstruct the body or frontmatter that existed then. Historical facts require retained superseded/versioned concepts or repository history. Plain Markdown documents without OKF temporal metadata remain available in Documents view but cannot participate in timestamp drift comparison.
