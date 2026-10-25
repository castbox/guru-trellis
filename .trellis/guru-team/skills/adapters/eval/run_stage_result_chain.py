"""Run the original native adapter for one continuous two-Delivery observation.

The caller supplies an external isolated CODEX_HOME. This driver supplies facts
and command transport only; it contains no expected exit or semantic grade.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',required=True)
    parser.add_argument('--run-root',required=True)
    parser.add_argument('--model',required=True)
    parser.add_argument('--resume-protocol')
    parser.add_argument('--mode', choices=('source', 'installed'), default='source')
    args=parser.parse_args()
    root=Path(args.root).resolve();run=Path(args.run_root).resolve()
    if run.exists(): raise ValueError('Use a fresh external run root.')
    work=run/'execution/workdir';work.mkdir(parents=True)
    relative='case/input.json';path=work/relative;path.parent.mkdir()
    path.write_text(json.dumps({'profile':'delivery_completion','mode':'workflow',
        'task_ref':'.trellis/tasks/current','task_key':{'task_id':'current','lifecycle_generation':0}}))
    skills=root/('trellis/skills/guru-team' if args.mode == 'source' else '.trellis/guru-team/skills')
    package=skills/'packages/guru-review-task-completion'
    interface=json.loads((package/'interface.json').read_text())
    request={'schema_version':'1.0','skill_id':package.name,'case_id':'native-stage-continuous',
        'package_root':str(package),'workdir':str(work),'files':[relative],
        'prompt':'Execute the continuous two-Delivery Task against its original source and owners. Judge each actual stage, consume real predecessor results and report only the final original wrapper stdout.',
        'interface':{'public_invocation':interface['public_contracts']['invocation']},
        'runtime_target':str(root/'.trellis/guru-team/scripts/bash/run-skill-command.sh'),
        'native_execution_mode':'semantic_authoring','native_execution_adapter':'codex',
        'model_id':args.model,'corpus_sha256':hashlib.sha256((package/'evals/evals.json').read_bytes()).hexdigest()}
    request_path=work.parent/'request.json';request_path.write_text(json.dumps(request))
    command=[sys.executable,'-m','adapters.eval.native_adapter','--adapter','codex',
        '--native-command','codex','--request',str(request_path)]
    runtime_root = skills if args.mode == 'source' else skills.parent
    environment={**os.environ,'PYTHONPATH':os.pathsep.join([str(skills), str(runtime_root)]),
        'GURU_TEAM_QUALIFICATION_SOURCE_WORKTREE':str(root),
        'GURU_UPSTREAM_DELIVERY_SCRIPTS':str(root/'.trellis/scripts')}
    if args.resume_protocol:
        from adapters.eval.stage_result_chain import RESUME_PROTOCOL_ENV
        environment[RESUME_PROTOCOL_ENV] = str(Path(args.resume_protocol).resolve())
    with (run/'adapter-response.json').open('w') as output, (run/'adapter.stderr').open('w') as diagnostic:
        result=subprocess.run(command,cwd=root,env=environment,stdout=output,stderr=diagnostic)
    return result.returncode


if __name__=='__main__':
    raise SystemExit(main())
