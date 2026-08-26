# Evolution Public Contracts

状态：`design_ready_for_delivery_planning`。本文件定义 target runtime 的公共 Skill graph 与最小 handoff；它不是
current registry/interface/schema，也不授权实现。target contract identity 为
`guru-team-evolution-contract-1.0`，只通过 existing-migration 的一次原子 activation 成为 current。

## 1. Contract Set And Ownership

| Identity | Owner | Purpose |
| --- | --- | --- |
| `guru-team-evolution-contract-1.0` | Guru Team workflow | target phase graph、mandatory Skill id、typed-exit router 与 stop |
| `guru-team-evolution-skill-registry-1.0` | canonical Skill registry | target public Skill/profile/interface inventory |
| `guru-context-envelope-1.0` | invocation admission owner | 一个 invocation 的 private lazy context 与定向 freshness |
| `guru-stock-projection-policy-1.0` | `guru-maintain-stock-projection` | pinned stock inventory、selected action、provider/worker/retained binding |
| `guru-trellis-reference-manifest-1.0` | Guru preset transaction（single writer） | official-doc/local-runtime/package-snapshot locator precedence、source identity 与 lazy read-only projection；exact reference callers只读，不复制 `trellis-meta` semantic/write surface |
| `guru-code-spec-projection-1.0` | `guru-bootstrap-repository-ssot:projection_refresh` | reviewed current RDT/Architecture/code-spec contribution 到最小 `.trellis/spec` locator/usage projection 的单写入合同 |
| `guru-extension-ownership-contract-4.0` | preset transaction owner | 在不取得 upstream source ownership 的前提下，声明 exact post-projection policy claim、validator 与 migration |
| `guru-extension-activation-manifest-1.0` | preset transaction owner | workflow、registry、runtime、ownership、stock policy、worker、host projection 的同一 candidate |

保留 marketplace workflow id `guru-team` 不表示保留旧合同。旧 registry、schema、route、private
artifact consumer 与 target graph 不 dual-read；migration final validation 前没有 target consumer。

## 2. Public I/O Rule

每个 Skill 自己拥有 closed input profile。表中的字段是该 profile 的完整业务字段；`exit_id` 是
每个 output schema 的固定 discriminator，不另建一个 optional-field 总 schema。invocation-scoped Skill
仅再带 `invocation_id`、`context_revision`；task-scoped Skill 仅再带 `task_ref`。

authority/provider section owner 在同一 envelope 内完成首次 live read 与 dependency/material-change 后的
定向 refresh。适用的 repository RDT、Architecture 与 task 三文档正文按稳定 locator/identity/order形成
call-local stable authority prefix；需要这些 authority 语义的 AI owner直接消费同一bound content view，
不消费producer摘要、handoff或再次用tool全文读取。cache miss/unavailable仍构造同一prefix且不改变判断。
consumer public edge只经owner runtime取得自己的authorized minimal projection；live fact正文不进入DTO，
只有direct consumer必需的最小identity/freshness token可以进入该exit的closed output。跨turn持久envelope
不得保存全文RDT。

private `context_envelope` 不作为 public input/output。任何 output 均不得包含 envelope path/body、
authorization、完整正文、完整 finding/review history、stdout、Git snapshot、per-file hash bundle、
recorder state 或 provider secret。

Every semantic Skill that may own a side effect first resolves its current action state. A no-mutation current result
bypasses action-plan display, confirmation wait and refusal handling. Only when a real choice or side effect remains
pending does that Skill own the `EVO-REQ-081` boundary: it authors and reviews one private exact action plan, displays
the current action/target/scope/effects/preserved boundaries, and lets only the AI accept any clear dialogue-local
affirmative. It never asks the user to copy a fixed prompt/password,
hash/digest, task id/path/branch/SHA/identity/summary, prescribed wording, `确认执行 <hash>` or lexical `合并PR`.
The plan and live facts may carry deterministic freshness identities, but no public/private schema, recorder,
validator or executor parses, matches, validates or persists the user's reply or authorization status. A question,
limit, revision, partial choice, refusal or material plan/live-fact change returns to the same action owner before
mutation. Every explicit refusal selects the owning Skill's named zero-side-effect refusal output below; it is never
collapsed into a provider/contract failure. One confirmation consumes only the displayed action; READY PR merge uses
this same contract, while Issue closure, Finish/archive and Cleanup remain separate actions.

### 2.1 Input Provenance And Edge Construction

Public input contains only caller-owned intent/identity that the caller must intentionally supply. Repository,
provider, checkout, plan, RDT, Architecture, projection and live-state facts are not silently relayed through an
invocation frame and are not accepted as caller-authored fields: the exact owning Skill obtains them from its named
envelope section owner as an authorized minimal projection, validates freshness, and never rereads the same source
body. A selected exit may be projected to a consumer only by `direct|select|rename|normalize`; a projection cannot
read a producer checkpoint, an envelope file, ambient Git state or runtime source, and cannot invent a missing field.

The rows below therefore use these closed construction rules:

1. `invocation_id,context_revision` and task-scoped `task_ref` are validated common invocation bindings, not exit
   payload fields. Profile/mode constants are fixed by the declared edge.
2. Every other required consumer field either appears in the selected exit output or is removed from public input
   and resolved by that consumer's exact authority/provider owner as part of positive behavior.
3. A same-Skill wait/re-entry uses a named workflow pause carrying only its closed continuation identity; a later
   event supplies the new event or product-choice fact. The re-entry profile consumes that continuation plus only
   the new fact declared by the pause, not the original profile fields again. The exact owner uses the continuation
   to address its own state and performs the required live reread; it never treats a dialogue reply, generic frame
   or private checkpoint body as a public DTO.
4. A cross-Skill clarification may carry one caller-owned `caller_continuation_ref` only when the selected profile
   fixes that caller and its exact re-entry. Clarification and its router return the token unchanged and never open
   it; only the original caller consumes it to address and live-validate its own state.
5. No generic “current frame”, implicit pass-through, target-owned default or hidden authoring seed may fill an
   otherwise missing required field. Future implementation must validate every row's output-to-input projection
   independently before activation.

The closed profile inventory for a public Skill is the union of its primary row below, the wording/qualification
caller-return profiles in Section 3 when that Skill is a listed caller, the exact lifecycle-owner profiles in
Section 3.1, and the recoverable-block profiles in Section 7.1. No other implicit repair/resume profile exists. An
ordinary recoverable blocked output carries the
producer-owned opaque `continuation_ref` declared by Section 7.1; only that producer opens it. Wording and
qualification are the only cross-Skill exceptions: their original caller creates `caller_continuation_ref`, the
specialist and thin router return it unchanged, and only that caller opens it. Bootstrap's separate authority-caller
continuation follows its Section 4 contract. A stop may consume the row's diagnostic fields to identify the exact
blocker and required repair, but neither the stop nor a router reconstructs the original input from task state, an
envelope file, a checkpoint or ambient live state. A result explicitly marked terminal/new-invocation is not given
a continuation merely to make recovery appear closed.

## 3. Entry, Answer, Resume And Specialist Skills

| Public Skill / profiles | Mode | Minimal public input | Exit -> minimal output -> unique consumer |
| --- | --- | --- | --- |
| `guru-admit-invocation` / `user_event`, `post_owner_pending`, `post_remote_pending`, `isolation_reentry`, `binding_reentry`, `isolation_repair_reentry`, `suppression_reentry`, `provider_boundary_reentry`, `retained_context_reentry` | semantic | user event=`host_event_id,host_session_id,arrival_sequence`; post-owner=`pending_intent_ref,prior_outcome_ref`; post-remote=`pending_intent_ref,remote_outcome_ref`; progress re-entry=`pending_invocation_id,progress_event_id` from the named wait plus the new host event; every blocked repair profile=`continuation_ref,repair_input`, with the selected profile and existing envelope/receipt state fixed by that producer-owned continuation | `lifecycle_bound` -> `lifecycle_ref,current_owner_id,bound_event_ref,event_sequence` -> `guru-bound-intent-router`, where `bound_event_ref` binds the host event identity/session and current event content while `event_sequence` preserves monotonic arrival order; `request_admitted` -> `request_ref` -> `guru-route-request`; `isolation_pending` -> `pending_invocation_id,progress_handle,next_event_kind` -> `invocation-isolation-wait`, which projects only `pending_invocation_id` plus the later `progress_event_id` back to this Skill; `independent_request_isolation_blocked` -> `isolation_fact_refs,continuation_ref,repair_input` -> `independent-request-isolation-blocked`; `binding_blocked` -> `continuation_ref,repair_input` -> `invocation-binding-blocked`; `upstream_suppression_blocked` -> `asset_ref,source_identity,policy_ref,continuation_ref,repair_input` -> `stock-suppression-admission-blocked`; `provider_boundary_blocked` -> `asset_ref,binding_fact_refs,provider_contract_ref,continuation_ref,repair_input` -> `stock-provider-admission-blocked`; `retained_context_blocked` -> `handoff_refs,continuation_ref,repair_input` -> `retained-context-admission-blocked`. `post_owner_pending|post_remote_pending` allocate a new invocation/envelope/receipt before isolation; isolation progress/repair re-entry reuses the existing envelope and the one receipt. A bound event creates neither receipt nor envelope, and its owner may not recover the missing event through host history or ambient lookup |
| `guru-route-request` / `top_level` plus standalone wording/qualification caller-return profiles below | semantic | top-level=`request_ref`; specialist-return inputs use the closed shapes below | `direct_answer` -> `answer_scope_ref,answer_profile` -> exact `guru-answer-request` profile, where `answer_profile=ordinary|trellis_reference|explicit_history|explicit_diagnosis`; `new_change` -> `change_scope_ref` -> `guru-select-workflow-mode`; `resume_or_history` -> `intent_ref` -> `guru-resolve-current-work`; `distribution_or_release` -> `terminal_intent_ref,candidate_ref,target_ref` -> `guru-route-distribution`; profile-specific `specialist_review`: wording -> `specialist_profile,scope_ref,caller_continuation_ref`, qualification -> `specialist_profile,scope_ref,target_ref,candidate_refs,caller_continuation_ref`, both -> `guru-specialist-router`; `standalone_specialist_completed` -> `result_ref` -> `workflow-completed`; `stopped` -> `stop_reason_ref,unexecuted_boundary_ref` -> `workflow-completed`; recoverable `blocked` -> `continuation_ref,repair_input` -> `request-routing-blocked` |
| `guru-answer-request` / `ordinary`, `trellis_reference`, `explicit_history`, `explicit_diagnosis`, `provider_reentry` | semantic | initial=`answer_scope_ref,answer_profile`; provider repair=`continuation_ref,repair_input`, where the Answer-owned continuation binds the original answer scope/profile and exact controlled-adapter profile. The selected reference/explicit profile resolves its exact provider asset from `answer_scope_ref` rather than accepting a caller-authored runtime asset identity | `answered` -> `answer_status,unverified_fact_refs` -> `workflow-completed`; recoverable `answer_provider_blocked` -> `binding_or_provider_fact_refs,continuation_ref,repair_input` -> `direct-answer-provider-blocked`; terminal `answer_binding_blocked` -> `binding_fact_refs,repair_input` -> `direct-answer-binding-blocked` |
| `guru-resolve-current-work` / `continue`, `history`, `disposition` | semantic | `intent_ref` | `current_work_recovered` -> `lifecycle_ref,current_owner_id` -> `guru-current-owner-router`; `history_query_required` -> `history_query_ref` -> `guru-query-lifecycle-history`; `disposition_required` -> `lifecycle_ref,disposition_intent` -> `guru-dispose-lifecycle`; `recovery_blocked` -> `candidate_refs,continuation_ref,repair_input` -> `current-work-recovery-blocked` |
| `guru-dispose-lifecycle` / `initial`, `choice_reentry`, `remote_reentry`, `cleanup_confirmation_reentry`, `cleanup_refusal_choice_reentry`, `repair_reentry` | semantic | initial=`lifecycle_ref,disposition_intent`; later-choice re-entry=`continuation_ref,disposition_intent`; remote re-entry=`remote_outcome_ref,continuation_ref`; cleanup-confirmation re-entry=`continuation_ref`; cleanup-refusal-with-choice re-entry=`continuation_ref,disposition_intent`; repair re-entry=`continuation_ref,repair_input` | `remote_convergence_required` -> `current_owner_id,remote_boundary_ref,continuation_ref` -> `active-lifecycle-remote-convergence-wait`; `cleanup_confirmation_required` -> `continuation_ref` -> `active-lifecycle-cleanup-confirmation-wait`, whose current clear affirmative enters `cleanup_confirmation_reentry`; an explicit cleanup refusal already containing one retain/suspend choice enters `cleanup_refusal_choice_reentry` and consumes that choice directly; otherwise `active_lifecycle_disposition_choice_required` -> `lifecycle_ref,continuation_ref` -> `active-lifecycle-disposition-choice-wait`, whose later unique choice alone enters `choice_reentry`, with zero deletion; `disposition_completed` -> `disposition_kind,durable_result_ref` -> `workflow-completed`; `blocked` -> `continuation_ref,repair_input` -> `lifecycle-disposition-blocked`, whose exact repair enters `repair_reentry` |
| `guru-query-lifecycle-history` / `resolve` | semantic | `history_query_ref` | `history_current` -> `durable_result_ref,result_kind` -> `workflow-completed`; recoverable `blocked` -> `candidate_refs,continuation_ref,repair_input` -> `lifecycle-history-blocked` |
| `guru-route-distribution` / `select` | semantic | `terminal_intent_ref,candidate_ref,target_ref` | `projection_validation` -> `candidate_ref,target_ref` -> `guru-validate-extension-projection`, whose owner derives the declared surface from the exact candidate; `clean_install` -> same -> `guru-install-clean-repository`; `existing_migration` -> same -> `guru-migrate-existing-repository`; `exact_release` -> same -> `guru-release-candidate`; recoverable `blocked` -> `state_class,continuation_ref,repair_input` -> `distribution-routing-blocked` |
| `guru-review-contract-wording` / five closed review-only caller profiles below | semantic | `scope_ref,caller_continuation_ref`; the selected profile fixes the original caller, which owns the opaque continuation | `pass` -> `scope_ref,caller_continuation_ref` -> `guru-specialist-result-router`; `revision_findings` -> `finding_refs,caller_continuation_ref` -> same router; `blocked` -> `caller_continuation_ref,repair_input` -> same router. `content_changed` is schema-invalid for every review-only profile |
| `guru-review-contract-wording` / four closed change-scoped caller profiles below | semantic | `scope_ref,caller_continuation_ref`; the selected profile fixes the active content owner | `pass` -> `scope_ref,caller_continuation_ref` -> `guru-specialist-result-router`; `content_changed` -> `changed_scope_ref,caller_continuation_ref` -> same router; `blocked` -> `caller_continuation_ref,repair_input` -> same router. `revision_findings` is schema-invalid for every change-scoped profile |
| `guru-qualify-normal-scenario` / eleven closed caller profiles listed below | semantic | standalone=`scope_ref,target_ref,candidate_refs,caller_continuation_ref`; active profiles=`target_ref,candidate_refs,caller_continuation_ref`; the profile fixes the original caller/return owner, the caller owns the opaque continuation, and the Skill owner live-reads applicable authority locators | `classified` -> `candidate_decisions,caller_continuation_ref` -> `guru-specialist-result-router`; `scope_confirmation_required` -> `scope_candidate_refs,caller_continuation_ref` -> the exact profile-fixed `guru-clarify-requirements` qualification-scope profile listed below; active profiles only: `mechanism_revision_required` -> `candidate_decisions,caller_continuation_ref` -> `guru-specialist-result-router`; `blocked` -> `caller_continuation_ref,repair_input` -> same router. `mechanism_revision_required` is schema-invalid for `standalone_specialist` |

`guru-bound-intent-router` 只把 `owner_local_additive|material_additive|override` 交给 current/earliest
owner；它不生成 receipt 或 top-level route。`guru-specialist-result-router` 按 validated profile/caller
投影到 active caller，或在 standalone result 报告后完成 invocation；它不做第二次 semantic 判断。
Qualification scope clarification is the only result that first visits another semantic owner: the qualifier
returns the original caller's opaque continuation to one profile-fixed Clarification input. Clarification obtains
one real scope choice and returns the token unchanged to that original caller. The caller then rebuilds the complete
current candidate set and freshly invokes the same qualification profile; neither Clarification nor either router
may inspect the continuation, reuse the pre-choice candidate set, or project an unresolved scope as `classified`.
The other three results also return the unchanged token: `classified` enters the original caller's closed current-
route re-entry, `mechanism_revision_required` enters only that caller's semantic mechanism-revision profile, and
`blocked` enters only that caller's qualification-repair profile. A mechanism owner that cannot yet remove or
replace the task-introduced mechanism emits its own recoverable blocked result; it never forwards the unmodified
candidate into acceptance, finding, implementation or publication.

Wording caller profiles are also closed. The four active callers below are the content owners that may request an
explicit bounded wording review inside an existing change lifecycle. Any other active owner first returns the
wording intent to its earliest applicable content owner; it cannot pass an arbitrary caller id to the specialist.

| Wording profile | Fixed caller / return owner | Supported result set |
| --- | --- | --- |
| `standalone_review_only` | `guru-route-request` | `pass|revision_findings|blocked` |
| `task_free_review_only` | `guru-execute-task-free-change` | `pass|revision_findings|blocked` |
| `requirements_review_only` | `guru-clarify-requirements` | `pass|revision_findings|blocked` |
| `planning_review_only` | `guru-plan-task` | `pass|revision_findings|blocked` |
| `implementation_review_only` | `guru-implement-task` | `pass|revision_findings|blocked` |
| `task_free_change_scoped` | `guru-execute-task-free-change` | `pass|content_changed|blocked` |
| `requirements_change_scoped` | `guru-clarify-requirements` | `pass|content_changed|blocked` |
| `planning_change_scoped` | `guru-plan-task` | `pass|content_changed|blocked` |
| `implementation_change_scoped` | `guru-implement-task` | `pass|content_changed|blocked` |

The standalone caller owns the three applicable return profiles below. Each active wording caller owns all four:

| Wording return profile | Complete business input | Required owner behavior |
| --- | --- | --- |
| `wording_pass_reentry` | `scope_ref,caller_continuation_ref` | open only its own continuation and resume the exact current route; standalone Route Request reports one `standalone_specialist_completed` result |
| `wording_revision_reentry` | `finding_refs,caller_continuation_ref` | active caller reports the bounded review result and resumes its current route; standalone Route Request reports the complete findings and then completes without asking for a modify/stop choice |
| `wording_content_changed_reentry` | `changed_scope_ref,caller_continuation_ref` | active content owner discards the prior review result, rebuilds the full fixed scope, rescans and freshly invokes the same wording profile; standalone use is invalid |
| `wording_blocked_reentry` | `caller_continuation_ref,repair_input` | original caller repairs the exact scope/authority/semantic prerequisite, rebuilds the current scope and freshly invokes the same wording profile; unresolved repair remains in that caller's Section 7.1 block |

`guru-specialist-result-router` selects these returns only from the producer profile already bound to the caller. It
does not inspect the token, choose an owner or turn revision findings into a change route.

`guru-answer-request:answer_binding_blocked` 只适用于 `answer_scope_ref`、fixed profile 或唯一 consumer
绑定 stale/mismatched 且无法在当前 invocation 内修复的 terminal 合同失效。controlled adapter 同步返回的
`provider_boundary_blocked` 由 Answer owner 转为自己的 recoverable `answer_provider_blocked`，保留
Answer-owned continuation，并在 repair 后只从 `provider_reentry` 重调同一个固定 adapter profile。
repository/provider unavailable、拒绝访问、结果不完整或无法核实 live fact 必须投影到
`answered.answer_status` 与 `unverified_fact_refs` 后正常完成；这些结果不得选择任一 blocked exit，且后续
重试建立新的 direct-answer invocation。

`active-lifecycle-disposition-choice-wait` 是 `guru-dispose-lifecycle` 拥有的 dialogue-local pause，只用于
cleanup plan 被明确拒绝且同一回复没有唯一 retain/suspend choice 的正常路径。它只询问一次该真实选择；
缺失、疑问或歧义回复保持 wait，唯一 retain/suspend choice 以新的 current `disposition_intent` 进入
`choice_reentry`。若原拒绝已包含唯一 choice，owner 直接消费该 choice而不先产生 wait。整个 choice current
前 cleanup/delete count 为0，reply/authorization 不持久化；该结果不得改写为 generic `blocked`、
`disposition_cleanup_not_executed` terminal或 `retained|suspended` 双结果。

Qualification profiles are a closed target set; an unlisted caller/profile pair is invalid:

| Qualification profile | Fixed caller / return owner | Clarification profile | Scope-choice return | Supported results |
| --- | --- | --- | --- | --- |
| `task_free_pre_write` | `guru-execute-task-free-change` | `qualification_task_free_pre_write_scope` | `guru-execute-task-free-change:qualification_scope_reentry` | all four |
| `task_free_evolution` | `guru-execute-task-free-change` | `qualification_task_free_evolution_scope` | `guru-execute-task-free-change:qualification_scope_reentry` | all four |
| `requirements_scope_set` | `guru-clarify-requirements` | `qualification_requirements_scope_set` | `guru-clarify-requirements:qualification_scope_reentry` | all four |
| `change_request_candidate_set` | `guru-review-change-request` | `qualification_change_request_scope` | `guru-review-change-request:qualification_scope_reentry` | all four |
| `planning_scenario_set` | `guru-approve-task-plan` | `qualification_planning_scope` | `guru-approve-task-plan:qualification_scope_reentry` | all four |
| `implementation_discovery` | `guru-implement-task` | `qualification_implementation_scope` | `guru-implement-task:qualification_scope_reentry` | all four |
| `base_impact_candidate_set` | `guru-reconcile-task-base` | `qualification_base_impact_scope` | `guru-reconcile-task-base:qualification_scope_reentry` | all four |
| `phase2_candidate_set` | `guru-check-task` | `qualification_phase2_scope` | `guru-check-task:qualification_scope_reentry` | all four |
| `branch_review_candidate_set` | `guru-review-branch` | `qualification_branch_review_scope` | `guru-review-branch:qualification_scope_reentry` | all four |
| `publication_candidate_set` | `guru-review-delivery-readiness` | `qualification_publication_scope` | `guru-review-delivery-readiness:qualification_scope_reentry` | all four |
| `standalone_specialist` | `guru-route-request` through the thin top-level `guru-specialist-router` | `qualification_standalone_scope` | `guru-route-request:qualification_scope_reentry`, then standalone completion after fresh classification | `classified|scope_confirmation_required|blocked`; mechanism revision is schema-invalid |

The ten active callers own all five additional closed profiles below. Standalone `guru-route-request` owns only
`qualification_classified_reentry`, `qualification_scope_reentry`, `qualification_scope_repair`, and
`qualification_blocked_reentry`; it is not an original mechanism owner and therefore cannot receive
`mechanism_revision_required` or expose `qualification_mechanism_reentry`:

| Qualification return profile | Complete business input | Required owner behavior |
| --- | --- | --- |
| `qualification_classified_reentry` | `candidate_decisions,caller_continuation_ref` | open only its own continuation, consume the current classification and resume that exact caller route; standalone Route Request reports one `standalone_specialist_completed` result |
| `qualification_scope_reentry` | `scope_choice_ref,caller_continuation_ref` | live-reread decision-relevant facts, rebuild the full candidate set and freshly invoke the same qualification profile |
| `qualification_scope_repair` | `caller_continuation_ref,repair_input` | repair the Clarification prerequisite and re-enter the same profile-fixed Clarification input; do not invoke Qualification directly |
| `qualification_mechanism_reentry` | `candidate_decisions,caller_continuation_ref` | as the original semantic mechanism owner, remove/replace only the task-introduced mechanism, rebuild the full candidate set and freshly invoke the same qualification profile |
| `qualification_blocked_reentry` | `caller_continuation_ref,repair_input` | repair authority/candidate/consumer freshness, rebuild the full candidate set and freshly invoke the same qualification profile |

These applicable profiles are part of each listed public caller's input contract even when its primary row uses the
compact phrase “qualification-return profiles”. `guru-route-request` owns only the four declared standalone returns;
the thin router never becomes the mechanism owner. A scope or mechanism repair prerequisite that remains unresolved emits
the caller's own Section 7.1 recoverable blocked result. No profile can return directly to `classified` or
acceptance without a fresh Qualification invocation.

### 3.1 Lifecycle Owner, Resume And Fresh-Entry Registry

The two lifecycle routers use the closed registry below. Every listed Skill owns exactly two additional input
profiles: `lifecycle_intent_reentry=lifecycle_ref,bound_event_ref,event_sequence` for a causally bound user event and
`current_work_resume=lifecycle_ref` for a recovered active lifecycle. The selected `current_owner_id` is validated
against one exact row before Admission or Current Work emits it; the router then selects that exact Skill and named
profile and projects only the fields shown. `bound_event_ref` is the direct-consumer reference to the new host event;
the owner opens its own current continuation, live-validates its current stage, consumes that exact event and resumes
or re-evaluates only that stage. No owner id outside this table, generic “matching profile”, task scan, host-message
history, envelope-file read, private checkpoint body or ambient lookup is accepted.

| Registry group | Exact public Skill ids |
| --- | --- |
| admission, answer and resolution | `guru-admit-invocation`, `guru-route-request`, `guru-answer-request`, `guru-resolve-current-work`, `guru-query-lifecycle-history` |
| change preparation | `guru-select-workflow-mode`, `guru-execute-task-free-change`, `guru-sync-base`, `guru-discover-change-context`, `guru-clarify-requirements`, `guru-review-change-request`, `guru-create-task-workspace` |
| authority and planning | `guru-maintain-requirements-design-test-ssot`, `guru-maintain-architecture-baseline`, `guru-bootstrap-repository-ssot`, `guru-plan-task`, `guru-approve-task-plan` |
| implementation and review | `guru-implement-task`, `guru-check-task`, `guru-create-task-commit`, `guru-reconcile-task-base`, `guru-review-branch` |
| delivery and disposition | `guru-select-delivery-route`, `guru-review-delivery-readiness`, `guru-accept-task`, `guru-publish-task-pr`, `guru-merge-task-pr`, `guru-resolve-issue-closure`, `guru-finalize-task`, `guru-clean-task-resources`, `guru-dispose-lifecycle` |
| distribution | `guru-route-distribution`, `guru-validate-extension-projection`, `guru-install-clean-repository`, `guru-migrate-existing-repository`, `guru-release-candidate`, `guru-maintain-stock-projection` |

These 37 ids are the complete lifecycle-owner subset of the 39 public Skills. The two specialist Skills,
`guru-review-contract-wording` and `guru-qualify-normal-scenario`, never become lifecycle owners: their fixed original
caller retains lifecycle ownership while the specialist and thin router return the caller-owned continuation. A
specialist wait/block therefore resumes through that original caller, not through a specialist registry row.

Only four registered owners can hold an irreversible remote result:
`guru-publish-task-pr`, `guru-merge-task-pr`, `guru-resolve-issue-closure`, and `guru-release-candidate`. Each owns an
additional `remote_disposition_resume=remote_boundary_ref` profile. When invoked by
`active-lifecycle-remote-convergence-wait`, that profile preserves the exact candidate and produces exactly one of
`remote_terminal_current|remote_forward_recovered_current|remote_terminal_block_current`, each with only
`remote_outcome_ref` for that wait. The wait retains the Disposition-owned `continuation_ref`, joins it with the
selected `remote_outcome_ref`, and projects both to `guru-dispose-lifecycle:remote_reentry`; the remote owner never
receives or returns the Disposition continuation.

Fresh successor Admission also has a closed producer inventory. A listed lifecycle owner may emit
`successor_invocation_required -> pending_intent_ref,prior_outcome_ref` only after a no-side-effect stop or local
suspend is current; its sole consumer is `guru-admit-invocation:post_owner_pending`. One of the four remote owners may
emit `post_remote_intent_ready -> pending_intent_ref,remote_outcome_ref` only after its normal/forward-recovered/
terminal-block outcome is current; its sole consumer is `guru-admit-invocation:post_remote_pending`. Both Admission
profiles allocate a new invocation/envelope and exactly one new receipt before the isolation gate. They never reuse
the prior lifecycle identity, candidate, envelope or receipt. A remote-disposition request instead uses the named
remote-convergence wait above and cannot be mistaken for a pending additive/override fresh entry.

## 4. Change Lifecycle Skills

| Public Skill / profiles | Mode | Minimal public input | Exit -> minimal output -> unique consumer |
| --- | --- | --- | --- |
| `guru-select-workflow-mode` / `select`, `choice_reentry` | semantic | select=`change_scope_ref`; choice re-entry=`continuation_ref,choice_ref`, where the continuation binds that change scope | `standard` -> `change_scope_ref` -> `guru-sync-base`; `task_free` -> `change_scope_ref` -> `guru-execute-task-free-change`; `choice_required` -> `continuation_ref` -> `workflow-mode-choice-wait`, whose later unique `choice_ref` enters `choice_reentry`; recoverable `blocked` -> `continuation_ref,repair_input` -> `workflow-mode-blocked` |
| `guru-execute-task-free-change` / `initial`, `finding_reentry`, `evolution_reentry`, four wording-return profiles, five qualification-return profiles | semantic | primary profiles=`change_scope_ref`; specialist returns use the Section 3 closed shapes; this owner resolves and reviews checkout suitability itself | `completed` -> `edited_path_refs,validation_summary,unverified_boundaries` -> `workflow-completed`; `current_work_required` -> `intent_ref` -> `guru-resolve-current-work`; `escalation_required` -> `partial_work_ref,change_scope_ref` -> `guru-task-free-escalation-router`; recoverable `blocked` -> `partial_work_ref,continuation_ref,repair_input` -> `task-free-blocked` |
| `guru-sync-base` / `pre_task`, `task_free_escalation`, `refresh_reentry` | semantic | pre-task=`change_scope_ref`; escalation adds `partial_work_ref`; refresh=`change_scope_ref,base_ref,continuation_ref`, where the continuation is owned by Discovery and binds its exact original profile; the Skill owns current base-selector resolution rather than accepting a caller-authored runtime selector | for an actual Git refresh it owns the private exact action plan and `EVO-REQ-081` boundary; `base_current` -> initial/escalation=`change_scope_ref,base_ref,authority_checkout_ref` plus escalation-only `partial_work_ref`, refresh additionally returns `continuation_ref`; all -> the matching `guru-discover-change-context` profile; `base_sync_not_executed` -> `change_scope_ref,base_selector_ref` plus refresh-only `continuation_ref` and escalation-only `partial_work_ref` -> `base-sync-not-executed`; recoverable `blocked` -> `continuation_ref,repair_input` -> `base-sync-blocked` |
| `guru-discover-change-context` / `initial`, `task_free_escalation`, `base_refresh`, `context_refresh` | semantic | initial/base-refresh=`change_scope_ref,base_ref,authority_checkout_ref`; escalation adds `partial_work_ref`; base-refresh adds the Discovery-owned `continuation_ref`; context-refresh=`change_scope_ref,change_context_ref,continuation_ref`, where that token belongs to Clarification and is returned unopened; this owner resolves base/authority-checkout identity from its own current context before targeted reread | `context_current` -> initial/escalation=`change_scope_ref,change_context_ref` plus escalation-only `partial_work_ref` -> matching Clarification profile; context-refresh=`change_context_ref,continuation_ref` -> `guru-clarify-requirements:context_refresh_reentry`; after base-refresh this owner opens only its own continuation and emits the corresponding one of those closed shapes. `base_refresh_required` -> `change_scope_ref,base_ref,continuation_ref` -> `guru-sync-base:refresh_reentry`; recoverable `blocked` -> `continuation_ref,repair_input` -> `change-context-blocked` |
| `guru-clarify-requirements` / `initial`, `task_free_escalation`, eight closed caller-return profiles below, eleven closed qualification-scope profiles above, four wording-return profiles, five qualification-return profiles, `context_refresh_reentry`, `retarget_reentry` | semantic | initial=`change_scope_ref,change_context_ref`; escalation adds `partial_work_ref`; ordinary caller-return profiles consume either `scope_ref,caller_continuation_ref`, planning revision=`revision_ref,caller_continuation_ref`, or approval scope=`scope_ref,plan_revision_ref`; qualification-scope profiles consume `scope_candidate_refs,caller_continuation_ref`; this Skill's wording/qualification returns use the Section 3 closed shapes; context-refresh re-entry=`change_context_ref,continuation_ref`; retarget re-entry=`continuation_ref,target_ref`. Clarification opens only its own continuation; every caller token is returned unchanged | initial/escalation `requirements_current` -> `requirement_delta_ref,reviewed_design_binding_ref,change_context_ref` plus escalation-only `partial_work_ref`; ordinary caller-return -> `requirements_result_ref` plus the exact `caller_continuation_ref` or `plan_revision_ref`; all -> `guru-requirements-current-router`, whose target is fixed by the selected profile. Qualification-scope profiles ask for one real scope choice, then `qualification_scope_current` -> `scope_choice_ref,caller_continuation_ref` -> `guru-qualification-scope-return-router`; their `qualification_scope_blocked` -> `caller_continuation_ref,repair_input` -> the same router and the original caller's exact repair profile. `context_refresh_required` -> owner-produced `change_scope_ref,change_context_ref,continuation_ref` -> `guru-discover-change-context:context_refresh`; `scope_retarget_required` -> `continuation_ref` -> `requirements-scope-retarget-wait`, whose later unique `target_ref` enters `retarget_reentry`; recoverable non-qualification `blocked` -> `continuation_ref,repair_input` -> `requirements-clarification-blocked` |
| `guru-review-change-request` / `initial`, `task_free_escalation`, `clarification_reentry`, `readiness_reentry`, `suspended_readiness_reentry`, five qualification-return profiles | semantic | initial=`requirement_delta_ref,reviewed_design_binding_ref,change_context_ref`; escalation adds `partial_work_ref`; clarification re-entry=`requirements_result_ref,caller_continuation_ref`; Workspace readiness re-entry=`change_identity`; suspended readiness re-entry=`change_identity,partial_work_ref`; qualification returns use the Section 3 closed shapes. Each re-entry identity is owned by this Skill and causes a targeted live reread rather than reconstruction of the initial three-field input | `ready` -> `change_identity` plus escalation-only `partial_work_ref` -> `guru-create-task-workspace`; `active_duplicate` -> `lifecycle_ref,current_owner_id` -> `guru-current-owner-router`; `completed_duplicate` -> `durable_result_ref` -> `workflow-completed`; `scope_clarification_required` -> `scope_ref,caller_continuation_ref` -> `guru-clarify-requirements:change_readiness_scope`; `prerequisite_blocked` -> `prerequisite_ref,continuation_ref,repair_input` -> `change-request-prerequisite-blocked`; `resolution_blocked` -> `candidate_refs,continuation_ref,repair_input` -> `change-request-resolution-blocked` |
| `guru-create-task-workspace` / `create_or_reuse`, `suspended_work` | semantic | `change_identity`; suspended profile adds `partial_work_ref` | the Skill first live-resolves the exact repo/Issue/base/branch/worktree/task/path and ownership/isolation state. When every required resource already matches the current change identity and no creation, transfer or isolation action remains, it emits `workspace_current` -> `task_ref` -> `guru-maintain-requirements-design-test-ssot:task_impact_sync` with zero plan display, confirmation wait, refusal branch and mutation. Otherwise it authors and semantically reviews one private exact resource/transfer-or-isolation plan, displays it under `EVO-REQ-081`, then consumes dialogue-local confirmation; terminal refusal `workspace_not_created` -> `change_identity` plus suspended-only `partial_work_ref` -> `task-workspace-not-created`; `readiness_refresh_required` -> `change_identity` plus suspended-only `partial_work_ref` -> the matching `guru-review-change-request` readiness-reentry profile; recoverable `blocked` -> `continuation_ref,repair_input` -> `task-workspace-blocked` |
| `guru-maintain-requirements-design-test-ssot` / `bootstrap_foundation`, `task_impact_sync`, `promotion`, `repair`, `bootstrap_reentry` | semantic | task impact=`task_ref`; bootstrap/repair=`task_ref,repair_scope_ref`; promotion=`task_ref,rdt_promotion_ref`, where that Branch-Review-authored ref binds exact contribution content, reviewed committed range and expected-current identity; Bootstrap re-entry=`authority_identity_refs,authority_caller_continuation_ref`; the RDT owner resolves current authority locators/identities itself, consumes the Clarification-owned `requirement_delta_ref,reviewed_design_binding_ref` from the same `authority_context`, and opens only its own continuation. It never reconstructs the pre-plan task delta from task files, Workspace state or an ambient lookup | `ssot_current` -> closed profile output: no-impact/aligned=`rdt_result_ref,impact_kind`; contribution-current additionally requires `contribution_ref` -> `guru-rdt-current-router`; task-local contribution authoring/revision remains inside `task_impact_sync` and never invokes shared promotion. `revision_required` -> `revision_ref` -> `guru-rdt-revision-router`; `baseline_incomplete` -> `missing_layer_refs,authority_caller_continuation_ref` plus common `task_ref` -> `guru-bootstrap-repository-ssot:rdt_request`; recoverable `blocked` -> `continuation_ref,repair_input` -> `rdt-ssot-blocked` |
| `guru-maintain-architecture-baseline` / `bootstrap_foundation`, `task_impact_sync`, `promotion`, `repair`, `bootstrap_reentry` | semantic | task impact=`task_ref,rdt_result_ref`; bootstrap/repair=`task_ref,repair_scope_ref`; promotion=`task_ref,architecture_promotion_ref`, where that Branch-Review-authored ref binds exact contribution content, reviewed committed range and expected-current identity; Bootstrap re-entry=`authority_identity_refs,authority_caller_continuation_ref`; the Architecture owner resolves baseline/constitution/change-contract identities and required concerns itself and opens only its own continuation | `baseline_current` has three disjoint output schemas: `impact_kind=no_impact` -> `rdt_result_ref,architecture_result_ref,impact_kind`; `impact_kind=aligned` -> `rdt_result_ref,architecture_result_ref,impact_kind,change_path`; `impact_kind=contribution_current` -> `rdt_result_ref,architecture_result_ref,impact_kind,change_path,contribution_ref`; all project to `guru-architecture-current-router`. Task-local contribution authoring/revision remains inside `task_impact_sync` and never invokes shared promotion. `baseline_incomplete` -> `missing_layer_refs,authority_caller_continuation_ref` plus common `task_ref` -> `guru-bootstrap-repository-ssot:architecture_request`; `architecture_conflict`/`contract_incomplete`/`fitness_regression` -> `finding_refs,revision_owner_kind` -> `guru-architecture-current-router`; recoverable `blocked` -> `continuation_ref,repair_input` -> `architecture-baseline-blocked` |
| `guru-bootstrap-repository-ssot` / `rdt_request`, `architecture_request`, `projection_refresh`, `repair_reentry`, `blocked_reentry` | semantic | authority request=`task_ref,missing_layer_refs,authority_caller_continuation_ref`, with profile fixed by the producing authority owner. Projection refresh has two disjoint inputs after the post-review router proves every selected outstanding RDT/Architecture promotion, if any, current: `projection_kind=authority_only -> task_ref,reviewed_range_ref`; `projection_kind=with_code_spec -> task_ref,reviewed_range_ref,code_spec_contribution_ref`, where the ref is Branch-Review-authored, binds that same range and denotes only code-spec work missing from the current projection. Repair re-entry=`task_ref,bootstrap_continuation_ref,repair_ref`; blocked re-entry=`task_ref,bootstrap_continuation_ref,repair_input`. Bootstrap opens only its own continuation and never inspects the authority caller token | authority `current` -> `authority_identity_refs,authority_caller_continuation_ref` -> `guru-bootstrap-return-router`; projection `current` -> `spec_projection_ref` -> `guru-check-task:authority_reentry` by renaming it to `authority_result_ref`; `repair_required` -> `bootstrap_continuation_ref,repair_ref` -> same Skill `repair_reentry`; `blocked` -> `bootstrap_continuation_ref,repair_input` -> `repository-ssot-bootstrap-blocked`, whose exact repair enters `blocked_reentry`. `projection_refresh` is the only `.trellis/spec` writer: it live-rereads the current RDT/Architecture authority identities, current `guru-code-spec-projection-1.0` and, only for `with_code_spec`, the same-range reviewed contribution. If the projection already contains the exact selected current authority and code-spec target identities, it emits current without a write; otherwise it semantically reviews/promotes only the missing locator/usage/freshness projection. Material identity/content drift returns repair or the affected authority owner. It never copies authority prose or accepts a raw `trellis-update-spec` result |
| `guru-plan-task` / `initial`, `revision_reentry`, `finding_reentry`, `requirements_reentry`, `approval_scope_reentry`, `authority_reentry`, `base_reentry`, four wording-return profiles | semantic | initial=`task_ref,rdt_result_ref,architecture_result_ref`; revision re-entry=`task_ref,revision_ref`; finding re-entry=`task_ref,finding_refs`; requirements re-entry=`task_ref,requirements_result_ref,caller_continuation_ref`; approval-scope re-entry=`task_ref,requirements_result_ref,plan_revision_ref`; authority re-entry=`task_ref,authority_result_ref`; base re-entry=`task_ref,base_result_ref`; wording returns use the Section 3 closed shapes. The Plan owner obtains the Clarification-owned current requirement delta/reviewed-design projection from `authority_context`, resolves the authorized RDT/Architecture result refs, and directly consumes the applicable stable authority content; it does not consume a producer summary or reread the source through an ambient path | `plan_authored` -> `task_ref` -> `guru-approve-task-plan:initial_review`; `requirements_revision_required` -> `revision_ref,caller_continuation_ref` -> `guru-clarify-requirements:task_planning_revision`; `rdt_revision_required` -> `revision_ref` renamed to `repair_scope_ref` -> `guru-maintain-requirements-design-test-ssot:repair`; `architecture_revision_required` -> `revision_ref` renamed to `repair_scope_ref` -> `guru-maintain-architecture-baseline:repair`; recoverable `blocked` -> `continuation_ref,repair_input` -> `task-planning-blocked` |
| `guru-approve-task-plan` / `initial_review`, `stale_reentry`, `activation_confirmation`, five qualification-return profiles | semantic | initial=`task_ref`; stale re-entry=`task_ref,stale_reason_refs`; confirmation=`task_ref,plan_identity_ref` from the same current private approval checkpoint; qualification returns use the Section 3 closed shapes. The Approval owner directly consumes the stable RDT/Architecture/task-doc content and current result projections from `authority_context`; author summaries and file-existence booleans are not inputs | `ready_for_activation_confirmation` -> `task_ref,plan_identity_ref` -> `task-plan-activation-wait`. Before this exit, the owner displays one exact compound next-action plan that includes both the deterministic task-status activation and immediate entry into `guru-implement-task:initial` under the approved implementation scope/allowed-write boundary, while explicitly excluding Commit, push, PR, merge, Release and cleanup. A current clear affirmative enters `activation_confirmation` and authorizes exactly that displayed compound action; it does not create a second routine implementation-entry confirmation. The owner then runs `phase-1-task-activation` and only on a current transition emits `approved` -> `task_ref` -> `guru-implement-task:initial`; an objective transition failure uses this Skill's recoverable `blocked` route and performs no implementation write. `plan_not_activated` -> `task_ref` -> `workflow-completed`; `approval_stale` -> `task_ref,stale_reason_refs` -> same Skill `stale_reentry`; `revision_required` -> `revision_ref` -> `guru-plan-task:revision_reentry`; `clarify_scope` -> `scope_ref,plan_revision_ref` -> `guru-clarify-requirements:plan_approval_scope`, which returns to Plan rather than directly re-approving stale planning artifacts; recoverable `blocked` -> `continuation_ref,repair_input` -> `task-plan-approval-blocked` |
| `guru-implement-task` / `initial`, `finding_reentry`, `discovery_reentry`, `authority_reentry`, `base_reentry`, four wording-return profiles, five qualification-return profiles | semantic | initial=`task_ref`; finding/discovery re-entry adds its exact ref; authority re-entry=`task_ref,authority_result_ref`; base re-entry=`task_ref,base_result_ref`; specialist returns use the Section 3 closed shapes. The owner resolves the current approved plan, implementation scope and RDT/Architecture projections itself | `implementation_current` -> `candidate_ref` -> `guru-check-task`; `planning_revision_required` -> `revision_ref` -> `guru-plan-task:revision_reentry`; `authority_reentry_required` -> `authority_kind,revision_ref` -> `guru-authority-reentry-router`; recoverable `blocked` -> `partial_work_ref,continuation_ref,repair_input` -> `task-implementation-blocked` |
| `guru-check-task` / `initial`, `authority_reentry`, `base_reentry`, five qualification-return profiles | semantic | initial=`task_ref,candidate_ref`; authority re-entry=`task_ref,authority_result_ref`; base re-entry=`task_ref,base_result_ref`; qualification returns use the Section 3 closed shapes. Either re-entry causes this owner to resolve the current candidate from its own continuation/current task binding and rerun only affected checks | `passed` -> `candidate_ref,validation_summary` -> `guru-create-task-commit`; `implementation_required` -> `finding_refs` -> `guru-implement-task`; `planning_required` -> `finding_refs` -> `guru-plan-task:finding_reentry`; `authority_reentry_required` -> `authority_kind,revision_ref` -> `guru-authority-reentry-router`; recoverable `blocked` -> `continuation_ref,repair_input` -> `task-check-blocked` |
| `guru-create-task-commit` / `initial`, `scope_reentry`, `authority_reentry` | semantic | initial=`task_ref,candidate_ref,validation_summary`; scope re-entry=`task_ref,requirements_result_ref,caller_continuation_ref`; authority re-entry=`task_ref,authority_result_ref`. The exact Commit owner restores and live-validates its bound candidate/check result | for the exact staged scope it owns the private commit plan and `EVO-REQ-081` boundary; terminal refusal `commit_not_created` -> `task_ref,candidate_ref` -> `task-commit-not-created`; `committed` -> `commit_ref,base_ref,range_ref` -> `guru-review-branch`; `implementation_required` -> `finding_refs` -> `guru-implement-task`; `planning_required` -> `finding_refs` -> `guru-plan-task:finding_reentry`; `scope_confirmation_required` -> `scope_ref,caller_continuation_ref` -> `guru-clarify-requirements:task_commit_scope`; `authority_reentry_required` -> `authority_kind,revision_ref` -> `guru-authority-reentry-router`; recoverable `blocked` -> `continuation_ref,repair_input` -> `task-commit-blocked` |
| `guru-reconcile-task-base` / `current_pair`, `reentry`, `scope_reentry`, five qualification-return profiles | semantic | current pair=`task_ref,task_head_ref,base_before_ref,base_after_ref,resume_target`, with `resume_target=plan|implement|check|branch_review|delivery_route|delivery_readiness`; base re-entry=`task_ref,base_pair_ref`; scope re-entry=`task_ref,requirements_result_ref,caller_continuation_ref`; qualification returns use the Section 3 closed shapes. The exact Reconcile owner resolves and live-validates its bound pair rather than requiring another caller to copy pair fields | `reconciled` -> `resume_target,base_result_ref` -> `guru-base-resume-router`; `review_continuity_required` -> `base_ref,commit_ref,range_ref` -> `guru-review-branch`; `implementation_required` -> `finding_refs` -> `guru-implement-task`; `planning_required` -> `finding_refs` -> `guru-plan-task:finding_reentry`; `scope_confirmation_required` -> `scope_ref,caller_continuation_ref` -> `guru-clarify-requirements:base_reconciliation_scope`; recoverable `blocked` -> `continuation_ref,repair_input` -> `task-base-reconciliation-blocked` |
| `guru-review-branch` / `full_diff`, `continuity`, `scope_reentry`, `authority_reentry`, `base_reentry`, five qualification-return profiles | semantic | full-diff/continuity=`task_ref,base_ref,commit_ref,range_ref`; scope re-entry=`task_ref,requirements_result_ref,caller_continuation_ref`; authority re-entry=`task_ref,authority_result_ref`; base re-entry=`task_ref,base_result_ref`; qualification returns use the Section 3 closed shapes. The Branch Review owner restores and live-validates its bound committed range | `passed` uses independent closed discriminators `promotion_kind=none|rdt|architecture|rdt_then_architecture` and `projection_kind=none|authority_only|with_code_spec`, each computed from outstanding work after comparing every in-range contribution with live authority/projection identities. All schemas require `reviewed_range_ref,promotion_kind,projection_kind`; applicable promotion schemas require exact `rdt_promotion_ref` and/or `architecture_promotion_ref`, each binding contribution content, this range and an expected-current identity that still matches live authority. A contribution already current at its reviewed target identity emits no promotion ref. `with_code_spec` alone requires a same-range `code_spec_contribution_ref` whose target identity is still missing from the current projection. `projection_kind=none` is valid only with `promotion_kind=none` and means no outstanding authority promotion plus no in-range code-spec contribution missing from current projection, even when the full diff still contains the original already-current contribution/projection changes; `authority_only` requires a non-none promotion and forbids the code-spec ref; `with_code_spec` is valid with any promotion kind. Authority/contribution/expected-current/projection material drift cannot be classified as none and returns the affected owner. A raw `trellis-update-spec` result is invalid -> `guru-post-review-authority-router`; `implementation_required` -> `finding_refs` -> `guru-implement-task`; `planning_required` -> `finding_refs` -> `guru-plan-task:finding_reentry`; `scope_confirmation_required` -> `scope_ref,caller_continuation_ref` -> `guru-clarify-requirements:branch_review_scope`; `authority_reentry_required` -> `authority_kind,revision_ref` -> `guru-authority-reentry-router`; `base_reconciliation_required` -> `base_pair_ref` -> `guru-reconcile-task-base:reentry`; recoverable `blocked` -> `continuation_ref,repair_input` -> `branch-review-blocked` |

Clarification caller-return profiles are a closed set. The selected producer edge fixes both the profile and the
return target; no `return_stage`, generic frame or router-authored default crosses the boundary:

| Clarification profile | Producer | Exact `requirements_current` return |
| --- | --- | --- |
| `change_readiness_scope` | `guru-review-change-request` | `guru-review-change-request:clarification_reentry` |
| `task_planning_revision` | `guru-plan-task` | `guru-plan-task:requirements_reentry` |
| `plan_approval_scope` | `guru-approve-task-plan` | `guru-plan-task:approval_scope_reentry` |
| `task_commit_scope` | `guru-create-task-commit` | `guru-create-task-commit:scope_reentry` |
| `base_reconciliation_scope` | `guru-reconcile-task-base` | `guru-reconcile-task-base:scope_reentry` |
| `branch_review_scope` | `guru-review-branch` | `guru-review-branch:scope_reentry` |
| `delivery_readiness_scope` | `guru-review-delivery-readiness` | `guru-review-delivery-readiness:scope_reentry` |
| `task_acceptance_scope` | `guru-accept-task` | `guru-accept-task:scope_reentry` |

`guru-rdt-current-router` and `guru-architecture-current-router` validate profile/stage and resume only the
declared stage. RDT and Architecture no-impact/aligned/contribution-current use disjoint closed exit-output schemas
under the shared external `ssot_current`/`baseline_current` route. `impact_kind` selects exactly one schema;
`change_path` is forbidden for Architecture no-impact and required for aligned/contribution-current, while
`contribution_ref` is forbidden except for contribution-current. No output contains a nullable union slot.

## 5. Delivery, Finish And Cleanup Skills

| Public Skill / profiles | Mode | Minimal public input | Exit -> minimal output -> unique consumer |
| --- | --- | --- | --- |
| `guru-select-delivery-route` / `select`, `base_reentry` | semantic | select=`task_ref,reviewed_range_ref`; base re-entry=`task_ref,base_result_ref`, whose owner restores and validates the still-current reviewed range | `github_pr` -> `route_ref` binding the reviewed range -> `guru-review-delivery-readiness:github_pr`; `none` -> the same closed route-ref shape -> `guru-review-delivery-readiness:none`; recoverable `blocked` -> `continuation_ref,repair_input` -> `delivery-route-blocked` |
| `guru-review-delivery-readiness` / `github_pr`, `none`, `scope_reentry`, `authority_reentry`, `base_reentry`, five qualification-return profiles | semantic | initial profiles=`task_ref,route_ref`; `route_ref` binds the reviewed range selected by its producer. Scope re-entry=`task_ref,requirements_result_ref,caller_continuation_ref`; authority re-entry=`task_ref,authority_result_ref`; base re-entry=`task_ref,base_result_ref`; qualification returns use the Section 3 closed shapes; this owner restores the exact route/range and live-validates both | `ready` -> `readiness_ref` -> `guru-accept-task`; `implementation_required` -> `finding_refs` -> `guru-implement-task`; `planning_required` -> `finding_refs` -> `guru-plan-task:finding_reentry`; `scope_confirmation_required` -> `scope_ref,caller_continuation_ref` -> `guru-clarify-requirements:delivery_readiness_scope`; `authority_reentry_required` -> `authority_kind,revision_ref` -> `guru-authority-reentry-router`; recoverable `blocked` -> `continuation_ref,repair_input` -> `delivery-readiness-blocked` |
| `guru-accept-task` / `github_pr`, `none`, `scope_reentry`, `authority_reentry` | semantic | initial profiles=`task_ref,readiness_ref`; the ref fixes route and reviewed-range identity. Scope re-entry=`task_ref,requirements_result_ref,caller_continuation_ref`; authority re-entry=`task_ref,authority_result_ref`; this owner restores and live-validates that readiness | profile-specific `accepted`: `github_pr` -> `acceptance_ref` -> `guru-accepted-route-router`; `none` -> `acceptance_ref,delivery_fact_ref` -> same router. `implementation_required` -> `finding_refs` -> `guru-implement-task`; `planning_required` -> `finding_refs` -> `guru-plan-task:finding_reentry`; `scope_confirmation_required` -> `scope_ref,caller_continuation_ref` -> `guru-clarify-requirements:task_acceptance_scope`; `authority_reentry_required` -> `authority_kind,revision_ref` -> `guru-authority-reentry-router`; recoverable `blocked` -> `continuation_ref,repair_input` -> `task-acceptance-blocked` |
| `guru-publish-task-pr` / `push_prepare`, `push_confirmation_reentry`, `push_provider_reentry`, `pr_create_prepare`, `pr_creation_confirmation_reentry`, `pr_provider_reentry` | semantic | push prepare=`task_ref,acceptance_ref`; PR-create prepare=`task_ref,acceptance_ref,published_head_ref`; either confirmation re-entry=`continuation_ref`; either provider re-entry=`continuation_ref,repair_input`. Every continuation fixes exactly one stage plus the bound task/acceptance/remote identity; the owner live-rereads it and never accepts a confirmation/authorization field | Every prepare/confirmation/provider re-entry first rereads its exact live remote state. `push_prepare` emits `branch_published -> acceptance_ref,published_head_ref -> pr_create_prepare` without mutation or confirmation when the bound task HEAD is already current on the target remote branch; otherwise it displays only the exact pending branch-push action and emits `push_confirmation_required -> continuation_ref -> task-branch-push-confirmation-wait`, explicitly excluding PR creation and merge. A current clear affirmative enters only `push_confirmation_reentry`; explicit refusal returns `branch_push_not_executed -> task_ref,acceptance_ref -> task-branch-push-not-executed`. A successful push or a re-entry that observes the exact push already completed emits the same `branch_published`. `pr_create_prepare` independently rereads the exact base/head PR and emits `ready_pr_current -> pr_ref,expected_head_ref -> guru-merge-task-pr` without mutation or confirmation when that PR already exists and is live READY; otherwise it displays only the exact pending PR-creation action and emits `pr_creation_confirmation_required -> continuation_ref -> task-pr-creation-confirmation-wait`, explicitly excluding merge. Its current clear affirmative enters only `pr_creation_confirmation_reentry`; refusal returns `pr_not_published -> task_ref,acceptance_ref,published_head_ref -> task-pr-not-published`. Successful creation or a re-entry that observes the exact PR already READY emits the same `ready_pr_current`. Divergent/mismatched remote branch or PR state never creates a duplicate or repeats an irreversible action: `push_recovery_required` and recoverable `push_blocked` enter only `push_provider_reentry` through their declared owner/stop route; `pr_recovery_required` and recoverable `pr_blocked` enter only `pr_provider_reentry`. Push preparation, reply judgment, refusal, executor and recovery cannot produce or consume the PR-create continuation |
| `guru-merge-task-pr` / `initial`, `provider_reentry` | semantic | initial=`task_ref,pr_ref,expected_head_ref`; provider re-entry=`continuation_ref,repair_input`. The exact Merge owner resolves and live-validates the bound PR/expected-head identity | after live READY/readiness review it displays the exact merge plan and accepts any clear semantic affirmative under `EVO-REQ-081`, without a fixed `合并PR` phrase; `merged` -> `delivery_fact_ref` (including merge identity) -> `guru-resolve-issue-closure`; `pr_not_merged` -> `pr_ref,expected_head_ref` -> `task-pr-not-merged`; `merge_recovery_required` -> `continuation_ref,repair_input` -> same Skill `provider_reentry`; `blocked` -> `continuation_ref,repair_input` -> `task-pr-merge-blocked` |
| `guru-resolve-issue-closure` / `github_pr`, `none`, `provider_reentry` | semantic | initial=`task_ref,delivery_fact_ref`; provider re-entry=`continuation_ref,repair_input`. The Closure owner resolves the original delivery identity from its continuation and rereads live Issue state | read-only current/not-applicable needs no confirmation; when an exact manual closure mutation is required, this owner separately displays it under `EVO-REQ-081` and never reuses merge confirmation; `closure_current` -> `closure_ref` -> `guru-delivery-terminal-router`; `closure_not_applicable` -> `reason_ref` -> same router; `issue_closure_not_applied` -> `task_ref,delivery_fact_ref` -> `issue-closure-not-applied`; `closure_recovery_required` -> `continuation_ref,repair_input` -> same Skill `provider_reentry`; `blocked` -> `continuation_ref,repair_input` -> `issue-closure-blocked` |
| `guru-finalize-task` / `finish`, `finish_reentry` | semantic | finish=`task_ref,delivery_terminal_ref`; finish re-entry=`continuation_ref,repair_input`. The Finish owner resolves and live-validates the bound task/delivery terminal rather than accepting copied originals | it live-reads exact task/archive/history state; if a pending archive/finish/history mutation exists, it owns a separate private plan and `EVO-REQ-081` boundary, then its executor performs only deterministic transitions; `finished` -> `durable_result_ref` -> `guru-clean-task-resources`; `finish_not_executed` -> `task_ref,delivery_terminal_ref` -> `task-finish-not-executed`; `finish_blocked` -> `continuation_ref,repair_input` -> `task-finish-blocked`, whose exact repair resumes `finish_reentry` |
| `guru-clean-task-resources` / `prepare`, `confirmation_reentry`, `cleanup_reentry` | semantic | prepare=`task_ref,durable_result_ref`; confirmation re-entry=`continuation_ref`; cleanup repair re-entry=`continuation_ref,repair_input`. The continuation binds the original task/durable result and current resource-plan identity | the Skill live-reads owned/unrelated/retained resources, authors and reviews its private exact cleanup plan and skips confirmation when deletable owned resources are empty; otherwise `cleanup_confirmation_required` -> `continuation_ref` -> `task-resource-cleanup-confirmation-wait`, whose clear current affirmative enters `confirmation_reentry`, missing confirmation remains waiting and explicit refusal returns `resources_retained`; `cleaned` -> `durable_result_ref` -> `workflow-completed`; `resources_retained` -> `durable_result_ref` -> `workflow-completed`; `blocked` -> `continuation_ref,repair_input` -> `task-resource-cleanup-blocked`, whose exact repair resumes `cleanup_reentry` |

`guru-accepted-route-router` invokes `guru-publish-task-pr:push_prepare` only for `github_pr`; `none` projects its accepted
`delivery_fact_ref` directly to `guru-resolve-issue-closure:none`. Each `acceptance_ref`, `delivery_fact_ref` and
`closure_ref|reason_ref` is a closed chained identity that binds, rather than asks a later router to reconstruct,
the preceding route/result identity. `guru-delivery-terminal-router` creates no durable artifact: from the closure
exit DTO alone it validates that bound route, acceptance and closure result match, deterministically projects the
consumer-minimal `delivery_terminal_ref`, and invokes Finish with that ref. The projection is the sole producer of
Finish's `delivery_terminal_ref`; Cleanup itself is the sole author of its private `resource_plan_ref`.

## 6. Distribution And Stock Skills

| Public Skill / profiles | Mode | Minimal public input | Exit -> minimal output -> unique consumer |
| --- | --- | --- | --- |
| `guru-validate-extension-projection` / `standalone`, `stock_policy_reentry` | semantic | standalone=`candidate_ref,target_ref`; stock-policy re-entry=`policy_ref`, whose closed identity binds the same candidate/target and this standalone projection route. This owner resolves the candidate-declared surface itself | `stock_maintenance_required` -> `candidate_ref,target_ref` -> `guru-maintain-stock-projection:standalone`, and only that fixed child edge may perform standalone policy maintenance; `stock_policy_reentry` freshly validates the complete declared surface after stock current. Only then may `projection_current` -> `candidate_ref` -> `workflow-completed`, or recoverable `projection_validation_blocked` -> `gate_kind,mismatch_refs,continuation_ref,repair_input` -> `projection-validation-blocked`; embedded exits are schema-invalid, and no fifth top-level distribution action is created |
| `guru-validate-extension-projection` / `embedded_clean`, `embedded_migration`, `embedded_release` | semantic | `candidate_ref,target_ref`; profile fixes the selected distribution caller, and this owner resolves the candidate-declared surface itself | only `returned_to_caller` -> `gate_result,finding_refs` -> `guru-embedded-projection-router`; standalone completion/blocked exits are schema-invalid, and every embedded failure remains a caller-owned finding |
| `guru-install-clean-repository` / `application`, `validation`, `action_reentry`, `reentry` | semantic | application=`candidate_ref,target_ref`; validation=`step_ref,continuation_ref` from the same transaction; refusal re-entry=`step_ref,continuation_ref`; blocked re-entry=`step_ref,continuation_ref,repair_input`. The continuation binds candidate/target and the owner rereads them; recovery callers never copy those original fields | each pending external mutation is a separately displayed exact action under `EVO-REQ-081`; `new_contract_current` -> `activation_ref` -> `workflow-completed`; `clean_install_not_executed` -> `step_ref,created_resource_refs,continuation_ref` -> `clean-install-not-executed`, which reports the truthful created/current resources and may project only `step_ref,continuation_ref` to `action_reentry` after a later explicit request to continue; `clean_install_blocked` -> `step_ref,created_resource_refs,continuation_ref,repair_input` -> `clean-install-blocked`, whose repair projects `step_ref,continuation_ref,repair_input` to `reentry` |
| `guru-migrate-existing-repository` / `preflight`, five ordered cells, `final_validation`, `action_reentry`, `reentry` | semantic | preflight=`candidate_ref,target_ref`; ordered-cell/final profiles use the transaction's current `step_ref,continuation_ref`; refusal re-entry=`continuation_ref`; blocked re-entry=`continuation_ref,repair_input`. The continuation binds candidate/target, ordered cell and live cutover phase; recovery never reconstructs them from ambient installation state | each pending external mutation is a separately displayed exact action under `EVO-REQ-081`; `new_contract_current` -> `activation_ref` -> `workflow-completed`; `pre_migration_action_not_executed` -> `step_ref,preserved_identity,continuation_ref` -> `migration-pre-cutover-not-executed`; `post_migration_action_not_executed` -> `step_ref,cutover_ref,continuation_ref` -> `migration-post-cutover-not-executed`; either refusal stop consumes its truthful phase display field and may project only `continuation_ref` to `action_reentry` after a later explicit request to continue; `pre_migration_current_preserved` -> `preserved_identity,continuation_ref,repair_input` -> `migration-pre-cutover-blocked`; `migration_blocked` -> `cutover_ref,continuation_ref,repair_input` -> `migration-post-cutover-blocked`; each blocked stop consumes its preservation/cutover display field and projects only `continuation_ref,repair_input` back to `reentry` |
| `guru-release-candidate` / `pre_publish`, `pre_publish_reentry`, `publication`, `publication_reentry_pending`, `publication_reentry_partial`, `publication_reentry_partial_repair`, `post_publish`, `post_publish_reentry` | semantic | pre-publish=`candidate_ref,target_ref`; pre-publish repair=`continuation_ref,repair_input`; publication=`candidate_ref,readiness_ref`; pending/unknown re-entry=`publication_progress_ref,continuation_ref,repair_input`; retryable partial re-entry=`published_partial_ref,continuation_ref`; blocked partial repair re-entry adds `repair_input`; post-publish=`published_ref,continuation_ref`; post-publish repair re-entry=`continuation_ref,repair_input` | `ready_for_confirmation` -> `candidate_ref,readiness_ref` -> `release-confirmation-wait`; terminal refusal `release_not_published` -> `candidate_ref` -> `workflow-completed`; `publication_current` -> `published_ref,continuation_ref` -> this Skill's `post_publish`; `release_verified` -> `published_ref` -> `workflow-completed`; recoverable `pre_publish_blocked` -> `finding_refs,continuation_ref,repair_input` -> `release-pre-publish-blocked`, whose exact repair enters `pre_publish_reentry`; zero-completed or unknown first-action outcome -> `publication_recovery_required` -> `publication_progress_ref,continuation_ref,repair_input` -> this Skill's pending re-entry; at least one completed and one pending action -> `publication_partial` -> `published_partial_ref,continuation_ref` -> this Skill's partial re-entry; non-retryable zero-completed/unknown -> `publication_pending_blocked` -> `publication_progress_ref,continuation_ref,repair_input` -> `release-publication-blocked`; non-retryable partial -> `publication_partial_blocked` -> `published_partial_ref,continuation_ref,repair_input` -> the same stop, whose exact repair enters `publication_reentry_partial_repair`; `post_publish_blocked` -> `published_ref,step_ref,continuation_ref,repair_input` -> `release-post-publish-blocked`, whose exact repair projects only `continuation_ref,repair_input` to `post_publish_reentry`; terminal `published_unverified` -> `published_ref,defect_refs` -> `release-published-unverified` |
| `guru-maintain-stock-projection` / `standalone`, `standalone_action_reentry`, `standalone_suppression_reentry`, `standalone_provider_reentry` | semantic | standalone=`candidate_ref,target_ref`, with the fixed caller `guru-validate-extension-projection:standalone`; action re-entry=`continuation_ref`; suppression/provider repair=`continuation_ref,repair_input`, with the selected profile fixed by the blocked exit. The stock owner resolves the selected `action_set_ref` and bound candidate/target from its current policy/continuation sections rather than requiring a caller replay | `stock_policy_current` -> `policy_ref`, whose identity binds candidate/target and the fixed standalone projection route -> `guru-validate-extension-projection:stock_policy_reentry`; it never completes the top-level invocation itself. `stock_policy_action_required`/`stock_policy_action_partial`/`stock_policy_action_unknown` each -> `continuation_ref` -> same Skill `standalone_action_reentry`, while the owner-private continuation binds exact pending/completed/unknown actions and file/context/sidecar state; a pending mutation uses `EVO-REQ-081`, with refusal `stock_policy_action_not_executed` -> `completed_action_refs,pending_action_refs,unknown_action_refs,continuation_ref` -> `stock-policy-action-not-executed`, which may project only `continuation_ref` to `standalone_action_reentry` after a later explicit request to continue; recoverable `upstream_suppression_blocked` -> `asset_refs,continuation_ref,repair_input` -> `stock-suppression-maintenance-blocked`; recoverable `provider_boundary_blocked` -> `asset_refs,continuation_ref,repair_input` -> `stock-provider-maintenance-blocked`; embedded/retained exits are schema-invalid |
| `guru-maintain-stock-projection` / nine closed `retained_host_r01..r09` profiles, `retained_host_reentry` | semantic | initial=`candidate_ref,target_ref,context_state_ref`; the selected R01..R09 profile fixes `handoff_ref,host_id,projection_cell,context_action` and one exact host-policy/session/workflow-context owner from the retained-host table; repair=`continuation_ref,repair_input` | only `retained_context_current` -> `handoff_ref,context_state_ref` -> that profile's exact host context owner, or recoverable `retained_context_blocked` -> `handoff_ref,continuation_ref,repair_input` -> `retained-context-blocked`; the host context owner alone may provide authorized minimal projections to later Admission/worker/current-owner consumers. Semantic-role and embedded exits are schema-invalid, and no public `caller_id` is accepted |
| `guru-maintain-stock-projection` / `embedded_clean`, `embedded_clean_action_reentry`, `embedded_migration`, `embedded_migration_action_reentry`, `embedded_release`, `embedded_release_action_reentry`, `reapply`, `reapply_action_reentry` | semantic | initial=`candidate_ref,target_ref`; action re-entry=`continuation_ref`; every profile fixes one exact caller, and the stock owner resolves the selected `action_set_ref` from its current policy/continuation section | only `returned_to_caller` with one disjoint schema -> `guru-stock-result-router`: current=`policy_result=current,policy_ref`; all-pending=`policy_result=action_required,action_state_ref,continuation_ref`; completed+pending=`policy_result=action_partial,action_state_ref,continuation_ref`; any-unknown=`policy_result=action_unknown,action_state_ref,continuation_ref`; explicit refusal=`policy_result=action_not_executed,action_state_ref,continuation_ref`; embedded role-local failure=`policy_result=caller_finding,finding_refs`. Fields from every other variant are forbidden. A pending mutation uses `EVO-REQ-081`; the exact caller consumes the selected variant, and only an action-required/partial/unknown or later explicit continuation request may project its `continuation_ref` to the matching profile-fixed `*_action_reentry`. Standalone completion/role-local block/retained exits are schema-invalid, so the caller alone owns its route terminal |

`release-confirmation-wait` owns only the current dialogue pause and applies the shared semantic-confirmation
contract. It never asks for a fixed prompt/password, hash/digest, task/path/branch/SHA/identity/summary repetition,
prescribed wording, `确认执行 <hash>` or lexical `合并PR`. A current clear affirmative enters the same invocation's
`publication` profile directly without emitting or persisting confirmation state; missing confirmation remains in
the wait, explicit refusal returns `release_not_published`, and candidate/decision-relevant-fact drift invalidates
the prior wait and returns to `pre_publish`. AI alone judges the current dialogue; scripts, validators and recorders
never parse, match, validate or persist the reply. Distribution blocked targets expose the exact same-Skill re-entry
and never select a fallback route.

## 7. Thin Router And Terminal Inventory

Routers below are deterministic workflow control-plane functions, not public Skills. The declared producer edge
fixes the validated caller/profile/return owner; no generic invocation frame or public output carries an arbitrary
route string.

| Router | Closed discriminator | Unique projection target |
| --- | --- | --- |
| `invocation-isolation-wait` | `pending_invocation_id,progress_handle,next_event_kind` plus a later matching `progress_event_id` | `guru-admit-invocation:isolation_reentry`; the pause never carries or interprets a user confirmation |
| `guru-bound-intent-router` | `lifecycle_ref,current_owner_id,bound_event_ref,event_sequence`, where `current_owner_id` is one exact Section 3.1 registry member and `bound_event_ref` binds the new host event identity/session/content | that exact Skill's `lifecycle_intent_reentry`, projecting only `lifecycle_ref,bound_event_ref,event_sequence`; Admission emits `binding_blocked` instead when the registry member is unknown/multiple/stale, and the router never substitutes host history or ambient message lookup for the event ref |
| `guru-current-owner-router` | `lifecycle_ref,current_owner_id`, where `current_owner_id` is one exact Section 3.1 registry member | that exact Skill's `current_work_resume`; Current Work emits `recovery_blocked` instead when the registry member is unknown/multiple/stale |
| `active-lifecycle-remote-convergence-wait` | one of the four Section 3.1 irreversible remote owner ids plus `remote_boundary_ref,continuation_ref` | invoke that exact owner's `remote_disposition_resume`; consume its one `remote_outcome_ref`, then project `remote_outcome_ref,continuation_ref` to `guru-dispose-lifecycle:remote_reentry`. The wait never opens either ref or reads owner-private state |
| `guru-specialist-router` | `wording` or `normal_scenario` | wording review or qualification Skill respectively |
| `guru-specialist-result-router` | selected wording/qualification producer profile plus unchanged `caller_continuation_ref` | wording -> exact `wording_*_reentry`; qualification -> exact `qualification_*_reentry`; standalone success/revision is reported by Route Request before completion. The router never opens the token or accepts an arbitrary caller id |
| `guru-qualification-scope-return-router` | one of the eleven fixed Clarification qualification-scope profiles plus unchanged `caller_continuation_ref` | `qualification_scope_current` -> the original caller's `qualification_scope_reentry`; `qualification_scope_blocked` -> that caller's `qualification_scope_repair`. The router never reads the token, chooses a scope or invokes Qualification directly |
| `guru-task-free-escalation-router` | validated `change_scope_ref,partial_work_ref` escalation | `guru-sync-base:task_free_escalation`, then the closed escalation profiles of Discovery -> Clarification -> Change Readiness -> Workspace; no direct Workspace edge |
| `guru-requirements-current-router` | selected Clarification profile plus that profile's closed output | initial/escalation -> matching Change Readiness profile; each caller-return profile -> the exact target in the closed table above by direct field projection only; unknown profile, missing token/result or caller mismatch blocks |
| `guru-rdt-current-router` | RDT profile/stage/return owner | declared next stage or original caller only; repair/promotion return renames the current `rdt_result_ref` to that caller's `authority_result_ref` |
| `guru-rdt-revision-router` | RDT profile/stage/return owner | exact RDT revision caller only |
| `guru-architecture-current-router` | Architecture stage/return owner plus semantic `revision_owner_kind` when finding | declared next stage, Plan, Implement or original caller only; repair/promotion return renames the current `architecture_result_ref` to that caller's `authority_result_ref`; router never chooses severity/remediation |
| `guru-bootstrap-return-router` | fixed `rdt_request|architecture_request` producer profile plus unchanged `authority_caller_continuation_ref` | the exact originating authority owner's `bootstrap_reentry` only; it passes `authority_identity_refs,authority_caller_continuation_ref` directly and never infers origin from task state, Bootstrap private state or an ambient lookup |
| `guru-authority-reentry-router` | `rdt` or `architecture` | corresponding repository authority owner |
| `guru-base-resume-router` | `resume_target=plan|implement|check|branch_review|delivery_route|delivery_readiness` plus `base_result_ref` from Reconcile | exact matching `base_reentry`; it passes `base_result_ref` directly and never reads a generic frame |
| `guru-post-review-authority-router` | Branch Review outstanding `promotion_kind`, outstanding `projection_kind`, exact applicable promotion refs, variant-specific `code_spec_contribution_ref` and `reviewed_range_ref` | first invoke only selected not-yet-current authority `promotion` profiles, ordered RDT then Architecture when both. Only `promotion_kind=none,projection_kind=none` goes to `guru-select-delivery-route`; this exact pair means all in-range authority contributions are already current or absent and no in-range code-spec contribution is missing from the current projection. `authority_only|with_code_spec` invokes the matching disjoint input of the single `.trellis/spec` owner `guru-bootstrap-repository-ssot:projection_refresh`, selecting/renaming only fields declared by that variant and only after every selected authority is current. Its `spec_projection_ref` is renamed to `authority_result_ref` -> `guru-check-task:authority_reentry`; Check success proceeds through a new Commit and committed full-diff Branch Review. That fresh review compares the still-complete diff with live current identities, emits exact double-none when prior promotion/projection is already current, and reopens only materially drifted work. The router never reruns current promotion/projection and cannot write shared authority prose |
| `guru-accepted-route-router` | `github_pr` or `none` | `github_pr` -> `guru-publish-task-pr:push_prepare`; `none` -> issue-closure-none |
| `guru-delivery-terminal-router` | route/acceptance/closure tuple | deterministic `delivery_terminal_ref` projection -> `guru-finalize-task` only |
| `guru-embedded-projection-router` | `clean`, `migration` or `release` caller | that exact distribution caller only |
| `guru-stock-result-router` | exact embedded clean/migration/release caller, or reapply fixed to Existing Migrator's ordered update/preset-reapply cell, plus one disjoint `policy_result` schema | current/finding/refusal -> that exact caller only; action-required/partial/unknown -> that caller's fixed stock-action edge, which may project only `continuation_ref` to the matching `*_action_reentry`. It rejects fields from another variant, standalone/retained-host output and workflow completion |

### 7.1 Recoverable Block Re-entry Inventory

The following table is the complete ordinary producer-owned block/recovery inventory. Each named stop consumes any
diagnostic fields shown in the producer row to report the exact blocker, but projects only the closed re-entry input
below. The continuation binds the original profile and business input; the owner live-rereads decision-relevant
facts before retrying and never reconstructs input from the stop or ambient state.

| Producer | Recoverable exit -> named stop | Exact owner re-entry profile / complete business input |
| --- | --- | --- |
| `guru-admit-invocation` | `binding_blocked` -> `invocation-binding-blocked` | `binding_reentry` / `continuation_ref,repair_input` |
| `guru-admit-invocation` | `independent_request_isolation_blocked` -> `independent-request-isolation-blocked` | `isolation_repair_reentry` / `continuation_ref,repair_input` |
| `guru-admit-invocation` | `upstream_suppression_blocked` -> `stock-suppression-admission-blocked` | `suppression_reentry` / `continuation_ref,repair_input` |
| `guru-admit-invocation` | `provider_boundary_blocked` -> `stock-provider-admission-blocked` | `provider_boundary_reentry` / `continuation_ref,repair_input` |
| `guru-admit-invocation` | `retained_context_blocked` -> `retained-context-admission-blocked` | `retained_context_reentry` / `continuation_ref,repair_input` |
| `guru-answer-request` | `answer_provider_blocked` -> `direct-answer-provider-blocked` | `provider_reentry` / `continuation_ref,repair_input` |
| `guru-route-request` | `blocked` -> `request-routing-blocked` | `routing_reentry` / `continuation_ref,repair_input` |
| `guru-resolve-current-work` | `recovery_blocked` -> `current-work-recovery-blocked` | `recovery_reentry` / `continuation_ref,repair_input` |
| `guru-dispose-lifecycle` | `blocked` -> `lifecycle-disposition-blocked` | `repair_reentry` / `continuation_ref,repair_input` |
| `guru-query-lifecycle-history` | `blocked` -> `lifecycle-history-blocked` | `recovery_reentry` / `continuation_ref,repair_input` |
| `guru-route-distribution` | `blocked` -> `distribution-routing-blocked` | `routing_reentry` / `continuation_ref,repair_input` |
| `guru-select-workflow-mode` | `blocked` -> `workflow-mode-blocked` | `repair_reentry` / `continuation_ref,repair_input` |
| `guru-execute-task-free-change` | `blocked` -> `task-free-blocked` | `repair_reentry` / `continuation_ref,repair_input` |
| `guru-sync-base` | `blocked` -> `base-sync-blocked` | `repair_reentry` / `continuation_ref,repair_input` |
| `guru-discover-change-context` | `blocked` -> `change-context-blocked` | `repair_reentry` / `continuation_ref,repair_input` |
| `guru-clarify-requirements` | non-qualification `blocked` -> `requirements-clarification-blocked` | `repair_reentry` / `continuation_ref,repair_input` |
| `guru-review-change-request` | `prerequisite_blocked` -> `change-request-prerequisite-blocked` | `prerequisite_reentry` / `continuation_ref,repair_input` |
| `guru-review-change-request` | `resolution_blocked` -> `change-request-resolution-blocked` | `resolution_reentry` / `continuation_ref,repair_input` |
| `guru-create-task-workspace` | `blocked` -> `task-workspace-blocked` | `repair_reentry` / `continuation_ref,repair_input` |
| `guru-maintain-requirements-design-test-ssot` | `blocked` -> `rdt-ssot-blocked` | `blocked_reentry` / `continuation_ref,repair_input` |
| `guru-maintain-architecture-baseline` | `blocked` -> `architecture-baseline-blocked` | `blocked_reentry` / `continuation_ref,repair_input` |
| `guru-bootstrap-repository-ssot` | `blocked` -> `repository-ssot-bootstrap-blocked` | `blocked_reentry` / `task_ref,bootstrap_continuation_ref,repair_input` |
| `guru-plan-task` | `blocked` -> `task-planning-blocked` | `repair_reentry` / `continuation_ref,repair_input` |
| `guru-approve-task-plan` | `blocked` -> `task-plan-approval-blocked` | `repair_reentry` / `continuation_ref,repair_input` |
| `guru-implement-task` | `blocked` -> `task-implementation-blocked` | `repair_reentry` / `continuation_ref,repair_input` |
| `guru-check-task` | `blocked` -> `task-check-blocked` | `repair_reentry` / `continuation_ref,repair_input` |
| `guru-create-task-commit` | `blocked` -> `task-commit-blocked` | `repair_reentry` / `continuation_ref,repair_input` |
| `guru-reconcile-task-base` | `blocked` -> `task-base-reconciliation-blocked` | `repair_reentry` / `continuation_ref,repair_input` |
| `guru-review-branch` | `blocked` -> `branch-review-blocked` | `repair_reentry` / `continuation_ref,repair_input` |
| `guru-select-delivery-route` | `blocked` -> `delivery-route-blocked` | `repair_reentry` / `continuation_ref,repair_input` |
| `guru-review-delivery-readiness` | `blocked` -> `delivery-readiness-blocked` | `repair_reentry` / `continuation_ref,repair_input` |
| `guru-accept-task` | `blocked` -> `task-acceptance-blocked` | `repair_reentry` / `continuation_ref,repair_input` |
| `guru-publish-task-pr` | `push_recovery_required` -> owner re-entry; `push_blocked` -> `task-branch-push-blocked` | `push_provider_reentry` / `continuation_ref,repair_input` |
| `guru-publish-task-pr` | `pr_recovery_required` -> owner re-entry; `pr_blocked` -> `task-pr-publication-blocked` | `pr_provider_reentry` / `continuation_ref,repair_input` |
| `guru-merge-task-pr` | `merge_recovery_required|blocked` -> owner re-entry or `task-pr-merge-blocked` | `provider_reentry` / `continuation_ref,repair_input` |
| `guru-resolve-issue-closure` | `closure_recovery_required|blocked` -> owner re-entry or `issue-closure-blocked` | `provider_reentry` / `continuation_ref,repair_input` |
| `guru-finalize-task` | `finish_blocked` -> `task-finish-blocked` | `finish_reentry` / `continuation_ref,repair_input` |
| `guru-clean-task-resources` | `blocked` -> `task-resource-cleanup-blocked` | `cleanup_reentry` / `continuation_ref,repair_input` |
| `guru-validate-extension-projection` | standalone `projection_validation_blocked` -> `projection-validation-blocked` | `standalone_reentry` / `continuation_ref,repair_input` |
| `guru-install-clean-repository` | `clean_install_blocked` -> `clean-install-blocked` | `reentry` / `step_ref,continuation_ref,repair_input` |
| `guru-migrate-existing-repository` | `pre_migration_current_preserved|migration_blocked` -> phase-specific migration block | `reentry` / `continuation_ref,repair_input` |
| `guru-release-candidate` | `pre_publish_blocked` -> `release-pre-publish-blocked` | `pre_publish_reentry` / `continuation_ref,repair_input` |
| `guru-release-candidate` | `publication_recovery_required|publication_pending_blocked` -> owner re-entry or `release-publication-blocked` | `publication_reentry_pending` / `publication_progress_ref,continuation_ref,repair_input` |
| `guru-release-candidate` | retryable `publication_partial` -> owner re-entry | `publication_reentry_partial` / `published_partial_ref,continuation_ref` |
| `guru-release-candidate` | `publication_partial_blocked` -> `release-publication-blocked` | `publication_reentry_partial_repair` / `published_partial_ref,continuation_ref,repair_input` |
| `guru-release-candidate` | `post_publish_blocked` -> `release-post-publish-blocked` | `post_publish_reentry` / `continuation_ref,repair_input` |
| `guru-maintain-stock-projection` | standalone `upstream_suppression_blocked` -> `stock-suppression-maintenance-blocked` | `standalone_suppression_reentry` / `continuation_ref,repair_input` |
| `guru-maintain-stock-projection` | standalone `provider_boundary_blocked` -> `stock-provider-maintenance-blocked` | `standalone_provider_reentry` / `continuation_ref,repair_input` |
| `guru-maintain-stock-projection` | retained `retained_context_blocked` -> `retained-context-blocked` | `retained_host_reentry` / `continuation_ref,repair_input` |

Wording and qualification blocked returns are intentionally absent from this table because Section 3 returns the
original caller-owned token and the original caller performs the repair/reinvocation. Bootstrap's
`repair_required` and stock action-required/partial/unknown results are non-blocked same-owner transitions declared
in their primary rows. `direct-answer-binding-blocked` and `release-published-unverified` terminate the current
invocation; later correction begins a new invocation and therefore receives no continuation.

`workflow-completed`, `release-published-unverified`, all named `*-blocked` targets and the named
`*-not-executed|*-not-created|*-not-published|*-not-merged|*-not-applied` targets are explicit workflow
terminals/pauses, not hidden Skills. A Section 7.1 block retains producer Skill/profile plus its declared repair
input and can re-enter only that producer; Section 3 specialist blocks instead return only to their original caller,
and the two declared terminal blocks have no re-entry. A refusal target records only objective unchanged/current
resource state and its exact owner or declared re-entry identity; it contains no reply or authorization field and
cannot be reclassified as a blocked provider/contract defect. `invocation-isolation-wait` is a progress-event pause;
`active-lifecycle-remote-convergence-wait` is a closed remote-outcome observer that preserves only the Disposition
continuation while the exact registered remote owner converges;
`workflow-mode-choice-wait`, `requirements-scope-retarget-wait`, `task-plan-activation-wait`,
`release-confirmation-wait`, `active-lifecycle-cleanup-confirmation-wait`,
`task-branch-push-confirmation-wait`, `task-pr-creation-confirmation-wait`,
`task-resource-cleanup-confirmation-wait` and `active-lifecycle-disposition-choice-wait` are dialogue-local pauses
owned by their exact Skills. None persists authorization. The first two consume one current product choice; plan,
Release and the two cleanup waits consume an AI-judged semantic confirmation for exactly their displayed action;
the disposition-choice wait consumes only one current retain/suspend product choice and never authorizes cleanup.
Plan approval is one AI semantic review followed by at most one compound activation/implementation-entry confirmation,
not a second approval or a second routine implementation-entry confirmation. The displayed plan names the task-status
transition and the approved implementation scope/allowed writes, and explicitly excludes all later delivery actions.
Missing confirmation waits, refusal keeps the task in planning and completes the invocation, and plan/authority
drift discards the private approval checkpoint before fresh review. `phase-1-task-activation` is the deterministic
substep inside `guru-approve-task-plan` only after current confirmation; it is not a router, public result or terminal.
Only its current transition permits `approved -> guru-implement-task:initial`, while objective transition failure
uses the Approval owner's Section 7.1 block. Unknown,
multiple or frame-mismatched router input fails closed before any downstream action.

## 8. Private Envelope And Provider Contracts

| Envelope section | Created/read by | Direct consumers | Invalidation |
| --- | --- | --- | --- |
| `request` | admission | route and answer owners | request identity/scope change |
| `lifecycle_binding` | admission/current-work owner | current owner, disposition, isolation | owner/phase/scope/candidate/arrival change |
| `authority_context` | Clarification owns current requirement-delta/reviewed-design binding; RDT owns repository RDT; Architecture owns baseline/constitution/change contract | RDT impact, Architecture impact, plan, approval, implement, check, review, readiness and acceptance consume only their applicable subprojections plus the same stable bound authority content | material requirement/authority/scope change |
| `stock_policy_context` | stock owner | admission guard and stock-touching distribution/provider caller | package/projection/file/context/sidecar change |
| `provider_context` | exact action/provider caller | Sync; task-free or standard local write; Commit; branch Publish; PR Publish; Merge; Closure; clean Install; existing Migration; Stock/Reapply; Release; controlled adapters, each only under its closed action profile | target/action/contract/live outcome change |
| `implementation_context` | task-free or standard implementation owner | exactly one implementation owner and its caller-bound worker | plan/scope/spec/authority change |
| `dependency_versions` | section owners | freshness checkers only | dependency identity change |
| `continuation` | current pending/blocked owner | exactly one re-entry owner | consumed, superseded or terminal |

Each section owner is the only live full reader for its source family. Applicable authority content remains the same
call-local stable prefix for every semantic consumer that must judge it; this is not a producer summary or public DTO.
A public edge or deterministic provider consumer asks the owner runtime only for the row's minimal projection, never
reads the envelope file or repeats the same full source read. Equivalent identity drift refreshes the owner projection
without replaying unchanged semantic review; dependency/material-fact change re-enters the earliest owning section for
a targeted live reread and invalidates only its downstream projections.

`provider_context` contains one closed `provider_action_contract` per exact external action. This private carrier is
owned by the action caller and contains all `EVO-REQ-039` dimensions, never user authorization:

Every profile carries the common fields
`provider_kind,source_owner,contract_locator,contract_version,caller_scope_ref,target_ref,action_id,input_identity,
input_field_semantics,output_receipt_semantics,effective_boundary,permission_model,rate_quota_semantics,
error_semantics,partial_success_semantics,unknown_outcome_semantics,idempotency_or_equivalent_repeat_key,
live_state_read_entry,retry_preconditions,stop_conditions,max_safe_automatic_retries`. It then selects exactly one
closed action row; fields from another row are rejected rather than treated as optional:

| Provider family | Closed action profiles | Required variant fields | Exact owner |
| --- | --- | --- | --- |
| Git | `base_sync`, `local_write`, `task_commit`, `task_push` | base sync=`selected_base_ref,authority_checkout_ref,base_before_ref,base_after_ref`; local write=`checkout_ref,changed_path_refs,write_result_ref`; commit=`selected_commit_ref,diff_ref,commit_result_ref`; push=`remote_ref,expected_head_ref,push_result_ref` | Sync, task-free/implementation, Commit, or PR Publication owner fixed by profile |
| GitHub | `pr_publish`, `pr_merge`, `issue_closure_read`, `issue_closure_write` | all require `repository_ref,remote_ref,target_kind,target_identity,remote_state_ref`; PR/merge add `expected_head_ref`; closure read adds `closure_result_ref`; closure write adds `close_scope_ref,closure_preimage_ref,closure_result_ref` | exact Publish, Merge, or Closure owner fixed by profile |
| Trellis upstream | `init`, `upgrade`, `update`, `workflow_switch` | `package_ref,template_or_registry_ref,source_identity,command_ref,flag_profile,stdout_semantics,exit_code_semantics`; update additionally requires `update_discriminator=migration_required|migration_not_required`; workflow switch additionally requires `preview_result_ref,cutover_ref` | Clean-install or Existing-migration owner |
| Guru preset | `install`, `stock_reapply`, `activation_validate` | install=`preset_identity,ownership_contract_identity,projection_cell_refs`; reapply=`preset_identity,ownership_contract_identity,stock_policy_identity,projection_cell_refs,sidecar_state_refs`; activation validation=`preset_identity,ownership_contract_identity,stock_policy_identity,projection_cell_refs,sidecar_state_refs,activation_manifest_ref` | Clean-install, Existing-migration, or exact Reapply caller |
| Release | `pre_publish_read`, `tag_publish`, `release_record_publish`, `tag_pinned_verify` | immutable `candidate_ref`; pre-publish adds `readiness_ref`; tag publish adds `tag_ref`; release record adds `tag_ref,release_ref`; verification adds `published_ref,verification_target_ref` | `guru-release-candidate` exact stage only |

One atomic action records only `action_state=completed|pending|unknown`. `partial` is never a single-action value:
the owner derives aggregate `action_required` only when every action is pending, `action_partial` only from a
completed+pending set, and `action_unknown` when any action is unknown, with priority
`unknown > partial > action_required`. The outcome also carries
`last_live_state_ref,completed_action_refs,pending_action_refs,unknown_action_refs,error_class,retry_class,
continuation_ref,unverified_boundaries`; terminal rejection is a non-retryable pending/blocked disposition, not a
fourth action state. The action owner updates this private state only after live reread. Public exits project only
the minimal result/continuation fields already declared above; no consumer receives the full provider contract.

Envelope default is process-local. Cross-turn isolation/provider/recovery writes only
`.trellis/.runtime/guru-team/invocations/<invocation-id>.json`; current consumer completion, stale replacement or
terminal deletes it and empty directories. A public consumer resolves only its authorized projection through the
owner runtime, never the envelope file.

Controlled provider contracts are private caller adapters, not auto-discoverable Skills:

| Adapter identity | Closed profiles | Required binding | Success result / minimal return shape | Evidence locator / result owner |
| --- | --- | --- | --- | --- |
| `guru-channel-transport-adapter-1.0` | request/re-entry pair for exactly `answer`, `discovery`, `task_free`, `standard_implementation`, `phase2_check` | profile-fixed caller, handle, scope, provider source | `transport_current -> transport_result_ref,handle_ref,unverified_boundaries` | caller-owned `transport_evidence_ref`; caller fixed by the selected profile |
| `guru-session-memory-read-adapter-1.0` | `standalone_answer` plus embedded `discovery|requirements|planning|task_free|implementation|check|branch_review` | profile-fixed caller, query scope, source identity | `history_observation_current -> observation_ref,unverified_boundaries` | caller-owned `history_evidence_ref`; caller fixed by the selected profile |
| `guru-diagnostic-read-adapter-1.0` | `standalone_answer` plus embedded `discovery|requirements|planning|task_free|implementation|check|branch_review` | profile-fixed caller, diagnostic scope, source identity | `diagnostic_observation_current -> diagnosis_ref,recommendation_refs,unverified_boundaries` | caller-owned `diagnostic_evidence_ref`; caller fixed by the selected profile |
| `guru-trellis-reference-read-adapter-1.0` | `standalone_answer` plus embedded `discovery|requirements|planning|task_free|implementation|check|branch_review` | profile-fixed caller, reference scope, `guru-trellis-reference-manifest-1.0` identity and selected official-doc/local-runtime/package-snapshot locator | `trellis_reference_observation_current -> reference_fact_refs,source_identity,unverified_boundaries` | caller-owned `trellis_reference_evidence_ref`; caller fixed by the selected profile |
| `guru-research-worker-adapter-1.0` | `discovery_research` | `guru-discover-change-context`, source/scope/candidate | `research_observation_current -> observation_refs,unverified_boundaries` | Discovery-owned `research_evidence_ref`; Discovery only |
| `guru-platform-implementation-worker-adapter-1.0` | `task_free`, `standard_phase2` | exact platform worker source plus exactly one implementation owner, scope/candidate/allowed writes | `implementation_worker_current -> changed_path_refs,validation_evidence_ref,unverified_boundaries` | owner-local `implementation_evidence_ref`; exact task-free or `guru-implement-task` caller |
| `guru-channel-implementation-worker-adapter-1.0` | `task_free`, `standard_phase2` | exact channel transport/source plus exactly one spawning implementation owner, scope/candidate/allowed writes | `implementation_worker_current -> changed_path_refs,validation_evidence_ref,transport_result_ref,unverified_boundaries` | owner-local `implementation_evidence_ref`; exact spawning task-free or `guru-implement-task` caller |
| `guru-check-worker-adapter-1.0` | `platform_phase2_check`, `channel_phase2_check` | `guru-check-task`, candidate/scope/source | `check_observation_current -> check_evidence_ref,unverified_boundaries` | Check-owned `check_evidence_ref`; `guru-check-task` only |

The preset transaction is the only writer of `guru-trellis-reference-manifest-1.0`. Its closed source precedence is
official Trellis documentation for extension semantics, the target repository's current local runtime files for
installed behavior, and the pinned package snapshot only for shipped-template/package facts. Each selected locator
binds source kind, identity and current/unverified status. The reference adapter reads that manifest lazily for its
profile-fixed caller; it never dispatches raw `trellis-meta`, edits a bundled Skill, chooses a customization route or
accepts write intent. Standalone read-only reference requests return to
`guru-answer-request:trellis_reference`; embedded requests return only to their listed caller. A request to change
workflow/preset/overlay/spec/product facts is classified before adapter invocation and enters the active owner or a
new Guru change lifecycle.

Every adapter returns exactly its profile's success result or
`provider_boundary_blocked -> binding_or_provider_fact_refs,repair_input` synchronously to the exact
profile-fixed caller: transport returns to its selected caller; standalone history/diagnosis returns to
`guru-answer-request`; embedded history/diagnosis/reference returns to the bound active caller; standalone reference
also returns to `guru-answer-request:trellis_reference`; research returns to
`guru-discover-change-context`; implementation returns to the exact task-free or `guru-implement-task` caller; and
check returns to `guru-check-task`. No adapter returns to a generic role-local block or asks a router to infer the
caller, and no adapter result carries a public `caller_ref`. The caller either repairs within its current semantic
step or emits its own Section 7.1 block; in particular, Answer promotes the adapter block to
`answer_provider_blocked` and returns only through `provider_reentry`. That caller's repair re-entry may reinvoke only
the same fixed adapter profile. The evidence ref identifies caller-owned live/process-local evidence and is consumed by that caller; it is
not a shared report or handoff file.
Adapters never ask a product question, assign finding severity, decide pass, change phase or persist a handoff.

## 9. Closure Rules

1. Every external exit above has exactly one named consumer/router/stop; routers validate profile and perform only
   a thin deterministic projection. A bound event reaches one of the 37 registered lifecycle owners only with
   `bound_event_ref,event_sequence`; the two specialist Skills leave lifecycle ownership with their fixed original
   caller. Standalone stock maintenance is produced only by the standalone Projection owner and returns current only
   to its `stock_policy_reentry`. Exact-current Workspace reuse returns only
   `workspace_current -> guru-maintain-requirements-design-test-ssot:task_impact_sync`, with plan display,
   confirmation wait, refusal branch and mutation all zero; only pending creation, transfer or isolation enters the
   Workspace confirmation graph. Plan activation becomes `approved` only after the owner-local deterministic
   transition, under the already displayed compound activation/implementation-entry plan, and then has
   `guru-implement-task:initial` as its sole consumer.
2. Unknown, multiple, unmapped, stale or consumer-mismatched output fails closed.
3. A semantic Skill completes positive behavior and AI gate before recorder/validator. A deterministic Skill has
   no semantic choice or human confirmation inside its boundary.
4. Re-entry reuses current envelope sections and reruns only affected semantic work; a new independent request gets
   a new envelope and exactly one admission receipt. Semantic owners that need repository authority consume the same
   stable bound content view; minimal DTO projection never substitutes a producer summary for that authority.
5. The old `guru-review-task-publication` and standalone `guru-verify-extension-installation` shapes are replaced by
   delivery-readiness and route-specific projection/install/migration/Release owners. Current `guru-finalize-task`
   provider/publication behavior is split into publish, merge, closure, Finish and Cleanup owners. Migration must
   prove zero legacy consumer before activation.
