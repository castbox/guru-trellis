from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILLS = Path(__file__).resolve().parents[1]
REPO = SKILLS.parents[2]
FINALIZER = SKILLS / "packages/guru-finalize-task"
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
        self.git("remote", "add", "origin", "https://github.com/castbox/guru-trellis.git")
        (self.repo / ".gitignore").write_text(
            ".trellis/.runtime/\n", encoding="utf-8"
        )
        target_package = self.repo / PUBLICATION.relative_to(REPO)
        target_package.parent.mkdir(parents=True)
        shutil.copytree(PUBLICATION, target_package)
        target_schemas = self.repo / "trellis/workflows/guru-team/schemas"
        target_schemas.parent.mkdir(parents=True)
        shutil.copytree(REPO / "trellis/workflows/guru-team/schemas", target_schemas)
        config = self.repo / ".trellis/guru-team/config.yml"
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text(
            "github_repo: castbox/guru-trellis\nworkspace_mode: worktree\n",
            encoding="utf-8",
        )
        (self.repo / "base.txt").write_text("old base\n", encoding="utf-8")
        self.git("add", ".")
        self.git("commit", "-qm", "old base")
        self.old_base = self.git("rev-parse", "HEAD")
        (self.repo / "base.txt").write_text("new base\n", encoding="utf-8")
        self.git("commit", "-qam", "new base")
        self.new_base = self.git("rev-parse", "HEAD")
        self.git("switch", "-qc", "feat/continuity", self.old_base)
        (self.repo / "task.txt").write_text("task content\n", encoding="utf-8")
        self._write_task_identity()
        self.git("add", "task.txt", TASK_REF)
        self.git("commit", "-qm", "reviewed task")
        self.review_head = self.git("rev-parse", "HEAD")

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
        for name in ("prd.md", "design.md", "implement.md"):
            (task / name).write_text(f"# {name}\n\nCurrent #376 authority.\n", encoding="utf-8")
        issue = {
            "number": 376,
            "url": "https://github.com/castbox/guru-trellis/issues/376",
            "title": "降低基线分支已更新对并行进行中的任务的干扰",
            "reason": "The continuity path is fully covered by this regression.",
        }
        (task / "issue-scope-ledger.json").write_text(
            json.dumps(
                {
                    "schema_version": "2.0",
                    "primary_issue": issue,
                    "close_issues": [issue],
                    "related_issues": [],
                    "followup_issues": [],
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

    def finalizer_reconciliation_input(self) -> dict:
        interface = json.loads(
            (FINALIZER / "interface.json").read_text(encoding="utf-8")
        )
        output = json.loads(
            (FINALIZER / "examples/public-base-reconciliation-required-output.json")
            .read_text(encoding="utf-8")
        )
        output.update(
            {
                "task_ref": TASK_REF,
                "task_head": self.review_head,
                "publication_head": self.review_head,
                "selected_base_ref": self.new_base,
                "old_base_head": self.old_base,
                "new_base_head": self.new_base,
                "branch_review_commit": self.review_head,
            }
        )
        self.assertEqual("base_reconciliation_required", output["exit_id"])
        projection = next(
            item
            for item in interface["public_contracts"]["projections"]
            if item["id"] == "project_base_reconciliation_required"
        )
        consumer = next(
            item
            for item in interface["public_contracts"]["consumer_inputs"]
            if item["id"] == projection["consumer_input_id"]
        )
        mappings = projection["mappings"]
        self.assertEqual(
            set(consumer["contract"]["seed_fields"]),
            {mapping["source"] for mapping in mappings},
        )
        projected = {
            mapping["target"]: output[mapping["source"]]
            for mapping in mappings
        }
        projected.update(
            {
                "profile": consumer["contract"]["profile_id"],
                "mode": "workflow",
            }
        )
        return projected

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

    def publication_review(self) -> dict:
        value = json.loads(
            (PUBLICATION / "examples/pr-readiness.json").read_text(encoding="utf-8")
        )
        for key in (
            "schema_version",
            "skill_id",
            "task_ref",
            "branch_review_commit",
            "reviewed_content_sha256",
        ):
            value.pop(key)
        value.update(
            {
                "profile": "publication_review",
                "mode": "workflow",
                "review_intent": "initial_review",
            }
        )
        value["pr_payload"]["title"] = "修复：#376 保持跨 Skill 审查连续性"
        value["pr_payload"]["body"] = value["pr_payload"]["body"].replace(
            "#179", "#376"
        )
        value["pr_payload"]["body"] = value["pr_payload"]["body"].replace(
            "- durable specs 与 public README 已同步。",
            "- strategy: update_existing\n- durable docs: workflow contracts synchronized\n- merged delta: continuity contract fixes\n- task history: task planning updated\n- follow-up: none",
        )
        return value

    def invoke_publication(self, public: dict, semantic_result: dict) -> dict:
        return PUBLICATION_WRAPPER.run(
            PUBLICATION,
            {},
            [
                "--root",
                str(self.repo),
                "--input",
                str(self.write_json("publication-input.json", public)),
                "--semantic-result",
                str(self.write_json("publication-semantic.json", semantic_result)),
            ],
        )

    def test_finalizer_mismatch_reconciles_reviews_and_publishes_current_head(self) -> None:
        reconcile_input = self.finalizer_reconciliation_input()
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
            self.write_json("reconcile-public.json", reconcile_input),
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
                {"public_input": reconcile_input, "owner_result": recorded},
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
            self.publication_review(),
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
            self.invoke_publication(public, self.publication_review())
        self.assertEqual("branch_review_handoff_contract_failed", raised.exception.code)
        self.assertEqual("input.branch_review_commit", raised.exception.field_path)


if __name__ == "__main__":
    unittest.main()
