# #769 单目标工具维护的 peer 增长与既有事务恢复

## 1. 来源与术语

Direct Source 为 [Issue #769](https://github.com/castbox/guru-trellis/issues/769) 的当前完整正文。

| 来源 | 角色 | 本 Task 用途 |
| --- | --- | --- |
| #769 背景与正常复现场景 | 已核实历史事实与当前机制证据 | 界定旧观测值保持、仅新增 peer 键的真实误阻塞 |
| #769 目标与行为 | 要求 | 原保持检查、新增 peer 隔离及明确的既有事务兼容恢复 |
| #769 范围与兼容边界、验收 | 要求 | 公共兼容、分发、真实恢复和验证层级 |
| docs/requirements/current/runtime-location.md R718-03/11 | 现行约束 | 原工具 owner、单目标维护、source/target 分别验证与 peer 保持 |
| 原 tools package references/contract.md | 现行接口/恢复合同 | 固定计划、来源、备份、目标自身验证及 public maintenance 职责 |

peer 是同一 Git common-dir 中的其它 registered checkout。原观测指原工具 owner 在首次写入前实际冻结的 common/peer 指针及运行时选择事实。新增 peer 不因拓扑成员身份获得原操作的写入或恢复资格。

## 2. 背景与问题

#766 的原工具事务已完成安装投影及目标自身验证。期间正常新增独立 worktree，原有 peer 值保持，但 `unchanged_peers` 将整个观测字典作相等比较，因新增键返回失败。原 invoke 进入 resume_required，原 resume 的 check_source 再次比较而返回 blocked。

原事务同时绑定执行源 HEAD 与 canonical tree token。直接修改原源代码来修复检查会使原源绑定失效；重写 checkpoint 或重 prepare 也会破坏恢复合同。整体目标必须同时解决未来正常操作和已被此问题卡住的原操作。

实施基线为 `main@a5f3ceeabbaccddae65935d97763f5a798f71ca9`，已含 #759 的失效 prunable peer 枚举修复。它不处理本次有效新增 peer 问题。#766 的原资产源与 Task 独立保留。

## 3. 目标与非目标

本 Task 完整交付原工具 owner 对正常新增独立 peer 的处理、旧事务明确恢复兼容、受影响分发和实际 #766 原事务恢复。恢复成功仅表示工具可继续使用；#766 自己的正式 Check、提交、合并和 Task 完成仍由原任务负责。

不自动 prune、删除、取消注册或改写其它 worktree；不重 prepare、不刷新原备份、不把后来业务改动加入恢复范围。不引入 Task 转换、全局事务、锁、TOCTOU、压力/攻击/额外故障注入或完整多平台升级/Release 矩阵。不接管 #759 或 #766 的功能实现。

## 4. 真实调用方、场景与流程

| 场景 | 调用方、前置与动作 | 处理与观察 |
| --- | --- | --- |
| S1 新操作 | 当前 tools-only install 已冻结单目标写集；其它正常工作新增独立 peer | 原观测值继续核保持，新增 peer 核隔离；不因增加键误阻塞，目标通过自己的验证后返回工具结果 |
| S2 同操作恢复 | 已冻结操作存在，之后新增有效独立 peer；原调用方执行 resume 或 rollback | 保留同一操作身份/计划/备份，新增 peer 不进入写集；原有保持检查及目标/回滚检查继续生效 |
| S3 真实既有变化 | 原有 peer 指针或已成立的合法选择发生普通变化 | 保留原正确性拒绝，不能用允许拓扑增长掩盖值变化 |
| S4 旧源事务 | 修复前原 owner 创建的事务因 S1 进入 blocked，原源资产及固定输入仍在 | 使用明示兼容恢复入口验证适用性，保持原来源/计划/备份；成功恢复 #766 同一 recovery_ref，不覆盖 checkpoint 制造成功 |

## 5. 行为要求

- R1（S1/S2）：区分原观测的值保持与正常新增 peer。不能仅因观测字典增加键而拒绝 install、resume 或 rollback。
- R2（S1/S2/S3）：原 common/peer 指针和合法已成立选择的保持条件继续执行。新增 peer 须与原目标实际工具写集隔离；它的指针、工具和业务内容不被当前操作写入，不进入备份或删除集合。
- R3（S4）：为修复前因本缺陷阻塞的操作提供明确受支持的恢复兼容路径。保留同一 recovery_ref、原 public operation/plan、Guru preimages、原资产 source 内容绑定和 rollback anchor。不重新 prepare、不换目标、不吸收后来的 owned/business 修改。
- R4（S4）：明确修复执行代码与原资产源的适用关系，机器验证必要固定事实。不能静默忽略旧 source 校验；原源缺失/变化、目标或 owned 内容不匹配时沿原 owner 报告具体阻塞。
- R5：目标自身 resolver、installed validation、native entry、原 peer 保持与新增 peer 隔离分别取证。工具结果不代表任何 Task/Delivery gate 或 Completion。
- R6：canonical package 和受影响安装/平台投影由原 tools/preset owner 成套维护。Markdown 拥有语义/兼容合同，代码只执行确定性事实；公共 I/O 有变化时提供显式兼容说明，既有 profile/exit 不静默改义。

## 6. 约束与依赖

原 public maintenance API 和冻结的 CLI/Core pair 保持原事务身份。工具资产仍来自原绑定的完整 source；修复执行代码只通过其明确兼容入口使用原事务。具体机制由选定 Delivery 的 Author 与独立 Architecture 收敛。

保留当前 source_locked 与 local_candidate 区别及 unverified 边界、用户配置和 sidecar 原 owner。不得手抄 manifest/hash、覆盖恢复锚点，或修改上游/全局包。#759 prunable 缺 .git 的精确跳过条件继续生效；普通有效/损坏 peer 仍按它的现行边界处理。

## 7. 可观察验收与验证方式

| 验收 | 要求/场景 | 入口与预期观察 |
| --- | --- | --- |
| AC1 | R1/R2，S1/S2 | 真实 Git worktree 拓扑经原 peer 观测入口形成 before，正常新增独立 peer 后原检查不误阻塞。核新增 peer bytes/模式与操作写集隔离；不以手造观测字典替代真实拓扑。 |
| AC2 | R2/R4，S3 | 既有 peer 指针/合法选择发生普通变化时继续拒绝错误恢复，原 preimage 不被刷新。复用仍适用恢复回归，不增加攻击/压力排列。 |
| AC3 | R3/R4/R5，S4 | 从原 owner 正常创建的固定事务经新兼容入口恢复；核同一 ref/public operation/plan/preimages/source bytes，无 reprepare 或备份扩张。实际 #766 原事务必须经该入口恢复成功。 |
| AC4 | R5/R6 | 定向 tools-owner/恢复回归、source/installed、dogfood drift、mode/sidecar；实际目标 own resolver/installed/native 通过。测试/源检查、真实本地恢复与 Release/外部采用分别报告。 |

完整多平台 clean-install/upgrade/Release 不在验收内。原业务问题 #766 的组件测试和交付仍由其本身负责，本 Task 不据此宣称它已完成。

## 8. 实际未决项

没有阻塞性产品范围问题。既有事务兼容入口的具体形态由当前 Delivery 规划和独立 Architecture 评估；必须完整满足 R3/R4，不能通过省略实际 #766 恢复来收窄完成定义。目前尚未实施修复或完成其验收。
