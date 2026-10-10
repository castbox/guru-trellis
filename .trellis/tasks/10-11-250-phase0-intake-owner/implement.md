# #250 实施与验证计划

## 执行前置

任务保持 planning，本阶段产物为三份文档与 Phase 1 门禁结果。实现须在 approved plan 展示后的明确回复之后，由现有 guru-activate-task 执行。每次 task/source write 前执行 check-task-checkout-boundary；所有新 commit/push/PR/merge/cleanup 单独展示精确副作用并取得确认。授权不写文件。

实施前 fresh 读取 #250 r19、live main、canonical/installed interfaces、RDT/Architecture、软件声明与 target Trellis。出现真实 base drift 调原 reconcile owner，不凭旧 planning SHA继续。目标只为本 task delivery 到 castbox/guru-trellis main；#292/#521 不实施。

## 分解与文件责任

1. **Profile 与迁移合同**：修改 trellis/skills/guru-team/packages/guru-clarify-requirements 的 SKILL/reference/interface/schemas/examples/runtime/tests；定义 standard/reviewed 独立输入、保留其余四 profile、source selection 与 caller-aware context return。旧 initial profile 及失去 consumer 的资产直接退役，迁移说明列出旧/新入口与 re-entry。脚本不判断语义。
2. **Discovery/Sync 与 downstream projections**：修改 guru-discover-change-context 的 initial/context_request public contracts、record/check/invoke 和 tests；Sync 仅更新受影响 consumer declaration；同步 stage0 consumers/transitions/invocation schemas、Wording/readiness 的必要薄 projection 与 runtime authoring adapter。每类 context_ready fresh 重建对应合法 input，不共享 private owner result。
3. **全局编排与 actual entry**：更新 trellis/workflows/guru-team/workflow.md 的 mandatory profiles、router return 和 continuation 约束，以及 Clarify package 的声明平台投影。current overlays 只有 Guru finish-work；start/continue 属 upstream 并已加载当前 workflow，因此通过 workflow/Clarify 合同覆盖 start/prompt/continue/resume/compression，不发明或 patch 上游入口。现有 Guru-owned overlay 仅在其真实 consumer 受影响时同步。保留 upstream trellis-brainstorm/trellis-*，不修改其源、全局 CLI、hooks 或清空发现清单。unknown exit stop；无变化 active resume 按 current phase。
4. **来源/现有 Planning 接缝**：current task-created consumer 解析 live TaskId/generation/binding/checkout 后消费最小来源定位并 fresh 读来源，最终处置在 design.md；不依赖 #292，不写第二 matrix、task.json 新来源模型或持久 handoff。完整 source stale/mutation、Wording content_changed、readiness revision 返回最早 owner。
5. **文档与贡献**：执行 design.md 的 Docs SSOT Plan，建立 task-isolated RDT contribution，必要 Architecture contribution/ADR 由其原 owner；维护 README/spec 的 current入口/迁移而非重复 step-local prose。shared promotion 只在符合现有 independent review 条件后执行，晋升差异重新进入 gates。
6. **受管同步**：canonical change 后运行 preset apply.sh --repo . 与 check-dogfood-overlay-drift.sh。检查 managed inventories、exec mode、各平台 projection、Trellis update 所属与 sidecars；仅处理本任务产生且已确认范围内的改动，不覆盖并行工作。

## 定向验证

| 验证组 | 真实入口与观察 | 检出的缺陷 |
| --- | --- | --- |
| V250-A Profile/return | current package formal invoke + consumer projection；六 Clarify profiles，四 context_request 回程、普通 stale/block/source refresh，scope producers 的 exact route | profile 丢失、错 consumer、合法 input 不可重建、blocked 假 clear |
| V250-B Qualification | 正常候选分别经 normal/solution recorder/check/invoke 产生实际 scope_confirmation_required，进入其合法 Clarify profile，再回原 owner | qualifier 混用、复制例子冒充实际退出 |
| V250-C Source/Planning | native 清晰技术 Issue含规范性接口/机制/顺序/兼容与候选建议；当前 planning owner fresh 读源并在 design 明确承接；no_issue/create/reuse/reference_only 和 mutation return | 来源承诺丢失、建议升级、Issue intent 被当关闭权限、#292 隐式依赖 |
| V250-D Prompt/resume | 真实 codex exec 的正常“讨论需求/设计新功能/先做规划”，zero/one/partial、repo-answerable；brainstorm 未选/自动选/方法复用；实际压缩恢复或真实 continuation；无变化 active、批准重规划 #468 回程 | 自动匹配另起 owner、重复访谈、额外确认、身份重置 |
| V250-E Distribution | source/installed validation，current dogfood parity、各声明 descriptor bytes/modes、apply/reapply/drift、.new/.bak、retired current API/asset 退出 | canonical/installed 不一致、旧入口复活、update/reapply 丢失 |
| V250-F representative install | 最多一个 clean throwaway，正确锁定 target Trellis + 同源 workflow/preset；在该环境 new install 与现有状态 update/reapply 后重复受影响 native entry | 源文件可测但新/已有安装 dispatch 无效 |

先从现有 scripts/tests/eval adapter 取得当前支持命令，再按受影响最小可靠集运行；不发明命令或拿 global 0.6.17 CLI 代替项目声明 target。正式 Agent 采用现有 formal_exit_boundary/native adapter，保留去敏原始输出作为证据，不把 Python 输出/固定关键字当语义评分。缺环境、真实上下游依赖或实际压缩能力时明确 SKIP/blocked 和受影响验收，不改成 pass，不通过复制 snapshot 模拟 live。

测试不比较常量与自身，不锁可变版本/数量，不为 hostile forgery、锁/TOCTOU/stress/fault injection 新增负例。每项证明对应行为，合并重复案例；package/unit/mock 证据明确层级。创建 Issue/task 与 Issue body/comment/reopen 外部 mutation 的真实验证须独立精确计划与确认，未获该动作确认则不执行，保留层级限制。

## 门禁与交付顺序

Phase 1：planning Wording → 独立 Architecture task_impact_sync(stage=planning) → normal/solution/root qualification → genuine guru-approve-task-plan → 链接展示与 plan pause。Architecture或 qualification 的 revision/clarify/blocked 按唯一 consumer 自动重入，不制造形式确认。

计划 accepted 后：pair guard/reconcile → Activate → 当前实施 owner → fresh independent Architecture Phase 2 + complete guru-check-task → reviewed task commit → fresh independent full origin/main...HEAD Architecture/Branch Review → task Delivery Review/readiness → separately confirmed Publish/Merge → Completion → separately authorized exact Closure → Finish →原 Cleanup disposition。任一 finding 修复只在 qualified current scope，修复后 fresh 对应 gates；不能重复用之前 pass。

Docs contribution/promotion 遵从原 owner，晋升 diff 回 fresh Phase2/TaskCommit/完整独立 Branch Review，不能直接发布。关键结论优先当前对话/最小 DTO 或 ignored private checkpoint，成功消费后删除，不写 tracked gate 证明。

## 终态与限制

Task whole-scope 完成须 #250 CLOSED/COMPLETED、所有 satisfying PR MERGED 且 heads reachable live main、genuine Check/完整独立 Branch Review/readiness/Completion/Closure/Finish/Cleanup typed results。当前 caller-owned branch/worktree 不被当 Guru 自动删除资源，原 Cleanup 说明 nonblocking retention/manual-only disposition。main 同步、清理、软件 tag/Release 与部署均不得被普通 implementation consent 覆盖。

最终报告列出真正变更、验证入口/层级和未验证项；普通 Issue targeted/new-existing-reapply proof 不称完整多平台 upgrade/Release gate。不得从 package tests、Issue body、规划或 PR merged 推断整体终态。
