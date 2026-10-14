# #547：来源关系与本次 Closure 处置分离

状态：`reviewed_promoted`；identity：`architecture-contribution-547-retain-source-open-v1`；path：`target_native`。按 expected `current-main-0.6.17-guru.87` 晋升至 `.88`，继承 current constitution `guru-trellis-design-constitution-v1` 与 project change contract v1。实现已独立审查的完整范围为 `origin/main@8ec6751dd84c8a1ae8b684e278de367a8e94c9a6...a89ee58e6557e1448df6d65328e06065640ec670`；晋升产生的新差额须重新通过原 gates。

Before：exact_source 资格被执行条件绑定为必须关闭；Finish 要求所有有资格动作 CLOSED，aggregate closed 被误作公共源关闭事实。After：原 Closure owner 可审查并冻结 retain_open，观察 OPEN 而不 close；原 Finish owner 消费同一冻结动作集，逐动作校验所需状态。公共 exact source fact 与 aggregate terminal 分离。决定由 [ADR-025](../adr/025-retain-source-open-disposition.md)拥有，step-local 行为仍由 canonical Closure/Finish Skills 独占。

| Concern | Applicability / 晋升依据 |
| --- | --- |
| authority-binding | applicable：nonplanning 2.0、expected `.87`、active successor `.88` 和 current change contract 绑定 |
| constitution-binding | applicable：current constitution；一个既有 action 增量与直接 consumer 足够，无额外机制或原则例外 |
| boundary-and-decision | applicable：来源资格与本次动作分离，ADR-025 增补 ADR-013/024；`target_native` |
| owner-and-single-writer | applicable：原 Completion/Closure/Finish/Cleanup 分工不变，原 Architecture owner 串行晋升 |
| compatibility-and-exit | applicable：matching producer/consumer 成套采用，无新双读；旧安装退出见下文 |
| gap-and-deviation | applicable：移除强制关闭缺口，不新增、关闭或重开既有 GAP |
| parallel-scope | applicable：只晋升本 Task 贡献，禁止竞争 shared current、改原 CMS 或引入第二 authority |
| evidence-and-freshness | applicable：before/after、唯一 Test 与当前文档候选绑定，外部边界不冒充验证 |
| review-and-promotion | applicable：独立完整 committed review 后按 expected current 晋升，新增差额重进原 gates |

没有第二 owner、store、公共 DTO 或 exit。移除错误的强制关闭条件，保留正常 identity/freshness、合法旧动作和原恢复 consumer。

真实旧安装继续固定原完整包，采用新枚举须由原 Upgrade/业务 owner 成套迁移；不新增 runtime adapter，旧 reader 退出仍以最后真实直接 consumer 完成为条件。该 support boundary 不将原 CMS 剩余责任转给本 Task。

RDT 的 R547-01..08 / D547-01..05 及全部实际验证、首次失败和未验证边界由 [唯一 Test](../../requirements-design-test-contributions/547-retain-source-open/test.md)及其同根 trace 承接。知识晋升不证明当前 app 采用、旧安装升级、原 CMS 恢复/联调/产品 #59 验收、远端 marketplace 或完整 Release 矩阵；软件四轴与 GAP lifecycle 保持。
