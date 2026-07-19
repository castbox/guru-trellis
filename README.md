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

在目标业务仓库根目录执行。Guru Team 安装不要求 developer name：

```bash
npm install -g @mindfoldhq/trellis@0.6.5

trellis init -y --codex --cursor \
  --workflow guru-team \
  --workflow-source gh:castbox/guru-trellis/trellis#v0.6.5-guru.2

GURU_TRELLIS_DIR="$(mktemp -d)/guru-trellis"
git clone --depth 1 --branch v0.6.5-guru.2 \
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
`#v0.6.5-guru.2`，用于可复现的稳定安装。维护者刻意采样最新 `main` / canary
时，可以去掉 `#ref` 或设置其它 branch/tag ref，但最终报告必须说明安装来源是
mutable ref 还是 immutable release tag，以及是否仍以官方 Trellis `0.6.5` 为目标基线。

本仓库也提供 throwaway 安装验证脚本，用来验证默认非交互路径是否仍可开箱运行：

```bash
./trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
```

Trellis CLI 支持 `gh:user/repo/path#ref` workflow marketplace source。该脚本默认验证
`gh:castbox/guru-trellis/trellis#v0.6.5-guru.2`；需要验证其它 branch/tag 时，设置
`TRELLIS_WORKFLOW_SOURCE` 为对应 `#ref`。如果使用不带 `#ref` 的公开远端 source，在非
`main` 分支或本地 marketplace 文件有改动时，该脚本会 fail closed，避免把公开远端验证
误报为当前分支验证。需要刻意采样公开 latest/canary marketplace 时，设置
`TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1`，并在结果中说明这不是当前分支或 release tag
验证。脚本还会用已安装的 wrapper、companion、schema、config、workflow 与官方
`task.py`，在初次安装和 `trellis update` + preset reapply 后各完成一次 dry-run digest、
formal draft、archive、三方 HEAD、ready 与 clean-tree 事务；不会把 canonical runtime
资产手工复制进 fixture。

维护者修改 preset、overlay、extension manifest 或公共 Skill package 前，还必须运行
source-only ownership gate：

```bash
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
```

该 gate 以 Trellis CLI `0.6.5` 为基线，冻结当前 43 条 legacy overlay path 和 payload
hash；其中 37 条由 clean init 生成，6 条历史 Codex prompt/skill path 已不再由 `0.6.5`
初装生成。新增 upstream namespace patch、扩张/替换冻结集合、active payload 漂移、缺失
replacement/removal owner、`unclassified` 或新增 upstream-owned managed claim 都会阻止
preset mutation。它只校验结构化事实，不替代 AI ownership、scope 或迁移充分性判断。

#### AI 安装 prompt

把这段 prompt 发给目标业务仓库里的 AI 会话：

```text
在当前 Repo 中安装官方 Trellis CLI v0.6.5，并安装 Guru Team extension stable v0.6.5-guru.2。

要求：
- 先实时确认 npm 上 @mindfoldhq/trellis 的 latest 版本，不要凭记忆判断版本；如果 latest 已不是 0.6.5，本次仍按 Guru Team stable v0.6.5-guru.2 的目标基线安装 @mindfoldhq/trellis@0.6.5，除非我明确要求升级官方 Trellis 基线。
- 安装前检查当前 Repo 是否已经使用 Superpowers、Spec Kit、OpenSpec、GSD 或其它 SDD / agent harness；如果存在，不要继续安装 Trellis，先报告冲突并让我确认迁移或清理方案。
- 安装/升级全局 Trellis CLI 到 @mindfoldhq/trellis@0.6.5。
- 默认只启用 Codex 和 Cursor 支持。
- Guru Team preset 与 task workspace executor 不要求 developer name，也不要求 `TRELLIS_USER`、`-u` 或 `--user`。
- 如果当前 Repo 还没有 .trellis/，直接用 Guru Team workflow 的稳定非交互命令初始化：`trellis init -y --codex --cursor --workflow guru-team --workflow-source gh:castbox/guru-trellis/trellis#v0.6.5-guru.2`。
- 官方 Trellis 可能仍根据 Git config 创建 `.trellis/.developer` 与 `.trellis/workspace/**`；这是官方 identity/journal 行为，不是 Guru 前置。Guru apply/update/reapply 与 task workspace executor 不读取、不创建、不恢复这些路径，也不删除已有官方数据。
- 如果我明确要求交互式选择 spec template，才可以去掉 `-y`；默认安装和自动验收必须使用 `-y` 或显式 `--template <name>`。
- 获取与 workflow source 相同 release tag 的公开 preset 仓库内容，例如 `git clone --depth 1 --branch v0.6.5-guru.2 https://github.com/castbox/guru-trellis.git <guru-trellis>`。只有明确要跟随 latest/canary 时，才复用 `main` 或不带 `#ref` 的远端 source，并在最终报告中说明来源是 mutable ref。
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
- 是否存在官方 Trellis identity/workspace 数据，以及 Guru preset 是否保持其原状；
- 实际启用并保留了哪些平台入口；
- 是否发现 `00-bootstrap-guidelines`；是否已获得确认并完成 spec bootstrap，或保留为后续 task；
- 验证命令结果；
- Git 发布预检结论、最终分支、commit hash，以及 push / PR 结果或未 push 的原因。
```

> **NOTE：** 如果你不使用默认的 Codex + Cursor，先把 prompt 里的平台说明、
> `trellis init` 平台参数和 `apply.sh --platform ...` 参数改成实际工具。

### 升级 Trellis

把这段 prompt 发给已经安装 Trellis 的目标业务仓库里的 AI 会话：

```text
在当前 Repo 中升级 Trellis 和 Guru Team Trellis workflow/preset。

要求：
- 先实时确认 npm 上 @mindfoldhq/trellis 的 latest 版本，并检查当前 trellis --version、which -a trellis、npm list -g @mindfoldhq/trellis --depth=0；如果 latest 已不是 0.6.5，本次仍按 Guru Team stable v0.6.5-guru.2 的目标基线安装 @mindfoldhq/trellis@0.6.5，除非我明确要求升级官方 Trellis 基线。
- 升级前检查当前 Repo 是否同时存在 Superpowers、Spec Kit、OpenSpec、GSD 或其它 SDD / agent harness；如果存在，不要继续升级 Trellis，先报告冲突并让我确认迁移或清理方案。
- 如果本机 Trellis CLI 不是 0.6.5，安装/升级到 @mindfoldhq/trellis@0.6.5。
- 默认只保留当前 Repo 的 Codex 和 Cursor 支持。
- 当前 Repo 已有 .trellis/ 时，先用 Guru Team stable marketplace 生成 workflow 预览：`trellis workflow --marketplace gh:castbox/guru-trellis/trellis#v0.6.5-guru.2 --template guru-team --create-new`，再对比现有 `.trellis/workflow.md` 和 `.trellis/workflow.md.new`；确认风险后运行 `trellis workflow --marketplace gh:castbox/guru-trellis/trellis#v0.6.5-guru.2 --template guru-team` 切换 active workflow。
- 获取与 workflow source 相同 release tag 的公开 preset 仓库内容，例如 `git clone --depth 1 --branch v0.6.5-guru.2 https://github.com/castbox/guru-trellis.git <guru-trellis>`。只有明确要跟随 latest/canary 时，才复用 `main` 或不带 `#ref` 的远端 source，并在最终报告中说明来源是 mutable ref。
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
- `trellis/presets/guru-team/ownership/`：43 条 legacy overlay 的 frozen ownership inventory 与 strict schema。
- `trellis/skills/guru-team/`：公共 workflow skill registry、interface schema、canonical package 与 test-only fixtures。

## Guru Team Extension Version

公共 closed-loop workflow skill 的 canonical source 位于
`trellis/skills/guru-team/`。Marketplace workflow 只安装
`.trellis/workflow.md`，不会安装 external skills；必须继续应用 Guru Team
preset，才会获得 `.trellis/guru-team/skills/` 的 audited installed copy、
shared skill copy 和所选 Codex/Cursor/Claude 平台副本。

Registry 的 `reserved` id 不安装也不参与 mandatory route；`planned` id 只保留未来
consumer identity，不安装 package，也不能拥有 invoke/exit marker。只有通过完整
package/interface/schema/route 验证的 `active` 项才会分发。当前 active ids 是
`guru-sync-base`、`guru-discover-change-context`、
`guru-clarify-requirements`、`guru-review-contract-wording`、
`guru-review-change-request`、`guru-create-task-workspace` 与
`guru-create-task-commit`。Active package 的
`SKILL.md` frontmatter `name`/`description` 必须与 stable id/interface 精确
一致，`tests[]` 必须是 package-local `tests/<file>` 的真实 regular file，不能
使用标签、虚构路径、越界路径或 symlink evidence。升级遇到已知
managed old bytes 时保留 `.bak` 后升级，遇到未知本地改动或无效 provenance
时保留原文件并写 `.new`，且 fail closed。运行 `trellis update` 后必须重放
workflow 与 preset，处理全部 sidecar，并运行：

```bash
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode source
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode installed
```

Public Skill 的 `workflow` / `standalone` 是稳定 routing mode id：前者由 global
workflow mandatory invoke，后者允许所选平台直接发现并调用。`standalone` 不表示复制单个
Skill 目录即可 self-contained/portable 运行；两种 mode 都要求完整且兼容的 Guru Team
preset、extension manifest、shared runtime 与 managed package inventory。Package wrapper
统一经 `.trellis/guru-team/scripts/bash/run-skill-command.sh` 校验 runtime API 和 drift 后
调用 companion command；缺失或不兼容时会在业务副作用前失败，并提示安装或升级完整
preset、处理 `.new` / `.bak`、重跑 source/installed validation 后再试。

Phase 0 的第一个 repo-changing hop 由 `guru-sync-base` 独占。Base 按以下固定顺序
解析：显式 `--base`、非空 scalar `base_branch`、按 `base_branch_candidates` 声明顺序
选择第一个 existing local 或 remote-tracking ref（缺省 `dev -> develop -> main -> master`）、
候选均不存在时的 remote default；current branch 永远不是隐式 fallback。多个候选同时
存在不是歧义，配置顺序就是优先级。Executor 以 pre-sync resolution digest 绑定重解析和
fetch/`ff-only`，同步后生成 `post_sync_resolution_sha256`。成功结果必须证明 decision
checkout HEAD、local base HEAD 与 remote-tracking HEAD 三方相等且 checkout clean，随后
由 validator 校验 schema、pre/post digest 和 live Git facts，并只把 post-sync digest
交给下一 consumer。Stable exits 只有 `synced`、
`skipped`、`blocked`；`prepare-task` 只以 query-only compatibility 复用同一个 strict
core，active mutation 由 workspace Skill 独立重验 current base facts。`standalone`
可直接发现该 Skill，但仍要求完整 preset/runtime，workflow-only
`skipped` recorder 不向 standalone 暴露。对应 result schema 是
`guru-base-sync-result-1.0`，managed commands 是 `sync-base` 与 `check-base-sync`。
Resolution 和 result facts 只通过 stdout 传递，不创建 repo-external evidence file、lease、
release 或 cleanup API。该 Skill 声明 `judgment_mode=deterministic`，执行
`forward_behavior -> recorder_validator -> typed_exit`；它没有 selected-base AI
confirmation、post-execution AI Review Gate 或 conditional human confirmation。Caller 仍由
AI 在 Skill 外完成 tool-free route classification，所有需要语义判断的 Skill 继续使用
`judgment_mode=semantic`。

`guru-sync-base:synced` 的唯一 consumer 是 semantic
`guru-discover-change-context`。Workflow 与 standalone 使用同一组 freshness
preconditions，固定执行 fresh base、live issue/proposed draft、open duplicate facts、
updated-base Docs、code/API/config/schema/ownership、tests/fixtures/throwaway/update、
canonical query、一次 archived history preview、AI candidate deep-read、AI Review Gate、
recorder/validator。History 只读取 archived `finish-summary.json:index.*`，使用
`guru-context-history-score-1.0` 产生稳定 query/manifest/preview digests、invalid
isolation、固定排序与 limit 20 projection。有候选时 AI 选择 1 至 3 个窄读，零候选
仍成功，并固定 empty selection/deep reads 与一致的 `mem_review=not_needed` shape，不得
触发其它历史源；candidate-present 时 `trellis mem` 只在 task artifacts、Docs/code/tests、GitHub 与 Git history 四类
证据均不足以解释命名的 load-bearing decision 时使用。

Pre-task 结果只通过 stdout 返回。Task 创建后 recorder 只把 expected digest 匹配的
同一 snapshot 写入 direct active `{TASK_DIR}/context-discovery.json`，并在写后重读
exact bytes、snapshot identity 与 live freshness；archived/completed/non-active task
必须拒绝。Recorder/checker 执行 published closed Draft 2020-12 schema；base evidence
嵌入完整 validator-passed sync result并绑定 post-sync digest、selected remote refs 与严格
GitHub repo identity。Pre-task/standalone 绑定 decision checkout branch；task mode 允许在相同
HEAD 上进入 `task.json.branch` feature worktree，但仍校验完整 provenance、base refs、active
task locator/status 与 task-local-only dirty paths。Git status failure 不得冒充 clean，base stale 在
任何 live issue/draft、reviewed blob 或 archive preview 前短路。Draft 绑定 created issue 时
live body digest 必须等于原 reviewed draft。Caller-authored `refresh_base` 记录当前 stable
stale codes、superseded query/snapshot digests、reason 与 detection time；record/check 只将
这些事实与当前 live freshness 对齐后要求整步 re-entry，并只消费当前 payload 与 expected
snapshot identity，不重建 external refresh chain。Task-local recorder 写前/写后与 checker 还必须通过 `git
check-ignore --quiet --no-index -- <target>` 证明 artifact 未被 repo ignore、
`.git/info/exclude` 或 `core.excludesFile` 忽略；pre-task stdout-only 不执行该 gate。只有
stable stale codes 与 live drift 一致时才返回 `refresh_base`，`context_ready` 对同一 stale
拒绝。Archive reader 以普通 file/read/JSON/index-shape failures 形成 portable invalid
evidence；snapshot deep-read locator 按 task artifact/canonical GitHub issue-or-PR/exact Git
object-or-ref 三类闭合校验。Closed schema 与结构化 locator 不保存 raw source payload，
只做 field-specific validation。不写 workspace、runtime、
repo-level archive index/cache 或 shared handoff。Schema 是
`guru-context-discovery-1.0`，managed commands 是
`preview-change-context-history`、`record-context-discovery`、
`check-context-discovery`。Stable exits 是 `context_ready` -> active Skill
`guru-clarify-requirements`、`refresh_base` -> `guru-sync-base`、`blocked` ->
`change-context-blocked`；duplicate reuse/new target 决策交给 #113。Source/installed
validator 要求 Skill consumer 是 active 或 consumer-only planned registry id：active 必须有
完整 installed package，planned 必须保持 package 缺失并在调用前 fail closed；workflow/stop
consumer 仍须各有唯一匹配 target marker。

`guru-clarify-requirements` 统一 initial issue/proposed draft、active-task scope change 与
standalone review。Workflow/standalone 使用相同 preconditions 和 semantic 五阶段；Skill
验证 repository-answerable `answered` evidence、question lifecycle与confirmed payload/live
mutation；先穷尽 repository-answerable questions，且 `answered` 必须有checked evidence，再按每轮一个最高价值
问题收敛。每轮question id必须来自本轮opened或既有open set，reducer固定为
`open_questions = opened - closed`。只有不可分割产品选择才记录 `atomic_group`。Scope proposal 与 source action 都绑定 recorder 派生的 digest；
未确认 expansion 纳入 current scope 必须取得 proposal-digest-bound 专用确认，普通“继续”、
task/planning/review approval 不得替代。Optional mechanism 产生的风险只能删除/替换机制或
另行提案。

Package 不提供 mutation executor。GitHub comment/body 只能由 AI 在 exact action
confirmation 和 live preimage 复核后通过现有 connector 或审查过的 `gh` 执行，随后重读
live facts；recorder/checker 只规范化和校验 closed schema、derived digest、freshness、
confirmed exact payload/mutation/live content、active-task ledger/planning/stale-gate linkage 与 typed exit。Pre-task/standalone stdout-only，
无专用 clarification artifact；active-task current inclusion 绑定
`guru-approve-task-plan`、`guru-check-task`、`guru-review-branch` re-entry owners。Schema 是
`guru-requirements-clarification-2.0`，managed commands 是
`record-requirements-clarification` 与 `check-requirements-clarification`。Active-task Scope
Change Gate mandatory invoke本Skill。Exits 是 `clear` -> caller-aware
`guru-requirements-clear-router`、`needs_context` ->
`guru-discover-change-context`、`refresh_context` -> `guru-sync-base`、`retarget_context` ->
`guru-sync-base` 并针对 selected issue 完整重跑 Intake、`new_task` -> staged
`guru-full-task-intake-chain`、`blocked` -> `requirements-clarification-blocked`。成功 GitHub
mutation 必须返回 `refresh_context`；`new_issue_draft` 不创建 issue，真正 intake mutation
属于 #112。Clear router只验证 `resume_target`并恢复initial wording、standalone caller、
active planning review或exact interrupted progression，不重新分类scope。

2.0 新增 checker-bound target disposition、duplicate candidate decision、authority impact、
`select_existing_issue` / `reopen_issue` 与 `retarget_context`。1.0 artifact/caller 无法表达这些
必填合同，recorder/checker 返回
`requirements_clarification_legacy_schema_requires_refresh`；不做语义自动迁移，必须从
`guru-sync-base` 重新执行完整 Intake。

Active-task `clear`/`new_task` 必须携带非空且全部属于七类 terminal decision 的 proposal set；
accepted-current/related/followup/new-task/out-of-scope 五类 scope classification 无论来源状态，
都必须有 proposal-digest-bound 用户证据，并把 structured
`decision_trail` exact 写入当前 `issue-scope-ledger.json.scope_decisions[]`，并绑定 live
GitHub comment/body authority 的 content/`updated_at`、planning approval/doc digests、review state、stale gates、
interrupted target 与 re-entry owners；planning approval 必须是 shared checker 完整校验通过的
`guru-planning-approval-2.0` `approved` result 并 exact 绑定 reviewed/approved 三文档，旧 ledger hash、两行 planning docs
或最小 approval JSON 均不成立。`mechanism_removed/replaced` 要求 optional origin、null
confirmation，不进入 trail 或 authority mutation。GitHub authority mutation 后必须先返回
`refresh_context`；context `generated_at` 不早于 authority `updated_at` 后执行 task update，
并以 `context_before_task_update_sha256` 绑定该 digest，不要求第二次 context refresh。
Active-task `new_task` 保留该 trail，只向 #112 返回 side-effect-free reviewed draft。

Source issue 的 live state 可为归一化后的 `open` 或 `closed`；open duplicate candidates
与 draft-created issue binding 仍分别保持 open-only。Current Docs、code/contracts、tests
使用 40 位 Git identity 时，validator 会重新解析 `HEAD:<path>` 并要求对象类型严格为
`blob`；tree、gitlink commit、tag、missing object 或 identity drift 均 fail closed。

Duplicate candidate 的 canonical fact projection 固定为 normalized bound repo、positive
number、`identity=#<number>`、canonical issue URL、`state=open` 与 `updated_at`；
`facts_sha256` 不含 AI reason/observation，并由 pure gate 从同一次 open duplicate search
返回字段重算 identity、URL 与 digest；validator 不进行第二次 search 或 candidate re-read。
Schema/runtime 同时
强制 `typed_exit=blocked` 当且仅当 `ai_review_gate.status=blocked`。

Recorder/checker 的 production entry 固定先执行 pure schema/digest/semantic
shape，再执行 base-only live gate；只有 fresh base 才能读取 repo-bound locator、issue、
reviewed blob 与 archive/history。Base stale 只核对 caller-authored refresh codes 和
superseded digests 后返回。`change_input` 十组 clue arrays 至少一组非空，issue binding
和 canonical query 不能替代入口线索。Portable locator 只按各 source 的 closed structure
验证，不扫描整份 payload。

Skill id、external exit id、schema/interface id、stable command 和 registry
lifecycle 是公共 API；破坏性变更必须使用新 id 或提供明确迁移合同。

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

例如 `v0.6.5-guru.2` 表示“针对官方 Trellis `0.6.5` 的 Guru Team 第 2 个稳定修订”。
同一个官方 Trellis 基线下，Guru Team 可用 `.2`、`.3` 递增发布兼容修订；只有切换官方
Trellis 基线时才移动前缀，例如未来的 `v0.6.6-guru.1`。

Guru 修订号按兼容性维护：

- patch：兼容 bugfix、文档澄清、非破坏性 guardrail 修正；
- minor：兼容新增字段、script 能力、platform overlay 或可选门禁；
- major：破坏 workflow id、script CLI、artifact schema、installed path、默认行为或升级语义。

本仓库的 release tag 使用 repo 级 tag，例如 `v0.6.5-guru.2`。tag 名称必须与该 tag
所指提交中的 `trellis/guru-team-extension.json.version` 对应；该 manifest 同时用 `target_trellis_cli`
记录目标官方 Trellis CLI 版本。稳定安装文档使用
`gh:castbox/guru-trellis/trellis#v0.6.5-guru.2`。不带 `#ref` 的
`gh:castbox/guru-trellis/trellis` 只表示 latest/canary，不应用作需要复现的问题定位坐标。
发布顺序必须是：先 merge 包含 manifest/docs 更新的 PR，再在 merge commit 上创建并 push
annotated tag `v0.6.5-guru.2` 这类 release tag，验证 `trellis init` / `trellis workflow`
的 tag-pinned 安装后，再退休旧 tag 名称。

当前已发布、可复现的 stable tag 是 `v0.6.5-guru.2`。工作分支中的 canonical
manifest 已递增到下一待发布版本 `0.6.5-guru.17`；在对应 merge commit 创建并验证
release tag 前，不得把 `.7` 写成已发布 stable source。

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
Guru Team issue intake 和 worktree preflight。Tool-free classification 之后，对
repo-changing route 的第一个 mandatory hop 是 `guru-sync-base`：

```text
guru-sync-base
  synced -> guru-discover-change-context
  skipped -> original-request-route
  blocked -> base-sync-blocked
guru-discover-change-context
  context_ready -> guru-clarify-requirements
  refresh_base -> guru-sync-base
  blocked -> change-context-blocked
guru-clarify-requirements
  clear -> guru-requirements-clear-router
    initial/draft -> guru-review-contract-wording:change_request
      pass -> guru-review-change-request
        ready -> guru-create-task-workspace
          created -> Phase 1
          refresh_review -> guru-sync-base
          cancelled -> task-workspace-cancelled
          blocked -> task-workspace-blocked
        clarify_requirements -> guru-clarify-requirements
        review_wording -> guru-review-contract-wording
        refresh_context -> guru-sync-base
        blocked -> change-request-review-blocked
    standalone -> guru-standalone-caller
    active-task -> planning review or exact interrupted progression
  needs_context -> guru-discover-change-context
  refresh_context -> guru-sync-base
  new_task -> guru-full-task-intake-chain
  blocked -> requirements-clarification-blocked
```

只有 `synced` 才能继续读取 issue、搜索 duplicate。兼容查询入口仍可运行：

```bash
.trellis/guru-team/scripts/bash/check-env.sh --json
.trellis/guru-team/scripts/bash/prepare-task.sh --json \
  --expected-resolution-sha256 <post-sync-resolution-sha256> \
  "<user request or issue URL>"
```

`prepare-task.sh --json` 只保留 query-only 兼容能力：它可以读取明确提供的
issue、搜索重复候选，并输出 proposed issue、base branch、branch name、workspace
path、create-task command 和 `naming_quality`，但不会创建 GitHub issue、worktree、
branch 或 Trellis task，也不会在未确认 source issue 时写
task-local `.trellis/tasks/<task-slug>/task-start-context.json` and gitignored `.trellis/.runtime/guru-team/**` mappings。没有 source issue 的 freeform 请求必须先由 AI 展示
proposed issue title/body、duplicate evidence 和 naming quality；planner 输出不会写
task context 或 runtime cache。Legacy `--create-issue-confirmed`、`--create-worktree`、
`--create-task` 均零写入 fail closed，并指向 active
`guru-create-task-workspace`；不能把 task creation consent 当成在 source checkout 直接运行
`task.py create` 的批准。
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
`prepare-task` query 必须接收前序 validator/guard 的 post-sync digest 和相同 resolver 输入，并在
`gh auth status`、issue read 和 duplicate search 前执行同一 strict base-sync core。
`guru-create-task-workspace` exact executor 在 issue 或 worktree/task mutation boundary 独立重验
完整 plan、prerequisites、target、base 和 live facts。每次成功都必须
满足 clean checkout 与 decision/local/remote HEAD 三方相等；只在 selected-base checkout
上用 `git merge --ff-only` 安全推进本地 base。Wrong checkout、dirty、missing ref、fetch
失败、divergence、resolution drift 或 freshness 无法确认都会阻塞，不会从 stale ref 创建
任务分支。

Plan 明确绑定 initial `post_sync_resolution_sha256`。Executor 在首次 confirmed GitHub 或
workspace/task mutation 前实际重跑一次 shared resolver/sync core；remote 正常前进时可以
安全 fast-forward selected base，但随后返回 `refresh_review`，且不创建 issue、branch、
worktree、task、artifact 或 runtime mapping。Fresh identity 不变才继续当前 plan。

`prepare-task` query 只消费当前 post-sync digest；它不再拥有 workspace mutation guard。
`guru-create-task-workspace` 在每个受支持的 issue/worktree/task mutation boundary 重验
plan、五个 prerequisite、base、target 与 live facts。任何 identity/digest 漂移都在
读取或 mutation 前阻塞。Phase 0 不创建需要跨调用清理的 resolution/result evidence 文件。

`guru-create-task-workspace` 使用 semantic 五阶段和完全相同的 workflow/standalone
preconditions。Reviewed draft invocation 只取得 `github_issue_mutation` confirmation，创建
exact issue 并重读后固定返回 `refresh_review`；同一调用不创建 branch/worktree/task。重跑完整
Intake 后，open issue invocation 另行取得 `workspace_and_task_mutation` confirmation。Assignee
固定按 explicit、single issue assignee、zero issue assignees 时 current GitHub login、
multiple/unresolved 时 AI/user 选择解析，并始终作为显式参数传给 official task-create handler。
Passed Gate + confirmed 才可 mutation；passed + digest-bound refused 返回
`cancelled`，`reroute` 返回 `refresh_review`，`blocked` 返回 `blocked`，后三者均由
checker 验证 zero-write snapshot。

Draft executor 在 create 前按 exact open title/body/labels 与 `createdAt >= reviewed plan`
执行 0/1/>1 recovery：0 个才创建，1 个恢复并重读，多个 fail closed。因此 remote create
成功但 immediate reread失败后的同 plan重试不会再次创建 Issue。完整 Intake重入后的
workflow-created existing issue还必须携带完整 checker-passed created-issue result，并与
current issue及 fresh context 的 canonical live existing-issue identity一致；该 context
必须为`kind=issue`且`issue_binding=null`，单独 SHA 不构成 authority。

Workspace executor 不直接进入会读取 developer identity 的 CLI 路径，而是在隔离子进程中调用官方
`common.task_store.cmd_create` handler，并把 reviewed assignee 作为显式 create 参数；仅在该
handler 调用内禁用 official developer accessor，因此 `task.json.assignee` 与
`task.json.creator` 都固定为 reviewed login。该 adapter 不读取或改写 existing
`.trellis/.developer`，source/target 中已有 identity bytes 保持不变。

创建成功后只写四个 tracked task-local Intake artifacts：`task-start-context.json`、
`issue-scope-ledger.json`、`context-discovery.json`、`issue-review.json`。Plan/result 只走
stdout 且不含 absolute workspace path，本机 mapping 只位于 ignored
`.trellis/.runtime/guru-team/**`。Checker 从 current config、reviewed slug 与 live Git facts
推导 worktree。A/B fixture 从同一
clean base 分别走 production recorder/executor/checker、task-local archive/commit，再验证
A -> B 和 B -> A 两个本地 merge 顺序均无 Guru metadata conflict；不创建远程 PR或并发进程。

executor 完成后，tracked `task-start-context.json` 只提供 portable
`workspace_slug`、`task_workspace_id` 和 `task_artifact_dir`，不得包含或读取 absolute
`workspace_path`。`workspace_mode: worktree` 下的 task artifact 写入边界由当前 checkout、
`.trellis/.runtime/guru-team/**`、`git worktree list` 和 boundary helper 共同推导/校验。AI 或 main session 在写入/校验
`planning-approval.json`、`phase2-check.json`、`agent-assignment.json`、`reviews/*.md`、
`review.md`、`review-gate.json` 等 task-local artifact 前，应从目标 worktree 运行：

```bash
.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task <task-path>
```

该 helper 只报告 expected workspace、actual repo root、source checkout status、task
worktree status 和 source checkout 中可疑同名 task artifact/review metadata；它不判断
sub-agent 是否 stale，不迁移误写 patch，也不清理 source checkout。若编辑工具不能显式传入
`workdir`，必须使用 boundary helper 已确认的当前 task worktree 下的绝对路径，不能从
committed task context 拼出本机路径。
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
`review-branch`、`check-review-gate` 是 workflow 内部 companion script；
`publish-pr` 仅保留为兼容性阻断入口。它们都不是需要用户日常手动记忆的新主流程。
`guru-approve-task-plan` 是 Phase 1 planning approval 与唯一
`planning-approval.json` 的 semantic owner；global workflow 只 mandatory invoke stable id、
消费 `approved` / `revision_required` / `clarify_scope` / `blocked` 四个 typed exits，并让
`approved` 唯一进入 task activation。Installed recorder/checker 只消费 AI-reviewed input、
重建确定性事实并校验 `guru-planning-approval-2.0` closed union，不执行 adequacy、
provenance、confirmation 或 route 判断。`approved_scope_expansion` 不接受 caller-only digest：
普通 proposal 从 current planning locator 重算，unusual proposal 从 canonical candidate 重算；
专用 confirmation 与 runtime-materialized current authority digest 必须绑定同一 proposal，
candidate link 不重复确认。Task 仍为 `planning` 时 checker 会复验 invocation
base/HEAD/dirty snapshot；activation 后正常实现 HEAD/dirty drift 不会单独使 approval stale。
`issue-scope-ledger.json` 作为 task projection 或 requirement authority 时都只绑定
primary/close/related/follow-up issue 分类投影，decision/acceptance metadata 更新不会误 stale。
`task.py start` 只写状态，不代表规划已审查。
`resolve-human-artifacts.sh` 为阶段回复提供确定性路径事实：规划停止、Phase 2 完成、
Branch Review Gate 结果、finish-work dry-run 和最终 archive/publish 回复都应先运行它，
然后输出 `Markdown 产物 review 表`。标准表只列 `prd.md`、`design.md`、
`implement.md`、`review.md`、`pr-body.md` 五个 Markdown；缺失文件不生成 Markdown
链接，`phase2-check.json`、`review-gate.json`、`agent-assignment.json` 等 JSON
证据不进入默认表。
Phase 2 在 unchanged official `trellis-check` / channel `check` 收集 raw evidence
后 mandatory invoke active semantic Skill `guru-check-task`。该 Skill 是 scope
qualification、adequacy、finding/full-rerun loop、Docs SSOT review、四出口和唯一
`phase2-check.json` 的 owner；新 artifact 使用 closed schema
`guru-phase2-check-2.0`。`record-phase2-check.sh` / `check-phase2-check.sh` 只记录和
校验 AI-authored closed result 的确定性事实；worker 输出、coverage flags、验证命令
或脚本成功都不能生成 Guru pass。
V2 evidence 的 provenance/handoff/durable/reviewed-path/command collections 与
每个 adequacy evidence refs 均非空，并闭合全部 known current-round source；current/scope-change
candidate 必须有 trigger refs。Checker 从源字段重算全部 semantic 子 digest、Gate bindings、
finding count 和 full-round digest。Handoff 内 task-local assignment 的合法 post-commit review
metadata tail 使用 stable Phase 2 projection，不放宽 implementation/check/recovery freshness。
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
`agent-assignment.json` schema 1.2 额外提供 append-only
`event_corrections[]` 与 `recovery_links[]`：前者用目标 event canonical digest 显式失效
错误 provenance 的 progress/status-request 记录，后者只补同 agent `failed` 到后续
manual/platform `terminated-unfinished` 的结构边。Validator 拒绝 unknown、duplicate、
cross-agent、cycle/backward 和 tampered target，并且仍要求 replacement 链真实到达
`completed`；自然语言说明本身不能修复 machine gate。
`phase2-check.json` 是 Guru Team 固化 `guru-check-task` semantic check 结论、
official worker/command evidence、scope qualification、adequacy、findings、unverified
items 和 `dirty_paths` 的 artifact；脚本成功不能替代 Skill 的 AI Review Gate。
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
`trellis-continue` 不得 push 分支、创建 PR、调用 `publish-pr` 或调用
`finish-work`，也不得提交 `review.md` / `reviews/*.md` / `review-gate.json` 等 Trellis metadata。
PR 发布只发生在显式 `trellis-finish-work` 入口。dry-run 输出完整 immutable
`closeout_plan` 与 `closeout_plan_digest`；正式执行必须原样传入该 digest，并在首个副作用前
重建校验。随后按 reviewed content push、marketplace evidence/readiness commit、draft PR、
final archive projection、单次 archive metadata commit/push、三方 HEAD 对齐、draft-to-ready
推进。裸 `finish-work.sh` 默认拒绝普通直接调用，`publish-pr.sh` 无条件作为兼容入口
阻断；中断只重跑同一个 `trellis-finish-work`，不暴露内部 recovery flag。

prepare 使用已安装的官方 config parser 读取 `.trellis/config.yaml`：只支持缺失或空
`hooks.after_archive`，非空、歧义、不可读、含 NUL 或 symlink 配置在任何副作用前拒绝，
且不会执行 hook。official move 前再次核对实时 archive 月份、空 index、精确 untracked
集合、所有 tracked regular-file/mode/blob continuity；失败时 task 保持 active、PR 保持
draft。若已提交 plan 跨月，same entry 必须重新 dry-run 并审查新 digest，再以仅更新
plan/readiness 的 additive evidence commit 显式 supersede；不 rewrite history、不迁移目录。
共享 prepare 从 archive root 到 month/final destination 对每个既有组件逐层 `lstat`，
不读取或跟随 symlink target，任何 symlink（含 dangling、repo 内 target）都拒绝；计划
final locator 还必须不存在。official move 前重复同一检查，阻止 prepare-to-move 漂移。
`task.json.children` 缺失按空 list 处理，否则必须为 `list[str]`。按官方 active task
exact/suffix lookup，只有仍会被 archive 改写 `task.json` 的 active child 阻塞，已归档
child 作为历史关系不阻塞 parent closeout。

`finish-work.sh --dry-run --from-trellis-finish-work` 是无副作用 readiness preview：
通过 `--finish-summary-index-file "{TASK_DIR}/finish-summary-index.json"` 校验 AI 已审查的索引输入，
并输出 canonical plan、digest、future archive mapping、metadata allowlist 与 transitions；
不会移动或写入文件、创建 commit、push 或创建 PR，也不存在 journal/workspace 计划。
dry-run 回复使用 active task 路径表；正式 finish archive 后，AI 必须重新运行
`resolve-human-artifacts.sh` 解析 archive 后 task 路径，并在最终回复输出 archive-path
`Markdown 产物 review 表`，不能复用 archive 前的 active task 链接。

Guru Team 不调用官方 `add_session.py`，不把 `.trellis/workspace/**` 用作 finish、readiness
或 context 证据；shared start 只组合 phase/packages/task/Git facts，Codex/Cursor SessionStart
overlay 不读取或枚举 journal。preset 固定 materialize `session_auto_commit: false` 并忽略该目录。
finish-work 在 active task 中绑定唯一 draft PR，再一次构建包含 canonical URL 与唯一
`PR #<number>` ref 的 final summary。recorder 将 raw base-to-HEAD paths 排序去重并过滤
workspace/runtime 受保护前缀，把安全集合同时写入 `git.changed_paths` 与 search `paths`；
schema/validator 的所有 path 字段仍拒绝受保护前缀。final summary 只随 exact archive metadata
transaction 提交，不存在 empty-URL initial summary 或 post-archive metadata tail。
archive 前 recovery 使用 committed plan/readiness/evidence 与 task-local body/summary facts。official
move 后、精确 archive commit 尚未形成时，仍严格校验 archived working-tree 完整布局、dirty/staged
path、blob continuity 与官方 `task.json` delta；commit 缺失或不匹配继续 fail closed。一旦当前
`HEAD` 已是精确 archive commit，普通 archived task 和 plan-only recovery 都从该 commit blob
读取 plan，只以 immutable plan 和 Git parent/path/tree/blob lineage 为准，
本地 archived 文件缺失、篡改及其 dirty state 不阻塞 exact push、远端 title/body digest、三方 HEAD
或 draft-to-ready。plan-only archived directory 只允许 `trellis-finish-work` 恢复入口解析，普通 task
命令仍要求 `task.json`。readiness、body、ledger 与 verifier 不再打开；但 final summary 的 real-PR
deterministic bytes/digest 属于 pre-move、incomplete recovery 与 exact recovery continuity。
pre-move/incomplete 路径用已绑定远端 PR 重建 expected bytes，exact 路径只从 immutable archive
commit 的 `finish-summary.json` blob 恢复原 PR number/URL 并重建校验，不读取 working-tree summary，
也不调用通用 summary artifact validator。fresh archived reentry 只接受与该原 number/URL 一致的唯一
open repo/head/base 候选；原 PR 缺失、closed 或被同分支新 PR 替代均 fail closed。
final projection、incomplete 与 exact recovery 统一复用 strict PR URL parser：GitHub
owner/repository identity 按大小写不敏感比较，canonical summary 输出保留 remote 返回的合法 casing
（如 `microsoft/PowerToys`）；非 HTTPS、错误 repo、非法 number、trailing/extra path、query/fragment
仍一律 fail closed。
plan-only 恢复不会把缺失 context 当作 boundary 豁免：它从当前 commit blob 读取 immutable plan，
在任何 GitHub/fast-path 动作前校验 Git toplevel、配置和effective remote repo、当前head branch、
base ref、current HEAD transaction、expected digest、task identity 与 active/archive locator。普通 task
discovery、workspace boundary 和其它命令继续要求 `task.json`，worktree mode 继续要求
`task-start-context.json`。
该入口在普通 resolver/`resolve()` 前保留 raw locator，只允许 task basename、原 active locator 或
精确 archive locator；path-like 输入先从 repo root 到 final task dir 逐组件 `lstat`。basename
输入则在普通 resolver 前按其候选顺序预检 `<repo>/<basename>`、active task candidate、archive
root 和 archive candidates；每个 direct/archive candidate 都先保留 `symlink_component` 证据，再用
普通 resolver 完全相同的 follow-symlink `directory + task.json` 谓词判断，matching alias fail closed，
unmatched alias 继续下一候选。预检统一拒绝 repo 内外、relative/absolute、ancestor/final、多层、dangling、loop
symlink，再调用普通 resolver，保留显式 `task.json`、active task 和普通 archived `task.json` 的
既有优先级；仅普通 resolver 返回 not-found 时才进入 plan-only fallback。精确 archive locator
只尝试该候选，basename/
原 active locator fallback 必须只命中一个 archive 月份，多候选 fail closed。plan-only resolved
target 仍须等于 plan canonical archive locator；仅允许经结构验证的 Darwin 系统
`/var -> /private/var` 映射，不使用任意 `samefile` 或用户 alias 重锚。

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

Task work commit 不再由 Phase 3.4 直接 stage/commit。Fresh final Phase 2 check
通过后，workflow mandatory invoke `guru-create-task-commit`；该 skill 写入独立
`task-commit-plans/<sequence>.json`，由 AI 审查 scope、exact paths、消息与授权，再由
candidate validator 复用统一 parser，最后由 `create-task-commit` exact executor 仅提交
计划路径并验证 parent、raw message bytes、path set、unrelated preservation 与 hook
mutation。Candidate、stage 与 commit 边界会拒绝 merge/cherry-pick/revert/rebase/
sequencer/am 等非普通 Git state；mode `160000` 的 snapshot 会绑定 initialized、clean
submodule 的 worktree HEAD。Executor 在 exact stage 前重验该 HEAD，并将 artifact
OID 直接写入 mode `160000` index entry，而不是由 `git add` 从可变 worktree 重新
读取；普通文件、symlink、delete 也只从 artifact SHA-256/mode/delete
identity 构造 isolated exact index。Snapshot 以 `renamed_from` 和 `copied_from`
分开 rename/copy；只有 rename source 继承 destination 的删除/exact-stage
authority，copy source 不会因 relation 自动入 stage，自身 dirty 时必须独立
分类。Candidate self 只使用 validated in-memory plan 的 deterministic bytes。
真实 hook chain 在 detached transaction HEAD 上完成，全部
commit/postcondition 与 live preimage 校验通过后才发布 branch/index/result。Executor
持有真实 `index.lock` sentinel 穿过 conditional ref、candidate/live-index publication
和 rollback；final index bytes 通过独立 temp 在 sentinel 仍存在时发布，真实 `git add`
持续被阻断。CAS 后立即持有/复核 loose-ref guard，并用 candidate guard/精确 result
identity 做条件恢复；ref/index/result 已发布且 guards 仍持有时，最后一次 candidate
inode/content identity read 才是线性化点。该 read 前写入 C 会触发 ref/index rollback
并保留 C；read 后写入 C 是独立 later operation，executor 仍以 immutable commit blob
与 returned result digest 返回 `committed`，且不覆盖 C。
并发 ref/candidate ownership 丢失时保留第三方状态，不覆盖后再声称 exact restore。
因此未审查 C 不会进入真实 index/commit。`committed` 进入 Branch Review，`revision-required` 重入 skill，`blocked`
fail closed；finding fix 必须先重跑完整 Phase 2，并使用新的 plan sequence。

发布前 AI 必须生成或审查 PR body readiness。PR body 面向不了解 Trellis task 的
GitHub reviewer，而不是 Trellis session 内部摘要；应包含具体的 `变更摘要`、
`影响范围`、`验证结果`、`Review Gate`、`Issue 关闭范围` 和 `安全说明`。禁止用
“当前 Trellis task”“已提交实现与文档更新”“详见 artifact”作为主要摘要。
`trellis-finish-work` 的唯一 PR body 来源是当前 task-local `pr-body.md`；dry-run 与 formal
都必须通过 `--body-file <current-task>/pr-body.md` 直接传入。`--body-artifact`、外部同文文件、
脚本生成的 body fallback，以及从 readiness artifact 相对解析 `body_file` 均不属于 closeout
合同并 fail closed。脚本只校验客观结构、低信息量短语、close/ref 语义和 reviewed source
是否存在，不替代 AI 判断内容是否真实充分。`pr-body.md` 属于 task metadata，必须在 archive
前完成全部校验；archive 后 remote-only identity 直接把 GitHub PR body 的 UTF-8 digest 与
plan 比较，不再读取归档 task body。
PR body 还必须包含 `Docs SSOT` / `文档同步` 处理结果：本次策略、durable docs
更新或 no-update 理由、已 merge 的 task delta、仅保留 task history 的内容，以及
follow-up / 当前 PR limitation。脚本最多检查 section/key 是否存在，语义充分性仍由 AI
readiness review 判断。finish-work/archive 不做首次 Docs SSOT merge；gate 后新增 durable
docs、`.trellis/spec/`、source、tests、schema、config、scripts、preset、overlay、CI/CD、
deployment、migration 或 Makefile drift 必须回 Phase 2/3。

本仓库保留 merge commit。`format-merge-commit` payload 会输出
`merge_commit.subject`、`merge_commit.body` 和显式
`gh pr merge <pr> --merge --subject ... --body-file ...` 命令；传入真实 PR number 时
返回 `ready=true`。维护者合并 PR 时必须使用该 payload，不能使用
GitHub 默认 `Merge pull request #xx from ...` subject，也不能把中文 PR title
`完成：#xx ... (#yy)` 直接当作 commit subject。

## 维护原则

- 不修改 Trellis npm 全局包、`node_modules` 或上游 Trellis 源码。
- 不把业务仓库的私有规则写入通用 workflow。
- 中台知识检索和 durable docs SSOT 对齐规则维护在通用 workflow 中，具体业务仓库只保留 task 证据和必要的 docs 更新。
- 长期规则维护在本仓库的 marketplace workflow、preset、companion scripts 和 overlay 中。
- 目标业务仓库中的 generated copy 只是安装结果，不作为长期维护源。
- 当前 43 条 upstream namespace overlay 是有 removal owner 的冻结迁移例外，不是新增
  extension 行为的常规入口；新行为优先进入 Markdown workflow 或 canonical `guru-*`
  package。删除迁移必须保留 inventory audit entry，并由 #132 完成 physical removal。
- 修改 `trellis/presets/guru-team/overlays/` 后，先重新应用 preset 到本仓库 dogfood copy，再运行 drift check：

```bash
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/apply.sh \
  --repo . \
  --all-platforms
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

如果 preset 产生 `.new` 或 `.bak`，必须逐个检查原因并处理，不能静默提交。
`trellis update` 仍按 `.trellis/.template-hashes.json` 和 overwrite/keep/`.new`
语义管理 upstream-generated files；preset 对已知 managed asset 可能写 `.bak`。这两类
sidecar 都不构成 ownership 或迁移授权。


## Push 后远端 Marketplace 门禁

修改 marketplace/preset/overlay/schema/public API 的发布路径会在 branch push 后、`gh pr create` 前执行远端分支 `init`、preview、switch 和 preset reapply，记录 task-local `marketplace-verification.json`。缺失、失败、HEAD 不匹配或 stale artifact 会阻止创建 PR；该门禁不创建 tag，AI 仍负责 PR readiness 判断。
