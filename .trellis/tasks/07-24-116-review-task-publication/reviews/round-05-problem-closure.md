# #116 Branch Review 第 5 轮问题闭环审查原始报告

## 审查身份与结论

- 审查角色：`问题闭环审查代理`
- 审查代理：`/root/issue116_branch_review_final_round4`
- 审查轮次：`round-05`
- 复用决定：`reuse-for-closure`
- 连续性依据：本代理在 Round 4 独立发现并拥有 `BR116-R04-P1-01`；`agent-assignment.json` 已记录 Round 4 → Round 5 的 finding-owner closure 复用。
- 闭环结论：`closure_passed`
- findings_count：`0`（P0=`0`，P1=`0`，P2=`0`，P3=`0`）
- Finding 状态：`BR116-R04-P1-01=closed`
- 身份边界：本报告只证明 Round 4 finding 在当前 HEAD 上闭环，不是 fresh final-release review，不能支持最终放行。下一轮必须由未参与该 finding discovery、implementation 或 closure 的另一全新技术身份审查完整 diff。

## 审查绑定与工作区证据

- GitHub repository：`castbox/guru-trellis`
- Live issue：`#116`，状态仍为 `OPEN`；已重新读取 issue 正文与 accepted-current comment `5045033833`，authority 未漂移。
- 工作树：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/116-review-task-publication`
- 基线：`origin/main@bdc8f50bcd1e325aed331d4b01107b83ed8ee940`
- 审查 HEAD：`d7ab98f5c53f470f4d3f3742f8cfca24f8465edd`
- 完整差异：`bdc8f50bcd1e325aed331d4b01107b83ed8ee940...d7ab98f5c53f470f4d3f3742f8cfca24f8465edd`
- Merge base：`bdc8f50bcd1e325aed331d4b01107b83ed8ee940`
- 差异规模：345 files、49,069 insertions、594 deletions、3 commits。
- 完整提交序列：
  - `aacb6e02e5386578bfe3d046511a0002a51cb581 feat(workflow): #116 实现 task publication 审查闭环`
  - `1dd2ef8af1cf583eeaf302a11c4770a07922b0b2 fix(workflow): #116 收紧 publication 状态校验`
  - `d7ab98f5c53f470f4d3f3742f8cfca24f8465edd fix(workflow): #116 修复 publication 六布局命令入口`
- Finding-fix commit：35 files、4,630 insertions、263 deletions；parent 为 `1dd2ef8af1cf583eeaf302a11c4770a07922b0b2`，tree 为 `f688b1c9e62ee4b8117de40eb1e019f40fa716b6`。
- `task-commit-plans/003.json` 为 `status=committed`、`exit=committed`，绑定上述 commit、parent、35 个 exact committed paths；expected/actual tree 与每个 blob/mode 全部匹配，`unrelated_preserved=true`、`hook_mutation=false`。
- 审查开始与报告写入前，`check-workspace-boundary.sh --json --task .trellis/tasks/07-24-116-review-task-publication` 均返回 `status=ok`：expected workspace 等于 actual repo root，source checkout 为空状态，`suspicious_source_artifacts=[]`。
- 报告写入前 worktree tail 只有主会话维护的 `agent-assignment.json` 与 `task-commit-plans/003.json`；本代理未编辑这些文件，也未将它们当作 implementation diff。

## 已读取的审查证据

本轮重新读取并交叉核对：

1. `AGENTS.md`、`guru-review-branch/SKILL.md` 与完整 `references/contract.md`；
2. live Issue #116 与 accepted-current comment；
3. `check.jsonl` 的 8 个 curated spec：
   - `.trellis/spec/workflow/quality-guidelines.md`
   - `.trellis/spec/workflow/skill-package-contract.md`
   - `.trellis/spec/workflow/workflow-contract.md`
   - `.trellis/spec/workflow/data-contracts.md`
   - `.trellis/spec/workflow/companion-scripts.md`
   - `.trellis/spec/preset/installer.md`
   - `.trellis/spec/preset/upstream-ownership.md`
   - `.trellis/spec/docs/public-docs.md`
4. current `prd.md`、`design.md`、`implement.md` 与 `planning-approval.json`；
5. `implementation-handoff.md` 第 11/12 节、`phase2-check.json`、Round 8/9 Phase 2 raw reports；
6. Round 4 raw report、issue scope ledger、commit plan 003 与 assignment/reuse/liveness lifecycle；
7. 完整 345-file committed diff，以及 finding-fix commit 的 35 个文件、六布局 package copies、preset assets、throwaway verifier 与 regression tests。

Planning 三件套 current SHA-256 与 approval 记录完全匹配：

- `prd.md`：`9814f640a7a624740b7f0cb06dc6e9b010e428ed523a5bd70345ba2b8ab7de01`
- `design.md`：`b2a38854623d55558807732a72bd586cfa60e38aafe22a0fb1b80a1168d2a408`
- `implement.md`：`13f7ec2d8fa925a803b37c662cd796fd47a62b0a574b8f2ca96b031099520603`

Planning approval 为 schema `2.0`、`typed_exit=approved`，保有 passed ambiguity review、fixed-scope scanner 零未检查 normative hit、`explicit-post-planning-review` 与匹配的规划文档 digest。

## `BR116-R04-P1-01` 闭环复核

### 原 finding

Round 4 在受支持的普通安装路径确认：

- publication recorder/checker 只会剥离 canonical source suffix；
- installed shared、`.agents`、`.codex`、`.cursor`、`.claude` layout 不匹配时会把完整 package root 误当 repo root；
- 随后错误追加 `.trellis/guru-team/scripts/bash/run-skill-command.sh`，在 shared dispatcher 前失败；
- interface-declared mandatory recorder/validator 因此不能产生任何 typed exit。

Round 4 要求修复六布局 resolver、保持 unsupported layout fail closed、同步所有 copies、增加真实命令 regression，并在 fresh install、`trellis update`、preset reapply 三个 checkpoint 执行 wrapper smoke。

### 当前实现

当前 recorder 与 checker 不再使用单一 suffix 展开，而是与同 package `invoke.sh` 及既有 `guru-review-branch` wrapper 一致，对以下六种 exact package root 做显式 `case` resolution：

1. `trellis/skills/guru-team/packages/guru-review-task-publication`
2. `.trellis/guru-team/skills/packages/guru-review-task-publication`
3. `.agents/skills/guru-review-task-publication`
4. `.codex/skills/guru-review-task-publication`
5. `.cursor/skills/guru-review-task-publication`
6. `.claude/skills/guru-review-task-publication`

未命中受支持 layout 时 `REPO_ROOT` 保持为空，wrapper 在 dispatcher 前 fail closed；没有 fallback 到 package-local 伪 repo root，也没有把 semantic judgment 移入 shell。

相同实现已同步到 canonical、installed shared 与四个平台 copies。三个被修改的 package 文件——recorder、checker 与 contract regression——在 canonical 与五个 destination 的 bytes 和 mode 完全一致。

### 六布局真实命令证据

本轮清除 `GURU_TEAM_DISPATCHER` override 后，直接执行 interface 中声明的 recorder/checker command，共 12 条：

| Layout | recorder | checker | 语义结果 |
| --- | --- | --- | --- |
| canonical source | rc=`2` | rc=`2` | 两条都已到达 shared dispatcher；dispatcher 按设计拒绝 audited source package layout |
| installed shared | rc=`0` | rc=`0` | 两条都输出 shared runtime usage |
| `.agents` | rc=`0` | rc=`0` | 两条都输出 shared runtime usage |
| `.codex` | rc=`0` | rc=`0` | 两条都输出 shared runtime usage |
| `.cursor` | rc=`0` | rc=`0` | 两条都输出 shared runtime usage |
| `.claude` | rc=`0` | rc=`0` | 两条都输出 shared runtime usage |

canonical 的 rc=`2` 是 shared dispatcher 对 audited source layout 的既定拒绝，不是 Round 4 的 nested package-root resolution failure；installed/shared 与四平台共 10 条用户可运行入口全部 rc=`0`。所有命令均不再尝试：

```text
<package-root>/.trellis/guru-team/scripts/bash/run-skill-command.sh
```

package regression 还把 package 复制到 unsupported 临时位置并验证拒绝，证明 resolver 没有通过任意父目录猜测扩大受支持布局。

### Preset 与开箱即用闭环

修复暴露出 workflow runtime wrapper 尚未作为 preset managed assets 安装。当前 canonical preset 已把以下两个 exact runtime wrappers 纳入 `MANAGED_ASSET_PATHS` 与 executable 集合：

- `.trellis/guru-team/scripts/bash/record-task-publication-review.sh`
- `.trellis/guru-team/scripts/bash/check-task-publication-review.sh`

对应终态：

- preset managed assets：`94`
- installed Skill managed files：`2100`
- upstream ownership managed assets：`50`
- sidecars：`0`
- removals：`0`
- conflicts：`0`
- recursive `.new/.bak/.orig`：`0`

throwaway verifier 从 `interface.json` 读取 exact command，并清除 dispatcher override，在以下三个 checkpoint 分别真实执行 installed shared 加四个平台的 recorder/checker，共 `10/10`：

1. `fresh-install`：`10/10`
2. `after-trellis-update`：`10/10`
3. `after-preset-reapply`：`10/10`

完整 throwaway 命令 exit=`0`，终态为：

```text
Verified public marketplace discovery plus local unpublished workflow sample
```

因此 Round 4 的五项闭环要求均已满足：

1. 六布局 exact resolver：满足；
2. unsupported layout fail closed：满足；
3. canonical、installed shared、四平台同步：满足；
4. interface recorder/checker 真实执行 regression：满足；
5. fresh install、update、reapply 三阶段真实 wrapper smoke：满足。

### Finding 结论

`BR116-R04-P1-01` 在 reviewed HEAD `d7ab98f5c53f470f4d3f3742f8cfca24f8465edd` 上关闭。没有发现同根因残留、fallback 漏洞、平台遗漏或开箱即用回退。

## 相邻 Phase 2 finding 复核

Round 8 的 `PH2-116-R8-P2-01` 指出 preset regression 仍断言 managed assets=`92`。Round 9 已把遗漏断言更新为 `94`；本轮 fresh scan 确认：

- old literal `92` count=`0`
- expected literal `94` count=`2`
- preset full suite `45/45` 通过
- throwaway 三阶段终态均使用 94-asset manifest

该 Phase 2 finding 保持关闭。它不是本代理的 Branch Review finding，本节只记录与 Round 4 closure 同一修复提交的相邻一致性证据。

## 新 finding、被拒绝候选与观察项

- 本轮没有新的 P0/P1/P2/P3 finding。
- Round 4 保留的 transient empty-response candidate 仍无 fresh 支持路径复现，保持 `rejected_candidate`，不赋 severity。
- 未使用恶意 artifact/hash/state 篡改、对抗性输入、并发、TOCTOU、锁、原子写入或 fault injection 构造问题。
- current `review.md` / `review-gate.json` 尚未消费本轮 raw closure evidence；这是主会话在报告完成后的 recorder/gate 流程状态，不是本轮允许自修复的 implementation finding。本报告本身不能把 gate 标记为 pass。
- Remote exact candidate-branch marketplace install 仍受分支未 push 限制；public marketplace discovery 与 local unpublished workflow sample 已验证。该已声明 publication-time limitation 不影响本地 finding closure，也不授权本轮 push。

## Public Skill I/O、语义边界与分发判断

- 本修复没有修改 `guru-review-task-publication` 的 public input、三个 typed exits、unique consumers、Interface 1.3 semantic dimensions 或 schema。
- recorder/checker 仍只负责 deterministic dispatcher resolution、记录与校验；scope、finding、publication sufficiency、route 与 pass/block 仍由 AI Review Gate 决定。
- source package validator：11 active Skills、42 exits、25 targets，`passed`。
- installed package validator：2100 managed files、0 sidecar/removal/conflict，`passed`。
- canonical 与五 destination package copies 的 bytes/mode parity 通过；两个 runtime wrappers 在 canonical/installed 间 bytes 与 executable parity 通过。
- `extension.json` 的 94 个 managed assets、2100 个 Skill files 与 public companion script command identities 一致。

## Docs SSOT

- Approved strategy：`ssot_first`
- Phase 2 记录的 16 个 durable paths在本轮重新计算 SHA-256 与 size，mismatch count=`0`。
- Resolver 与 regression 修复恢复已批准 durable installer/Skill contract 声明的 runnable behavior，没有改变 public contract；Round 9 的 no-additional-durable-doc-delta 判断在当前 committed diff 上仍成立。
- Task delta 已合并到 `implementation-handoff.md` 第 11/12 节、Phase 2 reports 与 `phase2-check.json`，并由 sequence 003 commit 固定。
- Round 4 所述 durable OOTB/runnable contract 与实际 wrapper 行为的不一致已消除。
- Docs SSOT closure 判断：`consistent_for_finding_closure`。
- 本判断仅适用于 current finding closure；最终 fresh reviewer 仍需重新审查完整 current-scope Docs SSOT。

## 验证结果

### 本轮独立执行

- Publication package contract（canonical）：`Ran 18 tests in 10.404s`，`OK`
- Publication package contract（installed）：`Ran 18 tests in 10.760s`，`OK`
- Full Skill packages：`Ran 174 tests in 278.874s`，`OK`
- Full preset installer：`Ran 45 tests in 91.569s`，`OK`
- Upstream ownership：`Ran 9 tests in 0.751s`，`OK`
- Publication validator wrapper direct execution：
  - canonical recorder/checker：2/2 到达 shared dispatcher，expected/actual rc=`2`
  - installed shared 与四平台 recorder/checker：10/10 到达 shared dispatcher usage，expected/actual rc=`0`
- Fresh throwaway install/update/reapply：
  - `fresh-install` publication wrappers：`10/10`
  - `after-trellis-update` publication wrappers：`10/10`
  - `after-preset-reapply` publication wrappers：`10/10`
  - full command exit=`0`
- Source package validator：`passed`
- Installed package validator：`passed`
- Upstream ownership validator：`status=ok`，managed assets=`50`
- Dogfood overlay drift：`status=ok`
- Canonical/installed/four-platform package bytes/mode parity：通过
- Runtime wrapper bytes/executable parity：通过
- Managed assets/Skill files：`94/2100`
- Sidecar/removal/conflict/recursive backup scan：`0/0/0/0`
- Durable paths digest/size comparison：16 paths，mismatch count=`0`
- `git diff --check origin/main...HEAD`：exit=`0`
- `git diff --check`：exit=`0`
- Deploy-sensitive finding-fix changed-path scan：`0`
- Finding-fix added credential-shaped token scan：`0`

### Fresh Phase 2 与 commit evidence

- Full runtime：`Ran 572 tests`，`OK (skipped=13)`
- Source/installed publication shared actual-wrapper eval：各 7 cases，`status=passed`
- Round 9 Phase 2：findings=`0`、`passed`
- `phase2-check.json` digest：`a8d7d6ffaef2883356f6de06851fa2b57aa48f80be07a34b8bf62cac5171fd1f`
- Sequence 003 commit：exact 35-path tree/blob/mode evidence 全部匹配

### Lint、TypeCheck、Tests 口径

- Lint：仓库没有独立统一 lint 命令；full suites、package validators、dogfood drift、shell real-command execution 与两种 `git diff --check` 均通过。
- TypeCheck：仓库没有独立静态 type-check 命令；本 finding 相关 shell 与 Python tests 由全量 suites 覆盖，Phase 2 的 Python compile 证据保持有效。
- Tests：通过。

## Issue scope、安全与部署影响

- `close_issues` 只有 #116。
- Related：#115、#131、#144、#146。
- Follow-up：#81、#117、#118、#119、#132。
- `BR116-R04-P1-01` 属于 #116 当前 active package 的 recorder/checker 与开箱即用范围，已在本任务内关闭；没有转移给 follow-up issue。
- 未发现 secret、credential、private key、`.env`、database URL、signed URL、客户数据或敏感原始记录泄漏。
- 无 CI/CD、Docker/Compose、Kubernetes/Kustomize/Helm、DB migration、Makefile 或 dependency manifest 变更；存在 workflow/preset/package/platform distribution 影响，已由 fresh install/update/reapply 覆盖。
- 当前分支未由本代理 push；未创建或更新 PR，未关闭 issue，未 archive/finalize。

## 证据交接与最终结论

Round 5 按 finding-owner continuity 覆盖完整 `origin/main...HEAD` identity、finding-fix commit、六布局 resolver、interface exact recorder/checker commands、canonical/installed/platform parity、preset 94-asset inventory、fresh install/update/reapply、regression suites、Phase 2、commit evidence 与 Docs SSOT。

Round 4 的 normal-path P1 已在全部受支持布局上以真实命令关闭；unsupported layout 继续 fail closed；fresh install、Trellis update 与 preset reapply 均证明 installed shared 与四平台 wrappers 可到达 shared dispatcher。没有发现新 finding。

最终为 `closure_passed`，`findings_count=0`，`BR116-R04-P1-01=closed`。本报告可作为 Round 4 finding closure raw evidence，但不能作为最终放行报告，也不能单独支持 Branch Review Gate pass。主会话在记录本轮后，必须分配另一个 fresh final-release reviewer 对 `bdc8f50bcd1e325aed331d4b01107b83ed8ee940...d7ab98f5c53f470f4d3f3742f8cfca24f8465edd` 执行最终放行审查。
