"""Public maintenance and Finish writers for the resumed-archive regression."""
import importlib.util
import json
import os
import subprocess
import unittest
from pathlib import Path

from runtime.delivery_projection import DeliveryProjection, authority_ref
from runtime.maintenance_transport import call


def resume_manual_archive(root: Path, source_kind: str, task_id: str = "resumed") -> dict:
    candidate_ref = os.environ.get("TRELLIS_MAINTENANCE_CANDIDATE")
    if not candidate_ref:
        raise unittest.SkipTest("Set TRELLIS_MAINTENANCE_CANDIDATE to the matching public pair")
    candidate = json.loads(Path(candidate_ref).read_text())
    cli = Path(candidate["cli_package_root"])
    source = {"cli_package_root": str(cli), "dependency_mode": "local_candidate",
              "expected_candidate": candidate["candidate"]}
    script = """
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
const require = createRequire(process.argv[1]+'/package.json');
const task = await import(pathToFileURL(require.resolve('@mindfoldhq/trellis-core/task')));
const v2 = await import(pathToFileURL(require.resolve('@mindfoldhq/trellis-core/task/v2')));
const header = {id:process.argv[2], name:'Resumed', title:'Resumed task'};
console.log(JSON.stringify({old:task.emptyTaskRecord(header), current:v2.emptyTaskRecordV2(header)}));
"""
    records = json.loads(subprocess.check_output(
        ["node", "--input-type=module", "-e", script, str(cli), task_id], text=True))
    old = records["old"]
    old.update(status="completed", completedAt="2025-01-01", base_branch="main")
    if source_kind == "legacy":
        old.pop("source")
        old.pop("lifecycle_generation")
        old.update(creator="fixture", assignee="fixture")
    else:
        old["lifecycle_generation"] = 2
    key = {"task_id": task_id, "lifecycle_generation": old.get("lifecycle_generation", 0)}
    archive_ref = ".trellis/tasks/archive/2025-01/" + task_id
    original_ref = ".trellis/tasks/original-" + task_id
    active_ref = ".trellis/tasks/current-" + task_id
    archive = root / archive_ref
    archive.mkdir(parents=True)
    (archive / "task.json").write_text(json.dumps(old) + "\n")
    (archive / "prd.md").write_text("Preserved accepted scope; formal acceptance remains open.\n")
    (archive / "manual-closeout.md").write_text("Manual historical archive without a Finish result.\n")
    raw_source = (archive / "task.json").read_bytes()
    authority = authority_ref(archive / "manual-closeout.md", root)
    selection = {"root": str(root), "key": key, "task_ref": archive_ref,
                 "original_task_ref": original_ref}
    inspected = call(source, "inspectTaskTarget", selection)
    projection = records["current"]
    projection["lifecycle_generation"] = key["lifecycle_generation"]
    projection["base_branch"] = "main"
    projection["accepted_scope"] = authority_ref(archive / "prd.md", root)
    prepared = call(source, "prepareArchivedTaskResume", {
        **selection, "active_ref": active_ref, "source_kind": source_kind, "projection": projection,
        "artifacts": [{"path": row["path"], "action": "preserve", "source": row["source"]}
                      for row in inspected["artifacts"]
                      if row["kind"] == "file" and row["path"] != archive_ref + "/task.json"],
        "legacy_facts": [{"field": "completedAt", "disposition": "source_snapshot",
                          "owner_id": "guru-maintain-legacy-task", "reason": authority}],
        "sessions": [], "branch_binding": {"action": "establish", "source": None,
            "record": {"schema_version": "1.0", **key, "binding_revision": 1, "branch_name": "main"}},
        "resume_intent": {"reason": authority, "archive_review": authority,
                          "next_owner_id": "guru-review-task-completion", "next_action": "Review current acceptance"},
    })
    call(source, "applyMaintenance", {"plan": prepared,
        "state_dir": str(root / ".trellis/.runtime/public-resume")})
    return {"key": key, "archive_ref": archive_ref, "active_ref": active_ref, "source_bytes": raw_source}


def finish_resumed_archive(root: Path, resumed: dict) -> str:
    key = resumed["key"]
    projection = DeliveryProjection(root, resumed["active_ref"])
    authority = projection.read_record()["accepted_scope"]
    completion = {"result_id": "completion:" + key["task_id"], "owner_id": "guru-review-task-completion",
                  "evidence": [authority], "lifecycle_generation": key["lifecycle_generation"],
                  "accepted_scope": authority, "delivery_result_ids": [], "outcome": "completed"}
    projection.apply({"api_version": "1.0", "operation": "complete_task", "key": key,
                      "owner_role": "completion", "owner_id": completion["owner_id"], "result": completion})
    closure = {"result_id": "closure:" + key["task_id"], "owner_id": "guru-complete-task-closure",
               "evidence": [authority], "lifecycle_generation": key["lifecycle_generation"],
               "completion_result_id": completion["result_id"], "disposition": "no_mutation", "source_result": None}
    projection.apply({"api_version": "1.0", "operation": "close_task", "key": key,
                      "owner_role": "closure", "owner_id": closure["owner_id"], "result": closure})
    package = Path(__file__).resolve().parents[3] / "packages/guru-finish-task"
    spec = importlib.util.spec_from_file_location("archive_resume_finish_fixture", package / "runtime/invoke.py")
    owner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(owner)
    archive_ref = ".trellis/tasks/archive/2026-10/" + Path(resumed["active_ref"]).name
    owner.project_archive(root, {**key, "task_ref": resumed["active_ref"], "closure_result": closure},
                          Path(resumed["active_ref"]), archive_ref, Path(archive_ref))
    return archive_ref
