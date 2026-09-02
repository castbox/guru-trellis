# #338 Design contribution

- `D338-01`：`finalization_existing_pr_recovery_context()` 保持 reprepare、fresh strict-ancestor、bound recovery
  的现有优先级，并在普通 preflight 前增加一个窄的 ordinary/push-content/unbound classifier。
- `D338-02`：classifier 先用 current transaction builder 反向校验完整 plan identity，再解析唯一 live PR、
  remote HEAD、close scope 与 metadata；只有三方 HEAD equal 时以 `allow_equal` 复用 existing recovery
  primitive，strict ancestor 不通过该 ordinary 分支接管。
- `D338-03`：preview recovery shape 增加 `metadata_comparison`，保留 live title/body 与逐字段 byte-equality
  facts；conversion 将该原始 comparison 和 `metadata_update_required` 决策绑定到 owner-private
  `adopted_pr`，使 `bind_pr` 恢复能检测缺失、不一致或原始 metadata 漂移。
- `D338-04`：conversion 复用 schema 3.0 builder，把 ordinary preimage 原位投影为
  `existing_pr_recovery/bind_pr`，写入 exact `pr`、`adopted_pr`、initial Draft/Ready、equal publication HEAD 与
  原始 metadata decision。Private schema 3.0 仅增加 optional fields，schema id/version、public schema、exit、
  registry 与旧 strict-ancestor transaction 兼容性不变。
- `D338-05`：executor 在任何剩余外部 mutation 前重新分类 live facts、与 preview 做 exact equality、写入一次
  converted transaction，然后复用现有 preflight、metadata convergence、archive、push_archive 与 Ready owner。
- `D338-06`：equal-HEAD transaction 在 `bind_pr` 阶段先验证原始 metadata binding；推进到 `archive` 后所有
  retry 进入现有 bound recovery。若 PR edit 已成功但 transaction 尚未来得及推进，`bind_pr` retry 仅接受
  原始 binding 或 `metadata_update_required=true` 时已精确等于 current Publication 的收敛后 payload，后者零
  重复 edit；其他 title/body、scope、PR identity 与 HEAD drift 仍由 current live reread 阻断。
- `D338-07`：canonical package 是唯一实现 source；preset apply 生成 installed/platform copies。Architecture
  仍为 `no_architecture_impact`，因为 owner、persistence type、public DTO 与 dependency direction 均未改变。
