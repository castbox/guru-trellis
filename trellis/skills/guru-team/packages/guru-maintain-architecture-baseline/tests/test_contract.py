import copy
import hashlib
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


class ArchitectureBaselineContractTest(unittest.TestCase):
    def setUp(self):
        self.package = Path(__file__).parents[1]

    @staticmethod
    def digest(value):
        return hashlib.sha256(
            json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()

    def load(self, name):
        return json.loads((self.package / "examples" / name).read_text())

    def schema(self, name):
        return json.loads((self.package / "schemas" / name).read_text())

    def assert_schema_valid(self, schema, value):
        errors = list(Draft202012Validator(schema).iter_errors(value))
        self.assertEqual(errors, [], [error.message for error in errors])

    def assert_schema_invalid(self, schema, value):
        self.assertTrue(list(Draft202012Validator(schema).iter_errors(value)))

    def project_check(self, public_input, *, descriptor=None, blocking=True, status="pass"):
        descriptor = descriptor or self.project_check_descriptor()
        check = {
            "schema_version": "2.0",
            "descriptor_identity": descriptor["descriptor_identity"],
            "check_id": descriptor["check_id"],
            "check_version": descriptor["check_version"],
            "applicability": "applicable",
            "blocking": blocking,
            "applicable_scope": copy.deepcopy(descriptor["applicable_scope"]),
            "rule_refs": copy.deepcopy(descriptor["rule_refs"]),
            "decision_refs": copy.deepcopy(descriptor["decision_refs"]),
            "gap_refs": copy.deepcopy(descriptor["gap_refs"]),
            "before": {"state": "one owner and one open GAP"},
            "after": {"state": "one owner and no worsened deviation"},
            "status": status,
            "freshness_identity": public_input["freshness_identity"],
        }
        if status == "unverified":
            check["unavailable_reason"] = "External evidence is unavailable."
        else:
            check["evidence_locator"] = "docs/architecture/evidence/example.md"
        return check

    def project_check_descriptor(self):
        return {
            "schema_version": "2.0",
            "descriptor_identity": "project-architecture:target-boundary:1",
            "check_id": "project-architecture",
            "check_version": "1",
            "entrypoint": "scripts/check-architecture.sh",
            "applicable_scope": ["target-boundary"],
            "rule_refs": ["RULE-owner"],
            "decision_refs": ["ADR-example"],
            "gap_refs": ["GAP-example"],
            "result_contract_identity": "guru-project-architecture-check-result-2.0",
            "freshness_source": "current task candidate",
        }

    @staticmethod
    def committed_range():
        return {
            "base_ref": "origin/main",
            "base_head": "0123456789abcdef0123456789abcdef01234567",
            "review_head": "89abcdef0123456789abcdef0123456789abcdef",
        }

    def architecture_selection(self, public_input, **overrides):
        descriptor = self.project_check_descriptor()
        selected = {
            "typed_exit": "baseline_current",
            "task_locator": public_input["task_locator"],
            "baseline_identity": public_input["baseline"]["identity"],
            "constitution_identity": public_input["constitution"]["identity"],
            "impact_kind": "architecture_impact",
            "impact_reason": "The reviewed task changes an Architecture boundary.",
            "change_path": "target_native",
            "promotion_state": "reviewed_candidate",
            "contribution_locator": "docs/architecture/contributions/example",
            "contribution_identity": "contribution-v1",
            "project_check_descriptors": [descriptor],
            "project_checks": [self.project_check(public_input, descriptor=descriptor)],
        }
        selected.update(overrides)
        return selected

    def contribution(self, public_input, **overrides):
        contribution = {
            "schema_version": "2.0",
            "task_locator": public_input["task_locator"],
            "requirement_authority": "#283",
            "behavior_authority": ".trellis/tasks/example/prd.md",
            "guru_contract_identity": "guru-maintain-architecture-baseline:2.0",
            "baseline_locator": public_input["baseline"]["locator"],
            "baseline_identity": public_input["baseline"]["identity"],
            "baseline_status": "active",
            "constitution_authority_locator": public_input["constitution"]["authority_locator"],
            "constitution_identity_kind": public_input["constitution"]["identity_kind"],
            "constitution_identity": public_input["constitution"]["identity"],
            "change_contract_locator": public_input["project_contract"]["change_contract_locator"],
            "change_contract_identity": public_input["project_contract"]["change_contract_identity"],
            "required_concern_set_identity": public_input["project_contract"]["required_concern_set_identity"],
            "contribution_identity": "contribution-v1",
            "change_path": "target_native",
            "domain_refs": ["DOMAIN-target"],
            "integration_refs": [],
            "decision_refs": ["ADR-example"],
            "gap_refs": ["GAP-example"],
            "required_concerns": [{
                "id": "single-writer",
                "applicability": "applicable",
                "rationale": "The target boundary retains one writer.",
            }],
            "owner_transition": {
                "current": "target-owner",
                "target": "target-owner",
                "single_writer": "target-owner",
            },
            "compatibility": {
                "required": False,
                "owner": "target-owner",
                "exit_condition": "No compatibility layer is introduced.",
            },
            "parallel_scope": {
                "allowed": ["task-owned contribution"],
                "forbidden": ["shared current authority"],
            },
            "deviations": {"closed": [], "retained": ["GAP-example"], "new": []},
            "legacy_deletion_conditions": ["No legacy implementation is introduced."],
            "design_responsibility": {
                "overview": "Keep the public Architecture contract project-neutral.",
                "detailed": "Bind the exact 2.0 schema and runtime projection.",
            },
            "before_plan": "One target owner with one retained GAP.",
            "after_candidate": "The candidate keeps the same owner and does not worsen the GAP.",
            "project_check_descriptors": [self.project_check_descriptor()],
            "project_checks": [self.project_check(public_input)],
            "evidence": {
                "test_refs": ["tests/test_contract.py"],
                "runtime_refs": ["runtime/invoke.py"],
                "external_refs": [],
                "external_status": "not_applicable",
            },
            "expected_current_identity": public_input["baseline"]["identity"],
            "adr": {
                "required": False,
                "locator": "",
                "reason": "The candidate does not create or change an Architecture decision.",
            },
            "review": {
                "status": "pending",
                "independent": False,
                "committed_range": None,
            },
            "promotion": {"state": "required", "promoted_identity": ""},
        }
        contribution.update(overrides)
        return contribution

    def invoke(self, public_input, selected):
        exit_id = selected["typed_exit"]
        owner = {
            "schema_version": "2.0",
            "profile": public_input["profile"],
            "mode": public_input["mode"],
            "continuation_id": public_input["continuation_id"],
            "stage": public_input["stage"],
            "task_locator": public_input["task_locator"],
            "input_sha256": self.digest(public_input),
            "baseline": public_input["baseline"],
            "constitution": public_input["constitution"],
            "project_contract": public_input["project_contract"],
            "freshness_identity": public_input["freshness_identity"],
            "ai_review_gate": {
                "status": "blocked" if exit_id == "blocked" else "passed",
                "reviewed_scope": "Current Architecture authority and task-local change contract.",
                "evidence_summary": "Baseline, constitution, task scope, checks, evidence, and stage identity were reread.",
                "findings": [],
                "conclusion": "The selected typed route is semantically justified.",
            },
            "typed_exit": exit_id,
            "consumer": {
                "baseline_current": {"kind": "workflow", "id": "guru-architecture-baseline-current-router"},
                "sync_required": {"kind": "skill", "id": "guru-maintain-architecture-baseline"},
                "baseline_incomplete": {"kind": "workflow", "id": "guru-architecture-baseline-bootstrap-router"},
                "architecture_conflict": {"kind": "workflow", "id": "guru-architecture-baseline-planning-router"},
                "contract_incomplete": {"kind": "workflow", "id": "guru-architecture-baseline-planning-router"},
                "fitness_regression": {"kind": "workflow", "id": "guru-architecture-baseline-check-router"},
                "blocked": {"kind": "stop", "id": "architecture-baseline-blocked"},
            }[exit_id],
            **selected,
        }
        if public_input["profile"] == "promotion":
            for field in ("expected_current_identity", "current_identity", "sync_kind", "sync_target"):
                owner[field] = copy.deepcopy(public_input[field])
        return subprocess.run(
            [str(self.package / "scripts/invoke.sh"), "--invocation", "-"],
            input=json.dumps({"public_input": public_input, "owner_result": owner}),
            text=True,
            capture_output=True,
            check=False,
        )

    def invoke_canonical(self, public_input, selected):
        exit_id = selected["typed_exit"]
        owner = {
            "schema_version": "2.0",
            "profile": public_input["profile"],
            "mode": public_input["mode"],
            "continuation_id": public_input["continuation_id"],
            "stage": public_input["stage"],
            "task_locator": public_input["task_locator"],
            "input_sha256": self.digest(public_input),
            "baseline": public_input["baseline"],
            "constitution": public_input["constitution"],
            "project_contract": public_input["project_contract"],
            "freshness_identity": public_input["freshness_identity"],
            "ai_review_gate": {
                "status": "blocked" if exit_id == "blocked" else "passed",
                "reviewed_scope": "Current Architecture authority and task-local change contract.",
                "evidence_summary": "Baseline, constitution, task scope, checks, evidence, and stage identity were reread.",
                "findings": [],
                "conclusion": "The selected typed route is semantically justified.",
            },
            "typed_exit": exit_id,
            "consumer": {
                "baseline_current": {"kind": "workflow", "id": "guru-architecture-baseline-current-router"},
                "sync_required": {"kind": "skill", "id": "guru-maintain-architecture-baseline"},
                "baseline_incomplete": {"kind": "workflow", "id": "guru-architecture-baseline-bootstrap-router"},
                "architecture_conflict": {"kind": "workflow", "id": "guru-architecture-baseline-planning-router"},
                "contract_incomplete": {"kind": "workflow", "id": "guru-architecture-baseline-planning-router"},
                "fitness_regression": {"kind": "workflow", "id": "guru-architecture-baseline-check-router"},
                "blocked": {"kind": "stop", "id": "architecture-baseline-blocked"},
            }[exit_id],
            **selected,
        }
        if public_input["profile"] == "promotion":
            for field in ("expected_current_identity", "current_identity", "sync_kind", "sync_target"):
                owner[field] = copy.deepcopy(public_input[field])
        environment = os.environ.copy()
        skills_root = self.package.parents[1]
        if not (skills_root / "runtime/compat.py").is_file():
            source_roots = (Path.cwd().resolve(), *self.package.resolve().parents)
            skills_root = next(
                (
                    root / "trellis/skills/guru-team"
                    for root in source_roots
                    if (root / "trellis/skills/guru-team/runtime/compat.py").is_file()
                ),
                None,
            )
        if skills_root is None:
            return None
        current_pythonpath = environment.get("PYTHONPATH")
        environment["PYTHONPATH"] = str(skills_root) + (
            os.pathsep + current_pythonpath if current_pythonpath else ""
        )
        return subprocess.run(
            [
                sys.executable,
                "-m",
                "runtime.compat",
                "--package-root",
                str(self.package),
                "--validator",
                "public_invocation",
                "--",
                "--invocation",
                "-",
            ],
            input=json.dumps({"public_input": public_input, "owner_result": owner}),
            text=True,
            capture_output=True,
            check=False,
            env=environment,
        )

    def test_preserves_public_graph_identity_and_selects_only_2_0(self):
        interface = json.loads((self.package / "interface.json").read_text())
        aggregate = interface["public_contracts"]["input"]["aggregate_schema"]
        self.assertEqual(
            aggregate,
            {
                "schema_id": "guru-architecture-baseline-input-aggregate-2.0",
                "path": "schemas/public-input-aggregate.schema.json",
            },
        )
        self.assertFalse((self.package / "schemas/public-input.schema.json").exists())
        self.assertEqual(
            {item["id"] for item in interface["public_contracts"]["input"]["profiles"]},
            {"bootstrap_foundation", "task_impact_sync", "promotion", "repair"},
        )
        self.assertEqual(
            {item["id"] for item in interface["external_exits"]},
            {"baseline_current", "sync_required", "baseline_incomplete", "architecture_conflict", "contract_incomplete", "fitness_regression", "blocked"},
        )
        self.assertTrue(all(item["schema"]["schema_id"].endswith("2.0") for item in interface["public_contracts"]["input"]["profiles"]))
        self.assertTrue(all(item["schema"]["schema_id"].endswith("2.0") for item in interface["public_contracts"]["outputs"]))
        for path in (self.package / "schemas").glob("*.json"):
            self.assertNotIn("architecture-baseline-input-aggregate-1.0", path.read_text())
            self.assertNotIn("architecture-baseline-output-current-1.0", path.read_text())

    def test_missing_and_old_schema_versions_are_rejected(self):
        current = self.load("public-input-impact.json")
        for version in (None, "1.0"):
            candidate = json.loads(json.dumps(current))
            if version is None:
                candidate.pop("schema_version")
            else:
                candidate["schema_version"] = version
            result = self.invoke(candidate, {
                "typed_exit": "baseline_current",
                "task_locator": candidate["task_locator"],
                "baseline_identity": candidate["baseline"]["identity"],
                "constitution_identity": candidate["constitution"]["identity"],
                "impact_kind": "no_architecture_impact",
                "promotion_state": "no_change",
            })
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)["code"], "schema_mismatch")

    def test_no_impact_is_lightweight_and_creates_no_contribution_or_adr(self):
        public_input = self.load("public-input-impact.json")
        self.assertNotIn("impact", public_input)
        result = self.invoke(public_input, {
            "typed_exit": "baseline_current",
            "task_locator": public_input["task_locator"],
            "baseline_identity": public_input["baseline"]["identity"],
            "constitution_identity": public_input["constitution"]["identity"],
            "impact_kind": "no_architecture_impact",
            "impact_reason": "The bounded change preserves all Architecture decisions and owners.",
            "promotion_state": "no_change",
        })
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertNotIn("project_check_descriptors", public_input)
        self.assertNotIn("contribution_locator", output)
        self.assertNotIn("project_checks", output)

        no_impact_selection = {
            "typed_exit": "baseline_current",
            "task_locator": public_input["task_locator"],
            "baseline_identity": public_input["baseline"]["identity"],
            "constitution_identity": public_input["constitution"]["identity"],
            "impact_kind": "no_architecture_impact",
            "impact_reason": "The bounded change preserves all Architecture decisions and owners.",
            "promotion_state": "no_change",
        }
        owner_descriptor_copy = copy.deepcopy(no_impact_selection)
        owner_descriptor_copy["project_check_descriptors"] = [
            self.project_check_descriptor()
        ]
        result = self.invoke(public_input, owner_descriptor_copy)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["code"], "semantic_result_invalid")

    def test_architecture_impact_rejects_no_change_promotion_state(self):
        public_input = self.load("public-input-impact-architecture.json")
        result = self.invoke(
            public_input,
            self.architecture_selection(public_input, promotion_state="no_change"),
        )
        self.assertEqual(result.returncode, 3)
        error = json.loads(result.stdout)
        self.assertEqual(error["code"], "semantic_result_invalid")
        self.assertEqual(error["field_path"], "owner_result.promotion_state")

        current_output = {
            "exit_id": "baseline_current",
            "task_locator": public_input["task_locator"],
            "stage": public_input["stage"],
            "baseline_identity": public_input["baseline"]["identity"],
            "constitution_identity": public_input["constitution"]["identity"],
            "impact_kind": "architecture_impact",
            "promotion_state": "no_change",
            "contribution_locator": "docs/architecture/contributions/example",
            "contribution_identity": "contribution-v1",
            "freshness_identity": public_input["freshness_identity"],
        }
        output_schema = self.schema("public-baseline-current-output.schema.json")
        consumer_schema = json.loads(
            (self.package / "consumers/workflow/current.schema.json").read_text()
        )
        self.assert_schema_invalid(output_schema, current_output)
        self.assert_schema_invalid(consumer_schema, current_output)
        for promotion_state in ("reviewed_candidate", "reviewed_promoted"):
            with self.subTest(promotion_state=promotion_state):
                candidate = {**current_output, "promotion_state": promotion_state}
                self.assert_schema_valid(output_schema, candidate)
                self.assert_schema_valid(consumer_schema, candidate)

    def test_three_architecture_paths_are_mutually_exclusive(self):
        public_schema = json.loads((self.package / "schemas/public-input-impact.schema.json").read_text())
        semantic_schema = json.loads((self.package / "schemas/semantic-result.schema.json").read_text())
        contribution_schema = json.loads((self.package / "schemas/architecture-contribution.schema.json").read_text())
        self.assertNotIn("impact_kind", public_schema["properties"])
        self.assertNotIn("change_path", public_schema["properties"])
        paths = semantic_schema["properties"]["change_path"]["enum"]
        self.assertEqual(paths, ["target_native", "legacy_boundary_convergence", "dedicated_refactor_slice"])
        self.assertEqual(contribution_schema["properties"]["change_path"]["enum"], paths)
        self.assertNotIn("no_architecture_impact", paths)

    def test_architecture_contribution_binds_both_contract_authorities(self):
        contribution = self.schema("architecture-contribution.schema.json")
        authority_fields = {
            "guru_contract_identity",
            "baseline_locator",
            "baseline_identity",
            "baseline_status",
            "constitution_authority_locator",
            "constitution_identity_kind",
            "constitution_identity",
            "change_contract_locator",
            "change_contract_identity",
            "required_concern_set_identity",
        }
        self.assertTrue(authority_fields.issubset(contribution["required"]))
        self.assertTrue(authority_fields.issubset(contribution["properties"]))
        self.assertEqual(
            contribution["properties"]["guru_contract_identity"]["const"],
            "guru-maintain-architecture-baseline:2.0",
        )
        self.assertEqual(
            contribution["properties"]["baseline_status"]["enum"],
            ["draft", "active", "superseded"],
        )
        self.assertEqual(
            contribution["properties"]["constitution_identity_kind"]["enum"],
            ["version", "content"],
        )

    def test_constitution_is_exactly_five_identity_name_pairs_without_checklist_fields(self):
        public_input = self.load("public-input-impact.json")
        principles = public_input["constitution"]["principles"]
        self.assertEqual([item["id"] for item in principles], [
            "mature-practice-applicability",
            "concept-semantic-completeness",
            "cohesion-change-isolation",
            "minimum-necessary-complexity",
            "debt-one-way-convergence",
        ])
        package_text = "\n".join(path.read_text() for path in (self.package / "schemas").glob("*.json"))
        self.assertNotIn('"score"', package_text)
        self.assertNotIn('"verdict"', package_text)
        self.assertNotIn('"principle_prose"', package_text)
        self.assertNotIn('"prefixItems"', package_text)
        self.assertNotIn('"items": false', package_text)

        profile_contracts = [
            ("public-input-bootstrap.schema.json", "public-input-bootstrap.json"),
            ("public-input-impact.schema.json", "public-input-impact.json"),
            ("public-input-promotion.schema.json", "public-input-promotion.json"),
            ("public-input-repair.schema.json", "public-input-repair.json"),
        ]
        for schema_name, example_name in profile_contracts:
            with self.subTest(schema=schema_name):
                schema = self.schema(schema_name)
                example = self.load(example_name)
                reordered = copy.deepcopy(example)
                reordered["constitution"]["principles"].reverse()
                self.assert_schema_valid(schema, reordered)

                duplicate = copy.deepcopy(example)
                duplicate["constitution"]["principles"][-1] = copy.deepcopy(
                    duplicate["constitution"]["principles"][0]
                )
                self.assert_schema_invalid(schema, duplicate)

                missing = copy.deepcopy(example)
                missing["constitution"]["principles"].pop()
                self.assert_schema_invalid(schema, missing)

                mismatched_name = copy.deepcopy(example)
                mismatched_name["constitution"]["principles"][0]["short_name"] = "错误短名称"
                self.assert_schema_invalid(schema, mismatched_name)

        semantic_schema = self.schema("semantic-result.schema.json")
        semantic_principles = copy.deepcopy(
            semantic_schema["$defs"]["constitution"]["properties"]["principles"]
        )
        semantic_principles["$defs"] = semantic_schema["$defs"]
        self.assert_schema_valid(semantic_principles, list(reversed(principles)))
        self.assert_schema_invalid(semantic_principles, [*principles[:-1], copy.deepcopy(principles[0])])
        self.assert_schema_invalid(semantic_principles, principles[:-1])
        mismatched_semantic_name = copy.deepcopy(principles)
        mismatched_semantic_name[0]["short_name"] = "错误短名称"
        self.assert_schema_invalid(semantic_principles, mismatched_semantic_name)

    def test_task_locator_is_bound_and_bootstrap_current_uses_active_successor(self):
        public_input = self.load("public-input-bootstrap.json")
        selected = {
            "typed_exit": "baseline_current",
            "task_locator": public_input["task_locator"],
            "baseline_identity": public_input["successor_baseline"]["identity"],
            "constitution_identity": public_input["constitution"]["identity"],
            "impact_kind": "no_architecture_impact",
            "impact_reason": "Bootstrap preserves the caller task identity.",
            "promotion_state": "no_change",
        }
        result = self.invoke(public_input, selected)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["task_locator"], public_input["task_locator"])
        self.assertEqual(
            json.loads(result.stdout)["baseline_identity"],
            public_input["successor_baseline"]["identity"],
        )

        selected["task_locator"] = ".trellis/tasks/wrong-task"
        result = self.invoke(public_input, selected)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["code"], "stale_identity")

        wrong_locator = copy.deepcopy(public_input)
        wrong_locator["successor_baseline"]["locator"] = "docs/architecture/other.md"
        selected["task_locator"] = public_input["task_locator"]
        result = self.invoke(wrong_locator, selected)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(
            json.loads(result.stdout)["field_path"],
            "public_input.successor_baseline.locator",
        )

        reused_identity = copy.deepcopy(public_input)
        reused_identity["successor_baseline"]["identity"] = reused_identity["baseline"]["identity"]
        selected["baseline_identity"] = reused_identity["baseline"]["identity"]
        result = self.invoke(reused_identity, selected)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(
            json.loads(result.stdout)["field_path"],
            "public_input.successor_baseline.identity",
        )

        repair = self.load("public-input-repair.json")
        repair_schema = self.schema("public-input-repair.schema.json")
        self.assert_schema_valid(repair_schema, repair)
        for status in ("missing", "draft", "superseded"):
            with self.subTest(repair_status=status):
                invalid_repair = copy.deepcopy(repair)
                invalid_repair["baseline"]["status"] = status
                self.assert_schema_invalid(repair_schema, invalid_repair)

    def test_applicable_unverified_check_cannot_return_current(self):
        public_input = self.load("public-input-impact-architecture.json")
        check = self.project_check(public_input, blocking=True, status="unverified")
        result = self.invoke(public_input, self.architecture_selection(
            public_input,
            project_checks=[check],
        ))
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["code"], "semantic_result_invalid")

    def test_nonblocking_unverified_check_preserves_evidence_gap(self):
        public_input = self.load("public-input-impact-architecture.json")
        check = self.project_check(public_input, blocking=False, status="unverified")
        check["unavailable_reason"] = "External evidence is unavailable and is not required by this task."
        result = self.invoke(public_input, self.architecture_selection(
            public_input,
            project_checks=[check],
        ))
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_branch_review_requires_independent_committed_full_diff(self):
        public_input = self.load("public-input-impact-architecture.json")
        public_input["stage"] = "branch_review"
        public_input["committed_range"] = self.committed_range()
        selected = self.architecture_selection(public_input)
        result = self.invoke(public_input, selected)
        self.assertEqual(result.returncode, 3)
        selected["review"] = {
            "status": "reviewed",
            "independent": True,
            "committed_range": copy.deepcopy(public_input["committed_range"]),
        }
        result = self.invoke(public_input, selected)
        self.assertEqual(result.returncode, 0, result.stderr)

        mismatched_range = copy.deepcopy(selected)
        mismatched_range["review"]["committed_range"]["review_head"] = (
            "fedcba9876543210fedcba9876543210fedcba98"
        )
        result = self.invoke(public_input, mismatched_range)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["field_path"], "owner_result.review")

    def test_sync_kinds_use_their_actual_stale_identity(self):
        public_input = self.load("public-input-impact.json")
        cases = [
            {
                "sync_kind": "baseline_advanced",
                "expected_current_identity": "current-v1",
                "current_identity": "current-v2",
                "sync_target": {"kind": "baseline", "locator": "docs/architecture/README.md", "expected_identity": "current-v1", "current_identity": "current-v2"},
            },
            {
                "sync_kind": "constitution_advanced",
                "expected_current_identity": "current-v1",
                "current_identity": "current-v1",
                "sync_target": {"kind": "constitution", "locator": "docs/architecture/00-foundation/design-constitution.md", "expected_identity": "constitution-v1", "current_identity": "constitution-v2"},
            },
            {
                "sync_kind": "contribution_stale",
                "expected_current_identity": "current-v1",
                "current_identity": "current-v1",
                "sync_target": {"kind": "contribution", "locator": "docs/architecture/contributions/example", "expected_identity": "contribution-v1", "current_identity": "contribution-v2"},
            },
            {
                "sync_kind": "repair",
                "expected_current_identity": "current-v1",
                "current_identity": "current-v1",
                "sync_target": {"kind": "project_contract", "locator": "docs/architecture/06-governance/change-contract.md", "expected_identity": "project-change-contract-v1", "current_identity": "project-change-contract-v1"},
            },
        ]
        for case in cases:
            with self.subTest(sync_kind=case["sync_kind"]):
                selected = {
                    "typed_exit": "sync_required",
                    "task_locator": public_input["task_locator"],
                    **case,
                }
                result = self.invoke(public_input, selected)
                self.assertEqual(result.returncode, 0, result.stderr)
                output = json.loads(result.stdout)
                self.assertEqual(output["sync_target"], case["sync_target"])
                self.assertNotIn("contribution_locator", output)

    def test_sync_kind_mismatches_fail_closed(self):
        public_input = self.load("public-input-impact.json")
        invalid = [
            {
                "sync_kind": "baseline_advanced",
                "expected_current_identity": "current-v1",
                "current_identity": "current-v1",
                "sync_target": {"kind": "baseline", "locator": "docs/architecture/README.md", "expected_identity": "current-v1", "current_identity": "current-v1"},
            },
            {
                "sync_kind": "constitution_advanced",
                "expected_current_identity": "current-v1",
                "current_identity": "current-v1",
                "sync_target": {"kind": "constitution", "locator": "docs/architecture/00-foundation/design-constitution.md", "expected_identity": "constitution-v1", "current_identity": "constitution-v1"},
            },
            {
                "sync_kind": "contribution_stale",
                "expected_current_identity": "current-v1",
                "current_identity": "current-v1",
                "sync_target": {"kind": "baseline", "locator": "docs/architecture/README.md", "expected_identity": "contribution-v1", "current_identity": "contribution-v2"},
            },
            {
                "sync_kind": "repair",
                "expected_current_identity": "current-v1",
                "current_identity": "current-v1",
                "sync_target": {"kind": "baseline", "locator": "docs/architecture/README.md", "expected_identity": "current-v1", "current_identity": "current-v1"},
            },
            {
                "sync_kind": "repair",
                "expected_current_identity": "current-v1",
                "current_identity": "current-v1",
                "sync_target": {"kind": "project_contract", "locator": "docs/architecture/06-governance/other-contract.md", "expected_identity": "project-change-contract-v1", "current_identity": "project-change-contract-v1"},
            },
        ]
        for case in invalid:
            with self.subTest(sync_kind=case["sync_kind"]):
                result = self.invoke(public_input, {
                    "typed_exit": "sync_required",
                    "task_locator": public_input["task_locator"],
                    **case,
                })
                self.assertEqual(result.returncode, 3)

    def test_promotion_required_needs_current_reviewed_contribution_and_successor(self):
        public_input = self.load("public-input-promotion.json")
        target = public_input["sync_target"]
        selected = self.architecture_selection(
            public_input,
            promotion_state="reviewed_promoted",
            contribution_locator=target["locator"],
            contribution_identity=target["current_identity"],
            review={
                "status": "reviewed",
                "independent": True,
                "committed_range": copy.deepcopy(public_input["committed_range"]),
            },
        )
        result = self.invoke(public_input, selected)
        self.assertEqual(result.returncode, 0, result.stderr)

        stale_baseline = copy.deepcopy(public_input)
        stale_baseline["baseline"]["identity"] = stale_baseline["expected_current_identity"]
        selected["baseline_identity"] = stale_baseline["baseline"]["identity"]
        result = self.invoke(stale_baseline, selected)
        self.assertEqual(result.returncode, 3)

        wrong_contribution = self.architecture_selection(
            public_input,
            promotion_state="reviewed_promoted",
            contribution_locator=target["locator"],
            contribution_identity="stale-contribution",
            review={
                "status": "reviewed",
                "independent": True,
                "committed_range": copy.deepcopy(public_input["committed_range"]),
            },
        )
        result = self.invoke(public_input, wrong_contribution)
        self.assertEqual(result.returncode, 3)

        wrong_range = self.architecture_selection(
            public_input,
            promotion_state="reviewed_promoted",
            contribution_locator=target["locator"],
            contribution_identity=target["current_identity"],
            review={
                "status": "reviewed",
                "independent": True,
                "committed_range": copy.deepcopy(public_input["committed_range"]),
            },
        )
        wrong_range["review"]["committed_range"]["base_ref"] = "origin/other"
        result = self.invoke(public_input, wrong_range)
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["field_path"], "owner_result.review")

    def test_each_sync_output_seed_merges_with_authoring_into_promotion_input(self):
        interface = json.loads((self.package / "interface.json").read_text())
        sync_projection = next(
            item for item in interface["public_contracts"]["projections"]
            if item["id"] == "sync_projection"
        )
        contract = next(
            item["contract"] for item in interface["public_contracts"]["consumer_inputs"]
            if item["id"] == "sync_input"
        )
        authoring = self.load("public-promotion-authoring.json")
        self.assertEqual(set(authoring), set(contract["authoring_fields"]))
        required = set(self.schema("public-input-promotion.schema.json")["required"])
        self.assertEqual(set(contract["seed_fields"]) | set(contract["authoring_fields"]), required)
        self.assertFalse(set(contract["seed_fields"]) & set(contract["authoring_fields"]))
        outputs = [
            {"sync_kind": "promotion_required", "expected_current_identity": "current-v1", "current_identity": "current-v1", "sync_target": {"kind": "contribution", "locator": "docs/architecture/contributions/example", "expected_identity": "contribution-v1", "current_identity": "contribution-v1"}},
            {"sync_kind": "baseline_advanced", "expected_current_identity": "current-v1", "current_identity": "current-v2", "sync_target": {"kind": "baseline", "locator": "docs/architecture/README.md", "expected_identity": "current-v1", "current_identity": "current-v2"}},
            {"sync_kind": "constitution_advanced", "expected_current_identity": "current-v2", "current_identity": "current-v2", "sync_target": {"kind": "constitution", "locator": "docs/architecture/00-foundation/design-constitution.md", "expected_identity": "constitution-v1", "current_identity": "constitution-v2"}},
            {"sync_kind": "contribution_stale", "expected_current_identity": "current-v2", "current_identity": "current-v2", "sync_target": {"kind": "contribution", "locator": "docs/architecture/contributions/example", "expected_identity": "contribution-v1", "current_identity": "contribution-v2"}},
            {"sync_kind": "repair", "expected_current_identity": "current-v2", "current_identity": "current-v2", "sync_target": {"kind": "project_contract", "locator": "docs/architecture/06-governance/change-contract.md", "expected_identity": "project-change-contract-v1", "current_identity": "project-change-contract-v1"}},
        ]
        schema = self.schema("public-input-promotion.schema.json")
        for case in outputs:
            with self.subTest(sync_kind=case["sync_kind"]):
                output = {
                    "exit_id": "sync_required",
                    "task_locator": ".trellis/tasks/example",
                    "stage": "acceptance_finish",
                    "freshness_identity": "promotion-fresh-v1",
                    **case,
                }
                seed = {
                    mapping["target"]: copy.deepcopy(output[mapping["source"]])
                    for mapping in sync_projection["mappings"]
                }
                self.assertEqual(set(seed), set(contract["seed_fields"]))
                merged = {**authoring, **seed}
                self.assert_schema_valid(schema, merged)

    def test_review_and_project_check_conditions_are_closed_and_duplicated_consistently(self):
        semantic = self.schema("semantic-result.schema.json")
        contribution = self.schema("architecture-contribution.schema.json")
        descriptor = self.schema("project-architecture-check-descriptor.schema.json")
        project_check = self.schema("project-architecture-check-result.schema.json")
        self.assertEqual(semantic["properties"]["review"], contribution["properties"]["review"])
        self.assertIn("project_check_descriptors", semantic["properties"])
        for public_schema in (
            self.schema("public-input-impact.schema.json"),
            self.schema("public-input-promotion.schema.json"),
        ):
            self.assertNotIn("project_check_descriptors", public_schema["required"])
            self.assertNotIn("project_check_descriptors", public_schema["properties"])
            self.assertNotIn("projectCheckDescriptor", public_schema["$defs"])
        descriptor_copies = [
            semantic["$defs"]["projectCheckDescriptor"],
            contribution["$defs"]["projectCheckDescriptor"],
        ]
        for candidate in descriptor_copies:
            self.assertEqual(candidate["required"], descriptor["required"])
            self.assertEqual(candidate["anyOf"], descriptor["anyOf"])
            self.assertEqual(candidate["properties"], descriptor["properties"])
        self.assert_schema_valid(
            descriptor,
            self.load("project-architecture-check-descriptor.json"),
        )
        self.assert_schema_valid(
            project_check,
            self.load("project-architecture-check-result.json"),
        )
        project_check_copies = [semantic["$defs"]["projectCheck"], contribution["$defs"]["projectCheck"], project_check]
        for candidate in project_check_copies:
            self.assertEqual(candidate["required"], project_check["required"])
            self.assertEqual(candidate["anyOf"], project_check["anyOf"])
            self.assertEqual(candidate["allOf"], project_check["allOf"])
            for field in ("status", "evidence_locator", "unavailable_reason", "applicability", "blocking"):
                self.assertEqual(candidate["properties"][field], project_check["properties"][field])

        review_schema = copy.deepcopy(semantic["properties"]["review"])
        review_schema["$defs"] = semantic["$defs"]
        pending_review = {"status": "pending", "independent": False, "committed_range": None}
        self.assert_schema_valid(review_schema, pending_review)
        invalid_pending = {
            "status": "pending",
            "independent": True,
            "committed_range": self.committed_range(),
        }
        self.assert_schema_invalid(review_schema, invalid_pending)

        public_input = self.load("public-input-impact-architecture.json")
        legal_checks = [
            self.project_check(public_input, status="pass"),
            self.project_check(public_input, blocking=False, status="fail"),
            self.project_check(public_input, blocking=False, status="unverified"),
            {
                **self.project_check(public_input, blocking=False, status="pass"),
                "applicability": "not_applicable",
            },
        ]
        for check in legal_checks:
            self.assert_schema_valid(project_check, check)

        invalid_checks = []
        missing_evidence = self.project_check(public_input, status="pass")
        missing_evidence.pop("evidence_locator")
        invalid_checks.append(missing_evidence)
        mixed_evidence = self.project_check(public_input, status="fail")
        mixed_evidence["unavailable_reason"] = "Unavailable."
        invalid_checks.append(mixed_evidence)
        unverified_with_evidence = self.project_check(public_input, blocking=False, status="unverified")
        unverified_with_evidence["evidence_locator"] = "docs/architecture/evidence/example.md"
        invalid_checks.append(unverified_with_evidence)
        not_applicable_blocking = self.project_check(public_input, blocking=True, status="pass")
        not_applicable_blocking["applicability"] = "not_applicable"
        invalid_checks.append(not_applicable_blocking)
        not_applicable_failed = self.project_check(public_input, blocking=False, status="fail")
        not_applicable_failed["applicability"] = "not_applicable"
        invalid_checks.append(not_applicable_failed)
        not_applicable_unverified = self.project_check(public_input, blocking=False, status="unverified")
        not_applicable_unverified["applicability"] = "not_applicable"
        invalid_checks.append(not_applicable_unverified)
        for check in invalid_checks:
            self.assert_schema_invalid(project_check, check)

    def test_project_check_descriptors_and_results_are_bound_one_to_one(self):
        public_input = self.load("public-input-impact-architecture.json")
        descriptor = self.project_check_descriptor()
        check = self.project_check(public_input, descriptor=descriptor)
        selection = self.architecture_selection(
            public_input,
            project_check_descriptors=[descriptor],
            project_checks=[check],
        )

        self.assertNotIn("project_check_descriptors", public_input)
        result = self.invoke_canonical(public_input, selection)
        if result is not None:
            self.assertEqual(result.returncode, 0, result.stderr)
        result = self.invoke(public_input, selection)
        self.assertEqual(result.returncode, 0, result.stderr)

        public_with_owner_field = copy.deepcopy(public_input)
        public_with_owner_field["project_check_descriptors"] = [descriptor]
        for invoke in (self.invoke_canonical, self.invoke):
            result = invoke(public_with_owner_field, selection)
            if result is None:
                continue
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)["code"], "schema_mismatch")

        mismatch_cases = [
            ("descriptor_identity", "unregistered-descriptor"),
            ("check_id", "unregistered-check"),
            ("check_version", "999"),
            ("applicable_scope", ["legacy-boundary"]),
            ("rule_refs", ["RULE-other"]),
            ("decision_refs", ["ADR-other"]),
            ("gap_refs", ["GAP-other"]),
        ]
        for field, value in mismatch_cases:
            with self.subTest(field=field):
                mismatched = copy.deepcopy(check)
                mismatched[field] = value
                result = self.invoke(
                    public_input,
                    self.architecture_selection(
                        public_input,
                        project_check_descriptors=[descriptor],
                        project_checks=[mismatched],
                    ),
                )
                self.assertEqual(result.returncode, 3)
                self.assertEqual(json.loads(result.stdout)["code"], "semantic_result_invalid")

        duplicate_descriptor = copy.deepcopy(descriptor)
        duplicate_descriptor["check_id"] = "project-architecture-duplicate"
        duplicate_descriptor["entrypoint"] = "scripts/check-architecture-again.sh"
        result = self.invoke(
            public_input,
            self.architecture_selection(
                public_input,
                project_check_descriptors=[descriptor, duplicate_descriptor],
                project_checks=[check],
            ),
        )
        self.assertEqual(result.returncode, 3)

        extra_descriptor = copy.deepcopy(descriptor)
        extra_descriptor["descriptor_identity"] = "project-architecture:legacy-boundary:1"
        extra_descriptor["check_id"] = "project-architecture-extra"
        result = self.invoke(
            public_input,
            self.architecture_selection(
                public_input,
                project_check_descriptors=[descriptor, extra_descriptor],
                project_checks=[check],
            ),
        )
        self.assertEqual(result.returncode, 3)

        duplicate_check = copy.deepcopy(check)
        duplicate_check["after"] = {"state": "same identity with a second result"}
        result = self.invoke(
            public_input,
            self.architecture_selection(public_input, project_checks=[check, duplicate_check]),
        )
        self.assertEqual(result.returncode, 3)

        second_descriptor = copy.deepcopy(descriptor)
        second_descriptor["descriptor_identity"] = "project-architecture:legacy-boundary:1"
        second_descriptor["entrypoint"] = "scripts/check-legacy-architecture.sh"
        second_descriptor["applicable_scope"] = ["legacy-boundary"]
        second_descriptor["rule_refs"] = ["RULE-legacy-owner"]
        second_check = self.project_check(public_input, descriptor=second_descriptor)
        result = self.invoke(
            public_input,
            self.architecture_selection(
                public_input,
                project_check_descriptors=[descriptor, second_descriptor],
                project_checks=[check, second_check],
            ),
        )
        self.assertEqual(result.returncode, 0, result.stderr)

        unsafe_descriptor = copy.deepcopy(descriptor)
        unsafe_descriptor["entrypoint"] = "../scripts/check-architecture.sh"
        result = self.invoke(
            public_input,
            self.architecture_selection(
                public_input,
                project_check_descriptors=[unsafe_descriptor],
                project_checks=[self.project_check(public_input, descriptor=unsafe_descriptor)],
            ),
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["code"], "unsafe_path")

    def test_not_applicable_requires_non_blocking_passed_evidence(self):
        public_input = self.load("public-input-impact-architecture.json")
        descriptor = self.project_check_descriptor()

        accepted = self.project_check(
            public_input,
            descriptor=descriptor,
            blocking=False,
            status="pass",
        )
        accepted["applicability"] = "not_applicable"
        accepted_selection = self.architecture_selection(
            public_input,
            project_check_descriptors=[descriptor],
            project_checks=[accepted],
        )
        for invoke in (self.invoke_canonical, self.invoke):
            result = invoke(public_input, accepted_selection)
            if result is None:
                continue
            self.assertEqual(result.returncode, 0, result.stderr)

        for status in ("fail", "unverified"):
            with self.subTest(status=status):
                rejected = self.project_check(
                    public_input,
                    descriptor=descriptor,
                    blocking=False,
                    status=status,
                )
                rejected["applicability"] = "not_applicable"
                rejected_selection = self.architecture_selection(
                    public_input,
                    project_check_descriptors=[descriptor],
                    project_checks=[rejected],
                )
                for invoke in (self.invoke_canonical, self.invoke):
                    result = invoke(public_input, rejected_selection)
                    if result is None:
                        continue
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(json.loads(result.stdout)["code"], "schema_mismatch")

    def test_project_checks_require_at_least_one_authority_reference_everywhere(self):
        public_input = self.load("public-input-impact-architecture.json")
        empty_refs = self.project_check(public_input)
        empty_refs["rule_refs"] = []
        empty_refs["decision_refs"] = []
        empty_refs["gap_refs"] = []

        self.assert_schema_invalid(
            self.schema("project-architecture-check-result.schema.json"),
            empty_refs,
        )

        descriptor = self.project_check_descriptor()
        descriptor["rule_refs"] = []
        descriptor["decision_refs"] = []
        descriptor["gap_refs"] = []
        self.assert_schema_invalid(
            self.schema("project-architecture-check-descriptor.schema.json"),
            descriptor,
        )

        contribution = self.contribution(public_input)
        contribution["project_checks"] = [empty_refs]
        self.assert_schema_invalid(
            self.schema("architecture-contribution.schema.json"),
            contribution,
        )

        result = self.invoke(
            public_input,
            self.architecture_selection(public_input, project_checks=[empty_refs]),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["code"], "schema_mismatch")

    def test_contribution_closes_adr_promotion_and_review_conditions(self):
        public_input = self.load("public-input-impact-architecture.json")
        schema = self.schema("architecture-contribution.schema.json")
        contribution = self.contribution(public_input)
        self.assert_schema_valid(schema, contribution)

        adr_required_without_locator = copy.deepcopy(contribution)
        adr_required_without_locator["adr"]["required"] = True
        self.assert_schema_invalid(schema, adr_required_without_locator)

        adr_not_required_with_locator = copy.deepcopy(contribution)
        adr_not_required_with_locator["adr"]["locator"] = "docs/architecture/adr/283.md"
        self.assert_schema_invalid(schema, adr_not_required_with_locator)

        adr_required = copy.deepcopy(contribution)
        adr_required["adr"] = {
            "required": True,
            "locator": "docs/architecture/adr/283.md",
            "reason": "The contribution changes an Architecture decision.",
        }
        self.assert_schema_valid(schema, adr_required)

        required_with_promoted_identity = copy.deepcopy(contribution)
        required_with_promoted_identity["promotion"]["promoted_identity"] = "current-v2"
        self.assert_schema_invalid(schema, required_with_promoted_identity)

        promoted_without_identity = copy.deepcopy(contribution)
        promoted_without_identity["promotion"]["state"] = "reviewed_promoted"
        self.assert_schema_invalid(schema, promoted_without_identity)

        promoted_with_pending_review = copy.deepcopy(contribution)
        promoted_with_pending_review["promotion"] = {
            "state": "reviewed_promoted",
            "promoted_identity": "current-v2",
        }
        self.assert_schema_invalid(schema, promoted_with_pending_review)

        reviewed_promoted = copy.deepcopy(promoted_with_pending_review)
        reviewed_promoted["review"] = {
            "status": "reviewed",
            "independent": True,
            "committed_range": self.committed_range(),
        }
        self.assert_schema_valid(schema, reviewed_promoted)

    def test_stale_authority_binding_fails_closed(self):
        public_input = self.load("public-input-impact.json")
        selected = {
            "typed_exit": "blocked",
            "reason_code": "stale_identity",
            "remediation": "Reread.",
        }
        result = self.invoke(public_input, selected)
        self.assertEqual(result.returncode, 0, result.stderr)
        envelope = json.loads(json.dumps(public_input))
        owner_baseline = dict(envelope["baseline"])
        owner_baseline["identity"] = "stale"
        owner = {
            "schema_version": "2.0", "profile": envelope["profile"], "mode": envelope["mode"],
            "continuation_id": envelope["continuation_id"], "stage": envelope["stage"],
            "task_locator": envelope["task_locator"],
            "input_sha256": self.digest(envelope), "baseline": owner_baseline,
            "constitution": envelope["constitution"], "project_contract": envelope["project_contract"],
            "freshness_identity": envelope["freshness_identity"],
            "ai_review_gate": {"status": "blocked", "reviewed_scope": "authority", "evidence_summary": "live", "findings": ["stale"], "conclusion": "blocked"},
            "typed_exit": "blocked", "consumer": {"kind": "stop", "id": "architecture-baseline-blocked"},
            "reason_code": "stale_identity", "remediation": "Reread.",
        }
        result = subprocess.run(
            [str(self.package / "scripts/invoke.sh"), "--invocation", "-"],
            input=json.dumps({"public_input": envelope, "owner_result": owner}),
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 3)
        self.assertEqual(json.loads(result.stdout)["code"], "stale_identity")

    def test_eval_inventory_covers_the_ten_approved_project_neutral_scenarios(self):
        evals = json.loads((self.package / "evals/evals.json").read_text())["evals"]
        self.assertEqual([item["id"] for item in evals], [
            "no-impact", "target-native", "legacy-boundary-convergence",
            "dedicated-refactor-slice", "scope-expansion", "fitness-regression",
            "parallel-stale", "unpromoted-contribution", "next-task-consumption",
            "missing-external-evidence",
        ])
        text = json.dumps(evals).lower()
        for private_term in ("afizzy", "flutter", "viewmodel", "controller"):
            self.assertNotIn(private_term, text)


if __name__ == "__main__":
    unittest.main()
