"""One bounded installed Check candidate/final native case.

Reuse the original command relay and independent reviewer. This module only
supplies this case's facts, execution context and raw evidence transport.
"""
from __future__ import annotations

import json
from pathlib import Path

from adapters.eval.phase2_authoring import FACTS, PUBLIC_READS, write_json, public_reads
from adapters.eval.stage_result_authoring import ImplementationCommands as _StageCommands


def facts_locator(request: dict) -> str:
    return FACTS


def owner_schema(package: Path) -> str:
    return "schemas/phase2-check.schema.json"


def context(repository: Path, package: Path, helper_command: str, reads: list[str],
            input_locator: Path, *, facts_relative: str = FACTS) -> str:
    """Describe this bounded Check exercise without supplying its judgments."""
    from adapters.eval.implementation_authoring import EXECUTION_SURFACE
    return "\n".join([
        "Execute this bounded fixture autonomously through the installed guru-check-task and its original prerequisite/continuation owners. The fixture supplies source and complete unaccepted planning. No semantic prerequisite is supplied. Apply the installed workflow's autonomous plan-pause rule; material scope/design/risk choices retain their original stopping boundary.",
        f"Repository projection: {repository}. Original command paths are relative to the actual owner checkout.",
        f"Read the fact sheet: {helper_command} read --kind owner_file --path {repository / facts_relative}",
        *[f"{helper_command} read --kind owner_file --path {repository / path}" for path in reads],
        f"Read installed Skill: {helper_command} read --kind skill_contract --path {package / 'SKILL.md'}",
        f"Read current public entry facts: {helper_command} read --kind owner_file --path {input_locator}",
        "Before the first command, complete every required fact-sheet read. Read the installed workflow and each original owner contract/schema before executing it. Read the normal installed Check Recorder Authoring and its example; the host supplies no authoring form or current owner result.",
        "Execute helper reads and commands sequentially. Use the existing command transport: helper command --skill-id <original skill-id> --command <original command-id or invoke> --stdin -- <original argv>. Stdin is the original command stdin. The transport supplies no semantic result or route. For installed Delivery APIs use skill-id delivery-api. The helper inserts the selected subcommand once; arguments after -- contain only that subcommand's arguments.",
        f"Read actual Delivery API capabilities with {helper_command} command --skill-id delivery-api --command contract -- --json. Read top-level syntax with {helper_command} command --skill-id delivery-api --command=--help, and selected syntax with {helper_command} command --skill-id delivery-api --command <subcommand> -- --help before choosing its exact arguments. These execute the original delivery.py in the owner checkout.",
        f"For a forwarded Skill wrapper's help use {helper_command} command --skill-id <original skill-id> --command invoke -- --help. Read that installed Skill's commands.json for concrete command IDs, then pass that exact ID as --command. The --command=--help form belongs only to delivery-api. Virtual inspect/run/write have no CLI help. Architecture keeps its independent-review boundary below; read its public metadata rather than replacing the independent worker with a direct invocation.",
        "For original delivery-api operations, --input accepts a complete inline JSON object or a regular UTF-8 JSON file path. The original delivery.py does not read that operation from stdin and does not accept --input -. Prepare a normal operation file through run, then pass its path unchanged. The helper --stdin option only carries stdin to commands that actually support it.",
        "For each Delivery operation, read [trellis-runtime-contract] in the actual owner checkout's .trellis/workflow.md. Take owner_id from that declaration's owners[owner_role] and carry it unchanged. A Guru workflow coordinator or route name is a different identity. The delivery-api contract command reports API/schema versions, not the owner mapping.",
        "The Planning bodies are a fixture seed, not an accepted plan. Execute the original required Wording, independent Architecture planning assessment, Planning adequacy and Activation under their installed contracts. Consume actual public outputs; never generate a prerequisite pass yourself. This bounded exercise begins after Task/Delivery creation and ends at Check, without commit, publication, merge or whole-Task Completion.",
        "The fixture's architecture-input.json is an optional future phase2 blueprint. It is not a current Planning input or Planning freshness source. Construct each Planning assessment from the actual original Author candidate or exact selected design file, using Architecture's planning schema and references/contract.md Planning freshness definition.",
        "For candidate_assessment without design_locator, the original Architecture input.freshness_identity is sha256: plus the SHA256 hex digest of json.dumps(candidate, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8'), where candidate is your actual current design_facts/constraint_refs object from the original Author. With design_locator, bind the exact selected design.md file bytes instead. This is the existing public Planning input binding; it does not use the worktree token, phase2 blueprint freshness or Phase 2 private result identity. The existing run command can compute that binding from your actual input. No semantic judgment is supplied by that computation.",
        "Use implementation-authoring inspect to observe the complete current candidate, original content token, fixed base and public state. It makes no judgment. Use implementation-authoring run with stdin {argv:[executable,arguments...]} for deterministic commands and transient original-wrapper JSON files under .trellis/.runtime/guru-team/evals. Its returned stdout is raw process output. Use implementation-authoring write with {file_updates:{relative_path:complete_text}} only for fact-sheet writable evidence files.",
        "implementation-authoring inspect/run/write are virtual transport operations, not installed CLI commands. inspect takes empty stdin; run takes {argv:[nonempty executable string,argument strings...]}; write takes {file_updates:{relative_path:complete_text}}. Use --help only with an original CLI command. A transport request_error or original Delivery argument-parse error preserves its diagnostic and leaves the original pre-execution correction path open. It is not an executed owner result or a failed Check attempt.",
        "For independent Architecture use guru-maintain-architecture-baseline independent-review with stdin {public_input:<your original public input>,reads:[ordered repository-relative authority,candidate,consumer locators]}. The existing fresh worker executes its actual original wrapper. Supply no owner_result, expected decision or exit. Read order begins Constitution, Baseline and project change contract; exclude PRD, implement, task.json and their patch narratives from its blind-first input.",
        *EXECUTION_SURFACE,
        "independent-review is a blocking call that can take several minutes. If the shell returns a running session ID, poll that same session until it completes. Do not start another helper read or command while any helper request is pending. Do not launch a duplicate call; silence does not establish failure. This uses the original sequential transport and shell-session continuation.",
        "After real Planning/Activation, original implementation binds the complete candidate from the fixed development baseline and actual HEAD through begin-check. Complete original RDT task-impact/no-change and independent Architecture phase2 prerequisites. The candidate public token remains part of its original public input; consume it from the producer without changing it.",
        "Perform the complete candidate Check using the installed Skill. Execute its real record, check and invoke commands with the original arguments. The checker reads that same Task checkpoint; it takes no input file. Read the recorder's intermediate receipt and pass its artifact_path unchanged to the public invocation. Keep checker receipts distinct from the full owner result. The adapter does not assemble or correct authoring.",
        "Continue only through the original outcome's unique consumer. When candidate Check permits final integration, its existing Check rework returns to implementation. Apply the installed final-integration router to the actual preceding public owner outputs: Architecture reviewed_candidate and RDT candidate_ready require their respective original promotion at final_integration for the real changes; Architecture no_change and RDT ssot_current skip inapplicable promotion writes. Preserve any already applicable reviewed_promoted output under its original contract. Original implementation then rebuilds the actual candidate with the same fixed base and invokes begin-check, including the no-change path. Obtain matching final Architecture phase2 over that rebound content, then execute final Check as a separate first authoring stage. A real finding or blocked/re-entry result retains its own original consumer; do not force the success path.",
        "Each command input, original argv/stdin/stdout/stderr and output is preserved outside the repository. Any actual recorder/checker/wrapper failure ends this sample; do not retry that failed owner, repair its submitted assembly, delete fields, replace a token or synthesize a DTO. Pre-execution transport request and Delivery syntax errors retain the correction boundary above. Failing business validation is review evidence and remains available to the Check owner.",
        "Original consumers retire their consumed transient inputs. Already retired files need no additional cleanup request. Complete any other applicable cleanup before the terminal wrapper, while keeping the inputs that wrapper still needs. Their original bytes remain in the external command evidence. Keep original owner checkpoints and every failed observation intact.",
        "Only the final original semantic wrapper call uses eval-only stdin {final:true,invocation:<its original stdin object>}. It must be the last helper request. For filename invocation, supply its original --input/--owner-result file arguments and use invocation:{} for unused stdin. After it completes, return only its actual stdout; send no further helper read, command or cleanup request. Earlier public results stay separate evidence.",
    ])


class ImplementationCommands(_StageCommands):
    def __init__(self, repository, environment, receipts_path, *, facts_relative=FACTS):
        super().__init__(repository, environment, receipts_path, facts_relative=facts_relative)

    def forward(self, payload):
        skill, command = payload["skill_id"], payload["command"]
        if (not self.terminal and skill in self.owners and command != "invoke"
                and not (skill == "guru-maintain-architecture-baseline" and command == "independent-review")):
            package = self.repository / ".trellis/guru-team/skills/packages" / skill
            declared = {row["id"] for row in json.loads((package / "commands.json").read_text())["commands"]}
            if command not in declared:
                response = {"returncode": 0, "stdout": json.dumps({
                    "request_error": "implementation command is not declared by its original owner",
                    "returncode": 2, "stdout": "",
                    "stderr": "Read the installed commands.json for concrete IDs; use invoke with --help for forwarded wrapper help.",
                }) + "\n", "stderr": ""}
                self.record_response(payload, response)
                return response
        if payload["skill_id"] == "implementation-authoring" and payload["command"] == "inspect":
            if self.terminal:
                raise ValueError("command follows the terminal original wrapper")
            from adapters.eval.fixture_io import run_git
            from adapters.eval.owner_runtime import load_package_runtime_module
            from adapters.eval.eval_support import qualification_planning_identity
            from runtime.delivery_projection.adapter import DeliveryProjection
            from runtime.reviewed_content import reviewed_content_identity, reviewed_content_metadata_path
            facts = json.loads((self.repository / self.facts_relative).read_text())
            projection = DeliveryProjection(self.repository, facts["task_ref"])
            base = projection.content_base(facts["delivery_key"], development_base=facts["initial_head"])
            head = run_git(self.repository, "rev-parse", "HEAD")
            common = load_package_runtime_module(
                self.repository / ".trellis/guru-team/scripts/bash/run-skill-command.sh",
                "guru-check-task", "common")
            paths = sorted({path for path in [
                *run_git(self.repository, "diff", "--name-only", base, head).splitlines(),
                *common.dirty_paths(self.repository),
            ] if not reviewed_content_metadata_path(path)})
            public = {"current_head": head, "fixed_base": base, "reviewed_paths": paths,
                "candidate": projection.candidate(paths, head_ref=head, base_ref=base),
                "architecture_candidate": {"head": head,
                    "content_identity": "sha256:" + reviewed_content_identity(self.repository)["sha256"]},
                "current_delivery": projection.resolve(facts["delivery_key"]),
                "current_selection": projection.current(facts["delivery_key"]),
                "diff": run_git(self.repository, "diff", base),
                "qualification_target": {**facts["qualification_target"], "checkout_head": head,
                    "planning_identity": qualification_planning_identity(self.repository, [
                        facts["task_ref"] + "/" + facts["planning_root"] + "/" + name
                        for name in ("prd.md", "design.md", "implement.md")])}}
            response = {"returncode": 0, "stdout": json.dumps(public) + "\n", "stderr": ""}
            self.record_response(payload, response)
            return response
        # Preserve call-local authoring before its original consumer retires it.
        # Inputs are never changed or filled by this transport.
        inputs = {}
        for flag in ("--input", "--owner-result", "--semantic-result", "--invocation"):
            path = self._file_argument(payload["arguments"], flag)
            if path is not None and path.is_file():
                inputs[flag] = {"path": str(path), "text": path.read_text()}
        response = super().forward(payload)
        self.receipts[-1]["input_files"] = inputs
        write_json(self.receipts_path, self.receipts)
        # The parent owns virtual request and Delivery parse-error handling.
        # A nonzero original owner command also closes this first-attempt case,
        # including intermediate record/check commands the parent leaves open.
        if payload["skill_id"] not in {"implementation-authoring", "delivery-api"} and response["returncode"]:
            self.terminal = True
        return response


def additional_mutated_paths(repository: Path, facts: dict) -> list[str]:
    """Account only for actual results written by the selected original owners."""
    from runtime.delivery_projection.adapter import DeliveryProjection
    record = DeliveryProjection(repository, facts["task_ref"]).read_record()
    roots = [repository / facts["task_ref"]]
    roots.extend(repository / ".trellis/.runtime/guru-team/owner-checkpoints" / name
                 for name in {record["id"], Path(facts["task_ref"]).name})
    return [path.relative_to(repository).as_posix() for root in roots if root.is_dir()
            for path in root.rglob("*") if path.is_file()]


def validate_trace(payload: dict, protocol: dict, public_stdout: str) -> list[str]:
    from adapters.eval.implementation_authoring import validate_trace as validate_commands
    invariants = validate_commands(payload, protocol, public_stdout)
    receipts = json.loads(Path(protocol["implementation_receipts_path"]).read_text())
    check_stage_sequence(receipts, json.loads(public_stdout))
    return invariants


def public_command_input(receipt: dict) -> dict:
    """Read the actual original input preserved before its consumer retired it."""
    request = receipt["request"]
    stdin = json.loads(request["stdin"]) if request.get("stdin", "").strip() else {}
    if isinstance(stdin, dict) and "final" in stdin and "invocation" in stdin:
        stdin = stdin["invocation"]
    if isinstance(stdin, dict) and isinstance(stdin.get("public_input"), dict):
        return stdin["public_input"]
    arguments = request["arguments"]
    for flag in ("--input", "--invocation"):
        if flag not in arguments:
            continue
        value = arguments[arguments.index(flag) + 1]
        if value == "-":
            supplied = stdin
        elif flag in receipt.get("input_files", {}):
            supplied = json.loads(receipt["input_files"][flag]["text"])
        else:
            supplied = json.loads(value)
        return supplied.get("public_input", supplied)
    return {}


def check_stage_sequence(receipts: list[dict], terminal: dict) -> None:
    """Compare observed stage operations outside model input; infer no judgment."""
    calls = []
    for index, receipt in enumerate(receipts):
        request, response = receipt["request"], receipt["response"]
        if request["skill_id"] in {"implementation-authoring", "delivery-api"}:
            continue
        if request["command"] not in {"invoke", "independent-review", "invoke-" + request["skill_id"]}:
            continue
        if response["returncode"]:
            raise ValueError("native sample retains a failed original semantic invocation")
        if "--help" in request["arguments"]:
            continue
        output = json.loads(response["stdout"])
        if "request_error" not in output:
            calls.append((index, request["skill_id"], public_command_input(receipt), output))
    checks = [row for row in calls if row[1] == "guru-check-task"]
    if not checks:
        raise ValueError("native sample has no original Check invocation")
    first = checks[0][0]
    preceding = [row for row in calls if row[0] < first]
    for skill in ("guru-approve-task-plan", "guru-activate-delivery",
                  "guru-maintain-requirements-design-test-ssot", "guru-maintain-architecture-baseline"):
        if not any(row[1] == skill for row in preceding):
            raise ValueError("native sample did not execute required original owner: " + skill)
    for stage in ("planning", "phase2"):
        if not any(row[1] == "guru-maintain-architecture-baseline" and row[2].get("stage") == stage
                   for row in preceding):
            raise ValueError("native sample lacks actual independent Architecture " + stage)
    if not any(row[1] == "guru-maintain-architecture-baseline"
               and row[2].get("planning_purpose") == "final_plan" for row in preceding):
        raise ValueError("native sample lacks original Architecture final_plan")
    if not any(row[1] == "guru-maintain-requirements-design-test-ssot"
               and row[2].get("stage") == "phase2" for row in preceding):
        raise ValueError("native sample lacks original RDT phase2")
    if terminal.get("exit_id") != "passed":
        # Findings/blocked/re-entry remain their actual outcomes. The eval's
        # external expectation and semantic grader assess their applicability.
        return
    if (len(checks) != 2 or checks[0][2].get("profile") != "delivery_candidate_check"
            or checks[0][3].get("exit_id") != "candidate_checked"
            or checks[1][2].get("profile") != "delivery_initial_check"
            or checks[1][3].get("exit_id") != "passed"):
        raise ValueError("native sample did not execute separate first candidate and final Checks")
    between = [row for row in calls if checks[0][0] < row[0] < checks[1][0]]
    architecture = [row for row in preceding if row[1] == "guru-maintain-architecture-baseline"
                    and row[2].get("stage") == "phase2"][-1][3]
    rdt = [row for row in preceding if row[1] == "guru-maintain-requirements-design-test-ssot"
           and row[2].get("stage") == "phase2"][-1][3]
    required_promotions = []
    if architecture.get("promotion_state") == "reviewed_candidate":
        required_promotions.append(("guru-maintain-architecture-baseline", "baseline_current"))
    elif architecture.get("promotion_state") not in {"no_change", "reviewed_promoted"}:
        raise ValueError("native sample lacks an applicable candidate Architecture result")
    if rdt.get("exit_id") == "candidate_ready":
        required_promotions.append(("guru-maintain-requirements-design-test-ssot", "ssot_current"))
    elif rdt.get("exit_id") != "ssot_current":
        raise ValueError("native sample lacks an applicable candidate RDT result")
    promotion_indexes = []
    for skill, exit_id in required_promotions:
        promoted = [row for row in between if row[1] == skill and row[2].get("stage") == "final_integration"
                    and row[3].get("exit_id") == exit_id
                    and (skill != "guru-maintain-architecture-baseline"
                         or row[3].get("promotion_state") == "reviewed_promoted")]
        if not promoted:
            raise ValueError("native sample lacks required original promotion: " + skill)
        promotion_indexes.append(promoted[-1][0])
    rebound = []
    for index, receipt in enumerate(receipts):
        request = receipt["request"]
        if (checks[0][0] < index < checks[1][0] and request["skill_id"] == "delivery-api"
                and request["command"] in {"begin-check", "apply"}
                and not any(flag in request["arguments"] for flag in ("--help", "--dry-run"))
                and receipt["response"]["returncode"] == 0):
            operation = public_command_input(receipt)
            if operation.get("operation") == "begin_check":
                rebound.append((index, operation))
    if not rebound:
        raise ValueError("native sample lacks actual implementation candidate rebinding")
    rebound_index, operation = rebound[-1]
    if any(index > rebound_index for index in promotion_indexes):
        raise ValueError("native sample did not rebind after its required promotions")
    final_architecture = [row for row in between if row[1] == "guru-maintain-architecture-baseline"
                          and row[2].get("stage") == "phase2" and row[0] > rebound_index]
    if (not final_architecture or final_architecture[-1][3].get("exit_id") != "baseline_current"
            or final_architecture[-1][3].get("promotion_state") not in {"no_change", "reviewed_promoted"}
            or final_architecture[-1][2].get("candidate", {}).get("head")
            != operation.get("candidate", {}).get("head_ref")):
        raise ValueError("native sample lacks matching final Architecture after rebinding")
    for command in ("record-phase2-check", "check-phase2-check"):
        rows = [row for row in receipts if row["request"]["skill_id"] == "guru-check-task"
                and row["request"]["command"] == command
                and not any(flag in row["request"]["arguments"] for flag in ("--help", "--dry-run"))]
        if len(rows) != 2 or any(row["response"]["returncode"] for row in rows):
            raise ValueError("native sample did not preserve first successful " + command + " at both stages")
