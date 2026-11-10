# #773：Task 载体恢复的 RDT 隔离贡献

状态：proposed；原语义 writer：`guru-maintain-requirements-design-test-ssot`。
本候选承接 #773 当前 R1/R2、Task accepted_scope 和本 Delivery design/implement。
适用 authority 为 `guru-trellis-rdt`；固定 before 为
`313d80215f65777fc70893a90c6d8dce8005d6dd:docs/`，Architecture 为同 revision 的
`guru-trellis-architecture`。本贡献不更新 shared current，也不声明实现或测试通过。

## 差额与完整目标

本次为独立恢复能力的 addition。既有 `RDT-REQ-LIFECYCLE`、
`RDT-DES-LIFECYCLE`、`RDT-TST-LIFECYCLE` 继续拥有公共 Task/Delivery 模型、阶段及
通用跨环境接续。新单元只展开缺载体诊断、同身份文件恢复、显式工作区关联以及各
原 owner 的顺序/结果边界，不复制另一套 lifecycle authority。

完整拟写分别位于：

| 稳定身份 | 本贡献中的完整 proposed 定义 | 最终目标 |
| --- | --- | --- |
| `RDT-REQ-TASK-CARRIER-RECOVERY` | `proposed/docs/requirements/current/task-carrier-recovery.md` | `docs/requirements/current/task-carrier-recovery.md` |
| `RDT-DES-TASK-CARRIER-RECOVERY` | `proposed/docs/design/current/task-carrier-recovery.md` | `docs/design/current/task-carrier-recovery.md` |
| `RDT-TST-TASK-CARRIER-RECOVERY` | `proposed/docs/test/current/task-carrier-recovery.md` | `docs/test/current/task-carrier-recovery.md` |

这些目标是候选完整正文，尚未成为 current。完整目标正文已包含拟晋升后的状态、来源和实际观察截止点；只有原 writer 的
final_integration 写入及读回才使其生效，不能把规划预期改记为执行通过。
独立 Architecture 和完整 candidate Check 前必须可以读取全部拟写。通过后原 RDT
owner 重读真实目标及必要关系，整合、写入、读回；implementation 重新绑定实际
after，最终 Check 和 committed Review 覆盖这些内容。根入口和共享索引不变。

## 追踪与直接 consumers

| Requirement / behavior | Design responsibility / contract | Test strategy / scenario | 直接用途 |
| --- | --- | --- | --- |
| R773-01 / BEH773-DIAGNOSTIC | D773-01 / CON773-DIAGNOSTIC | T773-01；V1 | discovery/recorder 调用方从准确拒绝定位原恢复 owner。 |
| R773-02 / BEH773-CARRIER | D773-02 / CON773-RESTORE | T773-02、T773-04；V2/V4 | 恢复 Agent 核固定载体、完整规划、目标/写集，并由原 writers 恢复。 |
| R773-03 / BEH773-ASSOCIATION | D773-03 / CON773-C4C5 | T773-02、T773-03；V2/V3 | Branch/Ensure/Bind 按公开入口补缺关联并继续同身份。 |
| R773-04 / BEH773-ADOPTION | D773-04 / CON773-DISTRIBUTION | T773-05；V5 | 原工具、Check、Review owners 判断匹配采用和真实证据层次。 |

原历史 Publication/Delivery/full_review/readiness 缺口、普通 HEAD 候选规则、primary
支持和 caller_owned/not_applicable 语义在三层明确承接。没有 deferred scope、历史
补录、额外 store 或授权状态。实际 V1–V5 命中结果及限制已由原 RDT owner 接入 Test 单元；独立候选 Check 与
最终质量链尚待执行，不从 #223 旧结果推定本候选通过。

## 关系与维护边界

三叶互相引用，并关联原 lifecycle 完整单元、Branch canonical package、
`MIGRATION-773.md` 和 proposed `ADR-TASK-RECOVERY-ASSOCIATION`。Architecture 的
C4/C5 owner 关系和 ADR 由原 Architecture owner 单写，本贡献不晋升它们。
普通后续查询通过 current 目录和稳定身份发现各叶；不追加 root/current README、
shared index、全局版本或逐 Issue 完成台账。实际晋升不是 Delivery、Completion、
软件发布或业务恢复证明。
