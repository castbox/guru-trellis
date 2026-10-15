"""Actual Git and public Delivery transitions for fixed content candidates."""
import json
import subprocess
import unittest
import uuid

import test_installed_projection as fixtures
from runtime.delivery_projection.gates import record_gate, rework


class FixedCandidateTests(unittest.TestCase):
    setUp = fixtures.InstalledProjectionTests.setUp
    create = fixtures.InstalledProjectionTests.create
    planning = fixtures.InstalledProjectionTests.planning

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, capture_output=True,
                              text=True, check=True).stdout.strip()

    def seed(self):
        self.git("config", "user.name", "Fixed Candidate Test")
        self.git("config", "user.email", "candidate@example.invalid")
        (self.root / ".gitignore").write_text(".trellis/.runtime/\n")
        (self.root / "app.txt").write_text("base\n")
        self.git("add", ".")
        self.git("commit", "-qm", "initial content")
        self.base = self.git("rev-parse", "HEAD")
        self.git("branch", "main")
        self.git("update-ref", "refs/remotes/origin/main", self.base)

    def change(self, name, value):
        (self.root / name).write_text(value)
        self.git("add", name)
        self.git("commit", "-qm", "actual content change")
        return self.git("rev-parse", "HEAD")

    def test_shared_fetch_preserves_fixed_candidate_and_result_range(self):
        self.seed()
        key = self.create()
        self.planning(key)
        head = self.change("app.txt", "Task A\n")
        base = self.projection.content_base(key, observed_target="origin/main")
        candidate = self.projection.candidate(["app.txt"], head_ref=head, base_ref=base)
        self.projection.begin_check(key, candidate)
        peer = self.root / "peer"
        self.git("worktree", "add", "-qb", "task-b", str(peer), self.base)
        try:
            (peer / "other.txt").write_text("independent B\n")
            subprocess.run(["git", "-C", str(peer), "add", "other.txt"], check=True, capture_output=True)
            subprocess.run(["git", "-C", str(peer), "commit", "-qm", "Task B"], check=True, capture_output=True)
            self.git("fetch", ".", "refs/heads/task-b:refs/remotes/origin/main")
            self.assertNotEqual(self.git("rev-parse", "origin/main"), base)
            self.assertEqual(self.projection.content_base(key, observed_target="origin/main"), base)
            self.projection.api.delivery_store.verify_candidate(self.root, candidate)
            self.assertEqual(self.projection.resolve(key)["candidate"], candidate)
            self.assertEqual(self.git("rev-parse", "HEAD"), head)
        finally:
            self.git("worktree", "remove", "--force", str(peer))

    def test_actual_head_evolution_retains_history_without_applicable_old_gates(self):
        self.seed()
        key = self.create()
        self.planning(key)
        head = self.change("app.txt", "first implementation\n")
        first = self.projection.candidate(["app.txt"], head_ref=head, base_ref=self.base)
        self.projection.begin_check(key, first)
        record_gate(self.projection, key, "check", "checked-first", "passed", [self.scope], [])
        record_gate(self.projection, key, "full_review", "reviewed-first", "passed", [self.scope], [])
        evolved = self.change("integration.txt", "actual integration delta\n")
        rework(self.projection, key, "full_review", "implementation", self.scope, ["readiness"])
        second = self.projection.candidate(["integration.txt"], head_ref=evolved,
                                           base_ref=self.projection.content_base(key))
        self.assertEqual(set(second["paths"]), {"app.txt", "integration.txt"})
        self.projection.begin_check(key, second)
        self.assertEqual(self.projection.resolve(key)["results"]["full_review"]["result_id"], "reviewed-first")
        self.assertEqual(self.projection.gate_applicability(key)["check"]["kind"], "not_applicable")
        self.assertEqual(self.projection.gate_applicability(key)["full_review"]["kind"], "not_applicable")
        record_gate(self.projection, key, "check", "checked-integrated", "passed", [self.scope], [])
        self.assertEqual(self.projection.resolve(key)["results"]["full_review"]["result_id"], "reviewed-first")
        record_gate(self.projection, key, "full_review", "reviewed-integrated", "passed", [self.scope], [])
        result = self.projection.resolve(key)["results"]["full_review"]
        self.assertEqual(result["candidate"], second)
        self.assertEqual(result["predecessor_result_id"], "checked-integrated")
        self.assertEqual(self.projection.gate_applicability(key)["full_review"]["kind"], "applicable")

    def test_d2_uses_actual_delivered_head_and_recovers_its_own_base(self):
        self.seed()
        workflow = self.root / ".trellis/workflow.md"
        declaration = self.projection.declaration()
        declaration["profiles"].append("local_commit")
        workflow.write_text("[trellis-runtime-contract]\n" + json.dumps(declaration) + "\n[/trellis-runtime-contract]\n")

        def create_local():
            key = {"task_id": "projection-task", "lifecycle_generation": 0, "delivery_id": str(uuid.uuid4())}
            self.projection.apply({"api_version": "1.0", "operation": "create_delivery", "key": key,
                "owner_role": "creation", "owner_id": fixtures.OWNERS["creation"], "profile": "local_commit",
                "scope_ref": {"authority": self.scope, "anchors": ["验收"]}})
            return key

        first = create_local()
        self.planning(first)
        delivered_head = self.change("app.txt", "D1\n")
        candidate = self.projection.candidate(["app.txt"], head_ref=delivered_head, base_ref=self.base)
        self.projection.begin_check(first, candidate)
        for role, outcome in (("check", "passed"), ("full_review", "passed"), ("readiness", "ready")):
            record_gate(self.projection, first, role, "d1-" + role, outcome, [self.scope], [])
        fact = {"result_id": "actual-d1", "owner_id": fixtures.OWNERS["delivery"], "evidence": [self.scope],
                "profile": "local_commit", "candidate": candidate, "commit": delivered_head}
        self.projection.apply({"api_version": "1.0", "operation": "record_delivery", "key": first,
            "owner_role": "delivery", "owner_id": fixtures.OWNERS["delivery"], "expected_phase": "publishing", "result": fact})
        second = create_local()
        self.planning(second)
        head = self.change("next.txt", "D2\n")
        self.assertEqual(self.projection.content_base(second, development_base=self.base), delivered_head)
        candidate = self.projection.candidate(["next.txt"], head_ref=head,
                                             base_ref=self.projection.content_base(second))
        self.assertEqual(candidate["paths"], ["next.txt"])
        self.projection.begin_check(second, candidate)
        self.git("update-ref", "refs/remotes/origin/main", head)
        self.assertEqual(self.projection.content_base(second, observed_target="origin/main"), delivered_head)
        self.assertEqual(self.projection.resolve(second)["candidate"], candidate)


if __name__ == "__main__":
    unittest.main()
