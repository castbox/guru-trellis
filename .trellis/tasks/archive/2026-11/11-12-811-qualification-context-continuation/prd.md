# #811 资格确认 context 正式接续：整体需求

## 1. 来源与术语

| 来源 | 章节/角色 | 用途 |
| --- | --- | --- |
| [Direct Source #811](https://github.com/castbox/guru-trellis/issues/811) | 完整正文；2026-11-12T13:06:20Z；要求 | 本 Task 的完整行为、独立正常场景验收与交付边界；`exact_source`。 |
| 当前协作边界 | 工作与交付约束 | 保留同一 Task/gen0/D1、固定 B 和既有工作；每次 merge 前交协调方处置。 |
| [业务 PR #820](https://github.com/castbox/guru-trellis/pull/820)、[归档 PR #821](https://github.com/castbox/guru-trellis/pull/821) | #812 已合并结果；事实 | 复用已交付的 explicit-task 资格入口，不重复实施。 |
| `trellis/skills/guru-team/packages/guru-discover-change-context/references/contract.md` | Caller-aware context requests；当前合同 | 旧四类返回、原 producer 职责和迁移起点。 |
| `trellis/skills/guru-team/packages/guru-clarify-requirements/references/contract.md` | 资格确认、公共调用与 source authority；当前合同 | 保留原语义门禁与原 caller 返回。 |

`context` 是原 Discovery producer 正式返回的当前上下文及公共 transition。
`target` 是当前资格确认对象；Task target 不等于来源 Issue authority。
`record/check` 仅记录或校验，不能替代公共 `invoke` 出口。
Task、Delivery、continuation 和 resume consumer 均沿原调用对象保留。

## 2. 背景与问题

#811 记录既有 Task 原执行会话的正常失败：D1 的 `implementation_discovery` 得到真实
`scope_confirmation_required`。Clarify record/check 通过，公共 invoke 却先因缺少
`invocation.transition` 返回 `schema_mismatch`；使用旧 Issue URL / `stage0-current`
context 后，又因 Task 目标及资格确认 continuation 不同而返回 `stale_identity`。

Intake 固定在 `origin/main@ca0b21f0dfc754a6979f919be14deee696719a4b`，包含 #812 业务及归档合并。
当前 Discovery `context_request` 2.0 的 `return_identity` 只有 standard、reviewed-plan、
active-task 和 standalone 四类。当前合同让两类资格确认回原 qualifier 修复 context，
没有完成取得匹配 context 的正式循环。本项要补真实接续，保留 stale/mismatch 检查。

## 3. 目标与非目标

整体目标：两类资格确认从真实 qualifier 公共输出进入原 Clarify，经原 context producer
获取或刷新 context，完成真实确认，再通过正式 `clear` 返回原 caller。

承担两类确认、Task target 与来源 Issue authority 的关系、旧四类回归、明确版本迁移、
canonical/受管 dogfood/声明平台同步，以及本项独立正常 Task/Delivery 场景的实际公共链接续验收。
整体完成还须有完整 Check、提交后独立完整 Review、readiness、业务交付、整体 Completion、
正确 Closure、必要 Finish 归档与资源 disposition，并核实 merge result 在 live main 可达。

不绑定特定发布 Issue、版本、发布时间或外部 Task，不实施后续 Issue。
不增加授权存储、审计 ledger、第二路由 authority、攻击或故意篡改防御、压力锁、crash 或并发加固。
普通定向验证不扩为完整多平台安装、升级或 Release 矩阵。

## 4. 真实调用方、场景与流程

| 场景 | 调用方与前置 | 动作及可观察结果 |
| --- | --- | --- |
| S811-01 当前 context | 原 caller 已获真实 normal 或 solution qualifier 确认出口，context 与原对象匹配 | Clarify 使用当前真实 context 完成确认；正式 clear 保留候选、目标、mode、Task/Delivery、continuation 和原 resume consumer。 |
| S811-02 缺失 context | 同一真实 qualifier 出口，没有匹配 context | 经声明公共路径请求原 producer；真实返回重新进入原确认 profile，不能预填 transition 或复制示例。 |
| S811-03 正常过期 context | 同一对象 context 因正常来源或身份变化而过期 | 原 owner 刷新受影响事实，再走同一循环；保留 stale/mismatch 拒绝，不改旧 transition 取得通过。 |
| S811-04 旧四类 | standard、reviewed-plan、active-task、standalone 的原合法入口 | 保留各自 target、profile、continuation、source locators 或 task/standalone consumer，及原成功、刷新和 fail-closed 行为。 |
| S811-05 独立同工作接续 | 本项独立、受支持的正常场景已通过原入口建立合法 Task/generation/Delivery，caller 持有其真实资格确认对象 | 从真实 qualifier 公共输出经过原 context producer 与正式 clear 返回原 caller，后续消费仍属于同一工作和场景身份；不指定发布 Task，不捏造未决范围选择。 |

两类确认逐项覆盖 S811-01..03。不得以手工修改 artifact/hash/state 构造正常验收。

## 5. 行为要求

- **R811-01 真实入口与返回**：承接 normal 确认的真实 qualifier 输出；由原 Clarify、原 context producer 和原 caller 完成循环。公共结果来自实际 invoke，record/check 不算正式出口。（来源要求1、验收）
- **R811-02 同一对象**：获取、刷新及返回保留原候选、Task/Delivery、mode、target、continuation、resume consumer。明确 Task target 与来源 Issue authority 的关系；不改写旧 Issue context 为新 Task context。（来源要求1、2）
- **R811-03 两类行为**：核对并承接 solution 确认的同一合法路径；原 owner 的语义职责保持，normal 结论不能代替 solution 判断。（来源要求3）
- **R811-04 版本兼容**：保留旧四类返回、Skill/exit ID 和 fail-closed 语义。实质 I/O 变化采用明确版本和迁移合同；说明支持集合、在途操作、采用和恢复，不静默改旧语义。（来源要求4、交付边界）
- **R811-05 判断与事实分层**：Markdown 定义 AI 判断及路由；脚本仅执行确定性投影、记录、校验和事实动作。保留原语义门禁、事实校验及已完成历史，不持久化授权或过程。（来源交付边界）
- **R811-06 分发与回归**：同步 canonical、受管 dogfood 及声明平台投影，经原安装 owner 验证。完整 producer→consumer 回归不能预填被测 producer 的结果。（来源验收、交付边界）
- **R811-07 独立同工作验收与交付**：使用 S811-05 独立正常 Task/Delivery 场景验证同一工作的正式接续，保留场景内真实身份。按本项要求完成交付、关闭、必要归档，并核实 merge result 在 live main 可达；不绑定发布对象或发布时间。fixture 的语义输入与实际 producer 输出分别陈述，不额外要求实际 Agent 或远端业务证明，不捏造未决范围选择。（来源验收及交付边界）

## 6. 约束与依赖

本 Task 为 `811-qualification-context-continuation`、gen0；集成与未来 PR 目标为 `main`。
固定 Git 起点不因 primary main 落后或共享 fetch 而改变；实际依赖/冲突才进入原 Reconcile。

完整公共 Skill package 合同、当前公共 schema/Interface/投影和直接 consumer 是方案约束。
具体字段、版本及薄投影由原 Author/Architecture 在 D1 设计中确定；整体需求不预设第二实现路径。
每次 source/test/task 写入前校验当前 checkout；现有安装由匹配 tools owner 更新，不手工覆盖受管副本。

接续验收由本项独立正常场景完成，不依赖其他 Task、版本发布或外部会话进度。
fixture 只建立声明边界前的合法对象和语义输入；被测 qualifier、context、clear 及后续消费必须真实执行。
原 Check owner 按当前验收判断组合证据充分性，不将 fixture 判定输入冒充实际 Agent 判断或远端副作用。
本项无服务部署、数据库或产品前端；方案出现新的实质责任时沿原 owner 判断，不自行加入验收。

## 7. 可观察验收与验证方式

| 验收 | 对应要求/场景 | 入口、输入及预期观察 |
| --- | --- | --- |
| AC811-01 | R811-01/02；S811-01..03 normal | 真实 normal qualifier 输出进入 Clarify；当前、缺失、正常过期 context 分别经原 producer 实际返回，完成正式 clear，原 caller 实际消费。 |
| AC811-02 | R811-02/03；S811-01..03 solution | 同上，使用真实 solution qualifier 出口；保留原候选及全部 continuation identity。 |
| AC811-03 | R811-04；S811-04 | 旧四类公共入口和返回回归通过；必要正常 stale/mismatch 仍拒绝；公开 ID 与迁移支持边界可核对。 |
| AC811-04 | R811-01/05/06 | 完整回归实际调用被测 producer，不预填结果；私有函数、record/check 或 fixture 自身不能代替正式出口；各项证据层级分别报告。 |
| AC811-05 | R811-06 | 原安装 owner 同步后，source/installed package、dogfood/平台投影、定向 reapply/drift 和实际 sidecar 处置满足本变更，不宣称完整矩阵通过。 |
| AC811-06 | R811-07；S811-05 | 本项独立正常 Task/Delivery 公共链从两类真实 qualifier 输出，经真实 context producer 和正式 clear 返回并由原 caller 消费；同一工作身份保持。无指定发布 Task、版本或时间前置；fixture 语义输入及实际输出边界明确，不预填 producer 结果或捏造未决选择。 |
| AC811-07 | R811-01..07 | 固定已提交完整候选由独立 reviewer 完成 Check/Review；readiness 与整体 Completion 覆盖上述真实义务，不以单一测试通过代替整体完成。 |
| AC811-08 | R811-07 | 原交付、Closure、Finish 与资源 owner 完成其结果；live #811 正确关闭，业务和必要归档 merge result 在 live main 可达；每次 merge 前交协调方处置。 |

以上为待执行验收，Intake 与 Task 创建不证明它们通过。

## 8. 实际未决项

整体行为和兼容范围清楚，没有需要追加的产品选择。本轮仅收敛验收对象和外部依赖，
D1 已有 schema/版本、context bootstrap 与薄投影由原 Author/Architecture 按受影响范围复核，既有实现和有效工程事实保留。
独立公共链的组合证据仍由原 Check owner 按当前验收判断；正式 Check/Review、交付与整体终态尚未完成。
完整多平台矩阵和生产效果不在本项结论内。
