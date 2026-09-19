import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from runtime.schema import validate_json


PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parents[1]
FINISH_REF = "finish:v1:0123456789abcdef"
LIFECYCLE_GENERATION = 0
TASK_REF = ".trellis/tasks/demo"
ARCHIVE_REF = ".trellis/tasks/archive/2026-09/demo"


def git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=True)


def init_repo(path: Path) -> str:
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=path, check=True)
    git(path, "config", "user.email", "test@example.com")
    git(path, "config", "user.name", "Test")
    (path / "tracked").write_text("base\n")
    git(path, "add", "tracked")
    git(path, "commit", "-qm", "base")
    head = git(path, "rev-parse", "HEAD").stdout.strip()
    git(path, "update-ref", "refs/remotes/origin/main", head)
    return head


def write_finish_receipt(root: Path, head: str, head_branch: str = "codex/demo") -> Path:
    receipt = root / ".trellis/.runtime/guru-team/finish/0123456789abcdef.json"
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "stage": "success",
                "task_ref": TASK_REF,
                "closure_ref": "closure:v1:demo",
                "finish_ref": FINISH_REF,
                "lifecycle_generation": LIFECYCLE_GENERATION,
                "repo_ref": "example/repo",
                "base_branch": "main",
                "head_branch": head_branch,
                "expected_base_head": head,
                "archive_ref": ARCHIVE_REF,
                "parent_head": head,
                "commit": head,
                "pr_number": 1,
                "pr_url": "https://github.com/example/repo/pull/1",
                "target_head": head,
            }
        )
        + "\n"
    )
    return receipt


def invocation(tmp_path: Path, root: Path, public: dict, semantic: dict) -> list[str]:
    input_path = tmp_path / "input.json"
    semantic_path = tmp_path / "semantic.json"
    input_path.write_text(json.dumps(public))
    semantic_path.write_text(json.dumps(semantic))
    return [
        sys.executable,
        str(PACKAGE / "runtime/invoke.py"),
        "--root",
        str(root),
        "--input",
        str(input_path),
        "--semantic-result",
        str(semantic_path),
    ]


def run(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    return subprocess.run(command, text=True, capture_output=True, env=env, check=check)


def public_input(resources: list[dict], source_exit: str = "success") -> dict:
    return {
        "profile": "finish_success",
        "source_exit": source_exit,
        "mode": "standalone",
        "task_ref": TASK_REF,
        "archive_ref": ARCHIVE_REF,
        "finish_ref": FINISH_REF,
        "lifecycle_generation": LIFECYCLE_GENERATION,
        "resources": resources,
    }


def semantic_result(resources: list[dict], exit_id: str = "cleaned") -> dict:
    route = {"typed_exit": exit_id}
    if exit_id != "cleaned":
        route.update({"reason_code": "cleanup_pending", "remediation": "Rediscover remaining resources."})
    return {
        "profile": "finish_success",
        "mode": "standalone",
        "owned_resources": resources,
        "route": route,
    }


def test_contract_assets():
    validate_json(
        json.loads((PACKAGE / "interface.json").read_text()),
        ROOT / "schemas/skill-interface-1.4.schema.json",
        "interface",
    )
    validate_json(
        json.loads((PACKAGE / "examples/public-input.json").read_text()),
        PACKAGE / "schemas/public-input.schema.json",
        "public_input_example",
    )
    validate_json(
        json.loads((PACKAGE / "examples/semantic-result.json").read_text()),
        PACKAGE / "schemas/semantic-result.schema.json",
        "semantic_result_example",
    )


def test_cleanup_requires_confirmation_and_recovers_cleaned_stdout_loss(tmp_path):
    repo = tmp_path / "repo"
    head = init_repo(repo)
    (repo / ARCHIVE_REF).mkdir(parents=True)
    (repo / ARCHIVE_REF / "task.json").write_text(json.dumps({"id": "demo", "status": "completed", "lifecycle_generation": 0}) + "\n")
    runtime = repo / ".trellis/.runtime/guru-team/demo.json"
    runtime.parent.mkdir(parents=True, exist_ok=True)
    runtime.write_text(json.dumps({"task_ref": TASK_REF}) + "\n")
    finish_receipt = write_finish_receipt(repo, head)
    resources = [{"kind": "runtime", "locator": ".trellis/.runtime/guru-team/demo.json"}]
    command = invocation(tmp_path, repo, public_input(resources), semantic_result(resources))

    pending = json.loads(run(command).stdout)
    assert pending == {
        "exit_id": "remaining_resources",
        "task_ref": TASK_REF,
        "archive_ref": ARCHIVE_REF,
        "finish_ref": FINISH_REF,
        "lifecycle_generation": LIFECYCLE_GENERATION,
    }
    assert runtime.exists()

    cleaned = json.loads(run(command + ["--confirmed-cleanup"]).stdout)
    assert cleaned == {"exit_id": "cleaned"}
    assert not runtime.exists()
    assert not finish_receipt.exists()
    cleanup_receipt = repo / ".trellis/.runtime/guru-team/cleanup/0123456789abcdef.json"
    assert cleanup_receipt.is_file()
    assert json.loads(cleanup_receipt.read_text())["lifecycle_generation"] == 0

    recovered = json.loads(run(command + ["--confirmed-cleanup"]).stdout)
    assert recovered == {"exit_id": "cleaned"}


def test_cleanup_rejects_terminal_receipt_from_previous_lifecycle_generation(tmp_path):
    repo = tmp_path / "repo"
    head = init_repo(repo)
    archive = repo / ARCHIVE_REF
    archive.mkdir(parents=True)
    (archive / "task.json").write_text(json.dumps({"id": "demo", "status": "completed", "lifecycle_generation": 0}) + "\n")
    finish_receipt = write_finish_receipt(repo, head)
    resources: list[dict] = []
    command = invocation(tmp_path, repo, public_input(resources), semantic_result(resources))
    assert json.loads(run(command).stdout) == {"exit_id": "cleaned"}
    cleanup_receipt = repo / ".trellis/.runtime/guru-team/cleanup/0123456789abcdef.json"
    assert cleanup_receipt.is_file()

    (archive / "task.json").write_text(json.dumps({"id": "demo", "status": "completed", "lifecycle_generation": 1}) + "\n")
    stale_input = public_input(resources)
    stale_input["lifecycle_generation"] = 1
    stale_command = invocation(tmp_path, repo, stale_input, semantic_result(resources))
    result = run(stale_command, check=False)
    assert result.returncode == 3
    error = json.loads(result.stderr)
    assert error["code"] == "stale_identity"
    assert error["field_path"] == "cleanup_receipt"
    assert cleanup_receipt.is_file()


def test_cleanup_accepts_empty_or_already_absent_owned_set(tmp_path):
    repo = tmp_path / "repo"
    head = init_repo(repo)
    (repo / ARCHIVE_REF).mkdir(parents=True)
    finish_receipt = write_finish_receipt(repo, head)
    resources: list[dict] = []
    command = invocation(tmp_path, repo, public_input(resources), semantic_result(resources))

    cleaned = json.loads(run(command).stdout)
    assert cleaned == {"exit_id": "cleaned"}
    assert not finish_receipt.exists()


def test_cleanup_accepts_reviewed_resource_that_is_already_absent(tmp_path):
    repo = tmp_path / "repo"
    head = init_repo(repo)
    (repo / ARCHIVE_REF).mkdir(parents=True)
    finish_receipt = write_finish_receipt(repo, head)
    resources = [{"kind": "runtime", "locator": ".trellis/.runtime/guru-team/already-absent.json"}]
    command = invocation(tmp_path, repo, public_input(resources), semantic_result(resources))

    cleaned = json.loads(run(command).stdout)
    assert cleaned == {"exit_id": "cleaned"}
    assert not finish_receipt.exists()


def test_remaining_resources_route_survives_missing_finish_receipt(tmp_path):
    repo = tmp_path / "repo"
    init_repo(repo)
    resources: list[dict] = []
    command = invocation(
        tmp_path,
        repo,
        public_input(resources, source_exit="remaining_resources"),
        semantic_result(resources, exit_id="remaining_resources"),
    )

    result = json.loads(run(command).stdout)
    assert result == {
        "exit_id": "remaining_resources",
        "task_ref": TASK_REF,
        "archive_ref": ARCHIVE_REF,
        "finish_ref": FINISH_REF,
        "lifecycle_generation": LIFECYCLE_GENERATION,
    }


def test_cleanup_deletes_only_exact_finish_remote_branch_and_tracking_ref(tmp_path):
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", "-q", str(remote)], check=True)
    repo = tmp_path / "repo"
    init_repo(repo)
    git(repo, "switch", "-c", "codex/demo")
    (repo / "tracked").write_text("finish\n")
    git(repo, "commit", "-qam", "finish")
    head = git(repo, "rev-parse", "HEAD").stdout.strip()
    git(repo, "switch", "main")
    git(repo, "merge", "--ff-only", "codex/demo")
    git(repo, "remote", "add", "origin", str(remote))
    git(repo, "push", "-u", "origin", "main")
    git(repo, "push", "-u", "origin", "codex/demo")
    git(repo, "fetch", "origin")
    (repo / ARCHIVE_REF).mkdir(parents=True)
    write_finish_receipt(repo, head)

    wrong = [{"kind": "remote_branch", "locator": "origin/codex/other"}]
    rejected = run(invocation(tmp_path, repo, public_input(wrong), semantic_result(wrong)) + ["--confirmed-cleanup"], check=False)
    assert rejected.returncode == 3
    assert git(repo, "ls-remote", "--heads", "origin", "refs/heads/codex/demo").stdout.strip()

    resources = [
        {"kind": "remote_branch", "locator": "origin/codex/demo"},
        {"kind": "remote_tracking", "locator": "refs/remotes/origin/codex/demo"},
    ]
    command = invocation(tmp_path, repo, public_input(resources), semantic_result(resources))
    pending = json.loads(run(command).stdout)
    assert pending["exit_id"] == "remaining_resources"
    cleaned = json.loads(run(command + ["--confirmed-cleanup"]).stdout)
    assert cleaned == {"exit_id": "cleaned"}
    assert not git(repo, "ls-remote", "--heads", "origin", "refs/heads/codex/demo").stdout.strip()
    tracking = subprocess.run(
        ["git", "show-ref", "--verify", "--quiet", "refs/remotes/origin/codex/demo"],
        cwd=repo,
    )
    assert tracking.returncode != 0


def test_cleanup_rejects_unbound_or_current_worktree(tmp_path):
    repo = tmp_path / "repo"
    head = init_repo(repo)
    write_finish_receipt(repo, head)
    resources = [{"kind": "worktree", "locator": str(repo)}]
    command = invocation(tmp_path, repo, public_input(resources), semantic_result(resources))

    rejected = run(command + ["--confirmed-cleanup"], check=False)
    assert rejected.returncode == 3
    assert repo.exists()
