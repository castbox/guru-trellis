"""Facts and command receipts for the eval-only standard Intake flow."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
from pathlib import Path
import subprocess
from typing import Any

from adapters.eval.fixture_io import run_git, write_fake_gh

INTAKE_SKILLS = (
    "guru-sync-base",
    "guru-discover-change-context",
    "guru-clarify-requirements",
    "guru-review-contract-wording",
    "guru-review-change-request",
)
FACTS_PATH = "docs/intake/public-source-facts.json"
COMMANDS = {
    INTAKE_SKILLS[0]: ("invoke",),
    INTAKE_SKILLS[1]: ("preview-change-context-history", "record-context-discovery", "check-context-discovery", "invoke"),
    INTAKE_SKILLS[2]: ("record-requirements-clarification", "check-requirements-clarification", "invoke"),
    INTAKE_SKILLS[3]: ("record-contract-wording-review", "check-contract-wording-review", "invoke"),
    INTAKE_SKILLS[4]: ("record-change-request-review", "check-change-request-review", "invoke"),
}


def standard_intake(request: dict[str, Any]) -> bool:
    flow = request.get("native_authoring_flow")
    if flow is None:
        return False
    if (flow != "standard_intake" or request.get("native_execution_mode") != "semantic_authoring"
            or request.get("skill_id") != INTAKE_SKILLS[-1]):
        raise ValueError("standard_intake requires Readiness semantic_authoring")
    return True


def stdout_digest(value: str) -> str:
    try:
        value = json.dumps(json.loads(value), separators=(",", ":"))
    except ValueError:
        value = value.strip()
    return hashlib.sha256(value.encode()).hexdigest()


def stage_intake_facts(request: dict[str, Any], execution_root: Path,
                       fixture: Path) -> tuple[Path, Path, dict[str, str]]:
    standard_intake(request)
    if len(request["files"]) != 1:
        raise ValueError("Intake authoring requires one source fixture")
    facts = json.loads((Path(request["workdir"]) / request["files"][0]).read_text())
    if set(facts) != {"source", "repository_files"}:
        raise ValueError("Intake fixture contains non-source fields")
    source = facts["source"]
    retrieval = Path(request["runtime_target"]).parents[4] / ".trellis/spec/workflow/semantic-retrieval.md"
    target_retrieval = fixture / ".trellis/spec/workflow/semantic-retrieval.md"
    target_retrieval.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(retrieval, target_retrieval)
    package = fixture / ".trellis/guru-team/skills/packages" / INTAKE_SKILLS[-1]
    for name in ("interface.json", "evals/evals.json"):
        if (package / name).read_bytes() != (Path(request["package_root"]) / name).read_bytes():
            raise ValueError("Intake installed package differs from evaluated package")
    evidence = []
    for relative, content in facts["repository_files"].items():
        path = Path(relative)
        if path.is_absolute() or ".." in path.parts or path.parts[0] not in {"docs", "src", "tests"}:
            raise ValueError("Intake repository fixture path is invalid")
        target = fixture / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        evidence.append({"path": relative, "sha256": hashlib.sha256(content.encode()).hexdigest()})
    body_sha256 = hashlib.sha256(source["body"].encode()).hexdigest()
    live = {"repo": source["repo"], "number": source["number"], "url": source["url"],
            "state": source["state"], "updated_at": source["updated_at"], "body_sha256": body_sha256}
    public = {"source": source, "body_sha256": body_sha256, "open_duplicate_candidates": [],
              "source_facts_sha256": hashlib.sha256((json.dumps(live, ensure_ascii=False,
                  sort_keys=True, separators=(",", ":")) + "\n").encode()).hexdigest(),
              "repository_files": evidence, "required_reads": [row["path"] for row in evidence] + [".trellis/spec/workflow/semantic-retrieval.md"]}
    path = fixture / FACTS_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(public, indent=2) + "\n")
    run_git(fixture, "add", ".")
    run_git(fixture, "commit", "-q", "-m", "stage Intake source facts")
    head = run_git(fixture, "rev-parse", "HEAD")
    run_git(fixture, "update-ref", "refs/remotes/origin/main", head)
    run_git(fixture, "remote", "add", "origin", f"https://github.com/{source['repo']}.git")
    local_remote = execution_root / "source-remote.git"
    run_git(execution_root, "clone", "--bare", str(fixture), str(local_remote))
    binary = write_fake_gh(execution_root, "standard-intake", source, local_remote)
    return package, fixture / ".trellis/guru-team/scripts/bash/run-skill-command.sh", {
        "PATH": str(binary) + os.pathsep + os.environ["PATH"], "PYTHONDONTWRITEBYTECODE": "1",
    }


def command_arguments(skill: str, command: str, arguments: list[str]) -> None:
    if skill not in COMMANDS or command not in COMMANDS[skill]:
        raise ValueError("Intake command is not declared")
    # Validate optional production flags without changing the forwarded argv.
    transport_arguments = []
    index = 0
    while index < len(arguments):
        argument = arguments[index]
        if argument == "--json":
            index += 1
            continue
        if argument == "--root":
            if (skill == INTAKE_SKILLS[0] or skill == INTAKE_SKILLS[2] and command == "invoke"
                    or arguments[index + 1:index + 2] != ["."]):
                raise ValueError("Intake command does not support this root argument")
            index += 2
            continue
        transport_arguments.append(argument)
        index += 1
    arguments = transport_arguments
    if command == "preview-change-context-history":
        if len(arguments) != 2 or arguments[0] != "--query-json" or not isinstance(json.loads(arguments[1]), dict):
            raise ValueError("history preview requires one query JSON object")
        return
    expected = ["--invocation", "-"]
    if skill == INTAKE_SKILLS[2] and command != "invoke":
        expected = ["--input", "-"]
        if command.startswith("record-"):
            expected = ["--mode", "workflow", *expected]
    if arguments == expected:
        return
    if skill == INTAKE_SKILLS[3] and command.startswith("record-") and arguments == [*expected, "--scan-only"]:
        return
    raise ValueError("Intake command arguments differ from declared stdin transport")


def next_intake_owner(skill: str, output: dict[str, Any], interface: dict[str, Any]) -> str | None:
    consumer = next(row["consumer"] for row in interface["external_exits"] if row["id"] == output["exit_id"])
    target = consumer["id"]
    if target == "guru-requirements-clear-router":
        target = output["resume_target"]
    elif target == "guru-contract-wording-pass-router":
        target = INTAKE_SKILLS[4] if output["profile"] == "change_request" else None
    index = INTAKE_SKILLS.index(skill)
    following = INTAKE_SKILLS[index + 1] if index < 4 else None
    return target if target == following else None


class IntakeCommands:
    """Forward declared commands; bind receipts without choosing semantic exits."""

    def __init__(self, repository: Path, environment: dict[str, str], receipts_path: Path):
        self.repository = repository
        self.environment = environment
        self.receipts_path = receipts_path
        self.receipts: list[dict[str, Any]] = []
        self.outputs: dict[str, dict[str, Any]] = {}
        self.owner_index = 0
        self.completed: list[str] = []
        self.recorded: Any = None
        self.checked: Any = None
        self.terminal = False

    def record_response(self, payload: Any, result: dict[str, Any]) -> None:
        self.receipts.append({"request": payload, "response": result})
        self.receipts_path.write_text(json.dumps(self.receipts, separators=(",", ":")))

    def forward(self, payload: dict[str, Any]) -> dict[str, Any]:
        skill, command, arguments = payload["skill_id"], payload["command"], payload["arguments"]
        command_arguments(skill, command, arguments)
        if self.terminal or skill != INTAKE_SKILLS[self.owner_index]:
            raise ValueError("Intake command is after terminal output or out of owner order")
        envelope = json.loads(payload["stdin"]) if payload["stdin"] else {}
        step = "scan" if "--scan-only" in arguments else command
        required = list(COMMANDS[skill])
        if skill == INTAKE_SKILLS[3]:
            required.insert(0, "scan")
        expected = required[len(self.completed)]
        last = self.receipts[-1] if self.receipts else None
        if (step.startswith("record-") and step in required and last
                and (expected.startswith("check-") or expected == "invoke")
                and isinstance(last["request"], dict)
                and last["request"].get("skill_id") == skill
                and last["request"].get("command") == expected
                and last["response"]["returncode"] != 0):
            # Same-owner correction retires the old record/check results, while
            # keeping preview/scan evidence and the original failure receipt.
            self.completed = required[:required.index(step)]
            self.recorded, self.checked = None, None
        if step != required[len(self.completed)]:
            raise ValueError("Intake command is out of recorder/checker order")
        if command.startswith("check-") or command == "invoke" and self.owner_index:
            owner = envelope if skill == INTAKE_SKILLS[2] and command != "invoke" else envelope.get("owner_result")
            if owner != self.recorded:
                raise ValueError("Intake owner result does not equal actual recorder stdout")
        if command == "invoke":
            self.check_projection(skill, envelope)
            if self.checked and "validation_receipt" in self.checked:
                if envelope.get("validation_receipt") != self.checked["validation_receipt"]:
                    raise ValueError("Intake invocation does not use actual checker receipt")
        wrapper = self.repository / ".trellis/guru-team/skills/packages" / skill / "scripts" / f"{command}.sh"
        process = subprocess.run([str(wrapper), *arguments], cwd=self.repository,
            input=payload["stdin"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            env={**os.environ, **self.environment}, check=False)
        result = {"returncode": process.returncode, "stdout": process.stdout, "stderr": process.stderr}
        self.record_response(payload, result)
        if process.returncode:
            return result
        output = json.loads(process.stdout)
        self.completed.append(step)
        if command.startswith("record-") and step != "scan":
            self.recorded = output
        elif command.startswith("check-"):
            self.checked = output
        elif command == "invoke":
            self.outputs[skill] = output
            interface = json.loads((wrapper.parents[1] / "interface.json").read_text())
            self.terminal = next_intake_owner(skill, output, interface) is None
            if not self.terminal:
                self.owner_index += 1
                self.completed, self.recorded, self.checked = [], None, None
        return result

    def check_projection(self, skill: str, envelope: dict[str, Any]) -> None:
        index = INTAKE_SKILLS.index(skill)
        if not index:
            return
        previous = self.outputs[INTAKE_SKILLS[index - 1]]
        if envelope.get("transition") != previous.get("transition"):
            raise ValueError("Intake input transition differs from real producer stdout")
        public = envelope["public_input"]
        if public.get("source_exit") != previous["exit_id"]:
            raise ValueError("Intake source_exit differs from real producer stdout")
        if public.get("mode") != previous["transition"]["mode"]:
            raise ValueError("Intake mode differs from real producer stdout")
        continuation = previous.get("handoff_continuation_id", previous.get("continuation_id"))
        if public.get("continuation_id") != continuation:
            raise ValueError("Intake continuation differs from real producer stdout")
        if index >= 2:
            if public.get("target_locator") != previous["transition"]["target_locator"]:
                raise ValueError("Intake target projection differs from real producer stdout")
        if index == 2 and public.get("duplicate_snapshot") != previous.get("duplicate_snapshot"):
            raise ValueError("Intake duplicate snapshot differs from real producer stdout")


def validate_intake_trace(payload: dict[str, Any], protocol: dict[str, Any], public_stdout: str) -> list[str]:
    receipts = json.loads(Path(protocol["intake_receipts_path"]).read_text())
    commands = [event for event in payload["events"] if event["kind"] == "command"]
    if len(commands) != len(receipts) or not commands or payload["events"][-1] != commands[-1]:
        raise ValueError("Intake trace is missing command receipts or terminal invoke")
    reads: set[Path] = set()
    root = Path(protocol["projection_root"])
    repository = Path(protocol["repository_projection_root"])
    facts = json.loads((repository / FACTS_PATH).read_text())
    required_facts = {repository / FACTS_PATH, *(repository / path for path in facts["required_reads"])}
    allowed_reads = protocol["intake_read_paths"]
    required_facts.update(Path(path) for path in allowed_reads["case_file"])
    command_index = 0
    for event in payload["events"]:
        if event.get("request_sha256") != payload["request_sha256"]:
            raise ValueError("Intake trace event request mismatch")
        if event["kind"] == "read":
            path = Path(event["path"])
            if (str(path) not in allowed_reads.get(event["target_kind"], [])
                    or any(part in {"examples", "evals", ".runtime", ".git"} for part in path.parts)):
                raise ValueError("Intake trace read is outside public projection")
            if hashlib.sha256(path.read_bytes()).hexdigest() != event["sha256"]:
                raise ValueError("Intake trace read digest mismatch")
            reads.add(path)
            continue
        receipt = receipts[command_index]
        command_index += 1
        request, response = receipt["request"], receipt["response"]
        expected = {"kind": "command", "skill_id": request["skill_id"], "command": request["command"],
                    "arguments": request["arguments"], "stdin_sha256": hashlib.sha256(request["stdin"].encode()).hexdigest(),
                    "returncode": response["returncode"], "stdout_sha256": stdout_digest(response["stdout"]),
                    "stderr_sha256": hashlib.sha256(response["stderr"].encode()).hexdigest(),
                    "request_sha256": payload["request_sha256"]}
        if event != expected:
            raise ValueError("Intake trace command does not match actual execution receipt")
        package = root if request["skill_id"] == INTAKE_SKILLS[-1] else root / "flow-packages" / request["skill_id"]
        if not {package / "SKILL.md", package / "references/contract.md", package / "interface.json"}.issubset(reads):
            raise ValueError("Intake command preceded complete owner contract reads")
        if request["skill_id"] != INTAKE_SKILLS[0] and not required_facts.issubset(reads):
            raise ValueError("Intake command preceded required authority reads")
    last = receipts[-1]
    if last["request"]["command"] != "invoke" or stdout_digest(last["response"]["stdout"]) != stdout_digest(public_stdout):
        raise ValueError("Intake terminal stdout is not the actual wrapper output")
    if payload.get("terminal_skill_id") != last["request"]["skill_id"]:
        raise ValueError("Intake terminal producer identity mismatch")
    terminal = payload["terminal_skill_id"]
    package = root if terminal == INTAKE_SKILLS[-1] else root / "flow-packages" / terminal
    interface = json.loads((package / "interface.json").read_text())
    if next_intake_owner(terminal, json.loads(public_stdout), interface) is not None:
        raise ValueError("Intake trace stopped before the declared next owner")
    return ["public_invocation", "evals_not_loaded", "private_runtime_not_read"]
