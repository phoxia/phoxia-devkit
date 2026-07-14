from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PackageManifestTest(unittest.TestCase):
    def test_manifest_is_current_version_and_matches_files(self) -> None:
        manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
        package_metadata = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        package = manifest["package"]
        version = package_metadata["version"]
        self.assertEqual(manifest["version"], version)
        paths = {entry["path"] for entry in manifest["files"]}
        self.assertTrue({
            "docs/DESIGN-BACKLOG.md",
            "site/vercel.json",
            "site/tests/redirects.spec.ts",
            "site/src/routes/docs/+page.ts",
            "site/src/routes/quick-start/+page.ts",
            "site/src/routes/quickstart/+page.ts",
            "site/src/routes/changelog/+page.ts",
        }.issubset(paths))
        self.assertFalse(any(
            "node_modules" in path
            or ".svelte-kit" in path
            or path.startswith("docs/superpowers/")
            or path.startswith("site/build/")
            or path.startswith("site/playwright-report/")
            or path.startswith("site/test-results/")
            for path in paths
        ))
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "package_manifest.py"), str(ROOT), package, version, "--check"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
