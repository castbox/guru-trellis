# Guru Team Trellis Workflow

本目录维护 Guru 团队可复用的 Trellis workflow。

这个 workflow 的 marketplace id 固定为通用的 `guru-team`。它承载 GitHub issue
intake、Git base branch/worktree preflight、业务项目中文文档默认规则、Issue
Scope Ledger、Middle-platform Knowledge Gate、Repo Docs SSOT reconciliation、
Branch Review Gate，以及 finish-work 成功后的自动 publish PR 规则。

Guru Team extension 版本不等于官方 Trellis CLI 版本，也不等于 `trellis/index.json`
里的 marketplace index schema version。canonical extension version 和目标官方
Trellis CLI 版本位于 `trellis/guru-team-extension.json`；preset installer 会把当前安装版本和 source
provenance 写入目标仓库的 `.trellis/guru-team/extension.json`，并通过
`check-env --json` / `version.sh --json` 暴露给用户和 AI 排障流程。

## Marketplace 安装

```bash
trellis init -y --codex --cursor \
  --workflow guru-team \
  --workflow-source gh:castbox/guru-trellis/trellis#v0.6.5-guru.2
```

`-y` 是团队默认安装路径的一部分，用于跳过交互式 spec template picker。自动验收、
throwaway 安装验证和 README 默认命令都必须使用非交互形式；只有用户明确想手动选择
spec template 时，才去掉 `-y` 或改用官方支持的 `--template <name>`。

稳定安装 source 使用 repo release tag `#v0.6.5-guru.2`，并要求官方 Trellis CLI 安装到
`0.6.5`。维护者刻意跟随最新 `main` / canary 时可以去掉 `#ref` 或改用其它 branch/tag ref，
但应在验证和排障报告中说明 source 是否为 mutable ref，以及是否仍以官方 Trellis `0.6.5`
为目标基线。Guru Team release tag 使用 repo 级 `v<official-trellis-version>-guru.<revision>`，
并与该 tag 所指提交中的 `trellis/guru-team-extension.json.version` 对应。当前已发布
stable 是 `.2`；本分支 canonical `.20` 在 merge/tag/远端验证完成前不是 stable source。

已有 Trellis 项目切换 active workflow：

```bash
trellis workflow \
  --marketplace gh:castbox/guru-trellis/trellis#v0.6.5-guru.2 \
  --template guru-team
```

只有在需要生成 `.trellis/workflow.md.new` 做人工 review、且不切换 active
workflow 时，才使用 `--create-new`。

## Companion Assets

Workflow marketplace 只安装 global `.trellis/workflow.md`，不安装 external
workflow skills。公共 skill 的唯一源头是 `trellis/skills/guru-team/`；global
workflow 只通过 `guru-skill-invoke` / `guru-skill-exit` marker 定义 mandatory
调用与唯一出口 consumer/stop，不复制 step-local skill 正文。完整运行时资产
由 Guru Team preset 分发。Production registry 保留
`guru-create-work-commit` reserved tombstone，并激活 `guru-sync-base`、
`guru-discover-change-context`、`guru-clarify-requirements`、
`guru-review-contract-wording`、`guru-review-change-request` 与
`guru-create-task-workspace`、`guru-create-task-commit`。Workflow 不得为
reserved/planned id 伪造 invocation route。当前 canonical
extension version 是待发布的 `0.6.5-guru.20`，已发布 stable source 仍是
`v0.6.5-guru.2`。

Interface 1.2 保持冻结的 legacy 语义；独立 interface 1.3 是新建或实质修改 public
I/O 的 minimal handoff target。Registry 1.1 的 active row exact 声明
`interface_schema_id` 与 `io_contract_state`，合法组合只有 `1.2+legacy` 和
`1.3+minimal_handoff`。`stage0-minimal-handoff-v1` 已原子迁移六个 Stage 0 packages
与 24 exits；`guru-approve-task-plan`、`guru-check-task`、
`guru-create-task-commit` 仍由 #146 保持 legacy。两版均保留 `workflow` / `standalone` mode id 和必填
`judgment_mode`，并以
`routing=global_workflow|direct_discovery` 区分 mandatory route 与平台直接发现。
`semantic` profile 固定五阶段，`deterministic` profile 固定三阶段；任何需要 scope、
sufficiency、finding、revision、用户选择或 route intent 判断的 Skill 不得降级。
`standalone` 仍依赖完整 Guru Team preset 与 compatible extension runtime，不是单目录
self-contained/portable 分发。Package wrapper 只能经 shared `run-skill-command`
dispatcher 调用 manifest 已发布的 companion command；runtime/API/inventory/drift 不匹配
必须在业务副作用前 fail closed，并提示完整 preset 安装或升级与 sidecar 处理步骤。

Active package 的 discovery contract 要求 `SKILL.md` 只有一段闭合
frontmatter，`name` 等于 stable id/registry/interface，`description` 非空且与
interface 一致；`tests[]` 只引用 package-local `tests/<file>` regular file。
Source validator 对 missing/drifted frontmatter 与 missing/outside/symlink test
evidence fail closed。

Interface 1.3 的 closed `public_contracts` 分开声明 caller-owned input、exact
package invocation、per-exit output、consumer-owned Skill/workflow/stop input、thin
projection 与 runtime/gate private artifact。每个 output field 都必须有直接 consumer
use；Skill consumer 只能引用 active registry exact canonical path 与相同 target id 的
`skill_input`；非 direct projection 与 direct 到 scalar CLI 必须静态证明 required source
与映射/normalizer 后的全域兼容，不能只验证 example；public/private
schema id/path 分别互斥。Wrapper 完整 bytes 必须匹配 dispatcher-only template。
Scalar argument 必须显式声明 boolean `required`；`guru-sync-base.base_branch` 为 optional，
省略时进入同一 owner resolver。Active-task clear 的 null disposition 只在 scope-change
profile 投影为 `retained`。
1.3 `pattern` 只接受 durable spec 的 printable-ASCII portable grammar，并按 ECMA-262
Unicode-mode search 语义执行；Python-only regex、Unicode source pattern 和未声明
shorthand 在 source/installed validation 中 fail closed。稳定的 public discovery
command 是：

```bash
.trellis/guru-team/scripts/bash/discover-skill-contract.sh \
  --root . --mode installed --skill guru-sync-base --json
```

Legacy package 只返回 version/migration identity；minimal package 返回完整 locator index。
Source validation 会真正执行 representative fixture wrapper 并按 exit schema 复验单一
stdout DTO。Fixture 不进入 production registry/manifest/platform roots/mandatory route。

Trellis workflow marketplace 只负责安装或切换 `.trellis/workflow.md`。
companion scripts、配置、schema 和团队自有入口 overlay 需要通过 preset installer
写入目标仓库：

```bash
git clone --depth 1 --branch v0.6.5-guru.2 \
  https://github.com/castbox/guru-trellis.git /path/to/guru-trellis
/path/to/guru-trellis/trellis/presets/guru-team/scripts/bash/apply.sh \
  --repo /path/to/project
```

installer 会写入 `.trellis/guru-team/`，并可安装 `.agents/skills`、
`.claude/commands`、`.cursor/commands` 下的 Guru Team overlay。它不会修改 Trellis
上游脚本、npm 全局包、`node_modules` 或 `.trellis/scripts/task.py`。

installer 还会写入 `.trellis/guru-team/extension.json`，记录 Guru Team extension
version、target Trellis CLI、workflow template id、source repo/ref/commit、source tree state、
selected platforms 和安装时间。这个文件是安装事实记录，不是用户配置。

installer 幂等：同内容跳过，缺失文件写入，Guru-managed companion assets 会升级 active
文件并把旧版保存为 `.bak`，已有 `.trellis/guru-team/config.yml` 不覆盖，识别为上游
Trellis 生成入口时替换为 Guru Team overlay；未知本地改动写 `.new`，不静默覆盖。

## Workflow Authoring Ownership

Workflow phase、mandatory Skill routing、typed exit consumer 和 semantic gate 的
canonical authoring 面是 Markdown workflow 与 `guru-*` closed-loop package。不得通过新增
Trellis upstream namespace overlay、修改 hook/script 判断语义或扩张 broad managed-path claim
实现新的流程行为。

当前 preset 的 43 条 overlay 是 issue #128 固定的 `transitional_legacy/active` 集合，
inventory 位于 `trellis/presets/guru-team/ownership/upstream-ownership.json`，每条都绑定
base payload SHA-256、replacement owners、blocking issues 与 #132 removal owner。Trellis
`0.6.5` clean init 会生成其中 37 条；6 条历史 Codex prompt/skill path 不再生成，但在
#132 physical removal 前仍保留审计与安装事实。

维护者在 preset mutation、dogfood drift、throwaway initial/update/reapply checkpoint 前运行：

```bash
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
```

该 source-only validator 不进入 `.trellis/workflow.md`、mandatory Skill routing、platform
entry 或业务 task runtime。`trellis update` 的 `.trellis/.template-hashes.json` 与
overwrite/keep/`.new` 语义仍归 upstream；preset 的 `.new`/`.bak` 仍需维护者逐个处理，
它们不代表 semantic ownership approval。

`config-template.yml` 显式包含 `middle_platform_knowledge.mode: optional_warn`。
已有目标仓库的 `.trellis/guru-team/config.yml` 不会为了补这个 key 被覆盖；如果 key
缺失，workflow 仍按 backward-compatible 默认 `optional_warn` 执行。`required` 只作
opt-in，`off` 只作 opt-out。

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
query-only compatibility 调用，不是 workflow hop。Standalone mode 可由所选平台直接发现
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
解释命名 load-bearing decision 时才进入。Pre-task 只输出 stdout snapshot；task 创建后
只将 expected digest 匹配的相同 snapshot 写入 direct active task-local
`context-discovery.json`，并在写后重读 exact bytes、snapshot identity 与 live freshness；
archived/completed/non-active task 必须拒绝。Recorder/checker 执行 published closed Draft
2020-12 schema；base evidence 嵌入完整 validator-passed sync result并绑定 post-sync
digest、selected remote refs 与严格 GitHub repo identity。Pre-task/standalone 绑定 decision
checkout branch；task mode 只允许相同 HEAD 上进入 `task.json.branch` feature worktree，并
继续校验完整 provenance、base refs、active task locator/status 与 task-local-only dirty paths。Git status
failure 不得冒充 clean，base stale 在 live issue/draft、reviewed blob 与 archive preview 前
短路。Draft-created-issue binding live 校验原 reviewed body；caller-authored `refresh_base`
必须与 stable live stale codes 一致，`context_ready` 对同一 stale 拒绝。Archive reader
以普通 file/read/JSON/index-shape failure 形成 portable invalid evidence。
Deep-read locator 按 selected task artifact、canonical GitHub issue/PR 与 exact Git object/ref
三类闭合校验。Closed schema 与结构化 locator 不保存 raw source payload，也不做
跨字段扫描；不写 workspace/runtime/repo cache。

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
query/snapshot digests、reason 与 detection time，然后要求整步 re-entry；只消费当前 payload
与 expected snapshot identity，不重建 ancestry。Task-local recorder 写前/写后与 checker 还使用 `git check-ignore
--quiet --no-index -- <target>` 验证 artifact 未命中 repo ignore、`.git/info/exclude` 或
`core.excludesFile`；pre-task stdout-only 不执行该 gate。Base stale 随后只匹配
caller-authored refresh codes 后返回。`change_input` 十组 clue arrays 至少一组非空，issue binding/canonical query 不得
替代。Portable locator 只按 source-specific closed structure 验证，不扫描整份 payload。

Schema 是 `guru-context-discovery-1.0`；managed commands 是
`preview-change-context-history`、`record-context-discovery` 和
`check-context-discovery`。Exits 是 `context_ready` -> active
`guru-clarify-requirements`、`refresh_base` -> `guru-sync-base`、`blocked` ->
`change-context-blocked`；source/installed validator 同时解析 active Skill consumer 及唯一
workflow/stop target markers。

## Phase 0 Requirements Clarification

`guru-discover-change-context:context_ready` mandatory invoke semantic
`guru-clarify-requirements`。Initial issue/draft、active-task scope change 与 standalone review
共享相同 preconditions、AI Gate、confirmation 与 freshness。Repository-answerable questions
必须先由 current Docs/code/tests/history/GitHub/Git evidence 回答或记录不可回答证据，
`answered`至少有一个checked ref。之后每轮只问一个最高价值问题，question id必须来自opened/current-open，
`partial`不得关闭 question，reducer固定为`open_questions = opened - closed`。

AI 拥有 scope/action/confirmation/pass/block/route 判断。Recorder 派生 proposal/action/
payload/content/result digest；checker 重算 schema/digest并只读验证 live source/context/task
binding。Package 没有 GitHub mutation executor；comment/body 写入仅在 AI 复核 live preimage
并取得 exact action/proposal confirmation 后使用现有 connector 或审查过的 `gh`，写后必须
重读；confirmed payload、payload digest、mutation result与live content必须一致。成功 mutation
返回 `refresh_context`，不直接 `clear`。

Pre-task/standalone 结果 stdout-only且无专用 artifact。Active-task current inclusion 绑定
GitHub-visible authority、`issue-scope-ledger.json`、`prd.md`/`design.md`/`implement.md`、stale
planning/Phase-2/Branch-Review identities与三个 re-entry owners。Schema 是
`guru-requirements-clarification-2.0`，commands 是
`record-requirements-clarification` / `check-requirements-clarification`。Active-task Scope Change
Gate mandatory invoke同一Skill。Exits 为 `clear` -> caller-aware
`guru-requirements-clear-router`（initial/draft -> #114 wording，standalone -> caller，active ->
planning review或exact interrupted progression）、`needs_context` -> context discovery、`refresh_context` -> base sync、
`retarget_context` -> base sync 并对 selected open issue 完整重跑 Intake、
`new_task` -> staged #112 full intake route、`blocked` -> fail-closed stop。

2.0 以 target disposition、duplicate candidate decision、authority impact、
`select_existing_issue` / `reopen_issue` 和 `retarget_context` 替代无法兼容扩展的 1.0 artifact。
旧 artifact/caller fail closed 并从 `guru-sync-base` 重跑，不执行语义自动迁移。

Active-task `clear`/`new_task` 要求非空且全部属于七类 terminal decision 的 proposal set；
五类 scope classification 无论 origin 均要求 exact proposal 用户证据，并 exact 匹配当前
`issue-scope-ledger.json.scope_decisions[]` 的 structured trail，并绑定 live GitHub authority、
shared validator 完整校验的 `guru-planning-approval-2.0` planning approval/docs、review state、stale gates、interrupted target
与 re-entry owners。`mechanism_removed/replaced` 使用 optional origin/null confirmation，
不进入 trail/action mutation。GitHub authority mutation 后只能 `refresh_context`；context
时间覆盖 authority 后 task update 绑定同一 digest，不要求第二次 refresh。Active-task `new_task` 保留该 trail，仍只给 #112
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
与 mutation-result digests，并由 checker 绑定 exact confirmation、preimage、current reread
content/source update time。`planning_artifacts:pass` 写入 task-local
`contract-wording-review.json`，`record-planning-approval` 只消费该 current evidence 并记录
explicit post-planning confirmation。该 profile 还必须按 canonical contract 显式记录
`semantic_review.ai_review_gate.planning_checked_dimensions`；成功 exit 要求其 exact shape
全部为 true，deterministic runtime 只能验证，planning projection 只能逐项复制，均不得生成语义
结论。`content_changed` 要求对应 profile 完整重入；旧 active approval 若没有 #114 binding，
或绑定的 schema 1.0 wording evidence 缺少该 planning-only 字段，必须重新执行完整 AI wording
review、展示三文档并取得 fresh 规划确认，禁止手补布尔值。Archived artifact 不改写。

## Phase 1 Task Plan Approval

Phase 1 在 current `guru-review-contract-wording:planning_artifacts:pass` 后 mandatory
invoke active semantic Skill `guru-approve-task-plan`。Workflow 与 standalone mode 使用相同
九项 entry preconditions，并依赖完整 Guru Team preset、shared dispatcher 与 runtime。
Canonical package 是 planning adequacy、四类 provenance、implementation choice、unusual
proposal、AI Gate、dedicated proposal confirmation、post-planning confirmation 和 re-entry 的
唯一 owner；workflow 只声明 invoke 与 typed routing。

唯一 artifact 仍是 task-local `planning-approval.json`，新 schema id 为
`guru-planning-approval-2.0`。Runtime commands `record-planning-approval` /
`check-planning-approval` 只消费 AI-reviewed input 并重建/校验 deterministic facts、digests、
freshness 与 closed exit union，不生成 semantic pass 或 route。四个 exits 是：

- `approved` -> workflow target `phase-1-task-activation`；
- `revision_required` -> `guru-approve-task-plan`；
- `clarify_scope` -> `guru-clarify-requirements`；
- `blocked` -> stop `task-plan-approval-blocked`。

普通 `post-planning-approval` confirmation 不能代替
`dedicated-unusual-scenario` confirmation。`approved_scope_expansion` 的 proposal 必须由 runtime
从 current planning controlled locator 或 canonical unusual candidate 重算；专用 confirmation 与
current authority SHA-256 绑定同一 proposal digest，unusual candidate link 只投影已有的一次确认。
Active schema 1.2 artifact 必须完整重入并重录
v2，archive 不改写。Scope ledger 的 task identity 与 requirement authority 使用同一
issue-category projection。Task 仍为 planning 时复验 invocation base/HEAD/dirty snapshot；
activation 后的实现 HEAD/dirty 变化不单独使 plan stale，planning、authority、Docs SSOT 或
wording 内容变化必须完整重入。

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
Active `guru-create-task-workspace` 是唯一 mutation owner，并把同一 checker-passed bytes
持久化到 direct active task 的 tracked `issue-review.json`。

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
`guru-create-task-commit`。Skill 为每次提交生成独立 task-local plan，AI 负责 scope/
message/authorization review；candidate validator 复用同一 parser，exact executor 只
stage 计划路径并验证真实 commit。Candidate、stage 与 commit 边界拒绝非普通 Git
operation/sequencer state；gitlink snapshot 绑定 initialized、clean worktree HEAD，
executor 在 exact stage 前重验该 HEAD，并直接把 artifact OID 写入 mode `160000`
index entry，而不是让 `git add` 从可变 worktree 重新取值。普通 path 也只从
artifact SHA-256/mode/delete identity 构造 cache entry。Snapshot 将 rename 与 copy
分别记录为 `renamed_from` / `copied_from`；只有 rename source 继承 destination
的删除/exact-stage authority，copy source 只能在自身独立 classified 且 reviewed
时进入计划。Candidate self 只用 validated plan deterministic bytes。
真实 hook chain 与 commit 先在 isolated index/detached HEAD
完成，commit/worktree/candidate/operation/live-index preimage 全部通过后才 recoverable
publish branch/index/result。真实 `index.lock` 作为 sentinel 持有到 transaction 结束，
final index bytes 使用独立 temp 并在 sentinel 存在时发布；conditional advance 后立即
持有/复核 loose-ref guard。Ref/index/result 已是 transaction state 且 guards 仍持有时，
最终 candidate inode/content identity read 是线性化点：此前的 C 会使 ref/index rollback
且 C 被保留，此后的 C 是独立 later operation，immutable commit blob/result digest 仍是
`committed` authority。因此 review 后切换
submodule revision 会 fail closed，未审查 OID/bytes 也不能进入真实 index/commit。`committed`、`revision-required`、`blocked` 分别由
Branch Review/finding closure、skill re-entry、fail-closed stop 唯一消费；finding fix
必须先返回完整 Phase 2，并创建新 sequence。

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
第一跳是 mandatory `guru-sync-base`。只有 typed exit `synced` 才进入：

`guru-discover-change-context -> guru-clarify-requirements ->
guru-review-contract-wording -> guru-review-change-request ->
guru-create-task-workspace`。以下命令仅用于兼容查询，不是 active workflow hop：

```bash
.trellis/guru-team/scripts/bash/check-env.sh --json
.trellis/guru-team/scripts/bash/prepare-task.sh --json \
  --expected-resolution-sha256 <post-sync-resolution-sha256> \
  "<user request or issue URL>"
```

`prepare-task.sh --json` 只执行 query-only compatibility，不创建 GitHub
issue、worktree、branch、Trellis task，也不写 `.trellis/tasks/<task-slug>/task-start-context.json`。
它只在 stdout JSON 中输出 source/proposed issue、duplicate candidates、base branch、
branch name、workspace path、`create_task_command`、`naming_quality`、
`preflight.base_freshness` 和 `no task context/runtime write`。在 `gh auth status`、issue read
与 duplicate search 前，planner 必须通过 shared strict core 重解析和同步 selected base；
`fetch_performed: false` 或三方 HEAD 不相等都不能成为 `fresh: true`。Selected local base
落后时，只能在 selected-base checkout 上执行 `git merge --ff-only`；wrong checkout、dirty、
missing ref、fetch failure、divergence、resolution drift 或 post-sync mismatch 均 fail closed。
Every prepare invocation receives the preceding validator/guard post-sync
resolution digest and the same resolver inputs. It preserves explicit/config/config-candidate/
remote-default provenance. Legacy `--create-issue-confirmed`,
`--create-worktree`, and `--create-task` fail closed before any write and point
to `guru-create-task-workspace`.

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

Package schemas 是 `guru-task-workspace-plan-1.0` 与
`guru-task-workspace-result-1.0`。Workflow/standalone preconditions 完全一致。
Reviewed draft invocation 只取得 `github_issue_mutation` confirmation，创建 exact issue 并
重读后固定返回 `refresh_review`；同一调用不创建 branch/worktree/task。完整 Intake 重跑后，
open issue invocation 另行取得 `workspace_and_task_mutation` confirmation。外部出口固定为
`created`、`refresh_review`、`cancelled`、`blocked`。
Passed + confirmed 才可 mutation；passed + refused、`reroute`、`blocked` 分别生成
checker-validated zero-write `cancelled`、`refresh_review`、`blocked` result。

Draft create 前按 exact open title/body/labels 与 `createdAt >= reviewed plan`执行 0/1/>1
recovery：0 个创建，1 个恢复并 live reread，多个阻断。完整 Intake 重入后的
workflow-created issue必须携带完整 checker-passed created-issue result，并重验 result/binding
digest、reviewed draft/confirmation identity、current issue 与 fresh context canonical live
existing-issue identity；该 context使用`kind=issue`与 null `issue_binding`。

Assignee 固定按 explicit input、exactly one issue assignee、zero issue assignees 时 current
GitHub login、multiple/unresolved 时 AI/user 选择解析；executor 始终向 official
task-create handler 显式传 reviewed assignee。Executor 在隔离子进程中调用 official
`common.task_store.cmd_create`，并仅在该 handler 调用内禁用 developer accessor，使
`task.json.assignee` 与 `task.json.creator` 都等于 reviewed login。创建成功只写 tracked task-local
`task-start-context.json`、`issue-scope-ledger.json`、`context-discovery.json`、
`issue-review.json`；plan/result stdout-only，本机 mapping 只在 ignored
`.trellis/.runtime/guru-team/**`。Public result 不含 absolute workspace path；checker
从 current config、reviewed slug 与 live Git facts 推导 worktree。

`task-start-context.json` 只提供 portable `workspace_slug`、`task_workspace_id` 和
repo-relative `task_artifact_dir`，不得提供 absolute `workspace_path`。`workspace_mode:
worktree` 下，task artifact 写入边界由当前 checkout、`.trellis/.runtime/guru-team/**`、
`git worktree list` 和 `check-workspace-boundary.sh --task` 推导/校验。
在写入或校验 `planning-approval.json`、`phase2-check.json`、`agent-assignment.json`、
`reviews/*.md`、`review.md` 或 `review-gate.json` 前，从目标 worktree 运行：

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

`no_task` 下的 current-checkout direct edit 是显式 override，而不是 AI 可自行选择的
默认捷径。只有当用户明确批准本轮跳过创建或复用 GitHub issue、Trellis task、worktree
和 branch 时，AI 才能在当前 checkout 改文件；改动前仍要说明 skipped artifacts、
current checkout / branch / dirty state、side effects 和 changed-file scope。该批准
不包含 commit、push、PR creation 或 issue closure。

Branch Review Gate、agent assignment recorder 与 publish helper 是内部子命令：

```bash
.trellis/guru-team/scripts/bash/record-subagent-liveness-event.sh --json \
  --task ".trellis/tasks/<task>" \
  --source-repo "<source-checkout-path>" \
  --logical-role "实现代理" \
  --agent-id "<technical-agent-id-or-empty>" \
  --platform-nickname "<display-name-or-empty>" \
  --event assigned \
  --observed-at "2026-07-07T00:00:00Z" \
  --evidence "中文分配原因"
.trellis/guru-team/scripts/bash/check-subagent-liveness.sh --json \
  --task ".trellis/tasks/<task>" \
  --agent-id "<technical-agent-id>" \
  --source-repo "<source-checkout-path>" \
  --progress-scan-interval 120 \
  --max-progress-silence 180
.trellis/guru-team/scripts/bash/record-agent-assignment.sh --json \
  --logical-role "最终放行审查代理" \
  --agent-id "<technical-review-agent-id>" \
  --platform-nickname "<display-name-or-empty>" \
  --review-round 3 \
  --reviewed-head "$(git rev-parse HEAD)" \
  --findings-count 0 \
  --reuse-policy "fresh 最终放行审查代理完整审查当前 HEAD diff" \
  --reuse-decision new-agent \
  --review-round-report ".trellis/tasks/<task>/reviews/round-003-final-release.md"
.trellis/guru-team/scripts/bash/record-agent-assignment.sh --json \
  --task ".trellis/tasks/<task>" \
  --invalidate-event-id "<incorrect-progress-or-status-event-id>" \
  --correction-reason "主会话已判断该 event provenance 不成立" \
  --correction-evidence "已核对技术 agent 披露与原始 recorder 来源"
.trellis/guru-team/scripts/bash/record-agent-assignment.sh --json \
  --task ".trellis/tasks/<task>" \
  --link-failed-event-id "<failed-event-id>" \
  --link-termination-event-id "<later-same-agent-terminated-event-id>" \
  --recovery-reason "补录历史 failed 到 termination 的 append-only 结构边" \
  --recovery-evidence "已核对 resume/termination/replacement/completed 原始事件顺序"
.trellis/guru-team/scripts/bash/check-agent-assignment.sh --json
.trellis/guru-team/scripts/bash/check-commit-messages.sh --json --task ".trellis/tasks/<task>"
.trellis/guru-team/scripts/bash/format-merge-commit.sh --json --task ".trellis/tasks/<task>" --pull-request "<pr-number>" --summary "中文 PR 摘要"
.trellis/guru-team/scripts/bash/review-branch.sh --json --pass \
  --review-source independent-agent \
  --reviewer "trellis-check-agent" \
  --review-report ".trellis/tasks/<task>/review.md" \
  --agent-assignment ".trellis/tasks/<task>/agent-assignment.json" \
  --summary "中文审查结论" \
  --evidence "已按 intake base 到 HEAD 的完整 diff 覆盖文档、代码、测试、Trellis artifacts、CI/CD、容器、K8s/Kustomize、数据库 migration、Makefile，并判断本次变更的部署影响及是否需要同步修改部署资产"
.trellis/guru-team/scripts/bash/check-review-gate.sh --json
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work \
  --finish-summary-index-file ".trellis/tasks/<task>/finish-summary-index.json" \
  --body-file ".trellis/tasks/<task>/pr-body.md" \
  --dry-run
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work \
  --finish-summary-index-file ".trellis/tasks/<task>/finish-summary-index.json" \
  --body-file ".trellis/tasks/<task>/pr-body.md" \
  --expected-plan-digest "<closeout_plan_digest>"
```

Sub-agent wait / stale / termination policy is part of the workflow contract,
not a hidden script decision. `wait_agent`, `trellis channel wait`, or
equivalent timeout only means the current wait window ended without a final
completion event. It does not prove the agent is stuck, failed, or ready to
stop. The main session must use `record-subagent-liveness-event.sh` and
`check-subagent-liveness.sh` as the active status/liveness path.

`agent-assignment.json` schema 1.2 is the single task-local assignment,
status/liveness, and review ledger. It contains `agents[]`, `status_events[]`,
`liveness[agent_id].last_scan_snapshot`, review rounds, reuse decisions,
append-only `event_corrections[]`, and `recovery_links[]`. Corrections
digest-bind one existing progress/status-request row and exclude it from the
effective projection; recovery links connect only same-agent failed-to-manual
termination events and still require a real replacement `completed` chain.
Non-machine-readable progress such as explicit messages, tool activity,
command output, platform progress events, or status responses must be recorded
to `status_events[]` before checker can use it as evidence. The checker is a
short-lived, single-sample command; it reads task/source checkout snapshots and
progress event digest, returns one decision, and exits. It does not read
platform UI, send status requests, terminate agents, or judge implementation
quality.

Default timing: `progress_scan_interval=120s` controls scan cadence.
`max_progress_silence=180s` is measured from `progress_anchor_at`.
`status-requested` does not refresh that anchor or extend
`max_progress_silence_deadline_at`. Only `status_request_required` authorizes
one status request; after recording `status-requested`, immediately rerun
checker and do not repeat the ping while pending. Only `stale_allowed`
authorizes `stale-assessed`. If the deadline has already passed but no pending
status request exists, checker still returns `status_request_required` first.

Source checkout dirty paths or task artifacts are workspace-boundary progress
facts. Source checkout `HEAD`, dirty status, diff stat, or mtime changes make
checker return `workspace_boundary_violation_progress`, not stale evidence.
Stale cutover requires `stale-assessed`, then
`terminated-unfinished termination_reason=stale_cutover
termination_source_event_id=<stale-assessed.event_id>`, then replacement
`assigned` and `replacement-started replacement_reason=max_progress_silence_exceeded`.
Manual/platform unfinished termination uses
`termination_reason=manual_or_platform_terminated_unfinished`. Failed, stale,
unfinished, or replacement partial output cannot be used as Phase 2 check pass
or Branch Review Gate pass evidence until a same-agent resume or replacement
chain reaches `completed`; replacement `failed` requires further recovery. The
old `record-agent-assignment.sh --status-event` path fails closed and points
callers to `record-subagent-liveness-event.sh`.

用户日常可以直接描述任务、贴 issue URL，或说“处理 issue #123”。AI 依赖
Trellis 自动注入的 startup context、workflow-state、hook breadcrumb 或 skill
matcher 判断是否进入 Guru Team issue intake 和 worktree preflight。

用户常用显式入口保留为 `trellis-continue` 和 `trellis-finish-work`。`trellis-start`
仍保留为 fallback / explicit orientation 入口，用于无自动注入平台、hook 未启用或
未审批、怀疑自动注入没有运行，或需要完整上下文报告和重新加载 Trellis 上下文的场景。

Planning start gate 和 Phase 2 check gate 都需要 task-local evidence。进入实现前主会话
在三份 planning artifact 与 `Docs SSOT Plan` 就绪后 mandatory invoke
`guru-approve-task-plan`。该 Skill 负责全部 entry precondition、审查、必要 revision/clarification、链接展示、
confirmation、v2 recorder/checker 和四出口；只有 `approved` 可以进入
`phase-1-task-activation`。Phase 0 handoff、active schema 1.2、缺失/过期/non-pass wording、
planning/authority 内容漂移、普通 confirmation 冒充 dedicated proposal confirmation 或
exit/Gate/consumer 不一致均 fail closed。`task.py start` 只是状态写入，不代表规划已审查。
阶段停止点和阶段完成回复还必须给用户一个最新的 task Markdown 入口表。AI 先运行
`resolve-human-artifacts.sh --json --task <task-path>`，再输出
`Markdown 产物 review 表`；标准表只列 `prd.md`、`design.md`、`implement.md`、
`review.md`、`pr-body.md` 五个 Markdown，缺失文件不生成 Markdown 链接，JSON gate /
evidence artifact 不进入默认表。Branch Review 后的 `review.md` 行代表 AI/human
review 报告，raw `reviews/*.md` 通过 `review.md` 进入。
commit 前先由 unchanged official `trellis-check` 收集 raw review evidence，再
mandatory invoke active semantic Skill `guru-check-task`。该 Skill 先做 scope
qualification，再做 current-scope severity、complete adequacy、Docs SSOT review、
finding/full-rerun loop 与最终 AI Gate；它独占 closed
`guru-phase2-check-2.0` 的唯一 `phase2-check.json` 和 `passed` /
`implementation_required` / `planning_stale` / `blocked` 四出口。
`record-phase2-check.sh` 与 `check-phase2-check.sh` 只处理 AI-authored result 的
确定性 schema/linkage/hash/HEAD/diff/dirty/agent/route facts；几个验证命令、worker
输出或脚本通过不等于 semantic pass。`phase2-check.json` 是 commit
前 Guru Team evidence artifact，用于固化完整 Skill round 的覆盖范围、
验证结果、findings 和 `dirty_paths`，不是 Trellis 原生步骤本身，也不是脚本替代
AI check 的入口；commit 后 Branch Review Gate 会审计后续提交
的非 metadata 路径是否都被这些 `dirty_paths` 覆盖。不要为了让 `phase2-check.json.head`
匹配当前 HEAD 而在 task work commit 后重录 Phase 2，除非提交后又出现新的非 metadata
改动或 evidence 已失效。

V2 schema/checker 要求 provenance、handoff、durable paths、reviewed paths、commands
与 adequacy evidence refs 非空并覆盖全部 known current-round source；current/scope-change
candidate 必须带 trigger refs。Checker 重算 execution/scope/adequacy、全部 Gate binding、
finding count 与 full-round digest。若 handoff 包含 task-local assignment，合法 post-commit
review assignment/status/completed/round tail 由 stable Phase 2 projection 复核，Phase 2
implementation/check/recovery drift 仍 fail closed。

Phase 2 必须消费 planning 阶段的 `Docs SSOT Plan`。实现代理需要在 handoff 中说明
plan strategy、durable docs 同步结果、task delta merge、task-history-only 内容、
`no_docs_update_needed` 理由或 `bootstrap_or_repair_docs` follow-up / PR 限制，以及哪些实现输入
来自 durable docs、哪些来自已确认 task delta。`trellis-check` 需要按同一策略复核 durable docs、
task artifacts、code/schema/config/deploy/test 和验证/测试覆盖是否一致；`delta_first` 必须在最终
Phase 2 check 前完成 durable docs merge，`ssot_first` 必须以修订后的 durable docs 为主要输入。
如果实现发现长期合同变化超出 plan，必须先更新 planning artifacts 和 `Docs SSOT Plan`，必要时重新
planning approval，再重新 Phase 2 check。

Codex 项目默认使用 `codex.dispatch_mode: sub-agent`，由 main session 调度
`trellis-implement` / `trellis-check`。默认 sub-agent mode 下，main session 只负责
规划、调度、等待/恢复/替换、记录 evidence、commit 和运行 recorder/validator；实现必须由
`trellis-implement` / channel `implement` 完成并输出 handoff，Phase 2 check 必须由
`trellis-check` / channel `check` 完成并输出可记录到 `phase2-check.json` 的 evidence，
commit 后 Branch Review 必须由独立 review sub-agent 审查完整 `origin/<base>...HEAD`
diff 并输出 `reviews/*.md` raw reports 与最终 `review.md` rollup。main session 自己实现、自检、自审或脚本校验通过都不能替代这些
边界；缺少 artifact evidence 时 fail closed。因为 Codex sub-agent 使用
`fork_turns="none"` 隔离，dispatch prompt 必须以 `Active task: <task path>` 开头；
sub-agent 若没有拿到该行，则运行 `task.py current --source` 解析当前 task。只有显式配置
`codex.dispatch_mode: inline` 时，Codex 才降级为 main session 直接实现和检查。
Guru Team preset 安装项目级 agent 定义：Codex 使用中文 `description` 表达 UI 语义，
但 `nickname_candidates` 保持 ASCII，因为当前 Codex 会拒绝中文 nickname 候选并忽略
agent 文件；Cursor / Claude / channel runtime agent 使用中文 description 和标题。这些文件中的
`trellis-implement` / `trellis-check` / `trellis-research` 以及 channel runtime 的
`implement` / `check` 是稳定调度标识，不能为了中文展示而改名。

sub-agent assignment 记录在 task-local `agent-assignment.json`。`logical_role`
是中文 Trellis 流程身份，允许值为 `实现代理`、`阶段二检查代理`、
`问题发现审查代理`、`问题闭环审查代理`、`最终放行审查代理`；`agent_id` 是技术身份；
`platform_nickname` 只记录平台 UI 展示名，优先记录中文昵称；平台只给随机/自动昵称时记录
原始值。它不参与 gate 判断。AI/human 决定分配、复用或更换 agent 后，脚本只能记录和
校验 JSON 结构、角色枚举、HEAD 与 digest，不替代判断。每轮 review 还必须用
`--review-round-report <task-local reviews/*.md>` 记录 raw report path、sha256、size
和 modified_at。AI/human 对 wait timeout、
stale、interrupt、unfinished termination、resume/replacement、completed、failed 的状态
处理也记录在 `status_events[]`；脚本不决定 timeout 是否等于 stale，也不决定是否终止 agent。

Branch Review Gate 必须先让所有发现过 finding 的 reviewer 作为同一 technical
`问题闭环审查代理` 确认其 finding 已闭环并记录 0 findings；如果原 reviewer 失败/中断且无法继续，
必须用 `status_events[]` + `reuse_decisions[] decision=replace` 记录替代闭环链，并由替代
`问题闭环审查代理` 只闭环该 finding。之后再由 fresh
`最终放行审查代理` 独立审查当前 HEAD 的完整 diff 并确认 0 findings，最后调用
`review-branch.sh` 固化结论。任意 finding priority（P0/P1/P2/P3）都会阻断；
`observation` 仅记录非阻断观察，`followup_candidate` 仅记录 scope 外后续候选。
最终放行审查还必须验证 Docs SSOT reconciliation 已经在 Phase 2 完成：读取 approved
`Docs SSOT Plan`、实现 handoff、`phase2-check.json`、durable docs、task artifacts
和完整 diff，确认 `ssot_first` / `delta_first` / `bootstrap_or_repair_docs` /
`no_docs_update_needed` 对应条件已经满足。当前 scope 的 Docs SSOT 不一致必须是 finding；
final reviewer 不首次 merge durable docs，也不替 implement/check 代理补 Phase 2 docs 工作。
独立 review sub-agent 只从 AI 角度审查文档、代码、测试、artifact 和 diff evidence，
不继续实现、不替 implement/check 代理补工作，也不运行 `review-branch.sh`、
`check-review-gate.sh` 或 `record-*` 这类 Guru Team recorder/validator 扩展脚本；
这些脚本由 main session 在 review 完成后执行。
`review-branch.sh` 是 recorder / validator，不是 reviewer；`--pass` 必须先写
每轮 task-local `reviews/*.md` raw report，再写最终 `review.md` rollup；rollup
必须链接所有 raw reports。然后带中文 `--summary`、至少一条 `--evidence`，
`--review-source independent-agent`、`--review-report .trellis/tasks/<task>/review.md`
和 `--agent-assignment .trellis/tasks/<task>/agent-assignment.json`。Gate 会记录
final `review.md` digest、raw `review_reports[]` digest、assignment digest、中文角色摘要和 status event count，并校验同 agent 或替代闭环先于 fresh final、
未完成终止的恢复/继任链已到达 `completed` 或 `failed`、最终放行代理不是 earlier
finding owner 或替代闭环 reviewer。`--reviewer` 只记录身份，不能替代 review report digest；
`*-main-session` / `self-review` 不能通过 gate。
Phase 2 的官方 `trellis-check` sub-agent 只提供 commit 前 raw review evidence；随后
active `guru-check-task` 独占完整 semantic check、四出口与 `phase2-check.json`。Phase 3 Branch Review 必须由独立 review sub-agent 审查完整
`origin/<base>...HEAD` diff 并输出 `review.md`，最终门禁以 `review-gate.json` 为准，
且 `review-branch.sh` 会先校验 Phase 2 check evidence 和 post-commit dirty-path
覆盖关系。

`trellis-continue` 不得 push 分支、创建 PR、调用 `publish-pr` 或调用
`finish-work`，也不得提交 `review.md` / `reviews/*.md` / `review-gate.json` 等 Trellis metadata。
PR 发布只发生在显式 `trellis-finish-work` 入口。dry-run 输出完整 immutable
`closeout_plan` 与 `closeout_plan_digest`；正式执行必须原样传入该 digest，并在首个副作用前
重建校验。随后按 reviewed content push、marketplace evidence/readiness commit、draft PR、
final archive projection、单次 archive metadata commit/push、三方 HEAD 对齐、draft-to-ready
推进。裸 `finish-work.sh` 默认拒绝普通直接调用，`publish-pr.sh` 无条件作为兼容入口
阻断；中断只重跑同一个 `trellis-finish-work`，不暴露内部 recovery flag。
Prepare 使用已安装的官方 config parser，只支持缺失或空 `hooks.after_archive`；
非空、歧义、不可读、含 NUL 或 symlink 配置在副作用前拒绝，且不会执行 hook。
official move 前重新核对实时 archive 月份、空 index、精确 untracked 集合、regular-file/mode
与 tracked evidence blob。已提交 plan 跨月时 task 保持 active；同一 entry 重新 dry-run
得到新 digest，再追加只更新 plan/readiness 的 evidence commit，不 rewrite history 或迁移目录。
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

`finish-work.sh --dry-run --from-trellis-finish-work` 是无副作用 readiness preview：
它校验 gate、dirty state、AI-authored `finish-summary-index.json` 和 PR body/readiness，
并输出 canonical plan、digest、future archive mapping、metadata allowlist 与 transitions，
不移动或写入文件、不创建 commit、不 push、不创建 PR，且没有 journal/workspace 计划。
dry-run 回复使用 active task 的 `Markdown 产物 review 表`；正式 archive 后，AI 必须
重新运行 resolver 解析 `.trellis/tasks/archive/YYYY-MM/<task>/...` 路径，并在最终回复输出
archive-path 表，不能复用 archive 前的 active task 链接。

PR body 是给 GitHub reviewer 看的发布材料，不是 Trellis task artifact 的内部索引。
AI 在调用 finish helper 前必须生成或审查 body readiness，确认 `变更摘要` 具体、
`影响范围` 明确、`验证结果` 是实际命令与结果、`Review Gate` 写明 reviewed HEAD /
diff range / findings 状态、`Issue 关闭范围` 只关闭 ledger 中的 `close_issues`，并且
`安全说明` / 部署影响与本次 diff 相符。Body 还必须包含 `Docs SSOT` / `文档同步`
section，说明策略、durable docs 更新或 no-update 理由、已 merge 的 task delta、仅保留
task history 的内容，以及 follow-up / 当前 PR limitation。finish-work 必须把审阅后的 Markdown
body 存成当前 task-local `pr-body.md` 并以 `--body-file` 传入；从 repo root 到 task
目录和最终文件的每个现存 path component 都必须不是 symlink。它拒绝 `--body-artifact`、
外部/alias 路径、dangling/loop symlink，以及仅在 trim/末尾换行/Markdown hard-break 空格上等价的替代内容：

```bash
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work \
  --finish-summary-index-file .trellis/tasks/<task>/finish-summary-index.json \
  --body-file .trellis/tasks/<task>/pr-body.md
```

AI-authored `finish-summary-index.json` accepts at most 19 `contract_changes`;
the final schema accepts 20 so the recorder can append the fixed filtering fact.

Guru Team 不调用 `.trellis/scripts/add_session.py`，不读写 `.trellis/workspace/**`。
shared `trellis-start` 只读取 phase/packages/current-task/Git facts，Codex/Cursor
SessionStart overlay 不导入或调用 journal helper，也不打开、枚举、读取或输出 journal。
finish-work 先绑定唯一 draft PR，再在 active task 中一次构建包含 canonical URL 与唯一
`PR #<number>` ref 的 final summary。recorder 对 raw base-to-HEAD paths 排序去重后过滤 workspace/runtime
受保护前缀，过滤发生时追加一条不含 path、basename 或数量的固定 contract fact；未发生过滤时
不追加。initial diff、initial untracked 或 final/recovery diff 失败时两个 path 数组都为空，
只追加固定 snapshot-unavailable fact，并重新派生 retrieval text。schema/validator 对所有 path 字段继续拒绝受保护前缀。final summary 在 active task 中严格
校验一次，并只随 archive metadata transaction 提交。archive 后不再校验、回写 artifact 或新增
metadata tail。同一入口在 archive 前根据 plan/readiness、active locator 与 evidence facts 恢复。
official move 后、精确 archive commit 尚未形成时，仍校验 archived working-tree 完整布局、
dirty/staged path、blob continuity 与官方 `task.json` delta；commit 缺失或不匹配继续 fail closed。
一旦当前 `HEAD` 已是精确 archive commit，普通 archived task 与 plan-only recovery 都从该
commit blob 读取 plan；immutable plan 与 Git parent/path/tree/blob lineage 成为
权威事实，本地 archived 文件缺失、篡改及其 dirty state 不阻塞 exact push、remote PR title/body
digest、三方 HEAD 或 draft-to-ready。plan-only archived directory 只由 `trellis-finish-work` 恢复入口
解析，普通 task 命令仍要求 `task.json`。real-PR final summary 的 deterministic bytes/digest 纳入
pre-move、incomplete recovery 与 exact recovery continuity：前两者用已绑定 remote PR 重建 expected
bytes，exact recovery 只从 immutable archive commit 的 `finish-summary.json` blob 恢复原 PR number/URL
并重建校验，不读取 working-tree summary，也不调用通用 summary artifact validator。原 PR 缺失、
closed 或被同 repo/head/base 的新 PR 替代时 fail closed；其它 archived artifacts 不重新打开。
final projection、incomplete 与 exact recovery 共用一个 strict PR URL parser。GitHub
owner/repository identity 大小写不敏感，canonical summary URL 保留 remote 返回的合法 casing
（例如 `microsoft/PowerToys`）；错误 repo、transport、number、额外 path、query/fragment 仍被拒绝。
plan-only 恢复从当前 commit blob 读取 immutable plan，并在 GitHub/fast-path 前用专用 fail-closed
boundary 校验 Git toplevel、配置/effective repo、当前head branch、base ref、current HEAD transaction、
expected digest、task identity 和 active/archive locator；它不是缺失 context 时的无条件跳过。普通
task discovery 与其它命令仍要求 `task.json`，worktree mode 仍要求 `task-start-context.json`。
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

`finish-work` 在首次 PR create 前写入并提交 task-local
`pr-readiness.json.publish_inputs`，固定 repo/base/head、reviewed HEAD、exact title、
`pr-body.md` SHA-256、`draft=true`、reviewed source 与 `closeout_plan_digest`。
readiness/body 文件属于 Trellis task metadata；archive transaction 将其与 final summary 原样移动。
脚本只做客观结构校验、低信息量短语阻塞、close/ref 语义校验和 reviewed source 门禁；
不能用脚本生成的空泛摘要或 `generated` body 替代 AI 发布判断。


## One-Time Archived Task Backfill

After installing or updating this preset, repositories with archived tasks from
before `finish-summary.json` can preview and write schema-valid history records:

```bash
.trellis/guru-team/scripts/bash/backfill-finish-summary.sh --json --dry-run
.trellis/guru-team/scripts/bash/backfill-finish-summary.sh --json --write
```

Use `--task .trellis/tasks/archive/<YYYY-MM>/<task>` to limit the batch. Existing
summaries are skipped unless `--write --force` is explicit. The command reads
only its fixed archived-task artifact whitelist, groups all changed paths by
surface kind without truncation, reports task-local errors while continuing the
batch, and never reads workspace/runtime state or creates a global index. This
one-time migration supplies historical records consumed by the later #98
history-discovery capability; it does not replace normal finish-work.

## Push 后远端 Marketplace 门禁

修改 marketplace/preset/overlay/schema/public API 时，recorder 在 reviewed content push 后从 immutable closeout plan 生成 pending machine evidence；verifier 成功后只替换为 passed。plan、readiness、artifact 与 ledger 形成 exact pre-draft metadata commit，push 并校验 remote HEAD 后才允许绑定 draft PR。缺失、重复、pending、失败、篡改、HEAD 不匹配或 stale 均阻止创建 PR；human reason 不参与 machine identity，该门禁不创建 tag，AI 仍负责 close scope 与 PR readiness 判断。

## Skill 行为评测

安装完整 Guru Team preset 后，可用 `discover-skill-evals` 发现 Interface 1.3
package 的 `evals/evals.json`，并用 `run-skill-evals` 经
`shared|codex|claude|cursor` adapter 实际执行 public wrapper。Schema id 是
`guru-team-skill-evals-1.0`，status 闭集为
`passed|evaluation_failed|execution_error|unsupported`。外部 semantic grading
与 human feedback 独立，run evidence 只能位于 repo 外。当前 production Skills
中的六个 Stage 0 packages 已维护 canonical corpora 并覆盖全部 24 exits/profile；
#146 继续覆盖 planning/check/commit 三包。四个 descriptor 分别绑定
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
