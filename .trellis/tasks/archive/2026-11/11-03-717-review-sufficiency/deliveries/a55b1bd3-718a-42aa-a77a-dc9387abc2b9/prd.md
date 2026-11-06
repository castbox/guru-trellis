# D1：审核充分性规则与消费者收敛

## 1. 整体来源与术语

整体 authority 为本 Task 根 `prd.md`，revision `sha256:06249bcffe09de0c8fb2ef701a8537b8358954c458ffd6fc8f889206235d40cb`；本批 scope_ref 选择 AC1、AC2、AC3、AC4、AC5。Direct Source 是 [Issue #717](https://github.com/castbox/guru-trellis/issues/717) 的完整当前正文。两者已读取；根 PRD 第3、5、6、7节拥有整体定义与约束。本批没有额外 advisory 来源。

planning_root 为 `deliveries/a55b1bd3-718a-42aa-a77a-dc9387abc2b9`。审核完成、对象通过、修复/验收完成分别采用根 PRD 的定义。provider 提供当前 Guru 规范和 Skill，target 是受审仓库；二者不能因相对路径而混用。

## 2. 整体与本批目标、非目标

现有完整范围、充分性和后继覆盖定义分散，共享方法与阶段合同互相依赖。本批完整交付共同审核充分性 SSOT、旧定义迁移、原 owner 执行接入、受管分发及真实 Agent 前后行为验证，使原 owner 在一次当前审查中按剩余覆盖推进并诚实结束。

整体非目标全部适用：不修业务 ORM；不改外部专业 Skill 或批量升级项目；不引入新 gate、充分性 Skill、台账、评分或 digest 链；不接管修复/Delivery 调度，不增加攻击/压力场景或完整发布矩阵。

## 3. 本批起点、前序结果、依赖与剩余责任

首次 D1，没有前序 Delivery。固定 source 是 `404c841e9ca917b4680831aa0becd2e26d72fa0c`。现有 `review-method.md`、候选覆盖合同、专业/测试规范及 native eval 能力是起点。#713 为相关工作，不自动阻塞；本批自行满足 Guru 侧原公开入口合同。外部专业标准继续按其实际来源消费，不声明外部独立调用已接入。

本批覆盖整体 AC1–AC5；不安排未来 Delivery 承担本项迁移或真实验证。源码、安装、真实行为、尚未验证的完整多平台/Release 边界必须分别表达。合并之后仍须由整体 Completion 审查本批实际证据，再由 Closure/Finish 收尾。

## 4. 本批调用方、场景与流程

| 场景 | 调用方、条件与动作 | 本批要求的结果 |
| --- | --- | --- |
| S1 | 原 Issue Clarify/Readiness/Wording、Planning Approval、独立审核、正式 Check/Review、Completion、Architecture、RDT 或安装验证 reviewer 接到自己的审查对象 | 读取共同规则及适用专业标准，从来源、入口、必要消费者形成并反查检查单元；原 profile 和出口保持 |
| S2 | 在当前范围发现多处缺陷或共享转换/状态/契约问题 | 按剩余覆盖继续，对真实同机制入口补查；完整保留 findings 的触发与影响，不按数量/篇幅早停 |
| S3 | 独立只读审核确认未修复 findings，或测试失败 | 失败作为证据；当前审查充分时完整报告并结束，不自行修复、等待修复或推进 Delivery |
| S4 | 已约定合法差异或正确对象已充分覆盖，且无新证据/影响 | 不制造问题、不固定轮数、不无因换 reviewer，能结束当前审查 |
| S5 | 必要来源、范围访问或执行证据缺失 | 报告已覆盖、剩余、具体阻塞与影响，按原前置停止/出口处理；部分完成不成为新公共出口 |
| S6 | 原流程发起后续候选审核 | 核完整增量、失效覆盖和受影响未改消费者；保留有效证据，影响无法界定时完成所需完整审查 |

共同循环仅是当前对象的范围、检查、发现/缺口判断、补查、结论。各 owner 的独立性、通过条件及修复/复审调度保持。

## 5. 完整行为、条件与约束

**D1-R1 共同定义与迁移。** 统一源定义覆盖形成、推进、同类补查、候选判断、结束、局限和后继覆盖承接。唯一源已有充分规则时直接引用；重复、冲突或缺失才迁移。迁出正文必须删除并改为引用，不能新增“本文件优先”并保留双份权威。专题检索、测试有效性、因果及专业正确性由原源定义。共享规范不依赖阶段私有 artifacts、recorder 或出口；共享方法只保留真实组合职责。

**D1-R2 固定消费者与适用特例。** 在固定 source 上盘点 Clarify、Readiness、Wording、Planning Approval、独立变更审核、Check、Branch Review、Delivery Review、Completion、Architecture、RDT 以及安装验证中实际承担审查的职责。每项明确实际对象、适用规则、读取入口及合法特例；不把写入前的一致性检查或每个 semantic gate 扩成代码审核。交付前核候选相对固定集合的变化及必要未改消费者，基线后无关新增不自动纳入。

**D1-R3 完整当前审查。** 不从实现/测试反推完整需求，不以逐文件读取、章节/维度齐全、命令/扫描、共识、问题数或零 finding 代替覆盖判断。分批可以，已确认 findings 不得丢失。候选需要证据、适用性和影响判断；排除候选只在争议或局限需要时报告，原记录义务保留。同根因归并不丢触发和影响。无新证据或影响且覆盖充分时停止；不要求全绿、修复完成、连续零 finding 或另派 reviewer。

**D1-R4 边界与后继。** 真实缺口阻碍充分性时说明部分完成或阻塞，原前置阻断继续有效。新候选审查完整增量和影响，并保留有效原覆盖；影响不明做所需完整审查，不只核修复点或从零重扫。共同规则不拥有修复—复审—Delivery 循环。公共 I/O、schema 和出口不变；真实破坏性变化须先进入显式迁移。

**D1-R5 provider/target 与专业证据。** Guru 从完整 provider 读取共同规则，按原专业 source/version 消费证据并单独读取 target authority。目标仓库无需因为共同方法而安装 Trellis；外部专业 Skill 的独立调用不隐含 `.trellis/` 前置。Guru 侧职责必须本批完成，外部接入只报告真实兼容边界。

**D1-R6 真实行为与分发。** 执行前由验收侧固定案例范围、已知问题、合法对照和必要证据缺口；不向 Agent 注入指定 findings、预填当前判断或入口外纠偏。复用既有 eval/观察，保留首次旧新实际结果与可比条件。Issue、代码、规划/设计均有代表，S1–S6 的行为均有观察。逐例判断遗漏、误报、早停和重复调查，不加通用召回阈值。原安装 owner 负责 canonical/dogfood/installed、声明平台和 reapply/drift；真实行为不能用机械绿测替代。

本批设计第3节是来源设计处置的唯一位置；本 PRD 不另建处置矩阵。

## 6. 本批验收、验证方式与未决项

| 验收 | 输入与入口 | 预期观察与证据边界 |
| --- | --- | --- |
| AC1 | 固定 source 和完整候选；Planning/设计迁移说明 | 每条共同规则唯一源；旧定义删除、阶段特例/专题 owner 和无环读取可逐项核对 |
| AC2 | 固定消费者的原调用入口和安装投影 | 全部有实际加载路径，代表入口按真实调用语义选择，保留原边界及出口 |
| AC3 | 验收方预先固定的 Issue、代码、规划/设计案例，走原生产入口 | 实际 Agent 调查、findings、完成/局限表述满足 S1–S6；不自行修复或等待下一 Delivery |
| AC4 | 同例旧新、可比入口/工具/模型，首次原始 trace/report | 逐例判断遗漏、误报、早停和重复调查，报告必要条件差异；不承诺任意对象全缺陷发现 |
| AC5 | 原受管同步、定向分发/加载/安装验证和 drift | canonical/dogfood/installed、声明平台一致，明确 sidecar 与未覆盖完整多平台/Release 矩阵 |

当前无产品未决项。具体迁移表和案例在方案中固定；预定执行不等于通过，缺口由原 owner 据依赖处理。

## 7. Canonical 引用与本轮差额

- `trellis/presets/guru-team/spec/workflow/workflow-contract.md#candidate-applicability-and-coverage`：候选承接与事实适用；迁移共同部分时保留工程事实/阶段绑定的唯一权威。
- `trellis/presets/guru-team/spec/workflow/quality-guidelines.md#specialist-review-standards` 与 `#test-and-validation-value`：专业及测试方法仍由原源拥有。
- `trellis/skills/guru-team/packages/guru-review-change/references/review-method.md`：当前组合职责和循环依赖；需要共同源取代阶段反向读取。
- `docs/architecture/README.md`、`00-foundation/design-constitution.md`、`06-governance/change-contract.md`：原 Markdown/脚本职责、唯一 owner、最小状态和阶段晋升约束。本批若改变当前架构定义，须经原独立评估和 final_integration 晋升；Planning 不写共享 authority。
- `docs/requirements/current/knowledge-maintenance.md` 的当前候选/覆盖与来源消费定义：本批在现有 RDT owner 下维护必要完整单元与测试关系，不新增长期列表系统。
