# #129 实现 `guru-approve-task-plan` 闭环 Skill

## 1. 目标

实现可在 workflow mode 与 standalone mode 调用的 semantic closed-loop Skill：

```text
guru-approve-task-plan
```

该 Skill 成为 Phase 1 planning adequacy、requirement provenance、实现选择识别、非常规场景专用确认和现有 `planning-approval.json` 的唯一 step-local semantic owner。Global workflow 只保留 mandatory invocation、四个 typed exit 的唯一 consumer 与 fail-closed stop。

## 2. Requirement authority 与清晰度

### 2.1 权威来源

1. Live source issue：https://github.com/castbox/guru-trellis/issues/129
2. Parent issue：https://github.com/castbox/guru-trellis/issues/127
3. 已完成依赖：#128、#114、#112。
4. 当前 task Intake evidence：
   - `context-discovery.json`
   - `issue-review.json`
   - `issue-scope-ledger.json`
   - `task-start-context.json`
5. Durable contracts：
   - `docs/requirements/guru-team-trellis-flow.md`
   - `docs/requirements/requirement-main.md`
   - `.trellis/spec/workflow/skill-package-contract.md`
   - `.trellis/spec/workflow/workflow-contract.md`
   - `.trellis/spec/workflow/data-contracts.md`
   - `.trellis/spec/workflow/companion-scripts.md`
   - `.trellis/spec/workflow/quality-guidelines.md`
   - `.trellis/spec/preset/upstream-ownership.md`

### 2.2 清晰度结论

Issue #129 已固定 Skill id、两种 mode、输入证据、四类 provenance、非常规场景确认规则、九步 closed loop、四个 external exit、script boundary、分发范围和验收结果。当前仓库证据也定位了 package registry、Phase 1 workflow、既有 planning recorder/checker、preset installer、dogfood 副本与测试入口。无产品语义问题阻塞设计。

## 3. 当前状态与缺口

- `trellis/skills/guru-team/registry.json` 尚无 `guru-approve-task-plan` active entry。
- `trellis/workflows/guru-team/workflow.md` 与 dogfood `.trellis/workflow.md` 仍展开规划充分性审查、三文档展示、用户确认、recorder/checker 和 task activation 内部步骤。
- `planning-approval.json` 现由 shared runtime 的 recorder/checker 生成并消费 `guru-review-contract-wording:planning_artifacts:pass`，但没有独立 planning approval Skill package。
- 现有 artifact 已绑定三份规划文档、wording evidence、明确的 post-planning confirmation、HEAD 和 dirty snapshot；该 artifact 必须演进，不能新增第二个 planning pass artifact。
- 现有 durable docs/spec 完整描述当前 Phase 1 门禁，但尚未承接 #129 的新 semantic owner、provenance 与非常规场景确认合同。
- #128 已建立 no-new-upstream-patch 门禁，本任务不得新增或修改 upstream-owned overlay。

## 4. Scope

### 4.1 In Scope

1. 新增并注册 canonical `guru-approve-task-plan` package，声明 `judgment_mode=semantic`。
2. Workflow mode 与 standalone mode 使用相同 entry preconditions、AI Gate、专用确认条件、recorder/validator 和 typed exits。
3. 固定读取 current task、base/HEAD、source issue 与 reviewed change request evidence、`prd.md`、`design.md`、`implement.md`、Docs SSOT Plan、issue scope ledger、artifact digests 和 current `guru-review-contract-wording:planning_artifacts:pass` evidence。
4. 对每个 load-bearing requirement、design contract、acceptance item 与 test obligation记录四类 provenance 之一：
   - `explicit_requirement`
   - `necessary_implementation_choice`
   - `approved_scope_expansion`
   - `out_of_scope_proposal`
5. 对 `necessary_implementation_choice` 记录候选方案、选中方案、选择理由和“不扩张产品或风险边界”的审查结论。
6. 对 source requirement 未触发的安全、威胁、攻击、恶意 actor、TOCTOU、并发 race、fault injection、跨 OS 原子性场景执行专用 proposal review；确认前不得进入 approved execution contract。
7. 风险只由非必要实现机制引入时，planning revision 必须先删除或替换该机制，不能通过 scope expansion 为该机制追加加固需求。
8. 复用并演进现有 `planning-approval.json`，加入完整 Skill identity、provenance、unusual-scenario review、AI Gate、confirmation、typed exit、consumer 与 freshness evidence；不得创建平行 artifact。
9. 复用 `guru-review-contract-wording:planning_artifacts` 作为唯一 wording owner；本 Skill 不复制 vocabulary、classification 或 scanner 规则。
10. 实现 `approved`、`revision_required`、`clarify_scope`、`blocked` 四个稳定 exit 及唯一 consumer。
11. 将 Phase 1 approval 行为从 workflow 正文收敛到 Skill package；workflow 只保留 mandatory invocation、typed-exit mapping、target/stop marker 和缺失/未知/多值/未映射 exit 的 fail-closed 规则。
12. 在 shared、Codex、Claude、Cursor 声明目标中 additive 分发 `guru-*` package discovery copy，并同步 dogfood 安装副本。
13. 更新 shared runtime、package registry、extension manifest、durable docs/spec、preset README/workflow README、tests、throwaway/update/reapply 检查。
14. 为当前 bootstrap task 保留迁移路径：实现前按旧门禁记录 schema 1.2 approval；新 package active 后，若三份 planning 文档 digest 未变化，则用同一 post-planning confirmation evidence 重新执行新 Skill recorder/checker，写入新 schema，再进入 Phase 2 final check。

### 4.2 Out of Scope

- 不实现 #130 `guru-check-task`。
- 不实现 #131 `guru-review-branch`。
- 不执行 #132 的 legacy upstream overlay 删除与最终三 Skill 集成收口。
- 不修改 Trellis upstream `trellis-brainstorm`、`trellis-before-dev`、`trellis-check`、Agent、Command、Prompt、Hook 或 runtime agent。
- 不拥有 initial change request review；该步骤仍由 `guru-review-change-request` 独占。
- 不复制 `guru-clarify-requirements` 的 issue/body/scope ledger mutation loop。
- 不复制 `guru-review-contract-wording` 的 wording vocabulary、classification、rewrite 或 scanner contract。
- 不创建 worktree、branch、task、commit、push 或 PR。
- 不处理恶意伪造、对抗性输入、故意绕过、额外 race/TOCTOU/lock/fault-injection/crash-consistency/cross-OS 加固。
- 不新增或修改 `trellis/presets/guru-team/overlays/**` 中的 upstream-owned asset。

## 5. 功能需求

### R1. Canonical package 与 public API

- Stable id 必须是 `guru-approve-task-plan`，registry state 必须是 `active`。
- Package 必须含 `SKILL.md`、`interface.json`、`references/contract.md`、closed schema、example、dispatcher-only wrappers 和 package tests。
- `interface.json` 必须使用 `guru-team-skill-interface-1.2`，并声明 semantic 五阶段 profile：`forward_behavior -> ai_review_gate -> conditional_human_confirmation -> recorder_validator -> typed_exit`。
- Package public 内容不得含 active task、workspace journal、平台 prompt、业务私有状态、secret 或本机绝对路径。

### R2. Mode parity 与 entry evidence

- Workflow 与 standalone 的 entry precondition id 集合必须完全相同。
- Standalone 先确定 current task 和 workspace boundary，再复验与 workflow 相同的 source authority、planning artifacts、Docs SSOT Plan、wording evidence、base/HEAD 和 digest。
- Missing、stale、mismatched 或 ambiguous evidence 必须 fail closed；frontmatter auto-match 不能替代 mandatory invocation。

### R3. Planning adequacy 与 ambiguity

- AI 必须审查 requirement 完整性、source semantics 保留、条件路径触发条件、单一实现 owner、机器门禁、验收可观察性、test obligation、Docs SSOT、兼容与回滚边界。
- Skill 必须复用 current `planning_artifacts:pass` evidence，不得由 runtime 生成 wording judgment 或七项 planning semantic result。
- AI 发现 task 内部缺口时返回 `revision_required`，修订三份 planning 文档并重新执行完整 review；旧 digest 不得继续进入 task activation。

### R4. Requirement provenance

- 每个 load-bearing planning contract 必须有稳定 id、artifact locator、current statement digest、provenance class、authority refs 和非空理由。
- `explicit_requirement` 必须指向 user、live issue、approved clarification 或 durable requirement SSOT 中的明确 authority。
- `necessary_implementation_choice` 必须记录候选方案、选中方案、选择理由和无产品/风险 scope expansion 结论。
- `approved_scope_expansion` 必须绑定 exact proposal digest、专用 confirmation 和更新后的 current authority evidence。
- `out_of_scope_proposal` 不得进入 approved execution contract；需要 authority change 时返回 `clarify_scope`。
- AI 决定 coverage 与分类语义；runtime 只验证记录 shape、locator、digest、枚举、引用完整性和 exit invariant。

### R5. 非常规场景专用确认

- 原 requirement 明确写入的非常规场景归入 `explicit_requirement`，不再发起 scope expansion confirmation。
- 原 requirement 未写入的非常规场景不得归入 `necessary_implementation_choice`。
- AI 认定某个新非常规场景不可缺失时，proposal 必须包含 scenario、触发证据、范围、成本、替代机制和不实施后果，并取得只绑定该 exact proposal 的专用确认。
- 普通 task 创建授权、planning review、`继续`、`确认` 或整个 task 的授权不得作为该专用确认。
- Proposal 需要修改 issue/body/scope ledger 时返回 `clarify_scope`，由 `guru-clarify-requirements` 完成 authority mutation 后再进入本 Skill。
- 非必要机制引发的风险必须以 `mechanism_removed` 或 `mechanism_replaced` 结束；该路径不创建 scope expansion confirmation。

### R6. Closed loop 与 typed exits

Skill 必须执行：读取 current authority/planning -> AI adequacy/ambiguity/provenance/scope review -> planning revision -> 命中条件时的专用确认 -> scope clarification route/re-entry -> current wording evidence复验 -> final AI Gate -> recorder/checker -> one typed exit。

- `approved`：唯一 consumer 是 task activation / Phase 2 入口。
- `revision_required`：唯一 consumer 是同一 Skill 的 planning revision re-entry。
- `clarify_scope`：唯一 consumer 是 `guru-clarify-requirements`。
- `blocked`：唯一 consumer 是 fail-closed stop。
- Unknown、multiple、unmapped exit 或 consumer 不唯一必须阻塞。

### R7. Existing artifact evolution

- Artifact path 保持 `{TASK_DIR}/planning-approval.json`。
- 新 schema 必须表达四个 exit，而不只表达 pass。
- `approved` 必须绑定三份 planning 文档、Docs SSOT Plan locator、source authority、wording evidence、provenance coverage、unusual-scenario review、post-planning confirmation、base/HEAD 与 dirty snapshot。
- 非 `approved` artifact 必须记录阻塞或 re-entry 理由，并且不能通过 task activation checker。
- 旧 schema 1.2 active artifact 在新 owner 生效后必须重新执行完整 Skill review；archive 不改写。
- HEAD 在本次 approval invocation 与 activation 前必须 current；task activation 后的预期 implementation/commit HEAD 变化不能单独抹除已绑定的 planning content approval。

### R8. Script boundary

- Script 只负责 schema、path、hash、size、HEAD/base snapshot、required field、enum、引用、artifact freshness、exit/consumer invariant 和 deterministic projection。
- Script 不得决定 adequacy、provenance class、choice 必要性、scope、非常规场景是否绝对必要、confirmation 是否足够、revision action 或 semantic pass。
- Recorder/checker 只能在 AI review 和命中条件的人类确认已经发生后记录或校验事实。

### R9. Workflow 与分发

- Canonical workflow 与 dogfood workflow 必须按 stable id mandatory invoke 本 Skill，并只消费声明出口。
- Platform entry 只负责 discovery/routing，不复制 Skill 内部步骤。
- Preset 从 canonical `trellis/skills/guru-team/` additive 安装 registry、package 与声明平台 discovery copy。
- 本任务改动后 ownership validator 必须证明 no-new-upstream-patch，overlay inventory 不得扩张。

### R10. Tests 与 install/update

- Package tests、shared runtime tests、registry/interface tests、preset tests 必须覆盖 mode parity、provenance matrix、unusual proposal matrix、四出口、stale evidence、legacy migration 和 script boundary。
- Fixture 必须证明“非必要机制引入风险”先删除或替换机制，不自动扩张 scope。
- Clean throwaway 必须覆盖 marketplace workflow install/preview/switch、preset initial apply/reapply、四平台 discovery、installed Skill invocation、`trellis update` 后 reapply、zero unresolved sidecar。
- Dogfood source/installed package equality、overlay drift 和 ownership checks 必须通过。

## 6. Docs SSOT 状态

- Docs state：`complete_docs`
- Evidence paths：`docs/requirements/**`、`.trellis/spec/workflow/**`、`.trellis/spec/preset/**`、`trellis/workflows/guru-team/{workflow.md,README.md}`、`trellis/presets/guru-team/README.md`
- Requirement impact：现有 durable docs 完整描述当前 Phase 1 approval 与 schema 1.2 行为；本任务改变长期 workflow/Skill/artifact public contract，必须把 task delta 合并回 durable SSOT。
- Strategy：`ssot_first`
- 权威 Docs SSOT Plan：`design.md` 的“Docs SSOT Plan”章节。
- Task history only：issue evidence、研究摘要、实施 handoff、check/review 证据与 bootstrap migration 过程记录。

## 7. 验收标准

- [ ] AC1：source registry 与 package validator 报告 `guru-approve-task-plan` 为 active semantic Skill，interface/schema/example/wrappers/tests 全部通过。
- [ ] AC2：workflow 与 standalone entry preconditions 完全相同，缺失或 stale requirements/wording/HEAD/artifact evidence 均返回非零并给出稳定 error code。
- [ ] AC3：fixture 中每个 load-bearing planning contract 都有唯一 provenance entry；缺失、重复、未知 class、空 authority 或 stale statement digest 不能产生 `approved`。
- [ ] AC4：`necessary_implementation_choice` 缺少候选方案、选中方案、理由或 no-scope-expansion 结论时不能产生 `approved`。
- [ ] AC5：未确认的非常规 proposal 不能进入 approved execution contract；普通 planning confirmation 不能满足专用 scope confirmation。
- [ ] AC6：非必要机制引发风险的 fixture 返回 planning revision，删除或替换机制后才通过；fixture 不新增 scope expansion。
- [ ] AC7：`approved`、`revision_required`、`clarify_scope`、`blocked` 每个出口只映射一个 consumer；unknown/multiple/unmapped 结果 fail closed。
- [ ] AC8：现有 `planning-approval.json` 是唯一 planning gate artifact；新 schema 绑定完整 AI/human evidence，非 approved 状态不能启动 task。
- [ ] AC9：旧 active schema 1.2 artifact 触发完整迁移 review，archive 字节保持不变。
- [ ] AC10：workflow approval 区只含 mandatory Skill invocation、四出口 mapping、target/stop marker 与 fail-closed 规则，不再保存该 Skill 的内部 checklist、confirmation、recorder command 或 recovery algorithm。
- [ ] AC11：shared/Codex/Claude/Cursor 安装副本与 canonical package 一致，dogfood apply 后无 package drift 和 unresolved `.new`/`.bak`。
- [ ] AC12：ownership validator 证明本次 diff 未新增或修改 upstream-owned overlay。
- [ ] AC13：targeted unit/package/preset tests、Python compile、Bash syntax、JSON schema、task validate、`git diff --check` 通过。
- [ ] AC14：clean throwaway 完成 marketplace/preset/install invocation/update/reapply/sidecar 全链路，README 命令可执行。
- [ ] AC15：durable docs/spec、canonical workflow、package contract、runtime、tests 与 installed copies 对同一 provenance、confirmation、exit 和 migration 语义保持一致。

## 8. Open Questions

无。实施若发现必须改变四类 provenance、四出口、专用确认边界、existing artifact 复用或 no-upstream-overlay 范围，必须返回 Phase 1 更新三份 planning artifact 并取得新的 post-planning confirmation。
