# Guru Team Trellis Workflow

本目录维护 Guru 团队可复用的 Trellis workflow。

这个 workflow 的 marketplace id 固定为通用的 `guru-team`。它承载 GitHub issue
intake、Git base branch/worktree preflight、中文 planning artifact、Issue Scope
Ledger、Middle-platform Knowledge Gate、Repo Docs SSOT reconciliation、Branch
Review Gate，以及 finish-work 成功后的自动 publish PR 规则。

## Marketplace 安装

```bash
trellis init -y -u <name> --codex --cursor \
  --workflow guru-team \
  --workflow-source gh:castbox/guru-trellis/trellis
```

`-y` 是团队默认安装路径的一部分，用于跳过交互式 spec template picker。自动验收、
throwaway 安装验证和 README 默认命令都必须使用非交互形式；只有用户明确想手动选择
spec template 时，才去掉 `-y` 或改用官方支持的 `--template <name>`。

已有 Trellis 项目切换 active workflow：

```bash
trellis workflow \
  --marketplace gh:castbox/guru-trellis/trellis \
  --template guru-team
```

只有在需要生成 `.trellis/workflow.md.new` 做人工 review、且不切换 active
workflow 时，才使用 `--create-new`。

## Companion Assets

Trellis workflow marketplace 只负责安装或切换 `.trellis/workflow.md`。
companion scripts、配置、schema 和团队自有入口 overlay 需要通过 preset installer
写入目标仓库：

```bash
git clone https://github.com/castbox/guru-trellis.git /path/to/guru-trellis
/path/to/guru-trellis/trellis/presets/guru-team/scripts/bash/apply.sh \
  --repo /path/to/project
```

installer 会写入 `.trellis/guru-team/`，并可安装 `.agents/skills`、
`.claude/commands`、`.cursor/commands` 下的 Guru Team overlay。它不会修改 Trellis
上游脚本、npm 全局包、`node_modules` 或 `.trellis/scripts/task.py`。

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

`prepare-task.sh --json` 默认只执行 intake 和 preflight planning，不创建 GitHub
issue、worktree、branch、Trellis task，也不写 `.trellis/guru-team/handoff.json`。
它只在 stdout JSON 中输出 source/proposed issue、duplicate candidates、base branch、
branch name、workspace path、`create_task_command` 和 `handoff_written: false`。

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
执行默认 preflight 不应污染 source checkout。

executor 路径创建 worktree 前会先刷新所选 base branch：执行 `git fetch`、记录
`preflight.base_freshness`、仅在安全时 fast-forward 本地 base，并在本地 base 与远端
分叉或 freshness 无法确认时 fail closed。不要从过期的本地 `main` / `dev` 创建任务分支。

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

Branch Review Gate 与 publish helper 是内部子命令：

```bash
.trellis/guru-team/scripts/bash/review-branch.sh --json --pass \
  --review-source independent-agent \
  --reviewer "trellis-check-agent" \
  --review-report ".trellis/tasks/<task>/review.md" \
  --summary "中文审查结论" \
  --evidence "已按 intake base 到 HEAD 的完整 diff 覆盖文档、代码、测试、Trellis artifacts、CI/CD、容器、K8s/Kustomize、数据库 migration、Makefile，并判断本次变更的部署影响及是否需要同步修改部署资产"
.trellis/guru-team/scripts/bash/check-review-gate.sh --json
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work
```

用户日常可以直接描述任务、贴 issue URL，或说“处理 issue #123”。AI 依赖
Trellis 自动注入的 startup context、workflow-state、hook breadcrumb 或 skill
matcher 判断是否进入 Guru Team issue intake 和 worktree preflight。

用户常用显式入口保留为 `trellis-continue` 和 `trellis-finish-work`。`trellis-start`
仍保留为 fallback / explicit orientation 入口，用于无自动注入平台、hook 未启用或
未审批、怀疑自动注入没有运行，或需要完整上下文报告和重新加载 Trellis 上下文的场景。

Planning start gate 和 Phase 2 check gate 都需要 task-local evidence。进入实现前先由
AI/human 审查 `prd.md` / `design.md` / `implement.md`，获得用户确认后调用
`record-planning-approval.sh` 写入 `planning-approval.json`，再用
`check-planning-approval.sh` 校验；`task.py start` 只是状态写入，不代表规划已审查。
commit 前必须完成完整 `trellis-check`，再用 `record-phase2-check.sh` 写入
`phase2-check.json` 并用 `check-phase2-check.sh` 校验；几个验证命令通过只是 check
evidence 的一部分，不等于完整 `trellis-check` 覆盖。

Branch Review Gate 必须先由独立 Agent 审查完整 diff，并确认无 P0/P1/P2 finding，再调用
`review-branch.sh` 固化结论。`review-branch.sh` 是 recorder / validator，不是
reviewer；`--pass` 必须先写 task-local `review.md`，再带中文 `--summary`、
至少一条 `--evidence`，以及 `--review-source independent-agent` 和
`--review-report .trellis/tasks/<task>/review.md`。`--reviewer` 只记录身份，不能替代
review report digest；`*-main-session` / `self-review` 不能通过 gate。
Phase 2 的官方 `trellis-check` sub-agent 负责 commit 前质量检查并以
`phase2-check.json` 留痕；Phase 3 Branch Review Gate 可由 sub-agent 辅助审查，但
最终门禁以 `review-gate.json` 为准，且 `review-branch.sh` 会先校验 Phase 2 check evidence。

`trellis-continue` 不得 push 分支、创建 PR、调用 `publish-pr` 或调用
`finish-work`，也不得提交 `review.md` / `review-gate.json` 等 Trellis metadata。
PR 发布只发生在显式 `trellis-finish-work` 入口带
`--from-trellis-finish-work` 意图标记、成功 archive task、记录 journal、提交允许的
Trellis metadata 之后。裸 `finish-work.sh` 和 `publish-pr.sh` 默认拒绝普通直接调用；
只有 `finish-work.sh` 的显式 finish entrypoint 调用或 finish-work 已完成后的显式
recovery/debug flag 可以进入 publish 检查。

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
