from __future__ import annotations

import copy
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
import sys
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE.parent / "guru-create-delivery/tests"))
from support import installed_fixture
from pathlib import Path


class ApproveTaskPlanPackageContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.package = Path(__file__).resolve().parents[1]
        self.repo = self.package.parents[1]
        self.interface = self.read("interface.json")
        self.schema = self.read("schemas/planning-approval-delivery.schema.json")
        self.example = self.read("examples/planning-approval-delivery.json")

    def read(self, relative: str) -> dict:
        return json.loads((self.package / relative).read_text(encoding="utf-8"))

    def planning_fixture(self):
        fixture = installed_fixture(self)
        key = fixture.create()
        directory = fixture.projection.planning_directory(key)
        for name in ("prd.md", "design.md", "implement.md"):
            (directory / name).write_text(f"# {name}\n", encoding="utf-8")
        authoring = {name: copy.deepcopy(self.example[name]) for name in (
            "mode", "authority_refs", "delivery_policy", "docs_ssot_plan",
            "semantic_review", "typed_exit", "consumer", "reason",
        )}
        path = fixture.root / "planning-owner-input.json"
        path.write_text(json.dumps(authoring), encoding="utf-8")
        return fixture, key, directory, path

    def command(self, fixture, name, *args, expected=0):
        result = subprocess.run([str(self.package / "scripts" / name), "--root", str(fixture.root), *args],
                                cwd=fixture.root, text=True, capture_output=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def record(self, fixture, key, path):
        return self.command(fixture, "record-planning-approval.sh", "--task", fixture.task_ref,
                            "--delivery-key", json.dumps(key), "--input", str(path), "--json")["result"]

    def check(self, fixture, key, expected=0):
        return self.command(fixture, "check-planning-approval.sh", "--task", fixture.task_ref,
                            "--delivery-key", json.dumps(key), "--json", expected=expected)

    def public_invoke(self, fixture, key, owner, expected=0):
        public = self.read("examples/public-delivery-initial-review-input-2.0.json")
        public.update(task_ref=fixture.task_ref, delivery_key=key)
        import hashlib
        directory=fixture.projection.planning_directory(key)
        public["architecture_assessment"]["freshness_identity"]="sha256:"+hashlib.sha256((directory/"design.md").read_bytes()).hexdigest()
        path = fixture.root / "public-input.json"
        path.write_text(json.dumps(public))
        return self.command(fixture, "invoke.sh", "--input", str(path), "--owner-result", owner["artifact_path"], expected=expected)


    def test_architecture_stage_consumes_adjacent_completed_owner_result(self) -> None:
        skill = (self.package / "SKILL.md").read_text(encoding="utf-8")
        contract = (self.package / "references/contract.md").read_text(encoding="utf-8")
        for text in (skill, contract):
            self.assertRegex(text, r"adjacent\s+upstream")
            self.assertRegex(text, r"second\s+external")
            self.assertRegex(text, r"already\s+completed")

    def test_approve_planning_staging_uses_real_record_and_check_wrappers(self):
        fixture, key, directory, path = self.planning_fixture()
        before = fixture.projection.resolve(key)
        recorded = self.record(fixture, key, path)
        checked = self.check(fixture, key)["result"]
        self.assertEqual(checked["consumer"], {"kind": "workflow", "id": "phase-1-delivery-activation"})
        output = self.public_invoke(fixture, key, recorded)
        self.assertEqual(output, {"exit_id": "approved", "task_ref": fixture.task_ref,
                                 "delivery_key": key, "planning_result_id": "planning:" + recorded["reviewed_content_sha256"]})
        self.assertFalse(Path(recorded["artifact_path"]).exists())
        self.assertEqual(fixture.projection.resolve(key), before)  # Approval does not activate.
        from support import owner_module
        activation = owner_module(self.package.parent / "guru-activate-delivery")
        public = {"profile": "delivery_activation", "mode": "workflow", "task_ref": fixture.task_ref,
                  "delivery_key": key, "action": "activate", "planning_result_id": output["planning_result_id"]}
        result = activation.invoke(self.package.parent / "guru-activate-delivery", fixture.root, public,
                                   {"typed_exit": "delivery_started", "reason": "The actual current plan was reviewed."})
        self.assertEqual(result["exit_id"], "delivery_started")
        self.assertNotEqual(result["planning_accepted_result_id"], output["planning_result_id"])


    def test_delivery_revision_actions_return_to_the_original_author_router(self):
        fixture, key, directory, path = self.planning_fixture()
        author = json.loads(path.read_text())
        author.update(typed_exit="revision_required", consumer={
            "kind": "workflow", "id": "guru-task-plan-approval-revision-router"})
        actions = ["修订当前 Delivery 的来源设计处置。"]
        author["semantic_review"].update(status="revision_required", revision_actions=actions)
        path.write_text(json.dumps(author))
        before = fixture.projection.read_record()
        recorded = self.record(fixture, key, path)
        self.assertEqual(self.check(fixture, key)["result"]["typed_exit"], "revision_required")
        output = self.public_invoke(fixture, key, recorded)
        self.assertEqual(output, {"exit_id": "revision_required", "task_ref": fixture.task_ref,
                                 "delivery_key": key, "revision_actions": actions})
        self.assertEqual(fixture.projection.read_record(), before)
        self.assertFalse(Path(recorded["artifact_path"]).exists())
        from jsonschema import Draft202012Validator
        row = next(row for row in self.interface["public_contracts"]["consumer_inputs"]
                   if row["id"] == "revision_workflow_input")
        Draft202012Validator(self.read(row["contract"]["path"])).validate(output)

    def test_clarify_scope_uses_real_record_check_and_invoke_wrappers(self):
        fixture, key, directory, path = self.planning_fixture()
        author = json.loads(path.read_text())
        author.update(typed_exit="clarify_scope", consumer={"kind": "workflow", "id": "guru-task-plan-clarify-scope-router"})
        author["semantic_review"].update(status="clarify_scope", scope_proposals=["scope-proposal:R13"])
        path.write_text(json.dumps(author))
        recorded = self.record(fixture, key, path)
        self.assertEqual(self.check(fixture, key)["result"]["typed_exit"], "clarify_scope")
        output = self.public_invoke(fixture, key, recorded)
        self.assertEqual(output, {"exit_id": "clarify_scope", "task_ref": fixture.task_ref,
                                 "delivery_key": key, "proposal_refs": ["scope-proposal:R13"]})
        self.assertFalse(Path(recorded["artifact_path"]).exists())
        self.assertEqual(fixture.projection.resolve(key)["phase"], "planning")


    def test_planning_artifact_resolution_is_package_owned_and_compatible(self):
        command = next(item for item in self.read("commands.json")["commands"] if item["id"] == "resolve-planning-artifacts")
        self.assertEqual(command["runtime_role"], "check")
        self.assertEqual(command["side_effect"], "repo_read")
        fixture, key, directory, path = self.planning_fixture()
        (directory / "implement.md").unlink()
        result = self.command(fixture, "resolve-human-artifacts.sh", "--task", fixture.task_ref,
                              "--delivery-key", json.dumps(key), "--json")["result"]
        self.assertEqual(result["task_dir_relative"], directory.relative_to(fixture.root.resolve()).as_posix())
        self.assertEqual([item["exists"] for item in result["markdown_artifacts"]], [True, True, False])
        self.assertEqual((fixture.task / "prd.md").read_text(), "整体scope\n")


    def test_artifact_help_and_compatibility_wrapper_route_to_package(self) -> None:
        root = self.package.parents[4]
        wrapper = (
            root / "trellis/workflows/guru-team/scripts/bash/resolve-human-artifacts.sh"
            if (root / "trellis/skills/guru-team").is_dir()
            else root / ".trellis/guru-team/scripts/bash/resolve-human-artifacts.sh"
        )
        for target in (self.package / "scripts/resolve-human-artifacts.sh", wrapper):
            result = subprocess.run(
                [str(target), "--help"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result)
            self.assertIn("usage: resolve-planning-artifacts", result.stdout)
            self.assertIn("owner: guru-approve-task-plan", result.stdout)


    def test_interface_declares_compact_private_owner_contract(self) -> None:
        self.assertEqual(self.interface["id"], "guru-approve-task-plan")
        self.assertEqual(self.interface["schema_version"], "1.4")
        self.assertEqual(self.interface["judgment_mode"], "semantic")
        expected = [
            "runtime_dependency", "task_checkout", "current_authority",
            "planning_documents", "docs_ssot", "wording_result",
            "invocation_freshness",
        ]
        self.assertEqual(self.interface["modes"]["workflow"]["entry_precondition_ids"], expected)
        self.assertEqual(self.interface["modes"]["standalone"]["entry_precondition_ids"], expected)
        self.assertEqual(
            [(item["id"], item["consumer"]) for item in self.interface["external_exits"]],
            [
                ("approved", {"kind": "workflow", "id": "phase-1-delivery-activation"}),
                ("revision_required", {"kind": "workflow", "id": "guru-task-plan-approval-revision-router"}),
                ("clarify_scope", {"kind": "workflow", "id": "guru-task-plan-clarify-scope-router"}),
                ("blocked", {"kind": "stop", "id": "task-plan-approval-blocked"}),
            ],
        )
        private = self.interface["public_contracts"]["private_artifacts"]
        self.assertEqual(private[0]["persistence"], "ignored_runtime")
        self.assertTrue(private[0]["schema"]["schema_id"].endswith("guru-planning-approval-delivery-1.0"))
        self.assertRegex(self.example["reviewed_content_sha256"], r"^[0-9a-f]{64}$")
        self.assertIn(
            "Owner-private composite freshness token",
            self.schema["properties"]["reviewed_content_sha256"]["description"],
        )

    def test_interface_gate_inputs_outputs_and_consumer_examples_validate(self) -> None:
        from jsonschema import Draft202012Validator

        interface_schema = json.loads(
            (self.package.parents[1] / self.interface["$schema"].removeprefix("../../")).read_text(encoding="utf-8")
        )
        Draft202012Validator(interface_schema).validate(self.interface)
        Draft202012Validator.check_schema(self.schema)
        Draft202012Validator(self.schema).validate(self.example)

        for name in ("delivery-initial-review", "delivery-revision-reentry", "delivery-clarification-reentry"):
            schema = self.read(f"schemas/public-{name}-input.schema.json")
            example = self.read(f"examples/public-{name}-input.json")
            Draft202012Validator(schema).validate(example)
        for name in ("approved", "revision-required", "clarify-scope", "blocked"):
            schema = self.read(next(row["schema"]["path"] for row in self.interface["public_contracts"]["outputs"] if row["exit_id"] == name.replace("-", "_")))
            example = self.read(next(row["example"]["path"] for row in self.interface["public_contracts"]["outputs"] if row["exit_id"] == name.replace("-", "_")))
            Draft202012Validator(schema).validate(example)

        consumer_schema = json.loads(
            (self.package / next(row["contract"]["path"] for row in self.interface["public_contracts"]["consumer_inputs"] if row["id"] == "approved_workflow_input")).read_text(encoding="utf-8")
        )
        self.assertIn("approved", consumer_schema["$id"])
        approved = self.read("examples/public-delivery-approved-output.json")
        consumer = Draft202012Validator(consumer_schema)
        consumer.validate(approved)
        self.assertFalse(consumer.is_valid({key: value for key, value in approved.items() if key != "planning_result_id"}))
        activation = json.loads((self.package.parent / "guru-activate-delivery/examples/public-delivery-activation-input.json").read_text())
        activation.update(task_ref=approved["task_ref"], delivery_key=approved["delivery_key"], planning_result_id=approved["planning_result_id"])
        activation_schema = json.loads((self.package.parent / "guru-activate-delivery/schemas/public-delivery-activation-input.schema.json").read_text())
        Draft202012Validator(activation_schema).validate(activation)

    def test_compact_gate_has_four_closed_semantic_routes(self) -> None:
        from jsonschema import Draft202012Validator

        validator = Draft202012Validator(self.schema)
        cases = {
            "revision_required": {
                "status": "revision_required",
                "revision_actions": ["Revise the task-local plan."],
                "scope_proposals": [],
                "blocking_reasons": [],
                "consumer": {"kind": "workflow", "id": "guru-task-plan-approval-revision-router"},
            },
            "clarify_scope": {
                "status": "clarify_scope",
                "revision_actions": [],
                "scope_proposals": ["scope-proposal:R13"],
                "blocking_reasons": [],
                "consumer": {"kind": "workflow", "id": "guru-task-plan-clarify-scope-router"},
            },
            "blocked": {
                "status": "blocked",
                "revision_actions": [],
                "scope_proposals": [],
                "blocking_reasons": ["Current authority is unavailable."],
                "consumer": {"kind": "stop", "id": "task-plan-approval-blocked"},
            },
        }
        for typed_exit, case in cases.items():
            with self.subTest(typed_exit=typed_exit):
                payload = copy.deepcopy(self.example)
                payload["typed_exit"] = typed_exit
                payload["consumer"] = case.pop("consumer")
                payload["semantic_review"].update(case)
                validator.validate(payload)

        invalid = copy.deepcopy(self.example)
        invalid["semantic_review"]["scope_proposals"] = ["scope-proposal:R13"]
        self.assertFalse(validator.is_valid(invalid))

        invalid_object = copy.deepcopy(self.example)
        invalid_object["typed_exit"] = "clarify_scope"
        invalid_object["consumer"] = {
            "kind": "workflow",
            "id": "guru-task-plan-clarify-scope-router",
        }
        invalid_object["semantic_review"].update({
            "status": "clarify_scope",
            "scope_proposals": [{"id": "scope-proposal:R13"}],
        })
        self.assertFalse(validator.is_valid(invalid_object))

    def test_public_inputs_only_route_owner_entry(self) -> None:
        forbidden = {
            "adequacy_review", "ai_review_gate", "evidence_locators",
            "exit_intent", "findings", "provenance_review",
            "scope_dispositions", "unusual_scenario_dispositions",
            "unverified_conclusions",
        }
        for path in sorted((self.package / "schemas").glob("public-*input.schema.json")):
            properties = self.read(path.relative_to(self.package).as_posix()).get("properties", {})
            self.assertTrue(forbidden.isdisjoint(properties), path)

    def test_package_json_has_no_authorization_or_routine_handoff_fields(self) -> None:
        forbidden = {
            "agent_assignment", "confirmation", "confirmation_ref",
            "confirmation_sha256", "confirmed_plan_digest", "human_authorization",
            "human_confirmation", "implementation_handoff", "liveness",
            "review_report", "review_reports", "user_confirmation",
        }

        def keys(value: object) -> set[str]:
            if isinstance(value, dict):
                return set(value) | set().union(*(keys(item) for item in value.values()), set())
            if isinstance(value, list):
                return set().union(*(keys(item) for item in value), set())
            return set()

        for path in sorted(self.package.rglob("*.json")):
            self.assertTrue(forbidden.isdisjoint(keys(json.loads(path.read_text(encoding="utf-8")))), path)

    def test_planning_requires_current_architecture_stage_result(self) -> None:
        repo = next(parent for parent in self.package.parents if (parent / "trellis/workflows/guru-team/workflow.md").is_file())
        sources = {
            "skill": self.package / "SKILL.md",
            "contract": self.package / "references/contract.md",
        }
        required = (
            "final_plan",
            "baseline_current",
            "design constitution",
            "change contract",
            "no_architecture_impact",
        )
        for label, path in sources.items():
            with self.subTest(source=label):
                text = " ".join(path.read_text(encoding="utf-8").replace("design-constitution", "design constitution").replace("change-contract", "change contract").split())
                for phrase in required:
                    self.assertIn(phrase, text)
                self.assertNotIn("Afizzy", text)

        skill = " ".join(sources["skill"].read_text(encoding="utf-8").split())
        self.assertIn("cannot approve a missing or stale Architecture result", skill)
        self.assertIn("do not copy the Architecture owner's reasoning", skill)

        workflow = (repo / "trellis/workflows/guru-team/workflow.md").read_text(encoding="utf-8")
        phase = workflow.split("#### 1.1 Unique Author and global sequence", 1)[1].split("#### 1.5 Task activation", 1)[0]
        self.assertLess(
            phase.index("final_plan"),
            phase.index("Approval"),
        )
        for exit_id in (
            "sync_required", "baseline_incomplete", "architecture_conflict",
            "contract_incomplete", "fitness_regression",
        ):
            self.assertIn(exit_id, workflow)

    def test_approved_exit_keeps_workflow_owned_phase1_review_pause(self) -> None:
        repo = next(parent for parent in self.package.parents if (parent / ".trellis/workflow.md").is_file())
        canonical = repo / "trellis/workflows/guru-team/workflow.md"
        workflow = (canonical if canonical.is_file() else repo / ".trellis/workflow.md").read_text(encoding="utf-8")
        normalized = " ".join(workflow.split())

        required = (
            "show clickable links to `prd.md`, `design.md`, and `implement.md`",
            "AI semantic conclusion",
            "key design choices",
            "important alternatives",
            "trade-offs",
            "remaining unverified boundaries",
            "`确认继续`, `可以，继续实现`, `方案没问题，开始做`",
            "A question, challenge, revision request, partial choice, or ambiguous reply is not acceptance",
            "no reply about an older presentation may be reused",
            "A Phase 0 confirmation never accepts a Phase 1 plan",
            "explicitly select autonomous execution",
            "still pause and use their existing route even during autonomous execution",
            "no recorder or validator parses the reply",
        )
        for phrase in required:
            self.assertIn(phrase, normalized)
        self.assertLess(normalized.index("show clickable links to `prd.md`"), normalized.index("resume_target=delivery_activation"))

        markers = [
            json.loads(raw)
            for raw in re.findall(r"<!-- guru-confirmation-boundary: (\{.*?\}) -->", workflow)
        ]
        by_id = {row["id"]: row for row in markers}
        self.assertEqual(by_id["phase_1_plan_review"]["profiles"], ["open_issue", "new_issue"])
        self.assertEqual(sum("open_issue" in row["profiles"] for row in markers), 4)
        self.assertEqual(sum("new_issue" in row["profiles"] for row in markers), 5)

    def test_approved_eval_covers_phase1_dialogue_matrix(self) -> None:
        corpus = self.read("evals/evals.json")
        approved = next(row for row in corpus["evals"] if row["id"] == "approved-initial")
        facts = self.read("evals/files/approved-initial-facts.json")
        scenarios = facts["workflow_consumer_scenarios"]
        self.assertEqual(len(facts["workflow_consumer_authority"]), 5)
        self.assertEqual(
            {row["id"] for row in scenarios},
            {
                "clear-confirmation", "equivalent-affirmative",
                "question-is-not-confirmation", "revision-request",
                "phase0-confirmation-not-reusable",
                "changed-plan-invalidates-old-confirmation", "open-ai-finding",
                "explicit-autonomous-execution", "autonomous-scope-change",
            },
        )
        self.assertEqual(len(scenarios), 9)
        for scenario in scenarios:
            self.assertNotIn("expected", scenario)
            self.assertNotIn("decision", scenario)
            self.assertNotIn("route", scenario)

        semantic = approved["assertions"]["semantic"]
        self.assertIn(
            "one concise but complete eval-private transcript decision for every scenario id",
            approved["prompt"],
        )
        self.assertEqual(
            {row["id"] for row in semantic},
            {
                "clear-confirmation-activates",
                "equivalent-affirmative-activates",
                "question-remains-paused",
                "revision-rereviews-before-presentation",
                "phase0-confirmation-not-reused",
                "changed-plan-invalidates-old-confirmation",
                "open-finding-blocks-activatable-presentation",
                "explicit-autonomous-omits-only-routine-pause",
                "autonomous-scope-change-still-pauses",
                "direct-evolution-first",
                "compatibility-exception-is-specific",
                "public-name-is-not-exemption",
                "maintainability-boundary",
            },
        )
        self.assertTrue(all(row["evidence_selector"] == "transcript" for row in semantic))

    def test_dialogue_matrix_requires_external_semantic_grading(self) -> None:
        repo_root = next(
            parent for parent in self.package.parents
            if (parent / ".trellis/workflow.md").is_file()
        )
        source_package = (
            repo_root
            / "trellis/skills/guru-team/packages/guru-approve-task-plan"
        )
        mode = "source" if self.package == source_package else "installed"
        runner = repo_root / ".trellis/guru-team/scripts/bash/run-skill-evals.sh"
        semantic = next(
            row for row in self.read("evals/evals.json")["evals"]
            if row["id"] == "approved-initial"
        )["assertions"]["semantic"]
        base_argv = [
            str(runner), "--root", str(repo_root), "--mode", mode,
            "--skill", "guru-approve-task-plan", "--adapter", "shared",
            "--case", "approved-initial",
        ]
        env = {**os.environ, "PATH": f"/usr/local/bin:{os.environ.get('PATH', '')}"}
        with tempfile.TemporaryDirectory(prefix="guru-plan-dialogue-eval-") as temporary:
            run_root = Path(temporary)
            missing = subprocess.run(
                [*base_argv, "--run-root", str(run_root / "missing"), "--json"],
                cwd=repo_root, env=env, text=True, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, check=False,
            )
            self.assertEqual(missing.returncode, 0, missing.stderr)
            missing_result = json.loads(missing.stdout)
            self.assertEqual(missing_result["status"], "evaluation_failed")
            self.assertEqual(
                len(missing_result["cases"][0]["semantic_results"]), len(semantic),
            )
            self.assertEqual(
                {row["detail"] for row in missing_result["cases"][0]["semantic_results"]},
                {"external semantic grading missing"},
            )

            grading = {
                "schema_version": "1.0",
                "results": [
                    {
                        "case_id": "approved-initial",
                        "comparison_side": "current",
                        "assertion_id": row["id"],
                        "passed": True,
                        "summary": "The transcript selects the required workflow-consumer behavior.",
                    }
                    for row in semantic
                ],
            }
            accepted_path = run_root / "accepted-grading.json"
            accepted_path.write_text(json.dumps(grading), encoding="utf-8")
            accepted = subprocess.run(
                [
                    *base_argv, "--run-root", str(run_root / "accepted"),
                    "--semantic-grading", str(accepted_path), "--json",
                ],
                cwd=repo_root, env=env, text=True, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, check=False,
            )
            self.assertEqual(accepted.returncode, 0, accepted.stderr)
            self.assertEqual(json.loads(accepted.stdout)["status"], "passed")

            grading["results"][0].update({
                "passed": False,
                "summary": "The transcript activates without a current post-presentation affirmative.",
            })
            rejected_path = run_root / "rejected-grading.json"
            rejected_path.write_text(json.dumps(grading), encoding="utf-8")
            rejected = subprocess.run(
                [
                    *base_argv, "--run-root", str(run_root / "rejected"),
                    "--semantic-grading", str(rejected_path), "--json",
                ],
                cwd=repo_root, env=env, text=True, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, check=False,
            )
            self.assertEqual(rejected.returncode, 0, rejected.stderr)
            rejected_result = json.loads(rejected.stdout)
            self.assertEqual(rejected_result["status"], "evaluation_failed")
            self.assertFalse(rejected_result["cases"][0]["semantic_results"][0]["passed"])

    def test_public_invoke_consumes_only_the_exact_successful_owner_checkpoint(self):
        fixture, key, directory, path = self.planning_fixture()
        recorded = self.record(fixture, key, path)
        # A normal edit makes both check and invoke stale and retains recoverable evidence.
        (directory / "design.md").write_text("New actual design obligation\n")
        self.assertEqual(self.check(fixture, key, expected=3)["code"], "stale_identity")
        self.assertEqual(self.public_invoke(fixture, key, recorded, expected=3)["code"], "stale_identity")
        self.assertTrue(Path(recorded["artifact_path"]).exists())
        self.record(fixture, key, path)
        self.public_invoke(fixture, key, recorded)
        self.assertFalse(Path(recorded["artifact_path"]).exists())

    def test_two_delivery_checkpoints_are_independent(self):
        fixture, first, directory, path = self.planning_fixture()
        first_owner = self.record(fixture, first, path)
        fixture.stop(first)
        second = fixture.create()
        second_dir = fixture.projection.planning_directory(second)
        for name in ("prd.md", "design.md", "implement.md"):
            (second_dir / name).write_text("D2 plan\n")
        second_owner = self.record(fixture, second, path)
        self.assertNotEqual(first_owner["artifact_path"], second_owner["artifact_path"])
        self.assertNotEqual(first_owner["reviewed_content_sha256"], second_owner["reviewed_content_sha256"])
        self.public_invoke(fixture, second, second_owner)
        self.assertTrue(Path(first_owner["artifact_path"]).exists())
        self.assertFalse(Path(second_owner["artifact_path"]).exists())
        self.assertEqual((directory / "design.md").read_text(), "# design.md\n")


    def test_subtraction_first_contract_is_loaded_without_public_authorization(self) -> None:
        repo = self.package.parents[4]
        spec = repo / ".trellis/spec/workflow/subtraction-first-compatibility.md"
        self.assertTrue(spec.is_file())
        text = " ".join(spec.read_text(encoding="utf-8").split())
        for phrase in (
            "direct modification, deletion",
            "affected deprecated asset",
            "current conversation",
            "Before coding, adding compatibility tests, or self-fixing",
            "Approval is dialogue-local",
            "direct consumer",
            "3000-line",
        ):
            self.assertIn(phrase, text)
        package_text = " ".join(
            path.read_text(encoding="utf-8")
            for path in (self.package / "SKILL.md", self.package / "references/contract.md")
        )
        self.assertIn("subtraction-first-compatibility.md", package_text)
        self.assertNotIn("human_authorization", json.dumps(self.interface))

    def test_delivery_policy_is_private_semantic_evidence_not_public_dto(self) -> None:
        policy = self.example["delivery_policy"]
        self.assertTrue(policy["task_scope"])
        self.assertTrue(policy["delivery_slice"])
        self.assertTrue(policy["independent_delivery_conditions"])
        self.assertTrue(policy["validation_boundaries"])
        self.assertIn("remaining_work_owner", policy)
        approved = self.read("examples/public-delivery-approved-output.json")
        self.assertEqual({"exit_id", "task_ref", "delivery_key", "planning_result_id"}, set(approved))
        self.assertEqual(
            approved["planning_result_id"],
            f"planning:{self.example['reviewed_content_sha256']}",
        )
        self.assertNotIn("delivery_policy", approved)

    def test_wrappers_are_dispatcher_only_and_package_is_not_portable(self) -> None:
        for name, validator in (
            ("record-planning-approval.sh", "planning_approval_recorder"),
            ("check-planning-approval.sh", "planning_approval_checker"),
        ):
            path = self.package / "scripts" / name
            self.assertTrue(path.stat().st_mode & 0o111)
            wrapper = path.read_text(encoding="utf-8")
            self.assertIn("runtime/launch.sh", wrapper)
            runtime_command = next(item["runtime_command"] for item in self.interface["validators"] if item["id"] == validator)
            self.assertIn(f'source "$LAUNCHER" {runtime_command}', wrapper)
            self.assertNotIn("guru_team_trellis.py", wrapper)

        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "guru-approve-task-plan"
            shutil.copytree(self.package, copied)
            result = subprocess.run(
                [str(copied / "scripts/record-planning-approval.sh"), "--help"],
                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("not self-contained or portable", result.stderr)

    def test_example_is_deidentified_and_current(self) -> None:
        encoded = json.dumps(self.example)
        self.assertNotIn("/Users/", encoded)
        self.assertEqual(self.example["schema_version"], "delivery-1.0")
        self.assertEqual(self.example["skill_id"], "guru-approve-task-plan")


if __name__ == "__main__":
    unittest.main()
