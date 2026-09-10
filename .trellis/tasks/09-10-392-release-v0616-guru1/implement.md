# Implementation Plan

## Stage 1: Preparation Delivery

1. 盘点 predecessor-to-HEAD release-facing 引用和 canonical/managed ownership，形成
   `v0.6.16-guru.1` / `0.6.16-guru.41` / CLI `0.6.16` / Fork full SHA 的唯一
   current mapping。
2. 更新 `trellis/guru-team-extension.json` 及其版本 expectation；运行 preset all-platform
   reapply，同步 dogfood/installed projection，并处理所有 managed drift 或 sidecar。
3. 更新 README、workflow/preset 文档、public-docs spec、测试 fixture、schema/validator 中
   属于 current release contract 的旧 mapping；历史 archived/released 内容保持原事实。
4. 从 `current-main-0.6.5-guru.47` 派生 Requirements、Design、Test successor `.48`，
   新增 #392 traceability 并创建 Architecture #392 contribution；保持 `.48` 为
   `reviewed_candidate`、`.47` 为唯一 active shared authority。
5. 直接演进 `.agents/.codex/.claude/.cursor` 四份 repository-private
   `release-guru-trellis-version` contract，删除 one-review 假设，明确 pre-promotion review、
   serialized promotion 与 post-promotion fresh review 顺序；同步更新 canonical contract test。
6. 运行 source/installed package、manifest、overlay/ownership、dogfood drift、定向测试、
   引用扫描、`git diff --check` 和 task scope 验证；修复 current-scope finding。
7. 完成 pre-promotion Phase 2 semantic check、task commit 和独立 full-branch review；
   P0-P3 open findings 为零后，Architecture/RDT serialized promotion owners 才绑定
   expected `.47` 将 `.48` 设为唯一 active，并把 `.47` 标记为 superseded。
8. 对 promotion-created diff 重新执行 Phase 2、task commit 和独立 full-branch review；
   通过后 Publication、Finalizer push/PR/archive/Ready 和 PR merge 分别进入其 owner
   与确认边界。

## Stage 2: Exact-Candidate Release

1. preparation PR 合并后 fresh-fetch `origin/main`，验证 predecessor ancestry，冻结唯一
   candidate commit/tree，并创建 clean detached candidate checkout。
2. 从该 checkout 执行 release contract 与 Issue #392 的完整 gate：lineage/full diff、
   version mapping、source/installed validators、四平台 parity、ownership、all-platform
   reapply、dogfood drift、clean/existing/update/workflow switch、Fork source/build、业务
   installed smoke、secret scan、diff hygiene 和递归 residue。
3. 对 gate 输出和完整 `v0.6.15-guru.6..candidate` diff 做独立语义复核；required
   `FAIL`、`SKIP`、stale、cross-SHA 或未映射 exit 均停止发布。
4. 生成并审核绑定 exact candidate 的 tag message；展示 tag ref/SHA/命令后单独确认，
   创建并 push annotated tag `v0.6.16-guru.1`，live 回读 tag object 与 peeled commit。
5. 展示 tag-pinned smoke checkout/命令/影响后单独确认，从 immutable tag 执行安装和
   post-publish smoke。
6. 生成并审核中文 GitHub Release title/body；展示 exact tag 与 Release mutation 后单独
   确认，创建正式 stable Release并回读远端属性。
7. Release 完成后分别处理 Issue #392 closeout 与 branch/worktree/task cleanup confirmation。

## Validation Commands

准备阶段使用 repository current scripts；exact candidate 阶段按 release contract 固定 locator
重新执行以下命令：

```bash
git diff --find-renames --find-copies "v0.6.15-guru.6^{commit}" "${candidate_commit}^{commit}" --
git diff --name-status "v0.6.15-guru.6^{commit}" "${candidate_commit}^{commit}" --
./trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json
./.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode installed --json
./trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
./trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
./trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
GURU_TEAM_THROWAWAY_SINGLE_REPO_COMPATIBILITY=1 \
  TRELLIS_WORKFLOW_SOURCE="gh:castbox/guru-trellis/trellis#${candidate_commit}" \
  ./trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
git status --short
git diff --check
find . \( -type d -name '__pycache__' -o -type f \( -name '*.pyc' -o -name '*.pyo' -o -name '*.new' -o -name '*.bak' \) \) -print
```

secret scan 必须覆盖由 predecessor-to-candidate changed-file set 得到的 candidate bytes；
使用当前环境真实 scanner，缺失能力不得用文本扫描冒充通过。

## Risky Files And Rollback Points

- manifest、preset installer/overlay 和 installed copies：reapply 后必须逐字节与 mode 验证。
- current Architecture/RDT navigation 与版本目录：必须保持单一 active identity、完整 trace 和
  immutable predecessor。
- public README/workflow/preset 安装命令：必须能从 target tag/candidate 实际执行。
- tag push 是不可逆发布边界；之前可停止，之后不得移动或重建该 tag。

## Docs SSOT Plan

- Strategy：`delta_first`。Phase 2 先完成代码/manifest/fixture 与 task delta，再在 final
  semantic check 前合并 durable docs 和 Architecture/RDT successor authority。
- Current docs state：release-facing文档仍混有 `v0.6.15-guru.6`、extension
  `0.6.15-guru.40` 与 #378 非发布过渡说明；Architecture/RDT `.47` 明确记录未发布。
- Evidence paths：Issue #392、`trellis/guru-team-extension.json`、
  `trellis/presets/guru-team/source/trellis-source.json`、`README.md`、
  `.trellis/spec/docs/public-docs.md`、三个 public README、Architecture/RDT `.47`。
- Durable docs to update：`README.md`、`.trellis/spec/docs/public-docs.md`、
  `.trellis/spec/docs/requirements-design-test-ssot.md`、workflow/preset README、
  `docs/{requirements,design,test}/README.md`、successor `.48` version directories、
  `docs/architecture/**` navigation/current/contribution/evidence/roadmap。
- Task artifact delta：仅更新本 task 的 `prd.md`、`design.md`、`implement.md`、context
  manifests 和既有 `issue-scope-ledger.json`；不创建 release notes、body handoff、动态
  checklist 或 lifecycle evidence。
- Merge checkpoint：Phase 2 owner 在最终 check 前验证 durable docs、task delta、manifest、
  tests 和 Architecture/RDT authority 已闭合；Branch Review 只验证，不首次合并文档。
- Repair/follow-up：current authority locator/version/status、trace 或 projection 不闭合时进入
  Architecture/RDT owner repair/promotion route；不把缺口降级为 follow-up。当前 scope 无
  follow-up Issue。
