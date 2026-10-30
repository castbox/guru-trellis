# D1 架构机制审核公共流程需求

## 1. 整体来源与术语

本批公共 scope_ref 选择根 [整体 PRD](../../prd.md) R1至R8、AC1至AC6，全量交付。accepted_scope 为该文件的实际 AuthorityRef；DeliveryKey 为 `2a0bdf40-feb7-4d21-b232-a9071b986820`，planning_root 为 `deliveries/2a0bdf40-feb7-4d21-b232-a9071b986820`。机制、RDT、Task 与 Delivery 的含义沿整体 PRD 第1节。

| 来源 | 章节与角色 | 本批用途 |
| --- | --- | --- |
| 整体 PRD | 第1至8节；要求 | 本批完整行为和边界 |
| [研究 proposal](https://github.com/castbox/ai-chat-roleplay-backend/blob/b84d26a5c7e7f0481b742b716aece7b802174e39/docs/research/2026-10-30-architecture-baseline-review/proposal.md) | 第2至9节；约定设计约束 | 机制审核、举证、复用、存量与验证方法 |
| [研究 evidence](https://github.com/castbox/ai-chat-roleplay-backend/blob/b84d26a5c7e7f0481b742b716aece7b802174e39/docs/research/2026-10-30-architecture-baseline-review/evidence.md) | E01至E12；advisory/历史事实 | 去敏案例来源，不证明原审核过程或训练成因 |
| [宪法](../../../../../docs/architecture/00-foundation/design-constitution.md)与[change contract](../../../../../docs/architecture/06-governance/change-contract.md) | 完整五原则与原晋升生命周期；当前约束 | 实际架构取舍与知识写入责任 |

本批 design 第3节是来源设计处置的唯一矩阵；本 PRD 不另维护处置结论。

## 2. 整体与本批目标、非目标

当前公共规则已有正常场景、保护必要性和旧实现非先例约束，但对无 diff 复用、保护提出方举证和错误决策存量的承接仍不充分。防御与安全偏好是重点纠偏的行为假设，不能被个案确认为训练层面的因果。

D1 在原 owners 中修订可复用方法及必要调用入口，同批完成分发、当前测试和真实 Agent 行为对照。审核针对本次采用的机制，既防止无依据保护进入基线，也保持真实权限、保密和业务不变量。

本批沿用整体非目标：不改后端安装、业务行为、密钥或生产资源；不引入新阶段、审批链、永久台账、原则排名、最短代码目标、固定六步及无 consumer 公共字段。公共 API/DTO 若发现真实变化需求，先回原设计 owner 说明 consumer，不由脚本补字段。

## 3. 本批起点、前序结果、依赖与剩余责任

这是首个 Delivery，没有前序已交付结果。开发起点为 Guru `main@2f70796103406683a2f63adfb6b54d247a7433a5`；当前只有 Task/Delivery 与需求编写，尚无流程实施或行为验证结果。

依赖现有 Architecture/Protection/current-knowledge owners、preset 分发和 eval/真实 Agent 入口。D1 选择全量范围，不预留后继 Delivery 作为当前验收的替代。Task Completion 还须检查所有本批验收和真实外部交付事实；本地完成不能证明 push、PR、合并、安装采用或发布完成。

## 4. 本批调用方、场景与流程

| 场景 | 调用方、条件与触发 | 本批行为 | 观察 |
| --- | --- | --- | --- |
| D1-S1 | Author/reviewer 提保护，或模板要求签名、锁、队列、重试、台账 | 明确对象、要求、现有缺口、具体补齐与代价；依据不足先修订或调查 | 不因技术缺失独立成立 finding；真实保护有依据则保留 |
| D1-S2 | 新入口复用旧机制，旧实现无 diff | 当前适用性判断覆盖职责/authority/协调/失败/生命周期约束；原论证覆盖时简短承接 | 不免审，也不重审所有 helper 或无变化工程命令 |
| D1-S3 | 新方案正在质疑旧技术决策 | 保持真实合同，比较移除、缩小、替换、保留的后果；实际行为、性能或存量范围存在证据缺口时，追踪该决策的实际采用者 | 不用受审技术规则自证；不把旧保护缺证直接解释为删除许可 |
| D1-S4 | 修订决策拟晋升或任务拟完成 | 判断同状态共存、独立可迁移、场景不同三类存量 | 真实适配、分期承接或范围保留明确；Task 内义务不因拆 Delivery 消失 |
| D1-S5 | 源规则已实施并准备验证 | 原 preset 投影与机械检查；相同事实下原/新方法真实执行 | 具体机制取舍、真实输出与证据边界可核对 |

流程仍由原 Author → 独立 Architecture → Wording/最终 Architecture/Approval → 实施/Check/晋升/Review → 原交付与 Completion 承接。本批不增加阶段。

## 5. 完整行为、条件与约束

1. 本批审核范围覆盖新增、修改、复用、扩大采用及直接消费者。普通 helper、无关依赖与无因果历史债务不自动扩张范围；同一被纠正决策的旧采用者必须纳入影响分析。
2. 新增或强化保护的提出方包括 reviewer 与模板。真实约束、缺口、补齐关系、正常请求影响、协调/状态/依赖及运维代价共同支撑选择。理论风险、惯例、已有代码、历史通过和“更安全”不能独立支撑。功能失败不是职责违规成立的前置；真实权限或保密要求不以事故发生为前置。
3. 完整宪法为取舍依据，不将某条提升排名。判断必要行为、职责范围、整体代价、可行方案与风险匹配证据，不要求全局最优或固定逐项产物。避免无 consumer 的包装、抽象、转换、配置与未来预留；替代不得把负担转移为另一台账或人工协调。
4. 优先从适用 RDT/Architecture 完整单元取得行为、职责、能力和取舍。文档足够不重复查代码；实际行为、性能、该机制全部受影响消费者或文档冲突存在证据缺口时定向取证。找到依据后仍独立判断必要性，不只解释设计如何工作。
5. 旧技术规则本身受审时允许形成不采用它的候选，保留真实外部合同。沿原受审变更合同实施，再按实际候选与原阶段晋升；不先改 CURRENT 自证，也不要求提前晋升才实施候选。
6. 新保护缺依据时补证/修订/撤回，不升级为测试和交付阻塞。旧保护缺证时只暂停依赖该结论的采用或晋升，不直接删除、不把缺证视为复用通过、不阻断无关工作。已论证范围中的同类消费者简短承接。
7. 共存破坏同一约束、产生不兼容读写或使纠正失效时，承接必要旧消费者适配与退出。独立存量可分期保留，但须说明共存约束、剩余采用者、保留依据、owner、具体后继交付或可观察触发条件与退出证据；仅“下次再改”、owner 或链接不算已安排。不同场景仍有充分依据的明确范围后保留。
8. 分开报告新决策生效、新需求交付、旧实现迁完和环境切换。Task scope 内迁移仍是整体责任；范围外且有共存依据的存量不自动阻断本 Task。真实支持窗口退出且无消费者后才删除旧 helper、配置、key 或兼容路径；不为迁移预建无依据双轨框架。
9. 原 owner、公共 typed exits、现有安全/权限与诚实协作边界保持。规则用正常受管分发，不 patch 安装缓存冒充源修复。知识同步经原隔离贡献、候选检查和 final_integration；历史正文不批量改写。
10. 验证同时覆盖误加保护与必要保护、错误继承与正常复用、局部新交付与存量义务。真实 Agent 使用同事实、可比上下文和实际规则；预期答案与另一侧轨迹不进入受测输入。机械通过、代码量、删 key 数及更少 finding 不单独证明改善。

## 6. 本批验收、验证方式与未决项

| 验收 | 场景/要求 | 输入与原入口 | 预期观察 |
| --- | --- | --- | --- |
| D1-AC1 | D1-S1/S3；R2/R3/R4/R5 | 普通游标、已有可信哈希记录及 reviewer 签名要求；另给真实保密载荷 | 拒绝无缺口新保护，保持绑定/归属校验；保密要求支持必要机制，不以无事故否定 |
| D1-AC2 | D1-S1；R2/R3/R8 | 配置稳定的独立账号路径与真正共享库存对照，附首次竞争失败及后续重试 | 分辨协调作用域；保留必要全局不变量；重试恢复不掩盖首次可用性缺口 |
| D1-AC3 | D1-S2/S3；R1/R4/R5 | 无 diff 旧加密复用、已论证同类消费者、旧 AES 技术条款与不完整删除证据 | 实际判断当前适用性；正当复用简短；可审替代但不擅删、不全局停工 |
| D1-AC4 | D1-S4；R6/R7 | 同状态新旧 writer、独立可迁移旧入口、不同场景、Task 内后继切片 | 必要同步适配；分期有可执行条件；场景保留；Task 内迁移仍未完成 |
| D1-AC5 | D1-S5；R8 | canonical、必要调用引用、dogfood 与完整安装/reapply 检查 | 无漂移与未处理 sidecar；只宣称实际机械范围 |
| D1-AC6 | 全场景；R8 | 上述四组可比旧/新真实 Agent 执行及语义复核 | 输出先于预期比对；记录真实输入、规则版本、条件、失败与未知；两边都正确则认定已有能力 |

四组是本任务的有界行为验证，不成为公共业务任务的固定矩阵。分发与 Agent 行为分别报告，缺原方法证据不宣称改善幅度。当前需求没有阻塞未决项；实际验证尚未执行。

## 7. Canonical 引用与本轮差额

- [RDT knowledge requirements](../../../../../docs/requirements/current/knowledge-maintenance.md)：Architecture 维护边界及 R648 原证据职责；本轮补采用机制、保护举证与存量实现处置的行为。
- [RDT knowledge design](../../../../../docs/design/current/knowledge-maintenance.md)：D331/D648 的原 owner 与分发；本轮方法仍落在原公共合同，项目完整单元承接行为与追踪。
- [knowledge tests](../../../../../docs/test/current/knowledge-maintenance.md)：原策略与结果定位；本轮增加具体机制对照和独立证据边界。
- [Completion requirements](../../../../../docs/requirements/current/completion-closure.md)：整项范围责任；本轮对存量迁移被拆 Delivery 的场景补明确承接。
- [Architecture contract](../../../../../trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/references/contract.md)：原架构审查与晋升；本轮补机制适用性、旧规则受审和存量分析。
- [Protection contract](../../../../../trellis/skills/guru-team/packages/guru-qualify-root-cause/references/contract.md)、[current knowledge](../../../../../trellis/skills/guru-team/packages/guru-maintain-requirements-design-test-ssot/references/current-knowledge.md)：原保护准入和知识职责；本轮补提出方责任与纠错后的当前/存量表达。
- 设计宪法、change contract 的用途见第1节；无独立原则排名。适用测试与知识拟写由本批 design/implement 确定，本文不直接改共享 authority。
