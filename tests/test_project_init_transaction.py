from __future__ import annotations

import argparse
import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from tools.phoxia_devkit import DevKitError, project_init_transaction


def arguments(path: Path, **overrides: object) -> argparse.Namespace:
    values: dict[str, object] = {
        "path": str(path), "profile": "personal", "targets": "codex", "layer": None,
        "owner": "Owner", "description": "Example", "company": "Owner",
        "visibility": "private", "license_model": "private", "commercial_use": None,
        "redistribution": None, "technical_maintainer": "Owner",
        "pull_request_approver": "Owner", "commercial_authority": "Owner",
        "documentation_visibility": "private", "vendor_skills": False,
        "mode": "add", "yes": True, "dry_run": False,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


class ProjectInitTransactionTest(unittest.TestCase):
    def test_dry_run_previews_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            root.mkdir()
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                project_init_transaction(arguments(root, dry_run=True))
            self.assertIn("CREATE .phoxia/project.yaml", output.getvalue())
            self.assertFalse((root / ".phoxia").exists())

    def test_add_refuses_an_existing_managed_project(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            root.mkdir()
            project_init_transaction(arguments(root))
            with self.assertRaisesRegex(DevKitError, "add mode"):
                project_init_transaction(arguments(root))

    def test_managed_instructions_define_documentation_triggers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            root.mkdir()
            project_init_transaction(arguments(root))
            agents = (root / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("version manifest", agents)
            self.assertIn("user-facing contract", agents)
            self.assertIn("Feature Record", agents)

    def test_update_preserves_user_text_and_creates_backup(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            root.mkdir()
            project_init_transaction(arguments(root))
            agents = root / "AGENTS.md"
            agents.write_text("user before\n\n" + agents.read_text(encoding="utf-8") + "\nuser after\n", encoding="utf-8")
            project_init_transaction(arguments(root, mode="update", description="Changed"))
            self.assertIn("user before", agents.read_text(encoding="utf-8"))
            self.assertIn("user after", agents.read_text(encoding="utf-8"))
            backups = list((root / ".phoxia" / "backups").glob("*/AGENTS.md"))
            self.assertEqual(len(backups), 1)
            self.assertIn("user before", backups[0].read_text(encoding="utf-8"))

    def test_update_requires_an_existing_managed_project(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            root.mkdir()
            with self.assertRaisesRegex(DevKitError, "update mode"):
                project_init_transaction(arguments(root, mode="update"))

    def test_add_refuses_to_overwrite_existing_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            (root / ".codex").mkdir(parents=True)
            (root / ".codex" / "config.toml").write_text("user = true\n", encoding="utf-8")
            with self.assertRaisesRegex(DevKitError, "would overwrite"):
                project_init_transaction(arguments(root))
            self.assertEqual((root / ".codex" / "config.toml").read_text(), "user = true\n")

    def test_noninteractive_write_requires_yes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "example"
            root.mkdir()
            with self.assertRaisesRegex(DevKitError, "--yes"):
                project_init_transaction(arguments(root, yes=False))


if __name__ == "__main__":
    unittest.main()
