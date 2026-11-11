from __future__ import annotations

import json
import importlib.util
import os
import subprocess
import tempfile
import unittest
import sys
from pathlib import Path


SKILLS = Path(__file__).resolve().parents[1]
REPO = SKILLS.parents[2]
sys.path.insert(0, str(SKILLS))
from runtime.io import project_intermediate_receipt
PACKAGES = (
    "guru-review-branch",
    "guru-verify-extension-installation",
)
TASK_REF = ".trellis/tasks/flow-task"


class ReviewedContentIdentityIntegrationTest(unittest.TestCase):
    def setUp(self) -> None:
        spec=importlib.util.spec_from_file_location("identity_delivery_flow",SKILLS/"packages/guru-check-task/tests/test_delivery_flow.py")
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        self.flow=module.DeliveryFlow();self.flow.setUp();self.addCleanup(self.flow.doCleanups)
        self.fixture=self.flow.repo;self.inputs=self.flow.inputs
        self.base=self.flow.projection.content_base(self.flow.key)
        self.review_head=self.flow.head

    def git(self, *args: str) -> str:
        return subprocess.run(
            ["git", *args],
            cwd=self.fixture,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        ).stdout.strip()

    def write_json(self, name: str, value: dict) -> Path:
        path = self.inputs / name
        path.write_text(json.dumps(value))
        return path

    def run_identity(self, package: str, *, include_worktree: bool = False) -> dict:
        command = [
            str(
                SKILLS
                / "packages"
                / package
                / "scripts/reviewed-content-identity.sh"
            ),
            "--root",
            str(self.fixture),
            "--commit",
            "HEAD",
            "--json",
        ]
        if include_worktree:
            command.append("--include-worktree")
        process = subprocess.run(
            command,
            cwd=REPO,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        payload = json.loads(process.stdout or process.stderr)
        self.assertEqual(0, process.returncode, (package, payload))
        return project_intermediate_receipt(payload, SKILLS / "schemas")

    def all_identities(self, *, include_worktree: bool = False) -> dict[str, dict]:
        return {
            package: self.run_identity(package, include_worktree=include_worktree)
            for package in PACKAGES
        }

    def assert_one_identity(self, outputs: dict[str, dict]) -> str:
        self.assertEqual(set(PACKAGES), set(outputs))
        algorithms = {value["algorithm"] for value in outputs.values()}
        digests = {value["sha256"] for value in outputs.values()}
        commits = {value["commit"] for value in outputs.values()}
        self.assertEqual({"guru-reviewed-content-1.0"}, algorithms)
        self.assertEqual(1, len(digests), outputs)
        self.assertEqual({self.git("rev-parse", "HEAD")}, commits)
        return next(iter(digests))

    def run_branch_wrapper(self, name: str, *args: object, ok: bool = True) -> dict:
        if name == "check-review-gate.sh":
            args = (*args, "--delivery-key", json.dumps(self.flow.key))
        process = subprocess.run(
            [
                str(SKILLS / "packages/guru-review-branch/scripts" / name),
                "--root",
                str(self.fixture),
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
        return project_intermediate_receipt(payload, SKILLS / "schemas") if ok and name != "invoke.sh" else payload

    def public_input(self) -> dict:
        return {"profile":"delivery_branch_review","mode":"workflow","task_ref":TASK_REF,
                "delivery_key":self.flow.key,"base_ref":self.base,
                "branch_review_commit":self.git("rev-parse","HEAD"),"review_intent":"initial_review"}

    def semantic_review(self) -> dict:
        return json.loads((SKILLS/"packages/guru-review-branch/examples/authoring-delivery-passed-2.0.json").read_text())

    def record_fresh_gate(self) -> Path:
        public = self.write_json("public.json", self.public_input())
        semantic = self.write_json("semantic.json", self.semantic_review())
        result = self.run_branch_wrapper(
            "review-branch.sh",
            "--task",
            TASK_REF,
            "--skill-input",
            public,
            "--semantic-review-file",
            semantic,
            "--typed-exit",
            "passed",
        )
        self.assertIn(result["status"], {"recorded", "duplicate"})
        return (
            self.fixture
            / ".trellis/.runtime/guru-team/owner-checkpoints"
            / Path(TASK_REF).name
            / self.flow.key["delivery_id"]
            / "review-gate.json"
        )

    def test_current_wrappers_share_one_identity_across_real_git_drift(self) -> None:
        reviewed = self.assert_one_identity(self.all_identities())

        metadata = {
            ".trellis/tasks/archive/fixture/task.json": "{}\n",
            ".trellis/workspace/test/journal.md": "metadata\n",
            ".trellis/.runtime/guru-team/checkpoint.json": "{}\n",
            ".trellis/guru-team/extension.json": "{}\n",
            "nested/.DS_Store": "noise\n",
        }
        for relative, content in metadata.items():
            target = self.fixture / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
        overlay_identity = self.assert_one_identity(
            self.all_identities(include_worktree=True)
        )
        self.assertEqual(reviewed, overlay_identity)

        self.git("add", "-f", *metadata)
        self.git("commit", "-qm", "metadata only")
        metadata_commit_identity = self.assert_one_identity(self.all_identities())
        self.assertEqual(reviewed, metadata_commit_identity)

        self.git("mv", "app.txt", "renamed.txt")
        self.git("commit", "-qm", "path drift")
        path_identity = self.assert_one_identity(self.all_identities())
        self.assertNotEqual(reviewed, path_identity)

        os.chmod(self.fixture / "renamed.txt", 0o755)
        self.git("add", "renamed.txt")
        self.git("commit", "-qm", "mode drift")
        mode_identity = self.assert_one_identity(self.all_identities())
        self.assertNotEqual(path_identity, mode_identity)

        (self.fixture / "renamed.txt").write_text("changed blob\n")
        self.git("add", "renamed.txt")
        self.git("commit", "-qm", "oid drift")
        oid_identity = self.assert_one_identity(self.all_identities())
        self.assertNotEqual(mode_identity, oid_identity)

    def test_branch_review_rejects_old_gate_and_keeps_freshness_independent(self) -> None:
        checkpoint = (
            self.fixture
            / ".trellis/.runtime/guru-team/owner-checkpoints"
            / Path(TASK_REF).name
            / self.flow.key["delivery_id"]
            / "review-gate.json"
        )
        checkpoint.parent.mkdir(parents=True)
        checkpoint.write_text(
            json.dumps({"schema_version": "5.0", "task_dir": TASK_REF})
        )
        old = self.run_branch_wrapper(
            "check-review-gate.sh", "--task", TASK_REF, ok=False
        )
        self.assertEqual("stale_identity", old["code"])
        self.assertIsNone(self.flow.projection.resolve(self.flow.key)["results"]["full_review"])

        checkpoint = self.record_fresh_gate()
        fresh = self.run_branch_wrapper(
            "check-review-gate.sh", "--task", TASK_REF, "--expected-exit", "passed"
        )
        self.assertEqual("owner_checkpoint_validated", fresh["status"])
        self.assertFalse(fresh["formal_exit"])
        current_gate = json.loads(checkpoint.read_text())
        self.assertEqual(
            "guru-reviewed-content-1.0",
            current_gate["reviewed_content_algorithm"],
        )

        wrong_range = self.public_input()
        wrong_range["branch_review_commit"] = self.base
        wrong = self.run_branch_wrapper(
            "invoke.sh",
            "--task",
            TASK_REF,
            "--input",
            self.write_json("wrong-range.json", wrong_range),
            ok=False,
        )
        self.assertEqual("stale_identity", wrong["code"])
        self.assertTrue(checkpoint.is_file())

        base_tree = self.git("rev-parse", f"{self.base}^{{tree}}")
        advanced_base = self.git(
            "commit-tree", base_tree, "-p", self.base, "-m", "advance base"
        )
        self.git("update-ref", "refs/remotes/origin/main", advanced_base)
        # The reviewed base is a fixed OID; an unrelated remote-ref advance
        # cannot replace that content range or stale its unchanged checkpoint.
        fixed_base = self.run_branch_wrapper(
            "check-review-gate.sh", "--task", TASK_REF
        )
        self.assertEqual("owner_checkpoint_validated", fixed_base["status"])

        self.git("update-ref", "refs/remotes/origin/main", self.base)
        tree = self.git("rev-parse", "HEAD^{tree}")
        unrelated = self.git("commit-tree", tree, "-m", "unrelated head")
        self.git("reset", "--hard", unrelated)
        ancestry_stale = self.run_branch_wrapper(
            "check-review-gate.sh", "--task", TASK_REF, ok=False
        )
        self.assertEqual("stale_identity", ancestry_stale["code"])


if __name__ == "__main__":
    unittest.main()
