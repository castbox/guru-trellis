from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class BaseSyncPackageContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.package = Path(__file__).resolve().parents[1]
        self.interface = json.loads((self.package / "interface.json").read_text(encoding="utf-8"))

    def test_identity_modes_stages_runtime_and_exits(self) -> None:
        self.assertEqual(self.interface["id"], "guru-sync-base")
        self.assertEqual(self.interface["schema_version"], "1.1")
        workflow = self.interface["modes"]["workflow"]
        standalone = self.interface["modes"]["standalone"]
        self.assertEqual(workflow["routing"], "global_workflow")
        self.assertEqual(standalone["routing"], "direct_discovery")
        self.assertEqual(workflow["entry_precondition_ids"], standalone["entry_precondition_ids"])
        self.assertEqual(
            workflow["entry_precondition_ids"],
            [
                "invocation_intent",
                "runtime_dependency",
                "decision_checkout",
                "selected_base_resolution",
                "clean_checkout",
                "result_evidence",
            ],
        )
        self.assertEqual(
            self.interface["ordered_stages"],
            [
                "forward_behavior",
                "ai_review_gate",
                "conditional_human_confirmation",
                "recorder_validator",
                "typed_exit",
            ],
        )
        self.assertEqual(
            {item["id"]: item["runtime_command"] for item in self.interface["validators"]},
            {"sync_executor": "sync-base", "result_validator": "check-base-sync"},
        )
        self.assertEqual(
            [item["id"] for item in self.interface["external_exits"]],
            ["synced", "skipped", "blocked"],
        )

    def test_skill_and_contract_keep_ai_script_boundary(self) -> None:
        skill = (self.package / "SKILL.md").read_text(encoding="utf-8")
        contract = (self.package / "references/contract.md").read_text(encoding="utf-8")
        normalized_contract = " ".join(contract.split())
        for phrase in ("Resolve first", "AI Review Gate", "not self-contained or portable"):
            self.assertIn(phrase, skill)
        self.assertIn(
            "resolve-only -> AI selected-base review -> conditional conflict confirmation "
            "-> digest-bound execute -> mandatory post-execution AI Review Gate "
            "-> objective result validation + result cleanup "
            "-> standalone resolution cleanup | workflow resolution lease transfer "
            "-> typed exit",
            normalized_contract,
        )
        for phrase in (
            "never consults current branch as a fallback",
            "AI Selected-Base Review",
            "Mandatory Post-Execution AI Review Gate",
            "git merge --ff-only",
            "decision checkout HEAD == local selected-base HEAD == remote-tracking HEAD",
            "--expected-resolution-sha256",
            "must never turn config, remote-default, or fallback provenance into explicit",
            "--release-resolution-evidence",
            "user-confirmation-pending route is non-terminal",
            "No result or lease path/digest is written",
            "run-skill-command",
        ):
            self.assertIn(phrase, contract)
        self.assertIn(
            "task-created, blocked, aborted, or superseded terminal routes",
            normalized_contract,
        )
        self.assertLess(
            contract.index("## AI Selected-Base Review"),
            contract.index("## Digest-Bound Execution"),
        )
        self.assertLess(
            contract.index("## Digest-Bound Execution"),
            contract.index("## Mandatory Post-Execution AI Review Gate"),
        )
        self.assertLess(
            contract.index("## Mandatory Post-Execution AI Review Gate"),
            contract.index("## Objective Validation And Exits"),
        )
        self.assertIn("It never\nuses `git branch -f`", contract)
        selected = next(
            item for item in self.interface["entry_preconditions"]
            if item["id"] == "selected_base_resolution"
        )
        self.assertIn("prepare-task", selected["binding"])
        self.assertIn("each GitHub/worktree/task mutation", selected["freshness"])
        self.assertIn("terminal release", selected["freshness"])
        synced = next(
            item for item in self.interface["external_exits"] if item["id"] == "synced"
        )
        self.assertIn("active external resolution raw-byte/digest lease", synced["evidence"])

    def test_wrappers_are_dispatcher_only(self) -> None:
        for name, validator in (
            ("sync-base.sh", "sync_executor"),
            ("check-base-sync.sh", "result_validator"),
        ):
            wrapper = (self.package / "scripts" / name).read_text(encoding="utf-8")
            self.assertIn("run-skill-command.sh", wrapper)
            self.assertIn(f"--validator {validator}", wrapper)
            self.assertNotIn("guru_team_trellis.py", wrapper)
            self.assertNotIn("git fetch", wrapper)
            self.assertNotIn("git merge", wrapper)

    def test_package_only_copy_fails_with_full_preset_remediation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "guru-sync-base"
            shutil.copytree(self.package, copied)
            for name in ("sync-base.sh", "check-base-sync.sh"):
                result = subprocess.run(
                    [str(copied / "scripts" / name), "--help"],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
                self.assertEqual(result.returncode, 2, result)
                self.assertIn("not self-contained or portable", result.stderr)
                self.assertIn("Install or upgrade the complete Guru Team preset", result.stderr)

    def test_schema_example_and_digest(self) -> None:
        schema = json.loads(
            (self.package / "schemas/base-sync-result.schema.json").read_text(encoding="utf-8")
        )
        example = json.loads(
            (self.package / "examples/base-sync-result.json").read_text(encoding="utf-8")
        )
        if importlib.util.find_spec("jsonschema") is not None:
            from jsonschema import Draft202012Validator

            Draft202012Validator.check_schema(schema)
            self.assertEqual(list(Draft202012Validator(schema).iter_errors(example)), [])
        normalized = dict(example)
        digest = normalized.pop("facts_sha256")
        encoded = json.dumps(
            normalized,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        self.assertEqual(hashlib.sha256(encoded).hexdigest(), digest)
        self.assertEqual(
            example["decision_checkout"]["head_after"],
            example["git"]["local_head_after"],
        )
        self.assertEqual(example["git"]["local_head_after"], example["git"]["remote_head_after"])
        self.assertNotIn("/Users/", json.dumps(example))


if __name__ == "__main__":
    unittest.main()
