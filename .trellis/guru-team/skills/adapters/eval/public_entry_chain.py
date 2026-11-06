"""Independent pre-Task native cases through the installed Codex entry.

The template is a real matching installation supplied by the installation
owner. Clones establish environment and business authority only. No Task,
Delivery, current owner judgment, candidate or expected exit is staged.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys

from adapters.eval import stage_result_chain as chain
from adapters.eval.fixture_io import run_git
from adapters.eval.phase2_authoring import write_json

CASES = ('N1', 'N2', 'N3')
SOURCE = '''# Inclusive selection requirement

Implement select(values, lower, upper) so both bounds are inclusive. Preserve
input order and duplicate values. Negative and singleton ranges are legal.
Use the existing pure function and its caller. Add focused behavior tests.
The source Issue is the complete scope; no deployment or external adoption is
required. Complete its ordinary Task lifecycle through Finish. Keep any real
finding, stale result or missing evidence truthful.
'''
FILES = {
    'docs/source.md': SOURCE,
    'interval.py': 'def contains(value, lower, upper):\n    raise NotImplementedError("not implemented")\n',
    'range_filter.py': 'from interval import contains\ndef select(values, lower, upper):\n    return [value for value in values if contains(value, lower, upper)]\n',
    'docs/architecture/README.md': '# Architecture\nIdentity: interval-architecture-v1. Active. interval.contains owns a pure predicate; range_filter.select composes it. No persistence or external service.\n',
    'docs/architecture/00-foundation/design-constitution.md': '# Design constitution\nIdentity: interval-constitution-v1. Apply mature practice, complete semantics, cohesive ownership, minimum necessary complexity and one-way debt convergence. Keep both functions pure.\n',
    'docs/architecture/06-governance/change-contract.md': '# Architecture change contract\nIdentity: interval-change-contract-v1. Concerns: interval-concerns-v1. Compare actual ownership, dependencies, state and normal behavior. No executable project Architecture check is required.\n',
}


def _template(template: Path) -> str:
    for relative in ('AGENTS.md', '.codex/config.toml', '.trellis/workflow.md',
                     '.trellis/guru-team/extension.json'):
        if not (template / relative).is_file():
            raise ValueError('Normal matching Codex installation is missing: ' + relative)
    for path in (template / '.trellis/tasks').rglob('task.json'):
        task = json.loads(path.read_text())
        bootstrap_deliveries = task.get('deliveries', [])
        unexecuted = all(
            delivery.get('profile') == 'manual' and delivery.get('phase') == 'planning'
            and not delivery.get('plan_ref') and not delivery.get('candidate')
            and not any(delivery.get('results', {}).values())
            and not any(delivery.get(name) for name in
                        ('publication_result', 'delivery_result', 'stop_result'))
            for delivery in bootstrap_deliveries)
        if (task.get('id') != '00-bootstrap-guidelines'
                or task.get('source') != {'kind': 'no_issue'}
                or not unexecuted or task.get('completion_results') or task.get('closure_results')):
            raise ValueError('Template contains a business Task, Delivery or current result before native execution.')
    if run_git(template, 'status', '--porcelain'):
        raise ValueError('Use the installation owner\'s clean committed template.')
    return run_git(template, 'rev-parse', 'HEAD')


def stage(template: Path, run: Path, *, case: str, python: str = sys.executable) -> dict:
    if case not in CASES:
        raise ValueError('Unknown public-entry case.')
    if run.exists():
        raise ValueError('Use a fresh run root; old failures are retained.')
    head = _template(template)
    run.mkdir(parents=True)
    repository = run / 'repository'
    clone = subprocess.run(['git', 'clone', '--quiet', '--no-local', str(template), str(repository)],
                           text=True, capture_output=True, check=False)
    if clone.returncode:
        raise ValueError('Cannot clone the selected matching installation: ' + clone.stderr)
    for name, value in (('user.name', 'Public entry fixture'),
                        ('user.email', 'public-entry@example.invalid'),
                        ('maintenance.auto', 'false'), ('gc.auto', '0')):
        run_git(repository, 'config', name, value)
    # Bootstrap is the existing deterministic dependency owner, not a patch or
    # copied private state from the template's original machine.
    runtime = repository / '.trellis/guru-team/runtime'
    bootstrap = subprocess.run([python, str(runtime / 'bootstrap.py'), '--repo', str(repository),
        '--runtime-assets', str(runtime), '--python', python, '--json'],
        cwd=repository, capture_output=True, text=True, check=False,
        env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    write_json(run / 'bootstrap-result.json', {'returncode': bootstrap.returncode,
        'stdout': bootstrap.stdout, 'stderr': bootstrap.stderr})
    if bootstrap.returncode:
        raise ValueError('Original runtime bootstrap failed; retain bootstrap-result.json.')
    for relative, content in FILES.items():
        target = repository / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding='utf-8')
    run_git(repository, 'add', '--', *FILES)
    run_git(repository, 'commit', '-qm', 'stage public-entry business authority')
    provider = repository / '.trellis/.runtime/guru-team/evals/chain-provider'
    (provider / 'bin').mkdir(parents=True)
    bare = provider / 'remote.git'
    subprocess.run(['git', 'init', '--bare', '--quiet', str(bare)], check=True)
    for name, value in (('user.name', 'Public entry provider'), ('user.email', 'provider@example.invalid')):
        subprocess.run(['git', '--git-dir', str(bare), 'config', name, value], check=True)
    chain.configure_provider_transport(repository)
    run_git(repository, 'push', 'origin', 'HEAD:refs/heads/main')
    run_git(repository, 'update-ref', 'refs/remotes/origin/main', run_git(repository, 'rev-parse', 'HEAD'))
    issue = {'number': 1, 'url': 'https://github.com/example/stage-chain/issues/1',
        'state': 'OPEN', 'title': 'Implement inclusive selection', 'body': SOURCE,
        'updatedAt': '2026-01-01T00:00:00Z', 'comments': [], 'labels': [],
        'author': {'login': 'example'}, 'assignees': []}
    write_json(provider / 'state.json', {'bare': str(bare), 'prs': [], 'issues': [issue]})
    executable = provider / 'bin/gh'
    executable.write_text('#!' + python + '\n' + chain.PROVIDER, encoding='utf-8')
    executable.chmod(0o755)
    # This is execution transport, not an alternate invocation contract.
    transport = run / 'run-original-command.py'
    shutil.copy2(Path(__file__).with_name('public_entry_transport.py'), transport)
    preparation = {'case': case, 'template_head': head, 'repository': str(repository),
        'provider_bin': str(provider / 'bin'), 'transport': str(transport),
        'receipts': str(run / 'original-command-receipts.jsonl'), 'python': python}
    write_json(run / 'preparation.json', preparation)
    return preparation


def context(preparation: dict) -> str:
    repository = preparation['repository']
    argv = [preparation['python'], preparation['transport'],
        '--repository', '.', '--receipts', preparation['receipts'],
        '--provider-bin', preparation['provider_bin']]
    if preparation['case'] == 'N3':
        argv += ['--loss-observation', str(Path(preparation['receipts']).with_name('stdout-loss.json'))]
    transport = shlex.join([*argv, '--'])
    entry = str(Path(repository) / '.agents/skills/trellis-start/SKILL.md')
    read_body = (
        "import sys\nfrom pathlib import Path\n"
        "data = Path(sys.argv[1]).read_bytes()\n"
        "start = int(sys.argv[2]); end = min(start + 8000, len(data))\n"
        "while end < len(data) and data[end] & 0xc0 == 0x80: end -= 1\n"
        "sys.stdout.buffer.write(data[start:end])\n"
        "sys.stderr.write(f'bytes {start}:{end}/{len(data)}\\n')\n"
    )
    entry_read = shlex.join([*argv, '--', preparation['python'], '-B', '-c',
        read_body, entry, '0'])
    scenario = {
        'N1': '实现 example/stage-chain 的 Issue #1，按正常已安装平台入口完成这项工作。',
        'N2': '实现 example/stage-chain 的 Issue #1。调用方最初给的source对象是 {"kind":"issue","repo_ref":"example/stage-chain","number":1,"relation":"exact_source"}。保留这次普通输入的原始形态和首次实际调用；若原公开入口拒绝，依其公开诊断修正后接续。',
        'N3': '实现 example/stage-chain 的 Issue #1。在首次形成实际候选后，给 range_filter.py 增加说明两端包含的注释，再按原流程处理这个真实内容变化；在一个已成功的原步骤输出丢失时，使用该步骤的正常恢复入口继续同一对象。保留真实非通过与恢复前后结果。验收运输记录只供观察，不得作为业务恢复来源。',
    }[preparation['case']]
    return '\n'.join([
        scenario,
        '业务要求在源Issue及docs/source.md。工作范围是当前隔离仓库；完成正常交付、整体Completion、Closure与Finish。',
        '从此仓库正式安装的Codex入口开始，自行读取其公开workflow、Skill及必要引用，完成各原owner的实际语义判断。',
        '这是一次完整执行；在范围和方案不变时自主接续。保留当前流程要求的具体副作用展示，所有Git/GitHub操作仅作用于本地隔离仓库及其确定性provider。',
        '不要读取Guru私有实现来获取业务调用知识，不要修改已安装工具或修补执行器。遇到真实工具/前提缺口如实停止该路径。',
        '环境事实：origin连接本地Git transport；PATH中的gh只实现隔离provider，不能证明真实GitHub或生产效果。',
        '本次验收中，caller 自建的临时调用载体仅写入当前 checkout 的 repository 根下的 .trellis/.runtime/guru-team/evals/call-local/，首次需要时创建。',
        '进入 linked checkout 后，以其实际 repository 根解析该相对目录。载体形式仍按当前公开接口选择。',
        '为完整保留原命令的stdin、exit、stdout和stderr，每条自行选择的读取或执行命令使用此透明运输前缀，后接原argv；stdin原样转发：',
        transport,
        f'公开 Skill 目录所列入口的展开路径：{entry}。先完整读取该 Skill，再按其公开引用执行；不按平台目录名猜路径。',
        '每个 owner 先完整读取当前 Interface；按其声明的 schema 路径、invocation 和链接合同定位本次输入、owner_result 与所选输出的 schema/ref 正文，不按参数名猜文件名。',
        '下面是入口正文首段的只读命令。stdout 直接返回最多 8000 bytes 的连续 UTF-8 正文，stderr 的 bytes start:end/total 只表示读取位置：',
        entry_read,
        '后续公开文件复用此命令，仅替换文件路径和起始字节；从 0 开始，逐次使用上一段的 end，直到 end=total。每次工具调用只执行一个片段命令，完整消费正文后再读取下一片段。',
        '捕获成功或字节计数不代表已看到正文。按原 owner 要求读全正文后再组参、判断或写入；运行 session 先收齐终态。原校验失败保留诊断，修正走原 owner 的 fresh re-entry。',
        '独立 reviewer 仍按原 owner 的隔离与读序合同启动；caller 派发时仅传递上述正文读取方法和临时载体位置约束作为操作说明，不传 caller 判断或任务辩护。',
        '运输不提供命令名称、schema、当前判断或派生身份。读取和执行均由你按正常公开入口决定，不从旧错误或历史成功补造通过。',
        '最终回复原最后一步的完整实际stdout；若未能到达终点，报告实际停点和原诊断。不要生成替代出口。',
    ])


def observe(run: Path, preparation: dict, returncode: int) -> dict:
    path = Path(preparation['receipts'])
    receipts = [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []
    exits = []
    for index, row in enumerate(receipts):
        try:
            value = json.loads(row['stdout'])
        except (ValueError, TypeError):
            continue
        if row['returncode'] == 0 and isinstance(value, dict) and isinstance(value.get('exit_id'), str):
            exits.append({'command_index': index, 'output': value})
    report = {'status': 'observed', 'case': preparation['case'], 'native_returncode': returncode,
        'command_count': len(receipts), 'formal_outputs': exits,
        'nonzero_commands': [i for i, row in enumerate(receipts) if row['returncode']],
        'boundary': 'Isolated local Git/provider only. Raw command and native logs require semantic review; no pass is inferred.',
        'native_stdout': str(run / 'native-events.jsonl'), 'native_stderr': str(run / 'native.stderr'),
        'last_message': str(run / 'last-message.txt'), 'original_receipts': str(path)}
    if preparation['case'] == 'N3':
        loss = run / 'stdout-loss.json'
        report['stdout_loss'] = json.loads(loss.read_text()) if loss.exists() else {'status': 'not_triggered'}
    write_json(run / 'observation.json', report)
    return report


def execute(args) -> int:
    run = Path(args.run_root).resolve()
    preparation = stage(Path(args.installed_template).resolve(), run, case=args.public_entry_case)
    prompt = context(preparation)
    (run / 'native-context.txt').write_text(prompt, encoding='utf-8')
    if args.prepare_only:
        print(json.dumps({'status': 'prepared', **preparation}, ensure_ascii=False))
        return 0
    native = shutil.which(args.native_command)
    if native is None:
        write_json(run / 'observation.json', {'status': 'unsupported', 'reason': 'native CLI unavailable'})
        return 2
    codex_home = os.environ.get('CODEX_HOME')
    if not codex_home or not Path(codex_home).is_dir():
        raise ValueError('Supply the caller-owned isolated CODEX_HOME before native execution.')
    argv = [native, 'exec', '--strict-config', '--json', '--cd', preparation['repository'],
        '--model', args.model, '--output-last-message', str(run / 'last-message.txt'), prompt]
    environment = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1',
        'PATH': preparation['provider_bin'] + os.pathsep + os.environ.get('PATH', '')}
    for name in ('TRELLIS_CONTEXT_ID', 'CODEX_THREAD_ID', 'CODEX_SESSION_ID', 'CODEX_CONVERSATION_ID'):
        environment.pop(name, None)
    with (run / 'native-events.jsonl').open('w') as output, (run / 'native.stderr').open('w') as diagnostic:
        native_result = subprocess.run(argv, cwd=preparation['repository'], env=environment,
            stdout=output, stderr=diagnostic, check=False)
    report = observe(run, preparation, native_result.returncode)
    print(json.dumps(report, ensure_ascii=False))
    return native_result.returncode
