# #713 测试贡献

完整策略见 [proposed test](proposed/docs/test/current/task-delivery-lifecycle.md) 的 T713-01..09。稳定 test 身份保留，按当前 AC1–AC4、缩减后的 AC6–AC8 与 AC9 核对已有 source、组件、原命令、consumer、匹配安装、synthetic 与局部 native 的适用性；仅刷新真实变更依赖。T713-04 / AC5 的新增首次正确完整 native 链取消，T713-06..09 对应 C2–C5 的追加 native、旧 fixture 接续和重复安装取消。

本贡献准备完整预期，不记录未发生的通过。原 T531/T638 前置和最终质量链保持。原首失败、部分成功、污染、未知退出码、H2 非通过、R5 方法不足及 execution_error/fitness_regression 保持；R3 仅 runtime 准备通过，未启动 native；旧 clean 后续损坏不归因 installer，不称当前可用。源码维护诊断不计 public-only，取消项不记 passed，也不形成必需补证支线。实际观察截止于原命令/run 与本 D1 验证记录，后续正式 Check 和交付结果由原 owner 承接。
