"""Actual Author document transport in the original native eval runner."""
from __future__ import annotations

import json
import hashlib
import os
from pathlib import Path
from datetime import datetime
import subprocess
import sys
import tempfile

from adapters.eval.architecture_authoring import stage_delivery_identity, public_contract_reads
from adapters.eval.fixture_io import public_input_path, run_git
from adapters.eval.phase2_authoring import write_json

SKILL = 'guru-author-task-plan'
FACTS = '.trellis/tasks/planning-evidence/public-authoring-facts.json'
ARCHITECTURE_INPUT = '.trellis/tasks/planning-evidence/architecture-input.json'
PUBLIC_INPUT = '.trellis/tasks/planning-evidence/author-input.json'
OWNER_SCHEMA = 'schemas/semantic-result-2.0.schema.json'
PUBLIC_READS = ('SKILL.md', 'references/authoring.md', 'references/planning-body.md',
                'templates/delivery-design.md', 'templates/delivery-implement.md',
                'interface.json', OWNER_SCHEMA, 'schemas/public-delivery-solution-planning-input.schema.json')



def acquire_authoring_checkout(fixture: Path, *, branch_name: str = 'eval/author'):
    """Acquire the fixture through the original linked-checkout C5 executor."""
    from runtime.task_lifecycle.checkout_acquisition import CheckoutAcquisitionPlan, acquire_checkout
    fixture = fixture.resolve()
    run_git(fixture, 'add', '.')
    run_git(fixture, 'commit', '-qm', 'stage installed tools for Author checkout acquisition')
    head = run_git(fixture, 'rev-parse', 'HEAD')
    primary = fixture.parent / (fixture.name + '-primary')
    fixture.rename(primary)
    return acquire_checkout(CheckoutAcquisitionPlan(
        route='provision_linked_worktree', repository_context=primary,
        task_id='current', task_ref=f'.trellis/tasks/{datetime.now():%m-%d}-current',
        lifecycle_generation=0, branch_ref='refs/heads/' + branch_name,
        expected_status='planning', decision_head=head,
        transaction_id='author-fixture-acquisition', result_id='author-fixture-checkout',
        provision_disposition='new_branch', target_path=fixture,
        forbidden_branch_refs=('refs/heads/main',), task_artifact_expectation='absent'))


def register_authoring_resources(fixture: Path, delivery_key: dict, acquisition):
    """Register actual acquired resources against the original current binding."""
    from runtime.task_lifecycle import BranchBindingStore, TaskLifecycleKey, inspect_repository
    from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore
    repository = inspect_repository(fixture)
    key = TaskLifecycleKey(delivery_key['task_id'], delivery_key['lifecycle_generation'])
    binding = BranchBindingStore(repository).read(key)
    if binding is None:
        raise ValueError('Author fixture requires the actual created branch binding')
    return ResourceLedgerStore(repository).establish_current(key,
        binding_revision=binding.binding_revision, branch_name=binding.branch_name,
        branch_ownership=acquisition.branch_ownership,
        worktree_ownership=acquisition.worktree_ownership)


def stage(request: dict, fixture: Path, package: Path, source_repo: Path) -> None:
    fixture = fixture.resolve()
    acquisition = acquire_authoring_checkout(fixture)
    public = json.loads(public_input_path(request).read_text())
    source = '# Snapshot operations source\n\nR1: Add label editing for stored historical snapshots. A label edit must not change the active target or its eligibility. Missing activation qualification must not reject a label edit.\nR2: Activating another target requires qualification for that exact target. Exception: restoring a previously active target may reuse its recorded still-applicable qualification. A target name or an earlier plan approval does not establish qualification.\nR3: Keep qualification owned by activation; do not add a universal snapshot-operation admission prerequisite.\n'
    directory = stage_delivery_identity(fixture, public, scope_content=source, scope_anchor='R1')
    resources = register_authoring_resources(fixture, public['delivery_key'], acquisition)
    task_ref = public.pop('task_locator')
    planning_root = public.pop('planning_root')
    public.update(task_ref=task_ref)
    public.pop('architecture_assessment', None)
    files = {
        'docs/source.md': source,
        f'{task_ref}/{planning_root}/prd.md': source,
        'docs/architecture/00-foundation/design-constitution.md': '# Constitution\nIdentity: snapshot-constitution-v1. Snapshot display metadata and active-target admission have separate responsibilities. Read the full operation conditions from docs/source.md.\n',
        'docs/architecture/README.md': '# Architecture\nIdentity: snapshot-v1. Active. snapshots.py owns historical label metadata; activation.py owns current target qualification and activation. Editing historical metadata does not activate a target.\n',
        'docs/architecture/06-governance/change-contract.md': '# Change Contract\nIdentity: snapshot-contract-v1. Concerns: snapshot-concerns-v1. Inspect operation effects and actual activation dependencies. No executable Architecture check applies; source and caller facts are directly inspectable.\n',
        'snapshots.py': 'def rename_label(snapshot, label):\n    return {**snapshot, "label": label}\n',
        'activation.py': 'def activate(state, target, qualified):\n    if target not in qualified:\n        raise ValueError("target qualification missing")\n    return {**state, "active_target": target}\n',
    }
    for relative, text in files.items():
        path = fixture / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    for name in ('design.md', 'implement.md', 'implement.jsonl', 'check.jsonl'):
        (directory / name).unlink(missing_ok=True)
    architecture_package = package.parent / 'guru-maintain-architecture-baseline'
    # Reuse only the public identity skeleton; no owner judgment is staged.
    skeleton = json.loads((architecture_package / 'examples/public-input-delivery-task-impact-sync-1.0.json').read_text())
    skeleton.update(schema_version='delivery-1.0', profile='delivery_task_impact_sync',
        delivery_key=public['delivery_key'], planning_root=planning_root,
        source_exit='planning', mode='workflow', continuation_id='snapshot-author', stage='planning',
        task_locator=task_ref, planning_purpose='candidate_assessment',
        baseline={'locator': 'docs/architecture/README.md', 'identity': 'snapshot-v1', 'status': 'active'},
        project_contract={'guru_contract_identity':'guru-maintain-architecture-baseline:planning:3.0',
            'change_contract_locator':'docs/architecture/06-governance/change-contract.md',
            'change_contract_identity':'snapshot-contract-v1', 'required_concern_set_identity':'snapshot-concerns-v1'},
        requirement_authority='docs/source.md', behavior_authority='docs/source.md',
        candidate={'design_facts':['Add historical snapshot label editing while preserving the existing activation qualification owner and active target.'], 'constraint_refs':['docs/source.md']})
    skeleton['constitution'].update(authority_locator='docs/architecture/00-foundation/design-constitution.md', identity='snapshot-constitution-v1')
    skeleton['freshness_identity'] = 'sha256:' + hashlib.sha256(json.dumps(
        skeleton['candidate'], ensure_ascii=False, sort_keys=True, separators=(',', ':')
    ).encode()).hexdigest()
    write_json(fixture / ARCHITECTURE_INPUT, skeleton)
    write_json(fixture / PUBLIC_INPUT, public)
    architecture_reads = ['docs/architecture/00-foundation/design-constitution.md', 'docs/architecture/README.md',
        'docs/architecture/06-governance/change-contract.md', 'snapshots.py', 'activation.py', 'docs/source.md', ARCHITECTURE_INPUT]
    contract_reads = [str(path.relative_to(fixture)) for path in public_contract_reads(architecture_package, skeleton)]
    required = [*files, f'{task_ref}/prd.md', PUBLIC_INPUT, *contract_reads,
                '.trellis/spec/workflow/clear-technical-writing.md']
    run_git(fixture, 'add', '.')
    run_git(fixture, 'commit', '-qm', 'stage source and actual Author planning boundary')
    starting_head = run_git(fixture, 'rev-parse', 'HEAD')
    run_git(fixture, 'update-ref', 'refs/remotes/origin/main', starting_head)
    observed_target = run_git(fixture, 'rev-parse', 'origin/main')
    from runtime.delivery_projection.adapter import DeliveryProjection
    projection = DeliveryProjection(fixture, task_ref)
    content_base = projection.content_base(public['delivery_key'],
        development_base=starting_head, observed_target=observed_target)
    write_json(fixture / FACTS, {'required_reads': sorted(set(required)), 'architecture_reads': architecture_reads,
        'task_checkout': {
            'task_id': resources.task_id,
            'lifecycle_generation': resources.lifecycle_generation,
            'branch_name': resources.branch_name,
            'binding_revision': resources.binding_revision,
            'registered_checkout': str(acquisition.checkout.path),
            'topology': acquisition.checkout.topology,
        },
        'delivery_range': {
            'delivery_key': public['delivery_key'],
            'head': starting_head,
            'development_base': starting_head,
            'development_base_source': 'Explicit fixture starting HEAD after source and selected Delivery staging.',
            'observed_target_ref': 'origin/main',
            'observed_target': observed_target,
            'content_base': content_base,
            'contract_locator': '.trellis/guru-team/skills/packages/guru-author-task-plan/references/authoring.md#fixed-delivery-range',
        },
        'architecture_input_sha256': hashlib.sha256(json.dumps(skeleton, ensure_ascii=False,
            sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
        'public_input_locator': PUBLIC_INPUT, 'planning_root': f'{task_ref}/{planning_root}',
        'writable_paths': [f'{task_ref}/{planning_root}/{name}' for name in ('design.md','implement.md','implement.jsonl','check.jsonl')]})


def execute(package: Path, repository: Path, envelope: dict, environment: dict) -> subprocess.CompletedProcess:
    facts = json.loads((repository / FACTS).read_text())
    updates = envelope.get('file_updates', {})
    if not isinstance(updates, dict) or any(path not in facts['writable_paths'] or not isinstance(text, str) for path, text in updates.items()):
        raise ValueError('Author writes must name only the selected Delivery planning files')
    contexts = {}
    for relative, text in updates.items():
        if Path(relative).name in {'implement.jsonl', 'check.jsonl'}:
            contexts[relative] = [json.loads(line) for line in text.splitlines() if line.strip()]
        else:
            (repository / relative).write_text(text)
    receipts = []

    def run(argv):
        result = subprocess.run(argv, cwd=repository, env=environment,
            capture_output=True, text=True, check=False)
        receipts.append({'argv': argv, 'returncode': result.returncode,
                         'stdout': result.stdout, 'stderr': result.stderr})
        return result

    try:
        for relative, entries in contexts.items():
            # Replace the author's complete selection; the official writer owns
            # every nonempty entry. An empty selection remains a regular file.
            (repository / relative).write_text('')
            for entry in entries:
                public = envelope['public_input']
                result = run([sys.executable, '-B', str(repository / '.trellis/scripts/task.py'),
                    'add-context', public['task_ref'], Path(relative).stem,
                    entry['file'], entry['reason'], '--delivery', public['delivery_key']['delivery_id']])
                if result.returncode:
                    return result
        # File transport and public invocation remain distinct. No host owner fields.
        with tempfile.TemporaryDirectory(prefix='guru-author-input-') as temp:
            root = Path(temp)
            write_json(root / 'input.json', envelope['public_input'])
            write_json(root / 'owner.json', envelope['owner_result'])
            return run([str(package / 'scripts/invoke.sh'), '--root', str(repository),
                '--input', str(root / 'input.json'), '--owner-result', str(root / 'owner.json')])
    finally:
        write_json(repository.parent / 'planning-command-receipts.json', receipts)


def context(repository: Path, package: Path, helper_command: str, reads: list[str], input_locator: Path) -> str:
    return '\n'.join([
        'Execute the installed Author solution-writing profile against the actual selected Delivery.',
        'The first listed helper command below reads this Author session’s exact SKILL.md. Execute that command once and retain its complete stdout. Use the retained text for later references; do not repeat that same SKILL.md helper read in this session.',
        'The preceding Architecture worker is a separate session with its own first Skill read. Do not replay that worker’s read or invocation commands in this Author session.',
        'Run every trace-helper read and invoke strictly sequentially, one process at a time. Wait for each helper process to finish before starting the next. Do not run helper commands in parallel or in the background, and do not edit the trace receipt.',
        'Complete the remaining listed contract and repository reads through the traced helper before writing.',
        *[f'{helper_command} read --kind skill_contract --path {package / path}' for path in PUBLIC_READS],
        f'{helper_command} read --kind owner_file --path {repository / FACTS}',
        *[f'{helper_command} read --kind owner_file --path {repository / path}' for path in reads],
        'Consume the actual preceding Architecture output. Project only its Interface-declared candidate assessment into architecture_assessment of the staged Author input; do not invent an assessment.',
        'Author complete design.md, implement.md and both context JSONL selections yourself under the selected planning_root. Their only allowed write transport is file_updates in the eval envelope: {relative-path: complete-file-text}. For each nonblank JSONL row supply your selected file and reason. The transport passes those exact values to the installed official task.py add-context for the same Task, context kind and Delivery UUID; the official writer creates each entry. Empty selections remain empty regular JSONL files. Markdown bytes are transported unchanged. Any original add-context failure ends this invocation before the Author wrapper. This transport field is removed before the original public wrapper call. Do not write product code or shared authority.',
        'Form your actual owner_result using the current schema. Send {public_input,owner_result,file_updates} to the helper invoke --stdin with a quoted heredoc. Return only its actual complete JSON stdout. A nonzero boundary ends this invocation; never manufacture a pass.',
        f'{helper_command} invoke --stdin',
    ])
