## 检查完成

### 检查身份与范围

- 角色：独立 Phase 2 `trellis-check` reviewer。
- Task：`.trellis/tasks/07-24-116-review-task-publication`。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/116-review-task-publication`。
- Branch：`codex/116-review-task-publication`。
- 审查 HEAD：`bdc8f50bcd1e325aed331d4b01107b83ed8ee940`。
- Diff/working-tree 范围：`origin/main`/`HEAD` 基线相同；检查了当前完整 tracked 与
  untracked implementation diff，而不是只检查最后一处编辑。
- Boundary：`check-workspace-boundary.sh --json` 通过；expected workspace 与 actual
  repo root 均为上述 task worktree，source checkout status 与 suspicious source
  artifacts 均为空。
- Planning：`check-planning-approval.sh --json --require-exit approved` 通过；approval
  由 `explicit-post-planning-review` 产生，planning bytes/digests、ambiguity review
  与 fixed-scope scanner evidence 均为 current。
- 官方 Trellis 扩展面：复核了
  `https://docs.trytrellis.app/advanced/custom-workflow` 与
  `https://docs.trytrellis.app/advanced/custom-spec-template-marketplace`；当前实现继续把
  workflow 行为放在 Markdown，将 spec template 限定为可复用工程约定，未发现通过
  upstream source、全局 npm、`node_modules` 或 hook 实现流程分叉。

### 已检查文件

- Task 与 approval：
  `.trellis/tasks/07-24-116-review-task-publication/{prd.md,design.md,implement.md,planning-approval.json,implementation-handoff.md,issue-scope-ledger.json,agent-assignment.json,check.jsonl}`。
- Curated specs：
  `.trellis/spec/workflow/{quality-guidelines.md,skill-package-contract.md,workflow-contract.md,data-contracts.md,companion-scripts.md}`、
  `.trellis/spec/preset/{installer.md,overlay-guidelines.md,upstream-ownership.md}`、
  `.trellis/spec/docs/public-docs.md`。
- Canonical package：
  `trellis/skills/guru-team/packages/guru-review-task-publication/**`。
- Runtime 与 wrapper：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`、
  `trellis/workflows/guru-team/scripts/bash/{record-task-publication-review.sh,check-task-publication-review.sh}`。
- Eval 与 tests：
  `trellis/skills/guru-team/adapters/eval/native_adapter.py`、
  `trellis/skills/guru-team/tests/test_skill_packages.py`、
  `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`、
  publication/Branch Review package tests、
  preset installer 与 upstream ownership tests。
- Registry、manifest、workflow 与 consumer contracts：
  `trellis/skills/guru-team/registry.json`、
  `trellis/guru-team-extension.json`、
  `trellis/workflows/guru-team/workflow.md`、
  publication workflow/stop consumer schemas。
- Installed/platform copies：
  `.trellis/guru-team/**` 以及
  `.agents/.codex/.claude/.cursor` 下的 publication package copies。
- Durable Docs SSOT 的 16 个 approved paths：
  `.trellis/spec/workflow/**` 六个文件、`.trellis/spec/preset/**` 三个文件、
  `.trellis/spec/docs/public-docs.md`、三份 `docs/requirements/**`、根 `README.md`、
  workflow README 与 preset README。
- 冻结面：
  `production-minimal-handoff.json`、#131 Branch Review public output
  schemas/examples、五个 `trellis-continue` overlay payload、完整 overlay tree 与
  upstream finish-work assets。

### 已修复问题

- 文件：
  `trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`
- 问题：throwaway verifier 的静态测试仍断言旧 planned identity
  `guru-review-task-publication`，与本 task 激活该 Skill、将 planned identity 迁移为
  `guru-finalize-task` 的 registry/manifest/verifier current contract 不一致。
- 修复：将单行 expectation 更新为 `guru-finalize-task`；重跑 preset installer
  45 tests 通过。

- 文件：
  `trellis/presets/guru-team/scripts/python/test_upstream_ownership.py`
- 问题：ownership baseline facts test 仍断言 10 active Skills，并保留由该旧 count
  导出的旧 `facts_sha256`；current deterministic validator 已稳定返回 11 active、
  1 planned。
- 修复：将 active count 更新为 11，并将 facts digest 更新为 current validator
  重建的
  `40ca853b4aa16239cc319267c8e1f733a4ccce36fa4369fe33a58f6aef3d2920`；
  重跑 ownership 9 tests 通过。

### 未修复问题

#### F-001（阻断，implementation_required）：stale invocation 与十二项 entry preconditions 未绑定到 current owner round

- 正常路径资格：`normal_required_behavior` / `explicit_requirement`。复现不需要手工
  篡改 hash、伪造 artifact 或任何恶意输入；只需 AI/recorder 在 supported stale
  profile 中遗漏 contract-required 字段。
- Contract 证据：
  - `interface.json` 为 workflow/standalone 均声明相同十二项 preconditions，并把
    re-entry identity 定义为 prior publication identity + current facts。
  - `public-publication-review-stale-input.schema.json` 要求
    `stale_reason` 与 `reentry_context`。
  - PRD R8 与 design 10.2(6) 要求 stale/non-ready replacement 绑定旧
    `publication_ref`。
- 实现证据：
  - `task_publication_semantic_errors()` 不读取或要求 `stale_reason`、
    `reentry_context`、`supersedes_publication_ref`。
  - `cmd_record_task_publication_review()` 只把
    `authored.get("supersedes_publication_ref")` 作为 nullable 值复制；无 stale
    conditional requirement。
  - `task_publication_check_errors()` 重建 authored payload 时完全不带
    `supersedes_publication_ref`，因此 checker 也不能恢复该约束。
  - public wrapper 对 stale profile 明确跳过 reviewed HEAD/review ref match，并且
    不把 `stale_reason`/`reentry_context` 与 owner result 比较。
  - recorder/checker 没有调用 planning approval checker、Phase 2 checker、
    Branch Review entry-precondition checker 或等价 publication-specific
    十二项 entry-precondition validator；它们只校验 passed review gate、文件字节
    bindings 与 repository snapshot。文件存在及其 hash current 不能证明这些 gate
    当前仍通过。
  - native eval staging 虽手工添加一个 `supersedes_publication_ref`，但 authored
    recorder payload仍不消费 stale public input 的 `stale_reason`/
    `reentry_context`，所以 7-case eval 没有覆盖 invocation binding。
- 独立 probe：
  - `publication_review_stale`、`stale_reentry_review`、十个 passed dimensions、
    `typed_exit=ready`，但不含上述三个 stale/replacement 字段时，
    `task_publication_semantic_errors(...)` 返回 `[]`。
- 影响：一个不属于 exact stale invocation、没有绑定 prior publication identity，
  或未重验 current planning/Phase 2/Docs/ledger 前置条件的 owner result仍可被记录并
  checker-pass 为 current `ready`。这违反 R1/R3/R8、AC2/AC8 与 package
  `invocation_freshness` 合同。
- 未自修原因：修复需要设计并实现 publication-specific entry validator、stale input
  到 private gate 的 invocation binding、replacement lifecycle、public owner-result
  matching 与 source/installed negative tests；不是小型机械修复。

#### F-002（阻断，implementation_required）：唯一 readiness gate schema/semantic validator 没有落实三层 closed evidence 与 finding closure

- 正常路径资格：`normal_required_behavior` / `explicit_requirement`。复现只使用
  schema-valid、recorder-authored normal payload。
- Contract 证据：
  - PRD R6、design §10、`.trellis/spec/workflow/data-contracts.md` 的
    `Publication Readiness Gate` 要求保存 AI-reviewed dimensions/findings、
    scope/Docs/safety/deployment conclusions、revision history、
    reviewer-process/confirmation evidence、typed conclusion、closed
    deterministic bindings 与 optional finalization layer。
  - ready 要求所有 finding 有真实 closure evidence。
- 实现证据：
  - `pr-readiness.schema.json` 将 `semantic_review`、
    `deterministic_bindings`、`consumer`、`publish_inputs` 仅定义为开放
    `{"type":"object"}`；没有 nested required、closed field set 或 typed-exit
    conditional。
  - package `examples/pr-readiness.json` 可通过该 JSON Schema，但同一 runtime 的
    semantic validator会返回
    `publication AI Review Gate is incomplete` 与
    `publication dimensions must contain the exact ordered ten ids`。因此
    interface 指向的 private gate example 不是可被 runtime 接受的 gate。
  - semantic validator只检查 finding 的 exact key set与少量 enum，不要求非空
    `summary`、`scope_basis`、`evidence_refs`、`affected_artifacts` 或
    `closure_evidence`。
- 独立 probe：
  - 一个 `ready` payload含十个 passed dimensions，并含一个
    `status=closed` 但 summary/scope/evidence/affected/closure 全为空的 finding，
    `task_publication_semantic_errors(...)` 仍返回 `[]`。
- 影响：checker-passed `ready` 可以没有 required review process/history/
  conclusions，也可以把没有 closure evidence 的 finding视为 closed。当前 durable
  Docs SSOT声称 active schema已强制三层 closed contract，实际 schema/runtime并未做到，
  形成 current-scope Docs SSOT 不一致。
- 未自修原因：需要重做 private artifact schema、recorder authored-input contract、
  semantic/checker validation、example、runtime/preset copies及负向 tests/evals，超出
  Phase 2 reviewer 的机械修复边界。

### 验证结果

- Lint：通过。`git diff --check` 通过；source/installed contract validator均通过。
  仓库无独立 ruff/flake8/shellcheck lint 配置。
- TypeCheck：不适用。仓库未提供 mypy/pyright/其它 type-check 配置或命令；未把
  Python import/单测成功冒充静态 type-check。
- Tests：任务级失败。常规 suites 均为绿色，但独立 normal-path negative probes
  复现 F-001/F-002，说明 current acceptance 未满足且现有 tests漏测：
  - skill package suite：171 tests，全部通过；
  - runtime suite：569 tests通过，13 skipped；
  - publication + Branch Review package contract suites：13 tests通过；
  - preset installer suite：45 tests通过；
  - upstream ownership suite：9 tests通过。
- Shared eval：source 7/7、installed 7/7通过；actual exits覆盖
  `ready`、`return_to_task_work`、`blocked`。这些 cases没有验证缺失 stale
  identity、缺失十二项 precondition recheck或空 closure evidence必须失败。
- Source/installed package validator：均通过，facts 为 11 active Skills、
  42 exits、25 targets、planned `guru-finalize-task`。
- Distribution parity：canonical、installed、Agents、Codex、Claude、Cursor
  publication package bytes一致（忽略未跟踪 Python cache），runtime 与 native
  adapter canonical/installed bytes一致，所有 package shell scripts executable。
- Overlay/ownership：dogfood overlay drift通过；frozen inventory 43 paths、
  reviewed current payload 5、active Skills 11、planned Skills 1；无
  `.new/.bak/.orig` sidecar。
- Frozen invariants：production manifest、#131 output schema/example、
  五个 continue overlay、完整 overlay tree 与 upstream finish-work assets均无 diff。
- Safety/deployment：完整 changed/untracked path scan未发现 GitHub Actions、
  Docker/Compose、Kubernetes/Helm、DB migration、Makefile、`.env` 或 production
  deployment surface；本轮未执行 publish、push、PR、archive、finalization 或远端写入。
- 开箱即用：复用了 current implementation handoff中已记录的
  `verify-throwaway-install.sh` public-marketplace sample结果；本 reviewer fresh
  重跑了 preset 45 tests、source/installed validators/evals、drift/parity/frozen
  checks。由于分支未 push，exact remote branch marketplace verifier仍不可执行；
  本轮没有把 public sample声明为 exact-branch verification。

### 证据交接

- 阶段二：覆盖 requirements/design/spec、完整 uncommitted implementation diff、
  canonical/install/platform copies、API/schema/runtime/workflow/eval/test、Docs SSOT、
  overlay/frozen/safety/deployment。两项 current-scope correctness finding阻断通过。
  本报告可支撑 `phase2-check.json` 的 `implementation_required` exit，不能支撑
  `passed`。本 reviewer未调用 Phase 2 recorder/checker。
- Docs SSOT：approved strategy 为 `ssot_first`，16 个 durable paths均有 task delta，
  implementation handoff也声明完成合并；但 F-002 证明 durable
  `data-contracts.md`/skill contract所声明的 active三层 closed gate与实际
  schema/runtime不一致。因此 current Docs SSOT reconciliation 结论为失败，修复后
  必须重新同步 durable docs或实现，并重新完整 Phase 2 check。
- Branch Review：不适用。本轮是 uncommitted Phase 2 check，不是 committed full
  branch review；未写 `review.md`、未调用 Branch Review recorder/validator。
- 开放风险：现有 green eval/contract suites主要证明 package closure/projection与
  happy routes，不证明 semantic evidence completeness。修复必须增加至少：
  missing stale reason/context、missing prior publication ref、stale planning/
  Phase2/Docs/ledger、schema-valid runtime-invalid example、empty finding closure、
  stale owner-result/public-input mismatch 的 source + installed negative cases。

### 结论

当前结论为 `implementation_required`。自动化回归、安装分发与冻结面大部分稳定，
但 publication owner的核心 freshness/replacement/evidence contract尚未实现完整；
在修复 F-001/F-002并重跑受影响 schema/runtime/eval/preset与完整 Phase 2 check前，
不得记录 passing `phase2-check.json`，不得进入 task commit 或 Branch Review。
