"""Actual installed Plan2 integration; preset/native acceptance is separate."""
from __future__ import annotations

import base64
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

PACKAGE = Path(__file__).resolve().parents[1]
SOURCE = PACKAGE.parents[4]
sys.path.insert(0, str(PACKAGE.parents[1]))
sys.path.insert(0, str(PACKAGE / "runtime"))
import delivery_upgrade as upgrade
from delivery_upstream import call, packages
from files import MigrationError, state, write_json
from owner import run
from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
from runtime.task_lifecycle.git_facts import RepositoryFacts


BUILD_RECORD = """
import fs from 'node:fs';import {pathToFileURL} from 'node:url';
const x=JSON.parse(fs.readFileSync(0,'utf8'));
const {emptyTaskRecordV2,applyTaskOperation}=await import(pathToFileURL(x.core+'/dist/task/v2/index.js'));
const metadata=Object.fromEntries(Object.entries(x.old).filter(([k])=>!['status','commit','pr_url','completedAt'].includes(k)));
let record=emptyTaskRecordV2(metadata);
if(x.key){
 record=applyTaskOperation(record,{api_version:'1.0',operation:'accept_scope',key:{task_id:record.id,lifecycle_generation:record.lifecycle_generation},owner_role:'task_scope',owner_id:x.contract.owners.task_scope,authority:x.authority},x.contract).record;
 record=applyTaskOperation(record,{api_version:'1.0',operation:'create_delivery',key:x.key,owner_role:'creation',owner_id:x.contract.owners.creation,scope_ref:{authority:x.authority,anchors:['R1']},profile:'pull_request'},x.contract).record;
}
process.stdout.write(JSON.stringify(record));
"""


class DeliveryUpgradeTests(unittest.TestCase):
    def setUp(self):
        configured = os.environ.get("GURU_UPSTREAM_DELIVERY_CLI")
        predecessor = os.environ.get("GURU_UPSTREAM_LEGACY_CLI")
        if not configured or not predecessor:
            self.skipTest("Set explicit reviewed installed Delivery and predecessor CLI entries")
        self.fork = Path(configured)
        self.cli, self.core = packages(self.fork)
        self.temp = tempfile.TemporaryDirectory(prefix="guru531-plan2-")
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name).resolve()
        self.root = self.directory / "business"
        self.root.mkdir()
        for args in (("init", "-q"), ("config", "user.name", "Upgrade fixture"), ("config", "user.email", "fixture@example.invalid")):
            self.git(*args)
        if getattr(self, "project_relative", None):
            self.root /= self.project_relative
            self.root.mkdir()
        self.execute(["node", predecessor, "init", "--codex", "--yes"])
        self.execute([sys.executable, ".trellis/scripts/task.py", "start", ".trellis/tasks/00-bootstrap-guidelines"])
        self.ref = ".trellis/tasks/00-bootstrap-guidelines"
        self.assertEqual(json.loads((self.root / self.ref / "task.json").read_text())["status"], "in_progress")
        self.source = self.directory / "source"
        (self.source / "trellis/workflows/guru-team").mkdir(parents=True)
        (self.source / "trellis/workflows/guru-team/workflow.md").write_bytes((SOURCE / "trellis/workflows/guru-team/workflow.md").read_bytes())
        (self.source / "trellis/guru-team-extension.json").write_text('{"version":"0.7.0-guru.4"}')
        for args in (("init", "-q"), ("config", "user.name", "Upgrade fixture"), ("config", "user.email", "fixture@example.invalid"), ("add", "."), ("commit", "-qm", "source fixture")):
            subprocess.run(["git", *args], cwd=self.source, check=True, capture_output=True)
        old = {"schema_version": "2.0", "extension": {"version": "0.6.17-guru.88", "target_trellis_cli": "0.7.0-castbox.3"},
               "source": {"repo": "https://github.com/castbox/guru-trellis.git", "commit": "a" * 40},
               "install": {"selected_platforms": ["codex"], "managed_assets": [], "managed_asset_hashes": {}}}
        write_json(self.root / ".trellis/guru-team/extension.json", old)
        for name in ("prd.md", "design.md", "implement.md", "implement.jsonl", "check.jsonl"):
            (self.root / self.ref / name).write_text("Old committed planning " + name + "\n")
        (self.root / "app.txt").write_text("Old real business candidate\n")
        self.git("add", ".")
        self.git("commit", "-qm", "legacy root planning candidate")
        self.old_head = self.git("rev-parse", "HEAD").strip()
        self.bind_task(self.root, "00-bootstrap-guidelines")
        self.public = {"profile": "delivery_upgrade", "source_profile": "guru0.6-family", "target_source_ref": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.source, text=True).strip()}
        self.patch_source = patch("owner.source_root", return_value=self.source)
        self.patch_source.start(); self.addCleanup(self.patch_source.stop)
        # The source/profile integration invokes upstream for real; production
        # preset and actual installed gates are exercised by the joint owner.
        self.module = types.SimpleNamespace(
            MANAGED_ASSET_PATHS=(),
            managed_transaction_paths=lambda *args: {Path(".trellis/guru-team/extension.json"), Path(".trellis/workflow.md")},
            prune_empty_managed_skill_parents=lambda *args: None,
            managed_source_projections=lambda *args: {},
        )
        self.patch_installer = patch("owner.installer", return_value=self.module)
        self.patch_installer.start(); self.addCleanup(self.patch_installer.stop)

    def execute(self, argv):
        result = subprocess.run(argv, cwd=self.root, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr[-1000:])
        return result.stdout

    def git(self, *args):
        return self.execute(["git", *args])

    def binding_store(self, target):
        def fact(argument):
            value = subprocess.check_output(["git", "rev-parse", argument], cwd=target, text=True).strip()
            return (target / value).resolve()
        return BranchBindingStore(RepositoryFacts(target, fact("--git-common-dir"), fact("--absolute-git-dir")))

    def bind_task(self, target, task_id):
        branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=target, text=True).strip()
        return self.binding_store(target).establish(TaskLifecycleKey(task_id, 0), branch)

    def raw(self, target, ref):
        path = target / ref
        if not path.exists():
            return None
        return {"content_base64": base64.b64encode(path.read_bytes()).decode(), **state(path)}

    def projected(self, old, key=None, authority=None, contract=None):
        result = subprocess.run(["node", "--input-type=module", "-e", BUILD_RECORD], input=json.dumps({"core": str(self.core), "old": old, "key": key, "authority": authority, "contract": contract}), text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr[-500:])
        return json.loads(result.stdout)

    def plan(self, workspace_roots=None, deferred_workspaces=()):
        selected = workspace_roots or {"primary": self.root}
        core_plan = {"schema_version": "2.0", "source": {"version": "0.7.0-castbox.3", "task_schema": "1.0", "delivery_api": None},
                     "target": {"version": "0.7.0-castbox.3", "task_schema": "2.0", "delivery_api": "1.0"},
                     "workspaces": [{"id": key, "root": str(value), "project_relative": getattr(self, "project_relative", None)} for key, value in selected.items()],
                     "installations": [], "tasks": [], "sessions": [], "workflows": [], "templates": [], "files": []}
        for workspace, target in selected.items():
            template = call(target, self.fork, "templates")
            core_plan["templates"].append({"workspace": workspace, "candidate_sha256": template["candidate_sha256"], "files": template["files"]})
            core_plan["installations"].append({"workspace": workspace, "version_source": self.raw(target, ".trellis/.version"), "receipt_source": self.raw(target, ".trellis/.template-hashes.json")})
            for path in (target / ".trellis/tasks").rglob("task.json"):
                ref = path.parent.relative_to(target).as_posix(); raw = self.raw(target, ref + "/task.json")
                old = json.loads(path.read_text())
                archived = ref.startswith(".trellis/tasks/archive/")
                row = {"workspace": workspace, "task_ref": ref, "source": raw, "disposition": "history_only" if archived else "defer" if workspace in deferred_workspaces else "convert_active"}
                if not archived and workspace not in deferred_workspaces:
                    row["record"] = self.projected(old)
                    row["legacy_facts"] = [{"field": name, "disposition": "source_snapshot", "owner_id": "controlled-upgrade-owner", "reason": {"locator": ref + "/migration/source-task.json", "revision": "sha256:" + raw["sha256"]}}
                                           for name in ("commit", "pr_url", "completedAt") if old.get(name)]
                core_plan["tasks"].append(row)
                for artifact in path.parent.rglob("*"):
                    if artifact.is_file() and artifact != path:
                        relative = artifact.relative_to(target).as_posix()
                        core_plan["files"].append({"target": {"kind": "project", "workspace": workspace, "path": relative}, "owner": "preserve", "action": "preserve", "source": self.raw(target, relative)})
            for item in template["files"]:
                name = item["path"]
                core_plan["files"].append({"target": {"kind": "project", "workspace": workspace, "path": name}, "owner": "template", "action": "write", "source": self.raw(target, name), "target_content_base64": template["contents"][name], "target_mode": item["mode"]})
            text = (self.source / "trellis/workflows/guru-team/workflow.md").read_text()
            contract = json.loads(text.split("[trellis-runtime-contract]", 1)[1].split("[/trellis-runtime-contract]", 1)[0])
            core_plan["workflows"].append({"workspace": workspace, "template_id": "guru-team", "contract": contract})
            core_plan["files"].append({"target": {"kind": "project", "workspace": workspace, "path": ".trellis/workflow.md"}, "owner": "workflow", "action": "write", "source": self.raw(target, ".trellis/workflow.md"), "target_content_base64": base64.b64encode(text.encode()).decode(), "target_mode": 0o644})
            receipt = json.loads((target / ".trellis/.template-hashes.json").read_text())
            for name in receipt["hashes"]:
                if name not in template["contents"] and name.startswith((".trellis/scripts/", ".trellis/agents/")):
                    core_plan["files"].append({"target": {"kind": "project", "workspace": workspace, "path": name}, "owner": "preserve", "action": "preserve", "source": self.raw(target, name)})
        common = Path(self.git("rev-parse", "--git-common-dir").strip())
        if not common.is_absolute(): common = self.root / common
        session_roots = [(common, "trellis/sessions", {"kind": "common_session"})] + [(target, ".trellis/.runtime/sessions", {"kind": "local_session", "workspace": workspace}) for workspace, target in selected.items()]
        for directory, ref, kind in session_roots:
            for path in (directory / ref).glob("*.json"):
                core_plan["sessions"].append({"target": {**kind, "filename": path.name}, "source": self.raw(directory, ref + "/" + path.name)})
        core_plan["branch_bindings"] = upgrade.prepare_inventory(self.root, None)["branch_bindings"]
        return {"core_plan": core_plan, "dependency_mode": "local_candidate", "source_candidate": upgrade.freeze_source(self.source), "fork_candidate": upgrade.freeze_fork(self.fork),
                "guru_workspaces": [{"workspace": key, "selected_platforms": ["codex"], "decisions": []} for key in selected], "controls": [], "owner_migrations": []}

    def tree(self):
        return {str(p): state(p) for p in self.root.rglob("*") if p.is_file() and ".git" not in p.parts}

    def test_prospective_preview_is_zero_write_and_preserves_old_active_root(self):
        plan = self.plan(); before = self.tree()
        facts = upgrade.preview(PACKAGE, self.root, self.public, plan, self.fork)
        self.assertEqual(facts["core"]["status"], "preview")
        self.assertEqual(self.tree(), before)
        self.assertEqual(self.git("rev-parse", "HEAD").strip(), self.old_head)
        self.assertEqual(json.loads((self.root / self.ref / "task.json").read_text())["status"], "in_progress")

    def test_real_legacy_monorepo_init_keeps_plan2_project_root_for_upgrade_and_rollback(self):
        nested = DeliveryUpgradeTests()
        nested.project_relative = "app"
        nested.setUp(); self.addCleanup(nested.doCleanups)
        plan = nested.plan(); before = nested.tree()
        for row in plan["core_plan"]["sessions"]:
            if row["target"]["kind"] == "common_session":
                original = json.loads(base64.b64decode(row["source"]["content_base64"]))
                row["record"] = {**original, "schema_version": 3, "delivery_id": None}
        facts = upgrade.preview(PACKAGE, nested.root, nested.public, plan, nested.fork)
        self.assertEqual(facts["core"]["status"], "preview")
        self.assertEqual(nested.tree(), before)
        recovery, checkpoint = upgrade.begin(PACKAGE, nested.root, nested.public, plan, nested.fork)
        nested.module.install_assets = lambda *args, **kwargs: (_ for _ in ()).throw(SystemExit("normal preset pause"))
        result = upgrade.resume(PACKAGE, nested.root, recovery, checkpoint)
        self.assertEqual(result["exit_id"], "delivery_resume_required")
        self.assertEqual(checkpoint["phase"], "preset", checkpoint.get("failure"))
        self.assertEqual(json.loads((nested.root / nested.ref / "task.json").read_text())["schema_version"], "2.0")
        self.assertFalse((nested.root / "app").exists())
        self.assertEqual(upgrade.business(checkpoint), checkpoint["business_before"])
        replay = upgrade.resume(PACKAGE, nested.root, recovery, json.loads((recovery / "checkpoint.json").read_text()))
        self.assertEqual(replay, result)
        self.assertEqual(upgrade.rollback(nested.root, recovery, checkpoint)["exit_id"], "rolled_back")
        self.assertEqual(nested.tree(), before)

    def test_real_plan2_same_plan_preserves_committed_root_candidate_and_old_history(self):
        archive = self.root / ".trellis/tasks/archive/2026-10/older-dependency"
        archive.mkdir(parents=True)
        write_json(archive / "task.json", {"id": "older-dependency", "status": "completed", "completedAt": "2026-09-20"})
        (archive / "dependency.md").write_text("Provider facts missing for scenario B; independent scenario A retained\n")
        plan = self.plan(); source = (self.root / self.ref / "prd.md").read_bytes()
        before_history = (archive / "task.json").read_bytes()
        call(self.root, self.fork, "migrate", plan["core_plan"])
        first = self.tree(); call(self.root, self.fork, "migrate", plan["core_plan"])
        self.assertEqual(self.tree(), first)
        self.assertEqual((self.root / self.ref / "prd.md").read_bytes(), source)
        self.assertEqual((archive / "task.json").read_bytes(), before_history)
        task = json.loads((self.root / self.ref / "task.json").read_text())
        self.assertEqual(task["id"], "00-bootstrap-guidelines");self.assertEqual(task["deliveries"], [])
        self.assertEqual(self.git("rev-parse", "HEAD").strip(), self.old_head)
        self.assertEqual((self.root / self.ref / "migration/source-task.json").read_bytes(), base64.b64decode(plan["core_plan"]["tasks"][0]["source"]["content_base64"]))

    def test_partial_preset_resume_and_rollback_restore_actual_plan2_bytes_modes(self):
        plan = self.plan(); before = self.tree()
        recovery, checkpoint = upgrade.begin(PACKAGE, self.root, self.public, plan, self.fork)
        self.module.install_assets = lambda *args, **kwargs: (_ for _ in ()).throw(SystemExit("normal unresolved customization"))
        result = upgrade.resume(PACKAGE, self.root, recovery, checkpoint)
        self.assertEqual(result["exit_id"], "delivery_resume_required")
        self.assertEqual(checkpoint["phase"], "preset")
        post = self.tree()
        result2 = upgrade.resume(PACKAGE, self.root, recovery, checkpoint, copy.deepcopy(plan))
        self.assertEqual(result2, result);self.assertEqual(self.tree(), post)
        reverted = upgrade.rollback(self.root, recovery, checkpoint)
        self.assertEqual(reverted["exit_id"], "rolled_back")
        self.assertEqual(self.tree(), before);self.assertFalse(recovery.exists())

    def test_source_candidate_edit_blocks_before_writes_and_resume_never_refreezes(self):
        plan = self.plan(); before = self.tree()
        (self.source / "trellis/guru-team-extension.json").write_text('{"version":"0.7.0-guru.4","normal":"new edit"}')
        with self.assertRaisesRegex(MigrationError, "frozen candidate"):
            upgrade.begin(PACKAGE, self.root, self.public, plan, self.fork)
        self.assertEqual(self.tree(), before)

    def test_new_business_archive_or_session_work_blocks_rollback(self):
        plan = self.plan(); recovery, checkpoint = upgrade.begin(PACKAGE, self.root, self.public, plan, self.fork)
        self.module.install_assets = lambda *args, **kwargs: (_ for _ in ()).throw(SystemExit("pause"))
        upgrade.resume(PACKAGE, self.root, recovery, checkpoint)
        new = self.root / ".trellis/tasks/archive/2026-10/new-observation/note.md"
        new.parent.mkdir(parents=True);new.write_text("new original-owner evidence\n")
        self.assertEqual(upgrade.rollback(self.root, recovery, checkpoint)["exit_id"], "blocked")
        self.assertTrue(new.is_file())

    def test_omitted_occupied_archive_or_session_is_upstream_rejected_without_writes(self):
        plan = self.plan()
        archive = self.root / ".trellis/tasks/archive/2026-10/occupied"
        archive.mkdir(parents=True);(archive / "task.json").write_text('{"id":"occupied","status":"completed"}')
        before = self.tree()
        with self.assertRaises(MigrationError):upgrade.preview(PACKAGE, self.root, self.public, plan, self.fork)
        self.assertEqual(self.tree(), before)

    def test_all_profiles_and_private_checkpoint_are_independent_versioned_contracts(self):
        from runtime.schema import validate_json
        for profile in ("delivery_upgrade", "delivery_resume", "delivery_rollback"):
            validate_json(json.loads((PACKAGE / f"examples/public-{profile}-input.json").read_text()), PACKAGE / "schemas/public-input.schema.json", "input")
        plan = self.plan()
        validate_json(plan, PACKAGE / "schemas/private-delivery-plan.schema.json", "plan")
        recovery, checkpoint = upgrade.begin(PACKAGE, self.root, self.public, plan, self.fork)
        validate_json(checkpoint, PACKAGE / "schemas/private-delivery-recovery.schema.json", "checkpoint")

    def test_current_delivery_entry_never_selects_historical_plan1_fallback(self):
        path = self.directory / "old-input.json"
        write_json(path, {"profile": "initial_upgrade", "source_profile": "guru0.6-family", "target_source_ref": self.public["target_source_ref"]})
        before = self.tree()
        result = run(PACKAGE, {"runtime_role": "invoke"}, ["--root", str(self.root), "--input", str(path)])
        self.assertEqual(result["exit_id"], "blocked")
        self.assertIn("Historical Plan1", result["reason"])
        self.assertEqual(self.tree(), before)

    def test_registered_multiple_workspaces_and_common_sessions_restore_raw_modes(self):
        sibling = self.directory / "second-workspace"
        self.git("worktree", "add", "-qb", "second-workspace", str(sibling))
        # Each worktree owns its actual Task; removing this fixture-only copied
        # directory avoids a duplicate public Task identity across workspaces.
        shutil.rmtree(sibling / self.ref)
        result = subprocess.run([sys.executable, ".trellis/scripts/task.py", "create", "Independent consumer", "--slug", "independent-consumer", "--description", "Scenario A continues while scenario B awaits provider facts", "--no-start"], cwd=sibling, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr[-500:])
        self.bind_task(sibling, "independent-consumer")
        plan = self.plan({"primary": self.root, "second": sibling})
        self.assertEqual(len(plan["core_plan"]["workspaces"]), 2)
        self.assertTrue(any(row["target"]["kind"] == "common_session" for row in plan["core_plan"]["sessions"]))
        original = {str(path): state(path) for target in (self.root, sibling)
                    for path in target.rglob("*") if path.is_file() and ".git" not in path.parts and path.name != ".git"}
        recovery, checkpoint = upgrade.begin(PACKAGE, self.root, self.public, plan, self.fork)
        self.module.install_assets = lambda *args, **kwargs: (_ for _ in ()).throw(SystemExit("pause"))
        result = upgrade.resume(PACKAGE, self.root, recovery, checkpoint)
        self.assertEqual(result["exit_id"], "delivery_resume_required")
        for row in plan["core_plan"]["tasks"]:
            target = self.root if row["workspace"] == "primary" else sibling
            self.assertEqual(json.loads((target / row["task_ref"] / "task.json").read_text())["schema_version"], "2.0")
        self.assertEqual(upgrade.rollback(self.root, recovery, checkpoint)["exit_id"], "rolled_back")
        actual = {str(path): state(path) for target in (self.root, sibling)
                  for path in target.rglob("*") if path.is_file() and ".git" not in path.parts and path.name != ".git"}
        self.assertEqual(actual, original)

    def test_retained_history_reapply_requires_actual_checkpoint_and_exact_preimage(self):
        archive = self.root / ".trellis/tasks/archive/2026-10/old-finished"
        archive.mkdir(parents=True);(archive / "task.json").write_text('{"id":"old-finished","status":"completed"}')
        (archive / "task.json").chmod(0o640)
        plan = self.plan();recovery, checkpoint = upgrade.begin(PACKAGE, self.root, self.public, plan, self.fork)
        self.module.install_assets = lambda *args, **kwargs: (_ for _ in ()).throw(SystemExit("pause"))
        upgrade.resume(PACKAGE, self.root, recovery, checkpoint)
        sys.path.insert(0, str(SOURCE / "trellis/presets/guru-team/scripts/python"))
        from delivery_installation import diagnose_delivery_installation
        result = diagnose_delivery_installation(self.source, self.root)
        self.assertEqual(result["status"], "supported_candidate", result)
        (archive / "task.json").write_text('{"id":"old-finished","status":"completed","notes":"ordinary new work"}')
        result = diagnose_delivery_installation(self.source, self.root)
        self.assertEqual(result["code"], "upstream_delivery_migration_required")
        self.assertEqual(upgrade.rollback(self.root, recovery, checkpoint)["exit_id"], "blocked")

    def test_lost_public_output_reentry_reuses_completed_core_and_same_backup(self):
        plan = self.plan();recovery, checkpoint = upgrade.begin(PACKAGE, self.root, self.public, plan, self.fork)
        self.module.install_assets = lambda *args, **kwargs: (_ for _ in ()).throw(SystemExit("pause"))
        upgrade.resume(PACKAGE, self.root, recovery, checkpoint)
        old = json.loads((recovery / "checkpoint.json").read_text())
        with patch("delivery_upgrade.call", side_effect=AssertionError("Core must not execute twice")):
            result = upgrade.resume(PACKAGE, self.root, recovery, old)
        self.assertEqual(result["recovery_ref"], recovery.name)
        self.assertEqual(old["preimages"], checkpoint["preimages"])

    def paused_preset(self):
        recovery, checkpoint = upgrade.begin(PACKAGE, self.root, self.public, self.plan(), self.fork)
        self.module.install_assets = Mock(side_effect=SystemExit("normal preset pause"))
        result = upgrade.resume(PACKAGE, self.root, recovery, checkpoint)
        self.assertEqual(result["exit_id"], "delivery_resume_required")
        self.assertTrue(checkpoint["core_completed"])
        self.assertEqual(checkpoint["phase"], "preset", checkpoint.get("failure"))
        self.assertEqual(self.module.install_assets.call_count, 1)
        return recovery, checkpoint

    def assert_paused_topology_change_is_preserved(self, recovery, checkpoint):
        post = self.tree()
        frozen = (recovery / "checkpoint.json").read_bytes()
        sessions = self.binding_store(self.root).repository.common_dir / "trellis/sessions"
        session_before = {p.name: upgrade.raw_snapshot(p) for p in sessions.glob("*.json")}
        self.assertEqual(upgrade.current(checkpoint), checkpoint["baseline"])
        loaded = json.loads(frozen)
        with patch("delivery_upgrade.call", side_effect=AssertionError("Completed Core must not execute twice")):
            with self.assertRaisesRegex(MigrationError, "Ordinary work changed"):
                upgrade.resume(PACKAGE, self.root, recovery, loaded)
        self.assertEqual(self.module.install_assets.call_count, 1)
        self.assertEqual(upgrade.rollback(self.root, recovery, loaded),
                         {"exit_id": "blocked", "reason": "work_since_delivery_migration"})
        self.assertEqual(self.tree(), post)
        self.assertEqual({p.name: upgrade.raw_snapshot(p) for p in sessions.glob("*.json")}, session_before)
        self.assertEqual((recovery / "checkpoint.json").read_bytes(), frozen)
        self.assertEqual(loaded, checkpoint)

    def test_post_core_registration_change_blocks_resume_and_rollback_preserving_new_worktree(self):
        recovery, checkpoint = self.paused_preset()
        sibling = self.directory / "new-registered"
        self.git("worktree", "add", "-qb", "new-registered", str(sibling))
        peer_before = {p.relative_to(sibling).as_posix(): upgrade.raw_snapshot(p)
                       for p in sibling.rglob("*") if p.is_file() and p.name != ".git"}
        registrations = self.git("worktree", "list", "--porcelain", "-z")
        self.assert_paused_topology_change_is_preserved(recovery, checkpoint)
        self.assertEqual(self.git("worktree", "list", "--porcelain", "-z"), registrations)
        self.assertEqual({p.relative_to(sibling).as_posix(): upgrade.raw_snapshot(p)
                          for p in sibling.rglob("*") if p.is_file() and p.name != ".git"}, peer_before)
        self.assertEqual(subprocess.check_output(["git", "branch", "--show-current"], cwd=sibling, text=True).strip(), "new-registered")

    def test_post_core_same_head_branch_change_blocks_resume_and_rollback_preserving_selection(self):
        recovery, checkpoint = self.paused_preset()
        self.git("checkout", "-qb", "normal-new-route")
        self.assertEqual(self.git("rev-parse", "HEAD").strip(), self.old_head)
        self.assert_paused_topology_change_is_preserved(recovery, checkpoint)
        self.assertEqual(self.git("branch", "--show-current").strip(), "normal-new-route")

    def taskcommit_plan(self, plan=None):
        plan = plan or self.plan()
        key = {"task_id": "00-bootstrap-guidelines", "lifecycle_generation": 0, "delivery_id": "c13a62ec-4ce7-4406-ab7c-fa1537a07658"}
        row = plan["core_plan"]["tasks"][0]
        authority = {"locator": self.ref + "/prd.md", "revision": "sha256:" + state(self.root / self.ref / "prd.md")["sha256"]}
        record = self.projected(json.loads(base64.b64decode(row["source"]["content_base64"])), key,
                                authority, plan["core_plan"]["workflows"][0]["contract"])
        row["record"] = record
        planning = record["deliveries"][0]["planning_root"]
        for name in ("prd.md", "design.md", "implement.md", "implement.jsonl", "check.jsonl"):
            source = self.raw(self.root, self.ref + "/" + name)
            plan["core_plan"]["files"].append({"target": {"kind": "project", "workspace": "primary", "path": self.ref + "/" + planning + "/" + name},
                                                  "owner": "artifact", "action": "write", "source": None,
                                                  "target_content_base64": source["content_base64"], "target_mode": source["mode"]})
        inputs = self.root / ".trellis/.runtime/inputs"
        write_json(inputs / "plan.json", plan["core_plan"])
        write_json(inputs / "source-review.json", {"status": "passed", "summary": "Fixture original TaskCommit semantic result.", "evidence": ["Actual original root Git blobs and reviewed Plan2 artifact mappings."]})
        public = {"profile": "delivery_source_migration", "task_ref": self.ref, "delivery_key": key,
                  "source_commit": self.old_head, "planning_sources": {name: self.ref + "/" + name for name in ("prd.md", "design.md", "implement.md", "implement.jsonl", "check.jsonl")},
                  "plan_file": str(inputs / "plan.json"), "workspace": "primary"}
        private = ".trellis/.runtime/guru-team/task-commit-sources/" + key["delivery_id"] + "/source.json"
        plan["owner_migrations"].append({"workspace": "primary", "skill_id": "guru-create-task-commit", "command_id": "migrate-task-commit-planning-source",
                                          "input": public, "owner_result": str(inputs / "source-review.json"), "paths": [private]})
        return plan, private

    def test_prepare_collects_inherited_planning_and_binding_without_deciding_dispositions(self):
        sibling = self.directory / "inherited-copy"
        self.git("worktree", "add", "-qb", "inherited-copy", str(sibling))
        peer_prd = sibling / self.ref / "prd.md"
        peer_prd.write_text("Same Task, independent mutable branch planning\n")
        peer_prd.chmod(0o640)
        archive = sibling / ".trellis/tasks/archive/2026-10/occupied-without-record"
        archive.mkdir(parents=True);(archive / "history.md").write_text("Original occupied historical directory\n")
        before = {str(p): state(p) for target in (self.root, sibling) for p in target.rglob("*") if p.is_file() and ".git" not in p.parts}
        facts = upgrade.preview(PACKAGE, self.root, self.public, None, self.fork)
        inventory = facts["inventory"]
        self.assertEqual({row["root"] for row in inventory["workspaces"]}, {str(self.root), str(sibling)})
        self.assertEqual(len(inventory["branch_bindings"]), 1)
        binding = inventory["branch_bindings"][0]
        self.assertEqual(set(binding), {"task_id", "lifecycle_generation", "source"})
        self.assertEqual(binding["source"], upgrade.raw_snapshot(self.binding_store(self.root).path_for(TaskLifecycleKey("00-bootstrap-guidelines", 0))))
        peer = next(row for row in inventory["workspaces"] if row["root"] == str(sibling))
        task = next(row for row in peer["tasks"] if row["task_ref"] == self.ref)
        self.assertEqual(base64.b64decode(task["artifacts"][self.ref + "/prd.md"]["content_base64"]), peer_prd.read_bytes())
        self.assertNotIn("disposition", task)
        self.assertIsNone(next(row for row in peer["tasks"] if row["task_ref"].endswith("occupied-without-record"))["source"])
        after = {str(p): state(p) for target in (self.root, sibling) for p in target.rglob("*") if p.is_file() and ".git" not in p.parts}
        self.assertEqual(before, after)

    def test_inherited_peer_preserved_through_real_migration_replay_private_resume_and_rollback(self):
        sibling = self.directory / "inherited-copy"
        self.git("worktree", "add", "-qb", "inherited-copy", str(sibling))
        (sibling / self.ref / "prd.md").write_text("Independent inherited planning bytes\n")
        (sibling / self.ref / "prd.md").chmod(0o640)
        plan, private = self.taskcommit_plan(self.plan({"primary": self.root, "peer": sibling}, ("peer",)))
        key = plan["owner_migrations"][0]["input"]["delivery_key"]
        for row in plan["core_plan"]["sessions"]:
            if row["target"]["kind"] == "common_session":
                row["record"] = {"schema_version": 3, **key}
        peer_before = {p.relative_to(sibling).as_posix(): state(p) for p in (sibling / self.ref).rglob("*") if p.is_file()}
        binding_path = self.binding_store(self.root).path_for(TaskLifecycleKey(key["task_id"], 0))
        binding_before = upgrade.raw_snapshot(binding_path)
        recovery, checkpoint = upgrade.begin(PACKAGE, self.root, self.public, plan, self.fork)
        anchors = copy.deepcopy(checkpoint["preimages"])
        self.module.install_assets = lambda *args, **kwargs: (_ for _ in ()).throw(SystemExit("normal preset pause"))
        result = upgrade.resume(PACKAGE, self.root, recovery, checkpoint)
        self.assertEqual(result["exit_id"], "delivery_resume_required")
        self.assertEqual(checkpoint["phase"], "preset", checkpoint.get("failure"))
        self.assertTrue((self.root / private).is_file()); self.assertFalse((sibling / private).exists())
        for target in (self.root, sibling):
            outcome = subprocess.run([sys.executable, ".trellis/scripts/delivery.py", "current", "--json"], cwd=target, text=True, capture_output=True)
            self.assertEqual(outcome.returncode, 0, outcome.stderr[-500:])
            current = json.loads(outcome.stdout)
            self.assertEqual(current["kind"], "current", current)
            self.assertEqual(current["key"], key)
        first = self.tree()
        self.assertEqual(call(self.root, self.fork, "migrate", plan["core_plan"])["status"], "migrated")
        self.assertEqual(self.tree(), first)
        loaded = json.loads((recovery / "checkpoint.json").read_text())
        with patch("delivery_upgrade.call", side_effect=AssertionError("Completed Core must not execute twice")):
            self.assertEqual(upgrade.resume(PACKAGE, self.root, recovery, loaded)["recovery_ref"], result["recovery_ref"])
        self.assertEqual(loaded["preimages"], anchors)
        self.assertEqual({p.relative_to(sibling).as_posix(): state(p) for p in (sibling / self.ref).rglob("*") if p.is_file()}, peer_before)
        self.assertEqual(upgrade.raw_snapshot(binding_path), binding_before)
        self.assertEqual(upgrade.rollback(self.root, recovery, loaded)["exit_id"], "rolled_back")
        self.assertEqual({p.relative_to(sibling).as_posix(): state(p) for p in (sibling / self.ref).rglob("*") if p.is_file()}, peer_before)
        self.assertFalse((self.root / private).exists())

    def test_normal_binding_and_registration_changes_require_fresh_prepare(self):
        plan = self.plan(); before = self.tree()
        self.git("checkout", "-qb", "normal-rebind")
        self.binding_store(self.root).advance(TaskLifecycleKey("00-bootstrap-guidelines", 0), expected_revision=0, branch_name="normal-rebind")
        with self.assertRaises(MigrationError):
            upgrade.preview(PACKAGE, self.root, self.public, plan, self.fork)
        self.assertEqual(self.tree(), before)
        self.assertEqual(upgrade.preview(PACKAGE, self.root, self.public, self.plan(), self.fork)["core"]["status"], "preview")
        frozen = self.plan()
        self.git("worktree", "add", "-qb", "new-registered", str(self.directory / "new-registered"))
        with self.assertRaises(MigrationError):
            upgrade.preview(PACKAGE, self.root, self.public, frozen, self.fork)

    def test_git_free_public_combination_keeps_no_binding_rows(self):
        plan = self.plan()["core_plan"]
        standalone = self.directory / "git-free"
        shutil.copytree(self.root, standalone, ignore=shutil.ignore_patterns(".git"))
        inventory = upgrade.prepare_inventory(standalone, self.fork)
        self.assertEqual(inventory["branch_bindings"], [])
        self.assertEqual(inventory["common_sessions"], {})
        plan["workspaces"][0]["root"] = str(standalone)
        plan.pop("branch_bindings")
        plan["sessions"] = [row for row in plan["sessions"] if row["target"]["kind"] == "local_session"]
        before = {str(p): state(p) for p in standalone.rglob("*") if p.is_file()}
        self.assertEqual(call(standalone, self.fork, "preview", plan)["status"], "preview")
        self.assertEqual({str(p): state(p) for p in standalone.rglob("*") if p.is_file()}, before)
        self.assertEqual(call(standalone, self.fork, "migrate", plan)["status"], "migrated")
        self.assertEqual(json.loads((standalone / self.ref / "task.json").read_text())["schema_version"], "2.0")

    def test_real_plan2_mapping_reaches_original_taskcommit_private_source_consumer(self):
        plan, private = self.taskcommit_plan()
        recovery, checkpoint = upgrade.begin(PACKAGE, self.root, self.public, plan, self.fork)
        self.module.install_assets = lambda *args, **kwargs: (_ for _ in ()).throw(SystemExit("pause after real private producer"))
        result = upgrade.resume(PACKAGE, self.root, recovery, checkpoint)
        self.assertEqual(result["exit_id"], "delivery_resume_required")
        self.assertEqual(checkpoint["phase"], "preset", checkpoint.get("failure"))
        self.assertEqual(checkpoint["owner_index"], 1)
        self.assertEqual(json.loads((self.root / private).read_text())["source_commit"], self.old_head)
        self.assertEqual(self.git("rev-parse", "HEAD").strip(), self.old_head)
        self.assertEqual(upgrade.rollback(self.root, recovery, checkpoint)["exit_id"], "rolled_back")
        self.assertFalse((self.root / private).exists())

    def test_original_owner_preview_stops_omitted_private_path_before_write(self):
        plan, private = self.taskcommit_plan()
        # An ordinary incomplete caller inventory must not expand the original
        # rollback anchors once Core has already created the target projection.
        plan["owner_migrations"][0]["paths"] = []
        before = self.tree()
        recovery, checkpoint = upgrade.begin(PACKAGE, self.root, self.public, plan, self.fork)
        anchors = copy.deepcopy(checkpoint["preimages"])
        result = upgrade.resume(PACKAGE, self.root, recovery, checkpoint)
        self.assertEqual(result["exit_id"], "delivery_resume_required")
        self.assertEqual(checkpoint["phase"], "owners")
        self.assertEqual(checkpoint["owner_index"], 0)
        self.assertIn("frozen initial backup", checkpoint["failure"]["detail"])
        self.assertEqual(checkpoint["preimages"], anchors)
        self.assertFalse((self.root / private).exists())
        self.assertEqual(upgrade.rollback(self.root, recovery, checkpoint)["exit_id"], "rolled_back")
        self.assertEqual(self.tree(), before)


if __name__ == "__main__":
    unittest.main()
