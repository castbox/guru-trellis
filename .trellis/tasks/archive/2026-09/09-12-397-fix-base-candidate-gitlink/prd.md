# #397 基线候选 gitlink 身份修复

## 目标与来源

使包含合法、未初始化 gitlink 的父仓库完成基线候选身份计算及验证，不下载子模块内容。
需求 authority：<https://github.com/castbox/guru-trellis/issues/397>。
关闭范围仅为 #397；#172、#186、#376 是背景引用，业务 Issue #74 不进入本任务。

## 当前问题

初始基线中，`trellis/skills/guru-team/packages/guru-reconcile-task-base/runtime/common.py:166`
的 `index_tree_digest` 对全部 stage-0 entry 执行 `git cat-file blob`。
`runtime/execute.py:46` 在执行验证命令前调用该函数；mode `160000` 的 OID
指向 commit，导致合法 gitlink 提前失败。临时候选和持久整合共用此函数。

初始真实 Git fixture 加入未初始化 gitlink 后复现
`candidate_failed / repository.index / git cat-file ...: bad file`。
复现前后 fixture HEAD、索引条目、refs 和注册 worktree 列表一致，未访问网络。
该证据只证明修复前失败，不表示修复已完成。

当前提交已修复索引 producer，但 Branch Review 的 `tree_identity` 仍跳过 gitlink。
正常 Reconcile 输出进入 `base_continuity` recorder 后，同一提交被重算为不同摘要，
返回 `stale_identity / candidate_tree_sha256`。R4 必须覆盖这个既有下游 consumer，
不能只验收到 Reconcile 的输出。

## 需求与验收

| ID | 需求 | 验收结果 |
| --- | --- | --- |
| R1 | 在既有身份 owner 中使用索引记录的 gitlink OID，不将其作为 blob 读取 | 合法、未初始化 gitlink 候选返回 clean 与非空身份；验证命令执行并返回记录 |
| R2 | gitlink 指针必须参与身份 | 相同索引重复计算字节一致；正常更新 gitlink 指针后身份不同；本地缺少子模块 commit 对象仍通过 |
| R3 | 保留普通文件、可执行文件和符号链接现有计算行为 | 三种 blob-backed mode 的内容改变仍改变摘要；不含 gitlink 的树与旧算法结果逐字一致 |
| R4 | 临时候选、持久整合及 Branch Review 已提交树重算使用同一行表示 | 真实 fixture 中三者身份字节一致、整合父顺序正确；实际 Reconcile 输出进入 Branch Review recorder/checker/invoke 并返回 continuity_passed |
| R5 | 明确既有短期证据的适用边界 | 无 gitlink 的既有成功摘要不失效；旧实现无法为含 gitlink 的树生成成功候选证据；含 gitlink 的失败尝试重新计算，不迁移或补造摘要 |
| R6 | 用真实 Git 状态验证无额外任务副作用 | candidate 前后任务 HEAD、index、refs 不变；验证失败退出码被记录；成功及原缺陷失败后的临时 worktree 均清理 |
| R7 | 从 canonical 交付并验证安装副本 | canonical 与 dogfood package 测试、一次代表性干净安装的候选调用、preset reapply 与 drift 检查通过 |

## 范围外

- 不修改业务 W2、Process Analytics、业务子模块、凭证或远端配置。
- 不调用 submodule init/update/fetch，不发布、不升级业务仓、不执行完整多平台 Release 矩阵。
- 不改变 workflow routing、planning validity、双时钟、resume target、公开 DTO 或 schema。
- 不扩展既有 blob-backed entry 的纯 mode-only 身份语义；本次保留其原算法。
- 不增加重试、锁、兼容双读、门禁绕过、恶意输入或并发压力场景。

## Docs SSOT Plan

策略：`delta_first`。本 PRD 拥有任务需求；`design.md` 拥有技术选择与兼容边界；
`implement.md` 拥有实施顺序与验证清单。实现阶段更新 package 的
`references/contract.md`，将 Git entry 与失败证据重算规则放在唯一候选 owner，
并经 preset 投影至 dogfood。最终 Phase 2 前完成该合并。
Branch Review 的 package contract 只引用这一候选表示并说明其 committed-tree consumer
责任，不另建算法 authority。跨 owner 回归放在既有 `test_base_continuity_integration.py`。

共享 RDT/CURRENT、Architecture、workflow 和通用 spec 不增加新的 authority：本次修复
既有 owner 的类型处理缺陷，不增加 domain、command 或 route。若实现发现必须改变这些边界，
停止扩展并回到对应语义 owner。

## 未决问题

无阻塞需求问题。实现、安装验证及生产效果尚未完成；业务环境验证不属于本任务。
