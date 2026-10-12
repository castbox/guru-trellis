# ADR-022：唯一 Planning writer 与两目的 Architecture

- 状态：`accepted`；来源：#292 design D9/D10，经[durable contribution](../contributions/292-unique-planning-author.md)承接。
- 继承：ADR-005 的 expected-current promotion、ADR-011 的唯一 continuation、ADR-019 的独立评估方法及原 lifecycle owners。

## Decision

`guru-author-task-plan` 独占 Task PRD/design/implement 的规划语义写作及已有 revision。Clarify 拥有 scope/来源意图，Discovery 拥有 context evidence，Wording 拥有受控措辞审查，Approval 拥有独立批准。原 normal/solution/root owners 通过 author_candidate_set 判断当前候选，Approval 保留原 planning_scenario_set。

同一 Architecture owner/stage 使用目的专属 planning3.0。candidate_assessment 在真实候选上判断，不要求未产生的 contribution/promotion_state；其 current 输出供 Author solution_planning 使用。final_plan 读取 Wording-current design 与真实 contribution/必要 ADR，绑定 reviewed_candidate 或合法 reviewed_promoted，仅供相邻 Approval 使用。前置输出不能当最终结果；sync 仅在当前调用保存 purpose，不另建 owner 或 store。

Wording change refs、Approval revision actions 与 Delivery/Completion 的适用原因通过薄显式 projection 回同一 writer。批准后由原 execution owner 承接首次 activate 或活动 resume_execution；TaskId/generation、Task metadata writer、终态与 promotion owners 保持。

## Alternatives and consequences

Approval 兼 writer 会破坏独立门禁；第二 prewrite Architecture owner 会重复责任；沿用 contribution 必填会阻断正常首次无文档规划；保留无 purpose planning2.0 fallback 会产生歧义回程。当前必要职责由单一 writer 和两种明确目的承接，八 profiles/四 exits 对应真实 callers，不预留 future capability。

canonical workflow/preset 与所有受控 consumers 匹配迁移；旧 planning2.0 runtime 退出，中断旧调用 fresh Author 重入。合法非 Planning/maintenance2.0 与历史 validation assets 保持原语义。无 constitution 例外、第二 authority、长期规划 cache、授权存储或 GAP lifecycle 增量。软件发布与完整矩阵仍由原独立 owner 验证。
