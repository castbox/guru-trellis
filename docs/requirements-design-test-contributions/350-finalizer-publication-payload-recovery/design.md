# #350 Design Contribution

`D350-01`: 原 topology-inapplicable allowlist 保持不变；
`provenance_tail_transaction_rebind_base_evolution_tail_parent()` 必须先证明
single legal provenance tail 与 exact base evolution 的组合拓扑，才允许
Publication title/body mismatch 继续进入 recovery。

`D350-02`: 组合拓扑成立后继续调用现有
`classify_existing_pr_recovery()`，由该单一 owner 负责 live PR metadata
comparison、scope 校验、strict ancestry 与 Ready/Draft 语义；pure base
evolution 与 direct tail 不单独放行 payload drift。

`D350-03`: 执行顺序、current-plan-bound transaction、metadata convergence、
archive、Ready handling 与 same-plan retry 均继续由现有 recovery transaction
engine 管理，不新增 public I/O、typed exit、transaction stage/schema 或新的
PR recovery classifier。
