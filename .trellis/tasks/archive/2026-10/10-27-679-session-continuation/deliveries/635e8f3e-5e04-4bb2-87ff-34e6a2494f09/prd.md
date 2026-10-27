# D1 跨会话接续、诊断与 standalone 身份投影需求

## 1. 整体来源与术语

整体 authority 是 [Task PRD](../../prd.md)，公共 scope_ref 选择 R1、R2、R3、R4、AC1–AC6。DeliveryKey 为 `635e8f3e-5e04-4bb2-87ff-34e6a2494f09`，generation 0，planning_root 为 `deliveries/635e8f3e-5e04-4bb2-87ff-34e6a2494f09`。本批使用原 Clarify 的来源选择，不重新选范围。

| 来源 | 章节、角色与用途 |
| --- | --- |
| [live #679](https://github.com/castbox/guru-trellis/issues/679) | 全文要求与约定边界；本批行为和六项验收 |
| [整体 PRD](../../prd.md) | 第4–7节；整体场景、完整条件、约束和验收责任 |
| docs/requirements/current/task-delivery-lifecycle.md | 当前身份和 Planning 要求；保持同对象/原 owner |
| docs/design/current/task-delivery-lifecycle.md | 当前职责；Markdown 路由、原应用状态和 writer |
| docs/requirements-design-test-contributions/548-creation-recovery/test.md | 历史证据；区分 explicit-task、预选 D1 与未绑定接收差额 |
| docs/requirements-design-test-contributions/396-draft-intake-recovery/test.md | 历史证据；区分 proposed_draft 与 standalone_request |

context 是原 resolver 的当前会话身份；显式 key 不是绑定。standalone_request 是来源 profile；执行 mode 仍为 workflow 或 standalone。正式出口只来自原公共 invoke，记录器/扫描/投影不提供语义 pass。

## 2. 整体与本批目标、非目标

现有 adapter 的有 context 选择限制正确，但交接明确身份后缺少 caller mandatory 衔接；Author/Architecture 的复合 stale 诊断无法区分首失败。Readiness 正确校验 request_id，本批补 standalone 构造和恢复指引。原 Human artifacts 展示命令另有遗漏必填 DeliveryKey 的正常调用失败，本批一并修正。

这是首次全量 D1，承担整体 R1/R2/R3/R4 与六项验收。交付目标是让正常主/子接收会话自行通过原 Bind/Selection 继续同对象的实际义务，并提供准确首失败诊断、真实 producer-bound standalone recipe 和明确对象的文档展示调用。

本批排除 #666、#363 遥测、业务故障和业务仓/业务 Task 修改、生产/部署/Release，以及完整多平台 Release/Upgrade 矩阵。攻击、伪造、压力竞态、锁及非常规 crash consistency 不进入测试或实现。

## 3. 本批起点、前序结果、依赖与剩余责任

没有前序 Delivery。起点为 main `e6c3b8276d62ac174ab42cba5bca4d5784be2ca3`，仅完成本 Task 创建和整体范围接受；当前公共 phase 为 planning，各阶段 gate 缺失。

输入为匹配当前的 Guru/Fixed Fork 安装、明确 TaskId/gen/key/root、原来源选择及实际 producer 输出。原 Bind/Selection 的状态写入和 explicit-task 校验继续复用。原生样本只能在隔离仓库由正常 writer 创建；接收会话不得预绑定或预选。缺原生运行能力时，对应验收保留未验证，不用 package 结果填补。

本批之外没有已计划的实现切片。整体 Completion 仍须独立审查全部六项证据及实际结果；Issue Closure、Finish 与 Cleanup 保留各自边界。

## 4. 本批调用方、场景与流程

| ID | 调用方与前置条件 | 触发、处理和可观察结果 |
| --- | --- | --- |
| S1 | 主会话接回明确创建结果，当前调用会话未绑定 | 原入口检查自身 current，经原身份/checkout/Bind 与 Selection 补缺，重读同 key/root 后到 Author 正式出口 |
| S2 | 全新独立 Architecture 子会话，明确 key/root，未绑定/未选 | 自行读取安装合同并恢复自身事实；保持 baseline-first 和 fresh reviewer，实际到 Architecture 正式出口 |
| S3 | 同 Delivery 已有 Author/Wording/Architecture/Approval 进度，缺绑定或选择 | 保留规划/适用前序，回实际未完义务；缺失/失效输出回原 producer，不重启初始规划 |
| S4 | 不同 Task/key、terminal、真实 phase/gen/scope 变化 | 保留首失败与原 owner，不静默切换、不重开终态；修复后再检查余下条件 |
| S5 | current error、损坏/不可读绑定、API 不支持或 checkout 歧义 | 原样保留具体条件并停止或交原 owner；不能归为缺 Task |
| S6 | 原 resolver 确认没有 context，caller 明确 key | 沿既有 explicit-task，校验同 Task/gen/C4/profile，不写 session |
| S7 | standalone_request，真实 Wording 输出/当前 source 可得 | 以 producer locator 绑定请求身份，独立 caller_locator，mode 一致；两 mode package 正常可到 ready |
| S8 | standalone consumer 自拟 request_id 被正常拒绝 | 真实 Agent 从未改 producer 完整重建 consumer，重审十维，再 record/check/invoke 到真实 ready；source 真变或缺前序交原 producer |
| S9 | 已选切片、无当前切片或归档的文档展示停点 | 明确切片向原 resolver 传实际 key；Task-only 只展示精确根 PRD；归档保持 archive TaskRef/key，不猜选、不造切片 |

## 5. 完整行为、条件与约束

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

规范性来源设计的具体 retain/change/reject 和落点由本批 design 第3节唯一拥有；本 PRD 不另建处置矩阵。保留 TaskId/gen/Delivery、规划、适用审核、Git 资源和并行会话内容；新绑定与选择均不生成阶段通过。

## 6. 本批验收、验证方式与未决项

以下六项仍为待验证义务，不记录预期为已通过：

1. 隔离仓库用正常 writer 建样本，原生主/子会话分别承接创建结果和独立 Architecture 审核，保留修复前首次失败/修复后成功对照。接收会话初始未绑定，不预绑/预选，不用业务 Task 或手写 session JSON。提示只给事实、目标、边界，不给答案、恢复步骤或预期 pass。初始 planning 经原 Bind/Selection 和真实语义门禁到 Author/Architecture 正式出口；已有进度回原未完义务。补绑定不重跑初始规划；真实前序失效按原 owner 刷新受影响步骤。人工补绑定只证明可恢复，不能证明流程修复。
2. 按 R2 表验证缺 Task/Delivery、匹配/不同选择、终态、真实 phase/generation/scope 变化和 error；无 context explicit-task 单独验证。记录恢复前后 current、原 owner 和正式出口，保留 TaskId/generation/Delivery、规划、适用审核及 Git 资源，不污染其它会话或并行 Task。改 profile、环境身份、错误名或提前推进阶段不算成功。
3. 复用现有 Intake fixture、回放入口及真实 producer 输出验证 standalone_request。正确最小输入及不同 caller_locator 可到正式 ready；自拟 request_id 被拒后，原生 Agent 读取合同，从未改 producer 完整重建消费者，再到 ready。测试 helper 不替 Agent 完成映射，不手写 pass/receipt。package 层验证两种 mode 的合法输入及 mode 失配拒绝；原生回放用其中一条实际 mode，不冒称双 mode 原生通过。source/body 变化仍按原链刷新。
4. 盘点本次共享绑定/current 边界的直接消费者，核对 Author、Wording、Architecture、Approval、Activation。仅对确实命中的调用边增加或复用定向回归；保留 #548 有/无 context、#443 会话隔离及 #396 proposed_draft 正确行为。不扩为全生命周期重写，使用原规划和 Test SSOT。R4 同时核对受改 Human artifacts 调用：明确 DeliveryKey 的原 resolver 返回实际切片路径，Task-only 展示不猜选或创建切片。
5. 完成证据逐项对应“历史覆盖边界 → 首个失败条件 → 实际机制改动 → 正向及失配结果 → 验证”。分别报告源码/package、安装投影和原生 Agent；原生不可运行记未验证。静态文本、parity/checker、mock key 或手动绕过不能关闭对应原生验收项。验证无需重复询问同范围“继续”，并保留独立审核隔离。
6. canonical 与 dogfood/installed 的受影响投影、reapply/drift 及定向兼容一致。普通修复不承担完整多平台 Release/Upgrade 矩阵；未验证平台和已有业务安装升级明确列出。R4 的调用说明与原 package-owned 定向验证一并覆盖受影响投影。

AC1/AC2 覆盖 S1–S6；AC3 覆盖 S7/S8；AC4 盘点 Author/Wording/Architecture/Approval/Activation 和 S9 文档展示的直接命中边；AC5 对全部证据逐项分层；AC6 证明受影响安装与兼容投影。package 验证两种 mode，原生只声明实际执行 mode。每次原生接收提示只含事实、目标、边界，不写恢复答案或 expected pass。

当前需求没有未决选择。首失败兼容表达、命中边清单和具体测试入口由 solution planning 展开；没有实际原生出口或安装证据时，后续 Check/Completion 必须保留缺口。

## 7. Canonical 引用与本轮差额

- Requirements：docs/requirements/current/task-delivery-lifecycle.md 的身份/整体责任/入口与 Planning；本批补调用会话前置事实和恢复条件。
- Design：docs/design/current/task-delivery-lifecycle.md 的原 owner/公共 state 边界；本批补 mandatory caller/consumer 接续与兼容诊断。
- Test：docs/test/current/task-delivery-lifecycle.md 及 #548/#396 历史贡献；本批补初始未绑定真实接收、standalone 身份重建与实际文档展示调用，不改历史观察。
- Architecture：docs/architecture/README.md、00-foundation/design-constitution.md、06-governance/change-contract.md；独立原 owner 评估实际候选，当前文件不预选 impact/path。
- 原子合同：trellis/skills/guru-team/packages/guru-bind-task-session、guru-create-delivery、guru-author-task-plan、guru-maintain-architecture-baseline、guru-review-change-request。只补实际命中边，不重写全生命周期。

