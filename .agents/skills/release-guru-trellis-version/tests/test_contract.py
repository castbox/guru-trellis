from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
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
PUBLIC_SKILLS = REPO / "trellis/skills/guru-team"
sys.path.insert(0, str(PUBLIC_SKILLS))
from runtime.delivery_projection.adapter import authority_ref

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


def load_fixture(name: str, relative: str):
    path = PUBLIC_SKILLS / "packages" / relative
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
        self.assertIn("local installation convergence", match.group(2))

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

    def test_contract_owns_current_delivery_chain_and_independent_release_boundaries(self) -> None:
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
        self.assertIn("one clean Shared plus Codex install", contract)
        self.assertIn('TRELLIS_PREDECESSOR_COMMIT="${predecessor_fork_commit}"', contract)
        self.assertIn("four-platform source-contract parity remains the separate gate", contract)
        self.assertNotIn("Shared/Codex/Claude/Cursor install", contract)
        self.assertNotIn("GURU_TEAM_THROWAWAY_SINGLE_REPO_COMPATIBILITY", contract)
        honest_path = (
            "stable_plan -> implementation_and_engineering_checks -> "
            "necessary_rdt_architecture_integration_and_readback -> "
            "guru-create-task-commit -> constructor/begin_check -> "
            "guru-review-branch -> publication_architecture_eligibility -> "
            "guru-review-task-delivery -> guru-publish-task-delivery -> "
            "guru-merge-task-delivery -> guru-review-task-completion"
        )
        self.assertIn(honest_path, contract)
        for responsibility in (
            "`pre_review_committed` enters only the original implementation router",
            "`check` then `full_review`",
            "successor content changes",
            "Complete Source Before Actual Adoption",
            "Only after D1 is actually `delivered`",
            "`additional_delivery_required`",
            "planning router invokes Creation to establish D2",
            "D2 receives its own Planning and Activation",
            "D1 source defects or required",
            "matching complete original",
        ):
            self.assertIn(responsibility, normalized)
        self.assertIn("*whole preparation task*", contract)
        self.assertIn("`reference_only`", contract)
        self.assertIn("`Refs #<issue>` with no closing keyword", contract)
        self.assertIn("Closure must return `no_mutation`", contract)
        self.assertIn("After Stage 1 Delivery and Finish bookkeeping merges", contract)
        self.assertIn("Verify the remote tag points to the exact", contract)
        self.assertIn("passing smoke for that tag and candidate", contract)
        self.assertIn("separate Issue-closure", contract)
        self.assertIn("Stage 1 reference-only Closure never substitutes", normalized)
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
                self.assertIn(owner, workflow)
                self.assertIn(consumer, workflow)
                self.assertIn(owner, contract)
        completion = json.loads((PUBLIC_SKILLS / "packages/guru-review-task-completion/interface.json").read_text())
        consumer = next(row["consumer"] for row in completion["external_exits"]
                        if row["id"] == "additional_delivery_required")
        self.assertEqual({"kind": "workflow", "id": "task-delivery-planning-router"}, consumer)
        self.assertIn("guru-create-delivery", workflow)
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


class PreparationDeliveryFlowTest(unittest.TestCase):
    """Real public producers; fixture judgments and PR facts are not AI/GitHub proof."""

    def setUp(self) -> None:
        module = load_fixture("release_delivery_flow", "guru-check-task/tests/test_delivery_flow.py")
        self.flow = module.DeliveryFlow()
        self.flow.delivery_profile = "pull_request"
        self.flow.setUp()
        self.addCleanup(self.flow.doCleanups)
        self.repo, self.key = self.flow.repo, self.flow.key
        self.projection = self.flow.projection
        module = load_fixture("release_commit_fixture", "guru-create-task-commit/tests/test_committed_reentry.py")
        self.commit_owner = module.CommittedReentryTest()
        self.commit_owner.fixture = self.flow
        self.commit_owner.repo, self.commit_owner.key = self.repo, self.key
        self.commit_owner.task_ref, self.commit_owner.projection = self.flow.task_ref, self.projection
        # The reused fixture establishes only the pre-test Planning boundary.
        # This test's business increment is committed by the actual TaskCommit.
        self.commit_owner.restart_implementation()
        self.base = self.projection.content_base(self.key)

    def commit_increment(self, relative="release-contract.md", content="Current release consumer.\n"):
        self.commit_owner.restart_implementation()
        (self.repo / relative).write_text(content)
        prepared = self.commit_owner.prepare({})
        before = int(self.flow.git("rev-list", "--count", "HEAD"))
        args = ("--candidate-artifact", prepared["candidate_artifact"])
        output = self.flow.wrapper("guru-create-task-commit", "invoke.sh", *args)
        self.assertEqual("pre_review_committed", output["exit_id"])
        self.assertEqual(output, self.flow.wrapper("guru-create-task-commit", "invoke.sh", *args))
        self.assertEqual(before + 1, int(self.flow.git("rev-list", "--count", "HEAD")))
        self.assertEqual(output["branch_review_commit"], self.flow.git("rev-parse", "HEAD").strip())
        return output

    def begin_check(self, *paths):
        head = self.flow.git("rev-parse", "HEAD").strip()
        result = subprocess.run(
            ["bash", str(REPO / "trellis/workflows/guru-team/scripts/bash/construct-delivery-candidate.sh"),
             "--root", str(self.repo), "--task", self.flow.task_ref,
             "--delivery-key", json.dumps(self.key), "--development-base", self.base,
             "--head", head, "--paths", *paths],
            capture_output=True, text=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        candidate = json.loads(result.stdout)
        operation = {"api_version": "1.0", "operation": "begin_check", "key": self.key,
                     "owner_role": "implementation",
                     "owner_id": self.projection.declaration()["owners"]["implementation"],
                     "expected_phase": "implementing", "candidate": candidate}
        result = subprocess.run(
            [sys.executable, str(REPO / ".trellis/scripts/delivery.py"), "begin-check",
             "--task", self.flow.task_ref, "--input", self.flow.write("begin-check.json", operation)],
            cwd=self.repo, capture_output=True, text=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(candidate, self.projection.resolve(self.key)["candidate"])
        self.assertEqual(self.base, candidate["base_ref"])
        return candidate

    def record_review(self):
        self.flow.head = self.flow.git("rev-parse", "HEAD").strip()
        public = {"profile": "delivery_branch_review", "mode": "workflow",
                  "task_ref": self.flow.task_ref, "delivery_key": self.key,
                  "base_ref": self.base, "branch_review_commit": self.flow.head,
                  "review_intent": "initial_review"}
        authoring = json.loads((PUBLIC_SKILLS / "packages/guru-review-branch/examples/authoring-delivery-passed-2.0.json").read_text())
        self.flow.wrapper("guru-review-branch", "review-branch.sh", "--task", self.flow.task_ref,
                          "--skill-input", self.flow.write("review.json", public),
                          "--semantic-review-file", self.flow.write("review-owner.json", authoring),
                          "--typed-exit", "passed")
        checked = self.flow.wrapper("guru-review-branch", "check-review-gate.sh", "--task", self.flow.task_ref,
                                    "--delivery-key", json.dumps(self.key))
        self.assertFalse(checked["formal_exit"])
        return public

    def invoke_review(self, public, success=True):
        return self.flow.wrapper("guru-review-branch", "invoke.sh", "--input",
                                 self.flow.write("review.json", public), success=success)

    def checkpoint(self):
        return (self.repo / ".trellis/.runtime/guru-team/owner-checkpoints" /
                self.key["task_id"] / self.key["delivery_id"] / "review-gate.json")

    def reviewed(self):
        self.commit_increment()
        self.begin_check("release-contract.md")
        public = self.record_review()
        output = self.invoke_review(public)
        self.assertEqual(output, self.invoke_review(public))
        self.assertFalse(self.checkpoint().exists())
        return output

    def test_current_commit_constructor_review_two_slots_and_readiness(self):
        output = self.reviewed()
        results = self.projection.resolve(self.key)["results"]
        self.assertEqual("planning:flow", results["check"]["predecessor_result_id"])
        self.assertEqual(results["check"]["result_id"], results["full_review"]["predecessor_result_id"])
        self.assertEqual(output["full_review_result_id"], results["full_review"]["result_id"])
        self.assertEqual(results["check"]["candidate"], results["full_review"]["candidate"])
        self.assertEqual("guru-review-branch", results["check"]["owner_id"])
        self.assertEqual("ready", self.flow.readiness(output)["exit_id"])

    def test_original_review_resumes_missing_second_slot_without_new_judgment(self):
        self.commit_increment()
        self.begin_check("release-contract.md")
        public = self.record_review()
        # Resume at the existing first-projection boundary with its real owner result.
        sys.path.insert(0, str(PUBLIC_SKILLS / "packages/guru-review-branch/runtime"))
        from delivery_review import result_id
        from runtime.delivery_projection.gates import record_gate
        owner = json.loads(self.checkpoint().read_text())
        check_id = result_id(owner, "check")
        record_gate(self.projection, self.key, "check", check_id,
                    owner["gate_judgments"]["check"]["outcome"],
                    [authority_ref(self.projection.planning_directory(self.key) / "implement.md", self.repo)], [])
        self.assertIsNone(self.projection.resolve(self.key)["results"]["full_review"])
        reviewed = self.invoke_review(public)
        self.assertEqual(check_id, self.projection.resolve(self.key)["results"]["check"]["result_id"])
        self.assertEqual(reviewed, self.invoke_review(public))
        self.assertEqual("ready", self.flow.readiness(reviewed)["exit_id"])

    def test_real_successor_needs_current_review_and_cannot_publish_old_readiness(self):
        from unittest.mock import patch
        ready = self.flow.readiness(self.reviewed())
        old_public = {"profile": "delivery_review_ready", "mode": "workflow",
                      "task_ref": self.flow.task_ref, "delivery_key": self.key,
                      "readiness_result_id": ready["readiness_result_id"],
                      "reviewed_head": self.flow.head, "pr_title": ready["pr_title"],
                      "pr_body": ready["pr_body"], "remaining_work_state": ready["remaining_work_state"]}
        prior = self.projection.resolve(self.key)["candidate"]
        self.commit_increment("consumer.txt", "A genuine successor consumer.\n")
        candidate = self.begin_check("consumer.txt")
        self.assertNotEqual(prior["content_ref"], candidate["content_ref"])
        self.assertTrue({"app.txt", "release-contract.md", "consumer.txt"}.issubset(candidate["paths"]))
        package, owner = self.flow.load_owner("guru-publish-task-delivery")
        review = {"schema_version": "1.0", "skill_id": package.name,
                  "review": {"status": "passed", "summary": "Fixture boundary only."},
                  "route": {"typed_exit": "ready_for_merge"}}
        with patch.object(owner, "execute") as remote:
            rejected = owner.invoke(self.repo.resolve(), old_public, review, None)
            self.assertEqual("review_stale", rejected["exit_id"])
            remote.assert_not_called()
        self.assertIsNone(self.projection.resolve(self.key)["results"]["full_review"])
        new_review = self.invoke_review(self.record_review())
        self.assertEqual("ready", self.flow.readiness(new_review)["exit_id"])
        self.assertNotEqual(ready["readiness_result_id"], self.projection.resolve(self.key)["results"]["readiness"]["result_id"])

    def test_delivered_source_remaining_adoption_enters_completion_then_creation(self):
        import hashlib
        ready = self.flow.readiness(self.reviewed())
        candidate = self.projection.resolve(self.key)["candidate"]
        evidence = [authority_ref(self.repo / "release-contract.md", self.repo)]
        # Read-only provider facts describe a completed remote boundary. They do
        # not claim real GitHub mutation; the public fact validators still run.
        with self.flow.provider_response(body=ready["pr_body"]):
            self.projection.apply({"api_version": "1.0", "operation": "record_publication", "key": self.key,
                "owner_role": "publication", "owner_id": "guru-test-publication", "expected_phase": "publishing",
                "result": {"result_id": "publication:release-source", "owner_id": "guru-test-publication",
                    "evidence": evidence, "profile": "pull_request", "candidate": candidate,
                    "repo_ref": "example/repo", "pr_number": 9, "reviewed_head": self.flow.head,
                    "target_ref": "main", "publication_ref": {"locator": "https://github.com/example/repo/pull/9",
                        "revision": "sha256:" + hashlib.sha256(ready["pr_body"].encode()).hexdigest()}}})
        with self.flow.provider_response(body=ready["pr_body"], merged=True):
            self.projection.apply({"api_version": "1.0", "operation": "record_delivery", "key": self.key,
                "owner_role": "delivery", "owner_id": "guru-test-delivery", "expected_phase": "publishing",
                "result": {"result_id": "delivery:release-source", "owner_id": "guru-test-delivery",
                    "evidence": evidence, "profile": "pull_request", "candidate": candidate,
                    "repo_ref": "example/repo", "pr_number": 9, "reviewed_head": self.flow.head,
                    "merge_commit": "f" * 40, "target_ref": "main"}})
        self.assertEqual("delivered", self.projection.resolve(self.key)["phase"])
        task_key = {name: self.key[name] for name in ("task_id", "lifecycle_generation")}
        public = {"profile": "delivery_completion", "mode": "workflow", "task_ref": self.flow.task_ref,
                  "task_key": task_key}
        semantic = {"profile": public["profile"], "mode": public["mode"], "reviewed_task_key": task_key,
                    "reviewed_scope": self.projection.read_record()["accepted_scope"],
                    "reviewed_delivery_result_ids": ["delivery:release-source"], "evidence": evidence,
                    "remaining_work_refs": ["scope:actual-adoption"], "result_id": "completion:release-source",
                    "route": {"typed_exit": "additional_delivery_required", "reason": {
                        "reason_code": "actual_adoption_unimplemented", "reason_refs": ["scope:actual-adoption"]}}}
        pending = self.flow.wrapper("guru-review-task-completion", "invoke.sh", "--input",
            self.flow.write("completion.json", public), "--semantic-result", self.flow.write("completion-owner.json", semantic))
        self.assertEqual("additional_delivery_required", pending["exit_id"])
        self.assertEqual([], self.projection.read_record()["completion_results"])
        creation = {"profile": "delivery_creation", "mode": "workflow", "task_ref": pending["task_ref"],
                    "task_key": pending["task_key"], "scope_ref": {
                        "authority": self.projection.read_record()["accepted_scope"], "anchors": ["R1"]},
                    "delivery_profile": "pull_request", "continuation_id": "actual-adoption", "action": "create"}
        owner = {"typed_exit": "created",
                 "reason": "Fixture accepted remaining actual adoption after source Delivery."}
        created = self.flow.wrapper("guru-create-delivery", "invoke.sh", "--input", self.flow.write("creation.json", creation),
                                    "--owner-result", self.flow.write("creation-owner.json", owner))
        self.assertEqual("created", created["exit_id"])
        self.assertNotEqual(self.key, created["delivery_key"])
        self.assertEqual(task_key, {name: created["delivery_key"][name] for name in task_key})
        successor = self.projection.resolve(created["delivery_key"])
        self.assertEqual("planning", successor["phase"])
        self.assertIsNone(successor["results"]["planning"])
        self.assertEqual("delivered", self.projection.resolve(self.key)["phase"])


if __name__ == "__main__":
    unittest.main()
