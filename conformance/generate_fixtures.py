#!/usr/bin/env python3
"""Generate deterministic OKF Tasks conformance fixtures."""

from __future__ import annotations

import argparse
import copy
import filecmp
import importlib.util
import shutil
import tempfile
from pathlib import Path
from typing import Any

import yaml


REPOSITORY = Path(__file__).resolve().parents[1]
CLI_PATH = REPOSITORY / "skills" / "okf-task-lifecycle" / "scripts" / "okf_tasks.py"
SPEC = importlib.util.spec_from_file_location("okf_tasks_fixture_cli", CLI_PATH)
assert SPEC and SPEC.loader
cli = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cli)

STAMP = "2026-07-17T09:00:00Z"
LATER = "2026-07-17T10:00:00Z"
TASK_BODY = """# {title}

## Outcome

Produce the stated outcome.

## Scope

- Included: the fixture contract.

## Acceptance

- [ ] The fixture is evaluated.

## Evidence

- Conformance fixture.
"""
WORKSTREAM_BODY = """# {title}

## Assigned outcome

Deliver the workstream outcome.

## Acceptance and validation

- [ ] Validate the workstream.

## Evidence

- Conformance fixture.

## Handoff

- Return evidence to the parent task.
"""
TIME_BODY = """# Time entry

## Summary

Fixture effort.

## Basis

Explicit fixture values.

## Activity

- Conformance work.
"""


def write_document(path: Path, metadata: dict[str, Any], body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frontmatter = yaml.safe_dump(metadata, sort_keys=False, allow_unicode=True).rstrip()
    path.write_text(f"---\n{frontmatter}\n---\n\n{body}", encoding="utf-8")


def task(slug: str = "fixture-task", **updates: Any) -> dict[str, Any]:
    value: dict[str, Any] = {
        "type": "Task",
        "task": slug,
        "title": "Fixture task",
        "description": "Exercise one portable task conformance rule.",
        "status": "ready",
        "created": STAMP,
        "timestamp": STAMP,
    }
    value.update(updates)
    return value


def workstream(task_slug: str = "fixture-task", slug: str = "delivery", **updates: Any) -> dict[str, Any]:
    value: dict[str, Any] = {
        "type": "Workstream",
        "task": task_slug,
        "workstream": slug,
        "title": "Delivery workstream",
        "description": "Deliver an independently validated part of the task.",
        "status": "ready",
        "created": STAMP,
        "timestamp": STAMP,
    }
    value.update(updates)
    return value


def time_entry(slug: str, **updates: Any) -> dict[str, Any]:
    value: dict[str, Any] = {
        "type": "Time Entry",
        "task": "fixture-task",
        "entry": slug,
        "status": "closed",
        "actor": "agent",
        "started": STAMP,
        "finished": LATER,
        "elapsed_minutes": 60,
        "effort_minutes": 60,
        "method": "manual",
        "timestamp": LATER,
    }
    value.update(updates)
    return value


def fixture(root: Path, category: str, name: str, task_meta: dict[str, Any], body: str | None = None) -> Path:
    bundle = root / category / name / "tasks"
    slug = str(task_meta.get("task", "fixture-task"))
    write_document(bundle / slug / "task.md", task_meta, body or TASK_BODY.format(title=task_meta.get("title", "Fixture task")))
    return bundle


def finalize(bundle: Path) -> None:
    (bundle / "index.md").write_text(cli.generated_index(bundle), encoding="utf-8")


def build(root: Path) -> None:
    # Positive: every optional family, unknown data, partial links, and lifecycle history.
    bundle = fixture(root, "valid", "full-task", task(
        owner="agent", assignees=["agent", "reviewer"], priority="high", tags=["spec"],
        estimate={"effort_minutes": 180, "method": "agent", "confidence": "medium", "basis": "Compared with similar work.", "actor": "agent", "timestamp": STAMP},
        sprint_points={"value": 3, "scale": "fibonacci", "context": "platform", "timestamp": STAMP},
        external=[{"system": "linear", "id": "ENG-1", "url": "https://linear.app/example/ENG-1"}],
        sync={"authority": "repository", "field_authority": {"status": "tracker"}, "base": {"local_revision": "abc", "remote_revision": "7"}},
        producer_extension={"preserve": True},
    )); finalize(bundle)

    bundle = fixture(root, "valid", "workstream", task())
    write_document(bundle / "fixture-task" / "workstreams" / "delivery.md", workstream(), WORKSTREAM_BODY.format(title="Delivery workstream")); finalize(bundle)

    bundle = fixture(root, "valid", "broken-relationships-warning", task(parent="missing-parent/task", depends_on=["missing-dependency/task"])); finalize(bundle)

    bundle = fixture(root, "valid", "unknown-concept", task())
    write_document(bundle / "fixture-task" / "coordination.md", {"type": "Coordination Note", "timestamp": STAMP, "extension": "retained"}, "# Coordination\n\nAn unknown adjacent concept.\n"); finalize(bundle)

    bundle = fixture(root, "valid", "reopened-history", task(status="in-progress", completion_history=[{"finished": STAMP, "reopened": LATER}])); finalize(bundle)

    bundle = fixture(root, "valid", "time-methods", task(started=STAMP, effort_minutes=180))
    for name, method, effort in (("manual-entry", "manual", 30), ("adjusted-entry", "tracked-adjusted", 60), ("commit-review", "estimated-commit-review", 90)):
        meta = time_entry(name, method=method, effort_minutes=effort)
        if method == "estimated-commit-review":
            meta.update(confidence="medium", source_commits=["a" * 40], estimation={"session_gap_minutes": 90, "allowance_minutes": 30, "session_count": 1, "sessions": [{"started": STAMP, "finished": LATER, "effort_minutes": 90}]})
        write_document(bundle / "fixture-task" / "time" / f"{name}.md", meta, TIME_BODY)
    finalize(bundle)

    bundle = fixture(root, "valid", "unique-external-mappings", task(external=[{"system": "github", "id": "1", "url": "https://github.com/example/repo/issues/1"}], sync={"authority": "manual"}))
    other = task("second-task", title="Second task", external=[{"system": "github", "id": "2", "url": "https://github.com/example/repo/issues/2"}])
    write_document(bundle / "second-task" / "task.md", other, TASK_BODY.format(title="Second task")); finalize(bundle)

    # Negative: one focused mutation per machine-testable requirement family.
    negatives: dict[str, tuple[dict[str, Any], str | None]] = {
        "missing-task-field": ({k: v for k, v in task().items() if k != "description"}, None),
        "invalid-task-slug": (task(task="Not-Kebab"), None),
        "unknown-task-status": (task(status="qa"), None),
        "invalid-task-timestamp": (task(timestamp="yesterday"), None),
        "missing-task-heading": (task(), TASK_BODY.format(title="Fixture").replace("## Evidence", "## Proof")),
        "invalid-estimate": (task(estimate={"effort_minutes": -1, "method": "guess", "confidence": "certain", "basis": "", "actor": "agent", "timestamp": STAMP}), None),
        "invalid-points": (task(sprint_points={"value": -3, "scale": "", "timestamp": "today"}), None),
        "invalid-sync-authority": (task(sync={"authority": "both"}), None),
        "invalid-field-authority": (task(sync={"authority": "repository", "field_authority": {"status": "both"}}), None),
        "invalid-completion-history": (task(completion_history=[{"finished": STAMP}]), None),
    }
    for name, (metadata, body) in negatives.items():
        bundle = fixture(root, "invalid", name, metadata, body); finalize(bundle)

    bundle = fixture(root, "invalid", "workstream-parent-mismatch", task())
    write_document(bundle / "fixture-task" / "workstreams" / "delivery.md", workstream(task_slug="other-task"), WORKSTREAM_BODY.format(title="Delivery")); finalize(bundle)

    bundle = fixture(root, "invalid", "workstream-missing-created", task())
    ws = workstream(); ws.pop("created")
    write_document(bundle / "fixture-task" / "workstreams" / "delivery.md", ws, WORKSTREAM_BODY.format(title="Delivery")); finalize(bundle)

    bundle = fixture(root, "invalid", "done-active-workstream", task(status="done", finished=LATER))
    write_document(bundle / "fixture-task" / "workstreams" / "delivery.md", workstream(), WORKSTREAM_BODY.format(title="Delivery")); finalize(bundle)

    bundle = fixture(root, "invalid", "duplicate-active-branch", task())
    for slug in ("one", "two"):
        write_document(bundle / "fixture-task" / "workstreams" / f"{slug}.md", workstream(slug=slug, branch="task/shared"), WORKSTREAM_BODY.format(title=slug)); finalize(bundle)

    time_cases: dict[str, dict[str, Any]] = {
        "running-with-closed-fields": time_entry("bad-entry", status="running", method="tracked"),
        "closed-missing-effort": {k: v for k, v in time_entry("bad-entry").items() if k != "effort_minutes"},
        "unknown-time-method": time_entry("bad-entry", method="automatic"),
    }
    for name, entry in time_cases.items():
        bundle = fixture(root, "invalid", name, task(started=STAMP, effort_minutes=0))
        write_document(bundle / "fixture-task" / "time" / "bad-entry.md", entry, TIME_BODY); finalize(bundle)

    bundle = fixture(root, "invalid", "done-running-time", task(status="done", started=STAMP, finished=LATER, effort_minutes=0))
    running = time_entry("running-entry", status="running", method="tracked")
    for field in ("finished", "elapsed_minutes", "effort_minutes"): running.pop(field)
    write_document(bundle / "fixture-task" / "time" / "running-entry.md", running, TIME_BODY); finalize(bundle)

    bundle = fixture(root, "invalid", "duplicate-running-combination", task(started=STAMP, effort_minutes=0))
    for slug in ("one-entry", "two-entry"):
        running = time_entry(slug, status="running", method="tracked")
        for field in ("finished", "elapsed_minutes", "effort_minutes"): running.pop(field)
        write_document(bundle / "fixture-task" / "time" / f"{slug}.md", running, TIME_BODY)
    finalize(bundle)

    bundle = fixture(root, "invalid", "external-missing-fields", task(external=[{"system": "linear"}])); finalize(bundle)

    bundle = fixture(root, "invalid", "duplicate-external-mapping", task(external=[{"system": "linear", "id": "ENG-1", "url": "https://linear.app/example/ENG-1"}]))
    other = task("second-task", title="Second", external=[{"system": "linear", "id": "ENG-1", "url": "https://linear.app/example/ENG-1"}])
    write_document(bundle / "second-task" / "task.md", other, TASK_BODY.format(title="Second")); finalize(bundle)

    bundle = fixture(root, "invalid", "stale-index", task())
    (bundle / "index.md").write_text("# Stale task index\n", encoding="utf-8")

    fixture(root, "invalid", "missing-index", task())

    bundle = root / "invalid" / "malformed-yaml" / "tasks"
    path = bundle / "fixture-task" / "task.md"; path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\ntype: [broken\n---\n# Broken\n", encoding="utf-8")
    (bundle / "index.md").write_text("# Task index\n", encoding="utf-8")

    bundle = root / "invalid" / "missing-frontmatter" / "tasks"
    path = bundle / "fixture-task" / "task.md"; path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# Missing frontmatter\n", encoding="utf-8")
    (bundle / "index.md").write_text("# Task index\n", encoding="utf-8")


def same_tree(left: Path, right: Path) -> bool:
    comparison = filecmp.dircmp(left, right)
    if comparison.left_only or comparison.right_only or comparison.funny_files:
        return False
    if any(not filecmp.cmp(left / name, right / name, shallow=False) for name in comparison.common_files):
        return False
    return all(same_tree(left / name, right / name) for name in comparison.common_dirs)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if tracked generated fixtures are stale")
    args = parser.parse_args()
    destination = Path(__file__).resolve().parent / "generated"
    if args.check:
        with tempfile.TemporaryDirectory() as temporary:
            expected = Path(temporary) / "generated"
            build(expected)
            if not destination.exists() or not same_tree(destination, expected):
                raise SystemExit("Generated conformance fixtures are stale; run conformance/generate_fixtures.py")
        return 0
    resolved = destination.resolve()
    if resolved.name != "generated" or resolved.parent != Path(__file__).resolve().parent:
        raise SystemExit(f"Refusing to replace unsafe fixture path: {resolved}")
    if resolved.exists():
        shutil.rmtree(resolved)
    build(resolved)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
