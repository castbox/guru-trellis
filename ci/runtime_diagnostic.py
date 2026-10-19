"""Observe the target's fixed public-wrapper capability fixture."""
from __future__ import annotations

import argparse
import importlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile

from targeted_ci import find_bash, write_json


class WrapperObserver:
    """Return original results and exceptions; record only declared fixture calls."""

    def __init__(self, run, cases, calls):
        self.run = run
        self.cases = cases
        self.calls = calls

    def record(self, command, kwargs, index, supplemental=False):
        row = {"case_index": index, "supplemental": supplemental,
               "argv": [str(part) for part in command]}
        self.calls.append(row)
        try:
            result = self.run(command, **kwargs)
        except Exception as exc:
            row["exception"] = {"type": type(exc).__name__, "message": str(exc)}
            raise
        row.update(returncode=result.returncode, stdout=result.stdout, stderr=result.stderr)
        return result

    def matches(self, result, case):
        try:
            payload = json.loads(result.stdout)
            return (result.returncode == case["expected_returncode"]
                    and all(payload.get(key) == value for key, value in case["expected_output"].items()))
        except (ValueError, AttributeError, TypeError):
            return False

    def supplement(self, command, kwargs, index):
        # The original fixture stops on its first mismatch. While its temporary
        # view is live, observe the remaining declared cases as separate calls.
        for next_index in range(index + 1, len(self.cases)):
            extra = [*command[:2], *self.cases[next_index]["arguments"]]
            try:
                self.record(extra, kwargs, next_index, supplemental=True)
            except Exception:
                pass  # Each exception is recorded; the primary exception is retained.

    def __call__(self, command, *args, **kwargs):
        index = next((i for i, case in enumerate(self.cases)
                      if isinstance(command, (list, tuple)) and len(command) >= 2
                      and command[0] == "bash" and Path(command[1]).name == "invoke.sh"
                      and list(command[2:]) == case["arguments"]), None)
        if index is None or args:
            return self.run(command, *args, **kwargs)
        try:
            result = self.record(command, kwargs, index)
        except Exception:
            self.supplement(command, kwargs, index)
            raise
        if not self.matches(result, self.cases[index]):
            self.supplement(command, kwargs, index)
        return result


def git_sha(root):
    return subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()


def collect(target, python, report):
    source_venv = python.parent.parent
    if not (source_venv / "pyvenv.cfg").is_file():
        raise RuntimeError("--python must select the target's hash-locked CI virtual environment")
    bash = find_bash()
    if not bash:
        raise RuntimeError("Bash unavailable; runtime diagnostic not executed")
    bash_result = subprocess.run([bash, "-c", "uname -s; bash --version"],
                                 text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    report["bash"] = {"executable": bash, "returncode": bash_result.returncode,
                      "stdout": bash_result.stdout, "stderr": bash_result.stderr}
    if bash_result.returncode or (os.name == "nt" and not bash_result.stdout.startswith(("MINGW", "MSYS"))):
        raise RuntimeError("Native Git for Windows Bash is required on Windows")
    # bootstrap_check invokes bare bash. Give it the verified native Bash, while
    # retaining its exact original argv and subprocess keyword arguments.
    os.environ["PATH"] = str(Path(bash).parent) + os.pathsep + os.environ.get("PATH", "")
    assets = target / "trellis/skills/guru-team/runtime"
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(assets))
    bootstrap = importlib.import_module("bootstrap")
    check = importlib.import_module("bootstrap_check")
    report["bootstrap_check"] = str(Path(check.__file__))
    cases = json.loads((assets / "python-runtime.json").read_text(encoding="utf-8"))["public_wrapper_check"]["cases"]
    report["declared_cases"] = len(cases)
    runtime_id, identity = bootstrap.runtime_identity(assets, python)
    probe = bootstrap.run_probe(python, assets)
    report["runtime_id"] = runtime_id
    with tempfile.TemporaryDirectory(prefix="guru-ci-runtime-diagnostic-") as temporary:
        candidate = Path(temporary) / "candidate"
        candidate.mkdir()
        shutil.copytree(source_venv, candidate / "venv")
        write_json(candidate / "metadata.json", {"schema_version": "1.0", "runtime_id": runtime_id,
                                                "identity": identity, "dependencies": probe["dependencies"]})
        original = check.subprocess.run
        check.subprocess.run = WrapperObserver(original, cases, report["calls"])
        try:
            check.check_public_wrapper(assets, runtime_id, candidate)
            report["fixture_status"] = "passed"
        except Exception as exc:
            if not report["calls"]:
                raise
            report["fixture_status"] = "failed"
            report["fixture_exception"] = {"type": type(exc).__name__, "message": str(exc)}
        finally:
            check.subprocess.run = original
    if len({row["case_index"] for row in report["calls"]}) != len(cases):
        raise RuntimeError("Declared wrapper cases were not all observed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-root", required=True, type=Path)
    parser.add_argument("--python", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    target = args.target_root.resolve()
    # Do not resolve the final interpreter symlink out of its dependency venv.
    python = Path(os.path.abspath(args.python))
    report = {"target_root": str(target), "python": str(python), "python_version": sys.version,
              "platform": platform.platform(), "collector_status": "incomplete", "calls": []}
    try:
        report["driver_sha"] = git_sha(Path(__file__).resolve().parent.parent)
        report["target_sha"] = git_sha(target)
        collect(target, python, report)
        report["collector_status"] = "completed"
    except Exception as exc:
        report["collector_status"] = "failed"
        report["collector_exception"] = {"type": type(exc).__name__, "message": str(exc)}
    write_json(args.output, report)
    return 0 if report["collector_status"] == "completed" else 1


if __name__ == "__main__":
    sys.exit(main())
