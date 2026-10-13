"""Production owner staging through the reviewed installed public Delivery API.

This is post-owner transport evidence. The case's semantic judgment is supplied
by its existing owner fixture; this adapter cannot establish native AI review.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from adapters.eval.eval_constants import OWNER_INPUT
from adapters.eval.fixture_io import bind_owner_result_argument, bind_task_commit_candidate_argument, run_git
from adapters.eval.owner_runtime import compose_production_fixture_runtime, compose_production_owner_command_runtime, load_package_owner_runtime
from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
from runtime.io import project_intermediate_receipt
from runtime.task_lifecycle import BranchBindingStore, TaskLifecycleKey, inspect_repository


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    return path


def wrapper(fixture, skill, script, args, *, formal=False, root_argument=True):
    package = fixture / '.trellis/guru-team/skills/packages' / skill
    selectors = ['--root', str(fixture)] if root_argument else []
    process = subprocess.run([str(package / 'scripts' / script), *selectors, *args, '--json'],
                             cwd=fixture, text=True, capture_output=True)
    if process.returncode:
        raise ValueError(f'{skill}/{script}: {process.stdout or process.stderr}')
    value = json.loads(process.stdout)
    return value if formal else project_intermediate_receipt(value, package.parents[1] / 'schemas')


def installed_task(fixture, context_id, task_id="current"):
    # Load only a real installation/template directory selected by the caller.
    scripts = fixture / '.trellis/scripts'
    if not (scripts / 'common/delivery_store.py').is_file():
        selected = Path(os.environ.get('GURU_UPSTREAM_DELIVERY_SCRIPTS', ''))
        if not (selected / 'common/delivery_store.py').is_file():
            raise ValueError('Production Delivery eval requires the reviewed installed upstream candidate; set GURU_UPSTREAM_DELIVERY_SCRIPTS. No model or source fallback is supported.')
        shutil.copytree(selected, scripts, dirs_exist_ok=True)
    command = [sys.executable, '-B', str(scripts / 'task.py'), 'create', 'Production Delivery eval',
               '--description', 'One real Task and independent Delivery planning', '--slug', task_id,
               '--task-id', task_id, '--schema-version', '2.0', '--source-json', '{"kind":"no_issue"}',
               '--base-branch', 'main', '--no-start']
    created = subprocess.run(command, cwd=fixture, text=True, capture_output=True,
                             env={**os.environ, 'TRELLIS_CONTEXT_ID': context_id})
    if created.returncode:
        raise ValueError('Installed Task creation failed: ' + created.stderr)
    task, = [p.parent for p in (fixture / '.trellis/tasks').glob('*/task.json')
             if json.loads(p.read_text()).get('id') == task_id]
    return task


def seed_delivery(fixture, context_id):
    (fixture / '.trellis/guru-team/config.yml').write_text('workspace_mode: current\n')
    task = installed_task(fixture, context_id)
    BranchBindingStore(inspect_repository(fixture)).establish(TaskLifecycleKey('current', 0), 'eval/current')
    ref = task.relative_to(fixture).as_posix()
    task.joinpath('prd.md').write_text('# Whole Task\n\n## R1. Production eval\n\nCurrent accepted scope.\n')
    projection = DeliveryProjection(fixture, ref)
    scope = authority_ref(task / 'prd.md', fixture)
    projection.scope(scope)
    public = {'profile': 'delivery_creation', 'mode': 'workflow', 'task_ref': ref,
              'task_key': {'task_id': 'current', 'lifecycle_generation': 0},
              'continuation_id': 'production-owner-delivery', 'action': 'create',
              'scope_ref': {'authority': scope, 'anchors': ['R1. Production eval']}, 'delivery_profile': 'pull_request'}
    owner = {'typed_exit': 'created', 'reason': 'The existing case owns one independently deliverable slice.'}
    result = wrapper(fixture, 'guru-create-delivery', 'invoke.sh',
                     ['--input', str(write(fixture / '.trellis/.runtime/guru-team/evals/create.json', public)),
                      '--owner-result', str(write(fixture / '.trellis/.runtime/guru-team/evals/create-owner.json', owner))], formal=True)
    if result['exit_id'] != 'created':
        raise ValueError('Delivery Creation did not establish the selected public identity: ' + str(result))
    key = result['delivery_key']
    directory = projection.planning_directory(key)
    for name, content in {'prd.md': '# Delivery PRD\n\nR1. Production eval\n',
                          'design.md': '# Design\n\n## Docs SSOT Plan\n\nStrategy: ssot_first.\n',
                          'implement.md': '# Implement\n\nExecute applicable real public owner wrappers.\n',
                          'implement.jsonl': '', 'check.jsonl': ''}.items():
        (directory / name).write_text(content)
    (fixture / 'docs').mkdir(exist_ok=True)
    (fixture / 'docs/requirements.md').write_text('# Requirements\n\nThe public wrapper owns the production eval boundary.\n')
    (fixture / 'src').mkdir(exist_ok=True)
    (fixture / 'src/production-eval.txt').write_text('baseline\n')
    # Actual lifecycle binding owns checkout identity. It is not a fabricated Task field.
    run_git(fixture, 'add', '.')
    run_git(fixture, 'commit', '-qm', 'stage real production Delivery planning')
    return task, key, projection


def planning(runtime, fixture, task, key, exit_id):
    from adapters.eval.production_fixtures import production_planning_input
    path = production_planning_input(runtime, fixture, task, exit_id)
    value = json.loads(path.read_text())
    if exit_id == 'approved':
        value['consumer'] = {'kind': 'workflow', 'id': 'phase-1-delivery-activation'}
        write(path, value)
    ref = task.relative_to(fixture).as_posix()
    recorded = wrapper(fixture, 'guru-approve-task-plan', 'record-planning-approval.sh',
                       ['--task', ref, '--delivery-key', json.dumps(key), '--input', str(path)])
    checked = wrapper(fixture, 'guru-approve-task-plan', 'check-planning-approval.sh',
                      ['--task', ref, '--delivery-key', json.dumps(key)])
    return recorded, checked


def final_architecture(fixture, task, key):
    """Execute fixture-owned final assessment; this is transport, not AI proof."""
    package = fixture / '.trellis/guru-team/skills/packages/guru-maintain-architecture-baseline'
    public = json.loads((package / 'examples/public-input-candidate-assessment-3.0.json').read_text())
    projection = DeliveryProjection(fixture, task.relative_to(fixture).as_posix())
    directory = projection.planning_directory(key)
    public.pop('candidate')
    public.update(schema_version='delivery-1.0', profile='delivery_task_impact_sync',
                  source_exit='pass', task_locator=task.relative_to(fixture).as_posix(),
                  delivery_key=key, planning_root=projection.resolve(key)['planning_root'],
                  planning_purpose='final_plan',
                  design_locator=(directory / 'design.md').relative_to(fixture).as_posix(),
                  freshness_identity='sha256:' + hashlib.sha256((directory / 'design.md').read_bytes()).hexdigest())
    constitution = fixture / public['constitution']['authority_locator']
    constitution.parent.mkdir(parents=True, exist_ok=True)
    constitution.write_text('Current production fixture constitution.\n')
    owner = {name: copy.deepcopy(public[name]) for name in (
        'schema_version', 'profile', 'mode', 'continuation_id', 'stage', 'task_locator',
        'baseline', 'constitution', 'project_contract', 'freshness_identity',
        'planning_purpose', 'delivery_key', 'planning_root')}
    owner.update(input_sha256=hashlib.sha256(json.dumps(public, ensure_ascii=False,
                 sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
                 typed_exit='baseline_current', baseline_identity=public['baseline']['identity'],
                 constitution_identity=public['constitution']['identity'],
                 impact_kind='no_architecture_impact', impact_reason='Fixture retains existing transport owners.',
                 promotion_state='no_change',
                 consumer={'kind': 'workflow', 'id': 'guru-architecture-baseline-current-router'},
                 ai_review_gate={'status': 'passed', 'reviewed_scope': 'Production fixture transport',
                                 'evidence_summary': 'Existing fixture decision only.', 'findings': [],
                                 'conclusion': 'No native AI assessment is claimed.'})
    invocation = json.dumps({'public_input': public, 'owner_result': owner}, ensure_ascii=False)
    output = wrapper(fixture, package.name, 'invoke.sh', ['--invocation', invocation], formal=True, root_argument=False)
    if output['exit_id'] != 'baseline_current' or output.get('planning_purpose') != 'final_plan':
        raise ValueError('Actual final Architecture producer did not yield the required continuation.')
    return {name: output[name] for name in ('planning_purpose', 'freshness_identity',
            'baseline_identity', 'constitution_identity', 'constitution_status', 'impact_kind', 'promotion_state')}


def activate(runtime, fixture, task, key):
    recorded, checked = planning(runtime, fixture, task, key, 'approved')
    ref = task.relative_to(fixture).as_posix()
    public = {'profile': 'delivery_initial_review', 'mode': 'workflow', 'task_ref': ref,
              'source_exit': 'baseline_current', 'delivery_key': key,
              'architecture_assessment': final_architecture(fixture, task, key)}
    approved = wrapper(fixture, 'guru-approve-task-plan', 'invoke.sh',
                       ['--input', str(write(fixture / '.trellis/.runtime/guru-team/evals/approval.json', public)),
                        '--owner-result', checked['artifact_path']], formal=True)
    public = {'profile': 'delivery_activation', 'mode': 'workflow', 'task_ref': ref, 'delivery_key': key,
              'planning_result_id': approved['planning_result_id'], 'action': 'activate'}
    owner = {'typed_exit': 'delivery_started', 'reason': 'The case supplied the current reviewed plan acceptance.'}
    output = wrapper(fixture, 'guru-activate-delivery', 'invoke.sh',
                     ['--input', str(write(fixture / '.trellis/.runtime/guru-team/evals/activation.json', public)),
                      '--owner-result', str(write(fixture / '.trellis/.runtime/guru-team/evals/activation-owner.json', owner))], formal=True)
    if output['exit_id'] != 'delivery_started':
        raise ValueError('Actual public activation failed: ' + str(output))
    return output['planning_accepted_result_id']


def check(runtime, fixture, task, projection, key, planning_id, exit_id, *, formal, base_head=None):
    from adapters.eval.production_fixtures import production_phase2_input
    paths = ['src/production-eval.txt']
    candidate = projection.candidate(paths, kind='git', head_ref=run_git(fixture, 'rev-parse', 'HEAD'),
                                     base_ref=base_head or run_git(fixture, 'rev-parse', 'origin/main'))
    if projection.resolve(key)['phase'] == 'reviewing':
        projection.apply({'api_version': '1.0', 'operation': 'rework', 'key': key,
                          'owner_role': 'full_review', 'owner_id': projection.declaration()['owners']['full_review'],
                          'expected_phase': 'reviewing', 'target_role': 'implementation',
                          'reason': authority_ref(task / 'prd.md', fixture),
                          'affected_results': ['check', 'full_review', 'readiness']})
    projection.begin_check(key, candidate)
    package = fixture / '.trellis/guru-team/skills/packages/guru-check-task'
    path = production_phase2_input(runtime, fixture, task, package, exit_id)
    recorded = wrapper(fixture, 'guru-check-task', 'record-phase2-check.sh', ['--task', task.relative_to(fixture).as_posix(), '--input', str(path)])
    checked = wrapper(fixture, 'guru-check-task', 'check-phase2-check.sh', ['--task', task.relative_to(fixture).as_posix()])
    public = {'profile': 'delivery_initial_check', 'mode': 'workflow', 'task_ref': task.relative_to(fixture).as_posix(),
              'source_exit': 'implementation_complete', 'delivery_key': key, 'planning_accepted_result_id': planning_id}
    if formal:
        output = wrapper(fixture, 'guru-check-task', 'invoke.sh',
                         ['--input', str(write(fixture / '.trellis/.runtime/guru-team/evals/check.json', public)),
                          '--owner-result', checked['artifact_path']], formal=True)
        if output['exit_id'] != 'passed':
            raise ValueError('Actual prerequisite Check did not pass: ' + str(output))
        checked.update(output)
    return recorded, checked, public


def stage_delivery_production(request, fixture, target, request_package, recipe, public_input_path):
    skill = request['skill_id']
    fixture = fixture.resolve()
    package = fixture / '.trellis/guru-team/skills/packages' / skill
    for name in ('interface.json', 'evals/evals.json'):
        if hashlib.sha256((package / name).read_bytes()).digest() != hashlib.sha256((request_package / name).read_bytes()).digest():
            raise ValueError('Owner staging package differs from current declared contract.')
    runtime = load_package_owner_runtime(target, skill)
    compose_production_fixture_runtime(target, runtime)
    compose_production_owner_command_runtime(target, runtime)
    runtime.read_json = lambda path: json.loads(Path(path).read_text())
    runtime.diff_base_ref = lambda root, branch: 'origin/' + branch
    runtime.changed_files = lambda root, revision: run_git(root, 'diff', '--name-only', revision).splitlines()
    def status_paths(root):
        value = subprocess.run(['git', 'status', '--porcelain', '-z'], cwd=root,
                               capture_output=True, check=True).stdout.decode()
        return [item[3:] for item in value.split('\0') if len(item) >= 4
                and not item[3:].startswith('.trellis/.runtime/')]
    runtime.git_status_paths = status_paths
    run_git(fixture, 'branch', '-M', 'main')
    run_git(fixture, 'add', '.')
    run_git(fixture, 'commit', '-qm', 'stage installed production candidate')
    base = run_git(fixture, 'rev-parse', 'HEAD')
    run_git(fixture, 'update-ref', 'refs/remotes/origin/main', base)
    if not run_git(fixture, 'remote'):
        run_git(fixture, 'remote', 'add', 'origin', 'https://github.com/example/guru-extension.git')
    run_git(fixture, 'checkout', '-qb', 'eval/current')
    context_id = 'production-delivery-eval'
    prior = os.environ.get('TRELLIS_CONTEXT_ID')
    os.environ['TRELLIS_CONTEXT_ID'] = context_id
    try:
        task, key, projection = seed_delivery(fixture, context_id)
        public = json.loads(public_input_path.read_text())
        public.update(task_ref=task.relative_to(fixture).as_posix(), delivery_key=key)
        if skill == 'guru-approve-task-plan':
            recorded, checked = planning(runtime, fixture, task, key, recipe.removeprefix('planning-').replace('-', '_'))
            public.update(source_exit='baseline_current', architecture_assessment=final_architecture(fixture, task, key))
            write(fixture / OWNER_INPUT, public)
            bind_owner_result_argument(request, fixture, Path(checked['artifact_path']))
        else:
            planning_id = activate(runtime, fixture, task, key)
            (fixture / 'src/production-eval.txt').write_text(recipe + '\n')
            if skill == 'guru-check-task' and recipe == 'check-delivery-stopped':
                candidate = projection.candidate(['src/production-eval.txt'], kind='git',
                                                 head_ref=run_git(fixture, 'rev-parse', 'HEAD'), base_ref=base)
                projection.begin_check(key, candidate)
                reason = authority_ref(task / 'prd.md', fixture)
                semantic = {'reviewed_delivery_key': key, 'result_id': 'stop:production-check',
                            'reason': reason, 'scope_decision': reason, 'evidence': [reason]}
                write(fixture / OWNER_INPUT, public)
                owner_path = write(fixture / '.trellis/.runtime/guru-team/evals/check-stop-owner.json', semantic)
                bind_owner_result_argument(request, fixture, owner_path)
                return package, target, {'TRELLIS_CONTEXT_ID': context_id}
            if skill == 'guru-check-task' and recipe == 'check-resolved-reconciliation-passed':
                # A legal evolved-base merge produces the actual resolved index.
                run_git(fixture, 'add', '.')
                run_git(fixture, 'commit', '-qm', 'stage feature candidate')
                run_git(fixture, 'switch', 'main')
                (fixture / 'src').mkdir(exist_ok=True)
                (fixture / 'src/base-evolution.txt').write_text('evolved base\n')
                run_git(fixture, 'add', '.')
                run_git(fixture, 'commit', '-qm', 'evolve base')
                new_base = run_git(fixture, 'rev-parse', 'HEAD')
                run_git(fixture, 'update-ref', 'refs/remotes/origin/main', new_base)
                run_git(fixture, 'switch', 'eval/current')
                run_git(fixture, 'merge', '--no-commit', '--no-ff', 'main')
            exit_id = recipe.removeprefix('check-').replace('-', '_') if skill == 'guru-check-task' else 'passed'
            recorded, checked, check_public = check(runtime, fixture, task, projection, key, planning_id, exit_id, formal=skill != 'guru-check-task')
            if skill == 'guru-check-task':
                public['planning_accepted_result_id'] = planning_id
                write(fixture / OWNER_INPUT, public)
                bind_owner_result_argument(request, fixture, Path(checked['artifact_path']))
            else:
                from adapters.eval.production_fixtures import production_prepare_task_commit, production_task_commit_authoring, production_record_review
                public.pop('phase2_commit_anchor', None)
                public['check_result_id'] = checked['check_result_id']
                if skill == 'guru-create-task-commit' and recipe == 'commit-clean-reentry':
                    initial = {'profile': 'delivery_initial_commit', 'mode': public['mode'], 'task_ref': public['task_ref'],
                               'source_exit': 'passed', 'delivery_key': key, 'check_result_id': checked['check_result_id']}
                    owner_path, _, _ = production_prepare_task_commit(runtime, fixture, initial,
                                                                    production_task_commit_authoring(runtime, fixture, checked, 'passed'))
                    wrapper(fixture, 'guru-create-task-commit', 'invoke.sh', ['--candidate-artifact', str(owner_path)], formal=True)
                    _, fresh, _ = check(runtime, fixture, task, projection, key, planning_id, 'passed', formal=True)
                    public['check_result_id'] = fresh['check_result_id']
                    write(fixture / OWNER_INPUT, public)
                    owner_path = write(fixture / '.trellis/.runtime/guru-team/evals/clean-commit-owner.json',
                                       {'status': 'passed', 'summary': 'Current candidate is already committed and clean; preserve its HEAD.',
                                        'evidence': ['actual fresh Check', 'actual clean candidate HEAD']})
                    bind_owner_result_argument(request, fixture, owner_path)
                elif skill == 'guru-create-task-commit':
                    status = {'commit-revision-required': 'revision-required', 'commit-blocked-recovery': 'blocked'}.get(recipe, 'passed')
                    owner_path, _, _ = production_prepare_task_commit(runtime, fixture, public,
                                                                     production_task_commit_authoring(runtime, fixture, checked, status))
                    write(fixture / OWNER_INPUT, public)
                    bind_task_commit_candidate_argument(request, fixture, owner_path)
                else:
                    initial = {'profile': 'delivery_initial_commit', 'mode': public['mode'], 'task_ref': public['task_ref'],
                               'source_exit': 'passed', 'delivery_key': key, 'check_result_id': checked['check_result_id']}
                    owner_path, _, prepared = production_prepare_task_commit(runtime, fixture, initial,
                                                                            production_task_commit_authoring(runtime, fixture, checked, 'passed'))
                    wrapper(fixture, 'guru-create-task-commit', 'invoke.sh', ['--candidate-artifact', str(owner_path)], formal=True)
                    # TaskCommit preserves actual commit; fresh Check binds it before Review.
                    continuity_base = run_git(fixture, 'rev-parse', 'HEAD^') if public['profile'] == 'delivery_base_continuity' else None
                    _, checked, _ = check(runtime, fixture, task, projection, key, planning_id, 'passed', formal=True,
                                          base_head=continuity_base)
                    public['check_result_id'] = checked['check_result_id']
                    production_record_review(runtime, fixture, task, public, recipe)
                    write(fixture / OWNER_INPUT, public)
        return package, target, {'TRELLIS_CONTEXT_ID': context_id}
    finally:
        if prior is None:
            os.environ.pop('TRELLIS_CONTEXT_ID', None)
        else:
            os.environ['TRELLIS_CONTEXT_ID'] = prior
