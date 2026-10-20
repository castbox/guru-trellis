"""Single-checkout tools executor; all semantic decisions remain in the Skill."""
from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import uuid
from pathlib import Path

from runtime.io import CommandError, read_json
from runtime.schema import validate_json
from runtime.base_selection import repo, select_base, authority_checkout
from runtime.maintenance_transport import call, inspect_source


def legacy_owner(package):
    """Reuse the original Guru installation ownership and preimage executor."""
    directory = package.parent / 'guru-upgrade-installation/runtime'
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))
    spec = importlib.util.spec_from_file_location('tools_original_installation_owner', directory / 'owner.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def project_agents_target(plan, module):
    """Compose the existing Guru block into the public writer's first target."""
    for action in plan['actions']:
        if action.get('kind', 'file') != 'file' or action['path'] != 'AGENTS.md':
            continue
        target = action['target']
        content = None if target is None else base64.b64decode(target['content_base64'])
        rendered = module.render_agents_ai_first_principles(content)
        action['target'] = {'content_base64': base64.b64encode(rendered).decode('ascii'),
                            'sha256': hashlib.sha256(rendered).hexdigest(),
                            'mode': 0o644 if target is None else target['mode']}
    return plan


def selected_target(context, public):
    if public.get('checkout'):
        target = Path(public['checkout']).resolve()
        if repo(str(target)) != target:
            raise ValueError('Explicit checkout must be its exact Git root')
        return target
    facts = select_base(context, public.get('base_branch'), public.get('remote', 'origin'))
    return authority_checkout(context, facts['selected_base'], require_clean=False)


def source_identity(source, public, old):
    head = old.git(source, 'rev-parse', 'HEAD')
    if old.git(source, 'rev-parse', public['source_ref'] + '^{commit}') != head:
        raise ValueError('source_ref must resolve to the executing complete source HEAD')
    if public['dependency_mode'] == 'source_locked':
        old.formal_guru_source(source, public['source_ref'])
    return head


def source_tree_token(source, old):
    # A dirty local development source cannot be recovered from HEAD alone.
    # Persist one private equality token, never a file/hash audit bundle.
    paths = old.command(['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard', '--', 'trellis'], source).split('\0')
    digest = hashlib.sha256()
    for relative in sorted(set(paths) - {''}):
        path = source / relative
        if path.is_file():
            digest.update(relative.encode())
            digest.update(str(path.stat().st_mode & 0o777).encode())
            digest.update(path.read_bytes())
    return digest.hexdigest()


def upstream_source(public, descriptor):
    if descriptor.get('dependency_mode') != public['dependency_mode']:
        raise ValueError('Public dependency mode differs from the selected actual CLI/Core source')
    inspect_source(descriptor)
    return descriptor


def peers(root, old):
    raw = old.git(root, 'worktree', 'list', '--porcelain')
    return [Path(line[9:]).resolve() for line in raw.splitlines() if line.startswith('worktree ')]


def isolated_layout(root, old):
    # Tools must have their own physical store. Task-root aliases are upstream's concern.
    own = root / '.trellis'
    if own.is_symlink():
        raise ValueError('Whole-.trellis alias cannot provide isolated checkout tools')
    for other in peers(root, old):
        if other != root and (other / '.trellis').exists() and own.exists():
            if os.path.samefile(own, other / '.trellis'):
                raise ValueError('Selected checkout physically shares its tool store with a peer')


def peer_pointers(root, old):
    """Only runtime pointer facts; no peer Task or business-data index."""
    from runtime.bootstrap import active_pointer_path
    paths = set()
    common = Path(old.git(root, 'rev-parse', '--git-common-dir'))
    if not common.is_absolute():
        common = root / common
    paths.add(common.resolve() / 'guru-team/python/active.json')
    target_override = root / '.trellis/.runtime/guru-team/python/active.json'
    for other in peers(root, old):
        gitdir = Path(old.git(other, 'rev-parse', '--absolute-git-dir'))
        paths.add(gitdir / 'guru-team/python/active.json')
        if other != root:
            paths.add(other / '.trellis/.runtime/guru-team/python/active.json')
            paths.add(active_pointer_path(other))
    return {str(path): old.state(path) for path in sorted(paths) if path != target_override}


def unchanged_peers(root, cp, old):
    if peer_pointers(root, old) != cp['peer_pointers']:
        raise ValueError('A peer/common Python pointer changed; review before recovery')


def validate_tools_plan(root, public, plan, old):
    descriptor = upstream_source(public, plan['upstream_source'])
    prepared = plan['upstream_plan']
    if prepared.get('kind') != 'tools_install' or Path(prepared.get('target_root', '')).resolve() != root:
        raise ValueError('Frozen public operation must install tools in the selected exact checkout')
    workflow = prepared.get('guard', {}).get('workflow', {})
    if workflow.get('action') == 'install':
        source = old.source_root(Path(__file__).resolve().parent.parent)
        canonical = (source / 'trellis/workflows/guru-team/workflow.md').read_bytes()
        if public['dependency_mode'] == 'source_locked' and workflow.get('provider') != 'gh:castbox/guru-trellis/trellis#' + old.git(source, 'rev-parse', 'HEAD'):
            raise ValueError('Formal Guru workflow provider must bind the exact executing source commit')
        actions = [row for row in prepared['actions'] if row['path'] == '.trellis/workflow.md']
        import base64
        if (workflow.get('ownership') != 'custom' or workflow.get('template_id') != 'guru-team'
                or len(actions) != 1 or actions[0]['target'] is None
                or base64.b64decode(actions[0]['target']['content_base64']) != canonical):
            raise ValueError('Guru workflow must be the reviewed canonical custom workflow, not bundled native')
    return call(descriptor, 'previewMaintenance', prepared)


def inventory(package, root, public, descriptor, plan=None):
    old = legacy_owner(package)
    source = old.source_root(package)
    source_identity(source, public, old)
    isolated_layout(root, old)
    upstream_source(public, descriptor)
    manifest = old.old_manifest(root, source)
    hashes = old.old_paths(manifest, source, root)
    managed = []
    for path, digest in sorted(hashes.items()):
        if old.guru_owned(path):
            current = old.state(old.relative_file(root, path))
            managed.append({'path': path, 'previous_sha256': digest, **current})
    module = old.installer(source)
    selected = set(plan['selected_platforms']) if plan else set(manifest['install']['selected_platforms'])
    # The original installer owns projections, staging, manifests and sidecars.
    projections = module.managed_source_projections(root, root / '.trellis/guru-team', selected)
    paths = {path.as_posix() for path in module.managed_transaction_paths(root, root / '.trellis/guru-team', selected, None, tools_only=True)}
    paths |= {row['path'] for row in managed}
    paths |= {'.trellis/guru-team/extension.json', '.trellis/.runtime/guru-team/python/active.json'}
    paths |= {path + suffix for path in list(paths) if not path.startswith('.trellis/.runtime/') for suffix in ('.new', '.bak')}
    forbidden = [path for path in paths if path.startswith(('.trellis/tasks/', '.trellis/workspace/', '.trellis/agent-traces/'))]
    if forbidden:
        raise ValueError('Tools installer projection includes Task/history paths; revise original owner before execution')
    facts = {'root': str(root), 'installed_version': manifest['extension']['version'], 'managed': managed,
             'guru_paths': sorted(paths), 'guru_inventory': [
                 {'path': path, **old.state(old.relative_file(root, path)),
                  'target_sha256': old.state(projections[Path(path)])['sha256'] if Path(path) in projections else None}
                 for path in sorted(paths)], 'peer_pointers': peer_pointers(root, old),
             'public_tools': call(descriptor, 'inspectToolsTarget', {'root': str(root)})}
    if plan is not None:
        facts['public_preview'] = validate_tools_plan(root, public, plan, old)
        decisions = {row['path']: row for row in plan['guru_decisions']}
        if len(decisions) != len(plan['guru_decisions']):
            raise ValueError('Duplicate Guru managed path decision')
        allowed = {row['path'] for row in managed} | {path.as_posix() for path in projections if old.guru_owned(path.as_posix())}
        for path, decision in decisions.items():
            if path not in allowed:
                raise ValueError('Decision is outside actual old Guru ownership: ' + path)
            if decision['expected_sha256'] != old.state(old.relative_file(root, path))['sha256']:
                raise ValueError('Guru managed decision is stale: ' + path)
        for row in managed:
            if row['sha256'] is not None and row['sha256'] != row['previous_sha256'] and row['path'] not in decisions:
                raise ValueError('Review actual local Guru edit: ' + row['path'])
        previous_paths = {row['path'] for row in managed}
        for path, canonical in projections.items():
            relative = path.as_posix()
            current = old.state(old.relative_file(root, relative))
            if (old.guru_owned(relative) and relative not in previous_paths and current['sha256'] is not None
                    and current['sha256'] != old.state(canonical)['sha256'] and relative not in decisions):
                raise ValueError('Review actual unmanaged Guru projection edit: ' + relative)
        if any(old.relative_file(root, path).exists() for path in paths if path.endswith(('.new', '.bak'))):
            raise ValueError('Existing Guru sidecars require reconciliation before initial tools operation')
    return facts


def recovery_path(root, ref, old):
    if not re.fullmatch(r'[a-f0-9-]{36}', ref):
        raise ValueError('Use the exact original tools recovery reference')
    return Path(old.git(root, 'rev-parse', '--absolute-git-dir')) / 'guru-team/tools-upgrade' / ref


def save(root, recovery, cp, old):
    cp['baseline'] = old.current_baseline(root, cp)
    old.write_json(recovery / 'checkpoint.json', cp)


def begin(package, root, public, plan):
    old = legacy_owner(package)
    facts = inventory(package, root, public, plan['upstream_source'], plan)
    source = old.source_root(package)
    ref = str(uuid.uuid4())
    recovery = recovery_path(root, ref, old)
    upstream_ref = str(root / '.trellis/.runtime/guru-team/tools-upgrade' / ref / 'public' / (plan['upstream_plan']['operation_id'] + '.json'))
    cp = {'schema_version': '1.0', 'root': str(root), 'source': str(source),
          'source_ref': source_identity(source, public, old), 'source_token': source_tree_token(source, old), 'public': public, 'plan': plan,
          'phase': 'public', 'old_version': facts['installed_version'], 'old_managed': facts['managed'],
          'controls': {}, 'peer_pointers': facts['peer_pointers'], 'upstream_ref': upstream_ref}
    # Freeze once before the first public or Guru write. Resume never expands this set.
    cp['preimages'] = old.snapshot(root, recovery, set(facts['guru_paths']), {})
    save(root, recovery, cp, old)
    return recovery, cp


def check_source(package, root, cp, old):
    source = old.source_root(package)
    if cp['source'] != str(source) or cp['root'] != str(root):
        raise ValueError('Tools recovery belongs to another source or checkout')
    if source_identity(source, cp['public'], old) != cp['source_ref'] or source_tree_token(source, old) != cp['source_token']:
        raise ValueError('Tools recovery source identity or canonical content changed')
    upstream_source(cp['public'], cp['plan']['upstream_source'])
    isolated_layout(root, old)
    unchanged_peers(root, cp, old)


NATIVE_OPERATION_PROBE = r"""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path('.trellis/scripts').resolve()))
from common.delivery_schema import parse_task_v2
from common.delivery_operations import apply_operation
from common.runtime_contract import read_runtime_contract
contract=read_runtime_contract(Path('.trellis/workflow.md'))
record=dict(schema_version='2.0',id='tools-capability-probe',name='Tools capability probe',
 lifecycle_generation=0,source={'kind':'no_issue'},title='Isolated API input',description='',
 dev_type=None,scope=None,package=None,priority='P2',createdAt='',base_branch=None,branch=None,
 worktree_path=None,children=[],parent=None,relatedFiles=[],notes='',meta={},accepted_scope=None,
 deliveries=[],completion_results=[],closure_results=[])
parse_task_v2(record)
authority={'locator':'isolated-capability-input','revision':'not-business-authority'}
result=apply_operation(record,dict(api_version='1.0',operation='accept_scope',
 key={'task_id':record['id'],'lifecycle_generation':0},owner_role='task_scope',
 owner_id=contract['owners']['task_scope'],authority=authority),contract)
assert result['record']['accepted_scope']==authority
assert record['accepted_scope'] is None
print(json.dumps({'status':'passed','scope':'isolated-in-memory-public-operation'}))
"""


def validate_actual_target(root, old):
    runtime = root / '.trellis/guru-team/runtime'
    prefix = ['env', 'PYTHONDONTWRITEBYTECODE=1', 'PYTHONPATH=' + str(root / '.trellis/guru-team'),
              'bash', str(runtime / 'resolve-python.sh'), str(root), str(runtime)]
    result = json.loads(old.command(prefix + [
        '-m', 'runtime.validate', '--root', str(root), '--mode', 'installed', '--json'], root))
    if result.get('status') != 'passed':
        raise ValueError('Actual target installed runtime validation failed')
    # The real native selection must work, or explicitly classify supported old
    # state. A manifest/package pass alone is not an installed-tools success.
    native = subprocess.run(prefix + [str(root / '.trellis/scripts/get_context.py'), '--mode', 'continuation'],
                            cwd=root, text=True, capture_output=True)
    diagnostic = native.stdout + '\n' + native.stderr
    maintenance = re.search(r'^Error:.*maintenance_required', diagnostic, re.MULTILINE) is not None
    if native.returncode and not (maintenance and 'Traceback (most recent call last)' not in diagnostic):
        raise ValueError('Actual target native continuation failed without a supported maintenance diagnostic')
    operation = json.loads(old.command(prefix + ['-c', NATIVE_OPERATION_PROBE], root))
    if operation != {'status':'passed','scope':'isolated-in-memory-public-operation'}:
        raise ValueError('Actual target public operation capability probe failed')
    return {'installed':'passed','native':'maintenance_required' if maintenance else 'passed',
            'public_operation':'isolated_in_memory_passed'}


def canonical_reconciliation(root, cp, old):
    """Accept only the original installer's canonical sidecar resolution.

    The AI reviews that resolution before resume. This checks exact bytes/modes;
    it does not treat arbitrary later tool edits as a replacement backup anchor.
    """
    observed = old.current_baseline(root, cp)
    if observed == cp['baseline']:
        return True
    if cp['phase'] != 'preset':
        return False
    module = old.installer(Path(cp['source']))
    projections = module.managed_source_projections(root, root / '.trellis/guru-team', set(cp['plan']['selected_platforms']))
    for key, current in observed.items():
        previous = cp['baseline'][key]
        if current == previous:
            continue
        if not key.startswith('repo:'):
            return False
        relative = key[5:]
        if relative.endswith('.new') and current['sha256'] is None:
            base = Path(relative[:-4])
            if base not in projections or previous['sha256'] != old.state(projections[base])['sha256']:
                return False
            if old.state(old.relative_file(root, base.as_posix()))['sha256'] != previous['sha256']:
                return False
            continue
        if relative.endswith('.bak') and current['sha256'] is None:
            original = cp['preimages'].get('repo:' + relative[:-4])
            if original is None or previous != {name: original[name] for name in ('sha256', 'mode')}:
                return False
            continue
        canonical = projections.get(Path(relative))
        if canonical is None:
            return False
        expected = old.state(canonical)
        preimage = cp['preimages'][key]
        if current['sha256'] != expected['sha256'] or current['mode'] not in (expected['mode'], preimage['mode']):
            return False
    return True


def resume(package, root, recovery, cp):
    old = legacy_owner(package)
    check_source(package, root, cp, old)
    plan = cp['plan']
    if cp['phase'] == 'rolled_back':
        return rollback(package, root, recovery, cp)
    # No newer owned-path edits are adopted into a refreshed rollback anchor.
    if not canonical_reconciliation(root, cp, old):
        return {'exit_id': 'blocked', 'reason': 'owned_tools_changed_since_operation'}
    try:
        if cp['phase'] == 'public':
            if Path(cp['upstream_ref']).is_file():
                result = call(plan['upstream_source'], 'resumeMaintenance', {'recovery_ref': cp['upstream_ref']})
            else:
                result = call(plan['upstream_source'], 'applyMaintenance', {'plan': plan['upstream_plan'], 'state_dir': str(Path(cp['upstream_ref']).parent)})
            if result.get('status') != 'applied' or result.get('recovery_ref') != cp['upstream_ref']:
                raise ValueError('Public tools operation has not completed')
            cp['phase'] = 'guru'
            save(root, recovery, cp, old)
        if cp['phase'] == 'guru':
            decisions = {row['path']: row for row in plan['guru_decisions']}
            for row in cp['old_managed']:
                path = old.relative_file(root, row['path'])
                decision = decisions.get(row['path'])
                if decision and decision['action'] == 'preserve':
                    continue
                expected = decision['expected_sha256'] if decision else row['previous_sha256']
                observed = old.state(path)['sha256']
                if observed is not None and observed != expected:
                    raise ValueError('Old Guru managed bytes changed: ' + row['path'])
                path.unlink(missing_ok=True)
            previous_paths = {row['path'] for row in cp['old_managed']}
            for decision in plan['guru_decisions']:
                if decision['path'] not in previous_paths and decision['action'] == 'replace':
                    path = old.relative_file(root, decision['path'])
                    if old.state(path)['sha256'] not in (None, decision['expected_sha256']):
                        raise ValueError('Reviewed new Guru projection changed: ' + decision['path'])
                    path.unlink(missing_ok=True)
            old.relative_file(root, '.trellis/guru-team/extension.json').unlink(missing_ok=True)
            cp['phase'] = 'preset'
            save(root, recovery, cp, old)
        if cp['phase'] == 'preset':
            source = Path(cp['source'])
            module = old.installer(source)
            for row in sorted(cp['old_managed'], key=lambda row: len(Path(row['path']).parts), reverse=True):
                path = old.relative_file(root, row['path'])
                if not path.exists():
                    module.prune_empty_managed_skill_parents(root, path)
            preserved = {row['path'] for row in plan['guru_decisions'] if row['action'] == 'preserve'}
            result = module.install_assets(source / 'trellis/workflows/guru-team', root / '.trellis/guru-team', root,
                        set(plan['selected_platforms']), migration_preserved_paths=preserved,
                        python=sys.executable, checkout_local=True, tools_only=True,
                        tools_maintenance={'source': plan['upstream_source'], 'plan': plan['upstream_plan'], 'recovery_ref': cp['upstream_ref']})
            if (result['skill_packages']['status'] != 'ok' or result['overlays']['status'] != 'ok'
                    or result['skill_installed_validation'].get('returncode') != 0):
                raise ValueError('Guru preset has unresolved edits or sidecars')
        validate_actual_target(root, old)
        unchanged_peers(root, cp, old)
        cp['phase'] = 'complete'
        cp.pop('failure', None)
        save(root, recovery, cp, old)
        installed = json.loads((root / '.trellis/guru-team/extension.json').read_text())['extension']['version']
        return {'exit_id': 'tools_upgraded', 'installed_version': installed, 'recovery_ref': recovery.name,
                'unverified': [] if cp['public']['dependency_mode'] == 'source_locked' else ['formal_fork_source_lock']}
    except (ValueError, OSError, KeyError, SystemExit, CommandError) as exc:
        cp['failure'] = str(exc)[:300]
        save(root, recovery, cp, old)
        return {'exit_id': 'resume_required', 'profile': 'resume', 'recovery_ref': recovery.name}


def old_native_smoke(root, old):
    runtime = root / '.trellis/guru-team/runtime'
    script = root / '.trellis/scripts/get_context.py'
    if not script.is_file():
        raise ValueError('Restored target native context entry is missing')
    if (runtime / 'resolve-python.sh').is_file():
        argv = ['bash', str(runtime / 'resolve-python.sh'), str(root), str(runtime), str(script), '--json']
    else:
        argv = [sys.executable, str(script), '--json']
    old.command(argv, root)


def rollback(package, root, recovery, cp):
    old = legacy_owner(package)
    check_source(package, root, cp, old)
    if cp['phase'] == 'rolled_back':
        try:
            old_native_smoke(root, old)
        except (ValueError, OSError, old.MigrationError):
            return {'exit_id': 'resume_required', 'profile': 'resume', 'recovery_ref': recovery.name}
        return {'exit_id': 'rolled_back', 'installed_version': cp['old_version']}
    # Verify all Guru writes before public rollback can write either half.
    if old.current_baseline(root, cp) != cp['baseline']:
        return {'exit_id': 'blocked', 'reason': 'owned_tools_changed_since_operation'}
    if Path(cp['upstream_ref']).is_file():
        # The public owner checks real Task2/session3 compatibility before restoring.
        # Incompatible old tools therefore leave both public and Guru halves intact.
        result = call(cp['plan']['upstream_source'], 'rollbackMaintenance', {'recovery_ref': cp['upstream_ref']})
        if result.get('status') != 'rolled_back':
            return {'exit_id': 'blocked', 'reason': 'public_tools_rollback_incomplete'}
    old.restore(root, recovery, cp)
    expected = {key: {name: row[name] for name in ('sha256', 'mode')} for key, row in cp['preimages'].items()}
    if old.current_baseline(root, cp) != expected:
        raise ValueError('Guru tool restoration does not match its original preimages')
    unchanged_peers(root, cp, old)
    cp['phase'] = 'rolled_back'
    save(root, recovery, cp, old)
    return rollback(package, root, recovery, cp)


def run(package_root, metadata, argv):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--root', required=True)
    parser.add_argument('--input', required=True)
    parser.add_argument('--plan')
    parser.add_argument('--upstream-source')
    args = parser.parse_args(argv)
    public = read_json(args.input, 'input')
    profile = public.get('profile')
    if profile not in ('install', 'resume', 'rollback'):
        raise CommandError('schema_mismatch', 'input.profile', 'Use install, resume or rollback.')
    validate_json(public, package_root / ('schemas/public-' + profile + '-input.schema.json'), 'input')
    plan = read_json(args.plan, 'plan') if args.plan else None
    old = legacy_owner(package_root)
    try:
        context = repo(args.root)
        root = selected_target(context, public) if profile == 'install' else context
        role = metadata['runtime_role']
        if role == 'record':
            if profile != 'install' or plan is None:
                raise ValueError('Prepare requires install and explicit private-prepare input')
            validate_json(plan, package_root / 'schemas/private-prepare.schema.json', 'plan')
            source = old.source_root(package_root)
            source_identity(source, public, old)
            upstream_source(public, plan['upstream_source'])
            tools = plan['tools_input']
            if Path(tools['root']).resolve() != root:
                raise ValueError('Public tools input root differs from selected checkout')
            frozen = {key: value for key, value in plan.items() if key != 'tools_input'}
            frozen['upstream_plan'] = project_agents_target(
                call(plan['upstream_source'], 'prepareToolsInstallation', tools), old.installer(source))
            validate_json(frozen, package_root / 'schemas/private-plan.schema.json', 'plan')
            facts = inventory(package_root, root, public, frozen['upstream_source'], frozen)
            return {'plan': frozen, 'facts': facts}
        if role == 'preview':
            if profile != 'install':
                raise ValueError('Recovery reads its original checkpoint, not an initial preview')
            descriptor = plan['upstream_source'] if plan else (read_json(args.upstream_source, 'upstream_source') if args.upstream_source else None)
            if descriptor is None:
                raise ValueError('Supply matching complete CLI/Core source descriptor')
            if plan is not None:
                validate_json(plan, package_root / 'schemas/private-plan.schema.json', 'plan')
            return inventory(package_root, root, public, descriptor, plan)
        if profile == 'install':
            if plan is None:
                raise ValueError('Install requires the reviewed frozen private tools plan')
            validate_json(plan, package_root / 'schemas/private-plan.schema.json', 'plan')
            recovery, cp = begin(package_root, root, public, plan)
            result = resume(package_root, root, recovery, cp)
        else:
            if plan is not None or args.upstream_source:
                raise ValueError('Recovery consumes only its original reference, not a replacement plan')
            recovery = recovery_path(root, public['recovery_ref'], old)
            cp = json.loads((recovery / 'checkpoint.json').read_text())
            validate_json(cp, package_root / 'schemas/private-recovery.schema.json', 'recovery')
            result = rollback(package_root, root, recovery, cp) if profile == 'rollback' else resume(package_root, root, recovery, cp)
        validate_json(result, package_root / ('schemas/public-' + result['exit_id'] + '-output.schema.json'), 'output')
        return result
    except (ValueError, OSError, KeyError, old.MigrationError, CommandError) as exc:
        if metadata['runtime_role'] != 'invoke':
            raise CommandError('schema_mismatch', 'tools', 'Read-only tools preparation blocked: ' + str(exc)[:300])
        return {'exit_id': 'blocked', 'reason': str(exc)[:300] or 'tools_operation_blocked'}
