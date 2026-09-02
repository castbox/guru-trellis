# #338 Design contribution

- `D338-01`：`finalization_existing_pr_recovery_context()` 保持 reprepare、fresh strict-ancestor、bound recovery
  的现有优先级，并在普通 preflight 前增加一个窄的 ordinary/push-content/unbound classifier。
- `D338-02`：classifier 先用 current transaction builder 反向校验完整 plan identity，再解析唯一 live PR、
  remote HEAD、close scope 与 metadata；只有三方 HEAD equal 时以 `allow_equal` 复用 existing recovery
  primitive，strict ancestor 不通过该 ordinary 分支接管。
- `D338-03`：preview recovery shape 增加 invocation-local `metadata_comparison`，保留 live title/body 与逐字段
  byte-equality facts，使 execute 能检测结果布尔值不变但原始 metadata 已漂移的情况。
- `D338-04`：conversion 复用 schema 3.0 builder，把 ordinary preimage 原位投影为
  `existing_pr_recovery/bind_pr`，写入 exact `pr`、`adopted_pr`、initial Draft/Ready 与 equal publication HEAD；
  public schema、exit 和 registry 字节不变。
- `D338-05`：executor 在任何剩余外部 mutation 前重新分类 live facts、与 preview 做 exact equality、写入一次
  converted transaction，然后复用现有 preflight、metadata convergence、archive、push_archive 与 Ready owner。
- `D338-06`：conversion 后所有 retry 进入现有 bound recovery；metadata convergence 后的 exact payload、scope、
  PR identity 与 HEAD 仍由 current live reread 验证。
- `D338-07`：canonical package 是唯一实现 source；preset apply 生成 installed/platform copies。Architecture
  仍为 `no_architecture_impact`，因为 owner、persistence type、public DTO 与 dependency direction 均未改变。
