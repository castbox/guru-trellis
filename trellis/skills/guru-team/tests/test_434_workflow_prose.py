"""Static regression for the canonical #434 lifecycle wording."""

from pathlib import Path
import unittest


WORKFLOW = Path(__file__).resolve().parents[4] / "trellis/workflows/guru-team/workflow.md"
SPEC = Path(__file__).resolve().parents[4] / "trellis/presets/guru-team/spec/workflow"
PROJECT_INDEX = Path(__file__).resolve().parents[4] / ".trellis/spec/workflow/index.md"
INSTALLER_SPEC = Path(__file__).resolve().parents[4] / ".trellis/spec/preset/installer.md"
PACKAGES = Path(__file__).resolve().parents[1] / "packages"


def section(text: str, heading: str) -> str:
    return text.split(heading + "\n", 1)[1].split("\n### ", 1)[0]


class WorkflowLifecycleProseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")

    def test_external_work_item_owner_is_post_completion_closure(self) -> None:
        prose = section(self.workflow, "### External work item and closure")
        for expected in (
            "Refs-only PR payload",
            "`guru-review-task-completion` alone reviews the whole accepted scope",
            "`completed` exit enters `guru-complete-task-closure`",
            "`no_mutation`",
            "bookkeeping PR also\nhas no Issue-closing keyword",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, prose)
        self.assertNotIn("Publication is the sole semantic owner", prose)
        self.assertNotIn("Finalizer only executes", prose)

    def test_phase_and_manual_routes_do_not_reintroduce_old_chain(self) -> None:
        phase = section(self.workflow, "## Phase Index")
        manual = section(self.workflow, "### Manual Git/GitHub Operations")
        self.assertIn("Delivery cycles, Completion, Closure, Finish, Cleanup", phase)
        self.assertIn("Delivery, Completion, Closure, Finish and archive state", manual)
        self.assertIn("a separate manual operation cannot produce their results", manual)
        self.assertNotIn("Publication, Finalizer, Merge, and archive contracts", manual)

    def test_finish_handoff_runs_cleanup_outside_deletion_targets(self) -> None:
        completion = section(self.workflow, "#### 3.7 Completion, Closure and Finish")
        self.assertIn("retained checkout of the same Git common-dir", completion)
        self.assertIn("not among the sealed deletion targets", completion)
        self.assertIn("move the invocation to the retained checkout", completion)

    def test_installed_workflow_contract_selects_current_graph(self) -> None:
        contract = (SPEC / "workflow-contract.md").read_text(encoding="utf-8")
        current = contract.split("## Integrated Public Graph\n", 1)[1].split("\n## ", 1)[0]
        self.assertIn("34 active packages", current)
        self.assertIn("Delivery Review\n-> Delivery Publish -> Delivery Merge -> whole-task Completion", current)
        self.assertIn("no current production edge", current)
        self.assertNotIn("`guru-review-branch:passed -> guru-review-task-publication`", current)

    def test_session_data_contract_uses_current_identity_owners(self) -> None:
        contract = (SPEC / "data-contracts.md").read_text(encoding="utf-8")
        current = contract.split("### Task identity and session binding (#443, selected by #434)\n", 1)[1].split("\n## ", 1)[0]
        self.assertIn("TaskId-to-TaskRef resolution", current)
        self.assertIn("C3 checkout and C4 branch/ownership readers", current)
        self.assertNotIn("guru-create-task-workspace", current)

    def test_project_spec_index_routes_to_current_lifecycle(self) -> None:
        index = PROJECT_INDEX.read_text(encoding="utf-8")
        current = index.split("## Local Architecture\n", 1)[1].split("\n## Required Validation", 1)[0]
        self.assertIn("34 active packages, 155 exits", current)
        self.assertIn("`guru-review-task-delivery`", current)
        self.assertIn("`guru-review-task-completion`", current)
        self.assertIn("pinned-old history only", current)
        self.assertNotIn("`guru-finalize-task` is the active", current)

    def test_intake_package_spec_retains_old_workspace_as_history(self) -> None:
        contract = (SPEC / "skill-package-contract.md").read_text(encoding="utf-8")
        intake = contract.split("### Intake Activation: Current Split And Pinned-Old Snapshot\n", 1)[1].split("\n### ", 1)[0]
        self.assertIn("six-package/23-exit count and the Workspace consumer are pinned-old-only", intake)
        self.assertIn("`guru-task-intake-router`", intake)
        current = contract.split("`guru-task-intake-router` consumes the public `ready`\ntransition", 1)[1].split("\n## ", 1)[0]
        self.assertIn("`guru-create-issue`", current)
        self.assertIn("`guru-create-task`", current)
        self.assertIn("## Historical Task Workspace Package (Pinned-Old-Only)", contract)

    def test_quality_guide_selects_current_graph_and_pins_old_counts(self) -> None:
        guide = (SPEC / "quality-guidelines.md").read_text(encoding="utf-8")
        current = guide.split("## Required Checks\n", 1)[1].split(
            "### Retired #389 Task Workspace Fixture (historical only)", 1
        )[0]
        self.assertIn("34 active Skills, 155 external exits, and 104 commands", current)
        self.assertIn("33 invokes and 153 exits", current)
        self.assertIn("six-package/23-exit Workspace graph is pinned-old", current)
        self.assertIn("32/142/102 and 22/98 counts are pinned-old", current)
        self.assertNotIn("workspace `created` cannot be serialized", current)
        entire_guide = guide.split("## Normal Scenario Qualification Quality\n", 1)[0]
        self.assertNotIn("32-Skill/142-exit/102-command current", entire_guide)
        self.assertIn("34-Skill/155-exit/104-command current package closure", entire_guide)

    def test_current_installer_and_quality_guidance_exclude_retired_entries(self) -> None:
        guide = (SPEC / "quality-guidelines.md").read_text(encoding="utf-8")
        intake = guide.split("When standard Intake is selected", 1)[1].split(
            "Search before editing", 1
        )[0]
        self.assertIn("The retired `prepare-task.sh` is not installed", intake)
        self.assertNotIn("compatibility-only `.trellis/guru-team/scripts/bash/prepare-task.sh", intake)
        python_gate = guide.split("## Managed Python Runtime Gate", 1)[1].split(
            "## Retired Closeout", 1
        )[0]
        self.assertIn("Retired `finish-work.sh` and `prepare-task.sh` must be absent", python_gate)
        self.assertNotIn("including installed `finish-work.sh`", python_gate)

        installer = INSTALLER_SPEC.read_text(encoding="utf-8")
        intake = installer.split("## Current Intake Package Activation", 1)[1].split(
            "## Branch Review Package Activation", 1
        )[0]
        self.assertIn("`guru-create-issue` and\n`guru-create-task` owners", intake)
        self.assertIn("The retired Workspace package", installer)
        self.assertNotIn("active consumer\n`guru-create-task-workspace`", intake)
        current = installer.split("## Current Delivery And Terminal Installation", 1)[1].split(
            "### Pinned-Old Finalizer Recovery", 1
        )[0]
        self.assertIn("Delivery/Completion graph", current)
        self.assertIn("## Retired Task Finalization Package Activation (pinned-old only)", installer)
        self.assertIn("34-Skill/155-package-exit/104-command", installer)
        self.assertIn("install one current Task Delivery graph", installer)
        self.assertNotIn("install only current Finalizer and Publication", installer)
        self.assertNotIn("The business Finalizer may consume this current manifest", installer)
        self.assertIn("Completion's Interface 1.7", installer)

    def test_retired_workspace_fixture_is_history_not_current_instructions(self) -> None:
        guide = (SPEC / "quality-guidelines.md").read_text(encoding="utf-8")
        historical = section(guide, "### Retired #389 Task Workspace Fixture (historical only)")
        normalized = " ".join(historical.split())
        self.assertIn("complete pinned-old graph", normalized)
        self.assertIn("do not define current Intake behavior", normalized)
        self.assertIn("No old Workspace result is synthesized", historical)
        for obsolete in ("Route tests require", "source-checkout matrix must", "tests use a real remote"):
            self.assertNotIn(obsolete, historical)

    def test_active_terminal_skills_do_not_claim_future_activation(self) -> None:
        for skill in ("guru-finish-task", "guru-complete-task-closure", "guru-reactivate-task", "guru-cleanup-task-resources"):
            with self.subTest(skill=skill):
                prose = (PACKAGES / skill / "SKILL.md").read_text(encoding="utf-8")
                self.assertNotIn("not active until the separate graph activation", prose)
                self.assertNotIn("downstream Finish and workflow projection migration belong to", prose)
                self.assertNotIn("Production router activation belongs to #434", prose)
                self.assertNotIn("normal route remains owned by #434 activation", prose)


if __name__ == "__main__":
    unittest.main()
