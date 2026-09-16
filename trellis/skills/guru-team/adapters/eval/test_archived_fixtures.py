"""Deterministic post-owner staging and transport, never native semantic proof."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SKILLS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILLS))

from adapters.eval import archived_fixtures as archived
from adapters.eval import production_fixtures as production
from adapters.eval.eval_constants import OWNER_INPUT
from adapters.eval.fixture_io import run_git


class ArchivedPostOwnerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="guru-archived-adapter-")
        cls.root = Path(cls.temp.name)
        cls.seed = cls.root / "installed-seed"
        installed = cls.seed / ".trellis/guru-team"
        ignore = shutil.ignore_patterns("__pycache__", "*.pyc")
        shutil.copytree(SKILLS / "runtime", installed / "runtime", ignore=ignore)
        shutil.copytree(SKILLS / "packages", installed / "skills/packages", ignore=ignore)
        shutil.copytree(SKILLS / "consumers", installed / "skills/consumers", ignore=ignore)
        repository = next(parent for parent in SKILLS.parents if (parent / ".trellis/scripts").is_dir())
        shutil.copytree(repository / ".trellis/scripts", cls.seed / ".trellis/scripts", ignore=ignore)
        shutil.copytree(repository / ".trellis/guru-team/schemas", installed / "schemas", ignore=ignore)
        shutil.copytree(repository / ".trellis/guru-team/scripts", installed / "scripts", ignore=ignore)
        shutil.copy2(repository / ".trellis/workflow.md", cls.seed / ".trellis/workflow.md")
        (cls.seed / ".gitignore").write_text(".trellis/.runtime/\n__pycache__/\n*.pyc\n")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def fixture(self, recipe, source):
        base = self.root / (("source-" if source else "installed-") + recipe)
        fixture = base / "owner-repo"
        shutil.copytree(self.seed, fixture)
        run_git(fixture, "init", "-q", "-b", "main")
        run_git(fixture, "config", "user.email", "archive-adapter@example.invalid")
        run_git(fixture, "config", "user.name", "Archive Adapter")
        runtime = fixture / ".trellis/guru-team/runtime"
        proc = subprocess.run([sys.executable, "-B", str(runtime / "bootstrap.py"), "--repo", str(fixture),
                               "--runtime-assets", str(runtime), "--python", sys.executable, "--json"],
                              text=True, capture_output=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        skill, profile = archived.RECIPES[recipe]
        package = (SKILLS / "packages" if source else self.seed / ".trellis/guru-team/skills/packages") / skill
        interface = archived.read(package / "interface.json")
        entry = next(p for p in interface["public_contracts"]["input"]["profiles"] if p["id"] == profile)
        case = base / "case"
        case.mkdir()
        public = case / "input.json"
        shutil.copy2(package / entry["example"]["path"], public)
        args = ["--input", OWNER_INPUT]
        if skill == archived.MERGE:
            args += ["--review-input", ".trellis/.runtime/guru-team/evals/merge-review.json"]
        elif skill == archived.PUBLICATION:
            args += ["--semantic-result", ".trellis/.runtime/guru-team/evals/publication-owner-input.json"]
        elif skill == archived.FINALIZER:
            args += ["--review-input", ".trellis/.runtime/guru-team/evals/semantic-review.json"]
        archived.write(case / "facts.json", {"owner_staging": {"recipe": recipe}, "public_invocation": {"arguments": args}})
        request = {"skill_id": skill, "package_root": str(package), "workdir": str(case),
                   "files": ["input.json", "facts.json"], "native_execution_mode": "post_owner"}
        target = fixture / ".trellis/guru-team/scripts/bash/run-skill-command.sh"
        return request, fixture, target, package, public

    def state(self, fixture, env):
        paths = [p for p in (fixture / ".trellis/tasks").rglob("*") if p.is_file()]
        for group in ("tasks", "workspaces"):
            paths += list((fixture / ".trellis/.runtime/guru-team" / group).glob("*.json"))
        return {"head": run_git(fixture, "rev-parse", "HEAD"), "refs": run_git(fixture, "show-ref"),
                "status": run_git(fixture, "status", "--porcelain"), "remote": run_git(fixture, "ls-remote", "origin"),
                "files": {str(p): p.read_bytes() for p in paths}, "provider": Path(env["ARCHIVED_EVAL_PROVIDER"]).read_bytes()}

    def run_case(self, recipe, *, source=False):
        request, fixture, target, package, public = self.fixture(recipe, source)
        actual_package, actual_target, env = production.stage_production_owner_execution(request, fixture, target, package, recipe, public)
        self.assertEqual(actual_package, fixture / ".trellis/guru-team/skills/packages" / request["skill_id"])
        self.assertEqual(actual_target, target)
        self.assertNotIn("GURU_TEAM_EVAL_STAGING", env)
        self.assertFalse((fixture / "trellis").exists())
        staged = archived.read(fixture / OWNER_INPUT)
        self.assertEqual(staged["profile"], archived.RECIPES[recipe][1])
        task = fixture / staged["task_ref"]
        self.assertEqual(archived.read(task / "task.json")["status"], "completed")
        summary = archived.read(task / "finish-summary.json")
        head = run_git(fixture, "rev-parse", "HEAD")
        self.assertNotIn(head, summary["git"]["commits"])
        self.assertTrue(summary["git"]["commits"])
        before = self.state(fixture, env)
        args = archived.read(Path(request["workdir"]) / "facts.json")["public_invocation"]["arguments"]
        output = archived.call(fixture, request["skill_id"], "invoke.sh", args, env)
        expected = {
            "merge-archived-review": "review_refresh_required", "review-archived-passed": "archived_review_passed",
            "review-archived-blocked": "blocked", "publication-archived-ready": "archived_ready",
            "publication-archived-metadata-blocked": "blocked", "publication-archived-task-work-blocked": "blocked",
            "publication-archived-external-blocked": "blocked", "finalization-archived-review-refresh": "ready_for_merge",
        }[recipe]
        self.assertEqual(output["exit_id"], expected)
        self.assertEqual(before, self.state(fixture, env))
        runtime = fixture / ".trellis/.runtime/guru-team"
        for name in ("review-gate.json", "pr-readiness.json", "archived-review-gate.json", "task-finalization-gate.json"):
            self.assertFalse(list(runtime.rglob(name)), name)
        calls = [json.loads(line) for line in Path(env["ARCHIVED_EVAL_LOG"]).read_text().splitlines()]
        self.assertFalse(any(row[:3] in (["gh", "pr", "merge"], ["gh", "pr", "edit"], ["gh", "issue", "close"]) for row in calls))
        self.assertFalse(any(row[0] == "git" and row[1] in {"push", "fetch", "add", "commit", "update-ref", "checkout", "merge"} for row in calls))
        if recipe.startswith("publication-archived-") and recipe.endswith("blocked"):
            semantic = archived.read(runtime / "evals/publication-owner-input.json")
            route_class = {"publication-archived-metadata-blocked": "metadata_revision", "publication-archived-task-work-blocked": "task_work",
                           "publication-archived-external-blocked": "external_blocker"}[recipe]
            self.assertEqual(semantic["findings"][0]["route_class"], route_class)

    def test_installed_only_staging_all_archived_recipes(self):
        for recipe in archived.RECIPES:
            with self.subTest(recipe=recipe):
                self.run_case(recipe)

    def test_source_request_runs_the_full_archived_prerequisite_chain(self):
        self.run_case("finalization-archived-review-refresh", source=True)

    def test_existing_recipe_dispatch_is_unchanged(self):
        request = {"skill_id": archived.FINALIZER}
        target = self.seed / ".trellis/guru-team/scripts/bash/run-skill-command.sh"
        with mock.patch.object(production, "load_package_owner_runtime", return_value=None):
            with mock.patch.object(production, "stage_finalization_owner_execution", return_value="normal-route") as normal:
                result = production.stage_production_owner_execution(request, self.seed, target, self.seed, "finalization-blocked", self.seed / "input.json")
        self.assertEqual(result, "normal-route")
        normal.assert_called_once()


if __name__ == "__main__":
    unittest.main()
