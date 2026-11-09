# MIGRATION-769：tools peer 增长与冻结源恢复

## 加性边界与真实旧consumer

旧consumer是修复前guru-upgrade-tools产生的private-recovery1.0事务，包括#766原操作。旧完整安装的install/resume/rollback和既有出口保持原义。当前修复直接修改原peer保持检查，逐项保原键值；正常新增且与原实际工具写集物理隔离的peer不因新增键阻塞，也不进入原backup/write/delete集。保留#759的prunable且缺.git精确跳过条件。

## 显式采用

从完整修复源加载同一guru-upgrade-tools owner，使用recover_frozen_source与action=resume或rollback、原recovery_ref，--root为原准确目标。修复源只提供当前executor，cp.source完整原源仍提供原installation helper/依赖、preset installer和资产。原root/source HEAD/tree token、公共CLI/Core pair/plan/ref、owned freshness和Guru preimages继续验证。无新source/plan覆盖，不改旧源或checkpoint，不reprepare，不刷新peer基线/备份，不吸收后来业务编辑。

原engine逐phase续接；preset保持pending，complete不再install。原已完成公共写由原public owner恢复，rollback先核公共tools/data兼容，再恢复原Guru preimages。frozen_recovery_required只携同profile/action/ref回同owner，不能投旧同源resume。新profile、独立retry schema/example、Interface及Skill合同成套采用；既有profile/出口无静默变化，private1.0不转换或双写。

## 安装、验收与退出

受影响canonical及当前目标安装由原tools/preset owner更新，保Task/session与用户配置，处理真实sidecar并核目标own resolver/installed/native及drift/mode。源码可执行不证明目标已采用。真实Git拓扑、旧owner正常事务/公共新入口、原peer普通变化拒绝及实际#766原操作恢复分别验证；local_candidate继续明确formal_fork_source_lock未验证，不声称完整多平台Release矩阵。工具结果不代表Task Completion。

兼容owner为guru-upgrade-tools。旧schema1.0操作进入终态且其原恢复保留责任结束后，由该owner通过明确迁移删除兼容入口及其注册/schema/consumer/文档。没有扫描器、自动删除或无限期通用兼容平台。历史事务与证据保原观察。
