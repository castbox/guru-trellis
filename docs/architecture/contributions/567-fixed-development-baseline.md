# #567：固定内容对象与实际阻塞整合

状态：`reviewed_promoted`；identity：`architecture-contribution-567-fixed-development-baseline-v1`；change_path：`target_native`。按 expected `current-main-0.6.17-guru.91/active` 晋升至 `.92`；constitution v1、project change contract v1、现有 GAP lifecycle 与软件四轴保持。ADR-028 窄化替代 ADR-005 的普遍 CURRENT-advance stale 解释及 ADR-012 第7项的无条件 fresh Phase2 要求；ADR-013/024 与原职责继续继承。

首次通过的独立完整 committed Review 范围为 `origin/main@3b165daef0001bd9816c0bf3bbe928bcb59de390...f2538d822dbede7ea34dc29bdad9a0f828130dad`，113路径。[不可变 task-owned contribution](https://github.com/castbox/guru-trellis/blob/f2538d822dbede7ea34dc29bdad9a0f828130dad/.trellis/tasks/10-15-567-fixed-development-baseline/architecture-contribution.md)与[proposed ADR](https://github.com/castbox/guru-trellis/blob/f2538d822dbede7ea34dc29bdad9a0f828130dad/.trellis/tasks/10-15-567-fixed-development-baseline/architecture-adr.md)保留原候选；长期机制由[唯一 Design](../../requirements-design-test-contributions/567-fixed-development-baseline/design.md)、canonical Skills 与 MIGRATION-567 单写，不依赖 future active Task 路径。

Before：默认多阶段 pair guard、最新 base 祖先资格及整体 freshness/SHA 耦合会触发无必要整合和全链重跑。After：原 owners 分别拥有固定完整内容、明确阶段适用 authority、实际整合操作与真实发布/完成事实。默认追赶退出；实际阻塞的普通/resolved/committed/continuity 与同操作恢复仍存在。当前 evidence 的边界由[唯一 Test](../../requirements-design-test-contributions/567-fixed-development-baseline/test.md)拥有。

| Concern | Applicability / 晋升依据 |
| --- | --- |
| authority-binding | applicable：expected .91、successor .92、原公开合同和阶段适用 authority；无关整体推进不替代真实变化判断。 |
| constitution-binding | applicable：固定对象和原 owner 降低耦合；删除无 consumer guard，无新 authority/store/通用机制。 |
| boundary-and-decision | applicable：开发基线、内容候选、target 与 integration operation 分离，ADR-028 明确窄 supersession。 |
| owner-and-single-writer | applicable：原 semantic owners、upstream 公共 store 与原私有 executor/writer 保持；shared-current 只由原 promotion owners 维护。 |
| compatibility-and-exit | applicable：MIGRATION-567 成套迁移接口与正常恢复；原 owner bounded 私有旧事务转换，不保留 retired guard 或普通长期双读。 |
| gap-and-deviation | applicable：无关 GAP 不新增、重开或关闭；正常恢复/原子能力保留，不把受控样本晋升为外部完成证据。 |
| parallel-scope | applicable：本Task隔离贡献与受影响canonical；不操作其他Task、upstream/global安装或来源业务仓。 |
| evidence-and-freshness | applicable：真实固定候选/当前结果与明确阶段适用规则；唯一Test区分当前运行、历史红测、fixture、实际AI和外部未验证边界。 |
| review-and-promotion | applicable：上述完整committed Review后按expected-current晋升；本次新差额仍须fresh Phase2/TaskCommit/不同reviewer完整Review。 |

知识晋升不证明 Delivery、Completion、Closure 或软件发布。真实 GitHub 策略/副作用、远端 marketplace、业务采用、作者完整旧 graph 迁移与完整多平台 Release 矩阵保持明确未验证边界。
