"""Repository-private native CI driver. Product assertions stay in each target."""
from __future__ import annotations

import argparse
import json
import locale
import os
from pathlib import Path
import platform
import shlex
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
TEST_ROOT = Path("trellis/presets/guru-team/scripts/python")


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def run(command, cwd, path_prepend=None, env_patch=None, input_data=None):
    command = [str(part) for part in command]
    # npm.cmd is a Windows command script; subsequent pnpm calls use node directly.
    shell = os.name == "nt" and command[0].lower().endswith((".cmd", ".bat"))
    env = None
    if path_prepend is not None or env_patch is not None:
        env = dict(os.environ)
        env.update(env_patch or {})
    if path_prepend is not None:
        env["PATH"] = str(path_prepend) + os.pathsep + env.get("PATH", "")
    return subprocess.run(subprocess.list2cmdline(command) if shell else command,
                          cwd=cwd, env=env, shell=shell, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, input=input_data)


class Steps:
    def __init__(self, directory, target):
        self.directory = directory
        self.target = target

    def call(self, stage, command, cwd, category="infrastructure", path_prepend=None, env_patch=None, input_data=None):
        item = {"stage": stage, "command": [str(x) for x in command],
                "cwd": str(cwd), "category": category}
        if path_prepend is not None:
            item["path_prepend"] = str(path_prepend)
        if input_data is not None:
            item["fixture_input"] = input_data.decode("utf-8")
        print(f"{self.target['role']}: {stage}", flush=True)
        try:
            completed = run(command, cwd, path_prepend=path_prepend, env_patch=env_patch, input_data=input_data)
            data = completed.stdout
            item["returncode"] = completed.returncode
        except OSError as exc:
            data = str(exc).encode("utf-8")
            item["returncode"] = None
            item["launch_error"] = str(exc)
        log = f"{len(self.target['steps']):02d}-{stage}.log"
        (self.directory / log).write_bytes(data)
        item["log"] = log
        self.target["steps"].append(item)
        write_json(self.directory / "result.json", self.target)
        return item["returncode"] == 0, data.decode("utf-8", errors="replace").strip()


def checkout(steps, repository, ref, destination, cwd, prefix="target"):
    for stage, command, directory in [
        ("init", ["git", "init", str(destination)], cwd),
        ("remote", ["git", "remote", "add", "origin", repository], destination),
        ("fetch", ["git", "fetch", "--no-tags", "origin", ref], destination),
        ("checkout", ["git", "checkout", "--detach", "FETCH_HEAD"], destination),
    ]:
        if not steps.call(f"{prefix}-{stage}", command, directory)[0]:
            return None
    ok, sha = steps.call(f"{prefix}-sha", ["git", "rev-parse", "HEAD"], destination)
    return sha if ok else None


def find_bash():
    if os.name != "nt":
        return shutil.which("bash")
    git = shutil.which("git")
    if git:
        root = Path(git).resolve().parent.parent
        for candidate in (root / "bin/bash.exe", root / "usr/bin/bash.exe"):
            if candidate.is_file():
                return str(candidate)
    return None


def environment(driver):
    details = {"platform": platform.platform(), "python": sys.version,
               "executable": sys.executable, "utf8_mode": sys.flags.utf8_mode,
               "filesystem_encoding": sys.getfilesystemencoding(),
               "preferred_encoding": locale.getpreferredencoding(False),
               "locale": locale.setlocale(locale.LC_ALL, None),
               "settings": {key: os.environ.get(key) for key in
                            ("ImageOS", "ImageVersion", "RUNNER_OS", "RUNNER_ARCH",
                             "LANG", "LC_ALL", "PYTHONUTF8", "PYTHONIOENCODING")},
               "tools": {}}
    for name, command in {"git": ["git", "--version"], "node": ["node", "--version"],
                          "npm": [shutil.which("npm") or "npm", "--version"]}.items():
        try:
            result = run(command, driver)
            details["tools"][name] = {"returncode": result.returncode,
                                      "output": result.stdout.decode("utf-8", "replace").strip()}
        except OSError as exc:
            details["tools"][name] = {"launch_error": str(exc)}
    return details


def smoke(steps, target, workspace, python, bash, sha):
    lock = json.loads((target / "trellis/presets/guru-team/source/trellis-source.json").read_text(encoding="utf-8"))
    steps.target["source_lock"] = lock
    fork = workspace / "fork"
    fork_sha = checkout(steps, lock["repository"], lock["commit"], fork, workspace, "fork")
    if fork_sha != lock["commit"]:
        raise RuntimeError("Fork checkout did not resolve the target source lock")
    ok, tree = steps.call("fork-tree", ["git", "rev-parse", "HEAD^{tree}"], fork)
    ok_parents, parents = steps.call("fork-parents", ["git", "show", "-s", "--format=%P", "HEAD"], fork)
    if not ok or not ok_parents or tree != lock["tree"] or parents.split() != lock["parents"]:
        raise RuntimeError("Fork tree/parents differ from the target source lock")
    package = json.loads((fork / "package.json").read_text(encoding="utf-8"))
    manager = package["packageManager"]
    if manager.split("+", 1)[0] != lock["package_manager"]:
        raise RuntimeError("Fork package manager differs from the target source lock")
    tools = workspace / "tools"
    npm = shutil.which("npm") or "npm"
    if not steps.call("pnpm-install", [npm, "install", "--prefix", tools,
                                       "--no-audit", "--no-fund", manager.split("+", 1)[0]], workspace)[0]:
        return
    pnpm = ["node", tools / "node_modules/pnpm/bin/pnpm.cjs"]
    pnpm_bin = tools / "node_modules/.bin"
    commands = [("pnpm-version", pnpm + ["--version"]),
                ("fork-dependencies", pnpm + ["install", "--frozen-lockfile"]),
                ("fork-core-build", pnpm + ["--filter", "@mindfoldhq/trellis-core", "build"]),
                ("fork-cli-build", pnpm + ["--filter", "@mindfoldhq/trellis", "build"])]
    for stage, command in commands:
        if not steps.call(stage, command, fork, path_prepend=pnpm_bin)[0]:
            return
    steps.call("fork-dependency-versions", pnpm + ["list", "--recursive", "--depth", "0", "--json"],
               fork, path_prepend=pnpm_bin)
    (fork / "packages/cli/dist/.guru-source-commit").write_text(fork_sha + "\n", encoding="utf-8")
    clean = workspace / "中文 clean install"
    steps.target["clean_install_root"] = str(clean)
    if not steps.call("smoke-git-init", ["git", "init", clean], workspace)[0]:
        return
    cli = fork / "packages/cli/bin/trellis.js"
    ok, version = steps.call("fork-cli-version", ["node", cli, "--version"], fork)
    if not ok or version.splitlines()[0] != lock["cli_version"]:
        raise RuntimeError("Built Fork CLI version differs from the target source lock")
    provider = f"gh:castbox/guru-trellis/trellis#{sha}"
    if not steps.call("smoke-cli-init", ["node", cli, "init", "-y", "--codex", "--workflow",
                                         "guru-team", "--workflow-source", provider], clean, "installation")[0]:
        return
    # Bash receives POSIX separators, including drive-prefixed Windows paths.
    apply = target / "trellis/presets/guru-team/scripts/bash/apply.sh"
    if not steps.call("smoke-preset", [bash, apply.as_posix(), "--repo", clean.as_posix(),
                                       "--platform", "codex", "--python", python.as_posix()], target, "installation")[0]:
        return
    required = [clean / ".trellis/workflow.md", clean / ".trellis/guru-team/extension.json"]
    if any(not path.is_file() for path in required):
        raise RuntimeError("Clean installation returned success without workflow or Guru manifest")
    validator = clean / ".trellis/guru-team/scripts/bash/check-skill-packages.sh"
    steps.call("smoke-installed-validation", [bash, validator.as_posix(), "--root", clean.as_posix(),
                                              "--mode", "installed", "--json"], clean, "installation")
    steps.call("smoke-installed-wrapper", [python, HERE / "runtime_diagnostic.py", "--target-root", target,
               "--installed-root", clean, "--python", python,
               "--output", steps.directory / "installed-wrapper.json"], clean, "installation")
    eol_driver = HERE.parent / TEST_ROOT / "test_managed_text_eol.py"
    eol_report = steps.directory / "native-eol.json"
    steps.call("native-eol", [python, HERE / "unittest_report.py", "--root", eol_driver.parent,
               "--output", eol_report,
               str(eol_driver) + "::ManagedTextInstallTests.test_real_install_clone_validate_reapply"],
               target, "tests", env_patch={"GURU_NATIVE_TARGET_ROOT": str(target),
               "GURU_UPSTREAM_DELIVERY_SCRIPTS": str(clean / ".trellis/scripts"), "PYTHONUTF8": "0"})
    if eol_report.exists():
        steps.target["native_eol"] = json.loads(eol_report.read_text(encoding="utf-8"))
    # The driver owns this harness; every product entry below belongs to target.
    from native_maintenance import maintain
    maintain(steps, target, clean, workspace, python, bash, cli, provider)


def execute_target(repository, role, ref, workspace, diagnostics, selections, bash):
    workspace.mkdir(parents=True)
    diagnostics.mkdir(parents=True)
    result = {"role": role, "requested_ref": ref, "workspace": str(workspace),
              "steps": [], "status": "incomplete"}
    steps = Steps(diagnostics, result)
    try:
        target = workspace / "target"
        sha = checkout(steps, repository, ref, target, workspace)
        result["sha"] = sha
        if not sha:
            return result
        for name in ("core.autocrlf", "core.eol"):
            steps.call("git-" + name, ["git", "config", "--get", name], target, "observation")
        venv = workspace / "python"
        ready = steps.call("python-venv", [sys.executable, "-m", "venv", venv], workspace)[0]
        python = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        lock = target / "trellis/skills/guru-team/runtime/requirements.lock"
        if ready:
            ready = steps.call("python-dependencies", [python, "-m", "pip", "install", "--require-hashes",
                                                       "-r", lock], target)[0]
        if ready:
            steps.call("python-versions", [python, "-m", "pip", "list", "--format=json"], target)
            steps.call("native-python-encoding", [python, "-c",
                       "import codecs,json,locale,os,sys; encoding=locale.getpreferredencoding(False); print(json.dumps({'executable':sys.executable,'utf8_mode':sys.flags.utf8_mode,'preferred_encoding':encoding})); sys.exit(1 if os.name=='nt' and (sys.flags.utf8_mode or codecs.lookup(encoding).name=='utf-8') else 0)"],
                       target, env_patch={"PYTHONUTF8": "0"})
            outcome = diagnostics / "unittest.json"
            steps.call("tests", [python, HERE / "unittest_report.py", "--root", target / TEST_ROOT,
                                 "--output", outcome, *selections], target, "tests")
            if outcome.exists():
                result["tests"] = json.loads(outcome.read_text(encoding="utf-8"))
            native = diagnostics / "native-compatibility.json"
            native_driver = HERE.parent / TEST_ROOT / "test_runtime_native_compatibility.py"
            steps.call("native-compatibility", [python, HERE / "unittest_report.py",
                       "--root", native_driver.parent, "--output", native, native_driver],
                       target, "tests", env_patch={"GURU_NATIVE_TARGET_ROOT": str(target), "PYTHONUTF8": "0"})
            if native.exists():
                result["native_compatibility"] = json.loads(native.read_text(encoding="utf-8"))
            diagnostic = diagnostics / "runtime-diagnostic.json"
            result["runtime_diagnostic"] = {"report": diagnostic.name}
            steps.call("runtime-diagnostic", [python, HERE / "runtime_diagnostic.py",
                       "--target-root", target, "--python", python, "--output", diagnostic], target)
            if diagnostic.exists():
                observed = json.loads(diagnostic.read_text(encoding="utf-8"))
                result["runtime_diagnostic"].update(
                    collector_status=observed["collector_status"],
                    fixture_status=observed.get("fixture_status", "not_executed"))
        else:
            result["runtime_diagnostic"] = {"collector_status": "not_executed",
                                            "reason": "Target Python dependencies unavailable"}
        # Tests and installation are independent; always attempt the latter.
        if bash:
            ok, uname = steps.call("bash-uname", [bash, "-c", "uname -s; bash --version"], target)
            if not ok or (os.name == "nt" and not uname.startswith(("MINGW", "MSYS"))):
                raise RuntimeError("Native Git for Windows Bash is required on Windows")
            smoke(steps, target, workspace, python if ready else Path(sys.executable), bash, sha)
        else:
            raise RuntimeError("Bash unavailable; clean installation not executed")
        failures = [item for item in result["steps"] if item["category"] != "observation" and item["returncode"] != 0]
        result["status"] = "failed" if failures else "passed"
    except (OSError, ValueError, KeyError, RuntimeError) as exc:
        result["execution_error"] = str(exc)
        result["status"] = "infrastructure_failed"
    finally:
        write_json(diagnostics / "result.json", result)
    return result


def baseline_matches(target, test_id, message):
    tests = target.get("tests", {})
    outcomes = tests.get("outcomes", [])
    failures = [row for row in target["steps"] if row["category"] != "observation" and row["returncode"] != 0]
    return bool(test_id and message and target["status"] == "failed" and tests.get("tests_run")
                and not tests.get("errors") and not tests.get("skips") and not tests.get("expected_failures")
                and failures and all(row["stage"] == "tests" for row in failures)
                and outcomes and all(row == {"id": test_id, "kind": "failure", "message": message}
                                     for row in outcomes))


def summarize(report, expected_test, expected_message):
    candidate = next((row for row in report["targets"] if row["role"] == "candidate"), {})
    baseline = next((row for row in report["targets"] if row["role"] == "baseline"), None)
    matched = baseline is not None and baseline_matches(baseline, expected_test, expected_message)
    comparison = bool(matched and candidate.get("status") == "passed")
    report["comparison"] = {"expected_test": expected_test, "expected_message": expected_message,
                            "baseline_matched": matched, "established": comparison}
    success = candidate.get("status") == "passed" and (baseline is None or baseline["status"] == "passed" or matched)
    report["returncode"] = 0 if success else 1
    lines = ["# Native targeted CI", "", f"Driver: `{report['driver_sha']}`", "",
             "| Target | SHA | Status |", "| --- | --- | --- |"]
    for target in report["targets"]:
        lines.append(f"| {target['role']} | `{target.get('sha', 'unresolved')}` | {target['status']} |")
        for step in target["steps"]:
            if step["category"] != "observation" and step["returncode"] != 0:
                lines.append(f"\n{target['role']}: `{step['stage']}` exit `{step['returncode']}`; see `{target['role']}/{step['log']}`.")
        if target.get("execution_error"):
            lines.append(f"\n{target['role']}: execution error: {target['execution_error']}")
    lines.extend(["", f"Specified baseline assertion matched: {matched}.",
                  f"Failure/fix comparison established: {comparison}.",
                  "", "Cancelled, missing or unexecuted evidence is incomplete."])
    return "\n".join(lines) + "\n"


def execute_targets(report, repository, targets, work_root, output, selections, bash):
    for role, ref in targets:
        report["targets"].append(execute_target(repository, role, ref, work_root / role,
                                                 output / role, selections, bash))
        write_json(output / "report.json", report)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--work-root", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    driver = HERE.parent
    report = {"driver_sha": run(["git", "rev-parse", "HEAD"], driver).stdout.decode().strip(),
              "event": os.environ.get("CI_EVENT"), "source_ref": os.environ.get("CI_SOURCE_REF"),
              "environment": environment(driver), "targets": []}
    write_json(output / "report.json", report)
    repository = run(["git", "remote", "get-url", "origin"], driver).stdout.decode().strip()
    # The public CI repository needs no authenticated Git transport.
    if os.environ.get("GITHUB_REPOSITORY"):
        repository = "https://github.com/" + os.environ["GITHUB_REPOSITORY"] + ".git"
    targets = []
    if os.environ.get("CI_BASELINE"):
        targets.append(("baseline", os.environ["CI_BASELINE"]))
    targets.append(("candidate", os.environ.get("CI_CANDIDATE") or report["driver_sha"]))
    selections = shlex.split(os.environ.get("CI_TESTS", "test_guru_platform_inventory.py"))
    bash = find_bash()
    report["environment"]["bash"] = bash
    execute_targets(report, repository, targets, args.work_root.resolve(), output, selections, bash)
    summary = summarize(report, os.environ.get("CI_EXPECTED_TEST", ""), os.environ.get("CI_EXPECTED_MESSAGE", ""))
    write_json(output / "report.json", report)
    (output / "summary.md").write_text(summary, encoding="utf-8")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as stream:
            stream.write(summary)
    print(summary)
    return report["returncode"]


if __name__ == "__main__":
    sys.exit(main())
