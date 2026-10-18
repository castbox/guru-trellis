"""Facts and exact check execution for an AI-owned local revision replay.

No reuse classifier, semantic result, expected route, or owner pass is staged.
The current AI chooses individual commands after reading the owner contract.
Use a fresh temporary directory; this is not a business installation fixture.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys


TASK_REF = ".trellis/tasks/local-revision"


def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=root, check=True, text=True,
                          capture_output=True).stdout.strip()


def write(root: Path, relative: str, content: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def stage(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    git(root, "init", "-q", "-b", "main")
    git(root, "config", "user.name", "Test")
    git(root, "config", "user.email", "test@example.invalid")
    task = {
        "id": "local-revision", "name": "local-revision", "lifecycle_generation": 0,
        "source": {"kind": "no_issue"}, "title": "Independent calculation checks",
        "description": "Local execution-fact replay", "status": "in_progress",
        "dev_type": None, "scope": "A/B calculations and optional C", "package": None,
        "priority": "P2", "createdAt": "2026-10-09", "completedAt": None,
        "base_branch": "main", "worktree_path": None, "commit": None, "pr_url": None,
        "children": [], "parent": None, "relatedFiles": [], "notes": "", "meta": {},
    }
    files = {
        ".gitignore": ".trellis/.runtime/\n__pycache__/\n",
        f"{TASK_REF}/task.json": json.dumps(task) + "\n",
        f"{TASK_REF}/prd.md": "# Local requirement\nA adds one. B multiplies by the factor and rounds to the selected decimal precision. C, when added, squares its input.\n",
        f"{TASK_REF}/design.md": "# Design\nIndependent pure A and C. B depends on factor.py and B_DECIMALS. Checks and Python executable are explicit execution inputs. No external effects.\n",
        f"{TASK_REF}/implement.md": "# Implementation\nCheck each applicable calculation via its independent check file. The AI owner decides execution-fact applicability.\n",
        "a.py": "def add(value):\n    return value + 1\n",
        "factor.py": "FACTOR = 2\n",
        "b.py": "import os\nfrom factor import FACTOR\n\ndef scale(value):\n    return round(value * FACTOR, int(os.environ.get('B_DECIMALS', '2')))\n",
        "check_a.py": "from a import add\nassert add(0) == 1\nassert add(-2) == -1\n",
        "check_b.py": "import os\nfrom b import scale\nfrom factor import FACTOR\nassert scale(0) == 0\nassert scale(1.234) == round(1.234 * FACTOR, int(os.environ.get('B_DECIMALS', '2')))\n",
    }
    for relative, content in files.items():
        write(root, relative, content)
    git(root, "add", ".")
    git(root, "commit", "-qm", "local calculation fixture")


def change(root: Path, action: str) -> None:
    if action == "a":
        write(root, "a.py", "def add(value):\n    return 1 + value\n")
    elif action == "dependency":
        write(root, "factor.py", "FACTOR = 3\n")
    elif action == "check-version":
        with (root / "check_b.py").open("a") as stream:
            stream.write("assert scale(-2) == -2 * FACTOR\n")
    elif action == "c":
        write(root, "c.py", "def square(value):\n    return value * value\n")
        write(root, "check_c.py", "from c import square\nassert square(-3) == 9\nassert square(0) == 0\n")
    elif action == "metadata":
        task_path = root / TASK_REF / "task.json"
        task = json.loads(task_path.read_text())
        task["notes"] = "The same calculation scope is now resumed."
        task_path.write_text(json.dumps(task) + "\n")


def run_check(root: Path, check_id: str, python: str, decimals: str) -> dict:
    argv = [python, "-B", f"check_{check_id.lower()}.py"]
    result = subprocess.run(argv, cwd=root, text=True, capture_output=True,
                            env={**os.environ, "B_DECIMALS": decimals})
    toolchain = subprocess.run([python, "-c", "import sys; print(sys.executable); print(sys.version)"],
                              text=True, capture_output=True, check=True).stdout.strip()
    event = {"check_id": check_id, "argv": argv, "B_DECIMALS": decimals,
             "toolchain": toolchain, "returncode": result.returncode,
             "stdout": result.stdout, "stderr": result.stderr}
    log = root / ".trellis/.runtime/check-executions.jsonl"
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a") as stream:
        stream.write(json.dumps(event) + "\n")
    return event


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("stage", "change", "run", "inspect"))
    parser.add_argument("root", type=Path)
    parser.add_argument("value", nargs="?")
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--decimals", default="2")
    args = parser.parse_args()
    if args.action == "stage":
        stage(args.root)
    elif args.action == "change":
        if args.value not in {"a", "dependency", "check-version", "c", "metadata"}:
            parser.error("choose one supported normal content change")
        change(args.root, args.value)
    elif args.action == "run":
        if args.value not in {"A", "B", "C"}:
            parser.error("choose the exact check to execute")
        result = run_check(args.root, args.value, args.python, args.decimals)
        print(json.dumps(result))
        raise SystemExit(result["returncode"])
    else:
        log = args.root / ".trellis/.runtime/check-executions.jsonl"
        events = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
        print(json.dumps({"head": git(args.root, "rev-parse", "HEAD"),
                          "dirty": git(args.root, "status", "--short"),
                          "executions": events}))
