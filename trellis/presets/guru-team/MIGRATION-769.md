# MIGRATION-769：tools peer 增长与冻结源恢复

## 加性边界与真实旧consumer

旧consumer是修复前guru-upgrade-tools产生的private-recovery1.0事务，包括#766原操作。旧完整安装的install/resume/rollback和既有出口保持原义。当前修复直接修改原peer保持检查，逐项保原键值；正常新增且与原实际工具写集物理隔离的peer不因新增键阻塞，也不进入原backup/write/delete集。保留#759的prunable且缺.git精确跳过条件。

## 显式采用

从完整修复源加载同一guru-upgrade-tools owner，使用recover_frozen_source与action=resume或rollback、原recovery_ref，--root为原准确目标。修复源只提供当前executor，cp.source完整原源仍提供原installation helper/依赖、preset installer和资产。原root/source HEAD/tree token、公共CLI/Core pair/plan/ref、owned freshness和Guru preimages继续验证。无新source/plan覆盖，不改旧源或checkpoint，不reprepare，不刷新peer基线/备份，不吸收后来业务编辑。

原engine逐phase续接；preset保持pending，complete不再install。原已完成公共写由原public owner恢复，rollback先核公共tools/data兼容，再恢复原Guru preimages。frozen_recovery_required保持同profile/action/ref回同owner，不能投旧同源resume。新profile、独立retry schema/example、Interface及Skill合同成套采用；既有profile/出口无静默变化，private1.0不转换或双写。

## 安装、验收与退出

受影响canonical及当前目标安装由原tools/preset owner更新，保Task/session与用户配置，处理真实sidecar并核目标own resolver/installed/native及drift/mode。源码可执行不证明目标已采用。真实Git拓扑、旧owner正常事务/公共新入口、原peer普通变化拒绝及实际#766原操作恢复分别验证；local_candidate继续明确formal_fork_source_lock未验证，不声称完整多平台Release矩阵。工具结果不代表Task Completion。

兼容owner为guru-upgrade-tools。旧schema1.0操作进入终态且其原恢复保留责任结束后，由该owner通过明确迁移删除兼容入口及其注册/schema/consumer/文档。没有扫描器、自动删除或无限期通用兼容平台。历史事务与证据保原观察。

## D2：正常退出的原 peer 位置

仅 recover_frozen_source 加性支持 retired_peer_roots。AI 先读取原 peer owner 的实际终态结果和准确位置，判断正常退出及本次适用性；路径缺失或 Git 未枚举不能代替该判断。省略或[]继续 D1 原检查；同源 profiles 不接收此例外。

非空项必须为原 frozen checkout-local pointer marker 可关联的绝对位置，不能是目标。确定性代码复用原 parser 核完整注册（含 prunable）无该位置，并核位置路径项自身不存在。只处理这些准确 root 的 local active/selection-v3 及 installed/source runtime 观测。原 common/gitdir 不被泛化忽略；该模式下未被当前枚举覆盖的其它原文件从原路径实际读取同值，未覆盖的 runtime 缺失仍拒绝。原 source/owned/public compatibility 与前后隔离保持。

原 engine 薄透传本次 roots，不改 private1.0、cp.public、peer snapshot、plan 或备份。frozen_recovery_required 仅在本次字段实际存在时原样携带，含显式[]；既有省略字段的 retry 不增加常驻空值。Interface 的既有 presence-select 只复制实际存在的属性，无新 DSL 或出口。新 caller 使用含配套 schema/runtime/Interface/consumer 的完整 matching D2 package；D1 的旧闭合 schema 不被宣称接受新字段。

实际旧 consumer 仍为 #766 原事务；本能力沿上述原保留期限及同一 owner 的明确迁移退出，不建立退出台账或资源生命周期平台。原终态依据、对象机械校验、组件验证、实际原操作恢复与目标自身安装结果分别成立。
