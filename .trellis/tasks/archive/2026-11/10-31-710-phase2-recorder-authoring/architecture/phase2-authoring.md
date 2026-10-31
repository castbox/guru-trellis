# #710 task-owned Architecture contribution

状态：proposed；TaskId=710-phase2-recorder-authoring，generation=0，Delivery=63d55014-9fec-48da-a106-2a7403305977。本文是实际规划贡献，供独立final_plan读取，不是shared current或已执行project-check。设计见../deliveries/63d55014-9fec-48da-a106-2a7403305977/design.md。

## 适用authority、边界与决定

before为Git 2fc49bda6552d1a8bf95dff243ab2de9a9ea8e30的docs/architecture/README.md、00-foundation/design-constitution.md和06-governance/change-contract.md；identity分别为guru-trellis-architecture、guru-trellis-design-constitution-v1及guru-trellis-architecture-change-contract-v1。Guru planning合同为guru-maintain-architecture-baseline:planning:3.0，concerns为guru-trellis-architecture-change-concerns-v1。

原Check AI拥有九维语义与出口；原record仅生成客观事实；check验证，invoke消费。唯一target_native路径退出record完整6.0输入，统一既有语义authoring；结果schema6及checker/invoke/maintenance既有完整消费保持。候选token与Phase2 token职责各自保留。详细兼容决定见adr-phase2-recorder-input.md；不是新增保护或digest authority。

命中ARCH-FND-002（AI/script）、ARCH-FND-004（公共兼容）、ARCH-INT-016（受管分发）、ARCH-DOM-053和ADR-KNOWLEDGE-FINAL-INTEGRATION（原最终整合）。完整宪法适用：复用已有官方扩展与record；输入/输出概念分清；原语义/确定性owner内聚；无新状态/DTO/wrapper；旧record输入无真实依赖时显式退出。没有原则例外、新owner或GAP生命周期变更，不声称关闭已有GAP。

## 九 concerns 的实际承接

| concern | applicability及本Task合同 |
| --- | --- |
| authority-binding | applicable；以上固定before、purpose和项目identity；最终对象必须绑定当前D1 design，candidate不能替final_plan |
| constitution-binding | applicable；完整current constitution及上述实际机制判断，独立owner重判，不制原则评分 |
| boundary-and-decision | applicable；需求#710及整体PRD；原Check输入职责目标；唯一target_native，compatibility退出由本ADR承担 |
| owner-and-single-writer | applicable；Check语义/record/check/invoke原分工；RDT和Architecture各自单写shared current，host不代产语义前置 |
| compatibility-and-exit | applicable；MIGRATION-710显式退出完整record输入，迁移本仓tests/模板；既有结果消费/恢复保持，不留dual reader。不能同步迁的真实consumer出现时先回方案owner |
| gap-and-deviation | applicable；不新增或关闭GAP，不扩大旧authority/dual write；consumer或mandatory native缺口保留未验证，不用pass掩盖 |
| parallel-scope | applicable；只写本Task规划/贡献及accepted canonical差额；禁止改其它Task/业务#994或抢写shared current；无新锁/并发协议 |
| evidence-and-freshness | applicable；design V710-01至09分别验证合同、命令、native、安装；真实完整candidate和未改消费者各stage亲审；当前只有规划，无实现/安装成功事实 |
| review-and-promotion | applicable；当前贡献与ADR供Wording后独立final_plan；实施补完整isolated proposed→独立Architecture/候选Check→原晋升/readback→actual after重绑→最终Check/committed Review |

## 真实改动与拟晋升内容

原Check package独占Recorder Authoring、例子、runtime局部差额和输出合同；原eval adapter扩展同fixture候选/最终运输，必需语义owners实际执行。受管安装由原tools/preset同步，Task/session保留。完整consumer清单和迁移安排由D1 design第7节拥有；本文不复制第二清单。

实施期完整拟写位于本目录的 `proposed/`，包含下列真实目标。两份现有单元保留固定 B 的全部有效条件及历史，增补本次输入职责与匹配分发；新增 ADR 承接兼容退出理由。没有全局 README/version 或 EVIDENCE 写入，不将决定生效或 CLI 可用升级为首次 native 成功。

| shared target | 完整 isolated proposed |
| --- | --- |
| docs/architecture/03-domains/ownership.md | proposed/docs/architecture/03-domains/ownership.md |
| docs/architecture/04-integrations/distribution.md | proposed/docs/architecture/04-integrations/distribution.md |
| docs/architecture/adr/phase2-recorder-input.md | proposed/docs/architecture/adr/phase2-recorder-input.md |

原RDT owner独立承接能力行为、设计与测试知识，package仍单写精确字段。完整proposed目标尚属实施期产物，本Planning材料不是空目录或提前晋升；final_plan判断本设计和真实ADR是否足够进入实施，phase2再审完整implementation与实际拟写。

## 检查、退出和恢复

project descriptor为guru-trellis-architecture-convergence:repository:1，check id/version为guru-trellis-architecture-convergence/1，result contract为guru-project-architecture-check-result-2.0。当前独立Architecture owner执行planning project-check；本贡献不生成自己的pass。缺适用事实用contract_incomplete，真实冲突用architecture_conflict，责任/GAP回归用fitness_regression，适用对象stale用sync_required。

迁移退出验收：所有正常record caller只author语义；完整结果仍由原checker/invoke恢复；业务变化拒旧结果、metadata排除不变；两个native阶段首次输入/命令及finding满足真实证据；matching安装无未处置sidecar。条件未满足不能声称已采用或交付。无DB迁移/部署或历史Task转换；旧完整安装固定旧合同，采用新版本走原完整工具owner，不单patch record。
