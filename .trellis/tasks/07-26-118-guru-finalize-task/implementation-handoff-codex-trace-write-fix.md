# Issue #118 Codex native trace writable-root 修复交接

## 1. 身份、边界与终态

- Task：`.trellis/tasks/07-26-118-guru-finalize-task`。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/118-guru-finalize-task`。
- Branch：`feat/118-guru-finalize-task`。
- 实现基线 HEAD：`c04ed1d7a816ac80217953bcf52f7a2a44b645d2`。
- Technical agent id：`/root/issue118_codex_trace_write_fix`。
- Logical role：`实现代理`。
- Current finding：P1 `F-CODEX-TRACE-WRITE-01`。
- 实现终态：本 finding 的代码、回归、canonical/dogfood 同步和验证已完成；无运行中
  命令，无实现 blocker。

本 handoff 只证明 `F-CODEX-TRACE-WRITE-01` 的 implementation closure 输入，不修改或
替代 `phase2-check.json`，也不代表 fresh Phase 2、task commit、独立 Branch Review、
publication review 或 finalization 已通过。

## 2. 正常路径根因

Codex native adapter 使用 `workspace-write`，并把 trusted Git root 作为 `--cd`。当
`--run-root` 位于 repository 外部时，旧 argv 只用 `--add-dir` 授权：

1. `<execution-root>/workdir`；
2. `<execution-root>/public-packages/guru-finalize-task`。

然而 native protocol 要求 Codex 通过同一 execution root 下的
`native-trace-helper.py` 写 `native-trace.json` 和 `native-last-message.txt`。旧 argv 没有
授予它们的 parent execution root，导致 runner 可能返回 `rc=0`，但 structured run/case
实际为 `execution_error`、`native_trace_unavailable`，真实 public wrapper 没有执行。

该问题可由受支持的 trusted-root、repo-external run-root 正常调用直接复现，不依赖恶意
artifact、手工篡改、并发 finalizer、TOCTOU、锁、fault injection、crash consistency 或
跨 OS 原子性。

## 3. 实现与设计承接

### 3.1 Adapter

`native_argv()` 的 Codex 分支新增：

- `execution_root = native_request_path.resolve().parent`；
- 在既有 workdir 与 public projection grants 之前增加
  `--add-dir <execution_root>`。

既有 trusted Git root `--cd`、workdir grant、projection grant、output-last-message 和 native
protocol 均保留。改动没有新增或改变 public profile、DTO、schema、typed exit、consumer、
semantic gate、transaction state 或 recovery ordering。

### 3.2 Regression

新增 workspace-enforcing temporary Codex shim 和
`test_codex_repo_external_execution_root_runs_real_finalizer_wrapper`：

1. 在 repository 外部建立绝对 run root；
2. 通过 installed `run-skill-evals.sh` 执行真实 `guru-finalize-task` public wrapper；
3. 若 argv 没有精确授权 execution root，则 shim 以非零返回拒绝旧合同；
4. shim 仍须通过 native trace helper 读取 Skill contract 并执行真实 `invoke.sh`；
5. 断言 structured run/case 均为 `passed`、actual exit 为
   `publication_review_stale`，且 native trace 最后一个 event 为真实 wrapper `invoke`。

回归因此同时覆盖 argv writable boundary、structured terminal、actual-exit ordering、native
trace receipt 与 real public-wrapper execution，避免再次把 runner `rc=0` 误判为通过。

## 4. 精确 owned paths

本实现代理拥有以下 delta：

1. `trellis/skills/guru-team/adapters/eval/native_adapter.py`
2. `.trellis/guru-team/skills/adapters/eval/native_adapter.py`
3. `trellis/skills/guru-team/tests/test_skill_packages.py`
4. `.trellis/guru-team/extension.json`
5. `.trellis/tasks/07-26-118-guru-finalize-task/implementation-handoff-codex-trace-write-fix.md`

Canonical adapter 经支持的 all-platform preset apply 同步到 dogfood 副本；两份文件
byte-identical，SHA-256 均为
`e519f1babbf5b90999f9cc3f64b431d7fc544a2e9fe2f640be482d4372a8fc35`。Extension manifest
只更新该 managed file 的 SHA-256；apply 产生的 timestamp/source-commit 非语义 churn 已恢复
为原值。

工作树内其余 runtime、review、publication、ledger、commit-plan 与旧 handoff/report delta
均为本轮之前已有状态；本实现代理未回退、覆盖或声明拥有。

## 5. Docs SSOT reconciliation

Approved Docs SSOT strategy 保持 `ssot_first`。主要 durable implementation inputs 为：

- `.trellis/spec/workflow/skill-package-contract.md`
- `.trellis/spec/workflow/companion-scripts.md`
- `.trellis/spec/workflow/quality-guidelines.md`
- `.trellis/spec/preset/installer.md`
- `.trellis/spec/preset/upstream-ownership.md`
- `trellis/skills/guru-team/packages/guru-finalize-task/references/contract.md`

Task `prd.md`、`design.md`、`implement.md` 与 Phase 2 finding 只提供 Issue #118 delta、复现
证据和验收边界。

本轮 Docs 结果为 `no_docs_update_needed`：current durable SSOT 已明确要求 Codex trusted-root
real-wrapper execution、structured result 检查、native trace 与 package/public wrapper 合同。
本修复使 runtime 对齐既有 SSOT，没有产生新的 durable wording、public behavior、安装方式
或 workflow ownership 语义。

- Durable docs sync result：无需新 delta，current durable docs 与修复后实现一致。
- Task delta merged to durable docs：无待合并语义，`task_delta_merged=false`。
- Task-history-only：本 handoff、finding 复现/closure 与实现验证记录。
- Follow-up/current PR limitation：fresh Phase 2 必须重新判断本 no-update 结论；#119 继续
  独占 global Finish family integration/combined acceptance，#132 继续独占 upstream overlay
  cleanup；remote exact-ref verification 仍属于后续 #117/#118 owner gate。

## 6. 验证结果

### 6.1 Focused 与 package

- 新增 Codex repo-external real-wrapper regression：1 test，`OK`。
- `guru-finalize-task` package contract：5 tests，`OK`。
- Full Skill package graph：180 tests，`OK`，377.037 秒。
- Source package validator：`status=ok`；13 active packages，workflow closure
  12/46/27。
- Installed package validator：`status=ok`；2659 managed files，零 removal/conflict/sidecar。

### 6.2 Preset、ownership 与静态检查

- Preset installer tests：45 tests，`OK`，118.419 秒。
- Upstream ownership tests：9 tests，`OK`。
- Upstream ownership validator：`status=ok`；frozen/active/overlay 均为 43，active Skill
  为 13，planned Skill 为 0，`errors=[]`。
- Dogfood overlay drift：passed。
- All-platform preset apply：第一次对旧 managed adapter 正常产生 1 个 `.bak` 并 fail
  closed；reviewed backup SHA-256 为
  `834f07870bed612de06be6af243f7866a7cda4023a1655dd46200007a6418a02`，与旧 manifest
  identity 一致。移出并清理该 backup 后第二次 apply 通过，零 sidecar/conflict/removal。
- Canonical/dogfood adapter `cmp` 与 SHA-256 parity：passed。
- Canonical adapter、dogfood adapter、Skill package test `py_compile`：passed；缓存写入
  repo-external 临时目录并已清理。
- Owned implementation paths `git diff --check`：passed。

### 6.3 真实 Codex native eval

使用 absolute repo-external run root 执行：

```bash
trellis/workflows/guru-team/scripts/bash/run-skill-evals.sh \
  --root . --mode source --skill guru-finalize-task \
  --adapter codex --case publication-review-stale \
  --run-root /tmp/guru118-native-eval.6wracP --json
```

结构化终态：

- runner exit code：0；
- run `status=passed`；
- case `status=passed`；
- `actual_exit=publication_review_stale`；
- native transcript argv 含
  `--add-dir /private/tmp/guru118-native-eval.6wracP/current/publication-review-stale/execution`；
- native trace 共 2 个 events，最后一个为 public
  `guru-finalize-task/scripts/invoke.sh` 的 `kind=invoke`，wrapper return code 为 0；
- eval duration：26768 ms。

该外部临时 run root 已清理，不在 repository 留存 eval payload、trace 或 cache。

## 7. Protected boundaries 与副作用

下列边界保持 no-diff：

- `trellis/workflows/guru-team/workflow.md` 与 `.trellis/workflow.md`；
- `trellis/presets/guru-team/overlays/**`；
- upstream `trellis-finish-work` Skill/Command/Prompt family；
- official `.trellis/scripts/task.py`；
- #105 transaction/recovery semantics。

未执行 `trellis-check`、未记录 `phase2-check.json`、未写 `agent-assignment.json`、未 commit、
push、创建/更新 PR、archive、draft-to-ready、merge、修改 Issue、deploy、production write、
tag/release、修改全局 npm 或 `node_modules`。

## 8. `trellis-check` 交接重点

Fresh Phase 2 应重点复核：

1. repo-external Codex execution root 在 `workspace-write` 下可写 trace/helper output；
2. structured run/case、actual exit、native trace 与真实 public wrapper invocation 全部通过，
   不能只采用 runner return code；
3. 新 regression 会拒绝旧 argv，并真实执行 installed finalizer wrapper；
4. canonical/dogfood/manifest identity、preset reapply、overlay drift、ownership 与 sidecar
   evidence 保持 current；
5. 增加 execution-root grant 没有改变 public Interface 1.3、typed exits、semantic owner、
   private state 或 #105 transaction ordering；
6. Docs SSOT `ssot_first` 和 `no_docs_update_needed` 结论成立；
7. #119 global integration、#132 overlay cleanup 与 upstream Finish assets 未进入 diff。

## 9. 剩余风险与后续

本 finding 的实现范围内未发现 remaining correctness blocker。Claude live eval 的 HTTP 401
仍是既有 external-auth residual，不得描述为 Claude live pass；feature exact ref 尚未 push，
remote marketplace verification 必须由后续 finalizer owner gate 执行。

本轮 delta 会使旧 Phase 2、task commit、Branch Review、publication review、immutable closeout
plan 与 confirmation 自然 stale。主会话后续必须使用 fresh checker 与 owner gates，不得复用
旧 evidence 或由本实现代理越权完成后续流程。
