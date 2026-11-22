# D1 设计

## 1. 设计目标、需求承接与内容基线

D1 承接 Delivery PRD 的 R1–R3、S1–S3 和 AC1–AC3。开发基线 B 由 Phase 0 通过固定基线读取选定，为 `origin/main@889d79e734072e2de954bbe8bd90b94880735a1b`。规划时 H0 同 B。实现后的 B..H 用于审核 #896 本身，发布目标为 `castbox/guru-trellis:main`。恢复历史 PR 的目标、合并基点、head 和合并提交均由所选 Task 与该 PR 的证据决定。

架构依据为项目 Architecture Baseline、设计宪章、change contract 与 ADR-026。独立候选评估要求区分 PR head 候选和实际合入内容。设计分别保留两者的 Git 对象。

## 2. 当前系统、边界与目标差额

现有 Merge 的 `delivery_merged_recovery` 从 Publication 取得关联与候选路径。D1 无前序 Delivery。新入口由同一 Merge Skill 承接，并从 Git 读取关系。历史闭环沿现有公开 API 1.0 和原 Completion、Closure、Finish 运行；无需改上游 Task2 格式、创建替代记录或回放历史发布。

## 3. 来源设计处置

#896 的「行为要求」「验收」是需求约束。Issue 把机制与兼容选择交给实施规划，未给出规范性来源设计。ADR-026 与 #557 是当前兼容依据。已有 Publication 时继续使用原终态恢复入口。

## 4. 模块、职责与设计取舍

| 模块 | 职责 |
| --- | --- |
| Merge Skill、Interface、workflow | 用户显式选择仓库、PR、TaskRef、DeliveryKey。workflow 明确进入该 Profile。Merge AI 评审归属、内容和现有验证，返回原交付出口。 |
| Merge runtime | 复用原同仓、终态、双父、第二父和目标第一父历史核验，以及原公共事实写入。新模块核对 Git 中 Task、Delivery、来源与范围，构造 PR head 候选。 |
| Completion Skill | 读取原接受范围与每个公开交付。针对这条恢复路径，核对 PR head 的候选、第一父至合并提交的完整落地差异，以及仍适用的证据。 |
| Closure、Finish | 原 Closure 重新读取已关闭的源 Issue。原 Finish 按公开 Completion 与 Closure 归档并核对目标。 |

沿用已有 Merge owner 可维持同一事实写入方。原 Publication 的缺失与其已存在的情况面向不同来源证据，各有独立入口。用 Git 对象建立历史关系可保留 #828 原始证据，并允许恢复后参考仍能回读。用户选定、分支名、PR 标题和继承的 Task 文件都不足以建立归属。

## 5. 接口与数据

- 公开输入使用 `delivery_adopt_merged_pr`，包含 `mode/task_ref/delivery_key/repo_ref/pr_number`。新入口纳入新增版本的聚合 schema，原输入、输出和 #557 单独的 schema 保持兼容。
- 独立 call-local review 绑定该 key、实际 repo/PR/head/merge/target、当前所查验的 CI，及 Merge AI 对归属和两段差异的判断。执行器校验客观字段；review 不持久化。显式调用不依赖原私有发布事务。
- 公开 DeliveryFact 仍用 `record_delivery(historical_success=true)`，保留实际 `reviewed_head`、`merge_commit`、目标和 PR 引用。按唯一 `merge-base(merge^1, head)` 至 head 的变更路径构造 Candidate。用既有内容排除规则，并用已安装公共 Git 内容构造生成哈希。合并树与父提交给出实际落地的完整差异；PR CI 仍绑定 PR head。
- `delivered` 仍输出 TaskRef/TaskKey，由原 Completion 消费。事实缺失或不一致使用原 `merge_blocked` 或该入口既有结构化执行错误，定位具体待核事实。归属成功后的证据不足由 Completion 给出正确未完成处置。

## 6. 状态、顺序、正常与失败流程

1. 解析公开 Task/Delivery，核对生命周期、原目标、接受范围及已有 Publication 或终态关联。已有 Publication 时指向对应原入口。未确认关系时不触碰 Delivery。
2. 从 GitHub 与实际 Git 对象核对仓库、合并状态、目标、父提交和 head。双父合并的第二父须是 PR head；合并提交须位于真实目标的第一父历史中。
3. 读取 PR head 与 merge 树中原 Task 记录。对照当前公开身份、来源、Task 接受范围及该 Delivery 的标识、切片范围、规划根与 profile。核对 Git 中当地接受范围的内容修订。相对于 PR 的实际共同基点，所选 Delivery 需要由 PR 引入，或其规划或关联证据由该 PR 实际改变。仅继承元数据的 PR 不成立。AI 检查完整差异并处理关系歧义。
4. Merge AI 审阅完整 PR 差异、实际 landed 差异及 head CI。通过后，原 writer 记录一个不可变交付。若已存在完全一致的事实则读回；与已记录事实冲突时保留原值。
5. 原 Completion 独立判断任务实现和范围要求的证据。Completion 先按原验收架构入口核对可适用的独立架构证据。没有历史预合并结果时，读取确定的 landed 范围和必要现行权威，沿原独立评估或证据缺口路线处理。Closure 读回实际关闭的 Issue，Finish 在其原成功路径上归档。Completion 的 evidence pending 或剩余 work 可从已记录的实际交付重入。

## 7. 恢复、兼容、迁移与集成

原 Delivery 事实写入前，错误留在原阶段。写入后输出丢失，复核同一 GitHub/PR/Git 事实并读回原结果。使用当前路径或公开档案记录的原 Task 路径定位历史树；归档后只有原事实可读回，缺失结果由原档案处置职责处理。保留已接受范围和历史 CI 记录。历史 GitHub 检查读取失败按缺口处理。

旧完整安装仍接受 #557 原输入。新入口需要匹配的 workflow、preset、Merge/Completion Skill 及安装投影。通过原工具升级或匹配安装采用。无需更新 Task 记录结构，也无需迁移历史发布事务。

## 8. 验证设计

| 验证 | 条件与独立观察 |
| --- | --- |
| V1，AC1 | 隔离的已合并 PR，原 Task/Delivery 由正常公共操作建立，无 Publication/事务。运行公开 Merge → Completion → Closure → Finish。读回目标上的归档和同一交付记录。已关闭源 Issue 保持关闭，模拟 provider 的原始检查状态不改。 |
| V2，AC1/AC2 | 双父合并实际内容可与 PR head 不同。核对记录的 Candidate 可从 PR head 读取，第一父差异能定位实际落地内容。另选继承 Task 但无所选 Delivery 归属证据的 PR，预期保留 Delivery 前后相同。 |
| V3，AC3 | 用同一调用重入，比较同一 DeliveryFact 与未改变的持久状态。运行原 Merge package #557 已有 Publication 的回归。 |
| V4，分发 | 校验 canonical 与 installed/skilled projections、重应用、漂移和侧车。代表性安装仅验证本次入口可用。GitHub 适配替身的观察和实际 GitHub 历史读取分别报告。 |

## 9. Canonical 引用、本轮差额与实际未决项

RDT 沿用当前 `task-delivery-lifecycle.md` 三层单元。公开合同、安全的正常操作边界及实际证据分别写入对应原职责。架构贡献补充 ADR-026 中的 Git 归属路径及两个内容边界，沿原 final integration、固定提交与独立完整审核。没有未决产品范围。
