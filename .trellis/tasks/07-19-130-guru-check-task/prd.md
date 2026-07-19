# #130 实现 `guru-check-task` 闭环 Skill

## 1. 目标

实现 Guru Team Phase 2 complete check semantic closed-loop Skill：

```text
guru-check-task
```

该 Skill 必须成为 task-scope implementation check、Docs SSOT reconciliation verification、finding loop、scope/adequacy judgment 和现有 `phase2-check.json` 的唯一 step-local semantic owner。Global workflow 只保留 mandatory invocation、四个 typed exit 的唯一 consumer 与 fail-closed stop。

## 2. Requirement Authority

1. Live source issue：https://github.com/castbox/guru-trellis/issues/130
2. Parent issue：https://github.com/castbox/guru-trellis/issues/127
3. 已完成依赖：#128、#129。
4. 当前 task Intake evidence：
   - `task-start-context.json`
   - `context-discovery.json`
   - `issue-review.json`
   - `issue-scope-ledger.json`
5. Durable contracts：
   - `docs/requirements/requirement-main.md`
   - `docs/requirements/guru-team-trellis-flow.md`
   - `.trellis/spec/workflow/skill-package-contract.md`
   - `.trellis/spec/workflow/workflow-contract.md`
   - `.trellis/spec/workflow/data-contracts.md`
   - `.trellis/spec/workflow/companion-scripts.md`
   - `.trellis/spec/workflow/quality-guidelines.md`
   - `.trellis/spec/preset/upstream-ownership.md`
6. 官方 Trellis extension contracts：
   - `https://docs.trytrellis.app/advanced/custom-workflow.md`
   - `https://docs.trytrellis.app/advanced/custom-skills.md`
   - `https://docs.trytrellis.app/reference/architecture.md`

Issue #130 已固定 Skill id、entry evidence、closed loop、scope-before-severity 顺序、四个 external exit、artifact 复用、script boundary、upstream ownership、分发范围和验收标准。当前仓库证据定位了现有 Phase 2 runtime、tests、workflow 展开行为、package registry、preset installer 与 dogfood 分发路径。无开放产品问题阻塞设计。

## 3. 当前状态与缺口

- `trellis/skills/guru-team/registry.json` 尚无 active `guru-check-task`。
- `trellis/workflows/guru-team/workflow.md` 与 `.trellis/workflow.md` 仍展开 Phase 2 check 的内部步骤，并直接要求 `trellis-check` 后调用旧 recorder/checker。
- `phase2-check.json` schema 1.0 记录 checker、coverage、validation、findings、HEAD 与 dirty paths，但没有 stable Skill identity、planning linkage、scope qualification、adequacy gate、four-exit union 或未验证项合同。
- Shared runtime 已实现 artifact path、checked artifact/spec digest、dirty snapshot、agent recovery chain、post-commit coverage 与 stale checks；这些 deterministic foundations 必须复用。
- 官方 `trellis-check` Skill/Agent 是 upstream-owned review worker，不得成为 Guru pass owner，也不得被修改或 overlay。
- #129 已建立 active Skill package、schema 1.2 interface、registry-driven distribution、workflow thin route 与 v2 planning approval，可作为 package/runtime/preset 模式依据。

## 4. Scope

### 4.1 In Scope

1. 新增并注册 canonical active `guru-check-task` package，声明 `judgment_mode=semantic`。
2. Workflow mode 与 standalone mode 使用相同 entry preconditions、AI Gate、recorder/checker 和 typed exits。
3. Entry 必须绑定 active task/workspace、current `guru-planning-approval-2.0` approved evidence、三份 planning artifacts、Docs SSOT Plan、requirement provenance、issue ledger、base/HEAD、完整 dirty snapshot、implementation/check assignment 与 recovery chain、受影响 durable docs/spec。
4. Skill 必须读取完整 task scope、implementation handoff、code/tests/docs/spec、current dirty diff 和 repository-defined validation commands。
5. AI 必须按固定顺序完成 scope qualification，再对 current-scope findings 分配 P0/P1/P2/P3 severity。
6. 未被 requirement/planning 触发的非常规安全、威胁、并发、fault-injection、locking、TOCTOU、cross-OS 场景必须记录为 scope proposal 或 out-of-scope evidence，不得成为 current-scope P0-P3 finding。
7. Current approved scope 内 finding 必须返回 `implementation_required`；修复后重新执行完整 check，不得只复查最后一处修改。
8. 需要改变 requirement/scope 的 finding 必须返回 `planning_stale`，由 `guru-approve-task-plan` 或 `guru-clarify-requirements` 处理。
9. 复用并演进现有 `{TASK_DIR}/phase2-check.json`；不得新增第二个 Phase 2 pass artifact。
10. Recorder/checker 必须验证 schema、hash、HEAD、diff、dirty snapshot、planning linkage、agent recovery、artifact freshness 与 exit/consumer invariant。
11. Workflow 必须收敛为 mandatory invocation、four-exit mapping、target/stop marker 和 fail-closed routing。
12. Additive 分发 canonical package 到 shared、Codex、Claude、Cursor discovery roots，并同步 dogfood installed copies。
13. 更新 runtime、schema、registry、extension manifest、durable docs/spec、README、package/runtime/preset tests、throwaway/update/reapply 验收。

### 4.2 Out Of Scope

- 不承担 #131 post-commit Branch Review。
- 不执行 #132 的最终 legacy overlay 删除或全流程收口。
- 不实现 #108 的具体 code/docs subtraction capability，只保留后续扩展所需 review dimension 合同。
- 不执行 #81 release/tag gate。
- 不修改或新增 overlay `trellis-check` Skill、`trellis-check` Agent、`.trellis/agents/check.md`、平台 `trellis-check` entry 或其它 upstream-owned check asset。
- 不把所有语言和仓库验证逻辑写成通用静态分析框架。
- 不让 script 判断 adequacy、scope、finding severity、Docs SSOT consistency、route intent 或 semantic pass。
- 不处理恶意伪造、对抗性输入、故意绕过、额外 race/TOCTOU/lock/fault-injection/crash-consistency/cross-OS 加固。

## 5. 功能需求

### R1. Canonical Package 与 Public API

- Stable id 必须是 `guru-check-task`，registry state 必须是 `active`。
- Package 必须包含 `SKILL.md`、`interface.json`、`references/contract.md`、closed schema、去敏 example、dispatcher-only wrappers 与 package tests。
- Interface 必须使用 schema 1.2，声明 semantic 五阶段 profile：`forward_behavior -> ai_review_gate -> conditional_human_confirmation -> recorder_validator -> typed_exit`。
- Package public 内容不得包含 active task、本机绝对路径、workspace journal、secret 或业务私有记录。

### R2. Mode Parity 与 Entry Evidence

- Workflow 与 standalone 的 entry precondition id 有序集合必须完全相同。
- Standalone 必须发现 direct active task 和 expected workspace，再执行与 workflow mode 相同的 evidence/freshness checks。
- Missing、legacy、non-approved 或 stale planning approval 必须阻塞 Phase 2。
- Planning document、Docs SSOT locator、authority、ledger、task identity、base lineage、agent recovery 或 checked-path identity 漂移必须 fail closed。
- Task activation 后的预期 implementation HEAD/dirty drift不能单独使 planning approval stale。

### R3. Repository Check Execution 与 Evidence

- Skill 必须基于仓库类型和 repository-defined commands 选择适用的 lint、type-check、unit/integration test、schema、generated/drift、install/update 验证。
- 未执行项必须记录具体原因与影响，不得用泛化“未验证”占位。
- 官方未修改的 `trellis-check` worker输出只能作为 AI evidence；最终 adequacy、scope、finding 与 pass 由 `guru-check-task` Gate 独占。
- Implementation handoff、review worker report、commands/results、checked paths 和 unresolved verification必须进入同一 semantic review round。

### R4. Scope Qualification 先于 Severity

- 每个候选问题必须先记录 requirement/planning trigger、supported normal-path reproduction、scope disposition 与 route basis。
- 只有 disposition=`current_scope` 的候选才能获得 P0/P1/P2/P3 severity。
- `scope_change_required` 必须进入 `planning_stale` route，不得由 check step直接扩张 planning 或修改 authority。
- `out_of_scope` 和 `followup_proposal` 不得阻塞当前 pass，也不得被自动实现。
- 仅靠手工伪造 artifact/hash/state 才能复现的候选必须是 `out_of_scope`。

### R5. Complete Adequacy 与 Docs SSOT Review

- AI Gate 必须覆盖 requirements -> design -> implementation -> tests -> Docs SSOT 的完整承接。
- Gate 必须审查 task scope、cross-layer contract、compatibility、deployment/config/schema/CI/CD/container/K8s/DB/Makefile 影响和 commit-message compatibility。
- Docs SSOT review 必须验证 planning strategy 已执行、durable docs 与 task delta 已合并或有批准的不更新/修复边界。
- Coverage flags、命令 exit 0 或 recorder success 均不能生成 semantic pass。

### R6. Finding Loop 与 Full Rerun

- Current-scope finding 存在时 exit 必须是 `implementation_required`，consumer 必须是 implementation route。
- Finding 修复后必须创建新的 complete check round，重读完整 scope、完整 diff、全部适用 commands 和 Docs SSOT 状态。
- Agent failed/unfinished/stale/replacement partial chain 必须闭环到后续 completed evidence后才能 pass。
- `passed` 必须要求零 blocking current-scope finding、零 unresolved verification blocker 和完整 current evidence。

### R7. Four Typed Exits

- `passed` -> `guru-create-task-commit`。
- `implementation_required` -> workflow implementation route。
- `planning_stale` -> `guru-approve-task-plan` 或 `guru-clarify-requirements` 的单一、显式 route discriminator。
- `blocked` -> fail-closed stop。
- Unknown、multiple、unmapped exit、ambiguous planning consumer 或 consumer mismatch 必须 fail closed。

### R8. Existing Artifact Evolution

- Artifact basename 必须保持 `phase2-check.json`。
- 新 schema 必须包含 stable Skill identity、entry projections、review rounds、scope qualification、findings、adequacy review、unverified items、AI Gate、typed exit、consumer、HEAD/diff/dirty snapshot 与 facts digest。
- `phase2-check.json` 只能由 `guru-check-task` 语义闭环写入；旧 top-level wrappers必须成为该 package runtime 的 compatibility入口或迁移后拒绝 legacy调用。
- Post-commit consumer必须继续验证 recorded dirty paths覆盖后续 committed non-metadata paths；不得为匹配新 HEAD 重录 pass。
- Legacy active artifact必须要求 complete semantic re-entry；archived artifact字节不得改写。

### R9. Script Boundary

- Executor只运行明确命令并收集 exit code/stdout-stderr digest/size。
- Recorder只写入 AI 已审查的 scope、finding、adequacy、route 和 pass/fail结论。
- Validator只校验 closed schema、path/hash/HEAD/diff/dirty/freshness、planning linkage、agent recovery 和 exit/consumer invariants。
- Script不得推断 scope disposition、severity、test sufficiency、Docs SSOT consistency 或 semantic pass。

### R10. Workflow、Distribution 与 Upgrade

- Canonical/dogfood workflow Phase 2区只能保留 mandatory Skill invocation、四出口 mapping、target/stop markers和global phase transitions。
- Preset必须从 canonical `trellis/skills/guru-team/`安装 registry/package和四平台 Guru discovery copies。
- 本任务不得新增或修改 upstream-owned overlay；ownership inventory必须保持43条 frozen entry不变。
- Clean throwaway必须覆盖 marketplace init/preview/switch、preset initial apply、installed invocation、`trellis update --force`、workflow/preset reapply、dogfood equality与zero unresolved sidecar。

## 6. Docs SSOT 状态

- Docs state：`complete_docs`
- Evidence paths：`docs/requirements/**`、`.trellis/spec/workflow/**`、`.trellis/spec/preset/**`、`trellis/workflows/guru-team/{workflow.md,README.md}`、`trellis/presets/guru-team/README.md`
- Requirement impact：本任务改变长期 Phase 2 workflow、Skill public API、artifact schema、script boundary和distribution合同。
- Strategy：`ssot_first`
- 权威 Docs SSOT Plan：`design.md` 的“Docs SSOT Plan”章节。
- Task history only：intake evidence、官方文档研究摘要、implementation handoff、check/review round和bootstrap迁移记录。

## 7. 验收标准

- [ ] AC1：source registry/package validator将`guru-check-task`识别为active semantic Skill，package/interface/schema/example/wrappers/tests完整通过。
- [ ] AC2：workflow/standalone entry集合相同；missing/legacy/non-approved/stale planning、authority、workspace、ledger、agent或repository evidence均fail closed。
- [ ] AC3：官方未修改的`trellis-check` worker只能提供evidence，无法单独生成Guru pass。
- [ ] AC4：fixture证明scope qualification固定先于severity；非`current_scope`候选无法携带P0-P3。
- [ ] AC5：未被approved requirement/planning触发的非常规场景只能成为scope proposal或out-of-scope，不得阻塞或自动实现。
- [ ] AC6：current-scope finding返回`implementation_required`；修复后必须full-scope rerun，partial rerun不能pass。
- [ ] AC7：scope-changing finding返回`planning_stale`并映射一个显式planning/clarification consumer；ambiguous consumer fail closed。
- [ ] AC8：`passed`、`implementation_required`、`planning_stale`、`blocked`与Gate/consumer双向invariant完整；unknown/multiple/unmapped fail closed。
- [ ] AC9：`phase2-check.json`只有`guru-check-task`一个semantic owner，绑定reviewed paths、commands/results、AI adequacy、findings、unverified items、dirty snapshot、HEAD和planning evidence。
- [ ] AC10：agent recovery fixtures覆盖failed、unfinished、stale、replacement和最终completed闭环；partial output不能产生pass。
- [ ] AC11：workflow Phase 2区不再展开check内部算法，也不依赖Guru patch的upstream `trellis-check` entry。
- [ ] AC12：shared/Codex/Claude/Cursor package copy与canonical一致，dogfood apply后无drift和unresolved `.new`/`.bak`。
- [ ] AC13：ownership validator证明本次diff未新增或修改upstream-owned overlay，43条inventory字节与分类保持不变。
- [ ] AC14：targeted package/runtime/preset tests、Python compile、Bash syntax、JSON schema、task validate、`git diff --check`通过。
- [ ] AC15：clean throwaway完成marketplace/preset/install invocation/update/reapply/sidecar全链路，README命令可执行。
- [ ] AC16：durable requirements/spec、canonical workflow、package contract、runtime、tests、manifest与installed copies对同一owner、scope、exit、artifact和freshness语义一致。

实施若发现必须改变四出口、artifact basename、scope-before-severity顺序、upstream ownership或normal-operation boundary，必须返回 Phase 1 更新三份 planning artifacts并取得新的 post-planning confirmation。
