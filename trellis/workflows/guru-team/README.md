# Guru Team Trellis Workflow

本目录维护 Guru 团队可复用的 Trellis workflow。

这个 workflow 的 marketplace id 固定为通用的 `guru-team`。它只承载 global
phase/status route、14 个 mandatory Skill invocation、54 个 typed exit、31 个
workflow/stop target，以及 workspace、Docs SSOT、Issue Scope Ledger、human artifact、
interaction 和外部 side-effect boundary。具体 intake、planning、check、review、
publication 与 finalization 判断由对应 active package 独占。

Guru Team extension 版本不等于官方 Trellis CLI 版本，也不等于 `trellis/index.json`
里的 marketplace index schema version。canonical extension version 和目标官方
Trellis CLI 版本位于 `trellis/guru-team-extension.json`；preset installer 会把当前安装版本和 source
provenance 写入目标仓库的 `.trellis/guru-team/extension.json`，并通过
`check-env --json` / `version.sh --json` 暴露给用户和 AI 排障流程。

## Marketplace 安装

```bash
trellis init -y --codex --cursor \
  --workflow guru-team \
  --workflow-source gh:castbox/guru-trellis/trellis#v0.6.5-guru.3
```

`-y` 是团队默认安装路径的一部分，用于跳过交互式 spec template picker。自动验收、
throwaway 安装验证和 README 默认命令都必须使用非交互形式；只有用户明确想手动选择
spec template 时，才去掉 `-y` 或改用官方支持的 `--template <name>`。

稳定安装 source 使用 repo release tag `#v0.6.5-guru.3`，并要求官方 Trellis CLI 安装到
`0.6.5`。维护者刻意跟随最新 `main` / canary 时可以去掉 `#ref` 或改用其它 branch/tag ref，
但应在验证和排障报告中说明 source 是否为 mutable ref，以及是否仍以官方 Trellis `0.6.5`
为目标基线。Guru Team release tag 使用 repo 级 `v<official-trellis-version>-guru.<revision>`，
并与该 tag 所指提交中的 `trellis/guru-team-extension.json.version` 精确映射。当前已发布
stable 是 annotated tag `v0.6.5-guru.3`，peeled source commit 为
`dbcbbb2d2776a3952b643b6bcce0a2693d103273`，canonical extension version 为
`0.6.5-guru.25`。Repo release tag 与 extension revision 是独立版本轴；workflow marketplace
与 preset 必须来自同一个 immutable tag。

已有 Trellis 项目切换 active workflow：

```bash
trellis workflow \
  --marketplace gh:castbox/guru-trellis/trellis#v0.6.5-guru.3 \
  --template guru-team
```

只有在需要生成 `.trellis/workflow.md.new` 做人工 review、且不切换 active
workflow 时，才使用 `--create-new`。

## Companion Assets

Workflow marketplace 只安装 global .trellis/workflow.md；完整 Guru Team extension
由 preset 安装。公共 Skill 唯一 canonical root 是 trellis/skills/guru-team/，
installed 与 Shared/Codex/Claude/Cursor discovery copies 都是 managed projection，
不能反向成为语义来源。

当前 registry 激活 14 Skills / 54 exits，global workflow closure 为
14/54/31（14 invokes / 54 exits / 31 targets）。Phase 0 到 Finalization 的
active ids 为：

- guru-select-workflow-mode
- guru-sync-base
- guru-discover-change-context
- guru-clarify-requirements
- guru-review-contract-wording
- guru-review-change-request
- guru-create-task-workspace
- guru-approve-task-plan
- guru-check-task
- guru-create-task-commit
- guru-review-branch
- guru-review-task-publication
- guru-verify-extension-installation
- guru-finalize-task

Global workflow 只写 phase/status route、mandatory invoke marker、typed exit、唯一
consumer/stop 与全局边界。每个 package interface.json 独占 public input、per-exit
output、consumer input、thin projection、target-owned authoring partition 与 package
内部行为；workflow、README 和平台入口不得从 runtime implementation 或 package
artifact 重建路由。

guru-review-branch 是 sole Phase 3.5 semantic owner。Branch Review passed 后，
workflow mandatory invoke guru-review-task-publication；Publication owner 直接从 live
authority 生成并审查 exact Chinese PR title/body。其 ready 4.0 DTO 无损投影 payload，
只有 ready 进入 guru-finalize-task。Finalizer 的
verification、stale、resume 与 reprepare exits 按 Interface 自动路由，不形成新的用户
continuation gate。

Finalizer stale DTO 只增加 Publication 唯一 consumer 直接使用的
`branch_review_commit`；真实 descendant content
drift 只能由 Publication 语义门禁返回现有 Phase 2 router，不能产生 `ready`。

Interface 1.3 的十二条 semantic package handoff 使用 target-owned
skill_input_authoring_seed；producer 只给 minimal seed，target authoring 补齐其自己拥有
的 fresh semantic input，projection 只允许 direct/select/rename/normalize。
`production-current-v1` 是 planning/check/commit 唯一 current manifest，固定为三包、
11 exits 和四条 authoring-seed edges。

workflow mode 表示 mandatory global route；standalone 表示平台直接发现。两种模式都
依赖完整、current Guru Team preset，单独复制 Skill 目录不是
self-contained/portable 安装。公共 wrapper 通过 installed executable
.trellis/guru-team/scripts/bash/run-skill-command.sh 调用 shared run-skill-command
dispatcher；缺 runtime、版本漂移或未解决 sidecar 时必须在业务副作用前 fail closed。

当前 canonical extension version `0.6.5-guru.25` 已由上文 pin 的 stable release tag
`v0.6.5-guru.3` 发布。Source/installed package validation 必须同时验证
registry、14/54/31 marker graph、consumer uniqueness、projection、selected-platform
byte identity 和 executable mode。

## Workflow Authoring Ownership

Canonical workflow 是 trellis/workflows/guru-team/workflow.md；dogfood
.trellis/workflow.md 必须 byte-identical。Global Markdown 只拥有 phase order、
current-task router、14 mandatory Skill markers、54 exits、31 workflow/stop targets、
workspace/task activation、Docs SSOT、Issue Scope Ledger、human artifact、
interaction 与外部 side-effect boundary。Step-local 合同只存在于对应 active
package/interface。

Official Trellis 独占 trellis-start、trellis-continue、trellis-finish-work、官方
hooks、sub-agents、runtime agents、bundled skills 与 meta references。Guru preset
不安装、不 patch、不 managed-upgrade 这些路径；mandatory Guru routing 由 active
workflow markers 和 installed guru-* packages 保证。

Preset overlay tree 只保留三个 Guru-owned explicit entry：

- .codex/prompts/guru-finish-work.md
- .claude/commands/guru/finish-work.md
- .cursor/commands/guru-finish-work.md

这些 entry 只读取 live context 和 .trellis/workflow.md、调用 public Skills、消费
mapped exits，并返回 terminal result。它们不读取 producer-private runtime/artifact，
不复制 package input fields、review dimensions、interaction algorithm 或 executor
commands。

Current-only ownership schema 3.0 固定为 11 条 anchored Guru-owned rules、9 条
managed claims 和上述 3 个 additive overlays，只记录 current Guru-owned assets；
非 current ownership/installed manifest 在 mutation 前统一
fail closed，不存在 projection 或迁移入口。当前更新顺序为：

1. official trellis update 或目标版本升级；
2. 重新选择 guru-team marketplace workflow；
3. reapply Guru preset；
4. 处理所有 .new/.bak 与 local-edit conflict；
5. 运行 source/installed package、ownership、platform identity、dogfood drift 与
   recursive zero-sidecar checks。

维护者在 preset mutation 和 combined acceptance 中运行：

    trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json

该 validator 只检查客观 ownership facts，不进入 workflow route，也不替代 AI
semantic judgment。

## Phase 0 Base Sync

Tool-free request classification 后，repo-changing route 的第一个 mandatory invocation
是 `guru-sync-base`。它按显式 `--base`、非空 scalar `base_branch`、配置顺序中第一个
existing `base_branch_candidates` ref（缺省 `dev -> develop -> main -> master`）、候选均
不存在时的 remote default 解析 selected base；current branch 不是隐式 fallback。多个
existing candidates 不歧义，配置顺序就是优先级。Deterministic executor 以 pre-sync
resolution digest 绑定重新解析、fetch 与可选 `git merge --ff-only`，同步后生成
`post_sync_resolution` / `post_sync_resolution_sha256`。

成功结果使用 `guru-base-sync-result-1.0`，并且必须证明 checkout clean、decision checkout
HEAD、local base HEAD 与 remote-tracking HEAD 三方相等。`sync-base` 在 stdout 输出
resolution/result facts，`check-base-sync --result-json` 校验 schema、pre/post digest 与 live
Git facts，并把 post-sync digest 交给下一 consumer；二者不创建 evidence file。该 package
声明 `judgment_mode=deterministic`，没有
selected-base AI confirmation、post-execution AI Review Gate 或 human confirmation；AI 只在
Skill 外负责 tool-free route classification。Stable exits 与唯一 consumers 是：

- `synced` -> `guru-discover-change-context`
- `skipped` -> `original-request-route`
- `blocked` -> `base-sync-blocked`

Workflow mode 中 `synced` 的唯一 consumer 是 `guru-discover-change-context`；
`check-env`、issue/duplicate reads 与 `prepare-task` 仅可在 `synced` 后作为独立的
current query-only diagnostic，不是 workflow hop。Standalone mode 可由所选平台直接发现
同一 Skill，但仍要求完整 compatible preset/runtime；workflow-only
`--record-skipped original-request-route` 不可在 standalone 调用。Managed executable commands 位于
`.trellis/guru-team/scripts/bash/sync-base.sh` 和
`.trellis/guru-team/scripts/bash/check-base-sync.sh`。

## Phase 0 Change Context Discovery

`guru-sync-base:synced` mandatory invoke semantic
`guru-discover-change-context`。Workflow/standalone entry preconditions 完全一致；Skill
固定先读 live change 与 duplicate facts，再 AI review updated-base Docs、
code/API/config/schema/ownership 和 tests/fixtures/throwaway/update，之后形成 canonical
query，执行一次 archived history preview，并由 AI 选择 1 至 3 个 candidates 窄读和完成
AI Review Gate。零候选是成功路径，固定 empty selection/deep reads 与一致的
`mem_review=not_needed` shape，且不得触发其它历史源；duplicate reuse/new target 决策不在本 Skill 内。

History runtime 只枚举 archived `finish-summary.json` 并只投影 `index.*`，使用
`guru-context-history-score-1.0` 产生稳定 query、archive manifest 和 preview digest、
invalid isolation、固定 sort/limit/projection。`trellis mem` 只有四类主证据源都不足以
解释命名 load-bearing decision 时才进入。完整 semantic evidence 保留在当前 AI cognition
与调用期 owner result 中；record/check/public invoke 通过 stdin/stdout 串联，正常
pre-task/standalone 不写 task、workspace 或 runtime artifact。Recorder/checker 执行
published closed Draft 2020-12 `guru-change-context-owner-result-2.0` schema；base evidence
嵌入完整 validator-passed sync result并绑定 post-sync digest、selected remote refs 与严格
GitHub repo identity。Git status failure 不得冒充 clean，base stale 在 live issue/draft、
reviewed blob 与 archive preview 前短路。Draft-created-issue binding live 校验原 reviewed
body；caller-authored `refresh_base` 必须与 stable live stale codes 一致，`context_ready`
对同一 stale 拒绝。Archive reader
以普通 file/read/JSON/index-shape failure 形成 portable invalid evidence。
Deep-read locator 按 selected task artifact、canonical GitHub issue/PR 与 exact Git object/ref
三类闭合校验。Closed schema 与结构化 locator 不保存 raw source payload，也不做
跨字段扫描；不写 workspace/runtime/repo cache。

正常 mapped active-task 调用通过 ephemeral task identity 绑定 direct task branch 与当前
task worktree，允许普通进行中 edits，但不创建 checkpoint。只有 active-task owner loop 确实跨调用中断时，才在 ignored
`owner-checkpoints/<task-key>/` 下惰性创建同一 owner 的最小 current checkpoint。正常
mapped exit 不创建 checkpoint；stale 删除 current checkpoint 后从 live authority 完整重跑；
public projection/schema 校验成功后立即 consume-and-clean owner input/result/checkpoint 与
空目录。下游 Clarify 只消费最小 DTO，不读取或删除 Discovery private state。

Source issue 支持 GitHub live `open` / `closed`，runtime 将受支持的 state casing
归一为小写；duplicate candidates 与 draft-created issue binding 仍是 open-only。
Current Docs、code/contracts、tests 的 40 位 Git identity 必须从 `HEAD:<path>` 解析为
exact `blob`，tree、gitlink commit、tag、missing object 或 identity drift 均 fail closed。

Duplicate candidate 的 deterministic fact projection 是 normalized bound `repo`、positive
`number`、`identity=#<number>`、canonical issue URL、`state=open` 与 `updated_at`；pure
gate 从同一次 open duplicate search 返回字段重算排除 reason/observation 的
`facts_sha256`、identity 与 URL；record/check 不运行第二次 search 或 candidate re-read。
`blocked` exit 与 blocked AI Review Gate 在 schema/runtime 中
双向绑定。

Record/check production entry 先执行 pure schema/digest/semantic shape，再执行
base-only live gate；repo-bound locator、issue、reviewed blob 与 archive/history 仅在 fresh
base 后读取。`refresh_base` record/check 记录并核对当前 stable stale codes、superseded
query/result digests、reason 与 detection time，然后要求整步从 live authority re-entry，
不重建 snapshot ancestry。Base stale 随后只匹配 caller-authored refresh codes 后返回。
`change_input` 十组 clue arrays 至少一组非空，issue binding/canonical query 不得
替代。Portable locator 只按 source-specific closed structure 验证，不扫描整份 payload。

Owner-result schema 是 `guru-change-context-owner-result-2.0`；managed commands 是
`preview-change-context-history`、`record-context-discovery` 和
`check-context-discovery`。Exits 是 `context_ready` -> active
`guru-clarify-requirements`、`refresh_base` -> `guru-sync-base`、`blocked` ->
`change-context-blocked`；source/installed validator 同时解析 active Skill consumer 及唯一
workflow/stop target markers。

## Phase 0 Requirements Clarification

`guru-discover-change-context:context_ready` mandatory invoke semantic
`guru-clarify-requirements`。Initial issue/draft、active-task scope change 与 standalone review
共享相同 preconditions、AI Gate、仅服务真实选择/副作用的当前对话交互与 freshness。Repository-answerable questions
必须先由 current Docs/code/tests/history/GitHub/Git evidence 回答或记录不可回答证据，
`answered`至少有一个checked ref。之后每轮只问一个最高价值问题，question id必须来自opened/current-open，
`partial`不得关闭 question，reducer固定为`open_questions = opened - closed`。

AI 拥有 scope/action/交互必要性/pass/block/route 判断。Recorder 派生 proposal/action/
payload/content/result digest；checker 重算 schema/digest并只读验证 live source/context/task
binding。Package 没有 GitHub mutation executor；comment/body 写入仅在 AI 复核 live preimage
并在当前对话完成真实副作用确认后使用现有 connector 或审查过的 `gh`，写后必须
重读；reviewed payload、payload digest、mutation result与live content必须一致，授权不进入
recorder/checker。成功 mutation
返回 `refresh_context`，不直接 `clear`。

Pre-task/standalone 结果 stdout-only且无专用 artifact。Active-task owner result 临时绑定
GitHub-visible authority、`issue-scope-ledger.json`、当前 planning/context/task-update 与 re-entry owner；
ledger 只接收不可重新推导的 compact classification。Schema 是
`guru-requirements-clarification-2.0`，commands 是
`record-requirements-clarification` / `check-requirements-clarification`。Active-task Scope Change
Gate mandatory invoke同一Skill。Exits 为 `clear` -> caller-aware
`guru-requirements-clear-router`（initial/draft -> #114 wording，standalone -> caller，active ->
planning review或exact interrupted progression）、`needs_context` -> context discovery、`refresh_context` -> base sync、
`retarget_context` -> base sync 并对 selected open issue 完整重跑 Intake、
`new_task` -> staged #112 full intake route、`blocked` -> fail-closed stop。

只接受 closed 2.0 artifact；其他 schema version 在 normalization 前 fail closed，
recorder/checker 不执行迁移或投影。

Active-task `clear`/`new_task` 要求非空且全部属于七类 terminal decision 的 proposal set；
五类 scope classification 无论 origin 均要求最终 disposition；只有真实产品/范围选择仍未决时才在当前对话询问。
compact owner-result `decision_trail` 精确保存 `trail_id`、proposal id/digest/decision 与 live
GitHub authority kind/URL/content checksum。`issue-scope-ledger.json` 是 closed scope-only 2.0，
只含 schema version 与 primary/close/related/followup issue；trail 和
planning/context/review/stale/interrupted/re-entry 均由 checker 从 owner 或 live facts 重读，
不进入 ledger。`mechanism_removed/replaced` 使用 optional origin，
不进入 trail/action mutation。GitHub authority mutation 后只能 `refresh_context`；context
时间覆盖 live authority 后 task update preimage 绑定当前 context digest，不要求第二次 refresh。Active-task `new_task` 仍只给 #112
side-effect-free reviewed draft。

## Contract Wording Review

`guru-clarify-requirements:clear` 对 initial issue/draft mandatory invoke semantic
`guru-review-contract-wording`；Phase 1 在展示规划链接前再次用固定
`planning_artifacts` profile 调用同一 Skill。Standalone caller 只能用
`explicit_paths` 审查本轮明确指定的 repo-relative Markdown 文件。Canonical package
独占三个 profile、`contract-wording-v2` vocabulary、
`contract-wording-classifications-v1`、AI rewrite/review、confirmation policy、schema
`guru-contract-wording-review-1.0` 与 `pass` / `content_changed` / `blocked` exits；workflow
只拥有 mandatory invocation、profile-aware router 与 fail-closed stop。

Runtime commands 是 `record-contract-wording-review` 与
`check-contract-wording-review`。它们只重建 fixed scope、执行 deterministic scan、派生
digests/unchecked projection，并校验 schema、freshness 和 Gate/exit invariant；不选择
classification、rewrite、semantic pass 或 route。`change_request` selected comment 缺
author/updated time 会 fail closed；live issue revision 由 recorder 派生 confirmed-payload
与 mutation-result digests，并由 checker 绑定 reviewed payload、preimage、current reread
content/source update time。所有 profile 的完整结果都只作为 stdout-only owner-private
证据；`planning_artifacts:pass` 由 typed-exit router 立即消费，不写 task-local
`contract-wording-review.json`。该 profile 仍必须按 canonical contract 显式记录
`semantic_review.ai_review_gate.planning_checked_dimensions`；成功 exit 要求其 exact shape
全部为 true，deterministic runtime 只能验证，planning owner 会直接重读当前三份规划，均不得生成语义
结论。`content_changed` 要求对应 profile 完整重入；任何 active approval 若缺少当前
planning-only binding，必须重新执行完整 AI wording
review，再由 planning owner 重读三文档；禁止手补布尔值或重建 replacement digest chain。
Archived artifact 不改写。

## Phase 1 Task Plan Approval

Phase 1 在 current `guru-review-contract-wording:planning_artifacts:pass` 后 mandatory
invoke active semantic Skill `guru-approve-task-plan`。Workflow 与 standalone mode 使用相同
八项 entry preconditions，并依赖完整 Guru Team preset、shared dispatcher 与 runtime。
Canonical package 是 planning adequacy、provenance、supported unusual scenarios、AI Gate、
真实选择或副作用的对话内交互必要性和 re-entry 的
唯一 owner；workflow 只声明 invoke 与 typed routing。

唯一 owner checkpoint 是 ignored-runtime `planning-approval.json`，schema id 为
`guru-planning-approval-3.0`。Runtime commands `record-planning-approval` /
`check-planning-approval` 只记录已完成的 AI semantic result，并校验 schema、task/planning
locator、required file、一个 owner-private 组合 planning-content freshness token 与 closed
exit union，不生成 semantic pass 或 route。该 token 只由相邻 checker 重算以发现同路径内容
漂移，不是授权、semantic approval、public handoff 或全链 authority。四个 exits 是：

- `approved` -> workflow target `phase-1-task-activation`；
- `revision_required` -> `guru-approve-task-plan`；
- `clarify_scope` -> routing-only workflow target
  `guru-task-plan-clarify-scope-router`；该 target 只消费
  `exit_id`/`task_ref`/`proposal_refs`，建立 scope context 后 mandatory invoke
  `guru-clarify-requirements:active_task_scope_change`，完整 semantic input 由
  caller AI 基于 fresh live context 编写；
- `blocked` -> stop `task-plan-approval-blocked`。

Task activation 或真实 scope choice 所需授权只存在于当前对话，不写入 owner checkpoint、
public DTO 或 archive。Planning approval 只接受当前 schema 3.0；其它 schema 或字段直接
fail closed，不执行升级、投影或兼容 re-entry。AI 对格式、拼写、链接、
派生文本与 workflow metadata 做 semantic delta classification，只刷新真实依赖；authority、
scope、design、acceptance、behavior 或 verification 变化才重入对应 semantic owner。

## Phase 0 Change Request Readiness

`guru-review-contract-wording:change_request:pass` mandatory invoke semantic
`guru-review-change-request`。Workflow 与 standalone 使用相同 preconditions，只消费 current、
checker-validated context、clarity 与 wording evidence，并绑定同一 target/content identity。
Target 固定为 `existing_issue`、side-effect-free `proposed_draft` 或
`standalone_request`。Canonical package 独占十项 readiness dimensions、findings、delivery
unit、scope conclusion、AI Review Gate、conditional confirmation 与 route judgment；global
workflow 和平台入口不得复制这些 step-local semantics。

Schema 是 `guru-change-request-review-1.0`，稳定 artifact basename 是
`issue-review.json`。`record-change-request-review` / `check-change-request-review` 复用现有
context/clarity/wording objective validators，重建 target projection、linkage 与 facts digest，
只校验 schema/hash/ref/freshness/Gate/consumer/ready invariant，并原样返回 AI-authored exit；
它们不搜索 duplicate/history、不读取 Docs/code/tests 作语义判断，也不生成 finding、delivery
unit、Gate 或 route。Pre-task/standalone 固定 stdout-only，#101 不创建 task、workspace、cache、
sidecar 或 tracked artifact。

五个 stable exits 与唯一 consumers 是：

- `ready` -> active `guru-create-task-workspace`
- `clarify_requirements` -> `guru-clarify-requirements`
- `review_wording` -> `guru-review-contract-wording`
- `refresh_context` -> `guru-sync-base`
- `blocked` -> `change-request-review-blocked`

`ready` 不得回退 `guru-full-task-intake-chain`、`check-env` 或 `prepare-task`。
Active `guru-create-task-workspace` 是唯一 mutation owner，直接消费当前 checked `ready`
exit，并且只持久化有真实后续 consumer 的 task-local `issue-scope-ledger.json`；不写
tracked `issue-review.json`。

## 中文 Conventional Commits

`guru-team` workflow 强制进入 PR 分支或 `main` 的提交使用中文 Conventional
Commits。工作提交和 Trellis metadata 提交 subject 格式为：

```text
{type}({scope}): #{primary_issue} 中文描述
```

工作提交 body 必须按 `背景：`、`变更：`、`边界：`、`验证：` 固定顺序编写，并用
`Refs #<primary_issue>` 作为 footer；不得在 commit message 中使用 close keywords
（`Closes` / `Fixes` / `Resolves` / `Close` / `Fix` / `Resolve`）。Issue 关闭语义只放在 PR body 的
`issue-scope-ledger.json.close_issues` 范围内。Trellis metadata 提交必须为空 body，
例如 `chore(trellis): #73 固化任务收尾元数据`。

本仓库保留 merge commit，最终 merge commit subject/body 必须由 publish payload 或
formatter 明确生成：

```text
chore(merge): #{pull_request} 合并 #{primary_issue} 中文 PR 摘要
```

companion helpers 只做 objective 校验和格式化，不替代 AI review：

```bash
.trellis/guru-team/scripts/bash/check-commit-messages.sh --json --task <task-path>
.trellis/guru-team/scripts/bash/format-merge-commit.sh --json \
  --task <task-path> \
  --pull-request <pr-number> \
  --summary "中文 PR 摘要"
```

Fresh final Phase 2 check 后，canonical workflow mandatory invoke
`guru-create-task-commit`。Skill 为每次提交在 ignored
`.trellis/.runtime/guru-team/task-commit-plans/<task-key>/<sequence>.json` 生成临时
candidate，AI 负责 scope/path/message/mechanical review；展示唯一 commit 副作用并只在
当前对话取得确认后，exact executor 才 stage 计划路径并验证真实 commit。candidate 不含
授权信息、永不 tracked/staged，成功后删除，只返回
`pre_commit_head`/`commit_sha`；Git 可推导的 result/tree evidence 不回写 task handoff，
所以成功提交不会制造 post-commit dirty。失败 candidate 仅用于同一未完成操作的 bounded
recovery；既有 tracked plan 只读兼容。`committed`、`revision-required`、`blocked`
分别由 Branch Review/finding closure、skill re-entry、fail-closed stop 唯一消费；finding
fix 必须先返回完整 Phase 2，并创建新 sequence。

`finish-work` dry-run 会输出合规 metadata commit subject 和 publish 计划；
`format-merge-commit` payload 会输出 `merge_commit.subject`、`merge_commit.body`
和显式 `gh pr merge ... --subject ... --body-file ...` 命令。维护者合并 PR 时不得使用
GitHub 默认 `Merge pull request #xx from ...` subject，也不得把中文 PR title
`完成：#xx ... (#yy)` 直接作为 commit subject。

## Knowledge Gate 与 Docs SSOT

当任务可能涉及 Guru Team 中台 SDK / framework 时，AI 应按 `.trellis/workflow.md`
检查当前平台是否可用 `guru-knowledge-center` MCP。可用时使用
`project_domain=middle-platform` 和当前 task context 检索，并把 citation 写入
`design.md`、`implement.md` 或 `{TASK_DIR}/research/middle-platform-knowledge.md`。
MCP 不可用时，默认 `optional_warn` 只告警并继续；配置为 `required` 时才阻塞。

Trellis task artifact 不是长期 repo docs 的替代品。Planning 阶段必须创建或更新
同一个 `Docs SSOT Plan`，推荐由 `design.md` 承载权威计划；`prd.md` 记录 docs 状态
和需求影响，`implement.md` 记录 checklist / checkpoint。计划需要记录 docs 状态：
`complete_docs`、`partial_docs`、`stale_docs`、`no_docs`；以及同步策略：
`ssot_first`、`delta_first`、`bootstrap_or_repair_docs`、`no_docs_update_needed`。

`Docs SSOT Plan` 还要列出证据路径、策略理由、当前 task 影响或检查过的 durable docs、
需要 merge 回 durable docs 的 task artifact delta。`delta_first` 必须写 merge checkpoint；
`bootstrap_or_repair_docs` 必须写最小修复范围或受限 follow-up；`no_docs_update_needed`
必须写具体理由。大范围、边界清楚的需求 / 设计 / workflow / API / 数据 / 部署 /
运营 / 测试合同变更应优先 `ssot_first`。无完整 docs 系统的 repo 也要明确记录创建
docs、补 partial / stale docs，或受限 follow-up 的结果。

业务项目内人类可读文档默认使用中文，覆盖 `.trellis/spec/**` 项目规范、
`.trellis/tasks/**` task artifact、`docs/**` durable docs、`00-bootstrap-guidelines`
创建或补齐的 docs SSOT，以及 workflow/helper artifact 中的 summary、evidence、
finding、observation、follow-up candidate、PR title/body 等字段。命令、路径、配置键、
GitHub keyword、外部 API 名称和代码符号等 literal token 可保留英文。`guru-trellis`
源码仓库自身是公共扩展仓库，它的 README、源码注释、脚本帮助和 marketplace metadata
可按分发需要保留英文或双语。

对 issue-backed、task-like 或需要文件修改的 `no_task` 请求，tool-free classification 后的
第一跳是 semantic `guru-select-workflow-mode`。`standard_intake` 才进入 mandatory
`guru-sync-base`；`task_free` 只进入当前 checkout 的限定编辑目标。明确 task-free 意图不再
确认，隐含意图最多确认一次，拒绝自动回到 `standard_intake`，不确定时保守走标准 Intake；
模式确定后 mapped exit、普通恢复和同范围重试不重复询问。只有 standard Intake 的
typed exit `synced` 才进入：

`guru-discover-change-context -> guru-clarify-requirements ->
guru-review-contract-wording -> guru-review-change-request ->
guru-create-task-workspace`。以下命令是 current query-only diagnostic，不是 active
workflow hop：

```bash
.trellis/guru-team/scripts/bash/check-env.sh --json
.trellis/guru-team/scripts/bash/prepare-task.sh --json \
  --expected-resolution-sha256 <post-sync-resolution-sha256> \
  "<user request or issue URL>"
```

`prepare-task.sh --json` 只执行 current query，不创建 GitHub
issue、worktree、branch 或 Trellis task。
它只在 stdout JSON 中输出 source/proposed issue、duplicate candidates、selected base、
`base_freshness`、branch/task/workspace naming suggestions 与 `naming_quality`；不输出
workspace absolute path、task-create command、authorization/handoff state，也不写 task/runtime
context。在 `gh auth status`、issue read
与 duplicate search 前，planner 必须通过 shared strict core 重解析和同步 selected base；
`fetch_performed: false` 或三方 HEAD 不相等都不能成为 `fresh: true`。Selected local base
落后时，只能在 selected-base checkout 上执行 `git merge --ff-only`；wrong checkout、dirty、
missing ref、fetch failure、divergence、resolution drift 或 post-sync mismatch 均 fail closed。
Every prepare invocation receives the preceding validator/guard post-sync
resolution digest and the same resolver inputs. It preserves
explicit/config/config-candidate/remote-default provenance. Issue, branch,
worktree, task, artifact, and runtime mutations belong exclusively to
`guru-create-task-workspace`.

Resolution/result facts remain stdout-only. The query consumes the current
post-sync digest and reruns the shared resolver/sync core before its reads;
workspace mutation freshness is independently owned by
`guru-create-task-workspace`. There is no
resolution lease, release command, result-evidence cleanup, repo runtime record,
or task artifact for these pre-task facts.

`naming_quality` 是 slug / branch / worktree / task 命名质量门禁。AI 读完 issue 后
应生成语义英文 short-name，并通过 `--short-name`、`--workspace-slug`、`--task-slug`
传给脚本；需要特殊分支名时再显式传 `--branch`。推荐 worktree/task slug 格式为
`NNN-business-capability`。未显式传 `--branch` 时，branch 格式为
`<branch-type>/NNN-business-capability`，其中 `branch-type` 只能是 `feat`、`fix`、
`refactor`、`perf`、`test`、`docs`、`style`、`build`、`ci`、`chore`、`revert`，
未知语义 fallback 为 `chore`，例如
`feat/052-resume-detail-inline-attachment-preview`。中文或非 ASCII issue 标题不依赖拼音
transliteration 作为默认分支名；脚本不会智能翻译，只会做确定性类型判定、拼装、冲突检查和
低信息命名阻断。

Active workspace Skill 使用三个 managed runtime commands：

```bash
.trellis/guru-team/scripts/bash/record-task-workspace-plan.sh --json ...
.trellis/guru-team/scripts/bash/create-task-workspace.sh --json ...
.trellis/guru-team/scripts/bash/check-task-workspace-result.sh --json ...
```

Package schemas 是 ignored-runtime `guru-task-workspace-plan-2.0` 与
`guru-task-workspace-result-2.0`。Workflow/standalone preconditions 完全一致。
Reviewed draft invocation 只取得 `github_issue_mutation` confirmation，创建 exact issue 并
重读后固定返回 `refresh_review`；同一调用不创建 branch/worktree/task。完整 Intake 重跑后，
open issue invocation 另行取得 `workspace_and_task_mutation` confirmation。外部出口固定为
`created`、`refresh_review`、`blocked`。Passed + confirmed 才可 mutation；用户拒绝时在
recorder/executor 前停止且不生成 DTO，`reroute` 与 `blocked` 分别生成 checker-validated
zero-write `refresh_review`、`blocked` result。

Draft create 前按 exact open title/body/labels 与 `createdAt >= reviewed plan`执行 0/1/>1
recovery：0 个创建，1 个恢复并 live reread，多个阻断。完整 Intake 重入后的
workflow-created issue必须携带完整 checker-passed created-issue result，并重验 result/binding
digest、reviewed draft identity、current issue 与 fresh context canonical live
existing-issue identity；该 context使用`kind=issue`与 null `issue_binding`。

Assignee 固定按 explicit input、exactly one issue assignee、zero issue assignees 时 current
GitHub login、multiple/unresolved 时 AI/user 选择解析；executor 始终向 official
task-create handler 显式传 reviewed assignee。Executor 在隔离子进程中调用 official
`common.task_store.cmd_create`，并仅在该 handler 调用内禁用 developer accessor，使
`task.json.assignee` 与 `task.json.creator` 都等于 reviewed login。创建成功除 official
`task.json` 外只写 tracked task-local `issue-scope-ledger.json`；其余 Intake evidence、
plan/result 保持 ignored owner-private，本机 mapping 只在 ignored
`.trellis/.runtime/guru-team/**`。Public result 不含 absolute workspace path；checker
从 current config、reviewed slug 与 live Git facts 推导 worktree。

`workspace_mode: worktree` 下，task artifact 写入边界由 current `task.json`、当前 checkout、
`.trellis/.runtime/guru-team/**`、`git worktree list` 和
`check-workspace-boundary.sh --task` 推导/校验。
在写入或校验 `planning-approval.json`、`phase2-check.json` 或
`review-gate.json` 前，从目标 worktree 运行：

```bash
.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task <task-path>
```

该 validator 只提供机器事实：expected workspace、actual repo root、source checkout
status、task worktree status、source checkout 中可疑同名 task artifact / review
metadata，以及 fail-closed 错误。它不判断 sub-agent 是否 stale，不迁移误写 patch，也不
清理 source checkout；这些仍由 AI/human workflow 决定。手工编辑工具不能接收显式
working directory 时，必须使用 boundary helper 已确认的当前 task worktree 下的绝对路径。

`create-task-workspace` 在 GitHub 或 worktree/task mutation boundary 重跑 shared core。每次 fresh result 都记录
`preflight.base_freshness` 并要求 decision/local/remote HEAD 三方相等。Initial planner
evidence 不能替代 mutation-time guard；不要从过期的本地 `main` / `dev` 创建任务分支。

Plan 绑定 initial checker-passed `post_sync_resolution_sha256`。Executor 在首次业务 mutation
前只运行一次 shared resolver/sync core；若 fetch发现remote前进，允许安全 fast-forward，
但必须返回 `refresh_review` 且不创建 issue/workspace/task/artifact/runtime。Post-sync identity
不变才继续；后续同一 invocation boundary只重验已刷新本地 facts。

Guru preset apply/update/reapply 与 workspace executor 不读取、不创建、不复制、不恢复
`.trellis/.developer` 或 `.trellis/workspace/**`，也不要求 `init_developer.py`。Official
Trellis 仍可独立创建和使用 identity/workspace journal；Guru 不删除已有数据，source/target
中 existing identity bytes 在 workspace transaction 前后保持不变。
A/B merge fixture 从同一 clean base 分别走 production recorder/executor/checker 与
task-local archive/commit，再验证 A -> B、B -> A 两个本地 merge 顺序无 Guru metadata
conflict；不创建远程 PR或并发进程。

`no_task` 下的 current-checkout direct edit 由 `guru-select-workflow-mode:task_free`
唯一承接。它只覆盖当前 checkout 的明确限定编辑，保留无关 dirty/untracked 文件，不授权
task/worktree/branch、commit、push、PR、merge、tag、release、installation 或 cleanup。

Branch Review Gate、exceptional recovery 与 publish helper 是内部子命令。routine
dispatch/wait/review 不调用 recovery recorder：

```bash
.trellis/guru-team/scripts/bash/record-agent-recovery.sh --json \
  --task ".trellis/tasks/<task>" \
  --event unfinished \
  --logical-role "实现代理" \
  --agent-id "<unfinished-agent-id>" \
  --reason "agent 已明确未完成" \
  --handoff-summary "已完成范围、剩余工作与 blocker"
.trellis/guru-team/scripts/bash/record-agent-recovery.sh --json \
  --task ".trellis/tasks/<task>" \
  --event replacement \
  --logical-role "实现代理" \
  --agent-id "<replacement-agent-id>" \
  --predecessor-event-id "<unfinished-event-id>" \
  --reason "replacement 接手未完成工作" \
  --handoff-summary "接续范围、剩余工作与 blocker"
.trellis/guru-team/scripts/bash/check-agent-recovery.sh --json --task ".trellis/tasks/<task>"
.trellis/guru-team/scripts/bash/check-commit-messages.sh --json --task ".trellis/tasks/<task>"
.trellis/guru-team/scripts/bash/format-merge-commit.sh --json --task ".trellis/tasks/<task>" --pull-request "<pr-number>" --summary "中文 PR 摘要"
.trellis/guru-team/scripts/bash/check-review-gate.sh --json
```

Closeout 不属于这组可手动调用的 recorder/validator 命令。显式 canonical
`guru-finish-work` entry 必须按 live workflow 进入 publication owner 和 active
finalizer；只有 finalizer 的 checked private engine 可以执行 finish helper。

Exceptional sub-agent recovery is activated only after an agent explicitly
returns unfinished and a replacement must inherit the work. The main session
records one minimal `unfinished`/`replacement` chain in ignored
`.trellis/.runtime/guru-team/agent-recovery/<task-key>.json`; routine assignment,
wait windows, progress, status requests, review rounds, and successful completion
do not create artifacts. Mapped stale/re-entry/reprepare routes remain inside the
AI workflow and never become a generic user confirmation prompt.

用户日常可以直接描述任务、贴 issue URL，或说“处理 issue #123”。AI 依赖
Trellis 自动注入的 startup context、workflow-state、hook breadcrumb 或 skill
matcher 判断是否进入 Guru Team issue intake 和 worktree preflight。

用户可以直接描述任务、贴 issue URL，或使用官方 Trellis 提供的
`trellis-start` / `trellis-continue` 入口；这些 upstream-owned 文件不由 Guru preset
覆盖。显式收尾使用 Guru-owned `guru-finish-work`：Codex、Claude、Cursor 分别是同名
prompt、`/guru:finish-work`、`/guru-finish-work`。三个 launcher 都只加载 live
`.trellis/workflow.md` 和 active public graph，不读取 package-private runtime/artifact，
不复制任何 step-local 合同。

Planning start gate 和 Phase 2 check gate 都需要 current task facts 与 owner-private
短生命周期 evidence。进入实现前主会话在三份 planning artifact 与 `Docs SSOT Plan`
就绪后 mandatory invoke `guru-approve-task-plan`。该 Skill 负责全部 entry precondition、
审查、必要 revision/clarification、仅服务真实选择或下一项副作用的当前对话交互、3.0
recorder/checker 和四出口；checked `approved` 自动进入 `phase-1-task-activation`，不增加
routine user stop。Phase 0 route DTO、非 3.0 planning input、缺失/过期/non-pass wording、
真实 planning/authority 语义漂移或 exit/Gate/consumer 不一致均 fail closed；owner 只接受
重新检查过的 current invocation。`task.py start` 只是状态写入，
不代表规划已审查。
阶段停止点和阶段完成回复先运行
`resolve-human-artifacts.sh --json --task <task-path>`，只展示实际存在的 `prd.md`、
`design.md` 与 `implement.md` 链接；不要求固定表格，JSON gate/evidence、private
checkpoint 与 PR payload 不进入默认 human artifact 展示。
commit 前先由 unchanged official `trellis-check` 收集实际 terminal evidence，再
mandatory invoke active semantic Skill `guru-check-task`。该 Skill 先做 scope
qualification，再做 current-scope severity、complete adequacy、Docs SSOT review、
finding/full-rerun loop 与最终 AI Gate；它独占 closed
`guru-phase2-check-4.0` 的唯一 ignored-runtime `phase2-check.json` 和 `passed` /
`implementation_required` / `planning_stale` / `blocked` 四出口。
`record-phase2-check.sh` 与 `check-phase2-check.sh` 只处理 AI-authored result 的
确定性 closed schema、`phase2_capture_commit`、`reviewed_content_sha256`、当前
dirty-path coverage、finding/scope linkage 和 route facts；reviewed-content identity
只由 `guru-check-task` public wrapper 内的 checker 在 DTO 投影前重算，不是授权、semantic approval、public handoff 或
全链 authority。几个验证命令、worker 输出或脚本通过不等于 semantic pass。
`phase2-check.json` 是 commit 前的 owner-private 短生命周期 checkpoint，不是 Trellis
原生步骤本身，也不是脚本替代 AI check 的入口。`passed` 只向 Task Commit 投影
`task_ref + phase2_commit_anchor`；public wrapper 在 DTO schema 校验成功后删除自己的 checkpoint。
Task Commit 和 Branch Review 只消费 DTO 与 live Git，不读取、删除或重开 Phase 2 私有状态。

Schema 4.0 只保留 current commit anchor、reviewed-content identity、reviewed paths、实际
validation、Docs SSOT、九个 adequacy 维度、finding lifecycle 与 typed route。Routine
assignment、handoff、liveness、raw worker payload、review round 与 per-file/artifact digest
bundle 不持久化；checker 只验证直接 consumer 所需的结构、freshness、coverage、linkage
与 closed exit union。

Phase 2 必须消费 planning 阶段的 `Docs SSOT Plan`。实现代理只返回最小 terminal result：
material changed behavior/paths、验证结果，以及确有必要的 Docs SSOT outcome 或 bounded follow-up；
不得重写 planning、生成 next-owner checklist 或创建独立 handoff artifact。`guru-check-task`
由 approved plan、task artifacts、implementation terminal result、embedded evidence、live diff 与测试事实
重建完整判断，并按同一策略复核 durable docs、
task artifacts、code/schema/config/deploy/test 和验证/测试覆盖是否一致；`delta_first` 必须在最终
Phase 2 check 前完成 durable docs merge，`ssot_first` 必须以修订后的 durable docs 为主要输入。
如果实现发现长期合同变化超出 plan，必须先更新 planning artifacts 和 `Docs SSOT Plan`，必要时重新
planning approval，再重新 Phase 2 check。

Codex 项目默认使用 `codex.dispatch_mode: sub-agent`，由 main session 调度
`trellis-implement` / `trellis-check`。默认 sub-agent mode 下，main session 只负责
规划、调度、等待、必要时处理异常恢复/替换、记录 Gate evidence、commit 和运行 recorder/validator；实现必须由
`trellis-implement` / channel `implement` 完成并输出最小 terminal result，Phase 2 check 必须由
`trellis-check` / channel `check` 完成并输出可记录到 `phase2-check.json` 的 evidence，
commit 后 Branch Review 必须由独立 review sub-agent 审查完整 `origin/<base>...HEAD`
diff 并向 semantic owner 返回最小 terminal findings/evidence；不创建 per-round report
或 rollup。main session 自己实现、自检、自审或脚本校验通过都不能替代这些边界；
缺少实际 evidence 时 fail closed。因为 Codex sub-agent 使用
`fork_turns="none"` 隔离，dispatch prompt 必须以 `Active task: <task path>` 开头；
sub-agent 若没有拿到该行，则运行 `task.py current --source` 解析当前 task。只有显式配置
`codex.dispatch_mode: inline` 时，Codex 才降级为 main session 直接实现和检查。
Guru Team preset 安装项目级 agent 定义：Codex 使用中文 `description` 表达 UI 语义，
但 `nickname_candidates` 保持 ASCII，因为当前 Codex 会拒绝中文 nickname 候选并忽略
agent 文件；Cursor / Claude / channel runtime agent 使用中文 description 和标题。这些文件中的
`trellis-implement` / `trellis-check` / `trellis-research` 以及 channel runtime 的
`implement` / `check` 是稳定调度标识，不能为了中文展示而改名。

Routine sub-agent assignment、wait、progress、review round 与 completion 不写 task
artifact。只有 agent 明确 unfinished 且 replacement 必须接手时，main session 才写 ignored
agent-recovery checkpoint；普通 mapped exit、stale/re-entry/reprepare 由 AI workflow 自动
承接，不向用户暴露为“确认继续”。

Active `guru-review-branch` 是唯一的 Phase 3.5 semantic owner。Global workflow 与
平台 `trellis-continue` entry 只用 `profile`、`mode`、`task_ref`、`base_ref`、
`branch_review_commit`、`review_intent` 六字段 public input mandatory invoke 该 package，
并消费 `passed`、`implementation_required`、
`scope_confirmation_required`、`blocked` 四个 typed exits。Reviewer lifecycle、
finding qualification、Docs SSOT Gate、recovery checkpoint、private artifacts 与 re-entry
规则均由 package 独占，入口不得复制。

`review-branch.sh` 与 `check-review-gate.sh` 只是 package-owned deterministic
recorder/validator implementation details，在 AI Review Gate 后记录和校验 objective
facts；它们不能替代 semantic review，也不能决定 scope、finding、充分性、pass 或 route。
Phase 2 的官方 `trellis-check` sub-agent 仍只提供 commit 前 raw evidence，active
`guru-check-task` 独占 Phase 2 semantic check；Phase 3.5 的全部判断由
`guru-review-branch` 独占。

`trellis-continue` 不得 push 分支、创建 PR 或调用 `finish-work`，也不得提交
`review-gate.json` 等 Trellis metadata。
PR 发布只从显式 canonical `guru-finish-work` 薄入口开始：该入口先按 live workflow 调用
`guru-review-task-publication`，仅从 `ready` 进入 `guru-finalize-task`。Finalizer 的私有
preview 生成 canonical `closeout_plan` 与 local digest；该 digest 只绑定 deterministic executor。
语义 Gate 在当前对话完成真实副作用确认后才执行
reviewed content push、按需 marketplace verification、draft PR、final archive
projection、单次 archive metadata commit/push、三方 HEAD 对齐与 draft-to-ready。裸
`finish-work.sh` 默认拒绝普通直接调用；中断由同一 finalizer 自动消费 recovery
route，不暴露内部 flag 或要求用户选择下一条命令。
Prepare 使用已安装的官方 config parser，只支持缺失或空 `hooks.after_archive`；
非空、歧义、不可读、含 NUL 或 symlink 配置在副作用前拒绝，且不会执行 hook。
official move 前重新核对实时 archive 月份、空 index、精确 untracked 集合、regular-file/mode
与 tracked source blob。Closeout schema 3.0 plan 在 active task 中跨月时，同一 entry 重新
dry-run 得到新 digest，并只替换 still-untracked current plan；不创建 plan/readiness/evidence
commit、不 rewrite history 或迁移目录。唯一 legacy schema 2.0 plan 只有在 current
Publication 4.0 DTO 的 task/commit/title/body digest 与 protected facts 完全匹配时才
normalize 为 schema 3.0，并记录 predecessor digest；其它 non-current shape fail closed。
共享 prepare 从 archive root 到 month/final destination 逐层 `lstat` 既有组件，不读取或
跟随 symlink target；任何 symlink（含 dangling、repo 内 target）都拒绝，且 final locator
必须不存在。official move 前重复同一检查，阻止 prepare-to-move 漂移。缺失的
`task.json.children` 视为
空 list、其余值严格校验为 `list[str]`。按官方 active task exact/suffix lookup，只有会被
archive 改写的 active child 阻塞；已归档 child 不阻塞 parent closeout。
Gate 后到 finish-work/archive 只允许 Trellis metadata tail；durable docs、`.trellis/spec/`、
source、tests、schema、config、scripts、preset、overlay、CI/CD、deployment、migration、
Makefile 等 non-metadata drift 必须回到 Phase 2/3。finish-work dry-run 和正式 finish 都不做
首次 Docs SSOT merge。

Finalizer 的 private preview 是无副作用 readiness step：它校验 gate、dirty state、
Publication ready 4.0 DTO 的 exact title/body 与 live facts，
并输出 canonical plan、digest、future archive mapping、exact transaction paths 与 transitions，
不移动或写入文件、不创建 commit、不 push、不创建 PR，且没有 journal/workspace 计划。
dry-run 回复使用 active task 的 `Markdown 产物 review 表`；正式 archive 后，AI 必须
重新运行 resolver 解析 `.trellis/tasks/archive/YYYY-MM/<task>/...` 路径，并在最终回复输出
archive-path 表，不能复用 archive 前的 active task 链接。

PR body 是给 GitHub reviewer 看的发布材料，不是 Trellis task artifact。Publication
owner 在同一 semantic loop 内生成并审查 body readiness，确认 `变更摘要` 具体、
`影响范围` 明确、`验证结果` 是实际命令与结果、`Review Gate` 写明
`branch_review_commit` / diff range / content identity / findings 状态、`Issue 关闭范围`
只关闭 ledger 中的 `close_issues`，并且
`安全说明` / 部署影响与本次 diff 相符。Body 还必须包含 `Docs SSOT` / `文档同步`
section，说明策略、durable docs 更新或 no-update 理由、已 merge 的 task delta、仅保留
task history 的内容，以及 follow-up / 当前 PR limitation。Publication ready 4.0 DTO
精确输出 `exit_id/task_ref/branch_review_commit/pr_title/pr_body`；Finalizer input 4.0
直接消费 payload，不从 task-local 文件、private checkpoint 或 runtime source 补取。

Guru Team 不调用 `.trellis/scripts/add_session.py`，不读写 `.trellis/workspace/**`。
shared `trellis-start` 只读取 phase/packages/current-task/Git facts，Codex/Cursor
SessionStart overlay 不导入或调用 journal helper，也不打开、枚举、读取或输出 journal。
finish-work 先绑定唯一 draft PR，再从 reviewed PR payload 与 live facts 在 active task 中
一次构建 schema 2 `finish-summary.json`，包含 canonical URL 与唯一 `PR #<number>` ref。
recorder 对 raw base-to-HEAD paths 排序去重后过滤 workspace/runtime
受保护前缀，过滤发生时追加一条不含 path、basename 或数量的固定 contract fact；未发生过滤时
不追加。initial diff、initial untracked 或 final/recovery diff 失败时两个 path 数组都为空，
只追加固定 snapshot-unavailable fact，并重新派生 retrieval text。schema/validator 对所有 path 字段继续拒绝受保护前缀。final summary 在 active task 中严格
校验一次，并只随 archive metadata transaction 提交。archive 后不再校验、回写 artifact 或新增
metadata tail。同一入口在 archive 前根据 plan/readiness、active locator 与 evidence facts 恢复。
official move 后、精确 archive commit 尚未形成时，仍校验 archived working-tree 布局、
dirty/staged path、blob continuity 与官方 `task.json` delta。Closeout schema 3.0 在 move 后先按
current retained set 幂等裁剪无长期 consumer 的中间文件，再校验 compact layout；进程在 move
与裁剪之间中断时，同一 recovery path 会先完成裁剪再提交。Current core 固定为 7 个 durable
文件，只有适用 marketplace gate 时再保留 `marketplace-verification.json`，总数最多 8。
Publication readiness 与 Finalizer gate 为 ignored runtime，不进入 archive。intake/context
snapshot、assignment/liveness、commit plan、raw review round 与 private checkpoints 不复制进
长期 archive tree。无效 plan、commit 缺失或不匹配继续 fail closed。
一旦当前 `HEAD` 已是精确 archive commit，普通 archived task 与 plan-only recovery 都从该
commit blob 读取 plan；committed plan blob 与 Git parent/path/tree/blob lineage 只作为
deterministic recovery inputs，本地 archived 文件缺失、篡改及其 dirty state 不阻塞 exact push、remote PR title/body
digest、三方 HEAD 或 draft-to-ready。plan-only archived directory 只由 `guru-finish-work` 恢复入口
解析，普通 task 命令仍要求 `task.json`。real-PR final summary 的 deterministic bytes/digest 纳入
pre-move、incomplete recovery 与 exact recovery continuity：前两者用已绑定 remote PR 重建 expected
bytes，exact recovery 只从 immutable archive commit 的 `finish-summary.json` blob 恢复原 PR number/URL
并重建校验，不读取 working-tree summary，也不调用通用 summary artifact validator。原 PR 缺失、
closed 或被同 repo/head/base 的新 PR 替代时 fail closed；其它 archived artifacts 不重新打开。
final projection、incomplete 与 exact recovery 共用一个 strict PR URL parser。GitHub
owner/repository identity 大小写不敏感，canonical summary URL 保留 remote 返回的合法 casing
（例如 `microsoft/PowerToys`）；错误 repo、transport、number、额外 path、query/fragment 仍被拒绝。
plan-only 恢复从当前 commit blob 读取 committed plan，并在 GitHub/fast-path 前用专用 fail-closed
boundary 校验 Git toplevel、配置/effective repo、当前head branch、base ref、current HEAD transaction、
expected digest、task identity 和 active/archive locator；它不是缺失 context 时的无条件跳过。普通
task discovery 与其它命令仍要求 `task.json`；worktree mode 从 current task、runtime mapping
与 Git worktree facts 解析边界。
raw locator 在普通 resolver/`resolve()` 前验证，只允许 basename、原 active locator 或精确 archive
locator；path-like 输入先从 repo root 到 final task dir 逐组件 `lstat`。basename 输入在普通
resolver 前按其候选顺序预检 `<repo>/<basename>`、active task candidate、archive root 和 archive
candidates；每个 direct/archive candidate 都先保留 `symlink_component` 证据，再用普通 resolver
完全相同的 follow-symlink `directory + task.json` 谓词判断，matching alias fail closed，unmatched
alias 继续下一候选。
预检统一拒绝 repo 内外、relative/absolute、ancestor/final、多层、dangling、loop symlink，再优先调用
普通 resolver，保留显式 `task.json`、active task 和普通 archived `task.json` 的顺序；仅 ordinary
not-found 才进入 plan-only fallback。精确 archive locator 只尝试该候选，basename/原 active locator
fallback 必须
唯一命中一个 archive 月份，多候选 fail closed。plan-only resolved target 仍须等于 plan canonical
archive locator；仅固定 Darwin `/var -> /private/var` 系统映射可重锚，不接受任意
`samefile`/用户 alias。

Publication owner 在 ignored runtime 记录 schema 4.0 `pr-readiness.json`，其 public
`ready` DTO 携带 task、`branch_review_commit` 与 exact `pr_title/pr_body`；Publication
wrapper 校验 DTO 后删除自己的 checkpoint，Finalizer 不读取、删除或提交该 owner
checkpoint。Closeout plan schema 3.0 直接绑定 title/body，且不创建独立 evidence commit。
Finalizer 从 reviewed body 的 `变更摘要` 与 live Git/task/ledger/PR facts 一次生成 schema 2
`finish-summary.json`；Discovery 仍可只读检索历史 schema 1 archive。
脚本只做客观结构校验、低信息量短语阻塞、close/ref 语义校验和 reviewed source 门禁；
不能用脚本生成的空泛摘要或 `generated` body 替代 AI 发布判断。


## Push 后远端 Marketplace 门禁

`guru-verify-extension-installation` 是 extension installation 唯一 semantic owner。
Workflow 或 task-bearing standalone 只持久化 task-local
`marketplace-verification.json`；taskless standalone 为 session-only。Runtime command
固定为 `execute-extension-verification`、`record-extension-verification`、
`check-extension-verification`、`invoke-extension-verification`，只执行、记录、
校验和按 actual exit 序列化，不判断语义通过。

Public `repo_ref` 始终表示业务 target。Workflow 与 task-bearing standalone
从 target checkout 的 `.trellis/guru-team/extension.json` 解析 extension source，
且 task-bearing source 必须为 `tree_state=clean`，否则在 source ref resolution
与 clone 前阻断。Runtime 分别校验 target checkout 与 extension-source checkout。Target reviewed-content
不得从 source 计算；installer、canonical assets、ownership 与 source sidecars
不得从 target 读取。Annotated source tag 选择 peeled commit 并与 manifest
`source.commit` 比较；branch/lightweight tag 使用 direct commit。Git worktree preset
apply 把完整 apply-time commit OID 同时记录为 immutable `source.ref` 与
`source.commit`；runtime 直接 fetch 该 OID，并要求 fetched commit 和 source checkout
HEAD 精确一致，target branch 后续前进不改变 source identity。Taskless
standalone 只有在明确验证 source repo 且 manifest 缺失时才允许 fallback，malformed
manifest 与 credential-bearing/non-canonical GitHub locator 均在 clone 前 fail closed。
Private schema 3.0 记录这两套 identity；四个 public exits/consumer DTO 保持不变。

Remote matrix 必须绑定 pushed ref/HEAD，覆盖 new init、preview/switch、preset
apply/reapply、`trellis update`、ownership/sidecar、contract discovery、platform
equality、README command 与 redaction。Workflow-required applicability conflict 会
`blocked`，不能 silently `not_required`。Production real-wrapper eval 与 pushed-remote
clean install 分别记录，任一不能替代另一份验收。

## Skill 行为评测

安装完整 Guru Team preset 后，可用 `discover-skill-evals` 发现 Interface 1.3
package 的 `evals/evals.json`，并用 `run-skill-evals` 经
`shared|codex|claude|cursor` adapter 实际执行 public wrapper。Schema id 是
`guru-team-skill-evals-1.0`，status 闭集为
`passed|evaluation_failed|execution_error|unsupported`。外部 semantic grading
与 human feedback 独立，run evidence 只能位于 repo 外。当前 production Skills
中的十四个 packages 已维护 canonical corpora 并覆盖全部 54 exits/profile；六个 Intake
packages 的 23-exit closure 仍独立验证。四个 descriptor 分别绑定
可执行 `shared.sh|codex.sh|claude.sh|cursor.sh`；shared 解析 preset-managed
`guru-team-shared-eval`，其余 adapter 从 `PATH` 解析 `codex|claude|cursor-agent` 并组装平台
专用非交互 argv。Runner 在 native
execution 外读取 canonical corpus；native 只加载 repo/package 外 public-only Skill projection、
prompt/staged files，不接收 canonical package/corpus/private runtime locator。Native CLI 必须通过 repo 外 trace helper
读取 `SKILL.md` 并调用 exact wrapper；`guru-team-skill-eval-native-trace-1.0` receipt 与
request、projection、Skill/wrapper digest、wrapper argv/return code 和返回 DTO 完整绑定后才产生 trace invariant。合法 DTO
缺少 receipt 为 `execution_error`。Native argv、output、context 与 receipt locator 收集到
repo 外 transcript；四平台 projection 中 eval/private runtime raw read 必须真实失败。缺失
native command 为 `unsupported`，不依赖隐藏环境变量替代 adapter。
Semantic case 必须引用 repo-local checker-passed owner result；actual exit 选择 output schema
后才比较 expected exit。Codex 使用 trusted Git root，Claude 使用 safe non-interactive 协议，
Cursor 未登录直接返回 `unsupported`。
Finalizer closeout plan 同时绑定 `reviewed_content_head` 与
`publication_head`。当 reviewed HEAD 已 push、PR/archive 尚未开始且 installed
manifest 仅缺 clean provenance 时，workflow 自动消费 `reprepare_required`：从
detached clean checkout 运行 canonical preset apply，提交一次 manifest-only tail，
废弃旧 private plan/gate/request，并由 executor 输出 unchanged reviewed HEAD 与新
publication HEAD；下一次 preview 直接验证这两个 identity 和单 tail 合同，不读取已删除
plan，然后继续 exact-ref verification。其它 diff、已有 PR、archive 已开始或
non-fast-forward 继续 fail closed。
