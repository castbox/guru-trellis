# Gen2 采用切片：实际安装已交付的 Sync 修复

## 1. 整体来源与术语

Task `808-release-v070-guru9` / generation 2，Delivery `9076720c-9302-4343-b50c-50a39a68a65a`，planning_root为本目录。整体权威为[根PRD](../../prd.md)，accepted revision为`sha256:835586c0c5ca6a22a50a872ce8249a2548dfac4d6f84a4321f78f4d06addb950`。本批选择AC-04及自身适用AC-01/03/05/06，不改变整体范围。

| 来源、章节 | 角色与用途 |
| --- | --- |
| [#808](https://github.com/castbox/guru-trellis/issues/808) 前置与准备范围、冻结候选与验收、正式发布与本地收尾、完成条件与范围边界 | 要求：完整来源交付后真实dogfood采用；准备终态与Stage2分别执行 |
| [根PRD](../../prd.md) §3.3/5.4/5.5/7 | 已接受要求：来源→采用顺序、完整目标验证及自身独立交付 |
| [原tools合同](../../../../../trellis/skills/guru-team/packages/guru-upgrade-tools/references/contract.md) Entry、Forward behavior、AI Review Gate、Deterministic execution、Recovery | 规范性设计：完整干净来源、source_locked、原preview/单次prepare/invoke及目标保留/验证 |
| [私有发布合同](../../../../../.agents/skills/release-guru-trellis-version/references/contract.md) Complete Source Before Actual Adoption、Whole Preparation Completion、Stage2 | 规范性设计：实际delivered后才能采用，每批完整质量链，后置责任不遗漏 |
| [MIGRATION-794](../../../../../trellis/presets/guru-team/MIGRATION-794.md) §1/4/5 | 规范性设计：提交前必要整合、提交后一次独立完整Review、匹配provider与完整采用 |

“来源”指已交付的完整干净commit；“采用”指当前Task checkout的实际安装及native可用性，临时分发样本不代替它。来源设计的唯一处置由本批design第3节承担。

## 2. 整体与本批目标、非目标

整体仍准备extension `0.7.0-guru.9`，CLI/Core `0.7.0-castbox.6`，后继由发布owner发布tag `v0.7.0-guru.9`，前驱为 `v0.7.0-guru.8`。仓库为castbox/guru-trellis，来源Issue #808，reference_only。

本批独立目标是通过原tools，将当前Task checkout的完整受管内容正式收敛到已交付Sync修复来源，证明目标resolver、installed/native入口及保留合同，并将全部实际安装after经自身完整质量链交付main。

不修改canonical机制、公共API、Fork或source lock；不新增测试框架、ledger、状态说明提交或历史转换。不覆盖旧Delivery正文/失败事实，不用普通apply或手抄managed资产。不更新primary/eafc；它们留给Stage2。不执行tag/Release、关闭Issue、生产部署、业务仓升级、累计完整矩阵或无关清理。

## 3. 本批起点、前序结果、依赖与剩余责任

历史四个Delivery均由公共Task facts确认delivered：PR839/`647df4de`、PR840/`997a57be`、PR842/`74f361da`、PR844/`d3b9196c5ca30c11e857fab5a912ab9aee6ac232`。PR844的reviewed head为`3f7099b9db78700d03a29b2c825e84280f5b6821`，是本批待取得的完整干净provider。其CI三平台通过；来源本身已完成独立审核与交付，不等于实际采用。

当前checkout的installed extension虽为.9，source仍为`ce25043d33e487def1043b4a9fee6cb180844480`，installed Sync与canonical不同。原Completion已正式返回additional_delivery_required/current_sync_runtime_adoption_unimplemented，原Creation已建立本批；没有重开历史切片。

前置：实际来源commit可读且干净、其自己lock与已有Fork/CLI/Core build匹配、目标唯一且无重叠未完事务。本批完整采用后，由原Completion重审全部准备业务；Closure no_mutation、acceptance-finish Architecture、Finish/精确Cleanup仍各归原owner。Stage2另冻fresh main并完成全部候选gate、tag/smoke/Release、两个本地目标和最终关闭，不由本批预先证明。

## 4. 本批调用方、场景与流程

| 场景 | 调用方、前置与动作 | 可观察结果 |
| --- | --- | --- |
| A-SC-01 来源与目标核实 | 原tools owner消费实际PR844 result和干净H，读取源lock、匹配build、目标及unfinished operation | 唯一source/target与source_locked输入明确；不以版本相同忽略来源 |
| A-SC-02 实际采用 | 本批已Activation，原owner审preview、单次prepare后的冻结plan、AGENTS/workflow/platform/managed决策，再invoke | 原installer生成完整.9安装与provenance，CLI仍.6，unverified为空 |
| A-SC-03 目标验证与保留 | 原owner及工程checker读实际目标resolver、installed/native、完整映射、mode、sidecar/preservation | Sync新runtime实际可达；Task/session/用户配置、peer及common指针未被工具更新更改 |
| A-SC-04 普通恢复 | 原事务输出丢失、partial或stale，原owner读实际完成/待办及相同source/plan/ref | 同操作合法resume/rollback；不重复prepare或改checkpoint/manifest造成功 |
| A-SC-05 质量与交付 | 采用和必要知识整合完成后，原TaskCommit→constructor/begin_check→新独立完整Review→readiness/Publication/Merge | 全部after进入本批完整B..H，中文Refs-only PR，未审前不push/建PR |

## 5. 完整行为、条件与约束

**A-R-01（AC01/04；SC01）**：只用实际已delivered H的完整干净来源；读取该来源自己的lock及匹配CLI/Core包字节身份和maintenance API。明确当前Task checkout；shared common-dir不扩大目标。重叠旧事务先由原owner处理，不换源接续。

**A-R-02（AC04；SC02）**：原preview只读；AI审查实际public tools/workflow、全部Guru managed差异及平台。AGENTS采用原custom能力和真实snapshot/content，原renderer维护Guru block；workflow用canonical完整内容、guru-team、真实immutable custom provider/ownership。只有原prepare一次冻结后，原invoke可写。installer生成manifest，不手工改hash或provenance。

**A-R-03（AC04；SC03）**：完整package/platform/workflow/spec/overlay、CLI/source lock及provenance一致；目标自己的resolver、installed validator和native continuation可用。核Shared/Claude/Cursor集合（Codex公共根为Shared）、ownership、mode/executable、drift及无未处理.new/.bak/bytecode。目标当前合法Task/Delivery继续原owner，不以源runtime或fixture代替。

**A-R-04（AC04；SC02/03/04）**：工具操作保持Task/archive/workspace/session/public/private control、用户内容、peer工具和common/peer pointers；维护只更新目标checkout-local runtime pointer。未知managed编辑明确preserve/replace，上游trellis归属和私有发布发现副本保留。恢复只沿原source/plan/ref，保后续业务改动，不转换历史Task或reset Git。

**A-R-05（AC03/05/06；SC05）**：必要当前知识差额由原RDT/Architecture处理；无新语义差额不写空贡献或README发布状态。全部安装after、规划及必要文档经原TaskCommit与完整独立提交后Review，check/full_review均真实适用才进入publication eligibility/readiness。中文PR仅Refs #808；Merge不关闭来源，不表示Task完成。

## 6. 本批验收、验证方式与未决项

| 验收 | 要求/入口与输入 | 预期观察与边界 |
| --- | --- | --- |
| A-AC-01 | R01/02；实际PR844 facts、干净源/lock/build、原preview/prepare/invoke | tools_upgraded，正式source_locked且unverified为空，目标.9/.6和真实clean来源正确 |
| A-AC-02 | R03；目标resolver、installed validator、native continuation及完整managed映射/lock/workflow | Sync实际等于来源；完整平台、字节/安装mode、ownership/drift成立，无sidecar；不能只抽样 |
| A-AC-03 | R04；原public postvalidation与preservation观察、目标Task/selection/native读回 | 原业务/session/用户/peer/common未变，正确进入本批下一owner；工具变更不迁移历史 |
| A-AC-04 | R05；实际知识after、TaskCommit、完整B..H独立Review及原交付链 | 本slice完整Refs-only交付；准备Completion、终态和Stage2责任保持 |

当前需求和技术选择没有待用户决定项。若实际必要依赖缺失，停在原owner并保具体失败；不能重标pass。验证方法由design/implement展开，不新增文本自证测试或扩大矩阵。

## 7. Canonical 引用与本轮差额

- [R794/R649](../../../../../docs/requirements/current/task-delivery-lifecycle.md#r794合并审核真实消费者与迁移)、配对[设计](../../../../../docs/design/current/task-delivery-lifecycle.md#d794原-owner-的单次提交后审核)与[测试](../../../../../docs/test/current/task-delivery-lifecycle.md)：本批执行既有完整采用和独立质量义务，不改变定义。
- [阶段成果/缺口](../../../../../docs/requirements/current/completion-closure.md#r649阶段成果维度与缺口分类)及配对design/test：source交付与实际采用分层，必要实现不能改称仅待证据。
- [Architecture ownership](../../../../../docs/architecture/03-domains/ownership.md) ARCH-DOM-010及[distribution](../../../../../docs/architecture/04-integrations/distribution.md) ARCH-INT-015：复用原tools及两阶段发布，不新增authority、contribution或ADR；实际影响由独立owner判断。
- [质量](../../../../../.trellis/spec/workflow/quality-guidelines.md#test-and-validation-value)与[原tools合同](../../../../../trellis/skills/guru-team/packages/guru-upgrade-tools/references/contract.md)：仍适用来源工程证据可采用，真实目标验证独立执行，证据充分后停止。

本轮差额仅真实受管采用及其本批规划。后序正式质量/交付由原公开结果承接；不回填正文自己的最终pass或HEAD。
