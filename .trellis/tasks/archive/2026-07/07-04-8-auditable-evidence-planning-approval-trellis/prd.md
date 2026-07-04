# #8 为 planning approval 和 trellis-check 增加可审计证据

## 目标

把 Guru Team workflow 中两个依赖 AI 判断的关键步骤从“口头执行过”升级为可审计 artifact：

- Phase 1.4 进入实现前，必须有 planning approval / start gate 证据。
- Phase 2.2 进入 commit / Branch Review Gate 前，必须有覆盖完整 task scope 的 check report 证据。

同时修复本次额外发现的问题：worktree preflight / worktree 创建前应先更新或校验本地 base branch 已同步到远端最新版本，避免从过期 `main` / `dev` 创建任务分支。

## 背景与证据

- GitHub issue：`https://github.com/castbox/guru-trellis/issues/8`。
- 官方 Trellis 文档已核对：
  - `https://docs.trytrellis.app/advanced/custom-workflow.md`：workflow 行为应通过 `.trellis/workflow.md` 控制，AI 运行时读取 Markdown 合同。
  - `https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md`：spec template marketplace 只放可复用工程约定，不放 task/runtime 状态。
- 本仓库规范已核对：
  - `.trellis/spec/workflow/workflow-contract.md`
  - `.trellis/spec/workflow/companion-scripts.md`
  - `.trellis/spec/workflow/data-contracts.md`
  - `.trellis/spec/workflow/quality-guidelines.md`
  - `.trellis/spec/preset/installer.md`
  - `.trellis/spec/preset/overlay-guidelines.md`
- 现状确认：
  - `task.py start` 只写任务状态，不证明 planning review 已发生。
  - `review-branch.sh` 已有先 AI/human review、再 recorder/validator 的模式，可作为本次两个 gate 的实现范式。
  - `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py::prepare_workspace()` 直接从本地 ref 创建 worktree；当前没有 `git fetch`、远端 HEAD 记录或 base stale 阻塞。

## 需求

### R1 Planning Approval Gate

- 新增 task-local planning approval artifact，建议文件名为 `planning-approval.json`。
- artifact 必须记录：
  - task 路径、生成时间、AI/human reviewer 身份或会话标识；
  - 被批准的 `prd.md`、`design.md`、`implement.md` 路径、sha256、size、modified_at；
  - 用户确认进入实现的证据摘要；
  - 当前 git HEAD 和 dirty 文件清单；
  - 该 artifact 是 recorder/validator 证据，不替代 AI/human 判断。
- 缺少 artifact、artifact 缺少必填字段、规划文件 hash 变化、或 artifact 记录的 HEAD 与当前 HEAD 不匹配时，workflow helper 必须阻塞进入实现。
- workflow / continue overlay 必须明确：先写 `planning-approval.json`，再执行 `task.py start`；`task.py start` 仍只是状态写入。

### R2 Phase 2 Check Report Gate

- 新增 task-local Phase 2 check artifact，建议文件名为 `phase2-check.json`。
- artifact 必须记录：
  - 当前 HEAD、working tree diff fingerprint 或 dirty 文件清单；
  - 读取过的 task artifacts 和 `.trellis/spec/` 文件；
  - 执行的验证命令及结果摘要；
  - checklist 覆盖：requirements、design、code、tests、spec sync、cross-layer consistency、docs SSOT、deployment impact；
  - findings、severity、状态；
  - 该 artifact 是 AI 执行完整 `trellis-check` 后的 recorder/validator 证据，不是几个 shell 命令的替代品。
- 缺少 check report、report stale、或存在未处理 P0/P1/P2 findings 时，commit 和 Branch Review Gate 前必须阻塞。

### R2.5 Branch Review Gate 独立审查来源

- Branch Review Gate 的通过结论必须建立在独立 Agent 审查完整 branch diff 后无 P0/P1/P2 findings 的基础上。
- `review-branch.sh --pass` 必须要求客观 metadata：
  - `--review-source independent-agent`；
  - 非主会话 / 非 self-review 的 `--reviewer`；
  - task-local `review.md` 的 digest。
- 主会话可以协调 review、读取 report、记录 gate，但不能用 `codex-main-session` / `claude-main-session` / `cursor-main-session` / `*-main-session` / `self-review` 作为 passed gate 来源。
- 如果当前平台或会话无法获得独立 Agent review evidence，workflow 必须停止在 Branch Review Gate pending，而不是让脚本 gate 假装通过。

### R3 Preflight Base Freshness

- `prepare-task.sh --create-worktree` / `--create-task` 在创建 worktree/branch 前必须更新或校验基础分支的远端最新状态。
- 默认行为应执行 `git fetch <remote> <base>`，记录 fetch 前后 local/remote HEAD，并在本地 base 落后远端时 fast-forward 本地 base；如果不能 fast-forward，应 fail closed。
- planner-only `prepare-task.sh --json` 不应创建 worktree 或写文件，但应在输出中报告 base freshness 状态或 stale 风险；executor 路径必须强制 fresh。
- handoff preflight evidence 应记录 base freshness 结果，供 Branch Review Gate 后续核对。

### R4 Canonical / Dogfood / Overlay 同步

- 长期源头必须更新在 `trellis/workflows/guru-team/` 和 `trellis/presets/guru-team/overlays/`。
- 本仓库 dogfood copy 必须同步：
  - `.trellis/workflow.md`
  - `.trellis/guru-team/scripts/*`
  - `.agents/skills/*`
  - `.codex/prompts/*` 与 `.codex/skills/*`
- preset README / workflow README / 根 README 中的日常入口说明应反映新 gate。

### R5 安全与边界

- 不修改 Trellis 上游源码、全局 npm 包或 `node_modules`。
- 不把业务仓库私有规则写进 marketplace workflow 或 spec template。
- artifact 不得包含 token、secret、`.env`、签名 URL、数据库 URL 或客户原始数据。

## 验收标准

- [ ] workflow 明确区分：`task.py start` 是状态写入，planning approval 是 AI/human review evidence。
- [ ] 缺少 `planning-approval.json` 或 artifact stale 时，进入实现前的 helper 检查失败。
- [ ] workflow 明确区分：验证命令只是 check evidence 的一部分，不等于完整 `trellis-check`。
- [ ] 缺少 `phase2-check.json`、report stale、或存在未处理 P0/P1/P2 findings 时，commit / Branch Review Gate 前的 helper 检查失败。
- [ ] `review-branch --pass` 缺少 `--review-source independent-agent`、使用 main-session/self-review reviewer，或没有 task-local review report digest 时必须失败。
- [ ] `review-branch --pass` 的 `--review-report` 必须指向 task-local `review.md`，不能用 `prd.md` / `design.md` / 其他 task artifact 冒充。
- [ ] workflow / overlay 明确：Branch Review Gate 通过前必须有独立 Agent review，无独立 review 时保持 pending，不能由主会话 self-review 通过。
- [ ] `trellis-continue` / platform overlays 同步要求 start 前写入/检查 planning approval，commit 前写入/检查 check report。
- [ ] `prepare-task --create-worktree` / `--create-task` 在 worktree 创建前刷新并校验 base branch 最新状态，handoff 记录 preflight freshness evidence。
- [ ] 有 focused 单元测试或 dry-run 覆盖 planning/check gate 缺失、stale、通过路径，以及 base freshness 的关键分支。
- [ ] throwaway install 验证必须覆盖当前分支 workflow marketplace 内容和 existing-project `trellis workflow --create-new` 预览/切换路径；如果只验证公开远端 marketplace，最终报告必须明确风险。
- [ ] 应用 preset 到 dogfood copy 后 drift check 通过，未遗留 `.new` / `.bak`。

## Durable Docs SSOT

本仓库没有独立 `docs/` 目录。长期说明由以下文件承载：

- `README.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`
- `.trellis/spec/workflow/*`
- `.trellis/spec/preset/*`

本次会把长期流程合同和安装/升级说明回写到上述 durable docs，task artifact 只保留本次任务证据。

## 中台知识门禁

本任务修改 Trellis workflow/preset/companion scripts，不涉及 Guru Team 中台 SDK 或 framework；Middle-platform Knowledge Gate 不适用。

## 不在范围内

- 不改 Trellis 官方 CLI 源码或 npm 包。
- 不为所有业务仓库自动迁移历史 artifact。
- 不把 `planning-approval.json` 或 `phase2-check.json` 作为 spec template 内容发布。
- 不新增独立用户日常命令阶段；仍通过 `trellis-continue` / `trellis-finish-work` 驱动。
