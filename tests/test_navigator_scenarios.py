from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "plugins" / "core" / "skills" / "devkit"


class NavigatorScenarioTest(unittest.TestCase):
    def test_scenario_routes_and_evidence_are_documented(self) -> None:
        scenarios = json.loads((ROOT / "tests" / "fixtures" / "navigator_scenarios.json").read_text(encoding="utf-8"))
        commands = (SKILL_ROOT / "references" / "commands.md").read_text(encoding="utf-8").lower()
        for scenario in scenarios:
            route_family = scenario["route"].split()[0]
            self.assertIn(route_family, commands, scenario["id"])
            reference = SKILL_ROOT / "references" / scenario["reference"]
            text = reference.read_text(encoding="utf-8").lower()
            for concept in scenario["concepts"]:
                self.assertIn(concept.lower(), text, f"{scenario['id']}: {concept}")

    def test_router_delegates_only_to_installed_public_skills(self) -> None:
        router = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        installed = {
            item.parent.name
            for item in (ROOT / "plugins").glob("*/skills/*/SKILL.md")
        }
        aliases = {
            "phoxia-dev": "dev", "phoxia-project": "project", "phoxia-docs": "docs",
            "phoxia-open": "phoxia", "phoxia-release": "release", "phoxia-specialist": "specialist",
            "phoxia-ui": "ui", "phoxia-handoff": "handoff",
        }
        for public_name, directory in aliases.items():
            self.assertIn(public_name, router)
            self.assertIn(directory, installed)


if __name__ == "__main__":
    unittest.main()
