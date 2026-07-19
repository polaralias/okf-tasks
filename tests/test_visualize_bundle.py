from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "visualize_bundle.py"
GENERATE_LOCAL_DOCS = Path(__file__).resolve().parents[1] / "scripts" / "generate_local_docs.py"
SPEC = importlib.util.spec_from_file_location("visualize_bundle", SCRIPT)
assert SPEC and SPEC.loader
visualize_bundle = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = visualize_bundle
SPEC.loader.exec_module(visualize_bundle)


class VisualizationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        task = self.root / "tasks" / "ship-viewer" / "task.md"
        workstream = self.root / "tasks" / "ship-viewer" / "workstreams" / "ui.md"
        task.parent.mkdir(parents=True)
        workstream.parent.mkdir(parents=True)
        task.write_text(
            """---
type: Task
task: ship-viewer
title: Ship viewer
description: Render the task graph.
status: in-progress
created: 2026-07-17T20:00:00Z
timestamp: 2026-07-17T20:00:00Z
tags: [visualization]
started: 2026-07-17T20:00:00Z
effort_minutes: 30
time:
  - id: session
    status: closed
    actor: agent
    started: 2026-07-17T20:00:00Z
    finished: 2026-07-17T20:30:00Z
    elapsed_minutes: 30
    effort_minutes: 30
    method: tracked
---
# Ship viewer

See the [UI workstream](./workstreams/ui.md).
Review the [recorded session](./task.md#time:session).
""",
            encoding="utf-8",
        )
        workstream.write_text(
            """---
type: Workstream
task: ship-viewer
workstream: ui
title: Build UI
description: Build the interactive graph.
status: ready
created: 2026-07-17T20:00:00Z
timestamp: 2026-07-17T20:00:00Z
---
# Build UI
""",
            encoding="utf-8",
        )
    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_builds_task_workstream_and_time_relationships(self) -> None:
        records = visualize_bundle.read_records(self.root)
        graph = visualize_bundle.build_graph(records)
        ids = {node["data"]["id"] for node in graph["nodes"]}
        self.assertEqual(
            {
                "tasks/ship-viewer/task",
                "tasks/ship-viewer/workstreams/ui",
            },
            ids,
        )
        relationships = {
            (edge["data"]["source"], edge["data"]["target"], edge["data"]["relationship"], edge["data"].get("fragment"))
            for edge in graph["edges"]
        }
        self.assertIn(
            ("tasks/ship-viewer/workstreams/ui", "tasks/ship-viewer/task", "workstream", None),
            relationships,
        )
        self.assertIn(
            ("tasks/ship-viewer/task", "tasks/ship-viewer/task", "time", "time:session"),
            relationships,
        )
        self.assertNotIn(
            ("tasks/ship-viewer/task", "tasks/ship-viewer/workstreams/ui", "links", None),
            relationships,
            "Structured relationships should replace duplicate generic Markdown edges.",
        )

    def test_generates_github_mermaid(self) -> None:
        graph = visualize_bundle.build_graph(visualize_bundle.read_records(self.root))
        markdown = visualize_bundle.generate_markdown(graph, "Example", "tasks")
        self.assertIn(chr(96) * 3 + "mermaid", markdown)
        self.assertIn("classDef task", markdown)
        self.assertIn("Build UI · ready", markdown)

    def test_html_embeds_graph_without_raw_script_breakout(self) -> None:
        task = self.root / "tasks" / "ship-viewer" / "task.md"
        text = task.read_text(encoding="utf-8").replace(
            "Render the task graph.",
            "Render </script><script>alert(1)</script> safely.",
        )
        task.write_text(text, encoding="utf-8")
        graph = visualize_bundle.build_graph(visualize_bundle.read_records(self.root))
        generated = visualize_bundle.generate_html(graph, "Example")
        self.assertNotIn("</script><script>alert(1)</script>", generated)
        match = re.search(r"window\.OKF_GRAPH=(\{.*\});</script>", generated)
        self.assertIsNotNone(match)
        parsed = json.loads(match.group(1))
        self.assertEqual(2, len(parsed["nodes"]))

    def test_html_uses_the_pinned_markdown_browser_build_with_a_plain_text_fallback(self) -> None:
        graph = visualize_bundle.build_graph(visualize_bundle.read_records(self.root))
        generated = visualize_bundle.generate_html(graph, "Example")
        self.assertIn("marked@16.1.2/lib/marked.umd.js", generated)
        self.assertIn('function renderMarkdown(value,body=$("record-body"))', generated)
        self.assertIn("body.textContent=value", generated)

    def test_html_keeps_relationship_labels_visible_and_legible(self) -> None:
        graph = visualize_bundle.build_graph(visualize_bundle.read_records(self.root))
        generated = visualize_bundle.generate_html(graph, "Example")
        self.assertNotIn('label:""', generated)
        self.assertIn('label:"data(relationship)"', generated)
        self.assertIn('"font-size":9', generated)
        self.assertIn('"text-background-opacity":.96', generated)

    def test_html_exposes_a_real_fullscreen_toggle(self) -> None:
        graph = visualize_bundle.build_graph(visualize_bundle.read_records(self.root))
        generated = visualize_bundle.generate_html(graph, "Example")
        self.assertIn('id="fullscreen"', generated)
        self.assertIn("requestFullscreen()", generated)
        self.assertIn("document.exitFullscreen()", generated)
        self.assertIn('addEventListener("fullscreenchange"', generated)

    def test_html_supports_a_persisted_light_and_dark_theme(self) -> None:
        graph = visualize_bundle.build_graph(visualize_bundle.read_records(self.root))
        generated = visualize_bundle.generate_html(graph, "Example")
        self.assertIn(':root[data-theme="light"]', generated)
        self.assertIn('id="theme"', generated)
        self.assertIn('localStorage.getItem("okf-theme")', generated)
        self.assertIn('localStorage.setItem("okf-theme",theme)', generated)

    def test_html_defaults_to_light_and_labels_every_button(self) -> None:
        graph = visualize_bundle.build_graph(visualize_bundle.read_records(self.root))
        generated = visualize_bundle.generate_html(graph, "Example")
        self.assertIn('document.documentElement.dataset.theme=savedTheme||"light"', generated)
        self.assertIn('function labelButtons()', generated)
        self.assertIn('button.dataset.tooltip=label', generated)
        self.assertIn('button.title=label', generated)
        self.assertIn('.icon-button[data-tooltip]:hover:after', generated)

    def test_html_prioritizes_rendered_markdown_and_collapses_raw_sources(self) -> None:
        graph = visualize_bundle.build_graph(visualize_bundle.read_records(self.root))
        generated = visualize_bundle.generate_html(graph, "Example")
        self.assertLess(generated.index('id="record-body"'), generated.index('id="raw-frontmatter"'))
        self.assertIn("<summary>Raw frontmatter</summary>", generated)
        self.assertIn("<summary>Complete source document</summary>", generated)
        self.assertIn('id="raw-document"', generated)

    def test_html_surfaces_explicit_record_timestamps(self) -> None:
        graph = visualize_bundle.build_graph(visualize_bundle.read_records(self.root))
        generated = visualize_bundle.generate_html(graph, "Example")
        self.assertIn('id="record-last-updated"', generated)
        self.assertIn('id="record-created"', generated)
        self.assertIn('id="record-started"', generated)
        self.assertIn('id="record-finished"', generated)
        self.assertIn('Last meaningful change', generated)
        self.assertIn('function setRecordTime(id,value)', generated)
        self.assertIn('setRecordTime("record-last-updated",d.frontmatter?.timestamp)', generated)

    def test_html_renders_github_flavored_markdown_and_mermaid_safely(self) -> None:
        graph = visualize_bundle.build_graph(visualize_bundle.read_records(self.root))
        generated = visualize_bundle.generate_html(graph, "Example")
        self.assertIn("mermaid@11.10.1/dist/mermaid.min.js", generated)
        self.assertIn("code.language-mermaid", generated)
        self.assertIn('securityLevel:"strict"', generated)
        self.assertIn("marked.parse(value,{gfm:true,breaks:false})", generated)
        self.assertIn(".markdown details", generated)
        self.assertIn(".markdown .task-list-item", generated)

    def test_html_can_browse_the_full_markdown_document_tree(self) -> None:
        (self.root / "README.md").write_text("# Repository guide\n", encoding="utf-8")
        records = visualize_bundle.read_records(self.root)
        graph = visualize_bundle.build_graph(records, visualize_bundle.read_documents(self.root, records))
        paths = {document["path"] for document in graph["documents"]}
        self.assertIn("README.md", paths)
        self.assertIn("tasks/ship-viewer/task.md", paths)
        generated = visualize_bundle.generate_html(graph, "Example")
        self.assertIn('id="browse-documents"', generated)
        self.assertIn('id="document-tree"', generated)
        self.assertIn("function showDocument(path)", generated)
        self.assertIn(
            "cursor.folders[part]??={folders:{},files:[]};cursor=cursor.folders[part]",
            generated,
        )
        self.assertNotIn("for(const document of graph.documents", generated)

    def test_html_has_a_full_page_document_reader_tab_with_a_persistent_tree(self) -> None:
        (self.root / "README.md").write_text("# Repository guide\n\nRead the docs.\n", encoding="utf-8")
        records = visualize_bundle.read_records(self.root)
        graph = visualize_bundle.build_graph(records, visualize_bundle.read_documents(self.root, records))
        generated = visualize_bundle.generate_html(graph, "Example")
        self.assertIn('role="tablist"', generated)
        self.assertIn('id="graph-tab"', generated)
        self.assertIn('id="documents-tab"', generated)
        self.assertIn('id="documents-view"', generated)
        self.assertIn('id="document-reader"', generated)
        self.assertIn('id="reader-tree"', generated)
        self.assertIn('grid-template-columns:minmax(0,1fr) 280px', generated)
        self.assertIn("function switchView(view)", generated)
        self.assertIn("function showReaderDocument(path)", generated)
        self.assertIn('renderTree(tree,$("reader-tree"),showReaderDocument)', generated)

    def test_html_defaults_to_grid_and_distinguishes_record_classes(self) -> None:
        graph = visualize_bundle.build_graph(visualize_bundle.read_records(self.root))
        generated = visualize_bundle.generate_html(graph, "Example")
        self.assertIn('<option value="grid" selected>Grid</option>', generated)
        self.assertIn('layout:{name:"grid"', generated)
        self.assertIn('.selector(\'node[type = "Task"]\')', generated)
        self.assertIn('.selector(\'node[type = "Workstream"]\')', generated)
        self.assertNotIn('.selector(\'node[type = "Time Entry"]\')', generated)
        self.assertIn('width:"data(nodeWidth)"', generated)
        self.assertIn('d.metric=', generated)

    def test_html_exposes_temporal_navigation_and_timestamp_drift_review(self) -> None:
        graph = visualize_bundle.build_graph(visualize_bundle.read_records(self.root))
        generated = visualize_bundle.generate_html(graph, "Example")
        self.assertIn('id="temporal-field"', generated)
        self.assertIn('id="time-range"', generated)
        self.assertIn('id="time-output"', generated)
        self.assertIn('id="drift-review"', generated)
        self.assertIn('<option value="timeline">Timeline</option>', generated)
        self.assertIn('function temporalValue(data,field=temporalField)', generated)
        self.assertIn('function updateTemporalRange(reset=false)', generated)
        self.assertIn('function updateDrift()', generated)
        self.assertIn('function runLayout(name)', generated)
        self.assertIn('edge.possible-drift', generated)
        self.assertIn('Timestamp ordering is a review signal, not proof of drift.', generated)

    def test_relationship_html_groups_bundles_without_replacing_explicit_edges(self) -> None:
        records = visualize_bundle.read_records(self.root)
        graph = visualize_bundle.build_graph(records)
        generated = visualize_bundle.generate_relationship_html(graph, "Relationships")
        self.assertIn('OKF Tasks · relationship map', generated)
        self.assertIn('<option value="relationship" selected>Relationship layout</option>', generated)
        self.assertIn('node[virtual]', generated)
        self.assertIn('Bundle lane', generated)
        self.assertIn('label:"data(relationship)"', generated)
        self.assertIn('"relationshipPosition":', generated)
        self.assertIn('"relationship": "workstream"', generated)

    def test_local_documentation_generator_builds_all_review_pages(self) -> None:
        output = self.root / "local-docs"
        completed = subprocess.run(
            [sys.executable, str(GENERATE_LOCAL_DOCS), "--output-dir", str(output)],
            cwd=SCRIPT.parents[1],
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        visualization = (output / "okf-tasks-visualization.html").read_text(encoding="utf-8")
        examples = (output / "okf-tasks-examples.html").read_text(encoding="utf-8")
        relationships = (output / "okf-tasks-relationships.html").read_text(encoding="utf-8")
        for generated in (visualization, examples):
            self.assertIn('id="browse-documents"', generated)
            self.assertIn('id="theme"', generated)
            self.assertIn('id="fullscreen"', generated)
        self.assertIn('OKF Tasks · relationship map', relationships)
        self.assertIn('Bundle lane', relationships)
        checked = subprocess.run(
            [sys.executable, str(GENERATE_LOCAL_DOCS), "--output-dir", str(output), "--check"],
            cwd=SCRIPT.parents[1],
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, checked.returncode, checked.stderr)

    def test_repository_skill_bundles_the_same_visualizer(self) -> None:
        bundled = SCRIPT.parents[1] / "skills" / "okf-task-lifecycle" / "scripts" / "visualize_bundle.py"
        self.assertEqual(SCRIPT.read_bytes(), bundled.read_bytes())


if __name__ == "__main__":
    unittest.main()
