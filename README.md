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

npm install -g @mindfoldhq/trellis@0.6.5

trellis init -y -u "$TRELLIS_USER" --codex --cursor \
  --workflow guru-team \
  --workflow-source gh:castbox/guru-trellis/trellis#v0.6.5-guru.3

GURU_TRELLIS_DIR="$(mktemp -d)/guru-trellis"
git clone --depth 1 --branch v0.6.5-guru.3 \
  https://github.com/castbox/guru-trellis.git "$GURU_TRELLIS_DIR"
"$GURU_TRELLIS_DIR/trellis/presets/guru-team/scripts/bash/apply.sh" \
  --repo "$PWD" \
  --platform codex \
  --platform cursor
```

最小验证：

```bash
trellis --version
test -f .trellis/.version
test -f .trellis/workflow.md
test -f .trellis/guru-team/extension.json
test -x .trellis/guru-team/scripts/bash/check-env.sh
test -x .trellis/guru-team/scripts/bash/version.sh
python3 ./.trellis/scripts/get_context.py --mode packages
.trellis/guru-team/scripts/bash/check-env.sh --json
.trellis/guru-team/scripts/bash/version.sh --json
```

如果 `check-env` 输出的 `github_repo` 为空，或 JSON 中出现 `warnings` / `next_steps`，
说明 workflow 还不能可靠执行 GitHub issue intake 或 publish；按提示配置
`.trellis/guru-team/config.yml` 的 `github_repo: owner/repo`，或给当前 Git 仓库配置
GitHub `origin` remote。

`trellis --version` 与 `.trellis/.version` 表示官方 Trellis CLI / project template
版本；Guru Team extension 的版本和安装来源记录在
`.trellis/guru-team/extension.json`，并由 `check-env --json` 与 `version.sh --json`
输出。

默认安装命令同时 pin 官方 Trellis CLI `@0.6.5` 和 Guru Team repo release tag
`#v0.6.5-guru.3`，用于可复现的稳定安装。维护者刻意采样最新 `main` / canary
时，可以去掉 `#ref` 或设置其它 branch/tag ref，但最终报告必须说明安装来源是
mutable ref 还是 immutable release tag，以及是否仍以官方 Trellis `0.6.5` 为目标基线。

本仓库也提供 throwaway 安装验证脚本，用来验证默认非交互路径是否仍可开箱运行：

```bash
./trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
```

Trellis CLI 支持 `gh:user/repo/path#ref` workflow marketplace source。该脚本默认验证
`gh:castbox/guru-trellis/trellis#v0.6.5-guru.3`；需要验证其它 branch/tag 时，设置
`TRELLIS_WORKFLOW_SOURCE` 为对应 `#ref`。如果使用不带 `#ref` 的公开远端 source，在非
`main` 分支或本地 marketplace 文件有改动时，该脚本会 fail closed，避免把公开远端验证
误报为当前分支验证。需要刻意采样公开 latest/canary marketplace 时，设置
`TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1`，并在结果中说明这不是当前分支或 release tag
验证。

#### AI 安装 prompt

把这段 prompt 发给目标业务仓库里的 AI 会话：

```text
在当前 Repo 中安装官方 Trellis CLI v0.6.5，并安装 Guru Team extension stable v0.6.5-guru.3。

要求：
- 先实时确认 npm 上 @mindfoldhq/trellis 的 latest 版本，不要凭记忆判断版本；如果 latest 已不是 0.6.5，本次仍按 Guru Team stable v0.6.5-guru.3 的目标基线安装 @mindfoldhq/trellis@0.6.5，除非我明确要求升级官方 Trellis 基线。
- 安装前检查当前 Repo 是否已经使用 Superpowers、Spec Kit、OpenSpec、GSD 或其它 SDD / agent harness；如果存在，不要继续安装 Trellis，先报告冲突并让我确认迁移或清理方案。
- 安装/升级全局 Trellis CLI 到 @mindfoldhq/trellis@0.6.5。
- 默认只启用 Codex 和 Cursor 支持。
- Trellis 用户名使用 <your-name>，请在执行前把这个占位符替换成你的用户名。
- 如果当前 Repo 还没有 .trellis/，直接用 Guru Team workflow 的稳定非交互命令初始化：`trellis init -y -u <your-name> --codex --cursor --workflow guru-team --workflow-source gh:castbox/guru-trellis/trellis#v0.6.5-guru.3`。
- 如果我明确要求交互式选择 spec template，才可以去掉 `-y`；默认安装和自动验收必须使用 `-y` 或显式 `--template <name>`。
- 获取与 workflow source 相同 release tag 的公开 preset 仓库内容，例如 `git clone --depth 1 --branch v0.6.5-guru.3 https://github.com/castbox/guru-trellis.git <guru-trellis>`。只有明确要跟随 latest/canary 时，才复用 `main` 或不带 `#ref` 的远端 source，并在最终报告中说明来源是 mutable ref。
- 执行 `<guru-trellis>/trellis/presets/guru-team/scripts/bash/apply.sh --repo <current-repo> --platform codex --platform cursor`，把 Guru Team companion assets 和所选平台 overlay 应用到当前 Repo；如需 Claude，改为追加 `--platform claude`，如需历史全量 overlay，改用 `--all-platforms`。
- 安装后检查是否存在 `.trellis/tasks/00-bootstrap-guidelines/`。这是 `trellis init` 生成的一次性 Repo 级 spec bootstrap 任务，用于把 `.trellis/spec/` 从通用模板改成当前 Repo 的真实工程规范；它不是每个 task 都要做，也不能作为安装副作用静默完成。先向我说明它的目的、将检查哪些源码/文档、将修改哪些 `.trellis/spec/` 文件，并询问我是现在让 AI 完成，还是保留该 task 后续单独处理。
- 业务项目内人类可读文档默认使用中文：`.trellis/spec/**`、`.trellis/tasks/**`、`docs/**` durable docs、`00-bootstrap-guidelines` 创建或补齐的 docs SSOT，以及 workflow artifact 的 summary/evidence/finding/PR title/body 等字段都写中文；命令、路径、配置键、GitHub keyword、API 名称、代码符号等 literal token 可保留英文。
- 只有在我明确确认现在执行 spec bootstrap 时，才扫描当前 Repo 的真实代码和文档，填充 `.trellis/spec/`、更新 `00-bootstrap-guidelines` checklist，并把这些改动纳入本次安装提交；如果我未确认，不要修改 `.trellis/spec/` 模板内容或 bootstrap task 状态。bootstrap 过程中如创建或补齐 `docs/**` SSOT 主文档，也必须按业务项目中文规则写作。
- 安装后确认 preset installer 没有创建未选择的平台入口目录；默认 Codex + Cursor 安装不应创建 `.claude/`。如果目标 Repo 历史上已经存在未选择的平台目录，例如 .claude/、.opencode/、.gemini/、.kiro/、.qoder/、.codebuddy/、.factory/、.pi/、.reasonix/、.kilocode/、.agent/、.devin/、.zcode/、.trae/ 等，说明这是历史残留或其它工具创建，并先请我确认是否清理。
- 运行最小验证：trellis --version、.trellis/.version、Trellis 上下文读取、Guru Team check-env、`.trellis/guru-team/extension.json`、Guru Team version；如果 check-env 的 `github_repo` 为空或输出 `warnings` / `next_steps`，必须明确报告需要配置 `.trellis/guru-team/config.yml` 或 GitHub origin remote。
- 检查 git diff，确认没有敏感信息、.env、token、私钥或本机-only 身份文件被提交。
- 提交前先做 Git 发布预检：检查当前分支、默认分支、远端、是否可能是受保护分支，以及是否已有未提交用户改动。不要默认直接 push 到 main/master/dev/develop 等共享分支。
- 如果当前分支可能受保护或不适合直接推送，先询问我是在当前分支提交，还是创建单独分支并在完成后 push 分支、创建 PR。
- 按我确认的分支策略提交；只有在确认允许 push 时才 push，只有在确认需要 PR 时才创建 PR。

完成后告诉我：
- 安装到的官方 Trellis 版本；
- 安装到的 Guru Team extension 版本、target Trellis CLI、source ref / commit、source tree state，以及是否来自 mutable ref；
- 使用的用户名；
- 实际启用并保留了哪些平台入口；
- 是否发现 `00-bootstrap-guidelines`；是否已获得确认并完成 spec bootstrap，或保留为后续 task；
- 验证命令结果；
- Git 发布预检结论、最终分支、commit hash，以及 push / PR 结果或未 push 的原因。
```

> **NOTE：复制 prompt 前必须先替换占位符。**
>
> - 把 `<your-name>` 替换成你的 Trellis 用户名（建议为姓名全拼）。
> - 如果你不使用默认的 Codex + Cursor，也要先把 prompt 里的平台说明、`trellis init` 平台参数和 `apply.sh --platform ...` 参数改成你实际使用的 AI 开发工具，例如 Claude、OpenCode、Gemini、Copilot 等。

### 升级 Trellis

把这段 prompt 发给已经安装 Trellis 的目标业务仓库里的 AI 会话：

```text
在当前 Repo 中升级 Trellis 和 Guru Team Trellis workflow/preset。

要求：
- 先实时确认 npm 上 @mindfoldhq/trellis 的 latest 版本，并检查当前 trellis --version、which -a trellis、npm list -g @mindfoldhq/trellis --depth=0；如果 latest 已不是 0.6.5，本次仍按 Guru Team stable v0.6.5-guru.3 的目标基线安装 @mindfoldhq/trellis@0.6.5，除非我明确要求升级官方 Trellis 基线。
- 升级前检查当前 Repo 是否同时存在 Superpowers、Spec Kit、OpenSpec、GSD 或其它 SDD / agent harness；如果存在，不要继续升级 Trellis，先报告冲突并让我确认迁移或清理方案。
- 如果本机 Trellis CLI 不是 0.6.5，安装/升级到 @mindfoldhq/trellis@0.6.5。
- 默认只保留当前 Repo 的 Codex 和 Cursor 支持。
- 当前 Repo 已有 .trellis/ 时，先用 Guru Team stable marketplace 生成 workflow 预览：`trellis workflow --marketplace gh:castbox/guru-trellis/trellis#v0.6.5-guru.3 --template guru-team --create-new`，再对比现有 `.trellis/workflow.md` 和 `.trellis/workflow.md.new`；确认风险后运行 `trellis workflow --marketplace gh:castbox/guru-trellis/trellis#v0.6.5-guru.3 --template guru-team` 切换 active workflow。
- 获取与 workflow source 相同 release tag 的公开 preset 仓库内容，例如 `git clone --depth 1 --branch v0.6.5-guru.3 https://github.com/castbox/guru-trellis.git <guru-trellis>`。只有明确要跟随 latest/canary 时，才复用 `main` 或不带 `#ref` 的远端 source，并在最终报告中说明来源是 mutable ref。
- 执行 `<guru-trellis>/trellis/presets/guru-team/scripts/bash/apply.sh --repo <current-repo> --platform codex --platform cursor`，重新应用 Guru Team companion assets 和所选平台 overlay；如需 Claude，改为追加 `--platform claude`，如需历史全量 overlay，改用 `--all-platforms`。
- 如果 preset 生成 .new 或 .bak，逐个检查原因；不要静默覆盖未知本地改动。
- 业务项目内人类可读文档默认使用中文：`.trellis/spec/**`、`.trellis/tasks/**`、`docs/**` durable docs、`00-bootstrap-guidelines` 创建或补齐的 docs SSOT，以及 workflow artifact 的 summary/evidence/finding/PR title/body 等字段都写中文；命令、路径、配置键、GitHub keyword、API 名称、代码符号等 literal token 可保留英文。
- 升级流程不要重新静默执行 spec bootstrap。若发现 `.trellis/tasks/00-bootstrap-guidelines/` 仍处于 active，或 `.trellis/spec/` 仍是通用模板，先报告这是尚未完成的一次性 Repo 级 bootstrap，并询问是否单独处理；未确认前不要修改 `.trellis/spec/` 模板内容或 bootstrap task 状态。
- 升级后确认 preset installer 没有创建或恢复未选择的平台入口目录；默认 Codex + Cursor 升级不应创建 `.claude/`。如果目标 Repo 历史上已经存在未选择的平台目录，例如 .claude/、.opencode/、.gemini/、.kiro/、.qoder/、.codebuddy/、.factory/、.pi/、.reasonix/、.kilocode/、.agent/、.devin/、.zcode/、.trae/ 等，说明这是历史残留或其它工具创建，并先请我确认是否清理。
- 运行最小验证：trellis --version、.trellis/.version、Trellis 上下文读取、Guru Team check-env、`.trellis/guru-team/extension.json`、Guru Team version。
- 检查 git diff，确认没有敏感信息、.env、token、私钥或本机-only 身份文件被提交。
- 提交前先做 Git 发布预检：检查当前分支、默认分支、远端、是否可能是受保护分支，以及是否已有未提交用户改动。不要默认直接 push 到 main/master/dev/develop 等共享分支。
- 如果当前分支可能受保护或不适合直接推送，先询问我是在当前分支提交，还是创建单独分支并在完成后 push 分支、创建 PR。
- 按我确认的分支策略提交；只有在确认允许 push 时才 push，只有在确认需要 PR 时才创建 PR。

完成后告诉我：
- 升级前后的官方 Trellis 版本；
- 升级前后的 Guru Team extension 版本、target Trellis CLI、source ref / commit、source tree state，以及是否来自 mutable ref；
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
> - 如果你的 repo 使用其它 AI 开发工具，要先把平台说明和 `apply.sh --platform ...` 参数改成实际需要的平台入口，例如 Claude、OpenCode、Gemini、Copilot 等，再执行升级。

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
- 本业务项目内 `.trellis/spec/**`、`.trellis/tasks/**`、`docs/**` durable docs 和 bootstrap 创建或补齐的 docs SSOT 人类可读内容默认写中文；命令、路径、配置键、GitHub keyword、API 名称、代码符号等 literal token 可保留英文。
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

## Guru Team Extension Version

Guru Team extension 是本仓库在官方 Trellis 之上提供的团队扩展包。它与官方
`@mindfoldhq/trellis` CLI 版本分开治理：

- `trellis --version`：官方 Trellis CLI 版本；
- `.trellis/.version`：目标 repo 当前 Trellis project template 版本；
- `trellis/index.json` 的 `version: 1`：Trellis marketplace index schema version；
- `trellis/guru-team-extension.json`：Guru Team extension 的 canonical release 版本和
  target Trellis CLI；
- `.trellis/guru-team/extension.json`：目标 repo 当前安装的 Guru Team extension version
  和 source provenance。

Guru Team extension 的 public API 包括 `guru-team` workflow template id、`.trellis/guru-team/`
managed assets、companion script CLI、config keys、JSON artifact / check-env fields、platform
overlay entrypoints，以及 `.new` / `.bak` conflict handling。Guru Team release 版本以官方
Trellis CLI 版本为前缀，并追加 Guru 修订号：

```text
v<official-trellis-version>-guru.<revision>
```

例如 `v0.6.5-guru.3` 表示“针对官方 Trellis `0.6.5` 的 Guru Team 第 3 个稳定修订”。
同一个官方 Trellis 基线下，Guru Team 可用 `.2`、`.3` 递增发布兼容修订；只有切换官方
Trellis 基线时才移动前缀，例如未来的 `v0.6.6-guru.1`。

Guru 修订号按兼容性维护：

- patch：兼容 bugfix、文档澄清、非破坏性 guardrail 修正；
- minor：兼容新增字段、script 能力、platform overlay 或可选门禁；
- major：破坏 workflow id、script CLI、artifact schema、installed path、默认行为或升级语义。

本仓库的 release tag 使用 repo 级 tag，例如 `v0.6.5-guru.3`。tag 名称必须与
`trellis/guru-team-extension.json.version` 对应；该 manifest 同时用 `target_trellis_cli`
记录目标官方 Trellis CLI 版本。稳定安装文档使用
`gh:castbox/guru-trellis/trellis#v0.6.5-guru.3`。不带 `#ref` 的
`gh:castbox/guru-trellis/trellis` 只表示 latest/canary，不应用作需要复现的问题定位坐标。
发布顺序必须是：先 merge 包含 manifest/docs 更新的 PR，再在 merge commit 上创建并 push
annotated tag `v0.6.5-guru.3` 这类 release tag，验证 `trellis init` / `trellis workflow`
的 tag-pinned 安装后，再退休旧 tag 名称。

`apply.sh` 每次安装/升级都会写入 `.trellis/guru-team/extension.json`。该文件记录
extension version、target Trellis CLI、workflow template id、source repo/ref/commit、source
tree state、selected platforms 和安装时间。`source.commit` / `source.tree_state` 表示 installer 运行时观测到的
Guru Team extension source 快照；在本仓库 dogfood 提交中，它不是“该 installed manifest
自身所在提交”的自指证明。脚本只记录事实；是否升级、回滚或关闭 issue 仍由 AI/human
review 根据证据判断。

## 日常入口

安装后，用户日常不需要先手动输入 `trellis-start`。直接描述任务、贴 GitHub
issue URL，或说“处理 issue #123”即可；AI 会根据 Trellis 自动注入的
startup context、workflow-state、hook breadcrumb 或 skill matcher 判断是否进入
Guru Team issue intake 和 worktree preflight。对 issue-backed、task-like 或需要文件
修改的请求，第一跳不是裸 `task.py create`，而是：

```bash
.trellis/guru-team/scripts/bash/check-env.sh --json
.trellis/guru-team/scripts/bash/prepare-task.sh --json "<user request or issue URL>"
```

默认 `prepare-task.sh --json` 只是 intake/preflight planner：它可以读取明确提供的
issue、搜索重复候选，并输出 proposed issue、base branch、branch name、workspace
path、create-task command 和 `naming_quality`，但不会创建 GitHub issue、worktree、
branch 或 Trellis task，也不会在未确认 source issue 时写
task-local `.trellis/tasks/<task-slug>/task-start-context.json` and gitignored `.trellis/.runtime/guru-team/**` mappings。没有 source issue 的 freeform 请求必须先由 AI 展示
proposed issue title/body、duplicate evidence 和 naming quality；planner 输出不会写
task context 或 runtime cache。用户确认后才可用
`--create-issue-confirmed --issue-title ... --issue-body-file ...` 执行 GitHub issue
创建；`--create-worktree` / `--create-task` 同样只用于 intake plan review 之后的显式执行。
当 `workspace_mode: worktree` 时，执行环境和 task 创建应通过
`prepare-task --create-worktree --create-task` 或等价 Guru Team 受控入口完成，不能把
task creation consent 当成在 source checkout 直接运行 `task.py create` 的批准。
AI 在读取 issue 后应生成语义英文 short-name，并用 `--short-name`、
`--workspace-slug`、`--task-slug`，必要时用 `--branch` 覆盖 prepare 脚本。推荐
worktree/task slug 格式是 `NNN-business-capability`；未显式传 `--branch` 时，branch
格式是 `<branch-type>/NNN-business-capability`，其中 `branch-type` 只能是 `feat`、
`fix`、`refactor`、`perf`、`test`、`docs`、`style`、`build`、`ci`、`chore`、
`revert`，未知语义 fallback 为 `chore`，例如
`feat/052-resume-detail-inline-attachment-preview`。中文或非 ASCII 标题不依赖拼音
transliteration 作为默认分支名；脚本不做智能翻译，只做确定性类型判定、拼装、冲突检查和
低信息命名门禁。低信息名称如 `issue-52`、`52-issue-52`、纯编号或仅包含 `bug` / `fix` /
`task` / `work` / `update` / `change` 等通用词时，executor 路径会在创建 worktree、
branch 或 Trellis task 前阻断。
这些 executor 路径创建 worktree 前会先刷新所选 base branch，记录
`preflight.base_freshness`，并在本地 base 落后时只做安全 fast-forward；如果本地 base
与远端分叉或 freshness 无法确认，会阻塞而不是从过期 ref 创建任务分支。

executor handoff 写入后，`workspace_mode: worktree` 下的
`handoff.workspace_path` 是 task artifact 写入边界。AI 或 main session 在写入/校验
`planning-approval.json`、`phase2-check.json`、`agent-assignment.json`、`reviews/*.md`、
`review.md`、`review-gate.json` 等 task-local artifact 前，应从目标 worktree 运行：

```bash
.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task <task-path>
```

该 helper 只报告 expected workspace、actual repo root、source checkout status、task
worktree status 和 source checkout 中可疑同名 task artifact/review metadata；它不判断
sub-agent 是否 stale，不迁移误写 patch，也不清理 source checkout。若编辑工具不能显式传入
`workdir`，task artifact 或 patch 路径必须使用 handoff `workspace_path` 下的绝对路径。
这层 workspace boundary 是 #76 liveness checker 的 source/task 双侧事实层；source
checkout 出现新的 `HEAD`、dirty status、diff stat 或 mtime 变化时，checker 输出
`workspace_boundary_violation_progress`，不把它当作 stale 证据。

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

`check-workspace-boundary`、`resolve-human-artifacts`、`record-planning-approval`、`check-planning-approval`、`record-phase2-check`、
`check-phase2-check`、`record-agent-assignment`、`record-subagent-liveness-event`、`check-subagent-liveness`、`check-agent-assignment`、
`review-branch`、`check-review-gate`、`publish-pr` 是 workflow
内部 companion script，不是需要用户日常手动记忆的新主流程。
`record-planning-approval.sh` / `check-planning-approval.sh` 在 `task.py start` 前记录并
校验规划审查证据：主会话必须先完成 planning artifact ambiguity review，再展示
`prd.md`、`design.md`、`implement.md` 三个 task-local 链接，并在用户看到后获得
`explicit-post-planning-review` 确认；artifact 必须是 schema 1.2，包含 passed
`ambiguity_review` evidence。Phase 0 handoff 确认、旧 schema/source 或缺失/non-passed
ambiguity evidence 不能通过 gate。校验 freshness 绑定三份规划文档内容 digest；实现提交后的
HEAD drift、metadata tail 或无关 dirty paths 不会单独使 approval stale。`task.py start`
只写状态，不代表规划已审查。
`resolve-human-artifacts.sh` 为阶段回复提供确定性路径事实：规划停止、Phase 2 完成、
Branch Review Gate 结果、finish-work dry-run 和最终 archive/publish 回复都应先运行它，
然后输出 `Markdown 产物 review 表`。标准表只列 `prd.md`、`design.md`、
`implement.md`、`review.md`、`pr-body.md` 五个 Markdown；缺失文件不生成 Markdown
链接，`phase2-check.json`、`review-gate.json`、`agent-assignment.json` 等 JSON
证据不进入默认表。
`record-phase2-check.sh` / `check-phase2-check.sh` 在 commit 前记录并校验完整
`trellis-check` 证据；验证命令只是 report 中的一部分，不等于完整 check 覆盖。
Codex 项目默认使用 `codex.dispatch_mode: sub-agent`，由 main session 调度
`trellis-implement` / `trellis-check`；sub-agent 通过 dispatch prompt 首行
`Active task: <task path>` 或 `task.py current --source` 加载上下文。默认 sub-agent
mode 下有三个强制执行边界：实现由 `trellis-implement` / channel `implement`
完成并输出实现 handoff；Phase 2 check 由 `trellis-check` / channel `check`
完成并输出可支撑 `phase2-check.json` 的 evidence；commit 后 Branch Review 由独立
review sub-agent 审查完整 `origin/<base>...HEAD` diff 并产出 task-local
`reviews/*.md` raw reports 与最终 `review.md` rollup。main session 只协调、等待/恢复/替换、记录 evidence、commit 和运行
recorder/validator；不能把自己的实现、自检、自审或脚本校验通过冒充上述 sub-agent
边界。只有显式配置 `codex.dispatch_mode: inline` 或已有明确 artifact evidence 的
self-exemption 时，Codex 才降级为 main session 直接实现和检查；缺少 implement/check/review
sub-agent evidence 时默认 fail closed。
Guru Team preset 会安装项目级 agent 定义：Codex agent 保持 `trellis-implement` /
`trellis-check` / `trellis-research` 技术标识，使用中文 `description`。当前 Codex
官方 `nickname_candidates` 只能使用 ASCII 字符；中文候选会让 Codex 忽略 agent 文件，
因此 Codex nickname 候选保持 ASCII。Cursor / Claude / channel runtime agent 保持技术
`name`，用中文 description 和标题展示。不要为了中文 UI 改掉这些调度 id。
sub-agent 流程身份使用 task-local `agent-assignment.json` 记录：`logical_role`
是中文 Trellis 逻辑角色，`agent_id` 是技术身份，`platform_nickname` 只是 UI 展示名，
优先记录中文 UI 昵称；平台只给随机/自动昵称或受 ASCII 限制时记录原始值。无论哪种都不参与 gate 判断。
实现、阶段二检查、问题发现审查、问题闭环审查和最终放行审查都应按中文角色留痕；
review round 还必须通过 `--review-round-report <task-local reviews/*.md>`
记录本轮 raw report 的 path、sha256、size 和 modified_at。脚本只校验 JSON、枚举、HEAD 和 digest，不决定该复用哪个 agent。
`wait_agent`、`trellis channel wait` 或等价等待命令 timeout 只表示本次等待窗口没有拿到
最终完成事件，不代表 sub-agent 卡死、失败或应该收口。主会话必须用
`record-subagent-liveness-event.sh` 记录 `assigned` 和非机器可读公开 progress，再按
`check-subagent-liveness.sh` 的唯一 decision 推进。默认 `progress_scan_interval=120s`
只是扫描间隔；`max_progress_silence=180s` 从 `progress_anchor_at` 起算。只有
`status_request_required` 授权发送一次 status request；成功后记录 `status-requested`
并立即重跑 checker，该事件不刷新 anchor、不延长 deadline。已有 pending request 时不重复
ping。只有 `stale_allowed` 授权记录 `stale-assessed`；stale cutover 后必须结构化记录
`terminated-unfinished termination_reason=stale_cutover
termination_source_event_id=<stale-assessed.event_id>`，再记录 replacement `assigned`
和 `replacement-started replacement_reason=max_progress_silence_exceeded`。人工/平台
unfinished termination 使用 `termination_reason=manual_or_platform_terminated_unfinished`。
failed、stale、unfinished 或 replacement partial output 未恢复到后续 `completed` 前，不能
作为实现完成、Phase 2 check pass 或 Branch Review Gate pass 证据。旧
`record-agent-assignment.sh --status-event` 状态路径 fail closed。
`phase2-check.json` 是 Guru Team 固化 `trellis-check` AI check 结论、覆盖范围、
验证结果、findings 和 `dirty_paths` 的 artifact，不是 Trellis 原生步骤本身，也不是
脚本替代 AI check 的入口。
`review-branch.sh` 只记录和校验已经
完成的 AI/human review 结论，不替代真正的文档 + 代码 review。通过 gate 必须先写
每轮 task-local `reviews/*.md` raw report，再写最终 `review.md` rollup；`review.md`
必须汇总 review rounds、finding lifecycle、最终结论，并链接每个 raw report。该 report 必须来自所有 finding owner 完成同 agent
`问题闭环审查代理` 确认其 finding 已闭环并记录 0 findings，或在原 agent 失败/中断时完成带 `status_events[]` 与 `reuse_decisions[] decision=replace` 证据的替代闭环之后，再由 fresh `最终放行审查代理` 对当前
HEAD 完整 diff 的独立审查并确认 0 findings；任意 finding priority（P0/P1/P2/P3）
都会阻断。非阻断 `observation` 和 scope 外 `followup_candidate` 可记录，但不能替代
当前 scope finding。独立 review sub-agent 只从 AI 角度审查文档、代码、测试、artifact
和 diff evidence，不继续实现、不替 implement/check 代理补工作，也不运行
`review-branch.sh`、`check-review-gate.sh` 或 `record-*` 这类 Guru Team
recorder/validator 扩展脚本；这些脚本由 main session 在 review 完成后执行。再用 `--review-source independent-agent`、
`--review-report .trellis/tasks/<task>/review.md` 和
`--agent-assignment .trellis/tasks/<task>/agent-assignment.json` 让 `review-gate.json`
记录来源、final `review.md` digest、raw `review_reports[]` digest、assignment digest、roles、review round 和 status event 摘要，并校验
同 agent 或替代闭环先于 fresh final、未完成终止的恢复/继任链已到达 `completed` 或 `failed`、且最终放行代理不是 earlier finding owner 或替代闭环 reviewer。`--reviewer` 只记录身份，
不能单独作为通过证据；`*-main-session` / `self-review` 不能通过 gate。
Branch Review 同时验证 Docs SSOT 链条：final reviewer 读取 `Docs SSOT Plan`、实现
handoff、`phase2-check.json`、durable docs、task artifacts 和完整 diff，确认 Phase 2
已经按策略完成 reconciliation。当前 scope 的 durable docs / task artifacts / code /
test / schema / config / script / preset / overlay 不一致必须记录为 finding；reviewer
不首次合并 durable docs，也不替 implement/check 代理补 Phase 2 docs 工作。
`finish-work.sh` 和 `publish-pr.sh` 默认拒绝普通直接调用，避免
`trellis-continue` 链式执行 closeout、提交 review metadata，或在未完成显式
`trellis-finish-work` 时提前 push 分支并创建 PR；日常发布必须由 `trellis-finish-work` 入口带
`--from-trellis-finish-work` 意图标记，在 archive task、记录 journal 并提交允许的
Trellis metadata（包括 `review.md`、`reviews/*.md`、`review-gate.json`、PR readiness）之后内部触发。只有 finish-work 已完成但 publish 需要重试时，才使用
显式 recovery/debug flag。

`finish-work.sh --dry-run --from-trellis-finish-work` 是无副作用 readiness preview：
只校验 gate、dirty state 和 PR body/readiness，并输出将要 archive、journal、
metadata commit、publish 与 merge commit payload 的计划；不会移动 task、写 journal、创建 commit、push 或创建 PR。
dry-run 回复使用 active task 路径表；正式 finish archive 后，AI 必须重新运行
`resolve-human-artifacts.sh` 解析 archive 后 task 路径，并在最终回复输出 archive-path
`Markdown 产物 review 表`，不能复用 archive 前的 active task 链接。

Guru Team workflow 强制中文 Conventional Commits。工作提交和 Trellis metadata
提交 subject 使用 `{type}({scope}): #{primary_issue} 中文描述`，工作提交 body 使用
`背景：`、`变更：`、`边界：`、`验证：` 固定小节并用 `Refs #<primary_issue>` footer；
metadata 提交 body 必须为空，finish/publish 生成的 metadata subject 为
`chore(trellis): #<primary_issue> 固化任务收尾元数据`。commit message 不使用
close keywords（`Closes` / `Fixes` / `Resolves` / `Close` / `Fix` / `Resolve`）；
issue close 语义只在 PR body 中根据
`issue-scope-ledger.json.close_issues` 表达。可用
`.trellis/guru-team/scripts/bash/check-commit-messages.sh --json --task <task-path>`
执行 objective subject/body 校验。

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
PR body 还必须包含 `Docs SSOT` / `文档同步` 处理结果：本次策略、durable docs
更新或 no-update 理由、已 merge 的 task delta、仅保留 task history 的内容，以及
follow-up / 当前 PR limitation。脚本最多检查 section/key 是否存在，语义充分性仍由 AI
readiness review 判断。finish-work/archive 不做首次 Docs SSOT merge；gate 后新增 durable
docs、`.trellis/spec/`、source、tests、schema、config、scripts、preset、overlay、CI/CD、
deployment、migration 或 Makefile drift 必须回 Phase 2/3。

本仓库保留 merge commit。`publish-pr` dry-run/formal payload 会输出
`merge_commit.subject`、`merge_commit.body` 和显式
`gh pr merge <pr> --merge --subject ... --body-file ...` 命令；正式 publish 会解析创建
出的 PR number 并返回 `ready=true`。维护者合并 PR 时必须使用该 payload，不能使用
GitHub 默认 `Merge pull request #xx from ...` subject，也不能把中文 PR title
`完成：#xx ... (#yy)` 直接当作 commit subject。

## 维护原则

- 不修改 Trellis npm 全局包、`node_modules` 或上游 Trellis 源码。
- 不把业务仓库的私有规则写入通用 workflow。
- 中台知识检索和 durable docs SSOT 对齐规则维护在通用 workflow 中，具体业务仓库只保留 task 证据和必要的 docs 更新。
- 长期规则维护在本仓库的 marketplace workflow、preset、companion scripts 和 overlay 中。
- 目标业务仓库中的 generated copy 只是安装结果，不作为长期维护源。
- 修改 `trellis/presets/guru-team/overlays/` 后，先重新应用 preset 到本仓库 dogfood copy，再运行 drift check：

```bash
trellis/presets/guru-team/scripts/bash/apply.sh \
  --repo . \
  --all-platforms
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

如果 preset 产生 `.new` 或 `.bak`，必须逐个检查原因并处理，不能静默提交。


## Push 后远端 Marketplace 门禁

修改 marketplace/preset/overlay/schema/public API 的发布路径会在 branch push 后、`gh pr create` 前执行远端分支 `init`、preview、switch 和 preset reapply，记录 task-local `marketplace-verification.json`。缺失、失败、HEAD 不匹配或 stale artifact 会阻止创建 PR；该门禁不创建 tag，AI 仍负责 PR readiness 判断。
