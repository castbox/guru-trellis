# Runtime与Git来源的设计合同

导航别名：`R718/D718/T718`；`R760/D760/T760`；`worktree配置路径`；`runtime与Git来源`。原语义 owner：`guru-maintain-requirements-design-test-ssot`。`R718/D718/T718` 与 `runtime与Git来源` 别名继承自 Git `f75f0f5dd078a0c2c4c9a54ac861383774162806:docs/design/current/README.md` 的原 current 条目；该来源定位原晋升状态及所属完整正文，不将知识状态扩大为实现/安装通过。原定义、来源与关系保持。

Identity：`RDT-DES-RUNTIME-LOCATION`；状态：current。承接[完整需求](../../requirements/current/runtime-location.md) R718-01—11 与 R760-01—05；[Test](../../test/current/runtime-location.md)拥有验证策略与实际观察。Architecture继承 `guru-trellis-architecture` / constitution v1 / ADR-RUNTIME-LOCATION。

本单元 RDT 定义修订：`worktree-config-path-760`。原 owner 在 #760 D1 candidate Check 后，
以本Task固定来源与真实 current 重读整合并写回；该标识不表示软件版本或最终 Git HEAD。

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

## D760-01 / CON760-PATH-FACTS：项目路径事实

承接 R760-01/02。现有 shared runtime 提供 topology/config/path 确定性解析，原 environment
与 Task acquisition 直接消费；没有新 Skill、planner、cache、锁或位置台账。
primary 候选来自 live worktree topology、可用 core.worktree，或调用位置 gitdir==common-dir
事实。逐候选核 actual toplevel/gitdir/common identity，排除 linked 冒充 primary。
separate-git-dir 的 porcelain 首行可能是 metadata，不能据其或common-dir.parent猜路径。
无法唯一确证返回 `primary_anchor_unavailable`，原 AI owner处理。

读取 primary 的 `.trellis/guru-team/config.yml`：空 root 采用primary父目录下
`<primary-name>-worktrees`，相对值对primary解析，绝对值直接使用。linked空模板没有独立
选址意图；调用checkout非空root解析后与primary不同则诊断冲突，不写任何配置。
普通空格和引号遵循既定标量解析语义，不扩为通用YAML框架。

## D760-02 / CON760-CREATE：两个创建 consumer 与分流

承接 R760-02—04。原 `check-env.sh` 输出解析后的绝对 `worktree_root` 与 `primary_root`、
`worktree_config_path` 来源事实，提供name时以 `checkout_root` 返回绝对目标；`--worktree-name`生成目标，配合 `--checkout-root` 核计划一致，后者需要前者。
查询不产生selector typed DTO、Task身份或持久映射。

create-task 对 provision 的 new_branch/existing_branch 新目录加性接收
`path_source=configured|explicit` 与 `worktree_name`。当前 AI 自行生成必须configured，
提供单目录名及绝对checkout_root；原runtime在任何创建副作用前重算root/name并比较，
失配诊断后原owner修正，不静默替换。真实显式位置使用explicit及原绝对路径合同。
Task-free原owner新建时消费公开预检的实际目标，经精确副作用审查后普通Git创建，
读回实际目录、Git注册并重新审linked/non-base适用性，不调用Task acquisition。

两个owner先分流合法采用或恢复。adopt_invocation_checkout、existing_checkout及原Task
recovery保留原identity/clean/绑定/位置要求，不受生成root限制；配置变化不重定位。
AI绝对值不反推用户选址。primary写入路径仍退役；既有其它身份/生命周期前置保持。

## D760-03 / CON760-MIGRATION：兼容与维护

承接 R760-04/05。完整公开支持合同由 [MIGRATION-760](../../../trellis/presets/guru-team/MIGRATION-760.md)
拥有。旧已安装create-task公开输入及其创建/恢复脚本省略新字段仍按原绝对checkout_root，
由同一schema/runtime消费；原create-task owner维护。调用方切换策略字段后，该调用退出省略
用法，当前AI合同直接切configured。无新增兼容executor，不迁移Task持久数据。

环境root从旧调用位置回退/原样配置值修正为项目解析绝对root，两个owner成套采用。
旧安装使用matching版本；新能力经原tools-only owner更新完整投影，保留配置/Task/session/peer，
按原冲突与sidecar处理并验drift，不手抄dogfood。RDT与Architecture依原候选Check和
final_integration晋升；原最终Check/Review独立审实际after。完整Release矩阵仍归专门owner。

## D769 / 原事务、原资产与修复执行器

承接R769-01—03。原upgrade-tools保持原观测键逐项同值，新增peer核物理隔离而不刷新基线。新recover_frozen_source原必填输入为profile/action/recovery_ref，D2按下节加性支持有限退出位置；完整修复源执行当前engine，cp.source完整原源加载原installation helper/installer和资产，保原身份及owned freshness。既有同源profiles保持原义。preset是pending续接，complete只验证；原公共operation恢复不reprepare。rollback先公共compatibility再原Guru preimages。frozen_recovery_required保同profile/action/ref回原owner，原成功/blocked语义保持。公开细节及schema由package/MIGRATION-769拥有；真实旧schema1.0消费者含#766，终态和原保留责任结束后明确迁移退出，无数据转换或第二台账。Architecture由ADR-TOOLS-FROZEN-SOURCE-RECOVERY与ARCH-RUNTIME-LOCATION约束。

## D769-D2 / CON769-RETIRED：调用期退出位置

承接 R769-04—06；Architecture 继承 ARCH-RUNTIME-LOCATION 和 ADR-TOOLS-RETIRED-PEER-OBSERVATIONS。原 tools Markdown owner 读取实际退出 owner 结果并作适用判断，非空 retired_peer_roots 只携准确绝对位置。executor 复用原 parser 读取包括 prunable 的完整注册；核 root 来自原 checkout-local 观测、不是目标、无注册且路径项不存在。仅这些 root 的已知 active/selection 与 installed/source runtime 观测承接对象终止；非空模式中其它缺枚举文件仍核原路径实际同值。common/gitdir 与存续真实变化不跳过，省略/[]及同源 profiles 无退出例外。

字段薄传原 engine 前后保持检查，不写 checkpoint 或改原资产源。frozen_recovery_required 仅在输入实际含字段时原样携回，包括 []，唯一 consumer 用已有 presence-select；终态不携。完整 schema/Interface/runtime/consumer/examples/MIGRATION-769 成套采用，旧 D1 闭合 schema 不被声称接受新字段。实际 #766 恢复与目标自身验证在交付后成立；原事务终态及原保留责任结束后，原 owner 明确迁移退出。没有 C5、台账、复活 peer 或第二阶段机。
