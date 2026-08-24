# Guru Trellis Evolution Requirements

版本：`evolution-requirements-draft-2026-08-24`；文档状态：`requirements_draft`；目标层
`EVO-001..007` 状态：`user_confirmed`；详细需求层状态：`ai_drafted`；最后修订：
`2026-08-24`。

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

它定义 target，不声明 current runtime 已经实现、验证或发布这些结果。current 行为仍由
[`current-main-0.6.5-guru.40/requirement-main.md`](../versions/current-main-0.6.5-guru.40/requirement-main.md)、
current Design/Test/Architecture authority、canonical workflow/Skill package 以及
Git/live facts 共同证明。

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

本节只约束发布后的重构 candidate，不追溯修改重构前稳定版：`v0.6.15-guru.1` 有意冻结
current 旧 graph、`issue-scope-ledger.json` 与现有稳定流程；该 pre-refactor release 不声称
实现任何 `EVO-*` target，也不以本目录作为 Release blocker。

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
- 使用 Shared、Codex、Claude 或 Cursor 执行 Guru Team workflow 的工程 Agent；
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

### 1.4 全量功能与场景清单

#### A. 请求进入与 requirement authority

| 场景 | 触发 | 目标结果 |
| --- | --- | --- |
| `REQ-UC-EVO-001` 清晰 Issue 需求 | live Issue 已充分描述业务目标、范围与验收 | 零例行提问地形成忠实、可追踪的 current requirement authority |
| `REQ-UC-EVO-002` Issue 含已审阅设计 | Issue 同时包含需求和已审阅的设计承诺 | 产品需求与 reviewed-design commitments 分别保真承接；后续 `design.md` 不得忽略、重写或无说明背离已审阅设计 |
| `REQ-UC-EVO-003` 信息不足或来源冲突 | 用户请求、Issue 正文/评论或 current authority 存在真实歧义 | 每轮只问一个最高价值问题；冲突显式化；在信息充分前不猜测、不启动下游副作用 |
| `REQ-UC-EVO-004` 无现有 Issue 的标准变更 | 请求需要标准 task/交付但没有 Issue | 先完成必要的需求理解和重复/范围判断，再就精确外部副作用取得确认；不得伪造 Issue identity |
| `REQ-UC-EVO-005` 有界 task-free 变更 | 请求满足 task-free 产品边界 | 在 current checkout 内完成有界闭环；不创建 Issue/task/worktree，不生成正式 `prd.md`/`design.md`/`implement.md`，也不借此绕过适用检查；范围演进后自动返回 standard route |
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
| `REQ-UC-EVO-025` `github_pr` 正常交付 | review 后需要发布 PR | 从 live Issue/Git/GitHub/current plan 形成真实 PR readiness、关闭语义和 expected-head delivery；不依赖 Issue Scope Ledger |
| `REQ-UC-EVO-026` `none` 正常交付 | 当前变更不使用 GitHub PR provider | 不调用 GitHub，不伪造 PR/Issue 事实；仍完成适用的 acceptance、Finish、history 与 owned-resource cleanup |
| `REQ-UC-EVO-027` provider 或外部状态失败 | push/PR/merge/Issue closure 等正常外部动作失败或状态变化 | 保留已完成且 current 的结果，从 delivery owner 恢复；不重复不可逆动作，不返回需求/Planning/实现 |
| `REQ-UC-EVO-028` Acceptance/Delivery/Merge | candidate 已完成 full-diff review | acceptance、publication、delivery、merge 和 closure 各自判断真实 current facts，顺序无倒置、无重复 semantic owner |
| `REQ-UC-EVO-029` Finish 与资源清理 | delivery 已达到对应 terminal condition | deterministic Finish 形成最小 durable history；只清理 exact owned resources，并验证必须保留的 commit/ref 可达性 |
| `REQ-UC-EVO-030` 历史查询与恢复 | 当前会话结束、压缩、重启或任务已归档 | 从 current authority、live facts 与最小 durable result 恢复，不依赖长篇 handoff summary、旧 locator 集合或授权记录 |

#### E. 对话连续性、分发与 Release

| 场景 | 触发 | 目标结果 |
| --- | --- | --- |
| `REQ-UC-EVO-031` 用户在长流程中追加意图 | Agent 正在等待工具/恢复/压缩，用户给出新指令 | 最新用户意图按到达顺序被优先消费；若覆盖旧请求则停止旧路线，若追加则与未完成请求一起承接；不得静默丢失 |
| `REQ-UC-EVO-032` 长运行命令或 Agent 工作 | 工具/子流程需要多次轮询或产生大量输出 | 每次只返回新增、紧凑、可消费结果；复用有效运行句柄，不重复注入累计 stdout，不制造无效 wait |
| `REQ-UC-EVO-033` 正常清晰请求 | 无歧义、无 finding、无外部失败 | 用户只看到真实选择、实质 finding/block、必要长等待状态、阶段结果和副作用确认，不看到 workflow 内部 artifact 搬运 |
| `REQ-UC-EVO-034` 平台与安装投影 | Shared/Codex/Claude/Cursor、canonical/dogfood/installed、apply/reapply/update 使用同一 candidate | 全部入口具备同一语义能力和路由，且没有旧合同残留、sidecar 或未审查 drift |
| `REQ-UC-EVO-035` official Trellis upgrade/update | 新仓库安装或已有仓库迁移到目标 candidate | 通过官方扩展面恢复完整新合同；已有仓库迁移后只运行新路径，用户数据与 current authority 不丢失 |
| `REQ-UC-EVO-036` exact-candidate Release | 所有演进实现已汇合 | 同一个 exact candidate 通过功能、Architecture lifecycle、执行成本/安静性治理、平台/install/update 与 post-publish smoke 后才可发布；不使用相对性能数值作 Release 门槛 |
| `REQ-UC-EVO-037` 显式合同措辞审核 | 用户明确要求审核有界 contract wording，或文字本身就是 change scope | 保留独立、可复用的 semantic wording review 能力；它只审核指定文字，不成为正常 Planning 的 mandatory gate |
| `REQ-UC-EVO-038` 显式 normal-scenario qualification | caller 的 current authority 明确要求判断候选是否属于受支持 normal scenario | 保留有界 qualification 能力并把结果返回唯一 caller；普通、直接派生的验收场景不经过该入口 |
| `REQ-UC-EVO-039` change request scope/prerequisite 审核 | standard request 可能重复、依赖未满足或不是一个可独立交付单元 | 在资源副作用前基于 live Issue/authority 判断复用、澄清、阻塞或独立交付 readiness；不把该判断与后续 requirement authoring 重复执行 |

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
| 意图到交付的 authority 与 route 连续性 | `REQ-UC-EVO-001..007,015..016,019..022,024..041,043` | `selected` -> `EVO-CAP-001` | 直接决定请求能否忠实、唯一地到达正确终点；来源冲突、scope/identity freshness、owner/re-entry、submodule scope 边界和不可逆副作用恢复可独立造成断链或错误交付；后续设计必须展开 authority resolution、route 状态与 terminal correctness，但不代替 RDT/Architecture 各自的 shared-current 生命周期 |
| Repository RDT SSOT 驱动与受治理演进 | `REQ-UC-EVO-001..003,006..007,015..016,019..030,034..036,040..043` | `selected` -> `EVO-CAP-002` | task planning 冒充或绕过 repository RDT 时，即使 route、Architecture 和工具执行都正常，产品/设计/测试语义仍会与 shared current 脱节；false-no-impact、跨 R/D/T 追踪、持续回写、serialized promotion、并行 contribution 与 downstream freshness 具有独立一致性和高返工风险，后续设计必须单独展开 |
| Architecture-aware Planning 与受治理演进 | `REQ-UC-EVO-008..016,019,022..026,028..029` | `selected` -> `EVO-CAP-003` | 不在 design 首稿前消费 baseline，或下游使用 stale alignment/proposal 状态，都会破坏核心目标；冲突、shared promotion 与跨阶段 freshness 具有动态决策、一致性和高返工风险；需独立展开 |
| 低成本且不中断的执行连续性 | `REQ-UC-EVO-017..018,030..033` | `selected` -> `EVO-CAP-004` | 当前观测已显示重复判断、输出规模、等待和压缩会使正常工作无法完成；执行成本、上下文生命周期、恢复和最新意图连续性可独立破坏用户完成工作，需与 `EVO-CAP-001` 的 authority/terminal correctness 分开展开 |
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
| `capability_level` / `parent_capability_refs` | `top_level` / 无 |
| `priority` | `P0` |
| `business_outcome` | 用户意图、accepted scope、已审阅设计承诺和交付状态在每个阶段保持忠实、current、可追踪，并由唯一 owner/route 到达正确终点 |
| `value_chain` | 请求/Issue -> requirement/change readiness -> exact scope/identity -> approved planning -> implementation/check/review -> publication/delivery -> Finish/history |
| `difficulty_focus` | 多来源冲突、submodule scope 排除、scope/identity freshness、唯一 owner/consumer、最早受影响点重入、不可逆副作用后的 forward recovery |
| `complexity_source` | 动态语义判断、跨阶段状态黏着、外部 Git/GitHub/Trellis facts、一致性与恢复边界 |
| `design_focus` | current authority resolution、语义依赖传播、阶段状态、唯一 owner/consumer、re-entry 与 terminal route |
| `design_expansion_requirement` | 展开 normal/revision/stale/blocked/recovery 状态、authority 读取与 submodule scope 边界、scope/identity freshness、不可逆动作边界、terminal correctness 和并行隔离；RDT 与 Architecture shared-current lifecycle 分别由 `EVO-CAP-002`、`EVO-CAP-003` 展开 |
| `risk_if_missed` | 产品意图被改写、重复 intake、错误关闭 Issue、阶段断链或错误交付 |
| `success_metrics` | 在同一个 exact-candidate Release gate 时间窗内，以 `EVO-FIX-INTAKE-CLEAR`、`EVO-FIX-INTAKE-REVIEWED-DESIGN`、`EVO-FIX-INTAKE-UNCLEAR`、`EVO-FIX-NO-ISSUE`、`EVO-FIX-TASK-FREE`、`EVO-FIX-TECH-REVISION`、`EVO-FIX-DETACHED-READ`、`EVO-FIX-CHANGE-REQUEST`、`EVO-FIX-BASE-REFRESH`、`EVO-FIX-BASE-EVOLUTION`、`EVO-FIX-BRANCH-FINDING`、`EVO-FIX-FULL-NORMAL`、`EVO-FIX-NONE`、`EVO-FIX-PROVIDER-RECOVERY`、`EVO-FIX-HISTORY-RESUME` 和 `EVO-FIX-SUBMODULE-BOUNDARY` 各至少 1 条 exact trace 为样本；全部通过，且需求静默漂移、unmapped route、submodule scope 泄漏、不可逆动作重放均为 0 |
| `failure_impact` | 即使局部工具通过，也不能把结果定义为正确交付 |
| `acceptance_bar` | 每个支持场景都有唯一 current authority、唯一下一 owner/终点和可复现验收证据 |
| `validation_strategy` | authority conflict、scope change、equivalent publication、submodule scope 排除、base/provider recovery、两种 delivery route、terminal cleanup 与唯一 consumer/stop fixtures；RDT/Architecture correctness 由对应独立核心能力 fixture 证明 |
| `source_req_refs` | `REQ-UC-EVO-001..007,015..016,019..022,024..041,043` |
| `evidence_refs` | `EVO-EVD-001,EVO-EVD-003,EVO-EVD-004,EVO-EVD-008,EVO-EVD-009` |
| `priority_score` | 业务影响 5 / 系统复杂度 5 / 失败成本 5，总分 15 |
| `priority_rationale` | 它承载意图到 terminal result 的 authority/route 主线；没有连续 authority 与唯一 route 即无法定义交付正确 |
| `counterfactual_check` | 不能延期；延期后仍会出现产品意图漂移或生命周期断链，本轮进化不能算成功 |
| `confirmation_status` | `user_confirmed_with_edits` |
| `open_questions` | 无 |

#### 1.5.3 `EVO-CAP-002` Repository RDT SSOT 驱动与受治理演进

| 字段 | 内容 |
| --- | --- |
| `capability_level` / `parent_capability_refs` | `top_level` / 无 |
| `priority` | `P0` |
| `business_outcome` | Repository Requirements/Design/Test 是唯一 shared 产品、设计与测试 authority；每个 standard task 在写作和执行前实际消费 current RDT，只通过 task-local contribution 与受治理 promotion 完善 shared current |
| `value_chain` | bootstrap/current RDT -> pre-read/impact -> task-local projection/contribution -> Planning/Implementation 持续回写 -> independent review/serialized promotion -> 受影响的 Phase 2/full-diff review/delivery freshness -> Finish |
| `difficulty_focus` | `rdt_no_impact`、`rdt_aligned`、`rdt_contribution_required`、`rdt_authority_blocked` 的真实判定，R/D/T 追踪，Implementation 中间发现回写，promotion conflict，并行 task 与 material/identity-equivalent freshness |
| `complexity_source` | 多文档语义一致性、shared current 与 task candidate 分离、跨阶段状态黏着、single-writer promotion、并行 contribution 和高返工风险 |
| `design_focus` | RDT current authority/identity、impact 状态机、task planning projection 边界、contribution lifecycle、独立 review/promotion、下游 consumer 与最早受影响点重入 |
| `design_expansion_requirement` | 展开 Requirements/Design/Test 各自责任与追踪、bootstrap/repair、四类 impact exit、task-local candidate 的新增/修订/替换/拆分/合并/删除、持续回写、expected-current serialized promotion、并行隔离、downstream freshness、Finish 消费边界和 submodule 默认排除；不得把 task 三件套设计成平行 RDT |
| `risk_if_missed` | task planning 或代码事实冒充 shared RDT、false-no-impact 被批准、R/D/T 追踪断裂、多个 task 形成双 current、实现发现未回写，最终发布无法代表 repository current 产品语义 |
| `success_metrics` | 在同一个 exact-candidate Release gate 证据采集时间窗内，以 `EVO-FIX-SSOT-BOOTSTRAP`、`EVO-FIX-PLAN-NORMAL`、`EVO-FIX-RDT-LIFECYCLE`、`EVO-FIX-RDT-DOWNSTREAM-FRESHNESS`、`EVO-FIX-PARALLEL`、`EVO-FIX-FULL-NORMAL`、`EVO-FIX-SUBMODULE-BOUNDARY`、`EVO-FIX-MIGRATION` 和 `EVO-FIX-RELEASE` 各至少 1 条 exact trace 为样本；全部通过，且 task-planning-as-RDT、错误 no-impact、stale downstream consumption、双 current、Finish 后补写 RDT 和 submodule authority 泄漏均为 0 |
| `failure_impact` | 即使 intent route、Architecture alignment 和工具执行都通过，也不能把 candidate 定义为目标 Guru Trellis |
| `acceptance_bar` | 所有 standard task 在首份 planning artifact 前绑定 current RDT 并得到证据相符的唯一 impact；最终 approved plan、实现、review、delivery 与 terminal state 均消费 current binding 或合法 task-local contribution，shared current 只经独立串行 promotion 前进 |
| `validation_strategy` | bootstrap/repair、no-impact/aligned/contribution/blocked、错误自报 no-impact、task-local projection 非替代性、Implementation 持续回写、review revision、expected-current conflict、serialized promotion、并行隔离、downstream freshness、migration/release 与 submodule boundary fixtures |
| `source_req_refs` | `REQ-UC-EVO-001..003,006..007,015..016,019..030,034..036,040..043` |
| `evidence_refs` | `EVO-EVD-004,EVO-EVD-006,EVO-EVD-008,EVO-EVD-009,EVO-EVD-010` |
| `priority_score` | 业务影响 5 / 系统复杂度 5 / 失败成本 5，总分 15 |
| `priority_rationale` | RDT 是跨 task 持续表达产品、设计和测试语义的唯一 shared authority；缺失该能力会让每个 task 的局部 PASS 与 repository 长期事实脱节 |
| `counterfactual_check` | 不能延期；延期后 task planning 仍可能冒充或绕过 RDT，即使其余核心能力完成，本轮文档中心转换仍失败 |
| `confirmation_status` | `user_confirmed_with_edits` |
| `open_questions` | 无 |

#### 1.5.4 `EVO-CAP-003` Architecture-aware Planning 与受治理演进

| 字段 | 内容 |
| --- | --- |
| `capability_level` / `parent_capability_refs` | `top_level` / 无 |
| `priority` | `P0` |
| `business_outcome` | design 首稿建立在 current Architecture 上，合法新需求既不被 baseline 吞掉，也能提出受治理的 Architecture 演进 |
| `value_chain` | requirement/reviewed design -> current baseline/constitution/change contract -> alignment/conflict/proposal -> implementation/check/review -> publication/acceptance/Finish freshness -> reviewed promotion 后受影响证明重算 |
| `difficulty_focus` | no-impact、正常承接、真实冲突、authority 不完整、新 decision、既有 decision/GAP/ownership 修订的区别 |
| `complexity_source` | 多 authority 一致性、原则取舍、shared current 串行演进、并行 task freshness |
| `design_focus` | 写作前消费点、alignment 主承载位置、proposal/ADR 判定、下游 current binding、shared promotion 与 downstream re-entry |
| `design_expansion_requirement` | 展开 impact 状态、conflict 决策、proposal lifecycle、各下游责任边界的 freshness、expected-current promotion、owner/single-writer/compatibility exit 与 fresh proof |
| `risk_if_missed` | 首稿忽略 baseline、PRD 被架构改写、不必要 ADR、双 current、未经 review 的 shared Architecture 变更 |
| `success_metrics` | 在同一个 exact-candidate Release gate 证据采集时间窗内，以 `EVO-FIX-ARCH-NO-IMPACT`、`EVO-FIX-ARCH-ALIGNED`、`EVO-FIX-ARCH-CONFLICT`、`EVO-FIX-ARCH-INCOMPLETE`、`EVO-FIX-ARCH-NEW-DECISION`、`EVO-FIX-ARCH-REVISION`、`EVO-FIX-ARCH-NO-ADR`、`EVO-FIX-FRESH-EQUIVALENT`、`EVO-FIX-FRESH-SCOPE`、`EVO-FIX-ARCH-DOWNSTREAM-FRESHNESS`、`EVO-FIX-ARCH-PROMOTION`、`EVO-FIX-PARALLEL` 各至少 1 条 exact trace 为样本；全部通过，且首稿未读 current authority、Planning 直接写 shared current、不必要 ADR、下游消费 stale Architecture binding 均为 0 |
| `failure_impact` | 架构方法论无法被贯彻，后续重构版即使完成发布动作也不是目标产品 |
| `acceptance_bar` | Architecture 场景 fixture 全覆盖，最终 approved plan 与 current baseline 对齐或包含明确、受治理的 evolution proposal |
| `validation_strategy` | no-impact、aligned、conflict、missing/stale、new decision、existing decision revision、unnecessary ADR、downstream freshness 与 parallel promotion fixtures |
| `source_req_refs` | `REQ-UC-EVO-008..016,019,022..026,028..029` |
| `evidence_refs` | `EVO-EVD-001,EVO-EVD-004` |
| `priority_score` | 业务影响 5 / 系统复杂度 5 / 失败成本 5，总分 15 |
| `priority_rationale` | Architecture Baseline 方法论是最终发布必须贯彻的产品目标，不是可延期增强 |
| `counterfactual_check` | 不能延期；延期后仍只能产后审核 Architecture，无法证明首稿承接 current baseline |
| `confirmation_status` | `user_confirmed_with_edits` |
| `open_questions` | 无 |

#### 1.5.5 `EVO-CAP-004` 低成本且不中断的执行连续性

| 字段 | 内容 |
| --- | --- |
| `capability_level` / `parent_capability_refs` | `top_level` / 无 |
| `priority` | `P0` |
| `business_outcome` | 正常工作显著更短、更快、更安静，异步等待、压缩或恢复后仍优先消费最新用户意图且不中断当前工作 |
| `value_chain` | 最小必要读取/判断 -> 紧凑交互 -> 阶段 evidence 卸载 -> 增量 wait/compression/resume -> 最新意图消费 -> current owner 继续 |
| `difficulty_focus` | 减少重复 semantic work 和上下文注入，同时保持证据充分、freshness、最新意图和当前 owner 连续性 |
| `complexity_source` | model/tool 往返、长输出、异步等待、context compression、跨平台对话/工具运行约束 |
| `design_focus` | 正常路径 action/consumer 边界、必要 evidence 生命周期、对话/工具增量协议、最新意图优先级和恢复所需最小信息 |
| `design_expansion_requirement` | 展开可删除/必须保留的信息与动作、长运行增量结果、override/additive 意图顺序、quiet update 和诊断观测方法；不得把诊断数值升级为验收门槛；terminal delivery correctness 由 `EVO-CAP-001` 承接，RDT/Architecture 证据充分性分别由 `EVO-CAP-002`、`EVO-CAP-003` 承接 |
| `risk_if_missed` | 流程形式正确但实际无法高效完成，压缩/等待后失联，用户被内部状态淹没 |
| `success_metrics` | 在同一个 exact-candidate Release gate 证据采集时间窗内，以 `EVO-FIX-PLAN-NORMAL`、`EVO-FIX-FULL-NORMAL`、`EVO-FIX-HISTORY-RESUME`、`EVO-FIX-LATEST-INTENT`、`EVO-FIX-LONG-OUTPUT` 各至少 1 条 exact trace 为样本；无 consumer 的中间文件、重复注入 unchanged authority/cumulative stdout、invalid wait、未消费最新用户意图均为 0，且每项保留的 handoff、脚本运行、文档重读和重复 gate 都能指向不可替代的直接 consumer 或 correctness 责任。不以相对 baseline 的耗时、rounds、bytes 或 compression 数值作为 PASS/FAIL 条件 |
| `failure_impact` | 本轮“显著更短、更快、更安静”和执行连续性目标失败 |
| `acceptance_bar` | normal planning 与 request-to-cleanup 路径不存在无消费者交接、重复 unchanged 正文/累计输出注入或无责任归属的脚本/gate；功能、Architecture、review 与 delivery 的证据充分性不因路径精简而降级 |
| `validation_strategy` | 对 `EVO-FIX-PLAN-NORMAL`、`EVO-FIX-FULL-NORMAL`、`EVO-FIX-HISTORY-RESUME`、`EVO-FIX-LATEST-INTENT`、`EVO-FIX-LONG-OUTPUT` 与声明平台等价运行执行 action/consumer trace；识别可删除交接、重复读取、重复判断、不必要脚本/验证和累计输出，不设置相对性能改善门槛 |
| `source_req_refs` | `REQ-UC-EVO-017..018,030..033` |
| `evidence_refs` | `EVO-EVD-001,EVO-EVD-002,EVO-EVD-003,EVO-EVD-007,EVO-EVD-008` |
| `priority_score` | 业务影响 5 / 系统复杂度 5 / 失败成本 5，总分 15 |
| `priority_rationale` | 当前诊断已证明成本和连续性会直接阻止交付完成，而非仅影响体验 |
| `counterfactual_check` | 不能延期；若只重排 owner 而不降低成本和断链，目标产品仍未完成 |
| `confirmation_status` | `user_confirmed_with_edits` |
| `open_questions` | 无 |

### 1.6 场景编号与入口追踪

本产品范围无独立 UI 页面、无服务端 API contract，也不新增或改变用户 CLI command
contract。Shared/Codex/Claude/Cursor 的 prompt/command/Skill 入口属于同一个 conversational
workflow product entry；既有 Trellis CLI 与 companion script 是后续设计可能使用的运行面，
不是本 Requirements 新定义的 CLI intent。

| 场景范围 | 入口类型 | API intent | CLI intent | 非功能主定义 |
| --- | --- | --- | --- | --- |
| `REQ-UC-EVO-001..043` | conversational workflow（Shared/Codex/Claude/Cursor） | 正常不映射：无服务端 API contract | 正常不映射：本轮不新增/改变用户 CLI contract | [`requirement-non-functional.md`](./requirement-non-functional.md) |

编号差集：API intent 为空、CLI intent 为空，均属于整体不适用，不是
`UC-接口映射豁免`；真实豁免 0，缺失映射 0。

## 2. 入口组织结构

页面组织不适用。目标入口按用户意图组织，而不是按平台复制流程：

| 入口 | 承接场景 | 摘要 |
| --- | --- | --- |
| 标准 change workflow | `REQ-UC-EVO-001..004,006..030,039..043` | 承接需要正式 task lifecycle 的产品与工程 change |
| task-free workflow | `REQ-UC-EVO-005` | 承接有界的 current-checkout change |
| resume/recovery entry | `REQ-UC-EVO-006,015..016,020..021,027,030..032` | 承接中断、恢复和 current facts 变化后的继续执行 |
| distribution/release entry | `REQ-UC-EVO-034..036` | 承接平台、安装、升级和 exact-candidate Release 验证 |
| explicit specialist review entry | `REQ-UC-EVO-037..038` | 承接显式、有界的 specialist review 请求 |

Shared/Codex/Claude/Cursor 是同一个 conversational workflow 的入口投影。入口的可执行规则
统一由[第 3 章](#3-功能需求)定义，route、re-entry 与 stop 统一由[第 6 章](#6-必需状态闭环)定义。

## 3. 功能需求

### 3.1 Authority、Intake 与 Workspace

- `EVO-REQ-001`：target Requirements 与 current runtime authority 必须明确分离；任何
  未实现目标不得被 current 文档、状态或发布说明冒充为已实现。
- `EVO-REQ-002`：Intake 必须读取当前用户请求、live Issue 正文/必要评论、parent repository
  current Requirements/Design/Test 及其适用的 authoring/review/lifecycle contract，以及完成
  requirement 判断所需的 Git/GitHub/Trellis live facts；不得把 task planning、旧会话摘要、候选
  Issue body 或 submodule 内容当作 parent repository current RDT authority，也不得在 Phase 0 提前
  执行 Architecture impact/alignment。current Architecture 的实质消费属于 pre-design Planning。
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
- `EVO-REQ-010`：进入标准 workflow、task-free workflow、resume/recovery 或停止，必须先由
  当前请求和完成分流所需的最小 live facts 唯一决定；在 `mode_selected` 前不得开展方案性
  repository/domain semantic work、生成 task/planning 产物或执行 Git/GitHub/Trellis/submodule
  副作用。只有真实产品选择或即将发生的 Git/GitHub/Trellis
  副作用才询问用户。task-free 只保留 invocation-local 的最小意图与检查结果，不生成正式
  `prd.md`、`design.md`、`implement.md` 或 task/archive history；范围不再有界时返回 standard
  workflow，并在任何标准资源副作用前取得精确确认。
- `EVO-REQ-011`：Workspace/task/branch 等资源只在 requirement readiness 成立且用户已
  确认精确副作用后创建；task/branch/worktree 名称必须绑定可用的 current change identity
  与语义动作，无 Issue 时不得伪造 Issue identity；资源准备不得反向拥有或重写 Intake 语义，
  也不得把 submodule init/update/checkout 或递归读取伪装成 parent task 的普通准备动作。
- `EVO-REQ-059`：standard change 在创建资源前必须判断它是否为一个可独立交付单元，并基于
  live Issue/current/相关 archived change authority 处理 duplicate、linked prerequisite、scope
  overlap 与 readiness；该结果只路由到复用/澄清/阻塞/继续，不重复拥有 requirement
  authoring 或 Workspace 创建。
- `EVO-REQ-060`：selected base/current authority 在 pre-task 读取前必须按 exact upstream
  identity 安全刷新；刷新不得修改 invocation checkout、创建临时 task worktree、重选低优先级
  base 或执行 reset/rebase/stash/force update，无法安全刷新时明确 blocked。
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
- `EVO-REQ-026`：freshness 必须按语义依赖传播：实质 scope/authority 变化只失效最早受影响
  结果及下游；locator-only 或经证明等价的重发布只更新 identity/freshness，不重放完整
  semantic review；技术机制变化不失效未改变的 product requirement。

### 3.3 Implementation、Check、Review 与 Promotion

- `EVO-REQ-027`：Implementation 必须消费 current approved plan、current repository RDT binding、
  task-local RDT contribution/alignment、适用 Architecture alignment 和必要 live facts；不得依赖
  planning author 的 private review transcript，也不得从 task planning artifacts 反推 shared RDT。
- `EVO-REQ-028`：Phase 2 必须对当前 task scope、实现、测试、repository RDT satisfaction/
  contribution、Architecture change contract 和未验证边界完成一次完整 semantic check；若输入
  unchanged，不得叠加重复
  reviewer 证明同一充分性。
- `EVO-REQ-029`：finding 修订后只重做其语义依赖的实现、验证和 gate；每次新的 pass 必须
  绑定 current candidate，旧 pass 不能被复用为 current。
- `EVO-REQ-030`：Branch Review 必须独立读取 exact committed `origin/<base>...HEAD` full
  diff、current repository RDT/task-local contribution/Architecture authority 与测试结果；工作树
  片段、旧 Phase 2 或未提交内容不能冒充 full-diff review。
- `EVO-REQ-031`：Architecture promotion 改变 shared current 后，原 candidate 必须重做
  受影响的 Architecture satisfaction、Phase 2、Task Commit 和 Branch Review，不得仅更新
  locator 后继续。
- `EVO-REQ-032`：base 演进必须按实际 diff 与语义依赖判断 no-impact/revision/recovery；
  不得从 Phase 0 重建已有 task，也不得因无关 base movement 全链失效。
- `EVO-REQ-033`：并行 task 必须隔离各自 task/workspace/branch/contribution；shared authority
  promotion 之后，绑定旧 identity 的 task 必须重算影响，不能形成双 current 或双 writer。
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
- `EVO-REQ-034`：每个阶段结果必须恰好具有一个下一 owner、一个明确 re-entry 或一个 terminal
  stop；unknown、multiple、unmapped 或无 consumer 的结果必须停止，Agent 不得猜测路线。

### 3.4 Publication、Delivery、Finish 与 History

- `EVO-REQ-035`：PR readiness 必须从 current repository RDT/task contribution、current plan、
  exact committed diff、验证、Architecture 状态以及 live GitHub facts 形成；标题/正文、部署/
  安全影响和未验证边界必须真实具体。
- `EVO-REQ-036`：Issue closure 语义必须由 current Issue、accepted requirement scope、exact
  reviewed diff 和 live delivery facts 判断；不得恢复 Issue Scope Ledger 或以
  `close_issues/related_issues/followup_issues` aggregate 作为 current authority。
- `EVO-REQ-037`：`github_pr` route 必须覆盖 push、PR publication、expected-head delivery、
  merge 与 Issue closure 的 current 状态；每个不可逆副作用只执行一次并具有 forward recovery。
- `EVO-REQ-038`：`none` route 必须保持完整本地 acceptance/Finish/history/cleanup 能力，且不
  调用 GitHub、不伪造 PR 或 Issue identity。
- `EVO-REQ-039`：正常 provider failure、认证缺失、远端状态变化或部分成功必须返回拥有该
  外部动作的 delivery boundary；保留 current 成果，不重跑无关 Planning/Implementation。
- `EVO-REQ-040`：Acceptance、Publication、Delivery、Merge、Issue closure、Finish 和 Cleanup
  的 semantic responsibility 必须唯一且顺序完整；同一事实不得在相邻阶段重复审批。
- `EVO-REQ-041`：远端不可逆副作用开始后，任何失败都只能 forward recover 或 terminal
  block，不得回到需求、Planning 或实现修订；若产品 scope 真正改变，必须先明确停止当前
  delivery，再启动新的 change lifecycle。
- `EVO-REQ-042`：Finish 只执行可机器判定的最终状态收敛；Cleanup 只删除 exact owned
  resource，并在删除前后证明需要保留的 commit/ref/history 可达性。
- `EVO-REQ-043`：任务历史只保留恢复、查询或 release 直接消费且无法从 live facts 重建的
  最小 durable result；不得保留用户授权、完整 stdout、逐轮审查、临时 locator 或重复摘要。
- `EVO-REQ-063`：从 Implementation 到 Phase 2、Branch Review、PR readiness 或 `none` route
  对应的 local acceptance readiness、pre-delivery Acceptance，各语义责任边界必须消费或验证其
  判断所依赖的 current Architecture alignment、proposal/promotion 状态和 shared-current binding；
  identity unchanged 或经证明等价时不重复语义审核，material stale/change 时返回最早受影响 owner
  并重算下游。Finish 与 Cleanup 只确定性验证或消费已经收敛且 current 的 terminal Architecture
  lifecycle 状态，不重新拥有 Architecture 判断。

### 3.5 低成本执行与对话连续性

- `EVO-REQ-044`：正常路径不得创建 planning handoff、Architecture report、Issue ledger、
  shared cache、continuation capsule、临时交接文档或没有直接 consumer 的 gate artifact。
- `EVO-REQ-045`：跨阶段只传递下一 owner 无法从 current authority/live facts 重建的最小
  信息；producer-private evidence 在 consumer 完成后卸载，consumer 不得读取 producer 的
  private result、digest 或 recorder internal state。
- `EVO-REQ-046`：阶段完成或上下文接近限制时，必须卸载原始 scan/stdout/重复正文，只保留
  current authority locator/identity、未解决问题、当前阶段和继续所需最小事实；不得用长篇
  handoff summary 替代下一 owner 的 current reread。
- `EVO-REQ-047`：compression/resume 必须优先恢复并消费最新用户意图、当前副作用状态和
  未完成 terminal action；旧请求若被覆盖必须停止，追加请求必须合并承接。
- `EVO-REQ-048`：长运行命令/Agent 的每次 wait 只返回新输出或紧凑最终结果，必须复用有效
  handle；不得轮询不存在的 handle、重复注入累计 stdout 或把无关大对象/base64 注入上下文。
- `EVO-REQ-049`：用户可见消息只服务真实选择、实质 finding/block、需要跨响应继续的长运行等待、
  阶段结果和副作用确认；正常内部读取、projection、recorder、validator 与 locator 搬运保持安静。
- `EVO-REQ-050`：支持的正常 fixture 中，invalid wait、影响决策的输出截断、未消费用户意图、
  重复全文注入、continuation capsule 和无消费者中间文件必须为 0。

### 3.6 能力保留、分发、迁移与 Release

- `EVO-REQ-051`：AI 继续独占 intent、scope、sufficiency、conflict、finding、revision、route、
  PR readiness 与 Architecture judgment；脚本只执行副作用或记录/校验确定性事实。
- `EVO-REQ-052`：Shared、Codex、Claude、Cursor 必须消费同一 semantic contract；platform
  launcher/prompt/command 只加载和路由，不复制 step-local behavior。
- `EVO-REQ-053`：canonical source 是唯一长期分发源；dogfood、installed、preset、
  apply/reapply/update 必须投影同一新合同、managed path、mode 和 capability inventory，任何
  未处理 drift/sidecar/`.new`/`.bak` 都阻塞一致性声明。
- `EVO-REQ-054`：重构可破坏旧 Guru workflow API，但不得保留兼容层；existing repository
  必须有一次明确、可验证的迁移路径，迁移后旧 route/schema/artifact 不再被生产或消费。
- `EVO-REQ-055`：不得丢失
  [`current-capability-inventory.md`](./current-capability-inventory.md) 中分类为
  `preserved_current` 或 `replaced_contract_shape` 的 current 用户能力；保留的是可观察结果和
  正常场景，不是 current Skill 数量、名称、handoff shape、Issue 顺序或文件布局。该 inventory
  只做 current-to-target 追踪；target 行为仍以本文件 `EVO-REQ-*` 为唯一主定义，验收以对应
  fixture 为准。
- `EVO-REQ-056`：只有同一个 exact candidate 同时通过本文件的功能、Architecture、执行成本治理、
  continuity、platform/install/update 和 post-publish fixtures，才能称进化完成并进入 Release；
  执行成本治理只验证精简策略与 correctness 不降级，不比较相对性能数值。
- `EVO-REQ-057`：显式 contract wording review 必须保持可独立调用、scope-bounded、
  semantic finding/revision/return-to-caller 闭环；除非文字本身是 change scope，不得成为
  normal Planning 的 mandatory reviewer。
- `EVO-REQ-058`：normal-scenario qualification 只在唯一 caller 的 current authority 明确要求
  时执行，并将 current 结论返回该 caller；明确 requirement 直接派生的普通场景不得例行调用。

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

| Fixture | 覆盖 | 必须证明 |
| --- | --- | --- |
| `EVO-FIX-INTAKE-CLEAR` | `REQ-UC-EVO-001` | 清晰 Issue 零问题进入 requirement ready |
| `EVO-FIX-INTAKE-REVIEWED-DESIGN` | `REQ-UC-EVO-002,014` | reviewed design 被保留并与 current Architecture reconciliation，不被重写或忽略 |
| `EVO-FIX-INTAKE-UNCLEAR` | `REQ-UC-EVO-003` | 每轮一个最高价值问题，直到 ready；无问题批量轰炸 |
| `EVO-FIX-NO-ISSUE` | `REQ-UC-EVO-004` | 无 Issue 的 standard change 不伪造 Issue identity；从请求经 requirement/change readiness、精确资源副作用确认、Workspace/Planning、实现/检查/提交/full-diff review、Publication/Delivery、Finish/Cleanup 到 normal completion，PR/closure 文案不虚构 Issue，且全程无断链 |
| `EVO-FIX-TASK-FREE` | `REQ-UC-EVO-005` | 不创建 Issue/task/worktree、三份 planning 文档或 task/archive history；直接消费 invocation-local current intent，完成适用 check 和 concise terminal result，只有存在真实产品选择或副作用时才询问；scope evolution 返回 standard route 且不重复已明确意图 |
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
| `EVO-FIX-PLAN-NORMAL` | `REQ-UC-EVO-001,002,009,017,018,033,042` | clear Issue + reviewed design + current aligned RDT/Architecture 从请求进入到 `plan_ready`；mode selection 前无方案性 repository work/副作用；RDT 前置回读和 impact 先于 task planning；三份 task 文件仅含 current locator/适用引用与 task-local delta；一次 authoring、一次 evidence-backed approval、零 routine clarification |
| `EVO-FIX-BRANCH-FINDING` | `REQ-UC-EVO-020,022` | finding 修订后 fresh check/commit/full-diff review 闭环 |
| `EVO-FIX-BASE-EVOLUTION` | `REQ-UC-EVO-021` | 无关 base delta 不全链失效；相关 delta 返回最早受影响 owner且不重建 task |
| `EVO-FIX-ARCH-PROMOTION` | `REQ-UC-EVO-023` | serialized promotion 后 fresh Phase 2/commit/review |
| `EVO-FIX-ARCH-DOWNSTREAM-FRESHNESS` | `REQ-UC-EVO-019,022..023,025..026,028..029` | 在 `github_pr` 与 `none` 两种 route 中，current Architecture binding 从 Implementation 经 Phase 2、full-diff review、对应 publication/local acceptance readiness、Acceptance 到 Finish 均可追踪；在各下游责任边界注入正常 identity-equivalent 与 material authority change，前者不重复语义审核，后者返回最早受影响 owner，任何 gate 不消费 stale binding；Cleanup 不重新判断 Architecture |
| `EVO-FIX-RDT-DOWNSTREAM-FRESHNESS` | `REQ-UC-EVO-019..020,022,025..026,028..029,042` | current RDT binding/impact/contribution 从 Planning 经 Implementation、Phase 2、full-diff review、两种 delivery readiness、Acceptance 到 Finish 可追踪；Implementation discovery 会及时回写 task-local contribution；等价 identity 不重审全文，material RDT change 返回最早受影响 owner，任何 gate 不消费 stale RDT，Cleanup 不重新判断 RDT |
| `EVO-FIX-PARALLEL` | `REQ-UC-EVO-024` | 两 task 隔离，promotion 后旧 identity 正确失效 |
| `EVO-FIX-FULL-NORMAL` | `REQ-UC-EVO-001,009,018..019,022,025,028..029,033,042..043` | 固定小变更从 request 经 Mode/Intake、Base/Context、Workspace、RDT/Architecture-aware Planning、实现/检查/提交/full-diff review、Publication/Delivery、Finish/Cleanup 到 normal completion，无断链；mode 前无方案性 work/副作用，task/branch/worktree 名称绑定 current change identity 与语义动作，RDT authority/task contribution 全程 current，执行与 Phase 2 包含 scope-relevant targeted validation，存在无关异常 submodule 时仍零 submodule action/block |
| `EVO-FIX-NONE` | `REQ-UC-EVO-026` | GitHub 调用为 0，仍完整 Finish/history/cleanup |
| `EVO-FIX-PROVIDER-RECOVERY` | `REQ-UC-EVO-027` | partial external success 只 forward recover，不重复副作用或返回早期 phase |
| `EVO-FIX-HISTORY-RESUME` | `REQ-UC-EVO-029..030` | session restart 与 archive query 只消费 current/live/minimal durable result，不依赖授权、stdout 或长 handoff |
| `EVO-FIX-LATEST-INTENT` | `REQ-UC-EVO-030..031` | 分别在 Phase 2 后、长运行 wait 中和 compression/resume 前后注入 override/additive 指令；下一响应必须先消费最新意图，override 停止未发生副作用的旧路线，additive 与未完成请求按到达顺序合并，旧目标不得在恢复后抢先执行 |
| `EVO-FIX-LONG-OUTPUT` | `REQ-UC-EVO-032` | 多次 wait 只返回 delta，invalid handle 与累计 stdout 重注入为 0 |
| `EVO-FIX-PROJECTION` | `REQ-UC-EVO-034` | Shared/Codex/Claude/Cursor + canonical/dogfood/installed/preset 语义一致且只含新合同；target draft 在 current runtime、安装结果和发布说明中均不得被声明为 current/implemented |
| `EVO-FIX-MIGRATION` | `REQ-UC-EVO-035` | clean 与 existing official update/upgrade/reapply 后完整新能力、无旧 route/artifact consumer |
| `EVO-FIX-RELEASE` | `REQ-UC-EVO-036` | exact-candidate 全矩阵和 post-publish smoke；局部 PASS 不可相加冒充 release PASS |
| `EVO-FIX-WORDING-EXPLICIT` | `REQ-UC-EVO-037` | 显式有界 wording review 可独立完成并返回 caller；normal plan 调用数为 0 |
| `EVO-FIX-QUALIFY-EXPLICIT` | `REQ-UC-EVO-017,038` | 明确 caller 请求时 qualification 可用；普通直接派生 acceptance 场景调用数为 0 |
| `EVO-FIX-CHANGE-REQUEST` | `REQ-UC-EVO-039` | ready、duplicate、linked-prerequisite blocked 与 scope clarification 都有唯一结果，且不写资源或重复 authoring |
| `EVO-FIX-BASE-REFRESH` | `REQ-UC-EVO-040` | behind authority 按 exact upstream 前进；detached/dirty invocation 不变；ambiguous/unsafe refresh 明确 blocked |
| `EVO-FIX-SSOT-BOOTSTRAP` | `REQ-UC-EVO-041` | new、partial、stale 和 conflicting repository authority 建立唯一 current 或明确 blocked，不把 inferred 内容冒充 current |
| `EVO-FIX-RDT-LIFECYCLE` | `REQ-UC-EVO-042` | 对同一 current RDT 分别注入真实 no-impact、正常 aligned、明确 RDT delta、missing/stale/conflicting authority 和错误 `no_docs_update_needed/docs_ssot=true`；前三者只能得到与证据相符的 impact，错误 false-no-impact 必须阻塞 approval；isolated contribution、Implementation 中间回写、review revision、expected-current conflict、serialized promotion、promotion 后受影响 evidence 重验与并行隔离全部保持 RDT 追踪和唯一 shared current；task planning 不得冒充 RDT |
| `EVO-FIX-SUBMODULE-BOUNDARY` | `REQ-UC-EVO-043` | parent repo 同时放置 uninitialized、dirty、detached、不可访问或命令失败的无关 submodule；standard 与 task-free/resume 各自执行时，submodule init/update/checkout/sync/递归 scan/read/write/test 调用均为 0，parent authority/readiness/result 不变；显式 submodule change 则进入该 repository 的独立 workflow，不把其 RDT 合并为 parent current |

### 5.2 执行成本约束与优化证据

- 流程耗时、model/tool rounds、injected bytes、automatic context compression 次数以及相对
  current baseline 的改善比例只可作为诊断和设计优化证据，不作为 Requirements、candidate 或
  Release 的 PASS/FAIL 门槛。
- `EVO-FIX-PLAN-NORMAL` 与 `EVO-FIX-FULL-NORMAL` 必须先完整证明功能、Architecture、review、
  delivery 和 evidence sufficiency；不得通过删减能力、隐藏失败或跳过 gate 获得更短路径。
- 每个跨阶段 handoff、持久 artifact、文档重读、脚本运行、validator、semantic gate 和用户可见
  update 都必须能够指出不可替代的直接 consumer、fresh live fact 或 correctness responsibility；
  无法指出者必须从正常路径删除。
- unchanged authority 正文、累计 stdout、完整 scan/review history 和 producer-private evidence
  不得跨阶段重复注入；下一 owner 只读取完成当前判断所需的 current locator、必要片段、delta 和
  无法重建的最小结果。
- 长运行过程只复用有效 handle 并返回新增输出；阶段完成后卸载无后续 consumer 的 private
  evidence。确需恢复时以 current authority/live facts 为主，不制造长篇中间交接文档。
- `continuation capsule` 是由 Guru workflow/Agent/tool 生成或持久化、主要用于在 context
  compression、session resume 或 owner 边界后继续同一工作的一份额外状态摘要。正常 authoritative
  planning 文档、当前对话中的简短阶段结果、平台内部不可见的 compression state 和 live reread
  不属于 capsule；正常路径不应为恢复便利主动制造 capsule。
- `EVO-EVD-002` 继续作为识别重复读取、无效 wait、累计输出、无消费者 locator 和最新意图丢失
  等问题的诊断样本，不作为性能 baseline 或 target 数值来源。

## 6. 必需状态闭环

正常生命周期只定义产品阶段结果，不预先决定 Skill 拆分、typed exit、DTO 或文件布局。
入口先按产品边界分流：

```text
request_received
-> mode_selected
   |-> task_free_ready
   |   -> task_free_change_checked
   |   -> task_free_finished
   |   -> workflow_completed
   |
   `-> standard_request
       -> base_current
       -> repository_authority_current
       -> requirement_ready
       -> change_request_ready
       -> workspace_ready
       -> rdt_alignment_current
       -> architecture_alignment_current
       -> plan_ready
       -> implementation_checked
       -> task_committed
       -> branch_reviewed
       -> [存在 Architecture/RDT contribution 时：
           contribution_reviewed
           -> shared_current_promoted
           -> affected_authority_reconciled
           -> affected implementation/check/commit/full-diff review 重算
           -> branch_reviewed]
       -> publication_ready
       -> pre_delivery_accepted
       -> delivered
       -> merged_or_none_terminal
       -> finished
       -> owned_resources_cleaned
       -> workflow_completed
```

`task_free_finished` 只返回本次 invocation 的 concise result，不产生 standard task 的 planning、
archive、publication 或 cleanup resource。任一 Architecture 或 RDT promotion 都只推进其唯一
shared current；多个 contribution 分别独立 review、按 expected current identity 串行 promotion。
promotion 后只重算语义依赖受影响的结果，其中 Architecture promotion 至少重做 fresh Phase 2、
Task Commit 与 committed full-diff Branch Review。

必须覆盖以下回程/停止语义：

| 变化/失败 | 最早合法回程或终点 |
| --- | --- |
| task-free scope 保持有界 | `task_free_change_checked -> task_free_finished -> workflow_completed`；不进入正式 Plan/task lifecycle |
| task-free scope 实质扩大 | 保留 current intent，返回 `standard_request`；标准资源副作用前重新确认 exact plan |
| duplicate/已有等价 change 可复用 | 返回 current change authority 或已存在 task；不创建重复资源 |
| linked prerequisite 未满足/不可独立交付 | pre-resource blocked；prerequisite current 后重入 change-request readiness |
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
| provider/remote failure | delivery owner forward recovery 或 blocked |
| irreversible remote side effect 后失败 | 只允许 forward recovery/terminal block |
| user 覆盖当前请求 | 停止尚未发生副作用的旧路线，优先承接最新意图 |
| mandatory capability/route 缺失或 ambiguous | fail closed；不得猜测下一步 |

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
- 没有真实选择时不提问，不向用户展示内部 artifact 搬运。
- 正常路径尽最大可能减少重复 semantic work、中间交接、上下文堆积、全文重读、不必要脚本和
  重复验证；是否满足由 action/consumer 与 correctness trace 证明，不以相对性能比例作为发布门槛。

### `EVO-006` 从请求进入到资源清理形成完整闭环

- normal、revision、refresh、recovery、blocked、no-Issue、`github_pr` 和 `none` 路径都有唯一
  回程或终点，不依赖 Agent 猜测。
- 不可逆远程副作用后只 forward recover，不返回早期产品阶段。

### `EVO-007` 所有交付形态保持同一能力

- Shared、Codex、Claude、Cursor 以及 canonical、dogfood、installed、preset、update/reapply
  使用同一新合同。
- exact-candidate Release 证明完整 business runtime、Architecture lifecycle、执行成本治理、平台/
  install/update matrix 和 post-publish smoke；相对性能观测不成为发布门槛。

## 8. 目标追踪

### 8.1 场景到需求追踪

| 场景 | 功能需求 | 非功能主定义/验收 |
| --- | --- | --- |
| `REQ-UC-EVO-001..007,039..041,043` | `EVO-REQ-002..011,059..061,066` | `EVO-NFR-009..010,016..018`；对应 `EVO-FIX-INTAKE-CLEAR`, `EVO-FIX-INTAKE-REVIEWED-DESIGN`, `EVO-FIX-INTAKE-UNCLEAR`, `EVO-FIX-NO-ISSUE`, `EVO-FIX-TASK-FREE`, `EVO-FIX-TECH-REVISION`, `EVO-FIX-DETACHED-READ`, `EVO-FIX-CHANGE-REQUEST`, `EVO-FIX-BASE-REFRESH`, `EVO-FIX-SSOT-BOOTSTRAP`, `EVO-FIX-SUBMODULE-BOUNDARY` |
| `REQ-UC-EVO-008..018` | `EVO-REQ-012..026` | `EVO-NFR-007,014..015`；对应 `EVO-FIX-ARCH-NO-IMPACT`, `EVO-FIX-ARCH-ALIGNED`, `EVO-FIX-ARCH-CONFLICT`, `EVO-FIX-ARCH-INCOMPLETE`, `EVO-FIX-ARCH-NEW-DECISION`, `EVO-FIX-ARCH-REVISION`, `EVO-FIX-ARCH-NO-ADR`, `EVO-FIX-FRESH-EQUIVALENT`, `EVO-FIX-FRESH-SCOPE`, `EVO-FIX-TECH-REVISION`, `EVO-FIX-PLAN-NORMAL` |
| `REQ-UC-EVO-019..024,042` | `EVO-REQ-027..034,062..065` | `EVO-NFR-009..011,015`；对应 `EVO-FIX-BRANCH-FINDING`, `EVO-FIX-BASE-EVOLUTION`, `EVO-FIX-ARCH-PROMOTION`, `EVO-FIX-ARCH-DOWNSTREAM-FRESHNESS`, `EVO-FIX-RDT-DOWNSTREAM-FRESHNESS`, `EVO-FIX-PARALLEL`, `EVO-FIX-RDT-LIFECYCLE` |
| `REQ-UC-EVO-025..030` | `EVO-REQ-035..043,046..047,063,065` | `EVO-NFR-009..011,016..017`；对应 `EVO-FIX-FULL-NORMAL`, `EVO-FIX-NONE`, `EVO-FIX-PROVIDER-RECOVERY`, `EVO-FIX-HISTORY-RESUME`, `EVO-FIX-LATEST-INTENT`, `EVO-FIX-ARCH-DOWNSTREAM-FRESHNESS`, `EVO-FIX-RDT-DOWNSTREAM-FRESHNESS` |
| `REQ-UC-EVO-031..033` | `EVO-REQ-044..050` | `EVO-NFR-001..010`；对应 `EVO-FIX-PLAN-NORMAL`, `EVO-FIX-LATEST-INTENT`, `EVO-FIX-LONG-OUTPUT` |
| `REQ-UC-EVO-034..036` | `EVO-REQ-001,051..056` | `EVO-NFR-012..017`；对应 `EVO-FIX-PROJECTION`, `EVO-FIX-MIGRATION`, `EVO-FIX-RELEASE`；必须证明 target/current authority 分离 |
| `REQ-UC-EVO-037..038` | `EVO-REQ-057..058` | `EVO-NFR-014..015`；对应 `EVO-FIX-WORDING-EXPLICIT`, `EVO-FIX-QUALIFY-EXPLICIT` |

### 8.2 Goal 追踪

| Goal | 场景 | 功能需求 | 非功能/验收 |
| --- | --- | --- | --- |
| `EVO-001` | `REQ-UC-EVO-001..007,014,039..043` | `EVO-REQ-002..011,021..022,059..062,064,066` | `EVO-FIX-INTAKE-CLEAR`, `EVO-FIX-INTAKE-REVIEWED-DESIGN`, `EVO-FIX-INTAKE-UNCLEAR`, `EVO-FIX-NO-ISSUE`, `EVO-FIX-TASK-FREE`, `EVO-FIX-TECH-REVISION`, `EVO-FIX-DETACHED-READ`, `EVO-FIX-CHANGE-REQUEST`, `EVO-FIX-BASE-REFRESH`, `EVO-FIX-SSOT-BOOTSTRAP`, `EVO-FIX-RDT-LIFECYCLE`, `EVO-FIX-SUBMODULE-BOUNDARY` |
| `EVO-002` | `REQ-UC-EVO-008..016,019,022..026,028..029` | `EVO-REQ-013..020,026..031,033,035,040,063` | `EVO-CAP-003`, `EVO-FIX-ARCH-NO-IMPACT`, `EVO-FIX-ARCH-ALIGNED`, `EVO-FIX-ARCH-CONFLICT`, `EVO-FIX-ARCH-INCOMPLETE`, `EVO-FIX-ARCH-NEW-DECISION`, `EVO-FIX-ARCH-REVISION`, `EVO-FIX-ARCH-NO-ADR`, `EVO-FIX-FRESH-EQUIVALENT`, `EVO-FIX-FRESH-SCOPE`, `EVO-FIX-ARCH-DOWNSTREAM-FRESHNESS`, `EVO-FIX-ARCH-PROMOTION`, `EVO-FIX-PARALLEL` |
| `EVO-003` | `REQ-UC-EVO-006..007,015..016,019..030,040..043` | `EVO-REQ-001,007..009,026..043,045..047,060..066` | `EVO-CAP-001,EVO-CAP-002`, `EVO-NFR-007,009..011,015,018`, `EVO-FIX-BASE-REFRESH`, `EVO-FIX-SSOT-BOOTSTRAP`, `EVO-FIX-RDT-LIFECYCLE`, `EVO-FIX-RDT-DOWNSTREAM-FRESHNESS`, `EVO-FIX-SUBMODULE-BOUNDARY` |
| `EVO-004` | `REQ-UC-EVO-001..043` | `EVO-REQ-010..012,024..025,027..028,034,040,051,057..066` | `EVO-NFR-007,014..015`, `EVO-FIX-WORDING-EXPLICIT`, `EVO-FIX-QUALIFY-EXPLICIT`, `EVO-FIX-CHANGE-REQUEST` |
| `EVO-005` | `REQ-UC-EVO-017..018,030..033` | `EVO-REQ-023..026,044..050` | `EVO-CAP-004`, `EVO-NFR-001..009`, `EVO-FIX-PLAN-NORMAL`, `EVO-FIX-HISTORY-RESUME`, `EVO-FIX-LATEST-INTENT`, `EVO-FIX-LONG-OUTPUT` |
| `EVO-006` | `REQ-UC-EVO-019..033,042..043` | `EVO-REQ-027..050,062,065..066` | `EVO-CAP-001..004`, `EVO-FIX-FULL-NORMAL`, `EVO-FIX-NONE`, `EVO-FIX-PROVIDER-RECOVERY`, `EVO-FIX-RDT-DOWNSTREAM-FRESHNESS`, `EVO-FIX-SUBMODULE-BOUNDARY` |
| `EVO-007` | `REQ-UC-EVO-034..036` | `EVO-REQ-052..056` | `EVO-CAP-001..004`, `EVO-NFR-012..015`, `EVO-FIX-PROJECTION`, `EVO-FIX-MIGRATION`, `EVO-FIX-RELEASE` |

Design/Test/Architecture mapping 尚未建立是当前阶段的有意边界，不是缺失追踪。它只能在本
Requirements 审核通过后由新的 Evolution Design/Test/Architecture contribution 建立。

## 9. 非目标

- 不在本阶段选择、重写或修订现有 Issue 链，也不创建新的 Issue、task、worktree、branch、
  PR 或 Release。
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

本 Requirements 已完成修订后的 fresh 全稿审核，当前仍待用户单独批准进入 Design。完整放行
条件依次为：

1. `EVO-NFR-001..008` 已按 `EVO-EVD-007` 收敛为执行成本与上下文治理约束，不包含相对 baseline
   的耗时、rounds、bytes、compression 或改善比例 Release 门槛；
2. `EVO-CAP-001..004` 的核心能力收敛结果具有用户确认；当前由确认四项独立 `P0` 的
   `EVO-EVD-010` 与收敛执行成本验收口径的 `EVO-EVD-007` 共同满足；
3. [`current-capability-inventory.md`](./current-capability-inventory.md) 的 completion contract
   全部满足：`.40` previous Skill、current Requirements/Behavior/NFR/Test capability 孤儿项为 0，
   每个 retained capability 均有 target requirement 与 fixture successor；
4. 完成一次 fresh、独立 Requirements 全稿审核，未解决 `P1` 与阻断性 `P2` finding 均为 0；非阻断性 `P2` 必须具有不改变范围、验收或设计承接的明确假设；
5. 重复主定义为 0，API/CLI 差集无缺失，非功能豁免完整；
6. 用户明确批准进入 Evolution Design。

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
> 全程不依赖冗余交接文件，也不会在阶段之间丢失语义或最新用户意图。

Guru Trellis 的本轮进化只有在同一个 exact candidate 上对 `EVO-001..007`、全部适用
`REQ-UC-EVO-*`、`EVO-REQ-*` 和 `EVO-NFR-*` 建立 current、可复现、无互相矛盾的端到端
证据后才算完成。单个 Skill、单个 Issue、静态 schema、历史运行或局部平台通过只能证明
对应局部结果，不能替代整体完成。
