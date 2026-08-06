#!/usr/bin/env python3
"""Focused regression tests for the current Guru ownership contract."""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
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
        cls.fixtures = Path(__file__).resolve().parent / "fixtures/upstream-ownership"

    def copy_minimal_source(self, target: Path) -> None:
        directories = [
            Path("trellis/presets/guru-team/ownership"),
            Path("trellis/presets/guru-team/overlays"),
            Path("trellis/workflows/guru-team"),
            Path("trellis/skills/guru-team"),
        ]
        files = [
            ownership.EXTENSION_RELATIVE,
            ownership.INSTALLER_RELATIVE,
        ]
        for relative in directories:
            shutil.copytree(self.repo / relative, target / relative)
        for relative in files:
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(self.repo / relative, destination)

    @staticmethod
    def write_json(path: Path, value: object) -> None:
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def apply_mutation(self, repo: Path, fixture: dict[str, object]) -> None:
        mutation = fixture["mutation"]
        self.assertIsInstance(mutation, dict)
        mutation_type = mutation["type"]
        inventory_path = repo / ownership.INVENTORY_RELATIVE
        inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        if mutation_type == "none":
            return
        if mutation_type == "add_overlay":
            path = repo / ownership.OVERLAY_ROOT_RELATIVE / mutation["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(mutation["content"], encoding="utf-8")
            return
        if mutation_type == "remove_overlay":
            (repo / ownership.OVERLAY_ROOT_RELATIVE / mutation["path"]).unlink()
            return
        if mutation_type == "add_inventory_field":
            inventory[mutation["name"]] = mutation["value"]
            self.write_json(inventory_path, inventory)
            return
        if mutation_type == "remove_managed_claim":
            inventory["managed_path_claims"] = [
                claim
                for claim in inventory["managed_path_claims"]
                if claim["path"] != mutation["path"]
            ]
            self.write_json(inventory_path, inventory)
            return
        if mutation_type == "append_manifest_managed_path":
            extension_path = repo / ownership.EXTENSION_RELATIVE
            extension = json.loads(extension_path.read_text(encoding="utf-8"))
            extension["public_api"]["managed_paths"].append(mutation["path"])
            self.write_json(extension_path, extension)
            return
        if mutation_type == "set_registry_platforms":
            registry_path = repo / ownership.SKILL_REGISTRY_RELATIVE
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            skill = next(item for item in registry["skills"] if item["id"] == mutation["skill_id"])
            skill["supported_platforms"] = mutation["platforms"]
            self.write_json(registry_path, registry)
            return
        self.fail(f"unknown fixture mutation: {mutation_type}")

    def fixture_paths(self) -> list[Path]:
        return sorted(self.fixtures.glob("*.json"))

    def test_structured_fixtures(self) -> None:
        for fixture_path in self.fixture_paths():
            with self.subTest(fixture=fixture_path.name):
                fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
                mutation = fixture["mutation"]
                if mutation["type"] == "classify_guru_paths":
                    inventory = json.loads((self.repo / ownership.INVENTORY_RELATIVE).read_text(encoding="utf-8"))
                    for case in mutation["cases"]:
                        self.assertEqual(
                            ownership.classify_guru_path(case["path"], inventory["guru_owned_rules"]),
                            [case["expected_rule"]],
                        )
                    continue
                with tempfile.TemporaryDirectory() as directory:
                    repo = Path(directory)
                    self.copy_minimal_source(repo)
                    self.apply_mutation(repo, fixture)
                    payload = ownership.validate_repository(repo)
                    cli_result = None
                    if fixture.get("assert_cli_json"):
                        command = self.repo / "trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh"
                        cli_result = subprocess.run(
                            [str(command), "--repo", str(repo), "--json"],
                            text=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            check=False,
                        )
                self.assertEqual(payload["status"], fixture["expected_status"], payload)
                codes = {item["code"] for item in payload["errors"]}
                self.assertTrue(set(fixture["expected_error_codes"]).issubset(codes), (fixture_path.name, payload))
                for error in payload["errors"]:
                    self.assertEqual(set(error), {"code", "path", "detail"})
                if cli_result is not None:
                    self.assertNotEqual(cli_result.returncode, 0)
                    self.assertEqual(json.loads(cli_result.stdout)["status"], "error")
                    self.assertNotIn("Traceback", cli_result.stderr)

    def test_current_facts_are_stable(self) -> None:
        first = ownership.validate_repository(self.repo)
        second = ownership.validate_repository(self.repo)
        self.assertEqual(first, second)
        self.assertEqual(first["status"], "ok")
        self.assertEqual(first["schema_version"], "3.0")
        self.assertEqual(first["inventory_id"], "guru-team-upstream-ownership")
        self.assertEqual(first["target_trellis_cli"], "0.6.5")
        self.assertEqual(first["overlay_count"], 3)
        self.assertEqual(first["managed_claim_count"], 9)
        self.assertEqual(first["classified_managed_claim_count"], 9)
        self.assertEqual(first["active_skill_count"], 14)
        self.assertEqual(first["planned_skill_count"], 0)
        self.assertEqual(first["canonical_package_count"], 14)
        for field in (
            "schema_sha256",
            "inventory_sha256",
            "guru_owned_rules_sha256",
            "managed_path_claims_sha256",
            "overlay_paths_sha256",
            "overlay_payload_aggregate_sha256",
            "facts_sha256",
        ):
            self.assertRegex(first[field], r"^[0-9a-f]{64}$")

        inventory = json.loads((self.repo / ownership.INVENTORY_RELATIVE).read_text(encoding="utf-8"))
        self.assertEqual(set(inventory), ownership.TOP_LEVEL_KEYS)
        self.assertEqual(inventory["guru_owned_rules"], ownership.EXPECTED_GURU_RULES)
        self.assertEqual(inventory["managed_path_claims"], ownership.EXPECTED_MANAGED_PATH_CLAIMS)
        self.assertEqual(
            first["overlay_paths_sha256"],
            ownership.path_set_sha256(sorted(ownership.EXPECTED_FINISH_OVERLAY_CLAIMS)),
        )

    def test_schema_is_valid_draft_2020_12_and_accepts_inventory(self) -> None:
        if importlib.util.find_spec("jsonschema") is None:
            self.skipTest("optional jsonschema dependency is not installed")
        from jsonschema import Draft202012Validator

        schema = json.loads((self.repo / ownership.SCHEMA_RELATIVE).read_text(encoding="utf-8"))
        inventory = json.loads((self.repo / ownership.INVENTORY_RELATIVE).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        self.assertEqual(list(Draft202012Validator(schema).iter_errors(inventory)), [])

    def test_finish_overlay_must_be_regular(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self.copy_minimal_source(repo)
            relative = ".codex/prompts/guru-finish-work.md"
            overlay = repo / ownership.OVERLAY_ROOT_RELATIVE / relative
            overlay.unlink()
            overlay.symlink_to("guru-finish-work-local.md")
            payload = ownership.validate_repository(repo)

        self.assertEqual(payload["status"], "error")
        self.assertIn(
            "overlay_not_regular",
            {item["code"] for item in payload["errors"] if item["path"] == relative},
        )

    def test_missing_managed_asset_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self.copy_minimal_source(repo)
            relative = "scripts/bash/check-env.sh"
            (repo / ownership.WORKFLOW_ROOT_RELATIVE / relative).unlink()
            payload = ownership.validate_repository(repo)

        self.assertEqual(payload["status"], "error")
        self.assertIn(
            "missing_managed_asset",
            {item["code"] for item in payload["errors"] if item["path"] == relative},
        )

    def test_extra_canonical_package_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self.copy_minimal_source(repo)
            (repo / ownership.SKILL_PACKAGE_ROOT_RELATIVE / "guru-extra").mkdir()
            payload = ownership.validate_repository(repo)

        self.assertEqual(payload["status"], "error")
        self.assertIn("canonical_package_set_mismatch", {item["code"] for item in payload["errors"]})

    def test_bash_entry_preserves_json_and_exit_status(self) -> None:
        command = self.repo / "trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh"
        completed = subprocess.run(
            [str(command), "--repo", str(self.repo), "--json"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["status"], "ok")


if __name__ == "__main__":
    unittest.main()
