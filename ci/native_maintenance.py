"""Exercise the target's fixed upstream CLI in separate native processes."""
from __future__ import annotations

import json
import base64
import hashlib
import os
from pathlib import Path
import shlex
import shutil


def document(output):
    """Maintenance emits one compact JSON line; CLI notices are separate lines."""
    for line in reversed(output.splitlines()):
        if line.startswith("{"):
            return json.loads(line)
    raise RuntimeError("Maintenance returned no JSON result")


def maintain(steps, target, clean, workspace, python, bash, cli, provider):
    command = "py -3" if os.name == "nt" else "python3"
    env = {"TRELLIS_PYTHON_CMD": command, "PYTHONUTF8": "0"}
    steps.target["maintenance_interpreter"] = command
    preserved = {name: (clean / name).read_bytes() for name in ("AGENTS.md", ".trellis/config.yaml")}
    if os.name == "nt":
        launcher = shutil.which("py")
        if not launcher:
            raise RuntimeError("Windows py launcher unavailable; py -3 integration not executed")
        if not steps.call("maintenance-python-probe", [launcher, "-3", "-c",
                "import json,sys; print(json.dumps({'executable':sys.executable,'version':sys.version}))"],
                clean, env_patch=env)[0]:
            return

    def call(stage, args):
        return steps.call(stage, ["node", cli, *args], clean, "installation", env_patch=env)

    # Preserve mode never silently replaces a user's workflow/configuration.
    for stage, args in [
        ("maintenance-update-preview", ["update", "--dry-run"]),
        ("maintenance-update", ["update", "--skip-all"]),
        ("maintenance-workflow-preview", ["workflow", "--marketplace", provider,
                                           "--template", "guru-team", "--create-new"]),
    ]:
        if not call(stage, args)[0]:
            return
    preview = clean / ".trellis/workflow.md.new"
    if not preview.is_file() or preview.read_bytes() != (target / "trellis/workflows/guru-team/workflow.md").read_bytes():
        raise RuntimeError("Workflow preview differs from the selected target marketplace source")
    if not call("maintenance-workflow-apply", ["workflow", "--marketplace", provider,
                                              "--template", "guru-team", "--force"])[0]:
        return
    if (clean / ".trellis/workflow.md").read_bytes() != preview.read_bytes():
        raise RuntimeError("Applied workflow differs from reviewed preview")
    # The exact reviewed preview has been consumed by the force operation.
    preview.unlink()
    request = workspace / "tools-input.json"
    decisions = [{"path": name, "action": "preserve", "source": {
        "content_base64": base64.b64encode(content).decode("ascii"),
        "sha256": hashlib.sha256(content).hexdigest(),
        "mode": (clean / name).stat().st_mode & 0o777}}
        for name, content in preserved.items()]
    request.write_text(json.dumps({"kind": "tools_install", "input": {
        "root": str(clean), "workflow": {"action": "preserve"}, "file_decisions": decisions}}), encoding="utf-8")
    ok, output = call("maintenance-tools-prepare", ["maintain", "prepare", "--input", request])
    if not ok:
        return
    plan = workspace / "tools-plan.json"
    plan.write_text(json.dumps(document(output)), encoding="utf-8")
    if not call("maintenance-tools-preview", ["maintain", "preview", "--plan", plan])[0]:
        return
    ok, output = call("maintenance-tools-apply", ["maintain", "apply", "--plan", plan,
                                                  "--state-dir", workspace / "maintenance-state"])
    if not ok:
        return
    applied = document(output)
    recovery = applied.get("recovery_ref")
    if applied.get("status") != "applied" or not recovery:
        raise RuntimeError("Tools operation did not finish with its original recovery reference")
    for operation in ("recover", "resume"):
        ok, output = call("maintenance-tools-" + operation,
                          ["maintain", operation, "--recovery", recovery])
        if not ok:
            return
        recovered = document(output)
        if recovered.get("status") != "applied" or recovered.get("operation_id") != applied["operation_id"]:
            raise RuntimeError("Maintenance recovery did not retain the original completed operation")
    apply = target / "trellis/presets/guru-team/scripts/bash/apply.sh"
    if not steps.call("maintenance-guru-reapply", [bash, apply.as_posix(), "--repo", clean.as_posix(),
            "--platform", "codex", "--python", python.as_posix()], target, "installation")[0]:
        return
    validator = clean / ".trellis/guru-team/scripts/bash/check-skill-packages.sh"
    steps.call("maintenance-installed-validation", [bash, validator.as_posix(), "--root", clean.as_posix(),
                "--mode", "installed", "--json"], clean, "installation")
    steps.call("maintenance-installed-wrapper", [python, Path(__file__).parent / "runtime_diagnostic.py",
                "--target-root", target, "--installed-root", clean, "--python", python,
                "--output", steps.directory / "maintenance-installed-wrapper.json"], clean, "installation")
    hooks = json.loads((clean / ".codex/hooks.json").read_text(encoding="utf-8"))
    fixture = json.dumps({"cwd": str(clean), "prompt": "Inspect the current Trellis route.",
                          "session_id": "guru-native-maintenance-fixture"}).encode("utf-8")
    for index, group in enumerate(hooks["hooks"]["UserPromptSubmit"]):
        for hook_index, hook in enumerate(group["hooks"]):
            ok, output = steps.call(f"maintenance-native-hook-{index}-{hook_index}", shlex.split(hook["command"]),
                                    clean, "installation", env_patch=env, input_data=fixture)
            if not ok:
                return
            context = document(output).get("hookSpecificOutput", {})
            if (context.get("hookEventName") != "UserPromptSubmit"
                    or "<workflow-state>" not in context.get("additionalContext", "")
                    or "Status: no_task" not in context.get("additionalContext", "")):
                raise RuntimeError("Native hook did not return the fixture's no-task workflow context")
    sidecars = [str(path.relative_to(clean)) for path in clean.rglob("*")
                if path.is_file() and path.suffix in (".new", ".bak") and ".git" not in path.parts]
    if sidecars:
        raise RuntimeError("Maintenance retained unresolved sidecars: " + ", ".join(sidecars))
    if any((clean / name).read_bytes() != content for name, content in preserved.items()):
        raise RuntimeError("Maintenance changed user-owned AGENTS/configuration bytes")
