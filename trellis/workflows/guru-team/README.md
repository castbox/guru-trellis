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
trellis init -y -u <name> --codex --cursor \
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
stable 是 `.2`；本分支 canonical `.6` 在 merge/tag/远端验证完成前不是 stable source。

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
`guru-create-work-commit` reserved tombstone，并激活 `guru-sync-base` 与
`guru-create-task-commit`；workflow 不得为 reserved id 伪造 route。当前 canonical
extension version 是待发布的 `0.6.5-guru.7`，已发布 stable source 仍是
`v0.6.5-guru.2`。

Active interface schema 1.1 保留 `workflow` / `standalone` mode id，并以
`routing=global_workflow|direct_discovery` 区分 mandatory route 与平台直接发现。
`standalone` 仍依赖完整 Guru Team preset 与 compatible extension runtime，不是单目录
self-contained/portable 分发。Package wrapper 只能经 shared `run-skill-command`
dispatcher 调用 manifest 已发布的 companion command；runtime/API/inventory/drift 不匹配
必须在业务副作用前 fail closed，并提示完整 preset 安装或升级与 sidecar 处理步骤。

Active package 的 discovery contract 要求 `SKILL.md` 只有一段闭合
frontmatter，`name` 等于 stable id/registry/interface，`description` 非空且与
interface 一致；`tests[]` 只引用 package-local `tests/<file>` regular file。
Source validator 对 missing/drifted frontmatter 与 missing/outside/symlink test
evidence fail closed。

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

`config-template.yml` 显式包含 `middle_platform_knowledge.mode: optional_warn`。
已有目标仓库的 `.trellis/guru-team/config.yml` 不会为了补这个 key 被覆盖；如果 key
缺失，workflow 仍按 backward-compatible 默认 `optional_warn` 执行。`required` 只作
opt-in，`off` 只作 opt-out。

## Phase 0 Base Sync

Tool-free request classification 后，repo-changing route 的第一个 mandatory invocation
是 `guru-sync-base`。它按显式 `--base`、scalar `base_branch`（或单值兼容
`base_branch_candidates`）、remote default、existing refs 中恰好一个 fallback
candidate 的固定顺序解析 selected base；current branch 不是隐式 fallback。AI 必须先审查
invocation intent、resolution source 与 selected base，deterministic executor 随后以 reviewed
resolution digest 绑定重新解析、fetch 与可选 `git merge --ff-only`。

成功结果使用 `guru-base-sync-result-1.0`，并且必须证明 checkout clean、decision checkout
HEAD、local base HEAD 与 remote-tracking HEAD 三方相等。`sync-base` 只执行 resolution/sync
事实，`check-base-sync` 只校验 repo-external non-symlink evidence、schema、digest 与 live Git
facts；二者都不替代 AI Review Gate 或 route judgment。Stable exits 与唯一 consumers 是：

- `synced` -> `guru-discover-change-context`
- `skipped` -> `original-request-route`
- `blocked` -> `base-sync-blocked`

Workflow mode 只有 `synced` 才能继续 `check-env`、issue/duplicate reads 与
`prepare-task`。Standalone mode 可由所选平台直接发现同一 Skill，但仍要求完整 compatible
preset/runtime；workflow-only `--record-skipped original-request-route` 不可在 standalone
调用。Managed executable commands 位于
`.trellis/guru-team/scripts/bash/sync-base.sh` 和
`.trellis/guru-team/scripts/bash/check-base-sync.sh`。

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

```bash
.trellis/guru-team/scripts/bash/check-env.sh --json
.trellis/guru-team/scripts/bash/prepare-task.sh --json \
  --resolution-file <reviewed-resolution-file> \
  --expected-resolution-sha256 <reviewed-resolution-sha256> \
  "<user request or issue URL>"
```

`prepare-task.sh --json` 默认只执行 intake 和 preflight planning，不创建 GitHub
issue、worktree、branch、Trellis task，也不写 `.trellis/tasks/<task-slug>/task-start-context.json`。
它只在 stdout JSON 中输出 source/proposed issue、duplicate candidates、base branch、
branch name、workspace path、`create_task_command`、`naming_quality`、
`preflight.base_freshness` 和 `no task context/runtime write`。在 `gh auth status`、issue read
与 duplicate search 前，planner 必须通过 shared strict core 重解析和同步 selected base；
`fetch_performed: false` 或三方 HEAD 不相等都不能成为 `fresh: true`。Selected local base
落后时，只能在 selected-base checkout 上执行 `git merge --ff-only`；wrong checkout、dirty、
missing ref、fetch failure、divergence、resolution drift 或 post-sync mismatch 均 fail closed。
Every prepare invocation consumes the prior AI-reviewed external resolution
file and expected digest. It preserves config/remote-default/fallback
provenance. GitHub, worktree, and task mutation boundaries each get an
independent adjacent guard; the task guard runs after workspace/identity setup
and before `task.py create`.

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

GitHub issue 创建必须在 AI/human review proposed title/body 之后显式执行：

```bash
.trellis/guru-team/scripts/bash/prepare-task.sh --json \
  --resolution-file <reviewed-resolution-file> \
  --expected-resolution-sha256 <reviewed-resolution-sha256> \
  --create-issue-confirmed \
  --issue-title "<reviewed issue title>" \
  --issue-body-file <reviewed-issue-body.md> \
  "<user request>"
```

只有在用户已经 review 计划中的 source issue、base branch 和 workspace path 后，才使用
`--create-worktree` 或 `--create-task`。前者创建或复用 chosen workspace，并且只写 gitignored local runtime mapping；后者还会创建 Trellis task，并把 `.trellis/tasks/<task-slug>/task-start-context.json` 写在该 task 目录内。仅启动新会话或
执行默认 preflight 不应污染 source checkout。`workspace_mode: worktree` 下应使用
`prepare-task --create-worktree --create-task` 或等价 Guru Team 受控入口创建执行 worktree
和 Trellis task；若 `naming_quality.ok=false`，executor 会在任何 worktree/task 副作用前失败，
并提示调用方传入语义命名覆盖。task creation consent 不是在 source checkout 直接运行裸
`task.py create` 的批准。

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

`--create-issue-confirmed` 在 GitHub mutation 前重跑 shared core；`--create-worktree` /
`--create-task` 在 worktree/task mutation 前再次重跑。每次 fresh result 都记录
`preflight.base_freshness` 并要求 decision/local/remote HEAD 三方相等。Initial planner
evidence 不能替代 mutation-time guard；不要从过期的本地 `main` / `dev` 创建任务分支。

executor 路径创建或复用 worktree 后还会确保目标 workspace 有 Trellis developer
identity。脚本优先从发起 preflight 的 source checkout 复制 gitignored
`.trellis/.developer`；如果 source checkout 缺失该文件但调用方显式提供
`--assignee`，则在目标 worktree 初始化等价 identity；如果两者都不可用，会 fail
closed 并提示运行 `python3 ./.trellis/scripts/init_developer.py <name>`。这保证
`get_context.py` 和 `task.py list --mine` 不会等到后续阶段才暴露 developer identity 缺失。
Guru Team finish 不调用 `add_session.py`。

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
必须完成可定位的 `Docs SSOT Plan` 和 planning artifact ambiguity review，再展示
`prd.md` / `design.md` / `implement.md` 三个 task-local 链接，用户看到后明确确认，
才能调用 `record-planning-approval.sh` 写入 schema 1.2、passed
`ambiguity_review`、固定范围正文扫描 `hits[]`、空 `unchecked_normative_hits[]` 和
`user_confirmation.source=explicit-post-planning-review` 的
`planning-approval.json`，再用 `check-planning-approval.sh` 重新扫描校验；Phase 0
handoff 确认、旧 schema/source、缺失/non-passed ambiguity evidence、未分类命中或
`contract_violation` 命中不能通过 gate。校验 freshness 绑定三份规划文档内容 digest 和
scanner evidence；实现提交后的 HEAD drift、metadata tail 或无关 dirty paths 不会单独使
approval stale。`task.py start` 只是状态写入，不代表规划已审查。
阶段停止点和阶段完成回复还必须给用户一个最新的 task Markdown 入口表。AI 先运行
`resolve-human-artifacts.sh --json --task <task-path>`，再输出
`Markdown 产物 review 表`；标准表只列 `prd.md`、`design.md`、`implement.md`、
`review.md`、`pr-body.md` 五个 Markdown，缺失文件不生成 Markdown 链接，JSON gate /
evidence artifact 不进入默认表。Branch Review 后的 `review.md` 行代表 AI/human
review 报告，raw `reviews/*.md` 通过 `review.md` 进入。
commit 前必须完成完整 `trellis-check`，再用 `record-phase2-check.sh` 写入
`phase2-check.json` 并用 `check-phase2-check.sh` 校验；几个验证命令通过只是 check
evidence 的一部分，不等于完整 `trellis-check` 覆盖。`phase2-check.json` 是 commit
前 Guru Team evidence artifact，用于固化 `trellis-check` AI check 的覆盖范围、
验证结果、findings 和 `dirty_paths`，不是 Trellis 原生步骤本身，也不是脚本替代
AI check 的入口；commit 后 Branch Review Gate 会审计后续提交
的非 metadata 路径是否都被这些 `dirty_paths` 覆盖。不要为了让 `phase2-check.json.head`
匹配当前 HEAD 而在 task work commit 后重录 Phase 2，除非提交后又出现新的非 metadata
改动或 evidence 已失效。

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
Phase 2 的官方 `trellis-check` sub-agent 负责 commit 前质量检查并以
`phase2-check.json` 留痕；Phase 3 Branch Review 必须由独立 review sub-agent 审查完整
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
