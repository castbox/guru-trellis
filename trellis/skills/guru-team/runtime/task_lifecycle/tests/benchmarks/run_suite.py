"""Run the fixed source16 + representative installed6 passes serially."""
import argparse
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source', type=Path, required=True)
parser.add_argument('--fork', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--pool', type=Path, required=True)
args = parser.parse_args()
source = args.source.resolve()
fork = args.fork.resolve()
output = args.output.resolve()
pool = args.pool.resolve()
output.mkdir(parents=True)
harness = Path(__file__).with_name('benchmark_lifecycle.py')
resolver = source / '.trellis/guru-team/runtime/resolve-python.sh'

for installed, modes, workloads in (
    (False, ('timing', 'profile', 'rss', 'volume'),
     (('create', 10), ('create', 100), ('binding', 10), ('binding', 100))),
    (True, ('timing', 'rss', 'volume'), (('create', 100), ('binding', 100))),
):
    for mode in modes:
        for entry, count in workloads:
            name = f"{'installed-' if installed else ''}{entry}{count}-{mode}"
            command = [
                str(resolver), str(source), str(source / '.trellis/guru-team/runtime'),
                str(harness), '--source', str(source), '--fork', str(fork),
                '--entry', entry, '--count', str(count), '--pass', mode,
                '--output', str(output / name), '--pool', str(pool / f'pool-{count}'),
                '--repeats', '2',
            ]
            if installed:
                command.append('--installed')
            print(f'Starting {name}', flush=True)
            subprocess.run(command, cwd=source, check=True)
            print(f'Completed {name}', flush=True)
