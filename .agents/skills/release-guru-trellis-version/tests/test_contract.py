from __future__ import annotations

import importlib.util
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


SKILL_ID = "release-guru-trellis-version"
REPO = Path(__file__).resolve().parents[4]
ROOTS = {
    "shared": REPO / ".agents/skills" / SKILL_ID,
    "codex": REPO / ".codex/skills" / SKILL_ID,
    "claude": REPO / ".claude/skills" / SKILL_ID,
    "cursor": REPO / ".cursor/skills" / SKILL_ID,
}
RUNTIME_MODULE = REPO / ".trellis/guru-team/runtime/reviewed_content.py"
PUBLIC_SKILLS = REPO / "trellis/skills/guru-team"
TASK_REF = ".trellis/tasks/09-02-release"
TASK_COMMIT_PACKAGE = PUBLIC_SKILLS / "packages/guru-create-task-commit"
DELIVERY_OWNERS = (
    "guru-review-task-delivery",
    "guru-publish-task-delivery",
    "guru-merge-task-delivery",
    "guru-review-task-completion",
    "guru-complete-task-closure",
    "guru-finish-task",
    "guru-cleanup-task-resources",
)
RETIRED_OWNERS = (
    "guru-review-task-publication",
    "guru-finalize-task",
    "guru-merge-task-pr",
)


def load_reviewed_content_module():
    spec = importlib.util.spec_from_file_location(
        "release_skill_reviewed_content", RUNTIME_MODULE
    )
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot import {RUNTIME_MODULE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


REVIEWED_CONTENT = load_reviewed_content_module()


class SkillContractTest(unittest.TestCase):
    def test_four_agent_projections_are_byte_identical_and_minimal(self) -> None:
        canonical_skill = (ROOTS["shared"] / "SKILL.md").read_bytes()
        canonical_contract = (
            ROOTS["shared"] / "references/contract.md"
        ).read_bytes()

        for name, root in ROOTS.items():
            with self.subTest(platform=name):
                self.assertEqual(canonical_skill, (root / "SKILL.md").read_bytes())
                self.assertEqual(
                    canonical_contract, (root / "references/contract.md").read_bytes()
                )
                files = {
                    path.relative_to(root).as_posix()
                    for path in root.rglob("*")
                    if path.is_file() and "__pycache__" not in path.parts
                }
                expected = {"SKILL.md", "references/contract.md"}
                if name == "shared":
                    expected.add("tests/test_contract.py")
                self.assertEqual(expected, files)

    def test_entrypoint_has_only_required_frontmatter_and_routes_to_contract(self) -> None:
        text = (ROOTS["shared"] / "SKILL.md").read_text(encoding="utf-8")
        match = re.fullmatch(r"---\n(.*?)\n---\n(.*)", text, re.DOTALL)
        self.assertIsNotNone(match)
        frontmatter = match.group(1).splitlines()
        self.assertEqual(2, len(frontmatter))
        self.assertEqual(f"name: {SKILL_ID}", frontmatter[0])
        self.assertTrue(frontmatter[1].startswith("description: "))
        self.assertIn("references/contract.md", match.group(2))
        self.assertLess(len(match.group(2).splitlines()), 12)

    def test_public_marketplace_preset_and_extension_inventories_exclude_skill(self) -> None:
        registry = json.loads(
            (REPO / "trellis/skills/guru-team/registry.json").read_text()
        )
        self.assertNotIn(SKILL_ID, {item["id"] for item in registry["skills"]})
        self.assertFalse((REPO / "trellis/skills/guru-team/packages" / SKILL_ID).exists())

        manifest = (REPO / "trellis/guru-team-extension.json").read_text()
        self.assertNotIn(SKILL_ID, manifest)

        installed_registry = json.loads(
            (REPO / ".trellis/guru-team/skills/registry.json").read_text()
        )
        self.assertNotIn(
            SKILL_ID, {item["id"] for item in installed_registry["skills"]}
        )
        self.assertFalse(
            (
                REPO
                / ".trellis/guru-team/skills/packages"
                / SKILL_ID
            ).exists()
        )
        self.assertNotIn(
            SKILL_ID,
            (REPO / ".trellis/guru-team/extension.json").read_text(),
        )

        for relative in (
            "trellis/index.json",
            "trellis/workflows/guru-team/workflow.md",
            "trellis/workflows/guru-team/README.md",
        ):
            with self.subTest(public_surface=relative):
                self.assertNotIn(
                    SKILL_ID, (REPO / relative).read_text(encoding="utf-8")
                )

        preset = REPO / "trellis/presets/guru-team"
        for path in preset.rglob("*"):
            if (
                not path.is_file()
                or "__pycache__" in path.parts
                or path.suffix in {".pyc", ".pyo"}
            ):
                continue
            with self.subTest(inventory=path.relative_to(REPO).as_posix()):
                self.assertNotIn(SKILL_ID, path.relative_to(REPO).as_posix())
                self.assertNotIn(
                    SKILL_ID, path.read_text(encoding="utf-8", errors="ignore")
                )

    def test_contract_owns_two_stages_two_reviews_and_independent_confirmations(self) -> None:
        contract = (
            ROOTS["shared"] / "references/contract.md"
        ).read_text(encoding="utf-8")
        normalized = " ".join(contract.split())
        self.assertIn("Stage 1: Preparation Task And PR", contract)
        self.assertIn("Stage 2: Post-Merge Exact Candidate", contract)
        for required_input in (
            "repository",
            "current release Issue",
            "target repository tag",
            "target extension revision",
            "official Trellis CLI version",
            "predecessor tag",
        ):
            with self.subTest(required_input=required_input):
                self.assertRegex(contract, rf"(?m)^- {re.escape(required_input)}[.;]$")
        for owner in (
            "standard intake",
            "Phase 2",
            "guru-create-task-commit",
            "guru-review-branch",
            *DELIVERY_OWNERS,
        ):
            with self.subTest(owner=owner):
                self.assertIn(owner, contract)
        for post_merge_gate in (
            "predecessor-to-candidate full diff",
            "version-axis mapping",
            "source and installed validators",
            "Shared/Codex/Claude/Cursor parity",
            "install/update/reapply checks",
            "secret scan",
        ):
            with self.subTest(post_merge_gate=post_merge_gate):
                self.assertIn(post_merge_gate, normalized)
        self.assertIn("residue", normalized)
        self.assertIn("diff hygiene", normalized)
        self.assertIn('TRELLIS_FORK_SOURCE="${trellis_fork_source}"', contract)
        self.assertIn("verify-throwaway-install.sh --mode focused", contract)
        self.assertIn("invocation-local evidence, not a seventh release input", contract)
        self.assertIn("Shared plus selected-platform install (Codex by default)", contract)
        self.assertIn("four-platform source-contract parity remains the separate gate", contract)
        self.assertNotIn("Shared/Codex/Claude/Cursor install", contract)
        self.assertNotIn("GURU_TEAM_THROWAWAY_SINGLE_REPO_COMPATIBILITY", contract)
        honest_path = (
            "stable_plan -> pre_promotion_delivery -> guru-create-task-commit -> "
            "pre_promotion_commit -> guru-review-branch_pre_promotion -> "
            "serialized_architecture_rdt_promotion -> fresh_phase2 -> "
            "guru-create-task-commit -> post_promotion_commit -> "
            "guru-review-branch_post_promotion -> "
            "guru-review-task-delivery -> guru-publish-task-delivery -> "
            "guru-merge-task-delivery -> guru-review-task-completion -> "
            "guru-complete-task-closure:no_mutation -> guru-finish-task -> "
            "guru-cleanup-task-resources"
        )
        self.assertIn(honest_path, contract)
        self.assertEqual(2, honest_path.split(" -> ").count("guru-create-task-commit"))
        self.assertEqual(
            2,
            sum(
                step.startswith("guru-review-branch_")
                for step in honest_path.split(" -> ")
            ),
        )
        self.assertEqual(
            1,
            honest_path.split(" -> ").count("serialized_architecture_rdt_promotion"),
        )
        self.assertIn("The first review cannot be reused", contract)
        self.assertIn("the second review cannot run before promotion", contract)
        self.assertIn("promotion is an intentional reviewed-content mutation", contract)
        self.assertIn("*whole preparation task*", contract)
        self.assertIn("`reference_only`", contract)
        self.assertIn("`Refs #<issue>` with no closing keyword", contract)
        self.assertIn("Closure has no Issue mutation", contract)
        self.assertIn("After Stage 1 Delivery and Finish bookkeeping merges", contract)
        self.assertIn("Verify the remote tag points to the exact", contract)
        self.assertIn("passing smoke for that tag and candidate", contract)
        self.assertIn("separate Issue-closure", contract)
        self.assertIn("Stage 1 reference-only Closure never substitutes", contract)
        for retired in RETIRED_OWNERS:
            self.assertNotIn(retired, contract)

        for boundary in (
            "task commit",
            "preparation PR push/bind/Ready",
            "preparation PR merge",
            "Finish archive projection",
            "Finish bookkeeping publication",
            "Finish bookkeeping PR merge",
            "annotated tag creation/push",
            "tag-pinned smoke",
            "GitHub Release creation",
            "release Issue closure",
            "branch/worktree/task cleanup",
        ):
            with self.subTest(boundary=boundary):
                self.assertIn(f"| {boundary} |", contract)
        self.assertIn("cannot authorize, pre-authorize, or be reused", contract)
        self.assertIn("three distinct", contract)
        self.assertIn("does not authorize the later preparation PR merge", contract)

    def test_stage1_owner_exit_chain_matches_current_interfaces_and_workflow(self) -> None:
        contract = (ROOTS["shared"] / "references/contract.md").read_text()
        workflow = (REPO / ".trellis/workflow.md").read_text()
        expected = (
            ("guru-review-branch", "passed", "guru-review-task-delivery"),
            ("guru-review-task-delivery", "ready", "guru-publish-task-delivery"),
            ("guru-publish-task-delivery", "ready_for_merge", "guru-merge-task-delivery"),
            ("guru-merge-task-delivery", "delivered", "guru-review-task-completion"),
            ("guru-review-task-completion", "completed", "guru-complete-task-closure"),
            ("guru-complete-task-closure", "no_mutation", "guru-finish-task"),
            ("guru-finish-task", "success", "guru-cleanup-task-resources"),
        )
        for owner, exit_id, consumer in expected:
            with self.subTest(owner=owner, exit=exit_id):
                interface = json.loads(
                    (REPO / ".agents/skills" / owner / "interface.json").read_text()
                )
                exits = {item["id"]: item["consumer"] for item in interface["external_exits"]}
                self.assertEqual({"kind": "skill", "id": consumer}, exits[exit_id])
                marker = (
                    '<!-- guru-skill-exit: '
                    + json.dumps(
                        {"skill": owner, "exit": exit_id, "consumer": exits[exit_id]},
                        separators=(",", ":"),
                    )
                    + " -->"
                )
                self.assertIn(marker, workflow)
                self.assertIn(owner, contract)
        for retired in RETIRED_OWNERS:
            self.assertNotIn(retired, contract)

    def test_contract_forbids_tracked_release_state_and_fail_open_routing(self) -> None:
        root = ROOTS["shared"]
        contract = (root / "references/contract.md").read_text(encoding="utf-8")
        owned_files = [path for path in root.rglob("*") if path.is_file()]
        self.assertFalse(
            any(re.fullmatch(r"release-notes.*\.md", path.name) for path in owned_files)
        )
        self.assertNotRegex(contract, r"(?m)^\s*- \[[ xX]\]")
        task = (
            REPO
            / ".trellis/tasks/archive/2026-09/09-02-335-release-guru-trellis-version"
        )
        self.assertFalse(any(task.glob("release-notes*.md")))
        forbidden_task_patterns = (
            "release-status*",
            "review-status*",
            "candidate-status*",
            "*pr-body*",
            "*release-body*",
        )
        for pattern in forbidden_task_patterns:
            with self.subTest(forbidden_task_pattern=pattern):
                self.assertFalse(any(task.glob(pattern)))
        implement = (task / "implement.md").read_text(encoding="utf-8")
        self.assertNotRegex(implement, r"(?m)^\s*- \[[ xX]\]")
        for forbidden in (
            "MUST NOT write tracked lifecycle state",
            "release-status commit",
            "stale evidence",
            "cross-SHA evidence",
            "`FAIL`",
            "`SKIP`",
            "unknown, multiple",
            "unmapped exit",
            "metadata commit",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertIn(forbidden, contract)


class ReviewedContentIdentityTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name) / "fixture"
        subprocess.run(
            ["git", "init", "-q", "-b", "main", str(self.repo)], check=True
        )
        self.inputs = self.repo / ".trellis/.runtime/guru-team/evals/release-skill"
        self.inputs.mkdir(parents=True)
        self.git("config", "user.name", "Release Skill Contract Test")
        self.git("config", "user.email", "release-skill@example.invalid")
        self.git(
            "remote",
            "add",
            "origin",
            "https://github.com/castbox/guru-trellis.git",
        )
        self.write(".gitignore", ".trellis/.runtime/\n")
        self.write(".trellis/config.yaml", "workspace_mode: worktree\n")
        shutil.copytree(REPO / ".trellis/scripts", self.repo / ".trellis/scripts")
        shutil.copytree(
            REPO / "trellis/workflows/guru-team/schemas",
            self.repo / "trellis/workflows/guru-team/schemas",
        )
        self.write("base.txt", "base\n")
        self.git("add", ".")
        self.git("commit", "-qm", "base")
        self.git("switch", "-qc", "feat/335-release-fixture")
        self.write(
            f"{TASK_REF}/implement.md",
            "# Stable implementation plan\n\nNo execution checklist.\n",
        )
        self.write(f"{TASK_REF}/prd.md", "# Fixture task\n")
        self.write(f"{TASK_REF}/design.md", "# Fixture design\n")
        self.write(
            f"{TASK_REF}/task.json",
            json.dumps(
                {
                    "id": Path(TASK_REF).name,
                    "name": Path(TASK_REF).name,
                    "title": "建立 guru-trellis 私有正式发布 Skill",
                    "status": "in_progress",
                    "branch": "feat/335-release-fixture",
                    "base_branch": "main",
                }
            )
            + "\n",
        )
        self.write(".agents/skills/release/SKILL.md", "delivery-v1\n")
        self.write("README.md", "durable-v1\n")
        self.write("config/release.yml", "revision: v1\n")
        self.write("schemas/release.schema.json", '{"revision": "v1"}\n')
        self.write("scripts/release.sh", "#!/usr/bin/env bash\necho v1\n")
        self.write("tests/test_release.py", "EXPECTED = 'v1'\n")
        self.delivery_commit = self.create_delivery_commit()

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

    def write(self, relative: str, content: str) -> None:
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def identity(self, *, include_worktree: bool = False) -> dict[str, str]:
        value = REVIEWED_CONTENT.reviewed_content_identity(
            self.repo, commit="HEAD", include_worktree=include_worktree
        )
        self.assertEqual("guru-reviewed-content-1.0", value["algorithm"])
        return value

    def commit_paths(self, message: str, *paths: str, force: bool = False) -> None:
        add = ["add"]
        if force:
            add.append("-f")
        self.git(*add, *paths)
        self.git("commit", "-qm", message)

    def write_json(self, relative: str, value: dict) -> Path:
        path = self.inputs / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def create_delivery_commit(self) -> dict[str, object]:
        phase2_anchor = self.git("rev-parse", "HEAD")
        self.git("update-ref", "refs/remotes/origin/main", phase2_anchor)
        self.write(
            ".trellis/.runtime/guru-team/owner-checkpoints/09-02-release/"
            "phase2-check.json",
            json.dumps(
                {
                    "typed_exit": "passed",
                    "task_ref": TASK_REF,
                    "phase2_capture_commit": phase2_anchor,
                }
            )
            + "\n",
        )
        public_input = self.write_json(
            "inputs/task-commit-public.json",
            {
                "profile": "initial_commit",
                "mode": "workflow",
                "task_ref": TASK_REF,
                "source_exit": "passed",
                "phase2_commit_anchor": phase2_anchor,
            },
        )
        reviewed_paths = (
            f"{TASK_REF}/design.md",
            f"{TASK_REF}/implement.md",
            f"{TASK_REF}/prd.md",
            f"{TASK_REF}/task.json",
            ".agents/skills/release/SKILL.md",
            "README.md",
            "config/release.yml",
            "schemas/release.schema.json",
            "scripts/release.sh",
            "tests/test_release.py",
        )
        authoring = {
            "path_classifications": [
                {
                    "path": path,
                    "category": "task-reviewed",
                    "reason": "The release delivery path passed the fixture Phase 2 review.",
                    "coverage_source": "guru-check-task fixture",
                }
                for path in reviewed_paths
            ],
            "message": {
                "type": "feat",
                "scope": "release",
                "summary": "create final delivery content",
                "background": "Issue #335 requires one owner-created delivery commit.",
                "changes": "Commit the reviewed release Skill, task, docs, config, schema, script, and test bytes.",
                "boundaries": "Keep publication and release side effects outside this fixture.",
                "validations": "Run the repo-private honest-path contract test.",
            },
            "ai_review": {
                "status": "passed",
                "summary": "The exact delivery paths and commit message are current and sufficient.",
                "evidence": ["The fixture Phase 2 result covers every staged path."],
            },
        }
        prepared = self.run_package_wrapper(
            TASK_COMMIT_PACKAGE,
            "prepare-task-commit.sh",
            "--input",
            public_input.relative_to(self.repo),
            "--candidate-json",
            json.dumps(authoring),
        )
        candidate = Path(str(prepared["candidate_artifact"]))
        checked = self.run_package_wrapper(
            TASK_COMMIT_PACKAGE,
            "check-task-commit-plan.sh",
            "--candidate-artifact",
            candidate,
        )
        self.assertEqual("committed", checked["typed_exit"])
        executed = self.run_package_wrapper(
            TASK_COMMIT_PACKAGE,
            "create-task-commit.sh",
            "--candidate-artifact",
            candidate,
        )
        invocation = self.write_json(
            "inputs/task-commit-invocation.json",
            {
                "result": {
                    **executed,
                    "typed_exit": "committed",
                    "task_ref": TASK_REF,
                    "base_ref": "origin/main",
                    "branch_review_commit": executed["commit_sha"],
                }
            },
        )
        output = self.run_package_wrapper(
            TASK_COMMIT_PACKAGE,
            "invoke.sh",
            "--invocation",
            invocation.relative_to(self.repo),
        )
        self.assertEqual("committed", output["exit_id"])
        self.assertEqual(output["branch_review_commit"], self.git("rev-parse", "HEAD"))
        self.assertFalse(candidate.exists())
        return output

    def run_branch_wrapper(
        self, name: str, *args: object, ok: bool = True
    ) -> dict:
        process = subprocess.run(
            [
                str(PUBLIC_SKILLS / "packages/guru-review-branch/scripts" / name),
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

    def run_package_wrapper(
        self,
        package: Path,
        name: str,
        *args: object,
        ok: bool = True,
        env: dict[str, str] | None = None,
    ) -> dict[str, object]:
        process = subprocess.run(
            [
                str(package / "scripts" / name),
                "--root",
                str(self.repo),
                *map(str, args),
                "--json",
            ],
            cwd=REPO,
            env={**os.environ, **(env or {})},
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

    def record_branch_review(self) -> tuple[Path, Path]:
        base = self.git("rev-parse", "HEAD^")
        self.git("update-ref", "refs/remotes/origin/main", base)
        public_input = self.write_json(
            "inputs/branch-review.json",
            {
                "profile": "branch_review",
                "mode": "workflow",
                "task_ref": TASK_REF,
                "base_ref": "origin/main",
                "branch_review_commit": self.git("rev-parse", "HEAD"),
                "review_intent": "initial_review",
            },
        )
        semantic = self.write_json(
            "inputs/semantic.json",
            {
                "delivery_review": {
                    "task_scope": ["R335-03"],
                    "delivery_slice": ["R335-03"],
                    "remaining_work": [],
                    "independent_delivery_conditions": [
                        "The reviewed preparation slice is independently deliverable."
                    ],
                    "validation_boundaries": [
                        "The release tag and smoke remain post-merge Issue work."
                    ],
                    "current_slice_status": "passed",
                    "remaining_work_status": "disclosed",
                    "summary": "Preparation delivery is complete; release work remains separate.",
                },
                "candidate_classifications": [
                    {
                        "candidate_ref": "candidate-no-defect",
                        "decision": "rejected_not_reproduced",
                        "witness": {
                            "requirement_refs": ["R335-03"],
                            "supported_entry_refs": ["entry:branch-review"],
                            "existing_caller_refs": ["caller:release-skill"],
                            "honest_action_sequence": [
                                "review the complete supported range"
                            ],
                            "defect_observation": "No current defect reproduced.",
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
                        "status": "passed",
                        "summary": "Reviewed the complete fixture range.",
                    },
                },
                "verification_evidence": {
                    "reviewer": "independent-agent-fixture",
                    "review_source": "independent-agent",
                    "evidence": ["Complete fixture range reviewed."],
                },
            },
        )
        result = self.run_branch_wrapper(
            "review-branch.sh",
            "--task",
            TASK_REF,
            "--skill-input",
            public_input,
            "--semantic-review-file",
            semantic,
            "--typed-exit",
            "passed",
        )
        self.assertIn(result["status"], {"recorded", "duplicate"})
        return public_input, (
            self.repo
            / ".trellis/.runtime/guru-team/owner-checkpoints"
            / Path(TASK_REF).name
            / "review-gate.json"
        )

    def test_honest_path_runs_commit_and_branch_review_without_retired_owners(self) -> None:
        delivery_head = str(self.delivery_commit["branch_review_commit"])
        reviewed = self.identity()["sha256"]
        public_input, checkpoint = self.record_branch_review()
        self.assertTrue(checkpoint.is_file())
        checked = self.run_branch_wrapper(
            "check-review-gate.sh", "--task", TASK_REF, "--expected-exit", "passed"
        )
        self.assertEqual("owner_checkpoint_validated", checked["status"])
        projected = self.run_branch_wrapper(
            "invoke.sh", "--task", TASK_REF, "--input", public_input
        )
        self.assertEqual("passed", projected["exit_id"])
        self.assertEqual(delivery_head, self.git("rev-parse", "HEAD"))
        self.assertEqual(reviewed, self.identity(include_worktree=True)["sha256"])
        self.assertFalse(checkpoint.exists())

    def test_delivery_durable_config_script_and_test_drift_change_identity(self) -> None:
        previous = self.identity()["sha256"]
        changes = (
            ("delivery", ".agents/skills/release/SKILL.md", "delivery-v2\n"),
            ("durable", "README.md", "durable-v2\n"),
            ("config", "config/release.yml", "revision: v2\n"),
            ("schema", "schemas/release.schema.json", '{"revision": "v2"}\n'),
            ("script", "scripts/release.sh", "#!/usr/bin/env bash\necho v2\n"),
            ("test", "tests/test_release.py", "EXPECTED = 'v2'\n"),
        )
        for category, relative, content in changes:
            with self.subTest(category=category):
                self.record_branch_review()
                self.write(relative, content)
                self.commit_paths(f"{category} drift", relative)
                current = self.identity()["sha256"]
                self.assertNotEqual(previous, current)
                stale = self.run_branch_wrapper(
                    "check-review-gate.sh",
                    "--task",
                    TASK_REF,
                    ok=False,
                )
                self.assertEqual(
                    ("stale_identity", "reviewed_content_sha256"),
                    (stale["code"], stale["field_path"]),
                )
                previous = current


if __name__ == "__main__":
    unittest.main()
