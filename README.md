# Guru Trellis

Guru Trellis 为业务研发仓库提供 Guru Team 的 AI 协作流程。它在 Trellis 框架上补充
需求澄清、规划、实现检查、独立审核和交付收口，让 Codex、Claude Code、Cursor 等
工具使用同一套团队约定。业务仓库保留自己的需求、设计和工程规范。

流程由 Markdown workflow 和 Skills 定义，AI 负责判断，脚本执行和校验确定性事实。
用户在真实选择、范围变化或外部副作用前参与确认。

## 快速开始

### 让 AI 安装

在目标业务仓库打开 AI 会话，复制以下请求：

> 请从 https://github.com/castbox/guru-trellis 安装 Guru Team Trellis。
> 使用正式发布 tag，并让 workflow 与 preset 来自同一 ref。先检查现有研发流程、
> 本地定制和需要的平台，再展示安装影响。从所选 Guru checkout 的 source lock
> 获取并构建匹配 Fork，按本文入口安装并做定向验证。保留未知修改；安装不包含
> commit、push 或 PR。若生成 `00-bootstrap-guidelines`，请说明它的用途，另行确认
> 是否完善项目规范。

仓库已采用另一套完整研发流程时，先评估迁移方式，再安装。

### 命令行安装新仓库

准备 Git、Bash、Python 3、Node.js，以及所选 Fork 要求的 Node 版本和锁定的 pnpm。
GitHub Issue、PR 等操作还需要已安装并登录的 GitHub CLI（`gh`）。
Guru 的 GitHub 操作使用显式绑定仓库的 `gh` / `gh api`；Git 传输使用 `git`。

先从 [Releases](https://github.com/castbox/guru-trellis/releases) 选择正式 tag。
以下示例使用已发布的 `v0.7.0-guru.8`；目录按本机情况设置：

```bash
GURU_REF=v0.7.0-guru.8
GURU_SOURCE=/absolute/path/to/guru-trellis
FORK_SOURCE=/absolute/path/to/Trellis
TARGET_REPO=/absolute/path/to/business-repo
GURU_WORKFLOW_SOURCE="gh:castbox/guru-trellis/trellis#$GURU_REF"

git clone --branch "$GURU_REF" --depth 1 \
  https://github.com/castbox/guru-trellis.git "$GURU_SOURCE"
```

已有 Guru checkout 时复用并核验所选 ref。然后按
[构建所选 Fork](trellis/presets/guru-team/README.md#构建所选-fork)
读取该 Guru checkout 自身的 lock、取得源码并完成构建。完成后在新业务仓库执行：

```bash
(
  set -e
  cd "$TARGET_REPO"
  node "$FORK_SOURCE/packages/cli/bin/trellis.js" init -y \
    --claude --codex --cursor \
    --workflow guru-team --workflow-source "$GURU_WORKFLOW_SOURCE"
  cd "$GURU_SOURCE"
  bash trellis/presets/guru-team/scripts/bash/apply.sh --repo "$TARGET_REPO"
)
```

按实际工具选择 init 的平台 flags；示例选择 Claude、Codex、Cursor。
`-y` 避免交互式 spec 模板选择。marketplace 只安装 `.trellis/workflow.md`，
完整 preset 才安装 Guru Skills、运行环境和所选平台入口。
单独复制 Skill 目录不能运行完整扩展。

安装后让 AI 运行 `.trellis/guru-team/scripts/bash/check-env.sh --json`，
检查 workflow/preset 来源、受管文件与所选平台投影，并处理
`.new` / `.bak`。若无法推断 GitHub 仓库，先设置 GitHub `origin` 或
`.trellis/guru-team/config.yml`，再使用 Issue 和 PR 功能。
详细安装与验证见 [preset 指南](trellis/presets/guru-team/README.md#apply-and-verify)。

`00-bootstrap-guidelines` 是一次性的项目规范初始化任务。安装不自动完成它；
AI 应先说明拟写入 `.trellis/spec/` 的内容，再确认现在执行或留待后续。
业务仓库的规范、需求设计、任务人类可读内容和 PR 说明默认使用中文。

## 来源与版本选择

<a id="guru-team-extension-version"></a>
<a id="发布身份边界"></a>

正式业务使用优先选择已发布 tag。当前已发布稳定版本为 `v0.7.0-guru.8`。
当前 canonical extension 与维护目标为 `0.7.0-guru.9`，处于未发布的完整来源准备阶段。
快速安装继续使用已发布 `.8`；源码版本更新不证明 `.9` 已发布或真实 dogfood 已采用。

- **稳定安装**：workflow marketplace 与 preset checkout 使用同一个正式 Guru tag。
- **候选试用**：两者使用同一个真实、远端可寻址的完整 Guru commit SHA。
  分支会变化；未发布 candidate 不作为业务仓库的默认安装版本。
- **框架来源**：从所选 Guru checkout 自身的
  [`trellis-source.json`](trellis/presets/guru-team/source/trellis-source.json)
  读取 `castbox/Trellis` repository、commit、CLI version 和 package manager。
  目标投影为 `.trellis/guru-team/trellis-source.json`。

Guru tag、extension revision、Fork commit/CLI 版本是不同的版本轴。
始终构建所选 lock 的 Fork，保留正常 workspace 依赖布局和模板 mode。
不要以同版本旧 tarball、全局 stock CLI 或可变 `latest` 替代匹配构建。
框架维护通过锁定 Fork 的公共入口进行，不运行 stock `trellis upgrade`。

本页不另存 Fork SHA/CI 对照表。source lock 和 CI 成功只说明各自绑定的来源与结果，
不证明本地 build、业务安装、实际 Agent 行为或 Release 已验证。
已发布 tag 也不自动包含当前源码中的修复。
当前准备先交付完整来源，再由后继 Delivery 经原升级 owner 实际采用。
来源验证和临时安装样本不替代实际采用、Task Completion 或正式发布门禁。

## 升级已有仓库

把本仓库地址、目标版本和升级目的交给业务仓库中的 AI。
AI 从**完整匹配的目标 Guru 来源**加载对应 Skill，先核对实际安装与定制：

| 目标 | 入口 |
| --- | --- |
| 单 checkout 更新工具、workflow、Skills 和受管投影，保留 Task/session 状态 | [guru-upgrade-tools](trellis/skills/guru-team/packages/guru-upgrade-tools/SKILL.md) |
| 完整旧安装升级，包含所需 Task/schema 迁移 | [guru-upgrade-installation](trellis/skills/guru-team/packages/guru-upgrade-installation/SKILL.md) |
| 单独维护所选旧 Task 或人工历史归档 | [guru-maintain-legacy-task](trellis/skills/guru-team/packages/guru-maintain-legacy-task/SKILL.md) |

例如：

> 请按 `guru-upgrade-tools` 将当前 checkout 的 Guru 工具更新到我选择的版本，
> 保留 Task/session 和业务定制。先核验同源 Guru/Fork 与实际目标，再展示写入范围。
> 若存在旧失败事务，先由其原 owner 按原 source pair 和冻结计划合法处置。

升级步骤、冲突、验证和恢复规则由所选 Skill 独占。
旧失败事务不要求回到原聊天；接续仍须使用原 owner、原 source pair 和原冻结计划。
需要改用修复来源时，先按原合同处置旧事务，再从新来源重新准备，不能换源直接 resume。

官方 update 后仍需更新匹配的 marketplace workflow 并 reapply 完整 preset。
workflow `--create-new` 只生成预览；实际替换使用同一 provider 的显式 `--force`。
这些动作由升级 owner 编排，不能用普通 apply 绕过旧 Task 或迁移前置。
保留本地定制并解决 `.new` / `.bak`，验证真实安装后才报告成功。

## 日常使用

安装后直接向 AI 描述需求。AI 读取业务仓库的 `.trellis/workflow.md` 和相关 Skills，
根据当前任务状态接续；通常无需记忆阶段编号或内部产物名称。

- **开发需求**：描述目标、约束和验收预期。AI 判断采用标准 Intake 或有界 task-free。
  可明确说“这次走 task-free”；创建资源和 Git/GitHub 副作用仍单独确认。
- **独立审核**：说明要审核的改动、分支、PR 或路径。
  [guru-review-change](trellis/skills/guru-team/packages/guru-review-change/SKILL.md)
  承接代码、测试覆盖和需求实现审核。正式提交后完整 Review、Completion
  由 workflow 调用或明确的正式阶段请求进入。
- **交付收口**：使用当前平台的 `guru-finish-work` 入口，由 workflow 接续交付和完成步骤。
  一个 Delivery 合并后，Task 可能仍有剩余工作。
- **跨 Issue 协调**：Codex 可显式调用 `guru-orchestrate-issue-dag` 或
  `guru-orchestrate-issue-sequence`。DAG 支持跨仓依赖及各仓环境恢复，Sequence 保持单仓串行；见 [编排说明](trellis/presets/guru-team/MIGRATION-ISSUE-ORCHESTRATION.md)。

专项需求、设计、Go-Guru 实现等方法按项目采用情况从 `guru-ai-guides` 加载，
不随 preset 安装。已归档任务的复审、恢复和手动 Git/GitHub 操作分别遵从
[当前 workflow](trellis/workflows/guru-team/workflow.md)，不以手动结果补写正式阶段结论。

## 文档导航

| 想了解 | 文档 |
| --- | --- |
| 安装资产、环境、平台选择与排障 | [Guru Team preset](trellis/presets/guru-team/README.md) |
| 团队流程、阶段与日常入口 | [workflow 指南](trellis/workflows/guru-team/README.md) / [完整流程](trellis/workflows/guru-team/workflow.md) |
| 某一步的输入、行为和出口 | [canonical Skills](trellis/skills/guru-team/) |
| 项目需求、设计、测试与架构知识 | [Requirements](docs/requirements/README.md) / [Design](docs/design/README.md) / [Test](docs/test/README.md) / [Architecture](docs/architecture/README.md) |
| 定向 CI 与诊断 | [CI 指南](docs/ci/README.md) |
| 正式版本与反馈 | [Releases](https://github.com/castbox/guru-trellis/releases) / [Issues](https://github.com/castbox/guru-trellis/issues) |

Trellis 官方参考：[首页](https://docs.trytrellis.app/index.md)、
[自定义 workflow](https://docs.trytrellis.app/advanced/custom-workflow.md)、
[spec template marketplace](https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md)。
本仓库使用这些扩展面；业务私有需求与运行状态留在业务仓库。

普通安装或升级的定向验证不代表完整多平台兼容矩阵或 Release Gate。
反馈问题时请说明版本来源、AI 工具、实际表现和预期结果，并移除密钥及敏感数据。
