# D1：阶段成果与完成证据一致性需求

## 1. 整体来源与术语

本批是 Task `649-stage-result-convergence`、generation `0` 的首次全量 Delivery，key 为 `244a5d53-0d81-4d1b-aebf-a6a56bf54e0d`。公共 `scope_ref` 选择整体 [PRD](../../prd.md) 的 AC649-01..07；accepted revision 为 `sha256:0094da0b1fac629390f6454728f0302ec64288219f2c259bdeed725e3fed13c5`。本目录是公共 API 返回的 planning_root，不以文件存在建立 Planning 接受事实。

| 来源与章节 | 角色 | 本批用途 |
| --- | --- | --- |
| https://github.com/castbox/guru-trellis/issues/649 全文及 2026-10-21 修订补充 | 当前 Direct Source 要求 | 原 owner 责任、六维状态、独立及组合验收；已重读，当前无评论 |
| 整体 PRD 第4..7节 | 已接受范围 | 本批全部行为、约束、验收及整体完成责任 |
| https://github.com/castbox/guru-trellis/issues/648 及 archive `2026-10/10-21-648-constraint-premise-review/task.json` | 已交付前置与原正式结果 | 约束来源、前提必要性及 operation 范围判断；不重做其 accepted scope |
| `docs/requirements-design-test-contributions/637-candidate-review-reuse/test.md` 与对应 archive Task | 当前结果样本、历史观察、正式结果入口 | 逐项核对截止点及后续结果，保留旧失败和真实未证项 |
| `docs/{requirements,design,test}/current/task-delivery-lifecycle.md`；最终检查、候选适用性、整体完成及 T637/T638 | 当前 RDT authority | 保留固定 B、原覆盖复用、原公共结果和最终整合顺序 |
| `docs/architecture/00-foundation/{design-constitution,baseline}.md`、`06-governance/change-contract.md` | 当前 Architecture 约束 | AI／脚本分层、单写、最小公共 I/O、正常场景范围；独立 Architecture 判断本候选 |
| 原 Author、RDT、Architecture、Check、Delivery Review、Completion、task-free、Closure／Finish package | 既有接口及职责约束 | 在 step-local Markdown 内补责任；不更改公共接口 |

六维依次是合同 authority、源码实现、制品部署／入口可达、初始化／启用、消费者采用、原业务请求端到端验收。每项结论限定到实际能力、对象和环境；“未激活”不能反推源码未实现。观察截止点指正文实际覆盖的候选或时点，不是后续结果的上限。

## 2. 整体与本批目标、非目标

正常后继实施已经解除限制时，当前规范和测试仍可能保护旧限制。Completion 也可能把实施遗漏、无依据机制前置、真实外部证据及无关未知统一当作外部待补。本批通过原 owner 合同、模板、示例与真实行为评测纠正这些判断；不把脚本变成语义分类器。

D1 覆盖 R649-01..12、S649-01..09 和 AC649-01..07 的全部产品及验证责任。本批交付目标是：各 owner 在自己的合法写入或审核边界收敛当前状态，分别表达六维事实与剩余责任，准确引用晚于正文的正式结果，并完成独立评测和真实多 Delivery 组合。

不启动 #651 或其它 Issue，不改 Backend／业务现场、业务 API 或兼容政策。不新增 Skill/profile/exit/schema/DTO/runtime 状态、状态台账、审核人、审批链、CI 或通用文档清理。不追改冻结历史，不为追记自身 pass 制造额外提交、空业务 Delivery 或递归 gate。无变化的普通交付不制造文档或验证义务。完整升级／Release 矩阵、业务采用及生产效果不在本批证明范围。

## 3. 本批起点、前序结果、依赖与剩余责任

本 Task 尚无前序 Delivery，D1 phase 为 planning，尚无 Planning／Check／Review／readiness 或交付结果。开发起点为 `main@319202beab79c7666ecdb855291bf117e43d407e`；后续 design 分开记录开发基线、固定内容 B 和 PR target，不将其替代最终候选。

#648 已关闭，PR #654 与 bookkeeping #655 已合入上述起点。创建前 source／installed packages 与 drift 检查成功，只证明匹配安装前置；其实际 Agent 的有效 false、execution_error、no-grade 和未验证外部运行继续保留，不能写成“全部绿”。本批还须定位并读取其实际验证结论，分别承接已完成自身验收和未验证边界。

#638 的 candidate Check → 原 final_integration → 实际 candidate/begin_check 重绑 → final Check → 完整 committed Review 是既有约束。本批的当前 Docs 写入必须经过这条链。#637 的实际后续结果须 fresh 读取原 archive、PR #644 及 Git 可达性，才能有限修正文案。

D1 不预设第二个产品 Delivery。若真实整体 Completion 发现新的独立剩余责任，仍由其原路线决定；不能为追记本批终态造空 Delivery。组合验收中的 D1／D2 是隔离样本的实际公共切片，不冒充本 Task 的第二次业务交付。整体 Completion 还须核对全部实际 Delivery、源 Issue、必要证据与 RDT／Architecture；本批合并本身不等于完成。

## 4. 本批调用方、场景与流程

| 场景 | 调用方／前置／动作 | 本批处理与可观察结果 |
| --- | --- | --- |
| DS649-01（S01） | Author 在合同 D1 写临时限制，后继 D2 完成其解除条件 | 原正文保留对象、原因、解除条件、阶段和后继 owner；实现与知识 owner 同步当前规范、指南及断言，旧观察保留 |
| DS649-02（S02、S06） | Delivery Review／Completion 读取部分能力已实现、其它能力仍待实现且环境证据未到的同范围成果 | 分别列事实和缺口；局部实现不扩为整体完成，环境未证不改写源码事实 |
| DS649-03（S03） | 必要消费者仍无实现，Completion 核全 scope | 回原实施／规划责任，不伪装成 evidence_pending |
| DS649-04（S04） | 机制自行增加迁移／启用门槛；对照有有效来源的外部前提 | 消费 #648 的来源、必要性和 operation 判断；前者回原机制／Architecture，后者保持原 evidence_refresh |
| DS649-05（S05） | 后续正式 Check／Review／Delivery／Completion 晚于受审正文 | 当前入口写清截止点并引用原公共结果及 Git／PR；保留旧失败，不回写正文自己的最终 pass／HEAD；实际修订仍重审受影响覆盖 |
| DS649-06（S07） | 合同合入、源码实现、制品部署，Control／phase 尚未开放 | 前三项保持成立，初始化／启用、采用、原请求 E2E 分别取证或说明不适用；切换证据只阻断实际依赖的声明 |
| DS649-07（S08） | task-free 完成有界本地修改，或触及状态／门禁 | 只报告 edited paths、本地目标检查和明确未验证项；门禁只影响有效 operation，不声明部署／激活／采用／E2E |
| DS649-08（S09） | 正常交付没有阶段限制变化 | 沿原合法路径继续，不新增台账、空文档、字段或重放已有验证 |
| DS649-09（组合） | 匹配 #648 安装后的同一隔离 Task 两个实际 Delivery | 合同限制→后继实施→说明／断言收敛；实际约束冲突与合法修订经原 owner 重入，再 candidate／final 链、committed Review、Delivery Review／Completion；被测 Agent 不接收预期答案 |

## 5. 完整行为、条件与约束

- DB649-01（R01..02）：只在本批存在真实临时限制时，由 Author 在原 Policy、步骤、Docs Plan 表达其五项边界。条件满足后，实现及原 RDT／Architecture 更新其拥有的当前内容。历史记录保持原观察；当前入口不依赖过期文字与散落覆盖说明拼装执行含义。
- DB649-02（R03..05）：Check 比较实际行为、当前文字及适用断言。绿色命令不能保护错误预期。Delivery Review 审本次载荷，Completion 审全范围；六维分别取证，不适用须有理由。局部状态不泛化为全版本冻结或全部完成。未激活／环境未知只影响真正依赖该状态的操作及声明。
- DB649-03（R06）：Completion 依缺口性质回现有 owner。实施遗漏回实施／规划，无依据前置消费 #648 后回机制／Architecture；真实必要外部证据沿原 evidence_refresh；无关未证项不阻断合法完成。不得仅因“还缺东西”统一选 evidence_pending，也不得把技术细化改成 scope 变化。
- DB649-04（R07..08）：结果正文明确候选／观察截止点及真实剩余边界。晚到结果由原正式公共结果与 Git／PR 承接；必要说明由原文档 writer 在合法边界更新。#637 仅修可证明过期的当前声明，安装、发布、业务采用及矩阵未证仍未证；不改命令、旧失败、当时未知、冻结历史或公共身份。
- DB649-05（R09..10）：共享 current 只由原 final_integration 写入，随后实际重绑并 final Check／完整 committed Review。说明性修订同样适用候选覆盖规则。工程事实可按 #637 复用，不重做无变化设计／测试／合并／晋升。Closure／Finish 只做终态、归档与 bookkeeping，不代写共享 Docs 或代替质量门禁。
- DB649-06（R11）：task-free 完成报告限本地编辑、检查及 unverified boundaries。涉及 gate 时消费 #648 operation 判断，不把单次迁移门槛扩成所有接口不可用。公共 DTO 不增加状态维度字段。
- DB649-07（R12）：原 native 入口让实际 Agent 读真实来源、候选和必要结果，自主判断并调用原 wrapper。期待值和 host 评分留在被测上下文之外。独立、组合与 #648 自身验收分别取证；结构、fixture、exit 和安装绿测不单独证明行为正确。失败、错误出口期待、运输错误和未知分开保留，不靠改 fixture 强制通过。
- DB649-08：只覆盖诚实协作正常路径、常见遗漏与 stale/mismatch；不扩恶意篡改、绕过、并发压力、锁、fault injection。canonical／dogfood／installed／平台入口成套一致，最多一个代表 clean，未验证 Release 和外部采用明确说明。

规范性来源设计的逐项处置只在本批 design 第3节维护。本 PRD 的 requirements 阶段输出只承载需求与候选，不代表实质 solution 已被接受，也不代替独立 Architecture assessment；后续方案与执行安排以当前 design／implement 及其原门禁结果为准。

## 6. 本批验收、验证方式与未决项

| 验收 | 输入与入口 | 预期观察 |
| --- | --- | --- |
| DAC649-01 → AC01 | 原 Skills／模板／示例、命中 spec 和调用方 | DB01..08 由原 owner 承担；global 只编排，无新增公共 I/O／状态／审核人 |
| DAC649-02 → AC02 | 原 Check、Delivery Review、Completion native 样本；失效限制、错误断言、遗漏、外部待证、混合能力、合法无变化 | Agent 自主检错并真实调用 wrapper；每次语义与运输／结构分别审核；对照不增加无依据阻塞 |
| DAC649-03 → AC03 | 六维、缺切换证据、无依据迁移 gate、task-free 本地完成对照 | 六维不合并，已成立事实保留；仅阻断依赖 operation；task-free 不声称部署、激活、采用或 E2E |
| DAC649-04 → AC04 | #648 自身结果与匹配安装；同一实际公共 Task 的 D1/D2 组合 | 实际合同、实施、文档／断言、冲突／修订、原 owner 重入、候选与最终门禁和 Completion 顺序可定位；不以独立样本替代组合或反向替代 |
| DAC649-05 → AC05 | #637 原 Test／archive、fresh PR #644／Git；终态晚于正文对照 | 只纠正已证过期项；准确截止点与引用；旧失败、未知及其它未证项保留；不递归追记、不免修订重审 |
| DAC649-06 → AC06 | 命中 package/runtime、source/installed、声明平台、apply/reapply、drift/mode/sidecar | 真实命令结果分层；最多一个代表 clean，零未处理 .new/.bak；不宣称完整 Release 或业务采用 |
| DAC649-07 → AC07 | 原 RDT／Architecture、candidate/final gates、正式交付及整体终态 | 当前知识、真实 Check／独立 Review、合并且可达 main 的 satisfying PR、Issue CLOSED/COMPLETED、Closure／Finish／Cleanup 各有事实 |

当前无待用户裁决的 scope 问题。评测支持的 current Delivery 适配、独立无答案执行与同样本组合由 Author／Architecture 在 solution 阶段细化，具体安排见本批当前 design／implement；方案与执行安排未完整时不得进入 plan_ready。所有行为评测、实现和终态仍待执行，不能预填通过。

## 7. Canonical 引用与本轮差额

| 当前 authority | 本轮差额及兼容边界 |
| --- | --- |
| `docs/requirements/current/task-delivery-lifecycle.md`：切片 Planning、最终检查、候选覆盖、整体完成；`completion-closure.md`：完整终态能力 | 补阶段限制收敛与六维／缺口责任；保留原 accepted scope、public result、固定范围及 Closure 独占 |
| `docs/design/current/task-delivery-lifecycle.md`：Author、最终晋升、候选职责、Delivery Review；`knowledge-maintenance.md` | 将状态语义放在原 step-local owner；不改 runtime 公共操作、现有单写及晋升顺序 |
| `docs/test/current/task-delivery-lifecycle.md`：T637／T638；#637／#648 原 Test | 添加独立状态样本、真实组合及截止点对照；历史记录保持自身候选，不冒充新通过 |
| `docs/architecture/00-foundation/{design-constitution,baseline}.md` 与 `06-governance/change-contract.md`；`01-current/system.md` 的 workflow/AI-runtime 边界 | 由独立 Architecture 判断是否仅无影响／必要 task-owned 贡献；Planning 不晋升 current、不预建空 ADR |
| canonical Author 的 planning-body／authoring／Delivery implement、RDT current-knowledge／contract、Architecture contract | 在现有正文和知识写入责任加入真实限制、解除及后继责任；不另造状态管理模块 |
| canonical Check／Delivery Review contract、Completion SKILL、task-free contract、Closure／Finish SKILL | 各审自己范围的阶段事实、缺口和载荷；Closure／Finish 不扩大写入边界 |
| canonical quality-guidelines／workflow-contract | 保留验证范围、candidate applicability、AI 判断与脚本事实分层；公共流程入口不复制 step-local 新逻辑 |

实施与各原审核 owner 在执行前继续完整加载其命中合同、引用和必要关联条件。这里只定位差额，不以链接替代正文或实际读取。
