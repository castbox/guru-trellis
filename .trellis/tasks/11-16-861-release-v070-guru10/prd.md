# #861 准备 v0.7.0-guru.10 正式发布：整体需求

## 1. 来源与术语

| 标识 | 来源及章节 | 角色 | 本 Task 用途 |
| --- | --- | --- | --- |
| S1 | https://github.com/castbox/guru-trellis/issues/861 ，完整正文 | 要求 | 无其它 Issue 前置、最新 main、准备与正式发布边界 |
| S2 | `.agents/skills/release-guru-trellis-version/references/contract.md`：Stage 1、Complete Source Before Actual Adoption、Whole Preparation Completion | 约定设计 | 准备交付、真实采用、reference-only Closure 与 Finish |
| S3 | 同一合同：Stage 2、Local Installation Convergence、Independent Mutation Confirmations | 约束 | Task 外正式发布和本地收尾的直接后继职责 |
| S4 | `.trellis/workflow.md`：Phase 1、Phase 2、Phase 3 | 约定设计 | 原 Author、Architecture、Approval、提交和交付 owner 顺序 |
| S5 | `trellis/guru-team-extension.json`；`trellis/presets/guru-team/source/trellis-source.json`；`.trellis/.version` | 当前事实 | 区分 Guru 版本和 Fork CLI/source lock |
| S6 | `README.md`；`trellis/workflows/guru-team/README.md`；`trellis/presets/guru-team/README.md` | 当前事实 | 正式安装入口、同源 ref 和版本说明 |

“准备完成”表示本 Task 的全部交付及收尾完成；不表示 tag、smoke 或 Release 已完成。“真实采用”指原 tools owner 对准备 checkout 完成 `source_locked` 更新并验证；临时安装不替代它。正式发布后的本地目标仅为保留主目录 `/Users/wumengye/Documents/GoProjects/guru-trellis`，由 Stage 2 处理。

## 2. 背景与问题

当前正式版本及 canonical extension 均为 `0.7.0-guru.9`。已合入 main 的后继变更尚未通过下一正式版本提供给安装者。下一正式 tag 与 extension revision 均采用 `v0.7.0-guru.10` / `0.7.0-guru.10`；前驱为 `v0.7.0-guru.9`。执行相关写入前重新核实占用，不覆盖已有 tag。

固定 Fork 的 CLI 为 `0.7.0-castbox.6`。本次 Guru 发版不单独提升 Fork 版本；复核 manifest、lock、实际构建和 CLI 记录的一致性。版本说明与实际安装必须共同准备，不能只改版本号或用验证器通过代替真实采用。

## 3. 目标与非目标

本 Task 完成 Stage 1：可分发的完整目标版本源、公开说明、受管投影、适用知识整合、准备 checkout 的真实 tools 采用，以及完整交付和终态收尾。没有其它 Issue 的完成、关闭、合并或归档前置。

本 Task 不创建最终发布候选、tag 或 GitHub Release，不执行 tag-pinned smoke，不关闭 #861，不升级业务仓库或部署生产，不清理其它 Task、分支或 worktree。准备 PR 和 Finish bookkeeping PR 均使用 `Refs #861`，不产生 Issue 关闭效果。

## 4. 真实调用方、场景与流程

| 场景 | 调用方、条件与触发 | 行为 | 可观察结果 |
| --- | --- | --- | --- |
| SC1 | 发布 owner 从最新 main 开始准备 | 原流程规划并交付完整目标版本源 | 目标版本的 manifest、公开安装入口、可分发资产和适用验证相符 |
| SC2 | 完整干净源已经实际交付，准备 checkout 需要采用 | 原 tools owner 使用该完整匹配源执行 source_locked | 真实 installed 内容、provenance、CLI、lock、平台入口得到验证 |
| SC3 | 准备整体范围全部满足 | 原 Completion、reference-only Closure 和 Finish 执行收尾 | Task 正常终态，终态归档进入 main，#861 保持开放 |
| SC4 | Stage 2 接续准备结果 | 发布 owner 重新读取届时最新 main 并冻结候选 | 准备分支的审查结果不被当作最终候选发布 pass |

## 5. 行为要求

- **R1 版本与来源**：目标 Guru tag/revision、前驱、Fork CLI 和 source lock 保持各自含义。workflow 与 preset 的正式或候选安装入口使用同一 immutable 来源。尚未正式发布的版本说明保留真实执行条件。
- **R2 完整可分发源**：收敛目标版本的 canonical manifest、直接版本消费者、公开说明和必要兼容迁移说明。原维护 owner 处理真实命中的 Requirements/Design/Test 和 Architecture 单元；不追加无消费方的 release ledger 或全局版本登记。
- **R3 交付顺序**：准备使用同一 Task。D1 先独立交付完整可分发源及其验证；D1 的完整性不能依赖 D2 已执行。D1 实际 delivered 后，原 Completion 对尚未实施的采用返回 additional_delivery_required，原路由才建立并规划 D2。不得提前创建 D2 或把采用缺口记作仅待补证据。
- **R4 真实采用**：D2 从 D1 实际交付的完整干净匹配源，经原 tools owner 完成准备 checkout 的 source_locked 更新。验证 installed extension、完整受管内容、平台投影、真实来源、CLI、source lock、native entry、可执行位和 sidecar。保留 Task、archive、workspace、session、用户配置、peer tools 和 common runtime。
- **R5 定向验证**：每个 Delivery 按其独立承诺完成 source/package、声明平台投影、安装或 reapply/drift、兼容直接消费者和真实采用所需验证。临时安装证明源行为，不证明准备 checkout 已采用。不自动扩张为累计多平台 Release Gate 矩阵。Stage 2 的最终候选门禁由其 owner 重新执行。
- **R6 全部准备收尾**：每个 Delivery 通过当前原 Author、Architecture、Approval、工程检查、知识整合、TaskCommit、一次独立完整 Check/Branch Review、Delivery Review、Publication 和 Merge。整体 Completion 覆盖所有准备责任；Closure 为 no_mutation；Finish 将精确终态归档及簿记合入 main。资源清理由原 owner 单独审查。
- **R7 后继与失败**：Stage 2 在准备及簿记合并后获取最新 main，冻结唯一 candidate commit/tree，并按 #861 在发布副作用前复核推进。准备阶段的失败、stale、内容变化或来源不匹配返回原 owner，保留真实失败及未验证边界。后续 tag、smoke、Release、主目录安装和 Issue 关闭保留各自确认边界。

## 6. 约束与依赖

复用当前 Markdown workflow、私有发布合同和原公共 Skill API；不修改上游或全局包，不模拟审批链，不写共享 journal，不持久化授权。当前流程没有默认独立 Wording 关卡；表达和语义保持由原写作、审核 owner 在其职责内完成。

D2 只依赖本 Task 内实际完成的 D1 完整源交付。这不是对其它 Issue 的状态依赖。真实工具采用、版本来源或安装冲突不能由临时测试替代。历史 Task guard 不授权转换历史数据、普通 apply 绕过或手工覆盖受管文件。

准备 checkout 的采用属于本 Task；正式发布后保留主目录的安装收敛属于 Stage 2。两者的目标、来源和证据分别核实，不互相代替。

## 7. 可观察验收与验证方式

| 验收 | 对应要求/场景 | 入口与预期结果 | 证据边界 |
| --- | --- | --- | --- |
| AC1 | R1–R2 / SC1 | 检查完整目标源、公开入口和版本映射；目标版本及同源安装规则一致 | 不声称远端正式 Release 已存在 |
| AC2 | R3 / SC1–SC2 | 读取实际 Delivery 事实；D1 独立 delivered 后才分配 D2 | 计划、单次提交或验证器不等于 delivered |
| AC3 | R4–R5 / SC2 | 原 tools owner 在真实准备 checkout 执行并验证 source_locked；实际资产、来源和 CLI/lock 相符，无未处理 sidecar | throwaway 只覆盖其明确测试层 |
| AC4 | R5–R6 / SC1–SC3 | 各 Delivery 原阶段输出和适用验证覆盖完整承诺；Task Completion 覆盖全部准备责任 | 不复用失效或跨候选 pass |
| AC5 | R6–R7 / SC3–SC4 | main 包含准备交付及精确终态归档；Closure no_mutation，#861 保持开放 | 最终候选发布门禁、本地发布后收尾仍待 Stage 2 |

## 8. 实际未决项

没有阻塞整体准备需求的未决产品选择。各 Delivery 的实际文件集合、验证命令、Docs 策略和 Architecture 承接由原规划 owner 在相应切片展开；它们不降低以上整体责任。正式发布候选和发布结果只在 Stage 2 从 live main 与真实结果取得，不在本文件预填。
