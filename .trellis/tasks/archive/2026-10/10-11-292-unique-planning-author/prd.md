# #292 Phase 1 唯一 Planning Author 与来源设计承接集成

## 目标与需求来源

让 Guru Team 的真实 Phase 1 由唯一 `guru-author-task-plan` 收敛需求、承接来源设计并写作三份 planning docs 和官方 planning JSONL；Architecture、Wording、Approval 保持独立职责，正常入口及恢复均进入这条可执行链。

Direct Source：[castbox/guru-trellis #292](https://github.com/castbox/guru-trellis/issues/292)，当前审阅正文 `2026-10-10-r27`。每次受影响阶段重入均 fresh 读取 live 正文及明确引入的 authority；本文件不是冻结来源版本的许可。来源设计处置只在 [design.md](./design.md) 记录，执行与验证安排只在 [implement.md](./implement.md) 记录。

## 当前事实与问题

2026-10-11 的创建基线为 main `44a8b9c1f8495e2f811f892f248a1f2693a8bc80`，RDT `current-main-0.6.17-guru.84`、Architecture `current-main-0.6.17-guru.83` 均 active。软件与 target Trellis 以当前 source lock/installed manifest 为准，不以全局 PATH CLI 为验证对象。

现有 Phase 1 提及未命名 planning writer，Architecture planning 只有一个回程；当前 registry 尚无 Author package。#250 已拥有 Intake 意图、来源角色与澄清；#468 已拥有活动重规划的 `resume_execution`；Delivery/Completion/Closure 和 shared authority promotion 已有独立 owners。需要补齐的是唯一 writer、来源设计的显式落点、两个 Architecture 调用目的、实际入口激活及行为证据。

## 需求

| ID | 可观察要求 |
| --- | --- |
| R292-01 | 三份 planning docs 与官方 planning JSONL 的业务语义由 Author 独占；Wording 只做自身合同内受控措辞修改，Approval 独占批准。 |
| R292-02 | fresh 读取 Direct Source、选定 comments、明确引入的 requirement/design authority、当前 docs 与 repo evidence；规范性接口、机制、顺序、owner、兼容承诺不能被当建议丢弃，建议也不能自动升级为约束。 |
| R292-03 | design.md 对每项 load-bearing 来源设计记录具体 locator、原承诺、retain/change/reject、当前落点、理由/影响与适用上游处理；没有设计承诺时给出依据。prd/implement 不重复矩阵。 |
| R292-04 | 八个 Author profiles 分别拥有闭合 input/exit/consumer：initial_review、active_task_scope_change、wording_reentry、approval_revision、delivery_plan_revision、requirements_revision、solution_planning、architecture_conflict_resolution。 |
| R292-05 | 实际链为 requirements_convergence → requirements_ready → 前置 Architecture → solution_planning → plan_ready → Wording → 最终 Architecture → Approval → 当前展示/对话接受/pair guard → activate 或 resume_execution。 |
| R292-06 | 同一 Architecture owner 区分前置候选评估回 Author 与最终判断直接回 Approval。前置结果不能跨 Author/Wording 重放为最终结果；最终结果不能回 Author 形成循环。sync/bootstrap/repair 重入原调用目的；冲突、regression、blocked 保持原含义。 |
| R292-07 | Create Task/current Phase 1、正常 start/prompt/continue/resume、真实压缩恢复，以及 no-PRD、PRD-only、design-only、three-doc、official seed、partial/stale docs 均可达唯一 Author 或正确 resolution/stop。identity mismatch 不创建替代任务。 |
| R292-08 | “讨论方案”“设计新功能”“先做规划”三种正常提示触发/加载 brainstorm 后，仍由 Guru owner 写作并完整经过门禁；不重复已完成澄清、不增加例行 planning consent、不重置 identity。真实新需求选择仍回 Clarify。 |
| R292-09 | requirements convergence 不为适应当前 Architecture 静默修改需求。第一次 substantive design/implement 写入前，Architecture 对真实候选作当前评估；最终判断基于 Wording 后当前事实，按原独立评估合同决定适用性与必要新评估。 |
| R292-10 | 唯一 Delivery Policy 在 implement.md：full 默认；partial 明确独立 slice/remaining work/Completion 条件；staged 明确顺序、当前 stage、entry/exit、remaining stages 与最终条件。Docs SSOT Plan 保留四策略及原 RDT owner。 |
| R292-11 | Delivery Review policy 缺口与 Completion 下一次独立 Delivery 规划保持两个 router 和不同 revision reason。Completion remaining_work、evidence_pending、requirements_revision_required、implementation_revision_required 保持原直接 consumer；不是所有出口都重规划。 |
| R292-12 | current normal-scenario、solution-mechanism、适用 root-cause qualification 与 #383 因果完成语义保留；来源/scope/policy/Architecture 变化仅失效依赖结果，从最早受影响 owner 恢复。 |
| R292-13 | approved active replan 通过 #468 的原展示/接受/pair guard 和 resume_execution 返回执行；TaskId/generation/branch/checkout/status 不变。实现修正和证据补齐若不影响 planning authority，保留原 Phase 2/Delivery/Completion ingress。 |
| R292-14 | canonical/dogfood/installed registry/interface/workflow、声明平台 projection 和 apply/reapply/drift 一致；旧竞争 Phase 1 edge 退役，未知/multiple/unmapped exit fail closed。 |
| R292-15 | public I/O 只含直接 consumer 所需最小 handoff；脚本不能解释来源承诺、决定设计/批准/route。无第二设计 SSOT、重复矩阵、授权记录、ledger、shared cache 或无人消费字段。 |

## 验收标准

| ID | 对应需求 | 必需证据 |
| --- | --- | --- |
| A292-01 | 01/04/14 | Author 实际写作/正式出口及 registry/workflow/安装投影闭包，证明唯一 writer 已激活。 |
| A292-02 | 07/08 | 新装及现有安装 update/reapply 后的真实正常提示、上述 docs 状态和 start/continue/resume/compression；brainstorm 加载本身不判失败，独立绕行才判失败。 |
| A292-03 | 02/03 | 来源承诺及逐项处置/落点可见，Approval 逐项核对；不依赖 #250 未来 DTO/矩阵。 |
| A292-04 | 05/06 | 同一任务实际 public-wrapper 串联及 native 行为，两个 Architecture return 可区分，最终 result 相邻交给 Approval，无首次规划循环。 |
| A292-05 | 09 | 正常 pre-write、候选变化 fresh 评估、七个 Architecture 出口、task-local proposal/必要 ADR 与既有 promotion 边界。 |
| A292-06 | 04/11/13 | Wording content_changed、Approval revision、两类 Delivery planning reason、Completion 各适用 owner、scope/source revision 和真实恢复；独立 Phase 2 ingress 未被吞并。 |
| A292-07 | 10/12 | full/partial/staged、Docs 四策略、三 qualification owners 和因果证据语义保持。 |
| A292-08 | 02/03/12 | 去敏技术 Issue 同时含需求与 A-D 设计：retain 有落点；正常遗漏不能通过 Approval；change/reject 有理由和适用上游处理；source 更新只重做依赖阶段，技术细化不过度提问。 |
| A292-09 | 15 | 对新增 DTO/状态/文件的直接 consumer 审查，确认没有上述重复 authority/持久化。 |
| A292-10 | 14 | source/dogfood/installed、声明平台、apply/reapply/drift 和定向验证通过，未验证边界真实披露。 |

package-only、schema-only、局部 eval、文件齐全、规划批准或单次 PR merge 都不能证明本 Issue 完成。关闭必须具备实际 planning activation 与上述行为证据，沿原 Completion/Closure/Finish owners 执行。

## 范围与约束

仅交付 #292；#453 → #396 → #250 为前序背景，#521 不启动。可以修改必要的 canonical Author、受影响 planning workflow/projection/平台/preset 和对应 docs/tests；不接管 Phase 0、创建/checkout、Check/Commit/Branch Review、Delivery/Completion/Closure/Finish/Cleanup、promotion 或 Release owner。

遵从官方 marketplace/preset 扩展面；不 patch/delete upstream trellis-*、hook、上游源码、全局 CLI 或 node_modules。只处理诚实正常路径、普通 omission/stale/mismatch 和 accepted 恢复；不新增 hostile-input、锁/TOCTOU/stress/fault injection 范围。保留 secret redaction、权限与副作用确认。

最多一个必要的代表性 clean throwaway；完整多平台 installer/upgrade/Release matrix、软件发布、部署及业务仓安装保持专门 owner 的未验证边界。真实压缩或必要 native 入口无法执行时列为对应验收缺口，不能以模拟或 package tests 改称通过。

当前无未决产品/scope 选择；技术方案仍需 current Wording、独立 Architecture 和 Planning Approval。创建确认不等于规划接受或任务激活。
