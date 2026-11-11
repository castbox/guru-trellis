# D1：按当前出口查询与按步加载

## 1. 整体来源与术语

本批属于 Task `792-step-context` / generation `0`，Delivery 为 `4a341415-1863-4308-b8ec-336121e859d3`，profile 为 `pull_request`。公共 `scope_ref` 的 authority 是 [整体 PRD](../../prd.md)，选定 R792-01–05 与 AC792-01–03；实际 revision 与当前阶段从 [Task 公共记录](../../task.json) 读取。本批规划目录为当前 Delivery 的 `planning_root`。

| 来源 | 条款及角色 | 本批用途 |
| --- | --- | --- |
| [Issue #792](https://github.com/castbox/guru-trellis/issues/792) | 全文；原 Clarify 选择为 requirement | 五项行为、兼容与最小验收的唯一 Direct Source。 |
| [整体 PRD](../../prd.md) | 第4–7节；已接受整体要求 | 本批完整承担其场景、要求和验收；第3节非目标与第6节约束全部适用。 |
| [canonical workflow](../../../../../trellis/workflows/guru-team/workflow.md) 与 [Skill registry](../../../../../trellis/skills/guru-team/registry.json) 所选 Interfaces | Global Workflow Contract、Integrated Public Graph、Guru Continuation；现行执行合同 | 保持唯一图、显式调用、原 typed exits 与语义 owner。 |
| [ADR-035](../../../../../docs/architecture/adr/035-current-continuation-scope-routing.md) | Decision、迁移；现行约束 | 保留接收会话检查、唯一 continuation 与原 producer 恢复，不从 phase 推断通过。 |

consumer、投影与 legacy 的定义沿整体 PRD 第1节。一次查询指调用方已经持有一个原 owner 的合法出口后，通过公开查询取得其直接 consumer 与必要入口/前置定位；查询不代替 consumer 的语义执行。

## 2. 整体与本批目标、非目标

当前完整 workflow 中的全表与历史细节增加了正常执行的查找和无关读取。本批独立交付按当前出口查询及按当前步骤加载的完整能力，同时保留原维护能力。

D1 覆盖整体全部 R792 与 AC792。查询改造、正常入口改造、legacy 按需加载、迁移和实际受影响投影共同交付，不将其中任何一项留为未分配的必需后继。

整体 PRD 第3节全部非目标保持：不改阶段或原 gate，不合并身份查询、qualifier、Check/Review，不重做旧迁移，不改历史归档，不承接 #734 或完整安装矩阵。文件长度减少不单独证明效果。

## 3. 本批起点、前序结果、依赖与剩余责任

本 Task 尚无前序 Delivery。D1 起点为 Git `05a16a5989669ca216d8ba34b9b419776410f04d`，工作分支为 `codex/792-step-context`，交付目标为 `castbox/guru-trellis/main`。该起点含 #793 业务 PR #797 及归档 PR #799；这些是外部前置交付事实，不是本 Task 的 D0 或本批 gate。

复用现有 Interface/registry、workflow 标记、`discover-skill-contract` 及 get_context 的 phase/continuation 能力。已有 installed validator 校验 invoke、exit 和 target 与声明一致；现有 native continuation 测试只支持其实际提取边界，不代表本项验收通过。

具体 #713 provider 缺口只阻塞其真正依赖项。原 tools owner 负责同 checkout 的 matching 同步并保留 Task/session。无本批之外已分配的实现责任；D1 结束后整体 Completion 仍须判断全部要求、迁移及验收证据是否实际完成。发布、merge、Issue Closure 和 Finish 分属后续原 owners。

## 4. 本批调用方、场景与流程

| 场景 | 调用方、前置及动作 | 本批行为和结果 |
| --- | --- | --- |
| D1-S1 正常接续 | Guru AI 持有当前合法 typed exit，调用公开查询 | 得到唯一 consumer、必要入口及前置合同定位，按 stable Skill id 显式加载并调用；原 AI owner 判断是否满足前置。 |
| D1-S2 普通路由错误 | 正常更新或调用错误带来 unknown、multiple 或 unmapped 出口 | 查询明确停止，给出对应普通错误恢复，不猜测路由或语义。 |
| D1-S3 正常阶段读取 | 新会话或恢复入口加载当前阶段上下文 | 取得当前所需投影及适用全局约束，不再要求无关全表或 legacy 详情；phase 仍只表示可用阶段，不表示原门禁通过。 |
| D1-S4 维护进入 | 识别支持的旧状态，或明确选择原 legacy 维护操作 | 正常入口最短识别并转交原 owner；实际入口加载必要历史合同和准确来源，原支持/停止条件保持。 |
| D1-S5 更新采用 | 同一权威发生合法路由变化，或项目安装本项修改 | 查询从实际权威自然反映变化；matching canonical、dogfood 与受影响平台同步，在途原工作按迁移继续。 |

S1–S5 分别承接整体 S792-01–05。整个顺序是“原 owner 正式出口 → 确定性上下文查询 → 原 consumer 语义入口”；脚本结果不直接产生下游 pass。

## 5. 完整行为、条件与约束

| 本批要求 | 具体承诺 | 整体来源与场景 |
| --- | --- | --- |
| D1-R1 | 复用现有标记与 consumer 合同，从同一长期权威派生上下文；保留全局顺序、mandatory invocation、typed exits 和唯一 consumer。不新增第二 workflow、手工副本或长期位置缓存。 | R792-01、03；S1、S3、S5 |
| D1-R2 | 公开一次查询必须给出合法出口的 consumer、必要入口和前置合同。unknown、multiple、unmapped 明确停止。前置充分性、scope 与 route intent 仍归原 AI owner。 | R792-02；S1、S2 |
| D1-R3 | 全量 router/stop 枚举退出正常必读正文，正常入口只加载当前步骤所需内容及适用全局约束。mandatory Skill 必须仍被明确加载和调用，不能由自动匹配代替。 | R792-03；S3 |
| D1-R4 | 正常路径只保留旧状态识别和原维护 owner 转交的最短说明。legacy 家族、转换、控制退役及历史恢复详情在实际入口加载；原支持边界及准确来源可达。不按版本号一刀切，不批量变更 Task，不改历史归档。 | R792-04；S4 |
| D1-R5 | 查询前置、最小输入、输出直接消费和普通错误恢复须可执行。改变的公共调用提供明确 matching 迁移及在途恢复；沿原 owner 同步实际受影响的受管投影，包括 Claude Code、Codex。未来路由变化不要求等待其他拆分项。 | R792-05；S2、S5 |

整体第6节约束全部适用。新增场景、保护机制、业务 authority、持久化或恢复范围如超出当前约束，回原 qualification/Architecture/Clarify；不得以查询或导航名义隐藏其变化。候选只是确定性读取和文本导航时，原 caller 按三个 qualifier 的短适用合同判断，不制造空调用。

源要求中已约定“复用既有 runtime/get_context 与标记/consumer”的技术边界必须保留；具体设计及唯一来源设计处置在本 Delivery design 第3节维护。本 PRD 不提前写 substantive solution。

## 6. 本批验收、验证方式与未决项

| 验收 | 输入、入口与预期观察 | 对应整体义务 |
| --- | --- | --- |
| D1-AC1 | 经本项公开入口输入真实合法出口，实际消费其投影并核对唯一权威；普通未知、多重、未映射错误停止。合法路由演进后的投影由同一权威更新。 | AC792-01；D1-R1、R2、R5 |
| D1-AC2 | 审核并观察改变的正常阶段与实际维护入口：当前所需内容可用，正常路径不要求无关全表/历史详情，原维护合同及来源仍可达。 | AC792-02；D1-R3、R4 |
| D1-AC3 | 原安装 owner 完成实际受影响投影同步；source/installed 与受影响平台、dogfood drift、必要 reapply/sidecar 定向检查证明分发及采用的实际层次。 | AC792-03；D1-R5 |

测试与观察从要求、真实消费路径和变化推导。复用适用的现有覆盖，补实际缺口，不以声明副本比较或计数证明行为。实际 Agent、确定性查询和安装投影证据分别报告；不添加固定评测框架或完整平台矩阵。

当前无需求或范围未决项。查询入口和正文分离方式由下一候选评估/方案阶段确定；本阶段不能预填实现、性能、生产或费用通过。

## 7. Canonical 引用与本轮差额

- requirement/behavior：[整体 PRD](../../prd.md) 与 live #792；本批承担全部选定要求，未选择新的整体范围。
- design：[canonical workflow](../../../../../trellis/workflows/guru-team/workflow.md) 的全局图/continuation，以及 [runtime discovery](../../../../../trellis/skills/guru-team/runtime/discovery.py)、[installed validator](../../../../../trellis/skills/guru-team/runtime/installed.py)；差额是按出口公开投影及正常必读/维护按需读取组织，不转移 AI 判断。
- test：[native continuation 定向测试](../../../../../trellis/skills/guru-team/tests/test_active_task_continuation_integration.py) 及原 runtime discovery 覆盖；下一方案选择公开查询、真实 consumer 与加载观察的必要增量，现有局部绿色不预判新路径。
- Architecture：[ADR-035](../../../../../docs/architecture/adr/035-current-continuation-scope-routing.md)、[Constitution](../../../../../docs/architecture/00-foundation/design-constitution.md)、[change contract](../../../../../docs/architecture/06-governance/change-contract.md)。候选必须先由原独立 Architecture owner 评估，后续方案再承接其实际输出。共享知识如需更新，先准备隔离完整候选，最终整合仍归原 maintenance owners。
