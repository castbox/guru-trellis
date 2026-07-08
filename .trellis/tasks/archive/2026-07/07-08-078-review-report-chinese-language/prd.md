# #78 Branch Review raw reports / review.md 必须继承 #57 中文 artifact 规则

## Goal

让 Branch Review 每轮 raw Markdown review report（`{TASK_DIR}/reviews/*.md`）
和最终 rollup（`{TASK_DIR}/review.md`）明确继承 #57 的中文 artifact
规则，并在生成链路与校验链路中补防复发机制。

本任务关闭 issue [#78](https://github.com/castbox/guru-trellis/issues/78)。

## 背景与已确认事实

- #57 已确立业务项目中的 `.trellis/spec/**`、`.trellis/tasks/**`、
  durable `docs/**` 和 workflow 写入的 human-readable artifact 字段默认使用中文；
  命令、路径、JSON 字段、HEAD、GitHub keyword、代码符号、外部 API 名称等
  literal token 可保留英文。
- #70 / PR #77 增加了 Branch Review raw report retention：每轮
  `reviews/*.md` raw report、最终 `review.md` rollup、`agent-assignment.json`
  review round digest 和 `review-gate.json.verification_evidence.review_reports[]`
  digest。
- #77 已修补当时归档产物，但没有修复后续生成链路。本任务必须修
  canonical workflow / overlays / agent prompt / validator or tests，不能只修历史 artifact。
- 官方 Trellis 文档确认 workflow 行为由 `.trellis/workflow.md` 这类
  Markdown 合同承载，运行时读取即可生效；spec template marketplace 只承载
  可复用规范、测试规则和 review checklist，不应存 active task / runtime state。
- 当前仓库已有 durable docs SSOT：`docs/requirements/README.md`、
  `docs/requirements/requirement-main.md`、`docs/requirements/guru-team-trellis-flow.md`
  以及 `.trellis/spec/**`。本任务若改变长期 workflow 规则，必须同步这些 durable docs。
- 当前仓库是 `guru-trellis` public extension repo。公开 README/source comments/script help
  可保持英文或双语，但业务项目安装后的 `.trellis/tasks/**` review artifacts
  需要中文为主。

## 需求

### R1. 中文 artifact 合同

`reviews/*.md` raw reports 和最终 `review.md` rollup 必须被明确列为
human-readable task artifacts。除 literal token 例外外，以下内容应中文为主：

- 标题和小节名；
- 字段名 / 标签；
- 摘要、证据、发现、观察项、后续候选；
- 部署 / 安全 / Docs SSOT 判断；
- 最终结论。

建议中文 rollup 小节名包括但不限于：`审查轮次`、`问题生命周期`、
`最终审查`、`证据`、`观察项`、`后续候选`、`结论`。

### R2. 生成链路防复发

Branch Review sub-agent prompt / handoff wording 必须要求 raw report 使用中文标题、
中文字段名和中文审查叙述；主会话生成最终 `review.md` rollup 时必须要求中文结构。

覆盖范围至少包括：

- canonical `trellis/workflows/guru-team/workflow.md`；
- dogfood `.trellis/workflow.md`；
- preset overlays 下的 continue / finish-work / check agent 入口；
- dogfood installed copies：`.agents/skills/`、`.codex/prompts/`、`.codex/skills/`、
  `.codex/agents/`、`.claude/commands/`、`.claude/agents/`、`.cursor/commands/`、
  `.cursor/agents/`、`.trellis/agents/`；
- `.trellis/spec/**` 与 `docs/requirements/**` durable docs。

### R3. 客观模板痕迹校验

补充 validator 或 test，至少能防止明显英文模板标题进入 `review.md` /
`reviews/*.md`。检查对象是客观字符串痕迹，不做语义充分性判断。

必须拦截的示例包括：

- `Review Rounds`
- `Findings Lifecycle`
- `Evidence Handoff`
- `Deployment / safety impact`
- `Follow-up Candidates`

可额外拦截现有 agent 模板里的明显英文小节，例如 `Files Checked`、
`Issues Found and Fixed`、`Issues Not Fixed`、`Verification Results`、`Summary`。

### R4. 不改变 #70 数据模型

保持 raw report retention / digest / archive migration 数据模型不变，不新增由脚本
判断审查语义充分性的职责；脚本只能做 artifact path、digest、链接、role
以及明显模板痕迹这类机器可判定检查。

### R5. 安装副本和 canonical 无漂移

修改 preset overlay 后必须重新应用到 dogfood 仓库，并通过 dogfood overlay drift check。
不得只修改 `.trellis/workflow.md`、`.agents/skills/**` 或 `.codex/**` 这类安装副本。

## 非目标

- 不 reopen #57；本任务只承接 #57 在 Branch Review report 新 artifact 上的遗漏。
- 不改变 #70 的 raw report retention / digest / archive migration 数据模型。
- 不把脚本变成语言语义 reviewer。
- 不要求 literal token 翻译成中文。
- 不修改 Trellis upstream npm package、`node_modules` 或全局安装目录。

## 验收标准

- [ ] workflow 明确 `reviews/*.md` raw reports 和最终 `review.md` rollup 属于
      human-readable task artifacts，默认中文。
- [ ] Branch Review sub-agent prompt 明确要求 raw report 的标题、字段名、发现、
      观察、后续候选、部署 / 安全判断、最终结论中文为主。
- [ ] main session 生成最终 `review.md` rollup 时明确使用中文标题和中文字段名，
      至少给出 `审查轮次`、`问题生命周期`、`最终审查`、`证据`、`观察项`、
      `后续候选`、`结论` 等推荐结构。
- [ ] literal token 例外写清楚。
- [ ] Codex / Claude / Cursor / `.agents` overlay 与 canonical workflow 同步。
- [ ] dogfood installed copies 与 preset overlays 无漂移。
- [ ] 补充测试、validator 或 checklist，至少防止 `Review Rounds`、
      `Findings Lifecycle`、`Evidence Handoff`、`Deployment / safety impact`、
      `Follow-up Candidates` 等明显英文模板标题进入 `review.md` / `reviews/*.md`。
- [ ] durable docs / spec 记录本规则，避免后续只修当前 task artifact。

## Docs SSOT 与知识门禁

- Durable docs SSOT：需要更新 `docs/requirements/requirement-main.md` 和
  `docs/requirements/guru-team-trellis-flow.md`；如 README / workflow README /
  preset README 中有 Branch Review report 语言说明，也应同步。
- Middle-platform Knowledge Gate：不适用。本任务不涉及 Guru Team middle-platform
  SDK / framework 使用。
