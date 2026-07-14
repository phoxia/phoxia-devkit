#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, subprocess

def run(*args: str) -> str:
    return subprocess.check_output(args, text=True).strip()

def parse(value: str):
    m = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)(?:[-+].*)?", value)
    if not m:
        raise SystemExit(f"Unsupported version: {value}")
    return tuple(map(int, m.groups()))

def bumped(v, level):
    major, minor, patch = v
    if level == "major": return f"{major + 1}.0.0"
    if level == "minor": return f"{major}.{minor + 1}.0"
    if level == "patch": return f"{major}.{minor}.{patch + 1}"
    return f"{major}.{minor}.{patch}"

parser = argparse.ArgumentParser()
parser.add_argument("--current", required=True)
parser.add_argument("--since")
args = parser.parse_args()

current = parse(args.current)
since = args.since or run("git", "describe", "--tags", "--abbrev=0")
messages = run("git", "log", "--format=%B%x00", f"{since}..HEAD").split("\x00")
rank = {"none": 0, "patch": 1, "minor": 2, "major": 3}
level, evidence = "none", []

for message in messages:
    message = message.strip()
    if not message: continue
    first = message.splitlines()[0]
    candidate = "none"
    if "BREAKING CHANGE:" in message or re.match(r"^[a-zA-Z]+(?:\([^)]*\))?!:", first):
        candidate = "major"
    elif first.startswith("feat"):
        candidate = "minor"
    elif first.startswith(("fix", "perf")):
        candidate = "patch"
    if current[0] == 0 and candidate == "major":
        candidate = "minor"
    if rank[candidate] > rank[level]:
        level = candidate
    if candidate != "none":
        evidence.append({"commit": first, "suggestion": candidate})

print(json.dumps({
    "current": args.current,
    "since": since,
    "recommendedBump": level,
    "recommendedVersion": bumped(current, level),
    "evidence": evidence,
    "requiresHumanApproval": True,
}, indent=2))
