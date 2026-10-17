"""Source-private real-wrapper PR conflict, recovery, Check and full Review flow.

Requires the explicit reviewed Fork via --fork. Provider and semantic inputs
are fixtures; outputs do not prove live GitHub or native AI judgments.
--output retains each public operation and its complete Git Trace2 events.
"""
import argparse, importlib.util, json, os, subprocess, sys, time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--fork',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.source=a.source.resolve();a.output.mkdir(parents=True,exist_ok=True)
skills=a.source/'trellis/skills/guru-team';sys.path.insert(0,str(skills));os.environ['TRELLIS_DELIVERY_API_COMMON']=str(a.fork/'packages/cli/src/templates/trellis/scripts/common')
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
f=load('joint_flow',skills/'packages/guru-check-task/tests/test_delivery_flow.py')
from runtime.delivery_projection.adapter import authority_ref
from runtime.delivery_projection.gates import rework
case=f.DeliveryFlow();case.delivery_profile='pull_request';case.setUp();reports=[]
original=case.wrapper
def wrapper(skill,name,*args,**kwargs):
 trace=a.output/f'op-{len(reports)}.trace.jsonl';before=os.environ.get('GIT_TRACE2_EVENT');os.environ['GIT_TRACE2_EVENT']=str(trace);start=time.perf_counter()
 try:
  raw=subprocess.run(['bash',str(skills/'packages'/skill/'scripts'/name),'--root',str(case.repo),*map(str,args)],capture_output=True,text=True)
  (a.output/f'raw-{len(reports)}.json').write_text(json.dumps({'code':raw.returncode,'stdout':raw.stdout,'stderr':raw.stderr}))
  assert raw.returncode==0,(raw.stdout,raw.stderr)
  parsed=json.loads(raw.stdout);result=parsed.get('result',parsed)
  reports.append({'skill':skill,'wrapper':name,'args':list(map(str,args)),'result':result,'seconds':time.perf_counter()-start,'trace':str(trace)})
  (a.output/'operations.json').write_text(json.dumps(reports,indent=2));return result
 finally:
  if before is None:os.environ.pop('GIT_TRACE2_EVENT',None)
  else:os.environ['GIT_TRACE2_EVENT']=before
case.wrapper=wrapper
try:
 checked=case.check();reviewed=case.full_review(checked);ready=case.readiness(reviewed)
 body=ready['pr_body'];record=case.projection.read_record();candidate=case.projection.resolve(case.key)['candidate']
 with case.provider_response(body=body):
  case.projection.apply({'api_version':'1.0','operation':'record_publication','key':case.key,'owner_role':'publication','owner_id':case.projection.declaration()['owners']['publication'],'expected_phase':'publishing','result':{'result_id':'publication:joint-pr9','owner_id':case.projection.declaration()['owners']['publication'],'evidence':[record['accepted_scope']],'profile':'pull_request','candidate':candidate,'repo_ref':'example/repo','pr_number':9,'reviewed_head':case.head,'target_ref':'main','publication_ref':{'locator':'https://github.com/example/repo/pull/9','revision':'sha256:'+__import__('hashlib').sha256(body.encode()).hexdigest()}}})
 prior=case.projection.resolve(case.key)['publication_result'];old_base=case.git('rev-parse','main').strip()
 case.git('add',case.task_ref);case.git('commit','-qm','persist original published facts');anchor=case.git('rev-parse','HEAD').strip()
 case.git('switch','main');(case.repo/'app.txt').write_text('base conflict\n');case.git('add','app.txt');case.git('commit','-qm','advance conflicting base');new=case.git('rev-parse','HEAD').strip();case.git('switch','feat/flow')
 merged=subprocess.run(['git','merge','--no-commit','--no-ff',new],cwd=case.repo,capture_output=True,text=True);assert merged.returncode!=0
 (case.repo/'app.txt').write_text('resolved feature and base\n');case.git('add','app.txt');tree=case.git('write-tree').strip()
 digest=subprocess.run([sys.executable,'-c','import sys;from pathlib import Path;sys.path[:0]=sys.argv[1:];from common import index_tree_digest;print(index_tree_digest(Path.cwd()))',str(skills/'packages/guru-reconcile-task-base/runtime'),str(skills)],cwd=case.repo,capture_output=True,text=True,check=True).stdout.strip()
 public={'profile':'delivery_resolved_candidate','mode':'workflow','source_exit':'resolved_reconciliation_passed','task_ref':case.task_ref,'delivery_key':case.key,'phase2_commit_anchor':anchor,'branch':'feat/flow','selected_base_ref':new,'old_base_head':old_base,'new_base_head':new,'merge_head':new,'stage0_tree':tree,'index_tree_sha256':digest,'parent_order':[anchor,new],'commit_message':'chore(base): record resolved joint candidate','resume_target':'branch_review'}
 result=wrapper('guru-reconcile-task-base','execute-resolved-base-reconciliation.sh','--input',case.write('resolved.json',public));again=wrapper('guru-reconcile-task-base','execute-resolved-base-reconciliation.sh','--input',case.write('resolved.json',public));assert result['status']=='committed' and again['status']=='recovered' and result['reconciled_task_head']==again['reconciled_task_head']
 case.head=result['reconciled_task_head'];rework(case.projection,case.key,'publication','implementation',authority_ref(case.repo/'requirements.md',case.repo),['check','full_review','readiness']);case.projection.begin_check(case.key,case.projection.candidate(['app.txt'],head_ref=case.head,base_ref=case.projection.content_base(case.key)))
 current=case.check();authoring={'profile':'delivery_branch_review','mode':'workflow','base_ref':case.projection.content_base(case.key),'review_intent':'initial_review','check_result_id':current['check_result_id']}
 projected=wrapper('guru-reconcile-task-base','project-resolved-full-review.sh','--input',case.write('resolved.json',public),'--result',case.write('resolved-result.json',result),'--authoring',case.write('full-review-authoring.json',authoring));assert projected['branch_review_commit']==case.head
 final=case.full_review(current);assert final['exit_id']=='passed' and case.projection.resolve(case.key)['publication_result']==prior
 assert case.projection.resolve(case.key)['id']==case.key['delivery_id'];assert case.git('show','-s','--format=%P',case.head).strip().split()==[anchor,new]
 print(json.dumps({'passed':True,'same_delivery':case.key,'same_pr':9,'resolved_head':case.head,'full_review':final,'operations':len(reports),'boundary':'local real Git/public wrapper fixture with provider/semantic fixtures; not live GitHub conflict'}))
finally:case.doCleanups()
