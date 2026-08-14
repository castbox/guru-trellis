from __future__ import annotations

import copy
import importlib.util
import hashlib
import json
import sys
import tempfile
import unittest
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
            mock.patch.object(GTT, "cmd_finish_work") as finish_work,
        ):
            result = GTT.cmd_execute_finalization_transition(args)

        self.assertEqual(result["stage"], "ready_recovered")
        self.assertEqual(result["output"], output)
        finish_work.assert_not_called()
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
