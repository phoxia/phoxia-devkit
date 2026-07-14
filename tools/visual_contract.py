#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("paths", nargs="+", type=Path)
parser.add_argument("--output", type=Path, default=Path("design/reference-lock.json"))
args = parser.parse_args()

entries = {}
for path in args.paths:
    if path.is_file():
        entries[path.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    elif path.is_dir():
        for child in sorted(p for p in path.rglob("*") if p.is_file()):
            entries[child.as_posix()] = hashlib.sha256(child.read_bytes()).hexdigest()

args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps({"files": entries}, indent=2) + "\n", encoding="utf-8")
print(args.output)
