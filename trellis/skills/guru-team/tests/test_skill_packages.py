from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
SKILLS_ROOT = REPO / "trellis/skills/guru-team"
FIXTURE = SKILLS_ROOT / "tests/fixtures/representative-active"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


runtime = load_module(
    "guru_team_trellis_skill_tests",
    REPO / "trellis/workflows/guru-team/scripts/python/guru_team_trellis.py",
)
preset = load_module(
    "apply_guru_team_trellis_skill_tests",
    REPO / "trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py",
)
native_adapter = load_module(
    "guru_team_native_adapter_skill_tests",
    SKILLS_ROOT / "adapters/eval/native_adapter.py",
)


class SourceValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "skills"
        shutil.copytree(FIXTURE, self.root)
        self.workflow = self.root / "workflow.md"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def validate(self) -> dict:
        return runtime.validate_skill_source(self.root, self.workflow)

    def read_interface(self) -> dict:
        return json.loads(
            (self.root / "packages/guru-example-action/interface.json").read_text(encoding="utf-8")
        )

    def write_interface(self, payload: dict) -> None:
        (self.root / "packages/guru-example-action/interface.json").write_text(
            json.dumps(payload),
            encoding="utf-8",
        )

    def interface_schema_errors(self, payload: dict) -> list[str]:
        schema = json.loads(
            (self.root / "schemas/skill-interface-1.3.schema.json").read_text(encoding="utf-8")
        )
        return runtime.skill_json_schema_validation_errors(
            payload,
            schema,
            "representative 1.3 interface",
        )

    def read_sync_interface(self) -> dict:
        return json.loads(
            (self.root / "packages/guru-example-sync/interface.json").read_text(encoding="utf-8")
        )

    def write_sync_interface(self, payload: dict) -> None:
        (self.root / "packages/guru-example-sync/interface.json").write_text(
            json.dumps(payload),
            encoding="utf-8",
        )

    def read_registry(self) -> dict:
        return json.loads((self.root / "registry.json").read_text(encoding="utf-8"))

    def write_registry(self, payload: dict) -> None:
        (self.root / "registry.json").write_text(json.dumps(payload), encoding="utf-8")

    def write_skill(self, content: str) -> None:
        (self.root / "packages/guru-example-action/SKILL.md").write_text(content, encoding="utf-8")

    def configure_action_direct_to_sync(
        self,
        item_schema: dict,
        item_example: object,
    ) -> None:
        schema_path = self.root / "packages/guru-example-action/schemas/action-forwarded-output.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        schema["required"] = ["exit_id", "item"]
        schema["properties"] = {
            "exit_id": {"const": "forwarded"},
            "item": item_schema,
        }
        schema_path.write_text(json.dumps(schema), encoding="utf-8")

        example_path = self.root / "packages/guru-example-action/examples/action-forwarded-output.json"
        example_path.write_text(
            json.dumps({"exit_id": "forwarded", "item": item_example}),
            encoding="utf-8",
        )

        interface = self.read_interface()
        projection = next(
            item for item in interface["public_contracts"]["projections"]
            if item["id"] == "rename_to_sync"
        )
        projection.clear()
        projection.update({
            "id": "rename_to_sync",
            "exit_id": "forwarded",
            "consumer_input_id": "sync_input",
            "operation": "direct",
        })
        self.write_interface(interface)

    def configure_structured_stop(self, contract_path: str = "consumers/stop/action-blocked.schema.json") -> None:
        schema_path = self.root / contract_path
        schema_path.parent.mkdir(parents=True, exist_ok=True)
        schema_path.write_text(
            json.dumps({
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "$id": "guru-fixture-stop-blocked-input-1.0",
                "type": "object",
                "additionalProperties": False,
                "required": ["exit_id"],
                "properties": {"exit_id": {"const": "blocked"}},
            }),
            encoding="utf-8",
        )
        interface = self.read_interface()
        consumer = next(
            item for item in interface["public_contracts"]["consumer_inputs"]
            if item["id"] == "stop_blocked_input"
        )
        consumer["payload_kind"] = "structured_json"
        consumer["contract"] = {
            "kind": "json_schema",
            "schema_id": "guru-fixture-stop-blocked-input-1.0",
            "path": contract_path,
        }
        projection = next(
            item for item in interface["public_contracts"]["projections"]
            if item["id"] == "select_to_stop"
        )
        projection.clear()
        projection.update({
            "id": "select_to_stop",
            "exit_id": "blocked",
            "consumer_input_id": "stop_blocked_input",
            "operation": "direct",
        })
        self.write_interface(interface)

    def test_production_registry_preserves_tombstone_and_activates_public_skills(self) -> None:
        result = runtime.validate_skill_source(
            SKILLS_ROOT,
            REPO / "trellis/workflows/guru-team/workflow.md",
        )
        self.assertEqual(result["status"], "passed", result["errors"])
        self.assertEqual(result["facts"]["reserved_ids"], ["guru-create-work-commit"])
        self.assertEqual(result["facts"]["planned_ids"], [])
        self.assertEqual(
            result["facts"]["active_ids"],
            ["guru-approve-task-plan", "guru-check-task", "guru-clarify-requirements", "guru-create-task-commit", "guru-create-task-workspace", "guru-discover-change-context", "guru-review-change-request", "guru-review-contract-wording", "guru-sync-base"],
        )
        self.assertEqual(result["facts"]["invoke_markers"], 9)
        self.assertEqual(result["facts"]["exit_markers"], 35)
        self.assertEqual(result["facts"]["target_markers"], 20)

        workflow = (REPO / "trellis/workflows/guru-team/workflow.md").read_text(encoding="utf-8")
        scope_gate = workflow.index("Scope Change Gate:")
        clarify_invoke = workflow.index(
            'guru-skill-invoke: {"skill":"guru-clarify-requirements"'
        )
        self.assertGreater(clarify_invoke, scope_gate)
        self.assertEqual(
            workflow.count('guru-skill-invoke: {"skill":"guru-clarify-requirements"'),
            1,
        )
        self.assertIn(
            'guru-skill-exit: {"skill":"guru-clarify-requirements","exit":"clear","consumer":{"kind":"workflow","id":"guru-requirements-clear-router"}}',
            workflow,
        )
        self.assertNotIn(
            "Scope Change Gate: when scope changes, first stop and ask the user",
            workflow,
        )
        self.assertIn("invocation_context.resume_target", workflow)
        self.assertIn(
            'guru-skill-exit: {"skill":"guru-review-change-request","exit":"ready","consumer":{"kind":"skill","id":"guru-create-task-workspace"}}',
            workflow,
        )
        self.assertNotIn("planned rather than active", workflow)
        self.assertNotIn(
            "The `pass` router maps `change_request` to the full task-intake continuation",
            workflow,
        )
        self.assertIn(
            "shared `guru-planning-approval-2.0` validator and exact reviewed/approved document",
            workflow,
        )
        self.assertNotIn("shared complete schema 1.2 validator", workflow)
        self.assertEqual(
            (REPO / "trellis/workflows/guru-team/workflow.md").read_bytes(),
            (REPO / ".trellis/workflow.md").read_bytes(),
        )

    def test_production_task_commit_package_contract(self) -> None:
        package = SKILLS_ROOT / "packages/guru-create-task-commit"
        interface = json.loads((package / "interface.json").read_text(encoding="utf-8"))
        skill = (package / "SKILL.md").read_text(encoding="utf-8")
        contract = (package / "references/contract.md").read_text(encoding="utf-8")
        workflow = (REPO / "trellis/workflows/guru-team/workflow.md").read_text(encoding="utf-8")

        self.assertEqual(interface["id"], "guru-create-task-commit")
        self.assertEqual(interface["schema_version"], "1.2")
        self.assertEqual(interface["judgment_mode"], "semantic")
        self.assertEqual(interface["modes"]["workflow"]["routing"], "global_workflow")
        self.assertEqual(interface["modes"]["standalone"]["routing"], "direct_discovery")
        self.assertEqual(
            interface["modes"]["workflow"]["entry_precondition_ids"],
            interface["modes"]["standalone"]["entry_precondition_ids"],
        )
        self.assertEqual(
            [item["id"] for item in interface["external_exits"]],
            ["committed", "revision-required", "blocked"],
        )
        self.assertEqual(interface["runtime_dependency"], runtime.SKILL_RUNTIME_DEPENDENCY)
        self.assertEqual(
            {item["id"]: item["runtime_command"] for item in interface["validators"]},
            {"candidate_validator": "check-commit-messages", "exact_executor": "create-task-commit"},
        )
        for phrase in ("creating a task commit", "committing Phase 2 changes", "finding fix", "revision commit"):
            self.assertIn(phrase, skill)
        self.assertIn("validate_commit_message()", contract)
        self.assertNotIn("def validate_commit_message", contract)
        self.assertEqual(workflow.count('guru-skill-invoke: {"skill":"guru-create-task-commit"'), 1)
        self.assertEqual(workflow.count('guru-skill-exit: {"skill":"guru-create-task-commit"'), 3)

    def test_active_downstream_planning_contracts_use_skill_owned_v2(self) -> None:
        commit_interface = json.loads(
            (
                SKILLS_ROOT
                / "packages/guru-create-task-commit/interface.json"
            ).read_text(encoding="utf-8")
        )
        planning_approval = next(
            item
            for item in commit_interface["entry_preconditions"]
            if item["id"] == "planning_approval"
        )
        self.assertIn("Skill-owned guru-planning-approval-2.0", planning_approval["binding"])
        self.assertIn("shared check-planning-approval --require-exit approved", planning_approval["freshness"])

        active_sources = [
            SKILLS_ROOT / "packages/guru-create-task-commit/interface.json",
            SKILLS_ROOT / "packages/guru-clarify-requirements/SKILL.md",
            SKILLS_ROOT / "packages/guru-clarify-requirements/references/contract.md",
        ]
        forbidden = (
            "schema 1.2 approval and planning document digests",
            "schema 1.2 planning-approval validator",
            "explicit-post-planning-review",
        )
        for path in active_sources:
            text = path.read_text(encoding="utf-8")
            self.assertIn("guru-planning-approval-2.0", text, path)
            for phrase in forbidden:
                self.assertNotIn(phrase, text, path)

        overlay_spec = (REPO / ".trellis/spec/preset/overlay-guidelines.md").read_text(
            encoding="utf-8"
        )
        for phrase in (
            "43 inventory-pinned upstream overlay payloads",
            "`transitional_legacy` assets owned by issue #132",
            "legacy `schema 1.2`",
            "`explicit-post-planning-review` implement-agent wording",
            "must not guide current Guru package/runtime behavior",
        ):
            self.assertIn(phrase, overlay_spec)

    def test_sync_base_entrypoints_bind_prepare_to_reviewed_resolution(self) -> None:
        start_paths = [
            REPO / "trellis/presets/guru-team/overlays/.agents/skills/trellis-start/SKILL.md",
            REPO / "trellis/presets/guru-team/overlays/.codex/prompts/trellis-start.md",
            REPO / "trellis/presets/guru-team/overlays/.codex/skills/trellis-start/SKILL.md",
        ]
        entry_paths = [
            REPO / ".trellis/workflow.md",
            REPO / "trellis/workflows/guru-team/workflow.md",
            *start_paths,
        ]
        command = ".trellis/guru-team/scripts/bash/prepare-task.sh --json"
        for path in entry_paths:
            text = path.read_text(encoding="utf-8")
            offsets = []
            start = 0
            while (offset := text.find(command, start)) >= 0:
                offsets.append(offset)
                start = offset + len(command)
            self.assertTrue(offsets, path)
            for offset in offsets:
                command_window = text[offset:offset + 320]
                self.assertIn("--expected-resolution-sha256", command_window, path)
                self.assertNotIn("--resolution-file", command_window, path)

        for path in start_paths:
            text = path.read_text(encoding="utf-8")
            route_offset = text.find("mandatory invoke `guru-sync-base`")
            context_offset = text.find("python3 ./.trellis/scripts/get_context.py")
            self.assertGreaterEqual(route_offset, 0, path)
            self.assertGreaterEqual(context_offset, 0, path)
            self.assertLess(route_offset, context_offset, path)

        flow = (REPO / "docs/requirements/guru-team-trellis-flow.md").read_text(encoding="utf-8")
        self.assertIn("guru-review-change-request -> guru-create-task-workspace", flow)
        result_offset = flow.index(
            "Script-->>AI: base-sync result + post_sync_resolution_sha256 + facts_sha256"
        )
        validator_offset = flow.index(
            "AI->>Script: check-base-sync --result-json ...",
            result_offset,
        )
        self.assertLess(result_offset, validator_offset)
        self.assertNotIn("mandatory post-execution AI Review Gate", flow)
        self.assertIn(
            "`guru-sync-base:synced` 后按 mandatory marker 进入完整六 Skill Intake chain",
            flow,
        )
        self.assertIn('SB -->|"skipped"| SkipRoute["original non-repo route"]', flow)

        workflow_contract = (REPO / ".trellis/spec/workflow/workflow-contract.md").read_text(
            encoding="utf-8"
        )
        normalized_contract = " ".join(workflow_contract.split())
        self.assertIn(
            "deterministic profile owns stdout resolution facts, pre-sync digest-bound "
            "execution, post-sync resolution generation, objective live Git validation, "
            "and typed exit",
            normalized_contract,
        )

    def test_platform_entries_and_workflows_only_route_task_commit_skill(self) -> None:
        entries = [
            REPO / "trellis/presets/guru-team/overlays/.agents/skills/trellis-continue/SKILL.md",
            REPO / "trellis/presets/guru-team/overlays/.codex/prompts/trellis-continue.md",
            REPO / "trellis/presets/guru-team/overlays/.codex/skills/trellis-continue/SKILL.md",
            REPO / "trellis/presets/guru-team/overlays/.cursor/commands/trellis-continue.md",
            REPO / "trellis/presets/guru-team/overlays/.claude/commands/trellis/continue.md",
        ]
        forbidden = ("git add -A", "--cleanup=verbatim", "背景：", "path_classifications")
        for path in entries:
            text = path.read_text(encoding="utf-8")
            self.assertIn("mandatory invoke `guru-create-task-commit`", text, path)
            self.assertIn("Typed-exit route:", text, path)
            for phrase in forbidden:
                self.assertNotIn(phrase, text, path)

        workflows = [
            REPO / "trellis/workflows/guru-team/workflow.md",
            REPO / ".trellis/workflow.md",
        ]
        workflow_forbidden = (
            "Work commit body must include",
            "背景：",
            "type` must be one of",
            "scope` must",
            "git commit --cleanup=verbatim",
            "def validate_commit_message",
            "validate_commit_message(",
        )
        for path in workflows:
            text = path.read_text(encoding="utf-8")
            self.assertIn('guru-skill-invoke: {"skill":"guru-create-task-commit"', text, path)
            self.assertIn("`check-commit-messages` shared branch validator", text, path)
            self.assertIn("selected-platform direct discovery", text, path)
            self.assertIn("does not make the package self-contained or portable", text, path)
            self.assertIn("`run-skill-command` runtime", text, path)
            self.assertNotRegex(text, r"(?i)\bgit\s+commit\b", path)
            for phrase in workflow_forbidden:
                self.assertNotIn(phrase, text, path)

    def test_public_readmes_share_standalone_runtime_semantics(self) -> None:
        readmes = [
            REPO / "README.md",
            REPO / "trellis/workflows/guru-team/README.md",
            REPO / "trellis/presets/guru-team/README.md",
        ]
        for path in readmes:
            text = path.read_text(encoding="utf-8")
            self.assertIn("standalone", text, path)
            self.assertIn("self-contained/portable", text, path)
            self.assertIn("run-skill-command", text, path)
            self.assertIn("完整", text, path)

    def test_public_readmes_match_canonical_extension_version(self) -> None:
        manifest = json.loads(
            (REPO / "trellis/guru-team-extension.json").read_text(encoding="utf-8")
        )
        canonical_version = manifest["version"]
        version_match = re.fullmatch(r"\d+\.\d+\.\d+-guru\.(\d+)", canonical_version)
        self.assertIsNotNone(version_match, canonical_version)
        canonical_revision = f".{version_match.group(1)}"
        readmes = [
            REPO / "README.md",
            REPO / "trellis/workflows/guru-team/README.md",
            REPO / "trellis/presets/guru-team/README.md",
        ]
        for path in readmes:
            text = path.read_text(encoding="utf-8")
            current_versions = set(
                re.findall(r"(?<!v)\b\d+\.\d+\.\d+-guru\.\d+\b", text)
            )
            self.assertEqual(current_versions, {canonical_version}, path)
            canonical_shorthand_revisions = set(
                re.findall(
                    r"\bcanonical\s+`?(\.\d+)`?",
                    text,
                    flags=re.IGNORECASE,
                )
            )
            self.assertLessEqual(
                canonical_shorthand_revisions,
                {canonical_revision},
                path,
            )

    def test_representative_active_package_and_routes_pass(self) -> None:
        result = self.validate()
        self.assertEqual(result["status"], "passed", result["errors"])
        self.assertEqual(result["facts"]["legacy_ids"], ["guru-example-legacy"])
        self.assertEqual(
            result["facts"]["minimal_handoff_ids"],
            ["guru-example-action", "guru-example-sync"],
        )
        interface = self.read_interface()
        consumers = {
            item["id"]: item for item in interface["public_contracts"]["consumer_inputs"]
        }
        projections = {
            item["id"]: item for item in interface["public_contracts"]["projections"]
        }
        self.assertEqual(consumers["stop_blocked_input"]["payload_kind"], "zero_payload")
        self.assertNotIn("contract", consumers["stop_blocked_input"])
        self.assertEqual(projections["select_to_stop"]["operation"], "select")
        self.assertEqual(projections["select_to_stop"]["mappings"], [])
        self.assertEqual(
            {item["operation"] for item in projections.values()},
            {"direct", "select", "rename", "normalize"},
        )

    def test_interface_12_contract_bytes_remain_published(self) -> None:
        schema = SKILLS_ROOT / "schemas/skill-interface.schema.json"
        self.assertEqual(
            hashlib.sha256(schema.read_bytes()).hexdigest(),
            "33e5daf1362d6580027254fc15d63824cb4688c9e97e896489e9e817b034841e",
        )
        self.assertEqual(runtime.SKILL_INTERFACE_SCHEMAS["guru-team-skill-interface-1.2"]["version"], "1.2")
        self.assertEqual(runtime.SKILL_INTERFACE_SCHEMAS["guru-team-skill-interface-1.3"]["version"], "1.3")

    def test_contract_discovery_distinguishes_legacy_and_minimal_variants(self) -> None:
        legacy = runtime.build_skill_contract_discovery(self.root, "guru-example-legacy")
        minimal = runtime.build_skill_contract_discovery(self.root, "guru-example-action")
        scalar = runtime.build_skill_contract_discovery(self.root, "guru-example-sync")
        self.assertEqual(legacy["variant"], "legacy")
        self.assertNotIn("input", legacy)
        self.assertEqual(minimal["variant"], "minimal_handoff")
        self.assertEqual(minimal["input"]["kind"], "structured_json")
        self.assertEqual(scalar["input"]["kind"], "scalar_cli")
        with self.assertRaises(runtime.WorkflowError) as raised:
            runtime.build_skill_contract_discovery(self.root, "guru-missing-skill")
        self.assertEqual(raised.exception.payload["code"], "unknown_skill")
        self.assertEqual(set(raised.exception.payload), {"code", "field_path", "remediation"})

    def test_contract_discovery_validation_failures_use_distinct_stable_codes(self) -> None:
        registry = self.read_registry()
        action = next(item for item in registry["skills"] if item["id"] == "guru-example-action")
        action["io_contract_state"] = "legacy"
        self.write_registry(registry)
        version_error = runtime.skill_contract_validation_error(
            "source",
            self.validate()["errors"],
        )
        self.assertEqual(version_error.payload["code"], "version_state_mismatch")

        self.write_registry(json.loads((FIXTURE / "registry.json").read_text(encoding="utf-8")))
        (self.root / "packages/guru-example-action/interface.json").unlink()
        asset_error = runtime.skill_contract_validation_error(
            "source",
            self.validate()["errors"],
        )
        self.assertEqual(asset_error.payload["code"], "contract_asset_invalid")

        installed_error = runtime.skill_contract_validation_error(
            "installed",
            ["installed platform package digest drift"],
        )
        self.assertEqual(installed_error.payload["code"], "installed_drift")
        for error in (version_error, asset_error, installed_error):
            self.assertEqual(set(error.payload), {"code", "field_path", "remediation"})

    def test_contract_discovery_cli_failure_is_closed(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(REPO / "trellis/workflows/guru-team/scripts/python/guru_team_trellis.py"),
                "discover-skill-contract",
                "--root",
                str(REPO),
                "--mode",
                "source",
                "--skill",
                "guru-missing-skill",
                "--json",
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(
            set(json.loads(result.stderr)),
            {"code", "field_path", "remediation"},
        )

    def test_representative_wrappers_emit_distinct_exits_and_stable_errors(self) -> None:
        environment = dict(os.environ)
        environment["GURU_TEAM_DISPATCHER"] = str(self.root / "fixture-dispatcher.py")
        action = self.root / "packages/guru-example-action/scripts/invoke.sh"
        sync = self.root / "packages/guru-example-sync/scripts/invoke.sh"
        completed = subprocess.run(
            [str(action), "--input", "examples/action-initial-input.json"],
            cwd=action.parents[1], env=environment, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        synced = subprocess.run(
            [str(sync), "--exit-id", "forwarded", "--item", "alpha"],
            cwd=sync.parents[1], env=environment, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        invalid = subprocess.run(
            [str(action)], cwd=action.parents[1], env=environment, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertEqual(json.loads(completed.stdout)["exit_id"], "completed")
        self.assertEqual(json.loads(synced.stdout)["exit_id"], "synced")
        self.assertNotEqual(invalid.returncode, 0)
        self.assertEqual(
            set(json.loads(invalid.stderr)),
            {"code", "field_path", "remediation"},
        )

    def test_registry_version_state_mismatch_fails_closed(self) -> None:
        registry = self.read_registry()
        action = next(item for item in registry["skills"] if item["id"] == "guru-example-action")
        action["io_contract_state"] = "legacy"
        self.write_registry(registry)
        self.assertTrue(any(
            "incompatible interface version/state" in item
            for item in self.validate()["errors"]
        ))

    def test_unknown_public_contract_field_fails_schema_validation(self) -> None:
        interface = self.read_interface()
        interface["public_contracts"]["unknown"] = True
        self.write_interface(interface)
        self.assertTrue(any(
            "additional property" in item and "public_contracts.unknown" in item
            for item in self.validate()["errors"]
        ))

    def test_missing_per_exit_example_and_consumer_input_fail(self) -> None:
        example = self.root / "packages/guru-example-action/examples/action-forwarded-output.json"
        example.unlink()
        self.assertTrue(any(
            "missing typed output example forwarded" in item
            for item in self.validate()["errors"]
        ))

        shutil.copyfile(
            FIXTURE / "packages/guru-example-action/examples/action-forwarded-output.json",
            example,
        )
        interface = self.read_interface()
        interface["public_contracts"]["consumer_inputs"].pop(0)
        self.write_interface(interface)
        self.assertTrue(any(
            "[projection_reference]" in item
            for item in self.validate()["errors"]
        ))

    def test_nullable_aggregate_authoring_template_fails(self) -> None:
        schema_path = self.root / "packages/guru-example-action/schemas/action-input.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        schema["oneOf"].append({"type": "null"})
        schema_path.write_text(json.dumps(schema), encoding="utf-8")
        self.assertTrue(any(
            "[input_nullable_template]" in item
            for item in self.validate()["errors"]
        ))

    def test_aggregate_requires_exact_ordered_profile_references(self) -> None:
        schema_path = self.root / "packages/guru-example-action/schemas/action-input.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        schema["oneOf"].reverse()
        schema_path.write_text(json.dumps(schema), encoding="utf-8")
        self.assertTrue(any(
            "[input_aggregate_oneof]" in item and "exact ordered" in item
            for item in self.validate()["errors"]
        ))

    def test_discriminator_requires_shared_required_field_and_matching_const(self) -> None:
        schema_path = self.root / "packages/guru-example-action/schemas/action-initial-input.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        schema["required"].remove("profile")
        schema["properties"]["profile"]["const"] = "wrong"
        schema_path.write_text(json.dumps(schema), encoding="utf-8")
        errors = self.validate()["errors"]
        self.assertTrue(any("[input_discriminator]" in item and "required" in item for item in errors))
        self.assertTrue(any("[input_discriminator]" in item and "schema const" in item for item in errors))

    def test_scalar_cli_requires_exact_ordered_typed_examples_and_binding(self) -> None:
        interface = self.read_sync_interface()
        interface["public_contracts"]["input"]["arguments"][1]["type"] = "positive_integer"
        interface["public_contracts"]["invocation"]["input_binding"]["argument_ids"].reverse()
        interface["public_contracts"]["invocation"]["example_argv"][-1] = "beta"
        self.write_sync_interface(interface)
        errors = self.validate()["errors"]
        self.assertTrue(any("[scalar_argument_value]" in item for item in errors))
        self.assertTrue(any("[invocation_input_binding]" in item for item in errors))
        self.assertTrue(any("[scalar_invocation_example]" in item for item in errors))

    def test_scalar_cli_allows_only_declared_optional_arguments_to_be_omitted(self) -> None:
        arguments = [
            {"id": "first", "flag": "--first", "type": "string", "required": True},
            {"id": "optional", "flag": "--optional", "type": "string", "required": False},
            {"id": "last", "flag": "--last", "type": "ascii_enum", "required": True},
        ]
        errors: list[str] = []
        values = runtime.skill_validate_scalar_argv(
            arguments, ["--first", "alpha", "--last", "ready"], "optional argv", errors
        )
        self.assertEqual(errors, [])
        self.assertEqual(values, {"first": "alpha", "last": "ready"})

        for argv in (
            ["--optional", "beta", "--last", "ready"],
            ["--last", "ready", "--first", "alpha"],
            ["--first", "alpha", "--first", "again", "--last", "ready"],
        ):
            with self.subTest(argv=argv):
                invalid: list[str] = []
                runtime.skill_validate_scalar_argv(arguments, argv, "invalid argv", invalid)
                self.assertTrue(invalid)

    def test_zero_payload_rejects_payload_fields_and_nonempty_projection(self) -> None:
        schema_path = self.root / "packages/guru-example-action/schemas/action-blocked-output.schema.json"
        example_path = self.root / "packages/guru-example-action/examples/action-blocked-output.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        schema["properties"]["reason"] = {"type": "string"}
        schema["required"].append("reason")
        schema_path.write_text(json.dumps(schema), encoding="utf-8")
        example = json.loads(example_path.read_text(encoding="utf-8"))
        example["reason"] = "blocked"
        example_path.write_text(json.dumps(example), encoding="utf-8")
        interface = self.read_interface()
        projection = next(
            item for item in interface["public_contracts"]["projections"]
            if item["id"] == "select_to_stop"
        )
        projection["mappings"] = [{"source": "exit_id", "target": "exit_id"}]
        self.write_interface(interface)
        errors = self.validate()["errors"]
        self.assertTrue(any("[projection_zero_payload_output]" in item for item in errors))
        self.assertTrue(any("[projection_zero_payload]" in item for item in errors))

    def test_empty_select_is_reserved_for_zero_payload_stop(self) -> None:
        interface = self.read_interface()
        projection = next(
            item for item in interface["public_contracts"]["projections"]
            if item["id"] == "rename_to_sync"
        )
        projection["operation"] = "select"
        projection["mappings"] = []
        self.write_interface(interface)
        self.assertTrue(any(
            "[projection_empty_select]" in item
            for item in self.validate()["errors"]
        ))

    def test_representative_invocation_validates_actual_consumer_projection(self) -> None:
        input_path = self.root / "packages/guru-example-action/examples/action-initial-input.json"
        input_payload = json.loads(input_path.read_text(encoding="utf-8"))
        input_payload["topic"] = "beta"
        input_path.write_text(json.dumps(input_payload), encoding="utf-8")
        consumer_path = self.root / "consumers/workflow/action-completed.schema.json"
        consumer = json.loads(consumer_path.read_text(encoding="utf-8"))
        consumer["properties"]["result"]["const"] = "alpha complete"
        consumer_path.write_text(json.dumps(consumer), encoding="utf-8")
        self.assertTrue(any(
            "[invocation_projection]" in item
            for item in self.validate()["errors"]
        ))

    def test_nonzero_output_requires_matching_exit_identity_const(self) -> None:
        schema_path = self.root / "packages/guru-example-action/schemas/action-completed-output.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        schema["properties"]["exit_id"] = {"type": "string", "minLength": 1}
        schema_path.write_text(json.dumps(schema), encoding="utf-8")
        self.assertTrue(any(
            "[output_exit_identity]" in item
            for item in self.validate()["errors"]
        ))

    def test_direct_projection_requires_exact_consumer_schema(self) -> None:
        consumer_path = self.root / "consumers/workflow/action-completed.schema.json"
        consumer = json.loads(consumer_path.read_text(encoding="utf-8"))
        consumer["properties"]["result"]["pattern"] = "^alpha complete$"
        consumer_path.write_text(json.dumps(consumer), encoding="utf-8")
        self.assertTrue(any(
            "[projection_direct_contract]" in item
            for item in self.validate()["errors"]
        ))

    def test_workflow_consumer_rejects_producer_owned_output_schema(self) -> None:
        interface = self.read_interface()
        consumer = next(
            item for item in interface["public_contracts"]["consumer_inputs"]
            if item["id"] == "workflow_completed_input"
        )
        consumer["contract"] = {
            "kind": "json_schema",
            "schema_id": "guru-fixture-action-completed-output-1.0",
            "path": "packages/guru-example-action/schemas/action-completed-output.schema.json",
        }
        self.write_interface(interface)
        self.assertTrue(any(
            "[consumer_owner_root]" in item
            for item in self.validate()["errors"]
        ))

    def test_non_skill_consumer_rejects_wrong_owner_root(self) -> None:
        workflow_path = "consumers/stop/action-completed.schema.json"
        target = self.root / workflow_path
        target.parent.mkdir(parents=True, exist_ok=True)
        schema = json.loads(
            (self.root / "consumers/workflow/action-completed.schema.json").read_text(encoding="utf-8")
        )
        target.write_text(json.dumps(schema), encoding="utf-8")
        interface = self.read_interface()
        consumer = next(
            item for item in interface["public_contracts"]["consumer_inputs"]
            if item["id"] == "workflow_completed_input"
        )
        consumer["contract"]["path"] = workflow_path
        self.write_interface(interface)
        self.assertTrue(any(
            "[consumer_owner_root]" in item
            for item in self.validate()["errors"]
        ))

        self.write_interface(json.loads(
            (FIXTURE / "packages/guru-example-action/interface.json").read_text(encoding="utf-8")
        ))
        self.configure_structured_stop("consumers/workflow/action-blocked.schema.json")
        self.assertTrue(any(
            "[consumer_owner_root]" in item
            for item in self.validate()["errors"]
        ))

    def test_non_skill_consumer_rejects_noncanonical_path_spelling(self) -> None:
        for path in (
            "./consumers/workflow/action-completed.schema.json",
            "consumers//workflow/action-completed.schema.json",
            "consumers/workflow/../workflow/action-completed.schema.json",
        ):
            with self.subTest(path=path):
                interface = self.read_interface()
                consumer = next(
                    item for item in interface["public_contracts"]["consumer_inputs"]
                    if item["id"] == "workflow_completed_input"
                )
                consumer["contract"]["path"] = path
                self.assertTrue(self.interface_schema_errors(interface))
                self.write_interface(interface)
                self.assertTrue(any(
                    "[consumer_owner_root]" in item
                    for item in self.validate()["errors"]
                ))
                self.write_interface(json.loads(
                    (FIXTURE / "packages/guru-example-action/interface.json").read_text(encoding="utf-8")
                ))

    def test_canonical_workflow_and_structured_stop_consumer_paths_pass(self) -> None:
        self.assertEqual(self.interface_schema_errors(self.read_interface()), [])
        self.assertEqual(self.validate()["status"], "passed")
        self.configure_structured_stop()
        self.assertEqual(self.interface_schema_errors(self.read_interface()), [])
        result = self.validate()
        self.assertEqual(result["status"], "passed", result["errors"])

    def test_closed_schema_subset_rejects_unsupported_and_malformed_keywords(self) -> None:
        schema_path = self.root / "packages/guru-example-action/schemas/action-completed-output.schema.json"
        original = json.loads(schema_path.read_text(encoding="utf-8"))

        def add_nested_resource(schema: dict) -> None:
            schema["$defs"] = {"target": {"type": "string"}}
            schema["properties"]["result"].update({
                "$id": "other.json",
                "$ref": "#/$defs/target",
            })

        mutations = {
            "pattern-properties": lambda schema: schema.update({
                "patternProperties": {"^result$": {"const": "not the example"}},
            }),
            "nested-unsupported": lambda schema: schema["properties"]["result"].update({
                "minProperties": 1,
            }),
            "keyword-type": lambda schema: schema["properties"]["result"].update({
                "minLength": "1",
            }),
            "boolean-schema": lambda schema: schema["properties"].update({"result": False}),
            "unresolved-ref": lambda schema: schema["properties"]["result"].update({
                "$ref": "missing.schema.json",
            }),
            "remote-ref": lambda schema: schema["properties"]["result"].update({
                "$ref": "https://example.com/schema.json",
            }),
            "recursive-ref": lambda schema: schema.update({
                "$defs": {"loop": {"$ref": "#/$defs/loop"}},
            }),
            "nested-id-resource": add_nested_resource,
            "format-type": lambda schema: schema["properties"]["result"].update({
                "format": [],
            }),
            "unsupported-format": lambda schema: schema["properties"]["result"].update({
                "format": "email",
            }),
            "invalid-pattern": lambda schema: schema["properties"]["result"].update({
                "pattern": "(",
            }),
            "python-only-pattern": lambda schema: schema["properties"]["result"].update({
                "pattern": "(?P<result>[a-z]+)",
            }),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                schema = json.loads(json.dumps(original))
                mutate(schema)
                schema_path.write_text(json.dumps(schema), encoding="utf-8")
                errors = self.validate()["errors"]
                self.assertTrue(any("[schema_subset]" in item for item in errors), errors)
        schema_path.write_text(json.dumps(original), encoding="utf-8")

    @staticmethod
    def portable_pattern_cases() -> list[tuple[str, str, str, bool]]:
        return [
            ("empty-search", "", "anything", True),
            ("unanchored", "beta", "alpha beta gamma", True),
            ("anchored", "^[a-z]+$", "alpha", True),
            ("strict-end-anchor", "^[a-z]+$", "a\n", False),
            ("escaped-literal", r"config\.json", "config.json", True),
            ("escaped-syntax", r"^\{ok\}$", "{ok}", True),
            ("ascii-class", "^[A-Za-z0-9_-]+$", "Az_9-", True),
            ("negated-class", "^[^0-9]{2,}$", "ab-", True),
            ("class-range-and-hyphen", "^[-a-c]+$", "-cab", True),
            ("capturing-alternation", "^(ab|cd)+$", "abcdab", True),
            ("noncapturing-alternation", "^(?:foo|bar){2}$", "foobar", True),
            ("star-and-optional-quantifiers", "^ab*c?$", "abbb", True),
            ("exact-quantifier", "^a{2}$", "aa", True),
            ("open-quantifier", "^a{2,}$", "aaaa", True),
            ("bounded-quantifier", "^ab{2,4}c+$", "abbbcc", True),
            ("negative-lookahead", "^(?!archive/).+$", "active/task", True),
            ("negative-lookahead-reject", "^(?!archive/).+$", "archive/task", False),
            ("astral-zero-width-before", "^(?!$)", "\U0001f600", True),
            ("astral-zero-width-interior", "(?!^|$)", "\U0001f600", True),
            ("astral-zero-width-after", "$(?!^)", "\U0001f600", True),
            ("astral-zero-width-alternation", "(?:a|(?!^|$))", "\U0001f600", True),
            ("astral-zero-width-empty-alternative", "(?:a|)", "\U0001f600", True),
            ("astral-zero-width-nullable-star", "(?!^|$)a*", "\U0001f600", True),
            ("astral-zero-width-nullable-optional", "(?!^|$)a?", "\U0001f600", True),
            ("astral-pair-is-one-dot", "^.$", "\U0001f600", True),
            ("astral-pair-is-not-two-dots", "^..$", "\U0001f600", False),
            ("astral-pair-is-one-negated-class", "^[^a]$", "\U0001f600", True),
            ("astral-pair-is-not-two-negated-classes", "^[^a][^a]$", "\U0001f600", False),
            ("astral-interior-cannot-start-dot", "(?!^|$).$", "\U0001f600", False),
            ("astral-interior-cannot-start-nonspace", r"(?!^|$)\S$", "\U0001f600", False),
            ("astral-interior-cannot-start-negated-class", "(?!^|$)[^a]$", "\U0001f600", False),
            ("isolated-high-is-one-dot", "^.$", "\ud800", True),
            ("isolated-low-is-one-dot", "^.$", "\udc00", True),
            ("isolated-high-is-nonspace", r"^\S$", "\ud800", True),
            ("isolated-low-is-nonspace", r"^\S$", "\udc00", True),
            ("isolated-high-is-negated-class", "^[^a]$", "\ud800", True),
            ("isolated-low-is-negated-class", "^[^a]$", "\udc00", True),
            ("isolated-high-before-bmp", "^..$", "\ud800a", True),
            ("isolated-high-after-bmp", "^..$", "a\ud800", True),
            ("isolated-low-before-bmp", "^..$", "\udc00a", True),
            ("isolated-low-after-bmp", "^..$", "a\udc00", True),
            ("isolated-high-quantified", "^.{2}$", "\ud800a", True),
            ("isolated-low-quantified", r"^\S{2}$", "a\udc00", True),
            ("isolated-high-nullable-negated-class", "^[^a]?a$", "\ud800a", True),
            ("isolated-low-nullable-nonspace", r"^a\S?$", "a\udc00", True),
            ("isolated-high-alternative-backtracking", "^(?:a|.){2}$", "\ud800a", True),
            ("isolated-low-alternative-backtracking", "^(?:a|[^a]){2}$", "a\udc00", True),
            ("valid-pair-remains-one-quantified-atom", "^.{1}$", "\ud83d\ude00", True),
            ("valid-pair-cannot-backtrack-as-two-atoms", "^(?:a|.){2}$", "\ud83d\ude00", False),
            ("control-escape", r"^\t$", "\t", True),
            ("ascii-unicode-escape", r"^\u0041+$", "AAA", True),
            ("class-whitespace-escape", r"^[\s]+$", "\u00a0", True),
            ("dot-line-feed", "^.$", "\n", False),
            ("dot-carriage-return", "^.$", "\r", False),
            ("dot-line-separator", "^.$", "\u2028", False),
            ("dot-paragraph-separator", "^.$", "\u2029", False),
            ("dot-astral-code-point", "^.$", "\U0001f600", True),
            ("ecma-whitespace", r"^\s+$", "\u00a0", True),
            ("python-only-whitespace", r"^\s+$", "\u001c", False),
            ("python-only-next-line", r"^\s+$", "\u0085", False),
            ("ecma-non-whitespace", r"^\S+$", "\u001c", True),
        ]

    def test_closed_pattern_subset_rejects_dialect_divergent_constructs(self) -> None:
        python_only = r"(?P<word>[a-z]+)"
        self.assertIsNotNone(re.compile(python_only))
        patterns = {
            "python-only-group": python_only,
            "python-only-anchor": r"\A[a-z]+",
            "digit-shorthand": r"\d+",
            "non-digit-shorthand": r"\D+",
            "word-shorthand": r"\w+",
            "non-word-shorthand": r"\W+",
            "unicode-property": r"\p{L}+",
            "hex-escape": r"\x41+",
            "null-escape": r"\0+",
            "word-boundary": r"\bword\b",
            "unicode-literal": "é+",
            "non-ascii-unicode-escape": r"\u00e9+",
            "raw-control": "a\n",
            "ecma-named-group": r"(?<word>[a-z]+)",
            "positive-lookahead": r"(?=a)a",
            "positive-lookbehind": r"(?<=a)b",
            "negative-lookbehind": r"(?<!a)b",
            "inline-flag": r"(?i:a)",
            "numbered-backreference": r"(a)\1",
            "lazy-quantifier": r"a+?",
            "possessive-quantifier": r"a++",
            "repeated-quantifier": r"a**",
            "misplaced-quantifier": r"*a",
            "empty-class": r"[]",
            "nested-class": r"[[a]]",
            "descending-class-range": r"[z-a]",
            "set-class-range-endpoint": r"[\s-a]",
            "class-complement-escape": r"[\S]",
            "overlong-bounded-quantifier": r"a{1234567}",
            "descending-bounded-quantifier": r"a{3,2}",
            "malformed-bounded-quantifier": r"a{,2}",
        }
        for name, pattern in patterns.items():
            with self.subTest(name=name):
                errors = runtime.skill_json_schema_subset_errors(
                    {"type": "string", "pattern": pattern},
                    "portable pattern",
                )
                self.assertTrue(any("invalid portable pattern" in item for item in errors), errors)

    def test_closed_pattern_subset_matches_expected_ecma_semantics(self) -> None:
        for name, pattern, value, expected in self.portable_pattern_cases():
            with self.subTest(name=name):
                errors = runtime.skill_json_schema_validation_errors(
                    value,
                    {"type": "string", "pattern": pattern},
                    "portable pattern",
                )
                self.assertEqual(not errors, expected, errors)

    def test_closed_pattern_subset_matches_node_ecma_unicode_regexp(self) -> None:
        node = shutil.which("node")
        if node is None:
            self.skipTest("Node.js is unavailable for the independent ECMA-262 comparison")
        cases = self.portable_pattern_cases()
        script = (
            "const cases = JSON.parse(process.argv[1]);"
            "process.stdout.write(JSON.stringify(cases.map((item) => "
            "new RegExp(item.pattern, 'u').test(item.value))));"
        )
        completed = subprocess.run(
            [
                node,
                "-e",
                script,
                json.dumps(
                    [{"pattern": pattern, "value": value} for _, pattern, value, _ in cases],
                    ensure_ascii=True,
                ),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        ecma_results = json.loads(completed.stdout)
        runtime_results = [
            not runtime.skill_json_schema_validation_errors(
                value,
                {"type": "string", "pattern": pattern},
                "portable pattern",
            )
            for _, pattern, value, _ in cases
        ]
        self.assertEqual(runtime_results, ecma_results)

    def test_generated_closed_patterns_match_node_ecma_unicode_regexp(self) -> None:
        node = shutil.which("node")
        if node is None:
            self.skipTest("Node.js is unavailable for the generated ECMA-262 comparison")

        atoms = ["a", "b", ".", r"\S", "[^a]", "[a]", r"\s", "(?:a|b)"]
        quantifiers = ["", "*", "+", "?", "{0}", "{1}", "{0,1}", "{1,2}", "{0,}"]
        bodies = [f"{atom}{quantifier}" for atom in atoms for quantifier in quantifiers]
        nullable_bodies = [
            f"(?:{alternative}){quantifier}"
            for atom in atoms
            for alternative in (f"{atom}|", f"|{atom}")
            for quantifier in ("", "*", "?", "{0,1}")
        ]
        assertions = [
            "^",
            "$",
            "(?!^)",
            "(?!$)",
            "(?!^|$)",
            "(?!a)",
            "(?!.)",
            r"(?!\S)",
            "(?![^a])",
            "(?!a|$)",
            "(?!|a)",
            "(?!a(?!b))",
            "(?!(?!a))",
        ]
        patterns = {"", "a|", "|a", "(?:|)", "(?!^|$)"}
        patterns.update(bodies)
        patterns.update(nullable_bodies)
        for assertion in assertions:
            patterns.add(assertion)
            for body in bodies + nullable_bodies:
                patterns.add(f"{assertion}{body}")
                patterns.add(f"{body}{assertion}")
        for body in bodies + nullable_bodies:
            patterns.add(f"^{body}$")
            patterns.add(f"(?!^|$){body}")
            patterns.add(f"(?:{body}|)")
            patterns.add(f"(?:|{body})")
        accepted_patterns = sorted(patterns)
        values = [
            "",
            "a",
            "b",
            "ab",
            "ba",
            "aa",
            "e",
            "\u00e9",
            "\U0001f600",
            "a\U0001f600",
            "\U0001f600a",
            "a\U0001f600b",
            "\U0001f600\U0001f600",
            "\n",
            "\r",
            "\u2028",
            "\u2029",
            "a\n",
            "\U0001f600\n",
            "\n\U0001f600",
            "\u00a0",
            "\u001c",
            " \t",
            "x\u2028y",
            "A0_",
            "-",
            "\ud800",
            "\udc00",
            "\ud800a",
            "a\ud800",
            "\udc00a",
            "a\udc00",
            "\ud83d\ude00",
        ]
        for pattern in accepted_patterns:
            with self.subTest(grammar_pattern=pattern):
                self.assertEqual(
                    runtime.skill_json_schema_subset_errors(
                        {"type": "string", "pattern": pattern},
                        "generated portable pattern",
                    ),
                    [],
                )

        # Node 26 has a V8 regression for an unanchored one-item negated class
        # before `$`; a spec-equivalent `{1}` wrapper bypasses that optimization.
        script = (
            "const matrix = JSON.parse(process.argv[1]);"
            "const major = Number(process.versions.node.split('.')[0]);"
            "const source = (pattern) => major === 26 ? `(?:${pattern}){1}` : pattern;"
            "process.stdout.write(JSON.stringify(matrix.patterns.map((pattern) => "
            "matrix.values.map((value) => new RegExp(source(pattern), 'u').test(value)))));"
        )
        completed = subprocess.run(
            [
                node,
                "-e",
                script,
                json.dumps(
                    {"patterns": accepted_patterns, "values": values},
                    ensure_ascii=True,
                ),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        node_results = json.loads(completed.stdout)
        mismatches = []
        for pattern_index, pattern in enumerate(accepted_patterns):
            for value_index, value in enumerate(values):
                runtime_result = not runtime.skill_json_schema_validation_errors(
                    value,
                    {"type": "string", "pattern": pattern},
                    "generated portable pattern",
                )
                if runtime_result != node_results[pattern_index][value_index]:
                    mismatches.append({
                        "pattern": pattern,
                        "value": value,
                        "runtime": runtime_result,
                        "node": node_results[pattern_index][value_index],
                    })
        self.assertEqual(len(accepted_patterns), 4081)
        self.assertEqual(len(values), 33)
        self.assertEqual(mismatches[:20], [], mismatches[:20])

    def test_closed_schema_subset_accepts_recursive_supported_keywords(self) -> None:
        schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$defs": {
                "payload": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["kind", "value"],
                    "properties": {
                        "kind": {"enum": ["alpha", "beta"]},
                        "value": {
                            "oneOf": [
                                {"type": "string", "minLength": 1},
                                {"type": "integer", "minimum": 1},
                            ],
                        },
                    },
                    "allOf": [{
                        "if": {"properties": {"kind": {"const": "alpha"}}},
                        "then": {"properties": {"value": {"type": "string"}}},
                    }],
                },
            },
            "$ref": "#/$defs/payload",
        }
        self.assertEqual(runtime.skill_json_schema_subset_errors(schema, "supported fixture"), [])
        self.assertEqual(
            runtime.skill_json_schema_validation_errors(
                {"kind": "alpha", "value": "ready"},
                schema,
                "supported fixture",
            ),
            [],
        )
        self.assertTrue(any(
            "wrong type" in item
            for item in runtime.skill_json_schema_validation_errors(
                {"kind": "alpha", "value": 1},
                schema,
                "supported fixture",
            )
        ))

    def test_closed_schema_integer_uses_json_schema_number_semantics(self) -> None:
        schema = {"type": "integer"}
        self.assertEqual(
            runtime.skill_json_schema_validation_errors(1.0, schema, "integer fixture"),
            [],
        )
        for value in (1.5, True):
            with self.subTest(value=value):
                self.assertTrue(runtime.skill_json_schema_validation_errors(
                    value,
                    schema,
                    "integer fixture",
                ))
        closed_empty_object = {"type": "object", "additionalProperties": False}
        self.assertEqual(
            runtime.skill_json_schema_validation_errors(
                {},
                closed_empty_object,
                "closed empty object fixture",
            ),
            [],
        )
        self.assertTrue(runtime.skill_json_schema_validation_errors(
            {"unexpected": "value"},
            closed_empty_object,
            "closed empty object fixture",
        ))

    def test_contract_json_assets_reject_nonfinite_and_overflow_numbers(self) -> None:
        schema_path = self.root / "packages/guru-example-action/schemas/action-completed-output.schema.json"
        original_schema = json.loads(schema_path.read_text(encoding="utf-8"))
        example_path = self.root / "packages/guru-example-action/examples/action-completed-output.json"
        for number in ("NaN", "Infinity", "-Infinity", "1e400"):
            with self.subTest(asset="schema", number=number):
                schema = dict(original_schema)
                schema["minimum"] = 0
                raw = json.dumps(schema).replace('"minimum": 0', f'"minimum": {number}')
                schema_path.write_text(raw, encoding="utf-8")
                errors = self.validate()["errors"]
                self.assertTrue(any("invalid JSON" in item for item in errors), errors)
            schema_path.write_text(json.dumps(original_schema), encoding="utf-8")
            with self.subTest(asset="example", number=number):
                example_path.write_text(
                    f'{{"exit_id":"completed","result":{number}}}',
                    encoding="utf-8",
                )
                errors = self.validate()["errors"]
                self.assertTrue(any("invalid JSON" in item for item in errors), errors)
            shutil.copyfile(
                FIXTURE / "packages/guru-example-action/examples/action-completed-output.json",
                example_path,
            )

    def test_interface_and_registry_reject_nonfinite_and_overflow_numbers(self) -> None:
        paths = (
            self.root / "packages/guru-example-action/interface.json",
            self.root / "registry.json",
        )
        originals = {path: path.read_text(encoding="utf-8") for path in paths}
        for path in paths:
            for number in ("NaN", "Infinity", "-Infinity", "1e400"):
                with self.subTest(path=path.name, number=number):
                    raw = originals[path].rstrip()
                    path.write_text(
                        raw[:-1] + f',"nonfinite_probe":{number}}}',
                        encoding="utf-8",
                    )
                    errors = self.validate()["errors"]
                    self.assertTrue(any("invalid JSON" in item for item in errors), errors)
            path.write_text(originals[path], encoding="utf-8")

    def test_package_local_schema_ref_rejects_nonfinite_and_overflow_numbers(self) -> None:
        aggregate_path = self.root / "packages/guru-example-action/schemas/action-input.schema.json"
        aggregate = json.loads(aggregate_path.read_text(encoding="utf-8"))
        target_path = self.root / "packages/guru-example-action/schemas/action-initial-input.schema.json"
        original_target = target_path.read_text(encoding="utf-8")
        for number in ("NaN", "Infinity", "-Infinity", "1e400"):
            with self.subTest(number=number):
                target = json.loads(original_target)
                target["minimum"] = 0
                raw = json.dumps(target).replace('"minimum": 0', f'"minimum": {number}')
                target_path.write_text(raw, encoding="utf-8")
                errors = runtime.skill_json_schema_subset_errors(
                    aggregate,
                    "aggregate input",
                    relative_root=aggregate_path.parent,
                    boundary=self.root,
                )
                self.assertTrue(any("unreadable package-local $ref" in item for item in errors), errors)
        target_path.write_text(original_target, encoding="utf-8")

    def test_invocation_stdout_rejects_nonfinite_and_overflow_numbers(self) -> None:
        dispatcher = self.root / "fixture-dispatcher.py"
        for number in ("NaN", "Infinity", "-Infinity", "1e400"):
            with self.subTest(number=number):
                dispatcher.write_text(
                    "#!/usr/bin/env python3\n"
                    f"print('{{\"exit_id\":\"completed\",\"result\":{number}}}')\n",
                    encoding="utf-8",
                )
                errors = self.validate()["errors"]
                self.assertTrue(any(
                    "[invocation_execution]" in item and "one typed-exit DTO" in item
                    for item in errors
                ), errors)

    def test_workflow_contract_markers_reject_nonfinite_and_overflow_numbers(self) -> None:
        original = self.workflow.read_text(encoding="utf-8")
        for number in ("NaN", "Infinity", "-Infinity", "1e400"):
            with self.subTest(number=number):
                self.workflow.write_text(
                    original.replace('"required":true', f'"required":{number}', 1),
                    encoding="utf-8",
                )
                self.assertTrue(any(
                    "invalid workflow skill marker JSON" in item
                    for item in self.validate()["errors"]
                ))

    def test_in_memory_schema_and_instance_reject_nonfinite_numbers(self) -> None:
        for value in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(location="schema", value=value):
                errors = runtime.skill_json_schema_subset_errors(
                    {"type": "number", "minimum": value},
                    "numeric schema",
                )
                self.assertTrue(any("non-finite number" in item for item in errors), errors)
            with self.subTest(location="instance", value=value):
                errors = runtime.skill_json_schema_validation_errors(
                    value,
                    {"type": "number", "minimum": 0},
                    "numeric instance",
                )
                self.assertTrue(any("non-finite number" in item for item in errors), errors)

    def test_public_contract_serialization_fails_closed_on_nonfinite_numbers(self) -> None:
        for value in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=value):
                with self.assertRaises(runtime.WorkflowError) as raised:
                    runtime.skill_public_json_text(
                        {"status": "ok", "value": value},
                        "discover-skill-contract",
                    )
                self.assertEqual(raised.exception.exit_code, 2)
                self.assertEqual(
                    raised.exception.payload,
                    {
                        "code": "public_json_serialization_failed",
                        "field_path": "stdout",
                        "remediation": "Return one finite, standard-JSON typed contract DTO and retry discovery.",
                    },
                )

    def test_closed_schema_date_time_format_matches_rfc3339_subset(self) -> None:
        schema = {"type": "string", "format": "date-time"}
        valid = (
            "0000-01-01T00:00:00Z",
            "0000-02-29T00:00:00Z",
            "2020-01-01T00:00:00Z",
            "2020-01-01t00:00:00z",
            "2020-02-29T23:59:59.123456+05:30",
            "1990-12-31T23:59:60Z",
            "1990-12-31T18:59:60-05:00",
            "1991-01-01T00:59:60+01:00",
        )
        invalid = (
            "0000-02-30T00:00:00Z",
            "2021-02-29T00:00:00Z",
            "2020-01-01T24:00:00Z",
            "2020-01-01T00:00:00+24:00",
            "2020-01-01T00:00:00",
            "2020-01-01 00:00:00Z",
            "1990-12-31T23:59:61Z",
            "1990-12-31T23:59:60+01:00",
            "2020-01-01T00:00:60Z",
        )
        for value in valid:
            with self.subTest(valid=value):
                self.assertEqual(
                    runtime.skill_json_schema_validation_errors(value, schema, "date-time"),
                    [],
                )
        for value in invalid:
            with self.subTest(invalid=value):
                self.assertTrue(runtime.skill_json_schema_validation_errors(
                    value,
                    schema,
                    "date-time",
                ))

    def test_closed_schema_uri_format_matches_rfc3986_subset(self) -> None:
        schema = {"type": "string", "format": "uri"}
        valid = (
            "https://example.com/a%20b?x=1#top",
            "urn:isbn:0451450523",
            "mailto:user@example.com",
            "http://[2001:db8::1]:8080/path",
            "http://[V1.a]:8080/path",
            "custom:",
        )
        invalid = (
            "relative/path",
            "//example.com/path",
            "1https://example.com",
            "foo: bar",
            "https://exa mple.com",
            "https://example.com/%ZZ",
            "https://example.com/%1",
            "https://example.com/\x01",
            "http://[invalid]/",
            "http://[fe80::1%eth0]/",
            "http://[fe80::1%25eth0]/",
            "http://[fe80::1%1]/",
            "http://host:port/path",
        )
        for value in valid:
            with self.subTest(valid=value):
                self.assertEqual(
                    runtime.skill_json_schema_validation_errors(value, schema, "uri"),
                    [],
                )
        for value in invalid:
            with self.subTest(invalid=value):
                self.assertTrue(runtime.skill_json_schema_validation_errors(
                    value,
                    schema,
                    "uri",
                ))

    def test_skill_consumer_requires_target_owned_matching_interface(self) -> None:
        interface = self.read_interface()
        consumer = next(
            item for item in interface["public_contracts"]["consumer_inputs"]
            if item["id"] == "sync_input"
        )
        consumer["contract"] = {
            "kind": "json_schema",
            "schema_id": "guru-fixture-action-forwarded-output-1.0",
            "path": "packages/guru-example-action/schemas/action-forwarded-output.schema.json",
        }
        self.write_interface(interface)
        self.assertTrue(any(
            "[consumer_skill_input]" in item and "target-owned" in item
            for item in self.validate()["errors"]
        ))

        interface = json.loads(
            (FIXTURE / "packages/guru-example-action/interface.json").read_text(encoding="utf-8")
        )
        consumer = next(
            item for item in interface["public_contracts"]["consumer_inputs"]
            if item["id"] == "sync_input"
        )
        consumer["contract"] = {
            "kind": "skill_input",
            "interface_path": "packages/guru-example-action/interface.json",
            "input_kind": "structured_json",
            "profile_id": "initial",
        }
        self.write_interface(interface)
        self.assertTrue(any(
            "[consumer_skill_input]" in item and "exact active registry interface" in item
            for item in self.validate()["errors"]
        ))

    def test_skill_consumer_rejects_stale_same_id_interface_locator(self) -> None:
        stale_path = self.root / "packages/guru-example-action/stale-sync-interface.json"
        shutil.copyfile(
            self.root / "packages/guru-example-sync/interface.json",
            stale_path,
        )
        interface = self.read_interface()
        consumer = next(
            item for item in interface["public_contracts"]["consumer_inputs"]
            if item["id"] == "sync_input"
        )
        consumer["contract"]["interface_path"] = (
            "packages/guru-example-action/stale-sync-interface.json"
        )
        self.write_interface(interface)
        self.assertTrue(any(
            "[consumer_skill_input]" in item
            and "exact active registry interface" in item
            for item in self.validate()["errors"]
        ))

    def test_direct_scalar_projection_rejects_example_only_compatibility(self) -> None:
        self.configure_action_direct_to_sync({"type": "string"}, "alpha")
        self.assertTrue(any(
            "[projection_contract_compatibility]" in item and "item" in item
            for item in self.validate()["errors"]
        ))

        schema_path = self.root / "packages/guru-example-action/schemas/action-forwarded-output.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        schema["required"].remove("item")
        schema_path.write_text(json.dumps(schema), encoding="utf-8")
        self.assertTrue(any(
            "[projection_required_source]" in item and "item" in item
            for item in self.validate()["errors"]
        ))

    def test_direct_scalar_projection_accepts_finite_compatible_values(self) -> None:
        self.configure_action_direct_to_sync({"enum": ["alpha", "beta"]}, "alpha")
        result = self.validate()
        self.assertEqual(result["status"], "passed", result["errors"])

    def test_direct_scalar_projection_accepts_positive_integer_domain(self) -> None:
        self.configure_action_direct_to_sync(
            {"type": "integer", "minimum": 1},
            1,
        )
        target = self.read_sync_interface()
        target["public_contracts"]["input"]["arguments"][1]["type"] = "positive_integer"
        target["public_contracts"]["input"]["example_argv"][-1] = "1"
        target["public_contracts"]["invocation"]["example_argv"][-1] = "1"
        self.write_sync_interface(target)
        result = self.validate()
        self.assertEqual(result["status"], "passed", result["errors"])

    def test_non_direct_projection_requires_all_valid_outputs_to_be_consumable(self) -> None:
        forwarded_path = self.root / "packages/guru-example-action/schemas/action-forwarded-output.schema.json"
        forwarded = json.loads(forwarded_path.read_text(encoding="utf-8"))
        forwarded["required"].remove("forwarded_item")
        forwarded_path.write_text(json.dumps(forwarded), encoding="utf-8")
        self.assertTrue(any(
            "[projection_required_source]" in item and "item" in item
            for item in self.validate()["errors"]
        ))

        shutil.copyfile(
            FIXTURE / "packages/guru-example-action/schemas/action-forwarded-output.schema.json",
            forwarded_path,
        )
        repeat_path = self.root / "packages/guru-example-action/schemas/action-repeat-output.schema.json"
        repeat = json.loads(repeat_path.read_text(encoding="utf-8"))
        repeat["properties"]["next_topic"].pop("pattern")
        repeat_path.write_text(json.dumps(repeat), encoding="utf-8")
        repeat_example_path = self.root / "packages/guru-example-action/examples/action-repeat-output.json"
        repeat_example = json.loads(repeat_example_path.read_text(encoding="utf-8"))
        repeat_example["next_topic"] = " "
        repeat_example_path.write_text(json.dumps(repeat_example), encoding="utf-8")
        self.assertTrue(any(
            "[projection_contract_compatibility]" in item and "next_topic" in item
            for item in self.validate()["errors"]
        ))

    def test_projection_rejects_duplicate_targets_when_example_values_alias(self) -> None:
        example_path = self.root / "packages/guru-example-action/examples/action-forwarded-output.json"
        example = json.loads(example_path.read_text(encoding="utf-8"))
        example["forwarded_item"] = "forwarded"
        example_path.write_text(json.dumps(example), encoding="utf-8")
        interface = self.read_interface()
        projection = next(
            item for item in interface["public_contracts"]["projections"]
            if item["id"] == "rename_to_sync"
        )
        projection["mappings"].append({"source": "forwarded_item", "target": "exit_id"})
        self.write_interface(interface)
        self.assertTrue(any(
            "[projection_target_duplicate]" in item
            for item in self.validate()["errors"]
        ))

    def test_unconsumed_output_field_fails_activation(self) -> None:
        schema_path = self.root / "packages/guru-example-action/schemas/action-forwarded-output.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        schema["properties"]["unused"] = {"type": "string"}
        schema_path.write_text(json.dumps(schema), encoding="utf-8")
        self.assertTrue(any(
            "[public_output_unconsumed_field]" in item
            for item in self.validate()["errors"]
        ))

    def test_projection_private_field_and_unknown_operation_fail(self) -> None:
        interface = self.read_interface()
        projection = interface["public_contracts"]["projections"][0]
        projection["mappings"][0]["source"] = "input_profile"
        self.write_interface(interface)
        self.assertTrue(any(
            "[projection_private_field]" in item
            for item in self.validate()["errors"]
        ))

        interface = self.read_interface()
        projection = interface["public_contracts"]["projections"][0]
        projection["operation"] = "evaluate"
        self.write_interface(interface)
        self.assertTrue(any("violates oneOf" in item for item in self.validate()["errors"]))

    def test_public_output_cannot_reuse_private_artifact_schema(self) -> None:
        interface = self.read_interface()
        output_schema = interface["public_contracts"]["outputs"][2]["schema"]
        interface["public_contracts"]["private_artifacts"][0]["schema"] = dict(output_schema)
        self.write_interface(interface)
        self.assertTrue(any(
            "[public_private_overlap]" in item
            for item in self.validate()["errors"]
        ))

    def test_public_private_schema_ids_and_paths_are_independently_disjoint(self) -> None:
        interface = self.read_interface()
        public_ref = interface["public_contracts"]["outputs"][2]["schema"]
        private_ref = interface["public_contracts"]["private_artifacts"][0]["schema"]
        private_path = self.root / "packages/guru-example-action" / private_ref["path"]
        private_schema = json.loads(private_path.read_text(encoding="utf-8"))
        private_schema["$id"] = public_ref["schema_id"]
        private_path.write_text(json.dumps(private_schema), encoding="utf-8")
        private_ref["schema_id"] = public_ref["schema_id"]
        self.write_interface(interface)
        self.assertTrue(any(
            "[public_private_overlap]" in item and "schema ids" in item
            for item in self.validate()["errors"]
        ))

        interface = json.loads(
            (FIXTURE / "packages/guru-example-action/interface.json").read_text(encoding="utf-8")
        )
        public_ref = interface["public_contracts"]["outputs"][2]["schema"]
        interface["public_contracts"]["private_artifacts"][0]["schema"]["path"] = public_ref["path"]
        self.write_interface(interface)
        self.assertTrue(any(
            "[public_private_overlap]" in item and "schema paths" in item
            for item in self.validate()["errors"]
        ))

        interface = json.loads(
            (FIXTURE / "packages/guru-example-action/interface.json").read_text(encoding="utf-8")
        )
        public_ref = interface["public_contracts"]["outputs"][2]["schema"]
        interface["public_contracts"]["private_artifacts"][0]["schema"]["path"] = (
            public_ref["path"].replace("schemas/", "schemas/./", 1)
        )
        self.write_interface(interface)
        self.assertTrue(any(
            "[public_private_overlap]" in item and "schema paths" in item
            for item in self.validate()["errors"]
        ))

    def test_package_contract_schema_locators_are_unique(self) -> None:
        interface = self.read_interface()
        artifacts = interface["public_contracts"]["private_artifacts"]
        artifacts[1]["schema"] = dict(artifacts[0]["schema"])
        self.write_interface(interface)
        errors = self.validate()["errors"]
        self.assertTrue(any("[contract_asset_duplicate_id]" in item for item in errors))
        self.assertTrue(any("[contract_asset_duplicate_path]" in item for item in errors))

    def test_public_wrapper_cannot_read_runtime_source(self) -> None:
        wrapper = self.root / "packages/guru-example-action/scripts/invoke.sh"
        wrapper.write_text(
            wrapper.read_text(encoding="utf-8") + "\n# guru_team_trellis.py is forbidden here\n",
            encoding="utf-8",
        )
        self.assertTrue(any(
            "[runtime_source_dependency]" in item
            for item in self.validate()["errors"]
        ))

    def test_public_wrapper_rejects_comment_only_dispatcher_and_local_output(self) -> None:
        wrapper = self.root / "packages/guru-example-action/scripts/invoke.sh"
        wrapper.write_text(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "# run-skill-command.sh\n"
            "printf '%s\\n' '{\"exit_id\":\"completed\",\"result\":\"alpha complete\"}'\n",
            encoding="utf-8",
        )
        self.assertTrue(any(
            "[invocation_dispatcher]" in item and "dispatcher-only template" in item
            for item in self.validate()["errors"]
        ))

        shutil.copyfile(
            FIXTURE / "packages/guru-example-action/scripts/invoke.sh",
            wrapper,
        )
        wrapper.write_text(
            wrapper.read_text(encoding="utf-8")
            + "printf '%s\\n' 'dead local output'\n",
            encoding="utf-8",
        )
        self.assertTrue(any(
            "[invocation_dispatcher]" in item and "dispatcher-only template" in item
            for item in self.validate()["errors"]
        ))

    def test_public_wrapper_resolves_dispatcher_from_every_supported_package_root(self) -> None:
        wrapper_bytes = (
            FIXTURE / "packages/guru-example-action/scripts/invoke.sh"
        ).read_bytes()
        package_roots = [
            Path("trellis/skills/guru-team/packages/guru-example-action"),
            Path(".trellis/guru-team/skills/packages/guru-example-action"),
            Path(".agents/skills/guru-example-action"),
            Path(".codex/skills/guru-example-action"),
            Path(".cursor/skills/guru-example-action"),
            Path(".claude/skills/guru-example-action"),
        ]
        for package_relative in package_roots:
            with self.subTest(package_root=str(package_relative)):
                repo = self.root / "dispatcher-resolution" / package_relative.parts[0].replace(".", "dot")
                package = repo / package_relative
                wrapper = package / "scripts/invoke.sh"
                wrapper.parent.mkdir(parents=True, exist_ok=True)
                wrapper.write_bytes(wrapper_bytes)
                wrapper.chmod(0o755)
                dispatcher = repo / ".trellis/guru-team/scripts/bash/run-skill-command.sh"
                dispatcher.parent.mkdir(parents=True, exist_ok=True)
                dispatcher.write_text(
                    "#!/usr/bin/env bash\n"
                    "set -euo pipefail\n"
                    "printf '%s\\n' '{\"exit_id\":\"completed\",\"result\":\"resolved\"}'\n",
                    encoding="utf-8",
                )
                dispatcher.chmod(0o755)
                environment = dict(os.environ)
                environment.pop("GURU_TEAM_DISPATCHER", None)
                result = subprocess.run(
                    [str(wrapper), "--input", "examples/action-initial-input.json"],
                    cwd=package,
                    env=environment,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout)["result"], "resolved")

    def test_extension_registry_and_legacy_inventory_mismatch_fail(self) -> None:
        extension_path = self.root / "extension.json"
        extension = json.loads(extension_path.read_text(encoding="utf-8"))
        extension["public_api"]["skill_contracts"]["registry_schema_id"] = "guru-team-skill-registry-1.0"
        extension_path.write_text(json.dumps(extension), encoding="utf-8")
        self.assertTrue(any(
            "incompatible Skill interface schema id" in item
            for item in self.validate()["errors"]
        ))

        extension = json.loads((FIXTURE / "extension.json").read_text(encoding="utf-8"))
        extension["public_api"]["skill_contracts"]["legacy_skill_ids"] = []
        extension_path.write_text(json.dumps(extension), encoding="utf-8")
        self.assertTrue(any(
            "legacy_skill_ids do not match" in item
            for item in self.validate()["errors"]
        ))

    def test_missing_mandatory_invoke_fails(self) -> None:
        text = self.workflow.read_text(encoding="utf-8")
        self.workflow.write_text("\n".join(line for line in text.splitlines() if "guru-skill-invoke:" not in line) + "\n", encoding="utf-8")
        self.assertTrue(any("no mandatory invoke" in item for item in self.validate()["errors"]))

    def test_reserved_mandatory_route_fails(self) -> None:
        registry = json.loads((self.root / "registry.json").read_text(encoding="utf-8"))
        registry["skills"] = [{"id": "guru-example-action", "state": "reserved", "reason": "fixture"}]
        (self.root / "registry.json").write_text(json.dumps(registry), encoding="utf-8")
        self.assertTrue(any("reserved skill" in item for item in self.validate()["errors"]))

    def test_unknown_and_duplicate_invoke_fail(self) -> None:
        original = self.workflow.read_text(encoding="utf-8")
        self.workflow.write_text(
            original
            + '<!-- guru-skill-invoke: {"skill":"guru-unknown-action","required":true} -->\n'
            + '<!-- guru-skill-invoke: {"skill":"guru-example-action","required":true} -->\n',
            encoding="utf-8",
        )
        errors = self.validate()["errors"]
        self.assertTrue(any("unknown skill guru-unknown-action" in item for item in errors))
        self.assertTrue(any("multiple mandatory invoke" in item for item in errors))

    def test_unmapped_multiple_and_unknown_exit_fail(self) -> None:
        lines = self.workflow.read_text(encoding="utf-8").splitlines()
        completed = next(line for line in lines if '"exit":"completed"' in line)
        self.workflow.write_text(
            "\n".join(line for line in lines if '"exit":"blocked"' not in line)
            + "\n"
            + completed
            + "\n"
            + '<!-- guru-skill-exit: {"skill":"guru-example-action","exit":"unknown","consumer":{"kind":"stop","id":"fixture-stop"}} -->\n',
            encoding="utf-8",
        )
        errors = self.validate()["errors"]
        self.assertTrue(any("blocked is unmapped" in item for item in errors))
        self.assertTrue(any("completed has multiple consumers" in item for item in errors))
        self.assertTrue(any("unknown external exit" in item for item in errors))

    def test_consumer_targets_require_unique_matching_declarations(self) -> None:
        original = self.workflow.read_text(encoding="utf-8")
        cases = {
            "missing": (
                original.replace(
                    '<!-- guru-workflow-target: {"id":"fixture-next"} -->\n',
                    "",
                ),
                "workflow consumer target fixture-next is not declared",
            ),
            "multiple": (
                original
                + '<!-- guru-workflow-target: {"id":"fixture-next"} -->\n',
                "workflow consumer target fixture-next has multiple declarations",
            ),
            "kind-mismatch": (
                original.replace(
                    '<!-- guru-workflow-target: {"id":"fixture-next"} -->',
                    '<!-- guru-stop-target: {"id":"fixture-next"} -->',
                ),
                "workflow consumer target fixture-next has a kind mismatch",
            ),
            "dangling": (
                original + '<!-- guru-stop-target: {"id":"unused-stop"} -->\n',
                "stop target unused-stop is dangling",
            ),
        }
        for name, (workflow, expected) in cases.items():
            with self.subTest(name=name):
                self.workflow.write_text(workflow, encoding="utf-8")
                self.assertIn(expected, self.validate()["errors"])

    def test_skill_consumer_must_resolve_to_active_or_planned_registry_entry(self) -> None:
        interface = self.read_interface()
        interface["external_exits"][0]["consumer"] = {
            "kind": "skill",
            "id": "guru-missing-consumer",
        }
        self.write_interface(interface)
        workflow = self.workflow.read_text(encoding="utf-8").replace(
            '{"kind":"skill","id":"guru-example-sync"}',
            '{"kind":"skill","id":"guru-missing-consumer"}',
        )
        self.workflow.write_text(workflow, encoding="utf-8")
        self.assertTrue(any(
            "references unknown skill consumer guru-missing-consumer" in item
            for item in self.validate()["errors"]
        ))

        registry = self.read_registry()
        registry["skills"].append({
            "id": "guru-missing-consumer",
            "state": "planned",
            "reason": "A later delivery owns this exact consumer package.",
        })
        self.write_registry(registry)
        self.assertEqual(self.validate()["status"], "failed")
        self.assertTrue(any(
            "projection rename_to_sync consumer does not match" in item
            for item in self.validate()["errors"]
        ))

        self.workflow.write_text(
            self.workflow.read_text(encoding="utf-8")
            + '<!-- guru-skill-invoke: {"skill":"guru-missing-consumer","required":true} -->\n',
            encoding="utf-8",
        )
        self.assertTrue(any(
            "planned skill guru-missing-consumer is referenced by a mandatory route" in item
            for item in self.validate()["errors"]
        ))

    def test_missing_declared_schema_fails(self) -> None:
        (self.root / "packages/guru-example-action/schemas/action-completed-output.schema.json").unlink()
        self.assertTrue(any("missing schema" in item for item in self.validate()["errors"]))

    def test_invalid_declared_schema_json_fails(self) -> None:
        schema = self.root / "packages/guru-example-action/schemas/action-completed-output.schema.json"
        schema.write_text("{invalid", encoding="utf-8")
        self.assertTrue(any("invalid JSON" in item for item in self.validate()["errors"]))

    def test_missing_validator_file_fails(self) -> None:
        (self.root / "packages/guru-example-action/scripts/invoke.sh").unlink()
        self.assertTrue(any("missing validator" in item for item in self.validate()["errors"]))

    def test_unsafe_artifact_path_fails(self) -> None:
        interface_path = self.root / "packages/guru-example-action/interface.json"
        interface = json.loads(interface_path.read_text(encoding="utf-8"))
        interface["artifacts"][0]["path"] = "../outside.json"
        interface_path.write_text(json.dumps(interface), encoding="utf-8")
        self.assertTrue(any("unsafe artifact path" in item for item in self.validate()["errors"]))

    def test_registry_symlink_is_rejected_without_reading_external_json(self) -> None:
        external = Path(self.temp.name) / "external-invalid.json"
        external.write_text("{invalid external", encoding="utf-8")
        registry = self.root / "registry.json"
        registry.unlink()
        registry.symlink_to(external)
        errors = self.validate()["errors"]
        self.assertTrue(any("symlink component" in item for item in errors))
        self.assertFalse(any("invalid JSON" in item for item in errors))

    def test_active_interface_empty_and_whitespace_names_fail(self) -> None:
        original_registry = self.read_registry()
        original_interface = self.read_interface()
        for value in ("", "   "):
            with self.subTest(value=repr(value)):
                registry = json.loads(json.dumps(original_registry))
                interface = json.loads(json.dumps(original_interface))
                registry["skills"][0]["name"] = value
                interface["name"] = value
                self.write_registry(registry)
                self.write_interface(interface)
                errors = self.validate()["errors"]
                self.assertTrue(any(
                    "name does not match" in item or "violates pattern" in item
                    for item in errors
                ))

    def test_bad_precondition_id_fails_when_modes_are_synchronized(self) -> None:
        interface = self.read_interface()
        interface["entry_preconditions"][0]["id"] = "Bad-ID"
        interface["modes"]["workflow"]["entry_precondition_ids"] = ["Bad-ID"]
        interface["modes"]["standalone"]["entry_precondition_ids"] = ["Bad-ID"]
        self.write_interface(interface)
        errors = self.validate()["errors"]
        self.assertTrue(any("violates pattern" in item and "entry_preconditions" in item for item in errors))

    def test_runtime_dependency_and_mode_routing_matrix_fail(self) -> None:
        original = self.read_interface()
        mutations = {
            "missing-dependency": lambda value: value.pop("runtime_dependency"),
            "bad-api": lambda value: value["runtime_dependency"].__setitem__("api_version", "2.0"),
            "bad-dispatcher": lambda value: value["runtime_dependency"].__setitem__("dispatcher", "other-dispatcher"),
            "workflow-routing": lambda value: value["modes"]["workflow"].__setitem__("routing", "direct_discovery"),
            "standalone-routing": lambda value: value["modes"]["standalone"].__setitem__("routing", "global_workflow"),
            "runtime-command": lambda value: value["validators"][0].__setitem__("runtime_command", "unknown-command"),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                interface = json.loads(json.dumps(original))
                mutate(interface)
                self.write_interface(interface)
                result = self.validate()
                self.assertEqual(result["status"], "failed")
                self.assertTrue(result["errors"])

    def test_judgment_mode_and_exact_stage_profiles(self) -> None:
        original = self.read_interface()
        semantic_stages = [
            "forward_behavior",
            "ai_review_gate",
            "conditional_human_confirmation",
            "recorder_validator",
            "typed_exit",
        ]
        deterministic_stages = [
            "forward_behavior",
            "recorder_validator",
            "typed_exit",
        ]

        deterministic = json.loads(json.dumps(original))
        deterministic["judgment_mode"] = "deterministic"
        deterministic["ordered_stages"] = deterministic_stages
        self.write_interface(deterministic)
        self.assertEqual(self.validate()["status"], "passed")

        mutations = {
            "missing-mode": lambda value: value.pop("judgment_mode"),
            "unknown-mode": lambda value: value.__setitem__("judgment_mode", "automatic"),
            "semantic-three-stage": lambda value: value.__setitem__("ordered_stages", deterministic_stages),
            "deterministic-five-stage": lambda value: (
                value.__setitem__("judgment_mode", "deterministic"),
                value.__setitem__("ordered_stages", semantic_stages),
            ),
            "old-schema": lambda value: value.__setitem__("schema_version", "1.1"),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                interface = json.loads(json.dumps(original))
                mutate(interface)
                self.write_interface(interface)
                result = self.validate()
                self.assertEqual(result["status"], "failed")
                self.assertTrue(result["errors"])

    def test_validator_runtime_command_cannot_self_map_to_dispatcher(self) -> None:
        interface = self.read_interface()
        interface["validators"][0]["runtime_command"] = interface["runtime_dependency"]["dispatcher"]
        self.write_interface(interface)

        result = self.validate()

        self.assertEqual(result["status"], "failed")
        self.assertEqual(
            result["errors"],
            [
                "interface for guru-example-action validator public_invocation runtime_command "
                "must not equal runtime_dependency.dispatcher"
            ],
        )

    def test_extension_runtime_capability_drift_fails(self) -> None:
        extension_path = self.root / "extension.json"
        extension = json.loads(extension_path.read_text(encoding="utf-8"))
        extension["public_api"]["skill_runtime"]["api_version"] = "2.0"
        extension_path.write_text(json.dumps(extension), encoding="utf-8")
        errors = self.validate()["errors"]
        self.assertTrue(any("incompatible Skill runtime capability" in item for item in errors))

    def test_bad_artifact_id_fails_schema_validation(self) -> None:
        interface = self.read_interface()
        interface["artifacts"][0]["id"] = "Bad-ID"
        self.write_interface(interface)
        errors = self.validate()["errors"]
        self.assertTrue(any("violates pattern" in item and "artifacts" in item for item in errors))

    def test_tests_object_fails_schema_validation(self) -> None:
        interface = self.read_interface()
        interface["tests"] = [{}]
        self.write_interface(interface)
        result = self.validate()
        self.assertEqual(result["status"], "failed")
        self.assertTrue(any("wrong type" in item and "tests" in item for item in result["errors"]))

    def test_test_evidence_parent_traversal_fails_schema_validation(self) -> None:
        interface = self.read_interface()
        interface["tests"] = ["tests/../outside.py"]
        self.write_interface(interface)
        result = self.validate()
        self.assertEqual(result["status"], "failed")
        self.assertTrue(any("violates pattern" in item and "tests" in item for item in result["errors"]))

    def test_empty_skill_md_fails_independently(self) -> None:
        self.write_skill("")
        result = self.validate()
        self.assertEqual(result["status"], "failed")
        self.assertTrue(any("opening frontmatter delimiter" in item for item in result["errors"]))

    def test_fictitious_test_evidence_fails_independently(self) -> None:
        interface = self.read_interface()
        interface["tests"] = ["tests/does-not-exist.py"]
        self.write_interface(interface)
        result = self.validate()
        self.assertEqual(result["status"], "failed")
        self.assertTrue(any("missing test evidence" in item for item in result["errors"]))

    def test_skill_frontmatter_structure_matrix_fails(self) -> None:
        original = (self.root / "packages/guru-example-action/SKILL.md").read_text(encoding="utf-8")
        invalid_documents = {
            "missing": "# No frontmatter\n",
            "unclosed": "---\nname: guru-example-action\ndescription: missing close\n",
            "duplicate-delimiter": original + "\n---\n",
            "duplicate-name": (
                "---\nname: guru-example-action\nname: guru-example-action\n"
                "description: Exercises the public closed-loop package contract without becoming a production skill.\n---\n"
            ),
            "extra-identity": (
                "---\nname: guru-example-action\nid: guru-example-action\n"
                "description: Exercises the public closed-loop package contract without becoming a production skill.\n---\n"
            ),
        }
        for label, content in invalid_documents.items():
            with self.subTest(label=label):
                self.write_skill(content)
                result = self.validate()
                self.assertEqual(result["status"], "failed")
                self.assertTrue(any("frontmatter" in item for item in result["errors"]))

    def test_skill_frontmatter_name_and_description_drift_fail(self) -> None:
        documents = {
            "name-drift": (
                "---\nname: guru-other-action\n"
                "description: Exercises the public closed-loop package contract without becoming a production skill.\n---\n"
            ),
            "description-drift": (
                "---\nname: guru-example-action\ndescription: Drifted discovery description.\n---\n"
            ),
            "name-whitespace-drift": (
                "---\nname: guru-example-action \n"
                "description: Exercises the public closed-loop package contract without becoming a production skill.\n---\n"
            ),
            "description-whitespace-drift": (
                "---\nname: guru-example-action\n"
                "description: Exercises the public closed-loop package contract without becoming a production skill. \n---\n"
            ),
            "empty-description": "---\nname: guru-example-action\ndescription: \n---\n",
        }
        for label, content in documents.items():
            with self.subTest(label=label):
                self.write_skill(content)
                result = self.validate()
                self.assertEqual(result["status"], "failed")
                self.assertTrue(any(
                    phrase in item
                    for item in result["errors"]
                    for phrase in ("identity", "description", "frontmatter")
                ))

    def test_test_evidence_outside_missing_symlink_and_duplicate_fail(self) -> None:
        original = self.read_interface()
        for value in ("references/contract.md", "../outside.py", "tests"):
            with self.subTest(kind="outside", value=value):
                interface = json.loads(json.dumps(original))
                interface["tests"] = [value]
                self.write_interface(interface)
                errors = self.validate()["errors"]
                self.assertTrue(any("tests root" in item or "violates pattern" in item for item in errors))

        interface = json.loads(json.dumps(original))
        interface["tests"] = ["tests/missing.py"]
        self.write_interface(interface)
        self.assertTrue(any("missing test evidence" in item for item in self.validate()["errors"]))

        interface = json.loads(json.dumps(original))
        interface["tests"] = ["tests/test_contract.py", "tests/test_contract.py"]
        self.write_interface(interface)
        duplicate_errors = self.validate()["errors"]
        self.assertTrue(any("uniqueItems" in item or "duplicate test evidence" in item for item in duplicate_errors))

        self.write_interface(original)
        evidence = self.root / "packages/guru-example-action/tests/test_contract.py"
        external = Path(self.temp.name) / "external-test.py"
        external.write_text("external test evidence\n", encoding="utf-8")
        evidence.unlink()
        evidence.symlink_to(external)
        symlink_errors = self.validate()["errors"]
        self.assertTrue(any("test evidence" in item and "symlink component" in item for item in symlink_errors))
        self.assertEqual(external.read_text(encoding="utf-8"), "external test evidence\n")

    def test_semantically_loose_interface_schema_fails_identity_check(self) -> None:
        schema = self.root / "schemas/skill-interface.schema.json"
        schema.write_text(json.dumps({"type": "string"}), encoding="utf-8")
        errors = self.validate()["errors"]
        self.assertTrue(any("skill interface schema" in item and "canonical schema contract digest" in item for item in errors))

    def test_nested_mode_id_returns_structured_failure(self) -> None:
        interface = self.read_interface()
        interface["modes"]["workflow"]["entry_precondition_ids"] = [["fresh_input"]]
        interface["modes"]["standalone"]["entry_precondition_ids"] = [["fresh_input"]]
        self.write_interface(interface)
        result = self.validate()
        self.assertEqual(result["status"], "failed")
        self.assertIsInstance(result["errors"], list)
        self.assertTrue(result["errors"])

    def test_interface_missing_required_additional_property_and_wrong_type_fail(self) -> None:
        original = self.read_interface()
        mutations = {
            "missing-required": lambda value: value.pop("reentry"),
            "additional-property": lambda value: value.__setitem__("unexpected", True),
            "wrong-type": lambda value: value.__setitem__("modes", []),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                interface = json.loads(json.dumps(original))
                mutate(interface)
                self.write_interface(interface)
                result = self.validate()
                self.assertEqual(result["status"], "failed")
                self.assertTrue(any(
                    phrase in item
                    for item in result["errors"]
                    for phrase in ("missing required property", "additional property", "wrong type")
                ))

    def test_duplicate_contract_ids_fail(self) -> None:
        interface = self.read_interface()
        interface["artifacts"].append(dict(interface["artifacts"][0]))
        self.write_interface(interface)
        self.assertTrue(any("duplicate id" in item for item in self.validate()["errors"]))

    def test_mode_parity_fails_for_different_order(self) -> None:
        interface = self.read_interface()
        interface["entry_preconditions"].append({
            "id": "second_input",
            "evidence": "fixture-input-2.json",
            "binding": "sha256",
            "freshness": "current fixture invocation",
        })
        interface["modes"]["workflow"]["entry_precondition_ids"] = ["fresh_input", "second_input"]
        interface["modes"]["standalone"]["entry_precondition_ids"] = ["second_input", "fresh_input"]
        self.write_interface(interface)
        self.assertTrue(any("workflow and standalone preconditions differ" in item for item in self.validate()["errors"]))

    def test_registry_schema_identity_and_constraint_matrix_fail(self) -> None:
        schema = self.root / "schemas/skill-registry.schema.json"
        schema.write_text(json.dumps({"type": "string"}), encoding="utf-8")
        self.assertTrue(any("skill registry schema" in item and "canonical schema contract digest" in item for item in self.validate()["errors"]))

        shutil.copyfile(FIXTURE / "schemas/skill-registry.schema.json", schema)
        original = self.read_registry()
        mutations = {
            "missing-required": lambda value: value.pop("schema_version"),
            "additional-property": lambda value: value.__setitem__("unexpected", True),
            "wrong-type": lambda value: value.__setitem__("skills", {}),
            "bad-id": lambda value: value["skills"][0].__setitem__("id", "Bad-ID"),
            "duplicate-id": lambda value: value["skills"].append(dict(value["skills"][0])),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                registry = json.loads(json.dumps(original))
                mutate(registry)
                self.write_registry(registry)
                result = self.validate()
                self.assertEqual(result["status"], "failed")
                self.assertTrue(result["errors"])

    def test_eval_corpus_discovery_and_legacy_migration_contract(self) -> None:
        discovery = runtime.build_skill_eval_discovery(self.root, "guru-example-action")
        self.assertEqual(discovery["corpus_schema_id"], "guru-team-skill-evals-1.0")
        self.assertEqual(discovery["case_ids"], ["complete-normal", "repeat-reentry", "blocked-family"])
        self.assertEqual([item["id"] for item in discovery["adapters"]], ["shared", "codex", "claude", "cursor"])
        descriptors = runtime.skill_eval_descriptor_index(self.root)
        self.assertEqual(
            {adapter_id: item["executable"] for adapter_id, item in descriptors.items()},
            {"shared": "shared.sh", "codex": "codex.sh", "claude": "claude.sh", "cursor": "cursor.sh"},
        )
        self.assertTrue(all((self.root / "adapters/eval" / item["executable"]).stat().st_mode & 0o100 for item in descriptors.values()))
        with self.assertRaises(runtime.WorkflowError) as unsupported:
            runtime.build_skill_eval_discovery(self.root, "guru-example-legacy")
        self.assertEqual(unsupported.exception.payload["code"], "evals_unsupported")

        legacy = json.loads((self.root / "legacy-evals.json").read_text(encoding="utf-8"))
        migrated = runtime.migrate_legacy_skill_evals(legacy, "guru-example-action", "completed")
        self.assertNotIn("expectations", json.dumps(migrated))
        self.assertEqual(migrated["evals"][0]["assertions"]["semantic"][0]["id"], "legacy-expectation-1")
        schema = json.loads((self.root / "schemas/skill-evals.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(runtime.skill_json_schema_validation_errors(migrated, schema, "migrated evals"), [])

    def test_eval_corpus_negative_matrix_uses_stable_errors(self) -> None:
        package = self.root / "packages/guru-example-action"
        corpus_path = package / "evals/evals.json"
        original = json.loads(corpus_path.read_text(encoding="utf-8"))
        mutations = {
            "unknown-field": (lambda value: value.__setitem__("unknown", True), "eval_schema_invalid"),
            "null": (lambda value: value["evals"][0].__setitem__("prompt", None), "eval_schema_invalid"),
            "duplicate-case": (lambda value: value["evals"].append(dict(value["evals"][0])), "eval_case_duplicate"),
            "unknown-profile": (lambda value: value["evals"][0].__setitem__("input_profile_id", "missing"), "eval_input_profile_unknown"),
            "unknown-exit": (lambda value: value["evals"][0].__setitem__("expected_exit", "missing"), "eval_expected_exit_unknown"),
            "absolute-file": (lambda value: value["evals"][0].__setitem__("files", ["/tmp/nope"]), "eval_schema_invalid"),
            "missing-file": (lambda value: value["evals"][0].__setitem__("files", ["evals/files/missing.txt"]), "eval_fixture_invalid"),
            "canonical-expectations": (lambda value: value["evals"][0].__setitem__("expectations", ["legacy"]), "eval_schema_invalid"),
            "unknown-assertion": (lambda value: value["evals"][0]["assertions"]["deterministic"][0].__setitem__("kind", "script"), "eval_schema_invalid"),
            "null-expected": (lambda value: value["evals"][0]["assertions"]["deterministic"][0].__setitem__("expected", None), "eval_schema_invalid"),
        }
        interface = self.read_interface()
        for label, (mutate, expected_code) in mutations.items():
            with self.subTest(label=label):
                corpus = json.loads(json.dumps(original))
                mutate(corpus)
                corpus_path.write_text(json.dumps(corpus), encoding="utf-8")
                with self.assertRaises(runtime.WorkflowError) as raised:
                    runtime.skill_eval_validate_corpus(self.root, package, interface)
                self.assertEqual(raised.exception.payload["code"], expected_code)
                self.assertEqual(set(raised.exception.payload), {"code", "field_path", "remediation"})
        corpus_path.write_text(json.dumps(original), encoding="utf-8")


class EvalRunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name) / "repo"
        self.skills = self.repo / "trellis/skills/guru-team"
        self.workflow = self.repo / "trellis/workflows/guru-team/workflow.md"
        self.workflow.parent.mkdir(parents=True)
        shutil.copytree(FIXTURE, self.skills)
        shutil.copyfile(FIXTURE / "workflow.md", self.workflow)
        self.runtime_target = self.repo / ".trellis/guru-team/scripts/bash/run-skill-command.sh"
        self.runtime_target.parent.mkdir(parents=True)
        shutil.copyfile(self.skills / "fixture-dispatcher.py", self.runtime_target)
        self.runtime_target.chmod(0o755)
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)
        self.runtime = REPO / "trellis/workflows/guru-team/scripts/python/guru_team_trellis.py"
        self.native_bin = Path(self.temp.name) / "native-bin"
        self.native_bin.mkdir()
        native_fixture = self.skills / "fake-native-cli.py"
        for command in ("guru-team-shared-eval", "codex", "claude", "cursor-agent"):
            target = self.native_bin / command
            shutil.copyfile(native_fixture, target)
            target.chmod(0o755)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_cli(
        self,
        *arguments: str,
        native: bool = True,
        native_direct_read: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        environment = dict(os.environ)
        environment["PATH"] = f"{self.native_bin}{os.pathsep}{environment['PATH']}" if native else "/usr/bin:/bin"
        environment.pop("GURU_TEAM_FAKE_NATIVE_DISPATCHER", None)
        environment.pop("GURU_TEAM_DISPATCHER", None)
        if native_direct_read is not None:
            environment["GURU_TEAM_FAKE_NATIVE_DIRECT_READ"] = native_direct_read
        return subprocess.run(
            [sys.executable, str(self.runtime), *arguments],
            cwd=self.repo, env=environment, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )

    def test_four_adapters_execute_same_corpus_and_expected_non_success_exits(self) -> None:
        discovery_process = self.run_cli(
            "discover-skill-evals", "--root", str(self.repo), "--mode", "source",
            "--skill", "guru-example-action", "--json",
        )
        self.assertEqual(discovery_process.returncode, 0, discovery_process.stderr)
        discovery = json.loads(discovery_process.stdout)
        self.assertTrue(all(item["native_available"] for item in discovery["adapters"]))
        self.assertEqual(
            {item["id"]: item["native_command"] for item in discovery["adapters"]},
            {"shared": "guru-team-shared-eval", "codex": "codex", "claude": "claude", "cursor": "cursor-agent"},
        )
        for adapter in ("shared", "codex", "claude", "cursor"):
            with self.subTest(adapter=adapter):
                run_root = Path(self.temp.name) / f"run-{adapter}"
                result = self.run_cli(
                    "run-skill-evals", "--root", str(self.repo), "--mode", "source",
                    "--skill", "guru-example-action", "--adapter", adapter,
                    "--run-root", str(run_root), "--semantic-grading", str(self.skills / "semantic-grading.json"),
                    "--human-feedback", str(self.skills / "human-feedback.json"),
                    "--json",
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                payload = json.loads(result.stdout)
                self.assertEqual(payload["status"], "passed")
                self.assertEqual({item["actual_exit"] for item in payload["cases"]}, {"completed", "repeat", "blocked"})
                self.assertTrue(Path(payload["evidence_path"]).resolve().is_relative_to(Path(self.temp.name).resolve()))
                self.assertFalse(Path(payload["evidence_path"]).resolve().is_relative_to(self.repo.resolve()))
                expected_command = {"shared": "guru-team-shared-eval", "codex": "codex", "claude": "claude", "cursor": "cursor-agent"}[adapter]
                for case in payload["cases"]:
                    transcript = json.loads(Path(case["transcript_locator"]).read_text(encoding="utf-8"))
                    self.assertEqual(Path(transcript["argv"][0]).name, expected_command)
                    context = Path(transcript["context_path"]).read_text(encoding="utf-8")
                    native_request = json.loads(Path(transcript["native_request_path"]).read_text(encoding="utf-8"))
                    adapter_request = json.loads(
                        Path(case["transcript_locator"]).with_name("adapter-request.json").read_text(encoding="utf-8")
                    )
                    self.assertNotIn("expected_exit", adapter_request)
                    self.assertNotIn("expected_exit", native_request)
                    projection_root = Path(transcript["projection_root"])
                    self.assertIn("First read the exact Skill contract with:", context)
                    self.assertIn("native-trace-helper.py", context)
                    self.assertNotIn("Exact SKILL.md:", context)
                    self.assertIn("scripts/invoke.sh", context)
                    self.assertIn("Case prompt:", context)
                    self.assertIn(
                        "The adapter has already completed any declared owner staging and checker validation",
                        context,
                    )
                    self.assertIn("Use the exact public_invocation.arguments", context)
                    self.assertIn("Do not read linked references", context)
                    self.assertEqual(set(native_request), {
                        "schema_version", "skill_id", "case_id", "prompt", "files",
                        "workdir", "public_package_root", "public_invocation",
                    })
                    self.assertEqual(Path(native_request["public_package_root"]), projection_root)
                    self.assertNotIn(str(self.skills.resolve()), context)
                    self.assertNotIn(str(self.skills.resolve()), json.dumps(native_request))
                    boundary = Path(transcript["protocol_path"]).with_name("public-invocation-boundary.sh")
                    boundary_text = boundary.read_text(encoding="utf-8")
                    compile(boundary_text, str(boundary), "exec")
                    self.assertNotIn(str(self.repo.resolve()), boundary_text)
                    self.assertNotIn(str((self.skills / "fixture-dispatcher.py").resolve()), boundary_text)
                    self.assertNotIn("guru_team_trellis.py", boundary_text)
                    self.assertFalse((projection_root / "evals").exists())
                    self.assertFalse(any(path.name == "guru_team_trellis.py" for path in projection_root.rglob("*")))
                    native_trace = json.loads(Path(transcript["native_trace_path"]).read_text(encoding="utf-8"))
                    self.assertEqual(Path(native_trace["projection_root"]), projection_root)
                    self.assertEqual(native_trace["skill_sha256"], hashlib.sha256((projection_root / "SKILL.md").read_bytes()).hexdigest())
                    self.assertEqual(native_trace["wrapper_sha256"], hashlib.sha256((projection_root / "scripts/invoke.sh").read_bytes()).hexdigest())
                    self.assertEqual(native_trace["events"][0]["kind"], "read")
                    self.assertEqual(native_trace["events"][0]["target_kind"], "skill_contract")
                    self.assertEqual(Path(native_trace["events"][0]["path"]).name, "SKILL.md")
                    self.assertEqual(native_trace["events"][-1]["kind"], "invoke")
                    self.assertEqual(Path(native_trace["events"][-1]["wrapper_path"]).name, "invoke.sh")
                    if case["case_id"] == "complete-normal":
                        self.assertIn("evals/files/context.txt", context)
                        self.assertIn("Representative non-sensitive context", context)
                argv = json.loads(Path(payload["cases"][0]["transcript_locator"]).read_text(encoding="utf-8"))["argv"]
                if adapter == "codex":
                    self.assertIn("exec", argv)
                    self.assertIn("--output-last-message", argv)
                    self.assertEqual(argv[argv.index("--cd") + 1], str(self.repo.resolve()))
                elif adapter in {"claude", "cursor"}:
                    self.assertIn("--print", argv)
                    self.assertIn("--output-format", argv)
                    if adapter == "claude":
                        self.assertIn("--safe-mode", argv)
                        self.assertNotIn("--bare", argv)
                else:
                    self.assertIn("--request", argv)
                    self.assertIn("--context", argv)

    def test_adapter_descriptor_drives_native_command(self) -> None:
        descriptor_path = self.skills / "adapters/eval/shared.json"
        descriptor = json.loads(descriptor_path.read_text(encoding="utf-8"))
        descriptor["native_command"] = "descriptor-selected-native"
        descriptor_path.write_text(json.dumps(descriptor), encoding="utf-8")
        shutil.copyfile(self.skills / "fake-native-cli.py", self.native_bin / "descriptor-selected-native")
        (self.native_bin / "descriptor-selected-native").chmod(0o755)

        result = self.run_cli(
            "run-skill-evals", "--root", str(self.repo), "--mode", "source",
            "--skill", "guru-example-sync", "--adapter", "shared", "--case", "sync-normal",
            "--run-root", str(Path(self.temp.name) / "descriptor-native"), "--json",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "passed")
        transcript = json.loads(Path(payload["cases"][0]["transcript_locator"]).read_text(encoding="utf-8"))
        self.assertEqual(transcript["native_command"], "descriptor-selected-native")
        self.assertEqual(Path(transcript["argv"][0]).name, "descriptor-selected-native")

    def test_cursor_authentication_unavailable_is_unsupported(self) -> None:
        cursor = self.native_bin / "cursor-agent"
        cursor.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
        cursor.chmod(0o755)
        result = self.run_cli(
            "run-skill-evals", "--root", str(self.repo), "--mode", "source",
            "--skill", "guru-example-sync", "--adapter", "cursor", "--case", "sync-normal",
            "--run-root", str(Path(self.temp.name) / "cursor-unsupported"), "--json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "unsupported")

    def test_native_failures_and_adapter_corpus_mismatch_are_execution_errors(self) -> None:
        native = self.native_bin / "guru-team-shared-eval"
        run_arguments = (
            "run-skill-evals", "--root", str(self.repo), "--mode", "source",
            "--skill", "guru-example-sync", "--adapter", "shared", "--case", "sync-normal",
        )

        native.write_text("#!/bin/sh\nexit 7\n", encoding="utf-8")
        native.chmod(0o755)
        launch_failure = self.run_cli(
            *run_arguments, "--run-root", str(Path(self.temp.name) / "launch-failure"), "--json",
        )
        self.assertEqual(json.loads(launch_failure.stdout)["status"], "execution_error")

        native.write_text("#!/bin/sh\nprintf 'not-json\\n'\n", encoding="utf-8")
        native.chmod(0o755)
        malformed = self.run_cli(
            *run_arguments, "--run-root", str(Path(self.temp.name) / "malformed-output"), "--json",
        )
        self.assertEqual(json.loads(malformed.stdout)["status"], "execution_error")

        native.write_text(
            "#!/bin/sh\nprintf '%s\\n' '{\"exit_id\":\"synced\",\"item\":\"alpha\"}'\n",
            encoding="utf-8",
        )
        native.chmod(0o755)
        dto_without_wrapper = self.run_cli(
            *run_arguments, "--run-root", str(Path(self.temp.name) / "dto-without-wrapper"), "--json",
        )
        dto_without_wrapper_payload = json.loads(dto_without_wrapper.stdout)
        self.assertEqual(dto_without_wrapper_payload["status"], "execution_error")
        self.assertEqual(dto_without_wrapper_payload["cases"][0]["deterministic_results"], [])
        self.assertFalse(
            Path(dto_without_wrapper_payload["cases"][0]["transcript_locator"])
            .with_name("native-trace.json")
            .exists()
        )

        shutil.copyfile(self.skills / "fake-native-cli.py", native)
        native.chmod(0o755)
        adapter_runtime = self.skills / "adapters/eval/native_adapter.py"
        adapter_text = adapter_runtime.read_text(encoding="utf-8")
        adapter_runtime.write_text(
            adapter_text.replace(
                '"corpus_sha256": corpus_sha256,',
                '"corpus_sha256": "0" * 64,',
                1,
            ),
            encoding="utf-8",
        )
        corpus_mismatch = self.run_cli(
            *run_arguments, "--run-root", str(Path(self.temp.name) / "corpus-mismatch"), "--json",
        )
        corpus_mismatch_payload = json.loads(corpus_mismatch.stdout)
        self.assertEqual(corpus_mismatch_payload["status"], "execution_error")
        self.assertEqual(
            corpus_mismatch_payload["cases"][0]["deterministic_results"],
            [{"id": "corpus-byte-identity", "passed": False, "detail": "adapter corpus bytes mismatch"}],
        )

    def test_four_native_platforms_cannot_read_evals_or_private_runtime_from_projection(self) -> None:
        commands = {
            "shared": "guru-team-shared-eval", "codex": "codex",
            "claude": "claude", "cursor": "cursor-agent",
        }
        for adapter, command in commands.items():
            with self.subTest(adapter=adapter):
                result = self.run_cli(
                    "run-skill-evals", "--root", str(self.repo), "--mode", "source",
                    "--skill", "guru-example-sync", "--adapter", adapter,
                    "--case", "sync-normal", "--run-root",
                    str(Path(self.temp.name) / f"projection-access-{adapter}"), "--json",
                    native_direct_read="both",
                )
                payload = json.loads(result.stdout)
                self.assertEqual(payload["status"], "execution_error")
                self.assertEqual(payload["cases"][0]["deterministic_results"], [])
                transcript = json.loads(Path(payload["cases"][0]["transcript_locator"]).read_text(encoding="utf-8"))
                self.assertEqual(Path(transcript["argv"][0]).name, command)
                projection_root = Path(transcript["projection_root"])
                self.assertFalse((projection_root / "evals/evals.json").exists())
                self.assertFalse((projection_root / "runtime/guru_team_trellis.py").exists())
                self.assertIn("native_projection_access_denied", transcript["stderr"])
                self.assertIn(str(projection_root / "evals/evals.json"), transcript["stderr"])
                self.assertIn(str(projection_root / "runtime/guru_team_trellis.py"), transcript["stderr"])
                trace = json.loads(Path(transcript["native_trace_path"]).read_text(encoding="utf-8"))
                self.assertEqual([event["kind"] for event in trace["events"]], ["read"])
                self.assertEqual(Path(trace["events"][0]["path"]), projection_root / "SKILL.md")

    def test_all_native_output_envelopes_require_verified_wrapper_receipt(self) -> None:
        script = (
            "#!/usr/bin/env python3\n"
            "import json, sys\n"
            "from pathlib import Path\n"
            "dto = '{\\\"exit_id\\\":\\\"synced\\\",\\\"item\\\":\\\"alpha\\\"}'\n"
            "command = Path(sys.argv[0]).name\n"
            "if command == 'codex':\n"
            "    output = Path(sys.argv[sys.argv.index('--output-last-message') + 1])\n"
            "    output.write_text(dto, encoding='utf-8')\n"
            "    print(json.dumps({'type': 'turn.completed'}))\n"
            "elif command in {'claude', 'cursor-agent'}:\n"
            "    print(json.dumps({'result': dto}))\n"
            "else:\n"
            "    print(dto)\n"
        )
        commands = {
            "shared": "guru-team-shared-eval", "codex": "codex",
            "claude": "claude", "cursor": "cursor-agent",
        }
        for adapter, command in commands.items():
            with self.subTest(adapter=adapter):
                native = self.native_bin / command
                native.write_text(script, encoding="utf-8")
                native.chmod(0o755)
                result = self.run_cli(
                    "run-skill-evals", "--root", str(self.repo), "--mode", "source",
                    "--skill", "guru-example-sync", "--adapter", adapter,
                    "--case", "sync-normal", "--run-root",
                    str(Path(self.temp.name) / f"dto-without-receipt-{adapter}"), "--json",
                )
                payload = json.loads(result.stdout)
                self.assertEqual(payload["status"], "execution_error")
                self.assertEqual(payload["cases"][0]["deterministic_results"], [])

    def test_semantic_feedback_status_unsupported_comparison_and_run_root_boundaries(self) -> None:
        missing_grade = self.run_cli(
            "run-skill-evals", "--root", str(self.repo), "--mode", "source", "--skill", "guru-example-action",
            "--adapter", "shared", "--case", "complete-normal", "--run-root", str(Path(self.temp.name) / "missing-grade"),
            "--human-feedback", str(self.skills / "human-feedback.json"), "--json",
        )
        self.assertEqual(json.loads(missing_grade.stdout)["status"], "evaluation_failed")

        unsupported = self.run_cli(
            "run-skill-evals", "--root", str(self.repo), "--mode", "source", "--skill", "guru-example-sync",
            "--adapter", "shared", "--run-root", str(Path(self.temp.name) / "unsupported"), "--json", native=False,
        )
        self.assertEqual(json.loads(unsupported.stdout)["status"], "unsupported")
        unavailable_discovery = self.run_cli(
            "discover-skill-evals", "--root", str(self.repo), "--mode", "source",
            "--skill", "guru-example-sync", "--json", native=False,
        )
        shared = next(item for item in json.loads(unavailable_discovery.stdout)["adapters"] if item["id"] == "shared")
        self.assertFalse(shared["native_available"])

        package = self.skills / "packages/guru-example-sync"
        comparison = self.run_cli(
            "run-skill-evals", "--root", str(self.repo), "--mode", "source", "--skill", "guru-example-sync",
            "--adapter", "shared", "--run-root", str(Path(self.temp.name) / "comparison"),
            "--current-package", str(package), "--comparison-package", str(package),
            "--json",
        )
        comparison_payload = json.loads(comparison.stdout)
        self.assertEqual(comparison_payload["status"], "passed")
        self.assertEqual({item["comparison_side"] for item in comparison_payload["cases"]}, {"current", "comparison"})

        semantic_package = self.skills / "packages/guru-example-action"
        comparison_grading = Path(self.temp.name) / "comparison-grading.json"
        comparison_grading.write_text(json.dumps({
            "schema_version": "1.0",
            "results": [
                {"case_id": "complete-normal", "comparison_side": "current", "assertion_id": "completion-is-relevant", "passed": True, "summary": "Current package passed."},
                {"case_id": "complete-normal", "comparison_side": "comparison", "assertion_id": "completion-is-relevant", "passed": False, "summary": "Comparison package failed."},
            ],
        }), encoding="utf-8")
        semantic_comparison = self.run_cli(
            "run-skill-evals", "--root", str(self.repo), "--mode", "source", "--skill", "guru-example-action",
            "--adapter", "shared", "--case", "complete-normal", "--run-root", str(Path(self.temp.name) / "semantic-comparison"),
            "--semantic-grading", str(comparison_grading), "--current-package", str(semantic_package),
            "--comparison-package", str(semantic_package), "--json",
        )
        semantic_payload = json.loads(semantic_comparison.stdout)
        self.assertEqual(semantic_payload["status"], "evaluation_failed")
        self.assertEqual(
            {item["comparison_side"]: item["semantic_results"][0]["passed"] for item in semantic_payload["cases"]},
            {"current": True, "comparison": False},
        )

        one_sided = self.run_cli(
            "run-skill-evals", "--root", str(self.repo), "--mode", "source", "--skill", "guru-example-sync",
            "--adapter", "shared", "--run-root", str(Path(self.temp.name) / "one-sided"),
            "--current-package", str(package), "--json",
        )
        self.assertEqual(json.loads(one_sided.stderr)["code"], "eval_comparison_pair_required")

        internal = self.run_cli(
            "run-skill-evals", "--root", str(self.repo), "--mode", "source", "--skill", "guru-example-sync",
            "--adapter", "shared", "--run-root", str(self.repo / "eval-output"), "--json",
        )
        self.assertEqual(json.loads(internal.stderr)["code"], "eval_run_root_inside_repo")

        external_package = Path(self.temp.name) / "external-package"
        shutil.copytree(package, external_package)
        comparison_run_root = external_package / "eval-output"
        inside_comparison = self.run_cli(
            "run-skill-evals", "--root", str(self.repo), "--mode", "source", "--skill", "guru-example-sync",
            "--adapter", "shared", "--run-root", str(comparison_run_root),
            "--current-package", str(external_package), "--comparison-package", str(external_package), "--json",
        )
        self.assertEqual(json.loads(inside_comparison.stderr)["code"], "eval_run_root_inside_package")
        self.assertFalse(comparison_run_root.exists())

    def test_four_adapters_share_runner_runtime_target_for_external_exact_comparison(self) -> None:
        current_package = self.skills / "packages/guru-example-sync"
        comparison_package = Path(self.temp.name) / "exact-comparison/guru-example-sync"
        shutil.copytree(current_package, comparison_package)
        for adapter in ("shared", "codex", "claude", "cursor"):
            with self.subTest(adapter=adapter):
                run_root = Path(self.temp.name) / f"external-comparison-{adapter}"
                result = self.run_cli(
                    "run-skill-evals", "--root", str(self.repo), "--mode", "source",
                    "--skill", "guru-example-sync", "--adapter", adapter,
                    "--current-package", str(current_package),
                    "--comparison-package", str(comparison_package),
                    "--run-root", str(run_root), "--json",
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                payload = json.loads(result.stdout)
                self.assertEqual(payload["status"], "passed")
                self.assertEqual({case["comparison_side"] for case in payload["cases"]}, {"current", "comparison"})
                self.assertTrue(all(case["status"] == "passed" for case in payload["cases"]))
                for case in payload["cases"]:
                    transcript_path = Path(case["transcript_locator"])
                    transcript = json.loads(transcript_path.read_text(encoding="utf-8"))
                    private_request = json.loads((transcript_path.parent / "adapter-request.json").read_text(encoding="utf-8"))
                    native_request = json.loads(Path(transcript["native_request_path"]).read_text(encoding="utf-8"))
                    context = Path(transcript["context_path"]).read_text(encoding="utf-8")
                    protocol = Path(transcript["protocol_path"]).read_text(encoding="utf-8")
                    native_trace = Path(transcript["native_trace_path"]).read_text(encoding="utf-8")
                    boundary = Path(transcript["protocol_path"]).with_name("public-invocation-boundary.sh")
                    boundary_text = boundary.read_text(encoding="utf-8")
                    projection_root = Path(transcript["projection_root"])
                    runtime_locator = private_request["runtime_target"]
                    self.assertEqual(Path(runtime_locator).resolve(), self.runtime_target.resolve())
                    self.assertNotIn("runtime_target", native_request)
                    self.assertNotIn(runtime_locator, json.dumps(native_request))
                    self.assertNotIn(runtime_locator, json.dumps(transcript["argv"]))
                    self.assertNotIn(runtime_locator, context)
                    self.assertNotIn(runtime_locator, protocol)
                    self.assertNotIn(runtime_locator, native_trace)
                    self.assertNotIn(runtime_locator, boundary_text)
                    self.assertNotIn("guru_team_trellis.py", boundary_text)
                    self.assertFalse(any(
                        runtime_locator.encode("utf-8") in path.read_bytes()
                        for path in projection_root.rglob("*") if path.is_file()
                    ))

    def test_comparison_uses_each_valid_side_wrapper_and_fails_closed_on_side_drift(self) -> None:
        current_package = self.skills / "packages/guru-example-sync"
        comparison_package = Path(self.temp.name) / "different-wrapper/guru-example-sync"
        shutil.copytree(current_package, comparison_package)
        old_wrapper = comparison_package / "scripts/invoke.sh"
        new_wrapper = comparison_package / "scripts/invoke-v2.sh"
        old_wrapper.rename(new_wrapper)
        interface_path = comparison_package / "interface.json"
        interface = json.loads(interface_path.read_text(encoding="utf-8"))
        interface["validators"][0]["command"] = "scripts/invoke-v2.sh"
        interface["public_contracts"]["invocation"]["wrapper"] = "scripts/invoke-v2.sh"
        interface_path.write_text(json.dumps(interface), encoding="utf-8")

        run_root = Path(self.temp.name) / "different-wrapper-run"
        result = self.run_cli(
            "run-skill-evals", "--root", str(self.repo), "--mode", "source",
            "--skill", "guru-example-sync", "--adapter", "shared", "--case", "sync-normal",
            "--current-package", str(current_package),
            "--comparison-package", str(comparison_package),
            "--run-root", str(run_root), "--json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "passed")
        wrappers = {
            case["comparison_side"]: Path(json.loads(
                Path(case["transcript_locator"]).read_text(encoding="utf-8")
            )["wrapper_path"]).name
            for case in payload["cases"]
        }
        self.assertEqual(wrappers, {"current": "invoke.sh", "comparison": "invoke-v2.sh"})

        missing_outputs = Path(self.temp.name) / "missing-outputs/guru-example-sync"
        shutil.copytree(current_package, missing_outputs)
        missing_outputs_interface_path = missing_outputs / "interface.json"
        missing_outputs_interface = json.loads(missing_outputs_interface_path.read_text(encoding="utf-8"))
        del missing_outputs_interface["public_contracts"]["outputs"]
        missing_outputs_interface_path.write_text(json.dumps(missing_outputs_interface), encoding="utf-8")
        missing_outputs_root = Path(self.temp.name) / "missing-outputs-run"
        missing_outputs_result = self.run_cli(
            "run-skill-evals", "--root", str(self.repo), "--mode", "source",
            "--skill", "guru-example-sync", "--adapter", "shared",
            "--current-package", str(current_package),
            "--comparison-package", str(missing_outputs),
            "--run-root", str(missing_outputs_root), "--json",
        )
        self.assertEqual(missing_outputs_result.returncode, 2)
        self.assertEqual(json.loads(missing_outputs_result.stderr)["code"], "eval_side_interface_invalid")
        self.assertNotIn("Traceback", missing_outputs_result.stderr)
        self.assertFalse(missing_outputs_root.exists())

        action_package = self.skills / "packages/guru-example-action"
        missing_fixture = Path(self.temp.name) / "missing-fixture/guru-example-action"
        shutil.copytree(action_package, missing_fixture)
        (missing_fixture / "evals/files/context.txt").unlink()
        missing_fixture_root = Path(self.temp.name) / "missing-fixture-run"
        missing_fixture_result = self.run_cli(
            "run-skill-evals", "--root", str(self.repo), "--mode", "source",
            "--skill", "guru-example-action", "--adapter", "shared",
            "--current-package", str(action_package),
            "--comparison-package", str(missing_fixture),
            "--run-root", str(missing_fixture_root), "--json",
        )
        self.assertEqual(missing_fixture_result.returncode, 2)
        self.assertEqual(json.loads(missing_fixture_result.stderr)["code"], "eval_fixture_invalid")
        self.assertNotIn("Traceback", missing_fixture_result.stderr)
        self.assertFalse(missing_fixture_root.exists())

    def test_normal_public_wrappers_do_not_reference_eval_or_private_runtime_source(self) -> None:
        for skill_id in ("guru-example-action", "guru-example-sync"):
            wrapper = (self.skills / "packages" / skill_id / "scripts/invoke.sh").read_text(encoding="utf-8")
            self.assertNotIn("evals/", wrapper)
            self.assertNotIn("guru_team_trellis.py", wrapper)

    def test_installed_runner_consumes_managed_descriptor_executable(self) -> None:
        destination = self.repo / ".trellis/guru-team"
        result = preset.install_skill_packages(
            self.repo,
            self.repo,
            destination,
            {"codex", "cursor", "claude"},
            None,
        )
        (self.repo / ".trellis/workflow.md").write_bytes((self.skills / "workflow.md").read_bytes())
        extension = json.loads((self.skills / "extension.json").read_text(encoding="utf-8"))
        (destination / "extension.json").write_text(
            json.dumps({"extension": extension, "skill_packages": result}),
            encoding="utf-8",
        )
        run = self.run_cli(
            "run-skill-evals", "--root", str(self.repo), "--mode", "installed",
            "--skill", "guru-example-sync", "--adapter", "codex", "--case", "sync-normal",
            "--run-root", str(Path(self.temp.name) / "installed-run"), "--json",
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        payload = json.loads(run.stdout)
        self.assertEqual(payload["status"], "passed")
        transcript = json.loads(Path(payload["cases"][0]["transcript_locator"]).read_text(encoding="utf-8"))
        self.assertEqual(Path(transcript["argv"][0]).name, "codex")
        self.assertTrue(os.access(destination / "skills/adapters/eval/codex.sh", os.X_OK))
        for platform in (".agents", ".codex", ".cursor", ".claude"):
            self.assertTrue((self.repo / platform / "skills/guru-example-sync/evals/evals.json").is_file())


class DistributionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name) / "target"
        (self.repo / ".trellis").mkdir(parents=True)
        self.guru_root = Path(self.temp.name) / "source"
        canonical = self.guru_root / "trellis/skills/guru-team"
        shutil.copytree(FIXTURE, canonical)
        self.dst = self.repo / ".trellis/guru-team"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def install(self, platforms: set[str], previous: dict | None = None) -> dict:
        return preset.install_skill_packages(self.repo, self.guru_root, self.dst, platforms, previous)

    def manifest(self, result: dict) -> dict:
        extension = json.loads((FIXTURE / "extension.json").read_text(encoding="utf-8"))
        return {"extension": extension, "skill_packages": result}

    def write_installed_manifest(self, result: dict) -> Path:
        canonical = self.guru_root / "trellis/skills/guru-team"
        (self.repo / ".trellis/workflow.md").write_bytes((canonical / "workflow.md").read_bytes())
        manifest_path = self.dst / "extension.json"
        manifest_path.write_text(json.dumps(self.manifest(result)), encoding="utf-8")
        return manifest_path

    def validate_installed(self, result: dict) -> dict:
        manifest_path = self.write_installed_manifest(result)
        return runtime.validate_skill_installed(
            self.repo,
            self.dst / "skills",
            self.repo / ".trellis/workflow.md",
            manifest_path,
        )

    def test_missing_and_platform_selection(self) -> None:
        result = self.install({"codex"})
        self.assertEqual(result["status"], "ok")
        self.assertTrue((self.repo / ".agents/skills/guru-example-action/SKILL.md").is_file())
        self.assertTrue((self.repo / ".codex/skills/guru-example-action/SKILL.md").is_file())
        self.assertTrue((self.repo / ".agents/skills/guru-example-action/tests/test_contract.py").is_file())
        self.assertTrue((self.repo / ".codex/skills/guru-example-action/tests/test_contract.py").is_file())
        self.assertTrue(os.access(self.repo / ".codex/skills/guru-example-action/scripts/invoke.sh", os.X_OK))
        self.assertFalse((self.repo / ".cursor/skills/guru-example-action").exists())
        self.assertFalse((self.repo / ".claude/skills/guru-example-action").exists())
        self.assertTrue(all(item["action"] == "installed" for item in result["files"]))
        self.assertTrue(any(item["source"].endswith("tests/test_contract.py") for item in result["files"]))
        for adapter_id in ("shared", "codex", "claude", "cursor"):
            descriptor = json.loads((self.dst / f"skills/adapters/eval/{adapter_id}.json").read_text(encoding="utf-8"))
            executable = self.dst / "skills/adapters/eval" / descriptor["executable"]
            self.assertTrue(executable.is_file())
            self.assertTrue(os.access(executable, os.X_OK))

    def test_python_cache_is_not_a_managed_package_asset(self) -> None:
        cache = self.guru_root / "trellis/skills/guru-team/packages/guru-example-action/tests/__pycache__"
        cache.mkdir(exist_ok=True)
        (cache / "test_contract.cpython-312.pyc").write_bytes(b"generated bytecode")

        result = self.install({"codex"})

        self.assertEqual(result["status"], "ok")
        self.assertFalse((self.repo / ".trellis/guru-team/skills/packages/guru-example-action/tests/__pycache__").exists())
        self.assertFalse((self.repo / ".agents/skills/guru-example-action/tests/__pycache__").exists())
        self.assertTrue(all("__pycache__" not in item["path"] for item in result["files"]))
        self.assertEqual(self.validate_installed(result)["status"], "passed")

    def test_unchanged_reapply(self) -> None:
        first = self.install({"codex", "cursor", "claude"})
        second = self.install({"codex", "cursor", "claude"}, self.manifest(first))
        self.assertEqual(second["status"], "ok")
        self.assertTrue(all(item["action"] == "unchanged" for item in second["files"]))
        for platform in (".agents", ".codex", ".cursor", ".claude"):
            self.assertTrue((self.repo / platform / "skills/guru-example-action/SKILL.md").is_file())

    def test_selected_but_unsupported_platform_is_not_created(self) -> None:
        canonical = self.guru_root / "trellis/skills/guru-team"
        registry_path = canonical / "registry.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        action_entry = next(item for item in registry["skills"] if item["id"] == "guru-example-action")
        action_entry["supported_platforms"] = ["shared", "codex"]
        registry_path.write_text(json.dumps(registry), encoding="utf-8")
        interface_path = canonical / "packages/guru-example-action/interface.json"
        interface = json.loads(interface_path.read_text(encoding="utf-8"))
        interface["platform_destinations"] = ["shared", "codex"]
        interface_path.write_text(json.dumps(interface), encoding="utf-8")
        result = self.install({"codex", "cursor"})
        self.assertFalse((self.repo / ".cursor/skills/guru-example-action").exists())
        (self.repo / ".trellis/workflow.md").write_bytes((canonical / "workflow.md").read_bytes())
        manifest_path = self.dst / "extension.json"
        manifest_path.write_text(json.dumps(self.manifest(result)), encoding="utf-8")
        valid = runtime.validate_skill_installed(
            self.repo, self.dst / "skills", self.repo / ".trellis/workflow.md", manifest_path
        )
        self.assertEqual(valid["status"], "passed", valid["errors"])

    def test_known_managed_upgrade_writes_backup_then_new_bytes(self) -> None:
        first = self.install({"codex"})
        source = self.guru_root / "trellis/skills/guru-team/packages/guru-example-action/SKILL.md"
        source.write_text(source.read_text(encoding="utf-8") + "\nknown upgrade\n", encoding="utf-8")
        second = self.install({"codex"}, self.manifest(first))
        target = self.repo / ".agents/skills/guru-example-action/SKILL.md"
        self.assertEqual(target.read_bytes(), source.read_bytes())
        self.assertTrue(target.with_name("SKILL.md.bak").is_file())
        self.assertIn(".agents/skills/guru-example-action/SKILL.md.bak", second["sidecars"])

    def test_known_upgrade_reapply_preserves_backup_gate_until_sidecars_are_removed(self) -> None:
        first = self.install({"codex"})
        source = self.guru_root / "trellis/skills/guru-team/packages/guru-example-action/SKILL.md"
        source.write_text(source.read_text(encoding="utf-8") + "\nknown upgrade\n", encoding="utf-8")

        upgraded = self.install({"codex"}, self.manifest(first))
        self.assertEqual(upgraded["status"], "conflict")
        self.assertEqual(upgraded["conflicts"], [])
        self.assertTrue(upgraded["sidecars"])

        still_blocked = self.install({"codex"}, self.manifest(upgraded))
        self.assertEqual(still_blocked["status"], "conflict")
        self.assertEqual(still_blocked["conflicts"], [])
        self.assertEqual(still_blocked["sidecars"], upgraded["sidecars"])

        for sidecar in still_blocked["sidecars"]:
            (self.repo / sidecar).unlink()
        recovered = self.install({"codex"}, self.manifest(still_blocked))
        self.assertEqual(recovered["status"], "ok", recovered["conflicts"])
        self.assertEqual(recovered["conflicts"], [])
        self.assertEqual(recovered["sidecars"], [])
        self.assertTrue(all(item["action"] == "unchanged" for item in recovered["files"]))
        self.assertEqual(self.validate_installed(recovered)["status"], "passed")

    def test_unknown_local_edit_is_preserved_and_gets_new_copy(self) -> None:
        first = self.install({"codex"})
        target = self.repo / ".agents/skills/guru-example-action/SKILL.md"
        target.write_text("local edit\n", encoding="utf-8")
        second = self.install({"codex"}, self.manifest(first))
        self.assertEqual(target.read_text(encoding="utf-8"), "local edit\n")
        self.assertEqual(target.with_name("SKILL.md.new").read_bytes(), (self.guru_root / "trellis/skills/guru-team/packages/guru-example-action/SKILL.md").read_bytes())
        self.assertEqual(second["status"], "conflict")

        reapplied = self.install({"codex"}, self.manifest(second))
        self.assertEqual(reapplied["status"], "conflict")
        self.assertTrue(any(
            item["reason"] == "invalid_previous_provenance"
            for item in reapplied["conflicts"]
        ))

    def test_invalid_provenance_is_preserved_and_gets_new_copy(self) -> None:
        first = self.install({"codex"})
        previous = self.manifest(first)
        previous["skill_packages"]["files"][0]["sha256"] = "invalid"
        target = self.repo / ".agents/skills/guru-example-action/SKILL.md"
        target.write_text("local edit\n", encoding="utf-8")
        second = self.install({"codex"}, previous)
        self.assertEqual(target.read_text(encoding="utf-8"), "local edit\n")
        self.assertTrue(target.with_name("SKILL.md.new").is_file())
        self.assertEqual(second["status"], "conflict")

    def test_target_regular_symlink_is_rejected_without_external_write(self) -> None:
        external = Path(self.temp.name) / "external-skill.md"
        external.write_text("external\n", encoding="utf-8")
        target = self.repo / ".agents/skills/guru-example-action/SKILL.md"
        target.parent.mkdir(parents=True)
        target.symlink_to(external)
        result = self.install({"codex"})
        self.assertEqual(result["status"], "conflict")
        self.assertEqual(external.read_text(encoding="utf-8"), "external\n")

    def test_target_dangling_symlink_is_rejected_without_external_create(self) -> None:
        external = Path(self.temp.name) / "missing-external.md"
        target = self.repo / ".agents/skills/guru-example-action/SKILL.md"
        target.parent.mkdir(parents=True)
        target.symlink_to(external)
        result = self.install({"codex"})
        self.assertEqual(result["status"], "conflict")
        self.assertFalse(external.exists())

    def test_external_ancestor_symlink_is_rejected_without_external_write(self) -> None:
        external = Path(self.temp.name) / "external-root"
        external.mkdir()
        (self.repo / ".agents").symlink_to(external, target_is_directory=True)
        result = self.install({"codex"})
        self.assertEqual(result["status"], "conflict")
        self.assertEqual(list(external.iterdir()), [])

    def test_internal_ancestor_symlink_is_rejected_without_internal_write(self) -> None:
        internal = self.repo / "internal-root"
        internal.mkdir()
        (self.repo / ".agents").symlink_to(internal, target_is_directory=True)
        result = self.install({"codex"})
        self.assertEqual(result["status"], "conflict")
        self.assertEqual(list(internal.iterdir()), [])

    def test_dangling_ancestor_symlink_is_rejected_without_target_create(self) -> None:
        missing = Path(self.temp.name) / "missing-root"
        (self.repo / ".agents").symlink_to(missing, target_is_directory=True)
        result = self.install({"codex"})
        self.assertEqual(result["status"], "conflict")
        self.assertFalse(missing.exists())

    def test_multilevel_ancestor_symlink_is_rejected_without_external_write(self) -> None:
        external = Path(self.temp.name) / "external-root"
        external.mkdir()
        intermediate = Path(self.temp.name) / "intermediate-root"
        intermediate.symlink_to(external, target_is_directory=True)
        (self.repo / ".agents").mkdir()
        (self.repo / ".agents/skills").symlink_to(intermediate, target_is_directory=True)
        result = self.install({"codex"})
        self.assertEqual(result["status"], "conflict")
        self.assertEqual(list(external.iterdir()), [])

    def test_known_platform_shrink_removes_previous_managed_files(self) -> None:
        first = self.install({"codex", "cursor", "claude"})
        second = self.install({"codex"}, self.manifest(first))
        self.assertEqual(second["status"], "ok", second["conflicts"])
        self.assertFalse((self.repo / ".cursor/skills/guru-example-action").exists())
        self.assertFalse((self.repo / ".claude/skills/guru-example-action").exists())
        self.assertTrue(any(item["action"] == "removed_managed" for item in second["removals"]))
        self.assertEqual(self.validate_installed(second)["status"], "passed")

    def test_platform_shrink_preserves_unknown_edit_with_new_sidecar(self) -> None:
        first = self.install({"codex", "cursor", "claude"})
        target = self.repo / ".cursor/skills/guru-example-action/SKILL.md"
        target.write_text("local cursor edit\n", encoding="utf-8")
        second = self.install({"codex"}, self.manifest(first))
        self.assertEqual(second["status"], "conflict")
        self.assertEqual(target.read_text(encoding="utf-8"), "local cursor edit\n")
        self.assertTrue(target.with_name("SKILL.md.new").is_file())
        self.assertTrue(any(item["reason"] == "stale_unknown_local_edit" for item in second["conflicts"]))

    def test_platform_shrink_invalid_provenance_preserves_files(self) -> None:
        first = self.install({"codex", "cursor", "claude"})
        previous = self.manifest(first)
        cursor_record = next(item for item in previous["skill_packages"]["files"] if item["path"].startswith(".cursor/"))
        cursor_record["sha256"] = "invalid"
        second = self.install({"codex"}, previous)
        self.assertEqual(second["status"], "conflict")
        self.assertTrue((self.repo / ".cursor/skills/guru-example-action/SKILL.md").is_file())
        self.assertTrue(any(item["reason"] == "invalid_previous_provenance" for item in second["conflicts"]))
        self.assertTrue(any(item["reason"] == "stale_invalid_provenance" for item in second["conflicts"]))

    def test_platform_shrink_symlink_is_rejected_without_external_read_or_write(self) -> None:
        first = self.install({"codex", "cursor", "claude"})
        external = Path(self.temp.name) / "external-stale.md"
        external.write_text("external stale\n", encoding="utf-8")
        target = self.repo / ".cursor/skills/guru-example-action/SKILL.md"
        target.unlink()
        target.symlink_to(external)
        second = self.install({"codex"}, self.manifest(first))
        self.assertEqual(second["status"], "conflict")
        self.assertEqual(external.read_text(encoding="utf-8"), "external stale\n")
        self.assertTrue(any(item["reason"] == "unsafe_stale_path_boundary" for item in second["conflicts"]))

    def test_installed_validator_detects_drift_and_reserved_install(self) -> None:
        result = self.install({"codex"})
        manifest_path = self.write_installed_manifest(result)
        valid = self.validate_installed(result)
        self.assertEqual(valid["status"], "passed", valid["errors"])
        target = self.repo / ".agents/skills/guru-example-action/SKILL.md"
        target.write_text("drift\n", encoding="utf-8")
        drift = runtime.validate_skill_installed(
            self.repo, self.dst / "skills", self.repo / ".trellis/workflow.md", manifest_path
        )
        self.assertTrue(any("digest drift" in item for item in drift["errors"]))

    def test_installed_validator_requires_unique_matching_consumer_targets(self) -> None:
        original = (self.guru_root / "trellis/skills/guru-team/workflow.md").read_text(
            encoding="utf-8"
        )
        cases = {
            "missing": (
                original.replace(
                    '<!-- guru-workflow-target: {"id":"fixture-next"} -->\n',
                    "",
                ),
                "workflow consumer target fixture-next is not declared",
            ),
            "multiple": (
                original + '<!-- guru-workflow-target: {"id":"fixture-next"} -->\n',
                "workflow consumer target fixture-next has multiple declarations",
            ),
            "kind-mismatch": (
                original.replace(
                    '<!-- guru-workflow-target: {"id":"fixture-next"} -->',
                    '<!-- guru-stop-target: {"id":"fixture-next"} -->',
                ),
                "workflow consumer target fixture-next has a kind mismatch",
            ),
            "dangling": (
                original + '<!-- guru-stop-target: {"id":"unused-stop"} -->\n',
                "stop target unused-stop is dangling",
            ),
        }
        for name, (workflow, expected) in cases.items():
            with self.subTest(name=name):
                result = self.install({"codex"})
                manifest_path = self.write_installed_manifest(result)
                (self.repo / ".trellis/workflow.md").write_text(workflow, encoding="utf-8")
                errors = runtime.validate_skill_installed(
                    self.repo,
                    self.dst / "skills",
                    self.repo / ".trellis/workflow.md",
                    manifest_path,
                )["errors"]
                self.assertIn(expected, errors)

    def test_installed_validator_rejects_missing_file_record(self) -> None:
        result = self.install({"codex"})
        result["files"].pop()
        errors = self.validate_installed(result)["errors"]
        self.assertTrue(any("file provenance inventory is incomplete" in item for item in errors))

    def test_installed_validator_rejects_missing_package_record(self) -> None:
        result = self.install({"codex"})
        result["packages"] = []
        errors = self.validate_installed(result)["errors"]
        self.assertTrue(any("package provenance inventory is incomplete" in item for item in errors))

    def test_installed_validator_rejects_unknown_platform_skill_copy(self) -> None:
        result = self.install({"codex"})
        unknown = self.repo / ".codex/skills/guru-unknown-action"
        shutil.copytree(self.repo / ".codex/skills/guru-example-action", unknown)
        errors = self.validate_installed(result)["errors"]
        self.assertTrue(any("unknown codex workflow skill copy" in item for item in errors))

    def test_installed_validator_rejects_unregistered_sidecar(self) -> None:
        result = self.install({"codex"})
        sidecar = self.repo / ".agents/skills/guru-example-action/SKILL.md.new"
        sidecar.write_text("unregistered sidecar\n", encoding="utf-8")
        errors = self.validate_installed(result)["errors"]
        self.assertTrue(any("sidecar inventory is incomplete" in item for item in errors))

    def test_installed_validator_rejects_platform_ancestor_symlink(self) -> None:
        result = self.install({"codex"})
        external = Path(self.temp.name) / "external-runtime"
        shutil.copytree(self.repo / ".agents", external)
        shutil.rmtree(self.repo / ".agents")
        (self.repo / ".agents").symlink_to(external, target_is_directory=True)
        errors = self.validate_installed(result)["errors"]
        self.assertTrue(any("symlink component" in item for item in errors))

    def test_installed_validator_rejects_target_symlink_without_external_read(self) -> None:
        result = self.install({"codex"})
        external = Path(self.temp.name) / "external-runtime-file"
        external.write_text("external runtime\n", encoding="utf-8")
        target = self.repo / ".agents/skills/guru-example-action/SKILL.md"
        target.unlink()
        target.symlink_to(external)
        errors = self.validate_installed(result)["errors"]
        self.assertTrue(any("symlink component" in item for item in errors))
        self.assertEqual(external.read_text(encoding="utf-8"), "external runtime\n")

    def test_installed_validator_rejects_dangling_target_symlink(self) -> None:
        result = self.install({"codex"})
        external = Path(self.temp.name) / "missing-runtime-file"
        target = self.repo / ".agents/skills/guru-example-action/SKILL.md"
        target.unlink()
        target.symlink_to(external)
        errors = self.validate_installed(result)["errors"]
        self.assertTrue(any("symlink component" in item for item in errors))
        self.assertFalse(external.exists())

    def test_installed_validator_rejects_unknown_platform_root(self) -> None:
        result = self.install({"codex"})
        unknown = self.repo / ".opencode/skills/guru-example-action"
        shutil.copytree(self.repo / ".codex/skills/guru-example-action", unknown)
        errors = self.validate_installed(result)["errors"]
        self.assertTrue(any("unknown platform root" in item for item in errors))

    def test_installed_manifest_symlink_is_rejected_without_external_json_read(self) -> None:
        result = self.install({"codex"})
        manifest = self.write_installed_manifest(result)
        external = Path(self.temp.name) / "external-invalid-manifest.json"
        external.write_text("{invalid external", encoding="utf-8")
        manifest.unlink()
        manifest.symlink_to(external)
        errors = runtime.validate_skill_installed(
            self.repo,
            self.dst / "skills",
            self.repo / ".trellis/workflow.md",
            manifest,
        )["errors"]
        self.assertTrue(any("symlink component" in item for item in errors))
        self.assertFalse(any("invalid JSON" in item for item in errors))


class RuntimeDispatcherTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name) / "target"
        (self.repo / ".trellis").mkdir(parents=True)
        (self.repo / ".trellis/workflow.md").write_bytes(
            (REPO / "trellis/workflows/guru-team/workflow.md").read_bytes()
        )
        preset.install_assets(
            REPO / "trellis/workflows/guru-team",
            self.repo / ".trellis/guru-team",
            self.repo,
            {"codex"},
        )
        self.runtime_file = self.repo / ".trellis/guru-team/scripts/python/guru_team_trellis.py"
        self.package_root = self.repo / ".agents/skills/guru-create-task-commit"
        self.manifest_path = self.repo / ".trellis/guru-team/extension.json"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def assert_runtime_blocked(self, validator: str = "candidate_validator") -> None:
        with self.assertRaises(runtime.WorkflowError) as raised:
            runtime.resolve_skill_runtime_command(
                str(self.package_root),
                validator,
                runtime_file=self.runtime_file,
            )
        self.assertEqual(raised.exception.exit_code, 2)
        self.assertIn("not self-contained or portable", str(raised.exception))
        self.assertIn("Install or upgrade the complete Guru Team preset", str(raised.exception))

    def test_full_install_resolves_standalone_discovery_command(self) -> None:
        (self.repo / ".trellis/workflow.md").write_text("# Unrelated active workflow\n", encoding="utf-8")
        installed_gate = runtime.validate_skill_installed(
            self.repo,
            self.repo / ".trellis/guru-team/skills",
            self.repo / ".trellis/workflow.md",
            self.manifest_path,
        )
        self.assertEqual(installed_gate["status"], "failed")
        self.assertTrue(any("mandatory invoke" in item for item in installed_gate["errors"]))
        command, identity = runtime.resolve_skill_runtime_command(
            str(self.package_root),
            "candidate_validator",
            runtime_file=self.runtime_file,
        )
        self.assertEqual(command, self.repo / ".trellis/guru-team/scripts/bash/check-commit-messages.sh")
        self.assertEqual(identity, ["shared", "guru-create-task-commit"])

    def test_missing_manifest_and_dispatcher_fail_closed(self) -> None:
        self.manifest_path.unlink()
        self.assert_runtime_blocked()

        preset.install_assets(
            REPO / "trellis/workflows/guru-team",
            self.repo / ".trellis/guru-team",
            self.repo,
            {"codex"},
        )
        (self.repo / ".trellis/guru-team/scripts/bash/run-skill-command.sh").unlink()
        self.assert_runtime_blocked()

    def test_api_dependency_command_and_discovery_drift_fail_closed(self) -> None:
        original_manifest = self.manifest_path.read_bytes()
        manifest = json.loads(original_manifest.decode("utf-8"))
        manifest["extension"]["public_api"]["skill_runtime"]["api_version"] = "2.0"
        self.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        self.assert_runtime_blocked()

        self.manifest_path.write_bytes(original_manifest)
        interface_path = self.package_root / "interface.json"
        original_interface = interface_path.read_bytes()
        interface = json.loads(original_interface.decode("utf-8"))
        interface["runtime_dependency"]["extension_id"] = "other-extension"
        interface_path.write_text(json.dumps(interface), encoding="utf-8")
        self.assert_runtime_blocked()

        interface_path.write_bytes(original_interface)
        interface = json.loads(original_interface.decode("utf-8"))
        interface["validators"][0]["runtime_command"] = "unknown-command"
        interface_path.write_text(json.dumps(interface), encoding="utf-8")
        self.assert_runtime_blocked()

        interface_path.write_bytes(original_interface + b"\n")
        self.assert_runtime_blocked()


class ReservedInstalledValidationTests(unittest.TestCase):
    def test_reserved_runtime_copy_fails_installed_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            installed_root = repo / ".trellis/guru-team/skills"
            installed_root.mkdir(parents=True)
            for relative in (
                "registry.json",
                "schemas/skill-registry.schema.json",
                "schemas/skill-interface.schema.json",
            ):
                source = SKILLS_ROOT / relative
                target = installed_root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
            workflow = repo / ".trellis/workflow.md"
            workflow.write_bytes((REPO / "trellis/workflows/guru-team/workflow.md").read_bytes())
            records = []
            for path in sorted(item for item in installed_root.rglob("*") if item.is_file()):
                records.append({
                    "path": path.relative_to(repo).as_posix(),
                    "source": f"trellis/skills/guru-team/{path.relative_to(installed_root).as_posix()}",
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "executable": False,
                    "action": "installed",
                })
            skill_manifest = {
                "schema_version": "1.0",
                "status": "ok",
                "canonical_registry_sha256": hashlib.sha256((installed_root / "registry.json").read_bytes()).hexdigest(),
                "registry_schema_version": "1.0",
                "reserved_ids": ["guru-create-work-commit"],
                "active_ids": [],
                "selected_platforms": ["codex"],
                "packages": [],
                "files": records,
                "sidecars": [],
            }
            manifest = repo / ".trellis/guru-team/extension.json"
            manifest.write_text(json.dumps({
                "extension": json.loads((REPO / "trellis/guru-team-extension.json").read_text(encoding="utf-8")),
                "skill_packages": skill_manifest,
            }), encoding="utf-8")
            forbidden = repo / ".agents/skills/guru-create-work-commit/SKILL.md"
            forbidden.parent.mkdir(parents=True)
            forbidden.write_text("reserved must not install\n", encoding="utf-8")
            result = runtime.validate_skill_installed(repo, installed_root, workflow, manifest)
            self.assertTrue(any("reserved skill guru-create-work-commit was installed" in item for item in result["errors"]))


class ProductionDistributionTests(unittest.TestCase):
    def test_active_packages_install_to_all_selected_roots(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            (repo / ".trellis").mkdir()
            workflow = repo / ".trellis/workflow.md"
            workflow.write_bytes((REPO / "trellis/workflows/guru-team/workflow.md").read_bytes())
            dst = repo / ".trellis/guru-team"

            result = preset.install_skill_packages(repo, REPO, dst, {"codex", "cursor", "claude"}, None)
            self.assertEqual(result["status"], "ok")
            self.assertEqual(result["reserved_ids"], ["guru-create-work-commit"])
            self.assertEqual(result["active_ids"], ["guru-approve-task-plan", "guru-check-task", "guru-clarify-requirements", "guru-create-task-commit", "guru-create-task-workspace", "guru-discover-change-context", "guru-review-change-request", "guru-review-contract-wording", "guru-sync-base"])
            self.assertFalse((repo / ".agents/skills/guru-create-work-commit").exists())
            for root in (".agents", ".codex", ".cursor", ".claude"):
                task_commit = repo / root / "skills/guru-create-task-commit"
                self.assertTrue((task_commit / "SKILL.md").is_file())
                self.assertTrue((task_commit / "schemas/task-commit-plan.schema.json").is_file())
                self.assertTrue(os.access(task_commit / "scripts/create-task-commit.sh", os.X_OK))
                task_check = repo / root / "skills/guru-check-task"
                self.assertTrue((task_check / "SKILL.md").is_file())
                self.assertTrue((task_check / "schemas/phase2-check.schema.json").is_file())
                self.assertTrue(os.access(task_check / "scripts/record-phase2-check.sh", os.X_OK))
                sync_base = repo / root / "skills/guru-sync-base"
                self.assertTrue((sync_base / "SKILL.md").is_file())
                self.assertTrue((sync_base / "schemas/base-sync-result.schema.json").is_file())
                self.assertTrue(os.access(sync_base / "scripts/sync-base.sh", os.X_OK))
                clarification = repo / root / "skills/guru-clarify-requirements"
                self.assertTrue((clarification / "SKILL.md").is_file())
                self.assertEqual(
                    (clarification / "SKILL.md").read_bytes(),
                    (SKILLS_ROOT / "packages/guru-clarify-requirements/SKILL.md").read_bytes(),
                )
                self.assertEqual(
                    (clarification / "references/contract.md").read_bytes(),
                    (
                        SKILLS_ROOT
                        / "packages/guru-clarify-requirements/references/contract.md"
                    ).read_bytes(),
                )
                clarification_text = (
                    (clarification / "SKILL.md").read_text(encoding="utf-8")
                    + "\n"
                    + (clarification / "references/contract.md").read_text(encoding="utf-8")
                )
                self.assertIn("guru-planning-approval-2.0", clarification_text)
                self.assertNotIn("schema 1.2 planning-approval validator", clarification_text)
                planning = repo / root / "skills/guru-approve-task-plan"
                self.assertTrue((planning / "SKILL.md").is_file())
                self.assertTrue((planning / "schemas/planning-approval.schema.json").is_file())
                self.assertTrue(os.access(planning / "scripts/record-planning-approval.sh", os.X_OK))
                self.assertTrue(os.access(planning / "scripts/check-planning-approval.sh", os.X_OK))
                task_commit_interface = json.loads(
                    (task_commit / "interface.json").read_text(encoding="utf-8")
                )
                task_commit_planning = next(
                    item
                    for item in task_commit_interface["entry_preconditions"]
                    if item["id"] == "planning_approval"
                )
                self.assertIn("Skill-owned guru-planning-approval-2.0", task_commit_planning["binding"])
                self.assertIn("shared check-planning-approval --require-exit approved", task_commit_planning["freshness"])
                self.assertTrue((clarification / "schemas/requirements-clarification.schema.json").is_file())
                self.assertTrue(os.access(clarification / "scripts/record-requirements-clarification.sh", os.X_OK))
                self.assertTrue(os.access(clarification / "scripts/check-requirements-clarification.sh", os.X_OK))
                wording = repo / root / "skills/guru-review-contract-wording"
                self.assertTrue((wording / "SKILL.md").is_file())
                self.assertTrue((wording / "schemas/contract-wording-review.schema.json").is_file())
                self.assertTrue(os.access(wording / "scripts/record-contract-wording-review.sh", os.X_OK))
                self.assertTrue(os.access(wording / "scripts/check-contract-wording-review.sh", os.X_OK))
                workspace = repo / root / "skills/guru-create-task-workspace"
                self.assertTrue((workspace / "SKILL.md").is_file())
                self.assertTrue((workspace / "schemas/task-workspace-plan.schema.json").is_file())
                self.assertTrue(os.access(workspace / "scripts/create-task-workspace.sh", os.X_OK))

            manifest = dst / "extension.json"
            manifest.write_text(json.dumps({
                "extension": json.loads((REPO / "trellis/guru-team-extension.json").read_text(encoding="utf-8")),
                "skill_packages": result,
            }), encoding="utf-8")
            validation = runtime.validate_skill_installed(repo, dst / "skills", workflow, manifest)
            self.assertEqual(validation["status"], "passed", validation["errors"])


class Stage0MigrationManifestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name) / "repo"
        self.skills = self.repo / "trellis/skills/guru-team"
        self.skills.parent.mkdir(parents=True)
        shutil.copytree(SKILLS_ROOT, self.skills)
        self.workflow = self.repo / "trellis/workflows/guru-team/workflow.md"
        self.workflow.parent.mkdir(parents=True)
        shutil.copyfile(REPO / "trellis/workflows/guru-team/workflow.md", self.workflow)
        shutil.copyfile(
            REPO / "trellis/guru-team-extension.json",
            self.repo / "trellis/guru-team-extension.json",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def validate(self) -> dict:
        return runtime.validate_skill_source(
            self.skills,
            self.workflow,
            boundary_root=self.repo,
        )

    def read_manifest(self) -> dict:
        return json.loads(
            (self.skills / "migrations/stage0-minimal-handoff.json").read_text(encoding="utf-8")
        )

    def write_manifest(self, payload: dict) -> None:
        (self.skills / "migrations/stage0-minimal-handoff.json").write_text(
            json.dumps(payload), encoding="utf-8"
        )

    def test_exact_stage0_activation_manifest_passes(self) -> None:
        result = self.validate()
        self.assertEqual(result["status"], "passed", result["errors"])
        self.assertEqual(result["facts"]["stage0_activation_unit"], "stage0-minimal-handoff-v1")
        self.assertEqual(len(result["facts"]["minimal_handoff_ids"]), 6)
        self.assertEqual(len(result["facts"]["legacy_ids"]), 3)

    def test_missing_exit_binding_fails_closed(self) -> None:
        manifest = self.read_manifest()
        manifest["skills"][0]["exit_bindings"].pop()
        self.write_manifest(manifest)
        result = self.validate()
        self.assertEqual(result["status"], "failed")
        self.assertTrue(any("manifest exits" in item for item in result["errors"]), result["errors"])

    def test_duplicate_profile_binding_fails_closed(self) -> None:
        manifest = self.read_manifest()
        manifest["skills"][1]["profile_case_bindings"].append(
            dict(manifest["skills"][1]["profile_case_bindings"][0])
        )
        self.write_manifest(manifest)
        result = self.validate()
        self.assertEqual(result["status"], "failed")
        self.assertTrue(any("repeats profile binding" in item for item in result["errors"]), result["errors"])

    def test_mixed_registry_activation_fails_closed(self) -> None:
        registry_path = self.skills / "registry.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        entry = next(item for item in registry["skills"] if item.get("id") == "guru-sync-base")
        entry["interface_schema_id"] = "guru-team-skill-interface-1.2"
        entry["io_contract_state"] = "legacy"
        registry_path.write_text(json.dumps(registry), encoding="utf-8")
        result = self.validate()
        self.assertEqual(result["status"], "failed")
        self.assertTrue(
            any("mixed" in item or "legacy_skill_ids" in item for item in result["errors"]),
            result["errors"],
        )


class Stage0PublicInvocationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name) / "target"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-b", "main"], cwd=self.repo, check=True, stdout=subprocess.DEVNULL)
        subprocess.run(["git", "config", "user.email", "stage0@example.invalid"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "Stage0 Test"], cwd=self.repo, check=True)
        (self.repo / "README.md").write_text("stage0\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md"], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=self.repo, check=True, stdout=subprocess.DEVNULL)
        (self.repo / ".trellis").mkdir()
        shutil.copytree(REPO / ".trellis/scripts", self.repo / ".trellis/scripts")
        shutil.copyfile(
            REPO / "trellis/workflows/guru-team/workflow.md",
            self.repo / ".trellis/workflow.md",
        )
        preset.install_assets(
            REPO / "trellis/workflows/guru-team",
            self.repo / ".trellis/guru-team",
            self.repo,
            {"codex", "cursor", "claude"},
        )
        self.remote = Path(self.temp.name) / "origin.git"
        subprocess.run(["git", "init", "--bare", str(self.remote)], check=True, stdout=subprocess.DEVNULL)
        subprocess.run(["git", "remote", "add", "origin", str(self.remote)], cwd=self.repo, check=True)
        subprocess.run(["git", "add", "."], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-m", "install stage0"], cwd=self.repo, check=True, stdout=subprocess.DEVNULL)
        subprocess.run(["git", "push", "-u", "origin", "main"], cwd=self.repo, check=True, stdout=subprocess.DEVNULL)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def invoke(self, skill_id: str, arguments: list[str]) -> dict:
        process = self.invoke_process(skill_id, arguments)
        self.assertEqual(process.returncode, 0, process.stderr)
        payload = json.loads(process.stdout)
        self.assertIsInstance(payload, dict)
        return payload

    def invoke_process(self, skill_id: str, arguments: list[str]) -> subprocess.CompletedProcess[str]:
        wrapper = self.repo / ".agents/skills" / skill_id / "scripts/invoke.sh"
        return subprocess.run(
            [str(wrapper), *arguments],
            cwd=self.repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def test_all_24_stage0_cases_do_not_feed_expected_exit_to_wrappers(self) -> None:
        manifest = json.loads(
            (self.repo / ".trellis/guru-team/skills/migrations/stage0-minimal-handoff.json").read_text(encoding="utf-8")
        )
        covered = set()
        for skill in manifest["skills"]:
            skill_id = skill["id"]
            package = self.repo / ".trellis/guru-team/skills/packages" / skill_id
            interface = json.loads((package / "interface.json").read_text(encoding="utf-8"))
            argv = interface["public_contracts"]["invocation"]["example_argv"]
            self.assertNotIn("--exit", argv, skill_id)
            corpus = json.loads((package / "evals/evals.json").read_text(encoding="utf-8"))
            cases = {item["id"]: item for item in corpus["evals"]}
            for binding in skill["exit_bindings"]:
                exit_id = binding["exit_id"]
                bound_cases = [cases[case_id] for case_id in binding["eval_case_ids"]]
                self.assertTrue(bound_cases, (skill_id, exit_id))
                for case in bound_cases:
                    prompt = case["prompt"]
                    self.assertNotIn("--exit", prompt, case["id"])
                    self.assertIsNone(
                        re.search(rf"(?<![A-Za-z0-9_]){re.escape(exit_id)}(?![A-Za-z0-9_])", prompt),
                        case["id"],
                    )
                    covered.add((skill_id, exit_id))
        self.assertEqual(len(covered), 24)

    def test_semantic_owner_recipe_is_independent_of_expected_exit(self) -> None:
        workdir = Path(self.temp.name) / "owner-recipe"
        facts = workdir / "evals/files/facts.json"
        public_input = workdir / "evals/files/input.json"
        facts.parent.mkdir(parents=True)
        facts.write_text(json.dumps({
            "expected_exit": "blocked",
            "owner_staging": {"recipe": "workspace-created"},
        }), encoding="utf-8")
        public_input.write_text(json.dumps({
            "profile": "issue_only_initial",
            "mode": "workflow",
        }), encoding="utf-8")
        request = {
            "workdir": str(workdir),
            "files": [
                "evals/files/input.json",
                "evals/files/facts.json",
            ],
        }

        recipe, selected_input = native_adapter.owner_recipe(request)

        self.assertEqual(recipe, "workspace-created")
        self.assertEqual(selected_input, public_input.resolve())

    def test_workspace_created_eval_uses_clean_checked_installed_owner_fixture(self) -> None:
        run_root = Path(self.temp.name) / "workspace-created-eval"
        process = subprocess.run(
            [
                str(self.repo / ".trellis/guru-team/scripts/bash/run-skill-evals.sh"),
                "--root", str(self.repo), "--mode", "installed",
                "--skill", "guru-create-task-workspace", "--adapter", "shared",
                "--case", "created-route", "--run-root", str(run_root), "--json",
            ],
            cwd=self.repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        payload = json.loads(process.stdout)
        self.assertEqual(payload["status"], "passed", payload)
        case = payload["cases"][0]
        self.assertEqual(case["actual_exit"], "created")
        transcript_path = Path(case["transcript_locator"])
        transcript = json.loads(transcript_path.read_text(encoding="utf-8"))
        execution_root = transcript_path.parent / "execution"
        owner_repo = execution_root / "owner-repo"
        owner_result = json.loads((
            owner_repo / native_adapter.OWNER_RESULT
        ).read_text(encoding="utf-8"))
        self.assertEqual(owner_result["checker"]["status"], "passed")
        self.assertEqual(owner_result["executor"]["status"], "passed")
        self.assertEqual(owner_result["typed_exit"], "created")
        created = owner_result["created_workspace"]
        self.assertEqual(len(created["artifacts"]), 4)
        self.assertTrue(all(row["ignored"] for row in created["runtime_mappings"]))

        clean = subprocess.run(
            ["git", "status", "--porcelain=v1", "--untracked-files=all"],
            cwd=owner_repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(clean.returncode, 0, clean.stderr)
        self.assertEqual(clean.stdout, "")
        installed = subprocess.run(
            [
                str(owner_repo / ".trellis/guru-team/scripts/bash/check-skill-packages.sh"),
                "--root", str(owner_repo), "--mode", "installed", "--json",
            ],
            cwd=owner_repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(installed.returncode, 0, installed.stderr)
        self.assertEqual(json.loads(installed.stdout)["status"], "passed")

        native_request = json.loads(
            Path(transcript["native_request_path"]).read_text(encoding="utf-8")
        )
        native_bytes = json.dumps(native_request, separators=(",", ":"))
        self.assertNotIn("expected_exit", native_request)
        self.assertNotIn(native_adapter.OWNER_RESULT, native_bytes)
        self.assertNotIn(native_adapter.OWNER_PLAN, native_bytes)
        self.assertNotIn("owner_staging", native_bytes)

    def test_stage0_parser_has_no_caller_selected_exit_argument(self) -> None:
        with self.assertRaises(SystemExit):
            runtime.build_parser().parse_args(["invoke-stage0-skill", "--exit", "ready"])

    def test_sync_base_wrapper_uses_formal_resolve_execute_and_check_routes(self) -> None:
        synced = self.invoke(
            "guru-sync-base",
            ["--source-exit", "start", "--mode", "workflow", "--repo-root", ".", "--base-branch", "main", "--route", "repo_change"],
        )
        self.assertEqual(synced["exit_id"], "synced")
        self.assertEqual(synced["handoff_base_branch"], "main")

        skipped = self.invoke(
            "guru-sync-base",
            ["--source-exit", "start", "--mode", "workflow", "--repo-root", ".", "--base-branch", "main", "--route", "original_request"],
        )
        self.assertEqual(skipped, {"exit_id": "skipped", "continuation_id": "start-original-request"})

        blocked = self.invoke(
            "guru-sync-base",
            ["--source-exit", "start", "--mode", "workflow", "--repo-root", ".", "--base-branch", "missing-stage0-base", "--route", "repo_change"],
        )
        self.assertEqual(blocked, {"exit_id": "blocked"})

        omitted = self.invoke(
            "guru-sync-base",
            ["--source-exit", "start", "--mode", "workflow", "--repo-root", ".", "--route", "repo_change"],
        )
        self.assertEqual(omitted["exit_id"], "synced")
        self.assertEqual(omitted["handoff_base_branch"], "main")

    def test_clarity_null_disposition_is_active_task_only(self) -> None:
        self.assertEqual(
            runtime.stage0_clarity_disposition({
                "invocation_context": {"kind": "active_task_scope_change"},
                "target_disposition": None,
            }),
            "retained",
        )
        for kind in ("initial_change_request", "standalone_review"):
            with self.subTest(kind=kind):
                with self.assertRaises(runtime.WorkflowError) as raised:
                    runtime.stage0_clarity_disposition({
                        "invocation_context": {"kind": kind},
                        "target_disposition": None,
                    })
                self.assertEqual(
                    raised.exception.payload["code"], "owner_result_projection_failed"
                )

    def test_shared_adapter_executes_checker_passed_semantic_wrapper(self) -> None:
        run_root = Path(self.temp.name) / "shared-semantic-eval"
        process = subprocess.run(
            [
                str(self.repo / ".trellis/guru-team/scripts/bash/run-skill-evals.sh"),
                "--root", str(self.repo), "--mode", "installed",
                "--skill", "guru-clarify-requirements", "--adapter", "shared",
                "--case", "clear-route", "--run-root", str(run_root), "--json",
            ],
            cwd=self.repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        payload = json.loads(process.stdout)
        self.assertEqual(payload["status"], "passed")
        self.assertEqual(payload["cases"][0]["actual_exit"], "clear")
        request = json.loads(
            Path(payload["cases"][0]["transcript_locator"])
            .with_name("adapter-request.json")
            .read_text(encoding="utf-8")
        )
        self.assertNotIn("expected_exit", request)

    def test_wording_wrapper_derives_route_from_checked_owner_result(self) -> None:
        wording_path = self.repo / "docs/requirements/requirement-main.md"
        wording_path.parent.mkdir(parents=True)
        wording_path.write_text("# Requirement\n\nThe current contract is explicit.\n", encoding="utf-8")
        scope, contents = runtime.contract_wording_build_scope(
            self.repo,
            "explicit_paths",
            "standalone",
            explicit_paths=["docs/requirements/requirement-main.md"],
        )
        scan = runtime.scan_contract_wording(scope, contents)
        owner_result = runtime.contract_wording_derive_result(
            "explicit_paths",
            "standalone",
            scope,
            scan,
            {
                "generated_at": "2026-07-21T00:00:00Z",
                "semantic_review": {
                    "revisions": [],
                    "classifications": [],
                    "ai_review_gate": {
                        "status": "passed",
                        "reviewer": "stage0-test-reviewer",
                        "summary": "The fixed scope was reviewed against the complete scan.",
                        "reviewed_scan_sha256": scan["scan_sha256"],
                        "checked_dimensions": {
                            name: True for name in runtime.CONTRACT_WORDING_REVIEW_DIMENSIONS
                        },
                    },
                },
                "human_confirmation": {
                    "status": "not_required",
                    "confirmed_by": None,
                    "confirmed_at": None,
                    "reason": "No content mutation was required.",
                },
                "typed_exit": "pass",
            },
        )
        owner_path = self.repo / ".trellis/.runtime/guru-team/evals/wording-owner-result.json"
        owner_path.parent.mkdir(parents=True)
        owner_path.write_text(json.dumps(owner_result) + "\n", encoding="utf-8")

        payload = self.invoke(
            "guru-review-contract-wording",
            [
                "--input", "examples/public-explicit-paths-input.json",
                "--owner-result", ".trellis/.runtime/guru-team/evals/wording-owner-result.json",
            ],
        )
        self.assertEqual(
            payload,
            {"exit_id": "pass", "profile": "explicit_paths", "continuation_id": "stage0-current"},
        )

    def test_clarification_wrapper_derives_route_from_checked_owner_result(self) -> None:
        payload = self.invoke(
            "guru-clarify-requirements",
            [
                "--input", "examples/public-standalone-review-input.json",
                "--owner-result", ".trellis/guru-team/skills/packages/guru-clarify-requirements/examples/requirements-clarification.json",
            ],
        )
        self.assertEqual(
            payload,
            {
                "exit_id": "clear",
                "resume_target": "guru-review-contract-wording",
                "target_disposition": "retained",
                "confirmed_action_id": "no_source_change",
                "continuation_id": "stage0-current",
            },
        )

    def test_semantic_wrapper_uses_repo_relative_public_input(self) -> None:
        package = self.repo / ".trellis/guru-team/skills/packages/guru-clarify-requirements"
        caller_input = self.repo / ".trellis/.runtime/guru-team/evals/clarification-input.json"
        caller_input.parent.mkdir(parents=True, exist_ok=True)
        caller_input.write_bytes((package / "examples/public-standalone-review-input.json").read_bytes())

        payload = self.invoke(
            "guru-clarify-requirements",
            [
                "--input", ".trellis/.runtime/guru-team/evals/clarification-input.json",
                "--owner-result", ".trellis/guru-team/skills/packages/guru-clarify-requirements/examples/requirements-clarification.json",
            ],
        )
        self.assertEqual(payload["exit_id"], "clear")

    def test_output_contract_does_not_read_public_output_example(self) -> None:
        package = Path(self.temp.name) / "minimal-package"
        (package / "schemas").mkdir(parents=True)
        schema = {
            "$schema": runtime.SKILL_SCHEMA_DIALECT,
            "$id": "stage0-test-output",
            "type": "object",
            "additionalProperties": False,
            "required": ["exit_id"],
            "properties": {"exit_id": {"const": "clear"}},
        }
        (package / "schemas/output.schema.json").write_text(json.dumps(schema), encoding="utf-8")
        interface = {
            "external_exits": [{"id": "clear"}],
            "public_contracts": {
                "outputs": [{
                    "exit_id": "clear",
                    "schema": {"path": "schemas/output.schema.json"},
                    "example": {"path": "examples/missing-output.json"},
                }],
                "projections": [{"exit_id": "clear", "operation": "select", "mappings": []}],
            },
        }
        loaded, projection = runtime.stage0_output_contract(
            "guru-clarify-requirements", package, interface, "clear"
        )
        self.assertEqual(loaded["$id"], "stage0-test-output")
        self.assertEqual(projection["exit_id"], "clear")

    def test_semantic_wrapper_requires_owner_result_locator(self) -> None:
        process = self.invoke_process(
            "guru-clarify-requirements",
            ["--input", "examples/public-standalone-review-input.json"],
        )
        self.assertEqual(process.returncode, 2)
        self.assertIn('"code": "invalid_owner_result"', process.stderr)

    def test_semantic_wrapper_rejects_owner_mode_mismatch(self) -> None:
        process = self.invoke_process(
            "guru-clarify-requirements",
            [
                "--input", "examples/public-initial-change-request-input.json",
                "--owner-result", ".trellis/guru-team/skills/packages/guru-clarify-requirements/examples/requirements-clarification.json",
            ],
        )
        self.assertEqual(process.returncode, 2)
        self.assertIn('"code": "owner_result_input_mismatch"', process.stderr)

    def test_readiness_wrapper_uses_checker_passed_owner_route(self) -> None:
        runtime_root = self.repo / ".trellis/.runtime/guru-team/evals"
        runtime_root.mkdir(parents=True, exist_ok=True)
        request_path = runtime_root / "readiness-change-request.json"
        source = {
            "kind": "draft",
            "draft_id": "stage0-readiness",
            "title": "Review Stage 0 readiness",
            "body": "The prerequisite evidence is intentionally incomplete.",
            "selected_comments": [],
        }
        request_path.write_text(json.dumps(source) + "\n", encoding="utf-8")
        request_relative = request_path.relative_to(self.repo).as_posix()
        scope, _ = runtime.contract_wording_build_scope(
            self.repo, "change_request", "standalone", change_request_input=request_relative
        )
        title_hash, body_hash, _ = runtime.change_request_review_scope_hashes(scope)
        authority = runtime.change_request_review_request_authority_projection(
            "example/guru-extension", source, body_hash
        )
        raw_target = {
            "kind": "standalone_request",
            "repo": "example/guru-extension",
            "caller_locator": "stage0-test",
            "request_id": source["draft_id"],
            "source_request_sha256": runtime.context_digest(authority),
            "side_effect_free": True,
            "title_sha256": title_hash,
            "body_sha256": body_hash,
        }
        target, scope, contents = runtime.change_request_review_normalize_target(
            self.repo, raw_target, request_relative, "standalone"
        )
        prerequisite_payloads = {"context": None, "clarity": None, "wording": None}
        prerequisites = runtime.change_request_review_prerequisite_projections(
            self.repo, prerequisite_payloads, target, scope, contents
        )
        linkage = runtime.change_request_review_linkage(target, prerequisites)
        finding_id = "missing-prerequisites"
        dimensions = []
        for index, dimension_id in enumerate(runtime.CHANGE_REQUEST_REVIEW_DIMENSIONS):
            dimensions.append({
                "id": dimension_id,
                "status": "failed" if index == 0 else "passed",
                "summary": "The current evidence was reviewed for this readiness dimension.",
                "evidence_refs": ["target"],
                "affected_hashes": [target["content_sha256"]],
                "finding_ids": [finding_id] if index == 0 else [],
            })
        scope_conclusion = {
            "requirement_scope_basis": "The standalone request is the current authority.",
            "delivery_unit_id": "stage0-readiness",
            "close_issues": [],
            "related_issues": [],
            "followup_issues": [],
            "duplicate_reuse_decision": "No duplicate decision can be completed without prerequisites.",
            "implementation_target": "The Stage 0 public readiness wrapper.",
            "current_gap": "Required prerequisite evidence is missing.",
            "archived_constraints": [],
            "risk_boundary": ["Normal honest workflow operation only."],
            "excluded_scope": [],
        }
        owner_result = runtime.change_request_review_derive_result(
            target,
            prerequisites,
            linkage,
            {
                "generated_at": "2026-07-21T00:00:00Z",
                "mode": "standalone",
                "target": raw_target,
                "prerequisite_payloads": prerequisite_payloads,
                "semantic_review": {
                    "dimensions": dimensions,
                    "findings": [{
                        "finding_id": finding_id,
                        "category": "prerequisite_mismatch",
                        "summary": "The prerequisite handoff is incomplete.",
                        "blocking": True,
                        "evidence_refs": ["target"],
                        "affected_hashes": [target["content_sha256"]],
                        "route_basis": "The readiness review cannot continue without all prerequisite evidence.",
                    }],
                    "scope_conclusion": scope_conclusion,
                    "ai_review_gate": {
                        "status": "blocked",
                        "reviewer": "stage0-test-reviewer",
                        "reviewed_linkage_sha256": linkage["linkage_sha256"],
                        "summary": "The semantic review blocked on missing prerequisites.",
                        "findings_count": 1,
                        "scope_conclusion_sha256": runtime.context_digest(scope_conclusion),
                    },
                },
                "human_confirmation": {
                    "status": "not_required",
                    "reason": "A blocked review does not request a product decision.",
                    "proposal_sha256": None,
                },
                "typed_exit": "blocked",
                "reason": "Prerequisite evidence is incomplete.",
                "affected_evidence": [{
                    "ref": "target",
                    "sha256": target["content_sha256"],
                    "summary": "The current standalone request content.",
                }],
                "consumer": runtime.CHANGE_REQUEST_REVIEW_CONSUMERS["blocked"],
            },
        )
        self.assertEqual(
            runtime.change_request_review_structural_errors(
                self.repo, owner_result, target, prerequisites, linkage
            ),
            [],
        )
        owner_path = runtime_root / "readiness-owner-result.json"
        prerequisites_path = runtime_root / "readiness-prerequisites.json"
        owner_path.write_text(json.dumps(owner_result) + "\n", encoding="utf-8")
        prerequisites_path.write_text(json.dumps(prerequisite_payloads) + "\n", encoding="utf-8")

        payload = self.invoke(
            "guru-review-change-request",
            [
                "--input", "examples/public-standalone-request-input.json",
                "--owner-result", owner_path.relative_to(self.repo).as_posix(),
                "--owner-prerequisites", prerequisites_path.relative_to(self.repo).as_posix(),
                "--owner-change-request", request_relative,
            ],
        )
        self.assertEqual(payload, {"exit_id": "blocked"})

    def test_workspace_created_requires_checker_passed_executor_result(self) -> None:
        process = self.invoke_process(
            "guru-create-task-workspace",
            [
                "--input", "examples/public-workspace-task-initial-input.json",
                "--owner-result", ".trellis/guru-team/skills/packages/guru-create-task-workspace/examples/task-workspace-result.json",
                "--owner-plan", ".trellis/guru-team/skills/packages/guru-create-task-workspace/examples/task-workspace-plan.json",
            ],
        )
        self.assertEqual(process.returncode, 2)
        self.assertIn('"code": "owner_result_not_checked"', process.stderr)


if __name__ == "__main__":
    unittest.main()
