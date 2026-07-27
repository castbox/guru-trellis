# Issue #118 verification metadata re-entry 修复交接

## 1. 身份、范围与 plan strategy

- Task：`.trellis/tasks/07-26-118-guru-finalize-task`。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/118-guru-finalize-task`。
- Branch：`feat/118-guru-finalize-task`。
- Base：`origin/main@7820a9eeec2a2a75fb52fba156a7211d9f9fb09c`。
- 实现起始 HEAD：`77ad13f0a65f652e68e655afbe11917aa659df5c`，加当前未提交 finding-fix delta。
- Finding：本 implementation 只处理 Round 12 P1
  `F-VERIFICATION-METADATA-REENTRY-01`；Round 12 P3
  `F-ROUND9-TRAILING-WHITESPACE-01` 不在本 implementation 中修改。
- Plan strategy：保持 approved `ssot_first`。先用 #117 owner checker 验证 current、
  same-task/plan/ref/HEAD evidence，再让 publication checker 对已验证的唯一
  `marketplace-verification.json` 做 finalizer-only compatibility augmentation；不得先放宽
  generic publication allowlist，也不得让任意 metadata 进入。

本 handoff 是 task-local implementation evidence，不替代 fresh Phase 2、finding closure、
Branch Review、publication review 或 finalization gate，也不授权任何外部副作用。

## 2. P1 根因与实现

正常 content push 后，#117 workflow `verified` 或 task-bearing standalone `not_required`
recorder 会写入唯一 task-local `marketplace-verification.json`。此前 #118 real preview 的顺序
是先检查 publication owner、再检查 verification owner；publication augmentation 只接受
plan/gate，因此在 #117 owner checker 有机会证明 evidence current 之前，就把该合法 artifact
判为 unexpected metadata，并路由 `publication_review_stale`。

实现修复如下：

1. `finalization_preview_context()` 对 verification re-entry profiles 先调用 #117 owner
   checker；非 verification profiles 保持原路径。
2. 已通过检查的 owner result 显式传给
   `finalization_publication_owner_result()`。只有 checker `status=ok` 且 exit 为
   `verified|not_required` 时，publication augmentation 才能启用 verification metadata。
3. `check_task_publication_for_finalization_augmentation()` 新增默认关闭的
   `allow_verification_metadata`。没有显式 owner binding 时，即使 caller 直接提供精确路径，
   仍 fail closed。
4. Finalizer-private verification augmentation 对 task-bearing standalone
   `marketplace.required=false` 的正常 `not_required` artifact，只在精确 owner locator 实际
   dirty 时把该单一路径加入 expected set。任意额外路径继续失败；generic #117 checker 未改。
5. Canonical runtime 已同步到 dogfood runtime，二者 byte-identical。

该修复不改变 public profile、Interface、schema、DTO、typed exit、consumer、transaction
ordering、confirmation 或 #105 closeout engine。

## 3. Regression 与 P1 implementation closure

新增四项 real regression：

- workflow `verified`：真实 #117 recorder、#117 public checker/wrapper、非 staged #118
  preview、finalization gate recorder/checker、#118 public wrapper 全链通过；
- task-bearing standalone `not_required`：同一真实 producer/checker 到 #118 public wrapper
  全链通过；
- 任意额外 metadata：real preview fail closed；
- 精确 verification path 但没有 explicit owner binding：publication augmentation fail closed。

四项最终单测均 exit 0；测试显式设置 `GURU_TEAM_EVAL_STAGING=0`，不使用 eval terminal
facts shortcut。P1 required closure 中的两条正常路径与两条严格负面边界均已由实现证据覆盖，
因此 implementation-side closure evidence 完成。P1 的 formal status 仍须由 fresh Phase 2 与
独立 finding-closure reviewer 按 lifecycle 正式判定，本实现代理不写 gate 或 closure 结论。

## 4. 验证终态

- Runtime full：`Ran 624 tests in 190.878s`，`OK (skipped=13)`，exit 0。
- Skill packages full：`Ran 179 tests in 359.172s`，`OK`，exit 0。
- Finalization focused：11/11 passed。
- Verification focused：11/11 passed。
- Publication focused：13/13 passed。
- 四项新增 real/negative regression：4/4 passed。
- Canonical、dogfood、test Python `py_compile`：exit 0。
- Canonical/dogfood `cmp`：exit 0，byte-identical；共同 SHA-256：
  `78ef92b5e69dd0036a537fe3904856f017569f2f6ef4c6a23ceb23fab2d6af11`。
- Canonical tests SHA-256：
  `c6f426e32532bc7a3612536e500d259a9a01a5319aae6e93e64c35dfdc52e9a3`。
- 本次三个 code/test paths 的 `git diff --check`：exit 0。
- 当前 working-tree `git diff --check`：exit 0。

完整 committed range `git diff --check origin/main...HEAD` 唯一输出为：

```text
.trellis/tasks/07-26-118-guru-finalize-task/reviews/round-009-finding-closure.md:203: trailing whitespace.
```

这不是遗漏修复，原因见第 6 节。

## 5. Docs SSOT reconciliation

Docs strategy 保持 `ssot_first`，结论为 `no_docs_update_needed`。当前 durable contracts 已明确
要求本次行为：

- `.trellis/spec/workflow/workflow-contract.md` 的 Phase 3.7 已定义 verified/not-required
  re-entry、generic #117 strictness 与 finalizer-only immutable-plan-bound metadata tail；
- `.trellis/spec/workflow/skill-package-contract.md` 已定义 workflow `verified`、reachable
  task-bearing standalone `not_required`、唯一 tracked private artifact 与最小
  `verification_ref` handoff；
- `.trellis/spec/workflow/companion-scripts.md` 已定义 finalizer-owned compatibility checker
  必须绑定 owner task/plan/HEAD/repository/remote/evidence allowlist，并拒绝任意额外 dirty path；
- `guru-finalize-task/references/contract.md` 已定义 verification re-entry 先运行 #117 owner
  checker，以及 exact compatibility augmentation。

因此 durable docs 与 approved task delta 没有新语义差异；本次只是 runtime/test 对既有 SSOT
的 correctness 修复。没有修改 planning artifacts、durable spec、public package contract、
Interface、schema、example 或 eval corpus。

## 6. P3 deferred semantic qualification

Round 9 raw review report line 203 的单个 trailing space 已恢复为原始字节。当前证据为：

- SHA-256：`b1424b1a0a5080730383834c820ad4f50d20f15216f2aec7a9c5a2177dbab3ce`；
- size：18367 bytes；
- lines：283；
- 与 `agent-assignment.json` Round 9 `review_report_sha256`、
  `review_report_size_bytes` 及 completed event 完全一致。

直接删除该空格会使 immutable raw review report 与 assignment 中的 owner binding 失配，并让
liveness/assignment checker fail closed。不可变审计证据优先于历史报告样式，因此本
implementation 不修改 ledger digest、不修改 shared assignment recorder，也不重写
assignment/review/gate。P3 应由后续 fresh independent closure reviewer 重新判断：在保持历史
raw evidence identity 的前提下，重新 qualification 该 committed whitespace 是否仍为可执行
current finding，并给出独立 closure/defer 结论。

## 7. 精确 changed paths 与未改边界

本 implementation 拥有的最终 changed paths：

1. `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
2. `.trellis/guru-team/scripts/python/guru_team_trellis.py`
3. `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
4. `.trellis/tasks/07-26-118-guru-finalize-task/implementation-handoff-verification-metadata-reentry-fix.md`

明确无本次 delta：

- global/dogfood workflow、workflow/preset README、preset overlays；
- `trellis/skills/guru-team/packages/**`、registry、Agents/Codex package copies、public
  schemas/interfaces/examples/eval corpus；
- `.trellis/spec/**` durable Docs SSOT；
- `prd.md`、`design.md`、`implement.md`、planning approval、Phase 2、issue scope ledger；
- publication/finalization/marketplace verification/finish artifacts；
- upstream Finish family、official `.trellis/scripts/task.py`；
- #119 global integration、#132 overlay cleanup 与 #105 transaction semantics。

工作树中已有的 `agent-assignment.json`、`review-gate.json`、`review.md`、
`task-commit-plans/005.json` 和 Round 11/12 raw reports 属于并行主会话/审查证据，本实现代理
未修改、回退、格式化或覆盖它们。

未执行 commit、push、PR、archive、publication/finalization gate recorder、Issue mutation、
deploy、production write、tag/release、全局 npm 或 `node_modules` mutation。

## 8. 后续

下游必须把当前 runtime/test/handoff delta 纳入 fresh Phase 2、task commit、P1 independent
finding closure 与 fresh final Branch Review。P3 应按第 6 节单独进行语义重资格化，不得通过
破坏 Round 9 raw evidence identity 来机械消除 lint 输出。publication/finalization 只有在对应
owner evidence 重新 current 且取得必要确认后才能继续。
