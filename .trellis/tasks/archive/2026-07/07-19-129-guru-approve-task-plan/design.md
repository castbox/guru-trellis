# #129 设计：`guru-approve-task-plan` semantic closed loop

## 1. 设计目标

把 Phase 1 planning approval 从 workflow 展开文本与 shared recorder/checker 的隐式组合迁移为一个 active Guru Skill package。迁移后：

- global workflow 只编排 stable Skill id 与 typed exits；
- canonical Skill package 独占 planning adequacy、provenance、implementation choice、unusual scenario proposal、AI Gate、confirmation policy、re-entry 与 artifact contract；
- shared runtime 只录制和校验确定性事实；
- `planning-approval.json` 仍是唯一 planning gate artifact；
- `guru-review-contract-wording` 仍是唯一 wording owner；
- preset 只 additive 分发 Guru namespace asset，本任务不触碰 upstream-owned overlay。

## 2. 所有权模型

| 层 | 唯一职责 | 明确不拥有 |
| --- | --- | --- |
| Global workflow | phase 顺序、mandatory invocation、external exit consumer、fail-closed stop | adequacy dimensions、provenance 分类、choice 判断、confirmation 细节、recorder 命令 |
| `guru-approve-task-plan` package | entry contract、语义闭环、planning revision、provenance、非常规 proposal、AI Gate、confirmation、artifact schema、typed exits | initial change request review、issue mutation loop、wording vocabulary、Phase 2 check、Branch Review |
| `guru-review-contract-wording` | fixed `planning_artifacts` scope、wording scan/rewrite/classification evidence | planning adequacy、provenance、scope expansion、task activation |
| `guru-clarify-requirements` | source authority、scope classification、issue/body/ledger mutation、re-entry evidence | planning pass、artifact approval |
| Shared runtime | path/hash/size/base/HEAD、schema、digest、projection、freshness、exit invariant、artifact write/check | semantic classification、充分性、proposal 必要性、user intent、route intent |
| Preset installer | registry/package/discovery copy 安装、manifest/hash/permission、upgrade/reapply | AI workflow judgment、upstream file patch |

## 3. Entry 与 mode parity

`interface.json` 的 workflow/standalone `entry_precondition_ids` 使用同一有序集合：

1. `runtime_dependency`
2. `task_workspace`
3. `requirement_authority`
4. `planning_artifacts`
5. `docs_ssot_plan`
6. `contract_wording_evidence`
7. `scope_ledger`
8. `repository_snapshot`
9. `invocation_freshness`

Workflow mode 从 active task route 获得 task locator。Standalone mode 先通过 task runtime/current checkout 发现同一 locator，然后执行相同 boundary 与 evidence check。两种 mode 不存在弱化路径。

Entry checker 复用现有 task workspace、issue review、contract wording 与 file-digest helpers。缺失 source authority、非 current review evidence、三文档缺失、Docs SSOT Plan 无法定位、wording 非 `planning_artifacts:pass`、scope ledger 不一致、base/HEAD snapshot stale 或 artifact digest mismatch 均阻塞 recorder。

## 4. Canonical package

新增：

```text
trellis/skills/guru-team/packages/guru-approve-task-plan/
├── SKILL.md
├── interface.json
├── references/contract.md
├── schemas/planning-approval.schema.json
├── examples/planning-approval.json
├── scripts/record-planning-approval.sh
├── scripts/check-planning-approval.sh
└── tests/test_contract.py
```

`trellis/skills/guru-team/registry.json` 新增 active entry：

```json
{
  "id": "guru-approve-task-plan",
  "state": "active",
  "name": "guru-approve-task-plan",
  "package": "packages/guru-approve-task-plan",
  "interface": "packages/guru-approve-task-plan/interface.json",
  "supported_platforms": ["shared", "codex", "cursor", "claude"],
  "validator_command": "check-skill-packages",
  "workflow_route_id": "phase-1-task-plan-approval"
}
```

Interface 使用 semantic 五阶段 profile，并声明 runtime commands `record-planning-approval` 与 `check-planning-approval`。Package wrapper 只通过 installed `run-skill-command` dispatcher 调用 shared runtime；脱离完整 preset 时以 exit code 2 阻塞。

## 5. Semantic closed loop

```text
validate task/workspace/authorities/snapshot
  -> read prd/design/implement + Docs SSOT Plan
  -> AI adequacy and ambiguity review
  -> AI provenance and implementation-choice review
  -> AI unusual-scenario review
  -> revise planning when task-internal gaps exist
  -> obtain exact unusual-scenario confirmation when triggered
  -> route authority changes to guru-clarify-requirements
  -> validate current planning_artifacts wording pass
  -> AI final Review Gate
  -> display three planning links
  -> obtain explicit post-planning confirmation
  -> recorder + checker
  -> one typed exit
```

`revision_required` 的 re-entry identity 绑定 task、三文档 digest、review result digest 与上一 artifact facts digest。文档修订后必须重跑 `guru-review-contract-wording:planning_artifacts`；旧 wording evidence 不能被投影到新 planning content。

`clarify_scope` 只在 source authority 或 scope ledger 必须变化时返回。Consumer 完成 `guru-clarify-requirements` 后，本 Skill 从完整 entry 开始重新验证 authority、context、planning、wording 与 HEAD，不接续旧 semantic pass。

## 6. Provenance contract

### 6.1 Load-bearing item

Planning 文档使用一个权威 provenance matrix，固定位置为 `design.md`，其 entry 对每个执行中不可缺失的 requirement、design contract、acceptance item、test obligation 建立稳定标识。Recorder 将 AI 已审查 entry 投影到 `planning-approval.json.provenance_review.entries[]`：

```json
{
  "id": "R4-provenance-entry-coverage",
  "artifact_path": ".trellis/tasks/<task>/prd.md",
  "locator": "R4. Requirement provenance",
  "statement_sha256": "<sha256>",
  "classification": "explicit_requirement",
  "authority_refs": ["issue:129#requirement-provenance"],
  "reason": "Issue #129 explicitly requires one provenance class for every load-bearing planning contract.",
  "implementation_choice": null,
  "scope_expansion": null
}
```

`statement_sha256` 由 canonical UTF-8 statement bytes 计算。Runtime 只验证 locator 可解析、statement bytes current、digest 相符、id 唯一、字段组合满足 schema。AI 决定哪些 statement load-bearing、coverage 是否完整和 classification 是否正确。

### 6.2 四类 provenance

| Class | 必填 evidence | Approved execution 中的状态 |
| --- | --- | --- |
| `explicit_requirement` | authority ref 与明确 source locator | 进入 execution contract |
| `necessary_implementation_choice` | 候选方案、选中方案、理由、`product_scope_expanded=false`、`risk_scope_expanded=false` | 进入 execution contract |
| `approved_scope_expansion` | exact proposal digest、专用 confirmation、current source authority ref | 进入 execution contract |
| `out_of_scope_proposal` | proposal reason 与 route/disposition | 不进入 execution contract |

`provenance_review.coverage` 记录 reviewer、summary、reviewed entry ids、`all_load_bearing_items_covered` 与 review digest。`approved` 要求该布尔值由 AI 显式写为 `true`；runtime 只校验值和 entry/digest 完整性，不能生成 `true`。

### 6.3 Implementation choice

`necessary_implementation_choice` 的 `implementation_choice` 结构固定含：

- `alternatives[]`：有序候选，每项有 id 与 tradeoff；
- `selected_id`：必须命中一个候选；
- `selection_reason`：非空；
- `product_scope_expanded=false`；
- `risk_scope_expanded=false`。

AI 发现 choice 改变产品、风险或运维 scope 时不得保留该 class，必须改成 `out_of_scope_proposal` 并进入 clarification，或在 current authority 更新后改成 `approved_scope_expansion`。

## 7. 非常规场景 proposal contract

`unusual_scenario_review.candidates[]` 支持以下 scenario class：

- `security_or_threat`
- `attack_or_malicious_actor`
- `toctou_or_concurrency_race`
- `fault_injection_or_crash_consistency`
- `cross_os_atomicity`
- `other_nonstandard`

每个 candidate 记录 scenario、trigger evidence、scope、cost、alternatives、consequence、source requirement refs 与 disposition。Disposition 为互斥集合：

- `explicit_requirement`
- `mechanism_removed`
- `mechanism_replaced`
- `confirmed_scope_expansion`
- `clarification_required`
- `out_of_scope`

`confirmed_scope_expansion` 必须带 `confirmation_kind=dedicated-unusual-scenario`、proposal SHA-256、用户原始确认摘要、确认时间和更新后的 authority ref。`user_confirmation.kind=post-planning-approval` 与该结构完全分离，任何普通确认值都不能填入专用字段。

当前 Issue #129 已明确排除新增非常规加固，本 task 的 expected candidates 为空。测试 fixture 必须覆盖非必要 lock/atomic mechanism 引发风险的场景，并证明 `mechanism_removed` 或 `mechanism_replaced` 后进入新 review，而不是创建隐含 scope expansion。

## 8. `planning-approval.json` v2

### 8.1 版本与唯一 artifact

路径保持 `{TASK_DIR}/planning-approval.json`。新增 closed Draft 2020-12 schema，schema id 为 `guru-planning-approval-2.0`，payload 使用：

```json
{
  "schema_version": "2.0",
  "skill_id": "guru-approve-task-plan"
}
```

使用新 major version 是因为新增四出口 union、provenance、unusual proposal、AI Gate、consumer 与 facts digest 均是 mandatory contract；继续标记为 1.2 会把不兼容 artifact 伪装成旧 public API。

### 8.2 核心结构

```json
{
  "schema_version": "2.0",
  "skill_id": "guru-approve-task-plan",
  "generated_at": "<time>",
  "mode": "workflow",
  "task": {},
  "repository_snapshot": {},
  "requirement_authorities": [],
  "reviewed_artifacts": [],
  "approved_artifacts": [],
  "docs_ssot_plan": {},
  "contract_wording_review": {},
  "ambiguity_review": {},
  "provenance_review": {},
  "unusual_scenario_review": {},
  "semantic_review": {"ai_review_gate": {}},
  "user_confirmation": {},
  "typed_exit": "approved",
  "consumer": {"kind": "workflow", "id": "phase-1-task-activation"},
  "reason": "<human-readable reason>",
  "facts_sha256": "<sha256>"
}
```

`reviewed_artifacts` 与 `approved_artifacts` alias 在 v2 继续保留，且 bytes 必须相同。`ambiguity_review` 继续从 current `guru-review-contract-wording:planning_artifacts:pass` 做 compatibility projection；本 Skill 不复制 scanner owner。

### 8.3 Exit union

| Exit | Gate 与 evidence invariant | Consumer |
| --- | --- | --- |
| `approved` | AI Gate passed；provenance complete；无未处理 unusual proposal；wording pass；post-planning confirmation exact；artifact current | workflow `phase-1-task-activation` |
| `revision_required` | AI Gate 记录可在 task 内修订的缺口；revision actions 非空；无 authority mutation | Skill `guru-approve-task-plan` |
| `clarify_scope` | authority/scope mutation proposal 非空；approved execution 未包含该 proposal | Skill `guru-clarify-requirements` |
| `blocked` | 缺失 authority、用户拒绝必需 proposal、外部 blocker 或无法安全修订 | stop `task-plan-approval-blocked` |

Exit/Gate/consumer 是 closed one-of union。Recorder 只写入 AI 已决定的 exit；checker 只验证结构与双向 invariant。

### 8.4 HEAD freshness

Approval invocation 记录 selected base、base ref、base HEAD、current HEAD 与 dirty paths。Recorder 前与 checker 后均重读 snapshot；任一值在同一 invocation 中漂移则阻塞。

`approved` 被 task activation 消费后，implementation 修改 working tree 与后续 task work commit 是预期状态变化。Downstream checker 继续以三文档 digests、authority/wording freshness和 task identity作为 planning approval validity 主条件；它不得只因 task activation 后 HEAD 改变而宣告 plan stale。若 planning 文档或 source authority 改变，则完整重入本 Skill。

## 9. Workflow route

Canonical workflow 与 dogfood workflow 的 Phase 1 approval 区收敛为：

```markdown
<!-- guru-skill-invoke: {"skill":"guru-approve-task-plan","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-approve-task-plan","exit":"approved","consumer":{"kind":"workflow","id":"phase-1-task-activation"}} -->
<!-- guru-skill-exit: {"skill":"guru-approve-task-plan","exit":"revision_required","consumer":{"kind":"skill","id":"guru-approve-task-plan"}} -->
<!-- guru-skill-exit: {"skill":"guru-approve-task-plan","exit":"clarify_scope","consumer":{"kind":"skill","id":"guru-clarify-requirements"}} -->
<!-- guru-skill-exit: {"skill":"guru-approve-task-plan","exit":"blocked","consumer":{"kind":"stop","id":"task-plan-approval-blocked"}} -->
```

Workflow 保留 task activation 这个 global transition，但不再展开 links、provenance、confirmation、recorder/checker 或 revision loop。Missing package、unknown/multiple/unmapped exit、consumer 重复或 marker 缺失均 fail closed。

## 10. Shared runtime 与 wrappers

现有 `record-planning-approval` / `check-planning-approval` runtime command 名保持不变，避免创建第二套命令 API。实现演进：

1. 新增 schema loader 与 v2 payload digest。
2. 复用 workspace boundary、task locator、file digest、contract wording checker、issue evidence和 Git snapshot helper。
3. Recorder 接收一个 AI-reviewed input JSON，重建所有 deterministic facts，再写 task-local artifact。
4. Checker 重建 current facts、验证 closed schema、provenance statement binding、confirmation proposal binding、exit union、facts digest与 freshness。
5. Legacy top-level wrappers作为 preset compatibility entry 保留；canonical package wrappers成为 Skill public entry，二者都通过同一 shared runtime command。
6. Runtime 不扫描 planning 文本来自动选 load-bearing item，不生成 provenance class，不决定 choice scope，不决定 scenario 必要性，不生成 AI Gate pass。

## 11. Migration 与 bootstrap

### 11.1 Existing active tasks

- Schema 1.2 active artifact 在新 package 生效后不能直接进入 task activation或下游 gate。
- Consumer 展示三份文档并执行完整新 Skill review；文档 digest未变化时，已有 post-planning confirmation可作为同一 reviewed content 的 general confirmation evidence重新录制。
- 非常规 proposal confirmation不能从旧 general confirmation推导。
- Archive artifact不改写。

### 11.2 当前 #129 task

本 task 必须在 package存在前通过当前 workflow门禁启动，因此使用两步 bootstrap：

1. Phase 1 按 current runtime 写 schema 1.2 approval并启动 task。
2. Phase 2 安装新 package/runtime后，在三份 planning文档 digest不变的前提下，由主会话按新 Skill contract重新执行 semantic review，复用本轮用户对同一文档的 post-planning confirmation，写 v2 artifact并运行新 checker。

若三份 planning文档任一内容变化，必须重新展示全部链接并取得 fresh confirmation，不能走 bootstrap复用。

## 12. Docs SSOT Plan

### 12.1 状态

- Docs state：`complete_docs`
- Evidence：
  - `docs/requirements/README.md`
  - `docs/requirements/requirement-main.md`
  - `docs/requirements/guru-team-trellis-flow.md`
  - `.trellis/spec/workflow/index.md`
  - `.trellis/spec/workflow/skill-package-contract.md`
  - `.trellis/spec/workflow/workflow-contract.md`
  - `.trellis/spec/workflow/data-contracts.md`
  - `.trellis/spec/workflow/companion-scripts.md`
  - `.trellis/spec/workflow/quality-guidelines.md`
  - `.trellis/spec/docs/public-docs.md`
  - `.trellis/spec/preset/overlay-guidelines.md`
  - `.trellis/spec/preset/upstream-ownership.md`
  - `trellis/workflows/guru-team/workflow.md`
  - `trellis/workflows/guru-team/README.md`
  - `trellis/presets/guru-team/README.md`

### 12.2 Strategy

- Strategy：`ssot_first`
- Reason：本任务修改 public Skill id、artifact schema、workflow route、runtime command语义、platform distribution与upgrade contract。稳定合同必须先写入 durable docs/spec/package contract，再让 task artifact只保存 task delta与 evidence。

### 12.3 Durable targets

| Contract | Durable target |
| --- | --- |
| Product/flow requirement | `docs/requirements/requirement-main.md`、`docs/requirements/guru-team-trellis-flow.md`、`docs/requirements/README.md` |
| Skill/public API | `.trellis/spec/workflow/skill-package-contract.md`、canonical package `references/contract.md`、schema、interface |
| Workflow route | `.trellis/spec/workflow/workflow-contract.md`、canonical/dogfood workflow |
| Artifact/runtime | `.trellis/spec/workflow/data-contracts.md`、`.trellis/spec/workflow/companion-scripts.md` |
| Tests/gates | `.trellis/spec/workflow/quality-guidelines.md` |
| Public install/docs | `.trellis/spec/docs/public-docs.md`、workflow README、preset README |
| Additive ownership | `.trellis/spec/preset/overlay-guidelines.md`、`.trellis/spec/preset/upstream-ownership.md` |

### 12.4 Task delta merge

必须合并回 durable docs 的 task delta：provenance model、unusual proposal confirmation、v2 artifact、四出口、bootstrap migration、no-upstream-overlay、throwaway/update/reapply gate。

保留为 task history only：Phase 0 evidence、官方文档核对摘要、当前 task 的 bootstrap 重录过程、implementation handoff、Phase 2 check 与 Branch Review raw evidence。

## 13. 分发与 upgrade/update

- Canonical source：`trellis/skills/guru-team/**`、`trellis/workflows/guru-team/**`、`trellis/presets/guru-team/**`。
- Dogfood installed source：`.trellis/guru-team/skills/**`、`.agents/skills/guru-approve-task-plan/**`、`.codex/skills/guru-approve-task-plan/**`、`.claude/skills/guru-approve-task-plan/**`、`.cursor/skills/guru-approve-task-plan/**`、`.trellis/workflow.md`。
- 先改 canonical，再运行 preset apply 同步 dogfood；安装副本不作为 source。
- `trellis update` 后必须重装 marketplace workflow并reapply preset，验证 package、runtime、discovery copy与workflow route恢复且没有 unresolved `.new`/`.bak`。
- `check-upstream-ownership.sh` 必须证明 overlay inventory无新增、无 payload drift、无 baseline rewrite。

## 14. 中台知识门禁

本任务不涉及 go-guru、proto-guru、Unity3D Guru SDK、Flutter Guru SDK 或其它中台 SDK/framework contract，因此 Middle-platform Knowledge Gate 标记为不适用。

## 15. 风险与回滚点

| 风险 | 阻断或回滚点 |
| --- | --- |
| Package 与现有 wording owner重复 | contract test发现 vocabulary/scanner副本即回滚重复内容，只保留 evidence ref |
| Runtime自动生成 provenance或pass | fixture发现 AI字段被推导即回滚 helper，改为只校验输入 |
| General confirmation被当作unusual confirmation | schema/fixture失败即阻断 `approved` |
| V2迁移使当前 task gate失效 | bootstrap重录失败则停止 Phase 2 check，不用手工拼 artifact |
| Workflow仍展开内部步骤 | workflow marker/text audit失败即继续收敛 |
| Platform copy与canonical漂移 | source/installed validator或dogfood drift失败即禁止提交 |
| Preset写入upstream-owned path | ownership validator失败即回滚该 path改动 |
| Update后package丢失或产生sidecar | throwaway gate失败即禁止发布 |
| 新测试只覆盖恶意篡改 | 没有正常路径复现依据时移出 current acceptance |

## 16. Provenance matrix

| ID | Load-bearing contract | Covered planning IDs | Class | Authority / choice |
| --- | --- | --- | --- | --- |
| P1 | Skill成为 planning approval唯一 semantic owner | R1、R3、R7；AC1、AC8、AC10、AC15 | `explicit_requirement` | Issue #129“定位” |
| P2 | Workflow与standalone同门禁 | R2；AC2 | `explicit_requirement` | Issue #129“Modes” |
| P3 | 四类 provenance覆盖全部load-bearing contract | R4；AC3、AC4 | `explicit_requirement` | Issue #129“Requirement provenance” |
| P4 | Untriggered unusual scenario不进入 ordinary choice | R5；AC5 | `explicit_requirement` | Issue #129“非常规场景确认” |
| P5 | 风险源自非必要机制时先删除或替换机制 | R5；AC6 | `explicit_requirement` | Issue #129“非常规场景确认”与 acceptance |
| P6 | 使用 `planning-approval.json` v2 closed union而不新建artifact | R7；AC8、AC9 | `necessary_implementation_choice` | 候选为扩展1.2、v2、平行artifact；选v2保持现有路径并显式声明breaking schema migration |
| P7 | Provenance entry使用 statement digest + locator | R4；AC3、AC4 | `necessary_implementation_choice` | 候选为文档inline tag、只存summary、结构化entry；选结构化entry获得deterministic freshness且不改变产品scope |
| P8 | 现有runtime command名保持不变 | R8；AC15 | `necessary_implementation_choice` | 候选为新命令名或复用；复用避免第二API且不改变产品scope |
| P9 | Wording evidence由 #114唯一owner提供 | R3、R7；AC2、AC15 | `explicit_requirement` | Issue #129 closed loop与Scope |
| P10 | 四 typed exits与唯一consumer | R6；AC7 | `explicit_requirement` | Issue #129“External Exits” |
| P11 | No new upstream-owned overlay | R9；AC11、AC12 | `explicit_requirement` | Issue #129 acceptance、#128、根 `AGENTS.md` |
| P12 | Docs采取 `ssot_first` | Docs SSOT Plan；AC15 | `necessary_implementation_choice` | 候选为delta-first或ssot-first；public workflow/schema变更选择ssot-first且不扩张产品scope |
| P13 | #130/#131/#132不进入当前实现 | Scope 4.2 | `explicit_requirement` | Issue #129 Scope与issue ledger |
| P14 | 本task无unusual scope proposal | R5；AC5、AC6 | `explicit_requirement` | Issue #129 normal-operation boundary明确排除新增非常规加固 |
| P15 | Package/runtime/preset/install验证覆盖完整 | R10；AC13、AC14、AC15；`implement.md` Step 6/7与Phase 2语义检查 | `explicit_requirement` | Issue #129 acceptance要求tests、dogfood、throwaway、update/reapply |
| P16 | 当前task使用两步bootstrap迁移 | R7；AC9；`implement.md` Step 8 | `necessary_implementation_choice` | 候选为阻塞自举、手工拼v2、两步重录；两步重录复用相同文档确认并保持recorder/checker边界 |

当前 matrix 无 `approved_scope_expansion` 或 `out_of_scope_proposal` entry。

`implement.md` 的 Step 1-8、验证命令、Phase 2语义检查与完成条件只分解上表已覆盖的R/AC，不引入新的产品或风险合同。实施中新增load-bearing contract时，必须先更新本matrix与对应R/AC，并重新执行planning review。
