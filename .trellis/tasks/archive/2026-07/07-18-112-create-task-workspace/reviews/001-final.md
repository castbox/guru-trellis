# Branch Review Round 1 最终放行审查报告

## 审查身份

- 逻辑角色：`最终放行审查代理`
- Technical agent id：`/root/branch_review_112`
- Reuse decision：`new-agent`；本代理未参与 issue #112 implementation 或 Phase 2 check
- Primary issue：`#112`
- Base ref：`origin/main`
- Base SHA：`7036dc4ca92a376288564345c98f6c55d8dfe6b8`
- Reviewed HEAD：`26a284477a1c1c21760ff7f93409466ebda9100f`
- Diff range：`origin/main...HEAD`
- 完整分支范围：1 个 commit、121 files，`24377 insertions / 1393 deletions`
- 审查方式：只读独立语义审查；除本 raw report 外未修改实现、规划、Phase 2、assignment、rollup 或 gate artifact，未 stage、commit、push、创建 PR 或关闭 Issue
- 禁止命令遵守：未运行 `review-branch.sh`、`check-review-gate.sh`、`record-agent-assignment.sh` 或任何 `record-*` recorder

Workspace boundary 检查确认 expected workspace 与 actual repo root 均为 `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/112-create-task-workspace`，source checkout 干净，suspicious source artifacts 为空。审查开始与报告写入前 HEAD 均精确等于上述 Reviewed HEAD。

## 审查输入与范围

- 读取 task `prd.md`、`design.md`、`implement.md`、`check.jsonl` curated specs、schema 1.2 `planning-approval.json`、`phase2-check.json`、`issue-scope-ledger.json`、`task-start-context.json`、`agent-assignment.json` 与 task commit plan 001。
- Planning approval 来自 `explicit-post-planning-review`，`ambiguity_review` 与 fixed-scope scanner evidence 均通过；三份 planning artifact 的当前 SHA-256 与 approval 记录一致。
- 审查 `origin/main...HEAD` 完整 committed diff、commit tree 与 task commit result 的 121 条 path/tree evidence。
- 重点检查 canonical Skill/interface/contract/schema/example/wrappers/tests、shared runtime、workflow typed-exit chain、extension/registry、preset installer、throwaway verifier、durable requirements/spec/README 与全部 managed copies。
- Issue ledger 的 close scope 为 `#112/#99/#54`，related 为 `#98/#53`，follow-up 为 `#132`；ledger 本身与批准范围一致。

## Findings

`findings_count=2`

- `P0=0`
- `P1=0`
- `P2=2`
- `P3=0`

### P2-1：existing official identity 路径仍读取并使用 `.trellis/.developer`

- 文件：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:24018`
- 相关上游 helper：`.trellis/scripts/common/task_store.py:232`
- 冲突合同：`docs/requirements/guru-team-trellis-flow.md:330`、`docs/requirements/requirement-main.md:144`、`README.md:114`
- 问题：workspace executor 虽然向 official `task.py create` 显式传入 `--assignee <login>`，但 official helper 仍无条件执行 `creator = get_developer(repo_root) or assignee`。因此 target workspace 已正常存在 official `.trellis/.developer` 时，executor 会读取并使用其内容写入 `task.json.creator`。runtime 在 `24005/24008/24074/24075` 还会直接检查 source/target identity path 是否存在。
- 正常路径复现：在临时初始化仓库写入 official `.trellis/.developer` 的 `name=legacy-identity`，随后执行 executor 使用的同形命令 `python3 ./.trellis/scripts/task.py create ... --assignee explicit-login`。结果为 `task.json.assignee = explicit-login`，但 `task.json.creator = legacy-identity`。
- 影响：这不是恶意篡改、TOCTOU 或对抗性输入，而是官方 identity 已存在的受支持正常路径。实现违反 “task workspace executor 不读取 `.trellis/.developer`” 的 current durable contract，并使 #99/#54 的 no-developer-identity closure 证据不完整。现有 throwaway 只覆盖 source/target identity 缺失，未覆盖 executor 在 existing identity 下的 creator 漂移；result checker 也不校验 `creator`。
- 处理：Branch Review 模式不修改实现。必须由 implementation/Phase 2 修复 runtime 或收敛合同，并增加 existing identity executor 回归测试；修复后重新生成 fresh Phase 2 evidence。

### P2-2：待发布 extension version 的公开 Docs SSOT 与 manifest 不一致

- 文件：`README.md:428`、`trellis/workflows/guru-team/README.md:33`、`trellis/workflows/guru-team/README.md:58`、`trellis/presets/guru-team/README.md:303`
- 权威 manifest：`trellis/guru-team-extension.json:5`、`.trellis/guru-team/extension.json:5`
- 问题：本提交把 canonical 与 dogfood manifest 从 `0.6.5-guru.14` 递增为 `0.6.5-guru.15`，但 root/workflow/preset README 仍把待发布版本写成 `.14`，workflow README 同一版本段另写 `.13`。
- 影响：三份 README 均在批准的 `ssot_first` Docs SSOT Plan 与 Phase 2 checked paths 中，且 AC14 要求 manifest、README、durable specs 与安装副本一致。当前公开版本诊断和发布说明会向维护者给出互相冲突的版本事实，Phase 2 的 “Docs SSOT 已完成、无开放 finding” 结论不能支撑最终 diff。
- 处理：Branch Review 模式不修改 durable docs。必须同步三份 README 到 `.15`，检查所有 current version prose，再重跑 Docs SSOT、dogfood/install 与 Phase 2 验证。

## 需求、设计与实现一致性

- R1-R7、R9-R12 的 package 生命周期、semantic profile、prerequisite evidence、target authority、四个 typed exits、portable artifact、A/B merge 与分发结构未发现新的确定性缺陷。
- R8/AC8/AC13 的 identity 缺失路径通过，但 existing identity 路径存在 P2-1，不能据此关闭完整 no-developer 边界。
- AC14 的 canonical/installed package bytes 与 runtime/workflow copies 一致，但公开 README version prose 存在 P2-2，因此整体 AC14 未满足。
- AC16 的 issue scope ledger 正确；由于当前有开放 finding，`acceptance_evidence` 仍为空是合理状态，当前不得关闭 #112/#99/#54。
- AC17 未发现 malicious-input、threat model、stress concurrency、TOCTOU、lock 或其它明确排除范围被引入。

## Docs SSOT

- Plan strategy：`ssot_first`。
- Durable requirements、workflow/preset specs、root/workflow/preset README、task artifacts、runtime/schema/test 的大部分 active workspace 合同已经同步。
- P2-1 表明 durable no-read contract 与实际 official `task.py create` code path 不一致；P2-2 表明 public version prose 未随 `.15` manifest 合并。
- 因此当前 `ssot_first` merge checkpoint 未完全完成，`phase2-check.json` 中 “Docs SSOT 已覆盖且当前无开放 P0-P3” 的结论对 Reviewed HEAD 不充分。
- Task-history-only 内容继续保留在 task、assignment、Phase 2 与 commit evidence 中；本轮未发现应误合并进 public docs 的 task-history 内容。

## 验证结果

- Tests：独立重跑五模块 Python suite，`Ran 636 tests in 183.884s, OK`。
- Lint：`git diff --check` 通过；changed Bash wrappers/installer 的 `bash -n` 通过。
- TypeCheck：仓库未配置独立静态 type checker；changed Python runtime/verifier 的 `python3 -m py_compile` 通过。
- Source/installed Skill validators：通过。
- Upstream ownership：通过，43 条 frozen legacy overlays 不变。
- Dogfood overlay drift：通过。
- Task JSONL validation：通过。
- Throwaway install/update/reapply：Phase 2 与本轮复核证据均显示通过；canonical/installed/shared/Codex/Cursor/Claude copies 一致，sidecar 为空。
- A/B archive + merge fixture：A -> B 与 B -> A 均通过，tracked Guru metadata 交集为空。
- Worktree 最终状态：除既有 task-local `agent-assignment.json`、`task-commit-plans/001.json` 与本 raw report 外，无实现文件 dirty drift。

通过的自动化验证没有覆盖 P2-1 的 existing identity creator 路径，也不能替代 P2-2 的 Docs SSOT 语义判断。

## 安全与部署

- 完整 diff 未修改 CI/CD、Docker、Docker Compose、Kubernetes、Helm、数据库 migration 或 Makefile；无服务部署与数据库迁移影响。
- 高置信 added-line credential 扫描未发现 GitHub token、AWS key、private key、数据库凭据、签名 URL 或敏感原始数据。
- 当前变更的运行影响限于 Guru Team public Skill、shared runtime、workflow、preset、registry、文档与多平台安装副本。

## 观察项

- Reviewed draft issue creation 把 `body + "\n"` 写入 `gh issue create --body-file`，而 plan/result 使用无尾换行 draft body 计算 digest。当前缺少无副作用证据证明 GitHub API 是否保留该尾换行，因此本轮不把它升级为 finding；建议在修复轮加入 adapter-level exact-body fixture，确认 production 返回 body 与 reviewed digest 的规范化规则一致。
- Remote branch/tag marketplace verification 尚未执行。该验证应由 publish/finish gate 在真实 pushed ref 可用后完成，不是当前本地 Branch Review 的独立 finding。

## 后续候选

无。两项 finding 都属于 #112 当前范围，应在当前 implementation/Phase 2 闭环，不应外移为新 Issue。

## 证据交接

- 完整审查范围：`origin/main...26a284477a1c1c21760ff7f93409466ebda9100f`，1 commit，121 files。
- Findings：2 项 P2，分别阻塞 no-developer identity 合同与 Docs SSOT/version release 一致性。
- 部署影响：无 CI/CD、容器、Kubernetes/Helm、数据库 migration 或 Makefile 变更。
- 安全影响：未发现高置信 secret/credential 或敏感原始数据。
- Docs SSOT：`ssot_first` 未完成，durable contract/runtime 与 public version prose 均有 current-scope inconsistency。
- 本报告可作为 main session 汇总 `review.md` 的 fresh raw finding report；由于 findings 未关闭，不能支持通过 Branch Review Gate，也不能进入 publish/issue closeout。

## 结论

- Round 1 最终放行审查：`阻塞`
- Reviewed HEAD：`26a284477a1c1c21760ff7f93409466ebda9100f`
- Diff range：`origin/main...HEAD`
- Findings count：`2`（`P2=2`）
- 必须返回 implementation / Phase 2，关闭 P2-1 与 P2-2，并由 fresh reviewer 复核完整修复 diff 后才能重新申请最终放行。
