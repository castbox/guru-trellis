"""Independent Git-volume observer; never installed in a plain timing pass."""
from collections import Counter
import json
import os
from pathlib import Path
import stat
import subprocess
import sys


def protocol(argv, lines):
    """Separate content requests from metadata/control without reading responses."""
    tail = argv[argv.index('cat-file') + 1:] if 'cat-file' in argv else []
    body, metadata, control = Counter(), Counter(), Counter()
    if any(arg.startswith('--batch-command') for arg in tail):
        for line in lines:
            verb, _, oid = line.strip().partition(' ')
            if verb == 'contents':
                body[oid] += 1
            elif verb == 'info':
                metadata[oid] += 1
            elif verb:
                control[verb] += 1
    elif any(arg.startswith('--batch-check') for arg in tail):
        metadata.update(line.strip() for line in lines if line.strip())
    elif any(arg.startswith('--batch') for arg in tail):
        body.update(line.strip() for line in lines if line.strip())
    elif len(tail) == 2:
        if tail[0] in ('blob', '-p'):
            body[tail[1]] += 1
        elif tail[0] in ('-e', '-s', '-t'):
            metadata[tail[1]] += 1
    return body, metadata, control


def git_location(argv, cwd):
    """Preserve Git's actual global options for the later size probe."""
    root, prefix, index = Path(cwd), [], 0
    while index < len(argv):
        arg = argv[index]
        if arg in ('-C', '-c', '--git-dir', '--work-tree', '--namespace'):
            value = argv[index + 1]
            prefix.extend([arg, value])
            if arg == '-C' and value:
                root = (root / value).resolve()
            index += 2
        elif arg.startswith(('--git-dir=', '--work-tree=', '--namespace=')) or arg == '--bare':
            prefix.append(arg)
            index += 1
        else:
            break
    return str(root), prefix


def observe():
    output, realgit, *argv = sys.argv[1:]
    output = Path(output)
    identity = f'{os.environ.get("GURU_BENCH_SAMPLE", "unknown")}-{os.getpid()}'
    request = output / f'git-{identity}.requests'
    captured = False
    if 'cat-file' in argv and any(arg.startswith('--batch') for arg in argv):
        if stat.S_ISREG(os.fstat(0).st_mode):
            offset = os.lseek(0, 0, os.SEEK_CUR)
            with request.open('wb') as stream:
                while data := os.pread(0, 1048576, offset):
                    stream.write(data)
                    offset += len(data)
            captured = True
    cwd = os.getcwd()
    root, prefix = git_location(argv, cwd)
    code = subprocess.run([realgit, *argv]).returncode
    (output / f'git-{identity}.json').write_text(json.dumps({
        'sample': os.environ.get('GURU_BENCH_SAMPLE'), 'argv': argv, 'cwd': cwd,
        'actual_root': root, 'probe_prefix': prefix, 'exit_code': code,
        'requests': request.name if captured else None,
        'uncaptured_batch_stdin': 'cat-file' in argv and any(a.startswith('--batch') for a in argv) and not captured,
    }) + '\n')
    return code


def summarize(output, realgit):
    body, metadata, control = Counter(), Counter(), Counter()
    roots, commands, unavailable = {}, [], []
    scalar = batch = total_bytes = 0
    unique_blobs = {}
    for path in sorted(output.glob('git-*.json')):
        command = json.loads(path.read_text())
        lines = ((output / command['requests']).read_text().splitlines()
                 if command['requests'] else [])
        b, m, c = protocol(command['argv'], lines)
        body.update(b)
        metadata.update(m)
        control.update(c)
        if command['requests']:
            batch += sum(b.values())
        else:
            scalar += sum(b.values())
        key = (command['cwd'], tuple(command['probe_prefix']))
        roots.setdefault(key, Counter()).update(b)
        commands.append(command)
    for ordinal, ((cwd, prefix), requests) in enumerate(roots.items()):
        if not requests:
            continue
        request_path, response_path = output / f'size-probe-{ordinal}.input', output / f'size-probe-{ordinal}.output'
        request_path.write_text(''.join(oid + '\n' for oid in requests))
        with request_path.open('rb') as source, response_path.open('wb') as target:
            subprocess.run([realgit, *prefix, 'cat-file', '--batch-check'], cwd=cwd,
                           stdin=source, stdout=target, stderr=subprocess.PIPE, check=True)
        for requested, line in zip(requests, response_path.read_text().splitlines(), strict=True):
            fields = line.split()
            if len(fields) == 2 and fields[1] == 'missing':
                unavailable.append({'cwd': cwd, 'prefix': list(prefix), 'object': requested,
                                    'requests': requests[requested]})
            elif len(fields) == 3:
                oid, kind, size = fields
                if kind == 'blob':
                    unique_blobs[oid] = int(size)
                    total_bytes += int(size) * requests[requested]
            else:
                raise ValueError('Invalid size probe response: ' + line)
    return {'scalar_content_requests': scalar, 'batch_content_requests': batch,
            'requested_objects': sum(body.values()), 'unique_requested_oids': len(body),
            'metadata_requests': sum(metadata.values()), 'control_requests': dict(control),
            'successful_content_bytes': total_bytes, 'unique_content_bytes': sum(unique_blobs.values()),
            'largest_requested_blob': max(unique_blobs.values(), default=0), 'requests_by_oid': dict(body),
            'commands': commands, 'unavailable_at_post_probe': unavailable,
            'failed_commands': sum(row['exit_code'] != 0 for row in commands),
            'uncaptured_batch_commands': sum(row['uncaptured_batch_stdin'] for row in commands),
            'scope': 'independent volume pass; requested blob bytes resolved at each actual Git root, not physical IO or successful-response parsing; local-complete numerical fixtures only; unavailable/uncaptured entries invalidate completeness'}


if __name__ == '__main__':
    sys.exit(observe())
