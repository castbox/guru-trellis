# Gen1：bootstrap 保留身份比较设计

## 1. 设计目标、需求承接与内容基线

本设计承接[本批 PRD](prd.md) G1-R-01～06、G1-SC-01～05、G1-AC-01～04，以及根 AC-01/03/04/05/06 的本批适用责任。目标是在原判据和原消费者边界内消除 verifier 的身份表示误报，不改变实际工具或发布验收含义。

固定 development baseline B 为 `50b9ffbefca36454363eb7ae1128ed5974cf7ba4`。本批已在 gen1 当前 selection 下通过原只读 constructor 验证，返回的 `base_ref` 为该值。它来自已合并的 gen0 Finish bookkeeping PR841，也是 Planning H0；PR 目标为 `main`。H0 不是最终待审 H，后续 implementation 保 B 并重新用完整实际增量构造 committed Candidate。

当前独立 Architecture candidate_assessment 已实际返回 `baseline_current/no_architecture_impact`：仅对齐两个既有消费者的身份语义，不改变 authority、owner、API/schema、状态、兼容退出或发布门禁。阶段适用 authority 为 B 中的 `docs/architecture/README.md`、`00-foundation/design-constitution.md`（`guru-trellis-design-constitution-v1`）与 `06-governance/change-contract.md`。本结果不代表 final_plan、Approval、实现或完整 Review。

## 2. 当前系统、边界与目标差额

`delivery_upgrade.raw_snapshot(path, include_content=False)` 为 preview 的 artifacts 提供 `sha256/mode`。`_upgrade_bootstrap_fixture` 中的局部 `raw(path)` 另外提供 `content_base64`，供 legacy CorePlan2 file source 等真实调用使用。native tools 和 legacy upgrade 成功后各有一个整字典比较；该比较对相同文件也会因额外字段拒绝。

本批只改 canonical `verify_trellis_compatibility_matrix.py` 的两个比较点，并新增必要的独立行为回归。原 `raw()` 签名和完整返回保持；inventory producer、两分支的准入/执行/返回、artifact 集合和错误阶段保持。代码文件当前 2912 行，改动应局部且不跨入无关重构。

原失败候选、tools 成功输出及同一 bootstrap 文件的实际 hash/mode 均保留；它们证明当前误报原因，不证明尚未实施的修复完成。gen0 两个 Delivery 和终态保持历史事实，本批不重复其交付或安装。

## 3. 来源设计处置（唯一）

| 来源及原承诺 | 处置与实际落点 | 理由、影响和上游处置 |
| --- | --- | --- |
| 私有发布合同 Stage 1：每个准备 Delivery 完整规划、工程、必要整合、TaskCommit、独立 Review、readiness 和交付 | retain；第 6/8 节，implement I1～I5、Policy | 本批同样完整交付，不把 source 修复直接当 Release pass；无来源偏离 |
| 私有合同 Stage 2 existing 及失败回准备、新 fresh main 冻结 | retain；第 7/8 节及 Policy | 两个原比较消费者修正后仍保真实差异拒绝；旧失败 C 不重标，后置实际 existing 由原发布 owner 执行 |
| 私有合同 Local Installation：验证真实 managed source/lock，等价已提交来源不追自引用 HEAD | retain；第 7 节及 implement V3/Docs Plan | helper 不在 managed 映射；仅 helper/test 变化不自动产生新 tools 安装。真实映射变化则回原 owner，而非预填豁免 |
| MIGRATION-794：原 writer、提交前整合、提交后新独立完整 Review/两槽、matching 恢复 | retain；第 6/7 节和 implement I4/I5 | 保原 owners 和真实后继覆盖，不转换 gen0 pass，不新增早期 PR 或重复 Check |
| 原 inventory artifacts 身份及 `raw()` 其他完整 source 消费 | retain；第 4/5 节，V1/V2 | 在消费者处直接对齐原身份，保其他内容消费者，不改 producer/schema 或全局删字段 |
| 根 R-03/04 与当前质量规范：真实差额、必要行为验证、清楚证据边界 | retain；第 8/9 节及唯一 Docs Plan | 回归必须执行原比较，不为文案或固定值自证；组件与 Stage 2 实际安装分别表达 |

没有 change/reject 的规范性来源承诺，没有待上游选择的偏离。PRD 与 implement 引用本矩阵，不另建处置来源。

## 4. 模块、职责与设计取舍

| 模块/owner | 实际行为与改动 | 边界 |
| --- | --- | --- |
| 原 verifier 实施 owner | 在 native、legacy 两个原 post-upgrade artifacts 比较点读取原 `raw()`，将非空 actual snapshot 投影为原 `sha256/mode` 身份后与原 snapshot 比较 | 就地修消费者；不改 `raw()` 的其他用途，不引入公共 helper、adapter 或跨包抽象 |
| 原 preview/inventory producer | 继续输出现有 artifacts 身份和其他 source snapshot | 本批不修改其 API、字段或文件 |
| 原 tools / legacy upgrade owner | 继续按现有 supported path 执行并提供实际结果 | 不改生产机制或状态，不因组件替身声称真实 owner 已执行 |
| 回归实施 owner | 新建 `scripts/python/test_verify_trellis_bootstrap_preservation.py`，通过原 `_upgrade_bootstrap_fixture` 入口观察两个分支、相关组装和拒绝结果 | fixture 只建立入口前状态；外部维护可隔离，原比较不能替换或修补 |
| 原 RDT/Architecture owners | 工程 after 后核既有完整单元是否真实有文义差额；无差额走原 no-change | 不为当前 bug 新建空 contribution、ADR 或共享索引 |

选择消费者身份投影，因为差异出现在这一转换边界。全局移除 `content_base64` 会破坏其他 source 消费；改 producer 会无故扩大公共合同；删比较、固定成功或排除 artifact 会放松原保护。局部直接演进满足当前要求，新增通用转换框架没有当前 consumer。

## 5. 接口与数据

无公共 API、schema 或持久化字段变化。现有流为：原 preview artifacts `{sha256, mode}` → 原分支维护执行 → 局部 `raw()` actual snapshot → 两个原比较点 → 原成功结果或 `MatrixError`。

对 actual snapshot，只在上述两个比较点取 `sha256/mode`；不将 `content_base64` 纳入身份相等判断。文件缺失时仍保原 `raw()` 的空值语义，与原 inventory 不相等并在原检查处失败；不增加缺失容忍。字节或 mode 不同也仍失败。legacy file source 等其他读取仍取得完整 `raw()` 返回，不通过身份投影传递给它们。

native/legacy 的原返回对象、原错误消息、原 artifact 遍历集合和前置 provider/bootstrap 校验不变。本批不新增缓存、checkpoint、恢复协议或异常吞并。

## 6. 状态、顺序、正常与失败流程

1. 本批方案经 Wording、独立 final_plan、Approval 和 Activation 后，原实施 owner 才改源码/测试。
2. 原 verifier 保其 source/provider、单 workspace、无 session、唯一 bootstrap 和 schema 分支前置。
3. native 分支调用原 native tools；legacy 分支保原 CorePlan2 组装与原 upgrade。原 owner 未成功时沿原错误结果停止，不运行一个伪造成功分支。
4. 成功后，在各自原位置遍历完整原 artifacts，按第 5 节比较身份。相同继续，真实缺失/字节/mode 差异在原位置报错。
5. 原工程完成行为验证及最小静态检查，原知识 owners 核 after；全部实际内容经 TaskCommit 和固定 B..H 的新独立完整 Review，再 readiness/Publication/Merge。
6. 原 Completion 重新审本代；Closure no_mutation、Finish/Cleanup 后，Stage 2 才对 fresh main 的新 candidate 执行完整验收与发布。

没有新状态机。常见 source mismatch、非支持 bootstrap、维护失败、真实不保留和 stale 均由原条件/owner 处理；不将它们映射为通过。

## 7. 恢复、兼容、迁移与集成

直接修改受控 consumer，无新兼容层或双读。当前 legacy 分支属于既有调用范围，本批仅保其同一比较和内容 source 行为；不借此扩大历史迁移或完整老版本矩阵。

没有业务数据迁移、生产部署或工具事务改变，因此不新增 rollback。既有工具事务、输出丢失和 Git/PR 恢复仍由原 owner 处理；不修改旧 frozen plan、原失败 C 或旧恢复载体。真实后继代码修复形成后继提交并补受影响审核，不重用旧 candidate pass。

原完整 managed 映射已确认本 helper 非 source/target。实施后还须核新回归文件同样不进入映射，且实际 source lock/managed assets 未变；若不成立，回原 tools/Architecture/Planning。既有真实采用事实只在这些输入/依赖/期望仍适用时采用，不能从相同版本字面推断等价。

## 8. 验证设计

| 验证 | 需求/场景、层次和实际入口 | 预期观察与边界 |
| --- | --- | --- |
| V1 | G1-R-01/03、SC-01/02；新回归通过原 `_upgrade_bootstrap_fixture`，分别建立合法 native 和 legacy fixture，外部维护按组件边界隔离 | 同身份实际完成原比较并返回原成功；legacy 组装的真实 file source 仍含可解码的原内容。不能只测一个自行构造的 identity helper |
| V2 | G1-R-02/04、SC-03；原函数入口后，外部执行边界出现普通 artifact 字节变化或 mode 变化 | 真实差异仍在原比较点抛原 `MatrixError`；两类有独立检测价值。fixture 不排除该 artifact，也不在比较前修回文件 |
| V3 | G1-R-05；原 `managed_source_projections`、实际 changed paths、锁与 managed diff | helper/test 均非投影 source/target，受管资产与锁无新差额；因此没有新增安装写集。该层不声称 new Release existing 已通过 |
| V4 | G1-R-04/06；新回归 module、受影响既有消费者和 `git diff --check`；原知识 after 核对 | 新测试执行真实受改逻辑，覆盖与必要性充分；工程与语义审核分别完成，不扩全 suite 或累计矩阵 |
| V5 | G1-R-06/SC-05；原提交/固定 Candidate/新独立 Review/交付链 | 全部源码、回归及必要文档 after 在自身当前范围；未通过不新 push/PR，原公开两槽真实记录 |

合法 fixture 可以建立调用前必须存在的 bootstrap、inventory 和 source 文件；不得替原比较生成成功结果。维护替身只限测试所声明边界外的动作，返回值不能替代 post-check。legacy 组装断言观察原函数写出的 plan 中真实 source 的解码内容，不复制 `raw()` 算法计算期望。

当前已有原失败与实际身份相等、producer/consumer 源码的充分因果依据；准入后不强制再跑旧冻结候选或固定红绿回退序列。实现后仍必须执行 V1/V2。只有原入口/分支实际是否命中仍不明时，补能回答该问题的最小诊断；充分后停止。Stage 2 的新 fresh candidate 真实 existing/focused/scanner 等仍由原发布 owner 后续执行，不能由本表组件证据替代。

## 9. Canonical 引用、本轮差额与实际未决项

PRD 第 7 节定位 R649/R794、D649/D794、T794、现行 Architecture 与公共质量/因果/减法规则，完整适用条件已读取。它们已有原完整质量链与结果边界，本批是既有 verifier 判据的正确实现，不改变通用生命周期或安装合同。

- [Requirements 当前单元](../../../../../docs/requirements/current/task-delivery-lifecycle.md)：R649/R794 保原结果层次和完整交付责任；本批无新通用需求。
- [Design 当前单元](../../../../../docs/design/current/task-delivery-lifecycle.md)：D649/D794 保原 writer/审核边界；本批只细化本地 consumer 修复。
- [Test 当前单元](../../../../../docs/test/current/task-delivery-lifecycle.md)：T794-06/07 保实际 reviewer、组件、安装和外部证据分层；新行为回归不等于发布验收。
- [Architecture 入口](../../../../../docs/architecture/README.md)及[change contract](../../../../../docs/architecture/06-governance/change-contract.md)：现行 ARCH-DOM-010/ARCH-INT-015 的 owner 与来源/采用关系保持，本批不新增架构贡献。

当前 candidate assessment 无 Architecture impact，不创建 contribution/ADR；原维护 owners 仍须对真实实施 after 判断 no-change 或必要差额。没有预填 final_plan、Approval、实现或 Release 通过。当前没有待用户选择的需求或技术取舍；真实新事实改变 scope、owner 或 managed 边界时回原 owner。
