# #547 Task-owned Architecture contribution

Identity：`architecture-contribution-547-retain-source-open-v1`；状态：`reviewed_candidate`。Requirement authority：本Task prd.md及castbox/guru-trellis#547；behavior authority：本Task design.md D547-01..05与#436设计贡献。Expected current：`docs/architecture/README.md` / `current-main-0.6.17-guru.87` / active；constitution：`docs/architecture/00-foundation/design-constitution.md` / `guru-trellis-design-constitution-v1` / current。Planning合同：`guru-maintain-architecture-baseline:planning:3.0`，project：`guru-trellis-architecture-change-contract-v1`。Path：`target_native`；decision refs ADR-013、ADR-024；ADR candidate为architecture-adr.md，required=true。

Before：Closure把exact_source资格等同本次必须close；纯保留OPEN被eligibility拒绝，Finish缺ref或要求CLOSED；多Issueaggregate closed被用作源source_closed。After目标：Closure选择并冻结retain_open，重读OPEN而不close；Finish消费原snapshot按动作重验OPEN/CLOSED；公共源结果由exact source动作产生。没有第二writer、state machine或source重写。

## 九 concern 的明确适用性

| Concern | Applicability / 依据与目标 |
| --- | --- |
| authority-binding | applicable：当前Task planning3.0、live .87、#547与design；不把installed旧摘要作为current |
| constitution-binding | applicable：语义完整、职责内聚、最小必要复杂度和债务单向收敛；一个现有枚举消费原owner即可覆盖目标，额外ledger/adapter无consumer |
| boundary-and-decision | applicable：ADR-013/024终态处置决定增量，target_native；来源身份与本次动作分离 |
| owner-and-single-writer | applicable：Completion审whole scope；Closure判断/执行；Finish归档；Cleanup删除；Author写规划，Architecture/RDT原owner写shared current |
| compatibility-and-exit | applicable：additive action需matching Closure/Finish consumer成套采用；旧完整安装固定原包，无新dual-read；原Upgrade owner处理真实legacy采用，最后旧consumer退出时原owner退休旧reader |
| gap-and-deviation | applicable：修复本次exact_source终态缺口，不新增GAP或重开既有ARCH-GAP-006/008；scope外历史债务不扩张 |
| parallel-scope | applicable：本Task独占闭环动作增量和隔离贡献；禁止#548、原CMS修改、并行shared-current写入和第二Task store |
| evidence-and-freshness | applicable：current design bytes、runtime/schema/normal recovery、受控matching安装投影；没有原业务/Release证明 |
| review-and-promotion | applicable：final_plan真实贡献/ADR审查；首个committed全diff独立Review后按expected live current晋升；新增promotion diff fresh Phase2/commit/full Review |

Current/target各owner不变；本Task仅删除exact_source必须close和Finish统一CLOSED的错误条件，不删除正常identity/freshness或旧合法动作。Required state漂移回Closure，scope不足回Completion原路径。

Project-check descriptor：`guru-trellis-architecture-convergence:repository:1` / `guru-trellis-architecture-convergence@1`；entrypoint：`docs/architecture/06-governance/change-contract.md`；rule refs ARCH-GOV-006..009，descriptor decision refs ADR-005/009、gap refs ARCH-GAP-006/008；本增量decision refs ADR-013/024。当前只形成方案；implementation/Phase2证据待执行，无shared promotion或Release声称。
