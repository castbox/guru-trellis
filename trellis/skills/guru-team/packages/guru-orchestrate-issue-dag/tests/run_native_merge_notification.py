"""Replay merge notifications with real Git and isolated native Codex turns."""

from __future__ import annotations

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import threading
import time

from run_native_orchestration import configuration, dump, native_argv, project_provider


REPOSITORY = "fixture/merge-notification"
ISSUE = 42
CHILD = "fixture-child-42"
CONDITION = "请关注同仓合并；仅在出现实际的 Git 合并冲突时同步目标分支。"
WORKFLOW = "trellis/workflows/guru-team/workflow.md"
RECONCILE = ".trellis/guru-team/skills/packages/guru-reconcile-task-base"
FILE = "report.txt"
GIT_ENV = {
    **os.environ,
    "GIT_AUTHOR_DATE": "2026-11-01T00:00:00Z",
    "GIT_COMMITTER_DATE": "2026-11-01T00:00:00Z",
}


def execute(cwd: Path, argv: list[str]) -> dict:
    proc = subprocess.run(argv, cwd=cwd, env=GIT_ENV, capture_output=True, text=True)
    return {"argv": argv, "exit_code": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}


def git(repo: Path, *args: str) -> str:
    result = execute(repo, ["git", *args])
    if result["exit_code"]:
        raise RuntimeError(result)
    return result["stdout"].strip()


class Fixture:
    def __init__(self, cwd: Path, scenario: str, wrapper: Path, evidence: Path):
        self.cwd = cwd
        self.scenario = scenario
        self.wrapper = wrapper
        self.evidence = evidence
        self.origin = cwd / "origin.git"
        self.repo = cwd / "review"
        self.sibling = cwd / "sibling"
        self.target: str | None = None
        git(cwd, "init", "--bare", "--initial-branch=main", str(self.origin))
        git(cwd, "clone", str(self.origin), str(self.repo))
        for key, value in (("user.name", "Fixture"), ("user.email", "fixture@example.invalid"),
                           ("commit.gpgsign", "false"), ("core.hooksPath", "/dev/null")):
            git(self.repo, "config", key, value)
        lines = ["Heading: original", *[f"Stable line {n}" for n in range(1, 11)], "Footer: original"]
        (self.repo / FILE).write_text("\n".join(lines) + "\n")
        git(self.repo, "add", FILE)
        git(self.repo, "commit", "-m", "Initial report")
        self.start = git(self.repo, "rev-parse", "HEAD")
        git(self.repo, "push", "origin", "main")
        git(self.repo, "switch", "-c", "issue-42")
        lines[0] = "Heading: reviewed change"
        (self.repo / FILE).write_text("\n".join(lines) + "\n")
        git(self.repo, "commit", "-am", "Edit report heading")
        self.head = git(self.repo, "rev-parse", "HEAD")
        git(self.repo, "push", "origin", "issue-42")
        self.before_evidence = execute(self.repo, ["git", "diff", "--check", self.start, self.head])
        if self.before_evidence["exit_code"]:
            raise RuntimeError(self.before_evidence)
        git(cwd, "clone", str(self.origin), str(self.sibling))
        for key, value in (("user.name", "Sibling"), ("user.email", "sibling@example.invalid"),
                           ("commit.gpgsign", "false"), ("core.hooksPath", "/dev/null")):
            git(self.sibling, "config", key, value)
        dump(evidence / "start.json", {"start": self.start, "candidate": self.head,
                                      "prior_review_evidence": self.before_evidence})

    def receive_notice(self) -> dict:
        if self.target is None:
            path = self.sibling / FILE
            source = path.read_text()
            if self.scenario == "conflict":
                source = source.replace("Heading: original", "Heading: parallel change")
            else:
                source = source.replace("Footer: original", "Footer: parallel change")
            path.write_text(source)
            git(self.sibling, "commit", "-am", "Apply sibling change")
            git(self.sibling, "push", "origin", "HEAD:main")
            git(self.repo, "fetch", "origin", "main")
            self.target = git(self.repo, "rev-parse", "origin/main")
        notice = {
            "repository": REPOSITORY, "merged_pr": 41, "target_branch": "origin/main",
            "observed_merge_head": self.target, "user_condition": CONDITION,
        }
        dump(self.evidence / "notice.json", notice)
        return notice

    def snapshot(self) -> dict:
        return {
            "repository": REPOSITORY, "issue": ISSUE, "task_id": "fixture-42",
            "delivery_id": "fixture-42-d1", "phase": "reviewing",
            "candidate": git(self.repo, "rev-parse", "HEAD"), "review_base": self.start,
            "target": git(self.repo, "rev-parse", "origin/main"),
            "target_branch": "origin/main", "worktree": str(self.repo),
            "branch": "issue-42", "prior_review_evidence": self.before_evidence,
            "issue_state": "OPEN", "dependencies": [],
            "issue_title": "Edit the report heading",
            "issue_body": "Review the heading change at its existing candidate.",
            "validation": ["git diff --check on the fixed candidate"],
            "required_integration_check_failures": [], "server_update_required": False,
            "review": "In progress. The previous range whitespace check is available.",
        }

    def call(self, operation: str, arguments: dict) -> dict:
        if operation == "inspect":
            return self.snapshot()
        if operation == "compare":
            base, head = (arguments[name] for name in ("base", "head"))
            for oid in (base, head):
                if oid not in {self.start, self.head, self.target}:
                    raise ValueError("Use a commit returned by the fixture.")
            return {
                "diff": execute(self.repo, ["git", "diff", base, head]),
                "check": execute(self.repo, ["git", "diff", "--check", base, head]),
            }
        if operation == "merge_tree":
            candidate = arguments["candidate"]
            target = arguments["target"]
            if candidate != self.head or target != self.target:
                raise ValueError("Use the live candidate and observed target commits.")
            return execute(self.repo, ["git", "merge-tree", "--write-tree", target, candidate])
        if operation == "read_notification":
            return self.receive_notice()
        if operation == "execute_base_candidate":
            if arguments["task_head"] != self.head or arguments["new_base_head"] != self.target:
                raise ValueError("Use exact candidate and target commits returned by the fixture.")
            request = {
                "task_head": arguments["task_head"], "new_base_head": arguments["new_base_head"],
                "validation_commands": [],
            }
            path = self.evidence / "reconcile-request.json"
            dump(path, request)
            return execute(self.repo, ["bash", str(self.wrapper), "--root", str(self.repo), "--request", str(path)])
        raise ValueError(f"Operation unavailable in this review segment: {operation}")

    def finish(self) -> None:
        dump(self.evidence / "end.json", self.snapshot())
        git(self.repo, "bundle", "create", str(self.evidence / "repository.bundle"), "--all")


REVIEW_TOOLS = """The native fixture tool accepts these operations:
inspect {}, compare {base, head}, merge_tree {candidate, target},
read_notification {}, execute_base_candidate {task_head, new_base_head}.
OID values come from real local Git. execute_base_candidate runs the installed
original Reconcile candidate command. It is the farthest integration action
available in this segment. No PR or merge writes are available.
"""

REVIEW_PROMPT = f"""You are the current owner of an in-progress fixed-candidate review
in the isolated repository {REPOSITORY}, Issue #{ISSUE}. Load the installed writing
contract and the applicable original workflow entry before acting. Retain the
existing review context. Read the current candidate and prior review evidence
through inspect. Then read the waiting notification and carry out the next
action of this existing phase through the fixture tool. Stop once you have
executed the next review action or the first applicable integration entry.
Give the observed outcome. Read only the projected files inside this directory.
{REVIEW_TOOLS}"""


class Run:
    def __init__(self, fixture: Fixture, model_root: Path, model: str, effort: str, limit: int):
        self.fixture = fixture
        self.model_root = model_root
        self.model = model
        self.effort = effort
        self.limit = limit
        self.output = fixture.evidence
        self.url = ""
        self.child = None
        self.messages: list[dict] = []
        self.operation: str | None = None
        self.lock = threading.Lock()

    def start(self, role: str, prompt: str, child: str = ""):
        output = self.output
        args = native_argv(self.model_root, output / f"{role}.final.txt", self.url, child, self.model, self.effort)
        with (output / f"{role}.jsonl").open("w") as stdout, (output / f"{role}.stderr").open("w") as stderr:
            proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr, text=True)
            assert proc.stdin is not None
            proc.stdin.write(prompt)
            proc.stdin.close()
        dump(output / f"{role}.process.json", {"argv": args, "prompt": prompt, "pid": proc.pid})
        return proc

    def child_state(self) -> dict:
        active = self.child is not None and self.child.poll() is None
        final = self.output / "child.final.txt"
        messages = list(self.messages)
        if final.is_file() and not active:
            messages.append({"role": "assistant", "text": final.read_text()})
        return {**self.fixture.snapshot(), "thread_id": CHILD, "host_id": "fixture-host",
                "active": active, "messages": messages, "safe": not active}

    def dispatch(self, role: str, operation: str, arguments: dict) -> dict:
        if role:
            return self.fixture.call(operation, arguments)
        if operation in ("inspect", "inspect_environment"):
            node = self.fixture.snapshot()
            return {
                **node, "children": {CHILD: self.child_state()}, "nodes": {str(ISSUE): node},
                "project_id": "fixture-project", "project_path": str(self.fixture.repo),
                "primary_folder": str(self.fixture.repo), "remote": str(self.fixture.origin),
                "authenticated": True, "ready": True, "trusted": True, "unresolved_operations": [],
            }
        if operation == "inspect_capabilities":
            return {"native": True, "operations": ["inspect", "read_child", "send_message", "wait_events"],
                    "model": self.model, "effort": self.effort}
        if operation == "list_projects":
            return {"projects": [{"id": "fixture-project", "repository": REPOSITORY,
                                  "path": str(self.fixture.repo), "primary_folder": str(self.fixture.repo)}]}
        if operation in ("read_child", "read_operation", "wait_events"):
            if operation == "read_child":
                return self.child_state()
            if operation == "wait_events":
                time.sleep(min(max(float(arguments.get("seconds", 0)), 0), 2))
            return {"children": {CHILD: self.child_state()}, "operation_id": self.operation}
        if operation == "send_message":
            if arguments["child_id"] != CHILD or self.child is not None:
                raise ValueError("This fixture allows one dispatch to the existing owner.")
            message = arguments["message"]
            self.messages.append({"role": "coordinator", "text": message})
            self.child = self.start("child", REVIEW_PROMPT + "\nCoordinator message:\n" + message, CHILD)
            self.operation = "fixture-send-42"
            return {"child_id": CHILD, "thread_id": CHILD, "host_id": "fixture-host",
                    "operation_id": self.operation, "active": True}
        return self.fixture.call(operation, arguments)

    def run(self) -> dict:
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                data = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                role, operation, arguments = (data[k] for k in ("child", "operation", "arguments"))
                with outer.lock:
                    try:
                        result = outer.dispatch(role, operation, arguments)
                    except (RuntimeError, ValueError, KeyError) as error:
                        result = {"error": type(error).__name__, "detail": str(error)}
                    with (outer.output / "carrier.jsonl").open("a") as trace:
                        trace.write(json.dumps({"role": role, "operation": operation, "arguments": arguments,
                                                "result": result}, ensure_ascii=False) + "\n")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode())

            def log_message(self, *args):
                pass

        with ThreadingHTTPServer(("127.0.0.1", 0), Handler) as server:
            self.url = f"http://127.0.0.1:{server.server_port}"
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                if self.fixture.scenario == "dispatch":
                    notice = self.fixture.receive_notice()
                    prompt = f"""Explicitly invoke the Guru Issue DAG Skill from
trellis/skills/guru-team/packages/guru-orchestrate-issue-dag/SKILL.md.
Resume one admitted node, {REPOSITORY}#{ISSUE}, with no dependencies, mode auto,
max_parallel 2, failure_policy continue_independent. Use the existing child
{CHILD} on fixture-host, model {self.model}, effort {self.effort}. The user's
current instruction is the condition in this received merge notice:
{json.dumps(notice, ensure_ascii=False)}
Continue this existing child's review through one coordinator dispatch. Then read
back the actual dispatch and stop at that user-selected boundary. Use only the
isolated fixture MCP operations and same-provider projected files. The fixture
stands in for Codex chat transport and GitHub observation. Its Git data is real
in a local repository. Inspect can read the current node and existing binding,
compare and merge_tree can read Git facts for observed commits, and send_message
accepts child_id and message. The tool records and sends exactly that message.
"""
                    actor = self.start("coordinator", prompt)
                else:
                    actor = self.start("reviewer", REVIEW_PROMPT, "reviewer")
                deadline = time.monotonic() + self.limit
                while time.monotonic() < deadline:
                    if actor.poll() is not None and (self.child is None or self.child.poll() is not None):
                        break
                    time.sleep(0.5)
                processes = {"actor": actor}
                if self.child is not None:
                    processes["child"] = self.child
                unfinished = [role for role, proc in processes.items() if proc.poll() is None]
                for role in unfinished:
                    processes[role].terminate()
                return {"returncodes": {role: proc.wait(timeout=15) for role, proc in processes.items()},
                        "timed_out": unfinished}
            finally:
                server.shutdown()


def project(root: Path, destination: Path) -> None:
    project_provider(root, destination, None)
    files = {
        WORKFLOW: ".trellis/workflow.md",
        "trellis/presets/guru-team/spec/workflow/clear-technical-writing.md":
            ".trellis/spec/workflow/clear-technical-writing.md",
        ".trellis/spec/workflow/companion-scripts.md": ".trellis/spec/workflow/companion-scripts.md",
        RECONCILE + "/SKILL.md": RECONCILE + "/SKILL.md",
        RECONCILE + "/references/contract.md": RECONCILE + "/references/contract.md",
    }
    for source, target in files.items():
        output = destination / target
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / source, output)
    shutil.copytree(root / "trellis/workflows/guru-team/references",
                    destination / ".trellis/guru-team/references")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model")
    parser.add_argument("--effort")
    parser.add_argument("--case", choices=["dispatch", "receive", "conflict"], action="append")
    parser.add_argument("--limit-seconds", type=int, default=480)
    options = parser.parse_args()
    root = options.root.resolve()
    output = options.output.resolve()
    output.mkdir()
    settings = configuration()
    model = options.model or settings.get("model")
    effort = options.effort or settings.get("model_reasoning_effort")
    if not model or not effort:
        raise RuntimeError("Set both --model and --effort or configure Codex defaults.")
    cli_version = subprocess.check_output(["codex", "--version"], text=True).strip()
    dump(output / "settings.json", {"model": model, "effort": effort, "codex": cli_version,
                                   "source_head": git(root, "rev-parse", "HEAD")})
    project(root, output / "source")
    wrapper = root / RECONCILE / "scripts/execute-base-candidate.sh"
    for scenario in options.case or ("dispatch", "receive", "conflict"):
        evidence = output / scenario
        evidence.mkdir()
        with tempfile.TemporaryDirectory(prefix=f"guru-merge-notification-{scenario}-") as temp:
            fixture = Fixture(Path(temp), scenario, wrapper, evidence)
            try:
                run = Run(fixture, output / "source", model, effort, options.limit_seconds)
                result = run.run()
                dump(evidence / "run.json", result)
                print(json.dumps({"scenario": scenario, **result}), flush=True)
            finally:
                fixture.finish()


if __name__ == "__main__":
    main()
