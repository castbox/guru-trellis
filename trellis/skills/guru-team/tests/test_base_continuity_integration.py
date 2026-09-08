from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SKILLS = Path(__file__).resolve().parents[1]
REPO = SKILLS.parents[2]
RECONCILE = SKILLS / "packages/guru-reconcile-task-base"
REVIEW = SKILLS / "packages/guru-review-branch"
PUBLICATION = SKILLS / "packages/guru-review-task-publication"
TASK_REF = ".trellis/tasks/09-08-base-continuity"


def load_publication_wrapper():
    runtime = PUBLICATION / "runtime"
    for path in (SKILLS, SKILLS.parent, runtime):
        if str(path) not in sys.path:
            sys.path.insert(0, str(path))
    spec = importlib.util.spec_from_file_location(
        "base_continuity_publication_invoke",
        runtime / "invoke.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


PUBLICATION_WRAPPER = load_publication_wrapper()


class PublicationOwner:
    class WorkflowError(RuntimeError):
        def __init__(self, message: str, *, payload=None, **_kwargs) -> None:
            super().__init__(message)
            self.payload = payload or {}

    def __init__(self, root: Path, result: dict, checkpoint: Path) -> None:
        self.root = root
        self.result = result
        self.checkpoint = checkpoint

    def repo_root(self, _path: Path) -> Path:
        return self.root

    @staticmethod
    def read_json(path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def resolve_task_dir(self, root: Path, task_ref: str) -> Path:
        return root / task_ref

    def cmd_check_task_publication_review(self, _args) -> dict:
        return {"owner_result": copy.deepcopy(self.result)}

    def task_publication_path(self, _root: Path, _task: Path) -> Path:
        return self.checkpoint


class BaseContinuityIntegrationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.parent = Path(self.temp.name)
        self.repo = self.parent / "repo"
        self.inputs = self.parent / "inputs"
        self.inputs.mkdir()
        subprocess.run(
            ["git", "init", "-q", "-b", "main", str(self.repo)], check=True
        )
        self.git("config", "user.name", "Base Continuity Integration")
        self.git("config", "user.email", "base-continuity@example.invalid")
        (self.repo / ".gitignore").write_text(".trellis/\n", encoding="utf-8")
        (self.repo / "base.txt").write_text("old base\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-qm", "old base")
        self.old_base = self.git("rev-parse", "HEAD")
        (self.repo / "base.txt").write_text("new base\n", encoding="utf-8")
        self.git("commit", "-qam", "new base")
        self.new_base = self.git("rev-parse", "HEAD")
        self.git("switch", "-qc", "feat/continuity", self.old_base)
        (self.repo / "task.txt").write_text("task content\n", encoding="utf-8")
        self.git("add", "task.txt")
        self.git("commit", "-qm", "reviewed task")
        self.review_head = self.git("rev-parse", "HEAD")
        self._write_task_identity()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def git(self, *args: str) -> str:
        return subprocess.run(
            ["git", *args],
            cwd=self.repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        ).stdout.strip()

    def write_json(self, name: str, value: dict) -> Path:
        path = self.inputs / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def run_wrapper(self, package: Path, script: str, *args: object) -> dict:
        process = subprocess.run(
            [str(package / "scripts" / script), *map(str, args), "--json"],
            cwd=REPO,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={"PATH": "/usr/bin:/bin:/usr/sbin:/sbin"},
        )
        payload = json.loads(process.stdout or process.stderr)
        self.assertEqual(0, process.returncode, payload)
        return payload

    def _write_task_identity(self) -> None:
        task = self.repo / TASK_REF
        task.mkdir(parents=True)
        task_id = Path(TASK_REF).name
        (task / "task.json").write_text(
            json.dumps(
                {
                    "id": task_id,
                    "status": "in_progress",
                    "branch": "feat/continuity",
                    "base_branch": "main",
                }
            ),
            encoding="utf-8",
        )
        tasks = self.repo / ".trellis/.runtime/guru-team/tasks"
        workspaces = self.repo / ".trellis/.runtime/guru-team/workspaces"
        tasks.mkdir(parents=True)
        workspaces.mkdir(parents=True)
        (tasks / f"{task_id}.json").write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "task_slug": task_id,
                    "workspace_slug": task_id,
                    "workspace_path": str(self.repo.resolve()),
                    "task_artifact_dir": TASK_REF,
                }
            ),
            encoding="utf-8",
        )
        (workspaces / f"{task_id}.json").write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "workspace_slug": task_id,
                    "workspace_path": str(self.repo.resolve()),
                    "branch_name": "feat/continuity",
                }
            ),
            encoding="utf-8",
        )

    def reconcile_input(self) -> dict:
        return {
            "profile": "finalizer_base_mismatch",
            "mode": "workflow",
            "task_ref": TASK_REF,
            "task_head": self.review_head,
            "selected_base_ref": self.new_base,
            "old_base_head": self.old_base,
            "new_base_head": self.new_base,
            "branch_review_commit": self.review_head,
            "resume_target": "finalization_resume",
        }

    def continuity_review(self) -> dict:
        return {
            "candidate_classifications": [
                {
                    "candidate_ref": "candidate:no-continuity-defect",
                    "decision": "rejected_not_reproduced",
                    "witness": {
                        "requirement_refs": ["issue:#376"],
                        "supported_entry_refs": ["entry:base-continuity"],
                        "existing_caller_refs": ["caller:guru-review-branch"],
                        "honest_action_sequence": [
                            "review the committed reconciliation delta and candidate tree"
                        ],
                        "defect_observation": "No defect is reproduced in the bounded continuity scope.",
                        "excluded_assumptions": [],
                    },
                    "consumer_use": "branch_review_route_checker",
                }
            ],
            "semantic_review": {
                "qualified_findings": [],
                "scope_proposals": [],
                "observations": [],
                "followup_candidates": [],
                "rejected_candidates": [],
                "ai_review_gate": {
                    "status": "continuity_passed",
                    "summary": "The committed reconciliation matches the reviewed candidate.",
                },
            },
            "verification_evidence": {
                "reviewer": "independent-continuity-review",
                "review_source": "independent-agent",
                "evidence": ["Reviewed exact base delta, merge commit and resulting tree."],
            },
        }

    def publication_ready(self, branch_review_commit: str) -> dict:
        value = json.loads(
            (PUBLICATION / "examples/pr-readiness.json").read_text(encoding="utf-8")
        )
        value["task_ref"] = TASK_REF
        value["branch_review_commit"] = branch_review_commit
        return value

    def invoke_publication(self, public: dict, owner_result: dict) -> dict:
        checkpoint = (
            self.repo
            / ".trellis/.runtime/guru-team/owner-checkpoints"
            / Path(TASK_REF).name
            / "pr-readiness.json"
        )
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        checkpoint.write_text(json.dumps(owner_result), encoding="utf-8")
        owner = PublicationOwner(self.repo, owner_result, checkpoint)
        with mock.patch.object(PUBLICATION_WRAPPER, "_owner", return_value=owner):
            return PUBLICATION_WRAPPER.run(
                PUBLICATION,
                {},
                [
                    "--root",
                    str(self.repo),
                    "--input",
                    str(self.write_json("publication-input.json", public)),
                    "--owner-result",
                    str(self.write_json("publication-owner.json", owner_result)),
                ],
            )

    def test_finalizer_mismatch_reconciles_reviews_and_publishes_current_head(self) -> None:
        candidate = self.run_wrapper(
            RECONCILE,
            "execute-base-candidate.sh",
            "--root",
            self.repo,
            "--request",
            self.write_json(
                "candidate.json",
                {
                    "task_head": self.review_head,
                    "new_base_head": self.new_base,
                    "validation_commands": [],
                },
            ),
        )
        request = {
            "task_ref": TASK_REF,
            "branch": "feat/continuity",
            "prior_task_head": self.review_head,
            "selected_base_ref": self.new_base,
            "old_base_head": self.old_base,
            "new_base_head": self.new_base,
            "branch_review_commit": self.review_head,
            "candidate_tree_sha256": candidate["candidate_tree_sha256"],
            "commit_message": "chore(base): reconcile reviewed task",
        }
        receipt = self.run_wrapper(
            RECONCILE,
            "execute-base-reconciliation.sh",
            "--root",
            self.repo,
            "--request",
            self.write_json("reconciliation-request.json", request),
        )
        reconciled_head = receipt["reconciled_task_head"]
        self.assertEqual(
            [self.review_head, self.new_base],
            self.git("show", "-s", "--format=%P", reconciled_head).split(),
        )

        gate = {
            "authority_impact": "unchanged",
            "task_content_impact": "unchanged",
            "integration_impact": "continuity_review_required",
            "reviewed_scope": ["authority", "task content", "integration candidate"],
            "key_delta_refs": ["base.txt"],
            "validation_evidence": ["candidate merge completed with the reviewed tree"],
            "unverified_boundaries": [],
            "summary": "Only the base integration clock advanced.",
            "typed_exit": "review_continuity_required",
            "route_payload": {
                "candidate_tree_sha256": candidate["candidate_tree_sha256"],
                "relevant_paths": ["base.txt"],
            },
        }
        recorded = self.run_wrapper(
            RECONCILE,
            "record-base-reconciliation.sh",
            "--root",
            self.repo,
            "--skill-input",
            self.write_json("reconcile-public.json", self.reconcile_input()),
            "--semantic-review-file",
            self.write_json("reconcile-gate.json", gate),
            "--typed-exit",
            "review_continuity_required",
            "--reconciliation-result",
            self.write_json("reconciliation-result.json", receipt),
        )
        continuity_seed = self.run_wrapper(
            RECONCILE,
            "invoke.sh",
            "--root",
            self.repo,
            "--invocation",
            self.write_json(
                "reconcile-envelope.json",
                {"public_input": self.reconcile_input(), "owner_result": recorded},
            ),
        )
        self.assertEqual(reconciled_head, continuity_seed["task_head"])
        self.assertEqual(self.review_head, continuity_seed["branch_review_commit"])

        review_input = {
            **continuity_seed,
            "profile": "base_continuity",
            "mode": "workflow",
            "review_intent": "base_continuity",
        }
        review_input.pop("exit_id")
        self.run_wrapper(
            REVIEW,
            "review-branch.sh",
            "--root",
            self.repo,
            "--task",
            TASK_REF,
            "--skill-input",
            self.write_json("continuity-input.json", review_input),
            "--semantic-review-file",
            self.write_json("continuity-review.json", self.continuity_review()),
            "--typed-exit",
            "continuity_passed",
        )
        continuity = self.run_wrapper(
            REVIEW,
            "invoke.sh",
            "--root",
            self.repo,
            "--task",
            TASK_REF,
            "--input",
            self.write_json("continuity-input.json", review_input),
        )
        self.assertEqual(reconciled_head, continuity["branch_review_commit"])

        publication_input = {
            "profile": "publication_review",
            "mode": "workflow",
            "task_ref": TASK_REF,
            "branch_review_commit": continuity["branch_review_commit"],
            "review_intent": "initial_review",
        }
        ready = self.invoke_publication(
            publication_input,
            self.publication_ready(reconciled_head),
        )
        self.assertEqual("ready", ready["exit_id"])
        self.assertEqual(reconciled_head, ready["branch_review_commit"])

    def test_unreviewed_base_merge_cannot_reuse_prior_review_for_publication(self) -> None:
        self.git("merge", "--no-ff", "-m", "unreviewed base merge", self.new_base)
        unreviewed_head = self.git("rev-parse", "HEAD")
        public = {
            "profile": "publication_review",
            "mode": "workflow",
            "task_ref": TASK_REF,
            "branch_review_commit": self.review_head,
            "review_intent": "initial_review",
        }
        from runtime.io import CommandError

        with self.assertRaises(CommandError) as raised:
            self.invoke_publication(public, self.publication_ready(unreviewed_head))
        self.assertEqual("publication_input_invalid", raised.exception.code)
        self.assertEqual("input.branch_review_commit", raised.exception.field_path)


if __name__ == "__main__":
    unittest.main()
