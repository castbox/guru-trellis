"""Source-private public-wrapper benchmark; provider and semantic review are fixtures."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import statistics
import subprocess
import sys
import time
import uuid
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parents[1]


def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=PACKAGE.parents[4])
    parser.add_argument('--installation', type=Path,
                        help='Existing clean installation used by the original fixture and preset reapply')
    parser.add_argument('--api-common', type=Path,
                        help='Reviewed upstream common directory (or TRELLIS_DELIVERY_API_COMMON)')
    parser.add_argument('--output', type=Path, required=True, help='New directory for this run')
    parser.add_argument('--entry', choices=['manual', 'history'], default='manual')
    parser.add_argument('--paths', type=int, default=1000, help='4096-byte assets, plus app and large blob')
    parser.add_argument('--kind', choices=['duplicates', 'unique'], default='duplicates')
    parser.add_argument('--deliveries', type=int, choices=[1, 2, 4], default=1)
    parser.add_argument('--repeats', type=int, default=2)
    parser.add_argument('--pass', dest='measurement', choices=['timing', 'rss', 'volume', 'profile', 'hash'], default='timing')
    args = parser.parse_args()
    if args.paths < 0 or args.repeats < 1:
        parser.error('--paths must be nonnegative and --repeats positive')
    if args.entry == 'manual' and args.deliveries != 1:
        parser.error('multiple Deliveries require --entry history')
    if args.measurement == 'rss' and sys.platform != 'darwin':
        parser.error('RSS uses BSD /usr/bin/time -l; run on macOS')
    args.source = args.source.resolve()
    args.output = args.output.resolve()
    if args.output.exists():
        parser.error('--output must be a new directory so raw observations cannot mix')
    return args


def setup(args):
    skills = args.source / 'trellis/skills/guru-team'
    sys.path.insert(0, str(skills))
    from runtime.delivery_projection.adapter import DeliveryProjection
    spec = importlib.util.spec_from_file_location('benchmark_manual_fixture',
        skills / 'packages/guru-merge-task-delivery/tests/test_manual_recovery.py')
    fixture = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fixture)
    assets, unique = [], {}
    realrun, original = subprocess.run, DeliveryProjection.candidate

    def run(command, *positional, **kwargs):
        if command[:4] == ['git', 'commit', '-qm', 'feature']:
            repo = Path(kwargs['cwd'])
            (repo / 'assets').mkdir()
            for index in range(args.paths):
                seed = index % 64 if args.kind == 'duplicates' else index
                data = hashlib.sha256(str(seed).encode()).digest() * 128
                locator = f'assets/{index:05d}.bin'
                (repo / locator).write_bytes(data)
                assets.append(locator)
                unique[hashlib.sha256(data).hexdigest()] = len(data)
            data = bytes(range(256)) * 65536
            (repo / 'assets/large.bin').write_bytes(data)
            assets.append('assets/large.bin')
            unique[hashlib.sha256(data).hexdigest()] = len(data)
            realrun(['git', 'add', 'assets'], cwd=repo, check=True, capture_output=True)
        return realrun(command, *positional, **kwargs)

    def candidate(projection, paths, *positional, **kwargs):
        return original(projection, paths + assets if paths == ['app.txt'] else paths,
                        *positional, **kwargs)

    case = fixture.ManualRecoveryTests()
    try:
        with patch('subprocess.run', run), patch.object(DeliveryProjection, 'candidate', candidate):
            case.setUp()
    except BaseException:
        case.doCleanups()
        raise
    return case, assets, unique, skills


def trace_counts(path, offset):
    """No full trace/string/argv list retained; this runs outside the timer."""
    counts = Counter()
    scalar_content = Counter()
    with path.open('rb') as stream:
        stream.seek(offset)
        for line in stream:
            event = json.loads(line)
            if event.get('event') != 'start':
                continue
            argv = event['argv']
            counts['git'] += 1
            for name in ('cat-file', 'show', 'ls-tree'):
                if name in argv:
                    counts[name] += 1
            if 'cat-file' in argv:
                tail = argv[argv.index('cat-file') + 1:]
                if len(tail) == 2 and tail[0] in ('blob', '-p'):
                    scalar_content[tail[1]] += 1
    return dict(counts), scalar_content


def install_observer(case, args):
    realgit = shutil.which('git')
    trace = args.output / 'git.trace.jsonl'
    command = shlex.quote(realgit) + ' "$@"'
    if args.measurement == 'rss':
        command = '/usr/bin/time -l -a -o ' + shlex.quote(str(args.output / 'git.rss')) + ' ' + command
    if args.measurement == 'volume':
        command = (shlex.quote(sys.executable) + ' ' +
                   shlex.quote(str(Path(__file__).with_name('benchmark_observer.py'))) + ' ' +
                   shlex.quote(str(args.output)) + ' ' + shlex.quote(realgit) + ' "$@"')
    (case.bin / 'git').write_text('#!/bin/sh\nexport GIT_TRACE2_EVENT=' +
        shlex.quote(str(trace)) + '\nexec ' + command + '\n')
    (case.bin / 'git').chmod(0o755)
    return trace


def profile_runtime_root(package):
    """Locate the two supported canonical/installed shared-runtime layouts."""
    for root in (package.parents[1], package.parents[2]):
        if (root / 'runtime/command.py').is_file():
            return root
    raise ValueError('No canonical or installed shared runtime for ' + str(package))


def instrument_wrapper(case, args, skills):
    if args.measurement not in ('rss', 'profile', 'hash'):
        return
    ordinal = 0

    def wrapper(skill, name, *parameters, success=True):
        nonlocal ordinal
        package = getattr(case.flow, 'installed_skills_root', skills) / 'packages' / skill
        if args.measurement == 'rss':
            command = ['/usr/bin/time', '-l', '-a', '-o', str(args.output / 'runtime.rss'),
                       'bash', str(package / 'scripts' / name)]
            env = None
        else:
            command_id = 'invoke-guru-merge-task-delivery' if name == 'invoke.sh' else 'discover-task-deliveries'
            command = [sys.executable, str(Path(__file__).with_name('benchmark_profile.py')),
                       str(args.output / f'profile-{ordinal}.json'), str(package), command_id]
            env = {**os.environ, 'PYTHONPATH': str(profile_runtime_root(package)), 'GURU_BENCH_PASS': args.measurement}
        observation = ordinal
        ordinal += 1
        result = subprocess.run([*command, '--root', str(case.repo), *map(str, parameters)],
                                env=env, capture_output=True, text=True)
        if args.measurement in ('profile', 'hash'):
            prefix = args.output / f'profile-{observation}'
            prefix.with_suffix('.stdout').write_text(result.stdout)
            prefix.with_suffix('.stderr').write_text(result.stderr)
            prefix.with_suffix('.process.json').write_text(json.dumps({
                'exit_code': result.returncode, 'pass': args.measurement,
                'pythonpath': env['PYTHONPATH'],
                'stdout': prefix.with_suffix('.stdout').name,
                'stderr': prefix.with_suffix('.stderr').name,
            }) + '\n')
        try:
            value = json.loads(result.stdout or result.stderr)
        except json.JSONDecodeError as exc:
            if args.measurement in ('profile', 'hash'):
                raise RuntimeError(f'Observed wrapper returned non-JSON, exit={result.returncode}; '
                                   f'see {prefix.with_suffix(".process.json")} and raw stdout/stderr') from exc
            raise
        case.assertEqual(result.returncode == 0, success, value)
        return value.get('result', value)
    case.flow.wrapper = wrapper


def candidate_identity(case, output):
    """Business-path identity only; source/install fixture trees may differ."""
    projection = case.projection
    record = projection.read_record()
    values = []
    for row in record['deliveries']:
        publication = row.get('publication_result')
        if publication is None:
            continue
        candidate = publication['candidate']
        paths = candidate['paths']
        tree = subprocess.run(['git', 'ls-tree', '-rz', '--full-tree', candidate['head_ref'], '--', *paths],
                              cwd=case.repo, capture_output=True, check=True).stdout
        values.append({'head': candidate['head_ref'], 'content_ref': candidate['content_ref'],
                       'paths': paths, 'ls_tree': tree.decode('utf-8').split('\0')[:-1]})
    (output / 'candidate-identities.json').write_text(json.dumps(values, indent=2) + '\n')
    return values


def main():
    args = arguments()
    args.output.mkdir(parents=True)
    environment = {'GIT_AUTHOR_DATE': '2026-10-15T00:00:00+00:00',
                   'GIT_COMMITTER_DATE': '2026-10-15T00:00:00+00:00'}
    if args.api_common:
        environment['TRELLIS_DELIVERY_API_COMMON'] = str(args.api_common.resolve())
    if args.installation:
        environment['GURU_DELIVERY_TEST_INSTALLATION'] = str(args.installation.resolve())
    ordinal = iter(range(1000000))
    def fixture_uuid():
        return uuid.uuid5(uuid.NAMESPACE_URL, 'guru-589-benchmark-v1/' + str(next(ordinal)))
    with patch.dict(os.environ, environment), patch('uuid.uuid4', fixture_uuid):
        start = time.perf_counter()
        case, assets, unique, skills = setup(args)
        try:
            if args.entry == 'history':
                from benchmark_history import prepare_history
                prepare_history(case, assets, args.deliveries)
            identities = candidate_identity(case, args.output)
            preparation = time.perf_counter() - start
            trace = install_observer(case, args)
            instrument_wrapper(case, args, skills)
            samples, scalar = [], Counter()
            for index in range(args.repeats):
                os.environ['GURU_BENCH_SAMPLE'] = str(index)
                offset = trace.stat().st_size if trace.exists() else 0
                start = time.perf_counter()
                if args.entry == 'manual':
                    result = case.invoke()
                    case.assertEqual('delivered', result['exit_id'])
                else:
                    query = {'schema_version': '2.0', 'task_identity': 'flow-task',
                             'repo_ref': 'example/repo', 'base_ref': 'main', 'task_ref': case.flow.task_ref}
                    result = case.flow.wrapper('guru-merge-task-delivery', 'discover-task-deliveries.sh',
                        '--input', case.flow.write('benchmark-history.json', query))
                    case.assertEqual(args.deliveries, len(result['deliveries']))
                elapsed = time.perf_counter() - start
                counts, current = trace_counts(trace, offset)
                scalar.update(current)
                sample = {'sample': index, 'seconds': elapsed, **counts,
                          'operation_state': ('first_record' if index == 0 else 'recorded_recovery') if args.entry == 'manual' else 'recorded_history_query',
                          'exit': result.get('exit_id', 'historical_query_complete')}
                samples.append(sample)
                print(json.dumps(sample), flush=True)
            report = {'source': str(args.source), 'installation': str(args.installation) if args.installation else None,
                      'entry': args.entry, 'pass': args.measurement, 'paths': args.paths,
                      'kind': args.kind, 'deliveries': args.deliveries, 'repeats': args.repeats,
                      'preparation_seconds': preparation, 'samples': samples,
                      'median_seconds': statistics.median(row['seconds'] for row in samples) if args.entry == 'history' or args.repeats == 1 else None,
                      'medians_by_state': {state: statistics.median(row['seconds'] for row in samples if row['operation_state'] == state) for state in {row['operation_state'] for row in samples}},
                      'candidate_identities': identities,
                      'fixture_dates': environment['GIT_AUTHOR_DATE'],
                      'fixture_uuid_seed': 'guru-589-benchmark-v1',
                      'candidate_paths': len(case.publication['candidate']['paths']),
                      'unique_asset_blobs': len(unique), 'asset_unique_bytes': sum(unique.values()),
                      'asset_path_bytes': args.paths * 4096 + 16777216, 'largest_asset_blob': 16777216,
                      'provider': 'local GitHub-response fixture; network waiting zero; no live GitHub or native AI semantic proof',
                      'timing_scope': 'original public wrapper including validators/store; preparation and streaming trace analysis excluded; no cold-cache claim'}
            if args.measurement == 'volume':
                from benchmark_observer import summarize
                report['volume'] = summarize(args.output, shutil.which('git', path=os.defpath))
            if args.measurement == 'rss':
                def rss(name):
                    return [int(value) for value in re.findall(r'(\d+)\s+maximum resident set size',
                            (args.output / name).read_text())]
                report['runtime_maxrss_bytes'] = rss('runtime.rss')
                git_rss = rss('git.rss')
                report['git_maxrss_bytes'] = max(git_rss)
                report['git_profiled_processes'] = len(git_rss)
                report['rss_scope'] = 'BSD time wrapper including descendants (maximum individual-process RSS, not pure Python) and each Git process; maxima are not simultaneous process-group totals; independent profiling pass'
            (args.output / 'summary.json').write_text(json.dumps(report, indent=2) + '\n')
            print(json.dumps({'summary': str(args.output / 'summary.json'),
                              'median_seconds': report['median_seconds']}), flush=True)
        finally:
            case.doCleanups()


if __name__ == '__main__':
    main()
