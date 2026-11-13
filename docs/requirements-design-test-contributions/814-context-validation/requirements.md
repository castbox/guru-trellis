# #814 需求差额

原 owner 为 `guru-maintain-requirements-design-test-ssot`。来源为 Issue #814、Task 根 PRD R1—R6/AC1—AC5 和 D1 已接受规划。直接 consumer 是原 RDT 整合、独立 committed Review 及 Task Completion；本文件不产生这些阶段的通过结果。

适用 before 为 Git `ce4644392d1ed9815d59071388b9bff9978d1cee:docs/requirements/current/runtime-location.md`。完整拟写为该固定正文原样保留，再在文件末尾追加下方完整章节。该方式唯一确定完整 after，不复制未变正文。R718、R760、R769、#813 的定义、稳定身份及历史来源保持；本次没有删除或替换。

## 原生 context 的正常规模行为（#814）

本单元追加定义修订：`context-adoption-814`。来源为 [Issue #814](https://github.com/castbox/guru-trellis/issues/814)，适用 before 为 Git `ce4644392d1ed9815d59071388b9bff9978d1cee`。原 `fixed-git-task-creation-813` 修订及此前条款保持。本节补充原生 context 正常规模行为；设计由对应单元 D814 承接，验证由 T814 承接。

| Identity / Behavior | 完整行为与条件 |
| --- | --- |
| R814-01 / BEH814-CONTEXT | 实际安装的原生 context 入口在正常小规模及约169个合法注册 worktree 下，解析当前会话或显式 Task，返回正确 owner、Task/generation 和唯一 checkout。消除同一次解析内无关重复 Git 开销时，仍须校验全部 eligible peers，保留原 prunable 例外、选中分支独立查询，以及必要 stale/conflict/非唯一拒绝；不能以跳过校验、借用其他会话或只改 PATH 替代修复。 |
| R814-02 / BEH814-PROBES | 公开 tools 的真实 runtime-contract/context probes 保持两个10000ms预算。验证分别记录实际入口、拓扑、Git调用来源与耗时；单次样本不是所有机器或所有 native 命令的延迟保证。外层等待结束先核原 executor，未知终态继续跟随原执行；需要恢复时仍由原 tools owner 使用同一 operation/ref/candidate/plan/preimages。安全诊断、原失败与未自然复现边界须保留。 |

来源代码与目标自身成功仍遵循 R718-03/11；原事务与 peer/common 保持仍遵循 R769。上述条款不改变公开身份格式、Task/Delivery/session writer 或恢复 authority。正式来源采用和实际工程结果分别成立；完整 Release 矩阵及 Task 整体完成继续由原 owner 独立判断。
