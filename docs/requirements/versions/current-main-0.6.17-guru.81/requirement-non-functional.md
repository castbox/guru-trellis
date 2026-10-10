# #468 Direct Source 兼容与活动重规划执行承接

版本：`current-main-0.6.17-guru.81`；状态：`active`；predecessor：`current-main-0.6.17-guru.80`。薄继承[不可变前驱](../current-main-0.6.17-guru.80/requirement-non-functional.md)全部有效合同与原对象证据。本版只承接已独立审查的 #468 增量；Architecture 当前继承 `docs/architecture/README.md` / `current-main-0.6.17-guru.81` / `active`，晋升 preimage 为 `.80`。知识晋升不表示软件发布、Backend 安装/重试/生产效果或任务完成；晋升产生的差异须 fresh Phase 2、Task Commit 与独立完整 Branch Review。

继承前驱非功能合同；不新增 source 拓扑、revision registry、授权持久化、永久结果历史或双读 adapter。completed execution checkpoint 仅服务当前原 owner 输出恢复与 current passed Check 消费，后者经原 owner retirement 端口删除。排除攻击/竞态/崩溃加固；完整 Upgrade/Release matrix 仍归专门 owner。
