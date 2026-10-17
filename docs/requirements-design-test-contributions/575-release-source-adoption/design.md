# 正式发布来源采用设计

## D575-SA-01：唯一正式来源

既有 source lock 字段固定完整 PR52 merge、ordered parents、tree、main CI、CLI/Core 与 packageManager。三个 README 和 public-docs 的直接映射同步。MIGRATION-577 追加 workspace 采用说明，原 local_candidate 与 packed mode 差异保持历史归属。正常 pnpm workspace 构建的实际 dist 不经复制或改 mode。

## D575-SA-02：原包定位边界

原 delivery_upstream.packages 仍从 CLI entrypoint 祖先选择 @mindfoldhq/trellis。以该 package.json 创建 Node createRequire，解析 @mindfoldhq/trellis-core/package.json。两种正常布局共用这一路径，没有 sibling fallback。manifest、CLI/Core 配对版本和后继 API/source/bytes/modes 校验保持；普通解析或读取失败返回原 MigrationError。

## D575-SA-03：前驱版本轴

私有发布合同读取 predecessor tag 的 extension manifest 与 source lock，要求 target_trellis_cli 等于 cli_version，再以该值给 --before-cli。其 Fork commit 同样来自该 tag。四份合同同步；没有新增发布输入或 verifier 分支。

## D575-SA-04：验证与不变量

完整候选精确 bytes/modes 在隔离 Git source 形成 clean 本地工程验证提交。原 source_locked tools/Plan2 owner 真实运行，无手写回执或旧档案 guard 绕过；history_only 与数据保留沿公共 Plan2。目标自身 native 与下一 consumer 分开观察。该本地验证不是正式 Task commit 或远端 exact candidate。

Architecture 继承 .98/active、ARCH-INT-057/ADR-027。当前方案没有新边界或状态算法；实现变化仍由原 Architecture owner 判断。RDT 使用 delta_first，晋升由原 owner 在 pre-promotion 完整审查后执行。

## D575-SA-05：共享 AGENTS 的首次目标

原tools prepare消费SDK导出的PreparedMaintenancePlan，并交公开preview/apply。它在第一次apply与checkpoint冻结前，对具名AGENTS.md action.target调用原installer共用的pure renderer，计算canonical Guru block与原target合成的bytes/mode。public writer写入该唯一目标，随后Guru installer的ensure应不再修改内容。source snapshot、operation_id、candidate、guard、其它action与Core模板hash回执保持；回执仍指原Core模板基线，Guru block是已存在的定制。

该薄projection不因字段可写而取得额外所有权；依据是public plan作为SDK公开消费输入，以及原Guru installer对该block的既有内容职责。原ensure与prepare使用同一renderer，不复制block算法。resume/recover/rollback只用冻结plan，不重新投影或修改checkpoint；public原Task/session compatibility与先public rollback后Guru restore的顺序保持。

原失败样本保留。等价新.3安装以原CLI正常创建Task/binding/session，沿strict source_locked升级、目标native及下一consumer，再原source rollback。真实SDK回归同时检验无投影的原双writer路径自然触发later_work_conflict，以及投影后原rollback恢复；不伪造target或兼容状态。
