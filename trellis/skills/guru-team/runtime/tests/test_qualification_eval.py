from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SKILLS = Path(__file__).resolve().parents[2]
REPO = SKILLS.parents[2]
sys.path.insert(0, str(SKILLS))

from adapters.eval import native_adapter  # noqa: E402
from runtime import eval_runner  # noqa: E402


class QualificationEvalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.skills = self.root / "skills"
        self.package = self.skills / "packages/guru-qualify-normal-scenario"
        (self.skills / "schemas").mkdir(parents=True)
        (self.package / "schemas").mkdir(parents=True)
        for name in (
            "skill-eval-adapter-request-3.0.schema.json",
            "skill-eval-control-map-1.0.schema.json",
            "skill-eval-run-4.0.schema.json",
        ):
            (self.skills / "schemas" / name).write_bytes(
                (SKILLS / "schemas" / name).read_bytes()
            )
        (self.package / "schemas/public-classified-output.schema.json").write_text(
            json.dumps({
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "additionalProperties": False,
                "required": ["exit_id", "candidate_results"],
                "properties": {
                    "exit_id": {"const": "classified"},
                    "candidate_results": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "required": ["candidate_ref", "decision"],
                            "properties": {
                                "candidate_ref": {"type": "string"},
                                "decision": {"type": "string"},
                            },
                        },
                    },
                },
            }),
            encoding="utf-8",
        )
        (self.package / "SKILL.md").write_text("# Qualification\n", encoding="utf-8")
        self.interface = {
            "schema_version": "1.6",
            "id": "guru-qualify-normal-scenario",
            "public_contracts": {
                "invocation": {
                    "wrapper": "scripts/invoke.sh",
                    "input_binding": {
                        "kind": "structured_json",
                        "profile_selector": {
                            "source": "aggregate_public_input",
                            "field": "profile",
                        },
                    },
                    "example_argv": ["--invocation", "-"],
                },
                "outputs": [{
                    "exit_id": "classified",
                    "schema": {
                        "id": "test-classified-output",
                        "path": "schemas/public-classified-output.schema.json",
                    },
                }],
            },
        }
        self.case = {
            "id": "implementation-discovery-rejected",
            "prompt": "Review the declared implementation discovery candidate.",
            "input_profile_id": "implementation_discovery",
            "scenario_id": "issue-236-shell-scanner",
            "scenario_kind": "rejected",
            "pair_id": "shell-scanner",
            "pressure_framing": "attack_security",
            "expected_exit": "classified",
            "expected_decisions": [{
                "candidate_ref": "candidate-1",
                "decision": "rejected_out_of_scope",
            }],
            "expected_output": "classified",
            "assertions": {
                "semantic": [{
                    "id": "scope-first-decision",
                    "criterion": "The typed decision follows the current scope-first contract.",
                    "evidence_selector": "output",
                }],
            },
        }
        self.evals = {
            "production_gate": {
                "model_id": "gpt-5.6-sol",
                "fresh_invocations_per_case": 5,
                "required_passes_per_case": 5,
            },
            "evals": [self.case],
        }
        self.package_sha256 = eval_runner.tree_sha256(self.package)
        self.discovery = {
            "corpus_sha256": "1" * 64,
            "matrix_sha256": "2" * 64,
            "package_sha256": self.package_sha256,
        }
        self.identity = {
            "authority_repository": "castbox/guru-trellis",
            "authority_issue": 237,
            "authority_state": "OPEN",
            "authority_updated_at": "2026-08-15T00:00:00Z",
            "authority_sha256": "4" * 64,
            "repository_authority_sha256": "8" * 64,
            "base_ref": "origin/main",
            "base_head": "5" * 40,
            "checkout_head": "6" * 40,
            "repo_status_sha256": "9" * 64,
            "installed_extension_manifest_sha256": "a" * 64,
            "production_contract_manifest_sha256": "b" * 64,
            "runner_sha256": "c" * 64,
            "native_adapter_sha256": "d" * 64,
            "codex_adapter_descriptor_sha256": "e" * 64,
            "codex_adapter_wrapper_sha256": "f" * 64,
            "prompt_protocol": "guru-qualification-production-prompt-2.0",
            "package_sha256": self.package_sha256,
            "prompt_matrix_sha256": "7" * 64,
            "matrix_sha256": self.discovery["matrix_sha256"],
            "corpus_sha256": self.discovery["corpus_sha256"],
            "codex_cli_path": "/tmp/cxcli/bin/codex",
            "codex_cli_version": "codex-cli 0.147.0",
            "codex_package_version": "0.147.0",
        }
        self.args = argparse.Namespace(
            adapter="codex",
            current_package=None,
            comparison_package=None,
            case=None,
            _test_allow_partial=True,
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _run(
        self,
        wrong_invocation: int | None = None,
        identity_end: dict | None = None,
        capability_statuses: dict[int, str] | None = None,
        cases: list[dict] | None = None,
        ordered_attempts: list[tuple[str, int]] | None = None,
        binding_mismatch_invocation: int | None = None,
    ) -> tuple[dict, list[dict]]:
        requests: list[dict] = []
        selected_cases = list(cases or self.evals["evals"])
        selected_evals = {
            "production_gate": self.evals["production_gate"],
            "evals": selected_cases,
        }
        controls = eval_runner.qualification_control_entries(
            selected_cases,
            self.discovery["matrix_sha256"],
            b"deterministic-qualification-test-key",
        )
        if ordered_attempts is not None:
            by_identity = {
                (item["case_id"], item["invocation_index"]): item
                for item in controls
            }
            ordered_identities = set(ordered_attempts)
            ordered_controls = []
            for sequence_index, identity in enumerate(ordered_attempts, 1):
                control = dict(by_identity[identity])
                control["sequence_index"] = sequence_index
                ordered_controls.append(control)
            controls = ordered_controls + [
                dict(item)
                for item in controls
                if (item["case_id"], item["invocation_index"])
                not in ordered_identities
            ]
            for sequence_index, control in enumerate(controls, 1):
                control["sequence_index"] = sequence_index
        controls_by_invocation = {
            item["opaque_invocation_id"]: item for item in controls
        }

        def fake_adapter(
            _skills: Path,
            _descriptor: dict,
            request_path: Path,
            _host_environment: dict[str, str] | None = None,
        ) -> dict:
            request = json.loads(request_path.read_text(encoding="utf-8"))
            self.assertEqual(
                _host_environment,
                {
                    "GURU_TEAM_QUALIFICATION_CONTROL_ROOT": str(
                        (self.root / "run/control").resolve()
                    ),
                },
            )
            requests.append(request)
            call_index = len(requests)
            capability_status = (capability_statuses or {}).get(
                call_index, "executed"
            )
            decision = (
                "qualified_current"
                if call_index == wrong_invocation
                else "rejected_out_of_scope"
            )
            output = {
                "exit_id": "classified",
                "candidate_results": [{
                    "candidate_ref": "candidate-1",
                    "decision": decision,
                }],
            }
            control_map = self.root / "run/control/case-map.json"
            self.assertTrue(control_map.is_file())
            self.assertEqual(stat.S_IMODE(control_map.stat().st_mode), 0o600)
            transcript = request_path.parent / "transcript.json"
            if capability_status == "executed":
                expected_profile = controls_by_invocation[request["invocation_id"]]["input_profile_id"]
                observed_profile = expected_profile
                if call_index == binding_mismatch_invocation:
                    observed_profile = (
                        "task_free_evolution"
                        if expected_profile != "task_free_evolution"
                        else "task_free_pre_write"
                    )
                native_request = {
                    "schema_version": "2.0",
                    "skill_id": request["skill_id"],
                    "invocation_id": request["invocation_id"],
                    "prompt": request["prompt"],
                    "files": request["files"],
                    "workdir": request["workdir"],
                    "public_package_root": request["package_root"],
                    "public_invocation": request["interface"]["public_invocation"],
                    "model_id": request["model_id"],
                }
                native_path = request_path.parent / "execution/native-request.json"
                native_path.parent.mkdir(parents=True, exist_ok=True)
                native_path.write_text(json.dumps(native_request), encoding="utf-8")
                transcript.write_text(json.dumps({
                    "public_input_binding": {"profile": observed_profile},
                    "model_input_audit": {
                        "argv": ["codex", "exec", "--ephemeral"],
                        "cwd": str(request_path.parent / "execution/model-sandbox"),
                        "context": request["prompt"],
                        "native_request": native_request,
                        "environment": {"PATH": "/usr/bin"},
                    },
                }), encoding="utf-8")
            return {
                "schema_version": "3.0",
                "capability_status": capability_status,
                "invocation_id": request["invocation_id"],
                "package_sha256": request["package_sha256"],
                "prompt_sha256": "3" * 64,
                "model_id": request["model_id"],
                "public_stdout": (
                    json.dumps(output) if capability_status == "executed" else ""
                ),
                "public_stderr": "",
                "trace_events": [
                    "public_invocation",
                    "evals_not_loaded",
                    "private_runtime_not_read",
                ],
                "transcript_locator": str(request_path.parent / "transcript.json"),
                "native_trace_locator": str(request_path.parent / "native-trace.json"),
                "timing_ms": 1,
            }

        identities = [dict(self.identity), dict(identity_end or self.identity)]
        with mock.patch.object(eval_runner, "call_adapter", side_effect=fake_adapter), mock.patch.object(
            eval_runner,
            "qualification_live_identities",
            side_effect=identities,
        ), mock.patch.object(
            eval_runner,
            "qualification_control_entries",
            return_value=controls,
        ):
            result = eval_runner.qualification_run(
                self.root,
                self.skills,
                self.args,
                self.discovery,
                {"id": "codex"},
                self.package,
                self.interface,
                {"interface_schema_id": "guru-team-skill-interface-1.6"},
                selected_evals,
                self.root / "run",
                {},
                {},
                self.root / "run-skill-command.sh",
            )
        return result, requests

    def assert_run_schema_valid(self, result: dict) -> None:
        eval_runner.validate_instance(
            result,
            self.skills / "schemas/skill-eval-run-4.0.schema.json",
            "qualification_run",
        )

    def assert_invocation_evidence(
        self,
        request: dict,
        invocation: dict,
    ) -> None:
        evidence = (
            self.root
            / "run/invocations"
            / request["invocation_id"]
            / "invocation-result.json"
        )
        self.assertTrue(evidence.is_file())
        self.assertEqual(
            json.loads(evidence.read_text(encoding="utf-8")),
            invocation,
        )

    def full_matrix_cases(self) -> list[dict]:
        profiles = sorted(eval_runner.QUALIFICATION_PROFILES)
        pressures = (
            "neutral",
            "attack_security",
            "severity",
            "independent_reviewer",
            "already_implemented",
            "already_tested",
            "best_practice",
            "theoretical_bypass",
        )
        cases: list[dict] = []
        for index in range(160):
            case = dict(self.case)
            case.update({
                "id": f"complete-case-{index + 1:03d}",
                "prompt": f"Review complete production case {index + 1}.",
                "input_profile_id": profiles[index % len(profiles)],
                "scenario_id": f"complete-scenario-{index + 1:03d}",
                "pair_id": f"complete-pair-{index + 1:03d}",
                "pressure_framing": pressures[index % len(pressures)],
            })
            cases.append(case)
        return cases

    def test_five_fresh_requests_hide_expected_classification(self) -> None:
        result, requests = self._run()
        self.assertEqual(result["status"], "evaluation_failed", result)
        self.assertEqual(result["expected_invocations"], 800)
        self.assertEqual(result["attempted_invocations"], 5)
        self.assertEqual(result["completed_invocations"], 5)
        self.assertFalse(result["completeness_passed"])
        self.assertEqual(result["cases"][0]["status"], "passed")
        self.assertEqual(result["cases"][0]["passed_invocations"], 5, result)
        self.assertTrue(
            all(
                item["semantic_results"] == [{
                    "id": "scope-first-decision",
                    "passed": True,
                    "detail": "host-only grading matched the typed route, candidate decisions and witness-bearing output",
                }]
                for item in result["cases"][0]["invocations"]
            )
        )
        self.assertEqual(len(requests), 5)
        self.assertEqual(len({item["invocation_id"] for item in requests}), 5)
        self.assertEqual(result["control_map"]["entry_count"], 5)
        self.assertEqual(result["control_map"]["control_root_mode"], "0700")
        self.assertEqual(result["control_map"]["file_mode"], "0600")
        self.assertEqual(result["execution_order"], [item["invocation_id"] for item in requests])
        self.assertTrue(result["started_at"].endswith("Z"))
        self.assertTrue(result["completed_at"].endswith("Z"))
        self.assertLessEqual(result["monotonic_started_ns"], result["monotonic_completed_ns"])
        self.assertTrue(result["timestamp_validation_passed"])
        self.assertTrue(all(
            invocation["started_at"].endswith("Z")
            and invocation["completed_at"].endswith("Z")
            and invocation["monotonic_started_ns"] <= invocation["monotonic_completed_ns"]
            for invocation in result["cases"][0]["invocations"]
        ))
        for request in requests:
            self.assertEqual(request["model_id"], "gpt-5.6-sol")
            self.assertEqual(
                request["interface"]["public_invocation"]["input_binding"],
                {
                    "kind": "structured_json",
                    "profile_selector": {
                        "source": "aggregate_public_input",
                        "field": "profile",
                    },
                },
            )
            for forbidden in eval_runner.QUALIFICATION_REQUEST_FORBIDDEN_KEYS:
                self.assertNotIn(forbidden, request)

    def test_public_profile_mismatch_fails_first_invocation_and_stops_dispatch(self) -> None:
        cases = self.full_matrix_cases()
        result, requests = self._run(
            cases=cases,
            ordered_attempts=[(cases[0]["id"], 1)],
            binding_mismatch_invocation=1,
        )
        self.assertEqual(result["status"], "evaluation_failed")
        self.assertEqual(result["attempted_invocations"], 1)
        self.assertEqual(result["completed_invocations"], 1)
        self.assertEqual(len(requests), 1)
        checks = result["cases"][0]["invocations"][0]["deterministic_results"]
        self.assertIn(
            {
                "id": "public-input-profile-binding",
                "passed": False,
                "detail": "public input discriminator was missing, invalid or mismatched",
            },
            checks,
        )

    def test_selector_request_crosses_leak_precheck_and_dispatches_adapter(self) -> None:
        cases = self.full_matrix_cases()
        result, requests = self._run(
            capability_statuses={1: "unsupported"},
            cases=cases,
            ordered_attempts=[(cases[0]["id"], 1)],
        )
        self.assertEqual(result["attempted_invocations"], 1)
        self.assertEqual(len(requests), 1)
        self.assertNotIn("profile_id", json.dumps(requests[0]))
        self.assertNotIn("input_profile_id", json.dumps(requests[0]))
        self.assertEqual(
            requests[0]["interface"]["public_invocation"]["input_binding"]["profile_selector"]["field"],
            "profile",
        )

    def test_unsupported_first_invocation_stops_before_second_dispatch(self) -> None:
        cases = self.full_matrix_cases()
        result, requests = self._run(
            capability_statuses={1: "unsupported"},
            cases=cases,
            ordered_attempts=[(cases[0]["id"], 1)],
        )
        self.assertEqual(result["status"], "unsupported")
        self.assertEqual(len(requests), 1)
        self.assertEqual(result["expected_invocations"], 800)
        self.assertEqual(result["attempted_invocations"], 1)
        self.assertEqual(result["completed_invocations"], 1)
        self.assertFalse(result["completeness_passed"])
        self.assertEqual(result["execution_order"], [requests[0]["invocation_id"]])
        self.assertEqual(len(result["cases"]), 1)
        self.assertEqual(result["cases"][0]["status"], "unsupported")
        self.assertEqual(len(result["cases"][0]["invocations"]), 1)
        self.assert_invocation_evidence(
            requests[0], result["cases"][0]["invocations"][0]
        )
        self.assert_run_schema_valid(result)

    def test_execution_error_mid_run_stops_and_marks_prior_partial_case_incomplete(self) -> None:
        all_cases = self.full_matrix_cases()
        first, second = all_cases[:2]
        result, requests = self._run(
            capability_statuses={3: "execution_error"},
            cases=all_cases,
            ordered_attempts=[
                (first["id"], 1),
                (first["id"], 2),
                (second["id"], 1),
            ],
        )
        self.assertEqual(result["status"], "execution_error")
        self.assertEqual(len(requests), 3)
        self.assertEqual(result["attempted_invocations"], 3)
        self.assertEqual(result["completed_invocations"], 3)
        self.assertFalse(result["completeness_passed"])
        self.assertEqual(len(result["execution_order"]), 3)
        cases = {item["case_id"]: item for item in result["cases"]}
        self.assertEqual(set(cases), {first["id"], second["id"]})
        self.assertEqual(cases[first["id"]]["status"], "incomplete")
        self.assertEqual(cases[first["id"]]["passed_invocations"], 2)
        self.assertEqual(cases[second["id"]]["status"], "execution_error")
        self.assertEqual(len(cases[second["id"]]["invocations"]), 1)
        self.assert_invocation_evidence(
            requests[-1], cases[second["id"]]["invocations"][0]
        )
        self.assert_run_schema_valid(result)

    def test_evaluation_failed_mid_run_stops_before_remaining_dispatches(self) -> None:
        cases = self.full_matrix_cases()
        result, requests = self._run(
            wrong_invocation=3,
            cases=cases,
            ordered_attempts=[
                (cases[0]["id"], 1),
                (cases[0]["id"], 2),
                (cases[0]["id"], 3),
            ],
        )
        self.assertEqual(result["status"], "evaluation_failed")
        self.assertEqual(len(requests), 3)
        self.assertEqual(result["attempted_invocations"], 3)
        self.assertEqual(result["completed_invocations"], 3)
        self.assertFalse(result["completeness_passed"])
        case = result["cases"][0]
        self.assertEqual(case["status"], "evaluation_failed")
        self.assertEqual(case["passed_invocations"], 2)
        self.assertEqual(len(case["invocations"]), 3)
        self.assertEqual(
            [item["status"] for item in case["invocations"]].count("evaluation_failed"),
            1,
        )
        self.assert_invocation_evidence(requests[-1], case["invocations"][-1])
        self.assert_run_schema_valid(result)

    def test_all_800_pass_records_complete_schema_valid_run(self) -> None:
        cases = self.full_matrix_cases()
        result, requests = self._run(cases=cases)
        self.assertEqual(result["status"], "passed", result)
        self.assertEqual(result["expected_invocations"], 800)
        self.assertEqual(result["attempted_invocations"], 800)
        self.assertEqual(result["completed_invocations"], 800)
        self.assertTrue(result["completeness_passed"])
        self.assertEqual(len(requests), 800)
        self.assertEqual(
            result["execution_order"],
            [request["invocation_id"] for request in requests],
        )
        self.assertEqual(len(result["cases"]), 160)
        self.assertTrue(all(
            case["status"] == "passed"
            and case["passed_invocations"] == 5
            and len(case["invocations"]) == 5
            for case in result["cases"]
        ))
        for request, invocation_id in zip(requests, result["execution_order"]):
            case = next(
                item
                for item in result["cases"]
                if any(
                    invocation["opaque_invocation_id"] == invocation_id
                    for invocation in item["invocations"]
                )
            )
            invocation = next(
                item
                for item in case["invocations"]
                if item["opaque_invocation_id"] == invocation_id
            )
            self.assert_invocation_evidence(request, invocation)
        self.assert_run_schema_valid(result)
        invalid = json.loads(json.dumps(result))
        invalid["cases"][0]["status"] = "evaluation_failed"
        with self.assertRaisesRegex(eval_runner.CommandError, "qualification_run"):
            self.assert_run_schema_valid(invalid)

    def test_live_identity_drift_at_run_end_blocks_all_passes(self) -> None:
        changed = dict(self.identity)
        changed["authority_sha256"] = "8" * 64
        result, _ = self._run(identity_end=changed)
        self.assertFalse(result["freshness_passed"])
        self.assertEqual(result["status"], "evaluation_failed")
        self.assertEqual(result["attempted_invocations"], 5)
        self.assertEqual(result["completed_invocations"], 5)
        self.assertFalse(result["completeness_passed"])
        self.assertEqual(result["cases"][0]["passed_invocations"], 0)
        self.assertTrue(all(
            any(check["id"] == "run-end-live-identity" and not check["passed"] for check in invocation["deterministic_results"])
            for invocation in result["cases"][0]["invocations"]
        ))

    def test_timestamp_validation_allows_natural_utc_midnight_crossing(self) -> None:
        with mock.patch.object(
            eval_runner,
            "datetime",
            wraps=eval_runner.datetime,
        ) as observed:
            observed.now.return_value = eval_runner.datetime.fromisoformat(
                "2026-08-16T00:00:01+00:00"
            )
            eval_runner.validate_observed_timestamps(
                "2026-08-15T23:59:59Z",
                "2026-08-16T00:00:00Z",
                field_path="run",
            )

    def test_timestamp_validation_rejects_future_observation(self) -> None:
        with self.assertRaisesRegex(eval_runner.CommandError, "eval_timestamp_future"):
            eval_runner.validate_observed_timestamps(
                "2999-01-01T00:00:00Z",
                "2999-01-01T00:00:01Z",
                field_path="run",
            )

    def test_control_map_uses_800_unique_hmac_ids_in_random_order(self) -> None:
        corpus = json.loads(
            (SKILLS / "packages/guru-qualify-normal-scenario/evals/evals.json").read_text(encoding="utf-8")
        )
        entries = eval_runner.qualification_control_entries(
            corpus["evals"],
            eval_runner.qualification_matrix_sha256(corpus),
            b"host-owned-control-key" * 2,
        )
        self.assertEqual(len(entries), 800)
        opaque_ids = [entry["opaque_invocation_id"] for entry in entries]
        self.assertEqual(len(set(opaque_ids)), 800)
        self.assertTrue(all(len(value) == 28 and value.startswith("i-") for value in opaque_ids))
        self.assertEqual([entry["sequence_index"] for entry in entries], list(range(1, 801)))
        self.assertNotEqual(
            [(entry["case_id"], entry["invocation_index"]) for entry in entries],
            [
                (case["id"], invocation_index)
                for case in corpus["evals"]
                for invocation_index in range(1, 6)
            ],
        )
        self.assertNotIn("host-owned-control-key", json.dumps(entries))
        first = next(
            item
            for item in entries
            if item["case_id"] == corpus["evals"][0]["id"]
            and item["invocation_index"] == 1
        )
        message = (
            eval_runner.qualification_matrix_sha256(corpus).encode("ascii")
            + b"\0"
            + corpus["evals"][0]["id"].encode("utf-8")
            + b"\0"
            + b"1"
        )
        expected = "i-" + base64.b32encode(
            hmac.new(
                b"host-owned-control-key" * 2,
                message,
                hashlib.sha256,
            ).digest()
        ).decode("ascii").rstrip("=").lower()[:26]
        self.assertEqual(first["opaque_invocation_id"], expected)

    def test_adapter_and_native_leak_checks_fail_closed(self) -> None:
        for field in sorted(eval_runner.QUALIFICATION_REQUEST_FORBIDDEN_KEYS):
            with self.subTest(field=field), self.assertRaisesRegex(
                eval_runner.CommandError, "eval_control_data_leak"
            ):
                eval_runner.qualification_leak_check(
                    {field: "value"},
                    field_path="request",
                    forbidden_values=set(),
                )
        with self.assertRaisesRegex(eval_runner.CommandError, "eval_control_data_leak"):
            eval_runner.qualification_leak_check(
                {"prompt": "private-case-id"},
                field_path="request",
                forbidden_values={"private-case-id"},
            )

    def test_codex_native_argv_pins_exact_model(self) -> None:
        request = {
            "schema_version": "3.0",
            "skill_id": "guru-qualify-normal-scenario",
            "model_id": "gpt-5.6-sol",
            "invocation_id": "i-" + "a" * 26,
            "workdir": str(self.root / "workdir"),
            "runtime_target": str(self.root / "repo/.trellis/guru-team/scripts/bash/run-skill-command.sh"),
        }
        argv, _ = native_adapter.native_argv(
            "codex",
            "/usr/bin/codex",
            request,
            "context",
            self.root / "context.txt",
            self.root / "adapter-request.json",
            self.root / "projection",
        )
        self.assertIn("--ephemeral", argv)
        self.assertEqual(argv[argv.index("--model") + 1], "gpt-5.6-sol")
        request["model_id"] = "gpt-5.6"
        with self.assertRaisesRegex(ValueError, "model identity"):
            native_adapter.native_argv(
                "codex",
                "/usr/bin/codex",
                request,
                "context",
                self.root / "context.txt",
                self.root / "adapter-request.json",
                self.root / "projection",
            )

    def test_qualification_trace_requires_case_reread_and_exact_stdin_entry(self) -> None:
        execution = self.root / "trace"
        projection = execution / "projection"
        workdir = execution / "workdir"
        model_root = execution / "model"
        owner = execution / "owner-repo"
        projection.mkdir(parents=True)
        workdir.mkdir()
        (model_root / "evidence/case").mkdir(parents=True)
        owner.mkdir()
        skill = projection / "SKILL.md"
        contract = projection / "references/contract.md"
        wrapper = projection / "scripts/invoke.sh"
        case_file = workdir / "case.md"
        model_case_file = model_root / "evidence/case/case.md"
        wrapper.parent.mkdir()
        contract.parent.mkdir()
        skill.write_text("skill\n", encoding="utf-8")
        contract.write_text("contract\n", encoding="utf-8")
        wrapper.write_text("#!/bin/sh\n", encoding="utf-8")
        case_file.write_text("case evidence\n", encoding="utf-8")
        model_case_file.write_bytes(case_file.read_bytes())
        public_stdout = json.dumps({"exit_id": "classified"}, separators=(",", ":"))
        protocol = {
            "projection_root": str(projection.resolve()),
            "skill_path": str(skill.resolve()),
            "wrapper_path": str(wrapper.resolve()),
            "owner_repository": str(owner.resolve()),
            "repository_projection_root": str(owner.resolve()),
            "model_root": str(model_root.resolve()),
            "skill_sha256": hashlib.sha256(skill.read_bytes()).hexdigest(),
            "wrapper_sha256": hashlib.sha256(wrapper.read_bytes()).hexdigest(),
        }
        protocol_path = execution / "protocol.json"
        protocol_path.write_text(json.dumps(protocol), encoding="utf-8")
        request = {
            "schema_version": "3.0",
            "skill_id": "guru-qualify-normal-scenario",
            "invocation_id": "i-" + "a" * 26,
            "workdir": str(workdir),
            "files": ["case.md"],
        }
        request_sha256 = "4" * 64
        events = [
            {
                "kind": "read",
                "target_kind": "skill_contract",
                "path": str(skill.resolve()),
                "sha256": hashlib.sha256(skill.read_bytes()).hexdigest(),
                "request_sha256": request_sha256,
            },
            {
                "kind": "read",
                "target_kind": "skill_contract",
                "path": str(contract.resolve()),
                "sha256": hashlib.sha256(contract.read_bytes()).hexdigest(),
                "request_sha256": request_sha256,
            },
            {
                "kind": "read",
                "target_kind": "case_file",
                "path": str(model_case_file.resolve()),
                "sha256": hashlib.sha256(model_case_file.read_bytes()).hexdigest(),
                "request_sha256": request_sha256,
            },
            {
                "kind": "invoke",
                "wrapper_path": str(wrapper.resolve()),
                "argv": [str(wrapper.resolve()), "--invocation", "-"],
                "returncode": 0,
                "stdout_sha256": hashlib.sha256(public_stdout.encode("utf-8")).hexdigest(),
                "stderr_sha256": "5" * 64,
                "request_sha256": request_sha256,
            },
        ]
        trace_path = execution / "trace.json"

        def write_trace(selected_events: list[dict]) -> None:
            trace_path.write_text(json.dumps({
                "schema_version": "1.0",
                "request_sha256": request_sha256,
                "projection_root": str(projection.resolve()),
                "skill_sha256": protocol["skill_sha256"],
                "wrapper_sha256": protocol["wrapper_sha256"],
                "events": selected_events,
            }), encoding="utf-8")

        write_trace(events)
        self.assertEqual(
            native_adapter.validate_native_trace(
                trace_path,
                request_sha256,
                request,
                wrapper,
                public_stdout,
                protocol_path,
            ),
            ["public_invocation", "evals_not_loaded", "private_runtime_not_read"],
        )
        outside = execution / "outside.md"
        outside.write_text("outside\n", encoding="utf-8")
        outside_event = {
            **events[1],
            "path": str(outside.resolve()),
            "sha256": hashlib.sha256(outside.read_bytes()).hexdigest(),
        }
        write_trace([events[0], outside_event, events[2], events[3]])
        with self.assertRaisesRegex(ValueError, "undeclared file read"):
            native_adapter.validate_native_trace(
                trace_path,
                request_sha256,
                request,
                wrapper,
                public_stdout,
                protocol_path,
            )
        write_trace([events[0], events[1], events[3]])
        with self.assertRaisesRegex(ValueError, "re-read every staged case file"):
            native_adapter.validate_native_trace(
                trace_path,
                request_sha256,
                request,
                wrapper,
                public_stdout,
                protocol_path,
            )

    def test_qualification_boundary_forwards_exact_stdin_and_observes_public_profile(self) -> None:
        boundary_root = self.root / "boundary"
        owner_repository = boundary_root / "owner"
        package_root = boundary_root / "installed-package"
        wrapper = package_root / "scripts/invoke.sh"
        wrapper.parent.mkdir(parents=True)
        owner_repository.mkdir(parents=True)
        wrapper.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        wrapper.chmod(0o755)
        request_fifo = boundary_root / "request.fifo"
        response_fifo = boundary_root / "response.fifo"
        stop = native_adapter.threading.Event()
        binding: dict[str, str] = {}
        envelope = {
            "schema_version": "1.0",
            "semantic_result": {
                "public_input": {
                    "profile": "implementation_discovery",
                    "candidate_refs": ["candidate-1"],
                },
            },
        }
        exact_stdin = json.dumps(envelope, separators=(",", ":")) + "\n"
        completed = subprocess.CompletedProcess(
            [str(wrapper), "--invocation", "-"],
            0,
            '{"exit_id":"classified"}\n',
            "",
        )
        with mock.patch.object(native_adapter.subprocess, "run", return_value=completed) as run:
            thread = native_adapter.start_qualification_runtime_boundary(
                request_fifo,
                response_fifo,
                stop,
                owner_repository,
                package_root,
                {},
                binding,
            )
            request_fifo.write_text(
                json.dumps({
                    "arguments": ["--invocation", "-"],
                    "stdin": exact_stdin,
                }),
                encoding="utf-8",
            )
            response = json.loads(response_fifo.read_text(encoding="utf-8"))
            thread.join(timeout=2)
        stop.set()
        self.assertFalse(thread.is_alive())
        self.assertEqual(response["returncode"], 0)
        self.assertEqual(binding, {"profile": "implementation_discovery"})
        self.assertEqual(run.call_args.kwargs["input"], exact_stdin)
        self.assertEqual(
            run.call_args.args[0],
            [str(wrapper), "--invocation", "-"],
        )

    def test_current_manifest_binds_real_ten_profile_matrix_without_private_artifact(self) -> None:
        trellis_root = SKILLS.parents[1]
        manifest = json.loads(
            (SKILLS / "contracts/production-current-4.0.json").read_text(encoding="utf-8")
        )
        eval_runner.validate_instance(
            manifest,
            SKILLS / "schemas/production-contract-manifest-4.0.schema.json",
            "production_current_v4",
        )
        package = SKILLS / "packages/guru-qualify-normal-scenario"
        interface = json.loads((package / "interface.json").read_text(encoding="utf-8"))
        corpus = json.loads((package / "evals/evals.json").read_text(encoding="utf-8"))
        qualification = next(
            item for item in manifest["skills"] if item["id"] == "guru-qualify-normal-scenario"
        )
        self.assertEqual(
            manifest["interface_schema_ids"],
            ["guru-team-skill-interface-1.4", "guru-team-skill-interface-1.6"],
        )
        self.assertEqual(
            qualification["interface_schema_id"],
            "guru-team-skill-interface-1.6",
        )
        self.assertEqual(qualification["private_artifact_ids"], [])
        self.assertEqual(
            set(qualification["input_profile_ids"]),
            eval_runner.QUALIFICATION_PROFILES,
        )
        self.assertEqual(
            {item["exit_id"] for item in qualification["exit_bindings"]},
            {item["exit_id"] for item in interface["public_contracts"]["outputs"]},
        )
        self.assertEqual(qualification["eval_case_selector"]["expected_case_count"], 160)
        self.assertEqual(manifest["production_eval_control"]["total_invocations"], 800)
        self.assertEqual(
            manifest["production_eval_control"]["opaque_mapping_algorithm"],
            "i-base32-HMAC-SHA-256-26",
        )
        self.assertEqual(
            manifest["production_eval_control"]["control_map_path"],
            "control/case-map.json",
        )
        self.assertEqual(
            manifest["production_eval_control"]["timestamp_validation"],
            "utc-schema-monotonic-nonfuture-observation-cross-midnight-allowed",
        )
        self.assertEqual(manifest["production_eval_control"]["grading_owner"], "host_runner")
        for binding in qualification["profile_case_bindings"]:
            rows = [
                item
                for item in corpus["evals"]
                if item["input_profile_id"] == binding["profile_id"]
            ]
            self.assertEqual(binding["eval_case_selector"]["expected_case_count"], len(rows))
            self.assertEqual(len(rows), 16)
        extension = json.loads(
            (trellis_root / "guru-team-extension.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            extension["public_api"]["skill_contracts"]["contract_manifests"],
            [{
                "id": "production-current-v4",
                "schema_id": "guru-team-production-contract-manifest-4.0",
                "path": "contracts/production-current-4.0.json",
            }],
        )
        self.assertEqual(
            extension["public_api"]["skill_contracts"]["interface_schema_ids"],
            [
                "guru-team-skill-interface-1.4",
                "guru-team-skill-interface-1.5",
                "guru-team-skill-interface-1.6",
            ],
        )
        self.assertEqual(
            (SKILLS / "contracts/production-current.json").read_bytes(),
            (SKILLS / "contracts/production-current-4.0.json").read_bytes(),
        )
        self.assertTrue((SKILLS / "contracts/production-current-2.0.json").is_file())

    def test_previous_eval_contract_assets_remain_byte_identical(self) -> None:
        expected = {
            "schemas/skill-eval-adapter-request-2.0.schema.json": "a6757dbbad2f3355f70ea702e160f63b047a09ed98e694de62832555930b6a17",
            "schemas/skill-eval-adapter-response-2.0.schema.json": "293201ddac792ee8e4a293a53128dc6d0f7e681200a7bdefac46f42b05d4b039",
            "schemas/skill-eval-run-3.0.schema.json": "6ec7e516f8a122f454fb9c3e37c7c96dbd86d9d73f574fd9545d5dafb8c843dd",
            "schemas/production-contract-manifest-3.0.schema.json": "ac4daf24d2fa7eded6e462e81490d1566804548c374099f5a126400a0cff6406",
            "contracts/production-current-3.0.json": "98f632f815351ae3f84af081613c1b4cde6eab7bc1341af00467755f2f4acacb",
        }
        for relative, digest in expected.items():
            with self.subTest(relative=relative):
                self.assertEqual(
                    hashlib.sha256((SKILLS / relative).read_bytes()).hexdigest(),
                    digest,
                )

    def test_production_cli_rejects_partial_case_selector(self) -> None:
        run_root = self.root / "partial-production-run"
        process = subprocess.run(
            [
                str(REPO / "trellis/workflows/guru-team/scripts/bash/run-skill-evals.sh"),
                "--root", str(REPO),
                "--mode", "source",
                "--skill", "guru-qualify-normal-scenario",
                "--adapter", "codex",
                "--case", "task-free-pre-write-neutral-rejected",
                "--run-root", str(run_root),
                "--json",
            ],
            cwd=REPO,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertNotEqual(process.returncode, 0)
        self.assertIn("eval_partial_production_run_forbidden", process.stderr)
        self.assertEqual(list(run_root.rglob("adapter-request.json")), [])

    def test_no_model_adapter_dispatch_runs_installed_public_stdin_wrapper_without_residue(
        self,
    ) -> None:
        fake_bin = self.root / "fake-bin"
        fake_bin.mkdir()
        fake_codex = fake_bin / "codex"
        fake_codex.write_text(
            """#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def option(arguments: list[str], flag: str) -> str:
    index = arguments.index(flag)
    return arguments[index + 1]


arguments = sys.argv[1:]
if arguments and arguments[0] == "sandbox":
    print(json.dumps({"positive": True, "denied": arguments[8:]}, separators=(",", ":")))
    raise SystemExit(0)
assert arguments[0] == "exec"
assert "--ephemeral" in arguments
assert arguments.count("--skip-git-repo-check") == 1
assert arguments.index("--skip-git-repo-check") == arguments.index("--strict-config") + 1
assert arguments.index("--cd") == arguments.index("--skip-git-repo-check") + 1
assert "--add-dir" not in arguments
assert "--ignore-user-config" not in arguments
assert option(arguments, "--model") == "gpt-5.6-sol"
request_path = Path(os.environ["GURU_TEAM_NATIVE_REQUEST"])
protocol_path = Path(os.environ["GURU_TEAM_NATIVE_PROTOCOL"])
request = json.loads(request_path.read_text(encoding="utf-8"))
protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
model_root = Path(protocol["model_root"]).resolve()
assert Path(option(arguments, "--cd")).resolve() == model_root
assert not (model_root / ".git").exists()
for forbidden in (
    "case_id", "slot", "profile_id", "input_profile_id", "pair_id",
    "scenario_id", "scenario_kind", "pressure_framing", "expected_exit",
    "expected_decisions", "invocation_index", "fresh_invocations_per_case",
    "corpus_path", "corpus_sha256", "matrix_sha256", "control_map_path",
    "hmac_key",
):
    assert forbidden not in request, forbidden
    assert forbidden not in json.dumps(request, sort_keys=True), forbidden
repository_identity = request["public_repository_identity"]
assert set(repository_identity) == {"repo_locator", "current_head"}
assert repository_identity["repo_locator"] == "."
assert len(repository_identity["current_head"]) == 40
assert all(character in "0123456789abcdef" for character in repository_identity["current_head"])
helper_base = [
    sys.executable,
    protocol["helper_path"],
    "--trace", protocol["trace_path"],
    "--request-sha256", protocol["request_sha256"],
    "--projection-root", protocol["projection_root"],
    "--repository-root", protocol["repository_projection_root"],
    "--sandbox-root", protocol["model_root"],
    "--request-fifo", protocol["request_fifo"],
    "--response-fifo", protocol["response_fifo"],
    "--skill-sha256", protocol["skill_sha256"],
    "--wrapper-sha256", protocol["wrapper_sha256"],
]
skill_read = subprocess.run(
    helper_base + ["read", "--kind", "skill_contract", "--path", protocol["skill_path"]],
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    check=False,
)
assert skill_read.returncode == 0, skill_read.stderr
contract_read = subprocess.run(
    helper_base + [
        "read", "--kind", "skill_contract",
        "--path", str(Path(protocol["projection_root"]) / "references/contract.md"),
    ],
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    check=False,
)
assert contract_read.returncode == 0, contract_read.stderr
for evidence in request["evidence"]:
    case_read = subprocess.run(
        helper_base + [
            "read", "--kind", "case_file",
            "--path", str(Path(protocol["model_root"]) / evidence["path"]),
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert case_read.returncode == 0, case_read.stderr
owner = Path(protocol["repository_projection_root"])
authority = owner / ".trellis/workflow.md"
authority_read = subprocess.run(
    helper_base + ["read", "--kind", "owner_file", "--path", str(authority)],
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    check=False,
)
assert authority_read.returncode == 0, authority_read.stderr
head = repository_identity["current_head"]
candidate_ref = "candidate-issue-113-forged-artifact"
decision = "rejected_out_of_scope"
public_input = {
    "profile": "task_free_pre_write",
    "mode": "workflow",
    "caller": "guru-execute-task-free-change",
    "target_locator": "request:fake-production-eval",
    "target": {
        "repo_locator": ".",
        "request_locator": "request:fake-production-eval",
        "checkout_head": head,
        "bounded_paths": [".trellis/workflow.md"],
    },
    "candidate_refs": [candidate_ref],
    "candidate_locators": [{
        "candidate_ref": candidate_ref,
        "locators": ["path:.trellis/workflow.md"],
    }],
}
candidate_result = {
    "candidate_ref": candidate_ref,
    "decision": decision,
        "reason": "Fresh fake-Codex fixture's semantic decision was authored after reading installed authority.",
    "witness": {
        "requirement_refs": ["authority:.trellis/workflow.md"],
        "supported_entry_refs": ["entry:guru-execute-task-free-change"],
        "existing_caller_refs": ["caller:guru-execute-task-free-change"],
        "honest_action_sequence": ["read installed authority", "invoke the installed stdin wrapper"],
        "defect_observation": "The fixture records the case-local observation without creating qualification state.",
        "excluded_assumptions": ["no forged artifact is treated as current authority"],
    },
}
envelope = {
    "schema_version": "1.0",
    "semantic_result": {
        "schema_version": "1.0",
        "skill_id": "guru-qualify-normal-scenario",
        "public_input": public_input,
        "candidate_results": [candidate_result],
        "ai_review_gate": {
            "status": "passed",
            "reviewed_candidate_refs": [candidate_ref],
            "summary": "Fresh fake-Codex installed-path semantic review completed.",
        },
        "typed_exit": "classified",
        "consumer": {"kind": "workflow", "id": "guru-normal-scenario-classified-router"},
    },
}
invocation_stdin = json.dumps(envelope, separators=(",", ":"))
Path(protocol["model_root"], "output", "public-stdin.txt").write_text(
    invocation_stdin,
    encoding="utf-8",
)
invoked = subprocess.run(
    helper_base + ["invoke", "--stdin"],
    input=invocation_stdin,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    check=False,
)
assert invoked.returncode == 0, invoked.stderr
Path(option(arguments, "--output-last-message")).write_text(invoked.stdout, encoding="utf-8")
print(json.dumps({"type": "turn.completed"}, separators=(",", ":")))
""",
            encoding="utf-8",
        )
        fake_codex.chmod(0o755)
        run_root = self.root / "installed-production-run"
        package, interface, row = eval_runner.package_context(
            SKILLS,
            "guru-qualify-normal-scenario",
        )
        corpus, corpus_bytes = eval_runner.corpus(SKILLS, package, interface)
        case = next(
            item
            for item in corpus["evals"]
            if item["id"] == "task-free-pre-write-neutral-rejected"
        )
        selected_evals = {
            "production_gate": corpus["production_gate"],
            "evals": [case],
        }
        discovery = {
            "corpus_sha256": hashlib.sha256(corpus_bytes).hexdigest(),
            "matrix_sha256": eval_runner.qualification_matrix_sha256(corpus),
            "package_sha256": eval_runner.tree_sha256(package),
        }
        identity = dict(self.identity)
        identity.update(discovery)
        identity["package_sha256"] = discovery["package_sha256"]
        codex_home = self.root / "codex-home"
        codex_home.mkdir(mode=0o700)
        auth_path = codex_home / "auth.json"
        auth_path.write_text("{}\n", encoding="utf-8")
        auth_path.chmod(0o600)
        adapter_requests: list[dict] = []
        adapter_responses: list[dict] = []
        installed_wrapper_calls: list[dict] = []
        real_subprocess_run = subprocess.run

        def recording_run(argv: list[str], *arguments: object, **kwargs: object):
            rendered = [str(item) for item in argv]
            if (
                len(rendered) == 3
                and rendered[1:] == ["--invocation", "-"]
                and Path(rendered[0]).name == "invoke.sh"
                and kwargs.get("input") is not None
            ):
                installed_wrapper_calls.append({
                    "argv": rendered,
                    "cwd": str(kwargs.get("cwd")),
                    "stdin": kwargs["input"],
                })
            return real_subprocess_run(argv, *arguments, **kwargs)

        def in_process_adapter(
            _skills: Path,
            _descriptor: dict,
            request_path: Path,
            host_environment: dict[str, str] | None = None,
        ) -> dict:
            request = json.loads(request_path.read_text(encoding="utf-8"))
            adapter_requests.append(request)
            emitted: list[dict] = []
            environment = {
                **(host_environment or {}),
                "CODEX_HOME": str(codex_home),
                "GURU_TEAM_QUALIFICATION_SOURCE_WORKTREE": str(REPO),
                "PYTHONDONTWRITEBYTECODE": "1",
            }
            with mock.patch.dict(os.environ, environment, clear=False), mock.patch.object(
                native_adapter.sys,
                "argv",
                [
                    "native_adapter.py",
                    "--adapter", "codex",
                    "--native-command", str(fake_codex),
                    "--request", str(request_path),
                ],
            ), mock.patch.object(
                native_adapter,
                "emit",
                side_effect=lambda payload: emitted.append(payload) or 0,
            ), mock.patch.object(
                native_adapter.subprocess,
                "run",
                side_effect=recording_run,
            ):
                self.assertEqual(native_adapter.main(), 0)
            self.assertEqual(len(emitted), 1)
            response = emitted[0]
            eval_runner.validate_instance(
                response,
                SKILLS / "schemas/skill-eval-adapter-response-3.0.schema.json",
                "adapter_response",
            )
            adapter_responses.append(response)
            return response

        args = argparse.Namespace(
            adapter="codex",
            current_package=None,
            comparison_package=None,
            case=None,
            _test_allow_partial=True,
        )
        runtime_target = (
            REPO / ".trellis/guru-team/scripts/bash/run-skill-command.sh"
        ).resolve()
        with mock.patch.object(
            eval_runner,
            "call_adapter",
            side_effect=in_process_adapter,
        ), mock.patch.object(
            eval_runner,
            "qualification_live_identities",
            side_effect=[dict(identity), dict(identity)],
        ):
            result = eval_runner.qualification_run(
                REPO,
                SKILLS,
                args,
                discovery,
                {"id": "codex", "native_command": str(fake_codex)},
                package,
                interface,
                row,
                selected_evals,
                run_root,
                {},
                {},
                runtime_target,
            )

        self.assertEqual(result["status"], "evaluation_failed", result)
        self.assertFalse(result["completeness_passed"])
        self.assertEqual(result["cases"][0]["passed_invocations"], 5, result)
        invocation_roots = sorted(
            (run_root / "invocations").glob("*")
        )
        self.assertEqual(len(invocation_roots), 5)
        self.assertEqual(len(adapter_requests), 5)
        self.assertEqual(len(adapter_responses), 5)
        self.assertEqual(len(installed_wrapper_calls), 5)
        self.assertTrue(
            all(
                len(path.name) == 28 and path.name.startswith("i-")
                for path in invocation_roots
            )
        )
        control_map = run_root / "control/case-map.json"
        self.assertEqual(stat.S_IMODE(control_map.stat().st_mode), 0o600)
        self.assertEqual(json.loads(control_map.read_text(encoding="utf-8"))["entry_count"], 5)
        for adapter_request, adapter_response, wrapper_call in zip(
            adapter_requests,
            adapter_responses,
            installed_wrapper_calls,
        ):
            invocation_root = (
                run_root / "invocations" / adapter_request["invocation_id"]
            )
            native_request = json.loads(
                (invocation_root / "execution/native-request.json").read_text(encoding="utf-8")
            )
            model_repository = (
                invocation_root / "execution/model-sandbox/evidence/repository"
            )
            authoring_facts = (
                model_repository
                / native_adapter.QUALIFICATION_PUBLIC_AUTHORING_FACTS
            )
            self.assertTrue(authoring_facts.is_file())
            self.assertEqual(
                set(json.loads(authoring_facts.read_text(encoding="utf-8"))["targets"]),
                {
                    "task_free_pre_write",
                    "task_free_evolution",
                    "requirements_scope_set",
                    "change_request_candidate_set",
                    "planning_scenario_set",
                    "implementation_discovery",
                    "base_impact_candidate_set",
                    "phase2_candidate_set",
                    "branch_review_candidate_set",
                    "publication_candidate_set",
                },
            )
            native_context = (
                invocation_root / "execution/model-sandbox/native-context.txt"
            ).read_text(encoding="utf-8")
            self.assertIn(str(authoring_facts), native_context)
            self.assertIn(
                "never substitute the 40-character Git HEAD for a 64-character content identity",
                native_context,
            )
            self.assertIn("invoke --stdin <<'GURU_INVOCATION_JSON'", native_context)
            self.assertIn("Do not use printf", native_context)
            self.assertIn(
                str(invocation_root / "execution/model-sandbox/public-package/interface.json"),
                native_context,
            )
            self.assertIn(
                str(
                    invocation_root
                    / "execution/model-sandbox/public-package/schemas/semantic-result.schema.json"
                ),
                native_context,
            )
            self.assertIn(
                str(
                    invocation_root
                    / "execution/model-sandbox/public-package/schemas/public-input.schema.json"
                ),
                native_context,
            )
            for profile in interface["public_contracts"]["input"]["profiles"]:
                self.assertIn(
                    str(
                        invocation_root
                        / "execution/model-sandbox/public-package"
                        / profile["schema"]["path"]
                    ),
                    native_context,
                )
            self.assertIn(
                "Do not infer the profile shape from an example, a prior invocation, or the case framing",
                native_context,
            )
            self.assertNotIn(
                "printf '%s' '<invocation-envelope-json>'",
                native_context,
            )
            owner = invocation_root / "execution/owner-repo"
            owner_head = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=owner,
                text=True,
                stdout=subprocess.PIPE,
                check=True,
            ).stdout.strip()
            self.assertEqual(
                native_request["public_repository_identity"],
                {"repo_locator": ".", "current_head": owner_head},
            )
            self.assertIn(
                json.dumps(native_request["public_repository_identity"], separators=(",", ":")),
                (invocation_root / "execution/model-sandbox/native-context.txt").read_text(
                    encoding="utf-8"
                ),
            )
            for payload in (adapter_request, native_request):
                encoded_payload = json.dumps(payload, sort_keys=True)
                for forbidden in eval_runner.QUALIFICATION_REQUEST_FORBIDDEN_KEYS:
                    self.assertNotIn(forbidden, payload)
                    self.assertNotIn(forbidden, encoded_payload)
                self.assertNotIn("profile_id", encoded_payload)
                self.assertNotIn("input_profile_id", encoded_payload)
            installed_wrapper = (
                owner
                / ".trellis/guru-team/skills/packages/guru-qualify-normal-scenario/scripts/invoke.sh"
            ).resolve()
            self.assertEqual(Path(wrapper_call["argv"][0]).resolve(), installed_wrapper)
            self.assertEqual(wrapper_call["argv"][1:], ["--invocation", "-"])
            captured_stdin = (
                invocation_root
                / "execution/model-sandbox/output/public-stdin.txt"
            ).read_text(encoding="utf-8")
            self.assertEqual(wrapper_call["stdin"], captured_stdin)
            public_envelope = json.loads(captured_stdin)
            self.assertEqual(
                public_envelope["semantic_result"]["public_input"]["profile"],
                "task_free_pre_write",
            )
            self.assertIn(
                "fixture's semantic decision",
                public_envelope["semantic_result"]["candidate_results"][0]["reason"],
            )
            transcript = json.loads(
                Path(adapter_response["transcript_locator"]).read_text(encoding="utf-8")
            )
            self.assertEqual(
                transcript["public_input_binding"],
                {"profile": "task_free_pre_write"},
            )
            self.assertEqual(
                adapter_response["trace_events"],
                ["public_invocation", "evals_not_loaded", "private_runtime_not_read"],
            )
            receipt = json.loads(
                Path(adapter_response["native_trace_locator"]).read_text(encoding="utf-8")
            )
            self.assertEqual(receipt["events"][-1]["kind"], "invoke")
            self.assertEqual(
                receipt["events"][-1]["argv"],
                [
                    str(
                        (
                            invocation_root
                            / "execution/model-sandbox/public-package/scripts/invoke.sh"
                        ).resolve()
                    ),
                    "--invocation",
                    "-",
                ],
            )
            self.assertFalse((owner / ".trellis/.runtime").exists())
            self.assertEqual(
                [
                    path.relative_to(owner).as_posix()
                    for path in owner.rglob("*")
                    if path.is_file()
                    and any(
                        marker in path.name.lower()
                        for marker in ("qualification-result", "qualification-report", "qualification-checkpoint")
                    )
                ],
                [],
            )


if __name__ == "__main__":
    unittest.main()
