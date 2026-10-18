# ADR-017 候选：独立旧安装迁移与 current-only 生命周期

状态：`proposed`；所属 task：`.trellis/tasks/10-06-495-legacy-installation-upgrade`；
expected current：`current-main-0.6.17-guru.71`。
来源：[Issue #495](https://github.com/castbox/guru-trellis/issues/495)、
[混合库存合同](https://github.com/castbox/guru-trellis/issues/495#issuecomment-6014030676)与
[候选交付顺序](https://github.com/castbox/guru-trellis/issues/495#issuecomment-6018378988)。
本文件由任务独占，供 Architecture 与独立 Branch Review 审查；尚不是 shared current 决策。

## Context

#481 退役任务人员模型，并拒绝旧安装和旧 task.json。后者阻止实际
core `0.6.16` / Guru `0.6.16-guru.41` 业务仓采用当前无人员版本。
移除人员概念与禁止原地升级是两个独立决策。#495 修订迁移拒绝边界，
保留 #481 无人员模型与 ADR-015 的 TaskId、source、session、branch、checkout
及 writer ownership；ADR-016 的 Delivery、Completion、Closure、Finish 分离不变。

## Proposed decision

1. 旧格式只在从完整目标 source 加载的 standalone `guru-upgrade-installation`
   及正式 Fork migration 边界读取。AI 审查精确来源、逐文件/任务动作、交付事实、
   恢复/回退适用性；当前对话确认具体写入后，脚本仅执行确定性转换和校验。
2. Fork 单写 core 与 task schema；Guru 单写自身受管资产迁移并复用官方
   marketplace/preset owners。转换保留合法 TaskId 和业务事实；generation/source
   按明确投影建立，branch/checkout/session 由既有 current owners 核对 live facts。
   不增加另一 task、binding 或 session writer，不把旧人员或路径当作当前 authority。
3. 正常 runtime 不双读旧生命周期。known-legacy inventory 只保留 TaskId/TaskRef
   占用并排除其 current candidate 身份；迁移私有 deferred TaskRef/原字节校验
   只供 preserve 与 installed inventory 消费。直接旧目标、身份冲突、无效 current
   与未诊断旧记录仍阻塞；历史归档/journal 原字节保留且不成为恢复 authority。
4. 转换成功与任务接续分开判断。planning 和未发布 in_progress 必须实际进入
   current owners 与 fresh Planning/check；旧 gate 不成为新 pass。已有 PR、merge
   或旧 Finalizer/Finish 在途按 live facts 逐案处置，不重复外部副作用，
   不承诺全部旧状态自动接续。
5. 私有备份仅供同 owner 的普通部分恢复与有界回退。core 完成时固定 task-content
   锚点，首次写前固定相关 control 基线；resume 不吸收新增业务事实作回退基线。
   回退只在没有新版工作时恢复实际动作路径的 bytes/modes，不重写 Git/远端历史。
6. 支持来源限定为上述精确旧版本，目标为固定正式 Fork 与提供本能力的 Guru 后继。
   停止支持该来源时，由 migration/Fork owners 删除局部旧 parser、executor、schema、
   tests 与文档入口；不留下正常 runtime fallback 或长期兼容双轨。

## Alternatives and consequences

维持全部拒绝无法满足已接受的业务仓升级需求；删除整个 `.trellis` 会丢失有效任务
及定制；正常 runtime 双读会恢复已退役模型并增加持续维护路径。因此选择一次性、
显式、可退出的迁移边界，新增复杂度只服务来源投影、普通恢复与回退的直接消费者。
不增加攻击模型、并发锁、额外 crash 协议或全链审计状态。

## Adoption and verification boundary

责任与验收追踪由本任务的 [RDT trace](../../requirements-design-test-contributions/495-legacy-installation-upgrade/traceability.md)
及 [Architecture contribution](./495-legacy-installation-upgrade.md) 拥有。
首 slice 只交付正式验收用候选代码与合同，已完成的本地隔离验证不证明远端同源验收。
expected-current promotion 只能在独立完整 committed Branch Review 后接受本候选；
promotion-created diff 必须再经 fresh Phase 2、Task Commit 与独立完整 Branch Review。
同一远端 Guru HEAD 的 source_locked/provider 与 MIG-495-06 代表性旧在途证据
仍须最终完成；缺失时不得合并或宣称 #495 完成。软件发布、真实业务仓升级及完整
多平台 Release matrix 保持各自独立边界。历史 ADR、版本与已发布 tag 不追溯改写。
