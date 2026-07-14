#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from package_manifest import SKIP_DIRS


def validate_tree(root: Path) -> tuple[list[str], int]:
    errors: list[str] = []
    profiles = 0
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts) or not path.is_file():
            continue
        rel = path.relative_to(root)
        if path.stat().st_size == 0:
            errors.append(f"empty: {rel}")
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if path.suffix == ".json":
            try:
                json.loads(content)
            except Exception as exc:
                errors.append(f"invalid JSON {rel}: {exc}")
        if path.name == "profile.json":
            profiles += 1
        if path.name != "SKILL.md":
            continue
        if not content.startswith("---\n"):
            errors.append(f"missing skill frontmatter: {rel}")
            continue
        end = content.find("\n---\n", 4)
        values = {}
        for line in content[4:end if end >= 0 else 4].splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                values[key.strip()] = value.strip()
        if not values.get("name"):
            errors.append(f"missing name in {rel}")
        if not values.get("description"):
            errors.append(f"missing description in {rel}")
        if values.get("name") and values["name"] != path.parent.name:
            errors.append(f'skill name must match directory: {rel} ({values["name"]})')
    if not profiles:
        errors.append("no profile manifests found")
    return errors, profiles


def main() -> None:
    if len(sys.argv) > 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} [PACKAGE_ROOT]")
    root = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else Path(__file__).resolve().parents[1]
    errors, profiles = validate_tree(root)
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Validation passed with {profiles} profiles.")


if __name__ == "__main__":
    main()
