"""Independent committed Branch Review facts and original owner transport."""
from __future__ import annotations
import json
from pathlib import Path
import subprocess
from adapters.eval import phase2_authoring
from adapters.eval.fixture_io import run_git
from adapters.eval.phase2_authoring import write_json
from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
from runtime.delivery_projection.gates import record_gate, rework
from runtime.reviewed_content import reviewed_content_identity, reviewed_content_metadata_path

SKILL = 'guru-review-branch'
FACTS = '.trellis/tasks/branch-evidence/public-authoring-facts.json'
ARCHITECTURE_INPUT = '.trellis/tasks/branch-evidence/architecture-input.json'
PUBLIC_INPUT = '.trellis/tasks/branch-evidence/public-input.json'
OWNER_SCHEMA = 'schemas/delivery-review-gate-1.0.schema.json'
PUBLIC_READS = ('SKILL.md', 'references/contract.md', 'interface.json', OWNER_SCHEMA,
    'schemas/public-delivery-branch-review-input-1.0.schema.json')


def stage(request: dict, fixture: Path, package: Path, source_repo: Path) -> None:
    # Reuse the actual shared-assumption candidate facts. Its historical Check
    # precondition below is staging only, never a claimed native Check result.
    phase2_authoring.stage({**request, 'case_id':'native-owner-common-expectation'}, fixture,
        package.parent / phase2_authoring.SKILL, source_repo)
    check = json.loads((fixture / 'docs/phase2-evidence/check-public-input.json').read_text())
    projection = DeliveryProjection(fixture, check['task_ref'])
    key = check['delivery_key']
    base = run_git(fixture, 'rev-parse', 'origin/main')
    run_git(fixture, 'add', '.')
    run_git(fixture, 'commit', '-qm', 'commit actual common-assumption review candidate')
    head = run_git(fixture, 'rev-parse', 'HEAD')
    paths = [path for path in run_git(fixture, 'diff', '--name-only', base, head).splitlines()
             if not reviewed_content_metadata_path(path)]
    rework(projection, key, 'check', 'implementation',
        authority_ref(projection.planning_directory(key) / 'implement.md', fixture),
        ['check', 'full_review', 'readiness'])
    projection.begin_check(key, projection.candidate(paths, head_ref=head, base_ref=base))
    record_gate(projection, key, 'check', 'check:historical-native-review-prerequisite', 'passed',
        [authority_ref(projection.planning_directory(key) / 'implement.md', fixture)], [])
    public = {'profile':'delivery_branch_review','mode':'workflow','task_ref':check['task_ref'],
        'delivery_key':key,'check_result_id':'check:historical-native-review-prerequisite',
        'base_ref':base,'branch_review_commit':head,'review_intent':'initial_review'}
    architecture = json.loads((fixture / phase2_authoring.ARCHITECTURE_INPUT).read_text())
    architecture.update(stage='branch_review', source_exit='task_commit_created',
        candidate={'head':head, 'content_identity':'sha256:'+reviewed_content_identity(fixture)['sha256']},
        committed_range={'base_ref':base,'base_head':base,'review_head':head})
    write_json(fixture / ARCHITECTURE_INPUT, architecture)
    write_json(fixture / PUBLIC_INPUT, public)
    diff = fixture / '.trellis/tasks/branch-evidence/committed.patch'
    diff.write_text(run_git(fixture, 'diff', base, head)+'\n')
    prior = json.loads((fixture / phase2_authoring.FACTS).read_text())
    write_json(fixture / FACTS, {'required_reads':sorted(set([*prior['required_reads'],
        *(f'.trellis/guru-team/skills/packages/{skill}/schemas/public-branch-review-candidate-set-input.schema.json'
          for skill in phase2_authoring.ALL_QUALIFIERS),
        PUBLIC_INPUT, '.trellis/tasks/branch-evidence/committed.patch'])),
        'architecture_reads':[path for path in prior['architecture_reads'] if path != phase2_authoring.ARCHITECTURE_INPUT] + [ARCHITECTURE_INPUT],
        'public_input_locator':PUBLIC_INPUT,'writable_paths':[],
        'owner_mutated_paths':[check['task_ref']+'/task.json',
            f".trellis/.runtime/guru-team/owner-checkpoints/{Path(check['task_ref']).name}/{key['delivery_id']}/review-gate.json"],
        'committed_range':{'base_ref':base,'review_head':head},
        'prerequisite_boundary':'The actual installed gate is a historical fixture precondition. This case proves only the independent Branch Review owner, not native Check or a continuous Check-to-Review chain.'})


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
        'Consume the actual preceding independent Architecture DTO. It is one input to your own complete Branch Review, not your final result. The historical Check gate only establishes this isolated fixture entry; it supplies no semantic evidence for your review.',
        'Judge the complete committed range and necessary unchanged consumers using the effective requirement, design and implementation contracts. Author candidate_classifications, semantic_review, delivery_review and verification_evidence yourself as the original recorder input. The delivery-review-gate schema describes the completed gate; do not author derived Git identities, timestamps or facts hashes.',
        'Form the actual candidate set under the original Skill. If it is empty, invoke no qualification owner and do not invent a placeholder candidate. For real nonempty candidates, load the original normal-scenario, solution-mechanism and root-cause contracts and selected schemas in required_reads. Invoke normal-scenario with helper invoke --stdin --qualifier normal-scenario; invoke solution-mechanism for its eligible refs with --qualifier solution-mechanism, then root-cause for its eligible refs with --qualifier root-cause. Use branch_review_candidate_set and each original {schema_version:"1.0",semantic_result:<your result>} envelope, with public_input inside semantic_result. Consume actual preceding outcomes and any still-applicable same-mechanism conclusion under the original owner contract. Ordinary features still require the original root owner applicability judgment when eligible; an all-rejected set supplies no root placeholder. The host supplies no candidate, disposition or route.',
        'Supply {public_input,owner_result} through the helper invoke --stdin. The host transports your fields unchanged to the original review-branch recorder, checker and public wrapper. Do not edit product files, planning or test assertions. Do not read the previous private Check checkpoint.',
        'Before invoking Review, finish every listed contract, repository and staged case-file read, including case-file commands shown after this section. Then make exactly one final Review helper invocation. After its successful stdout, return that complete JSON as your final response without further traced reads or invocations. A nonzero invocation ends this eval.',
        f'{helper_command} invoke --stdin',
    ])
