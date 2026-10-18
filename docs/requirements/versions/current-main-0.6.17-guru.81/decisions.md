# #468 Direct Source 兼容与活动重规划执行承接

版本：`current-main-0.6.17-guru.81`；状态：`active`；predecessor：`current-main-0.6.17-guru.80`。薄继承[不可变前驱](../current-main-0.6.17-guru.80/decisions.md)全部有效合同与原对象证据。本版只承接已独立审查的 #468 增量；Architecture 当前继承 `docs/architecture/README.md` / `current-main-0.6.17-guru.81` / `active`，晋升 preimage 为 `.80`。知识晋升不表示软件发布、Backend 安装/重试/生产效果或任务完成；晋升产生的差异须 fresh Phase 2、Task Commit 与独立完整 Branch Review。

继承 ADR-005/009/011/012/015/016 与前驱全部有效 decisions；本次 target_native 增量不改变 TaskId/source/lifecycle 状态、owner/single-writer、GAP lifecycle 或 compatibility exit，无新 ADR。单一 aggregate schema 2.0 的兼容合同由原 activation package 拥有，不增加版本分派或第二 parser。
