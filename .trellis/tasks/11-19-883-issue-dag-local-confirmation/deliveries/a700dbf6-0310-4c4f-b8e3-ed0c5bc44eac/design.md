# #883 D1：局部授权等待设计

## 1. 设计目标、需求承接与内容基线

实现 [D1 PRD](prd.md) 的 AC1–AC4 和 R3。Delivery 开发基线 B 是 Intake 固定的 `origin/main@8b92022d6cdf8f9debda09ed68602f1d137e3629`，Planning H0 与 B 相同。原候选构造器以后按实际提交 H 绑定完整 B..H。PR 与完成目标均为 `main`。

阶段适用的 Architecture authority 为 `guru-trellis-architecture`，当前宪法为 `guru-trellis-design-constitution-v1`；沿用 [项目 change contract](../../../../../docs/architecture/06-governance/change-contract.md)。新版独立候选评估返回 `baseline_current / architecture_impact / target_native`。现行边界承接 ARCH-FND-002、ARCH-FND-005、ARCH-DOM-ISSUE-REVIEW-INTAKE 和 ADR-ISSUE-REVIEW-INTAKE。本设计仍须独立 `final_plan` 评估。

## 2. 当前系统、边界与差额

公开 DAG 入口加载共享 Markdown 编排方法。共享方法已定义授权和原生有界观察，但没有明确从确认通知回到观察循环的同轮动作。隔离基线中，协调者以最终回复交出 A 的确认，B 仍在运行。D1 补齐此处的消息与工具顺序，以及两个正常节点停点的狭义授权规则：Git 失效注册和已收敛的 Issue 正文修订。没有前序 Delivery。

## 3. 来源设计处置

| 来源与承诺 | 处置 | 落点及依据 |
| --- | --- | --- |
| [#883](https://github.com/castbox/guru-trellis/issues/883)：已有委托覆盖且目标仓无直接确认要求时按原前置继续 | retain | §6 核对具体动作，指示原 owner 并回读。 |
| #883：局部确认时仍观察独立工作，保留终止、失败策略和写权限 | retain | §4–§7 保留原消息与观察机制，只暂停依赖该授权的工作。 |
| #883：真实 Agent 公开入口，同一场景和设置对照 | retain | §8 保留现行基线、载体证明、候选证明三类证据。 |
| #883（07:01:56Z）：两项免单独确认、准确作用域、回读与原节点接续 | retain | §4–§8 保持共享 SSOT，原执行者按正常入口落实，当前约束不能反向扩大到其他动作。 |
| #883：实际中断后恢复原身份，未知结果先查原操作 | retain | §7 复用原恢复入口。 |
| [共享方法](../../../../../trellis/presets/guru-team/spec/workflow/issue-orchestration.md)：会话权限、原生观察、通知去重、原 owner | retain | §4–§7 保留权限来源和现有观察循环。共享方法单写，DAG 直接消费。 |

## 4. 模块、职责与设计取舍

原共享方法 `trellis/presets/guru-team/spec/workflow/issue-orchestration.md` 单写授权判断、提供确认请求和下一观察动作。协调者使用宿主已支持的用户可见非终结消息，然后复用现有快照、游标、有界等待和状态回读。DAG 合同继续拥有节点调度、依赖、失败传播和整图终止；只在存在路由缺口时补共享方法引用。Sequence 共享通知规则，仍按原串行范围工作。

仅改最终回复的字句无法延续已结束的轮次。增加定时器或新调度器会转移责任并引入状态。因此复用当前协调者及原消息、观察工具。若宿主无法提供非终结消息，记录具体能力缺口，沿现有观察与恢复规则处置，不宣称已完成同轮交互。

源私有隔离载体复用真实 coordinator 和 child Codex 进程。它只记录事件和时间，接受主持者释放 B 的状态，执行 Agent 选定的模拟动作。主持者查看实际请求后释放结果；脚本不按关键词决定通过或代选路由。

### 两项 DAG 例外的责任

共享方法定义例外的资格和协调处置。DAG Skill 及本地合同引用它；Sequence 不获得这两项例外。现有目标仓库直接确认规则仍有效。协调者通过原子会话指令和回读承接，不能自行执行 Git 或 Issue 写回。

- **失效注册。** 当前节点必须有原步骤的实际共享仓库注册阻塞。原执行者在同一 Git common-dir 读注册、预览、目录状态和正常 Task/操作保留事实。只有全部资格同时满足且实际命令候选集合与明确拟处理的逐项核对集合相等，才运行匹配命令。现有 Git 没有逐注册 prune 选择。对于现场所用 `git worktree prune --expire=now`，先核对同参数的完整 `--dry-run --verbose`；有额外条目则暂停并复查，不能改用直接删除注册文件。回读注册差额和原节点状态后接续。
- **Issue 精准修订。** 原审核者交付当前 Issue、精确完整正文和固定权威证据。协调者核对目标、完整待写内容，以及目标、范围、验收和执行边界均保持。原 owner 用其现有 `issue_body_edit` 路径回读最新正文及待替换内容，再以原 repo-bound 写入入口执行。若 preimage 变动，先重新审核；写后必须核正文并消费 `refresh_context`，刷新受影响 Intake 与原审核。仅无标识冲突不足以认定已收敛。未决选择、实质变化和目标仓明确直接确认继续走原边界。

## 5. 接口与数据

公开 Skill id、输入、输出、typed exits 和 Git/GitHub 写入 owner 不变。生产端不新增字段、审批记录、通道或持久状态。Git 预览及注册回读、gh 读写分别是事实与执行；不能代替协调者或原审核者的判断。授权仍来自当前用户消息。隔离载体的时点、运行目录和事件开关均不进入产品或公共包。

## 6. 执行顺序及正常分支

1. 按原循环读取实际 child 提案、目标和当前步骤结果，核对委托、仓库限制及原前置。
2. 条件通过且无需用户直接确认时，给同一原 owner 精确指令并追踪结果。待授权标签本身不是确认理由。
3. 确需确认时，暂停受影响动作和依赖。仍有独立工作或有效有界等待时，在本轮提出具体请求后立即回到观察。B 结果变为可读时实际回读并交原 owner 承接；用户未回复前不推进 A。
4. 若原步骤为 §4 的两个停点之一，按所述资格和原 owner 写回边界处理，回读后接续同一节点原步骤。未知结果先恢复实际 Git/Issue 写入事实，不重复。
5. 原通知去重仍适用，去重不跳过观察。原终止条件、用户停止与宿主实际中断继续按原路径处置；最终回复不能替代独立观察。

## 7. 恢复、兼容、迁移与集成

实际中断后先回读原子会话和原操作，说明观察空档。指令或写入结果未知时先核证，避免重复。保留现有 DAG/Sequence 入口、旧 run 恢复和终局消费者。无新接口或数据迁移；受管 Markdown 经原安装 owner 同步。

## 8. 验证设计

- V1 / AC2：公开 DAG 入口运行相同的 A/B 受控场景。保留 A 的实际发布准备与直接确认要求、B 的独立有界 Test。执行设置均为 `codex-cli 0.167.0`、`gpt-6-luna`、`high`。用户不回复，隔离主持者读取请求时独立释放 B 结果。对照确认时点、B 可读时点、同轮回读及推进、A 未执行及轮次边界。最终回复上的请求以结束前状态判定是否复现；缺必要事实判证据不足。
- V2 / AC1：同一公开入口运行已有委托场景，证明精确指令、原 owner 执行及协调者回读，未出现额外用户询问。
- V3 / R3：核对适用既有恢复证据及未变路径，只给受影响恢复分支补针对性验证。
- V4：验证源包、受管安装和共享消费者，独立报告安装及行为结果。保留原失败轨迹；载体能力探针不替代同轮行为。Codex App 原生消息/调度、真实 PR/Test 发布与完整升级矩阵均未验证。

- V5 / AC3：公开 DAG 入口的真实协调和子 Agent，隔离 Git 仓库用正常原步骤收到 stale registration 阻塞。留原目录、注册和 Task/运行操作核对、预览与限定指令、实际前后差额和同一 Task 创建重试。另在命令会触及未核对注册时验证暂停复查。已有一次本机清理只证明现场路径。
- V6 / AC4：公开 DAG 入口下的隔离 Issue。基于 [Backend #1944](https://github.com/castbox/ai-chat-roleplay-backend/issues/1944) 固定基线例子，给真实审核者可证明已收敛的标识、旧完整正文和精确待写正文。观察协调者免问指示、原 owner 写前核对、写入、回读和 Intake 刷新。仅无冲突但未确定的选项保留原确认；若普通并行修改使 preimage 改变，原 owner 重审后才可写。载体提供事实、执行模拟动作，不代替判断。真实 #1944 不写。

## 9. Canonical 引用与差额

Requirements R731-04/05、Design D731-01/04/05、Test T731-03/06/07 及原生监督章节由原 RDT owner 整合本轮差额；见 [实施计划 §6](implement.md#6-docs-ssot-plan)。保留 [Architecture Baseline](../../../../../docs/architecture/00-foundation/baseline.md) 的控制面和事实执行分层。新版为 `target_native`，由 [架构贡献](../../../../../docs/architecture/contributions/883-dag-local-dispositions/contribution.md) 和其隔离 ADR 拟案承接。贡献只描述职责变更及晋升目标，不复制共享 Markdown 判定。原 Architecture 维护方实施后、TaskCommit 前核对真实候选与目标，整合并回读；提交后的独立 Review 核证。无待用户选择的需求，候选尚未验证。
