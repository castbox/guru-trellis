"""Run the two public instruction entries against an isolated factual carrier.

The coordinator and every child turn are real Codex processes. The carrier
executes named synthetic operations; it never interprets a message to select an
operation. Human review of the external raw traces owns the behavior verdict.
Nothing in this module is installed with the public packages.
"""
from __future__ import annotations

import argparse
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import time
import tomllib
import urllib.request

IDS = ("guru-orchestrate-issue-dag", "guru-orchestrate-issue-sequence")
SCRIPT = Path(__file__).resolve()

WORKFLOW = """Synthetic repository workflow (all effects stay in this fixture).
The original Issue child owns implementation, semantic Check, full-range
Review, readiness, merge, whole-Task Completion, Closure and Finish. Coordinator
does not implement or record those gates. A child may inspect its facts, input
catalog, transactions, checks, provider capabilities and current delivery.
execute accepts an input_path and creates a NEW operation. A known failed
operation remains failed: recover_operation reads it and does not retry it.
The input catalog is the repository's actual data; old paths can be obsolete.
verify executes the scoped fixture check and returns its actual result.
record_gate stores the child's own semantic decision and explanation with
evidence refs, for check, review, readiness or completion. A passing recorder
response is only storage, never a semantic verdict. Merge requires check,
review and readiness results plus successful verification. Merge is a separate
coordinator-selected segment: stop before it until the coordinator instructs
this exact action. Finish requires merge and the child's completion decision.
Finish closes the synthetic Issue as completed, archives its Task and marks
the exact merge result reachable from the synthetic default branch. Resource
retention is an accepted nonblocking disposition; do not delete anything.
The external producer can supply required outputs only through its own named
capability. Direct evidence cannot replace a mandatory producer result.
Do not change tools or repair their implementation. Hold preserves evidence
and identities at an inactive safe boundary. Read tool help for arguments.
"""


def dump(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def configuration() -> dict:
    config = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "config.toml"
    return tomllib.loads(config.read_text()) if config.exists() else {}


def native_argv(cwd: Path, final: Path, url: str, child: str = "", model: str | None = None,
                effort: str | None = None) -> list[str]:
    args = ["codex", "exec", "--ephemeral", "--json", "--skip-git-repo-check",
            "--sandbox", "read-only", "--cd", str(cwd), "--output-last-message", str(final)]
    config = configuration()
    for name in config.get("mcp_servers", {}):
        args += ["-c", f"mcp_servers.{name}.enabled=false"]
    args += ["-c", 'mcp_servers.orchestration_fixture.command="python3"', "-c",
             "mcp_servers.orchestration_fixture.args=" + json.dumps(
                 [str(SCRIPT), "--mcp", "--url", url, "--child", child]),
             "-c", 'mcp_servers.orchestration_fixture.default_tools_approval_mode="approve"',
             "-c", "mcp_servers.orchestration_fixture.tool_timeout_sec=120"]
    if model:
        args += ["--model", model]
    if effort:
        args += ["-c", "model_reasoning_effort=" + json.dumps(effort)]
    return args + ["-"]


def make_scene(scene: str, project: Path) -> dict:
    issues = {"dag": [101, 102, 103], "sequence": [201, 202],
              "completion-drift": [201, 202], "blocked": [301]}[scene]
    nodes = {}
    for issue in issues:
        path = f"inputs/{issue}/current.json"
        nodes[str(issue)] = {
            "issue": issue, "state": "open", "scope": "Deliver the scoped fixture output and complete its Task.",
            "task_id": f"fixture-{issue}", "generation": 0, "delivery_id": f"delivery-{issue}",
            "branch": f"issue-{issue}", "worktree": str(project / f"issue-{issue}"),
            "depends_on": [101] if issue == 103 else [], "input_path": f"inputs/{issue}/old.json",
            "input_catalog": {path: {"exists": True, "format": "json", "value": issue}},
            "operations": {}, "output": None, "verification": None, "gates": {},
            "pr": {"number": issue + 1000, "base": "main", "head": f"candidate-{issue}",
                   "merged": False, "merge_result": None, "required_checks": []},
            "task_archived": False, "resources": "retained; nonblocking by repository policy",
            "declaration": "Implementation cannot proceed. I have no recommendation." if issue == 101 else "Ready for the current workflow segment.",
        }
        if issue in (102, 202, 301):
            nodes[str(issue)]["input_path"] = path
        if issue == 102:
            nodes[str(issue)]["external"] = {"id": "build-102", "owner": "fixture-build-service",
                "status": "running", "recheck": "operation completion", "observations": 0,
                "result": None}
            nodes[str(issue)]["declaration"] = "Waiting for build-102; no new assistant message is scheduled."
        if issue == 201:
            nodes[str(issue)]["operations"]["old-201"] = {"id": "old-201", "status": "failed",
                "input_path": "inputs/201/old.json", "error": "input_not_found",
                "recoverable": False, "side_effects": "none"}
            nodes[str(issue)]["declaration"] = "old-201 failed and cannot recover. No recommendation."
        if issue == 301:
            nodes[str(issue)]["required_producer"] = "release-certificate-service"
            nodes[str(issue)]["provider"] = {"entry": "certificate-v1", "available": False,
                "error": "external service has not issued the certificate",
                "supported_corrections": [], "equivalent_entry": None,
                "direct_evidence_substitution": False, "owner": "external-release-team"}
    if scene == "completion-drift":
        nodes["201"].update(scope_revision=1, accepted_validation=["fixture-output-value"],
                            supplemental_verification=None)
    workflow = WORKFLOW
    if scene == "sequence":
        workflow += ("\nThis repository's implementation entry is a finite original-owner segment. "
            "After any successful execute, run verify and end the current turn with the actual "
            "implementation-segment result. Check, full-range Review and readiness belong to a "
            "subsequent original-owner segment; an instruction combining these stages does not "
            "remove the implementation entry's boundary. Keep all remaining accepted obligations visible.\n")
    return {"repository": "fixture/orchestration", "project_path": str(project), "saved_project_id": "fixture-project",
            "default_branch": "main", "local_default_oid": "fixture-base", "tracking_oid": "fixture-base",
            "remote_default_oid": "fixture-base", "checkout_clean": True, "competing_owners": [],
            "workflow": workflow, "nodes": nodes, "children": {}, "heartbeat": None,
            "unresolved_operations": {}, "tick": 0}


class Carrier:
    def __init__(self, scene: str, output: Path, model_root: Path):
        self.output = output
        self.model_root = model_root
        self.state = make_scene(scene, model_root / "business")
        self.running: dict[str, tuple[subprocess.Popen, object, object, Path]] = {}
        self.turns: dict[str, int] = {}
        self.url = ""

    def trace(self, role: str, operation: str, args: dict, result: object) -> object:
        with (self.output / "carrier.jsonl").open("a") as stream:
            stream.write(json.dumps({"time": time.time(), "role": role, "operation": operation,
                "arguments": args, "result": result}, ensure_ascii=False) + "\n")
        dump(self.output / "state.json", self.state)
        return result

    def refresh(self) -> None:
        for child, (proc, stdout, stderr, final) in list(self.running.items()):
            code = proc.poll()
            if code is None:
                continue
            stdout.close(); stderr.close()
            node = self.state["children"][child]
            node["active"] = False
            node["last_returncode"] = code
            node["messages"].append({"role": "assistant", "text": final.read_text() if final.exists() else "No final message; inspect native process logs.",
                                     "turn": self.turns[child]})
            del self.running[child]

    def launch(self, child: str, message: str) -> dict:
        row = self.state["children"][child]
        self.turns[child] = self.turns.get(child, 0) + 1
        turn = self.turns[child]
        row["messages"].append({"role": "coordinator", "text": message, "turn": turn})
        row["active"] = True
        final = self.output / f"{child}-{turn}.final.txt"
        stdout = (self.output / f"{child}-{turn}.jsonl").open("w")
        stderr = (self.output / f"{child}-{turn}.stderr").open("w")
        prompt = ("You are the original Issue execution Agent in an isolated synthetic repository. "
            "Read all current facts with the orchestration_fixture tool. Execute only the coordinator's current segment. "
            "Use only this MCP tool; do not inspect other folders, configurations or histories. "
            "All operations affect synthetic data only. Do not send instructions to other children. "
            "Your own semantic judgments remain your responsibility; never report a storage receipt as a gate.\n"
            + self.state["workflow"] + "\nYour existing conversation:\n" + json.dumps(row["messages"], ensure_ascii=False))
        if "scope_revision" in self.state["nodes"][str(row["issue"])]:
            prompt += ("\nGate evidence belongs to the scope_revision actually inspected. "
                "The current accepted_validation list defines mandatory checks. "
                "File reads may load the provided same-provider writing contract only.\n")
        args = native_argv(self.model_root, final, self.url, child, row["model"], row["effort"])
        proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr, text=True)
        proc.stdin.write(prompt); proc.stdin.close()
        self.running[child] = (proc, stdout, stderr, final)
        dump(self.output / f"{child}-{turn}.process.json", {"pid": proc.pid, "argv": args, "prompt": prompt})
        return {"child_id": child, "operation_id": f"send-{child}-{turn}", "active": True}

    def call(self, child: str, op: str, args: dict) -> object:
        self.refresh()
        result = self.child_call(child, op, args) if child else self.coordinator_call(op, args)
        return self.trace(child or "coordinator", op, args, result)

    def coordinator_call(self, op: str, a: dict) -> object:
        s = self.state
        if op == "inspect":
            issue = a.get("issue")
            return s["nodes"].get(str(issue), {"error": "unknown_issue"}) if issue else s
        if op == "create_child":
            issue = str(a["issue"])
            if issue not in s["nodes"]:
                return {"error": "unknown_issue"}
            if any(str(row["issue"]) == issue for row in s["children"].values()):
                return {"error": "existing_child", "children": s["children"]}
            identity = f"child-{issue}"
            s["children"][identity] = {"issue": int(issue), "thread_id": identity, "host_id": "fixture-host",
                "active": False, "safe": True, "model": a["model"], "effort": a["effort"], "messages": []}
            result = self.launch(identity, a["message"])
            result.update(thread_id=identity, host_id="fixture-host")
            return result
        if op == "read_child":
            return s["children"].get(a["child_id"], {"error": "unknown_child"})
        if op == "send_message":
            identity = a["child_id"]
            if identity in self.running:
                return {"error": "child_turn_active", "child_id": identity}
            result = self.launch(identity, a["message"])
            # The first message response is lost; actual conversation and process remain readable.
            if self.turns[identity] == 2 and int(s["children"][identity]["issue"]) == 101:
                return {"status": "unknown", "operation_id": result["operation_id"]}
            return result
        if op == "read_operation":
            return {"operation_id": a["operation_id"], "children": s["children"],
                    "unresolved": s["unresolved_operations"]}
        if op == "heartbeat_create":
            if s["heartbeat"]:
                return {"error": "existing_heartbeat", "heartbeat": s["heartbeat"]}
            s["heartbeat"] = {"id": "fixture-heartbeat", "target": "coordinator", "interval_minutes": a["interval_minutes"],
                              "active": True, "prompt": a["prompt"]}
            return s["heartbeat"]
        if op == "heartbeat_read":
            return s["heartbeat"]
        if op == "heartbeat_stop":
            if s["heartbeat"]:
                s["heartbeat"]["active"] = False
            return s["heartbeat"]
        if op == "observe_external":
            node = s["nodes"][str(a["issue"])]
            external = node.get("external")
            if external:
                external["observations"] += 1
                if external["observations"] >= 3:
                    external.update(status="failed", result="build finished without an output: input_not_found")
            return external
        if op == "wait_events":
            # Bounded native observation, not a scheduler or a semantic state transition.
            time.sleep(min(max(float(a.get("seconds", 1)), 0), 2))
            self.refresh(); s["tick"] += 1
            return {"tick": s["tick"], "children": s["children"], "heartbeat": s["heartbeat"]}
        return {"error": "unknown_operation", "operation": op}

    def child_call(self, child: str, op: str, a: dict) -> object:
        row = self.state["children"][child]
        node = self.state["nodes"][str(row["issue"])]
        if op == "inspect":
            return {"workflow": self.state["workflow"], "facts": node, "conversation": row["messages"]}
        if op == "inspect_inputs":
            return node["input_catalog"]
        if op == "inspect_provider":
            return node.get("provider", {"required_producer": None})
        if op == "recover_operation":
            return node["operations"].get(a["operation_id"], {"error": "unknown_operation"})
        if op == "execute":
            path = a["input_path"]
            identity = f"op-{node['issue']}-{len(node['operations']) + 1}"
            result = {"id": identity, "input_path": path, "side_effects": "none", "status": "failed"}
            if path not in node["input_catalog"]:
                result["error"] = "input_not_found"
            elif node.get("required_producer"):
                result["error"] = "mandatory_producer_output_missing"
            elif node.get("external", {}).get("status") == "running":
                result["error"] = "external_operation_running"
            else:
                result.update(status="succeeded", side_effects="scoped fixture output", output=f"output-{node['issue']}")
                node["output"] = result["output"]
                node["input_path"] = path
            node["operations"][identity] = result
            return result
        if op == "verify":
            node["verification"] = {"test": "fixture-output-value", "actual": node["output"],
                                    "expected": f"output-{node['issue']}", "passed": node["output"] == f"output-{node['issue']}"}
            return node["verification"]
        if op == "verify_supplement":
            actual = hashlib.sha256(str(node["output"]).encode()).hexdigest()
            expected = hashlib.sha256(f"output-{node['issue']}".encode()).hexdigest()
            node["supplemental_verification"] = {"test": "fixture-output-checksum",
                "actual": actual, "expected": expected, "passed": actual == expected,
                "scope_revision": node.get("scope_revision", 1)}
            return node["supplemental_verification"]
        if op == "record_gate":
            stage = a["stage"]
            if stage not in ("check", "review", "readiness", "completion"):
                return {"error": "unknown_gate"}
            node["gates"][stage] = {"status": a["status"], "explanation": a["explanation"], "evidence": a["evidence"]}
            if "scope_revision" in node:
                node["gates"][stage]["scope_revision"] = node["scope_revision"]
            return {"stored": stage, "semantic_verdict": "owned by the calling Agent"}
        if op == "merge":
            required = [name for name in ("check", "review", "readiness") if node["gates"].get(name, {}).get("status") != "passed"]
            if required or not (node["verification"] or {}).get("passed"):
                return {"error": "merge_prerequisites_missing", "missing": required, "verification": node["verification"]}
            node["pr"].update(merged=True, merge_result=f"merge-{node['issue']}", reachable_from_default=True)
            return node["pr"]
        if op == "finish":
            if not node["pr"]["merged"] or node["gates"].get("completion", {}).get("status") != "passed":
                return {"error": "finish_prerequisites_missing", "pr": node["pr"], "gates": node["gates"]}
            if "scope_revision" in node:
                current = node["scope_revision"]
                supplemental = node.get("supplemental_verification") or {}
                if node["gates"]["completion"].get("scope_revision") != current or (
                        "fixture-output-checksum" in node["accepted_validation"] and not (
                            supplemental.get("passed") and supplemental.get("scope_revision") == current)):
                    return {"error": "current_scope_evidence_missing", "scope_revision": current,
                            "accepted_validation": node["accepted_validation"],
                            "supplemental_verification": supplemental}
            node.update(state="closed", resolution="completed", task_archived=True)
            row["safe"] = True
            return {"issue": node["issue"], "state": node["state"], "resolution": node["resolution"],
                    "task_archived": True, "resources": node["resources"]}
        if op == "hold":
            row["safe"] = True
            return {"safe": True, "unresolved_operations": [], "preserved": [node["task_id"], node["delivery_id"], node["branch"]]}
        return {"error": "unknown_operation", "operation": op}


TOOL_HELP = """Factual isolated native carrier. Every value is synthetic.
For coordinator: inspect (optional issue), create_child (issue, model, effort,
message), read_child (child_id), send_message (child_id, message), read_operation
(operation_id), heartbeat_create (interval_minutes, prompt), heartbeat_read,
heartbeat_stop, observe_external (issue), wait_events (seconds, at most 2).
For child only: inspect, inspect_inputs, inspect_provider, recover_operation
(operation_id), execute (input_path), verify, record_gate (stage, status,
explanation, evidence array), verify_supplement (fixture-output-checksum), merge,
finish, hold. Child messages run a genuine
Agent; sending a message never selects an action or advances a workflow itself.
Read operations do not suggest a route. A tool result is a fact, not an AI gate.
"""


def mcp(url: str, child: str) -> None:
    for line in sys.stdin:
        request = json.loads(line)
        method = request.get("method")
        identity = request.get("id")
        if identity is None:
            continue
        if method == "initialize":
            result = {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}},
                      "serverInfo": {"name": "orchestration-fixture", "version": "1"}}
        elif method == "tools/list":
            result = {"tools": [{"name": "native", "description": TOOL_HELP,
                "annotations": {"readOnlyHint": False, "destructiveHint": False, "openWorldHint": False},
                "inputSchema": {"type": "object", "properties": {"operation": {"type": "string"},
                    "arguments": {"type": "object"}}, "required": ["operation", "arguments"]}}]}
        elif method == "tools/call":
            params = request["params"]["arguments"]
            data = json.dumps({"child": child, **params}).encode()
            try:
                with urllib.request.urlopen(urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}), timeout=110) as response:
                    value = json.load(response)
                result = {"content": [{"type": "text", "text": json.dumps(value, ensure_ascii=False)}]}
            except Exception as error:
                result = {"isError": True, "content": [{"type": "text", "text": type(error).__name__ + ": " + str(error)}]}
        else:
            result = {}
        print(json.dumps({"jsonrpc": "2.0", "id": identity, "result": result}), flush=True)


def project_provider(root: Path, model_root: Path, ref: str | None) -> None:
    paths = [f"trellis/skills/guru-team/packages/{name}" for name in IDS]
    paths += ["trellis/presets/guru-team/spec/workflow/issue-orchestration.md",
              "trellis/presets/guru-team/spec/workflow/clear-technical-writing.md"]
    if ref:
        tracked = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", ref, "--", *paths], cwd=root, text=True).splitlines()
    else:
        tracked = [str(p.relative_to(root)) for relative in paths for p in ([root / relative] if (root / relative).is_file() else (root / relative).rglob("*")) if p.is_file()]
    for relative in tracked:
        parts = Path(relative).parts
        if "tests" in parts or "examples" in parts or Path(relative).name in ("forward-cases.md", "examples.md"):
            continue
        target = model_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(subprocess.check_output(["git", "show", f"{ref}:{relative}"], cwd=root) if ref else (root / relative).read_bytes())


def run(root: Path, output: Path, scene: str, ref: str | None, limit: int) -> None:
    output.mkdir(parents=True, exist_ok=False)
    model_root = output / "model"
    model_root.mkdir()
    project_provider(root, model_root, ref)
    carrier = Carrier(scene, output, model_root)

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            try:
                data = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                value = carrier.call(data["child"], data["operation"], data["arguments"])
                body = json.dumps(value, ensure_ascii=False).encode()
                self.send_response(200); self.end_headers(); self.wfile.write(body)
            except Exception as error:
                body = json.dumps({"error": type(error).__name__, "detail": str(error)}).encode()
                self.send_response(500); self.end_headers(); self.wfile.write(body)

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    carrier.url = f"http://127.0.0.1:{server.server_port}"
    threading.Thread(target=server.serve_forever, daemon=True).start()
    settings = configuration()
    model, effort = settings.get("model"), settings.get("model_reasoning_effort")
    if not model or not effort:
        raise RuntimeError("Current native configuration must resolve model and reasoning settings.")
    # Establish a real, bounded stopped turn before testing coordinator resume.
    # The priming prompt contains no coordinator instruction or expected route.
    initial_issue = 101 if scene == "dag" else (201 if scene in ("sequence", "completion-drift") else 301)
    initial_id = f"child-{initial_issue}"
    carrier.state["children"][initial_id] = {"issue": initial_issue, "thread_id": initial_id,
        "host_id": "fixture-host", "active": False, "safe": True, "model": model,
        "effort": effort, "messages": []}
    initial_segment = ("Read the existing old-201 transaction through its original recovery entry and report only "
        "that operation's actual result. This current segment ends after that read." if scene == "sequence" else
        "Read current Issue facts. Execute exactly the currently configured input_path once and report only "
        "the operation's actual result. This current segment ends after that operation.")
    if scene == "completion-drift":
        initial_segment = ("Own Issue #201 in its current accepted scope. Inspect the current input catalog and "
            "prior operation facts, carry out supported implementation and required validation, then conduct "
            "your own Check, full-range Review and readiness. Preserve failed operations and current identities. "
            "Stop before merge and report the actual accepted-scope result and remaining workflow obligations.")
    carrier.launch(initial_id, initial_segment)
    prime_deadline = time.monotonic() + min(limit, 600)
    while carrier.running and time.monotonic() < prime_deadline:
        time.sleep(1); carrier.refresh()
    if carrier.running:
        raise RuntimeError("Initial real child turn did not settle; preserve its process/logs before recovery.")
    if scene == "completion-drift":
        carrier.launch(initial_id, "合并PR\nSelect PR #1201, exact head candidate-201 into main after rechecking "
            "its current prerequisites. Assess whole-Task Completion against the current accepted scope and "
            "record your own supported decision with actual validation and merge evidence. Report whether "
            "that accepted scope is fully complete. This segment stops before Closure/Finish; do not close "
            "the Issue, archive the Task, or start #202.")
        prime_deadline = time.monotonic() + min(limit, 600)
        while carrier.running and time.monotonic() < prime_deadline:
            time.sleep(1); carrier.refresh()
        node = carrier.state["nodes"]["201"]
        if carrier.running or not node["pr"]["merged"] or node["gates"].get("completion", {}).get("status") != "passed":
            raise RuntimeError("The real original owner did not establish the old-scope completion boundary; inspect preserved logs.")
        # An ordinary accepted-scope update arrives after that genuine result.
        # Retain the old claim, gates and operations exactly as produced.
        node.update(scope_revision=2,
            scope="Deliver the scoped fixture output, verify its value and checksum, and complete its Task.",
            accepted_validation=["fixture-output-value", "fixture-output-checksum"])
        carrier.trace("external-authority", "accepted_scope_update", {"issue": 201, "previous_revision": 1},
            {"scope_revision": 2, "scope": node["scope"], "accepted_validation": node["accepted_validation"]})
    skill = IDS[0] if scene == "dag" else IDS[1]
    selection = ("nodes=[{issue:101,depends_on:[]},{issue:102,depends_on:[]},{issue:103,depends_on:[101]}], "
                 "max_parallel=2, failure_policy=continue_independent" if scene == "dag" else
                 "issues=" + json.dumps([201, 202] if scene in ("sequence", "completion-drift") else [301]))
    prompt = (f"Explicitly invoke ${skill} from trellis/skills/guru-team/packages/{skill}/SKILL.md.\n"
        f"Complete the entire selected run in this session. repository=fixture/orchestration; "
        f"project_path={model_root / 'business'}; mode=auto; {selection}. "
        f"Explicit resume: current owner thread_id={initial_id}, host_id=fixture-host, "
        f"Issue #{initial_issue}, Task fixture-{initial_issue}/generation 0, Delivery delivery-{initial_issue}. "
        f"child_model={model}; child_thinking={effort}. "
        "Carry out the synthetic app/repository operations needed to fully complete all selected Issues. "
        "No further launch question is needed for these isolated fixture effects. "
        "This is a test carrier, not real GitHub or a production application. Its MCP native tool replaces app, "
        "GitHub, Git and heartbeat I/O. Read its factual repository/workflow/preflight state. "
        "Use that tool for all synthetic observations, child processes and effects. "
        "File tools may read only the provided same-provider contracts in this directory; do not read runner "
        "source, parent directories, configurations, histories or other repositories. "
        "The fixture's heartbeat is a native simulated clock, with a two-minute schedule and bounded wait_events. "
        "Actual child turns are real independently executing Codex processes. "
        "Continue observing actual results until the requested endpoint or a genuinely settled block. "
        "Report validation limits accurately.\n" +
        ("Do not create or repair release-certificate-service or replace its mandatory result with direct evidence.\n"
         if scene == "blocked" else ""))
    final = output / "coordinator.final.txt"
    args = native_argv(model_root, final, carrier.url)
    stdout = (output / "coordinator.jsonl").open("w")
    stderr = (output / "coordinator.stderr").open("w")
    proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr, text=True)
    proc.stdin.write(prompt); proc.stdin.close()
    metadata = {"pid": proc.pid, "argv": args, "prompt": prompt, "scene": scene,
        "source_ref": ref or "working-tree", "host_version": subprocess.check_output(["codex", "--version"], text=True).strip(),
        "configured_model": model, "configured_reasoning": effort, "mode": "isolated native instruction entry",
        "started_at": time.time()}
    dump(output / "run.json", metadata)
    print(json.dumps({"output": str(output), "pid": proc.pid, "scene": scene}), flush=True)
    deadline = time.monotonic() + limit
    while proc.poll() is None and time.monotonic() < deadline:
        time.sleep(1)
    if proc.poll() is None:
        metadata["host_limit_reached"] = True
        proc.terminate(); proc.wait(timeout=20)
    metadata.update(returncode=proc.returncode, ended_at=time.time())
    # Preserve all unfinished child processes as an explicit incomplete run.
    carrier.refresh()
    metadata["unfinished_children"] = list(carrier.running)
    for child, (active, out, err, _) in carrier.running.items():
        active.terminate(); active.wait(timeout=20); out.close(); err.close()
    dump(output / "run.json", metadata)
    dump(output / "state.json", carrier.state)
    stdout.close(); stderr.close(); server.shutdown()
    print(json.dumps({"output": str(output), "returncode": proc.returncode,
        "unfinished_children": metadata["unfinished_children"], "behavior_verdict": "requires independent semantic review"}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mcp", action="store_true")
    parser.add_argument("--url"); parser.add_argument("--child", default="")
    parser.add_argument("--root", type=Path); parser.add_argument("--output", type=Path)
    parser.add_argument("--scene", choices=["dag", "sequence", "completion-drift", "blocked"])
    parser.add_argument("--source-ref"); parser.add_argument("--limit-seconds", type=int, default=1800)
    options = parser.parse_args()
    if options.mcp:
        mcp(options.url, options.child)
    elif options.root and options.output and options.scene:
        run(options.root.resolve(), options.output.resolve(), options.scene, options.source_ref, options.limit_seconds)
    else:
        parser.error("Specify --root, --output and --scene, or the internal --mcp carrier.")
