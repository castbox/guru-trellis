# Issue #118 final projection compatibility chain 修复交接

## 1. 失败现场与 stale checkpoint 身份

- Task：`.trellis/tasks/07-26-118-guru-finalize-task`。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/118-guru-finalize-task`。
- 实现起始 local/remote/PR HEAD：
  `85ab42837a44968d892f520614ab611becf5b8d5`。
- PR：`#160`，`OPEN`、`Draft`；本轮不修改 PR 或 Issue。

本轮开始时 active task 仍保存一组旧 plan-bound checkpoints。删除前已记录其精确身份：

- `closeout-plan.json` bytes SHA-256：
  `d8be2e06cb4c2199744902ce03653509f4c362275cf7520019894c6d3cdd1fe6`；
  plan digest：
  `2d1fbc373cd467c813536cffeca2f9a900abc4bae7ecabf7277a853d84c866c4`；
  reviewed/evidence-parent HEAD：
  `1e5b1479b72e5b253c9755244be87f906cf855f4`。
- `marketplace-verification.json` owner bytes SHA-256：
  `66625c4de68a8997e4a2c882fa83f6e0a38a85b0debb6025d37f86ac794d7336`；
  `verification_ref=extension-verification:97378df8a6853c543d1dca8c`；
  owner task/plan/reviewed/remote HEAD 均绑定上述旧 plan 与 `1e5b147...`。
- 未跟踪 `task-finalization-gate.json` bytes SHA-256：
  `3e5b58f9a09d52c70a0a4d1928adb4dd55d4d665d659f146ef381adad5f6ed78`；
  route 为 private `published` executor marker，同样绑定上述旧 plan/head。
- `issue-scope-ledger.json` 的 `primary_issue=#118` 与 `close_issues=#118` 都保留旧
  `remote_marketplace_verification`，其 artifact SHA 与三个 HEAD 字段分别为
  `66625c...` 与 `1e5b147...`。

这些 checkpoint 早于 current `85ab428...` 及本轮未提交 code/test delta，不能作为新的
Phase 2、publication、finalization 或 verification 输入。本 handoff 先保存 provenance，随后
删除三个 active checkpoint，并仅移除 ledger 中两处旧 remote evidence；Git 历史中的旧 bytes
不被改写。

## 2. P1 根因

Finalizer 已把 checker-passed #117 owner result 投影为正确的 private #105 compatibility
payload。`cmd_finish_work()` 也使用该 projection 更新 ledger，而且
`artifact_sha256` 正确读取 task-local #117 owner artifact bytes。

但真实 remaining transaction 在 Draft PR 绑定后进入：

```text
build_final_archive_projection
-> validate_closeout_marketplace_artifact
-> read_json(marketplace-verification.json)
-> marketplace_verification_contract_errors
```

这里重新把 Interface 1.3 #117 owner artifact 当作 #105 legacy schema 1.0 校验，正常 happy
path 必然失败。后续 active projection、archive transaction 与 active interrupted-archive
recovery 也复用了同一错误读取路径。既有 real workflow regression mock 了整个
`cmd_finish_work()`，#105 order test 又 mock 了 final projection，所以没有执行到真实 consumer。

## 3. 实现 carryover

Runtime 新增仅在内存中传递的显式 private keyword
`_verification_projection`：

1. `validate_closeout_marketplace_artifact()` 无 projection 时保持 #105 legacy 行为，继续读取
   磁盘 legacy artifact；有 projection 时用它执行未放宽的 legacy
   schema/status/head/commands 校验。
2. 无论是否有 projection，artifact locator/existence 与 `artifact_sha256` 始终来自
   task-local `marketplace-verification.json` owner bytes；ledger evidence 仍与该 SHA 比对。
3. Private projection 贯穿 `build_final_archive_projection()`、
   `validate_closeout_active_projection()`、`execute_archive_metadata_transaction()`、
   `cmd_finish_work()` 与 `resume_active_archive_move()`。
4. Projection 不写盘、不进入 ledger/public DTO/task gate；#117 owner artifact/schema/checker、
   #105 transaction order/default behavior、public Interface 与 workflow route 均未修改。

## 4. Regression carryover

原 `test_real_workflow_verified_reentry_executes_remaining_finalization` 不再 mock 整个
`cmd_finish_work()`。测试现在真实进入 production consumer，并真实执行：

- finalizer-private compatibility projection；
- ledger machine evidence 更新；
- unique Draft identity validation；
- `build_final_archive_projection()`；
- archive 边界内的 `validate_closeout_active_projection()`。

测试只隔离 GitHub auth/remote identity、metadata commit、实际 archive/ready 等外部副作用。
它断言 primary/#118 ledger SHA 等于真实 #117 owner bytes SHA。另有负例覆盖 owner bytes
变化、reviewed HEAD mismatch、plan digest mismatch；legacy #105 regression 显式以“无
projection”调用 validator；active archive recovery 显式断言 private keyword 继续传入 active
projection 与 archive transaction。

当前验证结果：

- focused production/negative/legacy：5 tests，exit 0；
- 完整 `CloseoutTransactionContractTest`：107 tests，130.595s，exit 0。
- 完整 runtime suite：629 tests，208.155s，`OK (skipped=13)`，exit 0；
- canonical/dogfood/test `py_compile`：exit 0；
- canonical/dogfood runtime `cmp`：byte-identical，共同 SHA-256
  `1b9f1ad19e39ffe99a5e9590be6759075f9e5f1e47bd62d4fe040ebc18e8d0de`；
- canonical tests SHA-256：
  `9682b9940c1634af5a6efe544307fc0f59825503e333acd283f615e14cd80906`；
- `task.py validate`：exit 0；ledger cleanup 后 remote marketplace evidence count=0；
- `git diff --check`：exit 0；
- 最终 local HEAD、remote branch HEAD 与 Draft PR #160 head 仍全部为
  `85ab42837a44968d892f520614ab611becf5b8d5`；PR state/title/updatedAt 未改变。

## 5. Docs SSOT reconciliation

Docs strategy 保持 approved `ssot_first`，本轮结论为
`no_docs_update_needed`。实现继续以已经落地的 durable contracts 为主输入：

- `.trellis/spec/workflow/companion-scripts.md` 已要求 finalizer-only compatibility 绑定
  owner task/plan/HEAD/repository/exact transaction，同时规定 final projection 与 active
  projection 在 archive 前校验 task-relative artifact 和 ledger digest；
- `.trellis/spec/workflow/data-contracts.md` 已要求 verifier artifact locator 保持 task-relative、
  ledger digest 绑定 owner bytes，archive 后不得重验 owner artifact；
- `.trellis/spec/workflow/skill-package-contract.md` 已要求 generic #117 checker strict、private
  compatibility 不进入 public DTO；
- `.trellis/spec/workflow/workflow-contract.md` 与
  `guru-finalize-task/references/contract.md` 已固定 #105 transaction ordering 与 private state
  ownership。

本轮只是 runtime/test 对既有 SSOT 的 correctness 修复，没有新的 durable semantic delta；
本文件、失败现场与 checkpoint provenance 仅作为 task history，不成为第二份 behavior SSOT。
没有修改 workflow、preset、overlay、README、public package/interface/schema/example/eval corpus
或 upstream Finish family。

## 6. 精确 changed scope 与后续输入

本实现拥有：

1. `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
2. `.trellis/guru-team/scripts/python/guru_team_trellis.py`
3. `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
4. 本 handoff
5. 删除 stale `closeout-plan.json`、`marketplace-verification.json`、未跟踪
   `task-finalization-gate.json`
6. 只从 ledger primary/#118 删除旧 `remote_marketplace_verification`

并行主会话更新的 `agent-assignment.json` 不属于本实现，本轮不回退、不覆盖。

后续主会话必须基于新 task-work HEAD 重新生成：fresh Phase 2 evidence、task commit plan/commit、
独立 Branch Review、publication review/#116 `ready`、side-effect-free finalization preview、
新的 immutable plan/digest confirmation、以及按新 plan 执行的 #117 verification owner result。
在这些输入全部 current 且取得必要 confirmation 前，不得 push、创建/更新 PR、archive、Ready、
merge 或 Issue mutation。

## 7. Fresh trellis-check focus

- 真实 final/active/archive consumer 是否始终收到同一 private projection；
- legacy schema 校验对象与 owner artifact bytes/SHA owner 是否保持分离；
- 无 projection 的 #105 transaction/recovery matrix 是否完全不变；
- owner bytes、HEAD、plan mismatch 是否均 fail closed；
- canonical/dogfood parity、完整 runtime suite 与 stale checkpoint cleanup 是否纳入 current
  Phase 2 reviewed paths；
- Docs SSOT 是否继续满足 `ssot_first + no_docs_update_needed`，且本 task-history delta 没有被
  误写入 durable public contract。
