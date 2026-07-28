# Issue #118 finalizer owner evidence 兼容投影修复交接

## 1. 范围与根因

- Task：`.trellis/tasks/07-26-118-guru-finalize-task`。
- Reviewed/content-pushed HEAD：`d7308d4aeaa3228d7650b93821ac7b4269ec5b38`。
- Immutable plan：`closeout-plan:21d053f5e458f2cf1b8f4cfd492ea668ddb7e651893dd832a927bc6c000a300b`。
- Current #117 evidence：`marketplace-verification.json`，
  `verification_ref=extension-verification:4e9fea60ad8fdeceaad802eb`。

正常 verified re-entry 已通过 finalizer 的 #117 owner checker，但
`cmd_execute_finalization_transition()` 把 Interface 1.3 owner artifact 原样传给 #105
legacy `closeout_passed_marketplace_evidence()`。后者只接受 schema 1.0
`status/verified_head/remote_head/steps/assets`，因此在 evidence commit、Draft PR 与 archive
前以 `Cannot record invalid marketplace verification.` 阻断。

本 handoff 只记录 implementation delta，不替代 Phase 2、Branch Review、publication review
或 finalization gate，也不授权 commit、push、PR、archive 或 Issue mutation。

## 2. 实现

新增 finalizer-private deterministic compatibility projection：

1. 只接受 finalizer 已取得的 `(owner payload, owner checker result)`；要求 checker
   `status=ok`、`typed_exit=verified`、workflow mode、verification ref、owner digest 与可选
   finalization plan ref 精确匹配。
2. 再绑定 owner artifact regular-file 内容、task、plan、repo、remote、branch ref、reviewed
   HEAD、remote HEAD 与 `execution.status=passed`；任何 drift 都 fail closed。
3. 将 #117 `execution.commands` 投影为 legacy `steps`，从 checker-bound
   `asset_expectations` 精确选择 workflow 与三个 legacy schema digest；投影结果先经过未修改的
   `marketplace_verification_contract_errors()`。
4. 只有 `marketplace.required=true` 的 published transition 才把该私有投影交给 #105 engine；
   not-required 路径不制造 legacy verification payload。
5. 未修改 `closeout_passed_marketplace_evidence()`：ledger `artifact_sha256` 仍读取真实
   Interface 1.3 owner artifact path bytes，不对临时 compatibility payload 求 hash。

未放宽 #105 generic transaction、#117 generic checker/artifact/schema/public DTO，也未修改
upstream Finish Skill/Command/Prompt、global workflow、preset overlay、#119/#132 或排除的
恶意 actor、并发、TOCTOU/fault-injection 范围。

## 3. 回归与 live 证据

新增 real regression 从 #117 recorder/checker 生成 `verified` owner artifact，经过 finalizer
gate `published` transition 进入 remaining #105 engine boundary，并断言：

- compatibility payload 通过原 legacy validator；
- owner artifact SHA 与 ledger evidence SHA 完全相同；
- ledger `verified_content_head`、`remote_head` 精确等于 reviewed/remote HEAD；
- primary issue 与 close issue 两处 machine evidence 均保持上述 identity。

当前 task artifact 的只读 live projection 结果：

- legacy contract errors：`[]`；commands：6；
- owner file SHA-256 与 ledger candidate SHA-256 均为
  `a496b9bc9d5b4395ca3255f1da47e48fa7c7f3dafe23ebdea66c9bd4d8f78cb5`；
- verified/remote HEAD 均为 `d7308d4aeaa3228d7650b93821ac7b4269ec5b38`。

验证结果：

- focused real/negative re-entry：5/5，exit 0；
- 完整 `CloseoutTransactionContractTest`：106 tests，128.864s，exit 0；
- 完整 runtime suite：628 tests，236.968s，`OK (skipped=13)`，exit 0；
- canonical/dogfood Python `py_compile`：exit 0；
- canonical/dogfood runtime `cmp`：byte-identical，共同 SHA-256
  `abae4f48c8335d6b9b4a99a218ac23bb3412eb311ee5ad1e23b5b707504e0e7d`；
- `git diff --check`：exit 0。

## 4. Docs SSOT 与修改文件

Docs SSOT Plan 继续采用批准的 `ssot_first`。本 finding 的 durable contract 已存在：

- `skill-package-contract.md` 明确 generic #117 checker 保持 strict，finalizer 负责
  owner-private compatibility；
- `companion-scripts.md` 明确 finalizer compatibility 必须先绑定 owner
  task/plan/HEAD/repository 与 exact transaction；
- `workflow-contract.md` 明确 verification re-entry 只消费 current owner evidence。

因此本轮为 runtime/test 对既有 durable SSOT 的 correctness 修复，结论为
`no_docs_update_needed`；没有新的 task delta 需要合并到 durable docs。本文件只保留 task
history，不成为第二份 behavior SSOT。

本实现拥有的 changed paths：

1. `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
2. `.trellis/guru-team/scripts/python/guru_team_trellis.py`
3. `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
4. 本 handoff

既有 closeout plan、finalization gate、marketplace verification、publication/review evidence
均未被本实现修改、重写或删除。

## 5. trellis-check 交接

Fresh `trellis-check` 应重点复核 compatibility projection 的 owner-check binding、真实 owner
artifact SHA 进入 ledger、published transition 的 exact HEAD，以及 legacy #105 matrix 无语义
变化。完整 runtime 已跑；package/eval 全量与 clean throwaway install/update/reapply 未在本轮
重复执行，应由 check 阶段按当前最终 diff 决定是否补跑并如实记录。当前无已知实现 blocker；
剩余生命周期 evidence 会因本轮 code delta stale，必须重新生成后才能继续 finalization。
