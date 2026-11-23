# D1：v0.7.0-guru.11 完整可分发源

## 1. 整体来源与术语

整体权威是 [Task PRD](../../prd.md)。当前 DeliveryKey 为 `7fa61b67-258e-49db-9db3-505f1a0c4e3e`，profile 为 `pull_request`，planning_root 为当前目录。本批选择整体 R1、R2、R3、R4、R6 与 AC1、AC2、AC3、AC4。

| 来源 | 章节及角色 | 本批用途 |
| --- | --- | --- |
| [Issue #908](https://github.com/castbox/guru-trellis/issues/908) | 完整正文，要求 | 下一正式版本、main 基线、定向验证和 reference-only 准备边界 |
| [Task PRD](../../prd.md) | 第 3、5、7、8 节，要求 | 整体版本轴、当前发布链、D1/D2 顺序和验收责任 |
| `.agents/skills/release-guru-trellis-version/references/contract.md` | Stage 1、Complete Source Before Actual Adoption，设计约束 | 完整源先独立交付，D2 真实采用保持后继责任 |
| `.trellis/workflow.md` | Phase 1、Phase 2、Phase 3 与 Publication 入口，设计约束 | 当前 Author、Architecture、Approval、Review、Publication 和终态 owner 顺序 |
| `trellis/guru-team-extension.json`、`trellis/presets/guru-team/source/trellis-source.json`、`.trellis/.version` | 当前事实 | Guru revision、Fork CLI/source lock 和安装记录 |
| `README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md` | 当前事实 | 当前 canonical 版本、正式前驱、安装示例和 Release 条件 |
| `.trellis/tasks/archive/2026-11/11-16-861-release-v070-guru10/deliveries/60d7e5c9-e62e-4a92-bc33-ef7228202be0/{prd,design,implement}.md` | 历史事实 | 最近一次完整源及其验证边界，不复用其候选结果 |

“来源样本”是由现有 verifier/installer 创建的临时项目，用于观察当前源可安装、可更新、可 reapply 和可验证。来源样本不表示准备 checkout 已真实采用，也不表示正式 tag 或 Release 已存在。

## 2. 整体与本批目标、非目标

整体准备还需要 D2 真实采用、whole-Task Completion、reference-only Closure、Finish，以及 Task 外正式发布和本地收敛。D1 的独立目标是交付一个完整、可安装、版本直接消费者一致、私有发布消费者与当前 Skill graph 一致的 `.11` 源，供后继 tools owner 从实际 delivered 的干净提交消费。

本批覆盖：

- canonical extension version；
- `guru-upgrade-installation` 的目标版本生产者、输出 schema、shared/package stop consumers 和 active example；
- 三份公开 README 的当前版本、前驱和安装条件；
- Shared、Codex、Claude、Cursor 四份私有 release Skill 合同及必要回归；
- source/package、声明平台投影、来源样本安装与 reapply 的适用验证。

本批不执行准备 checkout 的正式 `source_locked` 更新，不手工修改真实 installed 资产来冒充 `.11` 已采用，不创建 D2，不执行 tag、smoke、GitHub Release、Issue closure 或业务仓库升级，不扩张为累计多平台 Release Gate 矩阵。

Guru 目标 tag/revision 为 `v0.7.0-guru.11` / `0.7.0-guru.11`，前驱为 `v0.7.0-guru.10`。Fork lock 保持 `castbox/Trellis@e3793251fad8bd261d0c370d408c7675b9f6a140`，CLI 保持 `0.7.0-castbox.6`。

## 3. 本批起点、前序结果、依赖与剩余责任

这是本 Task 的首个 Delivery，没有前序 delivered 结果。开发起点为创建 Task 时的 main commit `2acab7fadebf57c2f2560451b9ff2a050d8811f5`。当前 main 已有 #899 的续接收敛、#900 的发布入口合并和 #901 的交付对照结论，但版本面仍为 `.10`，私有发布合同仍引用已移除的 `guru-review-task-delivery`。

本批依赖固定 main 中的当前 workflow、registry、版本 producer/consumers、私有 Skill projections 和现有 tests。D1 delivered 后，整体 Completion 仍会因真实采用未实施而返回 `additional_delivery_required`；原 Creation 才可建立 D2。D1 自身缺陷不得延期到 D2，也不得从 dirty 或未交付源启动真实采用。

D2 负责准备 checkout 的 `source_locked` 更新、installed after 验证、全部保留责任和后续质量链。Stage 2 负责准备及簿记合并后的最新 main candidate、tag、smoke、Release、本地目标收敛和 Issue closure。

## 4. 本批调用方、场景与流程

| 场景 | 调用方、条件与触发 | 处理行为 | 可观察结果 |
| --- | --- | --- | --- |
| D1-SC1 版本生产者 | 维护者更新 Guru revision | 同一变更将 manifest、升级 owner、当前输出 schema、两个 stop consumers 和 active example 更新到 `.11` | 实际 producer 输出被全部当前消费者接受，Fork/CLI 轴不变 |
| D1-SC2 安装说明 | 安装者读取当前公开入口 | 三份 README 更新 `.11`、前驱 `.10`、Release 条件和同源 ref | 当前与历史版本身份清楚，未发布对象不被写成 stable/latest |
| D1-SC3 私有发布调用 | 发布 owner 按私有合同准备 Delivery | 合同使用 Branch Review 后的发布 Architecture eligibility 和 `guru-publish-task-delivery` readiness/Publication，不再要求 `guru-review-task-delivery` | 四份私有定义一致，回归按当前公共 registry/workflow 通过 |
| D1-SC4 来源验证 | 验证 owner 从完整 D1 after 建立来源样本 | 执行 source validator、临时 Codex 安装/update/reapply、同项目三平台 apply、installed validator 和完整投影核对 | 当前源在声明的来源样本边界内可安装、重复应用和验证 |
| D1-SC5 D1 交付 | D1 完整实现和工程结果齐备 | 原 TaskCommit、constructor/begin_check、独立完整 Review、Publication 和 Merge 执行 | 只有实际 delivered 才形成 D2 可消费源 |

## 5. 完整行为、条件与约束

- **D1-R1 版本生产者与消费者同步**：`trellis/guru-team-extension.json`、`guru-upgrade-installation/runtime/owner.py` 的 TARGET_GURU、该包 public upgraded output schema、包内与 shared stop consumer schema以及 active example 必须共同更新。现有输出 shape、来源家族和 dirty/untracked source rejection 保持。
- **D1-R2 公开说明精确**：根 README 只更新当前版本选择与正式安装条件；workflow README 保持流程导航；preset README 保持安装、构建和验证职责。三者使用 `.11` 和前驱 `.10`，保留已发布历史。未发布 `.11` 必须保留“仅在对应正式 Release 存在时使用”的条件。
- **D1-R3 当前发布链**：私有 release contract 的 Stage 1 按当前 workflow 写成 Branch Review → publication Architecture eligibility → `guru-publish-task-delivery` prepare readiness/execute publication → `guru-merge-task-delivery`。删除对 `guru-review-task-delivery` 的门禁和链路要求；不复制 Publication 的 schema、事务步骤或内部恢复。Shared `SKILL.md` 和 contract 只在真实入口语义变化时更新，Codex/Claude/Cursor 副本保持字节一致。
- **D1-R4 回归与分发**：私有 test_contract 验证当前发布 Skill graph、D1 delivered 后才进入真实采用、四份私有定义一致且不进入公共 registry/preset/inventory。版本 consumers 的现有定向测试必须沿实际 producer 输出观察，不为固定 `.11` 字面制造自证。
- **D1-R5 来源验证**：运行 source validator。来源样本先从当前 canonical source 完成 focused Codex 安装/update/reapply，再在同一项目补齐 Claude、Codex、Cursor 的 apply 和 installed validation。核对完整受管映射 bytes/mode、extension manifest、workflow、lock、CLI、平台选择和 unresolved sidecars。来源样本保留 `local_sample` 边界。
- **D1-R6 知识维护**：只处理真实命中的 Requirements/Design/Test 和 Architecture 单元。版本递增本身不追加全局版本登记、release ledger 或空 contribution；私有发布合同迁移需要独立 Architecture candidate/final assessment。Docs 策略与实际引用由后续 design 和 implement 展开。
- **D1-R7 交付完整性**：完整 committed candidate 经过一次独立完整 Architecture before/after、Check 和 Branch Review；任何真实后继内容变化回原 writer、TaskCommit 和受影响 Review。没有完整 Review 与 Publication readiness，不得进入 push/PR。

## 6. 本批验收、验证方式与未决项

| 验收 | 对应要求/场景 | 入口与可观察结果 | 证明边界 |
| --- | --- | --- | --- |
| D1-AC1 | D1-R1、D1-SC1 | 实际升级 producer 输出、全部当前 schema/consumer/example 和 canonical revision 一致 | 不设第二版本权威，不只比较字面 |
| D1-AC2 | D1-R2/R3、D1-SC2/SC3 | 三份 README 与四份私有合同的完整相关章节、同源命令、版本角色和当前 owner 一致 | 文档不证明 Release 或真实安装 |
| D1-AC3 | D1-R4/R5、D1-SC3/SC4 | 私有合同回归、source validator、来源样本安装/update/reapply、三平台 apply、installed validator、完整投影及其限制 | 来源样本不证明真实 Task checkout 采用 |
| D1-AC4 | D1-R6/R7、D1-SC5 | 真实 Knowledge/Architecture 判断、TaskCommit、constructor/begin_check、独立完整 Review、Publication、Merge | 只有实际 delivered 才允许 D2 |

本批在 requirements 阶段没有阻塞产品选择。来源样本、完整投影及后继真实采用的具体命令和文件责任由 design/implement 继续展开；未发生的结果不得预填为通过。

## 7. Canonical 引用与本轮差额

Requirements、Design、Test 的发现入口是 `docs/requirements/README.md`、`docs/design/README.md`、`docs/test/README.md`。本批预计命中现有 Codex/Skill distribution 的共享发现根、安装与证据分层单元，以及 task-delivery lifecycle 的发布责任单元；具体 complete units、必要关系和本轮差额由 candidate assessment 与后续 Docs Plan 确认。

Architecture 从 `docs/architecture/README.md` 进入。本批真实改变的是私有 release consumer 对当前公共发布 owner 的引用，以及版本 producer/consumers；是否新增 Architecture 影响必须由独立 candidate/final assessment 判断，不能因没有新增公共 Skill 就自行认定无影响。

共享 root/index/manifest、历史 Test 和已发布版本事实不因普通版本递增机械改写。实际未验证的真实 Task 采用、正式 Release、业务项目采用和累计矩阵不在本批声称完成。
