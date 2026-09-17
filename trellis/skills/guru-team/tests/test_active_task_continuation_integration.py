from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
WORKFLOW = REPO / "trellis/workflows/guru-team/workflow.md"
UPSTREAM_CANDIDATE = "43fffc170927c85d9f7fc106cc5a059e80d4530b"
EXTRACTOR_PATH = ".trellis/scripts/common/continuation_contract.py"


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


if __name__ == "__main__":
    unittest.main()
