# Guru Trellis Evolution Requirements

版本：`evolution-requirements-revision-2026-08-27`；文档状态：`requirements_ready_for_design`；目标层
`EVO-001..007` 状态：`user_confirmed`；详细需求层状态：`evidence_ready`；最后修订：
`2026-08-27`。

## 0. Authority、状态与阶段边界

本目录是 Guru Trellis 下一阶段产品进化需求的唯一文档集 SSOT。本文件拥有产品目标、
功能范围与进入 Design 的主合同，包括：

- 已由用户确认的产品目标 `EVO-001..007`；
- 全量目标场景 `REQ-UC-EVO-*`；
- 目标功能需求 `EVO-REQ-*`；
- 核心能力 `EVO-CAP-*`；
- 进入 Evolution Design 前的验收与放行条件。

目标非功能需求 `EVO-NFR-*` 的唯一主定义位于
[`requirement-non-functional.md`](./requirement-non-functional.md)；本文件只引用其编号和适用
fixture，不拥有或复制非功能正文。

它定义 target，不声明 current runtime 已经实现、验证或发布这些结果。本候选用于
current-to-target trace 的冻结 authority snapshot 为
`source_ref=d907fcc5e17f23b6499648e5e9a208457f2d6f8b`。该 ref 是本轮 reconciliation 时记录的
`origin/main`，提交时间为 `2026-08-25T17:20:17+08:00`；它不是对未来远端 `main` 的持续
声明。后续 `origin/main` 漂移不得被本候选隐式吸收，必须重新绑定并复审。该 snapshot 包含
未改变的 `.40` Requirements/Design/Test authority、其 capability-loss 与独立
consistency/installation gate 语义，以及 `.40` 发布后新增的 Phase 2 Gitlink reviewed-content
identity 与 Branch Review EOF-only whitespace observation 能力。具体
Requirements/Design/Test/Architecture 路径与读取方式由
[`current-capability-inventory.md` 第 1 节](./current-capability-inventory.md#1-authority-与一致性关系)
唯一列出。当前未 reconciliation 的 worktree 中相对 `.40` 文件只是 planning snapshot 的历史导航，
不得作为该 immutable source binding 的替代 authority；current 行为还须结合该 source snapshot 下的
canonical workflow/Skill package 与必要 Git/live facts 证明。

本轮已完成对上述 ref 的 Requirements reconciliation；`a4b68d42…` 仅保留在历史 evidence 中
描述当时事实，不再作为 current authority。重新绑定未复用任何旧 fresh-review 结论；`EVO-EVD-043`
曾使上一轮结论 stale，当前 `REQ-REV-129..132` 已把 cache-friendly authority ordering、task 三件套的
稳定上下文职责、AI-owned autonomous progression、导航/格式与下游 planning projection 同步到完整
候选；修订后 exact candidate 的 fresh Requirements、Strict technical 与确定性闭包均已通过。当前
Requirements 状态仍为 `requirements_ready_for_design`；后续 Evolution Design exact candidate 已独立
完成 fresh 全稿审核并达到 `design_ready_for_delivery_planning`，其 current 状态由
[`docs/design/evolution/README.md`](../../design/evolution/README.md) 拥有；target implementation 尚未开始。

### 0.1 唯一消费规则

- 后续 Evolution Design、推进方案、重构 Issue、Trellis planning、Architecture
  contribution、Branch Review 和 exact-candidate Release 只引用本文件 locator、适用
  identity、需求 delta 与验收，不复制本文件正文。
- 修改、删除、合并或弱化任一 `EVO-*`、`REQ-UC-EVO-*`、`EVO-REQ-*`、
  `EVO-NFR-*` 或 `EVO-CAP-*`，必须先形成新的明确产品决定并更新本 SSOT。
- 现有 `#247 -> #249 -> #250 -> #292 -> #293 -> #261 -> #248 -> #252 -> #267`
  串行链只保留为重构前稳定版发布后的候选实施拆分。它不是需求、设计、推进方案或实施
  顺序 authority，也不是 `v0.6.15-guru.1` 的前置、owner 或验收范围；不得反向限制本文件的
  场景和验收范围。
- 本文件完成 Requirements 审核前不得进入 Evolution Design；Requirements、Design 和
  推进方案全部审核通过前不得据此创建新的实施 Issue 链。
- 当前阶段不预选 Skill 边界、public DTO、schema、script、文件布局或 Issue 数量；这些
  属于后续设计与推进方案的责任。

### 0.2 新旧合同边界

本轮演进保留 current 产品能力，不保留旧 workflow 合同本身。最终 exact candidate：

- 只允许一个新合同和一条新正常路径；
- 不保留 legacy route、dual-read、dual-write、兼容 wrapper、旧 exit/schema fallback 或
  仅为旧 artifact 存活的 adapter；
- 仍须支持现有仓库通过官方 install/update/upgrade + Guru preset 重应用迁移到新合同；
- 迁移完成后 canonical、dogfood、installed 和各平台只投影新合同。

“不向前兼容旧合同”不得被解释为允许丢失 current 用户能力、破坏已有仓库迁移，或降低
exact-candidate Release 的证明范围。

本节只约束发布后的重构 candidate，不追溯修改重构前稳定版。#304 独占
`v0.6.15-guru.1` 的 current Release authority；其 `f962b640...` 历史快照当前为
`candidate_stale`，本文件不把该快照重新声明为 frozen/verified，也不参与其修正或重新冻结。
该 pre-refactor release 不声称实现任何 `EVO-*` target，本目录既不是其 Release blocker，
也不把 #304 发布闭环设为 Evolution Design eligibility 的前置。

### 0.3 需求证据

| Evidence | 证据与可得结论 | 边界 |
| --- | --- | --- |
| `EVO-EVD-001` | `2026-08-24` 用户明确确认 `EVO-001..007` 及其最终用户结果 | 证明产品方向，不证明 current 实现 |
| `EVO-EVD-002` | 用户提供的 Himora Issue #52 Codex visible-session export（thread `01a01ea9-1fd8-73f2-8219-53a69229cd56`；source SHA-256 `fac0ee1af72b12300174828023239be1837f466000b0fb32890716e52bfde71b`；visible JSONL SHA-256 `1c8d38a52be68f6f8f5fdd0fccbfe29d920169c992b691731377ed3785ec0786`）：17.14 小时跨度、172 条消息、793 次工具调用；标准 Intake 到 Plan approval 约 104 分钟、279 次工具调用；工具输出约 556 万字符，排除导出正文与两张 base64 图片后仍约 463 万字符；160 个结果超过 10k 字符、49 个结果被截断；118 条 commentary 中约 55 条暴露内部流程；68 次 wait 中 45 次引用不存在的 cell id；63 个不同 `/tmp/*.json` locator；4 份 continuation 摘要共 31,523 字符；Phase 2 后 9 条连续用户意图未被消费 | 是问题诊断样本，含人工等待与外部等待，不直接作为性能对照基线，也不能单独证明失联根因 |
| `EVO-EVD-003` | 对候选 Issue 链的多轮整体审核持续暴露新的 P0/P1 断链，用户确认根因风险是缺少端到端产品 authority，而非单个 Issue 措辞不足 | 证明应先完成本 Requirements/Design/推进方案，再拆 Issue；不证明候选链中每个 Issue 都不可复用 |
| `EVO-EVD-004` | current Requirements/Design/Test、Architecture 2.0、canonical workflow、Skill registry/interfaces 与官方 Trellis 扩展合同 | 只证明 current 能力与约束，不能把 current 实现形态固化为 target 设计 |
| `EVO-EVD-005` | `2026-08-24` 用户确认按上一轮 Requirements 全稿审核建议修订，收窄现行 `EVO-CAP-001/EVO-CAP-004` 的责任边界，并补齐 task-free、pre-task、RDT promotion、latest-intent 与 Design gate 闭环 | 其中关于流程性能定量门槛的旧选择已被 `EVO-EVD-007` 取代；核心能力由 `EVO-EVD-010` 进一步校正为四项独立 `P0`，其余产品取舍继续有效 |
| `EVO-EVD-006` | `2026-08-24` 用户确认建立完整 current capability inventory，并要求与 `.40` Design capability inventory 保持显式一致性关系 | 证明 inventory 是 Requirements 必需追踪产物；不把 `.40` Skill 数量、id 或合同 shape 固化为 target API |
| `EVO-EVD-007` | `2026-08-24` 用户明确决定：流程耗时、rounds、bytes、compression 次数及相对 baseline 改善比例不作为需求验收或 Release 门槛；目标是尽最大可能减少中间交接、上下文堆积、文档重读、不必要脚本与重复验证，同时不得降低语义审查、证据和交付正确性 | 取代 `EVO-EVD-005` 中关于定量性能门槛的选择；允许保留诊断观测，但不得以相对性能数值判定 candidate PASS/FAIL |
| `EVO-EVD-008` | 用户提供的 Guru SSOT/SDD 反馈包（session `01a02293-f53a-7f52-8a87-ffb424293902`；ZIP SHA-256 `50071437fbdf2d34fc2aa7c75cfc67bf50514e29ade5e0563aed9680227f6a7d`）证明：standard graph 延迟接管、task planning artifacts 被错误当成 repository RDT SSOT、`no_docs_update_needed` 与自报 semantic booleans 获得结构 PASS、submodule 初始化/读取多次阻塞并放大会话成本 | 是正常 honest-but-fallible 失败样本；不把反馈包中的固定目录、固定章节数或关键词 machine-check 建议直接提升为 target 合同 |
| `EVO-EVD-009` | `2026-08-24` 用户确认：repository Requirements/Design/Test SSOT 是 task 文档写作与全生命周期判断的上位 authority；task `prd.md`/`design.md`/`implement.md` 只能引用、修订和完善 current RDT，不得替代或绕过它；所有 parent-repository task 默认排除 Git submodule 的 RDT、代码、状态和验证 | 证明 target 必须完成 RDT-first 文档中心转换与 submodule 默认边界；不允许 Planning 直接改写 shared current，也不禁止用户显式启动独立 submodule repository task |
| `EVO-EVD-010` | `2026-08-24` 用户确认：Repository RDT SSOT 驱动与受治理演进必须与 authority/route 连续性、Architecture-aware Planning、低成本执行连续性并列为独立 `P0` 核心能力 | 证明后续 Design/Test 必须独立展开 RDT 的 current authority、impact、task-local contribution、promotion、freshness 和全生命周期消费；不预先规定 Skill、schema、DTO 或文件实现形态 |
| `EVO-EVD-011` | `2026-08-24` 用户确认按 fresh Requirements 全稿审核建议修订：补齐五类入口与两种 delivery route、校正 Release 前后时序、闭合 task-free finding/recovery、定义已有副作用后的 latest-intent 路线，并消除功能/非功能双主定义 | 证明这些是 Requirements 产品合同修订，不是 Design 对 Skill、typed exit、DTO 或脚本布局的预选；修订后仍须 fresh 全稿复审才能恢复 `requirements_ready_for_design` |
| `EVO-EVD-012` | `2026-08-24` 用户确认继续按第二轮 fresh 全稿复审建议修订：标准资源副作用前先收敛 suspended work 的 scope/plan、区分 clean install 与 existing migration、区分等价 stale recovery 与 unresolved/material stale block，并按 live cutover state 分类 migration failure | 证明本轮修订应修正产品 route、terminal、re-entry 与质量门槛的正向模型；不预选 transfer、installer、cutover 或恢复机制的 Design 实现 |
| `EVO-EVD-013` | `2026-08-24` 本候选采纳第三轮 fresh Requirements 审核建议：把 provider recovery 扩展到 distribution、clean install、migration、Release 外部动作，证明既有 active/archive history 经迁移后仍可恢复/查询，补齐 `github_pr`/`none` 混合并行隔离，并清除第二章重复的可执行 route 规则 | 证明四项 Requirements 合同与验收缺口已纳入本候选修订；不预选 provider、迁移或并行执行的实现机制，仍需 fresh 全稿复审 |
| `EVO-EVD-014` | `2026-08-24` 本候选采纳本轮 fresh Requirements 审核建议：撤销未来日期与未发生的 ready/pass 断言，并将 current `.40` authority 的 capability-loss gate 与独立 consistency/installation gate 同步到 Evolution Requirements | 证明 `REQ-REV-029..030` 的局部 Requirements 修订已纳入本候选；修订后仍需对 exact candidate 执行 fresh 全稿复审，Design、base reconciliation、提交与发布属于后续阶段 |
| `EVO-EVD-015` | `2026-08-24` 本候选采纳 Strict Requirements 审核建议：闭合 invocation-level entry 互斥分类与 stop、明确 standalone projection 和 install/migration/Release 内嵌 gate finding 的 caller ownership，并把 `.40` current authority 绑定到 immutable source ref/path | 证明 `REQ-REV-031..033` 的局部 Requirements 修订已纳入本候选；base reconciliation、Design、提交与发布不在当前阶段，修订后的完整候选仍需 fresh 全稿复审 |
| `EVO-EVD-016` | `2026-08-24` 本候选采纳 Strict Requirements 审核建议：修复 additive intent 在 current owner、material freshness 与不可逆远端副作用之间的断链，并要求 pending additive 具有唯一 consumer、不得修改 in-flight/published candidate，等待旧 lifecycle 收敛到既定 terminal 或 terminal block | 证明 `REQ-REV-034` 的局部 Requirements 修订已纳入本候选；不预选 Design、提交、base reconciliation 或发布实现，修订后的 exact candidate 仍需 fresh 全稿复审 |
| `EVO-EVD-017` | `2026-08-24` 本候选采纳 fresh Requirements 审核建议：修复不可逆远端副作用后的 generic override 绕过顶层入口重分类，并要求 latest override 在旧 lifecycle 收敛后投影为新的 `request_received`，重新执行 `entry_route_selected`，只有 `new change` 才进入 change lifecycle | 证明 `REQ-REV-035` 的产品 route 修订已纳入本候选；后续阶段仍需独立重入 Design/交付入口，exact candidate 仍需 fresh 全稿复审 |
| `EVO-EVD-018` | `2026-08-24` 本候选产品决定：不可逆远端副作用后的 material additive 在旧 lifecycle 收敛 current 后，作为新的 `request_received` 按内容重新执行五类顶层入口分类；只有 `new change` 才进入二级 mode selection 与独立 change lifecycle，保留的 current direct-answer 能力不改变不得默认 `new change` 的约束 | 证明 `REQ-REV-036` 的产品 route 已收敛；pending intent 不预设为 `new change`，后续 Design、提交、base reconciliation 与发布另按阶段入口处理 |
| `EVO-EVD-019` | `2026-08-24` 本候选采纳 fresh Requirements 审核建议：修复 specialist review 的 review-only/change-scoped 边界，并闭合 wording 与 normal-scenario qualification 的 typed result、唯一 caller、blocked/re-entry 路线 | 证明 `REQ-REV-039` 的局部 Requirements 修订已纳入本候选；review-only 不静默修改被审对象，change-scoped `content_changed` 回 active change caller，修订后的 exact candidate 仍需 fresh 全稿复审 |
| `EVO-EVD-020` | `2026-08-24` 本候选采纳 fresh Requirements 审核建议：修复 future authority ref 与 task candidate locator 漂移，并区分 planning baseline、working-tree candidate locator 与 current authority；当时读取的 future snapshot 不作为该轮 evidence，future-dated candidate HEAD 仅作定位 | 证明 `REQ-REV-040` 在当时把 current authority 重新绑定到 `a4b68d42b25e3d2173fac2db353295043590cca5`；这是历史事实，现已由 `EVO-EVD-037` 的 `d907fcc5…` reconciliation 继承，不得把该旧 locator 继续当作 current authority |
| `EVO-EVD-021` | `2026-08-25` 本候选采纳最新 fresh Requirements 审核建议：补齐 distribution/release 二级 exactly-one action、change-request readiness 结果、standalone specialist 自然完成、Archive/Finish/Cleanup 失败恢复，以及 Release publication/post-publish blocked 与 published-unverified 边界 | 证明 `REQ-REV-043..047` 的 Requirements 修订已纳入本候选；这些内容只定义 route、owner、terminal、re-entry 与验收，不预选 Design 实现，exact candidate 仍需 fresh 全稿复审 |
| `EVO-EVD-022` | `2026-08-25` 本候选采纳 fresh Requirements 审核建议：分离 Release confirmation 缺失、明确拒绝与 candidate/decision-relevant facts 变化三类结果 | 证明 `REQ-REV-048` 的 Requirements 修订已纳入本候选：缺失保持等待，明确拒绝形成零 publication 副作用 terminal，事实变化使旧等待失效并回 pre-publish owner；exact candidate 仍需 fresh 全稿复审 |
| `EVO-EVD-023` | `2026-08-25` 本候选采纳 fresh Requirements 审核建议：保留 current authority 的 non-file-changing direct answer，并闭合既有 active lifecycle 的取消、放弃与清理 disposition | 证明 `REQ-REV-049..050` 的 Requirements 修订已纳入本候选；direct answer 与 disposition 的副作用边界、re-entry 和 history 可达性属于本候选合同，后续实现另行承接 |
| `EVO-EVD-024` | `2026-08-25` 本候选采纳 fresh Requirements 审核建议：收窄 specialist 顶层 profile、闭合 active cleanup 拒绝/零资源 abandonment、disposition durable history 查询，以及 direct answer live facts 不可用时的诚实边界 | 证明 `REQ-REV-051..054` 的 Requirements 语义修订已纳入本候选：两个受支持 specialist profile、唯一 retain/suspend choice、cleanup 后 history 查询和 unavailable/unverified 结果均已有主合同，exact candidate 仍需 fresh 全稿复审 |
| `EVO-EVD-025` | `2026-08-25` 本候选产品决定：stock upstream Skill 与 Guru Skill 发生自然语言冲突或流程重叠时，Design 可比较 patch、managed absence、quarantine 或精确删除；本阶段只建立完整 inventory、successor/provider 边界、dispatch 抑制、provenance 与 install/migration/update/upgrade/reapply 验收 | 证明 `REQ-REV-055` 的范围与验收合同已纳入 Requirements；不表示任何 upstream mutation 已执行，后续 action 由 Design 选择并按独立阶段验证 |
| `EVO-EVD-026` | `2026-08-25` 对官方 `@mindfoldhq/trellis@0.6.15` immutable package snapshot 的 live 研究：common commands/skills、bundled skills、platform agents、channel workers、shared `.agents/skills` projection 与 `update.skip`/`.new`/`.bak` 行为均来自同一 registry integrity 与 capture tarball identity | 只证明本轮 stock inventory 的 source/projection facts 与外部 maintenance inputs；不把 package implementation、CLI flag 或 collector 行为提升为 Guru target contract，也不证明任何 suppression 已实现 |
| `EVO-EVD-027` | `2026-08-25` 当前 Guru workflow/preset 明确把 `trellis-*` official paths 归 upstream，现有 Guru overlay 只管理自身 namespace；尚未存在针对每个 host/path 的受支持 Guru mutation/interception owner | 证明 Requirements 必须交付逐 asset owner tuple、Design handoff 与 missing-owner blocked contract；Requirements gate 与尚未选择的 Design mutation owner 分属不同阶段，不能互相替代 |
| `EVO-EVD-028` | `2026-08-25` 本候选产品决定：Evolution 必须顺畅快速、无能力丢失、无反复回读、极简交接、最小上下文占用，并最大程度与 repository RDT SSOT 和 Architecture Baseline SSOT 深度融合；若 stock upstream Skill 与 Guru Skill 兼容性差，允许修改或精确删除，不为保留冲突 surface 增加长期 patch 压力 | 这是本轮 Requirements 的效率、能力保留、上下文和 authority integration 裁决；要求 stock policy 兼容性优先、精确移除优先、authority_context 复用和按语义依赖定向重读；upstream action 仍属于后续 Design/maintenance 阶段 |
| `EVO-EVD-029` | `2026-08-25` 本候选产品决定：独立请求不得因旧 lifecycle 的无界等待而饥饿；必须有无 active lifecycle 的显式验收输入；standard/task-free 只承接真实文件变更；stock action 选择规则保持单一主定义 | 证明 `REQ-REV-092..095` 已按该决定完成局部 Requirements 修订并保持 `requirements_draft`；补充独立请求隔离/回程、fixture 差集、mode applicability 和 NFR 单向引用；下游 Design、提交和发布不属于本证据范围 |
| `EVO-EVD-030` | `2026-08-25` 本候选产品决定：正式能力表必须具备完整字段；specialist caller/standalone terminal、远端 pending intent identity/envelope、bound override re-entry identity/envelope 与 functional SSOT 必须单向收敛 | 证明 `REQ-REV-096..100` 已按该决定完成局部 Requirements 修订并保持 `requirements_draft`；补充四张正式能力表的显式字段、active/standalone specialist 互斥回程、远端 pending intent 与 bound override 的新 invocation identity/envelope/receipt 顺序和 NFR/inventory 的单向引用；下游 Design、提交和发布不属于本证据范围 |
| `EVO-EVD-031` | `2026-08-25` 本候选产品决定：入口摘要与 target 文档读取导航保持单一来源，source-stimulus 与已绑定内部/上游 event 的顶层 preclassification 边界明确 | 证明 `REQ-REV-102` 已完成局部 Requirements 修订并保持 `requirements_draft`；下游 Design、提交、发布和 provider/isolation implementation 不属于本证据范围；不证明实现、测试执行或 Requirements gate 通过 |
| `EVO-EVD-032` | `2026-08-25` 本候选产品决定：post-publish semantic-defect follow-up 必须按统一 entry contract 重新分类，new candidate 只由 `distribution/release` 的 exact-candidate Release action 产生 | 证明 `REQ-REV-103` 已完成局部 Requirements 修订并保持 `requirements_draft`；后续请求沿用统一 entry contract；下游 Design、提交、发布和 provider/isolation implementation 不属于本证据范围；不证明实现、测试执行或 Requirements gate 通过 |
| `EVO-EVD-033` | `2026-08-25` 确定性审计结果：本表新增行与表头列数不一致；本候选已将全部 Evidence 行规范化为三列 | 证明表格结构可被统一解析；不改变任何 Evidence 语义、route、能力或 gate 结论，也不扩展本候选阶段范围；不证明实现、测试执行或 Requirements gate 通过 |
| `EVO-EVD-034` | `2026-08-26` 对官方 `@mindfoldhq/trellis@0.6.15` CLI 与 canonical compatibility verifier 的 live 复核：CLI 的 `init --yes/--skip-existing` 在已有文件上采用 skip 写模式；但 existing verifier cell 的初始 setup 使用 before-source 的 `trellis init -y --workflow guru-team` 并安装旧 preset，随后才按 `upgrade -> update(dry-run 分支) -> workflow preview/force switch -> preset reapply` 串行执行，整条链只做一次 composite validation，未执行 preservation-mode `trellis init -y --skip-existing` migration substep | 证明当前 verifier 的四阶段 provider chain 与一次 composite validation 的事实，并支持把 preservation-mode INSTALL 作为目标 migration substep/独立 fixture 纳入五-cell composite；不证明当前 verifier 已覆盖 `MIG-CELL-INSTALL` 或五个 supported cell 的 target closure，也不证明任何 target implementation、provider execution 或 Requirements gate 通过 |
| `EVO-EVD-035` | `2026-08-26` 本轮 deterministic pre-review 识别出 migration matrix 的物理行序、cutover 前后 failure 分类和 preset README 的 workflow replacement 文案尚未完全与 composite provider 事实对齐；本候选已统一为 `INSTALL -> UPGRADE -> UPDATE -> WORKFLOW-SWITCH -> PRESET-REAPPLY`、cutover 前仅 preservation、cutover 后才 forward-recover/blocked，以及 preview -> explicit `--force` application | 证明本轮只修订 Requirements/导航的事实一致性与可重放性；不证明 fresh semantic review、任何 target implementation、provider execution 或 Requirements gate 通过 |
| `EVO-EVD-036` | `2026-08-26` fresh Requirements 复核与本轮用户授权修订：distribution target 必须先分类 clean/partial/legacy/mixed，Intake 的 Architecture applicability 必须延后到 pre-design Planning，migration cell 只按适用执行且全 `not_applicable` 仍须形成 composite current | 证明 `REQ-REV-109` 已同步修订主需求、状态/回程投影、NFR、inventory、fixture 与 task-local evidence 边界；不证明 provider mutation、target implementation、fresh gate 通过或 Design readiness |
| `EVO-EVD-037` | `2026-08-26` 对 fresh `origin/main=d907fcc5e17f23b6499648e5e9a208457f2d6f8b` 的 immutable reconciliation：`.40` Requirements/Design/Test/Architecture locator 内容相对 `a4b68d42…` 未变，canonical installed inventory 仍派生 21 个 active Guru Skill 与 89 个 external exit；`82fb5172`/`f8d8b20d` 新增相关 reviewed Gitlink 的 superproject mode `160000`、pointer/content identity，`73973273` 新增仅 EOF 额外空行且 meaningful bytes 不变时的无严重度非阻断 observation | 证明 current authority 已统一重绑到 `d907fcc5…`，并要求 target 在 `EVO-REQ-028,030` 与 `CUR-CAP-022..023` 无损承接两项新增 current 能力；不把历史 `a4b68d42…` 改写成当前事实，不证明 target implementation、fresh Requirements gate 或 Design readiness |
| `EVO-EVD-038` | `2026-08-26` 对 frozen `@mindfoldhq/trellis@0.6.15` stock source 的 fresh role 复核：`trellis-channel` 只提供 transport；platform/channel workers 提供 caller-bound research/implementation/check 结果；`trellis-session-insight` 为只读 history query；raw `trellis-break-loop` 会要求立即更新 spec 并提交，因此其写入形态与 Guru RDT/change lifecycle 冲突 | 证明 `REQ-REV-116` 必须把 provider、worker、explicit 与 Guru-owned successor 的能力词汇完全拆开：只保留 break-loop 的显式只读诊断/建议，任何写入意图在 raw invocation 前回到 Guru `new change`/active caller；不证明 suppression/adapter 已实现、stock policy current 或 Requirements gate 通过 |
| `EVO-EVD-039` | `2026-08-26` 本轮 fresh Requirements/Strict technical review 识别出三项 current-candidate 缺口：已识别 non-Guru workflow 在安全 transition plan current 后仍无正向 migration 分类、hook 高层配置与七个 setup discriminator 被误读为交叉乘积且未按 approval surface 判定 applicability、`EVO-NFR-023` 可能让已绑定 provider/worker/CLI event 重跑顶层 guard | 证明 `REQ-REV-117..119` 的局部 Requirements 修订必须闭合 foreign-workflow 正向 transition、setup partition/applicability 与 single-guard reuse；不证明修订后 fresh full-document gate 已通过，也不证明 Design、provider mutation、fixture execution 或 implementation 已开始 |
| `EVO-EVD-040` | `2026-08-26` 对 frozen `@mindfoldhq/trellis@0.6.15` init provider 的 fresh 复核：`trellis init -y` 与 `--skip-existing` 都使用 skip 写模式；`createWorkflowStructure` 除 workflow 外还管理 `.trellis/config.yaml`、scripts、spec/workspace/task 基础结构与 platform projection。若 repository 已有可归属的 official Trellis installation footprint、但没有 active workflow 或 Guru projection，现有 clean predicate 会允许 fresh-init route 保留旧 managed file，失败后又禁止转入 migration；同轮 strict review 识别出 invocation-entry byte equality 与有序 WORKFLOW-SWITCH observation 的 cutover 表述可进一步消歧 | 证明 `REQ-REV-120..121` 必须把任何可唯一归属的 official Trellis/Guru managed installation state 排除出 `clean_target` 并正向纳入 `existing_migration_target`，且 byte-equal predicate 只在固定顺序抵达 WORKFLOW-SWITCH boundary 后推进 cutover；unknown/unowned/mixed identity 仍 fail closed。该证据不证明 migration implementation、provider mutation、fixture execution、fresh Requirements gate 或 Design readiness |
| `EVO-EVD-041` | `2026-08-26` 对当前 exact candidate 的 Requirements/Strict technical 复核识别出三项跨投影缺口：Chapter 6 migration state graph 从 cutover 直接进入 final validation、inventory 将 standalone 与 embedded explicit-only result/consumer 混成同一形状、NFR 又把 suppressed successor 不可达误称为 capability loss | 证明 `REQ-REV-122..124` 必须显式投影 PRESET-REAPPLY current/blocked/re-entry、按调用上下文拆开 explicit result/consumer，并把 suppression successor finding 归回 consistency/preservation 与 `upstream_suppression_blocked`；不证明修订后 fresh full-document gate、Design、fixture execution 或 implementation 已通过 |
| `EVO-EVD-042` | `2026-08-26` 当前对话中的正常 Guru 协作曾在已展示副作用计划、用户已回复“确认继续”后，仍要求用户输入固定的 `确认执行 <hash>`；同轮 live authority 复核确认 current workflow 与 Commit/Merge Skill 已要求接受清晰语义肯定、禁止重复 identity。`guru-qualify-normal-scenario:requirements_scope_set` 对该候选返回 `classified / qualified_current` | 证明 Evolution 必须把 dialogue-local semantic confirmation 作为独立 Requirements 合同无损保留，并同步 NFR、状态/回程、fixture、trace 与全部 planning projection；该证据不持久化任何授权，也不证明修订后 fresh gate、Design 实现、脚本修改或任何 Git/GitHub 副作用已发生 |
| `EVO-EVD-043` | `2026-08-27` 用户进一步明确：normal workflow 要以 repository RDT SSOT、Architecture Baseline SSOT 与 task `prd.md`/`design.md`/`implement.md` 为主要稳定上下文，尽量形成可复用的 LLM cache prefix；AI owner 应直接据此自主判断和执行，不创建人类式事务交接，也不反复复述已有事实。`guru-qualify-normal-scenario:requirements_scope_set` 对两个候选均返回 `classified / qualified_approved_expansion` | 证明 `REQ-REV-129` 必须在既有低成本执行合同内明确 stable authority ordering、cache 只是执行优化而非 authority、task 三件套不替代 RDT/Architecture，以及 transaction handoff/assignment/signoff/repeated-fact narration 的零计数；不新增 public DTO、中间 handoff artifact 或实现机制，也不证明修订后 fresh Requirements/Design gate、runtime cache hit 或 implementation 已发生 |

## 1. 产品总述

### 1.1 产品用途

Guru Trellis 是运行在官方 Trellis 扩展面上的 AI-first 工程工作流。它把一项用户请求从
需求理解、Repository RDT-driven 与 Architecture-aware Planning、实现与审查，持续推进到
发布、合并、Finish 和资源清理，并让每个阶段都以 live current authority 为依据。

本轮进化的北极星是：

> 把 Guru Trellis 进化成一个由 repository RDT SSOT 与 live current authority 驱动、
> Architecture Baseline 全程治理、AI semantic owner 闭环执行、低交接低上下文成本，
> 并能从需求进入一直可靠完成到交付清理的工程工作流。

### 1.2 目标用户

- 在业务仓库中提出需求、设计约束或已审阅设计，并与 AI 共同推进交付的用户；
- 使用 Codex、Claude 或 Cursor 执行 Guru Team workflow 的工程 Agent；其 Codex
  common/bundled Skill 通过官方写入的 shared `.agents/skills` projection layer 提供；
- 维护业务仓库 Requirements/Design/Test 与 Architecture Baseline 的仓库维护者；
- 审核完整 planning、committed full diff、PR readiness 与 exact candidate 的 reviewer；
- 维护 Guru Trellis marketplace、preset、installed projection 与 Release 的维护者。

### 1.3 用户核心痛点

- `PAIN-001`：需求、已审阅设计和 current Architecture 分散在不同来源，后续作者可能
  重写、忽略或静默改动产品意图。
- `PAIN-002`：流程按局部 artifact 或 Issue 切面拆分后，同一语义被多个 owner 重复判断，
  或无人对端到端结果负责。
- `PAIN-003`：大量中间 JSON、locator、摘要、全文重读和重复 gate 扩大上下文，导致
  workflow 慢、吵、频繁压缩，并提高恢复后丢失最新用户意图的概率。
- `PAIN-004`：正常路径与 revision/recovery/remote side effect 没有统一闭环时，Agent 需
  猜测下一步，或在已产生不可逆副作用后错误返回早期阶段。
- `PAIN-005`：Architecture Baseline 只在 planning 产后审核，无法证明首稿设计真正消费
  current baseline，也难以把合法的新架构发现转化为受治理的演进建议。
- `PAIN-006`：旧合同兼容、平台副本和安装投影可能让重构保留双路径，局部测试通过却无法
  证明 exact candidate 具备同一完整能力。
- `PAIN-007`：上游 Trellis 以 task planning artifacts 为主要文档 authority；若 Guru Team 沿用
  该模型，Agent 可以用三份 task 文件或自报 `no docs update` 结论替代、绕过 repository RDT
  SSOT，使局部 plan PASS 与项目长期产品/设计/测试 authority 脱节。
- `PAIN-008`：父仓库中的 uninitialized、dirty、不可访问或无关 Git submodule 被默认递归读取、
  初始化、检查或纳入验证时，会引入与 task 无关的阻塞、副作用和上下文成本。
- `PAIN-009`：官方 Trellis stock Skill 会与 Guru Skill 同时投影到平台 Skill 根；仅依靠
  `.trellis/workflow.md` 的 routing marker 不能阻止平台对 stock description/命令的自然语言
  自动匹配，可能让两个 semantic owner 同时澄清、检查、继续或收尾，产生重复读取、重复 gate
  或互相矛盾的 route。
- `PAIN-010`：AI 已完整展示 current 精确副作用计划且用户已用“确认继续”等清晰肯定回复时，
  若流程仍要求复制 `确认执行 <hash>`、task/branch/SHA、摘要或其它规定句式，就会把本应由 AI
  完成的对话语义判断错误下放给用户和字符串挑战，造成无业务选择的额外交互、确认反复和授权
  范围误读；脚本若解析或持久化该回复，还会把 dialogue-local confirmation 错写成 workflow authority。

### 1.4 全量功能与场景清单

#### A. 请求进入与 requirement authority

| 场景 | 触发 | 目标结果 |
| --- | --- | --- |
| `REQ-UC-EVO-001` 清晰 Issue 需求 | live Issue 已充分描述业务目标、范围与验收 | 零例行提问地形成忠实、可追踪的 current requirement authority |
| `REQ-UC-EVO-002` Issue 含已审阅设计 | Issue 同时包含需求和已审阅的设计承诺 | 产品需求与 reviewed-design commitments 分别保真承接；后续 `design.md` 不得忽略、重写或无说明背离已审阅设计 |
| `REQ-UC-EVO-003` 信息不足或来源冲突 | 用户请求、Issue 正文/评论或 current authority 存在真实歧义 | 每轮只问一个最高价值问题；冲突显式化；在信息充分前不猜测、不启动下游副作用 |
| `REQ-UC-EVO-004` 无现有 Issue 的标准变更 | 请求需要标准 task/交付但没有 Issue | 先完成必要的需求理解和重复/范围判断，再就精确外部副作用取得确认；不得伪造 Issue identity |
| `REQ-UC-EVO-005` 有界 task-free 变更 | 用户显式要求 task-free，或请求可高置信判定为目标清晰、路径有界、仅影响 current checkout、可逆、低风险，且不需要隔离 workspace、正式 Planning、committed full-diff review 或高风险验证 | 在 current checkout 内完成 pre-write suitability、受限写入、targeted check、finding/revision 与 post-write risk review；不创建 Issue/task/worktree，不生成正式 `prd.md`/`design.md`/`implement.md`，也不因显式 task-free 绕过适用检查。检查 finding 可在同一有界 owner 内修订并 fresh 重检；无法安全继续时明确 blocked；范围或风险实质扩大后停止剩余写入并返回 standard route |
| `REQ-UC-EVO-006` 已有 task 的技术修订 | 产品需求未变，只修订 design/implementation mechanism 或 closure metadata | 从最早受影响的 current owner 继续，不重跑 Phase 0、不重新询问已确认产品意图 |
| `REQ-UC-EVO-007` 非标准 invocation checkout | 当前 Codex checkout detached、dirty 或不是 selected base，但业务仓库存在可读的 exact current authority | Phase 0 可无仓库写入地读取 exact current authority；不得仅为读取创建临时 worktree，也不得把 invocation checkout 的 clean/branch-bound 状态误当产品前提 |

#### B. Architecture-aware Planning

| 场景 | 触发 | 目标结果 |
| --- | --- | --- |
| `REQ-UC-EVO-008` 无 Architecture 影响 | 需求不改变 Architecture concern | 形成可解释的快速 no-impact 结果，不创建 Architecture report、contribution 或 ADR |
| `REQ-UC-EVO-009` current baseline 正常承接 | current baseline/constitution/change contract 完整且与需求一致 | 首次实质设计写作前真实消费 current authority；`design.md` 承接 alignment，其他 planning 文档只引用 |
| `REQ-UC-EVO-010` requirement 与 baseline 冲突 | 产品意图与 current Architecture 不能同时满足 | 保留产品意图，显式呈现冲突和选择；不得为了 baseline 静默弱化 PRD，也不得把冲突伪装为 no-impact |
| `REQ-UC-EVO-011` Architecture authority 不可用 | baseline、constitution 或 change contract 缺失、过期、不完整、identity 不一致 | 在设计首稿前 fail closed，并返回 Architecture authority 的 bootstrap/repair 责任边界；修复后从最早受影响点重入 |
| `REQ-UC-EVO-012` 新需求发现 Architecture Baseline 不足 | current baseline 不能完整承接合法需求，可能只是补充 architecture fact，也可能需要新增或改变 decision | 形成 task-local Architecture contribution；只有 decision、原则取舍/例外、GAP lifecycle、owner、single-writer 或 compatibility exit 发生变化时才形成 ADR candidate；Planning 不修改 shared current |
| `REQ-UC-EVO-013` 新设计修订既有 Architecture | 设计改变 decision、GAP lifecycle、owner、single-writer、compatibility exit 或设计原则取舍/例外 | 明确 before/after、影响和退出条件，形成受治理的 task-local proposal/ADR candidate，并进入独立 promotion 生命周期 |
| `REQ-UC-EVO-014` Issue 设计与 current Architecture 不一致 | 已审阅 Issue design 与 current baseline 有真实冲突或已过期 | 两份 authority 都被保留并显式比较，由用户/Architecture 决策收敛；不得偷偷采用其中一方或完全重写 Issue design |
| `REQ-UC-EVO-015` Planning scope 实质变化 | requirement、reviewed design、Architecture authority 或实现范围的语义依赖发生变化 | 只失效最早受影响结果及其下游，自动回到正确 owner；无关上游结果保持 current |
| `REQ-UC-EVO-016` 等价 authority 重发布 | locator/version 变化但适用正文经确定性等价证明未变 | 更新 current identity/freshness 而不重放完整 semantic review；不能把 identity 更新误判为语义 scope 变化 |
| `REQ-UC-EVO-017` 普通验收场景 | 测试直接、无歧义地派生自明确 requirement/design | 直接进入 planning/test coverage，不因“需要证明是 normal scenario”再增加独立 qualification 或用户交互 |
| `REQ-UC-EVO-018` 正常计划批准 | PRD、Design、Implement 与 Architecture alignment 已完整 | 仅执行一次完整 planning semantic approval；plan acceptance、task activation 和进入实现不形成两个 routine confirmation |

#### C. 实现、审查与 shared authority promotion

| 场景 | 触发 | 目标结果 |
| --- | --- | --- |
| `REQ-UC-EVO-019` 按批准计划实现 | current plan 和 authority 未失效 | 实现只消费 current 计划与必要 live facts；完成 task scope 的 semantic check 和精确 commit |
| `REQ-UC-EVO-020` Check/Review 发现问题 | Phase 2 或 Branch Review 有真实 finding | 返回拥有修订语义的最早 owner；修订后重跑受影响 check/commit/review，不创建人工 handoff 文书 |
| `REQ-UC-EVO-021` base 演进 | 实现期间 selected base 前进 | 判断实际影响；无影响时继续，有影响时从最早受影响结果重入；不得从 Phase 0 重建既有 task |
| `REQ-UC-EVO-022` committed full-diff review | task work 已精确提交 | reviewer 从 current base 与 exact committed full diff 独立判断，不复用旧 Phase 2/旧 review 结论冒充 fresh pass |
| `REQ-UC-EVO-023` Architecture proposal promotion | task-local contribution/ADR candidate 经独立 review 可进入 shared current | 按 expected current identity 串行 promotion；promotion 后执行 fresh Phase 2、Task Commit 与 committed full-diff Branch Review |
| `REQ-UC-EVO-024` 并行 task | 多个 task 同时基于 shared current 工作 | 各自 contribution、workspace、branch 和 cleanup 隔离；shared current 只有一个串行 promotion owner，旧 identity task 正确失效/重入 |

#### D. Publication、Delivery、Finish 与恢复

| 场景 | 触发 | 目标结果 |
| --- | --- | --- |
| `REQ-UC-EVO-025` `github_pr` 正常交付 | current change/task authority 明确要求 GitHub PR，或在真实 delivery choice 中选择该 route | 从 live Issue/Git/GitHub/current plan 形成真实 PR readiness、expected-head delivery、merge 和 Issue closure-current/not-applicable 结果；不依赖 Issue Scope Ledger |
| `REQ-UC-EVO-026` `none` 正常交付 | current change/task authority 明确选择不使用 GitHub PR provider | 不调用 GitHub，不伪造 PR/Issue 事实，也不把 provider failure 降级为 `none`；仍完成适用的 local acceptance、Finish、history 与 owned-resource cleanup |
| `REQ-UC-EVO-027` provider 或外部状态失败 | push/PR/merge/Issue closure 等正常外部动作失败或状态变化 | 保留已完成且 current 的结果，从 delivery owner 恢复；不重复不可逆动作，不返回需求/Planning/实现 |
| `REQ-UC-EVO-028` Acceptance/Delivery/Merge | candidate 已完成 full-diff review | acceptance、publication、delivery、merge 和 closure 各自判断真实 current facts，顺序无倒置、无重复 semantic owner |
| `REQ-UC-EVO-029` Finish 与资源清理 | delivery 已达到对应 terminal condition | deterministic Finish 形成最小 durable history；只清理 exact owned resources，并验证必须保留的 commit/ref 可达性 |
| `REQ-UC-EVO-030` 历史查询与恢复 | 当前会话结束、压缩、重启，或用户查询已完成/已归档任务、active lifecycle disposition durable result | resumable current work 从 current authority、live facts 与最小 durable result 恢复并重入 current owner；durable history query 通过唯一 history owner 返回 archive/finish/disposition 的唯一 current result 后结束查询，不重入或激活被查询 lifecycle，且 disposition cleanup 后仍可发现；两者都不依赖长篇 handoff summary、旧 locator 集合或授权记录 |

#### E. 对话连续性、分发与 Release

| 场景 | 触发 | 目标结果 |
| --- | --- | --- |
| `REQ-UC-EVO-031` 用户在长流程中追加意图 | Agent 正在等待工具/恢复/压缩，用户给出新指令 | 最新用户意图按到达顺序被优先消费。owner-local additive 不改变 accepted scope、exact candidate、delivery route 或 terminal acceptance，或只补充 current forward-recovery 所需输入，由 current/最早受影响 owner 直接承接；material additive 在不可逆远端副作用前返回最早受影响 owner 并按 freshness 重算，在不可逆远端副作用开始后保留为可发现且有唯一 consumer 的 `additive_change_pending`，不修改 in-flight/published candidate，待原远端 owner 收敛为既定正常 current terminal、失败后 forward-recovered terminal 或 terminal block 后，唯一 consumer 为 pending intent 分配新的 invocation identity/`context_envelope`，恰好生成一次新的 `request_received`，再按 `independent_request_isolation_gate -> pre_semantic_dispatch_guard -> entry_route_selected` 顺序重新执行六类 exactly-one route；不得复用旧 identity/envelope/candidate/receipt。只有分类为 new change 才进入二级 mode selection 与独立 change lifecycle，其他分类由对应顶层 route 的唯一 owner 消费，不得默认 new change。覆盖意图仍按副作用状态停止、suspend 或完成既定 route 的三类收敛；不可逆远端副作用分支收敛后，latest override 也必须先取得新的 invocation identity/`context_envelope`，再恰好生成一次新的 `request_received`，按同一 isolation/guard/entry 顺序重新分类，且不得复用旧 identity/envelope/candidate/receipt；只有分类为 new change 才进入 change lifecycle，不得默认 new change，也不自动提交、丢弃或清理既有工作 |
| `REQ-UC-EVO-032` 长运行命令或 Agent 工作 | 工具/子流程需要多次轮询或产生大量输出 | 每次只返回新增、紧凑、可消费结果；复用有效运行句柄，不重复注入累计 stdout，不制造无效 wait |
| `REQ-UC-EVO-033` 正常清晰请求 | 无歧义、无 finding、无外部失败 | 用户只看到真实选择、实质 finding/block、必要长等待状态、阶段结果和副作用确认，不看到 workflow 内部 artifact 搬运 |
| `REQ-UC-EVO-051` 精确计划后的语义确认 | AI 已在当前对话完整展示一项 current 精确副作用计划，且计划此后未发生实质变化 | 用户回复“确认继续”“可以，继续”或其它语义等价的清晰肯定即可授权刚展示的下一项行动；不要求固定 prompt、口令、identity、摘要复述或规定句式。回复含疑问、限制或修改，计划未完整展示，或 target/scope/副作用已实质变化时，旧确认不可复用并重新展示 current 计划。PR 已创建且 READY 时，完整展示 merge 计划后的同类肯定可授权 merge，不要求用户另输 `合并PR` |
| `REQ-UC-EVO-034` 平台与安装投影 | shared `.agents/skills` projection layer、Codex/Claude/Cursor 三个 supported host、canonical/dogfood/installed、apply/reapply/update/workflow switch 使用同一 candidate | shared layer 只投影一次；三个 supported host 具备同一语义能力和路由，且没有旧合同残留、sidecar 或未审查 drift |
| `REQ-UC-EVO-035` clean install 与 existing repository migration | 新仓库 clean install，或已有仓库通过 install/update/upgrade、preset reapply、workflow switch 迁移到目标 candidate | clean repository 只从 active workflow 缺失且无任何可归属 official Trellis/Guru managed installation state 的 `clean_target` 初始状态安装并验证完整新合同；已有可唯一归属的 official Trellis installation footprint 即使没有 workflow 或 Guru projection，也属于 `existing_migration_target`，由 migration composite 承接 preserve-mode backfill、upgrade/update、workflow switch 与 preset reapply。已有 non-Guru 或未知 identity 的 active workflow 先作为 `foreign_workflow` blocked，不得被自动替换。若 non-Guru workflow 的 identity/provenance/owner 已唯一识别，且本次请求的安全 transition plan 已在当前对话中明确收敛，则重新 preclassification 为 `existing_migration_target`，由同一 migration owner 保留 source workflow 并在唯一 cutover 执行显式 preview/force switch；identity、ownership 或 plan 仍不唯一时继续 blocked。existing repository 经一次可恢复迁移后只运行新路径，用户数据与 current authority 不丢失；两类路径不混用失败 terminal |
| `REQ-UC-EVO-036` exact-candidate Release | 所有演进实现已汇合 | 同一个 exact candidate 先通过功能、Architecture/RDT lifecycle、执行成本/安静性治理和平台/install/update 的 pre-publish gate；确认缺失时只等待，明确拒绝时零 publication 副作用结束本次 Release invocation，candidate 或 decision-relevant facts 变化时使旧等待态失效并返回 pre-publish；只有取得对 current facts 的独立发布确认后才创建不可变 tag/Release，再从 tag-pinned source 完成 post-publish smoke。只有 post-publish 验证通过才是 `release_verified`；不使用相对性能数值作 Release 门槛 |
| `REQ-UC-EVO-037` 显式合同措辞审核 | 用户只要求审核有界 contract wording，且当前请求不要求修改被审对象；若文字修订本身是交付范围，则先按 `new change` 进入其生命周期，再由该 caller 嵌入 wording review | review-only 请求只能得到 `pass`、route-level `specialist_revision_required` 或 `blocked` 结果并由唯一 caller 收敛；该 route-level 标签不是新增 Skill typed exit；change-scoped wording 可由 active change caller 消费 `content_changed` 并完整重入，不成为正常 Planning 的 mandatory gate；standalone review 不得静默修改被审对象 |
| `REQ-UC-EVO-038` 显式 normal-scenario qualification | caller 的 current authority 明确要求判断候选是否属于受支持 normal scenario | 保留有界 qualification 能力；`classified`、`scope_confirmation_required`、`mechanism_revision_required`、`blocked` 均返回唯一 caller/owner，分别完成当前 route、一次 scope 澄清、机制修订后 fresh 重跑或 blocked re-entry；普通、直接派生的验收场景不经过该入口 |
| `REQ-UC-EVO-039` change request scope/prerequisite 审核 | standard request 可能重复、依赖未满足或不是一个可独立交付单元 | 在资源副作用前基于 live Issue/authority 判断复用、澄清、阻塞或独立交付 readiness；不把该判断与后续 requirement authoring 重复执行 |
| `REQ-UC-EVO-044` 显式停止当前 invocation | 用户在当前 invocation 尚未绑定需要处置的 active lifecycle、且尚未产生本 invocation 新副作用前，明确撤回请求、拒绝继续当前选择或要求不执行任何动作 | 不创建、不修改、不清理任何资源，返回停止原因和未执行边界，得到 `request_stopped -> workflow_completed`；既有无关或 suspended current work 保持可发现且不变。若用户要取消、放弃或清理一个已存在的 active lifecycle，必须先走 resume/recovery 解析 exact current work，再按已有副作用与 cleanup 合同处理，不能用 top-level stop 绕过 owner |
| `REQ-UC-EVO-045` 普通直接回答 | 用户只要求普通解释、事实、状态、信息答案或不绑定 active lifecycle 的通用只读分析/审核，不要求修改被审对象、`REQ-UC-EVO-037..038` 的受支持 specialist profile、distribution/release action、继续/恢复/处置 active lifecycle，或通过 durable history contract 解析 archive/finish/disposition result | 只读取回答所需的最小 live facts；即使主题涉及 Issue、task、branch、repository、Requirements、Design、代码或 Architecture，也不创建 Issue/task/worktree、不进入 standard/task-free mode selection、不启动 lifecycle。所需 live fact 不可用时，明确标记 unavailable/unverified 的事实与边界、不虚报 current，仍以 `direct_answer_completed -> workflow_completed` 诚实结束本次回答 |
| `REQ-UC-EVO-046` 处置既有 active lifecycle | 用户明确要求保留、暂停、取消、放弃或清理一个已存在的 active lifecycle | 先解析 exact current work、owner、副作用、owned resources 与 durable history；无不可逆远端副作用时恰好形成 retain/suspend，或在零 deletable owned resource 时 no-op abandonment，有 deletable resource 时仅经精确 cleanup 计划与当前对话确认后 abandonment；cleanup 明确拒绝必须收敛为唯一 retain/suspend choice，不能双终点。已有不可逆远端副作用时不删除、回滚或冒充取消，原远端 owner 保持 candidate 不变并收敛既定 terminal、forward-recovered terminal 或 terminal block，之后只处理允许清理的本地 owned resources；全部 disposition result 保留 cleanup 后仍可由 history owner 查询的最小 durable disposition/history |
| `REQ-UC-EVO-047` stock upstream semantic coexistence | 目标仓库同时存在官方 `trellis-*` 与 Guru projection，用户用未命名的自然语言请求启动、澄清、检查、继续、收尾或其它同域动作 | 当前请求必须由 Guru 的唯一顶层 entry owner 分类；被抑制的 upstream semantic route 不得独立执行、提问、创建副作用或形成第二 gate。若平台已自动匹配 stock Skill，必须在 semantic 行为开始前 redirect/stop，并保持零重复副作用 |
| `REQ-UC-EVO-048` explicit upstream provider/maintenance | 用户明确要求 Trellis architecture reference、memory lookup、channel transport、bug retrospective 或受控 worker 能力，或直接点名 raw `trellis-before-dev`、raw `trellis-update-spec`、raw `trellis-meta`、raw common `trellis-check`；这些能力均不得取代 Guru semantic owner，raw `trellis-spec-bootstrap` 的 spec-boundary/bootstrap 请求也不属于可直接调用的 provider | raw common `trellis-check` 必须 redirect 到 `guru-check-task`；raw `trellis-spec-bootstrap`、raw `trellis-before-dev`、raw `trellis-update-spec` 与 raw `trellis-meta` 必须分别 redirect 到 Guru bootstrap、同一 `context_envelope` 派生的 Guru-owned `implementation_context`、RDT/Architecture/code-spec contribution-to-projection lifecycle 与 Guru lazy read-only reference/new-change owner，无法在 semantic 行为前隔离时统一返回 `upstream_suppression_blocked`。其余请求先由唯一 `stock-policy owner`（一个 global workflow owner，不是自然语言可自动匹配的 Skill）绑定 asset、scope、source identity、action、caller profile 与调用目的：`provider_only` 只允许 `trellis-channel` 返回 caller-bound transport result；`explicit_only` 只允许 `trellis-session-insight` 与 `trellis-break-loop` 返回显式历史查询或诊断结果，任何真实写入必须重新进入 Guru `new change` 或返回 exact active caller；`controlled_worker_provider` 必须使用 caller-bound profile，implementation worker 每次只能绑定 task-free 或标准 Phase 2 中的一个 implementation owner。普通自然语言不得直接触发 stock matcher；Guru workflow 在已绑定 caller、scope、source identity、profile 与 consumer 后对 provider/worker 的内部调用不属于该直接 dispatch，仍不得自行取得 semantic ownership；若请求实际要求其它文件/合同/产品变更，必须重新进入 Guru `new change`；不支持的重叠调用 fail closed |
| `REQ-UC-EVO-049` fresh install/existing migration stock policy | 以官方 Trellis CLI 作为外部 provider test stimulus 安装 Guru，或已有仓库经 official install/update/upgrade、preset reapply、workflow switch 迁移 | 在 Guru candidate 激活前建立 stock inventory 与 policy，按每个 asset 的 successor 和 suppression action 完成一次可验证投影；clean install 与 existing migration 不混用 terminal，迁移前 active/history 能力不得因移除 stock 文件丢失。这里的 CLI 命令、参数、输出与退出码属于 pinned upstream provider facts，不是本产品新增的 CLI contract |
| `REQ-UC-EVO-050` upstream update/reapply/user modification | 以官方 Trellis CLI/template 变化、`trellis update --force/--create-new`、fresh `trellis init`、preset reapply，或用户修改/删除 stock 文件作为外部 provider test stimulus | 重新读取 upstream provenance 与 live file state；预期删除、patch、`.new/.bak`、用户修改和未知 asset 各有明确结果。不能证明安全抑制或 capability successor 时 fail closed，不覆盖用户修改、不留下未处理 sidecar 或 mixed semantic graph。命令语义不在 Guru 需求中重定义；若后续要新增/改变 Guru CLI 入口，必须重新建立 CLI authority 与 `CLI-INTENT` |

#### F. Base 与 repository SSOT lifecycle

| 场景 | 触发 | 目标结果 |
| --- | --- | --- |
| `REQ-UC-EVO-040` pre-task base refresh | selected base authority 存在但落后于其 exact upstream current | 在读取 Intake authority 前安全刷新选定 authority；不修改 detached/dirty invocation checkout、不回退其它 base，失败时明确 blocked |
| `REQ-UC-EVO-041` repository SSOT bootstrap/repair | 新仓库或已有仓库的 Requirements/Design/Test、Architecture Baseline、导航/投影缺失或不完整 | 在业务 task 继续前建立或修复唯一 current repository authority；draft/inferred 内容不冒充 confirmed current |
| `REQ-UC-EVO-042` task 消费并演进 RDT authority | 任一 standard task 进入 Planning；或 reviewed task delta 新增、修订、替换或删除 repository Requirements/Design/Test 事实 | 先回读并绑定 parent repository current RDT，完成影响分类；task planning 只引用 current 事实并承载 task-local delta/contribution，保持 requirement -> design -> test 追踪；shared current 只经独立、串行 promotion 前进 |
| `REQ-UC-EVO-043` parent repository 含 Git submodule | `.gitmodules` 或 mode `160000` gitlink 存在，且当前请求没有显式要求对该 submodule repository 单独开展工作 | parent task 的 authority、RDT、代码、状态、dirty/clean、验证和资源范围均排除 submodule；不得自动 init/update/checkout/sync/递归扫描，submodule 缺失或异常不得阻塞 parent task |

### 1.5 核心能力定义

#### 1.5.1 候选池与取舍

| `candidate_name` | `source_req_refs` | `decision` | `decision_rationale` |
| --- | --- | --- | --- |
| 意图到交付的 authority 与 route 连续性 | `REQ-UC-EVO-001..007,015..016,019..022,024..041,043..046,051` | `selected` -> `EVO-CAP-001` | 直接决定请求能否忠实、唯一地到达正确终点；来源冲突、scope/identity freshness、invocation/lifecycle entry 互斥、direct-answer terminal、active disposition、语义确认的 exact-action 授权边界、owner/re-entry、submodule scope 边界和不可逆副作用恢复可独立造成断链或错误交付；后续设计必须展开 authority resolution、route 状态与 terminal correctness，但不代替 RDT/Architecture 各自的 shared-current 生命周期 |
| Repository RDT SSOT 驱动与受治理演进 | `REQ-UC-EVO-001..003,006..007,015..016,019..030,034..036,040..043` | `selected` -> `EVO-CAP-002` | task planning 冒充或绕过 repository RDT 时，即使 route、Architecture 和工具执行都正常，产品/设计/测试语义仍会与 shared current 脱节；false-no-impact、跨 R/D/T 追踪、持续回写、serialized promotion、并行 contribution 与 downstream freshness 具有独立一致性和高返工风险，后续设计必须单独展开 |
| Architecture-aware Planning 与受治理演进 | `REQ-UC-EVO-008..016,019,022..026,028..029` | `selected` -> `EVO-CAP-003` | 不在 design 首稿前消费 baseline，或下游使用 stale alignment/proposal 状态，都会破坏核心目标；冲突、shared promotion 与跨阶段 freshness 具有动态决策、一致性和高返工风险；需独立展开 |
| 低成本且不中断的执行连续性 | `REQ-UC-EVO-017..018,030..033,045..046,051` | `selected` -> `EVO-CAP-004` | 当前观测已显示重复判断、输出规模、等待和压缩会使正常工作无法完成；普通信息请求被迫进入 change lifecycle、清晰肯定后仍要求固定口令/identity 复述，或 active lifecycle 无法以明确 disposition 收敛，都会产生额外成本和断链；执行成本、上下文生命周期、语义确认、恢复和最新意图连续性需与 `EVO-CAP-001` 的 authority/terminal correctness 分开展开 |
| 固定 Skill/Issue 列表 | 全局 | `dropped` | 是设计和实施拆分，不是业务结果；预先固化会让需求耦合 current 实现 |
| schema/digest/locator 体系 | 全局 | `dropped` | 可能是局部实现机制，不直接构成用户价值；只有被后续设计证明为最小必要机制时才可采用 |
| 完整过程审计包 | `REQ-UC-EVO-030` | `dropped` | 可由 current authority/live facts 重建的过程数据没有直接 consumer，反而扩大上下文；只保留不可重建的最小 durable result |
| 跨平台投影一致性 | `REQ-UC-EVO-034..036` | `dropped`（作为独立核心能力） | 是所有核心能力的交付约束，由 `EVO-NFR-012..015` 承接；缺少独立业务价值链，不单列核心能力 |
| 恶意 artifact/actor 防御 | 全局 | `dropped` | 本产品面向 honest-but-fallible 协作；恶意伪造、对抗输入、未要求的锁/TOCTOU 不是本轮正常场景 |

防膨胀复核：虽然 `P0/P1` 超过 3 项，但保留 4 个 `P0` 不是按文档、模块或流程环节拆分。
四者分别负责“意图与 route 正确”“repository 产品/设计/测试语义正确”“架构正确”和
“执行可持续”，每一项都有独立主价值链、shared-current/状态难点和 Design/Test 展开空间；
任一缺失，即使其余三项全部通过，`EVO-001..007` 仍不能在同一 exact candidate 上成立。
RDT 与 Architecture 是语义不同且生命周期独立的两类 repository shared authority，不能互相
替代，也不能继续由泛化的 authority 连续性吞并。其余候选均下沉为普通需求、非功能约束
或后续设计机制，不再拆分派生核心能力。

#### 1.5.2 `EVO-CAP-001` 意图到交付的 authority 与 route 连续性

| 字段 | 内容 |
| --- | --- |
| `capability_id` | `EVO-CAP-001` |
| `capability_name` | 意图到交付的 authority 与 route 连续性 |
| `capability_level` | `top_level` |
| `parent_capability_refs` | 无 |
| `priority` | `P0` |
| `business_outcome` | 用户意图、accepted scope、已审阅设计承诺和交付状态在每个阶段保持忠实、current、可追踪，并由唯一 owner/route 到达正确终点 |
| `value_chain` | 请求/Issue -> requirement/change readiness -> exact scope/identity -> approved planning -> implementation/check/review -> publication/delivery -> Finish/history |
| `difficulty_focus` | 多来源冲突、submodule scope 排除、scope/identity freshness、精确行动的 dialogue-local 语义确认、唯一 owner/consumer、最早受影响点重入、不可逆副作用后的 forward recovery |
| `complexity_source` | 动态语义判断、跨阶段状态黏着、外部 Git/GitHub/Trellis facts、一致性与恢复边界 |
| `design_focus` | current authority resolution、语义依赖传播、阶段状态、唯一 owner/consumer、re-entry 与 terminal route |
| `design_expansion_requirement` | 展开 normal/revision/stale/blocked/recovery 状态、authority 读取与 submodule scope 边界、scope/identity freshness、完整计划后的 AI 语义确认与 exact-action 授权隔离、不可逆动作边界、terminal correctness 和并行隔离；RDT 与 Architecture shared-current lifecycle 分别由 `EVO-CAP-002`、`EVO-CAP-003` 展开 |
| `risk_if_missed` | 产品意图被改写、重复 intake、错误关闭 Issue、阶段断链或错误交付 |
| `success_metrics` | 在同一个 exact-candidate Release gate 时间窗内，以 `EVO-FIX-ENTRY-ROUTING`、`EVO-FIX-REQUEST-STOP`、`EVO-FIX-ACTIVE-DISPOSITION`、`EVO-FIX-INTAKE-CLEAR`、`EVO-FIX-INTAKE-REVIEWED-DESIGN`、`EVO-FIX-INTAKE-UNCLEAR`、`EVO-FIX-NO-ISSUE`、`EVO-FIX-TASK-FREE`、`EVO-FIX-TECH-REVISION`、`EVO-FIX-DETACHED-READ`、`EVO-FIX-CHANGE-REQUEST`、`EVO-FIX-BASE-REFRESH`、`EVO-FIX-BASE-EVOLUTION`、`EVO-FIX-BRANCH-FINDING`、`EVO-FIX-FULL-NORMAL`、`EVO-FIX-NONE`、`EVO-FIX-PROVIDER-RECOVERY`、`EVO-FIX-FINISH-RECOVERY`、`EVO-FIX-HISTORY-RESUME`、`EVO-FIX-LATEST-INTENT`、`EVO-FIX-SUBMODULE-BOUNDARY` 和 `EVO-FIX-SEMANTIC-CONFIRMATION` 各至少 1 条 exact trace 为样本；全部通过，且 direct answer 误入 mode/lifecycle 或遗漏回答、顶层或 distribution 二级 route 重叠、需求静默漂移、unmapped route、submodule scope 泄漏、固定确认口令/identity challenge/脚本确认解析、确认跨 action 扩张、不可逆动作重放、Finish/Cleanup 或 disposition cleanup 重放、material additive 修改 in-flight/published candidate、pending intent 无 consumer，或 post-remote pending intent 被错误默认 new change均为 0 |
| `failure_impact` | 即使局部工具通过，也不能把结果定义为正确交付 |
| `acceptance_bar` | 每个支持场景都有唯一 current authority、唯一下一 owner/终点和可复现验收证据 |
| `validation_strategy` | invocation/lifecycle preclassification 与 entry、distribution action 两级互斥、direct answer、显式 stop、active lifecycle disposition、change-readiness 全结果、authority conflict、scope change、equivalent publication、owner-local/material additive/override/independent request 分流、post-remote pending intent 的六类顶层重分类、submodule scope 排除、base/provider recovery、完整 current 计划后的清晰语义肯定/疑问限制修改拒绝/material drift 与 exact-action scope、两种 delivery route、Finish/Cleanup partial recovery、Release confirmation 缺失/拒绝/stale 分流、published-unverified terminal 与唯一 consumer/stop fixtures；RDT/Architecture correctness 由对应独立核心能力 fixture 证明 |
| `source_req_refs` | `REQ-UC-EVO-001..007,015..016,019..022,024..041,043..046,051` |
| `evidence_refs` | `EVO-EVD-001,EVO-EVD-003,EVO-EVD-004,EVO-EVD-008,EVO-EVD-009,EVO-EVD-011,EVO-EVD-015,EVO-EVD-016,EVO-EVD-017,EVO-EVD-018,EVO-EVD-019,EVO-EVD-020,EVO-EVD-021,EVO-EVD-022,EVO-EVD-023,EVO-EVD-024,EVO-EVD-026,EVO-EVD-027,EVO-EVD-029,EVO-EVD-030,EVO-EVD-032,EVO-EVD-038,EVO-EVD-042` |
| `priority_score` | 业务影响 5 / 系统复杂度 5 / 失败成本 5，总分 15 |
| `priority_rationale` | 它承载意图到 terminal result 的 authority/route 主线；没有连续 authority 与唯一 route 即无法定义交付正确 |
| `counterfactual_check` | 不能延期；延期后仍会出现产品意图漂移或生命周期断链，本轮进化不能算成功 |
| `confirmation_status` | `user_confirmed_with_edits` |
| `open_questions` | 无 |

#### 1.5.3 `EVO-CAP-002` Repository RDT SSOT 驱动与受治理演进

| 字段 | 内容 |
| --- | --- |
| `capability_id` | `EVO-CAP-002` |
| `capability_name` | Repository RDT SSOT 驱动与受治理演进 |
| `capability_level` | `top_level` |
| `parent_capability_refs` | 无 |
| `priority` | `P0` |
| `business_outcome` | Repository Requirements/Design/Test 是唯一 shared 产品、设计与测试 authority；每个 standard task 在写作和执行前实际消费 current RDT，并以稳定 locator/identity/order 与 task 三件套的 task-local delta/projection 形成主要上下文，只通过 task-local contribution 与受治理 promotion 完善 shared current |
| `value_chain` | bootstrap/current RDT -> 稳定 authority context -> pre-read/impact -> task-local projection/contribution -> Planning/Implementation 持续回写 -> independent review/serialized promotion -> 受影响的 Phase 2/full-diff review/delivery freshness -> Finish |
| `difficulty_focus` | `rdt_no_impact`、`rdt_aligned`、`rdt_contribution_required`、`rdt_authority_blocked` 的真实判定，R/D/T 追踪，稳定 locator/identity/order 与最小变化 tail，task 三件套的非 authority 边界，Implementation 中间发现回写，promotion conflict，并行 task 与 material/identity-equivalent freshness |
| `complexity_source` | 多文档语义一致性、shared current 与 task candidate 分离、跨阶段状态黏着、single-writer promotion、并行 contribution 和高返工风险 |
| `design_focus` | RDT current authority/identity、cache-friendly stable context prefix 与 live-delta tail、impact 状态机、task planning projection 边界、contribution lifecycle、独立 review/promotion、下游 consumer 与最早受影响点重入 |
| `design_expansion_requirement` | 展开 Requirements/Design/Test 各自责任与追踪、稳定 locator/identity/order、bootstrap/repair、四类 impact exit、task-local candidate 的新增/修订/替换/拆分/合并/删除、AI owner 直接判断、持续回写、expected-current serialized promotion、并行隔离、downstream freshness、Finish 消费边界和 submodule 默认排除；不得把 task 三件套、cache 或中间 handoff 设计成平行 RDT |
| `risk_if_missed` | task planning 或代码事实冒充 shared RDT、false-no-impact 被批准、R/D/T 追踪断裂、多个 task 形成双 current、实现发现未回写，最终发布无法代表 repository current 产品语义 |
| `success_metrics` | 在同一个 exact-candidate Release gate 证据采集时间窗内，以 `EVO-FIX-SSOT-BOOTSTRAP`、`EVO-FIX-PLAN-NORMAL`、`EVO-FIX-RDT-LIFECYCLE`、`EVO-FIX-RDT-DOWNSTREAM-FRESHNESS`、`EVO-FIX-PARALLEL`、`EVO-FIX-FULL-NORMAL`、`EVO-FIX-SUBMODULE-BOUNDARY`、`EVO-FIX-CLEAN-INSTALL`、`EVO-FIX-MIGRATION` 和 `EVO-FIX-RELEASE` 各至少 1 条 exact trace 为样本；全部通过，且 task-planning-as-RDT、handoff-as-RDT、cache-as-authority、错误 no-impact、stale downstream consumption、双 current、Finish 后补写 RDT 和 submodule authority 泄漏均为 0 |
| `failure_impact` | 即使 intent route、Architecture alignment 和工具执行都通过，也不能把 candidate 定义为目标 Guru Trellis |
| `acceptance_bar` | 所有 standard task 在首份 planning artifact 前绑定 current RDT，并让 AI owner 从稳定 RDT context 与 task-local delta 直接得到证据相符的唯一 impact；最终 approved plan、实现、review、delivery 与 terminal state 均消费 current binding 或合法 task-local contribution，shared current 只经独立串行 promotion 前进 |
| `validation_strategy` | bootstrap/repair、no-impact/aligned/contribution/blocked、错误自报 no-impact、稳定 RDT locator/identity/order 与最小 live tail、task-local projection 非替代性、无中间 handoff authority、Implementation 持续回写、review revision、expected-current conflict、serialized promotion、并行隔离、downstream freshness、migration/release 与 submodule boundary fixtures |
| `source_req_refs` | `REQ-UC-EVO-001..003,006..007,015..016,019..030,034..036,040..043` |
| `evidence_refs` | `EVO-EVD-004,EVO-EVD-006,EVO-EVD-008,EVO-EVD-009,EVO-EVD-010,EVO-EVD-020,EVO-EVD-043` |
| `priority_score` | 业务影响 5 / 系统复杂度 5 / 失败成本 5，总分 15 |
| `priority_rationale` | RDT 是跨 task 持续表达产品、设计和测试语义的唯一 shared authority；缺失该能力会让每个 task 的局部 PASS 与 repository 长期事实脱节 |
| `counterfactual_check` | 不能延期；延期后 task planning 仍可能冒充或绕过 RDT，即使其余核心能力完成，本轮文档中心转换仍失败 |
| `confirmation_status` | `user_confirmed_with_edits` |
| `open_questions` | 无 |

#### 1.5.4 `EVO-CAP-003` Architecture-aware Planning 与受治理演进

| 字段 | 内容 |
| --- | --- |
| `capability_id` | `EVO-CAP-003` |
| `capability_name` | Architecture-aware Planning 与受治理演进 |
| `capability_level` | `top_level` |
| `parent_capability_refs` | 无 |
| `priority` | `P0` |
| `business_outcome` | design 首稿由 AI owner 从 current Architecture Baseline/constitution/change contract 与 task-local design delta 直接建立，合法新需求既不被 baseline 吞掉，也能提出受治理的 Architecture 演进 |
| `value_chain` | requirement/reviewed design -> 稳定 Architecture authority context + task-local delta -> alignment/conflict/proposal -> implementation/check/review -> publication/acceptance/Finish freshness -> reviewed promotion 后受影响证明重算 |
| `difficulty_focus` | no-impact、正常承接、真实冲突、authority 不完整、稳定 locator/identity/order 与最小 live tail、新 decision、既有 decision/GAP/ownership 修订的区别 |
| `complexity_source` | 多 authority 一致性、原则取舍、shared current 串行演进、并行 task freshness |
| `design_focus` | 写作前消费点、cache-friendly stable Architecture prefix 与 task delta tail、alignment 主承载位置、proposal/ADR 判定、下游 current binding、shared promotion 与 downstream re-entry |
| `design_expansion_requirement` | 展开稳定 Architecture locator/identity/order、impact 状态、AI owner 直接判断、conflict 决策、proposal lifecycle、各下游责任边界的 freshness、expected-current promotion、owner/single-writer/compatibility exit 与 fresh proof；不得另建 Architecture handoff/report authority |
| `risk_if_missed` | 首稿忽略 baseline、PRD 被架构改写、不必要 ADR、双 current、未经 review 的 shared Architecture 变更 |
| `success_metrics` | 在同一个 exact-candidate Release gate 证据采集时间窗内，以 `EVO-FIX-ARCH-NO-IMPACT`、`EVO-FIX-ARCH-ALIGNED`、`EVO-FIX-ARCH-CONFLICT`、`EVO-FIX-ARCH-INCOMPLETE`、`EVO-FIX-ARCH-NEW-DECISION`、`EVO-FIX-ARCH-REVISION`、`EVO-FIX-ARCH-NO-ADR`、`EVO-FIX-FRESH-EQUIVALENT`、`EVO-FIX-FRESH-SCOPE`、`EVO-FIX-ARCH-DOWNSTREAM-FRESHNESS`、`EVO-FIX-ARCH-PROMOTION`、`EVO-FIX-PARALLEL` 各至少 1 条 exact trace 为样本；全部通过，且首稿未读 current authority、Architecture-handoff-as-authority、cache-as-authority、Planning 直接写 shared current、不必要 ADR、下游消费 stale Architecture binding 均为 0 |
| `failure_impact` | 架构方法论无法被贯彻，后续重构版即使完成发布动作也不是目标产品 |
| `acceptance_bar` | Architecture 场景 fixture 全覆盖；AI owner 从 current baseline 与 task-local delta 自主形成判断，最终 approved plan 与 current baseline 对齐或包含明确、受治理的 evolution proposal |
| `validation_strategy` | stable Architecture context + live-delta tail、no-impact、aligned、conflict、missing/stale、new decision、existing decision revision、unnecessary handoff/report、downstream freshness 与 parallel promotion fixtures |
| `source_req_refs` | `REQ-UC-EVO-008..016,019,022..026,028..029` |
| `evidence_refs` | `EVO-EVD-001,EVO-EVD-004,EVO-EVD-020,EVO-EVD-043` |
| `priority_score` | 业务影响 5 / 系统复杂度 5 / 失败成本 5，总分 15 |
| `priority_rationale` | Architecture Baseline 方法论是最终发布必须贯彻的产品目标，不是可延期增强 |
| `counterfactual_check` | 不能延期；延期后仍只能产后审核 Architecture，无法证明首稿承接 current baseline |
| `confirmation_status` | `user_confirmed_with_edits` |
| `open_questions` | 无 |

#### 1.5.5 `EVO-CAP-004` 低成本且不中断的执行连续性

| 字段 | 内容 |
| --- | --- |
| `capability_id` | `EVO-CAP-004` |
| `capability_name` | 低成本且不中断的执行连续性 |
| `capability_level` | `top_level` |
| `parent_capability_refs` | 无 |
| `priority` | `P0` |
| `business_outcome` | 正常工作以 RDT、Architecture 与 task 三件套形成稳定、可缓存的主要上下文，由 AI owner 自主判断和执行，显著更短、更快、更安静；异步等待、压缩或恢复后仍优先消费最新用户意图且不中断当前工作 |
| `value_chain` | stable authority prefix -> 最小 live-delta tail -> AI-owned 判断/执行 -> 紧凑交互 -> 阶段 evidence 卸载 -> 增量 wait/compression/resume -> 最新意图消费 -> current owner 继续 |
| `difficulty_focus` | 利用稳定上下文减少重复 semantic work、全文回读、事务交接、固定确认挑战和上下文注入，同时保持证据充分、freshness、最新意图和当前 owner 连续性 |
| `complexity_source` | model/tool 往返、长输出、异步等待、context compression、跨平台对话/工具运行约束 |
| `design_focus` | 稳定 authority prefix/最小变化 tail、正常路径 AI-owned action/consumer 边界、必要 evidence 生命周期、对话/工具增量协议、最新意图优先级和恢复所需最小信息 |
| `design_expansion_requirement` | 展开 stable locator/identity/order、cache-friendly context construction、可删除/必须保留的信息与动作、AI owner 自主判断、完整计划后的 dialogue-local 语义确认、长运行增量结果、override/additive 意图顺序、quiet update 和诊断观测方法；不得把 cache hit、诊断数值、plan digest、人类式 assignment/signoff 或 transaction handoff 升级为 authority、验收或授权门槛；terminal delivery correctness 由 `EVO-CAP-001` 承接，RDT/Architecture 证据充分性分别由 `EVO-CAP-002`、`EVO-CAP-003` 承接 |
| `risk_if_missed` | 流程形式正确但实际无法高效完成，压缩/等待后失联，用户被内部状态淹没 |
| `success_metrics` | 在同一个 exact-candidate Release gate 证据采集时间窗内，以 `EVO-FIX-ENTRY-ROUTING`、`EVO-FIX-PLAN-NORMAL`、`EVO-FIX-FULL-NORMAL`、`EVO-FIX-HISTORY-RESUME`、`EVO-FIX-ACTIVE-DISPOSITION`、`EVO-FIX-LATEST-INTENT`、`EVO-FIX-LONG-OUTPUT`、`EVO-FIX-SEMANTIC-CONFIRMATION` 各至少 1 条 exact trace 为样本；direct answer 误入 mode/lifecycle/未支持 specialist profile、遗漏回答、live fact 不可用时虚报 current、无 consumer 的中间文件、human-style assignment/signoff/transaction handoff、already-current fact restatement、重复注入 unchanged authority/cumulative stdout、invalid wait、固定 prompt/口令/hash/digest/identity/摘要复述要求、脚本确认解析或持久化、未消费/丢失/重排最新用户意图、generic override 或 post-remote material additive 绕过 entry selection、错误默认 new change、无唯一 consumer 的 `additive_change_pending`、cleanup 拒绝产生多终点、零资源 abandonment 不可达、disposition cleanup 后 history 不可查询，以及 active disposition 无 terminal/re-entry 均为 0，且每项保留的 handoff、脚本运行、文档重读和重复 gate 都能指向不可替代的直接 consumer 或 correctness 责任。不以 cache hit、相对 baseline 的耗时、rounds、bytes 或 compression 数值作为 PASS/FAIL 条件 |
| `failure_impact` | 本轮“显著更短、更快、更安静”和执行连续性目标失败 |
| `acceptance_bar` | normal planning 与 request-to-cleanup 路径以稳定 RDT/Architecture/task context 和最小 live tail 驱动，不存在无消费者交接、人类式事务交接、固定确认挑战、already-current fact 复述、重复 unchanged 正文/累计输出注入或无责任归属的脚本/gate；功能、Architecture、review 与 delivery 的证据充分性不因路径精简而降级 |
| `validation_strategy` | 对 `EVO-FIX-ENTRY-ROUTING`、`EVO-FIX-PLAN-NORMAL`、`EVO-FIX-FULL-NORMAL`、`EVO-FIX-HISTORY-RESUME`、`EVO-FIX-ACTIVE-DISPOSITION`、`EVO-FIX-LATEST-INTENT`、`EVO-FIX-LONG-OUTPUT`、`EVO-FIX-SEMANTIC-CONFIRMATION` 与声明平台等价运行执行 action/consumer trace；覆盖 stable authority prefix/minimal live tail、cache unavailable 时结果等价、AI-owned judgment、lifecycle-bound/independent user intent preclassification、普通 direct answer 的最小读取/零资源路径、通用只读 review 与两个受支持 specialist profile 的互斥、live read unavailable 诚实完成、完整 current 计划后的多种清晰肯定与疑问/限制/修改/拒绝/material drift、exact-action scope isolation、无副作用/可逆本地/不可逆远端副作用下的 active disposition、零 deletable resource abandonment、cleanup 拒绝的唯一 choice、cleanup 后 disposition history query 与 generic override、owner-local additive、不可逆远端副作用前后的 material additive、post-remote pending intent 六类顶层重分类与唯一 consumer 消费，并识别可删除交接、事务交接、固定确认 challenge、事实复述、重复读取、重复判断、不必要脚本/验证和累计输出，不设置 cache-hit 或相对性能改善门槛 |
| `source_req_refs` | `REQ-UC-EVO-017..018,030..033,045..046,051` |
| `evidence_refs` | `EVO-EVD-001,EVO-EVD-002,EVO-EVD-003,EVO-EVD-007,EVO-EVD-008,EVO-EVD-011,EVO-EVD-016,EVO-EVD-017,EVO-EVD-018,EVO-EVD-019,EVO-EVD-020,EVO-EVD-021,EVO-EVD-023,EVO-EVD-024,EVO-EVD-026,EVO-EVD-027,EVO-EVD-029,EVO-EVD-030,EVO-EVD-032,EVO-EVD-038,EVO-EVD-042,EVO-EVD-043` |
| `priority_score` | 业务影响 5 / 系统复杂度 5 / 失败成本 5，总分 15 |
| `priority_rationale` | 当前诊断已证明成本和连续性会直接阻止交付完成，而非仅影响体验 |
| `counterfactual_check` | 不能延期；若只重排 owner 而不降低成本和断链，目标产品仍未完成 |
| `confirmation_status` | `user_confirmed_with_edits` |
| `open_questions` | 无 |

### 1.6 场景编号与入口追踪

本产品范围无独立 UI 页面、无服务端 API contract，也不新增或改变 Guru 自有的用户 CLI
command contract。该结论依据 `requirement-doc-standard` 第 5.1 节的 API/CLI 适用标准。
shared `.agents/skills` projection layer 与 Codex、Claude、Cursor 的 prompt/command/Skill
入口属于同一个 conversational workflow product entry；shared layer 不是独立 host，也不
重复计数。`trellis init`、`trellis workflow`、`trellis update`、`upgrade` 及其
`--force`/`--create-new` 仅在 `REQ-UC-EVO-034..036`、`REQ-UC-EVO-049..050` 及对应
fixture 中作为固定版本的外部 provider test
stimulus；其命令名、参数、stdout/stderr、退出码、update/backup 语义由官方 package/source
authority 拥有，Guru 只记录调用目的、输入 identity、观察到的结果和未验证边界，不重新定义或
发布这些 CLI contract。若后续目标变为新增/修改 Guru CLI 入口，必须回到 Requirements 建立
`requirement-cli-command.md` 与稳定 `CLI-INTENT-*`，不得沿用本段“不适用”结论。

| 场景范围 | 入口类型 | API intent | CLI intent | 非功能主定义 |
| --- | --- | --- | --- | --- |
| `REQ-UC-EVO-001..051` | conversational workflow（shared `.agents/skills` projection layer + Codex/Claude/Cursor 三个 supported host） | 正常不映射：无服务端 API contract | 正常不映射：本轮不新增/改变 Guru CLI contract；`REQ-UC-EVO-034..036`、`REQ-UC-EVO-049..050` 的 Trellis CLI 仅是外部 provider test stimulus，不形成 Guru CLI intent | [`requirement-non-functional.md`](./requirement-non-functional.md) |

编号差集：API intent 为空；Guru CLI intent 为空。二者均属于整体不适用，不是
`UC-接口映射豁免`；真实豁免 0，缺失映射 0。外部 Trellis CLI 的 provider facts 不进入该差集。

## 2. 入口组织结构

页面组织不适用。目标入口按用户意图组织，而不是按平台复制流程：

| 入口 | 承接场景 | 摘要 |
| --- | --- | --- |
| direct answer entry | `REQ-UC-EVO-045`；`REQ-UC-EVO-048` 的 standalone 只读 provider 子场景 | 普通解释、事实、状态、信息或通用只读分析/审核请求；执行规则见第 3、6 章 |
| new change entry | `REQ-UC-EVO-001..005,033,039` | 新产品、文档、合同或代码变更意图；standard/task-free 二级 mode 由第 3 章主定义，第 6 章只投影其状态与回程 |
| resume/recovery/history entry | `REQ-UC-EVO-006,030,046` | unfinished lifecycle 的继续、技术修订、中断恢复、active disposition 或 durable history query 请求；具体分支见第 3、6 章 |
| distribution/release entry | `REQ-UC-EVO-034..036` | exact candidate 的平台投影、安装、迁移验证或 Release 请求；具体 route 见第 3、6 章 |
| explicit specialist review entry | `REQ-UC-EVO-037..038` | contract wording review-only 与 normal-scenario qualification 两个受支持 profile；caller 与结果见第 3、6 章 |
| stop entry | `REQ-UC-EVO-044` | 未进入 active lifecycle 的显式撤回、拒绝继续或零动作结束请求 |
| stock policy/provider/maintenance boundary（非独立 semantic entry） | `REQ-UC-EVO-047..050` | stock policy、provider 与 maintenance 相关的边界事实和调用请求；owner、caller 与结果见第 3、6 章 |
| in-flight lifecycle event（非顶层入口） | `REQ-UC-EVO-007..029,031..032,040..043` | 已绑定 lifecycle 内的 authority、base、finding、provider、latest-intent、long-run、RDT 或 submodule 变化；处理规则见第 3、6 章 |

入口之间的关系、二级 mode、适用与互斥条件的产品主定义见[第 3 章](#3-功能需求)；第 6 章
只把这些主定义投影为统一的状态、回程与终点闭环。本节只提供入口层级与范围摘要。

shared layer 加上 Codex、Claude、Cursor 是同一个 conversational workflow 的入口投影。
shared layer 只是一份官方投影来源，三个 host 才是本候选的 supported runtime host；入口的
可执行规则与产品语义统一由[第 3 章](#3-功能需求)定义，第 6 章仅提供对应的 route、re-entry
与 stop 状态投影。

## 3. 功能需求

### 3.1 Authority、Intake 与 Workspace

- `EVO-REQ-001`：target Requirements 与 current runtime authority 必须明确分离；任何
  未实现目标不得被 current 文档、状态或发布说明冒充为已实现。
- `EVO-REQ-002`：进入 `new change -> standard change` 的 requirement Intake invocation 必须读取
  当前用户请求、live Issue 正文/必要评论、parent repository current Requirements/Design/Test 及其
  适用的 authoring/review/lifecycle contract，以及完成 requirement 判断所需的 Git/GitHub/Trellis
  live facts；这里的“Intake”只指 standard change 的 requirement-authoring/readiness 步骤，不是
  所有 top-level route 的通用前置步骤。direct answer、task-free、resume/recovery/history、
  distribution/release、specialist 与 stop route 只按 `EVO-REQ-026` 的 applicability 绑定回答或
  受影响 surface 所需的最小 facts；同一 invocation 复用已有 projection，不得因进入其它 route
  而全文读取 parent RDT。不得把 task planning、旧会话摘要、候选 Issue body 或 submodule 内容当作
  parent repository current RDT authority，也不得在 Phase 0 提前执行 Architecture impact/alignment。
  current Architecture 的实质消费属于 pre-design Planning。
- `EVO-REQ-003`：Issue 中的业务需求、约束、验收和已审阅设计承诺必须带来源保真分类；
  只有 live Issue/user authority 能证明已审阅状态时才分类为 reviewed-design commitment，
  否则按未审阅 proposal 处理；两者都不是 product requirement 或自动 current Architecture。
- `EVO-REQ-004`：来源充分且一致时不得例行提问；存在实质歧义时每轮只问一个能最大幅度
  收敛范围/验收/冲突的最高价值问题，直到 requirement authority 足以进入下一阶段。
- `EVO-REQ-005`：来源冲突必须先被显式呈现；用户对该冲突给出的最新明确选择成为当前 task
  requirement authority。若它改变 live Issue/共享 requirement intent，必须保留 provenance
  和待同步 delta，不能静默改写 Issue、猜测优先级或丢弃旧 authority。
- `EVO-REQ-006`：`prd.md` 首先表达业务目的、行为、范围和验收；不得为了适配 current
  Architecture、当前实现或实现便利而静默修改、弱化或反转产品意图。
- `EVO-REQ-007`：Phase 0 必须产出可被后续计划作者直接消费的 current requirement
  authority 和 reviewed-design commitments，但不得为此强制制造长期 handoff 文件；其
  持久位置由后续 Design 在满足 SSOT/生命周期约束下决定。
- `EVO-REQ-008`：产品需求未发生语义变化时，design/implementation/metadata 的技术修订
  不得重新进入 Intake，也不得重复询问已确认问题。
- `EVO-REQ-009`：Phase 0 读取 exact current base authority 不以 invocation checkout
  clean、branch-bound 或等于 selected base 为前提；不得只为读取 authority 创建临时
  worktree。authority 本身缺失、歧义或不可证明 current 时仍须 fail closed。
- `EVO-REQ-010`：每个通过 admission boundary 的用户 invocation 必须先由当前请求与完成分流所需的最小 live facts，恰好选择
  `direct answer`、`new change`、`resume/recovery/history`、`distribution/release`、`specialist review`
  或 `stop` 之一；若选择 `new change`，再恰好选择 `standard change` 或 `task-free change`。互斥分类规则为：
  只要求普通解释、事实、状态、信息答案或不绑定 active lifecycle 的通用只读分析/审核，且不要求修改
  被审对象、`REQ-UC-EVO-037..038` 的受支持 specialist profile、distribution/release action、继续/恢复/
  处置 active lifecycle，或通过 durable history contract 解析 archive/finish/disposition result 时，属于
  `direct answer`。Issue、task、branch、repository、Requirements、Design、代码或 Architecture 只是问题
  主题，不能把只读请求改分类为 change 或 specialist；direct answer 只读取形成真实答案所需的最小
  live facts，不创建 Issue/task/worktree、不进入 `change_mode_selected` 或启动 lifecycle。若正常
  provider/repository 读取失败、拒绝访问或返回不完整，使所需 live fact 无法核实，答案必须明确标记
  哪项事实 `unavailable`/`unverified` 及其边界，不得猜测或声称 current；该诚实结果仍得到
  `direct_answer_completed -> workflow_completed`，后续重试是新的 direct-answer invocation。
  `REQ-UC-EVO-048` 的 stock 请求不构成第七类 top-level route。Guru-owned lazy Trellis reference，
  以及 exact `explicit_only` 的 `trellis-session-insight` history query / `trellis-break-loop` 只读诊断，
  在没有 active lifecycle、文件变更或 authority 变更时归入 `direct answer`；只有这两项 exact
  explicit-only 子步骤可以得到 `explicit_provider_result_current`（结果可以携带 `unavailable`/
  `unverified` 边界），再由 direct-answer owner 完成。direct-answer owner 若需要 caller-bound
  `trellis-channel` transport 或 research/check worker observation，必须先绑定 exact caller/profile/
  consumer，并只消费 `provider_result_current -> returned_to_unique_caller`；它们不得冒充
  `explicit_provider_result_current` 或 standalone provider terminal。implementation worker execution、
  任何 spec/Issue/文档/代码写入或其它 authority 变更都归入 `new change`，或在已绑定 active caller
  时只返回该 caller 的 route-local result；写入意图必须在 raw explicit asset invocation 前完成该
  分类，不得把 provider result 当作 standalone completion。越界 authority/产品/合同变更始终重新
  进入 `new change`，provider 只能返回 `provider_boundary_blocked` 或 caller-owned result。
  要求返回 workflow-owned archive/finish/disposition durable result 且需解析其 identity/currentness 时
  仍属于 history route。要求新增/修改产品、文档、合同或代码，且不
  绑定 unfinished lifecycle 时属于 `new change`；继续、恢复、
  技术修订或处置一个 exact unfinished lifecycle 属于 `resume/recovery/history`；旧 lifecycle 已 terminal
  而当前请求要求新修改时仍属于 `new change`，旧 history 只作为 evidence；验证、安装、迁移或发布
  已选 exact candidate 属于 `distribution/release`，但修改 distribution/install/release 合同或代码本身
  属于 `new change`；只有当前请求明确属于 `REQ-UC-EVO-037` 的 contract wording review-only，或
  `REQ-UC-EVO-038` 的 supported normal-scenario qualification，且固定 review scope 不要求修改被审
  对象、review 结果本身不会静默改变产品、文档、合同或代码时，才属于 `specialist review`。不得仅凭
  “有界 semantic review”把 Requirements/Design/代码/Architecture 等其它通用只读审核扩张为未定义
  specialist profile；这些请求若不绑定 active lifecycle 且不要求修改，仍属于 direct answer。只要用户
  要求采纳 wording revision、
  修改被审对象，或文字本身就是本次交付范围，顶层分类必须是 `new change`；wording reviewer
  可以作为该 active change caller 的嵌入 owner，但其 `content_changed` 不得被当成 top-level
  specialist terminal。只有尚未绑定需要处置的 active lifecycle、且本 invocation 尚未产生新副作用时，
  显式撤回、拒绝继续或要求不执行任何动作才属于 `stop`。取消、放弃或清理既有 active lifecycle
  必须先经 `resume/recovery/history` 解析 exact current work，再由其 current owner 按 `EVO-REQ-067`
  的副作用与 disposition/cleanup 合同处理，不得用 top-level stop 绕过 owner。分类仍有实质歧义时只询问一个最高价值问题，并在
  收敛前保持 side-effect-free。每个可能启动顶层 invocation 的用户输入（通常是一条用户消息）在进入 source-stimulus ranking 或生成
  `request_received` 前，必须先经过 `lifecycle_intent_preclassification`。只有同时存在且仍
  current 的 exact active invocation/lifecycle identity、唯一 current phase/owner、受影响 scope
  与 candidate/remote-boundary identity、host session/user-event identity、单调到达序列，以及由
  active invocation 的 wait/response/continuation facts 证明的因果绑定，才可判定为
  `lifecycle_bound_user_intent`。该事件是 in-flight lifecycle event，不属于六类 source stimulus
  或 top-level route；它本身只回 current/最早受影响 owner，按 `EVO-REQ-047` 分类为 owner-local
  additive、material additive 或 override，绝不生成 `request_received`、`entry_route_selected`
  或 stock matcher dispatch。只有 bound `override` 在原 owner 完成停止、suspend 或不可逆远端
  收敛后，按 `EVO-REQ-047` 由唯一 request-entry consumer 启动的后续新 invocation 才能生成一次
  新的 receipt；该 receipt 属于新 invocation，不是 bound 事件的重复或延迟生成。没有 active lifecycle，或在 active lifecycle 存在时用户明确声明这是独立的新请求且当前消息已有唯一
  host `user-event identity`，或 live facts 明确证明该 user-event 与旧 lifecycle 的 wait/response/
  continuation、scope、candidate、owner 无因果关联且当前消息已有唯一 `user-event identity`，才可判定为
  `independent_user_request`。`user-event identity` 是每条消息在 preclassification 前的 host admission
  fact，不要求 host 预先创建新的 invocation identity；一旦判定独立，唯一 request-entry consumer 必须先建立新的 invocation
  identity 与 invocation-scoped `context_envelope`，再恰好生成一次 `request_received`。这里的
  `request_received` 只是本次 invocation 的 admission receipt，不代表已选择 top-level route；旧
  lifecycle 保持原 owner，除非用户同时明确请求其 override/disposition。receipt 之后必须先执行
  isolation safety gate：无 active lifecycle 时该 gate 立即 clear；有 active lifecycle 且处于非变更等待/确认，
  或共享 scope/不可逆动作已证明可安全隔离时，才进入 `pre_semantic_dispatch_guard` 并恰好选择一个 top-level
  route；有 active lifecycle 且共享可变 scope 或不可逆动作尚未安全隔离，则在 route selection 前形成可发现且有唯一 consumer 的
  `independent_request_isolation_pending`，绑定新 invocation、scope、旧 owner 和唯一 re-entry。该
  pending 不是第二个 top-level route，也不得让旧 owner 吞并或改写新请求；非变更等待/确认状态不得阻塞
  新请求。首次证明安全隔离的边界，或旧 owner 收敛为 current、forward-recovered current 或 terminal
  block 后，pending 只重入 `pre_semantic_dispatch_guard`，复用既有 envelope 和那一次 receipt，不再生成
  `request_received`。scope/owner 或安全隔离边界无法唯一解析时返回
  `independent_request_isolation_blocked` 与 exact re-entry；修复后重新评估 isolation，不得静默丢弃、无
  consumer pending 或无限等待。
  为避免在各个回程矩阵中重复展开，同一条完整顺序统一命名为
  `independent_invocation_entry_contract`：
  `new invocation identity -> invocation-scoped context_envelope -> exactly-one request_received`
  （只表示 admission receipt）`-> independent_request_isolation_gate -> pre_semantic_dispatch_guard`
  `-> entry_route_selected`。凡后文写“新的 invocation”“独立请求重新 entry”或“新的 request entry”，
  均只引用这条完整合同；isolation pending/blocked 的 re-entry 复用同一 envelope/receipt，不重新生成
  `request_received`。lifecycle-bound event 本身仍不生成 receipt、顶层 route 或 stock dispatch。
  active lifecycle 存在但上述因果/identity 证据既不能证明
  bound 也不能证明 independent 时，必须得到 `lifecycle_intent_binding_blocked`，只允许一次最高
  价值澄清或 exact live-fact repair 后回到该 preclassification；不得把消息降级为 ordinary new
  request，也不得把所有消息一律吞入 active owner。finding、base/provider 变化、latest intent 等已
  绑定 lifecycle 内事件只返回 current/最早受影响 owner，不重新执行顶层分流。在
  `entry_route_selected` 与适用的 `change_mode_selected` 完成前，不得开展方案性
  repository/domain semantic work、生成 task/planning 产物或执行 Git/GitHub/Trellis/submodule
  副作用。只有真实产品选择或即将发生的 Git/GitHub/Trellis 副作用才询问用户。
  `pre_semantic_dispatch_guard` 是进入上述 route 之前的非语义 admission boundary，只能识别
  source stimulus、精确 stock collision 和已绑定 caller 所需的最小 facts；它可以把命中重定向到
  Guru route，或在无法安全隔离时返回 role-local `upstream_suppression_blocked`、
  `provider_boundary_blocked` 或 `retained_context_blocked`。这些是合法的 pre-entry blocked/re-entry
  结果，不是第二个 top-level route，也不要求先伪造一个 route；它们必须有唯一修复 owner，且在
  admission boundary 内不得执行 Git/Trellis/file mutation、用户副作用确认交互、semantic question 或
  semantic gate。只有 admission clear/redirect 后的用户 invocation 才适用六类 exactly-one
  `entry_route_selected`；已选 route 内的 stock policy failure 由该 caller 形成 route-local
  blocked/re-entry，不重新执行顶层分流。
  若选择 `distribution/release`，还必须在任何 validation、installation、migration、tag 或 Release
  副作用前，按当前请求的 terminal intent、exact candidate 与目标 repository live current state，恰好
  选择 `standalone projection validation`、`clean repository installation`、`existing repository
  migration` 或 `exact-candidate Release` 之一并得到 `distribution_action_selected`：只要求验证既选
  candidate 的声明 projection surface、且不要求安装、迁移或发布时属于 standalone projection；请求的
  terminal outcome 是发布 exact candidate 时属于 Release，其 pre-publish projection/install/update
  检查只作为 Release caller 的内嵌 gate，不得把 invocation 改投其它 distribution owner。其它需要
  安装、更新、升级、preset reapply 或 workflow switch 的请求，必须先执行一次
  `distribution_state_preclassification`（只盘点 target live state，不产生副作用），再按以下互斥
  predicate 选择 action：`clean_target` 要求 active `.trellis/workflow.md` 缺失（不只是“没有 Guru
  current workflow”），且不存在任何可唯一归属的 official Trellis 或 Guru managed installation state：
  包括 official `.trellis/config.yaml`、`.trellis/.template-hashes.json`、scripts/spec/task/workspace 基础结构或
  manifest、`.trellis/guru-team/`、shared/host projection、未处理 `.new/.bak` sidecar、active/resumable
  lifecycle、archive/finish/history 或 retained ref。只有普通用户文件存在不影响 clean 分类；疑似
  Trellis/Guru surface 但 identity/owner 不可唯一时按 unknown/unowned blocked，不得猜测为普通文件。
  `existing_migration_target` 要求存在可识别的 Guru current，存在能唯一归属到一个 source/owner 的
  official Trellis installation footprint 或 partial/legacy Guru managed surface、sidecar、lifecycle、history
  或 ref（即使 workflow 与 Guru projection 均缺失），或存在 identity/provenance/owner 已唯一识别且本次安全 transition plan 已在
  当前对话中收敛的 non-Guru active workflow。前两类即使 `.trellis/workflow.md` 缺失也必须走 existing
  migration；第三类必须保留 foreign source workflow，直到 WORKFLOW-SWITCH 的唯一 cutover 才允许替换。
  若 active `.trellis/workflow.md` 明确为 non-Guru 但 transition plan 尚未 current，或其
  id/source/provenance/owner 无法唯一识别，先标记为独立的 `foreign_workflow` preclassification；已唯一
  归属 Guru 但 candidate/version 过期的 workflow 仍属于 `existing_migration_target`，不得误分类为
  foreign。`foreign_workflow` 在 provenance/ownership 与安全 transition plan 未经 clarification 或 live
  repair 唯一确认前，既不是 `clean_target` 也不是 `existing_migration_target`，必须得到 route-local
  `distribution_state_blocked` 并保持零副作用；确认后只重入 preclassification，并恰好转为
  `existing_migration_target`，不得要求先执行 workflow mutation 才能改变分类。若 target
  同时呈现 mixed/unknown/unowned/multiple identity，或无法唯一证明上述任一 predicate，则同样得到
  `distribution_state_blocked`，之后只重入 `distribution_state_preclassification`；不得把
  `foreign_workflow` 或 official/partial/legacy surface 猜测成 migration 或 clean install。`clean_target` 才选择 clean installation，
  `existing_migration_target` 才选择 existing migration；五个 migration cell 是否适用另按
  `EVO-REQ-054` 判定。一个请求同时表达多个独立 terminal outcome 时仍只询问一个最高价值问题，已绑定
  action 内的 finding/provider change 只返回该 action owner，不重新执行顶层或二级选择。
  `new change` 按定义必须具有明确的文件变更目标（产品、文档、合同或代码均可）。不包含文件变更
  的请求不得进入 `change_mode_selected`；它必须按上面的 direct answer、resume/recovery/history、
  distribution/release、specialist 或 stop 规则处理。若用户意图确实需要文件变更但目标或范围尚不清晰，
  只允许一次 scope clarification，choice current 前不得创建 mode/task/workspace 资源。
  对尚未进入 active-task route 的 file-changing 请求，standard/task-free 选择遵循以下产品边界：
  显式 task-free 意图直接进入 task-free candidate，不重复询问 mode，但不豁免 checkout suitability、
  applicable check、risk review 或副作用边界；无显式意图时，只有目标清晰、target path 有界、
  仅影响 current checkout、可逆、低风险，且高置信无需隔离 workspace、正式 Planning、committed
  full-diff review 或高风险验证的请求才自动进入 task-free。实质性 runtime 行为、跨层合同、public API、
  schema、CI、install/update、deploy、权限、安全或数据影响默认进入 standard；Issue 是否存在、
  文件数量、路径或关键词不得独立决定 mode。可能适用但 scope/risk 证据不足时只询问一次，
  相同 scope 的 mapped recovery/retry 复用 current 选择。
  task-free 只保留 invocation-local 的最小意图与检查结果，不生成正式 `prd.md`、`design.md`、
  `implement.md` 或 task/archive history，也不创建或触发 task/worktree/branch、commit、push、PR、merge、
  tag、Release、installation 或 cleanup。适用 check 产生可在原边界内修订的 finding 时，由同一
  task-free owner 修订并 fresh 重检；位置/active-task 事实要求恢复既有工作时返回对应 current
  owner；无法安全继续或 targeted check 无法收敛时明确 blocked，并报告实际 partial edit 与未验证
  边界；范围或风险不再有界时立即停止剩余 target 写入，把 exact partial edit 置为可发现的
  `task_free_escalation_pending`，再返回 standard workflow。该状态不得被自动提交、丢弃、复制或
  清理，并且必须由 `EVO-REQ-011` 的 Workspace owner 在任何标准资源副作用前取得精确确认后
  完成唯一归属的 reconciliation/isolation；无法安全收敛时明确 blocked。
- `EVO-REQ-011`：Workspace/task/branch 等资源只在 requirement readiness 成立且用户已
  确认精确副作用后创建；task/branch/worktree 名称必须绑定可用的 current change identity
  与语义动作，无 Issue 时不得伪造 Issue identity；资源准备不得反向拥有或重写 Intake 语义，
  也不得把 submodule init/update/checkout 或递归读取伪装成 parent task 的普通准备动作。若入口
  携带 `task_free_escalation_pending` 或其它 suspended local work，Workspace owner 必须先判断它与
  新 lifecycle 是同 scope 还是异 scope，并形成 exact transfer/reuse 或 isolation 计划；任何标准
  资源副作用前，该计划必须绑定 source work、target lifecycle、每项 edit 的预期唯一 owner、资源
  边界与待执行副作用，取得一次精确确认并得到 `suspended_work_plan_confirmed`。资源准备后，同
  scope 必须验证每项 edit 只有一个 current owner，得到 `suspended_work_reconciled`；异 scope 必须
  证明新资源与旧 work 隔离、旧 work 仍可发现并恢复，得到 `suspended_work_isolated`。具体转移
  机制由 Design 决定，但不得静默混入、重复实现、覆盖或遗失已有 edit；无法判定 scope、形成
  精确计划、取得确认或安全验证时 blocked，且不得进入 Planning。
- `EVO-REQ-059`：standard change 在创建资源前必须判断它是否为一个可独立交付单元，并基于
  live Issue/current/相关 archived change authority 处理 duplicate、linked prerequisite、scope
  overlap 与 readiness；每次判断必须恰好得到 `change_request_ready`、`active_duplicate_current`、
  `completed_duplicate_current`、`change_request_scope_clarification_required`、
  `change_request_prerequisite_blocked` 或 `change_request_resolution_blocked` 之一。ready 才能继续
  Workspace 准备；active duplicate 必须停止创建新 change/resource，把请求返回 exact unfinished
  lifecycle 的 current owner；completed duplicate 必须返回 current terminal/history result 并得到
  `workflow_completed`，不得重新激活已完成 task，若请求含 material 新 delta 则不属于 completed
  duplicate。scope clarification 只由唯一澄清 owner 取得一次真实 scope choice；choice current 后重建
  完整 readiness candidate 并 fresh 重入本判断，若 choice 改变 requirement intent 则先返回最早受影响
  requirement owner。linked prerequisite current 后只重入 change-request readiness。not-found、multiple、
  unresolved stale/material mismatch 或无法唯一解释 overlap 时得到 resolution blocked，绑定候选、最后
  确认 facts 与所需唯一输入；输入/live repair current 后 fresh 重入本判断。上述结果只路由到既有
  owner、澄清、阻塞、完成或继续，不重复拥有 requirement authoring 或 Workspace 创建。
- `EVO-REQ-060`：仅在 `new change -> standard change` 的 base-current/pre-task 读取，或其它
  route-local caller 明确声明 selected base/current authority 是其输入时，才按 exact upstream
  identity 安全刷新。这里的“pre-task”不是所有请求的通用前置步骤；direct answer、task-free、
  stop、history/specialist 与不依赖 selected base 的 distribution/release route 不得因该词自动
  触发 refresh。该 refresh 必须绑定 invocation checkout 的 current identity 与刷新前的
  HEAD/dirty-untracked 状态、selected base/ref/commit/diff identity、实际 refresh action 及其
  current result，并明确证明 invocation checkout 未被修改；刷新不得创建临时 task worktree、
  重选低优先级 base 或执行 reset/rebase/stash/force update。无法证明 upstream identity、refresh
  result 或 checkout 不变性时明确 blocked，并从 base-refresh owner 的 exact re-entry 重入。
- `EVO-REQ-061`：repository Requirements/Design/Test 或 Architecture authority 缺失、不完整、
  stale、冲突或导航断裂时，必须通过 bootstrap/repair 建立唯一 version/status/provenance 与最小
  projection；code-recovered/inferred/unverified 内容未经 semantic review 不得成为 current。
  bootstrap/repair 只在 parent repository 边界内建立 authority，不得从 submodule 拼装或推断
  parent current RDT。
- `EVO-REQ-066`：任何 parent repository route（standard/task-free/resume/recovery）默认排除
  `.gitmodules`、mode `160000` gitlink 和 submodule worktree 的内容、状态、RDT、代码、测试与验证；
  不得自动执行 init/update/checkout/
  sync/foreach/recursive scan，submodule 未初始化、dirty、detached、不可访问或失败不得改变 parent
  task 的 mode/readiness/result。只有 current 用户请求显式把某个 submodule repository 作为独立
  change scope 时才可 opt in，并为该 repository 单独建立 current authority、workflow 和精确副作用
  确认；submodule 中被用户引用的文档在 parent task 中最多是 external evidence，需经 parent
  task-local RDT contribution 承接后才能成为 parent shared current。

### 3.2 RDT- and Architecture-aware Planning

- `EVO-REQ-012`：标准 workflow 的 Planning 由同一轮 current requirement/reviewed-design、parent
  repository current Requirements/Design/Test 及其 authoring/review/lifecycle contract、current
  Architecture authority 共同驱动。RDT impact/alignment 是 Planning 的第一个实质步骤，之后才
  形成一次 `prd.md`、`design.md`、`implement.md` task-local 写作闭环；不得调用 upstream
  `trellis-brainstorm`、让 task planning 成为独立项目文档 authority，或形成双 author/wrapper
  author。task-free 不进入该正式写作闭环；它只能在 `EVO-REQ-010` 的有界合同内完成，否则返回
  standard workflow。
- `EVO-REQ-064`：在第一次实质编写 task planning artifacts 前，Planning 必须实际回读并绑定
  current repository RDT，比较 current task requirement/reviewed-design delta，并恰好形成
  `rdt_no_impact`、`rdt_aligned`、`rdt_contribution_required` 或 `rdt_authority_blocked` 之一。
  `rdt_no_impact` 必须可解释，不能由 `no_docs_update_needed`、`docs_ssot=true` 等自报布尔值、文件
  存在性或关键词规则替代；missing/stale/incomplete/conflicting authority 必须先进入 repair，真实
  RDT delta 必须先形成 task-local contribution，未收敛前不得 `plan_ready`。
- `EVO-REQ-013`：第一次实质编写 `design.md` 之前，必须实际读取并绑定 current
  Architecture Baseline、设计宪法和 change contract；产后补读不能声称“首稿参考过”。
- `EVO-REQ-014`：无 Architecture 影响时必须给出可解释的 no-impact 结果并快速继续；
  不得生成空 Architecture report、contribution 或 ADR candidate。
- `EVO-REQ-015`：current baseline 正常承接时，`design.md` 必须明确适用的 current
  decisions/rules/GAP/ownership 与项目检查，不复制 baseline 正文。
- `EVO-REQ-016`：requirement 或 reviewed design 与 baseline 冲突时，必须保留产品意图、
  显式呈现冲突和可选取舍，并在收敛前停止批准；Architecture 不能静默覆盖 PRD。
- `EVO-REQ-017`：baseline、constitution 或 change contract 缺失、过期、不完整、彼此冲突
  或 identity 不可证明 current 时，必须在 design 首稿前停止并返回 shared Architecture
  authority 的 bootstrap/repair 边界；修复后重读 current authority。
- `EVO-REQ-018`：新需求发现 current baseline 不足时，Planning 只能形成 task-local
  Architecture contribution；仅当改变 decision、原则取舍/例外、GAP lifecycle、owner、
  single-writer 或 compatibility exit 时才创建 ADR candidate。
- `EVO-REQ-019`：Architecture proposal 必须说明触发需求、current/target before-after、
  受影响决策/GAP/owner/single-writer/compatibility exit、取舍、验证与退出条件，但不得在
  Planning 直接修改 shared current authority。
- `EVO-REQ-020`：shared Architecture 只能经独立 review、expected-current serialized
  promotion、fresh Phase 2、Task Commit 和 committed full-diff Branch Review 前进。
- `EVO-REQ-021`：planning artifacts 必须从项目文档 authority 降为 task-local projection/delta：
  `prd.md` 引用 current repository Requirements，只拥有本 task 的 requirement delta、适用范围、
  未决澄清与验收映射；`design.md` 引用 current repository Design，只拥有 reviewed-design
  reconciliation、适用 Design delta 与 Architecture alignment；`implement.md` 引用 current
  repository Test 与 task-local Test delta，只把 approved RDT/Architecture 映射为执行顺序、验证
  和交付范围。可 promotion 的 RDT 变更应回写为 task workspace 中的 repository RDT candidate/
  contribution，三份 task 文件只引用它；不得复制完整 RDT 正文、另造平行 task RDT/handoff、冒充
  repository RDT 已完整，或成为跳过 RDT contribution/review/promotion 的替代 authority。
- `EVO-REQ-022`：Issue 已审阅设计必须进入 `design.md` 的 reconciliation：被保留、被 current
  authority 补充，或因明确冲突/过期而经决策修订；不得无说明重新设计。
- `EVO-REQ-023`：明确 requirement 直接派生的普通 acceptance/test scenario 默认直接进入
  coverage；只有真实语义歧义或明确的 current normal-scenario authority 要求时才增加
  qualification，且不得制造 routine user interaction。
- `EVO-REQ-024`：完整 planning 只接受一次 semantic approval。task activation 与进入实现
  是批准结果的正常承接；若同一时点确有资源副作用，可在一个精确确认中合并，不得形成
  两个语义相同的 routine confirmation。approval owner 必须从 current RDT identity/适用片段、
  task delta、RDT impact/alignment、Architecture alignment 与三份 task-local projection 实际判断
  sufficiency；不得只接受 author 自报 boolean、checker PASS 或文件存在性。
- `EVO-REQ-025`：planning finding 由拥有对应正文语义的 author 直接修订，再由同一个
  approval owner 复核受影响范围；不得通过独立 wording-only reviewer、Architecture report
  或 handoff wrapper 重复整稿语义审核。显式、有界的 contract wording 请求仍按
  `REQ-UC-EVO-037` 独立提供，不进入 normal Planning 主线。
- `EVO-REQ-026`：每个需要 repository authority 的 invocation 只建立一次 invocation-scoped
  `context_envelope`（private runtime envelope）。`authority_context`、`stock_policy_context`
  （包含 provenance）与 `provider_context` 是该 envelope 的按需 projection，不是三套独立的
  context、SSOT 或回读链；同一 projection 的 identity/freshness/dependency 只在 envelope 内绑定
  一次。先做最小 applicability 判断并按阶段区分：`new change -> standard change` 的 requirement
  Intake 只绑定当前用户/Issue、repository current Requirements/Design/Test、authoring/review/
  lifecycle contract、必要 Git/GitHub/Trellis facts；Intake 的 `Architecture slice = N/A`，不得在
  该阶段执行 Architecture impact/alignment 或实质正文消费。进入 pre-design Planning 后，同一
  invocation envelope 才按需投影 current Architecture Baseline、constitution、change contract
  及其适用片段，并与 current RDT、task delta 一起完成 alignment；这不是第二条读取链。随后
  Implementation/Check/Review/Delivery/Finish/Cleanup，以及实际触及 repository RDT、Architecture
  或 stock policy 的 route，只绑定适用的 current RDT/Architecture identity 与片段、stock
  source/provenance、provider contract 与必要 live facts；若某 slice 不适用，明确为 N/A，不因
  envelope 存在而读取它。direct answer、非 stock stop/history、通用只读 specialist 以及不依赖
  repository authority 的 standalone read 只绑定回答所需的最小 facts，只有答案确实依赖
  RDT/Architecture 或 stock surface 时才绑定对应 projection。task-free 与 standalone projection
  也必须先完成该最小 applicability 判断，不得因为存在 authority 或 stock inventory 就全文读取。
  task-free 与标准 Phase 2 在进入实现前使用的 Guru-owned `implementation_context` 必须是从同一
  envelope 按当前 implementation owner、scope 与适用 authority slice 派生的薄 projection；它只
  提供本次实现直接消费的 coding/spec/plan/authority context，不是第二套 authority、SSOT、全文
  回读链或 raw `trellis-before-dev` 的兼容 wrapper。两个 profile 共享同一派生合同，但每次调用
  必须恰好绑定 task-free 或标准 Phase 2 的一个 implementation owner。
  locator/status 级的 applicability 证据不等于完整正文回读。同一 invocation 内的 Guru Skill、
  provider、worker、check、review、delivery 与 stock-policy caller 只消费该 envelope 的最小
  projection，不各自重新读取 Requirements/Design/Test/Architecture、package provenance 或 provider
  contract。若 stock route 同时触及 RDT/Architecture，两个 projection 必须从同一 envelope 建立，
  不得形成第二条 authority read chain。
  同一 invocation 的 mapped recovery/re-entry 复用仍 current 的 envelope；只有实质 scope/authority、
  source/projection identity 或 decision-relevant live-fact 变化才从最早受影响 owner 使对应
  projection 及下游 freshness 失效并定向重读。locator-only 或经证明等价的重发布只更新
  identity/freshness，不重放完整 semantic review。普通入口在生成 `request_received` 前建立 envelope；
  独立入口也只在建立新 invocation identity 时建立一次。一个 invocation 恰好生成一次
  `request_received`，isolation pending/blocked 的 re-entry 复用该 envelope 和 receipt，不再建立第二个
  envelope 或 receipt。
  技术机制变化不失效未改变的 product requirement；envelope/projection 本身没有直接 consumer
  的字段不得进入 public handoff。

### 3.3 Implementation、Check、Review 与 Promotion

- `EVO-REQ-027`：Implementation 必须消费 current approved plan、current repository RDT binding、
  task-local RDT contribution/alignment、适用 Architecture alignment 和必要 live facts；不得依赖
  planning author 的 private review transcript，也不得从 task planning artifacts 反推 shared RDT。
- `EVO-REQ-028`：Phase 2 必须对当前 task scope、实现、测试、repository RDT satisfaction/
  contribution、Architecture change contract 和未验证边界完成一次完整 semantic check；若输入
  unchanged，不得叠加重复
  reviewer 证明同一充分性。若 reviewed path 是本 task scope 内的 Gitlink，Phase 2 的 reviewed-content
  identity 必须绑定 superproject index mode `160000` 与 commit/index pointer；已初始化 Gitlink 还须
  绑定其 root、clean status 与 `HEAD` content identity。无关 Gitlink 仍不进入 task scope、实现读取或
  validation，也不得因 Phase 2 能读取相关 Gitlink identity 而取得 Task Commit staging authority。
- `EVO-REQ-029`：finding 修订后只重做其语义依赖的实现、验证和 gate；每次新的 pass 必须
  绑定 current candidate，旧 pass 不能被复用为 current。
- `EVO-REQ-030`：Branch Review 必须独立读取 exact committed `origin/<base>...HEAD` full
  diff、current repository RDT/task-local contribution/Architecture authority 与测试结果；工作树
  片段、旧 Phase 2 或未提交内容不能冒充 full-diff review。若唯一 observation 只是文本文件 EOF
  多出一个或多个空行，且 meaningful bytes 完全不变，只记录无严重度、非阻断 observation，不得
  形成 `P0..P3` finding 或 implementation route；行尾空格、缩进、字符串/配置值、编码或会改变
  parser/linter/formatter 合同的 whitespace 仍按正常 candidate 审核。
- `EVO-REQ-031`：Architecture promotion 改变 shared current 后，原 candidate 必须重做
  受影响的 Architecture satisfaction、Phase 2、Task Commit 和 Branch Review，不得仅更新
  locator 后继续。
- `EVO-REQ-032`：base 演进必须按实际 diff 与语义依赖判断 no-impact/revision/recovery；
  不得从 Phase 0 重建已有 task，也不得因无关 base movement 全链失效。
- `EVO-REQ-033`：并行 task 必须隔离各自 task/workspace/branch/contribution、delivery provider、
  archive、Finish、cleanup、history 与 retained ref；shared authority promotion 之后，绑定旧 identity
  的 task 必须重算影响，不能形成双 current 或双 writer。同一 exact base 上 A=`github_pr`、
  B=`none` 时，两种 completion/merge order 都必须保持 route-specific 副作用与 terminal result
  独立；任一 task 的 provider/archive/Finish/cleanup failure 只返回该 task 的 current owner，不得
  阻塞、重放或错误归属另一 task 的动作。两个 task 各自恢复后都必须保有可查询 history/current
  result，cleanup 前后需保留的 commit/ref/history 均可达；B 的 GitHub I/O 始终为 0。
- `EVO-REQ-062`：task 对 repository Requirements/Design/Test 的新增、修订、替换、拆分、合并
  或删除必须在 task workspace 的 repository RDT candidate/contribution 中持续回写，保持 stable
  predecessor/successor 与
  requirement/behavior -> design responsibility/contract -> test strategy/scenario/case 追踪；该
  contribution 必须随 Planning、Implementation discovery、Phase 2 finding 和 review revision 回写，
  不得把只存在于 task planning 或代码中的新事实留到 Finish 后再补文档，也不得为回写制造第二套
  完整 RDT 或无 consumer handoff；shared current 只经 independent serialized promotion 激活。
- `EVO-REQ-065`：从 Implementation 到 Phase 2、Branch Review、PR readiness 或 `none` route
  对应的 local acceptance readiness、pre-delivery Acceptance，各语义责任边界必须消费或验证其
  判断所依赖的 current RDT binding、impact/alignment、task-local contribution 和 promotion 状态；
  identity unchanged 或经证明等价时不重复整份 RDT review，material stale/change 时返回最早受
  影响 owner并重算下游。Finish/Cleanup 只消费已收敛且 current 的 terminal RDT lifecycle 状态，
  不重新拥有 RDT judgment。
- `EVO-REQ-034`：每个阶段结果，包括 `direct_answer_completed` 与 active lifecycle disposition
  result，必须恰好具有一个下一 owner、一个明确 re-entry 或一个 terminal stop；unknown、multiple、
  unmapped 或无 consumer 的结果必须停止，Agent 不得猜测路线。

### 3.4 Publication、Delivery、Finish 与 History

- `EVO-REQ-035`：PR readiness 必须从 current repository RDT/task contribution、current plan、
  exact committed diff、验证、Architecture 状态以及 live GitHub facts 形成；标题/正文、部署/
  安全影响和未验证边界必须真实具体。
- `EVO-REQ-036`：Issue closure 语义必须由 current Issue、accepted requirement scope、exact
  reviewed diff 和 live delivery facts 判断；不得恢复 Issue Scope Ledger 或以
  `close_issues/related_issues/followup_issues` aggregate 作为 current authority。每个完成 delivery
  的 change 必须在 Finish 前恰好得到 `issue_closure_current` 或
  `issue_closure_not_applicable`；无 Issue、Issue 不应关闭或 `none` route 均属于可解释的
  not-applicable，而 closure mismatch 必须留在 delivery owner recovery/blocked，不能被
  `merged` 或 archive 隐藏。
- `EVO-REQ-037`：在 route-specific readiness 前，delivery route 必须由 current change/task
  authority 唯一决定为 `github_pr` 或 `none`；authority 已明确时不得提问，存在真实 delivery
  choice 时只询问一次。该选择必须绑定 current scope/provider intent；材料变化时在尚无不可逆
  remote side effect 前重新选择，已发生不可逆副作用后只 forward recover。GitHub provider
  failure、认证缺失或配额问题不得自动降级为 `none`。`github_pr` route 必须覆盖 push、PR
  publication、expected-head delivery、merge 与 Issue closure-current/not-applicable 的 current
  状态；每个不可逆副作用只执行一次并具有 forward recovery。
- `EVO-REQ-038`：`none` route 必须从明确 current delivery authority 进入，保持完整本地
  acceptance/Finish/history/cleanup 能力，且不调用 GitHub、不伪造 PR 或 Issue identity；其
  route-specific readiness 是 local acceptance readiness，不得复用或伪造 PR readiness。
- `EVO-REQ-039`：本条适用于 Delivery、distribution/projection、clean install、existing migration
  与 Release 中所有需要外部 provider 的动作。正常 timeout/unavailable、认证缺失、限流/配额、
  远端状态变化、unknown outcome 或部分成功必须返回拥有 exact action 的 delivery、projection、
  install、migration 或 publication boundary；不得切换到其它 route 掩盖失败。每类外部动作必须
  绑定 current provider contract/capability 与 exact target/action，并分类认证、配额、错误、unknown
  outcome、可重试性、幂等性与 terminal rejection。恢复前先重读 live provider state，区分已完成、
  未完成与结果未知的副作用，保留 current 成果且不得重复不可逆动作，也不重跑无关阶段。自动重试
  必须有界，且只在 live state 证明原动作未完成、provider contract 允许安全重复时执行；认证缺失、
  不可重试拒绝、无法消除的 unknown outcome 或未收敛的部分成功必须停止自动重试并进入所属边界的
  明确 recovery/blocked。每个 provider contract 在 action 前还必须绑定可定位的 source owner、
  contract locator/version、caller scope、exact target/action、输入 identity/字段语义、输出或
  回执状态与生效时点、权限/限流/配额/错误/部分成功/unknown 语义、幂等键或等价重复请求口径、
  live-state reread 入口、可重试条件与停止条件；不能只提供一个 provider 名称或版本字符串。
  Git provider 至少覆盖 selected base/ref/commit/diff identity 与 local write/commit/push 的
  current result；GitHub provider 至少覆盖 repository、ref、PR/Issue/tag/Release target identity、
  expected-head/remote state 与 closure/publication result；Trellis/upstream provider 至少覆盖
  pinned package/template/registry source identity、command/flag/output/exit-code facts 与 update
  discriminator。这些是外部 provider facts 与边界合同，不创建 Guru API/CLI intent；具体 adapter、
  字段载体和实现位置由 Design 决定，但不得省略上述语义维度。具体退避、最大尝试次数和 provider
  adapter 由 Design 决定，但必须形成有限的等待/尝试边界；不设置相对耗时或 rounds 的 Release
  门槛。认证/权限缺失、不可重试拒绝、无法消除的 unknown outcome 或未收敛的部分成功必须停止
  自动重试并进入所属边界的明确 recovery/blocked；不得弱化上述 live reread、停止、去重与 route
  ownership 语义。
- `EVO-REQ-040`：Acceptance、route-specific readiness、Publication、Delivery、Merge、Issue
  closure、Finish 和 Cleanup 的 semantic responsibility 必须唯一且顺序完整；`github_pr` 只能在
  publication readiness 与 pre-delivery Acceptance 后进入 remote delivery/merge/closure，`none`
  只能在 local acceptance readiness 与 pre-delivery Acceptance 后进入 local terminal。两条 route
  都必须先得到 closure-current/not-applicable 与 delivery terminal 才能 Finish，同一事实不得在
  相邻阶段重复审批。
- `EVO-REQ-041`：远端不可逆副作用开始后，任何失败都只能 forward recover 或 terminal
  block，不得回到需求、Planning 或实现修订。此边界前到达的 material additive 必须返回最早受
  影响 owner，并按 material freshness 重算 current candidate 与下游；此边界后到达的 material
  additive 不得修改当前 lifecycle 的 accepted scope、exact candidate、delivery route 或 terminal
  acceptance，必须形成绑定原 lifecycle、到达顺序与唯一 consumer 的最小
  `additive_change_pending`。原远端 owner 必须保持 in-flight/published candidate 不变并继续既定
  route：正常成功形成该 lifecycle 的既定 current terminal；失败只允许 forward recover 至 current
  terminal 或形成 terminal block。上述任一收敛结果 current 后，pending intent 的唯一 consumer 才能
  为 pending intent 分配全新的 invocation identity、建立新的 invocation-scoped `context_envelope`，
  再恰好生成一次新的 `request_received`，随后按
  `independent_request_isolation_gate -> pre_semantic_dispatch_guard -> entry_route_selected` 顺序重新执行六类
  exactly-one route；不得复用
  原 lifecycle 的 invocation identity、envelope、candidate 或 receipt。该 remote-after 分支与前述
  无副作用/可逆本地分支共享同一“新 invocation、一次 receipt、重新分类”合同；只有分类为 new change 才进入
  `change_mode_selected` 与独立 change lifecycle，其他分类由对应顶层 route 的唯一 owner 消费，不得默认
  new change。只补充当前 forward-recovery
  所需输入的 owner-local additive 仍由原远端 owner 消费，不创建 pending change。
- `EVO-REQ-042`：Finish 只执行可机器判定的 exact task 最终状态、archive/history 与 finish-summary
  收敛；Cleanup 只删除 exact owned resource，并在删除前后证明需要保留的 commit/ref/history
  可达性。每次执行前必须 live reread 当前 task、archive/history、owned resource 与 retained-ref facts，
  已 current 的步骤不得重放。Finish 任一步骤未收敛时得到 `finish_blocked`，绑定 exact task、已完成/
  待执行 transition、最后确认 history/ref facts、未验证边界与所需唯一输入；前提恢复后只重入
  `finish_current`，不得返回 Delivery、重复 archive 或把 partial Finish 冒充 `finished`。只有 `finished`
  current 后才进入 `owned_resource_cleanup`；Cleanup 部分完成或失败时得到 `cleanup_blocked`，绑定仍
  存在、已删除和必须保留的 exact resource/ref/history，重试前重新读取 live resource state，前提恢复
  后只重入 `owned_resource_cleanup`。不得重复删除已不存在资源、扩大 cleanup owner、重放 Delivery/
  Finish，或因 cleanup blocked 隐藏已经 current 的 durable history；成功后才得到
  `owned_resources_cleaned -> workflow_completed`。
  `EVO-REQ-067` 的 abandonment cleanup 继承本条的 exact owned-resource、live reread、retained
  ref/history reachability 与不重放已完成删除约束，但不得把未完成 active lifecycle 冒充 `finished`，
  也不得重放 Delivery、Archive 或普通 Finish。
- `EVO-REQ-043`：任务历史只保留恢复、查询或 release 直接消费且无法从 live facts 重建的
  最小 durable result；不得保留用户授权、完整 stdout、逐轮审查、临时 locator 或重复摘要。history
  owner 是 archive/finish 与 active lifecycle disposition durable result 的唯一查询 owner；每个
  `active_lifecycle_disposition_completed` 必须在完成前形成可由 exact lifecycle/change identity 发现的
  最小 disposition result，并证明删除 owned task/worktree/branch 等资源后该结果仍可查询。该 durable
  result 只表达查询/恢复直接需要的 disposition terminal、保留边界与适用 resume identity，不复制
  cleanup 过程或可重建 live facts。
  显式 durable history query 必须从 current task/disposition index、archive、finish summary、
  disposition result 与必要 live facts 解析：恰好一个 schema/current 结果时得到
  `durable_history_result_current`，返回该结果后得到
  `history_query_completed -> workflow_completed`，不得重入、恢复或重新激活被查询 lifecycle；
  not-found、multiple、unresolved stale 或 material mismatch 时得到 `history_query_blocked`，列明候选、
  最后确认 facts 与所需唯一输入。输入或 live repair 使结果唯一后重入
  `durable_history_resolution`；不得把 durable history query 误判为
  `current_work_recovery_blocked`，也不得用历史查询启动新 change。用户意图是继续 retained/suspended
  work 时仍走 current-work recovery，而不是把 resume 藏进 history query。
- `EVO-REQ-063`：从 Implementation 到 Phase 2、Branch Review、PR readiness 或 `none` route
  对应的 local acceptance readiness、pre-delivery Acceptance，各语义责任边界必须消费或验证其
  判断所依赖的 current Architecture alignment、proposal/promotion 状态和 shared-current binding；
  identity unchanged 或经证明等价时不重复语义审核，material stale/change 时返回最早受影响 owner
  并重算下游。Finish 与 Cleanup 只确定性验证或消费已经收敛且 current 的 terminal Architecture
  lifecycle 状态，不重新拥有 Architecture 判断。

### 3.5 低成本执行与对话连续性

- `EVO-REQ-044`：normal workflow 的主要稳定上下文依次是 applicable repository RDT SSOT、
  Architecture Baseline/constitution/change contract SSOT 与 active task `prd.md`/`design.md`/
  `implement.md`。repository authority 拥有 shared 产品、设计、测试与架构决策；task 三件套只拥有
  task scope/delta、authority reconciliation 与执行/验证/交付 projection，不复制或替代前两类 SSOT。
  正常路径不得另建 planning handoff、Architecture report、Issue ledger、shared cache、continuation
  capsule、临时交接文档或没有 direct consumer 的 gate artifact。host/model/provider 的 prompt cache
  只能复用这些 current stable bytes，是不可依赖的执行优化，不是 workflow authority、freshness evidence
  或 PASS 条件。
- `EVO-REQ-045`：context construction 必须按稳定 locator/identity 与稳定顺序组织适用的 RDT、
  Architecture 和 task 三件套，把 decision-relevant live facts、current delta 与未解决项限制在最小变化
  tail；跨阶段只传递下一 owner 无法从上述 current authority/live facts 重建的最小信息。AI owner 直接
  基于这些 authority 与 tail 自主判断 scope、充分性、finding、route 和下一动作，不要求前一 owner
  逐项交接或复述 already-current facts；producer-private evidence 在 consumer 完成后卸载，consumer
  不得读取 producer 的 private result、digest 或 recorder internal state。
- `EVO-REQ-046`：阶段完成、context compression 或 resume 时，必须卸载原始 scan/stdout/重复正文，
  先从 current RDT、Architecture 与 task 三件套 locator/identity 恢复稳定上下文，再只补未解决问题、
  当前阶段、最新用户意图、当前副作用状态与继续所需最小 live delta；不得用长篇 handoff summary、
  transaction ledger 或事实复述替代 exact owner 的 current authority resolution。
- `EVO-REQ-047`：compression/resume 必须优先恢复并消费最新用户意图、当前副作用状态和
  未完成 terminal action；每条恢复期间到达的用户消息先执行 `lifecycle_intent_preclassification`：
  bound intent 必须携带并复用同一 exact invocation/lifecycle identity、current owner/phase、scope/
  candidate identity、host user-event identity 与到达序列，回到 current/最早受影响 owner；明确
  independent intent 必须取得新的 invocation identity、建立最小 `context_envelope` 并恰好形成一次只表示
  admission 的 `request_received`，不得被 active owner 吞并；receipt 后先过 isolation safety gate，无 active
  lifecycle 时立即 clear 并进入 `pre_semantic_dispatch_guard`；有 active lifecycle 且 shared scope/不可逆动作
  尚未安全隔离时才进入 `independent_request_isolation_pending`，安全边界后复用该 receipt exact re-entry，不得重复 receipt。
  若 active lifecycle 存在而 binding 既非唯一 current、也无法证明独立请求，只得到
  `lifecycle_intent_binding_blocked`，一次澄清或 live-fact repair 后重入 preclassification，不能猜测
  为 override、additive 或 ordinary new request。随后才从 current authority、live facts 与最小 durable result 解析
  current work。恰好一个 current work，或 stale locator/identity 已由 live facts 证明只指向一个
  semantically equivalent current work 时，必须刷新 identity/freshness 并得到
  `current_work_recovered`；not-found、multiple、unresolved stale 或 material mismatch 必须得到可解释的
  `current_work_recovery_blocked`，列明候选 identity、最后确认的 current facts 与完成选择/修复所需的
  唯一输入，不得猜测 checkout、创建第二份 task 或复用未刷新的旧 locator。所需输入或 live repair
  使 current work 唯一可解析后，必须重入 `current_work_resolution`，不得跳过解析直接声明 recovered；
  用户明确放弃恢复并启动独立新请求时，唯一 request-entry consumer 必须先分配新的 invocation identity、建立新的 invocation-scoped `context_envelope`、恰好生成一次 admission `request_received`，再按
  `independent_request_isolation_gate -> pre_semantic_dispatch_guard -> entry_route_selected` 顺序重新分类；不得复用被恢复 lifecycle 的 identity、envelope、candidate 或 receipt。
  追加请求必须按到达顺序先分类再消费。不改变 accepted scope、exact candidate、delivery route、
  terminal acceptance，或只补充 current forward-recovery 所需输入的 owner-local additive，由
  current/最早受影响 owner 直接并入未完成请求，不失效无关 current 结果。改变上述任一事实的
  material additive 在不可逆远端副作用开始前必须返回最早受影响 owner，按 `EVO-REQ-015,063,065`
  的 freshness 语义重算受影响结果；在不可逆远端副作用开始后必须按 `EVO-REQ-041` 形成
  `additive_change_pending`，不得修改或重排原 lifecycle 的 in-flight/published candidate，待原远端
  owner 收敛为既定正常 current terminal、失败后 forward-recovered terminal 或 terminal block 后，由
  唯一 consumer 为 pending intent 分配全新的 invocation identity、建立新的 invocation-scoped
  `context_envelope`，再恰好生成一次新的 `request_received`，随后按
  `independent_request_isolation_gate -> pre_semantic_dispatch_guard -> entry_route_selected` 顺序重新执行六类
  exactly-one route；不得复用原 lifecycle 的 invocation identity、envelope、candidate 或 receipt。
  只有分类为 new change 才进入 `change_mode_selected` 与独立 change lifecycle，其他分类由对应顶层 route
  的唯一 owner 消费，不得默认 new change。覆盖请求必须先分类旧工作的
  副作用状态：尚无副作用时停止旧 route；已存在
  task/worktree/branch 或未提交写入等可逆本地
  副作用时，立即停止后续写入并保留 exact current work 为具有唯一 resume owner 的、可发现且
  可恢复的 `suspended_current_work`，不自动提交、丢弃、归档或清理。无副作用停止或本地
  suspend current 后，原 bound 事件由唯一 request-entry consumer 投影为一个全新 invocation：先
  分配新的 invocation identity、建立新的 invocation-scoped `context_envelope`，再恰好生成一次
  `request_received`，随后按
  `independent_request_isolation_gate -> pre_semantic_dispatch_guard -> entry_route_selected` 顺序继续；不得复用
  原 lifecycle 的 identity、envelope、candidate 或 receipt，也不得把该 bound 事件再次执行
  preclassification。新意图进入 entry selection
  后，若与 suspended work 同 scope，必须由消费新 lifecycle 的 owner 按 `EVO-REQ-011` 完成
  reconciliation；若为异 scope，必须先证明资源隔离并保留旧 work 的 discoverable resume route。
  无法判定 scope、owner 或隔离关系时 blocked。若用户明确要求保留、暂停、取消、放弃或清理旧工作，
  必须按 `EVO-REQ-067` 进入 exact active lifecycle disposition。已发生 push/PR/tag/Release/merge/
  Issue closure 等不可逆远端副作用
  时，必须先由原 owner 保持旧 candidate 不变，并收敛为既定正常 current terminal、失败后
  forward-recovered terminal 或 terminal block。旧结果 current 后，latest override 必须由唯一
  request-entry consumer 为该 override 分配全新的 invocation identity、建立新的 invocation-scoped
  `context_envelope`，再恰好生成一次新的 `request_received`，随后按
  `independent_request_isolation_gate -> pre_semantic_dispatch_guard -> entry_route_selected` 顺序继续；不得复用
  原 lifecycle 的 invocation identity、envelope、candidate 或 receipt。只有分类为 new change 才进入
  `change_mode_selected` 与新的 change lifecycle，不得默认 new change 或用新请求掩盖旧副作用。
- `EVO-REQ-048`：长运行命令/Agent 的每次 wait 只返回新输出或紧凑最终结果，必须复用有效
  handle；不得轮询不存在的 handle、重复注入累计 stdout 或把无关大对象/base64 注入上下文。
- `EVO-REQ-049`：用户可见消息只服务普通 direct answer、真实选择、实质 finding/block、需要跨响应
  继续的长运行等待、阶段结果和副作用确认；AI owner 必须从 current authority 与 task projection
  自主完成适用判断和执行，不把 human-style assignment、approval/signoff chain、transaction handoff
  或 already-current fact restatement 暴露为用户必须消费的流程。正常内部读取、projection、recorder、
  validator 与 locator 搬运保持安静。
- `EVO-REQ-050`：正常执行路径必须产生足以评估 `EVO-NFR-008` 的 current 可观察结果，并把
  异常计数绑定到 exact fixture/run；零计数项目与阈值只由 `EVO-NFR-008` 主定义，本需求不复制
  该集合，也不得用缺失观测、`unverified` 或旧 run 冒充满足质量门槛。
- `EVO-REQ-067`：用户要求保留、暂停、取消、放弃或清理既有 active lifecycle 时，必须先按
  `EVO-REQ-047` 解析并刷新 exact current work，再进入唯一 `active_lifecycle_disposition` owner；不得
  走 top-level stop、普通 task Finish/Cleanup 或重新创建 lifecycle。该 owner 必须绑定 exact lifecycle、
  current phase/owner、已发生副作用、owned resources、必须保留的 commit/ref/history、未解决 finding
  与用户当前 disposition intent，并按 live facts 恰好进入以下产品分支。尚无不可逆远端副作用，且
  “取消”等当前意图不能唯一判定 retain/suspend 或 abandon/cleanup 时，只询问一个最高价值问题；
  choice current 前保持 `active_lifecycle_disposition_choice_required` 且 cleanup 副作用为 0：

  - 尚无不可逆远端副作用且用户选择 retain/suspend 时，停止新增写入，保持 exact work 可发现、可恢复
    且只有一个 resume owner，不执行 cleanup；形成 `active_lifecycle_retained` 或
    `active_lifecycle_suspended`，保留区分该 disposition 所需的最小 current/durable result，并以
    `active_lifecycle_disposition_completed -> workflow_completed` 结束本次 invocation。
  - 尚无不可逆远端副作用且用户明确要求 abandon/cleanup 时，必须先形成并展示 exact cleanup plan：
    将删除的 exact owned resources、不会删除的 unrelated/retained resources、必须保留的 durable
    history/ref 与 abandonment terminal。若 live plan 证明 deletable owned resource 为 0，且保留项/
    history 可达性 current，则无需制造 cleanup 确认，直接得到 no-op
    `active_lifecycle_abandoned`。若存在 deletable owned resource，必须在当前对话取得 cleanup 副作用
    确认；确认缺失时只保持 `active_lifecycle_cleanup_confirmation_pending` 且 cleanup 为 0。明确拒绝
    exact cleanup plan 时不得直接投影为 `retained | suspended` 双终点：若拒绝回复已包含唯一 retain
    或 suspend 选择，直接按该选择重入 disposition；否则得到
    `active_lifecycle_disposition_choice_required` 并只询问一次 retain/suspend 的真实选择，choice
    current 前 cleanup 为 0。resource/owner/history facts 变化必须使旧确认失效、live reread 并重新形成
    plan。只有 current 确认可启动 `active_lifecycle_owned_cleanup`；成功后得到
    `active_lifecycle_abandoned`。no-op 或 cleanup abandonment 都必须按 `EVO-REQ-043` 形成 cleanup 后
    仍可查询的最小 durable disposition/history，再以
    `active_lifecycle_disposition_completed -> workflow_completed` 结束。授权状态和授权过程不得
    持久化。
  - 已发生不可逆远端副作用时，不得删除、回滚、移动或重建远端结果，也不得把旧 lifecycle 冒充
    cancelled/abandoned。原远端 owner 与 in-flight/published candidate 保持不变，必须先收敛为既定正常
    current terminal、失败后 forward-recovered current terminal 或 terminal block。该结果 current 后，
    disposition owner 只能对用户仍明确要求、当前对话已确认且不破坏远端/durable result 的 eligible
    local owned resources 执行 exact cleanup；随后保留原远端结果和最小 durable disposition/history，
    得到 `active_lifecycle_remote_outcome_current -> active_lifecycle_disposition_completed ->
    workflow_completed`。

  exact owner/副作用/资源/保留项无法唯一判定、required cleanup plan 无法 current，或 cleanup
  部分失败时，必须得到 `active_lifecycle_disposition_blocked`，绑定最后确认 facts、已完成/待执行动作、
  仍存在/已删除/必须保留资源与所需唯一输入；前提恢复并 live reread 后只重入 exact
  `active_lifecycle_disposition` 或 `active_lifecycle_owned_cleanup`，不得扩大 owner、重放已完成删除、
  隐藏 durable history，或重新执行顶层 entry selection。

- `EVO-REQ-081`：任何需要 human confirmation 的 Git、GitHub、Trellis、Release、cleanup 或其它
  副作用，只能使用 dialogue-local semantic confirmation。action owner 必须先在当前对话完整展示
  current 精确计划，至少使用户能唯一识别将执行的下一项行动、repo/target、scope、具体副作用、
  明确保留或不包含的相邻副作用，以及当前事实/前提；展示后 target、scope、副作用或
  decision-relevant facts 未发生实质变化时，用户回复“确认继续”“可以，继续”或其它语义等价的
  清晰肯定表达，即构成对刚展示行动的充分确认。

  - 不得要求用户复制固定 prompt、口令、hash、digest、task id、路径、branch、SHA、摘要或规定句式；
    `确认执行 <hash>`、identity challenge、摘要复述或其它固定字符串不得成为继续流程的必要条件。
  - 只有 AI 根据当前对话语义判断回复是否清晰肯定。script、validator、recorder、schema、DTO、
    checkpoint、gate、history 或 artifact 不得接收、解析、匹配、验证、推断或持久化用户回复、
    确认状态、确认来源、确认时间、确认 identity 或授权过程；确定性组件只校验/执行已由 AI
    semantic gate 选定并展示的 current action plan。
  - 尚未完整展示 current 精确计划，回复包含疑问、限制、条件、修改、部分选择或歧义，或展示后
    target、scope、副作用、authority/permission、candidate/HEAD 及其它 decision-relevant facts 发生
    实质变化时，旧确认立即失效；owner 必须先吸收最新意图、重建并重新展示 current 计划，再等待
    新的语义确认。不得复用更早阶段、不同 action 或旧 plan 的确认。
  - 一次确认只授权刚刚展示的下一项精确行动，不授权未展示的 commit、push、PR 创建、merge、
    tag/Release、Issue closure、archive 或 cleanup，也不把当前阶段的确认扩张成后续阶段授权。
    当 exact PR 已创建且 live state 为 READY，action owner 已完整展示包含 repo/PR、base/head expected
    identity、merge method、close scope 与 post-merge verification 边界的 current merge 计划时，同样的
    “确认继续”或语义等价肯定即授权该 merge；不得额外要求用户输入固定的 `合并PR`。
  - 缺少确认时保持该 action 的 confirmation-pending 且副作用为 0；明确拒绝按 owning route 的
    refusal/stop/re-entry 合同收敛，不得把拒绝、疑问或修改误判为确认。任何 owner 都不得为提高
    freshness 或可恢复性而将 confirmation 变成 digest authority；freshness 只绑定 plan/live facts。

### 3.6 能力保留、分发、迁移与 Release

- `EVO-REQ-051`：AI 继续独占 intent、scope、sufficiency、conflict、finding、revision、route、
  PR readiness 与 Architecture judgment；脚本只执行副作用或记录/校验确定性事实。
- `EVO-REQ-052`：shared `.agents/skills` projection layer 与 Codex、Claude、Cursor 三个
  supported host 必须消费同一 semantic contract；shared layer 只计一次，platform
  launcher/prompt/command 只加载和路由，不复制 step-local behavior。官方写入 shared layer
  的其它 host 读取能力属于 source-only boundary，不得被写成本候选的额外 supported host。
- `EVO-REQ-053`：canonical source 是唯一长期分发源；dogfood、installed、preset、
  apply/reapply/update 与 workflow switch 必须投影同一新合同。projection validation 必须绑定
  exact candidate 与全部声明 projection surface，并使用两个独立、均会阻断的 gate：
  capability-loss gate 只比较 `workflow`、`task_data`、`docs_authority`；consistency/installation
  gate 比较 Skill API/interface/schema/command、distribution、managed/installed inventory、mode、
  template hash、shared-layer/host projection parity 与 extension identity/version binding。
  后一类 drift 不构成 capability loss，但仍不得声明 projection 或 installation current。所有
  distribution/projection 与 clean-install 外部动作必须继承 `EVO-REQ-039` 的 provider recovery
  合同。top-level standalone projection validation 中，任一 capability loss、
  consistency/installation mismatch、drift 或未处理 `.new`/`.bak` 必须由唯一 projection owner 得到
  `projection_validation_blocked`，报告 affected surface、expected/current identity、所属 gate、
  mismatch 与最后确认结果，不得声明 `projection_current`；前提修复后只重入 exact
  `projection_validation`，不得转入 install/migration/Release 作为 fallback。若同一双门禁作为
  clean install、existing migration 或 Release pre-publish 的内嵌验证步骤运行，projection validator
  只把绑定 exact candidate/surface/gate/mismatch 的最小 finding 返回当前 caller，不取得顶层
  projection ownership、不得产生 `projection_validation_blocked` 或切换 invocation route；当前 caller
  分别按本条 clean-install、`EVO-REQ-054` migration 或 `EVO-REQ-056` Release 合同给出 route-local
  blocked/terminal result。clean repository 不存在
  pre-migration current，不进入 `EVO-REQ-054` 的 existing migration terminal contract；clean install
  必须由唯一 install owner 依次形成 `clean_install_application_current` 与
  `clean_install_validation_current`，完整新合同成立后得到 `new_contract_current`，任一阶段无法安全
  收敛则得到 `clean_install_blocked`。blocked 结果必须绑定 current install step、已创建资源与未验证
  边界，并在前提恢复后重入 exact clean-install step；不得伪造 `pre_migration_current_preserved`、
  猜测旧 authority 或借失败激活 target current。
- **Clean-install fixture contract (承接 `EVO-REQ-053`)**：必须可由独立执行者从同一 source/candidate identity
  重放，且先通过 `distribution_state_preclassification=clean_target`；不得借用 existing-migration
  状态。初始 repository 可以包含普通用户文件，但 active `.trellis/workflow.md` 必须缺失；若 active
  workflow 为 non-Guru 且 id/source/provenance/owner 或当前安全 transition plan 尚未唯一收敛，必须先
  标记 `foreign_workflow` 并得到 `distribution_state_blocked`。上述 facts 与 plan current 后只能重入
  preclassification 并转为 `existing_migration_target`；两种状态都不得被当作普通用户文件或
  clean-install 输入。除此之外不得存在任何可唯一归属的 official Trellis 或 Guru managed installation
  state，包括 official `.trellis/config.yaml`、`.trellis/.template-hashes.json`、scripts/spec/task/workspace
  基础结构或 manifest、Guru current workflow、`.trellis/guru-team/`、shared/host projection、未处理
  `.new/.bak` sidecar、user-modified managed file、active/resumable lifecycle、archive/finish/history 或
  retained ref。存在任一 official Trellis installation footprint 或 partial/legacy Guru managed surface、
  sidecar、lifecycle、history 或 retained ref 时不得进入 clean fixture，必须由
  `existing_migration_target` 进入 migration；疑似 managed surface 但 identity/owner 不唯一时必须 blocked，
  不得当作普通用户文件；
  target state mixed/unknown/unowned/multiple identity 时必须得到 `distribution_state_blocked` 并在修复后
  重入 preclassification。fixture 必须绑定
  Trellis package name/version、registry integrity、capture identity、Guru candidate commit/tree，以及
  `trellis/index.json` 的 `id=guru-team`、`type=workflow`、`path=workflows/guru-team/workflow.md`。
  upstream provider stimulus 使用
  `trellis init -y --claude --codex --cursor --workflow guru-team --workflow-source <immutable-source>`
  和 `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`；命令只验证
  provider 行为，不新增 Guru CLI contract。application phase 必须记录实际创建的
  `.trellis/workflow.md`、`.trellis/guru-team/`、shared `.agents/skills`、Codex/Claude/Cursor
  projection cells、脚本 executable bit 与 managed/sidecar state；validation phase 必须独立读取
  live resources、运行预期 Guru entry，并分别记录 capability-loss 与 consistency/installation
  gate 结果。只有 `clean_install_application_current` 后才能进入
  `clean_install_validation_current`，两者都 current 才能形成 `new_contract_current`；每个阶段
  绑定 candidate/source/projection identity、已创建资源、`.new/.bak`、user-modification 与最后确认
  live state。provider timeout、认证/配额、unknown/partial 或 gate finding 只能形成绑定当前
  phase/step 的 `clean_install_blocked`，前提恢复后从同一 exact step 重入，不切换到 migration、
  projection 或 Release route。
- `EVO-REQ-054`：重构可破坏旧 Guru workflow API，但不得保留兼容层；通过
  `distribution_state_preclassification=existing_migration_target` 的 existing repository，包括仅存在
  可唯一归属 official Trellis installation footprint、但 active workflow 或 Guru projection 缺失的
  repository，其五个
  supported migration cell 组成一个有序的 composite migration invocation，固定顺序为
  `MIG-CELL-INSTALL -> MIG-CELL-UPGRADE -> MIG-CELL-UPDATE -> MIG-CELL-WORKFLOW-SWITCH -> MIG-CELL-PRESET-REAPPLY`。
  五个 cell 是覆盖矩阵中的 supported provider substep/profile，不是每次 invocation 都必须执行的五个
  动作，也不是五个互相独立的完整 migration terminal；每次 invocation 只执行 applicability 判定为
  applicable 的 substep，并按固定顺序跳过其余 substep。即使五个 cell 全部 `not_applicable`，也必须
  记录五项判定、形成 composite current，并继续执行一次 final validation；不得把“未执行”解释成
  缺少 cell 或省略 composite。它们共享一次 migration preflight inventory、由 WORKFLOW-SWITCH 显式 `--force`（或已字节相等 target 的 current
  观测）形成的唯一 cutover boundary 和一次 composite final validation。每个 substep 仍必须有自己的 applicability、exact provider stimulus、
  step-local live reread、局部 finding、已完成/待执行动作与 exact-step re-entry；只有 composite
  invocation 完成后才可形成 migration terminal。全部迁移外部动作继承 `EVO-REQ-039` 的 provider
  recovery 合同，不能以任一 substep 的局部结果代替整条 composite 的 preservation 或 legacy-consumer
  proof。
  migration preflight 必须只建立一次并绑定迁移前可发现的 active/resumable task state、task index、
  archive、finish summary、durable history result 与需要保留的 commit/ref/history，逐项判定能否由新
  合同继续恢复或查询；后续 substep 复用该 current context，只在其 provider/source/file/sidecar 或
  decision-relevant live state 变化时定向 reread。任何适用结果无法无损承接时，必须在 cutover 前得到
  `pre_migration_current_preserved` 并停止 composite，不得用删除旧 runtime consumer 的名义静默丢失
  历史。所有适用的 INSTALL/UPGRADE/UPDATE substep 与 WORKFLOW-SWITCH preview/preflight current
  后，WORKFLOW-SWITCH 的显式 `--force` application（若 active workflow 已与 target 字节相等，则为
  对该事实的 current 观测）构成唯一 `migration_cutover_current`；在 final validation current 前不得
  派发 target consumer。byte-equal predicate 只能在固定顺序抵达 WORKFLOW-SWITCH boundary 后形成该
  current 观测；即使 invocation entry 已能读取到相同 bytes，也不提前推进 composite cutover，之前适用
  substep 的 finding 仍按 pre-cutover preservation 分类。cutover 前失败只能得到
  `pre_migration_current_preserved`，不得激活 target
  或破坏可恢复的 pre-migration current；cutover 开始后的部分成功必须以 live state 为依据由
  migration owner 完成 forward recovery，成功后得到 `new_contract_current`，且迁移前 active/resumable work 必须能通过新
  合同恢复、archived finish/history result 必须能通过新合同查询、retained commit/ref/history 必须
  保持可达；无法收敛时得到 `migration_blocked`。这三者是唯一合法 composite migration terminal
  category，任何 terminal 都不得暴露旧新 route/schema/artifact consumer 混合运行；
  `new_contract_current` 后 legacy runtime consumer 数量必须为 0。migration 中内嵌的 capability-loss
  或 consistency/installation gate finding 只作为当前 phase/substep 的最小输入返回 migration owner；
  它不得取得 standalone projection ownership，migration owner 必须按唯一 live cutover state 产生
  上述 terminal 结果。该失败恢复边界不构成发布后 legacy fallback。
#### `EVO-REQ-054` supported migration entry matrix

下表是本版本 composite migration 的完整 provider-substep scope；五个 cell 均为 supported，必须
在同一 composite invocation 中按固定顺序逐 step 验收，不能以一个 step 的结果代替其它 step，也不能
把任一步骤误报为完整 migration terminal。表中的 upstream command/flag 只记录 provider stimulus，
source/target identity、step applicability、local re-entry、共享 preflight/cutover、owner、
preservation 与 composite 结果分类属于本需求合同。

| Cell | Applicability / provider stimulus | Source -> target identity | Step-local phase and shared cutover | Provider / owner boundary | Preservation and composite proof | Blocked / re-entry and sidecar rule |
| --- | --- | --- | --- | --- | --- | --- |
| `MIG-CELL-INSTALL` | Optional preserve-mode backfill when existing repository is missing one or more official Trellis/platform files; provider stimulus is `trellis init -y --skip-existing --claude --codex --cursor` with no claim that `--workflow guru-team` replaces an existing workflow. If `.trellis/workflow.md` is already present with different bytes, init must preserve it and the later WORKFLOW-SWITCH step owns target activation; if no official files are missing, this step is `not_applicable`. `trellis init --force` is an independently observed overwrite control subcell, never the preservation success path. | existing official/user state -> preserved official base state ready for later target projection | `step_preflight -> provider_application -> step_current`; no step-local cutover; the shared composite cutover is reached only by the later WORKFLOW-SWITCH explicit `--force` (or its ordered byte-equal target observation) | official init provider; migration owner classifies applicability and preserves user/official files | step proves skipped/created files, user modifications and sidecars remain explainable; target capability and legacy-consumer proof wait for composite final validation | provider failure/unknown before the shared composite cutover returns composite `pre_migration_current_preserved`; exact install-step re-entry rereads only affected files/sidecars and never silently overwrites or replays completed writes. |
| `MIG-CELL-UPGRADE` | Applicable when bound official CLI version differs from target; provider stimulus is `trellis upgrade --tag <bound-npm-dist-tag-or-version>` in an isolated supported runtime, with before/after CLI version evidence. If already current, record `not_applicable` without re-running upgrade. | existing CLI/source identity -> bound target CLI identity | `step_preflight -> provider_application -> step_current`; no step-local cutover; composite cutover remains shared | official upgrade provider; migration owner owns live-state classification and forward recovery | step proves version/source transition and preserves the shared migration context; capability, active/history and legacy proof wait for composite final validation | provider timeout/auth/quota/unknown/partial before composite cutover returns composite `pre_migration_current_preserved`; exact upgrade-step re-entry rereads version and affected sidecars without replaying a confirmed upgrade. |
| `MIG-CELL-UPDATE` | Applicable after the upgrade step when an update source is bound; provider stimulus is `trellis update --dry-run`, followed by `trellis update --migrate --skip-all` only when output contains `MIGRATION REQUIRED`, otherwise `trellis update --skip-all`; the dry-run discriminator is part of this step's input. `--force`/`--create-new` are independent provider-policy/sidecar control subcells only. | existing projection + update source identity -> exact candidate projection after selected provider branch | `step_preflight -> provider_application -> step_current`; no step-local cutover; composite cutover remains shared | `trellis update` is upstream provider; migration owner preserves the observed branch and owns recovery | step proves `--skip-all` preservation of user modifications and explains `.new`/backup/sidecar state; full capability/history/legacy proof waits for composite final validation | pre-cutover provider/branch/sidecar finding returns composite `pre_migration_current_preserved`; exact update-step re-entry rereads dry-run/affected files and never guesses or replays an unknown outcome. |
| `MIG-CELL-WORKFLOW-SWITCH` | This cell is reachable only after preclassification has established `existing_migration_target`. A non-Guru active workflow may reach this cell only when its identity/provenance/owner and the current safe transition plan are uniquely resolved; before that it remains `foreign_workflow -> distribution_state_blocked`, with zero route mutation. For an eligible official Trellis/Guru current or partial target, or a resolved foreign-workflow transition target, if active `.trellis/workflow.md` is absent or not byte-equal to the bound target, provider stimulus is `trellis workflow --marketplace gh:castbox/guru-trellis/trellis --template guru-team --create-new` preview, followed by byte/sidecar/user-edit/live-identity preflight and explicit `--force` application. If the active workflow is already byte-equal to the bound target, this cell is `not_applicable` and that current observation is the sole `migration_cutover_current`; no `--force` is required. The byte-equality predicate is observed at this ordered WORKFLOW-SWITCH boundary only after all prior applicable substeps are current; byte equality visible at invocation entry does not by itself advance the composite cutover state. Preview is never application confirmation, and no-flag replacement is unsupported. | existing workflow/projection -> exact `guru-team` workflow candidate | `preview/preflight -> confirmed provider_application` -> shared composite `migration_cutover_current` -> `step_current`; the explicit `--force` write, or the ordered byte-equal target observation when the cell is `not_applicable`, is the sole cutover boundary, and no target consumer is dispatched before final validation | upstream workflow-switch provider; migration owner owns classification and forward recovery | step proves preview/application identity, user edits and sidecars; target authority and zero legacy consumers are proven only by composite final validation after later applicable steps | preview/preflight failure before composite cutover returns composite `pre_migration_current_preserved`; after the force/ordered-observation boundary, failure is post-cutover and follows forward recovery/blocked classification; exact switch-step re-entry rereads `.new/.bak`, user edits and live workflow identity and never silently overwrites/recreates the workflow. |
| `MIG-CELL-PRESET-REAPPLY` | Applicable after target workflow/provider steps when Guru preset projection is absent, stale, or source/candidate changed; provider stimulus is `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms` with the bound source/candidate. | existing Guru projection -> exact canonical/preset candidate projection | `step_preflight -> provider_application -> step_current -> composite final_validation` (the shared cutover occurred in WORKFLOW-SWITCH) | Guru preset/apply provider with bound source/candidate; migration owner owns classification and forward recovery | final validation after this last applicable step proves active/resumable recovery, archive/finish/history query, retained ref reachability, RDT/Architecture authority continuity, capability/consistency gates and zero legacy runtime consumers | provider/gate finding is post-cutover and can only resolve to composite `new_contract_current` or `migration_blocked`; exact preset-step re-entry rereads affected user-modified/unknown sidecars and never silently reapplies/removes resources. |

每个 substep 必须记录 source/target identity、step phase、applicability、provider discriminator、
owner、受影响文件/sidecar、最后确认 live delta、已完成/待执行/未知动作和 exact-step re-entry；共享
composite context 只记录一次 active/resumable work、archive/finish/history、retained ref、RDT/Architecture
  authority 与 WORKFLOW-SWITCH 的唯一 migration cutover。`not_applicable` 也必须记录该结论及其
provider/live-state 依据；若五项均为 `not_applicable`，仍须形成 composite current 并执行一次 final
validation。五个 substep 的 provider timeout、认证/配额、unknown/partial、projection
gate finding 和 legacy-consumer mismatch 都按 `EVO-REQ-039` 与共享 cutover 分类处理；任何 substep
未覆盖时，Requirements gate 只能保持 `requirements_draft`，不能以其它 substep 或独立 control subcell
的证据代替。当前 canonical compatibility verifier 的 existing cell 只提供
`UPGRADE -> UPDATE(dry-run 分支) -> WORKFLOW-SWITCH -> PRESET-REAPPLY` 四阶段 provider evidence；
其 before-state initial setup 不等于 preservation-mode `MIG-CELL-INSTALL`，因此该 current evidence
不计为 INSTALL 或五-cell target closure。目标 composite verifier/fixture 必须在后续 Design/Test
承接 `trellis init -y --skip-existing --claude --codex --cursor` 的 preservation INSTALL，并在同一
composite 中记录其 applicability/current，再于 cutover 后只执行一次 final validation；若未来要声明
五个独立 migration terminal，必须新增独立 profile、fixture 与 verifier，不能复用该 composite 证据。

每个 substep 还必须记录 provider flag/profile discriminator，且只使用该 provider 实际暴露的变体：
INSTALL 的 preservation profile 是完整的 `trellis init -y --skip-existing --claude --codex --cursor`，
不把 `--workflow guru-team` 写成 existing replacement；`trellis init --force` 只作独立 overwrite control
subcell，`--create-new` 对 `trellis init` 为有依据的 N/A。UPDATE 以 `trellis update --dry-run` 后的
`trellis update --migrate --skip-all` 或 `trellis update --skip-all` 为 composite success branch，
`--force`/`--create-new` 只能作独立 control subcell；UPGRADE 只使用
`trellis upgrade --tag <npm-dist-tag-or-version>`；PRESET-REAPPLY 的 apply script 不暴露这两项 flag，
均记录 provider-help 依据的 N/A；WORKFLOW-SWITCH 在 workflow 非字节相等时必须使用
`trellis workflow ... --create-new` preview 后显式 `trellis workflow ... --force` application，字节相等时
记录 live-state `not_applicable` 观察即可。每个 N/A 都必须有 provider help/contract 或 live-state 依据，不能
用泛化 flag、其它 substep 或 control subcell 结果代替；substep 局部 current 不得提前形成 migration
terminal。

- `EVO-REQ-055`：不得丢失
  [`current-capability-inventory.md`](./current-capability-inventory.md) 中分类为
  `preserved_current` 或 `replaced_contract_shape` 的 current 用户能力；保留的是可观察结果和
  正常场景，不是 current Skill 数量、名称、handoff shape、Issue 顺序或文件布局。该 inventory
  只做 current-to-target 追踪；target 行为仍以本文件 `EVO-REQ-*` 为唯一主定义，验收以对应
  fixture 为准。
- `EVO-REQ-056`：Release 必须分为两个不可倒置的证明边界：同一个 exact candidate 先通过本文件
  的功能、RDT/Architecture lifecycle、执行成本治理、continuity 与 platform/install/update
  pre-publish fixtures，形成唯一 canonical wait state `ready_for_release_confirmation`；取得独立发布
  确认后才进入 `release_publication_in_progress`，创建并 live 验证 immutable tag 与 GitHub Release。
  `ready_for_release_confirmation` 只在 exact candidate、完整 pre-publish result 与 decision-relevant live
  facts 都 current 且用户尚未作出发布选择时保持等待；缺失确认不得发布，也不得伪造超时决定。用户
  明确拒绝本次发布时，Release owner 必须以零 tag/Release/publication 副作用得到
  `release_not_published -> workflow_completed`，保留 candidate 与已完成证明的真实状态；后续发布请求
  必须由新的 independent invocation 分配 identity、建立 `context_envelope`，恰好生成一次 admission
  `request_received`，经 `independent_request_isolation_gate -> pre_semantic_dispatch_guard` 后重新选择
  distribution action 并读取 current facts。等待期间 exact
  candidate 发生任何 identity/content 变化，或 decision-relevant provider/target/gate facts 变化使原
  readiness 失效时，必须立即撤销旧等待资格并返回 `release_pre_publish_validation_current`：candidate
  变化生成新 identity 并完整重跑，candidate 未变的 live-fact 变化也必须重新读取并重跑全部受影响
  gate，直到同一 exact candidate 的完整 pre-publish result 再次 current；不得继续消费旧确认或从 stale
  `ready_for_release_confirmation` 进入 publication。确认只在当前对话中即时消费，不持久化授权状态。
  全部 pre-publish 与 publication/post-publish 外部 provider 动作必须继承 `EVO-REQ-039` 的 provider
  recovery 合同。pre-publish 中内嵌的 capability-loss 或 consistency/installation gate finding 只把
  最小 finding 返回当前 Release caller，由 Release owner 得到 `release_pre_publish_blocked`；它不得
  取得 standalone projection ownership，也不得进入 publication confirmation。修订 candidate 后必须
  生成新 identity，从完整 pre-publish gate 重跑，旧 candidate evidence 不得复用。
  两者均 current 后才得到 `release_published`，再从 tag-pinned source 执行 post-publish fixtures。
  若 tag 已成功但 GitHub Release 尚未 current，必须得到 `release_publication_partial`，由原
  publication owner 绑定已创建 tag、最后确认 live publication facts、已完成/待执行副作用与唯一
  recovery input；安全恢复条件 current 后只重入同一 `release_publication_in_progress`。无法继续自动
  恢复、结果长期 unknown 或 provider terminal rejection 时得到 `release_publication_blocked`；它只
  能在同一 immutable identity 的恢复前提 current 后重入 publication owner，不得删除、移动、重建
  tag，也不得返回 pre-publish gate。只有 tag 与 GitHub Release 都经 live 验证后才得到
  `release_published` 并从 tag-pinned source 进入 post-publish verification。可恢复的 provider/
  verification prerequisite failure 得到 `release_post_publish_blocked`，绑定 published identity、exact
  verification step、最后确认 facts 与唯一恢复输入；前提恢复后只重入 post-publish verification，
  不得重新 publication。若 post-publish 证明已发布 candidate 存在需要修改产品、合同或代码的语义
  defect，原 lifecycle 必须以 `release_published_unverified` 形成 terminal block，保持原 tag/Release
  不可变且不得称 `release_verified`；修订只能由后续新的 invocation 按
  `independent_invocation_entry_contract` 分配 identity、建立 `context_envelope`、生成一次 admission
  `request_received`，经 isolation 与 pre-semantic guard 后完成 `entry_route_selected`。若该请求要求
  修改产品、合同、文档或代码，才按 `EVO-REQ-010` 分类为独立 `new change` lifecycle；该 change
  完成后，必须由后续新的 invocation/action 再按统一入口合同分类为 `distribution/release`，且二级
  action 明确为 exact-candidate Release，才可基于新 candidate 重新经历完整 Release route。验证、安装、
  迁移或发布已选 exact candidate 的请求直接按其 terminal intent 进入 `distribution/release`；其它
  分类不得创建 candidate。不得由 post-publish defect 自动强制 route、复用旧 identity/candidate/receipt
  或 reforge 原发布 identity。
  只有 post-publish 全部通过才可称 `release_verified` 和进化完成。
  执行成本治理只验证精简策略与 correctness 不降级，不比较相对性能数值。
- `EVO-REQ-057`：显式 contract wording review 必须保持可独立调用、scope-bounded、
  semantic finding/revision/return-to-caller 闭环，并区分 review-only 与 change-scoped 两种
  caller contract。review-only 的 `pass`、route-level `specialist_revision_required` 与 `blocked` 结果必须分别由唯一 caller
  消费：active caller 继续自己的 current route；top-level standalone caller 在报告 `pass` 或完整
  revision findings 后，本次 review-only invocation 立即得到
  `standalone_specialist_completed -> workflow_completed`，不得为了结束审核再要求用户选择“修改或
  stop”。只有 blocked 保持 route-local blocked/re-entry。用户随后明确要求修改被审对象时，必须由唯一
  request-entry consumer 为新的 independent invocation 分配 identity、建立 `context_envelope`，恰好生成
  一次 admission `request_received`，经 `independent_request_isolation_gate -> pre_semantic_dispatch_guard`
  重新执行顶层分类；该明确修改进入独立 `new change` lifecycle，standalone review 不得直接修改被审对象。
  当 wording review 嵌入 `new change` 时，active caller 可收到 `pass`、`content_changed` 或
  `blocked`：`pass` 回到 caller 的 current route，`content_changed` 丢弃旧 review result、重建完整
  fixed scope 并 fresh re-entry，`blocked` 只返回 caller-owned blocked/re-entry，不得冒充 pass 或
  把 caller 静默结束。`content_changed` 不是独立 top-level route，也不能把 review-only 请求改写成
  `new change`；只有用户明确要求修改时才重新执行 `entry_route_selected` 为 `new change`。除非文字
  本身是 change scope，不得成为 normal Planning 的 mandatory reviewer。
- `EVO-REQ-058`：normal-scenario qualification 只在唯一 caller 的 current authority 明确要求时
  执行，并将每个 typed result 返回该 caller/owner；`classified` 由 active caller 恢复 current
  route，top-level standalone caller 在收到结果后完成；`scope_confirmation_required` 只能交给
  唯一澄清 owner 取得一次真实 scope 选择，选择后由原 caller 重建完整 candidate set 并 fresh
  qualification；该澄清 profile 若因未决 authority、无法取得真实选择或其它正常前提失败而
  `blocked`，必须投影为 route-local `qualification_blocked`，由原 caller 在前提恢复后重入，
  不得丢给 top-level stop、当作 `classified` 或完成当前 caller。`mechanism_revision_required`
  只能交给原机制 owner 删除/替换 task-introduced mechanism；若修订前提失败，同样保持
  `qualification_blocked` 并在恢复后 fresh qualification，不得先进入 acceptance、finding 或 implementation；
  `blocked` 只产生 route-local blocked/re-entry，修复 authority/candidate/consumer freshness 后
  才能重跑，不能当作 `classified` 或完成当前 caller。明确 requirement 直接派生的普通场景不得
  例行调用。

### 3.7 Stock upstream Skill 共存、抑制与替代

本节是 stock upstream surface 与 Guru semantic owner 共存时的产品主合同；具体文件布局、
installer 实现、平台 API 和 patch 载体留给后续 Design。当前已核实的官方行为是：Trellis
`0.6.15` 将 common command/skill 与 bundled multi-file Skill 投影到已配置平台，平台可基于
自然语言 description 自动匹配；没有通用的 bundled Skill per-project disable 开关。因此
workflow marker、平台 launcher 或一次性 prompt 提示单独存在时，不得被视为冲突已解决。

当前 ownership fact 也必须保留：`.trellis/workflow.md` 与 Guru preset README 声明官方
Trellis 拥有 `trellis-*` command/Skill、hook、agent、runtime agent、bundled reference 与
`.trellis/agents/*`，Guru preset 当前不安装、替换或 managed-upgrade 这些官方路径。该事实
不等于 target 合同允许双 owner；它表示 Requirements 必须为每个 asset 写清楚 source owner、
唯一 policy binding、目标 projection cell、所需 action 类别、唯一 direct consumer、Design
  handoff id、mutation/interception owner 的当前状态以及缺失 owner 时的
  `upstream_suppression_blocked`/`provider_boundary_blocked` 分支；retained host row 另以
  `retained_context_blocked` 承接 context preserve/reconcile failure。Requirements 阶段只要求
这些 handoff 与 blocked contract 完整；尚未存在的 current mutation owner 不得被伪装成已实现，
也不得反过来阻断进入 Design。Design 进入条件再绑定可执行的 canonical/preset/overlay owner；
在该绑定 current 前，任何 patch、absence/quarantine、delete 或 adapter 都只能停在 blocked。

- `EVO-REQ-068`：每个支持的 Trellis CLI/template source snapshot 必须建立完整 stock
  surface inventory，至少覆盖 common `start`、`continue`、`finish-work` command，
  `brainstorm`、`before-dev`、`check`、`update-spec`、`break-loop` Skill，bundled
  `trellis-meta`、`trellis-channel`、`trellis-session-insight`、`trellis-spec-bootstrap`，以及
  `trellis-research`/`trellis-implement`/`trellis-check` platform and channel workers。17 个
  semantic/provider asset 必须恰好分类为 `suppressed_semantic_route`、`provider_only`、
  `explicit_only` 或 `controlled_worker_provider` 之一，角色计数必须分别为 `9/1/2/5`，绑定其
  Guru successor，并记录 source
  owner、`stock-policy owner`、所需 mutation/interception owner 类型、目标 projection cell、
  Design handoff、真实 current direct consumer 或明确的 consumer handoff projection，以及缺失-owner blocked branch；`retained_nonsemantic` 是
  不计入这 17 个 asset 的独立 surface 类别，必须按 host-bound row 记录其
  capability-preservation reason、唯一 host/policy consumer 与 `retained_context_blocked` repair
  branch。Requirements gate 只检查 tuple/handoff/blocked branch 的
  完整性；未知、重复、无法分类、没有 successor/保留理由、没有真实 consumer 或没有明确
  handoff projection/可执行 blocked branch 的 stock
  surface 阻断后续 Design/implementation candidate。尚未完成的 mutation owner 绑定本身不阻断
  进入 Design，但在 owner current 前不得进入 implementation 或声明 `stock_policy_current`；
  `consumer_unbound`、`current_drift` 与 `design_handoff` 只能表示待绑定 projection，不能冒充
  current direct consumer 或 Requirements closure。
- `stock-policy owner` 是 `REQ-UC-EVO-048` 的唯一 global workflow owner：它只负责读取
  inventory、绑定显式 provider/maintenance 调用并把结果返回声明的 Guru caller，不拥有产品
  authoring、scope、finding、approval、route、publication、merge、Finish 或 cleanup 语义；
  它不得被 stock description 自动匹配，也不能成为第四个 semantic entry owner。
  对 standalone 的 exact `explicit_only` 只读请求，stock-policy owner 只能把结果投影为
  `explicit_provider_result_current`，交给 direct-answer owner 形成
  `direct_answer_completed -> workflow_completed`；请求包含任何写入意图时，必须在 raw explicit
  asset invocation 前交回统一 top-level classification，由 `new change`/active caller 拥有实际写入，
  stock-policy owner 不能执行写入或形成产品 terminal。provider/worker
  的 embedded result 使用同一 `returned_to_unique_caller` 回程；caller 缺失、重复或 scope/target
  不唯一时统一得到 `provider_boundary_blocked`。
- `EVO-REQ-069`：`REQ-UC-EVO-047` 的未命名自然语言请求，必须先由 Guru 的唯一顶层
  entry owner 承接。覆盖维度是“一份 shared `.agents/skills` projection layer + 三个
  supported host（Codex、Claude、Cursor）”，并在每个 host 的 `main/default`、`inline`、
  `sub-agent`、`channel worker` 与 `native context/hooks` 中逐项验证；shared layer 本身
  不是第四个 host，也不产生额外的入口计数。`suppressed_semantic_route` 的 upstream
  Skill/command 不得自己分类 scope、提问、创建资源、执行 semantic check、继续 current
  lifecycle 或 Finish；若平台自动匹配已选中该名称，必须在其第一项 semantic 行为前由
  `pre_semantic_dispatch_guard` redirect 到 Guru owner 或 fail closed，且不得产生第二个
  `entry_route_selected`、第二次 semantic approval、重复全文 read 或重复副作用。该 admission
  guard 不得在 route 选择前执行 patch、absence/quarantine、delete 或其它 Git/Trellis/file mutation；
  这些 action 只能由已经选定且绑定 caller/scope/target 的 stock maintenance/provider action
  承接。Guru caller 已经选中的 route 不得再被 stock auto-dispatch 改写。
- `EVO-REQ-070`：`provider_only` 与 `controlled_worker_provider` 只能在
  Guru caller 已绑定 current scope、输入、适用 source identity 和调用目的后运行。role-specific
  能力必须完全拆开：唯一 `provider_only` 的 raw `trellis-channel` 只提供 caller-bound transport；
  五项 `controlled_worker_provider` 只提供各自 caller-bound 的 research observation、implementation
  execution 或 check evidence。memory query 只属于 `EVO-REQ-074` 的 explicit session-insight，
  diagnosis 只属于 explicit break-loop，spec/reference 则只由本条后文列出的 Guru-owned successor
  projection 承接；不得把这些能力词汇重新授予 provider/worker raw surface。所有保留面都不得拥有
  Guru 的 intent、scope、sufficiency、finding、severity、
  approval、revision、route、publication、merge、Finish 或 cleanup 判断，不得向用户制造
  第二个 routine question 或 semantic gate。对 provider/explicit/worker surface，只有经
  Guru-owned adapter 明确降级为 observation/provider 或 exact explicit binding 后才可保留；
  无法证明该 caller boundary 时必须得到 `provider_boundary_blocked`，不得直接运行。特别地，
  raw `trellis-before-dev` 归 `suppressed_semantic_route`，不得继续作为 task-free 或标准 Phase 2
  provider。它的可观察结果由 `EVO-REQ-026` 的 Guru-owned `implementation_context` 薄 projection
  完全承接；该 projection 分别绑定 task-free 与标准 Phase 2 implementation owner，但不保留 raw
  Skill identity、自动匹配面或第二套 spec 全文读取链。平台 `trellis-implement` worker 仍必须按
  这两个 implementation caller 维度绑定 scope、profile、最小 result 和回程；每次 invocation 恰好
  选择一个 owner，不得固定只绑定 task-free。`trellis-brainstorm` 不得继续作为
  `guru-clarify-requirements` 的
  questioning provider。`trellis-spec-bootstrap` 的 raw asset 直接归
  `suppressed_semantic_route`：它会选择 spec/authoring 边界并写入 `.trellis/spec`，不能作为
  target provider。Design 若确有可复用的非语义读取，必须创建独立 Guru-owned adapter identity；
  该 adapter 不继承 raw Skill 的 role、自动匹配面或写入权，且 raw asset 仍按 suppression 验收。
  若请求要求修改文件、合同或产品事实，必须由新的 Guru `new change` invocation 承接；若调用
  与 current Guru owner 重叠或 provider 无法证明其 caller/consumer，则 fail closed。inline、
  sub-agent、channel 与 native worker 的 provider 结果必须回到唯一 Guru caller，不能自行继续
  下一阶段。
- `explicit_only` 不是“把原始 Skill 留在自动匹配根目录”的许可。它表示该 capability 只能在
  用户明确点名或 Guru `stock-policy owner` 产生 exact explicit binding 后运行，并且必须由
  managed quarantine、不可自动匹配的投影、受控 routing/content guard 或精确 allowlist 之一
  证明普通自然语言不会恢复它。显式请求一旦包含写入意图，就不得调用 raw explicit asset；必须
  在调用前重新分类到 Guru `new change` 或返回 exact active caller，由该 caller 绑定 action scope、
  目标文件、direct consumer 与真实副作用确认。
  raw `trellis-update-spec` 与 raw `trellis-meta` 均归 `suppressed_semantic_route`。code-spec 更新
  必须先由 Guru change lifecycle 形成 repository RDT/Architecture/code-spec contribution，经其
  current governance owner 审核与 promotion 后，才生成最小 `.trellis/spec` projection；不得让
  raw update-spec 直接写入或成为第二个 Docs authority。Trellis architecture/customization 的只读
  能力由 Guru-owned lazy reference projection 保留，并交给 direct-answer 或当前 caller；任何写
  请求必须进入 Guru `new change`/active lifecycle，绑定 canonical workflow/preset/overlay owner、
  exact target 与副作用边界。该 reference projection 不是 raw `trellis-meta` 的 callable/write
  surface，也不得修改 upstream-owned/bundled stock source、repository Requirements/Design/Test、
  Architecture/product/route authority。`trellis-session-insight` 只读历史；`trellis-break-loop` 只可
  输出显式只读诊断与 follow-up 建议，不得执行 spec/Issue/文档/代码写入。任何 follow-up 写入意图
  必须在 raw invocation 前回到 Guru `new change` 或 exact active caller，不得冒充 Guru semantic
  finding/approval，也不得改写上述 authority。普通自然语言、未绑定目标或越出窄边界的请求必须回到 Guru
  `new change` 或 fail closed。
- `EVO-REQ-071`：后续 Design 采用“兼容性优先、最小维护成本”的 stock 决策顺序，不要求为
  每个 asset 穷举所有 disable 载体。若 stock asset 与 Guru semantic owner 重叠且 Guru successor
  已覆盖可观察能力，第一候选是对明确 projection path 的 managed absence 或精确 allowlist delete；
  若该 asset 仍有不可替代的 provider/reference/worker 价值，才比较 caller-bound provider 或
  guarded explicit 保留；只有删除会损失必需能力且存在受支持 owner 时，才考虑 routing/content
  patch 或 quarantine。若兼容成本仍高、会产生第二 owner，或无法证明普通自然语言不会命中，允许
  直接删除该 stock surface，不以“保留上游能力”作为目标。
  Design 只需记录每个 asset 的选择、未选方案的简短否决原因、collision prevention、successor、
  用户修改保护及 fresh install/update/upgrade/reapply 的恢复检查；不要求实现或验证未选的每一种
  patch/absence/quarantine/delete 组合，也不得为保留一个冲突 raw surface 制造逐版本人工 patch loop。
  patch/absence/quarantine/delete 只允许由已选 maintenance/provider caller 在已证明由 Guru
  control-plane owner 管理的 canonical/preset/installed projection
  或其它官方支持扩展面，不得修改全局 npm 安装目录、`node_modules`、Trellis upstream source
  或当前 ownership fact 明确归官方管理但未提供 Guru interception boundary 的路径；删除/absence
  仍只能作用于明确 allowlist，不能使用宽泛 glob 触碰用户 Skill。ownership gate 缺失、来源/目标
  不唯一或只能依赖未支持的 upstream mutation 时，suppressed asset 先得到
  `upstream_suppression_blocked`，provider/explicit/worker asset 先得到
  `provider_boundary_blocked`；不得进入 suppression implementation 选择或声明
  `stock_policy_current`。
- `EVO-REQ-072`：执行 Design 选定的 patch、absence、quarantine、delete、provider binding 或
  explicit guard 前，必须已经存在一个选定 caller 所拥有的 stock policy action；
  `pre_semantic_dispatch_guard` 只能 redirect 或 fail closed，不能在 entry route/action 选择前
  执行上述 mutation。执行 action 时必须消费同一 invocation `context_envelope` 中已经建立且仍然
  current 的 `stock_policy_context`（含 provenance）；若该 projection 尚未建立、已过期或无法
  证明 current，才执行一次最小验证，覆盖 upstream
  package name/version、registry integrity 与 capture tarball identity、source version/path、预期模板
  hash/manifest、目标 projection cell、当前 file state 与是否存在 `.new`/`.bak` sidecar。
  对 `suppressed_semantic_route`，用户修改、来源版本未知、hash 不匹配、同名用户 Skill、未处理
  sidecar 或目标路径不唯一时，必须保留现状并得到 route-local `upstream_suppression_blocked`；对
  `provider_only`、`explicit_only` 与 `controlled_worker_provider`，caller/scope/source identity/
  guard 不完整或同类 provenance 无法证明时，必须保留现状并得到 `provider_boundary_blocked`。
  两类结果都必须说明 affected surface、successor、最后确认 facts 和唯一修复输入；不得静默覆盖、
  删除、把用户修改当成 stock、或让风险路径继续激活 Guru candidate。对新增归入
  `suppressed_semantic_route` 的 raw `trellis-before-dev`、raw `trellis-update-spec` 与 raw
  `trellis-meta`，absence/quarantine/delete 本身不能证明成功：同一 policy action 必须先验证其
  Guru successor capability current，分别为 `EVO-REQ-026` 的 task-free/标准 Phase 2
  `implementation_context`、经 repository RDT/Architecture/code-spec governance 后生成的最小
  `.trellis/spec` projection，以及 Guru-owned lazy read-only Trellis reference + `new change`/active
  lifecycle 写入路线。任一 successor 不可达或能力差集非零时保持
  `upstream_suppression_blocked`，不得用“raw asset 已不存在”冒充 capability preservation。
  若 patch、absence、quarantine
  或 delete 已部分完成、executor/validator 返回 `unknown`，或 action 记录与 live file state 不一致，
  必须按每个 exact role/target/action 归类为已完成、待执行或状态未知，并绑定已完成/待执行动作、
  当前独立的 `file_state`、`context_state`、`sidecar_state`、不可逆动作边界和唯一恢复 owner；已完成或不可逆动作不得重放，状态未知
  不得猜测成功或继续后续动作。恢复时必须复用同一 invocation 中仍然 current 的
  `context_envelope`/stock_policy_context；只有 package/source/projection identity、file/context/sidecar
  state 或 decision-relevant live facts 发生变化、过期或未知时，才定向重新读取受影响的 state，
  只允许从对应 exact policy/caller owner 重入未完成或可安全重试的 action；无法证明安全重试时继续
  保留现状并返回同一 role-local blocked 结果。可保留的最小 provenance 只记录 package/source
  identity、projection cell、action、前后内容 identity、successor/policy、当前 action state 与
  reapply 状态，不记录用户授权或授权过程。若该 policy 检查嵌入 clean-install、existing migration
  或 Release pre-publish，role-local finding 只作为最小输入返回对应 caller，由 caller 形成其
  `clean_install_blocked`、migration 或 `release_pre_publish_blocked` 结果；不得把嵌入检查投影为
  standalone stock terminal。
  本条的 `action` 词汇覆盖全部 stock role，但只对 Design 选定的 action 形成执行闭环：
  `suppressed_semantic_route` 可使用 `patch`、`absence`、`quarantine`、`delete`；
  `provider_only`/`controlled_worker_provider` 可使用 `provider_binding`、`worker_binding`、
  `scope_guard`、`projection_guard`；`explicit_only` 可使用 `explicit_binding`、
  `history_query_guard`、`diagnostic_guard`、`followup_redirect_guard`，这些 action 均不授予 raw
  write authority；九个 `retained_nonsemantic` host row 可使用 `context_preserve`、
  `context_reconcile`；所有角色均可有 `sidecar_reconcile`。未选 action 不要求实现或单独验证，
  但必须记录为何不选。每个已选 exact role/target/action 必须有 `completed`、`pending` 或
  `unknown` 状态和唯一恢复 owner；retained action 不得取得 semantic ownership，无法安全恢复时
  返回 `retained_context_blocked`，而不是伪装成 `stock_policy_current`。
- `EVO-REQ-073`：fresh install 必须先完成官方 Trellis projection，再由 Guru policy 形成
  stock inventory、suppression/provider projection 和 consistency gate；existing migration
  必须在 cutover 前盘点 active/resumable lifecycle、archive/finish/disposition history、用户
  修改 stock 文件与 retained refs，证明每项 current capability 有新 successor 后才能激活新
  contract。`trellis update`、`upgrade`、`workflow switch`、preset reapply 和 fresh `init` 后
  都必须重新验证 policy：官方 update 保留的 user deletion、`--force` 覆盖、`--create-new`
  生成的 `.new`、备份/`.bak` 与重新生成的 stock 文件不得造成第二 semantic owner 或 mixed
  graph。无法安全重应用时沿 standalone role-local 或 clean-install/migration/projection/Release
  pre-publish 的 caller-owned blocked/re-entry 合同停止；retained host context 的 standalone
  failure 使用 `retained_context_blocked`，内嵌 Release policy finding 由 Release owner 形成
  `release_pre_publish_blocked`，不得由 child validator 取得 projection ownership，也不得把
  “上游重新生成”当作自动恢复成功。
- `EVO-REQ-074`：`explicit_only` 只保留 raw `trellis-session-insight` 与 raw
  `trellis-break-loop` 两项：前者提供显式历史检索，后者提供显式诊断；任何会修改 spec、Issue、
  文档或代码的 follow-up 都必须重新进入 Guru `new change` 或返回已绑定 active caller。Trellis
  maintenance、raw `trellis-before-dev`、raw `trellis-update-spec` 与 raw `trellis-meta` 不属于
  `explicit_only`；channel/worker 也只能按 provider/worker caller contract 运行。不得允许用户用
  普通自然语言、direct Skill selection 或 maintenance 文本意外恢复被抑制 semantic route，也不得让
  两项显式保留绕过 `stock-policy owner` 的 exact binding。任何恢复/例外
  都必须绑定具体 asset、scope、caller、时间/版本、projection cell 和不与 Guru owner 重叠的条件；
  例外条件缺失或与当前 lifecycle 冲突时回到 Guru route 或 fail closed，不形成 dual-read、
  dual-write、dual-gate、legacy fallback 或逐版本人工 patch 依赖。`trellis init`、`trellis update`、
  `trellis workflow`、`trellis upgrade` 及其 `--force`/`--create-new` 参数在本需求中只是
  upstream provider test stimulus；若 Guru 后续新增或改变命令、参数、输出语义或退出码，必须
  重新建立 CLI authority 与 `CLI-INTENT-*`，不得把 provider stimulus 偷换成本产品 CLI contract。
  standalone exact explicit-only 的 history/diagnostic 只读请求只能返回
  `explicit_provider_result_current` 给 direct-answer owner 并完成本次 invocation；任何写入意图必须
  在 raw invocation 前进入 `new change` 或回到已绑定 active caller，embedded provider/worker/
  explicit read-only result 只能 `returned_to_unique_caller`。这些结果都不能让 stock-policy owner
  获得 semantic terminal ownership。
- `EVO-REQ-075`：已选 route/caller 的 `stock_policy_evaluation` 必须区分首次动作尚未开始、部分完成和结果未知。
  `pre_semantic_dispatch_guard` 不得创建这些 action state；它只能完成 admission redirect 或
  pre-entry blocked。对同一 exact `(role, target, action)` 集合，若所有 action 均为
  `pending` 且不存在
  `completed` 或 `unknown`，必须先返回 recovery-required 的
  `stock_policy_action_required`，绑定 pending action、exact owner、目标 projection cell、
  `file_state`、`context_state`、`sidecar_state` 和不可逆边界；不得把首次全 pending 当作
  `stock_policy_current`，也不得直接进入 `entry_route_selected`。若存在 `unknown`，它优先于
  `partial` 和 `action_required`；若至少一个 action 已完成且仍有 pending，则为
  `stock_policy_action_partial`。三个中间态都不是成功或 terminal，唯一 consumer 是对应
  `stock-policy owner`/嵌入 caller 的 action owner；经当前对话中必要的真实副作用确认（若该
  action 需要确认）后，或在无须确认的确定性 action 完成后，只能经
  `stock_policy_action_reentry` 复用仍然 current 的 policy context；仅在 identity、state 或
  decision-relevant facts 变化/过期/未知时定向 fresh reread，再重入未完成/安全 action。重入不得重放已完成或
  不可逆 action，无法证明安全时保持同一 role-local blocked。
- `EVO-REQ-076`：每个可能启动顶层 invocation 的用户输入（通常是一条用户消息；已绑定的
  provider/worker return、upstream CLI stimulus、native context 等内部或上游 event 不属于新的用户
  输入）在进入 source-stimulus ranking 或生成 `request_received` 前，必须先经过
  `lifecycle_intent_preclassification`。`active_user_intent` 是这一步的输入总称，
  不是一个可直接进入 source ranking 的结果；preclassification 必须恰好得到
  `lifecycle_bound_user_intent`、`independent_user_request` 或
  `lifecycle_intent_binding_blocked` 之一。只有同时具备且仍 current 的 exact active
  invocation/lifecycle identity、唯一 current phase/owner、受影响 scope、candidate/remote-boundary
  identity、host session/user-event identity、单调到达序列，以及由 active invocation 的
  wait/response/continuation facts 证明的因果绑定时，才得到 `lifecycle_bound_user_intent`；它是
  in-flight 用户事件，不属于 source class，不进入 stock matcher、`request_received` 或
  `entry_route_selected`。bound 结果随后只能由 current/最早受影响 owner 恰好分类为
  `owner_local_additive`、`material_additive` 或 `override`，分别按 `EVO-REQ-041,047` 回原 owner/
  最早受影响 owner。
  `independent_user_request` 只能在以下可观察条件之一成立时作为 preclassification 结果：没有
  active lifecycle；active lifecycle 存在但用户明确声明这是独立的新请求，且当前消息具有唯一 host
  `user-event identity`；或 active lifecycle 仍在运行但 live facts 明确证明该 user-event 与其
  wait/response/continuation、scope、candidate 和 owner 没有因果关联，且当前消息具有唯一
  `user-event identity`。`user-event identity` 是每条消息在 preclassification 前的 host admission fact；
  它不等于新的 invocation identity，后者只由唯一 request-entry consumer 在独立分类成立后分配。仅有普通自然语言、不同主题或消息到达先后，不能单独证明独立；这些证据不足时必须走
  `lifecycle_intent_binding_blocked`。可判定独立后，它不得被旧 owner 吞并，唯一 request-entry consumer
  必须先建立新的 invocation identity 与 `context_envelope`，再恰好生成一次 `request_received`；该 receipt
  只表示 admission 已接收，不表示已选择 top-level route。receipt 后先执行 isolation safety gate：无 active
  lifecycle 时立即 clear 并进入 `pre_semantic_dispatch_guard`；有 active lifecycle 且处于非变更等待/确认，
  或 scope 已证明可隔离时，也进入 `pre_semantic_dispatch_guard` 并选择 route；有 active lifecycle 且共享
  可变 scope/不可逆动作尚未安全隔离，则在 route selection 前进入可发现且有唯一 consumer 的
  `independent_request_isolation_pending`，绑定新 invocation、scope、旧 owner 与 exact re-entry。该
  pending 只有在旧 owner/handle 仍在执行一个安全相关、可观察的 transition，并且明确存在下一次
  可消费的进展事件或状态变化时才合法；“旧 owner 仍存在”、非变更等待/确认、无界外部等待或没有
  下一进展事件都不构成可持续 pending。每次 owner/handle 回程或 isolation 重评估都必须恰好得到：
  观察到进展并刷新当前 pending；已达到安全隔离边界并重入 `pre_semantic_dispatch_guard`；或转为
  `independent_request_isolation_blocked`，绑定唯一 repair input，必要时该 input 可以是一次真实的
  scope/isolation choice。无进展、handle 失效、owner 不再可消费或无法证明下一进展时，必须在该次
  重评估中转为 blocked，不得重复发出 pending 或无限等待。首次安全隔离边界或旧 route current、
  forward-recovered current、terminal block 后只重入 `pre_semantic_dispatch_guard`，复用同一
  envelope/receipt，不再生成 `request_received`；任何独立请求都不得复用旧 invocation 的 envelope、
  candidate 或 route owner。该 liveness 判定采用事件/状态进展，不以相对耗时或轮次阈值验收。
  scope/owner 或隔离边界无法唯一解析时同样得到 `independent_request_isolation_blocked` 与 exact
  re-entry，修复后重新评估 isolation。
  active lifecycle 存在但上述 identity/因果事实既不能证明 bound，也不能证明是独立请求时，必须得到
  `lifecycle_intent_binding_blocked`，只允许一次最高价值澄清或 exact live-fact repair 后回到该
  preclassification；不得降级为 ordinary new request，也不得把所有消息吞入 active owner。没有
  active binding 的普通文本才按 source class 处理。后文 source-stimulus matrix 的六类排序不包含
  该 preclassification 事件。矩阵中的 `worker_return_or_native_context`、
  `guru_bound_provider_or_worker` 与 `upstream_cli_stimulus` 只表示已经通过该入口、且在同一
  invocation/caller 内绑定的后续 stimulus；它们不得自行生成新的 `request_received` 或 top-level
  route，缺少 binding 时只能得到矩阵规定的 blocked/re-entry。
  独立请求的 source stimulus 必须按可观察证据分为
  `worker_return_or_native_context`、`guru_bound_provider_or_worker`、`upstream_cli_stimulus`、
  `explicit_slash_or_platform_command`、`explicit_skill_selection`、`ordinary_natural_language` 六类。
  `explicit_slash_or_platform_command` 必须有精确平台 command file/command-as-skill identity；
  `explicit_skill_selection` 必须有平台提供的 exact Skill identity；`upstream_cli_stimulus` 只进入
  provider test boundary。内部 provider/worker 与 return/context 必须带 caller、scope、source
  identity、profile 和 consumer，不能重新产生 top-level invocation；只有与当前 active invocation
  因果绑定且具备 invocation handle 或 worker identity、caller、scope、source identity、profile 和
  consumer 的 return/context 才合格。孤立 startup hook、session context 或普通 native context
  注入属于 `retained_nonsemantic`，不得消费用户请求、提升 source rank 或改变 Guru route。
  单一 stimulus 的固定优先级为：`worker_return_or_native_context` >
  `guru_bound_provider_or_worker` > `upstream_cli_stimulus` > `explicit_slash_or_platform_command` >
  `explicit_skill_selection` > `ordinary_natural_language`。exact command 与 exact Skill selection
  只有同一 canonical identity 才能折叠，否则 `multiple_source_class` fail closed；任何文本中出现
  的 Skill 名称都不能提升 source class，未知、重复或无法确定 rank 时 fail closed。suppressed asset
  的命中只能在第一项 semantic 行为前由 admission guard redirect，或在 managed suppression 不可
  证明时返回 `upstream_suppression_blocked`；admission guard 不得执行精确移除/delete、quarantine、
  patch 或其它 file/Git/Trellis mutation。上述 mutation 只能由已选且 caller/scope/target 绑定的
  maintenance/provider action 按 `EVO-REQ-072` 承接。provider/worker 绑定不完整返回
  `provider_boundary_blocked`。该矩阵必须包含“文本中提到 `trellis-meta` 或 `trellis-update-spec`
  但没有命令”的负例，证明不会与 direct answer 或 Guru route 产生双匹配。
- `EVO-REQ-077`：官方 `trellis update` 的维护分支必须按 dry-run 的真实 discriminator
  执行：dry-run 输出包含 `MIGRATION REQUIRED` 时，唯一后续命令为
  `trellis update --migrate --skip-all`；不包含时，唯一后续命令为
  `trellis update --skip-all`。两条分支都必须验证 `--skip-all` 保留用户修改，并复用同一
  invocation 中仍然 current 的 update policy context；只有 `.new`、backup/`.bak`、user deletion、
  modified-file decision 或其它 decision-relevant observed state 发生变化、过期或未知时，才对
  受影响 state 做定向 fresh policy reread。不得把 generic `trellis update`、`--force` 或另一分支的
  结果当作本分支成功。命令、参数、输出和退出码仍属于 pinned upstream provider facts，不形成
  Guru CLI intent。
- `EVO-REQ-078`：stock policy 必须采用最小的 pre-semantic dispatch guard。普通
  `direct answer`、未绑定 active lifecycle 的 `stop`、非 stock 的 history query 和两个受支持
  specialist profile 只有在请求或已选 route 实际触及 stock projection/provider/maintenance
  surface 时才进入完整 `stock_policy_evaluation`；无 stock surface 时只读取分类所需的最小
  source/matcher facts，直接进入对应 Guru route。任何请求都不得因为存在 stock inventory 而
  自动扫描全部 package/provenance/file/sidecar，且 guard 不能取得 semantic ownership、改变
  route 或制造 routine question。stock-touching route、显式 stock request、maintenance
  stimulus 和已绑定 provider/worker 才进入完整 policy；其结果仍按唯一 caller 返回。
- `EVO-REQ-079`：每个 provider、explicit 或 worker asset 的 caller/consumer 闭环必须由真实
  identity 或明确的 Design handoff 表示，至少包含 caller、profile、输入范围、最小 result/
  typed exit、唯一 consumer、回程和当前证据 locator。`STOCK-CONSUMER-*` 这种没有 interface、
  schema、typed exit 或 workflow consumer 的名称不得作为 closure 证据；只能改标为
  `consumer_unbound`/`design_handoff`，并说明 standalone read 交给 direct-answer owner、窄
  写入回到 new-change/active caller、embedded result 回到绑定 caller 的投影规则。当前
  `guru-phase2-implementation-coordinator` 若在 workflow/schema 中被引用但 package 中不存在，
  必须标为 `current_drift`/`design_handoff`，不能伪装为 active caller；在该 binding current
  前不得声称 worker/provider closure 或开始 implementation。platform `trellis-implement` 与
  channel `implement` 都必须分别声明 task-free 与标准 Phase 2 两个 input profile；每次 invocation
  只能选择一个 current implementation owner、一个 scope 和一个回程。channel `implement` 不得
  固定绑定 `guru-execute-task-free-change`，也不得在标准 Phase 2 caller 缺失时自行成为 owner。
- `EVO-REQ-080`：Codex native hook 行为必须独立覆盖三种正常配置：`hooks-enabled`（当前
  `UserPromptSubmit` 与 `SubagentStart` matcher 存在）、`hooks-disabled`（配置明确禁用）和
  `no-hook`（无 hook 配置）。Claude/Cursor 的 `trellis-start` hooks-enabled 与
  hooks-disabled/no-hook 分支也必须分别验证。三类高层配置标签是七个 setup discriminator 的派生
  coverage class，不是与七个 cell 再做交叉乘积的第二测试轴。每个 concrete host fixture 必须恰好
  记录一个可重放的
  `(user_feature_flag, project_hook_config, one_time_approval, emission, context_injection)`
  discriminator；每个 supported host 只覆盖对其真实 feature/config/approval surface 适用的
  `enabled_approved`、`enabled_pending`、`enabled_denied`、
  `feature_off_config_present`、`feature_on_config_absent`、`feature_off_config_absent` 和
  `configuration_unknown` 互斥 cell。`enabled_approved|pending|denied` 归入 `hooks-enabled`，
  `feature_off_config_present` 归入 `hooks-disabled`，两个 `*_config_absent` 归入 `no-hook`，
  `configuration_unknown` 只形成 blocked coverage。host 没有一次性批准面时，
  `enabled_pending`/`enabled_denied` 明确为 `not_applicable`，由 host/provider fact 证明；其 enabled
  success cell 使用 `one_time_approval=not_applicable`，不得把缺少该面推断为 granted，也不得制造
  不可能 fixture。每种适用
  setup 都要分别观察 stock command/Skill emission、context injection、suppression/redirect
  结果和 Guru route；`not-emitted`、hook absence、approval pending/denied 或 feature flag off
  都不能单独证明 suppression。任一字段 unknown、配置缺失但仍有 emission、setup 与观察结果不
  一致，或无法证明第一项 semantic 行为前的 redirect 或 fail-closed，就返回对应 role-local
  blocked，并从精确 setup repair 重入。精确移除/delete、quarantine 或 patch 只在
  `EVO-REQ-072` 选定并绑定 maintenance/provider action 后由其承接，不属于 admission guard。

#### Source stimulus and caller binding matrix

下表是 `EVO-REQ-076` 的最小可判定矩阵。第一行是 source ranking 之前的 lifecycle intent
preclassification，不计入六类 source class；其余行的 `Priority` 是唯一的 source-class 优先级（数字越小越高）。
同一 event 若存在多个不同 identity 必须按上文 ambiguity 规则 fail closed；它只定义来源识别与 owner 边界；语义 route 的
产品判断仍由第 3/6 章主定义完成。

| Priority | Stimulus class | 可接受识别证据 | 允许的第一 owner | stock policy 入口 | 负例/回程 |
| --- | --- | --- | --- | --- | --- |
| pre-rank | `lifecycle_bound_user_intent` | exact active invocation/lifecycle identity、唯一 current phase/owner、scope 与 candidate/remote-boundary identity、host session/user-event identity、到达序列，以及 wait/response/continuation facts 的因果绑定全部 current 且唯一 | current/最早受影响 owner | 不进入 source ranking、stock policy 或 top-level entry selection | 绑定不完整/过期/多重/无法证明时得到 `lifecycle_intent_binding_blocked`；独立请求必须先建立新 invocation identity/envelope、恰好生成一次 admission receipt，再通过 isolation safety gate 后进入 source ranking，不得被该 owner 吞并 |
| 1 | `worker_return_or_native_context` | 与 active invocation 因果绑定的 invocation handle 或 spawned worker identity，加 caller、scope、source identity、profile、consumer；孤立 hook/context event 不合格 | 原 Guru caller/host context consumer | 不重新执行 top-level policy 或 entry selection | 只回传最小 result/context；被动 startup/session/native context 不得消费用户请求或抢占 Guru route |
| 2 | `guru_bound_provider_or_worker` | caller、scope、source identity、profile、target 与 consumer 已绑定 | 声明的 Guru caller（例如 `guru-check-task`、`guru-execute-task-free-change`、标准 Phase 2 implementation owner 或 current-drift handoff） | 必须进入 caller-bound policy；provider 不重新选 route | 缺任何 binding 为 `provider_boundary_blocked` |
| 3 | `upstream_cli_stimulus` | pinned `trellis init/workflow/update/upgrade` 命令及 dry-run 输出 | maintenance/provider caller | 进入 `stock_policy_evaluation`，但不创建 Guru CLI intent | 命令语义由 upstream authority 拥有，观察结果回维护 caller |
| 4 | `explicit_slash_or_platform_command` | Claude/Cursor command file、Codex command-as-skill 或平台等价 exact command identity | 对应 Guru command/stock-policy binding | suppressed 命中只允许 admission redirect 或 role-local blocked；精确移除/delete、quarantine、patch 等 action 只能由已选且绑定的 maintenance/provider action 承接 | 同一文本不能再产生 ordinary route；binding 不完整为 role-local blocked |
| 5 | `explicit_skill_selection` | 平台提供的 exact Skill identity 或用户明确选择该 Skill | Guru successor 或 stock-policy owner | 同上；admission 只观测/隔离，不执行 mutation | 仅文字提及不满足此类；结果回唯一 caller |
| 6 | `ordinary_natural_language` | 普通文本，无 exact command/Skill selection binding；即使提到或引用 `trellis-meta`/`trellis-update-spec` 也仍属此类 | Guru `entry_route_selected` owner | 只有 route 实际触及 stock surface 才进入；否则跳过 | 不得由 stock matcher 抢占；若已绑定 Guru caller 的内部调用完成，结果回原 caller |

`guru-phase2-implementation-coordinator` 当前在 workflow/schema 中被引用，但在 active Guru
package 中不存在；因此矩阵中的该 caller 只能标记 `current_drift`/`design_handoff`，不能被
当作已安装可调用 owner。`STOCK-CONSUMER-*` 也只能作为待绑定的 handoff label，不能作为
真实 consumer 证据。

#### Current capability preservation trace

完整 current 能力、上一版 `.40` Design inventory 的 21 个 active Skill 逐项 successor、current
Requirements/NFR/Test coverage、target delta 与 intentionally-not-retained 差集统一维护在
[`current-capability-inventory.md`](./current-capability-inventory.md)。本文件不复制该追踪表；
任何 current capability 没有 target requirement/fixture successor 时，`EVO-REQ-055` 不成立。

## 4. 非功能需求

执行效率、安静性、上下文治理、可靠性、兼容、分发、安全与范围豁免的唯一主定义位于
[`requirement-non-functional.md`](./requirement-non-functional.md)。本文件只在第 5 章定义
这些约束所引用的验收 fixture 和执行成本证据规则，不复制非功能正文。

## 5. 验收 fixture 与执行成本证据

### 5.1 功能与闭环 fixture

`EVO-FIX-LATEST-INTENT` 的前置绑定场景必须覆盖五类可观察输入：无 active lifecycle 的 independent、
active lifecycle 非变更等待/确认中的 independent、共享可变 scope/不可逆动作尚未安全隔离的
independent、完整 current binding 的 lifecycle-bound，以及 binding/isolation facts 无法唯一证明的
ambiguous/blocked。每个 independent 都必须先建立新 invocation identity/envelope，再恰好生成一个只表示
admission receipt 的 `request_received`；无 active、active-wait 或已安全隔离分支随即通过 isolation safety
gate 进入 `pre_semantic_dispatch_guard`，shared-scope 分支则只有在旧 owner/handle 正在执行可观察的
安全相关 transition 且存在下一进展事件或状态变化时，才在 route selection 前进入可发现且有唯一
consumer 的 `independent_request_isolation_pending`。每次 pending re-evaluation 必须恰好观察到进展并
刷新 pending、达到安全边界并重入 guard，或转为 `independent_request_isolation_blocked`；无进展、
handle 失效或 owner 不再可消费时必须在该次重评估中 blocked，不得无限 pending，也不得使用相对耗时
或轮次阈值。安全边界或旧 owner current、forward-recovered current、terminal block 后复用同一
envelope/receipt 继续，不能生成第二次 receipt。
  lifecycle-bound 只回 current/最早受影响 owner；其中 bound `override` 只有在原 owner 完成
  停止、suspend 或不可逆远端收敛后，才由唯一 request-entry consumer 启动一个全新
  invocation/envelope 并恰好生成一次 admission `request_received`；该后续 receipt 不属于 bound
  事件本身。binding 证据不足时只得到
`lifecycle_intent_binding_blocked`，isolation facts 无法证明时只得到
`independent_request_isolation_blocked`，各自在一次澄清或 exact live-fact repair 后重入其原 gate，不能
猜测、无限 pending 或新增 top-level route。

下表的 `EVO-FIX-LATEST-INTENT` 行必须先通过这五类前置输入，再执行其 override/additive 矩阵；两部分
共同构成同一 fixture，不能用后半段代替 admission receipt、isolation 或 blocked re-entry 的验收。

| Fixture | 覆盖 | 必须证明 |
| --- | --- | --- |
| `EVO-FIX-ENTRY-ROUTING` | `REQ-UC-EVO-001,004..006,030,034..039,044..046` | 以代表性请求矩阵证明每个 invocation 恰好落入 direct answer、new change、resume/recovery/history、distribution/release、specialist review 或 stop 之一；矩阵必须显式包含 no-active、active-wait、shared-scope-pending、bound 与 ambiguous/blocked 输入。每个 independent 都先建立新 invocation identity/envelope、恰好生成一次只表示 admission receipt 的 `request_received`；pending 是 route selection 前的中间态，且仅在存在可观察的下一进展事件/状态变化时合法。每次 re-evaluation 必须得到 progress-refresh、safe-clear/re-entry 或 `independent_request_isolation_blocked` 三者之一；no-progress、invalid handle、不可消费 owner、无限 pending 与相对耗时/轮次阈值计数均为 0，安全 re-entry 不重复 receipt，最终 route 仍 exactly-one。new change 再恰好落入 standard/task-free，且只承接真实文件变更；distribution/release 再按 terminal intent、candidate 与 target live current state 恰好落入 standalone projection、clean install、existing migration 或 exact Release；install/migration 先覆盖 `distribution_state_preclassification` 的 `clean_target`、`existing_migration_target`、`foreign_workflow` 与 `distribution_state_blocked`，partial/legacy 不得进入 clean，foreign workflow 不得自动进入 migration，mixed/unknown/unowned/multiple identity 不得猜测。普通解释、事实、状态和信息查询，以及不绑定 active lifecycle、只要求通用 Requirements/Design/代码/Architecture 分析或审核的请求，包括以 Issue/task/branch/repository 为主题但只需答案的请求，都只读最小 live facts 并得到 `direct_answer_completed -> workflow_completed`，不得进入 mode selection、创建资源或扩张为 specialist；只有 `REQ-UC-EVO-037` wording review-only 与 `REQ-UC-EVO-038` qualification 可进入 top-level specialist。分别注入正常 unavailable/access/incomplete live read，必须透明返回 unavailable/unverified fact 与边界、current 虚假断言为 0；需要 archive/finish/disposition durable result identity/currentness 的 query 仍进入 history。unfinished lifecycle 的继续、技术修订或 disposition 不被分类为 direct answer/new change，terminal history 后的新修改不被分类为 resume，exact-candidate 验证/发布与修改其合同/代码互不混淆；Release 的内嵌 projection/install/update gate 不取得 child top-level ownership，clean/existing/foreign target state 与独立 terminal outcome 不混淆；finding、base/provider 变化等 in-flight event 不重新顶层或二级分流。两级真实歧义都只产生一个最高价值问题且在收敛前零副作用 |
| `EVO-FIX-REQUEST-STOP` | `REQ-UC-EVO-044,046` | 在未绑定需处置 active lifecycle、且本 invocation 尚无新副作用时，显式撤回得到 `request_stopped -> workflow_completed`，新资源/写入/cleanup/发布副作用均为 0，既有无关或 suspended work 保持可发现且不变；后续独立新意图由唯一 request-entry consumer 先建立新的 invocation identity/`context_envelope`、恰好生成一次 admission `request_received`，再按 `independent_request_isolation_gate -> pre_semantic_dispatch_guard -> entry_route_selected` 顺序重新分类，不得复用已停止 invocation 的 identity/envelope/candidate/receipt。对已存在 active lifecycle 的取消/放弃/清理请求必须先进入 resume/recovery 并由 `EVO-FIX-ACTIVE-DISPOSITION` 覆盖的 current disposition owner 处理，不得走 top-level stop |
| `EVO-FIX-ACTIVE-DISPOSITION` | `REQ-UC-EVO-046` | 先分别固定 unique current work、equivalent-stale refresh 与 not-found/multiple/unresolved-material-stale recovery block，再对已恢复 exact lifecycle 验证：无不可逆远端副作用时 retain、suspend、abandon/cleanup 三类明确 intent，以及不能唯一判定 retain/abandon 的“取消”意图只产生一次 `active_lifecycle_disposition_choice_required` 且 choice 前 cleanup 为 0；abandon 分别覆盖 deletable owned resource 为 0 的 no-op terminal 与存在 deletable resource 的 exact-plan confirmation。cleanup 确认缺失保持 pending；明确拒绝若未同时给出 retain/suspend，只进入一次唯一 disposition choice，若已给出则直接消费该 choice，任何拒绝都不得产生 `retained \| suspended` 双终点；resource/owner/history facts 变化使旧确认失效，并覆盖 cleanup 成功、部分失败与恢复。已有不可逆远端副作用时旧 route 正常形成既定 current terminal、失败后 forward recover 至 current terminal、terminal block 三类收敛，以及结果 current 后无 eligible local cleanup 与经 current 确认执行 eligible local cleanup 两类分支。retain/suspend 必须保持可发现且唯一 resume owner；abandon 只删除 exact owned resources并保留 unrelated resource、durable history/ref；remote 分支不得删除/回滚/移动/重建远端结果或冒充 cancelled。每个 success 都形成 cleanup 后仍可通过唯一 history owner 查询的最小 durable disposition/history，并得到 `active_lifecycle_disposition_completed -> workflow_completed`；每个正常失败只得到绑定 exact facts/actions/resources 的 `active_lifecycle_disposition_blocked`，恢复后只重入 exact disposition/cleanup step，不重放删除或顶层分流 |
| `EVO-FIX-INTAKE-CLEAR` | `REQ-UC-EVO-001` | 清晰 Issue 零问题进入 requirement ready |
| `EVO-FIX-INTAKE-REVIEWED-DESIGN` | `REQ-UC-EVO-002,014` | reviewed design 被保留并与 current Architecture reconciliation，不被重写或忽略 |
| `EVO-FIX-INTAKE-UNCLEAR` | `REQ-UC-EVO-003` | 每轮一个最高价值问题，直到 ready；无问题批量轰炸 |
| `EVO-FIX-NO-ISSUE` | `REQ-UC-EVO-004` | 无 Issue 的 standard change 不伪造 Issue identity；从请求经 requirement/change readiness、精确资源副作用确认、Workspace/Planning、实现/检查/提交/full-diff review、route selection、Publication/Delivery、`issue_closure_not_applicable`、Finish/Cleanup 到 normal completion，PR/closure 文案不虚构 Issue，且全程无断链 |
| `EVO-FIX-TASK-FREE` | `REQ-UC-EVO-005` | 分别验证显式 task-free、自动高置信适用、可能适用但证据不足、明确需 standard、已有 active task/位置恢复、targeted-check finding 可修订、不可安全继续 blocked 和 post-write scope/risk 扩大；task-free 不创建 Issue/task/worktree、三份 planning 文档或 task/archive history，也不执行 commit/publish/cleanup。finding 修订后 fresh check；blocked 报告 partial edit/未验证边界；scope/risk 扩大立即停止剩余写入并形成 `task_free_escalation_pending`，标准资源副作用前必须完成 scope resolution 与 exact plan confirmation，资源准备后再验证同 scope edit 的唯一归属 reconciliation 或异 scope isolation；全程既不重复已明确意图，也不自动提交、丢弃、复制或清理 partial work |
| `EVO-FIX-DETACHED-READ` | `REQ-UC-EVO-007` | detached/dirty invocation 可 side-effect-free 读取 exact current authority，不创建临时 worktree |
| `EVO-FIX-ARCH-NO-IMPACT` | `REQ-UC-EVO-008` | 快速继续，contribution/ADR 为 0 |
| `EVO-FIX-ARCH-ALIGNED` | `REQ-UC-EVO-009` | design 首稿前读 current baseline/constitution/change contract，最终 alignment 可追踪 |
| `EVO-FIX-ARCH-CONFLICT` | `REQ-UC-EVO-010,014` | requirement 保真，真实冲突阻塞批准并进入明确决策 |
| `EVO-FIX-ARCH-INCOMPLETE` | `REQ-UC-EVO-011` | missing/stale/incomplete authority 在首稿前 stop，repair 后正确重入 |
| `EVO-FIX-ARCH-NEW-DECISION` | `REQ-UC-EVO-012` 的 decision-level 分支 | 合法 task-local contribution 与 ADR candidate 均存在，不写 shared current |
| `EVO-FIX-ARCH-REVISION` | `REQ-UC-EVO-013` | decision/GAP/owner/single-writer/compatibility exit/原则取舍 before-after 完整 |
| `EVO-FIX-ARCH-NO-ADR` | `REQ-UC-EVO-008..009` 与 `REQ-UC-EVO-012` 的 non-decision 分支 | no-impact/alignment 不创建 contribution；非 decision-level baseline 补充可创建 contribution 但 ADR candidate 为 0 |
| `EVO-FIX-FRESH-EQUIVALENT` | `REQ-UC-EVO-016` | stale identity 被识别，正文等价时不重放 semantic review |
| `EVO-FIX-FRESH-SCOPE` | `REQ-UC-EVO-015` | 实质 scope 变化只失效最早受影响结果及下游 |
| `EVO-FIX-TECH-REVISION` | `REQ-UC-EVO-006` | requirement unchanged 时不重入 Phase 0 |
| `EVO-FIX-PLAN-NORMAL` | `REQ-UC-EVO-001,002,009,017,018,033,042` | clear Issue + reviewed design + current aligned RDT/Architecture 从请求进入到 `plan_ready`；entry-route/change-mode selection 前无方案性 repository work/副作用；RDT 前置回读和 impact 先于 task planning；RDT、Architecture 与三份 task 文件按稳定 identity/order 构成主要 context，live delta 位于最小变化 tail；task 三件套仅含 current locator/适用引用与 task-local delta；AI 直接据此完成一次 authoring、一次 evidence-backed approval，零 routine clarification、事务型 handoff、assignment/signoff 或 already-current fact restatement |
| `EVO-FIX-BRANCH-FINDING` | `REQ-UC-EVO-020,022` | finding 修订后 fresh check/commit/full-diff review 闭环 |
| `EVO-FIX-BASE-EVOLUTION` | `REQ-UC-EVO-021` | 无关 base delta 不全链失效；相关 delta 返回最早受影响 owner且不重建 task |
| `EVO-FIX-ARCH-PROMOTION` | `REQ-UC-EVO-023` | serialized promotion 后 fresh Phase 2/commit/review |
| `EVO-FIX-ARCH-DOWNSTREAM-FRESHNESS` | `REQ-UC-EVO-019,022..023,025..026,028..029` | 在 `github_pr` 与 `none` 两种 route 中，current Architecture binding 从 Implementation 经 Phase 2、full-diff review、对应 publication/local acceptance readiness、Acceptance 到 Finish 均可追踪；在各下游责任边界注入正常 identity-equivalent 与 material authority change，前者不重复语义审核，后者返回最早受影响 owner，任何 gate 不消费 stale binding；Cleanup 不重新判断 Architecture |
| `EVO-FIX-RDT-DOWNSTREAM-FRESHNESS` | `REQ-UC-EVO-019..020,022,025..026,028..029,042` | current RDT binding/impact/contribution 从 Planning 经 Implementation、Phase 2、full-diff review、两种 delivery readiness、Acceptance 到 Finish 可追踪；Implementation discovery 会及时回写 task-local contribution；等价 identity 不重审全文，material RDT change 返回最早受影响 owner，任何 gate 不消费 stale RDT，Cleanup 不重新判断 RDT |
| `EVO-FIX-PARALLEL` | `REQ-UC-EVO-024` | 在同一 exact base 上固定 A=`github_pr`、B=`none`，分别执行 A 先完成/合并与 B 先完成两种顺序；task/workspace/branch/contribution/provider/archive/Finish/cleanup/history/retained-ref 全程隔离，B 的 GitHub I/O 为 0。分别向 A 的 provider 与两 task 的 archive、Finish、cleanup 注入正常失败，失败只返回 exact task/current owner，另一 task 可继续且无交叉写入、错误归属、副作用重放或 failure propagation；各自 recovery 后 history/current result 可查询，cleanup 前后 retained commit/ref/history 均可达。shared promotion 后旧 identity 只使实际受影响 task 重算，不形成双 current/writer |
| `EVO-FIX-FULL-NORMAL` | `REQ-UC-EVO-001,009,018..019,022,025,028..029,033,042..043` | 固定小变更从 request 经 entry route、Intake、Base/Context、Workspace、RDT/Architecture-aware Planning、实现/检查/提交/full-diff review、`github_pr` route selection、Publication/Delivery/Merge、closure-current/not-applicable、Finish/Cleanup 到 normal completion，无断链；entry route 前无方案性 work/副作用，task/branch/worktree 名称绑定 current change identity 与语义动作，RDT authority/task contribution 全程 current；各 owner 复用同一稳定 authority/task-doc context，只解析自己的最小 live delta并自主判断，不创建中间 handoff 或重复陈述 current facts；执行与 Phase 2 包含 scope-relevant targeted validation，存在无关异常 submodule 时仍零 submodule action/block |
| `EVO-FIX-SEMANTIC-CONFIRMATION` | `REQ-UC-EVO-051` | 对需要确认的代表性 Issue/workspace/task、commit、push/PR、READY PR merge、Release 与 owned-resource cleanup action，先完整展示 current 精确计划，再分别输入“确认继续”“可以，继续”及其它无歧义语义肯定；每项都必须推进且只推进刚展示的 action。READY PR merge 的肯定直接授权已展示 merge，不要求 `合并PR`。分别注入未完整展示计划、疑问、限制、条件、修改、部分选择、明确拒绝，以及展示后 target/scope/副作用/authority/permission/candidate/HEAD/decision-relevant facts 实质变化；这些输入必须保持副作用为 0，并由 owner 吸收最新意图、重建和重新展示 current 计划或进入 route-local refusal/stop/re-entry。交叉验证 Phase 0/Planning/commit/PR/merge/Release/cleanup 的确认互不扩张或复用；固定 prompt/口令要求、`确认执行 <hash>`、hash/digest challenge、task/path/branch/SHA identity repetition、摘要复述、规定句式、脚本/validator/recorder 解析或验证回复、任何 confirmation/authorization 持久化的计数均为 0 |
| `EVO-FIX-NONE` | `REQ-UC-EVO-026` | current authority 明确选择 `none`；PR readiness、push/PR/merge/Issue closure GitHub 调用均为 0，provider failure 不得自动切入该 route；local acceptance、`issue_closure_not_applicable`、Finish/history/cleanup 仍完整 |
| `EVO-FIX-PROVIDER-RECOVERY` | `REQ-UC-EVO-027,034..036` | 对 Delivery、distribution/projection、clean install、existing migration 与 Release 的每类外部动作绑定 current provider contract/capability、source owner/contract locator/version 和 exact target/action，至少核对输入 identity/字段语义、输出/回执状态、生效时点、权限/错误/部分成功/unknown、幂等与有限重试/停止边界；分别注入 timeout/unavailable、认证缺失、限流/配额、可重试与不可重试拒绝、远端状态变化、unknown outcome、closure mismatch 和 partial external success；每次恢复先重读 live state，区分已完成、未完成与结果未知，自动尝试不超过 Design 声明的有限策略，只在原动作未完成且 contract 允许安全重复时执行；每个 blocked/recovery/wait/partial/unknown 结果都能由 owning boundary 查询其 identity、last confirmed live state、已完成/待执行动作、错误/重试分类、唯一 re-entry 与 unverified boundary；其余路径回到 exact owning boundary 的 recovery/blocked，只 forward recover，不重复副作用、不切换 route 或返回无关阶段 |
| `EVO-FIX-FINISH-RECOVERY` | `REQ-UC-EVO-029` | 对一个普通单 task 分别在 archive/history/finish-summary 收敛前后与 Cleanup 删除部分 owned resource 后注入正常失败；每次先 live reread exact task、history、resource 与 retained-ref facts，Finish failure 只得到绑定已完成/待执行 transition 的 `finish_blocked` 并从 `finish_current` 恢复，Cleanup failure 只得到绑定仍存在/已删除/须保留资源的 `cleanup_blocked` 并从 `owned_resource_cleanup` 恢复。恢复后只补未完成动作，不重放 Delivery、archive、已 current Finish 或已完成删除；durable history 始终可查询，cleanup 前后 retained commit/ref/history 均可达 |
| `EVO-FIX-HISTORY-RESUME` | `REQ-UC-EVO-029..030,046` | session restart、active-work recovery 与 durable history query 只消费 current/live/minimal durable result，不依赖授权、stdout 或长 handoff。resume 分支分别验证恰好一个 current work 直接恢复、stale locator/identity 经 live facts 证明 semantically equivalent 后刷新并恢复，以及 not-found、multiple、unresolved stale/material mismatch 得到 `current_work_recovery_blocked` 并在输入恢复后重入 `current_work_resolution`。history-query 分支分别固定 archived finish result 与 retain/suspend/abandon/remote-outcome disposition result；对 abandonment 必须在 owned-resource cleanup 后从 discoverable history authority 解析，唯一结果得到 `durable_history_result_current -> history_query_completed -> workflow_completed`，不得重入、恢复或激活被查询 lifecycle；not-found/multiple/unresolved-material-stale 得到 `history_query_blocked`，输入恢复后重入 `durable_history_resolution`。retained/suspended work 的继续仍走 resume 分支；两分支均无第二 task、猜测 checkout 或未刷新旧 locator 复用 |
| `EVO-FIX-LATEST-INTENT` | `REQ-UC-EVO-030..031` | 分别在无副作用、Phase 2 后已有可逆本地副作用、不可逆远端副作用前后、长运行 wait 中和 compression/resume 前后注入 override/additive 指令；下一响应必须先消费最新意图。无副作用 override 停止旧 route；停止 current 后，唯一 request-entry consumer 为 override 分配新的 invocation identity/`context_envelope`，恰好生成一次新的 admission `request_received`，随后按 `independent_request_isolation_gate -> pre_semantic_dispatch_guard -> entry_route_selected` 顺序重新执行六类 exactly-one route；本地副作用 override 停止新增写入并保留具有唯一 resume owner 的 exact `suspended_current_work`，随后由唯一 request-entry consumer 使用全新的 identity/envelope、恰好一次 admission receipt，并按同一 isolation/guard/entry 顺序重新分类，新 lifecycle 在任何标准资源副作用前完成 scope/plan confirmation，资源准备后同 scope 完成 reconciliation、异 scope 证明 isolation，不自动提交/丢弃/清理。上述 bound override 的 preclassification 事件本身不得生成 receipt 或再次 preclassify。不可逆远端副作用后的 generic override 保持旧 candidate 不变，分别等待旧 route 正常形成既定 current terminal、失败后 forward recover 至 current terminal 或 terminal block；任一结果 current 后，唯一 request-entry consumer 先为 latest override 分配新的 invocation identity/`context_envelope`，再恰好生成一次新的 admission `request_received`，随后按 `independent_request_isolation_gate -> pre_semantic_dispatch_guard -> entry_route_selected` 顺序重新分类，不得复用旧 identity/envelope/candidate/receipt，并分别验证它恰好分类为 direct answer、new change、resume/recovery/history、distribution/release、specialist review 或 stop 之一，只有 new change 进入二级 mode selection，错误默认 new change 为 0。additive 交叉验证三类：不改变 scope/candidate/route/terminal acceptance 的 owner-local 请求，以及只补充 recovery 输入的请求，均按到达顺序由 current/最早 owner 消费；不可逆远端副作用前的 material additive 返回最早受影响 owner 并重算 freshness；不可逆远端副作用开始后的 material additive 形成绑定原 lifecycle 与到达顺序、可发现且有唯一 consumer 的 `additive_change_pending`，不修改旧 in-flight/published candidate，并分别验证旧 route 正常成功、失败后 forward recover 至 current terminal 与 terminal block 三种收敛；任一结果 current 后，唯一 consumer 先为 pending intent 分配新的 invocation identity/`context_envelope`，再恰好生成一次新的 admission `request_received`，随后按 `independent_request_isolation_gate -> pre_semantic_dispatch_guard -> entry_route_selected` 顺序重新执行六类 exactly-one route，不得复用旧 identity/envelope/candidate/receipt，分别验证它恰好分类为 direct answer、new change、resume/recovery/history、distribution/release、specialist review 或 stop 之一，只有 new change 进入二级 mode selection，错误默认 new change 为 0。所有 pending/latest intent 的丢失、重排、重复消费、提前消费、无 consumer、错误 entry route 与旧 candidate mutation 均为 0 |
| `EVO-FIX-LONG-OUTPUT` | `REQ-UC-EVO-032` | 多次 wait 只返回 delta，稳定 authority/task-doc context 不随累计 stdout 重复注入；invalid handle、累计 stdout 重注入、长 handoff summary 与 already-current fact restatement 均为 0 |
| `EVO-FIX-PROJECTION` | `REQ-UC-EVO-034` | shared `.agents/skills` projection layer + Codex/Claude/Cursor 三个 supported host，以及 canonical/dogfood/installed/preset 的语义一致性只含新合同；target draft 在 current runtime、安装结果和发布说明中均不得被声明为 current/implemented。分别在 `workflow/task_data/docs_authority` 注入 capability loss，并在 Skill API/interface/schema/command、distribution/managed-installed inventory、mode/template hash/sidecar、平台 parity、extension identity/version binding 注入 consistency/installation drift；top-level standalone 两类 failure 都只由 projection owner 得到绑定 exact candidate/surface/gate/mismatch 的 `projection_validation_blocked`，后一类不得被分类为 capability loss。修复后重入 exact `projection_validation`，不得切换 install/migration/Release 或把任一局部 current 冒充 `projection_current` |
| `EVO-FIX-CLEAN-INSTALL` | `REQ-UC-EVO-035` | 仅从 `distribution_state_preclassification=clean_target` 的 repository 执行 supported install；clean predicate 必须证明 active `.trellis/workflow.md` 缺失，且没有任何可唯一归属的 official Trellis/Guru managed installation state，包括 official config/template-hash/scripts/spec/task/workspace/manifest、Guru current workflow/managed projection、未处理 sidecar、active/resumable lifecycle、archive/finish/history 或 retained ref。non-Guru active workflow 的 identity/provenance/owner 或当前安全 transition plan 未唯一收敛时，先形成 `foreign_workflow -> distribution_state_blocked`；收敛后只重入 preclassification 并转为 `existing_migration_target`。可唯一归属的 official Trellis footprint 与上述两类 workflow 状态都作为该 clean fixture 的负例，不得当作普通用户文件或 clean 输入。任一 official/partial/legacy surface 或无法唯一归属的 mixed/unknown state 必须改走 migration 或 `distribution_state_blocked`，不得进入成功路径。成功依次形成 application/validation current 并得到 `new_contract_current`。分别在 application 与 validation 注入本地 finding、内嵌两类 projection-gate finding 及 timeout/unavailable、认证/配额、unknown-outcome/partial-success provider failure；内嵌 validator 只返回最小 finding，clean-install owner 仍唯一得到绑定 exact step、created resources、最后确认 live state 与 unverified boundary 的 `clean_install_blocked` 或 exact-step recovery。前提恢复后重入 exact clean-install step，不生成 `projection_validation_blocked`、`pre_migration_current_preserved`，不猜测旧 authority、切换 distribution route 或把 partial install 冒充 target current |
| `EVO-FIX-MIGRATION` | `REQ-UC-EVO-035` | 仅从 `distribution_state_preclassification=existing_migration_target` 的 repository 执行一个 composite migration invocation；除存在 Guru current workflow 外，必须覆盖只有可唯一归属 official Trellis config/template-hash/scripts/spec/task/workspace/manifest、但 workflow/Guru projection 缺失的 installation footprint，以及 workflow 缺失但可唯一归属的 `.trellis/guru-team/`、shared/host managed projection、`.new/.bak` sidecar、active/resumable lifecycle、archive/finish/history 或 retained ref 等 partial/legacy target。non-Guru active workflow 只有在 identity/provenance/owner 与当前安全 transition plan 均唯一收敛后，才经 preclassification 进入该 existing migration fixture，并由 WORKFLOW-SWITCH 保留至唯一 cutover；在此之前先形成 `foreign_workflow -> distribution_state_blocked`，不得让 WORKFLOW-SWITCH 自动替换它，也不得要求先 mutation 才取得 migration 分类；mixed/unknown/unowned/multiple identity 必须先得到 `distribution_state_blocked`，不得猜测 clean 或 migration。共享 preflight 后按 `MIG-CELL-INSTALL -> MIG-CELL-UPGRADE -> MIG-CELL-UPDATE -> MIG-CELL-WORKFLOW-SWITCH -> MIG-CELL-PRESET-REAPPLY` 顺序执行适用 provider substep；INSTALL 的 `trellis init -y --skip-existing` 只补齐缺失 official/platform files，不替换 existing workflow，workflow target 由显式 preview/force substep 建立。每个 invocation 只执行适用 substep；全部 `not_applicable` 仍须形成 composite current 并执行一次 final validation。preflight 固定包含一个 active/resumable task、一个 completed archive/finish/history result 与 retained commit/ref，先证明逐项 preservation/migration 判定；WORKFLOW-SWITCH 的显式 `--force`（或在该有序 boundary 对已字节相等 target 的 current 观测）是唯一 cutover boundary，invocation-entry byte equality 本身不提前推进 composite cutover，final validation current 前不得派发 target consumer。不可承接项只在 cutover 前得到 `pre_migration_current_preserved` 并停止。只有 composite final validation 成功后 active work 经新合同恢复、archived result 经新合同查询、retained ref/history 保持可达且 legacy runtime consumer 为 0；任何 substep 不单独产生 migration terminal。对共享 preflight、每个 step-local provider/finding、内嵌两类 projection-gate finding 与 provider timeout/auth/quota/unknown-outcome/partial-success 分别取证；内嵌 validator 只返回最小 finding，由 migration owner 按 live cutover state 唯一落入 `pre_migration_current_preserved`、`new_contract_current` 或 `migration_blocked`，不得产生 `projection_validation_blocked`；cutover 后只 forward recover/blocked，不留下旧新 consumer 混合状态或静默历史丢失 |
| `EVO-FIX-RELEASE` | `REQ-UC-EVO-036` | 绑定同一 exact candidate 依次证明 pre-publish 全矩阵、`ready_for_release_confirmation`、独立确认、`release_publication_in_progress`、immutable tag/Release publication、`release_published`、tag-pinned post-publish smoke 与 `release_verified`；分别注入普通 pre-publish finding、内嵌两类 projection-gate finding、确认缺失、明确拒绝、candidate identity/content 变化、decision-relevant provider/target/gate facts 变化、publication provider timeout/auth/quota/unknown-outcome/partial-success、tag 已成功但 GitHub Release 未 current 的 `release_publication_partial`、无法继续 publication 的 `release_publication_blocked`，以及 post-publish 可恢复 prerequisite failure、provider failure 与语义 defect。确认缺失只保持 current wait state 且 publication 副作用为 0；明确拒绝得到 `release_not_published -> workflow_completed` 且 publication 副作用为 0；candidate/关键事实变化必须使旧 wait state 与旧确认不可消费，返回 pre-publish owner，candidate 变化生成新 identity 并完整重跑，live facts 变化重读并重跑全部受影响 gate。内嵌 validator 只返回最小 finding，Release owner 得到 `release_pre_publish_blocked`；修订 candidate 后生成新 identity 并完整重跑 pre-publish，不产生 `projection_validation_blocked` 或进入确认。每次 provider recovery 先重读 live publication state；partial/blocked publication 只从同一 immutable identity 的 publication owner 恢复，post-publish 可恢复失败只从 exact verification step 恢复。语义 defect 必须得到保持原 tag/Release 不变的 `release_published_unverified` terminal block；后续修订先按 `independent_invocation_entry_contract` 完成新 identity/envelope、一次 admission receipt、isolation、pre-semantic guard 与 top-level route，必须重新按内容分类；若分类为 `new change`，先完成独立 change lifecycle，只有后续重新分类为 `distribution/release` 且选择 exact-candidate Release 才生成 new candidate 并完整重跑 Release；其它分类不创建 candidate。不得复用旧 identity/candidate/receipt 或 reforge 原 tag/Release，任何路径都不重复、删除、移动或重建原 tag/Release，局部 PASS 不可相加冒充 release PASS |
| `EVO-FIX-WORDING-EXPLICIT` | `REQ-UC-EVO-037` | 分别验证 review-only 的 standalone 与 active caller，以及 active change-scoped wording：standalone review-only 的 `pass` 与 route-level `specialist_revision_required` 在完整报告结果后得到 `standalone_specialist_completed -> workflow_completed`；active caller 的同类结果回到 `caller_current_route_reentered`；两者都不静默修改被审对象，也不要求额外“修改或 stop”选择，`blocked` 保持各自 caller 的 repair/re-entry。change-scoped wording 的 `pass` 返回 active caller、`content_changed` 丢弃旧结果并完整重建 scope/rescan 后重入、`blocked` 由 caller-owned repair/re-entry 收敛；standalone 与 active caller 不得互相冒充，normal plan 调用数为 0 |
| `EVO-FIX-QUALIFY-EXPLICIT` | `REQ-UC-EVO-017,038` | 明确 caller 请求时 qualification 覆盖 `classified`、`scope_confirmation_required`、`mechanism_revision_required`、`blocked` 四类结果；scope choice 或机制修订前提失败均由对应 owner 投影为 route-local `qualification_blocked`，恢复后完整 fresh 重跑；active caller/standalone 均有唯一回程，普通直接派生 acceptance 场景调用数为 0 |
| `EVO-FIX-CHANGE-REQUEST` | `REQ-UC-EVO-039` | 分别固定 ready、active duplicate、completed duplicate、scope clarification、linked-prerequisite blocked 与 not-found/multiple/unresolved-stale/material-mismatch resolution blocked：ready 才进入 Workspace；active duplicate 返回 exact unfinished owner；completed duplicate 返回 current terminal/history 后 `workflow_completed` 且不重启 task；scope choice current 后重建完整 candidate 并 fresh 重入 readiness，material requirement change 先返回 requirement owner；prerequisite 或 resolution 前提恢复后只重入 readiness。每类均有唯一结果/consumer，不写资源、不重复 authoring、不把 completed duplicate 冒充 active work |
| `EVO-FIX-BASE-REFRESH` | `REQ-UC-EVO-040` | 记录 invocation checkout 刷新前 identity/HEAD/dirty-untracked 状态、selected base/ref/commit/diff、实际 refresh action 与结果；behind authority 按 exact upstream 前进且 invocation checkout 不变；ambiguous/unsafe refresh 明确 blocked |
| `EVO-FIX-SSOT-BOOTSTRAP` | `REQ-UC-EVO-041` | new、partial、stale 和 conflicting repository authority 建立唯一 current 或明确 blocked，不把 inferred 内容冒充 current |
| `EVO-FIX-RDT-LIFECYCLE` | `REQ-UC-EVO-042` | 对同一 current RDT 分别注入真实 no-impact、正常 aligned、明确 RDT delta、missing/stale/conflicting authority 和错误 `no_docs_update_needed/docs_ssot=true`；前三者只能得到与证据相符的 impact，错误 false-no-impact 必须阻塞 approval；isolated contribution、Implementation 中间回写、review revision、expected-current conflict、serialized promotion、promotion 后受影响 evidence 重验与并行隔离全部保持 RDT 追踪和唯一 shared current；task planning 不得冒充 RDT |
| `EVO-FIX-SUBMODULE-BOUNDARY` | `REQ-UC-EVO-043` | parent repo 同时放置 uninitialized、dirty、detached、不可访问或命令失败的无关 submodule；standard 与 task-free/resume 各自执行时，submodule init/update/checkout/sync/递归 scan/read/write/test 调用均为 0，parent authority/readiness/result 不变；显式 submodule change 则进入该 repository 的独立 workflow，不把其 RDT 合并为 parent current |
| `EVO-FIX-STOCK-COEXISTENCE` | `REQ-UC-EVO-047..048` | 以 `current-capability-inventory.md` 的 17 个 logical stock asset、一个 shared `.agents/skills` projection layer、三个 supported host（Codex/Claude/Cursor）和每个 host 的 main/default/inline/sub-agent/channel/native context 维度为矩阵；对 Claude/Cursor 的 `trellis-start` 还必须分别运行 hooks-enabled 与 hooks-disabled/no-hook 配置，不能把 hook 过滤单独计为 suppression；注入 ordinary natural language、exact slash/platform command、direct Skill selection、句中提及但无命令、具有/缺少 active binding 的用户消息、被动 hook/context、Guru-bound provider/worker 与带 active binding 的 worker return/context。证明九项 `suppressed_semantic_route` 在第一项 semantic 行为前只能由 admission guard redirect 或 fail closed；该 fixture 不执行精确移除/delete、quarantine、patch 等 mutation，实际 action 只由 `EVO-FIX-STOCK-MAINTENANCE` 的已选且绑定 caller 承接。`provider_only`/`controlled_worker_provider` 均在真实 caller/profile binding 下回到最小 typed result 和唯一 Guru caller，binding 缺失或不唯一时得到 `provider_boundary_blocked`，`explicit_only` 只在 exact explicit binding 下得到其窄结果且 binding 缺失时保持 `provider_boundary_blocked`，`retained_nonsemantic` 不取得 route ownership。自然语言、explicit selection 与 command collision/redirect 负例覆盖 start/continue/finish/brainstorm/check/spec-bootstrap/before-dev/update-spec/meta 九项 suppressed surface（raw check 必须 redirect 到 `guru-check-task`）；其中 before-dev/update-spec/meta 还必须分别证明 Guru-owned `implementation_context`、governed code-spec contribution-to-projection 与 lazy Trellis reference/new-change successor 可达且 raw 调用数为 0。被动 startup/session/native context 不得消费普通请求或改变 Guru route；`trellis-channel` 使用 caller-bound transport fixture，platform/channel research/implement/check worker 使用 caller/scope/profile-bound worker fixture，且两类 implement worker 均分别覆盖 task-free 与标准 Phase 2 owner；只有 session-insight/break-loop 使用 exact explicit binding 正例。第二个 entry owner、第二次 approval/finding、重复问题/全文读取/副作用与 stock 改写已选 Guru route 的计数为 0；`STOCK-CONSUMER-*` 占位、缺失 caller/profile/typed result 的 retained provider/explicit/worker 行均不得计为通过；unsupported official platform 不被写成 Guru coverage；`trellis-brainstorm`、raw `trellis-spec-bootstrap`、raw `trellis-before-dev`、raw `trellis-update-spec` 与 raw `trellis-meta` 均不得作为 Guru provider，任何新 adapter/reference 必须使用独立 Guru identity 重新审核 |
| `EVO-FIX-STOCK-MAINTENANCE` | `REQ-UC-EVO-049..050` | 在 clean install、existing migration、fresh init、`trellis update`、`upgrade`、workflow switch、preset reapply、`--force`、`--create-new`、用户修改/删除 stock 文件及 `.new/.bak` sidecar 场景中，对每个 asset 只读取一次与所选 action 直接相关的 package/source/version/path、source owner、policy owner、projection cell、template hash/manifest 和独立 file/context/sidecar state；首次全 pending 必须先得到 `stock_policy_action_required`，部分完成/未知分别得到 recovery-required 中间态，安全时才得到 `stock_policy_current`。官方 update 必须先 dry-run 分支：看到 `MIGRATION REQUIRED` 执行 `trellis update --migrate --skip-all`，否则执行 `trellis update --skip-all`，并在两条分支验证 `--skip-all` 保留用户修改。结果按调用边界分流：standalone policy/projection 校验中，所选 suppressed action 的 provenance/owner/内容不安全得到 `upstream_suppression_blocked`，provider/explicit/worker 的 caller/profile、scope、source identity 或 guard 不安全得到 `provider_boundary_blocked`；同一检查作为 clean-install、existing-migration 或 Release pre-publish 的内嵌 gate 时只向对应 caller 返回最小 finding，由 caller 分别形成 `clean_install_blocked`、按 live cutover state 形成 `pre_migration_current_preserved \| migration_blocked`，或形成 `release_pre_publish_blocked`，不得把内嵌结果改投 standalone projection owner。所有分支都只从其 exact caller/owner re-entry，证明不覆盖用户修改、不把未知文件当 stock、不留下 mixed semantic graph/未处理 sidecar、不丢 active/resumable/history/RDT/Architecture/Release capability，也不把 upstream regeneration 当作自动恢复成功；未选的 patch/absence/quarantine/delete 方案不进入本 fixture。 |

`EVO-FIX-ENTRY-ROUTING` 的 distribution preclassification 覆盖还必须包含 official-Trellis-only
existing repository：可唯一归属的 config/template-hash/scripts/spec/task/workspace/manifest 即使没有
active workflow 或 Guru projection，也必须得到 `existing_migration_target`；将其判为 `clean_target`
的计数为 0。疑似 official/Guru state 但 identity/owner 不唯一时仍得到
`distribution_state_blocked`，不得把未知 surface 当作普通用户文件。

`EVO-FIX-ENTRY-ROUTING` 与 `EVO-FIX-MIGRATION` 对 `foreign_workflow` 必须同时覆盖一正一负两类输入：
identity/provenance/owner 或安全 transition plan 未 current 时得到 `distribution_state_blocked` 且 route
mutation 为 0；已识别 non-Guru workflow 的上述 facts 与当前 transition plan 唯一收敛后，只重入
`distribution_state_preclassification`，恰好得到 `existing_migration_target`，并由
`MIG-CELL-WORKFLOW-SWITCH` 在唯一 cutover 前保持 source workflow 不变。不得要求先删除、覆盖或改写
foreign workflow 才能取得 migration 分类，也不得把该正向分支当作 clean install。

`EVO-FIX-STOCK-COEXISTENCE` 与 `EVO-FIX-STOCK-MAINTENANCE` 共享同一 hook setup discriminator：每个
concrete host fixture 必须恰好记录一个 `user_feature_flag`、`project_hook_config`、
`one_time_approval`、`emission` 与 `context_injection` 组合。七个 cell 是每个 supported host 的
applicability-aware partition，不与 `hooks-enabled/hooks-disabled/no-hook` 再做交叉乘积：
`enabled_approved`、
`enabled_pending`、`enabled_denied`、`feature_off_config_present`、`feature_on_config_absent`、
`feature_off_config_absent`、`configuration_unknown` 中，每项只运行 host 实际支持的 cell；无
one-time approval surface 时，`enabled_pending`/`enabled_denied` 以 host/provider fact 明确为
`not_applicable`，enabled success 使用 `one_time_approval=not_applicable`。高层 hook 配置由该 partition
派生，不能把 N/A 计为未覆盖或制造不可能组合。setup 字段 unknown、配置缺失
但仍 emitted、或 setup 与观察不一致时，两个 fixture 都只能得到对应 role-local blocked，并从
精确 setup/policy owner 重入；不能把 hook absence、not-emitted、feature flag off 或 approval
状态当作 suppression，也不能让 maintenance action 在 admission guard 中发生。

`EVO-FIX-STOCK-MAINTENANCE` 的每个上述场景还必须针对 Design 选定的 action 注入首次全 pending、
部分完成、结果 `unknown` 或 action 记录与 live file state 不一致的正常路径；对每个 Design
选定的 exact action 归类为
completed/pending/unknown，首次全 pending 必须得到 `stock_policy_action_required`，并绑定已完成/待执行动作、当前
`file_state`/`context_state`/`sidecar_state`、不可逆边界与唯一恢复 owner。unknown 不得当作成功，已完成或不可逆
action 不得重放；恢复前只在 identity/decision-relevant facts 变化时定向 reread，且只能从对应 exact
caller/owner 重入未完成或可安全重试 action，无法证明安全重试时保持同一 role-local blocked。

该 fixture 只需覆盖每个 role row/retained host row 的 Design 选定 action 及其 user-modification、
reintroduced/unknown 与 blocked/re-entry 分支；未选的 action family 不要求额外执行。channel/worker/
embedded explicit 的窄结果只能回到其绑定 caller；retained action 的失败只能得到
`retained_context_blocked` 并从同一 host/policy owner 重入。对 standalone exact explicit-only 的
history/diagnostic 只读请求，`EVO-FIX-STOCK-COEXISTENCE` 必须额外证明
`explicit_provider_result_current -> direct_answer_completed -> workflow_completed`；任何写入意图
必须在 raw invocation 前重新进入 `new change` 或 active caller，不得由 stock-policy owner 形成
standalone terminal。

### 5.2 执行成本约束与优化证据

本节只定义第 5.1 节 exact fixture/run 的取证与 correctness trace 判读方式，不定义正向行为、
允许/禁止动作、消息类别、handoff 内容、resume route 或质量阈值。执行连续性功能行为只由
`EVO-REQ-044..050` 主定义，质量门槛只由 `EVO-NFR-001..008` 主定义。

- 每份证据必须绑定 exact candidate 与 exact fixture/run，并足以区分 observed action、其被引用的
  direct-consumer/correctness responsibility、current result 和未验证边界；具体 trace 字段、载体与
  采集机制由 Design/Test 决定，不在 Requirements 预选。
- `EVO-FIX-PLAN-NORMAL` 与 `EVO-FIX-FULL-NORMAL` 先证明适用功能、RDT/Architecture、review、
  delivery 与 evidence sufficiency，再用同一 current trace 评估 `EVO-NFR-001..008`；不得把旧 run、
  不同 candidate 或缺失观测拼接为当前 PASS。
- 流程耗时、model/tool rounds、injected bytes、automatic context compression 次数以及相对
  current baseline 的改善比例只可作为诊断和设计优化证据，不作为 Requirements、candidate 或
  Release 的 PASS/FAIL 门槛。
- 为证据分类，`continuation capsule` 指 Guru workflow/Agent/tool 额外生成或持久化、主要用于在
  context compression、session resume 或 owner 边界后继续同一工作的状态摘要；正常 authoritative
  planning 文档、当前对话中的简短阶段结果、平台内部不可见的 compression state 和 live reread
  不属于 capsule。其正向行为与零计数只分别引用 `EVO-REQ-044..047` 和 `EVO-NFR-005,008`。
- `EVO-EVD-002` 继续作为识别重复读取、无效 wait、累计输出、无消费者 locator 和最新意图丢失
  等问题的诊断样本，不作为性能 baseline 或 target 数值来源。

## 6. 必需状态闭环

本章不另立产品 route 合同，而将第 3 章 `EVO-REQ-*` 主定义的 conversational workflow entry、
阶段结果、re-entry 与 terminal 投影为统一状态闭环；它不预先决定 Skill 拆分、typed exit、DTO
或文件布局。每个请求先完成入口分流；change entry 再选择 standard/task-free，不能把
resume/recovery/history、distribution/release 或 specialist request 压回新的 standard Intake：

每个可能启动顶层 invocation 的用户输入（通常是一条用户消息）先完成
`lifecycle_intent_preclassification`；已绑定的 provider/worker return、upstream CLI stimulus 与
native context 不是新的顶层用户输入，不再次执行该 preclassification。只有已判定为
`independent_user_request`、已经建立新的 invocation identity/`context_envelope`、恰好生成一次
admission receipt 且 `independent_request_isolation_gate` 已 clear 的 invocation，才进入
`pre_semantic_dispatch_guard`；同一 invocation 从 `independent_request_isolation_pending`、
`independent_request_isolation_blocked` 或其它 pre-entry blocked/re-entry owner 返回时，也必须先满足
其 exact isolation/re-entry 条件，不能跳过该顺序。由 bound event 在旧 route 收敛后创建的后续新
invocation 同样遵守这条顺序。该 guard 不是所有 request entry 的第一步，而是非语义 admission
boundary：只读取判断来源 stimulus、是否存在 exact stock surface 命中以及已绑定 caller 所需的最小
facts。命中 suppressed surface 时只能 redirect 到 Guru route，或在无法安全隔离时返回
`upstream_suppression_blocked`；provider/worker binding 或 retained host context 不完整时分别返回
`provider_boundary_blocked` 或 `retained_context_blocked`。这些 pre-entry 结果有唯一 repair owner/
re-entry，但不选择 top-level route、不执行 mutation、不触发用户确认交互，也不产生 semantic
question/gate。`lifecycle_bound_user_intent` 及其 owner-local/material/override 事件不进入该 guard、
source ranking 或 stock matcher，只由 current/最早受影响 owner 承接；已绑定的 upstream CLI、provider
或 worker event 继续由其 caller-owned policy evaluation 处理，不重新顶层分流。admission clear/redirect
后才进入 exactly-one `entry_route_selected`。
只有已选 route/caller 实际触及 stock projection/provider/maintenance surface 时，才进入完整
`stock_policy_evaluation` 并要求 `stock_policy_current`；普通 direct answer、非 stock stop、
非 stock history 和受支持 specialist profile 必须跳过完整 inventory/provenance scan。已绑定的
upstream CLI、provider 或 worker event 可直接进入 caller-owned policy evaluation，但不得重新顶层
分流。该 boundary 不得重复读取完整需求或制造 routine question；policy 无法唯一收敛时只由
对应 stock-policy/host/caller owner 在 source/path/hash/sidecar/user-modification facts 仍 current
时复用 `context_envelope` 的 stock policy projection；仅在这些 facts 或 decision-relevant state
变化、过期或未知时定向重入。不得猜测 stock role、让风险 surface 继续匹配，或把 provider failure
改写为 Guru semantic result。

`stock_policy_evaluation` 是已选 route/caller 的 stock-touching action 唯一状态入口，不是
top-level entry selection 的前置替代。它必须先按 exact `(role, target, action)` 读取动作状态：任一动作结果未知、记录与 live state 不一致或不可证明时得到
  `stock_policy_action_unknown`；否则至少一个动作已完成且仍有动作待执行时得到
  `stock_policy_action_partial`；否则所有动作均为 pending 且没有 completed/unknown 时得到
  `stock_policy_action_required`。优先级为 `unknown > partial > action_required`。三个状态都是
  recovery-required 中间态，不是成功或终端；它们必须携带已完成/待执行动作、独立的
  `file_state`、`context_state`、`sidecar_state`、不可逆边界和唯一 owner；复用
  `context_envelope` 中仍 current 的 `stock_policy_context` 与适用 `authority_context`，只有 package/source/projection identity、上述 state 或
  decision-relevant facts 变化、过期或未知时才定向 fresh reread，随后只重入未完成或可安全重试的
  action。重入后只能得到
`stock_policy_current`、对应 suppressed role 的 `upstream_suppression_blocked`、provider/explicit/
worker role 的 `provider_boundary_blocked`，或 retained host row 的 `retained_context_blocked`；不得
从未知/首次 pending 状态猜测成功、重放已完成/不可逆 action，或借 policy result 重新执行
`entry_route_selected`。已选 caller 只在 policy current 后继续自己的 route；pre-entry admission
blocked 则从对应 repair owner 重入 admission，不经过该 action 子图。
fresh install、migration、update/upgrade、workflow switch 与 preset reapply 的 maintenance caller
重入同一子图；它不是只适用于首次 request entry，也不能因嵌入 clean-install/migration/Release
而改投 standalone projection owner。

所有 route-local side-effect confirmation 共享 `EVO-REQ-081` 的对话状态投影，不创建通用
authorization artifact 或第二 semantic owner：

```text
exact_action_owner_current
-> side_effect_plan_current [完整展示 current 精确计划]
-> side_effect_confirmation_pending [副作用=0]
   |-> clear_semantic_affirmative
   |   -> side_effect_confirmation_current [仅当前对话即时消费]
   |      -> exact_displayed_action_execution
   |-> question_or_limit_or_revision_or_partial_choice
   |   -> side_effect_plan_revision_required [副作用=0]
   |      -> exact_action_owner_current
   |-> explicit_refusal
   |   -> route_local_refusal_or_stop_or_reentry [副作用=0]
   `-> material_plan_or_live_fact_change
       -> side_effect_plan_stale [旧确认不可消费，副作用=0]
          -> exact_action_owner_current
```

`clear_semantic_affirmative` 只由 AI 根据当前对话判断，不存在固定字符串/identity matcher 分支；
`确认继续`、`可以，继续` 与语义等价肯定走同一边。READY PR merge 也只在完整 merge 计划已展示后
进入该子图，不另设必须输入 `合并PR` 的 lexical gate。上述状态只表达 observable dialogue/action
边界；script、validator、recorder、DTO、checkpoint、gate 与 history 均不得存储或解析确认。

```text
user_event_received
-> lifecycle_intent_preclassification
   |-> lifecycle_bound_user_intent
   |   |-> owner_local_additive
   |   |   -> current_or_earliest_owner
   |   |      -> caller_current_route_reentered
   |   |         [不生成 request_received、entry_route_selected 或 stock matcher dispatch]
   |   |-> material_additive
   |   |   |-> [remote boundary 前：earliest_affected_owner -> freshness_recomputed]
   |   |   |   `-> caller_current_route_reentered
   |   |   `-> [remote boundary 后：additive_change_pending]
   |   |       -> [旧 route current/forward-recovered current/terminal block 后：唯一 request-entry consumer]
   |   |           -> [分配新 invocation identity、建立新 context_envelope]
   |   |               -> request_received [恰好一次；不复用旧 envelope/candidate/receipt]
   |   |                   -> [common `independent_invocation_entry_contract` continuation]
   |   |-> override
   |   |   |-> [无副作用：旧 route stopped -> 唯一 request-entry consumer 分配新 invocation identity/envelope]
   |   |   |   -> request_received [恰好一次；不复用旧 identity/envelope/candidate/receipt]
   |   |   |       -> [common `independent_invocation_entry_contract` continuation]
   |   |   |-> [可逆本地副作用：suspended_current_work -> 唯一 request-entry consumer 分配新 invocation identity/envelope]
   |   |   |   -> request_received [恰好一次；不复用旧 identity/envelope/candidate/receipt]
   |   |   |       -> [common `independent_invocation_entry_contract` continuation]
   |   |   `-> [不可逆远端副作用：旧 owner current/forward-recovered current/terminal block 后：唯一 request-entry consumer]
   |   |       -> [分配新 invocation identity、建立新 context_envelope]
   |   |           -> request_received [恰好一次；不复用旧 envelope/candidate/receipt]
   |   |               -> [common `independent_invocation_entry_contract` continuation]
   |-> lifecycle_intent_binding_blocked
   |   -> [一次最高价值澄清或 exact live-fact repair 后：
   |       lifecycle_intent_preclassification]
   `-> independent_user_request [preclassification 已证明独立]
       -> [唯一 request-entry consumer 建立新 invocation identity 与 context_envelope]
          -> request_received [恰好一次 admission receipt；尚未选择 top-level route]
             -> independent_request_isolation_gate
                |-> [无 active lifecycle，或旧 lifecycle 非变更等待/确认，或 scope 已证明可隔离：
                |   pre_semantic_dispatch_guard]
                |-> [有 active lifecycle 且共享可变 scope/不可逆动作尚未安全隔离：
                |   independent_request_isolation_pending]
                |   |-> [旧 owner/handle 仍在安全 transition 且出现可消费进展事件：刷新 pending]
                |   |-> [首次安全隔离边界，或旧 owner current/forward-recovered current/terminal block 后：
                |   |   pre_semantic_dispatch_guard；复用既有 envelope/receipt]
                |   `-> [无进展、handle 失效、owner 不可消费或下一进展不可证明：
                |       independent_request_isolation_blocked；绑定唯一 repair/choice，复用 envelope/receipt]
                `-> [isolation facts 无法唯一解析：independent_request_isolation_blocked]
                    -> [唯一 scope/owner/live fact current 后：independent_request_isolation_gate；
                        复用既有 envelope/receipt]

上方所有 bound 后续 invocation 与 independent request 都汇入同一条
`independent_invocation_entry_contract` continuation；其完整展开如下：
request_received [admission receipt 已生成；随后完成适用的 isolation gate，clear 后才进入下方 guard]
-> pre_semantic_dispatch_guard
   |-> admission_redirect_to_guru
   |   `-> entry_route_selected
   |-> admission_blocked
   |   |-> upstream_suppression_blocked
   |   |   `-> [exact suppression owner 修复后：pre_semantic_dispatch_guard]
   |   |-> provider_boundary_blocked
   |   |   `-> [exact caller/provider owner 修复后：pre_semantic_dispatch_guard]
   |   `-> retained_context_blocked
   |       `-> [exact host/policy owner 修复后：pre_semantic_dispatch_guard]
   `-> admission_clear
       `-> entry_route_selected
          `-> [已选 route/caller 实际触及 stock surface 时：stock_policy_evaluation]
             |-> stock_policy_action_unknown
             |   -> stock_policy_action_reentry
             |      -> [复用 envelope 中仍 current 的 stock policy/authority projection；仅在
             |          identity/state/decision-relevant facts 变化、过期或未知时定向 reread：只重入
             |          未完成或可安全重试 action]
             |         |-> stock_policy_current
             |         |-> upstream_suppression_blocked
             |         |-> provider_boundary_blocked
             |         `-> retained_context_blocked
             |-> stock_policy_action_partial
             |   -> stock_policy_action_reentry
             |      -> [复用同一 envelope 的 package/source/projection/file/context/sidecar state；
             |          仅在 identity/state/decision-relevant facts 变化、过期或未知时定向 reread，
             |          并按 exact owner 只重入 pending/安全 action]
             |         |-> stock_policy_current
             |         |-> upstream_suppression_blocked
             |         |-> provider_boundary_blocked
             |         `-> retained_context_blocked
             |-> stock_policy_action_required
             |   -> stock_policy_action_reentry
             |      -> [必要的真实副作用确认/确定性 action 完成后复用仍 current envelope；仅在
             |          identity/state/decision-relevant facts 变化、过期或未知时定向 reread，
             |          只执行 pending/安全 action]
             |         |-> stock_policy_current
             |         |-> upstream_suppression_blocked
             |         |-> provider_boundary_blocked
             |         `-> retained_context_blocked
             `-> stock_policy_current
                 `-> [回到已选 caller 的 route-local continuation；不重新执行顶层 entry selection]
entry_route_selected (admission clear/redirect；stock-touching route 先满足 stock_policy_current)
   |-> direct_answer_request
   |   |-> explicit_provider_request
   |   |   -> explicit_provider_result_current
   |   |   -> direct_answer_completed
   |   |      -> workflow_completed
   |   `-> [只读回答所需的零项或最小 live facts；
   |       不可用时透明返回 unavailable/unverified boundary]
   |       -> direct_answer_completed
   |       -> workflow_completed
   |
   |-> change_request (new change)
   |   -> change_mode_selected
   |      |-> task_free_candidate
   |      |   -> task_free_prewrite_current
   |      |   -> task_free_change_applied
   |      |   -> task_free_validation_current
   |      |   -> task_free_finished
   |      |   -> workflow_completed
   |      |
   |      `-> standard_request
   |          -> base_current
   |          -> repository_authority_current
   |          -> requirement_ready
   |          -> change_request_readiness
   |             |-> active_duplicate_current
   |             |   -> exact_unfinished_owner_reentered
   |             |-> completed_duplicate_current
   |             |   -> current_terminal_result_returned
   |             |   -> workflow_completed
   |             |-> change_request_scope_clarification_required
   |             |   -> [scope choice current、完整 candidate 重建后：
   |             |       change_request_readiness]
   |             |-> change_request_prerequisite_blocked
   |             |   -> [prerequisite current 后：change_request_readiness]
   |             |-> change_request_resolution_blocked
   |             |   -> [唯一输入/live repair current 后：change_request_readiness]
   |             `-> change_request_ready
   |                 -> [存在 suspended current work 时：
   |                     suspended_work_scope_resolved
   |                     -> suspended_work_plan_confirmed]
   |                 -> workspace_ready
   |                 -> [存在 suspended current work 时：
   |                     suspended_work_reconciled | suspended_work_isolated]
   |                 -> rdt_alignment_current
   |                 -> architecture_alignment_current
   |                 -> plan_ready
   |                 -> implementation_checked
   |                 -> task_committed
   |                 -> branch_reviewed
   |                 -> [存在 Architecture/RDT contribution 时：
   |                     contribution_reviewed
   |                     -> shared_current_promoted
   |                     -> affected_authority_reconciled
   |                     -> affected implementation/check/commit/full-diff review 重算
   |                     -> branch_reviewed]
   |                 -> delivery_route_selected
   |                    |-> github_pr_delivery
   |                    |   -> publication_ready
   |                    |   -> pre_delivery_accepted
   |                    |   -> remote_delivery_current
   |                    |   -> merged
   |                    |   -> [issue_closure_current | issue_closure_not_applicable]
   |                    |   -> delivery_terminal
   |                    |
   |                    `-> none_delivery
   |                        -> local_acceptance_ready
   |                        -> pre_delivery_accepted
   |                        -> issue_closure_not_applicable
   |                        -> delivery_terminal
   |                 -> finish_current
   |                    |-> finish_blocked
   |                    |   -> [前提恢复并 live reread 后：finish_current]
   |                    `-> finished
   |                        -> owned_resource_cleanup
   |                           |-> cleanup_blocked
   |                           |   -> [前提恢复并 live reread 后：owned_resource_cleanup]
   |                           `-> owned_resources_cleaned
   |                               -> workflow_completed
   |
   |-> resume_recovery_or_history_request
   |   |-> current_work_resume_or_recovery
   |   |   -> current_work_resolution
   |   |      |-> current_work_recovered
   |   |      |   |-> current_work_continuation
   |   |      |   |   -> latest_intent_reconciled
   |   |      |   |   -> earliest_current_owner
   |   |      |   |   -> re-enter exact current change/task/delivery state
   |   |      |   |
   |   |      |   `-> active_lifecycle_disposition
   |   |      |       |-> active_lifecycle_disposition_blocked
   |   |      |       |   -> [exact facts current 后：
   |   |      |       |       active_lifecycle_disposition]
   |   |      |       |-> active_lifecycle_disposition_choice_required
   |   |      |       |   -> [唯一 disposition choice current 后：
   |   |      |       |       active_lifecycle_disposition]
   |   |      |       |-> [retain/suspend：
   |   |      |       |    active_lifecycle_retained | active_lifecycle_suspended]
   |   |      |       |   -> active_lifecycle_disposition_history_current
   |   |      |       |   -> active_lifecycle_disposition_completed
   |   |      |       |   -> workflow_completed
   |   |      |       |-> active_lifecycle_cleanup_plan_current
   |   |      |       |   |-> no_deletable_owned_resources
   |   |      |       |   |   -> active_lifecycle_abandoned
   |   |      |       |   |   -> active_lifecycle_disposition_history_current
   |   |      |       |   |   -> active_lifecycle_disposition_completed
   |   |      |       |   |   -> workflow_completed
   |   |      |       |   |-> active_lifecycle_cleanup_confirmation_pending
   |   |      |       |   |   -> [current 确认后：
   |   |      |       |   |       active_lifecycle_cleanup_plan_current]
   |   |      |       |   |-> active_lifecycle_cleanup_confirmation_refused
   |   |      |       |   |   |-> [回复已包含唯一 retain/suspend choice：
   |   |      |       |   |   |    active_lifecycle_disposition]
   |   |      |       |   |   `-> [回复未包含唯一 choice：
   |   |      |       |   |        active_lifecycle_disposition_choice_required]
   |   |      |       |   |       -> [唯一 retain/suspend choice current 后：
   |   |      |       |   |           active_lifecycle_disposition]
   |   |      |       |   `-> active_lifecycle_owned_cleanup
   |   |      |       |       |-> active_lifecycle_disposition_blocked
   |   |      |       |       |   -> [live reread 后：
   |   |      |       |       |       active_lifecycle_owned_cleanup]
   |   |      |       |       `-> active_lifecycle_abandoned
   |   |      |       |           -> active_lifecycle_disposition_history_current
   |   |      |       |           -> active_lifecycle_disposition_completed
   |   |      |       |           -> workflow_completed
   |   |      |       `-> irreversible_remote_disposition_boundary
   |   |      |           -> original_remote_owner_current
   |   |      |              |-> lifecycle_terminal_current
   |   |      |              |-> lifecycle_forward_recovered_terminal_current
   |   |      |              `-> lifecycle_terminal_block_current
   |   |      |           -> remote_local_cleanup_resolution
   |   |      |              |-> no_eligible_or_requested_local_cleanup
   |   |      |              |-> active_lifecycle_cleanup_confirmation_pending
   |   |      |              |   -> [facts/current 确认后：
   |   |      |              |       remote_local_cleanup_resolution]
   |   |      |              |-> cleanup_confirmation_refused
   |   |      |              `-> [current plan/确认：active_lifecycle_owned_cleanup]
   |   |      |                  |-> active_lifecycle_disposition_blocked
   |   |      |                  |   -> [live reread 后：
   |   |      |                  |       active_lifecycle_owned_cleanup]
   |   |      |                  `-> eligible_local_resources_cleaned
   |   |      |           -> active_lifecycle_remote_outcome_current
   |   |      |           -> active_lifecycle_disposition_history_current
   |   |      |           -> active_lifecycle_disposition_completed
   |   |      |           -> workflow_completed
   |   |      |
   |   |      `-> current_work_recovery_blocked
   |   |          -> [所需唯一输入或 live repair current 后：
   |   |              current_work_resolution]
   |   |
   |   `-> durable_history_query
   |       -> durable_history_resolution
   |          |-> durable_history_result_current
   |          |   -> history_query_completed
   |          |   -> workflow_completed
   |          |
   |          `-> history_query_blocked
   |              -> [所需唯一输入或 live repair current 后：
   |                  durable_history_resolution]
   |
   |-> distribution_or_release_request
   |   -> distribution_candidate_current
   |      |-> distribution_action_selected=standalone_projection_validation
   |      |   -> projection_validation
   |      |   |-> projection_validation_blocked
   |      |   |   -> [exact candidate/surface 修复后：projection_validation]
   |      |   `-> projection_current
   |      |       -> distribution_validation_completed
   |      |       -> workflow_completed
   |      |
   |      |-> distribution_action_selected=exact-candidate Release
   |      |   `-> exact_release_candidate_current
   |          -> release_pre_publish_validation_current
   |             |-> release_pre_publish_blocked
   |             |   -> [candidate 修订并生成新 identity：
   |             |       release_pre_publish_validation_current]
   |             `-> ready_for_release_confirmation
   |                 |-> [确认缺失且 candidate/facts current：
   |                 |    ready_for_release_confirmation]
   |                 |-> release_not_published
   |                 |   -> workflow_completed
   |                 |-> [candidate 或 decision-relevant facts 变化：
   |                 |    release_pre_publish_validation_current]
   |                 `-> release_publication_in_progress [current 对话确认]
   |                    |-> release_publication_partial
   |                    |   |-> [同一 identity 的恢复前提 current 后：
   |                    |   |    release_publication_in_progress]
   |                    |   `-> release_publication_blocked
   |                    |       -> [同一 identity 的恢复前提 current 后：
   |                    |           release_publication_in_progress]
   |                    |-> release_publication_blocked
   |                    |   -> [同一 identity 的恢复前提 current 后：
   |                    |       release_publication_in_progress]
   |                    `-> release_published
   |                        -> post_publish_verification_current
   |                           |-> release_post_publish_blocked
   |                           |   `-> [可恢复前提 current 后：
   |                           |        post_publish_verification_current]
   |                           |-> release_published_unverified [terminal block；
   |                           |    后续修订由唯一 request-entry consumer 分配新的 invocation identity、建立新的
   |                           |    context_envelope、恰好生成一次 admission request_received，随后按
   |                           |    independent_request_isolation_gate -> pre_semantic_dispatch_guard -> entry_route_selected
   |                           |    顺序重新分类；只有 new change 进入二级 mode selection；只有重新分类为
   |                           |    distribution/release 且选择 exact-candidate Release 才创建 new candidate]
   |                           `-> release_verified
   |                               -> workflow_completed
   |      |
   |      `-> distribution_state_preclassification [install/migration only]
   |          |-> clean_target [active workflow absent and no attributable official Trellis/Guru managed state]
   |          |   `-> distribution_action_selected=clean_repository_installation
   |          |       -> clean_install_application_current
   |          |          |-> clean_install_blocked
   |          |          |   -> [application 前提恢复后：clean_install_application_current]
   |          |          `-> clean_install_validation_current
   |          |              |-> clean_install_blocked
   |          |              |   -> [validation 前提恢复后：clean_install_validation_current]
   |          |              `-> new_contract_current
   |          |                  -> distribution_validation_completed
   |          |                  -> workflow_completed
   |          |
   |          |-> existing_migration_target [official Trellis/Guru current or uniquely attributable partial/legacy state]
   |          |   `-> distribution_action_selected=existing_repository_migration
   |          |       -> migration_preflight_current
   |          |          |-> pre_migration_current_preserved
   |          |          |   -> [修复/输入恢复后：migration_preflight_current]
   |          |          `-> migration_application_current [cutover 前]
   |          |              |-> pre_migration_current_preserved [仅 live cutover 尚未开始]
   |          |              |   -> [前提恢复后：migration_application_current]
   |          |              `-> migration_cutover_current
   |          |                  |-> migration_blocked
   |          |                  |   -> [forward-recovery 前提恢复后：migration_cutover_current]
   |          |                  `-> migration_preset_reapply_current
   |          |                      [MIG-CELL-PRESET-REAPPLY step current，或有依据的 not_applicable current observation]
   |          |                      |-> migration_blocked
   |          |                      |   -> [preset-reapply forward-recovery 前提恢复后：migration_preset_reapply_current]
   |          |                      `-> migration_final_validation_current
   |          |                          |-> migration_blocked
   |          |                          |   -> [final-validation forward-recovery 前提恢复后：migration_final_validation_current]
   |          |                          `-> new_contract_current
   |          |                              -> distribution_validation_completed
   |          |                              -> workflow_completed
   |          |
   |          |-> foreign_workflow [non-Guru transition plan not current, or provenance/ownership is not uniquely bound]
   |          |   `-> distribution_state_blocked
   |          |       -> [一次 clarification/live repair 后：distribution_state_preclassification；
   |          |           resolved non-Guru transition -> existing_migration_target]
   |          `-> distribution_state_blocked [mixed/unknown/unowned/multiple or otherwise unresolved]
   |              -> [一次 clarification/live repair 后：distribution_state_preclassification]
   |
   |-> specialist_review_request [仅 REQ-UC-EVO-037 wording review-only
   |                               或 REQ-UC-EVO-038 qualification]
   |   -> specialist_scope_current
   |      |-> wording_review_result_current [review-only]
   |      |   |-> wording_pass
   |      |   |   -> returned_to_unique_caller
   |      |   |      |-> [active caller] caller_current_route_reentered
   |      |   |      `-> [standalone caller] standalone_specialist_completed
   |      |   |          -> workflow_completed
   |      |   |-> specialist_revision_required
   |      |   |   -> revision_findings_reported
   |      |   |   |-> [active caller] caller_current_route_reentered
   |      |   |   `-> [standalone caller] standalone_specialist_completed
   |      |   |       -> workflow_completed
   |      |   `-> wording_review_blocked
   |      |       -> [caller 修复 authority/scope/semantic precondition 后：
   |      |           wording_review_result_current]
   |      |
   |      `-> qualification_result_current
   |          |-> qualification_classified
   |          |   -> returned_to_unique_caller
   |          |      |-> [active caller] caller_current_route_reentered
   |          |      `-> [standalone caller] standalone_specialist_completed
   |          |          -> workflow_completed
   |          |-> qualification_scope_confirmation_required
   |          |   |-> [唯一澄清 owner 取得一次 scope choice、原 caller
   |          |   |    重建完整 candidate set 后：qualification_result_current]
   |          |   `-> [澄清 profile blocked：qualification_blocked]
   |          |-> qualification_mechanism_revision_required
   |          |   |-> [原机制 owner 完成删除/替换后：
   |          |   |    qualification_result_current]
   |          |   `-> [修订前提 blocked：qualification_blocked]
   |          `-> qualification_blocked
   |              -> [caller 修复 authority/candidate/consumer freshness 后：
   |                  qualification_result_current]
   |
   `-> request_stopped
       -> workflow_completed
```

图中 `user_event_received` 的 preclassification 是所有可能启动顶层 invocation 的用户输入的唯一
前置分流；已绑定的 provider/worker return、upstream CLI stimulus 与 native context 不产生新的
`user_event_received`。bound intent
只能回 current/最早受影响 owner；independent intent 先取得新 invocation identity/最小 envelope，
再恰好产生一次 admission-only `request_received`，并在 isolation safety gate clear 后才进入六类
route。两者不得共享一个未标识的 invocation identity；pending/blocked re-entry 复用既有 receipt。
`lifecycle_intent_binding_blocked` 只允许一次澄清或 exact live-fact repair 后回到 preclassification，不能
猜测为 bound 或 independent。该前置分流不改变六类
`entry_route_selected` 的产品定义，也不把 lifecycle-bound intent 计作第七类 top-level route。

图中的 `explicit_provider_result_current` 只属于 standalone exact explicit-only 的 history/diagnostic
只读请求，并由 direct-answer owner 消费；它不是 provider 自有 terminal。direct-answer owner 内部
调用的 channel/research/check provider，以及 active change/resume/distribution caller 内嵌调用的 provider/
worker/explicit result 统一走
`provider_result_current -> returned_to_unique_caller -> caller_current_route_reentered`，继续原 caller
的 current route；其中 direct-answer caller 随后形成 `direct_answer_completed`。任何写入意图都必须
在 raw explicit invocation 前重新分类，且没有 standalone provider terminal。binding、target、consumer 或
action state 不 current 时先得到 `provider_boundary_blocked` 或第 6 章开头的 action recovery 状态，
不得绕过 caller 或重新执行 top-level entry selection。

图中的 `specialist_review_request` 只表示 `REQ-UC-EVO-037` contract wording review-only 或
`REQ-UC-EVO-038` supported normal-scenario qualification 两个 top-level explicit specialist
profile，因此 wording 分支只承载 review-only 结果；standalone caller 的 `pass` 或完整 revision
findings 报告后进入 standalone completion，active caller 的同类结果回到其 current route，只有
blocked 保持各自 caller 的 repair/re-entry。其它不绑定 active lifecycle、
不修改对象的通用 Requirements/Design/代码/Architecture 只读分析或审核走 direct answer，不得在
状态图外发明第三个 specialist profile。wording review 或 qualification 由 active
workflow caller 内嵌调用时保持 caller-local：复用同一 result/owner/re-entry，不重新进入 top-level
`specialist_review_request` 或 `entry_route_selected`。change-scoped wording 的 `content_changed` 只在
active caller 内成立，并按 `EVO-REQ-057` 丢弃旧结果、重建完整 scope/rescan 后 fresh 重入
`wording_review_result_current`。review-only 的 `specialist_revision_required` 不直接生成 change route；
只有用户明确提出新的修改意图后，才从新的 `request_received` 完整执行 `entry_route_selected`。

`entry_route_selected` 只基于当前请求和最小 live facts，不表示已取得后续 Git/GitHub/Trellis
副作用授权。`direct_answer_request` 只在答案本身是 terminal outcome 时成立；它可以读取回答所需的
最小 live repository/provider facts，但不得调用 change mode、创建资源、修改被审对象或借回答启动
lifecycle。所需事实因正常 unavailable/access/incomplete response 无法核实时，必须返回明确的
unavailable/unverified 边界并禁止 current 断言，仍诚实完成本次 direct answer；不得仅为读取失败创建
blocked lifecycle。若用户请求的是 archive/finish/disposition durable result 本身，且必须解析其
identity/currentness，则进入 history owner，而不是把该 resolution 藏进 direct answer。

`task_free_finished` 只返回本次 invocation 的 actual edited paths、concise validation
result 与 unverified boundaries，不产生 standard task 的 planning、archive、publication 或 cleanup
resource。`task_free_validation_current` 只在 pre-write suitability、targeted check 与 post-write
scope/risk review 均 current 时成立。

`change_request_readiness` 只拥有 duplicate/prerequisite/scope/independent-unit 判断，不拥有
requirement authoring 或 Workspace 创建。active duplicate 返回 unfinished current owner；completed
duplicate 返回 current terminal/history 并结束本 invocation；scope clarification、prerequisite 与
resolution blocked 都只在各自前提 current 后 fresh 重入 readiness。任何 material requirement intent
变化必须先回到最早受影响 requirement owner，不能在 readiness 内静默改写 scope。

`task_free_escalation_pending` 与 `suspended_current_work` 都必须保持可发现的 exact source identity
和唯一 resume owner。它们进入 standard 或新的 change lifecycle 时，必须先于任何标准资源副作用
完成 scope resolution、exact plan confirmation 并得到 `suspended_work_plan_confirmed`；资源准备后、
Planning 前再恰好得到 `suspended_work_reconciled` 或 `suspended_work_isolated`。无法确定 scope、形成
精确计划、取得确认、证明唯一 owner 或验证资源隔离时只能 blocked，不能先创建第二套资源或把原
edit 静默混入新 workspace。

`additive_change_pending` 只承载不可逆远端副作用开始后到达的 material additive。它由原远端
owner 创建并保持可发现，最小绑定原 lifecycle/current candidate、用户意图与到达顺序，不包含授权
过程或可重建 evidence；原远端 owner 仍是旧 lifecycle 的唯一 owner，pending intent 不参与其
  publication、Finish 或 Cleanup 判断。只有原远端动作已正常形成既定 current terminal、失败后
  forward recover 至 current terminal，或形成 terminal block，新的 request entry owner 才是该 pending
  result 的唯一 consumer，并且唯一 re-entry 是按
  `independent_invocation_entry_contract` 建立新 identity/envelope、生成一次 admission receipt 后，
  依次通过 isolation、pre-semantic guard 与 `entry_route_selected`。
它可进入六类顶层 route 中任一类，只有 new change
才继续 `change_mode_selected` 与独立 change lifecycle；不得默认 new change、返回旧
lifecycle 的 Requirements/Planning/Implementation、静默修改已发布 identity，或让其它 caller 提前
消费、丢弃、重排该 intent。

不可逆远端副作用后的 generic override 不属于 `additive_change_pending`。按 `EVO-REQ-047`，原 owner
先保持旧 candidate 不变并完成既定 route 的 current terminal、forward-recovered terminal 或 terminal
  block；随后唯一 request-entry consumer 按 `independent_invocation_entry_contract` 为 latest override
  建立新 identity/envelope、生成一次 admission receipt，再依次通过 isolation、pre-semantic guard 与
  `entry_route_selected`。它可进入六类顶层 route 中任一类，只有 new change 才继续二级 mode selection。

`resume_recovery_or_history_request` 必须先按用户意图与 live facts 区分 resumable current work 和
archive/finish/disposition durable history query。前者恢复成功后，再按当前意图区分 continue/recovery 与
`active_lifecycle_disposition`；continue 才重入 earliest current owner，retain/suspend/abandon/cleanup
必须按 `EVO-REQ-067` 到达 disposition terminal 或 exact blocked re-entry。存在不可逆远端副作用时，
disposition 不能夺取原远端 owner，也不能把远端 current/terminal block 改写为 cancelled；只有原 owner
收敛后才处理允许的本地 cleanup。durable history query 只返回 current history result 并以
`history_query_completed` 结束，不能恢复或重新激活被查询 lifecycle；retained/suspended work 的继续
请求仍走 current-work recovery。recovery、history 与 disposition 的 blocked 结果各自只重入其 exact
resolution/disposition/cleanup owner，不得混用。

`delivery_route_selected` 必须绑定 current change/task authority。`none` 不是 `github_pr` provider
失败的 fallback；两条 route 只在各自 readiness 和 Acceptance 后进入 terminal。`github_pr` 在 merge
后仍须得到 current Issue closure 结果；无 Issue、不应关闭或 `none` 只能得到明确的
`issue_closure_not_applicable`，不能跳过该判断。

两条 delivery route 都只在 `delivery_terminal` current 后进入 `finish_current`。Finish blocked 只重入
Finish，Cleanup blocked 只重入 `owned_resource_cleanup`；两者都先 live reread exact task/history/
resource/ref facts，只补未完成动作，不重放 Delivery、archive、已 current Finish 或已完成删除。

`distribution_action_selected` 是 `distribution/release` 顶层 entry 的二级 exactly-one 产品分流。
Release terminal intent 优先拥有其 pre-publish 内嵌 projection/install/update gate；纯 candidate
surface 验证进入 standalone projection。需要安装、更新、升级、preset reapply 或 workflow switch
  时，先投影 `EVO-REQ-010` 定义的 `distribution_state_preclassification`：active
  `.trellis/workflow.md` 缺失且无任何可归属 official Trellis/Guru managed installation state 才能是
  `clean_target`；`existing_migration_target` 承接 Guru current、可唯一归属的 official Trellis
  installation footprint 或 partial/legacy Guru state（即使 workflow/Guru projection 缺失），以及
identity/provenance/owner 与当前安全 transition plan 均已唯一收敛的 non-Guru active workflow；
上述 facts 或 plan 未 current 的 non-Guru active workflow 才先标记 `foreign_workflow` 并得到
`distribution_state_blocked`。收敛后只重入 preclassification 并转入 existing migration；任何阶段都
不得被 clean installation 覆盖，也不得要求先 mutation 才取得分类。其它
`distribution_state_blocked` 只进入 clarification/live-repair re-entry。二级 route 未唯一收敛前零
validation/install/publication 副作用，action 内 finding/provider change 只返回 current action owner。

Top-level standalone projection validation 只在 exact candidate 的 capability-loss 与
consistency/installation 两类 gate 都 current 时得到 `projection_current`。
`workflow/task_data/docs_authority` capability loss，或 Skill API/interface/schema/command、
distribution/managed-installed inventory、mode/template hash/sidecar、平台 parity、extension
identity/version binding drift，均由 projection owner 进入 `projection_validation_blocked`；后一类
drift 不得误报为 capability loss。blocked 后只能在修复 exact candidate/surface 后重入 validation。
相同 gate 若内嵌于 clean install、existing migration 或 Release pre-publish，只返回最小 finding 给
当前 caller；caller 保持顶层 ownership 并按自身 route 收敛，不能借子 gate 切换 distribution route。

Clean install 只从 active `.trellis/workflow.md` 缺失且无任何可归属 official Trellis/Guru managed
installation state 的 `clean_target` 开始；可唯一归属的 official Trellis footprint 即使缺少 workflow
或 Guru projection，也必须进入 `existing_migration_target`，不得在 `init -y` skip 写模式下作为 clean
input 保留旧 managed file；
`foreign_workflow` 在 identity/provenance/owner 或安全 transition plan 未 current 时必须先得到
`distribution_state_blocked`，不得借 clean install 覆盖；上述 facts 与 plan 收敛后只重入
preclassification 并转为 `existing_migration_target`。成功只得到
`new_contract_current`，包括内嵌 projection finding 在内的失败只由 install owner 得到
`clean_install_blocked`；它不消费 standalone
`projection_validation_blocked` 或 existing migration 的 `pre_migration_current_preserved`。
Existing migration 的正常完成态只允许 `new_contract_current`；任一 phase finding 都先由 migration
owner 重读 live phase/cutover/current consumer 状态，live cutover 尚未开始时只保留
`pre_migration_current_preserved`，cutover 已开始且无法 forward recover 时才得到
`migration_blocked`；内嵌 projection finding 也遵循该 caller-owned 分类，不产生 standalone
projection terminal。两类 owner 都必须从 blocked/current result 重入其 exact step，不得从失败
状态猜测为成功，也不得形成旧新混合 graph。

任一 Architecture 或 RDT promotion 都只推进其唯一 shared current；多个 contribution 分别独立
review、按 expected current identity 串行 promotion。promotion 后只重算语义依赖受影响的结果，
其中 Architecture promotion 至少重做 fresh Phase 2、Task Commit 与 committed full-diff Branch
Review。

Release 的 pre-publish gate、独立确认、publication 和 post-publish verification 是不可倒置的四个
边界。普通 finding 或内嵌 projection finding 都由 Release owner 得到
`release_pre_publish_blocked`；candidate 修订后必须生成新 identity 并完整重跑 pre-publish，不能
产生 standalone projection terminal。`ready_for_release_confirmation` 是唯一确认等待态；确认本身
不持久化为 workflow authority。确认缺失只在 candidate 与 decision-relevant facts 均 current 时继续
等待；明确拒绝得到零 publication 副作用的 `release_not_published -> workflow_completed`。candidate
identity/content 或 decision-relevant provider/target/gate facts 变化必须使旧等待态与旧确认失效并返回
Release pre-publish owner；candidate 变化生成新 identity 并完整重跑，candidate 未变的 live facts 变化
也须重新读取并重跑全部受影响 gate，不能从 stale wait state 进入 publication。
tag 已创建但 GitHub Release 尚未 current 时是 `release_publication_partial`；无法继续自动恢复时
进入 `release_publication_blocked`，两者都只由同一 immutable identity 的 publication owner 恢复。
只有 tag 与 GitHub Release 均经 live 验证后才是 `release_published`。post-publish 可恢复失败进入
`release_post_publish_blocked` 并只重入 exact verification step；语义 defect 则得到不可冒充 verified
的 `release_published_unverified` terminal block。后续修订先按
`independent_invocation_entry_contract` 完成新 identity/envelope、一次 admission receipt、isolation、
pre-semantic guard 与 top-level route；只有重新分类为 `distribution/release` 才生成 new candidate
并完整重跑 Release，不得复用旧 identity/candidate/receipt 或 reforge 原发布 identity。
任一 publication/post-publish 失败都不返回 pre-publish，也不得删除、移动或重建原发布 identity。

Specialist result 的 caller graph 必须先绑定 `REQ-UC-EVO-037` wording review-only 或
`REQ-UC-EVO-038` qualification profile 与 invocation scope，再消费 typed result；不得
用一个组合状态把 caller re-entry 当成 workflow 已结束。wording review 的 review-only scope 只能
报告当前文字状态：`pass` 与 route-level `specialist_revision_required` 在结果完整报告后都结束当前
standalone review-only invocation，不要求额外“修改或 stop”选择；后续修改意图先按
`independent_invocation_entry_contract` 完成新 identity/envelope、一次 admission receipt、isolation、
pre-semantic guard 与 top-level route，不得静默修改、直接跳入 `new change` 或当作 `pass`；
`blocked` 才进入 route-local blocked/re-entry。只有 change-scoped wording 才允许
`content_changed`，且 active change caller 必须丢弃旧结果并完整重建 scope/rescan。normal-scenario
图中的 `qualification_result_current` 是 top-level specialist entry 的 projection；active caller
内嵌 qualification 时复用同一 result/owner/re-entry 合同，不重新执行 top-level
`entry_route_selected`。qualification 的 `classified`、`scope_confirmation_required`、
`mechanism_revision_required`、`blocked` 分别绑定原 caller、唯一澄清 owner、原机制 owner 和
caller-owned blocked/re-entry；scope clarification 或 mechanism revision 前提失败均投影为
`qualification_blocked`，任何非 `classified` 结果都不得被直接投影为 acceptance、finding、
implementation 或 publication。其它通用只读 semantic review 没有 specialist result graph，必须按
direct answer 的 terminal 与不可用事实诚实边界完成。

必须覆盖以下回程/停止语义：

| 变化/失败 | 最早合法回程或终点 |
| --- | --- |
| 普通解释、事实、状态、信息或通用只读分析/审核请求，不要求 change、`REQ-UC-EVO-037..038` specialist profile、distribution、lifecycle disposition 或 durable-history resolution | 只读答案所需的零项或最小 live facts，得到 `direct_answer_completed -> workflow_completed`；Issue/task/branch/repository/Requirements/Design/代码/Architecture 主题本身不触发 mode selection 或 specialist，不创建 Issue/task/worktree，也不遗漏用户答案。所需 live fact 不可用时明确返回 unavailable/unverified fact 与边界，current 虚假断言为 0 |
| 显式 task-free intent | 进入 `task_free_candidate`，但仍执行 suitability/check/risk review；显式意图不覆盖 blocked/standard 产品边界 |
| task-free 自动适用 | 仅在目标清晰、路径有界、current-checkout-only、可逆、低风险且无需 standard gate 时进入；文件数/路径/Issue 不独立分类 |
| `new change` 但没有文件变更目标 | 不得进入 `change_mode_selected`；按 direct answer、resume/recovery/history、distribution/release、specialist 或 stop 重新分类；若用户明确需要文件变更但目标/范围不清，只产生一次 scope clarification，choice current 前保持零 mode/task/workspace 副作用 |
| task-free 可能适用但证据不足 | 只询问一次 mode choice；同 scope 不重复提问 |
| task-free pre-write/targeted-check finding 可在原边界修订 | task-free owner 修订 -> fresh targeted check/post-write review |
| task-free active-task/location 事实要求恢复 | 返回 exact current task/location owner；不得创建第二份 task 或猜测 checkout |
| task-free 无法安全继续或 check 不收敛 | 停止写入并明确 blocked；报告 actual partial edit、未完成 target 和 unverified boundary |
| task-free scope/risk 实质扩大 | 立即停止剩余 target 写入，形成 `task_free_escalation_pending` 后返回 `standard_request`；标准资源副作用前完成 scope resolution 与 exact plan confirmation，得到 `suspended_work_plan_confirmed`；资源准备后、Planning 前必须得到 `suspended_work_reconciled` 或 `suspended_work_isolated` |
| suspended work 与新 lifecycle 同 scope | 标准资源副作用前确认绑定 source/target/edit owner 的 exact transfer/reuse plan；资源准备后验证 exact edit 只归属一个 Workspace/current owner，得到 `suspended_work_reconciled` 后继续，不重复实现或自动提交源 work |
| suspended work 与新 lifecycle 异 scope | 标准资源副作用前确认 exact isolation plan；资源准备后证明 resource/authority 隔离并保留旧 work 的 discoverable resume route，得到 `suspended_work_isolated` 后继续；无法隔离时 blocked |
| current 精确副作用计划已完整展示，且随后无实质变化；用户回复“确认继续”“可以，继续”或其它清晰语义肯定 | AI 得到 dialogue-local `side_effect_confirmation_current`，只执行刚展示的下一项 exact action；不要求固定 prompt、口令、hash/digest、task/path/branch/SHA、摘要复述或规定句式，不授权任何未展示的后续副作用 |
| exact PR 已创建且 live state 为 READY，current merge 计划已完整展示；用户回复清晰语义肯定 | 进入 expected-head merge action；不得因回复没有包含固定 `合并PR` 而拒绝。merge 计划之外的 archive、cleanup、Release 或其它副作用不被授权 |
| 计划尚未完整展示，或回复包含疑问、限制、条件、修改、部分选择或歧义 | 保持 `side_effect_confirmation_pending`/`side_effect_plan_revision_required` 且副作用为 0；AI 先消费最新意图、补全或修订并重新展示 current 计划，不解析关键词猜测确认 |
| 用户明确拒绝刚展示的 exact action | 保持副作用为 0，进入该 action owner 已声明的 refusal/stop/re-entry；不得把拒绝转换为肯定、复用到另一 action，或绕过 route-local disposition choice |
| displayed plan 的 target/scope/副作用/authority/permission/candidate/HEAD/decision-relevant facts 实质变化 | 进入 `side_effect_plan_stale`，旧确认不可消费；live reread 后由 exact action owner 重建并重新展示计划，再等待新的语义确认 |
| 任一 script/validator/recorder/schema/DTO/checkpoint/gate/history 尝试解析、匹配、验证或持久化用户确认 | Requirements finding；保持副作用为 0，删除该 confirmation authority 机制并回到 AI-owned dialogue-local confirmation。plan/live-fact freshness 可继续确定性验证，但不得把 digest 变成用户 challenge |
| active duplicate | 得到 `active_duplicate_current`，停止创建新 change/resource 并返回 exact unfinished lifecycle owner；不得重复 authoring 或重新顶层分流 |
| completed duplicate | 得到 `completed_duplicate_current`，返回 current terminal/history result 后 `workflow_completed`；不得重新激活已完成 task，material 新 delta 不得伪装为 duplicate |
| change-request scope clarification | 得到 `change_request_scope_clarification_required`；唯一 choice current 后重建完整 readiness candidate 并 fresh 重入，material requirement intent change 先返回 requirement owner |
| linked prerequisite 未满足/不可独立交付 | 得到 `change_request_prerequisite_blocked`；prerequisite current 后只重入 change-request readiness |
| change-request not-found/multiple/unresolved stale/material mismatch | 得到 `change_request_resolution_blocked`，绑定候选、最后确认 facts 与所需唯一输入；输入/live repair current 后只重入 readiness |
| selected base behind | 只刷新 exact authority checkout；成功后进入 `base_current` |
| base refresh unsafe/ambiguous | pre-task blocked；不得修改 invocation checkout 或回退低优先级 base |
| repository SSOT 缺失/不完整/stale/conflicting | bootstrap/repair；current authority 成立后重入 `repository_authority_current` |
| parent repository 存在无关 submodule | 默认排除其 authority/content/status/validation；零 submodule action，parent route 继续 |
| 用户显式要求修改 submodule repository | 停止把它作为 parent 内部目录处理；为该 repository 建立独立 mode/authority/workflow 与精确副作用边界 |
| requirement 信息不足/冲突 | requirement clarification；等待一个真实问题 |
| RDT 真实 no-impact/aligned | 绑定 current RDT 与适用片段；不创建 contribution，进入 Architecture alignment/task projection |
| RDT 需要新增/修订 | 形成并审查 task-local RDT contribution；未收敛前不得 `plan_ready` |
| RDT false-no-impact、自报 boolean 或 task planning 冒充 RDT | planning finding；返回 RDT impact/contribution owner，不得结构 PASS 后继续 |
| current Architecture 缺失/不完整 | Architecture bootstrap/repair；修复后重入 pre-design consumption |
| requirement 与 Architecture 冲突 | 保留 requirement，进入显式 Architecture/product choice；未决前 stop |
| planning finding | 对应 planning author 修订 -> 一次 fresh approval |
| implementation/Phase 2 finding | implementation owner 修订 -> affected validation/check |
| committed full-diff finding | implementation/design owner 修订 -> fresh check/commit/full-diff review |
| semantically equivalent identity change | 刷新 identity/freshness -> 原结果继续 current |
| material scope/authority change | 最早受影响 owner -> 全部受影响下游重算 |
| Implementation/Check 发现新的 RDT 事实 | 回写 task-local contribution -> 受影响 planning/check/review 重算；不得留到 Finish 后补写 |
| base movement | impact no-op 或受影响 owner；不重建 task |
| Architecture/RDT contribution no-impact | 不创建 contribution/ADR，不进入 shared-current promotion |
| Architecture/RDT contribution review finding | contribution owner 修订 -> fresh independent review |
| Architecture/RDT contribution 经 review 不进入 shared current | 按 review 结论保留为 task-local deferred proposal、修订或删除；返回最早受影响 task owner，不改变 shared current |
| expected current identity 冲突/其它 task 已 promotion | 重新读取 shared current并判断 no-impact/revision；不得覆盖新 current |
| Architecture/RDT promotion 成功 | 刷新 shared-current identity，重算受影响 evidence；Architecture 至少重做 fresh Phase 2/commit/full-diff review |
| resume/recovery 恰好解析到一个 current work，或 stale identity 经 live facts 证明 semantically equivalent 且唯一 | 刷新 identity/freshness 并得到 `current_work_recovered`，恢复 current phase/副作用/finding 后直接返回 earliest current owner；不重建 task 或重跑无关 Intake |
| resume/recovery not-found、multiple、unresolved stale 或 material mismatch | 得到 `current_work_recovery_blocked`；报告候选 identity、最后确认 facts 与所需唯一输入，不猜测 checkout 或复用未刷新 locator；输入/live repair 使解析唯一后重入 `current_work_resolution`。用户明确启动独立新请求时，才按 `independent_invocation_entry_contract` 建立新 identity/envelope、生成一次 admission receipt、通过 isolation 与 pre-semantic guard 后重新选择 `entry_route_selected`；不得把 recovery blocked 直接当作 route selection |
| archive/finish/disposition durable history query 恰好解析到一个 current result | 得到 `durable_history_result_current`，返回查询结果后 `history_query_completed -> workflow_completed`；abandonment cleanup 后仍可发现，不得重入、恢复或激活被查询 lifecycle |
| archive/finish/disposition durable history query not-found、multiple、unresolved stale 或 material mismatch | 得到 `history_query_blocked`；报告候选、最后确认 facts 与所需唯一输入，输入/live repair 使结果唯一后重入 `durable_history_resolution`；不得创建新 task、转成 active-work recovery，或把 retained/suspended 的 resume 意图当成只读查询 |
| active lifecycle 无不可逆远端副作用，用户要求 retain/suspend | 停止新增写入，形成 `active_lifecycle_retained` 或 `active_lifecycle_suspended`；保持 exact work 可发现、可恢复且只有一个 resume owner，记录最小 disposition/history 后 `active_lifecycle_disposition_completed -> workflow_completed`，cleanup 为 0 |
| active lifecycle 无不可逆远端副作用，但“取消”意图不能唯一判定 retain/suspend 或 abandon/cleanup | 得到 `active_lifecycle_disposition_choice_required`，只询问一个最高价值问题；choice current 前 cleanup 为 0，随后只重入 `active_lifecycle_disposition`，不得猜测 terminal 或重新顶层分流 |
| active lifecycle 无不可逆远端副作用，用户要求 abandon/cleanup，且 deletable owned resource 为 0 | exact plan 证明 unrelated/retained resource 与 durable history/ref 可达后，无需 cleanup 确认，直接得到 no-op `active_lifecycle_abandoned`；最小 disposition/history 必须在 cleanup-equivalent terminal 后可查询，不得把未完成 work 冒充普通 `finished` |
| active lifecycle 无不可逆远端副作用，用户要求 abandon/cleanup，且存在 deletable owned resource | 展示 exact owned-resource 删除计划、unrelated/retained 资源与 durable history/ref 保留项；只在 current 对话确认后进入 `active_lifecycle_owned_cleanup`，成功得到 `active_lifecycle_abandoned`，记录 cleanup 后仍可查询的最小 disposition/history 后完成；不得把未完成 work 冒充普通 `finished` |
| active lifecycle cleanup 确认缺失、明确拒绝或 plan facts 变化 | 缺失时保持 `active_lifecycle_cleanup_confirmation_pending` 且 cleanup 为 0；明确拒绝若已包含唯一 retain/suspend choice 则消费该 choice，否则得到 `active_lifecycle_disposition_choice_required` 并只询问一次，choice 前 cleanup 为 0，不得直接产生双 terminal；resource/owner/history facts 变化使旧确认失效，live reread 后重建 exact plan，不得持久化或复用授权状态 |
| active lifecycle disposition/cleanup facts 无法唯一或 cleanup 部分失败 | 得到 `active_lifecycle_disposition_blocked`，绑定最后确认 facts、已完成/待执行动作及仍存在/已删除/必须保留资源；恢复后只重入 exact disposition 或 owned cleanup step，不扩大 owner、重放删除或隐藏 durable history |
| active lifecycle 已有不可逆远端副作用 | 原远端 owner 保持 candidate/identity 不变，先收敛既定正常 current terminal、forward-recovered current terminal 或 terminal block；不得删除/回滚/移动/重建远端结果或冒充 cancelled。结果 current 后只对 current plan/确认覆盖的 eligible local owned resources cleanup，保留远端结果与最小 disposition/history，再得到 `active_lifecycle_remote_outcome_current -> active_lifecycle_disposition_completed -> workflow_completed` |
| delivery route 未明确 | 在 route-specific readiness 前等待一次真实 choice；未明确时不得调用 GitHub或把 `none` 当默认 fallback |
| delivery route authority material change 且无不可逆副作用 | 失效旧 route readiness，重新选择并重算受影响下游 |
| `github_pr` provider/remote failure | 原 delivery owner forward recovery 或 blocked；不得切换 `none`、重复不可逆动作或返回早期 phase |
| `none` route | GitHub I/O 为 0；完成 local acceptance、closure-not-applicable 与 local terminal 后进入 Finish |
| Issue closure mismatch | 保留 merge/delivery current 事实，返回 closure owner recovery/blocked；不得进入 Finish |
| irreversible remote side effect 后失败 | 只允许 forward recovery/terminal block |
| Archive/Finish 任一步骤失败或部分 current | 得到 `finish_blocked`，绑定 exact task、已完成/待执行 transition、history/ref facts 与唯一恢复输入；live reread 后只重入 `finish_current`，不得重放 Delivery/archive 或把 partial Finish 冒充成功 |
| Cleanup 部分完成或失败 | 得到 `cleanup_blocked`，绑定仍存在、已删除和必须保留的 exact resource/ref/history；live reread 后只重入 `owned_resource_cleanup`，不得重复删除、扩大 owner、重放 Delivery/Finish 或隐藏 durable history |
| active `.trellis/workflow.md` 为 non-Guru，或 identity/provenance/owner/transition plan 未 current 的 `foreign_workflow` | 由 `EVO-REQ-010` 的 `distribution_state_preclassification` 保留该独立标签并得到 route-local `distribution_state_blocked`；在 identity/provenance/owner 与安全 transition plan 经一次 clarification/live repair 唯一确认前，保留 foreign workflow、不得执行 init/workflow-switch/preset-reapply/migration route 副作用。确认后只重入 preclassification：已识别 non-Guru workflow 恰好转为 `existing_migration_target` 并由 migration owner 保留至唯一 cutover；其余未知/多重状态继续 blocked。不得要求先 mutation 才能取得 migration 分类，也不得把 foreign workflow 默认解释为 clean target |
| distribution target state 为 official/partial/legacy、mixed、unknown、unowned 或 multiple identity（不含已单列的 `foreign_workflow`） | 由 `EVO-REQ-010` 的 `distribution_state_preclassification` 唯一分类：可唯一归属的 official Trellis installation footprint 或 partial/legacy Guru managed surface、sidecar、lifecycle、history/ref，即使 active workflow/Guru projection 缺失，也得到 `existing_migration_target`；active workflow 缺失且无任何可归属 official Trellis/Guru managed installation state 才能得到 `clean_target`；无法唯一分类得到 route-local `distribution_state_blocked`，只允许一次 clarification/live repair 后重入，期间零 route 副作用 |
| distribution/release 二级 action 未唯一 | 按 terminal intent、candidate 与 target live current state 只询问一个最高价值问题；`distribution_action_selected` 前零 validation/install/migration/publication 副作用。Release 内嵌 gate 不取得 child top-level ownership，clean/existing state 与 standalone validation 不混用 |
| distribution/clean-install/migration/Release 外部 provider timeout、认证/配额、unknown outcome 或部分成功 | 按 `EVO-REQ-039` 返回 exact projection/install/migration/publication owner，先重读 live state 再分类安全重试、forward recovery 或 blocked；不得切换 route、重复不可逆动作或以其它 distribution terminal 掩盖失败 |
| distribution/projection/clean-install/migration 验证完成但不发布 | `distribution_validation_completed -> workflow_completed`；不得借验证结果执行 tag/Release |
| standalone projection 中出现 `workflow/task_data/docs_authority` capability loss，或 Skill API/interface/schema/command、distribution/managed-installed inventory、mode/template hash/sidecar、平台 parity、extension identity/version binding drift | projection owner 得到 `projection_validation_blocked`，绑定 exact candidate/surface/gate/mismatch；consistency/installation drift 仍阻断但不计为 capability loss。修复后只重入 `projection_validation`，不得切换 install/migration/Release 或声明局部 current |
| clean install application/validation finding，包括内嵌 projection gate finding | 内嵌 validator 只返回最小 finding；clean-install owner 绑定 exact step、created resources 与 unverified boundary，只允许重入 exact clean-install step 或得到 `clean_install_blocked`，不得产生 `projection_validation_blocked`、使用 migration terminal 或把 partial install 冒充 target current |
| migration preflight 无法承接 active/resumable work、archive/finish/history result 或 retained ref | 保持 `pre_migration_current_preserved` 并停止在 cutover 前；报告不可承接项与所需修复，修复后只重入 migration preflight，不得删除 durable result、激活 target 或依赖 legacy runtime consumer 完成迁移 |
| migration preflight/application finding，包括内嵌 projection gate finding，且 live cutover 尚未开始 | 内嵌 validator 只返回最小 finding；migration owner live reread，只允许 `pre_migration_current_preserved` 后 exact retry/re-entry，不得产生 `projection_validation_blocked` 或激活 target |
| migration cutover、PRESET-REAPPLY 或 final-validation finding，包括内嵌 projection gate finding，且 live cutover 已开始 | migration owner 绑定 current phase/cutover state forward recover，并只重入对应的 `migration_cutover_current`、`migration_preset_reapply_current` 或 `migration_final_validation_current`；只允许收敛为 `new_contract_current` 或 `migration_blocked`，不得产生 `projection_validation_blocked`、回退 legacy、跳过 mandatory PRESET-REAPPLY 或留下 mixed graph |
| A=`github_pr`、B=`none` 并行 task 的 provider/archive/Finish/cleanup failure | 只返回 exact failed task 的 route/current owner；另一 task 保持可继续且 B 的 GitHub I/O 为 0。恢复后分别验证 current history/result 与 cleanup 前后 retained-ref reachability，不得交叉写入、重放或传播失败 |
| Release pre-publish gate finding，包括内嵌 projection gate finding | 内嵌 validator 只返回最小 finding，Release owner 得到 `release_pre_publish_blocked`；修订 exact candidate 后生成新 identity 并完整重跑 pre-publish，旧 candidate evidence 不复用，不产生 `projection_validation_blocked` |
| Release confirmation 缺失，且 exact candidate/pre-publish/decision-relevant facts 均 current | 保持 `ready_for_release_confirmation`；不得发布、超时推断或持久化授权状态 |
| Release confirmation 明确拒绝 | 得到 `release_not_published -> workflow_completed`；tag/Release/publication 副作用为 0，candidate 与已完成证明保持真实可查询；后续发布请求按 `independent_invocation_entry_contract` 建立新 identity/envelope、生成一次 admission receipt、通过 isolation 与 pre-semantic guard 后重新执行 top-level/action selection 与 live reread |
| Release 等待期间 candidate identity/content 或 decision-relevant provider/target/gate facts 变化 | 旧 `ready_for_release_confirmation` 与旧确认立即失效；返回 `release_pre_publish_validation_current`，candidate 变化生成新 identity 并完整重跑，live facts 变化重读并重跑全部受影响 gate；不得从 stale wait state 发布 |
| tag 已创建但 GitHub Release 未 current | 得到 `release_publication_partial`，由原 publication owner 绑定 tag/live facts/已完成与待执行副作用；同一 identity 的恢复前提 current 后重入 publication，无法自动恢复时得到 `release_publication_blocked`；不得删除、移动或重建 tag |
| publication 在同一 immutable identity 上 blocked | 得到 `release_publication_blocked`；恢复前提 current 后只重入同一 publication owner，不得返回 pre-publish、换 candidate 或 reforge tag |
| `release_published` 后可恢复的 provider/verification prerequisite failure | 得到 `release_post_publish_blocked`；绑定已发布 identity、exact verification step 与唯一恢复输入，前提 current 后只重入 post-publish verification，不重新 publication |
| post-publish 证明已发布 candidate 存在语义 defect | 得到 `release_published_unverified` terminal block；原 tag/Release 保持不可变且不得称 verified，修订按 `independent_invocation_entry_contract` 建立新 identity/envelope、生成一次 admission receipt、通过 isolation 与 pre-semantic guard 后重新分类；只有 `distribution/release` 分类才建立 new candidate 并完整重跑 Release，不得复用旧 receipt/candidate 或 reforge 原 identity |
| wording review `pass` 由 active workflow caller 调用 | `returned_to_unique_caller -> caller_current_route_reentered`；不得结束 caller workflow |
| wording review `pass` 为 top-level standalone review-only 请求 | 完整报告结果后 `returned_to_unique_caller -> standalone_specialist_completed -> workflow_completed`；不得修改被审对象 |
| wording review 发现 `specialist_revision_required` 且为 standalone review-only | 完整报告 findings 后 `standalone_specialist_completed -> workflow_completed`；不得要求额外“修改或 stop”选择。后续修改按 `independent_invocation_entry_contract` 建立新 identity/envelope、生成一次 admission receipt、通过 isolation 与 pre-semantic guard 后完整执行顶层分类，不得静默修改、直接跳入 `new change` 或当作 `pass` |
| wording review `content_changed` 且属于 active change-scoped caller | 丢弃旧 review result，完整重建 fixed scope/rescan 后重入 `wording_review_result_current`；不得复用旧 digest、提前消费或结束 caller workflow |
| wording review `blocked` | 得到 `wording_review_blocked`；active caller 或 standalone caller 只在其 owner 修复 scope/authority/semantic precondition 后 fresh 重入 exact `wording_review_result_current`，否则只报告 blocked；不得进入 top-level entry selection 或产生新副作用 |
| qualification `classified` 由 active workflow caller 调用 | `returned_to_unique_caller -> caller_current_route_reentered`；不得结束 caller workflow |
| qualification `classified` 为 top-level standalone 请求 | `returned_to_unique_caller -> standalone_specialist_completed -> workflow_completed` |
| qualification `scope_confirmation_required` | 只交给唯一澄清 owner 取得一次真实 scope choice；choice current 后由原 caller 重建完整 candidate set 并 fresh 重入 qualification，不得把未决 scope 当作 qualified |
| qualification scope clarification blocked | 澄清 profile 无法安全取得或确认 scope choice 时投影为 route-local `qualification_blocked`；原 caller 在 authority/choice 前提恢复后重入 qualification，不得进入 top-level stop、`classified` 或 acceptance |
| qualification `mechanism_revision_required` | 只交给原机制 owner 删除/替换 task-introduced mechanism；修订后 fresh 重入 qualification，不得先进入 acceptance、finding 或 implementation |
| qualification mechanism revision precondition blocked | 原机制 owner 无法安全删除/替换时保持 `qualification_blocked`；前提恢复后 fresh 重入，不得把未修订 mechanism 当作 qualified 或进入 implementation |
| qualification `blocked` | 得到 route-local `qualification_blocked`；caller 修复 authority/candidate/consumer freshness 后重入 qualification，不能投影为 `classified` 或完成当前 caller |
| 尚未绑定需处置 active lifecycle 且本 invocation 尚无新副作用时显式 stop | `request_stopped -> workflow_completed`；零新增/修改/cleanup 副作用，既有 work 不变；后续新意图按 `independent_invocation_entry_contract` 建立新 identity/envelope、生成一次 admission receipt、通过 isolation 与 pre-semantic guard 后重新选择 `entry_route_selected` |
| 请求保留、暂停、取消、放弃或清理既有 active lifecycle | 不适用 top-level stop；先进入 resume/recovery 解析 exact current work，再按 `EVO-REQ-067` 进入唯一 disposition owner，并只得到 retain/suspend、零 deletable resource 的 no-op abandonment、有 deletable resource 且 current 确认后的 abandonment、cleanup 拒绝回复中的唯一 retain/suspend choice 或一次 disposition choice、remote-outcome current、disposition blocked/re-entry 或 disposition completion |
| `active_user_intent` 通过 lifecycle preclassification 且判定为 `owner_local_additive` | 由 current/最早受影响 owner 按到达序列消费；只重算实际受影响判断，复用仍 current 的 `context_envelope`，不得生成新 `request_received` 或触发 stock matcher |
| `active_user_intent` 通过 lifecycle preclassification 且判定为 `material_additive` | remote boundary 前回最早受影响 owner 并按 freshness 重算；remote boundary 后形成唯一 consumer 的 `additive_change_pending`，旧 route current/forward-recovered current/terminal block 后，唯一 consumer 先为 pending intent 分配新的 invocation identity/`context_envelope`，再恰好生成一次新的 `request_received`，随后按 `independent_request_isolation_gate -> pre_semantic_dispatch_guard -> entry_route_selected` 顺序继续；不复用旧 identity/envelope/candidate/receipt、不修改旧 candidate |
| `active_user_intent` 通过 lifecycle preclassification 且判定为 `override` | 无副作用停止旧 route；可逆本地副作用保留 `suspended_current_work`；不可逆远端副作用先由原 owner 收敛 current/forward-recovered current/terminal block；之后唯一 request-entry consumer 先分配新的 invocation identity/`context_envelope`，再恰好生成一次新的 `request_received`，随后按 `independent_request_isolation_gate -> pre_semantic_dispatch_guard -> entry_route_selected` 顺序继续；不得复用旧 identity/envelope/candidate/receipt |
| active lifecycle 存在但 `active_user_intent` 缺少唯一 identity/因果 predicate，且不能证明独立请求 | 得到 `lifecycle_intent_binding_blocked`，只由 preclassification 的唯一澄清/恢复 owner 重入；不得降级为 `ordinary_natural_language`、吞入 active owner 或进入 stock policy |
| 无 active lifecycle，或已证明为独立 invocation 的 `independent_user_request` | 唯一 request-entry consumer 先建立全新的 invocation identity/`context_envelope`，再生成恰好一个只表示 admission receipt 的 `request_received`；不得复用旧 lifecycle 的 envelope/candidate/owner，也不得把 receipt 当作 route 已选择。随后先过 isolation safety gate：旧 lifecycle 处于非变更等待/确认或 scope 已安全隔离时立即进入 `pre_semantic_dispatch_guard`；共享可变 scope/不可逆动作尚未安全隔离时，在 route selection 前进入 `independent_request_isolation_pending`；scope/owner 或安全隔离边界无法唯一解析时进入 `independent_request_isolation_blocked` |
| `independent_request_isolation_pending` | 只保留新 invocation、scope、旧 owner、不可逆边界与唯一 re-entry；旧 owner 不得消费/改写新请求。pending 只有在旧 owner/handle 正在执行可观察的安全相关 transition 且存在下一进展事件或状态变化时合法；每次 re-evaluation 必须恰好观察到进展并刷新 pending、达到安全隔离边界并重入 `pre_semantic_dispatch_guard`，或转为 `independent_request_isolation_blocked`。非变更等待/确认、无进展、handle 失效或 owner 不再可消费不得继续 pending，且不得用相对耗时/轮次阈值替代该判断；安全边界或旧 owner current/forward-recovered current/terminal block 后复用既有 envelope/receipt，不重新生成 `request_received` |
| `independent_request_isolation_blocked` | 绑定无法唯一解析的 scope/owner/隔离边界、最后确认 facts 与唯一 repair input；修复后只重入 `independent_request_isolation_gate` 重新判定，不直接假设 pending/clear，不重新生成 `request_received`，不得无限等待或静默丢弃 |
| user override 且旧 route 尚无副作用 | bound 事件只由旧 owner 消费并停止旧 route；随后唯一 request-entry consumer 分配全新 invocation identity/`context_envelope`，恰好生成一次 `request_received`，再按 `independent_request_isolation_gate -> pre_semantic_dispatch_guard -> entry_route_selected` 顺序继续；不得复用旧 identity/envelope/candidate/receipt 或再次 preclassify bound 事件 |
| user override 且已有可逆本地副作用 | 停止新增写入，形成具有唯一 resume owner 的 `suspended_current_work`；随后唯一 request-entry consumer 以全新 invocation identity/`context_envelope` 恰好生成一次 `request_received`，再按 `independent_request_isolation_gate -> pre_semantic_dispatch_guard -> entry_route_selected` 顺序继续；不得复用旧 identity/envelope/candidate/receipt 或再次 preclassify bound 事件，同 scope 必须 reconciliation、异 scope 必须 isolation，不自动提交、丢弃、归档或清理 |
| user override 且已有不可逆远端副作用 | 原 owner 保持旧 candidate 不变并先收敛为既定正常 current terminal、失败后 forward-recovered terminal 或 terminal block；结果 current 后，唯一 request-entry consumer 先为 latest override 分配新的 invocation identity/`context_envelope`，再恰好生成一次新的 `request_received`，随后按 `independent_request_isolation_gate -> pre_semantic_dispatch_guard -> entry_route_selected` 顺序继续；不得复用旧 identity/envelope/candidate/receipt；只有分类为 new change 才进入二级 mode selection，不得默认 new change |
| owner-local additive 不改变 accepted scope/exact candidate/delivery route/terminal acceptance，或只补充 current forward-recovery 所需输入 | 按到达顺序由 current/最早受影响 owner 消费；只重算该 owner 实际受影响的判断，不创建新 lifecycle 或 `additive_change_pending` |
| material additive 在不可逆远端副作用开始前到达 | 返回最早受影响 owner，按 freshness 失效并重算受影响 candidate/route/acceptance 与下游；不得保留 stale result 或跳过 gate |
| material additive 在不可逆远端副作用开始后到达 | 原远端 owner 创建可发现且有唯一 consumer 的 `additive_change_pending`，保持 in-flight/published candidate 不变，并收敛为既定正常 current terminal、失败后 forward-recovered terminal 或 terminal block；任一结果 current 后，唯一 consumer 先分配新的 invocation identity/`context_envelope`，再恰好生成一次新的 `request_received`，随后按 `independent_request_isolation_gate -> pre_semantic_dispatch_guard` 顺序重新执行六类 exactly-one `entry_route_selected`，不得复用旧 identity/envelope/candidate/receipt；只有分类为 new change 才进入二级 mode selection 与独立 change lifecycle，其他分类由对应顶层 route 的唯一 owner 消费；不得默认 new change、提前消费、丢失、重排或写入旧 candidate |
| mandatory capability/route 缺失或 ambiguous | fail closed；不得猜测下一步 |
| stock policy 首次全 pending、部分完成或结果 `unknown` | 仅在已选 route/caller 的 stock action 中评估：首次所有 action 为 `pending` 且无 `completed/unknown` 时先得到 `stock_policy_action_required`；有 completed+pending 时得到 `stock_policy_action_partial`；任一未知/不一致时得到 `stock_policy_action_unknown`，优先级为 `unknown > partial > action_required`。三者均绑定 exact role/target/action、caller/profile、已完成/待执行动作、独立 `file_state`/`context_state`/`sidecar_state`、不可逆边界与唯一 owner，均不是成功/终端；经必要确认或确定性 action 后复用同一 `context_envelope` 中仍 current 的 policy/authority projection，仅在 identity/state/decision-relevant facts 变化、过期或未知时定向 fresh reread，再从 `stock_policy_action_reentry` 重入；standalone policy/projection 只能得到 `stock_policy_current`、对应 role-local blocked 或 `retained_context_blocked`，嵌入 clean-install/migration/Release 则只把最小 finding 投影给 caller。pre-entry guard 不执行 action 或 mutation；不得猜测成功、重放已完成/不可逆 action 或重新进入 `entry_route_selected` |
| `active_user_intent` / lifecycle-bound user message | 先执行 `lifecycle_intent_preclassification`，其结果必须恰好是 `lifecycle_bound_user_intent`、`independent_user_request` 或 `lifecycle_intent_binding_blocked`。bound 结果要求 exact lifecycle/invocation identity、唯一 owner/phase、scope/candidate/remote-boundary、host event identity、到达序列和因果 wait/response facts，并只能由 current/最早 owner 唯一分类为 owner-local additive、material additive 或 override，前三类只回 exact owner/最早 owner；independent request 先建立新 identity/envelope、恰好生成一次 admission receipt，再经 isolation safety gate 后进入 source/route selection；shared-scope pending 与 isolation blocked 均复用既有 receipt。predicate 不完整时 `lifecycle_intent_binding_blocked`，不得降级 ordinary 或进入 stock policy |
| ordinary natural language、exact command/Skill selection、upstream CLI、Guru-bound provider/worker、worker return/context | 仅对已通过 lifecycle preclassification 的独立请求按 `EVO-REQ-076` 固定 rank 识别：return/context > caller-bound provider/worker > upstream CLI > exact command > exact Skill selection > ordinary natural language；句中提及 stock 名称但无 exact binding 走 ordinary natural language，internal return/context 不重新分流，同一 canonical identity 才折叠 command/selection，unknown/multiple source class fail closed；suppressed 命中先由 pre-entry guard redirect 或 fail closed，不执行精确移除/delete、quarantine 或 patch；这些 mutation 只能由已选且绑定的 maintenance/provider action 承接。provider/worker 缺 binding 得到 `provider_boundary_blocked`，明确只读 provider 经 `explicit_provider_result_current` 回 direct-answer owner |
| 无 stock surface 的 direct answer、非 stock stop/history/specialist | 只经过 `pre_semantic_dispatch_guard` 的最小 source/matcher 读取，跳过完整 `stock_policy_evaluation`，直接进入唯一 Guru route；不得因 inventory 存在而扫描全部 provenance/file/sidecar 或产生 stock policy state |
| 官方 `trellis update --dry-run` 输出包含 `MIGRATION REQUIRED` | 只执行 `trellis update --migrate --skip-all`，验证 `--skip-all` 保留 user modification；复用仍 current 的 update policy context，仅在 `.new`/backup/sidecar 或 decision-relevant observed state 变化、过期或未知时定向 reread；不得用非 migration 命令或 `--force` 代替 |
| 官方 `trellis update --dry-run` 输出不包含 `MIGRATION REQUIRED` | 只执行 `trellis update --skip-all`，验证 `--skip-all` 保留 user modification；复用仍 current 的 update policy context，仅在 `.new`/backup/sidecar 或 decision-relevant observed state 变化、过期或未知时定向 reread；两分支均属于 upstream provider facts，不产生 Guru CLI intent |
| Codex hooks 配置为 enabled、disabled 或无配置 | 三种输入分别验证 emission、context injection 与 suppression/redirect；无 hook 或 `not-emitted` 不能单独证明 suppression，缺失第一项 semantic 行为前的隔离证据时保持 role-local blocked |
| retained nonsemantic host context 的 preserve/reconcile action 无法安全完成 | 得到 `retained_context_blocked`，绑定 host/projection cell、context action、最后确认 state 与唯一 host/policy repair input；不取得 semantic ownership、不改写已选 Guru route，修复后只重入 exact retained action |
| stock asset role、successor/provider caller、direct consumer、supported projection cell 或受支持 mutation/interception owner 缺失/重复/未知 | admission 阶段对 `suppressed_semantic_route` 得到 `upstream_suppression_blocked`；对 `provider_only`、`explicit_only` 或 `controlled_worker_provider` 得到 `provider_boundary_blocked`；retained host context 得到 `retained_context_blocked`。两类（及 retained）结果都绑定 asset、source/version/path、source/policy/mutation owner、最后确认 facts、影响的 Guru successor 与唯一修复输入；修复后只重入对应 admission/policy owner。pre-entry 结果不得执行 mutation 或进入 `entry_route_selected`；已选 route 内的 action failure 只回当前 caller，不重新顶层分流 |
| stock provider/worker 被 Guru caller 调用但 caller、scope、source identity 或直接 consumer 不唯一 | 得到 `provider_boundary_blocked`，保持调用前状态；caller binding/facts current 后只重入原 provider boundary，不创建第二 semantic owner、question、gate 或副作用 |
| standalone exact explicit-only 请求只读取 session history 或生成 bug diagnosis/follow-up recommendation | 由 stock-policy owner 绑定 exact `trellis-session-insight` 或 `trellis-break-loop`、scope/source/read-only action 后得到 `explicit_provider_result_current`，交给 direct-answer owner；结果（包括 unavailable/unverified 边界）消费后得到 `direct_answer_completed -> workflow_completed`，不得创建 task/worktree、进入 mode、执行 follow-up 写入或把 provider 当 semantic owner |
| direct-answer owner 调用 caller-bound channel transport 或 research/check observation | 只得到 `provider_result_current -> returned_to_unique_caller`，由同一 direct-answer owner 完成答案；不得投影为 `explicit_provider_result_current`，implementation execution 不适用此行，binding/profile/consumer 不完整时得到 `provider_boundary_blocked` |
| exact explicit asset selection 同时要求 spec/Issue/文档/代码写入，或请求已属于 active caller | 在 raw explicit invocation 前，顶层无 active lifecycle 时重新分类为 `new change`；已有 active caller 时直接回该 caller 的 current route。raw explicit action 与 standalone provider terminal 均不得产生；binding/target/consumer 不完整时得到 `provider_boundary_blocked`，不得改写 RDT/Architecture/product/route authority |
| stock policy 在 fresh install/migration/update/upgrade/workflow switch/reapply 后完整且无未处理 user modification/sidecar | 得到 `stock_policy_current`，继续唯一 Guru entry；provider/explicit/worker 结果仍只能返回其 caller，不改变 top-level route |

## 7. `EVO-001..007` 已确认目标

### `EVO-001` 需求与既有设计被准确理解

- GitHub Issue 可以同时承载需求、约束和已经审阅的设计。
- Phase 0 无损形成 requirement authority 和 reviewed-design commitments，并读取 parent repository
  current RDT；task planning 只能引用、修订和完善该 authority，不能成为平行或替代 SSOT。
- 信息充分时零提问；信息不充分时，每轮只询问一个最高价值问题。
- `prd.md` 始终忠实表达产品意图，不能为了适应 current Architecture 而静默修改需求。

### `EVO-002` Architecture Baseline 成为设计与演进过程的一部分

- 第一次实质编写 `design.md` 前读取 current Architecture Baseline、设计宪法和 change contract。
- `design.md` 是 Architecture alignment 的主要载体，三份 planning 文档不重复 baseline 正文。
- 正常承接、真实冲突、authority 不完整、新增决策和既有决策修订都有明确结果。
- Planning 只形成 task-local proposal/contribution/ADR candidate；shared current 仍经独立
  review、serialized promotion、fresh Phase 2、Task Commit 和 full-diff Branch Review。

### `EVO-003` 从流程 artifact 驱动进化为 current authority 驱动

- shared Architecture、Requirements、Design、Test 和 Docs SSOT 是持久 authority；task
  planning 只提供该 task 对 current authority 的引用、delta/contribution 与执行映射，Git/GitHub/
  Trellis live facts 提供任务 current state。
- 不依赖 Issue Scope Ledger、跨阶段 aggregate、共享 handoff、历史 checkpoint 或重复摘要。
- scope/authority 变化按语义依赖失效并返回最早受影响 owner。
- parent repository task 默认排除 Git submodule；submodule 内容、状态和失败不参与 parent RDT、
  code、validation 或 readiness，显式 submodule change 使用独立 repository workflow。

### `EVO-004` 每项语义判断只有一个 owner

- 从 Intake 到 Cleanup 的每项 semantic responsibility 唯一；AI 判断与确定性执行分层。
- 不存在双 writer、wrapper owner、重复 reviewer 或 consumer 读取 producer-private result。

### `EVO-005` 正常工作流显著更短、更快、更安静

- 只保留有直接 consumer 且无法重建的最小信息，阶段后卸载 private evidence。
- 普通 non-file-changing 请求与未绑定 lifecycle 的通用只读 review 只读取回答所需的最小事实并
  直接完成，不进入 change mode、资源准备或未支持 specialist profile；live facts 不可用时透明返回
  unavailable/unverified，不虚报 current。
- 没有真实选择时不提问，不向用户展示内部 artifact 搬运。
- 正常路径尽最大可能减少重复 semantic work、中间交接、上下文堆积、全文重读、不必要脚本和
  重复验证；是否满足由 action/consumer 与 correctness trace 证明，不以相对性能比例作为发布门槛。

### `EVO-006` 从请求进入到资源清理形成完整闭环

- normal、revision、refresh、recovery、blocked、no-Issue、`github_pr` 和 `none` 路径都有唯一
  回程或终点，不依赖 Agent 猜测。
- change readiness、standalone review、Archive/Finish/Cleanup 与 Release publication/post-publish
  的每个正常失败都有 exact owner、blocked/terminal 与 re-entry，不以额外用户选择或副作用重放收敛。
- 既有 active lifecycle 可明确 retain/suspend、零 deletable resource 时 no-op abandon、有删除副作用时
  确认后 abandon/cleanup，或在不可逆远端边界保持原 candidate 并收敛为 current
  terminal/terminal block；cleanup 拒绝只形成唯一 choice，每类 disposition 都有完成或 exact blocked
  re-entry，且 cleanup 后 durable disposition result 仍可查询。
- 不可逆远程副作用后只 forward recover，不返回早期产品阶段。

### `EVO-007` 所有交付形态保持同一能力

- shared `.agents/skills` projection layer、Codex、Claude、Cursor 以及 canonical、dogfood、installed、
  preset、update/reapply 使用同一新合同；shared layer 只计一次，不作为第四个 host。
- Delivery、distribution、clean install、migration 与 Release 的外部 provider 动作使用同一
  live-reread、unknown-outcome、幂等、有界重试和 owning-boundary recovery 合同。
- distribution install/migration 先完成 `distribution_state_preclassification`；clean target 要求 active
  `.trellis/workflow.md` 缺失且不含任何可归属 official Trellis/Guru managed installation state；可唯一
  归属的 official Trellis footprint 即使 workflow/Guru projection 缺失也进入 existing migration；non-Guru active
  workflow 只有在 identity/provenance/owner 与当前安全 transition plan 均唯一收敛后才进入 existing
  migration，在此之前先标记 `foreign_workflow` 并 blocked，不能自动替换或要求先 mutation；
  partial/legacy Guru target（即使 workflow 缺失）进入 existing migration，mixed/unknown/unowned/multiple
  identity 先 blocked。existing repository 的
  active/resumable work、archived finish/history result 与 retained ref 在 cutover 前得到 preservation
  判定；迁移成功后经新合同保持可恢复、可查询、可达，且不依赖 legacy runtime consumer。
- exact-candidate Release 先以同一 candidate 证明完整 business runtime、RDT/Architecture lifecycle、
  执行成本治理和平台/install/update pre-publish matrix；独立确认后发布 immutable identity，再以
  tag-pinned post-publish smoke 收敛 `release_verified`。发布后语义 defect 保持原 identity
  `release_published_unverified`，只能由新的 request 按统一入口合同重新分类；只有
  `distribution/release` 的 exact-candidate Release action 才能创建 new candidate 修订；确认缺失只等待，明确拒绝以
  `release_not_published` 零副作用结束，candidate/关键 live facts 变化必须先使旧等待态失效并重做
  pre-publish；相对性能观测不成为发布门槛。

## 8. 目标追踪

### 8.1 场景到需求追踪

| 场景 | 功能需求 | 非功能主定义/验收 |
| --- | --- | --- |
| `REQ-UC-EVO-001..007,039..041,043` | `EVO-REQ-002..011,059..061,066` | `EVO-NFR-009..010,016..018`；对应 `EVO-FIX-INTAKE-CLEAR`, `EVO-FIX-INTAKE-REVIEWED-DESIGN`, `EVO-FIX-INTAKE-UNCLEAR`, `EVO-FIX-NO-ISSUE`, `EVO-FIX-TASK-FREE`, `EVO-FIX-TECH-REVISION`, `EVO-FIX-DETACHED-READ`, `EVO-FIX-CHANGE-REQUEST`, `EVO-FIX-BASE-REFRESH`, `EVO-FIX-SSOT-BOOTSTRAP`, `EVO-FIX-SUBMODULE-BOUNDARY` |
| `REQ-UC-EVO-008..018` | `EVO-REQ-012..026` | `EVO-NFR-007,014..015`；对应 `EVO-FIX-ARCH-NO-IMPACT`, `EVO-FIX-ARCH-ALIGNED`, `EVO-FIX-ARCH-CONFLICT`, `EVO-FIX-ARCH-INCOMPLETE`, `EVO-FIX-ARCH-NEW-DECISION`, `EVO-FIX-ARCH-REVISION`, `EVO-FIX-ARCH-NO-ADR`, `EVO-FIX-FRESH-EQUIVALENT`, `EVO-FIX-FRESH-SCOPE`, `EVO-FIX-TECH-REVISION`, `EVO-FIX-PLAN-NORMAL` |
| `REQ-UC-EVO-019..024,042` | `EVO-REQ-027..034,062..065` | `EVO-NFR-009..011,015`；对应 `EVO-FIX-BRANCH-FINDING`, `EVO-FIX-BASE-EVOLUTION`, `EVO-FIX-ARCH-PROMOTION`, `EVO-FIX-ARCH-DOWNSTREAM-FRESHNESS`, `EVO-FIX-RDT-DOWNSTREAM-FRESHNESS`, `EVO-FIX-PARALLEL`, `EVO-FIX-RDT-LIFECYCLE` |
| `REQ-UC-EVO-025..030` | `EVO-REQ-035..043,046..047,063,065` | `EVO-NFR-009..011,016..017`；对应 `EVO-FIX-FULL-NORMAL`, `EVO-FIX-NONE`, `EVO-FIX-PROVIDER-RECOVERY`, `EVO-FIX-FINISH-RECOVERY`, `EVO-FIX-HISTORY-RESUME`, `EVO-FIX-LATEST-INTENT`, `EVO-FIX-ARCH-DOWNSTREAM-FRESHNESS`, `EVO-FIX-RDT-DOWNSTREAM-FRESHNESS` |
| `REQ-UC-EVO-031..033` | `EVO-REQ-010,041,044..050` | `EVO-NFR-001..010`；对应 `EVO-FIX-PLAN-NORMAL`, `EVO-FIX-LATEST-INTENT`, `EVO-FIX-LONG-OUTPUT` |
| `REQ-UC-EVO-034..036` | `EVO-REQ-001,010,039,051..056` | `EVO-NFR-009..010,012..017`；对应 `EVO-FIX-ENTRY-ROUTING`, `EVO-FIX-PROJECTION`, `EVO-FIX-PROVIDER-RECOVERY`, `EVO-FIX-CLEAN-INSTALL`, `EVO-FIX-MIGRATION`, `EVO-FIX-RELEASE`；必须证明 target/current authority 分离与 distribution 二级 exactly-one action |
| `REQ-UC-EVO-037..038` | `EVO-REQ-057..058` | `EVO-NFR-009,014..015`；对应 `EVO-FIX-WORDING-EXPLICIT`, `EVO-FIX-QUALIFY-EXPLICIT`；必须证明这是 top-level specialist 的完整受支持 profile 集，并覆盖 review-only/change-scoped、active/standalone，以及所有结果的唯一 consumer/re-entry/terminal |
| `REQ-UC-EVO-044` | `EVO-REQ-010` | `EVO-NFR-009`；对应 `EVO-FIX-ENTRY-ROUTING`, `EVO-FIX-REQUEST-STOP` |
| `REQ-UC-EVO-045` | `EVO-REQ-010,034,049,055` | `EVO-NFR-009`；对应 `EVO-FIX-ENTRY-ROUTING`；必须证明最小 live read、通用只读 review 与两个 specialist profile 互斥、unavailable/unverified 诚实完成、答案不遗漏、零 mode/lifecycle/resource 副作用与 direct terminal |
| `REQ-UC-EVO-046` | `EVO-REQ-010,034,042..043,047,067` | `EVO-NFR-009,016..017`；对应 `EVO-FIX-REQUEST-STOP`, `EVO-FIX-HISTORY-RESUME`, `EVO-FIX-ACTIVE-DISPOSITION`；必须覆盖 retain/suspend、零资源 no-op abandonment、有资源 confirmed abandonment、cleanup 拒绝唯一 choice、cleanup 后 disposition history query、blocked exact re-entry 与 irreversible remote outcome boundary |
| `REQ-UC-EVO-047..048` | `EVO-REQ-068..080` | `EVO-NFR-019..032`；对应 `EVO-FIX-STOCK-COEXISTENCE`；必须逐项覆盖 17 个 logical stock asset、一个 shared `.agents/skills` projection layer、三个 supported host、每个 host 的五类 invocation context、`9/1/2/5` role closure、真实或明确标记的 caller/profile/typed-result/consumer handoff、lifecycle/source-stimulus/matcher 互斥（含 active user intent 与 passive context 负例）、suppressed semantic admission redirect/fail-closed 与 provider/explicit/worker boundary；raw before-dev/update-spec/meta 的 Guru successor 能力必须无损可达，platform/channel implement 均覆盖 task-free 与标准 Phase 2 owner。实际 patch/absence/quarantine/delete 只由 `EVO-FIX-STOCK-MAINTENANCE` 的已选 caller 承接，适用 authority slice 的 RDT/Architecture `authority_context` 不得重复读取 |
| `REQ-UC-EVO-049..050` | `EVO-REQ-072..080` | `EVO-NFR-022..032`；对应 `EVO-FIX-STOCK-MAINTENANCE`；必须覆盖 fresh install、existing migration、update/upgrade 的 dry-run discriminator 与两条 exact command 分支、workflow switch、preset reapply、`--force`/`--create-new`、user modification/deletion 与 `.new/.bak` sidecar 的最小 provenance、所选 action 的 pending/partial/unknown blocked/re-entry、Codex 三种 hooks 配置、capability preservation 与 mixed-graph prevention；未选 action 不要求额外验证 |
| `REQ-UC-EVO-051` | `EVO-REQ-081` | `EVO-NFR-017`；对应 `EVO-FIX-SEMANTIC-CONFIRMATION`；必须覆盖完整 current 计划后的多种语义肯定、READY PR merge、疑问/限制/修改/拒绝、material plan drift、exact-action scope isolation，以及固定口令、identity challenge、摘要复述、脚本解析和 authorization persistence 全部为 0 |

`EVO-REQ-053` 的 clean-install mapping 必须引用上文 clean-install observable contract；
`EVO-REQ-054` 的 migration mapping 必须引用同一个 composite invocation 中的
`MIG-CELL-INSTALL`、`MIG-CELL-UPGRADE`、`MIG-CELL-UPDATE`、`MIG-CELL-WORKFLOW-SWITCH` 与
`MIG-CELL-PRESET-REAPPLY` 五个有序 provider substep；共享一次 preflight、唯一 cutover 与 final
validation，分别保留每个 substep 的 provider owner/applicability/step-local live delta/blocked/re-entry，
并在 composite 级保留 preservation、legacy-consumer absence 与唯一 migration terminal 证据。
两者还必须引用 `EVO-REQ-010` 的 distribution-state preclassification：clean fixture 只接受
active workflow 缺失且无任何可归属 official Trellis/Guru managed installation state 的
`clean_target`；可唯一归属的 official Trellis footprint 即使缺少 workflow/Guru projection 也必须接受为
`existing_migration_target`；non-Guru active workflow 的
identity/provenance/owner 或当前安全 transition plan 未唯一收敛时，先作为 `foreign_workflow` 得到
`distribution_state_blocked`，不得当作 clean 或 migration；收敛后只重入 preclassification 并接受为
`existing_migration_target`，source workflow 保留到唯一 cutover。partial/legacy managed surface 即使
缺少 current workflow 也接受为
`existing_migration_target`，mixed/unknown/unowned/multiple identity 只能得到
`distribution_state_blocked`；该分类在 action 选择前完成且不产生 route 副作用。

### 8.2 Goal 追踪

| Goal | 场景 | 功能需求 | 非功能/验收 |
| --- | --- | --- | --- |
| `EVO-001` | `REQ-UC-EVO-001..007,014,039..043` | `EVO-REQ-002..011,021..022,059..062,064,066` | `EVO-FIX-INTAKE-CLEAR`, `EVO-FIX-INTAKE-REVIEWED-DESIGN`, `EVO-FIX-INTAKE-UNCLEAR`, `EVO-FIX-NO-ISSUE`, `EVO-FIX-TASK-FREE`, `EVO-FIX-TECH-REVISION`, `EVO-FIX-DETACHED-READ`, `EVO-FIX-CHANGE-REQUEST`, `EVO-FIX-BASE-REFRESH`, `EVO-FIX-SSOT-BOOTSTRAP`, `EVO-FIX-RDT-LIFECYCLE`, `EVO-FIX-SUBMODULE-BOUNDARY` |
| `EVO-002` | `REQ-UC-EVO-008..016,019,022..026,028..029` | `EVO-REQ-013..020,026..031,033,035,040,063` | `EVO-CAP-003`, `EVO-FIX-ARCH-NO-IMPACT`, `EVO-FIX-ARCH-ALIGNED`, `EVO-FIX-ARCH-CONFLICT`, `EVO-FIX-ARCH-INCOMPLETE`, `EVO-FIX-ARCH-NEW-DECISION`, `EVO-FIX-ARCH-REVISION`, `EVO-FIX-ARCH-NO-ADR`, `EVO-FIX-FRESH-EQUIVALENT`, `EVO-FIX-FRESH-SCOPE`, `EVO-FIX-ARCH-DOWNSTREAM-FRESHNESS`, `EVO-FIX-ARCH-PROMOTION`, `EVO-FIX-PARALLEL` |
| `EVO-003` | `REQ-UC-EVO-006..007,015..016,019..030,040..043,046` | `EVO-REQ-001,007..009,026..043,045..047,060..067` | `EVO-CAP-001,EVO-CAP-002`, `EVO-NFR-007,009..011,015,018`, `EVO-FIX-BASE-REFRESH`, `EVO-FIX-SSOT-BOOTSTRAP`, `EVO-FIX-RDT-LIFECYCLE`, `EVO-FIX-RDT-DOWNSTREAM-FRESHNESS`, `EVO-FIX-ACTIVE-DISPOSITION`, `EVO-FIX-SUBMODULE-BOUNDARY` |
| `EVO-004` | `REQ-UC-EVO-001..051` | `EVO-REQ-010..012,024..025,027..028,034,040,051,057..081` | `EVO-NFR-007,009,014..015,017,019..031`, `EVO-FIX-ENTRY-ROUTING`, `EVO-FIX-REQUEST-STOP`, `EVO-FIX-ACTIVE-DISPOSITION`, `EVO-FIX-SEMANTIC-CONFIRMATION`, `EVO-FIX-WORDING-EXPLICIT`, `EVO-FIX-QUALIFY-EXPLICIT`, `EVO-FIX-CHANGE-REQUEST`, `EVO-FIX-FINISH-RECOVERY`, `EVO-FIX-STOCK-COEXISTENCE`, `EVO-FIX-STOCK-MAINTENANCE`；每个 direct-answer/readiness/specialist/Finish/Cleanup/disposition/stock-policy result 都必须回到唯一 caller/owner 或 terminal，不得把 re-entry 误报为 workflow completion；source class、caller/profile/typed result、首次 action-required、update 分支、hooks 配置与 dialogue-local semantic confirmation 不得遗漏 |
| `EVO-005` | `REQ-UC-EVO-017..018,030..033,045..046,051` | `EVO-REQ-010,023..026,044..050,067,081` | `EVO-CAP-004`, `EVO-NFR-001..009,017`, `EVO-FIX-ENTRY-ROUTING`, `EVO-FIX-PLAN-NORMAL`, `EVO-FIX-HISTORY-RESUME`, `EVO-FIX-ACTIVE-DISPOSITION`, `EVO-FIX-SEMANTIC-CONFIRMATION`, `EVO-FIX-LATEST-INTENT`, `EVO-FIX-LONG-OUTPUT` |
| `EVO-006` | `REQ-UC-EVO-019..033,037..038,042..046,051` | `EVO-REQ-010,027..050,057..058,062,065..067,081` | `EVO-CAP-001..004`, `EVO-FIX-ENTRY-ROUTING`, `EVO-FIX-REQUEST-STOP`, `EVO-FIX-ACTIVE-DISPOSITION`, `EVO-FIX-SEMANTIC-CONFIRMATION`, `EVO-FIX-FULL-NORMAL`, `EVO-FIX-NONE`, `EVO-FIX-PROVIDER-RECOVERY`, `EVO-FIX-FINISH-RECOVERY`, `EVO-FIX-WORDING-EXPLICIT`, `EVO-FIX-QUALIFY-EXPLICIT`, `EVO-FIX-RDT-DOWNSTREAM-FRESHNESS`, `EVO-FIX-SUBMODULE-BOUNDARY` |
| `EVO-007` | `REQ-UC-EVO-034..036,047..051` | `EVO-REQ-010,039,052..056,068..081` | `EVO-CAP-001..004`, `EVO-NFR-009..010,012..015,017,019..031`, `EVO-FIX-ENTRY-ROUTING`, `EVO-FIX-PROJECTION`, `EVO-FIX-PROVIDER-RECOVERY`, `EVO-FIX-CLEAN-INSTALL`, `EVO-FIX-MIGRATION`, `EVO-FIX-RELEASE`, `EVO-FIX-SEMANTIC-CONFIRMATION`, `EVO-FIX-STOCK-COEXISTENCE`, `EVO-FIX-STOCK-MAINTENANCE` |

Design/Test/Architecture candidate mapping 已建立并同步 `REQ-REV-011..132` 的 current content；
同一 `evolution-requirements-revision-2026-08-27` exact identity 已通过 fresh Requirements gate，
当前 mapping 为 `requirements_input_current` planning projection，可作为下一次 Evolution Design
全稿审核输入。它不构成 Design pass、implementation 或 shared current promotion 证据。

## 9. 非目标

- 除承载本 Requirements 审核自身的既有隔离 task/worktree/branch 外，不据本 target authority
  选择、重写或修订现有 Issue 链，也不创建后续实施 Issue、task、worktree、branch、PR 或 Release；
  这些后续资源属于后续阶段的独立入口。
- 不在 Requirements 阶段确定 Skill 数量/名称、typed exit id、schema、DTO、script、文件布局、
  platform overlay 实现或 Issue 顺序。
- 不把 `EVO-EVD-002` 的 visible session 当作唯一根因证明或性能基准，不追求对单次历史会话
  做逐消息复刻。
- 不保留旧 Guru Team workflow 合同、旧 Issue Scope Ledger、旧 aggregate/handoff 或兼容
  wrapper；只保留经本文件明确列出的产品能力。
- 不在 Planning 直接修改 shared Requirements/Design/Test/Architecture current authority。
- 不把 parent repository 的 Git submodule 内容提升为 parent RDT/code authority，也不在 parent
  task 中顺带修复、初始化、更新或验证 submodule；显式 submodule repository task 是独立 scope。
- 不处理恶意 actor、对抗输入、故意伪造/篡改 artifact 或未要求的锁/TOCTOU/并发压力加固。
- 不通过减少 semantic review、跳过 full-diff evidence、隐藏 unverified boundary 或降低平台
  矩阵来制造表面上的流程精简。

## 10. 进入 Evolution Design 的条件

`requirements_ready_for_design` 只表示 Requirements 文档本身具备进入 Design 的资格。其门禁
条件依次为：

1. `EVO-NFR-001..008` 已按 `EVO-EVD-007` 收敛为执行成本与上下文治理约束，不包含相对 baseline
   的耗时、rounds、bytes、compression 或改善比例 Release 门槛；
2. `EVO-CAP-001..004` 的核心能力收敛结果具有用户确认；当前由确认四项独立 `P0` 的
   `EVO-EVD-010` 与收敛执行成本验收口径的 `EVO-EVD-007` 共同满足；
3. [`current-capability-inventory.md`](./current-capability-inventory.md) 的 completion contract
   全部满足：`.40` previous Skill、current Requirements/Behavior/NFR/Test capability 孤儿项为 0，
   每个 retained capability 均有 target requirement 与 fixture successor，17 个 logical stock
   asset、shared-layer/three-host projection matrix 与各 host context matrix 无未知、重复或孤儿项；
   role count 必须为 `suppressed_semantic_route=9`、`provider_only=1`、`explicit_only=2`、
   `controlled_worker_provider=5`；
   每个 stock asset 还必须有 source owner、唯一 policy binding、target projection cell、真实
   current direct consumer 或明确的 consumer handoff projection、Design handoff id 与
   mutation/interception owner status。官方 ownership 与
   Guru control-plane 尚未形成受支持 interception boundary 的 asset 必须保持
   `upstream_suppression_blocked`/`provider_boundary_blocked`，retained host row 的 context failure
   使用 `retained_context_blocked`，并带着该 handoff 进入 Design；每个 action 的
   completed/pending/unknown、按 identity/state/decision-relevant facts 变化触发的定向 fresh reread
   与 exact owner re-entry 也必须闭合。Requirements gate 不
   要求 current mutation owner 已实现，implementation candidate 则不得绕过这些 blocked 分支；
   `consumer_unbound`、`current_drift` 或 `design_handoff` 只能作为 Design handoff projection，
   不得被计为 current closure；
4. 完成一次 fresh、独立 Requirements 全稿审核，未解决 `P1` 与阻断性 `P2` finding 均为 0；非阻断性 `P2` 必须具有不改变范围、验收或设计承接的明确假设；
5. 重复主定义为 0，API/CLI 差集无缺失，非功能豁免完整。

本门禁的 `finding_severity` 只使用 `P1/P2/P3`；第 1.5 节中的 `P0/P1/P2` 只表示
`capability_priority`，不得混作 finding 严重度。

当前 `REQ-REV-011..132` 的正文修订已完成；其中 `REQ-REV-029..132` 改变了 exact candidate 的
状态、stock action partial/unknown、explicit provider result、两级 entry/action、change readiness、caller ownership、standalone specialist terminal、
Archive/Finish/Cleanup recovery、direct-answer route 与 unavailable boundary、受支持 specialist profile
闭包、active lifecycle disposition/cleanup refusal/no-op abandonment/durable history query、Release
publication/post-publish terminal、current-authority trace、
candidate identity、additive/generic override route、stock role/suppression/provenance policy 与最新
  修订证据闭包，并新增 `EVO-REQ-075..080`/`EVO-NFR-026..032` 对首次 action、source matcher、
  update 分支、pre-semantic cost、caller/consumer binding 与 hooks configuration 的约束；本轮
  `REQ-REV-092..102` 进一步闭合独立请求 isolation/liveness、无 active fixture、file-changing
  mode applicability、stock action 单一主定义、正式能力字段、specialist caller/standalone
  terminal projection、远端 pending intent identity/envelope 顺序与 bound override 的旧 owner
  consumption/new invocation identity/envelope boundary，并将功能行为 SSOT、状态投影、no-active
  coverage 与 release inventory summary 收敛为对统一入口合同的单向引用；`REQ-REV-102` 进一步把
  第二章入口摘要、根 Requirements README 的 target 读取顺序与 source-stimulus 的内部/上游 event
  边界收敛为单向导航和 admission 语义，不新增 route 或 receipt 合同；`REQ-REV-103` 进一步把
  post-publish semantic-defect follow-up 收敛为统一 entry reclassification：new change 先完成独立
  change lifecycle，只有后续 `distribution/release` exact-candidate Release action 才创建新 candidate；
  状态图、fixture、目标总结与 evidence 只引用该边界，不另立 route 或 candidate 合同；
`REQ-REV-104` 仅将 Evidence 表统一为三列，不改变任何证据语义或 gate 结论；`REQ-REV-105`
进一步闭合 isolation pending 的 progress-refresh、safe-clear/re-entry 与 blocked liveness；
`REQ-REV-106` 将根安装与 workflow README 的 switch 文案统一为 preview -> explicit `--force`；
`REQ-REV-107` 将 preset README 的同一 provider 文案补齐 preview/preflight/force 语义；`REQ-REV-108`
将 migration matrix 的物理执行顺序、composite-only terminal、显式 cutover phase 与前后 failure
分类统一为同一 provider 合同；`REQ-REV-109` 将 distribution target 收敛为 clean、existing
migration 与 blocked 三态 preclassification，明确 Intake 不读取 Architecture、pre-design Planning
从同一 invocation envelope 按需消费 RDT/Architecture，并让 migration cell 按适用性执行、全
`not_applicable` 时仍完成一次 composite final validation。`REQ-REV-110..115` 又完成 fresh-main
authority reconciliation，补入 Gitlink/EOF 两项 current capability，并将 raw before-dev、update-spec、
meta 统一改为 Guru successor 完全承接的 suppression，同时把 channel implement 收敛为 task-free/
标准 Phase 2 双 profile owner。`REQ-REV-116` 进一步把 channel transport、worker result、explicit-only
history/diagnosis 与 Guru-owned spec/reference successor 完全拆开，删除 raw explicit write action，
并把任何 follow-up 写入前置回统一 Guru route。`REQ-REV-117` 闭合已识别 non-Guru workflow 在
transition plan current 后只经 preclassification 正向进入 existing migration、并保留到唯一 cutover
的合同；`REQ-REV-118` 将 hook 高层配置收敛为 per-host、applicability-aware setup partition 的派生
  coverage，排除无 approval surface host 的不可能 fixture；`REQ-REV-119` 明确同一 top-level
  invocation 内的 migration/provider substep、worker return 与 upstream event 复用既有 guard/envelope，
  不生成第二 receipt 或重跑顶层分流。`REQ-REV-120` 将可唯一归属的 official Trellis-only
  installation footprint 从 clean target 排除并纳入 existing migration；`REQ-REV-121` 明确
  byte-equal predicate 只有在固定顺序抵达 WORKFLOW-SWITCH boundary 后才推进 cutover，entry bytes
  不改变前序 finding 分类。`REQ-REV-122` 将 mandatory PRESET-REAPPLY 的 current、blocked 与 exact
  re-entry 显式投影到 migration state graph/return matrix；`REQ-REV-123` 将 standalone explicit-only
  direct-answer result 与 embedded caller return 拆成互斥 profile；`REQ-REV-124` 将 suppressed successor
  不可达归类为 capability-preservation/consistency finding，并固定返回
  `upstream_suppression_blocked`，不再混入 capability-loss gate。`REQ-REV-125` 将完整计划后的
  dialogue-local semantic affirmative、exact-action scope、material drift 后重新展示、READY PR merge
  与 script/validator/recorder 零解析/零持久化闭合为 `EVO-REQ-081`，并明确排除
  `确认执行 <hash>`、identity challenge、摘要复述和固定 `合并PR` gate。`REQ-REV-126` 将
  `REQ-UC-EVO-051`、`EVO-EVD-042` 与 semantic-confirmation fixture 回写阶段 0 候选池及
  `EVO-CAP-001/EVO-CAP-004`，完成核心能力最终校正；`REQ-REV-127` 在回程矩阵补齐明确拒绝的
  零副作用与 route-local refusal/stop/re-entry；`REQ-REV-128` 将已存在且已同步 current draft 的
  Design/Test/Architecture candidate mapping 正确标记为 `fresh_review_pending` planning projection，
  并要求 Requirements ready 后重新绑定同一 exact identity 才可进入 Design 全稿审核。`REQ-REV-129`
  进一步把 repository RDT、Architecture Baseline 与 task 三件套的稳定 locator/identity/order 定义为
  normal workflow 的主要可缓存上下文，把 live facts/delta 收窄到最小变化 tail，并要求 AI owner 直接
  自主判断；cache 不成为 authority/evidence/PASS，人类式 assignment/signoff/transaction handoff、
  already-current fact restatement 与无 consumer 中间文档计数均为 0。`EVO-EVD-026..027` 对 stock package
  与 ownership handoff 的研究边界、`EVO-EVD-037..042` 对 current reconciliation、stock role、
  distribution/guard findings、init-provider clean/migration 分类、跨投影修订与 semantic confirmation
  缺陷的证据仍不证明任何 patch/delete 已实现，之前候选的审核通过结论均未复用。`REQ-REV-130`
  将根 Requirements 导航中错误保留的 ready 声明恢复为 current draft；`REQ-REV-131` 修正
  WORKFLOW-SWITCH phase chain 的 inline-code 定界，不改变 migration 语义。`REQ-REV-132` 将 stable
  RDT/Architecture/task-doc context hierarchy、minimal live tail、cache-unavailable correctness equivalence、
  AI-owned direct judgment 与零 human-style handoff/current-fact restatement 完整投影到
  Design/Test/Architecture/task planning，并且不新增中间 handoff/cache artifact。`EVO-EVD-043`
  已使绑定 `REQ-REV-011..128` 的旧 fresh review 结论 stale；当前 exact candidate 的
  `REQ-REV-129..132` 完整投影已通过 fresh 独立 Requirements 全稿 semantic review、Strict
  technical review 与确定性闭包，状态为 `requirements_ready_for_design` /
  `requirements_trace_ready_for_design`。本轮在 Requirements gate 通过后停止；不执行 Evolution
  Design 全稿审核，不激活 task 或进入实现。

Requirements 审核通过后，下一阶段才定义：整体状态模型、唯一 semantic owner、Skill-first
边界、public input/output 与 typed exits、最小 runtime state、platform projection、迁移方式、
eval harness 和推进拆分。Design 与推进方案全部审核通过后，才以该 SSOT 创建全新的串行
Issue 链；现有 `#247 -> #267` 链继续保持发布后的候选参考，不自动成为执行计划，也不进入
重构前稳定版 `v0.6.15-guru.1` 的 Release gate。

## 最终用户结果

> 用户给出一个新需求或已审阅设计后，Guru Trellis 能用最少必要交互理解它；标准路径先回读
> parent repository current RDT，并把 task planning 收窄为对 RDT 的引用、delta/contribution 与
> 执行映射，再在写设计前真正消费现有架构；必要时持续回写 task-local RDT/Architecture
> contribution并经受治理的 promotion 推进 shared current，然后沿清晰的 owner 链完成实现、审查、
> 交付与清理。parent task 默认完全忽略无关 Git submodule；task-free 直接完成有界检查闭环。
> 普通 non-file-changing 请求和通用只读 review 直接回答，live facts 不可用时透明标记未验证边界；
> 既有 active lifecycle 可保留/暂停、零资源直接放弃、有删除资源时确认后放弃清理，或在不可逆远端
> 边界保持原结果并收敛，且 disposition 在 cleanup 后仍可查询。全程不依赖冗余交接文件，也不会在
> 阶段之间丢失语义或最新用户意图。

Guru Trellis 的本轮进化只有在同一个 exact candidate 上对 `EVO-001..007`、全部适用
`REQ-UC-EVO-*`、`EVO-REQ-*` 和 `EVO-NFR-*` 建立 current、可复现、无互相矛盾的端到端
证据后才算完成。单个 Skill、单个 Issue、静态 schema、历史运行或局部平台通过只能证明
对应局部结果，不能替代整体完成。
