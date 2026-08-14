# #222 v0.6.5-guru.6 累计发布需求

## 背景

#219、#217、#218、#227 已按固定顺序通过 PR #224、#225、#226、#228
合并关闭，且四个 merge commit 均为 fresh `origin/main` 的祖先。当前稳定
映射仍为 repo tag `v0.6.5-guru.5`、Guru Team extension revision
`0.6.5-guru.27`、official Trellis CLI `0.6.5`；当前 `main` bytes 已与 `.5`
tag 不同，不得复用旧 revision、candidate、SHA 或验证证据。

## 目标

从 clean 且与 fresh `origin/main` 相等的 checkout 准备并冻结一个唯一 exact
candidate，将稳定映射升级为 `v0.6.5-guru.6` / `0.6.5-guru.28` / Trellis
CLI `0.6.5`，完成 #222 定义的完整 pre-tag、隔离业务仓 pinned upgrade、
tag-pinned、GitHub Release 与 Issue closure 门禁。

固定顺序：

```text
#219 -> #217 -> #218 -> #227 -> #222 -> 发布
```

## 范围

- 更新 canonical manifest、dogfood installed manifest、workflow/preset/public
  README、稳定安装与升级命令、stable tag/source 映射及中文 release notes。
- 正式执行一次 `guru-verify-extension-installation` 完整 capability catalog。
- 验证 clean workflow install、existing-repo preview/switch、preset initial
  apply、official Trellis update、preset reapply、受管 Python runtime、
  source/installed/platform equality、managed inventory、dogfood drift 与零
  `.new`/`.bak`/conflict/removal/unknown sidecar。
- 验证 Branch Review 的真实 `record -> check -> invoke -> retire/retain` 生命周期。
- 验证 Finalizer/Merge 的 single-JSON stdout、fresh transition、ready/terminal
  recovery、closure mismatch 与零重复 mutation。
- 在隔离业务仓副本中从 pinned stable source 升级，重放原 2130 路径的
  Publication Review/Finalizer preflight；不得改变任何现有业务 checkout 或远端。
- pre-tag 全部通过后，单独确认并创建 immutable annotated tag；随后核对 tag
  object、peeled commit、candidate tree、manifest revision 与 exact source，执行
  最小 tag-pinned clean install/upgrade entry smoke。
- 分别确认并创建 GitHub Release、发布 #222 去敏证据评论、关闭 #222。

## 非目标

- 不实现或修改 #219、#217、#218、#227 的 correctness 代码。
- 不处理 #223、#208、#164、#220，也不将其写成 `Closes` 范围。
- 不修改 Trellis upstream、全局 npm、系统 Python、用户 site-packages。
- 不修改、commit、push、部署任何现有业务仓 checkout 或生产状态。
- bytes 与已验证 candidate 不同，或任一 required gate 缺失/失败时，不创建 tag、
  Release 或完成性声明。

## 验收标准

1. exact candidate commit/tree 与 live `origin/main`、`v0.6.5-guru.6`、
   `0.6.5-guru.28`、CLI `0.6.5` 一一对应。
2. release-owned docs/manifest/install/upgrade/source bytes 完整且相互一致。
3. 完整 standalone verifier 返回 `verified`，所有 required capability 均有 fresh
   pre-tag 证据。
4. Branch Review、Finalizer、Merge 的公开 wrapper 正常与恢复生命周期通过。
5. 隔离业务仓 pinned upgrade 通过，2130 路径 Publication/Finalizer preflight
   不再因 2000 上限阻断。
6. annotated tag 仅在用户确认后创建并 push；tag-pinned source 与 candidate bytes
   一致，最小入口 smoke 通过。
7. 中文 Release notes 准确覆盖四个 prerequisite、升级步骤、版本映射、验证证据、
   已知限制、安全与部署影响。
8. Release、证据评论、Issue closure 各自取得当前确认并 live 复核；#222 之外
   没有 Issue 被关闭。

