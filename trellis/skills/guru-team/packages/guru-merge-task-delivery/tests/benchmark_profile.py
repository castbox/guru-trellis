"""Independent dispatcher profile/hash pass, never plain wrapper timing evidence."""
import atexit
from collections import Counter
import cProfile
import hashlib
import io
import json
import os
import pstats
import runpy
import subprocess
import sys
import time
from pathlib import Path


def selected_function(file, name):
    """Exact module and qualified function, avoiding unrelated content_ref names."""
    module = Path(file).name
    return ((module == 'manual_recovery.py' and name == 'commit_candidate')
            or (module == 'history.py' and name == 'HistoryContext.candidate')
            or (module == 'candidate_objects.py' and name == 'CandidateObjects.snapshot')
            or (module == 'delivery_store.py' and name in {
                'candidate_content_ref', '_candidate_content_ref', 'GitCandidateContent.content_ref',
                '_ContentObservation.file_hash', '_ContentObservation.content_ref'})
            or (module == 'git_objects.py' and name == 'hash_blob'))


def site(frame):
    location = f'{frame.f_code.co_filename}:{frame.f_lineno}:{frame.f_code.co_qualname}'
    path = frame.f_locals.get('path')
    if isinstance(path, Path):
        category = 'manual_snapshot' if any(part.startswith('guru-manual-delivery-snapshot-') for part in path.parts) else 'other_filesystem'
        location += '[' + category + ']'
    return location


def observe_hashes():
    """Count bytes fed to the real hashlib and actual filesystem read methods."""
    counts = Counter()
    original_sha, original_open = hashlib.sha256, io.open

    class Digest:
        def __init__(self, value, location, initial):
            self.value, self.location = value, location
            counts[('sha256_instances', location)] += 1
            counts[('sha256_input_bytes', location)] += len(initial)

        def update(self, value):
            counts[('sha256_updates', self.location)] += 1
            counts[('sha256_input_bytes', self.location)] += len(value)
            return self.value.update(value)

        def copy(self):
            # Copy is a real new state, without replaying input bytes.
            return Digest(self.value.copy(), self.location, b'')

        def __getattr__(self, name):
            return getattr(self.value, name)

    def sha256(value=b'', **kwargs):
        return Digest(original_sha(value, **kwargs), site(sys._getframe(1)), value)

    class Reader:
        def __init__(self, stream, location):
            self.stream, self.location = stream, location
            counts[('filesystem_read_opens', location)] += 1

        def read(self, *args):
            value = self.stream.read(*args)
            counts[('filesystem_read_calls', self.location)] += 1
            counts[('filesystem_read_bytes', self.location)] += len(value)
            return value

        def __enter__(self):
            self.stream.__enter__()
            return self

        def __exit__(self, *args):
            return self.stream.__exit__(*args)

        def __getattr__(self, name):
            return getattr(self.stream, name)

    def opened(file, mode='r', *args, **kwargs):
        stream = original_open(file, mode, *args, **kwargs)
        # Path.open calls io.open; attribute only the actual upstream caller.
        frame = sys._getframe(1)
        if frame.f_code is Path.open.__code__:
            frame = frame.f_back
        if (mode == 'rb' and Path(frame.f_code.co_filename).name == 'delivery_store.py'
                and frame.f_code.co_name in ('_candidate_content_ref', 'file_hash')):
            return Reader(stream, site(frame))
        return stream

    hashlib.sha256, io.open = sha256, opened
    return counts


def main():
    output = Path(sys.argv[1])
    sys.argv = ['runtime.command', *sys.argv[2:]]
    realrun = subprocess.run
    provider = 0.0

    def run(args, *a, **kw):
        nonlocal provider
        start = time.perf_counter()
        try:
            return realrun(args, *a, **kw)
        finally:
            if args and args[0] == 'gh':
                provider += time.perf_counter() - start
    subprocess.run = run
    is_hash = os.environ.get('GURU_BENCH_PASS') == 'hash'
    hashes = observe_hashes() if is_hash else None
    profile = cProfile.Profile()
    start = time.perf_counter()
    if not is_hash:
        profile.enable()

    def finish():
        elapsed = time.perf_counter() - start
        profile.disable()
        rows = []
        if not is_hash:
            # pstats names omit class qualification. Recover it from the loaded
            # code objects, not a broad content_ref function-name match.
            qualified = {}
            import gc
            import types
            for value in gc.get_objects():
                if isinstance(value, types.FunctionType):
                    code = value.__code__
                    qualified[(code.co_filename, code.co_firstlineno, code.co_name)] = code.co_qualname
            for (file, line, name), (cc, nc, tt, ct, callers) in pstats.Stats(profile).stats.items():
                name = qualified.get((file, line, name), name)
                if selected_function(file, name):
                    rows.append({'file': file, 'line': line, 'function': name, 'calls': nc,
                                 'self_seconds': tt, 'cumulative_seconds': ct})
        output.write_text(json.dumps({
            'runtime_dispatch_seconds': elapsed, 'fixture_provider_seconds': provider,
            'functions': rows, 'hash_observations': [
                {'metric': metric, 'site': location, 'value': value}
                for (metric, location), value in sorted(hashes.items())] if is_hash else [],
            'scope': 'independent hash/profile pass; real SHA256 implementation delegated unchanged; filesystem read bytes only delivery_store binary Path.open readers; hash input bytes include aggregate serialization at separately named sites; nested cumulative times are individual rows, never summed; wrapper timing independent',
        }) + '\n')
    atexit.register(finish)
    runpy.run_module('runtime.command', run_name='__main__')


if __name__ == '__main__':
    main()
