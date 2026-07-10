# #96 移除 handoff 并重建任务运行边界

## 目标

完整移除 Guru Team 原 `.trellis/guru-team/handoff.json` 概念，把任务启动阶段的数据拆分为 task-local、git tracked、可移植的“任务启动上下文”，以及 gitignored、可丢弃的“本机运行态”。普通 task 命令不得再修改固定 tracked 运行文件或仓库共享配置，从根因消除并行 task 对同一路径的争用和本机绝对路径泄露。

## 证据

- GitHub issue：`https://github.com/castbox/guru-trellis/issues/96`
- umbrella issue：`https://github.com/castbox/guru-trellis/issues/53`
- 后续拆分：`#97`、`#98`、`#99`、`#100`
- Trellis 官方 workflow 扩展说明：`https://docs.trytrellis.app/advanced/custom-workflow.md`
- Trellis 官方 spec template marketplace 说明：`https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md`
- 仓库规范：`.trellis/spec/workflow/**`、`.trellis/spec/preset/**`、`.trellis/spec/docs/**`、`.trellis/spec/guides/**`

## 已确认事实

- canonical workflow 位于 `trellis/workflows/guru-team/workflow.md`，dogfood active copy 位于 `.trellis/workflow.md`。
- canonical companion implementation 位于 `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`，preset installer 会把 canonical assets 和 overlays 同步到 dogfood 安装副本。
- 当前 `prepare-task --create-worktree/--create-task` 把 source issue、task facts、绝对 workspace 路径、worktree 列表、dirty/fetch 诊断和 developer identity 信息混写到固定 tracked 路径 `.trellis/guru-team/handoff.json`。
- 当前 workspace boundary 依赖 handoff 中 committed absolute `workspace_path` 推导 expected workspace。
- 当前 config、extension manifest、schema、workflow、skills、prompts、README 和 requirements docs 都把 handoff 当作公共 artifact contract。
- 本 issue 明确不要求 legacy fallback 或旧任务迁移；旧 handoff 文件、读取路径和命名应直接删除。

## 需求

### R1 任务启动上下文

创建 task-local、git tracked、可移植的 `.trellis/tasks/<task-slug>/task-start-context.json`，并提供独立 schema。字段只能包含：

- `schema_version`
- `source_issue` / `source_repo`
- `task_slug` / `task_title`
- repo-relative `task_artifact_dir`
- `branch_name`
- `base_branch`
- `base_ref` / `base_head_sha` / `remote_head_sha`
- portable `workspace_slug` / `task_workspace_id`
- `assignee` / `actor` metadata
- issue scope ledger seed：`close_issues`、`related_issues`、`followup_issues`
- duplicate decision、naming quality、intake confirmation 的可移植摘要

任务启动上下文不得包含绝对路径、`.trellis/.runtime/**` 路径、完整 `preflight`、dirty/fetch 过程、`existing_worktrees`、developer identity 路径或本机命令路径。`task_artifact_dir` 必须是 repo-relative task 目录。

### R2 本机运行态

可重算事实每次命令运行时重新读取，不持久化：当前 checkout、branch、dirty status、worktree existence、base freshness、fetch/fast-forward 结果。

必须跨 Guru Team 命令复用的本机映射只能写入：

- `.trellis/.runtime/guru-team/workspaces/<workspace-slug>.json`
- `.trellis/.runtime/guru-team/tasks/<task-slug>.json`

runtime cache 使用 portable slug 做 key，可包含 workspace slug 到绝对 worktree path、task slug 到 runtime workspace、上一次 executor context、lock/pid/temp cache。cache 必须 gitignored、可删除、可通过当前 checkout、task-start-context、`git worktree list` 或显式参数重建；不得新增 runtime index 或 developer 维度目录。

### R3 Workspace Boundary

workspace boundary 不得读取 committed absolute `workspace_path`。每次运行必须基于当前 checkout、repo-relative `task_artifact_dir`、task-start-context、worktree mapping、`git worktree list` 和 local-only cache 重算并校验当前 repo root、branch、dirty status、base freshness 与 worktree existence。

### R4 仓库共享配置只读边界

GitHub repo fallback、base branch fallback、workspace mode、artifact/schema 名称、命名规则、旧 handoff 删除策略和 runtime cache 合同继续由 canonical config/workflow/schema/preset 管理。普通 task create/plan/execute/review/finish/publish 只能读取这些 tracked 共享配置，不得静默修改；只有明确以 workflow/preset/config 为 scope 的 task 才可在正常 review 范围内修改。

### R5 普通 Task 写入 Allowlist

普通 Guru Team task 只能写当前 task active/archive 目录、当前 issue scope 明确要求的产品资产、`.trellis/.runtime/guru-team/**` 和临时目录。必须通过测试证明两个同一 developer、同一机器、不同 task slug 的并行任务不会共同修改固定 tracked Trellis metadata 路径。

### R6 移除 Handoff 公共 API

删除或重命名 `intake-handoff.schema.json`、`handoff_path` config、extension manifest artifact contract、helper API、workflow/skill/prompt/config/public docs 中的 handoff 概念。代码、schema、workflow、skill、prompt、config 和 public API 不得继续使用 handoff 命名；测试和历史说明只能用该字符串断言旧文件不存在或解释删除原因。Agent 之间通用自然语言“工作交接”不属于本 issue 的 Guru Team artifact/public API，但应避免与被移除 artifact 混淆。

### R7 Canonical 与 Dogfood 同步

先修改 `trellis/workflows/guru-team/`、`trellis/presets/guru-team/overlays/`、`trellis/guru-team-extension.json`、README、requirements docs 与适用 spec，再运行 preset apply 同步 `.trellis/guru-team/`、`.trellis/workflow.md` 和所有受支持平台入口。必须处理 `.new` / `.bak` 并通过 dogfood drift 检查。

### R8 开箱与抗升级验证

必须在 throwaway repo 验证 marketplace workflow 和 preset 安装后：普通 task 创建不写 `.trellis/guru-team/handoff.json`、不写 `.trellis/workspace/**`、不依赖 committed absolute workspace path；task-start-context 可移植，runtime cache 被 ignore。必须执行 `trellis update`；若当前 Trellis CLI 使用不同的官方 update 命令，先用 `trellis --help` 和官方文档确认命令后执行，并记录命令证据。验证必须证明 canonical workflow/preset/overlay 语义可恢复且不会被静默覆盖。

## 验收标准

- [ ] `.trellis/tasks/<task-slug>/task-start-context.json` 与 schema 实现固定字段白名单。
- [ ] committed task context 不含绝对路径、runtime path、完整 preflight、dirty/fetch/worktree 列表或 developer identity 路径。
- [ ] 本机复用状态只落 `.trellis/.runtime/guru-team/workspaces|tasks/*.json`，路径已 gitignore，cache 缺失可重建。
- [ ] workspace boundary 每次运行重算当前 checkout、branch、dirty、base freshness、worktree existence 和 fetch/fast-forward 结果。
- [ ] 普通 task create/execute/finish/publish 不修改共享 config、workflow、preset、schema、platform overlays、`.trellis/.developer` 或 `.trellis/workspace/**`。
- [ ] 两个并行 task fixture 的 tracked Trellis metadata diff 只包含各自 task 目录。
- [ ] 代码、schema、config、manifest、workflow、skills、prompts 和 public docs 删除 handoff artifact/public API。
- [ ] canonical 与 dogfood copies 同步，无未处理 `.new` / `.bak`，drift check 通过。
- [ ] throwaway install 和 upgrade/update 验证通过；未执行项必须在 PR body 和最终报告中列出风险。
- [ ] `#96` 验收证据完整后可关闭；`#53` 仅回填结论，不关闭。

## 不纳入范围

- 不处理 workspace journal / `add_session.py` / archive 的 finish-work 冲突；由 `#97` 处理。
- 不回填 archived task 的 `finish-summary.json`；由 `#100` 处理。
- 不实现历史上下文分级发现；由 `#98` 处理。
- 不彻底取消 Guru Team 任务创建对 `.trellis/.developer` 的剩余前置依赖；由 `#99` 处理。
- 不修改 Trellis 官方 task lifecycle、workspace journal、`trellis init/update` core、上游 npm 包、全局安装或 `node_modules`。
- 不改变 metadata-only dirty-state 的整体策略。

## 风险

- `prepare-task` 当前在创建 task 之前就需要 workspace/task 映射，拆分写入时序若处理不当会造成 task-start-context 缺字段或 runtime cache 先于 task 创建失配。
- finish/check/review/publish 多处通过 `load_handoff()` 获取 base/workspace 信息，必须逐调用点改为 task context + runtime recomputation，不能只替换文件名。
- `.trellis/.runtime/` 的官方 ignore 语义和 installer 行为必须在 throwaway repo 实证；不能依赖 dogfood 历史状态。
- 大量平台 overlay 文案存在重复，必须修改 canonical overlay 后统一 apply，避免手工同步遗漏。
