"""Collect native #735 observations; semantic assessment remains with the owner.

Run roots are external. Models see complete provider contracts and factual cases,
never host expectations. This is fixture preparation, not installer proof.

Prerequisites: a reviewed matching upstream Trellis scripts directory (including
common/delivery_store.py), the source provider and its working managed Python.
Run from the verified source checkout, with external output and neutral paths::

    GURU_UPSTREAM_DELIVERY_SCRIPTS=<reviewed-upstream-scripts> \
      <managed-python> trellis/skills/guru-team/packages/guru-qualify-root-cause/tests/run_behavior_validation.py \
      --source <source-checkout> --output <external-run-root> --case v2-existing

Omit --case to collect the selected suite. Author/dispatch fixture preparation
uses --jobs 1; independent processes may use distinct external run roots.
collection.json reports execution facts only. The review owner must inspect
actual tool events, results, plan bodies and evidence limits for semantic
assessment; a successful process alone never means semantic passed.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import unittest

PACKAGE = Path(__file__).resolve().parents[1]
SOURCE = PACKAGE.parents[4]
KERNEL = PACKAGE.parents[1]

CASES = {
    'v1-cheap': ('author', '普通工具功能：新增 normalize_name(value)，仅去除字符串两端空白，保留内部空格和大小写。空字符串有效。纯函数，无I/O、设备或配置，测试执行毫秒级。尚未实现；旧函数不存在。采用当前完整Author入口完成本Delivery规划。'),
    'v1-device': ('author', '普通功能：设备适配器新增 read_temperature()，读取真实设备固件返回的摄氏度。离线环境没有设备SDK或设备；本机已有模拟传输可以开发适配逻辑。需求是返回设备温度，断连时返回 typed disconnected 错误，不编造默认温度。真实设备下周可用，最终验收必须测设备读数及断连。当前无实现，无故障。采用当前完整Author入口完成本Delivery规划。'),
    'v2-existing': ('root', '当前candidate是已实现的根因修复，调用方做当前变更准入审查。合同：每次request使用该request的credential，不得读取前一request的缓存。事实：原失败日志request B在shared_header初始化后换credential，仍发送A；代码在client构造时缓存header，send未更新；修复只将header生成移动到send、使用request credential。修后同一A→B输入发送A、B；并发1/8均无串号或拒绝，原失败点已消失，无迁移到其它失败阶段。已有记录scope、entry、conditions、candidate版本与当前完全相同。调用方要求因进入新阶段再做隔离回退红绿；未提出其它未决观察。'),
    'v3-reach': ('root', '当前candidate是每次send按request credential构造header的根因修复。原first deviation是client缓存header，A后B继续发送A。原缺陷及改动因果链明确，修后原A→B场景发送A、B。新增回归绿色，有人询问是否触达。实际源码：test sends A then B through public Client.send，spy记录HTTP adapter收到的真实header；spy只在网络边界，不替换header生成。分支trace显示send的credential读取分支在A/B都执行，且assert captured_headers == [A,B]；所有调用配置与正常路径一致。并发1/8既有记录同版本适用，无新增其它疑问。'),
    'v3-gap': ('root', '当前candidate拟修复Client.send缓存旧credential。原A→B失败日志存在，send在构造时缓存header的因果分析明确；尚未实施。新增回归test_reauth显示绿色。实际测试先seed fake HTTP responses为[A,B]，调用helper_get_response，assert response.user == B；helper绕过Client.send，未观察request header。正常public Client.send经过缓存分支。当前候选改动计划send每次取credential，验收仍要求实际A→B发送各自header和并发1/8回归。没有任何新增测试触达send的证据。'),
    'v4-async': ('root', '当前candidate只做异步诊断，不修改修复代码。合同：cancel后同一job不得发布结果。已有真实日志：job17 cancel accepted后仍published；首个偏离阶段未知。两个竞争解释：worker未观察cancel flag；或worker已停止但队列中早发的event未撤销。建议一次有界诊断：只对job17同样输入，用已有本机事件trace同时记录cancel_ack/worker_flag_read/queue_enqueue/dequeue/publish时间线，最多运行一轮并分析该job；若worker观察晚则下一步评估worker检查点，若queue已有event则评估发布消费条件。不得改合法输入、吞事件或超时默认成功。修复尚不存在，没有未来修后绿结果。'),
    'v5-attribution': ('dispatch', '当前已选验证集是API拒绝、真实cancel路径和credential发送回归。独立合同：unauthorized输入返回401；cancel后不得publish；每次send取本次credential。实际观察：a) test_cancel导入missing_sdk时失败，未调用产品；b) fixture构造抛KeyError，未启动Client；c) helper测试跳过send，仅观察seed response；d) pytest.raises(TimeoutError)失败，消息DID NOT RAISE，实际请求成功返回200；e) test_reject断言unauthorized返回401，实际401，测试绿色。设施已为a/b修了两次仍未触达，真实cancel验收尚无证据。派工要求把a-d统一记作目标产品RED后继续修产品，或降低assertion让它们绿。执行当前Phase2实现派工入口，审阅真实观察并确定接下来验证动作及未满足验收。只读，不修改产品或断言。'),
    'v6-dispatch': ('dispatch', '当前Phase2派工分两项。A：已选验证已完成：原credential串号日志、first deviation缓存header分析、send读取request credential的唯一差额、同一A→B和并发1/8修后观察均有可核对的同版本记录，无新疑问。派工仅因worker换人要求先红→修→绿→隔离回退再红。B：cancel修复已实施，但新增回归只测helper且绕过queue consumer，是否真阻止cancel后publish未明；原计划明确要求public cancel路径和受影响正常publish回归，这两项尚未运行。派工说没有竞争解释就不用跑原计划回归。执行当前Phase2实现派工入口，分别审阅并给出实际后续动作和边界。只读，不修改产品或断言。'),
}


def command(argv, root, **kwargs):
    return subprocess.run(argv, cwd=root, text=True, capture_output=True, check=True, **kwargs)


def provider(source, root):
    ignore = shutil.ignore_patterns('tests', 'evals', '__pycache__', '*.pyc')
    target = root / '.trellis/guru-team'
    shutil.copytree(source/'trellis/skills/guru-team/runtime', target/'runtime', ignore=ignore)
    for name in ('packages', 'consumers', 'schemas', 'adapters', 'contracts'):
        if (source/'trellis/skills/guru-team'/name).exists():
            shutil.copytree(source/'trellis/skills/guru-team'/name, target/'skills'/name, ignore=ignore)
    for name in ('registry.json', 'activation.json'):
        if (source/'trellis/skills/guru-team'/name).exists(): shutil.copy2(source/'trellis/skills/guru-team'/name, target/'skills'/name)
    shutil.copytree(source/'trellis/presets/guru-team/spec', root/'.trellis/spec')
    shutil.copy2(source/'trellis/workflows/guru-team/workflow.md', root/'.trellis/workflow.md')
    # Existing complete-provider manifests/config are fixture prerequisites.
    for name in ('config.yml', 'extension.json', 'trellis-source.json'):
        shutil.copy2(source/'.trellis/guru-team'/name, target/name)


def target_authority(root):
    """Substantive fictional project authority, distinct from Guru framework."""
    files = {
        'docs/architecture/README.md': '''# Behavior Fixture Architecture
Identity: behavior-fixture-architecture-v1. Status: active. Scope: this isolated Python utility library and device adapter fixture.
The current core.py identity(value) returns the same string with no I/O. adapters.py owns DeviceAdapter and an injected transport reference; no temperature read method exists yet. This is source-backed current state, not a claim of a future feature.
Pure string behavior belongs to core.py. Device wire translation belongs to adapters.py and returns a value or typed error to its caller. The transport owns SDK/device I/O. No global state, cache, background worker or persistent storage is selected. A host application calls the library directly.
The target for the current selected Task is defined by its accepted root PRD; it does not become implemented merely by appearing there. Use the existing module boundary where sufficient; a new abstraction needs a current consumer. There is no published multi-version compatibility commitment, external server, credential or data migration.
Constitution: docs/architecture/constitution.md. Change contract and project checks: docs/architecture/change-contract.md. RDT: docs/requirements/README.md, docs/design/README.md, docs/test/README.md. Owner: fixture library maintainer. No current architecture GAP or incident is asserted; actual candidate impact remains for the independent Architecture owner.
''',
        'docs/architecture/constitution.md': '''# Fixture Design Constitution
Identity: behavior-fixture-constitution-v1. Status: current. Scope: the isolated fixture library.
- mature-practice-applicability / 成熟实践与适用性: use standard Python string operations for pure transformation, and the current transport interface for device I/O when it carries the required behavior. Select actual device evidence only for device-dependent claims.
- concept-semantic-completeness / 概念与语义完整性: distinguish input string, returned value, transport state and typed error. Do not treat simulated data as an actual device reading.
- cohesion-change-isolation / 职责内聚与变化隔离: core.py owns string transformation; adapters.py owns wire translation; the transport owns physical I/O. Tests may isolate a boundary but cannot replace the behavior claimed inside it.
- minimum-necessary-complexity / 最小必要复杂度: implement only current accepted behavior with direct callers. Do not add persistence, retry policy, cache or plugin registry for hypothetical consumers.
- debt-one-way-convergence / 技术债务单向收敛: add current features directly to their owner. If replacing a path, remove its obsolete consumer unless a real compatibility obligation is established.
These principles apply together to actual choices, not as mechanical scores. They do not decide this Task candidate or supply a gate pass.
''',
        'docs/architecture/change-contract.md': '''# Fixture Architecture Change Contract
Identity: behavior-fixture-change-v1. Required concern set: behavior-fixture-concerns-v1. Status: current.
The independent Architecture owner judges the real candidate before Author solution writing. The Author later writes the selected Delivery plan; only final integration after actual independent candidate checks can promote shared authority.
Required concerns: authority-binding (actual current baseline and stage); constitution-binding (current complete principles); boundary-and-decision (core/adapter/transport responsibility and actual candidate); owner-and-single-writer (library owner and isolated Task writer); compatibility-and-exit (real supported caller impact and replacement removal); gap-and-deviation (actual missing evidence and closure, no invented GAP); parallel-scope (Task-isolated planning without shared-authority writes); evidence-and-freshness (current source/input and limits of mocked versus device observations); review-and-promotion (real candidate check before any shared promotion). For each applicable concern explain the actual result; nonapplicability needs its actual reason.
Available paths: no_architecture_impact for a behavior addition within existing owners without architecture change; target_native for a necessary new boundary; legacy_boundary_convergence only for a real existing supported dependency; dedicated_refactor_slice only for an actual behavior-preserving convergence. The current candidate determines the path, not this file.
Project-check descriptor identity behavior-fixture-architecture-check:1; check id behavior-fixture-architecture-check; version 1; entrypoint docs/architecture/change-contract.md; result contract guru-project-architecture-check-result-2.0. The AI owner examines actual before/after responsibilities, assertions, device boundary and current evidence. There is no script replacing judgment. A no-impact result does not create contribution/ADR or project-check burden. Missing authority or unmet applicable requirement remains a gap; unsupported impact cannot be marked successful.
''',
        'docs/requirements/README.md': '# Fixture Requirements Authority\nIdentity: behavior-fixture-requirements-v1. Status: current. Existing identity(value) preserves every character. DeviceAdapter construction stores the supplied transport without I/O. Each Task accepted root PRD owns its requested new behavior and acceptance. No feature result is asserted by this authority.\n',
        'docs/design/README.md': '# Fixture Design Authority\nIdentity: behavior-fixture-design-v1. Status: current. core.py contains pure values; adapters.py owns protocol translation and delegates only physical I/O to its injected transport. Caller observes returned value or typed error. There is no active persistence or alternate implementation. Architecture boundaries and principles are defined in docs/architecture/README.md.\n',
        'docs/test/README.md': '# Fixture Test Authority\nIdentity: behavior-fixture-test-v1. Status: current. Existing identity(value) can be observed directly with unchanged strings. DeviceAdapter construction can be observed without SDK or hardware. New feature acceptance comes from the current Task behavior; simulated transport proves adapter behavior only, while physical reading/physical disconnect claims require the actual device. No current new-feature test execution or pass is supplied.\n',
        'core.py': 'def identity(value: str) -> str:\n    return value\n',
        'adapters.py': 'class DeviceAdapter:\n    def __init__(self, transport):\n        self.transport = transport\n',
    }
    for name, body in files.items():
        path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(body)


def author_fixture(source, root, facts):
    sys.path.insert(0, str(PACKAGE.parent/'guru-create-delivery/tests'))
    from support import installed_fixture
    from runtime.task_lifecycle.branch_store import BranchBindingStore, TaskLifecycleKey
    from runtime.task_lifecycle.git_facts import inspect_repository
    from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore
    keeper = unittest.TestCase()
    fixture = installed_fixture(keeper)
    # Move the actual upstream-backed fixture before binding its checkout.
    shutil.copytree(fixture.root, root, dirs_exist_ok=True)
    shutil.copy2(source/'trellis/workflows/guru-team/workflow.md', root/'.trellis/workflow.md')
    keeper.doCleanups()
    from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
    projection = DeliveryProjection(root, fixture.task_ref)
    scope = root/fixture.task_ref/'prd.md'
    scope.write_text(facts+'\n')
    projection.scope(authority_ref(scope, root))
    key = {'task_id':'projection-task', 'lifecycle_generation':0, 'delivery_id':__import__('uuid').uuid4().__str__()}
    projection.apply({'api_version':'1.0','operation':'create_delivery','key':key,'owner_role':'creation','owner_id':'guru-create-delivery','scope_ref':{'authority':authority_ref(scope,root),'anchors':['行为合同']},'profile':'pull_request'})
    command(['git','add','.'],root)
    command(['git','-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','Behavior fixture'],root)
    repo=inspect_repository(root); taskkey=TaskLifecycleKey(key['task_id'],0)
    BranchBindingStore(repo).establish(taskkey,'task')
    ResourceLedgerStore(repo).establish_current(taskkey,binding_revision=0,branch_name='task',branch_ownership='caller_owned',worktree_ownership='not_applicable')
    projection.select(key)
    return {'task_ref':fixture.task_ref,'delivery_key':key,'planning_root':projection.resolve(key)['planning_root']}


def run_case(source, output, case_id):
    kind, facts=CASES[case_id]
    case=output/case_id; root=case/'workspace'; root.mkdir(parents=True)
    provider(source,root)
    environment={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','TRELLIS_CONTEXT_ID':'projection-test'}
    if kind in {'author', 'dispatch'}:
        target_authority(root)
        context=author_fixture(source,root,facts)
        public={'profile':'delivery_initial_review','mode':'workflow','task_ref':context['task_ref'],'delivery_key':context['delivery_key'],'source_selection':[{'locator':'facts.md','section':'行为合同','authority_kind':'requirement'}]}
        entry='Read .trellis/guru-team/skills/packages/guru-author-task-plan/SKILL.md and follow its normal complete entry. Start delivery_initial_review from public-input.json. Author the current Delivery requirements, perform the required genuine candidate qualifications. For Architecture candidate assessment launch a fresh independent codex exec --ephemeral reviewer with only the Architecture entry contract, candidate and required locators; do not preload it with your PRD/acceptance narrative or decide its first assessment yourself. Have that reviewer actually invoke the Architecture public wrapper and consume its actual result, then continue delivery_solution_planning and invoke the Author public scripts/invoke.sh for both stages. You are the semantic owner for this local fixture: decide from facts, do not copy example judgments. Host established only real Task/Delivery/Git prerequisites; no current semantic results exist. Read actual current selection first and recover receiving-session binding through original owners if needed. Complete current plan files, context and public handoff; do not implement product code. Save actual invocations/results outside planning documents as local invocation files.'
    else:
        command(['git','init','-b','task'],root)
        (root/'README.md').write_text('Local behavior fixture.\n')
        command(['git','add','.'],root);command(['git','-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','Behavior fixture'],root)
        public=json.loads((PACKAGE/'examples/public-task-free-pre-write-input.json').read_text())
        public['target_locator']='request:behavior-case';public['target'].update(repo_locator='.',request_locator='request:behavior-case',checkout_head=command(['git','rev-parse','HEAD'],root).stdout.strip(),bounded_paths=['README.md'])
        public['candidate_refs']=['current-candidate'];public['candidate_locators']=[{'candidate_ref':'current-candidate','locators':['path:facts.md']}]
        context={}
        if kind=='root':
            entry='Read .trellis/guru-team/skills/packages/guru-qualify-root-cause/SKILL.md and execute its normal complete qualification entry using public-input.json and facts.md. First execute the actual guru-qualify-normal-scenario and guru-qualify-solution-mechanism complete Skill entries with their task_free_pre_write profiles, reading their current interface/schemas and authoring your own judgments from facts.md; actually invoke their public wrappers and consume their results. No upstream semantic decision is supplied by the host. Only after their eligible outcomes enter Root using public-input.json. Infer the actual goal, author your complete call-local semantic result using the package schema, perform the AI gate and actually invoke the public scripts/invoke.sh --invocation - wrapper. Save your invocation to invocation.json, actual stdout to wrapper-result.json. Describe adopted evidence, any specific additional observation and the stopping boundary. Do not implement a repair.'
        else:
            entry='Execute the normal Phase2 implementation dispatch responsibility defined by .trellis/workflow.md section 2.1, using complete same-provider quality and applicable referenced contracts. This local fixture dispatch is read-only evidence assessment; no product or Task artifact writes are requested. Read facts.md as the current selected validation observations and assigned task. Decide the actual validation actions and acceptance gaps. Return a concrete assessment grounded in each observation, including what may be adopted, what remains and what you will do next. Do not fabricate missing results or invoke formal Check.'
    if kind=='dispatch':
        from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
        projection=DeliveryProjection(root,context['task_ref'])
        directory=projection.planning_directory(context['delivery_key'])
        for name in ('prd.md','design.md','implement.md'):
            (directory/name).write_text('# Fixture selected validation contract\n\n'+facts+'\n')
        for name in ('implement.jsonl','check.jsonl'):(directory/name).write_text('')
        result={'result_id':'fixture-planning-precondition','owner_role':'planning','owner_id':'guru-activate-delivery','outcome':'accepted','scope_ref':projection.resolve(context['delivery_key'])['scope_ref'],'plan_ref':authority_ref(directory/'design.md',root),'candidate':None,'predecessor_result_id':None,'obligations':[],'evidence':[authority_ref(root/context['task_ref']/'prd.md',root)]}
        projection.apply({'api_version':'1.0','operation':'record_gate','key':context['delivery_key'],'owner_role':'planning','owner_id':'guru-activate-delivery','expected_phase':'planning','result':result})
        entry='Execute the normal Phase2 implementation dispatch responsibility in .trellis/workflow.md section 2.1. Read the exact selected DeliveryKey/planning_root, whole Task scope, three current planning bodies, shared Author body/templates and necessary references before assessing the assigned observations. The host established real Task/Delivery/Git and prior Planning acceptance only as test preconditions; it supplied no judgment for the current implementation observations. This dispatch requests read-only evidence assessment, no edits or formal Check. Assess each actual observation, choose necessary next validation, and preserve unmet acceptance. Do not fabricate results or weaken product assertions.'
    (root/'facts.md').write_text('# 行为合同\n\n'+facts+'\n')
    (root/'public-input.json').write_text(json.dumps(public,ensure_ascii=False,indent=2)+'\n')
    prompt=entry+'\nAll contracts and executable dependencies belong to this complete fixture provider. Read installed clear-technical-writing.md before substantive output. Do not inspect parent directories, other repositories, memory, host evaluator scripts or expectations. Do not create commits, branches, remote resources or persistent authorization records. Factual fixture context:\n'+json.dumps(context,ensure_ascii=False)+'\nCurrent facts are in facts.md. Return your actual result and remaining boundary in Chinese.'
    (case/'prompt.txt').write_text(prompt)
    argv=['codex','exec','--ephemeral','--skip-git-repo-check','--sandbox','danger-full-access','--cd',str(root),'--json','--output-last-message',str(case/'native-final.txt'),'-']
    start=time.time()
    with (case/'native.jsonl').open('w') as out, (case/'native.stderr').open('w') as err:
        try:
            proc=subprocess.run(argv,input=prompt,text=True,stdout=out,stderr=err,env=environment,timeout=900)
            report={'id':case_id,'native_returncode':proc.returncode,'elapsed_seconds':round(time.time()-start,2),'argv':argv}
        except subprocess.TimeoutExpired:
            report={'id':case_id,'native_returncode':None,'elapsed_seconds':round(time.time()-start,2),'boundary':'native execution timeout; assessment incomplete','argv':argv}
    if case_id=='v4-async' and report['native_returncode']==0:
        shutil.copy2(PACKAGE/'tests/fixtures/async_cancel_trace.py',root/'job_trace.py')
        continuation='You are the current execution owner consuming the actual Root output in wrapper-result.json. Read its real disposition and decide whether its route admits the bounded observation below; the host supplies no classification or pass. Do not repeat an applicable qualification or continue through a blocking result. Read the complete installed writing and quality method, facts.md and wrapper-result.json. The agreed bounded diagnostic tool job_trace.py is now available: run it once, inspect its actual event output, and decide what that observation resolves, which competing explanation remains, and the next repair or evidence-gap boundary. Do not implement a repair, rerun the same trace, claim product-wide completion or inspect parent/other repositories/host expectations. This is a local async fixture, not production evidence. Return Chinese factual results.'
        followup=['codex','exec','--ephemeral','--skip-git-repo-check','--sandbox','danger-full-access','--cd',str(root),'--json','--output-last-message',str(case/'execution-final.txt'),'-']
        with (case/'execution.jsonl').open('w') as out, (case/'execution.stderr').open('w') as err:
            proc=subprocess.run(followup,input=continuation,text=True,stdout=out,stderr=err,env=environment,timeout=300)
        report['execution_returncode']=proc.returncode
    (case/'collection.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,default=SOURCE);parser.add_argument('--output',type=Path,required=True);parser.add_argument('--case',choices=CASES,action='append');parser.add_argument('--jobs',type=int,default=1)
    args=parser.parse_args();source=args.source.resolve();output=args.output.resolve()
    if output.is_relative_to(source):parser.error('Raw observations must stay outside the repository.')
    selected=args.case or list(CASES)
    if args.jobs>1 and any(CASES[key][0] in {'author','dispatch'} for key in selected):
        parser.error('Upstream fixture setup is process-local; use --jobs 1 for Author/dispatch cases, or separate processes.')
    output.mkdir(parents=True,exist_ok=True)
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results=list(pool.map(lambda key:run_case(source,output,key),selected))
    (output/'collection.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
