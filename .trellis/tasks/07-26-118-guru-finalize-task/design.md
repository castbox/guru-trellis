# #118 guru-finalize-task 设计

## 1. 设计结论

实现采用“一项 semantic Skill + 一套 deterministic transaction engine + owner-private
checkpoint”结构。`guru-finalize-task` 是唯一语义 owner；现有 #105 engine 是唯一事务
实现；package scripts 只记录、校验、执行 AI/human 已决定的动作。全局 Finish family
entry/order 继续由 #119 持有，upstream overlay 清理继续由 #132 持有。

## 2. Authority 与 provenance matrix

本表是三份 planning artifacts 的唯一 authoritative provenance matrix。每个
load-bearing item 只使用一个 provenance class。

| ID | Planning locator | Class | Authority | 承接理由 |
| --- | --- | --- | --- | --- |
| P01 | `prd.md` R1 | `explicit_requirement` | `AUTH-118-BODY`, `AUTH-AGENTS` | Issue 与仓库规则共同要求 semantic closed loop。 |
| P02 | `prd.md` R2 | `explicit_requirement` | `AUTH-118-BODY`, `AUTH-105-RUNTIME` | Issue 要求复用 #105 且保持事务语义。 |
| P03 | `prd.md` R3 | `explicit_requirement` | `AUTH-118-BODY`, `AUTH-AGENTS` | AI 与 script ownership 已由 authority 固定。 |
| P04 | `prd.md` R4 | `explicit_requirement` | `AUTH-118-BODY` | Preview、plan digest 与第一次副作用确认是正文合同。 |
| P05 | `prd.md` R5 | `explicit_requirement` | `AUTH-118-CURRENT`, `AUTH-SKILL-CONTRACT` | Accepted-current 要求 Interface 1.3 distinct profiles。 |
| P06 | `prd.md` R6 | `explicit_requirement` | `AUTH-118-CURRENT`, `AUTH-116`, `AUTH-117` | Producer DTO 字段与 target-owned authoring partition 已固定。 |
| P07 | `prd.md` R7 | `explicit_requirement` | `AUTH-118-CURRENT` | 六 exits 与 `exit_id` 已固定。 |
| P08 | `prd.md` R8 | `explicit_requirement` | `AUTH-118-CURRENT`, `AUTH-SKILL-CONTRACT` | Reprepare seed/authoring split 已固定。 |
| P09 | `prd.md` R9 | `explicit_requirement` | `AUTH-118-BODY`, `AUTH-118-CURRENT` | Internal state 与完整 transaction facts 必须 private。 |
| P10 | `prd.md` R10 | `explicit_requirement` | `AUTH-118-BODY`, `AUTH-117` | Verification owner 与 transaction ordering 已固定。 |
| P11 | `prd.md` R11 | `explicit_requirement` | `AUTH-118-BODY`, `AUTH-105-RUNTIME` | PR/archive/recovery 不变量直接继承正文与 current engine。 |
| P12 | `prd.md` R12 | `explicit_requirement` | `AUTH-118-CURRENT`, `AUTH-SKILL-CONTRACT` | Real-wrapper eval 与 actual-exit ordering 已固定。 |
| P13 | `prd.md` R13 | `explicit_requirement` | `AUTH-118-CURRENT` | 四平台 corpus 与专属协议覆盖已固定。 |
| P14 | `prd.md` R14 | `explicit_requirement` | `AUTH-118-BODY`, `AUTH-AGENTS`, `AUTH-TRELLIS-DOCS` | 安装、update、dogfood 与 drift gate 已固定。 |
| P15 | `prd.md` R15 | `explicit_requirement` | `AUTH-118-BODY`, `AUTH-AGENTS`, #119, #132 | Close scope 与 upstream/integration 边界已固定。 |
| P16 | `prd.md` R16 | `explicit_requirement` | `AUTH-118-BODY`, `AUTH-AGENTS` | 正常运行与 unusual-scenario 排除项已固定。 |
| P17 | 本文件 3.1 六 profile 设计 | `necessary_implementation_choice` | P05, P06, P08 | 按结构差异拆 profile，禁止 optional-field 总对象。 |
| P18 | 本文件 4.1 私有 gate | `necessary_implementation_choice` | P01, P04, P09 | Semantic Gate 与 confirmation 必须有 task-local 可审计记录。 |
| P19 | 本文件 5 单引擎分层 | `necessary_implementation_choice` | P02, P03, P10, P11 | 复用现有 engine 并隔离语义判断，避免平行实现。 |
| P20 | 本文件 7 production eval | `necessary_implementation_choice` | P12, P13 | 复用 current native adapter 扩展点并增加 package corpus。 |
| P21 | 本文件 8 distribution | `necessary_implementation_choice` | P14, P15 | 只增加 Guru-namespaced package/runtime/discovery assets。 |
| P22 | 本文件 9 Docs SSOT Plan | `necessary_implementation_choice` | P01-P21 | 把 durable ownership 与导航放入既有 SSOT，禁止复制 step-local 正文。 |
| P23 | 恶意/并发/新 fault 机制 | `out_of_scope_proposal` | P16 | disposition=`excluded_by_current_authority`，route=`none`。 |
| P24 | Finish family global integration | `out_of_scope_proposal` | P15, #119 | disposition=`followup_issue_119`。 |
| P25 | Upstream overlay cleanup | `out_of_scope_proposal` | P15, #132 | disposition=`followup_issue_132`。 |

所有 `necessary_implementation_choice` 的 `product_scope_expansion=false` 且
`risk_scope_expansion=false`。本计划没有 `approved_scope_expansion`。

## 3. Public Interface 1.3

### 3.1 Input profiles

| Profile | Mode | Producer/caller seed | Target-owned authoring fields | Private validation |
| --- | --- | --- | --- | --- |
| `publication_ready` | `workflow` | `task_ref`, `reviewed_head`, `publication_ref` | `profile`, `mode`, `finalization_intent` | 调用 #116 owner checker，校验 opaque ref 与 reviewed HEAD。 |
| `verification_verified` | `workflow` | `task_ref`, `plan_ref`, `reviewed_head`, `verification_ref` | `profile`, `mode`, `reentry_intent` | 调用 #117 owner checker，校验 same plan/ref/HEAD。 |
| `verification_not_required` | `workflow` | `task_ref`, `plan_ref`, `reviewed_head` | `profile`, `mode`, `reentry_intent` | 调用 #117 owner checker，校验 not-required identity。 |
| `same_plan_resume` | `workflow` | `task_ref`, `plan_ref` | `profile`, `mode`, `recovery_intent`, `recovery_context` | Finalizer owner checker 识别同 plan 与唯一 draft/archive state。 |
| `reprepare_preview` | `workflow` | `task_ref`, `reason_code` | `profile`, `mode`, `reprepare_intent`, `reprepare_context` | Finalizer owner 重新 preview，生成新 digest 与新 confirmation。 |
| `standalone_finalization` | `standalone` | caller authors complete profile | 无 producer projection | 发现 active/partial/archived task 后执行同一 precondition 与 semantic gate。 |

`reprepare_preview` 的 producer `seed_fields` 精确为 `task_ref`、`reason_code`。
其 `authoring_fields` 与 seed 零交集；两者 union 精确覆盖 schema `required`。Runtime
只验证 no-overwrite merge，禁止生成 `reprepare_intent` 或 `reprepare_context`。

### 3.2 Output DTOs

| Exit | Required fields | Consumer |
| --- | --- | --- |
| `verification_required` | `exit_id`, `task_ref`, `plan_ref`, `repo_ref`, `reviewed_head`, `verification_target` | `guru-verify-extension-installation:verification_required` |
| `publication_review_stale` | `exit_id`, `task_ref`, `stale_reason` | `guru-review-task-publication:publication_review_stale` |
| `resume_finalization` | `exit_id`, `task_ref`, `plan_ref` | `guru-finalize-task:same_plan_resume` |
| `reprepare_required` | `exit_id`, `task_ref`, `reason_code` | `guru-finalize-task:reprepare_preview` |
| `published` | `exit_id`, `task_ref`, `pr_number`, `pr_url` | finish response contract |
| `blocked` | `exit_id`, `reason_code`, `remediation` | finalization stop contract |

`exit_id` 只承担 typed-exit identity，不进入 Skill seed projection。每个业务字段必须被
唯一 consumer 直接使用。Projection 仅使用 Interface 1.3 的 `select`；target profile 的
fresh fields 通过 `skill_input_authoring_seed` no-overwrite merge 进入。

### 3.3 Stable route reasons

- `publication_review_stale.stale_reason` 使用 closed codes：
  `publication_review_missing`、`publication_review_stale`、
  `publication_review_head_mismatch`。
- `reprepare_required.reason_code` 使用 `archive_month_changed`。
- `blocked.reason_code` 使用 closed codes：`prerequisite_incomplete`、
  `invalid_private_state`、`unexpected_path`、`head_mismatch`、
  `draft_identity_ambiguous`、`draft_identity_missing_or_replaced`、
  `external_dependency_blocked`。
- 同 plan 的瞬时 executor failure、draft-to-ready retry、active/archive/exact-commit
  continuation 使用 `resume_finalization`，禁止新增 public recovery state。

## 4. Owner-private evidence

### 4.1 `task-finalization-gate.json`

新增一个 task-local tracked private gate，schema id 为
`guru-task-finalization-gate-1.0`。它记录：input profile identity、task/HEAD/opaque refs、
AI plan review、scope/readiness/recovery judgment、exact human confirmation、selected
typed exit、consumer、current facts digest 与 supersession linkage。它不充当 public DTO，
不把 producer private artifact body 复制进来。

Recorder 必须在 AI Review Gate 与命中条件时的 human confirmation 完成后写入。Checker
只校验 schema、locators、owner checker results、plan digest、confirmation binding、HEAD、
private transition continuity、actual exit/consumer 与 freshness。Checker 禁止推导
semantic pass 或 recovery route。

### 4.2 Existing private assets

- `closeout-plan.json`：finalizer-owned immutable runtime checkpoint。
- `pr-readiness.json`：#116-owned gate；finalizer 只调用 owner checker 并消费 opaque ref。
- `marketplace-verification.json`：#117-owned gate；finalizer 只调用 owner checker并消费
  opaque ref。
- `pr-body.md` 与 `finish-summary-index.json`：#116 已审核的 task-local content。
- `finish-summary.json`：取得真实 PR identity 后由 finalizer engine 生成一次。
- ledger、Branch Review、planning、Phase 2、Docs SSOT evidence：通过各 owner checker 验证，
  不进入 public handoff。
- machine recovery journal：仅写 `.trellis/.runtime/guru-team/**` ignored runtime；tracked
  continuity 由 immutable plan、Git commit 与 task-local private gates 承担。

## 5. Single transaction engine

### 5.1 分层

1. `preview-finalization`：side-effect-free executor/validator，调用 current
   `prepare_closeout` 与 plan validator，返回 deterministic facts 与 plan digest。
2. `record-finalization-gate`：记录 AI/human 已完成的 review、confirmation 与 route。
3. `check-finalization-gate`：重建 objective facts 并校验 private gate。
4. `execute-finalization-transition`：只执行 private gate 授权的下一 deterministic
   transition，返回 machine state facts，不选择 external exit。
5. `invoke.sh`：校验 public input、checker-passed owner result，从 actual exit 选择 schema，
   输出一个 minimal DTO。

上述命令通过现有 Guru dispatcher 暴露给 package scripts。旧 `cmd_finish_work` 与新命令
必须调用同一 closeout engine；compatibility wrapper 的用户可见行为保持 current。不得
复制 `prepare_closeout`、PR resolver、projection、archive transaction 或 ready executor。

### 5.2 Semantic loop

```text
public input
-> owner preconditions and side-effect-free preview/state discovery
-> AI plan/scope/readiness/recovery review
-> exact digest confirmation when first side effect or new plan is required
-> recorder/checker
-> one deterministic transition or current terminal fact
-> AI route review
-> recorder/checker refresh
-> one external exit DTO
```

脚本返回的 internal state 只作为 AI evidence。AI 必须把当前事实归入六个 external exits
之一；无法形成唯一 route 时返回 `blocked`。

### 5.3 Transaction order

1. Build immutable plan and prevalidate maximum-width PR projection。
2. Push exact reviewed content HEAD。
3. 计划要求 installation verification 时返回 `verification_required`，此时无新 PR 与
   archive mutation。
4. Consume same plan/ref/HEAD #117 evidence，提交并 push exact pre-draft evidence allowlist。
5. Create/reuse one draft PR，绑定 repo/head/base/number/URL/title/body bytes。
6. Build final projection and final summary once。
7. 调用 official `task.py archive --no-commit`，创建一次 archive metadata commit并 push。
8. 校验 local/remote/PR HEAD 三方一致与 PR identity unchanged。
9. 执行 draft-to-ready，返回 `published`，禁止后续 repo write/commit/push。

## 6. Recovery state machine

| Objective state | AI route | Deterministic action |
| --- | --- | --- |
| Publication evidence missing/stale/head mismatch | `publication_review_stale` | 零副作用，调用 #116 完整 re-entry。 |
| Prepared, first side effect unconfirmed | `blocked` | 展示同 plan digest 并取得 exact confirmation 后重新调用。 |
| Content pushed, verification pending | `verification_required` | #117 完整 semantic verification。 |
| Same plan transient failure before archive | `resume_finalization` | 复用 plan 与唯一 draft，执行下一合法 transition。 |
| Archive month changed while task active | `reprepare_required` | 新 preview、新 digest、新 exact confirmation；旧 plan 只留 supersession evidence。 |
| Active task status completed after interrupted move | `resume_finalization` | 依照 prevalidated file set 与 official task delta 恢复。 |
| Exact archive commit 已存在但 remote/ready 未完成 | `resume_finalization` | Push exact commit 或 retry ready；不重开 archived artifacts。 |
| Draft-to-ready failed | `resume_finalization` | 只重试 GitHub state transition；零 archive/reverify/rewrite/commit。 |
| Missing/closed/replacement PR、ambiguous PR、unexpected path、HEAD mismatch | `blocked` | 零猜测、零替换、零新 PR。 |

该表完整继承 Issue 正文 matrix，不增加并发、锁、TOCTOU、crash 或新 fault branch。

## 7. Production eval 与测试设计

### 7.1 Package-local corpus

Corpus case 必须执行 package `scripts/invoke.sh`，并引用 repo-local
checker-passed `task-finalization-gate.json` fixture。Case 集合必须包含：

- publication -> `verification_required`
- stale publication -> `publication_review_stale`
- same-plan retry -> `resume_finalization`
- cross-month -> `reprepare_required`
- completed ready recovery -> `published`
- invalid objective state -> `blocked`
- verified re-entry 与 not-required re-entry 的 profile coverage
- standalone active/partial/archived profile coverage

Adapter 先解析 wrapper actual output 的 `exit_id`，再选择对应 output schema并校验 DTO，
最后比较 `expected_exit`。Native request 结构不得含 `expected_exit`。

### 7.2 平台矩阵

- `shared`：adapter request/response parsing 与 actual schema selection。
- `codex`：trusted Git root acceptance 与 untrusted root unavailable result。
- `claude`：stdin/file input protocol 与 single JSON stdout。
- `cursor`：unsupported 与 unavailable 都产生稳定 adapter result，不伪造 semantic pass。
- 四平台使用同一 canonical `evals/evals.json` 与 files bytes；dogfood copies 逐文件 hash
  一致。

### 7.3 Transaction regression

扩展现有 #105 tests，把每个正文 transition/failure 映射到唯一 external exit，同时保留
原 task path/status、PR state、local/remote/PR HEAD、dirty/staged paths、artifact
mutation 断言。既有 2026-07-03、2026-07-04、#100 tests 必须保持通过。禁止新增本
Issue 未列明的 fault injection。

## 8. Distribution 与 compatibility

### 8.1 Canonical write scope

- `trellis/skills/guru-team/packages/guru-finalize-task/**`
- #116/#117 Interface 1.3 consumer bindings 与 target authoring examples
- `trellis/skills/guru-team/registry.json` 与 extension public API inventory
- `trellis/skills/guru-team/adapters/eval/native_adapter.py` 与 package/eval tests
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 与对应 tests
- Guru-namespaced canonical/installed bash wrappers、schema inventory 与 preset installer
- README 与 `.trellis/spec/workflow/**` durable docs
- installer 生成的 `.trellis/guru-team/skills/**`、`.agents/skills/guru-finalize-task/**`、
  `.codex/skills/guru-finalize-task/**`、`.claude/skills/guru-finalize-task/**`、
  `.cursor/skills/guru-finalize-task/**`

### 8.2 Explicit no-write scope

- `trellis/workflows/guru-team/workflow.md` 与 `.trellis/workflow.md` 的 Finish global
  ordering/entry activation
- `.agents/skills/trellis-finish-work/**`
- `.codex/prompts/trellis-finish-work.md` 与 `.codex/skills/trellis-finish-work/**`
- `.claude/commands/trellis/finish-work.md`
- `.cursor/commands/trellis-finish-work.md`
- 上述 upstream-owned path 的 canonical overlay copies
- `.trellis/scripts/task.py`、global npm、`node_modules`

若 active package registry validation 强制修改 global Finish route，当前 task 必须 fail
closed 并回到 authority review；禁止用 workflow mutation 绕过 #119 边界。

### 8.3 Compatibility

`finish-work.sh` 与 `cmd_finish_work` 保持 compatibility surface，内部改为调用同一 engine。
`publish-pr.sh` 保持 current fail-closed。#119 后续只做 global ordering、entry 与 combined
acceptance，不重新实现本 Skill 内部行为。

## 9. Docs SSOT Plan

本章节是本 task 唯一完整 Docs SSOT Plan。

| Doc surface | Current status | 实施决定 | Semantic owner | 验证 |
| --- | --- | --- | --- | --- |
| `guru-finalize-task/references/contract.md` | 缺失 | 新建完整 step-local behavior SSOT：preconditions、semantic gate、confirmation、private state、six exits、recovery。 | `guru-finalize-task` | package contract tests + wording review |
| `guru-finalize-task/SKILL.md` | 缺失 | 新建短入口，只加载 contract、声明 `judgment_mode=semantic` 与闭环顺序。 | package discovery | package tests |
| `.trellis/spec/workflow/skill-package-contract.md` | finalizer 为 planned | 记录 active/public Interface 1.3 package、profiles、six exits、private ownership、production eval 与 closure facts；不复制 recovery 算法。 | durable public package architecture | spec assertions + wording review |
| `.trellis/spec/workflow/workflow-contract.md` | #105 engine 与 future owner 并存 | 把 transaction semantic owner 指向新 package，保留 #105 invariants；global route 仍标注由 #119 激活。 | durable transaction architecture | contract tests + scope diff |
| `README.md` | finalizer 为 planned | 更新 package discovery、eval、additive install 状态；明确 #119/#132 边界。 | repository navigation | README command tests |
| `trellis/presets/guru-team/README.md` | finalizer 为 planned | 更新 preset 安装 inventory、平台 copies、hash/update/reapply 行为；不写 Finish entry 步骤。 | preset installation docs | throwaway verifier |
| `trellis/workflows/guru-team/README.md` | future finalizer | 只更新 ownership/status 与 #119 handoff；不激活 global route，不复制 Skill 内部步骤。 | workflow marketplace navigation | workflow docs tests |
| Canonical/dogfood workflow Markdown | 当前 stop 在 missing finalizer gate | 本 task 不改变 global ordering/entry；#119 持有后续 delta。 | #119 | no-diff assertion |
| Upstream Finish Skill/Command/Prompt overlays | transitional legacy | 本 task 零修改；#119/#132 持有 integration/cleanup。 | #119/#132 | no-diff + ownership validator |
| Task `prd.md` | requirement delta | 只保留 requirements、acceptance、Docs 状态与影响。 | task-local | planning approval |
| Task `design.md` | 本文件 | 保存唯一 Docs SSOT Plan、provenance、I/O 与 implementation design。 | task-local | planning approval |
| Task `implement.md` | execution delta | 只保存执行 checklist、checkpoint、验证与 rollback。 | task-local | planning approval + Phase 2 check |

Docs reconciliation 完成条件：表中每个 `实施决定` 都映射到 final diff 或明确 no-diff
assertion；Durable docs 与 package contract 无互相冲突；README 只做导航/安装，不成为
第二份 behavior SSOT。

## 10. Compatibility、rollback 与异常处理

- Compatibility：#116/#117 producer DTO 字段不变；#105 transaction ordering 与 artifacts
  不变；旧 finish compatibility entry observable behavior 不变。
- Rollback：PR 合并前通过删除新 package/additive inventory并恢复 engine delegate 完成；
  不对外部 GitHub/task 执行 closeout 副作用。合并后的 migration 由后续独立 issue 处理。
- Failure：任何 schema、owner checker、digest、HEAD、PR identity、path、archive lineage、
  corpus drift 或 install drift 返回稳定 failure/typed exit，禁止猜测 route。
- Security：输出与 artifact 禁止 secret、credential-bearing remote、signed URL、`.env`、
  客户数据或原始 provider payload。

## 11. Unusual-scenario review

| Candidate | Trigger evidence | Disposition | Reason |
| --- | --- | --- | --- |
| 恶意 artifact/hash/state | 仅依赖人为伪造 | `out_of_scope` | 当前 authority 明确排除。 |
| 并发 finalizer、锁、TOCTOU | Issue 正文无 trigger | `mechanism_removed` | 会扩张 transaction scope。 |
| 新 fault injection/crash consistency | Issue 正文无 trigger | `mechanism_removed` | Matrix 已封闭。 |
| 跨 OS atomicity | Issue 正文无 trigger | `out_of_scope` | 当前 authority 明确排除。 |

本设计没有 unusual scope expansion，也不需要 dedicated proposal confirmation。
