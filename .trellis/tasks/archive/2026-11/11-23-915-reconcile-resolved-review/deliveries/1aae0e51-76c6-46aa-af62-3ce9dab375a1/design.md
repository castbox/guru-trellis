# D1 Reconcile 冲突接续设计

## 1. 设计目标、需求承接与内容基线

承接 R915-1 至 R915-4 和 AC915-1。开发基线 B 来自已核验的 `main@8604558695dfd9d8ea2181406a87ece70d9eea63`。规划时工作区 HEAD 同为该提交。交付目标 `origin/main` 是 PR 集成目标。临时仓库的 B 和 H 由该场景的实际提交独立确定。

阶段适用架构权威是固定 B 中的 [Architecture Baseline](../../../../../docs/architecture/README.md)、[设计宪法](../../../../../docs/architecture/00-foundation/design-constitution.md)和[变更合同](../../../../../docs/architecture/06-governance/change-contract.md)。独立候选评估结论为 `no_architecture_impact`。方案采用原 Reconcile、公开 Delivery 操作和联合审核职责。

## 2. 当前系统、边界与目标差额

当前 canonical Reconcile Skill 仍要求调用方先记录 Check。详细合同及公开命令已接入提交后的联合审核。D1 没有前序切片。本轮修改执行者实际加载的指导，并由安装 owner 重新生成受管副本。受影响入口包括受管 package、Codex 的共享 `.agents/skills`、Claude Code 和 Cursor。现有公开命令、参数、schema、结果槽和状态 owner 继续承载行为。

## 3. 来源设计处置

以下条款均来自 [Reconcile 详细合同](https://github.com/castbox/guru-trellis/blob/8604558695dfd9d8ea2181406a87ece70d9eea63/trellis/skills/guru-team/packages/guru-reconcile-task-base/references/contract.md#L249)及 [#794 架构决定](../../../../../docs/architecture/adr/postcommit-independent-review.md)。#915 明确采用这些条款。

| 原承诺 | 处置 | 设计落点及影响 |
| --- | --- | --- |
| 只有原 resolved executor 根据已解决的索引、已固定父提交和精确消息创建整合提交。 | retain | 第 4、6 节。复用当前公开命令与同操作读回，保持实际父顺序。 |
| 原实施 owner 保留 Task、Delivery 与适用的 Planning，固定 B，以实际整合 H 执行 `begin_check`。 | retain | 第 4 至 6 节。公开 Candidate 和 Planning 约束继续由原作者及消费者处理。 |
| 投影接收当前 resolved input/result、实际候选及 Review authoring，只输出正式 Branch Review 输入。 | retain | 第 5、6 节。当前输入为 2.0。旧的 Check 前置指导在本轮替换。 |
| 一次独立审核覆盖实际冲突、组合和受影响消费者。适用旧证据先判断后采用。 | retain | 第 6、8 节。正式审核依次产生同一 H 的 Check 和 full_review。 |
| 旧合同仍由匹配的固定旧 provider 处理。 | retain | 第 7 节。当前安装使用现行 2.0 链路。 |

## 4. 模块、职责与设计取舍

- Reconcile Skill 使用 `trellis/skills/guru-team/packages/guru-reconcile-task-base/SKILL.md` 作为唯一入口文案源。把当前顺序和调用方写在适用段落，引用原详细合同。
- Reconcile 执行者处理冲突并运行 `execute-resolved-base-reconciliation`。公开结果给出实际整合 H 和已核对的输入事实。
- 原实施 owner 保存合法 Planning 和 B，按当前阶段接续，再使用公开 Candidate 构造器和 `delivery.py begin-check` 绑定 H。
- 调用方运行原投影。独立审核者接收投影 `result`，完成正常 Branch Review。复用现有双结果 writer，消除旧入口导致的一次额外审核或手工组装。
- 受管更新使用 `guru-upgrade-tools`。验收安装为同一候选完整 preset 和匹配 Fork。入口和分发同时修正是实现范围。只有修改详细合同或直接复制安装副本，都无法完成该交付。

## 5. 接口与数据

| 生产者 | 交接与消费条件 | 直接消费者 |
| --- | --- | --- |
| 原 Reconcile 执行器 | `delivery_resolved_candidate` 2.0。输入绑定原锚点、已解决的阶段零索引树、唯一整合目标、父顺序及消息。输出实际整合回执。 | 原实施 owner 和原投影。 |
| 原实施 owner | 公共 Candidate 保留固定 B，使用实际 H 和完整内容。以现有 `begin_check` 接续到 checking，保留适用的 accepted Planning。 | 原投影验证 live candidate；Branch Review 审核同一候选。 |
| 原投影 | 读取实际 resolved 2.0 输入、执行器回执和 caller authoring。核对 checking、H、B 与适用 Planning。返回 `result`，类型为现行 `delivery_branch_review` 公开输入。 | `guru-review-branch:delivery_branch_review`。 |
| 原 Branch Review | 读取固定 B..H 与实际解法，审核两侧及组合、受影响消费者和证据。依次写 Check 和 full_review，后者以前者为 predecessor。 | 原后继阶段按现有合同核对两个适用结果。 |

## 6. 状态、顺序、正常与失败流程

Git 从共同起点进入两侧真实内容冲突。解决并暂存后，原执行器创建一次整合提交。原实施 owner 在当前公开阶段要求下完成合法接续，并调用 `begin_check`。调用方使用执行器实际回执执行 `project-resolved-full-review`。取得投影后调用一次正式 Branch Review。原审核者仍独立时可以续审，其原覆盖须可核验且适用。按变化、缺失和适用性不明的部分补充。

执行器或投影报告普通前置不满足时，先返回相应原 owner 处理。需要修订时按现有阶段路由保留同一对象。投影成功本身只证明输入构造和客观核验。两个正式结果由当前独立审核写入。

## 7. 恢复、兼容、迁移与集成

对已完成但丢失输出的执行，原执行器按相同父提交、树、消息和终态读回原 H。原 Review 负责其两个正式结果的同候选恢复。新安装或已有 checkout 使用完整匹配分发。旧固定 provider、历史结果和现有迁移规则沿 [MIGRATION-794](../../../../../trellis/presets/guru-team/MIGRATION-794.md) 保留。发生安装冲突或普通前像不匹配时，由原安装 owner 处理。

## 8. 验证设计

- **V915-1，安装与分发。** 定向验证 canonical、受管包和声明平台中的实际入口，运行原 dogfood drift 检查。用一个代表性临时仓库验证匹配安装与适用 reapply，检查未处置 sidecar 和命令可执行性。这些结果证明分发。
- **V915-2，真实冲突接续。** 临时仓库预置完整可核验的实际原审核。让两条分支修改同一段架构正文。观察真实冲突、原执行器一次创建和精确父提交、原 B 和新 H 的 `begin_check`、实际投影及消费、同 H 的双结果和正确 predecessor。原审核者逐项说明旧覆盖或验证的采用依据与补充内容。保留可重跑输入和关键实际结果。现有 wrapper fixture 单独用于机械回归。
- 两个验证共同覆盖 AC915-1。范围限于实际本地安装与执行。外部 go-guru 采用及完整多平台升级或发布矩阵不在该观察范围。

## 9. Canonical 引用、本轮差额与实际未决项

[当前 requirements](../../../../../docs/requirements/current/task-delivery-lifecycle.md)、[design](../../../../../docs/design/current/task-delivery-lifecycle.md) 和 [T794 验证策略](../../../../../docs/test/current/task-delivery-lifecycle.md)已经定义固定 B、一次独立审核和证据采用。D1 收敛落地指导。当前没有独立的公共架构决定变更。实施阶段由原维护 owner 复核实际差额是否仍与该判断一致。范围内没有待选产品问题。
