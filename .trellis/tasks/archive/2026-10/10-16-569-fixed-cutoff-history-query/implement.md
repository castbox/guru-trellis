# #569 实施与验证计划

本文件定义执行计划，不证明实现或测试通过。需求见prd.md；来源承诺处置唯一见design.md。

## Delivery Policy

policy=full。一个业务Delivery覆盖R569-01..11及T569-01..07：原history owner准备、固定public结果、query1/query2归属、原consumer和成套迁移/验证。没有提前发布的partial/staged slice；业务Delivery后没有预留实现工作。整体Completion仍须核验全部需求、实际installed/consumer证据、Architecture/RDT晋升和真实交付；Closure/Finish/Cleanup各归原owner。

独立交付条件：7组accepted验证均有实际足够证据，canonical/matching安装一致，semantic Check和独立完整committed Review通过，任务隔离贡献完成调和/晋升且新差额通过fresh gates。缺实际公开链或cutoff consumer证据仍为缺口，不以schema绿色提前交付。remaining work owner为同一Task原执行/Completion owner。

## Docs SSOT Plan

strategy=delta_first。原guru-maintain-requirements-design-test-ssot是唯一RDT writer；在最终Phase2前执行task_delta_reconciliation，写唯一隔离目录docs/requirements-design-test-contributions/569-fixed-cutoff-history-query/，文件为manifest.yaml、requirements.md、design.md、test.md、traceability.md。R569/BEH569→D569/CON569→T569保留双向trace；实际结果与未验证边界只在test.md单写，规划文件不复制长期authority。

Architecture的task-owned contribution在当前Task目录；原Architecture owner评估真实before/after、九concern及必要ADR。首次独立完整committed Review后，原owners按当时Architecture .92/RDT .98的适用expected-current串行promotion；若live authority变化先判断实际差额，不覆写。promotion新文件再Phase2/TaskCommit/不同reviewer完整Review，之后才能Publication/Acceptance。无需bootstrap，不顺带修复无关历史projection。

## 执行批次

1. 激活前：完整三文档Wording、fresh final_plan Architecture、Approval；呈现完整方案并完成当前对话的激活边界。创建和方案接受各有独立的当前对话边界。
2. 实现前：按trellis-before-dev读取所有适用spec与上下游，保留基线现状；qualification只接纳#569正常范围。候选/机制有实质变化回原owner。
3. 原Merge runtime/history.py：固定remote B1、local完整性复用、owner-local temporary Git准备、固定扫描、query2后继事实与原归属/去重。manual_recovery.py只做真实需要的内部Git context参数适配。
4. public边界：新增result3.0 schema/example；同步interface/commands的实际选择和git_write声明；旧result1/2不作current输出fallback。原query1/query2输入不变。
5. Markdown consumer：原Merge Skill/contract、Completion限定history消费段、必要shared contract与README/MIGRATION-569，明确固定截点、结果丢失、同Task新增交付/所需证据变化与其它前进、真实写入；只有现有薄编排直接引用已退出current输出时同步其引用，不复制step-local规则，不改upstream hooks/global包。
6. 定向测试和实际matching installed公开链；处理ordinary fixture/environment缺项时保留首次失败与实际层次。不得通过改scope、制造事实/门禁或Task分支同步让测试绿。
7. 原RDT reconciliation与fresh独立Phase2 Architecture后，原Check全面审查；精确TaskCommit边界另行展示。首次独立完整BranchReview覆盖全部committed base→HEAD，不复用Check。
8. Architecture/RDT promotion及新差额fresh gates；原DeliveryReview/PR readiness后分别展示push/PR、expected-head merge边界。Delivery PR为Refs #569。
9. 原Completion核验全部accepted scope与实际交付，原Closure执行精确Issue completed关闭，原Finish完成归档/bookkeeping PR并验证live main可达；原Cleanup单独审查精确本Task资源。

## 预期修改面与退出

| 位置 | 必要职责 |
| --- | --- |
| trellis/skills/guru-team/packages/guru-merge-task-delivery/runtime/history.py | 原owner内准备、固定扫描及public后继归属 |
| 同包runtime/manual_recovery.py | 必要的immutable candidate Git context；原manual recovery入口语义不变 |
| 同包schemas/examples/interface.json/commands.json/SKILL.md/references | result3.0、query1/2语义、metadata影响和当前consumer合同 |
| guru-review-task-completion/SKILL.md及必要合同/示例 | 实际history需求时消费公开cutoff；不新增全面history前置 |
| 同包tests及必要Completion/公开链tests | T569-01..07实际行为回归，非固定文案自证 |
| trellis/presets/guru-team/MIGRATION-569.md与必要README/spec | matching迁移、旧隐式current输出退出及原owner边界 |
| 本Task三文档/官方JSONL/Architecture contribution、任务隔离RDT目录 | 规划、必要贡献与唯一实际结果 |
| 受管installed/shared/Claude/Codex/Cursor投影及manifest | 仅由完整matching apply生成，不手工半升级开发carrier |

不修改共享内核承接本项业务判断；不改服务端策略、业务仓、原#566资源、其它Issue、upstream/global/node_modules。新增实现保持owner-local，每个触及非生成代码文件≤3000行。直接演进现有责任，不增加无consumer adapter/第二路径/长期状态。

## 验证计划

- V569-01 原query1/unit与真实Git：多Delivery、schema1/2、bookkeeping、PR/parents/head、完整合法空；local stale/missing/shallow与fixed B1，已有完整历史不fetch。保留原Task/PR去重。
- V569-02 query2/public facts：正常公开操作产生记录，manual事实与trailers融合；截点后真实后继排除，本次应覆盖却不可验证具体失败；candidate校验使用实际Git context。
- V569-03 准备失败：本地fixture Git transport的正常不可达/权限拒绝、获取后仍不完整，以及真实provider身份不一致。断言具体失败，绝无discovered/空数组伪成功；不进行追赶或业务重规划。
- V569-04 影响隔离：保存caller和registered peer的HEAD、语义index/工作文件、Task/Delivery字节、共享refs及必要Gitmetadata，前后核对。枚举temporary Git writes及退出清理；不把临时fixture写入误称业务写入。
- V569-05 matching installed公共Merge→query→Completion：真实Git/公开Task模型/原wrappers，Merge的真实delivered DTO薄投影给原consumer；目标ref仍落后且缺对象，原query自行取得，原Completion实际读取公开result并作完整判断。前序fixture pass与实际AI判断分列。
- V569-06 fixed-cutoff和恢复：取得B1后外部source前进B2；query仍B1，公开result返回cutoff。实际consumer分别处理无关B2直接消费和明确同Task新Delivery补事实；无相邻stdout、结果丢失恢复均从原producer重入，不读private state，不重跑旧业务gate。保留同一真实fixture状态与actual stdout，不手写中间成功DTO。
- V569-07 分发：从完整canonical source与matching upstream组合建立受控source-repository dogfood/installed样本，原apply/reapply，installed validator、overlay drift及Claude/Codex/Cursor/shared bytes/modes检查。逐个处理.new/.bak，不强制覆盖用户定制。开发Task旧carrier若普通apply触发迁移前置，诚实报告并在matching完整样本证明产品投影，不因此迁移本Task。
- V569-08 工程检查：托管解释器运行原package tests与新增定向回归；必要pytest经现有managed runner+隔离测试依赖，不污染immutable runtime。source package validator、触及Python语法、官方task context validate和git diff --check。具体命令按当前wrapper/help组装，不把缺依赖/skip当pass。

验证证据按code/static、组件、installed公共链、实际AI consumer和外部live分层；T569全部required证据满足后才能宣称完整。本项可采用Issue允许的代表性installed链，不冒称原业务现场或完整Release矩阵。真实PR/push/merge/Issue状态及live main可达属于本Task交付收尾另行核验。

## 尚未验证边界

上述实现、matching安装、public consumer及交付均是计划，当前尚未执行。完整多平台Release矩阵、软件tag/Release、原业务仓迁移/生产效果不属于本项。测试或门禁出现真实缺口时回原owner，不降低accepted范围。
