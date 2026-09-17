from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
WORKFLOW = REPO / "trellis/workflows/guru-team/workflow.md"
UPSTREAM_CANDIDATE = "43fffc170927c85d9f7fc106cc5a059e80d4530b"
EXTRACTOR_PATH = ".trellis/scripts/common/continuation_contract.py"

FORMAL_WRAPPER_CASES = (
    (
        "activation failure stops before mutation",
        "trellis/presets/guru-team/scripts/python/test_start_task_wrapper.py",
        "test_wrapper_blocks_before_upstream_task_start_when_boundary_fails",
    ),
    (
        "activation output loss rematerializes without repeating mutation",
        "trellis/presets/guru-team/scripts/python/test_start_task_wrapper.py",
        "test_recovery_rematerializes_success_without_repeating_upstream_start",
    ),
    (
        "Phase 2 lost output rematerializes only after the checker passes",
        "trellis/skills/guru-team/packages/guru-check-task/tests/test_runtime.py",
        "test_passed_output_can_be_rematerialized_only_after_fresh_checker_success",
    ),
    (
        "Task Commit stdout loss recovers the same commit once",
        "trellis/skills/guru-team/packages/guru-create-task-commit/tests/test_happy_path.py",
        "test_success_and_stdout_loss_recovery_execute_once",
    ),
    (
        "Branch Review adjacent output retires and cannot be reconstructed",
        "trellis/skills/guru-team/packages/guru-review-branch/tests/test_contract.py",
        "test_passed_record_check_invoke_retires_and_rejects_repeat",
    ),
    (
        "Branch Review implementation route remains recoverable",
        "trellis/skills/guru-team/packages/guru-review-branch/tests/test_contract.py",
        "test_nonterminal_record_and_invoke_are_idempotent_and_retain",
    ),
    (
        "Task Commit and Publication use their formal public invocation paths",
        "trellis/skills/guru-team/tests/test_closeout_happy_path_integration.py",
        "test_supported_internal_and_wrapper_routes_are_equivalent",
    ),
    (
        "Publication failure retains its current owner checkpoint",
        "trellis/skills/guru-team/packages/guru-review-task-publication/tests/test_contract.py",
        "test_public_wrapper_keeps_checkpoint_when_checker_or_projection_fails",
    ),
    (
        "confirmation is consumed once and mapped transitions stop at the next side effect",
        "trellis/skills/guru-team/tests/test_finish_family_integration.py",
        "test_confirm_continue_drives_actual_loaded_closeout_once",
    ),
)


def git_show(spec: str) -> str:
    return subprocess.run(
        ["git", "show", spec],
        cwd=REPO,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    ).stdout


def load_upstream_extractor(directory: Path):
    source = git_show(f"{UPSTREAM_CANDIDATE}:{EXTRACTOR_PATH}")
    path = directory / "continuation_contract.py"
    path.write_text(source, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("candidate_continuation_contract", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load exact upstream continuation extractor")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_formal_wrapper_case(test_path: str, test_name: str) -> subprocess.CompletedProcess[str]:
    environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    return subprocess.run(
        [sys.executable, "-m", "unittest", test_path, "-k", test_name],
        cwd=REPO,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env=environment,
    )


def run_upstream_prompt_hook(fixture: Path, prompt: str) -> str:
    hook = fixture / ".codex/hooks/inject-workflow-state.py"
    process = subprocess.run(
        [sys.executable, str(hook)],
        cwd=fixture,
        input=json.dumps(
            {
                "cwd": str(fixture),
                "session_id": "continuation-fixture",
                "prompt": prompt,
            }
        ),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    if process.returncode != 0:
        raise AssertionError(
            f"upstream prompt hook failed\nstdout:\n{process.stdout}\nstderr:\n{process.stderr}"
        )
    output = json.loads(process.stdout)
    return output["hookSpecificOutput"]["additionalContext"]


def markdown_table(body: str, heading: str) -> list[tuple[str, str]]:
    lines = body.splitlines()
    start = lines.index(heading)
    rows: list[tuple[str, str]] = []
    for line in lines[start + 1 :]:
        if line.startswith("#### "):
            break
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 2 or cells[0] in {
            "Bound status",
            "Current fact",
            "Stage/output state",
        }:
            continue
        if set(cells[0]) == {"-"}:
            continue
        rows.append((cells[0], cells[1]))
    return rows


class ActiveTaskContinuationIntegrationTests(unittest.TestCase):
    def test_exact_upstream_protocol_extracts_one_nonempty_guru_contract(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        lines = [line.strip() for line in workflow.splitlines()]
        self.assertEqual(lines.count("[trellis-continuation]"), 1)
        self.assertEqual(lines.count("[/trellis-continuation]"), 1)
        with tempfile.TemporaryDirectory(prefix="guru-continuation-") as temporary:
            extractor = load_upstream_extractor(Path(temporary))
            body = extractor.extract_continuation_contract(WORKFLOW)
        self.assertTrue(body.strip())
        self.assertEqual(body.count("### Guru active-task continuation"), 1)

    def test_closed_state_dispatch_covers_all_supported_families_and_invalid_stop(self):
        with tempfile.TemporaryDirectory(prefix="guru-continuation-state-") as temporary:
            body = load_upstream_extractor(Path(temporary)).extract_continuation_contract(
                WORKFLOW
            )
        rows = dict(markdown_table(body, "#### Closed state dispatch"))
        self.assertEqual(
            set(rows),
            {
                "`planning` or `planning-inline`",
                "`in_progress` or `in_progress-inline`",
                "`completed`",
                "anything else",
            },
        )
        self.assertEqual(
            rows["anything else"], "Stop at `invalid-task-state`."
        )

    def test_phase1_matrix_keeps_recovery_with_original_owners(self):
        with tempfile.TemporaryDirectory(prefix="guru-continuation-plan-") as temporary:
            body = load_upstream_extractor(Path(temporary)).extract_continuation_contract(
                WORKFLOW
            )
        rows = dict(markdown_table(body, "#### Phase 1 recovery matrix"))
        self.assertEqual(len(rows), 9)
        actions = "\n".join(rows.values())
        self.assertIn("`guru-create-task-workspace` recovery/rematerialization", actions)
        self.assertIn("`guru-review-contract-wording:planning_artifacts`", actions)
        self.assertIn(
            "`guru-maintain-architecture-baseline:task_impact_sync(stage=planning)`",
            actions,
        )
        self.assertIn("`guru-approve-task-plan`", actions)
        self.assertIn("`start-task.sh --mode initial <task-path>`", actions)
        self.assertIn("`start-task.sh --mode recovery <task-path>`", actions)
        recovery = rows[
            "Activation mutation succeeded but its result was lost and the exact task is already `in_progress`"
        ]
        self.assertIn("without calling `task.py start` again", recovery)

    def test_phase2_matrix_checks_before_rematerialization_and_freshly_reruns_failure(self):
        with tempfile.TemporaryDirectory(prefix="guru-continuation-phase2-") as temporary:
            body = load_upstream_extractor(Path(temporary)).extract_continuation_contract(
                WORKFLOW
            )
        rows = dict(markdown_table(body, "#### Phase 2-to-Finalizer recovery matrix"))
        self.assertEqual(len(rows), 9)
        phase2_loss = rows[
            "The `passed` DTO was lost but the producer checkpoint may still be current"
        ]
        self.assertLess(
            phase2_loss.index("`check-phase2-check`"),
            phase2_loss.index("`invoke-guru-check-task`"),
        )
        self.assertIn(
            "freshly rerun Phase 2 Architecture followed by `guru-check-task`",
            phase2_loss,
        )
        commit_loss = rows["Task Commit output was lost after its mutation"]
        for forbidden in ("second", "empty", "amended", "same-content"):
            self.assertIn(forbidden, commit_loss)
        self.assertIn(
            "complete current committed `origin/<base>...HEAD` range",
            rows[
                "Branch Review DTO is absent/stale/lost or its producer checkpoint retired"
            ],
        )
        self.assertIn(
            "live Issue/PR/payload authority",
            rows[
                "Publication DTO is absent/stale/lost or its producer checkpoint retired"
            ],
        )

    def test_active_state_breadcrumbs_only_delegate_to_the_continuation_contract(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        for status in (
            "planning",
            "planning-inline",
            "in_progress",
            "in_progress-inline",
            "completed",
        ):
            opening = f"[workflow-state:{status}]"
            closing = f"[/workflow-state:{status}]"
            body = workflow.split(opening, 1)[1].split(closing, 1)[0]
            self.assertIn("`[trellis-continuation]` block", body)
            self.assertNotIn("guru-approve-task-plan", body)
            self.assertNotIn("guru-check-task", body)
            self.assertNotIn("guru-review-branch", body)
            self.assertNotIn("guru-review-task-publication", body)

    def test_natural_language_prompts_converge_through_real_active_task_hook(self):
        with tempfile.TemporaryDirectory(prefix="guru-continuation-prompt-") as temporary:
            fixture = Path(temporary)
            scripts = fixture / ".trellis/scripts"
            scripts.mkdir(parents=True)
            shutil.copytree(REPO / ".trellis/scripts/common", scripts / "common")
            shutil.copy2(WORKFLOW, fixture / ".trellis/workflow.md")

            task = fixture / ".trellis/tasks/active-continuation"
            task.mkdir(parents=True)
            (task / "task.json").write_text(
                json.dumps(
                    {
                        "id": "active-continuation",
                        "status": "in_progress",
                    }
                ),
                encoding="utf-8",
            )
            sessions = fixture / ".trellis/.runtime/sessions"
            sessions.mkdir(parents=True)
            (sessions / "codex_continuation-fixture.json").write_text(
                json.dumps({"current_task": ".trellis/tasks/active-continuation"}),
                encoding="utf-8",
            )

            hook = fixture / ".codex/hooks/inject-workflow-state.py"
            hook.parent.mkdir(parents=True)
            hook.write_text(
                git_show(
                    f"{UPSTREAM_CANDIDATE}:.codex/hooks/inject-workflow-state.py"
                ),
                encoding="utf-8",
            )

            continue_context = run_upstream_prompt_hook(fixture, "继续")
            confirm_context = run_upstream_prompt_hook(fixture, "确认继续")

        self.assertEqual(continue_context, confirm_context)
        self.assertIn("Task: active-continuation (in_progress)", continue_context)
        self.assertIn("Load the current `[trellis-continuation]` block", continue_context)
        self.assertNotIn("[workflow-state:no_task]", continue_context)

    def test_formal_wrappers_execute_real_transition_and_recovery_fixtures(self):
        for label, test_path, test_name in FORMAL_WRAPPER_CASES:
            with self.subTest(case=label):
                result = run_formal_wrapper_case(test_path, test_name)
                self.assertEqual(
                    result.returncode,
                    0,
                    f"{label} failed\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
                )
                self.assertIn("Ran 1 test", result.stderr)
                self.assertIn("OK", result.stderr)


if __name__ == "__main__":
    unittest.main()
