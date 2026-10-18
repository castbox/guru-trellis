# #566：工具升级与所选旧任务维护解耦

本合同新增 `guru-upgrade-tools`、`guru-maintain-legacy-task`，以及原 Publish/Merge/Finish 的明确旧事实/控制入口。原 `guru-upgrade-installation` 的完整 Plan2、same-plan resume/rollback、普通 current-only parser 和业务生命周期不改义。不是把旧入口参数重新解释成tools-only。

## 依赖与执行来源

从完整 reviewed Guru canonical source加载Skill和runtime，`--root`指向目标context；旧目标dispatcher、Identity、Continuation和Reconcile都不是取得维护能力的前置条件。单独复制 `.agents/skills/` 或一个发现目录不能执行维护。

公共能力须来自匹配 CLI/Core 的 public package main `maintenance` namespace / Core `/task/maintenance`，实际 `maintenance_api=1.0` 及 `tools_install/task_conversion/legacy_closeout` 合同一致。版本号相同不证明构建相同；执行器核对实际包bytes/固定candidate身份。Guru不复制公共parser、projection、session/binding或恢复算法。

`source_locked`仍消费 `source/trellis-source.json` 的实际正式Fork。该锁当前为 `5c760463680ffc10a3f26957b330c57a4b0c3ff8`，尚不包含 #40 本地维护候选；正式入口须写前说明缺少前置，不能回退全局CLI、旧目标或任意同版本npm包。`local_candidate`仅供隔离开发验证，本任务不更新正式锁，也不把dirty本地包描述成发布能力。

## 新入口和不变的所有权

| 目标 | 独立入口 | 终态边界 |
| --- | --- | --- |
| 单checkout工具更新 | `guru-upgrade-tools` 的 install/resume/rollback | 工具安装结果；不代表任务转换、会话恢复或业务完成 |
| 所选旧任务继续执行 | `guru-maintain-legacy-task` 的 convert/resume/rollback | 目标自身正常native＋下一实际owner验证后接原continuation |
| 所选旧任务仅保留历史 | 同owner的history_closeout | rawarchive/note可读及准确carrier退役后停止，不进入正常Completion/Closure/Finish |
| 旧历史核验/私有控制 | 原Publish/Merge/Finish明确legacy profiles | 最小真实结果返回所选维护，不生成当前业务pass，不执行push/merge |
| 原完整安装/迁移 | `guru-upgrade-installation` 原profiles | 原Plan2保持独立，不隐式替代以上操作 |

各公共输入/出口是独立schema；具体字段、脚本、semantic gate和恢复合同由各完整canonical package的 `interface.json`、`references/contract.md` 独占。本文件不复制其步骤。新maintain/tools package登记为 `standalone_only`，不新增普通业务mandatory invocation。原owner新增旧路径exits只进入对应薄维护consumer，不能落入正常发布或完成路径。

## 单目标与runtime

显式checkout优先；未指定则保留原显式base/config及dev/develop/main/master/remote-default顺序，先选分支后找其唯一registered checkout。目标缺失、歧义或不可用不降级候选；不create/switch worktree或branch，不fetch/ff，不要求无关业务dirty清零。

工具资产归原preset installer。tools-only使用checkout-local ignored Python pointer，primary/linked均先读该override再原gitdir/common；不改common default、peer pointer或其实际解析的runtime。后续普通activation更新已有override的同一effective路径；原full upgrade同时备份和恢复该独立路径。没有override时保留原gitdir/common行为。旧Task/归档/规划/session/private control、用户config/spec保持。physically共享whole-.trellis工具存储的布局须写前阻塞。

## 成套切换与恢复

canonical packages、registry/Interfaces、public consumer schemas、command descriptors、extension inventory、必要workflow路由、runtime kernel、preset与发现投影必须同步安装。不得单独更新workflow或复制新Skill到旧dispatcher。官方Trellis update后仍按受支持marketplace选择与preset reapply恢复，不patch全局包、上游hooks或node_modules。

公共tools与selected-Task操作各有固定operation/recovery；Guru只保存原写集不可重建preimages和未完成阶段。普通重试不生成新ID、不覆盖原备份，不吞后续业务工作。归档后原私有owner从preserved源处理所选controls，不要求已移除active tree重新满足current parser。请求旧工具回退时先核对公共工具/数据兼容，再恢复Guru半边；后续Task转换不扩大原tools备份。

旧事实profiles只服务明确受支持旧数据的转换/历史保留。支持集合退出后通过后续显式migration删除，不加入普通current双读，不按一次扫描猜测无历史便自动删除公共API。

## 使用与证据

在目标AI会话中使用：

> 从完整、匹配的Guru新版来源读取 `guru-upgrade-tools` 或 `guru-maintain-legacy-task` 的SKILL和完整contract。只处理我明确指定的checkout和Task；未指定checkout时按其原base resolver选分支再绑定checkout。先只读准备、展示精确写集和依赖边界，经当前对话确认后执行；工具、转换、native续接、历史事实和业务完成分别报告。不要更新其他worktree，不要以旧Reconcile作为启动前置。

确定性帮助入口从完整来源运行，不先调用目标旧dispatcher：

```bash
bash "$GURU_SOURCE/trellis/skills/guru-team/packages/guru-upgrade-tools/scripts/preview.sh" --help
bash "$GURU_SOURCE/trellis/skills/guru-team/packages/guru-maintain-legacy-task/scripts/invoke.sh" --help
```

真实结果由 [唯一Test](../../../docs/requirements-design-test-contributions/566-single-checkout-upgrade/test.md)拥有。定向source/installed/native结果、正式来源、真实业务采用和Release矩阵分别陈述；规划、代码存在或上游公共fixture不能替代任何后续证明。
