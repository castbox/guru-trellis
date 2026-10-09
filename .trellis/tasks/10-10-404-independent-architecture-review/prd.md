# #404 独立架构审查与任务必要性约束

## Current requirement authority 与目标
唯一 source authority 为 castbox/guru-trellis #404 的 2026-10-09-r4 正文；评论为零。本文是 task-local 承接，正文冲突时回既有澄清路径，不自行删减 source scope。TaskId 为 404-independent-architecture-review，generation 0，base/delivery target 为 main。
交付“最小充分的架构一致变更”：完整实现当前目标及受影响合同，职责归正确位置，必要调整完整承担，无关目标不接管。五原则正文只读取 current constitution，不复制或增加第六原则。

## 当前缺口与 source provenance
当前 canonical Architecture Skill 的 Public and owner boundary 让当前执行 AI 读 task/planning scope 后自行形成结论；planning-semantic-authoring eval 同样要求完整任务读取，并在 prompt 提前给出 no-impact framing。guru-check-task native authoring adapter 让同一 Agent 先自行 author Architecture 再作整体检查。这些受支持路径尚未落实 fresh independent subagent 与第一轮输入边界。#283/#415 是历史演进证据，不是本任务的完成证明。
业务案例只是非合同历史背景，本任务不修改业务仓或生产。

## Accepted scope
- R404-01：Planning、实际触发的 implementation_discovery、完整 tracked/untracked Phase 2 候选、exact committed base/head/full diff Branch Review 的新 Architecture 结论由真实 fresh subagent 形成。reviewer 未参与当前候选编写/实现，不 full-history fork，不预载完成叙事。no-impact 同样执行评估。
- R404-02：第一轮依次读取 current constitution/baseline、真实候选设计或完整 diff、改变的决策/default/状态/拒绝/依赖/职责、实际消费者及装配、同类能力约束；先独立形成判断，再核对必要解释/contribution。派发摘要不泄漏 PRD、验收、通过结论。task 中独有的必要约束仅取最小事实与来源，缺失时条件性结论或既有 incomplete/blocked。
- R404-03：从实际责任分析共享变化；包括未修改的消费者，不以 owner 自述或设计/代码/测试一致性证明架构合理；区分既有错误和本次扩大，承担必要局部收敛。合法技术语义不因关键词被误报，不审计无关 exported 项。
- R404-04：在扩展修改、测试、severity、修复路由前区分问题成立、当前任务必要、机制合适；以“不做时当前目标/受影响合同在哪里失败”判断必要性。真实架构偏离不因缺功能失败或任务验收条款被压掉。必要重构、调用方适配、旧路径退出须完成，不为最小 diff 留 hack；无关债务不自动进入当前 finding/gate/required follow-up。
- R404-05：红测有限归因为回归、不可分割前置、无关历史、环境或未归因；确认无关后停止，未归因不假称历史。真实必需发布 gate 可阻塞而不扩大修复授权。默认、推荐、合法范围与硬不变量分开，合法非默认配置保留，诊断缺失不新增业务拒绝。
- R404-06：reviewer 自己执行 Architecture semantic authoring、recorder/validator/public wrapper 并返回真实 declared exit；主会话只消费 current 结果与协调修订。fresh worker 可先 Architecture 后读取叙事执行 Check/Branch Review，两项真实结果分开；先读叙事/参与实现 worker 不可回溯补评。
- R404-07：worker 未启动、未完成、结果缺失/候选 mismatch/平台无法合规调度时走已有 blocked/re-entry。Delivery/Completion 消费仍 current 的结果与 eligibility，不因 caller 改变追加同质审查；新候选、stage 或适用事实变化回对应 fresh 独立评估。Branch Review 始终独立评估 committed candidate。promotion 与 finding-fix 新 diff 回原 Phase2/commit/full review。
- R404-08：canonical、dogfood、installed、声明平台投影与入口一致；真实行为验收覆盖派发、读取顺序、判断、停止、wrapper/consumer 接续；静态文本/schema/预填 pass 不替代 native 行为。

## Non-goals 与共享接点
不实施 #382、#383、#464，不重写 #466 Constitution 或 #477 测试价值 authority，不接管 #292 独立 Planning 范围，不恢复旧 Finalizer/Publication/owner writer 安排。不新增 Skill wrapper、审批链、reviewer ledger、第三状态机、授权持久化或长期 transcript；不扩展 adversarial/race/TOCTOU/crash hardening。现有 Architecture 2.0 public I/O、四 profiles、七 exits、promotion owner、唯一 consumer 与 current graph 为集成基线。普通 task 不执行完整累计 Upgrade/Release 安装矩阵。

## 行为验收候选
以下候选在批准前由现有 planning_scenario_set 两项 qualification 接点审查；不以本文件存在代替资格或通过。
| 场景 | 正常入口与观察 | 必须可观察的结果 |
| --- | --- | --- |
| A404-01 | 通用 transport 候选引入业务阶段决策，设计/代码/测试/contribution 一致 | reviewer 从职责与调用链发现新增/恶化，不能被叙事或绿测放行；既有错误扩大只要求必要局部收敛 |
| A404-02 | 共享 default 变化，实际未改调用方；对照合法技术枚举 | 追溯真实消费者；指出变化因果；合法技术语义不过度 finding，不全仓审计无关 exported 项 |
| A404-03 | 必须调用方迁移/旧路径退出的候选，对照独立历史债务 | 必要调整进入当前工作，无关债务只说明且不自动 current finding/gate/follow-up；最小 diff hack 不过关 |
| A404-04 | 当前验证出现红测：回归/前置/历史/环境/未归因 | 有限取证后分别处理/停止/保留未归因；不修改 fixture/超时/映射以追求全绿 |
| A404-05 | 合法显式非默认配置、真正保护不变量、缺诊断标签 | 前两者按已有 authority 正确接受/校验，缺标签不凭空拒绝业务调用 |
| A404-06 | 任务独有约束、约束不足，真实 Planning 候选及无候选 | 只读取必要事实与来源；不足返回现有条件/阻塞；无真实候选不能 pass，authority read 不能代替设计评审 |
| A404-07 | 四评估 stages 的真实 fresh worker 与普通主会话自填结果路径 | 观察 fresh dispatch、无历史/叙事泄漏、实际读取与自主 author/wrapper；主会话自填或 checker green 不能宣称独立 |
| A404-08 | fresh worker 先专项后整体；已暴露叙事/参与实现 worker；no-impact | 合规 worker 可复用，两项真实结果分开；暴露 worker 换 fresh reviewer；no-impact 有实际判断且无无谓 ADR/artifact |
| A404-09 | worker 不可用/缺失/未完成/mismatch、正常 stale/new candidate、promotion diff | 已有 blocked/re-entry 与唯一 consumer 接续；不降级主会话；新候选重审，current Delivery/Completion 不重复，promotion 保留既有 owner |
| A404-10 | apply/reapply、选定平台 package、native 行为与脚本客观检查 | 投影一致、无 sidecar/ownership drift；脚本只证明客观事实；未覆盖 native/平台/完整矩阵如实记录 |

## Delivery 与完成边界
一个 Delivery 完整交付 R404-01..08 与 A404-01..10，包含受影响合同、行为评测、平台安装投影和文档收敛。未验证 accepted 行为不得以“文本已改”声明整个任务完成。Delivery PR 只 Refs #404；merge 不是 Completion，后续 whole-task Completion、source Closure、Finish、Cleanup 仍分别由现有 owner 执行。
