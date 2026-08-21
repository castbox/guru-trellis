# ADR-005: Architecture lifecycle one-way convergence

- 状态：`accepted`。
- 来源：Issue #283 reviewed Architecture contribution 的 `ADR-283-CANDIDATE`。
- predecessor：none；successor：none。

## Decision

采用“Guru Team 方法论 identity + 项目 Architecture Baseline/change-contract identity”的双维合同，唯一交叉点是 task-local Architecture change contract。每个标准 task mandatory 进入 Architecture semantic owner；architecture impact 选择且只选择 `target_native`、`legacy_boundary_convergence` 或 `dedicated_refactor_slice`。

普通 task 只写自己的 contribution 与必要 ADR candidate。shared current 由唯一 Architecture owner 在 independent committed-diff review 后，绑定 expected current identity 串行 promotion；live current 推进时旧 task 必须 `sync_required`。promotion 产生的 shared-current diff重新进入 Phase 2、task commit 与独立 full-diff Branch Review，之后 Publication/Acceptance 才可消费 `reviewed_promoted`。

## Rejected directions

- 由 schema/runtime 或固定测试数量决定架构充分性。
- task 在 review 前直接修改 shared current，或两个 task 竞争同一 GAP/owner/current file。
- 保留 Architecture 1.0 dual-read、adapter 或第二 authority。
- 把设计宪法五原则复制成公共逐项 score/verdict checklist。

## Consequences and boundary

Architecture owner 与项目 authority 各自保持单一职责；缺失适用 evidence 会 fail closed，并行 task 在 current 推进后必须 re-entry。#283 不实现业务仓库重构、#248/#252 owner 或 #267 release；extension candidate 仍为 `0.6.5-guru.37`。
