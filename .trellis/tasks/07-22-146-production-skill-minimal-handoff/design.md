# #146 技术设计：production Skills 最小 typed handoff 原子迁移

## 1. 设计原则

1. 三个 production Skills 构成一个 `production-minimal-handoff-v1` activation unit，禁止
   producer 与 consumer 分批切换形成 mixed graph。
2. Interface 1.3 只暴露 caller-owned semantic input、exact invocation、per-exit output、
   consumer projection 与 consumer 确实验证的最小 identity；private artifacts 不进入 DTO。
3. Workflow 只拥有 mandatory invocation、typed-exit routing 与 stop；三个 Skills 继续拥有
   现有 semantic closed loop、AI Review Gate 与 confirmation boundary。
4. Runtime 读取 live Git/GitHub/Trellis/task facts并生成 candidate、projection、digest 与
   path metadata；Agent 不填写 runtime-derived 字段，也不读取 private runtime source。
5. #144/#145/#147 的已交付合同是本次实现基线；本任务只新增三包 migration、9/35
   closure，以及已确认的 Stage 0 disposition、clarify_scope router、task-local owner/worktree
   binding 与 formal snapshot replacement 修复。
6. Canonical、installed、dogfood、四平台、throwaway、update/reapply 必须通过同一 closure
   定义。
7. 三条 semantic Skill handoff 使用 target-owned `skill_input_authoring_seed`：producer
   只提供 minimal seed，caller AI只提供 fresh authoring，两者确定性无覆盖合并后验证
   target profile；runtime 不代写 semantic judgment。

## 2. 所有权与路径

| Owner | Canonical path | 本任务中的职责 |
| --- | --- | --- |
| Production packages | `trellis/skills/guru-team/packages/<skill>/` | Interface、public schemas/examples/wrapper、private artifact declarations、eval corpus |
| Production migration manifest | `trellis/skills/guru-team/migrations/production-minimal-handoff.json` | 3×11 set、profile/output/consumer/projection/case bindings、activation version |
| Production manifest schema | `trellis/skills/guru-team/schemas/production-migration-manifest.schema.json` | Closed manifest shape 与 schema identity |
| Interface schema | `trellis/skills/guru-team/schemas/skill-interface-1.3.schema.json` | Additive `skill_input_authoring_seed` shape、field partition 与 exact target refs |
| Active closure validator | `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` | 合并 live registry、两个 manifests、Interfaces 与 corpora，验证 9×35 closure |
| Registry | `trellis/skills/guru-team/registry.json` | Active lifecycle、Interface id、I/O state、workflow route |
| Extension | `trellis/guru-team-extension.json` | Public schema inventories、migration manifests、active/minimal ids、managed commands/assets |
| Workflow | `trellis/workflows/guru-team/workflow.md` | Mandatory markers 与唯一 consumers，不复制 package 内部步骤 |
| Shared runtime | `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` | Public dispatch、live-fact derivation、candidate builder、projection、deterministic validation |
| Context discovery package | `trellis/skills/guru-team/packages/guru-discover-change-context/` | task-local owner locator、private worktree state、formal snapshot replacement schema/tests |
| Preset | `trellis/presets/guru-team/` | One-transaction distribution、installed inventory、update/reapply/throwaway verification |
| Installed copies | `.trellis/guru-team/skills/` 与 selected platform Skill roots | Canonical bytes 的安装结果，不是长期 source |

Production manifest schema 存在真实消费者：source/installed validator、preset installer、
throwaway verifier、closure tests 与 eval coverage tests 均读取它。

## 3. Exact production graph

| Producer exit | 唯一 consumer | Kind |
| --- | --- | --- |
| `guru-approve-task-plan:approved` | `phase-1-task-activation` | Workflow |
| `guru-approve-task-plan:revision_required` | `guru-approve-task-plan:revision_reentry` | Skill |
| `guru-approve-task-plan:clarify_scope` | `guru-task-plan-clarify-scope-router` | Workflow |
| `guru-approve-task-plan:blocked` | `task-plan-approval-blocked` | Stop |
| `guru-check-task:passed` | `guru-create-task-commit:initial_commit` | Skill |
| `guru-check-task:implementation_required` | `guru-resume-implementation` | Workflow |
| `guru-check-task:planning_stale` | `guru-task-check-planning-router` | Workflow |
| `guru-check-task:blocked` | `task-check-blocked` | Stop |
| `guru-create-task-commit:committed` | `branch-review-or-finding-closure` | Workflow |
| `guru-create-task-commit:revision-required` | `guru-create-task-commit:revision_reentry` | Skill |
| `guru-create-task-commit:blocked` | `task-commit-blocked` | Stop |

Workflow markers、Interface `external_exits`、registry routes、production manifest 与
consumer contracts 必须通过双向 set equality。`revision_required` 与 `revision-required`
是两个现存 API id，validator 必须按字节区分。

## 4. Public input profiles

### 4.1 Profile inventory

| Skill | Profile id | Route family | Caller-owned payload |
| --- | --- | --- | --- |
| `guru-approve-task-plan` | `initial_review` | 首次 planning review，workflow/standalone | `mode`、`task_ref`、`authority_refs`、provenance review、adequacy review、unusual-scenario dispositions、confirmation、AI Gate、`exit_intent` |
| `guru-approve-task-plan` | `revision_reentry` | task-local revision 后完整复审 | 上述 semantic input + `reentry_reason=task_local_revision`；不得携带旧 approval artifact body |
| `guru-approve-task-plan` | `clarification_reentry` | authority/scope owner 返回后完整复审 | 上述 semantic input + current authority refs + `reentry_reason=authority_refreshed` |
| `guru-check-task` | `initial_check` | 实现完成后的全量 Phase 2 | `mode`、`task_ref`、scope dispositions、adequacy review、findings、unverified conclusions、evidence locators、AI Gate、`exit_intent` |
| `guru-check-task` | `finding_fix_rerun` | finding 修复后的全量复跑 | 上述 semantic input + closed prior finding refs + `rerun_reason=finding_fix` |
| `guru-check-task` | `planning_reentry` | planning/authority 刷新后的全量检查 | 上述 semantic input + `rerun_reason=planning_refreshed` |
| `guru-create-task-commit` | `initial_commit` | 首次 task work commit | `mode`、`task_ref`、message intent、path authorizations、semantic review、human authorization、`exit_intent` |
| `guru-create-task-commit` | `revision_reentry` | candidate 可修订后重建 | 上述 semantic input + `reentry_reason=candidate_revision`；不得携带旧 plan body |
| `guru-create-task-commit` | `finding_fix_commit` | finding fix 完成 fresh Phase 2 后新 commit | 上述 semantic input + `commit_intent=finding_fix` |
| `guru-create-task-commit` | `recovery_resume` | 受支持的 transaction recovery | 上述 semantic input + closed `recovery_intent`；runtime 按 `task_ref` 定位 private checkpoint |

每个 aggregate schema 必须使用 `profile` discriminator、closed `oneOf` 与
`additionalProperties:false`。`mode` 使用 `workflow|standalone` closed enum；mode 只改变
caller route，不改变 entry preconditions 或 semantic Gate。

### 4.2 Input field policy

- `task_ref` 使用 repo-relative task locator，不使用本机绝对路径。
- `authority_refs` 与 `evidence_locators` 只传 consumer/runtime 可验证的 stable locators；
  issue content、file content、hash、size、mtime、HEAD、dirty snapshot 与 command output
  由 runtime 重读。
- Semantic arrays 只含 AI judgments 与其最小 locators：provenance classification、scope
  disposition、adequacy status、finding conclusion、unverified conclusion、confirmation 与
  route intent。
- Input example 必须覆盖每个 profile 的必填字段、closed enum 与互斥组合；invocation probe
  必须调用 package public wrapper，不得直接调用 private runtime function。
- Wrapper 先验证 input schema，再调用 owner recorder/checker/builder route，最终只输出一个
  declared typed-exit DTO。

## 5. Per-exit outputs 与 consumer projections

### 5.1 最小 output shapes

| Exit | Public DTO | Consumer 直接用途 |
| --- | --- | --- |
| `approved` | `exit_id`、`task_ref`、`approval_ref` | Activation 以 task locator + opaque current approval identity 执行 `task.py start` 前置校验 |
| `revision_required` | `exit_id`、`task_ref` | Self-reentry 选择 `revision_reentry` 并重读已修改 planning docs |
| `clarify_scope` | `exit_id`、`task_ref`、`proposal_refs` | Routing-only workflow target 建立 active task/proposal context，再 mandatory invoke requirements owner |
| planning `blocked` | `exit_id` | Stop route |
| `passed` | `exit_id`、`task_ref`、`checked_head`、`check_ref` | Commit builder 定位 task、验证 Phase 2 identity 与 ancestor/dirty contract |
| `implementation_required` | `exit_id`、`task_ref`、`finding_refs` | Workflow 返回实现并绑定 current-scope findings |
| `planning_stale` | `exit_id`、`task_ref`、`planning_route`、`proposal_refs` | Router 只按 `reapprove_plan|clarify_requirements` 选择唯一 owner |
| check `blocked` | `exit_id` | Stop route |
| `committed` | `exit_id`、`task_ref`、`base_ref`、`committed_head` | #131 input 直接消费；`task_ref` 定位 scope，`committed_head` 绑定 commit/freshness |
| `revision-required` | `exit_id`、`task_ref` | Self-reentry 选择 `revision_reentry` 并由 runtime 重建 candidate |
| commit `blocked` | `exit_id` | Stop route |

`approval_ref` 与 `check_ref` 是 opaque current identities，只在 consumer 实际执行 freshness
校验时存在；它们不得编码 private artifact body、review metadata 或 audit history。

### 5.2 Consumer contracts

- Skill consumer input 由目标 package 拥有；producer projection exact-ref target interface
  与 profile id。
- Workflow consumer contract 由 workflow route 拥有，只声明 route 完成所需字段。
- `guru-task-plan-clarify-scope-router` 精确接收 `exit_id`、`task_ref`、`proposal_refs`，只把
  scope context交给 caller AI，并 mandatory invoke existing
  `guru-clarify-requirements:active_task_scope_change`。Router、projection 与 runtime 均不构造
  该 target profile 的八个 AI/route-owned fields。
- 当前 `branch-review-or-finding-closure` workflow consumer拥有
  `task_ref`/`base_ref`/`committed_head` input shape，并按现有 route进入 Branch Review。
  该 shape 与 #131 已确认 public input完全兼容；#131 激活时由 #131 的独立 migration把
  workflow route替换为 active Skill invocation，不修改本次 committed DTO。
- Stop consumers 使用 `select` + empty mappings；完整 blocker 与 remediation 留在 private
  gate evidence 和用户可见 AI 说明中。

### 5.3 Projection policy

- `direct`：producer output 与 consumer input shape 字节一致。
- `select`：只选择 consumer schema 声明字段；stop 选择空 payload。
- `rename`：只处理 stable producer/consumer field naming 差异。
- `normalize`：只使用 #144 已发布的 closed normalizer ids。
- Projection validator 必须拒绝 private schema path、未知 operation、未知 property、无消费
  output property、consumer 缺失、schema mismatch 与 private artifact lookup。

### 5.4 Target-owned authoring-seed contract

只有下列三条 edge 使用 `consumer_inputs[].contract.kind=skill_input_authoring_seed`：

| Producer edge | Target profile | `seed_fields` | `authoring_fields` |
| --- | --- | --- | --- |
| `guru-approve-task-plan:revision_required` | `guru-approve-task-plan:revision_reentry` | `source_exit`、`task_ref` | target profile `required` 减去 seed fields 的全部 fresh semantic fields |
| `guru-check-task:passed` | `guru-create-task-commit:initial_commit` | `source_exit`、`task_ref`、`checked_head`、`check_ref` | target profile `required` 减去 seed fields 的全部 fresh message/path/review/authorization fields |
| `guru-create-task-commit:revision-required` | `guru-create-task-commit:revision_reentry` | `source_exit`、`task_ref` | target profile `required` 减去 seed fields 的全部 fresh semantic/re-entry fields |

`exit_id` 通过现有 `rename` mapping 形成 `source_exit`；producer output 的现有 property
是其它 seed fields 的唯一来源。Target package 为每个上述 profile 发布独立 authoring
example，且该 example 的 top-level keys 必须精确覆盖 `authoring_fields`。

Source/installed validator 与 public invocation probe 执行同一算法：

```text
required = target_profile_schema.required
require seed_fields intersect authoring_fields == empty
require seed_fields union authoring_fields == required
seed = apply_existing_projection(output_example)
authoring = validate_exact_authoring_example(target_package)
require keys(seed) == seed_fields
require keys(authoring) == authoring_fields
merged = no_overwrite_merge(seed, authoring)
validate merged against complete target profile schema
```

该算法只验证结构和确定性 projection，不生成 `authoring_fields`、不读取 producer private
artifact、不使用 runtime defaults、不改变 route。`direct|select|rename|normalize` 仍是完整
projection operation set；`skill_input_authoring_seed` 是 consumer contract kind，不是第五种
operation。所有其它 `skill_input`、workflow input 与 stop input 保持原行为。

## 6. Private artifacts 与 deterministic boundary

| Skill | Private owner state | Kind | Persistence |
| --- | --- | --- | --- |
| `guru-approve-task-plan` | `planning-approval.json`、完整 provenance/adequacy/scenario/Gate evidence | `gate_evidence` | `task_local_tracked` |
| `guru-check-task` | `phase2-check.json`、完整 command/worker/agent/finding/full-round evidence | `gate_evidence` | `task_local_tracked` |
| `guru-create-task-commit` | `task-commit-plans/*.json`、candidate/result、Git snapshots、transaction/recovery state | `runtime_checkpoint` + `gate_evidence` | `task_local_tracked` 与 transaction temp state |

Runtime 可使用 `task_ref` 读取并验证上表 state，但 public output 与 consumer projection
不得包含其完整内容。Active schemas 保持当前 schema ids；Interface 迁移不重写 artifact
schema 语义，也不修改 archive bytes。

## 7. Commit candidate builder 与 transaction

### 7.1 Builder pipeline

```text
public semantic input + task_ref
  -> runtime 重读 task/planning/Docs SSOT/Phase 2/ledger/Git state
  -> AI-owned path authorizations 与 semantic review shape validation
  -> deterministic snapshot materialization
  -> exact candidate JSON serialization + digest
  -> existing candidate validator
  -> existing isolated-index executor
  -> one typed exit DTO
```

Builder 输出是 private candidate，不是 public DTO。Builder 不决定 path scope、message
adequacy、deployment/safety impact、confirmation sufficiency 或 typed route。

### 7.2 Preserved transaction invariants

- 每个 dirty path 精确分类一次；unrelated paths 保持未 stage、未修改。
- Regular file、executable、symlink、delete、rename、copy 与 gitlink 使用现有 exact
  SHA/mode/object authority。
- `copied_from` 不授予 source staging/deletion authority；dirty source 需要独立 classification。
- Hook 在 isolated transaction 中执行；hook mutation、unexpected index/worktree drift、
  operation-state mismatch 与 postcondition mismatch 必须失败关闭。
- Ref/index/candidate publish 与 rollback 继续使用现有实现；本任务不得替换 transaction
  算法，也不得加入锁、TOCTOU、crash consistency 或跨 OS 扩展。
- Commit message 使用中文 Conventional Commit 与 `Refs #146`；close keyword 只进入 PR body。

### 7.3 Re-entry 与 recovery

- `revision_reentry` 根据 current public semantic input与 live task state创建新 sequence。
- `finding_fix_commit` 必须消费 fresh `guru-check-task:passed` DTO，并绑定新 Phase 2 identity。
- `recovery_resume` 只选择现有 contract 支持的 deterministic recovery action；runtime 按
  `task_ref` 定位 checkpoint并复验，public input不复制 journal。
- Unknown/stale sequence、HEAD drift、dirty snapshot drift 或 unsupported recovery 必须输出
  `blocked`，不得猜测修复。

## 8. Production manifest 与 9/35 closure

### 8.1 Manifest shape

`production-minimal-handoff.json` 顶层固定：

- `schema_id=guru-team-production-migration-manifest-1.0`；
- `activation_unit_id=production-minimal-handoff-v1`；
- required Interface 1.3、registry 1.1 与 eval 1.0 schema ids；
- exact 3 Skill ids；
- 每个 Skill 的 profile ids、11 exit bindings、output schema/example ids、consumer input ids、
  projection ids、private artifact ids 与 eval case ids；
- `activation_policy=preset_transaction`；只有 transaction 验证失败且 versioned adapter
  已被当前 authority 纳入范围时，才使用 adapter path。

Stage 0 manifest 保持 `stage0-minimal-handoff-v1` 原内容与 6×24 set。两个 manifests 不得
合并成破坏 #145 activation identity 的单一文件。

### 8.2 Closure algorithm

Validator 读取 live canonical registry，而不是硬编码 9 个 ids：

```text
active = registry entries where state == active
stage0 = exact skills/exits from stage0-minimal-handoff-v1
production = exact skills/exits from production-minimal-handoff-v1
new = active entries already at Interface 1.3 + minimal_handoff and absent from both manifests

require active.ids == stage0.ids union production.ids union new.ids
require every active Interface exit set == manifest/newly-active exit set
require every active profile and exit has current eval binding
require every bound case exists in one canonical package corpus
require every selected platform resolves the same corpus bytes
require no active entry has legacy, unknown, or missing I/O state
```

当前 baseline 的 expected cardinality 是 9 Skills / 35 exits。Cardinality 是回归断言；
closure authority 仍来自 live registry + manifests，未来新增 active 1.3 entry 通过 `new`
路径证明完整合约后进入闭包。

### 8.3 Eval data flow

```text
canonical case + fixtures
  -> selected adapter 创建隔离执行 context
  -> AI/human-reviewed owner result
  -> owner recorder/checker 验证 private result
  -> package public wrapper 接收 public input + owner result locator
  -> wrapper 返回 actual typed-exit DTO
  -> runner 按 actual exit 选择 output schema并验证 DTO
  -> grader 比较 expected_exit 并执行 typed assertions
```

`expected_exit` 不进入 wrapper、owner recorder/checker、route selection 或 output schema
selection。`committed` case 的 consumer assertion只验证投影后得到
`task_ref`/`base_ref`/`committed_head`，不运行 #131。

## 9. Stage 0 与 active-task context 修复

### 9.1 Stage 0 disposition projection

`stage0_clarity_disposition()` 的 retained input set 增加正式值
`keep_current_open_issue`，保留当前兼容 aliases。测试必须构造：

1. schema/checker-passed `guru-requirements-clarification-2.0` owner result；
2. `target_disposition.disposition=keep_current_open_issue`；
3. 真实 `invoke-stage0-skill` public wrapper；
4. actual exit `clear`；
5. output `target_disposition=retained`；
6. output schema validation 与 consumer projection pass。

该修复不修改 clarification schema、semantic owner、confirmation、typed exits、grader
policy 或 Stage 0 manifest。

### 9.2 clarify_scope routing-only router

`guru-approve-task-plan:clarify_scope` 的 producer DTO 保持
`exit_id`/`task_ref`/`proposal_refs`，consumer 改为 workflow target
`guru-task-plan-clarify-scope-router`。该 target 的 closed workflow input schema 与 DTO 精确
一致；它只建立 scope context并 mandatory invoke
`guru-clarify-requirements:active_task_scope_change`。Caller AI 随后从 live issue、task、
planning 与 proposal refs 新鲜编写 existing target profile 的完整八字段 input。

该 edge 不使用 `skill_input_authoring_seed`，所以 5.4 的 seed edge cardinality 保持 3；也不
扩大 producer output、不增加 projection operation、不修改 clarification target profile。
Router 的唯一 typed consumer仍是 existing clarification Skill，unknown/multiple/unmapped route
失败关闭。

### 9.3 task-local owner-checker locator binding

Shared public dispatch 在 input schema validation 后，把 validated public input 传给
`stage0_owner_result`。只有当 Skill/profile 精确为
`guru-discover-change-context:task_local_reentry` 时，resolver 才从 input 取 repo-relative
`task_locator` 并传给现有 owner checker；`pre_task` 与其它 Stage 0 profiles继续传
`task=None`。

Checker 同时验证 owner-result locator 与
`task_locator/prior_snapshot_locator`，并沿用现有 regular/path/freshness checks。任何 locator
mismatch、unsafe path 或 stale snapshot 均返回 checked failure；runtime不得从 private
snapshot反向推断 task，也不得为 wrapper复制 snapshot 到 clean checkout。

### 9.4 private task_worktree_state

`guru-discover-change-context` task-mode owner result 与 persisted snapshot 增加 private
`task_worktree_state`：

- `head` 绑定 current task worktree HEAD；
- `entries[]` 按 repo-relative path/status/mode/rename identity稳定排序；
- load-bearing working files记录 working-content SHA-256，deleted entries记录缺失状态；
- `context-discovery.json` 自身在 capture 与 live comparison 中均被同一规则排除；
- aggregate digest由 canonical JSON bytes确定性计算。

AI Gate先审查 dirty scope与每个 load-bearing docs/code/tests内容，再把已审结论交给 recorder。
Recorder/checker只验证 evidence shape、digest与 live task worktree exact equality，不判断 scope
是否足够。新增、删除、内容、status、mode或rename drift均失败关闭。`pre_task`/standalone
继续要求 clean checkout；task mode 不无条件接受 dirty path，也不执行 stash/revert/index/
commit来制造 clean。

### 9.5 formal fixed-snapshot replacement

Task-mode recorder 增加 private CLI 参数
`--expected-prior-snapshot-sha256`。固定 locator仍为
`{TASK_DIR}/context-discovery.json`，replacement transaction为：

```text
read prior fixed snapshot
  -> validate regular + Git-trackable + schema/identity
  -> require prior.snapshot_sha256 == explicit expected prior
validate complete new candidate
  -> structural + live issue/base/blob/content/history
  -> AI Gate evidence + task_worktree_state exact live match
write_json fixed locator
  -> read-back + trackability + identity + live freshness
  -> installed public wrapper returns context_ready
```

任一写前校验失败都不得改变 prior bytes。不同 bytes replacement成功时，新 snapshot的
optional `superseded_snapshot_sha256` 必须与 prior `snapshot_sha256` 相同；initial task write不
要求该字段，历史 snapshot继续按旧 bytes只读。相同 bytes retry沿用现有 idempotent success，
不要求形成自引用 supersession。

Replacement复用现有 `write_json`，不新增 archive/current pointer、delete/copy/rename、stash、
revert、stage、提前 commit、锁、TOCTOU或并发协议。Public input/output/typed exits完全不变。

## 10. Rollout、compatibility 与 rollback

### 10.1 Rollout

1. 更新 durable specs、production manifest schema 与 closure contract。
2. 创建 consumer inputs 和三包 public input/output schemas/examples/interfaces/wrappers。
3. 实现 authoring-seed field partition/no-overwrite merge、deterministic candidate builder、
   production dispatch/projection、clarify_scope router、task-local context binding 与 formal
   snapshot replacement。
4. 添加三份 corpora、production manifest、9/35 closure tests。
5. 原子更新 registry、extension inventory、workflow markers 与 preset transaction。
6. 同步 canonical 到 installed/dogfood/selected platform copies并处理 sidecars。
7. 执行 source/installed、unit/integration/eval、clean throwaway、pre-migration upgrade、
   `trellis update`、preset reapply 与 drift gates。

### 10.2 Compatibility

- Stable Skill/mode/exit/consumer ids、artifact schema ids、semantic Gates、confirmation 与
  transaction semantics 保持不变。
- Existing active state通过 fresh public re-entry重建 DTO；旧 artifact 不转存为 public
  cache。
- Existing Interface 1.3 `skill_input` consumers 与四种 projection operations 保持兼容；
  `skill_input_authoring_seed` 只为 5.4 的三条 edge additive 启用。
- `guru-discover-change-context` 的 public DTO、typed exits、pre-task/standalone clean contract
  保持不变；新增字段只存在于 task-local private snapshot schema。
- 历史 `context-discovery.json` 无 `superseded_snapshot_sha256` 时继续可读；只有 formal
  replacement新快照需要该字段精确绑定 prior。
- Extension 的 current interface id保持1.3；迁移结束后 `legacy_skill_ids=[]`，全部 9 个
  active ids进入 minimal handoff closure。
- Planned #131 consumer只使用 Issue 已确认 input shape；本任务不实现或激活 #131 package。

### 10.3 Rollback

- Canonical source validation失败：停止 preset apply，修订 canonical delta。
- Preset staging或 installed validation失败：保留迁移前完整 graph，修复后整包重跑；禁止
  手工逐包激活。
- Consumer direct-use proof缺失：删除 output property或修订 consumer input，不暴露 private
  artifact。
- Eval/closure失败：保持 registry entries为 legacy，直到 3×11 与 9×35 全部通过。
- Stable API、semantic owner、#147 policy、#131 internal behavior 或 product scope 需要变化：
  停止实现并进入 Scope Change Gate，不在当前计划内静默修改。
- Snapshot replacement任一 structural/live/worktree check失败：保持 prior bytes并返回
  deterministic blocked result，不删除、改名或复制 fixed snapshot。

### 10.4 Unusual-scenario dispositions

| Candidate class | Trigger evidence | Disposition | Route basis |
| --- | --- | --- | --- |
| `security_or_threat` / `attack_or_malicious_actor` | Source authority明确排除恶意伪造、对抗输入与威胁模型 | `out_of_scope` | 不进入实现、不产生 current finding |
| `toctou_or_concurrency_race` | Source authority明确排除竞态压力、锁与 TOCTOU；现有 commit transaction语义必须保留 | `mechanism_removed` | 不新增加固机制；实现若引入该机制即 revision |
| `fault_injection_or_crash_consistency` | Source authority明确排除额外 fault injection 与 crash consistency | `out_of_scope` | 不进入验收或 required follow-up |
| `cross_os_atomicity` | Source authority明确排除跨 OS 原子性 | `out_of_scope` | 不进入 implementation 或 Branch Review finding |
| `other_nonstandard` | 没有 current authority trigger | `out_of_scope` | 只有未来 exact authority确认后才进入新 scope |

R12-R16 都是在受支持正常路径中复现并经精确 proposal/action confirmation 纳入的
`confirmed_scope_expansion`。其范围分别只包含 5.4 的三条 authoring-seed edge、9.2 的
routing-only edge、9.3 的 owner locator、9.4 的 private worktree evidence 与 9.5 的 formal
replacement。R7 是正常 public wrapper 路径中已复现的 ordinary correctness expansion。
这些修复均不改变上表 unusual classes 的排除结论。

## 11. Docs SSOT Plan

### 11.1 Docs state

`complete_docs`。当前 durable authority：

- `.trellis/spec/workflow/skill-package-contract.md`：Interface、public/private I/O、consumer
  projection、target-owned authoring seed、production package contracts、registry closure；
- `.trellis/spec/workflow/workflow-contract.md`：planning、Phase 2、commit invocation/route；
- `.trellis/spec/workflow/companion-scripts.md`：builder/recorder/validator/executor、task-local
  worktree evidence 与 snapshot replacement boundary；
- `.trellis/spec/workflow/data-contracts.md`：registry、extension、manifest、artifact、eval；
- `.trellis/spec/workflow/quality-guidelines.md`：source/installed/negative/distribution gates；
- `.trellis/spec/preset/installer.md`、`overlay-guidelines.md`、`upstream-ownership.md`：preset、
  managed hashes、update/reapply、ownership；
- `.trellis/spec/docs/public-docs.md`：public docs sync；
- `docs/requirements/README.md`、`docs/requirements/requirement-main.md`、
  `docs/requirements/guru-team-trellis-flow.md`：长期 requirement/flow SSOT；
- `README.md`、`trellis/workflows/guru-team/README.md`、
  `trellis/presets/guru-team/README.md`：公开 install/runtime/eval 指南。

### 11.2 Strategy

Strategy：`ssot_first`。本任务修改团队公共 Skill I/O、activation、eval、upgrade 与 consumer
contracts，durable docs 必须先定义 production migration 与 closure，再修改 runtime/package。

### 11.3 Affected durable docs

实现阶段必须同步 11.1 列出的 workflow/package/data/script/quality/preset/public-doc specs，
requirements/flow SSOT 与三份 README。若实现证明某个列出文件无语义 delta，Phase 2
必须记录该文件的检查证据与 no-change 理由。

### 11.4 Task delta merge checkpoint

Implementation 完成 public schemas、consumer projections、authoring-seed partition/merge、
clarify_scope router、task-local owner/worktree binding、formal replacement、manifest、closure
validator 与 tests 后，implementation agent 必须把最终 field/profile ids、validation
commands、upgrade 结果与 compatibility decision 合并到 durable docs，再
交给 `guru-check-task`。Phase 2 不得用 task-local `design.md` 替代 durable docs。当前已存在
的 16-file `ssot_first` predecessor diff 必须保留，并在 implementation restart 前补齐 R12
合同；不得把该 predecessor diff 当作 authoring-seed 已实现证据。

### 11.5 Task-history-only content

Issue intake digests、Phase 0 evidence、planning approval、agent liveness、command raw output
digests、review rounds 与 PR readiness 只保留在 task artifacts；这些内容不进入 durable
SSOT。

### 11.6 Reconciliation evidence

Implementation handoff 必须列出：strategy、updated durable paths、task delta merge结果、
task-history-only 内容、no-change/follow-up 结论、durable-doc inputs 与 task-delta inputs。
Phase 2 必须逐项复核；缺失或冲突即返回 `implementation_required`。

## 12. 中台知识依据

本任务只修改 Trellis workflow marketplace、public Skill contracts、companion runtime、
preset installer 与 docs，不接入业务中台 SDK/framework。Middle-platform Knowledge Gate
结论为“不适用”。

## 13. 关键取舍

| Choice id | Selected design | Rejected alternative | Selection reason | Product/risk expansion |
| --- | --- | --- | --- | --- |
| C1 | 独立 production manifest | 把三包写入 Stage 0 manifest | 保留 #145 activation public identity，并让两个迁移单元独立验证 | `false/false` |
| C2 | `task_ref` 统一定位 task-local private state | 每个 artifact各加 public locator | Consumer只需要 task scope locator；runtime负责private discovery/freshness | `false/false` |
| C3 | `committed_head` 同时绑定 commit与 freshness | 新增 commit token | #131直接消费该 SHA；额外 token没有独立 consumer用途 | `false/false` |
| C4 | Deterministic builder生成 private candidate并调用现有 executor | 重写 commit transaction或让Agent编写完整plan | 分离 semantic authoring与objective materialization，保留现有transaction invariants | `false/false` |
| C5 | Closure从 live registry派生，9×35作为当前 cardinality assertion | Validator硬编码9个ids | 未来 active 1.3 entry必须证明完整合约，同时避免静默漏检 | `false/false` |
| C6 | `branch-review-or-finding-closure` 保持当前 consumer，input shape与#131兼容 | #146提前激活或引用不存在的#131 package | 保持 stable workflow route；#131独立拥有后续Skill activation | `false/false` |
| C7 | Additive target-owned `skill_input_authoring_seed`，minimal seed与fresh AI authoring无覆盖合并 | Producer输出完整semantic input；runtime/default重建AI fields；另开prerequisite后重启#146 | 唯一同时满足minimal DTO、完整target schema、semantic ownership与三条正常handoff的已确认方案 | `true/false` |
| C8 | `clarify_scope` 使用 routing-only workflow target | 第4条authoring seed；扩大producer DTO | 三字段proposal context没有target同名字段，router可保持semantic input由caller AI新鲜编写 | `true/false` |
| C9 | Public input显式定位task，private snapshot绑定完整worktree state | 从private artifact推断task；task mode无条件接受dirty paths | 同时保持public DTO不变、exact locator与active-task正常dirty scope correctness | `true/false` |
| C10 | 固定locator执行exact-prior formal replacement并记录optional superseded digest | 删除/改名旧snapshot；versioned archive/current pointer | 最小修复active task authority刷新，同时保留历史读取、重复执行结果一致性与public API | `true/false` |
