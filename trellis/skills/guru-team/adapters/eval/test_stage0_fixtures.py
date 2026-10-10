from __future__ import annotations

import copy
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest import mock
from types import SimpleNamespace

SKILLS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILLS))

from adapters.eval.fixture_io import (
    bind_task_commit_candidate_argument,
    run_git,
    write_fake_gh,
)
from adapters.eval.archived_fixtures import PINNED_OLD_SOURCE_SHA
from adapters.eval.owner_runtime import (
    compose_production_owner_command_runtime,
    load_package_owner_runtime,
)
from adapters.eval.stage0_fixtures import (
    build_clarity_owner,
    build_readiness_owner,
    prepare_readiness_invocation,
    record_readiness_invocation,
    stage0_command,
)


class ReadinessAdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="guru-readiness-adapter-")
        cls.root = Path(cls.temporary.name)
        cls.fixture = cls.root / "repo"
        cls.fixture.mkdir()
        installed = cls.fixture / ".trellis/guru-team"
        cls.packages = installed / "skills/packages"
        ignore = shutil.ignore_patterns("__pycache__", "*.pyc")
        shutil.copytree(SKILLS / "runtime", installed / "runtime", ignore=ignore)
        shutil.copytree(SKILLS / "schemas", installed / "skills/schemas", ignore=ignore)
        shutil.copytree(SKILLS / "consumers", installed / "skills/consumers", ignore=ignore)
        for skill in ("guru-sync-base", "guru-discover-change-context", "guru-clarify-requirements",
                      "guru-review-contract-wording", "guru-review-change-request"):
            shutil.copytree(SKILLS / "packages" / skill, cls.packages / skill, ignore=ignore)
        (cls.fixture / ".gitignore").write_text(".trellis/.runtime/\n__pycache__/\n*.pyc\n")
        for relative in ("docs/requirements.md", "trellis/runtime.py", "trellis/test_runtime.py"):
            target = cls.fixture / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("# Readiness adapter source fixture\n")
        (cls.fixture / ".trellis/.runtime/guru-team/evals").mkdir(parents=True)
        run_git(cls.fixture, "init", "-q", "-b", "main")
        run_git(cls.fixture, "config", "user.email", "adapter@example.invalid")
        run_git(cls.fixture, "config", "user.name", "Adapter fixture")
        run_git(cls.fixture, "add", ".")
        run_git(cls.fixture, "commit", "-qm", "Readiness fixture")
        run_git(cls.fixture, "remote", "add", "origin", "https://github.com/example/guru-extension.git")
        run_git(cls.fixture, "update-ref", "refs/remotes/origin/main", run_git(cls.fixture, "rev-parse", "HEAD"))
        result = subprocess.run([
            sys.executable, str(installed / "runtime/bootstrap.py"),
            "--repo", str(cls.fixture), "--runtime-assets", str(installed / "runtime"),
            "--python", sys.executable, "--json",
        ], text=True, capture_output=True, check=False,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        if result.returncode:
            raise AssertionError(result)
        cls.target = installed / "scripts/bash/run-skill-command.sh"

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def test_readiness_five_exits_use_real_producer_outputs(self):
        package = self.packages / "guru-review-change-request"
        runtime = load_package_owner_runtime(self.target, package.name)
        recipes = {
            "readiness-ready": "ready", "readiness-clarify": "clarify_requirements",
            "readiness-wording": "review_wording", "readiness-refresh": "refresh_context",
            "readiness-blocked": "blocked",
        }
        for mode in ("workflow", "standalone"):
            for recipe, exit_id in recipes.items():
                with self.subTest(mode=mode, recipe=recipe):
                    binary = write_fake_gh(self.root, recipe)
                    with mock.patch.dict(os.environ, {"PATH": f"{binary}:{os.environ['PATH']}"}):
                        owner, state, source = build_readiness_owner(
                            runtime, self.fixture, package, recipe, mode, "current_issue"
                        )
                        envelope = state["invocation"]
                        output = stage0_command(self.fixture, package.name, "invoke", envelope, "--invocation", "-")
                    self.assertEqual(exit_id, output["exit_id"])
                    self.assertNotIn("prerequisite_payloads", envelope["owner_result"])
                    self.assertEqual(source, envelope["owner_context"]["change_request"])
                    if exit_id in {"clarify_requirements", "review_wording"}:
                        self.assertEqual(envelope["transition"], output["transition"])
                    if "clarity" in state["producer_results"]:
                        semantic_hash = state["producer_results"]["clarity"]["content_identity"]["content_sha256"]
                        self.assertEqual(semantic_hash, owner["prerequisites"]["clarity"]["content_sha256"])
                        self.assertNotEqual(semantic_hash, owner["target"]["content_sha256"])

    def test_clarity_six_exits_use_recorder_authoring(self):
        package = self.packages / "guru-clarify-requirements"
        runtime = load_package_owner_runtime(self.target, package.name)
        recipes = {
            "clarity-clear": "clear", "clarity-needs-context": "needs_context",
            "clarity-refresh-context": "refresh_context", "clarity-blocked": "blocked",
            "clarity-retarget": "retarget_context", "clarity-new-task": "new_task",
        }
        for recipe, exit_id in recipes.items():
            with self.subTest(recipe=recipe):
                with mock.patch(
                    "adapters.eval.stage0_fixtures.stage0_command", wraps=stage0_command,
                ) as record:
                    owner = build_clarity_owner(runtime, package, recipe)
                authored = record.call_args.args[3]
                self.assertNotIn("content_identity", authored)
                self.assertNotIn("facts_sha256", authored["review_target"])
                if authored["target_disposition"] is not None:
                    self.assertNotIn("disposition_digest", authored["target_disposition"])
                for action in authored["source_actions"]:
                    self.assertNotIn("payload_sha256", action)
                    self.assertNotIn("action_digest", action)
                stage0_command(
                    self.fixture, package.name, "check-requirements-clarification",
                    owner, "--input", "-",
                )
                self.assertEqual(exit_id, owner["typed_exit"])

    def test_draft_and_standalone_source_profiles(self):
        package = self.packages / "guru-review-change-request"
        runtime = load_package_owner_runtime(self.target, package.name)
        binary = write_fake_gh(self.root, "readiness-ready")
        with mock.patch.dict(os.environ, {"PATH": f"{binary}:{os.environ['PATH']}"}):
            for profile in ("proposed_draft", "standalone_request"):
                with self.subTest(profile=profile):
                    _, state, _ = build_readiness_owner(
                        runtime, self.fixture, package, "readiness-ready", "standalone", profile
                    )
                    output = stage0_command(self.fixture, package.name, "invoke", state["invocation"], "--invocation", "-")
                    self.assertEqual("ready", output["exit_id"])

    def draft_seed(self, recipe="readiness-ready", *, source=None):
        package = self.packages / "guru-review-change-request"
        runtime = load_package_owner_runtime(self.target, package.name)
        binary = write_fake_gh(self.root, "readiness-ready")
        with mock.patch.dict(os.environ, {"PATH": f"{binary}:{os.environ['PATH']}"}):
            return prepare_readiness_invocation(
                runtime, self.fixture, package, recipe, "standalone", "proposed_draft",
                source_override=source,
            )

    def record_and_invoke(self, authored):
        recorded, envelope = record_readiness_invocation(self.fixture, authored)
        output = stage0_command(
            self.fixture, "guru-review-change-request", "invoke", envelope,
            "--invocation", "-",
        )
        return recorded, envelope, output

    def test_minimal_draft_and_executable_public_recipe_use_real_producers(self):
        seed, prerequisites, source = self.draft_seed()
        original_producers = copy.deepcopy(prerequisites["public_outputs"])
        self.assertEqual(
            ["context_ready", "clear", "pass"],
            [output["exit_id"] for output in original_producers.values()],
        )
        locator = original_producers["wording"]["transition"]["target_locator"]
        self.assertEqual(locator, source["draft_id"])
        self.assertEqual(locator, seed["owner_result"]["target"]["draft_id"])
        self.assertEqual(locator, seed["public_input"]["target_locator"])
        self.assertEqual(
            {"status", "reviewer", "summary"},
            set(seed["owner_result"]["semantic_review"]["ai_review_gate"]),
        )
        self.assertNotIn("prerequisites", seed["owner_result"])
        self.assertNotIn("evidence_linkage", seed["owner_result"])

        # Execute the public Markdown recipe itself, with actual producer stdout
        # and an explicitly objective-test semantic sample (not an Agent Gate).
        contract = (SKILLS / "packages/guru-review-change-request/references/contract.md").read_text()
        recipe = contract.split("```python\n", 1)[1].split("```", 1)[0]
        completed_review = {
            key: value for key, value in seed["owner_result"].items()
            if key not in {"mode", "target"}
        }
        driver = recipe + "\nimport sys\ninputs = json.load(sys.stdin)\n" + (
            "envelope = draft_envelope(inputs['source'], inputs['producer'], "
            "inputs['repo'], inputs['review'])\n"
            "print(json.dumps(record_check_invoke(envelope)))\n"
        )
        result = subprocess.run(
            [sys.executable, "-B", "-c", driver], cwd=self.fixture,
            input=json.dumps({"source": source, "producer": original_producers["wording"],
                              "repo": seed["owner_result"]["target"]["repo"],
                              "review": completed_review}),
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual("ready", json.loads(result.stdout)["exit_id"])
        self.assertEqual(original_producers, prerequisites["public_outputs"])
        self.assertEqual("", run_git(self.fixture, "status", "--porcelain"))
        self.assertFalse((self.fixture / ".trellis/tasks").exists())

    def test_five_draft_authoring_mistakes_rebuild_consumer_without_producer_changes(self):
        seed, prerequisites, _ = self.draft_seed()
        producers = copy.deepcopy(prerequisites["public_outputs"])
        recorded, _, _ = self.record_and_invoke(seed)

        mixed = copy.deepcopy(seed)
        mixed["owner_result"]["target"].update({
            "caller_locator": "copied-standalone-caller", "request_id": "copied-request",
        })
        normalized, _, output = self.record_and_invoke(mixed)
        self.assertEqual("ready", output["exit_id"])
        self.assertIsNone(normalized["target"]["caller_locator"])
        self.assertIsNone(normalized["target"]["request_id"])
        del mixed["owner_result"]["target"]["draft_id"]

        body_digest = copy.deepcopy(seed)
        body_digest["owner_result"]["target"]["source_request_sha256"] = hashlib.sha256(
            seed["owner_context"]["change_request"]["body"].encode("utf-8")
        ).hexdigest()

        invented = copy.deepcopy(seed)
        invented["owner_context"]["change_request"]["draft_id"] = "draft:invented-consumer"
        invented["owner_result"]["target"]["draft_id"] = "draft:invented-consumer"
        invented["public_input"]["target_locator"] = "draft:invented-consumer"

        self_linkage = copy.deepcopy(seed)
        self_linkage["owner_result"]["semantic_review"]["ai_review_gate"][
            "reviewed_linkage_sha256"
        ] = hashlib.sha256(json.dumps(
            recorded["evidence_linkage"], sort_keys=True, separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")).hexdigest()

        patched_old_result = copy.deepcopy(seed)
        patched_old_result["owner_result"] = copy.deepcopy(recorded)
        patched_old_result["owner_result"]["semantic_review"]["scope_conclusion"][
            "current_gap"
        ] = "A newly reviewed gap patched into the old complete result."

        for name, mistaken, error in (
            ("standalone_fields_without_draft_identity", mixed, "stale_identity.*target.draft_id"),
            ("body_digest", body_digest, "stale_identity.*target"),
            ("invented_draft", invented, "stale_identity.*transition.target_locator"),
            ("self_including_linkage", self_linkage, "schema_mismatch.*reviewed_linkage_sha256"),
            ("partially_patched_old_result", patched_old_result, "schema_mismatch.*scope_conclusion_sha256"),
        ):
            with self.subTest(mistake=name):
                with self.assertRaisesRegex(ValueError, error):
                    record_readiness_invocation(self.fixture, mistaken)
                # Reconstruct from the same actual source/output, dropping all
                # old derived fields; objective replay does not claim AI recovery.
                rebuilt = copy.deepcopy(seed)
                fresh, checked, ready = self.record_and_invoke(rebuilt)
                self.assertEqual("ready", ready["exit_id"])
                self.assertEqual(fresh, checked["owner_result"])
                self.assertIn("validation_receipt", checked)
                self.assertEqual(seed["transition"], checked["transition"])
                self.assertEqual(producers, prerequisites["public_outputs"])

    def test_body_revision_refreshes_real_producers_and_rejects_old_digest_and_receipt(self):
        old_seed, old_prerequisites, source = self.draft_seed()
        old_producers = copy.deepcopy(old_prerequisites["public_outputs"])
        _, old_checked, _ = self.record_and_invoke(old_seed)
        revised = copy.deepcopy(source)
        revised["body"] += "\nThe revised requirement includes a focused current-content replay."
        revised["draft_id"] = "draft:" + hashlib.sha256(revised["body"].encode()).hexdigest()
        new_seed, new_prerequisites, _ = self.draft_seed(source=revised)
        self.assertNotEqual(
            old_seed["owner_result"]["target"]["source_request_sha256"],
            new_seed["owner_result"]["target"]["source_request_sha256"],
        )
        self.assertNotEqual(
            old_producers["wording"]["transition"]["target_content_sha256"],
            new_prerequisites["public_outputs"]["wording"]["transition"]["target_content_sha256"],
        )
        old_digest = copy.deepcopy(new_seed)
        old_digest["owner_result"]["target"]["source_request_sha256"] = (
            old_seed["owner_result"]["target"]["source_request_sha256"]
        )
        with self.assertRaisesRegex(ValueError, "stale_identity.*target"):
            record_readiness_invocation(self.fixture, old_digest)
        _, new_checked, ready = self.record_and_invoke(new_seed)
        self.assertEqual("ready", ready["exit_id"])
        stale_receipt = copy.deepcopy(new_checked)
        stale_receipt["validation_receipt"] = old_checked["validation_receipt"]
        with self.assertRaisesRegex(ValueError, "stale_identity.*validation_receipt"):
            stage0_command(self.fixture, "guru-review-change-request", "invoke",
                           stale_receipt, "--invocation", "-")
        self.assertEqual(old_producers, old_prerequisites["public_outputs"])

    def test_missing_prerequisites_use_original_available_stage_or_stop(self):
        for recipe, expected_exit, expected_stage in (
            ("readiness-clarify", "clarify_requirements", "context_current"),
            ("readiness-wording", "review_wording", "clarity_current"),
        ):
            with self.subTest(stage=expected_stage):
                seed, prerequisites, _ = self.draft_seed(recipe)
                original = copy.deepcopy(prerequisites["transition"])
                self.assertEqual(expected_stage, original["stage"])
                self.assertNotIn("wording", prerequisites["public_outputs"])
                mistaken_ready = copy.deepcopy(seed)
                mistaken_ready["owner_result"]["typed_exit"] = "ready"
                with self.assertRaisesRegex(ValueError, "schema_mismatch.*transition.stage"):
                    record_readiness_invocation(self.fixture, mistaken_ready)
                absent = copy.deepcopy(seed)
                del absent["transition"]
                with self.assertRaisesRegex(ValueError, "schema_mismatch"):
                    record_readiness_invocation(self.fixture, absent)
                self.assertNotIn("validation_receipt", absent)
                _, checked, output = self.record_and_invoke(seed)
                self.assertEqual(expected_exit, output["exit_id"])
                self.assertEqual(original, output["transition"])
                self.assertEqual(original, checked["transition"])

    def test_task_commit_bindings_use_package_wrappers(self):
        runtime = SimpleNamespace()
        compose_production_owner_command_runtime(self.target, runtime)
        completed = subprocess.CompletedProcess(
            args=[], returncode=0, stdout='{"schema_version":"1.0","formal_exit":false,"result":{"status":"ok"}}\n', stderr="",
        )
        with mock.patch("adapters.eval.owner_runtime.subprocess.run", return_value=completed) as run:
            runtime.cmd_prepare_task_commit(SimpleNamespace(
                root=self.fixture,
                input=".trellis/.runtime/input.json",
                candidate_json=".trellis/.runtime/authoring.json",
            ))
            runtime.cmd_create_task_commit(SimpleNamespace(
                root=self.fixture,
                candidate_artifact=".trellis/.runtime/plans/001.json",
            ))

        prepare = run.call_args_list[0].args[0]
        create = run.call_args_list[1].args[0]
        self.assertTrue(str(prepare[0]).endswith(
            "guru-create-task-commit/scripts/prepare-task-commit.sh"
        ))
        self.assertEqual([
            "--root", str(self.fixture),
            "--input", ".trellis/.runtime/input.json",
            "--candidate-json", ".trellis/.runtime/authoring.json",
            "--json",
        ], prepare[1:])
        self.assertTrue(str(create[0]).endswith(
            "guru-create-task-commit/scripts/create-task-commit.sh"
        ))
        self.assertEqual([
            "--root", str(self.fixture),
            "--candidate-artifact", ".trellis/.runtime/plans/001.json",
            "--json",
        ], create[1:])

    def test_task_commit_candidate_binding_rewrites_public_invocation(self):
        workdir = self.root / "task-commit-case"
        workdir.mkdir(exist_ok=True)
        case = workdir / "facts.json"
        case.write_text(json.dumps({
            "public_invocation": {
                "arguments": ["--candidate-artifact", "placeholder.json"],
            },
        }) + "\n", encoding="utf-8")
        candidate = (
            self.fixture
            / ".trellis/.runtime/guru-team/task-commit-plans/current/001.json"
        )
        candidate.parent.mkdir(parents=True, exist_ok=True)
        candidate.write_text("{}\n", encoding="utf-8")

        relative = bind_task_commit_candidate_argument(
            {"workdir": str(workdir), "files": [case.name]},
            self.fixture,
            candidate,
        )

        self.assertEqual(
            ".trellis/.runtime/guru-team/task-commit-plans/current/001.json",
            relative,
        )
        payload = json.loads(case.read_text(encoding="utf-8"))
        self.assertEqual(relative, payload["public_invocation"]["arguments"][1])


class HistoricalWorkspaceAdapterTests(unittest.TestCase):
    def test_workspace_prerequisites_run_at_pinned_old_source_version(self):
        repository = next(parent for parent in SKILLS.parents if (parent / ".git").exists())
        self.assertFalse((SKILLS / "packages/guru-create-task-workspace/interface.json").exists())
        with tempfile.TemporaryDirectory(prefix="guru-pinned-old-workspace-") as temp:
            snapshot = Path(temp)
            result = subprocess.run(
                ["git", "archive", "--format=tar", PINNED_OLD_SOURCE_SHA, "trellis/skills/guru-team"],
                cwd=repository, capture_output=True, check=True,
            )
            with tarfile.open(fileobj=io.BytesIO(result.stdout)) as archive:
                archive.extractall(snapshot, filter="data")
            old_skills = snapshot / "trellis/skills/guru-team"
            self.assertTrue((old_skills / "packages/guru-create-task-workspace/interface.json").is_file())
            completed = subprocess.run(
                [sys.executable, "-B", "-m", "unittest",
                 "adapters.eval.test_stage0_fixtures.ReadinessAdapterTests."
                 "test_workspace_prerequisites_consume_production_ready_transition", "-v"],
                cwd=old_skills, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                text=True, capture_output=True, timeout=120,
            )
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            self.assertIn("Ran 1 test", completed.stderr)
            self.assertIn("OK", completed.stderr)
            self.assertNotIn("skipped", completed.stderr)


if __name__ == "__main__":
    unittest.main()
