# D1：实施与验证计划

## 1. 输入与引用

整体范围读[Task PRD](../../prd.md)，本批完整范围读[PRD](./prd.md)；技术方案与唯一来源处置读[design第3节](./design.md#3-来源设计处置唯一)。本批没有前序Delivery；固定B与Planning H0为`2dbaf308e6d5137bf640cfe546a078497c1c713a`，最终实现H待形成，PR目标main。原独立candidate_assessment及其key/root/purpose如design第1节，不代替final_plan或实现结果。

实施前实际加载 `.trellis/spec/workflow/{workflow-contract,companion-scripts,data-contracts,skill-package-contract,quality-guidelines,subtraction-first-compatibility}.md` 的适用完整条件、`.trellis/spec/preset/{installer,upstream-ownership,overlay-guidelines}.md`、原Architecture/RDT contracts及current-knowledge。公开README改动再读docs/public-docs。source source/工作流源码以canonical为准，安装副本不手改为唯一源。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置/owner | 文件与实际动作、完成观察 |
| --- | --- | --- |
| I694-01 | 当前规划已接受并由原Activation进入实施；implementation owner | 复核live #694、实际selected key/root/phase与原实现入口，读所列specs。范围或机制真实扩大回原owner，不借批准改后项。 |
| I694-02 | I01；Architecture/RDT原owners | 从B下完整authority准备task-owned RDT contribution及Architecture完整proposed单元；明确R679/D679/T679和实际Architecture目标及必要关系。shared current暂不写。 |
| I694-03 | I01及受审设计；implementation owner | 在原Architecture `runtime/invoke.py`实现purpose限定的只读接入helper，复用原对象/C4/checkout和public facts，保原stage/scope/root/design freshness及typed校验；共享current/key与其他consumers保持。 |
| I694-04 | I03；原workflow/Architecture责任 | 同步canonical workflow Explicit receiving-session/Planning派发、Architecture Skill/contract和必要派发入口引用；分开一次性无写评审与普通owner runtime恢复，保authority-first/独立性。核所有实际引用，不复制step-local规则。 |
| I694-05 | I03/04；implementation owner | 在原Architecture和受影响原测试中增加/修订V01..04，核正式stdout→当前aggregate/分支/projection/Approval输入；保原五Planning consumers和合法无context能力。源说明与断言共同承接目标，无新增专项eval资产。 |
| I694-06 | source候选完成；原preset/tools-only owner | 写MIGRATION-694与必要README使用边界，从canonical完整同步dogfood/installed/声明平台。保历史Task/session/用户内容；plain apply若被真实preflight阻止，沿原tools-only恢复。逐项处理真实sidecar，不手改hash/manifest。 |
| I694-07 | 完整实现+隔离拟写；原独立Architecture/Check owners | 审完整候选与proposed targets，原candidate Check合法返implementing后进入原final_integration。Architecture/RDT各自写经审完整单元并readback；implementation重绑全部实际candidate并begin_check。 |
| I694-08 | 原最终质量链 | 最终Architecture/Check、TaskCommit、独立固定B..H完整Branch Review、Delivery Review/PR readiness按原owners执行。Git提交/push/PR/merge及整体收尾仍按各自当前精确副作用边界。 |

只修改本批明确源/派生投影、必要现有tests及真实Docs差额。任何触及的非生成代码文件不超过3000行；必要机械拆分在原责任内审查，不借机改造无关模块。没有新服务、存储、依赖或业务数据迁移步骤。

## 3. 验证入口、输入与预期观察

| 验证 | 入口与输入 | 预期、设计/AC及边界 |
| --- | --- | --- |
| V694-01 | `python3 -B -m unittest discover -s trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/tests`；使用当前锁定installed upstream scripts | 原formal wrapper在正常不同context/选择下核只读final_plan；对应design V01、DAC01/02。预置语义fixture不等于AI判断。 |
| V694-02 | 原shared DeliveryProjection installed tests与受影响Author/Wording/Approval/Activation packages原测试；准确依赖路径由现行source lock确认 | 保其他目的/consumers、真失配及原错误consumer；对应design V02、DAC02/03。缺依赖为blocked/SKIP，不声称pass。 |
| V694-03 | 原Architecture tests中实际stdout的Interface当前schema/consumer组合，以及相邻Approval当前输入/guard | key/root/purpose/freshness正确，成功与非成功只走原consumer；对应design V03、DAC04。测试不能仅验证孤立schema或字符串。 |
| V694-04 | 原skill-package/source/installed验证、workflow routing/受影响contract检查；Python用quality-guidelines规定的内存compile，shell语法及`git diff --check` | 结构、runtime事实、原caller边界与文案一致；原独立语义Check/Review实际审读，不能用scanner代替。对应DAC03/05。 |
| V694-05 | `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`和原`check-dogfood-overlay-drift.sh`；如plain apply被历史数据preflight阻止，先沿原tools-only owner完成相同受审投影再核drift/installed | 同源投影、mode、reapply及递归`.new/.bak`真实结果；对应DAC05。无额外安装或矩阵，existing业务安装/各平台Agent行为未运行不宣称通过。 |
| V694-06 | 原scope完整Check→原owners final_integration/readback→candidate刷新/begin_check→最终Check/TaskCommit/独立完整committed Review | 审全部R01..07、完整实现与真实shared-current结果。工程事实可按原适用性规则采用，当前各语义gate仍实际执行。 |

精确命令/参数按当前公开help/Interface确认，不调用eval/private实现构造结果，不添加输出台账。只跑证明当前accepted scope的最小可靠集合；变更或失败有具体风险才补充。当前所有实施验证为待执行，不预填pass。无后端#961、部署、业务数据或生产效果验证。

## 4. 停止条件与适用回退点

身份/唯一checkout/选择错误回原Identity/Ensure/Bind/Selection；scope/来源变化回Clarify；机制/authority冲突回原Author/Architecture。正式invoke失败保实际code/field/remediation，新轮fresh重入，不patch私有结果或改报成功。缺真实依赖停止其相关验证，不能降低验收。

受影响源码或projection检查失败先修本批canonical及其consumer。保留无关并行改动；不reset、stash、覆写用户内容。普通本地候选可在受审范围修订；无数据/部署变更，故不新增数据回滚、双读或发布恢复协议。共享写入只在final_integration，对真实expected-current冲突由原owner重审。Git/GitHub副作用不由本计划代替后续确认。

## 5. Delivery Policy（唯一）

**full**：D1覆盖整体R694-01..07及AC694-01..05，没有计划延期的实现项。完成条件为本切片实际代码/合同/当前知识与受影响分发一致、原质量gate及真实PR交付满足；整体Task再由Completion审全部范围，Closure处理#694，Finish归档并明确资源处置。合并不代替整体完成。

没有临时产品限制或后继实现切片。验证层次边界不是未实现功能的替代；若实际实现或证据仍有accepted scope缺口，交原owner处理，不能标为已完成或新建空Delivery掩盖。

## 6. Docs SSOT Plan（唯一）

Strategy：**delta_first**。canonical源码/Skill/workflow候选和task-owned完整拟写先收敛，shared current在原candidate Check后的final_integration由原owners分别维护，最终Phase2之前完成reconciliation/readback和完整candidate重绑。

| 原writer→直接consumer | 真实差额与目标 |
| --- | --- |
| RDT owner→Author/Approval/implementation/Check/Completion | `docs/requirements-design-test-contributions/694-final-plan-object/`下requirements/design/test/traceability/manifest及命中完整proposed；维护`docs/requirements/current/task-delivery-lifecycle.md` R679接收行为、design D679职责、test T679正常验证，增加R/D/T694关系，保留其他既有语义。 |
| Architecture owner→独立Architecture/Check/后续Planning | 真实贡献`docs/architecture/contributions/694-final-plan-object.md`及同目录下完整proposed targets；按实际命中更新CURRENT、ARCH-DOM-019/043/045、change-contract与必要关系。ADR候选`694-final-plan-object/adr-explicit-review-object.md`在final_plan实际审查后由原晋升写目标ADR及必要导航，不复制全库或递增全局版本。 |
| canonical workflow/Skill writer→现有平台caller | 修改`trellis/workflows/guru-team/workflow.md`、Architecture package Skill/contract、必要overlay入口引用，说明只读final_plan与普通恢复runtime边界。canonical是唯一源，dogfood经完整preset同步；入口不复制步骤。 |
| 原公开文档/安装owner→当前采用者 | workflow/preset README必要采用边界、MIGRATION-694和命中spec最小projection。保官方marketplace preview/显式应用、matching preset/reapply、用户编辑及sidecar机制。源码变更不冒称已有安装采用。 |

根README/index仅在定位或必要关系改变时更新，不添加逐Issue总结。历史contribution/ADR/归档保历史身份，当前完整单元不留“旧指令+override链”。原候选Check、真实final_integration、最终Check和committed独立Review覆盖全部实际写入。
