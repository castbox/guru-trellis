# MIGRATION-896 接收缺少 Publication 的已合并 PR

采用同一份完整 Guru Team workflow 和 preset。新入口
`guru-merge-task-delivery:delivery_adopt_merged_pr` 及其消费者需要匹配的
Merge 和 Completion 包。现有 `delivery_merged_recovery` 继续处理已有
Publication 的双父合并。公共 Task2 记录和 DeliveryFact 使用原 API。

已有项目按官方方式预览和应用匹配的 workflow，再重应用完整 preset。
单 checkout 工具更新保留当前 Task 和 session 时，使用原
`guru-upgrade-tools`。运行该安装的 discovery 检查 Merge profile，并按
原安装 owner 处理受管文件的 `.new`、`.bak`。

进入新 profile 前，显式选择仓库、已合并 PR 和原 Task/Delivery。
Merge 核对 Git 归属和实际合并情况。收到 `delivered` 后进入现有
Completion、Closure 和 Finish。历史 CI 保持原状态，验收依赖仍适用
的实际内容和证据。遇到归属缺口时，使用本次结果指出的原事实补齐后
重入相同对象。
