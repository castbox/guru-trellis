# #588 Reconcile base 对象读取性能修复

## 来源与整体目标

唯一 Direct Source：[castbox/guru-trellis#588](https://github.com/castbox/guru-trellis/issues/588) 的当前正文。执行基线为 main 的 `1b2c30b4b1a326f2276c96f0d155605bf2cb1775`。#397、#579/#582、#567 仅提供既有摘要、传输及固定基线约束，不扩大本 Task 的关闭范围。

目标是解决正常 Reconcile 中全索引逐 blob 启动 Git 进程和同次 invoke 重复读取同一提交树的问题。完成必须同时具有实现、摘要兼容、实际正式调用链的性能/资源证据及可分发投影验证；进程数降低本身不代表完成。

## 整体范围与验收责任

| ID | 必须实现并证明的结果 |
| --- | --- |
| AC01 | 保持 Git 索引顺序、路径字节、blob 内容 SHA-256 行、gitlink mode/OID 行及最终摘要不变；独立 oracle 与旧正确基准一致。 |
| AC02 | 每轮 blob 读取只使用固定数量批量 Git 进程，同轮相同 blob OID 不重复读取或计算；gitlink 不读取子模块对象或访问远端。 |
| AC03 | 同次 invoke 对同一实际已提交树至多完整计算一次摘要，两份 owner result/checkpoint 的结构、身份、关系及摘要比较各自保留；当前树改变不能命中过期内容。 |
| AC04 | 普通整合、实施前 resolved baseline、审查后连续性、实施后 resolved candidate 及原提交后恢复分别沿既有入口/consumer 验证；同请求恢复原提交，无第二提交。无关 staged/unstaged/untracked 内容按原合同保留。 |
| AC05 | 批量传输不能重新引入 #579 的双向管道互等，不通过重试、放宽超时、截断输出或移除校验掩盖失败。 |
| AC06 | 实施前在 Delivery 设计固定可复现基准及摘要阶段/完整自动化链的最低性能改善与资源回归判据；原实现和修复实现按相同输入、工具、计时及重复测量口径验证。 |
| AC07 | 上万文件基准覆盖高重复内容及大量不同内容/较大对象，声明文件数、唯一 blob 数、总量、最大对象、各阶段时间、进程数与 Python/Git 峰值内存测量范围。原本可完成的大仓库不能因整批内容常驻内存回退为无法完成。 |
| AC08 | 功能回归覆盖普通/可执行/符号链接/空/二进制/重复 blob/已支持特殊路径/未初始化 gitlink，并验证真实 candidate→reconciliation→record→check→invoke 及其 checkpoint 消费。 |
| AC09 | canonical 源头、dogfood 和代表性 installed 正式链一致；声明平台投影、适用 reapply/drift、sidecar 与模式定向检查通过，完整 Release 矩阵不属于本 Task。 |
| AC10 | 整体 Completion 逐条核对上述责任，交付说明区分工具交付、软件发布与业务采用；PR 使用 Refs，只有完成审查后由 Closure 关闭 #588。 |

当前计划以一个完整 pull_request Delivery 覆盖 AC01–AC10。数值性能/资源判据由该 Delivery 在实施前依据完整基线测量固定，不在实施后放宽。

## 边界

只修改 Reconcile 原确定性 owner、必要测试/合同说明与受影响受管投影。公共 API、schema、typed exits、语义门禁、Task/Delivery identity、原恢复语义与 blob-backed mode-only 摘要语义保持。

不新增持久缓存、跨进程状态、通用 subprocess 框架、锁、对抗性输入、并发压力、默认追赶义务或业务仓升级。不修改无关任务或工作区，不把本 Task 扩大为 Release #575。
