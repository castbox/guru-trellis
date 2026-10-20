import importlib.util
import json
import os
import shutil
import subprocess
import sys
import types
import tempfile
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


def current_task_metadata(root, task_id, generation, source):
    # Read actual schema-2 creation bytes from the fixed installed public CLI.
    assert generation == 0
    scripts = Path(os.environ["GURU_UPSTREAM_DELIVERY_SCRIPTS"])
    shutil.copytree(scripts, root / ".trellis/scripts", dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copy2(PACKAGE.parents[4] / "trellis/workflows/guru-team/workflow.md", root / ".trellis/workflow.md")
    (root / ".trellis/.developer").write_text("finish-fixture\n")
    with tempfile.TemporaryDirectory() as directory:
        donor = Path(directory)
        subprocess.run(["git", "init", "-qb", "main", str(donor)], check=True)
        shutil.copytree(root / ".trellis/scripts", donor / ".trellis/scripts")
        shutil.copy2(root / ".trellis/workflow.md", donor / ".trellis/workflow.md")
        (donor / ".trellis/.developer").write_text("finish-fixture\n")
        created = subprocess.run([sys.executable, str(donor / ".trellis/scripts/task.py"), "create", "Finish fixture",
            "--slug", task_id, "--task-id", task_id, "--description", "Finish fixture",
            "--schema-version", "2.0", "--source-json", json.dumps(source), "--base-branch", "main", "--no-start"],
            cwd=donor, capture_output=True, text=True)
        assert created.returncode == 0, created.stdout + created.stderr
        path = next((donor / ".trellis/tasks").glob("*/task.json"))
        value = json.loads(path.read_text())
    return value


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
elif args[:2] == ['issue', 'view']:
    print(json.dumps({'number': int(args[2]), 'state': state['issue_state']}) if '--jq' not in args else state['issue_state'])
elif args[:2] == ['issue', 'close']:
    state['issue_state'] = 'CLOSED'
    state_path.write_text(json.dumps(state))
else:
    raise SystemExit('unsupported fake gh invocation: ' + repr(args))
""".replace("#!/usr/bin/env python3", "#!" + sys.executable)
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
    ("close", True), ("already_closed_at_review", True), ("retain_open", False), ("no_close_authority", False),
])
def test_closure_snapshot_requires_exact_terminal_result_and_disposition(tmp_path, monkeypatch, disposition, required):
    subprocess.run(["git", "init", "-q", "-b", "main", str(tmp_path)], check=True)
    ref = {"task_id": "demo", "lifecycle_generation": 0, "result_id": "closure:demo"}
    row = {"issue_ref": {"repo_ref": "example/repo", "issue_number": 7}, "disposition": disposition}
    snapshot = {"result_ref": ref, "terminal": "closed" if required else "no_mutation", "action_set": [row],
                "source": {"kind": "issue", "repo_ref": "example/repo", "number": 7, "disposition": "exact_source"}}
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


@pytest.mark.parametrize("disposition", ["close", "already_closed_at_review", "retain_open"])
def test_changed_required_issue_state_refreshes_closure_before_terminal_mutation(tmp_path, monkeypatch, disposition):
    public = json.loads((PACKAGE / "examples/public-input.json").read_text())
    public["closure_result"]["lifecycle_generation"] = 0
    subprocess.run(["git", "init", "-q", "-b", "main", str(tmp_path)], check=True)
    semantic = json.loads((PACKAGE / "examples/semantic-result.json").read_text())
    task = tmp_path / ".trellis/tasks/example-task"
    task.mkdir(parents=True)
    source = {"kind": "issue", "repo_ref": "example/repo", "number": 7, "disposition": "exact_source"}
    (task / "task.json").write_text(json.dumps(current_task_metadata(tmp_path, public["closure_result"]["task_id"], 0, source)))
    input_path = tmp_path / "input.json"
    semantic_path = tmp_path / "semantic.json"
    input_path.write_text(json.dumps(public))
    semantic_path.write_text(json.dumps(semantic))
    row = {"issue_ref": {"repo_ref": "example/repo", "issue_number": 7}, "disposition": disposition}
    monkeypatch.setattr(FINISH, "read_closure_snapshot", lambda *_args: {"result_ref": public["closure_result"], "terminal": "no_mutation" if disposition == "retain_open" else "closed", "action_set": [row], "source": source})
    monkeypatch.setattr(FINISH, "gh_json", lambda *_args: {"number": 7, "state": "CLOSED" if disposition == "retain_open" else "OPEN"})
    monkeypatch.setattr(FINISH, "project_archive", lambda *_args: pytest.fail("archive mutation attempted"))
    monkeypatch.setattr(FINISH.ResourceLedgerStore, "seal_for_finish", lambda *_args, **_kwargs: pytest.fail("ledger mutation attempted"))

    output = FINISH.run(PACKAGE, {}, ["--root", str(tmp_path), "--input", str(input_path), "--semantic-result", str(semantic_path), "--confirmed-finish"])

    assert output == {"exit_id": "closure_refresh_required", **public["closure_result"]}
    assert task.is_dir()
    assert not (tmp_path / semantic["bookkeeping"]["archive_ref"]).exists()


def test_changed_source_role_refreshes_closure_before_finish_archive(tmp_path, monkeypatch):
    public = json.loads((PACKAGE / "examples/public-input.json").read_text())
    public["closure_result"]["lifecycle_generation"] = 0
    semantic = json.loads((PACKAGE / "examples/semantic-result.json").read_text())
    subprocess.run(["git", "init", "-q", "-b", "main", str(tmp_path)], check=True)
    task = tmp_path / ".trellis/tasks/example-task"
    task.mkdir(parents=True)
    (task / "task.json").write_text(json.dumps(current_task_metadata(tmp_path, "example-task", 0,
        {"kind": "issue", "repo_ref": "example/repo", "number": 7, "disposition": "reference_only"})))
    input_path = tmp_path / "input.json"
    semantic_path = tmp_path / "semantic.json"
    input_path.write_text(json.dumps(public))
    semantic_path.write_text(json.dumps(semantic))
    frozen = {"result_ref": public["closure_result"], "terminal": "no_mutation", "action_set": [],
              "source": {"kind": "issue", "repo_ref": "example/repo", "number": 7, "disposition": "exact_source"}}
    monkeypatch.setattr(FINISH, "read_closure_snapshot", lambda *_args: frozen)
    monkeypatch.setattr(FINISH, "project_archive", lambda *_args: pytest.fail("archive mutation attempted"))

    result = FINISH.run(PACKAGE, {}, ["--root", str(tmp_path), "--input", str(input_path),
        "--semantic-result", str(semantic_path), "--confirmed-finish"])

    assert result == {"exit_id": "closure_refresh_required", **public["closure_result"]}
    assert task.is_dir()


def test_finish_identity_changes_between_lifecycle_generations():
    public = {"task_id": "demo", "closure_result": {"result_id": "closure:demo"}}
    assert FINISH.finish_ref(public, 0) != FINISH.finish_ref(public, 1)


def test_semantic_resume_finish_returns_complete_self_projection(tmp_path, monkeypatch):
    public = json.loads((PACKAGE / "examples/public-input.json").read_text())
    public["closure_result"]["lifecycle_generation"] = 0
    subprocess.run(["git", "init", "-q", "-b", "main", str(tmp_path)], check=True)
    task = tmp_path / ".trellis/tasks/example-task"
    task.mkdir(parents=True)
    (task / "task.json").write_text(json.dumps(current_task_metadata(tmp_path, "example-task", 0, {"kind": "no_issue"})))
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
        "transaction_id": FINISH.finish_ref({"task_id": "example-task", "closure_result": public["closure_result"]}, 0),
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


@pytest.mark.parametrize("trailer", [
    "Guru-Delivery-Task: example-task",
    "Guru-Delivery-Cycle: 1",
    "Guru-Task-Identity: example-task",
    "Guru-Delivery-Schema: 1",
    "Guru-Delivery-Head: " + "a" * 40,
])
@pytest.mark.parametrize("field", [
    "commit_subject", "commit_body", "pr_title", "pr_body", "merge_subject", "merge_body",
])
def test_bookkeeping_payload_rejects_delivery_trailers(trailer, field):
    bookkeeping = {
        "commit_subject": "chore(trellis): persist finish", "commit_body": "Refs #7",
        "pr_title": "Persist task finish", "pr_body": "Refs #7",
        "merge_subject": "chore(merge): persist task finish", "merge_body": "Refs #7",
    }
    bookkeeping[field] += "\n\n" + trailer
    with pytest.raises(CommandError) as caught:
        FINISH.verify_payload(bookkeeping)
    assert caught.value.field_path == "semantic_result.bookkeeping"


def test_merge_allows_unrelated_target_advance(tmp_path, monkeypatch):
    transaction = {"pr_number": 7, "commit": "2" * 40}
    bookkeeping = {"repo_ref": "example/repo", "base_branch": "main",
                   "merge_subject": "chore(merge): persist finish", "merge_body": "Refs #7"}
    mutations = []
    reads = iter([{"state": "OPEN"}, {"state": "MERGED", "mergedAt": "now", "mergeCommit": {"oid": "4" * 40}}])
    monkeypatch.setattr(FINISH, "exact_pr", lambda *_args: next(reads))
    monkeypatch.setattr(FINISH, "verify_target", lambda *_args: "5" * 40)
    monkeypatch.setattr(FINISH, "git", lambda *_args, **_kwargs: type("Result", (), {"returncode": 0})())
    monkeypatch.setattr(FINISH, "gh", lambda *_args: mutations.append(_args))
    monkeypatch.setattr(FINISH, "write_transaction", lambda *_args: None)
    result = FINISH.merge(tmp_path, {"task_ref": ".trellis/tasks/demo"}, bookkeeping, transaction, tmp_path / "transaction.json", PACKAGE)
    assert result["stage"] == "success" and result["target_head"] == "5" * 40
    assert len(mutations) == 1
    assert "--match-head-commit" in mutations[0]


@pytest.mark.parametrize("missing_ownership", [False, True])
@pytest.mark.parametrize("retained_source", [False, True])
def test_finish_publishes_and_merges_one_expected_head_bookkeeping_pr(tmp_path, monkeypatch, missing_ownership, retained_source):
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
    source = {"kind": "issue", "repo_ref": "example/repo", "number": 7, "disposition": "exact_source"} if retained_source else {"kind": "no_issue"}
    (task / "task.json").write_text(json.dumps(current_task_metadata(repo, "demo", 0, source)))
    wrapper_root = ROOT
    if retained_source:
        # Real matching preset installation; the engineering checkout's complete
        # legacy installation is never reapplied or changed by this fixture.
        sdk_package = Path(os.environ["GURU_UPSTREAM_DELIVERY_SCRIPTS"]).parents[3] / "package.json"
        (repo / ".trellis/.version").write_text(json.loads(sdk_package.read_text())["version"] + "\n")
        caller = tmp_path / "installer-source"
        shutil.copytree(ROOT / "runtime", caller / "trellis/skills/guru-team/runtime",
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        applied = subprocess.run(["bash", str(ROOT.parents[2] / "trellis/presets/guru-team/scripts/bash/apply.sh"), "--repo", str(repo)],
                                 cwd=caller, text=True, capture_output=True)
        assert applied.returncode == 0, applied.stdout + applied.stderr
        assert json.loads(applied.stdout)["skill_installed_validation"]["returncode"] == 0
        wrapper_root = repo / ".trellis/guru-team/skills"
        # The upstream API supports a local-commit workflow profile. Declare it
        # only in this controlled fixture; production Guru stays pull_request.
        workflow = repo / ".trellis/workflow.md"
        workflow.write_text(workflow.read_text().replace('"profiles": ["pull_request"]', '"profiles": ["local_commit", "pull_request"]'))
    for name in ("prd.md", "design.md", "implement.md"):
        (task / name).write_text("x\n")
    from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
    projection = DeliveryProjection(repo, ".trellis/tasks/demo")
    scope = authority_ref(task / "prd.md", repo)
    projection.scope(scope)
    owners = projection.declaration()["owners"]
    key = {"task_id": "demo", "lifecycle_generation": 0}
    delivery_key = {**key, "delivery_id": "43134b50-2c8b-4d70-b114-218a735a82e2"}
    if retained_source:
        # Accepted scope and history come from the actual public owners.
        (task / "prd.md").write_text("Document delivery; real integration initially included.\n")
        scope = authority_ref(task / "prd.md", repo); projection.scope(scope)
        projection.apply({"api_version": "1.0", "operation": "create_delivery", "key": delivery_key,
                          "owner_role": "creation", "owner_id": owners["creation"],
                          "scope_ref": {"authority": scope, "anchors": ["document"]}, "profile": "local_commit"})
        plan = projection.planning_directory(delivery_key); plan.mkdir(parents=True, exist_ok=True)
        for name in ("prd.md", "design.md", "implement.md"):
            (plan / name).write_text("Document delivery. Real integration / product #59 joint acceptance unverified.\n")
        from runtime.delivery_projection.gates import record_gate
        result = {"result_id": "planning:demo", "owner_role": "planning", "owner_id": owners["planning"],
                  "outcome": "accepted", "scope_ref": projection.resolve(delivery_key)["scope_ref"],
                  "plan_ref": authority_ref(plan / "implement.md", repo), "candidate": None,
                  "predecessor_result_id": None, "obligations": [], "evidence": [scope]}
        projection.apply({"api_version": "1.0", "operation": "record_gate", "key": delivery_key,
                          "owner_role": "planning", "owner_id": owners["planning"], "expected_phase": "planning", "result": result})
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "initial")
    base_head = git(repo, "rev-parse", "HEAD")
    git(repo, "push", "-q", "-u", "origin", "main")
    git(repo, "switch", "-qc", "codex/demo")
    store = ResourceLedgerStore(inspect_repository(repo))
    key = TaskLifecycleKey("demo", 0)
    binding_store = BranchBindingStore(store.repository)
    binding = binding_store.establish(key, "codex/demo")
    store.establish_current(key, binding_revision=0, branch_name="codex/demo", branch_ownership="guru_owned", worktree_ownership="not_applicable")
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
    def owner_wrapper(skill, value, review, *flags):
        inp = tmp_path / (skill + "-input.json"); inp.write_text(json.dumps(value))
        sem = tmp_path / (skill + "-semantic.json"); sem.write_text(json.dumps(review))
        result = subprocess.run(["bash", str(wrapper_root / "packages" / skill / "scripts/invoke.sh"),
            "--root", str(repo), "--input", str(inp), "--semantic-result", str(sem), *flags],
            env=env, text=True, capture_output=True)
        assert result.returncode == 0, result.stdout + result.stderr
        out = json.loads(result.stdout); return out.get("result", out)
    if retained_source:
        Path(env["FAKE_GH_STATE"]).write_text(json.dumps({"issue_state": "OPEN"}))
        candidate = projection.candidate([str((task / 'prd.md').relative_to(repo))], head_ref=base_head, base_ref=base_head)
        projection.begin_check(delivery_key, candidate)
        for role, outcome in (("check", "passed"), ("full_review", "passed"), ("readiness", "ready")):
            record_gate(projection, delivery_key, role, role + ":demo", outcome, [scope], [])
        projection.apply({"api_version": "1.0", "operation": "record_delivery", "key": delivery_key,
                          "owner_role": "delivery", "owner_id": owners["delivery"], "expected_phase": "publishing",
                          "result": {"result_id": "delivery:demo", "owner_id": owners["delivery"], "evidence": [scope],
                                     "profile": "local_commit", "candidate": candidate, "commit": base_head}})
        # Normal task-scope revision preserves identity, source and Delivery history.
        (task / "prd.md").write_text("Document delivery complete. Real integration / product #59 joint acceptance remains on source Issue, outside current Task scope.\n")
        scope = authority_ref(task / "prd.md", repo); projection.scope(scope)
        task_key = {"task_id": "demo", "lifecycle_generation": 0}
        completion_input = {"profile": "delivery_completion", "mode": "workflow", "task_ref": ".trellis/tasks/demo", "task_key": task_key}
        completion_owner = {"profile": "delivery_completion", "mode": "workflow", "reviewed_task_key": task_key,
                            "reviewed_scope": scope, "reviewed_delivery_result_ids": ["delivery:demo"], "evidence": [scope],
                            "remaining_work_refs": ["integration:evidence"], "result_id": "completion:demo",
                            "route": {"typed_exit": "evidence_pending", "reason": {"reason_code": "evidence_missing", "reason_refs": ["integration:evidence"]}}}
        assert owner_wrapper("guru-review-task-completion", completion_input, completion_owner)["exit_id"] == "evidence_pending"
        assert projection.read_record()["completion_results"] == []
        completion_owner.update(remaining_work_refs=[], route={"typed_exit": "completed"})
        completed = owner_wrapper("guru-review-task-completion", completion_input, completion_owner)
        actions = [{"issue_ref": {"repo_ref": "example/repo", "issue_number": 7}, "disposition": "retain_open"}]
        closure_input = {"profile": "completion_approved", "source_exit": "completed", "mode": "workflow",
                         "completion_result": completed["result_ref"], "source": source,
                         "accepted_scope_identity": scope["revision"], "delivery_target": {"repo_ref": "example/repo", "branch_ref": "main"},
                         "binding_ref": {**task_key, "binding_revision": 0}, "content_head": base_head,
                         "evidence_slots": {"completion": completed["result_ref"]["result_id"]}, "action_set": actions}
        closure_owner = {"profile": "completion_approved", "mode": "workflow", "reviewed_action_set": actions, "route": {"typed_exit": "apply"}}
        closed = owner_wrapper("guru-complete-task-closure", closure_input, closure_owner)
        assert closed["exit_id"] == "no_mutation"
        assert owner_wrapper("guru-complete-task-closure", closure_input, closure_owner) == closed
        public["closure_result"] = closed["result_ref"]; input_path.write_text(json.dumps(public))
        before_archive = projection.read_record()
    else:
        task_key = {"task_id": "demo", "lifecycle_generation": 0}
        completion_input = {"profile": "delivery_completion", "mode": "workflow",
                            "task_ref": ".trellis/tasks/demo", "task_key": task_key}
        completion_owner = {"profile": "delivery_completion", "mode": "workflow", "reviewed_task_key": task_key,
                            "reviewed_scope": scope, "reviewed_delivery_result_ids": [], "evidence": [scope],
                            "remaining_work_refs": [], "result_id": "completion:demo", "route": {"typed_exit": "completed"}}
        completed = owner_wrapper("guru-review-task-completion", completion_input, completion_owner)
        closure_input = {"profile": "completion_approved", "source_exit": "completed", "mode": "workflow",
                         "completion_result": completed["result_ref"], "source": source,
                         "accepted_scope_identity": scope["revision"], "delivery_target": {"repo_ref": "example/repo", "branch_ref": "main"},
                         "binding_ref": {**task_key, "binding_revision": 0}, "content_head": base_head,
                         "evidence_slots": {"completion": completed["result_ref"]["result_id"]}, "action_set": []}
        closure_owner = {"profile": "completion_approved", "mode": "workflow", "reviewed_action_set": [], "route": {"typed_exit": "apply"}}
        closed = owner_wrapper("guru-complete-task-closure", closure_input, closure_owner)
        public["closure_result"] = closed["result_ref"]; input_path.write_text(json.dumps(public))
    def invoke(*flags):
        if retained_source:
            return owner_wrapper("guru-finish-task", public, semantic, *flags)
        return FINISH.run(PACKAGE, {}, ["--root", str(repo), "--input", str(input_path), "--semantic-result", str(semantic_path), *flags])
    resume = {"exit_id": "resume_finish", "task_id": "demo", "lifecycle_generation": 0, "transaction_id": FINISH.finish_ref({"task_id": "demo", "closure_result": public["closure_result"]}, 0), "result_id": public["closure_result"]["result_id"]}

    assert invoke() == resume
    assert task.exists()
    original_body = semantic["bookkeeping"]["commit_body"]
    semantic["bookkeeping"]["commit_body"] += "\n\nCloses #7"
    semantic_path.write_text(json.dumps(semantic))
    with pytest.raises((CommandError, AssertionError)) as caught:
        invoke("--confirmed-finish")
    if retained_source:
        assert "semantic_result.bookkeeping" in str(caught.value)
    else:
        assert caught.value.field_path == "semantic_result.bookkeeping"
    assert task.exists()
    semantic["bookkeeping"]["commit_body"] = original_body
    semantic_path.write_text(json.dumps(semantic))
    projected = invoke("--confirmed-finish")
    assert projected == resume and not task.exists() and (repo / archive_ref).is_dir()
    assert "archive_dir" not in json.loads((repo / archive_ref / "task.json").read_text())
    if retained_source:
        assert json.loads((repo / archive_ref / "task.json").read_text()) == {
            **before_archive, "artifact_origin": ".trellis/tasks/demo"}
        assert before_archive["source"] == source and before_archive["lifecycle_generation"] == 0
        assert before_archive["deliveries"][0]["delivery_result"]["result_id"] == "delivery:demo"
        assert "outside current Task scope" in (repo / archive_ref / "prd.md").read_text()
        assert "unverified" in (repo / archive_ref / "deliveries" / delivery_key["delivery_id"] / "design.md").read_text()
    assert invoke() == resume
    published = invoke("--confirmed-bookkeeping-publish")
    assert published == resume
    original_merge_body = semantic["bookkeeping"]["merge_body"]
    semantic["bookkeeping"]["merge_body"] += "\n\nGuru-Delivery-Head: " + "a" * 40
    semantic_path.write_text(json.dumps(semantic))
    with pytest.raises((CommandError, AssertionError)) as caught:
        invoke("--confirmed-bookkeeping-merge")
    if retained_source:
        assert "semantic_result.bookkeeping" in str(caught.value)
    else:
        assert caught.value.field_path == "semantic_result.bookkeeping"
    assert not any(row[:2] == ["pr", "merge"] for row in map(json.loads, (tmp_path / "gh.log").read_text().splitlines()))
    semantic["bookkeeping"]["merge_body"] = original_merge_body
    semantic_path.write_text(json.dumps(semantic))
    if missing_ownership:
        store.path_for(key).unlink()
    finished = invoke("--confirmed-bookkeeping-merge")
    assert invoke() == finished
    if retained_source:
        assert json.loads(Path(env["FAKE_GH_STATE"]).read_text())["issue_state"] == "OPEN"
        calls = [json.loads(line)[:2] for line in Path(env["FAKE_GH_LOG"]).read_text().splitlines()]
        assert ["issue", "close"] not in calls
        assert calls.count(["pr", "create"]) == calls.count(["pr", "merge"]) == 1
    if missing_ownership:
        assert finished == {"exit_id": "manual_cleanup_required", "task_id": "demo",
                            "lifecycle_generation": 0, "finish_result_id": resume["transaction_id"],
                            "cleanup_state": "manual_cleanup_required"}
        transaction = json.loads(FINISH.transaction_path(repo, {"task_id": "demo", **public}, 0).read_text())
        assert transaction["cleanup_state"] == "manual_cleanup_required"
        assert transaction["stage"] == "success" and transaction["commit"] != transaction["target_head"]
        manual_result = json.loads(FINISH.manual_result_path(repo, key).read_text())
        validate_json(manual_result, PACKAGE / "schemas/manual-finish-result.schema.json", "manual_finish_result")
        assert manual_result["finish_head"] == transaction["commit"]
        assert manual_result["target_head"] == transaction["target_head"]
        assert binding_store.read(key) is None and invoke() == finished
        return
    assert finished == {"exit_id": "success", "task_id": "demo", "lifecycle_generation": 0, "finish_result_id": resume["transaction_id"], "inventory_id": finished["inventory_id"]}
    assert binding_store.read(key) is None
    assert store.read(key).finish_head == git(repo, "rev-parse", "HEAD")
    assert git(repo, "rev-parse", "refs/remotes/origin/main") != store.read(key).finish_head
    assert store.cleanup_resolution(TaskLifecycleKey("demo", 0), finish_result_id=finished["finish_result_id"], inventory_id=finished["inventory_id"]).resolution_kind == "ordinary_cleanup"
    fallback = json.loads(FINISH.manual_result_path(repo, key).read_text())
    assert fallback["finish_result_id"] == finished["finish_result_id"]
    assert fallback["head_branch"] == "codex/demo"
    validate_json(fallback, PACKAGE / "schemas/manual-finish-result.schema.json", "manual_finish_result")
    repeated = invoke()
    assert repeated["exit_id"] == "success"
    cleanup_package = PACKAGE.parent / "guru-cleanup-task-resources"
    cleanup_spec = importlib.util.spec_from_file_location("guru_cleanup_after_finish", cleanup_package / "runtime/invoke.py")
    assert cleanup_spec and cleanup_spec.loader
    cleanup = importlib.util.module_from_spec(cleanup_spec)
    cleanup_spec.loader.exec_module(cleanup)
    cleanup_input = tmp_path / "cleanup-input.json"
    cleanup_semantic = tmp_path / "cleanup-semantic.json"
    cleanup_input.write_text(json.dumps({"profile": "normal", "mode": "standalone", **{key: finished[key] for key in ("task_id", "lifecycle_generation", "finish_result_id", "inventory_id")}}))
    cleanup_semantic.write_text(json.dumps({"profile": "normal", "mode": "standalone", "route": {"typed_exit": "cleaned"}}))
    ledger_path = store.path_for(key)
    sealed_ledger = ledger_path.read_bytes()
    ledger_path.unlink()
    missing_ledger = cleanup.run(cleanup_package, {}, ["--root", str(repo), "--input", str(cleanup_input),
                                                        "--semantic-result", str(cleanup_semantic)])
    assert missing_ledger["exit_id"] == "manual_cleanup_required", missing_ledger
    ledger_path.write_bytes(sealed_ledger)
    git(repo, "switch", "-q", "main")
    assert cleanup.run(cleanup_package, {}, ["--root", str(repo), "--input", str(cleanup_input),
                                             "--semantic-result", str(cleanup_semantic), "--confirmed-cleanup"])["exit_id"] == "cleaned"
    assert store.read(key).resources[0].state == "resolved"
    log = (tmp_path / "gh.log").read_text()
    assert log.count('"create"') == 1 and log.count('"merge"') == 1 and '--match-head-commit' in log
    target = git(repo, "rev-parse", "refs/remotes/origin/main")
    assert subprocess.run(["git", "cat-file", "-e", f"{target}:{archive_ref}/finish-summary.json"], cwd=repo).returncode == 0
    assert subprocess.run(["git", "cat-file", "-e", f"{target}:.trellis/tasks/demo/task.json"], cwd=repo).returncode != 0


@pytest.mark.parametrize("task_ref", [".trellis/tasks/09-19-demo", ".trellis/tasks/09-19-renamed"])
def test_finish_accepts_mutable_task_locator_with_stable_task_id(tmp_path, task_ref):
    repo = tmp_path / "repo"; repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "--allow-empty", "-qm", "seed"], cwd=repo, check=True)
    task_dir = repo / task_ref; task_dir.mkdir(parents=True)
    (task_dir / "task.json").write_text(json.dumps({"id":"demo","status":"in_progress","lifecycle_generation":1,"source":{"kind":"no_issue"}}) + "\n")
    archive_ref = ".trellis/tasks/archive/2026-09/" + Path(task_ref).name
    FINISH.project_archive(repo, {"task_ref": task_ref, "task_id": "demo"}, Path(task_ref), archive_ref, Path(archive_ref))
    assert not task_dir.exists()
    assert (repo / archive_ref / "task.json").is_file()
    assert "archive_dir" not in json.loads((repo / archive_ref / "task.json").read_text())


def test_finish_archive_is_discoverable_by_source_issue(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "--allow-empty", "-qm", "seed"], cwd=repo, check=True)
    task_ref = ".trellis/tasks/demo"
    task_dir = repo / task_ref
    task_dir.mkdir(parents=True)
    (task_dir / "task.json").write_text(json.dumps({"id": "demo", "title": "Completed task", "status": "in_progress", "lifecycle_generation": 0, "source": {"kind": "issue", "repo_ref": "example/repo", "number": 454, "disposition": "reference_only"}}) + "\n")
    (task_dir / "prd.md").write_text("task requirements\n")
    archive_ref = ".trellis/tasks/archive/2026-09/demo"
    FINISH.project_archive(repo, {"task_ref": task_ref, "task_id": "demo"}, Path(task_ref), archive_ref, Path(archive_ref))
    summary = json.loads((repo / archive_ref / "finish-summary.json").read_text())
    assert summary["index"]["search_terms"]["issue_refs"] == ["#454"]
    assert f"{archive_ref}/prd.md" in summary["index"]["search_terms"]["paths"]

    schema = repo / ".trellis/guru-team/schemas/finish-summary.schema.json"
    schema.parent.mkdir(parents=True)
    shutil.copyfile(ROOT.parents[2] / ".trellis/guru-team/schemas/finish-summary.schema.json", schema)
    discovery = PACKAGE.parent / "guru-discover-change-context" / "runtime/common.py"
    spec = importlib.util.spec_from_file_location("guru_discover_history_for_finish", discovery)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    preview = module.preview(repo, {"issue_refs": ["#454"]}, 20)
    assert [row["finish_summary_path"] for row in preview["candidates"]] == [f"{archive_ref}/finish-summary.json"]


def test_finish_rejects_legacy_task_without_rewriting_source(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    task_ref = ".trellis/tasks/demo"
    task_dir = repo / task_ref
    task_dir.mkdir(parents=True)
    metadata = task_dir / "task.json"
    metadata.write_text(json.dumps({"id": "demo", "status": "in_progress",
                                    "lifecycle_generation": 0, "scope": "GitHub Issue #454"}))
    before = metadata.read_bytes()
    source = {"kind": "issue", "repo_ref": "example/repo", "number": 454,
              "disposition": "reference_only"}
    with pytest.raises(CommandError, match="stale_identity"):
        FINISH.closure_source_current(repo, {"task_id": "demo", "lifecycle_generation": 0}, source)
    assert metadata.read_bytes() == before
    assert not (repo / ".trellis/tasks/archive/2026-09/demo").exists()


def test_finish_archive_retires_only_its_generation_sessions(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                    "commit", "--allow-empty", "-qm", "seed"], cwd=repo, check=True)
    shutil.copytree(ROOT.parents[2] / ".trellis/scripts/common", repo / ".trellis/scripts/common",
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    task_ref = ".trellis/tasks/demo"
    task_dir = repo / task_ref
    task_dir.mkdir(parents=True)
    (task_dir / "task.json").write_text(json.dumps({
        "id": "demo", "title": "Demo", "status": "in_progress", "lifecycle_generation": 1,
        "source": {"kind": "no_issue"},
    }) + "\n")
    sessions = inspect_repository(repo).common_dir / "trellis/sessions"
    sessions.mkdir(parents=True)
    current = sessions / "codex_finished.json"
    other = sessions / "codex_other.json"
    current.write_text(json.dumps({"schema_version": 2, "task_id": "demo", "lifecycle_generation": 1}))
    other.write_text(json.dumps({"schema_version": 2, "task_id": "other", "lifecycle_generation": 0}))

    archive_ref = ".trellis/tasks/archive/2026-09/demo"
    FINISH.project_archive(repo, {"task_ref": task_ref, "task_id": "demo"}, Path(task_ref), archive_ref, Path(archive_ref))

    assert not current.exists() and other.is_file()
    probe = subprocess.run(
        [sys.executable, "-c", "from pathlib import Path; from common.active_task import resolve_active_task; "
         "a = resolve_active_task(Path('.')); print(a.task_path, a.error)"],
        cwd=repo, env={**os.environ, "PYTHONPATH": str(repo / ".trellis/scripts"),
                       "TRELLIS_CONTEXT_ID": "codex_finished"},
        text=True, capture_output=True, check=True,
    )
    assert probe.stdout.strip() == "None None"


def test_finish_archive_keeps_active_task_when_official_session_api_is_missing(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    task_ref = ".trellis/tasks/demo"
    task_dir = repo / task_ref
    task_dir.mkdir(parents=True)
    (task_dir / "task.json").write_text(json.dumps({
        "id": "demo", "status": "in_progress", "lifecycle_generation": 0,
        "source": {"kind": "no_issue"},
    }))
    session = inspect_repository(repo).common_dir / "trellis/sessions/codex_finished.json"
    session.parent.mkdir(parents=True)
    session.write_text(json.dumps({"schema_version": 2, "task_id": "demo", "lifecycle_generation": 0}))

    archive_ref = ".trellis/tasks/archive/2026-09/demo"
    with pytest.raises(CommandError) as caught:
        FINISH.project_archive(repo, {"task_ref": task_ref, "task_id": "demo"}, Path(task_ref), archive_ref, Path(archive_ref))
    assert caught.value.code == "official_session_unavailable"
    assert task_dir.is_dir() and session.is_file()
    assert not (repo / archive_ref).exists()


def test_finish_archive_keeps_active_task_when_official_session_method_is_missing(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    common = repo / ".trellis/scripts/common"
    common.mkdir(parents=True)
    (common / "__init__.py").write_text("class ActiveTask: pass\nactive_task = ActiveTask()\n")
    task_ref = ".trellis/tasks/demo"
    task_dir = repo / task_ref
    task_dir.mkdir(parents=True)
    (task_dir / "task.json").write_text(json.dumps({
        "id": "demo", "status": "in_progress", "lifecycle_generation": 0,
        "source": {"kind": "no_issue"},
    }))
    session = inspect_repository(repo).common_dir / "trellis/sessions/codex_finished.json"
    session.parent.mkdir(parents=True)
    session.write_text(json.dumps({"schema_version": 2, "task_id": "demo", "lifecycle_generation": 0}))

    archive_ref = ".trellis/tasks/archive/2026-09/demo"
    with pytest.raises(CommandError) as caught:
        FINISH.project_archive(repo, {"task_ref": task_ref, "task_id": "demo"}, Path(task_ref), archive_ref, Path(archive_ref))
    assert caught.value.code == "official_session_unavailable"
    assert task_dir.is_dir() and session.is_file()
    assert not (repo / archive_ref).exists()


def test_original_private_transaction_projects_same_operation_without_base_field(tmp_path):
    public = {"task_ref": ".trellis/tasks/demo", "task_id": "demo",
              "closure_result": {"result_id": "closure:demo"}}
    bookkeeping = {"repo_ref": "example/repo", "base_branch": "main", "head_branch": "codex/demo"}
    transaction = {"schema_version": "2.0", "stage": "committed",
                   "task_ref": public["task_ref"], "task_id": "demo", "closure_result_id": "closure:demo",
                   "finish_ref": FINISH.finish_ref(public, 0), "lifecycle_generation": 0,
                   **bookkeeping, "expected_base_head": "1" * 40,
                   "archive_ref": ".trellis/tasks/archive/2026-10/demo",
                   "parent_head": "2" * 40, "commit": "3" * 40}
    path = tmp_path / "transaction.json"
    path.write_text(json.dumps(transaction))
    projected = FINISH.read_transaction(path, public, bookkeeping, PACKAGE, 0)
    assert projected == {key: value for key, value in transaction.items() if key not in {"schema_version", "expected_base_head"}} | {"schema_version": "3.0"}
    assert json.loads(path.read_text()) == transaction
    FINISH.write_transaction(path, projected, PACKAGE)
    assert FINISH.read_transaction(path, public, bookkeeping, PACKAGE, 0) == projected
