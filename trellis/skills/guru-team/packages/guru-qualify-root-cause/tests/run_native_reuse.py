"""Native caller reuse review using an actual previously authored qualification.

Run with --root, --prior (a real native root envelope), and --output outside
that repository. Expected decisions remain in this host script only.
"""
from pathlib import Path
import argparse,json,tempfile,subprocess,os
parser=argparse.ArgumentParser()
parser.add_argument('--root',type=Path,required=True)
parser.add_argument('--prior',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
root=args.root.resolve(); pkg=root/'.trellis/guru-team/skills/packages/guru-qualify-root-cause'
out=args.output.resolve()
if out.is_relative_to(root): parser.error('Native outputs must stay outside the repository.')
out.mkdir(parents=True,exist_ok=True)
prior=json.loads(args.prior.read_text())['semantic_result']
pub=prior['public_input']; facts='Earlier mechanism replaces a stale shared Authorization header with the current credential per request; causal trace and same concurrency 1/8 validation support it. Current scope, authority, conditions and evidence remain the same. At later Check stage the exact same mechanism/code appears, with no new observation. Separately, a proposed materially changed repair replaces that behavior with max concurrency 4 rejection before Provider, leaves the stale header untouched, no independent protection or measured mitigation basis. Original valid concurrency 8 is excluded.'
with tempfile.TemporaryDirectory(prefix='guru-root-reuse-') as folder:
 m=Path(folder)
 for source,name in [(pkg/'references/contract.md','root-contract.md'),(root/'.trellis/guru-team/skills/packages/guru-check-task/SKILL.md','caller.md'),(pkg/'schemas/semantic-result.schema.json','semantic-schema.json')]: (m/name).write_bytes(source.read_bytes())
 prompt='Read caller.md and root-contract.md. Execute current stage applicability consumption for the two actual candidate variants below. This is stage review, not completion. Return JSON with unchanged {requires_fresh_qualification, stage_review_required, reason} and changed {requires_fresh_qualification, stage_review_required, reason, invocation}. In changed.invocation author a complete root package envelope (schema_version string 1.0, semantic_result) using semantic-schema.json and exact public input below. Prior result is actual owner output, not a new approval. Do not write files or search expectations.\nPRIOR ACTUAL SEMANTIC RESULT:\n'+json.dumps(prior)+'\nCURRENT FACTS:\n'+facts+'\nPUBLIC INPUT FOR CHANGED CANDIDATE:\n'+json.dumps(pub)
 argv=['codex','exec','--ephemeral','--skip-git-repo-check','--sandbox','read-only','--cd',str(m),'--output-last-message',str(out/'native.json'),'-']
 p=subprocess.run(argv,input=prompt,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=240); (out/'native.log').write_text(p.stdout+'\n'+p.stderr)
 v=json.load(open(out/'native.json')); invocation=v['changed']['invocation']
 w=subprocess.run([str(pkg/'scripts/invoke.sh'),'--invocation','-'],input=json.dumps(invocation),cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 report={'native_argv':argv,'native_returncode':p.returncode,'unchanged':v['unchanged'],'changed':{k:x for k,x in v['changed'].items() if k!='invocation'},'wrapper_returncode':w.returncode,'wrapper_stdout':w.stdout,'wrapper_stderr':w.stderr}
 report['status']='passed' if p.returncode==0 and w.returncode==0 and v['unchanged']['requires_fresh_qualification'] is False and v['unchanged']['stage_review_required'] is True and v['changed']['requires_fresh_qualification'] is True and v['changed']['stage_review_required'] is True and json.loads(w.stdout)['exit_id']=='mechanism_revision_required' else 'failed'
 (out/'results.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))

raise SystemExit(0 if report['status']=='passed' else 1)
