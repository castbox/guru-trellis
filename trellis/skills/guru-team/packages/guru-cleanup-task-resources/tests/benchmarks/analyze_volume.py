# Source-private measurement utility; not installed runtime.
import json, sys
from pathlib import Path
out = Path(sys.argv[1])
reports = []
for summary in sorted(out.glob('*-volume/sample-*/summary.json')):
    row = json.loads(summary.read_text())
    v = row['volume']
    fixture = row['fixture']
    success = dict(v['by_oid'])
    sizes = {}
    events = [json.loads(x) for x in (summary.parent / 'git.trace.jsonl').read_text().splitlines()]
    exits = {e['sid']: e['code'] for e in events if e.get('event') == 'exit'}
    for e in events:
        if e.get('event') == 'start' and 'show' in e['argv']:
            assert exits[e['sid']] == 0
    omitted = 0
    for expr, count in v['requests'].items():
        if expr.startswith('refs/heads/snapshot-') and expr.endswith(':.trellis/tasks/demo/task.json'):
            omitted += count
    if omitted:
        success[fixture['task_blob_oid']] = success.get(fixture['task_blob_oid'], 0) + omitted
    resolved = {**v, 'successful_blob_requests': v['successful_blob_requests'] + omitted, 'unique_blob_oids': len(success), 'returned_blob_bytes': v['returned_blob_bytes'] + omitted * fixture['task_blob_bytes'], 'largest_blob': max(v['largest_blob'], fixture['task_blob_bytes'] if omitted else 0), 'by_oid': success, 'analysis_note': 'Scalar ref:path queries run before deletion and have trace2 successful exits. Post-delete batch-check cannot resolve deleted refs; exact selected immutable Task blob OID/bytes captured before operation supplies those requests. No timing/entry/input changed. Raw original post-delete probe retained.'}
    path = summary.parent / 'resolved-volume.json'
    path.write_text(json.dumps(resolved, indent=2))
    reports.append({'sample': str(summary.relative_to(out)), 'volume': resolved})
(out / 'volume-analysis.json').write_text(json.dumps(reports, indent=2))
