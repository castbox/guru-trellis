# 第 001 轮独立 Branch Review 原始报告

## 审查身份与结论

- 审查角色：`/root/branch_review_109`，未参与实现或 Phase 2 check。
- 审查工作区：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/109-skill-first-contract`。
- 审查范围：`origin/main...HEAD`。
- 审查 HEAD：`0e3f18b8d4740b0e45c0c9bfade6252a787a09df`。
- 结论：**FAIL**。发现 1 个 P2；按 Guru Team 规则，任意优先级 finding 均阻止 Branch Review Gate 通过。本轮不是 final-pass。

## Workspace 边界证据

- `pwd`：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/109-skill-first-contract`。
- `git rev-parse --show-toplevel`：同上。
- `.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task .trellis/tasks/07-12-109-skill-first-contract`：`status=ok`。
- `expected_workspace` 与 `actual_repo_root` 完全一致；`source_checkout=/Users/wumengye/Documents/GoProjects/guru-trellis`，`source_checkout_status=[]`，`suspicious_source_artifacts=[]`。
- 审查开始时 task worktree 只有 `agent-assignment.json` 和 `research/commit-message-loop-analysis.md` 两个 task-local metadata/research 路径未提交；没有非 metadata 工作区漂移。

## 已审查范围

### Live GitHub scope

- #109 `建立 Guru Team Skill-first 闭环流程模块化强制规范`：OPEN；当前范围是只修改根 `AGENTS.md`，建立 Skill-first 原则。
- #120 `建立 Guru Team 闭环 Skill 合同与 Canonical 分发基础设施`：OPEN；是后续独立 owner，不是本分支交付。
- `issue-scope-ledger.json` 的集合语义正确：`close=[109]`、`related=[]`、`followup=[120]`，集合互斥。

### 完整 committed diff

- `origin/main...HEAD` 只有 1 个 commit：`0e3f18b docs(agents): #109 建立 Skill-first 闭环流程原则`。
- 业务文件只有根 `AGENTS.md`；其余 14 个 committed 路径均位于当前 task 目录。
- 已读取完整 `AGENTS.md` 及其 diff，逐项检查 global runtime workflow SSOT、step-local skill SSOT、platform entry、stable-id mandatory invocation、closed-loop 顺序、workflow/standalone parity、typed exits、fail-closed、AI/script 边界、拆分与禁止 wrapper、公共 API 和 package state boundary。
- `AGENTS.md` 正文满足 #109 验收语义，未声称已经交付 #120 的 runtime、installer、schema、validator、canonical package 或分发设施。

### Task 与 gate artifacts

- `prd.md`、`design.md`、`implement.md`、`planning-approval.json`。
- `task.json`、`task-start-context.json`、`implement.jsonl`、`check.jsonl`。
- `agent-assignment.json`、`phase2-check.json`、`phase2-findings.json`、`issue-scope-ledger.json`。
- `research/proposed-issue-109-body.md`、`research/proposed-skill-contract-distribution-issue.md`。
- 当前 task-local metadata tail：`agent-assignment.json` 与未跟踪的 `research/commit-message-loop-analysis.md`。后者明确只是提交消息闭环问题的 task history，不扩张 #109，也未声称该研究提案已经实现或已经创建新 issue。

### 官方文档与引用 spec

- Trellis 官方 `index.md`、`advanced/custom-workflow.md`、`advanced/custom-skills.md`、`advanced/architecture.md`、`advanced/custom-spec-template-marketplace.md`。
- `.trellis/spec/workflow/workflow-contract.md`。
- `.trellis/spec/workflow/quality-guidelines.md`。
- `.trellis/spec/workflow/companion-scripts.md`。
- `.trellis/spec/guides/code-reuse-thinking-guide.md`。
- 官方文档确认 skill 是 capability/phase 级 reusable workflow module，`.trellis/workflow.md` 是运行时 phase/routing/workflow-state SSOT，平台目录承担适配；新增 `AGENTS.md` 原则与这些事实一致。

## Finding

### [P2] Phase 2 finding 生命周期与 checker 归因互相矛盾

`agent-assignment.json` 的 Phase 2 检查代理完成事件记录：`/root/trellis_check_109` 在 `2026-07-12T11:15:10Z` 已完成，并且只“修复并复验关闭 3 个 P2”（当前文件约第 228-237 行）。但 `phase2-check.json` 在 `2026-07-12T11:25:34Z` 生成时，把 4 个 P2 全部归因给同一 `checker=/root/trellis_check_109`，并声称全部经过 closure re-check（第 3、17-18、125-149 行）。第 4 个 `issue-scope-ledger.json` 分类 finding 对应的 checked artifact 修改时间为 `2026-07-12T11:23:59Z`（第 45-60 行），晚于该检查代理的 completed 事件；`agent-assignment.json.status_events[]` 中没有检查代理在 11:15 后复用、恢复或完成 closure re-check 的事件。

因此当前证据不能同时证明“检查代理只关闭 3 个 P2”和“同一检查代理关闭了 4 个 P2”。`issue-scope-ledger.json` 第 9、18、21 行又依赖 `phase2-check.json` 的完整覆盖/全部关闭声明作为 #109 close evidence，使该不一致进入 issue closure 论证。ledger 的 close/follow-up 分类本身正确，但 Phase 2 finding lifecycle 与 checker attribution 不可审计。

修复要求：由主会话把真实 finding owner、修复者和 closure reviewer 生命周期记录一致；若第 4 个 P2 是 Phase 2 完成后新增，必须按 workflow 由适格检查路径完成并留下对应 assignment/status/closure 证据，然后重新生成与真实事实一致的 Phase 2/ledger evidence。不能只改数字或摘要来掩盖缺失的 AI check evidence。

## Phase 2 post-commit audit

- Direct `.trellis/guru-team/scripts/bash/check-phase2-check.sh --json` 返回 exit 2：记录 HEAD 与当前 HEAD 不一致、dirty paths 不同、`agent-assignment.json` digest/size 变化。
- 该 direct mismatch 符合 workflow 已定义的 post-commit 场景，不能单独视为失败，也不能通过事后重录 Phase 2 来抹平。
- `phase2-check.json.head=530a8972576ec85e42354dc67755c1782ea701fe` 是当前 HEAD 的祖先。
- 从该祖先到当前 HEAD 的唯一非 task-metadata 路径是 `AGENTS.md`，且已包含在 `phase2-check.json.dirty_paths`。
- 当前 working tree 没有非 metadata dirty path。
- `prd.md`、`design.md`、`implement.md`、`planning-approval.json`、`issue-scope-ledger.json`、`phase2-findings.json` 和四份 checked spec 的当前 sha256 均匹配 Phase 2 记录。
- `agent-assignment.json` 是 workflow 明确允许在 post-commit Branch Review 阶段变化的 task metadata；其 digest stale 本身可按例外处理，但本报告 Finding 所述语义矛盾不能被 freshness 例外豁免。

## 验证结果

- `git diff --check origin/main...HEAD`：通过。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-12-109-skill-first-contract`：通过；`implement.jsonl`、`check.jsonl` 各 4 条。
- 所有 task 根目录 JSON 执行 `jq empty`：通过。
- issue ledger 断言：通过，`close=[109]`、`related=[]`、`followup=[120]` 且集合互斥。
- 业务路径分类：通过；排除 task metadata 后只有 `AGENTS.md`。
- 新增 `AGENTS.md` 受控措辞扫描：无命中。
- Markdown 二级标题序列：`1` 至 `12` 连续。
- 敏感模式扫描：无 private key、token、数据库凭证或签名 URL 命中。
- `.trellis/guru-team/scripts/bash/check-commit-messages.sh --json --task ...`：exit 0；验证 1 个 work commit，subject/body 合同通过，使用 `Refs #109`，没有错误 close keyword。

## Docs SSOT、影响与安全判断

- Docs SSOT：根 `AGENTS.md` 是本次仓库级 Skill-first 原则的 durable SSOT；task artifact 仅保留规划与审计证据。四份引用 spec 未修改，和新增原则不存在正文冲突或重复实现路径。
- 开箱即用与 upgrade/update：本分支未修改 workflow、preset、marketplace、overlay、installer、skill、script、schema 或平台副本，因此 throwaway 安装、overlay drift、upgrade/update 重放不适用于本次业务变更；分支也未声称已完成这些验证。
- 部署与运行：无 runtime、配置、schema、CI/CD、容器、Kubernetes、数据库 migration、Makefile 或部署影响。
- 安全：业务 diff 是规范文档；未新增 secret、客户数据、本机绝对路径到公共 package，未引入网络或权限行为。

## 观察项与后续

- #120 应继续保持 OPEN，并由独立 Trellis task 承接 canonical package、distribution、managed hash、structure validator 与 throwaway 验收；本分支不得关闭或声称交付 #120。
- `research/commit-message-loop-analysis.md` 可保留为 task history；其 `guru-create-work-commit` 提案需要另行确认和建 issue，不能并入 #109 或 #120 的已交付范围。

## 最终结论

**FAIL**：`AGENTS.md` 正文和 commit message 本身满足 #109，但 Phase 2 finding lifecycle / checker attribution 存在 1 个 P2。修复并由适格 closure reviewer 复核前，不得记录 Branch Review Gate PASS，不得进入 PR readiness 或 issue close。
