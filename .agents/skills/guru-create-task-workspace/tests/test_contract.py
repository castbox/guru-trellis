from __future__ import annotations

import importlib.util
import copy
import json
import os
import subprocess
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def load_runtime():
    candidates = []
    for ancestor in [PACKAGE_ROOT, *PACKAGE_ROOT.parents]:
        candidates.extend([
            ancestor / "trellis/workflows/guru-team/scripts/python/guru_team_trellis.py",
            ancestor / ".trellis/guru-team/scripts/python/guru_team_trellis.py",
        ])
    runtime_path = next((path for path in candidates if path.is_file()), None)
    if runtime_path is None:
        raise RuntimeError("Compatible Guru Team runtime not found for package tests.")
    spec = importlib.util.spec_from_file_location("task_workspace_runtime", runtime_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Compatible Guru Team runtime could not be loaded.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GTT = load_runtime()


class TaskWorkspacePackageContractTests(unittest.TestCase):
    def test_interface_uses_semantic_profile_and_mode_parity(self) -> None:
        interface = json.loads((PACKAGE_ROOT / "interface.json").read_text(encoding="utf-8"))
        self.assertEqual(interface["schema_version"], "1.2")
        self.assertEqual(interface["id"], "guru-create-task-workspace")
        self.assertEqual(interface["judgment_mode"], "semantic")
        self.assertEqual(
            interface["modes"]["workflow"]["entry_precondition_ids"],
            interface["modes"]["standalone"]["entry_precondition_ids"],
        )
        self.assertEqual(interface["runtime_dependency"], GTT.SKILL_RUNTIME_DEPENDENCY)
        self.assertEqual(
            [item["id"] for item in interface["external_exits"]],
            ["created", "refresh_review", "cancelled", "blocked"],
        )
        self.assertEqual(
            {item["runtime_command"] for item in interface["validators"]},
            {"record-task-workspace-plan", "create-task-workspace", "check-task-workspace-result"},
        )

    def test_public_examples_match_closed_schemas(self) -> None:
        for stem in ("task-workspace-plan", "task-workspace-result"):
            schema = json.loads((PACKAGE_ROOT / "schemas" / f"{stem}.schema.json").read_text(encoding="utf-8"))
            example = json.loads((PACKAGE_ROOT / "examples" / f"{stem}.json").read_text(encoding="utf-8"))
            errors = GTT.skill_json_schema_validation_errors(example, schema, stem)
            self.assertEqual(errors, [], errors)

    def test_plan_schema_closes_target_variants_and_portable_paths(self) -> None:
        schema = json.loads((PACKAGE_ROOT / "schemas/task-workspace-plan.schema.json").read_text(encoding="utf-8"))
        example = json.loads((PACKAGE_ROOT / "examples/task-workspace-plan.json").read_text(encoding="utf-8"))

        wrong_kind = copy.deepcopy(example)
        wrong_kind["invocation"]["target_kind"] = "reviewed_draft"
        self.assertTrue(GTT.skill_json_schema_validation_errors(wrong_kind, schema, "wrong target kind"))

        unclosed_issue = copy.deepcopy(example)
        unclosed_issue["target"]["draft"] = {
            "draft_id": "draft-27",
            "source_request_sha256": "a" * 64,
            "title": "Draft title",
            "body": "Draft body",
            "labels": [],
            "reviewed_draft_sha256": "b" * 64,
        }
        self.assertTrue(GTT.skill_json_schema_validation_errors(unclosed_issue, schema, "unclosed issue"))

        absolute_evidence = copy.deepcopy(example)
        absolute_evidence["prerequisites"]["base"]["artifact"] = "/tmp/base-sync-result.json"
        self.assertTrue(GTT.skill_json_schema_validation_errors(absolute_evidence, schema, "absolute evidence"))

        reviewed_draft = copy.deepcopy(example)
        reviewed_draft["invocation"].update({"target_kind": "reviewed_draft", "action_scope": "github_issue_mutation"})
        reviewed_draft["target"].update({
            "kind": "reviewed_draft",
            "issue_number": None,
            "url": None,
            "state": None,
            "updated_at": None,
            "draft": {
                "draft_id": "draft-27",
                "source_request_sha256": "a" * 64,
                "title": "Draft title",
                "body": "Draft body",
                "labels": ["workflow"],
                "reviewed_draft_sha256": "b" * 64,
            },
            "created_issue_binding_sha256": None,
        })
        reviewed_draft["side_effects"] = {
            "operations": ["create_issue"],
            "task_artifacts": [],
            "runtime_mappings": [],
            "command_argv": ["create-task-workspace", "--input", "task-workspace-plan.json"],
            "stop_after": "created_issue_refresh",
        }
        reviewed_draft["confirmations"]["github_issue_mutation"]["status"] = "confirmed"
        reviewed_draft["confirmations"]["workspace_and_task_mutation"] = {
            "status": "not_in_current_invocation",
            "source": None,
            "reviewed_plan_sha256": None,
            "evidence": None,
            "confirmation_sha256": None,
        }
        self.assertEqual(GTT.skill_json_schema_validation_errors(reviewed_draft, schema, "reviewed draft"), [])

    def test_result_schema_closes_no_side_effect_union(self) -> None:
        schema = json.loads((PACKAGE_ROOT / "schemas/task-workspace-result.schema.json").read_text(encoding="utf-8"))
        example = json.loads((PACKAGE_ROOT / "examples/task-workspace-result.json").read_text(encoding="utf-8"))
        no_effect = copy.deepcopy(example)
        no_effect.update({
            "variant": "no_side_effect",
            "created_issue": None,
            "created_workspace": None,
            "no_side_effect": {
                "reason_code": "user_cancelled",
                "before": {"head": "a" * 40, "status_sha256": "b" * 64, "worktrees_sha256": "c" * 64, "issues_sha256": "d" * 64},
                "after": {"head": "a" * 40, "status_sha256": "b" * 64, "worktrees_sha256": "c" * 64, "issues_sha256": "d" * 64},
                "zero_writes": True,
            },
            "typed_exit": "cancelled",
            "consumer": {"kind": "stop", "id": "task-workspace-cancelled"},
        })
        self.assertEqual(GTT.skill_json_schema_validation_errors(no_effect, schema, "no effect"), [])
        no_effect["typed_exit"] = "created"
        no_effect["consumer"] = {"kind": "workflow", "id": "guru-task-workspace-created"}
        self.assertTrue(GTT.skill_json_schema_validation_errors(no_effect, schema, "invalid no effect"))
        no_effect["typed_exit"] = "blocked"
        no_effect["consumer"] = {"kind": "stop", "id": "task-workspace-blocked"}
        no_effect["created_workspace"] = copy.deepcopy(example["created_workspace"])
        self.assertTrue(GTT.skill_json_schema_validation_errors(no_effect, schema, "mixed no effect"))

    def test_public_result_example_contains_no_absolute_path(self) -> None:
        example = json.loads((PACKAGE_ROOT / "examples/task-workspace-result.json").read_text(encoding="utf-8"))

        def strings(value: object):
            if isinstance(value, dict):
                for child in value.values():
                    yield from strings(child)
            elif isinstance(value, list):
                for child in value:
                    yield from strings(child)
            elif isinstance(value, str):
                yield value

        for value in strings(example):
            self.assertFalse(Path(value).is_absolute(), value)

    def test_wrappers_are_thin_and_fail_without_installed_runtime(self) -> None:
        for name in (
            "record-task-workspace-plan.sh",
            "create-task-workspace.sh",
            "check-task-workspace-result.sh",
        ):
            path = PACKAGE_ROOT / "scripts" / name
            text = path.read_text(encoding="utf-8")
            self.assertIn("run-skill-command.sh", text)
            self.assertNotIn("guru_team_trellis.py", text)
            self.assertTrue(os.access(path, os.X_OK), name)
            result = subprocess.run([str(path), "--help"], text=True, capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("not self-contained", result.stderr)

    def test_contract_keeps_semantic_and_deterministic_owners_separate(self) -> None:
        contract = (PACKAGE_ROOT / "references/contract.md").read_text(encoding="utf-8")
        self.assertIn("AI Review Gate", contract)
        self.assertIn("github_issue_mutation", contract)
        self.assertIn("workspace_and_task_mutation", contract)
        self.assertIn("official `common.task_store.cmd_create`", contract)
        self.assertIn("developer accessor with a null", contract)
        self.assertIn(
            "`task.json.creator=task.json.assignee=<reviewed-login>`",
            contract,
        )
        self.assertIn("existing official identity bytes remain exact", contract)
        self.assertIn("does not trim them or append a newline", contract)
        self.assertIn("`prepare-task` is query-only", contract)
        self.assertNotIn("init_developer.py <name>", contract)


if __name__ == "__main__":
    unittest.main()
