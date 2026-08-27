from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import jsonschema


PACKAGE = Path(__file__).resolve().parents[1]
REPO = PACKAGE.parents[4]
RUNTIME_PATH = PACKAGE / "runtime/owner.py"


def load(relative: str):
    return json.loads((PACKAGE / relative).read_text(encoding="utf-8"))


def load_runtime():
    spec = importlib.util.spec_from_file_location("guru_verify_extension_installation_runtime", RUNTIME_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ExtensionVerificationContractTests(unittest.TestCase):
    def test_dispatcher_accepts_every_repeated_capability_and_runs_entrypoint(self) -> None:
        runtime = load_runtime()
        capabilities = list(runtime.EXTENSION_VERIFICATION_CAPABILITIES)
        command = next(
            item for item in load("commands.json")["commands"]
            if item["validator_id"] == "verification_executor"
        )
        capability_argument = next(
            item for item in command["arguments"]
            if item["flag"] == "--capability"
        )
        self.assertTrue(capability_argument["repeatable"])
        self.assertEqual(capability_argument["values"], capabilities)
        dispatcher = (
            REPO / "trellis/workflows/guru-team/scripts/bash/run-skill-command.sh"
            if PACKAGE
            == REPO / "trellis/skills/guru-team/packages/guru-verify-extension-installation"
            else REPO / ".trellis/guru-team/scripts/bash/run-skill-command.sh"
        )
        with tempfile.TemporaryDirectory() as temp:
            package = Path(temp) / "guru-verify-extension-installation"
            shutil.copytree(PACKAGE, package)
            (package / "runtime/owner.py").write_text(
                "def cmd_execute_extension_verification(args):\n"
                "    return {'status': 'executed', 'capabilities': args.capability}\n",
                encoding="utf-8",
            )
            argv = [
                str(dispatcher),
                "--package-root",
                str(package),
                "--validator",
                "verification_executor",
                "--",
                "--root",
                str(REPO),
                "--input",
                "unused-by-dispatch-regression.json",
            ]
            for capability in capabilities:
                argv.extend(["--capability", capability])
            result = subprocess.run(
                argv,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result)
        self.assertEqual(
            json.loads(result.stdout),
            {"status": "executed", "capabilities": capabilities},
        )
        self.assertEqual(result.stderr, "")

    def test_target_exact_oid_resolution_uses_isolated_origin_fetch(self) -> None:
        runtime = load_runtime()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            remote = root / "remote.git"
            source = root / "source"
            caller = root / "caller"
            subprocess.run(["git", "init", "--bare", "--quiet", str(remote)], check=True)
            subprocess.run(["git", "init", "--quiet", str(source)], check=True)
            subprocess.run(["git", "init", "--quiet", str(caller)], check=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=source, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=source, check=True)
            (source / "README.md").write_text("test\n", encoding="utf-8")
            subprocess.run(["git", "add", "README.md"], cwd=source, check=True)
            subprocess.run(["git", "commit", "--quiet", "-m", "test"], cwd=source, check=True)
            subprocess.run(["git", "remote", "add", "origin", str(remote)], cwd=source, check=True)
            subprocess.run(["git", "push", "--quiet", "origin", "HEAD:refs/heads/main"], cwd=source, check=True)
            commit = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=source, text=True,
                stdout=subprocess.PIPE, check=True,
            ).stdout.strip()
            before = subprocess.run(
                ["git", "status", "--porcelain=v2", "--branch"], cwd=caller,
                text=True, stdout=subprocess.PIPE, check=True,
            ).stdout
            command, result = runtime.extension_verification_target_ref_process(
                caller, "origin", commit, str(remote)
            )
            after = subprocess.run(
                ["git", "status", "--porcelain=v2", "--branch"], cwd=caller,
                text=True, stdout=subprocess.PIPE, check=True,
            ).stdout
        self.assertEqual(command, ["git", "fetch", "--depth=1", "origin", commit])
        self.assertEqual(result.returncode, 0, result)
        self.assertEqual(before, after)
        self.assertEqual(runtime.extension_verification_resolved_remote_head(result, commit), commit)
        self.assertIsNone(runtime.extension_verification_resolved_remote_head(
            subprocess.CompletedProcess([], 1, "", "not found"), commit
        ))
        self.assertEqual(
            runtime.extension_verification_remote_ref_command(
                "origin", "refs/heads/main"
            ),
            [
                "git",
                "ls-remote",
                "origin",
                "refs/heads/main",
                "refs/heads/main^{}",
            ],
        )

    def test_standalone_source_identity_uses_public_exact_oid_not_manifest_generation_head(self) -> None:
        runtime = load_runtime()
        requested = "b" * 40
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)
            manifest = target / runtime.GURU_TEAM_EXTENSION_MANIFEST
            manifest.parent.mkdir(parents=True)
            manifest.write_text(json.dumps({
                "source": {
                    "repo": "https://github.com/castbox/guru-trellis.git",
                    "ref": "a" * 40,
                    "commit": "a" * 40,
                    "tree_state": "dirty",
                    "is_mutable_ref": False,
                }
            }), encoding="utf-8")
            selected = runtime.extension_verification_standalone_source(
                target,
                {"repo_ref": "castbox/guru-trellis", "ref": requested},
            )
        self.assertEqual(selected["selection"], "standalone_fallback")
        self.assertEqual(selected["manifest_provenance"], "available")
        self.assertEqual(selected["requested_ref"], requested)
        self.assertIsNone(selected["manifest_commit"])
        self.assertEqual(selected["tree_state"], "clean")

    def test_platform_inventory_follows_manifest_public_projection(self) -> None:
        runtime = load_runtime()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source"
            installed = root / "installed"
            package = source / "trellis/skills/guru-team/packages/guru-verify-extension-installation"
            (package / "runtime").mkdir(parents=True)
            (package / "SKILL.md").write_text("public\n", encoding="utf-8")
            (package / "runtime/owner.py").write_text("private\n", encoding="utf-8")
            workflow = source / "trellis/workflows/guru-team"
            (workflow / "scripts/bash").mkdir(parents=True)
            (workflow / "workflow.md").write_text("workflow\n", encoding="utf-8")
            (workflow / "config-template.yml").write_text("config\n", encoding="utf-8")
            for name in (
                "execute-extension-verification.sh", "record-extension-verification.sh",
                "check-extension-verification.sh", "invoke-extension-verification.sh",
            ):
                (workflow / "scripts/bash" / name).write_text(name + "\n", encoding="utf-8")
            public_target = installed / ".agents/skills/guru-verify-extension-installation/SKILL.md"
            private_target = installed / ".trellis/guru-team/skills/packages/guru-verify-extension-installation/runtime/owner.py"
            canonical_target = installed / ".trellis/guru-team/skills/packages/guru-verify-extension-installation/SKILL.md"
            for target, origin in (
                (public_target, package / "SKILL.md"),
                (private_target, package / "runtime/owner.py"),
                (canonical_target, package / "SKILL.md"),
            ):
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(origin.read_bytes())
            manifest = installed / ".trellis/guru-team/extension.json"
            manifest.parent.mkdir(parents=True, exist_ok=True)
            files = []
            for target, origin in (
                (public_target, package / "SKILL.md"),
                (private_target, package / "runtime/owner.py"),
                (canonical_target, package / "SKILL.md"),
            ):
                files.append({
                    "path": target.relative_to(installed).as_posix(),
                    "source": origin.relative_to(source).as_posix(),
                    "sha256": hashlib.sha256(origin.read_bytes()).hexdigest(),
                })
            manifest.write_text(json.dumps({
                "install": {"managed_assets": [], "selected_platforms": []},
                "skill_packages": {"files": files},
            }), encoding="utf-8")
            expectations, _, _ = runtime.extension_verification_installed_asset_facts(source, installed)
        paths = {item["path"] for item in expectations}
        self.assertIn(".agents/skills/guru-verify-extension-installation/SKILL.md", paths)
        self.assertNotIn(".agents/skills/guru-verify-extension-installation/runtime/owner.py", paths)

    def test_version_projection_is_package_owned_and_manifest_compatible(self) -> None:
        command = next(
            item for item in load("commands.json")["commands"]
            if item["id"] == "show-extension-version"
        )
        self.assertEqual(command["entrypoint"], "runtime/check.py")
        self.assertEqual(command["runtime_role"], "check")
        self.assertEqual(command["side_effect"], "repo_read")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manifest = root / ".trellis/guru-team/extension.json"
            manifest.parent.mkdir(parents=True)
            manifest.write_text(json.dumps({
                "schema_version": "1.0",
                "installed_at": "2026-08-12T00:00:00Z",
                "extension": {
                    "extension_id": "guru-team",
                    "version": "0.6.15-guru.38",
                    "workflow_template_id": "guru-team",
                    "target_trellis_cli": "0.6.15",
                    "tested": {"trellis_cli": ["0.6.15"]},
                },
                "source": {
                    "repo": "castbox/guru-trellis",
                    "ref": "v0.6.5-guru.10",
                    "commit": "a" * 40,
                    "tree_state": "clean",
                    "is_mutable_ref": False,
                },
                "install": {"selected_platforms": ["codex"], "all_platforms": False},
            }), encoding="utf-8")
            result = subprocess.run(
                [str(PACKAGE / "scripts/version.sh"), "--root", str(root), "--json"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["guru_team_extension"]["version"], "0.6.15-guru.38")
            self.assertEqual(payload["guru_team_extension"]["tested_trellis_cli"], ["0.6.15"])
            self.assertEqual(result.stderr, "")

    def test_version_help_and_compatibility_wrapper_route_to_package(self) -> None:
        wrapper = (
            REPO / "trellis/workflows/guru-team/scripts/bash/version.sh"
            if (REPO / "trellis/skills/guru-team").is_dir()
            else REPO / ".trellis/guru-team/scripts/bash/version.sh"
        )
        for target in (PACKAGE / "scripts/version.sh", wrapper):
            result = subprocess.run(
                [str(target), "--help"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result)
            self.assertIn("usage: show-extension-version", result.stdout)
            self.assertIn("owner: guru-verify-extension-installation", result.stdout)
        repeated = subprocess.run(
            [str(PACKAGE / "scripts/version.sh"), "--root", str(REPO), "--root", str(REPO), "--json"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(repeated.returncode, 2, repeated)
        self.assertEqual(json.loads(repeated.stdout)["code"], "conflicting_arguments")

    def test_active_runtime_is_source_only_and_monolith_independent(self) -> None:
        runtime_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((PACKAGE / "runtime").glob("*.py"))
        )
        for retired in (
            "guru_team_trellis.py",
            "verification_required",
            "not_required",
            "finalization_verification",
            "task_ref",
            "task-bearing",
            "guru-finalize-task",
        ):
            self.assertNotIn(retired, runtime_text)
        commands = load("commands.json")
        self.assertEqual(
            {item["id"] for item in commands["commands"]},
            {item["runtime_command"] for item in load("interface.json")["validators"]},
        )

    def test_interface_is_source_owned_standalone_only(self) -> None:
        interface = load("interface.json")
        self.assertEqual(interface["schema_version"], "1.5")
        self.assertEqual(interface["modes"]["workflow"], {"routing": "not_applicable", "entry_precondition_ids": []})
        self.assertEqual(interface["modes"]["standalone"]["routing"], "direct_discovery")
        self.assertEqual([item["id"] for item in interface["external_exits"]], ["verified", "blocked"])
        self.assertEqual(
            [item["id"] for item in interface["public_contracts"]["input"]["profiles"]],
            ["source_repository_verification"],
        )
        current = json.dumps(interface["public_contracts"], sort_keys=True)
        for retired in ("verification_required", "not_required", "return_to_task_work", "task_ref", "guru-finalize-task"):
            self.assertNotIn(retired, current)
        self.assertEqual(interface["public_contracts"]["private_artifacts"][0]["persistence"], "ignored_runtime")

    def test_current_input_and_outputs_are_closed(self) -> None:
        input_schema = load("schemas/public-source-repository-verification-input.schema.json")
        input_example = load("examples/public-source-repository-verification-input.json")
        jsonschema.Draft202012Validator(input_schema).validate(input_example)
        self.assertFalse(jsonschema.Draft202012Validator(input_schema).is_valid({**input_example, "task_ref": ".trellis/tasks/current"}))
        for exit_id, schema_name in (("verified", "public-verified-output-4.0"), ("blocked", "public-blocked-output-2.0")):
            schema = load(f"schemas/{schema_name}.schema.json")
            example = load(f"examples/public-{exit_id}-output.json")
            jsonschema.Draft202012Validator(schema).validate(example)
        current_result = load("schemas/verification-result-5.0.schema.json")
        legacy_result = load("schemas/verification-result-4.0.schema.json")
        self.assertEqual(current_result["$id"], "guru-extension-installation-verification-result-5.0")
        self.assertEqual(legacy_result["$id"], "guru-extension-installation-verification-result-4.0")
        jsonschema.Draft202012Validator(current_result).validate(
            load("examples/verification-result.json")
        )
        self.assertEqual(
            hashlib.sha256(
                (PACKAGE / "schemas/verification-result-4.0.schema.json").read_bytes()
            ).hexdigest(),
            "8f47671d8b5abb60eb10e334ceb21a9c46d6fb1bd5854e0190fc99c1df7c874d",
        )

    def test_current_semantic_input_requires_explicit_applicability(self) -> None:
        schema = load("schemas/semantic-review-input-2.0.schema.json")
        self.assertEqual(
            schema["properties"]["applicability"]["allOf"][1]["properties"]["status"],
            {"const": "required"},
        )
        self.assertEqual(
            schema["properties"]["semantic_review"]["allOf"][1]["properties"]["conclusion"],
            {"enum": ["verified", "blocked"]},
        )

    def test_current_executor_facts_are_accepted_by_recorder_schema(self) -> None:
        runtime = load_runtime()
        schema = runtime.extension_verification_recorder_input_schema(
            REPO,
            "execution-facts.schema.json",
            "extension verification execution facts",
        )
        self.assertEqual(
            schema["properties"]["schema_version"]["const"],
            runtime.EXTENSION_VERIFICATION_SCHEMA_VERSION,
        )
        facts = load("examples/execution-facts.json")
        self.assertEqual(
            facts["schema_version"],
            runtime.EXTENSION_VERIFICATION_SCHEMA_VERSION,
        )
        self.assertEqual(
            runtime.skill_json_schema_validation_errors(
                facts,
                schema,
                "extension verification execution facts",
            ),
            [],
        )
        adapter_text = (
            REPO / "trellis/skills/guru-team/adapters/eval/native_adapter.py"
        ).read_text(encoding="utf-8")
        self.assertIn(
            '"schema_version": runtime.EXTENSION_VERIFICATION_SCHEMA_VERSION',
            adapter_text,
        )

    def test_throwaway_failure_parses_structured_matrix_terminal_before_cleanup(self) -> None:
        runtime = load_runtime()
        terminal = {
            "schema_version": "1.0",
            "status": "failed",
            "failure": {
                "kind": "matrix_failure",
                "stage": "matrix-cell",
                "cell_id": "codex-clean",
                "command_label": "run-skill-evals.sh",
                "exit_code": 23,
                "error_tail": (
                    "github_pat_SECRET https://user:password@example.com/repo.git "
                    "Authorization: Bearer bearer-secret "
                    "GITHUB_TOKEN=environment-secret "
                    "https://example.com/object?X-Goog-Signature=signed-secret "
                    "-----BEGIN PRIVATE KEY----- private-secret"
                ),
            },
        }
        proc = subprocess.CompletedProcess(
            [],
            2,
            "earlier output\n" + json.dumps(terminal) + "\n",
            "",
        )
        failure = runtime.extension_verification_throwaway_failure(proc)
        self.assertEqual(
            {key: failure[key] for key in ("kind", "stage", "cell_id", "command_label", "exit_code")},
            {
                "kind": "matrix_failure",
                "stage": "matrix-cell",
                "cell_id": "codex-clean",
                "command_label": "run-skill-evals.sh",
                "exit_code": 23,
            },
        )
        self.assertNotIn("github_pat_SECRET", failure["error_tail"])
        self.assertNotIn("user:password", failure["error_tail"])
        self.assertNotIn("bearer-secret", failure["error_tail"])
        self.assertNotIn("environment-secret", failure["error_tail"])
        self.assertNotIn("signed-secret", failure["error_tail"])
        self.assertNotIn("private-secret", failure["error_tail"])

    def test_throwaway_failure_marks_unparseable_output_explicitly(self) -> None:
        runtime = load_runtime()
        proc = subprocess.CompletedProcess(
            [],
            41,
            "not-json github_pat_SECRET",
            "https://user:password@example.com/repo.git",
        )
        failure = runtime.extension_verification_throwaway_failure(proc)
        self.assertEqual(failure["kind"], "unparseable_failure_output")
        self.assertIsNone(failure["stage"])
        self.assertIsNone(failure["cell_id"])
        self.assertEqual(failure["command_label"], "verify-throwaway-installation")
        self.assertEqual(failure["exit_code"], 41)
        self.assertNotIn("github_pat_SECRET", failure["error_tail"])
        self.assertNotIn("user:password", failure["error_tail"])

    def test_execution_facts_schema_accepts_bounded_failure_and_rejects_extra_fields(self) -> None:
        runtime = load_runtime()
        schema = runtime.extension_verification_recorder_input_schema(
            REPO,
            "execution-facts.schema.json",
            "extension verification execution facts",
        )
        facts = load("examples/execution-facts.json")
        facts["status"] = "failed"
        facts["failure"] = {
            "kind": "matrix_failure",
            "stage": "post-matrix",
            "cell_id": None,
            "command_label": "verify_installed_parallel_finish.py",
            "exit_code": 2,
            "error_tail": "parallel finish failed",
        }
        self.assertEqual(
            runtime.skill_json_schema_validation_errors(
                facts,
                schema,
                "extension verification execution facts",
            ),
            [],
        )
        facts["failure"]["unexpected"] = True
        self.assertTrue(
            runtime.skill_json_schema_validation_errors(
                facts,
                schema,
                "extension verification execution facts",
            )
        )

    def test_non_source_rejected_before_executor(self) -> None:
        runtime = load_runtime()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "remote", "add", "origin", "https://github.com/example/business.git"], cwd=root, check=True)
            for relative in (
                "trellis/guru-team-extension.json",
                "trellis/index.json",
                "trellis/workflows/guru-team/workflow.md",
                "trellis/presets/guru-team/scripts/bash/apply.sh",
            ):
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("{}\n", encoding="utf-8")
            previous = os.environ.get("GURU_TEAM_INVOKED_PACKAGE_ROOT")
            os.environ["GURU_TEAM_INVOKED_PACKAGE_ROOT"] = str(PACKAGE)
            try:
                with mock.patch.object(runtime, "extension_verification_execute_facts") as execute:
                    with self.assertRaisesRegex(runtime.WorkflowError, "source_origin_mismatch"):
                        runtime.cmd_execute_extension_verification(argparse.Namespace(
                            root=str(root),
                            input="examples/public-source-repository-verification-input.json",
                            capability=["marketplace_index"],
                        ))
                    execute.assert_not_called()
            finally:
                if previous is None:
                    os.environ.pop("GURU_TEAM_INVOKED_PACKAGE_ROOT", None)
                else:
                    os.environ["GURU_TEAM_INVOKED_PACKAGE_ROOT"] = previous


if __name__ == "__main__":
    unittest.main()
