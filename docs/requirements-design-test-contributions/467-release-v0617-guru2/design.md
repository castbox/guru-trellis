# #467 发布准备设计增量

- `D467-01`：canonical manifest、根 README、workflow/preset README 与 public
  Docs 分别展示 repository、extension、CLI 和 Fork source 版本轴。
- `D467-02`：现有 `prepare_creation_inputs` 逐 checkout 检查提议身份；
  历史分支 JSON 只在占用提议 TaskRef 时阻塞；resource ledger 只读取
  提议 TaskId 的目录。canonical runtime 经 preset 投影到 installed runtime。
- `D467-03`：Architecture/RDT contribution 在 task branch 审查；首次
  full Branch Review 后串行 promotion；promotion 内容进入第二轮 Phase 2、
  Task Commit 和 full Branch Review。
- `D467-04`：preparation task 的 Completion 只覆盖 Stage 1。Stage 2
  重新冻结 main candidate；每项检查与 tag、smoke、Release、Issue closure
  绑定相同 candidate，不持久化动态 release 状态。
- `D467-05`：在 focused clean cell 外运行单一 predecessor existing-install
  upgrade cell，对比旧版 managed inventory 与新版 registry，并核对
  upgrade/reapply 后退役路径缺席、受管删除记录及冲突 sidecar。
