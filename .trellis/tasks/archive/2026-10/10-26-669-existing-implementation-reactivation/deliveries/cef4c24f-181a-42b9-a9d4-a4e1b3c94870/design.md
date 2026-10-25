# D1 已有实现分支恢复设计

## 1. 设计目标、需求承接与内容基线

本批承接 D1 PRD 的 R1–R7、AC1–AC5。固定 development baseline B 和 Planning H0 均为 `83512901506409f59016121aebc2d0b0bbe98059`；来源是首次 D1 建立时已同步的 main。内容范围始终为 B 到本 Delivery 的实际候选，PR 目标为 main；无关目标推进不改写 B。

独立 Architecture `candidate_assessment` 已通过正式入口返回 `baseline_current`：`architecture_impact / target_native`，baseline `guru-trellis-architecture`，constitution `guru-trellis-design-constitution-v1`，decision `ADR-PORTABLE-SHARED-LIFECYCLE`。该判断的唯一后续步骤是本次方案写作，不代表 final_plan、实施或 Check 已完成。

## 2. 当前系统、边界与目标差额

当前 Reactivate 单写前驱核验、后继发现、原公共 reopen/formal operation 和本机 branch/resource 接线；C3 单写 checkout acquisition，C4/C5 单写绑定及本机责任。旧入口只接收 base HEAD 上的干净工作区。当前 Task2 reopen 保留历史并递增 generation；已有后继走实际 key/ref。

本批仅扩展原 owner 对“已有实现 HEAD + 已审本地差额 + 原 Draft PR”的接受能力。独立 profile/schema 避免把所有 acquisition 变成 allow_dirty；原旧入口、rebind 和 capture_checkout_state 的既有语义保持。首次 D1 无前序方案。

## 3. 来源设计处置（唯一）

Issue #669 明确把具体机制交设计阶段。它对原 owner、完整保留、单次增代、当前重新审核的要求由本方案第4–8节落实，不属于既有详细设计的改写。当前原公共 Task API、ARCH-DOM-060 和 ADR-PORTABLE-SHARED-LIFECYCLE 是必须保留的架构约束：继续原 writer，不另造 lifecycle、migration owner 或当前通过证据。没有需要 retain/change/reject 的外部已批准实现方案，不建立空矩阵。

## 4. 模块、职责与设计取舍

| 模块 / owner | 本批职责 | 边界 |
| --- | --- | --- |
| `guru-reactivate-task/SKILL.md`、interface 和独立 profile | AI 核前驱、来源、base、实现、完整本地差额、PR、ownership，决定路由 | 不把 preview/checker 当语义通过，不记录授权 |
| package read-only observer | 读取准确 checkout 的逻辑内容和原 PR facts，输出同 owner 的调用期比较输入 | 只读 Git/gh，无 tracked checkpoint、无 remote write |
| `task_lifecycle/git_facts.py` | 复用 Git读取，增加本场景需要的逻辑 index/worktree 内容身份 | 不改变原 raw-index snapshot/rebind consumers |
| `checkout_resolution.py`、`checkout_acquisition.py` | 新恢复调用绑定已审核内容，仍核准确仓库、注册 checkout、分支、HEAD、任务预期 | 不增加通用 allow_dirty；普通调用继续 clean |
| `guru-reactivate-task/runtime/invoke.py` 及本包必要 helper | 在原 acquisition、公用前驱/后继核验和 public writer 中承接新 profile；保存最小同操作恢复信息 | 不复制一套 reopen/Task parser/branch store |
| 原 public Task、C4/C5、Bind 和 Delivery owners | 原模型增代、真实绑定、后续当前质量门禁 | 不迁移旧通过，不自动发布 PR |

选择独立输入和有界内容比较，是因为真实 base 与实现提交是不同对象，且已审工具升级差额必须保留。直接取消 HEAD/clean 会接收未审状态；把既有实现移入临时 branch、先 reset/stash 或借 rebind 会增加内容迁移及资源副作用，均不采用。

## 5. 接口与数据

新增 `delivery_reactivate_existing_implementation`，仍由原公开 `guru-reactivate-task` 调用。独立 public schema 明确原 `archived_lifecycle`、`archive_anchor` 和原 Draft PR 的准确 locator；准确 branch、checkout 和实现状态由当前 AI 的独立 semantic schema承接。公开退出维持现有四种最小 DTO 和唯一 consumer，不向 Bind/Planning 传 snapshot 或 PR 审查历史。

旧 shared-archive public/semantic/schema 和 transaction 2.0 保留原义。Interface 以新 selected aggregate 暴露两个明确 profile；`MIGRATION-669.md` 说明新增入口、旧调用不变、匹配安装与旧在途操作边界。不得把旧输入重标为新通过。

内容比较覆盖逻辑 index entries 的 path/OID/mode/stage、工作区 tracked/untracked 内容、文件类型和执行位，以及分支/HEAD。snapshot 只输出摘要，不输出文件原文或凭据；Git index 的 mtime/cache/stat 刷新不改变逻辑内容。所有 .trellis 下真实本地差额也纳入，不能整体忽略 .trellis。

`reviewed_base_head` 单独核准确当前 base；acquisition `decision_head` 在新 profile 绑定实际实现 HEAD。原 PR 必须是所选仓库的开放 Draft，base 为所选目标，head branch/HEAD 对应准确实现。fork 或错误 repository/head/base、非 Draft、已关闭状态具体停止。PR facts 只来自 repo-bound gh，恢复不调用 push/edit/create/merge。

新 profile 如需要恢复交易版本，使用独立 3.0 schema；保存准确前驱/事务/绑定、真实 base 与实现 HEAD、原 PR identity，以及同操作下一步必需的最小内容比较值。操作前快照服务首次 acquisition；操作后快照服务输出丢失重试。不得用自己刚生成的 Task metadata 对比操作前状态而误报漂移，也不能放宽到忽略无关改动。公共后继已存在时优先核身份和历史，再继续实际后继；无本机旧 receipt 本身不授权再增代。

## 6. 状态、顺序、正常与失败流程

1. AI 读 live Issue/前驱归档/准确 bookkeeping PR 与目标可达性；原 shared reader 核 TaskId/generation/source/Completion/Closure。
2. 先发现实际公共后继。合法后继进入原接续；冲突后继停止。没有后继才审核新 acquisition。
3. 观察所选 checkout、base、实际实现 HEAD、完整本地差额和原 Draft PR；AI 判断范围和充分性。只在新 profile 使用已审精确内容作为 C3 的合法输入。
4. 执行前重新核 base、checkout、branch/HEAD、PR、内容及资源责任。任一失配均具体停止，零远端写入、零清理。
5. 原 acquisition 接收准确既有 checkout，保留 caller ownership。原 public reopen/formal operation 建立 generation+1；原 C4/C5 绑定。
6. 记录原交易实际结果和必要 after-state，返回真实 key/ref。Bind 缺失交原 session recovery；有业务变更进入原新 Delivery 创建及当前规划，不调用旧 gate pass。

原 operator 的正常重试接续同一操作。冲突、失配或依赖缺失保留提交、工作区和 PR；不删除现场来获得 clean。

## 7. 恢复、兼容、迁移与集成

已有公共后继时核其来源与保留历史；同操作输出丢失继续原后继，不重复 writer。若 public work 已发生而本机后续步骤失败，保留原公共事实，沿原 transaction/Bind route 完成，不做不安全回滚。已审事实发生实际变化后回当前 AI 重读，不能复用旧 snapshot 作为通过。

旧 clean-base 入口仍有当前从 base 开始的新工作消费者，本批并未退休它；新增入口只承接明确已有实现状态，不形成任意旧格式的 dual reader。旧在途 transaction 2.0 继续由原 owner 读取原格式，不能默默套用 3.0 的新内容。Matching preset/reapply 同步 canonical、dogfood 和声明平台；不 patch global npm、node_modules 或上游 Fork。

## 8. 验证设计

| ID / AC | 层与入口 | 输入和预期观察 |
| --- | --- | --- |
| V1 / AC1/3 | 原 package 源码测试及真实 Git/public writers | 合法归档、实现提交不同于 base、现有 Draft PR；只增代一次，重复执行返回同后继 |
| V2 / AC2/4 | acquisition/逻辑内容定向回归 | staged/unstaged/untracked、内容/类型/执行位、普通 index refresh；相同逻辑状态通过，实际失配停止；原内容不变 |
| V3 / AC4 | 前驱/PR/ownership 普通失配 | 错仓库/base/head、分支/HEAD推进、冲突后继和未完资源责任；具体停止，零远端 mutation |
| V4 / AC1–4 | 旧入口与现有原后继恢复回归 | 旧 clean-base、原正式 schema1 和 schema2 分工、丢 receipt 与 caller-owned 资源语义不被新 profile 改写 |
| V5 / AC5 | canonical、dogfood、installed、reapply/drift/sidecar | source/package validation、apply和drift检查；必要投影一致，sidecar逐项处理，不扩完整多平台Release矩阵 |
| V6 / AC5 | 一个代表完整安装后的真实 Agent 原生恢复 | driver只提供真实Git前驱/实现、受控repo-bound gh PR事实和客观观察；实际AI owner从installed公开入口读事实、写semantic result并恢复；分别记录安装、恢复与正式后续门禁 |

V6 沿当前 T635 明确规定的真实 Git/受控 provider 模式。它不证明 backend #802 已恢复、真实 GitHub 写入或业务生产效果；本批也不承担这些外部写入。source单测不能替代V6。

## 9. Canonical 引用、本轮差额与实际未决项

RDT 完整单元为 `docs/{requirements,design,test}/current/completion-closure.md`，Architecture 完整 owner 单元为 `docs/architecture/03-domains/ownership.md` 的 ARCH-DOM-060/shared lifecycle。task-owned Architecture contribution 位于 `docs/architecture/contributions/669-existing-implementation-reactivation.md`，阐明本方案、准确前驱、直接 consumers和验证限制。现有 ADR-PORTABLE-SHARED-LIFECYCLE 足以承接，不新增 ADR/GAP。

实施产生实际完整候选后，原独立 Architecture 与 candidate Check 先审旧 authority 和隔离拟写正文，原 Architecture/RDT owners 在 final_integration 晋升完整 current 单元，再由实施 owner 重绑实际 after 候选、最终 Check/commit/完整 Review 覆盖。不得先写共享 current 再补通过。方案当前无阻塞未决项；若实际 source/owner/恢复语义变化，回最早受影响 owner。
