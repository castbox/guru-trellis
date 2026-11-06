# #713 设计贡献

完整拟写见 [proposed design](proposed/docs/design/current/task-delivery-lifecycle.md)。D713-01..05 将导航、source 输入、Candidate 事实、诊断/恢复、eval 与 matching 分发放回原 owner，复用 D531/ADR-028/原 recorder 决定。原 Git-free 与旧成功 consumer 边界保持，不建立新状态、算法或兼容 parser。

本项采用仍适用的已有定向和匹配安装结果，仅刷新真实变更依赖。取消新增 native 链、非等价 native 代表、R5 方法补证、旧 fixture 接续与为此重复安装；原失败和证据不足保持。Architecture 独立评估、候选 Check、最终晋升/readback、after 重绑和最终质量链仍消费实际原出口；本贡献不代写 Architecture。
