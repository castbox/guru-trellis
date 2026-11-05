# D1 行为测试与因果验证设计

## 1. 设计目标、需求承接与内容基线

承接整体 R1–R4/S1–S6 与 AC1–AC7，全量 D1。development baseline B=b78edbbdc32e77392bc3775366473971050ccb4b，来自用户指定 main 的 Intake 固定 Git source；Planning H0 同 B。PR 目标 main 与内容范围分别保持。Architecture candidate_assessment 实际返回 no_architecture_impact（baseline guru-trellis-architecture / constitution guru-trellis-design-constitution-v1）；无贡献/ADR义务；以该结果为方案准入，最终规划另经 Wording-current final_plan。

## 2. 当前系统、边界与目标差额

quality-guidelines 已有行为断言、测试层级与非强制 mutation 审查；root contract 仍用 reverse-prove counterfactual；Author 模板没有方法选择和停止条件；Phase2 仅引用整体质量规范。差额是统一正文并让原入口消费，不修改 runtime、公共 schema、Skill id 或出口。尚无前序 Delivery。

## 3. 来源设计处置（唯一）

| 来源/原承诺 | 处置 | 本批落点及理由/影响 |
| --- | --- | --- |
| #735 修改落点：quality Test And Validation Value 统一方法 | retain | 第4节 quality 单写；避免第二套标准 |
| #735 根因准入保留普通功能/诊断/缓解/修复/保护 | retain | root 原 contract 直接替换含糊实验形式，保持各原分类与接口 |
| #735 Author 共享正文及两个模板在现有章节引用 | retain | planning-body 引用方法；design §8、implement §3/§4 给执行提示 |
| #735 Phase2 派工与审核原 owner/出口 | retain | workflow §2.1、Check 和 Branch 方法只定位共同原则，不复制流程 |
| #735 真实语义与分发验证、不新增状态 | retain | 第8节 V1–V7；使用现有原生执行与安装维护 owner |

全部来源承诺保留，无 change/reject，无须上游范围处置。

## 4. 模块、职责与设计取舍

quality-guidelines 的 Test And Validation Value 是唯一测试方法正文：条件→动作→结果→独立断言；按风险、环境和成本选择顺序；分清长期回归与临时诊断；已有适用证据复用；追加实验必须解决影响修复或验收的具体未决问题；证据充分即停止。必要验收与受影响回归保持原合同，不以竞争解释为前提。

root candidate admission 读取共同方法，在原修复条款判断 first deviation、因果链、差额与反事实依据，明确依据可来自现有观察/分析/实验。准入判断当前依据、候选与计划；修后观察归完成 owner，避免循环前置。新增测试的触达疑问先查实际入口、分支、观察，仍缺才选有界对照或等效检出。

Author 的共享正文定位共同原则；两个模板在原验证章节引导行为映射和覆盖复用。Phase2 coordinator 与审核引用共同原则，限制无依据追加整套红绿和重复回退。选择直接修改现有 owner，避免新 Skill、封装、脚本判定或测试理由文件。设施失败不得冒充业务失败；反复设施故障触发复现方式重评，未解决验收如实保留。

canonical 修改由实施者完成；受管同步由 guru-upgrade-tools 完整源 local_candidate 完成，保护 Task/session，不手工覆盖 projections。

## 5. 接口与数据

沿用原 Author profile→共同方法加载→原 typed exit、root profile→当前资格分类→原 consumer。没有公共 API、字段、状态或数据迁移。测试 runner 仅组织事实输入并采集实际工具/输出；host expectations 不进入被测上下文，AI 逐例判断。

## 6. 状态、顺序、正常与失败流程

没有业务状态转换。顺序为：来源行为→风险和证据缺口→已有适用覆盖→必要新增观察→结论；仅真实缺口追加有界诊断。入口可测试先行或实现先行。已足够时结束该项；阶段/执行者更换不自动重跑。fixture/编译/依赖失败先判断是否触达目标；未触达则只记设施失败，不改变业务断言制造通过。预期错误/拒绝/取消测试成功仍是有效行为证据。

## 7. 恢复、兼容、迁移与集成

保留全部公共输入/出口，无兼容双读、回退协议或新恢复状态。源到 dogfood/installed 沿原 maintenance owner，.new/.bak 依原 owner 处理。工具更新不是历史 Task 迁移。语义评估执行故障按真实缺口改装配或等效观察，不能自动无限修设施；保持原失败和边界。

## 8. 验证设计

| ID/AC | 入口与事实输入 | 可观察断言和边界 |
| --- | --- | --- |
| V1/AC1 | 正常 Author：明确普通 API/工具行为，尚未实现 | 规划条件/动作/结果/断言及足够层级；自选顺序，无固定旧实现/回退义务 |
| V2/AC2 | root qualification：适用的原失败、因果分析及修后观察齐备 | 采用已有效事实，结束该项验证，不重复制造失败 |
| V3/AC3 | Author/root：新回归绿色但是否经过缺陷分支存疑 | 先核入口/分支/观察；充分则停止，不充分补有界旧实现对照或等效检出；不能仅故障日志判有效 |
| V4/AC4 | root：异步原因未确定，有竞争解释与候选诊断 | 有界实验回答当前具体问题；准入不先要未实施修复的绿结果 |
| V5/AC5 | 实现派工：fixture/依赖失败、未触达、预期异常未发生和有效预期错误测试 | 正确区分产品缺陷失败与设施/预期；不改业务断言，保留缺口，反复设施失败重评方式 |
| V6/AC6 | Phase2 派工提出固定红绿、阶段更换重跑；分别有/无实际缺口 | 无缺口收敛义务，有缺口保留必要诊断；原必要验收与受影响回归仍执行 |
| V7/AC7 | canonical package 定向检查、原维护 owner 更新 dogfood、installed 验证和 overlay drift | source/shared/Codex/Claude/Cursor 实际受管选择一致，无未处理 sidecar；不声称完整平台安装/Release矩阵 |

V1–V6 由真实 Agent 从正常完整 owner/派工入口接收事实并选择动作，host 提前固定期待但不注入答案；记录实际输入、工具、输出与逐例判断。普通功能至少观察两种合法顺序的事实条件，V3 覆盖触达充分和仍存缺口，V6 覆盖必要回归不受阻。定向 contract/runtime 与分发测试证明其客观层，不能代替语义。已有 root 传输 smoke 可复用，无必要对全部历史语义案例重跑。

## 9. Canonical 引用、本轮差额与实际未决项

quality/root/Author 与现有方法引用见第4节；RDT 既有 knowledge-maintenance、review-sufficiency、completion-closure 保留本身职责。本批通过原 RDT owner 准备完整验证方法叶单元贡献，candidate Check 后 final integration；不复制质量规范正文，不改全局导航/版本。Architecture 原独立结论决定是否需要贡献。对应 EVO-001/003/004/005/007 的保真、authority、单 owner、减少重复和分发；EVO-002/006 维持原架构与闭环，不新增能力。没有必要未决产品项。
