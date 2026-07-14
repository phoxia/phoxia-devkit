#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path
from datetime import datetime, timezone

STATE = Path(".claude/project-state.local.json")
RELEVANT = (
    "package.json", "pnpm-lock.yaml", "Cargo.toml", "pyproject.toml",
    "go.mod", "pom.xml", "Dockerfile", "prisma", "migrations", "src",
    "apps", "packages", "docs", "AGENTS.md", "CLAUDE.md",
    "phoxia.project.yaml", "PROJECT.yaml",
)

def run(*args: str) -> str:
    return subprocess.check_output(args, text=True).strip()

def current() -> str:
    return run("git", "rev-parse", "HEAD")

def relevant(path: str) -> bool:
    return any(path == x or path.startswith(x.rstrip("/") + "/") for x in RELEVANT)

parser = argparse.ArgumentParser()
parser.add_argument("command", choices=["status", "mark"])
args = parser.parse_args()

if args.command == "status":
    if not STATE.exists():
        print(json.dumps({"syncDue": True, "reason": "no project state"}, indent=2))
    else:
        state = json.loads(STATE.read_text(encoding="utf-8"))
        last = state.get("lastSyncCommit")
        changed = run("git", "diff", "--name-only", f"{last}..HEAD").splitlines() if last else []
        changed = [p for p in changed if relevant(p)]
        print(json.dumps({
            "syncDue": bool(changed),
            "lastSyncCommit": last,
            "currentCommit": current(),
            "relevantChanges": changed,
        }, indent=2))
else:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps({
        "lastSyncCommit": current(),
        "lastSyncAt": datetime.now(timezone.utc).isoformat(),
    }, indent=2) + "\n", encoding="utf-8")
    print(STATE)
