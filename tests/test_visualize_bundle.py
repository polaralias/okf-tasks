from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
SCRIPT = REPOSITORY / "scripts" / "visualize_bundle.py"
GENERATE_LOCAL_DOCS = REPOSITORY / "scripts" / "generate_local_docs.py"
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
timestamp: 2026-07-17T21:00:00Z
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

    def graph(self, include_documents: bool = False) -> dict[str, object]:
        records = visualize_bundle.read_records(self.root)
        documents = visualize_bundle.read_documents(self.root, records) if include_documents else None
        return visualize_bundle.build_graph(records, documents)

    def generated(self, include_documents: bool = True) -> str:
        return visualize_bundle.generate_html(self.graph(include_documents), "Example")

    def embedded_payload(self, generated: str) -> dict[str, object]:
        match = re.search(
            r'<script type="application/json" id="okf-bundle">(.*?)</script>',
            generated,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(match)
        return json.loads(match.group(1))

    def test_builds_task_workstream_and_fragment_addressed_time_relationships(self) -> None:
        graph = self.graph()
        ids = {node["data"]["id"] for node in graph["nodes"]}
        self.assertEqual({"tasks/ship-viewer/task", "tasks/ship-viewer/workstreams/ui"}, ids)
        relationships = {
            (
                edge["data"]["source"],
                edge["data"]["target"],
                edge["data"]["relationship"],
                edge["data"].get("fragment"),
            )
            for edge in graph["edges"]
        }
        self.assertIn(
            ("tasks/ship-viewer/task", "tasks/ship-viewer/task", "time", "time:session"),
            relationships,
        )
        self.assertIn(
            ("tasks/ship-viewer/workstreams/ui", "tasks/ship-viewer/task", "workstream", None),
            relationships,
        )

    def test_embeds_a_safe_dynamic_payload_in_the_definitive_workspace(self) -> None:
        task = self.root / "tasks" / "ship-viewer" / "task.md"
        task.write_text(
            task.read_text(encoding="utf-8").replace(
                "Render the task graph.", "Render </script><script>alert(1)</script> safely."
            ),
            encoding="utf-8",
        )
        generated = self.generated()
        self.assertNotIn("</script><script>alert(1)</script>", generated)
        payload = self.embedded_payload(generated)
        self.assertEqual("Example", payload["name"])
        self.assertEqual(2, len(payload["nodes"]))
        task_node = next(node["data"] for node in payload["nodes"] if node["data"]["type"] == "Task")
        self.assertEqual("session", task_node["frontmatter"]["time"][0]["id"])

    def test_preserves_the_definitive_graph_board_reader_identity(self) -> None:
        generated = self.generated()
        self.assertIn('<button class="view-tab" data-view="graph"', generated)
        self.assertIn('<button class="view-tab" data-view="board"', generated)
        self.assertIn('<button class="view-tab" data-view="reader"', generated)
        self.assertIn('class="wordmark"', generated)
        self.assertIn('class="detail" id="detail"', generated)
        self.assertIn('--serif:Charter,"Bitstream Charter"', generated)
        self.assertIn('--accent:#2b4bc4', generated)

    def test_uses_embedded_task_time_without_time_nodes_or_documents(self) -> None:
        generated = self.generated()
        payload = self.embedded_payload(generated)
        self.assertNotIn("Time Entry", {node["data"]["type"] for node in payload["nodes"]})
        self.assertIn("times:Array.isArray(t.frontmatter?.time)", generated)
        self.assertIn("never become records, documents, or graph nodes", generated)
        self.assertNotIn("const timeEntries=", generated)

    def test_graph_keeps_relationships_visible_and_focusable(self) -> None:
        generated = self.generated()
        self.assertIn('id="cy"', generated)
        self.assertIn("function buildGraph()", generated)
        self.assertIn("function applyGraphFocus()", generated)
        self.assertIn('"label":"data(elabel)"', generated)
        self.assertIn('cy.on("tap","node.main"', generated)
        self.assertIn('id="fit-btn"', generated)

    def test_board_supports_columns_rows_effort_and_embedded_time_evidence(self) -> None:
        generated = self.generated()
        self.assertIn('data-layout="columns"', generated)
        self.assertIn('data-layout="rows"', generated)
        self.assertIn("function buildKanban()", generated)
        self.assertIn("function buildRows()", generated)
        self.assertIn("function effortHtml(logged,estimate)", generated)
        self.assertIn("m.times.length", generated)
        self.assertIn("e.finished||e.started", generated)

    def test_reader_renders_github_markdown_mermaid_and_repository_navigation(self) -> None:
        (self.root / "README.md").write_text("# Repository guide\n", encoding="utf-8")
        generated = self.generated()
        payload = self.embedded_payload(generated)
        self.assertIn("README.md", {document["path"] for document in payload["documents"]})
        self.assertIn('class="reader"', generated)
        self.assertIn('id="rtree"', generated)
        self.assertIn("function buildTree()", generated)
        self.assertIn("function openReader(path)", generated)
        self.assertIn("marked.parse(text||\"\")", generated)
        self.assertIn("code.language-mermaid", generated)
        self.assertIn('securityLevel:"strict"', generated)
        self.assertIn("DOMPurify.sanitize", generated)

    def test_adds_temporal_comparison_and_evidence_cautious_drift_indicators(self) -> None:
        generated = self.generated()
        self.assertIn('id="temporal-field"', generated)
        self.assertIn('id="drift-btn"', generated)
        self.assertIn("const driftEdgeKeys=()", generated)
        self.assertIn('selector:"edge.drift"', generated)
        self.assertIn("possible timestamp-order signal", generated)
        self.assertIn("review semantics before calling content stale", generated)
        self.assertIn('className="bcard"', generated)
        self.assertIn('possibleDrift?" drift":""', generated)

    def test_defaults_to_light_and_persists_theme_choice(self) -> None:
        generated = self.generated()
        self.assertIn('<html lang="en" data-theme="light">', generated)
        self.assertIn('localStorage.getItem("okf-proto-theme")', generated)
        self.assertIn('localStorage.setItem("okf-proto-theme",next)', generated)
        self.assertIn('@media(prefers-reduced-motion:reduce)', generated)

    def test_generates_github_mermaid(self) -> None:
        markdown = visualize_bundle.generate_markdown(self.graph(), "Example", "tasks")
        self.assertIn(chr(96) * 3 + "mermaid", markdown)
        self.assertIn("Build UI · ready", markdown)
        self.assertIn("time:session", markdown)

    def test_local_documentation_generator_builds_all_workspace_pages(self) -> None:
        output = self.root / "local-docs"
        completed = subprocess.run(
            [sys.executable, str(GENERATE_LOCAL_DOCS), "--output-dir", str(output)],
            cwd=REPOSITORY,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        for name in (
            "okf-tasks-visualization.html",
            "okf-tasks-examples.html",
            "okf-tasks-relationships.html",
        ):
            generated = (output / name).read_text(encoding="utf-8")
            self.assertIn('data-view="graph"', generated)
            self.assertIn('data-view="board"', generated)
            self.assertIn('data-view="reader"', generated)
            self.assertNotIn("__GRAPH__", generated)
        checked = subprocess.run(
            [sys.executable, str(GENERATE_LOCAL_DOCS), "--output-dir", str(output), "--check"],
            cwd=REPOSITORY,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, checked.returncode, checked.stderr)

    def test_repository_skill_bundles_the_same_renderer_and_template(self) -> None:
        bundled = REPOSITORY / "skills" / "okf-task-lifecycle" / "scripts" / "visualize_bundle.py"
        self.assertEqual(SCRIPT.read_bytes(), bundled.read_bytes())
        self.assertEqual(
            SCRIPT.with_name("visualizer_template.html").read_bytes(),
            bundled.with_name("visualizer_template.html").read_bytes(),
        )


if __name__ == "__main__":
    unittest.main()
