"""Static regression for the canonical #434 lifecycle wording."""

from pathlib import Path
import unittest


WORKFLOW = Path(__file__).resolve().parents[4] / "trellis/workflows/guru-team/workflow.md"
SPEC = Path(__file__).resolve().parents[4] / "trellis/presets/guru-team/spec/workflow"
PROJECT_INDEX = Path(__file__).resolve().parents[4] / ".trellis/spec/workflow/index.md"


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


if __name__ == "__main__":
    unittest.main()
