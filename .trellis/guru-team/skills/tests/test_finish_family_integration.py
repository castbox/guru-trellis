from __future__ import annotations

import argparse
from contextlib import ExitStack
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest import mock


SOURCE_REPO = Path(__file__).resolve().parents[4]
EXECUTION_MODE = os.environ.get("GURU_FINISH_INTEGRATION_MODE", "source")
if EXECUTION_MODE not in {"source", "installed"}:
    raise RuntimeError("GURU_FINISH_INTEGRATION_MODE must be source or installed")
REPO = Path(
    os.environ.get("GURU_FINISH_INTEGRATION_ROOT", str(SOURCE_REPO))
).resolve()
if EXECUTION_MODE == "installed":
    SKILLS_ROOT = REPO / ".trellis/guru-team/skills"
    WORKFLOW = REPO / ".trellis/workflow.md"
    EVAL_RUNNER = REPO / ".trellis/guru-team/scripts/bash/run-skill-evals.sh"
else:
    SKILLS_ROOT = REPO / "trellis/skills/guru-team"
    WORKFLOW = REPO / "trellis/workflows/guru-team/workflow.md"
    EVAL_RUNNER = (
        REPO / "trellis/workflows/guru-team/scripts/bash/run-skill-evals.sh"
    )

FINISH_EXITS = {
    "guru-review-task-publication": {"ready", "return_to_task_work", "blocked"},
    "guru-verify-extension-installation": {
        "verified", "not_required", "return_to_task_work", "blocked",
    },
    "guru-finalize-task": {
        "verification_required", "publication_review_stale",
        "resume_finalization", "reprepare_required", "published", "blocked",
    },
}
EXPECTED_CONSUMERS = {
    ("guru-review-task-publication", "ready"): ("skill", "guru-finalize-task"),
    ("guru-review-task-publication", "return_to_task_work"): (
        "workflow", "guru-task-publication-work-router",
    ),
    ("guru-review-task-publication", "blocked"): (
        "stop", "task-publication-review-blocked",
    ),
    ("guru-verify-extension-installation", "verified"): (
        "skill", "guru-finalize-task",
    ),
    ("guru-verify-extension-installation", "not_required"): (
        "skill", "guru-finalize-task",
    ),
    ("guru-verify-extension-installation", "return_to_task_work"): (
        "workflow", "guru-extension-verification-work-router",
    ),
    ("guru-verify-extension-installation", "blocked"): (
        "stop", "extension-installation-verification-blocked",
    ),
    ("guru-finalize-task", "verification_required"): (
        "skill", "guru-verify-extension-installation",
    ),
    ("guru-finalize-task", "publication_review_stale"): (
        "skill", "guru-review-task-publication",
    ),
    ("guru-finalize-task", "resume_finalization"): (
        "skill", "guru-finalize-task",
    ),
    ("guru-finalize-task", "reprepare_required"): (
        "skill", "guru-finalize-task",
    ),
    ("guru-finalize-task", "published"): (
        "workflow", "guru-finalization-finish-response",
    ),
    ("guru-finalize-task", "blocked"): (
        "stop", "task-finalization-blocked",
    ),
}
ROUTE_GROUPS = {
    "normal": [
        ("guru-review-task-publication", "ready"),
        ("guru-finalize-task", "published"),
    ],
    "extension": [
        ("guru-finalize-task", "verification_required"),
        ("guru-verify-extension-installation", "verified"),
        ("guru-finalize-task", "published"),
    ],
    "return_to_work": [
        ("guru-review-task-publication", "return_to_task_work"),
        ("guru-verify-extension-installation", "return_to_task_work"),
    ],
    "publication_refresh": [
        ("guru-finalize-task", "publication_review_stale"),
        ("guru-review-task-publication", "ready"),
    ],
    "same_plan_or_reprepare": [
        ("guru-finalize-task", "resume_finalization"),
        ("guru-finalize-task", "reprepare_required"),
    ],
    "terminal": [
        ("guru-review-task-publication", "blocked"),
        ("guru-verify-extension-installation", "blocked"),
        ("guru-finalize-task", "blocked"),
        ("guru-finalize-task", "published"),
    ],
}
PRIVATE_FIELDS = {
    "facts_sha256", "generated_at", "reviewer", "review_history",
    "transaction_state", "recovery_history", "closeout_plan",
    "changed_paths", "command_transcript",
}
GURU_ENTRIES = (
    ".codex/prompts/guru-finish-work.md",
    ".claude/commands/guru/finish-work.md",
    ".cursor/commands/guru-finish-work.md",
)
TERMINAL_CASES = {
    "publication-ready-published": (
        "publication_ready",
        "evals/files/publication-ready-published-facts.json",
        "finalization-publication-ready-published",
    ),
    "same-plan-published": (
        "same_plan_resume",
        "evals/files/same-plan-published-facts.json",
        "finalization-same-plan-published",
    ),
}


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{path} must contain one JSON object")
    return value


def package(skill_id: str) -> Path:
    return SKILLS_ROOT / "packages" / skill_id


def workflow_exits() -> list[dict[str, Any]]:
    text = WORKFLOW.read_text(encoding="utf-8")
    return [
        json.loads(value)
        for value in re.findall(r"<!-- guru-skill-exit: (\{.*?\}) -->", text)
    ]


def tree_bytes(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file() and not path.is_symlink()
    }


def output_object_branches(schema: dict[str, Any]) -> list[dict[str, Any]]:
    if schema.get("type") == "object":
        return [schema]
    branches = schema.get("oneOf")
    if isinstance(branches, list) and branches:
        return [branch for branch in branches if branch.get("type") == "object"]
    return []


def load_selected_runtime() -> Any:
    runtime = (
        REPO / ".trellis/guru-team/scripts/python/guru_team_trellis.py"
        if EXECUTION_MODE == "installed"
        else REPO / "trellis/workflows/guru-team/scripts/python/guru_team_trellis.py"
    )
    spec = importlib.util.spec_from_file_location(
        f"guru_finish_family_runtime_{EXECUTION_MODE}",
        runtime,
    )
    if spec is None or spec.loader is None:
        raise AssertionError(f"could not load runtime: {runtime}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FinishFamilyIntegrationTests(unittest.TestCase):
    def test_branch_review_passed_dto_reaches_side_effect_free_finalizer_preview(
        self,
    ) -> None:
        runtime = load_selected_runtime()
        branch_package = package("guru-review-branch")
        publication_package = package("guru-review-task-publication")
        gate = read_json(branch_package / "examples/review-gate.json")
        self.assertEqual(gate["schema_version"], "3.0")
        self.assertEqual(gate["typed_exit"], "passed")

        branch_output = {
            "exit_id": "passed",
            "task_ref": gate["task_dir"],
            "branch_review_commit": gate["review_commit"],
        }
        branch_interface = read_json(branch_package / "interface.json")
        branch_projection = next(
            item
            for item in branch_interface["public_contracts"]["projections"]
            if item["id"] == "project_passed"
        )
        publication_seed = runtime.skill_apply_projection(
            branch_projection,
            branch_output,
        )
        self.assertEqual(
            publication_seed,
            {
                "task_ref": gate["task_dir"],
                "branch_review_commit": gate["review_commit"],
            },
        )

        publication_output = {"exit_id": "ready", **publication_seed}
        publication_interface = read_json(publication_package / "interface.json")
        publication_projection = next(
            item
            for item in publication_interface["public_contracts"]["projections"]
            if item["id"] == "project_ready"
        )
        finalization_seed = runtime.skill_apply_projection(
            publication_projection,
            publication_output,
        )
        finalization_input = {
            "profile": "publication_ready",
            "mode": "workflow",
            **finalization_seed,
        }
        self.assertFalse(PRIVATE_FIELDS & set(publication_output))
        self.assertFalse(PRIVATE_FIELDS & set(finalization_input))

        with tempfile.TemporaryDirectory(prefix="guru-direct-finalizer-") as temporary:
            root = Path(temporary)
            task_dir = root / gate["task_dir"]
            task_dir.mkdir(parents=True)
            (task_dir / "task.json").write_text(
                json.dumps({"status": "in_progress"}),
                encoding="utf-8",
            )
            task_context = {"task_artifact_dir": gate["task_dir"]}
            plan = {
                "plan_digest": "c" * 64,
                "task": {
                    "active_locator": gate["task_dir"],
                    "archive_locator": (
                        ".trellis/tasks/archive/2026-08/example-task"
                    ),
                },
                "git": {
                    "repo": "castbox/guru-trellis",
                    "remote": "origin",
                    "base_branch": "main",
                    "head_branch": "codex/example-task",
                    "branch_review_commit": gate["review_commit"],
                },
                "marketplace": {"required": False},
            }
            prepared = {
                "plan": plan,
                "ledger": {},
                "gate": None,
                "month_supersession": None,
            }
            repository = {
                "head": gate["review_commit"],
                "branch": "codex/example-task",
                "base_ref": "origin/main",
                "diff_paths": ["src/example.py"],
                "status_paths": [],
            }
            before = tree_bytes(root)

            def prepare(
                _root: Path,
                _args: argparse.Namespace,
                _config: dict[str, Any],
                _task_dir: Path,
                _task_context: dict[str, Any],
                *,
                publication_ready: dict[str, Any] | None = None,
                verification_owner_result: Any = None,
            ) -> dict[str, Any]:
                self.assertEqual(publication_ready, finalization_input)
                self.assertIsNone(verification_owner_result)
                return prepared

            args = argparse.Namespace(
                root=str(root),
                input="inline-publication-ready.json",
                include_finalization_gate=True,
            )
            with (
                mock.patch.dict(os.environ, {"GURU_TEAM_EVAL_STAGING": "0"}),
                mock.patch.object(runtime, "repo_root", return_value=root),
                mock.patch.object(
                    runtime,
                    "finalization_public_input",
                    return_value=(finalization_input, args.input),
                ),
                mock.patch.object(runtime, "load_config", return_value={}),
                mock.patch.object(
                    runtime,
                    "load_task_runtime_identity",
                    return_value=task_context,
                ),
                mock.patch.object(runtime, "assert_workspace_boundary"),
                mock.patch.object(
                    runtime,
                    "finalization_verification_owner_result",
                    return_value=None,
                ),
                mock.patch.object(
                    runtime,
                    "task_publication_repository_binding",
                    return_value=repository,
                ),
                mock.patch.object(
                    runtime,
                    "task_publication_unexpected_status_paths",
                    return_value=[],
                ),
                mock.patch.object(
                    runtime,
                    "current_head",
                    return_value=gate["review_commit"],
                ),
                mock.patch.object(
                    runtime,
                    "review_branch_content_continuity_errors",
                    return_value=[],
                ),
                mock.patch.object(
                    runtime,
                    "reviewed_content_identity",
                    return_value={"sha256": gate["reviewed_content_sha256"]},
                ),
                mock.patch.object(runtime, "prepare_closeout", side_effect=prepare),
                mock.patch.object(
                    runtime,
                    "resolve_closeout_pre_draft_state",
                    return_value="prepared",
                ),
                mock.patch.object(
                    runtime,
                    "task_publication_path",
                    side_effect=AssertionError(
                        "Finalizer reopened Publication private evidence"
                    ),
                ) as private_artifact,
                mock.patch.object(
                    runtime,
                    "cmd_check_task_publication_review",
                    side_effect=AssertionError(
                        "Finalizer reran the Publication owner checker"
                    ),
                ) as owner_checker,
            ):
                preview = runtime.cmd_preview_finalization(args)

            self.assertFalse(preview["side_effects"])
            self.assertEqual(preview["transaction_state"], "prepared")
            self.assertEqual(preview["task_ref"], gate["task_dir"])
            self.assertEqual(
                preview["branch_review_commit"],
                gate["review_commit"],
            )
            self.assertEqual(tree_bytes(root), before)
            private_artifact.assert_not_called()
            owner_checker.assert_not_called()

    def test_verification_verified_reentry_keeps_scope_ledger_unchanged(
        self,
    ) -> None:
        runtime = load_selected_runtime()
        task_ref = ".trellis/tasks/example-finalizer-reentry"
        ledger_locator = f"{task_ref}/issue-scope-ledger.json"
        branch_review_commit = "a" * 40
        issue = {
            "number": 177,
            "url": "https://github.com/castbox/guru-trellis/issues/177",
            "title": "Content identity boundary",
            "reason": "Primary delivered scope.",
        }
        ledger = {
            "schema_version": "2.0",
            "primary_issue": issue,
            "close_issues": [issue],
            "related_issues": [],
            "followup_issues": [],
        }

        with tempfile.TemporaryDirectory(prefix="guru-finalizer-reentry-") as temporary:
            root = Path(temporary)
            task_dir = root / task_ref
            task_dir.mkdir(parents=True)
            (task_dir / "issue-scope-ledger.json").write_text(
                json.dumps(ledger),
                encoding="utf-8",
            )
            ledger_before = (task_dir / "issue-scope-ledger.json").read_bytes()
            plan = {
                "schema_version": runtime.CLOSEOUT_PLAN_SCHEMA_VERSION,
                "plan_digest": "d" * 64,
                "task": {
                    "active_locator": task_ref,
                    "archive_locator": (
                        ".trellis/tasks/archive/2026-08/"
                        "example-finalizer-reentry"
                    ),
                },
                "git": {"branch_review_commit": branch_review_commit},
                "review": {"changed_paths": []},
                "marketplace": {"required": True},
                "inputs": {
                    "issue_scope_ledger": {
                        "path": ledger_locator,
                        "sha256": hashlib.sha256(ledger_before).hexdigest(),
                    },
                },
            }
            (task_dir / runtime.CLOSEOUT_PLAN_ARTIFACT).write_text(
                json.dumps(plan),
                encoding="utf-8",
            )
            with mock.patch.object(
                runtime,
                "git_status_paths",
                return_value=[ledger_locator],
            ):
                self.assertEqual(
                    runtime.finalizer_unreviewed_dirty_paths(root, task_dir),
                    [],
                )
            owner_result = {
                "profile": "verification_required",
                "typed_exit": "verified",
            }
            checked_result = {"status": "ok", "typed_exit": "verified"}
            review_gate = {
                "review_commit": branch_review_commit,
                "reviewed_content_sha256": "c" * 64,
            }
            review_gate_path = runtime.configured_review_gate_path(root, task_dir)
            args = argparse.Namespace(
                finish_summary_index_file=None,
                repo=None,
                remote=None,
                title=None,
            )
            with ExitStack() as stack:
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "official_after_archive_hook_state",
                        return_value={},
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "validate_closeout_plan",
                        side_effect=lambda value: value,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "validate_review_gate",
                        return_value=(review_gate_path, review_gate, []),
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "review_branch_content_continuity_errors",
                        return_value=[],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "current_head",
                        return_value=branch_review_commit,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "closeout_reviewed_change_facts",
                        return_value={
                            "changed_paths": [],
                            "candidate_surfaces": ["workflow"],
                            "marketplace_required": True,
                        },
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "git_status_paths",
                        return_value=[ledger_locator],
                    )
                )
                dirty_paths = stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "finalizer_unreviewed_dirty_paths",
                        wraps=runtime.finalizer_unreviewed_dirty_paths,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "load_finish_summary_index",
                        return_value=(task_dir / "finish-summary-index.json", {}),
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "load_issue_scope_ledger",
                        return_value=ledger,
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "validate_ledger_for_publish",
                        return_value=[],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "resolve_closeout_reviewed_body",
                        return_value=("body", "body-file"),
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "validate_pr_body_quality",
                        return_value=[],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "validate_reviewed_body_source_for_publish",
                        return_value=[],
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "task_json",
                        return_value={"status": "in_progress"},
                    )
                )
                stack.enter_context(
                    mock.patch.object(runtime, "validate_closeout_task_children")
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "infer_github_repo",
                        return_value="castbox/guru-trellis",
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "normalize_github_repository",
                        return_value="castbox/guru-trellis",
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "base_branch_from_sources",
                        return_value="main",
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "current_branch",
                        return_value="codex/example",
                    )
                )
                stack.enter_context(
                    mock.patch.object(runtime, "validate_github_remote_repository")
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "pr_title_from_task",
                        return_value="title",
                    )
                )
                stack.enter_context(
                    mock.patch.object(
                        runtime,
                        "build_closeout_plan",
                        return_value=plan,
                    )
                )
                prepared = runtime.prepare_closeout(
                    root,
                    args,
                    {},
                    task_dir,
                    {},
                    verification_owner_result=(owner_result, checked_result),
                )

            self.assertEqual(prepared["plan"], plan)
            dirty_paths.assert_called_once_with(root, task_dir)
            self.assertEqual(
                (task_dir / "issue-scope-ledger.json").read_bytes(),
                ledger_before,
            )
            with mock.patch.object(
                runtime,
                "git_status_paths",
                return_value=[ledger_locator, "unrelated.txt"],
            ):
                self.assertEqual(
                    runtime.finalizer_unreviewed_dirty_paths(root, task_dir),
                    ["unrelated.txt"],
                )

    def test_stale_finalizer_projection_returns_content_drift_to_phase_2(
        self,
    ) -> None:
        runtime = load_selected_runtime()
        finalizer_package = package("guru-finalize-task")
        publication_package = package("guru-review-task-publication")
        finalizer_interface = read_json(finalizer_package / "interface.json")
        publication_interface = read_json(publication_package / "interface.json")

        stale_output = read_json(
            finalizer_package
            / "examples/public-publication-review-stale-output.json"
        )
        stale_projection = next(
            item
            for item in finalizer_interface["public_contracts"]["projections"]
            if item["id"] == "project_publication_review_stale"
        )
        stale_seed = runtime.skill_apply_projection(
            stale_projection,
            stale_output,
        )
        stale_authoring = read_json(
            finalizer_package
            / "examples/public-publication-review-stale-authoring.json"
        )
        stale_input = {**stale_seed, **stale_authoring}
        stale_profile = next(
            item
            for item in publication_interface["public_contracts"]["input"][
                "profiles"
            ]
            if item["id"] == "publication_review_stale"
        )
        stale_input_schema = read_json(
            publication_package / stale_profile["schema"]["path"]
        )
        self.assertEqual(
            runtime.skill_json_schema_validation_errors(
                stale_input,
                stale_input_schema,
                "Finalizer stale projection",
            ),
            [],
        )
        self.assertEqual(
            stale_input["branch_review_commit"],
            stale_output["branch_review_commit"],
        )

        owner = read_json(publication_package / "examples/pr-readiness.json")
        owner["task_ref"] = stale_input["task_ref"]
        owner["branch_review_commit"] = stale_input["branch_review_commit"]
        owner["dimensions"][0]["status"] = "finding"
        owner["findings"] = [{
            "finding_ref": "PUB-STALE-CONTENT-001",
            "dimension": "diff_outcome_consistency",
            "summary": "Current reviewed-content identity differs from the Branch Review anchor.",
            "scope_basis": "The task implementation changed after Branch Review.",
            "evidence_refs": ["git:branch_review_commit", "git:HEAD"],
            "affected_artifacts": ["trellis/workflows/guru-team/workflow.md"],
            "route_class": "task_work",
            "status": "open",
            "closure_evidence": [],
        }]
        owner["conclusions"]["issue_scope"]["status"] = "finding"
        owner["route"] = {"typed_exit": "return_to_task_work"}
        self.assertEqual(
            runtime.task_publication_semantic_errors(
                owner,
                branch_review_commit=stale_input["branch_review_commit"],
            ),
            [],
        )

        with tempfile.TemporaryDirectory(prefix="guru-stale-publication-") as temporary:
            root = Path(temporary)
            task_dir = root / stale_input["task_ref"]
            task_dir.mkdir(parents=True)
            continuity_error = (
                runtime.BRANCH_REVIEW_CONTENT_CHANGED_ERROR_PREFIX
                + "trellis/workflows/guru-team/workflow.md"
            )
            with (
                mock.patch.object(
                    runtime,
                    "task_publication_schema",
                    return_value=read_json(
                        publication_package / "schemas/pr-readiness.schema.json"
                    ),
                ),
                mock.patch.object(runtime, "load_config", return_value={}),
                mock.patch.object(runtime, "current_head", return_value="d" * 40),
                mock.patch.object(
                    runtime,
                    "review_branch_content_continuity_errors",
                    return_value=[continuity_error],
                ),
                mock.patch.object(
                    runtime,
                    "task_publication_entry_precondition_bindings",
                    return_value=({}, [continuity_error], {}, {}),
                ),
            ):
                self.assertEqual(
                    runtime.task_publication_check_errors(root, task_dir, owner),
                    [],
                )

        return_schema = read_json(
            publication_package
            / "schemas/public-return-to-task-work-output.schema.json"
        )
        returned = runtime.stage0_build_output(
            "guru-review-task-publication",
            "return_to_task_work",
            stale_input,
            owner,
            None,
            None,
            return_schema,
        )
        self.assertEqual(
            returned,
            {
                "exit_id": "return_to_task_work",
                "task_ref": stale_input["task_ref"],
                "finding_refs": ["PUB-STALE-CONTENT-001"],
                "resume_target": "phase-2",
            },
        )

    def test_selected_runtime_converges_pr_head_and_bounds_persistent_mismatch(
        self,
    ) -> None:
        runtime = load_selected_runtime()
        local_head = "a" * 40
        stale_head = "b" * 40
        body = "Issue #119 finalizer recovery\n"
        plan = {
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": "feat/119-finish-family-integration-main",
                "base_branch": "main",
            },
            "publish": {
                "title": "#119 完成 Finish family combined integration",
                "body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
            },
        }
        draft = {
            "number": 166,
            "url": "https://github.com/castbox/guru-trellis/pull/166",
            "title": plan["publish"]["title"],
            "body": body,
            "headRefName": plan["git"]["head_branch"],
            "baseRefName": "main",
            "headRefOid": stale_head,
            "isDraft": True,
            "headRepository": {"nameWithOwner": "castbox/guru-trellis"},
            "headRepositoryOwner": {"login": "castbox"},
            "isCrossRepository": False,
        }
        converged = dict(draft, headRefOid=local_head)
        ready = dict(converged, isDraft=False)
        with tempfile.TemporaryDirectory(prefix="guru-finish-head-") as temporary:
            root = Path(temporary)
            with (
                mock.patch.object(
                    runtime,
                    "resolve_closeout_pull_request",
                    side_effect=[draft, converged, ready],
                ) as resolve,
                mock.patch.object(runtime, "current_head", return_value=local_head),
                mock.patch.object(
                    runtime,
                    "closeout_remote_branch_head",
                    return_value=local_head,
                ),
                mock.patch.object(
                    runtime,
                    "run",
                    return_value=mock.Mock(returncode=0, stdout="", stderr=""),
                ) as command,
                mock.patch.object(runtime.time, "sleep") as sleeper,
            ):
                result = runtime.ensure_closeout_pr_ready(
                    root,
                    plan,
                    bound_pr=draft,
                )
            self.assertEqual(result["status"], "ready")
            self.assertEqual(result["pr"]["number"], 166)
            self.assertEqual(resolve.call_count, 3)
            sleeper.assert_called_once_with(
                runtime.CLOSEOUT_PR_HEAD_READ_DELAY_SECONDS,
            )
            self.assertEqual(command.call_count, 1)
            self.assertEqual(command.call_args.args[0][:3], ["gh", "pr", "ready"])

            with (
                mock.patch.object(
                    runtime,
                    "resolve_closeout_pull_request",
                    return_value=draft,
                ) as resolve,
                mock.patch.object(runtime, "current_head", return_value=local_head),
                mock.patch.object(
                    runtime,
                    "closeout_remote_branch_head",
                    return_value=local_head,
                ),
                mock.patch.object(runtime, "run") as command,
                mock.patch.object(runtime.time, "sleep") as sleeper,
                self.assertRaises(runtime.WorkflowError),
            ):
                runtime.ensure_closeout_pr_ready(root, plan, bound_pr=draft)
            self.assertEqual(
                resolve.call_count,
                runtime.CLOSEOUT_PR_HEAD_READ_ATTEMPTS,
            )
            self.assertEqual(
                sleeper.call_count,
                runtime.CLOSEOUT_PR_HEAD_READ_ATTEMPTS - 1,
            )
            command.assert_not_called()

    def test_selected_runtime_recovers_compact_archive_before_readiness_check(
        self,
    ) -> None:
        runtime = load_selected_runtime()
        plan_digest = "a" * 64
        branch_review_commit = "b" * 40
        active = ".trellis/tasks/07-31-119-combined-finish-family-integration"
        archive = (
            ".trellis/tasks/archive/2026-08/"
            "07-31-119-combined-finish-family-integration"
        )
        plan = {
            "plan_digest": plan_digest,
            "task": {"active_locator": active, "archive_locator": archive},
            "git": {
                "repo": "castbox/guru-trellis",
                "remote": "origin",
                "head_branch": "feat/119-finish-family-integration-main",
                "base_branch": "main",
                "branch_review_commit": branch_review_commit,
            },
            "marketplace": {"required": True},
        }
        public_input = {
            "profile": "same_plan_resume",
            "mode": "workflow",
            "task_ref": active,
            "plan_ref": f"closeout-plan:{plan_digest}",
        }
        publication = {
            "owner_status": "current",
            "publication_ref": f"publication:{'c' * 64}",
        }
        verification = (
            {"source": "committed-finalization-gate"},
            {
                "status": "ok",
                "typed_exit": "verified",
                "verification_ref": "extension-verification:checked",
            },
        )
        transaction = {
            "commit": "d" * 40,
            "parent": "e" * 40,
            "summary_pr": {
                "number": 166,
                "url": "https://github.com/castbox/guru-trellis/pull/166",
            },
        }
        with tempfile.TemporaryDirectory(prefix="guru-finish-archive-") as temporary:
            root = Path(temporary)
            archived = root / archive
            archived.mkdir(parents=True)
            retained = set(runtime.CLOSEOUT_ARCHIVE_CORE_ARTIFACTS)
            retained.update(runtime.CLOSEOUT_ARCHIVE_OPTIONAL_ARTIFACTS)
            for relative in retained:
                path = archived / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("committed fixture\n", encoding="utf-8")
            self.assertLessEqual(
                len(retained), runtime.CLOSEOUT_ARCHIVE_MAX_ARTIFACTS,
            )
            (archived / runtime.CLOSEOUT_PLAN_ARTIFACT).unlink()
            self.assertFalse((archived / runtime.CLOSEOUT_PLAN_ARTIFACT).exists())
            self.assertFalse((archived / runtime.PR_READINESS_ARTIFACT).exists())

            def committed_blob(
                _root: Path,
                commit: str,
                locator: str,
            ) -> bytes | None:
                self.assertEqual(commit, transaction["commit"])
                self.assertEqual(
                    locator,
                    f"{archive}/{runtime.CLOSEOUT_PLAN_ARTIFACT}",
                )
                return json.dumps(plan).encode("utf-8")

            with (
                mock.patch.object(
                    runtime,
                    "finalization_task_dir",
                    return_value=archived,
                ),
                mock.patch.object(runtime, "task_dir_is_archived", return_value=True),
                mock.patch.object(runtime, "load_config", return_value={}),
                mock.patch.object(
                    runtime,
                    "current_head",
                    return_value=transaction["commit"],
                ),
                mock.patch.object(
                    runtime,
                    "closeout_optional_commit_blob_bytes",
                    side_effect=committed_blob,
                ),
                mock.patch.object(
                    runtime,
                    "validate_closeout_plan",
                    side_effect=lambda value: value,
                ),
                mock.patch.object(
                    runtime,
                    "resolve_committed_closeout_archive_transaction",
                    return_value=transaction,
                ),
                mock.patch.object(
                    runtime,
                    "finalization_archived_owner_results",
                    return_value=(publication, verification),
                ),
                mock.patch.object(
                    runtime,
                    "finalization_archived_published_facts",
                    return_value=(False, None),
                ),
                mock.patch.object(
                    runtime,
                    "finalization_publication_owner_result",
                    side_effect=AssertionError("active readiness was reopened"),
                ) as readiness,
                mock.patch.object(
                    runtime,
                    "finalization_verification_owner_result",
                    side_effect=AssertionError("archived #117 artifact was reopened"),
                ) as verification_owner,
                mock.patch.object(runtime, "create_pull_request") as create_pr,
                mock.patch.object(
                    runtime,
                    "execute_archive_metadata_transaction",
                ) as archive_transaction,
            ):
                context = runtime.finalization_preview_context(
                    root,
                    mock.Mock(include_finalization_gate=True),
                    public_input,
                )
            self.assertEqual(context["transaction_state"], "archived")
            self.assertEqual(context["publication"], publication)
            readiness.assert_not_called()
            verification_owner.assert_not_called()
            create_pr.assert_not_called()
            archive_transaction.assert_not_called()

    def test_selected_runtime_archived_transition_skips_gate_and_verifier_mutation(
        self,
    ) -> None:
        runtime = load_selected_runtime()
        plan_digest = "a" * 64
        active = ".trellis/tasks/07-31-119-combined-finish-family-integration"
        archive = (
            ".trellis/tasks/archive/2026-08/"
            "07-31-119-combined-finish-family-integration"
        )
        plan = {
            "plan_digest": plan_digest,
            "task": {"active_locator": active, "archive_locator": archive},
            "git": {"branch_review_commit": "b" * 40},
            "marketplace": {"required": True},
        }
        public_input = {
            "profile": "same_plan_resume",
            "mode": "workflow",
            "task_ref": active,
            "plan_ref": f"closeout-plan:{plan_digest}",
        }
        context = {
            "task_dir": Path("unused"),
            "task_context": None,
            "prepared": None,
            "plan": plan,
            "plan_ref": public_input["plan_ref"],
            "transaction_state": "archived",
            "published_transition_complete": False,
            "publication": {"owner_status": "current"},
            "publication_status": "current",
            "publication_stale_reason": None,
            "verification": (
                {"source": "committed-finalization-gate"},
                {"status": "ok", "typed_exit": "verified"},
            ),
            "facts": {"transaction_state": "archived"},
            "current_facts_sha256": "c" * 64,
        }
        gate = {
            "route": {
                "typed_exit": "published",
                "consumer": runtime.FINALIZATION_CONSUMERS["published"],
                "output": runtime.FINALIZATION_EXECUTOR_OUTPUT_MARKER,
            }
        }
        reviewed = {
            "review": {
                "status": "passed",
                "summary": "The committed recovery is ready.",
                "evidence_refs": ["publication:current"],
            },
            "route": gate["route"],
            "supersedes_gate_ref": "task-finalization-gate:committed",
        }
        args = argparse.Namespace(
            root=None,
            input="unused-input.json",
            review_input="unused-review.json",
            gate=None,
            dry_run=False,
        )
        with tempfile.TemporaryDirectory(prefix="guru-finish-transition-") as temporary:
            root = Path(temporary)
            archived = root / archive
            archived.mkdir(parents=True)
            gate_path = archived / runtime.TASK_FINALIZATION_GATE_ARTIFACT
            gate_path.write_text("committed gate bytes\n", encoding="utf-8")
            committed_bytes = gate_path.read_bytes()
            context["task_dir"] = archived
            args.root = str(root)
            published_gate = {
                "route": {
                    "output": {
                        "exit_id": "published",
                        "task_ref": archive,
                        "pr_number": 166,
                        "pr_url": "https://github.com/castbox/guru-trellis/pull/166",
                    }
                }
            }
            finish_result = {
                "archived_task_dir": str(archived),
                "publish": {
                    "pr": {
                        "number": 166,
                        "url": "https://github.com/castbox/guru-trellis/pull/166",
                    }
                },
            }
            with (
                mock.patch.object(
                    runtime,
                    "finalization_public_input",
                    return_value=(public_input, "unused-input.json"),
                ),
                mock.patch.object(
                    runtime,
                    "finalization_semantic_review_input",
                    return_value=reviewed,
                ),
                mock.patch.object(
                    runtime,
                    "finalization_preview_context",
                    return_value=context,
                ),
                mock.patch.object(runtime, "finalization_validate_route"),
                mock.patch.object(
                    runtime,
                    "finalization_gate_schema",
                    return_value={},
                ),
                mock.patch.object(
                    runtime,
                    "skill_json_schema_validation_errors",
                    return_value=[],
                ),
            ):
                recorded = runtime.cmd_record_finalization_gate(args)
            self.assertEqual(recorded["typed_exit"], "published")
            self.assertEqual(gate_path.read_bytes(), committed_bytes)

            with (
                mock.patch.object(
                    runtime,
                    "finalization_public_input",
                    return_value=(public_input, "unused-input.json"),
                ),
                mock.patch.object(
                    runtime,
                    "finalization_gate_input",
                    return_value=(gate, gate_path),
                ),
                mock.patch.object(
                    runtime,
                    "check_finalization_gate_result",
                    return_value=(gate, context),
                ),
                mock.patch.object(
                    runtime,
                    "cmd_finish_work",
                    return_value=finish_result,
                ) as finish,
                mock.patch.object(
                    runtime,
                    "finalization_gate_with_published_output",
                    return_value=published_gate,
                ),
            ):
                transitioned = runtime.cmd_execute_finalization_transition(args)
            self.assertEqual(transitioned["output"]["pr_number"], 166)
            self.assertIsNone(getattr(finish.call_args.args[0], "external_verification", None))
            self.assertEqual(gate_path.read_bytes(), committed_bytes)

    def test_13_public_exits_have_unique_consumers_and_private_fields_stay_private(
        self,
    ) -> None:
        self.assertEqual(sum(len(exits) for exits in FINISH_EXITS.values()), 13)
        self.assertEqual(set(EXPECTED_CONSUMERS), {
            (skill_id, exit_id)
            for skill_id, exits in FINISH_EXITS.items()
            for exit_id in exits
        })
        for skill_id, expected_exits in FINISH_EXITS.items():
            interface = read_json(package(skill_id) / "interface.json")
            exits = interface["external_exits"]
            self.assertEqual({item["id"] for item in exits}, expected_exits)
            self.assertEqual(len(exits), len(expected_exits))
            outputs = interface["public_contracts"]["outputs"]
            projections = interface["public_contracts"]["projections"]
            consumers = interface["public_contracts"]["consumer_inputs"]
            for exit_id in expected_exits:
                with self.subTest(skill=skill_id, exit=exit_id):
                    external = [item for item in exits if item["id"] == exit_id]
                    output = [item for item in outputs if item["exit_id"] == exit_id]
                    projection = [
                        item for item in projections if item["exit_id"] == exit_id
                    ]
                    self.assertEqual(len(external), 1)
                    self.assertEqual(len(output), 1)
                    self.assertEqual(len(projection), 1)
                    consumer = [
                        item for item in consumers
                        if item["id"] == projection[0]["consumer_input_id"]
                    ]
                    self.assertEqual(len(consumer), 1)
                    self.assertEqual(
                        (
                            external[0]["consumer"]["kind"],
                            external[0]["consumer"]["id"],
                        ),
                        EXPECTED_CONSUMERS[(skill_id, exit_id)],
                    )
                    self.assertEqual(
                        external[0]["consumer"], consumer[0]["consumer"],
                    )
                    example = read_json(
                        package(skill_id) / output[0]["example"]["path"]
                    )
                    schema = read_json(
                        package(skill_id) / output[0]["schema"]["path"]
                    )
                    self.assertEqual(example["exit_id"], exit_id)
                    self.assertFalse(PRIVATE_FIELDS & set(example))
                    branches = output_object_branches(schema)
                    self.assertTrue(branches)
                    for branch in branches:
                        self.assertFalse(
                            branch.get("additionalProperties", True)
                        )
                        self.assertFalse(
                            PRIVATE_FIELDS & set(branch["properties"])
                        )

    def test_workflow_keeps_51_production_exits_28_targets_and_six_route_groups(
        self,
    ) -> None:
        rows = workflow_exits()
        production_rows = [
            row for row in rows if row.get("skill") != "guru-example-action"
        ]
        self.assertEqual(len(production_rows), 51)
        targets = set(
            re.findall(
                r'<!-- guru-(?:workflow|stop)-target: \{"id":"([^"]+)"\} -->',
                WORKFLOW.read_text(encoding="utf-8"),
            )
        )
        self.assertEqual(len(targets), 28)
        finish_rows: dict[tuple[str, str], list[dict[str, Any]]] = {}
        for row in rows:
            key = (row["skill"], row["exit"])
            if key in EXPECTED_CONSUMERS:
                finish_rows.setdefault(key, []).append(row)
        self.assertEqual(set(finish_rows), set(EXPECTED_CONSUMERS))
        for key, expected in EXPECTED_CONSUMERS.items():
            self.assertEqual(len(finish_rows[key]), 1, key)
            consumer = finish_rows[key][0]["consumer"]
            self.assertEqual((consumer["kind"], consumer["id"]), expected)
        self.assertEqual(len(ROUTE_GROUPS), 6)
        for group, edges in ROUTE_GROUPS.items():
            with self.subTest(group=group):
                self.assertTrue(edges)
                self.assertTrue(all(edge in finish_rows for edge in edges))

    def test_guru_entries_are_equal_thin_managed_routes(self) -> None:
        canonical_root = (
            REPO / "trellis/presets/guru-team/overlays"
            if EXECUTION_MODE == "source"
            else None
        )
        installed_payloads: list[bytes] = []
        for relative in GURU_ENTRIES:
            path = REPO / relative
            self.assertTrue(path.is_file(), relative)
            self.assertFalse(path.is_symlink(), relative)
            text = path.read_text(encoding="utf-8")
            self.assertIn("guru-team-overlay: v1", text)
            self.assertIn(".trellis/workflow.md", text)
            for skill_id in FINISH_EXITS:
                self.assertIn(skill_id, text)
            self.assertIn("not user choices", text)
            self.assertIn("Do not add a routine confirmation", text)
            self.assertNotIn("finish-work.sh", text)
            self.assertNotIn("--expected-plan-digest", text)
            installed_payloads.append(path.read_bytes())
            if canonical_root is not None:
                self.assertEqual(
                    path.read_bytes(), (canonical_root / relative).read_bytes(),
                )
        self.assertEqual(len(set(installed_payloads)), 1)

    def test_terminal_corpus_is_equal_across_runtime_and_platform_discovery(
        self,
    ) -> None:
        canonical = package("guru-finalize-task") / "evals"
        roots = [
            SKILLS_ROOT / "packages/guru-finalize-task/evals",
            REPO / ".agents/skills/guru-finalize-task/evals",
            REPO / ".codex/skills/guru-finalize-task/evals",
            REPO / ".claude/skills/guru-finalize-task/evals",
            REPO / ".cursor/skills/guru-finalize-task/evals",
        ]
        expected = tree_bytes(canonical)
        cases = {
            item["id"]: item
            for item in read_json(canonical / "evals.json")["evals"]
        }
        for case_id, (profile, facts_path, recipe) in TERMINAL_CASES.items():
            self.assertIn(case_id, cases)
            self.assertEqual(cases[case_id]["expected_exit"], "published")
            self.assertEqual(cases[case_id]["input_profile_id"], profile)
            facts = read_json(package("guru-finalize-task") / facts_path)
            self.assertEqual(facts["owner_staging"]["recipe"], recipe)
        for root in roots:
            with self.subTest(root=root):
                self.assertTrue(root.is_dir())
                self.assertEqual(tree_bytes(root), expected)

    def test_terminal_cases_execute_through_shared_public_wrapper(self) -> None:
        with tempfile.TemporaryDirectory(prefix="guru-finish-terminal-") as temporary:
            for case_id in TERMINAL_CASES:
                with self.subTest(case=case_id):
                    process = subprocess.run(
                        [
                            str(EVAL_RUNNER), "--root", str(REPO),
                            "--mode", EXECUTION_MODE,
                            "--skill", "guru-finalize-task",
                            "--adapter", "shared", "--case", case_id,
                            "--run-root", str(Path(temporary) / case_id),
                            "--json",
                        ],
                        cwd=REPO,
                        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        check=False,
                    )
                    self.assertEqual(process.returncode, 0, process.stderr)
                    result = json.loads(process.stdout)
                    self.assertEqual(result["status"], "passed", result)
                    self.assertEqual(
                        result["cases"][0]["actual_exit"], "published",
                    )

    @unittest.skipUnless(EXECUTION_MODE == "source", "source ownership assertion")
    def test_legacy_finish_tombstones_remain_frozen_without_119_blocker(
        self,
    ) -> None:
        inventory = read_json(
            REPO / "trellis/presets/guru-team/ownership/upstream-ownership.json"
        )
        legacy = [
            entry
            for entry in inventory["legacy_entries"]
            if entry["replacement_owners"]
            == [
                "guru-review-task-publication",
                "guru-verify-extension-installation",
                "guru-finalize-task",
            ]
        ]
        self.assertEqual(len(legacy), 5)
        overlay_root = REPO / "trellis/presets/guru-team/overlays"
        for entry in legacy:
            path = overlay_root / entry["path"]
            self.assertFalse(path.exists())
            self.assertEqual(entry["category"], "upstream_owned")
            self.assertEqual(entry["migration_state"], "removed")
            self.assertNotIn("current_payload_sha256", entry)
            self.assertIn(
                entry["baseline_sha256"], entry["migration_payload_sha256s"],
            )
            self.assertEqual(entry["blocking_issues"], [])
            self.assertEqual(entry["removal_issue"], 132)
            self.assertEqual(
                entry["dogfood_status"], "removed_with_audit_history",
            )
            self.assertEqual(
                entry["target_business_repo_status"], "no_longer_installed",
            )
        legacy_paths = {entry["path"] for entry in inventory["legacy_entries"]}
        claims = {
            claim["path"]: claim for claim in inventory["managed_path_claims"]
        }
        for relative in GURU_ENTRIES:
            self.assertNotIn(relative, legacy_paths)
            self.assertEqual(claims[relative]["category"], "guru_owned")
            self.assertEqual(claims[relative]["covered_by_legacy_paths"], [])


if __name__ == "__main__":
    unittest.main()
