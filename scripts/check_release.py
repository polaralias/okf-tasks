#!/usr/bin/env python3
"""Check immutable identity and release metadata consistency."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    errors: list[str] = []
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        errors.append("VERSION must contain X.Y.Z")
    major_minor = ".".join(version.split(".")[:2])
    tag = f"v{version}"
    profile = f"https://github.com/polaralias/okf-tasks/blob/{tag}/SPEC.md"
    spec = (ROOT / "SPEC.md").read_text(encoding="utf-8")
    if f"Version {major_minor}\n" not in spec:
        errors.append("SPEC.md version does not agree with VERSION")
    if f"Version {major_minor} — Draft" in spec:
        errors.append("SPEC.md is still marked Draft")
    if profile not in spec:
        errors.append("SPEC.md is missing the immutable tagged profile identity")
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    if package.get("version") != version:
        errors.append("package.json version does not agree with VERSION")
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    if f'version = "{version}"' not in pyproject:
        errors.append("pyproject.toml version does not agree with VERSION")
    for name in ("task", "workstream", "time-entry"):
        schema = json.loads((ROOT / "schemas" / f"{name}.schema.json").read_text(encoding="utf-8"))
        expected = f"https://raw.githubusercontent.com/polaralias/okf-tasks/{tag}/schemas/{name}.schema.json"
        if schema.get("$id") != expected:
            errors.append(f"{name}.schema.json has the wrong $id")
    manifest = json.loads((ROOT / "conformance" / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("profile") != profile:
        errors.append("conformance manifest profile does not agree with VERSION")
    if not any(case.get("valid") for case in manifest.get("cases", [])) or not any(not case.get("valid") for case in manifest.get("cases", [])):
        errors.append("conformance manifest requires positive and negative cases")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Release metadata is consistent for {tag} ({len(manifest['cases'])} conformance cases).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
