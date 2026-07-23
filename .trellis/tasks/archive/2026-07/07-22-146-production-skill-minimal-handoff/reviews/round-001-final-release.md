# Issue #146 Branch Review Round 001 最终放行审查报告

## 审查身份与结论摘要

- 逻辑角色：最终放行审查代理
- technical agent：`/root/review_146_final_r1`
- reuse_decision：`new-agent`
- issue：`https://github.com/castbox/guru-trellis/issues/146`
- base：`origin/main` / `7dc67e9aef08ca4928159d7d13db6fdbd40c5d4c`
- reviewed_head：`e3efc635e36039f0db94a9d24eddad676ad7fe7b`
- diff range：`origin/main...HEAD`
- diff scope：`1` 个提交、`621` 个路径
- findings_count：`2`（P1=`1`，P2=`1`）
- 结论：`blocked`

本轮直接审查固定 base 到 reviewed HEAD 的完整已提交差异，不以 Phase 2
摘要、测试绿灯或 commit candidate 代替语义审查。本代理只新增当前 raw report；未修改实现、
规划、spec、runtime、gate artifact 或其它 task metadata，未运行 recorder/review gate，未
commit、push、创建 PR、finish-work 或关闭 issue。

## 审查范围与证据源

本轮 fresh 读取并交叉检查：

- live Issue #146 正文及全部 scope clarification / exact confirmation 评论；
- `prd.md`、`design.md`、`implement.md`、planning approval、contract wording review、
  `issue-scope-ledger.json`、Phase 2 check、implementation handoff、commit plan/candidate；
- 完整 `origin/main...HEAD` diff、提交内容、当前 worktree/index 与 source/installed inventory；
- 三个 production Skill package 的 public I/O、profiles、interfaces、schemas、examples、
  eval corpora、consumer/projection、migration manifest、registry 和 runtime dispatch；
- canonical/dogfood workflow、companion runtime、preset installer、platform copies、durable
  specs、公开文档、测试与 throwaway/update/reapply evidence；
- CI/CD、container、K8s/Kustomize、DB migration、Makefile、secret-like path/content、
  `.new/.bak`、overlay drift 与 unrelated-change preservation。

Issue #146 ledger 只记录五个 `accepted_current` proposal：authoring seed、
`clarify_scope` router、task-local owner checker binding、task worktree state binding 与 formal
context snapshot replacement。它们分别绑定用户 exact confirmation 和 live issue-comment
authority；其中没有 production eval runner/adapter 修改授权。

## Findings

### P1-F001：未获 scope-change 授权即修改 #147 production eval adapter

- 主要位置：`trellis/skills/guru-team/adapters/eval/native_adapter.py:24`；相关实现位于
  `:1254` 与 `:1750`。
- 当前 commit 对该文件新增 `483` 行、删除 `1` 行，加入三个 production Skills 的 owner
  fixture、wording/evidence 构造和 `PRODUCTION_SKILLS` dispatch。这不是仅增加 #146 package
  corpus 数据，而是实质扩展 shared native adapter 的生产执行行为。
- Issue #146 正文明确把 #147 eval runner/adapter 排除在当前修改面之外；首条 scope
  clarification 又明确要求：若 corpus 无法在既有 #147 adapter 上运行，必须先形成具体
  proposal/action、经用户 exact digest confirmation、刷新 live authority、planning 与 approval，
  才能修改该 adapter。
- `issue-scope-ledger.json` 中五个已确认 proposal 均不包含 adapter；`implement.md:233-261`
  的预计修改面也不包含 `trellis/skills/guru-team/adapters/eval/native_adapter.py`。因此当前
  adapter diff 没有可追溯的 current-scope authority。

正常复现不依赖篡改或恶意输入：运行三个新增 production corpora，owner staging 会在
`skill_id in PRODUCTION_SKILLS` 时进入新增 dispatch，并执行本次新增 fixture/evidence 构造。
也就是说该越界修改已经参与支持的正常 eval 路径，而非死代码或仅测试注释。

影响：实现绕过了 #146 已建立并多次执行的 Scope Change Gate，令 commit 包含一个由 #147
拥有、但未经本 issue exact confirmation 的运行时行为变更。即使相关 corpora 全部通过，也
不能把 implementation 后写入的 adapter 代码反向解释为用户授权；当前 close #146、PR
readiness 与 reviewed scope 均不成立。

修复要求（二选一，不得由 reviewer 代选）：

1. 撤销本 issue 对 native adapter 的修改，并证明新增 corpora 可由既有 #147 adapter 合法
   执行；或
2. 返回 Scope Change Gate，提交最小且证据绑定的 adapter proposal/action，由用户 exact
   confirmation 后刷新 issue authority、context snapshot、planning、approval，再实现该变更。

无论采用哪条路径，均须重跑完整 Phase 2、创建新的 exact commit candidate/commit，并由
fresh final-release reviewer 审查新的完整 diff。

### P2-F002：`clarify_scope` workflow target 只有 marker，没有 mandatory clarification 路由合同

- 主要位置：`trellis/workflows/guru-team/workflow.md:918`；dogfood
  `.trellis/workflow.md` 同步存在相同缺口。
- `guru-approve-task-plan:clarify_scope` 在 `:911` 把唯一 consumer 指向
  `guru-task-plan-clarify-scope-router`，但 target marker 后立即进入 `1.5 Activate task`。marker
  与下一节之间没有 `guru-clarify-requirements`、`active_task_scope_change`、mandatory invoke、
  fresh scope-context authoring 或 stale/mismatch fail-closed 行为。
- `prd.md:261-273` 要求 router 精确消费 `exit_id`、`task_ref`、`proposal_refs` 三字段 DTO，
  只建立 scope context，然后 mandatory invoke
  `guru-clarify-requirements:active_task_scope_change`；完整八字段 input 必须由 caller AI 基于
  fresh live context 编写。仓库全局合同又规定跨 Skill transition 与 mandatory invocation
  由 workflow SSOT 显式定义，marker 本身不能代替执行合同。

正常复现不依赖伪造 artifact：让 planning review 在真实 scope ambiguity 下返回已通过 schema
的 `clarify_scope` exit，workflow 能解析出 consumer target，但 AI 到达 line 918 后没有任何
可读取的续接指令来建立 fresh scope context、编写 clarification input 或 mandatory invoke
目标 Skill。流程只能停在空 marker、猜测行为，或错误继续到只允许 `approved` 进入的 task
activation。

影响：R13 的 public DTO/consumer marker 虽已机器闭合，但用户确认的 routing-only 正向行为
没有进入实际 AI runtime contract。README/spec 对该行为的描述不能代替 `.trellis/workflow.md`
中的 mandatory invocation；现有 closure/corpus 测试只证明 marker/schema 集合，未证明正常
运行时可从 `clarify_scope` 唯一续接到 clarification Skill。

修复要求：在 canonical workflow target 附近补充 routing-only 运行时合同，明确：

- 只消费三字段 DTO，并验证 exit/consumer/task identity 与 freshness；
- 由 caller AI 基于 fresh live issue/task context 建立 scope context并编写完整八字段 input；
- mandatory invoke `guru-clarify-requirements:active_task_scope_change`；
- unknown、missing、stale、mismatch 或无法形成唯一输入时 fail closed；
- 不把 semantic judgment、第四条 authoring seed 或扩大 producer DTO 引入 workflow。

同步 dogfood workflow，并增加能验证上述行为文本与 route linkage 的 canonical/installed
regression。随后重跑完整 Phase 2、commit 与 fresh final release review。

## 需求、规划与实现承接判断

- 三个 production Skills 的 minimal public I/O、11 profiles/exits、consumer projections、
  private checkpoint ownership、source/installed/platform distribution 大部分按 R1-R12、R14-R16
  完成，9 active Skills / 35 exits / 21 targets 的 closure 没有 legacy residue。
- 五个已确认 scope proposals 均已进入 ledger、规划与实现；本轮没有发现 authoring seed、
  task-local locator、task worktree state 或 formal snapshot replacement 的新的 current-scope
  correctness finding。
- R13 只有 schema/consumer marker 与 durable-doc 描述完成，workflow 正向行为未完成，因此
 不能判定全部 R1-R16/AC 已被实现。
- Native adapter diff 不在 approved planning/change authority 中；这是 release-blocking scope
  violation，不得用“为了测试而需要”或 Phase 2 passing evidence降级为观察项。

## Phase 2、commit 与工作区 freshness

- `phase2-check.json` SHA-256：
  `c0f91fad9e457cf19665c7219353aa734e6af6f1d1796b2aa5ef5465cf1fc9b0`。
- Phase 2 pre-commit snapshot 为 base HEAD；其 `619` 个 dirty paths 全部属于当前 commit 的
  `621` 个 paths，commit 只额外包含 task metadata `phase2-check.json` 与
  `task-commit-plans/001.json`，没有未覆盖的 non-metadata source drift。
- commit candidate 共 `621` paths，`unrelated_preserved=true`、`hook_mutation=false`；live
  candidate 状态为 `committed`，commit 中的 plan blob仍保持不可变 `planned`，符合既有
  transaction 设计，不应为了本轮 finding 创建伪造或重复的 `002` plan。
- 审查开始时仅 `agent-assignment.json` 与 `task-commit-plans/001.json` 为合法 task metadata
  tail；raw report写入后应只额外出现本报告。两个 finding 针对 committed implementation/
  workflow，不是由 metadata tail 引起。

上述 ancestor coverage 证明 Phase 2 evidence 与 commit 没有普通 source 漂移，但不能弥补
Phase 2 semantic review漏掉的 scope authority 与 runtime workflow 行为问题。

## 独立验证与通过证据

本轮在 reviewed HEAD 上独立重跑并确认：

- package suite：`162 passed`；
- workflow runtime suite：`557 passed, 13 skipped`；
- preset suite：`45 passed`；
- upstream ownership suite：`6 passed`；
- canonical source / installed closure：均为 `9 Skills / 35 exits / 21 targets / 0 legacy`；
- installed inventory：`1711` managed files，sidecar/removal/conflict 均为 `0`；
- canonical/installed companion runtime与 workflow bytes一致，dogfood overlay drift通过；
- 所有 changed JSON可解析，task context、workspace boundary、Python compile、Bash syntax、
  `git diff --check origin/main...HEAD`、`.new/.bak` 与 secret-like scan通过。

Phase 2 记录的完整 throwaway public-marketplace discovery + local unpublished workflow/preset
fresh install、update、preset reapply 与 pre-#146 upgrade均 exit `0`；本轮核验该证据与当前
commit ancestor/path coverage，没有重复执行数百万字节输出的完整 throwaway。

这些绿灯支持未被 finding 指向的 package/runtime/distribution 部分，但不覆盖“用户是否授权
修改 adapter”的 semantic authority，也没有断言 workflow target marker 后存在 AI-readable
mandatory invocation，故不改变 blocked 结论。

## Docs SSOT

Phase 2 `docs_ssot_plan` 的 15 个 durable paths 当前 SHA-256 全部匹配，公开 README、workflow
README、preset README 与 durable specs 对 minimal handoff、clarification routing、install/update
的描述总体一致。`.trellis/spec/workflow/index.md` 也被提交且内容与新 contracts 协调，但未列入
这 15 个 durable paths；因 `implement.md` 已把它列入预计修改面且当前内容正确，本轮仅记录为
nonblocking evidence note。

Docs SSOT 最终判定仍为 `fail`：文档描述的 `clarify_scope -> mandatory clarification Skill`
没有落实到 canonical/dogfood workflow runtime contract，属于实现与 SSOT不一致；adapter 的
未授权 scope expansion 也不能由文档补记自动合法化。

## Scope ledger、问题生命周期与发布语义

- close issue：`[146]`
- related issues：`[127, 131, 132]`
- follow-up issues：`[]`
- 当前 acceptance evidence仍为空，符合 publish transaction 前状态。

本轮是 Round 001 final release，两个 finding 的 owner 为
`/root/review_146_final_r1`。后续必须先分别处理 P1 scope decision 与 P2 implementation；修复后
由 closure reviewer关闭本轮 findings，再使用新的 final-release reviewer检查完整最新 diff。
在此之前不得写 passing Branch Review Gate，不得把 `Closes #146` 发布为 ready PR 论证，也
不得 finish-work 或关闭 issue。

## 安全、兼容性与部署影响

- 未发现 token、secret、private key、签名 URL、`.env`、客户数据或敏感原始记录进入 diff。
- 未修改 CI/CD、Docker/container、K8s/Kustomize/Helm、DB migration、Terraform、proto 或
  Makefile；没有生产数据写入、部署或迁移副作用。
- source/installed/platform copies 与 pre-#146 upgrade证据支持分发兼容性；两个 finding 分别
  是 scope authority 与正常 AI workflow correctness，不扩展到恶意篡改、并发竞态、TOCTOU、
  hostile input 或其它 AGENTS.md 明确排除的场景。
- P2 会影响真实 planning scope-change 正常路径，因此不是理论防御性加固；P1 的正常 corpora
  dispatch 已进入新增 adapter branch，因此也不是仅靠手工篡改构造的越界案例。

## 未验证边界

- 分支在审查时尚未 push，无法安装 exact current-branch remote marketplace ref。已通过 public
  marketplace discovery 与 local unpublished workflow/preset throwaway；该限制非本轮新增
  finding，但必须继续保留在 PR readiness。
- 本轮没有调用真实 GitHub PR publish/merge/close，也没有把 throwaway 测试解释为真实生产发布。

## 最终结论

- P0：`0`
- P1：`1`
- P2：`1`
- P3：`0`
- findings_count：`2`
- reviewed_head：`e3efc635e36039f0db94a9d24eddad676ad7fe7b`
- reuse_decision：`new-agent`
- final verdict：`FAIL / BLOCKED`

当前 commit 不满足 Issue #146 最终放行条件。P1 必须返回 Scope Change Gate（或撤销 adapter
越界修改），P2 必须返回 implementation补齐 canonical/dogfood workflow 的 routing-only
mandatory invocation 合同。两项完成后必须执行 fresh planning/approval（P1 选择 scope expansion
时）、完整 Phase 2、new exact commit 和 fresh final release review；当前禁止 Branch Review
Gate passing、push/PR readiness、finish-work 与 issue close。
