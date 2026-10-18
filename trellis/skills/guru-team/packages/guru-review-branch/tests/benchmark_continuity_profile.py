"""Separate dispatcher profiling and hash observation; never wrapper timing proof."""
import atexit
from collections import Counter
import cProfile
import hashlib
import json
import os
from pathlib import Path
import pstats
import runpy
import sys
import time

output = Path(sys.argv[1])
sys.argv = ['runtime.command', *sys.argv[2:]]
mode = os.environ.get('GURU_CONTINUITY_PROFILE_MODE', 'legacy')
original = hashlib.sha256
initial_hashes = Counter()
completed_hashes = Counter()


class ObservedHash:
    def __init__(self, value, origin, initial_bytes):
        self.value = value
        self.origin = origin
        self.bytes = initial_bytes
        self.updates = 0
        self.observed = False

    def update(self, data):
        self.bytes += len(data)
        self.updates += 1
        return self.value.update(data)

    def observe(self):
        if not self.observed:
            completed_hashes[(*self.origin, self.bytes, self.updates,
                              self.value.hexdigest())] += 1
            self.observed = True

    def digest(self):
        self.observe()
        return self.value.digest()

    def hexdigest(self):
        self.observe()
        return self.value.hexdigest()

    def __getattr__(self, name):
        return getattr(self.value, name)


def sha256(data=b'', *args, **kwargs):
    value = original(data, *args, **kwargs)
    frame = sys._getframe(1)
    if mode == 'legacy':
        # Exact before observer: initial constructor payload only. Streaming
        # update bytes must be measured by the independent hashes pass.
        if frame.f_code.co_name == 'tree_identity':
            initial_hashes[(frame.f_code.co_filename, frame.f_lineno,
                            len(data), value.hexdigest())] += 1
        return value
    origin = (frame.f_code.co_filename, frame.f_lineno, frame.f_code.co_name)
    while frame is not None:
        if frame.f_code.co_name == 'tree_identity':
            return ObservedHash(value, origin, len(data))
        frame = frame.f_back
    return value


if mode in ('legacy', 'hashes'):
    hashlib.sha256 = sha256
profile = cProfile.Profile()
start = time.perf_counter()
if mode != 'hashes':
    profile.enable()


def finish():
    profile.disable()
    rows = []
    if mode != 'hashes':
        for (file, line, name), (_, calls, self_time, cumulative, _) in pstats.Stats(profile).stats.items():
            if name in ('tree_identity', 'validate_gate') or 'sha256' in name:
                rows.append({'file': file, 'function': name, 'calls': calls,
                             'self_seconds': self_time, 'cumulative_seconds': cumulative})
    groups = {}
    for (file, line, size, digest), count in initial_hashes.items():
        group = groups.setdefault((file, line), {'file': file, 'line': line,
            'constructor_calls': 0, 'initial_bytes': 0, 'digests': set()})
        group['constructor_calls'] += count
        group['initial_bytes'] += size * count
        group['digests'].add(digest)
    for group in groups.values():
        group['unique_initial_digests'] = len(group.pop('digests'))
    observed = {}
    for (file, line, function, size, updates, digest), count in completed_hashes.items():
        group = observed.setdefault((file, line, function), {'file': file, 'line': line,
            'function': function, 'completed_hash_objects': 0, 'hashed_bytes': 0,
            'update_calls': 0, 'digests': set()})
        group['completed_hash_objects'] += count
        group['hashed_bytes'] += size * count
        group['update_calls'] += updates * count
        group['digests'].add(digest)
    for group in observed.values():
        group['unique_final_digests'] = len(group.pop('digests'))
    output.write_text(json.dumps({'mode': mode,
        'dispatcher_seconds': time.perf_counter() - start, 'functions': rows,
        'legacy_initial_hashes': list(groups.values()),
        'completed_hashes_by_origin': list(observed.values()),
        'scope': 'independent pass; cumulative rows overlap; hashes mode counts constructor/update/finalization under tree_identity including helper calls; map origins to actual blob/final-tree code; legacy counts only constructor payload and cannot measure streaming update bytes; fixture semantic/provider, no native proof'}, indent=2) + '\n')


atexit.register(finish)
runpy.run_module('runtime.command', run_name='__main__')
