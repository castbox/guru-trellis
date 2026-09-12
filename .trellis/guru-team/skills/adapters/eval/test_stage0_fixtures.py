from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

SKILLS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILLS))

from adapters.eval.fixture_io import run_git, write_fake_gh
from adapters.eval.owner_runtime import load_package_owner_runtime
from adapters.eval.stage0_fixtures import (
    build_readiness_owner,
    stage0_command,
    workspace_prerequisites,
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
        shutil.copytree(SKILLS / "consumers", installed / "skills/consumers", ignore=ignore)
        for skill in ("guru-sync-base", "guru-discover-change-context", "guru-clarify-requirements",
                      "guru-review-contract-wording", "guru-review-change-request", "guru-create-task-workspace"):
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

    def test_workspace_prerequisites_consume_production_ready_transition(self):
        runtime = load_package_owner_runtime(self.target, "guru-create-task-workspace")
        binary = write_fake_gh(self.root, "workspace-created")
        with mock.patch.dict(os.environ, {"PATH": f"{binary}:{os.environ['PATH']}"}):
            prerequisites, issue, transition = workspace_prerequisites(runtime, self.fixture, "workflow")
        self.assertEqual("readiness_current", transition["stage"])
        self.assertEqual([145], transition["scope"]["close_issues"])
        self.assertEqual(
            prerequisites["discovery"]["context_result_sha256"],
            transition["context_result_sha256"],
        )
        self.assertEqual(prerequisites["readiness"]["facts_sha256"], transition["readiness_facts_sha256"])
        self.assertEqual(hashlib.sha256(issue["title"].encode()).hexdigest(), transition["target"]["title_sha256"])
        self.assertFalse((self.fixture / ".trellis/tasks").exists())
        self.assertEqual("", run_git(self.fixture, "status", "--porcelain"))


if __name__ == "__main__":
    unittest.main()
