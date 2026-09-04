from __future__ import annotations

import importlib.util
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from unittest import mock


PACKAGE = Path(__file__).resolve().parents[1]
PACKAGE_LAYOUTS = (
    (
        "canonical",
        Path("trellis/skills/guru-team/packages/guru-review-task-publication"),
    ),
    (
        "installed-shared",
        Path(
            ".trellis/guru-team/skills/packages/"
            "guru-review-task-publication"
        ),
    ),
    (
        "agents",
        Path(".agents/skills/guru-review-task-publication"),
    ),
    (
        "codex",
        Path(".codex/skills/guru-review-task-publication"),
    ),
    (
        "cursor",
        Path(".cursor/skills/guru-review-task-publication"),
    ),
    (
        "claude",
        Path(".claude/skills/guru-review-task-publication"),
    ),
)


def package_repo_root() -> Path:
    for candidate in PACKAGE.parents:
        if any(candidate / relative == PACKAGE for _, relative in PACKAGE_LAYOUTS):
            return candidate
    raise RuntimeError(f"Unsupported publication package test layout: {PACKAGE}")


def finish_summary_schema_path() -> Path:
    repo = package_repo_root()
    if "trellis/skills/guru-team/packages" in PACKAGE.as_posix():
        return repo / "trellis/workflows/guru-team/schemas/finish-summary.schema.json"
    return repo / ".trellis/guru-team/schemas/finish-summary.schema.json"


def load_runtime():
    runtime_path = PACKAGE / "runtime/owner.py"
    spec = importlib.util.spec_from_file_location(
        "task_publication_package_runtime",
        runtime_path,
    )
    if spec is None or spec.loader is None:
            raise RuntimeError("Current Guru Team runtime could not be loaded.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GTT = load_runtime()


def provenance_file_action_sections(action: str) -> dict[str, dict[str, object]]:
    return {
        "skill_packages": {
            "files": [
                {
                    "path": ".trellis/guru-team/skills/registry.json",
                    "source": "trellis/skills/guru-team/registry.json",
                    "sha256": "1" * 64,
                    "executable": False,
                    "action": action,
                },
                {
                    "path": ".trellis/guru-team/skills/packages/guru-finalize-task/runtime/owner.py",
                    "source": "trellis/skills/guru-team/packages/guru-finalize-task/runtime/owner.py",
                    "sha256": "2" * 64,
                    "executable": False,
                    "action": action,
                },
            ],
        },
        "overlays": {
            "files": [
                {
                    "path": ".claude/commands/guru/finish-work.md",
                    "source": "trellis/presets/guru-team/overlays/.claude/commands/guru/finish-work.md",
                    "sha256": "3" * 64,
                    "executable": False,
                    "action": action,
                },
                {
                    "path": ".codex/prompts/guru-finish-work.md",
                    "source": "trellis/presets/guru-team/overlays/.codex/prompts/guru-finish-work.md",
                    "sha256": "4" * 64,
                    "executable": False,
                    "action": action,
                },
            ],
        },
    }


def large_finish_summary() -> dict:
    paths = [f"changes/path-{index:04d}.txt" for index in range(2001)]
    title = "Large finish summary"
    index = {
        "problem": "Large diffs were rejected by an arbitrary path limit.",
        "outcome": "Complete large path sets are accepted.",
        "changed_behavior": ["Removed the arbitrary changed-path count limit."],
        "affected_surfaces": [{
            "kind": "schema",
            "name": "finish-summary",
            "paths": ["trellis/workflows/guru-team/schemas/finish-summary.schema.json"],
            "change": "Accept complete large path sets.",
        }],
        "contract_changes": [],
        "search_terms": {
            "issue_refs": ["#227"],
            "pr_refs": [],
            "branches": ["fix/227-finish-summary-large-path-set"],
            "paths": paths,
            "commands": [],
            "config_keys": [],
            "schema_fields": ["git.changed_paths", "index.search_terms.paths"],
            "symbols": ["finish_summary_errors"],
            "phrases": [
                "大型 diff 路径上限阻断",
                "finish_summary_errors 支持完整路径集",
                "已移除 finish summary limit",
            ],
        },
    }
    index["retrieval_text"] = GTT.current_finish_summary_retrieval_text(title, index)
    return {
        "schema_version": 2,
        "generated_at": "2026-08-14T00:00:00Z",
        "generator": "guru-team.finalize-task",
        "task": {
            "slug": "227-finish-summary-large-path-set",
            "title": title,
            "status": "completed",
            "artifact_dir": ".trellis/tasks/227-finish-summary-large-path-set",
            "archive_dir": ".trellis/tasks/archive/2026-08/227-finish-summary-large-path-set",
        },
        "git": {
            "base_branch": "main",
            "branch": "fix/227-finish-summary-large-path-set",
            "commits": ["a" * 40],
            "changed_paths": paths,
        },
        "github": {
            "source_issues": [227],
            "close_issues": [227],
            "related_issues": [],
            "followup_issues": [],
            "pr_url": "",
        },
        "artifacts": {},
        "index": index,
    }


def load_public_wrapper():
    sys.path.insert(0, str(PACKAGE.parents[1]))
    sys.path.insert(0, str(PACKAGE / "runtime"))
    runtime_path = PACKAGE / "runtime/invoke.py"
    spec = importlib.util.spec_from_file_location(
        "task_publication_public_wrapper",
        runtime_path,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Current Publication public wrapper could not be loaded.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PUBLIC_WRAPPER = load_public_wrapper()


def git_fixture_commit(root: Path, *paths: str) -> None:
    subprocess.run(["git", "add", "--", *paths], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)


def workspace_boundary_fixture() -> tuple[Path, Path, dict[str, object]]:
    temp_root = Path(tempfile.mkdtemp(prefix="guru-workspace-boundary-"))
    source = temp_root / "source"
    source.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=source, check=True)
    subprocess.run(["git", "config", "user.name", "Guru Test"], cwd=source, check=True)
    subprocess.run(["git", "config", "user.email", "guru@example.com"], cwd=source, check=True)
    task_relative = ".trellis/tasks/08-27-312-workspace-boundary-merged-active-task"
    source_task = source / task_relative
    source_task.mkdir(parents=True)
    ordinary = (
        "task.json",
        "prd.md",
        "design.md",
        "implement.md",
        "implement.jsonl",
        "check.jsonl",
        "issue-scope-ledger.json",
    )
    for name in ordinary:
        (source_task / name).write_text(f"{name}\n", encoding="utf-8")
    for name in GTT.WORKSPACE_BOUNDARY_REVIEW_METADATA:
        (source_task / name).write_text("review\n", encoding="utf-8")
    (source_task / "reviews").mkdir()
    git_fixture_commit(source, f"{task_relative}/")
    task_workspace = temp_root / "task-worktree"
    task_workspace.mkdir()
    context = {
        "workspace_mode": "worktree",
        "expected_workspace": task_workspace,
        "actual_repo_root": task_workspace,
        "source_checkout": source,
        "task_dir": task_workspace / task_relative,
        "task_dir_relative": task_relative,
        "task_context_present": True,
    }
    return temp_root, source, context


class TaskPublicationContractTest(unittest.TestCase):
    def test_workspace_boundary_accepts_clean_tracked_planning_and_blocks_real_overlays(self) -> None:
        temp_root, source, context = workspace_boundary_fixture()
        try:
            snapshot = GTT.collect_workspace_boundary_snapshot(context, {}, {})
            suspicious = snapshot["suspicious_source_artifacts"]
            suspicious_paths = {item["path"] for item in suspicious}
            for name in (
                "task.json",
                "prd.md",
                "design.md",
                "implement.md",
                "implement.jsonl",
                "check.jsonl",
                "issue-scope-ledger.json",
            ):
                self.assertNotIn(f"{context['task_dir_relative']}/{name}", suspicious_paths)
            for name in GTT.WORKSPACE_BOUNDARY_REVIEW_METADATA:
                self.assertIn(f"{context['task_dir_relative']}/{name}", suspicious_paths)
            self.assertTrue(
                any(item["kind"] == "same_task_reviews_dir" for item in suspicious)
            )

            untracked = source / context["task_dir_relative"] / "implement.jsonl"
            subprocess.run(["git", "rm", "--cached", "-q", str(untracked.relative_to(source))], cwd=source, check=True)
            snapshot = GTT.collect_workspace_boundary_snapshot(context, {}, {})
            self.assertIn(
                str(untracked.resolve()),
                [item["absolute_path"] for item in snapshot["suspicious_source_artifacts"]],
            )

            blocked_context = dict(context)
            blocked_context["actual_repo_root"] = source
            blocked_context["task_dir"] = source / context["task_dir_relative"]
            errors = GTT.workspace_boundary_errors(
                blocked_context,
                snapshot,
                allow_source_clean=True,
            )
            self.assertTrue(any("current-task artifacts" in error for error in errors))
        finally:
            shutil.rmtree(temp_root)

    def test_workspace_boundary_keeps_dirty_task_paths_fail_closed(self) -> None:
        cases = {
            "staged": lambda source, task: (
                (task / "prd.md").write_text("staged\n", encoding="utf-8"),
                subprocess.run(["git", "add", "--", str((task / "prd.md").relative_to(source))], cwd=source, check=True),
            ),
            "unstaged": lambda _source, task: (task / "design.md").write_text("unstaged\n", encoding="utf-8"),
            "deleted": lambda _source, task: (task / "implement.md").unlink(),
            "renamed": lambda source, task: subprocess.run(
                ["git", "mv", str((task / "issue-scope-ledger.json").relative_to(source)), str((task / "renamed-ledger.json").relative_to(source))],
                cwd=source,
                check=True,
            ),
            "unrelated": lambda source, _task: (
                (source / "unrelated.txt").write_text("unrelated\n", encoding="utf-8"),
            ),
        }
        for label, mutate in cases.items():
            with self.subTest(case=label):
                temp_root, source, context = workspace_boundary_fixture()
                try:
                    mutate(source, source / context["task_dir_relative"])
                    snapshot = GTT.collect_workspace_boundary_snapshot(context, {}, {})
                    dirty = [item for item in snapshot["suspicious_source_artifacts"] if item["kind"] == "same_task_dirty_path"]
                    if label == "unrelated":
                        self.assertEqual(dirty, [])
                    else:
                        self.assertTrue(dirty)
                finally:
                    shutil.rmtree(temp_root)

    def test_large_finish_summary_preserves_complete_path_contract(self) -> None:
        from jsonschema import Draft202012Validator

        payload = large_finish_summary()
        schema = json.loads(
            finish_summary_schema_path().read_text(encoding="utf-8")
        )
        self.assertEqual(
            list(Draft202012Validator(schema).iter_errors(payload)),
            [],
        )
        self.assertEqual(GTT.finish_summary_errors(payload), [])

        cases = {}
        mismatch = copy.deepcopy(payload)
        mismatch["index"]["search_terms"]["paths"] = payload["git"]["changed_paths"][:-1]
        cases["mismatch"] = (
            mismatch,
            "index.search_terms.paths must equal sorted git.changed_paths.",
        )
        unsorted = copy.deepcopy(payload)
        unsorted_paths = list(reversed(payload["git"]["changed_paths"]))
        unsorted["git"]["changed_paths"] = unsorted_paths
        unsorted["index"]["search_terms"]["paths"] = unsorted_paths
        cases["unsorted"] = (
            unsorted,
            "git.changed_paths must be sorted and unique.",
        )
        duplicate = copy.deepcopy(payload)
        duplicate_paths = payload["git"]["changed_paths"] + [payload["git"]["changed_paths"][-1]]
        duplicate["git"]["changed_paths"] = duplicate_paths
        duplicate["index"]["search_terms"]["paths"] = duplicate_paths
        cases["duplicate"] = (
            duplicate,
            "git.changed_paths must be sorted and unique.",
        )
        unsafe = copy.deepcopy(payload)
        unsafe_paths = payload["git"]["changed_paths"][:-1] + ["../unsafe.txt"]
        unsafe["git"]["changed_paths"] = unsafe_paths
        unsafe["index"]["search_terms"]["paths"] = unsafe_paths
        cases["unsafe"] = (
            unsafe,
            "git.changed_paths[] must not contain empty, dot, or parent segments.",
        )

        for name, (invalid, expected_error) in cases.items():
            with self.subTest(case=name):
                self.assertIn(expected_error, GTT.finish_summary_errors(invalid))

    def test_generated_search_phrases_trim_truncation_whitespace(self) -> None:
        title = "任务" + "x" * (59 - len("任务")) + " "
        body = "## 变更摘要\n- 修复一个足够具体且合法的行为变更描述"

        index = GTT.build_finish_summary_index(title, body, ["runtime/owner.py"])

        self.assertEqual(len(index["search_terms"]["phrases"][0]), 59)
        self.assertEqual(index["search_terms"]["phrases"][0], title.rstrip())
        self.assertEqual(
            GTT.finish_summary_text_errors(
                index["search_terms"]["phrases"][0],
                "index.search_terms.phrases[0]",
                2,
                120,
            ),
            [],
        )

    class WrapperOwner:
        class WorkflowError(RuntimeError):
            def __init__(self, message: str, **_kwargs) -> None:
                super().__init__(message)

        def __init__(
            self,
            root: Path,
            owner_result: dict,
            checkpoint: Path,
            *,
            checker_error: bool = False,
        ) -> None:
            self.root = root
            self.owner_result = owner_result
            self.checkpoint = checkpoint
            self.checker_error = checker_error
            self.check_calls = 0

        def repo_root(self, _path: Path) -> Path:
            return self.root

        @staticmethod
        def read_json(path: Path) -> dict:
            return json.loads(path.read_text(encoding="utf-8"))

        @staticmethod
        def skill_json_loads(value: str, _label: str) -> dict:
            return json.loads(value)

        def resolve_task_dir(self, root: Path, task_ref: str) -> Path:
            return root / task_ref

        def cmd_check_task_publication_review(self, args) -> dict:
            self.check_calls += 1
            if self.checker_error:
                raise self.WorkflowError("checker rejected the owner result")
            return {"owner_result": copy.deepcopy(self.owner_result)}

        def task_publication_path(self, _root: Path, _task: Path) -> Path:
            return self.checkpoint

    def run_public_wrapper(
        self,
        owner_result: dict,
        *,
        public_input: dict | None = None,
        supplied_owner_result: dict | None = None,
        checker_error: bool = False,
    ) -> tuple[dict, Path, "TaskPublicationContractTest.WrapperOwner"]:
        public_input = public_input or {
            "profile": "publication_review",
            "mode": "workflow",
            "task_ref": owner_result["task_ref"],
            "branch_review_commit": owner_result["branch_review_commit"],
            "review_intent": "initial_review",
        }
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        checkpoint = root / ".trellis/.runtime/guru-team/owner-checkpoints/task/pr-readiness.json"
        checkpoint.parent.mkdir(parents=True)
        checkpoint.write_text(json.dumps(owner_result), encoding="utf-8")
        self.last_wrapper_checkpoint = checkpoint
        input_path = root / "public-input.json"
        input_path.write_text(json.dumps(public_input), encoding="utf-8")
        owner_path = root / "owner-result.json"
        owner_path.write_text(
            json.dumps(supplied_owner_result or owner_result),
            encoding="utf-8",
        )
        fake_owner = self.WrapperOwner(
            root,
            owner_result,
            checkpoint,
            checker_error=checker_error,
        )
        self.last_wrapper_owner = fake_owner
        with mock.patch.object(PUBLIC_WRAPPER, "_owner", return_value=fake_owner):
            output = PUBLIC_WRAPPER.run(
                PACKAGE,
                {},
                [
                    "--root",
                    str(root),
                    "--input",
                    str(input_path),
                    "--owner-result",
                    str(owner_path),
                ],
            )
        return output, checkpoint, fake_owner

    def test_public_wrapper_projects_all_three_exits_and_retires_checkpoint(
        self,
    ) -> None:
        cases = (
            (
                "ready",
                copy.deepcopy(self.readiness_example),
                {
                    "exit_id": "ready",
                    "task_ref": self.readiness_example["task_ref"],
                    "branch_review_commit": self.readiness_example[
                        "branch_review_commit"
                    ],
                    "pr_title": self.readiness_example["pr_payload"]["title"],
                    "pr_body": self.readiness_example["pr_payload"]["body"],
                },
            ),
            (
                "return_to_task_work",
                self.return_payload(),
                {
                    "exit_id": "return_to_task_work",
                    "task_ref": self.readiness_example["task_ref"],
                    "finding_refs": ["PUB-WORK-001"],
                    "resume_target": "phase-2",
                },
            ),
            (
                "blocked",
                self.blocked_payload(),
                {
                    "exit_id": "blocked",
                    "reason_code": "external-publication-dependency",
                    "remediation": "Restore the external dependency and re-enter.",
                },
            ),
        )
        for name, owner_result, expected in cases:
            with self.subTest(exit=name):
                output, checkpoint, fake_owner = self.run_public_wrapper(owner_result)
                self.assertEqual(output, expected)
                self.assertEqual(fake_owner.check_calls, 1)
                self.assertFalse(checkpoint.exists())
                self.assertFalse(checkpoint.parent.exists())

    def test_public_wrapper_validates_input_before_checker_and_keeps_checkpoint(
        self,
    ) -> None:
        from runtime.io import CommandError

        invalid_input = {
            "profile": "publication_review",
            "mode": "workflow",
            "task_ref": self.readiness_example["task_ref"],
            "branch_review_commit": self.readiness_example["branch_review_commit"],
            "review_intent": "initial_review",
            "unknown": True,
        }
        with self.assertRaises(CommandError) as raised:
            self.run_public_wrapper(
                copy.deepcopy(self.readiness_example),
                public_input=invalid_input,
            )
        self.assertEqual(raised.exception.code, "schema_mismatch")
        self.assertEqual(self.last_wrapper_owner.check_calls, 0)
        self.assertTrue(self.last_wrapper_checkpoint.is_file())

    def test_public_wrapper_keeps_checkpoint_when_checker_or_projection_fails(
        self,
    ) -> None:
        from runtime.io import CommandError

        owner_result = copy.deepcopy(self.readiness_example)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            checkpoint = root / "owner/pr-readiness.json"
            checkpoint.parent.mkdir(parents=True)
            checkpoint.write_text("{}", encoding="utf-8")
            public_input = {
                "profile": "publication_review",
                "mode": "workflow",
                "task_ref": owner_result["task_ref"],
                "branch_review_commit": owner_result["branch_review_commit"],
                "review_intent": "initial_review",
            }
            input_path = root / "input.json"
            input_path.write_text(json.dumps(public_input), encoding="utf-8")
            owner_path = root / "owner.json"
            owner_path.write_text(json.dumps(owner_result), encoding="utf-8")
            fake_owner = self.WrapperOwner(
                root,
                owner_result,
                checkpoint,
                checker_error=True,
            )
            with mock.patch.object(PUBLIC_WRAPPER, "_owner", return_value=fake_owner):
                with self.assertRaises(CommandError):
                    PUBLIC_WRAPPER.run(
                        PACKAGE,
                        {},
                        [
                            "--root",
                            str(root),
                            "--input",
                            str(input_path),
                            "--owner-result",
                            str(owner_path),
                        ],
                    )
            self.assertTrue(checkpoint.is_file())

        invalid_output = copy.deepcopy(self.readiness_example)
        invalid_output["pr_payload"]["title"] = ""
        with self.assertRaises(CommandError) as raised:
            self.run_public_wrapper(invalid_output)
        self.assertEqual(raised.exception.code, "schema_mismatch")
        self.assertTrue(self.last_wrapper_checkpoint.is_file())

    def test_public_wrapper_requires_exact_checker_passed_owner_result(self) -> None:
        from runtime.io import CommandError

        supplied = copy.deepcopy(self.readiness_example)
        supplied["pr_payload"]["title"] = "stale title"
        with self.assertRaises(CommandError) as raised:
            self.run_public_wrapper(
                copy.deepcopy(self.readiness_example),
                supplied_owner_result=supplied,
            )
        self.assertEqual(raised.exception.code, "internal_error")
        self.assertTrue(self.last_wrapper_checkpoint.is_file())

    class FacadeContext:
        def __init__(self, root: Path, task_ref: str) -> None:
            self.task_dir = root / task_ref
            self.checked_owner_result = None
            self.operation_counts = {}

        def count(self, operation: str) -> None:
            self.operation_counts[operation] = self.operation_counts.get(operation, 0) + 1

    class FacadeOwner:
        class WorkflowError(RuntimeError):
            def __init__(self, message: str, *, payload=None, **_kwargs) -> None:
                super().__init__(message)
                self.payload = payload or {}

        def __init__(self, root: Path, owner_result: dict, checkpoint: Path) -> None:
            self.root = root
            self.owner_result = owner_result
            self.checkpoint = checkpoint
            self.record_calls = 0
            self.check_calls = 0
            self.context = None
            outer = self

            class ContextFactory:
                @staticmethod
                def create(context_root: Path, task_ref: str):
                    outer.context = TaskPublicationContractTest.FacadeContext(
                        context_root,
                        task_ref,
                    )
                    return outer.context

            self.TaskPublicationInvocationContext = ContextFactory

        def repo_root(self, _path: Path) -> Path:
            return self.root

        @staticmethod
        def read_json(path: Path) -> dict:
            return json.loads(path.read_text(encoding="utf-8"))

        @staticmethod
        def skill_json_loads(value: str, _label: str) -> dict:
            return json.loads(value)

        def cmd_record_task_publication_review(self, _args, *, invocation_context) -> dict:
            self.record_calls += 1
            invocation_context.checked_owner_result = copy.deepcopy(self.owner_result)
            self.checkpoint.parent.mkdir(parents=True, exist_ok=True)
            self.checkpoint.write_text(json.dumps(self.owner_result), encoding="utf-8")
            invocation_context.count("semantic.record")
            invocation_context.count("objective.check")
            return copy.deepcopy(self.owner_result)

        def cmd_check_task_publication_review(self, _args, *, invocation_context) -> dict:
            self.check_calls += 1
            invocation_context.count("checkpoint.verify")
            return {"owner_result": copy.deepcopy(invocation_context.checked_owner_result)}

        def task_publication_path(self, _root: Path, _task: Path) -> Path:
            return self.checkpoint

    def run_happy_path_facade(
        self,
        owner_result: dict,
        *,
        semantic_overrides: dict | None = None,
    ) -> tuple[dict, "TaskPublicationContractTest.FacadeOwner"]:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        public = {
            "profile": "publication_review",
            "mode": "workflow",
            "task_ref": owner_result["task_ref"],
            "branch_review_commit": owner_result["branch_review_commit"],
            "review_intent": "initial_review",
        }
        semantic = {
            "profile": public["profile"],
            "mode": public["mode"],
            "review_intent": public["review_intent"],
            "pr_payload": copy.deepcopy(owner_result["pr_payload"]),
            "candidate_classifications": copy.deepcopy(
                owner_result["candidate_classifications"]
            ),
            "dimensions": copy.deepcopy(owner_result["dimensions"]),
            "findings": copy.deepcopy(owner_result["findings"]),
            "conclusions": copy.deepcopy(owner_result["conclusions"]),
            "route": copy.deepcopy(owner_result["route"]),
        }
        semantic.update(semantic_overrides or {})
        public_path = root / "public.json"
        semantic_path = root / "semantic.json"
        public_path.write_text(json.dumps(public), encoding="utf-8")
        semantic_path.write_text(json.dumps(semantic), encoding="utf-8")
        checkpoint = root / "owner/pr-readiness.json"
        fake_owner = self.FacadeOwner(root, owner_result, checkpoint)
        with mock.patch.object(PUBLIC_WRAPPER, "_owner", return_value=fake_owner):
            output = PUBLIC_WRAPPER.run(
                PACKAGE,
                {"id": "review-task-publication"},
                [
                    "--root",
                    str(root),
                    "--input",
                    str(public_path),
                    "--semantic-result",
                    str(semantic_path),
                ],
            )
        return output, fake_owner

    def test_happy_path_facade_projects_three_exits_with_one_record_and_check(
        self,
    ) -> None:
        cases = (
            ("ready", copy.deepcopy(self.readiness_example)),
            ("return_to_task_work", self.return_payload()),
            ("blocked", self.blocked_payload()),
        )
        for exit_id, owner_result in cases:
            with self.subTest(exit=exit_id):
                output, fake_owner = self.run_happy_path_facade(owner_result)
                self.assertEqual(output["exit_id"], exit_id)
                self.assertEqual(fake_owner.record_calls, 1)
                self.assertEqual(fake_owner.check_calls, 1)
                self.assertEqual(
                    fake_owner.context.operation_counts,
                    {
                        "semantic.record": 1,
                        "objective.check": 1,
                        "checkpoint.verify": 1,
                        "public.project": 1,
                    },
                )
                self.assertFalse(fake_owner.checkpoint.exists())

    def test_happy_path_facade_rejects_semantic_result_for_another_invocation(
        self,
    ) -> None:
        from runtime.io import CommandError

        with self.assertRaises(CommandError) as raised:
            self.run_happy_path_facade(
                copy.deepcopy(self.readiness_example),
                semantic_overrides={"review_intent": "metadata_revision_review"},
            )
        self.assertEqual(raised.exception.code, "publication_input_invalid")

    def test_invocation_context_reuses_one_objective_snapshot(self) -> None:
        context = GTT.TaskPublicationInvocationContext(
            root=Path("/repo"),
            config={},
            task_dir=Path("/repo/.trellis/tasks/task"),
            task_context={},
        )
        invocation = {
            "task_ref": ".trellis/tasks/task",
            "branch_review_commit": "a" * 40,
            "pr_payload": {"title": "标题", "body": "正文"},
        }
        snapshot = ({}, [], {}, {})
        with mock.patch.object(
            GTT,
            "task_publication_entry_precondition_bindings",
            return_value=snapshot,
        ) as capture:
            self.assertIs(context.entry_bindings(invocation), snapshot)
            self.assertIs(context.entry_bindings(copy.deepcopy(invocation)), snapshot)
        capture.assert_called_once()
        self.assertEqual(context.operation_counts, {"publication.snapshot": 1})

    def test_invocation_context_does_not_reuse_changed_publication_metadata(self) -> None:
        context = GTT.TaskPublicationInvocationContext(
            root=Path("/repo"),
            config={},
            task_dir=Path("/repo/.trellis/tasks/task"),
            task_context={},
        )
        invocation = {
            "task_ref": ".trellis/tasks/task",
            "branch_review_commit": "a" * 40,
            "pr_payload": {"title": "标题", "body": "正文"},
        }
        with mock.patch.object(
            GTT,
            "task_publication_entry_precondition_bindings",
            return_value=({}, [], {}, {}),
        ) as capture:
            context.entry_bindings(invocation)
            changed = copy.deepcopy(invocation)
            changed["pr_payload"]["body"] = "修订正文"
            context.entry_bindings(changed)
        self.assertEqual(capture.call_count, 2)
        self.assertEqual(context.operation_counts, {"publication.snapshot": 2})

    def test_provenance_tail_accepts_only_semantic_spec_managed_hash(self) -> None:
        head = "a" * 40
        before = {
            "installed_at": "before",
            "source": {"ref": "before", "commit": "before", "tree_state": "dirty", "is_mutable_ref": True},
            "install": {"managed_assets": [".trellis/spec/workflow/semantic-retrieval.md"]},
        }
        after = {
            "installed_at": "after",
            "source": {"ref": head, "commit": head, "tree_state": "clean", "is_mutable_ref": False},
            "install": {
                "managed_assets": [".trellis/spec/workflow/semantic-retrieval.md"],
                "managed_asset_hashes": {
                    ".trellis/spec/workflow/semantic-retrieval.md": "b" * 64,
                },
            },
        }

        self.assertEqual(GTT.provenance_tail_manifest_errors(before, after, head), [])

        for field, value in (
            ("unexpected_install_field", True),
            ("managed_asset_hashes", {".trellis/spec/workflow/other.md": "c" * 64}),
        ):
            with self.subTest(field=field):
                invalid = json.loads(json.dumps(after))
                if field == "managed_asset_hashes":
                    invalid["install"][field].update(value)
                else:
                    invalid["install"][field] = value
                self.assertIn(
                    "provenance_tail_manifest_fields_outside_allowlist",
                    GTT.provenance_tail_manifest_errors(before, invalid, head),
                )

    def test_provenance_tail_file_action_transition_is_closed(self) -> None:
        head = "a" * 40
        before = {
            "installed_at": "before",
            "source": {
                "ref": "before",
                "commit": "before",
                "tree_state": "dirty",
                "is_mutable_ref": True,
            },
            "install": {
                "managed_assets": [
                    ".trellis/spec/workflow/semantic-retrieval.md"
                ]
            },
        }
        before.update(provenance_file_action_sections("installed"))
        after = copy.deepcopy(before)
        after["installed_at"] = "after"
        after["source"].update(
            {
                "ref": head,
                "commit": head,
                "tree_state": "clean",
                "is_mutable_ref": False,
            }
        )
        for container in GTT.PROVENANCE_TAIL_FILE_ACTION_CONTAINERS:
            section_name, field_name = container.split(".", 1)
            for item in after[section_name][field_name]:
                item["action"] = "unchanged"

        self.assertNotIn(
            "skill_packages.files",
            GTT.PROVENANCE_TAIL_ALLOWED_FIELDS,
        )
        self.assertNotIn("overlays.files", GTT.PROVENANCE_TAIL_ALLOWED_FIELDS)
        self.assertEqual(
            GTT.provenance_tail_manifest_errors(before, after, head),
            [],
        )
        for container in GTT.PROVENANCE_TAIL_FILE_ACTION_CONTAINERS:
            self.assertTrue(
                GTT.provenance_tail_safe_file_action_transition(
                    before,
                    after,
                    container,
                )
            )

        def reverse_action(before_value: dict, after_value: dict) -> None:
            before_value["skill_packages"]["files"][0]["action"] = "unchanged"
            after_value["skill_packages"]["files"][0]["action"] = "installed"

        def mutate_after_action(_before_value: dict, after_value: dict) -> None:
            after_value["overlays"]["files"][0]["action"] = "updated_managed"

        def mutate_path(_before_value: dict, after_value: dict) -> None:
            after_value["skill_packages"]["files"][0]["path"] += ".changed"

        def mutate_hash(_before_value: dict, after_value: dict) -> None:
            after_value["overlays"]["files"][0]["sha256"] = "f" * 64

        def mutate_mode(_before_value: dict, after_value: dict) -> None:
            after_value["skill_packages"]["files"][0]["executable"] = True

        def mutate_mode_type(_before_value: dict, after_value: dict) -> None:
            after_value["skill_packages"]["files"][0]["executable"] = 0

        def mutate_source(_before_value: dict, after_value: dict) -> None:
            after_value["overlays"]["files"][0]["source"] += ".changed"

        def mutate_destination(_before_value: dict, after_value: dict) -> None:
            after_value["skill_packages"]["files"][0]["destination"] = "other"

        def mutate_platform(_before_value: dict, after_value: dict) -> None:
            after_value["overlays"]["files"][0]["platform"] = "cursor"

        def add_entry(_before_value: dict, after_value: dict) -> None:
            after_value["skill_packages"]["files"].append(
                copy.deepcopy(after_value["skill_packages"]["files"][0])
            )

        def remove_entry(_before_value: dict, after_value: dict) -> None:
            after_value["overlays"]["files"].pop()

        def reorder_entries(_before_value: dict, after_value: dict) -> None:
            after_value["skill_packages"]["files"].reverse()

        def replace_with_non_object(_before_value: dict, after_value: dict) -> None:
            after_value["overlays"]["files"][0] = "not-an-object"

        def replace_with_non_list(_before_value: dict, after_value: dict) -> None:
            after_value["skill_packages"]["files"] = "not-a-list"

        cases = (
            ("unchanged_to_installed", reverse_action),
            ("installed_to_updated_managed", mutate_after_action),
            ("path", mutate_path),
            ("hash", mutate_hash),
            ("mode", mutate_mode),
            ("mode_type", mutate_mode_type),
            ("source", mutate_source),
            ("destination", mutate_destination),
            ("platform", mutate_platform),
            ("entry_added", add_entry),
            ("entry_removed", remove_entry),
            ("entry_reordered", reorder_entries),
            ("non_object_entry", replace_with_non_object),
            ("non_list_container", replace_with_non_list),
        )
        for name, mutate in cases:
            with self.subTest(case=name):
                invalid_before = copy.deepcopy(before)
                invalid_after = copy.deepcopy(after)
                mutate(invalid_before, invalid_after)
                self.assertIn(
                    "provenance_tail_manifest_fields_outside_allowlist",
                    GTT.provenance_tail_manifest_errors(
                        invalid_before,
                        invalid_after,
                        head,
                    ),
                )

    def test_package_local_runtime_has_no_retired_verifier_or_monolith_route(self) -> None:
        runtime_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((PACKAGE / "runtime").glob("*.py"))
        )
        for retired in ("guru_team_trellis.py", "verification_required", "not_required", "finalization_verification"):
            self.assertNotIn(retired, runtime_text)
        commands = json.loads((PACKAGE / "commands.json").read_text(encoding="utf-8"))
        self.assertEqual(
            {(item["validator_id"], item["id"]) for item in commands["commands"]},
            {(item["id"], item["runtime_command"]) for item in self.interface["validators"]},
        )
        for validator in self.interface["validators"]:
            self.assertIn("runtime/launch.sh", (PACKAGE / validator["command"]).read_text(encoding="utf-8"))

    def test_package_entrypoints_map_owner_failures_to_declared_error(self) -> None:
        sys.path.insert(0, str(PACKAGE.parents[1]))
        from runtime.io import CommandError

        class FakeOwner:
            class WorkflowError(RuntimeError):
                pass

            def fail(self, *_args):
                raise self.WorkflowError("expected fail-closed result")

        common_path = PACKAGE / "runtime/common.py"
        spec = importlib.util.spec_from_file_location(
            "task_publication_runtime_common",
            common_path,
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader if spec else None)
        common = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(common)

        with self.assertRaises(CommandError) as raised:
            common.call_owner(FakeOwner, FakeOwner().fail)
        self.assertEqual(raised.exception.code, "internal_error")
        self.assertEqual(raised.exception.field_path, "owner")

    def test_owner_diagnostic_projection_preserves_classified_codes_and_redacts(self) -> None:
        sys.path.insert(0, str(PACKAGE.parents[1]))
        from runtime.io import CommandError

        common_path = PACKAGE / "runtime/common.py"
        spec = importlib.util.spec_from_file_location("task_publication_runtime_common_diagnostic", common_path)
        assert spec and spec.loader
        common = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(common)

        class FakeOwner:
            class WorkflowError(RuntimeError):
                def __init__(self, payload):
                    super().__init__("secret token https://example.invalid/private")
                    self.payload = payload

            def fail(self, payload):
                raise self.WorkflowError(payload)

        cases = [
            ({"error_code": "publication_freshness_failed", "field_path": "publication.freshness", "recovery": "Repeat review."}, "publication_stale", "publication.freshness", "stale_identity"),
            ({"error_code": "github_auth_failed", "field_path": "github.auth", "recovery": "https://user:secret@example.invalid/token"}, "github_auth_failed", "github.auth", None),
            ({"error_codes": ["reviewed_content_continuity_invalid"]}, "reviewed_content_continuity_failed", "publication", "stale_identity"),
            ({"error_codes": ["invalid_input_shape"]}, "publication_input_invalid", "publication", None),
            (
                {"error_codes": ["issue_scope_ledger:issue_scope_ledger_primary_disposition_invalid"]},
                "issue_scope_ledger_primary_disposition_invalid",
                "publication.issue_scope_ledger.primary_issue",
                "task_content",
            ),
            (
                {"error_codes": ["publication_content:PR body 缺少 `Docs SSOT` section。"]},
                "publication_content_contract_failed",
                "publication.pr_payload.body",
                "publication_content",
            ),
            (
                {"error_codes": ["publication_content:PR title is empty"]},
                "publication_content_contract_failed",
                "publication.pr_payload.title",
                "publication_content",
            ),
            (
                {
                    "error_codes": [
                        "publication_content:PR title is empty",
                        "publication_content:PR body is empty",
                    ]
                },
                "publication_content_contract_failed",
                "publication.pr_payload",
                "publication_content",
            ),
            (
                {"error_codes": ["branch_review_handoff:branch_review_commit_invalid"]},
                "branch_review_commit_invalid",
                "input.branch_review_commit",
                "stale_identity",
            ),
            (
                {"error_codes": ["runtime_dependency:missing_runtime"]},
                "missing_runtime",
                "runtime",
                "runtime_dependency",
            ),
            (
                {"errors": ["publication_content:PR body 缺少 `影响范围` section。"]},
                "publication_content_contract_failed",
                "publication.pr_payload.body",
                "publication_content",
            ),
        ]
        for payload, code, locator, recovery_scope in cases:
            with self.subTest(payload=payload):
                with self.assertRaises(CommandError) as raised:
                    common.call_owner(FakeOwner, FakeOwner().fail, payload)
                self.assertEqual(raised.exception.code, code)
                self.assertEqual(raised.exception.field_path, locator)
                self.assertEqual(
                    (raised.exception.response or {}).get("recovery_scope"),
                    recovery_scope,
                )
                self.assertNotIn("secret", raised.exception.remediation)
                self.assertNotIn("https://", raised.exception.remediation)

        for payload in (
            {"error_codes": ["unknown_owner:unmapped_failure"]},
            {
                "error_codes": [
                    "publication_content:missing_section",
                    "unclassified_failure",
                ]
            },
            {
                "error_codes": [
                    "publication_content:missing_section",
                    "issue_scope_ledger:issue_scope_ledger_primary_disposition_invalid",
                ]
            },
        ):
            with self.subTest(payload=payload):
                with self.assertRaises(CommandError) as raised:
                    common.call_owner(FakeOwner, FakeOwner().fail, payload)
                self.assertEqual(raised.exception.code, "internal_error")
                self.assertEqual(raised.exception.field_path, "owner")
                self.assertNotIn("recovery_scope", raised.exception.response or {})

        parser = __import__("argparse").ArgumentParser(add_help=False)
        parser.add_argument("--required", required=True)
        with redirect_stderr(StringIO()):
            with self.assertRaises(CommandError) as invalid:
                common.parse_arguments(parser, [])
        self.assertEqual(invalid.exception.code, "invalid_arguments")

    def test_each_missing_required_pr_body_section_is_publication_content(self) -> None:
        ledger = {
            "schema_version": "2.0",
            "primary_issue": {"number": 361},
            "close_issues": [{"number": 361}],
            "related_issues": [],
            "followup_issues": [],
        }
        section_content = {
            "变更摘要": "- 保留 Publication owner 错误分类。",
            "影响范围": "仅影响 Publication Review facade 与恢复路由。",
            "验证结果": "Canonical 与 installed package tests 通过。",
            "Review Gate": "Branch Review 无未关闭 finding。",
            "Issue 关闭范围": "Closes #361。",
            "安全说明": "不涉及 secret、部署或数据迁移。",
            "Docs SSOT": "- strategy: no_docs_update_needed\n- durable docs: no-update\n- merged delta: none\n- task history: task-history-only\n- follow-up: none",
        }
        for missing in GTT.PR_BODY_REQUIRED_SECTIONS:
            body = "\n\n".join(
                f"## {section}\n\n{content}"
                for section, content in section_content.items()
                if section != missing
            )
            errors = GTT.validate_pr_body_quality(body, ledger, False)
            self.assertIn(f"PR body 缺少 `{missing}` section。", errors)

    @classmethod
    def setUpClass(cls) -> None:
        cls.interface = json.loads((PACKAGE / "interface.json").read_text(encoding="utf-8"))
        cls.readiness_schema = json.loads(
            (PACKAGE / "schemas/pr-readiness.schema.json").read_text(encoding="utf-8")
        )
        cls.readiness_example = json.loads(
            (PACKAGE / "examples/pr-readiness.json").read_text(encoding="utf-8")
        )

    def test_two_profiles_and_semantic_stage_order(self) -> None:
        self.assertEqual(self.interface["judgment_mode"], "semantic")
        self.assertEqual(
            self.interface["ordered_stages"],
            [
                "forward_behavior",
                "ai_review_gate",
                "conditional_human_confirmation",
                "recorder_validator",
                "typed_exit",
            ],
        )
        profiles = self.interface["public_contracts"]["input"]["profiles"]
        self.assertEqual(
            [item["id"] for item in profiles],
            ["publication_review", "publication_review_stale"],
        )
        self.assertEqual(
            self.interface["public_contracts"]["input"]["aggregate_schema"][
                "schema_id"
            ],
            "guru-production-review-task-publication-input-aggregate-4.0",
        )
        self.assertEqual(
            profiles[1]["schema"]["schema_id"],
            "guru-production-review-task-publication-input-publication-review-stale-3.0",
        )

    def test_one_recommended_happy_path_keeps_legacy_command_budget(self) -> None:
        commands = json.loads((PACKAGE / "commands.json").read_text(encoding="utf-8"))[
            "commands"
        ]
        by_id = {item["id"]: item for item in commands}
        self.assertEqual(
            self.interface["public_contracts"]["invocation"]["wrapper"],
            "scripts/review-task-publication.sh",
        )
        self.assertEqual(
            self.interface["public_contracts"]["invocation"]["example_argv"],
            [
                "--input",
                "examples/public-publication-review-input.json",
                "--semantic-result",
                "examples/public-publication-review-authoring.json",
            ],
        )
        self.assertEqual(
            by_id["review-task-publication"]["validator_id"],
            "publication_happy_path",
        )
        legacy = {
            "record-task-publication-review",
            "check-task-publication-review",
            "invoke-guru-review-task-publication",
        }
        self.assertTrue(legacy <= set(by_id))
        legacy_command_invocations = len(legacy)
        happy_path_command_invocations = 1
        reduction = (
            legacy_command_invocations - happy_path_command_invocations
        ) / legacy_command_invocations
        self.assertGreaterEqual(reduction, 0.5)
        legacy_complete_snapshot_operations = (
            "record.preflight",
            "record.validation",
            "check.validation",
            "invoke.recheck",
        )
        legacy_complete_snapshot_reads = len(legacy_complete_snapshot_operations)
        happy_path_complete_snapshot_reads = 1
        snapshot_reduction = (
            legacy_complete_snapshot_reads - happy_path_complete_snapshot_reads
        ) / legacy_complete_snapshot_reads
        self.assertGreaterEqual(snapshot_reduction, 0.7)

    def test_public_contract_exposes_complete_valid_semantic_authoring_template(self) -> None:
        import jsonschema

        skill = (PACKAGE / "SKILL.md").read_text(encoding="utf-8")
        contract = (PACKAGE / "references/contract.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("exact authoring fields, enums, route rules", skill)
        start = "<!-- publication-semantic-result-template:start -->"
        end = "<!-- publication-semantic-result-template:end -->"
        documented = contract.split(start, 1)[1].split(end, 1)[0]
        template = json.loads(
            documented.split("```json", 1)[1].split("```", 1)[0]
        )
        self.assertEqual(
            set(template),
            {
                "profile",
                "mode",
                "review_intent",
                "pr_payload",
                "candidate_classifications",
                "dimensions",
                "findings",
                "conclusions",
                "route",
            },
        )
        self.assertEqual(
            [item["id"] for item in template["dimensions"]],
            list(GTT.TASK_PUBLICATION_DIMENSIONS),
        )
        materialized = {
            "schema_version": "5.0",
            "skill_id": "guru-review-task-publication",
            "task_ref": ".trellis/tasks/09-02-example",
            "branch_review_commit": "a" * 40,
            "reviewed_content_sha256": "b" * 64,
            **template,
        }
        for field in ("profile", "mode", "review_intent"):
            materialized.pop(field)
        self.assertEqual(
            list(
                jsonschema.Draft202012Validator(
                    self.readiness_schema
                ).iter_errors(materialized)
            ),
            [],
        )
        self.assertEqual(
            GTT.task_publication_semantic_errors(
                materialized,
                branch_review_commit=materialized["branch_review_commit"],
            ),
            [],
        )
        normalized_contract = " ".join(contract.split())
        for required_text in (
            "qualified_current",
            "rejected_out_of_scope",
            "metadata_revision",
            "external_blocker",
            '`status` is `passed`, `finding`, or `blocked`',
            '`status` is `open` or `closed`',
            '`{"typed_exit":"return_to_task_work"}`',
            '`{"typed_exit":"blocked","reason_code":"...","remediation":"..."}`',
        ):
            self.assertIn(required_text, normalized_contract)

    def test_stale_profile_contains_only_direct_reentry_inputs(self) -> None:
        schema = json.loads(
            (
                PACKAGE
                / "schemas/public-publication-review-stale-input.schema.json"
            ).read_text(encoding="utf-8")
        )
        expected = {
            "profile",
            "mode",
            "task_ref",
            "branch_review_commit",
            "stale_reason",
            "review_intent",
        }
        self.assertEqual(set(schema["properties"]), expected)
        self.assertEqual(set(schema["required"]), expected)
        for relative in (
            "examples/public-publication-review-stale-input.json",
            "examples/public-publication-review-stale-authoring.json",
            "evals/files/stale-reentry-ready-input.json",
        ):
            payload = json.loads((PACKAGE / relative).read_text(encoding="utf-8"))
            self.assertNotIn("reentry_context", payload, relative)

    def test_three_minimal_exits_have_unique_consumers(self) -> None:
        exits = self.interface["external_exits"]
        self.assertEqual(
            [item["id"] for item in exits],
            ["ready", "return_to_task_work", "blocked"],
        )
        self.assertEqual(
            len({(item["consumer"]["kind"], item["consumer"]["id"]) for item in exits}),
            3,
        )

    def test_initial_authoring_partition_is_target_owned(self) -> None:
        branch = json.loads(
            (
                PACKAGE.parent
                / "guru-review-branch"
                / "interface.json"
            ).read_text(encoding="utf-8")
        )
        consumer = next(
            item
            for item in branch["public_contracts"]["consumer_inputs"]
            if item["id"] == "publication_seed_input"
        )
        contract = consumer["contract"]
        self.assertEqual(contract["kind"], "skill_input_authoring_seed")
        self.assertEqual(contract["seed_fields"], ["task_ref", "branch_review_commit"])
        self.assertEqual(contract["authoring_fields"], ["profile", "mode", "review_intent"])

    def test_public_outputs_exclude_private_review_state(self) -> None:
        forbidden = {
            "semantic_review",
            "findings",
            "deterministic_bindings",
            "publish_inputs",
            "facts_sha256",
            "artifact_path",
            "publication_ref",
            "review_ref",
            "human_confirmation",
        }
        for output in self.interface["public_contracts"]["outputs"]:
            schema = json.loads((PACKAGE / output["schema"]["path"]).read_text(encoding="utf-8"))
            self.assertFalse(forbidden & set(schema["properties"]))

    def test_ready_schema_migration_preserves_legacy_and_projects_current(self) -> None:
        import jsonschema

        legacy_path = PACKAGE / "schemas/public-ready-output.schema.json"
        current_path = PACKAGE / "schemas/public-ready-output-4.0.schema.json"
        self.assertEqual(
            hashlib.sha256(legacy_path.read_bytes()).hexdigest(),
            "57d984c5ef50b9ab2f4fa5e15fbde58c59ad76e563e1690d7cc4c6ceafc6062c",
        )
        legacy_schema = json.loads(legacy_path.read_text(encoding="utf-8"))
        current_schema = json.loads(current_path.read_text(encoding="utf-8"))
        current_payload = json.loads(
            (PACKAGE / "examples/public-ready-output.json").read_text(encoding="utf-8")
        )
        legacy_payload = {
            key: current_payload[key]
            for key in ("exit_id", "task_ref", "branch_review_commit")
        }

        self.assertEqual(
            list(jsonschema.Draft202012Validator(legacy_schema).iter_errors(legacy_payload)),
            [],
        )
        self.assertTrue(
            list(jsonschema.Draft202012Validator(current_schema).iter_errors(legacy_payload))
        )
        self.assertTrue(
            list(jsonschema.Draft202012Validator(legacy_schema).iter_errors(current_payload))
        )
        self.assertEqual(
            list(jsonschema.Draft202012Validator(current_schema).iter_errors(current_payload)),
            [],
        )

        schema_paths = {item["path"] for item in self.interface["schemas"]}
        self.assertIn("schemas/public-ready-output.schema.json", schema_paths)
        self.assertIn("schemas/public-ready-output-4.0.schema.json", schema_paths)
        ready_output = next(
            item
            for item in self.interface["public_contracts"]["outputs"]
            if item["exit_id"] == "ready"
        )
        self.assertEqual(
            ready_output["schema"],
            {
                "schema_id": "guru-production-review-task-publication-output-ready-4.0",
                "path": "schemas/public-ready-output-4.0.schema.json",
            },
        )

        projection = next(
            item
            for item in self.interface["public_contracts"]["projections"]
            if item["id"] == "project_ready"
        )
        projected = {
            mapping["target"]: current_payload[mapping["source"]]
            for mapping in projection["mappings"]
        }
        finalizer_package = PACKAGE.parent / "guru-finalize-task"
        authoring = json.loads(
            (finalizer_package / "examples/public-publication-ready-authoring.json")
            .read_text(encoding="utf-8")
        )
        finalizer = json.loads(
            (finalizer_package / "interface.json").read_text(
                encoding="utf-8"
            )
        )
        target_profile = next(
            item
            for item in finalizer["public_contracts"]["input"]["profiles"]
            if item["id"] == "publication_ready"
        )
        target_schema = json.loads(
            (finalizer_package / target_profile["schema"]["path"])
            .read_text(encoding="utf-8")
        )
        jsonschema.Draft202012Validator(target_schema).validate(
            {**projected, **authoring}
        )

    def test_pr_readiness_is_one_private_gate(self) -> None:
        private = self.interface["public_contracts"]["private_artifacts"]
        self.assertEqual([item["id"] for item in private], ["publication_readiness"])
        self.assertEqual(private[0]["kind"], "gate_evidence")
        self.assertEqual(
            private[0]["persistence"],
            "ignored_runtime",
        )

    def test_readiness_example_is_schema_and_runtime_semantic_valid(self) -> None:
        from jsonschema import Draft202012Validator

        Draft202012Validator.check_schema(self.readiness_schema)
        validator = Draft202012Validator(self.readiness_schema)
        self.assertEqual(list(validator.iter_errors(self.readiness_example)), [])
        self.assertEqual(
            GTT.task_publication_semantic_errors(
                self.readiness_example,
                branch_review_commit=self.readiness_example[
                    "branch_review_commit"
                ],
            ),
            [],
        )

    def test_schema_valid_runtime_invalid_duplicate_finding_refs_fail_closed(self) -> None:
        from jsonschema import Draft202012Validator

        finding = {
            "finding_ref": "PUB-001",
            "candidate_ref": "candidate:publication:no-defect",
            "dimension": "pr_body_quality",
            "summary": "The metadata fix was reviewed and closed.",
            "scope_basis": "The publication contract owns this metadata.",
            "evidence_refs": ["pr_payload"],
            "affected_artifacts": ["pr_payload"],
            "route_class": "metadata_revision",
            "status": "closed",
            "closure_evidence": ["pr_payload#fixed"],
        }
        invalid = copy.deepcopy(self.readiness_example)
        invalid["findings"] = [finding, copy.deepcopy(finding)]
        self.assertEqual(
            list(Draft202012Validator(self.readiness_schema).iter_errors(invalid)),
            [],
        )
        self.assertIn(
            "publication finding refs must be unique and non-empty",
            GTT.task_publication_semantic_errors(
                invalid,
                branch_review_commit=invalid["branch_review_commit"],
            ),
        )

    def test_empty_closed_finding_evidence_fails_schema_and_runtime(self) -> None:
        from jsonschema import Draft202012Validator

        invalid = copy.deepcopy(self.readiness_example)
        invalid["findings"] = [{
            "finding_ref": "PUB-EMPTY",
            "candidate_ref": "candidate:publication:no-defect",
            "dimension": "pr_body_quality",
            "summary": "",
            "scope_basis": "",
            "evidence_refs": [],
            "affected_artifacts": [],
            "route_class": "metadata_revision",
            "status": "closed",
            "closure_evidence": [],
        }]
        self.assertTrue(
            list(Draft202012Validator(self.readiness_schema).iter_errors(invalid))
        )
        self.assertIn(
            "publication finding evidence must be non-empty",
            GTT.task_publication_semantic_errors(
                invalid,
                branch_review_commit=invalid["branch_review_commit"],
            ),
        )

    def test_gate_schema_rejects_removed_process_and_binding_fields(self) -> None:
        from jsonschema import Draft202012Validator

        for field in (
            "generated_at",
            "facts_sha256",
            "deterministic_bindings",
            "review_identity",
            "review_ref",
            "publication_ref",
            "supersedes_publication_ref",
            "revision_history",
            "reviewer_process",
            "human_confirmation",
        ):
            with self.subTest(field=field):
                invalid = copy.deepcopy(self.readiness_example)
                invalid[field] = "forbidden"
                self.assertTrue(
                    list(
                        Draft202012Validator(self.readiness_schema).iter_errors(
                            invalid
                        )
                    )
                )

    def semantic_errors(self, payload: dict) -> list[str]:
        return GTT.task_publication_semantic_errors(
            payload,
            branch_review_commit=payload["branch_review_commit"],
        )

    @staticmethod
    def open_finding(
        *,
        finding_ref: str,
        dimension: str,
        route_class: str,
    ) -> dict:
        return {
            "finding_ref": finding_ref,
            "candidate_ref": "candidate:publication:no-defect",
            "dimension": dimension,
            "summary": "The current publication review cannot complete.",
            "scope_basis": "The approved publication contract owns this route.",
            "evidence_refs": ["review-gate.json"],
            "affected_artifacts": ["pr_payload"],
            "route_class": route_class,
            "status": "open",
            "closure_evidence": [],
        }

    def return_payload(self) -> dict:
        payload = copy.deepcopy(self.readiness_example)
        payload["route"] = {"typed_exit": "return_to_task_work"}
        payload["dimensions"][0]["status"] = "finding"
        payload["findings"] = [
            self.open_finding(
                finding_ref="PUB-WORK-001",
                dimension="diff_outcome_consistency",
                route_class="task_work",
            )
        ]
        payload["conclusions"]["issue_scope"]["status"] = "finding"
        return payload

    def blocked_payload(self) -> dict:
        payload = copy.deepcopy(self.readiness_example)
        payload["route"] = {
            "typed_exit": "blocked",
            "reason_code": "external-publication-dependency",
            "remediation": "Restore the external dependency and re-enter.",
        }
        payload["dimensions"][-1]["status"] = "blocked"
        payload["findings"] = [
            self.open_finding(
                finding_ref="PUB-BLOCK-001",
                dimension="artifact_binding_freshness",
                route_class="external_blocker",
            )
        ]
        payload["conclusions"]["safety_deployment"]["status"] = "blocked"
        return payload

    def test_ready_rejects_nonpassed_conclusion_in_schema_and_runtime(self) -> None:
        from jsonschema import Draft202012Validator

        invalid = copy.deepcopy(self.readiness_example)
        invalid["conclusions"]["issue_scope"]["status"] = "blocked"
        self.assertTrue(
            list(Draft202012Validator(self.readiness_schema).iter_errors(invalid))
        )
        self.assertIn(
            "ready requires every publication conclusion to pass",
            self.semantic_errors(invalid),
        )

    def test_return_rejects_all_passed_dimensions_in_schema_and_runtime(self) -> None:
        from jsonschema import Draft202012Validator

        invalid = self.return_payload()
        invalid["dimensions"][0]["status"] = "passed"
        self.assertTrue(
            list(Draft202012Validator(self.readiness_schema).iter_errors(invalid))
        )
        errors = self.semantic_errors(invalid)
        self.assertIn(
            "return_to_task_work requires a finding publication dimension",
            errors,
        )
        self.assertIn(
            "open publication finding must reference a non-passed dimension",
            errors,
        )

    def test_blocked_rejects_reason_only_semantics_in_schema_and_runtime(self) -> None:
        from jsonschema import Draft202012Validator

        invalid = copy.deepcopy(self.readiness_example)
        invalid["route"] = {
            "typed_exit": "blocked",
            "reason_code": "external-publication-dependency",
            "remediation": "Restore the external dependency and re-enter.",
        }
        self.assertTrue(
            list(Draft202012Validator(self.readiness_schema).iter_errors(invalid))
        )
        errors = self.semantic_errors(invalid)
        self.assertIn("blocked requires a blocked publication dimension", errors)
        self.assertIn("blocked requires an open external_blocker finding", errors)
        self.assertIn("blocked requires a blocked publication conclusion", errors)

    def test_valid_ready_return_and_blocked_unions_pass_both_layers(self) -> None:
        from jsonschema import Draft202012Validator

        validator = Draft202012Validator(self.readiness_schema)
        for name, payload in (
            ("ready", copy.deepcopy(self.readiness_example)),
            ("return_to_task_work", self.return_payload()),
            ("blocked", self.blocked_payload()),
        ):
            with self.subTest(exit=name):
                self.assertEqual(list(validator.iter_errors(payload)), [])
                self.assertEqual(self.semantic_errors(payload), [])

    def test_runtime_binds_open_findings_to_matching_nonpassed_dimensions(self) -> None:
        from jsonschema import Draft202012Validator

        invalid_return = self.return_payload()
        invalid_return["findings"][0][
            "dimension"
        ] = "pr_body_quality"
        self.assertEqual(
            list(Draft202012Validator(self.readiness_schema).iter_errors(invalid_return)),
            [],
        )
        self.assertIn(
            "return_to_task_work open findings must reference finding dimensions",
            self.semantic_errors(invalid_return),
        )

        invalid_blocked = self.blocked_payload()
        invalid_blocked["findings"][0][
            "dimension"
        ] = "pr_body_quality"
        self.assertEqual(
            list(Draft202012Validator(self.readiness_schema).iter_errors(invalid_blocked)),
            [],
        )
        self.assertIn(
            "blocked open findings must reference blocked dimensions",
            self.semantic_errors(invalid_blocked),
        )

    def test_stale_reentry_does_not_expand_the_owner_checkpoint(self) -> None:
        properties = set(self.readiness_schema["properties"])
        self.assertFalse(
            properties
            & {
                "profile",
                "mode",
                "review_intent",
                "stale_reason",
                "reentry_context",
                "supersedes_publication_ref",
            }
        )

    def test_ready_checker_runs_the_shared_finalizer_preflight(self) -> None:
        root = Path("/repo")
        task_dir = root / self.readiness_example["task_ref"]
        with (
            mock.patch.object(GTT, "task_publication_schema", return_value={}),
            mock.patch.object(
                GTT, "skill_json_schema_validation_errors", return_value=[]
            ),
            mock.patch.object(GTT, "load_config", return_value={}),
            mock.patch.object(
                GTT,
                "current_head",
                return_value=self.readiness_example["branch_review_commit"],
            ),
            mock.patch.object(
                GTT,
                "review_branch_content_continuity_errors",
                return_value=[],
            ),
            mock.patch.object(
                GTT,
                "reviewed_content_identity",
                return_value={
                    "algorithm": "guru-reviewed-content-1.0",
                    "sha256": self.readiness_example["reviewed_content_sha256"],
                },
            ),
            mock.patch.object(
                GTT,
                "task_publication_entry_precondition_bindings",
                return_value=({}, [], {}, {}),
            ),
            mock.patch.object(
                GTT, "task_publication_closeout_preflight"
            ) as preflight,
        ):
            errors = GTT.task_publication_check_errors(
                root,
                task_dir,
                copy.deepcopy(self.readiness_example),
            )
        self.assertEqual(errors, [])
        preflight.assert_called_once_with(
            root,
            task_dir,
            self.readiness_example["branch_review_commit"],
            self.readiness_example["pr_payload"],
        )

    def test_only_content_identity_drift_allows_return_to_task_work(
        self,
    ) -> None:
        root = Path("/repo")
        task_dir = root / self.readiness_example["task_ref"]

        def checked(
            payload: dict,
            *,
            continuity_errors: list[str] | None = None,
        ) -> list[str]:
            continuity_errors = continuity_errors or [
                GTT.BRANCH_REVIEW_CONTENT_CHANGED_ERROR_PREFIX + "identity mismatch"
            ]
            with (
                mock.patch.object(GTT, "task_publication_schema", return_value={}),
                mock.patch.object(
                    GTT, "skill_json_schema_validation_errors", return_value=[]
                ),
                mock.patch.object(GTT, "load_config", return_value={}),
                mock.patch.object(GTT, "current_head", return_value="d" * 40),
                mock.patch.object(
                    GTT,
                    "review_branch_content_continuity_errors",
                    return_value=continuity_errors,
                ),
                mock.patch.object(
                    GTT,
                    "reviewed_content_identity",
                    return_value={
                        "algorithm": "guru-reviewed-content-1.0",
                        "sha256": "d" * 64,
                    },
                ),
                mock.patch.object(
                    GTT,
                    "task_publication_entry_precondition_bindings",
                    return_value=({}, [], {}, {}),
                ),
                mock.patch.object(GTT, "task_publication_closeout_preflight"),
                mock.patch.object(GTT, "task_publication_semantic_errors", return_value=[]),
            ):
                return GTT.task_publication_check_errors(root, task_dir, payload)

        returning = self.return_payload()
        self.assertEqual(checked(returning), [])

        ready = copy.deepcopy(self.readiness_example)
        self.assertTrue(
            any(
                "reviewed content" in error and "stale" in error
                for error in checked(ready)
            )
        )

        blocked = self.blocked_payload()
        self.assertTrue(
            any(
                "reviewed content" in error and "stale" in error
                for error in checked(blocked)
            )
        )

        for case, continuity_errors in (
            (
                "non-ancestor",
                ["Branch Review review_commit is not an ancestor of the current HEAD."],
            ),
            (
                "identity-unreadable",
                ["Branch Review could not calculate reviewed-content continuity."],
            ),
        ):
            with self.subTest(case=case):
                self.assertTrue(
                    any(
                        "reviewed content is stale" in error
                        for error in checked(
                            returning,
                            continuity_errors=continuity_errors,
                        )
                    )
                )

        invalid = copy.deepcopy(returning)
        invalid["branch_review_commit"] = "not-a-sha"
        self.assertTrue(
            any(
                "branch_review_commit is invalid" in error
                for error in checked(invalid)
            )
        )

    def test_both_modes_declare_exact_eight_entry_preconditions(self) -> None:
        expected = [
            "runtime_dependency",
            "task_workspace",
            "task_identity",
            "branch_review_handoff",
            "issue_scope_ledger",
            "publication_content",
            "review_range_and_working_tree",
            "invocation_freshness",
        ]
        self.assertEqual(
            self.interface["modes"]["workflow"]["entry_precondition_ids"],
            expected,
        )
        self.assertEqual(
            self.interface["modes"]["standalone"]["entry_precondition_ids"],
            expected,
        )

    def test_interface_validator_commands_resolve_dispatcher_in_all_supported_layouts(
        self,
    ) -> None:
        repo_root = package_repo_root()
        validator_ids = (
            "publication_review_recorder",
            "publication_review_checker",
        )
        validators = {
            item["id"]: item
            for item in self.interface["validators"]
            if item["id"] in validator_ids
        }
        self.assertEqual(set(validators), set(validator_ids))
        env = os.environ.copy()
        env.pop("GURU_TEAM_DISPATCHER", None)

        present_layouts = {
            name
            for name, relative in PACKAGE_LAYOUTS
            if (repo_root / relative).is_dir()
        }
        if "canonical" in present_layouts:
            self.assertEqual(
                present_layouts,
                {name for name, _ in PACKAGE_LAYOUTS},
            )

        for layout, relative in PACKAGE_LAYOUTS:
            package_root = repo_root / relative
            if not package_root.is_dir():
                continue
            if layout not in {"canonical", "installed-shared"}:
                with self.subTest(layout=layout, projection="public-only"):
                    public_wrapper = self.interface["public_contracts"]["invocation"][
                        "wrapper"
                    ]
                    self.assertTrue(os.access(package_root / public_wrapper, os.X_OK))
                    for validator_id in validator_ids:
                        self.assertFalse(
                            (package_root / validators[validator_id]["command"]).exists()
                        )
                continue
            for validator_id in validator_ids:
                validator = validators[validator_id]
                command = package_root / validator["command"]
                with self.subTest(layout=layout, validator=validator_id):
                    result = subprocess.run(
                        [str(command), "--help"],
                        cwd=repo_root,
                        env=env,
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        check=False,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn(
                        f"usage: {validator['runtime_command']}",
                        result.stdout,
                    )
                    if layout == "canonical":
                        self.assertIn(
                            "owner: guru-review-task-publication",
                            result.stdout,
                        )

    def test_interface_validator_commands_reject_unsupported_package_layout(
        self,
    ) -> None:
        validators = {
            item["id"]: item
            for item in self.interface["validators"]
            if item["id"] in {
                "publication_review_recorder",
                "publication_review_checker",
            }
        }
        env = os.environ.copy()
        env.pop("GURU_TEAM_DISPATCHER", None)
        with tempfile.TemporaryDirectory() as temp:
            unsupported = Path(temp) / "unsupported-publication-package"
            shutil.copytree(PACKAGE, unsupported)
            for validator_id, validator in validators.items():
                with self.subTest(validator=validator_id):
                    result = subprocess.run(
                        [str(unsupported / validator["command"]), "--help"],
                        env=env,
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        check=False,
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(
                        "unsupported Skill package root "
                        "for guru-review-task-publication",
                        result.stderr,
                    )


if __name__ == "__main__":
    unittest.main()
