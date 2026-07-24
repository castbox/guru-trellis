# #116 技术设计：guru-review-task-publication 闭环 Skill

## 1. 设计结论

`guru-review-task-publication` 是 Branch Review `passed` 之后、finalization 之前的
唯一 publication semantic review owner。它采用 Interface 1.3、
`judgment_mode=semantic`，拥有双入口、十维 AI Review Gate、metadata-only 内部修订
闭环、唯一 `pr-readiness.json` gate 和三个 typed exits。

全局 workflow 只调用该 Skill 并消费 exits；shared runtime 只采集事实、记录已完成的
AI 判断、校验 freshness 与投影 public DTO。Issue scope、PR body 充分性、Docs SSOT、
finding route、安全/部署影响和最终 pass 均不得由脚本决定。

## 2. 设计原则

1. Skill-first：step-local semantic 行为只在 package contract 中定义。
2. Minimal handoff：public DTO 只携带唯一 consumer 的直接输入。
3. Private evidence：审查正文、hash、路径、review history 与 publish input 保持
   task-local。
4. One gate：`pr-readiness.json` 是唯一 publication readiness gate，不并行创建
   semantic pass artifact。
5. Fresh review：stale re-entry 与 metadata revision 后都必须重新完成当前十维审查。
6. No semantic script：deterministic success、空 findings 或 changed-file 分类不能生成
   `ready`。
7. Canonical first：先改 durable SSOT 与 canonical package，再由 preset 同步安装副本。
8. Compatibility by ownership：#116 激活 #131 bridge，但不实现 #118/#119/#132。
9. Honest-but-fallible：只处理正常错误、遗漏、stale 与 mismatch，不引入攻击模型、
   锁、TOCTOU 或 crash-consistency 范围。

## 3. 所有权与修改面

| Owner | Canonical path | 职责 |
| --- | --- | --- |
| Publication Skill | `trellis/skills/guru-team/packages/guru-review-task-publication/` | Skill、contract、Interface、schemas、examples、wrapper、eval、tests |
| Branch Review producer | `trellis/skills/guru-team/packages/guru-review-branch/interface.json` | 把 planned seed 替换为 #116 target-owned authoring seed，输出 bytes 不变 |
| Registry | `trellis/skills/guru-team/registry.json` | #116 active、`guru-finalize-task` planned identity、11/42 closure |
| Shared runtime | `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` | facts、recorder、checker、wrapper dispatch、source/installed validation |
| Workflow | `trellis/workflows/guru-team/workflow.md` | mandatory invocation、三 exits、唯一 consumers、re-entry、fail-closed stop |
| Extension inventory | `trellis/guru-team-extension.json` | command、managed asset、public/private schema 与 active package inventory |
| Preset | `trellis/presets/guru-team/` | 安装、平台复制、throwaway、update/reapply、ownership 与 drift 验证 |
| Durable Docs | `.trellis/spec/**`、`docs/requirements/**`、README | 稳定 contract、数据、脚本、质量、安装与流程 SSOT |

以下路径只能由 canonical source/preset 生成，不作为独立设计源：

- `.trellis/guru-team/skills/guru-review-task-publication/`
- `.agents/skills/guru-review-task-publication/`
- `.codex/skills/guru-review-task-publication/`
- `.claude/skills/guru-review-task-publication/`
- `.cursor/skills/guru-review-task-publication/`
- `.trellis/workflow.md`

禁止修改或 overlay upstream `trellis-finish-work` Skill、command、prompt；其集成与移除
分别由 #119、#132 承担。

## 4. Interface 1.3 public input

### 4.1 Profile `publication_review`

完整 input：

```json
{
  "profile": "publication_review",
  "mode": "workflow",
  "task_ref": ".trellis/tasks/07-24-116-review-task-publication",
  "reviewed_head": "0123456789abcdef0123456789abcdef01234567",
  "review_ref": "review-current:opaque",
  "review_intent": "initial_review"
}
```

Required fields 固定为：

```text
profile, mode, task_ref, reviewed_head, review_ref, review_intent
```

目标拥有的 partition：

| Partition | Fields |
| --- | --- |
| `seed_fields` | `task_ref`、`reviewed_head`、`review_ref` |
| `authoring_fields` | `profile`、`mode`、`review_intent` |

Producer 是 `guru-review-branch:passed`。激活时把其
`planned_skill_input_seed` 原位替换为 `skill_input_authoring_seed`；producer output
schema、example 与 public bytes 不变。Merge 必须 disjoint、complete、no-overwrite。

### 4.2 Profile `publication_review_stale`

完整 input：

```json
{
  "profile": "publication_review_stale",
  "mode": "workflow",
  "task_ref": ".trellis/tasks/07-24-116-review-task-publication",
  "stale_reason": "finalization-precondition-drift",
  "review_intent": "stale_reentry_review",
  "reentry_context": "rebuild publication evidence against current owner facts"
}
```

Required fields 固定为：

```text
profile, mode, task_ref, stale_reason, review_intent, reentry_context
```

未来 #118 producer partition：

| Partition | Fields |
| --- | --- |
| `seed_fields` | `task_ref`、`stale_reason` |
| `authoring_fields` | `profile`、`mode`、`review_intent`、`reentry_context` |

#116 现在发布 target schema、aggregate schema、完整 example、authoring example 与 eval
fixture，但不发布 #118 target schema，也不激活尚不存在的 producer edge。Registry 的
planned `guru-finalize-task` 只提供 stable identity。

### 4.3 Closed enums

- `mode`：`workflow`、`standalone`。
- `review_intent`：
  - `initial_review`
  - `metadata_revision_review`
  - `stale_reentry_review`

Standalone 直接发现 task，但执行相同 preconditions、semantic dimensions、
confirmation、artifact、freshness 与 pass contract。

## 5. Public outputs 与 consumer

### 5.1 `ready`

```json
{
  "exit_id": "ready",
  "task_ref": ".trellis/tasks/07-24-116-review-task-publication",
  "reviewed_head": "0123456789abcdef0123456789abcdef01234567",
  "publication_ref": "publication-current:opaque"
}
```

唯一 consumer 为 planned `guru-finalize-task`，seed 精确为
`task_ref/reviewed_head/publication_ref`。`publication_ref` 是 owner 生成并由 checker
校验的 opaque current token；consumer 不解析其中内容。

### 5.2 `return_to_task_work`

```json
{
  "exit_id": "return_to_task_work",
  "task_ref": ".trellis/tasks/07-24-116-review-task-publication",
  "finding_refs": ["PUB-001"],
  "resume_target": "phase-2"
}
```

唯一 consumer 为 `trellis-continue` workflow router。Router 必须重新经过
implementation、Phase 2、commit、Branch Review，再使用新的 `reviewed_head` 与
`review_ref` 调用 publication review。

### 5.3 `blocked`

```json
{
  "exit_id": "blocked",
  "reason_code": "external-confirmation-required",
  "remediation": "obtain the named external decision and re-enter"
}
```

唯一 consumer 为 `stop:task-publication-review-blocked`。

每个 exit 有独立 schema/example/projection。Unknown、missing、multiple、unmapped、
consumer mismatch、projection leftover 或 schema mismatch 全部 fail closed。

## 6. Entry preconditions 与 private evidence

按顺序执行：

1. `runtime_dependency`
2. `task_workspace`
3. `task_identity`
4. `branch_review_handoff`
5. `planning_approval`
6. `phase2_check`
7. `issue_scope_ledger`
8. `docs_ssot_reconciliation`
9. `branch_review_evidence`
10. `publication_content`
11. `review_range_and_working_tree`
12. `invocation_freshness`

Runtime 通过 `task_ref` 读取 private evidence：

- task、workspace、base/head/branch 与 intake binding；
- `prd.md`、`design.md`、`implement.md`、`planning-approval.json`；
- `phase2-check.json`；
- `agent-assignment.json`、raw reports、`review.md`、`review-gate.json`；
- `issue-scope-ledger.json`；
- Docs SSOT Plan 与 implementation reconciliation；
- `pr-body.md`、`finish-summary-index.json`；
- current diff、working tree、metadata tail；
- re-entry 时的 current `pr-readiness.json`。

Public input 不携带以上内容或绝对路径。缺失、failed、stale、wrong task/workspace、
HEAD/hash/scope mismatch、非 allowlisted tail、body/index identity 不一致时停止在
entry gate，并禁止 Agent 用推测补足。

## 7. 十维 semantic review

AI 对每个 dimension 记录 `status`、`summary`、`evidence_refs` 与必要 findings：

1. `diff_outcome_consistency`
2. `issue_scope_closure`
3. `pr_body_quality`
4. `validation_claims`
5. `branch_review_summary`
6. `docs_ssot_reconciliation`
7. `safety_deployment_impact`
8. `finish_summary_semantics`
9. `metadata_tail_integrity`
10. `artifact_binding_freshness`

所有维度必须是当前 invocation 的实际判断；不得从命令成功、changed-file allowlist、
零 scanner error 或旧 artifact 自动复制 pass。`ready` 要求十维全部 pass、current-scope
findings 全部有 closure evidence、无 unresolved revision/blocking item。

## 8. Finding model 与 route

每个 finding 的 required fields：

```text
finding_ref
dimension
summary
scope_basis
evidence_refs
affected_artifacts
route_class
status
closure_evidence
```

Route classes：

- `metadata_revision`：只修改 task-local `pr-body.md`、
  `finish-summary-index.json` 或 ledger 的 publication metadata。
- `task_work`：需要 code/test/durable docs/spec/workflow/schema/config/preset/
  CI/CD/deployment 变更，或会使 Branch Review stale。
- `external_blocker`：权限、外部状态或用户决定无法由当前 task work 解决。

AI 决定 route。Runtime 只验证 route 值、引用、artifact allowlist 与对应 exit shape。
Current-scope finding 不得降级成 observation/follow-up。

## 9. Metadata-only 内部闭环

内部状态机：

```text
review
  -> metadata finding
  -> AI revises task-local metadata
  -> deterministic reread/rescan
  -> fresh ten-dimension semantic review
  -> record/check
  -> typed exit
```

内部修订不向 workflow 返回中间 exit。若修订期间发现非 metadata drift，旧审查立即
stale，返回 `return_to_task_work`。若出现外部阻塞，返回 `blocked`。

Metadata 修订路径由 contract closed allowlist 管理；不能通过文件扩展名或
changed-file 推断。修订历史保存在 gate artifact，不进入 public output。

## 10. `pr-readiness.json` 分层设计

### 10.1 唯一 gate

Artifact path 固定为：

```text
{TASK_DIR}/pr-readiness.json
```

核心层：

```text
schema/skill/task identity
reviewed_head/review_ref
invocation profile/mode/intent
semantic dimensions
findings and closure
scope/docs/safety/deployment conclusions
metadata revision history
AI gate conclusion
typed exit and consumer
```

Deterministic binding 层：

```text
workspace/base/head/diff identity
planning/phase2/review/ledger hashes
pr-body/index hashes
working-tree/metadata-tail facts
artifact/facts digest
publication_ref
```

Optional finalization-owned compatibility 层：

```text
publish_inputs
```

### 10.2 Lifecycle

1. Publication Skill 在 AI Review Gate 之后调用 recorder。
2. Recorder 重读 current facts、写 semantic conclusion 与 deterministic bindings。
3. Checker 重建 facts、验证 schema/exit/consumer/freshness，绝不决定 semantic pass。
4. `ready` projection只从 checker-passed current gate读取最小 DTO。
5. Future finalization helper只能在 checker-passed `ready` gate 上添加/校验
   `publish_inputs`，不能覆盖 semantic sections、typed conclusion 或
   `publication_ref`。
6. Non-ready replacement 或 stale re-entry 必须记录 replacement identity，旧 artifact
   不得被当作 current pass。

当前 `build_pr_readiness_snapshot()` 必须迁移成 compatibility augmentation/checker，
移除其“无条件写 `ready=true` 即完成审查”的语义。已有 reader 保持读取兼容，但不能把
legacy snapshot 解释为新 gate pass。

## 11. Runtime command 与脚本边界

预计新增或演进 commands：

```text
record-task-publication-review
check-task-publication-review
invoke-skill --skill guru-review-task-publication
validate-skill-contracts
validate-installed-skill-contracts
```

Package `scripts/invoke.sh` 只做 dispatcher：

1. 接收并验证 public input；
2. 定位 repo-local checker-passed owner result；
3. 调用 shared runtime；
4. 根据 actual `exit_id` 选择 per-exit schema；
5. stdout 只输出一个 public DTO。

Semantic eval 的 `expected_exit` 只能在 wrapper 返回之后由 grader 比较。它不得进入
native request、owner result、route selector 或 runtime environment。

Runtime 可决定的只有 objective validation/projection；不得决定 issue closure、
dimension 结论、finding route、PR body充分性、Docs SSOT、安全/部署或 ready。

## 12. Workflow 与 active graph

Canonical workflow 只表达：

```text
guru-review-branch:passed
  -> mandatory invoke guru-review-task-publication
     -> ready -> planned guru-finalize-task
     -> return_to_task_work -> implementation/check/commit/review loop
     -> blocked -> explicit stop
```

Workflow 不复制十维 checklist、finding model、metadata loop、artifact字段或
recorder/checker步骤。

Registry/closure：

- `guru-review-task-publication`：planned -> active。
- `guru-finalize-task`：新增 planned identity。
- Active closure：10 Skills/39 exits -> 11 Skills/42 exits。
- `production-minimal-handoff-v1`：保持精确 3 Skills/11 exits与原 activation identity。
- 每个 active input profile 与 exit 都有 current eval binding。

## 13. Eval 与测试矩阵

### 13.1 Public wrapper corpus

| Case | Mode/Profile | Actual exit |
| --- | --- | --- |
| initial workflow pass | workflow/publication_review | ready |
| initial standalone pass | standalone/publication_review | ready |
| implementation gap | workflow/publication_review | return_to_task_work |
| external blocker | workflow/publication_review | blocked |
| stale finalization handback | workflow/publication_review_stale | ready 或按 fixture route |
| body/index/ledger metadata fix | workflow/publication_review | ready after fresh review |
| metadata fix reveals durable drift | workflow/publication_review | return_to_task_work |

Shared、Codex、Claude、Cursor corpus byte-identical。平台测试分别覆盖 trusted Git root、
input protocol、unsupported/unavailable 与 shared parsing，且不得把 eval corpus 或
private runtime source注入 Agent request。

### 13.2 Contract/runtime negative cases

- 两个 profile 的 missing/extra/wrong enum/mega-object。
- seed/authoring overlap、union incomplete、merge overwrite。
- #131 output bytes变化或 stale planned bridge未替换。
- planned #118 target schema越权发布。
- unknown/multiple/unmapped exit 或 wrong consumer。
- legacy `ready=true` snapshot被误当 semantic pass。
- checker在 AI gate前被调用。
- stale head/review/body/index/ledger/docs/working tree。
- metadata-only loop中出现 non-metadata drift。
- deterministic trace选择 semantic conclusion/route。
- `expected_exit` 影响 wrapper实际 route。

### 13.3 Installation/update

- source与installed contract validators。
- package tests、runtime tests、workflow marker/route tests。
- preset installer、managed assets、executable bit、platform copies。
- clean repo init、marketplace preview/switch、preset install。
- `trellis update` 后 preset reapply。
- 零 unresolved `.new/.bak`，零 dogfood overlay drift。
- standalone real-wrapper smoke。

## 14. 兼容与迁移

1. #131 public output稳定；只替换其 consumer contract。
2. #146 production manifest identity与3/11集合稳定。
3. Legacy `pr-readiness.json` reader可识别旧 snapshot，但新 publication checker必须拒绝
   把它当 semantic gate。
4. Existing finalization helper迁移为 passing-gate augmentation；不新增第二 artifact。
5. Archived task artifact只读，不批量重写。
6. Upstream Trellis managed paths不被直接 patch；canonical preset负责恢复安装副本。
7. 若 installer产生 `.new/.bak`，逐项审查并在验收前清零，不静默覆盖用户内容。

## 15. 必要实现选择

| ID | 选择 | 替代方案 | 原因 |
| --- | --- | --- | --- |
| IC-01 | `pr-readiness.json` 单一artifact分层 | 新建 semantic gate artifact | 需求明确唯一 gate，分层能保持 finalization compatibility |
| IC-02 | Target-owned authoring seed | #131预先定义#116 schema；runtime补字段 | 符合 Interface 1.3 owner与无推断边界 |
| IC-03 | 新增 planned `guru-finalize-task` identity | ready 先路由 workflow placeholder | 为 ready 提供唯一 Skill consumer 且不越权实现 #118 |
| IC-04 | Metadata fix在Skill内部re-review | 每次修订返回workflow | 需求明确内部闭环，避免重复Phase链 |
| IC-05 | Compatibility helper只augment passing gate | 删除所有legacy publish input逻辑 | 保持现有finalization reader兼容且不冒充semantic pass |
| IC-06 | 复用shared runtime与Interface 1.3 | 新建独立publication runtime | 避免平行validator/dispatcher/schema机制 |

以上都是实现显式需求所必需的结构选择；不增加产品范围或风险范围。

## 16. 异常场景审查

| Candidate | Trigger | Disposition | 理由 |
| --- | --- | --- | --- |
| 恶意伪造gate/hash | 无当前需求 | out_of_scope | AGENTS与Issue明确只处理honest-but-fallible |
| 并发finalization竞态/TOCTOU | 无当前需求 | out_of_scope | #116只做publication semantic gate |
| lock/atomic write protocol | 无当前需求 | mechanism_removed | 常规recorder/checker freshness足够 |
| crash-consistency/fault injection | 无当前需求 | out_of_scope | 不属于验收矩阵 |
| cross-OS atomicity hardening | 无当前需求 | out_of_scope | 安装兼容通过现有preset tests验证 |
| stale/mismatch正常错误 | Issue明确要求 | explicit_requirement | 使用identity/freshness/checker fail closed |

没有需要 dedicated unusual-scenario confirmation 的候选，也没有 scope expansion。

## 17. Docs SSOT Plan

### 17.1 Classification

- Docs state：`partial_docs`。
- Strategy：`ssot_first`。
- Middle-platform Knowledge Gate：不适用。

### 17.2 Durable authorities

| Path | 计划合并的稳定 delta |
| --- | --- |
| `.trellis/spec/workflow/index.md` | #116 active状态、11/42 closure与导航 |
| `.trellis/spec/workflow/skill-package-contract.md` | 双入口、target-owned seed、三 exits、private/public边界 |
| `.trellis/spec/workflow/workflow-contract.md` | publication mandatory invoke、routes、re-entry与fail-closed |
| `.trellis/spec/workflow/data-contracts.md` | `pr-readiness.json`唯一gate、分层、freshness与兼容迁移 |
| `.trellis/spec/workflow/companion-scripts.md` | recorder/checker/wrapper命令与semantic禁止项 |
| `.trellis/spec/workflow/quality-guidelines.md` | 十维review、finding closure、eval与Phase2口径 |
| `.trellis/spec/preset/installer.md` | canonical/install/platform/throwaway/update/reapply要求 |
| `.trellis/spec/preset/overlay-guidelines.md` | canonical同步与dogfood drift |
| `.trellis/spec/preset/upstream-ownership.md` | 不overlay finish family与ownership断言 |
| `.trellis/spec/docs/public-docs.md` | README/requirements对active Skill与命令的一致性 |
| `docs/requirements/requirement-main.md` | publication semantic gate稳定产品/流程需求 |
| `docs/requirements/guru-team-trellis-flow.md` | Branch Review到publication/finalization的路由 |
| `docs/requirements/README.md` | SSOT导航与active baseline |
| `README.md` | 用户可执行的discover/invoke/install/update命令 |
| `trellis/workflows/guru-team/README.md` | workflow行为与11/42 closure |
| `trellis/presets/guru-team/README.md` | preset分发、reapply与验证 |

### 17.3 Delta merge checkpoint

实现结束时逐条核对：

1. 实际 public fields/schema ids/commands 与 durable docs一致。
2. 11/42 closure、planned #118与3/11 production manifest数字一致。
3. 实际 test/install/update/reapply结果写入 task evidence，不把一次性命令输出塞入SSOT。
4. Durable docs不复制 package内部十维步骤；只定义跨组件稳定contract并链接owner。
5. 未完成的 remote marketplace verifier明确留给 finish/publish gate，不声明已验证。

### 17.4 Task-history-only

以下只保留在 task artifact：

- 单次审查finding与closure；
- 命令原始输出、临时repo路径、时间戳；
- eval fixture运行详情；
- implementation sub-agent与Phase2 reviewer过程；
- 本次 `.new/.bak` 处置记录。

### 17.5 No-change decisions

- 不更新业务中台/SDK知识库：无此场景。
- 不修改 upstream finish-work docs/assets：#119/#132 owning boundary。
- 不更新 production minimal handoff的Skill/exit集合：该manifest有独立固定范围。
- 不将 remote verification写成本地实施完成项：#117/finish gate owning boundary。

## 18. Provenance 与承接矩阵

| ID | 规划承接 | Provenance class | Authority |
| --- | --- | --- | --- |
| PV-01 | Interface 1.3 semantic Skill与阶段 | explicit_requirement | #116 body/comment、workflow spec |
| PV-02 | 双入口及两个partition | explicit_requirement | #116 accepted-current comment |
| PV-03 | 十维AI Gate与finding loop | explicit_requirement | #116 body/comment、AGENTS |
| PV-04 | 唯一分层`pr-readiness.json` | explicit_requirement | #116 body/comment |
| PV-05 | 三exits与唯一consumers | explicit_requirement | #116 comment、Interface 1.3 |
| PV-06 | #131 bridge原位激活 | explicit_requirement | #116 comment、#131 current Interface |
| PV-07 | planned `guru-finalize-task` identity | necessary_implementation_choice | IC-03 |
| PV-08 | compatibility helper只augment pass | necessary_implementation_choice | IC-05 |
| PV-09 | shared runtime/public wrapper复用 | explicit_requirement | #116 comment、companion script contract |
| PV-10 | real-wrapper跨平台corpus | explicit_requirement | #116 comment |
| PV-11 | 11/42与3/11不变边界 | explicit_requirement | live registry、#116 comment |
| PV-12 | canonical/preset/update/reapply | explicit_requirement | AGENTS、preset SSOT |
| PV-13 | Docs SSOT first/reconciliation | explicit_requirement | workflow contract、planning gate |
| PV-14 | 不实现#118/#119/#132或remote verifier | explicit_requirement | #116 scope/follow-ups |
| PV-15 | 不引入异常加固 | explicit_requirement | #116、AGENTS normal-operation boundary |

不存在 `approved_scope_expansion`。所有 out-of-scope proposal 已在第16节明确排除。

## 19. 停止与回退条件

实施中出现以下任一情况必须停止并回到表内指定的 owning Gate：

- GitHub authority或Issue scope发生实质变化；
- 需要破坏已有 public API、schema id、command或3/11 activation identity；
- 无法在不定义 #118 target schema的前提下给ready建立唯一consumer；
- 需要修改 upstream-owned finish/check/review assets；
- 发现 current base/head/workspace、planning approval或Branch Review evidence stale；
- clean install/update只能靠本机隐藏状态通过；
- 需要新增锁、原子写、攻击模型或其它未授权范围。

任务内可回退的实现变化通过普通修订与测试完成；scope/authority变化必须重新执行
requirements clarification与planning approval。
