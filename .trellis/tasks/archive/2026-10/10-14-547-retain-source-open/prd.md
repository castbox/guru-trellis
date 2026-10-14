# #547：exact_source Task 完成后保留源 Issue OPEN

## 当前 authority 与身份

Direct Source：[castbox/guru-trellis#547](https://github.com/castbox/guru-trellis/issues/547)，读取日期 2026-10-14，正文更新时间 `2026-10-14T03:41:48Z`。
选定来源段落：目标与职责、范围、验收条件、边界与关联；角色为 requirement。
TaskId `547-retain-source-open` / generation 0 / source `exact_source`；执行与交付仓库 `castbox/guru-trellis`，交付目标 `main`。
当前 Architecture authority 是 `docs/architecture/README.md` 的 `.87`；当前运行安装仍是完整旧 Task planning 流程，不能以旧安装摘要中的 `.84` 替代 live authority。

来源设计约束及最终承接位置由后续 `design.md` 的唯一处置矩阵拥有；本 PRD 不复制其设计处置。

## 问题与目标

合法范围修订可让同一 Task 完成当前整体 accepted scope，而真实源 Issue 仍承担已在来源正文明确的保留责任；本现场为真实联调和产品 #59 联合验收。当前 Closure 将 exact_source 来源关系与必须关闭源 Issue 绑定，拒绝无关闭处置；Finish 缺有效 Closure ResultRef，无法正式归档。

源 Issue 中的现场为 CMS Task `1-normal-price-promotion` / generation 0：范围已收敛，Completion 返回 completed，而源 Issue #1 保留真实联调与产品 #59 联合验收责任。本任务修复 Guru 流程合同和对应执行路径，不修改该业务 Task，也不以受控测试声称现场已恢复。

目标是分离三个既有职责：Completion 判断整个当前 Task scope；Closure 判断并执行本次源 Issue 处置；Finish 消费真实结果归档与 bookkeeping。保持 TaskId、generation、真实 source 及各 owner。

## 功能需求

| ID | 所需行为 |
| --- | --- |
| R547-01 | 支持原 owner 完成正常范围修订后的当前 Task；不能通过改 source 为 reference_only/no_issue 或重建 Task 绕过死路。 |
| R547-02 | 区分来源本身无关闭资格与具有关闭资格、经本次语义审查保留 OPEN。exact_source 不能单独推出关闭动作。 |
| R547-03 | 保留 OPEN 的 Closure 产生有效 no-mutation 结果，不执行 Issue close；既有最小 ResultRef/TransactionRef 接续现有唯一 consumer。 |
| R547-04 | Finish 消费该结果，归档当前规划、交付历史和未验证边界；不重新决定 Issue 处置，不冒充 Cleanup 完成。 |
| R547-05 | whole-task Completion 门禁保持：必要工作或证据不足时仍返回原 remaining/evidence/revision/blocked 路由，不能为归档降低条件。 |
| R547-06 | 原 close、already-closed、reference_only、no_issue 及已支持的多 Issue action set 保持；正常 stale/mismatch 回原 owner，语义 blocked 原因不能被不适用的强制关闭条件覆盖。 |
| R547-07 | 同 owner 的 Closure/Finish 正常输出丢失恢复不重复 close、archive 或 bookkeeping；外部正常状态变化回原处置 owner。 |
| R547-08 | 明确 public API 的 additive/匹配 consumer 迁移合同；按当前 Task2/Delivery1 与完整旧安装的真实支持边界分别验证和报告。 |

## 验收与证据范围

| 来源 AC | 本任务可核验的结果 |
| --- | --- |
| AC1 | 通过正式 Task/scope owner 构造同 TaskId/generation 的正常 scope 修订，exact_source 保持，当前 scope 不再包含联调；正式 Completion 判断完整当前 scope并返回 completed。 |
| AC2 | 对该 Task 正式调用 Closure 的保留 OPEN 处置，得到有效 no_mutation ResultRef；provider 日志无 close，源 Issue 状态 OPEN。 |
| AC3 | Finish 用同一 ResultRef 完成归档/bookkeeping，源保持 OPEN；archive 保留真实 scope、历史和未验证界限；Cleanup 独立。 |
| AC4 | 既有合法 close、already-closed recovery、非 exact/no_issue 路径及多 Issue action set 回归；公共源关闭事实不能误取其它 Issue 的结果。 |
| AC5 | 尚有必要工作或证据时不能 Completion completed/归档；真实 source/scope/state 漂移回原 owner；blocked 语义原因可由原 consumer 接续。 |
| AC6 | 丢失 Closure 或 Finish stdout 后，原入口恢复相同结果，不重复 provider close、archive 或 bookkeeping；按实际测试层报告。 |
| AC7 | 定向 package/runtime、canonical、受控 dogfood/installed 与声明平台 projection、reapply/drift/sidecar 验证；实际旧安装采用与原业务恢复单列未验证。 |

基线：当前 Closure/Finish 原有 72 项测试通过，仅覆盖既有行为，未证明本次保留 OPEN 能力。
后续验证记录 admission、最初失败阶段、typed exit/classification、源 Issue 状态与 archive/bookkeeping outcome 五项观察。
受控 fake-provider 的完整调用链验证是流程集成证据，不是原 CMS 生产联调或恢复证据；不产生测试数量代替充分性的结论。

## 约束与非目标

- Markdown/Skill 拥有 source 处置与充分性判断；脚本仅记录、执行和校验客观事实。Finish 不成为第二 Closure owner。
- 使用官方 workflow marketplace、preset 与平台 projection；不修改上游、全局 npm 或 node_modules。
- 不新增长期 Issue scope ledger、授权存储、替代 Task/Delivery 模型、并行收尾 state machine 或无 consumer DTO 字段。
- 不修改业务实现，不关闭 CMS Issue #1，不自动升级业务仓库；原 owner 的实际迁移/恢复需独立运行其正式流程。
- 不启动 #548；不增加恶意伪造、锁、竞态压力或非常规 crash hardening；不执行完整累计多平台/Release 矩阵。
- 当前完整旧运行安装保持其已支持模型。新候选验证不自动授权把本 app checkout 或业务 installation 切换为 schema-2；匹配投影与未采用边界必须如实报告。

## 全 Task 完成定义

R547-01..08 与来源 AC1..7 的本仓库 accepted scope 均完成，定向验证和长期文档承接完整，真实提交交付经全 diff 独立 Review 与正式 Delivery 后，Completion 才能判断本 Task completed。
原 CMS 联调/产品 #59 联合验收和原业务安装恢复不是本 Task 的未完成工作，也不能被本 Task 关闭；软件 Release/完整矩阵保持独立未验证边界。
