# Source-private measurement utility; not installed runtime.
import argparse, importlib.util, json, os, re, shutil, statistics, subprocess, sys, tempfile, time
from collections import Counter
from pathlib import Path
from types import SimpleNamespace
p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--fork', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
p.add_argument('--count', type=int, required=True)
p.add_argument('--mode', choices=['timing', 'rss', 'volume', 'profile'], required=True)
p.add_argument('--installed', action='store_true')
a = p.parse_args()
a.output.mkdir(parents=True)
skills = a.source / 'trellis/skills/guru-team'
sys.path.insert(0, str(skills))
os.environ['GURU_UPSTREAM_DELIVERY_SCRIPTS'] = str(a.fork / 'packages/cli/src/templates/trellis/scripts')

def module(n, path):
    s = importlib.util.spec_from_file_location(n, path)
    m = importlib.util.module_from_spec(s)
    sys.modules[n] = m
    s.loader.exec_module(m)
    return m
m = module('cleanup_fixture', skills / 'packages/guru-cleanup-task-resources/tests/test_cleanup_contract.py')
h = module('bench_helpers', skills / 'packages/guru-merge-task-delivery/tests/benchmark_git_objects.py')
from runtime.delivery_projection.tests.upstream_fixture import public_task
realgit = shutil.which('git')
env0 = {k: v for k, v in os.environ.items() if not k.startswith(('TRELLIS_', 'CODEX_', 'CLAUDE_', 'CURSOR_', 'GIT_'))}
env0['PATH'] = str(Path(sys.executable).parent) + os.pathsep + env0['PATH']

def counts(trace, beg, end):
    rows = [json.loads(x) for x in trace.read_bytes()[beg:end].splitlines()]
    commands = [x['argv'] for x in rows if x.get('event') == 'start']
    return {'git': len(commands), **{n: sum((n in c for c in commands)) for n in ['show', 'cat-file', 'ls-tree']}}
reports = []
for repeat in range(2):
    directory = a.output / f'sample-{repeat}'
    directory.mkdir()
    tmp = tempfile.TemporaryDirectory()
    root, store, public, _ = m.missing_ledger_fixture(Path(tmp.name))
    if a.installed:
        fork = a.fork
        shutil.copytree(fork / 'packages/cli/src/templates/trellis/scripts', root / '.trellis/scripts', dirs_exist_ok=True)
        (root / '.trellis/.version').write_text('0.7.0-castbox.3\n')
        (root / '.trellis/workflow.md').write_bytes((a.source / 'trellis/workflows/guru-team/workflow.md').read_bytes())
        (root / '.gitignore').write_text('.trellis/.runtime/\n')
        r = subprocess.run([sys.executable, str(a.source / 'trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py'), '--repo', str(root), '--python', sys.executable, '--json'], capture_output=True, text=True, env=env0)
        (directory / 'install.json').write_text(r.stdout)
        (directory / 'install.err').write_text(r.stderr)
        assert r.returncode == 0, r.stderr
        assert (root / '.trellis/guru-team/skills/packages/guru-cleanup-task-resources/runtime/invoke.py').read_bytes() == (skills / 'packages/guru-cleanup-task-resources/runtime/invoke.py').read_bytes()
    m.git(root, 'switch', '-qc', 'snapshot-first')
    active = root / '.trellis/tasks/demo/task.json'
    active.parent.mkdir(parents=True)
    active.write_text(json.dumps(public_task({'id': 'demo'})))
    m.git(root, 'add', '.trellis/tasks/demo/task.json')
    m.git(root, 'commit', '-qm', 'task snapshot before archival')
    head = m.git(root, 'rev-parse', 'HEAD')
    oid = m.git(root, 'rev-parse', head + ':.trellis/tasks/demo/task.json')
    size = active.stat().st_size
    for n in range(a.count):
        m.git(root, 'branch', f'snapshot-{n:03}', head)
    m.git(root, 'switch', '-q', 'main')
    available = m.CLEANUP.discover_candidates(root)
    public['selected_candidate_ids'] = [k for k, (d, i) in available.items() if d['branch_name'].startswith('snapshot-') and d['branch_name'] != 'snapshot-first' and (d['kind'] == 'local_branch')]
    assert len(public['selected_candidate_ids']) == a.count
    inp = directory / 'input.json'
    inp.write_text(json.dumps(public))
    case = SimpleNamespace(bin=directory / 'bin')
    case.bin.mkdir()
    trace = h.install_observer(case, SimpleNamespace(output=directory, measurement=a.mode))
    shim = case.bin / 'git'
    shim.write_text(shim.read_text().replace('*cat-file*--batch*', '*cat-file*" --batch "*'))
    env = {**env0, 'PATH': str(case.bin) + os.pathsep + env0['PATH']}
    package = (root / '.trellis/guru-team/skills' if a.installed else skills) / 'packages/guru-cleanup-task-resources'
    ops = []
    for phase in ['preview', 'delete', 'recovery']:
        sem = directory / f'{phase}.semantic.json'
        sem.write_text(json.dumps({'profile': public['profile'], 'mode': public['mode'], 'route': {'typed_exit': 'manual_cleanup_required' if phase == 'preview' else 'cleaned'}}))
        command = ['bash', str(package / 'scripts/invoke.sh')]
        runenv = env
        if a.mode == 'rss':
            command = ['/usr/bin/time', '-l', '-o', str(directory / f'{phase}.rss'), *command]
        if a.mode == 'profile':
            command = [sys.executable, str(Path(__file__).with_name('profile_cleanup.py')), str(directory / f'{phase}.profile.json'), str(package), 'invoke-guru-cleanup-task-resources']
            runenv = {**env, 'PYTHONPATH': str(root / '.trellis/guru-team' if a.installed else skills)}
        begin = trace.stat().st_size if trace.exists() else 0
        start = time.perf_counter()
        r = subprocess.run([*command, '--root', str(root), '--input', str(inp), '--semantic-result', str(sem), *(['--confirmed-cleanup'] if phase != 'preview' else [])], capture_output=True, text=True, env=runenv)
        elapsed = time.perf_counter() - start
        end = trace.stat().st_size if trace.exists() else 0
        (directory / f'{phase}.stdout.json').write_text(r.stdout)
        (directory / f'{phase}.stderr.log').write_text(r.stderr)
        v = json.loads(r.stdout or r.stderr)
        v = v.get('result', v)
        assert r.returncode == 0 and v['exit_id'] == ('manual_cleanup_required' if phase == 'preview' else 'cleaned'), v
        row = {'phase': phase, 'seconds': elapsed, 'exit_id': v['exit_id'], 'trace_begin': begin, 'trace_end': end, **counts(trace, begin, end)}
        if a.mode == 'profile':
            row['profile'] = json.loads((directory / f'{phase}.profile.json').read_text())
        ops.append(row)
    assert all((not m.git(root, 'for-each-ref', '--format=%(refname)', f'refs/heads/snapshot-{n:03}') for n in range(a.count)))
    report = {'repeat': repeat, 'operations': ops, 'fixture': {'resources': a.count, 'selected_heads': 1, 'task_paths': 1, 'task_blob_oid': oid, 'task_blob_bytes': size, 'unselected_snapshot_retained': True}, 'network_seconds': 0}
    if a.mode == 'rss':
        report['wrapper_maxrss_bytes'] = {q.stem: max(map(int, re.findall('(\\d+)\\s+maximum resident set size', q.read_text()))) for q in directory.glob('*.rss') if q.name != 'git.rss'}
        report['git_maxrss_bytes'] = max(map(int, re.findall('(\\d+)\\s+maximum resident set size', (directory / 'git.rss').read_text())))
    if a.mode == 'volume':
        req = Counter()
        for line in trace.read_text().splitlines():
            ev = json.loads(line)
            if ev.get('event') == 'start' and 'show' in ev['argv']:
                for x in ev['argv'][ev['argv'].index('show') + 1:]:
                    if ':' in x and (not x.startswith('-')):
                        req[x] += 1
        for q in directory.glob('batch-*.requests'):
            req.update(q.read_text().splitlines())
        probes = subprocess.run([realgit, 'cat-file', '--batch-check'], cwd=root, input=''.join((x + '\n' for x in req)), capture_output=True, text=True, check=True).stdout.splitlines()
        success = Counter()
        sizes = {}
        for expression, line in zip(req, probes, strict=True):
            fields = line.split()
            if len(fields) == 3 and fields[1] == 'blob':
                success[fields[0]] += req[expression]
                sizes[fields[0]] = int(fields[2])
        report['volume'] = {'content_requests': sum(req.values()), 'successful_blob_requests': sum(success.values()), 'unique_blob_oids': len(success), 'returned_blob_bytes': sum((sizes[k] * v for k, v in success.items())), 'largest_blob': max(sizes.values(), default=0), 'requests': dict(req), 'by_oid': dict(success), 'scope': 'all preview/delete/recovery together; fixed archive reads included, metadata excluded; object-size probe outside timer/trace'}
    reports.append(report)
    (directory / 'summary.json').write_text(json.dumps(report, indent=2))
    print(json.dumps({'repeat': repeat, 'operations': ops}), flush=True)
    tmp.cleanup()
summary = {'source_head': subprocess.check_output([realgit, 'rev-parse', 'HEAD'], cwd=a.source, text=True).strip(), 'source_cleanup_sha256': __import__('hashlib').sha256((skills / 'packages/guru-cleanup-task-resources/runtime/invoke.py').read_bytes()).hexdigest(), 'mode': a.mode, 'installed': a.installed, 'count': a.count, 'samples': reports, 'median_seconds': {phase: statistics.median((next((o['seconds'] for o in r['operations'] if o['phase'] == phase)) for r in reports)) for phase in ['preview', 'delete', 'recovery']}, 'python': sys.version, 'interpreter': sys.executable, 'scope': 'actual public wrappers preview, confirmed deletion in disposable fixture, same-input result recovery; setup/install untimed; serial fresh equivalent repos, warm OS cache, no warmup, two repeats median; fixture semantics not native AI; RSS max individual process per wrapper and per git, not simultaneous total'}
(a.output / 'summary.json').write_text(json.dumps(summary, indent=2))
