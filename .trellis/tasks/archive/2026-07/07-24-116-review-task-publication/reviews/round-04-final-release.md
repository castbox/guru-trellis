# #116 Branch Review 第 4 轮最终放行审查原始报告

## 审查身份与结论

- 审查角色：`最终放行审查代理`
- 审查代理：`/root/issue116_branch_review_final_round4`
- 审查轮次：`round-04`
- 审查身份：未参与 #116 的 implementation、Phase 2、Round 1 finding discovery、Round 2 finding ownership 或 Round 3 closure；本轮是 fresh final-release technical identity。
- 最终结论：`implementation_required`
- findings_count：`1`（P0=`0`，P1=`1`，P2=`0`，P3=`0`）
- 放行判断：不通过。当前 HEAD 不得进入 Branch Review Gate pass、publication、push、PR、issue close、archive 或 finalize。

## 审查绑定与工作区证据

- GitHub repository：`castbox/guru-trellis`
- Live issue：`#116`，状态 `OPEN`；已读取 issue 正文与 accepted-current comment `5045033833`。
- 工作树：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/116-review-task-publication`
- 基线：`origin/main@bdc8f50bcd1e325aed331d4b01107b83ed8ee940`
- 审查 HEAD：`1dd2ef8af1cf583eeaf302a11c4770a07922b0b2`
- 完整差异：`bdc8f50bcd1e325aed331d4b01107b83ed8ee940...1dd2ef8af1cf583eeaf302a11c4770a07922b0b2`
- Merge base：`bdc8f50bcd1e325aed331d4b01107b83ed8ee940`
- 差异规模：337 files、2 commits。
- 工作提交：
  - `aacb6e02e5386578bfe3d046511a0002a51cb581 feat(workflow): #116 实现 task publication 审查闭环`
  - `1dd2ef8af1cf583eeaf302a11c4770a07922b0b2 fix(workflow): #116 收紧 publication 状态校验`
- `task-commit-plans/002.json` 的 committed result 绑定当前 HEAD、parent `aacb6e02e5386578bfe3d046511a0002a51cb581`、23 个 exact committed paths 与 tree `3dc28ab29af7f5485d55e7837647d7ceb2a8af10`，expected/actual tree 与每个 blob/mode 均匹配。
- `check-workspace-boundary.sh` 在审查前与报告写入前均返回 `status=ok`：expected workspace 与 actual repo root 都是本 task worktree；source checkout 为 `/Users/wumengye/Documents/GoProjects/guru-trellis`、HEAD 为 base commit、status 为空，`suspicious_source_artifacts=[]`。
- 报告写入前的 worktree tail 只有主会话维护的 `agent-assignment.json`、`task-commit-plans/002.json` 与 Round 3 raw report；这些 task metadata 未被当作 implementation diff。

## 已读取的审查证据

本轮读取并交叉核对：

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
5. `implementation-handoff.md`，特别是第 9 节 `BR116-R02-P2-01` 与第 10 节 `PH2-116-R6-P2-01`；
6. `phase2-check.json`、Round 6/7 Phase 2 reports、commit plans 001/002、issue scope ledger；
7. Round 1/2/3 raw reports、current historical `review.md` / `review-gate.json` 与完整 assignment/liveness lifecycle；
8. 完整 337-file committed diff、publication runtime、Interface 1.3、schemas/examples、package scripts、eval adapter/corpus、workflow routes、registry/manifest、preset/platform copies、durable docs 与 tests。

Planning 三件套 current SHA-256 与 approval 完全匹配：

- `prd.md`：`9814f640a7a624740b7f0cb06dc6e9b010e428ed523a5bd70345ba2b8ab7de01`
- `design.md`：`b2a38854623d55558807732a72bd586cfa60e38aafe22a0fb1b80a1168d2a408`
- `implement.md`：`13f7ec2d8fa925a803b37c662cd796fd47a62b0a574b8f2ca96b031099520603`

Planning approval 为 schema `2.0`、`typed_exit=approved`，包含 passed ambiguity review、fixed-scope scanner 零未检查 normative hit 与 explicit post-planning confirmation。

## Prior finding closure 复核

### `BR116-R02-P2-01`

Round 3 的 closure 仍成立。当前 ordinary publication status allowlist 只接受 Branch Review exact task metadata、publication 三文件与显式 regular runtime input；`pr-readiness.json` self-excluded；dedicated finalization 只增补 exact current-task `closeout-plan.json`。定向 4 项回归在本轮重新运行，结果 `4/4 OK`。

### `PH2-116-R6-P2-01`

Round 7 的 closure 仍成立。`task_publication_repository_binding()` 使用 `git_status_paths(..., fail_closed=True)`；status 命令失败会向 binding、entry、checker 与 finalization augmentation 传播错误，而不会投影成空 status。本轮代码审查与对应 regression 未发现回退。

上述 closure 不抵消本轮独立发现的 package command 可执行性问题。

## Qualified finding

### `BR116-R04-P1-01` — installed/shared 与四平台 publication recorder/checker 无法定位 shared dispatcher

- Severity：`P1`
- 状态：`open`
- Scenario class：`normal_required_behavior`
- Qualification：`qualified_current_finding`
- Reviewed HEAD：`1dd2ef8af1cf583eeaf302a11c4770a07922b0b2`
- Owner round：`round-04`
- 受影响路径：
  - `trellis/skills/guru-team/packages/guru-review-task-publication/scripts/record-task-publication-review.sh`
  - `trellis/skills/guru-team/packages/guru-review-task-publication/scripts/check-task-publication-review.sh`
  - 由 preset 生成的 `.trellis/guru-team/skills/packages/`、`.agents/`、`.codex/`、`.claude/`、`.cursor/` 同名副本

#### 正常路径复现

在当前 task worktree、未设置隐藏 dispatcher override 的普通安装状态中执行 interface 声明的命令：

```text
.trellis/guru-team/skills/packages/guru-review-task-publication/scripts/record-task-publication-review.sh --help
```

返回 rc=`1`，尝试执行：

```text
<repo>/.trellis/guru-team/skills/packages/guru-review-task-publication/.trellis/guru-team/scripts/bash/run-skill-command.sh
```

同一 installed checker 也返回 rc=`1`。`.agents`、`.codex`、`.claude`、`.cursor` 的 recorder 与 checker 共 8 个直接调用全部返回 rc=`1`，并分别尝试在自身 package root 下附加 `.trellis/guru-team/scripts/bash/run-skill-command.sh`。

Canonical source 两个脚本能构造 repo-local dispatcher，但在当前 audited layout 下返回 rc=`2`；它们不能作为 installed/platform 命令失效的替代正常入口。

#### 根因

两个脚本第 5 行只执行：

```bash
REPO_ROOT="${PACKAGE_ROOT%/trellis/skills/guru-team/packages/guru-review-task-publication}"
```

当 `PACKAGE_ROOT` 是 installed shared 或平台 root 时，该 suffix 不匹配，参数展开保留完整 package root；第 6 行随后在 package root 下错误追加 `.trellis/guru-team/scripts/bash/run-skill-command.sh`。

同一 package 的 `scripts/invoke.sh` 已正确 case-match canonical、installed shared、`.agents`、`.codex`、`.cursor` 与 `.claude` 六种 layout。`guru-review-branch` 的 recorder/checker 也使用相同六 layout resolver，因此本问题不是平台不支持或 package 自包含要求，而是 publication 两个 validator wrappers 漏掉既定 resolver。

#### 当前范围与合同绑定

该 finding 直接违反当前 #116 合同：

1. `interface.json` 第 64/65 行把这两个 exact script 分别声明为 `publication_review_recorder` 与 `publication_review_checker`；
2. `SKILL.md` 第 8-11 行要求在 semantic review 后调用 package recorder 与 checker through shared dispatcher；
3. Interface stage order 是 `forward_behavior -> ai_review_gate -> conditional_human_confirmation -> recorder_validator -> typed_exit`；两个命令均在 dispatcher 前失败，三个 typed exits 因而不可到达；
4. `implement.md` Step 5 要求实现 recorder/checker，Step 11 要求 clean install/update/reapply 的 wrapper smoke 与开箱即用；
5. `.trellis/spec/preset/installer.md` 要求 active package、runtime commands、installed shared 与 Codex/Cursor/Claude copies 同步，并在 fresh install/update/reapply 后可运行。

该复现只使用 current installed files 与普通命令调用，不依赖伪造 artifact、恶意输入、并发、TOCTOU、锁或 fault injection。

#### 影响与 severity

这是 active `guru-review-task-publication` 的 mandatory semantic closed loop。用户或平台即使已完成十维 AI Review Gate，也不能通过 interface 声明的 package recorder/checker 记录与复验唯一 `pr-readiness.json`，因此 workflow 与 standalone mode 都无法按 Skill 合同产生任何 typed exit。影响不是可选文档、边缘 metadata 或单个平台，而是 installed shared 加全部四个平台副本的核心新能力。

因此定为 P1，并阻塞当前最终放行。

#### 现有验证为何未捕获

- source/installed validator 只验证文件、digest、mode、registry/manifest 与 command identity，没有执行两个 validator wrappers 的 dispatcher resolution；
- multi-root wrapper test 只覆盖 `scripts/invoke.sh`；
- publication package contract tests 验证 semantic/schema/runtime 规则，没有直接执行 recorder/checker scripts；
- shared actual-wrapper eval 真实执行 public `invoke.sh`，但 native adapter 在 owner staging 时直接加载 owner runtime/dispatcher，不走这两个 package scripts；
- fresh throwaway 的 wrapper/eval smoke 同样未直接执行 recorder/checker wrappers。

因此本轮 `572/174/45/9`、source/installed `7/7` eval 与 fresh throwaway 全部通过，不构成对该真实正常路径失败的反证；相反，缺少 multi-root validator-command execution regression 是覆盖缺口。

#### 修复与闭环要求

本轮 Branch Review 不修改实现。后续 implementation 必须：

1. 让 recorder/checker 使用与 `invoke.sh`、`guru-review-branch` 一致的受支持 package-root resolver，并保持 unsupported layout fail closed；
2. 同步 canonical、installed shared、`.agents`、`.codex`、`.claude`、`.cursor` copies；
3. 新增 regression，实际执行 interface 中的 recorder/checker command，覆盖 canonical、installed shared 与四平台 layout；不能只断言存在、executable、byte parity 或直接调用 runtime；
4. 在 fresh install、`trellis update` 与 preset reapply 后实际执行两个 validator wrappers，证明 shared dispatcher resolution 与 mode parity；
5. 重新执行完整 Phase 2、Docs SSOT reconciliation、finding-fix commit、同 finding owner closure review，再由另一个 fresh final-release reviewer 覆盖完整新 HEAD。

## Public Skill I/O、语义边界与分发判断

- Interface 1.3 的两个 input profiles、十二个 entry preconditions、十个 semantic dimensions、三个 typed exits 与 unique consumers 在数据合同层保持一致。
- Public wrapper 从 checker-passed owner result 选择 actual exit；`expected_exit` 仅供 grader 比较。source/installed shared eval 各 7/7 通过。
- Runtime 的 exact publication allowlist、`pr-readiness.json` self-exclusion、finalization-only `closeout-plan.json` augmentation 与 status-read fail-closed 均符合 durable contract。
- Canonical、installed、Agents、Codex、Claude、Cursor package bytes 完全一致；但本 finding 正是一个被 byte-identical 同步到所有 destination 的 canonical functional defect。Parity 不能替代 runnable parity。
- Semantic scope、finding、route 与 publication sufficiency 仍由 AI owner；本 finding 不要求把判断移入脚本，只修复 deterministic dispatcher resolution。

## Docs SSOT

- Approved strategy：`ssot_first`
- Phase 2 记录的 16 个 durable paths 在本轮逐项重新计算 SHA-256 与 size，mismatch count=`0`。
- `BR116-R02-P2-01` 的 exact allowlist delta 已合并；`PH2-116-R6-P2-01` 恢复既有 fail-closed 合同，没有遗漏 durable delta。
- 但是 current durable installer/Skill contracts宣称 installed shared 与平台 package commands 在 fresh install/update/reapply 后可运行，而实际 recorder/checker wrappers 均在 dispatcher 前失败。当前实现与 Docs SSOT 的 OOTB/runnable contract 不一致，因此 Docs SSOT 最终判断为 `blocked_by_BR116-R04-P1-01`。
- Remote candidate-branch marketplace verification 仍因分支未 push 而不存在；public marketplace discovery 与 local unpublished workflow sample 已验证。该既有 limitation 不阻塞本地审查，但也不影响本 finding 的本地普通安装复现。

## 验证结果

- Full runtime：
  - `python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
  - `Ran 572 tests in 174.760s`
  - `OK (skipped=13)`
- Full Skill packages：
  - `python3 trellis/skills/guru-team/tests/test_skill_packages.py`
  - `Ran 174 tests in 280.424s`
  - `OK`
- Full preset installer：
  - `python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`
  - `Ran 45 tests in 95.050s`
  - `OK`
- Upstream ownership：`Ran 9 tests`，`OK`
- Exact allowlist/finalization targeted regression：`Ran 4 tests`，`OK`
- Source/installed publication shared actual-wrapper eval：各 7 cases，`status=passed`
- Source package validator：`passed`，11 active Skills、42 exits、25 targets。
- Installed package validator：`passed`，2100 managed files、0 sidecar/removal/conflict。
- Dogfood overlay drift：`status=ok`
- Canonical/installed/platform package与 runtime/workflow byte parity：通过。
- Phase 2 durable path SHA-256/size fresh comparison：16 paths，mismatch count=`0`。
- Fresh throwaway：
  - `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 ./trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`
  - exit `0`
  - 覆盖 clean init/install、initial closeout、`trellis update`、workflow/preset reapply、after-update closeout、developer/no-developer、source/installed validator、ownership/drift、marketplace discovery；
  - 终态：`Verified public marketplace discovery plus local unpublished workflow sample`
  - 限制：未执行 publication recorder/checker package wrappers，因此未覆盖本 finding。
- Publication validator wrapper direct execution：
  - installed shared recorder/checker：2/2 failed，rc=`1`
  - `.agents/.codex/.claude/.cursor` recorder/checker：8/8 failed，rc=`1`
  - 结果：`BR116-R04-P1-01` reproduced
- `python3 -m py_compile` canonical runtime/test 与 installed runtime：通过。
- `bash -n` publication recorder/checker/invoke：通过；finding 是运行时路径解析，不是 shell syntax。
- `git diff --check <base>...<HEAD>`：exit `0`
- `git diff --check`：exit `0`
- Recursive `.bak/.new/.orig` scan：0
- Deploy-sensitive changed-path scan：无 CI/CD、container、K8s/Helm、DB migration、Makefile 或 dependency manifest 命中。
- Added credential-shaped token scan：0
- Lint：仓库没有独立统一 lint 命令；diff check、shell syntax、package validators与全量 suites已执行，但 P1 functional finding 阻塞。
- TypeCheck：仓库没有独立静态 type-check 命令；Python compile通过，但 P1 functional finding 阻塞。
- Tests：机械 suites通过；normal-path validator wrapper execution失败。

只读 durable digest loop 首次使用 zsh 特殊变量名 `path`，临时覆盖了命令搜索路径并产生无效 command-not-found 输出；该次结果未被采信。改用 `file_path` 后完整重跑，16 paths 的 digest/size mismatch count=`0`。

## Issue scope、安全与部署影响

- `close_issues` 只有 #116。
- Related：#115、#131、#144、#146。
- Follow-up：#81、#117、#118、#119、#132。
- 本 finding 属于 #116 当前 active package 的 recorder/checker 与开箱即用交付，不得转移给 #118 finalization 或 #119 integration。
- 未发现 secret、credential、private key、`.env`、database URL、signed URL、客户数据或敏感原始记录泄漏。
- 无 CI/CD、Docker/Compose、Kubernetes/Kustomize/Helm、DB migration、Makefile 或生产服务部署变更；存在 workflow/preset/package/schema/platform distribution 影响。
- 当前分支未 push；未创建或更新 PR，未关闭 issue，未 archive/finalize。

## 被拒绝候选、观察项与后续候选

- Round 3 保留的 transient empty-response candidate 仍无 fresh 正常路径复现，保持 `rejected_candidate`，不赋 severity。
- 没有使用恶意 artifact/hash/state 篡改、对抗性输入、并发、TOCTOU、锁或 fault injection 构造 finding。
- Remote exact candidate-branch marketplace install 是现有 publish-time limitation，不是本轮新增 finding。
- #118/#119/#132 保持原 follow-up 边界；它们不承担 `BR116-R04-P1-01`。

## 证据交接与最终结论

Round 4 作为 fresh final-release review 已覆盖 live authority、approved planning、curated specs、完整 337-file/2-commit diff、Phase 2、commit evidence、Round 1-3 finding lifecycle、Docs SSOT、public I/O、runtime、distribution、tests、fresh install/update/reapply 与工作树边界。

`BR116-R02-P2-01` 与 `PH2-116-R6-P2-01` 保持关闭；但本轮独立确认新的 `BR116-R04-P1-01`：active publication Skill 的 interface-declared recorder/checker 在 installed shared 与全部四个平台 discovery roots 中无法解析 shared dispatcher，导致 mandatory semantic closed loop 无法从 AI Review Gate进入 recorder/validator 与 typed exit。该问题在支持的普通路径稳定复现，属于 current #116 acceptance 与 OOTB contract，P1 open。

最终为 `implementation_required`，`findings_count=1`。本报告可作为 Branch Review finding-owner raw evidence，但不能支持 current `review.md` / `review-gate.json` pass。主会话必须返回 implementation；修复后重新完成 Phase 2、commit、closure review 与另一 fresh final-release round。
