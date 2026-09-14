"""Static contract regression only; not evidence of actual Agent execution."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SKILLS = ROOT / "trellis/skills/guru-team"
WORKFLOW = ROOT / "trellis/workflows/guru-team/workflow.md"
HEADING = "### Manual Git/GitHub Operations"
REFERENCE = ".trellis/workflow.md#manual-gitgithub-operations"
OWNERS = (
    "guru-create-task-commit",
    "guru-review-task-publication",
    "guru-finalize-task",
    "guru-merge-task-pr",
)
ENTRIES = (
    ".codex/prompts/guru-finish-work.md",
    ".claude/commands/guru/finish-work.md",
    ".cursor/commands/guru-finish-work.md",
)


class ManualGitFallbackContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")
        cls.section = cls.workflow.split(HEADING + "\n", 1)[1].split("\n### ", 1)[0]
        cls.normalized = " ".join(cls.section.split())

    def test_failure_reports_live_unknowns_without_identity_repair(self) -> None:
        for phrase in (
            "workflow-state injection, session/task routing",
            "hook, checkpoint, or wrapper",
            "Stop that automatic invocation chain",
            "failed step, original error (with secrets redacted)",
            "known repo/task/worktree/branch/HEAD/Issue/PR",
            "mark unreadable facts `unknown`",
            "not evidence of `no_task`",
            "Do not enter new Intake, switch to task-free, rebuild mappings",
            "repair hooks/runtime, or manufacture checkpoints",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.normalized)

    def test_each_operation_requires_its_own_current_confirmation(self) -> None:
        for phrase in (
            "An automatic stop does not prohibit",
            "For each operation, reread its live facts",
            "commands/payload, expected result, and side effects",
            "confirmation for this operation in the current dialogue before executing",
            "An earlier operation's confirmation does not authorize the next one",
            "requires a fresh display and confirmation",
            "Before execution, a changed target, HEAD, payload, or side-effect set",
            "A new commit SHA produced by the confirmed operation is an expected result to verify",
            "not a reason to reconfirm that same operation",
            "server-enforced remote rules still apply",
            "Never persist authorization or its process",
            "unrelated Guru residue alone does not block it",
            "Never chain later operations implicitly",
            "does not bypass the operation's own checks or the existing release contract",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.normalized)
        rows = {
            cells[0]: cells[1:]
            for line in self.section.splitlines()
            if line.startswith("| ")
            for cells in [[cell.strip() for cell in line.strip("|").split("|")]]
        }
        expected = {
            "commit": ("exact stage paths", "parents/tree/message", "Do not push"),
            "push": ("refspec", "remote HEAD", "do not create a PR"),
            "PR creation/update": ("Chinese title/body", "closing-keyword", "do not merge"),
            "merge": (
                "expected head", "GitHub-returned merge eligibility/checks", "merge method",
                "Do not add Ruleset or branch-protection reads as prerequisites",
                "without calling Issue closure",
            ),
            "Issue closure": ("delivery evidence", "actual closed/open state"),
            "tag/Release": ("existing release contract", "tag target", "never publish upstream"),
            "cleanup": ("uncommitted contents", "references/use state", "only listed resources"),
        }
        self.assertEqual(set(rows) - {"Operation", "---"}, set(expected))
        for operation, phrases in expected.items():
            with self.subTest(operation=operation):
                self.assertEqual(len(rows[operation]), 2)
                for phrase in phrases:
                    self.assertIn(phrase, " ".join(rows[operation]))

    def test_operation_result_never_claims_lifecycle_completion(self) -> None:
        for phrase in (
            "**Git/GitHub result**", "**Workflow residue**",
            "runtime, Finalizer and archive state",
            "Do not write Phase 2, Branch Review, Publication, Finalizer, Merge or archive completion markers",
            "not automatic Guru re-entry",
            "original current entry preconditions and declared routes",
            "not a new workflow node, Skill, typed exit, executor, or recovery path",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.normalized)

    def test_direct_consumers_reference_one_global_owner(self) -> None:
        self.assertEqual(self.workflow.count(HEADING), 1)
        for owner in OWNERS:
            text = (SKILLS / "packages" / owner / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(owner=owner):
                self.assertIn(REFERENCE, text)
                self.assertNotIn("| Operation |", text)
        entries = [
            (ROOT / "trellis/presets/guru-team/overlays" / path).read_text(encoding="utf-8")
            for path in ENTRIES
        ]
        self.assertEqual(len(set(entries)), 1)
        self.assertIn(REFERENCE, entries[0])
        self.assertNotIn("| Operation |", entries[0])
        no_task = self.workflow.split("[workflow-state:no_task]", 1)[1].split(
            "[/workflow-state:no_task]", 1
        )[0]
        self.assertIn("Manual Git/GitHub Operations", no_task)
        self.assertIn("missing context is not proof of no task", no_task)

    def test_existing_public_inventory_is_unchanged(self) -> None:
        registry = json.loads((SKILLS / "registry.json").read_text(encoding="utf-8"))
        active = [row for row in registry["skills"] if row["state"] == "active"]
        self.assertEqual(len(active), 23)
        exits = commands = 0
        for row in active:
            interface = json.loads((SKILLS / row["interface"]).read_text(encoding="utf-8"))
            exits += len(interface["external_exits"])
            package_commands = SKILLS / row["package"] / "commands.json"
            commands += len(json.loads(package_commands.read_text(encoding="utf-8"))["commands"])
        self.assertEqual((exits, commands), (97, 78))
        self.assertEqual(self.workflow.count("<!-- guru-skill-invoke:"), 22)
        self.assertEqual(self.workflow.count("<!-- guru-skill-exit:"), 95)
        self.assertEqual(self.workflow.count("<!-- guru-workflow-target:"), 35)
        self.assertEqual(self.workflow.count("<!-- guru-stop-target:"), 24)


if __name__ == "__main__":
    unittest.main()
