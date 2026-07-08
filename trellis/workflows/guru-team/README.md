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
  --workflow-source gh:castbox/guru-trellis/trellis#v0.6.5-guru.1
```

`-y` 是团队默认安装路径的一部分，用于跳过交互式 spec template picker。自动验收、
throwaway 安装验证和 README 默认命令都必须使用非交互形式；只有用户明确想手动选择
spec template 时，才去掉 `-y` 或改用官方支持的 `--template <name>`。

稳定安装 source 使用 repo release tag `#v0.6.5-guru.1`，并要求官方 Trellis CLI 安装到
`0.6.5`。维护者刻意跟随最新 `main` / canary 时可以去掉 `#ref` 或改用其它 branch/tag ref，
但应在验证和排障报告中说明 source 是否为 mutable ref，以及是否仍以官方 Trellis `0.6.5`
为目标基线。Guru Team release tag 使用 repo 级 `v<official-trellis-version>-guru.<revision>`，
并与 `trellis/guru-team-extension.json.version` 对应。

已有 Trellis 项目切换 active workflow：

```bash
trellis workflow \
  --marketplace gh:castbox/guru-trellis/trellis#v0.6.5-guru.1 \
  --template guru-team
```

只有在需要生成 `.trellis/workflow.md.new` 做人工 review、且不切换 active
workflow 时，才使用 `--create-new`。

## Companion Assets

Trellis workflow marketplace 只负责安装或切换 `.trellis/workflow.md`。
companion scripts、配置、schema 和团队自有入口 overlay 需要通过 preset installer
写入目标仓库：

```bash
git clone --depth 1 --branch v0.6.5-guru.1 \
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

## Knowledge Gate 与 Docs SSOT

当任务可能涉及 Guru Team 中台 SDK / framework 时，AI 应按 `.trellis/workflow.md`
检查当前平台是否可用 `guru-knowledge-center` MCP。可用时使用
`project_domain=middle-platform` 和当前 task context 检索，并把 citation 写入
`design.md`、`implement.md` 或 `{TASK_DIR}/research/middle-platform-knowledge.md`。
MCP 不可用时，默认 `optional_warn` 只告警并继续；配置为 `required` 时才阻塞。

Trellis task artifact 不是长期 repo docs 的替代品。Planning 阶段要识别 `docs/`
下 requirements、designs、testplans、deploy / operations、versioned design docs
等 durable docs SSOT；finish 前要记录哪些 docs 已更新、哪些 task artifact 内容已
合并回 durable docs、哪些只保留为 task history。无完整 docs 系统的 repo 也要明确
记录“创建 docs / 补 partial docs / 暂不设 durable docs SSOT”的结果。

业务项目内人类可读文档默认使用中文，覆盖 `.trellis/spec/**` 项目规范、
`.trellis/tasks/**` task artifact、`docs/**` durable docs、`00-bootstrap-guidelines`
创建或补齐的 docs SSOT，以及 workflow/helper artifact 中的 summary、evidence、
finding、observation、follow-up candidate、PR title/body 等字段。命令、路径、配置键、
GitHub keyword、外部 API 名称和代码符号等 literal token 可保留英文。`guru-trellis`
源码仓库自身是公共扩展仓库，它的 README、源码注释、脚本帮助和 marketplace metadata
可按分发需要保留英文或双语。

对 issue-backed、task-like 或需要文件修改的 `no_task` 请求，Guru Team 的第一跳是：

```bash
.trellis/guru-team/scripts/bash/check-env.sh --json
.trellis/guru-team/scripts/bash/prepare-task.sh --json "<user request or issue URL>"
```

`prepare-task.sh --json` 默认只执行 intake 和 preflight planning，不创建 GitHub
issue、worktree、branch、Trellis task，也不写 `.trellis/guru-team/handoff.json`。
它只在 stdout JSON 中输出 source/proposed issue、duplicate candidates、base branch、
branch name、workspace path、`create_task_command`、`naming_quality`、
`preflight.base_freshness` 和 `handoff_written: false`。默认 planner 输出也会执行
`git fetch origin <base>` 或给出明确的远端无法确认状态；不得把
`fetch_performed: false` 的本地 remote-tracking 缓存当作 `fresh: true` 证据。
如果本地 base 落后远端，planner 会报告 `fresh: false`、`status: stale`、
`fast_forwarded: false`，并保留 `local_head_before` / `local_head_after` 不变。

`naming_quality` 是 slug / branch / worktree / task 命名质量门禁。AI 读完 issue 后
应生成语义英文 short-name，并通过 `--short-name`、`--workspace-slug`、`--task-slug`
和 `--branch` 显式传给脚本。推荐 worktree/task slug 格式为
`NNN-business-capability`，branch 格式为 `codex/NNN-business-capability`，例如
`052-resume-detail-inline-attachment-preview`。中文或非 ASCII issue 标题不依赖拼音
transliteration 作为默认分支名；脚本不会智能翻译，只会做确定性拼装、冲突检查和低信息命名
阻断。

GitHub issue 创建必须在 AI/human review proposed title/body 之后显式执行：

```bash
.trellis/guru-team/scripts/bash/prepare-task.sh --json \
  --create-issue-confirmed \
  --issue-title "<reviewed issue title>" \
  --issue-body-file <reviewed-issue-body.md> \
  "<user request>"
```

只有在用户已经 review 计划中的 source issue、base branch 和 workspace path 后，才使用
`--create-worktree` 或 `--create-task`。这两个 executor 路径会创建或复用 chosen
workspace，并把 `.trellis/guru-team/handoff.json` 写在该 workspace 内；仅启动新会话或
执行默认 preflight 不应污染 source checkout。`workspace_mode: worktree` 下应使用
`prepare-task --create-worktree --create-task` 或等价 Guru Team 受控入口创建执行 worktree
和 Trellis task；若 `naming_quality.ok=false`，executor 会在任何 worktree/task 副作用前失败，
并提示调用方传入语义命名覆盖。task creation consent 不是在 source checkout 直接运行裸
`task.py create` 的批准。

executor 路径创建 worktree 前会再次刷新所选 base branch：执行 `git fetch`、记录
`preflight.base_freshness`、仅在安全时 fast-forward 本地 base，并在本地 base 与远端
分叉或 freshness 无法确认时 fail closed。planner 的刷新证据不能替代 executor 创建前
的强校验；不要从过期的本地 `main` / `dev` 创建任务分支。

executor 路径创建或复用 worktree 后还会确保目标 workspace 有 Trellis developer
identity。脚本优先从发起 preflight 的 source checkout 复制 gitignored
`.trellis/.developer`；如果 source checkout 缺失该文件但调用方显式提供
`--assignee`，则在目标 worktree 初始化等价 identity；如果两者都不可用，会 fail
closed 并提示运行 `python3 ./.trellis/scripts/init_developer.py <name>`。这保证
`get_context.py`、`task.py list --mine` 和 `add_session.py` 不会等到 finish / journal
阶段才暴露 developer identity 缺失。

`no_task` 下的 current-checkout direct edit 是显式 override，而不是 AI 可自行选择的
默认捷径。只有当用户明确批准本轮跳过创建或复用 GitHub issue、Trellis task、worktree
和 branch 时，AI 才能在当前 checkout 改文件；改动前仍要说明 skipped artifacts、
current checkout / branch / dirty state、side effects 和 changed-file scope。该批准
不包含 commit、push、PR creation 或 issue closure。

Branch Review Gate、agent assignment recorder 与 publish helper 是内部子命令：

```bash
.trellis/guru-team/scripts/bash/record-agent-assignment.sh --json \
  --logical-role "实现代理" \
  --agent-id "<technical-agent-id-or-empty>" \
  --platform-nickname "<display-name-or-empty>" \
  --reason "中文分配原因"
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
.trellis/guru-team/scripts/bash/check-agent-assignment.sh --json
.trellis/guru-team/scripts/bash/review-branch.sh --json --pass \
  --review-source independent-agent \
  --reviewer "trellis-check-agent" \
  --review-report ".trellis/tasks/<task>/review.md" \
  --agent-assignment ".trellis/tasks/<task>/agent-assignment.json" \
  --summary "中文审查结论" \
  --evidence "已按 intake base 到 HEAD 的完整 diff 覆盖文档、代码、测试、Trellis artifacts、CI/CD、容器、K8s/Kustomize、数据库 migration、Makefile，并判断本次变更的部署影响及是否需要同步修改部署资产"
.trellis/guru-team/scripts/bash/check-review-gate.sh --json
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work \
  --body-file ".trellis/tasks/<task>/pr-body.md" \
  --dry-run
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work \
  --body-file ".trellis/tasks/<task>/pr-body.md"
```

Sub-agent wait / stale / termination policy is part of the workflow contract,
not a hidden script decision. `wait_agent`, `trellis channel wait`, or
equivalent timeout only means the current wait window ended without a final
completion event. It does not prove the agent is stuck, failed, or ready to
stop. The main session must distinguish long total runtime from no recent
observable progress: ongoing output, in-scope worktree changes, validation
progress, or channel events mean continue waiting. Stale assessment is based on
no observable progress for a recent window, default at least 5 minutes.

`agent-assignment.json.status_events[]` records wait timeout, progress observed,
stale assessed, continue waiting, same-agent resume, replacement start,
unfinished termination, completion, and explicit failure decisions already made
by AI/human. The recorder validates objective fields only. If an unfinished
agent is interrupted or terminated, the same `agent_id` must resume or a
replacement must inherit predecessor output, current diff, task artifacts,
remaining checklist, and gate blockers; Branch Review Gate pass is blocked
until that recovery chain has a later `completed` or `failed` event.

用户日常可以直接描述任务、贴 issue URL，或说“处理 issue #123”。AI 依赖
Trellis 自动注入的 startup context、workflow-state、hook breadcrumb 或 skill
matcher 判断是否进入 Guru Team issue intake 和 worktree preflight。

用户常用显式入口保留为 `trellis-continue` 和 `trellis-finish-work`。`trellis-start`
仍保留为 fallback / explicit orientation 入口，用于无自动注入平台、hook 未启用或
未审批、怀疑自动注入没有运行，或需要完整上下文报告和重新加载 Trellis 上下文的场景。

Planning start gate 和 Phase 2 check gate 都需要 task-local evidence。进入实现前主会话
必须展示 `prd.md` / `design.md` / `implement.md` 三个 task-local 链接，用户看到后
明确确认，才能调用 `record-planning-approval.sh` 写入
`user_confirmation.source=explicit-post-planning-review` 的 `planning-approval.json`，再用
`check-planning-approval.sh` 校验；Phase 0 handoff 确认或旧 `source=workflow` 不能
通过 gate，`task.py start` 只是状态写入，不代表规划已审查。
commit 前必须完成完整 `trellis-check`，再用 `record-phase2-check.sh` 写入
`phase2-check.json` 并用 `check-phase2-check.sh` 校验；几个验证命令通过只是 check
evidence 的一部分，不等于完整 `trellis-check` 覆盖。`phase2-check.json` 是 commit
前 Guru Team evidence artifact，用于固化 `trellis-check` AI check 的覆盖范围、
验证结果、findings 和 `dirty_paths`，不是 Trellis 原生步骤本身，也不是脚本替代
AI check 的入口；commit 后 Branch Review Gate 会审计后续提交
的非 metadata 路径是否都被这些 `dirty_paths` 覆盖。不要为了让 `phase2-check.json.head`
匹配当前 HEAD 而在 task work commit 后重录 Phase 2，除非提交后又出现新的非 metadata
改动或 evidence 已失效。

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
`问题闭环审查代理` 确认其 finding 已闭环并记录 0 findings，然后再由 fresh
`最终放行审查代理` 独立审查当前 HEAD 的完整 diff 并确认 0 findings，最后调用
`review-branch.sh` 固化结论。任意 finding priority（P0/P1/P2/P3）都会阻断；
`observation` 仅记录非阻断观察，`followup_candidate` 仅记录 scope 外后续候选。
独立 review sub-agent 只从 AI 角度审查文档、代码、测试、artifact 和 diff evidence，
不继续实现、不替 implement/check 代理补工作，也不运行 `review-branch.sh`、
`check-review-gate.sh` 或 `record-*` 这类 Guru Team recorder/validator 扩展脚本；
这些脚本由 main session 在 review 完成后执行。
`review-branch.sh` 是 recorder / validator，不是 reviewer；`--pass` 必须先写
每轮 task-local `reviews/*.md` raw report，再写最终 `review.md` rollup；rollup
必须链接所有 raw reports。然后带中文 `--summary`、至少一条 `--evidence`，
`--review-source independent-agent`、`--review-report .trellis/tasks/<task>/review.md`
和 `--agent-assignment .trellis/tasks/<task>/agent-assignment.json`。Gate 会记录
final `review.md` digest、raw `review_reports[]` digest、assignment digest、中文角色摘要和 status event count，并校验闭环先于 fresh final、
未完成终止的恢复/继任链已到达 `completed` 或 `failed`、最终放行代理不是 earlier
finding owner。`--reviewer` 只记录身份，不能替代 review report digest；
`*-main-session` / `self-review` 不能通过 gate。
Phase 2 的官方 `trellis-check` sub-agent 负责 commit 前质量检查并以
`phase2-check.json` 留痕；Phase 3 Branch Review 必须由独立 review sub-agent 审查完整
`origin/<base>...HEAD` diff 并输出 `review.md`，最终门禁以 `review-gate.json` 为准，
且 `review-branch.sh` 会先校验 Phase 2 check evidence 和 post-commit dirty-path
覆盖关系。

`trellis-continue` 不得 push 分支、创建 PR、调用 `publish-pr` 或调用
`finish-work`，也不得提交 `review.md` / `reviews/*.md` / `review-gate.json` 等 Trellis metadata。
PR 发布只发生在显式 `trellis-finish-work` 入口带
`--from-trellis-finish-work` 意图标记、成功 archive task、记录 journal、提交允许的
Trellis metadata 之后。`check-review-gate` / `finish-work` 会校验 final `review.md`
digest、raw `review_reports[]` digest，并在 task archive 后迁移 active task path 到
archive path。裸 `finish-work.sh` 和 `publish-pr.sh` 默认拒绝普通直接调用；
只有 `finish-work.sh` 的显式 finish entrypoint 调用或 finish-work 已完成后的显式
recovery/debug flag 可以进入 publish 检查。

`finish-work.sh --dry-run --from-trellis-finish-work` 是无副作用 readiness preview：
它只校验 gate、dirty state 和 PR body/readiness，并输出将要 archive、journal、
metadata commit 与 publish 的计划，不移动 task、不写 journal、不创建 commit、不 push、
不创建 PR。

PR body 是给 GitHub reviewer 看的发布材料，不是 Trellis task artifact 的内部索引。
AI 在调用 finish helper 前必须生成或审查 body readiness，确认 `变更摘要` 具体、
`影响范围` 明确、`验证结果` 是实际命令与结果、`Review Gate` 写明 reviewed HEAD /
diff range / findings 状态、`Issue 关闭范围` 只关闭 ledger 中的 `close_issues`，并且
`安全说明` / 部署影响与本次 diff 相符。non-draft publish 必须把审阅后的 Markdown
body 存成 task-local 文件并传给 helper，或传入 task-local readiness artifact：

```bash
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work \
  --body-file .trellis/tasks/<task>/reviewed-pr-body.md
```

`publish-pr` 也支持 `--body-artifact .trellis/tasks/<task>/pr-readiness.json`
读取 readiness artifact。readiness/body 文件属于 Trellis task metadata，`finish-work`
会在 archive 后从 `.trellis/tasks/archive/YYYY-MM/<task>/...` 读取最终 PR body。
脚本只做客观结构校验、低信息量短语阻塞、close/ref 语义校验和 reviewed source 门禁；
不能用脚本生成的空泛摘要或 `generated` body 替代 AI 发布判断。
