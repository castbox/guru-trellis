"""Independent committed Branch Review facts and original owner transport."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
from adapters.eval import phase2_authoring
from adapters.eval.fixture_io import run_git
from adapters.eval.phase2_authoring import write_json
from runtime.delivery_projection.adapter import DeliveryProjection
from runtime.reviewed_content import reviewed_content_identity, reviewed_content_metadata_path

SKILL = 'guru-review-branch'
FACTS = '.trellis/tasks/branch-evidence/public-authoring-facts.json'
ARCHITECTURE_INPUT = '.trellis/tasks/branch-evidence/architecture-input.json'
PUBLIC_INPUT = '.trellis/tasks/branch-evidence/public-input.json'
OWNER_SCHEMA = 'schemas/delivery-review-gate-2.0.schema.json'
PUBLIC_READS = ('SKILL.md', 'references/contract.md', 'interface.json', OWNER_SCHEMA,
    'schemas/public-delivery-branch-review-input-2.0.schema.json')


def stage(request: dict, fixture: Path, package: Path, source_repo: Path) -> None:
    fixture = fixture.resolve()
    # Establish the installed repository HEAD before its real Task binding.
    run_git(fixture, 'add', '.')
    run_git(fixture, 'commit', '-qm', 'stage installed review fixture tools')
    # Reuse the original business candidate and fixture-owned Planning boundary.
    # No Check input/result or current review judgment is staged.
    phase2_authoring.stage({**request, 'case_id':'native-owner-common-expectation'}, fixture,
        package, source_repo, review_candidate=True)
    prior = json.loads((fixture / phase2_authoring.FACTS).read_text())
    projection = DeliveryProjection(fixture, prior['task_ref'])
    key = prior['delivery_key']
    # This fixture supplies an existing standalone checkout to the Task. Match
    # its actual C4 binding with the original C5 caller-owned resource state.
    from runtime.task_lifecycle import BranchBindingStore, TaskLifecycleKey, inspect_repository
    from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore
    repository = inspect_repository(fixture)
    task_key = TaskLifecycleKey(key['task_id'], key['lifecycle_generation'])
    binding = BranchBindingStore(repository).read(task_key)
    if binding is None:
        raise ValueError('Review fixture requires its original Task branch binding')
    ResourceLedgerStore(repository).establish_current(task_key,
        binding_revision=binding.binding_revision, branch_name=binding.branch_name,
        branch_ownership='caller_owned', worktree_ownership='not_applicable')
    base = run_git(fixture, 'rev-parse', 'origin/main')
    run_git(fixture, 'add', '.')
    run_git(fixture, 'commit', '-qm', 'commit actual common-assumption review candidate')
    head = run_git(fixture, 'rev-parse', 'HEAD')
    paths = [path for path in run_git(fixture, 'diff', '--name-only', base, head).splitlines()
             if not reviewed_content_metadata_path(path)]
    projection.begin_check(key, projection.candidate(paths, head_ref=head, base_ref=base))
    public = {'profile':'delivery_branch_review','mode':'workflow','task_ref':prior['task_ref'],
        'delivery_key':key, 'base_ref':base,'branch_review_commit':head,'review_intent':'initial_review'}
    planning = projection.planning_directory(key).relative_to(fixture).as_posix()
    architecture_package = package.parent / phase2_authoring.ARCHITECTURE
    architecture = json.loads((architecture_package /
        'evals/files/branch-review-independent-native-input.json').read_text())
    architecture.update(delivery_key=key, planning_root=prior['planning_root'],
        task_locator=prior['task_ref'], continuation_id='range-branch-review',
        requirement_authority='docs/range.md', behavior_authority=planning+'/design.md',
        freshness_identity='sha256:'+reviewed_content_identity(fixture)['sha256'],
        candidate={'head':head, 'content_identity':'sha256:'+reviewed_content_identity(fixture)['sha256']},
        committed_range={'base_ref':base,'base_head':base,'review_head':head})
    architecture['baseline'].update(identity='range-v1')
    architecture['constitution'].update(identity_kind='version', identity='range-constitution-v1')
    architecture['project_contract'].update(change_contract_identity='range-contract-v1',
        required_concern_set_identity='range-concerns-v1')
    architecture['before_authority'] = {'git_revision':base,
        'baseline_locator':architecture['baseline']['locator'],
        'constitution_locator':architecture['constitution']['authority_locator'],
        'change_contract_locator':architecture['project_contract']['change_contract_locator']}
    write_json(fixture / ARCHITECTURE_INPUT, architecture)
    write_json(fixture / PUBLIC_INPUT, public)
    diff = fixture / '.trellis/tasks/branch-evidence/committed.patch'
    diff.write_text(run_git(fixture, 'diff', base, head)+'\n')
    qualifiers = [f'.trellis/guru-team/skills/packages/{skill}/{path}'
        for skill in phase2_authoring.ALL_QUALIFIERS for path in (
            'SKILL.md', 'references/contract.md', 'interface.json',
            'schemas/semantic-result.schema.json',
            'schemas/public-branch-review-candidate-set-input.schema.json')]
    author = '.trellis/guru-team/skills/packages/guru-author-task-plan/'
    write_json(fixture / FACTS, {'required_reads':sorted(set([*prior['required_reads'],
        *qualifiers, author+'references/planning-body.md',
        *(author+'templates/delivery-'+name+'.md' for name in ('prd','design','implement')),
        *(f'.trellis/guru-team/skills/consumers/workflow/production/{name}-qualification-invocation.schema.json'
          for name in ('normal-scenario','solution-mechanism','root-cause')),
        prior['task_ref']+'/prd.md', PUBLIC_INPUT, '.trellis/tasks/branch-evidence/committed.patch'])),
        'architecture_reads':[architecture['constitution']['authority_locator'],
            architecture['baseline']['locator'], architecture['project_contract']['change_contract_locator'],
            planning+'/design.md', '.trellis/tasks/branch-evidence/committed.patch',
            'interval.py', 'range_filter.py', 'docs/range.md', ARCHITECTURE_INPUT],
        'architecture_input_sha256':hashlib.sha256(json.dumps(architecture, ensure_ascii=False,
            sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
        'public_input_locator':PUBLIC_INPUT,'writable_paths':[],
        'owner_mutated_paths':[prior['task_ref']+'/task.json',
            f".trellis/.runtime/guru-team/owner-checkpoints/{Path(prior['task_ref']).name}/{key['delivery_id']}/review-gate.json"],
        'committed_range':{'base_ref':base,'review_head':head},
        'prerequisite_boundary':'Business candidate and fixture-owned Planning/Activation prerequisites only. No native Planning producer is claimed. Check and full_review are empty; the receiving AI must author the current independent Review and both judgments after actual fresh Architecture output.'})



def execute(package: Path, repository: Path, envelope: dict, environment: dict) -> subprocess.CompletedProcess:
    public = envelope['public_input']
    owner = envelope['owner_result']
    typed_exit = owner['semantic_review']['ai_review_gate']['status']
    runtime = repository / '.trellis/.runtime/guru-team/evals'
    public_path, owner_path = runtime / 'native-branch-input.json', runtime / 'native-branch-owner.json'
    write_json(public_path, public)
    write_json(owner_path, owner)
    commands = [
        [str(package / 'scripts/review-branch.sh'), '--root', str(repository), '--task', public['task_ref'],
            '--skill-input',str(public_path),'--semantic-review-file',str(owner_path),'--typed-exit',typed_exit],
        [str(package / 'scripts/check-review-gate.sh'),'--root',str(repository),'--task',public['task_ref'],
            '--delivery-key',json.dumps(public['delivery_key']),'--expected-exit',typed_exit],
        [str(package / 'scripts/invoke.sh'),'--root',str(repository),'--task',public['task_ref'],
            '--input',str(public_path)],
    ]
    receipts=[]
    try:
        for argv in commands:
            result=subprocess.run(argv,cwd=repository,env=environment,capture_output=True,text=True,check=False)
            receipts.append({'argv':argv,'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
            if result.returncode:
                return result
        return result
    finally:
        write_json(repository.parent / 'branch-command-receipts.json',receipts)
        public_path.unlink(missing_ok=True)
        owner_path.unlink(missing_ok=True)


def context(repository: Path, package: Path, helper_command: str, reads: list[str], input_locator: Path) -> str:
    return '\n'.join([
        'Execute the installed independent full committed Branch Review owner against its actual fixed base-to-HEAD range.',
        *[f'{helper_command} read --kind skill_contract --path {package / path}' for path in PUBLIC_READS],
        f'{helper_command} read --kind owner_file --path {repository / FACTS}',
        *[f'{helper_command} read --kind owner_file --path {repository / path}' for path in reads],
        'Consume the actual preceding independent Architecture DTO. It is one input to your own complete Branch Review, not your final result. The fixture-owned Planning/Activation boundary supplies entry facts only. There is no prior Check result. Complete your independent review of the fixed committed candidate before authoring either required role outcome.',
        'Judge the complete committed range and necessary unchanged consumers using the effective requirement, design and implementation contracts. Author candidate_classifications, semantic_review, delivery_review, verification_evidence, adequacy_review, gate_judgments and planning_revision yourself as the original recorder input. Independently review all nine adequacy dimensions from the current contract, adopting only applicable original engineering facts and performing any missing or uncertain validation under the original owner. Each dimension requires status, summary and evidence. Author check and full_review outcome/summary independently from their actual responsibilities; neither follows automatically from the other or from Architecture. Use planning_revision=null unless the current planning_stale route requires concrete revision actions. The delivery-review-gate schema describes the completed gate; do not author derived Git identities, timestamps or facts hashes.',
        'Form the actual candidate set under the original Skill. If it is empty, invoke no qualification owner and do not invent a placeholder candidate. For real nonempty candidates, load the original normal-scenario, solution-mechanism and root-cause contracts and selected schemas in required_reads. Invoke normal-scenario with helper invoke --stdin --qualifier normal-scenario; invoke solution-mechanism for its eligible refs with --qualifier solution-mechanism, then root-cause for its eligible refs with --qualifier root-cause. Use branch_review_candidate_set and each original {schema_version:"1.0",semantic_result:<your result>} envelope, with public_input inside semantic_result. Consume actual preceding outcomes and any still-applicable same-mechanism conclusion under the original owner contract. Ordinary features still require the original root owner applicability judgment when eligible; an all-rejected set supplies no root placeholder. The host supplies no candidate, disposition or route.',
        'Supply {public_input,owner_result} through the helper invoke --stdin. The host transports your fields unchanged to the original review-branch recorder, checker and public wrapper. Do not edit product files, planning or test assertions. Do not read private runtime checkpoints. The transport supplies no missing semantic field, adequacy conclusion, typed exit or role outcome. The private gate uses schema_version 8.0; the recorder supplies derived identities only.',
        'Before invoking Review, finish every listed contract, repository and staged case-file read, including case-file commands shown after this section. Then make exactly one final Review helper invocation. After its successful stdout, return that complete JSON as your final response without further traced reads or invocations. A nonzero invocation ends this eval.',
        f'{helper_command} invoke --stdin',
    ])
