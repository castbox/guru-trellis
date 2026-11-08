"""One real linked-invocation migration, complete preset, reapply and rollback."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

import test_delivery_upgrade as fixture_module
from test_delivery_upgrade import PACKAGE, SOURCE
from files import state, write_json
import delivery_upgrade as upgrade


class DeliveryUpgradePresetTests(unittest.TestCase):
    def test_linked_preserved_history_through_public_upgrade_and_reapply(self):
        fixture = fixture_module.DeliveryUpgradeTests(methodName="runTest")
        self.addCleanup(fixture.doCleanups)
        fixture.setUp()
        fixture.patch_source.stop()
        fixture.patch_installer.stop()
        fixture.source = SOURCE
        fixture.public["target_source_ref"] = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=SOURCE, text=True).strip()
        nested = fixture.root / fixture.ref / "worktree-snapshots/prior/task.json"
        nested.parent.mkdir(parents=True)
        shutil.copyfile(fixture.root / fixture.ref / "task.json", nested)
        nested.chmod(0o640)
        fixture.git("add", "."); fixture.git("commit", "-qm", "normal Task snapshot before worktree")
        sibling = fixture.directory / "linked-invocation"
        fixture.git("worktree", "add", "-qb", "linked-invocation", str(sibling))
        nested_before = {str(target): state(target / fixture.ref / "worktree-snapshots/prior/task.json")
                         for target in (fixture.root, sibling)}
        plan = fixture.plan({"primary": fixture.root, "peer": sibling}, ("peer",))
        for row in plan["guru_workspaces"]:
            row["selected_platforms"] = ["codex", "cursor"]
            row["decisions"] = [{"path": ".cursor/commands/guru-finish-work.md", "action": "replace", "expected_sha256": None}]
        public_file = fixture.directory / "public.json"
        plan_file = fixture.directory / "plan.json"
        write_json(public_file, fixture.public); write_json(plan_file, plan)
        before = {str(p): state(p) for target in (fixture.root, sibling)
                  for p in target.rglob("*") if p.is_file() and ".git" not in p.parts and p.name != ".git"}

        def invoke(public):
            write_json(public_file, public)
            result = subprocess.run(["bash", str(PACKAGE / "scripts/invoke.sh"),
                                     "--root", str(sibling), "--input", str(public_file),
                                     "--plan", str(plan_file), "--fork", str(fixture.fork)],
                                    cwd=SOURCE, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout[-1000:] + result.stderr[-1000:])
            return json.loads(result.stdout)

        result = invoke(fixture.public)
        gitdir = Path(subprocess.check_output(["git", "rev-parse", "--absolute-git-dir"], cwd=sibling, text=True).strip())
        recovery = gitdir / "guru-team/install-upgrade" / result.get("recovery_ref", "missing")
        checkpoint = json.loads((recovery / "checkpoint.json").read_text()) if recovery.exists() else {}
        self.assertEqual(result["exit_id"], "upgraded", checkpoint.get("failure", result))
        self.assertEqual(checkpoint["phase"], "complete")
        for target in (fixture.root, sibling):
            self.assertTrue((target / ".cursor/commands/guru-finish-work.md").is_file())
            reapplied = subprocess.run(["bash", str(SOURCE / "trellis/presets/guru-team/scripts/bash/apply.sh"),
                                       "--repo", str(target), "--platform", "codex", "--platform", "cursor",
                                       "--python", sys.executable], cwd=SOURCE, text=True, capture_output=True)
            self.assertEqual(reapplied.returncode, 0, reapplied.stdout[-1500:] + reapplied.stderr[-1500:])
            self.assertEqual(json.loads(reapplied.stdout)["status"], "ok")
            self.assertEqual(state(target / fixture.ref / "worktree-snapshots/prior/task.json"), nested_before[str(target)])
            self.assertFalse([p for p in target.rglob("*") if p.is_file() and p.suffix in {".new", ".bak"}])
        self.assertEqual(invoke({"profile": "delivery_resume", "recovery_ref": result["recovery_ref"]})["exit_id"], "upgraded")
        self.assertEqual(upgrade.business(checkpoint), checkpoint["business_before"])
        self.assertEqual(invoke({"profile": "delivery_rollback", "recovery_ref": result["recovery_ref"]})["exit_id"], "rolled_back")
        self.assertEqual({str(p): state(p) for target in (fixture.root, sibling)
                          for p in target.rglob("*") if p.is_file() and ".git" not in p.parts and p.name != ".git"}, before)


if __name__ == "__main__":
    unittest.main()
