"""Opt-in native current shared/local controls and linked migration rehearsal.

Use the same three environment paths as test_495_migration_families.py and
prepare G8-current2 first. C4/C3/Bind create every control through actual old
installed owners; no task binding, ledger or session is fabricated.
"""
from pathlib import Path
import importlib.util
import json
import os
import shutil
import subprocess
import sys
_spec = importlib.util.spec_from_file_location('family_helpers', Path(__file__).with_name('test_495_migration_families.py'))
g = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(g)

def main():
    area = g.BASE / 'G8-linked-controls-portable'
    area.mkdir(exist_ok=True)
    primary = area / 'primary'
    linked = area / 'linked'
    if not primary.exists():
        shutil.copytree(g.BASE / 'G8-current2/repo', primary)
        g.run(primary, ['git', 'add', '.'])
        g.run(primary, ['git', 'commit', '-qm', 'native current task baseline'])
        g.run(primary, ['git', 'worktree', 'add', '-b', 'task/current-linked', str(linked), 'HEAD'])
        old = g.BASE / 'G8-current2/source'
        g.run(old, ['bash', str(old / 'trellis/presets/guru-team/scripts/bash/apply.sh'), '--repo', str(linked), '--platform', 'codex'])
    ref = next((p for p in (linked / '.trellis/tasks').glob('*/task.json') if p.parent.name.endswith('-selected'))).parent.relative_to(linked).as_posix()
    record = json.loads((linked / ref / 'task.json').read_text())
    task_id = record['id']
    generation = record['lifecycle_generation']

    def invoke(skill, public, owner=None):
        pkg = linked / '.trellis/guru-team/skills/packages' / skill
        args = ['bash', str(pkg / 'scripts/invoke.sh'), '--root', str(linked), '--input', '-']
        if owner:
            pp = area / 'bind-owner.json'
            g.write(pp, owner)
            args += ['--owner-result', str(pp)]
        env = {k: v for k, v in os.environ.items() if k not in ('CODEX_THREAD_ID', 'TRELLIS_CONTEXT_ID', 'PYTHONPATH')}
        env['TRELLIS_CONTEXT_ID'] = '495-current-linked'
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        r = subprocess.run(args, cwd=linked, env=env, input=json.dumps(public), capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
        return json.loads(r.stdout)
    identity = invoke('guru-establish-task-identity', {'profile': 'active_task', 'mode': 'standalone', 'task_id': task_id, 'task_ref': ref, 'lifecycle_generation': generation})
    assert identity['exit_id'] == 'identity_established', identity
    binding = invoke('guru-establish-task-branch-binding', {'profile': 'active_task', 'mode': 'standalone', 'action': 'establish', 'task_id': task_id, 'task_ref': ref, 'lifecycle_generation': generation, 'expected_status': 'planning'})
    print('binding', binding, flush=True)
    if binding['exit_id'] == 'selection_required':
        chosen = next((row for row in binding['candidates'] if row['branch_name'] == 'task/current-linked'))
        binding = invoke('guru-establish-task-branch-binding', {'profile': 'active_task', 'mode': 'standalone', 'action': 'establish', 'task_id': task_id, 'task_ref': ref, 'lifecycle_generation': generation, 'expected_status': 'planning', 'selected_candidate_id': chosen['candidate_id'], 'expected_candidate_head': chosen['head']})
    assert binding['exit_id'] == 'binding_established', binding
    checkout = invoke('guru-ensure-task-checkout', {'profile': 'active_task', 'mode': 'standalone', 'task_id': task_id, 'lifecycle_generation': generation})
    assert checkout['exit_id'] == 'checkout_resolved', checkout
    assert Path(checkout['checkout_path']).resolve() == linked.resolve(), checkout
    public = {'profile': 'rebind_missing_session', 'mode': 'standalone', 'task_id': task_id, 'lifecycle_generation': generation, 'continuation_id': '495-current-control-fixture'}
    owner = {**public, 'route': 'rebind', 'resume_target': 'phase-1', 'ai_review_gate': {'status': 'passed', 'summary': 'Reviewed native current task/source, actual unique linked checkout, C4 ownership and fresh planning continuation; no business behavior or external operation.'}}
    bound = invoke('guru-bind-task-session', public, owner)
    print('bound', bound, flush=True)
    assert bound['exit_id'] == 'session_rebound', bound
    common = Path(g.run(linked, ['git', 'rev-parse', '--path-format=absolute', '--git-common-dir']).strip())
    local = Path(g.run(linked, ['git', 'rev-parse', '--absolute-git-dir']).strip())
    paths = list((common / 'trellis').rglob('*.json'))
    print('control paths', [str(p.relative_to(common)) for p in paths], flush=True)
    g.write(area / 'owner-before.json', {'task_ref': ref, 'task_id': task_id, 'generation': generation, 'binding': binding, 'checkout': checkout, 'session': bound, 'common': str(common), 'local': str(local), 'control_paths': [str(p) for p in paths]})
    area = g.BASE / 'G8-linked-controls-portable'
    root = area / 'linked'
    primary = area / 'primary'
    facts = json.loads((area / 'owner-before.json').read_text())
    common = Path(facts['common'])
    local = Path(facts['local'])
    control_paths = [Path(p) for p in facts['control_paths']]
    task = root / facts['task_ref'] / 'task.json'
    before = {p: (p.read_bytes(), p.stat().st_mode & 511) for p in control_paths + [task]}
    python_pointers = [common / 'guru-team/python/active.json', local / 'guru-team/python/active.json']
    pointer_before = {p: (p.read_bytes(), p.stat().st_mode & 511) for p in python_pointers}
    primary_before = {p: (p.read_bytes(), p.stat().st_mode & 511) for p in [primary / facts['task_ref'] / 'task.json', primary / '.trellis/.version', primary / '.trellis/guru-team/extension.json']}
    plan = json.loads((g.BASE / 'G8-current2/plan.json').read_text())
    plan['controls'] = [{'location': 'common', 'path': p.relative_to(common).as_posix()} for p in control_paths]
    plan['workflow']['expected_sha256'] = g.digest(root / '.trellis/workflow.md')
    for row in plan['core_plan']['current_tasks']:
        row['expected_sha256'] = g.digest(root / row['task_ref'] / 'task.json')
    pp = area / 'plan.json'
    g.write(pp, plan)
    pub = {'profile': 'initial_upgrade', 'source_profile': 'guru0.7.0-family', 'target_source_ref': g.HEAD}
    result = g.public(root, {'profile': 'resume', 'recovery_ref': next((Path(facts['local']) / 'guru-team/install-upgrade').iterdir()).name}) if (root / '.trellis/.version').read_text().strip() == '0.7.0-castbox.3' else g.public(root, pub, pp)
    print('upgrade', result, flush=True)
    assert result['exit_id'] == 'upgraded', result
    for p, v in before.items():
        assert (p.read_bytes(), p.stat().st_mode & 511) == v, p
    for p, v in primary_before.items():
        assert (p.read_bytes(), p.stat().st_mode & 511) == v, p
    assert (python_pointers[0].read_bytes(), python_pointers[0].stat().st_mode & 511) == pointer_before[python_pointers[0]]
    assert python_pointers[1].is_file()

    def resume_binding():
        pkg = root / '.trellis/guru-team/skills/packages/guru-bind-task-session'
        public = {'profile': 'resume_current_task', 'mode': 'standalone', 'task_id': facts['task_id'], 'lifecycle_generation': facts['generation'], 'continuation_id': '495-current-control-fixture'}
        owner = {**public, 'route': 'resume', 'resume_target': 'phase-1', 'ai_review_gate': {'status': 'passed', 'summary': 'Native current task, unchanged shared branch/resource/session and unique linked checkout verified; resume consumes the retained current planning lifecycle without writing it.'}}
        op = area / 'resume-owner.json'
        g.write(op, owner)
        env = {k: v for k, v in os.environ.items() if k not in ('CODEX_THREAD_ID', 'TRELLIS_CONTEXT_ID', 'PYTHONPATH')}
        env['TRELLIS_CONTEXT_ID'] = '495-current-linked'
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        r = subprocess.run(['bash', str(pkg / 'scripts/invoke.sh'), '--root', str(root), '--input', '-', '--owner-result', str(op)], cwd=root, env=env, input=json.dumps(public), capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
        value = json.loads(r.stdout)
        assert value['exit_id'] == 'session_resumed', value
        return value
    current = resume_binding()
    print('current resumed', current, flush=True)
    for p, v in before.items():
        assert (p.read_bytes(), p.stat().st_mode & 511) == v, p
    rollback = g.public(root, {'profile': 'rollback', 'recovery_ref': result['recovery_ref']})
    print('rollback', rollback, flush=True)
    assert rollback == {'exit_id': 'rolled_back', 'installed_version': '0.7.0-guru.2'}, rollback
    for p, v in before.items():
        assert (p.read_bytes(), p.stat().st_mode & 511) == v, p
    for p, v in pointer_before.items():
        assert (p.read_bytes(), p.stat().st_mode & 511) == v, p
    for p, v in primary_before.items():
        assert (p.read_bytes(), p.stat().st_mode & 511) == v, p
    old = resume_binding()
    print('old resumed', old, flush=True)
    g.write(area / 'result.json', {'upgrade': result, 'rollback': rollback, 'native_before': facts['session'], 'current_after': current, 'old_after_rollback': old, 'control_paths': [p.relative_to(common).as_posix() for p in control_paths], 'task_and_controls': 'native writer bytes/modes preserved', 'primary': 'task/version/manifest and common runtime unchanged', 'linked_override': 'valid per-checkout pointer and exact restored on rollback (runtime cache identity may remain equal)'})
if __name__ == '__main__':
    main()
