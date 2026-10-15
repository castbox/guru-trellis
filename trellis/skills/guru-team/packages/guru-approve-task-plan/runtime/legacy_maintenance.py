"""This gate owner's bounded legacy inspection and retirement; no current pass."""
from __future__ import annotations
import argparse
import base64
import json
import re
import stat
from pathlib import Path
from runtime.io import CommandError
from runtime.schema import validate_json

OWNER = 'guru-approve-task-plan'
ARTIFACT = 'planning-approval.json'
GATE_SCHEMA = 'planning-approval.schema.json'
IDENTITY_FIELD = 'task_ref'
CONTROL_ROOT = ".trellis/.runtime/guru-team/owner-checkpoints/"
CHECKPOINT_ROOT = ".trellis/.runtime/guru-team/" + OWNER + "/legacy-retirement/"


def fail(code, field, message):
    raise CommandError(code, field, message)


def path_at(root, ref):
    path = Path(ref)
    if ".." in path.parts:
        fail("invalid_path", "control_ref", "Use the exact original owner path.")
    return path if path.is_absolute() else Path(root) / path


def raw(path):
    if not path.exists():
        return None
    if not path.is_file() or path.is_symlink():
        fail("unsupported_control", str(path), "Use a regular owner control file.")
    return {"content_base64": base64.b64encode(path.read_bytes()).decode(),
            "mode": stat.S_IMODE(path.stat().st_mode)}


def inspect_controls(root, key, task_ref, refs):
    source = path_at(root, task_ref + "/task.json")
    selected = json.loads(source.read_text())
    generation = selected.get("lifecycle_generation", 0)
    if (selected.get("id") != key["task_id"] or type(generation) is not int
            or generation != key["lifecycle_generation"]):
        fail("control_identity_mismatch", "key", "Inspect the exact original Task incarnation; do not invent a generation.")
    # Both pinned a32 and v0.6.17-guru.2 gate owners use the slug, not Finalizer's hash.
    expected = CONTROL_ROOT + Path(task_ref).name + "/" + ARTIFACT
    rows = []
    for ref in refs:
        if ref != expected:
            fail("control_owner_mismatch", ref, "Select only this original gate owner's exact legacy slug path.")
        path = path_at(root, ref)
        snapshot = raw(path)
        if snapshot is None:
            fail("control_missing", ref, "Inspect the original gate before public maintenance writes.")
        value = json.loads(path.read_text())
        validate_json(value, Path(__file__).resolve().parents[1] / "schemas" / GATE_SCHEMA, "legacy_gate")
        if value.get("skill_id") != OWNER or value.get(IDENTITY_FIELD) != task_ref:
            fail("control_identity_mismatch", ref, "Read the selected Task's original gate, not another Task or generation.")
        if "lifecycle_generation" in value and value["lifecycle_generation"] != generation:
            fail("control_identity_mismatch", ref, "Preserve another generation's gate.")
        rows.append({"path": ref, "source": snapshot})
    return rows


def freeze_controls(root, key, task_ref, rows, source, operation_id):
    if not re.fullmatch(r"[A-Za-z0-9._-]+", operation_id):
        fail("invalid_operation", "operation_id", "Use the original operation identity.")
    checkpoint = path_at(root, CHECKPOINT_ROOT + operation_id + ".json")
    state = {"owner_id": OWNER, "operation_id": operation_id, "root": str(root),
             "key": key, "task_ref": task_ref, "controls": rows, "source": source, "retired": False}
    if checkpoint.exists():
        previous = json.loads(checkpoint.read_text())
        if any(previous[k] != state[k] for k in state if k != "retired"):
            fail("operation_mismatch", "recovery_ref", "Keep the same owner's original frozen preimages.")
    else:
        if raw(path_at(root, task_ref + "/task.json")) != source:
            fail("source_mismatch", "source", "Freeze the physically read original Task bytes and mode.")
        if inspect_controls(root, key, task_ref, [row["path"] for row in rows]) != rows:
            fail("control_changed", "controls", "Refresh the original owner inspection before maintenance.")
        checkpoint.parent.mkdir(parents=True, exist_ok=True)
        checkpoint.write_text(json.dumps(state, indent=2) + "\n")
    return str(checkpoint)


def read_checkpoint(recovery_ref):
    path = Path(recovery_ref)
    state = json.loads(path.read_text())
    expected = path_at(state["root"], CHECKPOINT_ROOT + state["operation_id"] + ".json")
    if state.get("owner_id") != OWNER or path.resolve() != expected.resolve():
        fail("checkpoint_owner_mismatch", "recovery_ref", "Use only this gate owner's own fixed checkpoint.")
    return path, state


def checkpoint_input(public):
    path, state = read_checkpoint(public["recovery_ref"])
    if any(state[k] != public[k] for k in ("root", "key", "task_ref")):
        fail("identity_mismatch", "recovery_ref", "Use the selected gate owner's Task checkpoint.")
    if public["control_refs"] != [row["path"] for row in state["controls"]]:
        fail("control_mismatch", "control_refs", "Use the fixed original gate inventory.")
    return path, state


def precheck_restore(recovery_ref):
    _, state = read_checkpoint(recovery_ref)
    for row in state["controls"]:
        if raw(path_at(state["root"], row["path"])) != (None if state["retired"] else row["source"]):
            fail("control_changed", row["path"], "Preserve later work before either rollback half.")


def restore_controls(recovery_ref):
    precheck_restore(recovery_ref)
    path, state = read_checkpoint(recovery_ref)
    for row in state["controls"]:
        target = path_at(state["root"], row["path"])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(base64.b64decode(row["source"]["content_base64"]))
        target.chmod(row["source"]["mode"])
    state["retired"] = False
    path.write_text(json.dumps(state, indent=2) + "\n")


def execute(package_root, public):
    root = Path(public["root"])
    if public['profile']=='legacy_control_freeze':
        return {'recovery_ref':freeze_controls(root,public['key'],public['task_ref'],public['controls'],public['source'],public['operation_id'])}
    if public['profile'] in {'legacy_control_restore_check','legacy_control_restore'}:
        _,state=read_checkpoint(public['recovery_ref'])
        if Path(state['root']).resolve()!=root.resolve():fail('target_mismatch','root','Restore only the original owner selected target.')
        if public['profile']=='legacy_control_restore_check':precheck_restore(public['recovery_ref'])
        else:restore_controls(public['recovery_ref'])
        return {'recovery_ref':public['recovery_ref']}
    if public["profile"] == "legacy_control_inspection":
        return {"formal_exit": False, "controls": inspect_controls(root, public["key"], public["task_ref"], public["control_refs"])}
    if public["profile"] != "legacy_control_retirement":
        fail("profile_mismatch", "profile", "Select this owner's separate legacy profile.")
    checkpoint, state = checkpoint_input(public)
    preserved = path_at(root, public["preserved_source_ref"])
    conversion = path_at(root, public["task_ref"] + "/migration/source-task.json")
    archive_root = root / ".trellis/tasks/archive"
    archive = preserved.name == "task.json" and archive_root.resolve() in preserved.resolve().parents
    if preserved.resolve() != conversion.resolve() and not archive:
        fail("preserved_source_mismatch", "preserved_source_ref", "Read the actual conversion source or readable legacy archive.")
    if raw(preserved) != state["source"]:
        fail("preserved_source_mismatch", "preserved_source_ref", "Verify physically preserved original Task bytes/mode before retiring its gate.")
    for row in state["controls"]:
        actual = raw(path_at(root, row["path"]))
        if actual != (None if state["retired"] else row["source"]):
            fail("control_changed", row["path"], "Preserve later gate work and reuse the original operation.")
    for row in state["controls"]:
        path_at(root, row["path"]).unlink(missing_ok=True)
    state["retired"] = True
    checkpoint.write_text(json.dumps(state, indent=2) + "\n")
    result = {"exit_id": "legacy_controls_retired", "owner_id": OWNER, "key": public["key"]}
    validate_json(result, package_root / "schemas/legacy_controls_retired-output-1.0.schema.json", "stdout")
    return result


def invoke_retirement(package_root, public, root):
    validate_json(public, package_root / "schemas/legacy_control_retirement-input-1.0.schema.json", "input")
    if Path(root).resolve() != Path(public["root"]).resolve():
        fail("target_mismatch", "root", "Use the selected target checkout.")
    return execute(package_root, public)


def run(package_root, command, argv):
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--input", required=True)
    args = parser.parse_args(argv)
    public = json.load(sys.stdin) if args.input == "-" else json.loads(Path(args.input).read_text())
    validate_json(public, package_root / "schemas/legacy-maintenance-input-1.0.schema.json", "input")
    if Path(args.root).resolve() != Path(public["root"]).resolve():
        fail("target_mismatch", "root", "Use the exact selected target checkout.")
    if public["profile"] == "legacy_control_retirement":
        fail("profile_mismatch", "profile", "Use the original scripts/invoke.sh for formal retirement.")
    return execute(package_root, public)
