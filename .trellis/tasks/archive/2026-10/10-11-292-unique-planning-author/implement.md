# #292 实施与验证计划

## I1 执行前提与范围

需求以prd.md及fresh #292 current正文为准；具体来源设计处置和机制只在design.md D2-D11。此处安排实现顺序与验证，不复制第二矩阵。首次规划时task处于planning，这是创建阶段背景；本轮fresh读取的状态为in_progress。当前重规划仍须完成current Wording、独立Architecture、三qualification与Approval，然后走原workflow展示/对话接受/pair guard和Execution的resume_execution。创建结果及此前activate结果均不证明本轮重规划门禁通过。

仅#292。不启动#521，不改upstream trellis-*、hook、global CLI/node_modules，不创建额外task/Issue，不执行发布/部署/业务仓安装。commit/push/PR/merge/closure/cleanup按原owner和各自精确副作用边界执行；本文件不记录或授予授权。

## I2 唯一 Delivery Policy

Policy：`full`。当前Delivery scope是prd R292-01..15及A292-01..10全部要求，包括Author实际激活、入口/恢复与来源设计行为证据。无partial slice、remaining stage字段或隐含独立交付。

交付成立条件：I4-I6的scope-required证据齐备，current Phase2及committed full-diff BranchReview通过；Architecture/RDT贡献经原owner晋升后新增diff再次检查、commit与独立full review；DeliveryReview确认完整scope和policy。当前remaining work是所有尚未实现/运行证明的accepted scope，归本task执行owner，不能用一次package测试或PRmerge消除。

Whole-task Completion条件：上述完整交付的actual结果与I5 native行为证据均满足，没有accepted requirement/evidence gap；Completion独立确认后Closure按source disposition执行，Finish独立持久化归档。release/deploy/full installer matrix不在本taskCompletion要求。package-only、installed-callable、global planning activated、Release四种结论分别报告。

## I3 最小 Docs SSOT Plan

策略：`delta_first`。任务隔离RDT contribution落点为 `docs/requirements-design-test-contributions/292-unique-planning-author/`（实施阶段由原RDT owner创建）：requirements记录本次新增可观察合同；design承接D3-D11；test为唯一实际验证结果与未验证边界；traceability/manifest沿当前RDT合同，连到本task与current shared authority。不复制任务来源设计矩阵或Architectureproposal。

直接consumer为 `guru-maintain-requirements-design-test-ssot`、final Phase2、BranchReview及Completion。RDT owner在final Phase2 check前完成required delta reconciliation；BranchReview不能成为第一次merger。Architecture任务贡献当前在design.md D9/D10，原Architecture owner在首次独立完整committed review后expected-current-bound promotion，并写必要durableADR。并行task只写自身contribution，不直接写shared current；shared Architecture/RDT各归原promotion owner串行处理。promotion新diff重新进入Phase2/Commit/独立BranchReview。

durable requirement/design/test authority与导航只由原RDT owner写入；受管 `.trellis/spec` projection从canonical最小规则同步。workflow/skill/package规则不重复成为第二RDT authority。未完成promotion的贡献不作current knowledge claim。

## I4 实施单元（依次执行，不作为staged Delivery）

1. **准备 owner与public contracts。** 在canonical `trellis/skills/guru-team/packages/guru-author-task-plan/`实现D3八profiles及四exits，独立input/outputschemas、semantic Markdown、最小recorder/validator和正式invoke。写作语义由AI，runtime只验结构与当前事实。新 `author_candidate_set` 接入三个原qualifier packages/interface/profile映射；原Approval profiles不改caller。
2. **Architecture目的专属迁移。** 修改原Architecture package的planning3.0 input/owner-result/output分支，按D5支持真实call-local prewrite对象而不要求未来贡献；final仍需真实贡献与current binding。保留非planning2.0；current router按purpose唯一分派，六个其它exit保留原义与同目的重入。独立review输入隔离由现有Markdown owner持有。
3. **规划消费者。** Wording planning pass→finalArchitecture；content_changed→原change router→Author。Approval显式检查D2逐项承接、policy/Docs与final当前Architecture。两Delivery router各自投影不同reason；Completion其它routes、#468Execution和#383因果语义原样保留。
4. **全局入口与旧边退役。** 更新canonical workflow的mandatory stable invocation、currentcreated/Phase1、start/prompt/continue/resume/compression及docs状态dispatch；薄platform入口只加载currentowner。删除D11旧竞争edge和planning2.0专属残件；更新 `trellis/skills/guru-team/registry.json`、受影响interface及README/MIGRATION-292。对外接口明确版本边界，不做长期fallback或双planningparser。
5. **官方投影与开箱验证。** 使用canonicalworkflow marketplace/preset同步dogfood和installed/projectedskills；先检查目标用户修改/hash与sidecar再应用，不静默覆盖。运行canonicalapply及drift，逐个处理.new/.bak并记录；upstream官方脚本/skills不patch。完成I5真实入口证据，失败按D8表的精确出口回owner修订并fresh重审。
6. **权威与交付收口。** delta-firstreconciliation→完整Phase2→TaskCommit→独立完整BranchReview→serializedArchitecture/RDTpromotion→freshPhase2/Commit/fullReview→DeliveryReview。随后Publish/Merge/Completion/Closure/Finish由原owner执行，不提前关闭#292。

源文件影响限于上述canonicalpackages、registry/interfaces、workflow/README/preset入口、对应tests和受管投影。实施前fresh检索真实consumer后决定精确文件集合；不以历史归档textmatch作为runtimeconsumer。触及的非生成code文件超过3000行时先做机械拆分/小解耦review，不能顺带扩大无关重构。

## I5 验证分组与观察结果

| 组 | 入口/观察点 | 必须捕捉的失败与通过条件 | 验收映射 |
| --- | --- | --- | --- |
| V1 Author正式调用 | installedinvoke八closedprofile及原consumer输入；真实docs/官方JSONL写作 | owner/exits唯一，错profile/缺合法input停止；AI写作事实可见，不从runtime自动生文推断语义pass | A01/A09 |
| V2 同任务集成链 | requirements_ready→前置Architecture→solution_planning→plan_ready→Wording→finalArchitecture→Approval，actualpublicstdout薄串联 | 无docs首次candidate不会要求未来贡献；final不回Author；前置result不跨Wording批准；每个exit唯一consumer | A04/A05 |
| V3 正常入口及brainstorm | native“讨论方案”“设计新功能”“先做规划”；currentcreate/start/continue/resume | 加载brainstorm后Guruowner写作，已有Clarify不重访谈，无额外consent/reset，门禁与activation不跳过 | A02/A04 |
| V4 docs与恢复 | native无PRD/PRD-only/design-only/three-doc/officialseed/partial/stale，真实interruption/compression | 同TaskId/generation/source/checkout；丢producer结果fresh重建，普通mismatch回resolution/stop，无替代task或伪造approval | A02/A06 |
| V5 来源A-D与正常遗漏 | 去敏技术Issue-shapedfixture包含需求及A-D设计，真实Author/Wording/Approval | retain落点存在；正常遗漏被Approval挡住；change/reject有rationale及上游处理；source更新仅失效依赖阶段；普通技术细化不增加scope问题 | A03/A08 |
| V6 修订/两Deliveryrouter | actualWordingrewrite、Approvalrevision、DeliveryReviewpolicygap、Completionnextdelivery及其它exits | 不合并两个router/reason；remaining_work/evidence_pending/implementation修正保留原owner；source/scope/Architecture实质变化从最早owner重入 | A06 |
| V7 Policy/Docs/因果 | full/partial/staged的真实Authorconsumer输入，四Docs策略，三个qualification正式调用 | policy唯一/不越scope；no_docs_update_needed非exit；RDT owner及deltareconcile顺序；feature applicability与#383证据语义不被扩大成repair宣称 | A07/A09 |
| V8 投影/安装/update | source/installedpackagecheck、声明platform入口、一个代表性cleanthrowaway后existingupdate/reapply | new/oldcaller同步迁移、modes可执行、sidecar与ownership无静默覆盖、overlaydrift=0；nativebehavior与projection证据分别报告 | A01/A02/A10 |

V5的负例来自正常作者遗漏和真实source修订，不手工篡改artifact/hash/state或模拟恶意caller。V2/V6/V7的确定性fixtures只测试真实wrapper执行/DTO解析和路由；语义判断由实际AIowner执行。文件齐全、字符串比对、schema通过不是planning/native行为证明。新增case必须能检测不同defect，不添加重复assertion计数或未来防御场景。

V3/V4/V5/V6是本Issue必需native证据。用当前平台实际对话与工具结果观察，不用package-local eval冒充；若平台不支持主动真实压缩，只记录能执行的interruption与current压缩恢复事实，缺的具体compression验收保持blocked/evidencepending，不虚写PASS。原生多agent执行仅限既有Architecture独立要求或验证工具明确支持的场景，不新建用户chat或自动外发消息。

## I6 定向命令与证据边界

实现后使用managedPython运行Author/Architecture/qualifiers/Wording/Approval的受影响测试及真实wrapperevals；测试命令从各liveinterface读取，不假设全局python具有jsonschema。现有managedruntime由 `.trellis/guru-team/runtime/resolve-python.sh`解析。本轮systempython缺jsonschema，managedruntime可用；这不是测试已经通过的声明。

运行现有source/installedchecks与投影：

```bash
.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode installed --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

实际sourcecheck的root/command若liveinterface已演进则fresh采用其声明argv，不发明fallback。apply不自动更新activeworkflow；按官方 marketplace先create-newpreview，对字节/hash/sidecar/用户改动及liveidentity后同provider显式force。target CLI从source lock指定built Fork解析，本轮 `0.7.0-castbox.3`；全局PATH的旧0.6.17不作为target证明。workflow与preset使用同一Guru候选，不改global安装。

一个cleanthrowaway及其后existing状态承接V8；不执行完整多platforminstaller/upgrade/Release矩阵。声明platform projections做定向一致性与dispatch审查；只有实际运行的平台能声称native行为通过。完整matrix、tag-pinnedsmoke、软件Release、业务仓安装/部署明确未验证，交专门owner，不能转成本task失败或通过。

实际检查結果只写唯一RDT test落点及阶段所需最小owner-private结果；不新建per-test rationale、ledger/cache/审查账本，不持久化授权。外部请求、wrapper结构、semanticowner判断、nativebehavior、安装效果各自注明能证明的范围。

## I7 规划阶段限制与风险

首次规划时尚无Author实现或native/installed迁移证据，目的专属3.0当时是待实现合同；这些是创建基线背景，不是当前候选状态或验收结论。当前canonical与installed候选已包含Author和目的专属Planning 3.0；本轮接口核对不判断既有native/installed迁移证据是否满足验收。D9/D10仍是task-local设计，不是sharedauthority更新。当前规划必须通过已安装Wording、独立Architecture及Approval；不得从接口已安装推导Author写作或前置3.0评估已执行，这些事实只由实际owner输出证明。

主要风险是正常nativebrainstorm仍按上游写作、旧in-flightplanning缺purpose、final结果误回Author、consumer同步遗漏，以及真实compression无法执行。分别由D4、D5/D8、D11和V3/V4捕获；缺accepted证据不关闭Issue。规划语义通过只授权进入展示边界，用户接受后才能由Execution进入实现。
