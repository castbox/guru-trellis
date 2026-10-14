# #557：已有正式 Delivery 的手动合入事实

状态：`reviewed_promoted`；identity：architecture-contribution-557-manual-merged-delivery-recovery-v1；change_path：`target_native`。按 expected `current-main-0.6.17-guru.89/active` 晋升至 `.90`，constitution v1、project change contract v1 与既有 GAP/软件四轴保持；ADR-026 补充 ADR-024。

首次独立完整 committed Review 的精确范围为 `origin/main@ccf67ff157dc006f236870049dda9cba0fafa73f...6bba4880362a2e0ff31b535809e4895b7fa1a84d`。原 task-owned 贡献是历史候选，[不可变原稿](https://github.com/castbox/guru-trellis/blob/6bba4880362a2e0ff31b535809e4895b7fa1a84d/.trellis/tasks/10-15-557-manual-merged-delivery-recovery/architecture-contribution.md)保留 preimage；本文件是晋升后的架构责任定义，不依赖 Finish 后的 active Task 路径。

Before：已发布的正式 PR 被普通用户合并后，原 Merge/history 依赖 Guru trailers/gate，无法承接无这些副产物的真实事实。After：原 Merge 根据现有唯一 public Task/Delivery/Publication 与真实 Git/GitHub 归属，沿现有 public historical_success 记录 actual candidate；原 Completion 独占整体 scope 与必要证据判断。query2 只读已记录事实，原 expected-head/schema1/2 与 query1 具名消费者保持。具体行为由 canonical Merge/Completion 合同独占。

| Concern | Applicability / 晋升依据 |
| --- | --- |
| authority-binding | applicable：expected .89、active successor .90、原 Task2/API1 与当前 project contract。 |
| constitution-binding | applicable：复用唯一 public relation、writer 与原 owners；无第二模型、ledger 或授权记录，符合当前最小必要复杂度。 |
| boundary-and-decision | applicable：ADR-026 仅澄清真实手动事实恢复与 gate 适用性分离，不改变 Completion/Closure/Finish owner。 |
| owner-and-single-writer | applicable：上游公共模型/转换单写；原 Merge 归属/记录、history 只读、Completion 独立判断；shared current 由原 Architecture owner 串行晋升。 |
| compatibility-and-exit | applicable：manual profile/query2 成套 matching 采用；query1 只保留真实 legacy/migration/standalone consumer，最后 consumer 退出后由原 owner 删除。旧完整安装由原 Upgrade/业务 owner 成套迁移，不桥接旧 checkpoint。 |
| gap-and-deviation | applicable：修复正常手动恢复缺口，ARCH-GAP-006/008 原 owner 与 closure condition 保持，无 GAP 生命周期改变、双 writer 或原则例外。 |
| parallel-scope | applicable：仅 #557 与隔离验证资源；不触 backend #149/PR #526、其它 owner 或完整 Release 矩阵。 |
| evidence-and-freshness | applicable：[唯一 Test](../../requirements-design-test-contributions/557-manual-merged-delivery-recovery/test.md)记录实际代码/安装/外部观察；合入事实不授予 CI、review 或业务通过。 |
| review-and-promotion | applicable：首次独立完整 committed Review 后晋升；minimal project projection 同步 .90，新差额重新进入 Phase2/commit/独立完整 Review。 |

原设计责任 D557-01..05 与项目 convergence protocol 的对应关系保留于不可变候选；CURRENT/DOMAIN/INTEGRATION 只引用本贡献的归属。真实 GitHub 验证链不证明旧 source dogfood 采用、backend 现场恢复、业务验收或软件 Release。
