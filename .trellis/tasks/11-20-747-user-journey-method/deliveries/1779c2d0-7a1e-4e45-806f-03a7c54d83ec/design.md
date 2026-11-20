# D1 连续操作与阶段交接设计

## 1. 设计目标、需求承接与内容基线

本批落实 JQ-R1、R2 和适用的 R5/R6，验收 AC1、AC2、AC6、AC7、AC8。B 为 Intake 固定读取的 `origin/main@61da60132bd0f6b64ab8626ac3158093481cd21e`。当前 Planning H0 同 B。最终候选在实现后以实际提交为 H，交付目标为 `castbox/guru-trellis:main`。

采用原 Architecture candidate_assessment 的 `target_native`。现行权威是 `docs/architecture/README.md`、`00-foundation/design-constitution.md` 和 `06-governance/change-contract.md`。决策沿用 `ADR-REVIEW-SUFFICIENCY`，差额落在 `ARCH-REVIEW-SUFFICIENCY` 的隔离提案。

## 2. 当前系统、边界与目标差额

首次 Delivery 无前序。Clarify 的 choices 段已有证据和选择分类，Author 正文合同已有复杂度与层级深度要求。共用 review-sufficiency 已有 source/consumer 覆盖原则。补齐原方法怎样推导多阶段行为、怎样检查阶段交接。D2 的最小旅程优先和证据有效性仍是后续工作。

## 3. 来源设计处置（唯一）

| #747 条款 | 原承诺 | 处置与落点 | 理由及影响 |
| --- | --- | --- | --- |
| JQ-R1、方案与职责 | Clarify 在 Discover the actual choices 推导连续正常动作 | retain，§4 Clarify、§6 | 复用现有真实来源和资格边界 |
| JQ-R2、方案与职责 | Author 第3节及所属正文承接阶段语义和资源交接 | retain，§4 Author 和 Architecture/Approval、§6 | 技术判断留在原职责。当前自动化流程与 API 继续沿用 |
| JQ-R5、约束与兼容 | review-sufficiency 的 Form and cross-check coverage 承接独立推导 | retain，§4 Review | 保留读取顺序、隔离、审核人数、原专业边界及可复用证据 |
| JQ-R6、实施顺序与知识整合 | 最小正文结果、原 RDT 和 Architecture 整合 | retain，§4、§9 | 本批只整合 D1 的差额，旧观察保持原义 |
| 验证计划与兼容 | V1 原生执行及本批 V5/V6，使用原受管入口 | retain，§7、§8 | 机械检查与语义证据责任清楚，覆盖同一切片 |
| 方案与职责 | Author examples 采用去敏过程示例 | retain，§4 | D1 说明阶段与引用。D2 在同一示例补其负责的验证内容 |

没有偏离当前来源的上游处置。

## 4. 模块、职责与设计取舍

- Clarify 的 `references/contract.md` 在 Discover the actual choices 写出从真实入口推导连续起点、阶段、等待中再操作及可见结局的方法。确定原行为与真实未决选择的边界。
- Author 的 `references/planning-body.md` 第3节规定在 PRD 写阶段行为，在 design 写实际交接的不变量、动作顺序、writer/reader 以及失败或放弃后的归属。运行例子放在现有 `examples/planning-body/journey/`。去敏示例属于教学。
- `review-sufficiency.md` 的 Form and cross-check coverage 补原独立 reviewer 的推导方法。Architecture 继续先读 baseline、constitution、change contract。Approval 使用已有共享入口判断本批设计。两者在原职责中判断支持的正常路径能否维持该条件。
- 选用现有 Markdown 及其管理机制。Architectural proposal 只修改已存在审核域的完整单元，沿用已采纳 ADR。脚本仅负责检查、捕获和分发确定性事实。

## 5. 接口与数据

沿用当前 Clarify 需求输入及原退出契约。Author 各 profile 仍在所属正文输出，原 Architecture/Approval 消费当前的候选或完整计划。共用 spec 被原审核 owners 读取。原 managed package 和 managed-spec 分发协议承接正文。公共标识、状态、typed exit 和 schema 全部沿用主线。

## 6. 状态、顺序、正常与失败流程

处理正常多阶段交互时，Clarify 从来源及真实入口还原当前允许动作，说明等待期间能怎样再次操作。按确实存在的分支说明成功、失败、放弃或恢复的可见结果。明确局部确认、后台任务完成、可靠保留与最终提交分别由什么可见事件建立。无 UI 时取实际调用方与可见结果。真正未知的产品选择停在原 Clarify 的受影响分支。

Author 展开当前设计时，从每个相关业务交接说明交出者、接收者、writer/reader、必须持续成立的条件和先后动作。以普通编辑稿引用为例，后继表单读取该内容所需的资源在触发原持有者释放前必须可用。若接管或写入失败，说明由谁保持和清理以及调用方看到什么。Architecture 与 Approval 根据其各自 authority 和读取顺序追溯候选是否满足这些条件，再对照候选和后读总结。正常场景资格、真实产品选择及原技术修订路线继续适用。

## 7. 恢复、兼容、迁移与集成

各阶段仍通过原恢复和 stale 处理入口。现行工具 owner 接收完整候选，保留目标用户文件、Task/session、workflow 和未涉及投影，并回读实际结果。缺少匹配 provider 时保留失败和依赖缺口。没有公共数据变化或迁移步骤。后继 D2 可读取任何来源明确且已定义的正常旅程。

## 8. 验证设计

| 验证 | 入口、输入及观察 | 可支持结论 |
| --- | --- | --- |
| V1 | `codex exec --ephemeral --json`，中性分离的产品来源、组件事实和候选。期待覆盖等待中再次编辑、局部确认后退出、恢复至最终保存、真实待定选择和资源交接空档。同一组 V1 输入经现有原生入口分别观察 Clarify/Author 和独立 Approval 方法。后一过程使用未参加写作、没有前一输出的新进程。它先读取原 provider 的方法和来源，再输出关键问题并单独读取独立候选。两个过程是只读方法观察。完整正式 Approval 继续采用当前 Task 的原 gate。独立评价者在运行前冻结判据，按原始序列核对结论 | AC1/2/6/8 的本例方法能力 |
| V5 | 匹配 Fork 和受管 Python 运行现有 planning-body 与 review-sufficiency 分发测试、受影响包合同验证。核实实际安装与 reapply、投影和用户文件 | AC7 的分发和结构 |
| V6 | 原 `guru-upgrade-tools` 使用 local_candidate 在本 checkout 同步，回读 runtime/native current、ownership、dogfood drift 和 sidecar | AC7 的隔离工作区采用 |

工具或模型装配失败保持原记录，由原 owner 修真实缺口。证据限于实际方法、选定投影及本 checkout。

## 9. Canonical 引用、本轮差额与实际未决项

本批 PRD 第7节定义当前 RDT 单元及关系。RDT 补现有行为验证和审核充分性单元中的 D1 结果、设计接入与测试责任。架构读取 [本批隔离贡献](architecture-proposal/README.md) 的九项关切与目标。隔离目录提供现有域的完整拟写内容，沿用现有 ADR。原维护者在实施和工程验证完成后将差额整合并回读，等待独立 committed Review。当前没有待定的产品或架构选择。
