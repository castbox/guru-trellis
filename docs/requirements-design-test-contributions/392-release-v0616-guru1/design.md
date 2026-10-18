# #392 Release v0.6.16-guru.1 Design contribution

状态：`reviewed_promoted`；change path：`target_native`。immutable superseded
predecessor 为 `current-main-0.6.5-guru.47`，promoted/current active authority 为
`current-main-0.6.5-guru.48`。

## Design responsibilities

- `D392-01`：四个发布轴保持独立 authority，但所有 current release-facing surfaces
  投影同一 mapping：`v0.6.16-guru.1` / `0.6.16-guru.41` / CLI `0.6.16` /
  `castbox/Trellis@ad332e3fe5a19d7274cb03e7c2f3e2128f8de291`。Fork full SHA 是
  source/build authority，CLI 或 extension version 不能替代它。
- `D392-02`：task worktree 只写 delivery 与 task-isolated RDT/Architecture contributions；
  Architecture 与 RDT serialized promotion owners 绑定 expected `.47`，串行建立唯一 `.48`
  shared authority。pre-promotion candidate 不修改 shared current locator，也不把 `.48`
  称为 active/current。
- `D392-03`：current consumers 采用 subtraction-first direct convergence，同步迁移到目标
  mapping；不增加 dual-read、fallback、alias、adapter、第二 release state machine 或新公共
  API。`.47` 与历史 release/evidence 只在 promotion 后通过 lifecycle navigation 标记为
  immutable superseded，不改写历史正文事实。
- `D392-04`：Stage 1 只产生 preparation delivery bytes。repository-private release
  orchestration 先编排 pre-promotion Phase 2、Task Commit 与 full-branch review；通过后由
  serialized Architecture/RDT owners promotion `.48`，再对 promotion-created diff 执行 fresh
  Phase 2、Task Commit 与 full-branch review。只有第二次 review 通过后才能进入 Publication、
  Finalizer 与 Merge owners；preparation merge 后丢弃全部 Stage 1 review/release evidence，
  fresh-fetch `origin/main` 建立 Stage 2 exact candidate。
- `D392-05`：Stage 2 的 lineage、完整 predecessor diff、version mapping、source/installed
  validators、四平台 parity、ownership/reapply/drift、install/update/switch、Fork build、业务
  installed smoke、secret scan 与 residue checks 全部绑定同一 candidate。tag、tag-pinned
  smoke、GitHub Release、Issue close 与 cleanup 保持独立 mutation/verification boundary。
- `D392-06`：durable authority 只保留稳定 contract、identity、locator、关系与未验证边界；
  动态 candidate SHA、Gate/checkpoint、payload、tag/Release 状态、时间和用户授权不进入
  contribution、`.48` candidate 或其他 tracked Docs。

## Architecture inheritance

Architecture contribution 由
[#392 contribution](../../architecture/contributions/392-release-v0616-guru1.md) 拥有，
identity 为 `architecture-contribution-392-release-v0616-guru1-v2`。它继承
[current baseline](../../architecture/README.md) 的 `.47` immutable superseded predecessor，
并已将 `ARCH-CUR-025`、`ARCH-INT-015`、`EVD-024` promotion 为 `.48` current
Architecture authority。

本 contribution 的 promotion identity 不声明后续 Phase 2、Branch Review、Stage 1 或 Stage 2
结果，也不授权 Git/GitHub mutation、release publication 或 Issue closure。
