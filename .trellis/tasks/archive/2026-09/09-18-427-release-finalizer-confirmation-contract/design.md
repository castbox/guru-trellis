# Design

## Current Conflict

`release-guru-trellis-version` 当前把 Finalizer 的 branch push、PR creation、archive/Ready
建模为三个必须即时确认的动作；current `guru-finalize-task` 只提供一次 read-only preview、
一次 exact transaction confirmation 和一次连续执行完整 transaction 的 public Happy Path。
两者无法同时满足。

## Chosen Design

1. 将 release owner 的 Finalizer 确认行收敛为一个完整固定 transaction：provenance
   reprepare、content push、Draft PR binding/creation、archive、archive push、Ready。
2. 明确该确认仅授权展示的 Finalizer transaction，不授权后续 Merge。
3. 保持 Merge、annotated tag、tag-pinned smoke、GitHub Release、Issue closure 和 cleanup
   现有独立行与即时确认语义。
4. 修改仓库私有 Skill canonical 文件及四个平台 projection；不触碰公共 Finalizer package。
5. 更新 contract regression，使其同时断言“一次 Finalizer confirmation”和“其它边界仍独立”。

## Compatibility

- 不改变任何公共 Skill ID、schema、typed exit 或 consumer。
- 不改变 Finalizer transaction 内容和恢复语义，只修正上层 release orchestration 的确认数量。
- Release owner 仍拒绝笼统授权；每个独立 mutation boundary 必须展示精确目标与命令。

## Validation

- Release Skill focused unit/contract tests。
- Canonical/dogfood/platform projection parity 和 source/installed validators。
- Preset reapply、dogfood drift、ownership、sidecar/residue、`git diff --check`。
- Phase 2 semantic check 与完整 committed diff Branch Review。
