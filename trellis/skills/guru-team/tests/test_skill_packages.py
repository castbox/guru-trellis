from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
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

    def read_registry(self) -> dict:
        return json.loads((self.root / "registry.json").read_text(encoding="utf-8"))

    def write_registry(self, payload: dict) -> None:
        (self.root / "registry.json").write_text(json.dumps(payload), encoding="utf-8")

    def write_skill(self, content: str) -> None:
        (self.root / "packages/guru-example-action/SKILL.md").write_text(content, encoding="utf-8")

    def test_production_registry_preserves_tombstone_and_activates_task_commit(self) -> None:
        result = runtime.validate_skill_source(
            SKILLS_ROOT,
            REPO / "trellis/workflows/guru-team/workflow.md",
        )
        self.assertEqual(result["status"], "passed", result["errors"])
        self.assertEqual(result["facts"]["reserved_ids"], ["guru-create-work-commit"])
        self.assertEqual(result["facts"]["active_ids"], ["guru-create-task-commit"])
        self.assertEqual(result["facts"]["invoke_markers"], 1)
        self.assertEqual(result["facts"]["exit_markers"], 3)

    def test_production_task_commit_package_contract(self) -> None:
        package = SKILLS_ROOT / "packages/guru-create-task-commit"
        interface = json.loads((package / "interface.json").read_text(encoding="utf-8"))
        skill = (package / "SKILL.md").read_text(encoding="utf-8")
        contract = (package / "references/contract.md").read_text(encoding="utf-8")
        workflow = (REPO / "trellis/workflows/guru-team/workflow.md").read_text(encoding="utf-8")

        self.assertEqual(interface["id"], "guru-create-task-commit")
        self.assertEqual(interface["schema_version"], "1.1")
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

    def test_representative_active_package_and_routes_pass(self) -> None:
        result = self.validate()
        self.assertEqual(result["status"], "passed", result["errors"])

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

    def test_missing_declared_schema_fails(self) -> None:
        (self.root / "packages/guru-example-action/schemas/fixture-result.schema.json").unlink()
        self.assertTrue(any("missing schema" in item for item in self.validate()["errors"]))

    def test_invalid_declared_schema_json_fails(self) -> None:
        schema = self.root / "packages/guru-example-action/schemas/fixture-result.schema.json"
        schema.write_text("{invalid", encoding="utf-8")
        self.assertTrue(any("invalid JSON" in item for item in self.validate()["errors"]))

    def test_missing_validator_file_fails(self) -> None:
        (self.root / "packages/guru-example-action/scripts/validate-fixture-result.sh").unlink()
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

    def test_validator_runtime_command_cannot_self_map_to_dispatcher(self) -> None:
        interface = self.read_interface()
        interface["validators"][0]["runtime_command"] = interface["runtime_dependency"]["dispatcher"]
        self.write_interface(interface)

        result = self.validate()

        self.assertEqual(result["status"], "failed")
        self.assertEqual(
            result["errors"],
            [
                "interface for guru-example-action validator result_validator runtime_command "
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
        self.assertTrue(os.access(self.repo / ".codex/skills/guru-example-action/scripts/validate-fixture-result.sh", os.X_OK))
        self.assertFalse((self.repo / ".cursor/skills/guru-example-action").exists())
        self.assertFalse((self.repo / ".claude/skills/guru-example-action").exists())
        self.assertTrue(all(item["action"] == "installed" for item in result["files"]))
        self.assertTrue(any(item["source"].endswith("tests/test_contract.py") for item in result["files"]))

    def test_python_cache_is_not_a_managed_package_asset(self) -> None:
        cache = self.guru_root / "trellis/skills/guru-team/packages/guru-example-action/tests/__pycache__"
        cache.mkdir()
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
        registry["skills"][0]["supported_platforms"] = ["shared", "codex"]
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

    def test_unknown_local_edit_is_preserved_and_gets_new_copy(self) -> None:
        first = self.install({"codex"})
        target = self.repo / ".agents/skills/guru-example-action/SKILL.md"
        target.write_text("local edit\n", encoding="utf-8")
        second = self.install({"codex"}, self.manifest(first))
        self.assertEqual(target.read_text(encoding="utf-8"), "local edit\n")
        self.assertEqual(target.with_name("SKILL.md.new").read_bytes(), (self.guru_root / "trellis/skills/guru-team/packages/guru-example-action/SKILL.md").read_bytes())
        self.assertEqual(second["status"], "conflict")

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
    def test_active_task_commit_package_installs_to_all_selected_roots(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            (repo / ".trellis").mkdir()
            workflow = repo / ".trellis/workflow.md"
            workflow.write_bytes((REPO / "trellis/workflows/guru-team/workflow.md").read_bytes())
            dst = repo / ".trellis/guru-team"

            result = preset.install_skill_packages(repo, REPO, dst, {"codex", "cursor", "claude"}, None)
            self.assertEqual(result["status"], "ok")
            self.assertEqual(result["reserved_ids"], ["guru-create-work-commit"])
            self.assertEqual(result["active_ids"], ["guru-create-task-commit"])
            self.assertFalse((repo / ".agents/skills/guru-create-work-commit").exists())
            for root in (".agents", ".codex", ".cursor", ".claude"):
                package = repo / root / "skills/guru-create-task-commit"
                self.assertTrue((package / "SKILL.md").is_file())
                self.assertTrue((package / "schemas/task-commit-plan.schema.json").is_file())
                self.assertTrue(os.access(package / "scripts/create-task-commit.sh", os.X_OK))

            manifest = dst / "extension.json"
            manifest.write_text(json.dumps({
                "extension": json.loads((REPO / "trellis/guru-team-extension.json").read_text(encoding="utf-8")),
                "skill_packages": result,
            }), encoding="utf-8")
            validation = runtime.validate_skill_installed(repo, dst / "skills", workflow, manifest)
            self.assertEqual(validation["status"], "passed", validation["errors"])


if __name__ == "__main__":
    unittest.main()
