# 修复 Reconcile 解冲突后到独立审核的接续

## 1. 来源与术语

| 来源 | 角色 | 用途 |
| --- | --- | --- |
| [Guru Trellis #915](https://github.com/castbox/guru-trellis/issues/915)「期望行为」「验收」 | 直接需求 | 定义冲突解决后的接续顺序、审核责任和临时仓库验收。 |
| [Reconcile 详细合同](https://github.com/castbox/guru-trellis/blob/8604558695dfd9d8ea2181406a87ece70d9eea63/trellis/skills/guru-team/packages/guru-reconcile-task-base/references/contract.md#L249) | 约定设计 | 定义一次整合提交、固定内容基线、实际回执投影及正式 Branch Review 输入。 |
| [#915 开工复核讨论](https://github.com/castbox/guru-trellis/issues/915#issuecomment-7100730289) | 审核材料 | 确认入口矛盾与独立验收边界。 |
| [Guru Trellis #794](https://github.com/castbox/guru-trellis/issues/794) | 已交付历史 | 解释 Check 与 Branch Review 合并为提交后一次独立审核的由来。 |
| [go-guru PR #548](https://github.com/castbox/go-guru/pull/548)及[整合提交](https://github.com/castbox/go-guru/commit/53c520cfe45b5eb1043ee6cc4fd95dc7fdf67350) | 关联案例 | Issue 引用该次架构文档冲突，指出整合后跳过了原投影命令。 |

固定内容基线 B 是该 Delivery 原先选定的内容起点。整合 HEAD 是原 Reconcile 执行器实际创建或读回的整合提交。Check 和 Branch Review 是一次独立审核写出的两个正式结果。

## 2. 背景与问题

[当前 Reconcile 入口](https://github.com/castbox/guru-trellis/blob/8604558695dfd9d8ea2181406a87ece70d9eea63/trellis/skills/guru-team/packages/guru-reconcile-task-base/SKILL.md#L121) 仍要求先写单独的 Check，并引用旧 Branch Review profile。执行者按该入口操作时，可能在真正的联合审核之前重复执行 Check，或绕过实际整合回执的投影。详细合同与现行运行时已经支持联合审核。

## 3. 目标与非目标

让执行者从匹配安装的 Reconcile 入口完成同一 Delivery 的冲突解决和一次独立审核。Task 完成范围包括受管投影同步以及临时仓库的可重跑证明。原案例仅作为证据，验收发生在隔离 Git 仓库。新审核阶段、新公共接口和完整多平台升级或发布矩阵均在本 Task 范围之外。

## 4. 真实调用方、场景与流程

**S915-1**。现有 Delivery 已有固定提交候选及可核验的原审核记录。基线分支与 Delivery 分支从同一起点修改同一段架构正文，Git 合并报告真实内容冲突。解决并暂存冲突后，原 Reconcile owner 执行整合。原实施 owner 将该 Delivery 的当前候选接续到实际整合 HEAD。调用方把投影结果交给独立 Branch Review。审核通过时，可以从同一 Delivery 读回绑定整合 HEAD 的 Check 和 Branch Review。

## 5. 行为要求

- **R915-1**。对齐 `delivery_resolved_candidate` 的入口说明和实际受管安装投影。原 Reconcile 执行器根据已解决的冲突创建一次整合提交。
- **R915-2**。原实施 owner 保留同一 Task、Delivery、适用的 Planning 和固定 B。按原合法流程使用实际整合 HEAD 构造候选并执行 `begin_check`。
- **R915-3**。调用方用实际整合回执和合同规定的输入执行 `project-resolved-full-review`。投影输出仅供 `guru-review-branch:delivery_branch_review` 消费。投影前无需另跑独立 Check。正式 Branch Review 承担一次完整独立审核，并写入当前 Check 与 Branch Review 两个结果。
- **R915-4**。独立审核覆盖实际解法、整合后的组合语义与受影响消费者。原审核者仍符合独立性要求时可以继续。审核者采用可核验且仍适用的旧覆盖与验证，补充变化、缺失或适用性不明的部分。

## 6. 约束与依赖

复用原整合执行器、公开 `begin_check` 操作、既有投影命令和正式 Branch Review owner。适用的详细合同约束在本轮 Delivery 设计中逐项承接。安装验证使用同一版本的 workflow、Skill 和运行时。语义审核由 AI 执行，命令只执行或验证客观事实。

## 7. 可观察验收与验证方式

**AC915-1** 对应 R915-1 至 R915-4。使用修复后的匹配安装，在一个临时仓库从同一起点建立两个分支，并让两边修改同一段架构正文。为 Delivery 准备固定候选和可核验的原审核证据，再从原冲突解决入口接续。核对 Git 实际报告冲突，整合提交只创建一次，且两个父提交是原 Delivery 候选所在的整合锚点和选定的新基线。核对 `begin_check` 的候选保留 B 并指向整合 HEAD，实际整合回执进入投影，投影输出被正式 Branch Review 消费。读回同一 Delivery、同一整合 HEAD 的两个正式结果。调用记录要区分独立审核、旧证据的采用和必要补充，并保留起始提交、触发输入和关键调用结果供重跑。

## 8. 实际未决项

整体需求没有未决选择。匹配安装的构建与可重跑证据载体由 Delivery 规划确定，按 AC915-1 验证。
