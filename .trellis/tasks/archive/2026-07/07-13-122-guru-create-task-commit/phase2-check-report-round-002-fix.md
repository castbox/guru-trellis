# #122 Round 2 C-01 修复阶段二独立检查报告

## 检查身份与边界

- 逻辑角色：`阶段二检查代理`。
- 技术身份：`trellis_check_122_round2_fix`。
- 显示名：`Check-Agent-122-Round2-Fix`。
- 唯一工作目录：
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/122-guru-create-task-commit`。
- `pwd`、`git rev-parse --show-toplevel` 与 task start context 解析出的
  `expected_workspace` 均等于上述 worktree。
- Source checkout：`/Users/wumengye/Documents/GoProjects/guru-trellis`，检查前后均
  clean，未发现 same-task suspicious artifact。
- Reviewed HEAD：`03e813c5af37dec98c2c77114bc877c774256074`。
- Base：`origin/main`，`6b9495a17dc953c7a54c105e39c23a786edcd8a7`。
- Branch：`feat/122-guru-create-task-commit`。
- 检查按 `trellis-start`、`trellis-before-dev`、`trellis-check`、`trellis-meta`
  合同执行；未运行 Phase 2 / Branch Review recorder 或 validator，未 commit、push、
  创建 PR、调用 finish-work 或关闭 issue。
- 未修改受保护的 Round 1/2 raw review、`review.md`、`review-gate.json`、
  `review-findings-*.json` 或 `agent-assignment.json`。

## 输入与 dirty path

检查输入包括：

- live GitHub issue `castbox/guru-trellis#122`，检查时为 `OPEN`；
- `prd.md`、`design.md`、`implement.md`、`implementation-handoff.md` 的 Round 1 / 2
  delta、planning approval 与 Issue Scope Ledger；
- 旧 `phase2-check.json`、初始 Phase 2 报告与 Round 1 finding-fix Phase 2 报告；
- `task-commit-plans/001.json` 与 `002.json`；
- Round 1 raw final report、Round 2 finding closure raw report、failed gate、finding
  artifacts 与 rollup；
- `.trellis/spec/docs/**`、`.trellis/spec/preset/**`、`.trellis/spec/workflow/**` 与
  `cross-layer-thinking-guide.md`；
- `origin/main...HEAD` 的 103 个 committed paths；
- HEAD 后检查开始时的 38 个 dirty/untracked paths；
- canonical workflow/package/runtime/schema/tests、preset installer、dogfood runtime、
  installed package 与 shared/Claude/Codex/Cursor copies；
- 2026-07-13 live Trellis 官方 `index.md`、`custom-workflow.md`、`custom-skills.md`、
  `custom-spec-template-marketplace.md`。

检查开始时 38 个 dirty paths 分组如下：

| 分组 | 数量 | 内容 |
| --- | ---: | --- |
| Round 2 C-01 canonical 与 durable SSOT | 8 | canonical package contract/schema/tests、canonical runtime/tests、cross-layer guide、companion/data contracts |
| dogfood/installed/platform managed copies | 17 | dogfood extension/runtime/package，以及 shared/Claude/Codex/Cursor 各 3 个 package copies |
| task history 与旧 recorder metadata | 5 | agent assignment、implementation handoff、旧 Phase 2 recorder、plans 001/002 |
| Round 1/2 Phase 2 与 review metadata | 8 | 旧 Phase 2 report/findings、两轮 findings、failed gate、rollup、两份 raw reports |

本报告写入后是第 39 个 dirty path。没有发现 task scope 外、无法分类或已 staged 的
路径。

## C-01 独立复核

Round 2 raw finding `C-01` 的结论：**已关闭**。

### Public schema

Canonical Draft 2020-12 schema 已从单一 mismatch conditional 收敛为
`failure_stage x head_changed` 状态矩阵：

| 状态 | HEAD / commit identity | tree evidence | 结论 |
| --- | --- | --- | --- |
| `pre-commit`，tree 未绑定 | HEAD 未变；无 parent/message/path identity | `null` | 合法 |
| `pre-commit`，tree 已绑定 | HEAD 未变；无 created identity | matching `actual_source=index` | 合法 |
| `commit`，HEAD 未变 | 无 created identity | required `actual_source=index` | 合法 |
| `commit`，HEAD 已变 | 有 message/path identity | required `actual_source=commit` | 合法 |
| `postcondition` | HEAD 已变且有 message/path identity | required `actual_source=commit` | 合法 |

Schema 独立拒绝：

- `pre-commit + mismatched tree + hook_mutation=false`；
- `commit + tree_evidence=null`；
- `postcondition + tree_evidence=null + head_changed=false`；
- unchanged-HEAD commit 使用 `actual_source=commit`；
- postcondition 使用 `actual_source=index`。

### Runtime cross-field validation

独立 tamper harness 在 mock
`skill_json_schema_validation_errors(...)=[]`、即绕过 public schema 的条件下执行。
12/12 个 tamper 均被 `task_commit_result_validation_errors()` 拒绝：

1. pre-commit mismatched tree / hook false；
2. commit null tree；
3. postcondition null tree / unchanged HEAD；
4. commit unchanged HEAD / wrong `actual_source`；
5. postcondition wrong `actual_source`；
6. pre-commit `commit_sha` / `pre_commit_head` / `head_changed` identity 矛盾；
7. postcondition commit/pre-head identity 矛盾；
8. duplicate tree path；
9. missing tree path；
10. path `matches` 与 blob/mode equality 矛盾；
11. aggregate tree `matches` 与 tree/path facts 矛盾；
12. postcondition mode evidence 与 path/tree/mutation flags 矛盾。

Runtime 的独立拒绝没有依赖 schema 返回值；schema 负责可表达的 shape/source
约束，runtime 负责 equality、唯一集合覆盖和 derived boolean。

### 合法状态矩阵

以下 6/6 状态同时通过 public schema 与 mock schema 后的 runtime：

- pre-commit tree `null`；
- pre-commit matching index tree；
- 无 mutation 的 failing hook；
- 修改 index 的 failing hook；
- matching commit tree 的 non-tree postcondition error；
- post-commit tree/path mutation。

真实 Git regression 还覆盖 benign exit-0 hook、same-path content/mode restage、
literal metacharacter/decoy、unmerged path、delete/rename、unexpected path 与旧计划重用。

## R / AC / Docs SSOT

| 范围 | 独立结论 |
| --- | --- |
| R1 / AC1 | `guru-create-work-commit` 继续为 reserved tombstone；`guru-create-task-commit` 为唯一 active replacement，extension public API 一致。 |
| R2 / AC2 / AC8 | canonical/dogfood workflow 各 1 个 mandatory invocation 与 3 个唯一 typed-exit consumer；finding-fix 必须重新走 Phase 2 与新 sequence。 |
| R3-R6 / AC3-AC6 | workflow/standalone preconditions 相同；candidate 绑定 task/ledger/planning/Phase 2/HEAD/full dirty snapshot；AI 独占 scope/message/review/confirmation 判断，executor 只 exact stage。 |
| R7-R8 / AC4-AC8 | candidate mode 复用唯一 `validate_commit_message()`；literal index/tree identity、raw message、parent/path/unrelated/hook/tree result evidence 与 C-01 完整状态矩阵均通过。 |
| R9 / AC9 | step-local SSOT 位于 canonical package `references/contract.md`；workflow/platform continue entries 只保留 invocation、re-entry 与 typed-exit route。 |
| R10 / AC10-AC11 | source/installed validators、managed-hash apply、all-platform distribution、full suite、clean throwaway、update/workflow/preset reapply 与 drift 均通过。 |
| AC12 | local clean throwaway 通过；remote exact feature-ref 因 branch 尚未 push 仍为 pending，当前不满足 publish。 |
| AC13 | `close_issues=[122]`；#92、#120 只在 `related_issues`；`followup_issues=[]`。 |
| AC14 | public assets 未发现 secret、private key、签名 URL、本机用户绝对路径或 workspace journal。 |

Docs strategy 为 `ssot_first`。Design 的 14 个 durable evidence paths 全部存在且都在
`origin/main` 到当前 working tree 的变更集合内。C-01 的 producer-state matrix 已先
进入 canonical package contract、`data-contracts.md`、`companion-scripts.md` 与
`cross-layer-thinking-guide.md`，再由 runtime/schema/tests 实现并同步五份 managed
copies。Raw review、临时 tamper payload、单次运行输出与 agent liveness 仍只属于 task
history，没有进入公共 package。

官方文档复核确认：workflow 行为属于 Markdown 控制面；skill 是可复用 workflow
module；外部 skill 需要分发到平台 skill root；spec marketplace 不携带 active task、
workspace 或平台 prompt。当前 canonical/workflow/package/preset/spec ownership 符合
这些边界，没有修改 Trellis upstream、全局 npm 或 `node_modules`。

## Commit plan 与旧 evidence

- `002.json` 的 current committed result 通过新 public schema 与 runtime；真实 commit
  `03e813c5` 的 parent、raw message digest、31 个 path set 与 tree/blob/mode evidence
  全部匹配。
- `001.json` 是 Round 1 tree evidence 引入前由旧 executor 写回的 legacy committed
  history。真实 commit `afcab193` 的 parent、raw message digest 与 102 个 path set
  仍完全匹配，但当时没有捕获 pre-hook expected tree；当前 schema 正确拒绝其缺失
  `tree_evidence`，检查过程没有事后伪造不可证明的证据。
- Candidate validator 对 001/002 均返回非零：两者都不是下一条 fresh planned
  candidate，pre-commit HEAD、Phase 2、snapshot、sequence 和 plan digest 均不可重用。
- 旧 `phase2-check.json` 绑定 `afcab193` 和 Round 1 checker，已因 HEAD、dirty set、
  handoff 与 specs 改变而 stale；本报告不复用或改写该 recorder，主会话必须基于本轮
  evidence 记录 fresh Phase 2。

`001.json` 的 legacy evidence 限制是历史事实而非当前 runtime/schema 缺陷：它证明
旧计划不可重用，也避免用事后推断冒充 hook 前证据。

## 验证命令与结果

| 检查 | 结果 |
| --- | --- |
| 独立 schema/runtime tamper harness | 6/6 合法状态通过；12/12 tamper 在 schema 被 mock 后仍被 runtime 拒绝。 |
| `TaskCommitCandidateExecutorTest` | 18 tests，7.177s，`OK`。 |
| canonical package standalone | 4 tests，0.103s，`OK`。 |
| package/runtime/preset full suite | 496 tests，125.437s，`OK`。 |
| clean throwaway verifier | exit 0；覆盖 init、discovery、initial/finding-fix commits、old-plan reject、update、workflow/preset reapply、source/installed validation、drift、closeout smoke、sidecar scan。 |
| canonical preset `--all-platforms` | 幂等；`updated_managed=[]`、`managed_backups=[]`，43 managed files，conflict/removal/sidecar 均为 0。 |
| source / installed package validators | passed；reserved=1、active=1、invoke=1、exits=3。 |
| canonical/dogfood/platform equality | 6 个 package roots 各 8 files 字节一致；canonical/dogfood runtime 与 workflow 字节一致。 |
| dogfood overlay drift | passed。 |
| planning/workspace/task/context | planning schema 1.2、workspace boundary、task validate、phase 2.2/3.4/3.5 parsing 全部通过。 |
| Bash/Python/JSON/diff | 相关 Bash `bash -n`、canonical/dogfood Python compile、changed JSON parse、`git diff --check` 全部通过。 |
| scope/security/deployment | close=122、related=92/120；public security scan passed；deployment asset changes=0。 |
| staged/source/sidecar | staged paths=0；source checkout clean；recursive `.new/.bak=0`。 |

Throwaway 使用脚本明确支持的 `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1`：验证公开
marketplace discovery 后覆盖当前本地 canonical 内容。它不是 remote exact feature-ref
证据。`feat/122-guru-create-task-commit` reviewed content push 后仍必须由
`trellis-finish-work` verifier 读取该 exact ref；成功前不得宣称 remote verifier 通过、
创建 ready PR 或关闭 #122。

## 安全、部署与升级

- Executor 不 push，不 amend/rebase/reset/force/stash；message temporary file 为
  `0600` 并在 `finally` 删除。
- 未修改 GitHub Actions、Dockerfile/Compose、Kubernetes/Kustomize、Helm、数据库
  migration、Makefile、应用 service、worker、queue 或 runtime config；无需应用部署、
  数据迁移或部署资产同步。
- 变更影响 Trellis workflow/preset/local Git executor 的安装与升级。Clean install、
  known-managed reapply、`trellis update --force`、workflow switch/reapply、preset
  reapply、manifest 与 sidecar 状态均已验证。
- Compatibility target 保持 Trellis CLI `0.6.5`；当前 `trellis --version` 为
  `0.6.5`。本任务不扩展到 npm 可见的 `0.6.6`。

## Findings 与结论

- Round 2 C-01：已关闭。
- 本轮新 finding：0。
- 开放 finding：`0`（P0=0、P1=0、P2=0、P3=0）。
- 结论：`pass`。主会话可基于本报告记录 fresh `phase2-check.json`，再创建新的
  sequence 和取得独立 commit 副作用授权；不得复用 sequence 001/002 或旧授权。
- 当前 HEAD 保持
  `03e813c5af37dec98c2c77114bc877c774256074`，未被检查过程修改。
- Final working tree：本报告写入后 39 个 dirty/untracked paths；staged paths 为空，
  source checkout clean，recursive sidecar 为 0。
- 未执行 commit、push、PR、finish-work、remote verifier 或 issue close。
