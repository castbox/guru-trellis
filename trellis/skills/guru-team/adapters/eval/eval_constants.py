from __future__ import annotations

from typing import Any
import sys


ADAPTERS = ("shared", "codex", "claude", "cursor")

OWNER_INPUT = ".trellis/.runtime/guru-team/evals/public-input.json"

OWNER_RESULT = ".trellis/.runtime/guru-team/evals/owner-result.json"

OWNER_PLAN = ".trellis/.runtime/guru-team/evals/owner-plan.json"

OWNER_INVOCATION = ".trellis/.runtime/guru-team/evals/invocation.json"

WORKSPACE_CALL_LOCAL_STATE: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}

PRODUCTION_SKILLS = {
    "guru-approve-task-plan",
    "guru-check-task",
    "guru-create-task-commit",
    "guru-finalize-task",
    "guru-merge-task-pr",
    "guru-reconcile-task-base",
    "guru-review-branch",
    "guru-review-task-publication",
    "guru-restore-archived-task",
    "guru-verify-extension-installation",
}

QUALIFICATION_SKILL = "guru-qualify-normal-scenario"

QUALIFICATION_MODEL = "gpt-5.6-sol"

QUALIFICATION_MODEL_REQUEST_SCHEMA = "3.0"

QUALIFICATION_PROMPT_PROTOCOL = "guru-qualification-production-prompt-2.0"

QUALIFICATION_PERMISSION_PROFILE = "guru-qualification-production"

QUALIFICATION_PUBLIC_AUTHORING_FACTS = "docs/qualification-eval/public-authoring-facts.json"

MINIMAL_NATIVE_ENVIRONMENT_KEYS = (
    "HOME",
    "LANG",
    "LC_ALL",
    "LC_CTYPE",
    "PATH",
    "SSL_CERT_DIR",
    "SSL_CERT_FILE",
    "TERM",
    "TMPDIR",
)

SECRET_ENVIRONMENT_MARKERS = (
    "API_KEY",
    "ACCESS_TOKEN",
    "AUTH_TOKEN",
    "BEARER",
    "CREDENTIAL",
    "DATABASE_URL",
    "PASSWORD",
    "PRIVATE_KEY",
    "SECRET",
    "SESSION_TOKEN",
)

MANAGED_PYTHON_SHEBANG = f"#!{sys.executable}\n"

TRACE_HELPER = MANAGED_PYTHON_SHEBANG + r'''from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def stdout_digest(value: str) -> str:
    try:
        payload = json.loads(value)
    except json.JSONDecodeError:
        normalized = value.strip()
    else:
        normalized = json.dumps(payload, separators=(",", ":"))
    return digest(normalized.encode("utf-8"))


def append_event(
    trace_path: Path,
    request_sha256: str,
    projection_root: str,
    skill_sha256: str,
    wrapper_sha256: str,
    event: dict[str, object],
) -> None:
    if trace_path.exists():
        payload = json.loads(trace_path.read_text(encoding="utf-8"))
    else:
        payload = {
            "schema_version": "1.0",
            "request_sha256": request_sha256,
            "projection_root": projection_root,
            "skill_sha256": skill_sha256,
            "wrapper_sha256": wrapper_sha256,
            "events": [],
        }
    if (
        payload.get("request_sha256") != request_sha256
        or payload.get("projection_root") != projection_root
        or payload.get("skill_sha256") != skill_sha256
        or payload.get("wrapper_sha256") != wrapper_sha256
        or not isinstance(payload.get("events"), list)
    ):
        raise ValueError("native trace request binding mismatch")
    event["request_sha256"] = request_sha256
    payload["events"].append(event)
    trace_path.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", required=True)
    parser.add_argument("--request-sha256", required=True)
    parser.add_argument("--projection-root", required=True)
    parser.add_argument("--skill-sha256", required=True)
    parser.add_argument("--wrapper-sha256", required=True)
    subparsers = parser.add_subparsers(dest="operation", required=True)
    read_parser = subparsers.add_parser("read")
    read_parser.add_argument(
        "--kind",
        required=True,
        choices=("skill_contract", "case_file", "owner_file"),
    )
    read_parser.add_argument("--path", required=True)
    invoke_parser = subparsers.add_parser("invoke")
    invoke_parser.add_argument("--wrapper", required=True)
    invoke_parser.add_argument("--execution-wrapper", required=True)
    invoke_parser.add_argument("--stdin", action="store_true")
    invoke_parser.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    trace_path = Path(args.trace).resolve()
    if args.operation == "read":
        target = Path(args.path).resolve()
        content = target.read_bytes()
        append_event(trace_path, args.request_sha256, args.projection_root, args.skill_sha256, args.wrapper_sha256, {
            "kind": "read", "target_kind": args.kind, "path": str(target), "sha256": digest(content),
        })
        sys.stdout.buffer.write(content)
        return 0
    wrapper = Path(args.wrapper).resolve()
    forwarded = list(args.arguments)
    if forwarded and forwarded[0] == "--":
        forwarded = forwarded[1:]
    execution_wrapper = Path(args.execution_wrapper).resolve()
    process = subprocess.run(
        [str(execution_wrapper), "--package-root", args.projection_root, *forwarded], text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False, input=sys.stdin.read() if args.stdin else None,
    )
    append_event(trace_path, args.request_sha256, args.projection_root, args.skill_sha256, args.wrapper_sha256, {
        "kind": "invoke", "wrapper_path": str(wrapper), "argv": [str(wrapper), *forwarded],
        "returncode": process.returncode, "stdout_sha256": stdout_digest(process.stdout),
        "stderr_sha256": digest(process.stderr.encode("utf-8")),
    })
    sys.stdout.write(process.stdout)
    sys.stderr.write(process.stderr)
    return process.returncode


if __name__ == "__main__":
    import sys
    raise SystemExit(main())
'''

QUALIFICATION_TRACE_HELPER_BODY = r'''from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def stdout_digest(value: str) -> str:
    try:
        payload = json.loads(value)
    except json.JSONDecodeError:
        normalized = value.strip()
    else:
        normalized = json.dumps(payload, separators=(",", ":"))
    return digest(normalized.encode("utf-8"))


def append_event(
    trace_path: Path,
    request_sha256: str,
    projection_root: str,
    skill_sha256: str,
    wrapper_sha256: str,
    event: dict[str, object],
) -> None:
    if trace_path.exists():
        payload = json.loads(trace_path.read_text(encoding="utf-8"))
    else:
        payload = {
            "schema_version": "1.0",
            "request_sha256": request_sha256,
            "projection_root": projection_root,
            "skill_sha256": skill_sha256,
            "wrapper_sha256": wrapper_sha256,
            "events": [],
        }
    if (
        payload.get("request_sha256") != request_sha256
        or payload.get("projection_root") != projection_root
        or payload.get("skill_sha256") != skill_sha256
        or payload.get("wrapper_sha256") != wrapper_sha256
        or not isinstance(payload.get("events"), list)
    ):
        raise ValueError("native trace request binding mismatch")
    event["request_sha256"] = request_sha256
    payload["events"].append(event)
    trace_path.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")


def inside(root: Path, target: Path) -> bool:
    try:
        target.relative_to(root)
    except ValueError:
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", required=True)
    parser.add_argument("--request-sha256", required=True)
    parser.add_argument("--projection-root", required=True)
    parser.add_argument("--repository-root", required=True)
    parser.add_argument("--sandbox-root", required=True)
    parser.add_argument("--request-fifo", required=True)
    parser.add_argument("--response-fifo", required=True)
    parser.add_argument("--skill-sha256", required=True)
    parser.add_argument("--wrapper-sha256", required=True)
    subparsers = parser.add_subparsers(dest="operation", required=True)
    read_parser = subparsers.add_parser("read")
    read_parser.add_argument(
        "--kind",
        required=True,
        choices=("skill_contract", "case_file", "owner_file"),
    )
    read_parser.add_argument("--path", required=True)
    invoke_parser = subparsers.add_parser("invoke")
    invoke_parser.add_argument("--stdin", action="store_true")
    args = parser.parse_args()
    sandbox_root = Path(args.sandbox_root).resolve()
    projection_root = Path(args.projection_root).resolve()
    repository_root = Path(args.repository_root).resolve()
    trace_path = Path(args.trace).resolve()
    if not all(inside(sandbox_root, path) for path in (
        projection_root,
        repository_root,
        trace_path,
        Path(args.request_fifo).resolve(),
        Path(args.response_fifo).resolve(),
    )):
        raise ValueError("qualification helper path escapes the model sandbox")
    if args.operation == "read":
        target = Path(args.path).resolve()
        allowed_root = repository_root if args.kind == "owner_file" else sandbox_root
        if not inside(allowed_root, target):
            raise ValueError("qualification read target escapes its projected root")
        if "evals" in target.parts or ".runtime" in target.parts:
            raise ValueError("qualification read target is private")
        content = target.read_bytes()
        append_event(trace_path, args.request_sha256, str(projection_root), args.skill_sha256, args.wrapper_sha256, {
            "kind": "read", "target_kind": args.kind, "path": str(target), "sha256": digest(content),
        })
        sys.stdout.buffer.write(content)
        return 0
    if not args.stdin:
        raise ValueError("qualification invocation requires stdin")
    request_fifo = Path(args.request_fifo)
    response_fifo = Path(args.response_fifo)
    request_payload = {
        "arguments": ["--invocation", "-"],
        "stdin": sys.stdin.read(),
    }
    with request_fifo.open("w", encoding="utf-8") as handle:
        json.dump(request_payload, handle, separators=(",", ":"))
    with response_fifo.open("r", encoding="utf-8") as handle:
        response = json.load(handle)
    if set(response) != {"returncode", "stdout", "stderr"}:
        raise ValueError("qualification invocation response is invalid")
    append_event(trace_path, args.request_sha256, str(projection_root), args.skill_sha256, args.wrapper_sha256, {
        "kind": "invoke", "wrapper_path": str(projection_root / "scripts/invoke.sh"),
        "argv": [str(projection_root / "scripts/invoke.sh"), "--invocation", "-"],
        "returncode": response["returncode"], "stdout_sha256": stdout_digest(response["stdout"]),
        "stderr_sha256": digest(response["stderr"].encode("utf-8")),
    })
    sys.stdout.write(response["stdout"])
    sys.stderr.write(response["stderr"])
    return int(response["returncode"])


if __name__ == "__main__":
    raise SystemExit(main())
'''
