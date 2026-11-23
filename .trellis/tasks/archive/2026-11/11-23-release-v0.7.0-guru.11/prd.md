# #908 准备 v0.7.0-guru.11 正式发布：整体需求

## 1. 来源与术语

| 标识 | 来源及章节 | 角色 | 本 Task 用途 |
| --- | --- | --- | --- |
| S1 | [Issue #908](https://github.com/castbox/guru-trellis/issues/908)，完整正文和审核评论 | 要求 | main 基线、无其它 Issue 前置、版本、验证、发布和本地收敛边界 |
| S2 | `.agents/skills/release-guru-trellis-version/references/contract.md`，Stage 1、Complete Source Before Actual Adoption、Whole Preparation Completion | 约定设计 | 完整源、真实采用、reference-only PR/Closure 和 Finish 的责任顺序 |
| S3 | 同一合同，Stage 2、Local Installation Convergence、Independent Mutation Confirmations | 约束 | Task 外 tag、smoke、GitHub Release、本地安装和 Issue closure |
| S4 | `.trellis/workflow.md` 的 Phase 1 至 Phase 3 与 Publication 入口 | 约定设计 | 当前 Author、Architecture、Approval、提交、完整 Review、Publish、Merge 和终态 owner |
| S5 | `trellis/guru-team-extension.json`、`trellis/presets/guru-team/source/trellis-source.json`、`.trellis/.version` | 当前事实 | Guru revision、Fork source lock 与 CLI 版本轴 |
| S6 | `README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md` | 当前事实 | 当前版本、正式前驱、安装条件和历史版本说明 |
| S7 | `.trellis/tasks/archive/2026-11/11-16-861-release-v070-guru10/prd.md` 及其 D1/D2 交付 | 历史事实 | 最近一次完整源先交付、真实采用作后继 Delivery、Closure 保持 Issue 开放 |
| S8 | `guru-publish-task-delivery` 的当前 Interface、合同和 workflow Publication 入口 | 约定设计 | 当前 readiness 与远端写入由同一发布入口承接 |

“准备完成”表示本 Task 的全部 Delivery、Completion、reference-only Closure 和 Finish 已完成；“正式发布”表示 Task 外对冻结 main candidate 创建 tag、运行 tag-pinned smoke、创建 GitHub Release、收敛本地目标并关闭 Issue #908。准备分支 HEAD、Delivery SHA 或临时安装都不能成为最终发布候选。

## 2. 背景与问题

最新正式 tag 为 `v0.7.0-guru.10`，当前 `main@2acab7fadebf57c2f2560451b9ff2a050d8811f5` 比该 tag 多 57 个提交。canonical extension 和已安装 extension 仍为 `0.7.0-guru.10`，尚无 `v0.7.0-guru.11` tag 或 Release。

当前 main 已把 Delivery readiness 并入 `guru-publish-task-delivery`，并移除 `guru-review-task-delivery`。仓库私有发布合同及其 Codex、Claude、Cursor 发现副本仍要求经过已移除的 Skill，因此按当前合同执行会与真实 registry/workflow 不一致。三个公开 README 也仍以 `.10` 为当前 canonical 版本。

Fork source lock 为 `castbox/Trellis@e3793251fad8bd261d0c370d408c7675b9f6a140`，CLI 为 `0.7.0-castbox.6`。本次发版没有请求提升 Fork revision；准备必须保持 Guru tag、extension revision 和 CLI 三个版本轴分离。

## 3. 目标与非目标

整体目标是完成 `v0.7.0-guru.11` 的 Stage 1 准备：交付完整可分发源，更新全部直接版本消费者和公开发布说明，迁移私有发布消费者到当前 Skill graph，从已交付完整干净源真实采用到准备 checkout，并通过完整质量与终态收尾。

整体完成责任包括：

- D1 独立交付完整可分发源、版本消费者、公开说明、私有发布合同和适用验证。
- D1 实际 delivered 后，由原 Completion/Creation 分配 D2；D2 使用该真实完整干净源执行 `guru-upgrade-tools` 的 `source_locked` 采用并验证准备 checkout。
- 所有 Delivery 完成原 Planning、Architecture、Approval、工程检查、RDT/Architecture 必要整合、TaskCommit、一次独立完整 Check/Branch Review、Publication 和 Merge。
- 完成 whole-Task Completion、reference-only Closure 和 Finish，使精确归档及簿记进入 main。

本 Task 不创建最终 candidate/tag、不运行 tag-pinned smoke、不创建 GitHub Release、不关闭 #908、不升级业务仓库、不部署生产，也不清理无关 Task、branch 或 worktree。准备 PR 和 Finish PR 使用 `Refs #908`，不产生 Issue 关闭效果。

## 4. 真实调用方、场景与流程

| 场景 | 调用方、条件与触发 | 处理行为 | 可观察结果 |
| --- | --- | --- | --- |
| SC1 完整源准备 | 发布准备 owner 从 Issue #908 和固定 main 开始 | 更新 `.11` 版本面、公开说明、私有发布消费者和直接回归，交付完整源 | 源、消费者、说明和验证共同支持同一目标版本 |
| SC2 真实采用 | D1 已实际 delivered | 原 tools owner 从 D1 完整干净源执行 `source_locked`，更新准备 checkout | installed extension、source、CLI、受管内容、平台投影和保留状态经实际验证 |
| SC3 准备收尾 | 全部 Delivery 完成 | 原 Completion、reference-only Closure、Finish 和 Cleanup 按各自边界执行 | main 包含准备交付和精确归档；Issue #908 保持开放 |
| SC4 正式候选 | Stage 2 在准备与簿记合并后开始 | 发布 owner 重新获取最新 main 并冻结 candidate | 准备分支及旧审查结果不被冒充最终候选 |
| SC5 后继修复 | Stage 2 或正常验证发现准备源缺陷 | 原准备 owner 形成后继 Delivery，完成原质量链后重新冻结候选 | 修复实际进入 main，受影响证据由新内容重新取得 |

## 5. 行为要求

- **R1 版本轴**：目标 Guru tag/revision 为 `v0.7.0-guru.11` / `0.7.0-guru.11`，前驱为 `v0.7.0-guru.10`。执行版本写入前重新核实 tag、Release 和 revision 未被占用；不覆盖已有对象。Fork 保持现有 source lock 与 `0.7.0-castbox.6`，除非仓库当前 authority 在准备前真实变化并返回原 owner。
- **R2 完整可分发源**：canonical manifest、`guru-upgrade-installation` 的生产者、当前输出 schema、stop consumers、active example，以及所有真实版本直接消费者共同更新到目标 revision。不得只改版本字面或建立第二版本 authority。
- **R3 公开说明**：根 README、workflow README 和 preset README 更新当前 canonical target、正式前驱和 `.11` 安装示例的 Release 存在条件。已发布历史和前驱事实保留原身份；未发布 `.11` 不得声明为 stable/latest 或正式 Release 已通过。
- **R4 当前发布链迁移**：仓库私有 release contract 必须按当前 workflow 执行。Branch Review 通过后的发布 Architecture eligibility 与实际 readiness 均由当前 `guru-publish-task-delivery` 承接；不再要求 `guru-review-task-delivery`，也不复制 Publication 的内部流程。Shared `.agents` 私有合同与其 Codex、Claude、Cursor 发现副本保持一致，且不进入公共扩展分发。
- **R5 完整源与真实采用顺序**：D1 先独立交付完整源及自身验证，其完整性不得依赖 D2。只有 D1 实际 delivered，原 Completion 才可返回 `additional_delivery_required`，原 Creation 才建立 D2。D2 从真实 D1 完整干净源执行 `source_locked`，验证实际 installed 内容及所有保留责任。
- **R6 定向验证**：按变更覆盖 source/installed package validation、Shared/Codex/Claude/Cursor 投影一致性、版本生产者及直接消费者、私有合同回归、ownership、reapply、dogfood drift、定向安装和前驱升级。普通 Issue 不扩张为累计多平台 Release Gate 矩阵；Stage 2 在自己的最终 candidate 上执行完整发布门禁。
- **R7 准备收尾**：每个 Delivery 通过当前原质量链。whole-Task Completion 覆盖所有准备责任；Closure 对 reference-only source 返回 `no_mutation`，不得关闭 #908。Finish 归档、簿记 PR 和资源清理由原 owner 分别完成。
- **R8 后继与失败**：Stage 2 在准备与簿记合并后获取最新 main，冻结唯一 candidate commit/tree，并在每个发布副作用前重新核实 authority。失败、跳过、stale、cross-SHA、身份不匹配或不知道 route 时停在原 owner，不用元数据提交记录发布进度。
- **R9 证据与安全**：不得泄露 token、secret、private key、签名 URL、`.env`、数据库 URL、客户数据或敏感原始记录。公开正文、Issue、PR、Release 和验证说明只包含真实、可复核且未越界的结论。

## 6. 约束与依赖

必须复用现有 Trellis workflow、公共 Skill API、preset installer 和仓库私有发布合同，不修改上游源码、全局 npm 包或 `node_modules`。Workflow 行为由 Markdown 控制面定义，脚本只执行、记录或校验确定性事实。

D1 的完整源依赖固定 main、当前 release contract、版本清单、private Skill projections 和现有测试。D2 只依赖本 Task 内实际 delivered 的 D1，不依赖其它 Issue 状态。没有仓库 URL、Fork checkout、GitHub 身份、Trellis runtime 或必要验证入口时，由对应原 owner 返回阻塞，不猜测替代物。

准备 checkout 的真实采用属于本 Task；正式发布后对调用 checkout 的安装收敛属于 Stage 2。临时安装、验证器输出、准备分支或 dirty source 都不能替代真实 `source_locked` 采用。

## 7. 可观察验收与验证方式

| 验收 | 对应要求/场景 | 入口与可观察结果 | 证据边界 |
| --- | --- | --- | --- |
| AC1 | R1–R2、SC1 | 从实际升级生产者取得目标版本输出，并验证全部当前 schema/consumer/example 与 canonical revision 一致 | 不声称 tag 或 Release 已存在 |
| AC2 | R3、SC1 | 完整阅读三份 README 的相关章节；`.11`、`.10` 前驱、Release 条件、同源 ref、命令和 anchors 一致 | 文档检查不证明正式安装 |
| AC3 | R4、SC1 | 私有合同四份字节一致；真实 workflow/registry 中不存在 `guru-review-task-delivery`，ready 与发布使用当前 `guru-publish-task-delivery` 入口 | 私有副本不被当作公共分发 |
| AC4 | R5–R6、SC1–SC2 | D1 的 source/package、投影、安装、reapply、drift 和必要回归完成；D1 delivered 后 D2 的真实 tools 采用返回并验证目标 installed 状态 | 临时安装只证明其覆盖层 |
| AC5 | R5–R7、SC2–SC3 | Completion 读取全部真实 Delivery；Closure 返回 `no_mutation`；Finish 归档和簿记最终进入 main，#908 仍 open | 准备完成不证明 tag/Release |
| AC6 | R8–R9、SC4–SC5 | Stage 2 的 candidate、tag、smoke、Release 和本地收敛分别绑定同一实际对象；失败和未验证边界如实报告 | 不属于本 Task 的正式发布执行结果 |

验证方法必须命中实际生产者和消费者，区分 source、installed、dogfood、临时安装和正式发布层。固定字面、配置值与 fixture 自证不能代替行为入口。已完成或未触及的必要验证在 Delivery 实施结果中如实记录，不预填通过。

## 8. 实际未决项

没有阻塞整体准备目标的产品选择。D1 和 D2 的实际文件集合、验证命令、Policy、Docs Plan 和 Architecture 承接由各自规划 owner 在对应切片展开。最终 candidate、正式 tag、smoke、Release 和本地安装结果是 Stage 2 在 Task 完成后从 live main 与真实执行取得的未来事实，不在本 PRD 中预填。
