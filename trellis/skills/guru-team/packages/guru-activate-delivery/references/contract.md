# Delivery Activation 1.0

`judgment_mode=semantic`，完整五阶段 profile；workflow/standalone 相同 entry。Task 只保留 identity、整体 scope 与完成责任。D1、D2 和同 Delivery 返工采用同一个 Activation，不读取或写 Task 开发 status。

## 当前计划展示与合法 writer

读取明确 DeliveryKey、公共 scope_ref/planning_root、三份中文文档，以及实际邻接 Approval 的 approved DTO。Approval 的 `planning_result_id` 是仅用于本邻接 consumer 的文件 freshness token；必须消费真实返回值，不能由当前文件自行计算一个 token 代替之前批准。

AI 审查当前 owner/source、切片与整体约束、session/checkout 和基线连续性。完整计划经过当前 workflow 的人类可读展示及当次接受后才能记录公共 Planning。此前 creation 确认不等于接受未来计划；当前对话已接受同范围计划不重复询问。无授权字段、接受时间/来源/摘要或过程进入任何 DTO/checkpoint/evidence。

官方 resolver 无 context key 时，使用原输入明确 DeliveryKey 经原 projection 的 current generation/C4/公共record校验；不要求或写入不适用的session。具备key时必须匹配官方current，missing/stale/其它current不进入fallback。其余Planning freshness与合法公共转换条件保持。

调用 `delivery_activation(action=activate)`，确定性 validator 核验三份文档的局部 freshness 与明确 selection。只有本 Skill 占用公共 `planning` role；在公共 planning 阶段调用 `record_gate`，生成独立 `planning-accepted:<UUID>` result_id，绑定实际 scope_ref、plan_ref、文档 evidence，candidate/predecessor 为公共 role 的空值。公共 store 拥有阶段和合法转换；本 Skill 不维护第二状态机。

Guru freshness token 不写 GateResult.result_id、不成为 evidence 或跨阶段 authority。公共 receipt 的原 result_id 以 `planning_accepted_result_id` 交实施；Check predecessor 消费此公共结果。

## 返工、失效与恢复

原当前阶段 owner 先完成合法 rework 到 planning，再由唯一 Author 修订该 Delivery 文档、受影响 Wording/Architecture/Approval fresh 重入。保留同一 key/candidate/commit/PR，未受影响证据不整链 replay。整体 scope 修订先由 Clarify 收敛，再让最早受影响阶段 owner 接续。

公共转换前的 ignored checkpoint 只保留同 operation/key/result 的恢复输入；同 owner 重试必须用原 result_id。转换及输出校验后删除 checkpoint。`recover_activation` 从当前公共 planning slot 读回该原 key/result，校验同 scope 和当前文档；它不重复 record_gate、不新分配 result、不从 phase 推导批准。尚未转换或原结果不可用时回原计划展示/接受路径；新内容不允许旧结果冒充当前 pass。历史完成事实由公共查询保存，本恢复结果不覆盖后续语义义务。

## Typed exits

- `delivery_started`：key、task_ref、公共 planning_accepted_result_id 交 `guru-delivery-started-router`。
- `planning_refresh_required`：key/task_ref 交 `guru-delivery-activation-planning-router`；定位最早受影响 Planning owner 后，使用真实来源结果重入 Approval，不编造 planning_ready。
- `invalid_delivery_state`：明确身份/状态错误，停止。
- `blocked`：安装、session、公共 API 或所需事实缺失，停止。

无法读取安装端公共 API 时拒绝调用，不从上游源码或另一 model fallback。旧 `guru-activate-task` 及其 activate/resume_execution/status writer 在新 distribution 退出；旧安装未达到 D2 切换条件时仍使用其固定完整旧发行。

`delivery_scope_withdrawal` is this same planning owner's separate semantic
entry for full slice withdrawal. Reread current whole-Task authority and the
selected Delivery before deciding stop; consume Clarify scope_action only as
route intent. Use the installed public stop/release with fixed planning role;
recover the same stop result after stdout loss. `delivery_stopped` projects only
TaskRef/TaskKey to `guru-review-task-completion`; it is never delivered or completed.

## Current-stage scope revision

`delivery_scope_revision` is this existing owner's semantic re-entry after original
Clarify has published the changed whole-Task scope. Read actual accepted scope,
selected Delivery and obligations; review the retained slice anchors and original
source_selection/revision_refs. Complete the AI gate before invoking this profile.
Do not require stale Planning/Check/Review/Readiness evidence to revise scope.
Project only the reviewed current scope_ref through upstream rework to planning;
invalidate planning/check/full_review/readiness and retain identity, candidate and
historical publication/delivery facts. No new acceptance or approval is inferred.
`delivery_scope_revised` goes only to guru-delivery-scope-revised-router and the
same Delivery Author active_task_scope_change. A retry after lost output reads
matching public scope, planning phase and cleared results; it returns the same
minimal handoff, without replaying rework or installing an approval token.
A new change receives fresh original Clarify and this owner judgment.
