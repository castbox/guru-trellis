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
- [x] `guru-qualify-normal-scenario:requirements_scope_set` 对
  `NS-311-VERIFIER-FAILURE-DIAGNOSTICS` 返回 `classified/qualified_current`；用户接受该 verifier
  diagnostic contract 为当前 #311 scope。后续 Branch Review 对用户明确要求的延迟 Issue closure
  返回 `qualified_approved_expansion`，ledger 改为 refs-only，#311 在生产重试确认最大根因前保持 OPEN。

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
  scope 与 plan digest 不回退；首次 Publication 在没有 existing plan 时仍先解析 target repo 并返回
  schema-valid preview，不读取未初始化的 supersession-only state。
- [x] Finding-fix regression：首次 installed preview 在无 remote branch、无 PR、无 metadata tail 时由
  `prepared` 返回 `reprepare_required/provenance_metadata_tail`，且 push、PR create、archive、Ready 均未
  调用；fresh/post-bind existing-PR recovery 继续先于 provenance inference。
- [x] Existing fixture fresh candidate regression：installed verifier contract test 不再从业务 target
  读取 canonical `trellis/skills/**` adapter，改为从 package-local shared runtime 推导；canonical 与
  dogfood installed verifier 均 `17/17`。

## 8. Projection And Preset Validation

- [x] 先运行 canonical source package validator 与 focused tests。
- [x] 执行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`。
- [x] 检查并处理 apply 产生的精确 `.new/.bak`；未经单独核对不得删除 sidecar。
- [x] 运行 dogfood overlay drift、source/installed package validators、interface/schema/command
  discovery、canonical/installed/platform byte/mode parity 与 recursive sidecar-zero。
- [x] 再次运行 installed Finalizer focused tests与 preset reapply，证明 idempotent current graph。

## 9. Representative Closeout

- [x] 创建或复用精确 disposable business repository/Issue 前，向用户展示 repo、base、branch、Issue、
  worktree、预计 PR 与 cleanup 副作用并取得单独授权。
- [x] 从旧 clean candidate `ea30cac7878bf8f36338e6bfdc67869fbecca009` 安装到不含 canonical
  source tree 的 business repo，并完成 fixture Phase 2、task commit 与 independent Branch Review。
- [x] Branch Review 记录 `BR-311-FIXTURE-001`（P1）：首次 Publication 在没有 existing plan 时读取
  未初始化的 `prospective_git`，56/56 因对应 regression 被删除而 false green；source 已恢复
  regression 并通过 canonical/installed `57/57`。
- [x] validation candidate `8138e3dd355f088ad6d4b43548243134f7bbe7d5` 继续暴露首次无 remote
  branch/PR 时 `prepared` 未进入 provenance inference；source 已修复并以真实 preview/context 回归
  证明 `reprepare_required/provenance_metadata_tail` 与 mutation call count 为零，canonical/installed
  各 `58/58`。
- [x] current candidate `a03f8ad1bf2bb98575df4a9376a88b480c7bfd5f` 的第 2 次 throwaway 诊断在
  source caller inventory gate 停止：Finalizer apply second-hop 的完整 AST 内容锚点已随
  `target_reviewed_checkout` / `extension_source_checkout` 分离从 `004063a10598...` 合法演进为
  `f16c2314ce2a...`。canonical inventory 已只保留新 identity；focused routing tests `44/44`、source
  `check-inventory`、JSON 与 whitespace checks 通过。后续 candidate
  `cdc55ca93bc28934bfaa1c4ba48aeef83baf3277` 的第 3 次且最后一次 throwaway 已越过 inventory 并
  进入 default compatibility matrix，但失败后只剩 stdout/stderr hash/size；matrix
  cell/stage/command/error-tail 随 temporary workspace cleanup 丢失。对 `cdc55ca9` 禁止第 4 次。
- [x] 在 canonical `guru-verify-extension-installation` 与 compatibility matrix helper 增加 bounded
  structured failure facts，覆盖 pre-matrix/matrix-cell/post-matrix、outer parsing、schema/example 与
  credential-safe tests；本步不得运行完整 matrix/throwaway/live install。
- [x] all-platform preset apply 同步 verifier package projection，运行 source/installed package validator、
  focused tests、byte/mode parity、ownership 与 sidecar-zero。
- [x] Branch Review finding-fix：保留 preset direct subprocess 的真实 helper/exit identity；补齐 AWS/GCP
  credential query 参数脱敏；matrix 外 command 与 inventory/ownership/sidecar/capability postcheck 失败
  生成 `postcheck_failure`，schema 拒绝 failed + null failure。
- [x] finding-fix fresh local regression：canonical/installed Finalizer 各 `58/58`，canonical/installed
  verifier 各 `17/17`，preset installer `81/81`，upgrade contract `36/36`，routing `44/44`，ownership
  `7/7`；source/installed validator、dogfood drift、upstream ownership、task validate、compile/JSON、
  sidecar-zero 与 `git diff --check` 通过。Finish integration 的 fresh pre-commit rerun因当前 source 尚未
  形成 clean commit 正确停止于 `provenance_tail_source_not_clean`，必须在 finding-fix commit 后对 exact
  clean candidate 重跑，不得记为当前通过。
- [x] finding-fix commit `ff1ace8950f127326b7524e0120ed4032f6c1aef` 后 reapply 得到 clean source
  provenance；fresh Finish integration 越过 `provenance_tail_source_not_clean` 后先暴露 compatibility
  harness 仍跳过 `reprepare_required`，修正为两段 gate/execute 后继续暴露 executor 错误要求 absent
  remote 等于 reviewed head。source preflight 已改为仅接受 absent remote 或精确 reviewed head，非空 drift
  仍 fail closed；canonical/installed Finalizer 各 `59/59`，apply/validator/parity/sidecar-zero 通过。完整
  integration 必须在本轮 finding-fix 形成下一 clean commit 后重跑。
- [x] absent-remote finding-fix commit `b1d6fc00bed7c933b2b9613c5e6a8cfae604f9a5` 后 reapply 绑定 clean
  source provenance。完整 Finish integration 第一次暴露 harness 中已删除的 `finalization_input_rel`，第二次
  暴露 archive 后误用 `reprepare_preview` 导致其旧 `publication_head` 正确返回
  `finalization_stale`；最终修正为 terminal public invoke 复用原始 `publication_ready` 输入并消费第二轮
  gate 的精确 retired locator。Finalizer terminal projection 定点测试、all-platform installer 投影测试及
  第 3 次且最后一次本地完整 integration 均通过（`Ran 1 test in 378.336s, OK`）；本轮不得第 4 次完整
  integration。
- [x] `4a50f88eaee972829aa636af54a5d2d0c033c011` 的 distinct fresh-final Branch Review 已闭环
  `BR-311-SOURCE-004/005`，并发现 `BR-311-SOURCE-006`（P1）：`b1d6fc00` 为 installed closeout
  fake `git` 增加 `subprocess` 后，generated-shebang helper identity 已演进为 `07004913deeb...`，caller
  inventory 仍保留 `da71f59de8d1...`。canonical inventory 已替换为唯一当前 identity；本修复只刷新
  owner/kind/classification/launcher/ordinal 不变的确定性 anchor，不修改 caller 或 routing 机制，且不运行
  第 4 次完整 integration。
- [ ] 从上述 finding-fix 生成新的 clean candidate object，在现有 fixture worktree 上重新安装并完成
  fresh Phase 2、finding-fix commit 与 independent fresh-final Branch Review。
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
- [x] 旧 candidate 的 `guru-check-task` 曾因 representative closeout 尚未授权返回 `blocked`；授权后
  fixture Branch Review 形成 `BR-311-FIXTURE-001`，已返回 implementation finding-fix 并完成 source
  regression。prepared-state finding-fix 后，当前完整 worktree candidate 已重新执行 fresh Architecture
  Phase 2 与 `guru-check-task:finding_fix_rerun`，checker 与 public wrapper 均返回 `passed`，未复用旧
  checkpoint。
- [x] caller inventory 与 verifier evidence scope change 后已重新执行 fresh Architecture
  implementation-discovery/Phase 2、RDT reconciliation 与
  `guru-check-task:finding_fix_rerun`；Architecture 两阶段均返回 `baseline_current` /
  `architecture_impact` / `target_native` / `reviewed_candidate`，RDT 返回 `ssot_current`，Phase 2
  recorder、checker 与 public wrapper 返回 `passed`，未复用旧 checkpoint。
- [x] 使用 `guru-create-task-commit` 创建 finding-fix commit
  `ff1ace8950f127326b7524e0120ed4032f6c1aef`，只 stage 当轮 #311 文件。
- [x] 当前 terminal public-invoke harness finding-fix 重新执行 fresh Architecture/RDT/Phase 2 后创建 exact
  revision commit `c3bc809b548f7a94e2175c82fe32171a5b8762a9`。
- [ ] 独立 Branch Review 已覆盖 `origin/main@d907fcc5...4a50f88e` 的 6 commits / 85 paths；
  `BR-311-SOURCE-001..005` 已闭环，当前 `BR-311-SOURCE-006`（secondary generated-shebang caller
  inventory drift）仍在本 finding-fix 轮处理，尚未达到 P0-P3 open finding 为零。
- [ ] Architecture/RDT contribution 经独立 review 后执行 expected `.40` serialized promotion；
  promotion delta 重新进入 Phase 2、task commit 与 Branch Review。
- [ ] Publication/Finalizer 只消费 fresh promoted/current evidence。

## 11. Expected Change Surface

- `trellis/skills/guru-team/packages/guru-finalize-task/**`
- `trellis/skills/guru-team/packages/guru-verify-extension-installation/**`
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`
- `trellis/presets/guru-team/scripts/python/verify_trellis_compatibility_matrix.py`
- `trellis/presets/guru-team/**` 与 `trellis/workflows/guru-team/**` 中声明、测试、README、inventory
- `.trellis/spec/workflow/{data-contracts,companion-scripts,skill-package-contract,quality-guidelines}.md`
- `.trellis/spec/preset/installer.md`
- `.trellis/spec/docs/public-docs.md`
- dogfood installed 与 Shared/Codex/Claude/Cursor generated projection
- `docs/requirements-design-test-contributions/311-finalizer-provenance-source-checkout/**`
- `docs/architecture/contributions/311-finalizer-provenance-source-checkout.md`
- `docs/architecture/adr/007-finalizer-extension-source-target-binding.md`
- `.trellis/tasks/08-25-311-finalizer-provenance-source-checkout/**`

当前 scope 的 verifier re-entry 仅限 failure evidence；出现 public exit/Finalizer transaction change、verifier
lifecycle owner change、其它 Issue、业务 repository mutation、Release Gate、tag/Release 或敌对场景需求
时，停止并重新进入 owning route。

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
verifier failure projection/schema/example focused tests（不运行完整 matrix）
task.py validate <task>
git diff --check
representative clean business closeout
independent current-HEAD Branch Review
```

未执行的 #267 release-wide matrix、tag-pinned smoke、tag 与 GitHub Release 必须列为明确边界。
