# D1：提前 Draft 与独立最终门禁

## 1. 整体来源与术语

整体 authority 为 [Task PRD](../../prd.md)，公共 accepted_scope 的 revision 为 `sha256:dfca6518e73774e45a6079f7f9ebb9ca1e605626a8e8068b20a63ead042bba42`。本批 DeliveryKey 的 delivery_id 为 `b8023126-4ef9-4de1-bce3-f3ed6fc4346f`，generation=0，planning_root=`deliveries/b8023126-4ef9-4de1-bce3-f3ed6fc4346f`。

Direct Source [#636](https://github.com/castbox/guru-trellis/issues/636) 的行为1..7、候选阶段边界、全部验收与非目标均为要求；Backend #649/PR #693 为历史证据。来源无评论，updatedAt=`2026-10-19T17:14:36Z`。已读取完整来源，不将其历史总耗时视为单项优化证据。Draft、Ready、Task、Delivery 的含义沿整体 PRD §1，PR 状态不证明 gate 或整体完成。

## 2. 整体与本批目标、非目标

当前 Check→提交→完整 Review→readiness→Publication 顺序延后远端反馈。本批独立交付完整 #636：公共 owner 承接有界早期提交、Draft 创建/更新、Ready→Draft→Ready、原操作恢复、固定候选审核与验证合同，以及受管分发与迁移。覆盖整体 R636-01..07、AC636-01..10，策略为全量 D1。

不启动 #637/#638，不依赖其未来接口。不改 Backend 现场、业务 CI/CI/CD、权限或部署，不引入队列、自动批准或自动合并，不做完整多平台 Release 矩阵或额外 tag/Release。不增加攻击、伪造、竞态压力、锁或非常规 crash 机制。

## 3. 本批起点、前序结果、依赖与剩余责任

本批为首次 Delivery，尚无前序交付。当前 public phase 是 planning，不表示批准。开发基线为 `b470580d4f79f61c66d72db97861fe1564b5e746`；PR target 为 `castbox/guru-trellis:main`。固定内容基线、实际候选 HEAD 和 PR target 分开，沿 #567 原能力。

输入为已接受整体 PRD、当前 workflow、公共同步 owner 及 RDT/Architecture authority。本批完成后没有预先保留的 #636 实现切片；仍须整体 Completion 核对全部要求和真实证据，再 Closure/Finish/适用 Cleanup。缺少业务 CI 入口由业务 owner 补齐；本仓提供受支持 HEAD 调用/身份合同并如实保留业务组合验证缺口，不伪称通过。

## 4. 本批调用方、场景与流程

| 场景 | 前置/触发与调用方 | 行为及可观察结果 |
| --- | --- | --- |
| S636-01 | implementation owner 形成可审查内容，尚无完整 Check/重型结果 | 原 TaskCommit 有界内容/敏感检查、精确 stage 和真实 commit；原 Publication 创建 Draft，正文列待完成项 |
| S636-02 | 同 Draft 的修正或实际冲突解决形成新候选，最终审核未完成 | 原提交/发布 owner 更新同 PR；保持 Draft、Task/Delivery/PR 身份，不造空提交 |
| S636-03 | 已 Ready 的 PR 要先发布未审修订 | Publication 先退回 Draft，再更新候选；适用检查/审核完成后再 Ready，旧 readiness 不放行新 HEAD |
| S636-04 | 远端动作已成功，正式输出或本地结果丢失 | 原 owner 回读实际 Draft/Ready/HEAD 恢复同次操作；不重复创建、推送或空提交 |
| S636-05 | Draft 已创建，同一固定候选需审核与验证 | 独立审核和风险匹配验证并行；固定 base/head 审核不因目标前进中断 |
| S636-06 | PR 冲突、无 merge ref 或 pull_request CI 未启动 | 分支内容审核和受支持 HEAD 检查继续；组合候选验证保留具体待完成条件 |
| S636-07 | 当前证据完整，准备最终 Ready/Merge | 原 Publication 重新判断实际关闭意图；完整质量与独立最终审核保持；合并后整体 Completion/Closure/Finish |

失败、SKIP、HEAD 变化和状态变化分别由原 producer 判断及恢复，不能由 phase、Draft 存在或旧通过替代。

## 5. 完整行为、条件与约束

**R636-01**：实现形成可审查改动、完成最小自检并检查敏感内容后，支持创建同一 Delivery 的 Draft PR。最小自检的具体命令由 Planning 按风险确定；完整 Branch Review、Mongo/Redis 集成、race 和全部编译结果不作为创建 Draft 的统一前置。
**R636-02**：Draft 创建后，独立审核与风险匹配验证并行推进。正文准确列出已执行、失败、未执行和待完成项；未完成证据不得写为通过。
**R636-03**：冲突解决或问题修正形成候选后，支持在最终审核前提交并推送到同一 Draft PR。为这种提交明确有界的 AI 内容检查、精确 staging、敏感内容检查和目标核验；不得继续把完整 task Check、全部重型验证或最终 Branch Review 作为所有 Draft 提交的前置，否则早期入口仍会闭锁。最终交付的完整质量义务保持，迁移必须经公共提交/发布 owner，不能旁路调用 Git。
**R636-04**：显式分离 Draft 创建/更新与 Ready 转换、最终合并。Ready 和 Merge 消费精确当前候选及所需审核、验证；旧 HEAD 的通过不直接放行新候选。已 Ready 的同一 PR 若需要先发布尚未完成最终审核的新候选，由原 Publication owner 支持退回 Draft，再沿早期更新入口接续；保留 Task、Delivery 和 PR 身份，失效的 readiness 不得继续用于合并。若此前输出丢失，先读回实际 Draft/Ready 状态与 HEAD，再恢复同次操作。
**R636-05**：PR 处于冲突状态不阻止分支内容审核和 HEAD 验证；需要整合候选才能完成的检查保留具体待完成条件。现有 CI 不触发时如实说明，不以 Draft 存在证明远端验证已执行。
**R636-06**：复用同一 Task、Delivery 和 PR；支持中断恢复及已创建 Draft 的读回，不创建重复 PR，不制造空提交。早期 Draft 在关闭范围尚未通过最终 Publication 判断时只引用来源 Issue，不生成关闭指令（包括 `Closes`/`Fixes`/`Resolves`；完整禁用集合见原 Publication 合同）。最终正文由原 Publication owner 按实际交付范围和目标分支重新判断；部分 Delivery、reference-only 和非默认分支交付不得冒充完整关闭。Draft、Ready 和一次 PR 合并均不代表整体 Task 已完成。
**R636-07**：明确现有在途任务、公共 I/O、阶段状态及 producer/consumer 的迁移；同步 canonical、workflow、平台投影和 dogfood。不得通过旁路 gh 调用绕过公共 owner。

创建 Draft、首次内容审核、候选验证、Ready 转换和实际合并分别拥有明确结果。首次审核固定 base/head；进行中的审核不因 dev 前进中断。PR 分支 HEAD 的测试与目标分支组合候选的测试分别标识，不能相互冒充。重型测试在 Draft 创建后开始，不统一推迟到排队占位之后。

Draft 创建/更新后支持分支 HEAD 的验证；有文本冲突、GitHub 未产生 PR merge ref 或实际 pull_request CI 未启动时，仍能从受支持入口运行该 HEAD 的命中检查。本项只定义调用与候选身份合同，不要求在 Guru 内实现 Backend CI。具体业务 CI 入口若缺失，由业务 owner 补齐；正文必须报告哪些验证未发生。

本项不要求出现无实际集成需要的同步提交。早期 Draft 仅提供反馈，不触发自动 Ready、自动合并或额外 Delivery。故障恢复覆盖“远端 Draft 已创建但本地正式输出未收录”及“远端已更新但本地结果丢失”。

本批 design 第3节是来源设计承诺处置的唯一位置。Markdown 控制 AI 判断与流程；脚本只执行/校验事实。不新增重复状态机或跨阶段 qualification 缓存；I/O 变更以显式同步迁移承接在途记录。既有正常输入、提交恢复、完整审核、发布恢复、合并和收尾能力保持。

## 6. 本批验收、验证方式与未决项

- [ ] **AC636-01**：从标准入口在首次完整审核及重型验证之前创建真实 Draft PR；其正文准确说明待完成内容。
- [ ] **AC636-02**：在尚无完整 task Check/重型测试结果的候选上，经有界提交检查形成真实提交并推送 Draft；完整交付门禁仍阻止其直接 Ready 或 Merge。
- [ ] **AC636-03**：同一 Draft 在候选变化、实际冲突解决后更新；最终审核未完成时不误标 Ready 或合并。
- [ ] **AC636-04**：已 Ready 的 PR 在发布未审修订前退回 Draft，完成适用审核后再 Ready；状态转换输出丢失时读回原 PR 恢复，旧 readiness 不放行新 HEAD。
- [ ] **AC636-05**：对固定候选并行执行独立审核和风险匹配验证，两个结果都由最终门禁正确消费。
- [ ] **AC636-06**：失败、SKIP、HEAD 变化、Draft 创建输出丢失分别沿原 owner 恢复，不重复创建或假称通过。
- [ ] **AC636-07**：审核期间目标前进、有冲突导致无 PR merge ref 时，固定分支内容审核和受支持 HEAD 检查仍能推进；组合验证的缺口如实保留。
- [ ] **AC636-08**：早期 Draft 正文只引用尚未判定关闭的来源；最终正文按完整/部分交付及默认/非默认目标执行原 Issue 关闭语义，不能由 Draft 自动继承关闭结论。
- [ ] **AC636-09**：合并前全部适用证据覆盖实际候选；标准交付与收尾保持。
- [ ] **AC636-10**：package/runtime、声明平台投影、dogfood/reapply/drift 与 sidecar 检查通过；不扩张为完整多平台 Release 矩阵。

AC01/02 使用标准公共提交/发布入口证明真实早期 Draft；AC03/04 使用同 PR 实际候选更新和状态转换；AC05/07 观察固定内容审核/分支 HEAD 检查与组合验证区分；AC06 覆盖原操作输出丢失、失败与 SKIP；AC08 覆盖默认/非默认、full/partial/reference-only；AC09 完整质量及收尾；AC10 定向 package/runtime、matching installed、声明平台、dogfood/reapply/drift 和逐项 sidecar。每项保留实际结果和未验证边界，不预填通过。

本阶段没有必要补问的产品选择。实现机制与精确命令由候选 Architecture 后的 solution planning 决定；真实 GitHub 行为验证需原 owner 的独立副作用计划。组合验证缺口如实保留，不以 #637/#638 未实施降低本批标准。

## 7. Canonical 引用与本轮差额

- `docs/requirements/current/task-delivery-lifecycle.md`（RDT `current-main-0.7.0-guru.112`）：身份、Planning、固定内容、Check/Commit/Review、Publication 与整体完成。差额为早期反馈入口及其迁移；完整质量和 Refs-only/Closure 分工保持。
- `docs/design/current/task-delivery-lifecycle.md`：D531 的官方公共模型与 Guru owner 分工、固定候选、恢复职责；差额由原提交/发布 owner 和 consumer 原位迁移。
- `docs/test/current/task-delivery-lifecycle.md`：T531/T530/T600/T557 和 BEH567 固定候选；新增本批早期提交、状态转换、输出丢失与候选区分场景。
- `docs/architecture/README.md`（`current-main-0.7.0-guru.103`）、`docs/architecture/00-foundation/design-constitution.md`：实际 Architecture 适用性由独立 owner 判断；本阶段不预填影响结论，不写共享 authority。
- `trellis/workflows/guru-team/workflow.md` 与 canonical `guru-create-task-commit`、`guru-publish-task-delivery`、`guru-check-task`、`guru-review-branch`、`guru-review-task-delivery`、`guru-merge-task-delivery`：精确公共合同由 package 独占，workflow 只编排。受管 projection 由 preset 同步。
- `.trellis/spec/workflow/subtraction-first-compatibility.md`：直接演进和原位复用优先，当前受控 consumer 同步，不保留无期限双路径。
