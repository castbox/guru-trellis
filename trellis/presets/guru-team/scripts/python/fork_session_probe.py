"""Exercise supplied official runtime bytes in disposable linked worktrees."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def check_linked_session(scripts: Path, hooks: Path) -> None:
    env = {key: value for key, value in os.environ.items()
           if "SESSION" not in key and key not in (
               "CODEX_THREAD_ID", "TRELLIS_CONTEXT_ID", "CODEX_NON_INTERACTIVE",
               "TRELLIS_HOOKS", "TRELLIS_DISABLE_HOOKS")}
    env.update(PYTHONDONTWRITEBYTECODE="1", TRELLIS_CONTEXT_ID="codex_linked_probe")
    with tempfile.TemporaryDirectory(prefix="fork-linked-session-") as directory:
        main, linked = Path(directory).resolve() / "primary", Path(directory).resolve() / "linked"
        main.mkdir()

        def run(root, *command, payload=None, session=None):
            selected = dict(env)
            if session:
                selected["TRELLIS_CONTEXT_ID"] = session
            result = subprocess.run(command, cwd=root, env=selected, text=True,
                                    input=json.dumps(payload) if payload else None,
                                    capture_output=True, timeout=60)
            if result.returncode:
                raise AssertionError(f"{command}: {result.stdout}\n{result.stderr}")
            return result.stdout

        run(main, "git", "init", "-q", "-b", "main")
        run(main, "git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
            "-c", "core.hooksPath=/dev/null", "commit", "--allow-empty", "-qm", "fixture")
        run(main, "git", "worktree", "add", "-q", "-b", "linked", str(linked))
        for root in (main, linked):
            shutil.copytree(scripts, root / ".trellis/scripts", ignore=shutil.ignore_patterns("__pycache__"))
            (root / ".trellis/spec").mkdir()
            (root / ".trellis/workflow.md").write_text("# Fixture workflow\n")
            (root / ".codex/hooks").mkdir(parents=True)
            for name in ("session-start.py", "inject-workflow-state.py"):
                shutil.copy2(hooks / name, root / ".codex/hooks" / name)

        # The supported creator auto-starts this explicit session in the linked checkout.
        run(linked, sys.executable, ".trellis/scripts/task.py", "create", "Linked session probe",
            "--slug", "linked-session-probe", "--description", "Cross-worktree fixture",
            "--creator", "fixture", "--assignee", "fixture")
        linked_current = json.loads(run(linked, sys.executable, ".trellis/scripts/task.py", "current", "--json"))
        expected = linked_current["current_task"]
        assert expected is not None, linked_current
        assert not (main / expected["dir"]).exists()
        for root in (linked, main):
            current = json.loads(run(root, sys.executable, ".trellis/scripts/task.py", "current", "--json"))
            assert current["current_task"] == expected, current
            assert current["task_workspace_root"] == str(linked.resolve()), current
            assert current["resolved_task_path"] == str(linked / expected["dir"]), current
            context = run(root, sys.executable, ".trellis/scripts/get_context.py")
            context_lines = context.splitlines()
            assert f"Path: {expected['dir']}" in context_lines, context
            assert f"Task workspace: {linked}" in context_lines, context
            assert f"Resolved task: {linked / expected['dir']}" in context_lines, context
            for name in ("session-start.py", "inject-workflow-state.py"):
                output = run(root, sys.executable, str(root / ".codex/hooks" / name),
                             payload={"cwd": str(root), "session_id": "linked_probe", "platform": "codex"})
                assert "no_task" not in output, output
                if name == "inject-workflow-state.py":
                    assert f"Task: {expected['id']} ({expected['status']})" in output, output
                    assert f"Task workspace: {linked}; caller workspace: {root}." in output, output
                else:
                    assert expected["dir"].split("/")[-1] in output, output

        # A second honest session starts its own task; it must not replace the first binding.
        run(main, sys.executable, ".trellis/scripts/task.py", "create", "Foreign session probe",
            "--slug", "foreign-session-probe", "--description", "Isolation fixture",
            "--creator", "fixture", "--assignee", "fixture", session="codex_foreign_probe")
        for root in (main, linked):
            current = json.loads(run(root, sys.executable, ".trellis/scripts/task.py", "current", "--json"))
            assert current["current_task"] == expected, current
            result = subprocess.run([sys.executable, ".trellis/scripts/task.py", "current", "--json"],
                                    cwd=root, env=dict(env, TRELLIS_CONTEXT_ID="codex_unmatched_probe"),
                                    text=True, capture_output=True, timeout=60)
            assert json.loads(result.stdout)["current_task"] is None, result.stdout


if __name__ == "__main__":
    check_linked_session(Path(sys.argv[1]), Path(sys.argv[2]))
    print("linked session current/context/SessionStart/workflow-state passed")
