"""Public constructor transport with real Git and installed Delivery operations.

The existing fixture establishes prior Planning. It is not native authoring
evidence. Every tested candidate is produced by the public constructor itself.
"""
from __future__ import annotations

import json
import os
import subprocess
import unittest
import uuid
from pathlib import Path

import test_fixed_candidate as fixed
import test_installed_projection as fixtures
from runtime.task_lifecycle import BranchBindingStore, TaskLifecycleKey, inspect_repository
from runtime.delivery_projection.gates import record_gate
from runtime.delivery_projection.adapter import authority_ref


SOURCE = Path(__file__).resolve().parents[6]
WRAPPER = SOURCE / "trellis/workflows/guru-team/scripts/bash/construct-delivery-candidate.sh"


class CandidateCliTests(unittest.TestCase):
    git = fixed.FixedCandidateTests.git
    seed = fixed.FixedCandidateTests.seed
    change = fixed.FixedCandidateTests.change
    create = fixtures.InstalledProjectionTests.create
    planning = fixtures.InstalledProjectionTests.planning

    def setUp(self):
        fixtures.InstalledProjectionTests.setUp(self)
        self.seed()
        BranchBindingStore(inspect_repository(self.root)).establish(
            TaskLifecycleKey("projection-task", 0), "task")
        self.key = self.create()
        self.planning(self.key)
        self.head = self.change("app.txt", "first implementation\n")
        self.inputs = self.root / ".trellis/.runtime/candidate-inputs"
        self.inputs.mkdir(parents=True)

    def construct(self, *, key=None, paths=("app.txt",), head="HEAD", hint=None, carrier="inline"):
        selected = self.key if key is None else key
        value = json.dumps(selected)
        stdin = None
        if carrier == "file":
            file = self.inputs / "key.json"
            file.write_text(value)
            value = str(file)
        elif carrier == "stdin":
            stdin, value = value, "-"
        argv = ["bash", str(WRAPPER), "--root", str(self.root), "--task", self.task_ref,
                "--delivery-key", value, "--head", head]
        argv.extend(hint if hint is not None else ["--development-base", self.base])
        argv.extend(["--paths", *paths])
        result = subprocess.run(argv, input=stdin, cwd=SOURCE, text=True, capture_output=True,
                                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        self.assertTrue((result.stdout or result.stderr).lstrip().startswith("{"),
                        (result.returncode, result.stdout, result.stderr))
        return result, json.loads(result.stdout or result.stderr)

    def operation(self, name, *, owner_role=None, expected_phase=None, **payload):
        phase = expected_phase or self.projection.resolve(self.key)["phase"]
        role = owner_role or ("implementation" if name == "begin_check" else "check")
        operation = {"api_version": "1.0", "operation": name, "key": self.key,
                     "owner_role": role, "owner_id": fixtures.OWNERS[role],
                     "expected_phase": phase, **payload}
        return self.public_operation(operation)

    def public_operation(self, operation):
        path = self.inputs / "operation.json"
        path.write_text(json.dumps(operation))
        return subprocess.run([os.sys.executable, str(self.root / ".trellis/scripts/delivery.py"),
                               operation["operation"].replace("_", "-"), "--task", self.task_ref,
                               "--input", str(path)], cwd=self.root, capture_output=True, text=True,
                              env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})

    def test_raw_complete_candidate_is_read_only_and_consumed_by_original_begin_check(self):
        (self.root / "dirty.txt").write_text("actual dirty increment\n")
        before = (self.task / "task.json").read_bytes()
        result, candidate = self.construct(paths=("dirty.txt",))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(set(candidate), {"kind", "content_ref", "paths", "head_ref", "base_ref"})
        self.assertEqual((candidate["kind"], candidate["head_ref"], candidate["base_ref"]),
                         ("git", self.head, self.base))
        self.assertEqual(set(candidate["paths"]), {"app.txt", "dirty.txt"})
        self.assertEqual((self.task / "task.json").read_bytes(), before)
        self.assertEqual(self.projection.resolve(self.key)["phase"], "implementing")
        invoked = self.operation("begin_check", candidate=candidate)
        self.assertEqual(invoked.returncode, 0, invoked.stderr)
        self.assertEqual(self.projection.resolve(self.key)["candidate"], candidate)
        self.assertEqual(self.projection.resolve(self.key)["phase"], "checking")

    def test_output_loss_repeats_same_read_and_supported_key_carriers(self):
        before = (self.task / "task.json").read_bytes()
        outputs = []
        for carrier in ("inline", "file", "stdin"):
            result, candidate = self.construct(carrier=carrier)
            self.assertEqual(result.returncode, 0, result.stderr)
            outputs.append(candidate)
        self.assertEqual(outputs[0], outputs[1])
        self.assertEqual(outputs[0], outputs[2])
        self.assertEqual((self.task / "task.json").read_bytes(), before)

    def test_normal_edit_rework_keeps_base_and_rejects_original_stale_candidate(self):
        result, first = self.construct()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.operation("begin_check", candidate=first).returncode, 0)
        reworked = self.operation("rework", target_role="implementation", reason=self.scope,
                                 affected_results=["check", "full_review", "readiness"])
        self.assertEqual(reworked.returncode, 0, reworked.stderr)
        changed = self.change("app.txt", "real second implementation\n")
        self.git("update-ref", "refs/remotes/origin/main", changed)
        result, second = self.construct(hint=["--development-base", changed])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(second["base_ref"], self.base)
        self.assertEqual(second["head_ref"], changed)
        self.assertNotEqual(second["content_ref"], first["content_ref"])
        stale = self.operation("begin_check", candidate=first)
        self.assertNotEqual(stale.returncode, 0)
        self.assertEqual(self.projection.resolve(self.key)["phase"], "implementing")
        accepted = self.operation("begin_check", candidate=second)
        self.assertEqual(accepted.returncode, 0, accepted.stderr)
        self.assertEqual(self.projection.resolve(self.key)["candidate"], second)

    def test_missing_binding_stale_head_and_input_errors_preserve_specific_diagnostics(self):
        result, error = self.construct(head=self.base)
        self.assertEqual((result.returncode, error["code"], error["field_path"]),
                         (3, "candidate_head_mismatch", "head"))
        result, error = self.construct(key={})
        self.assertEqual(result.returncode, 3)
        self.assertEqual(error["code"], "invalid_record")
        self.assertNotIn("Traceback", result.stderr)
        with unittest.mock.patch.dict(os.environ, {"TRELLIS_CONTEXT_ID": "another-session"}):
            result, error = self.construct()
        self.assertEqual((result.returncode, error["code"], error["field_path"]),
                         (3, "no_current_task", "session.task"))

    def test_observed_target_and_existing_upstream_git_free_entry_keep_their_boundaries(self):
        result, candidate = self.construct(hint=["--observed-target", self.base])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(candidate["base_ref"], self.base)
        old = subprocess.run([os.sys.executable, str(self.root / ".trellis/scripts/delivery.py"),
                              "candidate", "--kind", "git_free", "--paths", "app.txt"],
                             cwd=self.root, capture_output=True, text=True,
                             env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        self.assertEqual(old.returncode, 0, old.stderr)
        self.assertEqual(set(json.loads(old.stdout)), {"content_ref"})

    def test_public_scope_revision_preserves_key_and_returns_to_original_planning(self):
        (self.task / "prd.md").write_text("整体scope修订：当前切片验收\n")
        authority = authority_ref(self.task / "prd.md", self.root)
        accepted = self.public_operation({"api_version": "1.0", "operation": "accept_scope",
            "key": {name: self.key[name] for name in ("task_id", "lifecycle_generation")},
            "owner_role": "task_scope", "owner_id": fixtures.OWNERS["task_scope"],
            "authority": authority})
        self.assertEqual(accepted.returncode, 0, accepted.stderr)
        scope = {"authority": authority, "anchors": ["当前切片验收"]}
        revised = self.operation("rework", owner_role="implementation", target_role="planning",
            reason=authority, scope_ref=scope,
            affected_results=["planning", "check", "full_review", "readiness"])
        self.assertEqual(revised.returncode, 0, revised.stderr)
        delivery = self.projection.resolve(self.key)
        self.assertEqual(delivery["phase"], "planning")
        self.assertEqual(delivery["scope_ref"], scope)
        self.assertTrue(all(value is None for value in delivery["results"].values()))
        self.assertEqual(self.projection.current()["key"], self.key)
        before = (self.task / "task.json").read_bytes()
        self.assertEqual(self.projection.resolve(self.key), delivery)
        self.assertEqual((self.task / "task.json").read_bytes(), before)
        self.assertEqual((self.root / "app.txt").read_text(), "first implementation\n")

    def test_public_stop_releases_selection_and_retries_exact_result_after_output_loss(self):
        result = {"result_id": "actual-withdrawal", "owner_id": fixtures.OWNERS["implementation"],
                  "reason": self.scope, "scope_decision": self.scope, "evidence": [self.scope]}
        operation = {"api_version": "1.0", "operation": "stop", "key": self.key,
                     "owner_role": "implementation", "owner_id": fixtures.OWNERS["implementation"],
                     "expected_phase": "implementing", "result": result}
        stopped = self.public_operation(operation)
        self.assertEqual(stopped.returncode, 0, stopped.stderr)
        self.assertEqual(self.projection.resolve(self.key)["phase"], "stopped")
        self.assertEqual(self.projection.resolve(self.key)["stop_result"], result)
        self.assertEqual(self.projection.current()["kind"], "no_current_delivery")
        before = (self.task / "task.json").read_bytes()
        recovered = self.public_operation(operation)
        self.assertEqual(recovered.returncode, 0, recovered.stderr)
        self.assertFalse(json.loads(recovered.stdout)["changed"])
        self.assertEqual((self.task / "task.json").read_bytes(), before)
        self.assertEqual(self.projection.current()["kind"], "no_current_delivery")

    def test_actual_prior_delivered_head_is_used_for_next_pull_request_slice(self):
        self.projection.apply({"api_version": "1.0", "operation": "stop", "key": self.key,
            "owner_role": "implementation", "owner_id": fixtures.OWNERS["implementation"],
            "expected_phase": "implementing", "result": {"result_id": "stop-first",
                "owner_id": fixtures.OWNERS["implementation"], "reason": self.scope,
                "scope_decision": self.scope, "evidence": [self.scope]}})
        declaration = self.projection.declaration()
        declaration["profiles"].append("local_commit")
        (self.root / ".trellis/workflow.md").write_text(
            "[trellis-runtime-contract]\n" + json.dumps(declaration) + "\n[/trellis-runtime-contract]\n")
        prior = {**self.key, "delivery_id": str(uuid.uuid4())}
        self.projection.apply({"api_version": "1.0", "operation": "create_delivery", "key": prior,
            "owner_role": "creation", "owner_id": fixtures.OWNERS["creation"], "profile": "local_commit",
            "scope_ref": {"authority": self.scope, "anchors": ["验收"]}})
        self.planning(prior)
        delivered = self.change("app.txt", "prior actual delivered content\n")
        candidate = self.projection.candidate(["app.txt"], head_ref=delivered, base_ref=self.base)
        self.projection.begin_check(prior, candidate)
        for role, outcome in (("check", "passed"), ("full_review", "passed"), ("readiness", "ready")):
            record_gate(self.projection, prior, role, "prior-" + role, outcome, [self.scope], [])
        self.projection.apply({"api_version": "1.0", "operation": "record_delivery", "key": prior,
            "owner_role": "delivery", "owner_id": fixtures.OWNERS["delivery"], "expected_phase": "publishing",
            "result": {"result_id": "actual-prior", "owner_id": fixtures.OWNERS["delivery"],
                       "evidence": [self.scope], "profile": "local_commit", "candidate": candidate, "commit": delivered}})
        self.key = self.create()
        self.planning(self.key)
        head = self.change("next.txt", "new independent slice\n")
        result, candidate = self.construct(paths=("next.txt",))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((candidate["base_ref"], candidate["head_ref"], candidate["paths"]),
                         (delivered, head, ["next.txt"]))


if __name__ == "__main__":
    unittest.main()
