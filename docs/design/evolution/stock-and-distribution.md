# Evolution Stock And Distribution Design

状态：`design_ready_for_delivery_planning` / `fresh_design_review_passed` / `evolution_refactor_eligible`。本文件已承接
`EVO-REQ-052..056,068..083`中适用的distribution/stock边界：17个official Trellis stock asset的selected
action不变，installed manifest额外作为Publish immutable extension-source binding authority，standalone
Projection拥有evidence-before-cleanup verifier failure lifecycle。它不表示任何stock文件已经被patch、隔离
或删除。

## 1. Source And Policy Ownership

- stock source：`@mindfoldhq/trellis@0.6.15`，registry integrity
  `sha512-grbF8PToesHojsaWkoG4+Aupih7eZHkXH5y33uzPrWQXwIRewwlM1AoeJEttcXAia9nLZzF/ezuR338PWCKv+A==`，
  capture tarball SHA-256
  `7b97e4247f54e71f22ff80caa328d9e68fb81908f984f15d70a4d81cc2a0306c`。
- source owner：official Trellis collector/template package。Guru 不修改 source checkout、全局 npm、
  package cache、`node_modules` 或 package tarball。
- policy owner：`guru-maintain-stock-projection`。canonical policy 位于 target
  `trellis/presets/guru-team/stock-policy/`；installed provenance 只写
  `.trellis/guru-team/extension.json` 的 closed `stock_projection` domain。
- standalone policy caller：`guru-validate-extension-projection:standalone`。它只在已选
  standalone-projection route中产生`stock_maintenance_required`；Stock current以绑定同一candidate/target的
  `policy_ref`只返回Projection的`stock_policy_reentry`并触发fresh完整surface验证，不直接完成workflow，也不
  新增第五个distribution action。
- projection owner：Guru preset transaction。它只在 official projection 后处理 exact selected
  host/path；workflow、Skill 或 hook 不自行删除或改写 stock。
- Trellis reference manifest owner：Guru preset transaction单写`guru-trellis-reference-manifest-1.0`；
  reference callers只通过`guru-trellis-reference-read-adapter-1.0`懒读取选定locator，不写manifest或调用raw
  `trellis-meta`。
- code-spec projection owner：`guru-bootstrap-repository-ssot:projection_refresh`单写
  `guru-code-spec-projection-1.0`；只有reviewed range相对live target identity仍有outstanding
  `authority_only|with_code_spec`工作且所有selected RDT/Architecture promotion current后可运行；target
  projection已精确current时无写入返回，fresh complete-diff review收敛到double-none，
  preset/stock owner只验证successor reachability，不代写`.trellis/spec`。
- ownership handoff：current schema/contract 3.0 禁止 Guru claim、patch 或 delete official `trellis-*`
  paths。future preset transaction 必须先在 Guru namespace 安装并验证
  `guru-extension-ownership-contract-4.0`、schema、validator 与 exact post-projection policy claim；只有该
  handoff current 后才能执行本文件选定的 mutation。它不取得 upstream source ownership，也不提前激活
  target workflow；handoff 前 stock mutation count 为 0。
- admission owner：`guru-admit-invocation` 只读 current policy，识别 collision 并 redirect/block；
  admission fixture 不执行 maintenance mutation。
- installed publication handoff：installer仍是installation manifest source provenance的唯一writer；
  `guru-publish-task-pr:provenance_prepare`只读该immutable repo/ref/full-commit与managed-byte identity，建立独立
  extension source checkout，并把apply target固定为业务reviewed checkout。Publish不得把target HEAD反写成
  source或fallback到self-hosted；Finish不得读取verifier state。
- standalone verifier boundary：`guru-validate-extension-projection:standalone|standalone_reentry`在runner
  failure后先绑定stage/cell/command/exit/bounded safe tail/hash-size private evidence，再允许temporary cleanup。
  matrix外failure为`postcheck_failure`；embedded clean/migration/Release只接收caller-owned finding。

选定 action family 恰好三种：`managed_absence`、`managed_quarantine`、
`caller_bound_replacement`。九项 semantic route 选择 absence，是因为 patch 仍留下第二个自然语言
matcher，quarantine 对无 provider capability 的 asset 增加无价值维护面，而 exact managed absence
在 Guru successor current、pinned provenance 与用户修改保护成立时维护成本最低。

## 2. Seventeen-Asset Decision Table

`shared+hosts` 表示 shared `.agents/skills` layer 只计一次，同时覆盖 Codex、Claude、Cursor 的
declared projection cell；具体 emitted/not-emitted 状态仍由 host matrix 验证。

| Asset / source locator | Role | Selected action | Target carrier / expected file state | Guru capability successor or adapter | Successful guard/result consumer | Blocked result |
| --- | --- | --- | --- | --- | --- | --- |
| `trellis-start` / `common/commands/start.md` | suppressed | `managed_absence` | shared+host discoverable projection cells absent; policy row retained | `guru-admit-invocation -> guru-route-request -> guru-select-workflow-mode` | `guru-admit-invocation:request_admitted -> guru-route-request:top_level` | `upstream_suppression_blocked` |
| `trellis-continue` / `common/commands/continue.md` | suppressed | `managed_absence` | shared+host discoverable projection cells absent; policy row retained | `guru-resolve-current-work` plus the Section 3.1 current-owner registry | `guru-admit-invocation:request_admitted -> guru-route-request:top_level` | `upstream_suppression_blocked` |
| `trellis-finish-work` / `common/commands/finish-work.md` | suppressed | `managed_absence` | shared+host discoverable projection cells absent; policy row retained | exact Draft/READY PR -> `guru-finalize-task:github_pr`; accepted none route -> `guru-finalize-task:none` | `guru-admit-invocation:request_admitted -> guru-route-request:top_level` | `upstream_suppression_blocked` |
| `trellis-brainstorm` / `common/skills/brainstorm.md` | suppressed | `managed_absence` | shared+host discoverable projection cells absent; policy row retained | `guru-clarify-requirements` | `guru-admit-invocation:request_admitted -> guru-route-request:top_level` | `upstream_suppression_blocked` |
| common `trellis-check` / `common/skills/check.md` | suppressed | `managed_absence` | shared+host discoverable projection cells absent; policy row retained | `guru-check-task` | `guru-admit-invocation:request_admitted -> guru-route-request:top_level` | `upstream_suppression_blocked` |
| `trellis-spec-bootstrap` / bundled skill | suppressed | `managed_absence` | shared+host discoverable projection cells absent; policy row retained | `guru-bootstrap-repository-ssot` | `guru-admit-invocation:request_admitted -> guru-route-request:top_level` | `upstream_suppression_blocked` |
| `trellis-update-spec` / `common/skills/update-spec.md` | suppressed | `managed_absence` | shared+host discoverable projection cells absent; policy row retained | outstanding-only `guru-bootstrap-repository-ssot:projection_refresh` -> `guru-code-spec-projection-1.0` -> fresh Check/Commit/Branch Review -> already-current double-none | `guru-admit-invocation:request_admitted -> guru-route-request:top_level` | `upstream_suppression_blocked` |
| `trellis-before-dev` / `common/skills/before-dev.md` | suppressed | `managed_absence` | shared+host discoverable projection cells absent; policy row retained | envelope-derived `implementation_context` | `guru-admit-invocation:request_admitted -> guru-route-request:top_level` | `upstream_suppression_blocked` |
| `trellis-meta` / bundled skill | suppressed | `managed_absence` | shared+host discoverable projection cells absent; policy row retained | `guru-trellis-reference-manifest-1.0` + caller-fixed `guru-trellis-reference-read-adapter-1.0`; write intent uses active/new-change route | `guru-admit-invocation:request_admitted -> guru-route-request:top_level` | `upstream_suppression_blocked` |
| `trellis-channel` / bundled skill | provider | `managed_quarantine` | `.trellis/guru-team/stock-providers/trellis-channel/` non-discoverable source | `guru-channel-transport-adapter-1.0` | exact spawning Guru caller | `provider_boundary_blocked` |
| `trellis-session-insight` / bundled skill | explicit | `managed_quarantine` | `.trellis/guru-team/stock-providers/trellis-session-insight/` non-discoverable source | `guru-session-memory-read-adapter-1.0` | standalone direct-answer or exact embedded caller | `provider_boundary_blocked` |
| `trellis-break-loop` / `common/skills/break-loop.md` | explicit | `managed_quarantine` | `.trellis/guru-team/stock-providers/trellis-break-loop/` non-discoverable source | `guru-diagnostic-read-adapter-1.0` | standalone direct-answer or exact embedded caller | `provider_boundary_blocked` |
| platform `trellis-research` | worker | `caller_bound_replacement` | Guru host agent projection with `discovery_research` profile | `guru-research-worker-adapter-1.0` | `guru-discover-change-context` | `provider_boundary_blocked` |
| platform `trellis-implement` | worker | `caller_bound_replacement` | Guru host agent projection with `task_free|standard_phase2` profiles | `guru-platform-implementation-worker-adapter-1.0` | exactly one task-free/standard implementation owner | `provider_boundary_blocked` |
| platform `trellis-check` | worker | `caller_bound_replacement` | Guru host agent projection with `platform_phase2_check` profile | `guru-check-worker-adapter-1.0` | `guru-check-task` | `provider_boundary_blocked` |
| channel `check` / `trellis/agents/check.md` | worker | `caller_bound_replacement` | Guru channel worker projection with `channel_phase2_check` profile | `guru-check-worker-adapter-1.0` with channel transport | spawning `guru-check-task` | `provider_boundary_blocked` |
| channel `implement` / `trellis/agents/implement.md` | worker | `caller_bound_replacement` | Guru channel worker projection with `task_free|standard_phase2` profiles | `guru-channel-implementation-worker-adapter-1.0` with channel transport | exactly one spawning implementation owner | `provider_boundary_blocked` |

Closure count is fixed at `suppressed=9`, `provider=1`, `explicit=2`, `worker=5`. Quarantined source is
non-discoverable reference/provider material, never a Skill registry row, auto-match surface or alternate semantic
route. A diagnostic follow-up that requests writes is reclassified before the raw provider is invoked.

For every suppressed row, the capability successor column describes behavior after route selection; it is not the
consumer of suppression success. The pre-semantic guard has exactly one successful edge for all nine rows:
`request_admitted -> guru-route-request:top_level`. Route Request then selects the successor route. A suppressed row
cannot bypass that edge and directly call its eventual capability owner.

The two removed write-capable surfaces have independent positive successor proofs. For `trellis-update-spec`,
reachability means either current authority locator/usage/freshness needs an `authority_only` repair (including
`promotion_kind=none` when shared authority is already current) or one same-range reviewed `with_code_spec`
contribution is still missing from current projection, with every selected outstanding RDT/Architecture promotion current,
`guru-bootstrap-repository-ssot:projection_refresh` as the sole `.trellis/spec` writer, and
`spec_projection_ref -> guru-check-task:authority_reentry -> fresh Commit -> fresh Branch Review -> exact double-none`
after the projection target is already current; a raw Skill result cannot satisfy any edge. For `trellis-meta`,
reachability means the preset-written reference manifest, exact source
precedence, standalone Answer plus seven embedded caller profiles on the private reference adapter, and a separate
active/new-change route for all writes. Natural-language mention, exact raw Skill selection and post-update
reprojection all preserve these boundaries; neither successor becomes a tenth discoverable semantic surface.

Blocked consumers are closed by invocation profile. Admission-time suppressed/provider collisions go only to
`stock-suppression-admission-blocked` / `stock-provider-admission-blocked`. Standalone maintenance sends
`upstream_suppression_blocked` only to `stock-suppression-maintenance-blocked` and
`provider_boundary_blocked` only to `stock-provider-maintenance-blocked`. Embedded maintenance returns one
`returned_to_caller` result to its exact clean/migration/Release/reapply caller. Controlled adapters return
`provider_boundary_blocked` synchronously to the caller fixed by their concrete profile; that caller either repairs
inside its current step or emits its own public recoverable block and later reinvokes the same adapter profile. No
adapter output carries a generic `caller_ref`, uses a generic “role-local block” or asks a router to infer the caller.

The standalone maintenance caller is not implicit: Projection alone enters the Stock standalone profile, and only a
current Stock result returns to Projection's `stock_policy_reentry`; neither role-local block nor Stock current may
skip that route-local caller and complete the invocation.

## 3. Projection And File-State Algorithm

For each selected host and asset, policy evaluation binds
`package/version/integrity/capture/source_locator/projection_cell/role/selected_action/carrier_kind/carrier_locator/
expected_file_state/successor` and separately classifies `file_state`, `context_state`, and `sidecar_state`.
`selected_action` is validated against the role-specific action enum; carrier fields only identify the expected
file/projection location and cannot imply, replace or broaden the action.

1. `managed_absence` may remove only a byte-equal pinned template or a previous-managed identity, and only after
   the successor registry/interface/projection is current and reachable.
2. `managed_quarantine` first copies the pinned source tree to
   `.trellis/guru-team/stock-providers/<asset>/`, verifies the caller adapter, then removes the discoverable
   projection under the same preset transaction.
3. `caller_bound_replacement` projects a Guru-owned worker definition containing caller/profile/scope/
   candidate/allowed-write/result bindings, then removes the raw worker from dispatch inventory.
4. User-edited, unowned, unknown-source, mixed-version or identity-mismatched targets are preserved in place.
   Existing `.new`/`.bak` is also preserved. The action returns the role-local blocked result and exact repair input.
5. Missing source target is not automatically success: policy still proves successor reachability, expected
   managed absence/quarantine/replacement, and no unresolved sidecar.
6. One atomic action state is exactly `completed`, `pending`, or `unknown`. `partial` exists only at the action-set
   aggregate when at least one action is completed and at least one remains pending; aggregate priority is
   `unknown > partial > action_required`. Re-entry live-reads the exact asset and executes only a pending action whose
   provider contract proves safe repetition; it never replays a completed mutation.
7. Before any pending mutation, the stock owner displays that next exact asset/target/action and applies
   `EVO-REQ-081`. Explicit refusal keeps every action state truthful and returns
   `stock_policy_action_not_executed` with the same stock-owner continuation in standalone mode or
   `returned_to_caller(policy_result=action_not_executed)` in embedded/reapply mode; it is not a policy defect.
   A later explicit request to continue may use only that continuation to enter `standalone_action_reentry`; the
   owner live-rereads the action set and never replays a completed mutation.

`stock_policy_current` requires all applicable rows current, all successors reachable, no raw discoverable semantic
route/worker, no unresolved sidecar and one activation candidate. A suppressed successor mismatch is a
capability-preservation/consistency finding, not the narrower capability-loss gate.

In standalone distribution, this result is not terminal. Its `policy_ref` binds the selected candidate/target and is
consumed only by `guru-validate-extension-projection:stock_policy_reentry`; the Projection owner then reruns both
capability-loss and consistency/installation gates before it may emit `projection_current`.

## 4. Retained Nonsemantic Rows

These rows are outside the 17-role count. `guru-maintain-stock-projection` owns the host-policy action;
`guru-admit-invocation` or the exact caller consumes only the projected context.

| Handoff | Host surface | Selected action | Direct consumer | Blocked condition |
| --- | --- | --- | --- | --- |
| `STOCK-HANDOFF-R01` | Codex official hooks | `context_preserve` | `codex-hook-policy-context-owner` | hook identity/config/approval/context unsafe |
| `STOCK-HANDOFF-R02` | Claude official hooks | `context_preserve` | `claude-hook-policy-context-owner` | same host-local condition |
| `STOCK-HANDOFF-R03` | Cursor official hooks | `context_preserve` | `cursor-hook-policy-context-owner` | same host-local condition |
| `STOCK-HANDOFF-R04` | Codex session/native context | `context_reconcile` | `codex-session-context-owner` | session/source/context mismatch |
| `STOCK-HANDOFF-R05` | Claude session/native context | `context_reconcile` | `claude-session-context-owner` | session/source/context mismatch |
| `STOCK-HANDOFF-R06` | Cursor session/native context | `context_reconcile` | `cursor-session-context-owner` | session/source/context mismatch |
| `STOCK-HANDOFF-R07` | Codex workflow breadcrumb | `context_reconcile` | `codex-workflow-breadcrumb-context-owner` | workflow/phase marker mismatch |
| `STOCK-HANDOFF-R08` | Claude workflow breadcrumb | `context_reconcile` | `claude-workflow-breadcrumb-context-owner` | workflow/phase marker mismatch |
| `STOCK-HANDOFF-R09` | Cursor workflow breadcrumb | `context_reconcile` | `cursor-workflow-breadcrumb-context-owner` | workflow/phase marker mismatch |

Every row uses one closed `guru-maintain-stock-projection:retained_host_r01..r09` profile. The selected profile fixes
`handoff_ref,host_id,projection_cell,context_action` and its exact direct consumer; public input is only
`candidate_ref,target_ref,context_state_ref`, with no caller-authored `caller_id`. It returns only
`retained_context_current -> handoff_ref,context_state_ref` to that profile's consumer or
`retained_context_blocked -> handoff_ref,continuation_ref,repair_input` to the retained-host pause. The pause
projects only `continuation_ref,repair_input` to `retained_host_reentry`. It never selects intent, scope, finding,
route or side effect. Passive startup/session/sub-agent/channel context is not a user request and cannot create an
invocation receipt.

Each direct consumer above is the single host-local owner of that retained result. Hook-policy owners may project
only a current `host_event_guard_ref` to Admission or a `worker_host_context_ref` to the exact profile-fixed worker
adapter. Session owners may project only `host_session_context_ref` to Admission. Workflow-breadcrumb owners may
project only `current_owner_binding_ref` to Admission's lifecycle-binding substep. Those later callers never consume
`retained_context_current` directly, and no one context owner may stand in for another host or context class.

## 5. Host And Setup Partition

- Shared `.agents/skills` is one projection layer, not three copies in inventory.
- Supported hosts are exactly Codex, Claude and Cursor. Each has main/default/inline, sub-agent, channel and native
  applicability; a non-emitted common asset is still checked against policy rather than counted as suppressed.
- Every concrete host fixture binds the five independently observed setup facts
  `user_feature_flag`, `project_hook_config`, `one_time_approval`, `emission`, and `context_injection`, then selects
  exactly one of the seven Requirements-owned setup discriminators below. The high-level labels
  `hooks-enabled`, `hooks-disabled`, and `no-hook` are derived views, not another matrix axis.

| Setup discriminator | Bound setup facts | Design result |
| --- | --- | --- |
| `enabled_approved` | feature=`on`; config=`present`; approval=`granted`, or `not_applicable` only for a host with no approval surface; observed emission/context retained separately | evaluate the role-local redirect/quarantine/fail-closed boundary; hook filtering or injection alone never proves suppression |
| `enabled_pending` | feature=`on`; config=`present`; approval=`pending`; only for a host with an approval surface; observed emission/context retained | remain role-local blocked unless pre-semantic isolation is current; never reinterpret pending as disabled or suppressed |
| `enabled_denied` | feature=`on`; config=`present`; approval=`denied`; only for a host with an approval surface; observed emission/context retained | remain role-local blocked unless pre-semantic isolation is current; never reinterpret denial as disabled or suppressed |
| `feature_off_config_present` | feature=`off`; config=`present`; actual approval or `not_applicable`; observed emission/context retained | derive `hooks-disabled`; any emitted surface or injected context still passes the exact role policy |
| `feature_on_config_absent` | feature=`on`; config=`absent`; approval=`not_applicable` or the actual readable state; observed emission/context retained | derive `no-hook`; config absence does not prove a discoverable surface is absent or safe |
| `feature_off_config_absent` | feature=`off`; config=`absent`; approval=`not_applicable` or the actual readable state; observed emission/context retained | derive `no-hook`; both absences still require the exact role policy |
| `configuration_unknown` | at least one setup fact is unknown/unreadable or the observed emission/context contradicts the setup | stop before semantic behavior with the exact role-local blocked result and re-enter only after setup repair |

For hosts without an approval surface, `enabled_pending` and `enabled_denied` are N/A;
`enabled_approved` records `one_time_approval=not_applicable` rather than inventing a grant. Missing configuration,
feature-off, not-emitted state and absent context are observations, not selected suppression actions.
- Hook-filtered `trellis-start`, hook absence and disabled hooks do not prove semantic collision closure.

## 6. Distribution State And Atomic Activation

`guru-route-distribution` first consumes one state classification:

| State | Predicate | Only route |
| --- | --- | --- |
| `clean_target` | no active workflow and no attributable official Trellis/Guru managed footprint | clean install |
| `existing_migration_target` | uniquely attributable official footprint, current/partial/legacy Guru state, or identified non-Guru workflow with current safe transition plan | existing migration |
| `foreign_workflow` | non-Guru workflow without current identity/provenance/owner/transition plan | blocked preclassification |
| `distribution_state_blocked` | mixed, unknown, unowned or multiple identity | clarification/live repair, then preclassification |

The new contract becomes callable only when `guru-extension-activation-manifest-1.0` binds the same candidate for
workflow, Skill registry/interfaces, runtime, stock policy, provider/worker definitions and all selected host
projections. Before activation, target consumer count is zero. After activation, legacy consumer count is zero.
There is no per-host partial activation, runtime selector, fallback or old/new dual-read.

## 7. Clean Install

`guru-install-clean-repository` owns one ordered transaction:

1. prove `clean_target` and pin source/candidate/target;
2. run official Trellis init/projection;
3. install target Guru contract/preset sources, the reference manifest/adapter, code-spec projection contract and
   ownership contract/schema/validator in the Guru namespace;
4. validate ownership 4.0 and its exact post-projection claims, then execute stock policy for shared and selected
   host cells;
5. build and validate one activation manifest binding ownership, reference and code-spec projection identities;
6. validate capability preservation, Skill/exit/consumer closure, modes, executable bits, sidecar zero and
   installed provenance, including the immutable source identity later consumed by publication preparation;
7. activate and return `new_contract_current`.

Any step finding returns `clean_install_blocked` with created resources and exact re-entry. It cannot switch to
migration after side effects; wrong preclassification is detected before step 2.

## 8. Existing Migration

`guru-migrate-existing-repository` creates one composite context and evaluates exactly these ordered cells:

| Cell | Application boundary | Current result |
| --- | --- | --- |
| `MIG-CELL-INSTALL` | preservation-mode official install/backfill | applied current or reasoned N/A |
| `MIG-CELL-UPGRADE` | official CLI/package upgrade | applied current or reasoned N/A |
| `MIG-CELL-UPDATE` | run `trellis update --dry-run`; output containing `MIGRATION REQUIRED` selects only `trellis update --migrate --skip-all`, otherwise only `trellis update --skip-all`; `--force`/`--create-new` are separate controls | selected branch applied current or reasoned N/A |
| `MIG-CELL-WORKFLOW-SWITCH` | preview `--create-new`, preflight, then explicit `--force` | unique cutover current |
| `MIG-CELL-PRESET-REAPPLY` | Guru preset + stock policy reapply | post-cutover projection current |

At entry it inventories active/resumable work, archive/Finish/history, retained refs, RDT/Architecture authority,
reference manifest/code-spec projection identity, user modifications and sidecars. Each cell owns applicability,
provider discriminator, target, side effects and
re-entry. Before the first selected stock mutation, the transaction also installs and validates ownership contract
4.0/schema/validator and records its exact policy claim; current ownership 3.0 never authorizes that mutation. All
N/A still reaches one final validation.

The only cutover is the explicit workflow force write, or byte-equal current observed only after the fixed order
reaches the workflow-switch boundary. Invocation-entry equality never skips or reclassifies earlier cells.
Pre-cutover finding returns `pre_migration_current_preserved`; post-cutover finding forward-recovers through
preset reapply and final validation or returns `migration_blocked`. Final validation proves preservation,
history/ref reachability, target graph uniqueness and legacy consumer absence before activation.

## 9. Update, Reapply And Release

- Official init/update/upgrade may regenerate stock paths. Completion of that provider command is only an input to
  `guru-maintain-stock-projection:reapply`, not proof that policy is current. This profile's caller is fixed to
  `guru-migrate-existing-repository`'s ordered UPDATE/PRESET-REAPPLY cell; it is not a standalone or inferred caller.
- Reapply reconstructs the exact inventory, preserves user files/sidecars, executes only selected actions, then
  revalidates activation, reference-manifest and code-spec-projection identities. It may verify or restore the preset
  manifest, but it cannot run code-spec promotion or write `.trellis/spec` on behalf of Bootstrap. Unknown upstream
  version/action remains blocked; it is never silently adopted.
- Standalone projection validation completes only with its own current/blocked exits. Embedded projection and stock
  validation return only `returned_to_caller` to clean, migration, Release or reapply; they cannot acquire a
  standalone or caller terminal. When standalone validation selects policy maintenance, Projection is the fixed
  Stock caller and Stock current returns only to Projection revalidation; Stock has no independent top-level terminal.
- Standalone Projection failure is not a Finish or embedded-distribution result. Pre-matrix/matrix/post-matrix failure
  binds non-null verifier-private evidence before temporary cleanup; the named Projection block may expose its
  `failure_ref` for diagnosis and projects only continuation/repair back to `standalone_reentry`. Raw stdout/stderr,
  full verifier lifecycle and authorization never enter public/durable state.
- Release binds an immutable candidate and executes pre-publish, the shared `EVO-DES-069` dialogue-local semantic
  confirmation boundary, publication and tag-pinned post-publish stages. A clear affirmative after the unchanged
  exact plan enters publication directly; missing confirmation waits, refusal returns `release_not_published`, and
  candidate/fact drift returns to pre-publish. No fixed prompt/password/hash/digest/task/path/branch/SHA/identity/
  summary/prescribed-wording challenge or scripted reply parser is accepted as a gate. A published semantic defect
  is `published_unverified`; remediation is a new invocation/candidate, never a fallback to the legacy contract.
  Before any publication action is known completed, pending/unknown recovery uses `publication_progress_ref` and
  its own re-entry/block schema; `published_partial_ref` is legal only after at least one action is confirmed
  completed and another remains pending. Neither state is synthesized from the other.
- Clean install and migration apply the same boundary to each pending external mutation. Refusal returns
  `clean_install_not_executed`, `pre_migration_action_not_executed` with preserved current identity, or
  `post_migration_action_not_executed` with the real cutover identity; every result carries its current
  step/resource/continuation and never guesses success, discards partial state or changes the selected distribution
  action.

Full three-host clean/existing/update/reapply/exact-candidate proof belongs only to the final dedicated matrix and
Release slices in [`delivery-plan.md`](./delivery-plan.md). Ordinary implementation slices run their declared
targeted cells and report the remainder as an unverified boundary.
