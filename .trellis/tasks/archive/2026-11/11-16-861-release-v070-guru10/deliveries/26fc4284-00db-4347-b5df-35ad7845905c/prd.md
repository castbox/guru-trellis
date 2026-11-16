# D2：准备 checkout 的正式工具采用需求

## 1. 整体来源与术语

整体权威为 [Task PRD](../../prd.md)，accepted_scope revision 为 `sha256:66862ed96338b66cc4adeccf7ad1b359b484cdff64fa2e381995d9d505729b47`。本批 Delivery `26fc4284-00db-4347-b5df-35ad7845905c` 选择整体 R3、R4、R5、AC2、AC3、AC4；R6/R7 的完整交付和后继发布边界继续约束本批，不把 Finish 或 Stage 2 纳入本批实现。

| 来源 | 章节与角色 | 本批用途 |
| --- | --- | --- |
| https://github.com/castbox/guru-trellis/issues/861 | 完整正文，要求 | 没有其它 Issue 前置；准备、最新 main 正式候选和发布边界 |
| `.agents/skills/release-guru-trellis-version/references/contract.md` | Stage 1、Complete Source Before Actual Adoption、Whole Preparation Completion、Independent Mutation Confirmations，设计约束 | D1 delivered 后新建 D2，真实 source_locked，全部 installed after 独立交付 |
| `.agents/skills/guru-upgrade-tools/references/contract.md` | Entry、Forward behavior、AI Review Gate、Deterministic execution、Recovery，设计约束 | 单 checkout 工具更新、完整来源、维护 API、保留和恢复 |
| https://github.com/castbox/guru-trellis/pull/865 | 原 Merge 与公共 Delivery 结果，事实 | D1 已 delivered，merge `dc300d26ed638d97a303753958f85eaa645f2067`，reviewed head `b3525d4b052f79f7d9cb4a18f827ff7c990f1983` |
| `docs/architecture/04-integrations/distribution.md` | ARCH-INT-006/014/015，设计约束 | 版本轴、固定 Fork、来源交付与真实采用分层 |

“真实采用”仅指准备 checkout 的原 tools owner source_locked 操作及验证；不代表发布后主目录安装或业务仓升级。“来源样本”保留 D1 local_workflow_sample 的原观察，不能替代本批真实目标结果。

## 2. 整体与本批目标、非目标

整体准备仍需真实采用、各 Delivery 交付及原 Completion/Closure/Finish。本批独立目标是在当前准备 checkout 正式采用 D1 已交付的完整干净 `.10` canonical 来源，并交付全部实际 installed after 和必要验证。

唯一目标为 `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/861-release-v070-guru10`，沿用同一 Task、generation、branch 和 checkout。目标当前 installed 为 `.9`，canonical 已为 `.10`；本批消除该实际采用差额，不能手改 manifest 或仅重写版本记录。

本批不修改已交付 D1 canonical 行为，不创建第二 Task/branch/worktree，不转换历史 Tasks，不更新 peer 或保留主目录 `/Users/wumengye/Documents/GoProjects/guru-trellis`，不执行 Finish、tag、Release、Issue closure、清理、业务升级或生产部署。完整累计 Release 矩阵仍由 Stage 2 的实际合同承接。

## 3. 本批起点、前序结果、依赖与剩余责任

D1 的公共结果为 `delivery:dc300d26ed638d97a303753958f85eaa645f2067`，实际 candidate head 为 `b3525d4b052f79f7d9cb4a18f827ff7c990f1983`；原 Merge 已核两 parent、消息和 main 可达。原 Completion 返回 `additional_delivery_required / actual_source_locked_adoption_unimplemented`，所以这是未实施工作，不是外部待证。

本批来源使用该 delivered head 的完整 canonical tree。执行时核来源 HEAD、`trellis/**` 无未提交/未跟踪差额、实际 remote 和版本；不要求 Task 规划元数据 clean，也不把其 dirty 等同于 canonical dirty。固定 Fork lock 为 `e3793251fad8bd261d0c370d408c7675b9f6a140`，CLI `0.7.0-castbox.6`；实际配对包和构建证据仍须由原 tools owner 检查。

本批完成 installed after 的工程、知识、TaskCommit、独立完整 Review 和交付后，原 Completion 才重新判断整体准备。reference_only Closure、Finish 簿记和 Stage 2 最新 main 候选均仍有自己的原 owner 与副作用边界。

## 4. 本批调用方、场景与流程

| 场景 | 条件、调用方与动作 | 可观察结果 |
| --- | --- | --- |
| D2-SC1 | D1 已 delivered；实施 owner 在本批规划经独立 Architecture/Approval 并接受后，加载完整来源的 tools owner | 只读 preview 识别真实目标、旧来源、平台、受管差额、维护 API 与未完成事务 |
| D2-SC2 | 来源和实际写集经审查；tools owner prepare 一次，展示目标/来源/写删集合并确认后 invoke | 真实 `.10` 安装由原 public maintenance 与 Guru installer 产生，完整 after/provenance/CLI/lock 一致 |
| D2-SC3 | 安装后；实施 owner 从目标自身入口验证并读取同一 Task/Delivery | resolver、installed/native 入口可用，原 Task/session 与用户配置、peer/common runtime 保留，平台投影和 drift 成立 |
| D2-SC4 | 普通冲突、stale 或部分操作失败；原 tools owner 从同一冻结输入恢复 | 保留真实失败和未处理差额；无普通 apply、手工 manifest 修补或重建 operation 捷径 |

## 5. 完整行为、条件与约束

- **D2-R1 来源**：采用 D1 的真实 delivered head，`dependency_mode=source_locked`；完整 Guru 来源和该来源自己的 Fork lock、CLI/Core 包、构建及 API1.0 相符。若需构建，使用当前 pnpm，不固定执行版本或更改 package-manager 声明。来源失配停在原 owner。
- **D2-R2 写入边界**：只更新所选准备 checkout 的工具、workflow、Skills、spec 和受管平台投影。平台选择来自目标 exact selection，不从 source 推断；workflow 使用原 custom provider 和完整 canonical bytes。AGENTS 保留用户正文，由原 renderer 处理 Guru block。未知修改和 sidecar 由原冲突机制审查，不能覆盖掩盖。
- **D2-R3 保留与恢复**：Task、archive、workspace、session、public Delivery facts、用户配置和 peer tools/common pointers 不在安装写集中；允许原 tools 自身必要的目标 runtime pointer/recovery 写入。先检查相交未完成事务；部分失败仅原冻结 operation 恢复，不重新 prepare、不转换历史资料。
- **D2-R4 实际验证**：核目标自身 resolver、installed validator、实际 native continuation、manifest/source/version/CLI/lock、完整受管集合 bytes/mode、声明公共 roots、ownership、reapply/drift 和零未处理 sidecar。临时样本、source validator 或返回 exit0 均不能替代真实目标结果。客户端真实 Agent 和业务效果只按实际观察报告，不从 native 脚本或投影推断。
- **D2-R5 完整交付**：本批交付全部 installed after，保持 D1 历史和固定前序范围；原 TaskCommit 后新独立 reviewer 审完整本批差额及必要未改 consumers，真实 check/full_review 后才 readiness/Publish/Merge。准备 PR 仅 Refs #861；本批不宣布整个 Task 或发版完成。

本批引用 design 第3节的唯一来源设计处置。正常错误、stale/mismatch 和明确保留边界属于本批；不扩攻击、压力或非常规 crash hardening。沿用原工具能力，不新增状态、脚本、公共 API 或长期台账。

## 6. 本批验收、验证方式与未决项

| 验收 | 要求/场景 | 入口与预期观察 |
| --- | --- | --- |
| D2-AC1 | R1 / SC1 | 原 public preview/prepare 识别本目标、D1来源与锁定 Fork 配对，无相交未决事务；不接受 local_candidate 替代 |
| D2-AC2 | R2/R3 / SC2/4 | 原 invoke 实际 tools_upgraded，unverified 不含 formal_fork_source_lock；完整安装由原 producer 产生，冲突和恢复有真实结果 |
| D2-AC3 | R3/R4 / SC3 | 目标自身 resolver、installed/native、完整 bytes/mode/root/provenance 和 drift/reapply 观察；Task/session、用户配置、peer/common 保留；无未处理 sidecar |
| D2-AC4 | R5 / SC3 | 本批全部 installed after 经完整独立 Review 与真实 Delivery；原 Completion 另评整体，#861 保持 OPEN |

目前没有未决产品选择。实际 preview 中的 per-path 冲突和未完成事务由原 tools owner 在安装前解决；尚未执行 preview/prepare/invoke，不预填通过。当前规划完成后停在接受/Activation及实际安装边界。

## 7. Canonical 引用与本轮差额

RDT 稳定入口为 `docs/{requirements,design,test}/README.md`；R724/D724/T724 的 `current/codex-skill-distribution.md` 定义现有共享发现根、目标选择、受管退出、用户保留和证据分层。本批是现有维护能力在本 checkout 的实际采用，不新增这些能力或重写 #724 的历史验收。

Architecture 由 `docs/architecture/README.md`、`00-foundation/design-constitution.md`、`06-governance/change-contract.md` 和 ARCH-INT-006/014/015 承接完整来源/真实采用分层。实际影响由独立 candidate/final Architecture 判断。没有新知识定义时不建空贡献或修改共享导航；真实命中差额经原 RDT/Architecture owners 在 TaskCommit 前维护和读回。
