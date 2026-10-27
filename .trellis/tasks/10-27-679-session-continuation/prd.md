# 跨会话 Task/Delivery 接续与 standalone 身份投影：整体需求

## 1. 来源与术语

Direct Source 为 [castbox/guru-trellis#679](https://github.com/castbox/guru-trellis/issues/679)，关系 exact_source。本轮读取其完整正文与零评论；下文第2、5、6、7节保留来源证据、行为条件、边界和六项验收；R4 承接同链路 Human artifacts 调用差额。

| 来源 | 章节与角色 | 本 Task 用途 |
| --- | --- | --- |
| Issue #679 | 目标与行为要求、验收与验证；要求 | R1/R2/R3/R4 与 AC1–AC6 的唯一外部来源 |
| Issue #679 | 范围与关联边界；约定设计约束 | 原 owner 复用、兼容和排除边界 |
| docs/requirements/current/task-delivery-lifecycle.md | 身份、整体责任与入口、切片建立；当前规范 | 保持 Task/Delivery 和阶段所有权 |
| docs/design/current/task-delivery-lifecycle.md | 当前生命周期职责；当前设计 | Establish/Ensure/Bind、Selection 与阶段 owner 的责任 |
| docs/requirements-design-test-contributions/548-creation-recovery/{design,test}.md | 已有方案与观察；历史/证据 | 保留 explicit-task 和既有原子能力，区分原生覆盖差额 |
| docs/requirements-design-test-contributions/396-draft-intake-recovery/{design,test}.md | producer-bound recipe 与回放；历史/证据 | 保留 proposed_draft、authority digest 与 receipt 消费 |
| AGENTS.md、.trellis/spec/workflow/clear-technical-writing.md | 当前工程约束 | Markdown 判断、脚本事实执行和清晰写作 |

Task 是整体 accepted scope；Delivery 是同 Task 内独立交付切片。context key 是原 resolver 返回的当前调用会话身份。显式 TaskId/generation/DeliveryKey 不是 session binding，也不是阶段 pass。standalone_request 是来源 profile，与 workflow/standalone 执行 mode 独立。

## 2. 背景与问题

2026-10-27，castbox/ai-chat-roleplay-backend 会话“排查生产 MongoDB 接口报错”（01a17b5d-430e-7700-be97-5ff326f0db49）及子 Agent 在创建后接续和独立架构审核中反复遇到 stale。本 Issue 修复 Guru 流程，业务 MongoDB 故障不在范围内。

北京时间：

| 调用方 | 现象 | 后续对照 |
| --- | --- | --- |
| 主会话 13:03、13:05 | Author 返回 stale_identity / delivery_key；同一调用会话的 delivery.py current 返回 no_current_task；原 Delivery 保持 planning | 经原 Bind owner 恢复主会话 Task 绑定、经原 Selection owner 选择同一 Delivery 后，13:08 Author 返回 requirements_ready |
| independent_architecture 子会话 13:13 | 收到显式 DeliveryKey 后，Architecture invoke 仍返回 stale_identity / delivery_key | 子会话恢复自身绑定并选择原 Delivery 后，13:17 返回 baseline_current / candidate_assessment |
| formal_intake 子会话 12:33 | Readiness 返回 stale_identity / target.request_id；调用方把 request_id 填为自拟任务名称，来源 draft_id 却是 producer locator | 后续把消费者 request_id 对齐真实来源 locator，继续原链路 |

取证基线 main `6b3e26b177f747fdde48b43685d8af8827e22614` 的下列四处代码，canonical、dogfood 与业务安装副本一致。2026-10-27 核对 main `e6c3b8276d62ac174ab42cba5bca4d5784be2ca3`，机制代码未变。这是历史证据，不代表修复或新原生回放；实施前重读最新版本。

固定源码：

- [DeliveryProjection.current / select](https://github.com/castbox/guru-trellis/blob/e6c3b8276d62ac174ab42cba5bca4d5784be2ca3/trellis/skills/guru-team/runtime/delivery_projection/adapter.py#L155)：区分有 context 的会话选择与无 context 的显式调用。
- [Author planning 检查](https://github.com/castbox/guru-trellis/blob/e6c3b8276d62ac174ab42cba5bca4d5784be2ca3/trellis/skills/guru-team/packages/guru-author-task-plan/runtime/invoke.py#L79)与 [Architecture planning 检查](https://github.com/castbox/guru-trellis/blob/e6c3b8276d62ac174ab42cba5bca4d5784be2ca3/trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/runtime/invoke.py#L572)：多个条件合并返回同一个 `stale_identity / delivery_key`。
- [Readiness normalize_target](https://github.com/castbox/guru-trellis/blob/e6c3b8276d62ac174ab42cba5bca4d5784be2ca3/trellis/skills/guru-team/packages/guru-review-change-request/runtime/common.py#L98)：校验 standalone 的 `request_id` 与 source `draft_id`。

历史记录解释现场；隔离回归用正常 writer/入口，不手改 session/artifact。

## 已定位的缺口

1. 显式 Task/Delivery 身份不等于会话绑定。DeliveryProjection.current(key) 仅在无 context key 时走 explicit-task；有 context 时读本会话选择。其它会话的创建/选择不会绑定接收会话。缺口在跨会话前置检查和接续，不要求继承父会话选择或取消 adapter 限制。
2. Author/Architecture planning 将缺 Task、缺选择、key 不符及 phase/generation/scope 失配合并为 stale_identity / delivery_key，错误引导阶段返工；主会话切换 Author profile 仍失败。
3. standalone_request 要求 target.request_id 等于 source.draft_id。现有可执行 recipe 只演示 proposed_draft，standalone 字段映射仍需补齐。本次错误输入被正确拒绝，不证明 normalization 错误，不预设必须修改 runtime。

## 历次修复为何没有覆盖本次现场

- #438 修复创建者 attach，#443 提供 Bind owner；均不证明父会话/新审核子会话已绑定。
- #548 补无 context 显式 key，fixture 覆盖 key/no-key transport；Codex 明确选 D1 后读 current/continuation，不证明未绑定接收会话自行恢复。
- #396 recipe 及原生恢复覆盖 proposed_draft 的 body-only digest/缺 Wording，不覆盖本次 standalone_request 身份构造；保留正确 normalization。
- 依据：`.trellis/tasks/archive/2026-09/09-19-438-session-binding-attach/design.md`、`.trellis/tasks/archive/2026-09/09-19-443-task-identity-binding/design.md`；`docs/requirements-design-test-contributions/548-creation-recovery/test.md`、`docs/requirements-design-test-contributions/396-draft-intake-recovery/test.md`。这些覆盖差额不证明旧修复整体失效或代码回退。

因果链为“交接身份但缺会话前置检查 → 缺绑定误报 stale → 错误重试”；原 Bind/Selection 恢复后同对象通过作对照。实施前核对首个缺失步骤、owner 和旧验证边界；事实变化先修正判断，不放宽校验。

## 3. 目标与非目标

整体目标是让明确同一对象的正常接收会话，经原身份和选择 owner 补齐自身缺失事实后，继续实际未完成义务；同时准确诊断首失败条件，给 standalone_request 提供真实 producer 身份投影与完整消费者恢复指引，并修复同链路 Human artifacts 文档展示调用。

本 Task 承担 R1、R2、R3、R4 和下述六项验收。整体完成要求 package、安装投影、原生 Agent 证据分别成立，再经 Delivery、Completion、Closure、Finish 与适用 Cleanup 的原门禁。交付合并不能替代整体完成。非目标和明确禁止项见第6节。

## 4. 真实调用方、场景与流程

| 场景 | 调用方与前置条件 | 触发、处理与可观察结果 |
| --- | --- | --- |
| S1 | 主会话接回子 Agent 创建结果；本会话初始未绑定，已有明确 Task/gen/key/root | 进入原阶段前检查自身 current；由原 Bind/Selection 补缺，重读后到适用 Author 正式出口，身份与规划保留 |
| S2 | 全新独立 Architecture 子会话接收明确身份；初始未绑定且未选 Delivery | 自行读取合同并按原 owner 恢复；保留 fresh reviewer 读取顺序，到适用 Architecture 正式出口 |
| S3 | 已有规划进度，绑定或选择缺失；实际前序结果仍适用 | 只补缺失事实，继续原未完成义务；不重跑初始规划，不把 phase 当批准 |
| S4 | 当前选择不同、终态、真实 phase/gen/scope 变化，或 error/损坏/不支持/歧义 | 报本次首先失败条件并交原 owner；不覆盖合法选择，不当成无绑定，不重开终态 |
| S5 | resolver 确认无 context key，caller 明确选 Task/Delivery | 沿既有 explicit-task 校验，无会话写入；显式 key/cwd 不能将有 context 缺绑定伪装成此路径 |
| S6 | 无 Issue 的 standalone_request，真实 Wording 输出与当前 source 可得 | 使用同一请求身份、真实 caller_locator 和 producer mode；正常构造到 ready，构造错误后 Agent 自行完整重建 consumer |
| S7 | 已选 Delivery 或 Task-only 的正常文档展示停点 | 已选切片向原 resolver 传入实际 key；无当前切片只展示明确 TaskRef 的根 PRD，不猜选或创建空切片 |

## 5. 行为要求

### R1 跨会话接续同一对象

- 在主会话接回子 Agent 创建结果，以及新独立审核子会话接收明确 TaskId、generation、DeliveryKey 和 planning_root 时，先检查调用会话自己的 Task/Delivery 状态，再进入原阶段 owner。
- 存在 context key、缺少 Task 绑定时，经原身份、checkout、Bind owner 恢复明确的同一 Task；绑定存在但缺少 Delivery 选择时，经原 Delivery Selection owner 选择明确的原 Delivery。写入前核定目标 generation、checkout 及 Delivery 适用性；恢复后重读公共 current、phase、scope 和 planning_root，继续原有未完成义务。
- 原 resolver 确认无 context key 时沿既有 explicit-task 执行，不写会话。显式 key/工作目录不能把有 context、缺绑定的调用改判为无 context。
- 只补缺失事实；匹配绑定/选择复核复用，不重复写。新绑定不代表已选 Delivery；恢复不改变 phase，不产生 Planning/Check/Review pass。
- 不同选择、真实 stale、歧义或冲突交原 owner，不静默覆盖；不改环境身份借用主会话绑定，不从唯一 inventory 行猜选对象。
- 保留 TaskId/generation、Delivery、规划、适用审核及 Git 资源；回到仍适用的原 profile/purpose，按唯一 continuation 消费实际前序输出与 source_selection。丢失或失效输出回原 producer，按原合同刷新或合法返工，不凭 phase/文件猜 pass。身份恢复本身不重置规划、重开 Intake、删除重建或创建空 Delivery；同范围恢复不重复询问“继续”。
- Architecture 保留 fresh reviewer 和原读取顺序；绑定恢复不注入 PRD、验收或前序 pass 叙事。
- 修复实际 caller/consumer mandatory 衔接；仅补提示、仍由用户绑定不满足 R1。Markdown 判断路由，validator 不代替原 Bind/Selection writer。

### R2 准确诊断并进入原恢复 owner

- 区分公共 current 的 `no_current_task`、`no_current_delivery`、`current`、`terminal_delivery` 和 `error`，并区分已选 key 不同与真实 phase/generation/scope 失配。下表规定各类事实的处置；不要求新增一套状态模型或给每个条件新增 public typed exit。

| 实际事实 | 期望处置 |
| --- | --- |
| 有 context，`no_current_task`，目标当前身份、唯一 checkout 及非终态 Delivery 适用性已核定 | 原 Bind owner 恢复同一 Task，再由原 Selection owner 补齐明确 Delivery 选择 |
| 同一当前 Task，`no_current_delivery`，明确目标非终态且适用 | 原 Selection owner 选择已明确的原 Delivery，不创建新切片 |
| `current` 且 key、generation、scope、phase 均适用 | 复用当前选择，进入原未完成义务 |
| 不同 Task/Delivery、`terminal_delivery`，或真实 phase/generation/scope 不符 | 返回对应生命周期或选择 owner；不能用“补缺绑定”覆盖现有合法选择或重开终态 |
| `error`、损坏/不可读绑定、API 不支持或 checkout/身份歧义 | 保留具体错误条件，按原 owner 停止或恢复；不能当作 `no_current_task`，不能静默覆盖或借用别的会话 |

- 诊断必须指出实际条件及对应原 owner，不能统一暗示规划或内容过期。若多个条件同时不符，说明本次检查首先失败的条件；恢复后重新读取其余条件。
- 普通缺失绑定或选择按 R1 接续；真实失配仍 fail closed，并只刷新受影响的原 owner 义务。
- 保留校验强度和公共语义；schema/exit/错误合同变化须有明确兼容或迁移方案，不静默改 API。

### R3 standalone_request 的 producer 身份投影

- `standalone_request` 是无 Issue 的来源 profile，与执行 mode 独立；保留现有 `workflow` 和 `standalone` 两种 mode。public_input、owner_result 与实际 producer transition 的 mode 必须一致，不因 profile 名称强制切换。
- `public_input.target_locator` 取真实 Wording `transition.target_locator`；当前 source `draft_id` 与 authored `target.request_id` 使用同一请求身份，不用 Task 名、Issue 标签或展示名替代。保留完整 producer transition 和 continuation。
- `target.caller_locator` 定位真实调用方，可以不同于请求身份；不新增与 producer locator 相等的限制。示例覆盖该合法组合。
- 明确 `source_request_sha256` 是当前 draft authority projection 的摘要，不是 body-only SHA。复用 recorder 派生字段和真实 checker receipt；提供完整可执行的最小 authoring/envelope 示例，不新建 profile、schema 或入口。
- 同范围构造错误时，重读当前 source 与仍适用的真实 producer 输出，重审消费者自身十维判断，完整重建消费者，再经 record → check → invoke 接续。不修改 producer、补算 private linkage、另造 request_id 或重复完整前序审核。前序输出丢失/失效回其原 producer；source/body/authority 真变按原链刷新；缺证据准确停止。
- 既有 mode/digest/通用恢复继续复用，只补 standalone 映射和 recipe。错误拒绝不证明 runtime 缺陷；合法输入通过时保留 normalization。

### R4 本次修复中发现的同链路合同差额

- 本次修复过程中发现、能够通过受支持正常入口复现并直接影响同链路接续或文档展示的合同差额，由 #679 同批处理。每个新问题仍由原 owner 核定实际条件、当前必要性和最小修复，不凭静态命中扩为全库历史清理。
- 当前 workflow 的 Human artifacts 命令省略原 package-owned resolver 必填的 `--delivery-key`，正常执行返回 `invalid_arguments / arguments`。已明确选择 Delivery 时，调用方必须将实际 DeliveryKey 交给原 resolver，读取同一 planning_root 的实际文档路径。
- Task 级停点尚无 Delivery 或没有当前 Delivery 时，仅展示明确 TaskRef 内存在的整体根 PRD；不得从 inventory 猜选 Delivery、构造假 key 或为展示文档创建空 Delivery。已归档的明确切片使用实际 archive TaskRef 与对应 DeliveryKey。
- 修正 canonical workflow 与 dogfood/installed 的命中说明；保留原 helper、公共 API、owner、阶段和最小输出。使用原 package-owned 定向回归实际执行受改调用，核对存在/缺失文件和返回路径；文本一致不能替代行为验证。

## 6. 约束与依赖

- 定位：上述四处源码；guru-bind-task-session、guru-create-delivery 接续合同；Readiness standalone 指引/示例；Guru workflow 调用衔接。
- #548 创建到激活/原任务恢复与 #396 proposed_draft 构造/恢复继续复用；本 Issue 只补正常跨会话与 standalone 差额。
- #666 仍负责通用停顿/重复确认，本 Issue 完成不关闭它；#363 遥测不是前置。
- 不新增 binding writer、全局映射、wrapper Skill、长期 reviewer/授权记录或通用恢复框架。Markdown 拥有 AI 判断和路由；脚本执行、校验事实。
- 不改 Trellis 上游、全局 npm、node_modules 或官方 Agent/hook；不升级/清理/修改业务 Task，不向业务仓 commit/push/PR、生产写入、部署或 Release。guru-trellis 交付按原 workflow 和副作用边界；Issue 修订不代表实施。
- 验证限于诚实协作中的正常创建、接续、普通操作错误与真实状态变化。排除恶意篡改、压力竞态、锁及非常规 crash consistency 加固。

实现方式及公共诊断兼容性由规划阶段核定。

现有 canonical Skill、workflow、安装投影和官方公共 API 是实施输入。诊断兼容性方案与命中 consumer 的改动范围由原 Author/Architecture 在 Delivery 规划核定，不在本整体 PRD 预设新 schema、exit 或错误 API。

没有业务数据、数据库或部署配置迁移。若公共诊断语义变化确有必要，必须提供明确兼容或迁移合同；不能以“不涉及业务数据”省略该项。原生工具不可运行时只阻塞对应证据和完成声明，不得以静态结果代替。

## 7. 可观察验收与验证方式

以下六项编号对应来源 AC1–AC6；它们定义预期结果，尚未执行或记为通过。

1. 隔离仓库用正常 writer 建样本，原生主/子会话分别承接创建结果和独立 Architecture 审核，保留修复前首次失败/修复后成功对照。接收会话初始未绑定，不预绑/预选，不用业务 Task 或手写 session JSON。提示只给事实、目标、边界，不给答案、恢复步骤或预期 pass。初始 planning 经原 Bind/Selection 和真实语义门禁到 Author/Architecture 正式出口；已有进度回原未完义务。补绑定不重跑初始规划；真实前序失效按原 owner 刷新受影响步骤。人工补绑定只证明可恢复，不能证明流程修复。
2. 按 R2 表验证缺 Task/Delivery、匹配/不同选择、终态、真实 phase/generation/scope 变化和 error；无 context explicit-task 单独验证。记录恢复前后 current、原 owner 和正式出口，保留 TaskId/generation/Delivery、规划、适用审核及 Git 资源，不污染其它会话或并行 Task。改 profile、环境身份、错误名或提前推进阶段不算成功。
3. 复用现有 Intake fixture、回放入口及真实 producer 输出验证 standalone_request。正确最小输入及不同 caller_locator 可到正式 ready；自拟 request_id 被拒后，原生 Agent 读取合同，从未改 producer 完整重建消费者，再到 ready。测试 helper 不替 Agent 完成映射，不手写 pass/receipt。package 层验证两种 mode 的合法输入及 mode 失配拒绝；原生回放用其中一条实际 mode，不冒称双 mode 原生通过。source/body 变化仍按原链刷新。
4. 盘点本次共享绑定/current 边界的直接消费者，核对 Author、Wording、Architecture、Approval、Activation。仅对确实命中的调用边增加或复用定向回归；保留 #548 有/无 context、#443 会话隔离及 #396 proposed_draft 正确行为。不扩为全生命周期重写，使用原规划和 Test SSOT。R4 同时核对受改 Human artifacts 调用：明确 DeliveryKey 的原 resolver 返回实际切片路径，Task-only 展示不猜选或创建切片。
5. 完成证据逐项对应“历史覆盖边界 → 首个失败条件 → 实际机制改动 → 正向及失配结果 → 验证”。分别报告源码/package、安装投影和原生 Agent；原生不可运行记未验证。静态文本、parity/checker、mock key 或手动绕过不能关闭对应原生验收项。验证无需重复询问同范围“继续”，并保留独立审核隔离。
6. canonical 与 dogfood/installed 的受影响投影、reapply/drift 及定向兼容一致。普通修复不承担完整多平台 Release/Upgrade 矩阵；未验证平台和已有业务安装升级明确列出。R4 的调用说明与原 package-owned 定向验证一并覆盖受影响投影。

| 验收 | 关联要求与场景 | 必要证据 |
| --- | --- | --- |
| AC1 | R1/R2，S1–S3 | 正常 writer 隔离样本，主/子原生接收首次失败和正式出口对照 |
| AC2 | R1/R2，S3–S5 | 每类 current/失配/error 与无 context explicit-task，恢复前后身份、规划、资源和原 owner |
| AC3 | R3，S6 | 两 mode package 合法/失配与不同 caller_locator；一条真实 mode 的原生拒绝后消费者重建 |
| AC4 | R1/R2/R4，S1–S5、S7 | Author/Wording/Architecture/Approval/Activation 直接消费边盘点及命中回归，保留 #548/#443/#396 |
| AC5 | R1–R4，S1–S7 | 历史覆盖→首失败→改动→正向/失配→验证逐项对应；package/安装/原生分层 |
| AC6 | R1–R4 | canonical/dogfood/installed、reapply/drift/sidecar/mode 定向验证，明确未验证平台及业务安装 |

## 8. 实际未决项

整体需求没有尚未解决的产品或范围选择。技术未定项为首失败诊断的兼容表达、五个直接消费者的命中范围以及原生回放的最小隔离样本安排及 R4 展示分支的命中回归，由原 Delivery Author 与独立 Architecture 在 plan_ready 前核定。实现和所有验收尚未发生；本 PRD 不预填阶段或整体通过。

