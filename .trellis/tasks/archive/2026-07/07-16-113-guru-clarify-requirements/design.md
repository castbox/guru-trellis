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

1. `runtime_dependency`：evidence 是 installed extension manifest、dispatcher、active package inventory 与已声明的 record/check runtime commands；绑定完整且兼容的 Guru Team preset runtime；每次 runtime command 前由 `run-skill-command` 验证 freshness。
2. `review_target`：evidence 是一个 current GitHub issue 或 side-effect-free proposed draft identity；绑定 AI 实际审查的 exact requirements authority；record/check 全程要求 target facts 与 content digest 不变。
3. `context_evidence`：evidence 是 current `guru-context-discovery-1.0` snapshot 或明确的 missing/stale evidence；绑定 repository、current/history evidence 与 load-bearing decisions；`clear` 前重新验证 current evidence，缺失时返回 `needs_context`。
4. `source_authority`：evidence 是 live issue/draft facts，以及适用时 exact source-action preimage 与 post-mutation facts；绑定 future intake 将读取的 issue 或 draft；AI 在 mutation 前立即重读，checker 重读已声明的 live facts。
5. `invocation_freshness`：evidence 是 mode、invocation kind、caller-aware resume target、target/context/scope/action/payload/result digests 与 active-task bindings；绑定一个 current semantic review round 及其合法 continuation；typed-exit validation 时所有 identity 必须仍然匹配。

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
- `atomic_group_id`
- `atomic_group_reason`
- `category`: `product_intent` 或 `scope_risk_decision`
- `question`
- `answer_summary`
- `answer_status`: `complete`、`partial`、`refused`
- `affected_contracts`
- `opened_question_ids`
- `closed_question_ids`

Closed schema 不定义额外的 single/atomic-group discriminator：普通单题使用 `atomic_group_id=null` 且 `atomic_group_reason=null`；只有不可拆分的 product choice 才使用非 null `atomic_group_id`，并同时提供非空的 `atomic_group_reason`。同一 round 仍只有一个 `question_id`，`question` 承载问题正文。`partial` 不得关闭自身或其它 load-bearing question。`repository_answerable_questions[]` 必须在第一轮用户问题前全部处于 `answered` 或 `not_answerable`；`not_answerable` 必须携带已检查 evidence refs 与缺失原因。

### 5.3 Convergence rule

`clear` 当且仅当：

- `open_questions=[]`
- `ai_review_gate.status=passed`
- source authority current
- `active_task_scope_change` 的 `scope_proposals[]` 包含一个或多个 terminal proposal；`clear/new_task` 不得以空数组表示“无变化”，`new_task` 必须含 `decision=new_task`
- 所有五类 scope classification proposal 已获得 proposal-digest-bound exact 用户决策证据
- 所有 proposal 已进入 accepted-current/related/followup/new task/out-of-scope 或明确的 mechanism removed/replaced 终态
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

Active-task 的 `accepted_current`、`related`、`followup`、`new_task`、`out_of_scope` 每个 final decision 都必须携带 proposal-digest-bound `confirmation_ref`，并与 `human_confirmation` 及 structured trail 的 `user_decision` exact 匹配。普通 continuation/task/planning/review confirmation 的 action kind 不匹配时 validator 必须拒绝。`optional_mechanism_origin=true` 时不得使用 `accepted_current`；只能删除、替换或把独立业务价值交由新 proposal 重新确认。

`mechanism_removed` 与 `mechanism_replaced` 属于 terminal mechanism disposition，不属于上述五类 scope classification。两者必须满足 `optional_mechanism_origin=true`、`confirmation_ref=null`，不得进入 `decision_trail.proposal_decisions[]`，不得单独要求 GitHub-visible scope authority 或 `active_task_scope_update`。仅含一个或多个 mechanism disposition 的 payload 在全部 proposal terminal 时返回 `clear`；混合 payload 的 trail 只投影五类 scope classification proposal。`new_task` 必须含 `decision=new_task`，mechanism disposition 不能单独产生该 exit。

每个 active-task final classification 必须绑定：

- GitHub comment/body evidence URL与 content facts
- `issue-scope-ledger.json` content SHA-256、classification delta 和唯一 `scope_decisions[]` trail
- `prd.md`、`design.md`、`implement.md` content SHA-256
- 完整有效的 schema 1.2 `planning-approval.json` 和 stale planning approval/Phase 2/Branch Review identities
- 当前 Branch Review 的 `not_started/current/stale` 状态及存在时的 `review-gate.json` content SHA-256
- task update 前 context digest、GitHub authority `updated_at` 与 exact interrupted resume target
- required re-entry owners：`guru-approve-task-plan`、`guru-check-task`、`guru-review-branch`

本任务不实现后三个 Skill；只记录 required re-entry contract。

### 6.1 Structured decision trail

`issue-scope-ledger.json` 在既有 `primary_issue`、`close_issues`、`related_issues`、`followup_issues` 之外增加 `scope_decisions[]`。每项内容必须与 result 的 `active_task_evidence.decision_trail` 一致，并包含：

- `trail_id`
- 一个或多个 `proposal_decisions[]`，每项记录 `proposal_id`、`proposal_digest`、final `decision` 与 `confirmation_ref`
- `user_decision`，记录 exact proposal digests、confirmer、confirmed_at 与 evidence summary
- `github_authority`，记录 live `issue_comment` 或 `issue_body` URL、content SHA-256 与 `updated_at`
- `context_before_task_update_sha256`
- 三份 `planning_documents` file evidence
- `stale_downstream_evidence`
- `review_evidence`
- 三个 `reentry_owners`
- `interrupted_resume_target`

同一 `trail_id` 必须在 ledger 中唯一。Active-task invocation 若五类 scope classification proposal 缺少 trail、trail 与分类 proposal 投影不一致、用户证据不一致、GitHub authority 不可 live 重读、planning/review evidence 不完整或 re-entry 尚未完成，checker 必须失败并阻塞。仅含 `mechanism_removed/replaced` 的 payload 不创建 trail。

### 6.2 Planning approval 与 re-entry

Active-task evidence 校验必须调用 shared runtime 的 `validate_planning_approval(root, task_dir)` 或语义完全相同的单一 helper，并要求返回零错误。该验证必须覆盖 schema 1.2、`user_confirmation.source=explicit-post-planning-review`、passed `ambiguity_review`、固定 `scan_scope`、完整 `hits[]`、空 `unchecked_normative_hits[]`、七个 true 审查维度、reviewed/approved artifact aliases 以及 `prd.md`、`design.md`、`implement.md` 当前 path/hash/size。`stale_downstream_evidence.planning_approval_sha256` 还必须与该完整 artifact 的当前 SHA-256 一致；只验证文件存在或 hash shape 不得通过。

Planning fixture 必须由正常 recorder 生成或构造出与正常 recorder 完全一致的 schema 1.2 artifact和非占位 planning 正文。Review 已开始时必须绑定当前 `review-gate.json` 并把状态记为 `stale`；只有该文件确实不存在时才能使用 `not_started + artifact=null`。

五类 scope classification 的 re-entry 顺序固定为：GitHub comment/body mutation 成功后本轮只能返回 `refresh_context`；context refresh 必须生成 `generated_at >= github_authority.updated_at` 的 current snapshot并重读相同 authority content；随后执行 task-local planning/ledger update，记录 `context_before_task_update_sha256`，完成 fresh schema 1.2 planning approval并把既有 Phase 2/Branch Review 标为 stale。最终 invocation 通过 live authority、context 时间、ledger exact trail、planning approval/docs、review state 与 stale gate identities证明 current 后，才能返回 `clear` 或 active-task `new_task`。Task-local update 不改变 repository/history context 时，不强制第二次 context refresh或 snapshot digest 不同。Router 随后按 trail 中的 exact interrupted target恢复，`accepted_current` 例外进入 `guru-active-task-planning-review`。

Mechanism disposition 不执行 GitHub/task authority mutation，不进入上述 refresh sequence；checker 只验证 `optional_mechanism_origin`、terminal decision、null confirmation 与不存在 classification trail/action mutation。

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
5. Active task：非空 terminal proposal set、五类 scope classification exact 用户证据、`scope_decisions[]` exact trail、mechanism removed/replaced terminal、planning/ledger/review bindings与 stale downstream gates。
6. #127 proposal：exact confirmation、generic confirmation rejection、refusal/defer continuation、optional mechanism removal/replacement。
7. Mutation evidence：preimage mismatch禁止write、comment/body exact confirmation、post-mutation reread与facts binding。
8. Distribution：registry、manifest、managed inventory、selected/unselected platforms、non-portable wrapper。
9. Throwaway：initial apply、standalone invocation、`trellis update`、workflow switch/reapply、all-platform discovery、dogfood drift、recursive sidecar check。
10. Finding regressions：空 `scope_proposals[] + action=none + empty mutations` 必须失败；active-task `mechanism_removed` 与 `mechanism_replaced` 必须通过 `clear`；两行 planning 文档、最小 planning approval JSON、五类 classification 缺失 `scope_decisions[]`、旧 review state、GitHub authority 晚于 context snapshot 或 mutation 后直接 resume 必须失败；正常 recorder 生成的 planning approval 与 authority-before-context-before-task-update re-entry 必须通过。

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
