# #648 约束与关键前提跨阶段语义审查：整体需求

## 1. 来源与术语

| 来源 | 角色与用途 |
| --- | --- |
| [castbox/guru-trellis #648](https://github.com/castbox/guru-trellis/issues/648) | Direct Source，exact_source；完整正文和 2026-10-21 补充全部为当前要求；live OPEN、updatedAt=2026-10-20T17:03:17Z、无评论 |
| [当前知识要求](../../../docs/requirements/current/knowledge-maintenance.md)、[设计](../../../docs/design/current/knowledge-maintenance.md)、[测试](../../../docs/test/current/knowledge-maintenance.md) | 现行完整 authority、原 owner、工程事实复用和最终整合合同 |
| [constitution](../../../docs/architecture/00-foundation/design-constitution.md)、[Architecture](../../../docs/architecture/README.md) | 当前规范性来源；按真实适用范围读取完整条件，不复制原则或建评分表 |
| [#637 整体需求](../archive/2026-10/10-20-637-candidate-review-reuse/prd.md)、[#638 整体需求](../archive/2026-10/10-20-638-shared-current-promotion/prd.md) | 已交付能力与历史来源；保留首次完整审核、差额复核和最终整合，不借旧 pass 证明本项效果 |

适用约束有真实来源、对象、完整条件、否定和例外。关键前提是影响可行性、职责、拒绝条件或阻塞依赖的事实假设。规范性约束、事实证据、接受设计和设计假设分开。A/B 是同一通用领域中的操作：A 不改变门禁保护的不变量；B 改变该不变量。样本使用去敏通用名称。

## 2. 背景与问题

来源记录了政策已加载，错误前提仍进入接受设计并被后续审核继承的历史失败。设计、代码和测试相互一致，不证明符合架构约束。历史失败不单独证明当前主线仍会漏检。

当前 main@cca65742bc485f8ab4e6399623b70dd5aebc25bd 已具备独立 Architecture、原始 authority 读取、测试价值审查、#637 候选复用及 #638 最终整合。本项先固定当前匹配版本，用真实 Agent 无答案提示采样，再补实际方法或验证覆盖缺口；不能仅加政策链接。

## 3. 目标与非目标

在现有 Author、Architecture、实施协调、Check、Branch Review 和 task-free owner 内落实适用约束、前提证据、正确测试预期及真实消费者影响。通过最早受影响的原 owner 修订、重审和恢复，完成本项全部验收与正式交付闭环。

不改业务政策、API 演进、业务代码或 Backend 现场；不新增阶段、profile、审批人、ledger、公共 DTO、schema、typed exit、runtime 状态或重复 CI。确需公共 API 变化时返回原范围与兼容决策。#649 独占阶段成果状态与完成证据组合验收，#651 独占 fresh reviewer 载体改进，本项不启动二者。本项效果证明不延期 #649。不发布版本，不扩完整 Release/多平台升级矩阵。

## 4. 真实调用方、场景与流程

| 场景 | 调用方、前置和触发 | 行为与可观察结果 |
| --- | --- | --- |
| S648-01 | Author 已加载政策，候选违反必要条件 | 指出原条款、候选落点及正常路径影响，返回原修订 owner |
| S648-02 | Architecture 面对已接受设计，原证据否定其关键前提 | 自主读取和检查继承前提；合法且有来源的例外通过 |
| S648-03 | 实施者发现批准方案内冲突，没有扩 scope | 暂停受影响操作，返回最小事实；协调者分流，修订/受影响审核匹配后恢复；无冲突工作按真实依赖继续 |
| S648-04 | Check/Review 面对设计、实现、测试共同错误预期 | 先从有效合同确定行为，再核测试入口/断言；检出共同错误，不弱化断言换全绿 |
| S648-05 | 状态、开关、迁移或执行分支变化影响未改消费者 | 检查真实前后状态与受影响调用方；无影响消费者不新增验证义务 |
| S648-06 | 原 reviewer 接续，新证据否定原前提但代码/测试不变 | 刷新受影响判断；合法无变化对照保留可核验事实；组合影响不能界定时完整评估 |
| S648-07 | task-free 目标或执行发现涉及 gate/admission/phase/switch/rollout | 识别不变量、最小触发迁移、不适用操作、缺证据阻断范围及 evidence owner/consumer；无依据跨能力依赖停止受影响写入，走原 evolution/scope route |
| S648-08 | 同域 A/B 都缺相同门禁证据 | A 成功并说明不适用理由；B 失败并说明保护的不变量；共同错误地限制 A 仍被检出 |

## 5. 行为要求

**R648-01 / S01：Author 约束落点。** 读取本次适用约束的完整条件、否定、例外、对象和来源，在实际设计及唯一来源设计处置说明具体落点。引用存在、retain 声明或原则复述不证明遵守；不新增逐条约束账本或复制基线全文。

**R648-02 / S02：原始证据与独立审查。** Architecture 区分规范性约束、事实、接受设计和假设。对影响方案可行性、职责、拒绝条件或依赖的前提读取原证据；前序 ADR、计划批准、知识晋升和实现/测试一致不豁免。合法例外按真实来源、范围及修订依据判断，不设无条件文档优先级。沿现有 before_authority 比较，拟改 baseline/ADR/测试预期不能自证符合原约束；真实修订由原 owner 取得有效来源后处理。独立审核隔离通过叙述，同时取得必要原约束/事实；缺事实保留不确定性并走原 incomplete/blocked。

**R648-03 / S03：实施停点、分流和恢复。** 发现批准方案违反约束、关键前提不成立或不能满足承诺，即使未扩 scope 也暂停受影响操作，返回条款来源、实际候选落点及影响这些最小事实。实施者不自行改需求、基线或断言。需求/约束仍有效而方案有误，回 Author/Architecture 修方案、保持 accepted scope；需求承诺/规范来源/例外 authority 自身冲突或确需改范围，回 Clarify，Architecture 提供具体冲突事实，不成为全部来源处理的新前置；规划有效而实现/断言偏离，回 implementation/Check。完成受影响规划和审核，冲突解决且候选/判断重新匹配后恢复；脚本通过或旧批准不足以恢复。无冲突工作按真实依赖继续。不新增 profile/exit/持久冲突记录。

**R648-04 / S04..05：合同先于测试。** Check/Branch Review 先依据适用权威确定应观察行为，再核实现、测试入口和断言。状态/开关/迁移/执行分支变化时检查实际前后状态与未改消费者，不机械生成全状态矩阵。具体有证据的职责违规是合同缺陷，不以已发生生产功能故障为前提。

**R648-05 / S02、S07..08：必要依赖和门禁适用性。** 区分有效约束要求的依赖与机制自行引入的无依据限制。后者回原机制/Architecture，不包装为外部证据待补。task-free owner 识别保护不变量、最小触发迁移、不适用 operation、缺证据实际阻断范围和真实 evidence owner/consumer；跨能力无依据前置导致停止受影响 target write，走原 evolution/scope route，不扩大编辑。A 不改变不变量，缺同证据仍成功；B 改变不变量，缺证据失败。设计/实现/测试一致地错误限制 A 时仍须检错并回原机制/Architecture 或 Check。

**R648-06 / S06：前提变化与复用。** 保留 #637 审核和工程事实复用。新证据否定原结论前提即刷新受影响判断，不以代码/测试未变免审；其余覆盖按现有适用性承接。组合影响无法界定时完整评估，不因阶段/reviewer 变化无条件重跑，不跨读或重建退休私有状态。

**R648-07 / 全部：当前真实行为验收。** 变更前冻结当前主线/匹配安装，去敏样本保留原失效关系。真实 Agent 无答案提示读取文件、自主判断、编写结果并调用原 wrapper；期待表不进入其上下文。对本轮改变方法用相同或严格等价输入复核，逐次审核条款、因果、预期及路由；两边均检错属已有能力，不记新增收益。保留失败、修复和边界。Author 落点、实施停点/分流/恢复、Check/Review 对共同错误预期/未改消费者检错及 A/B 全在本项执行；单点 Architecture 出口、读取顺序、关键词、结构或绿命令均不能单独证明效果。

## 6. 约束与依赖

开发基线为上述固定 main，交付目标 castbox/guru-trellis:main；TaskId=648-constraint-premise-review、generation=0。#637/#638/#635 已 CLOSED，#635 PR652/653 已 MERGED 且可达该 main。保留 candidate Check → final_integration → 实际候选重绑 → final Check/committed Review，不重建阶段或晋升机制。

Direct Source 完整选择由原 Clarify 输出承接；最终来源设计处置仅在所选 Delivery design。公共 Skill/profile/exit/schema/runtime 不变。Markdown 作语义判断，脚本只执行/记录/校验事实。honest-but-fallible 正常路径，不扩恶意伪造、故意绕过、竞态压力、锁或 fault injection。局部依赖缺口仅阻塞其依赖工作。

canonical 为长期源；dogfood、.agents、.codex 及声明平台按匹配受管机制同步。最多一个代表 clean，执行命中 package/runtime/source-installed/projection/apply/reapply/drift/modes/sidecar 检查，逐项处理 .new/.bak。已有 legacy 资产导致的全量 apply 边界如实报告，不迁移历史来伪造成功。源码分发不等于业务安装采用。授权只留当前对话。

## 7. 可观察验收与验证方式

| 验收 | 对应要求 | 入口、输入与必须观察 |
| --- | --- | --- |
| AC648-01 | R01..07 | 固定当前匹配主线，原 owner 无答案提示真实 Agent 错误/合法对照，区分已有能力和缺口 |
| AC648-02 | R01..06 | 原 Markdown 方法/示例仅补实际缺口；workflow 只编排及有歧义重入，不复制 step-local 判断 |
| AC648-03 | R01..04、R07 | 原 Architecture/Check semantic_authoring 和跨阶段 native 入口；真实 Author 落点、实施停点/分流/恢复、Check/Review 检错及未改消费者 |
| AC648-04 | R05、R07 | task-free 真实 A/B：A 缺证据仍成功、B 缺同证据失败，并说明不适用理由/不变量；共同错误预期被检出 |
| AC648-05 | R06..07 | 同 reviewer 前提改变且代码/测试不变时刷新受影响判断；合法无变化对照保留事实；旧新等价输入，保留失败和限制 |
| AC648-06 | R02、R06 | 首次完整、差额、candidate/final Check、committed Review 分工及原 wrapper 保持，不跨读/重建退休 private state |
| AC648-07 | 全部 | 定向 package/runtime、source/installed、声明平台、apply/reapply/drift/modes，零未处置 .new/.bak；最多一个 clean，不冒充 Release 矩阵 |
| AC648-08 | 全部 | 原 RDT/Architecture 同步；源码与 Agent 行为分开报告，不把业务安装采用记通过 |

全部验收当前待执行。最终还要求 satisfying PR 全 MERGED 且可达 live main、真实 semantic Check/独立 Review、Issue CLOSED/completed，以及原 Closure/Finish/Cleanup 闭环。单次 Delivery 合并不替代整体完成。

## 8. 实际未决项

没有待用户决定的产品/范围问题。当前匹配版本是否漏检、具体方法缺口、等价样本与原入口最小扩充交本 Delivery Author/Architecture 研究；未执行前不宣称通过或新增收益。公共 API 确需变化时停在原范围/兼容决策；完整 Release 矩阵、业务采用及后继 Issue 是明确边界。
