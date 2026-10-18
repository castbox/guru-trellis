# #467 发布准备需求增量

- `R467-01`：目标仓库 tag 为 `v0.6.17-guru.2`，extension 为
  `0.6.17-guru.43`，CLI/core 为 `0.6.17`，Fork source 保持
  `8336e78b8fafe2a4bc4ea3d01815a61cf4f08983`；正式发布以 exact candidate
  的 tag 和 GitHub Release 为准。
- `R467-02`：TaskId 创建检查只因目标 TaskId、TaskRef 或目标 resource
  ledger 冲突而阻塞；其他任务的旧 active/archive 重复、无关分支 JSON
  错误和旧 ledger schema 不阻塞新身份。
- `R467-03`：准备 PR 使用 `Refs #467`，合并、Completion、Closure 和 Finish
  后仍保持 Issue 开放；正式发布单独完成累计 candidate gate、tag、smoke、
  Release 和 Issue closure。
- `R467-04`：正式候选以 predecessor `v0.6.17-guru.1` 到 post-Finish
  `origin/main` exact commit/tree 的完整 diff 为范围，不以历史切片证据
  替代；完整多平台矩阵和业务仓生产安装不属于本 Issue 的通过声明。
- `R467-05`：从 predecessor 既有安装升级到新版本时，旧版本拥有且
  新版本退役的 Skill、命令、package 文件和平台投影须删除；被用户修改的
  退役文件须保留并报告冲突，不得静默删除。
