# 本地 slice 验收与远端边界

版本：`current-main-0.6.17-guru.75`；状态：`active`；predecessor：`current-main-0.6.17-guru.74`。薄继承[不可变前驱](../current-main-0.6.17-guru.74/test-plan.md)；本版只承接修复后证据与既有机制说明，来源范围、owner与兼容退出不扩张，前驱有效合同及历史边界继续继承。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.75` / `active`。知识版本不表示软件发布。

本版验收结果仅引用[唯一 Test](../../../requirements-design-test-contributions/495-upgrade-version-families/test.md)：精确远端 Guru `ecd152add05dbeb6df1873f0917ca3a62914ca7a` 的 public/source_locked/provider、G1/native G8 实际来源回退、三格暂停新工作及 native oldwriter deferred 已完成；不把本版后继文档 HEAD 当成重跑。晋升 diff 仍须 fresh Phase2/TaskCommit/不同 reviewer 完整复审；Release、真实业务安装、完整累计矩阵未执行。
