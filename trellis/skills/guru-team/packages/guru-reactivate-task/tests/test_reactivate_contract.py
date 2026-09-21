import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.schema import validate_json

PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parents[1]
TASK_ID = "demo"
DATE_PREFIXED_LOCATOR = "09-19-demo"


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=True).stdout.strip()


def repository(tmp_path, locator_basename=TASK_ID, archive_task_id=TASK_ID):
    repo = tmp_path / "repo"
    remote = tmp_path / "remote.git"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    subprocess.run(["git", "init", "-q", "--bare", remote], check=True)
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Test")
    git(repo, "remote", "add", "origin", str(remote))
    (repo / ".gitignore").write_text(".trellis/.runtime/\n")
    archive = repo / ".trellis/tasks/archive/2026-09" / locator_basename
    archive.mkdir(parents=True)
    (archive / "task.json").write_text(json.dumps({"id": archive_task_id, "status": "completed", "completedAt": "2026-09-18"}))
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "archived task")
    git(repo, "push", "-q", "-u", "origin", "main")
    head = git(repo, "rev-parse", "HEAD")
    git(repo, "switch", "-qc", "codex/demo-existing")
    return repo, head


def public_input(locator_basename=TASK_ID, archive_locator_basename=None):
    archive_locator_basename = archive_locator_basename or locator_basename
    return {
        "profile": "reactivate_completed_task",
        "mode": "standalone",
        "task_ref": f".trellis/tasks/{locator_basename}",
        "archive_ref": f".trellis/tasks/archive/2026-09/{archive_locator_basename}",
        "task_id": TASK_ID,
    }


def invocation(repo, semantic, confirmed=True, public=None):
    public = public or public_input()
    input_path = repo.parent / "input.json"
    semantic_path = repo.parent / "semantic.json"
    input_path.write_text(json.dumps(public))
    semantic_path.write_text(json.dumps(semantic))
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    command = [sys.executable, str(PACKAGE / "runtime/invoke.py"), "--root", str(repo), "--input", str(input_path), "--semantic-result", str(semantic_path)]
    if confirmed:
        command.append("--confirmed-reactivation")
    return subprocess.run(command, text=True, capture_output=True, env=env)


def semantic(workspace, branch, head, disposition="reuse_exact"):
    return {
        "profile": "reactivate_completed_task",
        "mode": "standalone",
        "reason_refs": ["new evidence"],
        "workspace": {
            "disposition": disposition,
            "workspace_path": str(workspace),
            "branch_name": branch,
            "base_branch": "main",
            "base_head": head,
            "workspace_mapping": ".trellis/.runtime/guru-team/workspaces/demo.json",
            "task_mapping": ".trellis/.runtime/guru-team/tasks/demo.json",
        },
        "route": {"typed_exit": "reactivated_to_evidence_refresh"},
    }


def test_contract_assets():
    validate_json(json.loads((PACKAGE / "interface.json").read_text()), ROOT / "schemas/skill-interface-1.4.schema.json", "interface")


def test_skill_route_projections_close_against_consumer_inputs():
    interface = json.loads((PACKAGE / "interface.json").read_text())
    contracts = interface["public_contracts"]
    outputs = {
        "reactivated_to_requirements": {"exit_id": "reactivated_to_requirements", "task_ref": ".trellis/tasks/demo", "resume_target": "requirements"},
        "reactivated_to_evidence_refresh": {"exit_id": "reactivated_to_evidence_refresh", "task_ref": ".trellis/tasks/demo", "resume_target": "evidence-refresh"},
    }
    consumer_schemas = {
        "requirements": ROOT / "packages/guru-clarify-requirements/schemas/public-active-task-scope-change-input.schema.json",
        "evidence": ROOT / "packages/guru-review-task-completion/schemas/public-input.schema.json",
    }
    consumers = {row["id"]: row for row in contracts["consumer_inputs"]}
    for projection in contracts["projections"]:
        if projection["consumer_input_id"] not in consumer_schemas:
            continue
        contract = consumers[projection["consumer_input_id"]]["contract"]
        authored = json.loads((PACKAGE / contract["authoring_example"]["path"]).read_text())
        source = outputs[projection["exit_id"]]
        projected = {mapping["target"]: source[mapping["source"]] for mapping in projection["mappings"]}
        validate_json({**authored, **projected}, consumer_schemas[projection["consumer_input_id"]], projection["consumer_input_id"])


def test_reactivate_reuses_exact_workspace_and_invalidates_old_finish(tmp_path):
    repo, head = repository(tmp_path)
    receipt = repo / ".trellis/.runtime/guru-team/finish/old.json"
    receipt.parent.mkdir(parents=True)
    receipt.write_text(json.dumps({"task_ref": ".trellis/tasks/demo", "finish_ref": "finish:v1:old"}))
    cleanup_receipt = repo / ".trellis/.runtime/guru-team/cleanup/old.json"
    cleanup_receipt.parent.mkdir(parents=True, exist_ok=True)
    cleanup_receipt.write_text(json.dumps({"task_ref": ".trellis/tasks/demo", "finish_ref": "finish:v1:old"}))
    blocked = invocation(repo, semantic(repo, "codex/demo-existing", head), confirmed=False)
    assert blocked.returncode == 4 and (repo / ".trellis/tasks/archive/2026-09/demo").exists()
    completed = invocation(repo, semantic(repo, "codex/demo-existing", head))
    output = json.loads(completed.stdout)
    task = json.loads((repo / ".trellis/tasks/demo/task.json").read_text())
    assert completed.returncode == 0 and output["exit_id"] == "reactivated_to_evidence_refresh"
    assert task["status"] == "in_progress" and task["completedAt"] is None and task["worktree_path"] == str(repo)
    assert task["lifecycle_generation"] == 1
    assert not (repo / ".trellis/tasks/archive/2026-09/demo").exists() and not receipt.exists()
    assert not cleanup_receipt.exists()
    workspace_mapping = json.loads((repo / ".trellis/.runtime/guru-team/workspaces/demo.json").read_text())
    task_mapping = json.loads((repo / ".trellis/.runtime/guru-team/tasks/demo.json").read_text())
    assert workspace_mapping["workspace_slug"] == "demo"
    assert task_mapping["task_slug"] == "demo" and task_mapping["workspace_slug"] == "demo"


def test_reactivate_creates_new_workspace_from_current_base(tmp_path):
    repo, head = repository(tmp_path)
    workspace = tmp_path / "worktrees" / "demo"
    completed = invocation(repo, semantic(workspace, "codex/demo-reactivated", head, "create_new"))
    output = json.loads(completed.stdout)
    task = json.loads((workspace / ".trellis/tasks/demo/task.json").read_text())
    assert completed.returncode == 0 and output == {
        "exit_id": "reactivated_to_evidence_refresh",
        "task_ref": ".trellis/tasks/demo",
        "resume_target": "evidence-refresh",
        "lifecycle_generation": 1,
    }
    assert git(workspace, "branch", "--show-current") == "codex/demo-reactivated"
    assert task["branch"] == "codex/demo-reactivated" and task["worktree_path"] == str(workspace)
    assert (repo / ".trellis/.runtime/guru-team/tasks/demo.json").is_file()


def test_reactivate_reuses_exact_workspace_with_date_prefixed_locator(tmp_path):
    repo, head = repository(tmp_path, DATE_PREFIXED_LOCATOR)
    public = public_input(DATE_PREFIXED_LOCATOR)

    completed = invocation(repo, semantic(repo, "codex/demo-existing", head), public=public)

    output = json.loads(completed.stdout)
    task = json.loads((repo / ".trellis/tasks" / DATE_PREFIXED_LOCATOR / "task.json").read_text())
    assert completed.returncode == 0 and output["task_ref"] == f".trellis/tasks/{DATE_PREFIXED_LOCATOR}"
    assert task["id"] == TASK_ID and task["status"] == "in_progress"
    assert not (repo / ".trellis/tasks/archive/2026-09" / DATE_PREFIXED_LOCATOR).exists()
    assert json.loads((repo / ".trellis/.runtime/guru-team/workspaces/demo.json").read_text())["workspace_slug"] == TASK_ID
    assert json.loads((repo / ".trellis/.runtime/guru-team/tasks/demo.json").read_text())["task_slug"] == TASK_ID


def test_reactivate_creates_new_workspace_with_date_prefixed_locator(tmp_path):
    repo, head = repository(tmp_path, DATE_PREFIXED_LOCATOR)
    workspace = tmp_path / "worktrees" / "demo"
    public = public_input(DATE_PREFIXED_LOCATOR)

    completed = invocation(repo, semantic(workspace, "codex/demo-reactivated", head, "create_new"), public=public)

    output = json.loads(completed.stdout)
    task = json.loads((workspace / ".trellis/tasks" / DATE_PREFIXED_LOCATOR / "task.json").read_text())
    assert completed.returncode == 0 and output["task_ref"] == f".trellis/tasks/{DATE_PREFIXED_LOCATOR}"
    assert git(workspace, "branch", "--show-current") == "codex/demo-reactivated"
    assert task["id"] == TASK_ID and task["status"] == "in_progress"
    assert not (workspace / ".trellis/tasks/archive/2026-09" / DATE_PREFIXED_LOCATOR).exists()
    assert (repo / ".trellis/.runtime/guru-team/tasks/demo.json").is_file()


def assert_output_loss_recovery(tmp_path, disposition, locator_basename):
    repo, head = repository(tmp_path, locator_basename)
    public = public_input(locator_basename)
    if disposition == "reuse_exact":
        workspace = repo
        branch = "codex/demo-existing"
    else:
        workspace = tmp_path / "worktrees" / "demo"
        branch = "codex/demo-reactivated"
    reviewed = semantic(workspace, branch, head, disposition)
    receipt = repo / ".trellis/.runtime/guru-team/finish/old.json"
    receipt.parent.mkdir(parents=True)
    receipt.write_text(json.dumps({"task_ref": public["task_ref"], "finish_ref": "finish:v1:old"}))

    first = invocation(repo, reviewed, public=public)
    assert first.returncode == 0
    expected_output = json.loads(first.stdout)
    worktrees_before = git(repo, "worktree", "list", "--porcelain")
    task_path = workspace / ".trellis/tasks" / locator_basename / "task.json"
    task_before = task_path.read_text()
    mappings_before = {
        path: path.read_text()
        for path in {
            repo / ".trellis/.runtime/guru-team/workspaces/demo.json",
            repo / ".trellis/.runtime/guru-team/tasks/demo.json",
            workspace / ".trellis/.runtime/guru-team/workspaces/demo.json",
            workspace / ".trellis/.runtime/guru-team/tasks/demo.json",
        }
    }

    recovered = invocation(repo, reviewed, public=public)

    assert recovered.returncode == 0 and json.loads(recovered.stdout) == expected_output
    assert git(repo, "worktree", "list", "--porcelain") == worktrees_before
    assert task_path.read_text() == task_before
    assert all(path.read_text() == content for path, content in mappings_before.items())
    assert not (workspace / ".trellis/tasks/archive/2026-09" / locator_basename).exists()
    assert not receipt.exists()


@pytest.mark.parametrize("disposition", ["reuse_exact", "create_new"])
def test_reactivate_recovers_same_output_after_stdout_loss_without_duplicate_mutation(tmp_path, disposition):
    assert_output_loss_recovery(tmp_path, disposition, TASK_ID)


@pytest.mark.parametrize("disposition", ["reuse_exact", "create_new"])
def test_reactivate_recovers_date_prefixed_output_after_stdout_loss_without_duplicate_mutation(tmp_path, disposition):
    assert_output_loss_recovery(tmp_path, disposition, DATE_PREFIXED_LOCATOR)


@pytest.mark.parametrize(
    ("public_change", "semantic_change", "field_path"),
    [
        ({"task_ref": ".trellis/tasks/other"}, {}, "archive_ref"),
        ({"archive_ref": ".trellis/tasks/archive/2026-09/other"}, {}, "archive_ref"),
        ({}, {"workspace_mapping": ".trellis/.runtime/guru-team/workspaces/other.json"}, "workspace.workspace_mapping"),
        ({}, {"task_mapping": ".trellis/.runtime/guru-team/tasks/other.json"}, "workspace.task_mapping"),
    ],
)
def test_reactivate_rejects_locator_identity_mismatch(tmp_path, public_change, semantic_change, field_path):
    repo, head = repository(tmp_path)
    public = public_input()
    public.update(public_change)
    reviewed = semantic(repo, "codex/demo-existing", head)
    reviewed["workspace"].update(semantic_change)

    result = invocation(repo, reviewed, public=public)

    error = json.loads(result.stderr)
    assert result.returncode == 3 and error["code"] == "stale_identity" and error["field_path"] == field_path
    assert (repo / ".trellis/tasks/archive/2026-09/demo").is_dir()
    assert not (repo / ".trellis/tasks/demo").exists()


def test_reactivate_rejects_active_archive_basename_mismatch_without_mutation(tmp_path):
    repo, head = repository(tmp_path, DATE_PREFIXED_LOCATOR)
    public = public_input(DATE_PREFIXED_LOCATOR, "09-20-demo")

    result = invocation(repo, semantic(repo, "codex/demo-existing", head), public=public)

    error = json.loads(result.stderr)
    assert result.returncode == 3 and error["code"] == "stale_identity" and error["field_path"] == "archive_ref"
    assert (repo / ".trellis/tasks/archive/2026-09" / DATE_PREFIXED_LOCATOR).is_dir()
    assert not (repo / ".trellis/tasks" / DATE_PREFIXED_LOCATOR).exists()
    assert not (repo / ".trellis/.runtime/guru-team/workspaces/demo.json").exists()
    assert not (repo / ".trellis/.runtime/guru-team/tasks/demo.json").exists()


def test_reactivate_rejects_archive_task_id_mismatch_before_move(tmp_path):
    repo, head = repository(tmp_path, DATE_PREFIXED_LOCATOR, archive_task_id="other")
    public = public_input(DATE_PREFIXED_LOCATOR)

    result = invocation(repo, semantic(repo, "codex/demo-existing", head), public=public)

    error = json.loads(result.stderr)
    assert result.returncode == 3 and error["code"] == "stale_identity" and error["field_path"] == "archive_ref"
    assert (repo / ".trellis/tasks/archive/2026-09" / DATE_PREFIXED_LOCATOR).is_dir()
    assert not (repo / ".trellis/tasks" / DATE_PREFIXED_LOCATOR).exists()
    assert not (repo / ".trellis/.runtime/guru-team/workspaces/demo.json").exists()
    assert not (repo / ".trellis/.runtime/guru-team/tasks/demo.json").exists()


def test_reactivate_fast_forwards_finish_branch_to_real_merge_commit(tmp_path):
    repo = tmp_path / "repo"
    remote = tmp_path / "remote.git"
    workspace = tmp_path / "worktrees" / "demo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    subprocess.run(["git", "init", "-q", "--bare", remote], check=True)
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Test")
    git(repo, "remote", "add", "origin", str(remote))
    (repo / ".gitignore").write_text(".trellis/.runtime/\n")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "base")
    git(repo, "push", "-q", "-u", "origin", "main")
    workspace.parent.mkdir()
    git(repo, "worktree", "add", "-qb", "codex/demo-finish", str(workspace), "main")
    archive = workspace / ".trellis/tasks/archive/2026-09/demo"
    archive.mkdir(parents=True)
    (archive / "task.json").write_text(json.dumps({"id": "demo", "status": "completed", "completedAt": "2026-09-19"}))
    git(workspace, "add", ".")
    git(workspace, "commit", "-qm", "persist finish")
    finish_head = git(workspace, "rev-parse", "HEAD")
    git(repo, "merge", "--no-ff", "codex/demo-finish", "-m", "merge finish")
    merge_head = git(repo, "rev-parse", "HEAD")
    git(repo, "push", "-q", "origin", "main")

    completed = invocation(repo, semantic(workspace, "codex/demo-finish", merge_head))

    output = json.loads(completed.stdout)
    assert completed.returncode == 0 and output["exit_id"] == "reactivated_to_evidence_refresh"
    assert finish_head != merge_head and git(workspace, "rev-parse", "HEAD") == merge_head
    assert git(workspace, "merge-base", "--is-ancestor", finish_head, merge_head) == ""
    assert (workspace / ".trellis/tasks/demo/task.json").is_file()
    assert not (workspace / ".trellis/tasks/archive/2026-09/demo").exists()
