# v0.6.15-guru.3 发布说明（草案）

## 发布身份

- repo annotated tag：`v0.6.15-guru.3`
- Guru Team extension revision：`0.6.15-guru.39`
- official Trellis CLI：`0.6.15`
- predecessor Release：`v0.6.15-guru.2`
- workflow/preset source：同一 immutable `v0.6.15-guru.3` tag

repo tag、extension revision 与 Trellis CLI 是三个独立版本轴。当前文件只定义目标
mapping；preparation PR 合并前不冻结 candidate SHA，tag object、peeled commit、GitHub
Release、tag-pinned install 与 post-publish smoke 均尚未建立。

## 累计内容

- #311：修复 installed business repository Finalizer provenance reprepare 时混淆业务
  target checkout 与 Guru Trellis extension source checkout 的问题；正式候选必须包含
  commit `5b3b7bef73824ae78b8bf13a20cfd9ba01acb2b8` 与 PR #313 merge commit
  `21c7da14798683193b460a5e7c5bd24c7c517804`。
- #312：允许已合并 active task 在原 worktree 中通过 workspace boundary；正式候选必须
  包含 PR #314 merge commit `3efcce72a0d47e38ec725aa8c0f8498992f3416f`。
- #267 release-owned：统一 stable install/update source、canonical/installed manifest、
  public README 与 verifier assertions，并在 merge 后对唯一 exact candidate 执行完整
  Release gates。
- #267 authority alignment：初始 preparation commit 的独立 Branch Review 发现 `.39`
  source manifest 与 active `.41` authority 中的 `.37` current-candidate facts 冲突。
  r18 要求先通过 task-owned RDT/Architecture contributions 与 serialized promotion 激活
  `current-main-0.6.5-guru.42`；`.42` 只同步 release/current facts 与 traceability，
  不改变产品行为、Skill API、Architecture decision、owner、GAP 或 compatibility exit。

## 安装与升级

新安装与已有仓升级都必须使用 pinned `v0.6.15-guru.3` marketplace/workflow source，
先安装 official Trellis CLI `0.6.15`。已有仓先 preview 并完成唯一一次 official Trellis
preserve-mode update，再切换 workflow、reapply 同 tag preset，处理全部 `.new` / `.bak`，
最后核对 source/installed/platform equality、managed inventory、受管 Python runtime、
ownership、mode、overlay drift 与递归零 sidecar。

## 验证状态与边界

本草案不把 preparation branch 测试写成 published exact-candidate 证据。preparation PR
合并后，#267 必须从 fresh remote `main` 冻结唯一 commit/tree，并确认 #311 fix、PR #313
merge 与 PR #314 merge 都是 candidate ancestor；随后在同一 candidate 上完成完整 committed
diff review、package/runtime、四平台、clean/existing install/update/reapply、installed
Finalizer recovery、workspace-boundary、secret scan 与 residue-zero 门禁。

当前 authority alignment 仍处于 task-owned contribution 阶段：`.41` 继续是 live current，
`.42` 尚未 promotion，初始 commit `2a546100…` 不是 Publication 或 Release candidate。只有
contribution review、serialized promotion 与 promotion-created diff 的 fresh review 全部通过后，
`.42` 才能成为唯一 active knowledge authority。

tag 创建后必须从 tag-pinned clean source 完成 smoke；GitHub Release 创建后必须 live 回读
tag object、peeled candidate、正式版状态、latest stable 与空 assets。任一 FAIL、SKIP、
stale、cross-SHA、unknown/multiple exit 或 residue 非零都阻断相应发布步骤。

本发布未取得 live GPT-5.6 Sol production semantic evidence；deterministic/no-model/
fake-production 结果不能证明 pressure matrix、模型稳定性或未来模型行为。

## Issue 关闭边界

#267 只在 tag-pinned smoke、正式 GitHub Release 与 live identity reread 全部通过后进入独立
关闭确认。#311 不由 preparation PR 或 #267 Release closeout 自动关闭；正式 `.3` 发布后，
必须在独立业务仓安装正式 `.3`，重试原 Finalizer 失败路径与错误文件路径。只有全部通过且
live #311 仍与该根因一致时，#311 才具备独立关闭条件，否则保持 OPEN。

## 安全、部署与资产

本发布不包含 secret、credential、private key、签名 URL、客户数据或真实业务仓部署，
不修改 Trellis upstream、global npm、系统 Python、数据库、容器、Kubernetes、CI/CD 或
schema migration。预期 GitHub Release assets 为空。
