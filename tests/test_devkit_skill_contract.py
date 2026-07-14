from __future__ import annotations

import subprocess
import sys
import unittest
import importlib.util
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins" / "core" / "skills" / "devkit" / "SKILL.md"
REFERENCES = SKILL.parent / "references"
COMMANDS = {
    "help", "status", "doctor",
    "project guide|init|adopt|sync|audit",
    "feature start|continue|review", "fix start|continue|review",
    "review change|security|reliability|privacy|legal|licensing|accessibility|performance|architecture|full",
    "docs check|adr|feature|rfc|data|operations|changelog|sync",
    "release analyze|prepare|verify",
    "operate readiness|incident|backup|restore|cost",
    "preferences show|set|reset", "mode guided|direct", "handoff",
}
SPEC = importlib.util.spec_from_file_location("phoxia_devkit_contract", ROOT / "tools" / "phoxia_devkit.py")
assert SPEC and SPEC.loader
DEVKIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DEVKIT)


class DevKitSkillContractTest(unittest.TestCase):
    def test_router_and_command_inventory(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")
        commands = (REFERENCES / "commands.md").read_text(encoding="utf-8")
        inventory = {line[2:] for line in commands.splitlines() if line.startswith("- `") and line.endswith("`")}
        inventory = {line[1:-1] for line in inventory}

        self.assertIn("name: devkit", skill)
        self.assertNotIn("disable-model-invocation: true", skill)
        self.assertEqual(inventory, COMMANDS)
        self.assertIn("$phoxia-devkit", commands)
        self.assertIn("/phoxia-core:devkit", commands)
        for reference in ("context-discovery.md", "project-guide.md", "lifecycle-routing.md", "review-routing.md", "preferences-and-style.md"):
            self.assertIn(reference, skill)
            self.assertTrue((REFERENCES / reference).is_file())

    def test_context_risk_and_style_contracts(self) -> None:
        context = (REFERENCES / "context-discovery.md").read_text(encoding="utf-8")
        guide = (REFERENCES / "project-guide.md").read_text(encoding="utf-8")
        lifecycle = (REFERENCES / "lifecycle-routing.md").read_text(encoding="utf-8")
        review = (REFERENCES / "review-routing.md").read_text(encoding="utf-8")
        style = (REFERENCES / "preferences-and-style.md").read_text(encoding="utf-8")

        precedence = ["AGENTS.md", "registered RFC", "ADR", "versioned APIs", "tests", "implementation", "Git history"]
        self.assertEqual([context.index(item) for item in precedence], sorted(context.index(item) for item in precedence))
        for item in ("RFC", "ADR", "Feature Record"):
            self.assertIn(item, context)
        self.assertIn("infrastructure", context.lower())
        for item in ("hobby/prototype", "professional MVP", "production", "critical/regulatory"):
            self.assertIn(item, guide)
        for item in ("feature start", "fix start", "releaseSuggestions", "handoff"):
            self.assertIn(item, lifecycle)
        for item in ("shared corporate NAT", "429", "tested restore", "network-copyleft", "retention", "accessibility"):
            self.assertIn(item, review)
        for item in ("guided", "direct", "session > project > user > defaults", "Critical warnings cannot be disabled", "reflexive praise"):
            self.assertIn(item, style)

    def test_external_parser_is_package_lifecycle_only(self) -> None:
        cli = ROOT / "tools" / "phoxia_devkit.py"
        help_result = subprocess.run([sys.executable, str(cli), "--help"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(help_result.returncode, 0, help_result.stderr)
        for command in ("install", "update", "uninstall", "restore", "doctor", "status"):
            self.assertIn(command, help_result.stdout)
        rejected = subprocess.run([sys.executable, str(cli), "project", "init"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("invalid choice", rejected.stderr)

    def test_startup_hints_are_static_localized_and_optional(self) -> None:
        english = DEVKIT.launcher_posix("codex", {}, hint=DEVKIT.startup_hint("codex", "en"))
        portuguese = DEVKIT.launcher_powershell("claude", {}, hint=DEVKIT.startup_hint("claude", "pt-BR"))
        silent = DEVKIT.launcher_posix("codex", {}, hint=None)

        self.assertIn("$phoxia-devkit project guide", english)
        self.assertIn("/phoxia-core:devkit project guide", portuguese)
        self.assertIn("Precisa de direção?", portuguese)
        self.assertNotIn("project guide", silent)
        for launcher in (english, portuguese):
            self.assertNotIn(" doctor", launcher)
            self.assertNotIn("git ", launcher)

    def test_authoritative_codex_plugin_install_refreshes_marketplaces(self) -> None:
        selection = {
            "marketplaces": {"example": "owner/repo"},
            "codex": ["tool@example"],
        }
        calls: list[list[str]] = []

        def record(command: list[str], _home: Path, timeout: int = 180) -> tuple[bool, str]:
            calls.append(command)
            return True, "ok"

        with patch.object(DEVKIT, "run_external_command", side_effect=record):
            warnings = DEVKIT.install_external_plugins(Path("/tmp/home"), ["codex"], selection, False)

        self.assertEqual(warnings, [])
        self.assertEqual(calls[0], ["codex", "plugin", "marketplace", "remove", "example"])
        self.assertEqual(calls[1], ["codex", "plugin", "marketplace", "add", "owner/repo", "--json"])
        self.assertEqual(calls[2], ["codex", "plugin", "add", "tool@example", "--json"])


if __name__ == "__main__":
    unittest.main()
