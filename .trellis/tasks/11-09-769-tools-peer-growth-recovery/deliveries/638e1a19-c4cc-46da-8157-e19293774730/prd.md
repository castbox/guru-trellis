# D1 tools-only peer 增长与原事务兼容恢复需求

## 1. 整体来源与术语

本批消费 [整体PRD](../../prd.md) 的当前 accepted_scope，覆盖 R1–R6、AC1–AC4。Direct Source 为 [#769](https://github.com/castbox/guru-trellis/issues/769) 当前完整正文：目标与行为、范围与兼容边界及验收均是要求；背景是已核实现场事实，不是 Task 已完成结论。

peer、原观测、原事务和新增 peer 的含义沿整体PRD第1节。本批的 DeliveryKey 为 `769-tools-peer-growth-recovery / 0 / 638e1a19-c4cc-46da-8157-e19293774730`，只在本 planning_root 写本批规划。

## 2. 整体与本批目标、非目标

本批完整交付共享 peer 保持检查的增长处理、修复前事务的明示兼容恢复、定向回归和真实 #766 原事务恢复。只修比较而不能恢复已经被卡住的操作，不能满足本批目标。

不修改 #766 schema 修复或其 accepted_scope；不替代 #759 prunable 缺 .git 的精确条件。不 prune/删除/取消注册/写改其它 worktree，不重 prepare 或刷新原备份，不增加锁、TOCTOU、攻击、压力、额外故障注入、通用事务迁移平台或全多平台升级/Release矩阵。

## 3. 本批起点、前序结果、依赖与剩余责任

首个 Delivery，无前序交付。开发基线 B 为 `main@a5f3ceeabbaccddae65935d97763f5a798f71ca9`，已含 #759；PR 目标为 main。原 `unchanged_peers` 对整字典作相等比较。check_source 仍绑定原 source HEAD/tree token。

依赖原 public maintenance API、冻结源/计划/preimages、managed Python、preset 原投影/验证 owner。#766 原事务是本批真实恢复验收对象，不能因工具修复源码通过而略去。#766 后续 Check/Review/PR/Task闭环由它自己的原 owner 承担。本批没有延期功能切片；整体 Completion仍独立核全部AC和真实交付事实。

## 4. 本批调用方、场景与流程

- D1-S1：tools install 已冻结单目标写集；其它诚实工作正常新增独立 registered peer。检查原观测保持和新增 peer 隔离，目标验证通过后返回工具结果，新增键本身不阻塞。
- D1-S2：同一当前源操作在新增 peer 后 resume 或 rollback。保留原 ref/plan/preimages，新增 peer 不进入备份/写入/删除集，既有保持条件继续有效。
- D1-S3：原 common/peer 指针或已成立合法选择真实变化。继续拒绝错误接续，不吸收该变化或刷新恢复锚点。
- D1-S4：修复前源的原事务已投影工具，却因新增 peer 阻塞。通过明示兼容入口验证旧事务/原资产源和实际目标，恢复同一操作；不能靠修改旧源、手改 checkpoint、重新 prepare 或重装冒充恢复。

## 5. 完整行为、条件与约束

- R1：install/resume/rollback 区分旧观测值保持与新增 peer，不因仅增加字典键而误拒绝。
- R2：原 common/peer 保持检查继续执行；新增 peer 须与实际目标工具写集隔离，其工具、指针和业务内容均不由本操作写入或纳入备份/删除。
- R3：修复前因本缺陷阻塞的旧操作具有明确兼容恢复路径；保持同一 recovery_ref、public operation/plan、Guru preimages、原资产 source 内容绑定和 rollback anchor。
- R4：兼容路径明确修复执行代码与原资产源的关系，验证原固定事实；原源/目标/owned内容真实不匹配仍阻塞。不重新 prepare、不扩大备份、不接受后续业务编辑。
- R5：目标 own resolver/installed/native、原 peer 保持和新增 peer 隔离分别证明；工具结果不提供 Task/Delivery gate 或 Completion。
- R6：原 canonical/tools/preset 分发和 managed provenance 继续；公共输入新增须有兼容合同，既有 profile/exit 不静默改义。Markdown负责AI判断，脚本只验证/执行事实。

本来源没有强制具体算法或新 profile 名称。候选机制由 Author提出并先经独立 Architecture；design第3节维护唯一来源处置。无业务数据迁移或 Task转换需求。

## 6. 本批验收、验证方式与未决项

| AC | 要求/场景 | 入口、输入和独立观察 |
| --- | --- | --- |
| AC1 | R1/R2；D1-S1/S2 | 真实Git worktree通过原观测入口形成before，正常新增独立peer后检查通过；核写集隔离和peer bytes/modes不变。 |
| AC2 | R2/R4；D1-S3 | 原peer指针/合法选择普通变化仍拒绝，原preimages不变；复用受影响回归。 |
| AC3 | R3/R4/R5；D1-S4 | 原owner真实创建的事务经明确兼容入口恢复；核ref/public operation/plan/preimages/source不变、无reprepare。实际#766同操作必须恢复成功。 |
| AC4 | R5/R6 | 定向tools/recovery测试、source/installed、dogfood drift、mode/sidecar和实际目标自身resolver/installed/native；不以源码或fixture通过代替现场恢复。 |

目前没有产品范围未决项。候选机制尚需独立 Architecture 审查，不提前宣称修复或验收通过。完整多平台升级/Release和#766业务交付由各自原owner负责。

## 7. Canonical 引用与本轮差额

- `docs/requirements/current/runtime-location.md` R718-03/11、对应Design D718-03/06及Test T718-06：保留单目标维护、源/目标区分、peer保持与原rollback。新peer增长/旧投影恢复的精确差额由原package/migration承接，RDT策略由方案判断。
- `trellis/skills/guru-team/packages/guru-upgrade-tools/references/contract.md` Same-operation resume and rollback：原固定计划/来源/备份与目标验证，兼容扩展必须明示边界。
- `trellis/skills/guru-team/packages/guru-upgrade-tools/runtime/tools_owner.py` 及 `tests/test_recovery.py`、`tests/test_contract.py`：现有判断、消费者和已包含#759的回归。
- `.trellis/spec/workflow/quality-guidelines.md` 的 Test And Validation Value / Validation Scope Ownership、`companion-scripts.md` 的确定性脚本边界、`clear-technical-writing.md`：本批执行与验证约束。
- `docs/architecture/README.md`、`00-foundation/design-constitution.md`、`06-governance/change-contract.md`：独立Architecture authority；本批尚不声称无影响或已晋升。
