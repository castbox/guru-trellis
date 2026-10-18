from __future__ import annotations

import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, RefResolver


ROOT = Path(__file__).resolve().parents[6]
PACKAGE = ROOT / "trellis/skills/guru-team/packages/guru-execute-task-free-change"
SKILLS = ROOT / "trellis/skills/guru-team"


class TaskFreeChangeContractTest(unittest.TestCase):
    def test_interface_and_examples_are_closed(self) -> None:
        interface = json.loads((PACKAGE / "interface.json").read_text())
        schema = json.loads((SKILLS / "schemas/skill-interface-1.4.schema.json").read_text())
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(interface)))
        self.assertEqual(interface["judgment_mode"], "semantic")
        self.assertEqual(
            [item["id"] for item in interface["external_exits"]],
            ["completed", "resume_active_task", "scope_change", "location_required", "reselect_mode", "explicit_choice_required", "blocked"],
        )
        for profile in interface["public_contracts"]["input"]["profiles"]:
            payload = json.loads((PACKAGE / profile["example"]["path"]).read_text())
            input_schema = json.loads((PACKAGE / profile["schema"]["path"]).read_text())
            self.assertEqual([], list(Draft202012Validator(input_schema).iter_errors(payload)))
        for output in interface["public_contracts"]["outputs"]:
            payload = json.loads((PACKAGE / output["example"]["path"]).read_text())
            output_schema = json.loads((PACKAGE / output["schema"]["path"]).read_text())
            self.assertEqual([], list(Draft202012Validator(output_schema).iter_errors(payload)))

    def test_selector_dto_stays_minimal_and_projects_as_authoring_seed(self) -> None:
        selector = SKILLS / "packages/guru-select-workflow-mode"
        schema = json.loads((selector / "schemas/public-task-free-output.schema.json").read_text())
        self.assertEqual(schema["required"], ["exit_id"])
        self.assertEqual(set(schema["properties"]), {"exit_id"})
        interface = json.loads((selector / "interface.json").read_text())
        consumer = next(item for item in interface["public_contracts"]["consumer_inputs"] if item["id"] == "task_free_input")
        self.assertEqual(consumer["contract"]["kind"], "skill_input_authoring_seed")
        self.assertEqual(consumer["contract"]["seed_fields"], ["selector_exit"])
        projection = next(item for item in interface["public_contracts"]["projections"] if item["exit_id"] == "task_free")
        self.assertEqual(projection["operation"], "rename")
        self.assertEqual(projection["mappings"], [{"source": "exit_id", "target": "selector_exit"}])

    def test_completed_requires_prewrite_edit_checks_and_postwrite_review(self) -> None:
        review = json.loads((PACKAGE / "examples/task-free-change-review.json").read_text())
        self.assertEqual(review["pre_write_review"]["status"], "suitable")
        self.assertTrue(review["completion_evidence"]["edited_paths"])
        self.assertTrue(any(item["status"] == "passed" for item in review["completion_evidence"]["targeted_checks"]))
        self.assertEqual(review["completion_evidence"]["post_write_review"]["status"], "passed")
        self.assertTrue(review["completion_evidence"]["unverified_boundaries"])
        self.assertEqual(review["ai_review_gate"]["status"], "passed")

        completed = json.loads((PACKAGE / "examples/public-completed-output.json").read_text())
        self.assertEqual(completed["edited_paths"], review["completion_evidence"]["edited_paths"])
        self.assertEqual(completed["validation_summary"]["overall_status"], "passed")
        self.assertEqual(completed["unverified_boundaries"], review["completion_evidence"]["unverified_boundaries"])

    def test_postwrite_expansion_requires_stop_and_remaining_write_evidence(self) -> None:
        schema = json.loads((PACKAGE / "schemas/task-free-change-review.schema.json").read_text())
        for origin, exit_id in (("automatic", "reselect_mode"), ("explicit", "explicit_choice_required")):
            owner = json.loads((PACKAGE / "examples/task-free-change-review.json").read_text())
            owner.update({"typed_exit": exit_id, "selection_origin": origin})
            owner.pop("completion_evidence")
            owner["target_paths"] = ["docs/guide.md", "docs/follow-up.md"]
            owner["evolution_evidence"] = {
                "write_state": "partial_edit",
                "edited_paths": ["docs/guide.md"],
                "expansion": {"kind": "scope_and_risk", "summary": "The partial edit revealed wider public impact."},
                "stop_after_detection": True,
                "remaining_writes_not_performed": [{"target_path": "docs/follow-up.md", "summary": "The planned follow-up edit was not performed."}],
                "targeted_checks": [{"command": "git diff --check -- docs/guide.md", "summary": "The partial diff has no whitespace errors.", "status": "passed"}],
            }
            self.assertEqual([], list(Draft202012Validator(schema).iter_errors(owner)))
            owner["evolution_evidence"].pop("remaining_writes_not_performed")
            self.assertTrue(list(Draft202012Validator(schema).iter_errors(owner)))

    def test_runtime_cannot_claim_completion_without_ai_authored_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            bad = Path(temp) / "owner.json"
            owner = json.loads((PACKAGE / "examples/task-free-change-review.json").read_text())
            owner.pop("completion_evidence")
            bad.write_text(json.dumps(owner))
            result = subprocess.run(
                [str(PACKAGE / "scripts/invoke.sh"), "--input", str(PACKAGE / "examples/public-selected-route-input.json"), "--owner-result", str(bad), "--json"],
                cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("schema_mismatch", result.stdout + result.stderr)

    def test_no_branch_protection_or_lifecycle_executor(self) -> None:
        text = "\n".join(path.read_text() for root in (PACKAGE / "runtime", PACKAGE / "scripts") for path in root.iterdir() if path.is_file())
        self.assertIsNone(re.search(r"branch[-_ ]protection|branches/.+/protection", text, re.IGNORECASE))
        for forbidden in ("git commit", "git push", "gh pr", "task.py", "subprocess"):
            self.assertNotIn(forbidden, text)

    def test_eval_corpus_owns_checkout_and_evolution_cases(self) -> None:
        corpus = json.loads((PACKAGE / "evals/evals.json").read_text())
        ids = {item["id"] for item in corpus["evals"]}
        self.assertTrue({"completed", "non-default-completed", "resume-active-task", "scope-change", "unrelated-worktree", "dirty-overlap", "position-insufficient", "automatic-risk-expansion", "explicit-risk-expansion", "blocked"}.issubset(ids))
        self.assertEqual({item["expected_exit"] for item in corpus["evals"]}, {"completed", "resume_active_task", "scope_change", "location_required", "reselect_mode", "explicit_choice_required", "blocked"})
        for case_id in ("automatic-risk-expansion", "explicit-risk-expansion"):
            case = next(item for item in corpus["evals"] if item["id"] == case_id)
            public_file = next(path for path in case["files"] if "public" in path)
            payload = json.loads((PACKAGE / public_file).read_text())
            self.assertEqual(payload["target_paths"], ["docs/guide.md", "docs/follow-up.md"])


if __name__ == "__main__":
    unittest.main()
