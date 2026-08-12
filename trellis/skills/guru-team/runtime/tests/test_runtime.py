from __future__ import annotations

import ast
import json
import shutil
import subprocess
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from runtime.validate import _package_paths


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT.parent


class SharedRuntimeTests(unittest.TestCase):
    def test_command_runtime_consumes_one_global_json_flag(self) -> None:
        from runtime.command import _consume_global_json_flag, _validate_argument_cardinality
        from runtime.io import CommandError

        self.assertEqual(
            _consume_global_json_flag(["--root", ".", "--json", "--input", "value"]),
            ["--root", ".", "--input", "value"],
        )
        with self.assertRaises(CommandError) as raised:
            _consume_global_json_flag(["--json", "--json"])
        self.assertEqual(raised.exception.code, "conflicting_arguments")
        command = {
            "arguments": [
                {"flag": "--profile", "repeatable": False, "conflicts": []},
                {"flag": "--path", "repeatable": True, "conflicts": []},
                {"flag": "--resolve-only", "repeatable": False, "conflicts": ["--execute"]},
                {"flag": "--execute", "repeatable": False, "conflicts": ["--resolve-only"]},
            ]
        }
        with self.assertRaises(CommandError) as repeated:
            _validate_argument_cardinality(command, ["--profile", "one", "--profile=two"])
        self.assertEqual(repeated.exception.code, "conflicting_arguments")
        _validate_argument_cardinality(command, ["--path", "one", "--path=two"])
        with self.assertRaises(CommandError) as conflicting:
            _validate_argument_cardinality(command, ["--resolve-only", "--execute"])
        self.assertEqual(conflicting.exception.code, "conflicting_arguments")

    def test_command_error_can_preserve_declared_private_stderr_payload(self) -> None:
        from runtime.io import CommandError, fail

        stdout = StringIO()
        stderr = StringIO()
        error = CommandError(
            "finalization_stale",
            "finalization",
            "Reprepare.",
            3,
            response={"status": "error", "stage": "archive-path-preflight"},
            response_stream="stderr",
        )
        with redirect_stdout(stdout), redirect_stderr(stderr):
            self.assertEqual(fail(error), 3)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(
            json.loads(stderr.getvalue()),
            {"status": "error", "stage": "archive-path-preflight"},
        )

    def test_version_utility_preserves_manifest_contract(self) -> None:
        from runtime.utility import extension_payload, version

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".trellis/guru-team").mkdir(parents=True)
            missing = version(repo)
            self.assertEqual(missing["guru_team_extension"], {
                "status": "missing",
                "path": ".trellis/guru-team/extension.json",
            })

            manifest = {
                "schema_version": "1.0",
                "extension": {
                    "extension_id": "guru-team",
                    "version": "0.6.5-guru.3",
                    "workflow_template_id": "guru-team",
                    "target_trellis_cli": "0.6.5",
                    "tested": {"trellis_cli": ["0.6.5"]},
                },
                "installed_at": "2026-08-12T00:00:00Z",
                "source": {
                    "repo": "castbox/guru-trellis",
                    "ref": "main",
                    "commit": "abc123",
                    "tree_state": "clean",
                    "is_mutable_ref": True,
                },
                "install": {"selected_platforms": ["codex", "cursor"], "all_platforms": False},
            }
            path = repo / ".trellis/guru-team/extension.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            current = version(repo)
            self.assertEqual(current["guru_team_extension"]["version"], "0.6.5-guru.3")
            self.assertEqual(current["guru_team_extension"]["tested_trellis_cli"], ["0.6.5"])
            self.assertEqual(current["guru_team_extension"]["selected_platforms"], ["codex", "cursor"])
            self.assertIs(current["guru_team_extension"]["all_platforms"], False)

            path.write_text("{", encoding="utf-8")
            invalid = extension_payload(repo)
            self.assertEqual(invalid["status"], "invalid")
            self.assertIn("invalid", invalid["error"])

    def test_version_wrapper_supports_source_and_installed_layouts(self) -> None:
        source_wrapper = Path(__file__).resolve().parents[4] / "workflows/guru-team/scripts/bash/version.sh"
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".trellis/guru-team/scripts/bash").mkdir(parents=True)
            (repo / ".trellis/guru-team/runtime").mkdir(parents=True)
            installed_wrapper = repo / ".trellis/guru-team/scripts/bash/version.sh"
            shutil.copy2(source_wrapper, installed_wrapper)
            for name in ("__init__.py", "utility.py"):
                shutil.copy2(ROOT / name, repo / ".trellis/guru-team/runtime" / name)

            for wrapper, root in ((source_wrapper, Path(__file__).resolve().parents[5]), (installed_wrapper, repo)):
                result = subprocess.run(
                    [str(wrapper), "--root", str(root), "--json"],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result)
                payload = json.loads(result.stdout)
                self.assertEqual(payload["status"], "ok")
                self.assertEqual(payload["repo_root"], str(root.resolve()))

    def test_prepare_base_freshness_revalidates_reviewed_provenance(self) -> None:
        from runtime.utility import _digest, _reviewed_base_freshness

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            remote = root / "origin.git"
            subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
            subprocess.run(["git", "init", "-q", "-b", "main", str(repo)], check=True)
            subprocess.run(["git", "config", "user.name", "Kernel Test"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.email", "kernel@example.invalid"], cwd=repo, check=True)
            (repo / "README.md").write_text("base\n")
            subprocess.run(["git", "add", "README.md"], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-q", "-m", "test: base"], cwd=repo, check=True)
            subprocess.run(["git", "remote", "add", "origin", str(remote)], cwd=repo, check=True)
            subprocess.run(["git", "push", "-q", "-u", "origin", "main"], cwd=repo, check=True)
            head = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=repo, check=True,
                text=True, stdout=subprocess.PIPE,
            ).stdout.strip()
            resolution = {
                "schema_version": "1.0",
                "skill_id": "guru-sync-base",
                "status": "resolved",
                "source": "explicit",
                "selected_base": "main",
                "remote": "origin",
                "candidates": ["main"],
                "decision_checkout": {"branch": "main", "head": head, "clean": True},
            }
            provenance = {
                "source": "explicit",
                "selected_base": "main",
                "remote": "origin",
                "ordered_candidates": ["main"],
                "decision_head": head,
                "local_base_head": head,
                "remote_base_head": head,
                "post_sync_resolution_sha256": _digest(resolution),
            }
            config = {"base_branch": "main", "base_branch_candidates": []}
            freshness = _reviewed_base_freshness(repo, config, provenance, "main")
            self.assertEqual(freshness["reviewed_resolution_sha256"], _digest(resolution))
            self.assertEqual(freshness["post_sync_resolution"], resolution)
            self.assertTrue(freshness["three_way_equal"])
            self.assertTrue(freshness["fresh"])
            self.assertEqual(freshness["facts_sha256"], _digest({
                key: value for key, value in freshness.items() if key != "facts_sha256"
            }))
            invalid = dict(provenance)
            invalid.pop("remote_base_head")
            with self.assertRaisesRegex(ValueError, "exactly eight fields"):
                _reviewed_base_freshness(repo, config, invalid, "main")

    def test_contract_discovery_projects_every_active_public_contract(self) -> None:
        from runtime.discovery import discover

        registry = json.loads((SKILLS / "registry.json").read_text(encoding="utf-8"))
        active = [row for row in registry["skills"] if row["state"] == "active"]
        self.assertEqual(len(active), 15)
        for row in active:
            with self.subTest(skill=row["id"]):
                payload = discover(SKILLS, row["id"])
                interface = json.loads((SKILLS / row["interface"]).read_text(encoding="utf-8"))
                contracts = interface["public_contracts"]
                self.assertEqual(payload, {
                    "status": "ok",
                    "skill_id": row["id"],
                    "interface_schema_id": row["interface_schema_id"],
                    "input": contracts["input"],
                    "invocation": contracts["invocation"],
                    "outputs": contracts["outputs"],
                    "consumer_inputs": contracts["consumer_inputs"],
                    "projections": contracts["projections"],
                    "private_artifacts": contracts["private_artifacts"],
                })

    def test_contract_discovery_wrapper_and_unknown_skill_error(self) -> None:
        wrapper = Path(__file__).resolve().parents[4] / "workflows/guru-team/scripts/bash/discover-skill-contract.sh"
        root = Path(__file__).resolve().parents[5]
        success = subprocess.run(
            [str(wrapper), "--root", str(root), "--mode", "source", "--skill", "guru-sync-base", "--json"],
            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertEqual(success.returncode, 0, success)
        self.assertEqual(json.loads(success.stdout)["skill_id"], "guru-sync-base")
        failure = subprocess.run(
            [str(wrapper), "--root", str(root), "--mode", "source", "--skill", "guru-missing-skill", "--json"],
            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertEqual(failure.returncode, 2, failure)
        self.assertEqual(failure.stdout, "")
        self.assertEqual(set(json.loads(failure.stderr)), {"code", "field_path", "remediation"})

    def test_launcher_direct_contract_and_missing_arguments(self) -> None:
        launcher = ROOT / "launch.sh"
        package = SKILLS / "packages/guru-sync-base"
        direct = subprocess.run(
            [str(launcher), str(package), "sync-base", "--help"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(direct.returncode, 0, direct)
        self.assertIn("usage: sync-base", direct.stdout)
        self.assertEqual(direct.stderr, "")

        missing = subprocess.run(
            [str(launcher)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(missing.returncode, 2, missing)
        payload = json.loads(missing.stdout)
        self.assertEqual(payload["code"], "invalid_arguments")
        self.assertNotIn("unbound variable", missing.stdout + missing.stderr)

    def test_platform_projection_routes_to_installed_package(self) -> None:
        skill_id = "guru-sync-base"
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            installed_root = repo / ".trellis/guru-team"
            shutil.copytree(ROOT, installed_root / "runtime")
            shutil.copytree(
                SKILLS / "packages" / skill_id,
                installed_root / "skills/packages" / skill_id,
            )
            for platform in (".agents", ".claude", ".codex", ".cursor"):
                projection = repo / platform / "skills" / skill_id
                (projection / "scripts").mkdir(parents=True)
                shutil.copy2(
                    SKILLS / "packages" / skill_id / "scripts/invoke.sh",
                    projection / "scripts/invoke.sh",
                )
                result = subprocess.run(
                    [str(projection / "scripts/invoke.sh"), "--help"],
                    cwd=repo,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result)
                self.assertIn("usage: invoke-guru-sync-base", result.stdout)
                self.assertEqual(result.stderr, "")

    def test_platform_projection_uses_installed_repo_as_default_root(self) -> None:
        skill_id = "guru-discover-change-context"
        with tempfile.TemporaryDirectory() as tmp:
            outside = Path(tmp)
            repo = outside / "repo"
            repo.mkdir()
            subprocess.run(
                ["git", "init", "-q", "-b", "feat/context", str(repo)],
                check=True,
            )
            installed_root = repo / ".trellis/guru-team"
            shutil.copytree(ROOT, installed_root / "runtime")
            shutil.copytree(
                SKILLS / "packages" / skill_id,
                installed_root / "skills/packages" / skill_id,
            )
            projection = repo / ".agents" / "skills" / skill_id
            (projection / "scripts").mkdir(parents=True)
            shutil.copy2(
                SKILLS / "packages" / skill_id / "scripts/invoke.sh",
                projection / "scripts/invoke.sh",
            )
            task = repo / ".trellis/tasks/08-12-context"
            task.mkdir(parents=True)
            (task / "task.json").write_text(json.dumps({
                "id": "08-12-context",
                "status": "in_progress",
                "branch": "feat/context",
            }))
            subprocess.run(["git", "config", "user.name", "Kernel Test"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.email", "kernel@example.invalid"], cwd=repo, check=True)
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-q", "-m", "test: add installed runtime"], cwd=repo, check=True)
            owner = json.loads((
                installed_root
                / "skills/packages"
                / skill_id
                / "examples/change-context-owner-result.json"
            ).read_text())
            public_output = json.loads((
                installed_root
                / "skills/packages"
                / skill_id
                / "examples/public-context-ready-output-2.0.json"
            ).read_text())
            owner["mode"] = "workflow"
            invocation = outside / "invocation.json"
            invocation.write_text(json.dumps({
                "schema_version": "1.0",
                "public_input": {
                    "profile": "pre_task",
                    "source_exit": "synced",
                    "mode": "workflow",
                    "repo_locator": "example/repo",
                    "base_branch": "main",
                    "continuation_id": "outside-cwd",
                },
                "transition": {
                    "repo_locator": ".",
                    "base": public_output["transition"]["base"],
                },
                "owner_context": {},
                "owner_result": owner,
            }))
            result = subprocess.run(
                [
                    str(projection / "scripts/invoke.sh"),
                    "--invocation",
                    str(invocation),
                    "--active-task",
                    ".trellis/tasks/08-12-context",
                ],
                cwd=outside,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result)
            self.assertEqual(json.loads(result.stdout)["exit_id"], "context_ready")
            self.assertEqual(result.stderr, "")

    def test_source_and_installed_layouts(self) -> None:
        source = _package_paths(Path("/repo"), "source")
        self.assertEqual(source[0], Path("/repo/trellis/skills/guru-team"))
        self.assertEqual(source[3], Path("/repo/trellis/skills/guru-team/runtime"))
        installed = _package_paths(Path("/repo"), "installed")
        self.assertEqual(installed[0], Path("/repo/.trellis/guru-team/skills"))
        self.assertEqual(installed[3], Path("/repo/.trellis/guru-team/runtime"))
    def test_command_and_error_contracts_for_pilots(self) -> None:
        from jsonschema import Draft202012Validator
        command_schema = json.loads((SKILLS / "schemas/skill-commands.schema.json").read_text())
        error_schema = json.loads((SKILLS / "schemas/skill-error-catalog.schema.json").read_text())
        for package_id in ("guru-sync-base", "guru-clarify-requirements"):
            package = SKILLS / "packages" / package_id
            commands = json.loads((package / "commands.json").read_text())
            errors = json.loads((package / "errors/catalog.json").read_text())
            self.assertEqual(list(Draft202012Validator(command_schema).iter_errors(commands)), [])
            self.assertEqual(list(Draft202012Validator(error_schema).iter_errors(errors)), [])
            codes = {item["code"] for item in errors["errors"]}
            self.assertEqual(len(codes), len(errors["errors"]))
            for command in commands["commands"]:
                self.assertEqual(command["owner"], package_id)
                self.assertTrue((package / command["entrypoint"]).is_file())
                self.assertLessEqual(set(command["errors"]), codes)

    def test_kernel_has_no_skill_specific_branching(self) -> None:
        forbidden = ("guru-sync-base", "guru-clarify-requirements", "typed_exit", "profile")
        for path in ROOT.glob("*.py"):
            if path.name == "validate.py":
                continue
            source = path.read_text()
            ast.parse(source)
            for token in forbidden:
                self.assertNotIn(token, source)

    def test_compat_dispatch_resolves_validator_metadata(self) -> None:
        package = SKILLS / "packages/guru-sync-base"
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "runtime.compat",
                "--package-root",
                str(package),
                "--validator",
                "sync_executor",
                "--",
                "--help",
            ],
            cwd=SKILLS,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("usage: sync-base", result.stdout)


if __name__ == "__main__":
    unittest.main()
