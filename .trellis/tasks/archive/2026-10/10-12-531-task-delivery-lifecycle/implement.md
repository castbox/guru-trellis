# #531 实施计划与验证边界

## 当前验收增量与未完成边界

真实安装漏 spec 修复沿 design §17.1 的原 installer writer；新来源的 clean apply、
reapply、原 drift、Claude/Codex/Cursor 投影检查实际通过，旧失败样本保留。
多 Delivery 隔离样本已由原 owners 完成 D1/D2 独立 Planning、scope 修订/恢复、
实施期与规划期退出；原 Completion 返回 evidence_pending，未把撤回当交付。
远端专用样本 PR542 已合入专用 base，原 Publish 同计划恢复与 Merge terminal
恢复已读回同一结果；历史 discovery 实际返回同 key、PR 与 merge。
这些事实不代表主 #531 Check、交付、整体完成或原业务会话恢复。

#149 mixed 新副本已完成 Upgrade/installed/native continuation，同 Task/gen0 与原
e27 候选保留，当前 gates 为空。原五规划迁到 Delivery 目录后十个相对文档引用
失效；上游原owner已确认Plan2 artifact内容能力，采用design §17.2显式窄投影，随后 fresh 原 Author/Architecture/Approval/
Activation/Check/clean TaskCommit/独立 Review。缺口未解决前不得提升该项为通过。

术语：本文“上游D1/D2”仅指上游历史交付阶段（接口opt-in/迁移采用），不是某Task首个/后继Delivery；后者以公共UUID区分并走同一生命周期。当前上游完成范围以2026-10-13正文为准，不继承旧阶段的退休/joint门禁。

## 1. 当前阶段

本文件是实施计划，不是实现完成证据。本 Task 当前 HEAD 为独立 base merge f03e8a04c487e64722e90697543ec7398de2b338，承接 main@bebf1993 与 Architecture .86 / RDT .89；此前 9bee7/main@8b55f624/.85/.88 保留为历史。merge不含 #531 工作，不是 gate pass。后续 main 演进由原 pair guard 判断。上游当前候选为 design §17 mixed CLI 5aeeb81c/45bb Core tar（§16的1e400140/185e保留为前序历史）、API1/schema2/Plan2和实际branch_bindings。§11的5181与§15 collision为历史，原失败保留。首轮 ce363 准入及执行保留为历史，不授予当前机制批准。已有受控 opt-in 集成代码待完整门禁；本轮修改仅推进受影响规划与已资格确认的局部修复，不提前迁移本 Task runtime。

实施准入：fresh审查上游固定candidate/API、补齐design绑定表与实例、核验#292/#530实际已交付合同、通过当前Planning Wording/Architecture/qualifications/Approval，然后按workflow展示完整计划并取得当次接受。创建确认不是计划接受。版本、接口或设计实质改变重新进入受影响Planning。

## 2. Delivery Policy 与执行位置

Policy：full。本Task当前选择整体解耦作为一个完整候选，不把规划草稿单独Publish，也不把局部API可调用当整项交付。当前计划覆盖全部accepted scope；无接口或联合证据时保留未完成，不由Delivery Review临时改为partial/staged。若后续实际边界需要独立切片，先回Author明确slice、remaining work和整体Completion条件，再重审计划。

目标castbox/guru-trellis，selected base/Delivery target为main；当前任务branch codex/531-task-delivery-lifecycle，generation 0。只在已解析的唯一注册Task checkout执行本任务写入；每次tracked写入前运行check-task-checkout-boundary。规划没有新建未来Delivery身份：本仓当前运行版本仍是旧合同，正式切换时按I01/I08迁移，不手工写未来字段。

## 3. 文件责任与迁移顺序

### P0：接口绑定与并行成果收敛

只读核验#31最新设计、PR/diff、审查、安装方式/API版本和原生证据；不是只看Issue状态。以 design §17 当前真实mixed候选逐项固化 I01..09，独立绑定其 source/tars 与公共 Plan2 的适用性，检查producer→公共input→公共output→consumer及正常缺失/冲突出口。若缺口仍在，回上游owner，不自填schema/API。

#292已CLOSED并交付main@8b55f624，拥有Author正向写作、来源设计承接与purpose回程；#531迁移其对象归属和consumer，不开发第二Author。#530已CLOSED，产品d7cde2f06经PR #540合入、PR #541归档；其actual committed_reentry contract/schema/runtime已读，按design §14逐项承接。本地base已整合main@bebf1993、Architecture .86/RDT .89，保留pending/index/runtime与其它工作树。新带入的旧Task runtime/schema/test/eval资产按§14 direct consumer逐项迁移/退出，不恢复第二活动入口；当前36项失败保留，迁移后定向重跑。后续必要base协调仍归原Reconcile/独立Git边界，不把来源交付当当前门禁pass。

### P1：D1 集成开发与 D2 迁移切换

主要位置：
- trellis/skills/guru-team/runtime/task_lifecycle/（以实际目录复核为准）及同名canonical runtime：Task identity、source、branch/resource、session、checkout consumer。
- trellis/skills/guru-team/contracts/task-lifecycle/ 与P2至P4列出的Skill schemas/interfaces/consumers：仅Guru I/O；引用上游公共合同，不复制其schema。
- guru-upgrade-installation及installer版本诊断：在apply前检查明确组合与迁移能力。
- guru-merge-task-delivery/history 与 guru-publish-task-delivery：旧cycle/PR/merge归属、在途事务恢复。

先在合格 D1 opt-in 的受控安装完成 API projection/Guru gate 集成，不切换旧安装。D2 上游迁移与 Guru consumer 就绪后，再成套删除 Task status 开发路由并切换旧安装；D2 不以 Guru 整项 Issue CLOSED 为前置。实现只做明确 API 调用和薄 projection。上游公共自有数据由上游迁移；Guru私有cycle/checkpoint/DTO/事务由原owner迁移。legacy header保留身份但须经过当前升级逐记录分类，不自动跳过/删除。新Guru包直接演进controlled consumers，不新增legacy活动fallback；未升级安装保留原固定发行包，待D2成套迁移。新兼容例外需回Planning具体展示后才可实现。切换前盘点旧active/archived、branch/worktree、session及远端事实；支持组合不完备则不应用。

### P2：Delivery Planning与返工/退出

主要位置：
- trellis/workflows/guru-team/workflow.md、README.md。
- 当前已交付#292的Author package及当前Wording、Architecture、Approval、Activate/执行入口、Clarify。
- public registry/interface/consumer及planning context locator，现有planning docs/freshness helper。

明确新增 Guru 自有 guru-create-delivery/guru-activate-delivery 两个 semantic 闭环，Creation/Activation 的输入/出口和既有 Skill Delivery profiles/schema 迁移见 design §5.3/§5.5；公共 key/types 直接引用上游，不复制 schema。Task scope/实施的确定性 projection 为无状态模块，由各自实际语义 owner 提供结果；不新增只包一条脚本的 wrapper Skill。

保留 Approval planning_result_id 作为仅交 Activation 的 Guru freshness token；公共 Planning slot 仅由 Activation 在真实转换时写入，上游 result_id 以 planning_accepted_result_id 交实施及正式 Check predecessor。两者不能同名混用，不将用户接受状态或过程写入任何结果。正常转换成功后丢输出恢复原公共result，尚未转换且接受不可确认时回原展示/接受路径。

D1和D2在首次Planning前使用上游身份创建owner；同一生命周期，Task整体authority分离。新locator/API以绑定表为准；D2不可覆盖D1恢复计划。迁移first activate/resume_execution为公共Delivery实施承接，保留原必要展示/接受和结果丢失恢复；退役旧Task status mutation/profile/reader，并明确破坏性I/O迁移，不静默改既有出口。

方案/部分scope返工同Delivery；整体scope先Clarify；全范围撤回经scope判断合法停止/unbind。已有PR关闭、分支/工作树清理走原owner和独立必要确认，不把退出当delivered。

V05 的正常整体 scope 修订必须实际执行原 Clarify→scope-only Author→accept_scope→
当前阶段 owner delivery_scope_revision→同 key Author；六阶段 wrapper 与现有
implementation adapter 均验证既有公共 rework 的 scope_ref 投影。不得用直接 API
调用替代阶段语义 gate。验证同输出恢复、其它 Delivery 不变、candidate 与历史成功
事实保留，以及当前受影响门禁局部失效；不以 scope 转换结果冒充 Planning pass。

### P3：Check/Commit/Review

主要packages：guru-check-task、guru-create-task-commit、guru-review-branch、guru-reconcile-task-base、配套runtime/contracts/consumer。

正式Check绑定当前Delivery完整切片和Task总体约束；普通检查method不推进正式phase。dirty必要增量提交；clean既有候选使用#530承接，不stage、不新commit、不制造tracked gate。base-contained、无在途Git操作、非空完整diff及freshCheck与当前candidate相符的实际约束按当前profile/API保留。明确selected base、完整status、稳定metadata、candidate HEAD及公共Check适用性按design §14逐项验证；缺base为stale_identity/base_branch，交原base owner，不默认main。原Git路径前置依实际profile验证；纯公共metadata/Plan2路径映射不成为必须新提交的业务增量。真实旧HEAD缺新planning路径时，按design §11.3/§17.2消费原commit/blob最小来源关联；缺模式严格bytes/modes，显式窄模式只接受同目标destination投影，不强迫clean候选重复提交；真实内容变化仍走必要dirty提交。完整旧安装的tracked产品增量按design §13由原Upgrade盘点、独立Git边界单独处置；只提交真实安装路径，不提交未来五规划/gate或无关文件，保留原业务commit祖先。零安装增量零新commit，待处置时不声称clean。实际新HEAD重新绑定candidate/freshCheck后接原committed_reentry。首次完整独立Branch Review仍必需，不拿Check/continuity Review代替。

dirty 提交改变 HEAD 的 Check/candidate 接续按 design §5 的 reviewing owner rework→实施 begin_check→Check owner 适用性重审→首次独立 Review 顺序执行。同内容仅重绑定受影响提交事实与 Check result，不重做 Planning、不强制重跑仍有效测试，不新建第二 commit。clean committed_reentry 保留原 HEAD。base演进、finding-fix和plan stale使用原最早owner回程，候选commit事实保持。所有touched非生成代码超过3000行触发机械拆分审查，避免把projection堆进新的巨型协调runtime。

### P4：Delivery Review/Publish/Merge与整体收尾

主要packages：guru-review-task-delivery、guru-publish-task-delivery、guru-merge-task-delivery、guru-review-task-completion、guru-complete-task-closure、guru-finish-task、guru-cleanup-task-resources、guru-reactivate-task。

保留现有semantic profiles和consumer责任，按必要identity/API变化显式版本化。Publish私有push_content/bind_pr/converge_metadata/mark_ready/ready不变公共authority；真实ready_for_merge及delivered/completion_seed按绑定表投影。正常成功后公共写失败/丢stdout从原owner恢复，不重复远端动作。历史恢复可记录实际成功，继续执行所需当前pass独立审查。

Completion重新读整体authority、遗漏工作和历史适用性；全部Deliveries合入仍可未完成。evidence_refresh/reactivation_validation、Closure/Finish/Cleanup在无currentDelivery时仍按原profile执行；Reactivate保留identity/history而新generation不复用旧gate。bookkeeping与业务Delivery分开。

### P5：运行面一致性与旧路径退出

trellis/presets/guru-team/README.md、overlays、canonical技能/运行包、所有受管平台start/continue/check/finish/natural-language/compression入口与模板按registry live声明逐项核验。入口只加载/调用/路由，mandatory skills按stable id显式调用；unknown/multiple/unmapped exit fail closed。

修改canonical后，先在绑定新pair的受控dogfood副本运行：
```bash
bash trellis/presets/guru-team/scripts/bash/apply.sh --repo .
bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```
命令在该受控副本执行，--repo .指向其root；同步dogfood投影并检查.new/.bak逐项处置。当前#531工作树的legacy完整安装保持，代码恢复不提前apply新runtime。自身成套迁移/apply须有匹配Plan2/private/native证据，再由原owner展示精确写集并处理必要确认。检查官方template-hashes/update语义，保留用户文件，不能把dogfood手补丁当唯一源头。

旧路删除条件：固定候选/API与支持组合已绑定；上游原生采用已证明；Guru当前controlled consumers已改；旧active/archived与在途事务迁移可恢复；真实installed/native/reapply证据齐备。只有必要旧历史读取保留给明确consumer，不保留旧开发writer或永久fallback。旧reader若为已发布consumer仍需要兼容窗口，应明列版本、owner、退出，而非私自破坏。

## 4. Docs SSOT Plan

Strategy：delta_first；当前需求/设计/test authority入口分别为 docs/requirements/README.md、docs/design/README.md、docs/test/README.md，共同绑定 RDT current-main-0.6.17-guru.89/active。Phase2由RDT原owner维护task-isolated contribution目录 docs/requirements-design-test-contributions/531-task-delivery-lifecycle/，承载 manifest.yaml、requirements.md、design.md、test.md、traceability.md，fresh绑定本Task、当前Architecture及两仓candidate/API；traceability连接需求、实际design责任和验收。原 .88/.85 contribution继承需该owner在最终Phase2前reconcile，旧验证仍保留对应内容身份。规划文档不取代durable authority。

Architecture contribution拟位于docs/architecture/contributions/531-task-delivery-lifecycle.md；实际影响/路径和必要ADR由独立Architecture owner判定。current Architecture baseline .86与change-contract-v1为expected启动身份，promotion时必须fresh，不能覆盖并行晋升。贡献涵盖owner变化、旧路退出和九concern，非逐原则评分或ledger。

Planning阶段直接绑定 design.md§9 的 task-owned contribution 与§9.1必要ADR候选；identity使用当前正式invocation实读内容，不另建审计副本。实施后才由原owner投为上述durable contribution并重绑实际identity，当前候选定位不冒充reviewed或promoted。

受影响durable specs：trellis/presets/guru-team/spec/workflow/下skill-package-contract.md、workflow-contract.md、data-contracts.md、causal-completion-semantics.md、companion-scripts.md、quality-guidelines.md；阶段专属合同保留在对应package/references/contract.md，实施前按实际被消费条款选定；更新唯一原authority，入口引用，不重复复制。README版本支持与升级合同同改。

RDT delta在最终Phase2前由原维护owner合并；Architecture共享晋升在独立committed Review之后串行执行。promotion新增diff重新fresh Phase2/TaskCommit/独立完整Review，再进入Publication。不能首次在Branch Review才合并文档。只有真正完成的验收写pass，缺接口、外部事实或未运行项保留unverified。

## 5. 风险匹配验证矩阵

所有场景由正常合法入口构造，保留真实事实，不手工伪造artifact/hash/state制造攻击负例。测试检查行为/consumer/副作用次数，不只镜像实现。确定性检查不代替AI scope/finding/完成门禁。

| 验证组 | 输入/入口 | 必须证据 | Owner与边界 |
| --- | --- | --- | --- |
| V01 canonical | 完整current packages/runtime/schema/registry/projection tests | 各正式wrapper单typed exit、薄投影、唯一consumer、无Task阶段writer | Guru；不重复上游full suite |
| V02 dogfood | 受控新pair副本canonical apply + drift；自身安装另走成套迁移 | 运行副本一致、可执行wrapper、.new/.bak逐个结果 | Guru；不覆盖其它工作树 |
| V03 installed | 一个代表性clean与一个受控旧安装样本，明确支持版本 | 安装来源SHA、两仓版本/API、正式wrapper和native continuation实际执行 | Guru；不是完整Release多平台矩阵 |
| V04 D1/D2 | 首次身份→Planning→实施→Check→commit/review→publish/merge | 同一链、不同identity、D1计划可恢复、Task整体scope保留 | Guru installed；上游原生样例由上游提供引用 |
| V05 rework/exit | D1方案改动、整体scope修订、部分/全部撤回 | earliest owner、identity保留、停止/unbind、无空commit/PR、Completion不误判 | Guru semantic owners及公共接口 |
| V06 #149形态 | 旧活动Task下一slice已planning事实迁移 | 同Task合法重规划进入实施，不重建/reset/首次activate | 受控副本；原业务恢复不在本项 |
| V07 #444形态 | 完整旧receipt/真实Git tracking、原候选/root五规划→Plan2/private→完整preset→§13精确安装增量前序→freshCheck | 原业务commit祖先与五blob保留、未来规划路径不预提交；只处置真实安装增量，首次完整独立Review可达、零空/业务重复commit | 复用#530成果与§14显式base诊断；记录真实候选 |
| V08 #155形态 | 局部provider事实缺口与独立必要consumer | 对应场景blocked，独立工作正确owner继续，真实缺口未消失 | 不实现provider业务 |
| V09 findings/base | 实现finding-fix、完整Review finding、base再演进 | fresh受影响gates、candidate事实保留、完整diff Review | 当前Reconcile/Check/Review |
| V10 publication | 同计划PR adoption、metadata/Ready丢输出、远端成功公共投影未完成 | 原事务恢复同一PR/result，无重复push/PR；stale义务回正确owner | 真实远端定向样本须另有精确副作用授权 |
| V11 merge/history | merge成功DTO/公共投影丢失、多旧PR/cycle | expected-head/CI/trailers、first-parent+GitHub核验、历史与当前pass分离 | 原Merge/history owner；不把bookkeeping当Delivery |
| V12 completion | 未分配scope、evidence_pending、nextDelivery、requirements/implementation回程 | completed仅整体充分；补证据/仅验证无空Delivery | Completion语义与formal exit |
| V13 closeout | Closure/Finish/Cleanup结果丢失/剩余资源、正常Reactivate | 原事务恢复、独立结果、新generation、cleanup不撤销完成 | 精确资源与必要确认 |
| V14 platforms/update | registry声明平台投影、native发现、压缩继续、reapply/template冲突 | 正确Guruowner、不竞争native gate；template-hashes/.new/.bak与用户修改保留 | 静态projection+代表性入口实际证据；未运行host单列 |
| V15 manual/task-free | 无formal Task的有界请求、独立Git/GitHub事实 | 保留原路径，manual不冒充formal pass | 不强制Task/Delivery |

V10/V11远端执行前展示exact repo/branch/candidate/PR和命令；当前创建授权不包含这些动作。能够本地验证的恢复合同和投影先完成，真实联合远端证据若未执行仍未通过。不得以mock成功冒充已安装或真实GitHub行为。

## 6. 联合验收与报告

联合证据须指向同一个 upstream 完整 source fingerprint/tar SHA/API 与 Guru 完整 candidate 内容身份；已提交 SHA 只识别其实际承载的 bytes：
1. 上游提供无Guru原生单/多Delivery、local/no-PR路径及公共接口迁移证据。
2. Guru提供真实installed D1/D2、返工/退出、clean复核、Publish/Merge输出丢失、旧history与整体收尾证据。
3. 两仓复用各自owned evidence核对projection/平台continuation；单仓green与joint green分别报告。
4. 原业务owner如需恢复，另在其授权范围安装/迁移并读回原Task/Delivery identity、实际candidate与typed exit。未发生这一步时只报告受控样本解决该类断点。

普通Issue不扩张完整Release矩阵，不发布版本、不关闭业务Issue、不自动同步业务工作树。收尾报告单列：设计完整度/审查、实现完整度、联合验证、原会话实际恢复与未验证边界。

## 7. 准入与剩余切换条件

本节 ce363 的初次准入是历史快照；当前同Task机制重规划按第8/11节和design §16，
不得复用旧Planning结论为新Plan2/private迁移授予实现资格。

D1外部实施准入B01/B02已闭合：上游四项正常路径finding经独立源码Review收敛，新包source增量/hash一致，三个新installed切片独立Review及交付重试、Completion/Closure已完成。该历史候选为ce36314b，包hash见design§5.4。当时PR #32 OPEN；当前已MERGED（merge 6e3ccc8d6d9e71dbcd77fbe6d945599e5f4f9b7f），不表示当前最终候选或Release已交付。当前实施绑定design§16，不复用旧准入。

当前计划通过fresh Planning链并展示后接受，才进入本Task的D1集成实现。B03实际Guru adapter/wrapper接续在实施中完成；B04公共Plan2已提供；Guru旧安装切换仍要求私有迁移和匹配验证，上游schema2原生采用与隔离legacy兼容由其owner独立验收，旧SDK/legacy最终退休归后续breaking release，不设为#31或Guru切换额外前置。#292/#530已交付成果按design §14及§12fresh复用；任何实质API/authority变化回受影响原owner，不重复创建Task，不替上游修复，不自动修改业务树。

## 8. 新候选匹配的同范围实施顺序

1. 绑定design §16 exact产品commit/tars/API/schema及本地snapshot区别，fresh读取两Issue、#292/#530
   及所有受影响原owner合同。已核验#292/#530 CLOSED且产品已交付main；按design §12/§14承接
   正式profiles、clean条件及退出，保持原owner，不复制旧私有checkpoint writer或创建另一Author。此活动机制修订完成Wording、独立Planning
   Architecture、适用qualifications与Approval，原执行owner走resume_execution，非首次activate。
2. projection既有kind透传错误在正常0600同文件场景复现，采用已formal-qualified的
   原公共helper透传修复，原9项与same-input回归重跑。该修复不新增状态/API。
3. Upgrade包新增独立delivery_upgrade/Plan2版本边界，修改原preview、preimages/write-set、
   source_candidate和same-plan恢复consumer；normal apply仍不是migration executor。
   使用185e真实installed collector/CLI fresh prepare，覆盖所有registered workspace、occupied archive、全部common/local session及原branch_bindings snapshot；按§16消费唯一active authority与其余defer副本的公共处置，保留各分支Task/五规划/modes，不创建peer私有迁移资产；不得将旧077模板/checkpoint换包same-plan接续。schema2 create/start不建Delivery、custom reinit及prunable sibling按design §11.2定向验证；
   原Plan1仅保留历史迁移consumer，不双写当前模型。代码分职责，不扩大巨型owner文件。
4. TaskCommit原owner增加仅迁移clean接续所必需的最小private来源consumer；先实际
   构造旧clean/root计划→Plan2新规划路径→freshCheck复现，再qualification和cause-local
   修复。不能为通过测试提前提交新路径、空/重复commit或把迁移metadata认作新业务增量。
5. Publish/Merge/history各原owner拥有自身有界旧cycle恢复输入转换；不通过Upgrade脚本
   判断PR成功、选Delivery归属或造currentpass。归属/义务不充分时保持精准blocked；
   archived公共历史必须由原语义owner在prospectivePlan2目标记录投完整PublicationFact+DeliveryFact，再由原Merge核验真实Git/PR后只读恢复；active store拒绝archived重复record不能改成reopen或私写schema。current generation的整体/收尾转换各走原owner，history_only不授予Reactivate。
6. 在受控副本执行#149/#444/#155实际旧形态及V04/V05/V12声明的多Delivery/rework/withdrawal/noDelivery/
   lost-output接续；原业务树与本#531运行安装保持，测试fixture真实本地commit独立于
   本Task工作提交。remote命令另需精确计划，现有本地样例不证明GitHub成功。
7. canonical spec/README、接口图和声明平台投影同步；新pair代表target执行真实update/
   apply/reapply、.new/.bak保留及drift。当前Task dogfood不提前切；其legacy→schema2迁移
   另在副本验证，缺任何支持组合不运行原树apply。完整Release矩阵不扩张。
8. 唯一RDT test.md分开保留ce363/077历史与当前185e新执行证据，冻结Guru完整tracked/untracked
   candidate后重新独立Phase2Architecture和Check；不promote共享authority或提交Task来
   制造pairSHA。只在实际consumer证据充分时返回matching readiness及其边界，上游自身验收仍归其owner；#531 joint不是#31完成前置。

## 9. #292 已交付合同的具体迁移执行与退出

P2 先实现 design §12 的九 profiles/五 exits Author新合同和原Clarify两段scope
consumer，连同八 Delivery profiles、purpose-bound Architecture3/Wording/Approval
输入输出成套迁移；先 scope判断、整体唯一写作、scope publication、Creation，再
Delivery Planning。不要在旧安装apply该候选或把Task scope-only列为Task Planning。

首次与活动整体scope修改、无Delivery Completion、D2 creation、Wording等价/实质修订、
Approval执行-only/方案修订和Architecture两purpose回程必须分别覆盖实际formal wrapper。
官方context选择当前workflow/spec、Architecture change-contract和task design，在本次
legacyTask用实际无--delivery命令；新受控安装才用真实upstream --delivery UUID。

Check的正常candidate_mismatch复现保留原失败输出；当前局部qualification确认原拒绝
链与漏映射cause后，将它映为原stale_identity并重入，验证同序列修改仍被拒绝且不
internal_error。它不授予Check pass、不修改公共candidate模型，不扩张攻击负例。

Source修复后fresh运行受影响package suite、正式Planning链和风险匹配的V01—V15；
旧installed快照 d052372a 的projection/native/reapply结果只作为历史，恢复后canonical
源码必须重新冻结内容并验收；不能用source结构检查取代当前installed/joint证据。

最终来源受影响验证必须额外覆盖final init/schema2 Task start、完整workspace/session盘点、fresh templates prepare、archived两facts转换与只读恢复、完整旧receipt安装增量前序；旧077结果仅按其身份保留。shared Architecture eval consumer应真实建立current selection并传递context，Phase2 fixture使用该helper的受影响回归需重跑。最终canonical/dogfood/installed证据绑定同一冻结candidate；基线继承drift缺项与本次定向drift分开报告，不能将历史失败改标通过。


## 10. 已交付 #530 的对象迁移与验证顺序

只消费 design §14 的唯一来源处置矩阵，保持同一 TaskCommit semantic owner。
先核对当前明确 base/注册 checkout/完整 status，再复核公共 Check result_id、
applicability、verify_candidate 与 actual HEAD；不新建 legacy Phase2 checkpoint。
读取稳定 committed identity 与五规划 direct HEAD blob；实际 Plan2 路径搬迁才使用
原 source bridge，安装增量由§13独立Git前序处理，不被metadata排除吸收。

分别验证缺base真实旧安装返回stale_identity/base_branch、明确base真实旧安装
fresh Check→原TaskCommit committed→post_commit pair guard→fresh Branch Architecture→
首次完整独立 Branch Review；对实际在途Git、真正dirty、正常planning/candidate/base
变化保持最早owner回程。clean通过时HEAD/index不变，不运行hooks或制造提交。
受控semantic authoring样本与真正独立host Check/Review分别报告，不以旧nullbase
默认通过样本作为当前合法接续。新main必要base整合与原业务会话恢复均另守精确边界。


## 11. 副本补修候选的实施与验收次序

当前来源与处置只引用design §1.1唯一矩阵和§16。5181 preview的真实collision、原
停止点与旧plan保持历史，不再声明新公共接口尚未交付。原Author先完成新候选独立
candidate_assessment、当前solution/Wording/final_plan/Approval与当前计划展示；
沿原legacy执行owner resume_execution，不重复Task首次激活或本地base整合。

原Upgrade consumer只做以下直接演进：
1. fresh冻结1e400140产品/185e CLI/45bb Core与完整Guru managed candidate，实际collector
   重新准备全部templates；不修改5181/077旧plan、其same-plan来源或rollback anchors。
2. 完整盘点所有eligible registered roots、occupied Task/archives、各分支五规划、
   common/local sessions、receipts/workflow与C4原binding。把已有binding bytes/mode
   投成公共branch_bindings row，包含unique active Task；不添加target path或binding writer。
3. 原Upgrade给定实际convert/current与defer/preserve。公共executor检查immutable来源、
   唯一authority与真实branch checkout；Guru不复制group判定，不省略副本或改TaskId。
   合法defer peers的Task/五规划/binding保持，不创建Delivery或Guru私有迁移资产。
4. 实读dry-run完整写集后，受控副本执行公共Plan2及原私有转换/完整preset；正常
   输出丢失从同plan owner恢复，普通source/binding/topology变化回prepare。后续安装
   增量按design§13独立处置；不得用新的HEAD覆盖旧rollback anchors。
5. 定向覆盖继承副本+binding、unique active+live binding、原Git-free合法组合的
   preview/current/session/native continuation与同plan resume/replay/rollback。
   对peer rawbytes/modes和没有新增迁移资产给实际观察；这不替代其它V01—V15。

#149保留实际D3a历史与D2b候选、五blob来源及§17.2显式窄投影，在同Task当前Delivery fresh规划
接受后进实施。#444沿五blobbridge/完整安装前序/freshCheck/首次独立Review，零业务
重复commit。#155真实dirty三规划沿原writer/必要提交链，不作为clean样本；保留
D1交付与P406局部依赖、独立查询场景，不接管provider。真实业务树与#531当前完整
legacy runtime保持，缺matching readiness时不apply原树；本轮不扩张Release矩阵。

full Policy、delta_first和final Phase2前RDT原owner reconciliation仍按§2/§4；
真实远端Publish/Merge及原业务实际恢复另守精确副作用边界。设计审查不冒充实现、
joint或原会话恢复，旧失败不重标为新candidate通过。
