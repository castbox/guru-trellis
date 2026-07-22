# #145 技术设计：Stage 0 最小 typed handoff 原子迁移

## 1. 设计原则

1. 六个 Stage 0 Skills 是一个 versioned activation unit，禁止 producer 与 consumer
   分批切换形成 mixed graph。
2. Interface 1.3 只暴露 caller-owned input、exact invocation、per-exit output、consumer
   input/projection 与最小 freshness token；owner private artifact 不进入 handoff DTO。
3. Workflow 只拥有 mandatory invocation、typed-exit routing 与 stop；Skill 继续拥有现有
   semantic/deterministic closed loop。
4. Runtime 读取 live facts并生成 digest/path metadata；Agent 不填写 runtime-derived 字段，
   也不读取/import private Python source。
5. #144/#147 继续拥有基础设施语义；#145 只实现已确认的两个 compatibility delta：
   Interface 1.3 optional scalar，以及真实 semantic package 的 production eval
   runner/adapter 闭环。不得借此重写 grader、semantic owner 或其它基础合同。
6. Canonical、installed、dogfood、四平台、throwaway、update/reapply 是同一个交付合同。

## 2. 所有权与路径

| Owner | Canonical path | 拥有 |
| --- | --- | --- |
| Production package | `trellis/skills/guru-team/packages/<skill>/` | Interface、public schemas/examples/wrapper、private artifact declarations、eval corpus |
| Stage 0 migration manifest | `trellis/skills/guru-team/migrations/stage0-minimal-handoff.json` | 6×24 exact set、profile/output/consumer/projection/case bindings、activation version |
| Manifest schema | `trellis/skills/guru-team/schemas/stage0-migration-manifest.schema.json` | Closed manifest shape 与 `guru-team-stage0-migration-manifest-1.0` identity |
| Production registry | `trellis/skills/guru-team/registry.json` | Active Skill lifecycle、Interface/state、workflow route |
| Extension manifest | `trellis/guru-team-extension.json` | Public schema inventories、legacy/minimal ids、migration manifest locator、managed command/assets |
| Workflow | `trellis/workflows/guru-team/workflow.md` | Mandatory markers、unique consumers、workflow/stop target schemas |
| Shared runtime | `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` | Deterministic validation、public wrapper dispatch、live-fact derivation、projection execution |
| Preset installer | `trellis/presets/guru-team/` | One-transaction distribution、mode、installed inventory、update/reapply verification |
| Dogfood installed copy | `.trellis/guru-team/skills/` 与四平台 Skill roots | Canonical bytes 的安装结果，不是长期 source |

Manifest schema 是真实结构化消费边界：source/installed validator、preset installer、
throwaway verifier 与 coverage tests 均读取它；不为纯形式创建无人消费 schema。

## 3. Exact Stage 0 graph

| Producer exit | 唯一 consumer | Consumer kind |
| --- | --- | --- |
| `guru-sync-base:synced` | `guru-discover-change-context` | Skill |
| `guru-sync-base:skipped` | `original-request-route` | Workflow |
| `guru-sync-base:blocked` | `base-sync-blocked` | Stop |
| `guru-discover-change-context:context_ready` | `guru-clarify-requirements` | Skill |
| `guru-discover-change-context:refresh_base` | `guru-sync-base` | Skill |
| `guru-discover-change-context:blocked` | `change-context-blocked` | Stop |
| `guru-clarify-requirements:clear` | `guru-requirements-clear-router` | Workflow |
| `guru-clarify-requirements:needs_context` | `guru-discover-change-context` | Skill |
| `guru-clarify-requirements:refresh_context` | `guru-sync-base` | Skill |
| `guru-clarify-requirements:retarget_context` | `guru-sync-base` | Skill |
| `guru-clarify-requirements:new_task` | `guru-full-task-intake-chain` | Workflow |
| `guru-clarify-requirements:blocked` | `requirements-clarification-blocked` | Stop |
| `guru-review-contract-wording:pass` | `guru-contract-wording-pass-router` | Workflow |
| `guru-review-contract-wording:content_changed` | `guru-contract-wording-change-router` | Workflow |
| `guru-review-contract-wording:blocked` | `contract-wording-blocked` | Stop |
| `guru-review-change-request:ready` | `guru-create-task-workspace` | Skill |
| `guru-review-change-request:clarify_requirements` | `guru-clarify-requirements` | Skill |
| `guru-review-change-request:review_wording` | `guru-review-contract-wording` | Skill |
| `guru-review-change-request:refresh_context` | `guru-sync-base` | Skill |
| `guru-review-change-request:blocked` | `change-request-review-blocked` | Stop |
| `guru-create-task-workspace:created` | `guru-task-workspace-created` | Workflow |
| `guru-create-task-workspace:refresh_review` | `guru-sync-base` | Skill |
| `guru-create-task-workspace:cancelled` | `task-workspace-cancelled` | Stop |
| `guru-create-task-workspace:blocked` | `task-workspace-blocked` | Stop |

Workflow markers、Interface `external_exits`、registry routes 与 migration manifest 必须由
validator做双向 set equality；表中任何 consumer 禁止被 adapter或脚本重判。

## 4. Public input profiles

### 4.1 Profile inventory

| Skill | Public input kind | Structurally distinct profiles/signatures |
| --- | --- | --- |
| `guru-sync-base` | `scalar_cli` | 一个共享 signature；`--mode workflow|standalone`、repo root、`required:false` 的 `--base-branch`、caller route classification；flag 缺省时由 owner 执行既有固定 resolver order；workflow/standalone 的显式与省略 argv 均有完整 example，standalone 禁止 `skipped` |
| `guru-discover-change-context` | `structured_json` | `pre_task`、`task_local_reentry`；二者分别覆盖 workflow/standalone mode，后者显式携带 task locator 与 prior snapshot locator，而非完整 private artifact |
| `guru-clarify-requirements` | `structured_json` | `initial_change_request`、`active_task_scope_change`、`standalone_review`；active profile 必填 task locator 与 `resume_target` |
| `guru-review-contract-wording` | `structured_json` | `change_request`、`planning_artifacts`、`explicit_paths`；固定 profile 禁止缩窄 scope，`planning_artifacts` 固定三份 task docs |
| `guru-review-change-request` | `structured_json` | `current_issue`、`proposed_draft`、`standalone_request`；每个 target kind 绑定同一组 current prerequisite handoff但使用独立 target schema |
| `guru-create-task-workspace` | `structured_json` | `issue_only_initial`、`issue_only_recovery`、`workspace_task_initial`、`workspace_task_recovery`；issue 与 workspace/task mutation 在 schema discriminator 层互斥 |

### 4.2 Public input field policy

- 每个 structured aggregate schema 使用 `profile` discriminator、closed `oneOf` 与
  `additionalProperties:false`。
- Caller-owned fields 限于：mode/profile、request/target locator、explicit base selector、
  confirmed proposal/action id、resume target、naming/assignee choice、continuation route 与
  package-local prior artifact locator。
- Live Git/GitHub/Trellis content、current HEAD、issue body、updated_at、file bytes、digest、
  size、mtime、artifact absolute path、duplicate result 与 recovery scan 均由 runtime重读。
- `prior artifact locator` 必须是 task-relative locator；runtime 打开并验证 owner private
  schema/freshness。Public input 不复制 private artifact body。
- `guru-sync-base` 只声明 scalar arguments 和 exact argv；不创建 aggregate/profile JSON
  schema。每个 scalar argument 显式声明 boolean `required`；validator 接受 `true` 与
  `false`、拒绝缺失和非 boolean。其 mode/route enum 与 optional base 行为由 public
  wrapper 和 invocation probe验证。

## 5. Per-exit output 与 consumer projection

### 5.1 Output family

每个 output schema 都必须包含稳定 `exit_id` discriminator。其余字段只能来自下列闭集：

| Family | 字段用途闭集 | 对应 exits |
| --- | --- | --- |
| Route-only | `exit_id`；投影到 `zero_payload` 或 router enum | 所有 `blocked`、`skipped`、`cancelled` |
| Fresh sync handoff | selected repo/base continuation 与唯一下一步需要的 post-sync freshness token | `synced` |
| Context handoff | target/request continuation、consumer 所需的精简 current/history/duplicate semantic context、snapshot freshness token | `context_ready` |
| Refresh handoff | 原 caller-owned continuation、refresh/retarget discriminator；live stale facts不进入 DTO | `refresh_base`、`needs_context`、`refresh_context`、`retarget_context`、`refresh_review` |
| Clarification route | resume target、target disposition、已确认 scope proposal/action 的最小结果 | `clear`、`new_task` |
| Wording route | fixed `profile` 与 exit；router据此选择已声明 consumer | `pass`、`content_changed` |
| Readiness handoff | target locator、approved delivery/scope projection、五个 prerequisite locator/token | `ready` |
| Prerequisite re-entry | target/profile continuation与 affected prerequisite id，不携带完整 review artifact | `clarify_requirements`、`review_wording` |
| Workspace completion | repo/issue/base/branch/worktree/task locator 与 task-start所需最小 identity | `created` |

这里的 freshness token 只在 consumer 无法通过 live reread证明同一 upstream identity 时保留；
manifest 的 field-to-consumer-use assertion 必须逐字段给出 consumer schema pointer。任何无法
给出 pointer 的候选字段从 public output 删除并留在 private artifact。

### 5.2 Consumer-owned contracts

- Skill consumer input 位于目标 package，并由目标 package拥有 schema/signature；producer
  只能 exact-ref `interface_path`、`input_kind` 与 `profile_id`。
- Workflow consumer schemas 位于
  `trellis/workflows/guru-team/consumers/stage0/`，分别为清晰度 router、措辞 pass/change
  router、new-task router 与 created workspace transition；这些 schema 不复制 private
  evidence。
- Stop consumers 统一使用 `zero_payload`，projection operation 为 `select` 且
  `mappings=[]`；错误详情保留在 owner private artifact/日志，不进入跨 Skill DTO。
- `consumer_use_ids` 与 projection ids 一一对应；schema test 对每个 output property 要求
  一个或多个目标 consumer JSON pointer 或 scalar argument id。

### 5.3 Projection policy

- `direct`：producer output schema 与 consumer input schema byte/shape相同。
- `select`：只选取 consumer需要的字段；stop 选择空 payload。
- `rename`：仅在 stable producer field 与 consumer-owned field命名不同使用。
- `normalize`：normalizer id 闭集为 #144 已发布集合，不添加 arbitrary code。
- Projection validator必须拒绝 private schema path、未知 operation、未知 field、无人消费
  output field、consumer缺失与 schema/version mismatch。

## 6. Private artifacts 与 persistence

| Skill | Private owner artifacts | Persistence |
| --- | --- | --- |
| `guru-sync-base` | `guru-base-sync-result-1.0` facts | `stdout_only_pre_task` |
| `guru-discover-change-context` | `guru-context-discovery-1.0` snapshot | pre-task `stdout_only_pre_task`；post-task `task_local_tracked` |
| `guru-clarify-requirements` | `guru-requirements-clarification-2.0` recorder/checker result | `stdout_only_pre_task`；不新增专用 tracked artifact |
| `guru-review-contract-wording` | `guru-contract-wording-review-1.0` gate evidence | pre-task/standalone `stdout_only_pre_task`；planning `task_local_tracked` |
| `guru-review-change-request` | `guru-change-request-review-1.0` readiness evidence | pre-task/standalone `stdout_only_pre_task`；workspace creator持久化 exact result |
| `guru-create-task-workspace` | `guru-task-workspace-plan-1.0`、`guru-task-workspace-result-1.0` | plan pre-write stdout；成功后 task-local tracked artifacts与 ignored runtime mapping |

Interface 的 `private_artifacts[]` 只登记 kind、schema与 persistence。Archived task artifacts
继续由原 schema 读取；migration validator 不扫描后回写 archive。

## 7. Exact public invocation

每个 production package 增加一个 package-local thin public wrapper，Interface
`public_contracts.invocation` 绑定：

- command id `run-skill-command`；
- package wrapper path；
- structured profile或 scalar argument binding；
- `stdout_contract=single_typed_exit`；
- stable invocation error schema/example；
- 每个 input profile/signature 的完整 executable argv example。

Wrapper 只把 public input交给 shared runtime并返回一个 DTO；不含 semantic review、
consumer route判断或 private artifact parsing policy。`discover-skill-contract` 必须能从
source/installed roots定位所有 input、output、consumer、projection、example 与 private
artifact，不要求调用方打开 runtime source。

`guru-sync-base` wrapper 在 `--base-branch` 存在时把该值传给 owner resolver；flag 不存在时
传递未指定状态，并调用同一 `resolve-only -> execute -> check` 链。Wrapper 不预选 configured
base、不复制 candidates 顺序。`synced` DTO 的 base 必须来自 checker-passed owner result，
不能从 caller input回显推断。

## 8. Migration manifest 与原子 activation

### 8.1 Manifest shape

`stage0-minimal-handoff.json` 顶层固定：

- schema/version 与 `activation_unit_id=stage0-minimal-handoff-v1`；
- required Interface/registry/eval schema ids；
- 精确六个 Skill ids；
- 每个 Skill 的 input profile/signature ids、24 exit ids、output schema/example ids、
  consumer input ids、projection ids、private artifact ids、eval case ids；
- legacy allowlist精确为 #146 三个 Skill ids；
- activation policy `preset_transaction`；仅当实现证明 transaction不可用时，使用
  `versioned_public_dto_adapter` 并登记 adapter id/removal condition。

Validator 比较 manifest 与 Interface/registry/workflow/extension/evals 的双向集合，不接受
missing、extra、duplicate、unknown 或 renamed id。

### 8.2 Preset transaction

Preset 在临时 staging root 构造完整 managed output并完成 source validation，然后一次
apply 六包、registry、manifest、schemas、runtime/wrappers、extension 与平台 copies。安装
后立即执行 installed validation；失败保留既有安装并报告冲突/sidecar，不留下可运行的
mixed graph。这里的 transaction 只覆盖正文要求的正常 installer path，不扩展为锁、
crash consistency 或跨 OS atomicity协议。

### 8.3 Existing active state

- Active task re-entry先通过新 public input的 task-local locator，由 runtime读取现有
  1.2 private artifact、按原 schema验证，再重新执行 owner Skill产生 1.3 DTO。
- 不把旧 private artifact转换成 public DTO缓存，不修改 archived artifact bytes。
- 若需要 versioned adapter，它只在 consumer边界把旧 public DTO字段 select/rename/
  normalize到 1.3 input；六包全部 current后 installer删除 adapter并由测试证明无引用。

## 9. Eval coverage 与 production runner/adapter

每个 package新增 `evals/evals.json`，case binding要求：

- 每个 24 exit绑定一个或多个 case；每个 4.1 profile/signature绑定一个或多个 case；
- normal chain覆盖 synced→context_ready→clear→wording pass→ready→created；
- refresh family覆盖 refresh_base、needs_context、refresh_context、retarget_context、
  review refresh 与 workspace refresh_review；
- stop family覆盖每个 Skill blocked、sync skipped 与 workspace cancelled；
- wording覆盖 pass/content_changed 三个 fixed profiles；
- workspace覆盖 issue-only initial/recovery 与 workspace/task initial/recovery；
- runner必须真实调用 package public wrapper并用 actual exit对应 schema复验；
- trace断言 `public_invocation_only`、`evals_not_loaded_by_skill`、
  `private_runtime_not_read_by_agent`；semantic assertions由外部 grader/human提供。

四 adapter exact-ref同一 canonical corpus；installer/platform tests比较 bytes，不生成副本
来源或平台专用 case。

### 9.1 Runner 数据流

```text
case + fixtures
  -> adapter 构造平台输入与 repo-local execution context
  -> AI/human-reviewed semantic owner decision
  -> owner recorder/checker 记录并验证 checker-passed owner result
  -> package public wrapper 读取 public input + owner result
  -> wrapper 返回 actual typed exit DTO
  -> runner 按 actual exit 选择 output schema并验证 DTO
  -> deterministic grader 比较 expected_exit 与 actual exit并执行 typed assertions
```

`expected_exit` 不进入 public wrapper argv/stdin、owner recorder/checker input或 route选择。
Owner result 必须位于当前 repo 支持的 locator 内并通过该 Skill 的 checker；fixture JSON 中
仅写一个 `typed_exit` 字段不能冒充 checker evidence。

### 9.2 Adapter compatibility

- Shared adapter 必须解析 corpus、fixture 与 public invocation，并执行 9.1 完整数据流。
- Codex adapter 必须在 trusted Git context 中绑定当前 repo/worktree，不把临时非 Git目录
  伪装成可信执行上下文。
- Claude adapter 必须把 corpus prompt/files 与 owner-result locator 按已发布输入协议传递，
  且收集一个可解析 typed DTO。
- Cursor adapter 在 native execution不可用时返回 `unsupported`；不得改写 corpus或回退为
  `expected_exit` 合成结果。
- Platform adapter 只负责上下文、输入与输出收集；grader policy、semantic ownership、
  output schema和 projection 继续由共享合同拥有。

## 10. Compatibility、rollout 与 rollback

### 10.1 Compatibility

- Stable Skill/mode/exit/consumer ids、semantic owner、human confirmation与副作用边界不变。
- Interface 1.3 `scalarArgument.required` 改为显式 boolean 后，现有 `required:true` fixture
  继续有效；调用时只能省略声明为 `required:false` 的 argument。
- 旧 private schema ids 与 archive读取保持兼容；public 1.3 schema使用新 ids，不静默覆盖
  旧 id。
- Extension兼容 scalar `interface_schema_id` 在 #146 完成前保持1.2，
  `current_interface_schema_id`保持1.3；legacy list只含 #146三包，六个 Stage 0
  registry entries分别使用1.3。
- Normal pre-task path继续 repo side-effect-free；task creation仍只发生在 workspace Skill。

### 10.2 Rollout

1. 先更新 durable SSOT与 manifest schema。
2. 迁移六个 canonical packages、consumer schemas、runtime与 tests。
3. 增加六份 eval corpus，完成 9.1/9.2 production execution closure并通过 source
   validation/runner。
4. 更新 registry/extension/preset transaction与 public docs。
5. Preset apply同步 dogfood和四平台；处理所有 sidecar。
6. 执行 clean throwaway install、full Stage 0、update/reapply和 upgrade fixture。

### 10.3 Rollback

- Canonical source validation未通过：不执行 preset apply，回退未安装 delta并修订实现。
- Preset staging/installed validation失败：保留原完整 1.2 Stage 0 graph，修复后重新整包
  apply；不得手工逐包切换。
- Public consumer缺少 direct-use proof：删除候选 output field或修订 consumer schema；不得
  把 audit artifact整体暴露。
- Eval adapter缺失：对应平台返回 `unsupported` 并阻断该平台验收，不创建平台 corpus。
- 发现 stable id、semantic owner、requirement authority、eval schema、grader policy或 run
  evidence contract需要变化：暂停实现，更新规划并重新执行 planning approval，不在 #145
  内静默扩 scope。

## 11. 中台知识依据

本任务仅修改 Trellis workflow marketplace、public Skill contracts、companion runtime、
preset installer 与 docs，不接入业务中台 SDK/framework。Middle-platform Knowledge Gate
结论为“不适用”，无需 Guru Knowledge Center检索。

## 12. Docs SSOT Plan

### 12.1 Docs state

`complete_docs`。已确认当前长期文档层：

- `.trellis/spec/workflow/skill-package-contract.md`：Interface 1.2/1.3、public/private I/O、
  consumer/projection SSOT；
- `.trellis/spec/workflow/companion-scripts.md`：public command与脚本边界；
- `.trellis/spec/workflow/data-contracts.md`：registry、extension、schema/artifact contract；
- `.trellis/spec/workflow/quality-guidelines.md`：source/installed/negative/distribution门禁；
- `.trellis/spec/workflow/index.md`：workflow spec导航；
- `.trellis/spec/preset/installer.md`、`overlay-guidelines.md`、
  `upstream-ownership.md`：安装、漂移、upgrade/update与ownership；
- `.trellis/spec/docs/public-docs.md`：公开文档同步规范；
- `docs/requirements/README.md`、`requirement-main.md`、
  `guru-team-trellis-flow.md`：durable requirements SSOT；
- 根 `README.md`、workflow README、preset README：用户安装/验证入口。

### 12.2 Strategy

`ssot_first`。本任务将 test-only 1.3基础激活到六个 production packages，并新增长期
migration manifest、production public I/O、consumer schemas、eval corpora与upgrade
contract；这些语义必须先进入 durable SSOT，不能只留在 task artifacts。

### 12.3 Affected durable docs

- 更新 `.trellis/spec/workflow/skill-package-contract.md`：Stage 0 6×24 activation、profile/
  output/consumer/private边界、optional scalar、legacy #146 boundary与 field-use proof。
- 更新 `.trellis/spec/workflow/data-contracts.md`：migration manifest schema、extension
  inventories、production schema ids与 existing-state migration。
- 更新 `.trellis/spec/workflow/companion-scripts.md`：六个 public invocation wrappers、
  optional base resolver handoff、checker-passed owner result、actual-exit schema选择、
  runtime-derived facts与 private-source prohibition。
- 更新 `.trellis/spec/workflow/quality-guidelines.md`：set equality、coverage、normal
  transcript、upgrade/mixed-graph negative matrix；当新增合同未被 workflow spec index
  导航时，必须同步更新 index。
- 更新 preset installer/overlay/upstream-ownership specs：transaction staging、managed
  inventory、platform copies、sidecar/update/reapply合同。
- 更新 public-docs spec与根/workflow/preset README：production 1.3 discovery/run示例、
  activation/legacy边界与可执行验证命令。
- 更新 `docs/requirements/*`：#145完成后的 production状态、#146剩余边界与完整 Stage 0
  workflow data flow。

### 12.4 Task delta merge checkpoint

实现子代理先更新 12.3 durable contracts，再修改 runtime/package/installer。Phase 2同一轮
完成 docs、code、schema、tests和distribution；`trellis-check`在记录
`phase2-check.json` 前逐项将 R1-R9/AC1-AC15映射到 durable docs与实际 diff，并单列 D1/D2
验证证据。

### 12.5 Task-history-only content

Phase 0 snapshot、planning approval、逐次命令输出、临时 eval run evidence、sub-agent
liveness、review findings生命周期与本机 throwaway路径只保留在 task/runtime evidence，
不复制到 durable docs。

### 12.6 Reconciliation evidence

Implementation handoff与 Phase 2 report必须列出：实际更新的 durable docs；已合并的 task
delta；仅属历史的内容；source/installed/dogfood/四平台/throwaway/update/reapply结果；
existing active/archive兼容证据；最终零 `.new`/`.bak`。任何 current-scope docs不一致是
blocking finding，不推迟到 Branch Review或 finish-work。

## 13. 关键取舍

| 方案 | 结论 | 原因 |
| --- | --- | --- |
| 六包逐个切换 registry | 拒绝 | 会形成 mixed producer/consumer graph |
| 一次 preset staging transaction | 采用 | 在正常 installer路径中提供完整 graph activation与失败回退 |
| 暴露现有 recorder artifact作为 output | 拒绝 | 继续要求 Agent理解 private 32-150 scalar artifact |
| 仅以 digest作为所有 handoff | 拒绝 | pre-task consumer无法从 repo artifact恢复必要语义内容 |
| 每字段 consumer pointer proof | 采用 | 机械拒绝无人消费 public字段 |
| 为 `guru-sync-base` 新增 input JSON | 拒绝 | scalar CLI已能表达 caller-owned input，额外 schema无人消费 |
| 按 D2 修复 #147 runner/adapter 的 production semantic execution closure | 采用 | 真实 Stage 0 corpus 必须通过 checker-passed owner result与 actual exit执行，且不得改变 grader或semantic owner |
| 用 `expected_exit` 选择 wrapper route或 output schema | 拒绝 | 该字段只属于执行后的预期断言，不能成为被测系统 oracle |
| 平台专用 corpus/adapter policy | 拒绝 | 四平台必须消费同一 corpus bytes与shared grader policy |
| 回写 archive到1.3 | 拒绝 | 破坏已发布 artifact与只读历史边界 |
| 新增 hostile/locking/TOCTOU hardening | 拒绝 | 超出正文 honest-but-fallible 正常场景范围 |
