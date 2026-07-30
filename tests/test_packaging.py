from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PackagingTests(unittest.TestCase):
    def test_editable_install_metadata_is_gitignored(self) -> None:
        ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("*.egg-info/", ignore)

    def test_installed_distribution_exposes_the_okf_tasks_command(self) -> None:
        configuration = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        self.assertEqual("okf_tasks:main", configuration["project"]["scripts"]["okf-tasks"])
        egg_info = ROOT / "skills" / "okf-task-lifecycle" / "scripts" / "okf_tasks.egg-info"
        if not egg_info.exists():
            self.addCleanup(shutil.rmtree, egg_info, True)
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "site"
            installed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--no-deps",
                    "--no-build-isolation",
                    "--target",
                    str(target),
                    str(ROOT),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, installed.returncode, installed.stderr)
            launchers = list(target.rglob("okf-tasks.exe")) + list(target.rglob("okf-tasks"))
            self.assertTrue(launchers, f"No okf-tasks launcher was installed under {target}")
            environment = os.environ.copy()
            environment["PYTHONPATH"] = str(target)
            invoked = subprocess.run(
                [str(launchers[0]), "--help"],
                capture_output=True,
                text=True,
                env=environment,
            )
            self.assertEqual(0, invoked.returncode, invoked.stderr)
            self.assertIn("init-bundle", invoked.stdout)
            self.assertIn("tracker", invoked.stdout)
            version = subprocess.run(
                [str(launchers[0]), "--version"],
                capture_output=True,
                text=True,
                env=environment,
            )
            self.assertEqual(0, version.returncode, version.stderr)
            expected_version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
            self.assertEqual(f"okf-tasks {expected_version}", version.stdout.strip())
            repository = Path(directory) / "repository"
            repository.mkdir()
            created = subprocess.run(
                [
                    str(launchers[0]),
                    "create",
                    "--root",
                    str(repository),
                    "--slug",
                    "packaged-task",
                    "--title",
                    "Packaged task",
                    "--description",
                    "Exercise the templates installed with the wheel.",
                ],
                capture_output=True,
                text=True,
                env=environment,
            )
            self.assertEqual(0, created.returncode, created.stderr)
            self.assertTrue((repository / "tasks" / "packaged-task" / "task.md").is_file())
            workstream = subprocess.run(
                [
                    str(launchers[0]),
                    "add-workstream",
                    "--root",
                    str(repository),
                    "--task",
                    "packaged-task",
                    "--slug",
                    "implementation",
                    "--title",
                    "Implementation",
                    "--description",
                    "Implement the packaged task.",
                    "--owner",
                    "test-agent",
                ],
                capture_output=True,
                text=True,
                env=environment,
            )
            self.assertEqual(0, workstream.returncode, workstream.stderr)
            self.assertTrue(
                (
                    repository
                    / "tasks"
                    / "packaged-task"
                    / "workstreams"
                    / "implementation.md"
                ).is_file()
            )


if __name__ == "__main__":
    unittest.main()
