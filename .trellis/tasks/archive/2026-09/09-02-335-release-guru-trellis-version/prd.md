# #335 建立 guru-trellis 仓库私有正式发布 Skill

## Goal

建立 `release-guru-trellis-version`，为 `castbox/guru-trellis` 的正式版本发布提供仓库私有、无 tracked 运行状态的两阶段编排入口，使 preparation PR 与 post-merge exact-candidate 发布在复用现有 owners 的前提下可靠收敛。

## Requirements

- Skill ID 固定为 `release-guru-trellis-version`，只属于本仓库，不使用公共 `guru-` Skill 命名和 package 接口。
- Skill 只进入仓库当前支持的 Shared、Codex、Claude、Cursor project-local Skill discovery roots；不得进入 Guru Team marketplace、preset、overlay、公共 registry、extension manifest 或业务仓库安装投影。
- 最小输入包括 current release Issue、目标 repository tag、目标 extension revision、official Trellis CLI version 和 predecessor tag；每次使用都必须重新读取 live Git/GitHub authority。
- lifecycle 分为 preparation task/PR 和 preparation merge 后的 exact-candidate 两阶段。preparation 复用 standard intake、Phase 2、Task Commit、一次完整 Branch Review、Publication、Finalizer 和 merge owners；post-merge 阶段从 fresh `origin/main` 重新冻结 candidate。
- Skill 不复制、不替代、不缩短或削弱现有 owner 的 semantic gate、typed route、freshness、confirmation 和 fail-closed 合同。
- PR title/body 与 GitHub Release title/body 分别在 Publication 和 Release 动作前，根据 live Issue、exact diff、验证结果及 candidate identity 即时生成并完成语义审查；不创建 task-local body handoff。
- 禁止 task-local `release-notes*.md`。`implement.md` 只记录稳定实施计划，不保存动态 checklist、HEAD、阶段进度、Gate pass/fail、finding closure、tag、smoke、Release 或时间状态。
- Phase 2、Branch Review、Publication、Finalizer、tag、smoke 和 Release 的运行态结论不得写入 tracked task 或 durable docs。owner-private runtime 只按既有 owner 合同存在和退休。
- 修改实际交付字节、durable docs、配置、schema、脚本或测试时，受影响的 Gate 必须 stale 并重新验证；lifecycle-only runtime metadata 不得引发 reviewed-content metadata loop。
- stale、cross-SHA、FAIL、SKIP、unknown、multiple、unmapped exit 或 live identity mismatch 必须停止在当前 owner，不以 metadata commit 记录进度或恢复。
- tag、tag-pinned smoke、GitHub Release、Issue closure、merge 和 cleanup 保持各自独立、精确展示和当前对话确认；任何确认不得跨动作复用或持久化。
- post-merge exact-candidate 保留 predecessor-to-candidate full diff、版本映射、source/installed validators、四平台 parity、install/update/reapply、secret scan、residue check 和 tag-pinned smoke 责任，但本 Issue 不扩张为完整累计多平台 Release Gate 矩阵。

## Acceptance Criteria

- 仓库内可发现 `release-guru-trellis-version`，四个 Agent 可读投影语义与字节一致，且 public package/preset/installed inventories 不包含它。
- honest-path 回归证明稳定计划到最终内容提交后只执行一次完整 Branch Review，随后可进入 Publication 和 Finalizer，不产生 release-status metadata commit 或二次内容 Review 循环。
- 回归证明 delivery/durable/config/script/test 变化会改变 reviewed-content identity 并使对应 Gate stale，owner-private lifecycle metadata 不改变该 identity。
- preparation PR body 与 post-merge GitHub Release body 均由 live authority 即时生成、语义审查并只交给对应外部动作 consumer。
- release task 不创建 `release-notes*.md`，稳定 `implement.md` 不含 checkbox 或执行状态字段，tracked tree 不保存 release lifecycle 状态。
- candidate 与 preparation reviewed head 不同、lineage 不可证明、验证出现 FAIL/SKIP 或 exit 不闭合时，流程停止且无后续发布副作用。
- tag、smoke、Release、Issue closure、merge 和 cleanup 的独立 confirmation boundary 有明确合同和定向测试。
- README、RDT/Architecture contribution、repo-private Skill、四平台投影与测试形成一致的 durable authority；current-checkout 验证无 drift、sidecar 或 public-package 泄漏。

## Boundaries

- 本 Issue 不发布 `v0.6.15-guru.5`，不创建、移动或删除任何 tag 或 GitHub Release。
- 不修改、关闭、归档或清理 Issue #332；不读取或复用其 branch、worktree、task、runtime checkpoint、Review 或未提交文件，#332 保持暂停。
- 不修改 Trellis upstream、全局 npm、`node_modules` 或业务仓库。
- 不改变 Guru Team public Skill I/O、typed exits、marketplace workflow、preset installer 或业务仓库投影。
- 不增加恶意 actor、对抗输入、并发竞态、锁、TOCTOU、fault injection 或跨 OS crash-consistency 范围。
