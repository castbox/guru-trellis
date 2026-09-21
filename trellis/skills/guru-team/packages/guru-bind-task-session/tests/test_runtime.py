import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[6]
RUNTIME = ROOT / "trellis/skills/guru-team/packages/guru-bind-task-session/runtime/invoke.py"


def git(cwd, *args):
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def make_repo():
    repo = Path(tempfile.mkdtemp())
    git(repo, "init", "-q", "-b", "main")
    (repo / "README").write_text("seed\n")
    git(repo, "add", ".")
    subprocess.check_call(["git", "commit", "-qm", "seed"], cwd=repo)
    return repo


def add_task(workspace, name="demo", *, branch=None, base_head=None, meta_workspace=True):
    branch = branch or f"codex/{name}"
    task_ref = f".trellis/tasks/{name}"
    path = workspace / task_ref
    path.mkdir(parents=True)
    data = {"id": name, "status": "in_progress", "branch": branch, "base_branch": "main", "worktree_path": None, "lifecycle_generation": 1, "meta": {}}
    if meta_workspace:
        data["meta"]["worktree_path"] = str(workspace)
    else:
        data["worktree_path"] = str(workspace)
    if base_head is None:
        base_head = git(workspace, "rev-parse", "refs/heads/main")
    data["meta"]["base_head"] = base_head
    (path / "task.json").write_text(json.dumps(data) + "\n")
    return task_ref, data


class FakeModule:
    def __init__(self, root):
        self.active = None
        self.root = root
        self.resolve_roots = []

    def resolve_context_key(self):
        return "codex_fixture"

    def resolve_active_task(self, repo_root):
        self.resolve_roots.append(Path(repo_root).resolve())
        if self.resolve_roots[-1] != self.root.resolve():
            raise AssertionError(f"unexpected repository root: {repo_root}")
        if self.active is None:
            return SimpleNamespace(task_path=None, task_workspace_root=None, repository_common_dir=None, error=None)
        return self.active

    def set_active_task(self, task_ref, workspace):
        resolved_task_path = (workspace / task_ref).resolve()
        raw = Path(git(workspace, "rev-parse", "--git-common-dir")); common = (workspace / raw if not raw.is_absolute() else raw).resolve(); self.active = SimpleNamespace(task_path=task_ref, resolved_task_path=resolved_task_path, task_workspace_root=workspace.resolve(), repository_common_dir=common, error=None)
        return self.active


class BindingRuntimeTest(unittest.TestCase):
    def load(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("binding_runtime_local", RUNTIME)
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        return module
    def test_external_worktree_meta_locator_and_null_top_level_path(self):
        repo = make_repo()
        workspace = repo.parent / ("task-worktree-" + next(tempfile._get_candidate_names()))
        subprocess.check_call(["git", "worktree", "add", "-qb", "codex/demo", str(workspace), "main"], cwd=repo)
        task_ref, data = add_task(workspace, "demo", branch="codex/demo")
        (workspace / task_ref / "task.json").write_text(json.dumps(data) + "\n")
        import importlib.util
        spec = importlib.util.spec_from_file_location("binding_runtime", RUNTIME)
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        facts = mod.task_facts(repo, task_ref, allow_missing_mappings=True)
        self.assertEqual(facts["workspace"], workspace.resolve())
        self.assertEqual(facts["base_branch"], "main")

    def test_repository_common_directory_mismatch_fails(self):
        repo = make_repo()
        task_ref, data = add_task(repo, "demo", branch="main", meta_workspace=False)
        foreign = make_repo()
        data["worktree_path"] = str(repo)
        (repo / task_ref / "task.json").write_text(json.dumps(data) + "\n")
        import importlib.util
        spec = importlib.util.spec_from_file_location("binding_runtime", RUNTIME)
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        with patch.object(mod, "_repo_common_dir", side_effect=[mod._repo_common_dir(repo), foreign / ".git"]):
            with self.assertRaises(Exception) as caught:
                mod.task_facts(repo, task_ref, allow_missing_mappings=True)
        self.assertIn("repository_common_dir", str(caught.exception))

    def test_legacy_base_head_mismatch_does_not_affect_task_identity(self):
        repo = make_repo()
        task_ref, data = add_task(repo, "demo", branch="main", meta_workspace=False, base_head="0" * 40)
        mod = self.load()
        facts = mod.task_facts(repo, task_ref, allow_missing_mappings=True)
        self.assertEqual(facts["task"]["meta"]["base_head"], "0" * 40)
        self.assertNotIn("base_head", facts)

    def test_manual_recovery_conflict_is_zero_write(self):
        repo = make_repo(); task_ref, data = add_task(repo, "demo", branch="main", meta_workspace=False)
        import importlib.util
        spec = importlib.util.spec_from_file_location("binding_runtime", RUNTIME)
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        facts = mod.task_facts(repo, task_ref, allow_missing_mappings=True)
        conflict = repo / ".trellis/.runtime/guru-team/tasks/demo.json"
        conflict.parent.mkdir(parents=True); conflict.write_text(json.dumps({"workspace_path": "/wrong"}))
        with self.assertRaises(Exception):
            mod.write_recovery_mappings(repo, facts, task_ref)
        self.assertFalse((repo / ".trellis/.runtime/guru-team/workspaces/demo.json").exists())

    def test_post_write_validator_rejects_wrong_active_task(self):
        repo = make_repo(); task_ref, data = add_task(repo, "demo", branch="main", meta_workspace=False)
        import importlib.util
        spec = importlib.util.spec_from_file_location("binding_runtime", RUNTIME)
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        facts = mod.task_facts(repo, task_ref, allow_missing_mappings=True)
        wrong_path = repo / ".trellis/tasks/other"
        wrong = SimpleNamespace(task_path=".trellis/tasks/other", resolved_task_path=wrong_path, task_workspace_root=repo, repository_common_dir=facts["common_dir"], error=None)
        with self.assertRaises(Exception):
            mod._assert_post_write(SimpleNamespace(resolve_active_task=lambda repo_root: wrong), repo, facts, task_ref)

    def test_post_write_validator_accepts_relative_task_path_in_external_worktree(self):
        repo = make_repo()
        workspace = repo.parent / ("task-worktree-post-write-" + next(tempfile._get_candidate_names()))
        subprocess.check_call(["git", "worktree", "add", "-qb", "codex/demo", str(workspace), "main"], cwd=repo)
        task_ref, data = add_task(workspace, "demo", branch="codex/demo")
        mod = self.load()
        facts = mod.task_facts(repo, task_ref, allow_missing_mappings=True)
        mod.write_recovery_mappings(repo, facts, task_ref)
        active = SimpleNamespace(
            task_path=task_ref,
            resolved_task_path=(workspace / task_ref).resolve(),
            task_workspace_root=workspace.resolve(),
            repository_common_dir=facts["common_dir"],
            error=None,
        )
        post = mod._assert_post_write(SimpleNamespace(resolve_active_task=lambda repo_root: active), repo, facts, task_ref)
        self.assertEqual(post["workspace"], workspace.resolve())

    def test_active_task_path_fallback_uses_workspace_not_process_cwd(self):
        mod = self.load()
        workspace = Path(tempfile.mkdtemp()).resolve()
        active = SimpleNamespace(task_path=".trellis/tasks/demo", task_workspace_root=workspace)
        self.assertEqual(mod._resolved_active_task_path(active), workspace / ".trellis/tasks/demo")
        missing_workspace = SimpleNamespace(task_path=".trellis/tasks/demo", task_workspace_root=None)
        self.assertIsNone(mod._resolved_active_task_path(missing_workspace))

    def test_switch_requires_source_and_binds_target(self):
        repo = make_repo(); add_task(repo, "a", branch="main", meta_workspace=False); add_task(repo, "b", branch="main", meta_workspace=False)
        import importlib.util
        spec = importlib.util.spec_from_file_location("binding_runtime", RUNTIME)
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        fake = FakeModule(repo); fake.set_active_task(".trellis/tasks/a", repo)
        for ref in (".trellis/tasks/a", ".trellis/tasks/b"):
            facts = mod.task_facts(repo, ref, allow_missing_mappings=True)
            mod.write_recovery_mappings(repo, facts, ref)
        public = {"profile":"switch_task","mode":"standalone","task_ref":".trellis/tasks/b","current_task_ref":".trellis/tasks/a","target_task_ref":".trellis/tasks/b","continuation_id":"c"}
        owner = {**public,"route":"switch","lifecycle_generation":1,"resume_target":"phase-2","ai_review_gate":{"status":"passed","summary":"ok"}}
        with patch.object(mod, "active_module", return_value=fake), patch.object(mod, "session_id", return_value="codex_fixture"):
            output = mod.execute(repo, json.dumps(public), json.dumps(owner))
        self.assertEqual(output["task_ref"], ".trellis/tasks/b")
        self.assertEqual(fake.active.task_path, ".trellis/tasks/b")
        self.assertEqual(fake.active.resolved_task_path, (repo / ".trellis/tasks/b").resolve())
        self.assertEqual(fake.resolve_roots, [repo.resolve(), repo.resolve(), repo.resolve()])

    def test_missing_mapping_without_base_provenance_is_supported(self):
        mod = self.load(); repo = make_repo(); task_ref, data = add_task(repo, "demo", branch="main", meta_workspace=False)
        data["meta"].pop("base_head", None); (repo / task_ref / "task.json").write_text(json.dumps(data) + "\n")
        facts = mod.task_facts(repo, task_ref, allow_missing_mappings=True)
        self.assertEqual(facts["task_ref"], task_ref)
        self.assertNotIn("base_head", facts)

    def test_profile_route_mismatch_is_blocked_before_write(self):
        mod = self.load(); repo = make_repo(); task_ref, data = add_task(repo, "demo", branch="main", meta_workspace=False)
        facts = mod.task_facts(repo, task_ref, allow_missing_mappings=True); mod.write_recovery_mappings(repo, facts, task_ref)
        public = {"profile":"manual_recovery","mode":"standalone","task_ref":task_ref,"continuation_id":"route-mismatch"}
        owner = {**public,"route":"rebind","lifecycle_generation":1,"resume_target":"phase-2","ai_review_gate":{"status":"passed","summary":"ok"}}
        with patch.object(mod, "active_module") as active:
            with self.assertRaises(Exception) as caught:
                mod.execute(repo, json.dumps(public), json.dumps(owner))
        self.assertIn(caught.exception.code, {"schema_mismatch", "stale_identity"}); active.assert_not_called()


class BindingBoundaryCoverageTest(unittest.TestCase):
    def load(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("binding_runtime_extra", RUNTIME)
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        return module

    def test_recovery_is_idempotent_and_old_generation_mapping_is_rejected(self):
        mod = self.load(); repo = make_repo(); task_ref, data = add_task(repo, "demo", branch="main", meta_workspace=False)
        facts = mod.task_facts(repo, task_ref, allow_missing_mappings=True)
        self.assertTrue(mod.write_recovery_mappings(repo, facts, task_ref))
        self.assertEqual(mod.write_recovery_mappings(repo, facts, task_ref), [])
        mapping = repo / ".trellis/.runtime/guru-team/tasks/demo.json"
        payload = json.loads(mapping.read_text()); payload["lifecycle_generation"] = 0; mapping.write_text(json.dumps(payload) + "\n")
        with self.assertRaises(Exception) as caught:
            mod.task_facts(repo, task_ref, allow_missing_mappings=False)
        self.assertIn("lifecycle_generation", str(caught.exception))

    def test_a_to_b_to_a_revalidates_target_each_time(self):
        mod = self.load(); repo = make_repo(); add_task(repo, "a", branch="main", meta_workspace=False); add_task(repo, "b", branch="main", meta_workspace=False)
        for ref in (".trellis/tasks/a", ".trellis/tasks/b"):
            facts = mod.task_facts(repo, ref, allow_missing_mappings=True); mod.write_recovery_mappings(repo, facts, ref)
        fake = FakeModule(repo); fake.set_active_task(".trellis/tasks/a", repo)
        with patch.object(mod, "active_module", return_value=fake), patch.object(mod, "session_id", return_value="codex_fixture"):
            for source, target in (("a", "b"), ("b", "a")):
                public = {"profile":"switch_task","mode":"standalone","task_ref":f".trellis/tasks/{target}","current_task_ref":f".trellis/tasks/{source}","target_task_ref":f".trellis/tasks/{target}","continuation_id":f"{source}-{target}"}
                owner = {**public,"route":"switch","lifecycle_generation":1,"resume_target":"phase-2","ai_review_gate":{"status":"passed","summary":"ok"}}
                output = mod.execute(repo, json.dumps(public), json.dumps(owner))
                self.assertEqual(output["task_ref"], f".trellis/tasks/{target}")
                self.assertEqual(fake.active.task_path, f".trellis/tasks/{target}")
                self.assertEqual(fake.active.resolved_task_path, (repo / f".trellis/tasks/{target}").resolve())

    def test_unknown_branch_and_missing_session_fail_closed(self):
        mod = self.load(); repo = make_repo(); task_ref, data = add_task(repo, "demo", branch="wrong", meta_workspace=False)
        with self.assertRaises(Exception) as caught:
            mod.task_facts(repo, task_ref, allow_missing_mappings=True)
        self.assertIn("branch", str(caught.exception))
        data["branch"] = "main"; (repo / task_ref / "task.json").write_text(json.dumps(data) + "\n")
        with patch.object(mod, "active_module", side_effect=Exception("missing session")):
            public = {"profile":"rebind_missing_session","mode":"standalone","task_ref":task_ref,"continuation_id":"missing"}
            owner = {**public,"route":"rebind","lifecycle_generation":1,"resume_target":"phase-2","ai_review_gate":{"status":"passed","summary":"ok"}}
            with self.assertRaises(Exception):
                mod.execute(repo, json.dumps(public), json.dumps(owner))

    def test_cross_session_resume_revalidates_same_task(self):
        mod = self.load(); repo = make_repo(); task_ref, data = add_task(repo, "demo", branch="main", meta_workspace=False)
        facts = mod.task_facts(repo, task_ref, allow_missing_mappings=True); mod.write_recovery_mappings(repo, facts, task_ref)
        public = {"profile":"rebind_missing_session","mode":"standalone","task_ref":task_ref,"continuation_id":"session-2"}
        owner = {**public,"route":"rebind","lifecycle_generation":1,"resume_target":"phase-2","ai_review_gate":{"status":"passed","summary":"ok"}}
        fake = FakeModule(repo)
        with patch.object(mod, "active_module", return_value=fake), patch.object(mod, "session_id", return_value="codex_session_2"):
            output = mod.execute(repo, json.dumps(public), json.dumps(owner))
        self.assertEqual(output["task_ref"], task_ref)
        self.assertNotIn("session_id", output)
        self.assertNotIn("binding_id", output)

    def test_old_cleanup_receipt_generation_is_rejected_by_owner_boundary(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("cleanup_runtime", ROOT / ".trellis/guru-team/skills/packages/guru-cleanup-task-resources/runtime/invoke.py")
        cleanup = importlib.util.module_from_spec(spec); spec.loader.exec_module(cleanup)
        repo = make_repo(); archive = repo / ".trellis/tasks/archive/2026-09/demo"; archive.mkdir(parents=True)
        (archive / "task.json").write_text(json.dumps({"id":"demo","status":"completed","lifecycle_generation":0}) + "\n")
        public = {"archive_ref":".trellis/tasks/archive/2026-09/demo","lifecycle_generation":1}
        with self.assertRaises(Exception) as caught:
            cleanup.archive_generation(repo, public)
        self.assertIn("lifecycle_generation", str(caught.exception))

    def test_manual_recovery_without_base_provenance_succeeds_after_base_advance(self):
        mod = self.load()
        repo = make_repo()
        task_ref, data = add_task(repo, 'demo', branch='main', meta_workspace=False)
        data['meta'].pop('base_head')
        (repo / task_ref / 'task.json').write_text(json.dumps(data) + '\n')
        git(repo, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '--allow-empty', '-qm', 'base advances')
        public = {'profile': 'manual_recovery', 'mode': 'standalone', 'task_ref': task_ref, 'continuation_id': 'missing-base'}
        owner = {**public, 'route': 'manual_recovery', 'lifecycle_generation': 1, 'resume_target': 'phase-2', 'ai_review_gate': {'status': 'passed', 'summary': 'Fresh preflight required.'}}
        fake = FakeModule(repo)
        with patch.object(mod, 'active_module', return_value=fake), patch.object(fake, 'set_active_task', wraps=fake.set_active_task) as writer:
            output = mod.execute(repo, json.dumps(public), json.dumps(owner))
            writer.assert_called_once_with(task_ref, repo.resolve())
        self.assertEqual(output['exit_id'], 'session_manually_recovered')
        for category in ('tasks', 'workspaces'):
            mapping = json.loads((repo / f'.trellis/.runtime/guru-team/{category}/demo.json').read_text())
            self.assertNotIn('base_head', mapping)

    def test_recorded_base_provenance_does_not_reject_live_base_advance(self):
        mod = self.load()
        repo = make_repo()
        task_ref, data = add_task(repo, 'demo', branch='main', meta_workspace=False)
        git(repo, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '--allow-empty', '-qm', 'base advances')
        facts = mod.task_facts(repo, task_ref, allow_missing_mappings=True)
        self.assertEqual(facts['task_ref'], task_ref)

    def test_runtime_rejects_every_mismatched_profile_route_before_discovery(self):
        mod = self.load()
        public = {'mode': 'standalone', 'task_ref': '.trellis/tasks/demo', 'continuation_id': 'route-pairs'}
        for profile, expected in mod.PROFILE_ROUTES.items():
            for route in mod.PROFILE_ROUTES.values():
                if route == expected:
                    continue
                with self.subTest(profile=profile, route=route):
                    request = {**public, 'profile': profile}
                    owner = {**request, 'route': route, 'lifecycle_generation': 1, 'resume_target': 'phase-2', 'ai_review_gate': {'status': 'passed', 'summary': 'fixture'}}
                    # Independently exercise the runtime pair guard after schema validation.
                    with patch.object(mod, 'validate_json'), patch.object(mod, 'active_module') as discovery:
                        with self.assertRaises(mod.CommandError) as caught:
                            mod.execute(Path('.'), json.dumps(request), json.dumps(owner))
                        discovery.assert_not_called()
                    self.assertEqual(caught.exception.field_path, 'owner_result.route')

    def test_existing_legacy_mappings_without_base_provenance_survive_base_advance(self):
        mod = self.load()
        repo = make_repo()
        task_ref, data = add_task(repo, 'demo', branch='main', meta_workspace=False)
        facts = mod.task_facts(repo, task_ref, allow_missing_mappings=True)
        mod.write_recovery_mappings(repo, facts, task_ref)
        data['meta'].pop('base_head', None)
        (repo / task_ref / 'task.json').write_text(json.dumps(data) + '\n')
        for path in repo.glob('.trellis/.runtime/guru-team/tasks/demo.json'):
            payload = json.loads(path.read_text()); payload.pop('base_head', None); path.write_text(json.dumps(payload) + '\n')
        for path in repo.glob('.trellis/.runtime/guru-team/workspaces/demo.json'):
            payload = json.loads(path.read_text()); payload.pop('base_head', None); path.write_text(json.dumps(payload) + '\n')
        git(repo, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '--allow-empty', '-qm', 'base advances')
        facts = mod.task_facts(repo, task_ref, allow_missing_mappings=False)
        self.assertEqual(facts['generation'], 1)

    def test_metadata_base_branch_fallback_is_used_by_recovery_writer(self):
        mod = self.load()
        repo = make_repo()
        task_ref, data = add_task(repo, 'demo', branch='main', meta_workspace=False)
        data['base_branch'] = None
        data['meta']['base_branch'] = 'main'
        (repo / task_ref / 'task.json').write_text(json.dumps(data) + '\n')
        facts = mod.task_facts(repo, task_ref, allow_missing_mappings=True)
        self.assertEqual(facts['base_branch'], 'main')
        mod.write_recovery_mappings(repo, facts, task_ref)
        mapping = json.loads((repo / '.trellis/.runtime/guru-team/tasks/demo.json').read_text())
        self.assertEqual(mapping['base_branch'], 'main')

    def test_resume_or_rebind_cannot_replace_a_different_active_task(self):
        mod = self.load()
        for profile, route in (("resume_current_task", "resume"), ("rebind_missing_session", "rebind")):
            with self.subTest(profile=profile):
                repo = make_repo(); add_task(repo, 'a', branch='main', meta_workspace=False); add_task(repo, 'b', branch='main', meta_workspace=False)
                for ref in ('.trellis/tasks/a', '.trellis/tasks/b'):
                    facts = mod.task_facts(repo, ref, allow_missing_mappings=True); mod.write_recovery_mappings(repo, facts, ref)
                fake = FakeModule(repo); fake.set_active_task('.trellis/tasks/b', repo)
                public = {'profile': profile, 'mode': 'standalone', 'task_ref': '.trellis/tasks/a', 'continuation_id': f'{profile}-wrong-active'}
                owner = {**public, 'route': route, 'lifecycle_generation': 1, 'resume_target': 'phase-2', 'ai_review_gate': {'status': 'passed', 'summary': 'fixture'}}
                with patch.object(mod, 'active_module', return_value=fake), patch.object(mod, 'session_id', return_value='codex_fixture'):
                    with self.assertRaises(mod.CommandError) as caught:
                        mod.execute(repo, json.dumps(public), json.dumps(owner))
                self.assertEqual(caught.exception.field_path, 'current_task_ref')
                self.assertEqual(fake.active.task_path, '.trellis/tasks/b')
                self.assertEqual(fake.active.resolved_task_path, (repo / '.trellis/tasks/b').resolve())

    def test_existing_mapping_locator_disambiguates_main_and_external_worktree_task_artifacts(self):
        mod = self.load()
        repo = make_repo()
        workspace = repo.parent / ("task-worktree-mapped-" + next(tempfile._get_candidate_names()))
        subprocess.check_call(["git", "worktree", "add", "-qb", "codex/demo", str(workspace), "main"], cwd=repo)
        task_ref, data = add_task(repo, 'demo', branch='main', meta_workspace=False)
        external_ref, external_data = add_task(workspace, 'demo', branch='codex/demo')
        task_ref = external_ref
        mapping_dir = workspace / '.trellis/.runtime/guru-team/tasks'; mapping_dir.mkdir(parents=True)
        (mapping_dir / 'demo.json').write_text(json.dumps({'workspace_path': str(workspace.resolve()), 'task_artifact_dir': task_ref, 'repository_common_dir': str((repo/'.git').resolve()), 'base_head': external_data['meta']['base_head']}) + '\n')
        workspace_map = workspace / '.trellis/.runtime/guru-team/workspaces'; workspace_map.mkdir(parents=True, exist_ok=True)
        (workspace_map / 'demo.json').write_text(json.dumps({'workspace_path': str(workspace.resolve()), 'branch_name': 'codex/demo', 'repository_common_dir': str((repo/'.git').resolve()), 'base_head': external_data['meta']['base_head']}) + '\n')
        facts = mod.task_facts(repo, task_ref, allow_missing_mappings=True)
        self.assertEqual(facts['workspace'], workspace.resolve())
        self.assertEqual(facts['branch'], 'codex/demo')

    def test_date_prefixed_task_ref_uses_task_json_id_for_mapping_locator(self):
        mod = self.load(); repo = make_repo(); workspace = repo.parent / ("task-worktree-date-" + next(tempfile._get_candidate_names()))
        subprocess.check_call(["git", "worktree", "add", "-qb", "codex/demo", str(workspace), "main"], cwd=repo)
        task_ref = '.trellis/tasks/09-19-demo'; task_path = workspace / task_ref; task_path.mkdir(parents=True)
        base_head = git(workspace, 'rev-parse', 'refs/heads/main')
        task = {'id':'demo','status':'in_progress','branch':'codex/demo','base_branch':'main','worktree_path':None,'lifecycle_generation':1,'meta':{'worktree_path':str(workspace.resolve()),'base_head':base_head}}
        (task_path/'task.json').write_text(json.dumps(task)+'\n')
        mapping_root = workspace/'.trellis/.runtime/guru-team'; (mapping_root/'tasks').mkdir(parents=True); (mapping_root/'workspaces').mkdir(parents=True)
        common = str((repo/'.git').resolve())
        (mapping_root/'tasks/demo.json').write_text(json.dumps({'workspace_path':str(workspace.resolve()),'task_artifact_dir':task_ref,'repository_common_dir':common,'base_head':base_head})+'\n')
        (mapping_root/'workspaces/demo.json').write_text(json.dumps({'workspace_path':str(workspace.resolve()),'branch_name':'codex/demo','repository_common_dir':common,'base_head':base_head})+'\n')
        facts = mod.task_facts(repo, task_ref, allow_missing_mappings=True)
        self.assertEqual(facts['workspace'], workspace.resolve())

if __name__ == '__main__':
    unittest.main()
