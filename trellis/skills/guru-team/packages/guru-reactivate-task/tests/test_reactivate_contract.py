import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from runtime.schema import validate_json

PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parents[1]


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=True).stdout.strip()


def repository(tmp_path):
    repo = tmp_path / "repo"
    remote = tmp_path / "remote.git"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    subprocess.run(["git", "init", "-q", "--bare", remote], check=True)
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Test")
    git(repo, "remote", "add", "origin", str(remote))
    (repo / ".gitignore").write_text(".trellis/.runtime/\n")
    archive = repo / ".trellis/tasks/archive/2026-09/demo"
    archive.mkdir(parents=True)
    (archive / "task.json").write_text(json.dumps({"id": "demo", "status": "completed", "completedAt": "2026-09-18"}))
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "archived task")
    git(repo, "push", "-q", "-u", "origin", "main")
    head = git(repo, "rev-parse", "HEAD")
    git(repo, "switch", "-qc", "codex/demo-existing")
    return repo, head


def invocation(repo, semantic, confirmed=True):
    public = {"profile": "reactivate_completed_task", "mode": "standalone", "task_ref": ".trellis/tasks/demo", "archive_ref": ".trellis/tasks/archive/2026-09/demo", "task_id": "demo"}
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


def test_reactivate_reuses_exact_workspace_and_invalidates_old_finish(tmp_path):
    repo, head = repository(tmp_path)
    receipt = repo / ".trellis/.runtime/guru-team/finish/old.json"
    receipt.parent.mkdir(parents=True)
    receipt.write_text(json.dumps({"task_ref": ".trellis/tasks/demo", "finish_ref": "finish:v1:old"}))
    blocked = invocation(repo, semantic(repo, "codex/demo-existing", head), confirmed=False)
    assert blocked.returncode == 4 and (repo / ".trellis/tasks/archive/2026-09/demo").exists()
    completed = invocation(repo, semantic(repo, "codex/demo-existing", head))
    output = json.loads(completed.stdout)
    task = json.loads((repo / ".trellis/tasks/demo/task.json").read_text())
    assert completed.returncode == 0 and output["exit_id"] == "reactivated_to_evidence_refresh"
    assert task["status"] == "in_progress" and task["completedAt"] is None and task["worktree_path"] == str(repo)
    assert not (repo / ".trellis/tasks/archive/2026-09/demo").exists() and not receipt.exists()
    assert (repo / ".trellis/.runtime/guru-team/workspaces/demo.json").is_file()


def test_reactivate_creates_new_workspace_from_current_base(tmp_path):
    repo, head = repository(tmp_path)
    workspace = tmp_path / "worktrees" / "demo"
    completed = invocation(repo, semantic(workspace, "codex/demo-reactivated", head, "create_new"))
    output = json.loads(completed.stdout)
    task = json.loads((workspace / ".trellis/tasks/demo/task.json").read_text())
    assert completed.returncode == 0 and output["task_id"] == "demo"
    assert git(workspace, "branch", "--show-current") == "codex/demo-reactivated"
    assert task["branch"] == "codex/demo-reactivated" and task["worktree_path"] == str(workspace)
    assert (repo / ".trellis/.runtime/guru-team/tasks/demo.json").is_file()
