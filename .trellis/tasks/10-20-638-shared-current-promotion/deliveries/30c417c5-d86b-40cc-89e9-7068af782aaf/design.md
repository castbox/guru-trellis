# D1：稳定知识身份与最终整合晋升设计

## 1. 设计目标、需求承接与内容基线

本批完整承接 [PRD](prd.md) 的 R638-01..07、S638-01..08、AC638-01..07，没有前序 Delivery。固定内容基线 B=`9cec623833b61814f1175f31acde4fa81334cdb0`，来源是本 D1 明确选定的 development baseline；原 `DeliveryProjection.content_base` 已返回同一 B。Planning H0=B，只是当前观察，不是最终实现 HEAD。内容审查固定 B..H；PR target 为 `castbox/guru-trellis:main`。目标分支前进不自动替换 B 或要求同步提交。

阶段适用 authority 是 B 中的 Architecture `.105`、RDT `.114`、`guru-trellis-design-constitution-v1`、`guru-trellis-architecture-change-contract-v1`。首次独立 Architecture candidate_assessment 实际返回 `baseline_current / architecture_impact / target_native`，decision_refs 为 ADR-028/030/034；它允许写方案，不证明 final_plan、实现或安装已通过。项目九 concerns、descriptor `guru-trellis-architecture-convergence:repository:1` 和 result2.0 保持。

设计将首次候选检查和真实 shared-current 写入分开。前者在 Task 隔离贡献及完整 proposed 正文上完成；后者在同 Delivery 最终整合边界完成。最终 public Check、commit、完整 committed Review 仍覆盖实际写入，Ready/Merge 不接受未晋升贡献。

## 2. 当前系统、边界与目标差额

现有 Architecture `runtime/promotion.py` 验证完整候选、拟写目标、实际写入和恢复，强制不同 successor identity 且总入口必须是 target。现有非 Planning4.0/Delivery2.0 promotion 固定 phase2。Check、Branch Review、Delivery readiness、RDT current-knowledge 以及项目 change-contract 都消费提前晋升后的候选。集中 Architecture/RDT README 同时维护全局编号和历史摘要。

目标保留原 AI owners 与确定性边界，删除普通晋升对全局入口写入和全局编号递增的强制依赖。保留真实 API/schema 版本；Knowledge identity 与精确内容快照分离。增加原 Check 的候选检查入口，完成首次完整质量检查后再进入最终整合；不新增公共 Task 状态、顶层 phase、Skill 或调度器。

本批只迁移知识维护、受影响生命周期条款及必要 Architecture 职责正文。未命中能力不批量改写；历史 ADR、版本页、归档与 Git 对象不回填。#636 早期 Draft、#637 唯一适用性机制、Task/Delivery 身份、Completion/Closure/Finish/Cleanup 不改归属。

## 3. 来源设计处置（唯一）

| 来源 / 原承诺 | 处置与具体落点 | 理由、影响与上游处置 |
| --- | --- | --- |
| #638「目标与行为」1：唯一完整单元、稳定身份、薄导航 | retain；§4 D638-01、§5 身份合同 | current 正文保留完整条件，读者不拼贡献历史；由本次原 maintenance owners 承接 |
| 同章2：取消普通任务全局递增竞争，Git 精确定位且保留真实合同版本 | retain；D638-01/04 | 根入口稳定身份、单元 Git revision；公共 API 另行版本化，不批量改历史 |
| 同章3：隔离贡献和完整拟晋升正文可先审 | retain；D638-02、§6 steps1..3 | Check 候选入口不写最终 public Check gate，不冒称 shared current 已更新 |
| 同章4及「最终合入准备」：真实目标合成、同 PR 写入、实际差额和全部消费者审核 | retain；D638-03、§6 steps4..7 | 原 owners 真正晋升；原质量链检查最终内容，行为/接口/验证义务改变回最早质量 owner |
| 同章5及最终准备第二段：无关推进不使所有设计失效，无故不 merge/rebase，不追 SHA | retain；D638-03/05、§7 | 一次读取固定 integration target，只解决命中单元真实差额；保留 #637 规则 |
| 同章6：Architecture/RDT/Check/Review/Publication 与 I/O 一起迁移，无第二 current | retain；D638-02/04、§5/7 | 受控消费者直接演进；匹配安装切换，不加双读 parser 或从旧 pass 转换 |
| 同章7、验收及边界：代表性迁移、no-change、#636/#637 installed 组合 | retain；D638-05、§8 | 无空贡献/ADR，安装和真实 Agent 分层验证；完整矩阵及业务仓实现仍排除 |
| current-knowledge「Revising and promoting」及 ADR-030 / D331-04 / project change-contract：Phase2 独立审拟写后，先实际晋升才 Check | change；D638-02/03、§6；ADR 候选 `ADR-KNOWLEDGE-FINAL-INTEGRATION` | #638 明确要求的新时机窄替代。保留原独立评估、写前真实目标、写后适用性和最终质量义务；必要决定由原 Architecture 评估和晋升，不以本表宣称共享 authority 已改 |
| 原 promotion validator：distinct successor、总入口必写、README 整体内容 token | change；D638-01/04、§5 | 单元无关变化不应争用该入口；只保留实际目标的客观一致性，公共版本迁移见§7 |
| ADR-028、ADR-034及 workflow-contract「Candidate Applicability And Coverage」 | retain；D638-03/05、§6/8 | 固定适用来源、首次完整独立审核、原覆盖加全部差额/消费者；不创建另一复用机制 |
| #331 完整定义、稳定关系、历史可解析及两层 generic/project 来源 | retain；D638-01/05、§7/8 | 只改本次命中时机/身份条款；不降低来源完整性，不将历史案例当当前 authority |

## 4. 模块、职责与设计取舍

### D638-01 完整正文与稳定身份

Architecture 根入口在本次真实切换中使用稳定 identity `guru-trellis-architecture`；三层 RDT 使用稳定 authority identity `guru-trellis-rdt`。它们声明状态和定位关系，不是每次正文变化的全局序号。保留现有单元 ID，包括 RDT-REQ/DES/TST-KNOWLEDGE 与 ARCH-CUR/DOM/INT/GOV 各 ID。单元精确来源使用完整 Git commit + repository-relative locator；写前未提交候选通过完整 proposed-target locator 和现有局部内容一致性 token 绑定。

根入口只在定位关系、身份或状态真的改变时写入。取消追加每个 Issue 的业务摘要与全局 predecessor 计数；现有历史内容先保留为 Git 历史，明确本次 .105/.114 的固定 predecessor 定位，不重解释旧引用。真实 public Skill/schema/API 版本继续独立维护。新增 ADR 使用语义 identity `ADR-KNOWLEDGE-FINAL-INTEGRATION`，文件 `docs/architecture/adr/knowledge-final-integration.md`，不争用下一个全局数字。

### D638-02 首次完整候选检查由原 Check owner 拥有

新增原 `guru-check-task` 的 `delivery_candidate_check` profile，保持九个语义维度、资格检查、完整 dirty/候选路径与未改消费者覆盖。其正向出口 `candidate_checked` 只证明当前完整候选及完整拟写正文被检查；不调用公共 `record_gate(check)`，不形成 TaskCommit 可消费的 `passed` 或 check_result_id。原 owner-private checkpoint 在该输出被消费后退休。

首次候选检查前，原 implementation owner 在公共 `implementing` 阶段以固定B、实际HEAD和完整B..HEAD加dirty paths调用原 `candidate`/`begin_check`，使公共phase为`checking`，candidate.content_ref绑定当前bytes/modes。原Check先校验该candidate并完成候选判断。选定`candidate_checked`时，仍由当前Check owner使用原公开`rework`将target_role设为`implementation`、affected_results设为`[readiness]`，reason绑定本设计的最终整合职责，再发出出口。该转换不写Check gate，保留planning与既有真实Check/full_review历史，不赋予它们当前适用性。

最终整合在`implementing`进行。原maintenance owners写入后，原implementation owner以同B、实际HEAD及包含全部晋升/关系/导航差额的paths重新构造candidate并`begin_check`，公共phase再次成为`checking`。原最终Check只能验证这个新content_ref，不能继续验证写前旧candidate。即使无知识写入，也通过同一合法回程重新绑定实际候选，不制造提交或空文件。此处只消费现有公共API，不新增操作或Task状态。

Architecture phase2 可返回真实 `reviewed_candidate`，不再为了使 Check 能开始而先晋升。RDT task_impact_sync 在有知识变化时完成隔离贡献和完整 proposed 正文，返回新的 `candidate_ready`，不把候选投影为已更新 shared authority；无变化仍返回实际 `ssot_current`。候选 Check 读 contribution 中公开的完整 proposed locators及固定来源，实际 shared current 仍保持写前状态。不能以尚未存在的最终正文通过消费者作为候选检查前置；消费者的真实运行义务在候选适用检查和最终写入检查分别验证。

### D638-03 同 Delivery 最终整合由原两个维护方写入

`candidate_checked` 的唯一 workflow consumer 进入最终整合，仍使用原 Architecture/RDT promotion。它不是新的 Git 同步 gate。原 owner 一次固定真实目标 branch/commit，逐个读取命中单元及必须更新的关系/导航；不遍历全仓建 hash inventory。若 remote commit 本地尚不可读，只通过已有 Git/gh 读取能力取得该精确对象，不移动 Task branch。

不同单元前进不修改本 Task 的未命中路径。相同单元变化由原 owner 比较适用来源、本方完整拟写内容和真实目标，保留双方仍有效条件，形成唯一完整组合正文。组合稿改变已审内容时，原独立 reviewer 按 #637 补审全部实际差额和受影响未改消费者，再写入。推翻需求前提回 scope/Planning；实现、接口或验证义务变化回对应原质量 owner，不把“文档”视作豁免。

原 owner 亲自写目标并读回全部内容。脚本只校验本次目标的 source bytes、branch-before bytes、实际 after bytes、完整候选和局部一致性。共享目标 revision、target bytes、恢复 intent 留在同 owner 当前调用或确有恢复 consumer 的短期私有状态，不进入 public handoff。一次操作固定目标；后续只处理实际阻塞，不以 ref 又前进为由重复追赶。

### D638-04 公共合同和确定性迁移

修改范围是 Architecture/RDT/Check 的实际 runtime、Interface、schema、examples、唯一 consumer projection，以及 workflow 和原 Review/Delivery/Publication 消费说明。原 Branch Review 继续完整 committed range；Ready/Publication/Acceptance 只接受 no_change 或真实 reviewed_promoted。取消全局 successor 强制写入，不取消目标内容 mismatch 或额外实现变化检测。

Arch 非 Planning 当前合同切到5.0/Delivery3.0；Planning3.0/Delivery1.0、bootstrap/repair 原语义保持。原 promotion profile 新 stage=`final_integration`，同 Task/Delivery 和 before_authority 仍绑定。旧4.0/Delivery2.0只作固定旧安装/历史验证，不在新 runtime 双读。RDT impact/promotion 使用显式2.0入口以表达候选阶段与实际最终整合；bootstrap/repair保持原合同。Check 当前 owner-private schema演进6.0，增加候选 profile/出口，现有最终 Check profiles/成功出口不改义。

不选新 Skill、通用证据账本、全仓 hash 清单、第二 current、队列或锁。也不把旧 Check 的 `passed` 改名当候选，避免已写 public gate 后无因返工。新增候选入口承担当前必需且独立可验证的“已审但未晋升”职责。

### D638-05 文档与分发职责

Author 写本批三正文及本 Task Architecture contribution/必要 ADR 候选。实施 worker 只在批准范围写 canonical、Task 隔离 RDT contribution 和完整 proposed targets；原维护方最终晋升。完整定义仍由 current-knowledge 与原 package 合同单写，workflow只编排。canonical变化通过原 preset/package分发同步 dogfood；官方 Trellis hooks、runtime agents、上游包和 node_modules 不改。

## 5. 接口与数据

| 原 owner / 入口 | 当前输入和最小输出 | 直接 consumer 与客观限制 |
| --- | --- | --- |
| Author requirements → Architecture Planning | 保留 actual candidate/key/root，Planning3.0 | candidate_assessment→同 Author；final_plan→Approval，两个实际判断不互换 |
| RDT task_impact_sync2.0 | 原 Task/authority/contribution context + `stage=phase2`；有变化输出 `candidate_ready={contribution_locator,authority_locator,authority_version}`，无变化用 ssot_current | 原 workflow RDT router 将已审拟写 locator交候选 Check；version指固定适用 authority，不能冒称候选已current |
| Check delivery_candidate_check1.0 | 与初次 Check相同的TaskRef/key/公共Planning result identity；输出 `candidate_checked={task_ref,delivery_key,candidate}` | 唯一 final-integration router；candidate使用现有 `{head,content_identity}`，只作紧邻内容一致性，不是跨阶段审计链 |
| Architecture delivery_promotion3.0 / repository promotion5.0 | `stage=final_integration`，原 task/key/root、baseline/constitution/project contract、before_authority、candidate、contribution sync target；stable baseline允许同 identity | 原 current router→本次实际写入适用性→最终 phase2 assessment/Check；删除 successor_baseline 和总README content token的普通晋升强制字段；bootstrap distinct successor仍有效 |
| RDT promotion2.0 | 原 contribution、实际 authority和 `stage=final_integration` | 真实写入后才 ssot_current；不需要全局版本递增，完整源以Git定位 |
| 最终 Check→TaskCommit→Review→Delivery | 保留 final passed/check_result_id、原固定B/H和当前完整结果 | 初次 candidate_checked不能投影到TaskCommit、full_review或readiness；最终实际写入须由这些原 owners覆盖 |

公共状态转换固定为：implementation `begin_check`（implementing→checking）→原Check候选判断及 `rework(target_role=implementation, affected_results=[readiness])`（checking→implementing）→原owners最终写入→implementation重新`candidate(...,base_ref=B,head_ref=actualHEAD)`/`begin_check`（implementing→checking）→原Check最终`record_gate`（checking→reviewing）。操作的owner_id从原workflow declaration读取，不能由caller指定任意role或直接修改Task文件。旧candidate content_ref在写入后不再适用，必须通过上述原owner回程更新；普通freshness校验不放宽。

Arch5.0/Delivery3.0保留原 stable exit IDs 和最小输出职责。`baseline_current` 的 baseline_identity是稳定 authority identity，精确实际候选通过原candidate字段交唯一consumer；不将完整目标hash/正文/历史塞入DTO。successor baseline全局字段退出普通promotion；owner_result的baseline_identity对齐实际activeauthority，promoted_identity只说明实际完成状态，不用数字大小判断更新。具体 public schemas 与 consumer schemas逐一成套切换，结构或语义旧入口在当前runtime拒绝并指向原owner迁移，不合成新pass。

Check6.0候选出口须验证完整当前reviewed content及对应candidate与公共Planning/Delivery一致，且不能调用final gate writer；最终passed仍调用原公共Check writer。RDT candidate_ready和Check candidate_checked各有独立exit输出schema，不以一个大量nullable字段对象代替。runtime不从scope、proposed正文或版本号判断semantic pass。

## 6. 状态、顺序、正常与失败流程

1. 原 Planning/Activation完成，同一Delivery实施并形成完整隔离贡献、拟写正文和必要ADR。#636可在implementing合法发布早期Draft，但Draft不证明最终Check或晋升。
2. 原独立Architecture phase2读取固定before authority、完整候选/拟写内容及受影响消费者，真实返回reviewed_candidate或no_change。RDT返回candidate_ready或真实no-change。
3. implementation已合法begin_check并进入checking后，原Check完成首次完整候选检查。候选有缺陷走implementation_required；规划实质变化走planning_stale；只有candidate_checked在原Check完成checking→implementation rework后进入最终整合，不写最终public Check gate。
4. 公共phase为implementing时，原两维护owner读取真实命中目标并合成。目标/组合稿有真实变化时，沿#637补充独立审核和受影响检查。没有知识变化就跳过实际写入和贡献/ADR创建。
5. 原owners只写已审组合稿，读回全部实际文件并判断适用性。部分写入只补同一可唯一恢复intent的pending；conflict或intent不明则停止原owner。输出丢失从实际匹配文件及原intent恢复同一结果，不新增successor或审计链。
6. 原implementation owner按同B及实际HEAD重建包含全部实际差额的candidate，并在implementing重新begin_check。原Architecture对实际候选给当前phase2结果，原Check在checking校验新candidate并检查全部最终变化和未改消费者，原公共Check writer记录真实passed并进入reviewing。已执行命令只在#637条件仍适用时采用，并说明来源；语义判断实际新作。
7. 原TaskCommit提交真实最终候选；独立Architecture branch_review及完整BranchReview绑定固定B..H、对比before authority，包含所有晋升文件和必要消费者。Ready/Publication/Merge消费真实promoted或no_change。额外内容变化回最早受影响owner，不用窄reference-alignment profile承接真实正文变化。

首次候选检查失败不进入最终整合；最终写入改变行为/接口/测试义务则回对应质量owner。mapped exits与缺失临时输出自动由原owner恢复，不制造人工批准链。Git冲突、必要依赖承接或平台更新阻塞才评估真实merge/rebase；没有这些阻塞时不为祖先关系造同步提交。

## 7. 恢复、兼容、迁移与集成

使用直接演进及一次受管切换，不新增长期兼容reader。`MIGRATION-638.md`逐项列出Arch4→5/Delivery2→3、RDT1→2命中入口、Check5→6与consumer/selector退出；旧schemas保留为历史validation资产，失去当前consumer的运行分支和当前示例入口删除或替换。真实API版本和历史含义不改。

在途对象分三类：未晋升的原owner重读候选和拟写正文后进入新候选检查/最终整合；已晋升但未完成最终Review的对象保留实际写入，补真实缺口，不重复晋升；已有最终Review者核当前适用性继续，只有真实变化才回最早owner。不能用旧pass补字段变新结果。旧计划适用Git authority仍能读取；Task完成、合法Reactivate改选或真实依赖改变时退出普通旧读，历史永久保留。

candidate_checked输出丢失时，先读公共phase与实际candidate：若仍checking，原Check重读同候选并完成本轮判断/合法rework；若已经implementing但尚未写入，原implementation owner先重新begin_check，再由原Check实际重新判断，不从phase制造候选pass；若已有晋升写入，由原maintenance owner恢复同一intent/结果，implementation绑定真实after候选并进入最终Check。所有恢复保留同DeliveryKey和固定B，不直接改state，不重放已完成写入。已有finalCheck/Review仍按其原producer恢复当前适用结果。

先在一个matching clean样本验证全套当前安装和in-flight reapply，再对本仓dogfood使用原受管同步。若原普通apply仍被228个legacy archives写前阻塞，保留该结果，不删归档绕过；只能通过原支持的matching tools升级处理本Task运行副本，按该owner要求先有可供安装的完整source。需要commit或额外安装副作用时在具体边界展示并取得确认。不能以局部复制runtime热改当前安装；不能把tools-only成功当普通全仓reapply通过。

同一最终业务PR包含代码、合同和实际current正文。独立baseline clone与原主checkout不移动。不开#635、不改Backend、不部署或Release。没有新增数据库或外部服务数据迁移；本次迁移对象是公共合同、受管运行副本和明确在途入口。

## 8. 验证设计

| ID / AC | 层次、入口与固定输入 | 预期观察及限制 |
| --- | --- | --- |
| V638-01 / AC01/05 | production promotion wrappers与真实临时Git仓：两个Task同B改能力A/B，稳定authority identity且根入口不变，逐次真实目标读/写 | 两完整能力保留，无总入口必写/递增要求；未命中unit/ref字节不变；非预填DTO可证明的AI语义另由V07证明 |
| V638-02 / AC03/04 | 同单元两合法贡献：B含条件/否定/例外，先晋升A再让B owner读真实目标并合成 | 组合正文保留原有效条件和双方改动；初稿与最终稿差额、关系/导航及两个未改consumer全部检查 |
| V638-03 / AC02/04/06 | 原implementation begin_check→Check候选wrapper/rework→最终integration→implementation重新candidate/begin_check→finalCheck→TaskCommit/BranchReview/Delivery wrappers | 逐步观察implementing/checking/implementing/checking/reviewing及content_ref；候选出口不写publicCheck，写后旧candidate被拒绝，新candidate才通过。未晋升不能Ready。no-change无空文件；无merge/rebase可晋升 |
| V638-04 / AC05/07 | matching schema/consumer projection和原恢复入口；未晋升/已晋升/已有Review三类，旧Git引用及普通mismatch/output-loss | 当前入口拒绝旧shape，不转换pass；同key恢复无重复写；旧意义可解析。只测普通错误，不造攻击或crash矩阵 |
| V638-05 / AC06/07 | Arch/RDT/Check/Review/Delivery/Publish命中package测试，shared Delivery projection及source validator | 独立发现真实路由/字段/阶段/内容错误，确认直接consumer；局部模块结果不冒称全链或Agent通过 |
| V638-06 / AC07 | 一个matching clean native Codex安装；完整reapply、在途Task/Delivery保全、声明平台投影、drift、mode、sidecar；本仓原受管同步 | source/dogfood/installed分开，逐项记录用户内容及`.new/.bak`。实际选择matching CLI/Core0.7.0-castbox.5；formal source lock缺口保持；不扩完整多平台Release矩阵 |
| V638-07 / AC01..04/07 | 真实native Agents通过安装后的原owners执行：不同能力双Task一组、同单元双Task一组、no-change及无需Git整合路径；#636Draft→#637后继差额→最终current组合 | 首次读完整拟写，最终原owner合成并写入，独立review覆盖全差额及未改consumer。公开正式输出、Git和当前正文证明实际工作；fixture预填pass只证明transport。无成本倍数目标，不把总时长全归无效流程 |
| V638-08 / AC06 | 本D1实际质量链、最终业务PR、Completion/Closure/Finish/Cleanup | 当前Check/Review、PR/merge及各生命周期终态分别取真实证据；planning或目录存在不证明完成 |

V07在实施前固定样本：能力A“查询超时必须保留原错误来源”，能力B“导出任务完成不代表通知发送”；两者无依赖。共享单元样本为“有历史数据时不覆盖已有条件，缺来源返回原repair”，A新增允许的只读查询入口，B新增导出入口，组合须保留缺来源repair和只读限制。未改consumer为查询调用方和导出调用方。测试范围限定同模型配置、权限、B、任务语义与已声明entry；实际Agent自行读authority、判断和调用，不接收host预写pass。真实数据均为去敏fixture，不证明Backend生产采用。

## 9. Canonical 引用、本轮差额与实际未决项

当前 [RDT requirement](../../../../../docs/requirements/current/knowledge-maintenance.md)、[design](../../../../../docs/design/current/knowledge-maintenance.md)、[test](../../../../../docs/test/current/knowledge-maintenance.md) 保留完整单元/历史/关系能力，本轮窄替代提前晋升与全局计数义务，并补T638场景。项目 [change-contract](../../../../../docs/architecture/06-governance/change-contract.md)、CURRENT/DOMAIN/INTEGRATION/GOV正文同步实际职责与公共版本，不宣称关闭ARCH-GAP-006/008。候选适用性仅由 [workflow-contract](../../../../../.trellis/spec/workflow/workflow-contract.md#candidate-applicability-and-coverage) 定义。

Task-owned Architecture贡献为 `docs/architecture/contributions/638-shared-current-promotion.md`；必要ADR候选为同名目录内`adr-final-integration.md`，最终进入上述语义ADR locator。RDT contribution使用`docs/requirements-design-test-contributions/638-shared-current-promotion/`；完整拟写内容在各本Task目录的`proposed/`，实施时生成真实正文，不预建空贡献。两原owner最终晋升；唯一实际结果由本次RDT `test.md`维护。

方案无未决产品选择。具体schema/projection、候选检查新出口及其必要性由Wording后的独立Architecture final_plan实际审核；若需机制修订，回Author及受影响资格owner，不以本方案预填通过。原Check两项基线失败、Architecture整组未完成、legacy archives reapply阻塞与formal_fork_source_lock均需本轮fresh归因；未验证不写pass。
