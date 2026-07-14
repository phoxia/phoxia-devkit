#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


SKIP_DIRS = {
    ".git",
    ".phoxia",
    ".agents",
    ".claude",
    ".codex",
    ".svelte-kit",
    "__pycache__",
    "build",
    "coverage",
    "node_modules",
    "migration-hold",
    "playwright-report",
    "test-results",
}
SKIP_ROOT_FILES = {".gitignore", "AGENTS.md", "CLAUDE.md", "COMMERCIAL-USE.md", "MANIFEST.json", "SHA256SUMS.txt"}


def package_files(root: Path) -> list[Path]:
    tracked = subprocess.run(
        ["git", "-C", root, "ls-files", "-z"],
        check=True,
        stdout=subprocess.PIPE,
    ).stdout.decode().split("\0")
    return sorted(
        path
        for relative in tracked
        if relative
        for path in (root / relative,)
        if path.is_file()
        and not any(part in SKIP_DIRS for part in path.relative_to(root).parts)
        and not path.relative_to(root).as_posix().startswith("docs/superpowers/")
        and not (path.parent == root and path.name in SKIP_ROOT_FILES)
        and path.suffix != ".pyc"
    )


def build(root: Path, package: str, version: str) -> tuple[str, str]:
    entries = []
    for path in package_files(root):
        data = path.read_bytes()
        try:
            words = len(data.decode("utf-8").split())
        except UnicodeDecodeError:
            words = 0
        entries.append(
            {
                "path": path.relative_to(root).as_posix(),
                "bytes": len(data),
                "words": words,
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    manifest = json.dumps(
        {"package": package, "version": version, "fileCount": len(entries), "files": entries},
        indent=2,
        ensure_ascii=False,
    ) + "\n"
    checksums = [f"{entry['sha256']}  {entry['path']}" for entry in entries]
    checksums.append(f"{hashlib.sha256(manifest.encode()).hexdigest()}  MANIFEST.json")
    return manifest, "\n".join(sorted(checksums, key=lambda line: line.split("  ", 1)[1])) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("package")
    parser.add_argument("version")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    manifest, checksums = build(root, args.package, args.version)
    if args.check:
        if (root / "MANIFEST.json").read_text(encoding="utf-8") != manifest:
            raise SystemExit("MANIFEST.json is stale")
        if (root / "SHA256SUMS.txt").read_text(encoding="utf-8") != checksums:
            raise SystemExit("SHA256SUMS.txt is stale")
        print(f"Package metadata passed: {args.package} {args.version}.")
        return
    (root / "MANIFEST.json").write_text(manifest, encoding="utf-8", newline="\n")
    (root / "SHA256SUMS.txt").write_text(checksums, encoding="utf-8", newline="\n")
    print(f"Generated package metadata: {args.package} {args.version}.")


if __name__ == "__main__":
    main()
