# #880 Issue 责任层与验收场景收敛需求

## 1. 整体来源与术语

公共 accepted_scope 为[整体 Task PRD](../../prd.md) R1–R7 / AC1–AC2 的 `sha256:b724b601e15e851fb09bed836fa5fb0358ce9953cd4bfd2129c1746d82ec26c3`。本 Delivery 的 planning_root 为 `deliveries/ebed2ee9-2ddc-457a-9f17-a7dc8e0e490f`，全量覆盖整体范围。

| 来源 | 章节与角色 | 本批用途 |
| --- | --- | --- |
| [Issue #880](https://github.com/castbox/guru-trellis/issues/880) | 完整正文、复审评论；要求 | 责任层可组合、验证/部署/业务发布分离、验收场景去重及两档验收 |
| [Issue #868](https://github.com/castbox/guru-trellis/issues/868) | 已交付前序；要求 | 复用原有边界、结果/证据与持续去重规则，不重做 |
| `trellis/skills/guru-team/packages/guru-clarify-requirements/references/issue-content.md` | 当前唯一 Issue 内容规范；设计约束 | 修改 Issue 责任、环境/发布和场景集合规则 |
| `trellis/presets/guru-team/spec/workflow/quality-guidelines.md#test-and-validation-value` | 跨阶段验证方法；设计约束 | 保持验证证据、去重、复用与停止外推的单一来源 |
| `trellis/skills/guru-team/packages/guru-review-change-request/references/issue-intake.md`、`guru-create-issue/SKILL.md` | 原 consumer；设计约束 | Readiness/Create Issue 的同一完整正文检查 |
| `docs/requirements/current/issue-content.md`、`docs/design/current/issue-content.md`、`docs/test/current/issue-content.md` | RDT current；设计约束 | 以原 RDT owner 承接本轮能力差额 |
| `docs/requirements/current/behavior-validation-method.md`、`docs/design/current/behavior-validation-method.md`、`docs/test/current/behavior-validation-method.md` | RDT current；设计约束 | 保持跨阶段验证方法归属 |
| [Issue #826](https://github.com/castbox/guru-trellis/issues/826)、[#747](https://github.com/castbox/guru-trellis/issues/747) | 关联方法；建议 | 复用真实 Agent 行为验证入口，不把整项完成作为硬前置 |

本批的“责任层”是 Issue 在自身权责边界内承诺的可观察结果层级；“验收场景”是足以判断一个独立结果或风险的输入、动作和观察。场景不等于验证层级，也不按 consumer、阶段或测试方法重复生成。

## 2. 整体与本批目标、非目标

整体问题是现有规则虽已禁止沿调用链外推，却未在 Issue 首次整理时清楚区分组件合同、跨组件结果、验证证据、服务部署、共享环境和业务发布操作；本 Issue 自身首轮验收又重复拆分同一 Agent 行为，说明场景集合也需要最小充分判断。

本批目标是全量交付 R1–R7：在原共享规范中定义可组合责任层、必要承诺保留、验证/部署/发布分离和独立风险场景；在原 Clarify、Readiness、Create Issue 中落实完整正文判断；扩展现有示例/eval；同步 RDT、canonical、dogfood 与声明平台安装投影。

本批不新增固定 Issue 类型、固定场景数、关键词扫描门禁、独立审批、证据账本、评测平台、部署平台、公共 schema/DTO/typed exit 或完整安装/Release 矩阵，也不批量改写历史 Issue。

## 3. 本批起点、前序结果、依赖与剩余责任

本 Delivery 是 Task 首个 Delivery，没有前序 Delivery。起点为固定基线 `main@76198a53b4da989b66d2e5f135ff4d2b703ca3cf` 和已接受的 root PRD。

现有 `issue-content.md`、`quality-guidelines.md`、原 owner contracts、RDT current 和验收边界 fixture 是已存在能力。本轮只补责任层/场景集合差额及其分发，不重建通用最小充分、完整审核或安装机制。

本批承担整体 AC1/AC2 的全部实现与工程结果。仅真实 Agent 使用其他仓库或完整 Release 矩阵不在本批可执行边界内；该证据若未取得须在整体 Completion 前如实保留，不能由文档或静态测试替代。

## 4. 本批调用方、场景与流程

| 场景 | 调用方与前置 | 本批处理 | 可观察结果 |
| --- | --- | --- | --- |
| D1-S1 组件边界 | Issue 作者、Clarify；只有组件承诺 | 识别下游、共享环境和部署措辞是否属于本 Issue | 正文不追加无依据的整站 E2E、共享部署或逐 Issue 发布 |
| D1-S2 混合责任 | Issue 作者、Clarify；同时有组件、联合/目标环境和业务发布 | 组合必要责任层并区分结果、证据、部署与发布 | 必要环境结果保留，业务发布不自动产生部署义务 |
| D1-S3 原审核 | Readiness/Create Issue；完整 S1/S2 草稿 | 按同一规则检查完整标题、正文和验收 | 越界义务回原 writer；未修订不创建 |
| D1-S4 场景去重 | Clarify/Readiness；已有草稿含多条同一行为场景 | 以独立风险判断场景集合，合并重复证明 | 同一 Agent 行为不按创建、复审、方法、阶段重复拆分 |
| D1-S5 采用 | 原 RDT/install/tools owner；实现和测试完成 | 同步 current、dogfood、平台与安装投影 | 文件、引用、mode、drift、sidecar 和 session 保持可验证一致 |

## 5. 完整行为、条件与约束

**D1-R1 责任层：** 组件/服务、调用方/界面、跨组件业务和发布/环境结果可以组合。不能按标题词机械分类。组件边界不自动承担调用方接入、整站联调或部署；调用方不能用替身成功冒充被调用组件或完整链路通过。

**D1-R2 必要承诺：** 有效需求明确包含组合行为或目标环境结果时，保留最小相应证据；只有该环境能判断或需求明确要求时才要求环境证据，并如实写原因、归属和未验证边界。

**D1-R3 动作分离：** 验收定义结果，证据证明结果，部署/环境/发布 owner 负责指定版本的运行结果。普通 Issue 不默认共享 test 部署；业务“发布模板/配置/同步配置”不能仅由名称推导服务部署。

**D1-R4 场景集合：** 每场景对应独立可观察结果或风险；同一场景可以有多条件和例外。同一行为不得因创建、复审、验证方法或阶段不同拆成多个重复场景；其他入口/阶段只在存在必要差异时增加场景。

**D1-R5 原 owner：** 三个原 consumer 实际读取同一正文并在原门禁执行。Clarify 负责最终正文；Readiness 在原十维返回内容缺口；Create Issue 在首次写前返回 `refresh_review`。不增加平行 writer。

**D1-R6 单一来源：** `issue-content.md` 单写 Issue 责任和场景；`quality-guidelines.md` 单写跨阶段证据。原 owner 只薄引用。受影响 RDT/Architecture 由原 owner 维护；受管副本由原 tools/install owner 分发。

**D1-R7 验证：** 扩展现有 acceptance-boundary fixture 和实际 native Agent 观察，不新建评测平台。固定文字、引用、评论存在、分发或脚本通过不能替代语义判断。

兼容约束：现有 Issue 内容 API、Skill id、profile、typed exit、schema、DTO 和原动作恢复不变。`issue-content.md` 的路径/引用保持可被原 consumer 投影加载。没有业务数据、持久化、服务配置或运行时状态迁移。

## 6. 本批验收、验证方式与未决项

**D1-AC1（D1-R1–R4/R7）：** 一个去敏混合草稿同时含组件结果、未要求的下游整站 E2E/共享部署/逐 Issue 发布、明确要求的目标环境结果和业务“发布模板/配置”。真实 Agent 经原 Clarify 及创建前审核处理完整正文后，应删除无依据完成条件、保留环境承诺、区分业务发布与服务部署，并只保留独立场景。固定文本、引用、评论存在或机械检查不能代替。

**D1-AC2（D1-R5/R6）：** 共享规范、原 owner 引用、现有教学/eval、RDT/current、canonical/dogfood、声明平台和安装投影一致；运行定向 distribution/reapply/drift/sidecar/package 检查。仅证明内容、引用和分发；不宣称完整 Release 或外部采用。

当前 requirements 阶段无未决需求选择。候选方案由随后 Architecture 独立判断；实现中若出现真实需求歧义回 Clarify，机制冲突回 Architecture。

## 7. Canonical 引用与本轮差额

| Authority | 当前责任 | 本轮差额 |
| --- | --- | --- |
| `docs/requirements/current/issue-content.md` | R153/R818/R868 Issue 内容能力 | 增加 R880/BEH880 责任层组合、环境/发布分离和场景集合去重 |
| `docs/design/current/issue-content.md` | Issue 内容唯一正文、原 consumer、受管分发 | 增加本次正文差额的 design/con 关系与落点 |
| `docs/test/current/issue-content.md` | Issue 内容行为与分发测试责任 | 增加混合场景 AC1 和 AC2 定向观察关系 |
| `docs/requirements/current/behavior-validation-method.md`、`docs/design/current/behavior-validation-method.md`、`docs/test/current/behavior-validation-method.md` | 共用验证方法 | 保持 quality-guidelines 单一来源，不复制验证规则 |
| `docs/architecture/README.md`、`docs/architecture/03-domains/review-sufficiency.md` | Architecture current authority 与审核充分性边界 | 候选为规则/Markdown/受管投影适配；最终影响由独立 Architecture 读取完整基线后判断 |

上述 RDT 与 Architecture 变更由原 maintenance owner 在实现和真实工程结果后维护；本 PRD 不预写共享 current 的通过状态。
