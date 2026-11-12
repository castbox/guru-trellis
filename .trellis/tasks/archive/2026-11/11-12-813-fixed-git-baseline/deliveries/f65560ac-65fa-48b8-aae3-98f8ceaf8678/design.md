# #813 D1 固定审核来源创建设计

## 1. 设计目标、需求承接与内容基线

承接本批 PRD 的 R1—R6、D1-S1—S4、AC1—AC5。固定开发基线 B 与 Planning H0 均为 `5c6a4591db7165ece045e6b0eb789c21d06d7d38`，来自本次原 Sync read 选定的 origin/main 对象。内容范围保留完整 B..最终H及实际 dirty 增量；PR 目标为 castbox/guru-trellis/main，不能用目标后来前进改写 B。

阶段适用 Architecture 为 `guru-trellis-architecture`，constitution 为 `guru-trellis-design-constitution-v1`，change contract 为 `guru-trellis-architecture-change-contract-v1`。原独立 candidate_assessment 已实际返回 architecture_impact / target_native，decision_refs 为 ADR-RUNTIME-LOCATION、ADR-028、ARCH-RUNTIME-LOCATION。该结果允许展开方案，不证明实现、安装或最终规划通过。

## 2. 当前系统、边界与目标差额

当前共享 `runtime/task_lifecycle/composition.py` 的 `prepare_creation_inputs` 对所有来源比较 local_branch_head 与 reviewed_base_head；`guru-create-task/runtime/invoke.py` 的恢复路径另行构造 CreationInputs。public shared/schema/profile/aggregate 尚不能表示 read 的独立来源。Sync及五阶段公开 transition 已有 git_object 与 synced 差异，无需修改上游或重造 transition。

本批在原输入和 composition 内表达来源并统一事实校验，迁移受控调用方、示例、测试及现行说明。原 acquisition、Task store、C4/C5、session、生成位置配置和声明出口继续各自负责原行为。没有前序 Delivery，没有新数据库、网络服务、锁、缓存、digest authority 或持久来源台账。

## 3. 来源设计处置（唯一）

| 来源及承诺 | 处置与具体落点 | 理由、影响及上游处置 |
| --- | --- | --- |
| Issue #813 要求1：固定 Git对象与delivery target分离 | retain：第4—6节独立 reviewed_base_source 与 selected_base_ref/delivery_target | 不把本地branch freshness套在固定对象；由本项直接落实 |
| Issue 要求2：exact source、common-dir、Task/generation/binding/acquisition | retain：第4、6节共享校验及原 acquisition/control | 只替换错误基线前置，不取消合法创建条件 |
| Issue 要求3：primary保持、真实mismatch字段恢复 | retain：第5、8节错误投影与原链断言 | 不移动primary，不以绕过错误代替修复 |
| Issue 要求4：旧同步来源与公共API边界 | retain：第5、7节新版输入和MIGRATION-813 | 直接演进受控consumer，旧资产验证和匹配旧操作恢复可追溯 |
| ADR-RUNTIME-LOCATION：来源variant贯通实际consumer，read不改名synced | retain：第5节薄projection | 不修改Sync或其实际同步语义，不制造新ADR |
| ADR-028与当前change contract：阶段适用、原owner整合和独立审核 | retain：第8、9节 | 原维护owner在工程验证后提交前整合；最终Review审核真实after |

## 4. 模块、职责与设计取舍

| 模块/owner | 本批责任 | 不承担的判断 |
| --- | --- | --- |
| `contracts/task-lifecycle/task-creation-input-3.0.schema.json` | 新版共享creation结构，明确审核来源与独立Task基线分支 | 不选择来源或业务scope |
| `packages/guru-create-task/schemas/public-delivery-task-creation-input-2.0.schema.json`、`public-input-2.0.schema.json` | 当前闭合profile和aggregate，引用新版共享合同 | 不接受旧字段猜测来源 |
| `runtime/task_lifecycle/composition.py` | 一个来源归一化/校验能力供record/create与check/recover复用；派生内部reviewed_base_head | 不执行AI Gate、选择route intent或新增持久状态 |
| `packages/guru-create-task/runtime/invoke.py` | 当前schema装配、调用共享校验、原官方创建和恢复、原diagnostic投影 | 不读取上游private结果，不改源Issue |
| 原Sync/Intake→Creation调用AI | 从实际ready.base薄投影来源，独立审查Task基线分支与target、精确副作用 | 不手填上游transition或把read视为sync |
| 原acquisition/C4/C5/session | 保持原注册、HEAD、ownership、Task/source和session条件 | 不充当固定对象freshness authority |

直接修改原模块，比增加创建前同步wrapper、重试、隐藏fallback或第二恢复层更接近首次偏离。新增结构只由Creation的当前输入消费者使用；无需全链新token或Task字段。所有改动的非生成代码文件应保持不超过3000行；若触及超限文件，先由原owner按职责机械拆分，不能绕过门禁。

## 5. 接口与数据

### 5.1 当前creation输入

新版保留 task_id、task_ref、source_profile、reviewed_source、accepted_scope_identity、delivery_target、selected_base_ref。移除当前输入的 reviewed_base_head，新增必填：

以下用本批实际已读对象示意结构。执行时必须从本轮原ready输出复制实际来源值。

```json
{"reviewed_base_source":{"kind":"git_object","selected_ref":"origin/main","commit":"5c6a4591db7165ece045e6b0eb789c21d06d7d38"}}
```

kind 的闭合集合为 git_object、synced_branch；selected_ref为非空来源定位，commit为完整40位commit OID。git_object.selected_ref不重新解析到当前ref，ref后续移动或退出不改变已采用对象。selected_base_ref继续是独立的Task基线branch，并供官方task.py --base-branch及非base/target资格检查；它不是read来源的selected_ref。delivery_target保持未来交付仓库/分支的原职责。

| 实际生产者字段 | Creation消费者字段 | 确定性projection |
| --- | --- | --- |
| `ready.transition.base.kind=git_object`、selected_ref、commit | reviewed_base_source | 选择这三项，丢弃Creation不消费的source precedence和identity digest |
| 实际synced base的selected_base、decision_head | reviewed_base_source | 固定kind=synced_branch；selected_ref使用原branch标准化，commit复制decision_head；不补造三方HEAD/provenance |
| 原owner审查的Task基线分支 | selected_base_ref | 原canonical_head_ref标准化；不得由当前工作分支猜测 |

git_object只要求固定对象可用及后续关系成立。synced_branch在新建前还要求来源branch与selected_base_ref标准化后相同、本地该branch HEAD等于commit。acquisition.decision_head始终必须等于source.commit。内部CreationInputs的reviewed_base_head从该commit派生，供现有创建/结果事实代码消费，不成为新公共输出或持久字段。

### 5.2 错误和输出

保留现有 created、refresh_review、blocked、invalid_task_state 及原DTO身份。对象不可用或不是commit、source/acquisition不符、错误仓库或真实源branch装配不符，用现有reason_code和可选diagnostic形状指明 reviewed_base_source.commit、reviewed_base_source.selected_ref、acquisition.decision_head 或 acquisition。同步基线真正前进保留原refresh_review→Sync。原error catalog/Interface如需新增reason声明，成套维护。

不改变已发布输出schema含义，不增加新的出口或强制诊断字段。字段级恢复由原创建owner重新读实际上游来源/正确acquisition；没有可靠来源时停止，不能只改hash或省略校验。

## 6. 状态、顺序、正常与失败流程

1. 原AI读取live Issue、ready与Git事实，选来源与acquisition，完成原semantic Gate及精确副作用边界。
2. record-task-plan验证当前新版结构，归一化来源及Task基线branch。固定对象在同repository检查commit类型/存在；同步来源加原新建freshness检查。两者都核commit/acquisition和原Task/generation/位置/唯一性。
3. create-task重复首副作用前客观检查，原acquisition创建或采用独立位置，官方task.py建Task，原C4/C5建立控制，原session绑定，发出created。
4. check/recover先通过同一新版结构和来源归一化，检查source.commit/acquisition实际起点及原result/head/source/control/session关系。它们不重跑precreation uniqueness，不重复创建Task、branch、worktree或C4/C5，不因结果已存在而再次分配身份。恢复保留原session分流：同Task/generation/ref保持；session_record_missing仅由原session owner重新attach；不同或无效session阻塞；context_key_unavailable保留explicit-task模式。同步来源也不把后来正常ref前进重新当作原结果缺失。
5. source、对象、acquisition或原control/session真实矛盾按原出口停止；普通装配修正或输出丢失走同owner恢复。没有额外状态机或授权存储。

## 7. 恢复、兼容、迁移与集成

新增shared3.0、Delivery profile2.0及aggregate2.0各自路径和$id；原shared2.0、旧profile及旧aggregate保持字节和历史语义，列为legacy验证资产。Interface仅选新当前合同，所有相关command schema bindings和examples选择当前新版。C6与package当前测试、delivery-chain调用方及命中benchmark更新同一输入，不留下当前旧字段reader。

`trellis/presets/guru-team/MIGRATION-813.md`说明完整matching cutover、每个旧consumer、转换来源与退出：旧成功创建/原丢失结果由完整固定旧provider读回原身份，不在current runtime加旧parser；旧待执行输入先经原Sync/Intake取得真实来源，再由当前Creation重审装配。不能从旧head或邻近字段猜kind。当前self-hosted Task已消费原created身份，继续原Task/Delivery，不重建。

原工具owner从完整源码更新本App目标，保留Task/session/config/peer，按原manifest/sidecar机制读回。普通apply被旧Task阻塞不能转成手抄dogfood。源码、受管安装与正式Release分别报告。切换只退出当前旧输入路径，不删除历史文件或改变已完成任务。

## 8. 验证设计

| 验证 | 层与入口 | 预期、独立断言和边界 |
| --- | --- | --- |
| V1 / AC1 | 真实Git临时仓库，原public Sync read→Discovery→Clarify→Wording→Readiness→Creation | main落后、primary保留staged/unstaged；不手造transition；观察固定对象Task、同generation/binding及primary refs/index/workfiles不变 |
| V2 / AC2 | V1同对象原check/recover，丢弃首个结果 | 原Task/branch/worktree数与身份不变；检查源commit/acquisition，不重复创建或unique扫描 |
| V3 / AC3 | 原public record/create/check/recover与模块级独立边界 | 正常错commit、非commit对象、source/ref和acquisition/common-dir不符均指具体字段；错误请求不创建；不手改artifact/hash/state |
| V4 / AC4 | 新输入同步来源、旧schema原样验证及交叉替代 | 当前sync合法创建和真实stale保持；不同branch拼写归一一致；旧字段代入当前拒绝，新字段代入旧拒绝；原旧操作恢复边界可执行 |
| V5 / AC5 | source/package/runtime定向suite，原tools owner更新本目标及至多一个代表性clean安装/reapply | 原target自身installed/native、声明平台、drift/mode/sidecar通过且Task/session保持；不声称完整多平台矩阵 |
| V6 / AC1、AC5 | 本Agent实际读取当前完整安装合同后，在V1代表样本执行语义owner与公开链 | 与确定性fixture分开记录实际入口、AI判断和创建终点；不发布产品Issue或向GitHub写入 |

复用原创建/acquisition/session与delivery-chain回归，新增case只覆盖上述独立缺口。长期回归验证可观察行为；临时诊断只回答实际剩余因果或入口疑问。静态schema/text检查不能代替链路，模块stub不能证明真实Agent或安装。没有额外红绿/回退次数配额；必要验收与受影响回归充分后停止追加实验。设施失败先区分依赖/fixture和产品分支，未触达行为不能当缺陷对照。

## 9. Canonical 引用、本轮差额与实际未决项

RDT runtime-location 的R718-07—11、D718-04/05/07、T718-04/05/07/08按PRD第7节承接。Architecture只修 ARCH-RUNTIME-LOCATION 的Git来源→Creation完整定义。task-owned贡献为 `docs/architecture/contributions/813-fixed-git-baseline.md`，完整拟写位于同名目录proposed；原ADR-RUNTIME-LOCATION与ADR-028继续适用，无新增ADR必要性。

共享RDT、Architecture由原维护owner在实现及工程验证后、TaskCommit前final_integration重读真实target，整合完整单元并读回；提交后独立Review审核真实before/after。Planning不改shared current/root/index。canonical spec旧Creation断言随公共输入实现替换，不能只改运行副本。

当前没有阻塞方案的未决用户选择。候选freshness仍须以最终design真实字节经Wording和独立final_plan验证；本方案不是实现完成或发布声明。
