# 接收已合并 PR 并接续原 Task 归档

## 1. 来源与术语

| 来源 | 角色 | 用途 |
| --- | --- | --- |
| [Issue #896](https://github.com/castbox/guru-trellis/issues/896) | Direct Source | 行为要求和验收 |
| [PR #828](https://github.com/castbox/guru-trellis/pull/828) 与 [Issue #826](https://github.com/castbox/guru-trellis/issues/826) | 历史证据 | 已实际合并，原 Delivery 缺少发布记录 |
| [Issue #557](https://github.com/castbox/guru-trellis/issues/557) | 兼容来源 | 已有正式 Publication 的手动合并恢复 |

Publication 是原发布职责写入的公开结果。这里的接收指把已经发生的合并归到已有 Delivery，并记录交付事实。

## 2. 背景与问题

现有恢复要求已有 Publication。#828 已通过双父提交并入 main，#826 已关闭，原 Task 和 Delivery 可从 Git 找回。现有入口遇到缺失 Publication 时停止，原 Task 无法进入正式归档。

## 3. 目标与范围

首批接收可查证的同仓双父合并 PR。沿用原 TaskId、generation、Delivery 和接受范围，随后按现有 Completion、Closure、Finish 收尾。保持原 #557 恢复行为及 GitHub 历史。

## 4. 真实场景

S1 用户显式选定仓库、已合并 PR 和原 Task/Delivery。能唯一归属时，记录原 Delivery 的实际交付，并进入验收。源 Issue 已关闭且验收通过时，核对源状态并归档。
S2 选定对象与 Git 或 GitHub 证据不匹配，或证据不足以证明归属。返回具体缺口并保持 Delivery 状态。
S3 再次处理同一个已接收的 PR。读回同一个交付结果。已有 Publication 的正式 Delivery 沿 #557 原行为恢复。

## 5. 行为要求

R1 确认 TaskId、generation、Delivery、接受范围和 Git 中的来源证据。核对 GitHub 仓库、目标分支、PR head、双父合并提交和目标分支合并历史。显式选择定位待核对对象。归属不足、歧义或内容不匹配时返回具体缺口。
R2 归属成立后，记录实际合入内容和已有验证事实。Completion 依据原接受范围判断验收。验收通过后接续 Closure 和 Finish。对于已关闭的源 Issue，Closure 核对实际关闭状态。
R3 重复处理同一 PR 时返回同一交付结果。保持已有 Publication 路径可用。

## 6. 约束与依赖

GitHub 合并事实与原 Task/Delivery 的 Git 证据都要可读取。保留既有版本接口，任何新增入口和兼容方案由规划核对。语义归属、验证充分性和下一步由 AI 判断。执行器核对客观身份与内容并写入原公开结果。历史 CI 的失败、未运行和成功保持原义。

## 7. 可观察验收

- AC1 通过公开入口处理一个类似 #828 的样本。原 Task/Delivery 存在，双父 PR 已合入目标，发布记录与发布事务都不可用。记录真实交付，依据实际验收证据完成原 Task 的 Closure 和 Finish。
- AC2 选定 PR 和原 Delivery 的证据不匹配。报告具体缺口，原 Delivery 状态保持。
- AC3 重入同一对象时读回同一结果，原 #557 恢复场景通过回归。

## 8. 实际未决项

归属所需最小证据及新旧入口的兼容落点进入 Delivery 规划。当前无待决定的产品范围。
