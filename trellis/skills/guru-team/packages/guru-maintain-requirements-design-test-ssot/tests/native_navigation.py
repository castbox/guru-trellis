"""Collect native navigation observations; never author a semantic result.

Run roots and raw traces stay outside the source checkout. An installed snapshot
is copied, never installed by this helper. The caller supplies the actual owner
prompt and reviews its output. Git observations are not a semantic pass.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
from pathlib import Path
import shutil
import subprocess


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)


def observe(root: Path) -> dict:
    return {"head": git(root, "rev-parse", "HEAD").stdout.strip(),
            "status": git(root, "status", "--porcelain=v1", "--untracked-files=all").stdout,
            "diff": git(root, "diff", "--stat").stdout,
            "changed_paths": git(root, "diff", "--name-only", "HEAD").stdout.splitlines(),
            "untracked_paths": git(root, "ls-files", "--others", "--exclude-standard").stdout.splitlines()}


def clone(args: argparse.Namespace) -> None:
    snapshot = Path(args.snapshot).resolve()
    target = Path(args.target).resolve()
    if git(snapshot, "status", "--porcelain=v1").stdout:
        raise SystemExit("Commit the snapshot before cloning it.")
    result = subprocess.run(["git", "clone", "--no-hardlinks", str(snapshot), str(target)],
                            capture_output=True, text=True)
    if result.returncode:
        raise SystemExit(result.stderr)
    # A new fixture has its own registry and session. Preserve committed history
    # and installed bytes, without copying another checkout's private controls.
    result = git(target, "switch", "-C", "main", "HEAD")
    if result.returncode:
        raise SystemExit(result.stderr)
    interpreter_selection = snapshot / ".trellis/.runtime/guru-team/python"
    if interpreter_selection.exists():
        shutil.copytree(interpreter_selection, target / ".trellis/.runtime/guru-team/python")
    if args.branch:
        result = git(target, "switch", "-c", args.branch)
        if result.returncode:
            raise SystemExit(result.stderr)
    print(json.dumps({"repository": str(target), "observation": observe(target)}, ensure_ascii=False))


def run(args: argparse.Namespace) -> None:
    root, output = Path(args.repository).resolve(), Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    prompt = Path(args.prompt).read_bytes()
    (output / "prompt.md").write_bytes(prompt)
    argv = ["codex", "exec", "--ephemeral", "--json", "--color", "never",
            "--dangerously-bypass-approvals-and-sandbox", "-C", str(root),
            "-o", str(output / "last-message.md"), "-"]
    if args.model:
        argv[2:2] = ["--model", args.model]
    write_json(output / "invocation.json", {"argv": argv, "started_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "codex_version": subprocess.run(["codex", "--version"], capture_output=True, text=True).stdout.strip(),
               "before": observe(root)})
    with (output / "events.jsonl").open("wb") as stdout, (output / "stderr.log").open("wb") as stderr:
        result = subprocess.run(argv, input=prompt, stdout=stdout, stderr=stderr,
                                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    write_json(output / "completion.json", {"returncode": result.returncode, "after": observe(root)})
    print(json.dumps({"output": str(output), "returncode": result.returncode}))


def collect(args: argparse.Namespace) -> None:
    root, output = Path(args.repository).resolve(), Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    write_json(output / "observation.json", observe(root))
    (output / "worktree.diff").write_text(git(root, "diff", "--binary", "HEAD").stdout)
    paths = git(root, "ls-files", "--others", "--exclude-standard").stdout.splitlines()
    for name in paths:
        source = root / name
        if source.is_file():
            target = output / "untracked" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    print(output)


def merge(args: argparse.Namespace) -> None:
    root, output = Path(args.repository).resolve(), Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    base = git(root, "merge-base", args.a, args.b)
    if base.returncode:
        raise SystemExit(base.stderr)
    baseline = base.stdout.strip()
    paths = {}
    for label, commit in (("A", args.a), ("B", args.b)):
        paths[label] = git(root, "diff", "--name-only", baseline, commit).stdout.splitlines()
        (output / f"{label}.diff").write_text(git(root, "diff", "--binary", baseline, commit).stdout)
    observations = {"base": baseline, "a": args.a, "b": args.b, "changed_paths": paths,
                    "overlapping_paths": sorted(set(paths["A"]) & set(paths["B"])), "orders": {}}
    for label, first, second in (("A-then-B", args.a, args.b), ("B-then-A", args.b, args.a)):
        result = git(root, "merge-tree", "--write-tree", first, second)
        (output / f"{label}.stdout").write_text(result.stdout)
        (output / f"{label}.stderr").write_text(result.stderr)
        tree = result.stdout.splitlines()[0] if result.stdout else ""
        observations["orders"][label] = {"returncode": result.returncode, "tree": tree}
        if tree:
            (output / f"{label}.files").write_text(git(root, "ls-tree", "-r", tree).stdout)
    write_json(output / "merge-observations.json", observations)
    print(json.dumps(observations, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    copy = commands.add_parser("clone-installed")
    copy.add_argument("--snapshot", required=True)
    copy.add_argument("--target", required=True)
    copy.add_argument("--branch")
    copy.set_defaults(action=clone)
    native = commands.add_parser("run")
    for name in ("repository", "prompt", "output"):
        native.add_argument("--" + name, required=True)
    native.add_argument("--model")
    native.set_defaults(action=run)
    capture = commands.add_parser("collect")
    capture.add_argument("--repository", required=True)
    capture.add_argument("--output", required=True)
    capture.set_defaults(action=collect)
    combine = commands.add_parser("merge")
    for name in ("repository", "a", "b", "output"):
        combine.add_argument("--" + name, required=True)
    combine.set_defaults(action=merge)
    args = parser.parse_args()
    args.action(args)


if __name__ == "__main__":
    main()
