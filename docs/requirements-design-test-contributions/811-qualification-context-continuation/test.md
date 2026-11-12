# #811 验证差额与实际结果

完整策略为 proposed/docs/test/current/{qualifier-applicability,local-fix-intake}.md 中的 TST-811。
本文件记录当前源码、独立公共链及 matching tools 采用的分层工程结果；正式 Check/full_review 和独立 committed 质量链尚未完成。验收按 2026-11-12T13:06:20Z 的 live #811 采用本项独立正常 Task/Delivery 场景，不依赖发布 Task、版本或时间。

## 前序源码与公共调用观察

本节保留本轮范围刷新前的原始结果截止。新的执行结果见下文“当前独立验收补证”，不回写旧失败或把定向结果称作当时整包全绿。

测试使用已验证的 managed Python，Task/Delivery fixture 采用真实 Fork 的公共 scripts。
各包测试由 `python -m unittest discover -s <package/tests> -p 'test_*.py'` 执行；
公共链使用原 invoke/record/check wrappers，gh 替身只替代声明的外部 GitHub 边界。
以下结果证明确定性公共链与工程合同，不证明真实 Agent 语义判断或远端副作用。

| 范围 | 实际结果 |
| --- | --- |
| Normal / Solution | 各 26/26 通过；Normal 只保留前序执行结果，未保留独立绿色日志 |
| Clarify | 34/34 通过 |
| Sync | 21/21 通过，含 reviewed-plan source_locators 接续 |
| Shared current graph | 4/4 通过 |
| Discovery 原 contract/runtime | 前序执行结果 20/20 通过，未保留独立绿色日志 |
| Discovery 公共确认链 | 原两 profile 的缺失、当前、普通 stale 及 body mutation 刷新通过；最后一次整包运行 24 项中有 1 项 no_issue fixture 失败。修正后 no_issue、nonTask 和新增 comment 用例分别定向通过；没有新的整包全绿命令 |
| Interface/current consumer | source discovery 的三个实际出口查询成功；context4、Sync 自有 call-local input 与两类 authoring profile 可定位，reviewed-plan 字段保持 |
| Ordinary run5 | 原 runner 实际执行 Interface1.10 Sync 的 skipped-route，产生 passed receipt；原 grader 消费实际 evidence_path 通过 |
| Installer fixture 投影 | 1/1 通过；只证明 fixture 内投影，不证明本 checkout 已采用 |
| Manifest / pinned assets | 定向 2/2 通过；旧 qualification adapter2、run3、manifest3/current3 的固定字节测试保持 |
| Source package checker | passed：43 active、41 command-backed、2 instruction-only、126 commands |
| 静态检查 | 实施 owner 报告 528 个 Python 文件内存 compile 通过；root 再核 git diff --check 通过 |

root 相对固定 B `ca0b21f0dfc754a6979f919be14deee696719a4b` 检查 Git 修改、删除、重命名及类型变化路径，
既有 `trellis/**/schemas/**` 和 `trellis/**/examples/**` 无变化。这是 Git 内容差异检查，不扩称全部历史发布资产逐个 hash 实验。
root 对本次 25 个改动或新增代码文件按 .py/.sh/.js/.ts/.mjs/.cjs 筛选并计行，无文件超过 3000 行；最大文件为 2993 行。

Ordinary receipt 的实际位置为 `/private/tmp/guru-811-ordinary-run5/guru-sync-base-shared-run.json`。
reader 初试曾因把该 producer 路径写成 `/tmp` 而失败；改为读取实际 evidence_path 后定向通过。
no_issue 的初试失败涉及原 draft identity、issue_binding 及检索线索；修正保持原 draft body identity，
另以正式 accepted_scope locator 承接 authority。最后定向调用使用实际 Task.source.kind 识别来源。
新增 confirmation owner5 comment 用例实际执行 comment POST/GET，观察 Issue body 未变且 return_identity 保持。

## 可重放入口

测试环境为 managed interpreter 与固定 Fork scripts；本机绝对路径是本次验证环境，不进入公共 package：

```bash
TASK811_PY=/Users/wumengye/Library/Caches/guru-team/python/f0b89dabd24ef812b1244b8b/venv/bin/python
export PYTHONPATH=trellis/skills/guru-team
export GURU_UPSTREAM_DELIVERY_SCRIPTS=/Users/wumengye/Documents/GoProjects/Trellis-worktrees/source-lock-aa898d090fc27c9ce6145cfa3c787a6f400da4e2/packages/cli/src/templates/trellis/scripts
```

各包使用上述 unittest discover 入口。三个最终定向调用在 Discovery tests 下选择
`test_qualification_context_chain.py`，分别以 `-k` 选择
`test_legal_task_without_issue_uses_current_accepted_scope_no_issue`、
`test_legal_non_task_and_other_candidate_context_stays_separate`、
`test_confirmation_comment_refreshes_without_changing_issue_body`。

ordinary 原入口为：

```bash
bash trellis/workflows/guru-team/scripts/bash/run-skill-evals.sh --root . --mode source --skill guru-sync-base --adapter shared --case skipped-route --run-root /tmp/guru-811-ordinary-run5 --json
```

原 grader 的定向入口是 runtime/tests/test_eval_adapter_diagnostics.py 的
`test_ordinary_interface_run_is_generated_and_consumed_by_current_reader`。
Installer 投影入口是 tests/test_skill_packages.py 的
`test_production_eval_contract_registration_survives_installation`；fixture 使用原公开 Python 参数指定 sys.executable。
source checker 使用 `bash trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json`。
这些命令由实施 owner 根据保留入口整理为重放方式，不声称保留了全部原 shell 调用逐字记录。

## 设施诊断与证据边界

首轮系统 Python 缺少原 fixture 所需 PYTHONPATH/GURU_UPSTREAM_DELIVERY_SCRIPTS，未触达业务断言。
后续补齐原 fixture 环境并使用 managed interpreter。Installer fixture 的默认 PATH bootstrap 初试也未到达资产写入；
使用原公开 Python 参数指定已验证 interpreter 后通过。默认 bootstrap 的该次设施缺口不记作产品通过。
前期 normal artifacts、authoring selector 与公共链 fixture 的失败保留其实际截止；最终定向结果只替代已修复部分。

matching tools 已消费原冻结计划并正式返回 tools_upgraded；同操作恢复状态为 complete，无 failure。
实际采用为本 checkout 的 local_candidate，Guru 版本仍为 0.7.0-guru.8；版本号不代表正式发布。
目标自己的 resolver 选择已验证 managed Python，加载路径为本 checkout 的 .trellis/guru-team/runtime。
installed checker 通过：43 active、126 commands、9789 managed files；三平台为 claude/codex/cursor，conflict 与 sidecar 均为 0。
目标原生 get_context.py --mode continuation 返回当前 continuation 合同；原 owner 的实际原生能力检查也已完成。
dogfood drift 校验通过，包含 workflow、受管 spec、共享 Codex 入口、Claude/Cursor 投影及 mode。
installed Discovery context_ready、Clarify refresh_context、Sync baseline_ready 三个实际查询均定位到当前 consumer、context4 和目标自有输入。
其中两次并行 discovery 初试返回 runtime_dependency_missing；不改环境、不执行 repair 的顺序原入口复读均成功。
保留该诊断，不从重读成功推断并发稳定性或根因；原 Check owner 判断其对受影响覆盖的意义。
installed ordinary runner 实际执行同一 skipped-route，产生 Interface1.10/run5 passed receipt，
位置为 /private/tmp/guru-811-installed-run5/guru-sync-base-shared-run.json。
历史采用前后保留检查核对 Task 树、workspace 树、所选 task.json、AGENTS/config 原字节，以及当时一个 peer 的 HEAD 与既有 dirty 文件字节均未变；
原 tools owner 核对并保留 722 项 peer/pointer 观察。该结果只证明本次工具采用的保留边界。
此前外部 checkout 的只读准备没有执行采用或接续；其原始观察保历史含义，已不再是本项验收或阻塞。
当前 AC811-06 使用独立正常 Task/Delivery 公共链的真实 producer 输出、正式 clear 和原 caller 消费；fixture 语义输入如实标注，不冒充实际 Agent 或远端业务验收，不制造未决选择。现有覆盖的组合充分性仍交原 Check 判断。
该前序观察时，RDT/Architecture 尚为隔离拟写；当时 integration/readback、TaskCommit、独立 Check/full_review 和外部交付均未完成。
正式 Fork source lock、完整多平台/升级/Release 矩阵及生产效果保持未验证边界。


## 当前独立验收补证

最新 live #811 与当前 accepted scope 未再变化。原实施 owner 复核完整链的入口、setup、投影和观察后，
只对先前缺失可核验绿色记录的三组执行补证；没有重做未变机制或重跑其余已有有效结果。

| 当前实际执行 | 结果与原日志 | 证明范围 |
| --- | --- | --- |
| Discovery 的完整 test_qualification_context_chain.py | exit 0；5/5；175.393s；/tmp/811-reaccepted-context-chain.log | 两类确认各自当前/缺失/正常过期、两类body mutation、comment refresh、非Task与no_issue，以及真实clear后原caller消费 |
| Normal package 全包 | exit 0；26/26；2.161s；/tmp/811-reaccepted-normal-package.log | 当前normal合同与runtime；补前序独立绿色日志缺口 |
| Discovery 原test_contract + test_runtime | exit 0；20/20；33.004s；/tmp/811-reaccepted-discovery-original.log | 当前原合同/runtime及旧支持关系；这是独立命令，不称一次全Discovery整包命令 |

使用上述同一managed Python和固定Fork scripts。PYTHONPATH为本checkout的trellis/skills/guru-team，
PYTHONDONTWRITEBYTECODE=1。依次执行：

```bash
"$TASK811_PY" -m unittest discover -s trellis/skills/guru-team/packages/guru-discover-change-context/tests -p test_qualification_context_chain.py -v
"$TASK811_PY" -m unittest discover -s trellis/skills/guru-team/packages/guru-qualify-normal-scenario/tests -p 'test_*.py' -v
# cwd: trellis/skills/guru-team/packages/guru-discover-change-context/tests
"$TASK811_PY" -m unittest -v test_contract test_runtime
```

完整链的Task/Scope/Identity/Ensure/Bind/Delivery前置由原公开Fork脚本建立。fixture提供显式语义输入与repo-bound gh外部替身；
qualifier、Sync、Discovery、Clarify的被测出口都来自实际公共invoke，没有预填context/clear或snapshot。
consume校原identity、重读authority，再真实调用qualifier取得classified；该次语义输入仍属于fixture。
因此本结果证明独立合法场景内真实producer→consumer接续，不证明实际Agent语义判断或远端副作用。

原实施owner另修正Clarify canonical SKILL.md:237的失效Public Handoff锚点，
由#interface-14-public-handoff改为实际#interface-110-public-handoff；写前boundary通过。
这是已批准I811-04的等义引用修复，不改变机制。受管同步结果另按原tools owner实际结果承接。
原始失败、当时未保留日志与前序定向通过记录保持。正式Check/full_review和整体终态尚未建立。


## 当前引用同步与RDT整合

原tools owner针对已批准I811-04的唯一锚点差额，采用同一完整local_candidate与固定CLI/Core，
完成新的受管同步并正式返回tools_upgraded。公开tools冻结的212项action无字节差额；
四份Clarify Skill投影已包含正确引用，安装manifest由原installer生成。
初次prepare因既有routing管理hash偏差停止；原owner核该文件实际字节等于canonical后，
给出同内容replacement决定，再成功prepare并消费其原冻结计划。首次invoke的临时plan路径拼写错误在参数读取前拒绝；
更正同一实际文件路径后执行，无目标操作重放。

目标自身验证：installed checker passed（43 active、126 commands、9789 managed、conflict/sidecar均0），
日志 /tmp/811-reaccepted-installed-checker.json；原生get_context.py --mode continuation成功返回当前入口，
输出 /tmp/811-reaccepted-native-continuation.json。dogfood drift核workflow、spec、共享Codex及Claude/Cursor投影一致，
日志 /tmp/811-reaccepted-dogfood-drift.log。formal_fork_source_lock继续未验证；不声明完整矩阵或发布通过。

RDT原owner在当前scope的实际task_impact_sync返回candidate_ready后，核六个live shared目标均等于固定before，
将完整proposed定义整合到六个原current单元并逐项读回，状态integrated_pending_review。
根入口、共享index/system/ownership未写；Architecture整合由其原owner另行返回。
TaskCommit、独立committed Architecture/Check/full_review、readiness及外部交付仍未完成。
