# D495 版本系列升级增量候选

状态：draft_candidate；继承 [Architecture `.73/active`](../../architecture/README.md)，完整 mechanism owner 见 generation 1 [design](../../../.trellis/tasks/10-06-495-legacy-installation-upgrade/design.md)。

| 责任 ID | 后继职责 / consumer |
| --- | --- |
| D-MIG-495-INVENTORY / FAMILY | Guru 单一升级入口读取真实 manifest/core/source，将两系列归入实际合同；G1..G8 不是支持白名单。 |
| D-MIG-495-CORE | Fork 显式 migrate 更新 core-owned assets；legacy/current/deferred 投影独立，普通 update/current reader 不扩双读。 |
| D-MIG-495-GURU | 旧 source/receipts 确定 ownership；upstream-owned 交还 Fork；本地定制显式保留/合并，current preset 与 marketplace 执行目标更新。 |
| D-MIG-495-LIFECYCLE | 保留合法 current task/control/session；known legacy 由既有正式 owner 转换或接续，不制造当前 gate。 |
| D-MIG-495-RECOVERY | 既有私有备份记录实际 before 与确实受影响控制面；回退恢复该来源，新业务工作阻止覆盖。 |

Public initial selector 演进为 `guru0.6-family` / `guru0.7.0-family`，同步 schema、Interface、受控 consumer 和文档；旧 fixed selector 不增加 alias。升级与回退 output 各自拥有最小 consumer DTO，实际恢复版本不固化 `.41`。候选 Guru `.3` 采用已固定的正式 Fork `.3` source lock，Guru 同源远端验收仍待候选发布；无第二状态机、writer 或新业务 workflow phase。


受管定制执行：既有 preset 接收 migration owner 的薄 `migration_preserved_paths` 参数，仅用于已审查 exact companion preserve；默认为空。定制退出 canonical managed ownership，后续普通 reapply 的 unknown-local-edit 机制保留文件并明确 `.new`，冲突文件不 chmod。旧 `config.yml` 为 user-owned。Skill/overlay 当前接口要求保持，不兼容定制显式 resume/合并，不把旧接口当 current pass。

正式 Fork 已固定到 `cc5f9a30652be29cffee9acc7e14d5dc5daaf04c` / 成功 main CI `37647767799`；该精确源码本地构建与来源验证通过。Guru 远端可寻址 exact source/provider 验收仍待候选发布。
