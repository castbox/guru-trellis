from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


class BaseSyncPackageContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.package = Path(__file__).resolve().parents[1]
        self.interface = json.loads((self.package / "interface.json").read_text(encoding="utf-8"))

    def load_common(self):
        runtime_root = self.package.parents[1]
        if str(runtime_root) not in sys.path:
            sys.path.insert(0, str(runtime_root))
        spec = importlib.util.spec_from_file_location("guru_sync_base_test_common", self.package / "runtime/common.py")
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def load_workspace_prepare(self):
        package_runtime = self.package.parent / "guru-create-task-workspace" / "runtime"
        shared_runtime = self.package.parents[1]
        previous_common = sys.modules.pop("common", None)
        sys.path.insert(0, str(shared_runtime))
        sys.path.insert(0, str(package_runtime))
        try:
            spec = importlib.util.spec_from_file_location(
                "guru_create_task_workspace_test_prepare",
                package_runtime / "prepare.py",
            )
            self.assertIsNotNone(spec)
            self.assertIsNotNone(spec.loader)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        finally:
            sys.path.remove(str(package_runtime))
            sys.path.remove(str(shared_runtime))
            sys.modules.pop("common", None)
            if previous_common is not None:
                sys.modules["common"] = previous_common

    def test_identity_modes_stages_runtime_and_exits(self) -> None:
        self.assertEqual(self.interface["id"], "guru-sync-base")
        self.assertEqual(self.interface["schema_version"], "1.4")
        self.assertEqual(self.interface["judgment_mode"], "deterministic")
        workflow = self.interface["modes"]["workflow"]
        standalone = self.interface["modes"]["standalone"]
        self.assertEqual(workflow["routing"], "global_workflow")
        self.assertEqual(standalone["routing"], "direct_discovery")
        self.assertEqual(workflow["entry_precondition_ids"], standalone["entry_precondition_ids"])
        self.assertEqual(
            workflow["entry_precondition_ids"],
            [
                "runtime_dependency",
                "decision_checkout",
                "selected_base_resolution",
                "clean_checkout",
                "result_facts",
            ],
        )
        self.assertEqual(
            self.interface["ordered_stages"],
            [
                "forward_behavior",
                "recorder_validator",
                "typed_exit",
            ],
        )
        self.assertEqual(
            {item["id"]: item["runtime_command"] for item in self.interface["validators"]},
            {
                "sync_executor": "sync-base",
                "result_validator": "check-base-sync",
                "public_invocation": "invoke-guru-sync-base",
            },
        )
        self.assertEqual(
            [item["id"] for item in self.interface["external_exits"]],
            ["synced", "skipped", "blocked"],
        )

    def test_skill_and_contract_keep_deterministic_boundary(self) -> None:
        skill = (self.package / "SKILL.md").read_text(encoding="utf-8")
        contract = (self.package / "references/contract.md").read_text(encoding="utf-8")
        for phrase in (
            "caller must finish tool-free route classification",
            "scripts/invoke.sh --invocation -",
            "invoke the low-level components first",
            "scalar CLI remains compatibility-only",
            "runtime alone executes the deterministic resolve, execute and",
            "not self-contained or portable",
        ):
            self.assertIn(phrase, skill)
        for forbidden in (
            "execute its\ndeterministic closed loop",
            "Public handoff uses `scripts/invoke.sh` with the declared scalar CLI signature",
            "The public `base_branch` scalar is the caller-owned",
        ):
            self.assertNotIn(forbidden, skill)
        for phrase in (
            "judgment_mode=deterministic",
            "forward_behavior -> recorder_validator -> typed_exit",
            "never consults current branch as a fallback",
            "Multiple existing candidates are not ambiguous",
            "`dev`, `develop`, `main`,",
            "git merge --ff-only",
            "decision checkout HEAD == local selected-base HEAD == remote-tracking HEAD",
            "scripts/invoke.sh --invocation -",
            "--reviewed-base-provenance '<JSON>'",
            "missing_reviewed_base_provenance",
            "query-only",
            "no selected-base AI",
            "run-skill-command",
        ):
            self.assertIn(phrase, contract)
        for forbidden in (
            "Run the `sync_executor` wrapper",
            "Run `sync_executor --execute`",
            "Run `result_validator --result-json",
            "through `--expected-resolution-sha256`",
        ):
            self.assertNotIn(forbidden, contract)
        self.assertIn("It never\nuses `git branch -f`", contract)
        selected = next(
            item for item in self.interface["entry_preconditions"]
            if item["id"] == "selected_base_resolution"
        )
        self.assertIn("prepare-task", selected["binding"])
        self.assertIn("compatibility-only prepare-task", selected["binding"])
        self.assertIn("complete base_current provenance", selected["freshness"])
        for forbidden in ("--resolution-file", "--evidence-file", "--release-resolution-evidence", "quarantine"):
            self.assertNotIn(forbidden, skill + contract + json.dumps(self.interface))

    def test_wrappers_are_package_local_launcher_only(self) -> None:
        for name, validator in (
            ("sync-base.sh", "sync_executor"),
            ("check-base-sync.sh", "result_validator"),
        ):
            wrapper = (self.package / "scripts" / name).read_text(encoding="utf-8")
            self.assertIn("runtime/launch.sh", wrapper)
            self.assertNotIn("guru_team_trellis.py", wrapper)
            self.assertNotIn("git fetch", wrapper)
            self.assertNotIn("git merge", wrapper)

    def test_package_only_copy_fails_with_full_preset_remediation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "guru-sync-base"
            shutil.copytree(self.package, copied)
            for name in ("sync-base.sh", "check-base-sync.sh"):
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

    def test_schema_example_and_digest(self) -> None:
        schema = json.loads(
            (self.package / "schemas/base-sync-result.schema.json").read_text(encoding="utf-8")
        )
        example = json.loads(
            (self.package / "examples/base-sync-result.json").read_text(encoding="utf-8")
        )
        from jsonschema import Draft202012Validator

        Draft202012Validator.check_schema(schema)
        self.assertEqual(list(Draft202012Validator(schema).iter_errors(example)), [])
        self.assertEqual(
            schema["$defs"]["resolution"]["properties"]["source"]["enum"],
            ["explicit", "config", "config-candidate", "remote-default"],
        )
        resolution_identity = {
            "schema_version": example["schema_version"],
            "skill_id": example["skill_id"],
            "status": "resolved",
            "source": example["resolution"]["source"],
            "selected_base": example["resolution"]["selected_base"],
            "remote": example["resolution"]["remote"],
            "candidates": example["resolution"]["candidates"],
            "decision_checkout": {
                "branch": example["decision_checkout"]["branch"],
                "head": example["decision_checkout"]["head_before"],
                "clean": example["decision_checkout"]["clean_before"],
            },
        }
        resolution_encoded = json.dumps(
            resolution_identity,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        self.assertEqual(
            hashlib.sha256(resolution_encoded).hexdigest(),
            example["resolution"]["resolution_sha256"],
        )
        post_resolution_encoded = json.dumps(
            example["post_sync_resolution"],
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        self.assertEqual(
            hashlib.sha256(post_resolution_encoded).hexdigest(),
            example["post_sync_resolution_sha256"],
        )
        self.assertEqual(
            example["post_sync_resolution"]["decision_checkout"]["head"],
            example["decision_checkout"]["head_after"],
        )
        normalized = dict(example)
        digest = normalized.pop("facts_sha256")
        encoded = json.dumps(
            normalized,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        self.assertEqual(hashlib.sha256(encoded).hexdigest(), digest)
        self.assertEqual(
            example["decision_checkout"]["head_after"],
            example["git"]["local_head_after"],
        )
        self.assertEqual(example["git"]["local_head_after"], example["git"]["remote_head_after"])
        self.assertNotIn("/Users/", json.dumps(example))

    def test_package_local_resolve_only_and_closed_json_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(["git", "init", "-b", "main", str(root)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.invalid"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
            (root / "README.md").write_text("test\n")
            (root / ".gitignore").write_text(".trellis/guru-team/config.yml\n")
            subprocess.run(["git", "-C", str(root), "add", "README.md", ".gitignore"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-m", "test"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = subprocess.run(
                [str(self.package / "scripts/sync-base.sh"), "--json", "--root", str(root), "--mode", "workflow", "--resolve-only", "--base", "main"],
                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            self.assertEqual(result.returncode, 0, result)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["skill_id"], "guru-sync-base")
            self.assertEqual(payload["selected_base"], "main")
            self.assertNotIn("guru_team_trellis", result.stdout + result.stderr)

            invalid = subprocess.run(
                [str(self.package / "scripts/sync-base.sh"), "--json", "--mode", "workflow"],
                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            self.assertNotEqual(invalid.returncode, 0)
            self.assertEqual(json.loads(invalid.stdout)["code"], "invalid_arguments")
            self.assertNotIn("Traceback", invalid.stdout + invalid.stderr)

    def test_base_resolution_provenance_and_precedence_use_live_git_facts(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_root = Path(temp)
            root = temp_root / "repo"
            remote = temp_root / "remote.git"
            subprocess.run(["git", "init", "-b", "main", str(root)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.invalid"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
            (root / "README.md").write_text("test\n")
            (root / ".gitignore").write_text(".trellis/guru-team/config.yml\n")
            subprocess.run(["git", "-C", str(root), "add", "README.md", ".gitignore"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-m", "test"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "-C", str(root), "branch", "develop"], check=True)
            develop_checkout = temp_root / "develop"
            subprocess.run(["git", "-C", str(root), "worktree", "add", str(develop_checkout), "develop"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "init", "--bare", str(remote)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "-C", str(root), "remote", "add", "origin", str(remote)], check=True)
            subprocess.run(["git", "-C", str(root), "push", "origin", "main"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "-C", str(remote), "symbolic-ref", "HEAD", "refs/heads/main"], check=True)
            config = root / ".trellis/guru-team/config.yml"
            config.parent.mkdir(parents=True)

            def resolve(*extra: str) -> dict:
                result = subprocess.run(
                    [str(self.package / "scripts/sync-base.sh"), "--json", "--root", str(root), "--mode", "workflow", "--resolve-only", *extra],
                    text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
                )
                self.assertEqual(result.returncode, 0, result)
                return json.loads(result.stdout)

            config.write_text("base_branch: 42\nbase_branch_candidates: invalid\n")
            explicit = resolve("--base", "main")
            self.assertEqual((explicit["source"], explicit["selected_base"], explicit["candidates"]), ("explicit", "main", ["main"]))

            config.write_text("base_branch: main\nbase_branch_candidates: invalid\n")
            scalar = resolve()
            self.assertEqual((scalar["source"], scalar["selected_base"], scalar["candidates"]), ("config", "main", ["main"]))

            config.write_text("base_branch: \nbase_branch_candidates:\n  - missing\n  - develop\n  - main\n  - develop\n")
            candidate = resolve()
            self.assertEqual(candidate["source"], "config-candidate")
            self.assertEqual(candidate["selected_base"], "develop")
            self.assertEqual(candidate["candidates"], ["missing", "develop", "main"])

            config.write_text("base_branch: \nbase_branch_candidates:\n  - missing\n")
            default = resolve()
            self.assertEqual(default["source"], "remote-default")
            self.assertEqual(default["selected_base"], "main")
            self.assertEqual(default["candidates"], ["missing", "main"])

    def test_porcelain_z_parser_keeps_registered_worktree_records_separate(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_root = Path(temp)
            root = temp_root / "repo"
            subprocess.run(["git", "init", "-b", "main", str(root)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.invalid"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
            (root / "README.md").write_text("test\n")
            subprocess.run(["git", "-C", str(root), "add", "README.md"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-m", "test"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "-C", str(root), "branch", "develop"], check=True)
            develop = temp_root / "develop"
            detached = temp_root / "detached"
            subprocess.run(["git", "-C", str(root), "worktree", "add", str(develop), "develop"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "-C", str(root), "worktree", "add", "--detach", str(detached), "HEAD"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            records = self.load_common()._registered_worktrees(root)
            self.assertEqual(len(records), 3)
            self.assertEqual({item["worktree"] for item in records}, {str(root.resolve()), str(detached.resolve()), str(develop.resolve())})
            by_path = {item["worktree"]: item for item in records}
            self.assertEqual(by_path[str(root.resolve())]["branch"], "refs/heads/main")
            self.assertEqual(by_path[str(develop.resolve())]["branch"], "refs/heads/develop")
            self.assertTrue(by_path[str(detached.resolve())]["detached"])

    def test_detached_session_binds_selected_authority_without_reselection(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_root = Path(temp)
            root = temp_root / "repo"
            remote = temp_root / "remote.git"
            subprocess.run(["git", "init", "-b", "main", str(root)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.invalid"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
            (root / "README.md").write_text("test\n")
            (root / ".gitignore").write_text(".trellis/guru-team/config.yml\n")
            subprocess.run(["git", "-C", str(root), "add", "README.md", ".gitignore"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-m", "test"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "-C", str(root), "branch", "release/1.3.0"], check=True)
            subprocess.run(["git", "-C", str(root), "branch", "dev"], check=True)
            subprocess.run(["git", "init", "--bare", str(remote)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "-C", str(root), "remote", "add", "origin", str(remote)], check=True)
            subprocess.run(["git", "-C", str(root), "push", "origin", "main", "release/1.3.0", "dev"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            release = temp_root / "release"
            dev = temp_root / "dev"
            session = temp_root / "session"
            subprocess.run(["git", "-C", str(root), "worktree", "add", str(release), "release/1.3.0"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "-C", str(root), "worktree", "add", str(dev), "dev"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "-C", str(root), "worktree", "add", "--detach", str(session), "HEAD"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            def invoke(base: str | None = None) -> dict:
                public = {"source_exit": "start", "mode": "workflow", "repo_root": str(session), "route": "repo_change"}
                if base is not None:
                    public["base_branch"] = base
                result = subprocess.run(
                    [str(self.package / "scripts/invoke.sh"), "--json", "--invocation", "-"],
                    input=json.dumps({"public_input": public}), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
                )
                self.assertEqual(result.returncode, 0, result)
                return json.loads(result.stdout)

            explicit = invoke("release/1.3.0")
            self.assertEqual(explicit["exit_id"], "synced")
            self.assertEqual(explicit["transition"]["base"]["selected_base"], "release/1.3.0")
            self.assertEqual(explicit["handoff_repo_locator"], str(release.resolve()))
            self.assertEqual(explicit["transition"]["repo_locator"], str(release.resolve()))

            config = session / ".trellis/guru-team/config.yml"
            config.parent.mkdir(parents=True)
            config.write_text("base_branch: main\nbase_branch_candidates:\n  - dev\n")
            explicit_against_config = invoke("release/1.3.0")
            explicit_freshness = self.load_workspace_prepare().reviewed_base_freshness(
                release,
                {"base_branch": "main", "base_branch_candidates": ["dev"]},
                explicit_against_config["transition"]["base"],
                "release/1.3.0",
            )
            self.assertTrue(explicit_freshness["fresh"])
            self.assertTrue(explicit_freshness["three_way_equal"])

            config.write_text("base_branch: release/1.3.0\nbase_branch_candidates: invalid\n")
            configured = invoke()
            self.assertEqual(configured["transition"]["base"]["source"], "config")
            self.assertEqual(configured["handoff_repo_locator"], str(release.resolve()))

            config.write_text("base_branch: \nbase_branch_candidates:\n  - dev\n  - main\n")
            ordered = invoke()
            self.assertEqual(ordered["transition"]["base"]["selected_base"], "dev")
            self.assertEqual(ordered["handoff_repo_locator"], str(dev.resolve()))
            ordered_provenance = ordered["transition"]["base"]
            self.assertEqual(ordered_provenance["ordered_candidates"], ["dev", "main"])
            ordered_freshness = self.load_workspace_prepare().reviewed_base_freshness(
                dev,
                {"base_branch": "", "base_branch_candidates": ["dev", "main"]},
                ordered_provenance,
                None,
            )
            self.assertTrue(ordered_freshness["fresh"])
            self.assertTrue(ordered_freshness["three_way_equal"])

            subprocess.run(["git", "-C", str(root), "worktree", "remove", str(dev)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(invoke(), {"exit_id": "blocked"})

            config.write_text("base_branch: \nbase_branch_candidates:\n  - missing\n")
            remote_default = invoke()
            remote_default_provenance = remote_default["transition"]["base"]
            self.assertEqual(remote_default_provenance["source"], "remote-default")
            self.assertEqual(remote_default_provenance["ordered_candidates"], ["missing", "main"])
            remote_default_freshness = self.load_workspace_prepare().reviewed_base_freshness(
                root,
                {"base_branch": "", "base_branch_candidates": ["missing"]},
                remote_default_provenance,
                None,
            )
            self.assertTrue(remote_default_freshness["fresh"])
            self.assertTrue(remote_default_freshness["three_way_equal"])

            (release / "dirty.txt").write_text("dirty\n")
            self.assertEqual(invoke("release/1.3.0"), {"exit_id": "blocked"})

    def test_authority_identity_mismatch_blocks_before_execution(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "repo"
            subprocess.run(["git", "init", "-b", "main", str(root)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.invalid"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
            (root / "README.md").write_text("test\n")
            subprocess.run(["git", "-C", str(root), "add", "README.md"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-m", "test"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            common = self.load_common()
            records = common._registered_worktrees(root)
            records[0] = {**records[0], "HEAD": "0" * 40}
            with mock.patch.object(common, "_registered_worktrees", return_value=records):
                with self.assertRaisesRegex(Exception, "branch, HEAD, and local ref identity do not match"):
                    common.authority_checkout(root, "main")

    def test_detached_session_fast_forwards_only_authority_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_root = Path(temp)
            root = temp_root / "repo"
            remote = temp_root / "remote.git"
            subprocess.run(["git", "init", "-b", "main", str(root)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.invalid"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
            (root / "README.md").write_text("one\n")
            subprocess.run(["git", "-C", str(root), "add", "README.md"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-m", "one"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "init", "--bare", str(remote)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "-C", str(root), "remote", "add", "origin", str(remote)], check=True)
            subprocess.run(["git", "-C", str(root), "push", "origin", "main"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            session = temp_root / "session"
            producer = temp_root / "producer"
            subprocess.run(["git", "-C", str(root), "worktree", "add", "--detach", str(session), "HEAD"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "clone", str(remote), str(producer)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "-C", str(producer), "config", "user.email", "test@example.invalid"], check=True)
            subprocess.run(["git", "-C", str(producer), "config", "user.name", "Test"], check=True)
            (producer / "README.md").write_text("two\n")
            subprocess.run(["git", "-C", str(producer), "commit", "-am", "two"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "-C", str(producer), "push", "origin", "main"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            remote_head = subprocess.run(["git", "-C", str(producer), "rev-parse", "HEAD"], check=True, text=True, stdout=subprocess.PIPE).stdout.strip()

            invocation = {"public_input": {"source_exit": "start", "mode": "workflow", "repo_root": str(session), "base_branch": "main", "route": "repo_change"}}
            result = subprocess.run(
                [str(self.package / "scripts/invoke.sh"), "--json", "--invocation", "-"],
                input=json.dumps(invocation), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            self.assertEqual(result.returncode, 0, result)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["exit_id"], "synced")
            self.assertEqual(payload["handoff_repo_locator"], str(root.resolve()))
            provenance = payload["transition"]["base"]
            self.assertEqual(provenance["decision_head"], remote_head)
            self.assertEqual(provenance["decision_head"], provenance["local_base_head"])
            self.assertEqual(provenance["local_base_head"], provenance["remote_base_head"])
            freshness = self.load_workspace_prepare().reviewed_base_freshness(
                root,
                {"base_branch": "main", "base_branch_candidates": []},
                provenance,
                "main",
            )
            self.assertTrue(freshness["fresh"])
            self.assertTrue(freshness["three_way_equal"])
            self.assertEqual(subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], check=True, text=True, stdout=subprocess.PIPE).stdout.strip(), remote_head)
            self.assertNotEqual(subprocess.run(["git", "-C", str(session), "rev-parse", "HEAD"], check=True, text=True, stdout=subprocess.PIPE).stdout.strip(), remote_head)
            execute = (self.package / "runtime/execute.py").read_text(encoding="utf-8")
            self.assertIn('git(authority,"fetch","--no-tags"', execute)
            self.assertIn('git(authority,"merge","--ff-only"', execute)
            for forbidden in ('git(authority,"checkout"', 'git(authority,"switch"', 'git(authority,"reset"', 'git(authority,"rebase"', 'git(authority,"stash"', '["git","branch"', '["git","worktree","add"'):
                self.assertNotIn(forbidden, execute)

    def test_public_invoke_skipped_is_schema_valid(self) -> None:
        invocation = {"public_input": {"source_exit": "start", "mode": "workflow", "route": "original_request"}}
        result = subprocess.run(
            [str(self.package / "scripts/invoke.sh"), "--json", "--invocation", "-"],
            input=json.dumps(invocation), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        self.assertEqual(result.returncode, 0, result)
        payload = json.loads(result.stdout)
        self.assertEqual(payload, {"exit_id": "skipped", "continuation_id": "start-original-request"})
        from jsonschema import Draft202012Validator
        schema = json.loads((self.package / "schemas/public-skipped-output.schema.json").read_text())
        self.assertEqual(list(Draft202012Validator(schema).iter_errors(payload)), [])

    def test_public_invoke_synced_is_schema_valid(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_root = Path(temp)
            root = temp_root / "repo"
            subprocess.run(["git", "init", "-b", "main", str(root)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.invalid"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
            (root / "README.md").write_text("test\n")
            subprocess.run(["git", "-C", str(root), "add", "README.md"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-m", "test"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            remote = temp_root / "remote.git"
            subprocess.run(["git", "init", "--bare", str(remote)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "-C", str(root), "remote", "add", "origin", str(remote)], check=True)
            subprocess.run(["git", "-C", str(root), "push", "origin", "main"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            invocation = {"public_input": {"source_exit": "start", "mode": "workflow", "repo_root": str(root), "base_branch": "main", "route": "repo_change"}}
            result = subprocess.run(
                [str(self.package / "scripts/invoke.sh"), "--json", "--invocation", "-"],
                input=json.dumps(invocation), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            self.assertEqual(result.returncode, 0, result)
            payload = json.loads(result.stdout)
            schema = json.loads((self.package / "schemas/public-synced-output-2.0.schema.json").read_text())
            from jsonschema import Draft202012Validator
            self.assertEqual(list(Draft202012Validator(schema).iter_errors(payload)), [])
            transition = payload["transition"]
            self.assertEqual(transition["stage"], "base_current")
            self.assertEqual(transition["mode"], "workflow")
            self.assertEqual(transition["base"]["decision_head"], transition["base"]["local_base_head"])
            self.assertEqual(transition["base"]["local_base_head"], transition["base"]["remote_base_head"])

    def test_public_invoke_unresolved_base_returns_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(["git", "init", "-b", "main", str(root)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.invalid"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
            (root / "README.md").write_text("test\n")
            subprocess.run(["git", "-C", str(root), "add", "README.md"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-m", "test"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            invocation = {"public_input": {"source_exit": "start", "mode": "workflow", "repo_root": str(root), "base_branch": "missing-base", "route": "repo_change"}}
            result = subprocess.run(
                [str(self.package / "scripts/invoke.sh"), "--json", "--invocation", "-"],
                input=json.dumps(invocation), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            self.assertEqual(result.returncode, 0, result)
            payload = json.loads(result.stdout)
            self.assertEqual(payload, {"exit_id": "blocked"})
            from jsonschema import Draft202012Validator
            schema = json.loads((self.package / "schemas/public-blocked-output.schema.json").read_text())
            self.assertEqual(list(Draft202012Validator(schema).iter_errors(payload)), [])

    def test_public_invoke_does_not_hide_invalid_public_input_as_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(["git", "init", "-b", "main", str(root)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.invalid"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
            (root / "README.md").write_text("test\n")
            subprocess.run(["git", "-C", str(root), "add", "README.md"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-m", "test"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            invocation = {"public_input": {"source_exit": "start", "mode": "workflow", "repo_root": str(root), "base_branch": "-unsafe", "route": "repo_change"}}
            result = subprocess.run(
                [str(self.package / "scripts/invoke.sh"), "--json", "--invocation", "-"],
                input=json.dumps(invocation), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            self.assertNotEqual(result.returncode, 0, result)
            self.assertEqual(json.loads(result.stdout)["code"], "invalid_arguments")

            invalid_route = {"public_input": {"source_exit": "start", "mode": "workflow", "repo_root": str(root), "route": "unsupported"}}
            result = subprocess.run(
                [str(self.package / "scripts/invoke.sh"), "--json", "--invocation", "-"],
                input=json.dumps(invalid_route), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            self.assertNotEqual(result.returncode, 0, result)
            self.assertEqual(json.loads(result.stdout)["code"], "invalid_arguments")


if __name__ == "__main__":
    unittest.main()
