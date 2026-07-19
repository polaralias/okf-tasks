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
GENERATE_COMPLEX_EXAMPLES = REPOSITORY / "scripts" / "generate_complex_examples.py"
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
    activity: implementation
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

    def test_uses_embedded_task_time_as_task_data(self) -> None:
        generated = self.generated()
        payload = self.embedded_payload(generated)
        task = next(node["data"] for node in payload["nodes"] if node["data"]["type"] == "Task")
        self.assertEqual("session", task["frontmatter"]["time"][0]["id"])
        self.assertIn("times:Array.isArray(t.frontmatter?.time)", generated)
        self.assertIn("Time is canonical Task frontmatter data", generated)

    def test_graph_keeps_relationships_visible_and_focusable(self) -> None:
        generated = self.generated()
        self.assertIn('id="cy"', generated)
        self.assertIn("function buildGraph()", generated)
        self.assertIn("function applyGraphFocus()", generated)
        self.assertIn('"label":"data(elabel)"', generated)
        self.assertIn('cy.on("tap","node.main"', generated)
        self.assertIn('id="fit-btn"', generated)

    def test_graph_uses_a_compact_vertical_relationship_focus_panel(self) -> None:
        generated = self.generated()
        self.assertIn("function renderGraphFocus(host)", generated)
        self.assertIn('className="graph-focus-flow"', generated)
        self.assertIn('graphFocusLane("Incoming",incoming,"incoming")', generated)
        self.assertIn('graphFocusLane("Outgoing",outgoing,"outgoing")', generated)
        self.assertIn('if(state.view==="graph"){renderGraphFocus(host)', generated)
        focus = generated.split("function renderGraphFocus(host)", 1)[1].split(
            "function renderRecordDetail", 1
        )[0]
        self.assertNotIn("renderMd(", focus)
        self.assertIn("Open in Reader", focus)

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
        self.assertIn("## Connected-area overview", markdown)
        self.assertIn("## Connected component 1", markdown)
        self.assertIn("## Key concept neighbourhoods", markdown)
        self.assertIn("Build UI · ready", markdown)
        self.assertIn("time:session", markdown)

    def test_visualization_manifest_covers_normative_generation_modes(self) -> None:
        manifest = json.loads((REPOSITORY / "conformance" / "visualization-manifest.json").read_text(encoding="utf-8"))
        case_ids = {case["id"] for case in manifest["cases"]}
        self.assertEqual(
            {"scalable-mermaid-report", "dynamic-small-graph-framing", "paired-derived-output"},
            case_ids,
        )

    def test_mermaid_flag_places_report_beside_html(self) -> None:
        html = self.root / "review.html"
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "--bundle", str(self.root), "--html", str(html), "--mermaid"],
            cwd=REPOSITORY,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        report = html.with_suffix(".mermaid.md")
        self.assertTrue(report.is_file())
        self.assertIn("## Connected component 1", report.read_text(encoding="utf-8"))

    def test_large_mermaid_component_splits_by_area_with_boundary_context(self) -> None:
        nodes = []
        edges = []
        for index in range(20):
            area = "alpha" if index < 10 else "beta"
            node_id = f"{area}/tasks/task-{index}/task"
            nodes.append({"data": {"id": node_id, "label": f"Task {index}", "type": "Task", "status": "ready"}})
            if index:
                previous_area = "alpha" if index - 1 < 10 else "beta"
                edges.append({"data": {"id": f"e{index}", "source": f"{previous_area}/tasks/task-{index - 1}/task", "target": node_id, "relationship": "depends on"}})
        markdown = visualize_bundle.generate_markdown({"nodes": nodes, "edges": edges}, "Large", "tasks")
        self.assertIn("### alpha", markdown)
        self.assertIn("### beta", markdown)
        self.assertIn("classDef boundary", markdown)
        for index in range(20):
            self.assertIn(f"Task {index} · ready", markdown)

    def test_small_graph_uses_compact_layout_and_always_fits(self) -> None:
        generated = self.generated()
        self.assertIn("function graphLayoutMetrics(count)", generated)
        self.assertIn("startRadius:compact?Math.min(190,80+count*14):340", generated)
        self.assertIn("cy.fit(cy.elements(),metrics.padding);", generated)
        self.assertNotIn("minimumZoom", generated)
        self.assertIn('window.addEventListener("resize"', generated)
        self.assertIn("fitGraph();", generated)

    def test_complex_examples_are_current_and_dense(self) -> None:
        checked = subprocess.run(
            [sys.executable, str(GENERATE_COMPLEX_EXAMPLES), "--root", str(REPOSITORY), "--check"],
            cwd=REPOSITORY,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, checked.returncode, checked.stdout + checked.stderr)
        expectations = {
            "complex-task-portfolio": (50, 45),
            "architecture-knowledge-base": (57, 55),
        }
        for name, (minimum_records, minimum_edges) in expectations.items():
            source = REPOSITORY / "examples" / name
            records = visualize_bundle.read_records(source)
            graph = visualize_bundle.build_graph(records, visualize_bundle.read_documents(source, records))
            with self.subTest(name=name):
                self.assertGreaterEqual(len(records), minimum_records)
                self.assertGreaterEqual(len(graph["edges"]), minimum_edges)

    def test_local_documentation_generator_builds_all_workspace_pages(self) -> None:
        output = self.root / "local-docs"
        completed = subprocess.run(
            [sys.executable, str(GENERATE_LOCAL_DOCS), "--output-dir", str(output), "--mermaid"],
            cwd=REPOSITORY,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        for name in (
            "okf-tasks-visualization.html",
            "okf-tasks-complex-task-portfolio.html",
            "okf-tasks-architecture-knowledge-base.html",
            "okf-tasks-examples.html",
            "okf-tasks-relationships.html",
        ):
            generated = (output / name).read_text(encoding="utf-8")
            self.assertIn('data-view="graph"', generated)
            self.assertIn('data-view="board"', generated)
            self.assertIn('data-view="reader"', generated)
            self.assertNotIn("__GRAPH__", generated)
        for name in (
            "okf-tasks-visualization.mermaid.md",
            "okf-tasks-complex-task-portfolio.mermaid.md",
            "okf-tasks-architecture-knowledge-base.mermaid.md",
            "okf-tasks-examples.mermaid.md",
        ):
            generated = (output / name).read_text(encoding="utf-8")
            self.assertIn("## Connected-area overview", generated)
            self.assertIn(chr(96) * 3 + "mermaid", generated)
        checked = subprocess.run(
            [sys.executable, str(GENERATE_LOCAL_DOCS), "--output-dir", str(output), "--mermaid", "--check"],
            cwd=REPOSITORY,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, checked.returncode, checked.stderr)

    def test_repository_skill_bundles_the_same_renderer_and_template(self) -> None:
        bundled = REPOSITORY / "skills" / "okf-task-lifecycle" / "scripts" / "visualize_bundle.py"
        self.assertEqual(SCRIPT.read_bytes(), bundled.read_bytes())
        self.assertEqual(
            GENERATE_COMPLEX_EXAMPLES.read_bytes(),
            bundled.with_name("generate_complex_examples.py").read_bytes(),
        )
        self.assertEqual(
            SCRIPT.with_name("visualizer_template.html").read_bytes(),
            bundled.with_name("visualizer_template.html").read_bytes(),
        )


if __name__ == "__main__":
    unittest.main()
