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
MODEL = "qwen3:4b"


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def command(argv, cwd, environment, output, name, timeout=600):
    with (output / (name + ".stdout")).open("wb") as stdout, (output / (name + ".stderr")).open("wb") as stderr:
        shell = os.name == "nt" and str(argv[0]).lower().endswith((".cmd", ".bat"))
        result = subprocess.run(subprocess.list2cmdline([str(x) for x in argv]) if shell else argv,
                                cwd=cwd, env=environment, shell=shell, stdout=stdout,
                                stderr=stderr, timeout=timeout, check=False)
    return {"argv": [str(x) for x in argv], "returncode": result.returncode,
            "stdout": name + ".stdout", "stderr": name + ".stderr"}


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
                           OLLAMA_CONTEXT_LENGTH="32768", OLLAMA_NUM_PARALLEL="1")
        server_log = (output / "ollama-server.log").open("wb")
        server = subprocess.Popen([str(ollama), "serve"], cwd=installed, env=environment,
                                  stdout=server_log, stderr=subprocess.STDOUT)
        report["model_server"] = wait_server(server, address)
        step = command([str(ollama), "pull", MODEL], installed, environment, output, "model-pull", timeout=1200)
        report["commands"].append(step)
        if step["returncode"]:
            raise RuntimeError("Local model download failed")
        with urllib.request.urlopen(address + "/api/tags", timeout=15) as response:
            report["local_models"] = json.load(response)
        bash = Path(shutil.which("git")).resolve().parent.parent / "bin/bash.exe"
        prompt = (
            "This is a read-only validation in the installed repository. Use the workflow and platform "
            "instructions automatically loaded by Codex. First acknowledge the actual Trellis session context "
            "if it loaded. Then use the installed guru-qualify-normal-scenario Skill in standalone mode with "
            "requirements_scope_set for this real candidate: whether an additional path-rendering repair is "
            "needed for supported Chinese-and-space repository paths in this installation. Read the Skill and "
            "its full contract, inspect current requirement authority and supported runtime consumers, and "
            "perform your own semantic judgment. Invoke its declared public wrapper and report its actual "
            "typed stdout. Do not edit files or create Issues, Tasks, Deliveries, commits or PRs. "
            f"The native Git for Windows Bash executable is {bash.as_posix()}. "
            "Use the activated installed managed runtime through the public wrapper. "
            "Do not substitute a direct hook call or a host-provided semantic result for the session workflow."
        )
        prompt_path = output / "session-prompt.txt"
        prompt_path.write_text(prompt, encoding="utf-8")
        argv = [str(codex), "exec", "--oss", "--local-provider", "ollama", "--model", MODEL,
                "--enable", "hooks", "--dangerously-bypass-hook-trust",
                "--dangerously-bypass-approvals-and-sandbox", "--json", "-C", str(installed),
                "-c", "model_context_window=32768", "-c", "model_max_output_tokens=4096", "-"]
        with prompt_path.open("rb") as stdin, (output / "session.jsonl").open("wb") as stdout, (output / "session.stderr").open("wb") as stderr:
            completed = subprocess.run(subprocess.list2cmdline(argv), shell=True, stdin=stdin,
                                       cwd=installed, env=environment, stdout=stdout, stderr=stderr,
                                       timeout=2700, check=False)
        report["session"] = {"argv": argv, "returncode": completed.returncode,
                             "events": "session.jsonl", "stderr": "session.stderr"}
        if (codex_home / "sessions").is_dir():
            shutil.copytree(codex_home / "sessions", output / "session-rollouts")
        report["status"] = "completed" if completed.returncode == 0 else "session_failed"
        # Completion is an execution fact. The task owner reviews automatic context
        # loading, actual Skill invocation and semantic output in the raw session.
        return 0 if completed.returncode == 0 else 1
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.SubprocessError) as exc:
        report.update(status="failed", error=f"{type(exc).__name__}: {exc}")
        return 1
    finally:
        if server is not None:
            server.terminate()
            try:
                server.wait(timeout=15)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait(timeout=15)
        if server_log is not None:
            server_log.close()
        write_json(output / "report.json", report)
        # Dependencies, binaries and model weights are temporary execution assets;
        # upload only non-sensitive configuration facts, raw events and logs.
        shutil.rmtree(output / "tools", ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
