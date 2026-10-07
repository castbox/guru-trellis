"""Opt-in grouped normal-installation migration rehearsal.

Set TRELLIS_495_FAMILIES_ROOT to an isolated temporary output directory,
TRELLIS_FIXED_FORK_SOURCE to the built candidate and TRELLIS_495_CORE_SOURCE
 to a local Git source with the historical refs. Run this script with optional
G1..G8 selectors. Historical sources build offline and their actual installers
create the before state. No business checkout is copied. This local candidate
matrix is separate from formal source_locked/provider release acceptance.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import unittest
if any((not os.environ.get(key) for key in ('TRELLIS_495_FAMILIES_ROOT', 'TRELLIS_FIXED_FORK_SOURCE', 'TRELLIS_495_CORE_SOURCE'))):
    raise unittest.SkipTest('Explicit isolated output, built Fork and historical core source are required; no family migration proof.')
SOURCE = Path(__file__).resolve().parents[4]
BASE = Path(os.environ['TRELLIS_495_FAMILIES_ROOT']).resolve()
FORK = Path(os.environ['TRELLIS_FIXED_FORK_SOURCE']).resolve() / 'packages/cli/dist/cli/index.js'
CORE_SOURCE = Path(os.environ['TRELLIS_495_CORE_SOURCE']).resolve()
PACKAGE = SOURCE / 'trellis/skills/guru-team/packages/guru-upgrade-installation'
HEAD = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=SOURCE, text=True).strip()
spec = importlib.util.spec_from_file_location('helpers', SOURCE / 'trellis/skills/guru-team/tests/test_495_migration_lifecycle.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
GROUPS = [('G1', 'v0.6.5-guru.1', '065'), ('G2', 'v0.6.5-guru.3', '065'), ('G3', 'v0.6.5-guru.4', '065'), ('G4', 'v0.6.5-guru.7', '065'), ('G5', 'v0.6.15-guru.1', '0615'), ('G6', 'v0.6.16-guru.1', '0616'), ('G7', 'v0.6.17-guru.2', '0617'), ('G8', 'v0.7.0-guru.1', '070'), ('G6-core17', '29954796d26dda59a57aede400bbcb1347e619df', '0617'), ('G7-config', 'v0.6.17-guru.1', '0617'), ('G8-current2', '11ef591ceb454041540721d44bcbb72e66b0f22e', '0702')]

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None

def write(p, v):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(v, indent=2) + '\n')

def run(root, args, payload=None):
    env = {k: v for k, v in os.environ.items() if k not in ('CODEX_THREAD_ID', 'TRELLIS_CONTEXT_ID', 'PYTHONPATH')}
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    r = subprocess.run(args, cwd=root, env=env, input=json.dumps(payload) if payload else None, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(str(args[:3]) + ' ' + r.stderr[-1500:] + ' ' + r.stdout[-500:])
    return r.stdout

def public(root, value, plan=None, script='invoke.sh'):
    args = ['bash', str(PACKAGE / 'scripts' / script), '--root', str(root), '--input', '-']
    if plan:
        args += ['--plan', str(plan), '--fork', str(FORK)]
    return json.loads(run(root, args, value))

def prepare_core(name, ref):
    path = BASE / ('core-' + name)
    if not path.exists():
        run(BASE, ['git', 'clone', '--shared', '--no-checkout', str(CORE_SOURCE), str(path)])
        run(path, ['git', 'checkout', '--detach', ref])
        run(path, ['pnpm', 'install', '--offline', '--frozen-lockfile', '--ignore-scripts'])
        run(path, ['pnpm', 'build'])

def group(name, tag, core):
    area = BASE / name
    area.mkdir(exist_ok=True)
    old = area / 'source'
    root = area / 'repo'
    if not old.exists():
        run(BASE, ['git', 'clone', '--shared', '--no-checkout', str(SOURCE), str(old)])
        run(old, ['git', 'checkout', '--detach', tag])
    run(old, ['git', 'remote', 'set-url', 'origin', 'https://github.com/castbox/guru-trellis.git'])
    if not (root / '.git/fixture-ready').exists():
        root.mkdir(exist_ok=True)
        run(root, ['git', 'init', '-q', '-b', 'main'])
        run(root, ['git', 'config', 'user.name', 'Fixture'])
        run(root, ['git', 'config', 'user.email', 'fixture@example.invalid'])
        init = ['node', str(BASE / ('core-' + core) / 'packages/cli/dist/cli/index.js'), 'init', '--codex', '-y', '--force']
        if not core.startswith('070'):
            init += ['-u', 'fixture']
        run(root, init)
        shutil.copy2(old / 'trellis/workflows/guru-team/workflow.md', root / '.trellis/workflow.md')
        (root / 'business.txt').write_text('business baseline\n')
        (root / '.trellis/config.yaml').write_text('task_auto_commit: false\nfixture_setting: preserved\n')
        (root / 'AGENTS.md').write_text('# Fixture business rules\nPreserve this paragraph.\n')
        run(old, ['bash', str(old / 'trellis/presets/guru-team/scripts/bash/apply.sh'), '--repo', str(root), '--platform', 'codex'])
        run(root, ['python3', str(root / '.trellis/scripts/task.py'), 'create', 'Fixture task', '--slug', 'selected', '--description', 'Retain fixture business work'])
        run(root, ['git', 'add', '.'])
        run(root, ['git', 'commit', '-qm', 'normal legacy installation and native task'])
        (root / 'business.txt').write_text('ordinary uncommitted business work\n')
        (root / 'unrelated.txt').write_text('ordinary untracked business work\n')
        (root / '.git/fixture-ready').write_text('normal installer/task setup complete\n')
    manifest = json.loads((root / '.trellis/guru-team/extension.json').read_text())
    installed = manifest['extension']['version']
    actual_core = (root / '.trellis/.version').read_text().strip()
    task = next((p for p in (root / '.trellis/tasks').glob('*/task.json') if p.parent.name.endswith('-selected')))
    ref = task.parent.relative_to(root).as_posix()
    record = json.loads(task.read_text())
    iscurrent = 'lifecycle_generation' in record and 'source' in record
    cp = {'schema_version': '1.0', 'target_version': '0.7.0-castbox.3', 'tasks': [], 'current_tasks': [], 'deferred_tasks': [], 'file_decisions': []}
    if iscurrent:
        cp['current_tasks'] = [{'task_ref': ref, 'expected_sha256': digest(task)}]
    else:
        cp['tasks'] = [{'task_ref': ref, 'expected_sha256': digest(task), 'record': h.reviewed_projection(record, {'kind': 'no_issue'})}]
    for other in (root / '.trellis/tasks').glob('*/task.json'):
        if other == task:
            continue
        value = json.loads(other.read_text())
        kind = 'current_tasks' if 'lifecycle_generation' in value and 'source' in value else 'deferred_tasks'
        cp[kind].append({'task_ref': other.parent.relative_to(root).as_posix(), 'expected_sha256': digest(other)})
    coreplan = area / 'core-plan.json'
    write(coreplan, cp)
    args = ['node', str(FORK), 'migrate', '--from', actual_core, '--plan', str(coreplan), '--dry-run']
    first = json.loads(run(root, args))
    cp['file_decisions'] = [{'path': p, 'action': 'preserve' if p == 'AGENTS.md' else 'remove' if p.endswith('/workspace-memory.md') or p in {'.trellis/scripts/add_session.py', '.trellis/scripts/common/developer.py', '.trellis/scripts/get_developer.py', '.trellis/scripts/init_developer.py'} else 'replace', 'expected_sha256': digest(root / p)} for p in first['conflicts']]
    retired = {f'.{p}/skills/trellis-meta/references/local-architecture/workspace-memory.md' for p in ('agents', 'claude', 'cursor')} | {'.trellis/scripts/add_session.py', '.trellis/scripts/common/developer.py', '.trellis/scripts/get_developer.py', '.trellis/scripts/init_developer.py'}
    hashes = json.loads((root / '.trellis/.template-hashes.json').read_text())['hashes']
    for p in sorted(retired & set(hashes)):
        if (root / p).is_file() and p not in {r['path'] for r in cp['file_decisions']}:
            cp['file_decisions'].append({'path': p, 'action': 'remove', 'expected_sha256': digest(root / p)})
    write(coreplan, cp)
    reviewed = json.loads(run(root, args))
    assert not reviewed['conflicts'], reviewed
    pub = {'profile': 'initial_upgrade', 'source_profile': 'guru0.6-family' if installed.startswith('0.6.') else 'guru0.7.0-family', 'target_source_ref': HEAD}
    plan = {'core_plan': cp, 'dependency_mode': 'local_candidate', 'selected_platforms': ['codex'], 'guru_decisions': [], 'controls': [], 'workflow': {'provider_ref': HEAD, 'action': 'replace', 'expected_sha256': digest(root / '.trellis/workflow.md')}}
    pp = area / 'plan.json'
    write(pp, plan)
    before = {str(p.relative_to(root)): (p.read_bytes(), p.stat().st_mode & 511) for p in [root / 'business.txt', root / 'unrelated.txt', root / '.trellis/config.yaml', root / '.trellis/guru-team/config.yml', task]}
    status = run(root, ['git', 'status', '--porcelain=v1', '--untracked-files=all'])
    facts = public(root, pub, pp, 'preview.sh')
    assert facts.get('status') == 'preview', facts
    assert status == run(root, ['git', 'status', '--porcelain=v1', '--untracked-files=all'])
    write(area / 'preview.json', facts)
    result = public(root, pub, pp)
    write(area / 'initial.json', result)
    if result['exit_id'] != 'upgraded':
        checkpoint = json.loads((root / '.git/guru-team/install-upgrade' / result['recovery_ref'] / 'checkpoint.json').read_text()) if 'recovery_ref' in result else {}
        raise RuntimeError(name + ' ' + str(result) + ' ' + str(checkpoint.get('failure')))
    assert result['installed_version'] == '0.7.0-guru.3'
    for p in ['business.txt', 'unrelated.txt', '.trellis/guru-team/config.yml']:
        assert ((root / p).read_bytes(), (root / p).stat().st_mode & 511) == before[p], p
    assert 'fixture_setting: preserved' in (root / '.trellis/config.yaml').read_text()
    assert 'task_auto_commit: false' in (root / '.trellis/config.yaml').read_text()
    if iscurrent:
        assert (task.read_bytes(), task.stat().st_mode & 511) == before[ref + '/task.json']
    rollback = public(root, {'profile': 'rollback', 'recovery_ref': result['recovery_ref']})
    assert rollback == {'exit_id': 'rolled_back', 'installed_version': installed}, rollback
    assert (root / '.trellis/.version').read_text().strip() == actual_core
    assert json.loads((root / '.trellis/guru-team/extension.json').read_text()) == manifest
    for p, v in before.items():
        assert ((root / p).read_bytes(), (root / p).stat().st_mode & 511) == v, p
    smoke = run(root, ['python3', str(root / '.trellis/scripts/get_context.py'), '--json'])
    json.loads(smoke)
    row = {'group': name, 'tag': tag, 'source_version': installed, 'source_core': actual_core, 'source_schema': manifest['schema_version'], 'task_mode': 'current_preserved' if iscurrent else 'legacy_converted', 'upgrade': result, 'rollback': rollback, 'old_runtime_smoke': 'passed', 'preservation': 'bytes/modes and dirty/untracked passed', 'dependency_mode': 'local_candidate'}
    write(area / 'result.json', row)
    print(json.dumps(row), flush=True)

def custom_preservation():
    area = BASE / 'G1-custom-bash'
    area.mkdir(exist_ok=True)
    root = area / 'repo'
    if not root.exists():
        shutil.copytree(BASE / 'G1/repo', root)
    target = root / '.trellis/guru-team/scripts/bash/check-env.sh'
    target.write_text('#!/usr/bin/env bash\n# locally customized companion\n')
    target.chmod(416)
    unknown = root / '.trellis/guru-team/scripts/custom-notes/README.md'
    unknown.parent.mkdir(parents=True, exist_ok=True)
    unknown.write_text('unknown local content preserved\n')
    unknown.chmod(416)
    config = root / '.trellis/guru-team/config.yml'
    config.write_text(config.read_text() + '\nfixture_private_setting: preserve\n')
    plan = json.loads((BASE / 'G1/plan.json').read_text())
    relative = target.relative_to(root).as_posix()
    plan['guru_decisions'] = [{'path': relative, 'action': 'preserve', 'expected_sha256': digest(target)}]
    for row in plan['core_plan']['tasks'] + plan['core_plan']['deferred_tasks']:
        row['expected_sha256'] = digest(root / row['task_ref'] / 'task.json')
    plan['workflow']['expected_sha256'] = digest(root / '.trellis/workflow.md')
    plan_path = area / 'plan.json'
    write(plan_path, plan)
    before = {p: (p.read_bytes(), p.stat().st_mode & 511) for p in (target, unknown, config)}
    result = public(root, {'profile': 'initial_upgrade', 'source_profile': 'guru0.6-family', 'target_source_ref': HEAD}, plan_path)
    assert result['exit_id'] == 'upgraded', result
    manifest = json.loads((root / '.trellis/guru-team/extension.json').read_text())
    assert relative not in manifest['install']['managed_assets']
    for path, value in before.items():
        assert (path.read_bytes(), path.stat().st_mode & 511) == value, path
    reapply = subprocess.run(['bash', str(SOURCE / 'trellis/presets/guru-team/scripts/bash/apply.sh'), '--repo', str(root), '--platform', 'codex', '--json'], cwd=SOURCE, capture_output=True, text=True)
    assert reapply.returncode == 2, reapply.stderr
    assert json.loads(reapply.stdout)['skill_packages']['status'] == 'conflict'
    for path, value in before.items():
        assert (path.read_bytes(), path.stat().st_mode & 511) == value, path
    pending = Path(str(target) + '.new')
    assert pending.read_bytes() == (SOURCE / 'trellis/workflows/guru-team/scripts/bash/check-env.sh').read_bytes()
    pending.unlink()
    rollback = public(root, {'profile': 'rollback', 'recovery_ref': result['recovery_ref']})
    assert rollback == {'exit_id': 'rolled_back', 'installed_version': '0.6.5-guru.1'}, rollback
    for path, value in before.items():
        assert (path.read_bytes(), path.stat().st_mode & 511) == value, path
    write(area / 'result.json', {'upgrade': result, 'ordinary_reapply': 'conflict_with_custom_bytes_modes_preserved', 'rollback': rollback, 'unknown_content_directory': 'preserved', 'config': 'preserved'})

def preserved_work_during_pause():
    area = BASE / 'G8-preserved-new-work'
    area.mkdir(exist_ok=True)
    root = area / 'repo'
    if not root.exists():
        shutil.copytree(BASE / 'G8-current2/repo', root)
    companion = '.trellis/guru-team/scripts/bash/check-env.sh'
    skill = '.codex/skills/guru-check-task/SKILL.md'
    (root / companion).write_text('#!/usr/bin/env bash\n# customization before migration\n')
    (root / skill).write_text((root / skill).read_text() + '\nLocal check preference before upgrade.\n')
    plan = json.loads((BASE / 'G8-current2/plan.json').read_text())
    plan['guru_decisions'] = [{'path': path, 'action': 'preserve', 'expected_sha256': digest(root / path)} for path in (companion, skill)]
    plan_path = area / 'plan.json'
    write(plan_path, plan)
    initial = public(root, {'profile': 'initial_upgrade', 'source_profile': 'guru0.7.0-family', 'target_source_ref': HEAD}, plan_path)
    assert initial['exit_id'] == 'resume_required', initial
    pending = Path(str(root / skill) + '.new')
    assert pending.is_file()
    newer = b'#!/usr/bin/env bash\n# new user customization during pause\n'
    (root / companion).write_bytes(newer)
    (root / skill).write_bytes(pending.read_bytes())
    pending.unlink()
    resumed = public(root, {'profile': 'resume', 'recovery_ref': initial['recovery_ref']})
    assert resumed['exit_id'] == 'upgraded', resumed
    assert (root / companion).read_bytes() == newer
    rolled = public(root, {'profile': 'rollback', 'recovery_ref': initial['recovery_ref']})
    assert rolled == {'exit_id': 'blocked', 'reason': 'business_work_since_migration'}, rolled
    assert (root / companion).read_bytes() == newer
    write(area / 'result.json', {'initial': initial, 'resumed': resumed, 'rollback': rolled, 'new_companion_bytes': 'preserved'})
def preserved_core_work_during_partial_pause():
    for kind, target in (('core', 'AGENTS.md'), ('workflow', '.trellis/workflow.md')):
        area = BASE / ('G8-preserved-partial-pause-' + kind)
        area.mkdir(exist_ok=True)
        root = area / 'repo'
        shutil.copytree(BASE / 'G8-current2/repo', root)
        skill = '.codex/skills/guru-check-task/SKILL.md'
        (root / skill).write_text((root / skill).read_text() + '\nLocal check preference before migration.\n')
        plan = json.loads((BASE / 'G8-current2/plan.json').read_text())
        plan['guru_decisions'] = [{'path': skill, 'action': 'preserve', 'expected_sha256': digest(root / skill)}]
        plan['workflow']['provider_ref'] = HEAD
        if kind == 'workflow':
            plan['workflow']['action'] = 'preserve'
        else:
            assert any(row['path'] == target and row['action'] == 'preserve' for row in plan['core_plan']['file_decisions'])
        plan_path = area / 'plan.json'
        write(plan_path, plan)
        initial = public(root, {'profile': 'initial_upgrade', 'source_profile': 'guru0.7.0-family', 'target_source_ref': HEAD}, plan_path)
        assert initial['exit_id'] == 'resume_required', initial
        newer = (root / target).read_bytes() + b'\n# Normal new business rule during migration pause.\n'
        (root / target).write_bytes(newer)
        resumed = public(root, {'profile': 'resume', 'recovery_ref': initial['recovery_ref']})
        assert resumed['exit_id'] == 'resume_required', resumed
        assert (root / target).read_bytes() == newer
        rolled = public(root, {'profile': 'rollback', 'recovery_ref': initial['recovery_ref']})
        assert rolled == {'exit_id': 'blocked', 'reason': 'business_work_since_migration'}, rolled
        assert (root / target).read_bytes() == newer
        write(area / 'result.json', {'initial': initial, 'resumed': resumed, 'rollback': rolled, 'preserved_path': target, 'new_bytes': 'retained'})

if __name__ == '__main__':
    BASE.mkdir(parents=True, exist_ok=True)
    requested = set(sys.argv[1:])
    run_custom = 'custom' in requested
    run_new_work = 'new-work' in requested
    run_partial_pause = 'partial-pause' in requested
    requested.difference_update({'custom', 'new-work', 'partial-pause'})
    for name, ref in [('065', 'v0.6.5'), ('0615', 'v0.6.15'), ('0616', 'v0.6.16'), ('0617', 'v0.6.17'), ('070', '9c36002a324c16a09a85b6aa5a380b74aabf801f'), ('0702', '8868c47c45fa1a9fa8f60fe30d641f70ff5c6ba1')]:
        if any(((not requested and (not run_custom) and (not run_new_work) and (not run_partial_pause) or row[0] in requested) and row[2] == name for row in GROUPS)):
            prepare_core(name, ref)
    for row in GROUPS:
        if not requested and (not run_custom) and (not run_new_work) and (not run_partial_pause) or row[0] in requested:
            try:
                group(*row)
            except Exception as exc:
                print(row[0] + ' FAILED ' + str(exc), flush=True)
                sys.exit(1)
    if run_custom:
        custom_preservation()
    if run_new_work:
        preserved_work_during_pause()
    if run_partial_pause:
        preserved_core_work_during_partial_pause()
