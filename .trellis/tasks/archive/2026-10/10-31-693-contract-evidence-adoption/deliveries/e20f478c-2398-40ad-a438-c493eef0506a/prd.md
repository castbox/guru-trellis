# D1：合同承接与证据判断公共方法

## 1. 整体来源与术语

本批消费 Task 根 [整体 PRD](../../prd.md) 的公共 accepted_scope，revision 为 `sha256:4e42e178b4a5d8380226fe2595534d9459a24d5cf60514537ef21553800e81ac`，scope_ref anchors 为 `AC693-01`、`AC693-02`、`AC693-03`、`AC693-04`。DeliveryKey 为 Task `693-contract-evidence-adoption`、generation `0`、Delivery `e20f478c-2398-40ad-a438-c493eef0506a`；planning_root 为本目录。

| 来源 | 角色、条款与用途 |
| --- | --- |
| [live #693](https://github.com/castbox/guru-trellis/issues/693) 与整体 PRD | 完整要求；本批落实历史取证、原 owner 方法及公共指导分发，保留正式采用的整体条件。 |
| `trellis/presets/guru-team/spec/workflow/workflow-contract.md`：Candidate Applicability And Coverage | 当前共享合同；已有消费者覆盖、事实/判断区分、旧证据适用性是可复用能力。 |
| 同目录 `quality-guidelines.md`：Test And Validation Value、Validation Scope Ownership | 测试层、fixture 和验证范围的原 authority；不得从绿测推定全链覆盖。 |
| 原 Architecture package `references/contract.md`：Adopted-mechanism review、独立读取、Responsibility and change causality | 已交付机制方法、五原则与当前独立性；本批不重做机制框架。 |
| `docs/requirements/current/knowledge-maintenance.md` 的 R648-01..06、R-MECH；对应 design/test 当前单元 | 当前完整知识：来源承接、实际消费者、共同错误预期、证据刷新与机制采用。保留已有约束，不继承旧 Task 的专项评测义务。 |
| `docs/architecture/06-governance/change-contract.md`：Constitution applicability consumption、候选适用性与独立职责 | Guru 项目的原方法消费与晋升职责，不建立另一套项目方法。 |
| 后端固定事故提交 `eaaf5b3cab3d3202f67956294d11aa6eed46087e`、原 Task/设计/coverage、[PR #953](https://github.com/castbox/ai-chat-roleplay-backend/pull/953)、[#955](https://github.com/castbox/ai-chat-roleplay-backend/issues/955)、[#961](https://github.com/castbox/ai-chat-roleplay-backend/issues/961) | 只读事实来源；说明具体合同失配、条件与证据边界，不成为业务修改或专项业务验收。 |

生产者成功、消费者可用、工程执行事实、当前语义判断沿整体 PRD 的术语区分。本批方法不定义业务字段或成功条件；它要求原 owner 到所属业务 authority 和真实消费者中取得这些定义。

## 2. 整体与本批目标、非目标

整体目标包括公共方法、项目 Architecture/Design 指导及后端正式采用。本批先交付公共方法与 Guru 项目的原指导承接，使后续原升级 owner 能从一个已交付的完整源采用，而非依赖未审 patch。

本批在现有 Author、Architecture、Check、Branch Review 和交付判断内，把合同承接、参数生命周期、测试边界与工程证据采纳的具体方法写到原 authority；充分的现有规则只引用和说明使用。公共 I/O、typed exits、schema、runtime 和阶段不增加。保留 #694/#695 已交付原子能力。

本批不执行后端安装或修改其项目指导；`AC693-05` 是公共交付后的剩余责任。业务实现、业务测试、数据、部署、QA、#692、额外 Issue/release/tag 及整体 PRD 的其他非目标全部保持。没有专项 native eval、A/B、固定数量、耗时统计、额外安装或完整多平台矩阵。

## 3. 本批起点、前序结果、依赖与剩余责任

固定开发基线为 `main@e514770dfa03711a4606046232593b9bf782695a`，D1 尚无前序 Delivery。该基线已包含关联 Architecture 机制指导及 #695/#694；它们是起点，不是本批收益。Task scope 已接受，当前 Delivery 为 planning，尚无方案接受、实施、Check 或 Review pass。

取证已经确认：事故当时安装的共享规则已有未改消费者、工程事实适用性和测试层约束。原设计列出 Public API、独立 State 与 ordinary 候选，并写有准备早于新记录创建的顺序。代码中的候选采纳保存 options 并标记成功，而读取器另检查完成快照；新准备链将预分配输出 ID 送入按既存消息读取的旧函数。它们支持具体合同与生命周期失配分析，不证明历史 reviewer 的实际思路。

原公开 Task 在事故提交保留 Planning 接受及候选 Check pass；原证据 E30 明确 integration 仅编译、未重跑 Mongo/race。PR #953 正文也保留这条边界。后续仍需核对最终候选、Branch Review 和交付判断能恢复的公开事实；不跨读其他 owner 的私有 checkpoint，不以记录缺失认定未审。

后端当前主 checkout 只读观察为 `dev@c03e75db98db22b4f55bac24add34c3b52d104b8`，安装源指向 `8d746ce561c464ca28af4dc91adf085132e4098c`，且存在在途 Tasks。这是规划观察，不是写入目标锁定或采用结果。后续原 Upgrade owner 须重新核安装、Task/会话、工作区和精确写集，展示该写集并取得当前对话确认后采用。未采用前 Task Completion 不成立；D1 合并不自动完成整体。

## 4. 本批调用方、场景与流程

| 场景 | 原 caller、前提与触发 | 行为、观察与原路由 |
| --- | --- | --- |
| D1-S01 结果承接 | Author/Architecture 比较执行链新旧生产者 | 从正式入口定位实际输出、持久状态及消费者使用前提，涵盖未改读取器；具体缺口回最早受影响原 owner。 |
| D1-S02 时序复用 | 新编排调用既有函数，但对象或阶段变化 | 核对参数身份、对象是否存在、前置状态与执行顺序；旧类型/名称/审核不能替代当前判断。 |
| D1-S03 验证对应 | Check/Branch Review 从有效合同确定预期，读取当前测试 | 对齐正式入口/context/配置/依赖/持久状态/分支/观察点；区分合法边界前 fixture 与边界内代产出，不削弱局部测试价值。 |
| D1-S04 证据继承 | 入口或启用范围扩大，原工程事实仍可核验 | 判断保留、失效与补充范围；新可达或条件不明时补命中验证，其余事实保留，当前语义判断仍亲自完成。 |
| D1-S05 历史取证 | 当前 Author 读取固定源码、原公开计划/阶段结果与实际命令 | 分别报告合同未承接、检查责任、已证执行事实和不能恢复的历史判断；区分缺陷引入与入口扩大。 |
| D1-S06 分发与采用边界 | 公共候选完整，原 preset/check/review owners 执行 | canonical→dogfood/声明平台/reapply/drift 沿原路径一致；交付判断不把这些事实升级为后端采用或业务修复。 |

## 5. 完整行为、条件与约束

- **D1-R01 → R693-01/02，S05**：调查以当时安装合同和实际候选为准，逐阶段核 Planning/Architecture/Check/Branch Review/交付的可得对象、已知条件、实际命令、工程事实来源与理由。支持的因果写具体来源；推断与记录缺口分开。规则已存在时不能称为规则缺失。不能因代码有缺陷、旧测试绿或没有 GitHub review submission 就认定 Agent 当时没有检查或如何判断。
- **D1-R02 → R693-03/04/07，S01/02**：原方法要能从新链成功走到真实消费者可用性，并核对复用参数的对象、存在状态、持久前提和时序。使用原业务 authority 定义结果；无 diff 的消费者仍在范围。只补真实方法差额，不复制已交付机制审查和五原则。
- **D1-R03 → R693-05，S03**：对齐测试声明边界及正式路径条件。允许边界前状态 fixture 与外部替身；边界内结果由 fixture 代产出、输出被修正或关键条件绕过时，不能用下游绿色证明该边界。真实数据库和测试名称不改变该判断。局部测试无需证明边界外的全链。
- **D1-R04 → R693-06，S04**：记录原工程事实实际采用的部分与理由，不将采用写成当前执行。不因阶段/reviewer/commit 变化无因重跑；不因同源码或 CI 绿推断新可达路径已验证。新输入、分支或未知适用性按风险补证，保留必要保护和有效局部证据。
- **D1-R05 → R693-07/08，S01–06**：方法归原共享规则和 step-local owners；项目原 Architecture/Design 指导引用其唯一正文。修改通过原 RDT/Architecture 隔离候选、候选 Check、final_integration、实际 after 绑定及最终质量链承接；不在 Planning 先改 shared current，不新增 ledger、字段或审批。
- **D1-R06 → R693-08，S06**：canonical 为源，按原 preset 完整 reapply 同步 dogfood 和受影响声明平台；逐项处理 sidecar，验证真实投影。只执行本批必要定向检查。正式后端采用在公共交付后由原 Upgrade owner 负责，D1 的证据不替代该完成条件。

未选择具体实现机制前不写 substantive design/implement。规范性来源设计的唯一处置留在本批 design 第3节；本 PRD 保留完整行为和兼容条件，不维护第二矩阵。

## 6. 本批验收、验证方式与未决项

| 验收 | 要求/场景 | 本批入口、输入与可观察结果 |
| --- | --- | --- |
| D1-AC01 | D1-R01；S05；整体 AC693-01 | 用固定原规则、规划、源码、测试和公开阶段/PR事实核对原因、责任与未知项；不把推断或缺失记录写成已确认 reviewer 思路。 |
| D1-AC02 | D1-R02/05；S01/02；整体 AC693-02 | 原 Author/Architecture/Check/Review/交付指导形成可操作且不重复的生产者→消费者、参数/生命周期方法；项目原指导消费同一来源。 |
| D1-AC03 | D1-R03/04；S03/04；整体 AC693-03 | 原 Check 与独立 Branch Review 亲自核对 fixture、关键分支及证据继承方法，区分实际命令、静态规则、语义判断和正式路径未知；不新增自动语义裁决器或业务测试。 |
| D1-AC04 | D1-R05/06；S06；整体 AC693-04 | 命中 package、canonical/dogfood/installed、声明平台、reapply/drift/sidecar 的现行验证及完整 Check/独立 committed Review/PR readiness 通过；结果只覆盖其实际范围。 |

本批需求没有待决产品问题。历史判断与命令来源无法恢复的部分由 Author 如实保留，不能补造；具体最小方法与项目指导承接由独立 Architecture 评估。后端安装、真实业务链、部署/QA和完整矩阵不在本批完成声明内。

## 7. Canonical 引用与本轮差额

| Authority | 本批用途与待实施差额 |
| --- | --- |
| `docs/requirements/current/knowledge-maintenance.md`：R648/R-MECH | 复用消费者、关键前提、完整来源和机制审查；只在原完整单元承接本批新增的合同连续性与证据判断方法。 |
| `docs/design/current/knowledge-maintenance.md`：D648/D-MECH | 保留原唯一方法 owner 与晋升链；本批拟写只定位方法归属和现有 owners 消费关系。 |
| `docs/test/current/knowledge-maintenance.md`：T648/T-MECH | 保留原真实证据分层与历史观察；本批用现行定向检查和原语义质量链验证，不继承历史专项矩阵。 |
| `docs/architecture/README.md`、`00-foundation/design-constitution.md`、`06-governance/change-contract.md` | 当前五原则、项目职责与原方法消费；项目必要差额由原 Architecture owner 隔离提出并晋升，不复制业务领域正文。 |
| canonical workflow-contract/quality-guidelines 及原 owners 的 contract | 共享方法和测试有效性正文的候选落点；step-local 只补真实缺失的消费指导，不改变公共 I/O、状态或 executor 事实边界。 |

以上为本批 requirements 阶段的边界和候选方向，不表示共享 authority 已修改、方案已批准或方法效果已被执行证明。
