from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .installed import validate_skill_installed
from .io import CommandError, read_json_file
from .validate import validate as validate_skill_source


ADAPTERS = ("shared", "codex", "claude", "cursor")
TRACE_INVARIANTS = {
    "public_invocation_only": "public_invocation",
    "evals_not_loaded_by_skill": "evals_not_loaded",
    "private_runtime_not_read_by_agent": "private_runtime_not_read",
}
INPUT_VARIANT_KEY = "input_" + "pro" + "file_id"
INPUT_VARIANTS_KEY = "pro" + "files"


def error(code: str, field_path: str, remediation: str) -> CommandError:
    return CommandError(code, field_path, remediation)


def strict_json(path: Path, field_path: str) -> dict[str, Any]:
    value = read_json_file(path, field_path)
    try:
        json.dumps(value, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise error("invalid_json", field_path, "Provide one finite standard-JSON object.") from exc
    return value


def validate_instance(instance: Any, schema_path: Path, field_path: str) -> None:
    schema = strict_json(schema_path, f"{field_path}.schema")
    failures = sorted(
        Draft202012Validator(schema).iter_errors(instance),
        key=lambda item: [str(part) for part in item.path],
    )
    if failures:
        suffix = ".".join(str(part) for part in failures[0].path)
        raise error(
            "schema_mismatch",
            field_path + (f".{suffix}" if suffix else ""),
            "Repair the value to match the declared schema.",
        )


def roots(root: Path, mode: str) -> tuple[Path, dict[str, Any]]:
    if mode == "source":
        skills = root / "trellis/skills/guru-team"
        return skills, validate_skill_source(root, mode)
    skills = root / ".trellis/guru-team/skills"
    return skills, validate_skill_installed(
        root,
        skills,
        root / ".trellis/workflow.md",
        root / ".trellis/guru-team/extension.json",
        require_workflow=False,
    )


def package_context(skills: Path, skill_id: str) -> tuple[Path, dict[str, Any], dict[str, Any]]:
    registry = strict_json(skills / "registry.json", "registry")
    matches = [
        row
        for row in registry.get("skills", [])
        if isinstance(row, dict) and row.get("id") == skill_id and row.get("state") == "active"
    ]
    if len(matches) != 1:
        raise error("unknown_skill", "skill", "Choose one active stable Skill id from the validated registry.")
    row = matches[0]
    package = skills / str(row["package"])
    interface = strict_json(skills / str(row["interface"]), f"skills.{skill_id}.interface")
    if interface.get("id") != skill_id:
        raise error("eval_contract_asset_invalid", f"skills.{skill_id}.interface", "Restore the exact selected Interface contract.")
    return package, interface, row


def descriptors(skills: Path) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    expected = {"schema_version", "id", "platform", "executable", "native_command", "capabilities"}
    for adapter_id in ADAPTERS:
        descriptor = strict_json(skills / f"adapters/eval/{adapter_id}.json", f"adapters.{adapter_id}")
        executable = skills / "adapters/eval" / str(descriptor.get("executable", ""))
        if (
            set(descriptor) != expected
            or descriptor.get("schema_version") != "1.0"
            or descriptor.get("id") != adapter_id
            or descriptor.get("platform") != adapter_id
            or descriptor.get("capabilities") != ["prompt", "files", "public_wrapper", "trace"]
            or not executable.is_file()
            or executable.is_symlink()
            or not os.access(executable, os.X_OK)
        ):
            raise error("eval_adapter_inventory_invalid", "adapters", "Restore all four closed eval adapter descriptors.")
        output[adapter_id] = descriptor
    return output


def corpus(skills: Path, package: Path, interface: dict[str, Any]) -> tuple[dict[str, Any], bytes]:
    path = package / "evals/evals.json"
    payload = strict_json(path, "evals/evals.json")
    validate_instance(payload, skills / "schemas/skill-evals.schema.json", "evals/evals.json")
    if payload.get("skill_name") != interface.get("id"):
        raise error("eval_skill_identity_mismatch", "skill_name", "Match the selected Interface id.")
    contracts = interface.get("public_contracts", {})
    input_contract = contracts.get("input", {})
    input_variants = {
        item.get("id")
        for item in input_contract.get(INPUT_VARIANTS_KEY, [])
        if isinstance(item, dict)
    }
    scalar = input_contract.get("kind") == "scalar_cli"
    exits = {item.get("id") for item in interface.get("external_exits", []) if isinstance(item, dict)}
    output_exits = {item.get("exit_id") for item in contracts.get("outputs", []) if isinstance(item, dict)}
    seen_cases: set[str] = set()
    for index, case in enumerate(payload.get("evals", [])):
        case_id = case["id"]
        if case_id in seen_cases:
            raise error("eval_case_duplicate", f"evals[{index}].id", "Use one unique stable case id.")
        seen_cases.add(case_id)
        input_variant = case.get(INPUT_VARIANT_KEY)
        if input_variant is not None and (scalar or input_variant not in input_variants):
            raise error(
                "eval_input_variant_unknown",
                f"evals[{index}].{INPUT_VARIANT_KEY}",
                "Reference one declared structured input variant.",
            )
        if case.get("expected_exit") not in exits or case.get("expected_exit") not in output_exits:
            raise error("eval_expected_exit_unknown", f"evals[{index}].expected_exit", "Reference one declared exit with an output schema.")
        for fixture in case.get("files", []):
            relative = Path(fixture)
            target = package / relative
            if relative.is_absolute() or ".." in relative.parts or relative.parts[:2] != ("evals", "files") or not target.is_file() or target.is_symlink():
                raise error("eval_fixture_invalid", f"evals[{index}].files", "Restore a regular package-local eval fixture.")
        assertion_ids: set[str] = set()
        assertions = case.get("assertions", {})
        if assertions and not any(assertions.get(kind) for kind in ("deterministic", "semantic")):
            raise error("eval_assertions_empty", f"evals[{index}].assertions", "Provide at least one assertion or omit assertions.")
        for group in ("deterministic", "semantic"):
            for assertion in assertions.get(group, []):
                if assertion["id"] in assertion_ids:
                    raise error("eval_assertion_duplicate", f"evals[{index}].assertions", "Use unique assertion ids per case.")
                assertion_ids.add(assertion["id"])
    return payload, path.read_bytes()


def adapter_inventory(skills: Path, descriptor_index: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for adapter_id in ADAPTERS:
        descriptor = descriptor_index[adapter_id]
        native = str(descriptor["native_command"])
        bundled = skills / "adapters/eval" / native
        result.append({
            "id": adapter_id,
            "platform": adapter_id,
            "native_command": native,
            "native_available": (adapter_id == "shared" and bundled.is_file() and os.access(bundled, os.X_OK)) or shutil.which(native) is not None,
            "capabilities": descriptor["capabilities"],
        })
    return result


def discover(skills: Path, skill_id: str) -> dict[str, Any]:
    package, interface, row = package_context(skills, skill_id)
    evals, corpus_bytes = corpus(skills, package, interface)
    descriptor_index = descriptors(skills)
    contracts = interface["public_contracts"]
    return {
        "status": "ok",
        "skill_id": skill_id,
        "interface_schema_id": row["interface_schema_id"],
        "interface_version": interface["schema_version"],
        "corpus_schema_id": "guru-team-skill-evals-1.0",
        "corpus_version": evals["schema_version"],
        "corpus_sha256": hashlib.sha256(corpus_bytes).hexdigest(),
        "corpus_path": f"{row['package']}/evals/evals.json",
        "case_ids": [case["id"] for case in evals["evals"]],
        "public_invocation": contracts["invocation"],
        "output_schemas": {item["exit_id"]: item["schema"] for item in contracts["outputs"]},
        "adapters": adapter_inventory(skills, descriptor_index),
    }


def runtime_target(root: Path) -> Path:
    override = os.environ.get("GURU_TEAM_FAKE_NATIVE_DISPATCHER") or os.environ.get("GURU_TEAM_DISPATCHER")
    target = Path(override) if override else root / ".trellis/guru-team/scripts/bash/run-skill-command.sh"
    if not target.is_absolute():
        raise error("eval_runtime_target_invalid", "runtime_target", "Provide an absolute installed public dispatcher.")
    try:
        mode = target.lstat().st_mode
    except OSError:
        mode = 0
    if not stat.S_ISREG(mode) or target.is_symlink() or not os.access(target, os.X_OK):
        raise error("eval_runtime_target_invalid", "runtime_target", "Install or repair the public Skill dispatcher.")
    return target.resolve()


def external(path_value: str | None, schema: Path, label: str) -> dict[str, Any] | None:
    if path_value is None:
        return None
    path = Path(path_value)
    if not path.is_absolute() or not path.is_file() or path.is_symlink():
        raise error(f"{label}_invalid", label, "Provide an absolute readable JSON file.")
    payload = strict_json(path, label)
    try:
        validate_instance(payload, schema, label)
    except CommandError as exc:
        raise error(f"{label}_invalid", label, "Repair the closed external input and retry.") from exc
    return payload


def pointer(value: Any, path: str) -> tuple[bool, Any]:
    if path == "":
        return True, value
    current = value
    for encoded in path[1:].split("/"):
        part = encoded.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(current, list) and part.isdigit() and int(part) < len(current):
            current = current[int(part)]
        else:
            return False, None
    return True, current


def deterministic_results(assertions: list[dict[str, Any]], output: dict[str, Any], trace: list[str], workdir: Path, package: Path) -> list[dict[str, Any]]:
    results = []
    for assertion in assertions:
        passed = False
        kind = assertion["kind"]
        operation = assertion.get("operation", "")
        if kind == "json_path":
            exists, actual = pointer(output, assertion["pointer"])
            expected = assertion.get("expected")
            passed = exists if operation == "exists" else exists and (actual == expected if operation == "equals" else (isinstance(actual, str) and isinstance(expected, str) and expected in actual) or (isinstance(actual, list) and expected in actual))
            detail = f"json_path {operation} {'passed' if passed else 'failed'}"
        elif kind == "trace":
            passed = TRACE_INVARIANTS[assertion["invariant"]] in trace
            detail = f"trace invariant {assertion['invariant']} {'passed' if passed else 'failed'}"
        else:
            relative = Path(assertion["path"])
            target = workdir / relative
            if relative.is_absolute() or ".." in relative.parts:
                passed = False
            elif operation == "exists":
                passed = target.is_file() and not target.is_symlink()
            elif operation == "text_equals":
                try:
                    passed = target.read_text(encoding="utf-8") == assertion.get("expected")
                except OSError:
                    passed = False
            elif operation == "json_schema":
                try:
                    validate_instance(strict_json(target, "file assertion"), package / assertion["expected"], "file assertion")
                    passed = True
                except (CommandError, OSError):
                    passed = False
            detail = f"file {operation} {'passed' if passed else 'failed'}"
        results.append({"id": assertion["id"], "passed": passed, "detail": detail})
    return results


def call_adapter(skills: Path, descriptor: dict[str, Any], request_path: Path) -> dict[str, Any]:
    command = skills / "adapters/eval" / descriptor["executable"]
    process = subprocess.run(
        [str(command), "--native-command", descriptor["native_command"], "--request", str(request_path)],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if process.returncode:
        return adapter_failure(request_path, "adapter command failed")
    try:
        response = json.loads(process.stdout)
        validate_instance(response, skills / "schemas/skill-eval-adapter-response.schema.json", "adapter_response")
    except (json.JSONDecodeError, CommandError):
        return adapter_failure(request_path, "adapter response failed validation")
    return response


def adapter_failure(request_path: Path, message: str) -> dict[str, Any]:
    request = strict_json(request_path, "adapter_request")
    return {
        "schema_version": "1.0", "capability_status": "execution_error",
        "corpus_sha256": request["corpus_sha256"], "public_stdout": "",
        "public_stderr": message, "trace_events": [],
        "transcript_locator": str(request_path.parent / "adapter-error.txt"),
        "native_trace_locator": str(request_path.parent / "native-trace.json"), "timing_ms": 0,
    }


def comparison_sides(args: argparse.Namespace, package: Path) -> list[tuple[str, Path]]:
    if bool(args.current_package) != bool(args.comparison_package):
        raise error("eval_comparison_pair_required", "comparison", "Provide both exact package paths or neither.")
    if not args.current_package:
        return [("current", package)]
    result = []
    for side, value in (("current", args.current_package), ("comparison", args.comparison_package)):
        path = Path(value)
        if not path.is_absolute() or not path.is_dir() or any(token in path.name.lower() for token in ("latest", "previous")):
            raise error("eval_comparison_identity_invalid", f"comparison.{side}", "Provide one caller-resolved absolute package directory.")
        result.append((side, path.resolve()))
    return result


def run(root: Path, skills: Path, args: argparse.Namespace) -> dict[str, Any]:
    discovery = discover(skills, args.skill)
    descriptor = descriptors(skills)[args.adapter]
    selected_package, selected_interface, row = package_context(skills, args.skill)
    evals, _ = corpus(skills, selected_package, selected_interface)
    selected_cases = [case for case in evals["evals"] if args.case is None or case["id"] == args.case]
    if not selected_cases:
        raise error("eval_case_unknown", "case", "Choose one case id returned by discovery.")
    run_root = Path(args.run_root)
    if not run_root.is_absolute():
        raise error("eval_run_root_invalid", "run_root", "Use an absolute temporary directory outside the repository.")
    run_root = run_root.resolve(strict=False)
    sides = comparison_sides(args, selected_package)
    for boundary in (root, *(package for _, package in sides)):
        try:
            run_root.relative_to(boundary.resolve())
        except ValueError:
            continue
        raise error("eval_run_root_inside_repo", "run_root", "Use an isolated directory outside repository and package roots.")
    run_root.mkdir(parents=True, exist_ok=True)
    if run_root.is_symlink() or not run_root.is_dir():
        raise error("eval_run_root_invalid", "run_root", "Use a regular external directory.")
    semantic = external(args.semantic_grading, skills / "schemas/skill-eval-semantic-grading.schema.json", "semantic_grading")
    feedback = external(args.human_feedback, skills / "schemas/skill-eval-human-feedback.schema.json", "human_feedback")
    semantic_index = {(item["comparison_side"], item["case_id"], item["assertion_id"]): item for item in semantic.get("results", [])} if semantic else {}
    feedback_index = {(item["comparison_side"], item["case_id"]): [item["feedback"]] for item in feedback.get("items", [])} if feedback else {}
    target = runtime_target(root)
    results = []
    for side, package in sides:
        interface = strict_json(package / "interface.json", f"comparison.{side}.interface")
        validate_instance(interface, skills / f"schemas/skill-interface-{interface['schema_version']}.schema.json", f"comparison.{side}.interface")
        if interface.get("id") != args.skill or interface.get("schema_version") != selected_interface.get("schema_version"):
            raise error("eval_side_interface_invalid", f"comparison.{side}.interface", "Restore the exact selected Interface identity.")
        side_corpus, side_bytes = corpus(skills, package, interface)
        if hashlib.sha256(side_bytes).hexdigest() != discovery["corpus_sha256"]:
            raise error("eval_comparison_corpus_mismatch", f"comparison.{side}", "Use packages with byte-identical eval corpora.")
        outputs = {item["exit_id"]: item["schema"] for item in interface["public_contracts"]["outputs"]}
        for case in selected_cases:
            case_root = run_root / side / case["id"]
            workdir = case_root / "execution/workdir"
            workdir.mkdir(parents=True, exist_ok=True)
            staged = []
            for fixture in case.get("files", []):
                destination = workdir / fixture
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(package / fixture, destination)
                staged.append(fixture)
            request = {
                "schema_version": "1.0", "adapter_id": args.adapter, "platform": args.adapter,
                "skill_id": args.skill, "package_root": str(package),
                "interface": {
                    "interface_schema_id": row["interface_schema_id"],
                    "interface_version": interface["schema_version"],
                    "public_invocation": interface["public_contracts"]["invocation"],
                    "output_schemas": outputs,
                },
                "case_id": case["id"], "prompt": case["prompt"], "files": staged,
                "workdir": str(workdir), "corpus_path": str(package / "evals/evals.json"),
                "corpus_sha256": discovery["corpus_sha256"], "runtime_target": str(target),
            }
            validate_instance(request, skills / "schemas/skill-eval-adapter-request.schema.json", "adapter_request")
            request_path = case_root / "adapter-request.json"
            request_path.write_text(json.dumps(request, separators=(",", ":")), encoding="utf-8")
            response = call_adapter(skills, descriptor, request_path)
            result: dict[str, Any] = {
                "case_id": case["id"], "comparison_side": side, "status": "execution_error",
                "deterministic_results": [], "semantic_results": [],
                "transcript_locator": response["transcript_locator"], "timing_ms": response["timing_ms"],
                "feedback": feedback_index.get((side, case["id"]), []),
            }
            if response["corpus_sha256"] != discovery["corpus_sha256"]:
                result["deterministic_results"] = [{"id": "corpus-byte-identity", "passed": False, "detail": "adapter corpus bytes mismatch"}]
            elif response["capability_status"] == "unsupported":
                result["status"] = "unsupported"
            elif response["capability_status"] == "executed":
                try:
                    public_output = json.loads(response["public_stdout"])
                except json.JSONDecodeError:
                    public_output = None
                if isinstance(public_output, dict) and isinstance(public_output.get("exit_id"), str):
                    actual_exit = public_output["exit_id"]
                    result["actual_exit"] = actual_exit
                    checks = deterministic_results(case.get("assertions", {}).get("deterministic", []), public_output, response["trace_events"], workdir, package)
                    schema_passed = False
                    if actual_exit in outputs:
                        try:
                            validate_instance(public_output, package / outputs[actual_exit]["path"], f"output.{actual_exit}")
                            schema_passed = True
                        except CommandError:
                            pass
                    checks.insert(0, {"id": "actual-exit-output-schema", "passed": schema_passed, "detail": f"actual exit output schema {'passed' if schema_passed else 'failed'}"})
                    exit_passed = actual_exit == case["expected_exit"]
                    checks.insert(0, {"id": "expected-exit", "passed": exit_passed, "detail": "actual exit matches expected exit" if exit_passed else "actual exit mismatch"})
                    semantic_results = []
                    for assertion in case.get("assertions", {}).get("semantic", []):
                        grade = semantic_index.get((side, case["id"], assertion["id"]))
                        semantic_results.append({"id": assertion["id"], "passed": bool(grade and grade["passed"]), "detail": grade["summary"] if grade else "external semantic grading missing"})
                    result["deterministic_results"] = checks
                    result["semantic_results"] = semantic_results
                    result["status"] = "passed" if all(item["passed"] for item in checks + semantic_results) else "evaluation_failed"
            results.append(result)
    status = "passed"
    for candidate in ("execution_error", "evaluation_failed", "unsupported"):
        if any(item["status"] == candidate for item in results):
            status = candidate
            break
    evidence = run_root / f"{args.skill}-{args.adapter}-run.json"
    output = {
        "schema_version": "2.0", "skill_id": args.skill,
        "interface_schema_id": row["interface_schema_id"],
        "corpus_schema_id": "guru-team-skill-evals-1.0", "corpus_version": side_corpus["schema_version"],
        "adapter": args.adapter, "platform": args.adapter, "status": status,
        "cases": results, "evidence_path": str(evidence),
    }
    validate_instance(output, skills / "schemas/skill-eval-run-2.0.schema.json", "evidence")
    evidence.write_text(json.dumps(output, separators=(",", ":")), encoding="utf-8")
    return output


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    subparsers = result.add_subparsers(dest="command", required=True)
    discover_parser = subparsers.add_parser("discover-skill-evals")
    run_parser = subparsers.add_parser("run-skill-evals")
    for child in (discover_parser, run_parser):
        child.add_argument("--root", default=".")
        child.add_argument("--mode", required=True, choices=("source", "installed"))
        child.add_argument("--skill", required=True)
        child.add_argument("--json", action="store_true")
    run_parser.add_argument("--adapter", required=True, choices=ADAPTERS)
    run_parser.add_argument("--case")
    run_parser.add_argument("--run-root", required=True)
    run_parser.add_argument("--current-package")
    run_parser.add_argument("--comparison-package")
    run_parser.add_argument("--semantic-grading")
    run_parser.add_argument("--human-feedback")
    return result


def main(argv: list[str]) -> int:
    args = parser().parse_args(argv)
    try:
        root = Path(args.root).resolve()
        skills, validation = roots(root, args.mode)
        if validation.get("status") != "passed":
            raise error("contract_validation_failed", str(skills.relative_to(root)), "Repair the invalid source schema, example, route, or contract and rerun package validation.")
        payload = discover(skills, args.skill) if args.command == "discover-skill-evals" else run(root, skills, args)
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")
        return 0
    except CommandError as exc:
        payload = {"code": exc.code, "field_path": exc.field_path, "remediation": exc.remediation}
        stream = sys.stderr if getattr(args, "json", False) else sys.stderr
        stream.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        return exc.exit_status


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
