#!/usr/bin/env python3
"""Focused regression tests for descriptor-derived Guru ownership."""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_upstream_ownership as ownership


class UpstreamOwnershipTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repo = Path(__file__).resolve().parents[5]

    @staticmethod
    def write_json(path: Path, value: object) -> None:
        path.write_text(
            json.dumps(value, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def copy_source(self, target: Path) -> None:
        directories = (
            Path("trellis/presets/guru-team/ownership"),
            Path("trellis/presets/guru-team/overlays"),
            Path("trellis/workflows/guru-team"),
            Path("trellis/skills/guru-team"),
            Path(".trellis/guru-team"),
            Path(".agents/skills"),
            Path(".claude/skills"),
            Path(".codex/skills"),
            Path(".cursor/skills"),
        )
        for relative in directories:
            source = self.repo / relative
            if source.exists():
                shutil.copytree(source, target / relative)
        for relative in (
            ownership.EXTENSION_RELATIVE,
            ownership.INSTALLER_RELATIVE,
        ):
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(self.repo / relative, destination)

    def test_current_facts_are_stable_and_descriptor_driven(self) -> None:
        first = ownership.validate_repository(self.repo)
        second = ownership.validate_repository(self.repo)
        self.assertEqual(first, second)
        self.assertEqual(first["status"], "ok", first["errors"])
        self.assertEqual(first["schema_version"], "4.0")
        self.assertEqual(first["descriptor_count"], 22)
        self.assertEqual(first["platform_ids"], list(ownership.PLATFORM_IDS))
        self.assertEqual(first["platform_cli_flags"], list(ownership.PLATFORM_FLAGS))
        self.assertEqual(first["dogfood_platforms"], ["claude", "codex", "cursor"])
        self.assertEqual(first["derived_managed_paths"], ownership.EXPECTED_MANAGED_PATHS)
        self.assertEqual(first["managed_claim_count"], len(ownership.EXPECTED_MANAGED_PATHS))
        self.assertEqual(first["classified_managed_claim_count"], len(ownership.EXPECTED_MANAGED_PATHS))
        self.assertEqual(first["overlay_count"], first["descriptor_count"])
        for field in (
            "schema_sha256",
            "inventory_sha256",
            "descriptor_sha256",
            "overlay_paths_sha256",
            "overlay_payload_aggregate_sha256",
            "facts_sha256",
        ):
            self.assertRegex(first[field], r"^[0-9a-f]{64}$")

    def test_schema_is_valid_and_accepts_inventory(self) -> None:
        from jsonschema import Draft202012Validator

        schema = json.loads((self.repo / ownership.SCHEMA_RELATIVE).read_text(encoding="utf-8"))
        inventory = json.loads((self.repo / ownership.INVENTORY_RELATIVE).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        self.assertEqual(list(Draft202012Validator(schema).iter_errors(inventory)), [])

    def test_descriptor_ids_and_cli_flags_are_unique(self) -> None:
        inventory = json.loads((self.repo / ownership.INVENTORY_RELATIVE).read_text(encoding="utf-8"))
        rows = inventory["platform_descriptors"]
        self.assertEqual(len(rows), 22)
        self.assertEqual(len({row["id"] for row in rows}), 22)
        self.assertEqual(len({row["cli_flag"] for row in rows}), 22)
        self.assertEqual(rows[0]["id"], "claude-code")
        self.assertEqual(rows[0]["cli_flag"], "claude")

    def test_legacy_supported_or_deferred_tier_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self.copy_source(repo)
            extension_path = repo / ownership.EXTENSION_RELATIVE
            extension = json.loads(extension_path.read_text(encoding="utf-8"))
            extension["public_api"]["platform_capabilities"]["deferred_platforms"] = []
            self.write_json(extension_path, extension)
            payload = ownership.validate_repository(repo)
        self.assertEqual(payload["status"], "error")
        self.assertIn("platform_capability_legacy_tier", {row["code"] for row in payload["errors"]})

    def test_descriptor_drift_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self.copy_source(repo)
            inventory_path = repo / ownership.INVENTORY_RELATIVE
            inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
            inventory["platform_descriptors"][0]["cli_flag"] = "claude-code"
            self.write_json(inventory_path, inventory)
            payload = ownership.validate_repository(repo)
        self.assertEqual(payload["status"], "error")
        self.assertIn("platform_descriptor_inventory_invalid", {row["code"] for row in payload["errors"]})

    def test_overlay_count_does_not_define_platform_count(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self.copy_source(repo)
            overlay = repo / ownership.OVERLAY_ROOT_RELATIVE / ".opencode/commands/guru-finish-work.md"
            if overlay.exists():
                overlay.unlink()
            payload = ownership.validate_repository(repo)
        self.assertNotIn("missing_finish_overlay", {row["code"] for row in payload["errors"]})
        self.assertEqual(payload["descriptor_count"], 22)

    def test_package_private_tests_in_public_projection_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self.copy_source(repo)
            leaked = repo / ".cursor/skills/guru-example/tests/test_private.py"
            leaked.parent.mkdir(parents=True, exist_ok=True)
            leaked.write_text("raise AssertionError\n", encoding="utf-8")
            payload = ownership.validate_repository(repo)
        self.assertEqual(payload["status"], "error")
        self.assertIn("package_private_test_projected", {row["code"] for row in payload["errors"]})

    def test_descriptor_classification_covers_skill_and_entry(self) -> None:
        inventory = json.loads((self.repo / ownership.INVENTORY_RELATIVE).read_text(encoding="utf-8"))
        self.assertIn(
            "platform:opencode:skill",
            ownership.classify_guru_path(".opencode/skills/guru-review-branch/SKILL.md", inventory),
        )
        self.assertEqual(
            ownership.classify_guru_path(".opencode/commands/guru-finish-work.md", inventory),
            ["platform:opencode:entry"],
        )
        self.assertEqual(
            ownership.classify_guru_path(".opencode/commands/trellis/start.md", inventory),
            [],
        )


if __name__ == "__main__":
    unittest.main()
