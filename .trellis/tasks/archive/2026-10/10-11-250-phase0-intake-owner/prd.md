# #250 Phase 0 唯一 Intake semantic owner

## Authority 与边界

Direct Source：[castbox/guru-trellis #250](https://github.com/castbox/guru-trellis/issues/250)，唯一 current contract 为 body `2026-10-10-r19`。历史 comments 未被选为 authority。实施、重入及发布前 fresh 读取该来源、live main、canonical workflow/registry/interface、RDT/Architecture 和实际 installed contract。本文是任务范围，不是产品 SSOT。

本任务只交付 #250；串行顺序的 #453/#396 为既有基线，#292/#521 为独立后续。本任务不编写 Phase 1 Author Skill，不恢复 #249 依赖，不重建 Delivery/Completion、TaskId/generation/checkout 或 #468 活动重规划恢复。

## 目标

Clarify 独占 Phase 0 需求澄清、来源识别、Intake 收敛与真实选择判断。技术 Issue 中明确约定的接口、机制、顺序、兼容性及既有审阅决定被识别并传给当前 Planning；候选建议保持候选性质。Sync 拥有 base，Discovery 拥有证据收集与覆盖充分性，创建和下游阶段保持现有 owner。

## Accepted scope

| ID | 必需行为 |
| --- | --- |
| P250-01 | standard、reviewed-plan、standalone、active-task 入口由 Clarify 收敛；no_issue/create/reuse/reference_only 保持现有 source/Issue intent，Intake 不授予关闭权限。 |
| P250-02 | 先读取 repo-answerable evidence；无真实选择时零问题；每轮最多一个最高价值问题并给证据、选择、推荐与 trade-off；partial answer 保留必需未决项，不假装 clear。 |
| P250-03 | standard/reviewed/standalone/active 缺上下文时请求 Discovery，携带最小 return profile/identity；每次回程 fresh 重建合法 input；source/base 变化回 Sync/refresh/retarget。 |
| P250-04 | normal_scenario_scope_confirmation 与 solution_mechanism_scope_confirmation 分别消费真实 qualifier 的最小输出，询问精确 authority choice 并返回各自原 owner；不替换或重新解释资格结论。 |
| P250-05 | 识别 load-bearing 来源定位、规范性设计承诺、建议及冲突。保留不可重新推导的语义选择；最终 retain/change/reject 和落点只在 Planning design.md。 |
| P250-06 | 保留 Wording/readiness 的完整当前语义，content_changed 回最早受影响 owner；Create Issue/Create Task 独占 mutation；created 仍经 guru-task-created 进入当前 Phase 1，无未来 #292 前置。 |
| P250-07 | 枚举所有 current scope-change producers，仅使依赖变化的判断失效；Direct Source/必要 Related Work、session/checkout、compression/resume、#468 resume_execution 保持同一身份合同。 |
| P250-08 | 正常“讨论需求”“设计新功能”“先做规划”以及 start/prompt/continue/resume/compression 遵循 Guru owner；brainstorm 未选中、自动匹配及方法复用均合法，但不能重复访谈、另起规划或绕过门禁。 |
| P250-09 | canonical/dogfood/installed、registry/interface、README/spec、声明平台投影与 new/existing/reapply/drift 定向验证；公共 API 迁移和旧竞争路线退役可审查。 |

## 验收场景与证据层

以下为 Planning 的候选场景集；进入实现/测试前由现有 qualification owners 准入，不以测试数量代替充分性。

| 场景 | 正常触发与观察 | 层级 |
| --- | --- | --- |
| S250-01 | 清晰技术 Issue 同时包含目标、设计与候选建议；实际 native Agent 直接进入正确 owner、零问题，并由当前 Planning 显式承接规范性条款。 | Agent / source-to-planning |
| S250-02 | repo 可回答的问题先读取证据；未决选择仅问一个；只答部分时不产生 clear。 | Agent semantic |
| S250-03 | 四类 context request 各自回到原 profile，重复回程/普通 stale 仍重建合法 input，标准路径同样覆盖。 | 正式 wrapper / Agent |
| S250-04 | 两种 qualifier 实际产生 scope_confirmation_required，分别进入合法 confirmation profile 并返回原 owner。 | 正式 qualification chain |
| S250-05 | no_issue、create、reuse、reference_only 与新任务/active 分类可达；Wording 修改、readiness 修订、source mutation/live reread 与 blocked 均保持原 consumer。 | wrapper / bounded fixtures |
| S250-06 | 当前 Planning/Approval、Architecture、Check、Branch Review、Delivery、Completion、task-free 的受影响回程保持身份；无变化 active resume 不重做 Intake，批准重规划经 #468 resume_execution。 | caller graph / native resume |
| S250-07 | source conflict/Direct Source revision/必要 Related Work 按 authority 与依赖范围返回正确 owner；未相关事实不被 blanket 作废。 | Agent / current recovery |
| S250-08 | 正常 prompt + brainstorm 三种加载条件、新装和已有安装更新/reapply 后实际 dispatch 合法；压缩恢复不重置身份或增加形式确认。 | native Agent / installed |
| S250-09 | canonical source validation、选定平台 bytes/exec mode、apply/reapply、drift/sidecar 与 retired API rejection 可证明实际投影。 | package / distribution |

native 证据必须是真实 Agent 输出和实际 invoke stdout；模拟 Agent、关键词扫描和 fixture pass 只证明各自层级。新装最多一个代表性 clean throwaway；已有安装 update/reapply 使用同一代表性环境的前后状态，不承担完整多平台矩阵。

## Non-goals 与风险

不修改/delete upstream trellis-*、hooks 或全局/npm/node_modules，不清空 Skill 发现清单，不新增通用排除机制、wrapper Skill、ledger、tracked handoff、shared cache、task_context、路径映射或授权记录。不覆盖 hostile forgery、锁/TOCTOU/stress/fault injection。完整 Release/upgrade 矩阵、额外业务仓安装、部署与软件发布均由专门 owner 负责。

风险集中于 profile/return migration 遗漏、来源选择丢失、语义自动匹配另起 owner 和 current source drift；由明确 consumer 图、真实 Agent 与 focused installed 验证覆盖。入口实际缺失或 unknown/multiple exit fail closed，不能以规划承诺冒充依赖已交付。

## Delivery 与完成

计划一个完整 Delivery slice，包含 P250-01..09、当前 Planning 薄承接和定向证据，无隐藏剩余本 task 工作；#292/#521 保持独立范围。slice 独立交付条件是当前链路无需未来 Author 即可运行、受支持回程完整、无 open finding、公共迁移及分发验证完成。合并不等同整体完成；后续真实 Check、完整独立 Branch Review、readiness、Delivery/Merge、Completion/Closure/Finish/Cleanup 分别执行。caller-owned branch/worktree 的保留或 manual-only disposition 由原 Cleanup owner 说明。
