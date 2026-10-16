from __future__ import annotations

import hashlib
import json
import os
import signal
import subprocess
import tempfile
import unittest
import sys
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
REPO = PACKAGE.parents[4]
TASK_REF = ".trellis/tasks/08-12-test"
sys.path.insert(0, str(PACKAGE.parents[1]))
from runtime.io import project_intermediate_receipt


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
        metadata_files = {
            ".trellis/tasks/archive/old/task.json": "archived\n",
            ".trellis/workspace/test/journal.md": "journal\n",
            ".trellis/.runtime/tracked-state.json": "runtime\n",
            ".trellis/guru-team/extension.json": "provenance\n",
            ".DS_Store": "os noise\n",
            "nested/.DS_Store": "nested os noise\n",
        }
        for relative, content in metadata_files.items():
            target = self.repo / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
        self.git("add", ".")
        self.git("add", "-f", ".trellis/.runtime/tracked-state.json")
        self.git("commit", "-qm", "feature")
        self.head = self.git("rev-parse", "HEAD")

    def tearDown(self):
        self.tmp.cleanup()

    def test_contract_keeps_eof_blank_lines_non_blocking_but_narrow(self):
        skill = (PACKAGE / "SKILL.md").read_text()
        contract = (PACKAGE / "references/contract.md").read_text()
        for text in (skill, contract):
            self.assertIn("extra blank line", text)
            self.assertIn("non-blocking", text)
            self.assertIn("trailing", text)
            self.assertIn("spaces", text)
            self.assertIn("indentation", text)

    def test_contract_requires_dialogue_visible_review_lifecycle_and_final_pass(self):
        skill = (PACKAGE / "SKILL.md").read_text()
        contract = (PACKAGE / "references/contract.md").read_text()
        for text in (skill, contract):
            normalized = " ".join(text.split())
            self.assertIn("independent reviewer identity", normalized)
            self.assertIn("exact committed `base_oid..head_oid` range", normalized)
            self.assertIn("final finding summary", normalized)
            self.assertIn("dialogue", normalized)
            self.assertIn("public wrapper return `passed`", normalized)
            self.assertIn("provisional", normalized)
            self.assertRegex(
                normalized,
                r"(?:do not persist|do not enter).*(?:gate|DTO|checkpoint|tracked)",
            )

    def test_eof_blank_line_reproduces_blocking_route_when_qualified(self):
        """Pre-change behavior: a qualified EOF-only candidate blocks review."""
        auth = self.auth("implementation_required")
        auth["candidate_classifications"] = [{
            "candidate_ref": "candidate:eof-blank-line",
            "decision": "qualified_current",
            "witness": {
                "requirement_refs": ["formatting contract"],
                "supported_entry_refs": ["entry:branch-review"],
                "existing_caller_refs": ["caller:guru-review-branch"],
                "honest_action_sequence": ["review the committed text file"],
                "defect_observation": "The file ends with an extra blank line.",
                "excluded_assumptions": [],
            },
            "consumer_use": "branch_review_route_checker",
        }]
        auth["semantic_review"]["qualified_findings"] = [{
            "candidate_ref": "candidate:eof-blank-line",
            "disposition": "qualified_finding",
            "affected_behavior": "The file ends with an extra blank line.",
            "path": "app.txt",
            "evidence_refs": ["diff:app.txt"],
            "finding_ref": "finding:eof-blank-line",
            "severity": "P1",
            "introduced_head": self.head,
            "fix_head": None,
            "closure_head": None,
            "status": "open",
            "closure_evidence": [],
        }]
        receipt = self.record(
            self.public("initial_review"), auth, "implementation_required"
        )
        self.assertEqual("recorded", receipt["status"])
        checked = self.run_wrapper(
            "check-review-gate.sh",
            "--task",
            TASK_REF,
            "--expected-exit",
            "implementation_required",
        )
        self.assertEqual("implementation_required", checked["typed_exit"])

    def test_eof_blank_line_is_non_blocking_after_policy(self):
        """Post-change behavior: the same EOF-only candidate is rejected."""
        (self.repo / "app.txt").write_text("feature\n\n")
        self.git("commit", "-qam", "add an EOF-only blank line")
        self.head = self.git("rev-parse", "HEAD")
        auth = self.auth("passed")
        auth["candidate_classifications"] = [{
            "candidate_ref": "candidate:eof-blank-line",
            "decision": "rejected_not_reproduced",
            "witness": {
                "requirement_refs": ["formatting contract"],
                "supported_entry_refs": ["entry:branch-review"],
                "existing_caller_refs": ["caller:guru-review-branch"],
                "honest_action_sequence": ["review the committed text file"],
                "defect_observation": "Only an EOF blank line is present; no semantic defect is reproduced.",
                "excluded_assumptions": ["EOF-only whitespace is not a blocking finding."],
            },
            "consumer_use": "branch_review_route_checker",
        }]
        auth["semantic_review"]["rejected_candidates"] = [{
            "candidate_ref": "candidate:eof-blank-line",
            "disposition": "rejected_candidate",
            "affected_behavior": "Only an EOF blank line is present.",
            "path": "app.txt", "evidence_refs": ["diff:app.txt"],
        }]
        receipt = self.record(
            self.public("initial_review"), auth, "passed"
        )
        self.assertEqual("recorded", receipt["status"])
        checked = self.run_wrapper(
            "check-review-gate.sh",
            "--task",
            TASK_REF,
            "--expected-exit",
            "passed",
        )
        self.assertEqual("owner_checkpoint_validated", checked["status"])
        self.assertFalse(checked["formal_exit"])
        self.assertEqual("passed", checked["typed_exit"])
        output = self.run_wrapper(
            "invoke.sh", "--task", TASK_REF,
            "--input", self.write("eof.json", self.public("initial_review"))
        )
        self.assertEqual("passed", output["exit_id"])

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
        child = subprocess.Popen(
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
            start_new_session=hasattr(self, "wrapper_timeout"),
        )
        try:
            stdout, stderr = child.communicate(timeout=getattr(self, "wrapper_timeout", None))
        except subprocess.TimeoutExpired:
            # Only this probe's process group belongs to the test.
            os.killpg(child.pid, signal.SIGKILL)
            stdout, stderr = child.communicate()
            self.fail(f"{name} did not complete within 60s: {stderr}")
        process = subprocess.CompletedProcess(child.args, child.returncode, stdout, stderr)
        payload = json.loads(process.stdout or process.stderr)
        if ok:
            self.assertEqual(0, process.returncode, payload)
        else:
            self.assertNotEqual(0, process.returncode, payload)
        return project_intermediate_receipt(payload, PACKAGE.parents[1] / "schemas") if ok and name != "invoke.sh" else payload

    def checkpoint(self):
        return (
            self.repo
            / ".trellis/.runtime/guru-team/owner-checkpoints/08-12-test/review-gate.json"
        )

    def tree_identity(self, commit):
        raw = subprocess.run(
            ["git", "ls-tree", "-r", "-z", "--full-tree", commit],
            cwd=self.repo,
            stdout=subprocess.PIPE,
            check=True,
        ).stdout
        rows = []
        blob_digests = {}
        for entry in raw.split(b"\0"):
            if not entry:
                continue
            metadata, _, path = entry.partition(b"\t")
            mode, kind, oid = metadata.split()
            if mode == b"160000" and kind == b"commit":
                rows.append(path + b"\0" + mode + b"\0" + oid + b"\0")
                continue
            if kind != b"blob":
                continue
            if oid not in blob_digests:
                blob = subprocess.run(
                    ["git", "cat-file", "blob", oid.decode("ascii")],
                    cwd=self.repo,
                    stdout=subprocess.PIPE,
                    check=True,
                ).stdout
                blob_digests[oid] = hashlib.sha256(blob).hexdigest().encode()
            rows.append(path + b"\0" + blob_digests[oid] + b"\0")
        return hashlib.sha256(b"".join(rows)).hexdigest()

    def continuity_public(self):
        prior_review = self.head
        self.git("switch", "main")
        (self.repo / "base.txt").write_text("advance\n")
        self.git("add", "base.txt")
        self.git("commit", "-qm", "advance base")
        new_base = self.git("rev-parse", "HEAD")
        self.git("switch", "feat/test")
        self.git("merge", "--no-ff", "-m", "reconcile base", new_base)
        task_head = self.git("rev-parse", "HEAD")
        return {
            "profile": "base_continuity",
            "mode": "workflow",
            "task_ref": TASK_REF,
            "task_head": task_head,
            "branch_review_commit": prior_review,
            "old_base_head": self.base,
            "new_base_head": new_base,
            "candidate_tree_sha256": self.tree_identity(task_head),
            "relevant_paths": ["base.txt"],
            "resume_target": "publication_review",
            "review_intent": "base_continuity",
        }

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
            "delivery_review": {
                "task_scope": ["R1", "R2"],
                "delivery_slice": ["R1"],
                "remaining_work": ["R2"],
                "independent_delivery_conditions": [
                    "R1 is independently usable and verifiable."
                ],
                "validation_boundaries": [
                    "R1 checks passed; R2 remains disclosed future work."
                ],
                "current_slice_status": "passed",
                "remaining_work_status": "disclosed",
                "summary": (
                    "The complete committed range satisfies the current slice "
                    "without claiming remaining work complete."
                ),
            },
            "candidate_classifications": [],
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

    def record(self, public=None, auth=None, exit_id="passed", ok=True):
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
            ok=ok,
        )

    def test_passed_record_check_invoke_retires_and_rejects_repeat(self):
        receipt = self.record()
        self.assertEqual(
            {
                "status": "recorded",
                "formal_exit": False,
                "task_ref": TASK_REF,
                "typed_exit": "passed",
                "checkpoint_id": "review-gate",
            },
            receipt,
        )
        gate = self.checkpoint()
        self.assertTrue(gate.is_file())
        self.assertEqual("7.0", json.loads(gate.read_text())["schema_version"])
        self.assertEqual(
            self.auth()["delivery_review"],
            json.loads(gate.read_text())["delivery_review"],
        )
        checked = self.run_wrapper(
            "check-review-gate.sh",
            "--task",
            TASK_REF,
            "--expected-exit",
            "passed",
        )
        self.assertEqual("owner_checkpoint_validated", checked["status"])
        self.assertFalse(checked["formal_exit"])
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

    def test_initial_review_zero_candidates_uses_original_full_chain(self):
        public = self.public("initial_review")
        self.record(public, self.auth())
        self.assertEqual([], json.loads(self.checkpoint().read_text())["candidate_classifications"])
        self.assertEqual("passed", self.run_wrapper(
            "check-review-gate.sh", "--task", TASK_REF,
        )["typed_exit"])
        self.assertEqual("passed", self.run_wrapper(
            "invoke.sh", "--task", TASK_REF,
            "--input", self.write("initial-zero.json", public),
        )["exit_id"])
        self.assertFalse(self.checkpoint().exists())

    def test_zero_candidates_do_not_admit_unclassified_dispositions(self):
        for key, disposition in (
            ("observations", "observation"),
            ("followup_candidates", "followup_candidate"),
            ("rejected_candidates", "rejected_candidate"),
        ):
            with self.subTest(key=key):
                auth = self.auth()
                auth["semantic_review"][key] = [{
                    "candidate_ref": "candidate:unclassified",
                    "disposition": disposition,
                    "affected_behavior": "The owner omitted this candidate classification.",
                    "path": "app.txt", "evidence_refs": ["diff:app.txt"],
                }]
                result = self.record(auth=auth, ok=False)
                self.assertEqual("candidate_classifications", result["field_path"])
                self.assertFalse(self.checkpoint().exists())

    def test_zero_candidates_still_require_complete_review_evidence(self):
        auth = self.auth()
        auth["verification_evidence"]["evidence"] = []
        result = self.record(auth=auth, ok=False)
        self.assertEqual("schema_mismatch", result["code"])
        self.assertFalse(self.checkpoint().exists())

    def test_record_and_check_allow_canonical_metadata_only_dirty_paths(self):
        metadata_changes = {
            f"{TASK_REF}/review.md": "current task review\n",
            ".trellis/tasks/archive/old/task.json": "updated archive\n",
            ".trellis/workspace/test/status\nnote.md": "newline path\n",
            ".trellis/.runtime/tracked-state.json": "updated runtime\n",
            ".trellis/guru-team/extension.json": "updated provenance\n",
            ".DS_Store": "updated os noise\n",
            "nested/.DS_Store": "updated nested os noise\n",
        }
        for relative, content in metadata_changes.items():
            target = self.repo / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
        self.git(
            "mv",
            ".trellis/workspace/test/journal.md",
            ".trellis/tasks/archive/old/journal.md",
        )

        receipt = self.record()
        self.assertEqual("recorded", receipt["status"])
        checked = self.run_wrapper(
            "check-review-gate.sh",
            "--task",
            TASK_REF,
            "--expected-exit",
            "passed",
        )
        self.assertEqual("passed", checked["typed_exit"])

    def test_record_and_check_reject_included_dirty_content(self):
        (self.repo / "app.txt").write_text("dirty before record\n")
        record_result = self.record(ok=False)
        self.assertEqual("stale_identity", record_result["code"])
        self.assertEqual("worktree", record_result["field_path"])

        (self.repo / "app.txt").write_text("feature\n")
        self.record()
        self.git("mv", "app.txt", ".trellis/workspace/test/app.txt")
        check_result = self.run_wrapper(
            "check-review-gate.sh", "--task", TASK_REF, ok=False
        )
        self.assertEqual("stale_identity", check_result["code"])
        self.assertEqual("worktree", check_result["field_path"])

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

    def test_shared_ref_advance_preserves_fixed_review(self):
        self.git("update-ref", "refs/remotes/origin/main", self.base)
        public = self.public()
        self.record(public)
        base_tree = self.git("rev-parse", f"{self.base}^{{tree}}")
        advanced = self.git("commit-tree", base_tree, "-p", self.base, "-m", "independent advance")
        self.git("update-ref", "refs/remotes/origin/main", advanced)
        checked = self.run_wrapper("check-review-gate.sh", "--task", TASK_REF)
        self.assertEqual("passed", checked["typed_exit"])
        output = self.run_wrapper("invoke.sh", "--task", TASK_REF, "--input", self.inputs / "public.json")
        self.assertEqual("passed", output["exit_id"])
        self.assertEqual(self.head, self.git("rev-parse", "HEAD"))
        self.assertFalse(self.checkpoint().exists())

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
        public = self.continuity_public()
        head_before = self.git("rev-parse", "HEAD")
        count_before = self.git("rev-list", "--count", "HEAD")
        self.record(public, self.auth("continuity_passed"), "continuity_passed")
        gate = json.loads(self.checkpoint().read_text())
        self.assertEqual("7.0", gate["schema_version"])
        self.assertEqual(public["task_head"], gate["review_commit"])
        self.assertEqual(
            public["branch_review_commit"],
            gate["integration_pair"]["prior_branch_review_commit"],
        )
        checked = self.run_wrapper(
            "check-review-gate.sh",
            "--task",
            TASK_REF,
            "--expected-exit",
            "continuity_passed",
        )
        self.assertEqual(public["task_head"], checked["review_commit"])
        output = self.run_wrapper(
            "invoke.sh",
            "--task",
            TASK_REF,
            "--input",
            self.inputs / "public.json",
        )
        self.assertEqual("continuity_passed", output["exit_id"])
        self.assertEqual(public["new_base_head"], output["new_base_head"])
        self.assertEqual(public["task_head"], output["branch_review_commit"])
        self.assertNotEqual(public["branch_review_commit"], output["branch_review_commit"])
        self.assertNotIn("prior_branch_review_commit", output)
        self.assertNotIn("relevant_paths", output)
        self.assertFalse(self.checkpoint().exists())
        self.assertEqual(head_before, self.git("rev-parse", "HEAD"))
        self.assertEqual(count_before, self.git("rev-list", "--count", "HEAD"))

    def test_large_committed_tree_continuity_completes_with_original_identity(self):
        """A normal large tree must finish the real recorder/checker/invoke chain."""
        self.wrapper_timeout = 60
        files = self.repo / "objects"
        files.mkdir()
        # Repeated OIDs remain separate requests, as in ordinary copied assets.
        content = bytes(range(256)) * 16
        for index in range(4096):
            (files / f"copy-{index:04d}.bin").write_bytes(content)
        (files / "00-large.bin").write_bytes(bytes(range(256)) * 4096)
        (files / "empty.txt").write_bytes(b"")
        executable = files / "run.sh"
        executable.write_text("#!/bin/sh\nexit 0\n")
        executable.chmod(0o755)
        (files / "link").symlink_to("copy-0000.bin")
        (self.repo / "submodule").mkdir()
        self.git("add", "objects")
        self.git("update-index", "--add", "--cacheinfo", f"160000,{self.head},submodule")
        self.git("commit", "-qm", "add normal large asset tree")
        self.head = self.git("rev-parse", "HEAD")
        public = self.continuity_public()
        before = (
            self.git("rev-parse", "HEAD"),
            self.git("ls-files", "--stage"),
            self.git("show-ref"),
            self.git("status", "--porcelain=v1"),
        )
        self.assertEqual("", before[-1])
        self.record(public, self.auth("continuity_passed"), "continuity_passed")
        gate = json.loads(self.checkpoint().read_text())
        self.assertEqual(public["candidate_tree_sha256"], gate["integration_pair"]["candidate_tree_sha256"])
        checked = self.run_wrapper(
            "check-review-gate.sh", "--task", TASK_REF,
            "--expected-exit", "continuity_passed",
        )
        self.assertEqual("continuity_passed", checked["typed_exit"])
        output = self.run_wrapper(
            "invoke.sh", "--task", TASK_REF,
            "--input", self.inputs / "public.json",
        )
        self.assertEqual({
            "exit_id": "continuity_passed",
            "task_ref": TASK_REF,
            "task_head": public["task_head"],
            "branch_review_commit": public["task_head"],
            "old_base_head": public["old_base_head"],
            "new_base_head": public["new_base_head"],
            "candidate_tree_sha256": public["candidate_tree_sha256"],
            "resume_target": public["resume_target"],
        }, output)
        self.assertFalse(self.checkpoint().exists())
        self.assertEqual(before, (
            self.git("rev-parse", "HEAD"),
            self.git("ls-files", "--stage"),
            self.git("show-ref"),
            self.git("status", "--porcelain=v1"),
        ))

    def test_base_continuity_rejects_stale_head_prior_review_base_and_tree(self):
        public = self.continuity_public()
        unrelated_tree = self.git("rev-parse", f"{self.base}^{{tree}}")
        unrelated = self.git("commit-tree", unrelated_tree, "-m", "unrelated")
        future_base = self.git(
            "commit-tree",
            self.git("rev-parse", f"{public['new_base_head']}^{{tree}}"),
            "-p",
            public["new_base_head"],
            "-m",
            "future base",
        )
        cases = (
            ("task_head", public["branch_review_commit"], "task_head"),
            ("branch_review_commit", public["task_head"], "branch_review_commit"),
            ("branch_review_commit", unrelated, "branch_review_commit"),
            ("new_base_head", future_base, "new_base_head"),
            ("candidate_tree_sha256", "f" * 64, "candidate_tree_sha256"),
        )
        for field, value, expected_field in cases:
            with self.subTest(field=field, value=value):
                stale = dict(public)
                stale[field] = value
                result = self.record(
                    stale,
                    self.auth("continuity_passed"),
                    "continuity_passed",
                    ok=False,
                )
                self.assertEqual("stale_identity", result["code"])
                self.assertEqual(expected_field, result["field_path"])
                self.assertFalse(self.checkpoint().exists())

    def test_base_continuity_gate_rejects_head_advance_after_record(self):
        public = self.continuity_public()
        self.record(public, self.auth("continuity_passed"), "continuity_passed")
        metadata = self.repo / TASK_REF / "review.md"
        metadata.write_text("metadata tail\n")
        self.git("add", str(metadata.relative_to(self.repo)))
        self.git("commit", "-qm", "metadata tail")
        result = self.run_wrapper(
            "check-review-gate.sh", "--task", TASK_REF, ok=False
        )
        self.assertEqual("stale_identity", result["code"])
        self.assertEqual("integration_pair.task_head", result["field_path"])
        self.assertTrue(self.checkpoint().exists())


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

    def test_branch_review_recomputes_architecture_over_committed_full_diff(self):
        workflow = REPO / "trellis/workflows/guru-team/workflow.md"
        sources = {
            "skill": PACKAGE / "SKILL.md",
            "contract": PACKAGE / "references/contract.md",
            "workflow": workflow,
        }
        for label, path in sources.items():
            with self.subTest(source=label):
                text = " ".join(path.read_text(encoding="utf-8").split())
                self.assertIn("task_impact_sync(stage=branch_review)", text)
                self.assertRegex(text, r"complete committed (?:base-to-HEAD )?diff|committed full diff")
                self.assertIn("Phase 2", text)
                self.assertRegex(text, r"reuse|reused|never treats")
                self.assertNotIn("Afizzy", text)

        contract = sources["contract"].read_text(encoding="utf-8")
        for route in (
            "sync_required", "contract_incomplete", "architecture_conflict",
            "fitness_regression",
        ):
            self.assertIn(route, contract)
        self.assertIn("does not read Architecture private state", contract)

        workflow_text = workflow.read_text(encoding="utf-8")
        phase = workflow_text.split("#### 3.5 Branch review", 1)[1].split("#### 3.6 Publication review", 1)[0]
        self.assertLess(
            phase.index("task_impact_sync(stage=branch_review)"),
            phase.index("invokes guru-review-branch"),
        )

    def test_workflow_closes_delivery_completion_finish_and_promotion_architecture_routes(self):
        text = (REPO / "trellis/workflows/guru-team/workflow.md").read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for stage in (
            "stage=planning", "stage=implementation_discovery", "stage=phase2",
            "stage=branch_review", "stage=publication", "stage=acceptance_finish",
        ):
            self.assertIn(stage, normalized)
        for phrase in (
            "Delivery Review rejects missing or stale Architecture evidence",
            "reviewed_promoted",
            "current `no_change` proof",
            "promotion-created shared-current diff returns to fresh Phase 2",
            "does not absorb Delivery publication, whole-task Completion",
        ):
            self.assertIn(phrase, normalized)
        publication = text.split("#### 3.6 Delivery review and publication", 1)[1].split("#### 3.7 Completion, Closure and Finish", 1)[0]
        self.assertLess(
            publication.index("task_impact_sync(stage=publication)"),
            publication.index("enters `guru-review-task-delivery`"),
        )
        finish = text.split("#### 3.7 Completion, Closure and Finish", 1)[1].split("## Global Integration Boundaries", 1)[0]
        self.assertLess(
            finish.index("task_impact_sync(stage=acceptance_finish)"),
            finish.index("`guru-finish-task` alone archives"),
        )
        contract = (PACKAGE / "references/contract.md").read_text(encoding="utf-8")
        self.assertIn("`guru-review-task-delivery`", contract)
        self.assertIn("`legacy-archived-review-disposition-required` stop", contract)
        self.assertNotIn("consumer is Publication's", contract)
        spec = (
            REPO / "trellis/presets/guru-team/spec/workflow/workflow-contract.md"
        ).read_text(encoding="utf-8")
        for phrase in (
            "Every standard task mandatory invokes",
            "committed full-diff Branch Review",
            "returns `sync_required`",
            "requires `reviewed_promoted`",
        ):
            self.assertIn(phrase, spec)
        self.assertRegex(spec, r"routing-only\s+integration")

    def test_current_interface_wording_matches_profiles_gate_and_exits(self):
        interface = json.loads((PACKAGE / "interface.json").read_text())
        boundary = next(row for row in interface["entry_preconditions"] if row["id"] == "workspace_boundary")
        self.assertIn("TaskBranchBinding", boundary["evidence"])
        self.assertNotIn("mapping", json.dumps(boundary).lower())
        public = interface["public_contracts"]
        self.assertEqual(
            "guru-review-branch-input-legacy-index-1.0",
            public["input"]["aggregate_schema"]["schema_id"],
        )
        self.assertEqual(
            ["delivery_branch_review", "delivery_base_continuity", "delivery_archived_review", "delivery_scope_withdrawal", "delivery_scope_revision", "legacy_control_inspection", "legacy_control_retirement"],
            [profile["id"] for profile in public["input"]["profiles"]],
        )
        self.assertEqual(
            "https://github.com/castbox/guru-trellis/schemas/guru-review-gate-7.0.json",
            public["private_artifacts"][0]["schema"]["schema_id"],
        )
        self.assertEqual(
            [
                "passed",
                "continuity_passed",
                "implementation_required",
                "scope_confirmation_required",
                "blocked",
                "archived_review_passed",
                "delivery_stopped",
                "delivery_scope_revised",
                "legacy_controls_retired",
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
            normalized = " ".join(text.split())
            self.assertIn("continuity", text)
            self.assertIn("current", text)
            self.assertIn("Delivery", text)
            self.assertIn("continuity_passed", text)
            self.assertIn("bounded", normalized)
            self.assertIn("full Branch Review", normalized)
        for path in (
            REPO / ".trellis/spec/workflow/companion-scripts.md",
            REPO / "trellis/presets/guru-team/spec/workflow/companion-scripts.md",
        ):
            text = path.read_text()
            section = text.split("## Branch Review Recorder And Checker\n", 1)[1]
            section = section.split("\n## ", 1)[0]
            profiles, ordinary = section.split("### Ordinary Profiles\n", 1)
            ordinary, archived = ordinary.split("### Archived Review Profile\n", 1)
            profiles = " ".join(profiles.split())
            ordinary = " ".join(ordinary.split())
            archived = " ".join(archived.split())
            with self.subTest(path=path):
                self.assertIn(
                    "Aggregate public input schema 4.0 dispatches two ordinary profiles: "
                    "the full `branch_review` schema 2.0 profile and the bounded "
                    "`base_continuity` schema 2.0 profile. Both remain valid and unchanged.",
                    profiles,
                )
                self.assertIn(
                    "Aggregate public input schema 5.0 retains those two ordinary "
                    "profiles unchanged and adds the independent read-only "
                    "`archived_review` schema 1.0 profile.",
                    profiles,
                )
                for phrase in (
                    "rules apply only to `branch_review` and `base_continuity`; "
                    "their existing behavior is unchanged",
                    "records only current gate schema 7.0",
                    "Only schema 7.0 is accepted for these ordinary profiles",
                    "schema 6.0 or older fails closed as stale without projection, "
                    "dual-read, rewrite, or migration",
                    "Successful `passed`, `continuity_passed`, and zero-payload stop "
                    "`blocked` projection retires the checkpoint",
                    "active re-entry routes retain that one checkpoint",
                ):
                    self.assertIn(phrase, ordinary)
                for phrase in (
                    "For `archived_review`, the same recorder/checker/invocation commands "
                    "use the separate `guru-archived-review-gate-1.0` schema "
                    "(version `archived-1.0`), not ordinary gate schema 7.0",
                    "Its only exits are `archived_review_passed` and `blocked`; "
                    "both retire the checkpoint after validated projection",
                    "does not restore the task or mutate the archive, PR, or Issue",
                    "does not loosen ordinary gate schema 7.0 validation, blocked "
                    "semantics, or re-entry behavior",
                ):
                    self.assertIn(phrase, archived)
                self.assertNotIn("records only current gate schema 6.0", section)
                self.assertNotIn("Only schema 7.0 is accepted;", section)

    def test_subtraction_review_is_independent_and_not_phase2_checkpoint_reuse(self):
        repo = PACKAGE.parents[4]
        spec = repo / ".trellis/spec/workflow/subtraction-first-compatibility.md"
        text = spec.read_text(encoding="utf-8")
        for phrase in (
            "independently judge both dimensions",
            "`code-only`, `docs-only`, and `mixed`",
            "does not read Phase 2 evidence",
            "Approval is dialogue-local",
            "3000",
            "named direct consumers",
            "long-term maintainability",
        ):
            self.assertIn(phrase, text)
        package_text = " ".join(
            path.read_text(encoding="utf-8")
            for path in (PACKAGE / "SKILL.md", PACKAGE / "references/contract.md")
        )
        self.assertIn("subtraction-first-compatibility.md", package_text)
        gate = json.loads((PACKAGE / "schemas/review-gate-7.0.schema.json").read_text())
        self.assertNotIn("user_confirmation", json.dumps(gate))

    def test_wrappers_are_executable(self):
        for name in ("review-branch.sh", "check-review-gate.sh", "invoke.sh"):
            self.assertTrue(os.access(PACKAGE / "scripts" / name, os.X_OK))


if __name__ == "__main__":
    unittest.main()
