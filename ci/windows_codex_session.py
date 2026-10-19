"""Collect a real Codex session on the candidate native Windows installation."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time
import urllib.request
import zipfile

CODEX_VERSION = "0.163.0"
OLLAMA_VERSION = "v0.40.6"
MODEL = "qwen3.5:9b"
SESSION_MODEL = "guru630-windows-validation:latest"
SESSION_TIMEOUT = 600
REQUEST_NAME = ".guru-validation-request.md"
REQUEST_IDENTITY = "guru630-windows-agent-request-v2"

REQUEST = """# Installed native root scenario request

Identity: guru630-windows-agent-request-v2

Source: https://github.com/castbox/guru-trellis/issues/630, supported native Chinese-and-space root and actual Agent entry requirements.

Current behavior requirement: this actual supported repository root may contain Chinese characters and spaces. The installed root consumer must accept the same repository identity as Git and native Path resolve.

Candidate failure hypothesis to assess: the installed runtime.base_selection.repo(".") rejects this supported Chinese-and-space repository root or returns a different root identity. Inspect the installed consumer and actually run its supported normal entry before qualifying this hypothesis. This is a question to investigate, not an assertion that a defect exists, a semantic decision, or a request to implement a repair.

Use standalone requirements_scope_set. The request authority is this draft, not an active Task. Do not edit files or create Tasks, Issues, commits or PRs. The Agent independently authors the semantic result and calls the installed Skill wrapper on stdin.
"""


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def command(argv, cwd, environment, output, name, timeout=600):
    print(f"Windows Codex validation: {name}", flush=True)
    with (output / (name + ".stdout")).open("wb") as stdout, (output / (name + ".stderr")).open("wb") as stderr:
        shell = os.name == "nt" and str(argv[0]).lower().endswith((".cmd", ".bat"))
        result = subprocess.run(subprocess.list2cmdline([str(x) for x in argv]) if shell else argv,
                                cwd=cwd, env=environment, shell=shell, stdout=stdout,
                                stderr=stderr, timeout=timeout, check=False)
    return {"argv": [str(x) for x in argv], "returncode": result.returncode,
            "stdout": name + ".stdout", "stderr": name + ".stderr"}


def prepare_fixture(installed, environment, output, report):
    git = shutil.which("git")
    if not git:
        raise RuntimeError("Git is unavailable")
    (installed / REQUEST_NAME).write_text(REQUEST, encoding="utf-8", newline="\n")
    (output / "request-draft.md").write_text(REQUEST, encoding="utf-8", newline="\n")
    report["request"] = {"path": REQUEST_NAME, "input_copy": "request-draft.md"}
    step = command([git, "rev-parse", "--verify", "HEAD"], installed, environment,
                   output, "fixture-head-before")
    report["commands"].append(step)
    if step["returncode"]:
        step = command([git, "-c", "user.name=Guru CI fixture",
                        "-c", "user.email=guru-ci@example.invalid", "commit", "--allow-empty",
                        "--only", "-m", "Initialize Windows Codex validation fixture"],
                       installed, environment, output, "fixture-initial-commit")
        report["commands"].append(step)
        if step["returncode"]:
            raise RuntimeError("Validation fixture initial commit failed")
    step = command([git, "rev-parse", "--verify", "HEAD"], installed, environment,
                   output, "fixture-head")
    report["commands"].append(step)
    if step["returncode"]:
        raise RuntimeError("Validation fixture HEAD is unavailable")


def stop_process_tree(process):
    if os.name == "nt":
        # The .cmd launcher and Ollama both start child processes.
        subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       timeout=30, check=False)
    elif process.poll() is None:
        process.kill()
    process.wait(timeout=15)


def wait_server(process, address):
    deadline = time.monotonic() + 60
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError("Local model server exited before readiness")
        try:
            with urllib.request.urlopen(address + "/api/version", timeout=2) as response:
                return json.load(response)
        except (OSError, ValueError):
            time.sleep(1)
    raise RuntimeError("Local model server did not become ready")


def session_prompts(bash, python):
    public_input = {
        "profile": "requirements_scope_set", "mode": "standalone",
        "caller": "guru-clarify-requirements", "target_locator": REQUEST_NAME,
        "target": {"repo_locator": ".", "authority_kind": "draft",
                   "authority_locator": REQUEST_NAME, "authority_identity": REQUEST_IDENTITY,
                   "scope_locator": REQUEST_NAME},
        "candidate_refs": ["native-root-consumer-rejection"],
        "candidate_locators": [{"candidate_ref": "native-root-consumer-rejection",
                                "locators": ["path:" + REQUEST_NAME,
                                             "path:.trellis/guru-team/runtime/base_selection.py"]}],
    }
    startup = f"""Validate this actual clean Guru installation through the automatically loaded Codex/Trellis entry.
Work directly in this Agent. A Skill is Markdown instructions, NOT an agent_type. Do not delegate, edit files, or create Issues, Tasks, Deliveries, commits or PRs. This is a read-only standalone Skill request, not a task-free change.
This first turn loads live context and observations. The next turn in this SAME session will ask you to make the semantic judgment and invoke the Skill. Do not provide a semantic result in this first turn.
The default tool shell on native Windows is PowerShell. Use PowerShell syntax, not POSIX environment assignments or shell heredocs. Execute EVERY numbered program step with actual shell tool calls. Reading a file does not execute the commands it describes. A Markdown code block is not a tool call. Do not finish this turn after only reading files.
For every exec_command file-reading call, explicitly set max_output_tokens=32768. Read ONE file per call, not a concatenated file group. If any output says truncated or omits lines, read the missing line ranges in chunks of at most 80 lines, using max_output_tokens=8000 per call. For example, Get-Content -Encoding utf8 'path' | Select-Object -Skip 80 -First 80 reads lines 81-160. Advance the range until you have actually read the complete file. Do not repeatedly reread the entire file or file group after truncation, and do not treat truncated output as a complete read.
S1. Read each of these complete files in its own shell tool call:
Get-Content -Raw -Encoding utf8 .trellis/spec/workflow/clear-technical-writing.md
Get-Content -Raw -Encoding utf8 .agents/skills/trellis-start/SKILL.md
S2. Actually execute the startup context command:
& '{python.as_posix()}' .trellis/scripts/get_context.py
S3. Actually execute the startup Phase Index command:
& '{python.as_posix()}' .trellis/scripts/get_context.py --mode phase
S4. Read each complete Skill/schema/request/runtime file in its own shell tool call, with the output-budget and truncation rules above:
Get-Content -Raw -Encoding utf8 .agents/skills/guru-qualify-normal-scenario/SKILL.md
Get-Content -Raw -Encoding utf8 .agents/skills/guru-qualify-normal-scenario/references/contract.md
Get-Content -Raw -Encoding utf8 .agents/skills/guru-qualify-normal-scenario/schemas/public-requirements-scope-set-input.schema.json
Get-Content -Raw -Encoding utf8 .agents/skills/guru-qualify-normal-scenario/schemas/semantic-result.schema.json
Get-Content -Raw -Encoding utf8 {REQUEST_NAME}
Get-Content -Raw -Encoding utf8 .trellis/guru-team/runtime/base_selection.py
Get-Content -Raw -Encoding utf8 .trellis/guru-team/runtime/qualification_facts.py
Get-Content -Raw -Encoding utf8 .trellis/guru-team/skills/packages/guru-qualify-normal-scenario/runtime/common.py
S5. Actually execute the supported root consumer. Put BOTH following lines in ONE shell tool call so the Python process receives PYTHONPATH:
$env:PYTHONPATH = '.trellis/guru-team'
& '{python.as_posix()}' -c "from runtime.base_selection import repo; from pathlib import Path; print(repo('.')); print(Path.cwd().resolve())"
S6. Actually execute the Git HEAD observation:
git rev-parse HEAD
S7. Actually execute the Git root observation:
git rev-parse --show-toplevel
Before finishing, check the actual tool-call history for S1 through S7. Execute any omitted command now. Use actual tool output and exit codes; never infer or simulate them. Do not run hooks directly or inject workflow text. Report the actual observations or concrete command errors for each step. Do not output PASS or claim qualification or validation passed in this evidence-only turn.
"""
    qualify = f"""Continue the read-only standalone Guru Skill request in this same session.
Apply the full guru-qualify-normal-scenario contract to the actual request draft and live observations. First inspect the real tool-call history: S2 get_context.py, S3 --mode phase, S5 repo('.') and Path.cwd(), S6 Git HEAD and S7 Git root must actually have executed, not merely appeared in a read file or proposed code. Execute every missing step from the previous prompt now. Complete any missing full file reads with real shell tools before judging. Explicitly set exec_command max_output_tokens=32768 for each individual file read. If an earlier output was truncated, read only the missing line ranges in chunks of at most 80 lines with max_output_tokens=8000, using Get-Content -Encoding utf8 'path' | Select-Object -Skip <already-read-line-count> -First 80. Do not repeat an entire file group or assume omitted text was read.
Use the following complete public_input, which contains only caller-supplied request facts:
{json.dumps(public_input, ensure_ascii=True, indent=2)}
Independently author the remaining semantic_result fields from the actual contract/schema and observations: candidate_results with decision, reason and six-part witness; ai_review_gate; typed_exit; consumer. The public_input is nested inside semantic_result, itself inside the invocation envelope. Read the actual schema again if necessary. No semantic decision, witness, gate or exit is supplied here.
Before invocation, review your own complete judgment against the contract definitions and observed evidence. Keep the decision label, reason and witness consistent. If you discover an error, correct your own judgment. Never choose a result merely to make validation pass.
You must actually invoke the installed public wrapper on stdin with a shell tool call, not merely print JSON or a proposed command. Static path arithmetic in runtime source does not establish that a schema is missing: the installed wrapper resolves its own assets. Do not declare a missing-schema blocker from that inference. Execute the actual wrapper and use its actual diagnostic. It is a Bash script, not Python. The real Git for Windows Bash is '{bash.as_posix()}'. Retain the default PowerShell tool shell and explicitly execute that absolute Bash path. Use this PowerShell command structure with your own complete invocation JSON between the here-string delimiters:
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
@'
<your independently authored complete invocation JSON>
'@ | & '{bash.as_posix()}' '.agents/skills/guru-qualify-normal-scenario/scripts/invoke.sh' --invocation -
Use the activated managed runtime through that wrapper. Do not write qualification files or invent process IDs. Never simulate stdout. A nonzero wrapper result is rejected input, not success. Read any actual diagnostic and report the outcome honestly; if you correct your own input, execute the corrected invocation.
Before finishing, reread your final actual tool result and check that its decision, reason, witness and your explanation agree with the full Skill definitions. Correct an error through your own judgment and a fresh real wrapper invocation if needed. Report the actual wrapper exit code and stdout, with concise evidence limits. CLI exit0, prose, or reading files alone do not establish completion. Do not edit files, delegate, run hooks directly, or create external artifacts.
"""
    return startup, qualify


def run_session(codex_argv, prompts, installed, environment, output, report):
    deadline = time.monotonic() + SESSION_TIMEOUT
    report["session"] = {"status": "running", "timeout_seconds": SESSION_TIMEOUT, "rounds": []}
    thread_id = None
    for index, prompt in enumerate(prompts):
        name = "session" if index == 0 else "session-resume"
        argv = codex_argv + (["-"] if index == 0 else ["resume", thread_id, "-"])
        prompt_path = output / (name + "-prompt.txt")
        prompt_path.write_text(prompt, encoding="utf-8")
        remaining = deadline - time.monotonic()
        step = {"argv": argv, "status": "running", "remaining_seconds": max(0, remaining),
                "events": name + ".jsonl", "stderr": name + ".stderr"}
        report["session"]["rounds"].append(step)
        if remaining <= 0:
            step["status"] = report["session"]["status"] = "timed_out"
            raise subprocess.TimeoutExpired(argv, 0)
        print(f"Windows Codex validation: {name} ({remaining:.0f} seconds remaining)", flush=True)
        with prompt_path.open("rb") as stdin, (output / step["events"]).open("wb") as stdout, (output / step["stderr"]).open("wb") as stderr:
            shell = os.name == "nt" and str(argv[0]).lower().endswith((".cmd", ".bat"))
            process = subprocess.Popen(subprocess.list2cmdline(argv) if shell else argv, shell=shell,
                                       stdin=stdin, cwd=installed, env=environment, stdout=stdout, stderr=stderr)
            try:
                process.wait(timeout=max(0, deadline - time.monotonic()))
            except subprocess.TimeoutExpired:
                step["status"] = report["session"]["status"] = "timed_out"
                stop_process_tree(process)
                step["returncode"] = process.returncode
                raise
        step.update(status="completed", returncode=process.returncode)
        if process.returncode:
            report["session"]["status"] = "session_failed"
            return process.returncode
        if index == 0:
            events = [json.loads(line) for line in (output / step["events"]).read_text(encoding="utf-8").splitlines() if line.strip()]
            ids = [event["thread_id"] for event in events if event.get("type") == "thread.started"]
            if len(ids) != 1 or not isinstance(ids[0], str) or not ids[0]:
                raise RuntimeError("The initial Codex session did not emit one thread.started identity")
            thread_id = ids[0]
            report["session"]["thread_id"] = thread_id
    report["session"]["status"] = "completed"
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--diagnostics", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    report = {"status": "incomplete", "platform": platform.platform(), "commands": [],
              "codex_version": CODEX_VERSION, "ollama_version": OLLAMA_VERSION,
              "model": MODEL, "provider": "ollama", "credential_source": "none_local_model"}
    server = None
    server_log = None
    codex_home = None
    try:
        if os.name != "nt":
            raise RuntimeError("This evidence requires native Windows")
        candidate = json.loads((args.diagnostics / "result.json").read_text(encoding="utf-8"))
        if candidate["status"] != "passed":
            raise RuntimeError("Candidate product checks and installation must pass before the session")
        installed = Path(candidate["clean_install_root"]).resolve()
        if not (installed / ".trellis/guru-team/extension.json").is_file():
            raise RuntimeError("The actual candidate Guru installation is absent")
        report.update(candidate_sha=candidate["sha"], installed_root=str(installed),
                      source_lock=candidate["source_lock"])
        runtime = output / "tools"
        runtime.mkdir()
        codex_home = runtime / "codex-home"
        codex_home.mkdir()
        environment = dict(os.environ)
        # This isolated official configuration contains no maintainer credentials.
        environment["CODEX_HOME"] = str(codex_home)
        for key in ("OPENAI_API_KEY", "CODEX_API_KEY", "CHATGPT_API_KEY", "OPENAI_BASE_URL"):
            environment.pop(key, None)
        prepare_fixture(installed, environment, output, report)
        project = json.dumps(str(installed))
        config = f'[features]\nhooks = true\n\n[projects.{project}]\ntrust_level = "trusted"\n'
        (codex_home / "config.toml").write_text(config, encoding="utf-8", newline="\n")
        report["configuration"] = {"isolated_codex_home": True, "hooks": True,
                                   "project_trust": "trusted",
                                   "hook_review": "external_source_review_and_documented_one_off_trust_flag"}
        # Record the actual source bytes reviewed before using the CLI's documented
        # one-off automation trust option. Do not change project hook definitions.
        hooks = []
        for relative in (".codex/config.toml", ".codex/hooks.json"):
            path = installed / relative
            hooks.append({"path": relative, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        report["hook_sources"] = hooks
        npm = shutil.which("npm")
        if not npm:
            raise RuntimeError("npm is unavailable")
        step = command([npm, "install", "--prefix", str(runtime / "npm"), "--no-audit", "--no-fund",
                        "@openai/codex@" + CODEX_VERSION], installed, environment, output, "codex-install")
        report["commands"].append(step)
        if step["returncode"]:
            raise RuntimeError("Codex installation failed")
        codex = runtime / "npm/node_modules/.bin/codex.cmd"
        report["commands"].append(command([str(codex), "--version"], installed, environment, output, "codex-version"))
        archive = runtime / "ollama.zip"
        url = f"https://github.com/ollama/ollama/releases/download/{OLLAMA_VERSION}/ollama-windows-amd64.zip"
        urllib.request.urlretrieve(url, archive)
        report["ollama_download"] = {"url": url, "sha256": hashlib.sha256(archive.read_bytes()).hexdigest()}
        ollama_root = runtime / "ollama"
        with zipfile.ZipFile(archive) as package:
            package.extractall(ollama_root)
        archive.unlink()
        ollama = ollama_root / "ollama.exe"
        address = "http://127.0.0.1:11434"
        environment.update(OLLAMA_HOST=address, OLLAMA_MODELS=str(runtime / "models"),
                           OLLAMA_CONTEXT_LENGTH="65536", OLLAMA_NUM_PARALLEL="1")
        server_log = (output / "ollama-server.log").open("wb")
        server = subprocess.Popen([str(ollama), "serve"], cwd=installed, env=environment,
                                  stdout=server_log, stderr=subprocess.STDOUT)
        report["model_server"] = wait_server(server, address)
        step = command([str(ollama), "pull", MODEL, "--runner", "llamacpp"],
                       installed, environment, output, "model-pull", timeout=1200)
        report["commands"].append(step)
        if step["returncode"]:
            raise RuntimeError("Local model download failed")
        modelfile = runtime / "Modelfile"
        modelfile.write_text(f"FROM {MODEL}\nPARAMETER num_ctx 65536\n", encoding="utf-8", newline="\n")
        shutil.copyfile(modelfile, output / "session.Modelfile")
        report["model_configuration"] = {"source_tag": MODEL, "session_tag": SESSION_MODEL,
                                         "modelfile": "session.Modelfile"}
        step = command([str(ollama), "create", SESSION_MODEL, "-f", str(modelfile)],
                       installed, environment, output, "model-create")
        report["commands"].append(step)
        if step["returncode"]:
            raise RuntimeError("Local session model creation failed")
        report["model_shows"] = {}
        for tag in (MODEL, SESSION_MODEL):
            request = urllib.request.Request(address + "/api/show", json.dumps({"model": tag}).encode("utf-8"),
                                             {"Content-Type": "application/json"})
            with urllib.request.urlopen(request, timeout=30) as response:
                actual = json.load(response)
            report["model_shows"][tag] = {key: actual[key] for key in
                                           ("details", "parameters", "capabilities", "manifests", "thinking")
                                           if key in actual}
        with urllib.request.urlopen(address + "/api/tags", timeout=15) as response:
            report["local_models"] = json.load(response)
        bash = Path(shutil.which("git")).resolve().parent.parent / "bin/bash.exe"
        argv = [str(codex), "exec", "--oss", "--local-provider", "ollama", "--model", SESSION_MODEL,
                "--enable", "hooks", "--dangerously-bypass-hook-trust",
                "--dangerously-bypass-approvals-and-sandbox", "--json", "-C", str(installed),
                "-c", "model_context_window=65536", "-c", "tool_output_token_limit=32768",
                "-c", "model_reasoning_effort=none"]
        returncode = run_session(argv, session_prompts(bash, Path(sys.executable)),
                                 installed, environment, output, report)
        report["status"] = "completed" if returncode == 0 else "session_failed"
        # Completion is an execution fact. The task owner reviews automatic context
        # loading, actual Skill invocation and semantic output in the raw session.
        return 0 if returncode == 0 else 1
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.SubprocessError) as exc:
        report.update(status="failed", error=f"{type(exc).__name__}: {exc}")
        return 1
    finally:
        if server is not None:
            if server.poll() is None:
                try:
                    with urllib.request.urlopen(address + "/api/ps", timeout=5) as response:
                        report["loaded_models"] = json.load(response)
                except (OSError, ValueError) as exc:
                    report["loaded_models_error"] = f"{type(exc).__name__}: {exc}"
            try:
                stop_process_tree(server)
            except (OSError, subprocess.SubprocessError) as exc:
                report["cleanup_error"] = f"{type(exc).__name__}: {exc}"
        if server_log is not None:
            server_log.close()
        if codex_home is not None and (codex_home / "sessions").is_dir():
            shutil.copytree(codex_home / "sessions", output / "session-rollouts")
        print(f"Windows Codex validation: {report['status']}", flush=True)
        write_json(output / "report.json", report)
        # Dependencies, binaries and model weights are temporary execution assets;
        # upload only non-sensitive configuration facts, raw events and logs.
        shutil.rmtree(output / "tools", ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
