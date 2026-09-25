import importlib.util
import json
import os
import shutil
import subprocess
import sys
import types
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.io import CommandError
from runtime.schema import validate_json
from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
from runtime.task_lifecycle.git_facts import inspect_repository
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore

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
    base = subprocess.run(['git', '--git-dir', str(remote), 'rev-parse', 'refs/heads/main'], text=True, capture_output=True, check=True).stdout.strip()
    tree = subprocess.run(['git', '-C', str(repo), 'rev-parse', expected + '^{tree}'], text=True, capture_output=True, check=True).stdout.strip()
    merged = subprocess.run(['git', '-C', str(repo), 'commit-tree', tree, '-p', base, '-p', expected, '-m', 'Merge reviewed bookkeeping'], text=True, capture_output=True, check=True).stdout.strip()
    subprocess.run(['git', '-C', str(repo), 'push', 'origin', merged + ':refs/heads/main'], check=True, capture_output=True)
    state['pr'].update({'state': 'MERGED', 'mergedAt': '2026-09-19T00:00:00Z', 'mergeCommit': {'oid': merged}})
    state_path.write_text(json.dumps(state))
else:
    raise SystemExit('unsupported fake gh invocation: ' + repr(args))
"""
    )
    path.chmod(0o755)


def test_contract_assets():
    validate_json(json.loads((PACKAGE / "interface.json").read_text()), ROOT / "schemas/skill-interface-1.4.schema.json", "interface")
    public = json.loads((PACKAGE / "examples/public-input.json").read_text())
    validate_json(public, PACKAGE / "schemas/public-input.schema.json", "input")
    validate_json(json.loads((PACKAGE / "examples/public-reentry-input.json").read_text()), PACKAGE / "schemas/public-input.schema.json", "reentry")
    for field, value in (("task_ref", ".trellis/tasks/example-task"), ("closure_actions", [])):
        with pytest.raises(CommandError):
            validate_json({**public, field: value}, PACKAGE / "schemas/public-input.schema.json", "input")


@pytest.mark.parametrize("disposition,required", [
    ("close", True), ("already_closed_at_review", True), ("no_close_authority", False),
])
def test_closure_snapshot_requires_exact_terminal_result_and_disposition(tmp_path, monkeypatch, disposition, required):
    subprocess.run(["git", "init", "-q", "-b", "main", str(tmp_path)], check=True)
    ref = {"task_id": "demo", "lifecycle_generation": 0, "result_id": "closure:demo"}
    row = {"issue_ref": {"repo_ref": "example/repo", "issue_number": 7}, "disposition": disposition}
    snapshot = {"result_ref": ref, "terminal": "closed" if required else "no_mutation", "action_set": [row]}
    module = types.ModuleType("runtime.task_lifecycle.closure_result")
    module.read_terminal_closure_result = lambda *_args: snapshot
    monkeypatch.setitem(sys.modules, module.__name__, module)
    observed = FINISH.read_closure_snapshot(tmp_path, PACKAGE, ref)
    assert observed == snapshot
    monkeypatch.setattr(FINISH, "gh_json", lambda *_args: {"number": 7, "state": "OPEN"})
    assert FINISH.closure_current(observed["action_set"]) is not required
    snapshot["result_ref"] = {**ref, "result_id": "closure:other"}
    with pytest.raises(CommandError) as caught:
        FINISH.read_closure_snapshot(tmp_path, PACKAGE, ref)
    assert caught.value.field_path == "closure_result"


def test_missing_shared_closure_reader_stops_before_mutation(tmp_path, monkeypatch):
    subprocess.run(["git", "init", "-q", "-b", "main", str(tmp_path)], check=True)
    ref = {"task_id": "demo", "lifecycle_generation": 0, "result_id": "closure:demo"}
    monkeypatch.setitem(sys.modules, "runtime.task_lifecycle.closure_result", None)
    with pytest.raises(CommandError) as caught:
        FINISH.read_closure_snapshot(tmp_path, PACKAGE, ref)
    assert caught.value.code == "closure_result_reader_missing"


def test_finish_outputs_project_into_cleanup_owned_profiles():
    interface = json.loads((PACKAGE / "interface.json").read_text())
    cleanup = PACKAGE.parent / "guru-cleanup-task-resources"
    for exit_id, example, authoring in (
        ("success", "public-output.json", "cleanup-authoring.json"),
        ("manual_cleanup_required", "public-manual-cleanup-output.json", "manual-cleanup-authoring.json"),
    ):
        output = json.loads((PACKAGE / "examples" / example).read_text())
        consumer = next(row for row in interface["public_contracts"]["consumer_inputs"] if row["id"] == ("cleanup" if exit_id == "success" else "manual_cleanup"))
        projection = next(row for row in interface["public_contracts"]["projections"] if row["exit_id"] == exit_id)
        authored = json.loads((PACKAGE / "examples" / authoring).read_text())
        projected = {row["target"]: output[row["source"]] for row in projection["mappings"]}
        assert set(projected) == set(consumer["contract"]["seed_fields"])
        assert set(authored) == set(consumer["contract"]["authoring_fields"])
        validate_json({**authored, **projected}, cleanup / "schemas/public-input.schema.json", exit_id)


@pytest.mark.parametrize("disposition", ["close", "already_closed_at_review"])
def test_reopened_required_closed_issue_refreshes_closure_before_terminal_mutation(tmp_path, monkeypatch, disposition):
    public = json.loads((PACKAGE / "examples/public-input.json").read_text())
    subprocess.run(["git", "init", "-q", "-b", "main", str(tmp_path)], check=True)
    semantic = json.loads((PACKAGE / "examples/semantic-result.json").read_text())
    task = tmp_path / ".trellis/tasks/example-task"
    task.mkdir(parents=True)
    (task / "task.json").write_text(json.dumps({"id": public["closure_result"]["task_id"], "lifecycle_generation": 1}))
    input_path = tmp_path / "input.json"
    semantic_path = tmp_path / "semantic.json"
    input_path.write_text(json.dumps(public))
    semantic_path.write_text(json.dumps(semantic))
    row = {"issue_ref": {"repo_ref": "example/repo", "issue_number": 7}, "disposition": disposition}
    monkeypatch.setattr(FINISH, "read_closure_snapshot", lambda *_args: {"result_ref": public["closure_result"], "terminal": "closed", "action_set": [row]})
    monkeypatch.setattr(FINISH, "gh_json", lambda *_args: {"number": 7, "state": "OPEN"})
    monkeypatch.setattr(FINISH, "project_archive", lambda *_args: pytest.fail("archive mutation attempted"))
    monkeypatch.setattr(FINISH.ResourceLedgerStore, "seal_for_finish", lambda *_args, **_kwargs: pytest.fail("ledger mutation attempted"))

    output = FINISH.run(PACKAGE, {}, ["--root", str(tmp_path), "--input", str(input_path), "--semantic-result", str(semantic_path), "--confirmed-finish"])

    assert output == {"exit_id": "closure_refresh_required", **public["closure_result"]}
    assert task.is_dir()
    assert not (tmp_path / semantic["bookkeeping"]["archive_ref"]).exists()


def test_finish_identity_changes_between_lifecycle_generations():
    public = {"task_id": "demo", "closure_result": {"result_id": "closure:demo"}}
    assert FINISH.finish_ref(public, 0) != FINISH.finish_ref(public, 1)


def test_semantic_resume_finish_returns_complete_self_projection(tmp_path, monkeypatch):
    public = json.loads((PACKAGE / "examples/public-input.json").read_text())
    subprocess.run(["git", "init", "-q", "-b", "main", str(tmp_path)], check=True)
    task = tmp_path / ".trellis/tasks/example-task"
    task.mkdir(parents=True)
    (task / "task.json").write_text(json.dumps({"id": "example-task", "lifecycle_generation": 1}))
    monkeypatch.setattr(FINISH, "read_closure_snapshot", lambda *_args: {"result_ref": public["closure_result"], "terminal": "no_mutation", "action_set": []})
    semantic = {
        "profile": "closure_completed",
        "mode": public["mode"],
        "allowlist": [".trellis/tasks/example-task"],
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
        "task_id": public["closure_result"]["task_id"],
        "lifecycle_generation": public["closure_result"]["lifecycle_generation"],
        "transaction_id": FINISH.finish_ref({"task_id": "example-task", "closure_result": public["closure_result"]}, 1),
        "result_id": public["closure_result"]["result_id"],
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


def test_staging_uses_existing_reviewed_paths_and_rejects_outside_changes(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Test")
    archive = repo / ".trellis/tasks/archive/2026-09/demo/task.json"
    archive.parent.mkdir(parents=True)
    archive.write_text('{"lifecycle_generation": 0}\n')
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "archive cycle zero")

    archive.write_text('{"lifecycle_generation": 1}\n')
    allowlist = (".trellis/tasks/demo", ".trellis/tasks/archive/2026-09/demo")
    FINISH.stage_reviewed_changes(repo, allowlist)
    assert git(repo, "diff", "--cached", "--name-only") == ".trellis/tasks/archive/2026-09/demo/task.json"

    git(repo, "reset", "-q")
    (repo / "outside.txt").write_text("not reviewed\n")
    with pytest.raises(CommandError) as caught:
        FINISH.stage_reviewed_changes(repo, allowlist)

    assert caught.value.field_path == "semantic_result.allowlist"
    assert git(repo, "diff", "--cached", "--name-only") == ""


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


def test_finish_publishes_and_merges_one_expected_head_bookkeeping_pr(tmp_path, monkeypatch):
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
    (task / "task.json").write_text(json.dumps({"id": "demo", "title": "Demo", "status": "in_progress", "base_branch": "main", "lifecycle_generation": 0}))
    for name in ("prd.md", "design.md", "implement.md"):
        (task / name).write_text("x\n")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "initial")
    base_head = git(repo, "rev-parse", "HEAD")
    git(repo, "push", "-q", "-u", "origin", "main")
    git(repo, "switch", "-qc", "codex/demo")
    store = ResourceLedgerStore(inspect_repository(repo))
    key = TaskLifecycleKey("demo", 0)
    binding_store = BranchBindingStore(store.repository)
    binding = binding_store.establish(key, "codex/demo")
    store.establish_current(key, binding_epoch=binding.binding_epoch, binding_revision=0, branch_name="codex/demo", branch_ownership="guru_owned", worktree_ownership="not_applicable")
    shutil.rmtree(old_archive)

    archive_ref = ".trellis/tasks/archive/2026-09/demo"
    public = {"profile": "closure_completed", "mode": "standalone", "closure_result": {"task_id": "demo", "lifecycle_generation": 0, "result_id": "closure:demo"}}
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
    for name, value in env.items():
        if name in {"PATH", "FAKE_GH_STATE", "FAKE_GH_LOG", "FAKE_REPO_PATH", "FAKE_REMOTE_PATH"}:
            monkeypatch.setenv(name, value)
    closure_path = store.repository.common_dir / "guru-team/closure/demo/0.json"
    closure_path.parent.mkdir(parents=True)
    closure_path.write_text(json.dumps({"ref": {"task_id": "demo", "lifecycle_generation": 0, "result_id": "closure:demo", "transaction_id": "closure:demo"},
                                        "frozen": {"action_set": []}, "verified": [], "terminal": "no_mutation"}))
    def invoke(*flags):
        return FINISH.run(PACKAGE, {}, ["--root", str(repo), "--input", str(input_path), "--semantic-result", str(semantic_path), *flags])
    resume = {"exit_id": "resume_finish", "task_id": "demo", "lifecycle_generation": 0, "transaction_id": FINISH.finish_ref({"task_id": "demo", "closure_result": public["closure_result"]}, 0), "result_id": "closure:demo"}

    assert invoke() == resume
    assert task.exists()
    projected = invoke("--confirmed-finish")
    assert projected == resume and not task.exists() and (repo / archive_ref).is_dir()
    assert invoke() == resume
    published = invoke("--confirmed-bookkeeping-publish")
    assert published == resume
    finished = invoke("--confirmed-bookkeeping-merge")
    assert finished == {"exit_id": "success", "task_id": "demo", "lifecycle_generation": 0, "finish_result_id": resume["transaction_id"], "inventory_id": finished["inventory_id"]}
    assert binding_store.read(key) is None
    assert store.read(key).finish_head == git(repo, "rev-parse", "HEAD")
    assert git(repo, "rev-parse", "refs/remotes/origin/main") != store.read(key).finish_head
    assert store.cleanup_resolution(TaskLifecycleKey("demo", 0), finish_result_id=finished["finish_result_id"], inventory_id=finished["inventory_id"]).resolution_kind == "ordinary_cleanup"
    repeated = invoke()
    assert repeated["exit_id"] == "success"
    git(repo, "switch", "-q", "main")
    cleanup_package = PACKAGE.parent / "guru-cleanup-task-resources"
    cleanup_spec = importlib.util.spec_from_file_location("guru_cleanup_after_finish", cleanup_package / "runtime/invoke.py")
    assert cleanup_spec and cleanup_spec.loader
    cleanup = importlib.util.module_from_spec(cleanup_spec)
    cleanup_spec.loader.exec_module(cleanup)
    cleanup_input = tmp_path / "cleanup-input.json"
    cleanup_semantic = tmp_path / "cleanup-semantic.json"
    cleanup_input.write_text(json.dumps({"profile": "normal", "mode": "standalone", **{key: finished[key] for key in ("task_id", "lifecycle_generation", "finish_result_id", "inventory_id")}}))
    cleanup_semantic.write_text(json.dumps({"profile": "normal", "mode": "standalone", "route": {"typed_exit": "cleaned"}}))
    assert cleanup.run(cleanup_package, {}, ["--root", str(repo), "--input", str(cleanup_input),
                                             "--semantic-result", str(cleanup_semantic), "--confirmed-cleanup"])["exit_id"] == "cleaned"
    assert store.read(key).resources[0].state == "resolved"
    log = (tmp_path / "gh.log").read_text()
    assert log.count('"create"') == 1 and log.count('"merge"') == 1 and '--match-head-commit' in log
    target = git(repo, "rev-parse", "refs/remotes/origin/main")
    assert subprocess.run(["git", "cat-file", "-e", f"{target}:{archive_ref}/finish-summary.json"], cwd=repo).returncode == 0
    assert subprocess.run(["git", "cat-file", "-e", f"{target}:.trellis/tasks/demo/task.json"], cwd=repo).returncode != 0


def test_finish_accepts_date_prefixed_task_directory_with_stable_task_id(tmp_path):
    repo = tmp_path / "repo"; repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "--allow-empty", "-qm", "seed"], cwd=repo, check=True)
    task_ref = ".trellis/tasks/09-19-demo"; task_dir = repo / task_ref; task_dir.mkdir(parents=True)
    (task_dir / "task.json").write_text(json.dumps({"id":"demo","status":"in_progress","lifecycle_generation":1}) + "\n")
    archive_ref = ".trellis/tasks/archive/2026-09/09-19-demo"
    FINISH.project_archive(repo, {"task_ref": task_ref}, Path(task_ref), archive_ref, Path(archive_ref))
    assert not task_dir.exists()
    assert (repo / archive_ref / "task.json").is_file()
