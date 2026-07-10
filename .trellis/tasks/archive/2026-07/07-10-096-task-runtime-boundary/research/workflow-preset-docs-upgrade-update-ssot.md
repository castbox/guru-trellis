# Research: Issue #96 workflow/preset/docs/upgrade-update SSOT

- Query: 调研 Issue #96 移除 Guru Team `handoff` 概念后，workflow、preset、overlay、dogfood 副本、README、requirements 与 upgrade/update 验证必须如何同步；识别官方扩展面约束、throwaway 验证方案和 SSOT/漂移风险。
- Scope: mixed
- Date: 2026-07-10

## Findings

### 1. Issue #96 的调研边界

Issue #96 明确要求完整移除 Guru Team 原 `handoff` 概念，而不是把同一 payload 换路径。新边界分成：

1. task-local、git tracked、可移植的 `.trellis/tasks/<task-slug>/task-start-context.json`；
2. 只存在于当前命令输出/进程内存的本机运行态；
3. repo/team 级 `.trellis/guru-team/config.yml` 与 schema/manifest 合同。

Issue 同时明确：不保留 legacy fallback、不迁移旧任务、不继续读取 `.trellis/guru-team/handoff.json`，且 Trellis 官方 task lifecycle、workspace journal、`trellis init/update` core 行为不在本 issue 内。Issue URL：`https://github.com/castbox/guru-trellis/issues/96`。

当前 task PRD 与 Issue 的核心目标一致，要求重建 `task-start-context.json` 和 local runtime state 边界；实施前应继续以 Issue 实时正文为范围 SSOT，并用 PRD 承接本 task 的设计/实现计划。相关文件：`.trellis/tasks/07-10-096-task-runtime-boundary/prd.md`。

### 2. 必须同步的 canonical 文档与 overlay

#### 2.1 Workflow 与 marketplace SSOT

- `trellis/workflows/guru-team/workflow.md`：canonical workflow 合同。所有 Phase 0 intake、workspace boundary、planning/check/review gate 中的 `handoff`、`handoff.workspace_path`、`handoff approval`、`implementation handoff` 等术语必须逐一分类：原 intake handoff 必须改为“任务启动上下文/本机运行态”；实现代理交接若只是自然语言过程，也应避免继续使用会被误读为共享 artifact SSOT 的 `handoff` 命名。
- `.trellis/workflow.md`：dogfood active copy。当前与 canonical 完全相同；修改 canonical 后必须同步并再次比较。项目 spec 明确 canonical 与 dogfood 的关系：`.trellis/spec/workflow/index.md:28`、`.trellis/spec/workflow/index.md:29`、`.trellis/spec/workflow/index.md:30`。
- `trellis/index.json`：marketplace id/path 当前正确，`guru-team` 为 `type: workflow` 且 path 指向 canonical workflow（`trellis/index.json:5`、`trellis/index.json:6`、`trellis/index.json:9`）。Issue #96 不要求更换 workflow id；除非公共 API 发生破坏性版本分叉，否则应保持 id 稳定。
- `trellis/workflows/guru-team/config-template.yml`：仍含旧 `handoff` artifact/schema 配置引用，必须改成新 task-start-context/schema 合同或删除已不再属于共享配置的项。
- `trellis/guru-team-extension.json`：公共 artifact contract 当前仍声明 `.trellis/guru-team/handoff.json`（`trellis/guru-team-extension.json:32`、`trellis/guru-team-extension.json:33`），必须替换为 task-local `task-start-context.json` 合同，并同步 companion script/schema 清单与 extension version/release notes。

#### 2.2 Preset canonical assets

- `trellis/workflows/guru-team/schemas/intake-handoff.schema.json`：旧 schema 名称和数据模型与新概念冲突，必须删除/替换为新 task-start-context schema；不能保留旧 schema 作为 fallback。
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 及对应 tests：虽然本报告不做代码调研结论，但 workflow/preset SSOT 必须把脚本输出合同、读取路径和安全边界同步到新命名；脚本只能 recorder/validator/executor，不能把 AI 判断重新编码进 runtime payload。
- `trellis/workflows/guru-team/scripts/bash/prepare-task.sh`、`check-workspace-boundary.sh`、`check-env.sh`、`version.sh` 等 wrapper：README/安装清单/验证脚本中的命令合同必须与新输出字段一致。
- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`：`MANAGED_ASSET_PATHS` 当前显式包含 `schemas/intake-handoff.schema.json`（`trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py:44`）；必须改为新 schema，并设计旧 managed file 的确定性删除/迁移规则。
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`：当前只断言 extension/companion assets、workflow preview/switch 等；必须新增“旧 handoff 不存在、新 task-start-context 正确生成、本机路径不进入 tracked artifact”的断言。现有 workflow preview/switch 基线在 `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh:246` 至 `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh:257`。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：继续作为 overlay canonical→dogfood 漂移检查，但它只遍历 canonical overlay 中存在的文件并比较 missing/changed（`trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh:51` 至 `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh:67`），不会发现 dogfood 中多余的旧文件；Issue #96 需要另加 obsolete-file 断言或清理验证。

#### 2.3 必须同步的 overlay 文件

实时 `rg` 发现以下 canonical overlay 仍引用 `handoff`，必须逐个改并通过 preset installer 同步 dogfood：

- `trellis/presets/guru-team/overlays/.agents/skills/trellis-start/SKILL.md`：Phase 0 intake、executor 输出、workspace boundary。
- `trellis/presets/guru-team/overlays/.agents/skills/trellis-continue/SKILL.md`：planning approval 与 workspace boundary。
- `trellis/presets/guru-team/overlays/.trellis/agents/implement.md`、`trellis/presets/guru-team/overlays/.trellis/agents/check.md`：实现/check 代理输入与输出术语。
- `trellis/presets/guru-team/overlays/.codex/prompts/trellis-start.md`、`trellis/presets/guru-team/overlays/.codex/prompts/trellis-continue.md`。
- `trellis/presets/guru-team/overlays/.codex/skills/trellis-start/SKILL.md`、`trellis/presets/guru-team/overlays/.codex/skills/trellis-continue/SKILL.md`。
- `trellis/presets/guru-team/overlays/.codex/agents/trellis-implement.toml`、`trellis/presets/guru-team/overlays/.codex/agents/trellis-check.toml`。
- `trellis/presets/guru-team/overlays/.claude/commands/trellis/continue.md`、`trellis/presets/guru-team/overlays/.claude/agents/trellis-implement.md`、`trellis/presets/guru-team/overlays/.claude/agents/trellis-check.md`。
- `trellis/presets/guru-team/overlays/.cursor/commands/trellis/continue.md`、`trellis/presets/guru-team/overlays/.cursor/agents/trellis-implement.md`、`trellis/presets/guru-team/overlays/.cursor/agents/trellis-check.md`。

当前所有 canonical overlay 与 dogfood 安装副本 `cmp` 结果均为 `SAME`。这证明现状无漂移，但也意味着实施时不能只改 `.agents/`、`.codex/`、`.claude/`、`.cursor/` 或 `.trellis/agents/` 下的 dogfood 文件；必须先改 `trellis/presets/guru-team/overlays/`，再运行 installer 同步。

#### 2.4 Public docs 与 requirements SSOT

- `README.md`：安装、Phase 0、workspace boundary、planning/check/review 示例多处直接暴露 `.trellis/guru-team/handoff.json`、`handoff_written`、`handoff.workspace_path`；必须改成新概念和新命令输出。
- `trellis/workflows/guru-team/README.md`：marketplace 只安装/switch workflow，preset 安装 companion assets；还描述 `.bak/.new` 与 extension manifest，必须补充旧 artifact 删除、task-local context 与 runtime-only 安全边界。
- `trellis/presets/guru-team/README.md`：installed files、managed assets、升级行为、throwaway 验证命令必须同步新 schema/artifact 和 obsolete-file 清理规则。
- `docs/requirements/requirement-main.md`：需求语义 SSOT，当前包含 handoff、workspace path 和流程合同，必须以 Issue #96 新概念重写对应要求。
- `docs/requirements/guru-team-trellis-flow.md`：流程细化文档，必须同步 Phase 0 输出、task artifact 落盘、workspace boundary 与安全校验。
- `docs/requirements/README.md`：导航/范围描述若引用旧概念必须同步。

项目 docs spec 要求 workflow 行为变化必须更新用户实际阅读的三个 README（`.trellis/spec/docs/public-docs.md:68` 至 `.trellis/spec/docs/public-docs.md:75`），因此 README 同步不是可选项。

### 3. 官方扩展面约束

#### 3.1 Workflow 行为必须留在 Markdown

Trellis 官方 custom workflow 文档明确：`/.trellis/workflow.md` 定义 phase、skill routing、per-turn reminders 和 `task.py` command catalog；fork workflow 只需改 Markdown，不需要改 Python、hook 或重新发布 Trellis。所有 injection path 在运行时读取 workflow（官方文档 `advanced/custom-workflow.md`，2026-07-10 实时读取，第 9-27 行）。

对 Issue #96 的含义：

- “什么时候读取任务启动上下文”“AI 如何区分可移植事实与 runtime state”“何时要求用户确认”“如何解释 workspace boundary”属于 workflow/skill/prompt 判断合同。
- Python/shell 只能产生或校验客观字段、路径、hash、当前 worktree/runtime 状态；不能把 intake scope 判断、是否可继续、是否需要 follow-up 等 AI 判断塞回新 JSON。
- 不应修改 Trellis 上游源码、全局 npm 包、`node_modules` 或 parser hook 来实现语义分叉。

#### 3.2 Workflow marketplace 与 preset 是不同扩展面

- `trellis/index.json` 中 `type: workflow` 的 marketplace entry 只负责安装/切换 `.trellis/workflow.md`。
- Guru Team companion scripts、schema、config、platform skills/prompts/agents 由 preset installer 安装；不能期待 `trellis workflow` 自动同步这些资产。
- workflow id、preset 路径、artifact/schema 名称属于公共 API。Issue #96 明确允许移除 legacy handoff，但仍应通过 extension version/release notes 和 upgrade 文档说明破坏性 artifact 变更。

#### 3.3 Spec template marketplace 不能承载 runtime/task 状态

官方 spec marketplace 文档明确禁止在 reusable spec template 中放 `.trellis/tasks/`、`.trellis/workspace/`、active task state 和平台 prompt 文件；平台 prompts 属于 platform customization，产品 PRD 也不属于公共 spec template（官方 `advanced/custom-spec-template-marketplace.md`，实时读取，第 162-182 行）。

因此：

- `task-start-context.json` 绝不能进入 spec marketplace/template。
- local runtime state 绝不能进入 spec template 或 tracked public docs 示例的真实 payload。
- `.trellis/spec/` 只能记录可复用工程约定/contract/checklist，不可成为当前 task context 的存储位置。

#### 3.4 `trellis update` 与 `trellis upgrade` 的边界

本机实时 CLI 为 Trellis `0.6.5`。

- `trellis update`：更新项目中的 Trellis configuration/commands；支持 `--dry-run`、`--force`、`--skip-all`、`--create-new`、`--allow-downgrade`、`--migrate`。
- `trellis upgrade`：更新全局 Trellis CLI npm package；支持 `--tag` 和 `--dry-run`，不等同于更新项目内 Guru Team marketplace/preset。
- 官方 configuration 文档说明 `trellis update` 会保留 `.trellis/config.yaml` 本地修改，并可通过 migration manifest append 新 config sections；`update.skip` 在普通 update 中阻止 template writes 和 safe-file-delete，`--migrate` 的 breaking migration 可为必需清理绕过 skip 并先警告（官方 `advanced/configuration.md`，实时读取，第 112-144 行）。

Issue #96 不应修改 Trellis core update 行为。Guru Team 必须自行定义并验证：官方 CLI upgrade/update 后，重新安装 marketplace workflow 与重新应用 preset，旧 handoff artifact 是否被确定性清理、新 SSOT 是否恢复、用户本地 config 是否保留。

### 4. Throwaway 安装验证方案

#### 4.1 新仓库安装

在全新临时 git repo 中执行，且 marketplace/preset 必须指向当前待测 branch/ref，而不是仅验证公开旧 tag：

1. 记录 `trellis --version`、`which trellis` 和待测 Guru Team extension version/ref。
2. `trellis init -y --workflow guru-team --workflow-source <current-branch-source>`；验证 `trellis/index.json` 可发现 `guru-team`、type/path 正确。
3. 运行 preset installer，默认 Codex+Cursor 路径和 `--all-platforms` 路径至少各覆盖一次。
4. 断言不存在 `.trellis/guru-team/handoff.json` 和 `schemas/intake-handoff.schema.json`。
5. 断言存在新 schema、extension manifest 的 `artifact_contracts` 包含 task-local `task-start-context.json` 形态且不含旧 handoff。
6. 运行 `check-env.sh --json` 与 Phase 0 planner-only `prepare-task.sh --json`：确认输出可包含绝对路径/dirty/worktree 诊断，但命令未写 tracked fixed runtime artifact。
7. 在明确 executor 路径创建 task/worktree 后，断言 `.trellis/tasks/<task>/task-start-context.json` 存在，字段仅包含 Issue 规定的可移植字段；扫描内容不得出现 `/Users/`、`/tmp/<worktree>`、`repo_root`、`worktree_root`、`workspace_path`、`existing_worktrees`、developer identity path 等本机字段。
8. 验证 task-start-context 中 `task_artifact_dir` 是 repo-relative `.trellis/tasks/...`，不是 worktree 根路径。
9. 运行 workspace boundary、planning、check/review/finish 的无副作用或 fail-closed 入口，确认它们从 task-local context + 当前 runtime 重新求值，不读取旧 handoff。
10. 对 Codex、Claude、Cursor 安装后的入口做 `rg`，旧 `handoff` 概念不得残留；若保留通用“agent handoff”英文，必须明确它不是 artifact/SSOT，最好统一改为中文“实现结果/检查结论/交接摘要”等不歧义术语。

#### 4.2 已有项目 workflow preview/switch

1. 准备已安装旧 Guru Team 版本的 throwaway repo，包含旧 `.trellis/guru-team/handoff.json`、旧 schema、旧 overlays 和用户自定义 `.trellis/guru-team/config.yml`。
2. 先运行 `trellis workflow --marketplace <source> --template guru-team --create-new`，检查 `.trellis/workflow.md.new` 使用新概念且 active workflow 未变化。
3. 人工/测试确认后运行不带 `--create-new` 的切换命令（或 `--force` 的自动化测试路径），验证 active `.trellis/workflow.md` 更新。
4. 运行新版 preset installer；验证用户 config 内容不被覆盖，managed scripts/schema 更新产生预期 `.bak`，未知 overlay 本地修改产生 `.new`。
5. 关键新增断言：旧 `.trellis/guru-team/handoff.json` 和旧 `intake-handoff.schema.json` 必须被删除或由显式 migration/obsolete list fail-closed 处理，不能仅因不在新 `MANAGED_ASSET_PATHS` 中而静默残留。
6. 扫描 `.new`、`.bak`、旧 artifact、旧术语；任何未处理结果都应让验证失败或在最终报告明确阻塞。

#### 4.3 Upgrade/update 抗漂移矩阵

至少覆盖以下矩阵：

| 场景 | 操作顺序 | 必须验证 |
| --- | --- | --- |
| 新 repo | `trellis init` → marketplace workflow → preset | 新文件齐全、旧 handoff 从未出现、入口一致 |
| 旧 Guru Team repo | workflow `--create-new` → review → switch → preset | 旧 artifact 被清理、config 保留、`.new/.bak` 可审计 |
| 官方 project update | 旧 Guru Team repo → `trellis update --dry-run` → `trellis update` → 重应用 marketplace/preset | 官方托管文件变化不回退 Guru Team 语义；preset 可恢复 overlay；无幽灵 handoff |
| 官方 CLI upgrade | `trellis upgrade --dry-run`/指定测试版本 → `trellis update` → 重应用 Guru Team | CLI 版本证据、marketplace 可识别、preset 兼容、命令入口仍可运行 |
| 用户修改 overlay | 制造未知本地修改 → 重应用 preset | 生成 `.new`，不静默覆盖；人工处理后 drift check 通过 |
| 用户修改 managed script | 制造 managed 文件修改 → 重应用 preset | 更新 canonical 版本并生成 `.bak`；backup 内容可审计 |
| obsolete tracked artifact | 安装旧版本后升级 | 旧 handoff/schema 被确定性删除；删除受 manifest/version/migration 约束 |

建议在现有 `verify-throwaway-install.sh` 基础上增加“fresh install”和“old-version upgrade fixture”两个阶段；不要只验证当前 branch 的全新安装，因为 Issue #96 的最高风险正是旧 tracked fixed artifact 残留。

### 5. 可能的 SSOT / 漂移风险

#### P0/P1 级风险

1. **旧 tracked artifact 残留**：当前 installer 的 managed copy 逻辑对已存在 managed 文件会备份为 `.bak` 后覆盖（`apply_guru_team_trellis_preset.py:349` 至 `apply_guru_team_trellis_preset.py:359`），但未发现通用 obsolete managed-file 删除合同。若仅从 `MANAGED_ASSET_PATHS` 删除旧 handoff/schema，新版安装可能不再管理它们，却让旧文件永久残留。
2. **drift checker 只做单向集合比较**：`check-dogfood-overlay-drift.sh` 只确认 canonical overlay 在 dogfood 中存在且相同，不检查 dogfood 多余文件。旧 overlay/入口文件即使从 canonical 删除，也可能不被发现。
3. **workflow 与 preset 分开升级**：用户只运行 `trellis workflow` 会得到新 `.trellis/workflow.md`，但 scripts/schema/overlays 仍旧；用户只运行 preset 则 active workflow 可能仍旧。README 和 verifier 必须明确固定顺序并校验 extension/workflow 版本匹配。
4. **manifest 自相矛盾**：`trellis/guru-team-extension.json`、安装后的 `.trellis/guru-team/extension.json`、preset `MANAGED_ASSET_PATHS`、README installed files、schema 名称若任一漏改，会形成多个“官方清单”。应以 canonical extension manifest + canonical workflow source 为源，installer 生成安装 manifest，README/测试对其验证。
5. **绝对路径回流 task artifact**：即使固定 handoff 删除，若 `prepare-task` 把完整 runtime payload直接嵌入 task-start-context，仍会提交 `repo_root/worktree_root/workspace_path/existing_worktrees`。必须使用 allowlist schema，而不是从旧 payload denylist 删除字段。

#### P2/P3 级风险

6. **术语漂移**：`handoff` 同时出现在 intake、implementation、check、review 文案中。只替换文件名会保留错误 mental model；需要按语义重命名，而不是全局机械替换。
7. **requirements 与执行文案分叉**：`docs/requirements/requirement-main.md`、`guru-team-trellis-flow.md`、三个 README、workflow、skills/prompts 均描述同一链路。需要定义语义 SSOT：requirements 定义产品要求，canonical workflow 定义 AI runtime 合同，extension manifest 定义安装公共 API，README 只做用户导航/命令，不复制完整规则。
8. **public API version 不更新**：删除 artifact/schema 是破坏性扩展变更。即便 workflow id 保持 `guru-team`，extension version/release notes、upgrade 指南和 compatibility evidence 必须更新。
9. **只跑 dogfood 验证**：当前 canonical overlay 与 dogfood 完全一致，但这不能证明新仓库可安装，也不能证明旧版本升级可清理旧文件。必须保留独立 throwaway fresh/upgrade 验证。
10. **把官方 update 当 Guru Team updater**：`trellis update` 只负责官方项目模板更新，`trellis upgrade` 只更新全局 CLI；两者都不会天然同步 Guru Team marketplace/preset。文档若写成“运行 update 即完成 Guru Team 升级”会产生静默漂移。

### 6. Files found

- `AGENTS.md` — 仓库级官方优先、Markdown/脚本边界、开箱即用与 upgrade/update 门禁。
- `.trellis/tasks/07-10-096-task-runtime-boundary/prd.md` — 当前 task 对 Issue #96 的需求承接。
- `trellis/workflows/guru-team/workflow.md` — canonical Guru Team workflow runtime 合同。
- `.trellis/workflow.md` — 当前仓库 dogfood active workflow；实时比较与 canonical 相同。
- `trellis/index.json` — workflow marketplace registry，发布 `guru-team` id/path/type。
- `trellis/guru-team-extension.json` — extension 公共 API、managed paths、artifact contracts、版本。
- `trellis/workflows/guru-team/config-template.yml` — Guru Team repo/team 共享配置模板。
- `trellis/workflows/guru-team/schemas/intake-handoff.schema.json` — 待移除的旧 handoff schema。
- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py` — preset managed assets、overlay copy、`.bak/.new` 行为。
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh` — 当前 fresh throwaway 安装与 workflow preview/switch 验证。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh` — canonical→dogfood 单向文件比较。
- `trellis/presets/guru-team/overlays/` — Codex/Claude/Cursor/shared skills 与 runtime agents 的 canonical overlay 源。
- `.agents/skills/`、`.codex/`、`.claude/`、`.cursor/`、`.trellis/agents/` — 当前 dogfood 安装副本。
- `README.md` — 对外安装、升级、Phase 0、daily workflow 文档。
- `trellis/workflows/guru-team/README.md` — marketplace workflow 行为与安装边界。
- `trellis/presets/guru-team/README.md` — preset installer 行为、安装文件和验证说明。
- `docs/requirements/requirement-main.md` — Guru Team Trellis 需求主 SSOT。
- `docs/requirements/guru-team-trellis-flow.md` — workflow 需求流程细化。
- `.trellis/spec/workflow/index.md`、`.trellis/spec/workflow/workflow-contract.md`、`.trellis/spec/workflow/companion-scripts.md` — workflow canonical/dogfood、AI 判断/脚本边界和 gate 合同。
- `.trellis/spec/preset/index.md`、`.trellis/spec/preset/installer.md`、`.trellis/spec/preset/overlay-guidelines.md` — preset public API、installer、overlay 同步/验证约定。
- `.trellis/spec/docs/public-docs.md` — README SSOT 同步和安装/升级文档要求。

### 7. External references

- Trellis Custom Workflow: `https://docs.trytrellis.app/advanced/custom-workflow.md` — `workflow.md` 是 phase/routing/state/task catalog 的 runtime Markdown 合同，hooks 为 parser-only。
- Trellis Custom Spec Template Marketplace: `https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md` — spec template 内容边界、禁止 active task/workspace/platform prompts、template id versioning。
- Trellis Configuration: `https://docs.trytrellis.app/advanced/configuration.md` — `update.skip`、`--migrate` 清理语义、config append-only migration/update 行为。
- Local Trellis CLI `0.6.5`: `trellis update --help` 与 `trellis upgrade --help` — project update 与 global CLI upgrade 命令边界。
- GitHub Issue #96: `https://github.com/castbox/guru-trellis/issues/96` — 本调研的实时需求/范围来源。

### 8. Related specs

- `.trellis/spec/workflow/index.md`
- `.trellis/spec/workflow/workflow-contract.md`
- `.trellis/spec/workflow/companion-scripts.md`
- `.trellis/spec/workflow/data-contracts.md`
- `.trellis/spec/workflow/quality-guidelines.md`
- `.trellis/spec/preset/index.md`
- `.trellis/spec/preset/installer.md`
- `.trellis/spec/preset/overlay-guidelines.md`
- `.trellis/spec/docs/index.md`
- `.trellis/spec/docs/public-docs.md`

## Caveats / Not Found

- 本次是只读调研，未运行会写文件的 preset installer、`trellis update`、`trellis upgrade`、throwaway init、task executor 或 Git 操作；所有验证方案均为待实施阶段执行的测试计划。
- 官方 docs `llms.txt` 中未发现独立的 `trellis update` / `trellis upgrade` 维护页；本报告对命令 flags 的证据来自本机 Trellis `0.6.5` CLI help，对 project config/update 语义的证据来自官方 configuration 文档。实施时若升级目标版本变化，必须重新实时核验对应 CLI help 和官方文档。
- Issue #96 明确不处理官方 Trellis core lifecycle/update 行为，因此不能为了清理 Guru Team 旧 artifact 去 patch 上游 Trellis；清理应由 Guru Team preset/versioned migration/validator 负责。
- 当前 `check-dogfood-overlay-drift.sh` 未检查 dogfood 中“canonical 已删除但目标仍存在”的额外文件；这是已确认的 not-covered gap，不应把现有 drift check pass 解释为 obsolete-file clean。
- 本报告仅覆盖用户指定的 workflow/preset/docs/upgrade-update SSOT；脚本内部字段设计、schema 精确字段、单元测试实现细节应由对应代码/schema 调研继续给出。
