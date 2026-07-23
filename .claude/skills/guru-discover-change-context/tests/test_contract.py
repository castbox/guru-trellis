from __future__ import annotations

import importlib.util
import copy
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class ChangeContextPackageContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.package = Path(__file__).resolve().parents[1]
        self.interface = json.loads((self.package / "interface.json").read_text(encoding="utf-8"))

    def test_identity_modes_semantic_stages_runtime_and_exits(self) -> None:
        self.assertEqual(self.interface["id"], "guru-discover-change-context")
        self.assertEqual(self.interface["schema_version"], "1.3")
        self.assertEqual(self.interface["judgment_mode"], "semantic")
        workflow = self.interface["modes"]["workflow"]
        standalone = self.interface["modes"]["standalone"]
        self.assertEqual(workflow["routing"], "global_workflow")
        self.assertEqual(standalone["routing"], "direct_discovery")
        self.assertEqual(workflow["entry_precondition_ids"], standalone["entry_precondition_ids"])
        self.assertEqual(
            workflow["entry_precondition_ids"],
            ["runtime_dependency", "fresh_base", "repository_identity", "change_input", "evidence_freshness"],
        )
        self.assertEqual(
            self.interface["ordered_stages"],
            ["forward_behavior", "ai_review_gate", "conditional_human_confirmation", "recorder_validator", "typed_exit"],
        )
        self.assertEqual(
            {item["id"]: item["runtime_command"] for item in self.interface["validators"]},
            {
                "history_previewer": "preview-change-context-history",
                "snapshot_recorder": "record-context-discovery",
                "snapshot_validator": "check-context-discovery",
                "public_invocation": "invoke-stage0-skill",
            },
        )
        self.assertEqual(
            [item["id"] for item in self.interface["external_exits"]],
            ["context_ready", "refresh_base", "blocked"],
        )
        self.assertEqual(
            self.interface["external_exits"][0]["consumer"],
            {"kind": "skill", "id": "guru-clarify-requirements"},
        )

    def test_contract_keeps_semantic_and_history_boundaries(self) -> None:
        skill = (self.package / "SKILL.md").read_text(encoding="utf-8")
        contract = (self.package / "references/contract.md").read_text(encoding="utf-8")
        normalized_skill = " ".join(skill.split())
        normalized_contract = " ".join(contract.split())
        for phrase in (
            "closed loop",
            "AI Review Gate before any",
            "stdout-only",
            "not self-contained or portable",
        ):
            self.assertIn(phrase, normalized_skill)
        for phrase in (
            "Current-state review must finish before history preview",
            "guru-context-history-score-1.0",
            "finish-summary.json",
            ".trellis/tasks/archive/**/finish-summary.json",
            ".trellis/workspace/**",
            "one to three selected candidates",
            "decision_owned_by_guru-clarify-requirements",
            "--expected-snapshot-sha256",
            "complete validator-passed `guru-base-sync-result-1.0`",
            "live body digest must equal the original reviewed draft body digest",
            "source issue may be live `open` or `closed`",
            "resolves from `HEAD:<path>` to exactly a `blob`",
            "source-specific portable locator",
            "matching live stale facts return `refresh_base` for complete re-entry",
            "at least one array must be non-empty",
            "facts_sha256` is recomputed from those returned fields",
            "do not issue a second duplicate search or re-read candidates after review",
            "git check-ignore --quiet --no-index --",
            "Skill `guru-clarify-requirements`",
            "context_ready",
            "refresh_base",
        ):
            self.assertIn(phrase, normalized_contract)
        self.assertNotIn("finish-summary-index.json` as an input", contract)

    def test_wrappers_are_dispatcher_only_and_executable(self) -> None:
        wrappers = {
            "preview-change-context-history.sh": "history_previewer",
            "record-context-discovery.sh": "snapshot_recorder",
            "check-context-discovery.sh": "snapshot_validator",
        }
        for name, validator in wrappers.items():
            path = self.package / "scripts" / name
            wrapper = path.read_text(encoding="utf-8")
            self.assertTrue(path.stat().st_mode & 0o100)
            self.assertIn("run-skill-command.sh", wrapper)
            self.assertIn(f"--validator {validator}", wrapper)
            self.assertNotIn("guru_team_trellis.py", wrapper)
            self.assertNotIn(".trellis/tasks/archive", wrapper)

    def test_package_only_copy_fails_with_full_preset_remediation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "guru-discover-change-context"
            shutil.copytree(self.package, copied)
            for name in (
                "preview-change-context-history.sh",
                "record-context-discovery.sh",
                "check-context-discovery.sh",
            ):
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

    def test_schema_and_deidentified_example(self) -> None:
        schema = json.loads((self.package / "schemas/context-discovery.schema.json").read_text(encoding="utf-8"))
        example = json.loads((self.package / "examples/context-discovery.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["$id"], "https://github.com/castbox/guru-trellis/schemas/guru-context-discovery-1.0.json")
        self.assertIn("task_worktree_state", schema["properties"])
        self.assertNotIn("task_worktree_state", schema["required"])
        self.assertIn("superseded_snapshot_sha256", schema["properties"])
        self.assertNotIn("superseded_snapshot_sha256", schema["required"])
        self.assertEqual(example["skill_id"], "guru-discover-change-context")
        if importlib.util.find_spec("jsonschema") is not None:
            from jsonschema import Draft202012Validator

            Draft202012Validator.check_schema(schema)
            validator = Draft202012Validator(schema)
            self.assertEqual(list(validator.iter_errors(example)), [])
            task_local = copy.deepcopy(example)
            task_local["task_worktree_state"] = {
                "head": "1" * 40,
                "context_snapshot_path": ".trellis/tasks/example/context-discovery.json",
                "entries": [{
                    "path": "trellis/runtime.py",
                    "index_status": "",
                    "worktree_status": "M",
                    "untracked": False,
                    "deleted": False,
                    "renamed_from": None,
                    "copied_from": None,
                    "index_blob": "2" * 40,
                    "worktree_sha256": "3" * 64,
                    "mode": "100644",
                }],
                "digest": "4" * 64,
            }
            self.assertEqual(list(validator.iter_errors(task_local)), [])
            invalid_task_local = copy.deepcopy(task_local)
            invalid_task_local["task_worktree_state"]["entries"][0]["unexpected"] = True
            self.assertNotEqual(list(validator.iter_errors(invalid_task_local)), [])
            invalid_mem = copy.deepcopy(example)
            invalid_mem["mem_review"].update({
                "status": "used",
                "load_bearing_question": "Which source owns this?",
                "exhausted_sources": {
                    "task_artifacts": True,
                    "current_docs_code_tests": True,
                    "github": True,
                    "git_history": True,
                },
                "summary": "",
            })
            self.assertNotEqual(list(validator.iter_errors(invalid_mem)), [])
            for field in ("reviewed_scope", "load_bearing_conclusions"):
                invalid_gate = copy.deepcopy(example)
                invalid_gate["ai_review_gate"][field] = []
                self.assertNotEqual(list(validator.iter_errors(invalid_gate)), [])
            blocked_with_passed_gate = copy.deepcopy(example)
            blocked_with_passed_gate["typed_exit"] = "blocked"
            blocked_with_passed_gate["error"] = {
                "codes": ["semantic_review_blocked"],
                "summary": "The semantic review could not form safe evidence.",
            }
            self.assertNotEqual(
                list(validator.iter_errors(blocked_with_passed_gate)), []
            )
            blocked_gate_with_ready_exit = copy.deepcopy(example)
            blocked_gate_with_ready_exit["ai_review_gate"]["status"] = "blocked"
            self.assertNotEqual(
                list(validator.iter_errors(blocked_gate_with_ready_exit)), []
            )
            valid_blocked = copy.deepcopy(blocked_with_passed_gate)
            valid_blocked["ai_review_gate"]["status"] = "blocked"
            self.assertEqual(list(validator.iter_errors(valid_blocked)), [])
            missing_base_result = copy.deepcopy(example)
            del missing_base_result["base_evidence"]["sync_result"]
            self.assertNotEqual(list(validator.iter_errors(missing_base_result)), [])
            missing_issue_binding = copy.deepcopy(example)
            missing_issue_binding["live_change"]["issue_binding"] = None
            self.assertNotEqual(list(validator.iter_errors(missing_issue_binding)), [])
            closed_source = copy.deepcopy(example)
            closed_source["live_change"] = {
                "kind": "issue",
                "identity": "https://github.com/example/guru-extension/issues/123",
                "state": "closed",
                "updated_at": "2026-01-01T00:00:00Z",
                "body_sha256": "3" * 64,
                "facts_sha256": "4" * 64,
                "issue_binding": None,
            }
            self.assertEqual(list(validator.iter_errors(closed_source)), [])
            closed_duplicate = copy.deepcopy(closed_source)
            closed_duplicate["duplicate_search"]["candidates"] = [{
                "repo": "example/guru-extension",
                "number": 99,
                "identity": "#99",
                "url": "https://github.com/example/guru-extension/issues/99",
                "state": "closed",
                "updated_at": "2026-01-01T00:00:00Z",
                "facts_sha256": "a" * 64,
                "reason": "Possible duplicate.",
                "observation": "Must remain open to be a duplicate candidate.",
            }]
            self.assertNotEqual(list(validator.iter_errors(closed_duplicate)), [])
            empty_change = copy.deepcopy(example)
            empty_change["change_input"] = {
                kind: [] for kind in (
                    "issue_refs", "pr_refs", "branches", "paths", "commands",
                    "config_keys", "schema_fields", "symbols", "terms", "queries",
                )
            }
            self.assertNotEqual(list(validator.iter_errors(empty_change)), [])
            clue_values = {
                "issue_refs": "#123",
                "pr_refs": "PR #123",
                "branches": "feat/context",
                "paths": "docs/context.md",
                "commands": "/trellis:continue",
                "config_keys": "context.mode",
                "schema_fields": "snapshot_sha256",
                "symbols": "ContextDiscovery",
                "terms": "change context",
                "queries": "discover context",
            }
            for kind, value in clue_values.items():
                single = copy.deepcopy(example)
                single["change_input"] = {
                    clue_kind: [value] if clue_kind == kind else []
                    for clue_kind in clue_values
                }
                if kind != "issue_refs":
                    single["live_change"]["issue_binding"] = None
                with self.subTest(single_clue=kind):
                    self.assertEqual(list(validator.iter_errors(single)), [])
        serialized = json.dumps(example, ensure_ascii=False)
        self.assertNotIn("/Users/", serialized)
        self.assertNotIn(".trellis/workspace/", serialized)
        self.assertNotIn(".trellis/.runtime/", serialized)


if __name__ == "__main__":
    unittest.main()
