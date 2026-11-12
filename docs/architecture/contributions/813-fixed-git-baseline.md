# #813 固定审核来源创建：Architecture 候选贡献

Task `813-fixed-git-baseline`，generation 0，Delivery `f65560ac-65fa-48b8-aae3-98f8ceaf8678`。来源为 https://github.com/castbox/guru-trellis/issues/813 的完整正文；具体方案由本Delivery的design.md单写。本贡献及proposed目录均为隔离候选，不是shared current、实现通过或知识晋升。

## Authority、边界和完整拟写

阶段适用baseline为 `guru-trellis-architecture`，constitution为 `guru-trellis-design-constitution-v1`，change contract为 `guru-trellis-architecture-change-contract-v1`。固定before为 `5c6a4591db7165ece045e6b0eb789c21d06d7d38`。原独立candidate_assessment选择architecture_impact / target_native，引用ADR-RUNTIME-LOCATION、ADR-028、ARCH-RUNTIME-LOCATION。

唯一Architecture目标是 `docs/architecture/01-current/runtime-location.md` 的“明确Git对象与实际副作用”完整条款。完整拟写位于 `813-fixed-git-baseline/proposed/docs/architecture/01-current/runtime-location.md`。保留环境选择、位置、#760/#769、真实历史观察与原owner定义，不写共享root、index或另一份current。RDT runtime-location三层及canonical data-contracts的旧Creation断言由其原writer分别承接。

本次落实既有固定来源贯通直接consumer的决定，不改变constitution、owner或公共Task/Delivery模型，不因schema字段版本新增制造ADR。MIGRATION-813拥有本次新旧输入与完整旧provider恢复退出合同；若实现发现该边界实质改变，回原Architecture与Author，不在此候选追加例外。

## 机制、替代与代价

固定commit及source/acquisition关系由原Creation validator检查，Task基线branch与交付target分别保留原职责。来源variant是原当前输入的必要值，不是新业务authority。四个Creation入口复用同一归一化与对象关系检查；恢复不执行precreation uniqueness。synced来源的新建前置保留；固定对象不等待无关primary同步。

不采用创建前自动Sync、重试、异常文字替换、所有来源无条件取消检查、长期旧parser或来源恢复台账。这些选择分别保留原错误前置、隐藏失败或引入第二路径。当前方案只修改原owner与真实consumer，成本为一个闭合source值、共享事实校验、新版契约和定向验证，没有新增共享写入或协调等待。

## Required concerns

| Concern | 适用性与本候选承接 |
| --- | --- |
| authority-binding | applicable：按Planning3.0候选/最终目的分别核本before与baseline/change contract；不复用候选结果冒充最终结果 |
| constitution-binding | applicable：保持五原则及既有ADR的来源/身份边界；简化路径和合法调用代价由原独立owner判断 |
| boundary-and-decision | applicable：固定Git对象与实际同步分开，依赖原Creation/acquisition；源Issue和D1方案明确差额 |
| owner-and-single-writer | applicable：AI判断、确定性事实、官方Task、C4/C5/session、RDT/Architecture维护各保持原writer |
| compatibility-and-exit | applicable：target_native整体迁移current消费者，旧schema原样验证、旧成功操作固定完整provider恢复，无current fallback |
| gap-and-deviation | applicable：本Task的固定来源被local branch阻断缺口由AC1—AC5关闭；不新增全局GAP、principle exception或延期债务 |
| parallel-scope | applicable：允许本隔离贡献及本Task规划，禁止竞争shared current/peer工具/其它Task或#808内容 |
| evidence-and-freshness | applicable：候选source和最终design字节分别绑定；工程、整链、Agent、安装证据各自限定，不预填通过 |
| review-and-promotion | applicable：原final_integration读真实target、整合完整拟写及readback；精确提交后新独立Review核实际before/after，整合结果不代readiness |

## 验证、晋升与重评

原项目descriptor `guru-trellis-architecture-convergence:repository:1`、check `guru-trellis-architecture-convergence/1`、result contract `guru-project-architecture-check-result-2.0` 由独立Architecture按实际阶段执行。V1—V6见Delivery design/implement：完整public链、原结果恢复、字段mismatch、旧schema/同步来源、受管安装及实际Agent分别观察。

实现和必要工程结果具备后，原Architecture owner在TaskCommit前以真实target/expected-current整合本完整proposal并读回，RDT owner独立写其三层正文。随后TaskCommit纳入全部after，implementation固定B/H并begin_check，新独立Review先核Architecture再完成整段质量检查。Planning不提前promotion，不写自证最终HEAD/pass，也不要求后续commit追写本贡献的最终结果。

Planning 观察截止时尚未执行实现测试、安装或验收。后续本地工程、原 provider 安装/reapply 和实际 Agent 创建/恢复观察见 `docs/test/current/runtime-location.md` 的 #813 节；这些事实不替代 committed 独立 Review。完整拟写由原 owner 按提交前 final_integration 整合与读回，结果只为 integrated_pending_review。

若 scope、来源 variant、旧 consumer 恢复退出、owner 或真实依赖变化，原 owner 重评；无关 ref 前进不改变固定对象，共享写入仍须按真实 target 整合。
