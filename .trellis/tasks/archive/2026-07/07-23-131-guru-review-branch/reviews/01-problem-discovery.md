# Issue #131 Branch Review 问题发现原始报告

## 审查身份与固定范围

- 审查角色：`问题发现审查代理`
- 审查模式：Branch Review；只读审查完整 committed diff，不修复实现、不写 gate artifact
- Task：`.trellis/tasks/07-23-131-guru-review-branch`
- 需求来源：GitHub Issue `#131`
- Base：`origin/main`
- 审查 HEAD：`cdf0fa47d3d6f508851b9c0e91260276d9fde8f5`
- 完整 diff range：`origin/main...cdf0fa47d3d6f508851b9c0e91260276d9fde8f5`
- Merge base：`ea132e350c4b6861fc955f17e590651a46e890ab`
- Diff 规模：307 files changed，25755 insertions，933 deletions
- 预期 workspace：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/131-guru-review-branch`
- 实际 repo root：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/131-guru-review-branch`
- Source checkout：`/Users/wumengye/Documents/GoProjects/guru-trellis`，状态为空
- Task worktree 审查前已有允许的并行 metadata tail：
  `.trellis/tasks/07-23-131-guru-review-branch/agent-assignment.json`、
  `.trellis/tasks/07-23-131-guru-review-branch/task-commit-plans/001.json`
- Suspicious source artifacts：无
- Workspace boundary：`status=ok`

## 审查覆盖

本轮读取并对照了以下证据，而非只审查最近一次修订：

- Live Issue `#131` body/comments、官方 Trellis workflow 与 spec marketplace 文档；
- `prd.md`、`design.md`、`implement.md`、planning approval、implementation handoff、
  三轮 Phase 2 raw report、`phase2-check.json`、issue scope ledger 与 task commit plan；
- `.trellis/spec/workflow/`、`.trellis/spec/preset/`、仓库级 requirements；
- `guru-review-branch` package 的 `SKILL.md`、contract、interface、schemas、examples、
  evals、tests、wrapper；
- canonical workflow/preset/overlay、dogfood installed copy、Codex/Claude/Cursor
  platform copy；
- `guru_team_trellis.py` 的 entry precondition、semantic qualification、finding lifecycle、
  assignment/recovery 与 gate recorder/checker 路径；
- 完整 committed diff 中的文档、代码、schema、config、installer、tests 与 task artifacts；
- Docs SSOT、升级/安装漂移、部署/配置/安全影响。

Canonical、dogfood installed copy 与 platform corpus 均逐文件一致；workflow
canonical/dogfood 一致，未发现 `.new` / `.bak`。Registry 中
`guru-review-branch` 为 active，`guru-review-task-publication` 保持 planned。

## 候选资格化明细

| Candidate | Affected behavior | Scope / scenario class | Disposition | 结论 |
| --- | --- | --- | --- | --- |
| C-131-01 | finding owner 失败后的 replacement closure | PRD R6、durable recovery contract；`normal_required_behavior` | `qualified_finding` | P1 |
| C-131-02 | Branch Review entry 的 dirty metadata allowlist | PRD R3/AC3、Design 5.1；`normal_required_behavior` | `qualified_finding` | P2 |
| C-131-03 | current-scope 候选经 qualification 证明非缺陷后的互斥 disposition | PRD R5、Design 6.2、Branch Review Data Boundary；`normal_required_behavior` | `qualified_finding` | P2 |
| C-131-04 | 完整 committed diff 的 whitespace validation | Implement validation plan；`normal_required_behavior` | `qualified_finding` | P3 |
| C-131-05 | 当前未授权 push，不能验证 exact remote feature ref marketplace install | 当前 PR publication limitation | `followup_candidate` | 不阻塞本轮代码 finding；push 后必须复验 |
| C-131-06 | `guru-review-task-publication` 尚未 active | Issue `#116` / `#132` 的已声明后续范围 | `observation` | 不属于 Issue `#131` current acceptance |
| C-131-07 | hostile artifact/hash forgery、恶意绕过、TOCTOU、额外 crash consistency、跨 OS atomicity | Issue 与仓库合同明确排除；`out_of_scope` | `rejected_candidate` | 不进入 finding 或 required follow-up |
| C-131-08 | 将 semantic scope/severity/confirmation 判断下沉到 recorder/checker | 违反 Markdown 判断、脚本确定性执行边界；`out_of_scope` | `rejected_candidate` | 不建议实现 |

## P0-P3 Findings

### F-131-BR-01 — P1：合法 replacement closure 被新 finding lifecycle 拒绝

- Scenario class：`normal_required_behavior`
- Requirement / contract：
  - PRD R6 要求每个 finding owner 都有 fresh closure evidence；
  - `.trellis/spec/workflow/data-contracts.md:1393-1400` 明确允许原 owner
    failed/interrupted/stale 后，用 `replacement-started`、
    `reuse_decisions[].decision=replace` 与 closure round
    `reuse_decision=replace` 完成闭环。
- Affected path：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:12750-12763`
- Evidence：
  - 新 lifecycle 的 `replacement_closure` 只接受
    `reuse_decisions[].decision == "new-agent"`；
  - 同文件既有 replacement validator
    `finding_round_has_replacement_closure()` 明确接受
    `decision=replace` 与 closure round `reuse_decision=replace`，说明两个生产路径
    对同一 durable contract 解释不一致；
  - 既有 legacy regression
    `test_review_branch_accepts_replacement_closure_when_original_review_agent_failed`
    覆盖 `replace`，但没有穿过新 v2 semantic lifecycle。
- 正常路径复现：
  在隔离的 `finding-fix-passed` production eval fixture 中，保留已 resolved 的
  `F-001`、合法 closure report digest 与 exact round/head，仅把原 same-agent closure
  改为 durable contract 定义的 replacement closure：
  closure agent 改为新替代 agent、round `reuse_decision=replace`、
  `reuse_decisions[].decision=replace`。直接执行真实
  `review_branch_finding_lifecycle_errors()` 返回：

  ```text
  resolved finding F-001 closure round lacks same-agent continuity or replacement linkage.
  resolved finding F-001 has no current bound closure_evidence.
  ```

- Impact：
  一旦 finding owner 客观失败、中断或 stale 且无法继续，合同要求的恢复闭环不能被
  v2 gate 接受；该正常恢复路径会永久阻塞 fresh final review 与 `passed`。
- 建议修复：
  让新 lifecycle 复用/等价实现既有完整 replacement-chain validator，接受经 assignment
  liveness/recovery 校验的 `decision=replace` 链；补充 semantic recorder、checker 与
  public wrapper 端到端 regression。

### F-131-BR-02 — P2：entry 把所有 task/runtime 路径误当作允许的 review metadata

- Scenario class：`normal_required_behavior`
- Requirement / contract：
  - PRD R3 / AC3 只允许 clean working tree 或 owner contract 白名单内的 task
    metadata tail；
  - `design.md:192` 进一步限定为 owner contract 列出的 **task-local review
    metadata**；
  - durable contract 不允许其它 task 或非 gate task artifact 被该例外覆盖。
- Affected path：
  - `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:703`
  - `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:12574-12590`
- Evidence：
  `METADATA_ONLY_PREFIXES = (".trellis/tasks/", ".trellis/.runtime/")`，entry
  precondition 仅以全局前缀判断 dirty path，没有绑定 current task，也没有校验
  owner-declared review metadata 名单。
- 正常路径复现：
  在隔离的 `workflow-passed` production eval owner repo 中，新增普通未跟踪文件
  `.trellis/tasks/unrelated/ordinary-note.md`。`git status` 明确出现
  `.trellis/tasks/unrelated/`，随后调用真实 installed wrapper：

  ```text
  .trellis/guru-team/skills/packages/guru-review-branch/scripts/invoke.sh \
    --input .trellis/.runtime/guru-team/evals/public-input.json \
    --owner-result .trellis/tasks/current/review-gate.json
  ```

  仍以 exit code 0 返回：

  ```json
  {"exit_id":"passed","task_ref":".trellis/tasks/current"}
  ```

- Impact：
  另一个正常 task 的普通 artifact、非 review gate task artifact 或任意 runtime tail
  都可绕过 Branch Review entry 的 dirty-state gate，使“working tree 仅含本轮允许
  metadata”的证据不真实。
- 建议修复：
  从 current task 与 owner contract 解析 exact allowlist，不再用全局
  `.trellis/tasks/` / `.trellis/.runtime/` 前缀替代；增加 unrelated task artifact、
  current task 非 gate artifact 与未声明 runtime artifact 的 blocked regression。

### F-131-BR-03 — P2：current-scope 非缺陷候选无法记录为 `rejected_candidate`

- Scenario class：`normal_required_behavior`
- Requirement / contract：
  - PRD R5 要求每个 candidate 先绑定当前合同并完成 qualification；只有前三类
    **且确实违反**当前交付合同时才可分配 P0-P3；
  - Design 6.2 与 Branch Review Data Boundary 定义五个互斥 disposition，其中包括
    `rejected_candidate`；
  - durable contract 只禁止最后两个 scenario class 成为 P0-P3 finding，并未要求
    将 current-scope、经证据证明“没有违反合同”的候选伪装为 out-of-scope。
- Affected path：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:12910-12924`
- Evidence：
  semantic normalizer 对 `observation`、`followup_candidate` 与
  `rejected_candidate` 统一限制为
  `out_of_scope|unconfirmed_nonstandard_proposal`，因此前三个合法 current-scope
  scenario 只有 `qualified_finding` 可被 schema/runtime 接受。
- 正常路径复现：
  构造一个绑定 PRD R5、scenario 为 `normal_required_behavior`、经代码证据证明当前
  实现符合合同、无 severity/finding 字段的 `rejected_candidate`，执行真实
  `review_branch_semantic_payload(..., typed_exit="passed", reviewed_head=...)`，
  返回：

  ```text
  WorkflowError: rejected_candidate candidate-no-defect has an invalid scenario or finding fields.
  ```

- Impact：
  正常 reviewer false positive 无法被忠实记录。调用方只能丢弃 raw candidate、
  错误改成 `out_of_scope`，或错误升级为 finding，破坏 qualification evidence 的
  完整性与互斥 disposition 合同。
- 建议修复：
  允许前三个 scenario class 在 qualification 结论为“未违反合同”时使用
  `rejected_candidate`，同时继续禁止 severity/finding 字段；为每个 scenario class
  增加 true finding 与 disproved candidate 成对 regression。

### F-131-BR-04 — P3：完整 committed diff 未通过计划要求的 `git diff --check`

- Scenario class：`normal_required_behavior`
- Requirement / contract：
  `implement.md:275` 将 `git diff --check` 列为最终 validation 命令。
- Affected path：
  `.trellis/tasks/07-23-131-guru-review-branch/phase2-worker-report.md:200`
- Evidence：
  对固定完整 range 执行：

  ```text
  git diff --check origin/main...cdf0fa47d3d6f508851b9c0e91260276d9fde8f5
  ```

  返回 exit code 2：

  ```text
  .trellis/tasks/07-23-131-guru-review-branch/phase2-worker-report.md:200: new blank line at EOF.
  ```

  但同文件 `:168` 和 `:176` 声称该命令通过，
  `phase2-check.json` 也把它列入已通过证据。
- Impact：
  committed diff 与 Phase 2/implement validation evidence 不一致；虽不影响 runtime，
  但当前 HEAD 不能满足其声明的完整验证门禁。
- 建议修复：
  删除 EOF 多余空行，重新执行固定 range `git diff --check`，并刷新 Phase 2 与后续
  commit/review evidence。

## Observations / Follow-ups / Rejections

### 非阻塞观察

- 远端 exact feature-ref marketplace install/switch 验证需要先 push 当前分支；本轮无
  push 授权，因此没有把公开 `main` 结果冒充当前 HEAD 结果。该验证必须在 publication
  前按 exact remote branch/ref 完成。
- `guru-review-task-publication` 仍为 planned，符合当前将 PR publication 迁移留给
  Issue `#116` / `#132` 的范围合同，不是 Issue `#131` 缺口。
- 当前 diff 未触及 CI/CD、container、Kubernetes、database migration、Makefile 或业务
  deployment 资产。文件名中的
  `skills/migrations/production-minimal-handoff.json` 是 Skill public API migration
  manifest，不是数据库/部署 migration。
- 未在新增/修改文件名及差异扫描中发现 `.env`、private key 或常见 GitHub/AWS secret
  literal；未发现真实业务私有样本或本机绝对路径进入 public package。

### 明确拒绝

- 不把 hostile artifact/hash forgery、恶意 actor、流程蓄意绕过、TOCTOU、额外 fault
  injection、crash consistency 或跨 OS atomicity 作为 P0-P3、required follow-up 或
  自动修复依据；它们均被 live Issue 与仓库 `AGENTS.md` 明确排除。
- 不建议让 Python/shell recorder/checker判断 scope、scenario、severity、finding、
  expansion confirmation 或 route intent。它们应继续只校验 AI Gate 已形成的确定性
  payload；F-131-BR-03 的修复仅是让确定性 schema/runtime 能忠实承载合法 AI 判断。

## 验证命令与结果

| 验证 | 结果 |
| --- | --- |
| `python3 trellis/skills/guru-team/packages/guru-review-branch/tests/test_contract.py` | 8/8 通过 |
| `python3 trellis/skills/guru-team/tests/test_skill_packages.py` | 167/167 通过 |
| `python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` | 560 通过，13 skipped |
| Preset tests | 45/45 通过 |
| Upstream ownership tests | 6/6 通过 |
| Dogfood overlay drift | 通过；43 frozen，10 active skills，1 planned，48 managed assets |
| Source shared eval `workflow-passed` | 通过 |
| Source shared eval `finding-fix-passed` | 通过 |
| Canonical / installed / platform corpus parity | 逐文件一致 |
| Python compile | 通过；生成的临时 ignored bytecode 已清理 |
| JSON parse / Bash syntax | Phase 2 套件覆盖并通过 |
| `git diff --check origin/main...<HEAD>` | **失败**：见 F-131-BR-04 |
| 独立 `ruff` / `shellcheck` | 环境与仓库未提供统一命令，未运行 |
| 独立 `mypy` / `pyright` | 环境未安装，仓库无声明 type-check gate；不适用 |

现有测试全部通过但未捕获 F-131-BR-01 至 F-131-BR-03，说明测试覆盖不足以替代
完整合同审查。Lint 类 committed-diff 检查存在一项确认失败。

## Docs SSOT、部署与安全判断

- Docs strategy：`ssot_first`；durable docs、task artifacts、canonical/installed copies
  基本完成同步。
- 但 current-scope Docs SSOT 与 runtime 存在三处阻塞性不一致：
  - durable docs 接受 `decision=replace` recovery closure，runtime lifecycle 不接受；
  - Design 只允许 current task owner-declared review metadata，runtime 接受所有
    task/runtime 路径；
  - Design/Data Boundary 定义每个 candidate 的五种互斥 disposition，runtime 无法记录
    current-scope non-defect rejection。
- 因此当前 Docs SSOT 不能被判定为“与最终 runtime 完全一致”，也不能以文档已合并
  替代 finding 修复。
- 本 diff 没有直接 deployment/DB/CI/CD 变更；主要风险是 workflow gate 误放行、
  qualification evidence 失真与 replacement recovery 被永久阻断。

## 结论

- Qualified findings：4
  - P0：0
  - P1：1
  - P2：2
  - P3：1
- Scope proposals：0
- 非阻塞 observations / follow-ups：2
- 明确 rejections：2
- Typed exit 建议：`implementation_required`
- 当前报告不能支持 Branch Review Gate `passed`，不能作为最终 `review.md` 的放行结论。
- 修复后必须重新执行 `guru-check-task -> guru-create-task-commit ->
  guru-review-branch`，由 finding owner/合法 replacement 形成 closure evidence；
  全部 findings 关闭后再 dispatch 从未参与前序 rounds 的 fresh final reviewer，覆盖新的
  `origin/main...HEAD` 完整 diff。
