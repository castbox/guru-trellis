"""Real Review staging and owner transport; fixture judgments are not AI evidence."""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SKILLS = Path(__file__).resolve().parents[1]
ROOT = SKILLS.parents[2]
sys.path.insert(0, str(SKILLS))
from adapters.eval import architecture_authoring, branch_authoring
from adapters.eval.fixture_io import run_git, stage_clean_installed_owner_repo
from runtime.delivery_projection.adapter import DeliveryProjection
from runtime.schema import validate_json


class BranchAuthoringTransportTests(unittest.TestCase):
    def test_current_candidate_and_authored_nonpassing_transport_without_check(self):
        with tempfile.TemporaryDirectory() as temporary, patch.dict(
            os.environ, {"TRELLIS_CONTEXT_ID": "branch-native-transport-test"},
        ):
            execution = Path(temporary).resolve()
            source_package = SKILLS / "packages/guru-review-branch"
            runtime = ROOT / ".trellis/guru-team/scripts/bash/run-skill-command.sh"
            fixture, _ = stage_clean_installed_owner_repo(execution, runtime, source_package)
            files = ["evals/files/native-owner-input.json", "evals/files/native-range-boundary.py"]
            work = execution / "workdir"
            for name in files:
                target = work / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_package / name, target)
            request = {"case_id": "native-common-expectation", "workdir": str(work), "files": files}
            package = fixture / ".trellis/guru-team/skills/packages/guru-review-branch"
            branch_authoring.stage(request, fixture, package, ROOT)
            public = json.loads((fixture / branch_authoring.PUBLIC_INPUT).read_text())
            validate_json(public, package / "schemas/public-delivery-branch-review-input-2.0.schema.json", "input")
            projection = DeliveryProjection(fixture, public["task_ref"])
            current = projection.resolve(public["delivery_key"])
            # Exercise the original receiving precondition, not only the later
            # Review wrappers: C4 alone cannot supply current C5 ownership.
            head_before_ensure = run_git(fixture, "rev-parse", "HEAD")
            ensure_input = {"profile":"delivery_active_task", "mode":"workflow",
                "task_id":public["delivery_key"]["task_id"],
                "lifecycle_generation":public["delivery_key"]["lifecycle_generation"]}
            ensured = subprocess.run([str(package.parent / "guru-ensure-task-checkout/scripts/invoke.sh"),
                "--root", str(fixture), "--input", json.dumps(ensure_input)],
                text=True, capture_output=True, cwd=fixture)
            self.assertEqual(0, ensured.returncode, ensured.stdout + ensured.stderr)
            resolved = json.loads(ensured.stdout)
            self.assertEqual("checkout_resolved", resolved["exit_id"], resolved)
            self.assertEqual(str(fixture), resolved["checkout_path"])
            self.assertEqual(public["task_ref"], resolved["task_ref"])
            self.assertEqual(head_before_ensure, run_git(fixture, "rev-parse", "HEAD"))
            self.assertEqual("checking", current["phase"])
            self.assertIsNone(current["results"]["check"])
            self.assertIsNone(current["results"]["full_review"])
            self.assertFalse((fixture / "docs/phase2-evidence/check-public-input.json").exists())
            self.assertFalse(list((fixture / ".trellis/.runtime/guru-team/owner-checkpoints").rglob("*review-gate.json")))
            self.assertEqual((fixture / "interval.py").read_bytes(), (source_package / files[1]).read_bytes())
            self.assertEqual(run_git(fixture, "diff", public["base_ref"], "HEAD", "--", "range_filter.py"), "")
            validation = json.loads((fixture / "docs/phase2-evidence/validation.json").read_text())
            self.assertEqual(0, validation["returncode"])
            behavior = subprocess.run([sys.executable, "-c",
                "from interval import contains; from range_filter import select; "
                "assert not contains(4,2,4); assert not contains(2,2,2); "
                "assert select([2,3,4],2,4)==[2,3]"], cwd=fixture, capture_output=True)
            self.assertEqual(0, behavior.returncode, behavior.stderr)

            architecture = json.loads((fixture / branch_authoring.ARCHITECTURE_INPUT).read_text())
            architecture_package = package.parent / "guru-maintain-architecture-baseline"
            validate_json(architecture, architecture_package / "schemas/public-input-delivery-task-impact-sync-4.0.schema.json", "architecture")
            self.assertIn("schemas/semantic-result-delivery-4.0.schema.json", architecture_authoring.contract_paths(architecture))
            facts = json.loads((fixture / branch_authoring.FACTS).read_text())
            self.assertEqual([architecture["constitution"]["authority_locator"], architecture["baseline"]["locator"],
                architecture["project_contract"]["change_contract_locator"]], facts["architecture_reads"][:3])
            self.assertFalse(any(Path(path).name in {"prd.md", "implement.md", "task.json"}
                for path in facts["architecture_reads"]))
            # This explicit fixture author exercises the real current Architecture
            # wrapper. It does not stand in for the fresh native reviewer.
            owner = {name: copy.deepcopy(value) for name, value in architecture.items()
                if name not in {"source_exit", "requirement_authority", "behavior_authority", "committed_range"}}
            owner.update(input_sha256=hashlib.sha256(json.dumps(architecture, ensure_ascii=False,
                sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
                typed_exit="baseline_current", baseline_identity=architecture["baseline"]["identity"],
                constitution_identity=architecture["constitution"]["identity"],
                impact_kind="no_architecture_impact", impact_reason="Fixture: pure predicate and filter retain ownership and dependencies.",
                promotion_state="no_change", consumer={"kind":"workflow", "id":"guru-architecture-baseline-current-router"},
                ai_review_gate={"status":"passed", "reviewed_scope":"Fixture current architecture transport",
                    "evidence_summary":"Fixture-owned transport only; no native judgment claimed.", "findings":[],
                    "conclusion":"No architecture ownership change is supplied by this fixture."})
            actual = subprocess.run([str(architecture_package / "scripts/invoke.sh"), "--invocation", "-"],
                input=json.dumps({"public_input":architecture, "owner_result":owner}), text=True,
                capture_output=True, cwd=fixture)
            self.assertEqual(0, actual.returncode, actual.stdout + actual.stderr)
            self.assertEqual("baseline_current", json.loads(actual.stdout)["exit_id"])

            # Missing actual judgments stop at the original recorder. The
            # adapter must not supply them from Architecture or an example.
            authored = json.loads((package / "examples/authoring-delivery-passed-2.0.json").read_text())
            authored["semantic_review"]["ai_review_gate"]["status"] = "blocked"
            authored["delivery_review"]["current_slice_status"] = "blocked"
            authored["adequacy_review"]["verification_completeness"]["status"] = "unverified"
            authored["gate_judgments"] = {role:{"outcome":"blocked", "summary":"Fixture transport stops without a completed native assessment."}
                for role in ("check", "full_review")}
            missing = copy.deepcopy(authored)
            del missing["gate_judgments"]
            rejected = branch_authoring.execute(package, fixture, {"public_input":public, "owner_result":missing}, dict(os.environ))
            self.assertNotEqual(0, rejected.returncode)
            self.assertEqual("schema_mismatch", json.loads(rejected.stdout)["code"])
            checkpoint = fixture / facts["owner_mutated_paths"][1]
            captured = {}
            original_run = subprocess.run
            def observe_checked_gate(argv, **kwargs):
                result = original_run(argv, **kwargs)
                if Path(argv[0]).name == "check-review-gate.sh" and result.returncode == 0:
                    captured.update(json.loads(checkpoint.read_text()))
                return result
            with patch("adapters.eval.branch_authoring.subprocess.run", side_effect=observe_checked_gate):
                actual = branch_authoring.execute(package, fixture, {"public_input":public, "owner_result":authored}, dict(os.environ))
            self.assertEqual(0, actual.returncode, actual.stdout + actual.stderr)
            self.assertEqual("blocked", json.loads(actual.stdout)["exit_id"])
            receipt = json.loads((fixture.parent / "branch-command-receipts.json").read_text())
            self.assertEqual(3, len(receipt))
            self.assertTrue(all(row["returncode"] == 0 for row in receipt))
            recorded = captured
            self.assertFalse(checkpoint.exists())
            self.assertEqual("8.0", recorded["schema_version"])
            self.assertEqual(authored["adequacy_review"], recorded["adequacy_review"])
            self.assertEqual(authored["gate_judgments"], recorded["gate_judgments"])
            self.assertIsNone(projection.resolve(public["delivery_key"])["results"]["check"])
            self.assertIsNone(projection.resolve(public["delivery_key"])["results"]["full_review"])


if __name__ == "__main__":
    unittest.main()
