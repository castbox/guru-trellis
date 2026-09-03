# Research: Finalizer provenance metadata tail transaction rebind

- Query: 只读研究 GitHub Issue #342；核对 `owner.py` 调用顺序、旧 `ordinary_publication/push_content` transaction 与新 plan identity 的合法 rebind 条件、#338 复用点、最小测试矩阵，以及 canonical/dogfood/installed/platform 投影。
- Scope: mixed
- Date: 2026-09-03

## Findings

### 1. Live authority and reproduced state

- GitHub Issue #342 当前为 Open，目标是在任何 mutation 前处理 provenance-only identity 演进，再恢复既有 PR；明确不关闭、删除、重建 PR，不人工改 transaction，不吸收 #333 业务实现。
- GitHub PR #337 当前仍为 Open、Ready、同仓库非 fork，`headRefOid=db49b964e72b4f59f9ef8285dce2b54d8917db10`，base/head 为 `main` / `fix/333-create-task-workspace-issue-recovery`。截至 2026-09-03 live mergeability 为 `CONFLICTING` / `DIRTY`；这是后续 Merge readiness 的 live 状态，不改变本 Issue 的 pre-merge Finalizer transaction 研究边界。
- Issue #342 与当前 task planning 均声明新 reviewed identity 为 `a4a9a399d594aa7a12fa3171cb2b12a1e3576508`，旧 publication/PR/remote identity 为 `db49b964e72b4f59f9ef8285dce2b54d8917db10`。因此两个 identity 在问题陈述中是明确不同的。

### 2. Files found

- `trellis/skills/guru-team/packages/guru-finalize-task/runtime/owner.py` - Finalizer plan preparation、provenance-tail validation、transaction validation/recovery、preview 与 execute 顺序的 canonical runtime。
- `trellis/skills/guru-team/packages/guru-finalize-task/tests/test_contract.py` - #191 provenance-tail、#208/#251 existing-PR recovery 与 #338 unbound equal-HEAD 的 focused/real-topology tests。
- `trellis/skills/guru-team/packages/guru-finalize-task/references/contract.md` - 当前 Finalizer 6.0 input、5.0 gate、3.0 private transaction 和 recovery 顺序合同。
- `trellis/skills/guru-team/packages/guru-finalize-task/schemas/finalization-transaction.schema.json` - 当前 private transaction 3.0 的闭合字段与 mode/stage 约束。
- `.trellis/tasks/archive/2026-09/09-02-338-finalizer-unbound-equal-head-recovery/{prd.md,design.md,implement.md}` - #338 的 exact-plan equal-HEAD 资格、transaction conversion 和测试矩阵。
- `.trellis/tasks/archive/2026-08/08-08-191-finalizer-clean-provenance-reprepare/design.md` - reviewed/publication 双 HEAD、单次 manifest-only provenance tail 与 pre-PR reprepare 原始边界。
- `.trellis/spec/workflow/{data-contracts,companion-scripts,quality-guidelines}.md` - transaction、single-tail、existing-PR recovery、验证范围与 generated projection 的 durable contracts。
- `.trellis/spec/preset/{installer,overlay-guidelines,upstream-ownership}.md` 与 `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py` - canonical 到 installed/shared/platform 的实际分发规则。

### 3. Current `owner.py` call order and root cause

当前 active-task preview 顺序是：

1. 读取 `current_transaction`，再读取 Publication owner result（`owner.py:12330-12337`）。
2. `prepare_closeout()` 使用当前 Publication DTO 重建新 plan（`owner.py:12381-12400`）。
3. 若 transaction 存在，立即执行 `finalization_validate_transaction_plan(current_transaction, plan)`（`owner.py:12401-12407`）。该校验通过 `finalization_transaction_from_plan()` 重建完整 expected transaction 并要求对象全等（`owner.py:11200-11225`）。
4. plan identity 不等时，只有 post-bind `existing_pr_recovery` 的 `archive|push_archive|mark_ready` 会先尝试 retired-projection rebind（`owner.py:12408-12418`）；其它 transaction 全部先进入 `finalizer_current_transaction_base_evolution_supersession_preflight()`（`owner.py:12419-12437`）。
5. generic current-transaction supersession 只接受历史 `next_transition=verify`、无 PR/verification binding、marketplace required、旧 publication 到新 reviewed 的 ancestry 和无既有 PR等条件（`owner.py:4357-4418`）。当前 transaction 已是 `ordinary_publication/push_content`，所以稳定返回 `provenance_reprepare_base_evolution_mismatch`。
6. 失败分支若成功才会把 state 设为 `reprepare_required`（`owner.py:12438-12443`）。existing-PR classification 直到其后才调用（`owner.py:12482-12486`）；而 `finalization_existing_pr_recovery_context()` 对 `reprepare_required` 直接返回、不分类 PR（`owner.py:8221-8224`）。

结论：#342 不是 #338 classifier 本身缺条件，而是 plan-mismatch 分派顺序使旧 ordinary transaction 在到达 #338 前被 legacy `verify` supersession contract 拒绝。

### 4. What #338 actually permits

- #338 的 entry predicate 是 exact current-plan `ordinary_publication/push_content`、`pr=null`、`adopted_pr=null`，并先调用完整 transaction-plan equality validation（`owner.py:8015-8029`）。
- 它要求 live remote HEAD 与 PR HEAD 相等，并且还必须等于**当前 plan** 的 `publication_head`；否则返回 `existing_pr_unbound_equal_head_required`（`owner.py:8055-8077`）。
- conversion 进一步硬编码 `ancestry=equal`、`push_required=false`、`pre_push_remote_head=current publication_head`，然后生成 `existing_pr_recovery/bind_pr` transaction（`owner.py:8132-8185`）。
- converted transaction 在首个外部 mutation 前持久化，后续复用 metadata convergence、archive、archive push、Ready handling 和 terminal projection（`owner.py:8187-8213`, `owner.py:10589-10613`）。
- #338 测试已覆盖 fresh equality rejection、exact ordinary stage、original metadata binding、already-converged retry、Ready/Draft、metadata equal/trailing-LF、零重复 push/PR-create/edit/archive/Ready 等（`test_contract.py:4093-4511`, `test_contract.py:2652-2678`, `test_contract.py:3123-3345`）。

### 5. Critical identity contradiction in the current #342 plan

当前事实同时声明：

- old PR/remote HEAD = `db49...`；
- new current plan reviewed/publication identity = `a4a9...`；
- 两者不同；
- rebind 后要复用 #338 `equal-HEAD` 且 `push_required=false`。

这四项不能在当前合同下同时成立。#338 equality 比较的是 live remote/PR HEAD 与**新 plan publication_head**，不是 predecessor transaction publication head（`owner.py:8055-8077`）。若新 plan publication head 为 `a4a9...`，live remote/PR 仍为 `db49...`，则只能是 strict ancestor 或 drift，不能是 equal。

因此实现前必须由 planning authority 明确选择下列一种可验证语义：

- **Strict-ancestor recovery（与现有身份模型一致）**：先对旧 transaction 做 provenance-only plan rebind，再将唯一 PR 作为 current plan publication HEAD 的 strict ancestor recovery；`pre_push_remote_head=db49...`、`push_required=true`，只推送新的 `a4a9...` publication commit，不重复推送旧 `db49...`。后续复用 #208/#338 的 PR binding、metadata decision、archive 与 retry 机制。此路径不满足当前文案中的 `push_required=false`。
- **Equal-HEAD recovery**：只有 live remote/PR 已经等于新 plan publication HEAD 时才能复用 #338 conversion 原样；这与 #342 当前真实复现“仍停在旧 publication HEAD”不一致，需要 live authority 或验收条件变化。

不建议通过把新 plan `publication_head` 回退为旧 PR HEAD 来制造 equality：durable contract 要求 `publication_head` 等于 `branch_review_commit` 或其单个合法 provenance-tail child，并作为 archive parent、remote/PR expected HEAD（`.trellis/spec/workflow/data-contracts.md:1642-1649`）。旧 ancestor 不能作为新 reviewed plan 的 publication identity。

### 6. Legal rebind conditions

若 authority 选择 strict-ancestor 语义，最小 package-private rebind predicate 应在 generic base-evolution supersession 之前运行，并要求：

- transaction 是 current schema 3.0、`mode=ordinary_publication`、`next_transition=push_content`、无 `pr`/`adopted_pr`；其它 mode/stage 直接不适用。
- 不变字段精确相等：`task_ref`、`repo_ref`、`base_branch`、`branch`、Publication `title/body`、完整 `close_issues`。transaction 3.0 不保存 `remote`，因此不能声称“predecessor/current remote 字段相等”；只能使用 current plan remote 加 live remote repository validation。schema 字段见 `owner.py:11106-11145` 和 `finalization-transaction.schema.json:6-54`。
- 允许变化只限 `branch_review_commit`、`publication_head`、`plan_digest`，且变化必须由现有 provenance-tail validator 证明。不要用 commit message、路径名计数或新的 metadata classifier。
- predecessor publication 到 current identity 必须是一个直接子提交、唯一 changed path 为 `.trellis/guru-team/extension.json`、manifest 变化满足既有 allowlist（`owner.py:3768-3863`）。当前 durable contract 明确只允许 `branch_review_commit` 本身或其 **single validated provenance metadata-tail child**（`.trellis/spec/workflow/data-contracts.md:1642-1649`; `.trellis/spec/workflow/companion-scripts.md:1059-1064`）。
- task 必须仍 active/unarchived；无 finish summary/archive locator materialization、无另一 transaction/gate owner 冲突；Issue close scope、Publication payload、Publication/Finalizer gate freshness均 current。
- 唯一 Open PR 必须为同 repository/base/head/head repository、非 fork；PR HEAD 必须等于 live remote predecessor publication HEAD；多个、terminal、fork、scope drift、identity drift均在写 transaction 前阻断。
- preview 只返回现有 `existing_pr_recovery` shape 和 current side-effect set，不持久化 rebind projection。execute 必须重跑 predicate/live PR comparison；在首个 Git/GitHub/archive mutation 前一次性写入 current-plan bound recovery transaction。

推荐一次性写最终 `existing_pr_recovery` transaction，而不是先写 rebound ordinary transaction再写 #338 conversion：两次 owner-private 写之间新增了无外部收益的中断状态。可以复用 #338 的 metadata comparison/adopted PR construction，但 strict-ancestor 时不能直接调用硬编码 equal/no-push 的 `finalization_convert_unbound_equal_head_transaction()`。

### 7. #338 reuse points

可直接复用：

- `resolve_closeout_pull_request()` 与 terminal/multiple/fork identity validation；
- `classify_existing_pr_recovery()` 的 strict-ancestor PR/remote/scope/metadata classification（`owner.py:7924-8013`）；
- `finalization_validate_recovery_metadata_decision()`（`owner.py:8086-8130`）；
- schema 3.0 `existing_pr_recovery` + `adopted_pr` 形状；
- `finalization_pre_mutation_remote_preflight()` 的 bound PR、scope、metadata convergence/retry validation（`owner.py:8470-8612`）；
- existing archive、push_archive、Ready/terminal transaction engine和 #338 real-topology mutation counters。

不能原样复用：

- `classify_unbound_equal_head_recovery()`，因为它要求 current publication equality；
- `finalization_convert_unbound_equal_head_transaction()`，因为它要求 `ancestry=equal`、`push_required=false`；
- generic `finalizer_current_transaction_base_evolution_supersession_preflight()`，因为它是退役 `verify` transaction 的窄迁移合同且拒绝已有 PR（`owner.py:4357-4418`, `owner.py:4574-4588`）。

### 8. Minimal test matrix

#### Focused helper/preview

- Positive: old ordinary/push_content/unbound transaction；old publication == remote == PR HEAD；new current plan为一个合法 direct-child provenance-only identity；payload/scope/task/repo/base/head不变。
- Positive variants: Ready/Draft x metadata equal/trailing-LF convergence。
- Boundary: old reviewed==old publication；old publication itself is a validated historical tail。不要新增“任意多 tail chain”正例。
- Negative: mode/stage/binding mismatch；payload/scope/task/repo/base/head drift；non-manifest path；额外 path；非法 manifest field/action；merge commit/multiple commits；broken/non-ancestor lineage；current plan/gate stale；archive/summary已开始；multiple/terminal/fork PR；remote/PR mismatch；preview后 HEAD/metadata/scope drift；未知 transaction字段。

#### Execution/idempotency

- Assert owner transaction binding write precedes content push/PR edit/archive/Ready mutation。
- Strict-ancestor semantics: exactly one push of new publication HEAD；PR create=0；metadata edit=0/1；archive move/commit/push各 1；Ready PR mutation=0，Draft=1。
- Interrupt/retry at transaction bind、after publication push、after metadata edit before stage advance、archive move、archive commit/push、Ready output loss；每个已完成 mutation不重复。
- Preserve existing #338 exact equal-HEAD tests unchanged，证明本修复没有放宽 fresh equality 或 current-plan exact transaction path。

#### Package/distribution

- Canonical Finalizer tests and installed Finalizer tests。
- Finish-family integration and real wrapper/facade recovery case。
- Source/installed package validation、ownership、dogfood drift、all-platform preset reapply、recursive `.new/.bak/.rej/.orig` zero、task validation、diff hygiene。
- 不执行完整 marketplace/update/tag-pinned/Release Gate matrix；这是普通 workflow defect 的明确 deferred boundary（`.trellis/spec/workflow/quality-guidelines.md:887-924`；`.trellis/spec/preset/installer.md:712-717`）。

### 9. Canonical, dogfood, installed, and platform projection

- Canonical semantic/runtime source: `trellis/skills/guru-team/packages/guru-finalize-task/**`。
- Dogfood installed full package: `.trellis/guru-team/skills/packages/guru-finalize-task/**`。当前 canonical 与 installed 均为 101 files，逐文件 bytes 相等。
- Shared/Codex/Claude/Cursor public discovery projection: `.agents/skills/guru-finalize-task/**`、`.codex/skills/guru-finalize-task/**`、`.claude/skills/guru-finalize-task/**`、`.cursor/skills/guru-finalize-task/**`。当前各为 64 public files，均与同路径 canonical bytes 相等；runtime/tests 只安装到 `.trellis/guru-team/skills/packages/**`，platform roots 只携带 `skill_platform_public_files()` 选出的 public package files（installer `apply_guru_team_trellis_preset.py:1231-1262`, `:1840-1884`）。
- 修改应只落 canonical package、directly-hit durable specs 与 task-owned RDT delta，再通过 preset `apply.sh --repo . --all-platforms` 生成 dogfood/platform copies。不得直接编辑 generated copies（`.trellis/spec/preset/overlay-guidelines.md:58-71`, `:120-152`）。
- 当前未发现 `.new`、`.bak`、`.rej`、`.orig` sidecar。

### 10. External references

- GitHub Issue #342: `https://github.com/castbox/guru-trellis/issues/342`（live authority，Open，读取于 2026-09-03）。
- GitHub Issue #338: `https://github.com/castbox/guru-trellis/issues/338`（Closed，#338 contract source）。
- GitHub PR #340: `https://github.com/castbox/guru-trellis/pull/340`（Merged 2026-09-02，merge commit `fbb9ffded71e3bb9d8613d691a0722c607db81ae`）。
- GitHub PR #337: `https://github.com/castbox/guru-trellis/pull/337`（live reproduction PR；Open/Ready，head `db49...`）。
- Trellis custom workflow: `https://docs.trytrellis.app/advanced/custom-workflow.md`。官方文档确认 workflow/phase/skill routing 的控制面属于 `.trellis/workflow.md`，确定性 runtime bug 应保持 package-local script/runtime ownership，不修改上游 Trellis。
- Trellis custom spec template marketplace: `https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md`。官方文档明确 template 用于可复用规范，不用于 active task/private runtime；本 Issue 的 transaction recovery state继续保持 ignored owner-private。

### 11. Related specs

- `.trellis/spec/workflow/semantic-retrieval.md` - concept-family 和 negative-conclusion evidence contract。
- `.trellis/spec/workflow/data-contracts.md:1343-1405` - current Finalizer transaction 和 #338 recovery contract。
- `.trellis/spec/workflow/data-contracts.md:1642-1699` - single provenance tail、pre-PR reprepare 和 existing-PR precedence。
- `.trellis/spec/workflow/companion-scripts.md:20-53` - transaction engine、pre-mutation remote/PR preflight 和 private owner state。
- `.trellis/spec/workflow/quality-guidelines.md:887-924` - existing-PR/equal-HEAD recovery tests和 source/installed/platform assertions。
- `.trellis/spec/preset/overlay-guidelines.md:58-71,120-152` - canonical/generated projection 与 reapply/drift/sidecar contract。
- `.trellis/spec/preset/installer.md:101-105,712-717` - installed/package/platform distribution 和 focused Finalizer recovery validation boundary。

## Caveats / Not Found

- **Critical planning caveat:** 当前 #342 的“remote/PR 仍为旧 `db49...`”与“对新 `a4a9...` plan 复用 #338 equal-HEAD、`push_required=false`”互相冲突。未澄清前，不应进入实现；否则测试只能通过改变真实拓扑或弱化 current plan identity。
- 当前 transaction 3.0 不保存 `remote` 字段。规划中“predecessor/current remote 完全一致”不能由 transaction 自身证明；只能依赖 current plan remote 与 live repository remote validation。若必须持久化 predecessor remote，意味着 private schema contract变化，需要重新评审，而不是静默增加字段。
- 当前 provenance validator只证明一个 direct-child single tail；未找到支持任意多 provenance-tail commit chain 的 durable contract或测试。#342 不应新增 multi-tail acceptance。
- Knowledge Center 当前未提供本问题的额外 indexed repository evidence；结论基于 live GitHub authority、当前 worktree code/spec 与 archived #338/#191 task。
- 未运行测试、preset apply、Git diff 或任何 Git/GitHub mutation；本文件是只读研究结论，不是 implementation/validation/release proof。
