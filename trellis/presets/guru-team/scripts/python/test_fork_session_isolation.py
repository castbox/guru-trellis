"""Run the same isolation cases against supplied canonical and installed roots."""
from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[5]
PROBE = r'''
import importlib.util, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
scripts, hooks = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(scripts))
from common.active_task import resolve_active_task
for key in list(os.environ):
    if "SESSION" in key or key in ("CODEX_THREAD_ID", "TRELLIS_CONTEXT_ID"):
        os.environ.pop(key, None)
with tempfile.TemporaryDirectory(prefix="fork-isolation-") as tmp:
    roots = [Path(tmp) / name for name in ("first", "second")]
    roots[0].mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main", str(roots[0])], check=True)
    subprocess.run(["git", "-C", str(roots[0]), "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "-c", "core.hooksPath=/dev/null", "commit", "--allow-empty", "-qm", "fixture"], check=True)
    subprocess.run(["git", "-C", str(roots[0]), "worktree", "add", "-q", "-b", "second", str(roots[1])], check=True)
    for root in roots:
        (root / ".trellis/.runtime/sessions").mkdir(parents=True)
        task = root / ".trellis/tasks/own"
        task.mkdir(parents=True)
        (task / "task.json").write_text(json.dumps({"id": root.name, "status": "planning"}))
    for root in roots:
        sessions = root / ".trellis/.runtime/sessions"
        for count in (0, 1, 2):
            if count:
                (sessions / f"codex_foreign{count}.json").write_text(json.dumps({"current_task": ".trellis/tasks/own"}))
            before = {p.name: p.read_bytes() for p in sessions.iterdir()}
            for payload in ({}, {"session_id": "unmatched"}):
                assert resolve_active_task(root, payload, "codex", allow_environment_context=False).task_path is None
            if count == 1:
                exact = resolve_active_task(root, {"session_id": "foreign1"}, "codex", allow_environment_context=False)
                assert exact.source_type == "session" and not exact.stale
                child = resolve_active_task(root, {}, "codex", allow_single_session_fallback=True, allow_environment_context=False)
                assert child.source_type == "session-fallback"
            assert {p.name: p.read_bytes() for p in sessions.iterdir()} == before
        (sessions / "codex_stale.json").write_text(json.dumps({"current_task": ".trellis/tasks/missing"}))
        assert resolve_active_task(root, {"session_id": "stale"}, "codex", allow_environment_context=False).stale
    # The first checkout cannot use the second checkout's exact session key.
    second = roots[1] / ".trellis/.runtime/sessions/codex_second_only.json"
    second.write_text(json.dumps({"current_task": ".trellis/tasks/own"}))
    assert resolve_active_task(roots[0], {"session_id": "second_only"}, "codex", allow_environment_context=False).task_path is None
    main = Path(tmp) / "hook-root"
    sessions = main / ".trellis/.runtime/sessions"
    sessions.mkdir(parents=True)
    (main / ".trellis/tasks/foreign").mkdir(parents=True)
    foreign = sessions / "codex_foreign.json"
    foreign.write_text(json.dumps({"current_task": ".trellis/tasks/foreign"}))
    before = foreign.read_bytes()
    for name in ("session-start.py", "inject-workflow-state.py"):
        hook = hooks / name
        assert hook.is_file(), hook
        copied = Path(tmp) / ".codex/hooks" / name
        copied.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(hook, copied)
        spec = importlib.util.spec_from_file_location(name, copied)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        for payload in ({}, {"session_id": "unmatched"}):
            arg = main / ".trellis" if name == "session-start.py" else main
            assert module._resolve_active_task(arg, payload).task_path is None
        assert foreign.read_bytes() == before
print("isolation cases passed")
'''


class ForkSessionIsolationTests(unittest.TestCase):
    def check_root(self, scripts, hooks):
        result = subprocess.run([sys.executable, "-c", PROBE, str(scripts), str(hooks)],
                                capture_output=True, text=True,
                                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_installed_runtime_and_main_hooks(self):
        root = Path(os.environ.get("TRELLIS_INSTALLED_REPO", str(SOURCE)))
        self.check_root(root / ".trellis/scripts", root / ".codex/hooks")

    @unittest.skipUnless(os.environ.get("TRELLIS_FORK_SOURCE"), "Explicit verified Fork checkout required")
    def test_canonical_fork_runtime_and_main_hooks(self):
        import tempfile
        import shutil

        root = Path(os.environ["TRELLIS_FORK_SOURCE"]) / "packages/cli/src/templates"
        with tempfile.TemporaryDirectory(prefix="canonical-hooks-") as tmp:
            hooks = Path(tmp)
            shutil.copy2(root / "codex/hooks/session-start.py", hooks / "session-start.py")
            shutil.copy2(root / "shared-hooks/inject-workflow-state.py", hooks / "inject-workflow-state.py")
            self.check_root(root / "trellis/scripts", hooks)


if __name__ == "__main__":
    unittest.main()
