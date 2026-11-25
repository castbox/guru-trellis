# D1 独立审查启动与恢复需求

## 1. 整体来源与术语

本批属于929-review-startup-recovery/g0，Delivery 166dac49-79f1-4190-82e3-fd51ca1915a0，planning_root为本目录。公共scope_ref选整体PRD的R929-01至R929-06，authority为根prd.md的已接受revision；完整定义、来源角色与术语见[整体需求](../../prd.md)第1至8节。

直接来源https://github.com/castbox/guru-trellis/issues/929的交付行为与可执行验收是requirement；其候选改进是advisory。当前Architecture与Review合同为兼容约束；#679原生沙箱样本仅是历史证据。不得以历史pass证明本候选，平台未知保持未知。

## 2. 整体与本批目标、非目标

D1覆盖整体六项要求，交付从fresh reviewer启动到独立正式结果与同候选恢复的完整Guru能力。实现目标是声明权限内可运行、执行条件问题提前暴露、诊断可用、重复前置工作减少，同时保留authority完整、独立判断及合法writer。

本批排除后端源码/Task/session/数据库/进程/部署、上游Codex/provider修补、缓存剪枝、预算遥测体系、审批链/ledger/授权持久化和完整多平台发布矩阵；整体PRD的其他非目标全部适用。

## 3. 本批起点、前序结果、依赖与剩余责任

首次D1，无前序Delivery。起点为main固定63e71ffd72300dee4f5bfdc030c2a5f342b97f32，现有final_plan只读特例和正式Review会话绑定、双槽一次审查与工程事实复用规则保持。Task与accepted_scope已建立，不表示Planning或实现通过。

本批需选择真实最小权限或合法writer分离方案，完成受影响canonical/安装/文档/测试与实际Agent证据。计划一次覆盖全部范围；若技术调查发现独立可延期能力，交原Clarify处理，不静默减少验收。整体Completion要求本批真实验收及后续正式Review结果，不含业务部署/账号恢复。

## 4. 本批调用方、场景与流程

D1-S1：协调者向真实支持载体派发fresh reviewer；输入精确对象、authority定位和工程规则。大规模读取前核实际prelude、固定对象可读、checkout及职责所需权限；不满足则具体失败回原owner，满足才进入authority-first判断。

D1-S2：reviewer读取完整适用authority，再读固定候选和必要消费者，形成独立判断；合法writer产生与原判断、B/H及Task/Delivery匹配的正式结果，候选内容保持只读。

D1-S3：普通中断/结果写入失败/部分投影后原owner补缺。仍合规reviewer优先续审，真实覆盖丢失补足；工程事实按真实依赖采用，无原因不重跑。generic已承担职责则直接执行，无反馈先有界查载体/阶段/结果，沿原恢复/停止出口。

D1-S4：authority入口存在其他任务历史pass时完整当前正文仍可读；历史用于追溯，不当作本次pass，也不一律当作污染。更换入口须保留引用和兼容/迁移。

## 5. 完整行为、条件与约束

D1-R01对应R929-01/S1：预检必须在大规模authority/候选读取前，只读必要工程规则和对象，避免提前任务叙述；核验prelude、commits、checkout和真实职责权限。其成功不生成质量pass、不改变authority-first语义顺序；失败保真实原因及owner。

D1-R02对应R929-02/S2：候选源码、测试及文档只读。确需元数据的writer、目录和最小范围明确且实际验证。若选择只读语义reviewer与正式writer分离，先完成public I/O/provenance/owner兼容设计；协调者或实现者不能补写、更改或制造独立结论。当前候选收敛为保留原writer，由启动者提供并实际验证必要元数据范围；本批不迁移reviewer/writer归属。完整写集及预检方法仍须原Architecture通过。

D1-R03对应R929-03/S3：同未变候选原owner只补未完成步骤；保留真实coverage和适用工程事实。合规reviewer续审，更换时明确丢失范围；没有完整语义coverage不能空写pass，不重复独立gate/审批/全测。

D1-R04对应R929-04/S3：generic/CLI直接执行同一委托，不递归派发同职责。实际未执行或无反馈给可定位信息并走既有blocked/re-entry；底层未知不猜模型或网络，无变化不循环等待新开。不新建常驻调度框架或任意超时阈值。

D1-R05对应R929-05/S4：定义当前authority、导航与历史分工，完整取得必要正文。若拆分保留原历史与引用条件，旧入口兼容或明确迁移；不引入摘要缓存/读过证明/路径剪枝。仅给业务仓采用指引。

D1-R06对应R929-06：稳定official_session_write_failed兼容，最小脱敏操作/位置/异常类别/errno定位真实读写环节，不将projection/旧记录读取失败误报写权限。诊断不含业务、凭证或授权。Markdown判断、脚本事实的边界保持。

## 6. 本批验收、验证方式与未决项

| 验收 | 入口/输入 | 可观察结果 |
| --- | --- | --- |
| D1-AC01→AC929-01 | 可丢弃linked-worktree和真实载体，普通权限遗漏或实际污染prelude | 昂贵读取前具体阻塞/owner，无quality pass；纠正后同候选继续 |
| D1-AC02→AC929-02 | 固定B/H及正常owner生成的Task/Delivery，声明候选只读/最小元数据 | 完整独立审查与真实正式结果一致；若只读拆分，reviewer不写主.git且writer不改判断 |
| D1-AC03→AC929-03 | 同候选正常失败/部分投影/中断恢复 | 采用真实覆盖/适用工程事实，仅补缺步，不空pass/重复gate/无因全测 |
| D1-AC04→AC929-04 | generic真实派发，代表未执行或无反馈条件 | 不递归同职责，有依据诊断并恢复或停止，不无限等/循环新开 |
| D1-AC05→AC929-05 | 含其他任务历史pass的正常authority入口 | 完整当前authority可取且历史可追溯，不误判污染或当前pass；差异定量但不承诺比例 |
| D1-AC06→AC929-06 | 正常入口代表projection/session读写失败 | 稳定码兼容且诊断可区分，敏感内容不泄露；unit不冒充真实sandbox |

使用最小必要真实linked-worktree/Agent和异常诊断、恢复证据，不伪造artifact/pass，不以字符串/DTO/exit0代替行为。现有#679可定位工程事实按条件采用；真实差额单独验证。受影响投影/reapply/drift和迁移需要实际证明，不扩完整矩阵。

当前产品范围无缺口。保留原writer的具体能力检查、完整Review写集、额外委托注入和嵌套worker底因，由Author/Architecture及实现owner调查；实际不能复现保未验证及外部owner，不宣称修复。mechanism定稿前不实质写design/implement或实现。

## 7. Canonical 引用与本轮差额

- docs/requirements/current/task-delivery-lifecycle.md及docs/design/current/task-delivery-lifecycle.md：接收者绑定/选择与正式writer关系；本批将按最终方案维护完整必要定义，未在规划写共享目标。
- docs/test/current/task-delivery-lifecycle.md#t679：采用既有接收者/沙箱证据，补新入口前置失败和恢复差额；历史观察保持。
- trellis/skills/guru-team/runtime/task_lifecycle/session_adapter.py及tests/test_control_stores.py：错误映射与现写失败回归是已确认实现起点，不预选修复手段。
- docs/architecture/README.md、00-foundation/design-constitution.md、06-governance/change-contract.md：项目authority-first、最小owner和变更职责。原独立Architecture先读它们后读候选事实，不预载本PRD。
- trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/references/contract.md与guru-review-branch/references/contract.md：保持独立性、合法purpose入口、一次双槽与既有恢复；实际合同差额在design与原维护owner确定。
