# #131 需求：实现 guru-review-branch 闭环 Skill

## 1. 目标

实现稳定公共 Skill：

```text
guru-review-branch
```

该 Skill 是 task work commit 之后完整分支审查的唯一 step-local SSOT。它独占
`origin/<base>...HEAD` 审查范围、独立审查代理交接、candidate scope qualification、
finding 生命周期、closure review、fresh final review、`review.md` 与
`review-gate.json` 的语义门禁。

全局 workflow 只保留 mandatory invocation、四个 typed exits、唯一 consumer 与
fail-closed stop，不再展开 Branch Review 的内部判断、恢复和 artifact 规则。

## 2. 权威与当前基线

### 2.1 当前权威

- GitHub Issue [#131](https://github.com/castbox/guru-trellis/issues/131) 正文定义 Skill
  定位、entry evidence、qualification-first、closed loop、四个 exits、artifact
  复用、上游边界与验收。
- [#131 accepted_current 评论](https://github.com/castbox/guru-trellis/issues/131#issuecomment-5045031945)
  固定 Interface 1.3、`exit_id`、#146 producer seed、target-owned authoring partition、
  real-wrapper eval、四平台 byte-identical corpus 与 #132 graph 验收。
- [#116](https://github.com/castbox/guru-trellis/issues/116) 及其
  [accepted_current 评论](https://github.com/castbox/guru-trellis/issues/116#issuecomment-5045033833)
  固定 `passed` 下游 seed 为 `task_ref`、`reviewed_head`、`review_ref`，并明确 #116
  独占 target input schema 与 authoring partition。
- 已合并的 #130、#144、#146 提供 `guru-check-task`、Interface 1.3、最小 typed handoff、
  `guru-create-task-commit:committed` 与 production eval 基线。
- `.trellis/spec/workflow/skill-package-contract.md`、当前
  `trellis/workflows/guru-team/workflow.md` 与本仓库 `AGENTS.md` 是仓库内执行约束。

### 2.2 Live baseline

- Intake base：`main` @ `ea132e350c4b6861fc955f17e590651a46e890ab`。
- 当前 registry 含 9 个 active Skills、35 个 exits，尚无 `guru-review-branch`。
- `guru-create-task-commit:committed` 输出固定为
  `exit_id`、`task_ref`、`base_ref`、`committed_head`；现有 workflow consumer
  只接收后三个字段。
- 当前 Phase 3.5 在 workflow 中展开 Branch Review prompt、reviewer lifecycle、
  finding route、artifact recorder 与 validator 规则。
- 当前 deterministic runtime 已提供 `review-branch`、`check-review-gate`、
  `agent-assignment.json`、`reviews/*.md`、`review.md` 与 `review-gate.json` 基础能力。
- Interface 1.3 接受 active Skill exit 指向 planned Skill，但 public consumer contract
  只能 exact-reference active target package。#116 尚未实现，因此 active #131 无法在
  不越权发布 #116 input schema 的前提下表达 `passed -> planned #116`。
- 当前 `exit_id` direct-use 检查只对一个历史 workflow edge豁免 routing identity投影；
  #116 固定 seed 不含 `exit_id`，需要把该规则收敛为通用、受限的 routing identity 规则。

## 3. 功能需求

### R1. Active Skill package 与稳定身份

- 新增 active `guru-review-branch` package，使用
  `schema_version=1.3`、`judgment_mode=semantic` 与固定阶段：
  `forward_behavior -> ai_review_gate -> conditional_human_confirmation ->
  recorder_validator -> typed_exit`。
- Workflow mode 与 standalone mode 使用相同语义门禁；standalone 只改变入口发现方式。
- Stable Skill id、input profile id、exit id、schema id、consumer id 与 runtime command
  均作为公共 API 管理。

### R2. Target-owned public input

- #131 独立拥有一个 closed structured profile `branch_review`，必填字段固定为：
  `profile`、`mode`、`task_ref`、`base_ref`、`committed_head`、`review_intent`。
- `mode` 枚举为 `workflow`、`standalone`。
- `review_intent` 枚举为 `initial_review`、`finding_fix_review`、
  `fresh_final_review`。
- `guru-create-task-commit:committed` 只提供 `task_ref`、`base_ref`、
  `committed_head`。#131 以 target-owned `skill_input_authoring_seed` 声明
  producer seed 与 `profile`、`mode`、`review_intent` caller authoring 的精确分区。
- Runtime 按 `task_ref` 读取并验证 planning、Phase 2、ledger、commit、Docs SSOT、
  assignment、raw reports 与 review artifacts。Public input 不携带这些 private bodies。

### R3. Complete review entry evidence

每次 invocation 必须绑定：

- current task、portable workspace boundary、base branch、current branch 与 current HEAD；
- 完整 committed range `origin/<base>...HEAD`；
- current `planning-approval.json`、`phase2-check.json`、
  `issue-scope-ledger.json`；
- current `guru-create-task-commit` evidence；
- approved Docs SSOT Plan 与 implementation reconciliation；
- `agent-assignment.json`、全部 task-local raw review reports 与 recovery chain；
- clean working tree，或仅含 owner contract白名单内的 task metadata tail。

缺失、failed、stale、range mismatch、HEAD mismatch、artifact digest mismatch、
workspace mismatch、unclosed reviewer lifecycle 均失败关闭。

### R4. Independent review 与 upstream ownership

- Skill 必须 dispatch 独立审查代理。问题发现、问题闭环、最终放行三个逻辑角色的
  assignment、liveness、reuse、replacement 与 raw report retention 必须可验证。
- Dispatch 使用未修改的 Trellis check/review agent。不得修改或 overlay
  `.trellis/agents/check.md`、`trellis-check` Skill、Codex/Claude/Cursor 对应的上游
  check agent 文件。
- Reviewer prompt、qualification contract、review loop 与 recorder/checker 调用顺序由
  `guru-review-branch` package 拥有。
- Raw reviewer output 不能直接成为 passing gate；必须先通过 Skill 内 AI qualification
  与 closure gate。

### R5. Qualification-first finding model

每个 candidate 按固定顺序处理：

1. 记录 affected behavior、path 与 evidence。
2. 绑定 requirement、approved planning contract、必要 correctness/compatibility invariant
   或已确认 scope expansion。
3. 只使用五个 scenario classes：
   `normal_required_behavior`、`explicit_nonstandard_requirement`、
   `approved_nonstandard_expansion`、`unconfirmed_nonstandard_proposal`、
   `out_of_scope`。
4. 只有前三类且违反当前交付合同时，才能分配 P0、P1、P2、P3。
5. `unconfirmed_nonstandard_proposal` 只形成 scope proposal，不能成为 finding，
   不能触发自动修复。
6. `out_of_scope` 只形成 observation 或 follow-up candidate。

普通继续、workspace 确认、planning approval、reviewer severity 均不能替代 exact scope
expansion confirmation。

### R6. Review closure 与 fresh final review

- Qualified P0-P3 finding 必须返回 implementation，完成
  `guru-check-task -> guru-create-task-commit -> guru-review-branch` 新一轮闭环。
- 每个 finding owner 必须有 fresh closure evidence。Closure round 产生的新 finding
  继续成为新的 finding owner。
- 全部 findings 关闭后，必须 dispatch 从未参与前序 review rounds 的 fresh final reviewer。
- Final reviewer 覆盖 current `origin/<base>...HEAD` 完整 diff，结果为零 P0-P3 findings
  才能形成 `passed`。
- Stale final review、closure reviewer兼任 final reviewer、未完成 replacement chain、
  raw report 缺失均不能通过。

### R7. Per-exit public outputs

四个 exits 使用独立 closed schema 与完整 example：

- `passed`：
  `exit_id`、`task_ref`、`reviewed_head`、`review_ref`。
- `implementation_required`：
  `exit_id`、`task_ref`、`reviewed_head`、`finding_refs`。
- `scope_confirmation_required`：
  `exit_id`、`task_ref`、`proposal_refs`。
- `blocked`：仅 `exit_id`。

完整 findings、proposal bodies、review narrative、artifact paths、hash bundle、agent
metadata 与 recovery history 均为 private gate evidence，不进入 public output。

### R8. 唯一 consumer 与 planned #116 bridge

- `passed` 指向 planned `guru-review-task-publication`。#131 只声明三个 producer seed
  字段及其薄 projection，不定义 #116 profile、input schema 或 authoring fields。
- Interface 1.3 新增 additive `planned_skill_input_seed` consumer contract。它仅适用于
  registry state 为 `planned` 的 Skill，只登记非空 seed field set，不能引用 target
  interface、profile、authoring example、private state或 runtime inference。
- planned target 在运行时不可调用；`passed` 到达该边界时必须因 target package缺失而
  fail closed。#116 激活时必须把 bridge 替换为 target-owned
  `skill_input_authoring_seed` 并重新完成完整 target schema proof。
- `implementation_required` 指向 routing-only workflow target，随后进入 implementation、
  `guru-check-task`、`guru-create-task-commit`、`guru-review-branch`。
- `scope_confirmation_required` 指向 routing-only workflow target。Caller AI fresh-read
  proposal 与 authority 后，完整编写
  `guru-clarify-requirements:active_task_scope_change` input；router 不新增
  authoring-seed edge。
- `blocked` 指向 zero-payload stop。
- `exit_id` 是 typed route discriminator，无需进入 non-stop consumer payload；除
  `exit_id` 外，每个 output field 必须具有 direct consumer use。

### R9. Artifact SSOT 与 script 边界

- 复用并演进 `reviews/*.md`、`review.md`、`review-gate.json`、
  `agent-assignment.json`，不新增平行 Branch Review pass artifact。
- Finding lifecycle 记录 requirement refs、scope basis、scenario class、qualification、
  severity、owner、closure evidence 与 reviewed HEAD。
- AI 先完成 scope、severity、adequacy、pass/fail、route 与 confirmation 判断；
  recorder 后写 evidence，validator 后校验 schema、range、HEAD、hash、lifecycle 与 freshness。
- Python/shell 不得选择 scenario class、severity、scope route、finding disposition、
  reviewer充分性或 final pass。

### R10. Real public wrapper 与 eval corpus

- Package 发布 thin `scripts/invoke.sh`，通过 shared `run-skill-command` 调用既有 owner
  recorder/checker，并只序列化 checker-passed actual exit。
- `expected_exit` 只用于 wrapper 返回后的断言，不能进入 native request、owner result、
  route selector 或 runtime semantic judgment。
- Canonical `evals/evals.json` 覆盖四个 exits、workflow entry、standalone entry、
  finding-fix review 与 fresh-final review。
- Shared、Codex、Claude、Cursor 使用 byte-identical corpus；Codex trusted Git root、
  Claude safe input、Cursor unsupported/unavailable 与 shared parsing 均进入验收。

### R11. Workflow、distribution 与 upgrade

- Canonical workflow 用一个 mandatory invocation 与四个 exit markers替换当前 Phase 3.5
  内部合同；只保留全局 route 与 fail-closed transition。
- #146 production migration manifest的 3-Skill/11-exit集合与 activation identity保持不变；
  `guru-create-task-commit:committed` consumer/projection binding切换到 #131 target profile，
  authoring-seed edge清单从 current 3 条同步为 4 条。
- Canonical package、installed package、shared/Codex/Claude/Cursor Skill copies、
  registry、extension inventory、workflow、runtime、schemas、tests 与 public docs
  必须同步。
- Preset apply 必须从 canonical source生成 installed/dogfood copies。不得把 dogfood
  副本作为唯一修改源。
- Clean throwaway init、existing-project workflow switch、preset install、
  `trellis update`、preset reapply、dogfood drift、`.new/.bak` 检查均必须通过。

### R12. 正常运行边界与非目标

本任务只覆盖 honest-but-fallible 协作下的正常执行、普通错误、stale/mismatch、
finding fix、review recovery、install/update 与兼容性路径。

明确不实现：

- 恶意 actor、故意伪造或篡改 artifact/evidence/hash/state；
- 对抗输入、威胁模型、额外 anti-tamper 或 anti-forgery 机制；
- 未被正文要求的竞态压力、TOCTOU、锁、原子写入协议、fault injection、
  crash consistency、跨 OS 原子性；
- `guru-review-task-publication`、最终发布事务、push、PR mutation、archive；
- 独立 `guru-qualify-review-findings` wrapper；
- upstream `trellis-check` Skill/Agent 修改或 overlay。

## 4. Issue scope ledger

- Close：#131。
- Related 且保持 open：#127。
- 已完成 authority refs：#130、#144、#146；本任务不重新关闭。
- Follow-up 且保持 open：#116、#132。

## 5. Docs 状态

- Docs state：`complete_docs`。
- Strategy：`ssot_first`。
- Requirement impact：本任务新增公共 Skill、Interface 1.3 planned-consumer bridge、
  review artifact contract、workflow route、runtime commands、eval corpus、preset
  distribution 与 upgrade contract，必须同步 durable specs 和 public README。
- 权威 Docs SSOT Plan：`design.md` 的 `## 12. Docs SSOT Plan`。
- Middle-platform Knowledge Gate：不适用；本任务不接入业务中台 SDK 或 framework。

## 6. 验收标准

- [ ] AC1：`guru-review-branch` 在 registry、source package、installed package、
  extension inventory、workflow markers 与 selected platforms 中为同一 active Skill。
- [ ] AC2：`branch_review` input schema、完整 example 与 wrapper invocation通过；#146
  seed 与 #131 authoring fields 不相交且 union 精确覆盖 required fields。
- [ ] AC3：Entry checker拒绝缺失、failed、stale、range mismatch、HEAD mismatch、
  workspace mismatch、non-metadata dirty state 与未闭合 reviewer lifecycle。
- [ ] AC4：Independent reviewer 使用未修改 upstream agent；raw report 必须经过
  qualification 与 closure gate，不能直接成为 pass。
- [ ] AC5：五类 scenario互斥；qualification先于 severity；未确认 proposal不产生
  P0-P3 或 implementation route；out-of-scope candidate不阻塞。
- [ ] AC6：Finding fix 强制经过 fresh Phase 2、fresh commit、closure review 与 fresh
  final review；finding owner、closure reviewer、final reviewer角色约束全部通过。
- [ ] AC7：四个 outputs 使用 `exit_id` 和独立 schema/example；除 routing identity 外，
  每个 public field均有唯一 direct consumer use。
- [ ] AC8：`passed` 只向 planned #116提供三个 seed字段；#131 不发布 #116 input
  schema；planned package缺失时运行时 fail closed。
- [ ] AC9：`implementation_required` 唯一返回 task work chain；
  `scope_confirmation_required` 唯一进入 clarification router；`blocked` 唯一进入 stop。
- [ ] AC10：`reviews/*.md`、`review.md`、`review-gate.json`、
  `agent-assignment.json` 保持唯一 artifact链，schema/hash/HEAD/range/freshness validator通过。
- [ ] AC11：Runtime traces证明 script不判断 scope、scenario、severity、route或 final pass。
- [ ] AC12：Package corpus覆盖四个 exits、两种 mode、finding-fix review 与 fresh-final
  review；actual exit 决定 schema，四平台 corpus bytes一致。
- [ ] AC13：Workflow 不再复制 Branch Review 内部合同；mandatory invocation 与四个 exits
  各有一个唯一 consumer。
- [ ] AC14：Production migration manifest保持 3-Skill/11-exit集合，committed binding指向
  #131，authoring-seed edges精确为 4；live active closure为 10 Skills/39 exits。
- [ ] AC15：Source、installed、dogfood、selected platforms、clean throwaway、
  `trellis update`、preset reapply、零 unresolved `.new/.bak` 全部通过。
- [ ] AC16：Docs SSOT Plan 已执行，task delta合并到 durable docs，公开安装命令在
  throwaway repo真实运行。
- [ ] AC17：独立 Phase 2 与 Branch Review 覆盖本任务全部 requirements、design、code、
  schema、tests、distribution、docs、deployment/safety 影响，且 current-scope finding为零。

## 7. 完成条件

AC1-AC17 全部获得命令、测试或独立语义审查证据，Docs SSOT reconciliation完成，
task work commit创建，`guru-review-branch` 对 current `origin/main...HEAD` 自身完成
fresh final review并返回 `passed`。发布、PR 与 issue关闭继续由 #116/#132 后续链路处理。
