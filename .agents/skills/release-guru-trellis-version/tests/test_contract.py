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
PUBLICATION_PACKAGE = PUBLIC_SKILLS / "packages/guru-review-task-publication"
FINALIZER_PACKAGE = PUBLIC_SKILLS / "packages/guru-finalize-task"


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

    def test_contract_owns_two_stages_one_review_and_independent_confirmations(self) -> None:
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
            "guru-review-task-publication",
            "guru-finalize-task",
            "guru-merge-task-pr",
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
        honest_path = (
            "stable_plan -> final_delivery_content -> guru-create-task-commit -> "
            "final_delivery_content_commit -> guru-review-branch_once -> "
            "guru-review-task-publication -> guru-finalize-task"
        )
        self.assertIn(honest_path, contract)
        self.assertEqual(1, honest_path.split(" -> ").count("guru-review-branch_once"))

        for boundary in (
            "task commit",
            "branch push",
            "PR creation",
            "Finalizer archive and Ready mutations",
            "preparation PR merge",
            "annotated tag creation/push",
            "tag-pinned smoke",
            "GitHub Release creation",
            "release Issue closure",
            "branch/worktree/task cleanup",
        ):
            with self.subTest(boundary=boundary):
                self.assertIn(f"| {boundary} |", contract)
        self.assertIn("cannot authorize, pre-authorize, or be reused", contract)

    def test_contract_forbids_tracked_release_state_and_fail_open_routing(self) -> None:
        root = ROOTS["shared"]
        contract = (root / "references/contract.md").read_text(encoding="utf-8")
        owned_files = [path for path in root.rglob("*") if path.is_file()]
        self.assertFalse(
            any(re.fullmatch(r"release-notes.*\.md", path.name) for path in owned_files)
        )
        self.assertNotRegex(contract, r"(?m)^\s*- \[[ xX]\]")
        task = REPO / ".trellis/tasks/09-02-335-release-guru-trellis-version"
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
        for package in (PUBLICATION_PACKAGE, FINALIZER_PACKAGE):
            shutil.copytree(
                package,
                self.repo
                / "trellis/skills/guru-team/packages"
                / package.name,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
            )
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
        issue = {
            "number": 335,
            "url": "https://github.com/castbox/guru-trellis/issues/335",
            "title": "建立 guru-trellis 仓库私有正式发布 Skill",
            "reason": "The fixture covers the accepted Issue #335 release workflow.",
        }
        self.write(
            f"{TASK_REF}/issue-scope-ledger.json",
            json.dumps(
                {
                    "schema_version": "2.0",
                    "primary_issue": issue,
                    "close_issues": [issue],
                    "related_issues": [],
                    "followup_issues": [],
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
            f"{TASK_REF}/issue-scope-ledger.json",
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

    def run_publication_wrapper(
        self, branch_output: dict[str, object], reviewed: str
    ) -> dict[str, object]:
        public_input = {
            "profile": "publication_review",
            "mode": "workflow",
            "task_ref": branch_output["task_ref"],
            "branch_review_commit": branch_output["branch_review_commit"],
            "review_intent": "initial_review",
        }
        authored = json.loads(
            (PUBLICATION_PACKAGE / "examples/pr-readiness.json").read_text()
        )
        authored = {
            key: authored[key]
            for key in (
                "candidate_classifications",
                "dimensions",
                "findings",
                "conclusions",
                "route",
            )
        }
        authored.update(
            profile="publication_review",
            mode="workflow",
            review_intent="initial_review",
            pr_payload={
                "title": "完成：建立 guru-trellis 私有正式发布 Skill",
                "body": (
                    "## 变更摘要\n\n- 建立仓库私有正式发布编排。\n\n"
                    "## 影响范围\n\n- 仅影响 guru-trellis 私有 Skill 与 Docs SSOT。\n\n"
                    "## 验证结果\n\n- honest-path owner 链验证通过。\n\n"
                    "## Review Gate\n\n- 完整 Branch Review 无未关闭 finding。\n\n"
                    "## Issue 关闭范围\n\n- Closes #335。\n\n"
                    "## 安全与部署影响\n\n- 不涉及 secret、部署或数据迁移。\n\n"
                    "## Docs SSOT\n\n"
                    "- strategy: delta_first。\n"
                    "- durable docs: README 与正式 Docs SSOT 已同步。\n"
                    "- merged delta: task 增量已写回长期文档。\n"
                    "- task history: task 只保留稳定规划历史。\n"
                    "- follow-up: 无待办或已知限制。"
                ),
            },
        )
        public_path = self.write_json("inputs/publication-public.json", public_input)
        authored_path = self.write_json("inputs/publication-authored.json", authored)
        recorded = self.run_package_wrapper(
            PUBLICATION_PACKAGE,
            "record-task-publication-review.sh",
            "--task",
            TASK_REF,
            "--input",
            authored_path.relative_to(self.repo),
            "--branch-review-commit",
            branch_output["branch_review_commit"],
        )
        self.assertEqual(reviewed, recorded["reviewed_content_sha256"])
        checked = self.run_package_wrapper(
            PUBLICATION_PACKAGE,
            "check-task-publication-review.sh",
            "--task",
            TASK_REF,
            "--expected-exit",
            "ready",
        )
        checkpoint = Path(str(checked["artifact_path"]))
        owner_path = self.write_json(
            "inputs/publication-owner.json", checked["owner_result"]
        )
        output = self.run_package_wrapper(
            PUBLICATION_PACKAGE,
            "invoke.sh",
            "--input",
            public_path,
            "--owner-result",
            owner_path,
        )
        self.assertFalse(checkpoint.exists())
        return output

    def run_finalizer_wrapper(
        self,
        publication_output: dict[str, object],
        reviewed: str,
        delivery_head: str,
    ) -> tuple[dict[str, object], str]:
        public_input = {
            "profile": "publication_ready",
            "mode": "workflow",
            **{
                key: publication_output[key]
                for key in (
                    "task_ref",
                    "branch_review_commit",
                    "pr_title",
                    "pr_body",
                )
            },
        }
        public_path = self.write_json("inputs/finalizer-public.json", public_input)
        plan_digest = "b" * 64
        plan_ref = f"closeout-plan:{plan_digest}"
        archive_ref = ".trellis/tasks/archive/2026-09/09-02-release"

        def write_context(transaction_state: str, publication_head: str) -> None:
            self.write(
                ".trellis/.runtime/guru-team/evals/finalization-context.json",
                json.dumps({
                "schema_version": "2.0",
                "task_ref": TASK_REF,
                "plan_ref": plan_ref,
                "plan_digest": plan_digest,
                "branch_review_commit": publication_output["branch_review_commit"],
                "publication_head": publication_head,
                "archive_locator": archive_ref,
                "repo_ref": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": self.git("branch", "--show-current"),
                "publication_status": "current",
                "publication_stale_reason": None,
                "transaction_state": transaction_state,
                })
                + "\n",
            )

        write_context("prepared", delivery_head)
        review_path = self.write_json(
            "inputs/finalizer-review.json",
            {
                "schema_version": "3.0",
                "skill_id": "guru-finalize-task",
                "review": {
                    "status": "passed",
                    "summary": "The exact current plan can resume without metadata commits.",
                },
                "route": {
                    "typed_exit": "ready_for_merge",
                    "consumer": {"kind": "skill", "id": "guru-merge-task-pr"},
                    "output": {"materialization": "executor"},
                },
            },
        )
        eval_env = {"GURU_TEAM_EVAL_STAGING": "1"}
        preview = self.run_package_wrapper(
            FINALIZER_PACKAGE,
            "preview-finalization.sh",
            "--input",
            public_path.relative_to(self.repo),
            env=eval_env,
        )
        self.assertFalse(preview["side_effects"])
        self.assertEqual("prepared", preview["transaction_state"])
        recorded = self.run_package_wrapper(
            FINALIZER_PACKAGE,
            "record-finalization-gate.sh",
            "--input",
            public_path.relative_to(self.repo),
            "--review-input",
            review_path.relative_to(self.repo),
            env=eval_env,
        )
        gate_path = Path(str(recorded["artifact_path"]))
        checked = self.run_package_wrapper(
            FINALIZER_PACKAGE,
            "check-finalization-gate.sh",
            "--input",
            public_path.relative_to(self.repo),
            "--gate",
            gate_path.resolve().relative_to(self.repo.resolve()),
            env=eval_env,
        )
        self.assertEqual("ready_for_merge", checked["typed_exit"])
        self.assertEqual("prepared", checked["transaction_state"])

        for relative in (
            "task.json",
            "prd.md",
            "design.md",
            "implement.md",
            "issue-scope-ledger.json",
        ):
            self.write(
                f"{archive_ref}/{relative}",
                (self.repo / TASK_REF / relative).read_text(encoding="utf-8"),
            )
        self.write(f"{archive_ref}/finish-summary.json", "{}\n")
        self.assertEqual(reviewed, self.identity(include_worktree=True)["sha256"])
        self.commit_paths("archive lifecycle metadata", archive_ref)
        archive_head = self.git("rev-parse", "HEAD")
        self.assertEqual(delivery_head, self.git("rev-parse", f"{archive_head}^"))
        self.assertEqual("1", self.git("rev-list", "--count", f"{delivery_head}..HEAD"))
        self.assertEqual(reviewed, self.identity()["sha256"])
        write_context("ready", archive_head)

        mock_bin = self.inputs / "bin"
        mock_bin.mkdir(parents=True, exist_ok=True)
        mock_gh = mock_bin / "gh"
        mock_gh.write_text(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "if [[ \"${1:-}\" == auth && \"${2:-}\" == status ]]; then exit 0; fi\n"
            "if [[ \"${1:-}\" == issue && \"${2:-}\" == view && \"${3:-}\" == 174 ]]; then\n"
            "  printf '%s\\n' "
            "'{\"number\":174,\"state\":\"OPEN\",\"url\":\"https://github.com/castbox/guru-trellis/issues/174\"}'\n"
            "  exit 0\n"
            "fi\n"
            "exit 1\n",
            encoding="utf-8",
        )
        mock_gh.chmod(0o755)
        terminal_env = {
            **eval_env,
            "PATH": f"{mock_bin}{os.pathsep}{os.environ['PATH']}",
        }
        executed = self.run_package_wrapper(
            FINALIZER_PACKAGE,
            "execute-finalization-transition.sh",
            "--input",
            public_path.relative_to(self.repo),
            "--gate",
            gate_path.resolve().relative_to(self.repo.resolve()),
            env=terminal_env,
        )
        self.assertEqual("ready_recovered", executed["stage"])
        self.assertEqual("ready_for_merge", executed["typed_exit"])
        self.assertFalse(gate_path.exists())
        return executed["output"], archive_head

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

    def test_honest_path_runs_branch_publication_and_finalizer_wrappers(self) -> None:
        delivery_head = str(self.delivery_commit["branch_review_commit"])
        self.assertEqual(delivery_head, self.git("rev-parse", "HEAD"))
        reviewed = self.identity()["sha256"]
        public_input, checkpoint = self.record_branch_review()
        self.assertTrue(checkpoint.is_file())
        self.assertEqual(delivery_head, self.git("rev-parse", "HEAD"))

        metadata = {
            ".trellis/workspace/test/journal.md": "workspace metadata\n",
            ".trellis/.runtime/guru-team/checkpoint.json": "{}\n",
            "nested/.DS_Store": "noise\n",
        }
        for relative, content in metadata.items():
            self.write(relative, content)
        self.assertEqual(reviewed, self.identity(include_worktree=True)["sha256"])
        self.assertEqual(delivery_head, self.git("rev-parse", "HEAD"))

        self.write(
            ".trellis/.runtime/guru-team/checkpoint.json",
            '{"state":"replaced"}\n',
        )
        self.assertEqual(reviewed, self.identity(include_worktree=True)["sha256"])
        self.assertEqual(delivery_head, self.git("rev-parse", "HEAD"))

        checked = self.run_branch_wrapper(
            "check-review-gate.sh", "--task", TASK_REF, "--expected-exit", "passed"
        )
        self.assertEqual("ok", checked["status"])
        projected = self.run_branch_wrapper(
            "invoke.sh", "--task", TASK_REF, "--input", public_input
        )
        self.assertEqual("passed", projected["exit_id"])
        self.assertFalse(checkpoint.exists())
        self.assertEqual(reviewed, self.identity(include_worktree=True)["sha256"])
        self.assertEqual(delivery_head, self.git("rev-parse", "HEAD"))
        publication = self.run_publication_wrapper(projected, reviewed)
        self.assertEqual("ready", publication["exit_id"])
        self.assertEqual(delivery_head, self.git("rev-parse", "HEAD"))
        finalizer, archive_head = self.run_finalizer_wrapper(
            publication,
            reviewed,
            delivery_head,
        )
        self.assertEqual("ready_for_merge", finalizer["exit_id"])
        self.assertEqual(archive_head, finalizer["expected_head_sha"])
        self.assertEqual(archive_head, self.git("rev-parse", "HEAD"))
        self.assertEqual(delivery_head, self.git("rev-parse", f"{archive_head}^"))
        self.assertEqual("1", self.git("rev-list", "--count", f"{delivery_head}..HEAD"))
        self.assertEqual(reviewed, self.identity(include_worktree=True)["sha256"])

        registry = json.loads((PUBLIC_SKILLS / "registry.json").read_text())
        by_id = {item["id"]: item for item in registry["skills"]}
        branch_interface = json.loads(
            (PUBLIC_SKILLS / by_id["guru-review-branch"]["interface"]).read_text()
        )
        publication_interface = json.loads(
            (
                PUBLIC_SKILLS
                / by_id["guru-review-task-publication"]["interface"]
            ).read_text()
        )
        branch_exits = {
            item["id"]: item["consumer"]["id"]
            for item in branch_interface["external_exits"]
        }
        publication_exits = {
            item["id"]: item["consumer"]["id"]
            for item in publication_interface["external_exits"]
        }
        self.assertEqual("guru-review-task-publication", branch_exits["passed"])
        self.assertEqual("guru-finalize-task", publication_exits["ready"])

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
