# #81 准备并发布 v0.6.5-guru.5 稳定基线

## 目标

在 #180 合并后的 fresh remote `main` 上完成 `v0.6.5-guru.5` 的 release preparation、exact remote candidate 验证、immutable annotated tag、tag-pinned 验证、GitHub Release、去敏 evidence comment 与 Issue closure，为后置 #195 提供可安装、可回滚、可精确复现的稳定基线。

## 已确认事实

- GitHub Issue #81 当前为 Open，且是本次发布的唯一 authority。
- PR #201 已于 `2026-08-10T10:28:42Z` 合并，merge commit 为 `83d91dd7ae2a950e26f3bb99c05d0e461496e7d4`；#180 于 `2026-08-10T10:28:44Z` 自动关闭。
- Intake 时本地 `main`、`origin/main` 与 decision checkout 均为 `83d91dd7ae2a950e26f3bb99c05d0e461496e7d4`。
- 已发布最新 release/tag 是 `v0.6.5-guru.4`；tag object 为 `995652edc2a53c17a9d980984e67f7dae4910d05`，peeled commit 为 `596a6a9ca0819f0c7ebac6adb1e9ac20cce806b5`。
- 当前 canonical extension revision 为 `0.6.5-guru.25`，official Trellis CLI target 为 `0.6.5`，但公开 workflow/preset README 仍将 `.3` 描述为 current stable。
- Current `main` 的 release-owned tree 已与 `.4` peeled commit 的 tree 不同；同一 extension revision 不得继续表示不同 bytes，因此 `.5` preparation 必须分配 `0.6.5-guru.26`。

## 需求

### R1 Release preparation

- 从本 task branch 最小修改 canonical manifest、公开 workflow/preset 文档、stable source 命令、release identity 示例/断言及其直接测试。
- 将 stable marketplace/preset source 收敛到 `gh:castbox/guru-trellis/trellis#v0.6.5-guru.5`，并将 canonical extension revision 提升到 `0.6.5-guru.26`。
- 不在 candidate merge commit 尚未产生时硬编码一个猜测 SHA。公开文档说明 annotated tag 必须 peel 到最终 candidate；精确 OID 映射由 release evidence 和 GitHub Release notes 记录。
- canonical 修改后同步 dogfood installed manifest/copies，并验证无 drift、无意外 managed files、无未处理 `.new/.bak`。

### R2 Preparation PR

- 完成 Phase 2、current-HEAD Branch Review、publication readiness、remote pushed-ref verification 和正常 Finalizer/merge gate。
- PR 标题和正文使用中文，正文只包含 `Refs #81`，不得包含 `Closes/Fixes/Resolves #81`。
- Scope Ledger 保持 `close_issues=[]`、`related_issues=[180]`、`followup_issues=[195]`；preparation PR merge 或 task archive 均不代表 #81 完成。

### R3 Candidate freeze 与 pre-tag remote validation

- Preparation PR 合并后重新同步 live remote `main`，把最新 exact remote commit 冻结为唯一 candidate。
- 任何 `main` 或 release-owned bytes 变化使旧 candidate evidence stale，并要求重新冻结、重跑。
- 以 exact remote candidate ref/commit 在 clean throwaway 环境验证 workflow init、existing workflow preview/switch、preset initial apply、15 active Skills/57 exits/33 targets、registry/interface/public contracts、source/installed schemas、managed inventory、hash/mode/sidecars、代表性 closed-loop probes、#180 Finalizer/PR Merge happy/recovery fixtures、official `trellis update` 后 reapply、`.4` 到 candidate upgrade/reapply、dogfood drift 与 README 命令。
- 所有 pre-tag gates 通过前不得创建 tag。

### R4 Immutable tag 与 tag-pinned validation

- 独立展示并确认 exact tag plan 后，在 candidate 上创建并 push annotated tag `v0.6.5-guru.5`；禁止复用、移动、覆盖或 force push tag。
- Push 后必须使用 `gh:castbox/guru-trellis/trellis#v0.6.5-guru.5` 重跑完整 clean install/update/upgrade/reapply、discovery、source/installed、sidecar、dogfood 和代表性 closed-loop 验证。
- Evidence 必须绑定 repo tag object、peeled candidate commit、extension revision `0.6.5-guru.26`、official Trellis CLI `0.6.5`、workflow/preset/schema/package/runtime inventory。

### R5 Release、证据与关闭

- Tag-pinned gate 通过后，独立展示并确认 GitHub Release 的 target、tag、title、notes 和副作用，再发布非 draft、非 prerelease Release。
- Release notes 覆盖 #180 的用户可见变化、`.4 → .5` pinned install/update/reapply、精确版本映射、已验证/未验证平台、已知限制、安全与部署影响，并明确 #195 未包含。
- Release 发布和最终 tag-pinned evidence 完成后，独立展示并确认去敏 comment/close payload；先写 #81 evidence comment，再显式关闭 #81，并 live reread 验证。

## 非目标

- 不实现、预改或启动 #195 的 package-local runtime 迁移。
- 不升级任何业务仓库；代表性业务仓库 pinned smoke 需要后续单独授权。
- 不修改 Trellis upstream、全局 npm 包或 `node_modules`。
- 不清理、修改或复用 #180 的 worktree/branch。
- 不把本机 dogfood pass、pre-tag pass、tag push 或 release draft 单独称为发布完成。
- 不增加恶意伪造、攻击模型、TOCTOU、锁、并发压力、fault injection 或跨 OS 原子性加固。

## 验收标准

- [ ] AC1：Stable 文档、命令、source identity 与 extension revision 已从历史 `.3/.4` 收敛到 `.5` / `0.6.5-guru.26`，且 preparation PR 仅 `Refs #81`。
- [ ] AC2：Preparation PR 已通过完整 task check、current-HEAD review、publication/finalizer/merge gate并合并，但 #81 仍 Open。
- [ ] AC3：唯一 exact remote candidate 已冻结，完整 pre-tag remote validation 全部通过，证据可检测 candidate/main/release-owned-byte drift。
- [ ] AC4：Annotated tag `v0.6.5-guru.5` 仅在 AC3 后创建并 push，tag object 唯一且 peeled commit 等于 candidate。
- [ ] AC5：精确 tag source 的完整 tag-pinned install/update/upgrade/reapply 与 #180 closeout probes 通过，pre-tag evidence 未被当作替代。
- [ ] AC6：GitHub Release 已发布，notes 准确覆盖升级命令、版本映射、验证范围、限制、安全/部署影响和 #195 排除范围。
- [ ] AC7：#81 留有去敏 candidate/tag/install/evidence comment，随后显式关闭并 live 验证 Closed。
- [ ] AC8：未升级业务仓库，未启动 #195，未清理 #180 worktree/branch。

## 阻塞问题

无。后续每个 Git/GitHub 发布副作用按 live identity 分别展示并取得当前步骤确认。
