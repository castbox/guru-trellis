# #880 区分 Issue 责任层并收敛验收场景整体需求

## 1. 来源与术语

| 来源 | 角色与本 Task 用途 |
| --- | --- |
| [#880 完整正文](https://github.com/castbox/guru-trellis/issues/880)（当前更新时间 `2026-11-17T10:42:50Z`） | Direct Source／要求：责任层、验证证据、目标环境发布与验收场景去重的全部用户行为、范围和验收 |
| [#880 当前复审评论](https://github.com/castbox/guru-trellis/issues/880#issuecomment-6945131802) | 审核材料：记录验收场景过重已纳入 scope；不替代完整 Issue 正文 |
| [#868](https://github.com/castbox/guru-trellis/issues/868) 及其归档 | 已完成前序／要求：责任边界、结果与支撑证据区分及持续去重已经交付，本 Task 只补差额 |
| `trellis/skills/guru-team/packages/guru-clarify-requirements/references/issue-content.md` | 规范正文：Issue 内容、责任切面、最小验收和完整正文审核的唯一来源 |
| `trellis/presets/guru-team/spec/workflow/quality-guidelines.md#test-and-validation-value` | 规范正文：跨阶段验证责任、最小证据、去重与复用 |
| `trellis/skills/guru-team/packages/guru-review-change-request/references/issue-intake.md`、`guru-create-issue/SKILL.md` | 当前消费者：Readiness 与 Create Issue 的原审核职责 |
| `docs/requirements/current/issue-content.md`、`docs/design/current/behavior-validation-method.md` | RDT/current：当前 Issue 内容能力、验证方法责任和单一来源关系 |
| [abtest-guru #542](https://github.com/castbox/abtest-guru/issues/542)、[#543](https://github.com/castbox/abtest-guru/issues/543) | 历史观察／证据：说明首次正文未区分 Issue 自身上下文与验证/发布责任，不成为公共规范中的项目专属要求 |
| [#826](https://github.com/castbox/guru-trellis/issues/826)、[#747](https://github.com/castbox/guru-trellis/issues/747) | 关联方法／建议：提供可复用的真实 Agent 与行为验证入口，不要求其整项完成 |

“责任层”是本 Issue 在自身权责边界内承诺的可观察结果覆盖范围；“支撑证据”证明该结果；“验收场景”是一组足以判断一个独立结果或风险的输入、动作和观察。责任层可以组合，验收场景数量不按入口、阶段或验证方法机械累加。

## 2. 背景与问题

当前 `issue-content.md` 已要求组件在对外合同处验收、结果验收不自动要求真实消费方/E2E/生产采用，`quality-guidelines.md` 也禁止沿调用链外推验证责任。但 Issue 首次整理仍未明确区分服务部署、共享环境验证、业务“发布模板/配置”和目标环境结果，导致业务 Issue 后续另补“验证与发布边界”。

本 Issue 首轮修订还把同一真实 Agent 行为证明拆成创建、联合/环境保留、复审修订和验证方式等四条验收，说明最小充分规则还需要落到验收场景集合层。当前差额是：补充责任层区分，并把同一次行为证明不得拆成多个重复场景写入共享规则、原 owner 消费和现有 eval。

## 3. 目标与非目标

目标是更新共享 Issue 内容与验证规则，使原 Clarify、Readiness 和 Create Issue 能在完整正文门禁中正确判断组件、调用方、跨组件和目标环境责任；同时按独立可观察结果或风险收敛验收场景，保留必要承诺并删除无依据或重复义务。

承担范围包括共享规范、原 owner 引用与执行检查、现有教学示例/eval fixture、RDT/current、canonical/dogfood、声明平台与受管安装投影。非目标包括新增 fixed Issue type、固定场景数、关键词扫描门禁、独立审批阶段、证据账本、评测平台、部署平台、完整安装/Release 矩阵，或批量重写历史 Issue。

## 4. 真实调用方、场景与流程

| 场景 | 调用方与前置 | 触发与处理 | 可观察结果 |
| --- | --- | --- | --- |
| S1 组件 Issue | Issue 作者与 Clarify；有效需求只承诺组件结果 | 整理正文并核对下游使用、共享 test、目标环境与发布措辞 | 组件合同在自身边界验收，不自动追加整站 E2E、共享部署或逐 Issue 发布 |
| S2 混合联合/环境 Issue | Issue 作者与 Clarify；有效需求同时承诺联合接线或目标环境结果，并含业务发布操作 | 区分交付结果、验证证据、部署动作和业务发布，保留必要组合 | 必要联合/环境证据保留，业务发布不被误写为服务部署，未要求的下游义务被删除 |
| S3 原创建前审核 | Readiness 与 Create Issue；S1/S2 的完整草稿 | 按同一共享规则检查完整标题、正文和验收 | 越界完成条件回到原 writer 修订；未修订通过不进入创建写入 |
| S4 已有 Issue 复审 | Clarify 或 Readiness；已有正文含重复场景或错误边界 | 按完整 postimage 审核并去重验收场景 | 独立风险覆盖保留，同一行为不再因阶段或验证方法拆成多个场景 |
| S5 受管采用 | 原安装/tools owner；canonical 正文与消费者已更新 | 同步 dogfood 与声明平台投影并校验漂移 | 受影响文件、引用和 sidecar 状态一致，用户与 Task/session 内容保持 |

## 5. 行为要求

**R1（S1–S4）责任层可组合：** Issue 根据有效需求、实际消费者和自身承诺判断可观察结果覆盖哪些必要责任层。组件/服务、调用方/界面、跨组件业务结果和发布/环境结果可以组合，不能按标题词或组件类型强制唯一分类。组件责任不自动包含调用方接入、整站联调或整体部署；调用方责任不能用替身成功冒充被调用组件或完整链路通过。

**R2（S1–S4）必要承诺不得误删：** 有效需求明确纳入组合行为或目标环境结果时，保留相应最小证据，不能以“组件独立”或“最小验证”删除承诺。只有目标环境能判断或需求明确要求时，才要求环境证据；必要时写明原因、环境和未验证边界。

**R3（S1–S4）验证、部署与业务发布分离：** 验收定义行为或结果，验证证据证明结果，服务版本部署及目标环境运行验证属于相应部署/环境/发布职责。普通 Issue 不默认逐 Issue 部署共享 test 环境。业务对象中的“发布模板”“发布配置”“同步配置”等动作不能仅因词语推导出部署义务。

**R4（S2–S4）验收场景按独立风险收敛：** 每个场景对应一个独立可观察结果或风险。一个场景可包含判断该结果所需的多个条件、输入和例外，但同一次行为观察不得因创建、复审、验证方法或阶段不同拆成多个重复场景。工程检查或一致性验证不自动成为新的行为场景；其他入口/阶段只有必要差异时才增加场景。

**R5（S3）原 owner 落实：** Clarify、Readiness 和 Create Issue 消费同一共享规则并在原门禁检查完整标题、正文和验收。普通缺口由原 writer 修订正文，评论不替代正文。Readiness 可将普通内容缺口返回原 Clarify，Create Issue 可在创建前返回 `refresh_review`；不得增加平行 writer 或审批阶段。

**R6（S5）单一来源与分发：** Issue 自身结果/证据/责任场景规则由 `issue-content.md` 单写；跨阶段验证责任、证据去重与复用继续由 `quality-guidelines.md#test-and-validation-value` 单写。原 owner 只补必要引用或执行检查，不复制第二套正文。受影响 RDT/current、canonical、dogfood、平台和安装副本沿原 owner 同步。

**R7（S1–S5）验证方式：** 真实 Agent 行为观察复用现有 Issue 内容示例、Skill eval、native Agent 或 #826/#747 已支持入口。固定文本、引用存在、评论存在、分发成功或脚本通过不能替代行为判断；行为观察与安装采用分别报告。

## 6. 约束与依赖

开发基线为 `main@76198a53b4da989b66d2e5f135ff4d2b703ca3cf`，交付目标为 `castbox/guru-trellis:main`。当前 Task 依赖完整匹配的 Guru Team preset/runtime、现有 Issue content canonical 与 RDT authority。

公共 Skill id、typed exit、schema、DTO、Task/Delivery 生命周期和用户授权边界保持不变。没有数据库、服务运行或业务部署迁移。源码修改不等于现有安装已采用；受管副本由原 tools/install owner 处理。外部关联 Issue 只提供可复用方法或观察，不作为整项硬前置。

## 7. 可观察验收与验证方式

**AC1（R1–R4、R7；S1–S4）：** 使用一个去敏混合 Issue 草稿，正文包含组件结果、未要求的下游整站 E2E/共享 test 部署/逐 Issue 发布、一个有效需求明确要求的目标环境结果，以及“发布模板/配置”业务操作。通过原 Clarify 与原创建前审核的实际 Agent 入口处理完整正文，最终正文删除无依据完成条件、保留明确目标环境承诺、区分业务发布与服务部署，并只使用足够的独立场景。固定免责文字、关键词、引用或评论存在不能替代该观察。

**AC2（R5–R6；S3–S5）：** 受影响共享规范、原 owner 引用、教学示例/eval fixture、RDT/current、canonical/dogfood、声明平台与安装投影保持一致；定向 package、分发、reapply/drift、sidecar 和既有 eval 检查通过。该验收只证明内容、引用和分发一致；未执行的真实 Agent 行为、其他业务仓库采用或完整 Release 矩阵如实保留。

## 8. 实际未决项

当前没有阻塞的产品或范围选择。具体规则落点、fixture 装配、Architecture 影响判断和安装 owner 调用由后续 Delivery 规划按当前责任边界确定。
