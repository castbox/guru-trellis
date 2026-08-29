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
- [x] 展示 stage paths 与 commit message，取得独立确认后调用 `guru-create-task-commit`；初始
  preparation commit 为 `2a5461002856ebcb981156f892e41ef4020d3626`。
- [x] 对初始完整 `origin/main...2a546100` 执行 independent Branch Review；发现
  `BR-267-CAND-001`：`.39` source manifest 与 `.37` active authority 冲突，Architecture
  owner 返回 `architecture_conflict -> planning`，未生成 passing review gate。

## Phase 2R：r18 Authority Alignment Contribution

- [x] 将 live Issue #267 body 修订为 `2026-08-29-r18`，明确 `.42` successor authority
  scope、文件边界、promotion 顺序与第十三项 pre-tag gate。
- [x] 通过 `requirements_scope_set` 将 authority alignment 分类为
  `qualified_approved_expansion`，保持同一 #267 delivery unit。
- [x] 更新本 task `prd.md`、`design.md`、`implement.md` 与 Release notes，删除 r17 的
  `.41` 保持不变假设。
- [x] 创建 RDT task-owned contribution
  `docs/requirements-design-test-contributions/267-release-v0615-guru3/`，目标 `.42`，
  `shared_current_write=false`。
- [x] 创建 Architecture task-owned contribution
  `docs/architecture/contributions/267-release-v0615-guru3.md`，绑定 expected `.41`、
  `target_native`、`ADR required=false` 与 pending independent review。
- [x] 完成 planning wording review、RDT/Architecture Planning gates 与 fresh plan approval。
- [x] 对 contribution candidate 运行 Phase 2；通过后展示并确认新的 task commit。
- [ ] 对完整 committed range 执行独立 Branch Review；通过前不得写 shared `.42`。

## Serialized `.42` Promotion

- [ ] contribution review 通过后，按 RDT 与 Architecture owner 的 fresh typed routes 确定
  调用顺序并串行执行；不得并发写 shared current，也不得在 planning 阶段预选顺序。
- [ ] RDT promotion 绑定 expected `.41` 并激活 `.42`，更新 Requirements/Design/Test
  navigation、version history、current facts 与 traceability。
- [ ] Architecture promotion 绑定 expected `.41` 并激活 `.42`，更新 README、CURRENT 与
  evidence；不创建 ADR，不改变 decision/owner/GAP/compatibility。
- [ ] 对 promotion-created diff 重新运行 Phase 2、task commit 与独立 Branch Review。
- [ ] 只有 post-promotion Branch Review 通过后才恢复 PR readiness。
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
