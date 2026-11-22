# #900 发布入口迁移

固定前驱为 `f06eddb6ccf97ddd2d1a41c117692f5957cb2dc7` 的完整 Guru provider。其 workflow、包、运行时和声明平台共同解释已经执行的旧操作。

## 当前入口

提交后独立 Review 的 `passed` 交给发布 Architecture 资格。取得适用资格后，调用 `guru-publish-task-delivery:delivery_prepare_publication`。Publication 负责 AI readiness、中文 PR 标题和正文、剩余责任与未验证边界。公开 Delivery API 仍使用原 readiness 槽和 full_review predecessor。新记录使用 Publication owner。历史记录保留其 producer 身份。

通过 readiness 后展示实际 pending push/PR 动作。对同一候选和预览取得当前对话确认后，调用 `delivery_execute_publication`。候选变化交原 Review，架构资格变化交 Architecture 保持原评估顺序。已确认预览中的待执行动作或载荷实质变化时，重新展示并确认。当前接口的输入、退出和可执行例子见 [Publication](../../skills/guru-team/packages/guru-publish-task-delivery/SKILL.md)。

当前正常 workflow 退出旧 Delivery Review 的独立 `ready` 交接。新版安装时成套采用 canonical workflow、路由、公共接口、包运行时、受管规范和声明平台投影。已有工作树按适用的 `guru-upgrade-tools` 合同更新。读取实际 sidecar、managed drift 与 Task/session 读回结果。

## 在途操作

| 实际状态 | 当前续接 |
| --- | --- |
| 固定候选已审，尚未进入旧 readiness | 使用仍适用的独立结果及架构资格进入当前 Publication。 |
| 已写 readiness，尚无可恢复预览或发布事务 | Publication 读取同一 Delivery 和真实 PR。适用 full_review 保持时，用原 rework 回 reviewing，再执行当前 readiness 和预览。缺失或失效的审查回原 Review。 |
| 同一事务已有部分远端效果 | 先回读原动作和同一 PR。只对实质变化后仍待执行的动作生成当前预览。原事务保留归属及已经完成的结果。 |
| 已完成 push 或 PR 操作，输出遗失 | 原事务恢复同一结果，按事实补缺少的投影。旧格式操作使用匹配的原 provider 恢复已执行结果。 |
| 已有同一 Open PR，本地事务不可用 | 走原 shared Open PR 恢复，保持明确 PR 和来源。待执行动作使用当前发布前置。 |
| 已发现同一 PR 合并 | 已有 PublicationFact 时进入原 Merge 恢复。缺少 PublicationFact 时，仅在满足原归属前置的情况下进入 `delivery_adopt_merged_pr`。 |

历史早期 Draft 继续受 [MIGRATION-794](MIGRATION-794.md) 的原边界约束。控制面切换不授予远端写入权限。验证分别观察公开准备和执行、实质预览变化、同一事务恢复、Merge 接收及安装投影。
