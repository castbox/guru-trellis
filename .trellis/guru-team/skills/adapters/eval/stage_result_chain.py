"""Initial facts and external I/O for a native, continuous two-Delivery eval.

No Planning, Check, Review, publication or Delivery result is staged here.
All such results must come from the executing AI and the original wrappers.
"""
from __future__ import annotations
import json
import hashlib
import os
import shlex
import subprocess
import sys
from pathlib import Path
from adapters.eval.fixture_io import run_git
from adapters.eval.phase2_authoring import write_json

CASE = 'native-stage-continuous'
RESUME_PROTOCOL_ENV = 'GURU_TEAM_STAGE_CHAIN_RESUME_PROTOCOL'
INTERRUPTED_PROTOCOL_ENV = 'GURU_TEAM_STAGE_CHAIN_INTERRUPTED_PROTOCOL'
RAW_OBSERVATION_PATHS = (
    'docs/chain-evidence/before.py', 'docs/chain-evidence/current.py',
    'docs/chain-evidence/diff.patch', 'docs/chain-evidence/validation.json',
)
CARRIER_PATHS = tuple('.trellis/tasks/stage-result-evidence/' + name for name in (
    'current-review.md', 'input.json', 'facts.json', 'continuation.json',
))

# This provider substitutes only GitHub I/O. Real Git owns refs and merge commits.
PROVIDER = r'''import json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
root=Path(__file__).resolve().parents[1]
state_file=root/'state.json'
state=json.loads(state_file.read_text())
args=sys.argv[1:]
def option(name,default=None):
 return args[args.index(name)+1] if name in args else default
def git(*argv):
 return subprocess.check_output(['git','--git-dir',state['bare'],*argv],text=True).strip()
def save(): state_file.write_text(json.dumps(state))
def pr_row(row):
 result=dict(row)
 result['headRefOid']=git('rev-parse','refs/heads/'+row['headRefName'])
 return result
def emit(value): print(json.dumps(value))
if args[:2]==['auth','status']: raise SystemExit(0)
if args[:2]==['repo','view']: emit({'nameWithOwner':'example/stage-chain'})
elif args[:2]==['pr','list']:
 emit([pr_row(r) for r in state['prs'] if r['state']=='OPEN' and r['headRefName']==option('--head')])
elif args[:2]==['pr','create']:
 number=len(state['prs'])+1
 row={'number':number,'url':f'https://github.com/example/stage-chain/pull/{number}',
 'state':'OPEN','isDraft':'--draft' in args,'headRefName':option('--head'),
 'baseRefName':option('--base'),'title':option('--title'),'body':option('--body'),
 'headRepositoryOwner':{'login':'example'},'mergeable':'MERGEABLE',
 'mergeStateStatus':'CLEAN','reviewDecision':'','statusCheckRollup':[],
 'mergedAt':None,'mergeCommit':None}
 state['prs'].append(row);save();print(row['url'])
elif args[:2] in (['pr','view'],['pr','edit'],['pr','ready'],['pr','merge']):
 row=next(r for r in state['prs'] if r['number']==int(args[2]))
 action=args[1]
 if action=='edit':
  for flag,key in (('--title','title'),('--body','body')):
   if flag in args: row[key]=option(flag)
  save()
 elif action=='ready': row['isDraft']='--undo' in args;save()
 elif action=='merge':
  head=git('rev-parse','refs/heads/'+row['headRefName'])
  assert head==option('--match-head-commit')
  base=git('rev-parse','refs/heads/'+row['baseRefName'])
  message=option('--subject')+'\n\n'+Path(option('--body-file')).read_text()
  tree=git('rev-parse',head+'^{tree}')
  merged=subprocess.check_output(['git','--git-dir',state['bare'],'commit-tree',tree,
    '-p',base,'-p',head],input=message,text=True).strip()
  git('update-ref','refs/heads/'+row['baseRefName'],merged,base)
  row.update(state='MERGED',mergeCommit={'oid':merged},mergedAt=datetime.now(timezone.utc).isoformat())
  save()
 else: emit(pr_row(row))
elif args and args[0]=='api':
 path=args[1]
 prefix='repos/example/stage-chain'
 if path==prefix: emit({'full_name':'example/stage-chain','default_branch':'main',
  'allow_merge_commit':True,'allow_squash_merge':False,'allow_rebase_merge':False})
 elif '/git/ref/heads/' in path: emit({'object':{'sha':git('rev-parse','refs/heads/'+path.split('/git/ref/heads/')[1])}})
 elif '/git/commits/' in path:
  sha=path.rsplit('/',1)[1]
  emit({'sha':sha,'message':git('show','-s','--format=%B',sha),
   'parents':[{'sha':p} for p in git('show','-s','--format=%P',sha).split()]})
 else: raise SystemExit('Unsupported provider API: '+path)
else: raise SystemExit('Unsupported provider command: '+repr(args))
'''


SSH_TRANSPORT = r'''import os,shlex,sys
from pathlib import Path
command=shlex.split(sys.argv[-1])
if (len(command)!=2 or command[0] not in ('git-upload-pack','git-receive-pack')
    or command[1]!='/example/stage-chain.git'):
 raise SystemExit('Unsupported controlled Git transport command')
bare=Path(__file__).resolve().parents[1]/'remote.git'
os.execvp('git',['git',command[0][4:],str(bare)])
'''


def configure_provider_transport(fixture):
    """Map Git network I/O while keeping the original repository identity."""
    provider = fixture / '.trellis/.runtime/guru-team/evals/chain-provider'
    executable = provider / 'bin/local-ssh'
    executable.write_text('#!' + sys.executable + '\n' + SSH_TRANSPORT)
    executable.chmod(0o755)
    previous = subprocess.run(['git', 'config', '--local', '--unset-all',
        'url.' + str(provider / 'remote.git') + '.insteadOf'],
        cwd=fixture, capture_output=True, text=True)
    if previous.returncode not in (0, 5):
        raise ValueError(previous.stderr)
    run_git(fixture, 'config', '--local', 'core.sshCommand', shlex.quote(str(executable)))
    run_git(fixture, 'config', '--local', 'ssh.variant', 'ssh')
    url = 'ssh://git@github.com/example/stage-chain.git'
    if 'origin' in run_git(fixture, 'remote').split():
        run_git(fixture, 'remote', 'set-url', 'origin', url)
    else:
        run_git(fixture, 'remote', 'add', 'origin', url)


def configure_raw_observation_paths(fixture):
    """Keep test observations and live carriers outside business Git content."""
    exclude = Path(run_git(fixture, 'rev-parse', '--git-path', 'info/exclude'))
    if not exclude.is_absolute():
        exclude = fixture / exclude
    previous = exclude.read_bytes() if exclude.exists() else b''
    lines = previous.splitlines()
    additions = [('/' + path).encode() for path in (*RAW_OBSERVATION_PATHS, *CARRIER_PATHS)
                 if ('/' + path).encode() not in lines]
    if additions:
        exclude.parent.mkdir(parents=True, exist_ok=True)
        separator = b'\n' if previous and not previous.endswith(b'\n') else b''
        exclude.write_bytes(previous + separator + b'\n'.join(additions) + b'\n')


def stage(request, fixture, package, source_repo):
    from adapters.eval import stage_result_authoring as stage_result
    from adapters.eval.architecture_authoring import stage_delivery_identity
    from adapters.eval.planning_authoring import acquire_authoring_checkout, register_authoring_resources
    from runtime.delivery_projection.adapter import DeliveryProjection
    acquisition = acquire_authoring_checkout(fixture, branch_name='eval/stage-chain')
    configure_raw_observation_paths(fixture)
    source = '''# Inclusive filter authority

## R1. Contract slice
Publish a pure inclusive filtering contract: select(values, lower, upper) returns
values within both bounds, preserving order and duplicates. Negative and singleton
ranges are legal. The first Delivery is a partial contract slice. Its current
usage must say implementation is unavailable until a later Delivery implements
and validates this contract. That later implementation owner releases the limit;
the original RDT owner updates complete current guidance at final integration.
No deployment, activation, external consumer or production effect is required.

## R2. Implementation slice
A later Delivery implements select and its pure inclusive predicate, updates
applicable current guidance and assertions, and validates actual consumers.
Do not weaken inclusive bounds to preserve an old assertion. A half-open upper
bound is a mechanism conflict with this authority, not a scope change or missing
external evidence. Preserve the first Delivery's historical cutoff and results.
Whole Task completion requires both slices and their actual original results.
'''
    files = {
        '.trellis/tasks/implementation-evidence/README.md': '# Native execution facts\nFresh independent Architecture inputs are authored during this execution. No judgment is staged.\n',
        'docs/source.md': source,
        'docs/architecture/README.md': '# Architecture\nIdentity: range-v1. Active. interval.py owns the pure predicate; range_filter.py composes it without state, external dependencies or I/O. docs/source.md defines legal behavior.\n',
        'docs/architecture/00-foundation/design-constitution.md': '# Constitution\nIdentity: range-constitution-v1. Use applicable mature practice, complete semantics, cohesive responsibilities, minimum necessary complexity and one-way debt convergence. Keep the predicate pure and caller composition separate.\n',
        'docs/architecture/06-governance/change-contract.md': '# Change contract\nIdentity: range-contract-v1. Concerns: range-concerns-v1. Compare actual before/candidate responsibility, default, state, dependency and legal inputs. No executable Architecture check is required for this fixture.\n',
        'docs/requirements/README.md': '# Requirements\nIdentity: range-rdt-v1. Active. Current definition: current/filter.md. Architecture: ../architecture/README.md, range-v1, active.\n',
        'docs/requirements/current/filter.md': '# Filter requirements\nR1 and R2 are defined completely in docs/source.md. Both bounds are inclusive; order and duplicates are retained.\n',
        'docs/design/README.md': '# Design\nIdentity: range-rdt-v1. Current definition: current/filter.md.\n',
        'docs/design/current/filter.md': '# Filter design\nD1 owns the pure contract. D2 will implement interval.contains and compose it in range_filter.select, without state or I/O. This is accepted target behavior, not implementation evidence.\n',
        'docs/test/README.md': '# Test\nIdentity: range-rdt-v1. Current definition: current/filter.md.\n',
        'docs/test/current/filter.md': '# Filter validation\nT1: check the R1 contract. T2: D2 must validate inclusive boundaries, singleton/negative values, order, duplicates and the unchanged composing caller. No remote evidence is required.\n',
        'interval.py': 'def contains(value, lower, upper):\n    raise NotImplementedError("contract only")\n',
        'range_filter.py': 'from interval import contains\ndef select(values, lower, upper):\n    return [value for value in values if contains(value, lower, upper)]\n',
    }
    for relative, content in files.items():
        path = fixture / relative;path.parent.mkdir(parents=True, exist_ok=True);path.write_text(content)
    public = {}
    directory = stage_delivery_identity(fixture, public, scope_content=source, scope_anchor='R1. Contract slice')
    resources = register_authoring_resources(fixture, public['delivery_key'], acquisition)
    # Only identity exists. Remove every ungenerated planning body placeholder.
    for name in ('prd.md','design.md','implement.md','implement.jsonl','check.jsonl'):
        (directory/name).unlink(missing_ok=True)
    run_git(fixture,'add','.');run_git(fixture,'commit','-qm','stage unreviewed source and first Delivery identity')
    head = run_git(fixture,'rev-parse','HEAD')
    provider = fixture / '.trellis/.runtime/guru-team/evals/chain-provider'
    (provider/'bin').mkdir(parents=True)
    bare = provider/'remote.git'
    subprocess.run(['git','init','--bare',str(bare)],check=True,capture_output=True)
    for key, value in (('user.name','Stage fixture'),('user.email','stage@example.invalid')):
        subprocess.run(['git','--git-dir',str(bare),'config',key,value],check=True)
    configure_provider_transport(fixture)
    run_git(fixture,'push','origin',head+':refs/heads/main')
    run_git(fixture,'update-ref','refs/remotes/origin/main',head)
    write_json(provider/'state.json',{'bare':str(bare),'prs':[]})
    executable=provider/'bin/gh';executable.write_text('#!'+sys.executable+'\n'+PROVIDER);executable.chmod(0o755)
    ref=public['task_locator']
    write_json(fixture/stage_result.PUBLIC_INPUT,{'profile':'delivery_completion','mode':'workflow',
        'task_ref':ref,'task_key':{'task_id':public['delivery_key']['task_id'],'lifecycle_generation':0}})
    from adapters.eval.fixture_io import public_input_path
    write_json(public_input_path(request), json.loads((fixture/stage_result.PUBLIC_INPUT).read_text()))
    (fixture/stage_result.REASONING).parent.mkdir(parents=True,exist_ok=True)
    (fixture/stage_result.REASONING).write_text('# Continuous native observation\n\nNot yet executed.\n')
    write_json(fixture/stage_result.FACTS,{
        'continuous_chain':True,'required_reads':[*files,ref+'/prd.md',stage_result.PUBLIC_INPUT,
            '.trellis/workflow.md','.trellis/spec/workflow/clear-technical-writing.md'],
        'task_ref':ref,'delivery_key':public['delivery_key'],
        'planning_root':directory.relative_to(fixture/ref).as_posix(),
        'writable_paths':[stage_result.REASONING,'interval.py','range_filter.py','test_interval.py',
            'docs/current-usage.md','docs/history-d1.md',
            *RAW_OBSERVATION_PATHS,
            *[path for path in files if path.startswith('docs/')]],
        'contribution_locator':'docs/requirements-design-test-contributions/stage-chain',
        'owner_mutated_paths':[ref+'/task.json'], 'initial_head':head,
        'task_checkout':{'task_id':resources.task_id,'registered_checkout':str(acquisition.checkout.path)},
        'python_executable':sys.executable,'provider_bin':str(provider/'bin'),
        'public_input_locator':stage_result.PUBLIC_INPUT,
        'boundary':'Only source, Task scope and D1 identity are staged. No semantic gate or delivered fact exists.'})


def context(repository, facts):
    lines = [
        ('Continue this same native Task from its actual current state and preceding original commands, including their actual arguments, stdin and responses. Inspect a failed call before authoring its correction. Do not recreate Deliveries or replay completed mutations. Read the continuation locator and determine the next original owner yourself.'
         if facts.get('continuation_locator') else
         'This is one continuous native Task with two actual Deliveries. Start with the existing unreviewed D1 identity; no historical gate is supplied.'),
        'Read full docs/source.md and the actual public state. Execute original Planning, fresh independent Architecture, Wording, Approval and Activation. D1 covers the contract partial slice. Author its real contract/current temporary guidance and applicable tests. Execute candidate Check, original RDT final_integration, actual rebind, final Check, original commit, complete committed Review, Delivery Review, Publication and Merge.',
        'Then create D2 in the same Task by its original owner, consuming actual D1 stdout. D2 implements the remaining source requirement. Exercise an ordinary initial half-open design proposal against the inclusive source through the original owner before revising that design lawfully and re-entering its owner. Do not change accepted scope to accommodate the proposal. Subsequent implementation and current guidance/assertions follow your accepted plan.',
        'Execute D2 original Planning/independent Architecture/Approval/Activation, actual implementation/validation, candidate Check, RDT actual final_integration and readback, real candidate rebind, final Check, local commit, complete committed Review, Delivery Review and Merge. Finally invoke original whole Task Completion using actual preceding outputs. No host result, pass, finding or route is provided. Judge each gate and remaining boundary yourself.',
        'All wrappers and schemas are installed under .trellis/guru-team/skills/packages. Use helper run for original help, read-only Git and source reads, bounded file authoring and concrete commands. Use helper command for original semantic invocations and their recorder/checker IDs. Load each exact owner contract before use; examples explain syntax but are not evidence or answers.',
        'Before forwarding your input, check its exact selected installed schema, including referenced definitions and literal values. Schema validity is only an input check; it does not establish semantic suitability or an exit.',
        'Each original owner defines its own current identity and freshness contract. Read that owner\'s public identity command and use its actual current stdout after relevant writes. Equal field names do not make another owner\'s opaque token interchangeable. Earlier command outputs remain historical when their content has changed.',
        'Use the fact sheet contribution_locator for the original RDT isolated contribution. The writable docs/chain-evidence paths carry your actual before/current source, diff and command observations for the fresh reviewer. They contain raw execution facts, not a supplied judgment.',
        'Fresh independent Architecture uses helper command --skill-id guru-maintain-architecture-baseline --command independent-review --stdin with JSON {"public_input":<your original input object>,"reads":[<ordered repository-relative path strings>]}. Do not pass reads as objects with embedded content. Prepare real current source/diff/validation for that independent worker and keep Task/implement narratives out of its first reads. Supply actual current token values, not example hashes. New files can be read through original run stdout.',
        'independent-review can take several minutes. When the shell returns a running session ID, poll that same session until completion. Do not relaunch the pending call because it is silent.',
        'A running session remains pending; elapsed time alone does not establish a missing capability or an execution failure. Continue polling the same session until it returns an actual result or execution error. Do not end this native segment while its independent owner is still running.',
        'The deterministic external provider is at '+facts['provider_bin']+'. Prepend it to PATH for original GitHub I/O commands. It implements real local Git commits/refs behind GitHub-shaped I/O. It never writes Task/Delivery facts or supplies semantic results. Git origin URL maps to its local bare remote. This is not real GitHub, production or adoption evidence.',
        'Keep inputs and semantic JSON under the original ignored eval runtime. Consumed input/semantic file arguments are removed after each successful original wrapper; regenerate a file when another invocation needs it. Original wrappers own public Task/Delivery writes. Do not import test fixture builders, seed gates, call record_gate directly or fabricate Publication/Delivery facts. Only original producer stdout may supply each next-stage input. A nonzero original wrapper ends this invocation; preserve the error rather than retrying its closed FIFO.',
        'Use final:true only for the final original Completion invocation. Preserve intermediate original stdout and actual validation under the existing private command receipts. Return only that final original wrapper stdout.',
    ]
    previous = os.environ.get(RESUME_PROTOCOL_ENV)
    if previous:
        protocol = json.loads(Path(previous).read_text())
        if not (Path(protocol['native_request_path']).parent / 'adapter-transcript.json').exists():
            error = (Path(protocol['model_root']) / 'output/native-last-message.txt').read_text()
            lines.insert(0, 'The preceding segment failed in test transport finalization and remains execution_error/no-grade. '
                'Its last command argv and native process returncode are unavailable. Do not reconstruct or replay that command. '
                'Read actual current Git, Task and files before choosing the next original owner. '
                'Retain existing stashes and original failed records. The live carriers are test inputs; keep them available.\n'
                'Actual preceding native error:\n' + error + '\nLive repository observations:\n'
                + json.dumps(_live_transport_observations(Path(protocol['owner_repository'])), ensure_ascii=False))
    return '\n'.join(lines)


def resume_execution(request):
    """Continue an ended native segment in its actual checkout, without seeding gates."""
    protocol_path = Path(os.environ[RESUME_PROTOCOL_ENV]).resolve()
    failed = inspect_resume_segment(request, protocol_path)
    return _continue_existing_fixture(request, json.loads(protocol_path.read_text()),
                                      restore_missing_specs=failed is None)


def inspect_resume_segment(request, protocol_path):
    """Check an ended segment or its actual failed-finalization evidence, without writes."""
    protocol = json.loads(protocol_path.read_text())
    first = json.loads(Path(protocol['native_request_path']).read_text())
    transcript = Path(protocol['native_request_path']).parent / 'adapter-transcript.json'
    if request['case_id'] != CASE or first['case_id'] != CASE:
        raise ValueError('chain continuation requires an ended actual native chain segment')
    if transcript.is_file():
        if 'returncode' not in json.loads(transcript.read_text()):
            raise ValueError('chain continuation requires an ended actual native chain segment')
        return None
    last_message = Path(protocol['model_root']) / 'output/native-last-message.txt'
    if not last_message.is_file() or not last_message.read_text().strip():
        raise ValueError('chain continuation requires an ended actual native chain segment')
    return inspect_failed_transport_segment(request, protocol_path)


def _existing_fixture(request, protocol):
    """Read the original fixture and matching production packages."""
    from adapters.eval import stage_result_authoring as stage_result
    from adapters.eval.eval_support import package_tree_sha256
    repository = Path(protocol['owner_repository']).resolve()
    facts = json.loads((repository / stage_result.FACTS).read_text())
    if not facts.get('continuous_chain'):
        raise ValueError('chain continuation requires its original Task fixture')
    package = repository / '.trellis/guru-team/skills/packages' / request['skill_id']
    sources = Path(request['package_root']).resolve().parent
    for skill in stage_result.ImplementationCommands.owners:
        if package_tree_sha256(package.parent / skill) != package_tree_sha256(sources / skill):
            raise ValueError('chain continuation production package differs: ' + skill)
    return repository, facts, package


def _partial_protocol(request, protocol_path):
    from adapters.eval import stage_result_authoring as stage_result
    protocol = json.loads(Path(protocol_path).read_text())
    native_path = Path(protocol['native_request_path'])
    native_bytes = native_path.read_bytes()
    first = json.loads(native_bytes)
    if (request.get('case_id') != CASE or first.get('case_id') != CASE
            or first.get('skill_id') != request['skill_id']
            or first.get('native_execution_mode') != 'semantic_authoring'
            or not protocol.get('semantic_authoring') or not protocol.get('implementation_commands')
            or protocol.get('implementation_facts_locator') != stage_result.FACTS
            or hashlib.sha256(native_bytes).hexdigest() != protocol['request_sha256']):
        raise ValueError('interrupted chain protocol and native request differ')
    return protocol


def _partial_trace(protocol):
    from adapters.eval.eval_constants import stdout_digest
    trace = json.loads(Path(protocol['trace_path']).read_text())
    if (trace.get('request_sha256') != protocol['request_sha256']
            or any(trace.get(name) != protocol.get(name)
                   for name in ('projection_root', 'skill_sha256', 'wrapper_sha256'))
            or any(event.get('request_sha256') != protocol['request_sha256']
                   for event in trace['events'])):
        raise ValueError('interrupted chain trace has a different native request binding')
    receipts = json.loads(Path(protocol['implementation_receipts_path']).read_text())
    commands = [event for event in trace['events'] if event['kind'] == 'command']
    for event, row in zip(commands, receipts):
        call, result = row['request'], row['response']
        expected = {'kind': 'command', 'skill_id': call['skill_id'], 'command': call['command'],
            'arguments': call['arguments'],
            'stdin_sha256': hashlib.sha256(call['stdin'].encode()).hexdigest(),
            'returncode': result['returncode'], 'stdout_sha256': stdout_digest(result['stdout']),
            'stderr_sha256': hashlib.sha256(result['stderr'].encode()).hexdigest(),
            'request_sha256': protocol['request_sha256']}
        if event != expected:
            raise ValueError('interrupted chain trace differs from the actual command receipt')
        try:
            envelope = json.loads(call['stdin'])
        except json.JSONDecodeError:
            envelope = None
        if (isinstance(envelope, dict) and envelope.get('final') is True
                and 'invocation' in envelope and result['returncode'] == 0):
            raise ValueError('interrupted chain already has a final original wrapper result')
    return commands, receipts


def _recorded_delivery_progression(repository, facts, projection, current, receipts):
    """Read the original delivered slice and its next Creation/Selection result."""
    origin = facts['delivery_key']
    key = current.get('key')
    record = projection.read_record()
    task_key = {'task_id': record['id'], 'lifecycle_generation': record['lifecycle_generation']}
    if (not isinstance(key, dict)
            or any(origin.get(name) != value or key.get(name) != value
                   for name, value in task_key.items())):
        return False
    deliveries = [row for row in record['deliveries']
                  if row['lifecycle_generation'] == task_key['lifecycle_generation']]
    ids = [row['id'] for row in deliveries]
    if (origin['delivery_id'] not in ids or key['delivery_id'] not in ids
            or ids.index(key['delivery_id']) != ids.index(origin['delivery_id']) + 1):
        return False
    previous = projection.resolve(origin)
    delivered = previous['delivery_result']
    if (previous['phase'] != 'delivered' or delivered is None
            or delivered['owner_id'] != 'guru-merge-task-delivery'):
        return False
    selected = projection.resolve(key)
    history = []
    if facts.get('continuation_locator'):
        history = json.loads((repository / facts['continuation_locator']).read_text())['preceding_commands']
    merged = False
    for row in [*history, *receipts]:
        call, response = row['request'], row['response']
        skill = call['skill_id']
        if (response['returncode'] or skill not in ('guru-merge-task-delivery', 'guru-create-delivery')
                or call['command'] not in ('invoke', 'invoke-' + skill)):
            continue
        output = json.loads(response['stdout'])
        if output.get('task_ref') != facts['task_ref']:
            continue
        if (skill == 'guru-merge-task-delivery' and output.get('exit_id') == 'delivered'
                and output.get('task_key') == task_key):
            merged = True
        # The original Creation invocation selects this exact key before it
        # emits created. Live current selection must independently agree.
        if (merged and skill == 'guru-create-delivery' and output.get('exit_id') == 'created'
                and output.get('delivery_key') == key
                and output.get('planning_root') == selected['planning_root']):
            return True
    return False


def _selected_fixture(request, protocol, *, receipts=None):
    from runtime.delivery_projection.adapter import DeliveryProjection
    repository, facts, _ = _existing_fixture(request, protocol)
    projection = DeliveryProjection(repository, facts['task_ref'])
    context_id = protocol.get('implementation_context_id') or 'architecture-delivery-eval'
    previous = os.environ.get('TRELLIS_CONTEXT_ID')
    os.environ['TRELLIS_CONTEXT_ID'] = context_id
    try:
        current = projection.current(facts['delivery_key'])
    finally:
        if previous is None:
            os.environ.pop('TRELLIS_CONTEXT_ID', None)
        else:
            os.environ['TRELLIS_CONTEXT_ID'] = previous
    if (current.get('kind') != 'current'
            or (current.get('key') != facts['delivery_key']
                and (receipts is None or not _recorded_delivery_progression(
                    repository, facts, projection, current, receipts)))):
        raise ValueError('interrupted chain requires its same current Task and Delivery')
    return repository, facts, projection, current['key']


def _live_transport_observations(repository):
    """Expose real side effects; an absent receipt never establishes a no-op."""
    return {'head': run_git(repository, 'rev-parse', 'HEAD'),
        'status': run_git(repository, 'status', '--short'),
        'refs': run_git(repository, 'show-ref'),
        'diff_stat': run_git(repository, 'diff', '--stat', 'HEAD'),
        'carrier_files': {path: hashlib.sha256((repository / path).read_bytes()).hexdigest()
                          if (repository / path).is_file() else None for path in CARRIER_PATHS}}


def inspect_failed_transport_segment(request, protocol_path):
    """Read one failed local transport tail and current state, without completing its history."""
    from adapters.eval.eval_support import package_tree_sha256
    protocol = _partial_protocol(request, protocol_path)
    native_path = Path(protocol['native_request_path'])
    if (native_path.parent / 'adapter-transcript.json').exists():
        raise ValueError('failed transport recovery requires the missing original transcript')
    commands, receipts = _partial_trace(protocol)
    if (not receipts or len(commands) != len(receipts) + 1
            or any(row['request']['skill_id'] != 'implementation-authoring' for row in receipts)
            or receipts[0]['request']['command'] != 'inspect'
            or receipts[0]['response']['returncode'] != 0):
        raise ValueError('failed transport recovery requires a receipt-backed local prefix and one failed run tail')
    tail = commands[-1]
    message = (Path(protocol['model_root']) / 'output/native-last-message.txt').read_text().strip()
    if (tail['skill_id'] != 'implementation-authoring' or tail['command'] != 'run'
            or tail['returncode'] == 0 or not message
            or hashlib.sha256(message.encode()).hexdigest() != tail['stderr_sha256']):
        raise ValueError('failed transport recovery requires the actual native transport error')
    repository, facts, projection, _ = _selected_fixture(request, protocol)
    source_runtime = Path(request['runtime_target']).resolve().parents[2] / 'runtime'
    if package_tree_sha256(repository / '.trellis/guru-team/runtime') != package_tree_sha256(source_runtime):
        raise ValueError('chain continuation shared runtime differs')
    observed = json.loads(receipts[0]['response']['stdout'])
    live = _live_transport_observations(repository)
    if projection.read_record() != observed['task'] or live['head'] != observed['head']:
        raise ValueError('failed transport owner state changed; reread its original owners')
    if any(value is None for value in live['carrier_files'].values()):
        raise ValueError('failed transport recovery requires the real restored carriers')
    return {'owner_repository': str(repository), 'task_ref': facts['task_ref'],
            'delivery_key': facts['delivery_key'], 'native_error': message, 'live': live}


def inspect_interrupted_segment(request, protocol_path):
    """Read an explicitly selected partial segment; choose no workflow route."""
    protocol = _partial_protocol(request, protocol_path)
    native_path = Path(protocol['native_request_path'])
    transcript = native_path.parent / 'adapter-transcript.json'
    last_message = Path(protocol['model_root']) / 'output/native-last-message.txt'
    if ((transcript.is_file() and 'returncode' in json.loads(transcript.read_text()))
            or (last_message.is_file() and last_message.read_text().strip())):
        raise ValueError('interrupted chain already has an ended native result')
    commands, receipts = _partial_trace(protocol)
    if not commands or len(commands) != len(receipts):
        raise ValueError('interrupted chain trace is missing actual command receipts')
    repository, facts, projection, key = _selected_fixture(request, protocol, receipts=receipts)
    delivery = projection.resolve(key)
    return {'owner_repository': str(repository), 'task_ref': facts['task_ref'],
        'delivery_key': key, 'planning_root': delivery['planning_root'],
        'head': run_git(repository, 'rev-parse', 'HEAD'), 'command_count': len(receipts),
        'preceding_owner_command_count': sum(
            row['request']['skill_id'] != 'implementation-authoring' for row in receipts)}


def resume_interrupted_execution(request):
    """Expose original partial commands to a fresh caller in the same fixture."""
    protocol_path = Path(os.environ[INTERRUPTED_PROTOCOL_ENV]).resolve()
    inspect_interrupted_segment(request, protocol_path)
    return _continue_existing_fixture(request, json.loads(protocol_path.read_text()),
                                      restore_missing_specs=False)


def _continue_existing_fixture(request, protocol, *, restore_missing_specs=True):
    from adapters.eval import stage_result_authoring as stage_result
    from adapters.eval.fixture_io import public_input_path
    from runtime.delivery_projection.adapter import DeliveryProjection
    repository, facts, package = _existing_fixture(request, protocol)
    sources = Path(request['package_root']).resolve().parent
    # Recover the installed-fixture copy omission without replacing the Task,
    # planning, original gates or business files from the ended segment.
    installed_specs = sources.parents[3] / '.trellis/spec'
    if (restore_missing_specs and not (repository / '.trellis/spec').exists()
            and installed_specs.is_dir()):
        import shutil
        shutil.copytree(installed_specs, repository / '.trellis/spec')
    projection = DeliveryProjection(repository, facts['task_ref'])
    record = projection.read_record()
    facts['planning_root'] = projection.resolve(facts['delivery_key'])['planning_root']
    receipts = json.loads(Path(protocol['implementation_receipts_path']).read_text())
    locator = '.trellis/tasks/stage-result-evidence/continuation.json'
    continuation = repository / locator
    preceding = (json.loads(continuation.read_text())['preceding_commands']
                 if continuation.is_file() else [])
    # Earlier original exits can have no durable public gate. Keep their actual
    # responses across segments; the executing AI still chooses the next owner.
    preceding.extend([{'request': {'skill_id': row['request']['skill_id'],
                             'command': row['request']['command'],
                             'arguments': row['request']['arguments'],
                             'stdin': row['request']['stdin']},
                  'response': {'returncode': row['response']['returncode'],
                               'stdout': row['response']['stdout'],
                               'stderr': row['response']['stderr'].splitlines()[0]
                                   if row['response']['stderr'] else ''}}
                 for row in receipts if row['request']['skill_id'] != 'implementation-authoring'])
    write_json(repository / locator, {'preceding_commands': preceding,
        'current_task': record, 'head': run_git(repository, 'rev-parse', 'HEAD')})
    facts['required_reads'] = sorted(set([*facts['required_reads'], locator]))
    facts['continuation_locator'] = locator
    facts['contribution_locator'] = 'docs/requirements-design-test-contributions/stage-chain'
    facts['writable_paths'] = sorted(set([*facts['writable_paths'],
        *RAW_OBSERVATION_PATHS]))
    write_json(repository / stage_result.FACTS, facts)
    write_json(public_input_path(request), json.loads((repository / stage_result.PUBLIC_INPUT).read_text()))
    return package, repository / '.trellis/guru-team/scripts/bash/run-skill-command.sh', {
        'TRELLIS_CONTEXT_ID': protocol.get('implementation_context_id') or 'architecture-delivery-eval'}
