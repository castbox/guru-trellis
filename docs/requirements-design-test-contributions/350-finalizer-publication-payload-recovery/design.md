# #350 Design Contribution

原 topology inapplicable allowlist 保持不变。`publication` mismatch 只在 `provenance_tail_transaction_rebind_base_evolution_tail_parent()` 证明 single legal provenance tail 与 exact base evolution 的组合拓扑后继续调用 `classify_existing_pr_recovery()`；pure base evolution 不得单独放行 payload drift。后者继续拥有 live PR metadata comparison、scope 校验、strict ancestry 与 Ready/Draft 语义。执行顺序和 retry 仍由现有 bound recovery transaction engine 管理。
