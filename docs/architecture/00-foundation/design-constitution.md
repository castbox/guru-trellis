# Design Constitution

Authority identity：`guru-trellis-design-constitution-v1`；状态：`current`；适用范围：Guru Team Trellis extension repository。本文是五项设计原则正文与解释的唯一项目 authority；公共 Skill、schema、fixture、task artifact 与 `.trellis/spec` 只可引用 identity/short name，不得复制本文或把它转成机械评分表。

| Identity | Short name | Current principle |
| --- | --- | --- |
| `mature-practice-applicability` | 成熟实践与适用性 | 优先采用官方、成熟、可维护的扩展面与工程实践，但每次必须结合当前 task 的真实边界、风险和证据判断适用性；不因惯例本身制造无 consumer 的机制。 |
| `concept-semantic-completeness` | 概念与语义完整性 | 每个进入公共合同的概念必须有唯一 identity、owner、状态、边界、关系与生命周期；缺失适用语义时 fail closed，不以 optional 空字段或脚本默认值冒充判断。 |
| `cohesion-change-isolation` | 职责内聚与变化隔离 | 语义判断、确定性执行、项目 authority 与 task-local contribution 各归唯一 owner；跨边界只交换最小 typed projection，并行 task 不直接竞争 shared current。 |
| `minimum-necessary-complexity` | 最小必要复杂度 | 只实现当前已批准 Requirement 与 Acceptance 必需的最小充分能力；全部新增能力都须有当前、可追踪且可验证的必要性，不为假设中的未来需求预留。真实当前职责与兼容边界按本 authority 的解释保留；未来需求出现后通过新 requirement/task 演进。 |
| `debt-one-way-convergence` | 技术债务单向收敛 | 新能力优先 `target_native`；保留 legacy 时必须选择可审查的局部收敛路径、明确 owner/GAP/退出与删除条件，禁止新增第二 authority、扩大无退出双写或让旧路径重新成为默认。 |

使用这些原则时，Architecture semantic owner 只记录与当前 task 真实冲突、权衡、例外或不足相关的 identity 和 evidence。未命中的原则不创建空白 verdict；no-impact/current-conforming task 不创建 contribution 或 ADR。

## 最小必要复杂度的适用范围

新增字段或公共 DTO 属性、状态/转换/枚举值、API/typed exit/callback/plugin point/公共接口、配置/feature switch/策略入口、持久化/缓存/锁/双读写/compatibility layer、metadata/extensions/reserved 等通用扩展容器，以及 wrapper/抽象层/规则引擎/通用机制，都按同一原则审查。

每项候选须能够回答：当前 Requirement 是什么、直接 consumer 是谁、当前版本如何触发、当前 Acceptance 或验证证据是什么，以及删除该能力及其职责后是否仍满足全部当前适用合同。AI 按实际变化与证据判断；这些问题不要求逐字段持久化表、公共 DTO、checkpoint 或独立评分器。

“全部当前适用合同”包含当前功能、Architecture、职责隔离、可维护性、运行、兼容、迁移、安全及发布合同。必须有当前依据；通用最佳实践不能将未知未来需求纳入。删除判据涵盖候选能力及其职责：替代实现仍承担同一必要职责，不证明职责不必要；功能测试仍绿也不能单独证明全部合同满足。当前职责隔离或可维护性有依据的抽象可以成立。删除该能力和职责后仍满足全部适用合同的候选，不进入当前设计或实现。

“未来可能需要”“便于以后扩展”“保持灵活性”“避免将来修改”“一次设计到位”“通用最佳实践”，或“增加后成本很高但当前没有 consumer/验收”，本身均不是当前 Requirement、architecture decision 或 implementation scope 的充分理由。提前预留会扩大当前合同、状态空间和测试矩阵，并可能让未经真实场景检验的抽象成为未来设计的错误锚点。未来需求出现时通过新的 requirement/task 演进；潜在 future candidate 只能留为 non-goal、unknown、limitation 或 follow-up candidate，不能因此产生当前字段、状态、接口、配置、Schema 或实现分支。

## 当前必要可演进性

本原则保留有当前证据与直接 consumer 的真实边界：已发布多版本客户端或外部 consumer 的兼容；当前数据迁移、发布、回滚或渐进切换；当前 secret、权限、隐私或合规；当前支持的平台/运行环境/官方 Trellis 扩展合同；已批准且正在分阶段交付的 Requirement/Initiative。兼容/迁移机制必须说明 owner、适用边界、当前依赖、验证方式、退出及删除条件。未知未来需求不能包装成 compatibility；真实兼容与历史保留的适用判断由原 owner 完成，不能借本原则顺带删除既有机制。

## Requirement 与 mechanism 的修订分流

已经写入或批准的 Requirement 不单独证明当前必要性。当前需求有真实必要性而机制多余时，原 qualification 和设计/实现 owner 去掉或替换多余机制，保留 accepted scope，重审受影响候选。Requirement 本身只靠未知未来依据时，Architecture semantic owner 形成具体冲突，经现有需求澄清/Planning 修订取得新的 current authority 后重审；执行者不能直接删 scope，也不能以既有批准覆盖冲突或继续声明 pass。缺必要性证据或存在真实选择时走已有澄清/blocked，不能仅凭未来相关关键词拒绝。

Planning、Phase 2 与完整 Branch Review 各自读取当前 authority、适用结论及当前候选；finding 仍须经过该阶段正常场景与 mechanism qualification。只消费现有 Architecture conflict、qualification、scope-change/revision 路径，不新建审批链、第二 requirement authority 或自动 Issue mutation；scope 修订与副作用沿原对话边界。

## 六类正常场景与语义示例

下面是可审核事实和预期语义结论，非关键词分类器、数量门槛或逐能力评分表。它们不构成新业务需求，具体阶段沿当时 current Interface 的唯一 consumer 返回。

| Case | 当前事实与对照 | 语义结论与原路径 |
| --- | --- | --- |
| C466-01 必要能力 | 当前 Requirement 要求 caller 根据一次调用的 typed exit 执行下一步；具名 consumer 已读取 exit，受支持入口实际触发，Acceptance 验证对应路由。删除 exit 及该职责使 caller 无法接续。对照候选：同一 DTO 新增从未被 caller 读取的备用属性，仅说明未来会用。 | 当前必要 exit 可成立；备用属性不进入当前候选。机制修订保留原接续需求。 |
| C466-02 未来预留 | 当前任务只交付一个已确定策略；草案同时预留 unused 字段/枚举状态、plugin callback/API、feature switch 与 extensions 容器，没有当前触发、caller 或 Acceptance，仅称以后扩展方便。对照：当前 caller 必须选择两个已要求策略，现有场景可触发并验证。 | 前者返回设计/实现 remove/replace，不追加当前义务；后者按真实当前合同审查。不得以“配置项”这个类别一律拒绝。 |
| C466-03 真实兼容/迁移 | 已发布 consumer 仍读旧格式，当前 rollout 在迁移完成前必须提供旧读路径；有迁移 owner、版本/数据边界、当前依赖、双版本与回滚验证、依赖退出后删除旧路径的条件。对照：没有旧 consumer 的新接口预留 v2 adapter，无法说明迁移对象或退出条件。 | 前者可保留受界定的当前兼容；后者不能因命名为 compatibility 获得必要性。证据不完整时先回既有 owner 补齐，不擅删既有 support。 |
| C466-04 边界中的 future candidate | 当前无 plugin consumer，只在 limitation/follow-up candidate 说明以后出现真实第三方场景再另开 requirement/task；当前 Schema、API、配置和实现均无预留。对照：从这段备注自动生成 reserved 字段和空分支。 | 边界记录可成立，不产生实现 obligation；自动生成的机制返回修订。 |
| C466-05 被投机内容污染的 Requirement | 已批准 PRD 写入“为未知未来 provider 预留多个状态”，当前 provider/触发/consumer/Acceptance 均不存在；功能实现全绿。对照：已批准分阶段 Initiative 的当前阶段确实需要已确定的迁移状态，具名后继阶段已消费且有当前 Acceptance。 | 前者产生 requirement-authority 冲突，经 Architecture -> Planning/澄清修订，取得新 current 后重审，不能执行者删 scope 或继续 pass；后者依据当前阶段合同审查，批准本身不是唯一证据。 |
| C466-06 必要抽象与未来抽象 | 当前合同要求语义 judgment 与 deterministic execution 由不同 owner 承担，两个已存在 caller 共用同一职责；职责隔离与维护边界已有依据。删除整个抽象及职责虽可能使一组功能测试仍绿，却违反当前 owner 合同；以更薄实现替换仍须承担职责。对照：无第二 caller 的新规则引擎只预测未知未来规则。 | 有当前职责依据的抽象可成立，替代实现接受独立机制审查；未来引擎返回 remove/replace。功能绿测不能代替全合同判断。 |
