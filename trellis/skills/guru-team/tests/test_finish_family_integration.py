from __future__ import annotations

import argparse
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
        reviewed_head = "b" * 40
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
                "reviewed_work_head": reviewed_head,
            },
            "marketplace": {"required": True},
        }
        public_input = {
            "profile": "same_plan_resume",
            "mode": "workflow",
            "task_ref": active,
            "plan_ref": f"closeout-plan:{plan_digest}",
            "recovery_intent": "Resume the same immutable transaction.",
            "recovery_context": "The compact archive is already committed.",
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
            self.assertEqual(len(retained), runtime.CLOSEOUT_ARCHIVE_MAX_ARTIFACTS)
            self.assertFalse((archived / runtime.PR_READINESS_ARTIFACT).exists())

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
                    "finalization_verification_augmentation_plan",
                    return_value=plan,
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
                mock.patch.object(
                    runtime,
                    "commit_closeout_evidence_metadata",
                ) as evidence_commit,
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
            evidence_commit.assert_not_called()

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
            "git": {"reviewed_work_head": "b" * 40},
            "marketplace": {"required": True},
        }
        public_input = {
            "profile": "same_plan_resume",
            "mode": "workflow",
            "task_ref": active,
            "plan_ref": f"closeout-plan:{plan_digest}",
            "recovery_intent": "Resume the same immutable transaction.",
            "recovery_context": "The compact archive is already committed.",
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
            "confirmation": {
                "status": "not_required",
                "confirmed_plan_digest": plan_digest,
                "summary": "The immutable plan was already confirmed.",
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
                    "finalization_marketplace_verification_compatibility_projection",
                    side_effect=AssertionError("archived #117 evidence was reopened"),
                ) as projection,
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
            projection.assert_not_called()
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

    def test_workflow_keeps_52_production_exits_29_targets_and_six_route_groups(
        self,
    ) -> None:
        rows = workflow_exits()
        production_rows = [
            row for row in rows if row.get("skill") != "guru-example-action"
        ]
        self.assertEqual(len(production_rows), 52)
        targets = set(
            re.findall(
                r'<!-- guru-(?:workflow|stop)-target: \{"id":"([^"]+)"\} -->',
                WORKFLOW.read_text(encoding="utf-8"),
            )
        )
        self.assertEqual(len(targets), 29)
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
    def test_legacy_finish_payloads_remain_frozen_compatibility_without_119_blocker(
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
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(),
                entry["current_payload_sha256"],
            )
            self.assertEqual(entry["blocking_issues"], [])
            self.assertEqual(entry["removal_issue"], 132)
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
