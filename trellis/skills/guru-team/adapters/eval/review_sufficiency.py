"""Bounded production-owner native collection; semantics belong to its observing AI."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import time

from decision_dialogue import inspect_events
from review_sufficiency_cases import CSV, FOLLOWUPS, files, request


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prepare(source: Path, output: Path, case: str, python: str) -> Path:
    """Establish a clean matching provider before the tested semantic boundary."""
    target = output / "target"
    target.mkdir()
    core = target / ".trellis"
    core.mkdir()
    shutil.copytree(source / ".trellis/scripts", core / "scripts")
    for name in (".version", "workflow.md", "delivery-contract.md", "config.yaml"):
        if (source / ".trellis" / name).is_file():
            shutil.copy2(source / ".trellis" / name, core / name)
    subprocess.run(["git", "init", "-q", str(target)], check=True)
    argv = ["bash", str(source / "trellis/presets/guru-team/scripts/bash/apply.sh"),
            "--repo", str(target), "--platform", "codex", "--python", python, "--json"]
    installed = subprocess.run(argv, capture_output=True, check=False)
    (output / "install.stdout").write_bytes(installed.stdout)
    (output / "install.stderr").write_bytes(installed.stderr)
    write_json(output / "install.execution.json", {"argv": argv, "returncode": installed.returncode})
    if installed.returncode:
        raise RuntimeError("Original installation prerequisite failed; raw result retained")
    # Framework state is a provider, not the candidate under review.
    (target / ".gitignore").write_text(".trellis/\n.agents/\n.codex/\nAGENTS.md\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(target), "-c", "user.name=Eval", "-c",
                    "user.email=eval@example.invalid", "commit", "--allow-empty", "-qm",
                    "fixture baseline"], check=True)
    for relative, content in files(case).items():
        (target / relative).write_text(content, encoding="utf-8")
    return target


def collect(source: Path, output: Path, case: str, timeout: float,
            python: str, codex: str = "codex", sandbox: str = "read-only") -> dict:
    output.mkdir(parents=True, exist_ok=False)
    report = {"case": case, "evidence_kind": "production_owner_native",
              "source": str(source), "execution_complete": False, "turns": []}
    try:
        target = prepare(source, output, case, python)
    except (RuntimeError, OSError, subprocess.CalledProcessError) as error:
        report["error"] = str(error)
        write_json(output / "execution.json", report)
        return report
    prompts = [request(case)] + (FOLLOWUPS if case == "B" else [])
    session = None
    for index, prompt in enumerate(prompts):
        if case == "B" and index == 1:
            domain = target / "domain.py"
            domain.write_text(domain.read_text().replace('"total": len(selected)',
                                                        '"total": len(rows)'), encoding="utf-8")
            (target / "csv_adapter.py").write_text(CSV, encoding="utf-8")
        turn_dir = output / f"turn-{index + 1}"
        turn_dir.mkdir()
        # No host expectations or desired findings enter the Agent's context.
        prompt += ("\n完整匹配的Guru provider已由原installer安装在当前目录；读取当前provider的原Skill、"
                   "完整合同及必需规范，执行其原生产公开入口与前置。评审对象就是当前目录。"
                   "不要访问本次输出目录的其它部分、采集器、其它case、外部记忆或其它仓库。"
                   "保留原owner的缺失证据/前置停点，不能伪造结果；不要把本次评测当生产发布证明。")
        (turn_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
        before = {p.name: p.read_bytes() for p in target.iterdir()
                  if p.is_file() and p.suffix in {".py", ".md"} and p.name != "AGENTS.md"}
        argv = [codex, "--no-daemon", "exec", "--sandbox", sandbox, "--disable", "hooks",
                "--disable", "apps", "--disable", "memories", "--enable", "multi_agent",
                "-c", "mcp_servers={}"]
        if session:
            argv += ["resume", session]
        argv += ["--skip-git-repo-check", "--json", "-"]
        turn = {"argv": argv, "returncode": None, "completed": False}
        started = time.monotonic()
        try:
            result = subprocess.run(argv, cwd=target, input=prompt.encode(), capture_output=True,
                                    timeout=timeout, check=False)
            stdout, stderr = result.stdout, result.stderr
            turn["returncode"] = result.returncode
        except subprocess.TimeoutExpired as error:
            stdout, stderr = error.stdout or b"", error.stderr or b""
            turn["error"] = "timeout"
        except OSError as error:
            stdout, stderr = b"", b""
            turn["error"] = type(error).__name__
        (turn_dir / "events.jsonl").write_bytes(stdout)
        (turn_dir / "stderr.txt").write_bytes(stderr)
        after = {p.name: p.read_bytes() for p in target.iterdir()
                 if p.is_file() and p.suffix in {".py", ".md"} and p.name != "AGENTS.md"}
        turn["reviewed_files_changed"] = sorted(
            name for name in before.keys() | after.keys() if before.get(name) != after.get(name))
        observed, completed, error = inspect_events(stdout)
        if error:
            turn["error"] = error
        if session is None:
            session = observed
        elif observed and observed != session:
            turn["error"] = "resumed_thread_mismatch"
        turn.update(elapsed_seconds=round(time.monotonic() - started, 2),
                    completed=bool(completed and session and turn["returncode"] == 0 and "error" not in turn))
        report["turns"].append(turn)
        report["thread_id"] = session
        write_json(output / "execution.json", report)
        if not turn["completed"]:
            break
    report["execution_complete"] = len(report["turns"]) == len(prompts) and all(
        turn["completed"] for turn in report["turns"])
    write_json(output / "execution.json", report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--case", choices=list("ABCDE"), required=True)
    parser.add_argument("--timeout", type=float, default=1800)
    parser.add_argument("--python", default="python3")
    parser.add_argument("--sandbox", choices=["read-only", "workspace-write", "danger-full-access"],
                        default="read-only")
    args = parser.parse_args()
    report = collect(args.source_root.resolve(), args.output.resolve(), args.case,
                     args.timeout, args.python, sandbox=args.sandbox)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report["execution_complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
