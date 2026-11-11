# D1：规划中的实际 PR 范围与前驱交付安排

## 1. 整体来源与术语

本批 TaskId 为 `delivery-target-preflight`，generation `0`，DeliveryId 为 `ab2f681d-68b8-4678-8f76-bb4dfad94c6b`；公共 planning_root 为 `deliveries/ab2f681d-68b8-4678-8f76-bb4dfad94c6b`。当前整体 accepted_scope 指向根 `prd.md` 的 `sha256:32e127d65966d64807c6bcbec0435ec932b0de475fbd42ba3d7ac19016c02e79`，本批选择 R1–R6。

实际读取整体 [PRD](../../prd.md) 全文，以及唯一来源 `/Users/devSC/Documents/JobProject/guru-validation-evidence/fizz-filter-controlled-2026-11-10/host/delivery-target-preflight-request.md` 全文。原 `source_selection=[]` 保留，原 producer locator 为 `draft:07939adebf332aeec2dc22a4b78d48ff84849ebdd44d3f20047e9e800791d86b`。request 的要求/约束/非目标/验收是 authority；历史123/177路径案例是回放事实，不是本批交付责任。外部 proposal 只是候选，冻结 behavior protocol 只是验证方法。

开发起点、固定内容审核 B..H 与计划 PR 目标分别定义，术语沿整体 PRD 第1节。未交付前驱不限同 Task；Git 差额只是调查线索。原 Author/Approval/Delivery Review 是本批直接行为消费者。

## 2. 整体与本批目标、非目标

本批完整覆盖整体 R1–R6 与 AC1–AC5：在原 Author 确定目标时识别内容关系，形成具体依赖安排，原 Approval 审可执行性，配套分发和实际行为对照。问题是跨 Task 继承未被展开，导致实现和切片审核后才发现实际 PR 带未交付内容。

源码范围为五处：Author `references/planning-body.md`、三个 `templates/delivery-{prd,design,implement}.md`，Approval `references/contract.md`。不新增模块、API、公共 DTO/schema、phase、审批轮次或前驱台账，不以案例增加通用门禁。沿原安装 owner 分发，原 RDT owner 更新命中的既有单元。

不接手旧查询/旅程 Task，不修改其提交或状态，不改客户端/后端业务，不执行 push/PR/merge/部署/归档/journal。不声称本切片能证明产品缺陷率下降。独立 Architecture 尚待评估，本 PRD 不预设其结论。

## 3. 本批起点、前序结果、依赖与剩余责任

本批是当前 Task 的 D1，无同 Task 前序 Delivery。另核实跨 Task 继承：当前 checkout HEAD 和本地 main 均为 `e30c7bb5d4c24bc075dc14cfcd04c1da00fcf78e`，创建从该固定 main 独立分出，未继承旧 `7027b75c…` 或旅程候选。观察时起点与目标内容相同，因此当前没有未交付继承差额或必要前驱。旧 Task 仅提供问题回放，不是当前发布依赖。

计划 PR 目标为 `castbox/guru-trellis:main`。本批未来固定内容 B 选择该独立起点，Planning H0 当前为同一提交；实际实现 H、完整候选与后续目标事实由原 owner 在各自阶段读取，不把 H0 当实现结果。目标普通前进不要求自动重同步或重审。

本批需要原安装分发、定向工程检查及主会话协调的冻结行为对照；具体发布安排只能使用原 Publish/Merge 实际支持能力。缺某项能力时，只限制依赖它的方案。源码/安装/行为验证尚未完成；这些责任都在本批，不预先分给另一个空 Delivery。即使本批后续交付，Task Completion 仍由原 owner判断整体责任，不提前声称完成。

## 4. 本批调用方、场景与流程

| 场景 | 前置条件与触发 | 行为及可观察结果 |
| --- | --- | --- |
| S1 未交付继承 | Author 从跨 Task 前驱起点确定 main 目标 | 读取内容关系与公共交付事实，判断归属/依赖，首次 PRD/Policy 即说明交付安排，而非只写 D1 无前序 |
| S2 前驱已进入目标 | 起点继承内容已合入或有充分等效内容事实 | 不只按 SHA 差异判待交付；独立实施继续 |
| S3 受支持的明确安排 | 前驱尚未进入最终目标，但有原能力支持的具体发布安排 | 写明动作、顺序、条件、责任和恢复事实；独立开发继续，Draft 按实际能力判断，不加统一前驱合并前置 |
| S4 无关目标前进 | 目标有与当前交付无关的新内容 | 不新增依赖、同步、重审或阻塞 |
| S5 遗漏/变化 | Approval 审规划，或 Delivery Review 发布前发现实际条件变化 | 原 Approval 对遗漏/不可执行安排返回原职责；原 Delivery Review 保留最终检查，变化回真实原 owner，不静默改 B/范围/目标 |

先区分起点、固定内容范围和目标，再调查差额、判断必要依赖，随后在原正文说明安排，原审核消费。既有 public 路由不变，没有新增状态转换。

## 5. 完整行为、条件与约束

- R1：Author 确定目标时分别写开发起点、固定审核范围、目标及当时实际关系。提交/路径差额不独立证明归属、已交付或阻塞。
- R2：同 Task/跨 Task 的实际必要依赖均须识别；尚未进入目标的继承内容有明确归属和安排。信息性关联、无关变化和普通目标前进不新增义务。
- R3：本批 PRD 上下文与 implement 的唯一 Delivery Policy 承载结论：可继续动作、依赖条件、剩余责任 owner、恢复所读事实。保留带明确依赖继续独立开发的合法路径，不一律要求合并前驱后才可编码或 Draft。
- R4：Approval 在既有独立交付维度核可执行性，Delivery Review 留最终实际核对。不能虚构堆叠 PR 支持。未知或变化回真实原 owner，不自动改范围、固定 B 或目标。
- R5：五处文本机制补足原职责；分发走原 owner。不新增 runtime/DTO/phase/台账/授权记录/全链 freshness 或仅因目标前进触发的 Reconcile 门禁。
- R6：实际行为验证 S1–S5，分别观察首次识别、可执行安排及合法工作是否误阻塞。模板存在、关键词和机械测试都不替代行为结果。

上述已接受技术约束保留；后续 design 第3节由原 Author 维护唯一来源设计处置，不在本阶段写实质 design/implement 或创建平行矩阵。

## 6. 本批验收、验证方式与未决项

| 验收 | 入口与输入 | 预期观察及证明边界 |
| --- | --- | --- |
| AC1（R1/R2） | 原 Author/Approval 的冻结未交付前驱回放 | 第一次规划即识别跨 Task 继承与实际目标差额，给具体交付顺序 |
| AC2（R2/R3） | 前驱已入目标、原能力支持的明确安排、无关目标前进控制 | 不误阻塞独立工作，不凭 SHA/差额要求同步/重审；不虚构发布支持 |
| AC3（R3/R4） | Approval 输入遗漏/不可执行安排及完整安排 | 前者按原职责指出修订，后者能继续；Delivery Review 最终核对仍保留 |
| AC4（R5） | 五处源码差额及原安装/reapply/drift和声明平台投影验证 | 字节/分发符合原机制，未引入新状态/阶段；不等同实际行为通过 |
| AC5（R6） | 冻结协议原始结果和工程事实 | 分层报告源码、安装、Agent行为及未验证边界，保留失败，不外推产品缺陷率 |

本阶段没有必要需求问题。独立架构尚未发生，实际方案与验证命令由其后原 Author 完成。没有 prewrite Architecture 结果时停在 requirements_ready，不提前写实质 solution。主会话负责行为回放调度，本执行者不重复该工作。

## 7. Canonical 引用与本轮差额

| 当前单元/合同 | 本轮用途与拟差额 |
| --- | --- |
| `docs/requirements/current/task-delivery-lifecycle.md`，RDT-REQ-LIFECYCLE 的切片建立、Planning与固定范围 | 在原单元补跨 Task 目标关系的规划义务，不新建平行 current 文件 |
| `docs/design/current/task-delivery-lifecycle.md`，RDT-DES-LIFECYCLE 的 Creation与Author/Activation、Scope内容边界 | 在原职责中展开 Author→Approval 消费；原 RDT owner 负责真实修订/晋升 |
| `docs/test/current/task-delivery-lifecycle.md`，RDT-TST-LIFECYCLE 的策略/完整性与 Planning 场景 | 原单元说明首次识别与误阻塞验证边界；不把教学文本当行为证据 |
| Author `planning-body.md`、三个模板及 Approval contract | 唯一五处源码目标，补读当时Git/公共事实及可执行安排，不复制新门禁 |
| 现有 Architecture Baseline 与 Constitution | 由独立 Architecture owner authority-first 判断职责/约束影响；本阶段不作 no-impact 结论、不预建 contribution/ADR |

原安装、RDT 与 Architecture owner 保持单写。当前不写共享 README/index，不新建平行知识单元或占位贡献。现有方法补足是否无架构影响，留给独立 owner 判断。
