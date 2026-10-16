# #579 Git 批量读取传输修复

唯一 Direct Source：[guru-trellis #579](https://github.com/castbox/guru-trellis/issues/579)。接受其当前正文全部修复范围、验收与非目标；目标 base/delivery 为 main，初始开发基线 404d3f4d7635b19fb2c9f0d6aa642e2f1bf925b4。

## 需求与验收

- R1：正常 Git 已提交树批量读取须完成；保持完整输入、完整对象输出、原顺序和树身份算法，不能用超时重试、截断或取消校验替代。
- R2：原 continuity recorder、checker 与公开 invoke 正式完成并返回 continuity_passed，checkpoint 按原 consumer 退休；单独 helper 成功不等于门禁完成。
- R3：普通文件、可执行文件、符号链接、空/二进制 blob、重复 OID 和既有 gitlink 表示保持原语义。独立逐对象读取 oracle 与修复身份一致。
- R4：仅修改 canonical 原读取 owner、必要测试及受影响分发；完整匹配 installed 公开链验证和适用 reapply/drift 检查证明投影。原业务任务与其他 worktree 的 HEAD/index/refs 均保留。
- R5：测试用正常真实 Git fixture 或严格等价输入，保留原失败、传输反事实及修复结果；不把平台特有失败强制成全平台红测。

## 已确认因果与验证边界

原现场正常提交 b88b73ca 的 13,085 个请求共536,485字节，Python向stdin写入与Git向stdout写入互等。独立 C pipe/poll/write 复现可写通知后EAGAIN；文件输入和非阻塞诊断输出162,189,132字节且SHA-256相同。只确认当前macOS环境，不推断所有macOS版本或底层上游归属。修复需在隔离fixture正式链验证，不干预原业务会话。

## 非目标

不修改 Reconcile 语义、业务代码、CI/CD、业务安装或会话资源，不增加通用进程框架、锁、对抗测试、重试协议或完整 Release 多平台矩阵。#567、#578、#397按原责任保持。源设计约束由 design.md 唯一处置，PRD不复制实现方案。
