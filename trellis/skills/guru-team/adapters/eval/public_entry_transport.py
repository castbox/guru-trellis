"""Transparent argv/stdin transport for public-entry native observations.

This test-only carrier adds no Skill command, input, identity or judgment. It
preserves the complete original process result before displaying either stream.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys


def execute(repository: Path, receipts: Path, argv: list[str], stdin: str,
            *, provider_bin: Path | None = None) -> dict:
    if not argv:
        raise ValueError('Supply the original command argv after --.')
    environment = None if provider_bin is None else {
        **os.environ, 'PATH': str(provider_bin) + os.pathsep + os.environ.get('PATH', '')}
    try:
        process = subprocess.run(argv, cwd=repository, input=stdin, text=True,
                                 capture_output=True, check=False, env=environment)
        result = {'argv': argv, 'stdin': stdin, 'returncode': process.returncode,
                  'stdout': process.stdout, 'stderr': process.stderr}
    except OSError as error:
        result = {'argv': argv, 'stdin': stdin, 'returncode': 127,
                  'stdout': '', 'stderr': str(error) + '\n'}
    receipts.parent.mkdir(parents=True, exist_ok=True)
    with receipts.open('a', encoding='utf-8') as output:
        output.write(json.dumps(result, ensure_ascii=False) + '\n')
    return result


def delivered_stdout(result: dict, receipts: Path, loss_observation: Path | None) -> str:
    """Withhold one N3 producer response after the original receipt is saved."""
    if loss_observation is None or loss_observation.exists() or result['returncode']:
        return result['stdout']
    producers = ('guru-create-task', 'guru-create-delivery')
    producer = next((skill for skill in producers if any(
        part.endswith('/' + skill + '/scripts/invoke.sh') for part in result['argv'])), None)
    if producer is None and '--package-root' in result['argv']:
        index = result['argv'].index('--package-root') + 1
        if index < len(result['argv']):
            selected = Path(result['argv'][index]).name
            producer = selected if selected in producers else None
    if producer is None:
        return result['stdout']
    try:
        output = json.loads(result['stdout'])
    except ValueError:
        return result['stdout']
    if not isinstance(output, dict) or output.get('exit_id') != 'created':
        return result['stdout']
    loss_observation.parent.mkdir(parents=True, exist_ok=True)
    loss_observation.write_text(json.dumps({
        'receipt_index': len(receipts.read_text().splitlines()) - 1,
        'producer': producer, 'stdout_delivered': False,
    }) + '\n', encoding='utf-8')
    return ''


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', required=True)
    parser.add_argument('--receipts', required=True)
    parser.add_argument('--provider-bin')
    parser.add_argument('--loss-observation')
    parser.add_argument('argv', nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    command = args.argv[1:] if args.argv[:1] == ['--'] else args.argv
    result = execute(Path(args.repository), Path(args.receipts), command,
                     '' if sys.stdin.isatty() else sys.stdin.read(),
                     provider_bin=Path(args.provider_bin) if args.provider_bin else None)
    sys.stdout.write(delivered_stdout(result, Path(args.receipts),
        Path(args.loss_observation) if args.loss_observation else None))
    sys.stderr.write(result['stderr'])
    return result['returncode']


if __name__ == '__main__':
    raise SystemExit(main())
