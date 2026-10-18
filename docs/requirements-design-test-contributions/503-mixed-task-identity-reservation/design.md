# #503 设计贡献

修订候选，current .75未变；依据task design与live职责评论。

- D503-CLASSIFY：共用JSON/object/id/locator确定性读取，reservation仅投影id/ref。非身份字段不参与占用；坏活动身份拒绝。
- D503-RESERVE：保留worktrees/branch/ledger范围，先唯一性再selected strict current校验。inventory/migration完整分类及创建后target严格校验保留；无第二索引。
- D503-DIAGNOSTIC：同一stop消费最小locator/remediation，旧最小output兼容，不持久化扫描/授权/session。
- D503-DISTRIBUTION：canonical正式Fork lock绑定已合并5c760463680ffc10a3f26957b330c57a4b0c3ff8和成功CI 37735554354；核对parents/tree，适用pin、official/dogfood投影、apply及实际安装矩阵一致。
- D503-EXIT：current-only与Fork单写owner不变；保留有inventory/migration消费者的完整分类，删除仅有越界占用消费者的冗余分类；不恢复legacy lifecycle、不新增迁移器。

expected-current .75；promotion后变化fresh检查。架构承接ARCH-CUR-049/ARCH-DOM-034/ADR-017/018，target_native职责拆分，无新增ADR或持久状态。
