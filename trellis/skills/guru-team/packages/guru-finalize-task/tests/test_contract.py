from __future__ import annotations

import copy
import importlib.util
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import jsonschema


PACKAGE = Path(__file__).resolve().parents[1]


def load(relative: str):
    return json.loads((PACKAGE / relative).read_text(encoding="utf-8"))


def load_runtime():
    runtime_path = PACKAGE / "runtime/owner.py"
    spec = importlib.util.spec_from_file_location("finalize_task_package_runtime", runtime_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GTT = load_runtime()


def shared_runtime_parent() -> Path:
    for parent in PACKAGE.parents:
        if (parent / "runtime/io.py").is_file():
            return parent
    raise AssertionError("shared Guru Team runtime is unavailable")


def large_finish_summary() -> dict:
    paths = [f"changes/path-{index:04d}.txt" for index in range(2001)]
    title = "Large finish summary"
    index = {
        "problem": "Large diffs were rejected by an arbitrary path limit.",
        "outcome": "Complete large path sets are accepted.",
        "changed_behavior": ["Removed the arbitrary changed-path count limit."],
        "affected_surfaces": [{
            "kind": "schema",
            "name": "finish-summary",
            "paths": ["trellis/workflows/guru-team/schemas/finish-summary.schema.json"],
            "change": "Accept complete large path sets.",
        }],
        "contract_changes": [],
        "search_terms": {
            "issue_refs": ["#227"],
            "pr_refs": [],
            "branches": ["fix/227-finish-summary-large-path-set"],
            "paths": paths,
            "commands": [],
            "config_keys": [],
            "schema_fields": ["git.changed_paths", "index.search_terms.paths"],
            "symbols": ["finish_summary_errors"],
            "phrases": [
                "大型 diff 路径上限阻断",
                "finish_summary_errors 支持完整路径集",
                "已移除 finish summary limit",
            ],
        },
    }
    index["retrieval_text"] = GTT.current_finish_summary_retrieval_text(title, index)
    return {
        "schema_version": 2,
        "generated_at": "2026-08-14T00:00:00Z",
        "generator": "guru-team.finalize-task",
        "task": {
            "slug": "227-finish-summary-large-path-set",
            "title": title,
            "status": "completed",
            "artifact_dir": ".trellis/tasks/227-finish-summary-large-path-set",
            "archive_dir": ".trellis/tasks/archive/2026-08/227-finish-summary-large-path-set",
        },
        "git": {
            "base_branch": "main",
            "branch": "fix/227-finish-summary-large-path-set",
            "commits": ["a" * 40],
            "changed_paths": paths,
        },
        "github": {
            "source_issues": [227],
            "close_issues": [227],
            "related_issues": [],
            "followup_issues": [],
            "pr_url": "",
        },
        "artifacts": {},
        "index": index,
    }


class FinalizeTaskContractTests(unittest.TestCase):
    def test_large_finish_summary_preserves_complete_path_contract(self) -> None:
        payload = large_finish_summary()
        self.assertEqual(GTT.finish_summary_errors(payload), [])

        cases = {}
        mismatch = copy.deepcopy(payload)
        mismatch["index"]["search_terms"]["paths"] = payload["git"]["changed_paths"][:-1]
        cases["mismatch"] = (
            mismatch,
            "index.search_terms.paths must equal sorted git.changed_paths.",
        )
        unsorted = copy.deepcopy(payload)
        unsorted_paths = list(reversed(payload["git"]["changed_paths"]))
        unsorted["git"]["changed_paths"] = unsorted_paths
        unsorted["index"]["search_terms"]["paths"] = unsorted_paths
        cases["unsorted"] = (
            unsorted,
            "git.changed_paths must be sorted and unique.",
        )
        duplicate = copy.deepcopy(payload)
        duplicate_paths = payload["git"]["changed_paths"] + [payload["git"]["changed_paths"][-1]]
        duplicate["git"]["changed_paths"] = duplicate_paths
        duplicate["index"]["search_terms"]["paths"] = duplicate_paths
        cases["duplicate"] = (
            duplicate,
            "git.changed_paths must be sorted and unique.",
        )
        unsafe = copy.deepcopy(payload)
        unsafe_paths = payload["git"]["changed_paths"][:-1] + ["../unsafe.txt"]
        unsafe["git"]["changed_paths"] = unsafe_paths
        unsafe["index"]["search_terms"]["paths"] = unsafe_paths
        cases["unsafe"] = (
            unsafe,
            "git.changed_paths[] must not contain empty, dot, or parent segments.",
        )

        for name, (invalid, expected_error) in cases.items():
            with self.subTest(case=name):
                self.assertIn(expected_error, GTT.finish_summary_errors(invalid))

    def test_execute_ready_recovery_materializes_without_finish_work(self) -> None:
        public_input = {"task_ref": ".trellis/tasks/archive/2026-08/example"}
        gate = {"route": {"typed_exit": "ready_for_merge", "output": {"materialization": "executor"}}}
        task_dir = Path("/repo/.trellis/tasks/archive/2026-08/example")
        context = {
            "transaction_state": "ready",
            "task_dir": task_dir,
            "plan": {"plan_digest": "a" * 64},
            "published_pr": {"number": 218},
        }
        output = {"exit_id": "ready_for_merge", "pr_number": 218}
        args = SimpleNamespace(root="/repo", input="input.json", gate=None)
        with (
            mock.patch.object(GTT, "repo_root", return_value=Path("/repo")),
            mock.patch.object(GTT, "finalization_public_input", return_value=(public_input, Path("/repo/input.json"))),
            mock.patch.object(GTT, "finalization_gate_input", return_value=(gate, Path("/repo/gate.json"))),
            mock.patch.object(GTT, "check_finalization_gate_result", return_value=(gate, context)),
            mock.patch.object(GTT, "finalization_gate_with_ready_for_merge_output", return_value={"route": {"output": output}}) as materialize,
            mock.patch.object(GTT, "finalization_retire_current_state", return_value=["transaction", "gate"]) as retire,
            mock.patch.object(GTT, "cmd_finish_work") as finish_work,
        ):
            result = GTT.cmd_execute_finalization_transition(args)

        self.assertEqual(result["stage"], "ready_recovered")
        self.assertEqual(result["output"], output)
        self.assertEqual(result["retired_owner_state"], ["transaction", "gate"])
        finish_work.assert_not_called()
        retire.assert_called_once_with(Path("/repo"), task_dir)
        materialize.assert_called_once_with(
            Path("/repo"), task_dir, gate, context["plan"], context["published_pr"]
        )

    def test_step_local_contract_matches_current_gate_and_exit_graph(self) -> None:
        skill = (PACKAGE / "SKILL.md").read_text(encoding="utf-8")
        contract = (PACKAGE / "references/contract.md").read_text(encoding="utf-8")
        interface = load("interface.json")
        gate = load("schemas/task-finalization-gate-5.0.schema.json")
        exits = [item["id"] for item in interface["external_exits"]]
        output_exits = [item["exit_id"] for item in interface["public_contracts"]["outputs"]]

        self.assertIn("and six typed exits.", skill)
        self.assertIn("and six typed exits.", interface["description"])
        self.assertIn("current aggregate input is 6.0, gate is 5.0, and ignored transaction is 3.0", contract)
        self.assertIn("The four inputs are", contract)
        self.assertIn("The six exits are", contract)
        self.assertIn("3.0 and 4.0 gates", contract)
        self.assertEqual(6, len(exits))
        self.assertEqual(exits, output_exits)
        self.assertEqual(
            exits,
            gate["properties"]["route"]["properties"]["typed_exit"]["enum"],
        )
        self.assertEqual(exits[0], "base_reconciliation_required")

    def test_provenance_tail_accepts_only_semantic_spec_managed_hash(self) -> None:
        head = "a" * 40
        before = {
            "installed_at": "before",
            "source": {"ref": "before", "commit": "before", "tree_state": "dirty", "is_mutable_ref": True},
            "install": {"managed_assets": [".trellis/spec/workflow/semantic-retrieval.md"]},
        }
        after = {
            "installed_at": "after",
            "source": {"ref": head, "commit": head, "tree_state": "clean", "is_mutable_ref": False},
            "install": {
                "managed_assets": [".trellis/spec/workflow/semantic-retrieval.md"],
                "managed_asset_hashes": {
                    ".trellis/spec/workflow/semantic-retrieval.md": "b" * 64,
                },
            },
        }

        self.assertEqual(GTT.provenance_tail_manifest_errors(before, after, head), [])

        for field, value in (
            ("unexpected_install_field", True),
            ("managed_asset_hashes", {".trellis/spec/workflow/other.md": "c" * 64}),
        ):
            with self.subTest(field=field):
                invalid = json.loads(json.dumps(after))
                if field == "managed_asset_hashes":
                    invalid["install"][field].update(value)
                else:
                    invalid["install"][field] = value
                self.assertIn(
                    "provenance_tail_manifest_fields_outside_allowlist",
                    GTT.provenance_tail_manifest_errors(before, invalid, head),
                )

    def test_invoke_unwraps_public_input_locator_before_gate_check(self) -> None:
        sys.path.insert(0, str(shared_runtime_parent()))
        sys.path.insert(0, str(PACKAGE / "runtime"))
        previous_common = sys.modules.pop("common", None)
        try:
            spec = importlib.util.spec_from_file_location(
                "finalize_invoke_test", PACKAGE / "runtime/invoke.py"
            )
            assert spec and spec.loader
            invoke = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(invoke)
        finally:
            sys.modules.pop("common", None)
            if previous_common is not None:
                sys.modules["common"] = previous_common
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            public = {"profile": "publication_ready"}
            output = {"exit_id": "blocked"}
            owner = {
                "route": {"typed_exit": "blocked", "output": output}
            }
            runtime = SimpleNamespace(
                repo_root=lambda path: root,
                finalization_public_input=lambda *_: (public, root / "input.json"),
                finalization_gate_input=mock.Mock(return_value=(owner, root / "gate.json")),
                check_finalization_gate_result=mock.Mock(return_value=(owner, {})),
                FINALIZATION_EXECUTOR_OUTPUT_MARKER={"marker": True},
                FINALIZE_TASK_SKILL_ID="guru-finalize-task",
                finalization_package_root=lambda *_: PACKAGE,
                finalization_interface=lambda *_: {},
                stage0_output_contract=lambda *_: ({}, {}),
                skill_json_schema_validation_errors=lambda *_: [],
            )
            with mock.patch.object(invoke, "_o", return_value=runtime):
                self.assertEqual(
                    invoke.run(
                        PACKAGE,
                        {"id": "invoke-guru-finalize-task"},
                        ["--input", "input.json", "--owner-result", "gate.json"],
                    ),
                    output,
                )
            runtime.finalization_gate_input.assert_called_once_with(
                root, public, "gate.json"
            )

    def test_private_owner_failure_preserves_fail_closed_diagnostics(self) -> None:
        sys.path.insert(0, str(shared_runtime_parent()))
        sys.path.insert(0, str(PACKAGE / "runtime"))
        spec = importlib.util.spec_from_file_location(
            "finalize_common_test", PACKAGE / "runtime/common.py"
        )
        assert spec and spec.loader
        common = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(common)

        class FakeOwner:
            class WorkflowError(RuntimeError):
                def __init__(self) -> None:
                    super().__init__("archive path is unsafe")
                    self.exit_code = 2
                    self.payload = {
                        "stage": "archive-path-preflight",
                        "component": "archive-root",
                    }

        def fail() -> dict:
            raise FakeOwner.WorkflowError()

        from runtime.io import CommandError

        with self.assertRaises(CommandError) as raised:
            common.call_owner(FakeOwner, fail)
        self.assertEqual(raised.exception.code, "finalization_stale")
        self.assertEqual(raised.exception.response_stream, "stderr")
        self.assertEqual(
            raised.exception.response,
            {
                "status": "error",
                "error": "archive path is unsafe",
                "stage": "archive-path-preflight",
                "component": "archive-root",
            },
        )

    def test_package_runtime_has_no_verifier_consumer_artifact_or_monolith(self) -> None:
        runtime_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((PACKAGE / "runtime").glob("*.py"))
        )
        for retired in ("guru_team_trellis.py", "verification_required", "not_required", "finalization_verification", "extension_verification", "marketplace-verification"):
            self.assertNotIn(retired, runtime_text)
        commands = load("commands.json")
        interface = load("interface.json")
        self.assertEqual(
            {(item["validator_id"], item["id"]) for item in commands["commands"]},
            {(item["id"], item["runtime_command"]) for item in interface["validators"]},
        )
        for validator in interface["validators"]:
            self.assertIn("runtime/launch.sh", (PACKAGE / validator["command"]).read_text(encoding="utf-8"))

    def test_current_contract_has_no_verifier_edge_or_reentry(self) -> None:
        interface = load("interface.json")
        contracts = interface["public_contracts"]
        self.assertEqual(
            contracts["input"]["aggregate_schema"],
            {
                "schema_id": "guru-finalize-task-input-aggregate-6.0",
                "path": "schemas/public-input-6.0.schema.json",
            },
        )
        self.assertEqual(
            [item["id"] for item in contracts["input"]["profiles"]],
            ["publication_ready", "same_plan_resume", "reprepare_preview", "standalone_finalization"],
        )
        self.assertEqual(
            [item["exit_id"] for item in contracts["outputs"]],
            ["base_reconciliation_required", "publication_review_stale", "resume_finalization", "reprepare_required", "ready_for_merge", "blocked"],
        )
        serialized = json.dumps(contracts, sort_keys=True)
        for retired in (
            "verification_required",
            "verification_verified",
            "standalone_verification_not_required",
            "guru-verify-extension-installation",
        ):
            self.assertNotIn(retired, serialized)

    def test_current_gate_and_transaction_remove_verify(self) -> None:
        gate = load("schemas/task-finalization-gate-5.0.schema.json")
        current_gate_alias = load("schemas/task-finalization-gate.schema.json")
        current_review_alias = load("schemas/semantic-review-input.schema.json")
        transaction = load("schemas/finalization-transaction.schema.json")
        self.assertEqual(gate["properties"]["schema_version"]["const"], "5.0")
        self.assertEqual(current_gate_alias["$id"], gate["$id"])
        self.assertEqual(current_gate_alias["properties"]["schema_version"], gate["properties"]["schema_version"])
        explicit_review = load("schemas/semantic-review-input-3.0.schema.json")
        self.assertEqual(current_review_alias["$id"], explicit_review["$id"])
        self.assertEqual(current_review_alias["properties"]["schema_version"], explicit_review["properties"]["schema_version"])
        exits = gate["properties"]["route"]["properties"]["typed_exit"]["enum"]
        self.assertNotIn("verification_required", exits)
        self.assertNotIn("verification_required", current_review_alias["properties"]["route"]["properties"]["typed_exit"]["enum"])
        self.assertIn("base_reconciliation_required", exits)
        self.assertEqual(transaction["properties"]["schema_version"]["const"], "3.0")
        self.assertEqual(
            transaction["properties"]["mode"]["enum"],
            ["ordinary_publication", "existing_pr_recovery"],
        )
        self.assertIn("bind_pr", transaction["properties"]["next_transition"]["enum"])
        self.assertNotIn("bind_draft", transaction["properties"]["next_transition"]["enum"])
        self.assertNotIn("verify", transaction["properties"]["next_transition"]["enum"])
        self.assertNotIn("verification_ref", transaction["properties"])
        self.assertEqual(
            load("schemas/finalization-transaction-2.0.schema.json")["$id"],
            "guru-finalization-transaction-2.0",
        )

    def test_existing_pr_recovery_classifies_strict_ancestor_and_scope(self) -> None:
        plan = {
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": "feat/208",
                "base_branch": "main",
                "branch_review_commit": "b" * 40,
                "publication_head": "b" * 40,
            },
            "review": {"close_issues_reviewed": [208]},
            "publish": {"title": "当前标题", "body": "## 变更摘要\n\nCloses #208"},
        }
        pr = {
            "number": 59,
            "url": "https://github.com/castbox/guru-trellis/pull/59",
            "headRefOid": "a" * 40,
            "isDraft": False,
            "title": "旧标题",
            "body": "旧内容\n\nCloses #208",
        }
        with mock.patch.object(GTT, "is_ancestor", return_value=True) as ancestor:
            facts = GTT.classify_existing_pr_recovery(
                Path("/repo"), plan, pr, "a" * 40
            )
        self.assertEqual(facts["mode"], "existing_pr_recovery")
        self.assertEqual(facts["ancestry"], "strict_ancestor")
        self.assertTrue(facts["push_required"])
        self.assertEqual(facts["ready_action"], "preserve_ready")
        self.assertTrue(facts["metadata_update_required"])
        ancestor.assert_called_once_with(Path("/repo"), "a" * 40, "b" * 40)

    def test_existing_pr_recovery_uses_real_git_ancestry(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            GTT.run_stdout(["git", "init", "-q"], cwd=root)
            GTT.run_stdout(["git", "config", "user.name", "Guru Test"], cwd=root)
            GTT.run_stdout(["git", "config", "user.email", "guru@example.invalid"], cwd=root)
            marker = root / "marker.txt"
            marker.write_text("old\n", encoding="utf-8")
            GTT.run_stdout(["git", "add", "marker.txt"], cwd=root)
            GTT.run_stdout(["git", "commit", "-q", "-m", "old pr head"], cwd=root)
            old_head = GTT.current_head(root)
            marker.write_text("new\n", encoding="utf-8")
            GTT.run_stdout(["git", "commit", "-q", "-am", "publication head"], cwd=root)
            publication_head = GTT.current_head(root)
            plan = {
                "git": {
                    "repo": "castbox/guru-trellis",
                    "remote": "origin",
                    "head_branch": "feat/208",
                    "base_branch": "main",
                    "branch_review_commit": publication_head,
                    "publication_head": publication_head,
                },
                "review": {"close_issues_reviewed": [208]},
                "publish": {"title": "current", "body": "Closes #208"},
            }
            pr = {
                "number": 59,
                "url": "https://github.com/castbox/guru-trellis/pull/59",
                "headRefOid": old_head,
                "isDraft": False,
                "title": "old",
                "body": "Closes #208",
            }
            facts = GTT.classify_existing_pr_recovery(root, plan, pr, old_head)
            self.assertEqual(facts["ancestry"], "strict_ancestor")
            self.assertTrue(facts["push_required"])

            GTT.run_stdout(["git", "checkout", "-q", old_head], cwd=root)
            marker.write_text("sibling\n", encoding="utf-8")
            GTT.run_stdout(["git", "commit", "-q", "-am", "force pushed sibling"], cwd=root)
            sibling_head = GTT.current_head(root)
            pr["headRefOid"] = sibling_head
            with self.assertRaises(GTT.WorkflowError) as raised:
                GTT.classify_existing_pr_recovery(root, plan, pr, sibling_head)
            self.assertEqual(
                raised.exception.payload["reason_code"],
                "existing_pr_head_not_ancestor",
            )

            unknown_head = "f" * 40
            pr["headRefOid"] = unknown_head
            with self.assertRaises(GTT.WorkflowError) as unknown:
                GTT.classify_existing_pr_recovery(root, plan, pr, unknown_head)
            self.assertEqual(
                unknown.exception.payload["reason_code"],
                "existing_pr_head_not_ancestor",
            )

    def test_existing_draft_pr_recovery_runs_real_same_plan_topology_exactly_once(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            root = temporary_root / "repo"
            remote = temporary_root / "remote.git"
            root.mkdir()
            GTT.run_stdout(["git", "init", "-q"], cwd=root)
            GTT.run_stdout(["git", "init", "-q", "--bare", str(remote)])
            GTT.run_stdout(["git", "config", "user.name", "Guru Test"], cwd=root)
            GTT.run_stdout(
                ["git", "config", "user.email", "guru@example.invalid"], cwd=root
            )
            GTT.run_stdout(["git", "remote", "add", "origin", str(remote)], cwd=root)

            source_root = PACKAGE.parents[4]
            shutil.copytree(source_root / ".trellis/scripts", root / ".trellis/scripts")
            (root / ".trellis/config.yaml").write_text("{}\n", encoding="utf-8")
            (root / ".gitignore").write_text(".trellis/.runtime/\n", encoding="utf-8")
            GTT.run_stdout(["git", "branch", "-M", "feat/208"], cwd=root)

            old_task = root / ".trellis/tasks/archive/2026-08/old-ready-task"
            old_task.mkdir(parents=True)
            (old_task / "task.json").write_text(
                json.dumps({"slug": "old-ready-task", "status": "completed"}) + "\n",
                encoding="utf-8",
            )
            marker = root / "reviewed.txt"
            marker.write_text("old ready PR\n", encoding="utf-8")
            GTT.run_stdout(["git", "add", "."], cwd=root)
            GTT.run_stdout(["git", "commit", "-q", "-m", "old ready task"], cwd=root)
            old_head = GTT.current_head(root)
            GTT.run_stdout(
                ["git", "push", "-q", "origin", f"{old_head}:refs/heads/feat/208"],
                cwd=root,
            )

            active_locator = ".trellis/tasks/repair-ready-task"
            active_task = root / active_locator
            active_task.mkdir(parents=True)
            task = {
                "id": "repair-ready-task",
                "name": "repair-ready-task",
                "title": "修复 Finalizer 既有 PR 恢复",
                "status": "in_progress",
                "branch": "feat/208",
                "base_branch": "main",
            }
            issue = {
                "number": 208,
                "url": "https://github.com/castbox/guru-trellis/issues/208",
                "title": "Finalizer 安全接管既有 Ready PR",
                "reason": "The recovery fixture fully covers Issue #208.",
            }
            ledger = {
                "schema_version": "2.0",
                "primary_issue": issue,
                "close_issues": [copy.deepcopy(issue)],
                "related_issues": [],
                "followup_issues": [],
            }
            (active_task / "task.json").write_text(
                json.dumps(task, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            (active_task / "issue-scope-ledger.json").write_text(
                json.dumps(ledger, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            for name, content in (
                ("prd.md", "# 需求\n\n恢复既有 Ready PR 并完成真实归档。\n"),
                ("design.md", "# 设计\n\n复用唯一 PR 并执行官方 task archive。\n"),
                ("implement.md", "# 实施\n\n验证 preview、transaction、archive 与恢复。\n"),
            ):
                (active_task / name).write_text(content, encoding="utf-8")
            extension_manifest = root / ".trellis/guru-team/extension.json"
            extension_manifest.parent.mkdir(parents=True, exist_ok=True)
            extension_manifest.write_text(
                json.dumps(
                    {
                        "source": {
                            "ref": old_head,
                            "commit": old_head,
                            "tree_state": "clean",
                            "is_mutable_ref": False,
                        }
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            historical_plan = active_task / GTT.CLOSEOUT_PLAN_ARTIFACT
            historical_plan.write_text(
                json.dumps({"schema_version": "2.0", "historical": True}) + "\n",
                encoding="utf-8",
            )
            marker.write_text("reviewed repair\n", encoding="utf-8")
            GTT.run_stdout(["git", "add", "."], cwd=root)
            GTT.run_stdout(["git", "commit", "-q", "-m", "reviewed repair"], cwd=root)
            publication_head = GTT.current_head(root)
            self.assertTrue(GTT.is_ancestor(root, old_head, publication_head))
            self.assertNotEqual(old_head, publication_head)
            historical_plan.unlink()

            pr_body = (
                "## 变更摘要\n\n"
                "- 修复 Finalizer 既有 Ready PR 恢复链路。\n\n"
                "## Issue 关闭范围\n\n"
                "- Closes #208\n"
            )
            task_context = {
                "slug": "repair-ready-task",
                "title": task["title"],
                "base_branch": "main",
                "base_ref": old_head,
                "branch_name": "feat/208",
                "task_artifact_dir": active_locator,
            }
            changed_paths = GTT.run_stdout(
                ["git", "diff", "--name-only", f"{old_head}..{publication_head}"],
                cwd=root,
            ).splitlines()
            plan = GTT.build_closeout_plan(
                root,
                active_task,
                task_context,
                task,
                ledger,
                repo="castbox/guru-trellis",
                remote="origin",
                base_branch="main",
                head_branch="feat/208",
                branch_review_commit=publication_head,
                title=task["title"],
                body=pr_body,
                review_facts={"changed_paths": changed_paths},
                include_closeout_plan=False,
                allow_existing_summary=True,
            )
            archive_locator = plan["task"]["archive_locator"]
            self.assertNotIn(
                GTT.CLOSEOUT_PLAN_ARTIFACT,
                plan["projection"]["move_paths"],
            )
            self.assertEqual(
                plan["projection"]["retired_tracked_paths"],
                [GTT.CLOSEOUT_PLAN_ARTIFACT],
            )
            prepared = {
                "plan": plan,
                "plan_digest": plan["plan_digest"],
                "task": task,
                "task_context": task_context,
                "ledger": ledger,
                "body": pr_body,
                "month_supersession": None,
                "pre_pr_reprepare": None,
                "migration_normalization": None,
                "reviewed_content_head": publication_head,
                "publication_head": publication_head,
                "metadata_tail": None,
            }
            public_input = {
                "profile": "publication_ready",
                "mode": "workflow",
                "task_ref": active_locator,
                "branch_review_commit": publication_head,
                "pr_title": task["title"],
                "pr_body": pr_body,
            }
            pr = {
                "number": 59,
                "url": "https://github.com/castbox/guru-trellis/pull/59",
                "state": "OPEN",
                "headRefName": "feat/208",
                "baseRefName": "main",
                "headRefOid": old_head,
                "headRepository": {"nameWithOwner": "castbox/guru-trellis"},
                "headRepositoryOwner": {"login": "castbox"},
                "isCrossRepository": False,
                "isDraft": True,
                "title": "旧标题",
                "body": "旧正文\n\nCloses #208",
            }
            mutations = {
                "content_push": 0,
                "metadata_edit": 0,
                "pr_create": 0,
                "archive": 0,
                "archive_push": 0,
                "ready": 0,
            }
            archive_attempts = 0
            original_run = GTT.run
            original_run_stdout = GTT.run_stdout
            original_publication_owner_result = GTT.finalization_publication_owner_result

            input_locator = ".trellis/.runtime/guru-team/issue-251/public-input.json"
            input_path = root / input_locator
            input_path.parent.mkdir(parents=True)

            def write_public_input(payload):
                input_path.write_text(
                    json.dumps(payload, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )

            write_public_input(public_input)

            def remote_head(*_args, **_kwargs):
                output = original_run_stdout(
                    ["git", "ls-remote", "origin", "refs/heads/feat/208"], cwd=root
                )
                return output.split()[0] if output else ""

            def resolve_pr(*_args, **_kwargs):
                return copy.deepcopy(pr)

            def recording_run_stdout(command, **kwargs):
                result = original_run_stdout(command, **kwargs)
                if command[:3] == ["git", "push", "-u"]:
                    mutations["content_push"] += 1
                    pr["headRefOid"] = remote_head()
                elif command[:3] == ["git", "push", "origin"]:
                    mutations["archive_push"] += 1
                    pr["headRefOid"] = remote_head()
                return result

            def interrupt_first_archive(command, **kwargs):
                nonlocal archive_attempts
                if command[:3] == [sys.executable, "./.trellis/scripts/task.py", "archive"]:
                    archive_attempts += 1
                    if archive_attempts == 1:
                        return SimpleNamespace(
                            returncode=1,
                            stdout="",
                            stderr="simulated interruption before archive mutation",
                        )
                result = original_run(command, **kwargs)
                if command[:3] == [sys.executable, "./.trellis/scripts/task.py", "archive"]:
                    mutations["archive"] += 1
                return result

            def edit_pr(_root, _repo, number, title, body):
                self.assertEqual(number, pr["number"])
                mutations["metadata_edit"] += 1
                pr["title"] = title
                pr["body"] = body

            def create_pr(*_args, **_kwargs):
                mutations["pr_create"] += 1
                raise AssertionError("existing PR recovery must not create a PR")

            def ready_pr(*_args, **_kwargs):
                mutations["ready"] += 1
                self.assertTrue(pr["isDraft"])
                pr["isDraft"] = False

            def publication_owner(current_root, current_task_dir, current_input, verification=None):
                if current_input.get("profile") == "publication_ready":
                    return {
                        "status": "ok",
                        "owner_status": "current",
                        "typed_exit": "ready",
                        "task_ref": active_locator,
                        "branch_review_commit": publication_head,
                    }
                return original_publication_owner_result(
                    current_root,
                    current_task_dir,
                    current_input,
                    verification,
                )

            def pre_draft_state(*_args, **_kwargs):
                return GTT.resolve_closeout_pre_draft_state(
                    root,
                    active_task,
                    plan,
                    ledger,
                    require_plan_artifact=False,
                )

            gate = {
                "route": {
                    "typed_exit": "ready_for_merge",
                    "output": copy.deepcopy(GTT.FINALIZATION_EXECUTOR_OUTPUT_MARKER),
                }
            }
            args = SimpleNamespace(root=str(root), input=input_locator, gate="gate.json")
            no_op = mock.Mock()
            patches = (
                mock.patch.object(GTT, "finalization_gate_input", return_value=(gate, root / "gate.json")),
                mock.patch.object(
                    GTT,
                    "check_finalization_gate_result",
                    side_effect=lambda current_root, current_args, current_input, *_args, **_kwargs: (
                        gate,
                        GTT.finalization_preview_context(
                            current_root,
                            current_args,
                            current_input,
                        ),
                    ),
                ),
                mock.patch.object(GTT, "validate_finish_work_invocation", no_op),
                mock.patch.object(GTT, "load_config", return_value={}),
                mock.patch.object(GTT, "load_task_runtime_identity", return_value=task_context),
                mock.patch.object(GTT, "assert_workspace_boundary", no_op),
                mock.patch.object(GTT, "prepare_closeout", return_value=prepared),
                mock.patch.object(
                    GTT,
                    "finalization_publication_owner_result",
                    side_effect=publication_owner,
                ),
                mock.patch.object(GTT, "require_gh_auth", no_op),
                mock.patch.object(
                    GTT,
                    "validate_github_remote_repository",
                    return_value="castbox/guru-trellis",
                ),
                mock.patch.object(GTT, "resolve_closeout_pull_request", side_effect=resolve_pr),
                mock.patch.object(GTT, "closeout_remote_branch_head", side_effect=remote_head),
                mock.patch.object(GTT, "run", side_effect=interrupt_first_archive),
                mock.patch.object(GTT, "run_stdout", side_effect=recording_run_stdout),
                mock.patch.object(GTT, "update_pull_request_metadata", side_effect=edit_pr),
                mock.patch.object(GTT, "create_pull_request", side_effect=create_pr),
                mock.patch.object(GTT, "run_gh_command", side_effect=ready_pr),
                mock.patch.object(GTT, "validate_publish_identity_and_remote_head", no_op),
                mock.patch.object(GTT, "finalization_live_open_close_issues", return_value=[]),
                mock.patch.object(GTT, "finalization_package_root", return_value=PACKAGE),
            )
            with ExitStack() as stack:
                for patcher in patches:
                    stack.enter_context(patcher)
                preview = GTT.cmd_preview_finalization(args)
                self.assertFalse(preview["side_effects"])
                self.assertEqual(preview["publication_mode"], "existing_pr_recovery")
                self.assertEqual(preview["existing_pr_recovery"]["ancestry"], "strict_ancestor")
                self.assertEqual(preview["existing_pr_recovery"]["initial_state"], "draft")
                self.assertEqual(
                    preview["expected_actions"],
                    [
                        "bind_existing_pr_transaction",
                        "push_exact_publication_head",
                        "converge_pr_metadata",
                        "archive",
                        "push_archive",
                        "mark_ready",
                        "verify_three_way_head",
                    ],
                )
                self.assertEqual(set(mutations.values()), {0})

                with self.assertRaisesRegex(
                    GTT.WorkflowError, "task.py archive move failed"
                ):
                    GTT.cmd_execute_finalization_transition(args)
                transaction = GTT.finalization_read_transaction(root, active_task)
                self.assertEqual(transaction["mode"], "existing_pr_recovery")
                self.assertEqual(transaction["next_transition"], "archive")
                self.assertEqual(transaction["adopted_pr"]["pre_push_remote_head"], old_head)
                predecessor_transaction = copy.deepcopy(transaction)
                predecessor_transaction["plan_digest"] = (
                    GTT.finalization_retired_projection_predecessor_digest(plan)
                )
                GTT.finalization_write_transaction(
                    root,
                    active_task,
                    predecessor_transaction,
                )
                write_public_input(
                    {
                        "profile": "same_plan_resume",
                        "mode": "workflow",
                        "task_ref": active_locator,
                        "plan_ref": f"finalization:{plan['plan_digest']}",
                    }
                )
                self.assertEqual(
                    mutations,
                    {
                        "content_push": 1,
                        "metadata_edit": 1,
                        "pr_create": 0,
                        "archive": 0,
                        "archive_push": 0,
                        "ready": 0,
                    },
                )

                mutation_snapshot = copy.deepcopy(mutations)
                tree = original_run_stdout(["git", "rev-parse", f"{old_head}^{{tree}}"], cwd=root)
                sibling = original_run_stdout(
                    ["git", "commit-tree", tree, "-p", old_head, "-m", "force-push sibling"],
                    cwd=root,
                )
                original_run_stdout(
                    ["git", "push", "-q", "--force", "origin", f"{sibling}:refs/heads/feat/208"],
                    cwd=root,
                )
                pr["headRefOid"] = sibling
                with self.assertRaises(GTT.WorkflowError) as force_push_error:
                    GTT.cmd_preview_finalization(args)
                self.assertEqual(
                    force_push_error.exception.payload["reason_code"],
                    "finalizer_remote_head_drift",
                )
                self.assertEqual(mutations, mutation_snapshot)
                original_run_stdout(
                    ["git", "push", "-q", "--force", "origin", f"{publication_head}:refs/heads/feat/208"],
                    cwd=root,
                )
                pr["headRefOid"] = publication_head

                current_body = pr["body"]
                pr["body"] = "drifted scope\n\nCloses #207"
                with self.assertRaises(GTT.WorkflowError) as scope_error:
                    GTT.cmd_preview_finalization(args)
                self.assertEqual(
                    scope_error.exception.payload["reason_code"],
                    "existing_pr_scope_drift",
                )
                self.assertEqual(mutations, mutation_snapshot)
                pr["body"] = current_body

                reentry_preview = GTT.cmd_preview_finalization(args)
                self.assertFalse(reentry_preview["existing_pr_recovery"]["push_required"])
                self.assertFalse(
                    reentry_preview["existing_pr_recovery"]["metadata_update_required"]
                )
                completed = GTT.cmd_execute_finalization_transition(args)
                self.assertEqual(completed["stage"], "ready")
                self.assertEqual(completed["typed_exit"], "ready_for_merge")
                transaction = GTT.finalization_read_transaction(
                    root, root / archive_locator
                )
                self.assertEqual(transaction["mode"], "existing_pr_recovery")
                self.assertEqual(transaction["adopted_pr"]["pre_push_remote_head"], old_head)
                self.assertEqual(transaction["next_transition"], "mark_ready")
                archive_head = GTT.current_head(root)
                self.assertEqual(remote_head(), archive_head)
                self.assertEqual(pr["headRefOid"], archive_head)
                self.assertTrue((root / archive_locator).is_dir())
                self.assertFalse((root / active_locator).exists())
                self.assertTrue(old_task.is_dir())
                summary = json.loads(
                    (root / archive_locator / GTT.FINISH_SUMMARY_ARTIFACT).read_text(
                        encoding="utf-8"
                    )
                )
                archived_task = json.loads(
                    (root / archive_locator / "task.json").read_text(encoding="utf-8")
                )
                self.assertEqual(summary["github"]["pr_url"], pr["url"])
                self.assertEqual(summary["index"]["search_terms"]["pr_refs"], ["PR #59"])
                self.assertEqual(archived_task["status"], "completed")
                self.assertIn("completedAt", archived_task)
                self.assertEqual(completed["archive_commit"]["parent"], publication_head)
                self.assertIn(
                    f"{active_locator}/{GTT.CLOSEOUT_PLAN_ARTIFACT}",
                    completed["archive_commit"]["paths"],
                )
                self.assertFalse(
                    (root / archive_locator / GTT.CLOSEOUT_PLAN_ARTIFACT).exists()
                )
                self.assertEqual(archive_attempts, 2)
                self.assertEqual(
                    mutations,
                    {
                        "content_push": 1,
                        "metadata_edit": 1,
                        "pr_create": 0,
                        "archive": 1,
                        "archive_push": 1,
                        "ready": 1,
                    },
                )

                terminal_snapshot = copy.deepcopy(mutations)
                terminal = GTT.cmd_execute_finalization_transition(args)
                self.assertEqual(terminal["stage"], "ready_recovered")
                self.assertEqual(terminal["output"], completed["output"])
                self.assertEqual(mutations, terminal_snapshot)
                self.assertTrue(terminal["retired_owner_state"])
                self.assertIsNone(
                    GTT.finalization_find_transaction_by_task_ref(root, active_locator)
                )

    def test_post_bind_recovery_precedes_pre_pr_provenance_inference(self) -> None:
        plan = {
            "plan_digest": "d" * 64,
            "task": {"active_locator": ".trellis/tasks/251"},
            "git": {
                "repo": "castbox/business-repo",
                "base_branch": "main",
                "head_branch": "fix/251",
                "branch_review_commit": "b" * 40,
                "publication_head": "b" * 40,
            },
            "publish": {"title": "current", "body": "Closes #251"},
            "review": {"close_issues_reviewed": [251]},
        }
        pr = {
            "number": 59,
            "url": "https://github.com/castbox/business-repo/pull/59",
        }
        transaction = GTT.finalization_transaction_from_plan(
            plan,
            next_transition="archive",
            pr=pr,
            mode="existing_pr_recovery",
            adopted_pr={
                **pr,
                "initial_is_draft": True,
                "pre_push_remote_head": "a" * 40,
            },
        )
        with mock.patch.object(
            GTT,
            "finalizer_pre_pr_provenance_tail_required",
            side_effect=AssertionError("post-bind recovery must not inspect provenance"),
        ) as provenance:
            self.assertFalse(
                GTT.finalizer_pre_pr_provenance_tail_applies(
                    Path("/repo"),
                    plan,
                    transaction,
                )
            )
        provenance.assert_not_called()

        drifted = copy.deepcopy(transaction)
        drifted["publication"]["title"] = "drifted"
        with self.assertRaises(GTT.WorkflowError):
            GTT.finalizer_pre_pr_provenance_tail_applies(
                Path("/repo"),
                plan,
                drifted,
            )

        retired_plan = copy.deepcopy(plan)
        retired_plan["projection"] = {
            "move_paths": ["task.json"],
            "tracked_move_paths": ["task.json"],
            "retired_tracked_paths": [GTT.CLOSEOUT_PLAN_ARTIFACT]
        }
        predecessor = copy.deepcopy(transaction)
        predecessor["plan_digest"] = (
            GTT.finalization_retired_projection_predecessor_digest(retired_plan)
        )
        rebound = GTT.finalization_rebind_retired_projection_transaction(
            predecessor,
            retired_plan,
        )
        self.assertEqual(rebound["plan_digest"], plan["plan_digest"])
        self.assertEqual(rebound["next_transition"], "archive")
        self.assertEqual(rebound["pr"], transaction["pr"])
        self.assertEqual(rebound["adopted_pr"], transaction["adopted_pr"])

        drifted_digest = copy.deepcopy(predecessor)
        drifted_digest["plan_digest"] = "e" * 64
        with self.assertRaisesRegex(
            GTT.WorkflowError,
            "exact retired-plan predecessor digest",
        ):
            GTT.finalization_rebind_retired_projection_transaction(
                drifted_digest,
                retired_plan,
            )

        predecessor["close_issues"] = [250]
        with self.assertRaises(GTT.WorkflowError):
            GTT.finalization_rebind_retired_projection_transaction(
                predecessor,
                retired_plan,
            )

    def test_existing_pr_resolver_rejects_ambiguous_fork_and_identity_matrix(self) -> None:
        def candidate(number: int = 59) -> dict:
            return {
                "number": number,
                "url": f"https://github.com/castbox/guru-trellis/pull/{number}",
                "title": "current",
                "body": "Closes #208",
                "headRefName": "feat/208",
                "baseRefName": "main",
                "headRefOid": "a" * 40,
                "isDraft": False,
                "headRepository": {"nameWithOwner": "castbox/guru-trellis"},
                "headRepositoryOwner": {"login": "castbox"},
                "isCrossRepository": False,
            }

        cases = {
            "multiple_open_prs": (
                [candidate(), candidate(60)],
                "zero or one exact open pull request",
            ),
            "fork": (
                [{
                    **candidate(),
                    "headRepository": {"nameWithOwner": "contributor/guru-trellis"},
                    "headRepositoryOwner": {"login": "contributor"},
                    "isCrossRepository": True,
                }],
                "cross-repository pull request candidates",
            ),
            "head_mismatch": (
                [{**candidate(), "headRefName": "feat/other"}],
                "repo/head/base identity is invalid",
            ),
            "base_mismatch": (
                [{**candidate(), "baseRefName": "release"}],
                "repo/head/base identity is invalid",
            ),
            "repository_fields_mismatch": (
                [{
                    **candidate(),
                    "headRepository": {"nameWithOwner": "other/guru-trellis"},
                }],
                "head repository fields are inconsistent",
            ),
        }
        for name, (values, message) in cases.items():
            with self.subTest(name=name), mock.patch.object(
                GTT,
                "validate_github_remote_repository",
                return_value="castbox/guru-trellis",
            ), mock.patch.object(GTT, "gh_json", return_value=values) as gh:
                with self.assertRaisesRegex(GTT.WorkflowError, message):
                    GTT.resolve_closeout_pull_request(
                        Path("/repo"),
                        "castbox/guru-trellis",
                        "feat/208",
                        "main",
                    )
                gh.assert_called_once()

    def test_stale_publication_blocks_before_recovery_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            task_dir = root / ".trellis/tasks/repair-ready-task"
            task_dir.mkdir(parents=True)
            (task_dir / "task.json").write_text(
                json.dumps({"status": "completed"}) + "\n",
                encoding="utf-8",
            )
            result = GTT.finalization_publication_owner_result(
                root,
                task_dir,
                {
                    "profile": "publication_ready",
                    "task_ref": ".trellis/tasks/repair-ready-task",
                    "branch_review_commit": "b" * 40,
                },
            )
        self.assertEqual(
            result,
            {
                "owner_status": "stale",
                "branch_review_commit": "b" * 40,
                "stale_reason": "publication_review_stale",
            },
        )

    def test_planless_publication_stale_runs_preview_record_check_and_public_invoke(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            GTT.run_stdout(["git", "init", "-q", "-b", "main"], cwd=root)
            GTT.run_stdout(["git", "config", "user.name", "Guru Test"], cwd=root)
            GTT.run_stdout(
                ["git", "config", "user.email", "guru@example.invalid"], cwd=root
            )
            marker = root / "reviewed.txt"
            marker.write_text("base\n", encoding="utf-8")
            GTT.run_stdout(["git", "add", "reviewed.txt"], cwd=root)
            GTT.run_stdout(["git", "commit", "-q", "-m", "base"], cwd=root)
            base_head = GTT.current_head(root)
            GTT.run_stdout(
                ["git", "update-ref", "refs/remotes/origin/main", base_head],
                cwd=root,
            )
            GTT.run_stdout(
                ["git", "switch", "-q", "-c", "fix/253-planless-stale"],
                cwd=root,
            )
            task_ref = ".trellis/tasks/08-17-253-planless-stale"
            task_dir = root / task_ref
            task_dir.mkdir(parents=True)
            (task_dir / "task.json").write_text(
                json.dumps(
                    {
                        "id": "253-planless-stale",
                        "name": "253-planless-stale",
                        "status": "in_progress",
                        "branch": "fix/253-planless-stale",
                        "base_branch": "main",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            marker.write_text("reviewed\n", encoding="utf-8")
            GTT.run_stdout(["git", "add", "."], cwd=root)
            GTT.run_stdout(["git", "commit", "-q", "-m", "reviewed"], cwd=root)
            reviewed_commit = GTT.current_head(root)
            marker.write_text("advanced after publication review\n", encoding="utf-8")
            GTT.run_stdout(["git", "commit", "-q", "-am", "advance head"], cwd=root)
            self.assertNotEqual(GTT.current_head(root), reviewed_commit)

            fixture_dir = root / ".trellis/.runtime/guru-team/issue-253"
            fixture_dir.mkdir(parents=True)
            public_input = {
                "profile": "publication_ready",
                "mode": "workflow",
                "task_ref": task_ref,
                "branch_review_commit": reviewed_commit,
                "pr_title": "修复 planless stale route",
                "pr_body": "## 变更摘要\n\n- 测试。",
            }
            public_path = fixture_dir / "public-input.json"
            public_path.write_text(
                json.dumps(public_input, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            stale_output = {
                "exit_id": "publication_review_stale",
                "task_ref": task_ref,
                "branch_review_commit": reviewed_commit,
                "stale_reason": "publication_review_stale",
            }
            review_path = fixture_dir / "semantic-review.json"
            review_path.write_text(
                json.dumps(
                    {
                        "schema_version": "3.0",
                        "skill_id": "guru-finalize-task",
                        "review": {
                            "status": "reroute",
                            "summary": "Publication owner facts are stale before plan creation.",
                        },
                        "route": {
                            "typed_exit": "publication_review_stale",
                            "consumer": {
                                "kind": "skill",
                                "id": "guru-review-task-publication",
                            },
                            "output": stale_output,
                        },
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            input_locator = public_path.relative_to(root).as_posix()
            review_locator = review_path.relative_to(root).as_posix()
            preview_args = SimpleNamespace(root=str(root), input=input_locator)
            record_args = SimpleNamespace(
                root=str(root),
                input=input_locator,
                review_input=review_locator,
                dry_run=False,
            )
            task_context = {"base_head_sha": base_head, "base_branch": "main"}
            with (
                mock.patch.object(GTT, "finalization_package_root", return_value=PACKAGE),
                mock.patch.object(GTT, "load_config", return_value={}),
                mock.patch.object(
                    GTT, "load_task_runtime_identity", return_value=task_context
                ),
            ):
                preview = GTT.cmd_preview_finalization(preview_args)
                self.assertFalse(preview["side_effects"])
                self.assertEqual(preview["closeout_plan"], None)
                self.assertEqual(preview["expected_actions"], [])
                self.assertEqual(
                    preview["transaction_state"], "publication_review_stale"
                )
                self.assertEqual(preview["publication_status"], "stale")
                self.assertEqual(
                    preview["publication_stale_reason"], "publication_review_stale"
                )
                self.assertEqual(preview["branch_review_commit"], reviewed_commit)

                recorded = GTT.cmd_record_finalization_gate(record_args)
                gate_path = Path(recorded["artifact_path"])
                gate = json.loads(gate_path.read_text(encoding="utf-8"))
                self.assertEqual(
                    gate["identity"]["branch_review_commit"], reviewed_commit
                )
                gate_locator = gate_path.resolve().relative_to(root.resolve()).as_posix()
                checked = GTT.cmd_check_finalization_gate(
                    SimpleNamespace(
                        root=str(root), input=input_locator, gate=gate_locator
                    )
                )
                self.assertEqual(checked["typed_exit"], "publication_review_stale")
                self.assertEqual(
                    checked["transaction_state"], "publication_review_stale"
                )

                sys.path.insert(0, str(shared_runtime_parent()))
                sys.path.insert(0, str(PACKAGE / "runtime"))
                previous_common = sys.modules.pop("common", None)
                try:
                    spec = importlib.util.spec_from_file_location(
                        "finalize_planless_stale_invoke_test",
                        PACKAGE / "runtime/invoke.py",
                    )
                    assert spec and spec.loader
                    invoke = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(invoke)
                finally:
                    sys.modules.pop("common", None)
                    if previous_common is not None:
                        sys.modules["common"] = previous_common
                with mock.patch.object(invoke, "_o", return_value=GTT):
                    public_output = invoke.run(
                        PACKAGE,
                        {"id": "invoke-guru-finalize-task"},
                        [
                            "--root",
                            str(root),
                            "--input",
                            input_locator,
                            "--owner-result",
                            gate_locator,
                        ],
                    )
                self.assertEqual(public_output, stale_output)
                self.assertFalse((task_dir / GTT.CLOSEOUT_PLAN_ARTIFACT).exists())
                self.assertIsNone(GTT.finalization_read_transaction(root, task_dir))

    def test_publication_stale_route_rejects_mismatched_owner_facts_and_current_status(self) -> None:
        task_ref = ".trellis/tasks/08-17-253-planless-stale"
        owner_commit = "a" * 40
        context = {
            "plan": None,
            "plan_ref": None,
            "transaction_state": "publication_review_stale",
            "publication_status": "stale",
            "publication_stale_reason": "publication_review_stale",
            "publication_branch_review_commit": owner_commit,
        }
        route = {
            "typed_exit": "publication_review_stale",
            "consumer": copy.deepcopy(
                GTT.FINALIZATION_CONSUMERS["publication_review_stale"]
            ),
            "output": {
                "exit_id": "publication_review_stale",
                "task_ref": task_ref,
                "branch_review_commit": owner_commit,
                "stale_reason": "publication_review_stale",
            },
        }
        with mock.patch.object(GTT, "finalization_package_root", return_value=PACKAGE):
            GTT.finalization_validate_route(
                Path("/repo"), {"task_ref": task_ref}, context, route
            )
            cases = {
                "wrong_task": {"task_ref": ".trellis/tasks/other"},
                "wrong_owner_commit": {"branch_review_commit": "b" * 40},
                "wrong_reason": {"stale_reason": "publication_review_missing"},
            }
            for name, changes in cases.items():
                with self.subTest(case=name):
                    invalid = copy.deepcopy(route)
                    invalid["output"].update(changes)
                    with self.assertRaises(GTT.WorkflowError):
                        GTT.finalization_validate_route(
                            Path("/repo"),
                            {"task_ref": task_ref},
                            context,
                            invalid,
                        )
            current = copy.deepcopy(context)
            current["publication_status"] = "current"
            with self.assertRaises(GTT.WorkflowError):
                GTT.finalization_validate_route(
                    Path("/repo"), {"task_ref": task_ref}, current, route
                )

    def test_plan_backed_reprepare_remains_bound_to_plan_commit(self) -> None:
        task_ref = ".trellis/tasks/08-17-253-plan-backed"
        plan_commit = "c" * 40
        publication_head = "d" * 40
        context = {
            "plan": {
                "git": {
                    "branch_review_commit": plan_commit,
                    "publication_head": publication_head,
                }
            },
            "plan_ref": "finalization:" + "e" * 64,
            "transaction_state": "reprepare_required",
            "publication_status": "current",
            "publication_stale_reason": None,
            "publication_branch_review_commit": "f" * 40,
            "reprepare_reason_code": GTT.FINALIZATION_REPREPARE_ARCHIVE_MONTH,
        }
        route = {
            "typed_exit": "reprepare_required",
            "consumer": copy.deepcopy(
                GTT.FINALIZATION_CONSUMERS["reprepare_required"]
            ),
            "output": {
                "exit_id": "reprepare_required",
                "task_ref": task_ref,
                "reason_code": GTT.FINALIZATION_REPREPARE_ARCHIVE_MONTH,
                "branch_review_commit": plan_commit,
                "publication_head": publication_head,
            },
        }
        with mock.patch.object(GTT, "finalization_package_root", return_value=PACKAGE):
            GTT.finalization_validate_route(
                Path("/repo"), {"task_ref": task_ref}, context, route
            )
            invalid = copy.deepcopy(route)
            invalid["output"]["branch_review_commit"] = context[
                "publication_branch_review_commit"
            ]
            with self.assertRaises(GTT.WorkflowError):
                GTT.finalization_validate_route(
                    Path("/repo"), {"task_ref": task_ref}, context, invalid
                )

    def test_archive_conflict_fails_before_finalizer_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive_locator = (
                f".trellis/tasks/archive/{GTT.current_archive_month()}/repair-ready-task"
            )
            (root / archive_locator).mkdir(parents=True)
            with self.assertRaises(GTT.WorkflowError) as raised:
                GTT.assert_closeout_archive_path_preflight(root, archive_locator)
        self.assertEqual(
            raised.exception.payload,
            {
                "stage": "archive-locator-preflight",
                "archive_locator": archive_locator,
            },
        )

    def test_unknown_transaction_state_fails_closed_on_read(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            task_dir = root / ".trellis/tasks/repair-ready-task"
            task_dir.mkdir(parents=True)
            plan = {
                "plan_digest": "d" * 64,
                "task": {"active_locator": ".trellis/tasks/repair-ready-task"},
                "git": {
                    "repo": "castbox/guru-trellis",
                    "base_branch": "main",
                    "head_branch": "feat/208",
                    "branch_review_commit": "b" * 40,
                    "publication_head": "b" * 40,
                },
                "publish": {"title": "current", "body": "Closes #208"},
                "review": {"close_issues_reviewed": [208]},
            }
            transaction = GTT.finalization_transaction_from_plan(
                plan,
                next_transition="bind_pr",
                pr={
                    "number": 59,
                    "url": "https://github.com/castbox/guru-trellis/pull/59",
                },
                mode="existing_pr_recovery",
                adopted_pr={
                    "number": 59,
                    "url": "https://github.com/castbox/guru-trellis/pull/59",
                    "initial_is_draft": False,
                    "pre_push_remote_head": "a" * 40,
                },
            )
            transaction["next_transition"] = "unknown"
            with mock.patch.object(GTT, "finalization_package_root", return_value=PACKAGE):
                path = GTT.finalization_transaction_path(root, task_dir)
                GTT.write_json(path, transaction)
                with self.assertRaisesRegex(
                    GTT.WorkflowError, "transaction is invalid"
                ) as raised:
                    GTT.finalization_read_transaction(root, task_dir)
        self.assertTrue(raised.exception.payload["errors"])

    def test_existing_pr_recovery_rejects_scope_and_remote_head_drift(self) -> None:
        plan = {
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": "feat/208",
                "base_branch": "main",
                "branch_review_commit": "b" * 40,
                "publication_head": "b" * 40,
            },
            "review": {"close_issues_reviewed": [208]},
            "publish": {"title": "当前标题", "body": "Closes #208"},
        }
        pr = {
            "number": 59,
            "url": "https://github.com/castbox/guru-trellis/pull/59",
            "headRefOid": "a" * 40,
            "isDraft": True,
            "title": "旧标题",
            "body": "Closes #207",
        }
        with self.assertRaises(GTT.WorkflowError) as remote_error:
            GTT.classify_existing_pr_recovery(Path("/repo"), plan, pr, "c" * 40)
        self.assertEqual(remote_error.exception.payload["reason_code"], "existing_pr_remote_head_mismatch")
        with (
            mock.patch.object(GTT, "is_ancestor", return_value=True),
            self.assertRaises(GTT.WorkflowError) as scope_error,
        ):
            GTT.classify_existing_pr_recovery(Path("/repo"), plan, pr, "a" * 40)
        self.assertEqual(scope_error.exception.payload["reason_code"], "existing_pr_scope_drift")

    def test_fresh_existing_pr_recovery_rejects_unbound_equal_head(self) -> None:
        head = "b" * 40
        plan = {
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": "feat/208",
                "base_branch": "main",
                "branch_review_commit": head,
                "publication_head": head,
            },
            "review": {"close_issues_reviewed": [208]},
            "publish": {"title": "current", "body": "Closes #208"},
        }
        pr = {
            "number": 59,
            "url": "https://github.com/castbox/guru-trellis/pull/59",
            "headRefOid": head,
            "isDraft": False,
            "title": "current",
            "body": "Closes #208",
        }
        with self.assertRaises(GTT.WorkflowError) as raised:
            GTT.classify_existing_pr_recovery(Path("/repo"), plan, pr, head)
        self.assertEqual(
            raised.exception.payload["reason_code"],
            "existing_pr_unbound_equal_head",
        )

    def test_reprepare_state_precedes_existing_pr_recovery(self) -> None:
        plan = {
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": "feat/208",
                "base_branch": "main",
            }
        }
        transaction = {"mode": "existing_pr_recovery"}
        with (
            mock.patch.object(GTT, "resolve_closeout_pull_request") as resolve_pr,
            mock.patch.object(GTT, "finalization_pre_mutation_remote_preflight") as preflight,
        ):
            state, recovery = GTT.finalization_existing_pr_recovery_context(
                Path("/repo"), plan, transaction, "reprepare_required"
            )
        self.assertEqual(state, "reprepare_required")
        self.assertIsNone(recovery)
        resolve_pr.assert_not_called()
        preflight.assert_not_called()

    def test_transaction_recovery_binding_survives_each_transition(self) -> None:
        plan = {
            "plan_digest": "d" * 64,
            "task": {"active_locator": ".trellis/tasks/208"},
            "git": {
                "repo": "castbox/guru-trellis",
                "base_branch": "main",
                "head_branch": "feat/208",
                "branch_review_commit": "b" * 40,
                "publication_head": "b" * 40,
            },
            "publish": {"title": "当前标题", "body": "Closes #208"},
            "review": {"close_issues_reviewed": [208]},
        }
        pr = {"number": 59, "url": "https://github.com/castbox/guru-trellis/pull/59"}
        adopted = {
            **pr,
            "initial_is_draft": False,
            "pre_push_remote_head": "a" * 40,
        }
        transaction = GTT.finalization_transaction_from_plan(
            plan,
            next_transition="push_content",
            pr=pr,
            pre_push_remote_head="a" * 40,
            mode="existing_pr_recovery",
            adopted_pr=adopted,
        )
        jsonschema.Draft202012Validator(
            load("schemas/finalization-transaction.schema.json")
        ).validate(transaction)
        advanced = GTT.finalization_advance_transaction(
            plan, transaction, next_transition="bind_pr"
        )
        self.assertEqual(advanced["mode"], "existing_pr_recovery")
        self.assertEqual(advanced["adopted_pr"], adopted)
        self.assertEqual(advanced["pr"], pr)
        self.assertNotIn("pre_push_remote_head", advanced)

    def test_transaction_schema_keeps_publication_modes_mutually_exclusive(self) -> None:
        schema = jsonschema.Draft202012Validator(
            load("schemas/finalization-transaction.schema.json")
        )
        plan = {
            "plan_digest": "d" * 64,
            "task": {"active_locator": ".trellis/tasks/208"},
            "git": {
                "repo": "castbox/guru-trellis",
                "base_branch": "main",
                "head_branch": "feat/208",
                "branch_review_commit": "b" * 40,
                "publication_head": "b" * 40,
            },
            "publish": {"title": "current", "body": "Closes #208"},
            "review": {"close_issues_reviewed": [208]},
        }
        ordinary = GTT.finalization_transaction_from_plan(
            plan, next_transition="push_content", pre_push_remote_head=""
        )
        recovery = GTT.finalization_transaction_from_plan(
            plan,
            next_transition="bind_pr",
            pr={"number": 59, "url": "https://github.com/castbox/guru-trellis/pull/59"},
            mode="existing_pr_recovery",
            adopted_pr={
                "number": 59,
                "url": "https://github.com/castbox/guru-trellis/pull/59",
                "initial_is_draft": False,
                "pre_push_remote_head": "a" * 40,
            },
        )
        schema.validate(ordinary)
        schema.validate(recovery)
        ordinary["adopted_pr"] = copy.deepcopy(recovery["adopted_pr"])
        recovery.pop("adopted_pr")
        self.assertFalse(schema.is_valid(ordinary))
        self.assertFalse(schema.is_valid(recovery))

    def test_ordinary_preflight_still_rejects_an_open_pr(self) -> None:
        plan = {
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": "feat/208",
                "base_branch": "main",
                "branch_review_commit": "b" * 40,
                "publication_head": "b" * 40,
            }
        }
        with (
            mock.patch.object(GTT, "resolve_closeout_pull_request", return_value={"number": 59}),
            mock.patch.object(GTT, "closeout_remote_branch_head", return_value="a" * 40),
            mock.patch.object(GTT, "is_ancestor", return_value=True),
            self.assertRaises(GTT.WorkflowError) as raised,
        ):
            GTT.finalization_pre_mutation_remote_preflight(Path("/repo"), plan, None)
        self.assertEqual(raised.exception.payload["reason_code"], "pre_finalizer_remote_state_exists")

    def test_ordinary_preflight_rejects_remote_left_by_terminal_pr(self) -> None:
        plan = {
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": "feat/208",
                "base_branch": "main",
                "branch_review_commit": "b" * 40,
                "publication_head": "b" * 40,
            }
        }
        with (
            mock.patch.object(GTT, "resolve_closeout_pull_request", return_value=None),
            mock.patch.object(GTT, "closeout_remote_branch_head", return_value="b" * 40),
            self.assertRaises(GTT.WorkflowError) as raised,
        ):
            GTT.finalization_pre_mutation_remote_preflight(Path("/repo"), plan, None)
        self.assertEqual(
            raised.exception.payload["reason_code"],
            "pre_finalizer_remote_state_exists",
        )

    def test_ordinary_preflight_rejects_terminal_exact_pr_before_push(self) -> None:
        plan = {
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": "feat/208",
                "base_branch": "main",
                "branch_review_commit": "b" * 40,
                "publication_head": "b" * 40,
            }
        }
        terminal = [{"number": 59, "url": "https://github.com/castbox/guru-trellis/pull/59", "state": "MERGED"}]
        with (
            mock.patch.object(GTT, "resolve_closeout_pull_request", return_value=None),
            mock.patch.object(GTT, "closeout_remote_branch_head", return_value="a" * 40),
            mock.patch.object(GTT, "is_ancestor", return_value=True),
            mock.patch.object(
                GTT, "resolve_closeout_terminal_pull_requests", return_value=terminal
            ),
            self.assertRaises(GTT.WorkflowError) as raised,
        ):
            GTT.finalization_pre_mutation_remote_preflight(Path("/repo"), plan, None)
        self.assertEqual(
            raised.exception.payload["reason_code"],
            "pre_finalizer_terminal_pr_exists",
        )
        self.assertEqual(raised.exception.payload["pull_requests"], terminal)

    def test_terminal_pr_discovery_binds_same_repository_and_state(self) -> None:
        values = [
            {
                "number": 59,
                "url": "https://github.com/castbox/guru-trellis/pull/59",
                "state": "CLOSED",
                "headRefName": "feat/208",
                "baseRefName": "main",
                "headRepository": {"nameWithOwner": "castbox/guru-trellis"},
                "headRepositoryOwner": {"login": "castbox"},
                "isCrossRepository": False,
            }
        ]
        with (
            mock.patch.object(
                GTT,
                "validate_github_remote_repository",
                return_value="castbox/guru-trellis",
            ),
            mock.patch.object(GTT, "gh_json", return_value=values) as gh,
        ):
            result = GTT.resolve_closeout_terminal_pull_requests(
                Path("/repo"),
                "castbox/guru-trellis",
                "feat/208",
                "main",
            )
        self.assertEqual(
            result,
            [{"number": 59, "url": values[0]["url"], "state": "CLOSED"}],
        )
        self.assertIn("closed", gh.call_args.args[0])

    def test_recovery_payload_drift_after_binding_fails_closed(self) -> None:
        plan = {
            "plan_digest": "d" * 64,
            "task": {"active_locator": ".trellis/tasks/208"},
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": "feat/208",
                "base_branch": "main",
                "branch_review_commit": "b" * 40,
                "publication_head": "b" * 40,
            },
            "publish": {"title": "current", "body": "Closes #208"},
            "review": {"close_issues_reviewed": [208]},
        }
        pr_identity = {
            "number": 59,
            "url": "https://github.com/castbox/guru-trellis/pull/59",
        }
        transaction = GTT.finalization_transaction_from_plan(
            plan,
            next_transition="archive",
            pr=pr_identity,
            mode="existing_pr_recovery",
            adopted_pr={
                **pr_identity,
                "initial_is_draft": False,
                "pre_push_remote_head": "a" * 40,
            },
        )
        live_pr = {
            **pr_identity,
            "headRefOid": "b" * 40,
            "isDraft": False,
            "title": "drifted",
            "body": "Closes #208",
        }
        with (
            mock.patch.object(GTT, "resolve_closeout_pull_request", return_value=live_pr),
            mock.patch.object(GTT, "closeout_remote_branch_head", return_value="b" * 40),
            mock.patch.object(GTT, "validate_closeout_remote_pull_request_binding"),
            self.assertRaises(GTT.WorkflowError) as raised,
        ):
            GTT.finalization_pre_mutation_remote_preflight(
                Path("/repo"), plan, transaction
            )
        self.assertIn("title differs", str(raised.exception))

    def test_ready_recovery_preserves_ready_pr_without_creation_or_transition(self) -> None:
        pr = {
            "number": 59,
            "url": "https://github.com/castbox/guru-trellis/pull/59",
            "headRefOid": "b" * 40,
            "isDraft": False,
            "title": "当前标题",
            "body": "Closes #208",
        }
        plan = {
            "git": {"repo": "castbox/guru-trellis", "remote": "origin", "head_branch": "feat/208", "base_branch": "main"},
            "publish": {"title": "当前标题", "body": "Closes #208"},
        }
        transaction = {
            "mode": "existing_pr_recovery",
            "pr": {"number": 59, "url": pr["url"]},
            "adopted_pr": {"number": 59, "url": pr["url"], "initial_is_draft": False, "pre_push_remote_head": "a" * 40},
        }
        with (
            mock.patch.object(GTT, "resolve_closeout_pull_request", return_value=pr),
            mock.patch.object(GTT, "current_head", return_value="b" * 40),
            mock.patch.object(GTT, "validate_closeout_remote_pull_request_binding"),
            mock.patch.object(GTT, "validate_closeout_pull_request_identity"),
            mock.patch.object(GTT, "closeout_task_dir_from_plan", return_value=Path("/repo/task")),
            mock.patch.object(GTT, "update_pull_request_metadata") as update,
            mock.patch.object(GTT, "ensure_closeout_draft_pr") as create,
        ):
            result = GTT.ensure_closeout_bound_pr(
                Path("/repo"), plan, "Closes #208", transaction
            )
        self.assertEqual(result, pr)
        update.assert_not_called()
        create.assert_not_called()

    def test_draft_recovery_converges_metadata_once_without_pr_creation(self) -> None:
        old_pr = {
            "number": 59,
            "url": "https://github.com/castbox/guru-trellis/pull/59",
            "headRefOid": "b" * 40,
            "isDraft": True,
            "title": "old",
            "body": "Closes #208",
        }
        current_pr = {**old_pr, "title": "current", "body": "Summary\n\nCloses #208"}
        plan = {
            "git": {"repo": "castbox/guru-trellis", "remote": "origin", "head_branch": "feat/208", "base_branch": "main"},
            "publish": {"title": "current", "body": "Summary\n\nCloses #208"},
        }
        transaction = {
            "mode": "existing_pr_recovery",
            "pr": {"number": 59, "url": old_pr["url"]},
            "adopted_pr": {"number": 59, "url": old_pr["url"], "initial_is_draft": True, "pre_push_remote_head": "a" * 40},
        }
        with (
            mock.patch.object(GTT, "resolve_closeout_pull_request", side_effect=[old_pr, current_pr, current_pr]),
            mock.patch.object(GTT, "current_head", return_value="b" * 40),
            mock.patch.object(GTT, "validate_closeout_remote_pull_request_binding"),
            mock.patch.object(GTT, "validate_closeout_pull_request_identity"),
            mock.patch.object(GTT, "closeout_task_dir_from_plan", return_value=Path("/repo/task")),
            mock.patch.object(GTT, "update_pull_request_metadata") as update,
            mock.patch.object(GTT, "ensure_closeout_draft_pr") as create,
        ):
            first = GTT.ensure_closeout_bound_pr(
                Path("/repo"), plan, plan["publish"]["body"], transaction
            )
            second = GTT.ensure_closeout_bound_pr(
                Path("/repo"), plan, plan["publish"]["body"], transaction
            )
        self.assertEqual(first, current_pr)
        self.assertEqual(second, current_pr)
        update.assert_called_once_with(
            Path("/repo"),
            "castbox/guru-trellis",
            59,
            "current",
            "Summary\n\nCloses #208",
        )
        create.assert_not_called()

    def test_archived_ready_recovery_preserves_ready_state(self) -> None:
        plan = {
            "plan_digest": "d" * 64,
            "git": {"repo": "castbox/guru-trellis", "remote": "origin", "head_branch": "feat/208", "base_branch": "main"},
        }
        pr = {
            "number": 59,
            "url": "https://github.com/castbox/guru-trellis/pull/59",
            "headRefOid": "c" * 40,
            "isDraft": False,
            "title": "current",
            "body": "Closes #208",
        }
        transaction = {
            "mode": "existing_pr_recovery",
            "adopted_pr": {"number": 59, "url": pr["url"], "initial_is_draft": False, "pre_push_remote_head": "b" * 40},
        }
        args = SimpleNamespace(expected_plan_digest="d" * 64, finalization_gate={})
        with (
            mock.patch.object(GTT, "require_gh_auth"),
            mock.patch.object(GTT, "current_head", return_value="c" * 40),
            mock.patch.object(GTT, "closeout_remote_branch_head", return_value="c" * 40),
            mock.patch.object(GTT, "resolve_closeout_pull_request", return_value=pr),
            mock.patch.object(GTT, "validate_closeout_remote_pull_request_identity") as validate,
            mock.patch.object(GTT, "ensure_closeout_pr_ready", return_value={"status": "ready", "pr": pr}) as ready,
        ):
            result = GTT.resume_archived_closeout(
                Path("/repo"),
                args,
                Path("/repo/archive"),
                committed_plan=plan,
                committed_archive={"commit": "c" * 40, "summary_pr": pr},
                finalization_transaction=transaction,
            )
        self.assertEqual(result["stage"], "ready")
        self.assertFalse(validate.call_args.kwargs["expected_draft"])
        ready.assert_called_once()

    def test_preexisting_summary_uses_adopted_ready_state(self) -> None:
        transaction = {
            "mode": "existing_pr_recovery",
            "adopted_pr": {"initial_is_draft": False},
        }
        self.assertFalse(
            GTT.finalization_expected_pr_draft_state(
                transaction,
                current_finalizer=True,
            )
        )

    def test_archive_month_reprepare_preserves_adopted_pr_transaction(self) -> None:
        plan = {
            "plan_digest": "e" * 64,
            "task": {"active_locator": ".trellis/tasks/208"},
            "git": {
                "repo": "castbox/guru-trellis",
                "base_branch": "main",
                "head_branch": "feat/208",
                "branch_review_commit": "b" * 40,
                "publication_head": "b" * 40,
            },
            "publish": {"title": "current", "body": "Closes #208"},
            "review": {"close_issues_reviewed": [208]},
        }
        previous = {
            "mode": "existing_pr_recovery",
            "pr": {
                "number": 59,
                "url": "https://github.com/castbox/guru-trellis/pull/59",
            },
            "adopted_pr": {
                "number": 59,
                "url": "https://github.com/castbox/guru-trellis/pull/59",
                "initial_is_draft": False,
                "pre_push_remote_head": "a" * 40,
            },
        }
        replacement = GTT.finalization_reprepared_transaction(
            plan,
            previous,
            pre_push_remote_head="a" * 40,
        )
        self.assertEqual(replacement["mode"], "existing_pr_recovery")
        self.assertEqual(replacement["pr"], previous["pr"])
        self.assertEqual(replacement["adopted_pr"], previous["adopted_pr"])
        self.assertEqual(replacement["next_transition"], "push_content")
        self.assertEqual(replacement["pre_push_remote_head"], "a" * 40)

    def test_content_push_uses_exact_publication_refspec(self) -> None:
        plan = {
            "plan_digest": "d" * 64,
            "git": {"remote": "origin", "head_branch": "feat/208", "branch_review_commit": "b" * 40, "publication_head": "b" * 40, "repo": "castbox/guru-trellis", "base_branch": "main"},
        }
        prepared = {"plan": plan, "task": {}}
        with (
            mock.patch.object(GTT, "validate_closeout_reviewed_content"),
            mock.patch.object(GTT, "current_head", return_value="b" * 40),
            mock.patch.object(GTT, "run_stdout") as run_stdout,
            mock.patch.object(GTT, "validate_publish_identity_and_remote_head"),
        ):
            GTT.execute_closeout_content_push(
                Path("/repo"), Path("/repo/task"), {}, prepared, persist_closeout_plan=False
            )
        self.assertEqual(
            run_stdout.call_args.args[0],
            ["git", "push", "-u", "origin", f"{'b' * 40}:refs/heads/feat/208"],
        )

    def test_current_schema_aliases_match_explicit_acceptance_domains(self) -> None:
        pairs = (
            (
                "schemas/semantic-review-input.schema.json",
                "schemas/semantic-review-input-3.0.schema.json",
                load("examples/semantic-review-input.json"),
            ),
            (
                "schemas/task-finalization-gate.schema.json",
                "schemas/task-finalization-gate-5.0.schema.json",
                load("examples/task-finalization-gate.json"),
            ),
        )
        for alias_path, explicit_path, positive in pairs:
            with self.subTest(alias=alias_path):
                alias_bytes = (PACKAGE / alias_path).read_bytes()
                explicit_bytes = (PACKAGE / explicit_path).read_bytes()
                self.assertEqual(alias_bytes, explicit_bytes)
                alias = jsonschema.Draft202012Validator(load(alias_path))
                explicit = jsonschema.Draft202012Validator(load(explicit_path))
                negative = json.loads(json.dumps(positive))
                negative["route"]["typed_exit"] = "verification_required"
                extra_property = json.loads(json.dumps(positive))
                extra_property["unexpected"] = True
                for instance, expected in (
                    (positive, True),
                    (negative, False),
                    (extra_property, False),
                ):
                    self.assertEqual(alias.is_valid(instance), expected)
                    self.assertEqual(explicit.is_valid(instance), expected)

    def test_current_closeout_projection_requires_retired_paths_without_mutating_legacy(self) -> None:
        current = load("schemas/closeout-plan.schema.json")
        legacy_path = PACKAGE / "schemas/closeout-plan-3.0.schema.json"
        legacy = load("schemas/closeout-plan-3.0.schema.json")

        self.assertEqual(current["properties"]["schema_version"]["const"], "4.0")
        self.assertIn("retired_tracked_paths", current["properties"]["projection"]["required"])
        self.assertIn("retired_tracked_paths", current["properties"]["projection"]["properties"])
        self.assertEqual(legacy["properties"]["schema_version"]["const"], "3.0")
        self.assertNotIn("retired_tracked_paths", legacy["properties"]["projection"]["properties"])
        self.assertEqual(
            hashlib.sha256(legacy_path.read_bytes()).hexdigest(),
            "4ac0576d0ac425dc9cd74b0390b63eb124d0ffc08e375d11857faba41153addc",
        )

    def test_archived_archive_stage_is_pending_ready_recovery(self) -> None:
        temp_root = tempfile.mkdtemp(prefix="finalizer-archived-recovery-")
        root = Path(temp_root)
        task_dir = root / ".trellis/tasks/archive/251"
        task_dir.mkdir(parents=True)
        task_ref = ".trellis/tasks/251"
        transaction = {
            "task_ref": task_ref,
            "next_transition": "archive",
            "repo_ref": "castbox/guru-trellis",
            "base_branch": "main",
            "branch": "fix/251",
            "remote": "origin",
            "branch_review_commit": "a" * 40,
            "publication_head": "b" * 40,
            "plan_digest": "c" * 64,
            "publication": {"title": "title", "body": "body"},
            "close_issues": [251],
            "mode": "existing_pr_recovery",
            "pr": {"number": 59, "url": "https://github.com/castbox/guru-trellis/pull/59"},
            "adopted_pr": {"initial_is_draft": True},
        }
        pr = {
            "number": 59,
            "url": transaction["pr"]["url"],
            "isDraft": True,
            "headRefOid": "d" * 40,
        }
        summary = {
            "task": {"artifact_dir": task_ref, "archive_dir": ".trellis/tasks/archive/251"},
            "github": {"pr_url": pr["url"]},
            "index": {"search_terms": {"pr_refs": ["PR #59"]}},
        }
        (task_dir / GTT.FINISH_SUMMARY_ARTIFACT).write_text("{}\n", encoding="utf-8")
        with (
            mock.patch.object(GTT, "repo_relative", return_value=".trellis/tasks/archive/251"),
            mock.patch.object(GTT, "task_json", return_value={"status": "completed"}),
            mock.patch.object(GTT, "closeout_plan_path", return_value=Path("/missing-plan")),
            mock.patch.object(GTT, "publish_config", return_value={"remote": "origin"}),
            mock.patch.object(GTT, "load_config", return_value={}),
            mock.patch.object(GTT, "validate_github_remote_repository", return_value="castbox/guru-trellis"),
            mock.patch.object(GTT, "resolve_closeout_pull_request", return_value=pr),
            mock.patch.object(GTT, "canonical_pull_request_url", return_value=pr["url"]),
            mock.patch.object(GTT, "current_head", return_value="d" * 40),
            mock.patch.object(GTT, "closeout_remote_branch_head", return_value="d" * 40),
            mock.patch.object(GTT, "read_json", return_value=summary),
            mock.patch.object(GTT, "validate_finish_summary"),
        ):
            context = GTT.finalization_current_archived_context(
                root,
                task_dir,
                {"task_ref": task_ref},
                transaction,
            )
        self.assertEqual(context["transaction_state"], "archived")
        self.assertFalse(context["published_transition_complete"])
        self.assertIsNone(context["published_pr"])
        self.assertEqual(context["plan"]["git"]["publication_head"], "d" * 40)
        shutil.rmtree(temp_root)

    def test_archived_archive_stage_preserves_ready_pr_recovery(self) -> None:
        temp_root = tempfile.mkdtemp(prefix="finalizer-archived-ready-recovery-")
        root = Path(temp_root)
        task_dir = root / ".trellis/tasks/archive/251"
        task_dir.mkdir(parents=True)
        task_ref = ".trellis/tasks/251"
        transaction = {
            "task_ref": task_ref,
            "next_transition": "archive",
            "repo_ref": "castbox/guru-trellis",
            "base_branch": "main",
            "branch": "fix/251",
            "remote": "origin",
            "branch_review_commit": "a" * 40,
            "publication_head": "b" * 40,
            "plan_digest": "c" * 64,
            "publication": {"title": "title", "body": "body"},
            "close_issues": [251],
            "mode": "existing_pr_recovery",
            "pr": {"number": 59, "url": "https://github.com/castbox/guru-trellis/pull/59"},
            "adopted_pr": {"initial_is_draft": False},
        }
        pr = {
            "number": 59,
            "url": transaction["pr"]["url"],
            "isDraft": False,
            "headRefOid": "d" * 40,
        }
        summary = {
            "task": {"artifact_dir": task_ref, "archive_dir": ".trellis/tasks/archive/251"},
            "github": {"pr_url": pr["url"]},
            "index": {"search_terms": {"pr_refs": ["PR #59"]}},
        }
        (task_dir / GTT.FINISH_SUMMARY_ARTIFACT).write_text("{}\n", encoding="utf-8")
        with (
            mock.patch.object(GTT, "repo_relative", return_value=".trellis/tasks/archive/251"),
            mock.patch.object(GTT, "task_json", return_value={"status": "completed"}),
            mock.patch.object(GTT, "closeout_plan_path", return_value=Path("/missing-plan")),
            mock.patch.object(GTT, "publish_config", return_value={"remote": "origin"}),
            mock.patch.object(GTT, "load_config", return_value={}),
            mock.patch.object(GTT, "validate_github_remote_repository", return_value="castbox/guru-trellis"),
            mock.patch.object(GTT, "resolve_closeout_pull_request", return_value=pr),
            mock.patch.object(GTT, "canonical_pull_request_url", return_value=pr["url"]),
            mock.patch.object(GTT, "current_head", return_value="d" * 40),
            mock.patch.object(GTT, "closeout_remote_branch_head", return_value="d" * 40),
            mock.patch.object(GTT, "read_json", return_value=summary),
            mock.patch.object(GTT, "validate_finish_summary"),
        ):
            context = GTT.finalization_current_archived_context(
                root, task_dir, {"task_ref": task_ref}, transaction
            )
        self.assertEqual(context["transaction_state"], "archived")
        self.assertFalse(context["published_transition_complete"])
        shutil.rmtree(temp_root)

    def test_interface_inventories_current_and_legacy_contract_assets(self) -> None:
        interface = load("interface.json")
        schemas = {item["id"]: item["path"] for item in interface["schemas"]}
        artifacts = {item["id"]: item["path"] for item in interface["artifacts"]}
        self.assertEqual(len(schemas), len(interface["schemas"]))
        self.assertEqual(len(artifacts), len(interface["artifacts"]))
        self.assertEqual(
            {
                "current_gate_schema_alias": "schemas/task-finalization-gate.schema.json",
                "current_gate_schema_5_0": "schemas/task-finalization-gate-5.0.schema.json",
                "current_semantic_review_input_alias": "schemas/semantic-review-input.schema.json",
                "current_semantic_review_input_3_0": "schemas/semantic-review-input-3.0.schema.json",
                "legacy_gate_schema_4_0": "schemas/task-finalization-gate-4.0.schema.json",
                "legacy_semantic_review_input_2_0": "schemas/semantic-review-input-2.0.schema.json",
            },
            {key: schemas[key] for key in (
                "current_gate_schema_alias",
                "current_gate_schema_5_0",
                "current_semantic_review_input_alias",
                "current_semantic_review_input_3_0",
                "legacy_gate_schema_4_0",
                "legacy_semantic_review_input_2_0",
            )},
        )
        self.assertEqual(
            artifacts["legacy_gate_example_3_0"],
            "examples/task-finalization-gate-3.0.json",
        )
        self.assertEqual(
            artifacts["legacy_semantic_review_input_2_0"],
            "examples/semantic-review-input-2.0.json",
        )

    def test_unversioned_examples_are_current_and_legacy_is_explicit(self) -> None:
        gate = load("examples/task-finalization-gate.json")
        review = load("examples/semantic-review-input.json")
        self.assertEqual(gate["schema_version"], "5.0")
        self.assertEqual(review["schema_version"], "3.0")
        for value in (gate, review):
            self.assertEqual(value["route"]["typed_exit"], "ready_for_merge")
            self.assertEqual(value["route"]["consumer"], {"kind": "skill", "id": "guru-merge-task-pr"})
            self.assertNotIn("verification_required", json.dumps(value, sort_keys=True))
        jsonschema.Draft202012Validator(load("schemas/task-finalization-gate.schema.json")).validate(gate)
        jsonschema.Draft202012Validator(load("schemas/semantic-review-input.schema.json")).validate(review)
        self.assertEqual(load("schemas/task-finalization-gate-4.0.schema.json")["properties"]["schema_version"]["const"], "4.0")
        self.assertEqual(load("schemas/semantic-review-input-2.0.schema.json")["properties"]["schema_version"]["const"], "2.0")
        self.assertEqual(
            hashlib.sha256((PACKAGE / "schemas/task-finalization-gate-4.0.schema.json").read_bytes()).hexdigest(),
            "eede98f83ece710b08e4288e6fa59ec10bdb8234d1557c66679a91539fe7c798",
        )
        self.assertEqual(
            hashlib.sha256((PACKAGE / "schemas/semantic-review-input-2.0.schema.json").read_bytes()).hexdigest(),
            "486d28daa78526176ecd11cbba9c1dbd2a7b46fa07b2b8fc3ef0963e62e52ffb",
        )
        legacy_examples = (
            (
                "examples/task-finalization-gate-3.0.json",
                "schemas/task-finalization-gate-3.0.schema.json",
                "8881ed49b300d25af183da1bdf454c9e2be2f48cc765447d0638b228a15be066",
            ),
            (
                "examples/semantic-review-input-2.0.json",
                "schemas/semantic-review-input-2.0.schema.json",
                "705620063f725147eef49fb48673bce2b5fbe882d15bd15a9af82c58fbc56492",
            ),
        )
        for example_path, schema_path, expected_sha256 in legacy_examples:
            with self.subTest(example=example_path):
                self.assertEqual(
                    hashlib.sha256((PACKAGE / example_path).read_bytes()).hexdigest(),
                    expected_sha256,
                )
                jsonschema.Draft202012Validator(load(schema_path)).validate(load(example_path))

    def test_current_input_examples_validate(self) -> None:
        interface = load("interface.json")
        for profile in interface["public_contracts"]["input"]["profiles"]:
            schema = load(profile["schema"]["path"])
            example = load(profile["example"]["path"])
            jsonschema.Draft202012Validator(schema).validate(example)

    def test_base_reconciliation_output_is_distinct_from_publication_stale(self) -> None:
        output = load("examples/public-base-reconciliation-required-output.json")
        jsonschema.Draft202012Validator(load("schemas/public-base-reconciliation-required-output.schema.json")).validate(output)
        self.assertEqual(output["task_head"], output["publication_head"])
        self.assertEqual(output["resume_target"], "finalization_resume")
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft202012Validator(load("schemas/public-publication-review-stale-output.schema.json")).validate(output)


if __name__ == "__main__":
    unittest.main()
