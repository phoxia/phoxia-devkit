from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATE = ROOT / "tools" / "validate.py"


class ValidateTest(unittest.TestCase):
    def run_validate(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATE), str(root)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def test_ignores_generated_directories(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "personal").mkdir()
            (root / "personal" / "profile.json").write_text("{}\n", encoding="utf-8")
            for name in ("node_modules", ".svelte-kit", "build", "coverage", "test-results"):
                path = root / "site" / name
                path.mkdir(parents=True)
                (path / "SKILL.md").write_text("", encoding="utf-8")

            result = self.run_validate(root)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_reports_empty_source_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "personal").mkdir()
            (root / "personal" / "profile.json").write_text("{}\n", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs" / "empty.md").write_text("", encoding="utf-8")

            result = self.run_validate(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("empty: docs/empty.md", result.stdout + result.stderr)

    def test_public_release_files_are_complete(self) -> None:
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        workflow = (ROOT / ".github" / "workflows" / "validate.yml").read_text(encoding="utf-8")
        template = (ROOT / "templates" / "phoxia" / "phoxia.project.yaml").read_text(encoding="utf-8")

        self.assertGreater(len(license_text), 30_000)
        self.assertNotIn("Before publishing", license_text)
        self.assertTrue(template.startswith("apiVersion: kit.phoxia.org/v1\n"))
        self.assertIn("python3 -m unittest discover -s tests -v", workflow)


if __name__ == "__main__":
    unittest.main()
