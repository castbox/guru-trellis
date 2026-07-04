# Guru Trellis

Guru Team Trellis 的公开 marketplace 与 preset 资产仓库。

本仓库是可复用 `guru-team` Trellis workflow 的 canonical 来源，用于让团队成员在业务仓库中安装统一的 Trellis 工作流、companion scripts 和平台入口 overlay。

## 推荐用法

先确认目标 repo 只使用一个研发 harness。Trellis 不要和 Superpowers、Spec Kit、OpenSpec、GSD 等其它 SDD / agent harness 框架在同一个 repo 中混用；多套 harness 同时存在会让 workflow、task artifact、spec、hooks 和平台入口互相抢控制权，后续 AI 会话也更容易读错上下文。如果目标 repo 已经采用其它 harness，先迁移或清理，再安装 Trellis。

本 README 提供两种安装入口：

- **非交互命令行安装**：适合 throwaway 验证、CI 抽样、或你想自己明确执行每一步。
- **AI 安装 prompt**：适合让 Codex、Cursor 或其它 AI 开发工具在目标业务仓库里完成安装、验证、提交和 push。

团队默认安装和自动验收必须使用非交互 `trellis init` 命令，也就是加 `-y` 或显式指定
`--template <name>`；如果你想手动选择 spec template，可以去掉 `-y`，但那不适合作为自动化验收路径。

### 安装 Trellis

#### 非交互命令行安装

在目标业务仓库根目录执行；先把 `<your-name>` 替换成你的 Trellis 用户名：

```bash
TRELLIS_USER="<your-name>"

npm install -g @mindfoldhq/trellis@latest

trellis init -y -u "$TRELLIS_USER" --codex --cursor \
  --workflow guru-team \
  --workflow-source gh:castbox/guru-trellis/trellis

GURU_TRELLIS_DIR="$(mktemp -d)/guru-trellis"
git clone --depth 1 https://github.com/castbox/guru-trellis.git "$GURU_TRELLIS_DIR"
"$GURU_TRELLIS_DIR/trellis/presets/guru-team/scripts/bash/apply.sh" --repo "$PWD"
```

最小验证：

```bash
trellis --version
test -f .trellis/.version
test -f .trellis/workflow.md
test -x .trellis/guru-team/scripts/bash/check-env.sh
python3 ./.trellis/scripts/get_context.py --mode packages
.trellis/guru-team/scripts/bash/check-env.sh --json
```

如果 `check-env` 输出的 `github_repo` 为空，或 JSON 中出现 `warnings` / `next_steps`，
说明 workflow 还不能可靠执行 GitHub issue intake 或 publish；按提示配置
`.trellis/guru-team/config.yml` 的 `github_repo: owner/repo`，或给当前 Git 仓库配置
GitHub `origin` remote。

本仓库也提供 throwaway 安装验证脚本，用来验证默认非交互路径是否仍可开箱运行：

```bash
./trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
```

Trellis CLI 目前只接受 `gh:user/repo/path` workflow marketplace source；在非 `main`
分支或本地 marketplace 文件有改动时，该脚本会 fail closed，避免把公开远端验证误报为
当前分支验证。需要刻意采样公开 marketplace 时，设置
`TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1`。

#### AI 安装 prompt

把这段 prompt 发给目标业务仓库里的 AI 会话：

```text
在当前 Repo 中安装最新版本的 Trellis。

要求：
- 先实时确认 npm 上 @mindfoldhq/trellis 的 latest 版本，不要凭记忆判断版本。
- 安装前检查当前 Repo 是否已经使用 Superpowers、Spec Kit、OpenSpec、GSD 或其它 SDD / agent harness；如果存在，不要继续安装 Trellis，先报告冲突并让我确认迁移或清理方案。
- 安装/升级全局 Trellis CLI 到 latest。
- 默认只启用 Codex 和 Cursor 支持。
- Trellis 用户名使用 <your-name>，请在执行前把这个占位符替换成你的用户名。
- 如果当前 Repo 还没有 .trellis/，直接用 Guru Team workflow 的非交互命令初始化：`trellis init -y -u <your-name> --codex --cursor --workflow guru-team --workflow-source gh:castbox/guru-trellis/trellis`。
- 如果我明确要求交互式选择 spec template，才可以去掉 `-y`；默认安装和自动验收必须使用 `-y` 或显式 `--template <name>`。
- 获取本公开 preset 仓库的最新内容，例如 clone 到临时目录或复用已有本地副本并 `git pull --ff-only`：`https://github.com/castbox/guru-trellis.git`。
- 执行 `<guru-trellis>/trellis/presets/guru-team/scripts/bash/apply.sh --repo <current-repo>`，把 Guru Team companion assets 和所选平台 overlay 应用到当前 Repo。
- 安装后检查是否存在 `.trellis/tasks/00-bootstrap-guidelines/`。这是 `trellis init` 生成的一次性 Repo 级 spec bootstrap 任务，用于把 `.trellis/spec/` 从通用模板改成当前 Repo 的真实工程规范；它不是每个 task 都要做，也不能作为安装副作用静默完成。先向我说明它的目的、将检查哪些源码/文档、将修改哪些 `.trellis/spec/` 文件，并询问我是现在让 AI 完成，还是保留该 task 后续单独处理。
- 只有在我明确确认现在执行 spec bootstrap 时，才扫描当前 Repo 的真实代码和文档，填充 `.trellis/spec/`、更新 `00-bootstrap-guidelines` checklist，并把这些改动纳入本次安装提交；如果我未确认，不要修改 `.trellis/spec/` 模板内容或 bootstrap task 状态。
- 安装后确认当前 Repo 只保留你选择的平台入口目录；如果出现未选择的平台目录，例如 .claude/、.opencode/、.gemini/、.kiro/、.qoder/、.codebuddy/、.factory/、.pi/、.reasonix/、.kilocode/、.agent/、.devin/、.zcode/、.trae/ 等，说明原因并清理或请我确认。
- 运行最小验证：trellis --version、.trellis/.version、Trellis 上下文读取、Guru Team check-env；如果 check-env 的 `github_repo` 为空或输出 `warnings` / `next_steps`，必须明确报告需要配置 `.trellis/guru-team/config.yml` 或 GitHub origin remote。
- 检查 git diff，确认没有敏感信息、.env、token、私钥或本机-only 身份文件被提交。
- 提交前先做 Git 发布预检：检查当前分支、默认分支、远端、是否可能是受保护分支，以及是否已有未提交用户改动。不要默认直接 push 到 main/master/dev/develop 等共享分支。
- 如果当前分支可能受保护或不适合直接推送，先询问我是在当前分支提交，还是创建单独分支并在完成后 push 分支、创建 PR。
- 按我确认的分支策略提交；只有在确认允许 push 时才 push，只有在确认需要 PR 时才创建 PR。

完成后告诉我：
- 安装到的 Trellis 版本；
- 使用的用户名；
- 实际启用并保留了哪些平台入口；
- 是否发现 `00-bootstrap-guidelines`；是否已获得确认并完成 spec bootstrap，或保留为后续 task；
- 验证命令结果；
- Git 发布预检结论、最终分支、commit hash，以及 push / PR 结果或未 push 的原因。
```

> **NOTE：复制 prompt 前必须先替换占位符。**
>
> - 把 `<your-name>` 替换成你的 Trellis 用户名（建议为姓名全拼）。
> - 如果你不使用默认的 Codex + Cursor，也要先把 prompt 里的平台说明和 `trellis init` 平台参数改成你实际使用的 AI 开发工具，例如 Claude、OpenCode、Gemini、Copilot 等。

### 升级 Trellis

把这段 prompt 发给已经安装 Trellis 的目标业务仓库里的 AI 会话：

```text
在当前 Repo 中升级 Trellis 和 Guru Team Trellis workflow/preset。

要求：
- 先实时确认 npm 上 @mindfoldhq/trellis 的 latest 版本，并检查当前 trellis --version、which -a trellis、npm list -g @mindfoldhq/trellis --depth=0。
- 升级前检查当前 Repo 是否同时存在 Superpowers、Spec Kit、OpenSpec、GSD 或其它 SDD / agent harness；如果存在，不要继续升级 Trellis，先报告冲突并让我确认迁移或清理方案。
- 如果本机 Trellis CLI 不是 latest，安装/升级到 @mindfoldhq/trellis@latest。
- 默认只保留当前 Repo 的 Codex 和 Cursor 支持。
- 当前 Repo 已有 .trellis/ 时，先用 Guru Team marketplace 生成 workflow 预览：`trellis workflow --marketplace gh:castbox/guru-trellis/trellis --template guru-team --create-new`，再对比现有 `.trellis/workflow.md` 和 `.trellis/workflow.md.new`；确认风险后运行 `trellis workflow --marketplace gh:castbox/guru-trellis/trellis --template guru-team` 切换 active workflow。
- 获取本公开 preset 仓库的最新内容，例如 clone 到临时目录或复用已有本地副本并 `git pull --ff-only`：`https://github.com/castbox/guru-trellis.git`。
- 执行 `<guru-trellis>/trellis/presets/guru-team/scripts/bash/apply.sh --repo <current-repo>`，重新应用 Guru Team companion assets 和所选平台 overlay。
- 如果 preset 生成 .new 或 .bak，逐个检查原因；不要静默覆盖未知本地改动。
- 升级流程不要重新静默执行 spec bootstrap。若发现 `.trellis/tasks/00-bootstrap-guidelines/` 仍处于 active，或 `.trellis/spec/` 仍是通用模板，先报告这是尚未完成的一次性 Repo 级 bootstrap，并询问是否单独处理；未确认前不要修改 `.trellis/spec/` 模板内容或 bootstrap task 状态。
- 升级后确认当前 Repo 只保留你选择的平台入口目录；如果出现未选择的平台目录，例如 .claude/、.opencode/、.gemini/、.kiro/、.qoder/、.codebuddy/、.factory/、.pi/、.reasonix/、.kilocode/、.agent/、.devin/、.zcode/、.trae/ 等，说明原因并清理或请我确认。
- 运行最小验证：trellis --version、.trellis/.version、Trellis 上下文读取、Guru Team check-env。
- 检查 git diff，确认没有敏感信息、.env、token、私钥或本机-only 身份文件被提交。
- 提交前先做 Git 发布预检：检查当前分支、默认分支、远端、是否可能是受保护分支，以及是否已有未提交用户改动。不要默认直接 push 到 main/master/dev/develop 等共享分支。
- 如果当前分支可能受保护或不适合直接推送，先询问我是在当前分支提交，还是创建单独分支并在完成后 push 分支、创建 PR。
- 按我确认的分支策略提交；只有在确认允许 push 时才 push，只有在确认需要 PR 时才创建 PR。

完成后告诉我：
- 升级前后的 Trellis 版本；
- workflow/preset 是否已重新应用；
- 实际启用并保留了哪些平台入口；
- 是否产生 .new 或 .bak 以及处理结果；
- 是否发现未完成的 `00-bootstrap-guidelines`，以及是否保留为后续单独处理；
- 验证命令结果；
- Git 发布预检结论、最终分支、commit hash，以及 push / PR 结果或未 push 的原因。
```

> **NOTE：复制 prompt 前必须先确认平台范围。**
>
> - 默认升级 prompt 只保留 Codex + Cursor。
> - 如果你的 repo 使用其它 AI 开发工具，要先把平台说明改成实际需要的平台入口，例如 Claude、OpenCode、Gemini、Copilot 等，再执行升级。

## 如何完成 Spec Bootstrap

`trellis init` 可能会生成 `.trellis/tasks/00-bootstrap-guidelines/`。这是安装
Trellis 后的一次性 Repo 初始化步骤，不是每个需求都要做的 task。

Spec bootstrap 的目标是让 AI 先读当前 Repo 已经存在的 README、设计文档、目录结构、
源码、测试、脚本和配置，再把 `.trellis/spec/` 从通用模板改写成这个 Repo 的真实工程
规范。完成后，后续日常开发 task 只需要读取这些 spec；只有项目约定发生变化或踩到可复用
问题时，才做小范围 spec update。

建议在新 Repo 安装 Trellis 后、开始第一个正式开发 task 前完成 bootstrap。升级已有
Repo 时不要默认重做；只有发现 `00-bootstrap-guidelines` 仍未完成，或 `.trellis/spec/`
明显还是通用模板时，才单独处理。

如果你想现在完成 bootstrap，把下面这段 prompt 发给目标 Repo 里的 AI 会话：

```text
请处理 Trellis 的一次性 spec bootstrap。

要求：
- 先检查 `.trellis/tasks/00-bootstrap-guidelines/` 和 `.trellis/spec/` 当前状态。
- 先不要修改文件；先说明为什么需要 bootstrap、计划读取哪些 README / docs / source / tests / scripts / config，以及预计会新增、删除或改写哪些 `.trellis/spec/` 文件。
- 等我明确确认“现在执行 spec bootstrap”后，再扫描 Repo 并更新 `.trellis/spec/`。
- 更新完成后，同步更新 `00-bootstrap-guidelines` task 状态或 checklist，运行 Trellis context/task 校验，展示 changed files 和验证结果。
- 提交前检查 diff，确认没有 `.env`、token、私钥、本机-only 配置或无关运行态文件。
- 未经我确认，不要 push 到共享分支。
```

如果你暂时不想做 bootstrap，可以保留 `00-bootstrap-guidelines`，后续再单独让 AI 处理。
不要把未确认的 spec bootstrap 混进普通功能开发提交里。

## 仓库内容

- `trellis/index.json`：Trellis marketplace 入口，提供 `guru-team` workflow。
- `trellis/workflows/guru-team/`：workflow 主合同、配置模板、schema 和 companion scripts。
- `trellis/presets/guru-team/`：把 companion scripts 和平台入口 overlay 安装到目标业务仓库的 preset installer。

## 日常入口

安装后，用户日常不需要先手动输入 `trellis-start`。直接描述任务、贴 GitHub
issue URL，或说“处理 issue #123”即可；AI 会根据 Trellis 自动注入的
startup context、workflow-state、hook breadcrumb 或 skill matcher 判断是否进入
Guru Team issue intake 和 worktree preflight。

默认 `prepare-task.sh --json` 只是 intake/preflight planner：它可以读取明确提供的
issue、搜索重复候选，并输出 proposed issue、base branch、branch name、workspace
path 和 create-task command，但不会创建 GitHub issue、worktree、branch 或 Trellis
task，也不会在未确认 source issue 时写 `.trellis/guru-team/handoff.json`。没有 source
issue 的 freeform 请求必须先由 AI 展示 proposed issue title/body 和 duplicate
evidence；stdout JSON 会标记 `handoff_written: false`。用户确认后才可用
`--create-issue-confirmed --issue-title ... --issue-body-file ...` 执行 GitHub issue
创建；`--create-worktree` / `--create-task` 同样只用于 handoff review 之后的显式执行。
这些 executor 路径创建 worktree 前会先刷新所选 base branch，记录
`preflight.base_freshness`，并在本地 base 落后时只做安全 fast-forward；如果本地 base
与远端分叉或 freshness 无法确认，会阻塞而不是从过期 ref 创建任务分支。

`no_task` 下不是绝对禁止当前 checkout 直接修改，但这只能作为用户显式批准的 override：
用户必须明确表示本轮跳过创建或复用 GitHub issue、Trellis task、worktree 和 branch。
AI 在改文件前要说明将跳过哪些 artifact、当前 checkout / branch / dirty state、预期
副作用和 changed-file scope；这个批准不包含 commit、push、PR 或 issue close。

用户仍然需要记住的常用显式入口是：

- `trellis-continue`
- `trellis-finish-work`

`trellis-start` 仍保留为 fallback / explicit orientation 入口，用于平台没有自动
session/startup 注入、hook 未启用或未审批、怀疑自动注入没有运行，或用户需要完整
上下文报告和重新加载 Trellis 上下文的场景。

`record-planning-approval`、`check-planning-approval`、`record-phase2-check`、
`check-phase2-check`、`review-branch`、`check-review-gate`、`publish-pr` 是 workflow
内部 companion script，不是需要用户日常手动记忆的新主流程。
`record-planning-approval.sh` / `check-planning-approval.sh` 在 `task.py start` 前记录并
校验规划审查证据；`task.py start` 只写状态，不代表规划已审查。
`record-phase2-check.sh` / `check-phase2-check.sh` 在 commit 前记录并校验完整
`trellis-check` 证据；验证命令只是 report 中的一部分，不等于完整 check 覆盖。
Codex 项目默认使用 `codex.dispatch_mode: sub-agent`，由 main session 调度
`trellis-implement` / `trellis-check`；sub-agent 通过 dispatch prompt 首行
`Active task: <task path>` 或 `task.py current --source` 加载上下文。只有显式配置
`codex.dispatch_mode: inline` 时，Codex 才降级为 main session 直接实现和检查。
`review-branch.sh` 只记录和校验已经
完成的 AI/human review 结论，不替代真正的文档 + 代码 review。通过 gate 必须先写
task-local `review.md`，且该 report 必须来自独立 Agent 审查并确认无 P0/P1/P2
finding；再用 `--review-source independent-agent` 和
`--review-report .trellis/tasks/<task>/review.md` 让 `review-gate.json` 记录来源与
digest。`--reviewer` 只记录身份，不能单独作为通过证据；`*-main-session` /
`self-review` 不能通过 gate。
`finish-work.sh` 和 `publish-pr.sh` 默认拒绝普通直接调用，避免
`trellis-continue` 链式执行 closeout、提交 review metadata，或在未完成显式
`trellis-finish-work` 时提前 push 分支并创建 PR；日常发布必须由 `trellis-finish-work` 入口带
`--from-trellis-finish-work` 意图标记，在 archive task、记录 journal 并提交允许的
Trellis metadata 之后内部触发。只有 finish-work 已完成但 publish 需要重试时，才使用
显式 recovery/debug flag。

`finish-work.sh --dry-run --from-trellis-finish-work` 是无副作用 readiness preview：
只校验 gate、dirty state 和 PR body/readiness，并输出将要 archive、journal、
metadata commit 与 publish 的计划；不会移动 task、写 journal、创建 commit、push 或创建 PR。

发布前 AI 必须生成或审查 PR body readiness。PR body 面向不了解 Trellis task 的
GitHub reviewer，而不是 Trellis session 内部摘要；应包含具体的 `变更摘要`、
`影响范围`、`验证结果`、`Review Gate`、`Issue 关闭范围` 和 `安全说明`。禁止用
“当前 Trellis task”“已提交实现与文档更新”“详见 artifact”作为主要摘要。
non-draft publish 必须把 AI 审阅后的 Markdown 通过 `--body-file <path>` 传给内部
publish，或用 `--body-artifact <path>` 传 readiness artifact；脚本只校验客观结构、
低信息量短语、close/ref 语义和 reviewed source 是否存在，不替代 AI 判断内容是否真实充分。
这些 readiness/body 文件属于 task metadata，通常写在当前 task 目录，`finish-work`
archive 后从归档 task artifact 读取最终 PR body；脚本生成的 `generated` body 只用于
draft/preview 辅助，不能作为 non-draft 发布证据。

## 维护原则

- 不修改 Trellis npm 全局包、`node_modules` 或上游 Trellis 源码。
- 不把业务仓库的私有规则写入通用 workflow。
- 中台知识检索和 durable docs SSOT 对齐规则维护在通用 workflow 中，具体业务仓库只保留 task 证据和必要的 docs 更新。
- 长期规则维护在本仓库的 marketplace workflow、preset、companion scripts 和 overlay 中。
- 目标业务仓库中的 generated copy 只是安装结果，不作为长期维护源。
- 修改 `trellis/presets/guru-team/overlays/` 后，先重新应用 preset 到本仓库 dogfood copy，再运行 drift check：

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

如果 preset 产生 `.new` 或 `.bak`，必须逐个检查原因并处理，不能静默提交。
