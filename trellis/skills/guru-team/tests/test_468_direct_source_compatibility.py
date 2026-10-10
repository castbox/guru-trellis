"""Formal-wrapper transport for portable Direct Source and legal no-Issue tasks.

Semantic decisions are test preconditions. These tests observe the existing
owners' handoffs and side effects; they do not classify Issue prose or prove a
native AI review, full task lifecycle, or live GitHub closure.
"""

from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


SOURCE = Path(__file__).resolve().parents[4]
PACKAGES = SOURCE / "trellis/skills/guru-team/packages"


def git(root: Path, *arguments: str) -> str:
    return subprocess.run(["git", *arguments], cwd=root, text=True,
                          capture_output=True, check=True).stdout.strip()


def invoke(root: Path, skill: str, public: dict, semantic: dict | None = None,
           *, env: dict | None = None, confirmed: bool = False) -> dict:
    input_path = root / "input.json"
    input_path.write_text(json.dumps(public), encoding="utf-8")
    argv = ["bash", str(PACKAGES / skill / "scripts/invoke.sh"),
            "--root", str(root), "--input", str(input_path)]
    if semantic is not None:
        semantic_path = root / "review.json"
        semantic_path.write_text(json.dumps(semantic), encoding="utf-8")
        argv.extend(["--semantic-result", str(semantic_path)])
    if confirmed:
        argv.append("--confirmed-close")
    result = subprocess.run(argv, cwd=SOURCE, capture_output=True, text=True,
                            env=env, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout)


def repository(root: Path, source: dict) -> tuple[Path, str, dict]:
    git(root, "init", "-q", "-b", "main")
    git(root, "config", "user.email", "fixture@example.com")
    git(root, "config", "user.name", "Fixture")
    (root / ".gitignore").write_text(".trellis/.runtime/\ninput.json\nreview.json\nbin/\nprovider*\n")
    git(root, "add", ".gitignore")
    git(root, "commit", "-qm", "fixture base")
    # A real local Delivery merge supplies the observed Git identities below.
    git(root, "switch", "-qc", "fixture-delivery")
    (root / "delivery.txt").write_text("bounded fixture work\n")
    git(root, "add", "delivery.txt")
    git(root, "commit", "-qm", "fixture delivery")
    reviewed_head = git(root, "rev-parse", "HEAD")
    git(root, "switch", "-q", "main")
    git(root, "merge", "--no-ff", "-qm", "fixture merge", "fixture-delivery")
    merge_head = git(root, "rev-parse", "HEAD")
    (root / ".trellis").mkdir()
    creation_source = copy.deepcopy(source)
    if creation_source.get("disposition") in {"follow_up", "parent"}:
        # Current creation supports exact/reference. These two published
        # read-only relations are legal existing metadata, not creation exits.
        creation_source["disposition"] = "reference_only"
    created = subprocess.run([
        sys.executable, str(SOURCE / ".trellis/scripts/task.py"), "create",
        "Portable source fixture", "--slug", "source-fixture", "--task-id", "source-fixture",
        "--description", "Only bounded fixture work is accepted scope",
        "--source-json", json.dumps(creation_source), "--base-branch", "main", "--no-start",
    ], cwd=root, text=True, capture_output=True, check=False)
    assert created.returncode == 0, created.stdout + created.stderr
    task_file = next((root / ".trellis/tasks").glob("*/task.json"))
    if creation_source != source:
        metadata = json.loads(task_file.read_text())
        metadata["source"] = source
        task_file.write_text(json.dumps(metadata))
    task_ref = task_file.parent.relative_to(root).as_posix()
    # These are ordinary informational links, not a second structured source.
    (task_file.parent / "prd.md").write_text(
        "Accepted scope: bounded fixture work.\n"
        "Coordination: coord/project#20 (information only).\n"
        "Related work: related/service#30 (information only).\n"
        "Follow-up: later/work#40 (outside accepted scope).\n")
    started = subprocess.run([
        sys.executable, str(SOURCE / ".trellis/scripts/task.py"), "start", task_ref,
        "--allow-empty-context",
    ], cwd=root, text=True, capture_output=True, check=False)
    assert started.returncode == 0, started.stdout + started.stderr
    git(root, "add", ".trellis/tasks")
    git(root, "commit", "-qm", "current task facts")
    merge = {"task_id": "source-fixture", "task_ref": task_ref, "lifecycle_generation": 0,
             "delivery_cycle_ref": "fixture:delivery", "repo_ref": "execution/repository",
             "pr_number": 1, "reviewed_head": reviewed_head, "merge_commit_sha": merge_head,
             "result_id": "fixture:merge"}
    return task_file, task_ref, merge


def provider(root: Path) -> tuple[dict, Path, Path]:
    bin_dir = root / "bin"
    bin_dir.mkdir()
    script = bin_dir / "gh"
    script.write_text(
        "#!/usr/bin/env python3\n"
        "import json, os, pathlib, sys\n"
        "args = sys.argv[1:]\n"
        "with pathlib.Path(os.environ['PROVIDER_LOG']).open('a') as f: f.write(json.dumps(args)+'\\n')\n"
        "repo = args[args.index('--repo') + 1]\n"
        "key = repo + '#' + args[2]\n"
        "path = pathlib.Path(os.environ['PROVIDER_STATE'])\n"
        "states = json.loads(path.read_text())\n"
        "if args[:2] == ['issue', 'view']: print(states[key])\n"
        "elif args[:2] == ['issue', 'close']:\n"
        "    states[key] = 'CLOSED'; path.write_text(json.dumps(states))\n"
        "else: sys.exit(2)\n")
    script.chmod(0o755)
    states = root / "provider-state.json"
    states.write_text(json.dumps({"source/other-repository#17": "OPEN",
                                 "coord/project#20": "OPEN", "related/service#30": "OPEN",
                                 "later/work#40": "OPEN"}))
    log = root / "provider-log.jsonl"
    env = {**os.environ, "PATH": str(bin_dir) + os.pathsep + os.environ["PATH"],
           "PROVIDER_STATE": str(states), "PROVIDER_LOG": str(log)}
    return env, states, log


@pytest.mark.parametrize("source", [
    {"kind": "issue", "repo_ref": "source/other-repository", "number": 17,
     "disposition": "exact_source"},
    {"kind": "no_issue"},
    *({"kind": "issue", "repo_ref": "source/other-repository", "number": 17,
       "disposition": role} for role in ("reference_only", "follow_up", "parent")),
], ids=["cross-repository-source", "no-issue", "reference-only", "follow-up", "parent"])
def test_formal_source_completion_closure_preserves_identity_and_issue_purpose(tmp_path, source):
    task_file, task_ref, merge = repository(tmp_path, source)
    before = task_file.read_bytes()
    head = git(tmp_path, "rev-parse", "HEAD")
    branch = git(tmp_path, "branch", "--show-current")
    identity = invoke(tmp_path, "guru-establish-task-identity", {
        "profile": "active_task", "mode": "workflow", "task_id": "source-fixture",
        "task_ref": task_ref, "lifecycle_generation": 0,
    })
    assert identity["exit_id"] == "identity_established"
    assert identity["source"] == source
    assert task_file.read_bytes() == before

    slots = {"planning": "fixture:planning", "delivery_review": "fixture:review",
             "delivery_publication": "fixture:publication"}
    # Explicit, already-selected semantic fixture: all accepted work is done;
    # the informational links above have no required evidence or work role.
    completed = invoke(tmp_path, "guru-review-task-completion", {
        "profile": "completion", "mode": "workflow",
        "task_artifact": {"task_id": "source-fixture", "task_ref": task_ref, "lifecycle_generation": 0},
        "accepted_scope_identity": "fixture:scope", "merge_result": merge, "evidence_slots": slots,
    }, {"profile": "completion", "mode": "workflow", "reviewed_scope_identity": "fixture:scope",
        "reviewed_merge_result_id": merge["result_id"], "reviewed_evidence_slots": slots,
        "remaining_work_refs": [], "route": {"typed_exit": "completed"}})
    assert completed["exit_id"] == "completed"
    can_close = source.get("disposition") == "exact_source"
    actions = [] if source["kind"] == "no_issue" else [
        {"issue_ref": {"repo_ref": source["repo_ref"], "issue_number": source["number"]},
         "disposition": "close" if can_close else "no_close_authority"},
        {"issue_ref": {"repo_ref": "coord/project", "issue_number": 20}, "disposition": "no_close_authority"},
        {"issue_ref": {"repo_ref": "related/service", "issue_number": 30}, "disposition": "no_close_authority"},
        {"issue_ref": {"repo_ref": "later/work", "issue_number": 40}, "disposition": "no_close_authority"},
    ]
    env, states, log = provider(tmp_path)
    closure_input = {
        "profile": "completion_approved", "source_exit": completed["exit_id"], "mode": "workflow",
        "completion_result": completed["result_ref"], "source": identity["source"],
        "accepted_scope_identity": "fixture:scope",
        "delivery_target": {"repo_ref": "execution/repository", "branch_ref": branch},
        "binding_ref": {"task_id": "source-fixture", "lifecycle_generation": 0, "binding_revision": 0},
        "content_head": head, "evidence_slots": {"completion": completed["result_ref"]["result_id"]},
        "action_set": actions,
    }
    closure_review = {"profile": "completion_approved", "mode": "workflow", "reviewed_action_set": actions,
                      "route": {"typed_exit": "apply"}}
    closed = invoke(tmp_path, "guru-complete-task-closure", closure_input,
                    closure_review, env=env, confirmed=can_close)
    assert closed["exit_id"] == ("closed" if can_close else "no_mutation")
    assert closed["result_ref"]["task_id"] == "source-fixture"
    assert closed["result_ref"]["lifecycle_generation"] == 0
    assert task_file.read_bytes() == before
    assert git(tmp_path, "rev-parse", "HEAD") == head
    assert git(tmp_path, "branch", "--show-current") == branch
    observed = json.loads(states.read_text())
    assert all(observed[key] == "OPEN" for key in ("coord/project#20", "related/service#30", "later/work#40"))
    if not can_close:
        assert not log.exists()
        assert observed["source/other-repository#17"] == "OPEN"
    else:
        calls = [json.loads(line) for line in log.read_text().splitlines()]
        assert [call[:3] for call in calls] == [["issue", "view", "17"], ["issue", "close", "17"], ["issue", "view", "17"]]
        assert all(call[call.index("--repo") + 1] == "source/other-repository" for call in calls)
        assert observed["source/other-repository#17"] == "CLOSED"
        # Genuine output loss recovers the completed original transaction.
        transaction_path = tmp_path / ".git/guru-team/closure/source-fixture/0.json"
        transaction = transaction_path.read_bytes()
        recovered = invoke(tmp_path, "guru-complete-task-closure", closure_input, closure_review, env=env)
        assert recovered == closed
        assert transaction_path.read_bytes() == transaction
        # A normal external reopen returns to that closeout owner, without
        # recreating the task, advancing generation, or re-closing the Issue.
        observed["source/other-repository#17"] = "OPEN"
        states.write_text(json.dumps(observed))
        reopened = invoke(tmp_path, "guru-complete-task-closure", closure_input, closure_review, env=env)
        assert reopened["exit_id"] == "external_change_conflict"
        assert reopened["reason"]["reason_code"] == "required_closed_issue_reopened"
        assert reopened["transaction_ref"]["result_id"] == closed["result_ref"]["result_id"]
        assert transaction_path.read_bytes() == transaction
        assert task_file.read_bytes() == before
        all_calls = [json.loads(line) for line in log.read_text().splitlines()]
        assert sum(call[:2] == ["issue", "close"] for call in all_calls) == 1
        assert json.loads(states.read_text())["source/other-repository#17"] == "OPEN"
