from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
import sys


REPO = Path(__file__).resolve().parents[4]
SKILLS = REPO / "trellis/skills/guru-team"
POST_DELIVERY_PACKAGES = (
    "guru-review-task-completion",
    "guru-complete-task-closure",
    "guru-finish-task",
    "guru-cleanup-task-resources",
    "guru-reactivate-task",
)
sys.path.insert(0, str(SKILLS))
from runtime.io import CommandError  # noqa: E402
from runtime.installed import validate_skill_installed, workflow_facts  # noqa: E402
from runtime.schema import validate_json  # noqa: E402
from runtime.validate import validate  # noqa: E402


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


preset = load_module(
    "guru_team_preset_integration",
    REPO / "trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py",
)


class InstalledWorkflowIntegrationStateTests(unittest.TestCase):
    def test_deferred_package_does_not_require_workflow_markers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workflow = root / ".trellis/workflow.md"
            workflow.parent.mkdir(parents=True)
            workflow.write_text("# Empty production graph\n", encoding="utf-8")
            errors: list[str] = []
            facts = workflow_facts(
                root,
                workflow,
                {
                    "guru-example-deferred": {
                        "workflow_integration_state": "deferred",
                        "interface_data": {"external_exits": []},
                    }
                },
                True,
                errors,
            )
        self.assertEqual(errors, [])
        self.assertEqual(facts["invoke_markers"], 0)

    def test_integrated_package_still_requires_one_invoke_marker(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workflow = root / ".trellis/workflow.md"
            workflow.parent.mkdir(parents=True)
            workflow.write_text("# Empty production graph\n", encoding="utf-8")
            errors: list[str] = []
            workflow_facts(
                root,
                workflow,
                {
                    "guru-example-integrated": {
                        "workflow_integration_state": "integrated",
                        "interface_data": {"external_exits": []},
                    }
                },
                True,
                errors,
            )
        self.assertEqual(
            errors,
            ["active skill guru-example-integrated has 0 mandatory invoke markers"],
        )


class SkillEvalAdapterRequestSchemaTests(unittest.TestCase):
    schemas = (
        SKILLS / "schemas/skill-eval-adapter-request.schema.json",
        SKILLS / "tests/fixtures/representative-active/schemas/skill-eval-adapter-request.schema.json",
    )

    def setUp(self) -> None:
        self.request = {
            "schema_version": "1.0",
            "adapter_id": "codex",
            "platform": "codex",
            "skill_id": "guru-maintain-architecture-baseline",
            "package_root": "packages/guru-maintain-architecture-baseline",
            "interface": {},
            "case_id": "planning-semantic-authoring",
            "prompt": "Review the planning Architecture impact.",
            "files": [],
            "workdir": ".",
            "corpus_path": "evals/evals.json",
            "corpus_sha256": "a" * 64,
            "runtime_target": "scripts/invoke.sh",
        }
        self.authoring_fields = {
            "native_execution_adapter": "codex",
            "model_id": "gpt-5.6-sol",
        }

    def test_representative_adapter_request_schema_matches_canonical(self) -> None:
        self.assertEqual(self.schemas[0].read_bytes(), self.schemas[1].read_bytes())

    def test_semantic_authoring_request_accepts_adapter_and_model(self) -> None:
        request = {
            **self.request,
            "native_execution_mode": "semantic_authoring",
            **self.authoring_fields,
        }
        for schema in self.schemas:
            with self.subTest(schema=schema):
                validate_json(request, schema, "adapter_request")

    def test_semantic_authoring_request_requires_each_adapter_and_model_field(self) -> None:
        for schema in self.schemas:
            for missing in self.authoring_fields:
                request = {
                    **self.request,
                    "native_execution_mode": "semantic_authoring",
                    **self.authoring_fields,
                }
                del request[missing]
                with self.subTest(schema=schema, missing=missing):
                    with self.assertRaises(CommandError) as raised:
                        validate_json(request, schema, "adapter_request")
                    self.assertEqual(raised.exception.code, "schema_mismatch")

    def test_post_owner_request_accepts_omitted_or_explicit_mode(self) -> None:
        for schema in self.schemas:
            for mode in (None, "post_owner"):
                request = dict(self.request)
                if mode is not None:
                    request["native_execution_mode"] = mode
                with self.subTest(schema=schema, mode=mode):
                    validate_json(request, schema, "adapter_request")

    def test_post_owner_request_rejects_native_authoring_fields(self) -> None:
        for schema in self.schemas:
            for mode in (None, "post_owner"):
                for fields in (
                    {"native_execution_adapter": "codex"},
                    self.authoring_fields,
                ):
                    request = {**self.request, **fields}
                    if mode is not None:
                        request["native_execution_mode"] = mode
                    with self.subTest(schema=schema, mode=mode, fields=fields):
                        with self.assertRaises(CommandError) as raised:
                            validate_json(request, schema, "adapter_request")
                        self.assertEqual(raised.exception.code, "schema_mismatch")

    def test_codex_post_owner_request_accepts_model_identity(self) -> None:
        request = {**self.request, "model_id": "gpt-5.6-sol"}
        for schema in self.schemas:
            with self.subTest(schema=schema):
                validate_json(request, schema, "adapter_request")


class SkillPackageIntegrationTests(unittest.TestCase):
    def run_json(self, *arguments: str, cwd: Path = REPO) -> dict:
        process = subprocess.run(
            list(arguments), cwd=cwd, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        payload = json.loads(process.stdout)
        self.assertIsInstance(payload, dict)
        return payload

    def test_source_command_graph_is_closed(self) -> None:
        payload = self.run_json(
            str(REPO / "trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh"),
            "--root", str(REPO), "--mode", "source", "--json",
        )
        self.assertEqual(payload["status"], "passed")
        self.assertEqual(payload["active_packages"], 32)
        self.assertEqual(payload["complete_package_commands"], 32)
        self.assertGreater(payload["commands"], 0)
        self.assertGreater(payload["package_test_count"], 0)

    def test_post_delivery_public_contract_projections_are_closed(self) -> None:
        for package_id in POST_DELIVERY_PACKAGES:
            with self.subTest(package=package_id):
                package = SKILLS / "packages" / package_id
                interface = json.loads((package / "interface.json").read_text(encoding="utf-8"))
                contracts = interface["public_contracts"]
                artifacts = {item["path"] for item in interface["artifacts"]}
                schemas = {item["path"] for item in interface["schemas"]}
                outputs = {item["exit_id"]: item for item in contracts["outputs"]}
                consumers = {item["id"]: item for item in contracts["consumer_inputs"]}
                projections = {item["id"]: item for item in contracts["projections"]}

                self.assertNotIn("planned_skill_input_seed", (package / "interface.json").read_text(encoding="utf-8"))
                self.assertEqual(len(outputs), len(contracts["outputs"]))
                self.assertEqual(len(projections), len(contracts["projections"]))
                self.assertEqual(
                    {use_id for output in outputs.values() for use_id in output["consumer_use_ids"]},
                    set(projections),
                )
                self.assertEqual(
                    len({output["schema"]["path"] for output in outputs.values()}),
                    len(outputs),
                )
                self.assertEqual(
                    len({output["example"]["path"] for output in outputs.values()}),
                    len(outputs),
                )

                for output in outputs.values():
                    self.assertIn(output["schema"]["path"], schemas)
                    self.assertIn(output["example"]["path"], artifacts)
                    example = json.loads((package / output["example"]["path"]).read_text(encoding="utf-8"))
                    validate_json(example, package / output["schema"]["path"], f"{package_id}.{output['exit_id']}.example")
                    validate_json(example, package / "schemas/public-output.schema.json", f"{package_id}.{output['exit_id']}.aggregate")

                for projection in projections.values():
                    output = outputs[projection["exit_id"]]
                    example = json.loads((package / output["example"]["path"]).read_text(encoding="utf-8"))
                    consumer = consumers[projection["consumer_input_id"]]
                    projected = {
                        mapping["target"]: example[mapping["source"]]
                        for mapping in projection.get("mappings", [])
                    }
                    if consumer["payload_kind"] == "zero_payload":
                        self.assertEqual(projection["operation"], "select")
                        self.assertEqual(projected, {})
                        self.assertEqual(example, {"exit_id": projection["exit_id"]})
                        continue

                    contract = consumer["contract"]
                    if contract["kind"] == "json_schema":
                        self.assertIn("exit_id", projected)
                        validate_json(projected, package / contract["path"], f"{package_id}.{projection['id']}.workflow")
                        continue

                    self.assertEqual(contract["kind"], "skill_input_authoring_seed")
                    self.assertEqual(set(projected), set(contract["seed_fields"]))
                    self.assertFalse(set(contract["seed_fields"]) & set(contract["authoring_fields"]))
                    authoring = json.loads((package / contract["authoring_example"]["path"]).read_text(encoding="utf-8"))
                    self.assertEqual(set(authoring), set(contract["authoring_fields"]))
                    target_interface_path = SKILLS / contract["interface_path"]
                    target_interface = json.loads(target_interface_path.read_text(encoding="utf-8"))
                    profile = next(
                        item for item in target_interface["public_contracts"]["input"]["profiles"]
                        if item["id"] == contract["profile_id"]
                    )
                    target_package = target_interface_path.parent
                    validate_json(
                        {**authoring, **projected},
                        target_package / profile["schema"]["path"],
                        f"{package_id}.{projection['id']}.skill_input",
                    )

    def test_source_validator_rejects_duplicate_command_owner(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(SKILLS, root / "trellis/skills/guru-team")
            packages = root / "trellis/skills/guru-team/packages"
            first = packages / "guru-approve-task-plan/commands.json"
            second = packages / "guru-check-task/commands.json"
            first_data = json.loads(first.read_text(encoding="utf-8"))
            second_data = json.loads(second.read_text(encoding="utf-8"))
            second_data["commands"][0]["id"] = first_data["commands"][0]["id"]
            second.write_text(json.dumps(second_data), encoding="utf-8")
            with self.assertRaises(CommandError) as raised:
                validate(root, "source")
            self.assertEqual(raised.exception.code, "duplicate_command")

    def test_contract_and_eval_discovery_use_shared_runtime(self) -> None:
        contract = self.run_json(
            str(REPO / "trellis/workflows/guru-team/scripts/bash/discover-skill-contract.sh"),
            "--root", str(REPO), "--mode", "source",
            "--skill", "guru-sync-base", "--json",
        )
        self.assertEqual(contract["skill_id"], "guru-sync-base")
        evaluations = self.run_json(
            str(REPO / "trellis/workflows/guru-team/scripts/bash/discover-skill-evals.sh"),
            "--root", str(REPO), "--mode", "source",
            "--skill", "guru-sync-base", "--json",
        )
        self.assertEqual(evaluations["skill_id"], "guru-sync-base")
        self.assertTrue(evaluations["case_ids"])

    def test_public_wrapper_reaches_package_owner(self) -> None:
        wrapper = SKILLS / "packages/guru-select-workflow-mode/scripts/invoke.sh"
        process = subprocess.run(
            [str(wrapper), "--help"], cwd=REPO, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertNotIn("guru_team_trellis.py", wrapper.read_text(encoding="utf-8"))

    def test_installed_tree_and_platform_projections_are_private_runtime_free(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "repo"
            (target / ".trellis").mkdir(parents=True)
            (target / ".trellis/workflow.md").write_bytes(
                (REPO / "trellis/workflows/guru-team/workflow.md").read_bytes()
            )
            preset.install_assets(
                REPO / "trellis/workflows/guru-team",
                target / ".trellis/guru-team",
                target,
                {"codex", "cursor", "claude"},
            )
            installed = self.run_json(
                str(target / ".trellis/guru-team/scripts/bash/check-skill-packages.sh"),
                "--root", str(target), "--mode", "installed", "--json",
                cwd=target,
            )
            self.assertEqual(installed["status"], "passed")
            self.assertEqual(len(installed["facts"]["active_ids"]), 32)
            source_commands = sum(
                len(json.loads(path.read_text(encoding="utf-8"))["commands"])
                for path in (SKILLS / "packages").glob("guru-*/commands.json")
            )
            self.assertEqual(installed["facts"]["command_count"], source_commands)
            self.assertEqual(installed["facts"]["package_private_test_count"], 0)
            self.assertFalse((target / ".trellis/guru-team/scripts/python/guru_team_trellis.py").exists())
            for projection in (
                target / ".agents/skills",
                target / ".codex/skills",
                target / ".cursor/skills",
                target / ".claude/skills",
            ):
                for path in projection.rglob("*"):
                    self.assertNotIn(path.name, {"runtime", "tests", "errors"})

    def test_installed_validator_rejects_package_private_tests(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "repo"
            (target / ".trellis").mkdir(parents=True)
            (target / ".trellis/workflow.md").write_bytes(
                (REPO / "trellis/workflows/guru-team/workflow.md").read_bytes()
            )
            preset.install_assets(
                REPO / "trellis/workflows/guru-team",
                target / ".trellis/guru-team",
                target,
                {"codex", "cursor", "claude"},
            )
            injected = (
                target
                / ".trellis/guru-team/skills/packages/guru-bind-task-session/tests/injected.py"
            )
            injected.parent.mkdir(parents=True)
            injected.write_text("# package-private fixture\n", encoding="utf-8")

            process = subprocess.run(
                [
                    str(target / ".trellis/guru-team/scripts/bash/check-skill-packages.sh"),
                    "--root", str(target), "--mode", "installed", "--json",
                ],
                cwd=target,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )

            self.assertEqual(process.returncode, 2, process.stderr)
            payload = json.loads(process.stdout)
            self.assertEqual(payload["status"], "failed")
            self.assertEqual(payload["facts"]["package_private_test_count"], 1)
            self.assertTrue(
                any("contains package-private tests" in error for error in payload["errors"])
            )

    def test_installed_validator_rejects_empty_package_private_tests_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "repo"
            (target / ".trellis").mkdir(parents=True)
            (target / ".trellis/workflow.md").write_bytes(
                (REPO / "trellis/workflows/guru-team/workflow.md").read_bytes()
            )
            preset.install_assets(
                REPO / "trellis/workflows/guru-team",
                target / ".trellis/guru-team",
                target,
                {"codex", "cursor", "claude"},
            )
            empty_tests = (
                target
                / ".trellis/guru-team/skills/packages/guru-bind-task-session/tests"
            )
            empty_tests.mkdir()

            process = subprocess.run(
                [
                    str(target / ".trellis/guru-team/scripts/bash/check-skill-packages.sh"),
                    "--root", str(target), "--mode", "installed", "--json",
                ],
                cwd=target,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )

            self.assertEqual(process.returncode, 2, process.stderr)
            payload = json.loads(process.stdout)
            self.assertEqual(payload["status"], "failed")
            self.assertEqual(payload["facts"]["package_private_test_count"], 0)
            self.assertTrue(
                any("contains package-private tests directory" in error for error in payload["errors"])
            )

    def test_interface_declared_non_invoke_wrapper_is_projected_and_invocable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "repo"
            (target / ".trellis").mkdir(parents=True)
            (target / ".trellis/workflow.md").write_bytes(
                (REPO / "trellis/workflows/guru-team/workflow.md").read_bytes()
            )
            preset.install_assets(
                REPO / "trellis/workflows/guru-team",
                target / ".trellis/guru-team",
                target,
                {"codex", "cursor", "claude"},
            )

            skill_id = "guru-restore-archived-task"
            package = target / ".trellis/guru-team/skills/packages" / skill_id
            interface = json.loads(
                (package / "interface.json").read_text(encoding="utf-8")
            )
            public_wrapper = interface["public_contracts"]["invocation"]["wrapper"]
            self.assertEqual("scripts/restore-archived-task.sh", public_wrapper)
            self.assertTrue((package / public_wrapper).is_file())

            for platform in (".agents", ".codex", ".claude", ".cursor"):
                projection = target / platform / "skills" / skill_id
                wrapper = projection / public_wrapper
                self.assertTrue(wrapper.is_file(), wrapper)
                self.assertTrue(wrapper.stat().st_mode & 0o111, wrapper)
                self.assertFalse((projection / "scripts/invoke.sh").exists())
                process = subprocess.run(
                    [str(wrapper), "--help"],
                    cwd=target,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
                self.assertEqual(0, process.returncode, process.stderr)
                self.assertIn("usage: restore-archived-task", process.stdout)

    def test_production_eval_contract_registration_survives_installation(self) -> None:
        canonical_manifest = json.loads(
            (REPO / "trellis/guru-team-extension.json").read_text(encoding="utf-8")
        )
        public_api = canonical_manifest["public_api"]
        self.assertEqual(
            public_api["skill_contracts"]["contract_manifests"],
            [
                {
                    "id": "production-current-v4",
                    "schema_id": "guru-team-production-contract-manifest-4.0",
                    "path": "contracts/production-current-4.0.json",
                }
            ],
        )
        self.assertEqual(
            public_api["skill_evals"]["adapter_request_schema_ids"][-1],
            "guru-team-skill-eval-adapter-request-3.0",
        )
        self.assertEqual(
            public_api["skill_evals"]["adapter_response_schema_ids"][-1],
            "guru-team-skill-eval-adapter-response-3.0",
        )
        self.assertEqual(
            public_api["skill_evals"]["run_schema_ids"][-1],
            "guru-team-skill-eval-run-4.0",
        )
        self.assertEqual(
            public_api["skill_evals"]["control_map_schema_id"],
            "guru-team-skill-eval-control-map-1.0",
        )
        schema_ids = {
            "schemas/skill-interface-1.6.schema.json": (
                "https://github.com/castbox/guru-trellis/schemas/guru-team-skill-interface-1.6.json"
            ),
            "schemas/skill-eval-adapter-request-3.0.schema.json": (
                "guru-team-skill-eval-adapter-request-3.0"
            ),
            "schemas/skill-eval-adapter-response-3.0.schema.json": (
                "guru-team-skill-eval-adapter-response-3.0"
            ),
            "schemas/skill-eval-run-4.0.schema.json": "guru-team-skill-eval-run-4.0",
            "schemas/skill-eval-control-map-1.0.schema.json": (
                "guru-team-skill-eval-control-map-1.0"
            ),
            "schemas/production-contract-manifest-4.0.schema.json": (
                "guru-team-production-contract-manifest-4.0"
            ),
        }
        for relative, schema_id in schema_ids.items():
            schema = json.loads((SKILLS / relative).read_text(encoding="utf-8"))
            self.assertEqual(schema["$id"], schema_id)
        production_contract = json.loads(
            (SKILLS / "contracts/production-current-4.0.json").read_text(encoding="utf-8")
        )
        self.assertEqual(production_contract["contract_id"], "production-current-v4")
        self.assertEqual(
            production_contract["production_eval_control"],
            {
                "adapter_request_schema_id": "guru-team-skill-eval-adapter-request-3.0",
                "adapter_response_schema_id": "guru-team-skill-eval-adapter-response-3.0",
                "run_schema_id": "guru-team-skill-eval-run-4.0",
                "control_map_schema_id": "guru-team-skill-eval-control-map-1.0",
                "model_id": "gpt-5.6-sol",
                "case_count": 160,
                "invocations_per_case": 5,
                "total_invocations": 800,
                "opaque_mapping_algorithm": "i-base32-HMAC-SHA-256-26",
                "opaque_mapping_message": "matrix_sha256+NUL+case_id+NUL+decimal_slot",
                "opaque_order_algorithm": "independent-HMAC-SHA-256-sort-key",
                "control_map_path": "control/case-map.json",
                "control_root_file_mode": "0700",
                "control_map_file_mode": "0600",
                "invocation_order": "randomized",
                "grading_owner": "host_runner",
                "identity_validation": "fresh-live-issue-origin-main-and-required-identities-at-run-start-and-end",
                "timestamp_validation": "utc-schema-monotonic-nonfuture-observation-cross-midnight-allowed",
                "forbidden_request_fields": [
                    "case_id",
                    "slot",
                    "input_profile_id",
                    "profile_id",
                    "pair_id",
                    "scenario_id",
                    "scenario_kind",
                    "pressure_framing",
                    "expected_exit",
                    "expected_decisions",
                    "invocation_index",
                    "fresh_invocations_per_case",
                    "corpus_path",
                    "corpus_sha256",
                    "matrix_sha256",
                    "control_map_path",
                    "hmac_key",
                ],
            },
        )

        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "repo"
            (target / ".trellis").mkdir(parents=True)
            (target / ".trellis/workflow.md").write_bytes(
                (REPO / "trellis/workflows/guru-team/workflow.md").read_bytes()
            )
            preset.install_assets(
                REPO / "trellis/workflows/guru-team",
                target / ".trellis/guru-team",
                target,
                {"codex", "cursor", "claude"},
            )
            installed_root = target / ".trellis/guru-team/skills"
            for relative in (
                "schemas/skill-eval-adapter-request-3.0.schema.json",
                "schemas/skill-eval-adapter-response-3.0.schema.json",
                "schemas/skill-eval-run-4.0.schema.json",
                "schemas/skill-eval-control-map-1.0.schema.json",
                "schemas/production-contract-manifest-4.0.schema.json",
                "contracts/production-current-4.0.json",
                "contracts/production-current.json",
                "contracts/production-current-3.0.json",
                "contracts/production-current-2.0.json",
            ):
                self.assertTrue((installed_root / relative).is_file(), relative)
            for relative, schema_id in schema_ids.items():
                installed_schema = json.loads(
                    (installed_root / relative).read_text(encoding="utf-8")
                )
                self.assertEqual(installed_schema["$id"], schema_id)
            self.assertEqual(
                (installed_root / "contracts/production-current.json").read_bytes(),
                (installed_root / "contracts/production-current-4.0.json").read_bytes(),
            )
            self.assertEqual(
                (installed_root / "contracts/production-current-4.0.json").read_bytes(),
                (SKILLS / "contracts/production-current-4.0.json").read_bytes(),
            )
            for legacy in ("production-current-2.0.json", "production-current-3.0.json"):
                self.assertEqual(
                    (installed_root / "contracts" / legacy).read_bytes(),
                    (SKILLS / "contracts" / legacy).read_bytes(),
                )

    def test_installed_validator_rebuilds_global_command_ownership(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "repo"
            (target / ".trellis").mkdir(parents=True)
            (target / ".trellis/workflow.md").write_bytes(
                (REPO / "trellis/workflows/guru-team/workflow.md").read_bytes()
            )
            preset.install_assets(
                REPO / "trellis/workflows/guru-team",
                target / ".trellis/guru-team",
                target,
                {"codex", "cursor", "claude"},
            )
            packages = target / ".trellis/guru-team/skills/packages"
            first = json.loads((packages / "guru-approve-task-plan/commands.json").read_text())
            second_path = packages / "guru-check-task/commands.json"
            second = json.loads(second_path.read_text())
            second["commands"][0]["id"] = first["commands"][0]["id"]
            second_path.write_text(json.dumps(second), encoding="utf-8")
            result = validate_skill_installed(
                target,
                target / ".trellis/guru-team/skills",
                target / ".trellis/workflow.md",
                target / ".trellis/guru-team/extension.json",
            )
            self.assertEqual(result["status"], "failed")
            self.assertTrue(any("multiple owners" in error for error in result["errors"]))

    def test_active_runtime_has_no_monolith_dependency(self) -> None:
        active_roots = (
            REPO / "trellis/skills/guru-team/runtime",
            REPO / "trellis/skills/guru-team/packages",
            REPO / "trellis/workflows/guru-team/scripts/bash",
        )
        offenders = []
        for root in active_roots:
            for path in root.rglob("*"):
                if path.is_file() and path.suffix in {".py", ".sh"}:
                    text = path.read_text(encoding="utf-8", errors="replace")
                    if (
                        "guru_team_trellis.py" in text
                        and path.name != "validate.py"
                        and "/tests/" not in path.as_posix()
                    ):
                        offenders.append(path.relative_to(REPO).as_posix())
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
