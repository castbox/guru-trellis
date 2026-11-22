# #896 验证记录

| 验证 | 实际观察 |
| --- | --- |
| T896-01 | 隔离验收使用匹配 preset 的四个公开入口、两父合并和本地裸 Git 仓库，通过 Merge、Completion、Closure、Finish。运行目标树中的实际交付内容。归档保留原 TaskId、generation、Delivery 和终态结果。源 Issue 在测试开始时已经关闭。测试只观察到归档 PR 合并。 |
| T896-02 | 回归构造真实合并冲突。Candidate 绑定 PR head，实际内容由合并提交定位。继承所选 Task 的无关 PR 与已接受新范围的旧 PR 均返回缺口，未改原 Delivery。 |
| T896-03 | 回归核对相同结果重入和历史 CI 含义。Merge 的手动恢复测试组 15 项通过，包含已有 Publication 的 12 项回归。隔离归档旅程 1 项通过。 |

测试使用 GitHub 接口替身和测试用语义判断。另从实际 GitHub 读取了 #828 的合并状态、PR head、目标、merge commit 及 3 项 CI 结果。从 Git 核对了该范围内新增的原 Task 记录、Delivery 和接受范围。本次验证未写入 #826 的 Task，也未执行完整多平台发布矩阵。
