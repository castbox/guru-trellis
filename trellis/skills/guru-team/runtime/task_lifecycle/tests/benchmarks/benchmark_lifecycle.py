"""Disposable real-public-wrapper lifecycle benchmark; no business Task mutation."""
import argparse
from collections import Counter
import hashlib, importlib.util, json, os, re, shlex, shutil, statistics, subprocess, sys, time
from pathlib import Path
p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--fork', type=Path, required=True)
p.add_argument('--entry', choices=['create', 'binding'], required=True)
p.add_argument('--count', type=int, required=True)
p.add_argument('--pass', dest='measurement', choices=['timing', 'volume', 'rss', 'profile'], default='timing')
p.add_argument('--output', type=Path, required=True)
p.add_argument('--pool', type=Path)
p.add_argument('--repeats', type=int, default=2)
p.add_argument('--installed', action='store_true', help='Prepare original canonical preset installation outside each operation timer')
a = p.parse_args()
a.source = a.source.resolve()
a.fork = a.fork.resolve()
a.output = a.output.resolve()
a.output.mkdir(parents=True)
if a.count < 1 or a.repeats < 1:
    p.error('positive count and repeats required')
if sys.version_info[:2] != (3, 14):
    p.error('run with the selected managed Python3.14, not PATH default')
skills = a.source / 'trellis/skills/guru-team'
sys.path.insert(0, str(skills))
scripts = a.fork / 'packages/cli/src/templates/trellis/scripts'
os.environ['GURU_UPSTREAM_DELIVERY_SCRIPTS'] = str(scripts)

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m
creation = module('d3_creation_fixture', skills / 'packages/guru-create-task/tests/test_contract.py')
binding = module('d3_binding_fixture', skills / 'packages/guru-establish-task-branch-binding/tests/test_contract.py')
helpers = module('d3_git_helpers', skills / 'packages/guru-merge-task-delivery/tests/benchmark_git_objects.py')
realgit = shutil.which('git')
baseline_env = {k: v for k, v in os.environ.items() if not k.startswith(('TRELLIS_', 'CODEX_', 'CLAUDE_', 'CURSOR_', 'GIT_'))}
baseline_env['TRELLIS_CONTEXT_ID'] = 'lifecycle-benchmark'

def git(root, *args):
    return subprocess.run([realgit, *args], cwd=root, check=True, capture_output=True, text=True).stdout.strip()

def make_creation():
    case = creation.CreateTaskTests('test_adopt_no_issue_create_and_read_only_recovery')
    case.setUp()
    return case

def pool():
    target = (a.pool or a.output / 'existing-pool').resolve()
    if target.exists():
        manifest = json.loads((target / 'manifest.json').read_text())
        if manifest['count'] != a.count or manifest['fork_head'] != git(a.fork, 'rev-parse', 'HEAD'):
            raise ValueError('Pool input does not match')
        return (target, manifest)
    target.mkdir(parents=True)
    case = make_creation()
    try:
        logs = []
        for index in range(a.count):
            slug = f'existing-{index:06d}'
            command = [sys.executable, str(case.primary / '.trellis/scripts/task.py'), 'create', 'Existing ' + f'{index:06d}', '--description', 'Fixed existing Task fixture', '--slug', slug, '--task-id', slug, '--schema-version', '2.0', '--source-json', '{"kind":"no_issue"}', '--base-branch', 'main', '--no-start']
            result = subprocess.run(command, cwd=case.primary, env={**baseline_env, 'TZ': 'Asia/Shanghai'}, capture_output=True, text=True)
            logs.append(result.stdout + result.stderr)
            if result.returncode:
                raise RuntimeError(logs[-1])
        shutil.copytree(case.primary / '.trellis/tasks', target / 'tasks')
        paths = sorted((target / 'tasks').glob('*/task.json'))
        sizes = [q.stat().st_size for q in paths]
        manifest = {'count': a.count, 'fork_head': git(a.fork, 'rev-parse', 'HEAD'), 'official_task_store_sha256': hashlib.sha256((scripts / 'common/task_store.py').read_bytes()).hexdigest(), 'task_json_sizes': sorted(set(sizes)), 'task_ids': [json.loads(q.read_text())['id'] for q in paths], 'preparation': 'real original task.py create --schema-version2.0 --no-start; existing active fixture records, not archived/completed; no bindings/ledgers copied', 'interpreter': sys.executable, 'python_version': sys.version}
        (target / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
        (target / 'official-preparation.log').write_text(''.join(logs))
        return (target, manifest)
    finally:
        case.doCleanups()

def prepare():
    start = time.perf_counter()
    if a.entry == 'create':
        prepared, manifest = pool()
        case = make_creation()
        shutil.copytree(prepared / 'tasks', case.primary / '.trellis/tasks')
        git(case.primary, 'add', '.trellis/tasks')
        git(case.primary, 'commit', '-qm', 'existing official Task fixture records')
        git(case.root, 'merge', '--ff-only', 'main')
        head = git(case.root, 'rev-parse', 'HEAD')
        case.payload['creation']['reviewed_base_head'] = head
        case.payload['acquisition']['decision_head'] = head
        chain = [('guru-create-task', case.payload, 'created'), ('guru-ensure-task-checkout', {'profile': 'delivery_active_task', 'mode': 'workflow', 'task_id': 'example-task', 'lifecycle_generation': 0}, 'checkout_resolved')]
        recovery = ('guru-create-task', {**case.payload, 'action': 'recover_created_task_result'}, 'created')
    else:
        case = binding.BranchBindingTests('test_unique_candidate_establishes_once_and_recovers_without_write')
        case.setUp()
        head = git(case.root, 'rev-parse', 'HEAD')
        base = git(case.root, 'rev-parse', 'main')
        for index in range(a.count):
            git(case.root, 'branch', f'other-{index:06d}', base)
        manifest = {'count': a.count, 'extra_branch_heads': 'same immutable no-target-Task head; unique registered target Task branch', 'task_json_size': (case.root / '.trellis/tasks/demo/task.json').stat().st_size}
        chain = [('guru-establish-task-branch-binding', case.input, 'binding_established')]
        recovery = ('guru-establish-task-branch-binding', {**case.input, 'action': 'recover', 'recovery': {'expected_revision': 0, 'expected_branch_name': 'task/demo', 'expected_head': head}}, 'binding_established')
    if a.installed:
        before_tasks = {str(q.relative_to(case.root)): q.stat().st_size for q in (case.root / '.trellis/tasks').glob('*/task.json')}
        shutil.copytree(scripts, case.root / '.trellis/scripts', dirs_exist_ok=True)
        (case.root / '.trellis/.version').write_text('0.7.0-castbox.3\n')
        (case.root / '.trellis/workflow.md').write_bytes((a.source / 'trellis/workflows/guru-team/workflow.md').read_bytes())
        (case.root / '.gitignore').write_text('.trellis/.runtime/\n')
        installer = a.source / 'trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py'
        result = subprocess.run([sys.executable, str(installer), '--repo', str(case.root), '--python', sys.executable, '--json'], text=True, capture_output=True, env=baseline_env)
        (a.output / f'install-{len(samples)}.stdout.json').write_text(result.stdout)
        (a.output / f'install-{len(samples)}.stderr.log').write_text(result.stderr)
        if result.returncode:
            raise RuntimeError('Original installed fixture apply failed: ' + result.stderr)
        git(case.root, 'config', 'user.name', 'Test')
        git(case.root, 'config', 'user.email', 'test@example.invalid')
        git(case.root, 'add', '.')
        git(case.root, 'commit', '-qm', 'install current preset')
        head = git(case.root, 'rev-parse', 'HEAD')
        if a.entry == 'create':
            git(case.primary, 'merge', '--ff-only', head)
            case.payload['creation']['reviewed_base_head'] = head
            case.payload['acquisition']['decision_head'] = head
        else:
            recovery[1]['recovery']['expected_head'] = head
        after_tasks = {str(q.relative_to(case.root)): q.stat().st_size for q in (case.root / '.trellis/tasks').glob('*/task.json')}
        actual = case.root / '.trellis/guru-team/skills'
        compared = []
        for relative in ['runtime/task_lifecycle/git_facts.py', 'runtime/task_lifecycle/composition.py', 'runtime/task_lifecycle/branch_resolution.py', 'packages/guru-create-task/runtime/invoke.py', 'packages/guru-establish-task-branch-binding/runtime/invoke.py', 'packages/guru-ensure-task-checkout/runtime/invoke.py']:
            source_bytes = (skills / relative).read_bytes()
            installed_path = case.root / '.trellis/guru-team' / relative if relative.startswith('runtime/') else actual / relative
            installed_bytes = installed_path.read_bytes()
            if source_bytes != installed_bytes:
                raise RuntimeError('Installed source differs: ' + relative)
            compared.append({'path': relative, 'sha256': hashlib.sha256(source_bytes).hexdigest()})
        all_compared = []
        for prefix, target in [('runtime', case.root / '.trellis/guru-team/runtime'), ('packages', actual / 'packages')]:
            for installed in sorted(target.rglob('*')):
                if not installed.is_file() or '__pycache__' in installed.parts:
                    continue
                relative = str(installed.relative_to(target))
                canonical = skills / prefix / relative
                if canonical.is_file():
                    if installed.read_bytes() != canonical.read_bytes():
                        raise RuntimeError('Installed byte drift: ' + prefix + '/' + relative)
                    all_compared.append(prefix + '/' + relative)
        resolver = case.root / '.trellis/guru-team/runtime/resolve-python.sh'
        check = subprocess.run([str(resolver), str(case.root), str(case.root / '.trellis/guru-team/runtime'), '-c', 'import sys,json; print(json.dumps({"executable":sys.executable,"version":sys.version}))'], capture_output=True, text=True, check=True, env=baseline_env)
        runtime = json.loads(check.stdout)
        if runtime['executable'] != sys.executable:
            raise RuntimeError('Installed runtime differs from source managed interpreter: ' + str(runtime))
        manifest = {**manifest, 'installed': {'source_head': git(a.source, 'rev-parse', 'HEAD'), 'installer': str(installer), 'installer_sha256': hashlib.sha256(installer.read_bytes()).hexdigest(), 'preparation': 'original fixture canonical workflow and original Python preset installer via source managed sys.executable; commit, create primary FF, heads refreshed; all timer external', 'task_json_before': before_tasks, 'task_json_after': after_tasks, 'additional_task_paths': sorted(set(after_tasks) - set(before_tasks)), 'verified_source_files': compared, 'all_compared_installed_paths': all_compared, 'runtime': runtime}}
    return (case, chain, recovery, manifest, time.perf_counter() - start)

def observer(case, directory):

    class Args:
        pass
    args = Args()
    args.output = directory
    args.measurement = a.measurement
    case.bin = directory / 'bin'
    case.bin.mkdir()
    trace = helpers.install_observer(case, args)
    path = case.bin / 'git'
    s = path.read_text().replace('*cat-file*--batch*', '*cat-file*" --batch "*')
    path.write_text(s)
    return trace

def trace_counts(path, start=0, end=None):
    counts = Counter()
    requests = Counter()
    with path.open('rb') as stream:
        stream.seek(start)
        while end is None or stream.tell() < end:
            line = stream.readline()
            if not line:
                break
            event = json.loads(line)
            if event.get('event') != 'start':
                continue
            argv = event['argv']
            counts['git'] += 1
            for name in ['cat-file', 'show', 'ls-tree']:
                if name in argv:
                    counts[name] += 1
            if 'show' in argv:
                tail = argv[argv.index('show') + 1:]
                for value in tail:
                    if not value.startswith('-') and ':' in value:
                        requests[value] += 1
            if 'cat-file' in argv:
                tail = argv[argv.index('cat-file') + 1:]
                if len(tail) == 2 and tail[0] in ['blob', '-p']:
                    requests[tail[1]] += 1
    return (dict(counts), requests)

def volume(case, directory, requests):
    requests = Counter(requests)
    for path in directory.glob('batch-*.requests'):
        with path.open() as stream:
            for line in stream:
                requests[line.strip()] += 1
    request = directory / 'size-probe.input'
    response = directory / 'size-probe.output'
    request.write_text(''.join((value + '\n' for value in requests)))
    with request.open('rb') as inp, response.open('wb') as out:
        subprocess.run([realgit, 'cat-file', '--batch-check'], cwd=case.root, stdin=inp, stdout=out, stderr=subprocess.PIPE, check=True)
    success = Counter()
    sizes = {}
    missing = 0
    other = Counter()
    with response.open() as stream:
        for expression, line in zip(requests, stream, strict=True):
            fields = line.split()
            if len(fields) == 2 and fields[-1] == 'missing':
                missing += requests[expression]
                continue
            if len(fields) != 3:
                raise ValueError('Invalid object probe: ' + line)
            oid, kind, size = fields
            if kind == 'blob':
                success[oid] += requests[expression]
                sizes[oid] = int(size)
            else:
                other[kind] += requests[expression]
    return {'captured_batch_request_files': [q.name for q in directory.glob('batch-*.requests')], 'attempted_content_requests': sum(requests.values()), 'successful_blob_requests': sum(success.values()), 'unique_blob_oids': len(success), 'successful_blob_bytes': sum((sizes[k] * v for k, v in success.items())), 'unique_blob_bytes': sum(sizes.values()), 'largest_blob': max(sizes.values(), default=0), 'missing_path_requests': missing, 'other_object_requests': dict(other), 'requests_by_expression': dict(requests), 'successful_requests_by_oid': dict(success), 'scope': 'scalar show head:path and cat-file content plus regular-file batch input; metadata -e excluded; post-operation probes outside timer/trace; logical returned bytes, not physical IO'}

def call(case, skill, payload, ordinal, directory, env, expected, *, recovery=False):
    package = (case.root / '.trellis/guru-team/skills/packages' if a.installed else skills / 'packages') / skill
    name = ('recovery-' if recovery else '') + f'{ordinal}-{skill}'
    source_input = directory / (name + '.input.json')
    source_input.write_text(json.dumps(payload))
    if a.measurement == 'profile' and (not recovery):
        command = [sys.executable, str(Path(__file__).with_name('profile_dispatcher.py')), str(directory / (name + '.profile.json')), str(package), 'invoke-' + skill]
        environment = {**env, 'PYTHONPATH': str(skills)}
    else:
        command = ['bash', str(package / 'scripts/invoke.sh')]
        environment = env
        if a.measurement == 'rss' and (not recovery):
            command = ['/usr/bin/time', '-l', '-a', '-o', str(directory / (name + '.rss')), *command]
    start = time.perf_counter()
    result = subprocess.run([*command, '--root', str(case.root), '--input', str(source_input)], env=environment, text=True, capture_output=True)
    elapsed = time.perf_counter() - start
    (directory / (name + '.stdout.json')).write_text(result.stdout)
    (directory / (name + '.stderr.log')).write_text(result.stderr)
    value = json.loads(result.stdout or result.stderr)
    value = value.get('result', value)
    if result.returncode or value.get('exit_id') != expected:
        raise RuntimeError({'command': command, 'returncode': result.returncode, 'result': value})
    return {'skill': skill, 'seconds': elapsed, 'exit_id': value['exit_id'], 'recovery': recovery}
samples = []
for sample in range(a.repeats):
    directory = a.output / f'sample-{sample}'
    directory.mkdir()
    case = None
    try:
        case, chain, recover, manifest, preparation = prepare()
        trace = observer(case, directory)
        env = {**baseline_env, 'PATH': str(case.bin) + os.pathsep + baseline_env['PATH'], 'GURU_D3_TRACE': str(trace)}
        operation = time.perf_counter()
        calls = []
        ranges = []
        for index, (skill, payload, expected) in enumerate(chain):
            begin = trace.stat().st_size if trace.exists() else 0
            calls.append(call(case, skill, payload, index, directory, env, expected))
            end = trace.stat().st_size
            ranges.append((begin, end))
        elapsed = time.perf_counter() - operation
        counts, requests = trace_counts(trace)
        stage_counts = [trace_counts(trace, begin, end)[0] for begin, end in ranges]
        for c, n, limits in zip(calls, stage_counts, ranges):
            c['git_counts'] = n
            c['trace_start'] = limits[0]
            c['trace_end'] = limits[1]
        row = {'trace_operation_end': ranges[-1][1], 'sample': sample, 'seconds': elapsed, 'preparation_seconds': preparation, 'calls': calls, **counts, 'fixture': manifest, 'branch_refs': git(case.root, 'for-each-ref', '--format=%(refname)', 'refs/heads').splitlines(), 'worktree_count': len([x for x in git(case.root, 'worktree', 'list', '--porcelain').splitlines() if x.startswith('worktree ')])}
        if a.measurement == 'volume':
            row['volume'] = volume(case, directory, requests)
        if a.measurement == 'rss':
            row['wrapper_invocation_maxrss_bytes'] = {q.name: [int(x) for x in re.findall('(\\d+)\\s+maximum resident set size', q.read_text())] for q in directory.glob('*.rss') if q.name != 'git.rss'}
            row['git_individual_maxrss_bytes'] = max((int(x) for x in re.findall('(\\d+)\\s+maximum resident set size', (directory / 'git.rss').read_text())))
            row['rss_scope'] = 'BSDtime max individual process RSS per real public-wrapper invocation (official writer subprocess retained) and per Git command; not simultaneous sum or pure-parent-Python RSS; Python parent/writer not separately attributed'
        begin = trace.stat().st_size
        recovered = call(case, *recover[:2], 99, directory, env, recover[2], recovery=True)
        end = trace.stat().st_size
        recovered['git_counts'] = trace_counts(trace, begin, end)[0]
        recovered['trace_start'] = begin
        recovered['trace_end'] = end
        row['recovery'] = recovered
        samples.append(row)
        (directory / 'summary.json').write_text(json.dumps(row, indent=2) + '\n')
        print(json.dumps({'sample': sample, 'seconds': elapsed, 'git_counts': counts, 'calls': calls, 'recovery': recovered}), flush=True)
    except BaseException:
        if case is not None:
            case.temporary._finalizer.detach()
            print(json.dumps({'failed_fixture_retained': str(case.root)}), flush=True)
        raise
    else:
        case.doCleanups()
report = {'entry': a.entry, 'count': a.count, 'pass': a.measurement, 'repeats': a.repeats, 'source_head': git(a.source, 'rev-parse', 'HEAD'), 'fork_head': git(a.fork, 'rev-parse', 'HEAD'), 'source': str(a.source), 'fork': str(a.fork), 'interpreter': sys.executable, 'python_version': sys.version, 'median_seconds': statistics.median((x['seconds'] for x in samples)), 'samples': samples, 'scope': 'new equivalent fixture per measured initial operation; actual public wrappers and original task.py writer retained; recoveries separate; semantic/context fixture not native AI or live GitHub proof; analyses/size probes outside complete timer'}
(a.output / 'summary.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'summary': str(a.output / 'summary.json'), 'median_seconds': report['median_seconds']}), flush=True)
