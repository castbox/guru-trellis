# #146 需求：迁移 production Skills 到最小 typed handoff I/O

## 1. 目标

把 `guru-approve-task-plan`、`guru-check-task`、`guru-create-task-commit`
三个 production Skills 的 11 个稳定 typed exits 从
`guru-team-skill-interface-1.2` + `legacy` 原子迁移到
`guru-team-skill-interface-1.3` + `minimal_handoff`。迁移完成后，Agent 只编写
AI 拥有的 semantic input，并只消费 per-exit 最小 DTO；planning、Phase 2 与 commit
的 gate/checkpoint/transaction artifacts 全部保留为 runtime private state。

本任务同时完成 9 个 active Skills、35 个 exits 的 registry、public I/O、consumer
projection 与 eval coverage 闭包，并修复当前 `main` 已复现的
`keep_current_open_issue -> retained` Stage 0 public projection 缺口。对于两个
self-reentry 与 `passed -> initial_commit` 三条 semantic Skill handoff，Interface 1.3
必须新增 additive、target-owned `skill_input_authoring_seed`，在不扩大 producer DTO、
不重建 AI judgment 的前提下把 minimal seed 与 fresh caller authoring 合并为完整 target
profile input。

## 2. 权威与当前基线

### 2.1 权威来源

- GitHub Issue [#146](https://github.com/castbox/guru-trellis/issues/146) 正文固定
  3 Skills、11 exits、9/35 closure、#131 handoff、兼容合同与验收范围。
- [依赖耦合澄清评论](https://github.com/castbox/guru-trellis/issues/146#issuecomment-5042614203)
  固定 #144/#145/#147 的已交付基线、共享基础设施修改的条件式 Scope Change Gate 与回归边界。
- [Stage 0 projection proposal](https://github.com/castbox/guru-trellis/issues/146#issuecomment-5042976037)
  已经精确确认，`keep_current_open_issue -> retained` 以 `accepted_current` 纳入本任务。
- [Semantic handoff authoring-seed proposal](https://github.com/castbox/guru-trellis/issues/146#issuecomment-5044522718)
  绑定 proposal `9957d4d64f8e5a599264df6c5ef909b5432a8822e43979ea9c9ab4db85a18902`
  与 action `06762b79209e4ca40e4d36b495cffc2d2faf87c45a099d6e8d5207ddd62d44e6`；
  用户已精确确认以 `accepted_current` 纳入 #146。
- [clarify_scope workflow router proposal](https://github.com/castbox/guru-trellis/issues/146#issuecomment-5045340918)
  绑定 proposal `94fa389212eb801e5d5efeb1264b506c4d40c51969424c498cb7c341d8626421`
  与 action `7d0affc297881201825277a74fdd7edace0777f6ef86e631e277984537c057af`；
  用户已精确确认以 `accepted_current` 纳入 #146。
- [task-local owner-checker locator proposal](https://github.com/castbox/guru-trellis/issues/146#issuecomment-5047220259)
  绑定 proposal `b27b0331ad057a111df26556d69ae4f38d1792134187e1caf362014f81530a03`
  与 action `02dd426fcc9cafe8b494cd93004a6e124709008cad311bd7f60226c80b14ff0c`；
  用户已精确确认以 `accepted_current` 纳入 #146。
- [task-local worktree state proposal](https://github.com/castbox/guru-trellis/issues/146#issuecomment-5049566946)
  绑定 proposal `420548bc06f157928b8dafe73bb51854fbb01fa5d4f0cfe4b1d03606993c2f10`
  与 action `21fdaa68ab5af088aa269ff96603cd0561236de35bf1b561b18b5c72a2a1abc4`；
  用户已精确确认以 `accepted_current` 纳入 #146。
- [formal task context snapshot replacement proposal](https://github.com/castbox/guru-trellis/issues/146#issuecomment-5050065847)
  绑定 proposal `0f8472c3728ee8b8d4188bc0b4301d9f2039d44b90b127a17b81aa176bf5bc49`
  与 action `a7a60a956923882ed8ea5684152a9e31dd5803dd24aff69331f438d866fa5943`；
  用户已精确确认以 `accepted_current` 纳入 #146，并授权发布该 exact issue comment。
- #144 拥有 Interface 1.3、public invocation、consumer projection 与 public/private
  artifact 基础合同；#147 拥有 eval schema、runner、grader 与 adapter 基础合同；#145
  已交付六个 Stage 0 Skills、24 exits、optional scalar、actual-exit schema selection 与
  atomic activation。

### 2.2 Live baseline

- Base：`main` @ `7dc67e9aef08ca4928159d7d13db6fdbd40c5d4c`。
- `trellis/skills/guru-team/registry.json` 当前含 9 个 active Skills；六个 Stage 0 entries
  为 Interface 1.3 + `minimal_handoff`，本任务三个 entries 为 Interface 1.2 + `legacy`。
- 三个目标 `interface.json` 均缺少 `public_contracts`；其 semantic Gate、typed exits、
  recorder/checker 与 commit transaction 已存在，迁移不得重写这些业务语义。
- `trellis/skills/guru-team/migrations/stage0-minimal-handoff.json` 固定 #145 的 6×24
  activation unit；本任务不得修改其集合语义。
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:19176` 的
  `stage0_clarity_disposition()` 未识别 schema 正式值 `keep_current_open_issue`，从而令
  checker-passed `guru-clarify-requirements:clear` 在 public wrapper projection 阶段失败。
- Interface 1.3 当前 `skill_input` projection 要求 producer output 单独填满 target profile
  required fields；在三条已批准 semantic handoff 中，这与 minimal DTO 和 fresh AI-owned
  authoring 同时成立时发生确定性冲突，并已按 `implement.md` RP1 触发 Scope Change Gate。
- `guru-approve-task-plan:clarify_scope` 当前被直接连接到
  `guru-clarify-requirements:active_task_scope_change`，但 producer DTO 无法构造 target 的八个
  AI/route-owned required fields。
- `guru-discover-change-context:task_local_reentry` 当前 public wrapper 未把 validated
  `task_locator` 传给 owner checker，且 task-mode live facts 不接受正常 task worktree dirty
  scope；这两项都会把有效 active-task re-entry 错判为 `owner_result_not_checked`。
- 固定 task-local `context-discovery.json` 当前只能首次写入或接受相同 bytes；合法 authority
  或 worktree state 更新后，fresh candidate 会因 `existing_snapshot_mismatch` 无法替换旧快照。

## 3. 精确迁移集合

| Skill | Judgment mode | Stable exits |
| --- | --- | --- |
| `guru-approve-task-plan` | `semantic` | `approved`、`revision_required`、`clarify_scope`、`blocked` |
| `guru-check-task` | `semantic` | `passed`、`implementation_required`、`planning_stale`、`blocked` |
| `guru-create-task-commit` | `semantic` | `committed`、`revision-required`、`blocked` |

`guru-create-task-commit:revision-required` 的连字符 id 必须保持不变。Source、installed、
workflow markers、registry、extension inventory 与 production migration manifest 的
Skill/exit sets 必须精确一致。

## 4. 功能需求

### R1. Interface 1.3 与 production activation

- 三个 registry entries 必须同时切换到
  `interface_schema_id=guru-team-skill-interface-1.3` 与
  `io_contract_state=minimal_handoff`。
- 三个 Interface 必须发布 `public_contracts`，并保留现有 Skill id、mode id、judgment
  mode、ordered stages、entry preconditions、typed exit id、consumer id、semantic owner、
  confirmation boundary 与 side-effect boundary。
- 新建 production migration manifest 与对应 schema；该 manifest 精确登记本任务的
  3 Skills、11 exits、input profiles、outputs、consumer inputs、projections、private
  artifacts、eval bindings 与 activation policy。
- Stage 0 manifest 的 6 Skills、24 exits 与 activation identity 必须保持不变；production
  manifest 与 Stage 0 manifest 共同构成 active registry closure 输入。

### R2. Structured public input profiles

- 三个 Skills 全部使用 discriminator + closed `oneOf` structured input；每个结构差异明确的
  normal、revision、finding-fix、planning re-entry 或 recovery route 必须拥有独立 profile
  schema、完整 example 与真实 invocation probe。
- `guru-approve-task-plan` public input 只携带 `task_ref`、mode/profile、最小 authority refs、
  AI 编写的 provenance/adequacy/unusual-scenario review、confirmation、exit intent 与 re-entry
  intent；由上游 semantic Skill handoff 进入 re-entry 时还接收 R12 声明的最小 seed
  fields。Runtime 必须重建 planning docs、wording evidence、Docs SSOT、Git 与 task facts。
- `guru-check-task` public input 只携带 `task_ref`、mode/profile、AI 编写的 scope
  disposition、adequacy、findings、unverified conclusions、evidence locators、exit intent 与
  rerun intent。Runtime 必须重建 approved planning、handoff、agent、ledger、Git、command
  与 Docs SSOT facts。
- `guru-create-task-commit` public input 只携带 `task_ref`、mode/profile、commit message
  intent、path authorization、semantic review、human authorization、exit intent 与 recovery
  intent；由 `guru-check-task:passed` 或 self-reentry 进入时还接收 R12 声明的最小 seed
  fields。Runtime 必须生成 exact path/hash/mode/object/digest candidate plan。
- Public input 不得携带完整 private artifact、live Git/GitHub facts、完整 file metadata、
  runtime-derived digest、transaction journal 或 recovery checkpoint body。

### R3. Per-exit outputs 与 consumer projections

- 11 个 exits 必须各自拥有 closed output schema、完整 validator-passing example、唯一
  consumer input/stop contract、declarative projection 与非空 `consumer_use_ids`。
- 每个 output property 必须映射到 consumer 的直接用途；无法绑定 consumer field 或 route
  判断的 property 必须从 public DTO 删除。
- `guru-approve-task-plan:revision_required` 与
  `guru-create-task-commit:revision-required` 必须投影到同一 Skill 的独立 re-entry profile，
  re-entry 不得读取 producer private artifact 来恢复 public input。
- `guru-check-task:passed` 到 `guru-create-task-commit` 的 projection 必须只消费 public DTO。
- `guru-create-task-commit:committed` 必须输出 #131 input 直接消费的 `task_ref`、`base_ref`
  与 `committed_head`；`task_ref` 同时承担 scope locator，`committed_head` 同时承担 commit
  identity 与 freshness identity，不新增无 consumer 字段。
- Stop output 只保留 stable `exit_id`，或保留 stop consumer 明确消费的 stable reason；
  debug、audit、完整 finding 与 transaction facts 不得进入 stop DTO。

### R4. Public/private state 分离

- `planning-approval.json`、`phase2-check.json`、`task-commit-plans/*.json`、candidate plan、
  transaction journal、Git snapshots、agent recovery、complete findings 与 gate evidence
  必须登记为 `gate_evidence` 或 `runtime_checkpoint`，不得成为 public output。
- Task-local tracked、ignored runtime 与 stdout-only state 必须按现有 persistence 语义登记；
  active/archived artifact schemas 保持可读，archive bytes 不追溯修改。
- Runtime 可按 `task_ref` 定位并验证 private state；consumer 不得解析 producer private
  artifact 来补足 public DTO。

### R5. Deterministic commit candidate builder

- 新增 deterministic candidate builder，读取 current task、fresh Phase 2、scope ledger、
  dirty snapshot 与 AI public input，输出供 recorder/validator/executor 消费的 private
  candidate plan。
- Builder 只执行 objective path classification materialization、hash/mode/object/digest
  计算与 schema construction；scope、message semantics、path authorization、deployment/
  safety judgment、semantic pass 与 route intent 继续由 AI 拥有。
- 现有 exact staging、copy/rename、gitlink、hook execution、isolated index、rollback、
  Conventional Commit、unrelated preservation 与 transaction postconditions 必须保持不变。
- Revision/finding-fix/recovery 每次必须生成绑定 current Phase 2 digest、HEAD 与 dirty
  snapshot 的新 candidate sequence，不得复用 stale plan。

### R6. Eval corpus 与 9/35 closure

- 三个目标 package 各自新增唯一 canonical `evals/evals.json`，复用 #147 的 schema、runner、
  grader、adapter 与 run evidence contract。
- 每个 11 exit 与每个 structurally distinct input profile 必须绑定一个或多个 current case；
  同一 case 同时覆盖 profile 与 exit 时不得复制 case。
- `guru-create-task-commit:committed` case 只验证 DTO 可投影到 #131 input，不执行 Branch
  Review 行为。
- 新增 closure validator，读取 live registry、Stage 0 manifest、production manifest、
  Interfaces 与 corpora，并证明：

  ```text
  active_skill_ids == migrated_by_145 union migrated_by_146 union newly_active_1_3
  ```

- 当前基线闭包必须为 9 active Skills、35 exits；reserved/planned ids 不得进入 production
  migration set。`newly_active_1_3` entry 只有在 Interface 1.3、`minimal_handoff`、完整 public
  contracts 与 eval bindings 全部存在时才进入闭包。
- Missing、extra、duplicate、stale、platform-specific case binding、corpus byte mismatch、
  `legacy` active entry、unknown I/O state 或 coverage set difference 必须失败关闭。

### R7. Stage 0 clarification disposition projection

- Shared public dispatch 必须把 schema 正式值 `keep_current_open_issue` 投影为 `retained`。
- `keep_current_draft`、retarget/reopen/complete、全部 typed exit/consumer、semantic owner 与
  human confirmation 语义必须保持不变。
- 必须新增 checker-passed owner result 经真实 public wrapper 返回 `clear` + `retained` 的
  normal-path regression，并同步 canonical runtime、preset-installed copy 与 dogfood copy。
- #145 的 6 Skills/24 exits、optional fallback、actual-exit schema selection、四平台同 corpus
  与 atomic activation 必须通过回归。

### R8. Compatibility、upgrade 与原子切换

- 现有 active planning/check/commit state 必须通过 versioned re-entry 或 atomic activation
  进入 Interface 1.3；archive artifact 保持只读。
- Preset installer 必须在一个完整 transaction 中分发三包、production manifest、registry、
  extension inventory、runtime、schemas、wrappers、eval corpora 与 selected platform copies，
  禁止发布 mixed 1.2/1.3 production graph。
- 若现有 preset transaction 无法证明 consumer 全部 current，必须引入只转换 public DTO
  的 versioned adapter；adapter 不得读取 private artifact或重放 semantic judgment，并在
  三包全部 current 后删除。
- `trellis update`、pre-migration upgrade、preset reapply 与 dogfood drift 验证必须得到零
  unresolved `.new`/`.bak`/managed drift。

### R9. Docs SSOT 与分发

- Durable workflow/package/data/script/preset/public-doc specs 必须先更新，再实现 schemas、
  runtime 与 packages。
- Canonical source、installed `.trellis/guru-team/skills/`、shared/Codex/Claude/Cursor copies、
  registry、extension、workflow markers、migration manifests 与 corpora 必须通过同一 source/
  installed/closure validator。
- README 的 discovery、invocation、eval、install、update 与 reapply 命令必须在 clean
  throwaway repo 真实执行。

### R10. Workflow 与 semantic ownership 保持

- Workflow 继续只拥有 mandatory invocation、typed-exit route 与 fail-closed stop。
- 三个 Skills 继续拥有各自完整 semantic closed loop、AI Review Gate、触发式 human
  confirmation、recorder/checker 与 typed exit。
- Python/shell 只承担 executor、validator、recorder 与 deterministic builder；不得判断
  scope、adequacy、finding、semantic pass、human confirmation、route intent 或 PR readiness。
- #147 grader policy、semantic ownership、human review boundary、#131 Branch Review 内部行为
  与 Finish family 不得修改。

### R11. 场景边界

只覆盖 honest-but-fallible 协作下的正常执行、普通错误、stale/mismatch、re-entry、
finding fix、recovery、upgrade/update 与行为回归。恶意伪造、对抗性输入、威胁模型、
并发竞态压力、锁、TOCTOU、额外 fault injection、crash consistency 与跨 OS 原子性全部
属于 `out_of_scope`。

### R12. Semantic Skill authoring seed

- Interface 1.3 必须新增 consumer kind `skill_input_authoring_seed`。该合同由 target
  package 拥有，exact-ref target interface/profile，并分别声明 closed、互不相交的
  `seed_fields` 与 `authoring_fields`。
- Producer projection 继续只使用现有 `direct|select|rename|normalize` operation，从
  minimal output 消费全部 output properties 并只生成 `seed_fields`；不得新增 literal、
  default、merge expression、private lookup 或 semantic inference operation。
- Target package 必须提供 profile-specific authoring example，只包含 fresh caller AI
  负责的 `authoring_fields`。`seed_fields union authoring_fields` 必须精确覆盖 target
  profile top-level required fields，交集必须为空。
- Public invocation probe 必须先分别验证 seed 与 authoring example，再执行无覆盖 merge；
  任一重复、缺失、额外或 unknown field 必须失败关闭。合并结果必须完整通过 target
  profile schema 后才能调用 consumer。
- 该 kind 只用于
  `guru-approve-task-plan:revision_required -> revision_reentry`、
  `guru-check-task:passed -> guru-create-task-commit:initial_commit` 与
  `guru-create-task-commit:revision-required -> revision_reentry`。其它 Skill/workflow/stop
  consumers 保持现行合同。
- Shared schema、validator/public probe、representative fixtures、package contracts、eval
  cases、canonical/installed/platform copies、preset、throwaway、update/reapply 与 durable
  docs 必须同步验证；#144/#145/#147 的既有 public ids、projection operations、Stage 0
  identity 与 grader policy不得改变。

### R13. clarify_scope routing-only workflow target

- `guru-approve-task-plan:clarify_scope` 的唯一 consumer 必须改为 routing-only workflow
  target `guru-task-plan-clarify-scope-router`，并精确消费 `exit_id`、`task_ref`、
  `proposal_refs` 三字段 DTO。
- Router 只建立 scope context 并 mandatory invoke
  `guru-clarify-requirements:active_task_scope_change`；完整八字段 target input 必须由 caller AI
  基于 fresh live context 编写。
- 不得为该 edge 增加第 4 条 authoring seed，不得扩大 producer DTO、projection operation
  集合或 clarification target profile，也不得由 workflow、runtime 或 private artifact重建
  semantic judgment。
- Production manifest、workflow consumer contract、canonical/dogfood workflow、durable docs、
  fixtures、source/installed/preset/throwaway/update-reapply 验证必须同步。

### R14. task-local re-entry owner checker binding

- Shared `stage0_owner_result` 必须接收已通过 public input schema 验证的 input；只对
  `guru-discover-change-context:task_local_reentry` 将 exact `task_locator` 传给现有 checker，
  `pre_task` 继续使用 `task=None`。
- Owner-result locator 必须与 `task_locator/prior_snapshot_locator` 精确相同；mismatch、unsafe
  path 或 freshness failure 必须失败关闭，runtime 不得从 private artifact 推断 task。
- 不修改 public schemas、minimal DTO、typed exits、projection operations、semantic owner、
  human confirmation、#145 Stage 0 identity 或 #147 grader policy。
- 必须覆盖真实 task branch/task-local dirty wrapper pass、pre-task regression 与 locator
  mismatch negative case，并同步所有 canonical/installed/preset/dogfood 分发面。

### R15. private task worktree state evidence

- `guru-discover-change-context` task mode 的 private owner result、recorder 与 checker 必须增加
  exact `task_worktree_state` evidence，绑定 current HEAD 和完整 dirty path status/content
  identity，并确定性排除 `context-discovery.json` 自身；该 evidence 不进入 public DTO。
- AI Gate 必须审查 current dirty scope；load-bearing changed docs/code/tests 使用 working-content
  SHA-256。`task_local_reentry` 要求 live worktree 与 evidence 精确一致；新增、删除、内容、
  status、mode 或 rename drift 必须失败关闭。
- `pre_task` 与 standalone 继续要求 clean checkout；不得通过 stash、revert、index、提前提交
  或复制 private snapshot 绕过 task-mode binding，也不得无条件接受任意 dirty path。
- 必须覆盖 active-task dirty implementation pass、snapshot 后 drift fail、pre-task dirty fail
  以及既有 locator/freshness regressions，并同步 schema、runtime、packages、docs 与分发面。

### R16. formal task context snapshot replacement

- 只在 task mode 的 private recorder 增加参数
  `--expected-prior-snapshot-sha256`；pre-task、standalone、public input/output 与 typed exits
  保持不变。
- 对不同 bytes 的既有固定 `context-discovery.json`，recorder 必须先验证其为 regular、
  Git-trackable、schema/identity 自洽，并要求 prior `snapshot_sha256` 与显式 expected
  digest。
- 新 snapshot 必须在替换前完整通过 structural、live issue/base/blob/content/history、AI Gate
  与 R15 `task_worktree_state` 验证；任一失败都保持 prior bytes 不变。
- 验证通过后复用现有 `write_json` 替换固定 snapshot，并执行 read-back、trackability、
  identity、live freshness 与真实 public wrapper 检查。Formal replacement 时新 private
  snapshot 必须用 additive optional `superseded_snapshot_sha256` 精确绑定 prior；历史 snapshot
  继续只读兼容，initial task write 不要求该字段。
- 相同 bytes 重试的结果必须保持一致；不得新增 public DTO 字段、Skill/exit、versioned archive/current
  pointer、锁、TOCTOU、并发压力、hostile-input 防御，也不得执行 delete/copy/rename/stash/
  revert/stage/提前 commit。
- 必须覆盖 exact-prior pass、missing/wrong prior fail、invalid/stale new snapshot preserves
  prior bytes、idempotent same-snapshot、task-local wrapper `context_ready` 与 pre-task clean
  regressions，并同步 canonical/installed/四平台、extension hashes、docs 与 upgrade/update。

## 5. Requirement provenance matrix

| Requirement | Classification | Current authority | Design / execution locator | Acceptance |
| --- | --- | --- | --- | --- |
| R1 | `explicit_requirement` | #146 迁移集合与 active closure | `design.md` 2、3、8；`implement.md` Step 1、3、6 | AC1、AC2、AC8 |
| R2 | `explicit_requirement` | #146 Public I/O 迁移 | `design.md` 4；`implement.md` Step 2 | AC3 |
| R3 | `explicit_requirement` | #146 per-exit output、self-reentry、#131 handoff | `design.md` 3、5；`implement.md` Step 2、3 | AC4、AC5 |
| R4 | `explicit_requirement` | #146 private artifact boundary | `design.md` 6；`implement.md` Step 3、4 | AC3、AC4、AC12 |
| R5 | `explicit_requirement` | #146 deterministic candidate builder 与 transaction preservation | `design.md` 7；`implement.md` Step 4 | AC6 |
| R6 | `explicit_requirement` | #146 eval bindings 与 active closure | `design.md` 8；`implement.md` Step 1、5 | AC7、AC8、AC9、AC10 |
| R7 | `explicit_requirement` | #146 与 comment 5042976037 的 `accepted_current` projection | `design.md` 9；`implement.md` Step 4 | AC11 |
| R8 | `explicit_requirement` | #146 compatibility、upgrade、atomic activation | `design.md` 8、10；`implement.md` Step 6、8 | AC12、AC13 |
| R9 | `explicit_requirement` | #146 distribution gate 与仓库 Docs SSOT 规则 | `design.md` 11；`implement.md` Step 1、7、9 | AC13、AC14 |
| R10 | `explicit_requirement` | #146 非目标与仓库 Markdown/script ownership | `design.md` 1、6、7；`implement.md` Step 3、4、5 | AC6、AC10、AC15 |
| R11 | `explicit_requirement` | #146 场景范围与仓库 normal-operation boundary | `design.md` 10.3、13；`implement.md` 5、6 | AC15、AC16 |
| R12 | `confirmed_scope_expansion` | comment 5044522718 与精确 proposal/action confirmation | `design.md` 5.4、8、10、11、13；`implement.md` Step 2-8 | AC3、AC5、AC7、AC12、AC13、AC17 |
| R13 | `confirmed_scope_expansion` | comment 5045340918 与精确 proposal/action confirmation | `design.md` 3、5.2、9.2、10-11、13；`implement.md` Step 2-8 | AC4、AC5、AC13、AC18 |
| R14 | `confirmed_scope_expansion` | comment 5047220259 与精确 proposal/action confirmation | `design.md` 6、9.3、10-11、13；`implement.md` Step 4、7-8 | AC11、AC13、AC19 |
| R15 | `confirmed_scope_expansion` | comment 5049566946 与精确 proposal/action confirmation | `design.md` 6、9.4、10-11、13；`implement.md` Step 4、7-8 | AC11、AC12、AC13、AC20 |
| R16 | `confirmed_scope_expansion` | comment 5050065847 与精确 proposal/action confirmation | `design.md` 6、9.5、10-11、13；`implement.md` Step 4、7-8 | AC11、AC12、AC13、AC21 |

R7、R12-R16 分别承接 comments 5042976037、5044522718、5045340918、5047220259、
5049566946、5050065847 的 current authority；六个 `accepted_current` 语义均已由精确用户
确认与 GitHub-visible authority 固定，规划不新增或改写其产品语义。其余
design profile ids、opaque ref命名、独立 production manifest与 live-registry closure算法是
实现 R1-R6/R8-R10 的 `necessary_implementation_choice`；这些 choices不扩张产品范围或风险
范围，替代方案与选择理由记录在 `design.md` 13。

## 6. Issue scope ledger

- Close：#146。
- Related 且保持 open：#127、#131、#132。
- Closed authority refs：#144、#145、#147；本任务不 reopen，也不再次关闭。
- Follow-up：无。

## 7. Docs 状态

- Docs state：`complete_docs`。
- Strategy：`ssot_first`。
- Requirement impact：本任务改变 production public Skill I/O、consumer projection、
  target-owned authoring-seed contract、registry/extension inventory、preset activation、
  eval coverage、clarify_scope routing、active-task owner-checker/worktree binding、formal
  context snapshot replacement 与 upgrade contract，必须在同一 Phase 2 中同步 durable specs
  与 public README。
- 权威 Docs SSOT Plan：`design.md` 的 `## 11. Docs SSOT Plan`。
- Middle-platform Knowledge Gate：不适用；本任务不接入 go-guru、proto-guru、Unity3D
  Guru SDK、Flutter Guru SDK 或业务中台框架。

## 8. 验收标准

- [ ] AC1：3 Skills、11 exits 在 source/installed/workflow/registry/extension/production
  manifest 中集合精确一致，`revision-required` 未重命名。
- [ ] AC2：三个 entries 全部为 Interface 1.3 + `minimal_handoff`；9 个 active entries 不含
  `legacy`、unknown 或 missing I/O state。
- [ ] AC3：每个 input profile 有 closed schema、完整 example 与真实 invocation probe；
  public input 不含 runtime-derived facts 或 private artifact body。
- [ ] AC4：11 exits 各自拥有 output schema/example、唯一 consumer contract/projection，
  每个 output property 均有 direct-use proof。
- [ ] AC5：两个 self-reentry、passed-to-commit、committed-to-#131 与全部 workflow/stop
  consumers 通过 projection tests，且不读取 producer private artifact；前三条 semantic
  handoff 通过 R12 的 authoring-seed merge。
- [ ] AC6：Candidate builder、recorder、validator、executor 恢复现有 commit transaction
  semantics；copy/rename/gitlink/hook/rollback/Conventional Commit regressions 全部通过。
- [ ] AC7：三个 canonical corpora 覆盖本次全部 profiles 与 11 exits，并由 #147 runner
  实际执行 public wrappers；actual exit 决定 output schema，`expected_exit` 只执行事后断言。
- [ ] AC8：Closure validator 对 9 Skills、35 exits 与全部 input profiles 的 registry/I/O/eval
  set difference 为零。
- [ ] AC9：九份 canonical corpora 在 shared/Codex/Claude/Cursor adapters 下保持 byte
  identity；unsupported 平台返回已发布的 `unsupported`，不生成平台 corpus。
- [ ] AC10：Normal planning-to-check-to-commit-to-#131 transcript 与 eval trace 不读取或
  import private runtime source。
- [ ] AC11：`keep_current_open_issue -> retained` 真实 public wrapper regression 通过，
  #145 的 6 Skills/24 exits 与 atomic activation 无回归。
- [ ] AC12：Existing active re-entry、finding rerun、revision/finding-fix commit、recovery、
  archive read 与 freshness fixtures 通过，archive 无回写。
- [ ] AC13：Source、installed、dogfood、selected platforms、clean throwaway、pre-migration
  upgrade、`trellis update`、preset reapply 与零 sidecar/drift 门禁全部通过。
- [ ] AC14：Docs SSOT Plan 已执行，task delta 已合并到 durable docs，README 命令不依赖
  本机隐藏状态。
- [ ] AC15：Phase 2 `guru-check-task` 完整审查 requirements、design、code、schemas、tests、
  distribution、docs 与 task artifacts，并得到零 current-scope finding。
- [ ] AC16：Branch Review 覆盖 intake base `origin/main...HEAD` 完整 diff；PR body 只使用
  `Closes #146`，#127/#131/#132 只使用 open reference 语义。
- [ ] AC17：`skill_input_authoring_seed` 只出现在三条声明 edge；每条 edge 的 seed/authoring
  fields 不相交且 union 精确覆盖 target required fields，无覆盖 merge 后完整 target schema
  validation 通过；overlap、missing、extra、private lookup、runtime semantic reconstruction
  与新增 projection operation 负例全部失败关闭。
- [ ] AC18：`clarify_scope` 唯一投影到 `guru-task-plan-clarify-scope-router` 的三字段 workflow
  input；router mandatory invoke existing clarification owner，八字段 target input由 caller AI
  fresh authoring，且 authoring-seed edge 数仍为 3。
- [ ] AC19：`task_local_reentry` public wrapper 使用 validated `task_locator` 复验 owner result，
  exact prior locator pass；mismatch/unsafe/stale fail；`pre_task` 行为不变。
- [ ] AC20：Private `task_worktree_state` 精确绑定 HEAD 与排除 snapshot 自身后的完整 dirty
  state；active-task dirty scope pass，snapshot 后任一 path/status/content/mode/rename drift fail，
  `pre_task`/standalone dirty checkout fail，public DTO 不新增字段。
- [ ] AC21：不同 bytes 的 task context snapshot 只有在 exact expected prior 与新 snapshot 全部
  structural/live/worktree checks 通过后才替换；失败保持 prior bytes，相同 bytes retry 结果一致，
  replacement 精确记录 `superseded_snapshot_sha256`，真实 installed wrapper 返回
  `context_ready`。

## 9. 完成条件

AC1-AC21 全部获得命令、测试或 semantic review 证据，Docs SSOT reconciliation 完成，
Branch Review Gate 通过，且 PR readiness 对安全、部署、配置、schema、CI/CD、容器、K8s、
DB migration 与 Makefile 影响给出真实结论后，本任务才进入 `trellis-finish-work`。
