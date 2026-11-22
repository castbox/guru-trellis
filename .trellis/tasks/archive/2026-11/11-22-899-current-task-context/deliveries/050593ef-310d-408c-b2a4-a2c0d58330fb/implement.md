# D1 实施与验证计划

## 1. 输入与引用

以本批 PRD、已接受整体范围 AC1/AC2 和本批 design 为输入。固定开发起点见 design §1。当前标准续接和恢复边界见 `.trellis/workflow.md` 的 explicit receiving session 与 bound formal Task 两节。公共 Delivery 读取沿 `.trellis/delivery-contract.md` 的现有协议。

## 2. 步骤与文件责任

1. 从标准入口记录当前调用和实际输出。读取上游 session/Delivery 查询及 Guru Identity、Ensure、Bind 的真实依赖。确定哪些共同读能力可直接调用，哪些需要最小提取。
2. 在 canonical Guru runtime 编写只读组合和公开 launcher。用同一个调用处理现有绑定、显式只读、无 Task 和原诊断。保留原公共命令。复用事实前比较同一会话的当前依赖，将受影响值替换为新读取结果。
3. 修改 canonical workflow 的标准接续消费，用解析结果定位精确 Delivery，保持按阶段分流前读取官方 record 和 gate applicability。存在 Publication PR 时，先由原 repo-bound 入口核实 GitHub 状态，继续适用的 Merge recovery 或普通分流。保留原 owners 处理阶段义务、恢复和写入。同步 README 中最小调用、输出、诊断和迁移说明。通过 matching 更新 owner 和原生成方式同步 dogfood、声明平台投影及受管 manifest。
4. 运行下面的定向验证。按原 RDT 和 Architecture owners 整合已验证的知识差额，读回所有实际文档后进入 TaskCommit 与一次独立完整 Review。

## 3. 验证入口、输入与预期观察

| 检查 | 入口与观察 |
| --- | --- |
| V1 正常路径 | 使用匹配安装和真实 Task、session、checkout。让标准继续入口实际完成一次解析。观察当前可续接、无当前和终态分流，核对读取前后状态。追加一条能暴露承接回归的正常路径，验证实际 MERGED 时 Merge recovery 优先于 pre-merge 路径，以及 Planning 的适用性不从 phase 单独推导。 |
| V2 复用与刷新 | 同会话用 previous 重复查询，先观察采用。再用官方 Delivery select 在同一验证 Task 上改选另一个合法 Delivery，预期只刷新 Delivery 定位。另在验证仓库用 guru-bind-task-session 的 delivery_switch_task 正常从 Task A 切到 Task B，分别预置合法分支和登记 checkout。查询传回 A 的 previous，预期当前会话身份仍匹配，但 A 的 Task、checkout、Delivery 依赖均失效并返回 B 的实际定位。用原 Bind 测试支持切换，补测新入口实际刷新。 |
| V3 诊断 | 用现有支持的无绑定、显式读取和普通 stale/冲突样本执行公共入口。旧记录复用 guru-upgrade-tools/tests/test_native_install.py 的保留 predecessor Task 和 session 的工具升级验证输入。原 native continuation 产生 maintenance_required 及原 inspect-task 建议。新入口应保留同一诊断和 guru-maintain-legacy-task 的处理边界，不能将旧对象变为当前 Task，也不能写入记录。已有工具升级验证供采用，本批只从新入口验证诊断透传。 |
| V4 源码与安装 | 运行新增公开 CLI 契约用例及 `trellis/skills/guru-team/tests/test_active_task_continuation_integration.py` 中受影响场景。检查 canonical、dogfood、实际安装入口和受影响的 Codex、Claude Code、Cursor 投影。对 exact matching 更新运行定向 reapply、sidecar 检查及 `check-dogfood-overlay-drift.sh`。 |

V1 至 V4 为待执行计划。测试使用独立验证资源，以免改变本 Task 或其他任务的活动选择。验证止于 #899 受影响入口与匹配投影。

## 4. 停止与恢复

固定基线若发生适用变化，交原 Reconcile owner 判断，只刷新实际受影响的结果。若读取到原 stale、冲突、缺绑定或不支持记录，保留诊断与资源，由原 owner 恢复。同一批候选修订遵循原 Architecture 或 Clarify 路由。没有运行期数据迁移。

## 5. Delivery Policy

full。D1 覆盖 #899 全部 AC。当前无后继切片责任。只有 D1 的实际交付和完整验收证据达到整体范围，原 Completion 才能判断完成。

## 6. Docs SSOT Plan

采用 delta_first。当前待纳入的差额是生命周期需求、设计、测试单元中的标准续接读约定，以及 Architecture Workflow Context 的读取职责和与 ADR-035 的关系。实施结束后由原 RDT 与 Architecture owner 分别集成完整目标并读回。独立完整 Review 消费实际 before/after。历史材料保留原义。
