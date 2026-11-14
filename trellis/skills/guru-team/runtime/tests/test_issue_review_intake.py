"""Real source wrappers with local Git/GitHub fixtures; no live mutation claims."""
from __future__ import annotations
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SKILLS = Path(__file__).resolve().parents[2]
REPO = SKILLS.parents[2]
sys.path.insert(0, str(SKILLS))
from runtime.schema import validate_json

R = 'guru-review-change-request'
D = 'guru-discover-change-context'
C = 'guru-clarify-requirements'
W = 'guru-review-contract-wording'
DIMENSIONS = ('requirement_completeness','delivery_unit_consistency','implementation_target_evidence','claimed_behavior_current','current_implementation_gap','docs_code_tests_consistency','archived_history_constraints','duplicate_reuse_validity','target_authority_current','prerequisite_hash_linkage')


class IssueReviewIntakeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='guru-819-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'repo'
        self.repo.mkdir()
        self.git('init','-q','-b','main')
        self.git('config','user.email','fixture@example.invalid')
        self.git('config','user.name','Fixture')
        (self.repo / 'source.txt').write_text('selected source\n')
        self.git('add','source.txt'); self.git('commit','-qm','source')
        self.commit = self.git('rev-parse','HEAD')
        self.state = self.root / 'github.json'
        self.state.write_text(json.dumps({'issue':{'number':27,'url':'https://github.com/example/repo/issues/27','state':'OPEN','title':'Issue','body':'Reviewed scope','updatedAt':'2026-11-14T00:00:00Z','labels':[],'createdAt':'2026-11-14T00:00:01Z'},'comments':[], 'calls':[]}))
        binary=self.root/'bin';binary.mkdir()
        gh=binary/'gh'
        gh.write_text('#!'+sys.executable+'\n'+'''import json,os,sys
from datetime import datetime,timezone
from pathlib import Path
p=Path(os.environ['ISSUE_REVIEW_FIXTURE']);s=json.loads(p.read_text());a=sys.argv[1:];s['calls'].append(a)
result=None
if a[:2]==['issue','view']:result=s['issue']
elif a[:2]==['issue','create']:
 s['issue'].update(title=a[a.index('--title')+1],body=a[a.index('--body')+1],createdAt=datetime.now(timezone.utc).isoformat());result=s['issue']['url']
elif a[:2]==['issue','list']:result=[{'number':s['issue']['number']}]
elif a[0]=='api':
 if '--method' in a and a[a.index('--method')+1] in ['POST','PATCH']:
  body=a[a.index('--raw-field')+1].removeprefix('body=')
  if a[a.index('--method')+2]=='repos/example/repo/issues/27':
   s['issue']['body']=body;result=s['issue']
  else:
   c={'id':701,'body':body,'issue_url':'https://api.github.com/repos/example/repo/issues/27'}
   if a[a.index('--method')+1]=='POST':s['comments'].append(c)
   else:s['comments']=[c if x['id']==701 else x for x in s['comments']]
   result=c
 elif '--paginate' in a:result=[s['comments']]
 elif a[-1]=='repos/example/repo/issues/27':result=s['issue']
 else:result=next(x for x in s['comments'] if str(x['id'])==a[-1].rsplit('/',1)[-1])
p.write_text(json.dumps(s))
if s.get('lose_comment_response') and '--method' in a and a[a.index('--method')+1]=='POST':
 s['lose_comment_response']=False;p.write_text(json.dumps(s));raise SystemExit(1)
print(result if isinstance(result,str) else json.dumps(result))
''')
        gh.chmod(0o755)
        self.env={**os.environ,'PATH':str(binary)+os.pathsep+os.environ['PATH'],'ISSUE_REVIEW_FIXTURE':str(self.state)}
        self.source={'kind':'issue','repo':'example/repo','number':27,'title':'Issue','body':'Reviewed scope','updated_at':'2026-11-14T00:00:00Z'}
        sync=self.call('guru-sync-base','invoke.sh',{'schema_version':'1.0','public_input':{'source_exit':'start','mode':'workflow','repo_root':str(self.repo),'route':'repo_change','operation':'read','base_ref':'main','base_commit':self.commit}})
        b=sync['transition']['base']
        self.public={'profile':'existing_issue_intake','source_exit':sync['exit_id'],'mode':sync['handoff_mode'],'issue':{'repo_ref':'example/repo','number':27},'base_source':{k:b[k] for k in ('kind','selected_ref','commit')},'continuation_id':'issue-27'}

    def git(self,*args):
        return subprocess.run(['git','-C',str(self.repo),*args],check=True,capture_output=True,text=True).stdout.strip()

    def call(self,skill,script,payload,*,flags=None,ok=True):
        args=[str(SKILLS/'packages'/skill/'scripts'/script),*(flags or ['--invocation','-'])]
        result=subprocess.run(args,input=json.dumps(payload),capture_output=True,text=True,env=self.env,cwd=REPO)
        if ok:self.assertEqual(result.returncode,0,result.stdout+'\n'+result.stderr)
        value=json.loads(result.stdout)
        if skill=='guru-sync-base' and script=='invoke.sh' and value.get('exit_id') in ('synced','baseline_ready'):
            # Validate the unchanged stdout before the workflow's thin projection.
            contracts=json.loads((SKILLS/'packages'/skill/'interface.json').read_text())['public_contracts']
            output=next(row for row in contracts['outputs'] if row['exit_id']==value['exit_id'])
            projection=next(row for row in contracts['projections'] if row['id'] in output['consumer_use_ids'])
            self.assertEqual('direct',projection['operation'])
            consumer=next(row for row in contracts['consumer_inputs'] if row['id']==projection['consumer_input_id'])
            validate_json(value,SKILLS/consumer['contract']['path'],'sync_consumer')
        return value['result'] if value.get('formal_exit') is False else value

    def readiness(self,public,exit_id):
        owner={'public_input':public,'typed_exit':exit_id,'result_summary':'Actual fixture review conclusion.','source_refs':[],'source_selection':[], 'dimensions':[{'id':x,'conclusion':'Reviewed within this original dimension.'} for x in DIMENSIONS],'ai_review_gate':{'status':'passed' if exit_id=='ready' else 'blocked' if exit_id=='blocked' else 'reroute','summary':'Fixture semantic authoring, not native AI evidence.'}}
        if exit_id.startswith('supplement_'):owner['gap']='The indicated coverage is missing.'
        e={'schema_version':'1.0','public_input':public,'owner_context':{'change_request':self.source},'owner_result':owner}
        e['owner_result']=self.call(R,'record-change-request-review.sh',e)
        checked=self.call(R,'check-change-request-review.sh',e)
        e['validation_receipt']=checked['validation_receipt']
        return self.call(R,'invoke.sh',e)

    def test_ready_and_all_requested_routes_use_real_sync_source_without_chain_receipts(self):
        for route in ['ready','supplement_context','supplement_requirements','supplement_wording','full_intake_required','refresh_issue_baseline','blocked']:
            with self.subTest(route=route):
                out=self.readiness(self.public,route)
                self.assertEqual(route,out['exit_id'])
                if route!='blocked':self.assertEqual(self.public['base_source'],out['base_source'])
        self.git('commit','--allow-empty','-qm','unrelated main advance')
        out=self.readiness(self.public,'ready')
        self.assertEqual(self.commit,out['base_source']['commit'])
        self.assertNotIn('transition',out)

    def test_actual_discovery_return_reenters_same_readiness(self):
        requested=self.readiness(self.public,'supplement_context')
        public={'profile':'issue_readiness_supplement',**{k:v for k,v in requested.items() if k!='exit_id'},'source_exit':requested['exit_id']}
        owner={'public_input':public,'typed_exit':'supplemented','result_summary':'The selected source behavior is unchanged.','source_refs':['source.txt'],'ai_review_gate':{'status':'passed','summary':'Reviewed requested current facts.'}}
        envelope={'schema_version':'1.0','public_input':public,'owner_context':{},'owner_result':owner}
        envelope['owner_result']=self.call(D,'record-context-discovery.sh',envelope,flags=['--root',str(self.repo),'--invocation','-'])
        self.call(D,'check-context-discovery.sh',envelope,flags=['--root',str(self.repo),'--invocation','-'])
        actual=self.call(D,'invoke.sh',envelope,flags=['--root',str(self.repo),'--invocation','-'])
        returned={'profile':'issue_review_return','source_exit':actual['exit_id'],**{k:v for k,v in actual.items() if k not in ['exit_id','result_summary']},'context_result':actual['result_summary']}
        ready=self.readiness(returned,'ready')
        self.assertEqual('ready',ready['exit_id'])
        self.assertEqual(self.public['base_source'],ready['base_source'])

    def test_dedicated_sync_refresh_preserves_fixed_source_and_issue(self):
        out=self.readiness(self.public,'refresh_issue_baseline')
        self.git('commit','--allow-empty','-qm','main evolved')
        b=out['base_source']
        actual=self.call('guru-sync-base','invoke.sh',{'schema_version':'1.0','public_input':{'source_exit':out['exit_id'],'mode':out['mode'],'repo_root':str(self.repo),'route':'repo_change','operation':'read','base_ref':b['selected_ref'],'base_commit':b['commit'],'return_identity':{'profile':'existing_issue_intake','issue':out['issue'],'continuation_id':out['continuation_id']}}})
        self.assertEqual(self.commit,actual['transition']['base']['commit'])
        self.assertEqual('existing_issue_intake',actual['handoff_profile'])
        self.assertEqual(self.public['issue'],actual['return_identity']['issue'])

    def test_new_ready_enters_current_creation_with_independent_integration_branch(self):
        import hashlib
        import shutil
        from datetime import datetime
        from zoneinfo import ZoneInfo
        from runtime.delivery_projection.tests.upstream_fixture import scripts_source
        scripts=scripts_source()
        shutil.copytree(scripts,self.repo/'.trellis/scripts')
        package=next(parent/'package.json' for parent in scripts.parents if (parent/'package.json').is_file() and json.loads((parent/'package.json').read_text()).get('name')=='@mindfoldhq/trellis')
        (self.repo/'.trellis/.version').write_text(json.loads(package.read_text())['version']+'\n')
        (self.repo/'.trellis/workflow.md').write_bytes((REPO/'trellis/workflows/guru-team/workflow.md').read_bytes())
        self.git('add','.trellis');self.git('commit','-qm','matching task runtime')
        fixed=self.git('rev-parse','HEAD');self.git('update-ref','refs/remotes/origin/main',fixed)
        self.git('remote','add','origin','https://github.com/example/repo.git')
        baseline=self.call('guru-sync-base','invoke.sh',{'schema_version':'1.0','public_input':{'source_exit':'start','mode':'workflow','repo_root':str(self.repo),'route':'repo_change','operation':'read','base_ref':'origin/main','base_commit':fixed}})
        public={**self.public,'source_exit':baseline['exit_id'],'base_source':{k:baseline['transition']['base'][k] for k in ('kind','selected_ref','commit')}}
        ready=self.readiness(public,'ready')
        # Local integration main may advance after the exact source was reviewed.
        self.git('commit','--allow-empty','-qm','later integration commit')
        target=self.root/'task-checkout';prefix=datetime.now(ZoneInfo('Asia/Shanghai')).strftime('%m-%d');ref=f'.trellis/tasks/{prefix}-issue-review'
        request={'profile':'delivery_task_creation','action':'create_task','creation':{'task_id':'issue-review','task_ref':ref,'source_profile':'existing_issue','reviewed_source':{'kind':'issue',**ready['issue'],'disposition':'exact_source'},'accepted_scope_identity':'scope:'+hashlib.sha256(self.source['body'].encode()).hexdigest(),'delivery_target':{'repo_ref':'example/repo','branch_ref':'main'},'selected_base_ref':'main','reviewed_base_source':ready['base_source']},'acquisition':{'route':'provision_linked_worktree','branch_ref':'codex/issue-review','decision_head':ready['base_source']['commit'],'transaction_id':'acquisition:issue-review','result_id':'checkout:issue-review','provision_disposition':'new_branch','path_source':'explicit','checkout_root':str(target)},'task':{'title':'Issue review fixture','description':'Reviewed exact source','scope':self.source['body']}}
        created=self.call('guru-create-task','invoke.sh',request,flags=['--root',str(self.repo),'--input','-'])
        self.assertEqual('created',created['exit_id'])
        self.assertEqual(fixed,subprocess.check_output(['git','-C',str(target),'rev-parse','HEAD'],text=True).strip())
        task=json.loads((target/ref/'task.json').read_text())
        self.assertEqual('main',task['base_branch']);self.assertEqual(27,task['source']['number'])
        request['action']='recover_created_task_result'
        self.assertEqual(created,self.call('guru-create-task','invoke.sh',request,flags=['--root',str(self.repo),'--input','-']))

    def local_clarification(self, public, *, missing=False, comment_body=None, comment_id=None, body_edit=None, pending_comment=False):
        import hashlib
        auth=json.loads((SKILLS/'packages'/C/'examples/requirements-clarification.json').read_text())
        auth.pop('content_identity')
        auth['mode']='workflow';auth['schema_version']='1.0'
        for field in ('invocation_context','target_disposition','active_task_evidence','consumer','error'):
            auth.pop(field)
        auth['review_target']={'kind':'issue','repo':'example/repo','issue_number':27,'url':'https://github.com/example/repo/issues/27','state':'open','updated_at':self.source['updated_at'],'body_sha256':hashlib.sha256(self.source['body'].encode()).hexdigest()}
        for row in auth['source_actions']:
            row.pop('action_digest');row.pop('payload_sha256')
        if missing:
            auth.update(typed_exit='needs_context')
            auth['context_evidence']={'status':'missing','evidence_refs':[],'missing_reason':'The requested current fact needs investigation.'}
        if comment_body is not None or body_edit is not None:
            digest=lambda v:hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
            actions,results=[],[]
            def completed_action(action_id,kind,method,endpoint,body):
                before=json.loads(subprocess.check_output(['gh','api','repos/example/repo/issues/27'],env=self.env,text=True))
                preimage=hashlib.sha256(before['body'].encode()).hexdigest()
                if kind=='issue_comment' and pending_comment:
                    attempted=subprocess.run(['gh','api','--method',method,endpoint,'--raw-field','body='+body],env=self.env,text=True,capture_output=True)
                    self.assertNotEqual(0,attempted.returncode)
                    action={'action_id':action_id,'kind':kind,'target':{'repo':'example/repo','issue_number':27},'payload':{'body':body},'preimage_sha256':preimage,'payload_sha256':digest({'body':body})}
                    action['action_digest']=digest(action)
                    action.update(status='pending',mutation_evidence=None)
                    actions.append(action)
                    return
                receipt=json.loads(subprocess.check_output(['gh','api','--method',method,endpoint,'--raw-field','body='+body],env=self.env,text=True))
                read_endpoint='repos/example/repo/issues/27' if kind=='issue_body_edit' else f"repos/example/repo/issues/comments/{receipt['id']}"
                live=json.loads(subprocess.check_output(['gh','api',read_endpoint],env=self.env,text=True))
                action={'action_id':action_id,'kind':kind,'target':{'repo':'example/repo','issue_number':27},'payload':{'body':body},'preimage_sha256':preimage,'payload_sha256':digest({'body':body})}
                action['action_digest']=digest(action)
                action.update(status='executed',mutation_evidence={'source':'ai-reviewed-gh'})
                url='https://github.com/example/repo/issues/27' if kind=='issue_body_edit' else f"https://github.com/example/repo/issues/27#issuecomment-{receipt['id']}"
                actions.append(action)
                results.append({'action_id':action_id,'kind':kind,'status':'succeeded','url':url,'state':'open','updated_at':self.source['updated_at'],'content_sha256':hashlib.sha256(live['body'].encode()).hexdigest(),'action_digest':action['action_digest'],'facts_sha256':digest(live)})
            if body_edit is not None:
                completed_action('revise-body','issue_body_edit','PATCH','repos/example/repo/issues/27',body_edit)
            if comment_body is not None:
                completed_action('review-comment','issue_comment','POST' if comment_id is None else 'PATCH','repos/example/repo/issues/27/comments' if comment_id is None else f'repos/example/repo/issues/comments/{comment_id}',comment_body)
            auth.update(typed_exit='blocked' if pending_comment else 'refresh_context',source_actions=actions,mutation_results=results)
            if pending_comment:
                auth['ai_review_gate'].update(status='blocked',summary='The body revision succeeded; the comment response is unresolved.')
                auth['reason']='Preserve the completed body revision and recover the original comment response.'
        recorded=auth
        local={'public_input':public,'typed_exit':'blocked' if pending_comment else 'needs_context' if missing else 'supplemented','result_summary':'Reviewed this requirement gap.','source_refs':[],'source_selection':recorded['source_selection'],'clarification':recorded,'ai_review_gate':{'status':'blocked' if pending_comment else 'passed','summary':'Original Clarify method completed for this object.'}}
        local=self.call(C,'record-requirements-clarification.sh',local,flags=['--mode','workflow','--input','-'])
        self.call(C,'check-requirements-clarification.sh',local,flags=['--input','-'])
        self.last_local_clarification=local
        return self.call(C,'invoke.sh',{'schema_version':'1.0','public_input':public,'owner_context':{},'owner_result':local})

    def test_clarify_extra_facts_return_and_readonly_supplement(self):
        requested=self.readiness(self.public,'supplement_requirements')
        public={'profile':'issue_readiness_supplement',**{k:v for k,v in requested.items() if k!='exit_id'},'source_exit':requested['exit_id']}
        missing=self.local_clarification(public,missing=True)
        context={'profile':missing['handoff_profile'],'source_exit':missing['exit_id'],'mode':missing['handoff_mode'],'issue':missing['issue'],'base_source':missing['base_source'],'continuation_id':missing['handoff_continuation_id'],'gap':missing['gap'],'return_identity':missing['return_identity']}
        owner={'public_input':context,'typed_exit':'context_ready','result_summary':'The requested repository fact is established.','source_refs':['source.txt'],'ai_review_gate':{'status':'passed','summary':'Resolved the original fact gap.'}}
        e={'schema_version':'1.0','public_input':context,'owner_context':{},'owner_result':owner}
        e['owner_result']=self.call(D,'record-context-discovery.sh',e,flags=['--root',str(self.repo),'--invocation','-'])
        actual=self.call(D,'invoke.sh',e,flags=['--root',str(self.repo),'--invocation','-'])
        resumed={'profile':actual['handoff_profile'],'source_exit':actual['exit_id'],'mode':actual['handoff_mode'],'issue':actual['handoff_issue'],'base_source':actual['handoff_base_source'],'continuation_id':actual['handoff_continuation_id'],'gap':actual['handoff_gap'],'context_result':actual['context_result'],'source_refs':actual['source_refs']}
        supplemented=self.local_clarification(resumed)
        returned={'profile':'issue_review_return','source_exit':supplemented['exit_id'],**{k:v for k,v in supplemented.items() if k not in ['exit_id','result_summary']},'requirements_result':supplemented['result_summary']}
        self.assertEqual('ready',self.readiness(returned,'ready')['exit_id'])
        self.assertFalse(any('--method' in x or x[:2]==['issue','create'] for x in json.loads(self.state.read_text())['calls']))

    def test_clarify_publishes_and_updates_same_comment_through_source_actions(self):
        request=self.readiness(self.public,'supplement_requirements')
        public={'profile':'issue_readiness_supplement',**{k:v for k,v in request.items() if k!='exit_id'},'source_exit':request['exit_id']}
        first=self.local_clarification(public,comment_body='Reviewed requirements only. Wording and start prerequisites remain for Readiness.')
        self.assertEqual('supplemented',first['exit_id'])
        second=self.local_clarification(public,comment_body='Updated requirements review. The scope choice is resolved; readiness remains independent.',comment_id=701)
        self.assertEqual('supplemented',second['exit_id'])
        state=json.loads(self.state.read_text())
        self.assertEqual(1,len(state['comments']))
        self.assertEqual(1,sum('POST' in x for x in state['calls']))
        self.assertEqual(1,sum('PATCH' in x for x in state['calls']))

    def test_clarify_body_revision_then_comment_uses_each_live_preimage(self):
        import hashlib
        import importlib.util
        request=self.readiness(self.public,'supplement_requirements')
        public={'profile':'issue_readiness_supplement',**{k:v for k,v in request.items() if k!='exit_id'},'source_exit':request['exit_id']}
        revised='Revised scope and explicit acceptance.'
        comment='Reviewed the revised requirements. Independent Readiness still checks all start conditions.'
        result=self.local_clarification(public,body_edit=revised,comment_body=comment)
        self.assertEqual('supplemented',result['exit_id'])
        state=json.loads(self.state.read_text())
        self.assertEqual(revised,state['issue']['body'])
        self.assertEqual(comment,state['comments'][0]['body'])
        owner=self.last_local_clarification['clarification']
        self.assertEqual(hashlib.sha256(self.source['body'].encode()).hexdigest(),owner['source_actions'][0]['preimage_sha256'])
        self.assertEqual(hashlib.sha256(revised.encode()).hexdigest(),owner['source_actions'][1]['preimage_sha256'])
        # The existing confirmation validator shares this Issue action sequence.
        # This unit call does not claim the unrelated confirmation entry/gates.
        owner=copy.deepcopy(owner)
        owner['invocation_context']={'kind':'normal_scenario_scope_confirmation'}
        owner['target_disposition']={'disposition':'keep_current_open_issue'}
        spec=importlib.util.spec_from_file_location('issue_confirmation_sequence',SKILLS/'packages'/C/'runtime/confirmation.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        module.validate_actions(owner)

    def test_clarify_body_success_pending_comment_preserves_facts_then_recovers(self):
        import hashlib
        import importlib.util
        digest=lambda v:hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
        request=self.readiness(self.public,'supplement_requirements')
        public={'profile':'issue_readiness_supplement',**{k:v for k,v in request.items() if k!='exit_id'},'source_exit':request['exit_id']}
        state=json.loads(self.state.read_text());state['lose_comment_response']=True;self.state.write_text(json.dumps(state))
        revised='Resolved requirement and current acceptance.'
        comment='Requirements reviewed after the body revision; readiness remains independent.'
        blocked=self.local_clarification(public,body_edit=revised,comment_body=comment,pending_comment=True)
        self.assertEqual({'exit_id':'blocked'},blocked)
        local=copy.deepcopy(self.last_local_clarification)
        self.assertEqual(['executed','pending'],[x['status'] for x in local['clarification']['source_actions']])
        self.assertEqual(['issue_body_edit'],[x['kind'] for x in local['clarification']['mutation_results']])
        spec=importlib.util.spec_from_file_location('partial_issue_confirmation',SKILLS/'packages'/C/'runtime/confirmation.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        confirmation=copy.deepcopy(local['clarification'])
        confirmation['invocation_context']={'kind':'normal_scenario_scope_confirmation'}
        confirmation['target_disposition']={'disposition':'keep_current_open_issue'}
        module.validate_actions(confirmation)
        # Original recovery rereads the one actual comment; it does not POST again.
        pages=json.loads(subprocess.check_output(['gh','api','--paginate','--slurp','repos/example/repo/issues/27/comments'],env=self.env,text=True))
        matches=[row for page in pages for row in page if row['body']==comment]
        self.assertEqual(1,len(matches))
        live=json.loads(subprocess.check_output(['gh','api',f"repos/example/repo/issues/comments/{matches[0]['id']}"],env=self.env,text=True))
        action=local['clarification']['source_actions'][1]
        action.update(status='executed',mutation_evidence={'source':'ai-reviewed-gh'})
        local['clarification']['mutation_results'].append({'action_id':action['action_id'],'kind':'issue_comment','status':'succeeded','url':f"https://github.com/example/repo/issues/27#issuecomment-{live['id']}",'state':'open','updated_at':self.source['updated_at'],'content_sha256':hashlib.sha256(live['body'].encode()).hexdigest(),'action_digest':action['action_digest'],'facts_sha256':digest(live)})
        local['clarification']['typed_exit']='refresh_context';local['clarification']['ai_review_gate'].update(status='passed',summary='The original comment was recovered and both final objects were read back.')
        local['clarification']['reason']='The completed body revision and original comment are now verified.'
        local['typed_exit']='supplemented';local['ai_review_gate']['status']='passed'
        local=self.call(C,'record-requirements-clarification.sh',local,flags=['--mode','workflow','--input','-'])
        self.call(C,'check-requirements-clarification.sh',local,flags=['--input','-'])
        recovered=self.call(C,'invoke.sh',{'schema_version':'1.0','public_input':public,'owner_context':{},'owner_result':local})
        self.assertEqual('supplemented',recovered['exit_id'])
        state=json.loads(self.state.read_text())
        self.assertEqual(revised,state['issue']['body']);self.assertEqual(comment,state['comments'][0]['body'])
        self.assertEqual(1,len(state['comments']))
        self.assertEqual(1,sum('POST' in row for row in state['calls']))

    def test_wording_scanner_result_returns_or_reports_requirement_gap(self):
        requested=self.readiness(self.public,'supplement_wording')
        public={'profile':'issue_readiness_supplement',**{k:v for k,v in requested.items() if k!='exit_id'},'source_exit':requested['exit_id']}
        review=json.loads((SKILLS/'packages'/W/'examples/contract-wording-review.json').read_text())['semantic_review']
        review['typed_exit']='pass';review['generated_at']='2026-11-14T00:00:00Z';review['ai_review_gate'].pop('reviewed_scan_sha256');review['ai_review_gate'].pop('planning_checked_dimensions')
        change={'source_kind':'issue','identity':'https://github.com/example/repo/issues/27','title':self.source['title'],'body':self.source['body'],'updated_at':self.source['updated_at']}
        e={'profile':'change_request','mode':'workflow','change_request':change,'owner_result':review}
        recorded=self.call(W,'record-contract-wording-review.sh',e)
        e['owner_result']=recorded;checked=self.call(W,'check-contract-wording-review.sh',e)
        for exit_id in ['supplemented','requirements_gap']:
            owner={'public_input':public,'typed_exit':exit_id,'result_summary':'Complete title/body wording review.','source_refs':[],'wording_review':recorded,'ai_review_gate':{'status':'reroute' if exit_id=='requirements_gap' else 'passed','summary':'Reviewed this local wording scope.'}}
            if exit_id=='requirements_gap':owner['gap']='The Issue describes two conflicting product outcomes.'
            out=self.call(W,'invoke.sh',{'schema_version':'1.0','public_input':public,'owner_context':{},'owner_result':owner,'validation_receipt':checked['validation_receipt']})
            key='wording_result' if exit_id=='supplemented' else 'requirements_gap'
            ret={'profile':'issue_review_return','source_exit':out['exit_id'],**{k:v for k,v in out.items() if k not in ['exit_id','result_summary','gap']},key:out['result_summary'] if exit_id=='supplemented' else out['gap']}
            actual=self.readiness(ret,'ready' if exit_id=='supplemented' else 'supplement_requirements')
            self.assertEqual('ready' if exit_id=='supplemented' else 'supplement_requirements',actual['exit_id'])

    def creation_input(self):
        from datetime import datetime,timezone
        data=json.loads((SKILLS/'packages/guru-create-issue/examples/public-create-input.json').read_text())
        data['draft'].update(repo_ref='example/repo',title='Issue',body='Reviewed scope',labels=[])
        # Derive only the existing creation input's documented target facts.
        import hashlib
        digest=lambda v:hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
        sha=lambda t:hashlib.sha256(t.encode()).hexdigest()
        authority={'kind':'draft','repo':'example/repo','issue_number':None,'url':None,'state':'draft','updated_at':None,'body_sha256':sha('Reviewed scope')}
        target={'kind':'proposed_draft','repo':'example/repo','draft_id':'draft-27','source_request_sha256':digest(authority),'title_sha256':sha('Issue'),'body_sha256':sha('Reviewed scope')}
        data['reviewed_target']={**target,'identity_sha256':digest(target),'content_sha256':digest({'title_sha256':sha('Issue'),'body_sha256':sha('Reviewed scope')})}
        data['reviewed_label_identity_sha256']=digest({'reviewed_target':digest(target),'labels':[]})
        data['reviewed_at']=datetime.now(timezone.utc).isoformat()
        return data

    def test_create_comment_order_and_same_object_recovery(self):
        data=self.creation_input()
        first=self.call('guru-create-issue','invoke.sh',data,flags=['--input','-'])
        data['action']='recover_created_issue_result'
        recovered=self.call('guru-create-issue','invoke.sh',data,flags=['--input','-'])
        self.assertEqual(first,recovered)
        state=json.loads(self.state.read_text());calls=state['calls']
        self.assertEqual(1,sum(x[:2]==['issue','create'] for x in calls))
        self.assertEqual(1,sum('--method' in x and 'POST' in x for x in calls))
        self.assertEqual(['issue','create'],calls[0][:2]);self.assertEqual(['issue','view'],calls[1][:2])
        self.assertIn('POST',calls[2]);self.assertEqual(['api','repos/example/repo/issues/comments/701'],calls[3])
        self.assertEqual(1,len(state['comments']))
        self.assertNotIn('comment_id',first)

    def test_comment_response_loss_recovers_completed_comment_without_reposting(self):
        state=json.loads(self.state.read_text());state['lose_comment_response']=True;self.state.write_text(json.dumps(state))
        data=self.creation_input()
        failed=self.call('guru-create-issue','invoke.sh',data,flags=['--input','-'],ok=False)
        self.assertEqual('stale_identity',failed['code'])
        data['action']='recover_created_issue_result'
        result=self.call('guru-create-issue','invoke.sh',data,flags=['--input','-'])
        self.assertEqual('created',result['exit_id'])
        state=json.loads(self.state.read_text())
        self.assertEqual(1,len(state['comments']))
        self.assertEqual(1,sum('--method' in x and 'POST' in x for x in state['calls']))
        self.assertEqual(1,sum(x[:2]==['issue','create'] for x in state['calls']))

    def test_real_sync_preserves_synced_source_kind(self):
        remote=self.root/'origin.git'
        subprocess.run(['git','clone','--bare','--quiet',str(self.repo),str(remote)],check=True)
        self.git('remote','add','origin',str(remote))
        sync=self.call('guru-sync-base','invoke.sh',{'schema_version':'1.0','public_input':{'source_exit':'start','mode':'workflow','repo_root':str(self.repo),'route':'repo_change','operation':'sync','base_branch':'main'}})
        self.assertEqual('synced',sync['exit_id'])
        base=sync['transition']['base']
        public={**self.public,'source_exit':sync['exit_id'],'base_source':{'kind':'synced_branch','selected_ref':base['selected_base'],'commit':base['decision_head']}}
        ready=self.readiness(public,'ready')
        self.assertEqual({'kind':'synced_branch','selected_ref':'main','commit':self.commit},ready['base_source'])

        # Advance the local bare origin while the selected checkout stays behind.
        advanced=self.git('commit-tree',self.git('rev-parse','HEAD^{tree}'),'-p',self.commit,'-m','remote source advance')
        self.git('push','--quiet','origin',advanced+':refs/heads/main')
        self.assertEqual(self.commit,self.git('rev-parse','HEAD'))
        requested=self.readiness(public,'refresh_issue_baseline')
        actual=self.call('guru-sync-base','invoke.sh',{'schema_version':'1.0','public_input':{'source_exit':requested['exit_id'],'mode':requested['mode'],'repo_root':str(self.repo),'route':'repo_change','operation':'sync','base_branch':requested['base_source']['selected_ref'],'return_identity':{'profile':'existing_issue_intake','issue':requested['issue'],'continuation_id':requested['continuation_id']}}})
        self.assertEqual('synced',actual['exit_id'])
        self.assertEqual('existing_issue_intake',actual['handoff_profile'])
        self.assertEqual(public['mode'],actual['handoff_mode'])
        self.assertEqual(public['continuation_id'],actual['handoff_continuation_id'])
        self.assertEqual({'profile':'existing_issue_intake','issue':public['issue'],'continuation_id':public['continuation_id']},actual['return_identity'])
        refreshed=actual['transition']['base']
        self.assertEqual('main',refreshed['selected_base'])
        self.assertEqual('origin',refreshed['remote'])
        for field in ('decision_head','local_base_head','remote_base_head'):
            self.assertEqual(advanced,refreshed[field])
        self.assertEqual(advanced,self.git('rev-parse','HEAD'))
        returned={'profile':actual['handoff_profile'],'source_exit':actual['exit_id'],'mode':actual['handoff_mode'],'issue':actual['return_identity']['issue'],'base_source':{'kind':'synced_branch','selected_ref':refreshed['selected_base'],'commit':refreshed['decision_head']},'continuation_id':actual['return_identity']['continuation_id']}
        ready=self.readiness(returned,'ready')
        self.assertEqual('ready',ready['exit_id'])
        self.assertEqual(public['issue'],ready['issue'])
        self.assertEqual(public['continuation_id'],ready['continuation_id'])
        self.assertEqual({'kind':'synced_branch','selected_ref':'main','commit':advanced},ready['base_source'])


if __name__=='__main__':unittest.main()
