# #350 Test Contribution

`T350-01`: real base-evolution-plus-tail recovery fixture 覆盖 predecessor
body 与 current fresh Publication body 不同；preview 返回
`strict_ancestor`、`push_required=true`、`metadata_update_required=true`，并
保留精确 PR identity 与 Ready action。

`T350-02`: real pure-base-evolution fixture 覆盖 Publication payload mismatch，
必须在 PR 解析与 mutation 前返回
`provenance_tail_transaction_rebind_invalid`；metadata-equal、direct-tail 与
#338 equal-HEAD 回归保持通过。

`T350-03`: 非法 tail、多 tail、非 provenance 文件、业务 delta、scope/branch/
HEAD/PR/transaction drift 与 stale state 保持 fail-closed。

`T350-04`: execution/retry 继续断言 transaction-before-mutation、current push
一次、PR create 零次、metadata edit 不超过一次，且 same-plan retry 不重复
已完成副作用。

`T350-05`: 运行 source/task/RDT 文档验证、JSON/YAML 解析、ownership、drift、
package/task 与 `git diff --check`；完整 Release/Throwaway、PR #337/#333
transaction 与 Issue mutation 不在本测试贡献范围内。
