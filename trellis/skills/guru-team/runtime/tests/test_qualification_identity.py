"""Public qualifier facts after real original Task/Scope/Delivery owners.

Fixture semantic payloads exercise deterministic transport, not native AI
qualification. Native current-host/caller observations are separate evidence.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

SKILLS = Path(__file__).resolve().parents[2]
PACKAGES = SKILLS / "packages"
sys.path.insert(0, str(SKILLS))
from runtime.delivery_projection.adapter import authority_ref
from runtime.qualification_facts import file_set_identity

spec = importlib.util.spec_from_file_location("qualification_creation_fixture", PACKAGES / "guru-create-task/tests/test_contract.py")
creation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(creation)


class QualificationIdentityTest(unittest.TestCase):
    def setUp(self):
        # Absence is an explicit fixture condition, never native context proof.
        environment = {k: v for k, v in os.environ.items()
                       if not k.startswith(("TRELLIS_", "CODEX_", "CLAUDE_", "CURSOR_", "GIT_"))}
        # Preserve the deliberately selected reviewed upstream source locator.
        for field in ("GURU_UPSTREAM_DELIVERY_SCRIPTS", "TRELLIS_FIXED_FORK_SOURCE"):
            if field in os.environ:
                environment[field] = os.environ[field]
        self.environment = patch.dict(os.environ, environment, clear=True)
        self.environment.start()
        self.addCleanup(self.environment.stop)
        fixture = creation.CreateTaskTests("test_public_no_issue_creation_recovery_and_source_identity")
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.fixture, self.root = fixture, fixture.root.resolve()
        created = self.owner("guru-create-task", fixture.payload)
        self.assertEqual(created["exit_id"], "created", created)
        installed = self.root / ".trellis/guru-team"
        shutil.copytree(SKILLS / "runtime", installed / "runtime", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        for name in ("schemas", "contracts", "consumers"):
            shutil.copytree(SKILLS / name, installed / "skills" / name)
        shutil.copytree(PACKAGES, installed / "skills/packages", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        initialized = subprocess.run([sys.executable, "-S", str(installed / "runtime/bootstrap.py"),
            "--repo", str(self.root), "--runtime-assets", str(installed / "runtime"), "--repair", "--python", sys.executable, "--json"],
            text=True, capture_output=True)
        self.assertEqual(initialized.returncode, 0, initialized.stdout + initialized.stderr)
        self.ref = created["task_ref"]
        task = self.root / self.ref
        (task / "prd.md").write_text("# Whole requirements\n\nAC01: qualifier identity remains current.\n")
        source = [{"locator": "README.md", "section": "Requirements", "authority_kind": "requirement"}]
        public = {"profile": "task_scope_requirements_acceptance", "mode": "workflow", "task_ref": self.ref,
                  "requirements_locator": self.ref + "/prd.md", "source_selection": source, "revision_refs": ["README.md#Requirements"]}
        result = {"public_input": public, "typed_exit": "scope_ready", "reason": "Fixture reviewed scope transport.",
                  "ai_review_gate": {"status": "passed", "summary": "Factual fixture only."},
                  "source_selection": source, "revision_refs": public["revision_refs"], "scope_action": "revised",
                  "authority": authority_ref(task / "prd.md", self.root)}
        scope = self.owner("guru-clarify-requirements", {"public_input": public, "owner_result": result}, flag="--invocation")
        self.assertEqual(scope["exit_id"], "scope_ready", scope)
        identity = self.owner("guru-establish-task-identity", {"profile": "delivery_active_task", "mode": "workflow",
            "task_id": created["task_id"], "task_ref": self.ref, "lifecycle_generation": 0})
        self.assertEqual(identity["exit_id"], "identity_established", identity)
        ensured = self.owner("guru-ensure-task-checkout", {"profile": "delivery_active_task", "mode": "workflow",
            "task_id": identity["task_id"], "lifecycle_generation": identity["lifecycle_generation"]})
        self.assertEqual(ensured["exit_id"], "checkout_resolved", ensured)
        bind = {"profile": "delivery_rebind_missing_session", "mode": "workflow", "task_id": identity["task_id"],
                "lifecycle_generation": 0, "continuation_id": "qualification-fixture-bind"}
        bound = self.owner("guru-bind-task-session", bind, owner={**bind, "route": "rebind", "resume_target": "phase-1",
            "ai_review_gate": {"status": "passed", "summary": "Exact fixture lifecycle transport."}})
        self.assertEqual(bound["exit_id"], "explicit_task_mode", bound)
        delivery = self.owner("guru-create-delivery", {"profile": "delivery_creation", "mode": "workflow", "task_ref": self.ref,
            "task_key": scope["task_key"], "scope_ref": {"authority": result["authority"], "anchors": ["AC01"]},
            "delivery_profile": "pull_request", "continuation_id": "qualification-fixture-d1", "action": "create"},
            owner={"typed_exit": "created", "reason": "Fixture one independent slice."})
        self.assertEqual(delivery["exit_id"], "created", delivery)
        self.key = delivery["delivery_key"]
        self.directory = task / delivery["planning_root"]
        for filename in ("prd.md", "design.md", "implement.md"):
            (self.directory / filename).write_text("# Current " + filename + "\n")
        self.paths = [(self.directory / filename).relative_to(self.root).as_posix()
                      for filename in ("prd.md", "design.md", "implement.md")]
        self.head = fixture.git("rev-parse", "HEAD")

    def owner(self, skill, public, *, flag="--input", owner=None):
        package = (PACKAGES if skill == "guru-create-task" else self.root / ".trellis/guru-team/skills/packages") / skill
        args = ["bash", str(package / "scripts/invoke.sh")]
        if skill != "guru-clarify-requirements":
            args.extend(["--root", str(self.root)])
        args.extend([flag, "-"])
        if owner is not None:
            args.extend(["--owner-result", json.dumps(owner)])
        process = subprocess.run(args, cwd=self.root, input=json.dumps(public), text=True, capture_output=True)
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        return json.loads(process.stdout)

    def semantic(self, name, profile="implementation_discovery"):
        package = self.root / ".trellis/guru-team/skills/packages" / ("guru-qualify-" + name)
        result = json.loads((package / "examples/semantic-result.json").read_text())
        public = json.loads((package / ("examples/public-" + profile.replace("_", "-") + "-input-2.0.json")).read_text())
        public.update(target_locator=self.ref)
        public["candidate_locators"] = [{"candidate_ref": ref, "locators": ["path:README.md"]} for ref in public["candidate_refs"]]
        target = public["target"]
        target.update(repo_locator=".", task_ref=self.ref, delivery_key=self.key)
        if "planning_identity" in target:
            target["planning_identity"] = file_set_identity(self.root, self.paths)
        if "planning_paths" in target:
            target["planning_paths"] = self.paths
        if "author_identity" in target:
            target.update(author_paths=[self.ref + "/prd.md"], author_identity=file_set_identity(self.root, [self.ref + "/prd.md"]))
        for field in ("checkout_head", "task_head", "review_head", "review_commit", "base_head", "old_base_head", "new_base_head"):
            if field in target:
                target[field] = self.head
        # Current semantic examples have one candidate; retain their shape and
        # independently bind that candidate to the fixture's live public input.
        ref = result["candidate_results"][0]["candidate_ref"]
        public["candidate_refs"] = [ref]
        public["candidate_locators"] = [{"candidate_ref": ref, "locators": ["path:README.md"]}]
        result["public_input"] = public
        result["ai_review_gate"]["reviewed_candidate_refs"] = [ref]
        return result

    def invoke(self, name, result, expected=0):
        wrapper = self.root / ".trellis/guru-team/skills/packages" / ("guru-qualify-" + name) / "scripts/invoke.sh"
        process = subprocess.run(["bash", str(wrapper), "--invocation", "-"], cwd=self.root,
            input=json.dumps({"schema_version": "1.0", "semantic_result": result}), text=True, capture_output=True)
        self.assertEqual(process.returncode, expected, process.stdout + process.stderr)
        return json.loads(process.stdout)

    def test_three_public_wrappers_accept_real_explicit_identity_and_keep_continuation(self):
        runtime_root = self.root / ".trellis/.runtime"
        before_runtime = {p.relative_to(runtime_root).as_posix(): p.read_bytes() for p in runtime_root.rglob("*") if p.is_file()}
        for name in ("normal-scenario", "solution-mechanism", "root-cause"):
            with self.subTest(owner=name):
                result = self.semantic(name)
                before = (self.root / self.ref / "task.json").read_bytes()
                output = self.invoke(name, result)
                self.assertEqual(output["exit_id"], "classified", output)
                self.assertEqual(output["profile"], "implementation_discovery")
                self.assertEqual((self.root / self.ref / "task.json").read_bytes(), before)
        for profile in ("author_candidate_set", "planning_scenario_set", "base_impact_candidate_set",
                        "phase2_candidate_set", "branch_review_candidate_set", "publication_candidate_set"):
            with self.subTest(profile=profile):
                output = self.invoke("normal-scenario", self.semantic("normal-scenario", profile))
                self.assertEqual((output["exit_id"], output["profile"]), ("classified", profile))
        self.assertEqual({p.relative_to(runtime_root).as_posix(): p.read_bytes() for p in runtime_root.rglob("*") if p.is_file()}, before_runtime)

    def test_planning_and_candidate_revisions_reject_original_input(self):
        original = self.semantic("normal-scenario")
        (self.directory / "design.md").write_text("# Ordinary design revision\n")
        error = self.invoke("normal-scenario", original, expected=3)
        self.assertEqual((error["code"], error["field_path"]), ("stale_identity", "public_input.target.planning_identity"))
        refreshed = self.semantic("normal-scenario")
        (self.root / "README.md").unlink()
        error = self.invoke("normal-scenario", refreshed, expected=3)
        self.assertEqual(error["field_path"], "candidate." + refreshed["public_input"]["candidate_refs"][0])

    def test_wrong_delivery_generation_and_planning_set_are_rejected(self):
        for name in ("normal-scenario", "solution-mechanism", "root-cause"):
            result = self.semantic(name)
            result["public_input"]["target"]["delivery_key"] = {**self.key, "lifecycle_generation": 1}
            self.assertEqual(self.invoke(name, result, expected=3)["code"], "stale_identity")
        result = self.semantic("normal-scenario", "planning_scenario_set")
        other = self.root / "docs/other-plan"
        other.mkdir(parents=True)
        for filename in ("prd.md", "design.md", "implement.md"):
            (other / filename).write_text("# Another existing plan: " + filename + "\n")
        wrong = [(other / filename).relative_to(self.root).as_posix()
                 for filename in ("prd.md", "design.md", "implement.md")]
        result["public_input"]["target"].update(planning_paths=wrong,
            planning_identity=file_set_identity(self.root, wrong))
        error = self.invoke("normal-scenario", result, expected=3)
        self.assertEqual(error["field_path"], "public_input.target.planning_paths")

    def test_author_needs_only_existing_source_and_checkout_remains_current(self):
        for filename in ("design.md", "implement.md"):
            (self.directory / filename).unlink()
        # Author has no planning_identity and does not need future bodies.
        self.assertEqual(self.invoke("normal-scenario", self.semantic("normal-scenario", "author_candidate_set"))["exit_id"], "classified")
        self.fixture.git("switch", "--detach", self.head)
        error = self.invoke("normal-scenario", self.semantic("normal-scenario", "author_candidate_set"), expected=3)
        self.assertEqual(error["code"], "stale_identity")


if __name__ == "__main__":
    unittest.main()
