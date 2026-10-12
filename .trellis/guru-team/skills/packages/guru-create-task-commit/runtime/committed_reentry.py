from __future__ import annotations

import json
import subprocess
from pathlib import Path

from common import git, json_file, load, root, status_records, task_dir
from runtime.io import CommandError, project_intermediate_receipt
from runtime.schema import validate_json
from runtime.task_lifecycle import LifecycleContractError, resolve_active_task_checkout


def run(package_root: Path, root_value: str | None, envelope_value: str) -> dict:
    """Verify the existing candidate; Phase 2 keeps its content-check algorithm."""
    if envelope_value != "-":
        raise CommandError("invalid_arguments", "committed_reentry", "Use --committed-reentry - with one stdin envelope.")
    repo = root(package_root, root_value)
    envelope = load(repo, package_root, envelope_value, "committed_reentry")
    validate_json(envelope, package_root / "schemas/committed-reentry-envelope.schema.json", "committed_reentry")
    public, owner = envelope["public_input"], envelope["owner_result"]
    td = task_dir(repo, public["task_ref"])
    try:
        resolve_active_task_checkout(repo, public["task_ref"])
    except LifecycleContractError as exc:
        raise CommandError("stale_identity", exc.field_path, exc.remediation, 3) from exc
    task = json_file(td / "task.json", "task")
    if task.get("status") != "in_progress":
        raise CommandError("stale_identity", "task", "Use the current in-progress task checkout.", 3)
    head = git(repo, "rev-parse", "HEAD").stdout.strip()
    for marker in ("MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD", "rebase-merge", "rebase-apply", "sequencer"):
        location = Path(git(repo, "rev-parse", "--path-format=absolute", "--git-path", marker).stdout.strip())
        if location.exists():
            raise CommandError("stale_identity", "git_operation_state", "Finish the current operation through its existing recovery owner.", 3)
    if status_records(repo):
        raise CommandError("stale_identity", "worktree", "Use the dirty prepare/exact-commit path, then fresh Phase 2.", 3)
    base = task.get("base_branch")
    if not isinstance(base, str) or not base:
        raise CommandError("stale_identity", "base_branch", "Resolve the task selected base before Task Commit.", 3)
    base_ref = f"origin/{base}" if git(repo, "rev-parse", "--verify", f"origin/{base}", check=False).returncode == 0 else base
    base_head = git(repo, "rev-parse", "--verify", f"{base_ref}^{{commit}}").stdout.strip()
    if (base_head == head or git(repo, "merge-base", "--is-ancestor", base_head, head, check=False).returncode
            or not git(repo, "diff", "--name-only", f"{base_ref}...HEAD").stdout.strip()):
        raise CommandError("stale_identity", "base_ref", "Run the current base pair guard/Reconcile owner before Task Commit.", 3)
    committed_task = git(repo, "show", f"HEAD:{public['task_ref']}/task.json", check=False)
    try:
        committed = json.loads(committed_task.stdout)
    except (ValueError, TypeError) as exc:
        raise CommandError("stale_identity", "task", "Commit the current task metadata through the dirty Task Commit path.", 3) from exc
    if committed_task.returncode or committed != task:
        raise CommandError("stale_identity", "task", "Use the committed current task metadata.", 3)

    checker = package_root.parent / "guru-check-task/scripts/check-phase2-check.sh"
    checked = subprocess.run(["bash", str(checker), "--root", str(repo), "--task", public["task_ref"], "--json"], cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if checked.returncode:
        raise CommandError("stale_identity", "phase2_result", "Rerun the existing Phase 2 owner against current content/history.", 3)
    try:
        receipt = json.loads(checked.stdout)
    except ValueError as exc:
        raise CommandError("invalid_json", "phase2_result", "Restore the complete Phase 2 checker runtime.") from exc
    skills_root = package_root.parents[1]
    schemas = skills_root / "schemas" if (skills_root / "schemas").is_dir() else skills_root.parent / "schemas"
    result = project_intermediate_receipt(receipt, schemas)
    checkpoint = repo / ".trellis/.runtime/guru-team/owner-checkpoints" / td.name / "phase2-check.json"
    phase2 = json_file(checkpoint, "phase2")
    if (result.get("status") != "ok" or result.get("typed_exit") != "passed"
            or result.get("head") != head or result.get("phase2_capture_commit") != head
            or public["phase2_commit_anchor"] != head
            or phase2.get("phase2_capture_commit") != head
            or phase2.get("task_ref") != public["task_ref"] or phase2.get("mode") != public["mode"]):
        raise CommandError("stale_identity", "phase2_commit_anchor", "Run fresh Phase 2 at the exact current committed HEAD.", 3)
    if owner["status"] != "passed":
        return {"typed_exit": owner["status"], "task_ref": public["task_ref"]}
    output = {"exit_id": "committed", "task_ref": public["task_ref"], "base_ref": base_ref, "branch_review_commit": head}
    validate_json(output, package_root / "schemas/public-committed-output.schema.json", "stdout")
    checkpoint.unlink()
    return output
