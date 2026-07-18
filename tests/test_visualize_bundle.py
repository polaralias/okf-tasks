from __future__ import annotations

import importlib.util
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "visualize_bundle.py"
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


if __name__ == "__main__":
    unittest.main()
