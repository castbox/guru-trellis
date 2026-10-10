# #468 Direct Source 兼容与活动重规划执行承接

版本：`current-main-0.6.17-guru.81`；状态：`active`；predecessor：`current-main-0.6.17-guru.80`。薄继承[不可变前驱](../current-main-0.6.17-guru.80/design-main.md)全部有效合同与原对象证据。本版只承接已独立审查的 #468 增量；Architecture 当前继承 `docs/architecture/README.md` / `current-main-0.6.17-guru.81` / `active`，晋升 preimage 为 `.80`。知识晋升不表示软件发布、Backend 安装/重试/生产效果或任务完成；晋升产生的差异须 fresh Phase 2、Task Commit 与独立完整 Branch Review。

[设计增量](../../../requirements-design-test-contributions/468-direct-source-replanning-compatibility/design.md)拥有 D468-01..04。原 guru-activate-task 独占 resume_execution、identity-only recover_execution 和完成结果；workflow 只承接 approved/execution_resumed，原 Check 在 current passed 后调用原 owner retirement 端口。原 activate/recover_activation payload 与语义保持，受控 consumers 同次更新单一 schema 2.0。
