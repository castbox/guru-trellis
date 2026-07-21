# Guru Team Trellis 已实现扩展总览

本文按重要性说明本仓库已经在官方 Trellis 之上建设的扩展。内容基于本 repo 全量
GitHub issue / PR 历史，包括已 closed issue、已 merged PR、已 closed 未合并 PR，
并在后续维护中追加当前 active issue 已形成的长期能力。

重点不是重新写一份抽象流程，而是把历史迭代已经沉淀出的 Trellis 扩展能力分类，并说明
每类能力的职责边界、实现资产和历史来源。

## 1. P0：Workflow 主合同与日常入口

`guru-team` workflow 是本仓库最核心的扩展。它通过官方 Trellis workflow marketplace
机制安装到目标仓库，并把 Guru Team 的任务流程定义为 Markdown 合同，而不是依赖脚本
或 hook 分叉。

历史来源：

- Issue #1 / PR #4：中台知识门禁与 Repo Docs SSOT。
- Issue #64：Phase 1 `Docs SSOT Plan` planning 合同，明确 docs 状态、同步策略和 task artifact delta merge 责任。
- Issue #65：Phase 2 implementation/check 消费 `Docs SSOT Plan`，把 docs 同步执行和一致性复核纳入实现 handoff 与 `trellis-check`。
- Issue #66：Phase 3 / Branch Review / finish-work / PR body 只验证 Phase 2 Docs SSOT reconciliation 已完成，不首次执行 docs merge。
- Issue #122：Phase 2 pass 后的 task work commit 收敛为公共
  `guru-create-task-commit` closed-loop skill，并在 finding fix 后以 fresh evidence
  重复进入；candidate 与 executor 必须拒绝 merge/cherry-pick/revert/rebase/
  sequencer/am 等非普通 Git operation state，dirty snapshot 必须绑定 initialized、
  clean gitlink 的 worktree HEAD，并把该 artifact OID 直接绑定到 exact index；普通
  path 使用既有 SHA-256/mode/delete identity，rename 与 copy 分别由
  `renamed_from` / `copied_from` 表达；只有 rename source 可以继承 destination
  的删除/exact-stage authority，copy source 若 dirty 必须独立分类。Candidate self
  使用 validated plan deterministic bytes，所有 hook/commit 先在 isolated
  transaction 完成再发布。
- Issue #125：`workflow` / `standalone` 保持稳定 mode id，并只表达 global routing 与
  direct discovery 差异；两者都依赖完整 Guru Team extension runtime。Interface schema
  1.1、installed manifest、`run-skill-command` shared dispatcher、installer inventory 与
  public docs 必须共同证明 non-portable/fail-closed 合同。
- Issue #144：保留 public Skill interface 1.2 legacy 语义并新增独立 1.3 minimal
  handoff 合同。Registry 1.1 以 exact `interface_schema_id` 和
  `io_contract_state` 选择版本；1.3 将 caller-owned input、exact invocation、per-exit
  output、consumer-owned input、thin projection 与 private artifacts 分开声明，公开
  `discover-skill-contract`。Skill consumer 必须引用 target-owned input 并绑定 active
  registry 的 exact canonical target interface path 与 target interface id；非 direct
  projection 与 direct 到 scalar CLI 必须证明所有合法 producer output 可消费，
  public/private schema id 与 path 分别互斥，wrapper 必须可确定性证明只路由 shared
  dispatcher。#144 交付时，九个 production Skills 全部维持 1.2 `legacy`，1.3
  只由 mixed test-only fixture 验证；随后 #145 已把六个 Stage 0 Skills 及其 24 exits
  原子迁移到 `1.3+minimal_handoff`，#146 的 planning/check/commit 三包仍保持
  `1.2+legacy` 并由 #146 负责后续迁移。
- Issue #110：Phase 0 在任何 repo/network semantic read 前 mandatory invoke
  `guru-sync-base`。Skill 拥有 selected-base resolve/sync/validate 闭环，workflow
  只消费 `synced` / `skipped` / `blocked`。
- Issue #111：`synced` mandatory invoke semantic `guru-discover-change-context`。
  Workflow 与 standalone 使用相同 freshness preconditions，固定先读取 live change 与
  duplicates、审查 updated-base Docs/code/tests，再对 archived
  `finish-summary.json:index.*` 执行一次 versioned preview。AI 选择 1 至 3 个候选窄读，
  零候选仍成功；`context_ready`、`refresh_base`、`blocked` 分别唯一进入
  active Skill `guru-clarify-requirements`、active Skill `guru-sync-base` 和
  fail-closed stop。Deep-read locator 必须按 task artifact、
  canonical GitHub issue/PR、exact Git object/ref 分型校验；closed schema 与结构化 locator
  不保存 raw source payload，只做 field-specific validation。
- Issue #113：激活 semantic `guru-clarify-requirements`，统一 initial intake
  clarity、active-task scope change 与 standalone clarification review；先穷尽
  repository-answerable evidence，再按单问题循环收敛，并在 source-of-truth mutation
  前取得 action/proposal digest-bound confirmation；active-task `clear`/`new_task` 要求
  非空 terminal proposal set，五类 scope classification 均要求 exact 用户证据，
  `mechanism_removed/replaced` 无 confirmation/trail/mutation；当前 planning evidence 复用
  shared `guru-planning-approval-2.0` 完整 validator。
- Issue #2 / PR #3：对齐 Trellis auto-bootstrap start model。

Canonical 资产：

- `trellis/index.json`
- `trellis/workflows/guru-team/workflow.md`
- `trellis/workflows/guru-team/README.md`
- 本仓库 dogfood 运行副本 `.trellis/workflow.md`

已实现能力：

| 能力 | 说明 |
| --- | --- |
| 固定 marketplace id | `trellis/index.json` 暴露 `guru-team` workflow，稳定安装使用 `trellis init --workflow guru-team --workflow-source gh:castbox/guru-trellis/trellis#vX.Y.Z`，latest/canary 才使用不带 `#ref` 的 source。 |
| Phase 0 intake | AI 先在 tool-free 阶段分类 request；repo-changing route mandatory invoke deterministic `guru-sync-base`。`synced` 后依次 mandatory invoke semantic `guru-discover-change-context`、`guru-clarify-requirements`、`guru-review-contract-wording:change_request`、`guru-review-change-request` 与 active `guru-create-task-workspace`。Readiness `ready` 只进入 workspace Skill；该 Skill 复验五个 prerequisite result、展示 exact plan、完成 AI Gate 与当前 invocation 专用 confirmation，再调用 deterministic recorder/executor/checker。Workspace executor 通过隔离 adapter 调用 official `common.task_store.cmd_create`，仅在该 handler 调用内禁用 developer accessor，并强制 `task.json.creator=task.json.assignee=reviewed login`；existing official identity bytes 保持不变。External exits 固定为 `created`、`refresh_review`、`cancelled`、`blocked`。 |
| Change-context history 与 snapshot | History engine 只能读取 `.trellis/tasks/archive/**/finish-summary.json:index.*`，以 `guru-context-history-score-1.0` 产生稳定 query/manifest/preview digest、invalid isolation、排序和 limit 20 projection；普通 non-file/read/JSON/index-shape failure 形成 portable invalid evidence。Pre-task snapshot 只走 stdout；task 创建后由 `guru-create-task-workspace` 将 checker-passed exact bytes 写入 task-local `context-discovery.json`。不得读取 `.trellis/workspace/**`、runtime、repo-level index/cache；closed schema 与结构化 locator 不保存 raw source payload。 |
| Intake clarity / scope evolution | `guru-clarify-requirements` 是 active semantic closed-loop Skill。它加载 `trellis-brainstorm` 作为单问题问答方法，但独占问题选择、收敛、scope/action、semantic Gate 与 typed route 判断。Repository-answerable `answered` 必须有 checked evidence；每轮 `question_id` 必须来自本轮 opened 或既有 open set，且 reducer 固定为 `open_questions = opened - closed`。GitHub comment/body mutation 必须把 human-confirmed exact payload、payload digest、mutation result与live content绑定；成功后返回 `refresh_context`。Pre-task/standalone stdout-only，无专用 clarification artifact；active-task `clear`/`new_task` 要求非空七类 terminal proposal set，五类 scope classification 无论 origin 均要求 exact 用户证据并 exact 写入当前 ledger structured trail；`mechanism_removed/replaced` 要求 optional origin、null confirmation，且不进入 trail/action mutation。Trail 绑定 live GitHub authority content/`updated_at`、shared `guru-planning-approval-2.0` validator 通过的 planning approval/docs、review/stale/re-entry evidence；context `generated_at` 不早于 authority `updated_at` 后 task update 绑定该 digest，不要求第二次 context refresh。`new_task` 保留当前 task trail，只把 side-effect-free draft 交给 #112。Active-task Scope Change Gate mandatory invoke本 Skill，`clear` 由 caller-aware router恢复 initial wording、standalone caller、active planning或exact interrupted progression。 |
| 业务项目中文文档默认规则 | 业务项目 `.trellis/spec/**`、`.trellis/tasks/**`（含 `reviews/*.md` raw reports 与 `review.md` rollup）、`docs/**` durable docs、`00-bootstrap-guidelines` 生成或补齐的 docs SSOT，以及 workflow artifact human-readable 字段默认中文；literal token 可保留英文。 |
| Phase 1 planning | Trellis task 创建后写中文 `prd.md` / `design.md` / `implement.md`，并定位同一个 `Docs SSOT Plan`；current wording pass 后 mandatory invoke `guru-approve-task-plan`。该 Skill 完成 adequacy/provenance/unusual proposal/AI Gate、展示三份 task-local 规划文档链接并取得独立 post-planning confirmation；Phase 0 handoff 或普通确认不能替代专用 proposal confirmation。只有 `approved` 进入 task activation。 |
| Phase 2 execute/check | 默认 sub-agent mode 下实现由 `trellis-implement` / channel `implement` 完成并输出 handoff；official unchanged `trellis-check` / channel `check` 只提供 raw review evidence。Workflow 随后 mandatory invoke active semantic Skill `guru-check-task`，由该 Skill 独占完整 task-scope adequacy、scope qualification、current-scope severity、finding/full-rerun loop、Docs SSOT reconciliation、最终 AI Gate、`phase2-check.json` 与四个 typed exits。实现/check 都必须消费 Phase 1 `Docs SSOT Plan`，按 `ssot_first` / `delta_first` / `bootstrap_or_repair_docs` / `no_docs_update_needed` 策略说明 docs 同步结果并复核 durable docs / task artifacts / code / test 一致性；不用 worker 输出、主会话自检、coverage flags、命令 exit 0 或 recorder/checker 成功替代 semantic pass。 |
| Phase 3 task work commit / review / finish / publish | Final Phase 2 check 通过后，workflow mandatory invoke `guru-create-task-commit`；skill 由 AI 审查 exact stage scope 与中文消息，由 deterministic validator/executor 校验 fresh evidence、只提交计划路径并验证真实 commit。任何 merge/cherry-pick/revert/rebase/sequencer/am state 都必须在 candidate、stage 与 commit 边界 fail closed；ordinary SHA-256/mode/delete、gitlink `gitlink_head` 和 validated candidate deterministic bytes 是 exact-index authority。Snapshot 以 `renamed_from` 和 `copied_from` 区分 rename/copy；只有 rename source 随 reviewed destination 进入 exact stage 并被删除，copy source 只能作为自身 independently reviewed path 进入计划，否则保留或因 unrelated staged content 阻断。Executor 在 isolated index/detached transaction HEAD 上执行真实 hooks 与 `git commit`，校验 commit/worktree/candidate/operation/live-index preimage 后，持有真实 `index.lock` sentinel、CAS 后立即复核的 loose-ref guard 与 candidate guard 完成 conditional ref/candidate publication/rollback；独立 final-index temp 在 sentinel 存在时发布，ref/index/result 已为 transaction state 且 guards 仍持有时的最终 candidate inode/content identity read 是线性化点。Read 前并发 C 触发 owned ref/index rollback 并保留 C；read 后 C 是 later operation，immutable commit blob/returned result digest 仍授权 `committed`。`committed` 进入 Branch Review，`revision-required` 重入本 skill，`blocked` fail closed；finding fix 必须回到实现和完整 Phase 2，再创建新 sequence。随后独立 review sub-agent 审查完整 `origin/<base>...HEAD` diff；每轮保留 task-local中文 `reviews/*.md` raw report，最终中文 `review.md` 作为 rollup 汇总并链接 raw reports，再经过 Branch Review Gate；之后由 `trellis-finish-work` 完成 archive 与 publish。 |
| Public Skill typed handoff | Interface 1.2 与 1.3 独立共存；registry active row exact 选择 `1.2+legacy` 或 `1.3+minimal_handoff`。`stage0-minimal-handoff-v1` 将 `guru-sync-base`、`guru-discover-change-context`、`guru-clarify-requirements`、`guru-review-contract-wording`、`guru-review-change-request`、`guru-create-task-workspace` 六包及其 24 exits 原子激活到 1.3；`guru-approve-task-plan`、`guru-check-task`、`guru-create-task-commit` 仍由 #146 保持 legacy。1.3 structured input 使用 closed schema/discriminator/`oneOf`，deterministic scalar CLI 不制造 input JSON；每个 exit 独立 output schema/example，每个字段绑定直接 consumer use，consumer input 由 Skill/workflow/stop 自身拥有，projection 只允许 direct/select/rename/closed normalize。Runtime/private checkpoint 与 gate evidence 不进入 public DTO。`discover-skill-contract` 返回 closed legacy/minimal index 和 portable stable errors；六包真实 public wrapper 和 canonical eval corpora 覆盖全部 profile/exit。Manifest、registry、workflow、extension、source/installed/selected-platform copies 必须 set-equal，preset transaction、pre-activation upgrade、update/reapply 不得产生 mixed graph 或 sidecar。Existing task 由 owner re-entry，archive 保持只读。 |
| Auto-bootstrap 日常入口 | 用户日常直接描述任务、贴 issue URL 或说 issue number；`trellis-start` 是 fallback / explicit orientation，不是每个任务的必需入口。 |

Duplicate candidate 的事实不是 caller-trusted 文本。Closed schema 要求 normalized bound
`repo`、positive `number`、`identity=#<number>`、canonical issue URL、`state=open` 与
`updated_at`；runtime pure gate 用该 projection 重算排除 AI reason/observation 的
`facts_sha256`、identity 与 URL。该投影只来自同一次 open duplicate search；record/check
不进行第二次 search 或 candidate re-read。`typed_exit=blocked` 与
`ai_review_gate.status=blocked` 必须双向等价，
schema/runtime 均拒绝 passed Gate 携带 blocked exit 或 blocked Gate 携带其他 exit。

Change-context recorder/checker 的 deterministic entry validator 固定执行 pure
schema/digest/semantic shape、base-only live gate、fresh-base-only repo
locator/issue/blob/history 三段顺序。`change_input` 十组 clue arrays 至少一组非空；
issue binding 与 canonical query 不能替代入口线索。Pure invalid 立即阻断；`refresh_base`
记录当前 stable stale codes、superseded query/snapshot digests、reason 与 detection time，
record/check 将这些 caller-authored facts 与 live drift 对齐后要求整步 re-entry，只消费当前
payload 与 expected snapshot identity，不重建 ancestry。Task-local recorder 写前/写后和 checker 必须通过 `git check-ignore
--quiet --no-index -- <target>` 证明 artifact 可追踪，覆盖 repo ignore、`.git/info/exclude`
与 `core.excludesFile`；pre-task stdout-only 路径不执行该 gate。Base stale 通过该 pure gate 后只核对
caller-authored refresh codes，再返回且不得读取 archive、
deep Git locator、issue、reviewed blob 或 history。Portable locator 只按 source-specific
closed structure 验证，不扫描整份 payload。

边界：

- Workflow 行为写在 Markdown 合同中，不通过修改 Trellis 上游源码、全局 npm 包、
  `node_modules` 或 hook hack 实现分叉。
- `trellis-continue` 只推进到 Branch Review Gate，不 push、不创建 PR、不调用
  `finish-work`。
- `trellis-finish-work` 是正常 closeout 与 PR publish 的唯一用户入口。

## 2. P0：Intake / worktree / no_task 副作用边界

这类扩展解决的是“AI 何时可以造成副作用”。历史问题集中在 freeform 请求、duplicate
issue、worktree、branch、task 创建和当前 checkout 直改上。

历史来源：

- Issue #6 / PR #14：`prepare-task` 默认路径改为无副作用 planner。
- Issue #15 / PR #16：`no_task` 当前 checkout 直接修改必须显式审批。
- Issue #26 / PR #28：历史上 worktree 曾继承或初始化 Trellis developer identity；#99/#112
  现已取消该 Guru 前置，但不删除官方 identity/journal 支持。
- Issue #51：`prepare-task` slug / branch / worktree / task 命名质量门禁。
- Issue #60：workspace boundary 机器事实层，阻断 task artifact、review metadata 和
  recorder/validator 路径误写 source checkout；#76 在该事实层上实现 sub-agent liveness
  与 source checkout progress/boundary violation 判定。
- Issue #55：历史 intake clarity / brainstorming、issue evidence update、任务中 scope change 留痕；由 #113 以 Skill-first package 重实现。
- Issue #113：active `guru-clarify-requirements`、closed result schema、exact confirmation、五个 typed exits与 active-task re-entry binding。
- Issue #110：公共 `guru-sync-base`、四级 selected-base resolution、digest-bound safe
  sync、三方 equality 与 `prepare-task` shared core。

已实现能力：

| 能力 | 说明 |
| --- | --- |
| Query-only prepare | `prepare-task.sh --json` 只输出兼容查询事实。Legacy `--create-issue-confirmed`、`--create-worktree`、`--create-task` 统一零写入 fail closed，并指向 `guru-create-task-workspace`。 |
| Task workspace closed loop | `guru-create-task-workspace` 是唯一 mutation owner。Workflow/standalone 使用完全相同的五个 prerequisite evidence、target authority、naming/assignee、confirmation、freshness 与 result checker 门禁。 |
| Intake clarity gate | Mandatory invoke active `guru-clarify-requirements`。Workflow/standalone preconditions 与 semantic stages 完全一致；`clear` / `needs_context` / `refresh_context` / `new_task` / `blocked` 分别进入 caller-aware resume router、context discovery、base sync、完整 intake route 与 fail-closed stop。`clear` 必须 open questions 为空、AI Gate passed、可客观验证的 authority/context current、accepted proposals 已 exact-confirmed且无未刷新 mutation。 |
| Reviewed draft creation | Draft invocation 只取得 `github_issue_mutation` confirmation。创建前按 exact title/body/labels、open state、`createdAt >= reviewed plan` 执行 0/1/>1 恢复判定：0 个创建一次，1 个恢复并重读，多个阻断。GitHub adapter 不 trim title/body，也不追加换行。重读 live issue并记录 `created_issue_binding` 后立即返回 `refresh_review`；同一 invocation 不创建 branch/worktree/task。 |
| Created issue re-entry | 完整 Intake 重跑后的 existing-issue plan 必须携带先前完整 checker-passed created-issue result，重算 result/binding digest，并核对 current issue、reviewed draft id/digest 与 creation confirmation digest。Fresh context 必须投影 canonical live existing issue：`kind=issue`、URL identity/open state/update time/body/facts digest 一致且 `issue_binding=null`。普通 existing issue 的 result/binding 均为 null；missing、partial 或 mismatch 全部阻断。 |
| Workspace/task executor boundary | Open issue invocation 另行取得 `workspace_and_task_mutation` confirmation。Plan 绑定 initial `post_sync_resolution_sha256`；executor 在首次 GitHub 或 workspace/task mutation 前只运行一次 shared resolver/sync core。Fresh identity不变才继续；remote 前进时允许安全刷新 base，但必须在 issue/branch/worktree/task/artifact/runtime mutation 前返回 `refresh_review`。后续 mutation boundary继续重验 plan/target/prerequisites与已刷新本地 facts，仅创建或 `reuse_exact` identity一致对象。 |
| Assignee route | 固定顺序为 explicit input、exactly one issue assignee、zero issue assignees 时 current GitHub login、multiple/unresolved 时 AI/user 选择一个 login；未解析前零 workspace/task 副作用。Executor 通过隔离 adapter 把 resolved login 显式传给 official `common.task_store.cmd_create`，只在该 handler 调用内禁用 developer accessor，使 `creator=assignee=resolved login`。 |
| Portable Intake artifacts | 创建成功只写 tracked task-local `task-start-context.json`、`issue-scope-ledger.json`、`context-discovery.json`、`issue-review.json`；result 本身不落盘，本机 mapping 只写 ignored `.trellis/.runtime/guru-team/**`。 |
| Workspace boundary guard | worktree mode 下 `local runtime workspace mapping` 是 task artifact 写入边界；`check-workspace-boundary.sh --json --task <task>` 输出 expected workspace、actual repo root、source checkout status、task worktree status 和 source checkout 可疑同名 artifact/review metadata，并让 recorder/validator 在错误 cwd 或错误 artifact path 下 fail closed。 |
| Base resolution | 固定顺序为 explicit `--base`、non-empty scalar `base_branch`、按 `base_branch_candidates` 声明顺序选择首个 existing local 或 remote-tracking ref（缺省 `dev -> develop -> main -> master`）、候选均不存在时的 remote default branch；resolver 只能在需要当前优先级时解析并校验该来源，已选高优先级来源不得被 malformed 低优先级输入阻断；多个候选同时存在按配置顺序选择，不是歧义；branch name 必须通过 `git check-ref-format --branch`，所有来源均失败时 blocked，禁止 current branch implicit fallback。 |
| Base sync | `sync-base --resolve-only` 在 fetch 前输出无绝对路径的 stdout resolution facts/pre-sync digest；`--execute` 必须重算并绑定该 digest，成功后输出绑定同步后 checkout 的 `post_sync_resolution` / `post_sync_resolution_sha256`。只允许显式 refspec fetch 和 selected-base checkout 上的 `git merge --ff-only`；dirty、missing ref、fetch failure、diverged、wrong checkout、stale resolution 或 post-sync mismatch 均 blocked。 |
| Fresh equality | 成功必须同时证明 checkout clean，decision checkout HEAD、local base HEAD、remote-tracking base HEAD 三者是完整 commit SHA 且完全相等；validator 只校验 schema/digest/live Git facts，不判断 scope、semantic pass 或 route。 |
| Phase 0 stdout facts | Resolution/result facts 只经 stdout 传递，不创建 repo-external evidence file、lease、release 或 cleanup API。Validator 向后只传 post-sync digest；`prepare-task` query 消费当前 digest，并在 issue/duplicate 读取前重跑 shared resolver/sync core。它不拥有 mutation guard；`guru-create-task-workspace` 在首次业务 mutation 前实际重跑 shared core，并在后续 boundary 独立重验完整 plan、五个 prerequisites、base、target 与 live facts。Fresh post-sync identity变化返回 `refresh_review`；其它 identity/digest 漂移立即 blocked。 |
| Naming quality gate | planner 输出 `naming_quality`；中文、非 ASCII 或低信息自动 slug（如 `issue-52`、`52-issue-52`、纯编号、仅通用词）不得静默进入 create 路径，agent 必须在读完 issue 后显式传入语义英文 `--short-name` / `--workspace-slug` / `--task-slug`，需要特殊分支名时才传 `--branch`。未显式传 `--branch` 时，branch 格式为 `<branch-type>/<slug>`，类型只能是 `feat` / `fix` / `refactor` / `perf` / `test` / `docs` / `style` / `build` / `ci` / `chore` / `revert`，未知语义 fallback 为 `chore`。 |
| Official identity boundary | Guru preset apply/update/reapply 与 task workspace executor 不读取、不创建、不复制、不恢复 `.trellis/.developer` 或 `.trellis/workspace/**`，也不要求 `init_developer.py`。已有 official Trellis identity/journal 数据保持不变。 |
| Parallel metadata merge gate | 真实本地 A/B fixture 从同一 base 分别走 production recorder/executor/checker 与 task-local archive/commit，再验证 A -> B、B -> A 两个 merge 顺序。两 task 的 tracked Guru metadata path 交集必须为空；不创建远程 PR，也不运行并发进程。 |
| no_task direct edit override | 当前 checkout 直改必须由用户明确批准跳过 issue、Trellis task、worktree 和 branch；批准不包含 commit、push、PR 或 issue close。 |
| Scope-change gate | task 进行中新增需求、引用其他 issue 或发现新 bug 时暂停 progression，canonical workflow mandatory invoke `guru-clarify-requirements`，不得复制分类/确认/ledger更新流程。Skill分类为 current close、related、followup、new task 或 out-of-scope。`clear`/`new_task` 必须有非空七类 terminal proposal set，五类 scope classification 无论 origin 均必须有 proposal-digest-bound 专用确认；optional mechanism 只能以 `mechanism_removed/replaced` terminal disposition 收敛，使用 null confirmation 且不进入 trail/action mutation。五类 classification 必须在当前 `issue-scope-ledger.json.scope_decisions[]` 留下 exact structured trail，绑定 live GitHub authority content/`updated_at`、shared validator 完整通过的 `guru-planning-approval-2.0` planning approval/docs、review state、stale gates、interrupted target 与 re-entry owners。GitHub authority mutation 后必须 `refresh_context`；context 时间覆盖 authority 后 task update 绑定同一 digest，不要求第二次 refresh。Current inclusion 返回planning review，其余分类恢复exact interrupted progression；`new_task` 只给 #112 side-effect-free draft。 |

实现资产：

- `trellis/workflows/guru-team/scripts/bash/prepare-task.sh`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/workflows/guru-team/schemas/task-start-context.schema.json`
- `trellis/workflows/guru-team/workflow.md`
- `.agents/skills/trellis-start/SKILL.md`
- `.codex/prompts/trellis-start.md`

## 3. P0：Planning / check / Branch Review Gate 证据链

这类扩展解决的是“通过 gate 必须留下什么证据，以及脚本不能冒充 reviewer”。

历史来源：

- Issue #5 / PR #12：Branch Review Gate 前必须先执行 AI review prompt。
- Issue #8 / PR #25：增加 planning approval 与 phase2 check 可审计证据。
- Issue #52：历史上要求 `prd.md` / `design.md` / `implement.md` 生成后展示三份文档链接并等待用户显式 post-planning 确认；其当前 semantic owner 与 evidence shape 已由 Issue #129 收敛到 `guru-approve-task-plan` v2。
- Issue #83：历史 schema 1.2 在展示三份规划文档前记录 planning artifact ambiguity review；Issue #129 保留其兼容 projection，但 active evidence 必须完整重入 `guru-planning-approval-2.0`，脚本仍只做 recorder / validator。
- Issue #93：planning-only wording scanner 的历史兼容基线，固定三份 planning artifacts、记录全部命中并阻塞 unchecked violation；其规则所有权由 Issue #114 replacement-first 迁移。
- Issue #114：active semantic Skill `guru-review-contract-wording` 统一拥有 `change_request`、`planning_artifacts`、`explicit_paths` 三个固定 profile、versioned vocabulary/classification、AI rewrite/review、deterministic scanner/recorder/checker、schema `guru-contract-wording-review-1.0` 与 `pass` / `content_changed` / `blocked` typed exits。Selected authoritative comment 必须绑定 identity/author/updated time/selection reason/content hash；live issue revision 还必须把 human-confirmed exact payload digest、preimage 与 current live reread mutation result identity 串成可检查 evidence。`planning_artifacts` 必须按 canonical Skill contract 显式记录 planning-only checked dimensions，全部经 AI review 为 true 才能 pass；deterministic runtime 只验证 shape/value。Task-local current `content_changed`/`blocked` 在 consumer 完成 same-profile re-entry 后，只能以旧 `facts_sha256` 精确绑定的 supersession 被完整、current 且不同的新 evidence 替换；stale evidence 走独立 stale replacement，相同结果与 current `pass` 继续受保护。Planning approval 只消费当前 `planning_artifacts:pass` evidence，不再拥有或接收逐条 classification 输入，也不得默认生成 planning semantics。
- Issue #129：active semantic Skill `guru-approve-task-plan` 成为 Phase 1 planning approval 唯一 owner。Workflow/standalone 使用相同九项 entry preconditions；Skill 独占 planning adequacy、四类 provenance、implementation choice、unusual proposal review、AI Gate、专用/普通 confirmation 分离、revision/re-entry 与四个 typed exits。唯一 artifact 继续是 `planning-approval.json`，breaking schema 升级为 `guru-planning-approval-2.0`；shared recorder/checker 只重建 deterministic facts、验证 statement/digest/freshness/closed union，不生成语义判断。`approved_scope_expansion` 不接受 caller-only digest：普通 proposal 从当前 planning artifact controlled locator 重算，unusual proposal 从 canonical candidate 重算；专用 confirmation 与 runtime-materialized current authority SHA-256 必须绑定同一 proposal digest，candidate link 复用同一次 unusual confirmation。Scope ledger 无论作为 task identity 或 requirement authority 都使用相同 issue-category projection；task activation 前复验 invocation repository snapshot，activation 后允许普通实现 drift。
- Issue #101：active semantic Skill `guru-review-change-request` 成为 pre-task readiness 唯一 owner；它消费 current context/clarity/wording evidence，支持 existing issue、side-effect-free proposed draft 与 standalone request，固定十项 review dimensions、finding/scope/Gate/confirmation 与 `ready` / `clarify_requirements` / `review_wording` / `refresh_context` / `blocked` 五出口。Runtime 只重验 schema/hash/projection/linkage/freshness/consumer/ready invariant，pre-task/standalone stdout-only。两类 draft target 的 `source_request_sha256` 必须从 #113 current draft `review_target` authority projection重算。`ready` 唯一进入 active #112 `guru-create-task-workspace`。
- Issue #20 / PR #22：Branch Review Gate 建立 task-local final `review.md` 人类入口和
  `review-gate.json` digest 基线。
- Issue #70：多轮 Branch Review 每轮保留 task-local `reviews/*.md` raw report，最终
  `review.md` 只做 rollup 并链接 raw reports；`agent-assignment.json.review_rounds[]` 和
  `review-gate.json.verification_evidence.review_reports[]` 追溯 raw report digest。#61
  顶层 artifact 表默认仍只列 final `review.md`。
- Issue #78：`reviews/*.md` raw reports 和 `review.md` rollup 继承 #57 中文
  human-readable artifact 规则；标题、小节、字段/标签、发现、观察、后续候选、
  部署/安全判断、Docs SSOT 判断和结论默认中文，literal token 可保留英文。
- PR #21：`#20` 的早期 closed 未合并实现，由 PR #22 替代。
- Issue #62：sub-agent wait timeout / stale / unfinished termination 策略，避免把等待窗口
  timeout 或未闭环部分输出当作 pass evidence。

已实现能力：

| 能力 | Artifact / 脚本 | 说明 |
| --- | --- | --- |
| Contract wording review | `guru-review-contract-wording`、`contract-wording-review.json`、`record-contract-wording-review.sh`、`check-contract-wording-review.sh` | Canonical Skill package 是 vocabulary、classification、三个固定 profile、AI semantic loop、confirmation policy、schema 与三个 typed exits 的唯一 owner。Shared runtime 只重建 scope、扫描、派生 digest/unchecked projection 并校验 freshness；`planning_artifacts` 固定绑定当前 task 的三份 planning docs，并要求 canonical planning-only dimensions 全部显式 AI-reviewed 为 true，passed evidence 才能写入 task-local artifact。Consumer 完成 same-profile re-entry 后，recorder 只允许 exact prior `facts_sha256` 绑定、与旧 artifact 不同且完整 current 的新结果 supersede current non-pass；stale replacement 与该路径互斥，相同结果与 current `pass` 不得无理由覆盖。其它 profile 禁止 planning-only 字段。 |
| Change-request readiness review | `guru-review-change-request`、`guru-change-request-review-1.0`、`record-change-request-review.sh`、`check-change-request-review.sh` | Canonical Skill package 独占 target/prerequisite semantic readiness、十项 dimensions、findings、delivery unit、scope conclusion、AI Gate、confirmation 与五出口。Runtime 复用前置 objective validators并重建 portable projection/linkage/facts，不生成 semantic result或 route。Pre-task/standalone 只输出 stdout；active #112 持久化同一 checker-passed `issue-review.json` bytes。 |
| Planning approval closed loop | `guru-approve-task-plan`、`guru-planning-approval-2.0`、`planning-approval.json`、`record-planning-approval.sh`、`check-planning-approval.sh` | Skill 消费 checker-validated `guru-review-contract-wording:planning_artifacts:pass` evidence，审查三份 planning artifacts 与 `Docs SSOT Plan`，为全部 load-bearing statement 记录 `explicit_requirement`、`necessary_implementation_choice`、`approved_scope_expansion` 或 `out_of_scope_proposal`，并将非常规 proposal 的 dedicated confirmation 与普通 post-planning confirmation 分离。`approved_scope_expansion` 的 `proposal_binding` 只允许 current planning locator 或 canonical unusual candidate；runtime 重算 proposal digest，要求 `confirmation` 与含 current authority digest 的 `authority_binding` 同时绑定该 digest，unusual candidate 不重复提问。`approved` 唯一进入 `phase-1-task-activation`；`revision_required` 重入本 Skill；`clarify_scope` 转 `guru-clarify-requirements`；`blocked` 进入 fail-closed stop。Recorder/checker 只消费 AI-reviewed input、重建 task/authority/planning/docs/wording/repository facts，并验证 schema、digest、freshness 与 exit/Gate/consumer closed union。`scope_ledger_sha256` 只绑定 primary/close/related/follow-up 的 canonical 正 issue number 分类，排除 decision trail、验收 metadata 与内嵌 approval hash，避免 scope decision 正常回写形成循环 identity；issue 分类变化仍使 approval stale。Active schema 1.2 artifact 必须按完整 Skill 重录为 2.0；archive 不改写。`task.py start` 只是状态写入。 |
| Phase 2 check gate | `guru-check-task`、`guru-phase2-check-2.0`、`phase2-check.json`、`record-phase2-check.sh`、`check-phase2-check.sh` | `guru-check-task` 是 Phase 2 与唯一 artifact 的 semantic owner。每轮先对 candidate 记录 requirement/planning trigger、受支持 normal-path reproduction 与 `current_scope` / `scope_change_required` / `followup_proposal` / `out_of_scope` disposition；仅 `current_scope` 可取得 P0-P3。Skill 完整审查 requirements -> design -> implementation -> tests -> Docs SSOT、记录 commands/results、worker evidence、unverified items、完整 dirty snapshot 与 agent recovery，再经 AI Gate 返回 `passed`、`implementation_required`、`planning_stale` 或 `blocked`。Finding 修复后必须 full-scope rerun。Agent projection 只摘要实现/check agents、events/liveness、corrections/recovery links、completed exact sets 与 recovery closure；commit 后合法 Branch Review assignment/status/round/reuse metadata 可追加，但 Phase 2 内容漂移仍 fail closed，Branch Review Gate 独立校验完整 current assignment artifact。Recorder/checker 只重建 schema/hash/HEAD/diff/dirty/planning/agent/exit-consumer 事实；official worker、coverage、命令通过或脚本成功均不能生成 pass。Legacy active schema 1.0 与旧 `--pass --coverage` 调用必须完整 semantic re-entry，archive 字节保持不变。 |
| Phase 2 evidence closure | `guru-phase2-check-2.0` schema / checker | Provenance、handoff、durable paths、reviewed paths、commands 与每个 adequacy evidence refs 必须非空，完整 adequacy round 覆盖全部 known current-round evidence source，current/scope-change candidate 必须携带 trigger refs。Checker 重算 execution/scope/adequacy、全部 Gate binding、finding count 与 full-round digest；这些仅为客观存在/引用/派生一致性校验，不替代 AI adequacy。Handoff 包含 task-local assignment 时，合法 Branch Review metadata tail 由 Phase-2-stable agent projection 复核，implementation/check/recovery drift 仍阻断。 |
| Task work commit gate | `guru-create-task-commit`、`task-commit-plans/<sequence>.json`、`check-commit-messages --candidate-artifact`、`create-task-commit` | 每次提交绑定 task/issue/base/pre-commit HEAD、planning/Phase 2/ledger digests、完整 dirty snapshot、AI-reviewed path classification、exact stage paths、message bytes 与授权；Git state detector 在 candidate、transaction commit 和 publish 前拒绝非普通 operation/sequencer state；ordinary SHA-256/mode/delete、gitlink HEAD/OID 与 validated candidate deterministic bytes 构成唯一 exact-index authority。`renamed_from` 只为 rename destination 授权 source 删除；`copied_from` 只记录 copy relation，不授权 source 删除或自动 exact stage。Copy source 若也在 snapshot 中，必须独立分类与受审。Executor 不使用 broad add，不让可变 worktree 选择 staged content；它在 isolated index/detached HEAD 执行 hooks/commit，验证 parent/message/path/tree/worktree/candidate/live-index preimage 后，保持真实 `index.lock` sentinel 到 transaction 结束，使用独立 temp 发布 final index，再以最终 candidate identity read 线性化。Read 前 C 会触发 owned ref/index rollback 并被保留；read 后 C 是不改变 committed 证据的 later operation。失败按 conditional ownership 恢复自有状态而不覆盖并发 writer。 |
| AI review prompt | workflow / overlay 文案 | Branch Review Gate 前必须由独立 review sub-agent 审查 `origin/<base>...HEAD` 完整 diff；review sub-agent 不继续实现、不替 implement/check 代理补工作。 |
| Raw reports + rollup 必填 | `reviews/*.md`、`review.md` | 每轮 AI/human review 判断都必须写 task-local 中文 raw Markdown report；顶层 `review.md` 是最终中文 rollup，建议使用 `审查轮次`、`问题生命周期`、`最终审查`、`证据`、`观察项`、`后续候选`、`结论` 等小节，汇总审查轮次、问题闭环生命周期、关键证据、最终结论，并链接所有 raw reports。#61 顶层 artifact 表默认仍只列 final `review.md`，raw reports 通过 rollup 和 gate digest 追溯；literal command/path/JSON/HEAD/API/code token 可保留英文。 |
| Finding 全阻断 | workflow、`review-branch.sh`、`review-gate.json` | Branch Review Gate 中任意 finding 都阻断，包括 P3；`observation` 与 `followup_candidate` 可记录但不是放行 finding 的替代品。 |
| 闭环后 Fresh 最终放行审查 | `agent-assignment.json`、`review-branch --agent-assignment` | 任何发现过 findings 的 agent 必须先作为同一 `问题闭环审查代理` 确认其 finding 已闭环并记录 0 findings；若原 agent 失败/中断且无法继续，必须记录 predecessor failed/unfinished、`replacement-started`、`reuse_decisions[] decision=replace from_round/to_round` 和替代闭环 round。之后最终 pass 必须由新的 fresh `最终放行审查代理` 完整审查当前 HEAD diff 并记录 0 findings，且 final agent 不能是 finding owner 或替代闭环 reviewer。 |
| Sub-agent liveness 状态机 | `agent-assignment.json`、`record-subagent-liveness-event.sh`、`check-subagent-liveness.sh`、`check-agent-assignment.sh`、`review-branch --agent-assignment` | `agent-assignment.json` 是唯一 task-local assignment/status/liveness/review ledger，schema 1.2 包含 `agents[]`、`status_events[]`、`liveness[agent_id].last_scan_snapshot`、append-only `event_corrections[]` 与 `recovery_links[]`；correction 只以 target digest 失效错误 provenance 的 progress/status-request，link 只连接同 agent `failed` 到后续 manual/platform termination，validator 拒绝 unknown/duplicate/cycle/cross-agent/tamper 并仍遍历到 replacement `completed`。checker 每次按需单次采样 task/source checkout 与 effective progress event digest；旧 `record-agent-assignment.sh --status-event` 路径 fail closed。 |
| Workspace boundary snapshot | `check-workspace-boundary.sh`、recorder/validator boundary helper | 在记录 planning、phase2、assignment、review gate 或 sub-agent status evidence 前确认 actual repo root 等于 local runtime workspace mapping，并拒绝 source checkout / 非当前 task worktree 的 `--review-report`、`--agent-assignment`、`--review-round-report`、`--checked-artifact` 等路径；脚本只输出事实，不判断 stale、不迁移 patch、不清理 source checkout。 |
| Review gate recorder | `review-branch.sh`、`check-review-gate.sh`、`review-gate.json` | 固化 review result、final `review.md` digest、raw `review_reports[]` digest、base/head、evidence、findings、observations、follow-up candidates；脚本不是 reviewer，且独立 review sub-agent 不调用这些 recorder/validator 扩展脚本作为审查过程。脚本可客观拦截 `Review Rounds`、`Findings Lifecycle`、`Evidence Handoff`、`Deployment / safety impact`、`Follow-up Candidates` 等英文模板标题痕迹，但不判断中文审查语义充分性。 |
| Independent review source | `--review-source independent-agent` | 通过 gate 不能来自 `self-review` 或 `*-main-session`。 |
| Sub-agent assignment ledger | `agent-assignment.json`、`record-agent-assignment.sh`、`check-agent-assignment.sh`、`review-branch --agent-assignment` | 记录中文 `logical_role`、技术 `agent_id`、展示用 `platform_nickname`、HEAD、review round、raw report path/sha256/size/modified_at 和复用/更换判断；脚本只做客观校验，不决定复用。UI 展示面优先使用中文 subagent 名称，平台只给随机/自动昵称时记录原始值。 |
| 默认 sub-agent mode 执行边界 | workflow / overlay / agent definitions | 默认 mode 下必须有 `trellis-implement`、`trellis-check` 和 Branch Review review sub-agent 三段真实 sub-agent evidence；review sub-agent 每轮输出中文 `reviews/*.md` raw report，最终形成中文 `review.md` rollup。main session 只协调和记录，不能用主会话实现、自检、自审或 recorder/validator 成功替代。inline/self-exemption 必须有 artifact evidence，否则 fail closed。 |
| Post-commit audit / metadata tail 规则 | `review-branch.sh`、`finish-work.sh` / gate 校验 | Branch Review Gate 接受 Phase 2 后提交的非 metadata task paths，但这些 paths 必须已被 commit 前 `phase2-check.json.dirty_paths` 覆盖；review gate 通过后到 finish-work 之间仍只允许 Trellis metadata tail，新的非 metadata 变更会使 evidence stale。 |

覆盖范围：

- docs、code、tests、Trellis artifacts
- preset overlay、companion scripts、schema、config
- CI/CD、container、Kubernetes/Kustomize/Helm、DB migration、Makefile
- Issue Scope Ledger、publish readiness、部署影响和安全风险

## 4. P0：Finish / publish / PR readiness

这类扩展解决的是“PR 何时发布、由谁判断 PR body 是否足够，以及 dry-run 是否真的无副作用”。

历史来源：

- Issue #18 / PR #19：PR publish 只能发生在 finish-work 之后。
- Issue #17 / PR #23：PR body 质量标准，禁止低信息量默认摘要。
- Issue #7 / PR #24：publish 前必须有 AI-reviewed body file 或 readiness artifact。
- Issue #27 / PR #29：`finish-work --dry-run` 成为真正无副作用 readiness preview，同时修正
  Codex 默认 dispatch 为 `sub-agent`。

已实现能力：

| 能力 | 说明 |
| --- | --- |
| Publish after finish | `publish-pr` 是兼容性阻断入口；正常发布与恢复只由 `finish-work.sh --from-trellis-finish-work` 执行 reviewed content push、draft PR、final projection、archive transaction 与 draft-to-ready。 |
| Recovery/debug 明确化 | 同一 `trellis-finish-work` 从 committed plan/readiness、active/archive locator、Git/remote 与唯一 PR identity 恢复；不暴露 publish recovery flag，也不生成 initial empty-URL summary 或 URL tail commit。 |
| Reviewed body source | closeout 必须传入当前 task-local `pr-body.md`；`--body-artifact` 与 generated fallback 不进入 finish-work 事务。 |
| PR body 质量门禁 | 变更摘要、影响范围、验证结果、Review Gate、Issue 关闭范围、安全说明必须具体，禁止“当前 Trellis task”“详见 artifact”等低信息量短语作为主要摘要。 |
| Issue close 语义 | `Closes #xx` 只能来自 task-level `issue-scope-ledger.json` 的 `close_issues`，`related_issues` / `followup_issues` 不得被关闭。 |
| Final archive projection | finish-work 在 active task 中生成最终 summary，并由 official archive move 原样迁移；archive 后不重写 body/readiness/summary。 |
| Dry-run readiness preview | `finish-work --dry-run --from-trellis-finish-work --finish-summary-index-file <task>/finish-summary-index.json` 运行与 formal 相同的 prepare/validate，输出 immutable plan/digest，不移动或写入文件、不 commit、不 push、不创建 PR。 |
| Codex default dispatch | 缺省或非法 `codex.dispatch_mode` 回落到 `sub-agent`，显式 `inline` 保留为调试/降级模式。 |

实现资产：

- `trellis/workflows/guru-team/scripts/bash/finish-work.sh`
- `trellis/workflows/guru-team/scripts/bash/publish-pr.sh`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/presets/guru-team/overlays/**/trellis-finish-work*`
- `.trellis/spec/workflow/workflow-contract.md`
- `.trellis/spec/workflow/companion-scripts.md`

## 5. P1：Preset installer 与平台 overlay

Preset installer 把 workflow 之外的 Guru Team companion assets 和平台入口安装到目标仓库。
它不运行 `trellis init`，不修改官方 Trellis 生成脚本，也不改上游源码。

历史来源：

- Issue #9 / PR #13：保持 dogfood installed overlays 与 canonical preset overlays 同步。
- Issue #11 / PR #30：preset installer 只安装所选平台 overlay。
- Issue #31：Guru Team extension version manifest 与 installed provenance。
- Issue #33：Guru Team extension version 与 repo 级 release tag `vX.Y.Z` 对齐。

Canonical 资产：

- `trellis/presets/guru-team/scripts/bash/apply.sh`
- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
- `trellis/presets/guru-team/README.md`
- `trellis/presets/guru-team/overlays/`

已实现能力：

| 能力 | 说明 |
| --- | --- |
| Managed assets 安装 | 安装 `.trellis/guru-team/config.yml`、schema、bash scripts、Python helper。 |
| 幂等更新 | 同内容跳过；Guru-managed 文件升级 active 文件并保留 `.bak`；未知本地改动写 `.new`。 |
| 配置保护 | 已有 `.trellis/guru-team/config.yml` 不为补 key 被覆盖；`middle_platform_knowledge.mode` 缺失时按 `optional_warn`。 |
| Codex dispatch 默认 | 物化 `.trellis/config.yaml` 的 `codex.dispatch_mode: sub-agent` 默认，显式 `inline` 保留。 |
| Subagent UI 中文展示名 | 安装 `.trellis/agents`、`.codex/agents`、`.cursor/agents`、`.claude/agents`；保留 `trellis-implement` / `trellis-check` / `trellis-research` / `implement` / `check` 技术标识。Cursor / Claude / channel runtime 用中文 `description` 和标题作为展示名来源；Codex 当前限制 `nickname_candidates` 为 ASCII，因此只用中文 `description` 和 assignment 角色表达中文 UI 语义。 |
| Subagent 执行边界 | workflow、continue overlay、agent definitions | 默认 sub-agent mode 下 main session 必须 dispatch implement/check/review sub-agent 并等待 evidence；`trellis-implement` 输出实现 handoff，并包含 `Docs SSOT Plan` strategy、docs 同步结果、task delta merge / task history-only 内容、no-update 或 follow-up / PR 限制；`trellis-check` 输出 Phase 2 evidence 并按 plan strategy 复核 durable docs / task artifacts / code / test 一致性；Branch Review sub-agent 输出可被 gate 消费的中文 `reviews/*.md` raw reports 与最终中文 `review.md` rollup。 |
| 平台可选安装 | 默认安装 shared + Codex + Cursor；支持重复 `--platform codex|cursor|claude`；支持 `--all-platforms`。 |
| 未选择平台不恢复 | 默认 Codex + Cursor 安装不创建 `.claude/`；重复 apply 不会恢复未选择平台目录。 |
| Extension version/provenance | `trellis/guru-team-extension.json` 是 Guru Team extension canonical version；installer 写入 `.trellis/guru-team/extension.json` 记录安装版本、source ref/commit、source tree state 和 selected platforms。 |
| Release tag contract | Guru Team extension release tag 使用 repo 级 `vX.Y.Z`，并与 `trellis/guru-team-extension.json.version` 一致；tag-pinned stable marketplace source 使用 `gh:castbox/guru-trellis/trellis#vX.Y.Z`。 |
| Dogfood drift check | canonical overlay 与本仓库安装副本可通过 `check-dogfood-overlay-drift.sh` 比对。 |
| 业务项目语言归一化 | preset installer 确定性替换 `.trellis/spec/**` 和 `00-bootstrap-guidelines` 中已知 Trellis 英文文档语言规则，不扫描 `.trellis/workspace/**`、普通 task 历史或翻译业务 `docs/**`。 |
| Finish summary 合同 | `finish-summary.schema.json` 是正常 finish 与 #100 backfill 的共同 SSOT；Guru Team 不调用 `add_session.py`，shared/Codex/Cursor context 不打开、枚举或输出 `.trellis/workspace/**`，preset 写入 `session_auto_commit: false` 与 workspace ignore。recorder 对 raw paths 排序去重并过滤受保护前缀；任一必需 Git path snapshot 命令失败时两个 path 数组清空，只记录固定 unavailable fact。`pr-readiness.json.publish_inputs` 在首次 PR create 前提交并绑定 repo/base/head/title/body digest/draft/reviewed source，recovery 在 query/create 前验证 Git blob、snapshot/body digest、gate 与 current/remote HEAD。 |

平台 overlay 当前覆盖：

| 平台/层 | 文件 |
| --- | --- |
| Shared skills | `.agents/skills/trellis-start`、`trellis-continue`、`trellis-finish-work` |
| Channel runtime | `.trellis/agents/implement.md`、`.trellis/agents/check.md` |
| Codex | `.codex/agents/trellis-*.toml`、`.codex/prompts/*` 与 `.codex/skills/*` |
| Cursor | `.cursor/agents/trellis-*.md`、`.cursor/commands/trellis-continue.md`、`.cursor/commands/trellis-finish-work.md` |
| Claude | `.claude/agents/trellis-*.md`、`.claude/commands/trellis/continue.md`、`.claude/commands/trellis/finish-work.md` |

## 6. P1：安装、升级与开箱验证

公共 workflow skill 基础设施由 `trellis/skills/guru-team/` 单点定义。
Production registry 的 `reserved` 项只占用公共 id，不能安装或被 mandatory
route 引用；`active` 项必须携带完整 package/interface/schema/validator/test
和 workflow marker 证据。global workflow 只拥有 mandatory invocation、跨
skill transition 和 typed exit consumer/stop，step-local 正文只属于 skill。
Active `SKILL.md` 必须具有唯一闭合 frontmatter，且 `name` 等于 registry、
interface 与 stable skill id，非空 `description` 与 interface 一致；`tests[]`
只允许指向 package-local `tests/<file>` 的真实 regular file，并随 package
inventory 安装，missing/outside/symlink/duplicate evidence 一律 fail closed。

Preset 负责把 active package 安装到 `.trellis/guru-team/skills/`、shared
root 和已选择的平台 root，并用 previous managed hash 区分 missing、
unchanged、known managed upgrade 与 unknown local edit。unknown/invalid
provenance 必须保留原文件、生成 `.new` 并 fail closed；known upgrade 先生成
`.bak`。`check-skill-packages --mode source|installed` 只校验机器事实，不得
替代 AI Gate。`trellis update` 后必须重放 workflow 和 preset、处理 sidecar，
再通过 source/installed/drift 检查。

`workflow.routing=global_workflow` 由 mandatory marker 触发；
`standalone.routing=direct_discovery` 允许所选平台直接发现同一个 package。后者不承诺
单目录 self-contained 或 portable。Interface schema 1.2 要求显式 `judgment_mode`：
`semantic` 固定 forward/AI Gate/conditional confirmation/recorder-validator/typed-exit 五阶段，
`deterministic` 固定 forward/recorder-validator/typed-exit 三阶段；两种 mode 的 entry
preconditions 和同一 profile 行为必须一致，且 package wrapper 只能
把固定 validator id 交给 `.trellis/guru-team/scripts/bash/run-skill-command.sh`。Dispatcher
校验 interface dependency、installed extension runtime API、managed inventory 与公开
`runtime_command` 后才调用共享 companion command；任何缺失、不兼容或 drift 都必须在
业务副作用前阻断并提示安装或升级完整 preset。

`guru-sync-base` 与 `guru-create-task-commit` 都遵守上述 package/runtime 合同。
前者发布 `sync-base`、`check-base-sync` 与 `guru-base-sync-result-1.0`，并要求
workflow/standalone mode 具有完全相同的 entry preconditions。Standalone 只处理
explicit base refresh/verification，不支持 `skipped`，也不进入 issue intake、context
discovery、task 或 worktree 创建。

这类扩展证明 `guru-team` 不是 dogfood 仓库里的局部 patch，而是可以安装、升级、抽样验证的
团队扩展。

历史来源：

- Issue #10：README 安装命令必须非交互且可开箱验证。
- Issue #9 / PR #13：dogfood overlay 同步。
- Issue #11 / PR #30：平台选择安装验证。
- Issue #27 / PR #29：finish-work dry-run readiness 和 Codex default dispatch 让新装项目不在 closeout 阶段卡死。
- Issue #31：安装/升级后用户和 AI 可直接查看 Guru Team extension version 与来源 provenance。

已实现验证能力：

| 能力 | 入口 | 说明 |
| --- | --- | --- |
| Non-interactive install | `README.md` | 默认命令使用 `trellis init -y ... --workflow guru-team --workflow-source gh:castbox/guru-trellis/trellis#vX.Y.Z`，不进入交互式 spec template picker。 |
| AI install / upgrade prompt | `README.md` | 提供可复制到目标业务仓库 AI session 的安装、升级、spec bootstrap prompt。 |
| Throwaway install | `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh` | 创建临时 Git repo，运行非交互 `trellis init`、应用 preset、检查 workflow、脚本、平台选择和 `check-env --json`。 |
| Extension version check | `.trellis/guru-team/scripts/bash/version.sh --json` | 读取 installed manifest，输出 Guru Team extension version、workflow template id、source ref/commit、source tree state 和 selected platforms。 |
| Existing workflow preview/switch | `trellis workflow --marketplace ... --template guru-team --create-new` / 无 `--create-new` | 验证已有项目可以预览并切换 active workflow。 |
| Dogfood overlay drift | `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh` | 比对 canonical overlay 与本仓库安装副本，防止 dogfood 文件漂移。 |
| Installer unit tests | `trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py` | 覆盖平台选择、Codex dispatch 默认、unknown platform fail closed 等 installer 行为。 |
| Workflow helper tests | `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` | 覆盖 intake side-effect boundary、planning/phase2 gate、review/publish/finish 边界等行为。 |

维护规则：

- README 命令必须真实可执行，不依赖本机隐藏状态。
- 修改 `trellis/presets/guru-team/overlays/` 后，要重新 apply 到本仓库并运行 dogfood drift
  check。
- 修改 workflow/preset/overlay/脚本后，需要说明 throwaway install 或 upgrade/update
  验证覆盖了什么，未覆盖什么。

## 7. P2：Docs、spec 与 knowledge 协同

这类扩展不直接创建 task 或发布 PR，但决定长期维护质量。

历史来源：

- Issue #1 / PR #4：Middle-platform Knowledge Gate 与 Repo Docs SSOT。
- Issue #10：README install / upgrade prompt 需要包含 spec bootstrap 边界。
- Issue #9：overlay 与 dogfood 副本同步属于公共 docs / spec 可维护性问题。

已实现能力：

| 能力 | 说明 |
| --- | --- |
| Middle-platform Knowledge Gate | 当任务涉及 Guru Team 中台 SDK / framework 时，AI 检查当前平台是否可用 `guru-knowledge-center` MCP，并将 citation 写入 task artifact。 |
| Configurable knowledge mode | `middle_platform_knowledge.mode` 支持 `off`、`optional_warn`、`required`；缺失时按 `optional_warn`。 |
| Docs SSOT Plan | Phase 1 必须创建或更新同一个 planning 合同，推荐由 `design.md` 承载权威计划，`prd.md` 记录 docs 状态 / 需求影响，`implement.md` 记录 checklist / checkpoint。计划记录 `complete_docs`、`partial_docs`、`stale_docs`、`no_docs` 之一，以及 `ssot_first`、`delta_first`、`bootstrap_or_repair_docs`、`no_docs_update_needed` 之一。 |
| Repo Docs SSOT reconciliation | Planning 阶段识别 durable docs；Phase 2 完成 durable docs 更新/merge/repair/no-update 复核并在 handoff/check 中留痕；Phase 3 只验证结果，finish-work/archive 不首次执行 docs merge。 |
| Spec bootstrap 边界 | 安装后发现 `00-bootstrap-guidelines` 时只报告并询问，不把 spec bootstrap 作为安装副作用静默完成。 |
| Bootstrap/docs 中文规则 | 用户确认 bootstrap 后，生成或刷新 `.trellis/spec/**` 与 `docs/**` SSOT 主文档时按业务项目中文默认规则写作。 |
| Spec update 判断 | 每个任务 closeout 前判断是否需要更新 `.trellis/spec/`，但不把 active task 或私有业务 PRD 放入公共 template / marketplace。 |
| Public docs 规范 | `.trellis/spec/docs/public-docs.md` 约束 README 安装/升级 prompt、Git 发布预检、安全和 SSOT 一致性。 |

## 8. 历史覆盖矩阵

| Issue | 状态 | 对应 PR | 已沉淀扩展 |
| --- | --- | --- | --- |
| #1 | closed | #4 merged | Middle-platform Knowledge Gate；Repo Docs SSOT reconciliation。 |
| #2 | closed | #3 merged | Auto-bootstrap 日常入口；`trellis-start` fallback 定位。 |
| #5 | closed | #12 merged | Branch Review Gate 前先执行 AI review prompt；脚本只是 recorder / validator。 |
| #6 | closed | #14 merged | `prepare-task` 默认无副作用 planner；confirmed issue creation。 |
| #7 | closed | #24 merged | publish 前必须有 AI-reviewed PR body / readiness artifact。 |
| #8 | closed | #25 merged | `planning-approval.json` 与 `phase2-check.json` 可审计 gate。 |
| #9 | closed | #13 merged | canonical overlay 与 dogfood installed copy 同步；drift check。 |
| #10 | closed | 已体现在 README / verification | 非交互安装命令、AI install/upgrade prompt、开箱验证要求。 |
| #11 | closed | #30 merged | preset installer 支持 platform overlay selection。 |
| #15 | closed | #16 merged | `no_task` 当前 checkout 直改必须显式审批。 |
| #17 | closed | #23 merged | PR body 自解释质量标准与低信息量摘要阻塞。 |
| #18 | closed | #19 merged | PR publish 只能发生在 finish-work 后。 |
| #20 | closed | #22 merged | Branch Review Gate 建立 task-local final `review.md` 人类入口和 gate digest 基线；#21 为 closed 未合并尝试，#70 在其上扩展 raw reports + rollup。 |
| #26 | closed | #28 merged | worktree 创建后继承或初始化 Trellis developer identity。 |
| #27 | closed | #29 merged | `finish-work --dry-run` 真正无副作用；Codex 默认 `sub-agent` dispatch。 |
| #31 | closed | #32 merged | Guru Team extension canonical manifest、installed provenance、`check-env` / `version.sh` 可观测入口。 |
| #33 | open | 当前任务 | Guru Team extension version 对齐 `0.6.5`；repo release tag 使用 `v0.6.5`；稳定 marketplace source 使用 `#v0.6.5`。 |
| #52 | open | #129 当前 v2 owner | 显式 post-planning 审核需求由 `guru-approve-task-plan` 独占；`planning-approval.json` v2 的 ordinary confirmation 与 dedicated unusual confirmation 分离，Phase 0 handoff 确认不能替代。 |
| #43 | open | 当前任务 | Trellis sub-agent 中文逻辑角色、UI 展示名中文化、`agent-assignment.json`、reviewer 复用/更换记录和 gate digest 集成。 |
| #72 | open | 当前任务 | 默认 sub-agent mode 下强制 implement、Phase 2 check 和 Branch Review 均由 sub-agent 执行；main session 只协调，脚本只 recorder/validator。 |
| #55 | closed | #113 的历史来源 | 原 issue intake clarity / brainstorming 与 scope-change 行为；不重复关闭。 |
| #113 | open | 当前任务 | `guru-clarify-requirements` semantic closed loop、result schema、runtime record/check、workflow/standalone distribution与五个唯一 typed-exit consumers。 |
| #57 | open | 当前任务 | 业务项目 Trellis 文档语言默认中文；installer 归一化已知英文模板语言规则；bootstrap docs SSOT 中文规则。 |
| #60 | open | 当前任务 | workspace boundary guard：新增 `check-workspace-boundary` 事实快照、recorder/validator cwd 与 task-local path fail-closed 校验、source checkout 可疑 task artifact 检测、workflow/overlay/docs 绝对 worktree 路径规则；为 #76 的 source/task 双侧 liveness checker 提供事实层。 |
| #76 | open | 当前任务 | sub-agent liveness、progress/stale 判定与 replacement cutover 状态机：单一 `agent-assignment.json` 1.1 artifact、required recorder/checker、status request 前置审计、stale cutover 结构化 termination/replacement cause、completed-only recovery gate；不新增 heartbeat 文件、daemon、sidecar、long-command wrapper 或后台 liveness 进程。 |
| #70 | open | 当前任务 | Branch Review 每轮保留 `reviews/*.md` raw report；最终 `review.md` 是 rollup 并链接 raw reports；`agent-assignment.json.review_rounds[]` 与 `review-gate.json.verification_evidence.review_reports[]` 记录 raw digest；#61 顶层 artifact 表默认仍只列 final `review.md`。 |
| #78 | open | 当前任务 | Branch Review raw reports / `review.md` 继承 #57 中文 artifact 规则；workflow / overlay / docs / spec / validator 防止英文模板标题复发。 |
| #83 | open | #93/#114 的 baseline | Planning artifact semantic review gate：展示三份 planning docs 前完成 AI 语义审查，recorder/validator 只记录和校验结构化 evidence。 |
| #93 | open | #114 的历史兼容基线 | 原 planning-only scanner 的固定三文件、全部命中与 unchecked blocking 行为；active 规则所有权不再留在 planning approval。 |
| #114 | open | 当前任务 | `guru-review-contract-wording` semantic closed loop、三个固定 profile、versioned evidence、generic deterministic scanner/recorder/checker、三个唯一 typed-exit consumers，以及 planning approval adapter 与 #93 legacy owner 删除。 |
| #101 | open | 当前任务 | `guru-review-change-request` semantic readiness closed loop、三类 target、current prerequisite linkage、十项 dimensions、五个唯一 consumer、stdout-only record/check、active #112 transition 与旧 readiness route replacement。 |
| #110 | open | 已实现前置合同 | `guru-sync-base` public deterministic closed loop：ordered-candidate-first 四级 base resolution、digest-bound ff-only sync、三方 equality、stdout facts、typed exits、prepare-task reuse、interface schema 1.2 双 profile与 preset/platform distribution。`synced` 唯一进入 #111。 |
| #111 | open | 当前任务 | `guru-discover-change-context` public semantic closed loop：workflow/standalone freshness parity、current-state-first、archived finish-summary index preview、AI 1-3 candidate deep-read、mem insufficiency gate、current stale-code/superseded-digest refresh re-entry、Git-trackable same-snapshot task-local persistence 与三个唯一 typed-exit consumers。 |

## 9. 当前扩展边界

已经实现的边界：

- 本仓库维护 `guru-team` 可复用 workflow 与 preset，不 fork 官方 Trellis。
- 脚本可以执行事实动作、校验 JSON/hash/HEAD/diff/dirty state，但不替代 AI 判断。
- Platform overlay 是 harness 适配层，不是新的 workflow source。
- Subagent 技术 `name` 是调度 API，不为了中文 UI 展示改名；中文展示名通过 description、标题和 `agent-assignment.json.logical_role` 表达。Codex 当前 `nickname_candidates` 只能是 ASCII，不能用它承载中文展示名。
- Task artifact 是任务证据，不是 durable docs 的替代品。
- PR publish 必须经过 finish-work 与 review/readiness evidence，不能由普通 `publish-pr` 直接触发。

尚未在本目录展开的内容：

- 每个 companion script 的完整 CLI 参数合同。
- 每个 platform overlay 的逐文件行为差异。
- Throwaway install 在不同 Trellis CLI 版本上的兼容性矩阵。
- 完整 upgrade/update 漂移测试记录。


## Push 后远端 Marketplace 门禁

修改 marketplace/preset/overlay/schema/public API 的发布路径会在 branch push 后、`gh pr create` 前执行远端分支 `init`、preview、switch 和 preset reapply，记录 task-local `marketplace-verification.json`。缺失、失败、HEAD 不匹配或 stale artifact 会阻止创建 PR；该门禁不创建 tag，AI 仍负责 PR readiness 判断。

## Skill 行为评测合同

Guru Team extension 必须从 Interface 1.3 发现 exact public invocation、input
profile、declared exits 与 per-exit output schema，并对 package-local versioned
corpus 的每个 case 实际执行公开 wrapper。Runner 只做确定性 parsing、schema、
exit、closed assertions、external grading binding 与 evidence 汇总；semantic
pass 只能来自显式外部 grader，human feedback 独立。结果状态为
`passed|evaluation_failed|execution_error|unsupported`，run evidence 仅写 repo
外临时目录。shared/Codex/Claude/Cursor adapter 使用同一 corpus bytes，普通
workflow/standalone invocation 不读取任何 eval asset。每个 adapter descriptor 绑定一个
安装时校验 executable mode 的 wrapper；runner 只从 descriptor path 调用它。Shared
解析 preset-managed native executor，Codex/Claude/Cursor 从 `PATH` 检测 documented native
command，传递 exact `SKILL.md`、public wrapper、prompt
与 staged files，并收集平台 argv、public output 和 trace；native 缺失为 `unsupported`。
Runner 在 native execution 外读取 canonical corpus，并只向 native 提供 repo/package 外
public-only projection、case workdir 与最小 request；canonical package/corpus/private runtime
locator 均不进入 native context。Trace evidence 使用
`guru-team-skill-eval-native-trace-1.0`：native CLI 必须经 repo 外 helper 完成 projected exact
Skill read 与 exact wrapper invocation，receipt 绑定 request、projection、Skill/wrapper digest、
argv、return code 和 DTO output。合法 DTO 缺 receipt，或 projection 暴露 eval/private runtime，
均为 `execution_error`。

Production semantic case 引用 repo-local checker-passed owner result；actual exit 决定
per-exit output schema，`expected_exit` 只在 wrapper 返回后参与比较且不进入 adapter/native
request。Codex 使用 trusted Git root，Claude 使用 safe non-interactive 输入，Cursor 未登录
确定返回 `unsupported`。Interface 1.3 scalar `required` 为显式 boolean；
`guru-sync-base --base-branch` optional omission 继续复用 formal resolver。
