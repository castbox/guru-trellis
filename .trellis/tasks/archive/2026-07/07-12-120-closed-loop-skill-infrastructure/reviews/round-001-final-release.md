# #120 Branch Review 第 1 轮最终放行审查原始报告

## 审查身份与结论

- 审查角色：独立 `最终放行审查代理`
- 审查轮次：`round-001`
- 结论：`blocked`
- 问题数量：`2`（P0=`0`，P1=`1`，P2=`1`，P3=`0`）
- 门禁判断：当前报告不能作为 Branch Review Gate 的 final pass evidence；两个 finding 均须回到 Phase 2 修复并由新的完整 Branch Review 复验。

## 审查绑定

- GitHub issue：`castbox/guru-trellis#120`，live 状态为 `OPEN`
- 工作树：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/120-closed-loop-skill-infrastructure`
- 基线：`origin/main`
- 合并基点：`f14f167294154abffc0ef6124e0428911350b25b`
- 审查范围：`origin/main...HEAD`
- 审查 HEAD：`ea5d5e46686348b3006b9678eab7edfe735c31b3`
- 变更规模：54 files，6114 insertions，47 deletions
- 提交：`feat(trellis): #120 建立闭环 Skill Canonical 分发基础设施`；正文使用中文事实段落与 `Refs #120`，未使用 close keyword，符合当前 work commit 合同。
- 工作区边界：`pwd`、Git toplevel 和 `git worktree list` 均绑定上述 task worktree；既有未提交改动仅为主会话维护的 `agent-assignment.json` liveness 状态，不计入 reviewed committed diff，也未被本代理修改。

## 问题清单

### P0

无。

### P1-1：Source validator 会放行不可发现且没有可验证测试证据的 active package

- 位置：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:10248`、`:10379`；`trellis/skills/guru-team/schemas/skill-interface.schema.json:42`
- 合同：issue #120 R1/R2 要求 active package 具有 stable `name` / `description`、完整 `SKILL.md` 入口和 tests；AC4 要求缺失 active package 必需合同时 `source` mode fail closed。`.trellis/spec/workflow/skill-package-contract.md` 也把可发现 `SKILL.md` 与 tests 列为 active interface 合同。
- 事实：`validate_skill_interface()` 对 `SKILL.md` 只做 regular-file 存在性检查，不解析 frontmatter，也不校验 `name` / `description` 与 registry/interface 一致；`tests[]` 只验证为非空字符串，未绑定可定位、存在或可执行的测试证据。
- 独立复现：复制 `representative-active` fixture 到临时目录后，分别把 `SKILL.md` 清空，以及把 `tests` 改为 `["does-not-exist-anywhere"]`；两次 `validate_skill_source(...)` 均返回 `status=passed, errors=[]`。
- 影响：后续 issue 可以把缺失 discovery frontmatter 或没有真实测试的 package 激活并由 preset 分发，平台无法按 stable id 发现，且 deterministic structure gate 仍错误通过。这破坏了本任务要一次固定的 active lifecycle 公共基础设施，不能推迟到首个业务 skill 修补。
- 修复要求：为 `SKILL.md` 定义并校验机器可判定的 frontmatter contract，至少将 `name`/stable id 与非空 `description` 绑定 registry/interface；把 `tests` 改为可机器绑定的测试证据合同并验证其真实存在/归属，或提供等价的 registry-backed test inventory；补充空/缺 frontmatter、identity drift、虚构/缺失 tests 的 fail-closed 回归。
- 状态：`unresolved`。

### P2-1：Phase 2 evidence 没有记录 workflow 强制要求的 Docs SSOT implementation handoff 与复核结果

- 位置：`.trellis/tasks/07-12-120-closed-loop-skill-infrastructure/agent-assignment.json:193`、`.trellis/tasks/07-12-120-closed-loop-skill-infrastructure/phase2-check.json:60`、`:131`
- 合同：`trellis/workflows/guru-team/workflow.md:973`、`:1016`、`:1039` 和 `.codex/agents/trellis-check.toml:52` 要求 implementation handoff 明确记录 plan strategy、docs sync、task delta merge、task-history-only、follow-up/no-update 边界及 durable-docs/task-delta 输入，并要求 Phase 2 check 对这些逐项复核。Branch Review 遇到缺失或不完整 Phase 2 evidence 必须作为 finding，不得凭命令通过补推语义。
- 事实：实现代理的 committed completion/liveness 记录只说明“完成全范围实现”或“首轮 durable docs 已写入”，`handoff_summary` 为空；`phase2-check.json` 只有泛化 `check_summary`、`coverage.docs_ssot=true` 和命令结果，没有记录 `ssot_first` 的 docs sync result、task delta merge、task-history-only 内容或 durable-docs 作为 primary input 的实际证据。
- 影响：虽然本轮人工 diff 审查确认 durable requirements/spec/README 与实现大体同步，但 Branch Review Gate 无法从 Phase 2 artifact 证明实现/check 当时按批准的 `ssot_first` 计划消费并复核这些输入；空白布尔断言不能替代关键 gate 的可审计 evidence。
- 修复要求：回到 Phase 2，由实现/check owner 对当前 scope 补全真实 handoff 与 check evidence，逐项记录 `ssot_first`、已更新 durable docs、合并的 task delta、仅保留为 task history 的内容、follow-up/current PR limitation、durable-docs 与 task-delta 输入来源；不得由 recorder 默认值或本 Branch Review 代写语义结论。随后重录 fresh Phase 2 evidence 并重新提交。
- 状态：`unresolved`。

### P3

无。

## 实际审查证据

- 读取 live issue #120、根 `AGENTS.md`、官方 Trellis live docs（index、custom workflow、custom skills、custom spec marketplace）、task `prd.md` / `design.md` / `implement.md`、planning approval、Phase 2 check/findings/recovery liveness、issue scope ledger 和全部 curated specs。
- 审查完整 `origin/main...HEAD` 54 文件 diff，重点逐段读取 canonical/dogfood Python runtime、preset installer、registry/interface schemas、marker parser、installed manifest inventory、path/symlink containment、platform shrink/removal、sidecar、fixture 与 tests。
- 规划 approval schema 1.2、`explicit-post-planning-review`、ambiguity review、固定扫描零 unchecked hit 均有记录，三份规划文档当前 SHA-256 与 approval 绑定一致。
- Phase 2 历史 2 个 P1 和 1 个 P2 均标记 resolved；本轮重新核对 symlink containment、schema evaluator/inventory、platform shrink 与对应 tests，未重新打开这三项旧 finding。
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`、`.trellis/guru-team/scripts/python/guru_team_trellis.py` 逐字节一致；canonical/dogfood workflow 和 wrapper 逐字节一致；canonical/installed registry 与 schema 一致；production registry 只有 `guru-create-work-commit` reserved，fixture 没有进入 production platform copy。
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest` 直接执行 skill、preset、companion 三组 suite：468/468 通过。
- `python3 -m py_compile`、相关 `bash -n`、changed JSON `jq empty`、`git diff --check origin/main...HEAD` 通过；测试生成的 `__pycache__` 已清理。
- 未运行任何 Guru Team recorder/validator extension script，包括 `review-branch.sh`、`check-review-gate.sh`、`record-*`、`check-skill-packages.sh`、dogfood/throwaway wrapper；这是本轮明确边界。Phase 2 已记录 local throwaway/dogfood/source-installed 结果，本轮以真实代码、tests 和独立负向复现审查其充分性。

## Docs SSOT

- 批准策略：`ssot_first`，`docs_state=partial_docs`。
- Durable docs 落点齐全：`docs/requirements/**`、`.trellis/spec/workflow/skill-package-contract.md` 及 workflow/preset/docs specs、根/workflow/preset README 已覆盖 canonical root、registry lifecycle、marker、managed hash、platform distribution、update/reapply 和公共 API。
- Docs 与当前代码大体一致，未发现第二套 canonical root 或 production fixture 泄漏。
- 但 Phase 2 的 implementation/check artifact 未留下上述策略消费和 reconciliation 的具体证据，构成 P2-1；Branch Review 不替 Phase 2 首次补录。

## 安全与部署影响

- 安全：本 diff 扩大了 preset 对 `.trellis/guru-team/skills/` 和所选 platform roots 的文件写入/删除面。已审查 lexical containment、逐组件 `lstat`、target/ancestor symlink、unknown edit preserve + `.new`、known upgrade + `.bak` 与 installed inventory；旧 symlink finding 的修复和回归存在。changed public assets 未发现 secret、private key、credential URL、`.env` 值、客户数据或签名 URL。
- 部署：无 Docker、K8s、数据库 migration、Makefile 或服务运行时部署变更；有 extension version `0.6.5-guru.4`、preset installer、schema、wrapper、platform skill discovery 和 installed manifest 行为变化，属于发布/安装资产影响。
- Stable/canary：public docs 仍将 `v0.6.5-guru.2` 标为 stable；当前 `.4` 在 merge/tag/远端验证完成前明确不是 stable source，未发现提前宣称 stable。

## Issue Close Scope 与延期边界

- `issue-scope-ledger.json` 仅有 primary/close issue #120，`related_issues=[]`、`followup_issues=[]`；commit 仅 `Refs #120`，未越界关闭具体 business skill 或其它 issue。
- `acceptance_evidence` 当前为空，符合 ledger 中“publish 前补齐”的 pending 语义；在本轮 findings 关闭且 finish-work 完成前不得关闭 #120。
- 远端 exact feature-ref marketplace verification 尚未执行。该步骤必须在 reviewed content push 后由 finish-work verifier 对精确 remote branch/ref 和 HEAD 执行，并写入 `marketplace-verification.json`/ledger；本轮禁止 push，因此 local throwaway、`#main`/unpinned canary 抽样或 Phase 2 命令记录都不能替代它。

## 观察项与后续候选

- 观察项：marker parser 当前只识别三反引号 fence；若未来 contract 允许 `~~~` 或 indented code examples，需要明确语法或扩展 parser/tests。本项未证明当前 production workflow 失效，不单独计 finding。
- 后续候选：P1-1 修复时应选择稳定 tests evidence 模型，避免仅把任意字符串换成另一个不可验证标签。

## 最终结论

完整 committed diff 存在 2 个未解决问题。当前 round 1 为阻塞证据，不是 final pass evidence；禁止进入 Branch Review Gate pass、finish-work、push、PR 或 issue close。
