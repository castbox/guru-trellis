# #443 Task Identity Session Binding Contribution

## Identity And Authority Boundary

- candidate identity: `architecture-contribution-443-task-identity-session-binding-v1`.
- lifecycle state: `reviewed_promoted`; absorbed by `current-main-0.6.17-guru.57`.
- source authority: closed Issue #443 and integrated committed range `a74d729ed84449ce603d112e277fa567e87a7bf3..4dd9f7b7d4df2167819745565225001355adb5ee`.
- task locator: `.trellis/tasks/archive/2026-09/09-19-443-task-identity-binding`.
- related RDT contribution: `docs/requirements-design-test-contributions/443-task-identity-session-binding/`.
- source/expected baseline: `docs/architecture/README.md` / predecessor `current-main-0.6.17-guru.56`; current successor `current-main-0.6.17-guru.57` / `active`.
- design constitution: `docs/architecture/00-foundation/design-constitution.md` / `guru-trellis-design-constitution-v1` / `current`.
- project change contract: `docs/architecture/06-governance/change-contract.md` / `guru-trellis-architecture-change-contract-v1`.
- change path: `target_native`.

## Scope

本 contribution 只定义 task identity-centered session binding capability，作为 #434 全局生命周期切换的前置能力。它不激活 #434，不创建第二 task ledger，不修改上游 Trellis task 状态集合，也不拥有 Completion、Finish、Cleanup 或 Issue closure。

## Authority and ownership

- `task.json`、task artifact locator、live branch/worktree、repository common dir 与 task/workspace mappings 是 task/workspace identity authority。
- `.trellis/scripts/common/active_task.py` 与 `session_storage.py` 是现有 session resolver/store；`guru-bind-task-session` 只在其上增加 lifecycle-aware binding projection，不复制 resolver。
- 新 package 是 session binding/rebind/switch/resume 的唯一 writer/validator。
- #438 保持创建期 attach owner；#436 保持 Reactivate generation、Finish/Cleanup receipt owner；#434 后续消费 public exits 与 route projections。

## Binding contract

每条 official ignored runtime mapping 绑定：`session_id`、`task_ref`、`task_id`、workspace path、branch、base branch、task HEAD、lifecycle generation、current route 与 freshness。binding 丢失时，当前 session 必须重新读取并验证完整 identity；任一 task/repository/workspace/branch/base/mapping/session/lifecycle mismatch 均 zero-write stop。本 capability 不创建重复的 binding store。

同一合法 binding 重试返回同一 binding identity，不创建第二记录。Reactivate generation 变化时，旧 generation binding 不可用于当前 route；Finish/Cleanup receipt 仍由各自 owner 校验，session binding 不得绕过它们。

## Architecture path

`target_native`。新 package 以 Interface 1.4、独立 schema、五个成功 exits 与一个 blocked exit进入target boundary。未建立legacy dual-read/dual-write，也未改变production workflow graph。shared authority已由expected `.56`串行提升为`.57`；promotion-created combined diff仍需fresh Phase 2、Task Commit与完整Branch Review，#434仍独占后续cutover审核。

## Validation boundary

本 contribution 的最小验证包括 package contract/runtime、A→B→A、跨 session rebind、Reactivate generation invalidation、mismatch zero-write、canonical/installed/platform projection、ownership 与 dogfood drift。完整 Release matrix、#434 production graph activation 和生产业务操作不属于本 contribution。

## Project Check And Promotion

- check identity/version: `guru-trellis-architecture-convergence@1`.
- refs: `ARCH-GOV-006..011`, `ARCH-GAP-009`, `ADR-005`, `ADR-013`.
- before: `.56`包含31 packages / 136 exits / 101 commands及22-invoke / 98-exit production graph，缺少#443 current authority。
- after candidate: canonical与managed projections包含32 packages / 142 exits / 102 commands；`guru-bind-task-session`为active/deferred，production graph保持22/98。
- current evidence: integrated range已进入main；当前canonical package 26 tests PASS，installed interface/runtime与canonical bytes一致，live count与workflow markers匹配。
- promotion state: `reviewed_promoted`; shared current is `current-main-0.6.17-guru.57`.
- expected current identity: predecessor `current-main-0.6.17-guru.56`; promoted successor `current-main-0.6.17-guru.57`.
- ADR: `ADR-014`，因为本capability建立stable task identity、session binding single writer、base provenance与generation invalidation的持久owner边界。

## Review Boundary

本promotion不把当前#452 OpenCode/platform扩展倒填为#443历史证据，也不证明#434 activation、完整Release
matrix、生产binding或任何远端mutation。combined diff必须重新通过fresh Phase 2、Task Commit与independent
complete Branch Review；后续Publication、push、PR、merge、tag、Release与Issue closure保持独立门禁。
