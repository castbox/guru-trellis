from __future__ import annotations

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

        mismatch = json.loads(json.dumps(payload))
        mismatch["index"]["search_terms"]["paths"] = payload["git"]["changed_paths"][:-1]
        self.assertIn(
            "index.search_terms.paths must equal sorted git.changed_paths.",
            GTT.finish_summary_errors(mismatch),
        )

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
        self.assertIn("current aggregate input is 6.0, gate is 5.0, and ignored transaction is 2.0", contract)
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
        sys.path.insert(0, str(PACKAGE.parents[1]))
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
        sys.path.insert(0, str(PACKAGE.parents[1]))
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
        self.assertEqual(transaction["properties"]["schema_version"]["const"], "2.0")
        self.assertNotIn("verify", transaction["properties"]["next_transition"]["enum"])
        self.assertNotIn("verification_ref", transaction["properties"])

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
