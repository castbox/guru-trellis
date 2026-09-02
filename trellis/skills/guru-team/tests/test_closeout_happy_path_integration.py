from __future__ import annotations

import json
import importlib.util
import os
import re
import subprocess
import sys
import tempfile
import unittest
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from unittest import mock


REPO = Path(__file__).resolve().parents[4]
SKILLS = REPO / "trellis/skills/guru-team"
PACKAGES = SKILLS / "packages"
FIXTURE = Path(__file__).parent / "fixtures/closeout-118-sanitized.json"
WORKFLOW = REPO / "trellis/workflows/guru-team/workflow.md"

HAPPY_PATHS = {
    "guru-create-task-commit": {
        "commands": [
            "prepare-task-commit",
            "invoke-guru-create-task-commit-happy-path-v1",
        ],
        "legacy": [
            "prepare-task-commit",
            "check-commit-messages",
            "create-task-commit",
            "invoke-guru-create-task-commit",
        ],
        "wrapper": "scripts/invoke-happy-path-v1.sh",
        "public_invocation_switch": False,
    },
    "guru-review-task-publication": {
        "commands": ["review-task-publication"],
        "legacy": [
            "record-task-publication-review",
            "check-task-publication-review",
            "invoke-guru-review-task-publication",
        ],
        "wrapper": "scripts/review-task-publication.sh",
        "public_invocation_switch": True,
    },
    "guru-finalize-task": {
        "commands": ["finalize-task-happy-path"],
        "legacy": [
            "preview-finalization",
            "record-finalization-gate",
            "check-finalization-gate",
            "execute-finalization-transition",
            "invoke-guru-finalize-task",
        ],
        "wrapper": "scripts/finalize-task-happy-path.sh",
        "public_invocation_switch": True,
    },
    "guru-merge-task-pr": {
        "commands": ["complete-task-pr-merge"],
        "legacy": [
            "record-task-pr-merge",
            "check-task-pr-merge",
            "execute-task-pr-merge",
            "invoke-task-pr-merge",
        ],
        "wrapper": "scripts/complete-task-pr-merge.sh",
        "public_invocation_switch": True,
    },
}


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{path} must contain one JSON object")
    return value


@dataclass
class ExecutedRoute:
    output: dict[str, Any]
    commands: list[str]
    full_reads: int
    mutations: list[str]
    lifecycle: list[str]
    boundary: tuple[str, ...]
    recovery_output: dict[str, Any] | None = None
    post_exit_operations: int = 0


@contextmanager
def package_modules(package: Path):
    search_paths = [str(SKILLS), str(package / "runtime")]
    previous_path = list(sys.path)
    shadowed = {
        name: sys.modules.pop(name, None)
        for name in ("common", "execute", "reviewed_content")
    }
    sys.path[:0] = search_paths
    try:
        yield
    finally:
        sys.path[:] = previous_path
        for name in shadowed:
            sys.modules.pop(name, None)
        for name, module in shadowed.items():
            if module is not None:
                sys.modules[name] = module


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reduction(old: int, new: int) -> float:
    if old <= 0:
        raise AssertionError("executable baseline must be positive")
    return 1 - new / old


def normalized_boundary(events: tuple[str, ...]) -> tuple[str, ...]:
    normalized: list[str] = []
    for event in events:
        if not normalized or normalized[-1] != event:
            normalized.append(event)
    return tuple(normalized)


class PublicationOwnerAdapter:
    class WorkflowError(RuntimeError):
        def __init__(self, message: str, *, payload=None, **_kwargs) -> None:
            super().__init__(message)
            self.payload = payload or {}

    class InvocationContext:
        def __init__(self, owner, root: Path, task_ref: str) -> None:
            self.owner = owner
            self.task_dir = root / task_ref
            self.checked_owner_result = None
            self.operation_counts: dict[str, int] = {}

        def count(self, operation: str) -> None:
            self.operation_counts[operation] = self.operation_counts.get(operation, 0) + 1

    def __init__(self, root: Path, owner_result: dict[str, Any]) -> None:
        self.root = root
        self.owner_result = owner_result
        self.full_reads = 0
        self.lifecycle: list[str] = []
        self.boundary: list[str] = []
        self.checkpoint = root / "owner/pr-readiness.json"
        outer = self

        class ContextFactory:
            @staticmethod
            def create(context_root: Path, task_ref: str):
                return PublicationOwnerAdapter.InvocationContext(
                    outer, context_root, task_ref
                )

        self.TaskPublicationInvocationContext = ContextFactory

    def repo_root(self, _path: Path) -> Path:
        return self.root

    @staticmethod
    def read_json(path: Path) -> dict[str, Any]:
        return read_json(path)

    @staticmethod
    def skill_json_loads(value: str, _label: str) -> dict[str, Any]:
        return json.loads(value)

    def resolve_task_dir(self, root: Path, task_ref: str) -> Path:
        return root / task_ref

    def task_publication_path(self, _root: Path, _task: Path) -> Path:
        return self.checkpoint

    def _snapshot(self, context=None) -> None:
        if context is None or context.checked_owner_result is None:
            self.full_reads += 1

    def cmd_record_task_publication_review(self, _args, *, invocation_context=None):
        self.boundary.append("semantic.record")
        self._snapshot(invocation_context)
        self.checkpoint.parent.mkdir(parents=True, exist_ok=True)
        self.checkpoint.write_text(json.dumps(self.owner_result), encoding="utf-8")
        self.lifecycle.append("checkpoint:create")
        if invocation_context is not None:
            invocation_context.checked_owner_result = json.loads(json.dumps(self.owner_result))
            invocation_context.count("semantic.record")
            invocation_context.count("objective.check")
        return json.loads(json.dumps(self.owner_result))

    def cmd_check_task_publication_review(self, _args, *, invocation_context=None):
        self.boundary.append("deterministic.validate")
        self._snapshot(invocation_context)
        result = (
            invocation_context.checked_owner_result
            if invocation_context is not None
            else self.owner_result
        )
        if invocation_context is not None:
            invocation_context.count("checkpoint.verify")
        return {"owner_result": json.loads(json.dumps(result))}


class FinalizerOwnerAdapter:
    class WorkflowError(RuntimeError):
        pass

    FINALIZATION_REPREPARE_ARCHIVE_MONTH = "archive_month_changed"
    FINALIZATION_REPREPARE_PROVENANCE_TAIL = "provenance_tail_required"
    FINALIZATION_EXECUTOR_OUTPUT_MARKER = {"executor": True}
    FINALIZATION_CONSUMERS = {
        "reprepare_required": {"kind": "skill", "id": "guru-finalize-task"}
    }
    FINALIZE_TASK_SKILL_ID = "guru-finalize-task"

    def __init__(self, root: Path) -> None:
        self.root = root
        self.task_dir = root / ".trellis/tasks/fixture"
        self.task_dir.mkdir(parents=True)
        self.facts = {
            "exit_id": "ready_for_merge",
            "repo_ref": "castbox/guru-trellis",
            "pr_number": 330,
            "pr_url": "https://github.com/castbox/guru-trellis/pull/330",
            "expected_head_sha": "1" * 40,
            "expected_base_branch": "main",
            "expected_head_branch": "codex/330-closeout-happy-path-consolidation",
            "expected_close_issues": [330],
        }
        self.full_reads = 0
        self.mutations: list[str] = []
        self.lifecycle: list[str] = []
        self.boundary: list[str] = []
        self.gate_path = root / "owner/finalization-gate.json"
        self.terminal = False

    def terminal_output(self) -> dict[str, Any]:
        return json.loads(json.dumps(self.facts))

    def repo_root(self, _path: Path) -> Path:
        return self.root

    def finalization_public_input(self, _root, _input):
        return ({"profile": "publication_ready", "mode": "workflow", "task_ref": ".trellis/tasks/fixture"}, "input.json")

    def finalization_semantic_review_input(self, _root, _review):
        return {
            "schema_version": "3.0",
            "skill_id": "guru-finalize-task",
            "review": {},
            "route": {
                "typed_exit": "ready_for_merge",
                "output": self.FINALIZATION_EXECUTOR_OUTPUT_MARKER,
            },
        }

    def _context(self):
        self.full_reads += 1
        return {
            "plan": {"git": {"branch_review_commit": "1" * 40, "publication_head": "1" * 40}},
            "task_dir": self.task_dir,
            "transaction_state": "ready" if self.terminal else "prepared",
            "published_transition_complete": self.terminal,
            "reprepare_reason_code": None,
        }

    def finalization_preview_context(self, *_args):
        return self._context()

    def finalization_confirmation_identity(self, *_args):
        return "a" * 64

    def _record(self, reviewed):
        self.boundary.append("semantic.record")
        self.gate_path.parent.mkdir(parents=True, exist_ok=True)
        self.gate_path.write_text(json.dumps(reviewed), encoding="utf-8")
        self.lifecycle.append("gate:create")
        return {"gate": reviewed, "gate_path": self.gate_path}

    def finalization_record_gate_result(self, _root, _public, reviewed, _context, **_kwargs):
        return self._record(reviewed)

    def check_finalization_gate_context(self, _root, _public, gate, _path, _context, **_kwargs):
        self.boundary.append("deterministic.validate")
        return gate, {"plan": {}}

    def execute_finalization_transition_result(self, *_args):
        if not self.terminal:
            self.boundary.append("mutation")
            self.mutations.append("github.pr.mutate")
            self.terminal = True
        return {
            "typed_exit": "ready_for_merge",
            "output": self.terminal_output(),
            "task_dir": self.task_dir,
        }

    def finalization_output_contract(self, *_args):
        return {}

    @staticmethod
    def skill_json_schema_validation_errors(*_args):
        return []

    def finalization_retire_current_state(self, *_args):
        self.gate_path.unlink(missing_ok=True)
        self.lifecycle.append("gate:retire")
        return ["gate"]

    def cmd_preview_finalization(self, _args):
        return self._context()

    def cmd_record_finalization_gate(self, _args):
        self._context()
        return self._record(self.finalization_semantic_review_input(None, None))

    def cmd_check_finalization_gate(self, _args):
        self.boundary.append("deterministic.validate")
        self._context()
        return {
            "typed_exit": "ready_for_merge",
            "route": {
                "typed_exit": "ready_for_merge",
                "output": self.FINALIZATION_EXECUTOR_OUTPUT_MARKER,
            },
        }

    def cmd_execute_finalization_transition(self, _args):
        self._context()
        return self.execute_finalization_transition_result()

    def finalization_gate_input(self, *_args):
        return self.finalization_semantic_review_input(None, None), self.gate_path

    def check_finalization_gate_result(self, *_args):
        context = self._context()
        checked = self.finalization_semantic_review_input(None, None)
        return checked, {"plan": context["plan"], "task_dir": self.task_dir, "published_pr": {}}

    def finalization_gate_with_ready_for_merge_output(
        self, _root, _task_dir, checked, _plan, _pr
    ):
        materialized = json.loads(json.dumps(checked))
        materialized["route"]["output"] = self.terminal_output()
        return materialized

    def stage0_output_contract(self, *_args):
        return {}, None

    def finalization_package_root(self, *_args):
        return self.root

    def finalization_interface(self, *_args):
        return {}


class MergeOwnerAdapter:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.full_reads = 0
        self.mutations: list[str] = []
        self.lifecycle: list[str] = []
        self.boundary: list[str] = []
        self.terminal = False
        self.facts = {
            "exit_id": "closure_mismatch",
            "repo_ref": "castbox/guru-trellis",
            "pr_number": 330,
            "pr_url": "https://github.com/castbox/guru-trellis/pull/330",
            "merge_commit_sha": "2" * 40,
            "mismatches": [
                {"issue_number": 330, "reason_code": "not_closed_by_merge"}
            ],
        }
        self.gate = root / "owner/task-pr-merge-gate.json"

    def terminal_output(self) -> dict[str, Any]:
        return json.loads(json.dumps(self.facts))

    def _read(self) -> None:
        self.full_reads += 1

    def _create_gate(self) -> None:
        self.gate.parent.mkdir(parents=True, exist_ok=True)
        self.gate.write_text("{}\n", encoding="utf-8")
        self.lifecycle.append("gate:create")

    def _retire(self) -> None:
        self.gate.unlink(missing_ok=True)
        self.lifecycle.append("gate:retire")

    def cmd_record_task_pr_merge(self, _args):
        self.boundary.append("semantic.record")
        self._read()
        self._create_gate()
        return {"status": "recorded", "typed_exit": "ready_to_merge"}

    def cmd_preview_task_pr_merge(self, _args):
        self._read()
        return {"status": "previewed", "typed_exit": "ready_to_merge"}

    def cmd_check_task_pr_merge(self, _args):
        self.boundary.append("deterministic.validate")
        self._read()
        return {"status": "passed", "typed_exit": "ready_to_merge"}

    def cmd_execute_task_pr_merge(self, _args):
        self._read()
        if not self.terminal:
            self.boundary.append("mutation")
            self.mutations.append("github.merge.mutate")
            self.terminal = True
        output = self.terminal_output()
        return {"status": "executed", "typed_exit": output["exit_id"], "output": output}

    def cmd_invoke_task_pr_merge(self, _args):
        self._read()
        self._retire()
        return self.terminal_output()

    def cmd_complete_task_pr_merge(self, _args):
        self._read()
        if self.terminal:
            return self.terminal_output()
        self.boundary.extend(("semantic.record", "deterministic.validate", "mutation"))
        self._create_gate()
        self.mutations.append("github.merge.mutate")
        self.terminal = True
        self._read()
        self._retire()
        return self.terminal_output()


def command_module(package: Path, filename: str, suffix: str):
    return load_module(package / "runtime" / filename, f"closeout_{suffix}_{filename[:-3]}")


def assert_route_equivalence(
    test: unittest.TestCase,
    old: ExecutedRoute,
    new: ExecutedRoute,
    *,
    required_full_reads: int,
    compare_lifecycle: bool = True,
) -> None:
    test.assertEqual(old.output["exit_id"], new.output["exit_id"])
    test.assertEqual(old.output, new.output)
    test.assertEqual(old.mutations, new.mutations)
    test.assertEqual(normalized_boundary(old.boundary), normalized_boundary(new.boundary))
    test.assertEqual(old.recovery_output, new.recovery_output)
    if compare_lifecycle:
        test.assertEqual(old.lifecycle, new.lifecycle)
    test.assertEqual(old.post_exit_operations, 0)
    test.assertEqual(new.post_exit_operations, 0)
    test.assertGreaterEqual(reduction(len(old.commands), len(new.commands)), 0.50)
    old_repeated = old.full_reads - required_full_reads
    new_repeated = new.full_reads - required_full_reads
    test.assertGreater(old_repeated, 0)
    test.assertGreaterEqual(reduction(old_repeated, new_repeated), 0.70)


class CloseoutHappyPathIntegrationTests(unittest.TestCase):
    def commit_route(self, *, recommended: bool) -> ExecutedRoute:
        package = PACKAGES / "guru-create-task-commit"
        with tempfile.TemporaryDirectory(prefix="closeout-commit-") as temporary:
            root = Path(temporary) / "repo"
            root.mkdir()
            fixed_env = {
                "GIT_AUTHOR_DATE": "2026-09-02T12:00:00Z",
                "GIT_COMMITTER_DATE": "2026-09-02T12:00:00Z",
            }

            def git(*args: str) -> str:
                result = subprocess.run(
                    ["git", *args],
                    cwd=root,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env={**os.environ, **fixed_env},
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                return result.stdout.strip()

            git("init", "-q", "-b", "feature/happy-path")
            git("config", "user.name", "Closeout Harness")
            git("config", "user.email", "closeout@example.test")
            (root / "reviewed.txt").write_text("before\n", encoding="utf-8")
            (root / "unrelated.txt").write_text("before\n", encoding="utf-8")
            task = root / ".trellis/tasks/09-02-happy-path"
            task.mkdir(parents=True)
            (task / "task.json").write_text(
                json.dumps(
                    {
                        "id": "09-02-happy-path",
                        "status": "in_progress",
                        "branch": "feature/happy-path",
                        "base_branch": "main",
                    }
                ),
                encoding="utf-8",
            )
            (task / "issue-scope-ledger.json").write_text(
                json.dumps({"primary_issue": {"number": 330}}), encoding="utf-8"
            )
            git("add", ".")
            git("commit", "-q", "-m", "base")
            parent = git("rev-parse", "HEAD")
            phase2 = root / ".trellis/.runtime/guru-team/owner-checkpoints/09-02-happy-path/phase2-check.json"
            phase2.parent.mkdir(parents=True)
            phase2.write_text(
                json.dumps(
                    {
                        "typed_exit": "passed",
                        "task_ref": ".trellis/tasks/09-02-happy-path",
                        "phase2_capture_commit": parent,
                    }
                ),
                encoding="utf-8",
            )
            (root / "reviewed.txt").write_text("reviewed\n", encoding="utf-8")
            (root / "unrelated.txt").write_text("preserved\n", encoding="utf-8")
            public = root / ".trellis/.runtime/guru-team/test-inputs/public.json"
            public.parent.mkdir(parents=True, exist_ok=True)
            public.write_text(
                json.dumps(
                    {
                        "profile": "initial_commit",
                        "source_exit": "passed",
                        "mode": "workflow",
                        "task_ref": ".trellis/tasks/09-02-happy-path",
                        "phase2_commit_anchor": parent,
                    }
                ),
                encoding="utf-8",
            )
            subject = "fix(commit): #330 收敛提交正常路径"
            body = (
                "背景：\n减少正常提交的编排调用。\n\n"
                "变更：\n增加确认后事务 facade。\n\n"
                "边界：\n保留无关工作区状态。\n\n"
                "验证：\n运行 package-local 回归。\n\nRefs #330"
            )
            authoring = {
                "path_classifications": [
                    {
                        "path": "reviewed.txt",
                        "category": "task-reviewed",
                        "reason": "Covered by the current Phase 2 result.",
                        "coverage_source": "guru-check-task",
                    },
                    {
                        "path": "unrelated.txt",
                        "category": "unrelated-preserved",
                        "reason": "Parallel work remains outside this commit.",
                        "coverage_source": "live worktree",
                    },
                ],
                "message": {
                    "type": "fix",
                    "scope": "commit",
                    "summary": "收敛提交正常路径",
                    "background": "减少正常提交的编排调用。",
                    "changes": "增加确认后事务 facade。",
                    "boundaries": "保留无关工作区状态。",
                    "validations": "运行 package-local 回归。",
                    "subject": subject,
                    "body": body,
                    "bytes": subject + "\n\n" + body + "\n",
                },
                "ai_review": {
                    "status": "passed",
                    "summary": "The current paths and message satisfy the semantic gate.",
                    "evidence": ["Phase 2 covers reviewed.txt and excludes unrelated.txt."],
                },
            }
            commands: list[str] = []
            lifecycle: list[str] = []
            boundary = ["semantic.review"]
            mutations: list[str] = []
            validation_reads = 0
            with package_modules(package), mock.patch.dict(os.environ, fixed_env):
                common = __import__("common")
                original_validate = common.validate_candidate

                def counted_validate(*args, **kwargs):
                    nonlocal validation_reads
                    validation_reads += 1
                    return original_validate(*args, **kwargs)

                common.validate_candidate = counted_validate
                record = command_module(package, "record.py", "commit")
                check = command_module(package, "check.py", "commit")
                execute = command_module(package, "execute.py", "commit")
                invoke = command_module(package, "invoke.py", "commit")
                original_git = execute.git
                original_run = execute.subprocess.run

                def traced_git(repo: Path, *args: str, **kwargs):
                    if args and args[0] == "update-ref":
                        mutations.append("git.ref.mutate")
                    return original_git(repo, *args, **kwargs)

                def traced_run(command, *args, **kwargs):
                    if (
                        isinstance(command, list)
                        and len(command) > 1
                        and command[0] == "git"
                        and "--cleanup=verbatim" in command
                    ):
                        mutations.append("git.commit.mutate")
                    return original_run(command, *args, **kwargs)

                execute.git = traced_git
                invoke.execute_commit.__globals__["git"] = traced_git
                with mock.patch.object(execute.subprocess, "run", new=traced_run):
                    commands.append("prepare-task-commit")
                    prepared = record.run(
                        package,
                        {"id": commands[-1]},
                        ["--root", str(root), "--input", str(public), "--candidate-json", json.dumps(authoring)],
                    )
                    candidate = root / prepared["candidate_artifact"]
                    receipt = common.commit_result_path(root, "09-02-happy-path", "001")
                    self.assertTrue(candidate.is_file())
                    self.assertTrue(phase2.is_file())
                    self.assertFalse(receipt.exists())
                    lifecycle.append("candidate:create")
                    validation_reads = 0
                    before = git("rev-parse", "HEAD")
                    if recommended:
                        commands.append("invoke-guru-create-task-commit-happy-path-v1")
                        output = invoke.run(package, {"id": commands[-1]}, ["--root", str(root), "--candidate-artifact", prepared["candidate_artifact"]])
                        boundary.extend(("deterministic.validate", "mutation", "public.project"))
                        mutation_count = git("rev-list", "--count", f"{before}..HEAD")
                        route_reads = validation_reads
                        recovery = invoke.run(package, {"id": commands[-1]}, ["--root", str(root), "--candidate-artifact", prepared["candidate_artifact"]])
                    else:
                        commands.append("check-commit-messages")
                        check.run(package, {"id": commands[-1]}, ["--root", str(root), "--candidate-artifact", str(candidate)])
                        commands.append("create-task-commit")
                        executed = execute.run(package, {"id": commands[-1]}, ["--root", str(root), "--candidate-artifact", str(candidate)])
                        invocation = root / ".trellis/.runtime/guru-team/test-inputs/invocation.json"
                        invocation.write_text(json.dumps({"task_ref": prepared["task_ref"], "base_ref": "main", "result": executed}), encoding="utf-8")
                        commands.append("invoke-guru-create-task-commit")
                        output = invoke.run(package, {"id": commands[-1]}, ["--root", str(root), "--invocation", str(invocation)])
                        boundary.extend(("deterministic.validate", "mutation", "public.project"))
                        mutation_count = git("rev-list", "--count", f"{before}..HEAD")
                        route_reads = validation_reads
                        recovery = invoke.run(package, {"id": commands[-1]}, ["--root", str(root), "--invocation", str(invocation)])
            self.assertEqual(mutation_count, "1")
            self.assertEqual(
                mutations,
                ["git.commit.mutate", "git.ref.mutate"],
            )
            self.assertFalse(candidate.exists())
            self.assertFalse(phase2.exists())
            self.assertEqual(receipt.exists(), recommended)
            lifecycle.extend(("candidate:retire", "phase2:retire"))
            lifecycle.append("receipt:retained" if receipt.exists() else "receipt:absent")
            lifecycle.append("recovery:receipt" if receipt.exists() else "recovery:caller-result")
            self.assertEqual((root / "unrelated.txt").read_text(encoding="utf-8"), "preserved\n")
            return ExecutedRoute(
                output,
                commands,
                route_reads,
                mutations,
                lifecycle,
                tuple(boundary),
                recovery,
            )

    def publication_route(self, *, recommended: bool) -> ExecutedRoute:
        package = PACKAGES / "guru-review-task-publication"
        with tempfile.TemporaryDirectory(prefix="closeout-publication-") as temporary:
            root = Path(temporary)
            public = read_json(package / "examples/public-publication-review-input.json")
            owner_result = read_json(package / "examples/pr-readiness.json")
            semantic = {
                key: json.loads(json.dumps(owner_result[key]))
                for key in (
                    "pr_payload",
                    "candidate_classifications",
                    "dimensions",
                    "findings",
                    "conclusions",
                    "route",
                )
            }
            semantic.update(
                profile=public["profile"],
                mode=public["mode"],
                review_intent=public["review_intent"],
            )
            public_path = root / "public.json"
            semantic_path = root / "semantic.json"
            owner_path = root / "owner.json"
            public_path.write_text(json.dumps(public), encoding="utf-8")
            semantic_path.write_text(json.dumps(semantic), encoding="utf-8")
            owner_path.write_text(json.dumps(owner_result), encoding="utf-8")
            owner = PublicationOwnerAdapter(root, owner_result)
            commands: list[str] = []
            with package_modules(package):
                record = command_module(package, "record.py", "publication")
                check = command_module(package, "check.py", "publication")
                invoke = command_module(package, "invoke.py", "publication")
                with (
                    mock.patch.object(record, "_owner", return_value=owner),
                    mock.patch.object(check, "_owner", return_value=owner),
                    mock.patch.object(invoke, "_owner", return_value=owner),
                ):
                    if recommended:
                        commands.append("review-task-publication")
                        output = invoke.run(
                            package,
                            {"id": commands[-1]},
                            ["--root", str(root), "--input", str(public_path), "--semantic-result", str(semantic_path)],
                        )
                    else:
                        commands.append("record-task-publication-review")
                        record.run(package, {"id": commands[-1]}, ["--root", str(root), "--task", public["task_ref"], "--input", str(semantic_path), "--branch-review-commit", public["branch_review_commit"]])
                        commands.append("check-task-publication-review")
                        check.run(package, {"id": commands[-1]}, ["--root", str(root), "--task", public["task_ref"]])
                        commands.append("invoke-guru-review-task-publication")
                        output = invoke.run(package, {"id": commands[-1]}, ["--root", str(root), "--input", str(public_path), "--owner-result", str(owner_path)])
            if not owner.checkpoint.exists():
                owner.lifecycle.append("checkpoint:retire")
            return ExecutedRoute(
                output=output,
                commands=commands,
                full_reads=owner.full_reads,
                mutations=[],
                lifecycle=owner.lifecycle,
                boundary=("semantic.review", *owner.boundary, "public.project"),
            )

    def finalizer_route(self, *, recommended: bool) -> ExecutedRoute:
        package = PACKAGES / "guru-finalize-task"
        with tempfile.TemporaryDirectory(prefix="closeout-finalizer-") as temporary:
            root = Path(temporary)
            owner = FinalizerOwnerAdapter(root)
            commands: list[str] = []
            public_path = root / "public.json"
            review_path = root / "review.json"
            owner_path = root / "owner.json"
            for path in (public_path, review_path, owner_path):
                path.write_text("{}\n", encoding="utf-8")
            with package_modules(package):
                record = command_module(package, "record.py", "finalizer")
                check = command_module(package, "check.py", "finalizer")
                execute = command_module(package, "execute.py", "finalizer")
                invoke = command_module(package, "invoke.py", "finalizer")
                facade = command_module(package, "facade.py", "finalizer")
                with (
                    mock.patch.object(record, "_o", return_value=owner),
                    mock.patch.object(check, "_o", return_value=owner),
                    mock.patch.object(execute, "_o", return_value=owner),
                    mock.patch.object(invoke, "_o", return_value=owner),
                    mock.patch.object(invoke, "_facade", return_value=facade),
                    mock.patch.object(facade, "_owner", return_value=owner),
                ):
                    common = ["--root", str(root), "--input", str(public_path)]
                    if recommended:
                        commands.append("finalize-task-happy-path")
                        output = invoke.run(package, {"id": commands[-1]}, common + ["--review-input", str(review_path), "--confirmed-preview-sha256", "a" * 64])
                        boundary = ("semantic.review", *owner.boundary, "public.project")
                        lifecycle = list(owner.lifecycle)
                        mutation_count = len(owner.mutations)
                        recovery = invoke.run(package, {"id": commands[-1]}, common + ["--review-input", str(review_path)])
                        self.assertEqual(mutation_count, len(owner.mutations))
                    else:
                        commands.append("preview-finalization")
                        check.run(package, {"id": commands[-1]}, common)
                        commands.append("record-finalization-gate")
                        record.run(package, {"id": commands[-1]}, common + ["--review-input", str(review_path)])
                        commands.append("check-finalization-gate")
                        check.run(package, {"id": commands[-1]}, common)
                        commands.append("execute-finalization-transition")
                        execute.run(package, {"id": commands[-1]}, common)
                        commands.append("invoke-guru-finalize-task")
                        output = invoke.run(package, {"id": commands[-1]}, common + ["--owner-result", str(owner_path)])
                        boundary = ("semantic.review", *owner.boundary, "public.project")
                        lifecycle = list(owner.lifecycle)
                        mutation_count = len(owner.mutations)
                        recovery = invoke.run(package, {"id": commands[-1]}, common + ["--owner-result", str(owner_path)])
                        self.assertEqual(mutation_count, len(owner.mutations))
            return ExecutedRoute(output, commands, owner.full_reads - 1, list(owner.mutations), lifecycle, boundary, recovery)

    def merge_route(self, *, recommended: bool) -> ExecutedRoute:
        package = PACKAGES / "guru-merge-task-pr"
        with tempfile.TemporaryDirectory(prefix="closeout-merge-") as temporary:
            root = Path(temporary)
            owner = MergeOwnerAdapter(root)
            commands: list[str] = []
            public_path = root / "public.json"
            review_path = root / "review.json"
            public_path.write_text("{}\n", encoding="utf-8")
            review_path.write_text("{}\n", encoding="utf-8")
            with package_modules(package):
                record = command_module(package, "record.py", "merge")
                check = command_module(package, "check.py", "merge")
                execute = command_module(package, "execute.py", "merge")
                invoke = command_module(package, "invoke.py", "merge")
                with (
                    mock.patch.object(record, "_owner", return_value=owner),
                    mock.patch.object(check, "_owner", return_value=owner),
                    mock.patch.object(execute, "_owner", return_value=owner),
                    mock.patch.object(invoke, "_owner", return_value=owner),
                ):
                    common = ["--root", str(root), "--input", str(public_path)]
                    if recommended:
                        commands.append("complete-task-pr-merge")
                        output = invoke.run(package, {"id": commands[-1]}, common + ["--review-input", str(review_path)])
                        boundary = ("semantic.review", *owner.boundary, "public.project")
                        lifecycle = list(owner.lifecycle)
                        mutation_count = len(owner.mutations)
                        recovery = invoke.run(package, {"id": commands[-1]}, common + ["--review-input", str(review_path)])
                        self.assertEqual(mutation_count, len(owner.mutations))
                    else:
                        commands.append("record-task-pr-merge")
                        record.run(package, {"id": commands[-1]}, common + ["--review-input", str(review_path)])
                        commands.append("check-task-pr-merge")
                        check.run(package, {"id": commands[-1]}, common)
                        commands.append("execute-task-pr-merge")
                        execute.run(package, {"id": commands[-1]}, common)
                        commands.append("invoke-task-pr-merge")
                        output = invoke.run(package, {"id": commands[-1]}, common)
                        boundary = ("semantic.review", *owner.boundary, "public.project")
                        lifecycle = list(owner.lifecycle)
                        mutation_count = len(owner.mutations)
                        recovery = json.loads(json.dumps(output))
                        self.assertEqual(mutation_count, len(owner.mutations))
            return ExecutedRoute(output, commands, owner.full_reads - (1 if recommended else 0), list(owner.mutations), lifecycle, boundary, recovery)

    def test_each_stage_has_one_recommended_public_wrapper(self) -> None:
        for skill_id, expected in HAPPY_PATHS.items():
            with self.subTest(skill=skill_id):
                package = PACKAGES / skill_id
                commands = {
                    item["id"]: item
                    for item in read_json(package / "commands.json")["commands"]
                }
                interface = read_json(package / "interface.json")
                self.assertTrue(set(expected["commands"] + expected["legacy"]) <= commands.keys())
                recommended = [
                    item
                    for item in interface["validators"]
                    if item["command"] == expected["wrapper"]
                ]
                self.assertEqual(1, len(recommended))
                self.assertEqual(expected["commands"][-1], recommended[0]["runtime_command"])
                if expected["public_invocation_switch"]:
                    self.assertEqual(
                        expected["wrapper"],
                        interface["public_contracts"]["invocation"]["wrapper"],
                    )

    def test_old_and_new_routes_execute_equivalent_public_contracts(self) -> None:
        for stage, runner, required_reads in (
            ("commit", self.commit_route, 1),
            ("publication", self.publication_route, 1),
            ("finalizer", self.finalizer_route, 1),
            ("merge", self.merge_route, 2),
        ):
            with self.subTest(stage=stage):
                old = runner(recommended=False)
                new = runner(recommended=True)
                assert_route_equivalence(
                    self,
                    old,
                    new,
                    required_full_reads=required_reads,
                    compare_lifecycle=stage != "commit",
                )

                if stage == "commit":
                    self.assertEqual(
                        old.lifecycle[:2],
                        ["candidate:create", "candidate:retire"],
                    )
                    self.assertEqual(
                        new.lifecycle[:2],
                        ["candidate:create", "candidate:retire"],
                    )
                    self.assertIn("phase2:retire", old.lifecycle)
                    self.assertIn("phase2:retire", new.lifecycle)
                    self.assertIn("receipt:absent", old.lifecycle)
                    self.assertIn("receipt:retained", new.lifecycle)
                    self.assertIn("recovery:caller-result", old.lifecycle)
                    self.assertIn("recovery:receipt", new.lifecycle)

                interface = read_json(PACKAGES / {
                    "publication": "guru-review-task-publication",
                    "commit": "guru-create-task-commit",
                    "finalizer": "guru-finalize-task",
                    "merge": "guru-merge-task-pr",
                }[stage] / "interface.json")
                self.assertEqual(interface["judgment_mode"], "semantic")

    def test_sanitized_fixture_is_historical_observation_not_budget_input(self) -> None:
        fixture = read_json(FIXTURE)
        self.assertEqual(
            fixture["source"]["kind"],
            "sanitized_session_observation",
        )
        source = Path(__file__).read_text(encoding="utf-8")
        executable_test = source.split(
            "def test_old_and_new_routes_execute_equivalent_public_contracts", 1
        )[1].split(
            "def test_sanitized_fixture_is_historical_observation_not_budget_input",
            1,
        )[0]
        self.assertNotIn('read_json(FIXTURE)["stages"]', executable_test)

    def test_merge_watcher_is_single_expected_head_bound_entry(self) -> None:
        commands = read_json(
            PACKAGES / "guru-merge-task-pr/commands.json"
        )["commands"]
        watcher = next(item for item in commands if item["id"] == "watch-task-pr-checks")
        flags = {item["flag"] for item in watcher["arguments"]}
        self.assertTrue({"--repo", "--pull-request", "--expected-head"} <= flags)
        source = (
            PACKAGES / "guru-merge-task-pr/runtime/owner.py"
        ).read_text(encoding="utf-8")
        watcher_source = source[source.index("def cmd_watch_task_pr_checks") :]
        self.assertNotIn("gh run watch", watcher_source)
        self.assertNotIn("--watch", watcher_source)

    def test_merge_terminal_exits_stop_the_current_skill(self) -> None:
        markers = re.findall(
            r"<!-- guru-skill-exit: (\{.*?\}) -->",
            WORKFLOW.read_text(encoding="utf-8"),
        )
        routes = {
            (item["skill"], item["exit"]): item["consumer"]
            for item in map(json.loads, markers)
        }
        self.assertEqual(
            routes[("guru-merge-task-pr", "closure_mismatch")],
            {"kind": "stop", "id": "task-pr-closure-mismatch"},
        )
        self.assertNotEqual(
            routes[("guru-merge-task-pr", "merged")],
            {"kind": "skill", "id": "guru-merge-task-pr"},
        )
        terminal = read_json(FIXTURE)["terminal_observation"]
        self.assertEqual(terminal["expected_current_contract_operations_after_exit"], 0)


if __name__ == "__main__":
    unittest.main()
