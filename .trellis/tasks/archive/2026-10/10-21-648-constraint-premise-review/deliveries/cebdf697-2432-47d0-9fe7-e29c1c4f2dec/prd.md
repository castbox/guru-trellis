# D1：约束与关键前提审查方法及行为验证

## 1. 整体来源与术语

本批属于 Task `648-constraint-premise-review`、generation 0，Delivery `cebdf697-2432-47d0-9fe7-e29c1c4f2dec`。公共 accepted_scope 为根 [prd.md](../../prd.md)，revision `sha256:87c8fb7043d29a3c6591f3d3696bc5cb0ef41f787582592fbdef0fc4452a4d61`，scope_ref 覆盖全部 R648-01..07 和 AC648-01..08。planning_root 是当前目录，不使用 Task 根开发方案。

Direct Source 为 [live #648](https://github.com/castbox/guru-trellis/issues/648) 完整正文及 2026-10-21 补充，角色为要求；边界、原 owner 分流和现有公共机制是设计约束。根 PRD 第1节的完整 current RDT/Architecture 和 #637/#638 来源已实际读取。术语沿根 PRD：规范性约束、事实证据、接受设计和关键前提分开；同域 A 不改变门禁保护的不变量，B 改变它。最终来源设计处置只在本批 design 第3节维护。

## 2. 整体与本批目标、非目标

本批全量交付 #648：先冻结当前匹配版本并真实无答案提示采样，区分已有能力和方法/验证缺口；再在原 owner 方法、示例与原测试入口补齐，并通过原完整交付链。解决政策已进入上下文而错误前提被设计/实现/测试共同继承的问题，不能仅增加链接。

本批不改业务政策/API/代码或 Backend 现场，不启动 #649/#651，不新增阶段、profile、审批人、ledger、公共 DTO、schema/typed exit、runtime 状态或重复 CI。公共 API 若确需变化回原范围/兼容决策。保留 #637 复用与 #638 最终整合。最多一个代表 clean；完整 Release/升级矩阵、版本发布与业务实际采用不在本批。

## 3. 本批起点、前序结果、依赖与剩余责任

本 Task 尚无前序 Delivery。开发起点/Planning H0 为 main@cca65742bc485f8ab4e6399623b70dd5aebc25bd，PR 目标 main；内容固定 B 由原 projection 确认后写 design，不因目标前进自动追赶。#637/#638/#635 均已 CLOSED，PR652/653 已 MERGED 且可达起点；它们的已有能力保留，旧 pass 不是当前证明。

当前已在 repo 外冻结该 Git 版本源码，尚未修改 canonical；变更前现有 Architecture 错误样本/合法对照启动前因缺 isolated CODEX_HOME 失败，未产生语义结果，正沿原 adapter 环境恢复。此为真实研究事实，不证明方法有误。所有本批行为、安装与质量验收仍待执行。

D1 不延期自身效果到 #649。交付后 Task Completion 核全部要求、结果及边界，随后 Closure/Finish/Cleanup。局部依赖只阻塞真正依赖场景；全部 satisfying PR 必须 MERGED 且可达 live main，Issue CLOSED/completed。单次合并不证明 Task 完成。

## 4. 本批调用方、场景与流程

| 场景 | 入口、前置和触发 | 必须观察 |
| --- | --- | --- |
| D1-S01 | 原 Author 已读政策，候选遗漏必要条件 | 从来源到设计具体落点，自主指出条款/候选影响，非链接或 retain 自证 |
| D1-S02 | 原独立 Architecture，接受设计前提被原证据否定 | 分清四类 authority/事实/设计/假设；检查继承前提，合法来源例外通过 |
| D1-S03 | 实施者发现规划内冲突，无 scope 扩张 | 停受影响操作、返回最小事实；协调者回最早原 owner，修订/重审匹配后恢复；独立工作继续 |
| D1-S04 | 原 Check/Branch Review，设计/实现/测试共同错误 | 依据有效合同检错，不迁就实现改断言；职责违规无需先发生生产功能故障 |
| D1-S05 | 状态/开关/迁移/分支变化，消费者未改 | 检查真实前后状态和受影响消费者，无影响对象不新增义务 |
| D1-S06 | 同 reviewer、新证据否定前提，代码/测试未变 | 刷新命中判断，保留合法无变化事实；组合影响不明则完整评估 |
| D1-S07 | task-free gate/admission/phase/switch/rollout，新增跨能力前置 | 说明不变量/最小迁移/不适用操作/真实缺证据阻断范围/owner/consumer，停止受影响写入，走原 evolution/scope route |
| D1-S08 | 同域 A/B 缺同门禁证据 | A 成功且解释不适用，B 失败且解释不变量；共同错误限制 A 仍由审查指出 |

## 5. 完整行为、条件与约束

**D1-R01（整体 R648-01）**：Author 读取约束完整条件、否定、例外、对象与真实来源，在设计和唯一来源处置给具体落点。不复制基线、不建逐条账本；原则复述、引用或 retain 不证明符合。

**D1-R02（整体 R648-02）**：Architecture 对可行性/职责/拒绝/依赖的关键前提读原证据，前序 ADR、批准、知识晋升和代码/测试一致不豁免。比较原 before_authority 与候选，候选拟改基线/ADR/测试不自证。例外按真实来源/范围/修订依据审，不设无条件文档优先级。独立性隔离通过叙述，同时取得必要事实/约束；缺证据保留不确定性并走 incomplete/blocked。

**D1-R03（整体 R648-03）**：实施中发现批准方案违约、前提不成立或不能兑现承诺，即使无 scope 扩张也停止受影响操作，返回条款来源、候选落点和影响。约束仍有效而方案错，回 Author/Architecture 修方案、保留 scope；authority/承诺/例外冲突或需改范围，回 Clarify，Architecture 只提供具体冲突事实；规划有效而实现/断言错，回 implementation/Check。实施者不自行改需求、基线、断言；无冲突工作按真实依赖继续。冲突解决、受影响规划/审核及实际候选匹配后恢复，脚本或旧批准不能恢复。

**D1-R04（整体 R648-04）**：Check/Review 先从适用权威确定应观察行为，再核实现、测试入口和断言。状态/开关/迁移/分支变化检查真实前后状态及未改消费者，不机械生成全矩阵。具体职责违规即合同缺陷，不要求生产功能故障已发生。

**D1-R05（整体 R648-05）**：区别有效约束要求的依赖和机制无依据新增的限制；后者回原机制/Architecture，不伪装为外部缺证据。task-free 当前执行 owner 识别不变量、最小门禁触发迁移、不适用 operation、实际阻断范围及 evidence owner/consumer。无依据跨能力依赖停止受影响 target write，经既有 evolution/scope route 返回，不扩大范围。真实 A 不改变不变量，缺证据仍成功；B 改变不变量，缺同证据失败。共同错误限制 A 也须检出并回原机制/Architecture 或 Check。

**D1-R06（整体 R648-06）**：保留 #637 审核/工程事实复用，新证据否定原关键前提即刷新受影响判断，代码/测试未变不能免审；其余覆盖保留。组合影响不明完整评估，不因 owner/stage/HEAD 变化无因重跑。不读取或重建退休 private state。

**D1-R07（整体 R648-07）**：变更前固定当前匹配版本，样本去敏保留失效关系；真实 Agent 无答案提示读文件、自主判断、写结果、调原 wrapper，host 期待表不注入。对改变的方法以相同或严格等价输入复核；审核条款、因果、预期与路由，正确出口/读取顺序/关键词/结构/绿命令均不能独立证明检错。两边都检错记已有能力，保留首次失败、修复和边界。Author、实施停点/分流/恢复、Check/Review 和 A/B 均在本项实际证明。

保持原首次完整、差额复核、candidate Check/final_integration/实际重绑 final Check、committed Review 分工。只在原 Markdown 方法/示例补实际缺口，global workflow 只编排和有歧义的重入。不新增公共对象或授权记录。

## 6. 本批验收、验证方式与未决项

| 验收 | 对应场景/行为 | 实际入口、输入和观察 |
| --- | --- | --- |
| D1-AC01 | S01..08 / R01..07 | 变更前匹配主线，原 owner 真实盲测错误/合法对照，区分已有能力与缺口 |
| D1-AC02 | S01..07 / R01..06 | 原 Markdown/示例实际差额；不复制 step-local 判断或无证据扩改全部 owner |
| D1-AC03 | S01..05 / R01..04、07 | 原 Architecture/Check semantic_authoring 及跨阶段 native；Author 落点、实施停点/分流/恢复、Check/Review 共同错误与未改消费者 |
| D1-AC04 | S07..08 / R05、07 | task-free A/B 真执行与共同错误审查，A 成功/B 失败及各自理由 |
| D1-AC05 | S06 / R06..07 | 同 reviewer 前提变化复核与合法无变化对照，前后同口径，失败/修复保留 |
| D1-AC06 | 全部 / R02、06 | 原 wrappers/public phases，首次完整及 candidate/final/committed 分工保持 |
| D1-AC07 | 全部 | 命中 package/runtime、source-installed、声明平台、apply/reapply/drift/modes、零未处理 sidecar，最多一个 clean |
| D1-AC08 | 全部 | 原 RDT/Architecture 同步；源码、Agent、安装和外部采用分层，未验证边界诚实报告 |

对应整体 AC648-01..08，当前均未验收。没有用户未决范围选择。当前能力实测、样本等价性、精确方法差额与环境依赖由 Author/Architecture 研究。证据不足时，停止依赖该证据的审查方法修改和效果声明；原测试事实准备、环境恢复与变更前实测继续，不能先改方法后补称 before。

## 7. Canonical 引用与本轮差额

RDT-REQ/DES/TST-KNOWLEDGE 的完整适用读取、阶段复用与最终整合是本批保留约束；拟补约束落点、原前提、自证错误、实施内冲突分流与门禁适用性的行为及测试关系，由原 RDT owner 在 isolated candidate 承接，最终整合再晋升。Architecture FOUNDATION、DOMAIN/INTEGRATION/GOV 和原 change contract 拥有职责、独立审查及判断/事实边界；原 owner 判断具体影响与必要 contribution/ADR，不预建空证明。

长期源为 `trellis/skills/guru-team/packages/` 原 Author/Architecture/Check/Review/task-free 方法、原 evals/adapters、`trellis/workflows/guru-team/workflow.md`、preset/spec/overlays。dogfood/installed 是投影，按原 apply/reapply/drift 同步；源码更新不等于业务安装已采用。具体差额由实际样本及独立候选评估确定。
