# #350 Test Contribution

- real base-evolution-plus-tail recovery fixture 覆盖 predecessor body 与 current fresh Publication body 不同，preview 返回 `strict_ancestor`、`push_required=true`、`metadata_update_required=true`。
- real pure base-evolution fixture 覆盖 Publication payload mismatch，必须在 PR 解析与 mutation 前返回 `provenance_tail_transaction_rebind_invalid`。
- 保留 metadata-equal、非法 tail、业务 delta、scope/branch/HEAD/transaction drift 的 fail-closed 覆盖。
- execution/retry 继续断言 transaction-before-mutation、current push 一次、PR create 零次、metadata edit 不超过一次且 retry 不重复。
