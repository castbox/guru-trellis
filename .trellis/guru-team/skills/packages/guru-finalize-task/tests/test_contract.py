from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest
from unittest import mock

from jsonschema import Draft202012Validator


PACKAGE = Path(__file__).resolve().parents[1]


def load(relative: str):
    return json.loads((PACKAGE / relative).read_text(encoding="utf-8"))


def load_runtime():
    path = PACKAGE / "runtime" / "owner.py"
    spec = importlib.util.spec_from_file_location("finalize_task_runtime", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GTT = load_runtime()


class FinalizeTaskContractTests(unittest.TestCase):
    def test_all_json_documents_and_schemas_are_valid(self) -> None:
        for path in PACKAGE.rglob("*.json"):
            with self.subTest(path=path.relative_to(PACKAGE)):
                payload = json.loads(path.read_text(encoding="utf-8"))
                if path.name.endswith(".schema.json"):
                    Draft202012Validator.check_schema(payload)

    def test_current_lifecycle_module_is_packaged(self) -> None:
        self.assertTrue((PACKAGE / "runtime/lifecycle.py").is_file())

    def test_interface_projects_minimal_merge_identity(self) -> None:
        interface = load("interface.json")
        projection = next(
            item for item in interface["public_contracts"]["projections"]
            if item["id"] == "project_ready_for_merge"
        )
        self.assertEqual(
            [item["source"] for item in projection["mappings"]],
            ["repo_ref", "pr_number", "pr_url", "expected_head_sha", "expected_base_branch", "expected_head_branch"],
        )

    def test_transaction_binds_only_publication_payload(self) -> None:
        plan = {
            "task": {"active_locator": ".trellis/tasks/current"},
            "git": {
                "repo": "castbox/guru-trellis", "base_branch": "main",
                "head_branch": "codex/247", "branch_review_commit": "a" * 40,
                "publication_head": "b" * 40,
            },
            "plan_digest": "c" * 64,
            "publish": {"title": "修订 Finalizer", "body": "Closes #247"},
        }
        transaction = GTT.finalization_transaction_from_plan(
            plan, next_transition="push_content", pre_push_remote_head=""
        )
        self.assertEqual(transaction["publication"], plan["publish"])
        Draft202012Validator(load("schemas/finalization-transaction.schema.json")).validate(transaction)

    def test_ready_output_has_no_close_projection(self) -> None:
        output = load("examples/public-ready-for-merge-output.json")
        Draft202012Validator(load("schemas/public-ready-for-merge-output.schema.json")).validate(output)

    def test_pr_quality_accepts_publication_owned_closing_keyword(self) -> None:
        body = """## 变更摘要\n- 删除旧关闭数组\n\n## 影响范围\nFinalizer 只绑定 PR payload。\n\n## 验证结果\n已运行 targeted tests。\n\n## 安全说明\n无新增安全影响。\n\n## Review Gate\nPublication 已审查精确 PR payload。\n\n## Issue 关闭范围\n由本 PR body 表达关闭效果。\n\n## Docs SSOT\n- requirements: current\n- design: current\n- tests: current\n\nCloses #247\n"""
        errors = GTT.validate_pr_body_quality(body, False)
        self.assertFalse(any("close keyword" in error for error in errors))

    def test_existing_pr_recovery_compares_exact_title_and_body(self) -> None:
        plan = {
            "git": {
                "repo": "castbox/guru-trellis", "remote": "origin",
                "head_branch": "codex/247", "base_branch": "main",
                "publication_head": "b" * 40, "branch_review_commit": "a" * 40,
            },
            "publish": {"title": "当前标题", "body": "Closes #247"},
        }
        pr = {
            "number": 247, "url": "https://github.com/castbox/guru-trellis/pull/247",
            "title": "旧标题", "body": "Refs #247", "isDraft": True,
            "headRefOid": "a" * 40,
        }
        with mock.patch.object(GTT, "is_ancestor", return_value=True):
            result = GTT.classify_existing_pr_recovery(
                Path("."), plan, existing_pr=pr, remote_head="a" * 40
            )
        self.assertTrue(result["metadata_update_required"])
        self.assertFalse(result["metadata_comparison"]["title_matches"])
        self.assertFalse(result["metadata_comparison"]["body_matches"])

    def test_metadata_commit_subject_is_issue_independent(self) -> None:
        self.assertEqual(GTT.format_metadata_commit_subject(), "chore(trellis): 固化任务收尾元数据")

    def test_owner_fragments_satisfy_line_limit(self) -> None:
        for path in sorted((PACKAGE / "runtime").glob("_owner_part_*.py")):
            with self.subTest(path=path.name):
                self.assertLessEqual(len(path.read_text(encoding="utf-8").splitlines()), 3000)


if __name__ == "__main__":
    unittest.main()
