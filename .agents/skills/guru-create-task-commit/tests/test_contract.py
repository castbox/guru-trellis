from __future__ import annotations

import json
import hashlib
import unittest
from pathlib import Path


class TaskCommitPackageContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.package = Path(__file__).resolve().parents[1]
        self.interface = json.loads((self.package / "interface.json").read_text(encoding="utf-8"))

    def test_identity_modes_and_exits(self) -> None:
        self.assertEqual(self.interface["id"], "guru-create-task-commit")
        self.assertEqual(
            self.interface["modes"]["workflow"]["entry_precondition_ids"],
            self.interface["modes"]["standalone"]["entry_precondition_ids"],
        )
        self.assertEqual(
            [item["id"] for item in self.interface["external_exits"]],
            ["committed", "revision-required", "blocked"],
        )

    def test_skill_triggers_and_thin_wrappers(self) -> None:
        skill = (self.package / "SKILL.md").read_text(encoding="utf-8")
        for phrase in ("creating a task commit", "committing Phase 2 changes", "finding fix", "revision commit"):
            self.assertIn(phrase, skill)
        for name in ("check-task-commit-plan.sh", "create-task-commit.sh"):
            wrapper = (self.package / "scripts" / name).read_text(encoding="utf-8")
            self.assertIn("exec \"$RUNTIME\"", wrapper)
            self.assertNotIn("validate_commit_message", wrapper)
            self.assertNotIn("git add", wrapper)

    def test_example_message_and_plan_digests_match(self) -> None:
        plan = json.loads((self.package / "examples/task-commit-plan.json").read_text(encoding="utf-8"))
        message = plan["message"]["bytes"].encode("utf-8")
        self.assertEqual(hashlib.sha256(message).hexdigest(), plan["message"]["sha256"])
        normalized = json.loads(json.dumps(plan, ensure_ascii=False))
        normalized["freshness"]["plan_digest"] = ""
        encoded = json.dumps(normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        self.assertEqual(hashlib.sha256(encoded).hexdigest(), plan["freshness"]["plan_digest"])


if __name__ == "__main__":
    unittest.main()
