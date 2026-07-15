#!/usr/bin/env python3
"""Focused regression tests for the upstream ownership freeze."""

from __future__ import annotations

import copy
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
        ]
        files = [
            ownership.EXTENSION_RELATIVE,
            ownership.INSTALLER_RELATIVE,
            ownership.SKILL_REGISTRY_RELATIVE,
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
        if mutation_type == "append_legacy_clone":
            source = next(item for item in inventory["legacy_entries"] if item["path"] == mutation["source_path"])
            clone = copy.deepcopy(source)
            clone["path"] = mutation["new_path"]
            inventory["legacy_entries"].append(clone)
            self.write_json(inventory_path, inventory)
            return
        if mutation_type == "append_overlay_bytes":
            path = repo / ownership.OVERLAY_ROOT_RELATIVE / mutation["path"]
            path.write_bytes(path.read_bytes() + mutation["content"].encode("utf-8"))
            return
        if mutation_type == "remove_legacy_ownership_fields":
            entry = next(item for item in inventory["legacy_entries"] if item["path"] == mutation["path"])
            for field in mutation["fields"]:
                entry.pop(field)
            self.write_json(inventory_path, inventory)
            return
        if mutation_type == "set_legacy_category":
            entry = next(item for item in inventory["legacy_entries"] if item["path"] == mutation["path"])
            entry["category"] = mutation["category"]
            self.write_json(inventory_path, inventory)
            return
        if mutation_type == "add_upstream_managed_claim":
            inventory["managed_path_claims"].append({
                "path": mutation["path"],
                "category": "upstream_owned",
                "classification_rule": "frozen-legacy-overlay-coverage",
                "covered_by_legacy_paths": [],
            })
            self.write_json(inventory_path, inventory)
            extension_path = repo / ownership.EXTENSION_RELATIVE
            extension = json.loads(extension_path.read_text(encoding="utf-8"))
            extension["public_api"]["managed_paths"].append(mutation["path"])
            self.write_json(extension_path, extension)
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
                self.assertEqual(payload["status"], fixture["expected_status"])
                codes = {item["code"] for item in payload["errors"]}
                self.assertTrue(set(fixture["expected_error_codes"]).issubset(codes), (fixture_path.name, payload))
                for error in payload["errors"]:
                    self.assertEqual(set(error), {"code", "path", "detail"})

    def test_baseline_facts_are_stable(self) -> None:
        first = ownership.validate_repository(self.repo)
        second = ownership.validate_repository(self.repo)
        self.assertEqual(first, second)
        self.assertEqual(first["status"], "ok")
        self.assertEqual(first["frozen_count"], 43)
        self.assertEqual(first["active_count"], 43)
        self.assertEqual(first["generated_in_clean_init_count"], 37)
        self.assertEqual(first["legacy_not_generated_count"], 6)
        inventory = json.loads((self.repo / ownership.INVENTORY_RELATIVE).read_text(encoding="utf-8"))
        self.assertEqual(first["schema_sha256"], ownership.sha256_file(self.repo / ownership.SCHEMA_RELATIVE))
        self.assertEqual(first["inventory_sha256"], ownership.sha256_file(self.repo / ownership.INVENTORY_RELATIVE))
        self.assertEqual(first["guru_owned_rules_sha256"], ownership.canonical_sha256(inventory["guru_owned_rules"]))
        self.assertEqual(first["managed_path_claims_sha256"], ownership.canonical_sha256(inventory["managed_path_claims"]))
        self.assertEqual(first["legacy_entries_sha256"], ownership.canonical_sha256(inventory["legacy_entries"]))
        self.assertEqual(first["facts_sha256"], "993676201e239fd50c5084d3c89eac9c97a4f1150ed50b03da4d74e20cbefa48")

        recorded_owners = {
            owner
            for entry in inventory["legacy_entries"]
            for owner in entry["replacement_owners"]
        }
        self.assertTrue(recorded_owners.issubset(ownership.EXPECTED_REPLACEMENT_OWNERS))
        self.assertNotIn("guru-start-task", recorded_owners)

    def test_schema_is_valid_draft_2020_12_and_accepts_inventory(self) -> None:
        if importlib.util.find_spec("jsonschema") is None:
            self.skipTest("optional jsonschema dependency is not installed")
        from jsonschema import Draft202012Validator

        schema = json.loads((self.repo / ownership.SCHEMA_RELATIVE).read_text(encoding="utf-8"))
        inventory = json.loads((self.repo / ownership.INVENTORY_RELATIVE).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        self.assertEqual(list(Draft202012Validator(schema).iter_errors(inventory)), [])

    def test_unknown_replacement_owner_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self.copy_minimal_source(repo)
            inventory_path = repo / ownership.INVENTORY_RELATIVE
            inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
            inventory["legacy_entries"][0]["replacement_owners"] = ["guru-start-task"]
            self.write_json(inventory_path, inventory)
            payload = ownership.validate_repository(repo)

        self.assertEqual(payload["status"], "error")
        errors = [item for item in payload["errors"] if item["code"] == "unknown_replacement_owner"]
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["path"], inventory["legacy_entries"][0]["path"])

    def test_replacement_owner_requires_its_live_blocking_issue(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self.copy_minimal_source(repo)
            inventory_path = repo / ownership.INVENTORY_RELATIVE
            inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
            inventory["legacy_entries"][0]["blocking_issues"] = [112]
            self.write_json(inventory_path, inventory)
            payload = ownership.validate_repository(repo)

        self.assertEqual(payload["status"], "error")
        errors = [
            item
            for item in payload["errors"]
            if item["code"] == "replacement_owner_issue_mismatch"
        ]
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["path"], inventory["legacy_entries"][0]["path"])

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
