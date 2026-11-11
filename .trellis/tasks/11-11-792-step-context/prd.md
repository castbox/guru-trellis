# #792 按当前步骤提供流程上下文：整体需求

## 1. 来源与术语

| 标识 | 来源与条款 | 角色 | 本 Task 用途 |
| --- | --- | --- | --- |
| SRC-792 | [castbox/guru-trellis#792](https://github.com/castbox/guru-trellis/issues/792)，背景、行为要求1–5、边界与迁移、最小验收 | 唯一 Direct Source；要求及明确的技术约束 | 定义本 Task 的整体交付责任。正文已完整读取，当前无评论。 |
| CUR-GRAPH | [canonical workflow](../../../trellis/workflows/guru-team/workflow.md)，Global Workflow Contract、Integrated Public Graph、Guru Continuation；[registry](../../../trellis/skills/guru-team/registry.json) 及其所选 Interface | 当前实现证据与路由权威 | 复用实际标记、consumer 和公共调用，不建立第二 workflow。 |
| CUR-CONTINUATION | [ADR-035](../../../docs/architecture/adr/035-current-continuation-scope-routing.md)，Decision、精确替代与历史边界、迁移 | 已接受的现行约束 | 保留唯一 continuation、原 producer 恢复与 matching 采用边界。 |
| CUR-QUERY | [runtime discovery](../../../trellis/skills/guru-team/runtime/discovery.py)、[installed validator](../../../trellis/skills/guru-team/runtime/installed.py) 的 workflow_facts；已安装 get_context.py 的 phase、continuation、runtime-contract 入口 | 当前能力证据 | 调查已有查询与校验能力，具体公开入口由 Delivery 规划确定。 |
| PRE-793 | [PR #797](https://github.com/castbox/guru-trellis/pull/797)、[PR #799](https://github.com/castbox/guru-trellis/pull/799) | 已交付事实 | #793 的 qualifier 条件与归档已经合入本 Task 起点；本项不重复修改其条件。 |

术语：consumer 是一个合法 typed exit 的唯一消费方，可能为 Skill、workflow target 或明确 stop。投影是从现有权威确定性派生的当前调用所需内容，不产生新的流程权威。legacy 合同指原维护入口支持的旧状态识别、转换、控制退役或历史恢复合同，不以软件版本号代替适用性判断。

## 2. 背景与问题

本 Task 的调查与创建起点为 `origin/main@05a16a5989669ca216d8ba34b9b419776410f04d`。该起点已包含 #793。

当前 workflow 正文仍包含全量 invoke/exit 标记、router/stop 枚举和多处 legacy 恢复详情。已有 Skill Interface consumer 合同、标记结构校验以及 phase/continuation 查询可以复用，但尚未提供从当前合法出口一次取得唯一 consumer、必要入口及前置合同的完整承接。正常执行者需要查找和读取与当前步骤无关的内容。

期望行为是按当前步骤读取必要流程上下文，同时保留原阶段顺序、语义判断、失败停止和维护能力。文件变短、静态检索命中减少或查询成功均不能单独证明运行效果改善。

## 3. 目标与非目标

整体目标：让正常 Guru 调用方从当前合法出口取得下一步所需的确定性上下文，并只在实际 legacy 入口加载历史详情。

整体承担 R792-01–05、AC792-01–03，以及实际改变的公共调用迁移和受管投影同步。Task Completion 必须检查这些整体义务；某个查询入口可用或某个 Delivery 合并不等于整体完成。

非目标：

- 不改变阶段顺序、原语义门禁、mandatory Skill 的显式调用、typed exit 含义或唯一 consumer 语义。
- 不合并身份查询，不改变 qualifier 触发条件，不实施 #794 的 Check/Review 合并。
- 不以 #736 整体完成为前置，不实施 #734，不承接预算、消息额度、设备治理或事故重放。
- 不重做 #712/#64，不批量转换或退役 Task，不改写历史归档字节。
- 不增加 wrapper Skill、第二 workflow、审计账本、长期位置缓存、用户授权记录或无直接 consumer 的 DTO 字段。
- 不要求固定成本降幅、独立 Agent 评测框架或完整多平台安装、升级、Release 矩阵。

## 4. 真实调用方、场景与流程

| 场景 | 调用方与前置 | 触发动作 | 处理行为与可观察结果 |
| --- | --- | --- | --- |
| S792-01 正常出口接续 | Guru AI 已取得原 owner 的一个合法 typed exit，使用当前 matching 安装 | 从公开查询入口查询该出口 | 一次查询给出与唯一权威一致的 consumer、必要入口及前置合同定位；AI 显式加载并调用原 Skill，原 owner 判断其前置是否满足。 |
| S792-02 无法唯一接续 | 正常更新或调用错误导致 unknown、multiple 或 unmapped 出口 | 调用同一查询入口 | 明确停止并给出该入口的普通错误恢复指引；不猜测 consumer，不以 fallback 继续。 |
| S792-03 正常阶段加载 | 正常新会话或接续入口需要当前阶段上下文 | 加载阶段及全局约束 | 不再要求读取无关的全量 router/stop 表或历史恢复详情；适用的全局约束和 mandatory invocation 仍可获得并执行。 |
| S792-04 实际 legacy 维护 | 原入口识别到其支持的旧状态，或用户明确选择相应维护操作 | 沿现有路由进入原维护 owner | 正常入口提供最短识别及转交说明；实际 owner 加载其必要旧合同及准确来源，保持原支持与停止边界。 |
| S792-05 权威与安装演进 | 后续合法路由变化，或已有项目采用本项修改 | 通过同一权威更新并沿原安装 owner 同步 | 查询自然反映当前权威；受影响 canonical、dogfood 和声明平台入口一致，受支持在途工作可沿明确迁移合同恢复。 |

## 5. 行为要求

### R792-01 单一权威与确定性投影

保持全局顺序、mandatory invocation、typed exits 与唯一 consumer 的单一长期权威。复用现有标记和 consumer 合同，通过既有 runtime/get_context 的入口提供确定性投影。具体入口由 Delivery 规划根据现有能力确定，不预设新 wrapper 或第二 workflow。承接 S792-01、S792-05；来源为 SRC-792 行为1。

### R792-02 一次查询与明确停止

AI 取得一个合法出口后，一次公开查询必须定位其唯一 consumer、必要入口及前置合同。前置是否满足、下一原 owner 的 scope 和充分性判断仍由 AI 负责。unknown、multiple、unmapped 必须明确停止；脚本不得猜测路由意图或替代 owner 的语义选择。承接 S792-01、S792-02；来源为 SRC-792 行为2。

### R792-03 正常入口按当前步骤加载

将全量 router/stop 枚举移出正常执行必读正文。正常入口加载当前阶段所需投影及适用全局约束。投影必须从同一权威派生，不能依赖手工维护副本或长期位置缓存。保留 mandatory Skill 的显式加载和调用；不能用 frontmatter 自动匹配或脚本返回值代替。承接 S792-03、S792-05；来源为 SRC-792 行为3。

### R792-04 legacy 详情按实际入口加载

正常流程只保留识别旧状态及转交原维护 owner 的最短说明。具体 legacy 家族、转换、控制退役和历史恢复合同在实际入口加载，原支持边界及准确来源必须继续可获得。不得按版本号一刀切，不批量转换或退役用户 Task，不改历史归档字节，不重做 #712/#64。承接 S792-04；来源为 SRC-792 行为4。

### R792-05 查询合同、迁移与分发

新增或改变的查询入口必须说明实际前置、最小输入、输出的直接消费方和普通错误恢复。未来路由变化继续通过同一权威承接，不要求等待其他拆分项。

实际改变的公共 id、schema、命令、typed exit 或 consumer 必须提供明确迁移合同，并保留受支持在途 Task 的合法恢复。canonical、dogfood 与实际受影响的声明平台，包括 Claude Code、Codex，沿原安装 owner 同步。只改变源码不能证明实际安装已采用。承接 S792-02、S792-05；来源为 SRC-792 行为5、边界与迁移。

## 6. 约束与依赖

- Markdown 与原 AI owner 拥有意图、适用性、前置充分性、finding、pass/block 和 route intent 判断；脚本只做确定性查询、投影和客观校验。
- 复用 #713 已交付的公开调用与必要恢复能力。若发现具体依赖缺口，只阻塞依赖该缺口的工作，不制造空结果或替代 owner。
- 当前 #793 交付作为基线事实保留；#794 是后继独立工作，不成为本项验收或阻塞条件。
- 只有诚实正常路径、普通操作失误、外部状态演进、stale/mismatch 与 correctness/compatibility 边界属于本项。不得用故意伪造或篡改 artifact/state 构造范围内 finding，不新增竞态压力、锁、TOCTOU、crash consistency 或额外 fault injection 机制。
- 遵守官方 workflow marketplace 与 preset/overlay 扩展边界，不修改 Trellis 上游源码、全局 npm 包、node_modules 或 upstream-owned 入口来实现流程分叉。
- 活动 Task 及 session 由原工具维护 owner 保留并同步；普通 apply 阻塞不授权绕过、手工覆盖受管副本或迁移无关历史。实际 sidecar 由原 owner 处理。
- 不持久化用户授权。公共 output 只携带有明确直接 consumer 的最小 handoff；本 Task 不新增跨阶段审计链。
- 本项没有业务服务、数据库或生产部署需求，不为填充模板新增这些接口或迁移。具体查询输入输出及兼容差额在选定 Delivery 的设计中展开。

## 7. 可观察验收与验证方式

| 验收 | 对应要求与场景 | 验证入口、输入及预期可观察结果 | 证据边界 |
| --- | --- | --- | --- |
| AC792-01 查询与停止 | R792-01、02、05；S792-01、02、05 | 经本项公开查询入口提交真实合法出口，核 consumer、必要入口与原权威一致，并实际承接改变的消费路径。对普通未知、多重、未映射状态核明确停止及原恢复。对同一权威的合法演进核查询自然更新。 | 只验证实际改变的查询和消费路径；结构校验或手写期望 DTO 不能替代公开入口行为。 |
| AC792-02 加载与维护可达 | R792-03、04；S792-03、04 | 审核正常阶段及实际 legacy 入口的加载引用，观察当前步骤能取得必要内容，正常路径不再要求无关全表或历史详情，原维护合同及准确来源仍可达。 | 不以关键词数量、文件长度或源码分发一致代替加载语义判断；按实际观察分别说明静态、installed 与 Agent 行为范围。 |
| AC792-03 受管投影与采用 | R792-05；S792-05 | 沿原安装 owner 同步实际受影响投影，核 canonical/dogfood/所选平台一致，执行必要 dogfood drift 与变更涉及的 reapply/sidecar 定向检查。 | 不宣称其他业务安装已采用；不扩张为完整多平台安装、upgrade/update 或 Release 矩阵。 |

具体用例与命令由 Delivery 规划根据真实入口、变化和已有覆盖确定。验证必须能发现对应行为缺陷；不通过比较固定声明与其副本来证明路由或加载正确。未执行验证保持未验证，不预填通过。

## 8. 实际未决项

当前无必要的需求、范围或验收未决项。具体查询入口、投影组织和 legacy 正文的目标位置由原 Author/Architecture 在 Delivery 规划中确定；这些尚未完成的技术选择不等于需求缺失。

本 PRD 的写作和 scope 接受不证明实现、安装效果、生产效能或成本改善。原 Clarify 接受整体 scope 后，才进入明确 Delivery 的独立规划；当前没有 Delivery 方案或实现结果可供批准。
