# #101 实现 `guru-review-change-request` semantic closed-loop Skill

## 目标

新增公共 Skill `guru-review-change-request`，在 task 创建前审查 change request 是否具备独立交付条件。该 Skill 只消费 current 且已由前置 checker 通过的 context、clarity、wording evidence，由 AI 完成 readiness、current/history 一致性、duplicate/reuse、delivery unit、finding 与 typed exit 判断；deterministic runtime 只校验 schema、hash、digest、linkage、record/check 事实。

## 需求清晰度结论

Live Issue #101 已固定目标、输入、AI Review Gate、五个出口、artifact 生命周期、脚本边界、范围排除与验收口径。Live #98 和 #112 固定跨 Skill 顺序与下游职责；当前 main 已包含 #109、#111、#113、#114、#128 的实现。仓库证据已回答现状、duplicate、ownership、legacy route 与 archived history 问题。本任务没有阻塞规划的产品问题。

## 已确认事实

- Source issue: https://github.com/castbox/guru-trellis/issues/101
- #98 与 #112 当前为 open；#101 是本分支唯一交付单元，PR 只关闭 #101。
- #109、#111、#113、#114、#128 当前为 closed，且实现已进入 live `main` 基线 `9087987b9239168e00063a2ac89e9ae3d186d6cf`。
- 当前 registry、runtime、extension manifest 和 workflow 尚未包含 `guru-review-change-request`。
- 当前 `guru-review-contract-wording:change_request:pass` 仍直接进入 `guru-full-task-intake-chain`，缺少 #101 readiness owner。
- #112 尚未实现；本任务只声明 `ready -> guru-create-task-workspace` 的稳定 consumer/transition，不创建 workspace。
- Phase 0 context preview 中 `invalid_index_shape` 可在正常 history preview 复现，但 reader 已逐项隔离该记录，preview 仍返回有效候选并通过 `context_ready`。该现象不阻塞 #101，且不进入本任务实现。

## 范围

### In Scope

1. 创建并注册 public semantic package `guru-review-change-request`，支持 workflow 与 standalone 两种 mode。
2. 消费以下 current、checker-validated evidence：
   - `guru-discover-change-context:context_ready`
   - `guru-clarify-requirements:clear`
   - `guru-review-contract-wording:change_request:pass`
3. 支持 `existing_issue`、`proposed_draft`、`standalone_request` 三类 target。
4. AI Review Gate 固定审查 requirement completeness、delivery unit、implementation target、claimed old behavior、current implementation、docs/code/tests consistency、archived constraints、duplicate/reuse、target authority 与 prerequisite linkage。
5. 实现五个稳定出口及唯一 consumer：
   - `ready -> guru-create-task-workspace`
   - `clarify_requirements -> guru-clarify-requirements`
   - `review_wording -> guru-review-contract-wording`
   - `refresh_context -> guru-sync-base`
   - `blocked -> stop`
6. 新增 `issue-review.json` 公共 artifact contract、schema、去敏 example、recorder/checker wrapper 与 runtime command。Pre-task 执行只在 stdout 返回结果，不写 repo；#112 后续负责 task-local 持久化。
7. 更新 canonical workflow/runtime/registry/extension manifest、preset installer/inventory/README、durable requirements/spec、canonical package、dogfood runtime 与 shared/Codex/Cursor/Claude discovery copies。
8. 新 package 与 replacement tests 通过后，移除 Guru-owned active source 中被替代的 readiness route、重复规则或内联 ownership。
9. 验证 source、installed、dogfood、clean throwaway、update/reapply、remote branch-pinned marketplace 与 publish closeout 合同。

### Out of Scope

- 不实现 #112 的 issue/worktree/branch/task 创建、handoff side effect 或 `issue-review.json` task-local 写入。
- 不实现 #129、#130、#131、#132 的 planning approval、Phase 2 replacement、Branch Review replacement或 legacy overlay removal。
- 不复制 #111 的 current/history discovery、#113 的 clarification loop、#114 的 vocabulary/scanner/classification。
- 不修复 #111 的 `invalid_index_shape` archived record；仅在正常路径再次阻塞 #101 时重新进入 scope clarification。
- 不修改、扩展或删除 Trellis upstream-owned 与 `transitional_legacy` overlay；只写 Guru-owned namespace。
- 不修改 Trellis upstream source、全局 npm package 或 `node_modules`。
- 不引入恶意 actor、攻击模型、故意伪造、对抗性输入、TOCTOU、锁、压力并发、额外 fault injection、偶发 crash consistency或跨 OS 原子性设计和测试。

## 功能需求

### FR-1 Public Skill package

- Stable id 必须是 `guru-review-change-request`，registry state 必须是 `active`。
- Package 必须包含 `SKILL.md`、`interface.json`、`references/contract.md`、schema、example、record/check wrappers 与 package tests。
- `judgment_mode` 必须是 `semantic`。
- Ordered stages 必须固定为 `forward_behavior -> ai_review_gate -> conditional_human_confirmation -> recorder_validator -> typed_exit`。
- Workflow 与 standalone 必须声明同一组 entry preconditions，并依赖完整兼容的 Guru Team preset runtime。

### FR-2 Prerequisite evidence 与 target binding

- Context evidence 必须来自 `guru-discover-change-context:context_ready` 的 current checker result，并绑定 base、live target、current docs/code/tests、duplicate facts 和 archived history digest。
- Clarity evidence 必须来自 `guru-clarify-requirements:clear` 的 current checker result，并绑定同一 target/content/scope identity。
- Wording evidence 必须来自 `guru-review-contract-wording` 的 `profile=change_request`、`typed_exit=pass` current checker result，并绑定同一 reviewed content hash。
- `existing_issue` 必须绑定 repo、issue number、URL、authority update time、title/body identity 与 source hash。
- `proposed_draft` 必须绑定 side-effect-free reviewed title/body bytes、draft identity 与 source request digest。
- `standalone_request` 必须绑定显式 request identity、reviewed content hash 与 caller locator。
- 任一 base、target、scope、query、current/history、clarity 或 wording binding stale 时，`ready` 必须被拒绝。

### FR-3 AI Review Gate

AI 必须逐项记录：

1. Problem、goal、scope、non-goals、acceptance、risk boundary 均完整。
2. Close/ref/followup 与单一 delivery unit 一致。
3. Implementation target 有 current evidence 支撑，不是未证实 solution assumption。
4. Change request 声称的旧行为在 current base 仍存在。
5. Current base 未完整实现目标；已有实现与缺口已分开记录。
6. Docs、code、tests 的证据没有未解释冲突。
7. Archived task 没有已完成、替代或否定当前目标；历史约束已进入 scope conclusion。
8. Duplicate/reuse 结论与 current search evidence 一致。
9. Existing issue、draft 或 standalone target 的 owner/locator/hash current。
10. Context、clarity、wording evidence 与当前 target/content hash 完全链接。

AI 必须记录 requirement/scope basis、findings、affected evidence/hash、delivery unit、close/ref/followup、reuse decision、implementation target 和 risk boundary。Recorder/checker 不得生成、补全或推断这些语义字段。

### FR-4 Typed exits

- `ready` 仅在全部 review dimensions 通过、blocking finding 为空、三份 prerequisite evidence current 且 linkage 完整时成立。
- `clarify_requirements` 用于用户决策缺口、delivery unit 冲突或需要新 draft 的情形。
- `review_wording` 用于 wording evidence missing、stale、unchecked 或未通过 `change_request` profile 的情形。
- `refresh_context` 用于 base、live target、scope、query、current/history binding stale 的情形。
- `blocked` 用于原目标已完成且没有独立缺口，或当前 delivery unit 内冲突无法消解的情形。
- 每次结果必须携带恰好一个 scalar typed exit、非空 reason、完整 findings 数组、affected evidence/hash 数组和固定 consumer object。
- Missing mandatory Skill、unknown/multiple/unmapped exit 或 consumer mismatch 必须 fail closed。

### FR-5 Deterministic runtime 与 artifact contract

- Schema id 固定为 `guru-change-request-review-1.0`，artifact basename 固定为 `issue-review.json`。
- Result 必须绑定 target identity、三份 prerequisite evidence identity、current/history linkage、review dimensions、findings、scope conclusion、AI Review Gate、typed exit、consumer 与 facts digest。
- Runtime 只执行 JSON Schema、closed shape、stable enum、SHA-256、canonical digest、evidence linkage、prerequisite checker result、consumer mapping 与 freshness check。
- Runtime 不搜索 duplicate/history，不读取 docs/code/tests 作语义判断，不生成 finding，不选择 delivery unit，不把 scanner 或 validator success 转成 `ready`。
- Recorder 必须只记录 AI 已给出的 review payload；checker 必须重验 objective facts并返回已记录 exit，不得改写 exit。

### FR-6 Side-effect 与 artifact 生命周期

- Workflow pre-task 与 standalone execution 必须 stdout-only，不能写 task、workspace、repo cache、history index 或 fixed tracked runtime。
- Public package example 必须去敏，不能含 active task、workspace journal、secret、本机绝对路径或业务私有状态。
- #112 后续持久化时只能把同一 checker-validated result 写入当前 `{TASK_DIR}/issue-review.json` 并受 Git 跟踪。
- 本任务测试必须证明 recorder/checker 未创建 `issue-review.json` 或其它 repo sidecar。

### FR-7 Workflow integration 与 replacement boundary

- `guru-review-contract-wording:change_request:pass` consumer 必须改为 mandatory `guru-review-change-request`。
- `guru-review-change-request:ready` 必须指向 stable id `guru-create-task-workspace`；该 package 缺失时当前 workflow 停止，不能回退旧 task intake。
- 四个非 ready exits 必须按 FR-4 的 consumer 重入或停止。
- Workflow 只保留 stable ids、required evidence、typed exit transition 和 fail-closed stop，不复制 Skill 内部 dimensions、finding logic 或 schema。
- Replacement verification 通过后，删除 `change_request:pass -> guru-full-task-intake-chain` 旧 route 和 Guru-owned active source 中重复 readiness ownership。
- #112 仍拥有的 environment/issue/worktree/task side effect 流程必须保留；#128 冻结的 upstream/transitional overlay 不得修改。

### FR-8 Distribution 与 ownership

- Canonical package 必须从 `trellis/skills/guru-team/packages/guru-review-change-request/` 分发到 `.trellis/guru-team/skills/packages/` 与 shared/Codex/Cursor/Claude discovery roots。
- Extension public API 必须声明 package、schema、artifact contract、record/check commands 与 managed paths。
- Preset installer、inventory、README、source/installed package validation 必须同步。
- Canonical、installed 与四平台文件 bytes 和 executable mode 必须一致。
- Ownership validator 必须证明 frozen upstream overlay path set、payload hash 与 managed claims未扩大。

### FR-9 Verification 与 publish

- Source package contract/schema/runtime/preset suites必须通过。
- 五个 exits、missing/stale prerequisite、unknown/multiple/unmapped exit 必须有正向与负向测试。
- 三类 target 与 current/history、clarity、wording hash linkage 必须有正向与 stale/mismatch 测试。
- Tests 必须证明 AI Gate 不会被 scanner/validator return value 替代。
- Dogfood apply/drift、clean throwaway workflow marketplace + preset install、`trellis update --force` + workflow/preset reapply 必须通过。
- `.new`、`.bak`、sidecar、removal、conflict 计数必须为零。
- Push 后且 PR 创建前，`trellis-finish-work` 必须执行 remote branch-pinned marketplace verification。
- Phase 2 和 Branch Review 必须记录 secret、CI/CD、container、Kubernetes、DB migration、Makefile 与 deployment impact 结论。

## Docs SSOT 状态

- Docs state: `stale_docs`
- Evidence paths:
  - `docs/requirements/requirement-main.md`
  - `docs/requirements/guru-team-trellis-flow.md`
  - `trellis/workflows/guru-team/workflow.md`
  - `trellis/workflows/guru-team/README.md`
  - `trellis/presets/guru-team/README.md`
  - `.trellis/spec/workflow/skill-package-contract.md`
  - `.trellis/spec/workflow/workflow-contract.md`
  - `.trellis/spec/workflow/data-contracts.md`
  - `.trellis/spec/workflow/companion-scripts.md`
  - `.trellis/spec/workflow/quality-guidelines.md`
  - `.trellis/spec/preset/installer.md`
  - `.trellis/spec/preset/overlay-guidelines.md`
  - `.trellis/spec/preset/upstream-ownership.md`
- Requirement impact: Durable docs 已描述 context、clarity 与 wording prerequisites，但仍缺少独立 change-request readiness owner 和五出口 route。
- Strategy: `ssot_first`
- Task artifact delta: 本 task 保存 #101 的规划、执行与 gate 证据；稳定 Skill、schema、workflow、installer 和 consumer contract 必须写回上述 durable sources。

## 验收标准

- [ ] Public package、interface、contract、schema、example、wrappers 和 tests 均存在并通过 source validation。
- [ ] `judgment_mode=semantic`，AI Gate 与 deterministic runtime boundary 在 contract 和 tests 中一致。
- [ ] Existing issue、proposed draft、standalone request 均有完整 target identity 与 evidence linkage tests。
- [ ] Context、clarity、wording evidence 缺失、过期或 hash mismatch 时，`ready` 均被拒绝并保留 AI 选择的 prerequisite exit。
- [ ] 十个 review dimensions、findings、scope conclusion、affected evidence/hash、reason 与 consumer 均进入 schema 和 example。
- [ ] 五个 exits 具有唯一 consumer，workflow/package tests 拒绝 missing/unknown/multiple/unmapped exit。
- [ ] Scanner/validator success 不能生成 `ready`，缺少 AI-authored Gate 时 recorder/checker fail closed。
- [ ] Pre-task 与 standalone result stdout-only，repo 中不产生 `issue-review.json`、cache、index 或 sidecar。
- [ ] `ready` 只声明 #112 的 `guru-create-task-workspace` consumer，不实现 task workspace 创建。
- [ ] Replacement verification 通过后，旧 `change_request:pass -> guru-full-task-intake-chain` route 和 Guru-owned duplicate readiness owner 已删除；#112 behavior 与 frozen upstream overlay 保持未修改。
- [ ] Canonical、installed、shared/Codex/Cursor/Claude package bytes 与 mode 一致，dogfood drift 为零。
- [ ] Clean throwaway install、`trellis update --force`、workflow/preset reapply、sidecar/removal/conflict 零计数全部通过。
- [ ] Remote branch-pinned marketplace verification 在 push 后、PR 创建前通过。
- [ ] 完整 `trellis-check` 与 `origin/main...HEAD` Branch Review 通过，P0-P3 findings 全部闭环。
- [ ] `issue-scope-ledger.json` 的 `close_issues` 仅含 #101，PR body 只使用 `Closes #101`。
- [ ] `trellis-finish-work` dry-run、closeout plan review 与同 digest formal finish 创建中文 Ready PR，且不合并 PR。

## Open Questions

无。实施中若证据要求改变五出口、#112 consumer、artifact lifecycle、ownership 或正常运行范围，必须返回 Phase 1 更新三份规划并重新取得 post-planning confirmation。
