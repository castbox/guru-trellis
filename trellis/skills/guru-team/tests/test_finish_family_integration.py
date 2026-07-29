from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from typing import Any


SOURCE_REPO = Path(__file__).resolve().parents[4]
EXECUTION_MODE = os.environ.get("GURU_FINISH_INTEGRATION_MODE", "source")
if EXECUTION_MODE not in {"source", "installed"}:
    raise RuntimeError(
        "GURU_FINISH_INTEGRATION_MODE must be source or installed"
    )
REPO = Path(
    os.environ.get("GURU_FINISH_INTEGRATION_ROOT", str(SOURCE_REPO))
).resolve()
if EXECUTION_MODE == "installed":
    SKILLS_ROOT = REPO / ".trellis/guru-team/skills"
    EVAL_RUNNER = REPO / ".trellis/guru-team/scripts/bash/run-skill-evals.sh"
else:
    SKILLS_ROOT = REPO / "trellis/skills/guru-team"
    EVAL_RUNNER = (
        REPO / "trellis/workflows/guru-team/scripts/bash/run-skill-evals.sh"
    )
REAL_ADAPTERS = tuple(
    item
    for item in os.environ.get(
        "GURU_FINISH_INTEGRATION_ADAPTERS",
        "shared,codex,claude,cursor",
    ).split(",")
    if item
)
if not REAL_ADAPTERS or set(REAL_ADAPTERS) - {
    "shared",
    "codex",
    "claude",
    "cursor",
}:
    raise RuntimeError("GURU_FINISH_INTEGRATION_ADAPTERS is invalid")

FINISH_EXITS = {
    "guru-review-task-publication": {
        "ready",
        "return_to_task_work",
        "blocked",
    },
    "guru-verify-extension-installation": {
        "verified",
        "not_required",
        "return_to_task_work",
        "blocked",
    },
    "guru-finalize-task": {
        "verification_required",
        "publication_review_stale",
        "resume_finalization",
        "reprepare_required",
        "published",
        "blocked",
    },
}

EVAL_CASES = {
    ("guru-review-task-publication", "ready"): "workflow-initial-ready",
    ("guru-review-task-publication", "return_to_task_work"): "return-to-task-work",
    ("guru-review-task-publication", "blocked"): "blocked-external",
    ("guru-verify-extension-installation", "verified"): "workflow-required-verified",
    ("guru-verify-extension-installation", "not_required"): "standalone-not-required",
    ("guru-verify-extension-installation", "return_to_task_work"): "task-install-finding-return",
    ("guru-verify-extension-installation", "blocked"): "standalone-remote-unavailable",
    ("guru-finalize-task", "verification_required"): "publication-verification-required",
    ("guru-finalize-task", "publication_review_stale"): "publication-review-stale",
    ("guru-finalize-task", "resume_finalization"): "same-plan-resume",
    ("guru-finalize-task", "reprepare_required"): "cross-month-reprepare",
    ("guru-finalize-task", "published"): "published-recovery",
    ("guru-finalize-task", "blocked"): "blocked-private-state",
}

SCENARIOS = {
    "normal_non_extension": [[
        ("guru-review-task-publication", "ready"),
        ("guru-finalize-task", "verification_required"),
        ("guru-verify-extension-installation", "not_required"),
        ("guru-finalize-task", "published"),
    ]],
    "extension": [[
        ("guru-review-task-publication", "ready"),
        ("guru-finalize-task", "verification_required"),
        ("guru-verify-extension-installation", "verified"),
        ("guru-finalize-task", "published"),
    ]],
    "return_to_task_work": [
        [("guru-review-task-publication", "return_to_task_work")],
        [("guru-verify-extension-installation", "return_to_task_work")],
    ],
    "publication_stale": [[
        ("guru-finalize-task", "publication_review_stale"),
        ("guru-review-task-publication", "ready"),
        ("guru-finalize-task", "published"),
    ]],
    "same_plan_resume": [[
        ("guru-finalize-task", "resume_finalization"),
        ("guru-finalize-task", "published"),
    ]],
    "cross_month_reprepare": [[
        ("guru-finalize-task", "reprepare_required"),
    ]],
    "published_recovery": [[
        ("guru-finalize-task", "published"),
    ]],
    "blocked": [
        [("guru-review-task-publication", "blocked")],
        [("guru-verify-extension-installation", "blocked")],
        [("guru-finalize-task", "blocked")],
    ],
}

AUTHORING_EDGES = {
    ("guru-review-branch", "passed"): (
        "guru-review-task-publication",
        "publication_review",
    ),
    ("guru-review-task-publication", "ready"): (
        "guru-finalize-task",
        "publication_ready",
    ),
    ("guru-finalize-task", "verification_required"): (
        "guru-verify-extension-installation",
        "verification_required",
    ),
    ("guru-verify-extension-installation", "verified"): (
        "guru-finalize-task",
        "verification_verified",
    ),
    ("guru-verify-extension-installation", "not_required"): (
        "guru-finalize-task",
        "standalone_verification_not_required",
    ),
    ("guru-finalize-task", "publication_review_stale"): (
        "guru-review-task-publication",
        "publication_review_stale",
    ),
    ("guru-finalize-task", "resume_finalization"): (
        "guru-finalize-task",
        "same_plan_resume",
    ),
    ("guru-finalize-task", "reprepare_required"): (
        "guru-finalize-task",
        "reprepare_preview",
    ),
}

PRIVATE_FIELDS = {
    "facts_sha256",
    "generated_at",
    "reviewer",
    "review_history",
    "transaction_state",
    "recovery_history",
    "closeout_plan",
    "changed_paths",
    "command_transcript",
}


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{path} must contain a JSON object")
    return value


def interface_for(skill_id: str) -> tuple[Path, dict[str, Any]]:
    package = SKILLS_ROOT / "packages" / skill_id
    interface = read_json(package / "interface.json")
    if interface.get("name") != skill_id:
        raise AssertionError(f"{skill_id} interface identity drifted")
    return package, interface


def public_contract(
    skill_id: str,
    exit_id: str,
) -> tuple[Path, dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    package, interface = interface_for(skill_id)
    outputs = [
        item
        for item in interface["public_contracts"]["outputs"]
        if item.get("exit_id") == exit_id
    ]
    projections = [
        item
        for item in interface["public_contracts"]["projections"]
        if item.get("exit_id") == exit_id
    ]
    exits = [item for item in interface["external_exits"] if item.get("id") == exit_id]
    if len(outputs) != 1 or len(projections) != 1 or len(exits) != 1:
        raise AssertionError(f"{skill_id}:{exit_id} does not have one public route")
    projection = projections[0]
    consumers = [
        item
        for item in interface["public_contracts"]["consumer_inputs"]
        if item.get("id") == projection.get("consumer_input_id")
    ]
    if len(consumers) != 1:
        raise AssertionError(f"{skill_id}:{exit_id} does not have one consumer input")
    return package, outputs[0], consumers[0], projection, exits[0]


def schema_errors(value: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    branches = schema.get("oneOf")
    if isinstance(branches, list):
        matches = [not schema_errors(value, branch, path) for branch in branches]
        return [] if sum(matches) == 1 else [f"{path} must match exactly one branch"]

    errors: list[str] = []
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path} does not match const")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path} is not in enum")

    value_type = schema.get("type")
    if value_type == "object":
        if not isinstance(value, dict):
            return [f"{path} must be an object"]
        required = set(schema.get("required", []))
        missing = required - set(value)
        if missing:
            errors.append(f"{path} is missing {sorted(missing)}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extra = set(value) - set(properties)
            if extra:
                errors.append(f"{path} has extra fields {sorted(extra)}")
        for key, child in properties.items():
            if key in value:
                errors.extend(schema_errors(value[key], child, f"{path}.{key}"))
    elif value_type == "array":
        if not isinstance(value, list):
            return [f"{path} must be an array"]
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path} has too few items")
        if schema.get("uniqueItems") and len({json.dumps(item, sort_keys=True) for item in value}) != len(value):
            errors.append(f"{path} items are not unique")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(schema_errors(item, item_schema, f"{path}[{index}]"))
    elif value_type == "string":
        if not isinstance(value, str):
            return [f"{path} must be a string"]
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path} is too short")
        pattern = schema.get("pattern")
        if isinstance(pattern, str) and re.search(pattern, value) is None:
            errors.append(f"{path} does not match its pattern")
    elif value_type == "integer" and (not isinstance(value, int) or isinstance(value, bool)):
        errors.append(f"{path} must be an integer")
    elif value_type == "boolean" and not isinstance(value, bool):
        errors.append(f"{path} must be a boolean")
    return errors


def apply_projection(projection: dict[str, Any], output: dict[str, Any]) -> dict[str, Any]:
    operation = projection["operation"]
    if operation == "direct":
        return dict(output)
    if operation not in {"select", "rename", "normalize"}:
        raise AssertionError(f"unsupported public projection operation: {operation}")
    projected: dict[str, Any] = {}
    for mapping in projection.get("mappings", []):
        source = mapping["source"]
        target = mapping["target"]
        if target in projected:
            raise AssertionError(f"projection overwrites {target}")
        projected[target] = output[source]
    return projected


def projected_route(skill_id: str, exit_id: str) -> dict[str, Any]:
    package, output_contract, consumer, projection, exit_contract = public_contract(
        skill_id,
        exit_id,
    )
    output = read_json(package / output_contract["example"]["path"])
    output_schema = read_json(package / output_contract["schema"]["path"])
    errors = schema_errors(output, output_schema)
    if errors:
        raise AssertionError(f"{skill_id}:{exit_id} output is invalid: {errors}")
    if output.get("exit_id") != exit_id:
        raise AssertionError(f"{skill_id}:{exit_id} example has the wrong discriminator")
    if PRIVATE_FIELDS & set(output):
        raise AssertionError(f"{skill_id}:{exit_id} exposes private fields")
    if output_contract.get("consumer_use_ids") != [projection["id"]]:
        raise AssertionError(f"{skill_id}:{exit_id} has ambiguous consumer use")
    if exit_contract.get("consumer") != consumer.get("consumer"):
        raise AssertionError(f"{skill_id}:{exit_id} consumer identity drifted")

    projected = apply_projection(projection, output)

    contract = consumer.get("contract", {})
    result: dict[str, Any] = {
        "skill": skill_id,
        "exit_id": exit_id,
        "output": output,
        "consumer": consumer["consumer"],
        "projection": projection["id"],
        "projected_input": projected,
    }
    if contract.get("kind") == "skill_input_authoring_seed":
        seed_fields = set(contract["seed_fields"])
        authoring_fields = set(contract["authoring_fields"])
        if seed_fields & authoring_fields:
            raise AssertionError(f"{skill_id}:{exit_id} seed overlaps authoring")
        if set(projected) != seed_fields:
            raise AssertionError(f"{skill_id}:{exit_id} projected seed drifted")
        target_interface_path = SKILLS_ROOT / contract["interface_path"]
        target_interface = read_json(target_interface_path)
        authoring = read_json(
            target_interface_path.parent / contract["authoring_example"]["path"]
        )
        if set(authoring) != authoring_fields:
            raise AssertionError(f"{skill_id}:{exit_id} authoring example drifted")
        merged = dict(projected)
        for key, value in authoring.items():
            if key in merged:
                raise AssertionError(f"{skill_id}:{exit_id} overwrites {key}")
            merged[key] = value

        target_profiles = [
            item
            for item in target_interface["public_contracts"]["input"]["profiles"]
            if item.get("id") == contract["profile_id"]
        ]
        if len(target_profiles) != 1:
            raise AssertionError(f"{skill_id}:{exit_id} target profile is ambiguous")
        target_schema = read_json(
            target_interface_path.parent / target_profiles[0]["schema"]["path"]
        )
        required = set(target_schema["required"])
        if seed_fields | authoring_fields != required:
            raise AssertionError(f"{skill_id}:{exit_id} does not cover target required fields")
        errors = schema_errors(merged, target_schema)
        if errors:
            raise AssertionError(f"{skill_id}:{exit_id} merged input is invalid: {errors}")
        result["authoring_input"] = authoring
        result["target_profile"] = contract["profile_id"]
        result["merged_input"] = merged
    elif contract.get("kind") == "json_schema":
        consumer_schema = read_json(SKILLS_ROOT / contract["path"])
        errors = schema_errors(projected, consumer_schema)
        if errors:
            raise AssertionError(f"{skill_id}:{exit_id} consumer input is invalid: {errors}")
    return result


class FinishFamilyPublicContractTests(unittest.TestCase):
    def test_13_exit_closure_and_eight_temporary_route_scenarios(self) -> None:
        self.assertEqual(sum(map(len, FINISH_EXITS.values())), 13)
        self.assertEqual(set(EVAL_CASES), {
            (skill_id, exit_id)
            for skill_id, exits in FINISH_EXITS.items()
            for exit_id in exits
        })

        with tempfile.TemporaryDirectory(prefix="guru-finish-routes-") as temporary:
            transcript_root = Path(temporary)
            self.assertFalse(transcript_root.resolve().is_relative_to(REPO.resolve()))
            for scenario, routes in SCENARIOS.items():
                with self.subTest(scenario=scenario):
                    transcripts = []
                    for route in routes:
                        steps = [projected_route(*node) for node in route]
                        for current, following in zip(steps, steps[1:]):
                            consumer = current["consumer"]
                            self.assertEqual(consumer["kind"], "skill")
                            self.assertEqual(consumer["id"], following["skill"])
                        transcripts.append({"scenario": scenario, "steps": steps})
                    path = transcript_root / f"{scenario}.json"
                    path.write_text(
                        json.dumps(transcripts, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8",
                    )
                    self.assertEqual(
                        json.loads(path.read_text(encoding="utf-8")),
                        transcripts,
                    )

    def test_six_key_edges_and_resume_use_target_owned_authoring_partitions(self) -> None:
        for producer, expected_target in AUTHORING_EDGES.items():
            with self.subTest(producer=producer):
                route = projected_route(*producer)
                self.assertEqual(
                    (route["consumer"]["id"], route["target_profile"]),
                    expected_target,
                )


class FinishFamilyPublicWrapperTests(unittest.TestCase):
    def run_eval(
        self,
        skill_id: str,
        adapter: str,
        case_id: str,
        run_root: Path,
        environment: dict[str, str] | None = None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        process = subprocess.run(
            [
                str(EVAL_RUNNER),
                "--root",
                str(REPO),
                "--mode",
                EXECUTION_MODE,
                "--skill",
                skill_id,
                "--adapter",
                adapter,
                "--case",
                case_id,
                "--run-root",
                str(run_root),
                "--json",
            ],
            cwd=REPO,
            env={
                **os.environ,
                "PYTHONDONTWRITEBYTECODE": "1",
                **(environment or {}),
            },
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(process.returncode, 0, process.stderr)
        result = json.loads(process.stdout)
        self.assertEqual(result["status"], "passed", result)
        self.assertEqual(len(result["cases"]), 1, result)
        case = result["cases"][0]
        self.assertEqual(case["status"], "passed", case)
        return result, case

    def assert_public_execution(
        self,
        skill_id: str,
        expected_exit: str,
        case: dict[str, Any],
    ) -> dict[str, Any]:
        self.assertEqual(case["actual_exit"], expected_exit)
        transcript = read_json(Path(case["transcript_locator"]))
        public_stdout = transcript["stdout"]
        if transcript["adapter"] == "codex":
            output_flag = transcript["argv"].index("--output-last-message")
            public_stdout = Path(transcript["argv"][output_flag + 1]).read_text(
                encoding="utf-8"
            )
        elif transcript["adapter"] in {"claude", "cursor"}:
            public_stdout = json.loads(public_stdout)["result"]
        output = json.loads(public_stdout)
        package, contract, _consumer, _projection, _exit = public_contract(
            skill_id,
            expected_exit,
        )
        schema = read_json(package / contract["schema"]["path"])
        self.assertEqual(schema_errors(output, schema), [])
        self.assertEqual(output["exit_id"], expected_exit)
        self.assertTrue(transcript["wrapper_path"].endswith("/scripts/invoke.sh"))

        native_request = read_json(Path(transcript["native_request_path"]))
        self.assertNotIn("expected_exit", native_request)
        self.assertNotIn("files", native_request)
        self.assertNotIn("workdir", native_request)
        native_bytes = json.dumps(native_request, separators=(",", ":"))
        self.assertNotIn("evals/files/", native_bytes)
        self.assertNotIn("guru_team_trellis.py", native_bytes)
        self.assertIsInstance(native_request["public_invocation_arguments"], list)
        self.assertNotIn("runtime_target", native_request)
        trace = read_json(Path(transcript["native_trace_path"]))
        self.assertEqual([event["kind"] for event in trace["events"]], ["read", "invoke"])
        return output

    def test_shared_real_public_wrappers_cover_all_13_finish_exits(self) -> None:
        with tempfile.TemporaryDirectory(prefix="guru-finish-public-") as temporary:
            run_root = Path(temporary)
            self.assertFalse(run_root.resolve().is_relative_to(REPO.resolve()))
            for (skill_id, exit_id), case_id in EVAL_CASES.items():
                with self.subTest(skill=skill_id, exit=exit_id):
                    _result, case = self.run_eval(
                        skill_id,
                        "shared",
                        case_id,
                        run_root / skill_id / exit_id,
                    )
                    self.assert_public_execution(skill_id, exit_id, case)

    def write_fake_native_commands(self, root: Path) -> Path:
        root.mkdir(parents=True)
        script = textwrap.dedent(
            """\
            #!/usr/bin/env python3
            from __future__ import annotations

            import json
            import os
            import subprocess
            import sys
            from pathlib import Path


            def option(arguments, flag):
                index = arguments.index(flag)
                return arguments[index + 1]


            def main():
                command = Path(sys.argv[0]).name
                arguments = sys.argv[1:]
                if command == "cursor-agent" and arguments == ["status"]:
                    print("Logged in")
                    return 0
                request_path = Path(os.environ["GURU_TEAM_NATIVE_REQUEST"])
                request = json.loads(request_path.read_text(encoding="utf-8"))
                protocol = json.loads(
                    Path(os.environ["GURU_TEAM_NATIVE_PROTOCOL"]).read_text(encoding="utf-8")
                )
                invocation_arguments = request.get("public_invocation_arguments")
                if not isinstance(invocation_arguments, list):
                    print("public invocation facts are unavailable", file=sys.stderr)
                    return 74
                helper = str(protocol["helper_path"])
                common = [
                    "--trace", str(protocol["trace_path"]),
                    "--request-sha256", str(protocol["request_sha256"]),
                    "--projection-root", str(protocol["projection_root"]),
                    "--skill-sha256", str(protocol["skill_sha256"]),
                    "--wrapper-sha256", str(protocol["wrapper_sha256"]),
                ]
                read = subprocess.run(
                    [sys.executable, helper, *common, "read", "--kind", "skill_contract",
                     "--path", str(protocol["skill_path"])],
                    text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
                )
                if read.returncode != 0:
                    sys.stderr.write(read.stderr)
                    return read.returncode
                invoked = subprocess.run(
                    [sys.executable, helper, *common, "invoke", "--wrapper",
                     str(protocol["wrapper_path"]), "--",
                     *invocation_arguments],
                    cwd=request["public_package_root"],
                    text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
                )
                if invoked.returncode != 0:
                    sys.stderr.write(invoked.stderr)
                    return invoked.returncode
                if command == "codex":
                    Path(option(arguments, "--output-last-message")).write_text(
                        invoked.stdout, encoding="utf-8"
                    )
                    print(json.dumps({"type": "turn.completed"}))
                else:
                    print(json.dumps({"result": invoked.stdout}))
                return 0


            if __name__ == "__main__":
                raise SystemExit(main())
            """
        )
        source = root / "fake-finish-native"
        source.write_text(script, encoding="utf-8")
        source.chmod(0o755)
        for name in ("codex", "claude", "cursor-agent"):
            shutil.copy2(source, root / name)
        return root

    def test_real_adapters_consume_normal_and_extension_combined_routes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="guru-finish-platforms-") as temporary:
            temporary_root = Path(temporary)
            binaries = self.write_fake_native_commands(temporary_root / "bin")
            environment = {
                "PATH": f"{binaries}{os.pathsep}{os.environ.get('PATH', '')}",
            }
            for route in (
                "not-required-reentry-published",
                "verified-reentry-published",
            ):
                outputs = []
                corpus_identities = []
                for adapter in REAL_ADAPTERS:
                    with self.subTest(route=route, adapter=adapter):
                        result, case = self.run_eval(
                            "guru-finalize-task",
                            adapter,
                            route,
                            temporary_root / "runs" / route / adapter,
                            environment,
                        )
                        outputs.append(
                            self.assert_public_execution(
                                "guru-finalize-task",
                                "published",
                                case,
                            )
                        )
                        corpus_identities.append(
                            (
                                result["corpus_schema_id"],
                                result["corpus_version"],
                            )
                        )
                self.assertEqual(outputs, [outputs[0]] * len(REAL_ADAPTERS))
                self.assertEqual(
                    corpus_identities,
                    [corpus_identities[0]] * len(REAL_ADAPTERS),
                )


if __name__ == "__main__":
    unittest.main()
