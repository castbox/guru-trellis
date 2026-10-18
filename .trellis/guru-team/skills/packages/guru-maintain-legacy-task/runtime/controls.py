"""Deterministic file facts used by the original legacy control owners."""
from __future__ import annotations
import base64
import json
import stat
from pathlib import Path
from runtime.io import CommandError

def fail(code, field, message):
    raise CommandError(code, field, message)

def path_at(root, ref):
    path = Path(ref)
    if path.is_absolute() or any(x in {'..', '.'} for x in path.parts):
        fail('invalid_path', 'control_ref', 'Use an exact target-relative path.')
    return Path(root) / path

def raw(path):
    if not path.exists(): return None
    if not path.is_file() or path.is_symlink(): fail('unsupported_control', str(path), 'Select a regular control file.')
    return {'content_base64':base64.b64encode(path.read_bytes()).decode(), 'mode':stat.S_IMODE(path.stat().st_mode)}

def preserved_source(root,state):
    plan=state['public_plan'];task_ref=state['public_input']['task_ref']
    active_ref=state.get('resumed_task',{}).get('task_ref',task_ref)
    ref=(plan['guard']['archive_ref']+'/task.json') if plan['kind']=='legacy_closeout' else active_ref+'/migration/source-task.json'
    source=next((a.get('source') for a in plan['actions'] if a['path']==task_ref+'/task.json'),None)
    if source is None:fail('preserved_source_missing','plan','Original Task preimage is required.')
    actual=raw(path_at(root,ref))
    if actual is None or any(actual[k]!=source[k] for k in actual):fail('preserved_source_mismatch','preserved_source_ref','Read actual public-preserved Task bytes before original-owner retirement.')
    if plan['kind']=='task_resume':
        archive_ref=task_ref+'/task.json'
        if raw(path_at(root,archive_ref))!=actual:fail('preserved_source_mismatch','task_ref','Keep the original archive bytes and mode readable.')
        return archive_ref
    return ref
