from __future__ import annotations

import copy
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class ApproveTaskPlanPackageContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.package = Path(__file__).resolve().parents[1]
        self.repo = self.package.parents[1]
        self.interface = self.read("interface.json")
        self.schema = self.read("schemas/planning-approval.schema.json")
        self.example = self.read("examples/planning-approval.json")

    def read(self, relative: str) -> dict:
        return json.loads((self.package / relative).read_text(encoding="utf-8"))

    def planning_fixture(self, root: Path) -> tuple[Path, Path]:
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        task = root / ".trellis/tasks/current"
        task.mkdir(parents=True)
        for name in ("prd.md", "design.md", "implement.md"):
            (task / name).write_text(f"# {name}\n", encoding="utf-8")
        authoring = {key: self.example[key] for key in (
            "mode", "authority_refs", "delivery_policy", "docs_ssot_plan",
            "semantic_review", "typed_exit", "consumer", "reason",
        )}
        authoring["mode"] = "workflow"
        owner_input = root / "planning-owner-input.json"
        owner_input.write_text(json.dumps(authoring) + "\n", encoding="utf-8")
        return task, owner_input

    def test_architecture_stage_consumes_adjacent_completed_owner_result(self) -> None:
        skill = (self.package / "SKILL.md").read_text(encoding="utf-8")
        contract = (self.package / "references/contract.md").read_text(encoding="utf-8")
        for text in (skill, contract):
            self.assertRegex(text, r"adjacent\s+upstream")
            self.assertRegex(text, r"second\s+external")
            self.assertRegex(text, r"already\s+completed")

    def test_approve_planning_staging_uses_real_record_and_check_wrappers(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = Path(temp)
            task, owner_input = self.planning_fixture(fixture)
            task_ref = task.relative_to(fixture).as_posix()
            recorded = subprocess.run(
                [
                    str(self.package / "scripts/record-planning-approval.sh"),
                    "--root", str(fixture),
                    "--task", task_ref,
                    "--input", owner_input.relative_to(fixture).as_posix(),
                    "--json",
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(recorded.returncode, 0, recorded.stderr)
            checked_process = subprocess.run(
                [
                    str(self.package / "scripts/check-planning-approval.sh"),
                    "--root", str(fixture),
                    "--task", task_ref,
                    "--json",
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(checked_process.returncode, 0, checked_process.stderr)
            checked = json.loads(checked_process.stdout)
            self.assertEqual(checked["typed_exit"], "approved")
            self.assertEqual(
                checked["consumer"],
                {"kind": "workflow", "id": "phase-1-task-activation"},
            )
            checkpoint = json.loads(Path(checked["artifact_path"]).read_text(encoding="utf-8"))
            self.assertEqual(checkpoint["delivery_policy"], self.example["delivery_policy"])
            public_input = fixture / "public-input.json"
            public_input.write_text(json.dumps({"mode": "workflow", "task_ref": task_ref}), encoding="utf-8")
            invoked = subprocess.run(
                [
                    str(self.package / "scripts/invoke.sh"), "--root", str(fixture),
                    "--input", str(public_input), "--owner-result", checked["artifact_path"],
                ],
                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            self.assertEqual(invoked.returncode, 0, invoked.stderr)
            self.assertEqual(json.loads(invoked.stdout), {
                "exit_id": "approved", "task_ref": task_ref,
                "planning_result_id": f"planning:{checkpoint['reviewed_content_sha256']}",
            })
            self.assertFalse(Path(checked["artifact_path"]).exists())

    def test_clarify_scope_uses_real_record_check_and_invoke_wrappers(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            fixture = Path(temp)
            task, owner_input = self.planning_fixture(fixture)
            task_ref = task.relative_to(fixture).as_posix()
            authoring = json.loads(owner_input.read_text(encoding="utf-8"))
            authoring["typed_exit"] = "clarify_scope"
            authoring["consumer"] = {"kind": "workflow", "id": "guru-task-plan-clarify-scope-router"}
            authoring["semantic_review"].update({
                "status": "clarify_scope", "scope_proposals": ["scope-proposal:R13"],
            })
            owner_input.write_text(json.dumps(authoring) + "\n", encoding="utf-8")

            recorded = subprocess.run(
                [
                    str(self.package / "scripts/record-planning-approval.sh"),
                    "--root", str(fixture),
                    "--task", task_ref,
                    "--input", owner_input.relative_to(fixture).as_posix(),
                    "--json",
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(recorded.returncode, 0, recorded)
            owner_result = json.loads(recorded.stdout)
            self.assertEqual(owner_result["typed_exit"], "clarify_scope")

            checked = subprocess.run(
                [
                    str(self.package / "scripts/check-planning-approval.sh"),
                    "--root", str(fixture),
                    "--task", task_ref,
                    "--require-exit", "clarify_scope",
                    "--json",
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(checked.returncode, 0, checked)
            self.assertEqual(json.loads(checked.stdout)["typed_exit"], "clarify_scope")

            public_input = fixture / ".trellis/.runtime/guru-team/evals/public-input.json"
            public_input.parent.mkdir(parents=True, exist_ok=True)
            public_input.write_text(
                json.dumps({
                    "profile": "clarification_reentry",
                    "mode": "workflow",
                    "task_ref": task_ref,
                    "source_exit": "clarify_scope",
                    "reentry_reason": "authority_refreshed",
                }),
                encoding="utf-8",
            )
            checkpoint_relative = (
                Path(".trellis/.runtime/guru-team/owner-checkpoints")
                / task.name
                / "planning-approval.json"
            )
            checkpoint = fixture / checkpoint_relative
            invoked = subprocess.run(
                [
                    str(self.package / "scripts/invoke.sh"),
                    "--root", str(fixture),
                    "--input", public_input.relative_to(fixture).as_posix(),
                    "--owner-result", checkpoint_relative.as_posix(),
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(invoked.returncode, 0, invoked)
            self.assertEqual(
                json.loads(invoked.stdout),
                {
                    "exit_id": "clarify_scope",
                    "task_ref": task_ref,
                    "proposal_refs": ["scope-proposal:R13"],
                },
            )
            self.assertFalse(checkpoint.exists())

    def test_planning_artifact_resolution_is_package_owned_and_compatible(self) -> None:
        command = next(
            item for item in self.read("commands.json")["commands"]
            if item["id"] == "resolve-planning-artifacts"
        )
        self.assertEqual(command["entrypoint"], "runtime/check.py")
        self.assertEqual(command["runtime_role"], "check")
        self.assertEqual(command["side_effect"], "repo_read")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            task = root / ".trellis/tasks/08-12-example"
            task.mkdir(parents=True)
            (task / "prd.md").write_text("# PRD\n", encoding="utf-8")
            wrapper = self.package / "scripts/resolve-human-artifacts.sh"
            result = subprocess.run(
                [str(wrapper), "--root", str(root), "--task", str(task), "--json"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["task_dir_relative"], ".trellis/tasks/08-12-example")
            self.assertEqual(
                [item["exists"] for item in payload["markdown_artifacts"]],
                [True, False, False],
            )
            self.assertEqual(payload["markdown_artifacts"][0]["status"], "已生成")

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
            "runtime_dependency", "task_workspace", "current_authority",
            "planning_documents", "docs_ssot", "wording_result",
            "invocation_freshness",
        ]
        self.assertEqual(self.interface["modes"]["workflow"]["entry_precondition_ids"], expected)
        self.assertEqual(self.interface["modes"]["standalone"]["entry_precondition_ids"], expected)
        self.assertEqual(
            [(item["id"], item["consumer"]) for item in self.interface["external_exits"]],
            [
                ("approved", {"kind": "workflow", "id": "phase-1-task-activation"}),
                ("revision_required", {"kind": "skill", "id": "guru-approve-task-plan"}),
                ("clarify_scope", {"kind": "workflow", "id": "guru-task-plan-clarify-scope-router"}),
                ("blocked", {"kind": "stop", "id": "task-plan-approval-blocked"}),
            ],
        )
        private = self.interface["public_contracts"]["private_artifacts"]
        self.assertEqual(private[0]["persistence"], "ignored_runtime")
        self.assertTrue(private[0]["schema"]["schema_id"].endswith("guru-planning-approval-3.0.json"))
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

        for name in ("initial-review", "revision-reentry", "clarification-reentry"):
            schema = self.read(f"schemas/public-{name}-input.schema.json")
            example = self.read(f"examples/public-{name}-input.json")
            Draft202012Validator(schema).validate(example)
        for name in ("approved", "revision-required", "clarify-scope", "blocked"):
            schema = self.read(f"schemas/public-{name}-output.schema.json")
            example = self.read(f"examples/public-{name}-output.json")
            Draft202012Validator(schema).validate(example)

        consumer_schema = json.loads(
            (self.repo / "consumers/workflow/production/approve-task-plan-approved.schema.json").read_text(encoding="utf-8")
        )
        self.assertTrue(consumer_schema["$id"].endswith("approved-input-3.0"))
        approved = self.read("examples/public-approved-output.json")
        consumer = Draft202012Validator(consumer_schema)
        consumer.validate(approved)
        self.assertFalse(consumer.is_valid({key: value for key, value in approved.items() if key != "planning_result_id"}))
        activation = json.loads(
            (self.package.parent / "guru-activate-task/examples/public-activate-input.json").read_text(encoding="utf-8")
        )
        activation_schema = json.loads(
            (self.package.parent / "guru-activate-task/schemas/public-input.schema.json").read_text(encoding="utf-8")
        )
        activation["activation"]["task_ref"] = approved["task_ref"]
        activation["activation"]["task_id"] = Path(approved["task_ref"]).name
        activation["activation"]["planning_result_id"] = approved["planning_result_id"]
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
                "consumer": {"kind": "skill", "id": "guru-approve-task-plan"},
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
            "workflow": repo / "trellis/workflows/guru-team/workflow.md",
        }
        required = (
            "task_impact_sync(stage=planning)",
            "baseline_current",
            "design constitution",
            "Architecture change contract",
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

        workflow = sources["workflow"].read_text(encoding="utf-8")
        phase = workflow.split("#### 1.4 Task plan approval", 1)[1].split("#### 1.5 Task activation", 1)[0]
        self.assertLess(
            phase.index("task_impact_sync(stage=planning)"),
            phase.index("invoke guru-approve-task-plan"),
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
        self.assertLess(normalized.index("show clickable links to `prd.md`"), normalized.index("resume_target=task_activation"))

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

    def test_public_invoke_consumes_only_the_exact_successful_owner_checkpoint(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(["git", "init", "-b", "main", str(root)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            task_ref = ".trellis/tasks/08-12-planning-consumption"
            task_dir = root / task_ref
            task_dir.mkdir(parents=True)
            checkpoint = root / ".trellis/.runtime/guru-team/owner-checkpoints/08-12-planning-consumption/planning-approval.json"
            checkpoint.parent.mkdir(parents=True)
            owner = copy.deepcopy(self.example)
            owner["mode"] = "workflow"
            owner["task_ref"] = task_ref
            owner["planning_paths"] = [f"{task_ref}/{name}" for name in ("prd.md", "design.md", "implement.md")]
            checkpoint.write_text(json.dumps(owner), encoding="utf-8")
            public_input = root / "public-input.json"
            public_input.write_text(json.dumps({"mode": "workflow", "task_ref": task_ref}), encoding="utf-8")

            result = subprocess.run(
                [str(self.package / "scripts/invoke.sh"), "--root", str(root), "--input", "public-input.json", "--owner-result", checkpoint.relative_to(root).as_posix()],
                cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            self.assertEqual(result.returncode, 0, result)
            self.assertEqual(json.loads(result.stdout), {
                "exit_id": "approved", "task_ref": task_ref,
                "planning_result_id": f"planning:{owner['reviewed_content_sha256']}",
            })
            self.assertFalse(checkpoint.exists())
            self.assertFalse(checkpoint.parent.exists())

            checkpoint.parent.mkdir(parents=True)
            checkpoint.write_text(json.dumps(owner), encoding="utf-8")
            public_input.write_text(json.dumps({"mode": "workflow", "task_ref": ".trellis/tasks/other"}), encoding="utf-8")
            mismatch = subprocess.run(
                [str(self.package / "scripts/invoke.sh"), "--root", str(root), "--input", "public-input.json", "--owner-result", checkpoint.relative_to(root).as_posix()],
                cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            self.assertNotEqual(mismatch.returncode, 0, mismatch)
            self.assertTrue(checkpoint.is_file())

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
        approved = self.read("examples/public-approved-output.json")
        self.assertEqual({"exit_id", "task_ref", "planning_result_id"}, set(approved))
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
        self.assertEqual(self.example["schema_version"], "3.0")
        self.assertEqual(self.example["skill_id"], "guru-approve-task-plan")


if __name__ == "__main__":
    unittest.main()
