# #454 C3 Checkout Acquisition Provenance Design Contribution

状态：`reviewed_promoted`。采用 `target_native`，关联
`architecture-contribution-454-task-lifecycle-state-model-c3-provenance-v1`；
expected current 为 `.60`，promoted successor 为 `.61`。

- `D454-C3-10`：`checkout_acquisition.py` 在 transaction-created linked worktree 的 `git_dir` 下创建 `guru-checkout-acquisition-provenance.json`。payload 为 closed schema/versioned object，并复用 acquisition plan/result 的 exact identity 与 ownership projection。
- `D454-C3-11`：`recover_checkout_acquisition()` 先重建 fresh exact result，再对 created-worktree disposition 要求 marker key set、value type 与 value 全部 exact match。different-path、same-path replacement、missing marker、invalid JSON、extra/missing field 或任一 identity mismatch 统一返回 `acquisition_result_mismatch / transaction_provenance`。
- `D454-C3-12`：`provision_linked_worktree()` 在 post-create validation 后写 marker；存在 `post_acquire` 时先删除 marker，再调用 consumer。marker 写入/删除失败或 callback 失败进入既有 bounded rollback；callback 已接受资源后不再触发 marker-retirement failure。

Marker 不是长期 owner 或第二 store。`git worktree remove` 自然删除原
administrative directory；replacement checkout 无法继承 marker。`ADR-015` 已覆盖
保守 ownership 与 framework-extension boundary，因此不新增 ADR。
