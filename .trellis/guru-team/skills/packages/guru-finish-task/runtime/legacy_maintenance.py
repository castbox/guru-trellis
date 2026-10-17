"""Original owner selected-legacy profile. Never invokes current lifecycle mutation."""
from __future__ import annotations
import argparse
import importlib.util
import json
import subprocess
from pathlib import Path
from runtime.io import CommandError

OWNER = "guru-finish-task"

CONTROL_ROOT = ".trellis/.runtime/guru-team/finish/"

def fail(code, field, message):
    raise CommandError(code,field,message)

def path_at(root,ref):
    path=Path(ref)
    if '..' in path.parts: fail('invalid_path','control_ref','Use an exact owner control path.')
    return path if path.is_absolute() else Path(root)/path

def raw(path):
    import base64,stat
    if not path.exists():return None
    if not path.is_file() or path.is_symlink():fail('unsupported_control',str(path),'Select a regular control file.')
    return {'content_base64':base64.b64encode(path.read_bytes()).decode(),'mode':stat.S_IMODE(path.stat().st_mode)}

def attributed(value,key,task_ref):
    if not isinstance(value,dict):return False
    if value.get('task_id')==key['task_id'] and value.get('lifecycle_generation')==key['lifecycle_generation']:
        return value.get('task_ref',task_ref)==task_ref
    if value.get('task_ref')==task_ref and 'task_id' not in value and 'lifecycle_generation' not in value:return True
    return any(attributed(value.get(k),key,task_ref) for k in ('input','public_input','task_key','key','identity'))

def inspect_controls(root,key,task_ref,refs,source_task_ref=None):
    import hashlib
    selected=json.loads(path_at(root,(source_task_ref or task_ref)+'/task.json').read_text())
    if selected.get('id')!=key['task_id'] or selected.get('lifecycle_generation',0)!=key['lifecycle_generation']:fail('control_identity_mismatch','key','Inspect the exact original Task source before public writes.')
    historical=set()
    if OWNER=='guru-finish-task':
        config_path=Path(root)/'.trellis/guru-team/config.yml'
        runtime_value='.trellis/.runtime/guru-team'
        if config_path.exists():
            for line in config_path.read_text().splitlines():
                if line.startswith('runtime_root:'):
                    value=line.split(':',1)[1].split('#',1)[0].strip()
                    runtime_value=value.strip("\"'") or runtime_value
        runtime=Path(runtime_value)
        runtime=runtime if runtime.is_absolute() else Path(root)/runtime
        token=hashlib.sha256(selected.get('id',Path(task_ref).name).strip().encode()).hexdigest()[:20]
        for suffix in ('finalization-transaction/'+token+'/finalization-transaction.json','owner-checkpoints/'+token+'/task-finalization-gate.json'):
            path=runtime/suffix
            try: historical.add(path.relative_to(root).as_posix())
            except ValueError:historical.add(str(path))
    rows=[]
    for ref in refs:
        if not ref.startswith(CONTROL_ROOT) and ref not in historical:fail('control_owner_mismatch',ref,'Use this original owner namespace or a proven exact historical source inventory.')
        path=path_at(root,ref);snapshot=raw(path)
        if snapshot is None:fail('control_missing',ref,'Inspect original controls before public writes.')
        value=json.loads(path.read_text())
        matched=attributed(value,key,task_ref)
        if OWNER=='guru-publish-task-delivery' and not matched and ref.endswith('.gate.json'):
            transaction=path_at(root,ref[:-10]+'.json')
            if transaction.is_file():
                original=json.loads(transaction.read_text())
                matched=attributed(original,key,task_ref) and value.get('transaction_ref')==original.get('transaction_ref')
        if not matched:fail('control_identity_mismatch',ref,'Establish exact original Task/generation attribution.')
        if OWNER=='guru-finish-task' and value.get('stage')=='success':fail('terminal_result_preserved',ref,'Preserve terminal Finish results and sealed resources.')
        rows.append({'path':ref,'source':snapshot})
    return rows

def freeze_controls(root,key,task_ref,rows,source,operation_id,source_task_ref=None):
    # Same-owner checkpoint: no other producer's private format is read.
    checkpoint=path_at(root,CONTROL_ROOT+'legacy-retirement/'+operation_id+'.json')
    value={'root':str(root),'key':key,'task_ref':task_ref,'controls':rows,'source':source,'retired':False}
    if source_task_ref is not None:value['source_task_ref']=source_task_ref
    if checkpoint.exists():
        previous=json.loads(checkpoint.read_text())
        if any(previous[k]!=value[k] for k in value if k!='retired'):fail('operation_mismatch','recovery_ref','Keep the original owner checkpoint.')
    else:
        if source_task_ref is not None and raw(path_at(root,source_task_ref+'/task.json'))!=source:fail('source_mismatch','source','Freeze the physically read original Task bytes and mode.')
        if inspect_controls(root,key,task_ref,[r['path'] for r in rows],source_task_ref)!=rows:fail('control_changed','controls','Refresh original owner preimages.')
        checkpoint.parent.mkdir(parents=True,exist_ok=True);checkpoint.write_text(json.dumps(value,indent=2)+'\n')
    return str(checkpoint)

def checkpoint_input(public):
    path=Path(public['recovery_ref']);state=json.loads(path.read_text())
    if any(state[k]!=public[k] for k in ('root','key','task_ref')):fail('identity_mismatch','recovery_ref','Use this original owner exact checkpoint.')
    if state.get('source_task_ref',state['task_ref'])!=public.get('source_task_ref',public['task_ref']):fail('identity_mismatch','source_task_ref','Use the exact frozen physical source.')
    if public['control_refs']!=[r['path'] for r in state['controls']]:fail('control_mismatch','control_refs','Use fixed original owner controls.')
    return path,state

def precheck_restore(recovery_ref):
    state=json.loads(Path(recovery_ref).read_text())
    for row in state['controls']:
        if raw(path_at(state['root'],row['path']))!=(None if state['retired'] else row['source']):fail('control_changed',row['path'],'Preserve later work before either rollback half.')

def restore_controls(recovery_ref):
    import base64
    precheck_restore(recovery_ref);path=Path(recovery_ref);state=json.loads(path.read_text())
    for row in state['controls']:
        target=path_at(state['root'],row['path']);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(base64.b64decode(row['source']['content_base64']));target.chmod(row['source']['mode'])
    state['retired']=False;path.write_text(json.dumps(state,indent=2)+'\n')

def execute(package_root, public):
    profile=public['profile']; root=Path(public['root'])
    if profile=='legacy_control_freeze':
        return {'recovery_ref':freeze_controls(root,public['key'],public['task_ref'],public['controls'],public['source'],public['operation_id'],public.get('source_task_ref'))}
    if profile in {'legacy_control_restore_check','legacy_control_restore'}:
        state=json.loads(Path(public['recovery_ref']).read_text())
        if Path(state['root']).resolve()!=root.resolve():fail('target_mismatch','root','Restore only this original owner target.')
        if profile=='legacy_control_restore_check':precheck_restore(public['recovery_ref'])
        else:restore_controls(public['recovery_ref'])
        return {'recovery_ref':public['recovery_ref']}
    if profile=='legacy_control_inspection':
        return {'formal_exit':False,'controls':inspect_controls(root,public['key'],public['task_ref'],public['control_refs'],public.get('source_task_ref'))}
    if profile=='legacy_control_retirement':
        checkpoint,state=checkpoint_input(public)
        preserved=path_at(root,public['preserved_source_ref'])
        if raw(preserved)!=state['source']:fail('preserved_source_mismatch','preserved_source_ref','Read the physically preserved original Task bytes before retiring controls.')
        for row in state['controls']:
            actual=raw(path_at(root,row['path']))
            if actual is not None and actual!=row['source']:fail('control_changed',row['path'],'Preserve later control work.')
        for row in state['controls']:path_at(root,row['path']).unlink(missing_ok=True)
        state['retired']=True;checkpoint.write_text(json.dumps(state,indent=2)+'\n')
        return {'exit_id':'legacy_controls_retired','owner_id':OWNER,'key':public['key']}
    if profile!='legacy_history_verification' or OWNER=='guru-finish-task': fail('profile_mismatch','profile','Select an explicit supported legacy original-owner profile.')
    facts=public['fact_refs']; verified=[]
    for fact in facts:
        command=['gh','pr','view',str(fact['pr_number']),'--repo',fact['repo_ref'],'--json','number,url,headRefOid,baseRefName,headRefName,state,mergeCommit,mergedAt']
        proc=subprocess.run(command,cwd=root,capture_output=True,text=True)
        if proc.returncode: return {'exit_id':'unverified_legacy_history','key':public['key'],'reason_code':'github_facts_unavailable'}
        actual=json.loads(proc.stdout)
        if actual['number']!=fact['pr_number'] or actual['headRefOid']!=fact['reviewed_head'] or actual['baseRefName']!=fact['target_branch'] or actual['headRefName']!=fact['head_branch']:
            return {'exit_id':'unverified_legacy_history','key':public['key'],'reason_code':'historical_pr_mismatch'}
        result={'repo_ref':fact['repo_ref'],'pr_number':fact['pr_number'],'reviewed_head':actual['headRefOid'],'target_branch':actual['baseRefName'],'head_branch':actual['headRefName']}
        if OWNER=='guru-merge-task-delivery':
            merge=(actual.get('mergeCommit') or {}).get('oid')
            if actual['state']!='MERGED' or merge!=fact['merge_commit'] or not actual.get('mergedAt'):
                return {'exit_id':'unverified_legacy_history','key':public['key'],'reason_code':'historical_merge_mismatch'}
            for args in [('cat-file','-e',merge+'^{commit}'),('merge-base','--is-ancestor',merge,fact['target_ref'])]:
                if subprocess.run(['git',*args],cwd=root,capture_output=True).returncode:
                    return {'exit_id':'unverified_legacy_history','key':public['key'],'reason_code':'historical_target_unverified'}
            result['merge_commit']=merge
        verified.append(result)
    return {'exit_id':'verified_legacy_history','key':public['key'],'facts':verified}

def run(package_root, command, argv):
    import sys
    parser=argparse.ArgumentParser(); parser.add_argument('--root',required=True); parser.add_argument('--input',required=True)
    args=parser.parse_args(argv)
    public=json.load(sys.stdin) if args.input=='-' else json.loads(Path(args.input).read_text())
    if Path(args.root).resolve()!=Path(public['root']).resolve(): raise CommandError('target_mismatch','root','Use the selected target checkout.')
    from runtime.schema import validate_json
    validate_json(public,package_root/'schemas/legacy-maintenance-input-1.0.schema.json','input')
    return execute(package_root,public)


def maybe_run(package_root, argv):
    import io,sys
    parser=argparse.ArgumentParser(add_help=False);parser.add_argument('--root');parser.add_argument('--input')
    args,_=parser.parse_known_args(argv)
    if not args.input:return None
    if args.input=='-':
        content=sys.stdin.read();sys.stdin=io.StringIO(content);public=json.loads(content)
    else:
        from runtime.io import read_json
        public=read_json(args.input,'input')
    if public.get('profile') not in {'legacy_control_retirement','legacy_history_verification'}:return None
    if Path(args.root or '.').resolve()!=Path(public['root']).resolve():raise CommandError('target_mismatch','root','Use exact selected legacy target.')
    from runtime.schema import validate_json
    validate_json(public,package_root/'schemas/legacy-maintenance-input-1.0.schema.json','input')
    return execute(package_root,public)
