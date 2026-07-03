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
- 默认只启用 Codex 和 Cursor 支持；如果你使用其它 AI 开发工具，请先把本条改成你需要的平台入口，例如 Claude、OpenCode、Gemini、Copilot 等。
- Trellis 用户名使用 <your-name>，请在执行前把这个占位符替换成你的用户名。
- 使用 Guru Team workflow：workflow id 是 guru-team，workflow source 是 gh:castbox/guru-trellis/trellis。
- 参考 https://github.com/castbox/guru-trellis/tree/main/trellis 中的方式安装 Guru Team preset，把 companion assets 和所选平台 overlay 应用到当前 Repo。
- 安装后确认当前 Repo 只保留你选择的平台入口目录；如果出现未选择的平台目录，例如 .claude/、.opencode/、.gemini/、.kiro/、.qoder/、.codebuddy/、.factory/、.pi/、.reasonix/、.kilocode/、.agent/、.devin/、.zcode/、.trae/ 等，说明原因并清理或请我确认。
- 运行最小验证：trellis --version、.trellis/.version、Trellis 上下文读取、Guru Team check-env。
- 检查 git diff，确认没有敏感信息、.env、token、私钥或本机-only 身份文件被提交。
- 提交并 push。

完成后告诉我：
- 安装到的 Trellis 版本；
- 使用的用户名；
- 实际启用并保留了哪些平台入口；
- 验证命令结果；
- commit hash 和 push 结果。
```

### 升级 Trellis

把这段 prompt 发给已经安装 Trellis 的目标业务仓库里的 AI 会话：

```text
在当前 Repo 中升级 Trellis 和 Guru Team Trellis workflow/preset。

要求：
- 先实时确认 npm 上 @mindfoldhq/trellis 的 latest 版本，并检查当前 trellis --version、which -a trellis、npm list -g @mindfoldhq/trellis --depth=0。
- 升级前检查当前 Repo 是否同时存在 Superpowers、Spec Kit、OpenSpec、GSD 或其它 SDD / agent harness；如果存在，不要继续升级 Trellis，先报告冲突并让我确认迁移或清理方案。
- 如果本机 Trellis CLI 不是 latest，安装/升级到 @mindfoldhq/trellis@latest。
- 默认只保留当前 Repo 的 Codex 和 Cursor 支持；如果你使用其它 AI 开发工具，请先把本条改成你需要的平台入口，例如 Claude、OpenCode、Gemini、Copilot 等。
- 当前 Repo 已有 .trellis/ 时，先用 Guru Team marketplace 生成 workflow 预览，再对比现有 .trellis/workflow.md 和预览内容；确认风险后切换到 workflow id guru-team，workflow source/marketplace 是 gh:castbox/guru-trellis/trellis。
- 拉取或临时获取 https://github.com/castbox/guru-trellis 的最新内容，然后重新应用 trellis/presets/guru-team/scripts/bash/apply.sh 到当前 Repo。
- 如果 preset 生成 .new 或 .bak，逐个检查原因；不要静默覆盖未知本地改动。
- 升级后确认当前 Repo 只保留你选择的平台入口目录；如果出现未选择的平台目录，例如 .claude/、.opencode/、.gemini/、.kiro/、.qoder/、.codebuddy/、.factory/、.pi/、.reasonix/、.kilocode/、.agent/、.devin/、.zcode/、.trae/ 等，说明原因并清理或请我确认。
- 运行最小验证：trellis --version、.trellis/.version、Trellis 上下文读取、Guru Team check-env。
- 检查 git diff，确认没有敏感信息、.env、token、私钥或本机-only 身份文件被提交。
- 提交并 push。

完成后告诉我：
- 升级前后的 Trellis 版本；
- workflow/preset 是否已重新应用；
- 实际启用并保留了哪些平台入口；
- 是否产生 .new 或 .bak 以及处理结果；
- 验证命令结果；
- commit hash 和 push 结果。
```

## 仓库内容

- `trellis/index.json`：Trellis marketplace 入口，提供 `guru-team` workflow。
- `trellis/workflows/guru-team/`：workflow 主合同、配置模板、schema 和 companion scripts。
- `trellis/presets/guru-team/`：把 companion scripts 和平台入口 overlay 安装到目标业务仓库的 preset installer。

## 用户主流程

安装后，用户仍然只需要记住三个主入口：

- `trellis-start`
- `trellis-continue`
- `trellis-finish-work`

`review-branch`、`check-review-gate`、`publish-pr` 是 workflow 内部 companion script，不是需要用户日常手动记忆的新主流程。

## 维护原则

- 不修改 Trellis npm 全局包、`node_modules` 或上游 Trellis 源码。
- 不把业务仓库的私有规则写入通用 workflow。
- 长期规则维护在本仓库的 marketplace workflow、preset、companion scripts 和 overlay 中。
- 目标业务仓库中的 generated copy 只是安装结果，不作为长期维护源。
