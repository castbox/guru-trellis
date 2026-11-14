# D2：真实 dogfood 采用设计

## 1. 设计目标、需求承接与内容基线

本设计承接[本批PRD](prd.md) D2-R-01～05、SC-01～06及整体AC-01/03/04/05/06。D1已实际交付完整来源；本批交付当前Task checkout的真实source_locked采用、必要当前说明及自身完整质量链。Stage2和准备终态仍按根PRD分别承接。

固定内容基线B为`ce25043d33e487def1043b4a9fee6cb180844480`，来自公共D1 delivery_result的reviewed_head，亦为当前HEAD/Planning H0。D1 merge为`647df4de6c4443720b4bacb674dbe3909333bf4d`，PR目标名仍为main。H0不预定最终H；本批constructor恢复该真实前序delivered head作为B，不重复D1内容或追逐新main。

独立Architecture candidate_assessment已实际baseline_current/no_architecture_impact，freshness `sha256:91c1a41914d4f9f486316e94c0b8a01776366445e031f75f55dcb5cf4754006d`。适用authority为B中的`docs/architecture/README.md`、`00-foundation/design-constitution.md`（guru-trellis-design-constitution-v1）与`06-governance/change-contract.md`。结论承接既有ARCH-INT-015及ARCH-DOM-010，无新contribution/ADR；完整Wording后仍需独立final_plan，当前结果不代表批准。

## 2. 当前系统、边界与目标差额

当前canonical `.9`、CLI/Core `.6`、lock及原tools完整源已由D1交付。当前真实installed `.8`，其manifest/provenance是原观察，尚不能证明正式采用。目标由原installer生成`.9`安装manifest、完整managed assets和原公共tools/workflow结果，并保持CLI `.6`与源lock。

唯一安装目标是原Identity/Ensure解析的当前Task checkout。原D1已交付head的临时干净完整checkout只作为执行provider，路径由当次对话/原owner私有输入携带，不写tracked workspace映射。Fork从该来源自己的lock解析到既有匹配干净build；已实际核来源与Fork的Git clean/commit，执行前原owner再核。

本批修改installer实际生成的受管文件以及三个README的受影响当前版本/采用说明，不修改canonical机制、source lock、业务代码或历史记录。原tools保留Task/session/用户配置和peer工具；后置primary最终更新留Stage2。

## 3. 来源设计处置（唯一）

| 来源及承诺 | 处置与具体落点 | 理由、影响与上游处置 |
| --- | --- | --- |
| 私有发布合同Complete Source Before Actual Adoption：D1 delivered后原Completion/Creation建立D2，再独立规划与正式采用 | retain；第1/2/6节，implement步骤I1与Policy | 实际前序及Creation已成立；不改原出口，不以本地提交冒充delivered |
| 原tools Forward behavior：完整干净Guru/Fork源配对、明确checkout、preview/单次prepare/invoke | retain；第4～6节，I1/I2及V1/V2 | 直接复用唯一owner与生产入口；没有新安装wrapper、fallback或迁移路径 |
| 原tools AGENTS/workflow/public API、managed edits、原保存与恢复边界 | retain；第4/5/7节，I2与V2/V3 | 使用实际inspection/contract决定原输入，installer生成manifest；不手改产物或序列化授权 |
| 原tools真实target resolver/installed/native及complete preservation | retain；第6/8节，I3与V3/V4 | 真实目标的公开入口与完整集合读回证明AC04，D1临时样本不替代 |
| MIGRATION794：提交前必要整合→原TaskCommit→固定完整Review双槽→原readiness/Publication；旧操作原provider | retain；第6/7节，I5/I6与V6 | 本批安装和文档全部after经自身审核；无重复Check/新earlyDraft或历史pass转换 |
| public-docs与根R03：版本轴分开、同源immutable安装、保历史与真实层次 | retain；第4/8节，I4与Docs Plan | README采用源码目标/Release存在条件，避免前后发布状态自引用；无规范性来源被拒绝或静默改为建议 |
| 根R05与私有Whole Preparation Completion：D2交付后整体Completion，再Closure no_mutation/Finish/Cleanup | retain；第6节与Policy | 独立D2不预称Task完成或关闭#808；Stage2完整保留 |

本矩阵为本批唯一来源设计处置；PRD和implement只引用本节。没有变更/拒绝规范性承诺，无待上游选择。

## 4. 模块、职责与设计取舍

| 模块/owner | 输入、行为与输出 | 文件与边界 |
| --- | --- | --- |
| 来源取得与原tools semantic owner | 消费真实D1 result/commit，验证完整干净源、实际Fork build和目标；审查preview、冻结计划和真实副作用 | 执行选定源canonical `guru-upgrade-tools`，本机路径只在对话/私有输入；不从旧target dispatcher执行 |
| 原CLI/Core公共maintenance API | 实际inspect/getMaintenanceContract/prepareToolsInstallation/applyMaintenance，拥有public tools计划、hash与workflow | 原SDK及工具文件；不改上游源码、全局包、node_modules或package-manager声明 |
| 原Guru installer/tools | 按旧manifest和真实managed preimage处置replace/preserve，生成完整当前package/platform/spec/overlay/manifest及checkout-local runtime指针 | `.trellis/guru-team/**`、实际选择的平台受管目录和spec/配置、AGENTS Guru block；完整写集以实际冻结原计划列出的工具文件为限；不把未知用户编辑丢弃 |
| 原实施/docs writer | 在真实采用成功后修改三个README的当前版本、入口和采用边界 | root快速安装目标与版本选择；workflow/preset安装说明。保原anchors、历史`.8`事实和能力说明，不写Release已发生 |
| RDT/Architecture maintenance | 按真实after核命中完整现行单元；无差额走原no_change，有真实delta先合法整合/readback | 现有R649/R794、D649/D794、T794、ARCH-DOM-010/ARCH-INT-015；不造空贡献或root/index登记 |
| 原质量/交付owners | 全部after→工程→知识→TaskCommit→constructor/begin_check→独立完整Review→eligibility/readiness→Publication/Merge | 保完整B..H、真实两槽、Refs-only载荷及各原事务 |

直接复用原tools是最小机制；普通apply会触发历史Task guard且不提供本批保留合同，手工同步无法证明原事务及完整target，故不选择。没有新wrapper、并行状态机、retry/lock/compatibility开关或新测试框架。

## 5. 接口与数据

公共接口和字段不变。实际原链：`install {source_ref=真实D1已交付head,dependency_mode=source_locked,checkout=明确当前Task checkout}`→源`preview.sh`与实际upstream_source descriptor→`prepare.sh`的原private-prepare→其实际receipt.result.plan→同源`invoke.sh --plan`。`--root`仅为上下文，不替代checkout。

原tools AI从匹配public SDK取得实际CLI/Core身份和byte identities；descriptor绑定实际Guru/Fork roots及expected_candidate，不复制其digest实现。private-prepare只用原schema的upstream_source、selected_platforms、guru_decisions、tools_input，所有file decisions来自实际inspection。

AGENTS决策明确为custom，source为实际原snapshot（缺失则null），content为已审当前完整用户正文；原pure renderer只维护Guru block，原public writer拥有最终mode/hash。先确认public getMaintenanceContract声明`tools_custom_instruction={path:AGENTS.md,action:custom}`，不得把preserve/replace默改custom。workflow使用完整canonical Guru内容、template guru-team及真实immutable custom provider、ownership=custom；不标bundled native。实际已选Claude/Codex/Cursor集合完整承接，Codex公共Skill根为Shared `.agents/skills`，不恢复退休public `.codex/skills/guru-*`。

成功只消费真实`tools_upgraded`的installed_version/recovery_ref/unverified；本批source_locked要求unverified为空且目标验证完整。receipt不是Task质量通过。未完成返回原同operation recovery_ref，不能另prepare或改source。没有新持久化数据、业务API或Task schema转换。

## 6. 状态、顺序、正常与失败流程

1. 本批完整规划→Wording→独立final_plan→Approval与当前计划展示→原Activation。
2. 原tools核真实D1 result/源/lock/Fork、当前目标与unfinished transactions。仅合法完整源进入preview；未知普通managed编辑由AI明确preserve/replace，旧操作先回原owner。
3. 审查public tools/workflow、Guru写集、AGENTS、platform/pointer及保留范围。原prepare仅一次，AI审其实际冻结result.plan与AGENTS renderer-idempotence；展示精确写集后原invoke。
4. 原tools执行public maintenance和原installer，运行目标自身resolver、installed validation和native continuation，核preservation。冲突/sidecar或不可用native不报成功；原恢复继续相同source/plan/ref。
5. 真实采用后原writer维护当前说明/断言；原RDT/Architecture核实际完整after；有真实知识delta时整合并readback，无delta时走原no_change，再工程检查。未变D1来源suite按适用性采用，不因此免除本批实际目标验证。
6. 原TaskCommit纳入所有安装/文档/规划after；constructor保B完整范围并begin_check；新独立Review按authority-first完成Architecture、九维及fullReview双槽。真实修复再走原writer/后继提交及受影响审核。
7. 当前passed→publication eligibility→本批readiness和中文Refs-only载荷→Publication/expected-head Merge。D2 delivered后原Completion核全部准备业务；后续终态及Stage2各归原owner。

任一步stale/mismatch回该事实原owner；不重算hash维持旧pass、不把前序或临时样本变成本批成功。current phase只标事实，不代表语义门禁通过。

## 7. 恢复、兼容、迁移与集成

本批沿原tools支持的install/resume/rollback及固定source恢复合同，不新增恢复协议。源/计划/写集实质变化先原owner重审；partial/输出丢失核原recovery_ref及真实completed/pending，保后续业务工作。rollback为原owner单独审查的精确副作用，不能reset Git或转换历史数据。

原Task/session/Task schema和peer工具不迁移，源库历史归档继续原支持域。必要旧hash从实际旧源/receipt取得，不由successor捏造。原installer只清退真实旧Guru-owned且无当前consumer的资产，保unowned私有release发现副本、用户内容和上游trellis-*归属；新兼容候选先回原owner，不能为通过临时增加双路径。

D1来源实际已交付是本批输入；本批installed provenance指向实际安装的干净H2。原owner确认H2与最终完整受管集合及lock一致时，该来源继续有效；不追随自身新commit。准备交付、真实采用、整体Completion、终态归档和正式Release分层。本批失败保D1真实事实，尚未完成采用不能记为仅待外部证据。

## 8. 验证设计

| 验证 | 要求/AC与层次、入口 | 预期观察与限制 |
| --- | --- | --- |
| V1 | R01/AC01/04；live Git/GitHub/source与原preview | D1 delivered、源clean/实际head、源lock/Fork/build配对和唯一目标正确；版本相同不足以证明 |
| V2 | R02/AC04；原tools实际prepare/invoke/public维护与installer | 实际tools_upgraded，`.9`/`.6`/真实clean provenance、完整managed集合及选定平台/workflow/lock成立；没有local_candidate未验证项 |
| V3 | R03/AC04；目标自身resolver、installed validator及`get_context.py --mode continuation` | 实际当前Task/D2继续原owner，零Traceback/未处理冲突；不是源resolver、投影parity或fixture native证明 |
| V4 | R03/AC04；原preservation/public postvalidation、完整managed_source_projections/installed inventory、ownership/drift/mode/sidecar | Task/archive/workspace/session/user config及peer/common pointers保持，完整mapping/模式由原owners判定，无未处理sidecar；不全平台throwaway |
| V5 | R04/AC03；三README changed links/anchors、shell block语法、完整说明语义及diff-check；原RDT/Architecture真实结果 | 保版本轴与Release条件、同源安装、历史cutoff及现行定义一致；无文本自证新测试或动态发布状态字段 |
| V6 | R05/AC05/06；本批实际TaskCommit/独立Review/eligibility/readiness/Publication/Merge | 全部after被自身当前审核并实际交付。工程、静态、真实Agent与GitHub效果各按实际结果报告 |

V2/V3/V4直接对本目标执行，是本批AC04证据；D1源suite、临时来源全映射及CI仅在输入/工具/定义/期望仍适用时采用，不能替代真实目标。无新生产算法，不为安装状态或版本字面加长期测试。必要实际受影响回归和原owner检查仍执行；存在具体证据缺口才补实验，充分后停止。Stage2单独执行fresh candidate focused/existing/前驱upgrade/scanner/smoke，不在本批预记通过。

## 9. Canonical 引用、本轮差额与实际未决项

本批PRD第7节定位R/D/T lifecycle、Architecture与public-docs/quality authority；均已读必要现行条件。R794/D794/T794及ARCH-INT-015已定义这次既有采用，差额是实际执行和当前说明，不是新架构能力。原maintenance在实施after阶段亲自判断no_change或真实delta；candidate no-impact不替代实施/提交后判断。

没有待用户选择的需求/技术方案问题。依赖原SDK/源配对/native能力若实际缺失，在原owner保留具体失败，回最早受影响owner；不能换普通apply/手工同步或把未实施当evidence_pending。当前设计不是Activation、tools执行或验收通过。
