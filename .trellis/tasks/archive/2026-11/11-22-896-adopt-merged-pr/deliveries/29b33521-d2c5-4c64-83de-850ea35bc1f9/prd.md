# D1：接收缺少 Publication 的已合并 PR

## 1. 整体来源与术语

整体范围见 [Task PRD](../../prd.md) 第 3–7 节，以公开 `accepted_scope` 为准。本 Delivery 的 `scope_ref` 覆盖 R1–R3 和 AC1–AC3。规划根为本文件所在的 Delivery 目录。

| 来源 | 角色 | 用途 |
| --- | --- | --- |
| [#896](https://github.com/castbox/guru-trellis/issues/896)「行为要求」「验收」 | 规范要求 | 决定本批的归属、交付记录与收尾行为 |
| [#896](https://github.com/castbox/guru-trellis/issues/896)「背景」与 [#828](https://github.com/castbox/guru-trellis/pull/828) | 背景和历史事实 | 检验方案能否处理已有的 Task 和 Delivery |
| [#557](https://github.com/castbox/guru-trellis/issues/557) 与 ADR-026 | 兼容依据 | 保留已有 Publication 的原恢复路径 |

接收是把已经合入的内容归到已有 Delivery，并记录实际交付。Publication 是原发布职责写入的公开结果。

## 2. 整体与本批目标、非目标

当原 Publication 和发布事务不可用时，提供标准公开入口。经核实，原 Delivery 能接续 Completion、Closure 和 Finish。本批覆盖整体三项需求。首批支持同仓双父合并。排除 squash、rebase、fork PR、创建替代 Task 或 Delivery、补写过去的审核和发布结果。#828 作为历史样本。此任务的验收使用隔离样本完成收尾。

## 3. 本批起点、前序结果、依赖与剩余责任

本批是 D1，当前没有前序交付。现有 Merge 在无对应 Publication 时返回 `manual_merge_missing_publication`。新入口需要能读取已选 Task/Delivery、接受范围、不可变 Git 对象及 GitHub 合并状态。完整交付后，由 #896 的 Completion 判断整体要求和公开链验收。无需计划后续 Delivery。

## 4. 本批调用方、场景与流程

| 场景 | 入口及条件 | 可观察结果 |
| --- | --- | --- |
| S1 接收并收尾 | 用户选择仓库、已合并 PR 和原 Task/Delivery。Git 与 GitHub 证据能建立唯一关系。 | Merge 记录实际交付，调用原 Completion。验收通过后接续 Closure 和 Finish。源 Issue 已关闭时，Closure 核对现状。 |
| S2 证据有缺口 | 用户选择了无法唯一归属的正常历史 PR，或选错了 Delivery。 | 返回缺少或不匹配的具体事实，保持原 Delivery 状态。用户可补齐原事实后重入。 |
| S3 重入与兼容 | 用户重试同一成功合并，或处理已有 Publication 的手动合并。 | 前者读回同一原 Delivery 结果。后者仍由 #557 入口恢复。 |

## 5. 完整行为、条件与约束

- R1（S1/S2）。选择只定位对象。核对 TaskId、generation、Delivery、接受范围、PR 带来的 Git 来源证据、GitHub 仓库、目标分支、PR head、双父合并提交和实际目标分支历史。事实缺失、歧义、归属或内容不匹配时保留 Delivery 状态。
- R2（S1）。记录实际合入的内容，并读取其已有验证事实。保留未运行、失败、待定和通过的区别。Completion 对整体范围和证据独立判断。Closure 核对已关闭源 Issue 后由 Finish 完成归档。证据仍待补时，保留原 Completion 处置。
- R3（S3）。重入读取同一原 Delivery 事实。保留 #557 已有 Publication 的合并恢复语义。

## 6. 本批验收、验证方式与未决项

- AC1（R1/R2，S1）。隔离样本从公开入口处理原 Task/Delivery 及同仓双父合并。原 Publication 和发布事务均不可用。观察实际事实写入，并通过原 Completion、Closure、Finish 得到原 Task 的归档结果。验证合并提交和 CI 保持实际含义。
- AC2（R1，S2）。通过同一入口选一个正常合并但与所选 Delivery 不符的 PR。检查具体缺口，核对 Delivery 前后相同。
- AC3（R3，S3）。重入并比较原交付结果及 Task 状态。跑已有 Publication 恢复回归。

没有未解决的产品范围问题。架构候选需明确 Git 归属来源、实际树及 Completion 的消费方式。

## 7. Canonical 引用与本轮差额

- `docs/requirements-design-test-contributions/557-manual-merged-delivery-recovery/requirements.md` 中 BEH-557-01..04 定义兼容边界。本批补充缺 Publication 的入口。
- 同一贡献的 `design.md` 中 DES-557-01..04 定义原 Merge、Completion 与分发边界。本批复用这些原职责。
- 同一贡献的 `test.md` 中 T557-01..07 区分公开链、历史 CI、身份、重入与安装证据。本批增加无 Publication、已关闭 Issue 与归档场景。
- `docs/architecture/adr/026-manual-merged-delivery-recovery.md` 定义原 Merge 的终态归属。追加 Git 证据的适用条件由原 Architecture owner 评估。
