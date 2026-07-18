# Interactive visualization guide

The OKF Tasks viewer is a derived, read-only consumer. Markdown/YAML files remain canonical.

## Generate the review pages

From the repository root:

```text
python scripts/generate_local_docs.py
```

This creates the ignored local review artifacts:

- `local-docs/okf-tasks-visualization.html` from `examples/visualization/tasks/`;
- `local-docs/okf-tasks-examples.html` from the complete `examples/` tree.

Both pages use `scripts/visualize_bundle.py` and therefore share the same HTML, styling, interaction, security, and Markdown-rendering behavior. Verify that generated files are current with:

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

## Viewer behavior

- Relationship labels remain visible without selecting a node and gain stronger emphasis around the selected record.
- The inspector presents summarized record metadata, rendered Markdown, backlinks, then collapsed raw YAML and complete-source disclosures.
- The document browser includes every Markdown file below the selected source tree, including files that are not OKF records.
- The theme control persists light or dark mode locally.
- The fullscreen control uses the browser Fullscreen API and resizes/refits the graph when entering or leaving fullscreen.
- Search, type filters, layout selection, graph fitting, and reset remain independent controls.

## GitHub-style Markdown

The viewer enables Marked's GitHub-flavored Markdown mode for autolinks, tables, strikethrough, and task lists. It preserves sanitized HTML disclosure elements such as `<details>` and `<summary>`, and converts fenced `mermaid` blocks into diagrams.

All rendered HTML passes through DOMPurify. Mermaid runs with `securityLevel: strict`. If Marked or DOMPurify cannot load, the viewer displays the Markdown source as plain text rather than leaving the inspector empty. If Mermaid cannot load, its fenced source remains readable.

The generated HTML currently loads pinned browser builds from jsDelivr:

- Cytoscape `3.31.2`;
- Marked `16.1.2` using `lib/marked.umd.js`;
- DOMPurify `3.2.6`;
- Mermaid `11.10.1`.

Internet access is therefore needed for the interactive libraries when opening a generated file. The embedded repository content itself remains local.
