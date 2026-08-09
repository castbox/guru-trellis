# 修复 Finalizer 前 clean provenance tail 与 pre-PR plan reprepare 缺口

## Goal

在 reviewed content 已完成 Branch Review、Finalizer 已推送后，允许一次由独立 clean source checkout 产生的 provenance metadata-tail，并在该 tail 使旧 closeout plan 失效时自动进入唯一的 `reprepare_required` 恢复路径。保持 #184 的 dirty-source fail-close，不读取或改变 #179 的真实资源。

## Requirements

1. 将 `reviewed_content_head`（实现、测试、durable docs、workflow/skill/preset/script bytes）与 `publication_head`（其后唯一允许 provenance metadata-tail）作为独立、最小、可验证的身份。
2. metadata-tail 只能由 detached、clean、精确等于 reviewed head 的 source checkout，经 canonical preset/overlay apply 生成；tracked diff 只能修改 `extension.json` 的 `installed_at`、`source.ref`、`source.commit`、`source.tree_state`、`source.is_mutable_ref`，且 commit/ref/clean/mutable 值必须绑定 reviewed head。
3. Verifier 使用 manifest 绑定的 clean immutable reviewed head 验证 source bytes，同时把 target/ref/PR identity 绑定 publication head；任何 dirty、mutable、mismatch、managed-byte drift、sidecar、额外 task 内容或越界 diff 继续 fail closed。
4. 在 PR 创建、archive 或 archive commit 之前，且 issue/scope/body/base/reviewed content/verification profile 未变、remote 可 fast-forward 且无并行 publication consumer 时，Finalizer 自动 supersede 并清理旧 owner-private plan/gate/request，返回稳定 `reprepare_required`，重新 prepare、展示新 plan 并在新确认后继续 exact-ref verification。
5. metadata-tail 不改变 reviewed-content identity，不重复 Phase 2、Branch Review 或 Publication semantic review，不触发第二次 apply；失败场景返回精确 implementation/block 边界。
6. canonical workflow/runtime、Skills、schemas、preset/overlay、平台入口、README/spec 与同步副本保持一致；用受控 fixture 重演 #179 顺序，不读取或写入 #179 真实 worktree/branch/task/runtime/remote/plan。

## Acceptance Criteria

- [ ] clean source checkout 只生成一次允许字段 metadata-tail，reviewed/publication identity 可分别验证。
- [ ] 正常 tail 不触发重复 semantic phases；旧 plan/gate/request 自动 supersede/cleanup，mapped recovery 只要求新确认。
- [ ] 非允许字段、dirty/mutable/mismatch/drift/sidecar/task-content 混入、PR 已存在、archive 已开始、scope/content 改变、non-FF 均 fail closed。
- [ ] 新 publication head 仅 fast-forward push；exact remote verification 同时绑定 reviewed content 与 publication head；成功后可继续 Draft PR、archive、Ready，Issue #191 在 merge 前保持 open。
- [ ] #179 controlled fixture 证明原 `extension_source_not_clean` 顺序可通过标准 recovery 完成；不接触 #179 实际状态。
- [ ] source/installed package graph、dogfood、preset/overlay、throwaway install/update/reapply、zero sidecar、upgrade/update 与独立 current-HEAD Branch Review 均有真实证据。

## Scope Boundaries

- Close scope 只有 #191；#179、#180、#181、#184、#187 仅作 live/read-only authority 或受控 fixture 语义，不修改其任何资源。
- 不实施 #180 transaction compression/merge lifecycle、#181 全局 gh 治理、PR/archive 中途 history rewrite、跨月迁移、任意 scope change、恶意/竞态/TOCTOU/crash-consistency 防御。
