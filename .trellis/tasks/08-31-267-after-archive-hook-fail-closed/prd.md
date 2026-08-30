# #267 after_archive hook fail-closed Release Gate 修复需求

## 1. Goal

修复 `v0.6.15-guru.3` exact-candidate 六单元安装矩阵暴露的 Finalizer 缺陷：在
eval-staging installed closeout 路径中，preview 与 execute 必须在任何 closeout 副作用前拒绝
非空 official Trellis `after_archive` hook，从而解除 #267 当前 Release Gate blocker。

本任务只交付该 blocker 的实现、回归与分支级验证。正式 tag、GitHub Release、post-publish
smoke、Issue closure 与业务仓复测仍由后续独立门禁和独立副作用确认控制。

## 2. Live Authority And Candidate Facts

- repository：`castbox/guru-trellis`；base branch：`main`。
- task base / fresh remote main：`59d25f1caae24684af11d5e9459bd8e7dcfd4c02`。
- base tree：`e68d7030bcabe6476edd53fad2adcb7af9caeb47`。
- #267 current contract：`2026-08-30-r20`；Release identity 固定为 repo tag
  `v0.6.15-guru.3`、extension `0.6.15-guru.39`、Trellis CLI `0.6.15`。
- `v0.6.15-guru.3` tag 与 GitHub Release 均不存在；本任务不得创建二者。
- candidate 已包含 #311 fix commit
  `5b3b7bef73824ae78b8bf13a20cfd9ba01acb2b8`、PR #313 merge commit
  `21c7da14798683193b460a5e7c5bd24c7c517804` 与 PR #314 merge commit
  `3efcce72a0d47e38ec725aa8c0f8498992f3416f`。
- #267 与 #311 保持 OPEN；#312 已 CLOSED。本任务 ledger 的 `close_issues` 为空。
- #311 只有在正式 `.3` business-repository reinstall、原错误路径重试与错误文件重试通过后，
  才进入独立 closure review。

## 3. Failure Evidence

standalone verifier 已实际进入六单元矩阵，但首个 `claude-clean` cell 在
`verify_installed_closeout.py` 中失败：

```text
installed closeout accepted a non-empty official after_archive hook
```

保留的 verifier-private evidence：

```text
/Users/wumengye/Documents/GoProjects/guru-trellis-release-gate-267-59d25f1c-tmp/execution-facts.json
sha256=5262c3ad41d4a1784f039a452dc0e7e417470d4ab0821d50756d46a4cf12c3f9
```

该结果只证明 `claude-clean` 当前 blocker。其余五个 cell、完整 Publication/Finalizer、full diff
review 与 Release Gate 不得据此声明通过。

## 4. Root Cause

- `trellis/skills/guru-team/packages/guru-finalize-task/runtime/owner.py:6313` 的
  `official_after_archive_hook_state()` 已正确解析 official config，并对非空 hook 返回
  `stage=after-archive-hook-preflight`、`hook_executed=false`。
- `prepare_closeout()` 在同文件 `:7423` 调用该 preflight，正常非 eval 路径保持 fail closed。
- `finalization_preview_context()` 在同文件 `:11962` 先调用
  `finalization_eval_preview_context()`；eval context 非空时在 `:11968-11969` 直接返回。
- installed matrix 使用 `GURU_TEAM_EVAL_STAGING=1`，因此 preview 与 execute 共用的 preview context
  路径绕过 `prepare_closeout()` 之前的 hook preflight。
- `trellis/presets/guru-team/scripts/python/verify_installed_closeout.py:950-1100` 已定义端到端
  fail-closed contract，并验证 preview/execute、错误 payload 与零副作用；fixture 本身不是缺陷。

## 5. Requirements

### REQ-267-HOOK-001 Common preflight boundary

`finalization_preview_context()` 必须在 eval-context early return 之前调用
`official_after_archive_hook_state(root)`。preview 与 execute 均必须通过该 common boundary。

### REQ-267-HOOK-002 Direct-path defense preservation

`prepare_closeout()` 中现有 preflight 必须保留，继续保护不经过 preview dispatcher 的 direct caller。
本任务不得用移除既有 defense 的方式消除重复调用。

### REQ-267-HOOK-003 Stable failure contract

非空 official hook 必须返回非零结果，并保留：

- `stage=after-archive-hook-preflight`；
- `hook_executed=false`；
- `configured_command_count` 与配置中的命令数量一致。

空 hook、缺失 hook 与 current 支持的正常 closeout 路径必须保持现有行为。

### REQ-267-HOOK-004 Zero side effects

被拒绝的 preview 与 execute 均不得：

- 创建 hook sentinel；
- 移动、完成或归档 task；
- 改变 local HEAD、remote branch 或 publication head；
- 创建、查询或修改持久 PR state；
- 改变 closeout plan、gate、ledger、readiness 或工作树状态。

### REQ-267-HOOK-005 Contract preservation

本任务不得改变 public Skill I/O、schema、typed exit、consumer、Finalizer owner、source/target checkout
ownership、Release identity、Issue closure 语义或 supported platform/matrix cell 集合。

### REQ-267-HOOK-006 Canonical-first projection

实现先修改 canonical Finalizer runtime 与 owning tests，再通过 preset apply 同步 dogfood installed
projection。canonical 与 `.trellis/guru-team/**` 对应 runtime bytes 必须一致，且不得留下 `.new`、
`.bak`、未知 sidecar 或 owner-private residue。

## 6. Acceptance Criteria

1. focused canonical test 在 `GURU_TEAM_EVAL_STAGING=1` 且 eval context 可用时，证明 preview 对非空
   official hook 返回稳定 preflight payload，且 eval context 未被返回。
2. focused canonical test 通过 execute 的 gate-check/preview-context 路径证明相同拒绝，并断言 archive、
   push、PR 与 Ready mutation 均未调用。
3. `prepare_closeout()` direct caller 的现有 hook preflight 测试继续通过。
4. `verify_installed_closeout.py` 的现有 installed fixture 不做语义放宽，preview 与 execute 都以非零
   结果拒绝 hook，sentinel 不存在，task/HEAD/remote/PR state 全部不变。
5. canonical 与 installed Finalizer focused/full suites、preset apply、dogfood drift、package validation、
   managed-byte/mode parity、permission、registry、consumer graph 与 recursive sidecar-zero 全部 PASS。
6. 分支实现完成后，Phase 2 与 committed full-diff Branch Review 的 P0/P1/P2/P3 未关闭 finding 数量
   全部为 `0`，然后才进入 PR/merge 副作用流程。
7. 修复 PR 合并后，从 fresh remote `main` 记录新的 candidate SHA/tree；新 candidate 必须包含
   `59d25f1c...`、`5b3b7bef...`、`21c7da147...` 与 `3efcce72...`。
8. 新 candidate 从零重跑 standalone verifier 与六个 matrix cells；六个 cell 全部 PASS 后，才继续
   #267 的其余 pre-tag semantic gates。
9. `.3` tag、Release、#267 closure 与 #311 closure 在各自独立确认前均不得发生。

## 7. Docs SSOT Plan

策略：`no_shared_authority_change + canonical_contract_test_sync`。

- current RDT/Architecture authority `current-main-0.6.5-guru.42` 已规定 Finalizer fail-closed、
  installed business-repository closeout 与 `.3` unverified Release boundary；本任务恢复既有 invariant，
  不创建 RDT contribution、Architecture contribution、ADR 或 successor shared authority。
- public Skill contract、schema 与 typed exits 不变。current canonical Finalizer contract 未写明
  non-empty official hook 的 common preview/execute preflight，因此本任务在
  `trellis/skills/guru-team/packages/guru-finalize-task/references/contract.md` 增补该既有 fail-closed
  invariant，再由 preset apply 同步 installed projection。
- `.trellis/spec/**`、`docs/requirements/**`、`docs/design/**`、`docs/test/**` 与
  `docs/architecture/**` 本任务保持不变。
- Planning Architecture owner 若返回 architecture impact、contract incomplete、conflict、regression
  或 sync route，本计划立即失效并按其 typed route 重做。

## 8. Out Of Scope

- 修改 Trellis upstream、global npm、`node_modules` 或未授权业务仓。
- 放宽、删除或跳过 installed fixture 的 hook preflight 断言。
- 重构整个 Finalizer dispatcher、transaction、Publication 或 archive 流程。
- 新增 dual path、fallback pass、cross-SHA evidence reuse 或 matrix cell SKIP。
- 修改 version mapping、tag message、Release notes 或 latest-stable identity。
- commit、push、PR create/merge、tag、Release、Issue closure 或 cleanup。

## 9. Blocking Open Questions

无。
