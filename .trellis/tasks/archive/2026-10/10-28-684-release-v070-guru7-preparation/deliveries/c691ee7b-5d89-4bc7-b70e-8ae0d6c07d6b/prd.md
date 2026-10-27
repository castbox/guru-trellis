# D1：v0.7.0-guru.7 版本、文档与真实 dogfood 准备需求

## 1. 整体来源与术语

本批属于 Task `684-release-v070-guru7-preparation` 的 generation `0`，Delivery id 为 `c691ee7b-5d89-4bc7-b70e-8ae0d6c07d6b`，公共 `planning_root` 为 `deliveries/c691ee7b-5d89-4bc7-b70e-8ae0d6c07d6b`。

整体 authority 为 [Task PRD](../../prd.md)，由公共 `accepted_scope` 绑定其实际 revision。本批 `scope_ref` 选择 R-01、R-02、R-03、R-04、R-05、R-06、R-08。R-07 是 Completion 后原生命周期 owners 的责任，不纳入本批业务交付，也不制造后继空 Delivery。

| 来源 | 章节、角色与用途 |
| --- | --- |
| [#684](https://github.com/castbox/guru-trellis/issues/684) | 完整需求来源；Stage 1 定义本批准备，Stage 2 与发布收尾约束本批不得提前宣称的结果 |
| [私有发布合同](../../../../../.agents/skills/release-guru-trellis-version/references/contract.md) | 已约定设计；完整两阶段、真实 dogfood、双完整 Review、串行 promotion、Refs-only 及独立副作用边界 |
| [当前 workflow](../../../../workflow.md) | 全局原 owner 和 typed route 约束；每 Delivery 的 Author/Architecture/Wording/Approval/Activation 与实施、交付顺序 |
| [manifest](../../../../../trellis/guru-team-extension.json)、[Fork lock](../../../../../trellis/presets/guru-team/source/trellis-source.json) | 当前版本、依赖及受影响定义；不能用相同 CLI 版本代替匹配构建来源 |
| [public-docs](../../../../spec/docs/public-docs.md) 的 Install and Upgrade Prompts | 当前公开文档约束；本批修正版本与安装来源表述，保留历史结果和无关合同 |

`repository tag`、`extension revision`、CLI/Core、固定 Fork commit/tree 和内部知识 identity 是不同概念。`source_locked` 沿原 `guru-upgrade-tools` 定义，更新真实 tools，不转换历史 Task。

## 2. 整体与本批目标、非目标

整体目标是完成 #684 的 Stage 1 准备。本批以一个独立的 Refs-only 准备 PR 交付：统一 `.7` 的 canonical/maintenance version、公开来源与实际 dogfood；必要知识差额由原 owners 收敛；晋升前后完整质量与独立 Review 不省略。

背景差额为：`.6` 已正式发布，当前源码版本仍为 `.6`，公开文档仍把 `.6` 当未发布候选。当前 installed manifest 的字符串和 dirty provenance 不能证明其实际受管内容、匹配工具链或 `.7` 安装已成立。

本批不增加流程能力，不修复其它 Issue，不改 Task/Delivery API、公共 Skill I/O、上游或全局包，不转换历史 Task，不维护业务仓库或部署生产。Stage 2 的最终 candidate、predecessor 安装清退、secret scan、tag、smoke、Release、两个选定本地目标的发布后收尾和 #684 关闭不属于本批结果。完整累计矩阵、所有 native-host、真实业务升级和 Himora 同因证明维持原 owner 边界。

## 3. 本批起点、前序结果、依赖与剩余责任

这是本 Task 的首个 Delivery，尚无前序交付。开发 baseline 为已核定的 `main` 内容；后续由原 content-base projection 固定 B，不能把后续移动的 PR target 当作内容基线。当前没有本批 implementation、Check、full_review、readiness、Publication 或 Delivery 结果。

当前 canonical extension 为 `0.7.0-guru.6`，目标为 `0.7.0-guru.7`；目标 repository tag 为 `v0.7.0-guru.7`，前驱稳定 tag 为 `v0.7.0-guru.6`。Fork 保持 `79a97ed60fe19e8f287eaddfa74722b5250ced35` / CLI/Core `0.7.0-castbox.5`。`.trellis/.version` 继续记录 CLI。

本批依赖完整 matching Guru 来源、其 source-lock 的干净 Fork checkout 与实际匹配构建。真实 tools 更新若需干净已提交准备来源，采用原 early-commit/source-acquisition 路线，每次提交仍由原 TaskCommit owner 承接；不能从 dirty 工作树伪造 clean source，也不能手改安装 manifest 跳过更新。

交付后，Task Completion 仍须整体评审准备内容及实际证据；Closure、acceptance-finish Architecture、Finish、Cleanup 依原序收尾。#684 的 Stage 2 在准备内容及归档合并之后才 fresh 冻结唯一候选，旧准备 HEAD 和旧发布 pass 不转移。

## 4. 本批调用方、场景与流程

| 场景 | 调用方与前置条件 | 行为及分支 | 可观察结果 |
| --- | --- | --- | --- |
| D1-S1 版本与来源准备 | 发布维护者从当前 `.6` 源码准备 `.7` | 核 manifest/maintenance const/公开来源；稳定安装使用已发布 `.6`，试用候选使用真实远端完整 SHA | `.7` 目标、`.6` 稳定来源、CLI `.5` 与各自 lock 没有混用 |
| D1-S2 实际 tools 收敛 | 原 tools owner 已具备完整干净匹配来源 | 只读 preview、一次 prepare、`source_locked` 执行和真实目标验证；普通缺失或失败留原 owner 恢复 | 当前 Task dogfood 的版本、provenance、CLI、managed assets 和原 owner 要求的 native entry 有实际结果；用户状态保留 |
| D1-S3 知识与质量整合 | 本批规划完成并经接受后进入 implementing | 完整候选检查、原 TaskCommit、晋升前完整独立 Branch Review；零开放 P0–P3 后串行 Architecture/RDT promotion；实际 after 再 Check/TaskCommit/完整 Review | 两组完整审查分别覆盖其当前字节；候选状态或旧 Review 不替代晋升后结果 |
| D1-S4 准备 PR | 晋升后完整 Review 与 Architecture publication 适用 | 原 Delivery Review 审查范围、证据、剩余责任及中文 Refs-only payload；Publish/expected-head Merge 使用独立边界 | 一个真实准备 PR 合入 main，不关闭 #684，不宣称正式发布通过 |

输入、正文、来源或实际内容变化时，返回受影响最早原 owner；结果未知先回读同一操作，不重复创建/提交/推送/合并。无关问题不能扩为本批修复支线。

## 5. 完整行为、条件与约束

**D1-R1／整体 R-01、R-02／D1-S1**：canonical manifest、maintenance target/const schema 及命中断言使用 `0.7.0-guru.7`。README、workflow/preset README 与项目 public-docs 使用唯一当前映射。准备期默认稳定 workflow marketplace 和 preset 同指已发布 `.6`；候选使用同一远端可寻址完整 SHA，读取该 SHA 自身锁定的 Fork 构建。`.7` tag 未创建和核验前不能作为 provider。保留历史 `.5`、`.6`、前序功能与未验证事实的适用范围，不把全局替换当语义修订。

**D1-R2／整体 R-01、R-03／D1-S2**：CLI/Core 仍为 `0.7.0-castbox.5`，source lock 不因软件 `.7` 准备而更新，内部知识 identity 也不随软件版本递增。通过原 `guru-upgrade-tools` 的 `source_locked` 路线更新实际 dogfood。实际 changed scripts/schema/projections/manifest 纳入本批候选，完整 matching set 统一采用。合法已提交前驱来源只有在原合同规定的 managed bytes 与 source-lock 等价证明成立时才可接受；不能追逐自引用 HEAD。

**D1-R3／整体 R-02、R-03、R-08／D1-S1、S2**：canonical workflow/preset/overlay 是可复用内容的长期来源；受管副本通过原 installer/overlay 更新。项目 public-docs 是本仓库维护的文档规范。检查声明 Shared/Codex/Claude/Cursor 投影、ownership、mode、drift 与 sidecar。保留 Task/archive/workspace/session/user config 和无关工作树。真实安装不能由 source validator、版本号或 throwaway 替代；普通 guard 不授权历史数据转换或绕过。

**D1-R4／整体 R-04、R-05／D1-S3**：所有规划正文与 Docs Plan 保持稳定；已约定接口、顺序、角色及兼容约束由未来 design 第3节维护唯一 retain/change/reject 处置，PRD 不另建第二设计矩阵。Architecture 和 RDT 的实际影响、贡献与 promotion 由原 owner 判断，不为发版制造空 ADR、空 contribution 或全局知识版本。晋升前后各有一次当前完整 Phase 2、原 TaskCommit 与完整独立 Branch Review。即使维护 owner 返回真实 no-change，也不制造空提交或用前一次 Review 代替规定的后一次门禁。

**D1-R5／整体 R-06、R-08／D1-S4**：原 Delivery Review 编写并审核中文具体 title/body、安全及部署影响、实际验证和剩余 Stage 2。PR 仅 `Refs #684`，没有关闭效果；原 Publish 处理精确 push/PR/Ready，原 Merge 执行 expected-head merge。一个操作的确认不授权下一独立操作，授权不进入任何记录。

**D1-R6／整体 R-08／全部场景**：不创建发布状态账本、release-notes、PR/Release body handoff、动态 checklist 或自引用 metadata commit。FAIL、SKIP、stale/mismatch 均如实保留并阻止其依赖动作；script/checker 成功不替代 AI semantic Gate。阶段和工程事实的采用依原适用性合同，不无因重复已适用检查，不把旧 semantic pass 当当前判断。

## 6. 本批验收、验证方式与未决项

| 验收 | 对应要求/场景 | 入口、输入与预期观察 |
| --- | --- | --- |
| D1-AC1 | D1-R1/R2；S1 | 读取实际候选 manifest、maintenance schema、README/public-docs、source lock 和 CLI record；`.7` 目标、`.6` 稳定来源和 CLI `.5` 明确，准备不冒充已发布 |
| D1-AC2 | D1-R2/R3；S2 | 原 tools owner 在真实 dogfood 上执行 `source_locked`，读取实际版本/provenance/CLI/managed set/native 结果并核用户状态保留；旧 manifest、隔离样本或 throwaway 不替代 |
| D1-AC3 | D1-R3；S1/S2 | 原 source/installed validators、声明平台 parity、ownership、overlay/preset reapply、drift、mode 与 sidecar 检查；canonical 与实际受管内容一致，所有 sidecar 按原合同处理 |
| D1-AC4 | D1-R4；S3 | 原 Check、TaskCommit、独立完整 Review 与串行 Architecture/RDT owner 的实际结果；晋升前后完整范围各覆盖，零开放 P0–P3，after 内容重绑并复核 |
| D1-AC5 | D1-R5/R6；S4 | 当前 Architecture publication、Delivery Review/readiness、Publish、expected-head Merge；一个中文具体 Refs-only 准备 PR 合入 main，证据层次与未验证边界真实，#684 仍 Open |

本表是待执行验收，不预填通过。两轮完整实质审核要求保持；晋升前成环的正式结果记录按 design 第6、7节的既有 workflow-defect-recovery 处理，真实 typed exit 与缺失 public 记录分别说明，第二轮仍取得真正 public Check/full_review。完整干净来源、匹配构建、实际安装及定向验证属于后续实施依赖，缺失时由各原 owner 处理，不能删除本批责任。

## 7. Canonical 引用与本轮差额

| Authority | 具体章节及用途 | 本批差额 |
| --- | --- | --- |
| [Task PRD](../../prd.md)，R-01..R-06、R-08 | 本批唯一整体范围与可观察验收来源 | 本批全量准备内容；R-07 留给 Task 后续 lifecycle，不改变整体 scope |
| [Requirements knowledge unit](../../../../../docs/requirements/current/knowledge-maintenance.md)，四 profiles/日常闭环与晋升、阶段适用版本 | 原知识 writer、隔离候选、实际 promotion 与 no-change 责任 | 按原 owner 判断本次 release 文档的真实知识差额，不新增流程能力或全局版本 |
| [Design knowledge unit](../../../../../docs/design/current/knowledge-maintenance.md)，D331-02/04、D638 | 原 owner 的 source/proposed/shared-current 分界和真实 after 重绑 | 本批复用该机制；私有 release 合同增加的双 committed Review 次序必须保持 |
| [Test knowledge unit](../../../../../docs/test/current/knowledge-maintenance.md)，T638 及证据层次 | 当前候选、实际晋升、最终质量和工程事实的证据边界 | 只证明本批命中范围，不重跑既有能力的全部原生实验，也不继承其 pass |
| [Architecture entry](../../../../../docs/architecture/README.md)、[change contract](../../../../../docs/architecture/06-governance/change-contract.md) | 当前 authority、独立 candidate/final Planning、single-writer 和 project-check | 交原独立 Architecture owner 对真实 candidate facts 判断；本 PRD 不预选影响或 path |
| [Public docs spec](../../../../spec/docs/public-docs.md)，Install and Upgrade Prompts | 软件版本、稳定/候选来源、Fork 配对及真实验收边界 | 改正当前 `.5` 稳定来源与 `.6` 未发布目标的过期说明，保留无关和历史定义 |

实现、Check 和 Review 前实际读取命中正文与必要条件。共享定义可定位引用，本批需求、完整条件和责任已在上文展开。
