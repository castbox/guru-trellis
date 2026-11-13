from __future__ import annotations

import copy
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


class ChangeContextPackageContractTests(unittest.TestCase):
    def test_current_ai_owns_unexecuted_review_without_external_handoff(self) -> None:
        package = Path(__file__).resolve().parents[1]
        for path in ("SKILL.md", "references/contract.md"):
            with self.subTest(path=path):
                text = " ".join((package / path).read_text(encoding="utf-8").split())
                self.assertIn("The current executing AI is this Skill's semantic owner", text)
                self.assertIn("`owner_not_yet_executed`", text)
                self.assertIn("not a typed", text)
                self.assertIn("agent ID", text)
                self.assertIn("subagent evidence", text)
                self.assertIn("pre-existing owner result", text)
        contract = " ".join((package / "references/contract.md").read_text(encoding="utf-8").split())
        self.assertIn("Current-state review must finish before history preview", contract)
        self.assertIn("Pass only actual public invoke stdout", contract)
        self.assertIn("never read or reconstruct producer-private results", contract)
        self.assertIn("declared blocker or re-entry route when a real gap remains", contract)
        interface = json.loads((package / "interface.json").read_text(encoding="utf-8"))
        self.assertEqual(interface["judgment_mode"], "semantic")
        self.assertNotIn("owner_not_yet_executed", [row["id"] for row in interface["external_exits"]])

    def setUp(self) -> None:
        self.package = Path(__file__).resolve().parents[1]
        self.interface = json.loads((self.package / "interface.json").read_text(encoding="utf-8"))

    def test_identity_modes_semantic_stages_runtime_and_exits(self) -> None:
        self.assertEqual(self.interface["id"], "guru-discover-change-context")
        from runtime.schema import validate_json
        registry = json.loads((self.package.parents[1] / "registry.json").read_text())
        selected = next(row for row in registry["skills"] if row["id"] == self.interface["id"])
        version = selected["interface_schema_id"].removeprefix("guru-team-skill-interface-")
        validate_json(self.interface, self.package.parents[1] / "schemas" / f"skill-interface-{version}.schema.json", "selected_interface")
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
                "source_reader": "read-change-context-source",
                "owner_result_recorder": "record-context-discovery",
                "owner_result_validator": "check-context-discovery",
                "public_invocation": "invoke-guru-discover-change-context",
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

    def test_invocation_commands_share_declared_envelope_and_migration(self) -> None:
        commands = json.loads((self.package / "commands.json").read_text())["commands"]
        for command in commands:
            if command["runtime_role"] == "preview" or command["id"] == "read-change-context-source":
                continue
            flags = {item["flag"]: item for item in command["arguments"]}
            self.assertTrue(flags["--invocation"]["required"])
            self.assertEqual(command["stdin"], "optional_json")
            self.assertFalse({"--input", "--public-input", "--transition", "--mode"} & flags.keys())
        binding = self.interface["public_contracts"]["invocation"]["call_local"]
        schema = json.loads((self.package.parents[1] / binding["envelope"]["path"]).read_text())
        self.assertEqual(schema["$id"], "guru-stage0-invocation-semantic-owner-1.0")
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(binding["flag"], "--invocation")
        self.assertEqual(binding["stdin"], "-")
        contract = (self.package / "references/contract.md").read_text()
        self.assertIn("Issue #384 Invocation Migration", contract)
        self.assertIn("direct command-input replacement", contract)
        self.assertIn("public_input.mode", contract)

    def test_contract_keeps_semantic_and_history_boundaries(self) -> None:
        skill = (self.package / "SKILL.md").read_text(encoding="utf-8")
        contract = (self.package / "references/contract.md").read_text(encoding="utf-8")
        normalized_skill = " ".join(skill.split())
        normalized_contract = " ".join(contract.split())
        for phrase in (
            "closed loop",
            "AI Review Gate before any",
            "stdout-only",
            "--active-task <task>",
            "--recovery-continuation-id <id>",
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
            "writes no authorization field to owner state",
            "`scripts/invoke.sh --invocation -`",
            "`base_current` transition",
            "read-only Discovery observer",
            "Neither the public input nor owner result reconstruct Sync private result",
            "`guru-create-issue:created` does not use this draft binding",
            "including the creation-attempt marker",
            "original draft is not carried across Sync as source authority",
            "source issue may be live `open` or `closed`",
            "source-specific portable locator",
            "return the caller-authored `refresh_base` exit for complete re-entry from live authority",
            "at least one array must be non-empty",
            "facts_sha256` is recomputed from those returned fields",
            "do not issue a second duplicate search or re-read candidates after review",
            "never create a task, workspace, or ignored runtime file",
            "normal mapped route remains repository-write-free",
            "direct task identity independently as `--active-task`",
            "Only a real interruption adds `--recovery-continuation-id`",
            "change-context-recovery.json",
            "public wrapper deletes a current checkpoint only after its typed DTO passes",
            "Skill `guru-clarify-requirements`",
            "context_ready",
            "refresh_base",
            "Git-object source uses owner-result 4.0",
            "synchronized source",
            "schema-only copy",
            "original record/check/invoke",
            "genuine unknown `internal_error`",
        ):
            self.assertIn(phrase, normalized_contract)
        self.assertNotIn("scripts/invoke.sh --input ... --owner-result", normalized_contract)
        self.assertNotIn("finish-summary-index.json` as an input", contract)

    def test_wrappers_are_dispatcher_only_and_executable(self) -> None:
        wrappers = {
            "preview-change-context-history.sh": "history_previewer",
            "record-context-discovery.sh": "owner_result_recorder",
            "check-context-discovery.sh": "owner_result_validator",
        }
        for name, validator in wrappers.items():
            path = self.package / "scripts" / name
            wrapper = path.read_text(encoding="utf-8")
            self.assertTrue(path.stat().st_mode & 0o100)
            self.assertIn("runtime/launch.sh", wrapper)
            self.assertIn(f'source "$LAUNCHER" {self.interface["validators"][[x["id"] for x in self.interface["validators"]].index(validator)]["runtime_command"]}', wrapper)
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
        current_schema = json.loads((self.package / "schemas/change-context-owner-result-4.0.schema.json").read_text(encoding="utf-8"))
        current_example = json.loads((self.package / "examples/change-context-owner-result-4.0.json").read_text(encoding="utf-8"))
        self.assertEqual(current_schema["$id"], "https://github.com/castbox/guru-trellis/schemas/guru-change-context-owner-result-4.0.json")
        self.assertEqual(current_example["repository"]["source_kind"], "git_object")
        self.assertEqual(list(Draft202012Validator(current_schema).iter_errors(current_example)), [])
        schema = json.loads((self.package / "schemas/change-context-owner-result-3.0.schema.json").read_text(encoding="utf-8"))
        recovery_schema = json.loads((self.package / "schemas/change-context-recovery.schema.json").read_text(encoding="utf-8"))
        example = json.loads((self.package / "examples/change-context-owner-result-3.0.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["$id"], "https://github.com/castbox/guru-trellis/schemas/guru-change-context-owner-result-3.0.json")
        self.assertEqual(recovery_schema["$id"], "https://github.com/castbox/guru-trellis/schemas/guru-change-context-recovery-1.0.json")
        private_artifacts = {
            item["id"]: item for item in self.interface["public_contracts"]["private_artifacts"]
        }
        self.assertEqual(
            private_artifacts["change_context_recovery"]["persistence"],
            "ignored_runtime",
        )
        retired_worktree_state = "task_" + "worktree_" + "state"
        retired_superseded_digest = "superseded_" + "snapshot_" + "sha256"
        self.assertNotIn(retired_worktree_state, schema["properties"])
        self.assertNotIn(retired_superseded_digest, schema["properties"])
        self.assertNotIn("refresh_history", schema["properties"])
        self.assertEqual(example["skill_id"], "guru-discover-change-context")
        Draft202012Validator.check_schema(schema)
        Draft202012Validator.check_schema(recovery_schema)
        validator = Draft202012Validator(schema)
        self.assertEqual(list(validator.iter_errors(example)), [])
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
        missing_base_observation = copy.deepcopy(example)
        del missing_base_observation["base_observation"]["local_head"]
        self.assertNotEqual(list(validator.iter_errors(missing_base_observation)), [])
        active_schema = json.dumps(schema, sort_keys=True)
        self.assertNotIn("baseSyncResult", active_schema)
        self.assertNotIn("sync_result", active_schema)
        self.assertNotIn("base_sync_facts_sha256", active_schema)
        legacy_owner = json.loads((self.package / "schemas/change-context-owner-result.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(legacy_owner["$id"], "https://github.com/castbox/guru-trellis/schemas/guru-change-context-owner-result-2.0.json")
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
            "schema_fields": "result_identity",
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

    def test_active_public_input_and_both_reentry_projections_use_authoring_seed(self) -> None:
        schema = json.loads((self.package / "schemas/public-pre-task-input-4.0.schema.json").read_text())
        self.assertEqual(schema["$id"], "guru-stage0-discover-change-context-input-pre-task-4.0")
        self.assertEqual(
            set(schema["required"]),
            {"profile", "source_exit", "mode", "change_input", "continuation_id", "clarify_profile"},
        )
        self.assertNotIn("repo_locator", schema["properties"])
        self.assertNotIn("base_branch", schema["properties"])
        legacy = json.loads((self.package / "schemas/public-pre-task-input-3.0.schema.json").read_text())
        self.assertEqual(legacy["$id"], "guru-stage0-discover-change-context-input-pre-task-3.0")
        from runtime.discovery import select_authoring_profile
        from runtime.schema import validate_json
        for producer in ("guru-sync-base", "guru-clarify-requirements"):
            package = self.package.parent / producer
            interface = json.loads((package / "interface.json").read_text())
            contracts = interface["public_contracts"]
            consumers = [row for row in contracts["consumer_inputs"]
                         if row["consumer"] == {"kind":"skill", "id":"guru-discover-change-context"}]
            self.assertTrue(consumers)
            for consumer in consumers:
                contract = consumer["contract"]
                self.assertEqual(contract["kind"], "skill_input_authoring_seed")
                for row in contract.get("authoring_profiles", [contract]):
                    self.assertFalse(set(row["seed_fields"]) & set(row["authoring_fields"]))
                    self.assertIn("change_input", row["authoring_fields"])
                projection = next(row for row in contracts["projections"] if row["consumer_input_id"] == consumer["id"])
                output = next(row for row in contracts["outputs"] if row["exit_id"] == projection["exit_id"])
                actual = json.loads((package / output["example"]["path"]).read_text())
                selected = select_authoring_profile(contract, actual)
                seed = {row["target"]:actual[row["source"]] for row in projection["mappings"] if row["source"] in actual}
                self.assertEqual(set(seed), set(selected["seed_fields"]))
                profile = next(row for row in self.interface["public_contracts"]["input"]["profiles"] if row["id"] == selected["profile_id"])
                for variant in (selected, *selected.get("alternate_authoring", [])):
                    path = package / variant["authoring_example"]["path"]
                    if not path.is_file():path = self.package / variant["authoring_example"]["path"]
                    example = json.loads(path.read_text())
                    authored = {key:example[key] for key in variant["authoring_fields"]}
                    self.assertFalse(set(seed) & set(authored))
                    validate_json({**seed, **authored}, self.package / profile["schema"]["path"], "actual_consumer")

    def test_current_interface_navigation_matches_git_object_and_minimal_examples(self) -> None:
        artifacts = {item["id"]: item["path"] for item in self.interface["artifacts"]}
        schemas = {item["id"]: item["path"] for item in self.interface["schemas"]}
        profiles = {item["id"]: item for item in self.interface["public_contracts"]["input"]["profiles"]}
        outputs = {item["exit_id"]: item for item in self.interface["public_contracts"]["outputs"]}

        self.assertEqual(
            profiles["pre_task"]["schema"],
            {
                "schema_id": "guru-stage0-discover-change-context-input-pre-task-4.0",
                "path": "schemas/public-pre-task-input-4.0.schema.json",
            },
        )
        self.assertEqual(profiles["pre_task"]["example"]["path"], "examples/public-pre-task-input-4.0.json")
        from runtime.schema import validate_json
        current_output = outputs["context_ready"]
        output_schema = json.loads((self.package / current_output["schema"]["path"]).read_text())
        self.assertEqual(output_schema["$id"], current_output["schema"]["schema_id"])
        output_example = json.loads((self.package / current_output["example"]["path"]).read_text())
        validate_json(output_example, self.package / current_output["schema"]["path"], "selected_output")
        self.assertEqual(artifacts["change_context_owner_result_example"], "examples/change-context-owner-result-4.0.json")
        self.assertEqual(artifacts["public_input_pre_task_example"], "examples/public-pre-task-input-4.0.json")
        self.assertEqual(artifacts["public_output_context_ready_example_5_0"], "examples/public-context-ready-output-5.0.json")
        self.assertEqual(schemas["change_context_owner_result_schema"], "schemas/change-context-owner-result-4.0.schema.json")
        self.assertEqual(schemas["public_output_context_ready_5_0"], "schemas/public-context-ready-output-5.0.schema.json")

        for current_id, legacy_id in (
            ("change_context_owner_result_example", "legacy_change_context_owner_result_example_3_0"),
            ("public_input_pre_task_example", "legacy_public_input_pre_task_example_3_0"),
            ("public_output_context_ready_example_5_0", "legacy_718_public_context_ready_example_4_0"),
        ):
            self.assertIn(legacy_id, artifacts)
            self.assertTrue((self.package / artifacts[legacy_id]).is_file())
        for legacy_id in (
            "legacy_change_context_owner_result_schema_3_0",
            "legacy_718_public_context_ready_output_4_0",
            "legacy_pre_task_718",
        ):
            self.assertTrue((self.package / schemas[legacy_id]).is_file())

        pairs = (
            (
                "schemas/change-context-owner-result-4.0.schema.json",
                "examples/change-context-owner-result-4.0.json",
            ),
            (
                "schemas/public-pre-task-input-4.0.schema.json",
                "examples/public-pre-task-input-4.0.json",
            ),
            (
                "schemas/public-context-ready-output-5.0.schema.json",
                "examples/public-context-ready-output-5.0.json",
            ),
        )
        for schema_path, example_path in pairs:
            with self.subTest(schema=schema_path):
                schema = json.loads((self.package / schema_path).read_text(encoding="utf-8"))
                example = json.loads((self.package / example_path).read_text(encoding="utf-8"))
                self.assertEqual(list(Draft202012Validator(schema).iter_errors(example)), [])

        owner_index = json.loads((self.package / schemas["owner_result_index"]).read_text())
        self.assertEqual(
            [item["$ref"] for item in owner_index["oneOf"]],
            ["change-context-owner-result-3.0.schema.json", "change-context-owner-result-4.0.schema.json"],
        )


if __name__ == "__main__":
    unittest.main()
