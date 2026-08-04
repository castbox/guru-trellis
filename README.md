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
python3 - <<'PY'
import json
from pathlib import Path

installed = json.loads(Path(".trellis/guru-team/extension.json").read_text())
assert installed["extension"]["version"] == "0.6.5-guru.25"
assert installed["extension"]["target_trellis_cli"] == "0.6.5"
assert installed["source"]["ref"] == "v0.6.5-guru.3"
assert installed["source"]["commit"] == "dbcbbb2d2776a3952b643b6bcce0a2693d103273"
assert installed["source"]["tree_state"] == "clean"
assert installed["source"]["is_mutable_ref"] is False
PY
```

如果 `check-env` 输出的 `github_repo` 为空，或 JSON 中出现 `warnings` / `next_steps`，
说明 workflow 还不能可靠执行 GitHub issue intake 或 publish；按提示配置
`.trellis/guru-team/config.yml` 的 `github_repo: owner/repo`，或给当前 Git 仓库配置
GitHub `origin` remote。

`trellis --version` 与 `.trellis/.version` 表示官方 Trellis CLI / project template
版本；Guru Team extension 的版本和安装来源记录在
`.trellis/guru-team/extension.json`，并由 `check-env --json` 与 `version.sh --json`
输出。

当前 stable 发布映射为 repo release tag `v0.6.5-guru.3`、peeled source commit
`dbcbbb2d2776a3952b643b6bcce0a2693d103273`、Guru Team extension
`0.6.5-guru.25`、官方 Trellis CLI `0.6.5`。Workflow marketplace 与 preset 必须来自
同一个 immutable release tag；不要把 tag-pinned workflow 与 `main`、无 `#ref` 或其它
preset source 混装。维护者刻意采样最新 `main` / canary
时，可以去掉 `#ref` 或设置其它 branch/tag ref，但最终报告必须说明安装来源是
mutable ref 还是 immutable release tag，以及是否仍以官方 Trellis `0.6.5` 为目标基线。

本仓库也提供 throwaway 安装验证脚本，用来验证默认非交互路径是否仍可开箱运行：

```bash
./trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
```

Trellis CLI 支持 `gh:user/repo/path#ref` workflow marketplace source。该脚本默认验证
`gh:castbox/guru-trellis/trellis#main`，作为显式 mutable canary baseline。验证 feature
branch 或 release 时，必须把 `TRELLIS_WORKFLOW_SOURCE` 设置为已经存在于远端的精确
branch/tag `#ref`；只有该 ref 已 push 后的运行才能作为对应 ref 的 marketplace evidence。
在非 `main` 分支或本地 marketplace 文件有改动时，公开 `#main` sample 会 fail closed，避免
误报为当前分支验证。若当前 dirty branch 尚未 push，只能显式设置
`TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1` 来采样公开 `main`，并在结果中说明这是“公开
main marketplace + 本地 preset/runtime projection”，不是当前分支或 release tag 验证。
脚本还会用已安装的 wrapper、companion、schema、config、workflow 与官方
`task.py`，在初次安装和 `trellis update` + preset reapply 后各完成一次 dry-run digest、
formal draft、archive、三方 HEAD、ready 与 clean-tree 事务；不会把 canonical runtime
资产手工复制进 fixture。

维护者修改 preset、overlay、extension manifest 或公共 Skill package 前，还必须运行
source-only ownership gate：

```bash
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
```

该 gate 以 Trellis CLI `0.6.5` 为历史基线，保留 issue #128 的 43 条
path/baseline immutable identity；所有条目当前均为
`upstream_owned/removed` tombstone，其中 37 条属于 clean-init generated path，6 条属于
legacy-only path。每条 tombstone 显式保留 installer 迁移所需的历史 Guru payload hash，
但 preset 不再安装、声明或 managed-upgrade 这些路径。Validator 要求 active legacy 与
`unclassified` 均为 0、overlay tree 只含 3 个 Guru-owned `guru-finish-work` entry，并在
preset mutation 前阻止未知 managed claim、历史 identity 漂移或缺失 migration provenance。
这些 hash 只用于正常迁移和漂移识别，不是 authenticity/anti-tamper 边界，也不替代 AI
ownership、scope 或迁移充分性判断。

#### AI 安装 prompt

把这段 prompt 发给目标业务仓库里的 AI 会话：

```text
在当前 Repo 中安装官方 Trellis CLI v0.6.5，并从 stable release tag v0.6.5-guru.3 安装 Guru Team extension 0.6.5-guru.25。

要求：
- 先实时确认 npm 上 @mindfoldhq/trellis 的 latest 版本，不要凭记忆判断版本；如果 latest 已不是 0.6.5，本次仍按 Guru Team stable v0.6.5-guru.3 的目标基线安装 @mindfoldhq/trellis@0.6.5，除非我明确要求升级官方 Trellis 基线。
- 安装前检查当前 Repo 是否已经使用 Superpowers、Spec Kit、OpenSpec、GSD 或其它 SDD / agent harness；如果存在，不要继续安装 Trellis，先报告冲突并让我确认迁移或清理方案。
- 安装/升级全局 Trellis CLI 到 @mindfoldhq/trellis@0.6.5。
- 默认只启用 Codex 和 Cursor 支持。
- Guru Team preset 与 task workspace executor 不要求 developer name，也不要求 `TRELLIS_USER`、`-u` 或 `--user`。
- 如果当前 Repo 还没有 .trellis/，直接用 Guru Team workflow 的稳定非交互命令初始化：`trellis init -y --codex --cursor --workflow guru-team --workflow-source gh:castbox/guru-trellis/trellis#v0.6.5-guru.3`。
- 官方 Trellis 可能仍根据 Git config 创建 `.trellis/.developer` 与 `.trellis/workspace/**`；这是官方 identity/journal 行为，不是 Guru 前置。Guru apply/update/reapply 与 task workspace executor 不读取、不创建、不恢复这些路径，也不删除已有官方数据。
- 如果我明确要求交互式选择 spec template，才可以去掉 `-y`；默认安装和自动验收必须使用 `-y` 或显式 `--template <name>`。
- 获取与 workflow source 相同 immutable release tag 的公开 preset 仓库内容：`git clone --depth 1 --branch v0.6.5-guru.3 https://github.com/castbox/guru-trellis.git <guru-trellis>`。不得混用其它 tag、`main` 或无 `#ref` source；只有明确要跟随 latest/canary 时才可改用 mutable ref，并在最终报告中说明。
- 执行 `<guru-trellis>/trellis/presets/guru-team/scripts/bash/apply.sh --repo <current-repo> --platform codex --platform cursor`，把 Guru Team companion assets、`guru-*` discovery copies 和所选平台的 Guru-owned finish entry 应用到当前 Repo；如需 Claude，追加 `--platform claude`；如需启用全部受支持平台，改用 `--all-platforms`。Preset 不安装或覆盖 upstream-owned `trellis-*` entries、hooks 或 agents。
- 安装后检查是否存在 `.trellis/tasks/00-bootstrap-guidelines/`。这是 `trellis init` 生成的一次性 Repo 级 spec bootstrap 任务，用于把 `.trellis/spec/` 从通用模板改成当前 Repo 的真实工程规范；它不是每个 task 都要做，也不能作为安装副作用静默完成。先向我说明它的目的、将检查哪些源码/文档、将修改哪些 `.trellis/spec/` 文件，并询问我是现在让 AI 完成，还是保留该 task 后续单独处理。
- 业务项目内人类可读文档默认使用中文：`.trellis/spec/**`、`.trellis/tasks/**`、`docs/**` durable docs、`00-bootstrap-guidelines` 创建或补齐的 docs SSOT，以及 workflow artifact 的 summary/evidence/finding/PR title/body 等字段都写中文；命令、路径、配置键、GitHub keyword、API 名称、代码符号等 literal token 可保留英文。
- 只有在我明确确认现在执行 spec bootstrap 时，才扫描当前 Repo 的真实代码和文档，填充 `.trellis/spec/`、更新 `00-bootstrap-guidelines` checklist，并把这些改动纳入本次安装提交；如果我未确认，不要修改 `.trellis/spec/` 模板内容或 bootstrap task 状态。bootstrap 过程中如创建或补齐 `docs/**` SSOT 主文档，也必须按业务项目中文规则写作。
- 安装后确认 preset installer 没有创建未选择的平台入口目录；默认 Codex + Cursor 安装不应创建 `.claude/`。如果目标 Repo 历史上已经存在未选择的平台目录，例如 .claude/、.opencode/、.gemini/、.kiro/、.qoder/、.codebuddy/、.factory/、.pi/、.reasonix/、.kilocode/、.agent/、.devin/、.zcode/、.trae/ 等，说明这是历史残留或其它工具创建，并先请我确认是否清理。
- 运行最小验证：trellis --version、.trellis/.version、Trellis 上下文读取、Guru Team check-env、`.trellis/guru-team/extension.json`、Guru Team version；确认 extension version 为 `0.6.5-guru.25`、target CLI 为 `0.6.5`、source ref 为 `v0.6.5-guru.3`、source commit 为 `dbcbbb2d2776a3952b643b6bcce0a2693d103273`、`tree_state=clean` 且 `is_mutable_ref=false`。如果 check-env 的 `github_repo` 为空或输出 `warnings` / `next_steps`，必须明确报告需要配置 `.trellis/guru-team/config.yml` 或 GitHub origin remote。
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
- 先实时确认 npm 上 @mindfoldhq/trellis 的 latest 版本，并检查当前 trellis --version、which -a trellis、npm list -g @mindfoldhq/trellis --depth=0；如果 latest 已不是 0.6.5，本次仍按 Guru Team stable v0.6.5-guru.3 的目标基线安装 @mindfoldhq/trellis@0.6.5，除非我明确要求升级官方 Trellis 基线。
- 升级前检查当前 Repo 是否同时存在 Superpowers、Spec Kit、OpenSpec、GSD 或其它 SDD / agent harness；如果存在，不要继续升级 Trellis，先报告冲突并让我确认迁移或清理方案。
- 如果本机 Trellis CLI 不是 0.6.5，先安装/升级到 @mindfoldhq/trellis@0.6.5。
- 默认只保留当前 Repo 的 Codex 和 Cursor 支持。
- CLI 到达 0.6.5 后，先运行官方 `trellis update`，恢复 Trellis upstream-owned entries、hooks、agents 和 template-managed 文件；先检查现有本地改动，并逐个处理 update 产生的 `.new` / `.bak`，未知本地改动不得静默覆盖或删除。
- 官方 upstream ownership 恢复后，用 tag-pinned stable marketplace 生成 workflow 预览：`trellis workflow --marketplace gh:castbox/guru-trellis/trellis#v0.6.5-guru.3 --template guru-team --create-new`，对比现有 `.trellis/workflow.md` 和 `.trellis/workflow.md.new`；确认风险后运行 `trellis workflow --marketplace gh:castbox/guru-trellis/trellis#v0.6.5-guru.3 --template guru-team` 切换 active workflow。
- 获取与 workflow source 相同 immutable release tag 的公开 preset 仓库内容：`git clone --depth 1 --branch v0.6.5-guru.3 https://github.com/castbox/guru-trellis.git <guru-trellis>`。不得混用其它 tag、`main` 或无 `#ref` source。
- 最后执行 `<guru-trellis>/trellis/presets/guru-team/scripts/bash/apply.sh --repo <current-repo> --platform codex --platform cursor`，重新应用 Guru Team companion assets、`guru-*` discovery copies 和所选平台的 Guru-owned finish entry；如需 Claude，追加 `--platform claude`；如需启用全部受支持平台，改用 `--all-platforms`。Preset 不覆盖 upstream-owned `trellis-*` entries、hooks 或 agents。
- 如果 update 或 preset 生成 `.new` / `.bak`，逐个检查来源和处置结果；不要静默覆盖或删除未知本地改动，未解决 sidecar 时不得报告升级成功。
- 业务项目内人类可读文档默认使用中文：`.trellis/spec/**`、`.trellis/tasks/**`、`docs/**` durable docs、`00-bootstrap-guidelines` 创建或补齐的 docs SSOT，以及 workflow artifact 的 summary/evidence/finding/PR title/body 等字段都写中文；命令、路径、配置键、GitHub keyword、API 名称、代码符号等 literal token 可保留英文。
- 升级流程不要重新静默执行 spec bootstrap。若发现 `.trellis/tasks/00-bootstrap-guidelines/` 仍处于 active，或 `.trellis/spec/` 仍是通用模板，先报告这是尚未完成的一次性 Repo 级 bootstrap，并询问是否单独处理；未确认前不要修改 `.trellis/spec/` 模板内容或 bootstrap task 状态。
- 升级后确认 preset installer 没有创建或恢复未选择的平台入口目录；默认 Codex + Cursor 升级不应创建 `.claude/`。如果目标 Repo 历史上已经存在未选择的平台目录，例如 .claude/、.opencode/、.gemini/、.kiro/、.qoder/、.codebuddy/、.factory/、.pi/、.reasonix/、.kilocode/、.agent/、.devin/、.zcode/、.trae/ 等，说明这是历史残留或其它工具创建，并先请我确认是否清理。
- 运行最小验证：trellis --version、.trellis/.version、Trellis 上下文读取、Guru Team check-env、`.trellis/guru-team/extension.json`、Guru Team version；确认 extension version 为 `0.6.5-guru.25`、target CLI 为 `0.6.5`、source ref 为 `v0.6.5-guru.3`、source commit 为 `dbcbbb2d2776a3952b643b6bcce0a2693d103273`、`tree_state=clean` 且 `is_mutable_ref=false`。
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
- `trellis/presets/guru-team/ownership/`：43 条 removed upstream tombstone、历史 migration payload provenance 与 strict schema。
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
`guru-review-change-request`、`guru-create-task-workspace`、
`guru-approve-task-plan`、`guru-check-task`、`guru-create-task-commit`、
`guru-review-branch`、`guru-review-task-publication`、
`guru-verify-extension-installation` 与 `guru-finalize-task`。Active package 的
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

Public Skill interface 采用独立版本共存：1.2 是冻结的 legacy contract，1.3 是新建或
实质修改 I/O 的 minimal handoff target。Registry 1.1 的 active row 必须显式声明
`interface_schema_id` 与 `io_contract_state=legacy|minimal_handoff`，validator 按该 exact
pair 选 schema，不从文件或 optional 字段猜版本。#144 的 Interface 1.2 结论只描述冻结
历史 snapshot，不是当前 active
状态。当前十三个 active Skills / 51 exits 全部使用 Interface 1.3；
冻结的 `stage0-minimal-handoff-v1` 记录 `guru-sync-base`、
`guru-discover-change-context`、`guru-clarify-requirements`、
`guru-review-contract-wording`、`guru-review-change-request` 与
`guru-create-task-workspace` 六包、24 exits 的原始原子迁移边界，bytes 不再修改；
新增 `stage0-ai-first-contract-v2` 显式迁移当前六包到 23 exits，其中用户拒绝
workspace/task mutation 在 recorder/executor 前停止，不再产生 `cancelled` DTO；两代均使用
`guru-team-skill-interface-1.3 + minimal_handoff`；该 v2 migration 也显式声明
`guru-sync-base.repo_root` / `route` 从 required 变为可由 runtime 推导的 optional scalar。
独立 `production-minimal-handoff-v1` 冻结 `guru-approve-task-plan`、
`guru-check-task`、`guru-create-task-commit` 三包、十个 profiles 与 11 exits 的原始
output schema identities；`production-ai-first-contract-v2` 再显式迁移当前
`approved` / `passed` minimal DTO，并将旧 Task Commit message/path/semantic 输入一次性
投影为五字段 v2 owner-entry seed 与 ignored-runtime candidate；旧授权、caller 预选出口和
terminal result journal 不进入新合同，且不改写 v1 bytes。`guru-review-branch` 之后的
`guru-review-task-publication` 以两个 closed
profiles、三个 minimal exits 和唯一 task-local `pr-readiness.json` 负责 Phase 3.6
publication semantic gate；ignored-runtime `pr-readiness.json` 使用 schema 2.0，
`ready` 只向 active `guru-finalize-task` 投影
`exit_id/task_ref/reviewed_content_head`，Publication 不读取 Branch Review 私有
checkpoint。新增 active
`guru-verify-extension-installation` 以两个独立 input profiles、四个 minimal exits
和唯一 task-local-or-session private owner result 负责 extension installation
semantic gate。新增 active `guru-finalize-task` 以七个 distinct input profiles、
六个 `exit_id` outputs、owner-private `task-finalization-gate.json` 与既有 #105
transaction engine 负责完整 semantic closeout。当前 package closure 为 13 Skills /
51 exits，
`legacy_skill_ids=[]`；冻结 Stage 0 v1 manifest 保持 6 Skills / 24 exits，
AI-first v2 当前合同为 6 Skills / 23 exits；global workflow production markers 为
13/51/28。
Finish-family combined integration 由 canonical `guru-finish-work` 入口、两个 terminal
eval、checked #117 private projection bridge 与安装验收共同覆盖。Upstream
`trellis-finish-work` 文件由官方 Trellis 独占 ownership，不再属于 Guru overlay 或
installed managed inventory。

`guru-verify-extension-installation` 的 workflow input
`verification_required` 只携带 `task_ref/plan_ref/repo_ref/reviewed_head/
verification_target` 与固定 discriminator；active finalizer producer 与 #117 的
`verified` workflow re-entry 与可达的 task-bearing standalone `not_required`
re-entry 使用 target-owned authoring seed；后者只投影
`repo_ref/resolved_head/verification_ref`，由 finalizer target author
`profile/mode/task_ref`，plan identity 保持 private。Standalone direct
discovery 使用结构不同的
`standalone_verification`，只携带 repo、remote、ref、caller intent 与可选 task。
Skill 的 AI owner 判断 applicability、closed capability profile、adequacy、finding
与 route；changed paths、command exit 0、checker pass 或 production eval 都不能产生
`verified`。Task-bearing 调用只写
`marketplace-verification.json`，taskless standalone 只返回 session report，不写
cache/index/latest pointer，也不能返回 task-work route。

Branch Review `passed` 后，global workflow caller 先从 current reviewed evidence
编写 task-local `pr-body.md` 与 `finish-summary-index.json` 初始候选，再 mandatory
invoke active `guru-review-task-publication`。该 preparation 不判断内容充分性、Issue
closure、十维结论、finding route 或 ready；这些 semantic judgment 仍只属于
publication Skill。缺失或结构错误在 invocation 前失败关闭，Phase 3.7 不得在
`ready` 后首次创建、重写或修改这两份已绑定内容。Finalizer package 与 public edge
已 active，global `ready -> guru-finalize-task` invocation/order 与 Codex、Claude、Cursor
的 Guru-owned `guru-finish-work` 薄入口均已 integrated。入口只读取 live workflow 并调用
semantic owner，不直接调用 closeout engine；四类 machine recovery exit 自动消费。
Official `trellis-finish-work` 文件保持 upstream-owned，Guru preset 不安装、不修改也不管理。

Planning self-reentry、`guru-check-task:passed` 到 initial commit、commit
self-reentry、`guru-create-task-commit:committed` 到 active
`guru-review-branch`，以及 `guru-review-branch:passed` 到 active
`guru-review-task-publication`，连同 publication/finalizer/verification/recovery
family 共十二条 semantic edge 使用 target-owned
`skill_input_authoring_seed`。Producer 仍只用既有
`direct|select|rename|normalize` projection 生成 minimal seed；caller AI 独立编写其余
required semantic fields。Validator 证明 seed/authoring 字段不相交、union 精确等于 target
profile required set，并在无覆盖 merge 后验证完整 target schema。该 consumer kind 不新增
projection operation，也不允许 private-artifact lookup、default 或 runtime semantic
reconstruction。

Interface 1.3 分开声明 caller-owned structured/scalar input、package-local exact
invocation、每个 typed exit 的独立 output schema/example、consumer-owned
Skill/workflow/stop input、direct/select/rename/closed normalize projection，以及
runtime checkpoint/gate evidence private artifact。Skill consumer 必须引用相同 id 且
与 active registry exact canonical path 一致的 target-owned input；非 direct projection
与 direct 到 scalar CLI 必须证明 required 与映射/normalizer 后全域兼容，
public/private schema id/path 分别互斥；wrapper 必须完整匹配 dispatcher-only template。
1.3 closed schema 的 `pattern` 只接受 durable spec 定义的 printable-ASCII portable
grammar，并按 ECMA-262 Unicode-mode search 语义执行；Python-only regex、Unicode source
pattern 和未声明 shorthand 会在 source/installed validation 中 fail closed。
使用稳定 discovery 命令查看合同：

```bash
.trellis/guru-team/scripts/bash/discover-skill-contract.sh \
  --root . --mode installed --skill guru-sync-base --json
```

1.2 返回明确的 `legacy` variant；1.3 返回 `minimal_handoff` locator index。失败返回
stable `code`、repo-relative `field_path` 与 `remediation`。Mixed 1.2/1.3 fixture 只用于
contract tests，不进入 production registry、installed inventory 或 workflow route。
两个 production manifests 位于 `trellis/skills/guru-team/migrations/`；source/installed
validator 会把它们与 live registry、Interface、workflow markers、extension inventories、
十三份 corpora 及 selected-platform copies 双向比较。每个 migrated package 的
`scripts/invoke.sh` 是 dispatcher-only wrapper，normal Agent 只提交 caller-owned input
并在 semantic owner loop 完成后传入 repo-relative owner-result locator；runtime 重跑现有
checker 后从 checker-passed `typed_exit` 推导 route。调用方不能传入 expected exit，也不
读取/import shared Python runtime、private artifact body 或 public output example。

`guru-finalize-task` 的完整 step-local 行为位于 package
`references/contract.md`。它独占 canonical transaction-plan review、当前对话中的真实副作用确认、
recovery route、六个 typed exits 与 private gate；用户不复述 digest，deterministic runtime 只复用 #105
engine 执行/校验/记录。plan/digest 只绑定该 deterministic consumer，不是 semantic 或 workflow authority。`publication_review_stale` 保留 #116 owner checker 的
missing/stale/head-mismatch fact，由 AI 选择 route；无 plan 的 stale handback 不产生
closeout 副作用。Public DTO 不包含内部 transition、plan/readiness/verification、
PR/archive/recovery facts 或 digest。

Planning/check wrappers 复用既有 recorder/checker；commit wrapper 由 deterministic builder
物化 private candidate 后复用既有 validator/executor transaction。`committed` DTO 精确为
`exit_id`、`task_ref`、`base_ref`、`committed_head`，继续交给未改变的
`branch-review-or-finding-closure`；这是 #146 交付时的历史边界。#131 已将该 consumer
切换为 active `guru-review-branch`，同时保持 #146 的三包/11 exits activation identity 不变。

Interface 1.3 的每个 scalar argument 显式声明 boolean `required`；
`guru-sync-base --base-branch` 可省略，省略时直接进入同一 owner resolver 的 configured
scalar、ordered candidates、remote default 顺序。Active-task scope-change 的 checker-passed
`clear` 可把 `target_disposition=null` 固定投影为 `retained`，initial/standalone 不放宽。
Production eval 的 shared adapter 使用 preset 管理的本地 native executor；semantic case
引用 repo-local checker-passed owner result，actual exit 先选择 output schema，随后 runner
才比较 `expected_exit`。Codex 从 trusted Git root 执行，Claude 使用 safe non-interactive
协议，Cursor 未登录时确定返回 `unsupported`。

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

Active-task re-entry 先验证 exact `task_locator` 与固定
`prior_snapshot_locator=context-discovery.json`，owner result 与 checker 必须绑定同一 task。
Private `task_worktree_state` 绑定 current HEAD 与除 fixed snapshot/runtime 外的全部 dirty
path/status/content/mode/rename facts。Different-byte fixed snapshot 只有在 existing target 为
regular/trackable、prior identity 等于显式 expected digest、完整 new/live/worktree checks
通过后才由 `write_json` formal replace，并记录 `superseded_snapshot_sha256`；任何写前失败
保持 prior bytes，same-byte retry 幂等。

`guru-clarify-requirements` 统一 initial issue/proposed draft、active-task scope change 与
standalone review。Workflow/standalone 使用相同 preconditions 和 semantic 五阶段；Skill
验证 repository-answerable `answered` evidence、question lifecycle与objective payload/live
mutation；先穷尽 repository-answerable questions，且 `answered` 必须有checked evidence，再按每轮一个最高价值
问题收敛。每轮question id必须来自本轮opened或既有open set，reducer固定为
`open_questions = opened - closed`。只有不可分割产品选择才记录 `atomic_group`。Scope proposal 与 source action 都绑定 recorder 派生的 digest；
该 digest 只校验当前 bytes，不是 workflow authority 或授权证据。Material expansion 纳入
current scope 前必须完成一次对话内的真实产品/范围选择，普通“继续”、task/planning/review
approval 不得替代；选择过程不写入 artifact。Optional mechanism 产生的风险只能删除/替换
机制或另行提案。

Package 不提供 mutation executor。GitHub comment/body 只能由 AI 在当前对话完成 exact
副作用确认并复核 live preimage 后，通过现有 connector 或审查过的 `gh` 执行，
随后重读 live facts；recorder/checker 只规范化和校验 closed schema、derived digest、
freshness、reviewed payload/mutation/live content、active-task compact ledger 与 live owner linkage 及 typed exit，
不接收或记录授权。Pre-task/standalone stdout-only，
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
都必须有最终 decision；其中确有未决产品/范围选择的 classification 先在当前对话完成选择。
兼容字段 `decision_trail` exact 写入当前 `issue-scope-ledger.json.scope_decisions[]`，但它不是过程轨迹：
只记录 `trail_id`、最终 proposal id/digest/decision 与 live GitHub authority 的 kind/URL/content checksum。
用户身份、原话、时间、confirmation ref、authorization digest、planning/context/review/stale/interrupted/re-entry
等可重读事实均不得进入 ledger；checker 从各 owner 和 live authority 重新验证。旧 full-shape trail 由 recorder
一次性投影为 compact task-update payload，不要求新的用户选择或 GitHub mutation。`mechanism_removed/replaced` 要求 optional origin，不进入
trail 或 authority mutation。GitHub authority mutation 后必须先返回
`refresh_context`；context `generated_at` 不早于 live authority `updated_at` 后，task update 的 preimage
必须等于当前 context snapshot digest，不要求第二次 context refresh。
Active-task `new_task` 持久化同一 compact classification，只向 #112 返回 side-effect-free reviewed draft。

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

例如当前 `v0.6.5-guru.3` 表示“针对官方 Trellis `0.6.5` 的 Guru Team 第 3 个 repo
发布修订”。同一个官方 Trellis 基线下，repo release tag 可用 `.3`、`.4` 递增发布兼容修订；只有切换官方
Trellis 基线时才移动前缀，例如未来的 `v0.6.6-guru.1`。

Guru 修订号按兼容性维护：

- patch：兼容 bugfix、文档澄清、非破坏性 guardrail 修正；
- minor：兼容新增字段、script 能力、platform overlay 或可选门禁；
- major：破坏 workflow id、script CLI、artifact schema、installed path、默认行为或升级语义。

本仓库的 release tag 使用 repo 级 tag，例如 `v0.6.5-guru.3`。Repo release tag 与
`trellis/guru-team-extension.json.version` 是两个独立版本轴：tag 标识可安装的 immutable
仓库发布快照，manifest version 标识 extension 内部修订；发布元数据必须把 tag 精确映射到
tagged commit 中实际存在的 manifest version，不能假定两个后缀相等。该 manifest 同时用
`target_trellis_cli` 记录目标官方 Trellis CLI 版本。稳定安装文档使用
`gh:castbox/guru-trellis/trellis#v0.6.5-guru.3`。不带 `#ref` 的
`gh:castbox/guru-trellis/trellis` 只表示 latest/canary，不应用作需要复现的问题定位坐标。
发布顺序必须是：先 merge 包含 manifest/docs 更新的 PR，再在 merge commit 上创建并 push
annotated tag `v0.6.5-guru.3` 这类 release tag，验证 `trellis init` / `trellis workflow`
的 tag-pinned 安装后，再退休旧 tag 名称。

当前已发布、可复现的 stable 映射是：annotated tag `v0.6.5-guru.3`，peeled source
commit `dbcbbb2d2776a3952b643b6bcce0a2693d103273`，canonical extension version
`0.6.5-guru.25`，target Trellis CLI `0.6.5`。Workflow marketplace 与 preset 必须 pin
同一个 `v0.6.5-guru.3` immutable tag。

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
issue、搜索重复候选，并输出 proposed issue、base branch、branch name、portable
workspace/task slug 和 `naming_quality`，但不会创建 GitHub issue、worktree、branch、
Trellis task、task-local artifact 或 gitignored `.trellis/.runtime/guru-team/**`
mapping。新任务不生成 `task-start-context.json`。没有 source issue 的 freeform 请求必须先由 AI 展示
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
Passed Gate + confirmed 才可 mutation；用户拒绝时在 recorder/executor 前停止，不生成
plan、result 或 public DTO。`reroute` 返回 `refresh_review`，`blocked` 返回 `blocked`，
两者均由 checker 验证 zero-write snapshot。

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

创建成功后，除 official Trellis `task.json` 外只写一个 Guru-owned tracked Intake artifact：
`issue-scope-ledger.json`。Plan/result 位于 ignored runtime 且不含 absolute workspace path，
本机 mapping 只位于 ignored
`.trellis/.runtime/guru-team/**`。Checker 从 current config、reviewed slug 与 live Git facts
推导 worktree。A/B fixture 从同一
clean base 分别走 production recorder/executor/checker、task-local archive/commit，再验证
A -> B 和 B -> A 两个本地 merge 顺序均无 Guru metadata conflict；不创建远程 PR或并发进程。

`workspace_mode: worktree` 下的 task artifact 写入边界由 current `task.json`、当前 checkout、
`.trellis/.runtime/guru-team/**`、`git worktree list` 和 boundary helper 共同推导/校验。
既有 active task 的 `task-start-context.json` 只作为一次性只读兼容输入，不是新任务依赖或
新 artifact。AI 或 main session 在写入/校验
`planning-approval.json`、`phase2-check.json`、`review-gate.json` 等 owner-private
ignored-runtime checkpoint 前，应从目标 worktree 运行：

```bash
.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task <task-path>
```

该 helper 只报告 expected workspace、actual repo root、source checkout status、task
worktree status 和 source checkout 中可疑同名 task artifact/review metadata；它不判断
sub-agent 是否 stale，不迁移误写 patch，也不清理 source checkout。若编辑工具不能显式传入
`workdir`，必须使用 boundary helper 已确认的当前 task worktree 下的绝对路径，不能从
committed task context 拼出本机路径。
这层 workspace boundary 只提供当前 checkout/task worktree 的确定性事实，不承担
sub-agent 存活、进展或 stale 判断。

`no_task` 下不是绝对禁止当前 checkout 直接修改，但这只能作为用户显式批准的 override：
用户必须明确表示本轮跳过创建或复用 GitHub issue、Trellis task、worktree 和 branch。
AI 在改文件前要说明将跳过哪些 artifact、当前 checkout / branch / dirty state、预期
副作用和 changed-file scope；这个批准不包含 commit、push、PR 或 issue close。

用户仍然需要记住的常用显式入口是：

- `trellis-continue`
- `guru-finish-work`（Claude 使用 `/guru:finish-work`，Cursor 使用
  `/guru-finish-work`；Codex 使用同名 prompt）

`trellis-finish-work` 是官方 Trellis 入口，不属于 Guru preset ownership；Guru Team
日常收尾只使用 `guru-finish-work`。

`trellis-start` 仍保留为 fallback / explicit orientation 入口，用于平台没有自动
session/startup 注入、hook 未启用或未审批、怀疑自动注入没有运行，或用户需要完整
上下文报告和重新加载 Trellis 上下文的场景。

`check-workspace-boundary`、`resolve-human-artifacts`、`record-planning-approval`、`check-planning-approval`、`record-phase2-check`、
`check-phase2-check`、`record-agent-recovery`、`check-agent-recovery`、`review-branch`、
`check-review-gate` 是 workflow 内部 companion script；
`publish-pr` 仅保留为兼容性阻断入口。它们都不是需要用户日常手动记忆的新主流程。
`guru-approve-task-plan` 是 Phase 1 planning approval 与唯一
`planning-approval.json` 的 semantic owner；global workflow 只 mandatory invoke stable id、
消费 `approved` / `revision_required` / `clarify_scope` / `blocked` 四个 typed exits，并让
`approved` 唯一进入 task activation。`clarify_scope` 只进入三字段 routing-only workflow
target `guru-task-plan-clarify-scope-router`；router 建立 scope context 后 mandatory invoke
`guru-clarify-requirements:active_task_scope_change`，完整 semantic input 由 caller AI 基于
fresh live context 编写。Installed recorder/checker 只记录已完成的 AI result，并校验
`guru-planning-approval-3.0` schema、task/planning locators、非空文件与 closed union，不执行
adequacy、provenance、authorization 或 route 判断。必要授权只存在于当前会话，不进入
checkpoint、archive 或 public DTO。Active schema 1.2/2.0 只作为 re-entry signal；新流程不会
重建旧 digest/confirmation chain。
Planning public wrapper 在 checker-passed typed DTO 通过 output schema 后删除自己的
`planning-approval.json`；task activation 与 Phase 2 只消费 DTO 和当前 planning/live facts。
`task.py start` 只写状态，不代表规划已审查。
`resolve-human-artifacts.sh` 为阶段回复提供确定性路径事实：规划停止、Phase 2 完成、
Branch Review Gate 结果、finish-work dry-run 和最终 archive/publish 回复都应先运行它，
然后输出 `Markdown 产物 review 表`。标准表只列 `prd.md`、`design.md`、
`implement.md`、`pr-body.md` 四个 Markdown；缺失文件不生成 Markdown 链接，JSON
gate/evidence 不进入默认表。
Phase 2 在 unchanged official `trellis-check` / channel `check` 收集 raw evidence
后 mandatory invoke active semantic Skill `guru-check-task`。该 Skill 是 scope
qualification、adequacy、finding/full-rerun loop、Docs SSOT review、四出口和唯一
`phase2-check.json` 的 owner；新 artifact 使用 closed schema
`guru-phase2-check-3.0`。`record-phase2-check.sh` / `check-phase2-check.sh` 只记录和
校验 AI-authored closed result 的确定性事实；worker 输出、coverage flags、验证命令
或脚本成功都不能生成 Guru pass。
3.0 只保留 `checked_head`、reviewed paths、实际 validation、Docs SSOT、九个 adequacy
维度、finding lifecycle 与 typed route；routine assignment、handoff、recovery transcript、
raw worker payload 和 digest bundle 不进入 checkpoint。Checker 只校验 closed schema、
task/HEAD freshness、当前 dirty-path coverage、finding/scope linkage 与 exit/consumer union。
Codex 项目默认使用 `codex.dispatch_mode: sub-agent`，由 main session 调度
`trellis-implement` / `trellis-check`；sub-agent 通过 dispatch prompt 首行
`Active task: <task path>` 或 `task.py current --source` 加载上下文。默认 sub-agent
mode 下有三个强制执行边界：实现由 `trellis-implement` / channel `implement`
完成并返回 concise terminal result，不创建独立 handoff artifact；Phase 2 check 由 `trellis-check` / channel `check`
完成并输出可支撑 `phase2-check.json` 的 terminal evidence；commit 后 Branch Review
由独立 review sub-agent 审查完整 `origin/<base>...HEAD` diff，并把最小 terminal
findings/evidence 返回 semantic owner。main session 只协调、在真实 unfinished 时恢复/
替换、记录 compact gate、commit 和运行 recorder/validator；不能把自己的实现、自检、自审或脚本校验通过冒充上述 sub-agent
边界。只有显式配置 `codex.dispatch_mode: inline` 或已有明确 artifact evidence 的
self-exemption 时，Codex 才降级为 main session 直接实现和检查；缺少 implement/check/review
sub-agent evidence 时默认 fail closed。
项目级 `trellis-implement` / `trellis-check` / `trellis-research` 与 channel runtime agent
定义由官方 Trellis init/update/upgrade 管理。Guru preset 不再安装、覆盖或
managed-upgrade 这些 upstream files；它只安装 canonical `guru-*` package discovery
copies。平台原生 agent 的技术 id、description、nickname 与运行协议以当前官方 Trellis
版本为准，mandatory Guru route 由 `.trellis/workflow.md` 的 stable markers 保证。
routine sub-agent dispatch、等待、进展和每轮 review 不持久化。`wait_agent`、
`trellis channel wait` 或等价等待命令 timeout 只表示本次等待窗口未返回结果，AI 在
workflow 内继续观察或重入，不向用户索要“确认继续”。只有 agent 明确 unfinished 且必须
由 replacement 接手时，main session 才通过 `record-agent-recovery.sh` 写 ignored
`.trellis/.runtime/guru-team/agent-recovery/<task-key>.json`，记录一次 `unfinished` 和一次
`replacement` 的最小 reason/handoff；`check-agent-recovery.sh` 验证这条真实 recovery 链。
该 checkpoint 不进入 task artifact、commit、public DTO 或长期 archive。
`phase2-check.json` 是 Guru Team 固化 `guru-check-task` semantic check 的 owner-private
短生命周期 checkpoint，只包含 reviewed paths、validation、Docs SSOT、scope decisions、
adequacy、findings 和 typed route；脚本成功不能替代 Skill 的 AI Review Gate。Phase 2
public wrapper 校验 typed DTO 后删除自己的 checkpoint，Task Commit 只消费
`task_ref + checked_head` 与 live Git，不读取或代删上游私有状态。
Active `guru-review-branch` 是唯一的 Phase 3.5 semantic owner。Global workflow 通过
package Interface 的 target-owned authoring seed 形成 `profile`、`mode`、`task_ref`、
`base_ref`、`committed_head`、`review_intent` 六字段 public input，并消费
`passed`、`implementation_required`、`scope_confirmation_required`、`blocked`
四个 typed exits；官方 `trellis-continue` entry 不属于 Guru managed surface，也不复制
finding qualification、reviewer lifecycle、Docs SSOT
Gate、recovery checkpoint 或 revision 规则。

`review-branch.sh` 与 `check-review-gate.sh` 是该 package 拥有的 deterministic
recorder/validator implementation details：只在 AI Review Gate 已完成后记录或验证
task-local private evidence，不能判断 scope、finding、充分性、pass 或 route。完整 lifecycle、
private artifact 与 re-entry 合同只在 canonical package/spec 中维护。
Branch Review public wrapper 在 typed DTO 校验后删除自己的 private gate；Publication 只消费
该 DTO 与 live Git，不读取或代删 Branch Review checkpoint。
`trellis-continue` 不得 push 分支、创建 PR、调用 `publish-pr` 或调用
`finish-work`，也不得提交 `review-gate.json` 等 Trellis metadata。
PR 发布只从显式 canonical `guru-finish-work` 薄入口开始：该入口先按 live workflow 调用
`guru-review-task-publication`，仅从 `ready` 进入 `guru-finalize-task`。Finalizer 的私有
preview 生成 canonical `closeout_plan` 与 local digest；该 digest 只绑定 deterministic executor。
语义 Gate 在当前对话完成真实副作用确认后才执行
reviewed content push、按需 marketplace verification、draft PR、final archive
projection、单次 archive metadata commit/push、三方 HEAD 对齐与 draft-to-ready。裸
`finish-work.sh` 默认拒绝普通直接调用，`publish-pr.sh` 无条件阻断；中断由同一 finalizer
自动消费 recovery route，不暴露内部 flag 或要求用户选择下一条命令。

prepare 使用已安装的官方 config parser 读取 `.trellis/config.yaml`：只支持缺失或空
`hooks.after_archive`，非空、歧义、不可读、含 NUL 或 symlink 配置在任何副作用前拒绝，
且不会执行 hook。official move 前再次核对实时 archive 月份、空 index、精确 untracked
集合、所有 tracked regular-file/mode/blob continuity；失败时 task 保持 active、PR 保持
draft。若 schema 1.2 plan 在 task 仍 active 时跨月，same entry 必须重新 dry-run、审查
新 digest 并只替换 still-untracked plan；不创建 plan/readiness evidence commit、不 rewrite history、
不迁移目录。已持久化 schema 1.0/1.1 plan 的 committed supersession 仅保留在兼容路径。
共享 prepare 从 archive root 到 month/final destination 对每个既有组件逐层 `lstat`，
不读取或跟随 symlink target，任何 symlink（含 dangling、repo 内 target）都拒绝；计划
final locator 还必须不存在。official move 前重复同一检查，阻止 prepare-to-move 漂移。
`task.json.children` 缺失按空 list 处理，否则必须为 `list[str]`。按官方 active task
exact/suffix lookup，只有仍会被 archive 改写 `task.json` 的 active child 阻塞，已归档
child 作为历史关系不阻塞 parent closeout。

Finalizer 的 private preview 是无副作用 readiness step：它校验 AI 已审查的
`finish-summary-index.json`、PR body、gate 与 dirty state，并输出 canonical plan、digest、
future archive mapping、metadata allowlist 与 transitions；
不会移动或写入文件、创建 commit、push 或创建 PR，也不存在 journal/workspace 计划。
Schema 1.2 将 active transaction state 与长期 history 分层：10 文件 core compatibility
allowlist 包含 `task.json`、三份 planning 文档、scope ledger、既有 task-local Planning/
Phase 2/Branch Review artifact、closeout plan 与 finish summary；新 AI-first task 通常只
保留其中 7 个 durable 文件。仅在 marketplace verification 适用时保留第 11 个 verifier
artifact。Publication readiness 与 Finalizer gate 为 ignored runtime，不进入 archive；其它
intake/context、legacy assignment/liveness、commit plan、raw review 与 PR preparation 也不
复制进 archive tree。已持久化 schema 1.0 保留原 full-move，schema 1.1 保留旧 evidence
commit 与 11+1 文件上限，均只走兼容路径。
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
archive 前 recovery 使用 untracked schema 1.2 plan、live Git/GitHub、marketplace owner 与
task-local body/summary facts。official move 后、精确 archive commit 尚未形成时，先幂等完成 compact prune，再严格校验
retained working-tree 布局、dirty/staged path、blob continuity、pruned-path absence 与官方
`task.json` delta；commit 缺失或不匹配继续 fail closed。一旦当前
`HEAD` 已是精确 archive commit，普通 archived task 和 plan-only recovery 都从该 commit blob
读取 plan，只以 committed plan blob 和 Git parent/path/tree/blob lineage 作为 deterministic recovery input，
本地 archived 文件缺失、篡改及其 dirty state 不阻塞 exact push、远端 title/body digest、三方 HEAD
或 draft-to-ready。plan-only archived directory 只允许 `guru-finish-work` 恢复入口解析，普通 task
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
plan-only 恢复不会把缺失 context 当作 boundary 豁免：它从当前 commit blob 读取 committed plan，
在任何 GitHub/fast-path 动作前校验 Git toplevel、配置和effective remote repo、当前head branch、
base ref、current HEAD transaction、expected digest、task identity 与 active/archive locator。普通 task
discovery、workspace boundary 和其它命令继续要求 `task.json`；worktree mode 的边界由
current task、ignored runtime mapping 与 Git worktree facts 解析，旧
`task-start-context.json` 仅作一次性只读兼容输入。
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
通过后，workflow mandatory invoke `guru-create-task-commit`；该 skill 在 ignored
`.trellis/.runtime/guru-team/task-commit-plans/<task-key>/<sequence>.json` 写临时
candidate，由 AI 审查 scope、exact paths、消息与机械约束；随后展示唯一 commit 副作用并
只在当前对话取得确认，再由 exact executor 验证并提交计划路径。candidate 不含授权信息、
永不 stage，commit 成功后删除；executor 只返回 Git 可推导的
`pre_commit_head` 与 `commit_sha`，不再把 `committed/result/tree_evidence` 回写 tracked
handoff，因此成功提交不会主动制造 post-commit dirty。失败时 private candidate 可用于
同一未完成操作的 bounded recovery。既有 tracked plan 仅作只读迁移证据；finding fix
必须先重跑完整 Phase 2，并使用新的 plan sequence。

发布前 AI 必须生成或审查 PR body readiness。PR body 面向不了解 Trellis task 的
GitHub reviewer，而不是 Trellis session 内部摘要；应包含具体的 `变更摘要`、
`影响范围`、`验证结果`、`Review Gate`、`Issue 关闭范围` 和 `安全说明`。禁止用
“当前 Trellis task”“已提交实现与文档更新”“详见 artifact”作为主要摘要。
canonical `guru-finish-work` route 的唯一 PR body 来源是当前 task-local
`pr-body.md`；dry-run 与 formal 都必须通过
`--body-file <current-task>/pr-body.md` 直接传入。`--body-artifact`、外部同文文件、
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
- 43 条历史 upstream path 只保留为 `upstream_owned/removed` inventory tombstone；overlay
  tree 只含 3 个 Guru-owned `guru-finish-work` entry。新行为进入 Markdown workflow 或
  canonical `guru-*` package，不得重新引入 upstream namespace overlay。
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

修改 marketplace/preset/overlay/installer/schema/public extension contract 时，由
active semantic `guru-verify-extension-installation` 独占 applicability、capability
profile、adequacy、finding 与 route。Deterministic runtime 只对已推送 remote ref
冻结 HEAD，并执行 clean new-repo init、existing preview/switch、preset
apply/reapply、`trellis update` 后再次选择/apply、ownership/sidecar、Skill contract、
四平台 bytes、README command 与 redaction 检查；它不会把 exit 0 翻译为语义通过。

稳定 runtime command 是 `execute-extension-verification`、
`record-extension-verification`、`check-extension-verification` 和
`invoke-extension-verification`。Package wrapper 仍只经 `run-skill-command` 调用。
可先发现 installed contract：

```bash
.trellis/guru-team/scripts/bash/discover-skill-contract.sh \
  --root . --mode installed --skill guru-verify-extension-installation --json
```

Standalone 调用由所选平台发现 Skill 后完整执行 AI review、executor、recorder、
checker 和 public wrapper；不要把 package example 或 caller-selected
`expected_exit` 当作 owner result。Workflow `verified` 与 task-bearing standalone
`not_required` 桥接 active `guru-finalize-task`；workflow-shaped not-required schema
保持兼容，但 applicability conflict 不能产生该 exit。`return_to_task_work` 回到
Phase 2，`blocked` 停止。
Workflow-required target 若 AI 判断 `not_required` 会以 applicability conflict
失败关闭，不能静默跳过。

Package-local seven-case real-wrapper production eval 与真实 pushed-remote clean
installation 是两份独立验收。只有 exact remote ref/HEAD 的后者完成后才能声明远端门禁
通过；local/dogfood 或 public stable sampling 不能替代。该 gate 不创建 tag，也不能单独
替代本地 43-tombstone、installer migration、update/upgrade/reapply 与 zero-sidecar combined
acceptance。

### Skill 行为评测（#147）

Guru Team extension 提供 versioned package-local eval contract 与两个稳定命令：

```bash
.trellis/guru-team/scripts/bash/discover-skill-evals.sh --root . --mode installed --skill <interface-1.3-skill> --json
run_root="$(mktemp -d)"
.trellis/guru-team/scripts/bash/run-skill-evals.sh --root . --mode installed --skill <interface-1.3-skill> --adapter shared --run-root "$run_root" --json
```

Schema id 为 `guru-team-skill-evals-1.0`；adapter 为 `shared|codex|claude|cursor`；
status 为 `passed|evaluation_failed|execution_error|unsupported`。Deterministic
grader 不生成 semantic pass，human feedback 不能覆盖机械失败，run evidence
只写显式 repo 外临时目录。Runner 从已安装 descriptor 执行对应的
`shared.sh|codex.sh|claude.sh|cursor.sh`，再从 `PATH` 检测
`guru-team-shared-eval|codex|claude|cursor-agent`；不需要隐藏
`GURU_TEAM_*_EVAL_EXECUTABLE`。`shared` 要求 caller 提供实现 documented request/context
CLI 的 `guru-team-shared-eval`，其它三者使用各自非交互 native CLI。Discovery 的
`native_available` 可用于预检；缺失 native command 返回 `unsupported`。Runner 在 native
execution 外读取 canonical corpus；Adapter 只将 repo/package 外 public-only Skill projection、
prompt、staged files 与最小 request 写入隔离 context，不传 canonical package/corpus/private
runtime locator。Native CLI 通过 trace helper 读取 projected `SKILL.md`、调用 exact wrapper。
只有 request/projection/Skill/wrapper-digest-bound receipt 的
wrapper stdout 与返回 DTO 一致时才产生 trace invariant；合法 DTO 无 receipt 为
`execution_error`。Schema id 为 `guru-team-skill-eval-native-trace-1.0`，transcript 记录
native argv、stdout/stderr、context 与 receipt locator；四平台 projection 内 eval/private
runtime raw read 必须真实失败。十三个 active packages 维护唯一 canonical
corpora 并覆盖全部 51 exits/input profiles；Stage 0 AI-first v2 的独立
23-exit current corpus closure 保持不变，冻结 v1 manifest 仍为 24 exits。
执行 `trellis update` 后需重新应用
workflow/preset，运行 source/installed/platform checks 并清理所有 `.new`/`.bak`。
