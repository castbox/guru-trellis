# #556 唯一 Test 与证据边界

状态：reviewed_delta；实现与聚焦验证完成，完整语义 Check/Review 仍由各原 owner 独立判断。本文件独占实际结果、first failure、fixture 与未验证边界。

| Test | 必须观察的对象 | 当前结果 |
| --- | --- | --- |
| T556-01 | apply/bootstrap 默认 PATH 与明确解释器、缺失/不可执行/非3诊断 | PASS：新增7项选择/失败保护纳入最终43项组合；shell明确覆盖默认失效时显式选择优先；直接installer不使用runner作默认目标 |
| T556-02 | minor admission、identity 维度、同身份复用、patch/path 不参与、minor 分流 | 实际CPython3.15只读admission通过，identity fcd303b616c52a278e1b6a8e；minor/patch/path分流与稳定性为fixture行为测试，不是wheel兼容证明 |
| T556-03 | locked install、Draft202012 probe、真实 public wrapper；依赖/检查失败保留 pointer 和旧环境，含 same-id repair | PASS：最终43项组合含复制式disposable view的真实locked bootstrap/public wrapper；依赖/公开检查失败比较原pointer和旧环境文件bytes/modes，same-id repair不覆盖旧target |
| T556-04 | 一个完整 matching current clean/reapply、无 jsonschema PATH、公开 wrapper、bytes/modes/sidecars/drift | PASS：verify_managed_python_update.py使用固定匹配CLI、原base精确marketplace workflow和PATH3.12.8无pip/jsonschema venv；完整Codex安装action=installed，managed runner直接reapply默认PATH选择action=reused；runtime id c5898e3ddcd9197c2cc683bf，installed校验passed，canonical spec一致，零conflict/sidecar，caller pointer未变，临时样本正常清理 |
| T556-05 | 原 runtime/cache/repair/resolver、installer 事务、必要 managed caller 定向回归 | 初次runtime/update/temp组合43项/47.885s/OK、routing45项/15.757s/OK。Check独立冻结源码重验：43项/58.835s/OK、45项/17.855s/OK、helper+transaction完整18项/397.261s/OK；首轮源码编辑期间17pass/1conflict及exact单项复跑仍保留 |
| T556-06 | source package、声明平台投影、静态/context、旧 dogfood 边界 | source package38/114通过；完整Codex样本installed validator校验bytes/modes，canonical spec一致。Task context validate通过但大文件注入截断需直接读取。旧dogfood ordinary apply和drift实际失败，见下文；完整平台矩阵未运行 |

## First failure 与安装前置

本轮 PATH python3 为 3.12.8；明确 `/opt/homebrew/bin/python3` 为 3.15.0。变更前原 bootstrap 的只读 `--print-identity --json --python /opt/homebrew/bin/python3` 返回 exit2/runtime_dependency_missing，未创建或切换环境。PATH 3.12 identity 计算成功。这只证明旧 admission 拒绝，不能证明 3.15 锁定依赖可安装。

代表性样本的本地匹配前置已核：CLI tar SHA256 `5aeeb81ca72508081b7dd94ddb7a19f69444714f78b3a38858d908196cc77916`、Core tar `45bbfee507ed4964649610f703a90ba01c5f5cea21fb95d0845f92ed45302967`。713 个 installed CLI 文件、270 个 Core 文件的 bytes/modes 均匹配对应 tar；不是只比版本字符串。先找到的另一同版本 CLI tar 不匹配，未用于验收。该组合仅为合同固定受控 local candidate，不是正式 released source-lock。

保留验证过程的普通失败：首轮30项中，两项因新增helper内的硬编码Skill fixture触发既有kernel边界检查，改为manifest声明的能力检查数据后修正；另一个错误来自缺少固定上游脚本环境，补足已核实matching candidate后继续。后续37项通过，但disposable view从symlink改成普通复制以避免额外Windows权限前提后，以最终组合重验为准。首次样本启动误用了不存在的解释器路径，argparse exit2、无目标写入；改用实际PATH解释器后完成真实样本。临时资源inventory新增前缀后，原预期列表也作相应同步。这些是验证装配/实现集成错误，不代表生产事故或额外fault matrix。

最后一轮routing先指出三个受控caller增加显式`--python`后的normalized hash陈旧；更新对应原inventory三项后45项通过。installer组合期间源runtime仍有编辑，一项declared-kernel测试产生conflict；冻结后exact测试重跑通过，未为该失败新增产品逻辑。代表性clean/reapply在最终Bash preflight和复制式view代码上再次通过。

独立Check补查untracked hygiene发现三份planning和extracted helper末尾多余空行，原tracked-only diff check未覆盖；精确移除4处EOF空行，需求/设计/批准scope和运行语义等价，不新增测试或重规划。冻结源码上的完整18项组合已另验exit0/OK，排除对首轮混合编辑结果的依赖；后续只刷新当前内容与直接依赖校验。

## 可复现入口

产品测试均通过源码checkout已有managed resolver，不以PATH依赖import作产品证据。组合使用`PYTHONPATH=trellis/skills/guru-team:trellis/presets/guru-team/scripts/python`；需要current upstream fixture时设置`GURU_UPSTREAM_DELIVERY_SCRIPTS`为已核matching CLI的`dist/templates/trellis/scripts`。

```sh
.trellis/guru-team/runtime/resolve-python.sh . .trellis/guru-team/runtime -m unittest runtime.tests.test_python_update runtime.tests.test_runtime.SharedRuntimeTests runtime.tests.test_temporary_lifecycle -q
.trellis/guru-team/runtime/resolve-python.sh . .trellis/guru-team/runtime -m unittest test_verify_throwaway_python_routing -q
.trellis/guru-team/runtime/resolve-python.sh . .trellis/guru-team/runtime -m unittest test_apply_guru_team_trellis_preset.ManagedPythonBootstrapBoundaryTest test_preset_transaction_installer -q
.trellis/guru-team/runtime/resolve-python.sh . .trellis/guru-team/runtime -m unittest test_preset_transaction_installer.PresetTransactionInstallerTest.test_installs_only_declared_runtime_kernel_files -v
.trellis/guru-team/runtime/resolve-python.sh . .trellis/guru-team/runtime trellis/presets/guru-team/scripts/python/verify_managed_python_update.py --trellis-cli /path/to/verified/current/trellis/bin/trellis.js
```

测试会话输出为本轮执行事实；未制造tracked原始日志或审查过程副本。上述CLI路径是调用者提供的固定匹配本地候选，不修改全局安装。

最终静态检查通过：35个当前改动文件中的15个Python AST、4个JSON、2个JSONL、1个shell语法及diff whitespace；没有触及的非生成代码达到3000行。Task context validate为4项implement/6项check通过，保留大文件注入截断提示，审查需直接读取正文。

源码旧dogfood实际执行ordinary `apply.sh --repo . --json`返回exit1/`upstream_delivery_migration_required`，在runtime/preset staging前拒绝；未迁移旧Task记录、未半升级。`check-dogfood-overlay-drift.sh`返回exit1，定位`.claude/commands/guru/finish-work.md`的既有模型差异；ownership validator自身通过。该边界在base已存在，不能计为本轮新模型同步成功。完整matching current样本的installed/parity结果独立于它。

## 未验证边界

完整 Python-minor、多平台 clean/existing/update/Release 矩阵、业务仓升级/生产运行、系统 Python/Homebrew 改动与软件 Release 均未执行。源码工程完整旧 dogfood 不做半升级；其 ordinary reapply/migration-required 与既有 drift 必须按实际结果记录，不能冒充新模型 parity 通过。公开 wrapper 能力 fixture 证明真实 schema runtime 路径，不代表真实任务的 AI semantic gate。
