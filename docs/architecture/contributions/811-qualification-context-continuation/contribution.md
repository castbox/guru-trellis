# #811 Architecture 隔离贡献候选

状态：reviewed_candidate（当前 Planning 已接受；本文件保留整合前来源，不是共享 authority）。Task为811-qualification-context-continuation/gen0，
D1为32f655a1-8b8e-4f02-94a0-7cf74fc39a6e，before为ca0b21f0dfc754a6979f919be14deee696719a4b。
来源为[Issue #811](https://github.com/castbox/guru-trellis/issues/811)。本文件是原Author的真实隔离拟写，
不是public handoff、授权记录、共享current或实施通过证明。原Architecture owner仍为guru-maintain-architecture-baseline。

## 责任与完整目标

原normal/solution各自准入，Clarify作具体scope/source判断与原source_actions，Discovery取证并生成context，
Sync只读取Git基线和投影已规范化return identity，原resume caller继续其未完义务。
两确认沿原graph补needs_context和mutation后的refresh返回；确认Task target独立于Task.source指向的Issue authority。
Task-bound output带必要task_ref/key，非Task不带；不从inventory推断对象、不改旧transition、不新增writer或state。
原Discovery duplicate_search通过authority_duplicate_snapshot向Clarify disposition提供最小真实事实；snapshot绑定实际authority，
private review_target/disposition与公开Task target分离。缺失/stale回原context owner，不重复搜索、不跨读private、不伪造disposition。

共享metadata属于同一实际context边：普通Interface1.10声明context4、consumer自有call_local.public_input和
profile-selected authoring seed。Clarify refresh只引用Sync目标Interface声明的结构化aggregate；Sync仍保scalar入口。
baseline_ready真实handoff_profile唯一选择pre_task/context_request；前者原AI补change_input/clarify_profile，
reviewed-plan还保source_locators，后者seed含原return_identity且AI只补change_input。seed不是完整输入。
原discovery/validator校引用及字段，原installed/installer保公开投影，original ordinary runner/reader消费run5。
registry1.5、production manifest6与extension current引用成套切换；旧1.8/1.9等发布字节和qualification run3/4保持。
这不新增独立resolver、状态、语义脚本或任意schema通道；完整当前合同由Delivery design5.4拥有。

本轮目标正文由所选Delivery design第4..7节完整拥有。Architecture拟维护的真实targets是：
`docs/architecture/03-domains/qualifier-applicability.md` 的确认对象/版本关系、
`docs/architecture/03-domains/workflow-context.md` 的producer/return边、共享metadata和AI authoring职责，以及
`docs/architecture/adr/qualification-context-continuation.md` 的决定。
同目录ADR候选给出理由、替代、成本和退出。完整共享after拟写及真实工程结果在实施期形成，
由原owner提交前final_integration核expected-current后整合/readback。本文件保留该整合前来源；
实际整合状态读取三个共享目标及原promotion公开结果，不以本文件建立第二个current或reviewed_promoted结论。

本次实施期已经形成完整隔离拟写；精确目标映射如下。相对业务引用按最终target位置解释。
源码与本 checkout 的 matching tools 定向验证已完成。本轮按最新 live #811 刷新为本项独立正常 Task/Delivery 验收，
不再以 #808 或特定发布对象为前置；独立 committed 质量链仍未完成。
这些文件仍是 proposed，不触发 shared 写入；各层实际截止由配对 Test 单写。
验收使用原公开入口建立的合法独立场景，两个真实 qualifier 输出经原 context producer、正式 clear 到原 caller 消费。
fixture 的显式语义输入只属于测试声明层，不新增实际 Agent 或远端业务证明前置，不捏造用户未决选择。

| target | 本贡献内完整proposed locator |
| --- | --- |
| docs/architecture/03-domains/qualifier-applicability.md | proposed/docs/architecture/03-domains/qualifier-applicability.md |
| docs/architecture/03-domains/workflow-context.md | proposed/docs/architecture/03-domains/workflow-context.md |
| docs/architecture/adr/qualification-context-continuation.md | proposed/docs/architecture/adr/qualification-context-continuation.md |

qualifier单元保留#793/812完整条件，只窄标两确认output/key的替代。
workflow-context单元保#792实际历史；其已被当前postcommit合同替代的执行时机明确为历史，
当前整合顺序继续读取原ADR和项目change contract，不恢复已退休candidate Check前置。

## 九 concerns

| concern | applicability与当前落点 |
| --- | --- |
| authority-binding | applicable：Planning3.0/Delivery1.0，baseline guru-trellis-architecture，项目change-contract-v1；后续非planning按原6.0/Delivery4.0，不混用 |
| constitution-binding | applicable：guru-trellis-design-constitution-v1五原则，采用原producer与直接演进；完整独立评估由原Architecture执行，本候选不替代 |
| boundary-and-decision | applicable：Issue #811和DES-793/812为authority；target_native，新ADR为ADR-QUALIFICATION-CONTEXT-CONTINUATION |
| owner-and-single-writer | applicable：上述原语义owners不变；原Author写所选计划，原Architecture单写共享架构，原RDT只写三层authority |
| compatibility-and-exit | applicable：successor成套切换，旧schema/example只保验证资产；current无dual-reader；旧pending回原caller重装，固定旧provider恢复；迁移由MIGRATION-811维护 |
| gap-and-deviation | applicable：本轮补已确认public context返回缺口；不新增或重开GAP，不把普通字段运输变成新scope authority；原缺口的关闭须本项独立正常Task/Delivery真实公共链与原质量判断，不由规划宣称 |
| parallel-scope | applicable：本Task规划和811隔离贡献允许写；shared root/system/ownership/index、其他Task不写；实际晋升由原owner核live expected-current |
| evidence-and-freshness | applicable：Planning绑定当前design原字节；source/installed/public链和fixture语义输入分别报告，未执行不填pass；实施candidate固定B/H后独立Review |
| review-and-promotion | applicable：candidate通过不是final_plan；本贡献/ADR经原final_plan独立判断；实施后原owner整合/readback，TaskCommit后一次完整独立Review才能建立reviewed_promoted |

## before/after、成本与边界

before：确认不能needs_context；Discovery只有旧四类且将Issue当target；mutation refresh经Sync退pre_task/stage0-current。
拟after：真实qualifier→Clarify→Discovery公开context及authority duplicate snapshot→Clarify clear回原caller；mutation另经原Sync实际read baseline再回Discovery，
保原profile/candidates/Task/key/target/mode/continuation/resume。两profile分别承担当前、缺失、普通过期及mutation行为。

必要成本是五包及consumer/Interface/Markdown同步、最小identity运输和实际source读取。
共享版本迁移另包含registry/manifest与直接runtime、installer、ordinary eval receipt readers。
不能只更新白名单而留下当前消费者不理解新增声明；不整体抬升无新增能力的其他包。
不增加通用continuation引擎、wrapper、资格ledger、授权或digest authority、锁与双reader。
旧四类保其原current/pinned支持边界，不恢复退休入口。#812其余输出与显式key判断保持。

## 检查、证据与直接consumer

project check descriptor沿guru-trellis-architecture-convergence:repository:1、id/version guru-trellis-architecture-convergence/1、
result合同2.0；本文件不替脚本或AI生成check pass。历史 final_plan 只适用于其当时版本；本轮当前直接 consumer 是原 final_plan Architecture owner。
原 final_integration owner 消费当前完整拟写；其正式结果记录实际整合/readback，随后新的独立 committed reviewer 消费完整实施 after 与工程事实。
V811-01..07由Delivery design/implement定义。五包、共享metadata和本 checkout 的 matching 采用已经实施并作定向验证；
前序整包失败、修正后定向通过及本轮独立完整链补证分别由配对Test保留，不回写旧观察。本项独立公共链证据仍由原 Check 按当前验收判断充分性，独立 committed Review 与外部交付仍未完成。
本贡献不据源码或安装结果建立完整验收通过；实际结果由配对 Test 维护。
formal_fork_source_lock、完整多平台/Release矩阵与生产效果不在当前已证明范围。
