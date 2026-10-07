from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

from jsonschema import Draft202012Validator

PACKAGE = Path(__file__).resolve().parents[1]
SKILLS = PACKAGE.parents[1]
sys.path.insert(0, str(SKILLS))
sys.path.insert(0, str(PACKAGE / "runtime"))
from files import business_state, control_token, current_baseline, snapshot, state, task_token, write_json
from owner import MigrationError, formal_guru_source, old_manifest, old_paths, business_managed_paths, guru_owned, source_profile, preview, core_preview, preserve_customizations, resume, rollback, save_baseline, validate_task_dispositions


class MigrationContractTests(unittest.TestCase):
    def test_independent_profiles_outputs_and_resume_projection(self):
        interface = json.loads((PACKAGE / "interface.json").read_text())
        for profile in interface["public_contracts"]["input"]["profiles"]:
            schema = json.loads((PACKAGE / profile["schema"]["path"]).read_text())
            example = json.loads((PACKAGE / profile["example"]["path"]).read_text())
            Draft202012Validator(schema).validate(example)
        for output in interface["public_contracts"]["outputs"]:
            schema = json.loads((PACKAGE / output["schema"]["path"]).read_text())
            example = json.loads((PACKAGE / output["example"]["path"]).read_text())
            Draft202012Validator(schema).validate(example)
            projection = next(p for p in interface["public_contracts"]["projections"] if p["exit_id"] == output["exit_id"])
            consumer = next(c for c in interface["public_contracts"]["consumer_inputs"] if c["id"] == projection["consumer_input_id"])
            if projection["operation"] == "select":
                projected = {m["target"]: example[m["source"]] for m in projection["mappings"]}
                target = PACKAGE / "schemas/public-resume-input.schema.json"
            else:
                projected = example
                target = SKILLS / consumer["contract"]["path"]
            Draft202012Validator(json.loads(target.read_text())).validate(projected)
            self.assertTrue(output["consumer_use_ids"])

    def test_same_github_repository_transports_are_normal_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for repo in ("https://github.com/castbox/guru-trellis", "https://github.com/castbox/guru-trellis.git", "git@github.com:castbox/guru-trellis.git", "ssh://git@github.com/castbox/guru-trellis.git"):
                with self.subTest(repo=repo):
                    manifest = {"schema_version": "1.0", "extension": {"version": "0.6.5-guru.1", "target_trellis_cli": "0.6.5"}, "source": {"repo": repo, "commit": "a" * 40}}
                    write_json(root / ".trellis/guru-team/extension.json", manifest)
                    self.assertEqual(old_manifest(root)["source"]["repo"], repo)

    def test_preserved_user_work_during_pause_survives_resume_and_blocks_rollback(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            recovery, checkpoint, paths = self.fixture(root)
            plan = checkpoint["plan"]
            plan.update({"dependency_mode": "local_candidate", "workflow": {"action": "preserve"}, "selected_platforms": ["codex"], "guru_decisions": [{"path": "managed.txt", "action": "preserve"}]})
            checkpoint.update({"phase": "preset", "root": str(root), "source": str(root), "source_ref": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(), "fork": "/unused", "old_managed": []})
            checkpoint["business_before"] = business_state(root, business_managed_paths(paths, plan))
            save_baseline(root, recovery, checkpoint)
            fixed = checkpoint["business_before"]
            newer = "normal user customization during pause\n"
            (root / "managed.txt").write_text(newer)
            with patch("owner.source_root", return_value=root), patch("owner.installer") as module, patch("owner.command", return_value='{"status":"passed"}'):
                module.return_value.MANAGED_ASSET_PATHS = []
                module.return_value.managed_source_projections.return_value = {}
                module.return_value.install_assets.return_value = {"skill_packages": {"status": "ok"}, "overlays": {"status": "ok"}, "skill_installed_validation": {"returncode": 0}}
                self.assertEqual(resume(PACKAGE, root, recovery, checkpoint)["exit_id"], "upgraded")
            self.assertEqual(checkpoint["business_before"], fixed)
            self.assertEqual(rollback(root, recovery, checkpoint), {"exit_id": "blocked", "reason": "business_work_since_migration"})
            self.assertEqual((root / "managed.txt").read_text(), newer)

    def test_unknown_old_version_does_not_mutate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / ".trellis/guru-team/extension.json"
            write_json(path, {"schema_version": "2.0", "extension": {"version": "0.8.0-guru.1", "target_trellis_cli": "0.8.0"}})
            before = path.read_bytes()
            with self.assertRaises(MigrationError):
                old_manifest(root)
            self.assertEqual(before, path.read_bytes())

    def test_preserved_core_and_workflow_work_blocks_rollback_after_pause(self):
        for kind, target in (("core", "managed.txt"), ("workflow", ".trellis/workflow.md")):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                recovery, checkpoint, paths = self.fixture(root)
                path = root / target
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("preserved before pause\n")
                paths.add(target)
                checkpoint["preimages"] = snapshot(root, recovery, paths, {})
                plan = checkpoint["plan"]
                plan.update({"workflow": {"action": "preserve"}, "guru_decisions": []})
                plan["core_plan"]["file_decisions"] = [{"path": target, "action": "preserve"}] if kind == "core" else []
                checkpoint["business_before"] = business_state(root, business_managed_paths(paths, plan))
                fixed = checkpoint["business_before"]
                save_baseline(root, recovery, checkpoint)
                path.write_text("normal new work during pause\n")
                save_baseline(root, recovery, checkpoint)
                self.assertEqual(checkpoint["business_before"], fixed)
                self.assertEqual(rollback(root, recovery, checkpoint), {"exit_id": "blocked", "reason": "business_work_since_migration"})
                self.assertEqual(path.read_text(), "normal new work during pause\n")

    def test_formal_source_requires_committed_clean_canonical_candidate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            write_json(root / "trellis/guru-team-extension.json", {"version": "0.7.0-guru.3"})
            skill = root / "trellis/skills/guru-team/packages/guru-upgrade-installation/SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("candidate source\n")
            subprocess.run(["git", "add", "trellis"], cwd=root, check=True, capture_output=True)
            subprocess.run(["git", "commit", "-qm", "candidate"], cwd=root, check=True, capture_output=True)
            # Ordinary task/docs/business dirt outside canonical source is valid.
            formal_guru_source(root, "HEAD")
            skill.write_text("ordinary canonical edit\n")
            with self.assertRaisesRegex(MigrationError, "uncommitted or untracked"):
                formal_guru_source(root, "HEAD")
            skill.write_text("candidate source\n")
            (skill.parent / "new-reference.md").write_text("new untracked canonical contract\n")
            with self.assertRaisesRegex(MigrationError, "uncommitted or untracked"):
                formal_guru_source(root, "HEAD")

    def test_formal_source_rejects_untracked_only_migration_package(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            write_json(root / "trellis/guru-team-extension.json", {"version": "0.7.0-guru.3"})
            subprocess.run(["git", "add", "trellis"], cwd=root, check=True, capture_output=True)
            subprocess.run(["git", "commit", "-qm", "version"], cwd=root, check=True, capture_output=True)
            skill = root / "trellis/skills/guru-team/packages/guru-upgrade-installation/SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("ordinary new package before commit\n")
            with self.assertRaisesRegex(MigrationError, "uncommitted or untracked"):
                formal_guru_source(root, "HEAD")

    def test_old_exact_hash_inventory_not_markers(self):
        row = {"path": ".codex/skills/guru-test/SKILL.md", "sha256": "a" * 64}
        manifest = {"install": {"managed_asset_hashes": {row["path"]: row["sha256"]}},
                    "skill_packages": {"status": "ok", "files": [row], "conflicts": [], "sidecars": []},
                    "overlays": {"status": "ok", "files": [], "conflicts": [], "sidecars": []}}
        self.assertEqual(old_paths(manifest), {row["path"]: "a" * 64})
        manifest["skill_packages"]["files"][0] = {**row, "sha256": "b" * 64}
        with self.assertRaises(MigrationError):
            old_paths(manifest)

    def test_legacy_missing_companion_hash_comes_from_exact_source_commit(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            self.fixture(source)
            write_json(source / "trellis/guru-team-extension.json", {"version": "0.6.16-guru.41"})
            companion = source / "trellis/workflows/guru-team/scripts/bash/prepare-task.sh"
            companion.parent.mkdir(parents=True)
            companion.write_text("legacy exact companion bytes\n")
            subprocess.run(["git", "add", "trellis"], cwd=source, check=True, capture_output=True)
            subprocess.run(["git", "commit", "-qm", "legacy-source"], cwd=source, check=True, capture_output=True)
            commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=source, text=True).strip()
            target = ".trellis/guru-team/scripts/bash/prepare-task.sh"
            manifest = {"source": {"commit": commit}, "install": {"managed_assets": [target], "managed_asset_hashes": {}},
                        "skill_packages": {"status": "ok", "files": [], "conflicts": [], "sidecars": []},
                        "overlays": {"status": "ok", "files": [], "conflicts": [], "sidecars": []}}
            expected = state(companion)["sha256"]
            companion.write_text("ordinary newer source bytes\n")
            self.assertEqual(old_paths(manifest, source), {target: expected})

    def test_all_source_families_accept_actual_manifest_schemas(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for version, core, schema in (("0.6.5-guru.1", "0.6.5", "1.0"),
                    ("0.6.5-guru.25", "0.6.5", "1.0"),
                    ("0.6.5-guru.27", "0.6.5", "2.0"),
                    ("0.6.15-guru.40", "0.6.15", "2.0"),
                    ("0.6.16-guru.41", "0.6.17", "2.0"),
                    ("0.6.17-guru.43", "0.6.17", "2.0"),
                    ("0.7.0-guru.1", "0.7.0-castbox.1", "2.0"),
                    ("0.7.0-guru.2", "0.7.0-castbox.2", "2.0")):
                with self.subTest(version=version, core=core, schema=schema):
                    manifest = {"schema_version": schema, "extension": {"version": version, "target_trellis_cli": core},
                        "source": {"repo": "https://github.com/castbox/guru-trellis.git", "commit": "a" * 40,
                                   "ref": "main", "tree_state": "dirty", "is_mutable_ref": True}}
                    write_json(root / ".trellis/guru-team/extension.json", manifest)
                    self.assertEqual(old_manifest(root), manifest)
                    self.assertEqual(source_profile(version), "guru0.6-family" if version.startswith("0.6.") else "guru0.7.0-family")

    def test_early_observed_predecessor_receipt_uses_formal_release_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            extension = root / "trellis/guru-team-extension.json"
            write_json(extension, {"version": "0.6.5-guru.1", "target_trellis_cli": "0.6.5"})
            companion = root / "trellis/workflows/guru-team/scripts/bash/check-env.sh"
            companion.parent.mkdir(parents=True)
            companion.write_text("predecessor bytes\n")
            subprocess.run(["git", "add", "trellis"], cwd=root, check=True, capture_output=True)
            subprocess.run(["git", "commit", "-qm", "predecessor"], cwd=root, check=True, capture_output=True)
            predecessor = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
            companion.write_text("formal release bytes\n")
            subprocess.run(["git", "add", "trellis"], cwd=root, check=True, capture_output=True)
            subprocess.run(["git", "commit", "-qm", "release"], cwd=root, check=True, capture_output=True)
            subprocess.run(["git", "tag", "v0.6.5-guru.1"], cwd=root, check=True, capture_output=True)
            target = ".trellis/guru-team/scripts/bash/check-env.sh"
            path = root / target
            path.parent.mkdir(parents=True)
            path.write_bytes(companion.read_bytes())
            manifest = {"extension": {"version": "0.6.5-guru.1", "target_trellis_cli": "0.6.5"},
                        "source": {"commit": predecessor, "ref": "main", "tree_state": "dirty"},
                        "install": {"managed_assets": [target, ".agents/skills/trellis-start/SKILL.md"]}}
            self.assertEqual(old_paths(manifest, root, root), {target: state(path)["sha256"]})
            path.write_text("ordinary customization\n")
            self.assertEqual(old_paths(manifest, root, root), {target: None})

    def test_preserved_companion_customization_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / ".trellis/guru-team/scripts/bash/check-env.sh"
            target.parent.mkdir(parents=True)
            target.write_text("ordinary local customization\n")
            canonical = root / "canonical.sh"
            canonical.write_text("current canonical bytes\n")
            plan = {"selected_platforms": ["codex"], "guru_decisions": [{"path": target.relative_to(root).as_posix(), "action": "preserve"}]}
            with patch("owner.installer") as module:
                module.managed_source_projections.return_value = {target.relative_to(root): canonical}
                with self.assertRaisesRegex(MigrationError, "requires reconciliation"):
                    preserve_customizations(root, root, module, plan)
                self.assertEqual(target.read_text(), "ordinary local customization\n")
                self.assertEqual(Path(str(target) + ".new").read_bytes(), canonical.read_bytes())
                target.write_bytes(canonical.read_bytes())
                preserve_customizations(root, root, module, plan)

    def test_early_materialized_configuration_is_user_owned(self):
        path = ".trellis/guru-team/config.yml"
        self.assertFalse(guru_owned(path))
        manifest = {"install": {"managed_assets": [path]}}
        self.assertEqual(old_paths(manifest), {})
        self.assertTrue(guru_owned(".trellis/guru-team/config-template.yml"))

    def test_normal_core_only_update_reports_recorded_and_live_core(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = {"schema_version": "2.0", "extension": {"version": "0.6.16-guru.41", "target_trellis_cli": "0.6.16"},
                        "source": {"repo": "https://github.com/castbox/guru-trellis.git", "commit": "a" * 40},
                        "install": {"managed_assets": [], "selected_platforms": ["codex"]}}
            write_json(root / ".trellis/guru-team/extension.json", manifest)
            (root / ".trellis/.version").write_text("0.6.17\n")
            with patch("owner.source_root", return_value=root), patch("owner.git", return_value="a" * 40):
                facts = preview(PACKAGE, root, {"profile": "initial_upgrade", "source_profile": "guru0.6-family", "target_source_ref": "HEAD"}, None, None)
            self.assertEqual(facts["installed_core"], "0.6.17")
            self.assertEqual(facts["recorded_core"], "0.6.16")
            self.assertEqual(facts["installed_version"], "0.6.16-guru.41")

    def test_actual_source_core_is_passed_to_fork_preview(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch("owner.command", return_value='{"status":"preview"}') as execute:
                self.assertEqual(core_preview(Path(directory), Path("/fixed/fork.js"), {"tasks": []}, "0.6.5"), {"status": "preview"})
                self.assertEqual(execute.call_args.args[0][4], "0.6.5")

    def test_current_task_work_keeps_fixed_rollback_anchor(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            recovery, checkpoint, paths = self.fixture(root)
            ref = ".trellis/tasks/selected"
            path = root / ref / "task.json"
            record = self.current_record()
            record["lifecycle_generation"] = 3
            write_json(path, record)
            checkpoint["plan"]["core_plan"]["current_tasks"] = [{"task_ref": ref, "expected_sha256": state(path)["sha256"]}]
            checkpoint["task_after_core"] = task_token(root, checkpoint)
            anchor = checkpoint["task_after_core"]
            record["meta"]["new_work"] = "current native writer"
            write_json(path, record)
            save_baseline(root, recovery, checkpoint)
            self.assertEqual(checkpoint["task_after_core"], anchor)
            self.assertEqual(rollback(root, recovery, checkpoint)["reason"], "task_work_since_core_migration")
            self.assertEqual(json.loads(path.read_text())["lifecycle_generation"], 3)

    def fixture(self, root):
        for argv in (["git", "init", "-q"], ["git", "config", "user.email", "fixture@example.invalid"], ["git", "config", "user.name", "Fixture"]):
            subprocess.run(argv, cwd=root, check=True, capture_output=True)
        (root / "business.txt").write_text("committed\n")
        subprocess.run(["git", "add", "business.txt"], cwd=root, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True, capture_output=True)
        (root / "business.txt").write_text("ordinary pre-existing business work\n")
        (root / "unrelated.txt").write_text("untracked before upgrade\n")
        (root / "managed.txt").write_text("old runtime\n")
        (root / "managed.txt").chmod(0o755)
        recovery = root / ".git/guru-team/install-upgrade/fixture"
        paths = {"managed.txt", "new-managed.txt"}
        checkpoint = {"preimages": snapshot(root, recovery, paths, {}), "controls": {},
                      "plan": {"core_plan": {"tasks": []}}, "phase": "complete",
                      "old_installation": {"core": "0.6.5", "guru": "0.6.5-guru.1", "source": {}}}
        checkpoint["control_before"] = control_token(checkpoint)
        checkpoint["task_after_core"] = task_token(root, checkpoint)
        checkpoint["business_before"] = business_state(root, paths)
        (root / "managed.txt").write_text("actual updated runtime\n")
        (root / "new-managed.txt").write_text("actual new managed bytes\n")
        checkpoint["baseline"] = current_baseline(root, checkpoint)
        checkpoint["business_after"] = business_state(root, paths)
        return recovery, checkpoint, paths

    def test_actual_post_write_rollback_preserves_dirty_work_and_modes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            recovery, checkpoint, paths = self.fixture(root)
            self.assertIsInstance(checkpoint["business_before"], str)
            result = rollback(root, recovery, checkpoint)
            self.assertEqual(result["exit_id"], "rolled_back")
            self.assertEqual(result["installed_version"], "0.6.5-guru.1")
            self.assertEqual((root / "managed.txt").read_text(), "old runtime\n")
            self.assertEqual(state(root / "managed.txt")["mode"], 0o755)
            self.assertFalse((root / "new-managed.txt").exists())
            self.assertFalse(recovery.exists())
            self.assertEqual((root / "business.txt").read_text(), "ordinary pre-existing business work\n")
            self.assertEqual((root / "unrelated.txt").read_text(), "untracked before upgrade\n")

    def test_new_business_work_blocks_actual_restore(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            recovery, checkpoint, paths = self.fixture(root)
            (root / "business.txt").write_text("new-version work\n")
            result = rollback(root, recovery, checkpoint)
            self.assertEqual(result, {"exit_id": "blocked", "reason": "business_work_since_migration"})
            self.assertEqual((root / "managed.txt").read_text(), "actual updated runtime\n")
            self.assertTrue(recovery.exists())

    def test_new_task_blocks_actual_restore(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            recovery, checkpoint, paths = self.fixture(root)
            write_json(root / ".trellis/tasks/new-task/task.json", {"id": "new-task"})
            self.assertEqual(rollback(root, recovery, checkpoint)["exit_id"], "blocked")
            self.assertTrue((root / ".trellis/tasks/new-task/task.json").exists())

    def current_record(self):
        return {"id": "selected", "name": "selected", "title": "Selected", "description": "", "status": "planning",
                "lifecycle_generation": 0, "source": {"kind": "no_issue"}, "dev_type": None, "scope": None,
                "package": None, "priority": "P2", "createdAt": "", "completedAt": None, "base_branch": None,
                "worktree_path": None, "commit": None, "pr_url": None, "children": [], "parent": None,
                "relatedFiles": [], "notes": "", "meta": {}}

    def test_partial_native_task_work_survives_resume_and_blocks_rollback(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            recovery, checkpoint, paths = self.fixture(root)
            ref = ".trellis/tasks/selected"
            path = root / ref / "task.json"
            write_json(path, {"id": "selected", "creator": "legacy"})
            checkpoint["preimages"].update(snapshot(root, recovery / "task-backup", {ref + "/task.json"}, {}))
            # Preserve a distinct backup path in the combined checkpoint.
            checkpoint["preimages"]["repo:" + ref + "/task.json"]["backup"] = "task-backup/preimages/0"
            paths.add(ref + "/task.json")
            checkpoint["business_before"] = business_state(root, paths)
            record = self.current_record()
            write_json(path, record)
            checkpoint["plan"].update({"dependency_mode": "local_candidate", "workflow": {"action": "preserve"}, "selected_platforms": ["codex"], "guru_decisions": []})
            checkpoint["plan"]["core_plan"]["tasks"] = [{"task_ref": ref}]
            checkpoint["task_after_core"] = task_token(root, checkpoint)
            checkpoint.update({"phase": "preset", "root": str(root), "source": str(root), "source_ref": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(), "fork": "/unused", "old_managed": []})
            save_baseline(root, recovery, checkpoint)
            fixed = checkpoint["task_after_core"]
            record["meta"]["new_work"] = "native task writer result"
            write_json(path, record)
            with patch("owner.source_root", return_value=root), patch("owner.installer") as install:
                install.return_value.install_assets.return_value = {"skill_packages": {"status": "ok"}, "overlays": {"status": "ok"}, "skill_installed_validation": {"returncode": 0}}
                # This unit fixture has no activated target launcher. Even a
                # successful staged result cannot publish installation success.
                self.assertEqual(resume(PACKAGE, root, recovery, checkpoint)["exit_id"], "resume_required")
                self.assertEqual(checkpoint["phase"], "preset")
                with patch("owner.command", return_value='{"status":"passed"}'):
                    self.assertEqual(resume(PACKAGE, root, recovery, checkpoint)["exit_id"], "upgraded")
            self.assertEqual(checkpoint["task_after_core"], fixed)
            self.assertEqual(rollback(root, recovery, checkpoint), {"exit_id": "blocked", "reason": "task_work_since_core_migration"})
            self.assertEqual(json.loads(path.read_text())["meta"]["new_work"], "native task writer result")

    def test_control_anchor_excludes_pointer_alias_and_keeps_new_control_work(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            recovery, checkpoint, paths = self.fixture(root)
            pointer = root / ".git/guru-team/python/active.json"
            control = root / ".git/trellis/binding.json"
            write_json(pointer, {"runtime": "old"})
            write_json(control, {"binding": "before"})
            ctrl = {"python_common": pointer, "python_checkout": pointer, "checkout:guru-team/python/active.json": pointer, "checkout:trellis/binding.json": control}
            checkpoint["controls"] = {k: str(p) for k, p in ctrl.items()}
            checkpoint["preimages"].update(snapshot(root, recovery / "control-backup", set(), ctrl))
            for key, row in checkpoint["preimages"].items():
                if key.startswith("control:"):
                    row["backup"] = "control-backup/" + row["backup"]
            checkpoint["control_before"] = control_token(checkpoint)
            fixed = checkpoint["control_before"]
            write_json(pointer, {"runtime": "current"})
            self.assertEqual(control_token(checkpoint), fixed)
            write_json(control, {"binding": "new legitimate binding work"})
            save_baseline(root, recovery, checkpoint)
            self.assertEqual(checkpoint["control_before"], fixed)
            self.assertEqual(rollback(root, recovery, checkpoint), {"exit_id": "blocked", "reason": "control_work_since_migration"})
            self.assertEqual(json.loads(control.read_text())["binding"], "new legitimate binding work")

    def test_consumed_preset_sidecar_allows_rollback_and_old_anchorless_recovery_blocks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            recovery, checkpoint, paths = self.fixture(root)
            sidecar = "managed.txt.new"
            checkpoint["preimages"].update(snapshot(root, recovery / "sidecar-backup", {sidecar}, {}))
            paths.add(sidecar)
            checkpoint["business_before"] = business_state(root, paths)
            (root / sidecar).write_text("ordinary preset conflict\n")
            save_baseline(root, recovery, checkpoint)
            (root / sidecar).unlink()
            save_baseline(root, recovery, checkpoint)
            self.assertEqual(rollback(root, recovery, checkpoint)["exit_id"], "rolled_back")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            recovery, checkpoint, _ = self.fixture(root)
            del checkpoint["task_after_core"]
            self.assertEqual(rollback(root, recovery, checkpoint)["reason"], "recovery_missing_stable_rollback_anchors")

    def test_deferred_notes_after_partial_resume_failure_block_rollback(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            recovery, checkpoint, paths = self.fixture(root)
            ref = ".trellis/tasks/deferred"
            path = root / ref / "task.json"
            record = {"id": "deferred", "name": "deferred", "title": "Deferred", "status": "planning",
                      "creator": "old", "assignee": "old", "notes": "old notes"}
            write_json(path, record)
            checkpoint["preimages"].update(snapshot(root, recovery / "task-backup", {ref + "/task.json"}, {}))
            checkpoint["preimages"]["repo:" + ref + "/task.json"]["backup"] = "task-backup/preimages/0"
            paths.add(ref + "/task.json")
            checkpoint["business_before"] = business_state(root, paths)
            checkpoint["plan"].update({"dependency_mode": "local_candidate"})
            checkpoint["plan"]["core_plan"]["deferred_tasks"] = [{"task_ref": ref, "expected_sha256": state(path)["sha256"]}]
            checkpoint["task_after_core"] = task_token(root, checkpoint)
            checkpoint.update({"phase": "preset", "root": str(root), "source": str(root),
                               "source_ref": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(), "fork": "/unused"})
            save_baseline(root, recovery, checkpoint)
            fixed = checkpoint["task_after_core"]
            record["notes"] = "ordinary new notes during partial pause"
            write_json(path, record)
            with patch("owner.source_root", return_value=root):
                self.assertEqual(resume(PACKAGE, root, recovery, checkpoint)["exit_id"], "resume_required")
            self.assertEqual(checkpoint["task_after_core"], fixed)
            self.assertEqual(rollback(root, recovery, checkpoint), {"exit_id": "blocked", "reason": "task_work_since_core_migration"})
            self.assertEqual(json.loads(path.read_text())["notes"], record["notes"])

    def test_exact_deferred_inventory_allows_new_current_and_rejects_omission_or_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            old = root / ".trellis/tasks/deferred/task.json"
            write_json(old, {"id": "deferred", "name": "deferred", "title": "Deferred", "status": "planning", "creator": "old", "assignee": "old"})
            write_json(root / ".trellis/tasks/selected/task.json", self.current_record())
            plan = {"core_plan": {"tasks": [], "deferred_tasks": [{"task_ref": ".trellis/tasks/deferred", "expected_sha256": state(old)["sha256"]}]}}
            validate_task_dispositions(root, plan)
            current = self.current_record()
            current.update({"id": "new", "name": "new"})
            write_json(root / ".trellis/tasks/new/task.json", current)
            validate_task_dispositions(root, plan)
            with self.assertRaisesRegex(MigrationError, "differs"):
                validate_task_dispositions(root, {"core_plan": {"tasks": []}})
            data = json.loads(old.read_text())
            data["title"] = "ordinary deferred edit"
            write_json(old, data)
            with self.assertRaisesRegex(MigrationError, "bytes changed"):
                validate_task_dispositions(root, plan)


if __name__ == "__main__":
    unittest.main()
