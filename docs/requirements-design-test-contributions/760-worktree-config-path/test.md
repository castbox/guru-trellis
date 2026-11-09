# worktree 配置路径测试贡献

Status：promoted。完整目标为 [runtime-location](proposed/docs/test/current/runtime-location.md)，
保留 `RDT-TST-RUNTIME-LOCATION`、T718 策略与所有既有观察，追加 T760-01—04。

本次本地公开入口/真实Git行为与source机械验证已执行，实际命令、结果和边界见完整Test目标。
修复版原tools更新、installed validator、drift与sidecar实际观察已补入完整Test目标；完整Release仍未验证。
证据到达后只更新本候选的独立观察，不回写历史失败或把 #718 的通过当 #760 证明。
实际代码、schema、公开入口、计划/目录/注册/后继读取需分别对齐；测试数量、文本命中
和 helper 成功不能替代公开 consumer 行为。完整多平台安装/升级/Release、业务采用及
真实 Codex 清理不属于本项验证；formal Check/Review和Completion由原 owner执行。

原 RDT owner在实际 candidate_checked 后重读真实目标、整合并写回/读回。定义修订为
`worktree-config-path-760`；实际 current 完整单元：[runtime-location](../../test/current/runtime-location.md)。
本贡献保留来源，不替代普通查询的 current 正文；最终实际候选重绑与质量链由原 owners 承接。
