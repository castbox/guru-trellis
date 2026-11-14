# Gen2 采用切片设计

## 1. 设计目标、需求承接与内容基线

承接[本批PRD](prd.md) A-R-01～05、五个场景及四项验收，完成当前Task checkout的真实source_locked采用。固定内容基线B为`3f7099b9db78700d03a29b2c825e84280f5b6821`，来自最近实际delivered PR844的reviewed head；该head为当前HEAD/Planning H0，merge是`d3b9196c5ca30c11e857fab5a912ab9aee6ac232`。三个更早Delivery的实际head均为它的祖先。PR目标为main；最终H由实际安装和原TaskCommit产生，不将main浮动ref作为B。

独立Architecture candidate_assessment已正式返回baseline_current/no_architecture_impact，freshness为`sha256:581e2010f444e179abdc895b6958f5e67930bd50a98cacec35d3329296849b33`。authority为H0的`docs/architecture/README.md`、`00-foundation/design-constitution.md`（guru-trellis-design-constitution-v1）和`06-governance/change-contract.md`。沿ARCH-DOM-010/ARCH-INT-015，无新贡献/ADR；完整方案仍需Wording、final_plan、Approval和Activation。

## 2. 当前系统、边界与目标差额

canonical来源已通过PR844交付普通Sync入口修复和真实回归。目标installed extension为.9，但来源仍ce250、Sync仍旧字节；版本字面不能证明采用。目标由原installer生成H0的完整managed投影和clean来源provenance，CLI保持0.7.0-castbox.6，lock保持源自己的精确Fork commit/tree。

唯一目标是当前原Identity/Ensure解析的gen2 Task checkout。独立完整干净H0 checkout只作为执行provider；源checkout、Fork/build及目标的实际本机路径只在本次调用和原owner私有输入，不写tracked映射。共享Git common-dir不扩大写集。

本批只改变installer实际生成的受管内容、manifest和本批规划。canonical机制、三个README和当前知识定义没有新增语义承诺；历史观察不更新成最新pass。若实际发现必要文档差额，先回原RDT/Architecture整合再进入完整提交/审核。

## 3. 来源设计处置（唯一）

| 来源与原承诺 | 处置、具体落点 | 理由、影响与上游处置 |
| --- | --- | --- |
| 根PRD§3.3/5.4及私有Complete Source Before Actual Adoption：完整来源delivered后原Completion/Creation与独立Planning | retain；第1/2/6节、I1和Policy | PR844与本批已实际建立；不把未交付提交或样本当正式源 |
| 原tools Version/Forward1：完整干净Guru commit、自己的Fork lock、实际CLI/Core byte identities及maintenance API1.0 | retain；第2/4/5节、I1/V1 | 不改Fork版本/源码，不从旧target dispatcher执行或使用local_candidate |
| 原tools Forward2/3及AI Gate：唯一checkout、unfinished operation、旧manifest/preimages、user edits/platform/shared paths审查 | retain；第4/6/7节、I2/V2/V4 | 普通dirty业务可保留，重叠旧事务归原owner；未知编辑明确决策 |
| 原tools Forward4：AGENTS custom真实source/content、renderer幂等；canonical Guru workflow/custom provider；一次prepare冻结原plan | retain；第5/6节、I2/V2 | 原public writer单写工具，installer维护Guru block；不新增wrapper或手修manifest |
| 原tools执行与证据：完整受管生成、checkout-local pointer、target resolver/installed/native、peer/common和业务保留、mode/sidecar | retain；第4/6/8节、I3/V3/V4 | 直接证明本目标AC04；源测试或临时安装不代替实际采用 |
| 原tools Same-operation recovery：同source/plan/ref恢复，rollback单独审查并先公共兼容校验 | retain；第7节、I2及停止点 | 不另prepare、不扩备份/写集、不reset Git或转换历史 |
| MIGRATION794§1/4/5与私有Whole Preparation Completion：全部after走本批完整质量/Refs-only交付，之后整体Completion/终态 | retain；第6/8节、I4～I6及Policy/Docs Plan | 不借来源旧pass代替本批审查，不关闭#808；Stage2完整保留 |

没有change/reject或未完成上游处置。PRD与implement只引用本矩阵，不复写来源设计。

## 4. 模块、职责与设计取舍

| 原模块/owner | 输入→行为→输出与文件责任 |
| --- | --- |
| 来源取得/原tools semantic owner | 实际PR844/head及源lock→核完整干净来源、既有匹配Fork/build/公共API、目标和旧事务→真实preview/冻结计划和唯一正式出口 |
| 原CLI/Core maintenance | 实际upstream_source/tools_input→inspect/getMaintenanceContract/prepareToolsInstallation/applyMaintenance→原工具与workflow产物；不修改上游源码、全局包或node_modules |
| 原Guru installer/tools executor | 审过的old manifest/managed决策/平台/plan→仅目标受管资产生成与旧owned资产退休→实际manifest及checkout-local runtime pointer；完整写集以本次冻结plan为准 |
| 原工程implement/check agents | 完整批准规划和目标事实→执行/核目标安装、保留与源/installed/parity/drift→临时真实证据，不生成质量pass |
| 原RDT/Architecture | 真实after和Docs Plan→核现行完整目标的适用差额或no_change→必要整合/readback；独立质量仍归提交后reviewer |
| 原TaskCommit、Review与交付owners | 全部after→精确本地H→constructor/begin_check固定B..H→新独立完整Review/两槽→publication eligibility/readiness/Publication/expected-head Merge |

复用原tools直接更新目标，不建立备用执行路径、兼容reader、状态机、锁、retry或新资产账本。普通apply不承接本请求的历史保留/单checkout合同，手工复制也不能证明原事务及完整映射，因此不选择。

## 5. 接口与数据

公共接口/字段不变。实际调用为：
`install {source_ref=3f7099b9db78700d03a29b2c825e84280f5b6821,dependency_mode=source_locked,checkout=当前Task checkout}`
→源`preview.sh --upstream-source`→原private-prepare→`prepare.sh`实际receipt.result.plan→同源`invoke.sh --plan`。root仅为调用上下文，不替换checkout。

private-prepare使用原schema的upstream_source、selected_platforms、guru_decisions、tools_input。upstream_source从匹配公开SDK取得真实CLI/Core roots和byte identities/expected_candidate；不复制摘要算法。platform保持实际Claude/Codex/Cursor，Codex公共Skill在Shared .agents/skills，不恢复退休public .codex/skills/guru-*。

先核实际getMaintenanceContract声明tools_custom_instruction={path:AGENTS.md,action:custom}；AGENTS唯一决策带真实source snapshot/content，原renderer只维护Guru block，公共writer拥有最终mode/hash。workflow选择完整canonical内容、template guru-team、同一immutable Guru custom provider、ownership=custom；不标bundled native。原managed edits用真实preimage/hash决定replace/preserve，旧hash不足时从实际旧源取得。

成功只消费tools_upgraded的installed_version/recovery_ref/unverified；source_locked要求unverified为空。恢复继续原source/plan/ref。没有业务数据、API、Task/session schema转换或公共handoff扩张。

## 6. 状态、顺序、正常与失败流程

1. 完整规划→Wording→独立final_plan→Approval、展示→Activation后才安装。
2. 核PR844结果和干净H0/Fork/build，读目标现状、共享路径、未完事务；普通来源/能力缺失停原owner，不借用其他source。
3. 原preview，AI核完整write/delete/preserve集及AGENTS/workflow/platform/pointer；原prepare一次冻结，审实际plan和renderer幂等，展示后原invoke。
4. 原执行器安装，再核目标resolver/installed/native和preservation。partial/输出丢失读同ref续原事务；sidecar或native缺口不报tools_upgraded。
5. 完整目标after及真实工程事实交原RDT/Architecture；无语义差额走原no_change，有真实差额先整合/readback，不能用安装成功替知识或质量判断。
6. 原TaskCommit纳入全部本批after和规划，原constructor保B绑定实际H；新独立reviewer按authority-first做Architecture、完整九维/fullrange及check/full_review两槽。
7. 当前passed→publication Architecture→本批readiness/中文Refs-only载荷→Publication→expected-head Merge。原Completion再判全Task；Closure no_mutation/Finish/Cleanup和Stage2保持独立。

源安装步骤自身不改变Delivery公共phase；Task lifecycle只由原公开owners写入。真实scope、source或机制变化回最早受影响owner；phase和脚本成功均不代替AI门禁。

## 7. 恢复、兼容、迁移与集成

原tools install/resume/rollback及frozen-source支持域保持，当前不建立新恢复协议。partial或输出丢失不另prepare、不修改原checkpoint、plan/ref/preimages或切source；真实source/写集变化先回原semantic gate。rollback只按原兼容/owned freshness顺序恢复，不能reset Git、删分支或覆后续业务工作。

installer仅退休实际旧Guru-owned且无当前consumer的资产；保私有release发现副本、用户内容、上游trellis-*和peer。Task/archive/workspace/session/public/private control不转换，common runtime pointer保持原字节；目标checkout-local pointer可由原installer更新。普通Task历史guard不授权绕过或手改安装。

前序source真实delivered是本批输入；H0与本批最终canonical managed集合及lock可证等价时，实际安装provenance可继续指向H0，不追逐自身最终HEAD。若内容变化改变该等价性，回原owner重新判断正式采用与受影响质量门禁。源、制品、启用、采用、准备Completion和正式Release分别取证。

## 8. 验证设计

| 验证→验收 | 入口、输入与独立预期 |
| --- | --- |
| V1→A-AC01 | PR844/public Delivery fact、完整source Git clean/head、自己的lock及匹配Fork/build/API；六项输入唯一，source为真实已交付H，不以.9字面代替 |
| V2→A-AC01/03 | 原preview/单次prepare/invoke与public postvalidation；唯一目标tools_upgraded、.9/.6、clean provenance、unverified空；AGENTS/workflow/managed决策可核 |
| V3→A-AC02 | 实际目标自己的resolver、source/installed validators、native get_context continuation和当前Delivery读回；可达新Sync runtime，进入实际原owner，无Traceback或旧Task伪装 |
| V4→A-AC02/03 | 全部managed_source_projections/实际集合、安装mode、三平台、workflow/lock、ownership/drift、sidecar/bytecode及原preservation；无缺失/字节差异/未处理冲突，业务/user/peer/common不变 |
| V5→A-AC02 | H0已审21项Sync/read/Issue回归与当前来源/目标字节适用性；实际目标普通bare skipped入口观察修复可达。旧组合fixture失败仍保留，不称完整资格链通过 |
| V6→A-AC04 | 必要RDT/Architecture after、全部实际TaskCommit/B..H、独立完整Review、eligibility/readiness和原远端交付；不以任何单项替代其他层次 |

没有新增算法或接口，不为版本/文本/固定声明增加长期测试。原21项及临时完整分发结果只有在输入、依赖、toolchain、参数、check定义及期望仍适用时采用；实际目标V2～V4独立执行。V5真实target探针选择无Git写入的skipped分支，避免在真实目标上误触普通sync去同步别的checkout；普通sync完整行为由已核真实临时Git证据覆盖。必要失败定位后留实际缺口，不无限修测试设施。证据充分即停止；Stage2的fresh focused/existing/scanner/tag smoke不提前记pass。

## 9. Canonical 引用、本轮差额与实际未决项

命中的R794/R649、D794/D649、T794/T649、ARCH-DOM-010/ARCH-INT-015及原tools、质量合同见PRD§7；本方案已读取各必要章节与关联条件。当前只是既有实际采用，不改规范、指南、断言或Architecture decision，Docs Plan由原owners在真实after核对。没有新contribution/ADR候选，不造空文件。

没有待用户决定的范围或重大方案问题。能力、source/build或native若真实缺失，停原owner并按实际路由修复；不改用ordinary apply、手抄或local_candidate取得正式通过。当前设计不是安装或质量验收事实。
