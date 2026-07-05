# #43 规范 Trellis subagent 中文逻辑角色与复用记录

## 目标

在 Guru Team workflow 的 sub-agent 模式下，建立稳定、中文、可审计的 Trellis 流程身份模型。平台提供的 `agent_id` 作为技术身份，`platform_nickname` 只作为 UI 展示信息；workflow、review report、review gate、任务 artifact 和最终汇报都应以中文逻辑角色和 task-local assignment 记录为准。声明支持的 subagent UI 展示面应优先显示中文名称；平台只能返回随机/自动昵称时，记录原始值作为兼容 fallback。

## 背景与证据

- GitHub issue #43 明确指出：当前 Trellis artifact 和 review gate 主要依赖运行时描述，缺少稳定中文逻辑角色与 agent 复用/更换记录，导致多轮实现、检查、review 难以审计。
- 官方 Trellis `custom-workflow.md` 说明 workflow 行为由 `.trellis/workflow.md` 的 Markdown 定义，修改 workflow 不需要改 Python、hook 或重发 Trellis。
- 官方 Trellis `custom-agents.md` 说明 Trellis 已有 `trellis-implement`、`trellis-check`、`trellis-research`，且不同平台有不同 agent 文件格式；没有 hook 注入的平台依赖 agent 文件中的 pull-based prelude。agent `name` / channel runtime `implement` / `check` 是技术调度标识，不能为了中文 UI 展示改名。
- 官方 Trellis `custom-hooks.md` 说明 hook 可做 session/workflow-state/sub-agent context injection；hook 是注入层，不应替代 workflow 判断。
- 官方 Trellis `custom-spec-template-marketplace.md` 说明 spec marketplace 只放可复用工程约定，不能放 `.trellis/tasks/`、workspace 或 active runtime state。本任务新增的是 task-local artifact 合同，不应写进 spec template marketplace。
- OpenAI Codex subagents 文档说明 custom agent `name` 是识别该 agent 的技术标识，`nickname_candidates` 是 UI 昵称候选且当前要求 ASCII 字符；本地 `codex doctor` 已验证中文 `nickname_candidates` 会导致 Codex 忽略该 agent 文件。因此 Codex overlay 只能把中文名称放在 `description` 和 workflow / assignment 记录中，`nickname_candidates` 保持 ASCII 以保证 agent 可加载。
- 本仓库 durable docs SSOT 存在于 `docs/requirements/`；本任务会改变长期 workflow / artifact / gate 语义，需要同步更新 `docs/requirements/requirement-main.md`。
- 中台知识门禁不适用：本任务不涉及 `go-guru`、`proto-guru`、Unity3D Guru SDK、Flutter Guru SDK 或其他 middle-platform SDK/framework。

## 范围

### 必须完成

- 在 canonical workflow 中定义 task-local `agent-assignment.json` 的用途、字段、写入时机和审计规则。
- 明确中文逻辑角色与平台身份的边界：
  - `logical_role` 是 Trellis 流程身份。
  - `agent_id` 是技术身份，用于继续消息或复用。
  - `platform_nickname` 只记录 UI 展示名，不参与 gate 判断。
- 支持并文档化这些中文逻辑角色：
  - `实现代理`
  - `阶段二检查代理`
  - `问题发现审查代理`
  - `问题闭环审查代理`
  - `最终放行审查代理`
- 新增或规范 `agent-assignment.json` task-local artifact，记录实现、检查、review agent 分配，以及复用/更换原因、HEAD、review round。
- 让 Branch Review Gate 或 review artifact 可以引用中文逻辑角色，不只依赖随机英文 nickname 或笼统 reviewer 字符串。
- 让声明支持的平台 agent UI 展示面优先使用中文名称：
  - Codex custom agents 保持 `name = "trellis-..."` 和 ASCII `nickname_candidates`，提供中文 `description`，避免 Codex 因中文 nickname 候选忽略 agent 文件。
  - Cursor / Claude agent Markdown 保持 frontmatter `name` 技术标识，使用中文 `description` 和中文标题。
  - Trellis channel runtime `.trellis/agents/{implement,check}.md` 保持 `name: implement|check`，使用中文 `description`、中文标题和中文 UI 展示名说明。
- 提供 companion script recorder / validator 能力，只校验客观字段、JSON 结构、HEAD 匹配和角色值；不得让脚本决定应该使用哪个 subagent。
- 同步 canonical workflow、dogfood `.trellis/workflow.md`、platform overlays、README、preset README、workflow README、requirements docs。
- 修改 overlay 后重新 apply 到本仓库 dogfood 副本，并运行 drift check。

### 非目标

- 不修改 Codex 平台生成 UUID 或随机 nickname 的机制。
- 不修改 Trellis 官方上游源码、全局 npm 包或 `node_modules`。
- 不把 subagent 调度决策写成 shell / Python 智能 planner。
- 不在本 issue 中收紧 Branch Review Gate 对 findings 的最终放行规则。
- 不把 active task 记录放入 spec template marketplace。
- 不修改平台运行时随机 nickname 生成机制；平台如果忽略 overlay 提供的中文展示字段，本任务只在 artifact 中记录实际可见值并说明兼容风险。

## 需求

### R1. 中文逻辑角色合同

Workflow 和文档必须声明：Trellis 判断流程身份时只依赖中文逻辑角色和 task artifact；平台 nickname 不参与 gate 判断。

验收：

- `trellis/workflows/guru-team/workflow.md` 和 `.trellis/workflow.md` 包含角色清单和三类身份边界。
- README / workflow README / preset README 说明平台 nickname 仅作展示。

### R2. `agent-assignment.json` task-local artifact

任务目录下新增 `agent-assignment.json` 合同，支持记录：

- `agents[]`：按分配事件记录 `logical_role`、`agent_id`、`platform_nickname`、`assigned_at`、`reason`、`assigned_head`。
- `review_rounds[]`：按 review round 记录 `round`、`logical_role`、`agent_id`、`platform_nickname`、`reviewed_head`、`findings_count`、`reuse_policy`、`reuse_decision`。
- `reuse_decisions[]` 或等价字段：记录复用/更换目标、原因、HEAD 和 round。

验收：

- Workflow / README 给出最小 JSON 示例。
- Companion script 能记录或校验该 artifact。
- 旧任务缺少该 artifact 时，非 publish/check 路径保持兼容；新流程在实际分配 agent 后应写入。

### R3. Review Gate 引用 assignment 证据

Branch Review Gate 的 review artifact / recorder artifact 应能引用中文逻辑角色和 `agent-assignment.json` 摘要。

验收：

- `review-branch.sh` 或 Python helper 能在 gate artifact 中记录 assignment 摘要或路径/hash。
- `review.md` 写作要求包含中文逻辑角色和 agent 复用/更换判断。
- `check-review-gate.sh` 能客观校验已记录 assignment artifact 的存在、digest 和 HEAD 语义。

### R4. AI 判断与脚本边界

脚本只能是 recorder / validator。复用哪个 subagent、是否更换 reviewer、最终 release review 是否充分，必须由 AI/human 按 workflow 判断并写入 artifact。

验收：

- Workflow、overlay、companion script docs 明确脚本不得替 AI 决定 subagent 复用。
- Python helper 中新增逻辑只做字段存在性、枚举值、HEAD、digest、JSON 结构等客观校验。

### R5. 多平台入口与 UI 展示名同步

声明支持的 Codex / Claude / Cursor / channel runtime 入口文案要一致；shared `.agents/skills` 和 `.codex` / `.claude` / `.cursor` / `.trellis/agents` overlay 不能保留旧流程说法。平台 UI 能展示 agent 名称或说明时，应显示中文 subagent 名称，而不是只暴露英文技术 id 或随机英文 nickname。

验收：

- `trellis/presets/guru-team/overlays/` 中 continue / finish / start 相关入口同步说明 assignment 记录。
- `trellis/presets/guru-team/overlays/` 中 Codex / Cursor / Claude / `.trellis/agents` agent 文件保留技术 `name`。Cursor / Claude / `.trellis/agents` 使用中文 `description` 和标题；Codex 使用中文 `description` 和 ASCII `nickname_candidates`，并在文档中标明当前 Codex 对中文 nickname 的平台限制。
- 重新 apply preset 后，本仓库 `.agents/skills/`、`.trellis/agents/`、`.codex/agents/`、`.codex/prompts/`、`.codex/skills/`、`.claude/agents/`、`.claude/commands/`、`.cursor/agents/`、`.cursor/commands/` dogfood 副本无漂移。

### R6. Docs SSOT 与开箱验证说明

长期能力说明必须进入 durable docs；最终报告要说明开箱即用 / upgrade-update 门禁覆盖情况。

验收：

- `docs/requirements/requirement-main.md` 增加 #43 能力条目或更新历史矩阵。
- 运行必要 validation：JSON、bash syntax、Python compile/tests、task validate、phase context read、dogfood drift。
- 若无法跑完整 throwaway install 或 upgrade/update 验证，最终说明必须明确未覆盖项和风险。

## 验收标准

- [ ] Workflow / skill / prompt 文案明确中文逻辑角色和平台 nickname 的区别。
- [ ] Task-local artifact 能记录实现、检查、review agent 分配与复用/更换原因。
- [ ] Branch Review Gate 或 review artifact 能引用中文逻辑角色，而不是只依赖随机英文 nickname。
- [ ] 文档明确脚本不得替 AI 决定该使用哪个 subagent，只能 validator / recorder。
- [ ] 覆盖 Codex / Claude / Cursor / channel runtime 等声明支持入口和 agent UI 展示名同步。
- [ ] Dogfood installed copies 与 canonical overlay 无漂移。
- [ ] Companion script 变更有测试或代表性验证。
- [ ] Durable docs 已更新，或明确说明为何不需要更新；本任务判断为需要更新。

## 开放问题

无阻塞开放问题。Issue 已给出角色清单、artifact 形态、脚本边界和非目标；实现时若发现字段需要微调，应保持向后兼容并记录在 `design.md`。
