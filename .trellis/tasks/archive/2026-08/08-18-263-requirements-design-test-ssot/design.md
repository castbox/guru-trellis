# 设计：guru-maintain-requirements-design-test-ssot

## 1. 设计原则

该 Skill 是 Requirements、Design、Test 三层 repository authority 的一个原子语义 owner，而不是三个彼此重复判断的 wrapper。global workflow 只负责 mandatory invocation、profile caller 与 typed-exit routing；package-local contract 独占完整 forward behavior、AI Review Gate、必要确认、recorder/validator 与 re-entry。确定性 runtime 不判断文档充分性、authority、版本、冲突、revision 或 route。

实现以 `guru-maintain-architecture-baseline` 的 Interface 1.4 package/layout 为兼容先例，但使用 #263 自己的四 profile、五出口与 R/D/T traceability 语义，不复制 Architecture authority，也不修复先例中的无关行为。

## 2. Authority 与 contribution 模型

### 2.1 Canonical authority

目标 repository 的标准逻辑目录遵循 Issue #263：

```text
docs/requirements/{README.md,versions/<version>/**}
docs/design/{README.md,versions/<version>/**}
docs/test/{README.md,versions/<version>/**}
```

每层 README 拥有 current entry、version matrix 与 historical navigation；version 目录拥有正文、decisions、traceability 和 changes。Skill input 接受 repo-relative canonical locator，因此能复用已审查为兼容的 authority；AI 负责判断兼容性和迁移策略。

### 2.2 Task-owned contribution

标准稳定 boundary 为：

```text
docs/requirements-design-test-contributions/<task-ref>/
  manifest.yaml
  requirements.md
  design.md
  test.md
  traceability.md
```

具体业务 repository 能使用其已审查为兼容的 task-owned locator。一个 contribution 只属于一个 task/ref；普通 task 不更新 shared current docs 或 index。`promotion` 以 contribution locator、目标 version 与当前 authority freshness 为输入，重读 live authority 后完成语义 review；失败只返回当前 contribution 的 re-entry。

### 2.3 Traceability

稳定逻辑边为：`requirement_id / behavior_id -> design_responsibility_id / contract_id -> test_strategy_id / scenario_id / case_id`。traceability 保存 id、locator、version/status 和关系，不复制正文。删除/替换/拆分/合并必须同时给出 predecessor/successor 与 historical boundary。

## 3. 四个 profile

### `bootstrap_foundation`

输入 caller/repository locator、目标 version 与适用 scope；存在 existing authority 时同时输入其 locator，不存在时省略该字段。AI 审查新建/复用/迁移、provenance、版本状态、三层完整性与 #264 architecture inheritance。正常出口为 `ssot_current` 或 `baseline_incomplete`；需要受控修复时返回 `sync_required`，无法继续时 `blocked`。

### `task_impact_sync`

输入 task locator、当前 authority locator/version/freshness 与 task delta locator。AI 识别受影响 requirement/behavior/design contract/test scenario/case，决定 no-op、task-owned contribution、direct canonical sync（仅无并行冲突时）或 revision。正常出口为 `ssot_current`、`sync_required` 或 `revision_required`。

### `promotion`

输入由 `sync_required` 最小 seed 投影的 contribution/authority identity，以及 caller 补充的固定 profile。AI 重读 contribution 与 canonical authority，审查 traceability、subtraction、version/historical boundary 和 #264 inheritance，成功后返回 `ssot_current`；普通 stale/缺失可返回 `sync_required`/`revision_required`，基础不完整返回 `baseline_incomplete`。

### `repair`

输入 authority locator、problem scope 与 freshness。AI 修复 incomplete/stale/conflict/version/navigation/migration 问题；不得借 repair 扩张业务需求或重写无关历史。成功返回 `ssot_current`，仍需同步时 `sync_required`，需上游修订时 `revision_required`，基础不足时 `baseline_incomplete`。

## 4. Public I/O 与 typed exits

四个 profile 使用各自 schema 与 example，通过 aggregate `oneOf` 仅作验证索引。公共输入只含 caller 必须主动提供的 locator、profile identity、version/scope 与必要 freshness；AI owner result 保持 call-local。

- `ssot_current`: `authority_locator`、`active_version`、`status`、`applicability_scope`、最小 `freshness`；consumer 为 current workflow router。
- `sync_required`: `authority_locator`、`target_version`、`contribution_locator`、`sync_kind`、最小 `freshness`；以 `skill_input_authoring_seed` 回到本 Skill `promotion`/`repair`。
- `revision_required`: `task_locator`、`affected_scope`、`authority_locator/version`、revision code；consumer 为 planning/implementation router。
- `baseline_incomplete`: `authority_locator`、known status/scope、missing layer code；consumer 为 Bootstrap/controlled repair router。
- `blocked`: 稳定 `reason_code` 与最小 remediation；consumer 为 fail-closed stop。

每个字段必须在 interface 中绑定直接 consumer use。完整 scan、文档全文、diff、review narrative、分类历史、hash bundle、Git 状态、授权与 recorder 状态不得进入 public DTO。

## 5. Consumer 与 workflow 接入

canonical workflow 和 dogfood workflow 添加一个 mandatory invoke 与五个唯一 exit markers；新增 current、bootstrap、planning 三个 workflow router 和一个 blocked stop target。router 只做薄 projection，不重新判断语义。Planning/Phase 2/Branch Review/Publication/Acceptance/Finish 继续从 live authority 读取直接需要的 R/D/T SSOT status、locator 与 freshness，不读取 package-private result，不在 #263 原地扩展既有 public DTO。实现若证明现有 DTO 必须承接新字段，则发布新版本 schema/interface 并保留旧版本语义。

live 基线为 19 active package、70 command、19 complete command、80 package exit，以及 18 business invoke、78 business exit、28 workflow target、19 stop target。新增 package 和路由后的精确目标为 20/71/20/85 与 19/83/31/20。validator 与测试以 registry/workflow 实际集合为 authority；仅在 #263 接入必须触及的文件中移除陈旧固定计数，不把该动作扩张为 #264 repair。

Architecture inheritance 通过 #264 public baseline locator/version/status 或 consumer-owned seed 引用；R/D/T package 不读取 #264 私有 result，也不复制 architecture documents。

## 6. Package 与 distribution

canonical package 包含以下固定成员：

- `SKILL.md`、`references/contract.md`、`interface.json`、`commands.json`；
- 四个 profile input schema、aggregate schema、五个 output schema、consumer schema、error catalog；
- package-local deterministic invoke/record/check runtime 与薄 shell wrappers；
- 去敏 examples、四 profile/五 exit eval coverage、contract/runtime tests。

注册与投影更新包括 canonical registry、`.trellis/guru-team/extension.json`/installed registry、production/current inventory、workflow markers、preset managed/ownership inventory、README、dogfood installed package，以及 `.agents`、`.codex`、`.claude`、`.cursor`。canonical 修改后由 preset `apply.sh --repo .` 同步生成副本，不手改生成副本作为 source。

## 7. Freshness、失败与恢复

AI 在每次 profile gate 前重读 target authority、task/contribution 和必要 #264 public identity。validator 校验 current locator、version/status、traceability ids、profile/exit/consumer mapping 与 owner result identity。任何 missing/stale/mismatch/unknown/multiple/unmapped exit fail closed。

普通 contribution conflict 只影响该 contribution。`sync_required` 只回到本 Skill；`revision_required` 回到当前 planning/implementation owner；`baseline_incomplete` 回到 Bootstrap/controlled repair；`blocked` 不携带额外流程状态。不得新增锁、transaction log、shared ledger 或 cross-task cache。

## 8. 验证设计

1. package schema/runtime/tests：四 profile、五 exit、profile/exit mismatch、stale、provenance、traceability、subtraction、Architecture inheritance。
2. 并行边界：两个 task 使用不同 contribution locator；promotion failure 不污染另一个 task identity。
3. consumer graph：registry/interface/extension/workflow 的三个 router、一个 stop target，以及 Planning/Check/Review/Publication/Finish 的 live authority consumption 与 public field consumer use 完整；精确计数达到 20/71/20/85 和 19/83/31/20。
4. distribution：canonical/dogfood/installed/Agents/Codex/Claude/Cursor byte parity、managed paths、executable mode。
5. reapply/drift：preset apply、dogfood drift、recursive zero `.new/.bak`。
6. 一个代表性 clean throwaway：从当前 source 安装 preset，验证 package inventory、workflow marker、public wrapper 的一个 current 与一个 re-entry/stop probe。

不运行完整 multi-platform clean/existing/update/reapply/workflow-switch 或 exact-candidate matrix；这些证据明确 deferred 给 #260/#267。

## 9. 取舍

- 采用一个原子 R/D/T owner，避免三套独立 Skill 对 authority 和 traceability 作不一致判断；代价是 package contract 更丰富，但 public exits 仍保持最小。
- 采用 task-owned contribution 根目录而不是普通 task 直写 shared current docs，换取并行隔离与局部恢复；promotion 增加一步，但不制造人工交接或 shared bookkeeping。
- 保留现有 Docs SSOT strategy 并通过版本化 consumer contract 接入，避免破坏旧 API；不把本 Issue 扩张为全量旧 schema 重构。
