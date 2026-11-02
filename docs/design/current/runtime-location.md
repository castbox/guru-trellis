# Runtime与Git来源的设计合同

Identity：`RDT-DES-RUNTIME-LOCATION`；状态：current。承接[完整需求](../../requirements/current/runtime-location.md) R718-01—11；[Test](../../test/current/runtime-location.md)拥有验证策略与实际观察。Architecture继承 `guru-trellis-architecture` / constitution v1 / ADR-RUNTIME-LOCATION。

## D718-01 / CON718-ENV：环境身份与代码

原bootstrap拥有identity、user cache、锁依赖、capability和真实public wrapper检查。环境需求使用runtime API/layout、lock digest和implementation/major/minor、OS/architecture/ABI，不使用patch/path、Git HEAD、Task或位置。实际目标代码由本次assets提供，seed只运行标准库解析/维护。最终业务命令仅在被选受管环境执行；global site-packages与其他checkout新版代码不能证明目标成功。

## D718-02 / CON718-SELECT：选择与可重建hint

当前选择在checkout-private `.trellis/.runtime/guru-team/python/selection-v3.json` 保存3.0格式，区分自动模式和显式Python兼容类别。旧 `active.json` 原文保留供旧installed读取，不双写。显式类别只表示implementation/major/minor及平台/ABI，日常不依赖原路径仍存在；同类别patch/path复用。按当前assets要求优先验证对应hint，无有效自动hint则按runtime identity字典序验证已有cache，选择首个有效匹配者并缓存解析结果。每需求hint支持不同依赖切换与切回，不增加全局偏好或时间顺序authority。显式类别缺少匹配环境则拒绝并恢复，不换类别。

初始化/apply/reapply未传--python使用当时PATH python3并保存自动选择；显式--python优先且失效不回退。日常不安装、不因PATH变化重选。自动hint是可重建定位信息，不提供Task/阶段/授权资格。

## D718-03 / CON718-REPAIR：独立维护

原环境owner公开check、resolve、repair：check只读，resolve仅缓存已验证定位，repair需要真实CPython3和锁来源，沿原candidate→locked install→probe/真实wrapper→成功切换。缺seed、缺cache、损坏、依赖失配和显式类别失配输出安全稳定JSON诊断。失败不提前替换此前可用环境或选择。目标dispatcher坏时，从明确matching source可达环境检查/恢复；工具维护仍归原upgrade-tools。每次维护后由目标自身resolver/installed/native入口证明结果。

## D718-04 / CON718-BASE：明确Git对象和实际同步

原guru-sync-base公开invoke以operation=read请求只读明确base_ref及适用base_commit；输出baseline_ready，base为明确git_object来源，携带selected_ref、固定commit和局部一致性identity。原operation=sync及既有调用继续原synced语义：实际目标checkout、clean、可ff历史和三方identity检查。只读不fetch、不ff、不要求所选分支检出或无关位置干净。所选固定commit与后续无关ref前进区分，刷新由caller明确请求和采用新来源。

来源variant由canonical Interface/schema独占字段版本；新来源不能伪填decision/local/remote三个角色，也不冒充同步事实。具体公开flags/schema迁移由[同批迁移合同](../../../trellis/presets/guru-team/MIGRATION-718.md)拥有。

## D718-05 / CON718-CONSUMER：真实读取与链路

Discovery读取固定tree的Docs/code/tests/blob/archive index，复核实际source对象；草案工作区独立绑定。公开source读取事实命令只服务该owner/Agent查看真实内容。保留current-state→history→语义gate顺序。base来源通过五阶段transition及Clarify回程、Wording、Readiness和CreateIssue/Task的薄projection承接。每consumer只读其必要字段，不读上游private artifact。

Task Creation仍核同一Task/源码关系、选定base提交与合法目标；Task/Delivery身份和generation仍由原公共模型/owners校验。正式committed Review和实际remote发布约束保持。无Task/外部worktree/dirty或untracked草案能读审，不因此生成正式gate或隐式commit/push/移动其他checkout。错基线与普通candidate变化回原纠正/刷新路径。

## D718-06 / CON718-CUTOVER：旧选择与rollback

旧v2来源未知，不推断曾经显式或自动。当前assets兼容有效时保留原物理环境；失效时作为可替代hint查兼容cache。需要持久显式类别时用当前公开--python入口表达。只有新载体不存在时才按原local/gitdir/common读取v2一次；新载体成立后只读写当前格式，新载体存在但无效时准确拒绝，不能回退旧来源丢失显式约束。不新增来源认证或授权账本。

工具维护只写目标checkout私有选择，common/peer载体不变；共享cache新增也不能改变peer已成立的合法实际选择。原rollback先核公共tools/data兼容，再按原preimage恢复目标工具和新旧选择载体的实际存在与原文；旧工具仍读取原v2。公开`--print-active-pointer`返回新writer locator，实际解析值由`--check`/resolver提供。旧完整安装按固定原合同继续，切换与退出由原runtime/installer/maintenance owners执行。cache不随位置/Task生命周期删除。

## D718-07 / CON718-BOUNDARY：知识与分发

canonical workflow/Skill负责操作选择与语义，确定性脚本只执行和校验。canonical/package/dogfood/installed/platform、mode、reapply/drift和sidecar使用matching安装owner成套更新，不能手抄受管副本。RDT与Architecture先写完整隔离proposal，candidate Check后原final_integration晋升，实际after重绑final Check/Review；promotion不替代实现或Completion。

前驱替代范围与未迁移范围由对应Requirement单元定义；ADR-027的单目标维护、peer隔离、source/target分别验证、公共数据兼容及Task维护仍成立。没有新Task模型、资源池、GC、telemetry或通用依赖平台。
