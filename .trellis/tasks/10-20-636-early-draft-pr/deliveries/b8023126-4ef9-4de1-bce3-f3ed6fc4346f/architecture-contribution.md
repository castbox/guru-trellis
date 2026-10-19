# #636 早期 Draft 架构贡献候选

TaskId=`636-early-draft-pr`，generation=0，Delivery=`b8023126-4ef9-4de1-bce3-f3ed6fc4346f`。状态为未审核的Planning候选；change_path=`target_native`。本文件不是共享Architecture authority，也不记录授权或gate通过。

比较起点为 `b470580d4f79f61c66d72db97861fe1564b5e746:docs/architecture/`，阶段适用baseline `.103`、constitution v1、change contract/concerns v1。真实设计在同目录design.md D636-01..05，ADR候选为adr-early-draft-pr.md。原candidate_assessment已明确架构影响，但final_plan与Phase2评估尚未完成。

Before：TaskCommit所有当前入口都要求完整Check；Publication只在readiness后执行到Ready，远端反馈被延后。After：同一原owner具有早期有界提交与Draft反馈入口，原事务在push前确保Draft并恢复同PR状态；Draft后完整内容分析与HEAD验证并行。最终Check、正式full_review predecessor、readiness、PublicationFact/Merge和整体收尾保持。

| Concern | 适用性、责任及差额 |
| --- | --- |
| authority-binding | applicable；Planning3.0两个purpose、后续非Planning Delivery2.0和当前project contract，最终实际候选fresh绑定；本文件不产生pass。 |
| constitution-binding | applicable；v1职责内聚、语义完整、最小复杂度和单向收敛。新增profile只承担#636早期反馈/状态恢复，删除其职责会失去AC01..07；不用第二Skill/账本/双读。 |
| boundary-and-decision | applicable；保留原TaskCommit/Publication/Review，变更时机而非新业务权限；ADR-024/028/030和ARCH-DOM-042/043、ARCH-GOV-008/009，target_native。 |
| owner-and-single-writer | applicable；Author独占规划；TaskCommit提交，Publication远端事务，Check/full_review/readiness各自判断。RDT与Architecture各单写自身共享定义，不互相代写。 |
| compatibility-and-exit | applicable；MIGRATION-636成套matching切换，一次性旧candidate/receipt/事务恢复；不把旧终态当新pass、不保留runtime双读。旧安装固定版本不被半更新。 |
| gap-and-deviation | applicable；无计划新增GAP，不重新打开closed GAP；真实外部/安装验证缺口如实保留Test，不能变成已交付能力。 |
| parallel-scope | applicable；本Task worktree、包、隔离贡献可写；禁止编辑其他Task或在未重读expected-current时竞争共享CURRENT/GAP/owner。 |
| evidence-and-freshness | applicable；固定B/H内容、HEAD H与组合T/M分开；target前进不是自动stale。命令结果仅为执行事实，当前语义由原owner判断。 |
| review-and-promotion | applicable；final_plan独立读实际方案/贡献；Phase2独立评估完整拟晋升targets后原owner写入和判断适用性；最终Check/commit/独立完整Review覆盖实际差额。 |

项目检查沿 `guru-trellis-architecture-convergence:repository:1` / version1、change-contract入口和`guru-project-architecture-check-result-2.0`。当前只形成设计贡献；实际结果由原owner在本阶段语义检查后正式调用。源码、安装、真实Draft/状态往返、Agent审核、CI、Merge与Release矩阵均未在本候选中宣称通过。没有#637/#638或Backend队列/CI的新职责。
