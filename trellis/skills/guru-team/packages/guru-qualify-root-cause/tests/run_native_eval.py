"""Focused factual native authoring, followed by the actual installed wrapper.

Expectations remain host-only. The native context receives contracts and facts,
never the corpus or expected decisions. Outputs/logs stay outside the repository.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time

PACKAGE = Path(__file__).resolve().parents[1]


def run(root: Path, output: Path, selected: list[str], cases_file: Path | None = None) -> list[dict]:
    installed = root / '.trellis/guru-team/skills/packages/guru-qualify-root-cause'
    cases = json.loads((cases_file or PACKAGE / 'tests/semantic_cases.json').read_text())
    if selected: cases = [row for row in cases if row['id'] in selected]
    public_input = json.loads((installed / 'examples/public-task-free-pre-write-input.json').read_text())
    public_input['target_locator'] = 'request:focused-native-eval'
    public_input['target'].update(repo_locator='.', request_locator='request:focused-native-eval',
        checkout_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(), bounded_paths=['README.md'])
    public_input['candidate_refs'] = ['current-candidate']
    public_input['candidate_locators'] = [{'candidate_ref':'current-candidate','locators':['path:README.md','request:focused-native-eval']}]
    output.mkdir(parents=True,exist_ok=True)
    results=[]
    for row in cases:
        start=time.time()
        with tempfile.TemporaryDirectory(prefix='guru-root-native-') as folder:
            model_root=Path(folder)
            # Public semantic contract and closed authoring schema, with no examples or expectations.
            for name in ['SKILL.md','references/contract.md','schemas/semantic-result.schema.json']:
                target=model_root/name; target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes((installed/name).read_bytes())
            prompt=('Execute the semantic review specified by the provided Skill and contract. '
                'Treat the factual record below as the current accepted scope and observed candidate. '
                'Normal-scenario and solution-mechanism owners have already qualified this real supported candidate. '
                'Read SKILL.md, references/contract.md and schemas/semantic-result.schema.json. '
                'Do not inspect other repositories, configuration, memory or an eval corpus. '
                'Determine the actual goal and causal disposition from these facts. '
                'Author one complete schema_version 1.0 envelope containing your semantic_result, '
                'including this exact public_input, your candidate result, full-set AI gate, selected typed_exit and its consumer. '
                'The outer object MUST have exactly schema_version and semantic_result; put all result fields inside semantic_result. Return only JSON; the host executes the original public wrapper without changing your judgment.\n'
                'PUBLIC INPUT:\n'+json.dumps(public_input)+'\nCURRENT FACTS:\n'+row['facts'])
            argv=['codex','exec','--ephemeral','--skip-git-repo-check','--sandbox','read-only','--cd',str(model_root),
                  '--output-last-message',str(output/(row['id']+'.native.json')),'-']
            proc=subprocess.run(argv,input=prompt,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=240)
            (output/(row['id']+'.native.log')).write_text(proc.stdout+'\n'+proc.stderr)
            result={'id':row['id'],'native_argv':argv,'native_returncode':proc.returncode,'elapsed_seconds':round(time.time()-start,2)}
            if proc.returncode:
                result.update(status='native_unavailable',detail=proc.stderr[-1500:]); results.append(result); print(json.dumps(result),flush=True); continue
            try:
                raw=(output/(row['id']+'.native.json')).read_text().strip()
                if raw.startswith('```'): raw=raw.split('\n',1)[1].rsplit('```',1)[0]
                envelope=json.loads(raw)
                wrapper=subprocess.run([str(installed/'scripts/invoke.sh'),'--invocation','-'],cwd=root,
                    input=json.dumps(envelope),text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                    env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
                actual=envelope['semantic_result']['candidate_results'][0]
                result.update(wrapper_returncode=wrapper.returncode,wrapper_stdout=wrapper.stdout.strip(),
                    wrapper_stderr=wrapper.stderr.strip(),goal=actual['goal'],classification=actual['classification'])
                result['status']='passed' if (wrapper.returncode==0 and json.loads(wrapper.stdout)['exit_id']==row['expected_exit']
                    and actual['goal']==row['expected_goal'] and actual['classification']==row['expected_classification']) else 'failed'
            except (ValueError,KeyError,OSError) as error: result.update(status='failed',detail=str(error))
            results.append(result); print(json.dumps(result),flush=True)
    (output/'results.json').write_text(json.dumps(results,indent=2)+'\n')
    return results


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--cases-file',type=Path); parser.add_argument('--output',type=Path,required=True); parser.add_argument('--case',action='append',default=[])
    args=parser.parse_args()
    results=run(args.root.resolve(),args.output.resolve(),args.case,args.cases_file)
    raise SystemExit(0 if results and all(row['status']=='passed' for row in results) else 1)
