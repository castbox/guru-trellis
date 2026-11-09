# D2 正常 peer 退出后的原事务恢复需求

## 1. 整体来源与术语

本批消费[整体 PRD](../../prd.md) 当前 accepted_scope，选择 R2、R3、R4、R5、R6 与 AC2、AC3、AC4。Direct Source 仍为 [Issue #769](https://github.com/castbox/guru-trellis/issues/769) 的目标与行为、范围与兼容边界及验收。没有新的 Task、来源或整体范围。

本批 DeliveryKey 为 `769-tools-peer-growth-recovery / 0 / 2b62b86b-ab9c-415d-9cfc-87ec5141e8d0`。存续 peer 指仍存在、仍需保持其原指针和合法选择的 checkout。退出位置指其原 owner 已正常结束使用并移除的位置；目录或观测缺失本身不证明退出合法。

## 2. 整体与本批目标、非目标

整体目标仍包括实际 #766 原操作恢复。D1 已交付新增 peer 处理、冻结源恢复入口与分发，但真实恢复在存续检查处被已经退出的 #759 位置阻塞。D2 补齐这个剩余适用性边界，并继续同一原操作。

保留整体非目标。不得恢复已完成的 #759 worktree、重新 prepare、修改原 peer 快照或备份、放宽存续 peer 的真实变化拒绝。不得自动 prune、清理其它位置、推断 Task 完成或增加通用资源生命周期平台。完整多平台安装、升级与 Release 矩阵仍不属于本批。

## 3. 本批起点、前序结果、依赖与剩余责任

D1 为 `638e1a19-c4cc-46da-8157-e19293774730`，已通过最终 Check、独立完整 Branch Review 和三平台 Targeted native CI，经 [PR #776](https://github.com/castbox/guru-trellis/pull/776) 合并为 `4b92335054fd5d6cb9de9844110ba01d56a3f00a`。其实际交付 head 为 `aaf7f939e83c5a5230ecbb9d9f0827fd5c2e97ff`，是本批内容基线 B 与起始 H0；PR 目标仍为 main。D2 不重复交付 D1。

交付后调用 `recover_frozen_source / resume`，原 recovery_ref `05d804ba-1a5d-4975-93bd-9909ff00e719` 返回 blocked。实时差额只有 #759 原位置的五个键不再被枚举：两个原本缺失的 active pointer、原本存在的 selection-v3，以及 installed/source runtime 观测。其原目录、gitdir 和 Git 注册均已不存在。现已找回原 Finish `success` 与 Cleanup `cleaned` 输出，并通过原 Cleanup 入口只读恢复同一个 `cleaned` 结果，Task 为 `TASK-759-PRUNABLE-PEER / 0`。正常退出依据与当前缺失事实分别成立，不能只靠后者认定合法。

原 source 仍为 #766 checkout，HEAD `8d97fe5401345180ce294e2f729ec33071b37f62`。原 public operation 仍为 `8838ed00-b7c3-4ab3-97cd-0fd392e0740b`。D2 必须保持这些固定输入及原 plan、preimages、peer snapshot；恢复成功后 #766 自己的质量和交付仍由其原 Task 承接。局部 source token 由原 tools owner 从自己的冻结输入校验，不复制到规划或公共 handoff。

## 4. 本批调用方、场景与流程

- D2-S1：原 tools owner 有冻结事务；另一个 peer 的原 owner 正常退出并删除其位置。恢复 owner 先核实际退出依据及原对象边界，再继续原事务，不把退出对象的观测消失误报为存续对象改值。
- D2-S2：某个原 peer 仍存续，其指针或已成立合法选择普通变化。原保持拒绝继续生效；D2-S1 不能掩盖该变化。
- D2-S3：只有位置或观测缺失，退出依据不完整，或位置仍注册、仍存在、与目标不符。原 owner 报告具体缺口，不自行推断退出、不扩大例外、不写改其它 peer。
- D2-S4：从已交付完整修复源恢复实际 #766 同一 ref/action。原阶段、public operation、资产源、计划及备份保持；目标自身 installed/runtime/native 结果独立成立。

## 5. 完整行为、条件与约束

- R2/AC2：区分存续对象与原 owner 已正常退出的位置。存续 peer、common 状态及不属于已核退出对象的原保持条件继续执行。不能以减少错误键数替代对象判断。
- R3/AC3：提供原冻结操作的明确支持路径，继续复用 D1 原恢复 engine。不得刷新快照、扩大备份、吸收后来的业务修改或创建第二恢复事务。
- R4：AI 拥有正常退出及适用性的判断。确定性代码只校验其有直接 consumer 的身份、对象和状态事实；路径存在性、Git 枚举或 OS 原语不得替代业务判断。原 source、owned 内容及其它真实 mismatch 继续阻塞。
- R5：原 owner 的退出结果、原事务身份保持、实际目标自身 resolver/installed/native 分别取证。工具恢复成功不代表 #766 或 #769 已完成。
- R6：若输入或重试 handoff 需要调整，成套维护精确 schema、Interface、consumer、示例和兼容合同；字段必须有直接 consumer。保留既有未使用新能力时的含义，不加入授权字段或长期退出台账。

具体候选机制由 Author qualification 与独立 Architecture 评估；本 PRD 不预先接受一种实现。D1 的正常新增 peer 处理和 #759 的 `prunable && .git lexically absent` 精确边界均继续成立。

## 6. 本批验收、验证方式与未决项

| AC | 要求/场景 | 入口与可观察结果 |
| --- | --- | --- |
| D2-AC1 | R2/R4；D2-S1/S2/S3 | 用真实 Git peer 与原观测入口建立冻结输入，正常退出后经公开恢复入口继续。核原快照、计划、备份不变；存续 peer 普通变化仍拒绝，依据缺失不能自动放行。 |
| D2-AC2 | R3/R5；D2-S4 | 修复交付后，实际 #766 原 ref/action 恢复成功；核同 public operation/source/plan/preimages，并读目标自身 installed/native。组件测试不能替代该现场结果。 |
| D2-AC3 | R5/R6 | 命中 package/恢复回归、source/installed、真实目标更新、drift、mode/sidecar；原未变执行事实可按适用性采用。重试仍消费同一操作及本次必要输入，无新状态机或新备份。 |

产品范围没有新的未决选择。退出的原 owner 依据已取证；候选机制仍需在 Author qualification/Architecture 边界完成判断，未完成前不写成已通过。本批合并后实际恢复仍是整体 Completion 的必要条件。

## 7. Canonical 引用与本轮差额

沿 D1 已晋升的 `docs/{requirements,design,test}/current/runtime-location.md` R769/D769/T769，以及 `docs/architecture/01-current/runtime-location.md`、`docs/architecture/adr/tools-frozen-source-recovery.md`。这些当前正文仍约束实现；正常退出边界的窄差额由原 RDT/Architecture owners 评估并按适用路径维护，不直接改共享导航。

实现与接口承接原 `guru-upgrade-tools` package 的 peer 观测、same-operation/frozen-source 恢复及 `MIGRATION-769.md`。测试层级和停止条件沿 quality-guidelines 的 Test And Validation Value / Validation Scope Ownership；写作及脚本职责沿 clear-technical-writing、companion-scripts 和 workflow-contract 的 Candidate Applicability And Coverage。
