import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.io import CommandError
from runtime.schema import validate_json

PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parents[1]
SPEC = importlib.util.spec_from_file_location("guru_finish_task_invoke", PACKAGE / "runtime/invoke.py")
assert SPEC and SPEC.loader
FINISH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FINISH)


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=True).stdout.strip()


def write_fake_gh(path):
    path.write_text(
        """#!/usr/bin/env python3
import json, os, subprocess, sys
from pathlib import Path

args = sys.argv[1:]
state_path = Path(os.environ['FAKE_GH_STATE'])
log_path = Path(os.environ['FAKE_GH_LOG'])
repo = Path(os.environ['FAKE_REPO_PATH'])
remote = Path(os.environ['FAKE_REMOTE_PATH'])
state = json.loads(state_path.read_text()) if state_path.exists() else {}
with log_path.open('a') as stream:
    stream.write(json.dumps(args) + '\\n')

if args[:2] == ['pr', 'list']:
    print(json.dumps([state['pr']] if state.get('pr') and state['pr']['state'] == 'OPEN' else []))
elif args[:2] == ['pr', 'create']:
    def value(flag): return args[args.index(flag) + 1]
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=repo, text=True, capture_output=True, check=True).stdout.strip()
    state['pr'] = {'number': 7, 'url': 'https://github.com/example/repo/pull/7', 'state': 'OPEN', 'isDraft': False, 'title': value('--title'), 'body': value('--body'), 'headRefName': value('--head'), 'headRefOid': head, 'baseRefName': value('--base'), 'mergedAt': None, 'mergeCommit': None}
    state_path.write_text(json.dumps(state))
    print(state['pr']['url'])
elif args[:2] == ['pr', 'view']:
    print(json.dumps(state['pr']))
elif args[:2] == ['pr', 'merge']:
    expected = args[args.index('--match-head-commit') + 1]
    subprocess.run(['git', '--git-dir', str(remote), 'update-ref', 'refs/heads/main', expected], check=True)
    state['pr'].update({'state': 'MERGED', 'mergedAt': '2026-09-19T00:00:00Z', 'mergeCommit': {'oid': expected}})
    state_path.write_text(json.dumps(state))
else:
    raise SystemExit('unsupported fake gh invocation: ' + repr(args))
"""
    )
    path.chmod(0o755)


def test_contract_assets():
    validate_json(json.loads((PACKAGE / "interface.json").read_text()), ROOT / "schemas/skill-interface-1.4.schema.json", "interface")


def test_semantic_resume_finish_returns_complete_self_projection(tmp_path):
    public = json.loads((PACKAGE / "examples/public-input.json").read_text())
    semantic = {
        "profile": "closure_completed",
        "mode": public["mode"],
        "allowlist": [public["task_ref"]],
        "route": {
            "typed_exit": "resume_finish",
            "reason_code": "bookkeeping_requires_revision",
            "remediation": "Revise the reviewed bookkeeping route.",
        },
    }
    input_path = tmp_path / "input.json"
    semantic_path = tmp_path / "semantic.json"
    input_path.write_text(json.dumps(public))
    semantic_path.write_text(json.dumps(semantic))

    output = FINISH.run(
        PACKAGE,
        {},
        ["--root", str(tmp_path), "--input", str(input_path), "--semantic-result", str(semantic_path)],
    )

    expected = {
        "exit_id": "resume_finish",
        "task_ref": public["task_ref"],
        "closure_exit": public["closure_exit"],
        "closure_ref": public["closure_ref"],
    }
    assert output == expected
    validate_json(output, PACKAGE / "schemas/public-resume-finish-output.schema.json", "resume_finish")

    interface = json.loads((PACKAGE / "interface.json").read_text())
    projection = next(item for item in interface["public_contracts"]["projections"] if item["id"] == "self")
    authored = json.loads((PACKAGE / "examples/self-authoring.json").read_text())
    projected = {mapping["target"]: output[mapping["source"]] for mapping in projection["mappings"]}
    validate_json({**authored, **projected}, PACKAGE / "schemas/public-input.schema.json", "self_projection")


def test_allowlist_rejects_archive_root_for_another_task():
    public = {"task_ref": ".trellis/tasks/demo"}
    semantic = {
        "allowlist": [
            ".trellis/tasks/demo",
            ".trellis/tasks/archive/2026-08/other-task",
            ".trellis/tasks/archive/2026-09/demo",
        ],
        "bookkeeping": {"archive_ref": ".trellis/tasks/archive/2026-09/demo"},
    }

    with pytest.raises(CommandError) as caught:
        FINISH.lifecycle_roots(public, semantic)

    assert caught.value.field_path == "semantic_result.allowlist"


@pytest.mark.parametrize("closing_reference", ["Closes #7", "Fixes example/repo#7", "Resolved: owner.repo/repo-name#42"])
def test_payload_rejects_bare_and_repo_qualified_closing_keywords(closing_reference):
    bookkeeping = {
        "commit_subject": "chore(trellis): persist finish",
        "commit_body": "Refs #7",
        "pr_title": "Persist task finish",
        "pr_body": closing_reference,
        "merge_subject": "chore(merge): persist task finish",
        "merge_body": "Refs example/repo#7",
    }

    with pytest.raises(CommandError) as caught:
        FINISH.verify_payload(bookkeeping)

    assert caught.value.field_path == "semantic_result.bookkeeping"


def test_merge_rechecks_expected_base_before_github_mutation(tmp_path, monkeypatch):
    expected_base_head = "1" * 40
    transaction = {
        "pr_number": 7,
        "commit": "2" * 40,
        "expected_base_head": expected_base_head,
    }
    bookkeeping = {
        "repo_ref": "example/repo",
        "base_branch": "main",
        "merge_subject": "chore(merge): persist finish",
        "merge_body": "Refs #7",
    }
    mutations = []
    monkeypatch.setattr(FINISH, "exact_pr", lambda *_args: {"state": "OPEN"})
    monkeypatch.setattr(FINISH, "current_remote_head", lambda *_args: "3" * 40)
    monkeypatch.setattr(FINISH, "gh", lambda *_args: mutations.append(_args))

    with pytest.raises(CommandError) as caught:
        FINISH.merge(tmp_path, {"task_ref": ".trellis/tasks/demo"}, bookkeeping, transaction, tmp_path / "transaction.json", PACKAGE)

    assert caught.value.field_path == "bookkeeping.expected_base_head"
    assert mutations == []


def test_finish_publishes_and_merges_one_expected_head_bookkeeping_pr(tmp_path):
    repo = tmp_path / "repo"
    remote = tmp_path / "remote.git"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    subprocess.run(["git", "init", "-q", "--bare", remote], check=True)
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Test")
    git(repo, "remote", "add", "origin", str(remote))
    (repo / ".gitignore").write_text(".trellis/.runtime/\n")
    old_archive_ref = ".trellis/tasks/archive/2026-08/demo"
    old_archive = repo / old_archive_ref
    old_archive.mkdir(parents=True)
    (old_archive / "legacy-finish-summary.json").write_text("{}\n")
    task = repo / ".trellis/tasks/demo"
    task.mkdir(parents=True)
    (task / "task.json").write_text(json.dumps({"id": "demo", "title": "Demo", "status": "in_progress", "base_branch": "main"}))
    for name in ("prd.md", "design.md", "implement.md"):
        (task / name).write_text("x\n")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "initial")
    base_head = git(repo, "rev-parse", "HEAD")
    git(repo, "push", "-q", "-u", "origin", "main")
    git(repo, "switch", "-qc", "codex/demo")
    shutil.rmtree(old_archive)

    archive_ref = ".trellis/tasks/archive/2026-09/demo"
    public = {"profile": "closure_completed", "source_exit": "no_mutation", "mode": "standalone", "task_ref": ".trellis/tasks/demo", "closure_exit": "no_mutation", "closure_ref": "closure:v1:demo"}
    semantic = {
        "profile": "closure_completed",
        "mode": "standalone",
        "allowlist": [".trellis/tasks/demo", old_archive_ref, archive_ref],
        "bookkeeping": {
            "repo_ref": "example/repo",
            "base_branch": "main",
            "expected_base_head": base_head,
            "head_branch": "codex/demo",
            "archive_ref": archive_ref,
            "commit_subject": "chore(trellis): persist demo finish",
            "commit_body": "Persist terminal task metadata.\n\nRefs #7",
            "pr_title": "持久化 demo task 收尾归档",
            "pr_body": "仅包含 task lifecycle bookkeeping。\n\nRefs #7",
            "merge_subject": "chore(merge): 持久化 demo task 收尾归档",
            "merge_body": "Merge reviewed bookkeeping.\n\nRefs #7",
        },
        "route": {"typed_exit": "success"},
    }
    input_path = tmp_path / "input.json"
    semantic_path = tmp_path / "semantic.json"
    input_path.write_text(json.dumps(public))
    semantic_path.write_text(json.dumps(semantic))
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    write_fake_gh(fake_bin / "gh")
    env = os.environ.copy()
    env.update({"PYTHONPATH": str(ROOT), "PATH": str(fake_bin) + os.pathsep + env["PATH"], "FAKE_GH_STATE": str(tmp_path / "gh-state.json"), "FAKE_GH_LOG": str(tmp_path / "gh.log"), "FAKE_REPO_PATH": str(repo), "FAKE_REMOTE_PATH": str(remote)})
    command = [sys.executable, str(PACKAGE / "runtime/invoke.py"), "--root", str(repo), "--input", str(input_path), "--semantic-result", str(semantic_path)]
    resume = {"exit_id": "resume_finish", "task_ref": ".trellis/tasks/demo", "closure_exit": "no_mutation", "closure_ref": "closure:v1:demo"}

    assert json.loads(subprocess.run(command, text=True, capture_output=True, env=env, check=True).stdout) == resume
    assert task.exists()
    projected = json.loads(subprocess.run(command + ["--confirmed-finish"], text=True, capture_output=True, env=env, check=True).stdout)
    assert projected == resume and not task.exists() and (repo / archive_ref).is_dir()
    assert json.loads(subprocess.run(command, text=True, capture_output=True, env=env, check=True).stdout) == resume
    published = json.loads(subprocess.run(command + ["--confirmed-bookkeeping-publish"], text=True, capture_output=True, env=env, check=True).stdout)
    assert published == resume
    finished = json.loads(subprocess.run(command + ["--confirmed-bookkeeping-merge"], text=True, capture_output=True, env=env, check=True).stdout)
    assert finished == {"exit_id": "success", "task_ref": ".trellis/tasks/demo", "archive_ref": archive_ref, "finish_ref": finished["finish_ref"]}
    repeated = json.loads(subprocess.run(command, text=True, capture_output=True, env=env, check=True).stdout)
    assert repeated["exit_id"] == "success"
    log = (tmp_path / "gh.log").read_text()
    assert log.count('"create"') == 1 and log.count('"merge"') == 1 and '--match-head-commit' in log
    target = git(repo, "rev-parse", "refs/remotes/origin/main")
    assert subprocess.run(["git", "cat-file", "-e", f"{target}:{archive_ref}/finish-summary.json"], cwd=repo).returncode == 0
    assert subprocess.run(["git", "cat-file", "-e", f"{target}:.trellis/tasks/demo/task.json"], cwd=repo).returncode != 0
