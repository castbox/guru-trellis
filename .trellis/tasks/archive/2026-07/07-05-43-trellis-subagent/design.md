# #43 详细设计

## 设计目标

以 task-local artifact 建立 Trellis 层的 agent assignment 审计链：AI/human 判断谁承担哪个流程角色，脚本只记录和校验客观事实。设计必须能在 Codex / Claude / Cursor overlay 中一致表达，并能通过 preset installer 同步到 dogfood 副本。

## 架构边界

### Canonical source

- `trellis/workflows/guru-team/workflow.md`：流程合同和 artifact 语义主定义。
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`：客观 recorder / validator。
- `trellis/workflows/guru-team/scripts/bash/*.sh`：薄 wrapper。
- `trellis/presets/guru-team/overlays/`：平台入口 canonical overlay。
- `trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、`README.md`、`docs/requirements/requirement-main.md`：durable docs。

### Dogfood installed copies

- `.trellis/workflow.md`
- `.agents/skills/`
- `.codex/prompts/`
- `.codex/skills/`
- `.claude/commands/`
- `.cursor/commands/`

Dogfood 副本必须由 canonical source 同步，不能作为唯一修改源头。

Agent UI 展示名相关副本也属于 overlay 安装面：

- `.trellis/agents/implement.md`
- `.trellis/agents/check.md`
- `.codex/agents/trellis-implement.toml`
- `.codex/agents/trellis-check.toml`
- `.codex/agents/trellis-research.toml`
- `.cursor/agents/trellis-implement.md`
- `.cursor/agents/trellis-check.md`
- `.cursor/agents/trellis-research.md`
- `.claude/agents/trellis-implement.md`
- `.claude/agents/trellis-check.md`
- `.claude/agents/trellis-research.md`

## 数据合同

### Artifact 路径

```text
.trellis/tasks/<task>/agent-assignment.json
```

### 建议结构

```json
{
  "schema_version": "1.0",
  "task": ".trellis/tasks/07-05-43-trellis-subagent",
  "head": "49c8f5c...",
  "agents": [
    {
      "logical_role": "实现代理",
      "agent_id": "019f...",
      "platform_nickname": "实现代理",
      "assigned_at": "2026-07-05T08:00:00Z",
      "assigned_head": "49c8f5c...",
      "reason": "Codex dispatch_mode=sub-agent; task touches workflow and companion scripts"
    }
  ],
  "review_rounds": [
    {
      "round": 1,
      "logical_role": "问题发现审查代理",
      "agent_id": "019f...",
      "platform_nickname": "问题发现审查代理",
      "reviewed_head": "abc123...",
      "findings_count": 1,
      "reuse_policy": "问题发现代理可继续做闭环复查，但不能作为最终放行审查代理。",
      "reuse_decision": "reuse-for-closure"
    }
  ],
  "reuse_decisions": [
    {
      "from_round": 1,
      "to_round": 2,
      "logical_role": "问题闭环审查代理",
      "agent_id": "019f...",
      "decision": "reuse",
      "reason": "同一代理持有 finding 上下文，适合验证修复闭环。",
      "head": "def456..."
    }
  ]
}
```

### 字段规则

- `schema_version`：新增 artifact schema 版本，当前 `1.0`。
- `task`：repo-relative task path。
- `head`：artifact 最近一次记录时的 Git `HEAD`。
- `agents[]`：每次分配 agent 时追加，不要求覆盖旧记录。
- `logical_role`：必须是允许的中文逻辑角色之一。
- `agent_id`：可为空但字段应存在；平台未提供 id 时记录空字符串，并在 `reason` 说明。
- `platform_nickname`：可为空，只作展示，不参与 gate 判断。优先记录平台 UI 已展示的中文名称；平台只提供随机/自动昵称时记录原始值，并在 `reason` 或 review report 中说明 fallback。
- `assigned_head` / `reviewed_head` / `head`：用于判断证据对应的代码状态。
- `reuse_decision` / `reuse_decisions[]`：记录 AI/human 已做出的复用或更换判断；脚本只检查字段存在和结构。

允许的 `logical_role`：

- `实现代理`
- `阶段二检查代理`
- `问题发现审查代理`
- `问题闭环审查代理`
- `最终放行审查代理`

## Agent UI 展示名设计

技术调度标识与 UI 展示名分离：

- Codex custom agents 保持 `name = "trellis-implement" | "trellis-check" | "trellis-research"`，这是平台识别 agent 的技术标识；同时配置中文 `description`。当前 Codex 0.142.5 和官方文档要求 `nickname_candidates` 只能使用 ASCII 字符，本地 `codex doctor` 已验证中文候选会让 agent 文件被忽略，所以 Codex `nickname_candidates` 保持 ASCII，以保证 agent 可加载。
- Cursor / Claude Markdown agent 保持 frontmatter `name` 为 `trellis-implement`、`trellis-check`、`trellis-research`，用中文 `description`、中文 H1 和正文说明表达 UI 展示名。
- Trellis channel runtime `.trellis/agents/implement.md` / `.trellis/agents/check.md` 保持 `name: implement|check`，用中文 `description`、中文 H1 和正文说明表达 channel UI 展示名。

不把技术 `name` 改成中文，因为 Trellis / 平台调度、CLI spawn、overlay path 和既有 workflow 都依赖这些稳定 id。若某个平台忽略中文展示字段、或像当前 Codex 一样限制中文 nickname，`agent-assignment.json.platform_nickname` 记录实际可见值，`logical_role` 继续承担中文流程身份。

## Companion script 设计

### 新增 subcommand

建议新增：

```bash
.trellis/guru-team/scripts/bash/record-agent-assignment.sh --json \
  --logical-role "实现代理" \
  --agent-id "019f..." \
  --platform-nickname "Lovelace" \
  --reason "中文原因"

.trellis/guru-team/scripts/bash/check-agent-assignment.sh --json
```

Python 内部新增 `record-agent-assignment` / `check-agent-assignment` subcommand。

### Recorder 行为

- 解析当前 task dir。
- 读取或创建 `agent-assignment.json`。
- 追加 `agents[]` 或 `review_rounds[]` / `reuse_decisions[]`。
- 写入当前 `HEAD`、UTC 时间和 task path。
- 使用 `ensure_ascii=False`、两空格缩进。

### Validator 行为

- 校验 JSON 可读。
- 校验 `schema_version`、`task`、`head` 类型。
- 校验 `logical_role` 在允许枚举内。
- 校验 review round 是正整数，`findings_count` 是非负整数。
- 校验 `head` / `assigned_head` / `reviewed_head` 在当前 repo 可解析；若要求 current head match，则校验匹配。
- 生成 digest 摘要，供 review gate 引用。

### Review Gate 集成

`review-branch.sh` 增加可选参数：

```bash
--agent-assignment ".trellis/tasks/<task>/agent-assignment.json"
```

通过 gate 时：

- 如果传入，加载并校验 task-local `agent-assignment.json`。
- 在 `review-gate.json.verification.agent_assignment` 中记录 `path`、`sha256`、`size_bytes`、`modified_at`、`roles`、`review_rounds_count`。
- Gate evidence 仍由 AI/human 提供，脚本不判断 agent 选择是否合理。

兼容策略：

- 不让旧任务因为缺少 `agent-assignment.json` 全面失败。
- 当 workflow / overlay 要求本任务已经发生 sub-agent dispatch 或 review reuse decision 时，AI 应记录 artifact；review gate 可通过 `--agent-assignment` 固化证据。
- Publish 阶段不直接要求该 artifact，但 review gate 记录后应由 `check-review-gate` 校验 digest。

## Workflow / overlay 文案设计

### Workflow

新增或更新：

- Task System：列出 `agent-assignment.json`。
- Sub-agent Boundary：解释中文逻辑角色、`agent_id`、`platform_nickname`。
- Phase 2：main session dispatch implement/check 时记录 `实现代理` / `阶段二检查代理`。
- Phase 3.5：independent review 前后记录 `问题发现审查代理`、`问题闭环审查代理`、`最终放行审查代理`，并要求 review report 引用中文逻辑角色。
- Companion script 示例：展示 `record-agent-assignment.sh` / `check-agent-assignment.sh` / `review-branch --agent-assignment`。

### Platform overlays

所有 continue entry 需要同步：

- 继续入口在 dispatch implement/check/review agent 后，主会话记录中文逻辑角色与技术身份。
- 若平台没有可见 `agent_id` / nickname，记录为空并说明原因。
- 复用或更换 reviewer 时必须写明 `reuse_decision`。
- `review.md` 必须引用 `agent-assignment.json` 或说明没有 sub-agent assignment 的原因。

Finish entry 只需提示：finish 前 review gate 已经固化 assignment digest；finish-work 不重新决定 reviewer。

Start entry 不需要深改；可说明 handoff 只是 intake provenance，agent assignment 属于 task-local artifact。

Agent definition overlay 需要同步：

- `.codex/agents/trellis-*.toml`：中文 `description`、ASCII `nickname_candidates`，保留英文技术 `name`；中文 UI 名称由 description / workflow 文案 / assignment 记录表达。
- `.cursor/agents/trellis-*.md`、`.claude/agents/trellis-*.md`：中文 frontmatter `description`、中文 H1，保留英文技术 `name`。
- `.trellis/agents/{implement,check}.md`：中文 frontmatter `description`、中文 H1，保留 channel runtime 技术 `name`。

## Durable docs 设计

更新 `docs/requirements/requirement-main.md`：

- 在 P0 证据链或 P1 preset/platform overlay 章节增加 #43 能力说明，包括 UI 展示名中文化与技术 id 稳定边界。
- 历史覆盖矩阵增加 issue #43。
- 当前扩展边界增加：platform nickname 不参与流程判断，agent assignment task artifact 是审计证据；UI 展示名尽量中文，但平台实际返回值只作为 display-only 事实记录。

## 测试与验证设计

### 单元/静态验证

- `python3 -m json.tool trellis/index.json`
- `python3 -m json.tool trellis/workflows/guru-team/schemas/intake-handoff.schema.json`
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
- `python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- `python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`

### Trellis / workflow 验证

- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-05-43-trellis-subagent`
- `python3 ./.trellis/scripts/get_context.py --mode phase`
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 2.1`
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5`

### Overlay / dogfood 验证

- `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
- 检查 `.new` / `.bak`，若产生必须逐个处理。

### 开箱即用验证

最低应尝试 `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`。如果当前分支 marketplace source 无法直接被远端验证，应在最终说明中明确未覆盖当前分支完整 throwaway install，并列出风险。

## 风险与取舍

- 新 artifact 不应成为旧任务 publish 的硬性阻塞，否则会破坏向后兼容。采取可选记录 + workflow 要求新流程记录的方式。
- 平台 `agent_id` / nickname 能见度不同，字段允许为空，避免因平台能力差异阻塞流程。
- 最终放行审查代理的复用限制只在 artifact 中记录判断，不在本 issue 中实现更严格 gate 规则，避免超出非目标。
