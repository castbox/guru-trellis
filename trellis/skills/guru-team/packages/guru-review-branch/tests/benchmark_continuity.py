"""Source-private bounded-continuity benchmark using real public wrappers.

Provider and semantic judgments are fixtures, not native AI/live GitHub proof.
"""
import argparse, importlib.util, hashlib, json, os, re, statistics, subprocess, sys, time
from collections import Counter
from pathlib import Path
from unittest.mock import patch
p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, default=Path(__file__).resolve().parents[6])
p.add_argument('--api-common', type=Path)
p.add_argument('--profile-mode', choices=['legacy', 'plain'], default='legacy')
p.add_argument('--installation', type=Path)
p.add_argument('--paths', type=int, default=8)
p.add_argument('--kind', choices=['duplicates', 'unique'], default='duplicates')
p.add_argument('--pass', dest='measurement', choices=['timing', 'volume', 'rss', 'profile', 'hashes'], default='timing')
p.add_argument('--output', type=Path, required=True)
p.add_argument('--repeats', type=int, default=2)
a = p.parse_args()
a.source = a.source.resolve()
if a.api_common:
    os.environ['TRELLIS_DELIVERY_API_COMMON'] = str(a.api_common.resolve())
if a.paths < 0 or a.repeats < 1:
    p.error('paths must be nonnegative and repeats positive')
if a.measurement == 'rss' and sys.platform != 'darwin':
    p.error('RSS requires macOS BSD time')
a.output = a.output.resolve()
a.output.mkdir(parents=True)
skills = a.source / 'trellis/skills/guru-team'
sys.path.insert(0, str(skills))

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m
helpers = module('d1_helpers', skills / 'packages/guru-merge-task-delivery/tests/benchmark_git_objects.py')
fixture = module('d2_fixture', skills / 'packages/guru-check-task/tests/test_delivery_flow.py')
from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
from runtime.delivery_projection.gates import rework
realrun = subprocess.run
original_candidate = DeliveryProjection.candidate
assets = []

def run(command, *args, **kwargs):
    if command[:4] == ['git', 'commit', '-qm', 'feature']:
        repo = Path(kwargs['cwd'])
        (repo / 'assets').mkdir()
        for i in range(a.paths):
            data = hashlib.sha256(str(i % 64 if a.kind == 'duplicates' else i).encode()).digest() * 128
            path = f'assets/{i:05d}.bin'
            (repo / path).write_bytes(data)
            assets.append(path)
        (repo / 'assets/large.bin').write_bytes(bytes(range(256)) * 65536)
        assets.append('assets/large.bin')
        realrun(['git', 'add', 'assets'], cwd=repo, check=True, capture_output=True)
    return realrun(command, *args, **kwargs)

def candidate(self, paths, *args, **kwargs):
    return original_candidate(self, paths + assets if paths == ['app.txt'] else paths, *args, **kwargs)
if a.installation:
    os.environ['GURU_DELIVERY_TEST_INSTALLATION'] = str(a.installation.resolve())
case = fixture.DeliveryFlow()
case.delivery_profile = 'pull_request'
start = time.perf_counter()
try:
    with patch('subprocess.run', run), patch.object(DeliveryProjection, 'candidate', candidate):
        case.setUp()
    case.full_review(case.check())
    prior = case.head
    old_base = case.git('rev-parse', 'main').strip()
    case.git('add', case.task_ref)
    case.git('commit', '-qm', 'persist actual review facts')
    case.git('switch', 'main')
    (case.repo / 'base-only.txt').write_text('independent base change\n')
    case.git('add', 'base-only.txt')
    case.git('commit', '-qm', 'advance base')
    new_base = case.git('rev-parse', 'HEAD').strip()
    case.git('switch', 'feat/flow')
    case.git('merge', '--no-ff', '-m', 'reconcile actual base', 'main')
    case.head = case.git('rev-parse', 'HEAD').strip()
    rework(case.projection, case.key, 'full_review', 'implementation', authority_ref(case.repo / 'requirements.md', case.repo), ['check', 'full_review', 'readiness'])
    case.projection.begin_check(case.key, original_candidate(case.projection, ['app.txt', *assets], head_ref=case.head, base_ref=case.projection.content_base(case.key)))
    checked = case.check()
    package = skills / 'packages/guru-review-branch'
    common = module('d2_tree', package / 'runtime/common.py')
    public = {'profile': 'delivery_base_continuity', 'mode': 'workflow', 'task_ref': case.task_ref, 'delivery_key': case.key, 'check_result_id': checked['check_result_id'], 'task_head': case.head, 'branch_review_commit': prior, 'old_base_head': old_base, 'new_base_head': new_base, 'candidate_tree_sha256': common.tree_identity(case.repo, case.head), 'relevant_paths': ['base-only.txt'], 'resume_target': 'publication_review', 'review_intent': 'base_continuity'}
    auth_fixture = json.loads((package / 'examples/review-gate.json').read_text())
    auth = {k: auth_fixture[k] for k in ['candidate_classifications', 'semantic_review', 'verification_evidence', 'delivery_review']}
    auth['semantic_review']['qualified_findings'] = []
    auth['semantic_review']['ai_review_gate']['status'] = 'continuity_passed'
    inp = case.write('continuity-input.json', public)
    owner = case.write('continuity-owner.json', auth)
    record_args = ('--task', case.task_ref, '--skill-input', inp, '--semantic-review-file', owner, '--typed-exit', 'continuity_passed')
    check_args = ('--task', case.task_ref, '--delivery-key', json.dumps(case.key), '--expected-exit', 'continuity_passed')
    preparation = time.perf_counter() - start
    tree = realrun(['git', 'ls-tree', '-r', '-z', case.head], cwd=case.repo, check=True, capture_output=True).stdout
    objects = []
    for entry in tree.split(b'\x00'):
        if entry:
            meta, path = entry.split(b'\t', 1)
            mode, kind, oid = meta.split()
            if kind == b'blob':
                objects.append(oid.decode())
    probe = realrun(['git', 'cat-file', '--batch-check'], input=('\n'.join(objects) + '\n').encode(), cwd=case.repo, check=True, capture_output=True).stdout
    sizes = [int(line.split()[2]) for line in probe.splitlines()]
    case.bin = case.repo / '.trellis/.runtime/benchmark-bin'
    case.bin.mkdir()
    case.flow = case
    trace = helpers.install_observer(case, a)
    with patch.dict(os.environ, {'PATH': str(case.bin) + os.pathsep + os.environ['PATH']}):
        wrapper = case.wrapper
        ordinal = 0
        if a.measurement in ['rss', 'profile', 'hashes']:

            def wrapper(skill, name, *args, success=True):
                global ordinal
                runtime_package = getattr(case, 'installed_skills_root', skills) / 'packages/guru-review-branch'
                if a.measurement == 'rss':
                    cmd = ['/usr/bin/time', '-l', '-a', '-o', str(a.output / (name + '.rss')), 'bash', str(runtime_package / 'scripts' / name)]
                    env = None
                else:
                    cmdid = {'review-branch.sh': 'review-branch', 'check-review-gate.sh': 'check-review-gate', 'invoke.sh': 'invoke-guru-review-branch'}[name]
                    cmd = [sys.executable, str(Path(__file__).with_name('benchmark_continuity_profile.py')), str(a.output / f'{a.measurement}-{ordinal}-{name}.json'), str(runtime_package), cmdid]
                    env = {**os.environ, 'PYTHONPATH': str(runtime_package.parents[1]), 'GURU_CONTINUITY_PROFILE_MODE': 'hashes' if a.measurement == 'hashes' else a.profile_mode}
                ordinal += 1
                r = realrun([*cmd, '--root', str(case.repo), *map(str, args)], env=env, capture_output=True, text=True)
                v = json.loads(r.stdout or r.stderr)
                case.assertEqual(r.returncode == 0, success, v)
                return v.get('result', v)
        samples = []
        scalar = Counter()
        for i in range(a.repeats):
            offset = trace.stat().st_size if trace.exists() else 0
            operation = time.perf_counter()
            calls = []
            for name, args in [('review-branch.sh', record_args), ('check-review-gate.sh', check_args), ('invoke.sh', ('--input', inp))]:
                start = time.perf_counter()
                value = wrapper('guru-review-branch', name, *args)
                elapsed = time.perf_counter() - start
                calls.append({'entry': name, 'seconds': elapsed, 'result': value})
            elapsed = time.perf_counter() - operation
            case.assertEqual('continuity_passed', value['exit_id'])
            counts, current = helpers.trace_counts(trace, offset)
            scalar.update(current)
            sample = {'sample': i, 'seconds': elapsed, 'calls': calls, **counts}
            samples.append(sample)
            print(json.dumps(sample), flush=True)
    report = {'installation': str(a.installation) if a.installation else None, 'paths': a.paths, 'kind': a.kind, 'pass': a.measurement, 'preparation_seconds': preparation, 'candidate_tree_sha256': public['candidate_tree_sha256'], 'tree_blob_paths': len(objects), 'tree_unique_blobs': len(set(objects)), 'tree_path_bytes': sum(sizes), 'tree_unique_bytes': sum({oid: size for oid, size in zip(objects, sizes)}.values()), 'largest_blob': max(sizes), 'samples': samples, 'median_seconds': statistics.median((r['seconds'] for r in samples)), 'scope': 'original public recorder/checker/invoke after actual integration and current Check; provider and semantic fixture, not native AI or live GitHub; candidate tree digest prepared outside operation timer; analyses outside timer'}
    if a.measurement == 'volume':
        report['volume'] = helpers.volume_summary(a, scalar, case)
    if a.measurement == 'rss':
        report['runtime_maxrss_bytes'] = {name: [int(x) for x in re.findall('(\\d+)\\s+maximum resident set size', (a.output / (name + '.rss')).read_text())] for name in ['review-branch.sh', 'check-review-gate.sh', 'invoke.sh']}
        report['git_maxrss_bytes'] = max((int(x) for x in re.findall('(\\d+)\\s+maximum resident set size', (a.output / 'git.rss').read_text())))
    (a.output / 'summary.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'summary': str(a.output / 'summary.json'), 'median_seconds': report['median_seconds']}), flush=True)
finally:
    case.doCleanups()
