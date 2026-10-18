# Source-private measurement utility; not installed runtime.
import json, os, subprocess, sys
from pathlib import Path
source = sys.argv[1]
out = Path(sys.argv[2])
fork = sys.argv[3]
out.mkdir(parents=True, exist_ok=True)
rows = []
for installed in [False, True]:
    for count in [10, 100]:
        for mode in ['timing', 'profile', 'rss', 'volume']:
            name = f'{('installed' if installed else 'source')}-{count}-{mode}'
            target = out / name
            if (target / 'summary.json').is_file():
                rows.append(json.loads((target / 'summary.json').read_text()))
                continue
            cmd = [sys.executable, str(Path(__file__).with_name('benchmark_cleanup.py')), '--source', source, '--fork', fork, '--output', str(target), '--count', str(count), '--mode', mode, *(['--installed'] if installed else [])]
            with (out / (name + '.log')).open('w') as log:
                r = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT)
            if r.returncode:
                print(json.dumps({'failed': name, 'log': str(out / (name + '.log'))}), flush=True)
                sys.exit(r.returncode)
            report = json.loads((target / 'summary.json').read_text())
            rows.append(report)
            print(json.dumps({'completed': name, 'median_seconds': report['median_seconds']}), flush=True)
(out / 'aggregate.json').write_text(json.dumps(rows, indent=2))
