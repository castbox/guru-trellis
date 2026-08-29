# #267 v0.6.15-guru.3 successor Release 需求

## Authority

唯一 current contract 是 live Issue #267 body `2026-08-29-r17`。2026-08-20 与
2026-08-21 的 Issue comments、`2026-08-23-r16` body、历史 task 和旧 Release
均为 non-contract history，不拥有本任务范围或发布身份。

release preparation base 固定为
`origin/main@3efcce72a0d47e38ec725aa8c0f8498992f3416f`。该 commit 只是 preparation
base，不是最终 exact candidate。

## 发布目标

本任务发布一个正式 correctness successor，身份固定为：

- repository：`castbox/guru-trellis`；
- repo annotated tag：`v0.6.15-guru.3`；
- Guru Team extension revision：`0.6.15-guru.39`；
- target / required / tested Trellis CLI：`0.6.15`；
- predecessor Release：`v0.6.15-guru.2`；
- predecessor peeled commit：`d907fcc5e17f23b6499648e5e9a208457f2d6f8b`。

最终 exact candidate 必须包含以下 ancestor：

- Issue #311 fix commit：`5b3b7bef73824ae78b8bf13a20cfd9ba01acb2b8`；
- PR #313 merge commit：`21c7da14798683193b460a5e7c5bd24c7c517804`；
- PR #314 merge commit：`3efcce72a0d47e38ec725aa8c0f8498992f3416f`。

## Accepted Scope

- 将 stable install/update source、manifest、public README、workflow/preset
  README、verifier fixture 与 canonical/dogfood/installed projection 统一到
  `.3` / `.39` / CLI `0.6.15`。
- 生成 release preparation committed candidate，并在 PR merge 后从 fresh
  live remote `main` 冻结 commit 与 tree。
- 对 predecessor peeled commit 到 exact candidate 的完整 committed diff 执行
  semantic review，P0/P1/P2/P3 未关闭 finding 数必须全部为 `0`。
- 在同一 candidate 上完成 package/runtime、四平台、clean/existing
  install/update/reapply、#311 installed Finalizer recovery、#312 workspace
  boundary、secret scan 与 residue-zero 门禁。
- 经独立确认创建 annotated tag，完成 tag-pinned smoke；再经独立确认创建
  GitHub Release，并 live 回读最终发布身份。
- Release、tag-pinned smoke 与 live reread 全部通过后，单独审查并确认 #267
  closure。
- #311 不由 preparation PR 或 #267 Release closeout 自动关闭。正式 `.3` Release
  发布后，另行在独立业务仓安装正式 `.3`，重试原 Finalizer 失败路径与错误文件路径；
  全部通过时 #311 才进入独立 closure，任一失败或未验证时保持 OPEN。

## Release Preparation 文件边界

实现阶段只修改以下 release identity owner、projection、assertion 与 task 文件：

- `README.md`；
- `trellis/guru-team-extension.json`；
- `trellis/presets/guru-team/README.md`；
- `trellis/workflows/guru-team/README.md`；
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`；
- `trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`；
- `trellis/skills/guru-team/packages/guru-verify-extension-installation/tests/test_contract.py`；
- `.trellis/guru-team/skills/packages/guru-verify-extension-installation/tests/test_contract.py`；
- `.trellis/spec/docs/public-docs.md`；
- preset apply 生成的 `.trellis/guru-team/extension.json`；
- `.trellis/tasks/08-29-267-release-v0615-guru3/**`。

门禁发现功能缺陷、公共合同变化或上述边界外的 managed byte 变化时，任务停止在
scope confirmation，不在 release preparation 中吸收修复。

## Issue Scope

- #267 是 primary Release owner；preparation PR 只写 `Refs #267`，不得通过
  PR merge 关闭 #267。
- #311 是 required fix 与 post-release business-repository proof owner；preparation PR
  与 #267 Release closeout 均不关闭 #311。正式 `.3` 安装及原失败路径、错误文件路径
  重试全部通过后，才进入独立 #311 closure；否则保持 OPEN。
- #312 是 CLOSED historical prerequisite；本任务不重开或再次关闭 #312。
- #247、#249、#250、#292、#293、#261、#248、#252 保持 OPEN，均不是本次
  correctness successor 的 prerequisite 或 close target。

## 禁止范围

- 不移动、删除或重写 `v0.6.15-guru.1`、`v0.6.15-guru.2`。
- 不 rewrite `main` history。
- 不修改 Trellis upstream、global npm、`node_modules` 或未授权业务仓。
- 不把用户授权写入 task artifact、gate、tag message 或 Release body。
- 不把旧测试、package test、SKIP 或跨 SHA evidence 写成 exact-candidate pass。
- tag 创建后 smoke 失败时，不删除、移动或重建该 immutable tag。

## Acceptance

1. preparation PR 合并后的 fresh remote candidate commit/tree 唯一，且三个 required
   ancestor 检查命令全部返回成功。
2. release-facing source、projection 与 assertion 中，repo tag 唯一为
   `v0.6.15-guru.3`，extension revision 唯一为 `0.6.15-guru.39`，CLI 唯一为
   `0.6.15`；历史 task 与 released-history 文档不计入 mutable release surface。
3. exact-candidate full diff review 的 P0/P1/P2/P3 未关闭 finding 数均为 `0`。
4. Issue #267 的十二项 pre-tag gate 在同一 candidate 上全部 PASS；任一 FAIL、SKIP、
   stale、cross-SHA、unknown exit、multiple exit 或 residue 非零均阻断 tag。
5. annotated tag peeled commit 与 frozen candidate 相同，tag-pinned smoke PASS。
6. GitHub Release 为正式版、非 draft、非 prerelease、assets 为空，target 与 peeled
   candidate 相同，latest stable 属性经 live API 回读成立。
7. #267 只在第 5、6 项成立后进入独立 closure；#311 在 preparation 与 Release
   closeout 阶段仍为 OPEN。
8. 正式 `.3` 发布后的独立业务仓安装、原 Finalizer 失败路径与错误文件路径重试全部
   PASS 时，#311 才具备独立关闭条件；任一 FAIL、SKIP、stale 或未验证结果均保持 OPEN。
