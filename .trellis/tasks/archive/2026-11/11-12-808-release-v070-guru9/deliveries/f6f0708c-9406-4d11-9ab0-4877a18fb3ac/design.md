# Sync 普通输入兼容设计

## 1. 设计目标、需求承接与内容基线

承接本批 [PRD](prd.md) G2-R-01 至06及 G2-AC-01 至04，恢复发布候选完整审核发现的普通入口兼容缺陷。整体 accepted scope 与本批 AC-01/03/05/06 选择保持。

原 public constructor 已实际返回 development B `139626ac1e860ee67c03196ce664c4a2a7145152`。来源为本次明确选择的 gen2 起点 main commit；Planning H0 同为该 commit，PR 目标为 main。B 是内容比较起点，H0 不是最终实现候选。

独立 Architecture candidate_assessment 实际返回 baseline_current / no_architecture_impact，绑定本 key。适用 authority 为 B 的 `guru-trellis-architecture`、`guru-trellis-design-constitution-v1` 及其 change contract。其判断是原 Sync owner 内恢复原边界，不需要 contribution、ADR 或共享基线修改；final_plan 和 committed after 仍由原独立 owner 判断。

## 2. 当前系统、边界与目标差额

gen0 的私有发布链、版本来源和真实 tools 采用已交付，gen1 的 verifier 修复已交付。当前 main 的 Sync `runtime/invoke.py` 在解析普通 mode/route 前无条件校验 deterministic-sync-3.0 envelope 和 current-input-3.0 aggregate。原普通无版本 envelope 因此在 schema_version 被拒绝；原默认 source_exit 也受 aggregate 必填收紧。

目标仅将这两项新增校验移入原 `return_identity` 分支，保留紧随其后的 dedicated input 校验。普通输入继续由原字段处理及 Git executor/validator 判断。改变 canonical runtime 和有独立价值的回归；不改变 Interface、schema、selector、输出、共享 dispatcher、Git 算法或发布版本。当前安装仍是此前已交付来源，不能宣称包含本修复。

## 3. 来源设计处置（唯一）

| 来源及承诺 | 处置与设计落点 | 理由、影响与上游处置 |
| --- | --- | --- |
| Sync contract：Qualification confirmation refresh，普通 bare/public_input envelope、默认与字段诊断 | retain；第4至6节，普通分支使用原字段处理 | 恢复原承诺，无 API 退役或迁移选择 |
| 同合同：return_identity 的封闭 current envelope 和 dedicated read input | retain；第4至6节，所有 aggregate/envelope/dedicated 校验留在该分支 | 普通兼容不能替结构化返回补身份或放宽条件 |
| MIGRATION-811 §2.1：新增 envelope 不得收紧普通调用 | retain；原普通路径不先经过该封闭校验 | 修复现实现偏差，不新增 compatibility parser |
| MIGRATION-819 公共选择器与消费者：current3 引用原普通/确认分支及专用 Issue 返回 | retain；current3 和所有专用 schema/consumer 不变 | 不恢复退休 selector，不引入版本检测或双 reader |
| 私有 release contract：Complete Source Before Actual Adoption | retain；本批完整来源交付，后继正式 tools 采用 | 避免把未交付或 dirty 来源当正式采用；implement §5拥有阶段责任 |
| MIGRATION-794 新正常链与完整采用 | retain；知识整合后 TaskCommit，再一次完整 committed Review及原发布链 | 没有新增 precommit 独立 Check/Review，也不提前 push |

## 4. 模块、职责与设计取舍

Sync `runtime/invoke.py` 独占输入分支判断和现有确定性执行。读取 JSON 后依原规则提取 public；携 return_identity 时执行现有三个层次校验，再进入原 read/sync 分支。没有该字段时直接进入原 mode/route/operation 处理。

`tests/test_contract.py` 复用公开 invoke skipped、synced、blocked、字段错误与 detached authority 覆盖，只补裸输入和默认的真实缺口。`test_read_baseline_chain.py` 与 Discovery `test_qualification_context_chain.py` 验证受影响的固定对象 read/结构化消费者。

选择原分支内移动校验，能直接恢复已承诺格式。给 fixture 补 schema_version 会掩盖缺陷；全局删校验会削弱结构化合同；新增 normalization/adapter 会复制原默认与维护责任。因此均不采用。没有新增业务 authority、持久状态或协调机制，原 root qualification 的同机制结论仍适用；normal/solution 不因阶段变化制造调用。

## 5. 接口与数据

公开 wrapper、scalar CLI、public_input envelope、bare object 与既有输出保持。普通 mode 为 workflow/standalone；route 省略仍为 repo_change；operation 省略仍为 sync；repo_root 省略仍为当前仓库；skipped 的 source_exit 省略仍为 start。原非法 mode/route/operation 的 field_path 和错误类型保持。

携 return_identity 时，transport schema_version 仍为1.0，schema 路径版本为3.0；不得混淆。当前 envelope/current aggregate 校验先执行，随后按 return_identity.profile 选择 existing_issue_intake 或原 qualification dedicated schema。字段、固定 commit、continuation 与 handoff_profile/consumer 均不变化。无新数据字段，因此没有 Task/Delivery 或数据库数据迁移。

## 6. 状态、顺序、正常与失败流程

1. 原 wrapper/dispatcher 校验安装与命令，读取 invocation，按现有规则提取 public。
2. 携 return_identity：执行当前封闭 envelope、aggregate、专用输入校验。正常缺字段/不匹配仍在原校验边界拒绝。普通输入不进入这些新增约束。
3. 原字段校验处理 mode、route。workflow/original_request 返回 skipped；standalone 选择该 route 仍报原错误。
4. repo_change 解析原 repo_root 与 operation。read 执行固定 Git-object 读取并产生 baseline_ready；sync 执行原 resolve→fetch/ff-only→check，产生 synced 或原 blocked。
5. 原输出 schema、分流和唯一 consumer 保持。没有新状态机、重试或异常吞并；无效普通参数不转换为 blocked，真实 Git/base/dirty 阻塞也不转换为成功。

## 7. 恢复、兼容、迁移与集成

这是既有支持分支的实现修复，不演进公共 shape 或发布资产，不需要新增 migration id。未执行的普通调用按原入口重试；结构化调用仍按 matching current provider。已有完成事实、旧失败 candidate 和历史证据保持。

canonical runtime 与实际安装不能手抄同步。本批先完成来源和一个必要临时安装的可分发验证；后继由 Completion 的 additional_delivery_required 经 Creation/Planning/Activation 从实际 delivered 的完整干净来源执行 source_locked tools。临时样本不证明真实采用。之后全 Task 终态及 fresh candidate Release 仍承担完整责任。

## 8. 验证设计

| 验证 | 要求/验收、边界及入口 | 独立观察与限制 |
| --- | --- | --- |
| G2-V-01 | R01/03/04，AC01；Sync test_contract 原公开 wrapper与真实临时 Git fixture | 三类普通 carrier/default 到达原 skipped/read/sync；错误 field_path、dirty/unresolved 阻塞保持。既有覆盖采用，裸/default 只补未覆盖语义 |
| G2-V-02 | R02/04，AC02；原 read_baseline_chain 与 qualification_context_chain | 固定对象/真实 producer 输出和 return_identity 消费保持；原结构化缺字段仍拒绝。fixture 不预填被测输出，不把局部测试称真实 Agent/远端业务 |
| G2-V-03 | R05，AC03；source validator及一个临时完整 preset 安装、声明平台投影与 installed validator | 受影响 runtime 实际按完整 source 分发；检查 managed bytes、CLI/lock、mode、provenance和sidecar。dirty/local 来源如实限定，不证明正式安装 |
| G2-V-04 | R05/06，AC04；原知识 after、TaskCommit和固定完整 committed Review | 实际范围完整、测试有效，来源无开放 finding 后才 readiness。原受管差额交后继实际采用 |

方法引用 `.trellis/spec/workflow/quality-guidelines.md` 的 Test And Validation Value。已有失败与代码分支解释原因，直接最小实现后执行必要回归；不强制额外 rollback/red-green。长期测试断言来自原兼容承诺；临时安装回答本来源是否完整分发。必要行为和受影响回归充分后停止追加实验，设施失败则重评复现方法或如实保留缺口。

## 9. Canonical 引用、本轮差额与实际未决项

PRD §7 的 REQ/DES/TST-811、issue-content 及原 Sync/MIGRATION 权威保持。Architecture 的 ownership/distribution 与 constitution 保原单 owner、最小复杂度和完整采用分层。本批不新增语义定义或架构机制；RDT owner 在真实工程结果后核当前完整单元是否需要差额，只维护真实变化，不能为了发布写状态或重复定义。

当前无待用户决定的需求或重大技术取舍。实现、实际安装、独立 committed Review与 Release 均尚未证明；这些分别由 implement 的步骤、Policy 和原 owners 承接。
