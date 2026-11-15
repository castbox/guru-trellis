# D1：v0.7.0-guru.10 完整可分发源

## 1. 整体来源与术语

整体权威是[Task PRD](../../prd.md)，公共 accepted_scope 绑定该文件当前 revision。本批 Delivery 为 `60d7e5c9-e62e-4a92-bc33-ef7228202be0`，profile 为 pull_request；scope_ref 选择整体 R1、R2、R5、AC1。整体 R3、R6、R7 的顺序、交付和后继边界继续适用，不把 R4 的实际采用提前纳入本批。

| 来源 | 章节及角色 | 本批用途 |
| --- | --- | --- |
| https://github.com/castbox/guru-trellis/issues/861 | 完整正文，要求 | 无其它 Issue 前置、最新 main 和准备/发布边界 |
| `.agents/skills/release-guru-trellis-version/references/contract.md` | Stage 1 / Complete Source Before Actual Adoption，设计约束 | 完整源先交付，实际 source_locked 后继采用 |
| `.trellis/workflow.md` | 当前 Intake、Phase 1–3，设计约束 | 原 owner 顺序及已取消默认独立 Wording 的迁移 |
| `trellis/guru-team-extension.json`、`trellis/presets/guru-team/source/trellis-source.json` | 当前事实 | Guru 与 Fork 分离的版本轴 |
| `README.md` 的来源与版本选择、workflow README 的 Installation、preset README 的 Apply And Verify | 当前事实 | 正式安装条件、当前与历史版本说明及同源 ref |

“来源样本”是原 verifier/installer 创建的一个临时项目，用来验证当前源的可分发行为；它不代表本 Task checkout 已正式采用，也不代表远端目标版本已发布。

## 2. 整体与本批目标、非目标

整体准备还需真实采用和全部收尾。本批独立目标是交付一个完整、可安装、版本直接消费者一致的 `.10` 来源，供后继 tools owner 从真实 delivered 的干净提交消费。

本批覆盖 canonical extension、直接升级输出生产者/消费者、公开版本入口、私有发布消费者及其实际回归、完整源和样本投影验证，以及真实命中的知识差额。当前目标 tag/revision 为 `v0.7.0-guru.10` / `0.7.0-guru.10`；前驱为 `.9`；Fork CLI 保持 `0.7.0-castbox.6` 和现有 source lock。

本批不提前执行 Task checkout 的正式 source_locked 更新，不修改真实 installed 资产来消除版本观察，不创建 D2，不执行 tag、smoke、Release、Issue closure 或业务升级，不扩累计多平台矩阵。

## 3. 本批起点、前序结果、依赖与剩余责任

这是本 Task 的首个 Delivery，没有前序 delivered 结果。准备从已同步的 main 来源建立独立 checkout；当前源及已安装版本均为 `.9`。版本变更后，Task checkout 的旧 installed 观察保留，不能作为 `.10` 采用通过。

本批源及来源样本须自行完整通过适用验证；自身缺陷不能转给 D2。本批 delivered 后，原 Completion 对仍未实施的 R4 真实采用返回 additional_delivery_required，原 Creation 才建立 D2。D2 使用本批真实完整干净来源，独立规划/审核后完成真实采用及全部安装 after 的交付。全部准备满足后才进入 Task Completion、no_mutation Closure 和 Finish。Stage 2 再获取届时最新 main 冻结候选。

## 4. 本批调用方、场景与流程

| 场景 | 条件与调用方 | 行为与可观察结果 |
| --- | --- | --- |
| D1-SC1 | 发布准备 owner 更新 Guru 目标版本 | canonical manifest 与升级 owner 的目标常量、公开输出 schema、独立 stop consumer 和示例共同指向 `.10`，形状与来源家族支持保持 |
| D1-SC2 | 安装者读取当前安装说明 | 未发布 `.10` 的正式安装有 Release 存在条件；`.9` 为前驱；workflow/preset 使用同一真实 ref，历史事实不被全局替换 |
| D1-SC3 | 私有发布 owner 调用当前公共流程 | 私有合同使用当前 Author/Clarify/Architecture/Approval 职责及后继链，不再要求默认独立 Wording；Stage 2 及逐项副作用边界保持 |
| D1-SC4 | 原验证 owner 从本批源码建立来源样本 | 一个 focused Codex 临时项目完成当前源安装/update/reapply，再在同一项目补齐 Claude/Codex/Cursor；完整受管集、installed validator 和各声明根投影检查可观察 |

## 5. 完整行为、条件与约束

- **D1-R1**：目标版本的生产者与直接消费者成套更新。至少包含 canonical manifest、`guru-upgrade-installation/runtime/owner.py` 的 TARGET_GURU、该包 public upgraded output schema、包内和 shared stop consumer schema、active upgraded example。现有正常来源家族及输出结构保持，不新增长期双读或另建版本 authority。
- **D1-R2**：三个 README 只更新当前版本、前驱和真实发布集合说明；`.8` 等仍有效历史叙述保留历史角色。`.10` 未发布时不能写成 stable/latest 或将源码检查说成正式发布已通过。
- **D1-R3**：私有发布合同对齐当前公共 owner 顺序，保持同 Task 的完整源→delivered→Completion→后继采用，不插入早提交、early Draft、重复 Check 或安装捷径。Shared 私有正文与 Codex/Claude/Cursor 私有发现副本一致，仍不进入公共扩展分发。规范性来源的唯一 retain/change 处置由本批 design 第3节展开。
- **D1-R4**：运行 source validator，并在一个来源样本上证明完整安装、update/reapply、声明三平台投影、CLI/source lock、实际字节、可执行位、provenance 和 sidecar。使用现有 verifier 的公开 local sample 边界，不手修临时产物。平台比对针对该完整样本，不将 Task checkout 的 `.9` discovery/installed 观察冒充 `.10` 实际采用。
- **D1-R5**：新增或调整的回归观察真实生产者及其直接消费者。版本值只在当前目标语义中更新；历史 fixture 与正常 dirty 来源拒绝语义保持。私有迁移回归验证当前链和不分发私有 Skill 的真实入口，测试不能直接种入其被测 producer 应产生的结果。
- **D1-R6**：知识维护仅处理真实命中的完整单元和必要关系。原 RDT/Architecture owners 在各自边界整合/readback；本批规划不修改共享导航，不生成发布 ledger、状态提交或 PR/Release body handoff。未验证的真实目标、远端或平台行为如实说明。

## 6. 本批验收、验证方式与未决项

| 验收 | 入口、输入与预期结果 | 证明边界 |
| --- | --- | --- |
| D1-AC1 | 检查目标版本生产者→实际 upgraded 输出→三处 schema/consumer 及 active example；当前版本与后继版本选择一致 | 不只比较字面，不运行真实业务迁移 |
| D1-AC2 | 三个 README、私有四份合同及实际命中回归；当前顺序、历史身份、Refs-only 和私有排除分发一致 | fixture 不代表真实 AI 独立审核或远端成功 |
| D1-AC3 | canonical source validator；一个 focused Codex 来源项目及同项目三平台补充；目标 own installed validator、完整 managed 字节/mode/manifest/workflow/lock 与投影检查 | 来源样本保留 local sample/dirty 观察；不证明 source_locked、真实 Task checkout 采用或完整矩阵 |
| D1-AC4 | 原完整 committed Check/Branch Review、Delivery Review、Publication、Merge 实际结果 | 只有真实 delivered 才形成 D2 可消费的来源；不表示 Task Completion 或 Stage 2 通过 |

需求层没有未决产品选择。来源投影与验证采用原公开能力；若本批自身必须先更新真实 Task checkout 才能验证，返回原规划/Architecture owner，不能放宽采用、提交或审查门禁。

## 7. Canonical 引用与本轮差额

整体定义见 Task PRD 第5–7节；来源与版本的实际差额见本批第2、5节。`docs/architecture/04-integrations/distribution.md` 的 ARCH-INT-015 承接完整源与后继真实采用，ARCH-INT-014 承接固定 Fork 构建和来源样本边界。本批没有新增公共生命周期节点或 owner；私有消费者对齐当前公共职责的真实差额由独立 Architecture 判断，不能从自检推定无影响。

Requirements/Design/Test 的稳定入口为 `docs/requirements/README.md`、`docs/design/README.md`、`docs/test/README.md`；具体命中单元和必要引用在 design 与 implement 的 Docs Plan 展开。现有行为不因 release 版本递增而自动产生新的业务需求或全局知识版本。当前规划尚不声明工程验证、真实采用或正式发布已完成。
