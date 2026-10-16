"""Opt-in #588 experiment, not a timing assertion in the regression suite.

Run with the managed interpreter and explicit GURU_UPSTREAM_DELIVERY_SCRIPTS.
--source selects the unchanged fixture source; --package-root optionally selects
an installed package's real wrappers. JSON outputs belong outside the source.
Fixture semantic inputs exercise deterministic transport, not native AI review.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import time


def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=root, text=True,
                          capture_output=True, check=True).stdout.strip()


def trace_counts(path: Path, offset: int) -> tuple[int, int, int]:
    git_count = cat_count = scans = 0
    with path.open() as stream:
        stream.seek(offset)
        for line in stream:
            event = json.loads(line)
            if event.get("event") == "start":
                argv = event.get("argv", [])
                git_count += 1
                cat_count += "cat-file" in argv
                scans += "ls-files" in argv
    return git_count, cat_count, scans


def digest_sample(package: Path, repo: Path) -> dict:
    # A fresh Python process provides SELF and completed-child RSS separately.
    skills = package.parents[2] if "/.trellis/" in package.as_posix() else package.parents[1]
    code = """import sys,time,json,resource
from pathlib import Path
sys.path.insert(0,sys.argv[1]);sys.path.insert(0,sys.argv[2])
import common
start=time.perf_counter();value=common.index_tree_digest(Path(sys.argv[3]))
print(json.dumps({'digest':value,'seconds':time.perf_counter()-start,
 'python_maxrss':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
 'git_child_maxrss':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}))
"""
    process = subprocess.run([sys.executable, "-c", code, str(skills),
                              str(package / "runtime"), str(repo)],
                             text=True, capture_output=True, check=True)
    return json.loads(process.stdout)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True)
    parser.add_argument("--package-root")
    parser.add_argument("--output", required=True)
    parser.add_argument("--kind", choices=("duplicates", "unique"), required=True)
    parser.add_argument("--repeats", type=int, default=2)
    parser.add_argument("--digest-only", action="store_true")
    args = parser.parse_args()
    source = Path(args.source).resolve()
    fixture_package = source / "trellis/skills/guru-team/packages/guru-reconcile-task-base"
    package = Path(args.package_root).resolve() if args.package_root else fixture_package
    sys.path.insert(0, str(fixture_package / "tests"))
    import test_runtime as fixture

    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    reports = []
    for sample in range(args.repeats):
        test = fixture.RuntimeTest()
        test.setUp()
        try:
            assets = test.repo / "assets"
            assets.mkdir()
            for number in range(10000):
                value = number % 64 if args.kind == "duplicates" else number
                content = hashlib.sha256(str(value).encode()).digest() * 512
                (assets / f"{number:05}.bin").write_bytes(content)
            (assets / "large.bin").write_bytes(bytes(range(256)) * 65536)
            test.git("add", "assets")
            test.git("commit", "-qm", "normal benchmark assets")
            test.head = test.git("rev-parse", "HEAD")
            report = {"kind": args.kind, "sample": sample,
                      "source_head": git(source, "rev-parse", "HEAD"),
                      "package_source_sha256": {name: hashlib.sha256((package / "runtime" / name).read_bytes()).hexdigest()
                                                for name in ("common.py", "invoke.py")},
                      "installation_kind": "installed" if args.package_root else "canonical",
                      "environment": {"os": platform.platform(), "python": platform.python_version(),
                                      "git": git(source, "--version")},
                      "files": 10004, "asset_files": 10001,
                      "unique_asset_blobs": 65 if args.kind == "duplicates" else 10001,
                      "unique_asset_bytes": (64 if args.kind == "duplicates" else 10000) * 16384 + 16777216,
                      "asset_bytes": 10000 * 16384 + 16777216,
                      "largest_blob_bytes": 16777216}
            if args.digest_only:
                report.update(digest_sample(package, test.repo))
            else:
                trace = output / f"{args.kind}-{sample}-git.jsonl"
                if trace.exists():
                    raise RuntimeError("Use a fresh output directory; do not append earlier traces.")
                stages = []

                def call(script: str, *argv: str) -> dict:
                    offset = trace.stat().st_size if trace.exists() else 0
                    env = {**os.environ, "GIT_TRACE2_EVENT": str(trace), "GIT_TERMINAL_PROMPT": "0"}
                    start = time.perf_counter()
                    proc = subprocess.run(["/usr/bin/time", "-l", "bash", str(package / "scripts" / script),
                                           "--root", str(test.repo), *argv, "--json"],
                                          cwd=source, text=True, capture_output=True, env=env)
                    elapsed = time.perf_counter() - start
                    if proc.returncode:
                        raise RuntimeError(script + " " + proc.stdout + " " + proc.stderr)
                    rss = re.search(r"(\d+)\s+maximum resident set size", proc.stderr)
                    counts = trace_counts(trace, offset)
                    stages.append({"stage": script, "seconds": elapsed,
                                   "maxrss_bytes": int(rss.group(1)) if rss else None,
                                   "git_processes": counts[0], "cat_file_processes": counts[1],
                                   "index_scans": counts[2]})
                    print(json.dumps({"sample": sample, "kind": args.kind, **stages[-1]}), flush=True)
                    value = json.loads(proc.stdout)
                    return value["result"] if value.get("formal_exit") is False else value

                request = {"task_head": test.head, "new_base_head": test.new,
                           "validation_commands": [["git", "diff", "--quiet"]]}
                candidate = call("execute-base-candidate.sh", "--request", str(test.write("candidate.json", request)))
                digest = candidate["candidate_tree_sha256"]
                public = test.public("delivery_post_plan")
                request = {"profile": "delivery_post_plan", "task_ref": test.task_ref, "delivery_key": test.delivery_key,
                           "branch": "feature", "prior_task_head": test.head, "selected_base_ref": test.new,
                           "old_base_head": test.old, "new_base_head": test.new, "resume_target": public["resume_target"],
                           "candidate_tree_sha256": digest, "commit_message": "chore(base): benchmark normal reconciliation"}
                receipt = call("execute-base-reconciliation.sh", "--request", str(test.write("reconcile.json", request)))
                recorded = call("record-base-reconciliation.sh", "--skill-input", str(test.write("public.json", public)),
                                "--semantic-review-file", str(test.write("fixture-semantic.json", test.gate(digest))),
                                "--typed-exit", "reconciled", "--reconciliation-result", str(test.write("receipt.json", receipt)))
                checked = call("check-base-reconciliation.sh", "--input", str(test.write("recorded.json", recorded)),
                               "--expected-exit", "reconciled")
                result = call("invoke.sh", "--invocation", str(test.write("invoke.json", {"public_input": public, "owner_result": recorded})))
                assert result["exit_id"] == "reconciled" and checked["status"] == "ok"
                from common import checkpoint_path
                assert not checkpoint_path(test.repo, test.task_ref, delivery_key=test.delivery_key).exists()
                report.update(stages=stages, total_seconds=sum(row["seconds"] for row in stages),
                              cat_file_processes=sum(row["cat_file_processes"] for row in stages),
                              git_processes=sum(row["git_processes"] for row in stages),
                              digest=digest, formal_exit=result["exit_id"], checkpoint_consumed=True)
            reports.append(report)
            (output / "summary.json").write_text(json.dumps(reports, ensure_ascii=False, indent=2) + "\n")
            print(json.dumps({"sample_complete": report}, ensure_ascii=False), flush=True)
        finally:
            test.tearDown()


if __name__ == "__main__":
    main()
