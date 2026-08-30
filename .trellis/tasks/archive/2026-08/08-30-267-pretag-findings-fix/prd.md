# #267 pre-tag findings 修复需求

## Authority And Current Facts

唯一 current requirement authority 是 live Issue #267 body `2026-08-30-r19`。
本任务从 `main@9f560ec191851f82768d5e7aa031e6d852c34f14` 开始，处理该候选在
pre-tag review 中确认的三个未关闭 finding。历史 Issue comments、旧 task 结论与旧候选
只提供事实背景，不拥有本任务范围。

截至 2026-08-30 的 live 发布身份为：

- latest stable GitHub Release：`v0.6.15-guru.2`；
- annotated tag object：`641ed35e91c4a58cc7083ab2e4811d30e392fbed`；
- peeled commit：`d907fcc5e17f23b6499648e5e9a208457f2d6f8b`；
- released extension revision：`0.6.15-guru.38`；
- released target Trellis CLI：`0.6.15`；
- successor target 保持 `v0.6.15-guru.3` / extension `0.6.15-guru.39` /
  Trellis CLI `0.6.15`，尚未创建 tag 或 Release。

当前 `main` 已包含 #311 fix commit `5b3b7bef73824ae78b8bf13a20cfd9ba01acb2b8`、
PR #313 merge commit `21c7da14798683193b460a5e7c5bd24c7c517804` 与 PR #314
merge commit `3efcce72a0d47e38ec725aa8c0f8498992f3416f`。#311 在正式 `.3`
业务仓安装与原失败路径重试完成前保持 OPEN。

## Goal

关闭当前三个 pre-tag finding，使新合并后的 `main` 能重新冻结为
`v0.6.15-guru.3` exact candidate，并从 fresh candidate 重新执行完整 Release Gate。

## Requirements

### R1 Preserve Installed Platform Selection During Finalizer Reprepare

`prepare_provenance_metadata_tail()` 当前无条件向 preset apply 传递
`--all-platforms`。该行为会把 Claude-only installed business repository 扩张为三平台
安装，使 `claude-clean` matrix 产生 provenance 之外的 managed diff。

修复必须：

- 从 reviewed target 的 parent installed manifest 读取平台选择；
- 校验 `install.selected_platforms`、`skill_packages.selected_platforms` 与
  `overlays.selected_platforms` 三者完全相同；
- 校验 `install.all_platforms` 与平台集合语义一致；
- `all_platforms=true` 时传递 `--all-platforms`；
- `all_platforms=false` 时按排序后的精确集合重复传递 `--platform <name>`；
- manifest 缺字段、类型错误、平台未知、集合为空、集合重复或三处不一致时，在 preset
  apply 前 fail closed；
- metadata tail 变化仍限定为 `.trellis/guru-team/extension.json` 的既有 provenance 字段，
  禁止新增 managed path、sidecar 或 overlay mutation。

### R2 Repair Active Latest-Stable Authority

active `.42` authority 把 `v0.6.5-guru.10` 写成 latest stable；live GitHub Release 已是
`v0.6.15-guru.2`。通过现有 RDT `repair` 与 Architecture `repair` owner lifecycle
修复 latest-stable current fact、tag object、peeled commit、extension revision 与 CLI
identity。

`v0.6.5-guru.10` / extension `.36` / CLI `0.6.5` 继续作为 existing migration 的
immutable historical before-state；禁止对这类历史语义做全仓替换。

### R3 Remove The #312 Machine-Local Path

将 archived #312 `implement.md` 中唯一 `/Users/...` business worktree 路径替换为明确的
repo-neutral locator。只清除机器身份；不改写 #312 的历史需求、验证结论、Issue 状态或
workspace-boundary 语义。

### R4 Preserve Release And Issue Boundaries

- 本任务不改变 `.3/.39/CLI 0.6.15` successor mapping。
- 本任务不创建 tag、GitHub Release 或 assets。
- 本任务不关闭 #267、#311 或其它 Issue。
- #267 保持 Release semantic owner；#311 保持正式 `.3` 业务仓验证 owner。
- 修复合并后必须从 fresh remote `main` 重新冻结 candidate；旧 SHA 的 matrix evidence
  不得作为新 candidate pass。

## Exact File Boundary

实现范围固定为：

- `trellis/skills/guru-team/packages/guru-finalize-task/runtime/owner.py`；
- `trellis/skills/guru-team/packages/guru-finalize-task/tests/test_contract.py`；
- preset apply 生成的 `.trellis/guru-team/skills/packages/guru-finalize-task/runtime/owner.py`；
- preset apply 生成的 `.trellis/guru-team/skills/packages/guru-finalize-task/tests/test_contract.py`；
- preset apply 生成的 `.trellis/guru-team/extension.json`；
- `docs/requirements/versions/current-main-0.6.5-guru.42/requirement-main.md`；
- `docs/architecture/01-current/system.md`；
- `docs/architecture/evidence/current-evidence.md`；
- `.trellis/tasks/archive/2026-08/08-27-312-workspace-boundary-merged-active-task/implement.md`；
- `.trellis/tasks/08-30-267-pretag-findings-fix/` 下的本任务文件。

若 generator 产生上述边界外的 managed byte 变化、`.new`、`.bak` 或 undeclared sidecar，
实现阶段立即停止并返回 scope review。

## Acceptance Criteria

1. Claude-only、Codex-only、Cursor-only、Codex+Cursor 与 all-platform installed manifest
   均生成与 parent 完全相同的平台集合；Finalizer metadata tail 只改变 allowlist 内的 provenance
   字段。
2. malformed 或三处平台集合不一致的 installed manifest 在 preset apply 前返回确定性错误，
   target checkout 与 extension source checkout 均保持 clean。
3. canonical 与 installed Finalizer runtime/test bytes 完全相同；dogfood overlay drift、package
   registry、consumer graph、mode、permission 与 recursive sidecar checks 通过。
4. active `.42` 的 latest-stable current fact 唯一指向 `v0.6.15-guru.2`、tag object
   `641ed35e...`、peeled commit `d907fcc5...`、extension `.38` 与 CLI `0.6.15`；
   `.10/.36/CLI 0.6.5` 只保留在明确的 historical before-state 语境。
5. scoped sensitive-path scan 不再命中 #312 的 `/Users/...` 路径；替换文本不包含另一台机器
   或另一位用户的绝对路径。
6. focused Finalizer tests、canonical/installed package tests、preset apply/drift checks、
   `claude-clean` regression 与 task validation 全部 PASS；任何 FAIL、SKIP、stale 或 residue
   非零均阻断发布恢复。
7. 修复合并后的 fresh `main` 仍包含三个 required ancestor；predecessor `.2` tag identity
   不变，`.3` tag/Release 仍不存在。
8. 新 exact candidate 的完整 diff review 返回 P0/P1/P2/P3 未关闭 finding 全为 `0`，随后才
   进入 pre-tag full matrix、tag 与 Release 副作用确认。

## Out Of Scope

- 修改 Finalizer public input/output、typed exit、schema、consumer 或 GitHub side-effect contract。
- 改变 preset 支持平台集合或 source/target checkout ownership。
- 重写 `.42` 的 architecture decision、owner、single-writer、GAP、ADR 或 compatibility exit。
- 重写 #312 历史实现与测试内容。
- 修改 Trellis upstream、global npm、`node_modules` 或业务仓。
- commit、push、PR、merge、tag、Release、Issue closure 或 cleanup。

## Blocking Open Questions

无。
