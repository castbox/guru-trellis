# #267 v0.6.15-guru.3 successor Release 执行计划

## Phase 1：Planning 与 Activation

- [x] 从 fresh live Issue #267 body/comments、remote `main`、PR #313/#314 与 Release API
  建立 current authority；历史 comments 明确为 non-contract history。
- [x] 创建 task branch/worktree、`task.json` 与 `issue-scope-ledger.json`，绑定
  `origin/main@3efcce72a0d47e38ec725aa8c0f8498992f3416f`。
- [x] 编写 `prd.md`、`design.md`、`implement.md` 与 Docs SSOT Plan。
- [x] 将 `issue-scope-ledger.json` 修订为：#267 是 primary 与 related，`close_issues=[]`；
  #311/#312 保持 related；preparation PR 固定使用 `Refs #267`。
- [x] 完成 `planning_artifacts` wording review、planning Architecture impact、normal-scenario
  qualification 与 `guru-approve-task-plan`，只消费 checked `approved` exit。
- [x] 展示 approved plan 与 task start 精确副作用，取得新确认后运行官方 activation。

## Phase 2：Release Preparation

- [x] 按 `trellis-before-dev` 重读 docs/preset/workflow/spec 与 generator owner。
- [x] 将 `README.md` stable mapping 与 install commands 更新为
  `v0.6.15-guru.3` / `0.6.15-guru.39` / CLI `0.6.15`。
- [x] 将 `trellis/guru-team-extension.json` version 更新为 `0.6.15-guru.39`；
  `target/requires/tested` CLI 保持 `0.6.15`。
- [x] 更新 workflow/preset README 的 immutable source、candidate mapping 与 commands。
- [x] 更新 throwaway verifier、preset tests、canonical/installed
  `guru-verify-extension-installation` version assertions。
- [x] 更新 `.trellis/spec/docs/public-docs.md` stable mapping。
- [x] 运行 preset apply 生成 `.trellis/guru-team/extension.json`，验证未产生边界外 managed
  bytes、`.new` 或 `.bak`。
- [x] 创建 task-local `release-notes-zh.md`，写明 #311/#312 payload、upgrade path、安全与
  部署影响、assets、验证结果和未验证边界。

## Phase 2：Check、Commit 与 PR

- [x] 运行 release identity scan、manifest/schema/fixture tests、Finalizer/Publication/
  verifier/routing/ownership/workspace-boundary suites、source/installed validators、dogfood
  overlay drift、managed byte/mode parity、permission、registry/consumer graph、recursive
  sidecar-zero 与 secret scan。
- [x] 调用 `guru-check-task`；任何 finding 修复后按实际影响重跑 freshness-dependent gates。
- [ ] 展示 stage paths 与 commit message，取得独立确认后调用 `guru-create-task-commit`。
- [ ] 对完整 `origin/main...HEAD` 执行 independent Branch Review；P0/P1/P2/P3 未关闭
  finding 数必须全部为 `0`。
- [ ] 完成 PR readiness；title/body 使用具体中文，Issue trailer 只写 `Refs #267`，并写明
  tests、安全、部署、配置、schema、CI/CD、container/K8s/DB migration 影响。
- [ ] 分别展示并确认 push、PR create、Finalizer 与 merge；merge 只接受精确文本
  `合并PR`。

## Post-merge：Exact Candidate Freeze

- [ ] fresh fetch 后核对 local `main`、`origin/main` 与 GitHub remote `main`；三者相同才记录
  candidate commit/tree。
- [ ] 执行 `git merge-base --is-ancestor`，分别验证 `5b3b7bef...`、`21c7da147...`、
  `3efcce72...` 为 candidate ancestor。
- [ ] 验证 predecessor `v0.6.15-guru.2^{commit}` 仍为
  `d907fcc5e17f23b6499648e5e9a208457f2d6f8b`，且 `.3` tag/Release 尚不存在。
- [ ] 对 predecessor peeled commit 到 candidate 的完整 committed diff 执行 fresh independent
  review；未关闭 finding 数必须全部为 `0`。

## Pre-tag Exact-candidate Gates

- [ ] 在 candidate 上重新执行 Phase 2 全部 deterministic/package/runtime gates；旧 branch
  evidence 不替代 candidate evidence。
- [ ] 完成 clean throwaway workflow install、preview、switch、preset apply、reapply、official
  update、clean install 与 existing install/update。
- [ ] 完成 Shared、Codex、Claude、Cursor actual-load 与 projection equality。
- [ ] 在不含 `trellis/presets/guru-team` source tree 的 installed business repository 完成
  Publication ready、Finalizer reprepare_required、execute、reprepare_preview、唯一 Draft PR、
  archive、Ready、terminal ready_for_merge 全链。
- [ ] 验证 metadata-tail 只改变 extension provenance，`reviewed_content_head` 不变，
  `publication_head` 为唯一 fast-forward。
- [ ] 完成 #312 workspace-boundary path matrix、secret scan、`.new/.bak/sidecar/tracked-gate/
  owner-private-residue` zero scan。
- [ ] 任一 FAIL、SKIP、stale、cross-SHA、unknown/multiple/unmapped exit 或 residue 非零时停止
  tag plan。

## Tag、Smoke、Release 与 Closure

- [ ] 展示 repository、candidate SHA/tree、annotated tag、tag message、精确 push refspec；取得
  独立确认后创建并 push `v0.6.15-guru.3`。
- [ ] live 回读 tag object、peeled commit/tree；mismatch 时停止，不移动 tag。
- [ ] 展示 tag-pinned clean-install smoke 的临时目录、命令与预期结果；取得独立确认后执行。
- [ ] smoke PASS 后展示 GitHub Release 中文 title/body、target、draft=false、
  prerelease=false、assets=[]；取得独立确认后创建 Release。
- [ ] live 回读 Release、tag、peeled commit、latest stable 与 assets。
- [ ] 展示 `gh issue close 267` 精确命令；取得独立确认后关闭 #267。
- [ ] #311 在 preparation PR 与 #267 Release closeout 阶段保持 OPEN；不把它加入
  `close_issues`。
- [ ] 正式 `.3` 发布后，另行展示业务仓、目标 ref、安装命令、预计改动与回滚方式；取得
  独立安装/重试副作用确认后，安装正式 `.3`，重试原 Finalizer 失败路径与错误文件路径。
- [ ] 上述验证全部 PASS 后，live 回读 #311 并展示 evidence comment、
  `gh issue close 311 --repo castbox/guru-trellis --reason completed` 的精确动作；只有根因与
  acceptance 均闭环时才执行，任一失败、SKIP、stale 或未验证结果均保持 OPEN。
- [ ] cleanup 前展示 branch/worktree/task/runtime resources 与 recoverability；取得独立确认后
  执行 cleanup。
