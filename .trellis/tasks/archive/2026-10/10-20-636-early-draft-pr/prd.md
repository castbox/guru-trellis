# #636 提前创建和更新 Draft PR：整体需求

## 1. 来源与术语

| 来源 | 角色与条款 | 本 Task 用途 |
| --- | --- | --- |
| [castbox/guru-trellis #636](https://github.com/castbox/guru-trellis/issues/636)，本轮读取 updatedAt=`2026-10-19T17:14:36Z`，无评论 | Direct Source，exact_source；全部行为、阶段边界、验收和非目标是要求 | 整体 accepted scope |
| 当前用户请求 | 仅实现并关闭 #636；独立 project worktree 从默认 main 开始；完整 workflow；实现和 Check 使用独立子 Agent | 执行范围与独立审核责任 |
| [#567 已归档 PRD](../archive/2026-10/10-15-567-fixed-development-baseline/prd.md) | 已交付的固定候选和实际阻塞触发约束 | 保留原子能力，不恢复持续追赶目标 |
| Issue 所述 Backend PR #693 | 历史证据，非执行授权或优化通过证据 | 说明背景，不操作业务仓现场 |

Draft 是同一 Delivery 的开发反馈入口。Ready 是当前候选满足适用交付条件后的 PR 状态。Task 表示整体范围责任；Delivery 表示一个交付切片。创建、Ready 和一次合并不证明整体 Completion。

## 2. 背景与问题

当前标准流程先完成 Check、提交、完整 Branch Review 和 Delivery Review，再创建或更新 PR。远端反馈被推迟；冲突解决已经形成候选时，也会等待正式审核后才推送，GitHub 在此期间仍显示旧 HEAD 的冲突。

本 Issue 将 Draft PR 作为开发与验证入口，提前获得远端反馈；PR 创建不代表审核通过、Ready、Delivery 已交付或 Task 已完成。

以下是来源记录的历史证据：

- 正常案例：castbox/ai-chat-roleplay-backend#649 的 PR https://github.com/castbox/ai-chat-roleplay-backend/pull/693 。2026-10-19 19:54 创建 PR；此前已执行完整审核。第四轮整合在本地形成后，仍等待审核至 23:16 才更新远端。时间为北京时间，属于历史快照。
- 本地原始会话标识：01a14836-133c-7f32-8f1c-111efb98c9b3。该会话是证据来源，不是执行授权或未来固定状态。
- 当前入口：trellis/workflows/guru-team/workflow.md；guru-check-task、guru-create-task-commit、guru-review-branch、guru-review-task-delivery、guru-publish-task-delivery、guru-merge-task-delivery 的 canonical package。
- 复用 #567 的固定候选和实际阻塞触发原则，不恢复持续追赶 base。

补充终态证据：PR #693 已于 2026-10-19 23:28:58（北京时间）合入 dev，合并提交为 `08d84b0053271d15f9ffa69358e4c83aa6de7835`，最终 PR HEAD 为 `8e13d0deb08b26096289d50eeeccaaf2ead03a97`。从创建至合并约 3 小时 34 分钟；其间存在真实缺陷修正、整合验证、审核与 CI，不能将总时长全部归因于无效流程。该案例证明反复整合与串行成本，不证明任何单项优化已通过。

本轮仓库核对：公共 TaskCommit 当前提交 profile 绑定 `check_result_id`；Publication 当前事务消费 readiness 后标 Ready。实现位置为 `trellis/skills/guru-team/packages/guru-create-task-commit/`、`guru-publish-task-delivery/` 及 `trellis/workflows/guru-team/workflow.md`。

## 3. 目标与非目标

完整承担第5节 R636-01..07、第6节候选边界和第7节 AC636-01..10；Task Completion 负责核对全部要求，单次 Delivery 合并不替代整体完成。

本项独立交付 PR 生命周期时机调整。跨阶段审核复用由 #637 承担，共享文档晋升由 #638 承担，Actions 合入队列由 castbox/ai-chat-roleplay-backend#702 承担；本项不以这些未来接口或队列存在为前置。不提前实现后项，不修改业务奖励逻辑、业务 CI、CI/CD、仓库权限或部署，不引入自动批准或自动合并。不扩为完整多平台 Release 矩阵，不要求额外 tag/Release。不增加攻击/伪造、锁、竞态压力或非常规 crash 测试。

## 4. 真实调用方、场景与流程

| 场景 | 调用方、前置与触发 | 行为和可观察结果 |
| --- | --- | --- |
| S636-01 早期反馈 | implementation owner 形成可审查内容，尚无完整 Check/重型结果 | 原提交 owner 有界检查和真实提交，原 Publication 创建 Draft，正文列待完成项 |
| S636-02 修正更新 | 同 Delivery 已有 Draft，修正或实际冲突解决形成新候选 | 原提交/发布 owner 更新同 PR；最终审核未完成时保持 Draft |
| S636-03 Ready 后修订 | 同 PR 已 Ready，需先发布尚未最终审核的新候选 | 原 Publication 先退回 Draft，再早期更新；适用审核完成后再 Ready，旧 readiness 不放行新 HEAD |
| S636-04 中断恢复 | 远端创建、更新或状态转换已成功，但正式输出丢失 | 原 producer 回读实际状态/HEAD，恢复同操作，不重复 PR、空提交或已成功副作用 |
| S636-05 并行审核验证 | Draft 已创建，同一固定候选待审 | 独立审核与风险匹配验证并行；目标前进不中断内容审核，最终门禁分别消费结果 |
| S636-06 冲突和无 merge ref | 存在文本冲突、无 PR merge ref 或 pull_request CI 未触发 | 固定内容审核及受支持 HEAD 检查仍推进；组合验证保留具体缺口 |
| S636-07 最终交付收尾 | 准备 Ready/Merge，适用证据覆盖实际候选 | 原 Publication 判断实际关闭语义；完整 Check、独立 Branch Review/readiness/Merge、整体 Completion/Closure/Finish 与适用 Cleanup 保持 |

## 5. 行为要求

下列保留 Direct Source 的全部七项承诺，稳定编号按原顺序为 R636-01..07。分别对应 S636-01、S636-05、S636-02、S636-03/04、S636-06、S636-04/07、全部场景；不是预填通过结论。

1. 实现形成可审查改动、完成最小自检并检查敏感内容后，支持创建同一 Delivery 的 Draft PR。最小自检的具体命令由 Planning 按风险确定；完整 Branch Review、Mongo/Redis 集成、race 和全部编译结果不作为创建 Draft 的统一前置。
2. Draft 创建后，独立审核与风险匹配验证并行推进。正文准确列出已执行、失败、未执行和待完成项；未完成证据不得写为通过。
3. 冲突解决或问题修正形成候选后，支持在最终审核前提交并推送到同一 Draft PR。为这种提交明确有界的 AI 内容检查、精确 staging、敏感内容检查和目标核验；不得继续把完整 task Check、全部重型验证或最终 Branch Review 作为所有 Draft 提交的前置，否则早期入口仍会闭锁。最终交付的完整质量义务保持，迁移必须经公共提交/发布 owner，不能旁路调用 Git。
4. 显式分离 Draft 创建/更新与 Ready 转换、最终合并。Ready 和 Merge 消费精确当前候选及所需审核、验证；旧 HEAD 的通过不直接放行新候选。已 Ready 的同一 PR 若需要先发布尚未完成最终审核的新候选，由原 Publication owner 支持退回 Draft，再沿早期更新入口接续；保留 Task、Delivery 和 PR 身份，失效的 readiness 不得继续用于合并。若此前输出丢失，先读回实际 Draft/Ready 状态与 HEAD，再恢复同次操作。
5. PR 处于冲突状态不阻止分支内容审核和 HEAD 验证；需要整合候选才能完成的检查保留具体待完成条件。现有 CI 不触发时如实说明，不以 Draft 存在证明远端验证已执行。
6. 复用同一 Task、Delivery 和 PR；支持中断恢复及已创建 Draft 的读回，不创建重复 PR，不制造空提交。早期 Draft 在关闭范围尚未通过最终 Publication 判断时只引用来源 Issue，不生成 `Closes`/`Fixes`/`Resolves` 等关闭指令。最终正文由原 Publication owner 按实际交付范围和目标分支重新判断；部分 Delivery、reference-only 和非默认分支交付不得冒充完整关闭。Draft、Ready 和一次 PR 合并均不代表整体 Task 已完成。
7. 明确现有在途任务、公共 I/O、阶段状态及 producer/consumer 的迁移；同步 canonical、workflow、平台投影和 dogfood。不得通过旁路 gh 调用绕过公共 owner。

## 6. 约束与依赖

创建 Draft、首次内容审核、候选验证、Ready 转换和实际合并分别拥有明确结果。首次审核固定 base/head；进行中的审核不因 dev 前进中断。PR 分支 HEAD 的测试与目标分支组合候选的测试分别标识，不能相互冒充。重型测试放在 Draft 创建后，不等于一律等到排队占位后才开始。

Draft 创建/更新后支持分支 HEAD 的验证；有文本冲突、GitHub 未产生 PR merge ref 或实际 pull_request CI 未启动时，仍能从受支持入口运行该 HEAD 的命中检查。本项只定义调用与候选身份合同，不要求在 Guru 内实现 Backend CI。具体业务 CI 入口若缺失，由业务 owner 补齐；正文必须报告哪些验证未发生。

本项不要求出现无实际集成需要的同步提交。早期 Draft 仅提供反馈，不触发自动 Ready、自动合并或额外 Delivery。故障恢复覆盖“远端 Draft 已创建但本地正式输出未收录”及“远端已更新但本地结果丢失”。

Markdown workflow/Skill 定义 AI 判断、范围和路由；脚本仅执行事实、校验和最小记录。沿原 TaskCommit、Publication、Check、Branch Review、readiness、Merge、Completion/Closure/Finish/Cleanup owner 迁移，不另建协调器或旁路。公共接口演进给出在途迁移合同，不以机械加字段制造新 pass。

开发起点 `main@b470580d4f79f61c66d72db97861fe1564b5e746`，PR target 为 `castbox/guru-trellis:main`；开发基线、固定内容候选和 PR 目标分别承接。#567 的正常目标前进不触发追赶义务，真实整合沿现有原子能力处理。caller-owned 与链外资源保留。

## 7. 可观察验收与验证方式

以下依来源顺序编号 AC636-01..10，尚未执行，不代表通过。AC01/02 经公共有界提交和 Publication 证明真实早期入口；AC03/04 验证同 PR 候选与状态转换；AC05/07 区分固定内容审核、HEAD 验证和组合验证；AC06 验证原 owner 恢复；AC08 保留关闭语义；AC09 验证最终交付收尾；AC10 验证受管分发与安装。

- [ ] 从标准入口在首次完整审核及重型验证之前创建真实 Draft PR；其正文准确说明待完成内容。
- [ ] 在尚无完整 task Check/重型测试结果的候选上，经有界提交检查形成真实提交并推送 Draft；完整交付门禁仍阻止其直接 Ready 或 Merge。
- [ ] 同一 Draft 在候选变化、实际冲突解决后更新；最终审核未完成时不误标 Ready 或合并。
- [ ] 已 Ready 的 PR 在发布未审修订前退回 Draft，完成适用审核后再 Ready；状态转换输出丢失时读回原 PR 恢复，旧 readiness 不放行新 HEAD。
- [ ] 对固定候选并行执行独立审核和风险匹配验证，两个结果都由最终门禁正确消费。
- [ ] 失败、SKIP、HEAD 变化、Draft 创建输出丢失分别沿原 owner 恢复，不重复创建或假称通过。
- [ ] 审核期间目标前进、有冲突导致无 PR merge ref 时，固定分支内容审核和受支持 HEAD 检查仍能推进；组合验证的缺口如实保留。
- [ ] 早期 Draft 正文只引用尚未判定关闭的来源；最终正文按完整/部分交付及默认/非默认目标执行原 Issue 关闭语义，不能由 Draft 自动继承关闭结论。
- [ ] 合并前全部适用证据覆盖实际候选；标准交付与收尾保持。
- [ ] package/runtime、声明平台投影、dogfood/reapply/drift 与 sidecar 检查通过；不扩张为完整多平台 Release 矩阵。

## 8. 实际未决项

当前整体需求没有必要补问的产品选择。公共 profile、最小 DTO、阶段衔接及测试实现交 Delivery Author 和独立 Architecture 细化。技术未定不得降低以上验收。真实 GitHub 验收、发布、合并和 Cleanup 分别保留原 owner 的精确计划与当前对话边界。
