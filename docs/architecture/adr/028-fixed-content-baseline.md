# ADR-028：固定内容对象与实际阻塞整合

状态：`accepted`；来源：#567 已独立完整审查的[贡献](../contributions/567-fixed-development-baseline.md)；expected Architecture `.91` 晋升至 `.92`。原 proposed ADR 的不可变来源见贡献链接。

## 背景与决定

开发基线、每轮 Delivery 的未交付完整内容与 PR target 是不同对象。以最新 target SHA、整体 CURRENT 或其祖先关系作为全链资格，会让隔离任务为无关变化反复整合。当前决定由原 semantic owners 选择固定完整内容候选与明确阶段适用 authority；后续 Delivery 依据真实前序交付事实确定范围，实际实施 HEAD 的演进由原公共转换承接，既有历史 gate 不冒充新候选的 applicable result。

默认 mandatory pair guard 与无消费者同步状态退出。仅 behind、共享 ref 或无关整体版本前进不触发整合、重签业务 gate 或回规划。实际 conflict、必需检查的具体集成问题、原 Merge 已确认的既有服务端更新要求、明确依赖/需求承接和主动同步仍使用原 Reconcile。一次操作固定目标；原 Check/full_review owner 实际审查解决差额及受影响依赖并记录当前结果，保留首次独立完整 Review、所有原子能力与同操作恢复。

Merge 保留实际 GitHub 资格、expected task HEAD、受控 method/message 与真实 merge identity/parents/reachability；不要求真实合并第一 parent 等于更早观察的 target。Completion 仍核验全部 scope 与真实 Delivery/证据；截点后新增相关事实只补缺少部分，#569 独占查询准备。Finish 仍拥有精确 bookkeeping 和终态恢复。真实 scope/依赖/方案及明确立即适用 authority 变化由原 owner 处理，旧批准不能覆盖真实变化。

## 窄 supersession 与保留

- ADR-005：只替代“无关 shared CURRENT 前进就使所有旧 Task stale/re-entry”的普遍解释。原 Architecture owner、contribution-first、写前 expected-current、独立 committed Review 和 post-promotion fresh gates 保持。
- ADR-012：只替代第7项把实施后 resolved-tree commit 无条件绑定 fresh Phase2 的要求；按实际整合差额和受影响依赖接回原 owners。Delivery 职责、Refs-only 和受控合并身份保持。
- ADR-013：不替代正文。Completion/Closure/Finish/Cleanup/Reactivate 独立职责和 promotion 新差额须 fresh gates 的要求完整保留。
- ADR-024：公共 Task/Delivery authority、所有 Delivery 对称生命周期、原语义门禁及历史事实不制造 current pass 的原则保持；内容基线和当前目标的错误耦合按本决定退出。

ARCH-DOM-014、ARCH-CUR-032/036/059 和 ARCH-INT-013/045 的冲突默认由 ARCH-CUR-065 / ARCH-DOM-048 / ARCH-INT-051 承接。历史 ADR 与 evidence 正文保持原对象，不倒填新证据。constitution 无例外，无关 GAP、软件四轴和业务采用责任不变。

## 采用与代价

采用 [MIGRATION-567](../../../trellis/presets/guru-team/MIGRATION-567.md)成套迁移受控 producer/consumer，正常结果丢失回原 producer；工具与旧数据采用归 #566。不增加 bypass、并行协调器、审批链、跨任务库或长期证据账本。旧私有事务只由原 owner 在明确 recovery 内验证并转换，不成为普通双读路径。

本次知识晋升新差额仍须 fresh Phase2、TaskCommit 与不同 reviewer 的独立完整 BranchReview。实际证明及边界由[唯一 Test](../../requirements-design-test-contributions/567-fixed-development-baseline/test.md)单写；本 ADR 不证明真实 GitHub 策略/副作用、业务安装、author graph 迁移、Release 矩阵或软件发布。
