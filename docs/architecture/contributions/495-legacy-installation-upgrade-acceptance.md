# #495 固定来源验收架构增量

Identity：`architecture-contribution-495-legacy-installation-upgrade-acceptance-v2`；state：`reviewed_candidate`；task：`.trellis/tasks/10-06-495-legacy-installation-upgrade`；expected current：`current-main-0.6.17-guru.72`；拟 successor `.73`。继承 [v1 contribution](./495-legacy-installation-upgrade.md)、[ADR-017](../adr/017-legacy-installation-upgrade.md) 与 current baseline，不改已晋升历史。

绑定 `guru-maintain-architecture-baseline:2.0`、`guru-trellis-architecture-change-contract-v1`、`guru-trellis-design-constitution-v1`；change path：`legacy_boundary_convergence`。生产机制仍为远端 `6a563f5f06cb1284c0935b3a2be68524d93df988`；本增量不新增 ADR、API/writer、正常双读、锁或 state store。

| Required concern | 当前判断 |
| --- | --- |
| authority-binding | live #495 与 comment6028281048 明确允许旧正式 writer 构造来源；其它 MIG01..09/current-only 不变。 |
| constitution-binding | 复用旧 canonical/native 与新正式 owners；完整身份、职责隔离、最小本地备份与单向退出，无原则例外。 |
| boundary-and-decision | Fork core/task、Guru migration/preset、current lifecycle 边界沿 ADR-015/017；test provider 只拥有构造 fixture facts。 |
| owner-and-single-writer | snapshot observer 在原正式 writer 之后只读复制；不成为第二生产 writer，新 preset/current owners 不接受旧 gate。 |
| compatibility-and-exit | 旧在途明确 deferred/preserve + pinned-old/manual；当前 identity 拒绝 direct old；旧 parser 仍局限一次 migration，停止支持后删除。 |
| gap-and-deviation | 同一远端 source_locked/public/provider 与 accepted 旧在途样本已取得；首轮失败/恢复及未归类原因保留。ARCH-GAP-012 当前仍 open，待独立 review/promotion 再更新。 |
| parallel-scope | 三 planning 与隔离贡献拥有本轮 diff；真实业务/Fork/worktrees 只读，shared current 未修改。 |
| evidence-and-freshness | 固定 old a32/new 6a/Fork8868；旧 writer 正常终态、非 terminal 快照及新 migration 16 文件保留；完整结果见 RDT test。 |
| review-and-promotion | 独立 committed full-range Branch Review 后 expected `.72` promotion，新增 diff 再 fresh check/commit/review；不以证据贡献替代 merge/Completion。 |

Before：`.72` 已接受独立单向迁移，但同源远端与旧在途验收尚有缺口。After：正式七场景首轮5/7 + 两原样本恢复/剩余断言、同provider更新/reapply、真实live PR195 deferred 与合并PR诊断，以及旧writer快照真实source_locked升级/保留均已有证据。具体失败、test doubles、native current neighbor 和未验证项由 [RDT test](../../requirements-design-test-contributions/495-legacy-installation-upgrade-acceptance/test.md) 唯一记录。

Project check：`guru-trellis-architecture-convergence:repository:1` applicable/blocking。应审查本增量及完整实现维持单 writer/current-only，旧 gate 无当前 consumer，构造/provider/live 证据未混淆，恢复/rollback 固定基线未吸收新工作，shared version 历史 immutable。没有新增/恶化偏差；是否通过由 fresh stage owner 实际判断，本文不是 checker receipt。

`ARCH-GAP-012` 的 successor 更新条件：独立 committed review 接受全部 MIG01..09 证据及局部兼容出口、expected-current RDT/Architecture promotion 完成，并复审晋升 diff。该缺口收敛不证明完整 Release matrix、tag/Release 或真实业务升级。
