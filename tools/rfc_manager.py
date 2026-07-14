#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, shutil
from pathlib import Path

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def next_number(root: Path) -> int:
    values = []
    for path in (root / "accepted/en").glob("RFC-*.md"):
        m = re.match(r"RFC-(\d{4})-", path.name)
        if m: values.append(int(m.group(1)))
    return max(values, default=0) + 1

parser = argparse.ArgumentParser()
sub = parser.add_subparsers(dest="command", required=True)

new = sub.add_parser("new-draft")
new.add_argument("--root", type=Path, required=True)
new.add_argument("--slug", required=True)
new.add_argument("--title", required=True)

accept = sub.add_parser("accept")
accept.add_argument("--root", type=Path, required=True)
accept.add_argument("--en", type=Path, required=True)
accept.add_argument("--pt", type=Path, required=True)
accept.add_argument("--slug", required=True)

sync = sub.add_parser("sync")
sync.add_argument("--root", type=Path, required=True)
sync.add_argument("--repo", type=Path, required=True)
sync.add_argument("--number", type=int, required=True)

args = parser.parse_args()

if args.command == "new-draft":
    drafts = args.root / "drafts"
    drafts.mkdir(parents=True, exist_ok=True)
    for lang in ("en", "pt-BR"):
        path = drafts / f"{args.slug}.{lang}.md"
        path.write_text(f"# Draft • {args.title}\n\n- Status: Draft\n- Language: {lang}\n", encoding="utf-8")
        print(path)

elif args.command == "accept":
    number = next_number(args.root)
    for source, lang in ((args.en, "en"), (args.pt, "pt-BR")):
        target_dir = args.root / "accepted" / lang
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / f"RFC-{number:04d}-{args.slug}.md"
        shutil.copy2(source, target)
        print(target)
    print(f"Accepted RFC-{number:04d}")

else:
    repo_dir = args.repo / "docs/rfcs"
    lock = {"rfc": f"RFC-{args.number:04d}", "files": {}}
    for lang in ("en", "pt-BR"):
        candidates = list((args.root / "accepted" / lang).glob(f"RFC-{args.number:04d}-*.md"))
        if len(candidates) != 1:
            raise SystemExit(f"Expected one {lang} RFC, found {len(candidates)}")
        target_dir = repo_dir / lang
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / candidates[0].name
        shutil.copy2(candidates[0], target)
        lock["files"][target.relative_to(args.repo).as_posix()] = sha(target)
    lock_path = repo_dir / f"RFC-{args.number:04d}.lock.json"
    lock_path.write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")
    print(lock_path)
