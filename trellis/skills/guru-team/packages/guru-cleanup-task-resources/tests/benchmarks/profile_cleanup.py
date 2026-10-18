# Source-private measurement utility; not installed runtime.
import atexit, cProfile, json, pstats, runpy, sys, time
from pathlib import Path
out = Path(sys.argv[1])
sys.argv = ['runtime.command', *sys.argv[2:]]
p = cProfile.Profile()
start = time.perf_counter()
p.enable()

def finish():
    p.disable()
    rows = [{'file': f, 'function': n, 'calls': v[1], 'self_seconds': v[2], 'cumulative_seconds': v[3]} for (f, l, n), v in pstats.Stats(p).stats.items() if n in {'manual_targets_current', 'inspect_resource', 'discover_candidates', 'require_missing_terminal'}]
    out.write_text(json.dumps({'dispatcher_seconds': time.perf_counter() - start, 'functions': rows}, indent=2))
atexit.register(finish)
runpy.run_module('runtime.command', run_name='__main__')
