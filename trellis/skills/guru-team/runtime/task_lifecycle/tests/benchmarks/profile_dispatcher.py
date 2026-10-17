"""Independent cProfile pass; actual official Task writer command is unchanged."""
import atexit, cProfile, json, os, pstats, runpy, subprocess, sys, time
from pathlib import Path
output = Path(sys.argv[1])
sys.argv = ['runtime.command', *sys.argv[2:]]
realrun = subprocess.run
writer = []
trace = Path(os.environ['GURU_D3_TRACE'])

def run(command, *args, **kwargs):
    official = isinstance(command, (list, tuple)) and len(command) > 2 and str(command[1]).endswith('/.trellis/scripts/task.py') and (command[2] == 'create')
    offset = trace.stat().st_size if official and trace.exists() else 0
    start = time.perf_counter()
    try:
        return realrun(command, *args, **kwargs)
    finally:
        if official:
            writer.append({'seconds': time.perf_counter() - start, 'trace_start': offset, 'trace_end': trace.stat().st_size if trace.exists() else 0, 'interpreter': str(command[0]), 'writer': str(command[1])})
subprocess.run = run
profile = cProfile.Profile()
start = time.perf_counter()
profile.enable()

def finish():
    profile.disable()
    rows = []
    names = {'prepare_creation_inputs', '_create_official_task', 'establish_created_control_state', 'discover_branch_candidates', 'resolve_establishment', 'commit_path_bytes', 'resolve_task_id', 'task_identity_reservation', 'discover_worktree_facts', 'capture_checkout_state', 'establish_branch_binding', 'validate_candidate'}
    for (file, line, name), (_, calls, self_time, cumulative, _) in pstats.Stats(profile).stats.items():
        if name in names:
            rows.append({'file': file, 'function': name, 'calls': calls, 'self_seconds': self_time, 'cumulative_seconds': cumulative})
    output.write_text(json.dumps({'dispatcher_seconds': time.perf_counter() - start, 'interpreter': sys.executable, 'python_version': sys.version, 'functions': rows, 'official_writer_subprocesses': writer, 'scope': 'independent pure cProfile; real dispatcher and unchanged official writer subprocess; cumulative stages can overlap, do not sum nested rows or subtract across passes'}, indent=2) + '\n')
atexit.register(finish)
runpy.run_module('runtime.command', run_name='__main__')
