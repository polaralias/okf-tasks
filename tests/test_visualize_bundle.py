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
        entry = self.root / "tasks" / "ship-viewer" / "time" / "session.md"
        task.parent.mkdir(parents=True)
        workstream.parent.mkdir(parents=True)
        entry.parent.mkdir(parents=True)
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
---
# Ship viewer

See the [UI workstream](./workstreams/ui.md).
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
        entry.write_text(
            """---
type: Time Entry
task: ship-viewer
entry: session
status: closed
actor: agent
started: 2026-07-17T20:00:00Z
finished: 2026-07-17T20:30:00Z
effort_minutes: 30
method: tracked
timestamp: 2026-07-17T20:30:00Z
---
# Time entry
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
                "tasks/ship-viewer/time/session",
            },
            ids,
        )
        relationships = {
            (edge["data"]["source"], edge["data"]["target"], edge["data"]["relationship"])
            for edge in graph["edges"]
        }
        self.assertIn(
            ("tasks/ship-viewer/workstreams/ui", "tasks/ship-viewer/task", "workstream"),
            relationships,
        )
        self.assertIn(
            ("tasks/ship-viewer/time/session", "tasks/ship-viewer/task", "time"),
            relationships,
        )
        self.assertNotIn(
            ("tasks/ship-viewer/task", "tasks/ship-viewer/workstreams/ui", "links"),
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
        self.assertEqual(3, len(parsed["nodes"]))

    def test_html_uses_the_pinned_markdown_browser_build_with_a_plain_text_fallback(self) -> None:
        graph = visualize_bundle.build_graph(visualize_bundle.read_records(self.root))
        generated = visualize_bundle.generate_html(graph, "Example")
        self.assertIn("marked@16.1.2/lib/marked.umd.js", generated)
        self.assertIn("function renderMarkdown(value)", generated)
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

    def test_html_prioritizes_rendered_markdown_and_collapses_raw_sources(self) -> None:
        graph = visualize_bundle.build_graph(visualize_bundle.read_records(self.root))
        generated = visualize_bundle.generate_html(graph, "Example")
        self.assertLess(generated.index('id="record-body"'), generated.index('id="raw-frontmatter"'))
        self.assertIn("<summary>Raw frontmatter</summary>", generated)
        self.assertIn("<summary>Complete source document</summary>", generated)
        self.assertIn('id="raw-document"', generated)

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

    def test_local_documentation_generator_builds_both_pages_from_the_same_viewer(self) -> None:
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
        for generated in (visualization, examples):
            self.assertIn('id="browse-documents"', generated)
            self.assertIn('id="theme"', generated)
            self.assertIn('id="fullscreen"', generated)
        checked = subprocess.run(
            [sys.executable, str(GENERATE_LOCAL_DOCS), "--output-dir", str(output), "--check"],
            cwd=SCRIPT.parents[1],
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, checked.returncode, checked.stderr)


if __name__ == "__main__":
    unittest.main()
