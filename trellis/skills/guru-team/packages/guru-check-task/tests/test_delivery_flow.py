"""Actual public wrappers against an explicitly installed upstream candidate.

These are local integration checks; fixture semantic judgments do not claim AI
review, installed host continuation, or any remote publication success.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
SKILLS = PACKAGE.parents[1]
sys.path.insert(0, str(SKILLS))
from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
from runtime.task_lifecycle import BranchBindingStore, TaskLifecycleKey, inspect_repository


class DeliveryFlow(unittest.TestCase):
    def setUp(self):
        source = os.environ.get("TRELLIS_DELIVERY_API_COMMON")
        if not source:
            self.skipTest("Set TRELLIS_DELIVERY_API_COMMON to the reviewed public candidate common directory.")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        template = os.environ.get("GURU_DELIVERY_TEST_INSTALLATION")
        if template:
            shutil.copytree(template, self.repo, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns(".git", "__pycache__"))
            self.installed_skills_root = self.repo / ".trellis/guru-team/skills"
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Local Test")
        self.git("config", "user.email", "test@example.invalid")
        if template:
            # Reapply the complete preset in this new Git context. A copied
            # installation has no Git-common-dir Python pointer of its own.
            source_root = SKILLS.parents[2]
            applied = subprocess.run(["bash", str(source_root / "trellis/presets/guru-team/scripts/bash/apply.sh"),
                            "--repo", str(self.repo), "--platform", "codex", "--json"],
                           cwd=source_root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            summary = json.loads(applied.stdout) if applied.stdout.strip().startswith("{") else {"error": applied.stderr[-1000:]}
            self.assertEqual(0, applied.returncode, {"status": summary.get("status"),
                "conflicts": {k: summary.get(k, {}).get("conflicts") for k in ("skill_packages", "overlays")},
                "sidecars": {k: summary.get(k, {}).get("sidecars") for k in ("skill_packages", "overlays")}})
        common = self.repo / ".trellis/scripts/common"
        shutil.copytree(source, common, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__"))
        self.key = {"task_id": "flow-task", "lifecycle_generation": 0,
                    "delivery_id": "43134b50-2c8b-4d70-b114-218a735a82e2"}
        self.task_ref = ".trellis/tasks/flow-task"
        task_dir = self.repo / self.task_ref
        task_dir.mkdir(parents=True)
        owners = {role: "guru-test-" + role for role in
                  ("task_scope", "creation", "planning", "implementation", "check", "full_review", "readiness", "publication", "delivery", "completion", "closure")}
        owners["implementation"] = "guru-delivery-implementation-projection"
        declaration = {"task_schema": "2.0", "delivery_api": "1.0", "profiles": ["local_commit", "pull_request"], "owners": owners}
        if template:
            from runtime.delivery_projection.adapter import upstream_modules
            owners = upstream_modules(self.repo).runtime_contract.read_runtime_contract(self.repo / ".trellis/workflow.md")["owners"]
        else:
            (self.repo / ".trellis/workflow.md").write_text("[trellis-runtime-contract]\n" + json.dumps(declaration) + "\n[/trellis-runtime-contract]\n")
        (self.repo / ".gitignore").write_text(".trellis/.runtime/\n")
        (self.repo / "requirements.md").write_text("R1: keep clean candidate and review it.\n")
        (self.repo / "app.txt").write_text("old\n")
        # Public Task metadata, with no development status fields.
        record = {"schema_version": "2.0", "id": "flow-task", "name": "flow", "lifecycle_generation": 0,
                  "source": {"kind": "no_issue"}, "title": "flow", "description": "", "dev_type": None,
                  "scope": None, "package": None, "priority": "P2", "createdAt": "2026-10-12", "base_branch": "main",
                  "worktree_path": None, "children": [], "parent": None, "relatedFiles": [], "notes": "", "meta": {},
                  "accepted_scope": authority_ref(self.repo / "requirements.md", self.repo), "deliveries": [],
                  "completion_results": [], "closure_results": []}
        (task_dir / "task.json").write_text(json.dumps(record))
        self.git("add", ".")
        self.git("commit", "-qm", "base")
        self.git("switch", "-qc", "feat/flow")
        self.projection = DeliveryProjection(self.repo, self.task_ref)
        self.projection.apply({"api_version": "1.0", "operation": "create_delivery", "key": self.key,
            "owner_role": "creation", "owner_id": owners["creation"],
            "scope_ref": {"authority": record["accepted_scope"], "anchors": ["R1"]}, "profile": getattr(self, "delivery_profile", "local_commit")})
        plan = self.projection.planning_directory(self.key)
        plan.mkdir(parents=True, exist_ok=True)
        for name in ("prd.md", "design.md", "implement.md"):
            (plan / name).write_text("R1: current reviewed plan.\n")
        for name in ("implement.jsonl", "check.jsonl"):
            (plan / name).write_text("")
        d = self.projection.resolve(self.key)
        result = {"result_id": "planning:flow", "owner_role": "planning", "owner_id": owners["planning"], "outcome": "accepted",
                  "scope_ref": d["scope_ref"], "plan_ref": authority_ref(plan / "implement.md", self.repo), "candidate": None,
                  "predecessor_result_id": None, "obligations": [], "evidence": [record["accepted_scope"]]}
        self.projection.apply({"api_version": "1.0", "operation": "record_gate", "key": self.key,
            "owner_role": "planning", "owner_id": owners["planning"], "expected_phase": "planning", "result": result})
        (self.repo / "app.txt").write_text("feature\n")
        self.git("add", ".")
        self.git("commit", "-qm", "feature")
        self.head = self.git("rev-parse", "HEAD").strip()
        BranchBindingStore(inspect_repository(self.repo)).establish(TaskLifecycleKey("flow-task", 0), "feat/flow")
        self.projection.begin_check(self.key, self.projection.candidate(["app.txt"], head_ref=self.head, base_ref=self.git("rev-parse", "main").strip()))
        self.inputs = self.repo / ".trellis/.runtime/test-inputs"
        self.inputs.mkdir(parents=True)

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.repo, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout

    def write(self, name, value):
        path = self.inputs / name
        path.write_text(json.dumps(value))
        return str(path)

    def wrapper(self, skill, name, *args, success=True):
        package = getattr(self, "installed_skills_root", SKILLS) / "packages" / skill
        result = subprocess.run(["bash", str(package / "scripts" / name), "--root", str(self.repo), *map(str, args)],
                                capture_output=True, text=True)
        value = json.loads(result.stdout or result.stderr)
        self.assertEqual(result.returncode == 0, success, value)
        return value.get("result", value)

    def check(self):
        local = PACKAGE / "runtime"
        sys.path.insert(0, str(local))
        spec = importlib.util.spec_from_file_location("flow_check_common", local / "common.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        owner = json.loads((PACKAGE / "examples/phase2-check.json").read_text())
        owner.update(task_ref=self.task_ref, phase2_capture_commit=self.head,
                     reviewed_content_sha256=module.content_identity(self.repo), reviewed_paths=self.projection.resolve(self.key)["candidate"]["paths"])
        public = {"profile": "delivery_initial_check", "mode": "workflow", "task_ref": self.task_ref,
                  "delivery_key": self.key, "source_exit": "implementation_complete", "planning_accepted_result_id": "planning:flow"}
        return self.wrapper("guru-check-task", "invoke.sh", "--input", self.write("check.json", public),
                            "--owner-result", self.write("check-owner.json", owner))

    def test_fresh_check_metadata_does_not_force_second_commit_and_full_review(self):
        checked = self.check()
        self.assertEqual("passed", checked["exit_id"])
        self.assertIn("task.json", self.git("status", "--porcelain"))
        public = {"profile": "delivery_committed_reentry", "mode": "workflow", "task_ref": self.task_ref,
                  "delivery_key": self.key, "check_result_id": checked["check_result_id"]}
        owner = {"status": "passed", "summary": "Retain existing committed candidate.", "evidence": ["Current candidate and full range reviewed."]}
        committed = self.wrapper("guru-create-task-commit", "invoke.sh", "--input", self.write("commit.json", public),
                                 "--owner-result", self.write("commit-owner.json", owner))
        self.assertEqual(self.head, self.git("rev-parse", "HEAD").strip())
        self.assertEqual("committed", committed["exit_id"])
        p = SKILLS / "packages/guru-review-branch"
        fixture = json.loads((p / "examples/review-gate.json").read_text())
        auth = {key: fixture[key] for key in ("candidate_classifications", "semantic_review", "verification_evidence", "delivery_review")}
        auth["semantic_review"]["qualified_findings"] = []
        public = {"profile": "delivery_branch_review", "mode": "workflow", "task_ref": self.task_ref,
                  "delivery_key": self.key, "check_result_id": checked["check_result_id"], "base_ref": self.projection.content_base(self.key),
                  "branch_review_commit": self.head, "review_intent": "initial_review"}
        self.wrapper("guru-review-branch", "review-branch.sh", "--task", self.task_ref,
                     "--skill-input", self.write("review.json", public), "--semantic-review-file", self.write("review-owner.json", auth),
                     "--typed-exit", "passed")
        reviewed = self.wrapper("guru-review-branch", "invoke.sh", "--input", self.write("review.json", public))
        self.assertEqual("passed", reviewed["exit_id"])
        self.assertEqual(reviewed, self.wrapper("guru-review-branch", "invoke.sh", "--input", self.write("review.json", public)))
        self.assertEqual(self.head, self.git("rev-parse", "HEAD").strip())

    def test_normal_candidate_change_requires_check_reentry(self):
        checked = self.check()
        (self.repo / "app.txt").write_text("new legitimate work\n")
        public = {"profile": "delivery_committed_reentry", "mode": "workflow", "task_ref": self.task_ref,
                  "delivery_key": self.key, "check_result_id": checked["check_result_id"]}
        value = self.wrapper("guru-create-task-commit", "invoke.sh", "--input", self.write("commit.json", public),
                             "--owner-result", self.write("owner.json", {"status": "passed", "summary": "review", "evidence": ["candidate"]}), success=False)
        self.assertNotEqual("committed", value.get("exit_id"))



    def full_review(self, checked):
        p = SKILLS / 'packages/guru-review-branch'
        fixture = json.loads((p / 'examples/review-gate.json').read_text())
        auth = {key: fixture[key] for key in ('candidate_classifications', 'semantic_review', 'verification_evidence', 'delivery_review')}
        auth['semantic_review']['qualified_findings'] = []
        public = {'profile': 'delivery_branch_review', 'mode': 'workflow', 'task_ref': self.task_ref,
                  'delivery_key': self.key, 'check_result_id': checked['check_result_id'], 'base_ref': self.projection.content_base(self.key),
                  'branch_review_commit': self.head, 'review_intent': 'initial_review'}
        self.wrapper('guru-review-branch', 'review-branch.sh', '--task', self.task_ref,
                     '--skill-input', self.write('review.json', public), '--semantic-review-file', self.write('review-owner.json', auth), '--typed-exit', 'passed')
        checkpoint_result = self.wrapper('guru-review-branch', 'check-review-gate.sh', '--task', self.task_ref, '--delivery-key', json.dumps(self.key))
        self.assertFalse(checkpoint_result['formal_exit'])
        return self.wrapper('guru-review-branch', 'invoke.sh', '--input', self.write('review.json', public))

    def readiness(self, reviewed):
        p = SKILLS / 'packages/guru-review-task-delivery'
        semantic = json.loads((p / 'examples/semantic-ready.json').read_text())
        semantic['pr_payload']['body'] = semantic['pr_payload']['body'].replace('Refs #435', '')
        public = {'profile': 'delivery_delivery_review', 'mode': 'workflow', 'task_ref': self.task_ref,
                  'delivery_key': self.key, 'full_review_result_id': reviewed['full_review_result_id'], 'branch_review_commit': self.head}
        return self.wrapper('guru-review-task-delivery', 'invoke.sh', '--input', self.write('readiness.json', public), '--semantic-result', self.write('readiness-owner.json', semantic))

    def test_readiness_and_no_delivery_required_completion(self):
        reviewed = self.full_review(self.check())
        ready = self.readiness(reviewed)
        self.assertEqual('ready', ready['exit_id'])
        self.assertEqual('publishing', self.projection.resolve(self.key)['phase'])
        # Actual local commit delivery is an explicit supported public profile.
        candidate = self.projection.resolve(self.key)['candidate']
        self.projection.apply({'api_version': '1.0', 'operation': 'record_delivery', 'key': self.key,
            'owner_role': 'delivery', 'owner_id': 'guru-test-delivery', 'expected_phase': 'publishing',
            'result': {'result_id': 'delivery:flow', 'owner_id': 'guru-test-delivery', 'evidence': [authority_ref(self.repo / 'app.txt', self.repo)],
                       'profile': 'local_commit', 'candidate': candidate, 'commit': self.head}})
        public = {'profile': 'delivery_completion', 'mode': 'workflow', 'task_ref': self.task_ref,
                  'task_key': {'task_id': self.key['task_id'], 'lifecycle_generation': 0}}
        semantic = {'profile': public['profile'], 'mode': public['mode'], 'reviewed_task_key': public['task_key'],
                    'reviewed_scope': self.projection.read_record()['accepted_scope'], 'reviewed_delivery_result_ids': ['delivery:flow'],
                    'evidence': [authority_ref(self.repo / 'app.txt', self.repo)], 'remaining_work_refs': [], 'result_id': 'completion:flow',
                    'route': {'typed_exit': 'completed'}}
        completed = self.wrapper('guru-review-task-completion', 'invoke.sh', '--input', self.write('completion.json', public), '--semantic-result', self.write('completion-owner.json', semantic))
        self.assertEqual('completed', completed['exit_id'])
        self.assertEqual(completed, self.wrapper('guru-review-task-completion', 'invoke.sh', '--input', self.write('completion.json', public), '--semantic-result', self.write('completion-owner.json', semantic)))
        self.assertNotIn('status', self.projection.read_record())

    def test_scope_withdrawal_and_stop_stdout_recovery(self):
        public = {'profile': 'delivery_scope_withdrawal', 'mode': 'workflow', 'task_ref': self.task_ref, 'delivery_key': self.key}
        reason = authority_ref(self.repo / 'requirements.md', self.repo)
        semantic = {'reviewed_delivery_key': self.key, 'result_id': 'stop:flow', 'reason': reason, 'scope_decision': reason, 'evidence': [reason]}
        stopped = self.wrapper('guru-check-task', 'invoke.sh', '--input', self.write('withdrawal.json', public), '--owner-result', self.write('withdrawal-owner.json', semantic))
        self.assertEqual('delivery_stopped', stopped['exit_id'])
        self.assertEqual('stopped', self.projection.resolve(self.key)['phase'])
        self.assertEqual(stopped, self.wrapper('guru-check-task', 'invoke.sh', '--input', self.write('withdrawal.json', public), '--owner-result', self.write('withdrawal-owner.json', semantic)))
        self.assertEqual(self.head, self.git('rev-parse', 'HEAD').strip())

    def test_withdrawal_at_each_later_owner_recovers_without_git_mutation(self):
        for skill, stage, flag in (
            ('guru-review-branch', 'review', '--owner-result'),
            ('guru-review-task-delivery', 'review', '--semantic-result'),
            ('guru-publish-task-delivery', 'ready', '--review-input'),
            ('guru-merge-task-delivery', 'ready', '--review-input'),
        ):
            with self.subTest(skill=skill):
                fixture = DeliveryFlow(); fixture.setUp()
                try:
                    checked = fixture.check()
                    if stage == 'ready': fixture.readiness(fixture.full_review(checked))
                    public = {'profile':'delivery_scope_withdrawal','mode':'workflow','task_ref':fixture.task_ref,'delivery_key':fixture.key}
                    reason = authority_ref(fixture.repo/'requirements.md', fixture.repo)
                    semantic = {'reviewed_delivery_key':fixture.key,'result_id':'stop:'+skill,'reason':reason,'scope_decision':reason,'evidence':[reason]}
                    before = fixture.git('rev-parse','HEAD')
                    args = ('--input',fixture.write('withdrawal.json',public),flag,fixture.write('withdrawal-owner.json',semantic))
                    stopped = fixture.wrapper(skill,'invoke.sh',*args)
                    self.assertEqual('delivery_stopped',stopped['exit_id'])
                    self.assertEqual(stopped,fixture.wrapper(skill,'invoke.sh',*args))
                    self.assertEqual(before,fixture.git('rev-parse','HEAD'))
                finally: fixture.doCleanups()

    def test_readiness_refresh_requires_original_publication_rework(self):
        ready = self.readiness(self.full_review(self.check()))
        package, owner = self.load_owner('guru-publish-task-delivery')
        stale = {'exit_id':'review_stale','task_ref':self.task_ref,'delivery_key':self.key,'stale_reason':'metadata_changed'}
        self.assertEqual(stale,owner.project_review_stale(self.repo,stale))
        self.assertEqual('reviewing',self.projection.resolve(self.key)['phase'])
        self.assertIsNone(self.projection.resolve(self.key)['results']['readiness'])
        p = SKILLS/'packages/guru-review-task-delivery'
        semantic=json.loads((p/'examples/semantic-ready.json').read_text())
        semantic['pr_payload']['body']=semantic['pr_payload']['body'].replace('Refs #435','')
        public={'profile':'delivery_readiness_refresh','mode':'workflow','task_ref':self.task_ref,'delivery_key':self.key,'reentry_reason':'metadata_changed'}
        output=self.wrapper('guru-review-task-delivery','invoke.sh','--input',self.write('refresh.json',public),'--semantic-result',self.write('refresh-owner.json',semantic))
        self.assertEqual('ready',output['exit_id']);self.assertEqual('publishing',self.projection.resolve(self.key)['phase'])

    def test_resolved_tree_check_projects_reconcile_without_committed_gate(self):
        from runtime.delivery_projection.gates import rework
        # Finish committing the initial public metadata before a normal Git merge.
        self.git('add','.')
        self.git('commit','-qm','bind current delivery metadata')
        self.head=self.git('rev-parse','HEAD').strip()
        old_base=self.git('rev-parse','main').strip()
        self.git('switch','main')
        (self.repo/'app.txt').write_text('evolved base\n')
        self.git('add','app.txt');self.git('commit','-qm','base evolution')
        new_base=self.git('rev-parse','HEAD').strip()
        self.git('switch','feat/flow')
        result=subprocess.run(['git','merge','--no-commit','main'],cwd=self.repo,capture_output=True,text=True)
        self.assertNotEqual(0,result.returncode)
        (self.repo/'app.txt').write_text('feature with evolved base\n');self.git('add','app.txt')
        rework(self.projection,self.key,'check','implementation',authority_ref(self.repo/'requirements.md',self.repo),['check','full_review','readiness'])
        self.projection.begin_check(self.key,self.projection.candidate(['app.txt'],head_ref=self.head,base_ref=old_base))
        # Upstream state writes are metadata, keep the resolved index exact.
        self.git('add',self.task_ref+'/task.json')
        local=PACKAGE/'runtime';sys.path.insert(0,str(local))
        spec=importlib.util.spec_from_file_location('resolved_check_common',local/'common.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        owner=json.loads((PACKAGE/'examples/phase2-check.json').read_text())
        owner.update(task_ref=self.task_ref,phase2_capture_commit=self.head,reviewed_content_sha256=module.content_identity(self.repo),reviewed_paths=['app.txt'],typed_exit='resolved_reconciliation_passed',consumer={'kind':'skill','id':'guru-reconcile-task-base'})
        public={'profile':'delivery_resolved_reconciliation','mode':'workflow','task_ref':self.task_ref,'delivery_key':self.key,'source_exit':'resolved_tree_ready','planning_accepted_result_id':'planning:flow'}
        checked=self.wrapper('guru-check-task','invoke.sh','--input',self.write('resolved.json',public),'--owner-result',self.write('resolved-owner.json',owner))
        self.assertEqual('resolved_reconciliation_passed',checked['exit_id']);self.assertIsNone(self.projection.resolve(self.key)['results']['check'])
        authoring={'profile':'delivery_resolved_candidate','mode':'workflow','branch':'feat/flow','selected_base_ref':new_base,'old_base_head':old_base,'new_base_head':new_base,'merge_head':new_base,'stage0_tree':self.git('write-tree').strip(),'index_tree_sha256':self.load_owner('guru-reconcile-task-base','common.py')[1].index_tree_digest(self.repo),'parent_order':[self.head,new_base],'commit_message':'整合已审查基线','resume_target':'branch_review'}
        projected=self.wrapper('guru-check-task','project-resolved-reconciliation.sh','--input',self.write('resolved.json',public),'--owner-result',self.write('resolved-owner.json',owner),'--authoring',self.write('resolved-authoring.json',authoring))
        self.assertEqual('delivery_resolved_candidate',projected['profile']);self.assertEqual(self.key,projected['delivery_key']);self.assertEqual(self.head,projected['phase2_commit_anchor'])
        self.assertEqual(self.head,self.git('rev-parse','HEAD').strip())
        self.assertEqual('checking', self.projection.resolve(self.key)['phase'])
        reconciled = self.wrapper('guru-reconcile-task-base', 'execute-resolved-base-reconciliation.sh',
            '--input', self.write('resolved-executor.json', projected))
        self.assertEqual('committed', reconciled['status'])
        self.assertEqual('checking', self.projection.resolve(self.key)['phase'])
        self.assertIsNone(self.projection.resolve(self.key)['results']['check'])
        rework(self.projection, self.key, 'check', 'implementation',
               authority_ref(self.repo / 'requirements.md', self.repo), ['readiness'])
        self.head = reconciled['reconciled_task_head']
        self.projection.begin_check(self.key, self.projection.candidate(
            ['app.txt'], head_ref=self.head, base_ref=old_base))
        refreshed = self.check()
        self.assertEqual('passed', refreshed['exit_id'])
        self.assertEqual('reviewing', self.projection.resolve(self.key)['phase'])
        self.assertEqual(self.head, self.projection.resolve(self.key)['results']['check']['candidate']['head_ref'])

    def test_dirty_exact_commit_and_lost_stdout_preserve_unrelated_paths(self):
        from runtime.delivery_projection.gates import rework
        rework(self.projection, self.key, 'check', 'implementation', authority_ref(self.repo / 'requirements.md', self.repo), ['check', 'full_review', 'readiness'])
        (self.repo / 'app.txt').write_text('feature two\n')
        (self.repo / 'unrelated.txt').write_text('parallel work\n')
        self.projection.begin_check(self.key, self.projection.candidate(['app.txt'], head_ref=self.head, base_ref=self.projection.content_base(self.key)))
        # The full Check explicitly reviews app + classifies unrelated work.
        p = PACKAGE / 'runtime'
        sys.path.insert(0, str(p))
        spec = importlib.util.spec_from_file_location('dirty_flow_check', p / 'common.py')
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        owner = json.loads((PACKAGE / 'examples/phase2-check.json').read_text())
        owner.update(task_ref=self.task_ref, phase2_capture_commit=self.head, reviewed_content_sha256=module.content_identity(self.repo), reviewed_paths=['app.txt', 'unrelated.txt'])
        public_check = {'profile':'delivery_initial_check','mode':'workflow','task_ref':self.task_ref,'delivery_key':self.key,'source_exit':'implementation_complete','planning_accepted_result_id':'planning:flow'}
        checked = self.wrapper('guru-check-task','invoke.sh','--input',self.write('dirty-check.json',public_check),'--owner-result',self.write('dirty-check-owner.json',owner))
        public = {'profile':'delivery_initial_commit','mode':'workflow','task_ref':self.task_ref,'delivery_key':self.key,'source_exit':'passed','check_result_id':checked['check_result_id']}
        commit_package = SKILLS / 'packages/guru-create-task-commit'
        message = json.loads((commit_package / 'examples/task-commit-candidate.json').read_text())['message']
        authoring = {'message': message, 'ai_review': {'status':'passed','summary':'Exact app increment; preserve parallel work.','evidence':['Current complete Check and candidate diff.']},
                     'path_classifications':[{'path':path,'category':'task-reviewed' if path=='app.txt' else 'unrelated-preserved','reason':'Exact reviewed scope.' if path=='app.txt' else 'Preserve parallel work or deterministic metadata.','coverage_source':checked['check_result_id']} for path in ('app.txt','unrelated.txt',self.task_ref+'/task.json')]}
        prepared = self.wrapper('guru-create-task-commit','prepare-task-commit.sh','--input',self.write('dirty-commit.json',public),'--candidate-json',self.write('dirty-commit-owner.json',authoring))
        committed = self.wrapper('guru-create-task-commit','invoke.sh','--candidate-artifact',prepared['candidate_artifact'])
        self.assertEqual('committed',committed['exit_id']);self.assertNotEqual(self.head,committed['branch_review_commit'])
        self.assertEqual('app.txt',self.git('diff','--name-only',self.head,committed['branch_review_commit']).strip())
        self.assertTrue((self.repo/'unrelated.txt').is_file())
        self.assertEqual(committed,self.wrapper('guru-create-task-commit','invoke.sh','--candidate-artifact',prepared['candidate_artifact']))

    def provider_response(self, *, body, merged=False):
        from unittest.mock import patch
        actual_run = subprocess.run
        def response(command, *args, **kwargs):
            if command[:3] == ['gh','pr','view']:
                actual={'number':9,'headRefOid':self.head,'baseRefName':'main','state':'MERGED' if merged else 'OPEN','mergeCommit':{'oid':'f'*40} if merged else None,'url':'https://github.com/example/repo/pull/9','body':body}
                return subprocess.CompletedProcess(command,0,json.dumps(actual),'')
            return actual_run(command,*args,**kwargs)
        return patch('subprocess.run',side_effect=response)

    def load_owner(self, skill, filename='owner.py'):
        package = SKILLS / 'packages' / skill
        sys.path.insert(0, str(package / 'runtime'))
        spec = importlib.util.spec_from_file_location('flow_' + skill.replace('-', '_'), package / 'runtime' / filename)
        owner = importlib.util.module_from_spec(spec); spec.loader.exec_module(owner)
        return package, owner

    def test_remote_publication_fact_recovers_before_current_readiness(self):
        from unittest.mock import patch
        from runtime.delivery_projection.gates import rework
        package, owner = self.load_owner('guru-publish-task-delivery')
        ready = self.readiness(self.full_review(self.check()))
        # Create the supported PR-profile Delivery via public creation, not record tampering.
        key = {**self.key, 'delivery_id':'43134b50-2c8b-4d70-b114-218a735a82e3'}
        record = self.projection.read_record()
        self.projection.apply({'api_version':'1.0','operation':'create_delivery','key':key,'owner_role':'creation','owner_id':'guru-test-creation','scope_ref':{'authority':record['accepted_scope'],'anchors':['R1']},'profile':'pull_request'})
        selected = self.projection.resolve(key)
        source = {'profile':'delivery_review_ready','mode':'workflow','task_ref':self.task_ref,'delivery_key':key,'readiness_result_id':'readiness:historical','reviewed_head':self.head,'pr_title':'交付当前结果','pr_body':'当前验证事实','remaining_work_state':'complete'}
        transaction = {'transaction_ref':'publication-tx:local','input':source,'bound_pr':{'number':9},'reviewed_head':self.head,'public_candidate':self.projection.resolve(self.key)['candidate'],'repo_ref':'example/repo','base_branch':'main'}
        pr = {'number':9,'state':'OPEN','is_draft':False,'head_sha':self.head,'title':source['pr_title'],'body':source['pr_body']}
        with self.provider_response(body=source['pr_body']), patch.object(owner,'read_pr',return_value=pr):
            result = owner.ready_output(self.repo,transaction)
            repeated = owner.ready_output(self.repo,transaction)
        self.assertEqual('review_stale',result['exit_id'])
        self.assertEqual(result,repeated)
        self.assertEqual('planning',self.projection.resolve(key)['phase'])
        self.assertIsNone(self.projection.resolve(key)['results']['readiness'])
        self.assertEqual('publication:publication-tx:local',self.projection.resolve(key)['publication_result']['result_id'])

    def test_merged_fact_projection_failure_retries_without_remote_merge(self):
        from unittest.mock import patch
        from runtime.task_lifecycle import LifecycleContractError
        package, owner = self.load_owner('guru-merge-task-delivery')
        history = self.projection.read_record()
        key = {**self.key,'delivery_id':'43134b50-2c8b-4d70-b114-218a735a82e3'}
        self.projection.apply({'api_version':'1.0','operation':'create_delivery','key':key,'owner_role':'creation','owner_id':'guru-test-creation','scope_ref':{'authority':history['accepted_scope'],'anchors':['R1']},'profile':'pull_request'})
        candidate = self.projection.resolve(self.key)['candidate']
        public = {'profile':'delivery_ready_for_merge','mode':'workflow','task_ref':self.task_ref,'delivery_key':key,'publication_result_id':'publication:flow','repo_ref':'example/repo','pr_number':9,'expected_head_sha':self.head,'publication_body_sha256':__import__('hashlib').sha256(b'Refs #9').hexdigest()}
        with self.provider_response(body='Refs #9'):
            self.projection.apply({'api_version':'1.0','operation':'record_publication','key':key,'owner_role':'publication','owner_id':'guru-test-publication','expected_phase':'planning','historical_success':True,'result':{'result_id':'publication:flow','owner_id':'guru-test-publication','evidence':[history['accepted_scope']],'profile':'pull_request','candidate':candidate,'repo_ref':'example/repo','pr_number':9,'reviewed_head':self.head,'target_ref':'main','publication_ref':{'locator':'https://github.com/example/repo/pull/9','revision':'sha256:'+__import__('hashlib').sha256(b'Refs #9').hexdigest()}}})
        review = {'dimensions':[{'id':name,'status':'passed','summary':'Actual current dimension reviewed.'} for name in owner.DIMENSIONS], 'route':{'typed_exit':'delivered','merge_method':'merge','merge_message':{'subject':'chore(merge): 合并当前结果','body':'交付本切片。\n\n'+'\n'.join(owner.expected_trailers('flow-task',self.head,key))}}}
        merge = 'f'*40;base = 'e'*40;message=review['route']['merge_message']
        facts={'task':{'task_ref':self.task_ref,'stable_task_id':'flow-task','lifecycle_generation':0,'branch':'feat/flow','base_branch':'main','head_sha':self.head},'pr':{'number':9,'url':'https://github.com/example/repo/pull/9','state':'MERGED','is_draft':False,'head_sha':self.head,'head_branch':'feat/flow','base_branch':'main','body':'Refs #9','merged_at':'2026-10-12T01:00:00Z','merge_commit_sha':merge,'mergeable':'MERGEABLE','merge_state_status':'CLEAN','review_decision':'APPROVED','checks':[]},'repository_policy':{'allow_merge_commit':True,'allow_squash_merge':True,'allow_rebase_merge':True},'base_ref':{'name':'main','head_sha':merge},'merge_commit':{'sha':merge,'message':message['subject']+'\n\n'+message['body'],'parents':[base,self.head]},'objective_blockers':[]}
        facts['facts_sha256']=owner.digest(facts)
        import argparse
        args=argparse.Namespace(root=str(self.repo),input=self.write('merge.json',public),review_input=self.write('merge-review.json',review))
        original=DeliveryProjection.apply
        def fail_projection(projection, operation):
            if operation['operation']=='record_delivery':raise LifecycleContractError('delivery_projection_failed','delivery','Retry public projection.')
            return original(projection,operation)
        with patch.object(owner,'live_facts',return_value=facts),patch.object(owner,'run_merge') as remote,patch.object(DeliveryProjection,'apply',fail_projection):
            with self.assertRaises(owner.CommandError):owner.cmd_invoke(package,args)
            remote.assert_not_called()
        with self.provider_response(body='Refs #9', merged=True), patch.object(owner,'live_facts',return_value=facts),patch.object(owner,'run_merge') as remote:
            delivered=owner.cmd_invoke(package,args); repeated=owner.cmd_invoke(package,args)
            remote.assert_not_called()
        self.assertEqual(delivered,repeated);self.assertEqual({'exit_id','task_ref','task_key'},set(delivered))
        self.assertEqual('delivered',self.projection.resolve(key)['phase'])
        self.assertIsNone(self.projection.resolve(key)['results']['readiness'])

    def test_no_mutation_closure_records_public_result_and_recovers(self):
        self.test_readiness_and_no_delivery_required_completion()
        public={'profile':'completion_approved','source_exit':'completed','mode':'workflow','completion_result':{'task_id':'flow-task','lifecycle_generation':0,'result_id':'completion:flow'},'source':{'kind':'no_issue'},'accepted_scope_identity':'scope:flow','delivery_target':{'repo_ref':'example/repo','branch_ref':'main'},'binding_ref':{'task_id':'flow-task','lifecycle_generation':0,'binding_revision':0},'content_head':self.head,'evidence_slots':{'completion':'completion:flow'},'action_set':[]}
        semantic={'profile':'completion_approved','mode':'workflow','reviewed_action_set':[],'route':{'typed_exit':'apply'}}
        closed=self.wrapper('guru-complete-task-closure','invoke.sh','--input',self.write('closure.json',public),'--semantic-result',self.write('closure-owner.json',semantic))
        self.assertEqual('no_mutation',closed['exit_id']);self.assertEqual(1,len(self.projection.read_record()['closure_results']))
        self.assertEqual(closed,self.wrapper('guru-complete-task-closure','invoke.sh','--input',self.write('closure.json',public),'--semantic-result',self.write('closure-owner.json',semantic)))
        self.assertEqual(1,len(self.projection.read_record()['closure_results']))

    def test_active_replanning_stays_same_delivery_and_other_plan_survives(self):
        from runtime.delivery_projection.gates import rework
        checked=self.check()
        other={**self.key,'delivery_id':'43134b50-2c8b-4d70-b114-218a735a82e3'}
        record=self.projection.read_record()
        self.projection.apply({'api_version':'1.0','operation':'create_delivery','key':other,'owner_role':'creation','owner_id':'guru-test-creation','scope_ref':{'authority':record['accepted_scope'],'anchors':['R2']},'profile':'local_commit'})
        other_plan=self.projection.planning_directory(other);other_plan.mkdir(parents=True,exist_ok=True);(other_plan/'prd.md').write_text('R2 independent plan.\n')
        first_plan=self.projection.planning_directory(self.key)
        rework(self.projection,self.key,'full_review','planning',authority_ref(self.repo/'requirements.md',self.repo),['planning','check','full_review','readiness'])
        (first_plan/'implement.md').write_text('R1 revised plan.\n')
        selected=self.projection.resolve(self.key)
        self.assertEqual('planning',selected['phase']);self.assertEqual(self.key['delivery_id'],selected['id'])
        self.assertIsNone(selected['results']['check']);self.assertEqual(0,self.projection.read_record()['lifecycle_generation'])
        self.assertEqual('R2 independent plan.\n',(other_plan/'prd.md').read_text())
        self.assertNotEqual(first_plan,other_plan)

    def test_remaining_scope_does_not_complete_from_known_deliveries(self):
        self.test_scope_withdrawal_and_stop_stdout_recovery()
        public={'profile':'delivery_completion','mode':'workflow','task_ref':self.task_ref,'task_key':{'task_id':self.key['task_id'],'lifecycle_generation':0}}
        semantic={'profile':public['profile'],'mode':'workflow','reviewed_task_key':public['task_key'],'reviewed_scope':self.projection.read_record()['accepted_scope'],'reviewed_delivery_result_ids':[],'evidence':[authority_ref(self.repo/'requirements.md',self.repo)],'remaining_work_refs':['scope:R2'],'result_id':'completion:pending','route':{'typed_exit':'remaining_work','reason':{'reason_code':'unallocated_scope','reason_refs':['scope:R2']}}}
        result=self.wrapper('guru-review-task-completion','invoke.sh','--input',self.write('remaining.json',public),'--semantic-result',self.write('remaining-owner.json',semantic))
        self.assertEqual('remaining_work',result['exit_id']);self.assertEqual([],self.projection.read_record()['completion_results'])

    def test_finish_archive_preserves_public_aggregate_without_task_status(self):
        self.test_no_mutation_closure_records_public_result_and_recovers()
        package,owner=self.load_owner('guru-finish-task','invoke.py')
        schema=self.repo/'.trellis/guru-team/schemas';schema.mkdir(parents=True)
        shutil.copyfile(SKILLS.parent.parent/'workflows/guru-team/schemas/finish-summary.schema.json',schema/'finish-summary.schema.json')
        archive='.trellis/tasks/archive/2026-10/flow-task'
        public={'task_id':'flow-task','task_ref':self.task_ref,'closure_result':{'task_id':'flow-task','lifecycle_generation':0,'result_id':self.projection.read_record()['closure_results'][0]['result_id']}}
        before=self.projection.read_record()
        owner.project_archive(self.repo,public,Path(self.task_ref),archive,Path(archive),{'kind':'no_issue'})
        after=json.loads((self.repo/archive/'task.json').read_text())
        self.assertEqual(before,after);self.assertNotIn('status',after);self.assertNotIn('completedAt',after)
        self.assertTrue((self.repo/archive/'finish-summary.json').is_file())
        self.assertTrue((self.repo/archive/'deliveries'/self.key['delivery_id']/'prd.md').is_file())


    def test_bounded_continuity_does_not_fabricate_full_review_for_new_candidate(self):
        from runtime.delivery_projection.gates import rework
        reviewed = self.full_review(self.check())
        prior_head = self.head
        old_base = self.git("rev-parse", "main").strip()
        self.git("add", self.task_ref); self.git("commit", "-qm", "persist actual review facts")
        self.git("switch", "main")
        (self.repo / "base-only.txt").write_text("independent base change\n")
        self.git("add", "base-only.txt"); self.git("commit", "-qm", "advance base")
        new_base = self.git("rev-parse", "HEAD").strip()
        self.git("switch", "feat/flow"); self.git("merge", "--no-ff", "-m", "reconcile actual base", "main")
        self.head = self.git("rev-parse", "HEAD").strip()
        rework(self.projection,self.key,"full_review","implementation",authority_ref(self.repo/"requirements.md",self.repo),["check","full_review","readiness"])
        self.projection.begin_check(self.key,self.projection.candidate(["app.txt"],head_ref=self.head,base_ref=self.projection.content_base(self.key)))
        checked = self.check()
        package = SKILLS / "packages/guru-review-branch"
        spec = importlib.util.spec_from_file_location("continuity_tree_reader",package/"runtime/common.py")
        common = importlib.util.module_from_spec(spec); spec.loader.exec_module(common)
        public = {"profile":"delivery_base_continuity","mode":"workflow","task_ref":self.task_ref,"delivery_key":self.key,"check_result_id":checked["check_result_id"],"task_head":self.head,"branch_review_commit":prior_head,"old_base_head":old_base,"new_base_head":new_base,"candidate_tree_sha256":common.tree_identity(self.repo,self.head),"relevant_paths":["base-only.txt"],"resume_target":"publication_review","review_intent":"base_continuity"}
        fixture = json.loads((package/"examples/review-gate.json").read_text())
        auth = {key:fixture[key] for key in ("candidate_classifications","semantic_review","verification_evidence","delivery_review")}
        auth["semantic_review"]["qualified_findings"] = []
        auth["semantic_review"]["ai_review_gate"]["status"] = "continuity_passed"
        args = ("--task",self.task_ref,"--skill-input",self.write("continuity-input.json",public),"--semantic-review-file",self.write("continuity-owner.json",auth),"--typed-exit","continuity_passed")
        self.wrapper("guru-review-branch","review-branch.sh",*args)
        bounded = self.wrapper("guru-review-branch","invoke.sh","--input",self.write("continuity-input.json",public))
        self.assertEqual("continuity_passed",bounded["exit_id"])
        self.assertIsNone(self.projection.resolve(self.key)["results"]["full_review"])
        readiness_package = SKILLS/"packages/guru-review-task-delivery"
        semantic = json.loads((readiness_package/"examples/semantic-ready.json").read_text())
        semantic["pr_payload"]["body"] = semantic["pr_payload"]["body"].replace("Refs #435","")
        refresh = {"profile":"delivery_readiness_refresh","mode":"workflow","task_ref":self.task_ref,"delivery_key":self.key,"reentry_reason":"bounded_continuity_requires_current_full_review"}
        rejected = self.wrapper("guru-review-task-delivery","invoke.sh","--input",self.write("readiness-refresh.json",refresh),"--semantic-result",self.write("readiness-refresh-owner.json",semantic),success=False)
        self.assertEqual("stale_identity",rejected["code"])
        self.assertEqual("ready",self.readiness(self.full_review(checked))["exit_id"])
        self.assertEqual(self.head,self.git("rev-parse","HEAD").strip())

    def test_current_check_and_full_review_reject_normal_checkout_context_switch(self):
        checked = self.check()
        self.git("switch", "-qc", "feat/other-context")
        package = SKILLS / "packages/guru-review-branch"
        public = {"profile":"delivery_branch_review","mode":"workflow","task_ref":self.task_ref,"delivery_key":self.key,"check_result_id":checked["check_result_id"],"base_ref":self.projection.content_base(self.key),"branch_review_commit":self.head,"review_intent":"initial_review"}
        fixture = json.loads((package/"examples/review-gate.json").read_text())
        auth = {key:fixture[key] for key in ("candidate_classifications","semantic_review","verification_evidence","delivery_review")}
        auth["semantic_review"]["qualified_findings"] = []
        blocked = self.wrapper("guru-review-branch","review-branch.sh","--task",self.task_ref,"--skill-input",self.write("review-no-binding.json",public),"--semantic-review-file",self.write("review-no-binding-owner.json",auth),"--typed-exit","passed",success=False)
        self.assertEqual("stale_identity",blocked["code"])
        check_public = {"profile":"delivery_initial_check","mode":"workflow","task_ref":self.task_ref,"delivery_key":self.key,"source_exit":"implementation_complete","planning_accepted_result_id":"planning:flow"}
        blocked = self.wrapper("guru-check-task","invoke.sh","--input",self.write("check-no-binding.json",check_public),"--owner-result",str(self.inputs/"check-owner.json"),success=False)
        self.assertEqual("stale_identity",blocked["code"])
        self.assertEqual(self.head,self.git("rev-parse","HEAD").strip())
        self.assertIsNone(self.projection.resolve(self.key)["results"]["full_review"])

if __name__ == "__main__":
    unittest.main()
