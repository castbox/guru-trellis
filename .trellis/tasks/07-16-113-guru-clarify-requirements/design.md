# #113 技术设计：guru-clarify-requirements

## 1. 设计结论

采用“semantic Skill 拥有 clarification state machine与确认后的 GitHub action，recorder/checker只记录与验证事实，global workflow只路由 exits”的三层结构：

```text
context evidence / explicit standalone target / active-task scope proposal
  -> guru-clarify-requirements semantic loop
  -> AI Review Gate
  -> exact human confirmation when action requires mutation or scope inclusion
  -> existing GitHub connector / reviewed gh command when applicable
  -> live source/task evidence refresh
  -> stdout result recorder + checker
  -> one typed exit
```

本任务不新增 repo-level clarification artifact。Initial/standalone result 通过 stdout digest 交给后续 consumer；active-task invocation 直接更新当前 task 的 GitHub authority、ledger、planning 和 review evidence，并在 result 中绑定这些 evidence 的 content hash。

## 2. SSOT 与 ownership

| 层 | SSOT | 本任务责任 |
| --- | --- | --- |
| Global routing | `trellis/workflows/guru-team/workflow.md` | Mandatory invocation、typed exit consumer、fail-closed stop |
| Step-local semantics | `trellis/skills/guru-team/packages/guru-clarify-requirements/` | Inputs、question loop、AI Gate、confirmation、mutation sequencing、freshness、exits |
| Deterministic runtime | `trellis/workflows/guru-team/scripts/` | Record、schema/digest/live validation；不执行 mutation |
| Distribution | `trellis/skills/guru-team/registry.json` 与 preset installer | Canonical package、installed registry、platform discovery copies、managed hashes |
| Durable contracts | `.trellis/spec/**` 与 `docs/requirements/**` | 长期行为、data contract、upgrade/update、public authoring rules |
| Public guidance | `README.md`、workflow README、preset README | 安装、daily route、standalone、validation 与 migration 状态 |

`trellis-brainstorm` 只提供问答方法，不拥有 #113 的 question selection、closure、source action 或 typed exit。#113 不修改该 upstream-owned Skill。

## 3. Package 布局

```text
trellis/skills/guru-team/packages/guru-clarify-requirements/
  SKILL.md
  interface.json
  references/contract.md
  schemas/requirements-clarification.schema.json
  examples/requirements-clarification.json
  scripts/record-requirements-clarification.sh
  scripts/check-requirements-clarification.sh
  tests/test_contract.py
```

两个 package scripts 必须保持 dispatcher-only。Shared Bash wrappers 与 Python subcommands 使用相同 command ids：

- `record-requirements-clarification`
- `check-requirements-clarification`

Artifact schema id 固定为 `guru-requirements-clarification-1.0`。Extension interface schema 保持 `guru-team-skill-interface-1.2`；本任务不改变通用 interface shape。

## 4. Modes 与 entry preconditions

两种 mode 的 `entry_precondition_ids` 完全一致：

1. `runtime_dependency`：完整 Guru Team preset、installed manifest、dispatcher、managed package inventory current。
2. `invocation_context`：`initial_intake`、`active_task_scope_change` 或 `explicit_review` 三选一。
3. `review_target`：existing issue、proposed draft、active task scope 或 standalone request 的 portable identity。
4. `context_availability`：current #111 snapshot reference、明确 missing evidence codes 或 standalone caller supplied evidence。
5. `source_authority`：current issue/draft/task scope content hashes与 mutation preimage。
6. `evidence_freshness`：question state、action digest、confirmation digest、mutation result、scope/content/result digest current。

缺 context 是合法输入状态，用于产生 `needs_context`；不得把它建模为 package invocation failure。Runtime dependency、target identity 或 closed payload shape 无效才属于 fail-closed invocation failure。

## 5. Clarification state machine

### 5.1 状态

```text
classified
  -> evidence_research
  -> questioning
  -> converged
  -> action_reviewed
  -> confirmation_pending | confirmation_not_required
  -> mutation_observed | no_mutation
  -> refreshed
  -> recorded
  -> validated
  -> typed_exit
```

### 5.2 Question model

`clarification_rounds[]` 每项包含：

- `round_id`
- `question_id`
- `question_kind`: `single` 或 `atomic_group`
- `question_text`
- `atomicity_reason`: `atomic_group` 必填，`single` 必须为 null
- `category`: `product_intent` 或 `scope_risk_decision`
- `answer_summary`
- `answer_status`: `complete`、`partial`、`refused`
- `affected_contracts[]`
- `opened_question_ids[]`
- `closed_question_ids[]`

同一 round 只能有一个 `question_id`。`partial` 不得关闭自身或其它 load-bearing question。`repository_answerable_questions[]` 必须在第一轮用户问题前全部处于 `answered` 或 `not_answerable`；`not_answerable` 必须携带已检查 evidence refs 与缺失原因。

### 5.3 Convergence rule

`clear` 当且仅当：

- `open_questions=[]`
- `ai_review_gate.status=passed`
- source authority current
- 所有 accepted scope proposals 已获得 exact confirmation
- 所有 rejected/deferred proposals 已进入 related/followup/new task/out-of-scope
- action 为 `none` 且无需 refresh，或 active caller 的 current evidence 已经由完整 refresh 证明

Mutation 成功后 initial workflow 返回 `refresh_context`，不得直接返回 `clear`。

## 6. Scope proposal 与 active-task gate

`scope_proposals[]` 使用 closed shape：

- `proposal_id`
- `scenario`
- `trigger_evidence[]`
- `proposed_contracts[]`
- `cost`
- `alternatives[]`
- `consequence_if_omitted`
- `origin_requirement_status`: `explicit`、`necessary_correctness`、`confirmed_expansion`、`unconfirmed_expansion`
- `optional_mechanism_origin`: boolean
- `decision`: `pending`、`accepted_current`、`related`、`followup`、`new_task`、`out_of_scope`、`mechanism_removed`、`mechanism_replaced`
- `proposal_digest`
- `confirmation_ref`

`unconfirmed_expansion + accepted_current` 必须携带 proposal-digest-bound `confirmation_ref`。普通 continuation/task/planning/review confirmation 的 action kind 不匹配时 validator 必须拒绝。`optional_mechanism_origin=true` 时不得使用 `accepted_current`；只能删除、替换或把独立业务价值交由新 proposal 重新确认。

Active-task current inclusion 必须绑定：

- GitHub comment/body evidence URL与 content facts
- `issue-scope-ledger.json` content SHA-256 和 classification delta
- `prd.md`、`design.md`、`implement.md` content SHA-256
- stale planning approval/Phase 2/Branch Review identities
- required re-entry owners：`guru-approve-task-plan`、`guru-check-task`、`guru-review-branch`

本任务不实现后三个 Skill；只记录 required re-entry contract。

## 7. Source-of-truth action model

`source_actions[]` 以数组表达 GitHub mutation 与 task-local updates 的组合；每项 action 必须有唯一 kind、target、exact payload/content digest、preimage digest、status 与 mutation evidence。

| Action | Side effect | Executor |
| --- | --- | --- |
| `none` | 无 | 不调用 executor |
| `issue_comment` | GitHub comment | AI在exact confirmation后调用现有GitHub connector或审查过的`gh issue comment` |
| `issue_body_edit` | GitHub body edit | AI在exact confirmation后调用现有GitHub connector或审查过的`gh issue edit` |
| `proposed_draft_update` | 无 repo/GitHub write | AI 更新 in-memory reviewed draft，recorder 绑定 hash |
| `new_issue_draft` | 无 issue creation | AI 形成 reviewed draft，返回 `new_task` |
| `active_task_scope_update` | 当前 task-local ledger/planning/review write | AI 按已确认 payload编辑；checker 验证 exact paths/hashes |

### 7.1 Confirmation

`human_confirmation` 使用：

- `status`: `not_required`、`confirmed`、`refused`
- `action_digest`
- `proposal_digests[]`
- `confirmed_actions[]`
- `confirmer`
- `confirmed_at`
- `evidence_summary`

AI 必须在 mutation 前重读 live preimage；target repo/issue、action digest或confirmation digest任一不匹配时停止且不得调用 GitHub write。

### 7.2 Mutation execution boundary

Skill 对 `issue_comment` 或 `issue_body_edit` 执行以下顺序：

1. AI审查 source action closed shape、target repo/issue、preimage、confirmation与 exact payload digest。
2. 读取 live issue facts；preimage不一致时返回 `refresh_context`，不得执行 mutation。
3. AI执行已展示并确认的GitHub connector action或exact `gh issue comment` / `gh issue edit --body-file`命令。
4. 重读 live issue/comment facts。
5. Recorder记录 URL、state、updated_at、body/content hash、action digest与 facts digest；checker重新验证。

本 Skill 不执行 new issue creation；真正 issue 创建属于 #112。

## 8. Result schema

Top-level closed fields：

- `schema_version`
- `skill_id`
- `generated_at`
- `mode`
- `typed_exit`
- `invocation_context`
- `review_target`
- `context_evidence`
- `confirmed_facts`
- `repository_answerable_questions`
- `clarification_rounds`
- `open_questions`
- `scope_proposals`
- `source_actions`
- `human_confirmation`
- `mutation_results`
- `active_task_evidence`
- `ai_review_gate`
- `affected_contracts`
- `content_identity`
- `reason`
- `consumer`
- `error`

`content_identity` 必须包含 target/content/context/scope/action/payload/result SHA-256。Recorder 计算 derived digests；checker 重新计算并验证 live GitHub 与 task-local paths。Schema、pure validator 和 live validator必须分层，任何 script pass 都不得生成 semantic `clear`。

## 9. Typed exit mapping 与 staged migration

### 9.1 #113 merge 时

- 把 `guru-discover-change-context:context_ready` consumer 从 workflow placeholder 改为 active Skill `guru-clarify-requirements`。
- 新增 #113 mandatory invocation marker。
- `clear` -> workflow target `guru-requirements-clear-router`。Router 只验证 caller-aware `resume_target`，不执行新的语义判断：initial issue/draft进入 staged `guru-review-contract-wording` target，standalone返回 caller，accepted-current active scope进入 planning review，non-current active classification恢复 exact interrupted progression。
- `needs_context` -> active Skill `guru-discover-change-context`。
- `refresh_context` -> active Skill `guru-sync-base`。
- `new_task` -> workflow target `guru-full-task-intake-chain`。
- `blocked` -> stop target `requirements-clarification-blocked`。

### 9.2 后续迁移

#114 激活时只把 `guru-requirements-clear-router` 的 initial issue/draft downstream 从 staged workflow target切换为 active Skill `guru-review-contract-wording`；public `clear` consumer保持 `guru-requirements-clear-router` 不变。仅当 placeholder target 已无任何 consumer 时才删除。#112 最终集成完整 Intake chain。#113 不预先实现 #114/#112 内部步骤。

## 10. Runtime 与测试结构

### 10.1 Python runtime

在 shared runtime 增加 pure helpers、schema loader、live issue fact reader、recorder、checker和parser dispatch。Canonical workflow runtime与preset分发 runtime必须保持字节同步。Runtime不得调用GitHub write。

### 10.2 Test matrix

1. Package contract：frontmatter、modes parity、stages、commands、schema、exits、consumers。
2. Pure schema：closed fields、digest、question round、partial answer、scope proposal、confirmation与 exit invariants。
3. Initial intake：existing issue clear、comment、body edit、draft update、new issue draft。
4. Context routes：needs context、stale context、mutation refresh、blocked conflict。
5. Active task：current/related/followup/new task/out-of-scope、planning/ledger/review hashes与 stale downstream gates。
6. #127 proposal：exact confirmation、generic confirmation rejection、refusal/defer continuation、optional mechanism removal/replacement。
7. Mutation evidence：preimage mismatch禁止write、comment/body exact confirmation、post-mutation reread与facts binding。
8. Distribution：registry、manifest、managed inventory、selected/unselected platforms、non-portable wrapper。
9. Throwaway：initial apply、standalone invocation、`trellis update`、workflow switch/reapply、all-platform discovery、dogfood drift、recursive sidecar check。

Tests只覆盖需求声明的正常路径与常见 correctness边界，不增加恶意 actor、并发 race、fault injection或跨 OS 原子性矩阵。

### 10.3 Branch Review F-001 范围决策

2026-07-16 用户确认 F-001 为 `out-of-scope`，GitHub-visible 决策固定在 [issue comment](https://github.com/castbox/guru-trellis/issues/113#issuecomment-4990373622)。Pre-task/standalone caller 恶意伪造无法解引用的 draft/context hash 不属于 #113 的威胁模型，因此不新增仅为该场景服务的 embedded draft body、portable context content 或 evidence locator 合同，也不把对应恶意输入负例作为 acceptance。

该排除不改变正常 correctness 边界：F-002 的 question lifecycle、F-003 的 confirmed payload/live mutation 一致性、F-004 的 active-task mandatory invocation 与 caller-aware resume、F-005 的 repository answer evidence、F-006 的 ownership facts 与完整 discovery 都保留。实现修订必须撤回仅属于 F-001 的 package/schema/runtime/example/test/docs delta，同时维持既有 evidence-first 与缺 context 返回 `needs_context` 的语义。

## 11. Docs SSOT Plan

- `docs_state`: `partial_docs`
- `strategy`: `ssot_first`
- Evidence paths：`.trellis/spec/workflow/{workflow-contract,skill-package-contract,companion-scripts,data-contracts,quality-guidelines}.md`、`.trellis/spec/preset/{installer,upstream-ownership}.md`、`.trellis/spec/docs/public-docs.md`、`docs/requirements/{requirement-main,guru-team-trellis-flow}.md`、三份 public README。
- Durable docs updates：补充 #113 package/state machine、result schema、mutation/confirmation、active-task scope proposal、typed exit staged migration、additive distribution与验证矩阵。
- Task artifact deltas：本设计中的 mode/precondition、question/confirmation/scope/action/result合同必须在实现 runtime 前写入 durable specs；PRD中的产品规则必须进入 durable requirements。
- Task-history-only：Phase 0 snapshot、候选筛选、规划审查、逐轮实现finding、F-001 的用户拒绝与 GitHub-visible scope decision、临时测试日志保留在当前 task artifacts。
- Merge checkpoint：实现 runtime 前完成 durable spec delta；Phase 2 final check核对 durable docs、canonical package、runtime、installed copies、public docs和tests一致。
- Follow-up boundary：#114/#101/#112 的内部合同不进入本任务 durable implementation；只记录 staged consumer关系。

## 12. Upgrade、兼容与回滚

- Extension version从 `0.6.5-guru.11` 递增到 `0.6.5-guru.12`，并同步 canonical/dogfood manifest与 public version matrix。
- `guru-clarify-requirements` 是新增 public API；stable id、exit ids、schema id与command ids merge后不得静默改义。
- Upgrade必须执行官方 `trellis update`、重新选择 marketplace workflow、preset reapply、sidecar处置、source/installed/drift/throwaway validation。
- 回滚必须回退本任务 work commit并使用前一 extension source重新 apply；不得手工删除业务 repo中的未知本地修改。
- 本任务不新增服务、数据库、容器、Kubernetes、CI/CD workflow或Makefile行为。

## 13. 安全边界

Result、日志、fixture、issue comment、task artifact与PR body不得包含 token、secret、private key、签名 URL、`.env`、数据库 URL、客户数据或本机绝对路径。Public example只使用去敏 repo、issue与payload。
