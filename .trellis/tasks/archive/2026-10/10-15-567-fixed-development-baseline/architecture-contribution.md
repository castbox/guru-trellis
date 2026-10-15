# #567 固定内容对象 Architecture contribution

状态：task-owned Planning candidate，未晋升、未验证。Identity：architecture-contribution-567-fixed-development-baseline-v1。来源：live #567；TaskId 567-fixed-development-baseline/generation0。当前独立 candidate_assessment 为 Planning3.0 / architecture_impact / target_native；不代表 final_plan 或实现通过。

baseline：docs/architecture/README.md / current-main-0.6.17-guru.91 / active；constitution：docs/architecture/00-foundation/design-constitution.md / guru-trellis-design-constitution-v1/current；project change contract：docs/architecture/06-governance/change-contract.md / guru-trellis-architecture-change-contract-v1 / guru-trellis-architecture-change-concerns-v1。

## 决策与 owner

选择 target_native。沿用 ADR-012/013/024 的原 Task/Delivery/阶段 owners；替代 ARCH-DOM-014、ARCH-CUR-032 的默认 base continuity/祖先资格，收敛 ARCH-GOV-003/007/008 与 ADR-005 中整体 CURRENT 前进自动 stale 的含义。共享 CURRENT promotion 自身仍验证写入时 expected-current，不被扩为开发资格。

必要新决策由 [ADR-567-CANDIDATE](./architecture-adr.md) 单写。技术机制与来源处分在 Task design.md；长期 Requirement/Design/Test 在 `docs/requirements-design-test-contributions/567-fixed-development-baseline/`，实施阶段由原RDT writer协调。无新 coordinator、跨任务数据库、审批或 authority store。

## Required concerns

| Concern | 适用 | 本候选合同 |
| --- | --- | --- |
| authority-binding | applicable | Planning3.0 两 purpose 与非Planning2.0 原owners；明确适用 authority，不以整体CURRENT推进代替真实变化判断。 |
| constitution-binding | applicable | 五原则identity保持；最小必要复杂度与变化隔离要求直接修改原owner/consumer，删除无consumer的强制同步机制。 |
| boundary-and-decision | applicable | 分离开发基线、固定Delivery内容与PR target；实际阻塞才整合，依据必要新ADR替代旧默认。 |
| owner-and-single-writer | applicable | 原semantic owners与Task/Delivery公共模型保持；shared-current仅原promotion写入，scripts不判适用性。 |
| compatibility-and-exit | applicable | MIGRATION-567明确受控接口同步演进、旧guard退出、原producer正常恢复；工具/数据采用归#566，不新增长期双读。 |
| gap-and-deviation | applicable | 不借本任务重开/关闭无关GAP；原子能力必须保留，无实际consumer的新机制不入scope。 |
| parallel-scope | applicable | 先只写本Task规划/contribution、受影响canonical与受管投影；不改他人task、source业务仓、upstream/global安装。 |
| evidence-and-freshness | applicable | 固定candidate与阶段适用版本；真实scope/content/事务错配仍阻塞；分层记录实际结果，不把哈希或绿色命令当语义审查。 |
| review-and-promotion | applicable | 首次独立完整committed Review后才按当时expected-current晋升；promotion差额再Check/commit/独立完整Review。 |

## Before / after 与验证

before：默认多阶段pair guard追赶base；BranchReview要求base ancestry；DeliveryReview重新取origin/base并比较SHA；Finish有target SHA全等资格。原Task/Delivery/Check/Review/Reconcile恢复能力已存在。

after candidate：原owner固定本轮内容基线B和阶段内候选/适用authority；正常实施与提交推进实际head后，由原implementation/check转换形成新的完整B..H候选，不能冻结Planning head。无实际阻塞时零整合；D2使用真实前序delivery_result.reviewed_head确定完整差额。局部整合沿原stage rework→implementation begin_check→原Check/full_review record_gate→readiness/publication，同一public记录中尚未被替换的旧gate只作历史证据，不能作为新候选的applicable gate；实际owner用旧完整审查加真实解决差额判断新完整候选。Completion消费明确截点并只刷新缺少事实。实际expected-head、精确候选/事务、既有服务端阻塞、全部scope完成责任保留。

project descriptor：guru-trellis-architecture-convergence:repository:1 / guru-trellis-architecture-convergence@1；refs ARCH-GOV-006..009、ADR-005/012/013/024。本轮prewrite九concern已由独立Architecture owner审查，无候选架构阻塞；implementation、final_plan、Phase2、完整BranchReview、installed与外部效果均未验证。

后续每个项目检查由对应真实owner按实际对象完成；不把本候选评估当later pass。适用原则、偏移与before/after需在真实diff中复核。shared-current .91/RDT .97保持，未来晋升版本由原owner当时决定，不预写成功或改历史正文。
