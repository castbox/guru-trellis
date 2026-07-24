# #131 技术设计：guru-review-branch 闭环 Skill

## 1. 设计原则

1. Branch Review 的全部语义判断收敛到一个 `judgment_mode=semantic` Skill。
2. Workflow 只拥有全局 phase、mandatory invocation、typed route 与 stop。
3. Reviewer、closure、final pass 都是 AI 判断；script 只记录和验证客观事实。
4. Public DTO 只携带 direct consumer需要的最小字段；review transcript与 gate evidence
   保持 task-local private。
5. Canonical package、installed package、四平台 Skill copy、workflow、runtime、preset 与
   docs 使用同一 active closure定义。
6. 不修改 upstream-owned check/review agent。独立 reviewer prompt由新 package提供。
7. planned #116 的 bridge 只保留 producer seed，不预先拥有 target schema或 authoring。

## 2. 所有权与修改面

| Owner | Canonical path | 职责 |
| --- | --- | --- |
| Skill package | `trellis/skills/guru-team/packages/guru-review-branch/` | `SKILL.md`、contract、Interface、schemas、examples、wrapper、evals、tests |
| Skill registry | `trellis/skills/guru-team/registry.json` | `guru-review-branch` active entry，`guru-review-task-publication` planned entry |
| Interface contract | `trellis/skills/guru-team/schemas/skill-interface-1.3.schema.json` | planned consumer seed与通用 routing identity约束 |
| Production migration | `trellis/skills/guru-team/migrations/production-minimal-handoff.json` | 保持 3-Skill/11-exit集合，切换 committed consumer/projection并登记第4条 authoring-seed edge |
| Shared runtime | `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` | recorder、checker、public dispatch、contract/source/installed validation |
| Workflow | `trellis/workflows/guru-team/workflow.md` | 一个 invoke、四个 exits、两个 workflow routers、一个 planned Skill consumer、一个 stop |
| Extension | `trellis/guru-team-extension.json` | commands、managed assets、active/public/private schema inventories |
| Preset | `trellis/presets/guru-team/` | canonical install、selected-platform distribution、throwaway/update/reapply validation |
| Durable docs | `.trellis/spec/`、`docs/requirements/`、三份 README | 长期 Skill、workflow、data、script、quality、install合同 |

Installed `.trellis/guru-team/skills/`、`.agents/skills/`、`.codex/skills/`、
`.claude/skills/`、`.cursor/skills/` 由 preset canonical source生成。

明确禁止修改：

- `.trellis/agents/check.md`
- `trellis/presets/guru-team/overlays/.trellis/agents/check.md`
- `.agents/skills/trellis-check/`
- `.codex/agents/trellis-check.toml`
- `.claude/agents/trellis-check.md`
- `.cursor/agents/trellis-check.md`

## 3. Skill Interface 1.3

### 3.1 Input profile

唯一 structured profile：

```json
{
  "profile": "branch_review",
  "mode": "workflow",
  "task_ref": ".trellis/tasks/07-23-131-guru-review-branch",
  "base_ref": "main",
  "committed_head": "0123456789abcdef0123456789abcdef01234567",
  "review_intent": "initial_review"
}
```

Required fields固定为：

```text
profile
mode
task_ref
base_ref
committed_head
review_intent
```

枚举：

- `mode`：`workflow`、`standalone`
- `review_intent`：`initial_review`、`finding_fix_review`、
  `fresh_final_review`

`task_ref` 是唯一 private evidence discovery locator。`base_ref` 与
`committed_head` 是 producer提供的 public identity/freshness seed。

### 3.2 Producer authoring seed

`guru-create-task-commit:committed` 到本 profile 的 target-owned合同：

| Partition | Fields |
| --- | --- |
| `seed_fields` | `task_ref`、`base_ref`、`committed_head` |
| `authoring_fields` | `profile`、`mode`、`review_intent` |

Producer projection只读取 public output，忽略 producer `exit_id` routing identity，
不读取 commit private artifact。Caller AI fresh编写 authoring fields。Runtime执行
no-overwrite merge后验证完整 input schema。

### 3.3 Public outputs

```text
passed:
  exit_id, task_ref, reviewed_head, review_ref

implementation_required:
  exit_id, task_ref, reviewed_head, finding_refs

scope_confirmation_required:
  exit_id, task_ref, proposal_refs

blocked:
  exit_id
```

约束：

- 每个 exit有独立 schema、完整 example、唯一 consumer input与唯一 projection。
- `exit_id` 是 routing identity，无需进入 non-stop consumer payload。
- 除 `exit_id` 外，任何未被 projection消费的字段均使 activation失败。
- `review_ref` 是 #116 后续实际校验的 opaque current token，不承载 narrative或 digest
  bundle。
- `finding_refs` 与 `proposal_refs` 只携带 stable ids；完整内容由 owner runtime按
  `task_ref` 读取 private gate evidence。

## 4. Planned #116 compatibility bridge

### 4.1 问题

Interface 1.3 当前接受 exit consumer引用 planned registry id，但 `consumer_inputs`
要求 exact-reference active target Interface。#116 依赖 #131，且 #116 明确独占自己的
input schema与 authoring partition。若 #131 创建 #116 schema会越权；若省略 consumer
contract则 #131 无法 active。

### 4.2 Additive contract

新增 `planned_skill_input_seed`：

```json
{
  "kind": "planned_skill_input_seed",
  "seed_fields": [
    "task_ref",
    "reviewed_head",
    "review_ref"
  ]
}
```

Validator规则：

1. Consumer identity必须为 `kind=skill`。
2. Registry target必须精确为 `state=planned`。
3. Contract不得包含 `interface_path`、`profile_id`、`authoring_fields`、
   `authoring_example`、schema path或 private locator。
4. `seed_fields` 必须非空、唯一，且 projection精确消费 output中除 `exit_id` 外的全部字段。
5. Output example projection只验证 seed shape和 producer field schemas；不声称已通过未来
   target schema。
6. Runtime遇到 planned target必须返回 missing-Skill blocked，不调用、不 fallback到
   workflow、不推断 authoring。
7. Target激活时，该 bridge必须替换为 target-owned `skill_input` 或
   `skill_input_authoring_seed`，并对 target schema执行完整 compatibility proof。

### 4.3 Routing identity通用化

把当前仅为 `branch-review-or-finding-closure` 编码的 `exit_id` omission例外替换为：

- output schema必须 require exact matching `exit_id const`；
- projection无需携带 `exit_id`；
- `exit_id` 之外的 output properties必须全部被消费；
- zero-payload stop仍要求 output只有 `exit_id` 且 empty select；
- consumer input若显式 require `exit_id`，projection必须提供它。

该规则禁止省略业务字段，也不新增 projection operation。

## 5. Entry preconditions

Workflow与 standalone使用相同 ordered preconditions：

1. `runtime_dependency`
2. `workspace_boundary`
3. `task_identity`
4. `commit_handoff`
5. `planning_approval`
6. `phase2_check`
7. `issue_scope_ledger`
8. `docs_ssot_outcome`
9. `review_range`
10. `working_tree`
11. `reviewer_assignment`
12. `review_evidence`
13. `invocation_freshness`

关键绑定：

- `task_ref` 必须解析为 current task worktree内的 active task。
- `base_ref` 必须与 intake及 task记录的 base branch一致。
- `committed_head` 必须与 current HEAD一致，并解析为 commit。
- Review range固定为 `origin/<base_ref>...<committed_head>`。
- Planning与 Phase 2使用现有 post-commit audit语义，不能覆盖未审 non-metadata tail。
- Working tree仅接受 owner contract列出的 task-local review metadata；source、spec、
  docs、tests、config、preset、overlay、CI/CD、container、K8s、migration、Makefile dirty
  path全部阻塞。
- Assignment与 raw reports必须位于 current task，所有 digests/current HEAD/lifecycle
  关系必须有效。

## 6. Semantic closed loop

### 6.1 Forward behavior

1. Validate public input与 13 个 entry preconditions。
2. 生成独立 reviewer handoff，明确 task、range、requirements、approved planning、
   Docs SSOT outcome、Phase 2与禁止读取 private runtime source的边界。
3. Dispatch未修改的 check/review agent。
4. 保存 raw Markdown report，记录 agent assignment与 liveness evidence。
5. AI读取 raw report并形成 candidates。

### 6.2 Qualification gate

每个 candidate生成互斥 disposition：

```text
qualified_finding
scope_proposal
observation
followup_candidate
rejected_candidate
```

`qualified_finding` 必须包含：

- `finding_ref`
- affected behavior/path/evidence
- requirement refs
- scope basis
- scenario class
- qualification reason
- P0-P3 severity
- owner round
- reviewed HEAD
- closure state

`scope_proposal` 的 scenario class固定为 `unconfirmed_nonstandard_proposal`，包含 `proposal_ref`、
exact proposal、trigger evidence与 clarification route，不含 severity。

`observation`、`followup_candidate` 不进入 gate-blocking findings。

### 6.3 Finding route

存在 qualified finding：

1. AI形成 `implementation_required`。
2. Recorder写 current failed review evidence。
3. Validator检查 finding refs、current round与 reviewed HEAD。
4. Workflow router返回 implementation。
5. Fix后 mandatory经过 `guru-check-task` 与 `guru-create-task-commit`。
6. 新 commit以 `review_intent=finding_fix_review` 重新进入本 Skill。

### 6.4 Scope proposal route

不存在 qualified finding但存在 scope proposal：

1. AI形成 `scope_confirmation_required`。
2. Workflow router只消费 `exit_id`、`task_ref`、`proposal_refs`。
3. Caller AI fresh-read live issue、task、ledger、proposal与 context。
4. Caller AI完整编写 existing
   `guru-clarify-requirements:active_task_scope_change` input。
5. Clarification完成后从 current authority重新进入 planning/implementation/review chain。

### 6.5 Closure与 final review

- Finding owner round必须有同 agent closure、fresh different-agent closure或完整 replacement
  chain。
- Closure agent只验证 finding已关闭，不获得 final-pass资格。
- 全部 owners关闭后，dispatch新的 `最终放行审查代理`。
- Final round必须为最后一轮，reviewed HEAD与 current HEAD一致，range覆盖完整 final diff，
  findings count为零，technical agent id未出现在前序 round。
- AI审查 Docs SSOT、deployment/safety、unverified items、observations与 follow-up candidates，
  再形成 final conclusion。

## 7. Artifact model

### 7.1 复用 artifact

| Artifact | Kind | Owner |
| --- | --- | --- |
| `agent-assignment.json` | runtime checkpoint | reviewer assignment、liveness、reuse、replacement、round identity |
| `reviews/*.md` | gate evidence | 每轮 raw human-readable review |
| `review.md` | gate evidence | 全部 rounds、finding lifecycle、final conclusion rollup |
| `review-gate.json` | gate evidence | AI-reviewed conclusion与 deterministic binding |

不新增 `branch-review-result.json`、`finding-qualification.json` 或第二个 pass artifact。

### 7.2 `review-gate.json` 演进

在现有 gate中增加 closed qualification/lifecycle结构，保留 finish/publication consumer
当前需要的 reviewed range、HEAD、review report与 assignment digests。Schema明确分层：

- AI-owned：candidate qualification、findings、scope proposals、observations、
  follow-up candidates、unverified items、Docs SSOT判断、deployment/safety判断、
  final conclusion、route。
- Deterministic：task/base/head/range、file digests、round report digests、assignment摘要、
  working tree snapshot、artifact schema/version与 freshness。

Recorder只接受已完成的 AI review payload。Validator不生成或修订 semantic内容。

## 8. Runtime与 wrapper

### 8.1 Runtime commands

新 package wrappers调用 shared dispatcher，runtime复用并收敛现有能力：

- review candidate/private input materialization
- `record-review-branch-result`
- `check-review-branch-result`
- public `invoke-stage0-skill`/`run-skill-command` dispatch

现有 `review-branch` 与 `check-review-gate` CLI保持 compatibility，内部委托同一 owner
recorder/checker，不保留第二套 semantic path。

### 8.2 Deterministic职责

Runtime职责：

- 解析 task/base/head/range；
- 读取 Git status、artifact、schema与 file digest；
- 校验 report path、round、lifecycle、HEAD、range、freshness；
- 记录 AI提供的 candidate dispositions与 conclusion；
- 从 checker-passed actual exit投影 public DTO。

Runtime不能：

- 判定 candidate scenario class；
- 绑定 requirement是否充分；
- 分配 severity；
- 决定 observation、follow-up或 scope proposal；
- 决定 reviewer是否充分；
- 决定 pass、route或 confirmation。

### 8.3 Public invocation

Wrapper流程：

1. Validate selected input profile。
2. Resolve task-local owner result locator。
3. Require checker-passed current owner result。
4. Read actual `typed_exit`。
5. Select matching output schema。
6. Project minimal DTO。
7. Serialize one JSON object to stdout。

Invocation error使用独立 closed schema。`expected_exit` 不能进入步骤1-6。

## 9. Workflow收敛

Phase 3.5替换为：

```markdown
<!-- guru-skill-invoke: {"skill":"guru-review-branch","required":true} -->
<!-- guru-skill-exit: {"skill":"guru-review-branch","exit":"passed","consumer":{"kind":"skill","id":"guru-review-task-publication"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-branch","exit":"implementation_required","consumer":{"kind":"workflow","id":"guru-branch-review-implementation-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-branch","exit":"scope_confirmation_required","consumer":{"kind":"workflow","id":"guru-branch-review-scope-router"}} -->
<!-- guru-skill-exit: {"skill":"guru-review-branch","exit":"blocked","consumer":{"kind":"stop","id":"branch-review-blocked"}} -->
```

Workflow只说明：

- 何时 mandatory invoke；
- 每个 exit进入哪个唯一 consumer；
- routers如何重新进入已有 phase；
- planned target缺失、unknown/multiple/unmapped/mismatch均 fail closed。

Package内部 review dimensions、qualification、round lifecycle、recorder/checker参数不再
复制到 workflow。

## 10. Eval与测试设计

### 10.1 Canonical corpus

Canonical corpus固定包含：

| Case | Mode/intent | Expected exit |
| --- | --- | --- |
| `passed-workflow-initial` | workflow / initial_review | passed |
| `passed-standalone-initial` | standalone / initial_review | passed |
| `implementation-required-finding` | workflow / initial_review | implementation_required |
| `scope-confirmation-required` | workflow / initial_review | scope_confirmation_required |
| `blocked-stale-evidence` | workflow / initial_review | blocked |
| `passed-finding-fix-review` | workflow / finding_fix_review | passed |
| `passed-fresh-final-review` | workflow / fresh_final_review | passed |

Semantic cases引用 repo-local checker-passed owner result。Actual exit先选 output schema，
grader再断言 expected exit。

### 10.2 Contract negative tests

- input unknown/missing/extra field
- invalid mode/review intent
- stale task/base/head/range
- public input携带 private artifact body
- candidate未 qualification即分配 severity
- proposal含 severity或自动 implementation route
- out-of-scope candidate阻塞 gate
- closure与 final reviewer角色冲突
- raw report缺失、digest mismatch、round gap、replacement chain未闭合
- planned bridge引用 active/unknown/reserved target
- planned bridge声明 target schema/profile/authoring
- routing identity之外存在 unconsumed output field
- wrapper由 expected exit驱动 route
- upstream-owned check agent发生 diff

### 10.3 Distribution tests

- source/installed contract discovery
- active registry closure从 9/35增长到 10/39
- new active Interface 1.3 row不修改 frozen Stage 0与 production migration sets
- shared/Codex/Claude/Cursor corpus byte identity与 executable mode
- preset transaction、dogfood drift、upstream ownership
- clean init、existing switch、update、reapply、零 unresolved sidecar

## 11. Compatibility与 rollback

### 11.1 Compatibility

- 现有 `review.md`、`reviews/*.md`、`review-gate.json`、
  `agent-assignment.json` path保持不变。
- 现有 CLI入口保持可用，但必须使用同一 package owner recorder/checker。
- `guru-create-task-commit:committed` DTO保持不变；只把 consumer从 workflow placeholder
  切换到 active `guru-review-branch` target profile。
- Stage 0与 production migration manifest的 Skill/exit集合及 activation identity保持不变；
  production manifest更新 committed binding并把 authoring-seed edge清单从 3 条改为 4 条。
  Live active closure按现有未来
  complete Interface 1.3 row规则派生为 10 Skills、39 exits。
- planned #116 bridge是暂态 fail-closed contract，不激活 #116。
- Issue #128 固定的 43-path historical baseline identity保持不变。五个仍 active 的
  transitional `trellis-continue` entry需要修订当前 bytes时，使用仅覆盖这五条路径的
  reviewed `current_payload_sha256` 做正常版本绑定和漂移检测；其余路径继续使用
  `baseline_sha256`。该 current binding不是 authenticity、anti-tamper或 anti-forgery
  边界，不得泛化到其它 entry，也不授权或提前执行 #132 removal。

### 11.2 Rollback

- Source contract validation失败：不运行 preset apply，修订 canonical package。
- Staged install validation失败：保留当前 installed graph，修复后整包重跑。
- Planned bridge不能证明除 `exit_id` 外的全部字段被消费：删除无 consumer字段或修订
  producer output，不创建 #116 schema。
- Existing review artifact无法兼容演进：提供 versioned reader并保持 archive只读，不新增
  平行 pass artifact。
- Independent agent evidence不可用：返回 `blocked`，不写 passing gate。
- Stable API或 requirement authority需要变化：停止实现并路由
  `guru-clarify-requirements`。

### 11.3 Unusual-scenario dispositions

| Candidate class | Trigger evidence | Disposition | Route |
| --- | --- | --- | --- |
| `security_or_threat` | Issue authority排除新威胁模型 | `out_of_scope` | 不进入实现或 finding |
| `attack_or_malicious_actor` | Issue authority排除恶意伪造 | `out_of_scope` | 不增加 anti-forgery机制 |
| `toctou_or_concurrency_race` | Issue authority排除未要求的竞态、锁、TOCTOU | `mechanism_removed` | 删除非必要机制 |
| `fault_injection_or_crash_consistency` | Issue authority排除额外 fault injection与 crash consistency | `out_of_scope` | 不进入验收 |
| `cross_os_atomicity` | Issue authority排除跨 OS原子性 | `out_of_scope` | 不进入实现 |
| `other_nonstandard` | 无 current authority trigger | `out_of_scope` | 未来 exact authority后另立 scope |

本规划没有 `approved_scope_expansion`。planned bridge、routing identity通用化、单 profile、
router ids与 artifact schema演进均为满足 explicit requirements的必要实现选择，不改变产品
或风险范围。

## 12. Docs SSOT Plan

### 12.1 Docs state

`complete_docs`。当前 durable authority：

- `.trellis/spec/workflow/skill-package-contract.md`
- `.trellis/spec/workflow/workflow-contract.md`
- `.trellis/spec/workflow/companion-scripts.md`
- `.trellis/spec/workflow/data-contracts.md`
- `.trellis/spec/workflow/quality-guidelines.md`
- `.trellis/spec/preset/installer.md`
- `.trellis/spec/preset/overlay-guidelines.md`
- `.trellis/spec/preset/upstream-ownership.md`
- `.trellis/spec/docs/public-docs.md`
- `docs/requirements/README.md`
- `docs/requirements/requirement-main.md`
- `docs/requirements/guru-team-trellis-flow.md`
- `README.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`

### 12.2 Strategy

Strategy：`ssot_first`。先在 durable specs定义 Skill ownership、planned bridge、
routing identity、review artifact、workflow route、script boundary、distribution与
upgrade合同，再实现 package/runtime。

### 12.3 Task delta merge checkpoint

Implementation完成 Interface fields、qualification schema、runtime commands、workflow
routers、eval corpus与 install/update tests后，implementation agent必须把最终 field ids、
schema ids、runtime commands、validation commands、compatibility结论合并到 12.1 的
durable docs。若某个列出文档无 semantic delta，implementation handoff必须记录检查证据与
no-change理由。

### 12.4 Task-history-only content

Intake digests、Phase 0 artifacts、planning approval、agent liveness事件、raw command
output、review rounds、PR readiness只保留在 task artifacts，不进入 durable SSOT。

### 12.5 Reconciliation evidence

Implementation handoff必须列出：

- strategy
- updated durable paths
- task delta merge结果
- task-history-only内容
- no-change或 follow-up结论
- durable-doc inputs与 task-delta inputs

Phase 2逐项复核，缺失或冲突返回 `implementation_required`。

## 13. Provenance matrix

| ID | Planning statement | Classification | Authority | Reason |
| --- | --- | --- | --- | --- |
| P1 | 新增 `guru-review-branch` semantic closed-loop Skill | `explicit_requirement` | #131 定位与 Closed Loop | 直接要求 |
| P2 | Input固定 #146 seed加 caller mode/review intent | `explicit_requirement` | #131 accepted_current | 直接要求 target-owned profile |
| P3 | 完整 entry evidence与 full branch range | `explicit_requirement` | #131 Entry Preconditions | 直接要求 |
| P4 | 未修改 upstream independent reviewer | `explicit_requirement` | #131 Trellis upstream边界 | 直接要求 |
| P5 | Qualification先于 severity，五类 scenario互斥 | `explicit_requirement` | #131 Finding qualification | 直接要求 |
| P6 | Finding closure后 fresh final review | `explicit_requirement` | #131 Closed Loop与 AC | 直接要求 |
| P7 | 四个 `exit_id` outputs与最小 DTO | `explicit_requirement` | #131 accepted_current及 2026-07-20 I/O修订 | 直接要求 |
| P8 | `passed` 只提供 #116 三字段 seed | `explicit_requirement` | #116/#131 accepted_current | 直接要求 consumer边界 |
| P9 | 复用四类 Branch Review artifacts | `explicit_requirement` | #131 Artifact | 直接要求 |
| P10 | Real-wrapper corpus与四平台 byte identity | `explicit_requirement` | #131 accepted_current | 直接要求 |
| P11 | Workflow收敛为 invoke与 routes | `explicit_requirement` | #131 Acceptance Criteria | 直接要求 |
| P12 | Clean install/update/reapply/dogfood | `explicit_requirement` | #131 Acceptance Criteria与 AGENTS.md | 直接要求 |
| P12A | Production manifest同步 committed binding与第4条 authoring-seed edge | `explicit_requirement` | #131 accepted_current producer-to-consumer projection | 直接要求，保持 #146 Skill/exit集合不变 |
| P13 | planned consumer seed bridge | `necessary_implementation_choice` | P8加当前 Interface 1.3 gap | 备选为越权定义 #116 schema或无法激活 #131；选定方案保持 target ownership与 fail-closed |
| P14 | 通用 routing identity omission | `necessary_implementation_choice` | P7、P8加 current validator特例 | 备选为把 `exit_id`塞入 #116 seed；选定方案保留 fixed seed且只豁免 discriminator |
| P15 | 单 `branch_review` profile加 intent枚举 | `necessary_implementation_choice` | P2、production corpus范围 | 备选为三个重复 profiles；选定方案没有结构差异且保持最小 public surface |
| P16 | Scope与 implementation使用 workflow routers | `necessary_implementation_choice` | P5、P6与 current clarification input ownership | 备选为扩大 DTO或新增 semantic reconstruction；router保持 caller AI fresh authoring |
| P17 | Docs采用 `ssot_first` | `necessary_implementation_choice` | R11与公共合同变更 | 备选为 task-only delta；选定方案避免 package/runtime/docs漂移 |
| P18 | 保留 issue #128 historical baseline，并为五个 active continue entry增加窄 current payload binding | `necessary_implementation_choice` | R11、AC15与 issue #128 immutable ownership baseline | 备选为伪造/重置历史 baseline或提前执行 #132 removal；选定方案只绑定五条当前 bytes，保持历史身份与 follow-up边界 |

P13-P18 的 product scope expansion与 risk scope expansion均为 `false`。本规划无
`approved_scope_expansion`，无待确认 unusual proposal。
