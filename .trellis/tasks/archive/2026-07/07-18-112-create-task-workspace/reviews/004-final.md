# Branch Review Round 4 最终放行审查报告

## 审查身份与 freshness

- 逻辑角色：`最终放行审查代理`
- Technical agent id：`final_review_112_r4`
- Reuse decision：`new-agent`；本代理未参与 issue #112 implementation、Phase 2 check 或 Round 1-3 finding/closure review
- Primary issue：`#112`
- Base ref：`origin/main`
- Base SHA：`7036dc4ca92a376288564345c98f6c55d8dfe6b8`
- Reviewed HEAD：`ed7c0786cc85f3bfd0378cd7433b37a5703c6425`
- Diff range：`origin/main...HEAD`
- 完整分支范围：3 个 commits、123 files，`25727 insertions / 1418 deletions`
- 审查方式：独立语义审查完整分支 diff；除本 raw report 外未修改实现、规划、Phase 2、assignment、rollup 或 gate artifact，未 stage、commit、push、创建 PR 或关闭 Issue
- 禁止命令遵守：未运行 `review-branch.sh`、`check-review-gate.sh`、`record-agent-assignment.sh` 或任何 `record-*` recorder

Workspace boundary 已确认 expected workspace 与 actual repo root 均为 `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/112-create-task-workspace`。报告写入前 source checkout 干净；task worktree 的 dirty paths 只有既有 task-local review/commit metadata tail。审查开始、测试完成与报告写入前 HEAD 均精确等于 Reviewed HEAD。

## 审查输入与范围

- 重读 live issues `#112/#99/#54/#98/#53/#132`，以 live `#112` 正文中的 created-issue recovery、mutation-time base freshness、no-developer、parallel merge、distribution 与 close scope 为权威边界。
- 读取完整 `prd.md`、`design.md`、`implement.md`、schema 1.2 planning approval、issue scope ledger、implementation/Phase 2 handoff、fresh `phase2-check.json`、task commit plans 001-003 与完整 commit/tree/path evidence。
- 读取 Round 1-3 raw reports、`review.md`、`review-gate.json` 与 `agent-assignment.json`；确认 Round 1 两项 P2 经 Round 2/3 closure chain 关闭，Round 4 使用未出现过的 fresh final reviewer identity。
- 审查 canonical package/interface/contract/schema/example/wrappers/tests、shared production runtime、workflow typed-exit chain、durable requirements/spec/README、preset/installer/throwaway verifier、extension manifest、dogfood 与 Agents/Codex/Cursor/Claude managed copies。
- 覆盖 `origin/main...ed7c0786` 的完整 3-commit diff，而非只审查最后一个 docs finding-fix commit。

## Findings

`findings_count=2`

- `P0=0`
- `P1=1`
- `P2=1`
- `P3=0`

### P1-1：created issue 在 live reread 失败后的重试会再次创建等价 Issue

- 文件：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:3194`、`:23675`、`:24198`
- Schema/validation：`trellis/skills/guru-team/packages/guru-create-task-workspace/schemas/task-workspace-plan.schema.json:78`、`:159`；`guru_team_trellis.py:23377`
- 冲突合同：live `#112` “Created issue authority 与正常失败恢复”、PRD R4/AC5、design 7.2、package contract “Exact execution and recovery”。
- 问题：`create_issue()` 先成功执行远端 `gh issue create`，随后才调用 `issue_view()`。若远端创建已成功但该立即重读因普通 GitHub/API/连接错误失败，函数在形成 `created_issue_binding` 和 checker-passed `refresh_review` result 前抛错。相同 confirmed reviewed-draft plan 仍是 current；直接重试会再次进入 `create_issue()`，没有 one-use confirmation、pre-create live duplicate/current-state recovery guard，或可供 executor 查找的已创建 binding。
- Binding 重入也未完成：reviewed-draft schema 强制 `created_issue_binding_sha256=null`；existing-issue schema 只把该字段定义为 nullable SHA。Existing-issue semantic validation 只核对 readiness target 的 repo/number/url/update/content，没有把非空 SHA 与先前 checker-passed created binding、reviewed draft id/digest 或 creation confirmation digest 做确定性关联。因此字段存在时只能作为未验证标记，不能证明“复用同一 created issue”。
- 正常路径复现：focused no-repo-write diagnostic 模拟两次调用；第一次 `gh issue create` 返回 issue `#500` 后立即 live reread失败，第二次直接重试创建 `#501` 并返回 `refresh_review`。观测值为 `remote_created_issue_numbers=[500, 501]`、`second_exit=refresh_review`。
- 影响：这是 live `#112` 明确要求覆盖的普通 post-create failure/session interruption recovery，不依赖恶意输入、伪造 artifact、竞态压力或额外 fault model。它可在用户已确认的正常调用中制造不可自动回滚的重复远端 Issue，违反“不得再次创建等价 issue”和 AC5 “reviewed draft 路径只创建一次 issue”。
- 处理：返回 implementation / full Phase 2。需要让任何后续调用在创建前通过 checker-passed binding 或 live duplicate/current-state evidence识别已创建 Issue，并确定性绑定 reviewed draft/confirmation；补充“remote create succeeded + immediate reread failed + retry”的 production-path regression，以及 existing-issue binding identity 正负用例。

### P2-1：workspace mutation boundary 未重新 fetch/sync，可能从过期 base 创建任务分支

- 文件：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:3652`、`:23142`、`:23856`、`:24150`
- 冲突合同：live `#112` 创建闭环第 10 步“Executor重新运行base sync/freshness”、PRD R6、design 10、package contract 74-83 行、`trellis/workflows/guru-team/README.md:494`。
- 问题：executor 的 mutation-boundary guard 调用 `validate_live_base_sync_result()`，它只把先前 `guru-sync-base` result 与当前 checkout、local base ref、local remote-tracking ref 比较。该路径没有调用 `git fetch`、`execute_base_sync()` 或等价 shared sync core；因此在 initial Intake sync 后远端 base 正常前进、但本地 `refs/remotes/<remote>/<base>` 尚未更新时，旧 result 与三个本地值仍相等，guard 会接受旧 HEAD。
- `task_workspace_require_execution_boundary()` 在 branch/worktree/task/artifact/runtime mutation 前重复调用相同的旧-result validator，这能检测本地漂移，却不能把 mutation 时刻与 live remote authority 重新同步。README 对外宣称该 executor “在 GitHub 或 worktree/task mutation boundary 重跑 shared core”，与实际 call path 不一致。
- 影响：人类确认和完整 Intake chain 之间远端 base 正常合入新提交是受支持的常见外部状态变化，不是 TOCTOU/并发压力扩张。当前实现可能从过期 `main` 创建 branch/worktree/task，漏掉刚合入的 prerequisite/fix，并把 `base_freshness.status=fresh` 写入 task context。
- 处理：返回 implementation / full Phase 2。Mutation owner 应在首个 GitHub 或 workspace/task 副作用前重新执行 shared base resolver/sync/freshness，并把 fresh post-sync identity 绑定到 plan 或触发 `refresh_review`；测试需让真实 remote ref 在 initial evidence 后前进，同时保持本地 remote-tracking ref未刷新，证明 mutation 前会 fetch/sync 或 fail closed。

## Round 1-4 问题生命周期

| 来源 | Finding | 当前状态 |
| --- | --- | --- |
| Round 1 P2-1 | existing `.trellis/.developer` 污染 `task.json.creator` | `closed`；isolated official handler adapter、creator/assignee 与 identity-preservation tests current |
| Round 1 P2-2 | `.15` manifest 与 public README `.14/.13` 漂移 | `closed`；Round 3 public version regression 与 live README current |
| Round 1 observation | issue body adapter 尾换行风险 | `closed observation`；exact reviewed body bytes regression current |
| Round 4 P1-1 | post-create reread failure retry duplicate Issue | `open` |
| Round 4 P2-1 | mutation boundary 未重新 fetch/sync base | `open` |

Round 1-3 closure chain本身有效，但 closure-before-final 不表示完整 diff 不再可能出现此前 reviewer 未发现的新问题。Round 4 的两项 finding 均来自完整 runtime/schema/recovery call-path审查，属于当前 scope，必须形成新的 finding owner/closure chain；当前 fresh final reviewer不能给出 pass。

## 需求、设计与实现一致性

- Package 生命周期、semantic profile、五个 prerequisite ids、target/disposition owner、互斥 confirmation、四个 typed exits、assignee/no-developer adapter、四类 portable artifacts、runtime mapping、A/B merge 与 distribution结构未发现其它新缺陷。
- R4/AC5 未满足：created issue result 的成功路径能形成 live binding，但失败后重试与后续 existing-issue binding authority没有闭环。
- R6 的“每个 mutation 边界重验 base”在实现中只覆盖本地 snapshot consistency，没有承接 issue/README 明确要求的 shared base sync/freshness rerun。
- AC16 ledger 仍正确把 close scope限定为 `#112/#99/#54`，related 为 `#98/#53`、follow-up 为 `#132`；由于当前存在 open findings，不得关闭任何 close issue。
- 未发现 malicious actor、hostile input、故意伪造、lock/atomic、并发压力、cross-OS 或其它明确排除范围被引入。

## Docs SSOT

- Plan strategy：`ssot_first`。
- Public version、stable tag、no-developer、exact-body、workflow/preset/package distribution 与 Round 1-3 修复当前一致。
- Durable issue/PRD/design/package contract/README 都要求 ordinary created-issue recovery 和 mutation-time fresh base；production runtime 与 schema未完整实现这两项。因此 current-scope Docs SSOT 与代码行为存在两处阻塞性不一致，`ssot_first` merge checkpoint不能视为完成。
- Task-history-only 的旧 finding、failed gate、handoff 和 commit evidence保持历史真实；本轮没有要求追溯改写历史 artifact。

## 验证结果

- Fresh full Python suite：`Ran 639 tests in 184.308s`，`OK`。
- Source package validator：通过。
- Installed package validator：通过；303 managed files，sidecar/conflict/removal 均为 0。
- Upstream ownership：通过；43 条 frozen legacy overlays 未变化。
- Dogfood overlay drift、canonical/installed runtime parity、workflow parity、`git diff --check origin/main...HEAD`：通过。
- Phase 2/closure evidence 的 clean throwaway install/update/reapply、existing/no-identity、A -> B / B -> A merge、platform copies 与 sidecar=0 仍与 Reviewed HEAD 的相关 bytes 匹配。
- Source checkout 最终复查干净；worktree 无 non-metadata dirty drift。

通过的 639 tests 没有覆盖“远端 issue 已创建但首次 live reread失败后的重试”，也没有覆盖“initial base evidence 后 remote 前进且 local remote-tracking ref仍旧”的 mutation-time场景；自动化通过不能替代上述明确 acceptance call path。

## 安全与部署

- 完整 diff 未修改 CI/CD、Docker、Docker Compose、Kubernetes、Helm、数据库 migration 或 Makefile；无服务部署、配置发布或数据库迁移影响。
- 高置信 added-line credential 扫描未发现 GitHub token、AWS key、private key、数据库凭据、签名 URL 或敏感原始数据。
- 当前运行影响限于 Guru Team public Skill、shared companion runtime、workflow、preset、registry、文档与多平台安装副本。
- P1-1 涉及远端 GitHub Issue 重复副作用，因此在修复和 fresh review前不得进入 publish/issue closeout。

## 观察项

- Remote branch/tag marketplace verification 尚未执行，仍应由 publish/finish gate 在真实 pushed ref 可用后完成；它不是本轮 finding。
- 当前 `review.md` 与 `review-gate.json` 仍是 earlier-round rollup/gate metadata；main session 应在消费本 raw report 后重新汇总并记录 blocking gate，本代理未修改它们。

## 后续候选

无。两项 finding 都是 #112 当前明确 acceptance，不应降级为 observation 或外移到新 Issue。

## 证据交接

- Reviewed HEAD：`ed7c0786cc85f3bfd0378cd7433b37a5703c6425`
- 完整 diff：`origin/main...ed7c0786cc85f3bfd0378cd7433b37a5703c6425`，3 commits、123 files。
- Round 1-3 closure：有效；原两项 P2 与 exact-body observation 已关闭。
- Round 4 findings：`P1=1`、`P2=1`，均为 current-scope open finding。
- Tests/validators：fresh 639 suite OK；source/installed/303/43/dogfood/parity/diff-check 通过。
- Docs SSOT：created-issue recovery 与 mutation-time base freshness 的 durable contract未被 runtime/schema完整承接。
- 部署影响：无 CI/CD、container、Kubernetes/Helm、database migration 或 Makefile 变更。
- 安全影响：未发现 secret/credential；存在未闭环的重复远端 Issue 副作用风险。

## 结论

- Round 4 最终放行审查：`阻塞`
- Findings count：`2`（`P1=1`、`P2=1`）
- 当前 Branch Review Gate 不得通过，不得进入 `trellis-finish-work`、push、PR 或 Issue closeout。
- 必须返回 implementation 与完整 Phase 2，修复两项 finding并生成 fresh commit 后，由 finding owner/closure reviewer按当前 HEAD完成闭环，再派发新的 fresh final reviewer。
