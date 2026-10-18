"""Selected maintenance orchestration; all semantic decisions belong to contract.md."""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path
from runtime.io import CommandError
from runtime.schema import validate_json
from runtime.maintenance_transport import call, inspect_source
from controls import raw, path_at, preserved_source, fail

ORDER=('guru-publish-task-delivery','guru-merge-task-delivery','guru-finish-task','guru-approve-task-plan','guru-check-task','guru-review-branch')

def read(value):
    import sys
    return json.load(sys.stdin) if value=='-' else json.loads(Path(value).read_text())

def store(path,state):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')

def owner_call(package_root,owner,public):
    wrapper='invoke.sh' if public['profile']=='legacy_control_retirement' else 'legacy-maintenance.sh'
    script=package_root.parent/owner/'scripts'/wrapper
    if not script.is_file():fail('owner_missing',owner,'Load the original owner public maintenance port from the complete source.')
    result=subprocess.run(['bash',str(script),'--root',str(public['root']),'--input','-'],input=json.dumps(public),text=True,capture_output=True)
    if result.returncode:
        try: reason=json.loads(result.stdout).get('code','original_owner_failed')
        except json.JSONDecodeError: reason='original_owner_failed'
        fail(reason,owner,'Repair the concrete original-owner maintenance mismatch before resuming; fixed preimages remain unchanged.')
    try: output=json.loads(result.stdout)
    except json.JSONDecodeError:fail('original_owner_output_invalid',owner,'Require one actual original-owner JSON result.')
    return output['result'] if output.get('formal_exit') is False and 'result' in output else output

def inspect_selected_source(public):
    facts=inspect_source(public['source_ref'])
    if public['profile']=='archive_resume' and 'task_resume' not in facts['contract']['operation_kinds']:
        fail('maintenance_prerequisite_missing','source_ref','The selected pair lacks task_resume. Resolve the matching source through the original tools owner before archive-resume writes.')
    return facts

def selection_input(public):
    selected={"root":public["target_checkout"],"key":public["key"],"task_ref":public["task_ref"]}
    if public["profile"]=="archive_resume": selected["original_task_ref"]=public["original_task_ref"]
    return selected

def control_selection(public):
    selected={"root":public["target_checkout"],"key":public["key"],"task_ref":public.get("original_task_ref",public["task_ref"])}
    if public["profile"]=="archive_resume": selected["source_task_ref"]=public["task_ref"]
    return selected

def prepare(package_root, public, decisions):
    inspect_selected_source(public)
    selection=selection_input(public)
    observed=call(public['source_ref'],'inspectTaskTarget',selection)
    upstream=decisions['upstream_input']
    if any(upstream.get(k)!=v for k,v in selection.items()): fail('selection_mismatch','upstream_input','Use the exact explicit selected Task and checkout.')
    if public['profile']=='archive_resume' and upstream.get('active_ref')!=public['active_ref']: fail('selection_mismatch','active_ref','Use the exact selected active destination.')
    method={'convert':'prepareTaskConversion','archive_resume':'prepareArchivedTaskResume','history_closeout':'prepareLegacyCloseout'}[public['profile']]
    controls={}
    if set(decisions['control_refs'])-set(ORDER): fail('owner_missing','control_refs','Add the exact original owner profile before any maintenance write.')
    for owner in ORDER:
        refs=decisions['control_refs'].get(owner,[])
        result=owner_call(package_root,owner,{'profile':'legacy_control_inspection',**control_selection(public),'control_refs':refs})
        if result['controls']: controls[owner]=result['controls']
    plan=call(public['source_ref'],method,upstream)
    return {'public_input':public,'public_plan':plan,'controls':controls,'history_note':decisions['history_note'],'retired_owners':[],'upstream_recovery_ref':None,'phase':'prepared'}

def freeze_selected_owners(package_root,path,state):
    public=state['public_input'];state.setdefault('owner_recovery_refs',{})
    source=next(a['source'] for a in state['public_plan']['actions'] if a['path']==public['task_ref']+'/task.json')
    original={key:source[key] for key in ('content_base64','mode')}
    for owner,rows in state['controls'].items():
        if owner in state['owner_recovery_refs']:continue
        state['owner_recovery_refs'][owner]=owner_call(package_root,owner,{'profile':'legacy_control_freeze',**control_selection(public),'controls':rows,'source':original,'operation_id':state['public_plan']['operation_id']})['recovery_ref']
        store(path,state)
    for owner,ref in state['owner_recovery_refs'].items():
        owner_call(package_root,owner,{'profile':'legacy_control_restore_check','root':public['target_checkout'],'recovery_ref':ref})

def resume(package_root,path,state):
    source=state['public_input']['source_ref']; root=state['public_input']['target_checkout']
    if state['phase']=='prepared':
        freeze_selected_owners(package_root,path,state)
        # Ref is deterministically fixed by the public operation id before apply.
        state['upstream_recovery_ref']=str(path.parent/'public'/ (state['public_plan']['operation_id']+'.json')); store(path,state)
        result=call(source,'applyMaintenance',{'plan':state['public_plan'],'state_dir':str(path.parent/'public')})
    else:
        result=call(source,'resumeMaintenance',{'recovery_ref':state['upstream_recovery_ref']})
    state['upstream_recovery_ref']=result['recovery_ref']; state['phase']='public_pending'; store(path,state)
    if result['status']!='applied': return {'exit_id':'resume_required','profile':'resume','recovery_ref':str(path)}
    if state['public_input']['profile']=='archive_resume':
        if not result.get('resumed_task'): fail('resumed_identity_missing','resumed_task','Read the active identity returned by public archive resume.')
        state['resumed_task']=result['resumed_task']
        store(path,state)
    preserved_source(root,state)
    state['phase']='retiring'; store(path,state)
    for owner in ORDER:
        if owner not in state['controls'] or owner in state['retired_owners']: continue
        owner_call(package_root,owner,{'profile':'legacy_control_retirement',**control_selection(state['public_input']),'preserved_source_ref':preserved_source(root,state),'control_refs':[x['path'] for x in state['controls'][owner]],'recovery_ref':state['owner_recovery_refs'][owner]})
        state['retired_owners'].append(owner); store(path,state)
    state['phase']='verification_required'; store(path,state)
    return {'exit_id':'resume_required','profile':'resume','recovery_ref':str(path)}

def observe_native(root, argv):
    if not isinstance(argv,list) or not argv or not all(isinstance(x,str) and x for x in argv): fail('invalid_native_entry','argv','Supply the actual target-native entry argv.')
    # A source/external installed script cannot stand in for the target entry.
    local=[]
    for arg in argv:
        candidate=Path(arg)
        if candidate.is_absolute():
            try: relative=candidate.relative_to(root)
            except ValueError: continue
        else: relative=candidate
        ref=relative.as_posix()
        if ref.startswith('.trellis/') or ref.startswith('.agents/'): local.append(ref)
    if not local or any(not path_at(root,x).is_file() for x in local): fail('target_native_required','argv','Invoke an existing target checkout native entry, not an external replacement.')
    result=subprocess.run(argv,cwd=root,text=True,capture_output=True)
    return {'argv':argv,'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr}

def run(package_root, command, argv):
    parser=argparse.ArgumentParser(); parser.add_argument('--root',required=True); parser.add_argument('--input',required=True); parser.add_argument('--plan'); parser.add_argument('--action',choices=['inspect','prepare','apply','resume','rollback','observe','finalize'],default='inspect'); parser.add_argument('--review-input')
    args=parser.parse_args(argv); public=read(args.input)
    if command and command.get('stdout')=='single_typed_exit' and args.action in {'inspect','prepare','observe'}: fail('preview_command_required','action','Use scripts/preview.sh for read-only intermediate facts.')
    if command and command.get('stdout')=='intermediate_receipt' and args.action not in {'inspect','prepare','observe'}: fail('invoke_command_required','action','Use the public invocation for target writes or terminal routes.')
    validate_json(public,package_root/'schemas/public-input.schema.json','input')
    if public['profile'] in {'convert','archive_resume','history_closeout'}:
        if Path(args.root).resolve()!=Path(public['target_checkout']).resolve(): fail('target_mismatch','root','Use the explicit target checkout.')
        if args.action=='inspect':
            inspect_selected_source(public)
            return {'formal_exit':False,'result':call(public['source_ref'],'inspectTaskTarget',selection_input(public))}
        if args.action not in {'prepare','apply'} or not args.plan: fail('plan_required','plan','Prepare the AI-reviewed private plan before writing.')
        prepared=prepare(package_root,public,read(args.plan)) if args.action=='prepare' else read(args.plan)
        if prepared.get('public_input')!=public: fail('prepared_input_mismatch','plan','Apply exactly the reviewed read-only prepared plan.')
        if args.action=='prepare': return {'formal_exit':False,'result':prepared}
        inspect_selected_source(public)
        call(public['source_ref'],'previewMaintenance',prepared['public_plan'])
        path=Path(public['target_checkout'])/'.trellis/.runtime/guru-team/guru-maintain-legacy-task'/prepared['public_plan']['operation_id']/'checkpoint.json'
        if path.exists(): fail('operation_exists','recovery_ref','Resume the fixed original operation; do not recreate its backup.')
        prepared['owner_recovery_refs']={}
        store(path,prepared)
        return resume(package_root,path,prepared)
    path=Path(public['recovery_ref']); state=read(str(path)); root=Path(state['public_input']['target_checkout'])
    if root.resolve()!=Path(args.root).resolve(): fail('target_mismatch','root','Resume only the original target.')
    if public['profile']=='rollback':
        # Validate private postimages before public rollback can mutate either half.
        for owner,ref in state['owner_recovery_refs'].items(): owner_call(package_root,owner,{'profile':'legacy_control_restore_check','root':str(root),'recovery_ref':ref})
        if state['upstream_recovery_ref'] is not None:
            result=call(state['public_input']['source_ref'],'rollbackMaintenance',{'recovery_ref':state['upstream_recovery_ref']})
            if result['status']!='rolled_back': return {'exit_id':'resume_required','profile':'resume','recovery_ref':str(path)}
        for owner,ref in state['owner_recovery_refs'].items(): owner_call(package_root,owner,{'profile':'legacy_control_restore','root':str(root),'recovery_ref':ref})
        state['phase']='rolled_back'; store(path,state)
        return {'exit_id':'rolled_back','key':state['public_input']['key']}
    if state['phase']=='rolled_back': return {'exit_id':'rolled_back','key':state['public_input']['key']}
    if args.action=='observe':
        request=read(args.plan)
        result={'native':observe_native(root,request['native_argv'])}
        if state['public_input']['profile'] in {'convert','archive_resume'}: result['next_owner']=observe_native(root,request['next_owner_argv'])
        return {'formal_exit':False,'result':result}
    if args.action=='finalize':
        if state['phase']!='verification_required': fail('verification_required','phase','Complete public maintenance and exact original owner retirements.')
        review=read(args.review_input)
        # AI selects the route from actual observations; no status-to-success rule.
        observations={'native':observe_native(root,review['native_argv'])}
        if state['public_input']['profile'] in {'convert','archive_resume'}: observations['next_owner']=observe_native(root,review['next_owner_argv'])
        if any(v['returncode'] for v in observations.values()): fail('native_verification_failed','native','Repair the target native/next-owner entry before semantic finalization.')
        if review['observations']!=observations: fail('stale_native_observation','review_input','Review the current actual native and next-owner outputs.')
        output=review['output']; validate_json(output,package_root/'schemas/public-output.schema.json','output')
        expected='task_resumed' if state['public_input']['profile'] in {'convert','archive_resume'} else 'history_archived'
        if output['exit_id']!=expected: fail('route_mismatch','output','Use the profile-specific semantic result.')
        if expected=='task_resumed':
            current_ref=state.get('resumed_task',{}).get('task_ref',state['public_input']['task_ref'])
            current=json.loads(path_at(root,current_ref+'/task.json').read_text())
            if state['public_input']['profile']=='archive_resume' and state['resumed_task']['key']!={'task_id':current['id'],'lifecycle_generation':current['lifecycle_generation']}: fail('task_identity_mismatch','resumed_task','Use the actual public returned active Task key.')
            if current.get('schema_version')!='2.0' or output['task_id']!=current['id'] or output['lifecycle_generation']!=current['lifecycle_generation'] or output['task_ref']!=current_ref: fail('task_identity_mismatch','output','Read the actual converted Task identity.')
        elif output['key']!=state['public_input']['key'] or output['archive_ref']!=state['public_plan']['guard']['archive_ref']: fail('archive_identity_mismatch','output','Use the readable original archive identity.')
        state['phase']='verified'; state['terminal_output']=output; store(path,state)
        return output
    if state['phase']=='verified': return state['terminal_output']
    return resume(package_root,path,state)
