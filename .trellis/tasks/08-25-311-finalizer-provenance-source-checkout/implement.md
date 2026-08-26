# #311 实施计划：修复 Finalizer provenance source checkout

## 1. Pre-Implementation Gates

- [x] 三份 planning artifacts 通过
  `guru-review-contract-wording:planning_artifacts`。
- [x] `guru-qualify-normal-scenario:planning_scenario_set` 对本计划的 acceptance、negative fixtures 与
  architecture finding 候选返回 `classified`，拒绝项不进入实现。
- [x] `guru-maintain-architecture-baseline:task_impact_sync(stage=planning)` 返回 fresh
  `baseline_current`，impact 为 `architecture_impact`，change path 为 `target_native`。
- [x] `guru-maintain-requirements-design-test-ssot:task_impact_sync` 确认 `delta_first` 与 task-owned
  contribution route。
- [x] `guru-approve-task-plan` 返回 `approved`。
- [x] 用户在最新 planning summary 后确认实施；此前不运行 `task.py start`，不编辑 product/docs
  implementation surface。
- [x] `trellis-before-dev` 加载 curated `implement.jsonl`，重新核对 task/worktree/base 与 current specs。

## 2. Establish Task-Owned Docs Delta

- [x] 创建
  `docs/requirements-design-test-contributions/311-finalizer-provenance-source-checkout/` 的
  `manifest.yaml`、`requirements.md`、`design.md`、`test.md`、`traceability.md`。
- [x] Planning 已创建
  `docs/architecture/contributions/311-finalizer-provenance-source-checkout.md`，完整记录 current/target
  boundary、owner、single writer、compatibility exit、GAP、project checks 与 promotion state。
- [x] Planning 已创建 ADR candidate
  `docs/architecture/adr/007-finalizer-extension-source-target-binding.md`，绑定两个 checkout 与两种
  source mode。
- [x] Phase 2 按实现发现、before/after candidate、test/runtime evidence 与 fresh project check 更新
  Architecture contribution 和 ADR status。
- [x] 绑定 current `.40` RDT/Architecture、design constitution、change contract 与 Issue #311；不直接
  修改 shared current。

## 3. Implement Private Source Binding

- [x] 在 canonical `guru-finalize-task` runtime 增加 manifest source parser 与 closed
  `self_hosted|installed` binding resolver。
- [x] 规范化 target/source GitHub repository identity，拒绝 missing、malformed、dirty、mutable 与
  non-OID source。
- [x] self-hosted mode 从 target Git object 建立独立 detached source worktree，commit 固定为 reviewed
  head。
- [x] installed mode 在独立目录执行 `git init -> remote add origin -> exact-OID fetch -> detached
  checkout`，校验 origin、HEAD 与 clean state。
- [x] source-resolution helper 保持 Finalizer package-local，复用本 package 现有低层 Git/repository
  primitives，不新增 shared resolver 或 verifier owner dependency。
- [x] 增加 static/runtime assertion，证明 Finalizer 不调用 verifier package、wrapper、gate、artifact
  或 typed exit。

## 4. Separate Apply Target And Source

- [x] 将现有 detached `source` 重命名并收敛为 `target_reviewed_checkout` owner。
- [x] 从 `extension_source_checkout` 定位 canonical apply script，`--repo` 精确传入 target reviewed
  checkout。
- [x] apply 前后检查 source checkout 无变化；target checkout 只有 installed manifest dirty。
- [x] 保持 source 与 target 临时资源独立 cleanup；cleanup 不触碰调用方 worktree 或其它 worktree。

## 5. Make Tail Validation Binding-Aware

- [x] 将 `provenance_tail_manifest_errors()`、commit validator、publication identity 与 pre-PR detector
  统一消费 private binding。
- [x] self-hosted postcondition 保持 source commit/ref 绑定 reviewed head。
- [x] installed postcondition 绑定 manifest source repo 与 exact extension commit，不写入 business HEAD。
- [x] 保持 allowed fields、manifest-only changed path、direct parent、single-tail 与 FF-only contract。
- [x] 保持 matching post-bind recovery 先于 provenance inference。
- [x] 为 source resolution 与 binding mismatch 增加稳定 error code/field path，禁止泄露 remote credential。

## 6. Update Canonical Contracts And Docs

- [x] 更新 Finalizer `SKILL.md`/contract、README 与 interface-facing说明；public ids、profiles、exits、
  projection 不变。
- [x] 更新 `.trellis/spec/workflow/data-contracts.md` 的 target parent 与 extension source binding。
- [x] 更新 `.trellis/spec/workflow/companion-scripts.md` 的双 checkout executor 与 failure boundary。
- [x] 更新 `.trellis/spec/workflow/skill-package-contract.md` 的 Finalizer package-local ownership。
- [x] 更新 `.trellis/spec/workflow/quality-guidelines.md` 的 self-hosted/installed regression matrix。
- [x] 更新 `.trellis/spec/preset/installer.md` 的 source provenance consumer contract。
- [x] 更新 `.trellis/spec/docs/public-docs.md`、preset README、workflow README 的 source/target 说明。
- [x] 运行 local link、code-fence、whitespace、terminology 与 cross-SSOT contradiction 检查。

## 7. Focused Tests

- [x] Finalizer package contract/runtime tests：两种 binding、source resolution、tail validation、
  reprepare、post-bind ordering、terminal projection。
- [x] Installer/source tests：manifest provenance、canonical origin、exact-OID fetch、clean/detached
  checkout、apply entry。
- [x] Negative fixtures：missing/malformed repo/ref/commit、dirty/mutable、OID mismatch、source dirty、
  apply entry missing、source repo drift、business HEAD overwrite、extra path/field、managed drift、sidecar。
- [x] Installed fixture：target 不含 canonical source tree；从 installed wrapper 完成
  `ready -> reprepare -> reprepare_preview`，verifier call count 为零。
- [x] Regression：self-hosted Guru Trellis closeout、existing-PR recovery、archive/Ready/terminal、Issue
  scope 与 plan digest 不回退。

## 8. Projection And Preset Validation

- [x] 先运行 canonical source package validator 与 focused tests。
- [x] 执行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`。
- [x] 检查并处理 apply 产生的精确 `.new/.bak`；未经单独核对不得删除 sidecar。
- [x] 运行 dogfood overlay drift、source/installed package validators、interface/schema/command
  discovery、canonical/installed/platform byte/mode parity 与 recursive sidecar-zero。
- [x] 再次运行 installed Finalizer focused tests与 preset reapply，证明 idempotent current graph。

## 9. Representative Closeout

- [ ] 创建或复用精确 disposable business repository/Issue 前，向用户展示 repo、base、branch、Issue、
  worktree、预计 PR 与 cleanup 副作用并取得单独授权。
- [ ] 从 clean candidate 安装到不含 canonical source tree 的 business repo。
- [ ] 执行 Publication `ready`、Finalizer preview、`reprepare_required`、execute、
  `reprepare_preview`、push、唯一 Draft PR、archive、Ready。
- [ ] archive 后 public invoke 返回 schema-valid `ready_for_merge`，重复 invoke 不产生新 Git/GitHub
  mutation。
- [ ] 记录该验证只覆盖 #311 normal closeout，不宣称 #267 release matrix、tag 或 Release 通过。

## 10. Phase 2, Review And Promotion

- [ ] 任何 planning 外新场景先走
  `guru-qualify-normal-scenario:implementation_discovery`；qualified boundary 扩大时重新执行
  Architecture implementation-discovery impact。
- [x] 完成 Architecture `task_impact_sync(stage=phase2)`，取得 fresh `baseline_current` /
  `architecture_impact` / `target_native` / `reviewed_candidate`。
- [x] 完成 RDT task delta reconciliation，取得 current `.40` 的 `ssot_current`。
- [x] 执行 `guru-check-task`；当前结果为 `blocked`，无 open P0-P3 finding，唯一 blocking
  unverified item 是尚未取得单独 GitHub mutation 授权的 representative clean business closeout。
- [ ] 使用 `guru-create-task-commit` 创建 exact task commit，只 stage #311 文件。
- [ ] 独立 Branch Review 覆盖 `origin/main...HEAD` 完整 committed diff，P0-P3 open finding 为零。
- [ ] Architecture/RDT contribution 经独立 review 后执行 expected `.40` serialized promotion；
  promotion delta 重新进入 Phase 2、task commit 与 Branch Review。
- [ ] Publication/Finalizer 只消费 fresh promoted/current evidence。

## 11. Expected Change Surface

- `trellis/skills/guru-team/packages/guru-finalize-task/**`
- `trellis/presets/guru-team/**` 与 `trellis/workflows/guru-team/**` 中声明、测试、README、inventory
- `.trellis/spec/workflow/{data-contracts,companion-scripts,skill-package-contract,quality-guidelines}.md`
- `.trellis/spec/preset/installer.md`
- `.trellis/spec/docs/public-docs.md`
- dogfood installed 与 Shared/Codex/Claude/Cursor generated projection
- `docs/requirements-design-test-contributions/311-finalizer-provenance-source-checkout/**`
- `docs/architecture/contributions/311-finalizer-provenance-source-checkout.md`
- `docs/architecture/adr/007-finalizer-extension-source-target-binding.md`
- `.trellis/tasks/08-25-311-finalizer-provenance-source-checkout/**`

出现 public exit/transaction change、verifier re-entry、其它 Issue、业务 repository mutation、Release
Gate、tag/Release 或敌对场景需求时，停止并重新进入 owning route。

## 12. Validation Commands

Implementation 开始后由 `trellis-before-dev` 按 current package command inventory 精确解析命令；
最低验证集合包括：

```text
Finalizer canonical package tests
Finalizer installed package tests
preset installer/source provenance tests
source and installed package validators
all-platform preset apply and dogfood drift
canonical/installed/Shared/Codex/Claude/Cursor byte and mode parity
recursive .new/.bak/unknown-sidecar zero check
task.py validate <task>
git diff --check
representative clean business closeout
independent current-HEAD Branch Review
```

未执行的 #267 release-wide matrix、tag-pinned smoke、tag 与 GitHub Release 必须列为明确边界。
