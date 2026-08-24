# Guru Trellis

Guru Team GitHub operations require an installed and authenticated GitHub CLI.
All platform reads and mutations are explicitly repository-bound `gh` or
`gh api` operations; GitHub App, MCP, connector, and browser UI fallback are
not supported. Git transport remains owned by `git`.

Guru Trellis 是 Guru Team 面向业务研发仓库提供的 Trellis 团队扩展。

它建立在官方 Trellis 之上，为团队补充一套开箱即用、AI-first 的研发协作方式，让不同 AI 工具能够按照一致的流程理解需求、规划实现、检查变更、审查分支并完成交付。

如果你只是想在业务仓库中使用 Guru Team Trellis，不需要理解本仓库的内部实现。可以把本仓库地址交给业务仓库中的 AI，让它完成安装或升级，也可以使用下方固定版本命令：

[https://github.com/castbox/guru-trellis](https://github.com/castbox/guru-trellis)

## 本次发布固定身份

| 组件 | 固定版本 |
| --- | --- |
| Guru Trellis repo tag | `v0.6.15-guru.1` |
| Guru Team extension revision | `0.6.5-guru.37` |
| 官方 `@mindfoldhq/trellis` CLI | `0.6.15` |

repo tag 与 extension revision 是两个独立版本轴。本次发布的 workflow 与 preset
固定使用同一个目标 annotated tag `v0.6.15-guru.1`。该 tag object、peeled commit、
GitHub Release、tag-pinned install 与 post-publish smoke 尚未创建或验证；#304 必须在
修复合并后重新冻结 exact candidate，并从头执行 Release gates。

新仓库的非交互安装入口：

```bash
npm install --global @mindfoldhq/trellis@0.6.15
trellis init -y --claude --codex --cursor \
  --workflow guru-team \
  --workflow-source gh:castbox/guru-trellis/trellis#v0.6.15-guru.1
guru_trellis_source="$(mktemp -d)"
git clone --depth 1 --branch v0.6.15-guru.1 \
  https://github.com/castbox/guru-trellis.git "$guru_trellis_source"
"$guru_trellis_source/trellis/presets/guru-team/scripts/bash/apply.sh" \
  --repo . --all-platforms
```

已有仓库先安装固定 CLI 并 preview official update：

```bash
npm install --global @mindfoldhq/trellis@0.6.15
trellis update --dry-run
```

dry-run 输出包含 `MIGRATION REQUIRED` 时，只执行：

```bash
trellis update --migrate --skip-all
```

否则只执行：

```bash
trellis update --skip-all
```

完成唯一一次 preserve-mode update 后，再切换 workflow 并 reapply 同 tag preset：

```bash
trellis workflow \
  --marketplace gh:castbox/guru-trellis/trellis#v0.6.15-guru.1 \
  --template guru-team --create-new
trellis workflow \
  --marketplace gh:castbox/guru-trellis/trellis#v0.6.15-guru.1 \
  --template guru-team
guru_trellis_source="$(mktemp -d)"
git clone --depth 1 --branch v0.6.15-guru.1 \
  https://github.com/castbox/guru-trellis.git "$guru_trellis_source"
"$guru_trellis_source/trellis/presets/guru-team/scripts/bash/apply.sh" \
  --repo . --all-platforms
```

升级完成后必须处理全部 `.new` / `.bak`，再验证 source/installed/platform equality、
managed inventory、受管 Python runtime、dogfood drift 和递归零 sidecar，才能声明升级成功。

## 它解决什么问题

AI 编程工具很擅长完成局部开发工作，但团队协作还需要稳定的共同约定：

- 从真实需求和 Issue 出发，而不是直接开始改代码；
- 在实现前澄清范围、依赖、风险和验收标准；
- 让规划、实现、检查和审查各自拥有清晰职责；
- 在提交、推送、创建 PR、合并和关闭 Issue 前核对真实状态；
- 让 Codex、Claude Code、Cursor 等工具看到一致的团队规则；
- 升级工具时保留业务仓库已有的有效定制，不静默覆盖本地内容。

Guru Trellis 把这些团队能力整理成可复用的 workflow、preset 和 Skills，并让 AI 在实际开发过程中自动使用它们。

## 与官方 Trellis 的关系

Guru Trellis 不是 Trellis 的分叉版本，也不替代官方 Trellis。

官方 Trellis 负责基础能力，包括项目规范、任务上下文、工作流运行方式以及各类 AI 工具的基础接入。Guru Trellis 使用 Trellis 提供的正式扩展方式，在其上增加 Guru Team 的团队流程和交付约定。

两者的分工可以简单理解为：

- **Trellis** 提供通用研发框架；
- **Guru Trellis** 提供 Guru Team 的团队工作方式；
- **业务仓库** 保存自己的产品需求、工程规范和项目事实。

官方 Trellis 的升级继续由 Trellis 管理，Guru Team 的能力由本仓库发布和维护。业务仓库不需要修改 Trellis 上游源码，也不应把两套完整研发流程叠加在一起。

## Guru Team preset 增强了什么

### 完整的研发闭环

覆盖从需求进入到最终交付的主要阶段，包括需求澄清、规划审核、实现检查、分支审查、发布准备和任务收口。

Phase 0 的六个 mandatory Skills 通过五阶段 closed transition 直接衔接：每个 producer 的真实
public output 只交给唯一 consumer，当前 Skill 的 semantic owner result 保持 call-local，正常
pre-task 不需要在仓库保存 owner 或 prerequisite 文件。Base sync 只有一个 public authoritative
入口；兼容 `prepare-task` 不是正常 workflow step。

### AI-first 判断

流程中的判断由 AI 基于当前需求、实现和验证结果完成，而不是模拟人工审批表、签字链或书面交接流程。

用户只需要在存在真实选择、范围变化或外部副作用时参与确认。

### 正常场景资格

公共 closed-loop Skill `guru-qualify-normal-scenario` 是新场景资格的唯一语义
Owner。它覆盖 task-free 写前/演化、需求、变更请求、规划、实现发现、base impact、
Phase 2、Branch Review 和 Publication 共十个 mandatory profiles；Guru caller 只把
worker 的当前观察投影为 candidate refs 与 live locators。每次 worker dispatch 只授权
approved-plan work；规划外候选资格完成前不 edit、不补负向测试、不 self-fix、不赋
severity，也不形成 finding、实现或发布 blocker。官方 `trellis-*` agent bytes 保持
upstream-owned，不由 Guru preset 修改。

Skill 只返回 `classified`、`scope_confirmation_required`、
`mechanism_revision_required`、`blocked` 四个 typed exits，并由 workflow 交给唯一
consumer。资格 decision/result 只存在当前 invocation 的 memory/stdout，不生成 tracked
或 ignored qualification report/checkpoint、共享 candidate ledger、handoff 或跨进程
result locator。Phase 2、Branch Review、Publication 只在各自现有 owner-private gate 中
直接记录本阶段 consumer 必需的最终 classification/witness。

Production eval 资产通过 clean install 后的真实 public entry 覆盖全部十 profiles，将
#113 F-001 与 #236 攻击式 scanner 变体同 paired legitimate cases 一起验证。当前
deterministic release gate 验证 corpus、runner、真实 wrapper、sandbox 与 no-model/fake
production path，但不执行 live GPT-5.6 Sol matrix。只有另行完成且绑定 exact
model/prompt/package/matrix 的 live run 才能形成模型行为证据；没有该证据时 Issue、PR、
README 与 release text 均不得声称 pressure matrix 或模型稳定性已经通过，本文也不承诺
未来永不复发。

本发布未取得 live GPT-5.6 Sol production semantic evidence；deterministic/no-model/
fake-production 结果不能证明 pressure matrix、模型稳定性或未来模型行为。

### 智能选择 task-free 或标准 Intake

尚未进入活动 task 路径的文件修改请求都会先由 semantic
`guru-select-workflow-mode` 选择模式；Issue 是否存在、当前 branch、文件数量、路径和关键词
都不能独立决定 mode。最简显式表达是 `这次走 task-free`，此时不再询问 mode。没有明确表达时，
边界清楚、局部、可逆且低风险的修改自动走 `task_free`；大概率适合但证据不足时只问
一次；运行时影响明显或风险较高，或涉及跨层合同、public API、schema、CI、安装升级、
发布部署、权限、安全或数据时自动走 `standard_intake`。

Selector 的最小 `task_free` DTO 通过 target-owned authoring seed 调用 semantic
`guru-execute-task-free-change`。该 Skill 在写入前只读检查本地 branch/worktree、活动 task
scope、dirty/untracked 与目标文件重叠；默认或非默认 branch 本身都不阻塞，也不查询远端
branch protection。它独占限定编辑、targeted checks 和写后 scope/risk 复核；`completed`
必须同时有写前 suitability、实际 edited paths、通过的 targeted check 和写后复核，并向
completion consumer 报告实际修改路径、精简检查结果和未验证边界。自动选择的 task-free
在真实 partial edit 后发现风险扩大时立即停止剩余写入并重新判断 mode；显式 task-free 同样
停止剩余写入，再由用户选择缩小范围或进入标准 Intake。

Task-free 只授权限定编辑、保留无关改动和 targeted checks；Issue/task/worktree/branch
创建以及 commit、push、PR、merge、tag、release、安装、清理和关闭 Issue 都是独立的后续
副作用，不由 mode selection 自动授权。

`guru-execute-task-free-change` 提供 `selected_route` / `interaction_resume` 两种 inputs，
稳定 exits 为 `completed|resume_active_task|scope_change|location_required|reselect_mode|explicit_choice_required|blocked`；
完整 preset 安装命令 `record-task-free-change`、`check-task-free-change` 与
`invoke-guru-execute-task-free-change`。单独复制 Skill 目录不可运行。

### 更可靠的变更边界

在创建任务、修改仓库、提交代码、推送分支、创建 PR 或完成发布前，AI 会先核对目标、影响范围和当前状态，降低误改仓库、误用旧上下文或错误关闭 Issue 的风险。

### 规划、检查与审查能力

Guru Team preset 提供面向规划、实现检查、任务提交、分支审查、发布审核和最终收口的协作能力，使每个阶段都能读取前序结果，同时保持职责清晰。

发布审核由 Publication 在同一个语义循环中生成并审查准确的中文 PR 标题与正文，随后以包含任务、分支审查提交和标题正文的五字段 4.0 结果直接交给 Finalizer，不再创建 task-local PR body 或索引交接文件。Finalizer 将该结果与实时仓库事实绑定为 closeout plan 3.0，并在草稿 PR 建立后一次生成 finish summary 2；历史归档中的 finish summary 1 仍可只读检索。

### 多平台一致体验

团队可以在 Codex、Claude Code、Cursor 等不同 AI 工具中使用同一套 Guru Team 语义。平台入口可以不同，但工作目标、判断原则和交付标准保持一致。

### 面向业务项目的文档习惯

业务需求、设计、检查结果和 PR 说明默认以团队成员易于阅读的方式呈现。对于中文团队，面向人的内容优先使用中文，代码符号、路径和专有名词保留其原始形式。

### 安全的安装与升级

安装和升级时，AI 会区分官方 Trellis、Guru Team 和业务仓库各自拥有的内容。已知版本可以平滑迁移，无法确认来源的本地修改会被保留并交给用户判断，而不是被静默删除。

Phase 0 六包、transition schemas、invocation envelopes、package runtime、minimal shared kernel 和 manifest 作为一个
版本单元安装。Clean install、existing-project update/reapply、dogfood 与平台副本验证必须同时
通过，任何 mixed graph 或未处理的 `.new` / `.bak` 都会阻止激活。

扩展安装验证不属于业务 task 或业务 closeout。业务仓库即使已经安装完整 preset、
manifest 和 Skill package，也不会调用或路由到 `guru-verify-extension-installation`。
该 Skill 只允许从 clean `castbox/guru-trellis` source checkout 显式发起 standalone
验证；runtime 会在 clone、临时目录、安装或 artifact 写入前核对 canonical assets、
origin、requested ref、resolved commit、HEAD 和 clean tree。验证目标由 source 流程创建
clean throwaway repo，不绑定真实业务 task、branch、Finalizer plan 或 publication HEAD。
任何携带 credential 的 locator 都会在外部动作和证据写入前被拒绝。

源仓的完整 upgrade/update 验收使用隔离环境并严格按顺序执行：clean initial
workflow/preset install；在 disposable npm prefix/container 中运行
`trellis upgrade --tag latest` 并核验前后 CLI version；在 throwaway project 运行
`trellis update --dry-run`，只在输出明确包含 `MIGRATION REQUIRED` 时运行
`trellis update --migrate --skip-all`，否则运行 `trellis update --skip-all`；
`--skip-all` 保留项目已有修改并以非交互方式继续。随后完成 marketplace
`--create-new` preview、active switch 与 canonical preset reapply。最后验证 package、
workflow、十 profiles、平台投影、ownership、dogfood drift 与递归零 `.new`/`.bak`。
该门禁不修改开发机 global npm，也不升级真实业务仓。

## 适合哪些仓库

Guru Trellis 适合：

- 已经使用 Trellis，希望采用 Guru Team 工作方式的业务仓库；
- 希望为多个 AI 编程工具提供统一研发流程的团队；
- 希望把 Issue、规划、代码检查、PR 和发布收敛为一个完整闭环的项目；
- 新项目初始化，以及需要从旧 Guru Team preset 升级的存量项目。

如果仓库已经使用另一套完整的研发流程，应先让 AI 评估两者的关系并给出迁移方案。不要直接叠加安装，否则不同流程可能互相干扰。

## 正确的使用方式

### 安装到新仓库

在目标业务仓库中打开 AI 会话，把本仓库地址发给 AI，并说明需要安装 Guru Team Trellis。

AI 应当先了解目标仓库和实际使用的开发工具，再选择当前正式发布版本完成安装和验证。读者不需要从 README 中复制安装命令。

### 升级已有仓库

同样把本仓库地址交给目标仓库中的 AI，并说明需要升级 Guru Team Trellis。

AI 应先识别现有 Trellis 版本、本地定制、历史 Guru Team 安装以及可能存在的其它研发流程，再展示迁移影响。无法确认来源的改动必须保留，不能为了升级而直接覆盖。

### 日常开发

安装完成后，继续用自然语言向 AI 描述需求即可。

AI 会读取当前仓库中的 Guru Team workflow 和相关 Skills，并根据任务状态进入合适阶段。通常不需要用户记忆命令、阶段编号或内部产物名称。

## 使用原则

- 一个业务仓库只保留一套主研发流程；
- 默认使用本仓库最新的正式发布版本，而不是开发中的临时版本；
- 安装或升级前先检查目标仓库，不能套用其它项目的结论；
- 不静默覆盖业务仓库已有的未知修改；
- 只有在真实选择或副作用发生前才打断用户；
- 最终结论以当前需求、仓库内容和实际验证结果为准。

## 本仓库包含什么

本仓库集中维护：

- Guru Team 的团队 workflow；
- 可安装到业务仓库的 Guru Team preset；
- 规划、检查、审查和收口等公共 Skills；
- Codex、Claude Code、Cursor 等平台的接入内容；
- 安装、升级、兼容性和发布质量保障。

这些内容共同组成一个版本化的团队扩展。业务仓库通过正式发布版本使用它们，不需要复制或维护本仓库的内部实现。

## 发布与反馈

面向业务仓库的安装和升级应使用本仓库的正式发布版本。

如果发现安装、升级或日常使用问题，请在本仓库提交 Issue，并附上目标仓库的可公开环境信息、使用的 AI 工具、当前表现和预期结果。不要提交密钥、客户数据或其它敏感信息。
