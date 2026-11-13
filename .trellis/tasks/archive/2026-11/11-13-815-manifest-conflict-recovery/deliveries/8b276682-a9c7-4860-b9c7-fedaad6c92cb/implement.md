# #815 D1 实施与验证计划

## 1. 输入与引用

输入为整体 Task PRD 的 accepted_scope、D1 prd.md、design.md及第3节唯一来源设计处置。固定B=cb8b4ce349b54cd832ff5b8f72602c5a721ce875；D1无前序。真实candidate_assessment已返回no_architecture_impact；最终Wording/final_plan/Approval仍是实施前依赖。

实施前完整读取原Reconcile/tools/Publication SKILL及完整references、.trellis/spec/workflow/skill-package-contract.md、preset/installer.md、preset/upstream-ownership.md、workflow/quality-guidelines.md适用合同与当前before-dev指南。当前规划已读Test And Validation Value和Validation Scope Ownership；不得用测试数或正文相等代替行为验证。源码诊断不替代公开支持路径。

框架来源固定为trellis/presets/guru-team/source/trellis-source.json：castbox/Trellis@e3793251fad8bd261d0c370d408c7675b9f6a140，CLI/Core 0.7.0-castbox.6。匹配构建候选位于/Users/wumengye/Documents/GoProjects/Trellis-builds/guru-814-e3793251；实施先核其真实source/build/package身份，不凭目录或版本标签认定匹配。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置、owner和精确写集 | 行为与完成观察 |
| --- | --- | --- |
| I815-01 | 当前批准计划；Author/实施owner；trellis/skills/guru-team/packages/guru-reconcile-task-base/{SKILL.md,references/contract.md} | 在原实际冲突处理中补固定完整旧blob、临时工作文件和返回tools的入口/停止条件；原resolved/state/gate保持 |
| I815-02 | I01；原tools合同；trellis/skills/guru-team/packages/guru-upgrade-tools/{SKILL.md,references/contract.md} | 说明旧前像的适用性、原provenance/hash、逐路径决定、原installer最终生成、pending与原恢复；不改runtime或原I/O |
| I815-03 | I01/02；原Publication合同；trellis/skills/guru-team/packages/guru-publish-task-delivery/references/contract.md | 明确completed原事务通过retire_completed退役、公共facts保持、unknown先原恢复；不增加清理入口 |
| I815-04 | 上述正文；验证owner；三个package各tests/test_contract.py，加guru-upgrade-tools/tests/managed_manifest_conflict_flow.py | 受影响合同分发/入口检查加真实Git/CLI/installer组合driver；真实writer造fixture，不修补待测输出；既有resolved/Publication测试只补实际缺口 |
| I815-05 | 稳定公开正文；文档owner；trellis/presets/guru-team/README.md、trellis/workflows/guru-team/README.md | 只定位原owners和兼容采用，不复制步骤或新建workflow edge；完整workflow的现有顺序保持 |
| I815-06 | I01..05、实际工程事实；原RDT owner；docs/requirements-design-test-contributions/815-manifest-conflict-recovery/ 的manifest.yaml、requirement.md、design.md、test.md、traceability.md及proposed/docs/{requirements,design,test}/current/task-delivery-lifecycle.md | 准备受影响三层完整拟写，原owner在提交前整合真实current并readback；保持既有有效条件和历史字节 |
| I815-07 | canonical完整可用；原guru-upgrade-tools | 从完整本Task source对显式本Task checkout预览，逐路径判断，冻结一次plan并同步受管投影；实际owned preimage和sidecar由原owner处理，保Task/session/peer |
| I815-08 | 实际canonical clean H和独立Git提交边界；原tools owner | 开发local_candidate有formal_fork_source_lock限制；形成H后以新source_locked操作正式采用并验证target，不能改旧ref/plan或把开发结果改标正式。实际差额由原TaskCommit/完整committed Review覆盖 |

I07写集由原工具preview具体冻结，仅限本Task的.trellis/workflow.md、.trellis/guru-team受管runtime/packages/extension.json及受影响managed specs、.agents/skills、.claude/skills、.cursor/skills的声明投影和原指针/必要受管元信息。只写实际preview中的路径；不手工覆盖投影，不改peer或共享journal。root AGENTS/Git attributes仅在原installer确有其已定义受管block差额时由原owner精确显示；无差额保持。

不预授权新Git/GitHub副作用；正式TaskCommit、push/PR、merge、Closure、Finish按原owners各自展示精确动作。本次Planning只写Task规划和原必要会话状态。

## 3. 验证入口、输入与预期观察

- **V815-01（design V01/AC01）**：使用真实匹配Fork CLI/Core和本Task source运行新增source-private managed_manifest_conflict_flow.py，参数为--source <实际完整源> --fork <核实后的Fork> --output <Task-owned外部临时目录>。driver创建scratch Git repo/两个正常canonical分支，各用原installer生成manifest后merge，观察真实冲突和固定H/blob。scratch commits仅属于测试输入，不提交本Task候选。fixture写入范围和生成方法在执行前核定。
- **V815-02（design V02/AC02/05）**：当前执行Agent完整读修订后Reconcile/tools合同，在该fixture经普通git show临时前像和原tools公开preview/prepare/invoke接续。比较原blob/原provenance/hash；独立核组合canonical两侧内容已安装、最终manifest由原installer生成。运行目标自身resolver、原installed package validator、python3 .trellis/scripts/get_context.py --mode runtime-contract及--mode continuation，检查真实结果和范围；具体installed命令采用目标当前--help。
- **V815-03（design V03/AC03/04）**：复用guru-reconcile-task-base/tests/joint_resolved_flow.py的真实Git/公开wrapper结构，执行原execute-resolved-base-reconciliation及同请求恢复，观察正确父序/tree/零unmerged、同key/PR公开facts与自然dirty当前task.json。独立前后比较无关Task/session/peer和index/worktree内容。Publication复用test_transaction.py及test_current_transaction_migration.py的适用终态/unknown原操作检查；provider fixture不证明真实远端效果，不执行live push/PR。
- **V815-04（design V04/AC01/02）**：AI执行前像适用性与逐路径Gate，原命令只执行事实。当前对话记录真实入口、动作和结果；driver、schema或词法检查不能替代该判断。若仅自动driver跑过而AI未按正文接续，保留该项未验证。
- **V815-05（design V05/AC05）**：对实际改变的三个packages运行原source validator、适用合同/runtime测试；经原tools同步后跑installed validator和trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .。执行原owned-sidecar/mode/Claude-Codex-Cursor投影检查和必要一次self-reapply；可采用仍匹配结果，实际差额必须覆盖。不得因安装变量缺失把opt-in SKIP写成通过。
- **V815-06（AC06）**：必要RDT整合/readback后，由原TaskCommit形成本地候选；原constructor固定B和完整H，独立committed Review覆盖全部差额和组合。后续原Delivery/Completion/Closure/Finish核live main可达性和Issue状态，不能在本批提前声明。

候选本身不改变原tools/resolved/Publication runtime，故不重复不受影响的Fork广泛测试，也不触发完整多平台Throwaway/Release矩阵。先补真实组合缺口和受影响回归，再实际安装/投影；出现具体剩余问题才追加诊断。无权限中断、fault injection、锁或攻击负例。真实正常失败沿原事务核验和恢复，不人为改内部state/hash制造失败。

## 4. 停止条件与适用回退点

- 每次源码、测试或Task写入前运行check-task-checkout-boundary.sh。身份/C4/C5/注册checkout冲突停止，回原owner，不重建。
- 旧blob或原来源不可用、原pending未恢复、owned preimage变化、sidecar或public入口失败，停在原Reconcile/tools/Publication owner；保留原输入、plan、ref及原失败。未知mutation先恢复同操作，不重复prepare/create。
- 验证不能到达声明边界时如实报告缺口；基础设施反复失败先重评复现方法，不改业务断言或扩大成通用框架。
- 实际需要新增runtime机制、schema/owner或超出I01..08写集时回原Author/Architecture；需求边界变化回Clarify，不现场自修。
- 原tools rollback是独立有界写，核原前像与公共兼容后才执行；不reset本Task或清无关工作。仅文案和测试可在精确本批路径中修订，保留别人改动。
- V01..05充分支持当前接受范围后停止额外重复验证；未验证完整矩阵/其它native host/live远端fixture效果保持明确边界。

## 5. Delivery Policy（唯一）

policy=full，覆盖scope_ref的全部R815-01..06、AC815-01..06。没有延期子能力或待建D2。当前切片独立可交付条件是：原公开恢复合同完整、真实正常两分支组合/同身份/resolved/原事务验收充分、必要RDT已整合、受管实际同步与定向验证完成，以及完整committed独立Review和原readiness。历史#792成功不作为本批pass。

Delivery合并不等于Task完成。整体Completion保留live main可达、整个accepted scope、Issue关闭及必要Finish责任；这些后交付动作由其原owners按真实事实完成。开发local_candidate的source-lock限制只适用于该证据，I08真实正式采用成功后才解除，不转成全Task冻结。无实际解除结果时不得宣称formal采用完成。

## 6. Docs SSOT Plan（唯一）

strategy=delta_first。原RDT owner为guru-maintain-requirements-design-test-ssot；直接consumer是其final_integration、后续独立committed Review、Delivery Review与Completion。

原current unit locators为docs/{requirements,design,test}/current/task-delivery-lifecycle.md，保持RDT-REQ-LIFECYCLE、RDT-DES-LIFECYCLE、RDT-TST-LIFECYCLE及全部既有有效条件。本批在各原完整单元内补managed manifest冲突接续的行为、owner接口与验证责任，精确步骤仍由原canonical Skill合同单写；不建第二活动定义或Issue专属current页面。完整拟写由I06的task-owned contribution承载，实现工程充分后原owner固定真实target、整合完整组合并readback，所有actual after进入本地TaskCommit，之后一次独立committed Review；Planning不提前写shared current。

Architecture实际candidate结果为no_architecture_impact，不造空contribution/ADR、不更新全局CURRENT/version或root/index；最终final_plan如发现真实影响则回原Architecture/Author重订必要计划。README只更新实际新增采用说明。历史#792及已完成归档保持原字节；source、installed、AI行为和外部交付证据分别说明。
