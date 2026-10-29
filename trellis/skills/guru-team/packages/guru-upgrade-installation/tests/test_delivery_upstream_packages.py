"""Resolve the Core dependency actually used by reviewed CLI installations."""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime"))
from delivery_upstream import packages
from files import MigrationError


@unittest.skipUnless(shutil.which("node"), "Node is required for actual dependency resolution")
class PackageResolutionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="guru-plan2-package-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()

    def package(self, path, name, version="0.7.0-castbox.6"):
        path.mkdir(parents=True)
        (path / "package.json").write_text(json.dumps({"name": name, "version": version}))
        return path

    def workspace(self, *, core_version="0.7.0-castbox.6", link=True):
        cli = self.package(self.root / "packages/cli", "@mindfoldhq/trellis")
        core = self.package(self.root / "packages/core", "@mindfoldhq/trellis-core", core_version)
        (cli / "bin").mkdir()
        entry = cli / "bin/trellis.js"
        entry.write_text("")
        if link:
            dependency = cli / "node_modules/@mindfoldhq/trellis-core"
            dependency.parent.mkdir(parents=True)
            dependency.symlink_to(core, target_is_directory=True)
        return cli, core, entry

    def test_workspace_resolves_core_via_actual_cli_dependency(self):
        cli, core, entry = self.workspace()
        self.assertFalse((cli.parent / "trellis-core").exists())
        self.assertEqual(packages(entry), (cli, core))

    def test_npm_sibling_layout_keeps_matching_pair(self):
        modules = self.root / "node_modules/@mindfoldhq"
        cli = self.package(modules / "trellis", "@mindfoldhq/trellis")
        core = self.package(modules / "trellis-core", "@mindfoldhq/trellis-core")
        (cli / "bin").mkdir()
        entry = cli / "bin/trellis.js"
        entry.write_text("")
        self.assertEqual(packages(entry), (cli, core))

    def test_missing_core_dependency_reports_migration_error(self):
        _, _, entry = self.workspace(link=False)
        with self.assertRaisesRegex(MigrationError, "Cannot resolve matching Core"):
            packages(entry)

    def test_mismatched_core_version_remains_rejected(self):
        _, _, entry = self.workspace(core_version="0.7.0-castbox.3")
        with self.assertRaisesRegex(MigrationError, "matching installed CLI/Core"):
            packages(entry)

    def test_unreadable_core_manifest_reports_migration_error(self):
        _, core, entry = self.workspace()
        (core / "package.json").write_text("{")
        with self.assertRaises(MigrationError):
            packages(entry)


if __name__ == "__main__":
    unittest.main()
