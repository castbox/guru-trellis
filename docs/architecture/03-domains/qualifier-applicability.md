# qualifier 适用条件与原 owner

Identity：ARCH-DOM-QUALIFIER-APPLICABILITY；aliases：conditional qualification、explicit-task qualification、#793、#812。
原 owner：guru-maintain-architecture-baseline。状态 current；#793 定义来源为 Issue #793 和
固定 before Git e30c7bb5d4c24bc075dc14cfcd04c1da00fcf78e。本次 #812 来源为
[Issue #812](https://github.com/castbox/guru-trellis/issues/812)，适用 before Git
f16bb562e4ea844939786cebd5c6c20e686914b2。原 owner 在批准 Planning、实施与工程验证后，
于 final_integration 整合完整定义并读回；#812 内容为 integrated_pending_review，
独立 committed Review 尚待执行。决定分别为
[ADR-CONDITIONAL-QUALIFICATION](../adr/conditional-qualification.md) 和
[ADR-EXPLICIT-TASK-QUALIFICATION](../adr/explicit-task-qualification.md)。

## 完整职责

normal、solution、root 分别独占场景准入、业务 authority 承载与因果候选准入。
各原包 `references/applicability.md` 独占可先读取的触发、采用、刷新和加载条件；
完整资格算法仍在原 Skill/contract。caller先判断是否需要该owner，不在短条件层
给qualified/rejected或因果充分性verdict。原stage仍判断其scope、规划、实现、
证据、severity、readiness与完成，qualifier不会替代这些职责。

十类lifecycle及已有Author profile在各自候选提升边界分别读取三条件。触发且无
适用结论时显式load原stable Skill，以实际适用非空集合执行原闭环；未触发不
load全文、装配空输入或制造classified/skipped结果。solution检查真实机制承载的
业务决定、证明、拒绝或执行资格，不把普通计算或OS关键词当完整判据。root按
真实诊断、缓解、修复、保护行为进入，普通feature名称不能遮蔽实际机制。

root入口使用caller当前场景/authority-placement判断，消费真正触发的上游结果；
正确未触发的normal/solution没有结果前置。非通过先回各原唯一consumer，未变
机制采用仍适用结论；实质authority、机制、支持路径、条件或证据变化刷新依赖项。
丢失必要结论回原producer。新invocation仍校当前facts，采用不重放旧envelope。

runtime只校schema、facts、coverage、aggregation和consumer，不决定是否触发或
语义pass；没有新Skill、wrapper、classifier、资格数据库或授权持久化。#793当时不扩大输出；
两类确认output的当前窄替代由下文#811定义。

## 选择、成本与采用

仅删global mandatory不能消除原caller/root前置；统一wrapper/固定问卷会复制
三个owner。选择各原owner短reference和原caller落点，减少不适用全文与装配，
保必要判断和原出口。新增reference有现有caller直接消费；不为未来预留状态。
本设计没有费用比例或业务效果结论。

[MIGRATION-793](../../../trellis/presets/guru-team/MIGRATION-793.md)保留条件调用的原采用边界；
当前显式输入的成套采用与旧输入退出由下文 MIGRATION-812 承接。
旧完整安装采用前保其匹配合同，同Task/gen/key/root按实际义务续接。原tools owner
保Task/session同步受管投影，原Architecture/RDT在candidate检查后分别晋升完整
定义并readback，actual after再绑定和最终质量链。不存在兼容双reader或新审批链。

本单元窄替代原固定调用、root两上游普遍前置和无材料变化的重复要求，保
ADR-008/020的其余职责和#383完成语义。方法变更、真实authority/consumer变化时
回原owner重审。R/D/T关系为 `REQ-793` → `DES-793` → `TST-793`，完整定义位于
各层 `current/qualifier-applicability.md`；实际观察由配对Test单写。

## 显式资格对象与输入版本

七类 Task/Delivery qualification profile 由原 caller 明确提供完整上游 DeliveryKey：
planning_scenario_set、author_candidate_set、implementation_discovery、
base_impact_candidate_set、phase2_candidate_set、branch_review_candidate_set、
publication_candidate_set。精确输入由各原 package 的 Interface/schema 拥有。
phase2_candidate_set 只保既有 pinned-old/recovery 边界，不恢复退休 Check 阶段。
四类非 Delivery profile 保持原输入和职责。

共享 qualification_facts 以该 key 复用原公共 Task/Delivery model、当前 generation、
C4/C5 与唯一 registered checkout 事实。有官方 context 时，官方 current 必须为同一
完整 key；缺失、错误、terminal 或冲突交原 owner，不能走无 context fallback。
只有官方 resolver 确实无 context key 时，才由原 current(key) 校验显式对象，不写 session。
该 key 不成为新的选择 authority。

Planning 解析该 key 的实际 planning_root。需要 Planning identity 时，以其中 prd.md、
design.md、implement.md 的原字节构造既有 file-set identity；supplied planning_paths
必须等于这三份实际文件集合。author_candidate_set 只校自己的已有 author_paths 与
author_identity，不要求未来 design/implement。原 HEAD、路径、候选和 file-set 校验继续成立。

原 caller 在调用期保留实际 TaskRef/key/profile 与目的，消费原 classified 或非通过出口，
回到自己的当前义务。三 qualifier 的语义算法、条件加载及唯一 consumer 保持；
classified及其他原输出不新增key、恢复或审计属性；两类确认output的窄替代见下文#811。
没有新增binding/selection writer、资格存储或授权记录。

## 迁移、成本与重审

三个 package 的七类当前输入使用独立 path/id 的 input 2.0，aggregate 使用3.0。
Interface、runtime selectors、原 caller、新版公开输入示例和受控 eval/test 成套采用。
旧公开 profile/aggregate schema 与输入示例的 path/id/bytes 保留为历史验证资产，
没有 current runtime consumer；current 不双读旧形状，也不猜缺失 key。

[MIGRATION-812](../../../trellis/presets/guru-team/MIGRATION-812.md)拥有精确采用、
旧 pending 重装、固定完整旧 provider 恢复及工具回退合同。已完成结论只在原 applicability
仍适用时采用，不改写为当前阶段 pass。旧待调用输入由原 caller 从真实已知对象重新装配；
缺失身份回原 owner。旧 provider 未完成操作在其固定完整 provider 下恢复，不重复副作用。

必要成本为完整 key 传输、原事实读取和三个 package/caller 的版本同步。该方案直接复用
已有 model，避免新增 session 写入、重复 resolver 和资格账本的维护及恢复成本。
inventory 推断、借其他 context、跳过 Planning 或复制 resolver 不能保留原对象与校验职责。
对象 authority、caller/consumer、官方 context 规则或支持的恢复边界实质改变时，由原 owner 重审。

R/D/T 的 #812 完整行为、设计和验证分别由各层现有 current/qualifier-applicability.md
承接。本轮源码、确定性入口、实际 AI/caller 与安装观察见
[配对 Test](../../requirements-design-test-contributions/812-explicit-task-qualification/test.md)；
各证据只覆盖其实际层级。formal_fork_source_lock、完整多平台安装/升级/Release 矩阵
与生产效果仍未验证。原 TaskCommit 与独立 committed Architecture/Check/full_review、
后续 readiness 和外部交付终态仍由原 owners 判断，当前整合不建立 reviewed_promoted。


## 资格确认的原context接续（#811）

本节来源为[Issue #811](https://github.com/castbox/guru-trellis/issues/811)，适用before为
ca0b21f0dfc754a6979f919be14deee696719a4b。本节由原 Architecture owner 在 #811 final_integration 整合并读回，
状态为 integrated_pending_review；独立 committed Review 尚待执行。
决定为[ADR-QUALIFICATION-CONTEXT-CONTINUATION](../adr/qualification-context-continuation.md)。
它仅窄替代#812两种scope_confirmation_required不携Task/key的输出约束；三qualifier算法、
条件调用、显式对象校验、classified及其余输出职责保持。

normal/solution真实确认出口保候选、target、mode、continuation、resume consumer，并从已校验target
为Task-bound分支投影task_ref和完整DeliveryKey；非Task为独立分支。原Clarify独占具体scope/source选择，
Discovery独占当前证据获取及context生成，Sync只读取Git基线并投影规范化返回identity，原caller继续未完义务。
Task target保持Task locator；实际authority按Task.source读取Issue，合法no_issue沿accepted_scope/draft/source，
不把Task对象、来源authority与官方会话context key混为一项。

缺失或正常过期context通过原Sync read和Clarify needs_context进入Discovery；真实context_ready回同一确认。
Discovery公开原duplicate_search的最小authority_duplicate_snapshot，绑定实际Issue/draft，供Clarify原AI disposition
和action校验。Clarify不重复搜索、不跨读private；缺失或stale snapshot回原producer，不静默替换Task.source。
真实load-bearing source_actions执行并live reread后仍返回refresh_context，保原return_identity经Sync实际baseline_ready
回Discovery context_request。Discovery重读已变authority和duplicate事实，Clarify核已生效选择后clear，不重复mutation。
正式clear只交原caller，不能充当资格、实施或完成pass；scope变化仍回原whole-scope owner。

公共确认输出3、Clarify确认input2/private5/needs4/refresh3/独立clear1、Discovery request3/ready6/context4及Sync确认read
成套迁移。精确字段、封闭分支与路径由原package Interface/schema和[MIGRATION-811](../../../trellis/presets/guru-team/MIGRATION-811.md)拥有。
共享普通Interface1.10、consumer自有call-local input和profile-selected authoring由
[ARCH-CONTEXT-001](workflow-context.md#8-资格确认共享合同与ai补写811)承接。旧发布字节和原四类current/pinned支持边界保持，
不恢复退休active Task-status入口，不新增资格存储、状态机、授权记录或任意schema通道。

必要成本为五包、共享metadata及直接reader/installer/ordinary receipt消费者同步维护和每轮真实取证。
复用1.9会混淆instruction-only职责，删descriptor或重标context版本会隐藏当前合同缺口；wrapper、continuation store
与inventory推断复制原职责。因此选择原graph内target_native演进。authority/source/consumer或合法恢复边界实质变化回原owner重审。

R/D/T关系为REQ-811→DES-811→TST-811，各层current/qualifier-applicability.md单写完整定义；
本项以原公开入口建立的独立正常Task/Delivery场景验证两类真实qualifier输出、context producer、正式clear和原caller消费。
不绑定特定发布对象或时点，不捏造未决选择；fixture语义输入属于测试层，不新增实际Agent或远端业务证明前置。
实际工程、安装、独立公共链与外部交付结果由[配对Test](../../requirements-design-test-contributions/811-qualification-context-continuation/test.md)单写。
源码、installed、实际Agent和远端结果分层；规划、结构检查或部分试跑均不建立完整验收或reviewed_promoted。
原maintenance owners在工程验证后提交前整合/readback，TaskCommit后一次独立committed Review判断实际before/after。
