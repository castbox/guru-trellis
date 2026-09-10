"""Exercise verifier-owned fixture setup against installed public Skill entries."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[5]
SCRIPTS = Path(__file__).resolve().parent


class InstalledCloseoutOwnerBoundaryTests(unittest.TestCase):
    def test_missing_installed_entry_is_reported_without_adapter_fallback(self):
        import verify_installed_closeout as closeout

        with tempfile.TemporaryDirectory(prefix="guru-closeout-missing-") as tmp:
            client = closeout.InstalledPackageClient(Path(tmp), "guru-approve-task-plan")
            with self.assertRaisesRegex(RuntimeError, "installed package wrapper is unavailable"):
                client._call("invoke.sh")

    def test_fixture_uses_installed_entries_without_eval_adapter(self):
        with tempfile.TemporaryDirectory(prefix="guru-closeout-owner-") as tmp:
            work = Path(tmp)
            repo = work / "project"
            (repo / ".trellis").mkdir(parents=True)
            shutil.copy2(SOURCE / "trellis/workflows/guru-team/workflow.md", repo / ".trellis/workflow.md")
            shutil.copytree(SOURCE / ".trellis/scripts", repo / ".trellis/scripts", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            (repo / ".gitignore").write_text(".trellis/.runtime/\n", encoding="utf-8")
            env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
            for key in tuple(env):
                if key.startswith("INSTALLED_CLOSEOUT_"):
                    env.pop(key)
            self.run_ok(["git", "init", "-q", "-b", "main", str(repo)], work, env)
            applied = self.run_ok([sys.executable, str(SCRIPTS / "apply_guru_team_trellis_preset.py"), "--repo", str(repo), "--all-platforms", "--json"], SOURCE, env)
            self.assertIn('"status": "ok"', applied.stdout)
            # This fixture uses one current checkout. No source task or session
            # is copied, and GitHub operations are handled by the verifier fake.
            (repo / ".trellis/guru-team/config.yml").write_text("workspace_mode: current\n", encoding="utf-8")
            driver = r'''
import json, os, shutil, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import verify_installed_closeout as v
root = Path(sys.argv[2]).resolve()
real_git = shutil.which("git")
remote = root.parent / "fixture.git"
v.ensure_baseline(root, real_git, remote, False)
fake = root.parent / "fake-bin"
v.install_fake_commands(fake)
os.environ.update({
    "PATH": str(fake) + os.pathsep + os.environ["PATH"],
    "INSTALLED_CLOSEOUT_REAL_GIT": real_git,
    "INSTALLED_CLOSEOUT_REMOTE": str(remote),
    "INSTALLED_CLOSEOUT_BRANCH": "fix/105-installed-closeout-initial",
    "INSTALLED_CLOSEOUT_PR_NUMBER": "105",
    "INSTALLED_CLOSEOUT_PR_STORE": str(root.parent / "pr.json"),
    "INSTALLED_CLOSEOUT_MUTATION_STORE": str(root.parent / "mutations.json"),
})
owners = {name: v.InstalledPackageClient(root, name) for name in (
    "guru-approve-task-plan", "guru-check-task", "guru-create-task-commit",
    "guru-review-branch", "guru-review-task-publication",
)}
calls = []
real_run = v.run
def observed_run(command, cwd, **kwargs):
    calls.append([str(part) for part in command])
    return real_run(command, cwd, **kwargs)
v.run = observed_run
task, branch, commit = v.write_fixture(root, owners, real_git, "initial", 105)
for skill in owners:
    expected = str(root / ".trellis/guru-team/skills/packages" / skill / "scripts/invoke.sh")
    assert any(command[0] == expected for command in calls), (skill, calls)
for script in ("record-planning-approval.sh", "check-planning-approval.sh"):
    assert any(command[0].endswith("/" + script) for command in calls), (script, calls)
loaded = [str(getattr(m, "__file__", "")) for m in sys.modules.values() if m]
assert not any(p.endswith(("native_adapter.py", "production_fixtures.py", "owner_runtime.py")) for p in loaded), loaded
assert task.is_dir() and len(commit) == 40
print(json.dumps({"task": task.name, "branch": branch, "reviewed_commit": commit, "fixture_prepared": True}))
'''
            prepared = self.run_ok([sys.executable, "-c", driver, str(SCRIPTS), str(repo)], work, env)
            value = json.loads(prepared.stdout.strip().splitlines()[-1])
            self.assertTrue(value["fixture_prepared"])
            self.assertEqual(value["branch"], "fix/105-installed-closeout-initial")

    def run_ok(self, argv, cwd, env):
        result = subprocess.run(argv, cwd=cwd, env=env, text=True, capture_output=True, timeout=180)
        self.assertEqual(result.returncode, 0, result.stdout[-6000:] + result.stderr[-6000:])
        return result


if __name__ == "__main__":
    unittest.main()
