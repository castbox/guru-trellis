# #566：工具安装、任务转换与历史保留独立维护

状态：`reviewed_promoted`；identity：architecture-contribution-566-independent-maintenance-v1；change_path：`legacy_boundary_convergence`。按 expected `current-main-0.6.17-guru.90/active` 晋升至 `.91`，constitution v1、project change contract v1、既有 GAP 与软件四轴保持；ADR-027 补充 ADR-017/018，ADR-024 公共模型权威保持。

首次独立完整 committed Review 的精确范围为 `origin/main@3e8b281c93894cd3df4e704901bda63ca2885f23...95bcf24334f9a4d25df3f9175af9d00b58d86915`。[不可变 task-owned 候选](https://github.com/castbox/guru-trellis/blob/95bcf24334f9a4d25df3f9175af9d00b58d86915/.trellis/tasks/10-15-566-single-checkout-upgrade/architecture/contribution.md)保留历史；长期责任和接口由[唯一 Design](../../requirements-design-test-contributions/566-single-checkout-upgrade/design.md)与 canonical Skills 单写，不依赖 active Task 路径。

Before：旧工具与 Task 处置由完整 Plan2 组合，primary Python 默认指针存在共享消费者。After：source-loaded tools 与 selected legacy Task 两个独立 semantic 闭环各有具名消费者。公共模型、模板、转换与恢复仍归 Trellis；Guru 原 installer、私有控制 owner、managed Python owner 分别处理自身资产。只读选择先分支后唯一 checkout；tools-only 使用 checkout-local override，原 Sync 同步与完整 Plan2 不改义。业务 Reconcile 与 Completion 保留原职责。

| Concern | Applicability / 晋升依据 |
| --- | --- |
| authority-binding | applicable：expected .90、active successor .91、公共 Task2/API 与当前 change contract。 |
| constitution-binding | applicable：两项能力分别解除已观察到的安装耦合与维护启动依赖，复用公共算法及原状态 owners，无第二生命周期、通用策略引擎或授权记录。 |
| boundary-and-decision | applicable：ADR-027 显式补充 ADR-017/018 的完整升级唯一解释边界；ADR-024 与普通 current-only 保持。 |
| owner-and-single-writer | applicable：AI semantic、Trellis public writer、Guru 私有控制/资产与 runtime pointer 各守原边界；历史事实核验不制造当前 gate。 |
| compatibility-and-exit | applicable：selected legacy 转换/历史保留使用匹配完整来源，旧 Plan2 保持独立 consumer；legacy-only profiles 在真实 consumer 退出后由后续 migration 删除，无永久普通 dual-read。 |
| gap-and-deviation | applicable：仅处理本次耦合与共享 pointer 影响；ARCH-GAP-006/008/012 生命周期与 closure conditions 不变，local candidate 不晋升为正式 Fork 能力。 |
| parallel-scope | applicable：仅 #566 source/贡献与隔离验证资源，不更新其它 checkout 或真实业务 Task；shared authority 由原 owners 串行维护。 |
| evidence-and-freshness | applicable：[唯一 Test](../../requirements-design-test-contributions/566-single-checkout-upgrade/test.md)拥有实际安装/native/原 owner/历史保留/回退及限制；独立完整 Review 绑定上述提交范围。 |
| review-and-promotion | applicable：首次独立 committed full-diff Review 后 expected-current 晋升；本差额 fresh Phase2/commit/独立完整 Review 后才可进入 Publication。 |

新工具可用、任务转换、原生续接、历史交付恢复与业务完成分别报告。正式锁仍不含公共 maintenance API，source_locked 写前阻塞；未提交 #40 matching 本地包只证明隔离开发链路。未验证真实业务安装、正式依赖采用或完整 Release 矩阵，不据此关闭兼容 GAP 或声称软件发布。
