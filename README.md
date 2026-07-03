# Guru Trellis

Guru Team Trellis 的公开 marketplace 与 preset 资产仓库。

本仓库是可复用 `guru-team` Trellis workflow 的 canonical 来源，用于让团队成员在业务仓库中安装统一的 Trellis 工作流、companion scripts 和平台入口 overlay。

## 推荐用法

先确认目标 repo 只使用一个研发 harness。Trellis 不要和 Superpowers、Spec Kit、OpenSpec、GSD 等其它 SDD / agent harness 框架在同一个 repo 中混用；多套 harness 同时存在会让 workflow、task artifact、spec、hooks 和平台入口互相抢控制权，后续 AI 会话也更容易读错上下文。如果目标 repo 已经采用其它 harness，先迁移或清理，再安装 Trellis。

不要手工照着命令一步步执行。把下面的 prompt 粘贴给 Codex、Cursor 或你正在使用的 AI 开发工具，让 AI 在目标业务仓库里完成安装、验证、提交和 push。

### 安装 Trellis

把这段 prompt 发给目标业务仓库里的 AI 会话：

```text
在当前 Repo 中安装最新版本的 Trellis。

要求：
- 先实时确认 npm 上 @mindfoldhq/trellis 的 latest 版本，不要凭记忆判断版本。
- 安装前检查当前 Repo 是否已经使用 Superpowers、Spec Kit、OpenSpec、GSD 或其它 SDD / agent harness；如果存在，不要继续安装 Trellis，先报告冲突并让我确认迁移或清理方案。
- 安装/升级全局 Trellis CLI 到 latest。
- 默认只启用 Codex 和 Cursor 支持。
- Trellis 用户名使用 <your-name>，请在执行前把这个占位符替换成你的用户名。
- 如果当前 Repo 还没有 .trellis/，直接用 Guru Team workflow 初始化：`trellis init -u <your-name> --codex --cursor --workflow guru-team --workflow-source gh:castbox/guru-trellis/trellis`。
- 获取本公开 preset 仓库的最新内容，例如 clone 到临时目录或复用已有本地副本并 `git pull --ff-only`：`https://github.com/castbox/guru-trellis.git`。
- 执行 `<guru-trellis>/trellis/presets/guru-team/scripts/bash/apply.sh --repo <current-repo>`，把 Guru Team companion assets 和所选平台 overlay 应用到当前 Repo。
- 安装后确认当前 Repo 只保留你选择的平台入口目录；如果出现未选择的平台目录，例如 .claude/、.opencode/、.gemini/、.kiro/、.qoder/、.codebuddy/、.factory/、.pi/、.reasonix/、.kilocode/、.agent/、.devin/、.zcode/、.trae/ 等，说明原因并清理或请我确认。
- 运行最小验证：trellis --version、.trellis/.version、Trellis 上下文读取、Guru Team check-env。
- 检查 git diff，确认没有敏感信息、.env、token、私钥或本机-only 身份文件被提交。
- 提交前先做 Git 发布预检：检查当前分支、默认分支、远端、是否可能是受保护分支，以及是否已有未提交用户改动。不要默认直接 push 到 main/master/dev/develop 等共享分支。
- 如果当前分支可能受保护或不适合直接推送，先询问我是在当前分支提交，还是创建单独分支并在完成后 push 分支、创建 PR。
- 按我确认的分支策略提交；只有在确认允许 push 时才 push，只有在确认需要 PR 时才创建 PR。

完成后告诉我：
- 安装到的 Trellis 版本；
- 使用的用户名；
- 实际启用并保留了哪些平台入口；
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
- 验证命令结果；
- Git 发布预检结论、最终分支、commit hash，以及 push / PR 结果或未 push 的原因。
```

> **NOTE：复制 prompt 前必须先确认平台范围。**
>
> - 默认升级 prompt 只保留 Codex + Cursor。
> - 如果你的 repo 使用其它 AI 开发工具，要先把平台说明改成实际需要的平台入口，例如 Claude、OpenCode、Gemini、Copilot 等，再执行升级。

## 仓库内容

- `trellis/index.json`：Trellis marketplace 入口，提供 `guru-team` workflow。
- `trellis/workflows/guru-team/`：workflow 主合同、配置模板、schema 和 companion scripts。
- `trellis/presets/guru-team/`：把 companion scripts 和平台入口 overlay 安装到目标业务仓库的 preset installer。

## 日常入口

安装后，用户日常不需要先手动输入 `trellis-start`。直接描述任务、贴 GitHub
issue URL，或说“处理 issue #123”即可；AI 会根据 Trellis 自动注入的
startup context、workflow-state、hook breadcrumb 或 skill matcher 判断是否进入
Guru Team issue intake 和 worktree preflight。

用户仍然需要记住的常用显式入口是：

- `trellis-continue`
- `trellis-finish-work`

`trellis-start` 仍保留为 fallback / explicit orientation 入口，用于平台没有自动
session/startup 注入、hook 未启用或未审批、怀疑自动注入没有运行，或用户需要完整
上下文报告和重新加载 Trellis 上下文的场景。

`review-branch`、`check-review-gate`、`publish-pr` 是 workflow 内部 companion
script，不是需要用户日常手动记忆的新主流程。

## 维护原则

- 不修改 Trellis npm 全局包、`node_modules` 或上游 Trellis 源码。
- 不把业务仓库的私有规则写入通用 workflow。
- 长期规则维护在本仓库的 marketplace workflow、preset、companion scripts 和 overlay 中。
- 目标业务仓库中的 generated copy 只是安装结果，不作为长期维护源。
