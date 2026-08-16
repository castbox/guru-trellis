from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
REPO = PACKAGE.parents[4]
TASK_REF = ".trellis/tasks/08-12-test"


class BranchReviewWrapperLifecycleTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.parent = Path(self.tmp.name)
        self.repo = self.parent / "repo"
        self.inputs = self.parent / "inputs"
        self.inputs.mkdir()
        subprocess.run(
            ["git", "init", "-q", "-b", "main", str(self.repo)], check=True
        )
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.invalid")
        (self.repo / "app.txt").write_text("base\n")
        (self.repo / ".gitignore").write_text(".trellis/.runtime/\n")
        self.git("add", ".")
        self.git("commit", "-qm", "base")
        self.base = self.git("rev-parse", "HEAD")
        self.git("switch", "-qc", "feat/test")
        (self.repo / "app.txt").write_text("feature\n")
        (self.repo / TASK_REF).mkdir(parents=True)
        (self.repo / ".trellis/tasks/08-12-other").mkdir(parents=True)
        self.git("add", ".")
        self.git("commit", "-qm", "feature")
        self.head = self.git("rev-parse", "HEAD")

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args):
        return subprocess.run(
            ["git", *args],
            cwd=self.repo,
            text=True,
            stdout=subprocess.PIPE,
            check=True,
        ).stdout.strip()

    def write(self, name, value):
        path = self.inputs / name
        path.write_text(json.dumps(value))
        return path

    def run_wrapper(self, name, *args, ok=True):
        process = subprocess.run(
            [
                str(PACKAGE / "scripts" / name),
                "--root",
                str(self.repo),
                *map(str, args),
                "--json",
            ],
            cwd=REPO,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        payload = json.loads(process.stdout or process.stderr)
        if ok:
            self.assertEqual(0, process.returncode, payload)
        else:
            self.assertNotEqual(0, process.returncode, payload)
        return payload

    def checkpoint(self):
        return (
            self.repo
            / ".trellis/.runtime/guru-team/owner-checkpoints/08-12-test/review-gate.json"
        )

    def public(self, intent="fresh_final_review"):
        return {
            "profile": "branch_review",
            "mode": "workflow",
            "task_ref": TASK_REF,
            "base_ref": self.base,
            "branch_review_commit": self.git("rev-parse", "HEAD"),
            "review_intent": intent,
        }

    def auth(self, exit_id="passed"):
        return {
            "candidate_classifications": [{
                "candidate_ref": "candidate-no-defect",
                "decision": "rejected_not_reproduced",
                "witness": {
                    "requirement_refs": ["PRD R1"],
                    "supported_entry_refs": ["entry:branch-review"],
                    "existing_caller_refs": ["caller:guru-review-branch"],
                    "honest_action_sequence": ["review the complete supported range"],
                    "defect_observation": "Current evidence does not reproduce a defect.",
                    "excluded_assumptions": [],
                },
                "consumer_use": "branch_review_route_checker",
            }],
            "semantic_review": {
                "qualified_findings": [],
                "scope_proposals": [],
                "observations": [],
                "followup_candidates": [],
                "rejected_candidates": [],
                "ai_review_gate": {
                    "status": exit_id,
                    "summary": "Reviewed the complete current base to HEAD range.",
                },
            },
            "verification_evidence": {
                "reviewer": "independent-agent-2",
                "review_source": "independent-agent",
                "evidence": ["Reviewed complete diff and tests."],
            },
        }

    def record(self, public=None, auth=None, exit_id="passed"):
        public = public or self.public()
        auth = auth or self.auth(exit_id)
        return self.run_wrapper(
            "review-branch.sh",
            "--task",
            TASK_REF,
            "--skill-input",
            self.write("public.json", public),
            "--semantic-review-file",
            self.write("auth.json", auth),
            "--typed-exit",
            exit_id,
        )

    def test_passed_record_check_invoke_retires_and_rejects_repeat(self):
        receipt = self.record()
        self.assertEqual(
            {
                "status": "recorded",
                "task_ref": TASK_REF,
                "typed_exit": "passed",
                "checkpoint_id": "review-gate",
            },
            receipt,
        )
        gate = self.checkpoint()
        self.assertTrue(gate.is_file())
        self.assertEqual("5.0", json.loads(gate.read_text())["schema_version"])
        checked = self.run_wrapper(
            "check-review-gate.sh",
            "--task",
            TASK_REF,
            "--expected-exit",
            "passed",
        )
        self.assertEqual("passed", checked["typed_exit"])
        public_path = self.inputs / "public.json"
        output = self.run_wrapper(
            "invoke.sh", "--task", TASK_REF, "--input", public_path
        )
        self.assertEqual(
            {
                "exit_id": "passed",
                "task_ref": TASK_REF,
                "branch_review_commit": self.head,
            },
            output,
        )
        self.assertFalse(gate.exists())
        repeated = self.run_wrapper(
            "invoke.sh", "--task", TASK_REF, "--input", public_path, ok=False
        )
        self.assertEqual("stale_identity", repeated["code"])

    def test_nonterminal_record_and_invoke_are_idempotent_and_retain(self):
        auth = self.auth("implementation_required")
        auth["candidate_classifications"] = [{
            "candidate_ref": "candidate-1",
            "decision": "qualified_current",
            "witness": {
                "requirement_refs": ["PRD R1"],
                "supported_entry_refs": ["entry:branch-review"],
                "existing_caller_refs": ["caller:guru-review-branch"],
                "honest_action_sequence": ["run the supported task behavior"],
                "defect_observation": "The required behavior is missing.",
                "excluded_assumptions": [],
            },
            "consumer_use": "branch_review_route_checker",
        }]
        auth["semantic_review"]["qualified_findings"] = [
            {
                "candidate_ref": "candidate-1",
                "disposition": "qualified_finding",
                "affected_behavior": "Required behavior is missing.",
                "path": "app.txt",
                "evidence_refs": ["diff:app.txt"],
                "finding_ref": "finding-1",
                "severity": "P1",
                "introduced_head": self.head,
                "fix_head": None,
                "closure_head": None,
                "status": "open",
                "closure_evidence": [],
            }
        ]
        public = self.public("initial_review")
        first = self.record(public, auth, "implementation_required")
        second = self.record(public, auth, "implementation_required")
        self.assertEqual("recorded", first["status"])
        self.assertEqual("duplicate", second["status"])
        checked = self.run_wrapper(
            "check-review-gate.sh",
            "--task",
            TASK_REF,
            "--expected-exit",
            "implementation_required",
        )
        self.assertEqual("implementation_required", checked["typed_exit"])
        public_path = self.inputs / "public.json"
        first_output = self.run_wrapper(
            "invoke.sh", "--task", TASK_REF, "--input", public_path
        )
        second_output = self.run_wrapper(
            "invoke.sh", "--task", TASK_REF, "--input", public_path
        )
        self.assertEqual(first_output, second_output)
        self.assertEqual(["finding-1"], first_output["finding_refs"])
        self.assertTrue(self.checkpoint().is_file())

    def test_stale_content_and_wrong_task_base_or_head_fail_closed(self):
        public = self.public()
        self.record(public)
        gate = self.checkpoint()
        wrong_task = self.run_wrapper(
            "check-review-gate.sh", "--task", ".trellis/tasks/08-12-other", ok=False
        )
        self.assertEqual("stale_identity", wrong_task["code"])
        for field, value in (("base_ref", self.head), ("branch_review_commit", self.base)):
            mismatched = dict(public)
            mismatched[field] = value
            result = self.run_wrapper(
                "invoke.sh",
                "--task",
                TASK_REF,
                "--input",
                self.write(f"wrong-{field}.json", mismatched),
                ok=False,
            )
            self.assertEqual("stale_identity", result["code"])
            self.assertTrue(gate.is_file())
        (self.repo / "app.txt").write_text("later\n")
        self.git("add", "app.txt")
        self.git("commit", "-qm", "later")
        stale = self.run_wrapper(
            "check-review-gate.sh", "--task", TASK_REF, ok=False
        )
        self.assertEqual("stale_identity", stale["code"])
        self.assertTrue(gate.is_file())

    def test_advanced_base_ref_fails_check_and_invoke_without_retirement(self):
        self.git("update-ref", "refs/remotes/origin/main", self.base)
        public = self.public()
        public["base_ref"] = "origin/main"
        self.record(public)
        gate = self.checkpoint()

        base_tree = self.git("rev-parse", f"{self.base}^{{tree}}")
        advanced_base = self.git(
            "commit-tree", base_tree, "-p", self.base, "-m", "advance base ref"
        )
        self.git("update-ref", "refs/remotes/origin/main", advanced_base)
        self.assertEqual(self.head, self.git("rev-parse", "HEAD"))

        checked = self.run_wrapper(
            "check-review-gate.sh", "--task", TASK_REF, ok=False
        )
        self.assertEqual("stale_identity", checked["code"])
        self.assertEqual("base_ref", checked["field_path"])
        self.assertTrue(gate.is_file())

        invoked = self.run_wrapper(
            "invoke.sh",
            "--task",
            TASK_REF,
            "--input",
            self.inputs / "public.json",
            ok=False,
        )
        self.assertEqual("stale_identity", invoked["code"])
        self.assertEqual("base_ref", invoked["field_path"])
        self.assertTrue(gate.is_file())

    def test_symlink_checkpoint_and_ancestor_fail_closed(self):
        public = self.public()
        self.record(public)
        gate = self.checkpoint()
        saved = self.inputs / "saved-gate.json"
        gate.replace(saved)
        gate.symlink_to(saved)
        result = self.run_wrapper(
            "check-review-gate.sh", "--task", TASK_REF, ok=False
        )
        self.assertEqual("unsafe_path", result["code"])
        gate.unlink()
        owner = gate.parent
        owner.rmdir()
        owner.symlink_to(self.inputs, target_is_directory=True)
        ancestor = self.run_wrapper(
            "review-branch.sh",
            "--task",
            TASK_REF,
            "--skill-input",
            self.inputs / "public.json",
            "--semantic-review-file",
            self.inputs / "auth.json",
            "--typed-exit",
            "passed",
            ok=False,
        )
        self.assertEqual("unsafe_path", ancestor["code"])

    def test_unsafe_task_locator_fails_closed(self):
        result = self.run_wrapper(
            "check-review-gate.sh", "--task", "../outside", ok=False
        )
        self.assertEqual("unsafe_path", result["code"])

    def test_blocked_projects_and_retires(self):
        public = self.public("initial_review")
        self.record(public, self.auth("blocked"), "blocked")
        output = self.run_wrapper(
            "invoke.sh", "--task", TASK_REF, "--input", self.inputs / "public.json"
        )
        self.assertEqual({"exit_id": "blocked"}, output)
        self.assertFalse(self.checkpoint().exists())

    def test_base_continuity_projects_pair_and_retires(self):
        self.git("switch", "main")
        (self.repo / "base.txt").write_text("advance\n")
        self.git("add", "base.txt")
        self.git("commit", "-qm", "advance base")
        new_base = self.git("rev-parse", "HEAD")
        self.git("switch", "feat/test")
        public = {
            "profile": "base_continuity",
            "mode": "workflow",
            "task_ref": TASK_REF,
            "task_head": self.head,
            "branch_review_commit": self.head,
            "old_base_head": self.base,
            "new_base_head": new_base,
            "candidate_tree_sha256": "d" * 64,
            "relevant_paths": ["base.txt"],
            "resume_target": "publication_review",
            "review_intent": "base_continuity",
        }
        self.record(public, self.auth("continuity_passed"), "continuity_passed")
        output = self.run_wrapper(
            "invoke.sh",
            "--task",
            TASK_REF,
            "--input",
            self.inputs / "public.json",
        )
        self.assertEqual("continuity_passed", output["exit_id"])
        self.assertEqual(new_base, output["new_base_head"])
        self.assertNotIn("relevant_paths", output)
        self.assertFalse(self.checkpoint().exists())


class BranchReviewContractTest(unittest.TestCase):
    def test_official_reviewer_dispatch_is_candidate_only_before_fresh_qualification(self):
        repo = PACKAGE.parents[4]
        sources = {
            "workflow": repo / "trellis/workflows/guru-team/workflow.md",
            "skill": PACKAGE / "SKILL.md",
            "contract": PACKAGE / "references/contract.md",
        }
        candidate_fields = (
            "candidate_ref",
            "observed_behavior",
            "locators",
            "minimal_reproduction_hint",
        )
        for label, path in sources.items():
            with self.subTest(source=label):
                text = path.read_text(encoding="utf-8")
                normalized = " ".join(text.split())
                self.assertIn("approved-plan work only", normalized)
                self.assertIn("fresh", normalized)
                self.assertIn("qualification", normalized)
                self.assertIn("self-fix", normalized)
                for field in candidate_fields:
                    self.assertIn(field, text)
        self.assertIn(
            "Upstream-owned `trellis-*` agent files stay",
            sources["skill"].read_text(encoding="utf-8"),
        )

    def test_current_interface_wording_matches_profiles_gate_and_exits(self):
        interface = json.loads((PACKAGE / "interface.json").read_text())
        public = interface["public_contracts"]
        self.assertEqual(
            "guru-production-review-branch-input-aggregate-3.0",
            public["input"]["aggregate_schema"]["schema_id"],
        )
        self.assertEqual(
            ["branch_review", "base_continuity"],
            [profile["id"] for profile in public["input"]["profiles"]],
        )
        self.assertEqual(
            "https://github.com/castbox/guru-trellis/schemas/guru-review-gate-5.0.json",
            public["private_artifacts"][0]["schema"]["schema_id"],
        )
        self.assertEqual(
            [
                "passed",
                "continuity_passed",
                "implementation_required",
                "scope_confirmation_required",
                "blocked",
            ],
            [output["exit_id"] for output in public["outputs"]],
        )
        self.assertNotIn("--owner-result", public["invocation"]["example_argv"])
        for facts_path in sorted((PACKAGE / "evals/files").glob("*facts.json")):
            facts = json.loads(facts_path.read_text())
            arguments = facts["public_invocation"]["arguments"]
            self.assertNotIn("--owner-result", arguments, facts_path)
        for path in (
            PACKAGE / "SKILL.md",
            PACKAGE / "references/contract.md",
        ):
            text = path.read_text()
            self.assertIn("base_continuity", text)
            self.assertIn("schema 3.0", text)
            self.assertIn("schema 5.0", text)
            self.assertIn("schemas 3.0 and 4.0", text)
            self.assertIn("continuity_passed", text)

    def test_wrappers_are_executable(self):
        for name in ("review-branch.sh", "check-review-gate.sh", "invoke.sh"):
            self.assertTrue(os.access(PACKAGE / "scripts" / name, os.X_OK))


if __name__ == "__main__":
    unittest.main()
