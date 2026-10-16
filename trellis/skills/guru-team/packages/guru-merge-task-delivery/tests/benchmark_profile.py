"""Independent dispatcher cProfile pass, excluded from wrapper timing evidence."""
import atexit, cProfile, json, pstats, runpy, subprocess, sys, time
from pathlib import Path
output = Path(sys.argv[1])
sys.argv = ['runtime.command', *sys.argv[2:]]
realrun = subprocess.run
provider = 0.0

def run(args, *a, **kw):
    global provider
    start = time.perf_counter()
    try:
        return realrun(args, *a, **kw)
    finally:
        if args and args[0] == 'gh':
            provider += time.perf_counter() - start
subprocess.run = run
profile = cProfile.Profile()
start = time.perf_counter()
profile.enable()

def finish():
    elapsed = time.perf_counter() - start
    profile.disable()
    stats = pstats.Stats(profile)
    rows = []
    for (file, line, name), (cc, nc, tt, ct, callers) in stats.stats.items():
        if name in {'commit_candidate', 'candidate_content_ref'} or (name == 'candidate' and file.endswith('/history.py')):
            rows.append({'file': file, 'function': name, 'calls': nc, 'self_seconds': tt, 'cumulative_seconds': ct})
    output.write_text(json.dumps({'runtime_dispatch_seconds': elapsed, 'fixture_provider_seconds': provider, 'functions': rows, 'scope': 'separate profiling pass; original public dispatcher/core validation; public-wrapper wall time measured independently'}) + '\n')
atexit.register(finish)
runpy.run_module('runtime.command', run_name='__main__')
