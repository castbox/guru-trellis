"""Actual committed candidate staging; independent native review is separate."""
from __future__ import annotations
import json
import hashlib
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from adapters.eval import native_adapter, branch_authoring, architecture_authoring
from adapters.eval.eval_support import repository_file_inventory
from runtime.schema import validate_json
SKILLS=Path(__file__).resolve().parents[2]
REPO=SKILLS.parents[2]
PACKAGE=SKILLS/'packages/guru-review-branch'

class BranchAuthoringTests(unittest.TestCase):
    def test_committed_native_candidate_preserves_unchanged_caller_and_separate_precondition(self):
        with tempfile.TemporaryDirectory() as temp:
            case=next(c for c in json.loads((PACKAGE/'evals/evals.json').read_text())['evals'] if c['id']=='native-common-expectation')
            work=Path(temp)/'execution/workdir';work.mkdir(parents=True)
            for relative in case['files']:
                target=work/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(PACKAGE/relative,target)
            interface=json.loads((PACKAGE/'interface.json').read_text())
            req={**{k:case[k] for k in ('prompt','files','model_id','native_execution_mode','native_execution_adapter')},
                'schema_version':'1.0','skill_id':PACKAGE.name,'case_id':case['id'],'package_root':str(PACKAGE),
                'workdir':str(work),'runtime_target':str(REPO/'.trellis/guru-team/scripts/bash/run-skill-command.sh'),
                'interface':{'public_invocation':interface['public_contracts']['invocation']}}
            values=native_adapter.build_context(req,'codex')
            try:
                protocol=json.loads(values[4].read_text());repo=Path(protocol['owner_repository'])
                facts=json.loads((repo/branch_authoring.FACTS).read_text())
                public=json.loads((repo/branch_authoring.PUBLIC_INPUT).read_text())
                validate_json(public,PACKAGE/'schemas/public-delivery-branch-review-input-1.0.schema.json','input')
                architecture=json.loads((repo/branch_authoring.ARCHITECTURE_INPUT).read_text())
                validate_json(architecture,PACKAGE.parent/'guru-maintain-architecture-baseline/schemas/public-input-delivery-task-impact-sync-3.0.schema.json','input')
                self.assertEqual(public['branch_review_commit'],subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip())
                self.assertNotEqual(public['base_ref'],public['branch_review_commit'])
                diff=(repo/'.trellis/tasks/branch-evidence/committed.patch').read_text()
                self.assertIn('diff --git a/interval.py',diff)
                self.assertNotIn('diff --git a/range_filter.py',diff)
                self.assertIn('not native Check',facts['prerequisite_boundary'])
                self.assertIn('actual fixed base-to-HEAD',values[0])
                self.assertIn('--upstream-architecture',protocol['architecture_context'])
                self.assertFalse((repo/'.trellis/.runtime/guru-team/evals/owner-result.json').exists())
                self.qualifier_trace_roundtrip(req,values,protocol)
            finally:
                values[9].set();values[8].join(timeout=2)

    def qualifier_trace_roundtrip(self,request,values,protocol):
        # Real helper/FIFO/original wrappers; owner fields are objective test
        # inputs only, never native semantic evidence or model context.
        repository=Path(protocol['repository_projection_root'])
        package=Path(protocol['projection_root'])
        architecture_package=repository/'.trellis/guru-team/skills/packages/guru-maintain-architecture-baseline'
        architecture=json.loads((repository/branch_authoring.ARCHITECTURE_INPUT).read_text())
        facts=json.loads((repository/branch_authoring.FACTS).read_text())
        owner_repository=Path(protocol['owner_repository'])
        before=repository_file_inventory(owner_repository)
        helper=[sys.executable,protocol['helper_path'],'--trace',protocol['trace_path'],
            '--request-sha256',protocol['request_sha256'],'--projection-root',str(package),
            '--repository-root',str(repository),'--sandbox-root',protocol['model_root'],
            '--request-fifo',protocol['request_fifo'],'--response-fifo',protocol['response_fifo'],
            '--skill-sha256',protocol['skill_sha256'],'--wrapper-sha256',protocol['wrapper_sha256']]
        def read(path,kind='owner_file'):
            result=subprocess.run([*helper,'read','--kind',kind,'--path',str(path)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
        def invoke(envelope,*arguments):
            result=subprocess.run([*helper,'invoke','--stdin',*arguments],input=json.dumps(envelope),
                capture_output=True,text=True,timeout=30)
            self.assertEqual(result.returncode,0,result.stderr or result.stdout)
            return result.stdout.strip()
        for path in architecture_authoring.public_contract_reads(architecture_package,architecture):read(path)
        for path in facts['architecture_reads']:read(repository/path)
        schema=json.loads((architecture_package/'schemas/semantic-result-delivery-3.0.schema.json').read_text())
        props=schema['oneOf'][0]['properties']
        owner={key:value for key,value in architecture.items() if key in props}
        owner.update(input_sha256=hashlib.sha256(json.dumps(architecture,ensure_ascii=False,
            sort_keys=True,separators=(',',':')).encode()).hexdigest(),typed_exit='baseline_current',
            baseline_identity=architecture['baseline']['identity'],
            constitution_identity=architecture['constitution']['identity'],
            impact_kind='no_architecture_impact',impact_reason='Objective transport fixture only.',promotion_state='no_change',
            consumer={'kind':'workflow','id':'guru-architecture-baseline-current-router'},
            ai_review_gate={'status':'passed','reviewed_scope':'Objective transport fixture.',
                'evidence_summary':'Native semantics are evaluated separately.','findings':[],
                'conclusion':'Original wrapper chain only.'})
        invoke({'public_input':architecture,'owner_result':owner},'--upstream-architecture')
        for name in branch_authoring.PUBLIC_READS:read(package/name,'skill_contract')
        read(repository/branch_authoring.FACTS)
        for path in facts['required_reads']:read(repository/path)
        for path in Path(protocol['model_root'],'evidence/case').iterdir():read(path,'case_file')
        public=json.loads((repository/branch_authoring.PUBLIC_INPUT).read_text())
        target={'repo_locator':'.','task_ref':public['task_ref'],'base_head':public['base_ref'],
            'review_head':public['branch_review_commit'],'review_commit':public['branch_review_commit'],
            'range_locator':'.trellis/tasks/branch-evidence/committed.patch'}
        qualification={'profile':'branch_review_candidate_set','mode':'workflow','caller':'guru-review-branch',
            'target_locator':public['task_ref'],'target':target,'candidate_refs':['transport-only'],
            'candidate_locators':[{'candidate_ref':'transport-only','locators':['interval.py']}]}
        witness={'requirement_refs':['docs/range.md'],'supported_entry_refs':['interval.py'],
            'existing_caller_refs':['range_filter.py'],
            'honest_action_sequence':['Call the supplied upper endpoint operation.'],
            'defect_observation':'The supplied half-open predicate excludes the contract upper endpoint.',
            'excluded_assumptions':[]}
        for name in ('normal-scenario','solution-mechanism','root-cause'):
            semantic={'schema_version':'1.0','skill_id':'guru-qualify-'+name,'public_input':qualification,
                'candidate_results':[{'candidate_ref':'transport-only','decision':'qualified_current',
                    'reason':'Objective wrapper chain only.','witness':witness}],
                'ai_review_gate':{'status':'passed','reviewed_candidate_refs':['transport-only'],
                    'summary':'Objective transport only.'},'typed_exit':'classified',
                'consumer':{'kind':'workflow','id':'guru-'+name+'-classified-router'}}
            if name == 'root-cause':
                semantic['candidate_results']=[{'candidate_ref':'transport-only','goal':'ordinary_feature',
                    'classification':'not_incident_applicable','reason':'Objective original wrapper transport only.',
                    'evidence':{'applicability_basis':'The bounded range predicate is an ordinary feature.'}}]
            invoke({'schema_version':'1.0','semantic_result':semantic},'--qualifier',name)
        result=invoke({'public_input':public,'owner_result':{
            'candidate_classifications':[{'candidate_ref':'transport-only','decision':'qualified_current',
                'witness':witness,'consumer_use':'branch_review_route_checker'}],
            'semantic_review':{**{key:[] for key in ('qualified_findings','scope_proposals','observations',
                'followup_candidates','rejected_candidates')},'qualified_findings':[{
                    'candidate_ref':'transport-only','disposition':'qualified_finding',
                    'affected_behavior':witness['defect_observation'],'path':'interval.py',
                    'evidence_refs':['docs/range.md'],'finding_ref':'transport-upper-endpoint','severity':'P2',
                    'introduced_head':public['branch_review_commit'],'fix_head':None,'closure_head':None,
                    'status':'open','closure_evidence':[]}], 'ai_review_gate':{'status':'implementation_required',
                    'summary':'No native semantic review is asserted by this transport test.'}},
            'delivery_review':{'task_scope':['R1'],'delivery_slice':['R1'],'remaining_work':[],
                'independent_delivery_conditions':['Actual native review remains required.'],
                'validation_boundaries':['Original wrapper transport only.'],'current_slice_status':'failed',
                'remaining_work_status':'disclosed','summary':'Transport does not establish semantic adequacy.'},
            'verification_evidence':{'reviewer':'transport-only','review_source':'independent-agent',
                'evidence':['Original wrappers executed; native semantics remain unverified.']}}})
        trace=Path(protocol['trace_path'])
        events=json.loads(trace.read_text())['events']
        self.assertEqual(len([event for event in events if event['kind']=='invoke']),5)
        native_adapter.validate_native_trace(trace,protocol['request_sha256'],request,
            Path(protocol['wrapper_path']),result,values[4])
        self.assertEqual(json.loads(result)['exit_id'],'implementation_required')
        after=repository_file_inventory(owner_repository)
        changed={path for path in before.keys()|after.keys() if before.get(path)!=after.get(path)}
        self.assertEqual(changed,set(facts['owner_mutated_paths']))
        self.assertEqual(len(changed),2)
        self.assertTrue(any(path.endswith('/'+public['delivery_key']['delivery_id']+'/review-gate.json') for path in changed))

if __name__=='__main__':unittest.main()
