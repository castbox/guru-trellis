"""Test-only native dialogue collector. AI reviews semantics, never this script."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time


SKILLS = Path(__file__).resolve().parents[2]
REPO = SKILLS.parents[2]
CASES = Path(__file__).with_name("decision_dialogue_cases.json")


def section(text: str, heading: str) -> str:
    start = text.index(heading)
    end = text.find("\n## ", start + len(heading))
    return text[start:] if end < 0 else text[start:end]


def stage_methods(source: Path, fixture: Path) -> None:
    assets = {
        "interaction.md": (
            source / "trellis/presets/guru-team/spec/workflow/workflow-contract.md",
            "## Interaction Budget",
        ),
        "exploration.md": (
            source / "trellis/skills/guru-team/packages/guru-clarify-requirements/references/contract.md",
            "## Questions And Convergence",
        ),
        "planning.md": (
            source / "trellis/skills/guru-team/packages/guru-author-task-plan/references/planning-body.md",
            "## 2. 从来源到正文",
        ),
    }
    methods = fixture / "methods"
    methods.mkdir()
    for name, (path, heading) in assets.items():
        (methods / name).write_text(section(path.read_text(encoding="utf-8"), heading), encoding="utf-8")


def inspect_events(raw: bytes) -> tuple[str | None, bool, str | None]:
    ids = set()
    completed = False
    try:
        for line in raw.decode("utf-8").splitlines():
            if not line.strip():
                continue
            event = json.loads(line)
            if event.get("type") == "thread.started":
                ids.add(event["thread_id"])
            if event.get("type") == "turn.completed":
                completed = True
    except (UnicodeDecodeError, ValueError, KeyError, TypeError, AttributeError):
        return None, False, "invalid_native_events"
    if len(ids) > 1:
        return None, False, "ambiguous_thread_identity"
    return next(iter(ids), None), completed, None


def collect(case: dict, source: Path, output: Path, *, codex: str = "codex",
            timeout: float = 600, disable_mcp: tuple[str, ...] = (), run=subprocess.run) -> dict:
    output.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    report = {"case_id": case["id"], "evidence_kind": "question_method_only",
              "execution_complete": False, "turns": []}
    with tempfile.TemporaryDirectory(prefix="guru-decision-method-") as directory:
        fixture = Path(directory)
        stage_methods(source, fixture)
        (fixture / "repository-facts.md").write_text(case["repository_facts"], encoding="utf-8")
        (fixture / "AGENTS.md").write_text(
            "# Isolated question-method experiment\n\n"
            "Read methods/*.md and repository-facts.md before answering. Apply only the "
            "loaded decision-exploration methods to the synthetic request. This fixture "
            "has no installed Guru runtime, Task or lifecycle. Do not claim formal Skill "
            "invocation, approval, implementation or lifecycle results. Investigate the "
            "provided files; do not access outside this fixture or modify files. Respond "
            "in Chinese. Ask real unresolved choices; when clear, present the resulting "
            "behavior and acceptance plan in chat. Future test replies are not available "
            "until the next user turn.\n", encoding="utf-8")
        shutil.copytree(fixture / "methods", output / "methods")
        shutil.copyfile(fixture / "repository-facts.md", output / "repository-facts.md")
        session = None
        for index, prompt in enumerate(case["turns"]):
            remaining = timeout - (time.monotonic() - started)
            if remaining <= 0:
                report["error"] = "deadline_exceeded"
                break
            args = [codex, "--no-daemon", "exec", "--sandbox", "read-only",
                    "--disable", "hooks", "--disable", "apps", "--disable", "memories"]
            for server in disable_mcp:
                args += ["-c", f"mcp_servers.{server}.enabled=false"]
            if session is not None:
                args += ["resume", session]
            args += ["--skip-git-repo-check", "--json", "-"]
            turn_path = output / f"turn-{index + 1}"
            turn_path.mkdir()
            (turn_path / "prompt.txt").write_text(prompt, encoding="utf-8")
            turn = {"argv": args, "returncode": None, "completed": False}
            try:
                result = run(args, cwd=fixture, input=prompt.encode("utf-8"),
                             capture_output=True, timeout=remaining, check=False)
                stdout, stderr = result.stdout, result.stderr
                turn["returncode"] = result.returncode
            except subprocess.TimeoutExpired as exc:
                stdout, stderr = exc.stdout or b"", exc.stderr or b""
                turn["error"] = "timeout"
            except OSError as exc:
                stdout, stderr = b"", b""
                turn["error"] = type(exc).__name__
            (turn_path / "events.jsonl").write_bytes(stdout)
            (turn_path / "stderr.txt").write_bytes(stderr)
            observed, completed, error = inspect_events(stdout)
            if error:
                turn.setdefault("error", error)
            if session is None:
                session = observed
            elif observed is not None and observed != session:
                turn["error"] = "resumed_thread_mismatch"
            turn["completed"] = bool(completed and session and turn["returncode"] == 0
                                     and "error" not in turn)
            report["turns"].append(turn)
            if not turn["completed"]:
                break
        report["thread_id"] = session
        report["execution_complete"] = (len(report["turns"]) == len(case["turns"])
                                        and all(turn["completed"] for turn in report["turns"]))
    (output / "execution.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", required=True)
    parser.add_argument("--source-root", type=Path, default=REPO)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--codex", default="codex")
    parser.add_argument("--timeout", type=float, default=600)
    parser.add_argument("--disable-mcp", action="append", default=[], metavar="NAME",
                        help="Disable one configured MCP server for this trial; repeat for every configured server.")
    args = parser.parse_args()
    cases = json.loads(CASES.read_text(encoding="utf-8"))["cases"]
    case = next((value for value in cases if value["id"] == args.case), None)
    if case is None:
        parser.error("Unknown case; inspect decision_dialogue_cases.json for available ids.")
    report = collect(case, args.source_root.resolve(), args.output.resolve(),
                     codex=args.codex, timeout=args.timeout, disable_mcp=tuple(args.disable_mcp))
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report["execution_complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
