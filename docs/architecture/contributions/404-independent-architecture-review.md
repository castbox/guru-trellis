# #404 task-owned Architecture contribution
状态：implementation candidate；非 shared CURRENT。TaskId：404-independent-architecture-review / generation 0。身份：404-independent-architecture-review:implementation-v2。
本文件是现有 Architecture owner 的 task-local change-contract consumer，不是独立评审结果、审计清单或通过声明。

## Authority binding 与变更对象
requirement authority：[Issue #404 r4](https://github.com/castbox/guru-trellis/issues/404)；候选设计：.trellis/tasks/10-10-404-independent-architecture-review/design.md；任务定位：.trellis/tasks/10-10-404-independent-architecture-review。
Guru contract：guru-maintain-architecture-baseline:2.0；baseline：docs/architecture/README.md / current-main-0.6.17-guru.77 / active；expected current：current-main-0.6.17-guru.77。
constitution：docs/architecture/00-foundation/design-constitution.md / guru-trellis-design-constitution-v1 / content / current；只消费其identity和实际适用正文，不复制原则。
project contract：docs/architecture/06-governance/change-contract.md / guru-trellis-architecture-change-contract-v1；concern set：guru-trellis-architecture-change-concerns-v1。
decision refs：ADR-005、ADR-009及本次draft ADR；rule refs：ARCH-GOV-006..009。既有descriptor的ARCH-GAP-006、ARCH-GAP-008只作继承证据，不改变其lifecycle；无新增domain/GAP或独立业务integration。
候选 change path：target_native，直接演进既有owner/入口，不保留主会话自评作为独立评估的旧执行路径。独立owner负责实际适用性判断。

## Required concern applicability
| Concern | Applicability | 候选依据 |
| --- | --- | --- |
| authority-binding | applicable | 上述Guru、baseline、constitution、change-contract及r4 live authority共同约束候选；task计划不自封CURRENT |
| constitution-binding | applicable | 当前职责隔离与最小必要复杂度约束应用于dispatch、输入与consumer；五identity不变、不复制正文/评分 |
| boundary-and-decision | applicable | 独立评估executor与协调器分开，旧task叙事预注入退出；下游matching-stageeligibility不重做同质评估 |
| owner-and-single-writer | applicable | semantic owner仍是Architecture Skill；fresh worker执行新评估，main只协调；各整体owner职责不吞并；shared current仍原promotion owner |
| compatibility-and-exit | applicable | 2.0 publicDTO/profiles/exits不变，受控consumer与eval同步直接演进；不新增adapter/dual-read/fallback；旧混合preset通过官方reapply更新，不持有长期旧方法 |
| gap-and-deviation | applicable | 计划消除当前自评/叙事/预填nativeproof缺口；未实现前不称closed。继承历史GAP/debt不顺带治理；不新增/恶化责任偏移 |
| parallel-scope | applicable | task-isolatedcandidate/package/test/docs增量允许；review前禁止sharedCURRENT/acceptedADR/GAP/constitution修改，禁止写并行task/业务仓/生产 |
| evidence-and-freshness | applicable | Planning审真实design与受影响实现；Phase2含tracked/untracked；BranchReviewexactcommittedrange；真实nativeTest证据后续产生，未执行不记pass |
| review-and-promotion | applicable | draft贡献与ADR先受独立review；committedreview后原ownerexpected-currentpromotion；current推进sync_required；promotiondiff回freshgates |

## Owner 与单写
current：Architecture Skill由当前执行AI从task/planning叙事形成新结论；workflow编排、各整体gate、deterministicruntime和promotion均有既有owner。
target：Architecture Skill的四个新评估stage由fresh隔离输入subagent执行semantic/check/result/wrapper；main不补pass。Delivery/Completion的publication/acceptance_finish由原Architecture owner消费仍适用独立结论，评eligibility并formal调用，变化则回新评估；main不relabelDTO。
single_writer：本task隔离checkout写candidate；sharedcurrent与acceptedADR只有既有Architecture promotion owner在review后写。
兼容例外：不需要长期运行兼容。维护/退出责任为现有package与preset owner；受控所有consumer迁移和apply/reapply投影验收完成即删除失去consumer的旧narrative staging/自评proof路径，不删除仍有真实wrapper单元consumer的post-owner证据。

## Before / candidate after / deviations
Before：canonicalArchitecture合同要求currentAI读scope后author；Planningnativeprompt预置无架构影响，stagingrequired_reads含prd/implement；Phase2native由已经读叙事的同一AI自己authorArchitecture。workflow原publication/acceptance阶段要求freshstage调用。
Candidate after：canonical Architecture contract 已定义四评估stage fresh reviewer-first、实际设计/diff/consumer取证先于解释；两下游stage保留matching public wrapper与current eligibility。Planning/qualification/Check/BranchReview消费区分问题、任务必要性和机制；Delivery/Completion/Finish消费真实matching-stage输出。Native adapter/fixture与受控consumer正在直接演进，实际行为通过与平台安装投影仍待唯一Test证据，不由方法文本推定。
closed：当前无已证实closed增量；待实施与实际行为证据。retained：与本task无因果关系的历史偏离和既有GAP状态。new：计划不引入新偏离，实际发现由stageowner报告，不写成保证。
design responsibility overview：taskdesign的候选职责/consumer/compatibility结构。detailed：Architecturestep-localcontract、受影响stagecaller和nativeeval薄transport；不制造另一份长期方法SSOT。

## Project-check 与证据
descriptor：guru-trellis-architecture-convergence:repository:1；check guru-trellis-architecture-convergence@1；entrypoint docs/architecture/06-governance/change-contract.md；result contract guru-project-architecture-check-result-2.0。
scope：stage invocation、authority binding、path exclusivity、required concern completeness、before/after regression、single-writer、parallel stale、contribution/ADR review、promotion freshness。refs使用currentdescriptor的ARCH-GOV-006..009、ADR-005/009、ARCH-GAP-006/008。
Planningcheck由独立Architecture owner实际执行该AI语义协议并在其既有result中记录descriptor-bound结论；本贡献不代authorpass。Phase2/BranchReview/promotion各绑定当前candidate或exactrange，不复用旧checkergreen。
test refs：唯一docs/requirements-design-test-contributions/404-independent-architecture-review/test.md；task implement.md只定义验证计划。runtime refs：当前canonicalArchitectureSkill、trellis/skills/guru-team/adapters/eval/native_adapter.py、owner_staging.py与architecture_authoring.py；external refs：无生产/业务变更，nativeprovider实际证据尚未完成，status unverified。planned文件或脚本green不充当已验证独立行为。
ADR候选：required=true，locator docs/architecture/contributions/404-independent-architecture-review-adr.md；原因是独立执行边界与下游assessment/eligibility区分改变Architecture运行合同。独立owner仍评该必要性。
committed review：status pending；independent false；committed_range null。Planning独立设计审查不冒充committedreview。
promotion：state required；promoted_identity为空。expectedcurrentadvance时回同一Architectureowner，不覆盖并行结果。本文件非CURRENT，软件发布/完整矩阵/业务部署未验证。
