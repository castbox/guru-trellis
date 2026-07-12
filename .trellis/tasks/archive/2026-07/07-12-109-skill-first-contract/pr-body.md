## 变更摘要

- 在根 `AGENTS.md` 增加 Skill-first 闭环流程模块化强制规范，明确项目运行时 workflow SSOT 与 step-local skill SSOT 的职责边界。
- 规定 mandatory invocation、workflow/standalone 同门禁、typed exits 与 fail-closed consumer，避免流程只在主 workflow 中成立。
- 固定 AI 判断与 companion script 的分层，并定义强制 skill 化、禁止无意义 wrapper、`guru-<action>-<object>` 命名和 package state boundary。

## 影响范围

- 唯一业务规范变更是根 `AGENTS.md`；现有章节顺序与官方 Trellis 优先、Markdown/脚本分层、副作用控制等规则保持一致。
- 当前 task artifacts 记录规划审批、Phase 2、finding closure、四轮 Branch Review 和 issue scope 证据，不形成第二份长期业务规范。
- 不修改 workflow、preset、marketplace、overlay、installer、skill、prompt、script、schema、测试或平台入口。

## 验证结果

- `git diff --check` 与 `git diff --check origin/main...HEAD` 通过。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-12-109-skill-first-contract` 通过，`implement.jsonl` 与 `check.jsonl` 各 4 条。
- `.trellis/guru-team/scripts/bash/check-commit-messages.sh --json --task .trellis/tasks/07-12-109-skill-first-contract` 通过，两条分支提交均符合仓库提交规范。
- 受控措辞、二级标题序列、issue ledger 集合、task JSON、artifact digest 和敏感信息扫描通过。
- 本次未修改 workflow、preset、overlay、installer 或 companion script，因此 throwaway 安装、overlay drift 与 upgrade/update 重放门禁不适用，未将其声明为已验证能力。

## Review Gate

- Branch Review Gate 已绑定 HEAD `a97d42fd44cf886e6ccadd07550b949d570203ee` 并通过，P0/P1/P2/P3 findings 均为 0。
- Round 001 的 Phase 2 closure 归因 P2 已由 fresh Phase 2 checker 复核并在 Round 002 关闭；Round 003 覆盖旧 HEAD，Round 004 使用全新 reviewer 覆盖 corrective metadata commit 后的完整 `origin/main...HEAD`。
- 最终审查覆盖 live #109/#120、R1-R5、8 项验收标准、Docs SSOT、task lifecycle、commit messages、安全和部署影响。

## Issue 关闭范围

Closes #109

### 后续范围

- Follow-up #120：建立 Guru Team 闭环 Skill 合同与 Canonical 分发基础设施。
- `guru-create-work-commit` 闭环 skill 作为 #120 完成后的独立具体实施候选，不属于本 PR。

## Docs SSOT

- 状态与策略：`complete_docs / ssot_first`。
- `durable_docs`：根 `AGENTS.md` 是本次 Skill-first 原则的 durable docs SSOT。
- `task_history`：当前 task planning/review/research 仅保留任务差异、审查证据和后续候选。
- 已完成的文档同步仅限 `AGENTS.md`；不需要同步 workflow/preset/overlay/skill，因为本 issue 不实现这些运行资产。
- #120 独立承接 canonical package、distribution、managed hash、structure validator 与 throwaway 验收，本 PR 不提前实现或关闭该范围。

## 安全说明

- 不包含 token、secret、private key、签名 URL、`.env`、数据库 URL、客户数据或敏感原始记录。
- 不新增或修改运行时代码、配置、API、schema、依赖、CI/CD、容器、Docker Compose、Kubernetes/Kustomize、数据库 migration 或 Makefile。
- 无部署步骤、运行时配置迁移、数据库迁移或回滚操作；风险仅限 AI Agent 后续执行仓库流程时需遵守新增原则。
