# #434 重构 Guru Task Delivery Lifecycle：任务内多次交付，成功后再完成与归档

## Goal

将现有一次性交付并提前归档的 closeout 图，原子切换为唯一的多次业务交付生命周期：

`Active Task -> Delivery cycle 1..N -> Task Completion -> Issue Closure -> Official Finish -> Resource Cleanup`

本任务拥有 #454 Phase E434 六个 planned ID 的完整 canonical package 交付、独立 Issue-creation owner，以及全局 workflow graph、版本绑定、迁移、原子激活和旧边退休。#435 与 #436 已交付的 capability 保留其内部语义 owner；本任务不复制它们的行为。

## Requirement Authority

- GitHub Issue：`castbox/guru-trellis#434`
- 合同版本：`2026-09-18-r4`
- 子能力 Issue：#435、#436、#443
- 2026-09-26 协调基线：`origin/main@bab8cfcd534692735b9240b25dd8bc63e40a5cb4`；Architecture/RDT 当时的 current authority 为 `current-main-0.6.17-guru.66`。切换前 source registry 为 32 active / 149 exits / 102 commands，旧生产图为 22 invokes / 98 exits；这些计数只是历史快照。#434 本地激活候选为 34 active / 155 exits / 104 commands、33 invokes / 153 production exits，installed 与选定平台投影已同步；Architecture/RDT `.66 -> .67` 晋升已经完成。广义测试、本地 clean install、旧/混合图负例和两轮独立只读审核曾在晋升及后续修订前通过，当前候选仍需重新审核及正式 Phase 2、提交后完整 Branch Review，不能称作已验收交付。
- 官方 Trellis 扩展约束：workflow 行为写入 canonical `.trellis/workflow.md`；preset/overlay 分发受控内容，不修改 Trellis 上游源码或全局安装。远端 marketplace 安装不是本任务的使用场景或验收项。

## Functional Requirements

### R1. 唯一生产生命周期

- 业务 Delivery 可在同一个 active task 内顺序发生一次或多次。
- 每次 Delivery merge 只产生一次 Delivery result，不产生 task completion，不归档 task，不关闭 Issue。
- 每次 Delivery PR 必须使用 `Refs`；Completion pass 前不得使用 `Closes`、`Fixes` 或 `Resolves`。
- 最终 Completion 之后，顺序固定为 Closure、Finish、Cleanup。
- Finish bookkeeping PR 是行政收尾，不计入 Delivery history，不产生 Delivery result，不再次触发 Completion。

### R2. 子能力 readiness 与版本绑定

- #435 已通过 PR #437 合入 Delivery Review、Publish、Merge，以及分批交付所需 Planning/Check/Commit/Branch Review 最小适配；三个 package 的 Interface selector 均为 `1.4`，registry 状态为 `active/deferred`，尚未进入 production workflow。
- #436 已提供 Completion、Closure、Finish、Cleanup、Reactivate 和 evidence-refresh 入口，并保持 workflow integration deferred。
- #454 D443 已将 `guru-bind-task-session` canonical major 迁至 TaskId/generation 与 path-free session；五个既有成功 exits 加 `explicit_task_mode` 和 `binding_blocked` stop 是 #434 activation 的 hard prerequisite，#434 只消费其 contract，不复制 binding 逻辑。
- 每个新 package 必须具备 closed Interface、schema/example、consumer declaration、wrapper/runtime、eval/test、Shared/Codex/Claude/Cursor 投影和 installed manifest 条目。
- #434 只能消费已合入当前目标基线、通过 source/installed parity 的精确 package 接口版本；不得按名称猜测或读取 child task 私有状态。

### R2.1 Child capability readiness snapshot

- `guru-review-task-delivery` 已固定 `delivery_review` profile；`ready` 的唯一 Skill consumer 为 `guru-publish-task-delivery`，其余 planning/implementation/scope/block exits 仍回现有 owner 或 stop。
- `guru-publish-task-delivery` 已固定 `review_ready`、`same_plan_resume`、`reprepare_publication` profiles；`ready_for_merge` 的唯一 consumer 为 `guru-merge-task-delivery`。
- `guru-merge-task-delivery` 已固定 `ready_for_merge` profile；`delivered` 的唯一 consumer 为 `guru-review-task-completion`。D436 canonical major 已合入并在本地候选 installed/selector/全局图闭合，最终 gate 尚待验证。
- #435 的 source、installed 与 Shared/Codex/Claude/Cursor projection 已随 PR #437 合入；这些事实只证明 Delivery capability ready，不证明 #434 graph ready。
- 当前顺序为：复核 live interface 与协调基线 -> 组合 source package-ready -> 同一候选切图及安装投影 -> 完成广义回归、代表性安装和迁移负例 -> 独立 review。任一后置验证失败，不发布候选。

### R2.2 #436/#443 readiness snapshot

- #454 D436 的五个 terminal packages 在 PR #474 合入 canonical major；本地候选 selector/installed/platform 已迁移。Closure/Finish/Cleanup 使用 TaskId/generation、ResultRefDTO、ResourceSealRefDTO 及 C5 ledger，不可用历史 `task_ref/closure_ref/resources` fixture 证明新入口。
- #454 D443 的 `guru-bind-task-session` 在 PR #473 合入 canonical major；五个成功出口 `session_resumed`、`session_rebound`、`task_switched`、`reactivate_rebound`、`session_manually_recovered`，`explicit_task_mode` 和 `binding_blocked` stop 均已进入本地候选图和投影。
- #454 C6/C7 创建基座的六个 stable IDs 和独立 `guru-create-issue` 已在本地候选 registry 注册 active，七包定向测试 19/19；组合 source/installed validator 为 34/155/104，非切换前进程内 39/126 的临时 source fixture。不得继续把 `task_workspace` mapping 当新图 authority。
- 组合 readiness 的 cardinality 从 live registry/interface 派生；退役五个 predecessor packages 并激活七个 E434 packages 后，本地候选为 34 active / 155 exits / 104 commands。该数字是可复算断言，不是独立 authority。
- 本地候选已按此顺序切换 source graph、registry、manifest 与 installed/platform 投影；未通过的后置测试继续阻断提交和发布。

### R3. 原子图激活

- 激活提交必须同时更新 canonical workflow、registry、extension manifest、public graph contract、consumer schemas、dogfood/installed projection、平台投影和 cardinality assertions。
- 激活前旧生产图保持完整可运行；激活后新生产图是唯一生产图。
- 禁止出现 Branch Review 已指向新 Delivery Review，而 Merge 仍输出旧 Finalizer/Restore DTO 的半图状态。
- 禁止把旧 Publication、Finalizer、Merge 或 Restore output 转换、包装或伪投影成新 lifecycle result。

### R4. 旧边与旧 owner 退休

必须从 active production graph 同时移除：

- `guru-create-task-workspace` 及其旧 workspace/mapping 创建入口
- `Branch Review -> guru-review-task-publication`
- `guru-review-task-publication -> guru-finalize-task`
- `guru-finalize-task -> guru-merge-task-pr`
- `guru-merge-task-pr:phase2_reentry_required -> guru-restore-archived-task`
- 旧 archived read-only review chain 对 Publication/Finalizer/Merge 的专用生产边

旧 package、schema、tests、docs 和 platform projection 按 subtraction-first 合同处理：失去 supported consumer 的 active 资产在本任务删除或明确历史化；不得仅因名称曾是 public/stable 而保留第二运行路径。

### R5. Completion 路由

`guru-review-task-completion` 的生产出口必须一一映射到真实 owner：

- `remaining_work` -> `active-task-continuation`，再按 current task 阶段进入真实工作 owner
- `evidence_pending` -> Completion 自身的 fresh evidence-refresh 入口，不预填 completed
- `additional_delivery_required` -> `task-delivery-planning-router`，重新确定下一 slice 后才进入 Delivery Review
- `requirements_revision_required` -> requirements clarification owner
- `implementation_revision_required` -> Phase 2 implementation owner
- `completed` -> Issue Closure owner
- `blocked` -> completion stop

任何路由都保持同一 task active，只有 `completed` 可进入 Closure。

### R6. Reactivate 路由

`guru-reactivate-task` 必须保留原 TaskId/source/原 scope 与历史 Delivery，建立递增 generation，并按现行五个出口精确映射：

- `reactivated_to_planning` -> `task-planning-router`，由当前规划 owner 判断真实缺口；不得从历史完成状态直接跳过规划
- `session_binding_recovery_required` -> `task-session-recovery-router`
- `resume_reactivation` -> `task-reactivation-resume-router`
- `source_correction_required` -> `task-source-correction-router`
- `reactivate_blocked` -> `task-reactivate-blocked` stop

Issue reopen 仅触发 fresh 核对，不自动激活。旧 `guru-restore-archived-task` 的 `restored_to_phase2` I/O 不得复用或改名为 Reactivate。

### R7. 在途旧链迁移

- 切图前已开始且仍依赖旧 Restore 的任务，必须按其 pinned 旧版本完成，或由人工逐项处置。
- 不建设通用旧链迁移状态机，不批量改写 archived task，不自动把不完整旧 archive 当成已正常结束 task。
- 正常结束的旧格式 archive 仅能经新 Reactivate fresh 验证后承接。
- 旧归档按来源 Issue 查找时，必须读取旧 finish-summary/index 及 archive Git 身份作候选发现，再验证唯一 TaskId/source；没有结构化来源、只在旧 summary/ledger 中记载 Issue 的归档必须先人工语义核对并修正来源，不能直接进入 Reactivate。不能因目录名、Issue 状态或旧 Finalizer residue 猜测已正常结束。
- `castbox/ai-chat-roleplay-backend#154` 是在途旧链阻断实例：旧 PR #156 已合并、远端 head 与本地 reviewed head 不同，旧 Finalizer preview 可 prepared 而执行被 terminal PR 前置阻断。旧版本完成或逐项人工处置必须明确此差异；不得修改业务 task branch/mapping、复用已合并 PR、绕过 Finalizer 或将旧 DTO 伪装成 Delivery result。该业务仓 Test Application/Deployment 和上游 #52 P8 仍是独立外部阻塞，不在本 task 代执行。

### R8. 分发与升级一致性

- canonical、dogfood、installed、Shared/Codex/Claude/Cursor 必须载入同一 active graph 和同一 package interfaces。
- preset reapply 后不得出现 `.new`/`.bak` 未处置漂移，且不得把新图回退成旧图。
- `trellis update` 后，团队扩展仍由 canonical workflow/preset/overlay 恢复，不依赖一次性 patch；不要求远端 marketplace 安装。

## Acceptance Criteria

- [x] #435 Delivery package/interface/projection inventory 已随 PR #437 合入，并保持 workflow integration deferred。
- [x] 历史 #436 五包已随 PR #442 合入；#454 D436 又由 PR #474 更新其 canonical majors，现行 installed/production 仍 deferred，旧 #436 通过记录不证明新 major 就绪。
- [ ] #435/#436/#443/E434 的组合 source package-ready gate 通过，六个 planned ID 与 `guru-create-issue` 有完整 canonical package；切换候选的 installed/platform/graph 门禁也通过。缺一项、cardinality 与 current authority 不一致、或 session-binding consumer 未闭合时 fail closed。
- [ ] workflow graph 只有一条生产链：Branch Review -> Delivery Review -> Publish -> Delivery Merge -> Completion -> Closure -> Finish -> Cleanup。
- [ ] A/B scope 先交付 A 时，第一次 merge 后 task 仍 active、Issue 仍 Open、B 明确 remaining work；第二次 Delivery 后才能 Completion。
- [ ] Delivery PR 全部为 `Refs`，Finish bookkeeping PR 不进入 Delivery discovery，Completion 前不存在 closing keyword。
- [ ] Completion 七个 exits、Reactivate 四个非阻断 exits 与一个 blocked exit、D443 六个非阻断 exits 与一个 blocked exit均有唯一 consumer，unknown/multiple/dangling edge fail closed；按现行 interface 精确校验，不沿用 r4 历史名称。
- [ ] Completion pass 后才执行 Closure；Closure 完成后才执行 Finish；目标基线已持久化唯一 archive 后才返回 Finish success；Cleanup 只消费本轮 Finish success。
- [ ] Reactivate 覆盖原资源复用、重新准备、同月归档、跨月归档、业务变更新 Delivery、只补验证无业务 Delivery 六类路径；旧归档按 Issue 检索与唯一身份验证通过，无替代 task、旧 PR 复用或 active/archive 双副本。
- [ ] 旧 Publication/Finalizer/Merge/Restore active markers、consumer declarations、manifest selectors 和平台入口全部退休；历史文档可保留但不成为 current runtime consumer。
- [ ] 切换测试证明旧图完整或新图完整，所有 package 缺失/版本不符/投影不一致组合均不能激活半条新链。
- [ ] canonical、dogfood、installed、Shared/Codex/Claude/Cursor、preset reapply、workflow graph/cardinality、task validation 和 `git diff --check` 全部通过。
- [ ] 一个代表性 clean throwaway 以本地 canonical workflow 样本 + preset 验证新图与原生入口；远端 marketplace 不在验收范围，完整多平台 Release Gate matrix 留给专门 Release Issue。
- [ ] 旧前驱集成失败逐项归因：历史 Finalizer eval/exit 与 D436 major 输入 fixture 不得以修改期望或旧 DTO adapter 虚假通过；旧图定向验收和新图定向验收各自只在适用版本运行。

## Non-Goals

- 不实现 #435/#436 已独占的 package 内部业务语义。
- 不重构 Phase 0、完整 Planning、KDD、CI 自动合并、GitHub ruleset、遥测或独立架构审查方法。
- 不新增独立 Acceptance，不纳入 follow-up task 的创建、分类或路由。
- 不建设 archive 通用自动恢复框架、通用事务日志、分布式锁、故障注入矩阵或 hostile-input 防御。
- 不在本轮执行正式版本发布、tag、GitHub Release 或业务仓生产验证。

## Docs SSOT Plan

- 状态：`delta_first`
- Task-local 计划：本目录的 `prd.md`、`design.md`、`implement.md`。
- RDT contribution：新增 `docs/requirements-design-test-contributions/434-task-delivery-lifecycle/`，承接本任务的 requirement/design/test/traceability/manifest 增量；经 RDT owner 审查后再 promotion 到 current version authority。
- Architecture contribution：新增 `docs/architecture/contributions/434-task-delivery-lifecycle.md`，并按 Architecture owner 结论新增必要 ADR，更新 current/target/domain/integration/GAP/roadmap/evidence；未经 serialized promotion 不直接改写 shared current authority。
- Workflow durable docs：同步 `trellis/workflows/guru-team/workflow.md`、`.trellis/spec/workflow/` canonical specs、preset README/workflow README、extension/version release notes 中的 current graph 和迁移说明。
- 历史资料：旧 Issue、旧 contribution、旧 version docs 保持 immutable historical evidence；只移除其 current selector/active runtime authority。
- Phase 2 checkpoint：实现完成后由 RDT/Architecture owner 完成 task contribution review/promotion；promotion-created diff 重新经过 Phase 2、Task Commit 和独立 Branch Review。

## Notes

- 本任务已由当前 Planning approval 进入 `in_progress`；#434 激活候选的实现、组合定向验证、本地 clean sample 与两轮新鲜只读审核已完成，正式 Phase 2、提交后完整 Branch Review、shared authority 晋升与交付收尾仍须逐项完成。
- #435/#436/#443 历史能力与 #454 D443/D436 canonical majors 已合并；#454 的 Phase E 候选包仍需组合接口、installed/selector/旧前驱收敛，不能把 source-local 39/126 或定向测试视为生产切换。
- Issue #434 的 Phase 0 workspace 创建确认不能替代 Phase 1 方案确认。
