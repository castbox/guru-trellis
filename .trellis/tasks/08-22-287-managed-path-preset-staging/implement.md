# #287 实施计划

1. 读取 #286 lifecycle inventory/runtime 与现有 preset manifest、installed manifest、overlay/package inventory，固定 managed asset id、source/target 和 sidecar/validation contract。
2. 重构 preset staging helper：增加 inventory 构建、managed-only materialization、path safety、计数/bytes 统计和空间预检；删除 whole-repo copy 及全量 tree-diff activation 依赖。
3. 将 action plan/preimage binding 接入 managed activation、backup/sidecar、partial recovery 与 installed validation，保持原有用户修改保护和失败路径。
4. 补充 targeted unit tests：unmanaged large content/nested repo 不被读取或复制，managed count/bytes 不随 repo 规模增长；space fail-before-write；initial/reapply/conflict/sidecar/recovery/update semantics。
5. 运行 canonical source tests，并使用 `apply.sh --repo .` 同步 dogfood；运行 `check-dogfood-overlay-drift.sh`、installed validation、preset/update/reapply checks 和一个代表性 clean isolated fixture。
6. 做完整 `origin/main...HEAD` Branch Review，修复 findings，确认 PR readiness、Issue scope ledger 与 #287 close 语义；提交并按流程请求 PR merge。#247 只在 #287 合并、关闭、main convergence 与 cleanup 后交接。
