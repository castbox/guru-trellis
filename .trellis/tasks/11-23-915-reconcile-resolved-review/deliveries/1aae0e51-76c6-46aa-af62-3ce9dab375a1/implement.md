# D1 Reconcile 冲突接续实施与验证计划

## 1. 输入与引用

读取 [D1 需求](prd.md)、[设计及唯一来源设计处置](design.md#3-来源设计处置)、[整体 PRD](../../prd.md)。开发从固定 B `8604558695dfd9d8ea2181406a87ece70d9eea63` 开始。本批没有前序 Delivery。现行 Reconcile 详细合同、公开 `begin_check` 和 Branch Review 的正式合同分别决定执行、候选和审核行为。

## 2. 有依赖顺序的步骤与文件责任

1. **I915-1。** 用当前安装核对错误入口及真实调度关系。修改 canonical Reconcile `SKILL.md` 的 `delivery_resolved_candidate` 段。保留现有 resolved executor，写清实施 owner 的固定 B 与实际 H、原投影的输入及正式 `delivery_branch_review` 消费。按现有复制和受管分发边界处理旧文案。
2. **I915-2。** 在 #915 worktree 由原 `guru-upgrade-tools` 准备真实 source 和 exact write set，按其写入门禁更新 dogfood 受管包与声明平台投影。原安装器生成 manifest。使用适用的开发候选范围并保留正式 source lock 的限制。核对未处理 sidecar、实际安装读取、源与投影及 Task/session 保留。
3. **I915-3。** 用锁定 Fork 构建的 `0.7.0-castbox.6` 初始化一个独立临时 Git 仓库。使用固定 B 的官方 Guru marketplace workflow 和当前候选完整 preset，核对 workflow 本轮等同。保存可重跑输入和关键结果。按 V915-2 走真实已有独立审核后的正常冲突接续。以一次真正独立后继审核形成双槽结果。
4. **I915-4。** 工程自检后交原 RDT/Architecture owners 复核实际差额。然后按标准交付门禁提出精确本地提交，绑定完整固定候选，执行 #915 自身的独立 Branch Review。Publication 和 expected-head Merge 各自沿原门禁。

## 3. 验证入口、输入与预期观察

- **V915-1。** 在 #915 worktree 运行 `bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .` 和 `git diff --check`。复核受管 Skill 及声明平台的生效副本和命令权限。临时仓库使用匹配 CLI 的 `init --codex --yes --workflow guru-team --workflow-source gh:castbox/guru-trellis/trellis#8604558695dfd9d8ea2181406a87ece70d9eea63`。在同一临时仓库运行当前候选的 `bash trellis/presets/guru-team/scripts/bash/apply.sh --repo "$GURU_915_FIXTURE" --platform codex --json`。记录实际匹配身份和 sidecar。适用时用同一原安装入口重跑，核相同资产和保留边界。
- **V915-2。** 在上述临时安装中，先记录真实提交候选、独立原审核和至少一个可验证且具有后继适用性的工程事实。以同一基点的两个正常分支修改同一段架构正文。保留实际 `git merge --no-commit --no-ff` 结果、`MERGE_HEAD` 和冲突路径，按已安装 Reconcile 入口解决。运行原 `execute-resolved-base-reconciliation.sh --input <实际输入>`。验证 `git show -s --format=%P <实际H>` 的父顺序、整合提交次数及恢复边界。实施 owner 通过当前公开候选构造器和 `delivery.py begin-check` 绑定完整 B..H。调用方使用真实执行回执的 `result` 运行 `project-resolved-full-review.sh --input <实际输入> --result <实际回执> --authoring <当前审核输入>`，将返回 `result` 原样传给正式 Branch Review。读取公开结果核同 key、B、H、两个正式结果及 predecessor。独立审核记录应具体标明原覆盖的来源、采用理由及实际补充。
- 现有机械回归按需采用：`python3 trellis/skills/guru-team/packages/guru-reconcile-task-base/tests/joint_resolved_flow.py --source . --fork "$GURU_915_FORK" --output "$GURU_915_EVIDENCE/joint"`。该 fixture 使用模拟语义判断。保留真实 Agent 审核和真实入口的观察作为验收依据。测试说明与实际结果分开记录。

## 4. 停止条件与适用回退点

当前资料缺失、安装前像冲突、实际投影拒绝或后继审核不足时，保留首次结果和命中前置，回到原 owner。临时验收按记录中的起始提交、输入与命令启动新工作目录。证据放在与临时 Git 仓库独立的位置后核对可读性，再处理本次产生的临时资源。达到 AC915-1 并通过命中的分发检查后停止追加验证。外部采用和完整升级或发布矩阵仍属于其他工作。

## 5. Delivery Policy

**full**。本切片覆盖 AC915-1 对应的受管说明与临时仓库接续验证。当前没有需后继 Delivery 承接的验收。整体 Completion 仍需核对实际验收、公开独立审核与 Delivery 结果。

## 6. Docs SSOT Plan

**no_docs_update_needed**。[现行 RDT 与 Architecture 引用](design.md#9-canonical-引用本轮差额与实际未决项)已有实际职责、顺序和验证边界。修正唯一入口及受管安装输出，保留原 RDT 和 Architecture current 正文。原 RDT owner 核对实际变更，原 Architecture owner 按当时实际差额处理适用结果。若发现现行权威也需要调整，回到原 owner 判断受影响规划和提交前整合。
