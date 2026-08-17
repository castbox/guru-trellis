# #251 修复 Finalizer post-bind same-plan 恢复与 legacy closeout-plan 归档缺口

## Goal

让 current Finalizer 在一个已由 owner-private schema 3.0 transaction 绑定唯一 PR、完成 publication push 且进入 `archive` 或更后阶段的 same-plan recovery 中，优先恢复该 transaction，而不是重新执行 pre-PR provenance 判断；同时为历史仍被 Git index 跟踪、但 current Finalizer 不再持久化的 `closeout-plan.json` 提供唯一确定性的退休迁移，使 archive、terminal recovery 与 `ready_for_merge` 闭环一致。

## Background And Authority

- Live authority 是 GitHub Issue #251 当前正文；该 Issue 无评论修订。
- 基线为 `main@ad7a1a6a227278b5c7710c6fb7b5567f4db72875`，已包含 #220 和 #253。
- 真实业务拓扑中，业务 reviewed HEAD 与 `.trellis/guru-team/extension.json` 的外部 Guru Trellis source commit 按设计不同；该差异不能触发业务 Finalizer 的 provenance/verifier route。
- Current Finalizer 的 owner-private transaction 已包含 `mode=existing_pr_recovery`、绑定 PR、pre-push HEAD、publication HEAD、Publication payload、close scope 与 `next_transition`，这些事实是 post-bind recovery 的阶段 authority。
- Current preparation 使用 `include_closeout_plan=false`；`closeout-plan.json` 已由 #180 从 current tracked handoff 退休。历史任务仍可能在 Git index 中保留 schema 1.x/2.x 文件，但工作树已删除。
- 完整 Throwaway initial install、workflow preview/switch、official update、preset reapply、全平台与 tag-pinned smoke 由 Release Gate #254 统一执行，本任务不得运行或声称通过。

## Requirements

### R1. Post-bind transaction 优先恢复

1. `finalization_preview_context` 在 pre-PR provenance reprepare 之前识别与 rebuilt plan 完全匹配的 current `existing_pr_recovery` transaction。
2. 当 transaction 已绑定唯一 PR，且 `next_transition` 为 `archive`、`push_archive` 或 `mark_ready` 时，不调用 `finalizer_pre_pr_provenance_tail_required`，不把 state 改写为 `reprepare_required`。
3. Preview 保留 `publication_mode=existing_pr_recovery`、exact adopted PR identity、初始 Draft/Ready 状态、pre-push HEAD、publication HEAD、剩余 transition 与是否仍需 push/metadata/Ready 动作。
4. Plan digest、Publication payload、PR、Issue close scope、local/remote/PR HEAD 或 transaction identity 任一漂移仍 fail closed。

### R2. Pre-PR provenance 边界不扩张

1. `provenance_tail_required` 只适用于未绑定 PR、尚未开始 archive 的真实 pre-PR current state。
2. 外部 Guru Trellis installation source commit 不得被要求等于业务仓 reviewed-content commit。
3. 本任务不重新引入 `guru-verify-extension-installation`、`verification_required`、provenance metadata tail、Branch Review 回退或新 publication HEAD。

### R3. Legacy tracked closeout-plan 唯一退休迁移

1. 选择“受控 projection 退休”策略：current Finalizer 构建新 plan 时，从 current `move_paths`、`tracked_move_paths`、reviewed bindings、transaction paths 与 archive retained paths 中排除历史 `closeout-plan.json`。
2. 历史 index entry 的删除必须作为 current archive transaction 的确定性删除集合处理，而不是要求工作树恢复或 materialize 旧/current plan。
3. Archive 前后 continuity、commit path、archive move、terminal recovery 与 cleanup 对该退休策略保持一致。
4. Archived current transaction 不因 archive 中缺少或存在历史 plan 而误判；current successful archive 的规范结果是不保留 `closeout-plan.json`。

### R4. 真实拓扑回归

1. 增加 focused fixture：业务 reviewed HEAD 与外部 extension source commit 不同。
2. Fixture 包含 schema 3.0 `existing_pr_recovery` transaction、唯一已绑定 Draft PR、remote/PR HEAD 等于 publication HEAD、`next_transition=archive`。
3. Fixture 包含历史 tracked schema 1.x/2.x `closeout-plan.json` index entry，工作树为删除/未 materialize 状态。
4. `same_plan_resume` preview 必须返回 gate-compatible `resume_finalization`，不返回 provenance reprepare。
5. Executor 完成一次 archive、一次 archive commit/push、一次 Draft-to-Ready，并验证 local/remote/PR HEAD 一致；terminal invocation materialize `ready_for_merge` 并清理 owner-private transaction/gate。
6. 漂移、任意 Open PR、未绑定 equal-head 或跨 task identity 继续 fail closed。

### R5. Canonical 与安装投影

1. Canonical 修改以 `trellis/skills/guru-team/packages/guru-finalize-task/**` 为 SSOT。
2. 同步 installed dogfood 与 shared/Codex/Claude/Cursor copies，不手工把生成副本当源头。
3. 更新受影响的 Finalizer contract、durable workflow/preset specs、tests/evals 与必要 README；不改变 public Skill id 或六个 typed exits。
4. 运行 preset apply、dogfood overlay drift、ownership/parity、零 `.new/.bak` 检查。

## Acceptance Criteria

- [ ] Post-bind same-plan recovery 在 provenance 判断前恢复 current transaction。
- [ ] Preview 保留 `existing_pr_recovery` 与 exact PR/HEAD/payload/scope identity，只报告剩余 transition。
- [ ] 外部 extension source commit 与业务 reviewed HEAD 不同不会触发 provenance/verifier route。
- [ ] 历史 tracked `closeout-plan.json` 通过受控 projection 退休，不要求恢复、materialize 或手工删 index。
- [ ] Archive、archive push、Draft-to-Ready、三方 HEAD 与 terminal `ready_for_merge` focused regression 通过。
- [ ] PR/remote/plan/payload/close scope/HEAD 漂移继续 fail closed，不采纳 arbitrary push 或任意 Open PR。
- [ ] Canonical、installed、shared/Codex/Claude/Cursor、contract/spec/tests/evals 同步。
- [ ] Focused clean installed-package recovery smoke、受影响 package/runtime/integration tests、overlay drift 与零 `.new/.bak` 通过。
- [ ] 完整 Throwaway installer、initial install、workflow preview/switch、official update、preset reapply、全平台/tag-pinned 发布矩阵未执行，并明确由 #254 承担。

## Out Of Scope

- 不修改 Afizzy 文档、产品代码、PR #38、Issue #30 或其 worktree/transaction。
- 不创建第二个 PR，不关闭业务 Issue，不执行真实业务仓 archive/Ready/merge/cleanup。
- 不放宽普通首次发布必须无未绑定 Open PR的合同。
- 不修改公共 typed exit 集合，不新增跨 Skill handoff、tracked closeout plan 或授权 artifact。
- 不执行完整 Throwaway installer 与 #254 拥有的累计发布门禁。

## Open Questions

无。Issue #251 已明确 recovery、迁移、验证与 Release Gate 边界；实现选择由 current Finalizer 私有 transaction 和无 tracked handoff 的现行合同确定。
