# #579 设计

## 唯一责任与机制

原 `guru-review-branch/runtime/common.py:tree_identity` 继续拥有已提交树身份计算；`record.py` 和 `validate_gate` 继续消费同一函数。仅将完整 OID 请求写入调用内 `tempfile.TemporaryFile()`，`seek(0)` 后交给原 `git cat-file --batch` 的 stdin。保留 stdout/stderr PIPE 与现有解析和错误分支。with 退出关闭文件；临时文件无业务 identity、授权或持久化 consumer。

消除的因果依赖：父进程不再向子进程 stdin pipe 阻塞写入，因而可持续读取 Git stdout；没有重试、忙轮询、时间放宽、fallback 或第二算法。文件 I/O 或 Git 非零/不完整输出保持失败，不将部分结果判为成功。

## 身份与兼容

`ls-tree -r -z` 顺序、完整请求（包括重复 OID）、blob 内容 SHA-256、路径 NUL 行、gitlink mode/OID 行及最终摘要保持不变。普通/可执行/符号链接仍读 Git blob，不追踪 symlink filesystem。原公共 DTO、schema、typed exit、checkpoint/retirement、Reconcile 及语义 review 不变；没有旧新双读或迁移协议。

## 源设计约束处置

| 源 | commitment | 处置与落点 | 理由/影响 |
| --- | --- | --- | --- |
| #579 修复范围1 | 原读取 owner 最小传输修复 | retain：本章 TemporaryFile 输入 | 原机制就地替换，无新框架 |
| #579 修复范围2 | 全对象/顺序/树身份与支持类型不变 | retain：身份章节与独立oracle回归 | 不改变算法、公共API |
| #579 修复范围3 | 原 recorder/checker/formal exit/recovery 保留 | retain：原函数两消费者及公开链回归 | 不将诊断当门禁 |
| #579 修复范围4 | canonical/受影响投影/必要说明 | retain：implement.md 分发验证 | 不做无关工具升级 |
| #579 非目标 | 不改变业务/CI/CD/Reconcile/Release职责 | retain：PRD非目标与全diff review | 不扩修 |

## 架构适用

按独立 Architecture owner 的实际 purpose-specific output 承接 current baseline、constitution 与 change-contract。机制仅改变调用内请求传输，不建立新owner/state/public contract。若其正式结论为 no_architecture_impact，按现有合同不创建 contribution/ADR/project-check；本技术设计是此局部决策的唯一规划落点，长期说明由必要 Docs consumer承接。任何新增公共接口或持久化必须回原owner，不自动扩大范围。

## 验证

1. 真实 Git fixture 产生跨管道容量的批量输入和大对象响应；独立逐对象 oracle 给出相同树摘要，覆盖空/二进制/重复OID/模式/symlink/gitlink。
2. 原读取在当前受影响环境的失败证据保留；新 fixture 通过原 continuity recorder→checker→invoke，监督进程有时限，失败仅终止自身进程，不留下挂起子进程。平台无原失败时只记录本机边界，不伪报复现。
3. 原正式结果 identity、continuity_passed 和checkpoint退休正常；Git HEAD/index/refs保持受测操作允许的精确结果。
4. 匹配 canonical/installed tests 与分发/reapply/drift；当前仓库旧dogfood与canonical差异先隔离，不将无关全量升级并入修复。具体分发采取原installer支持路径，无法证明的投影明确为边界，不手工patch活跃业务安装。

## 风险与回滚

临时文件增加一次请求落盘，输入规模仅OID列表；对象输出/内存解析保持既有行为，本任务不优化全树内存。最小回滚为原函数输入传输及对应测试/说明；回滚会恢复已知阻塞，不作为通过状态。真实业务仓升级、原会话完成及完整Release矩阵不是本Task完成证据。
