# Runtime与Git来源的设计合同

导航别名：`R718/D718/T718`；`R760/D760/T760`；`worktree配置路径`；`runtime与Git来源`。原语义 owner：`guru-maintain-requirements-design-test-ssot`。`R718/D718/T718` 与 `runtime与Git来源` 别名继承自 Git `f75f0f5dd078a0c2c4c9a54ac861383774162806:docs/design/current/README.md` 的原 current 条目；该来源定位原晋升状态及所属完整正文，不将知识状态扩大为实现/安装通过。原定义、来源与关系保持。

Identity：`RDT-DES-RUNTIME-LOCATION`；状态：current。承接[完整需求](../../requirements/current/runtime-location.md) R718-01—11 与 R760-01—05；[Test](../../test/current/runtime-location.md)拥有验证策略与实际观察。Architecture继承 `guru-trellis-architecture` / constitution v1 / ADR-RUNTIME-LOCATION。

本单元 RDT 定义修订：`fixed-git-task-creation-813`。来源为[Issue #813](https://github.com/castbox/guru-trellis/issues/813)，适用 before 为 Git `5c6a4591db7165ece045e6b0eb789c21d06d7d38`。本次细化原 R718 固定来源贯通 Creation 的定义，保留稳定身份、#760/#769 条件和历史观察截止。该标识不是软件版本或最终 Git HEAD；独立 committed Review、Delivery 和 Completion 由其原 owner 建立。

## D718-01 / CON718-ENV：环境身份与代码

原bootstrap拥有identity、user cache、锁依赖、capability和真实public wrapper检查。环境需求使用runtime API/layout、lock digest和implementation/major/minor、OS/architecture/ABI，不使用patch/path、Git HEAD、Task或位置。实际目标代码由本次assets提供，seed只运行标准库解析/维护。最终业务命令仅在被选受管环境执行；global site-packages与其他checkout新版代码不能证明目标成功。

## D718-02 / CON718-SELECT：选择与可重建hint

当前选择在checkout-private `.trellis/.runtime/guru-team/python/selection-v3.json` 保存3.0格式，区分自动模式和显式Python兼容类别。旧 `active.json` 原文保留供旧installed读取，不双写。显式类别只表示implementation/major/minor及平台/ABI，日常不依赖原路径仍存在；同类别patch/path复用。按当前assets要求优先验证对应hint，无有效自动hint则按runtime identity字典序验证已有cache，选择首个有效匹配者并缓存解析结果。每需求hint支持不同依赖切换与切回，不增加全局偏好或时间顺序authority。显式类别缺少匹配环境则拒绝并恢复，不换类别。

初始化/apply/reapply未传--python使用当时PATH python3并保存自动选择；显式--python优先且失效不回退。日常不安装、不因PATH变化重选。自动hint是可重建定位信息，不提供Task/阶段/授权资格。

## D718-03 / CON718-REPAIR：独立维护

原环境owner公开check、resolve、repair：check只读，resolve仅缓存已验证定位，repair需要真实CPython3和锁来源，沿原candidate→locked install→probe/真实wrapper→成功切换。缺seed、缺cache、损坏、依赖失配和显式类别失配输出安全稳定JSON诊断。失败不提前替换此前可用环境或选择。目标dispatcher坏时，从明确matching source可达环境检查/恢复；工具维护仍归原upgrade-tools。每次维护后由目标自身resolver/installed/native入口证明结果。

## D718-04 / CON718-BASE：明确Git对象和实际同步

原guru-sync-base公开invoke以operation=read请求只读明确base_ref及适用base_commit；输出baseline_ready，base为明确git_object来源，携带selected_ref、固定commit和局部一致性identity。原operation=sync及既有调用继续原synced语义：实际目标checkout、clean、可ff历史和三方identity检查。只读不fetch、不ff、不要求所选分支检出或无关位置干净。所选固定commit与后续无关ref前进区分，刷新由caller明确请求和采用新来源。

来源 variant 由 canonical Interface/schema 独占字段版本；新来源不能伪填 decision/local/remote 三个角色。原 Sync/read 与实际同步迁移仍由[MIGRATION-718](../../../trellis/presets/guru-team/MIGRATION-718.md)拥有。Creation 当前迁移由[MIGRATION-813](../../../trellis/presets/guru-team/MIGRATION-813.md)拥有：package input 2.0 引用 shared task-creation-input 3.0，必填 `reviewed_base_source={kind,selected_ref,commit}`，移除 current `reviewed_base_head`。

AI 从实际 ready.transition.base 薄投影：git_object 原样复制三字段；synced 来源将 selected_base 归入 selected_ref、decision_head 归入 commit。`selected_base_ref` 独立选定 Task integration branch，传官方 task.py --base-branch 并限定非 base/non-target checkout；delivery_target 保留未来交付职责。归一化层用 exact `git cat-file -t` 确认对象为 commit，核同 common-dir 和 acquisition.decision_head，不追读较新的同名 ref。只有 synced_branch 的新建路径比较所选本地 branch 与 commit；git_object 不要求 primary main 同步。

## D718-05 / CON718-CONSUMER：真实读取与链路

Discovery读取固定tree的Docs/code/tests/blob/archive index，复核实际source对象；草案工作区独立绑定。公开source读取事实命令只服务该owner/Agent查看真实内容。保留current-state→history→语义gate顺序。base来源通过五阶段transition及Clarify回程、Wording、Readiness和CreateIssue/Task的薄projection承接。每consumer只读其必要字段，不读上游private artifact。

Creation 创建、检查与恢复复用 `normalize_creation_inputs`，保持 exact source、仓库/common-dir、Task/generation、branch binding、位置与 ownership 条件。`prepare_creation_inputs` 另核新建专属 linked/non-primary 资格、synced branch freshness 与 precreation uniqueness，再由原 acquisition/官方 Task/C4/C5/session owners 执行。错误字段经原 optional diagnostic 指向原 owner，不用异常文字改写掩盖失败。

结果恢复仅核原 source/acquisition、Task、binding 和 resources；不重复新建、不再执行新建唯一性或后来的 local branch freshness。旧 completed primary 结果保留原只读恢复，不重新开放新建 primary 采用。同 Task/generation/ref session 不改，缺 record 可由原 session owner attach；不同或无效 current route 阻塞，缺 context 以 explicit-task 续接。正式 committed Review 和 remote 发布约束保持；无 Task/外部 worktree/dirty draft 读审不建立正式 gate。错基线和普通候选变化仍回原纠正/刷新路径。

## D718-06 / CON718-CUTOVER：旧选择与rollback

旧v2来源未知，不推断曾经显式或自动。当前assets兼容有效时保留原物理环境；失效时作为可替代hint查兼容cache。需要持久显式类别时用当前公开--python入口表达。只有新载体不存在时才按原local/gitdir/common读取v2一次；新载体成立后只读写当前格式，新载体存在但无效时准确拒绝，不能回退旧来源丢失显式约束。不新增来源认证或授权账本。

工具维护只写目标checkout私有选择，common/peer载体不变；共享cache新增也不能改变peer已成立的合法实际选择。原rollback先核公共tools/data兼容，再按原preimage恢复目标工具和新旧选择载体的实际存在与原文；旧工具仍读取原v2。公开`--print-active-pointer`返回新writer locator，实际解析值由`--check`/resolver提供。旧完整安装按固定原合同继续，切换与退出由原runtime/installer/maintenance owners执行。cache不随位置/Task生命周期删除。

## D718-07 / CON718-BOUNDARY：知识与分发

canonical workflow/Skill 负责操作选择与语义，确定性脚本只执行和校验。current Creation Interface/commands/examples/真实调用方成套切到新版；旧 schema 验证资产原样保留，当前入口拒绝旧请求。旧成功操作使用固定完整旧 provider 恢复；旧待执行请求回原 Sync/Intake 重新形成来源。没有来源猜测、current fallback、第二状态或新的授权记录。

canonical/package/dogfood/installed/platform、mode、reapply/drift 和 sidecar 使用 matching 原安装 owner 成套更新，不能手抄受管副本。RDT 与 Architecture 先写完整隔离 proposal，批准 Planning、实施和真实工程验证后，由原 final_integration 在提交前整合并读回。结果仅为 integrated_pending_review；TaskCommit 纳入全部 after，再固定 committed candidate，由同一次新独立 Review 判断 Architecture before/after 与完整质量。此处采用当前提交后独立审核合同；历史 #760/#769 当时的 candidate Check 观察保持其截止，不作为当前门禁顺序。

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
按原冲突与sidecar处理并验drift，不手抄dogfood。当前RDT与Architecture整合及独立审核
采用D718-07的提交前final_integration、TaskCommit、提交后同次独立Review顺序。
#760当时的candidate Check观察保留历史截止，不作为当前整合前置。完整Release矩阵仍归专门owner。

## D769 / 原事务、原资产与修复执行器

承接R769-01—03。原upgrade-tools保持原观测键逐项同值，新增peer核物理隔离而不刷新基线。新recover_frozen_source原必填输入为profile/action/recovery_ref，D2按下节加性支持有限退出位置；完整修复源执行当前engine，cp.source完整原源加载原installation helper/installer和资产，保原身份及owned freshness。既有同源profiles保持原义。preset是pending续接，complete只验证；原公共operation恢复不reprepare。rollback先公共compatibility再原Guru preimages。frozen_recovery_required保同profile/action/ref回原owner，原成功/blocked语义保持。公开细节及schema由package/MIGRATION-769拥有；真实旧schema1.0消费者含#766，终态和原保留责任结束后明确迁移退出，无数据转换或第二台账。Architecture由ADR-TOOLS-FROZEN-SOURCE-RECOVERY与ARCH-RUNTIME-LOCATION约束。

## D769-D2 / CON769-RETIRED：调用期退出位置

承接 R769-04—06；Architecture 继承 ARCH-RUNTIME-LOCATION 和 ADR-TOOLS-RETIRED-PEER-OBSERVATIONS。原 tools Markdown owner 读取实际退出 owner 结果并作适用判断，非空 retired_peer_roots 只携准确绝对位置。executor 复用原 parser 读取包括 prunable 的完整注册；核 root 来自原 checkout-local 观测、不是目标、无注册且路径项不存在。仅这些 root 的已知 active/selection 与 installed/source runtime 观测承接对象终止；非空模式中其它缺枚举文件仍核原路径实际同值。common/gitdir 与存续真实变化不跳过，省略/[]及同源 profiles 无退出例外。

字段薄传原 engine 前后保持检查，不写 checkpoint 或改原资产源。frozen_recovery_required 仅在输入实际含字段时原样携回，包括 []，唯一 consumer 用已有 presence-select；终态不携。完整 schema/Interface/runtime/consumer/examples/MIGRATION-769 成套采用，旧 D1 闭合 schema 不被声称接受新字段。实际 #766 恢复与目标自身验证在交付后成立；原事务终态及原保留责任结束后，原 owner 明确迁移退出。没有 C5、台账、复活 peer 或第二阶段机。

## 原生 context 来源采用与解析职责（#814）

本单元追加定义修订：`context-adoption-814`。来源为 [Issue #814](https://github.com/castbox/guru-trellis/issues/814)，适用 before 为 Git `ce4644392d1ed9815d59071388b9bff9978d1cee`。原 R718/D718、D760、D769 与 #813 条件保持；本节承接对应 Requirement 的 R814-01/02，实际观察由 T814 拥有。

### D814-01 / CON814-FACTS：原生解析内事实复用

原生 context/session 身份解析由固定 Fork 的 `session_storage.py` 拥有。一次同步 `RepositoryFacts` 解析内合并 toplevel/common-dir 查询，复用已经成功核验的工作区事实；既有分支拓扑缩小 Task 候选后，选中分支仍独立查询。全部 eligible peers、原 prunable 例外、唯一位置及必要拒绝继续执行。解析结束即结束该局部复用；Guru 不复制身份算法，不增加跨调用缓存、持久 store、锁或新 writer。

该选择减少正常多 worktree 下重复 Git 子进程，同时保留原身份条件。维护成本限于固定 Fork 来源、匹配构建、原工具投影与定向回归；正常规模计时由 Test 限定对象和环境。若 Task/C4/session 协议、拓扑条件、prunable 语义或原生入口变化，原实现与审核 owner 重新评估受影响路径。

### D814-02 / CON814-ADOPTION：原 owner 采用与接续

采用来源由 canonical `trellis/presets/guru-team/source/trellis-source.json` 拥有；CLI/Core 必须从该 lock 的同一精确 Fork commit 成对构建。版本字符串相同不证明源码相同。完整 Guru source 经原 `guru-upgrade-tools` 对显式单 checkout 做 preview、一次 prepare 和冻结 invoke，目标自身 resolver、installed/native 与受管投影分别验证；D718-03/06/07 与 D769 的 source/target、Task/session、peer/common 保持及 rollback 合同继续适用。

开发 `local_candidate` 保留 `formal_fork_source_lock` 未验证标记。实际包含新 lock 的 Guru commit H 形成后，从完整 H 及其自身 lock 重新 preview，再建立独立 `source_locked` 操作，workflow provider 固定 H；不能把开发结果改名为正式结果，或复用旧操作来替换其 candidate。若正式采用产生内容差额，原实施/TaskCommit owner 纳入真实候选并刷新受影响证据。

原 probes 仍真实执行且各为10000ms。外层等待结束不判定 executor 失败：先读原执行 handle 和原操作；仍运行则继续跟随，需要恢复则消费原 ref，保留原 operation/candidate/plan/preimages，不 reprepare 或放宽 candidate_mismatch。没有自然重现历史超时时，报告新样本和原 ref 接续事实，不把它们写成旧历史事务恢复。

该采用复用原安装/恢复 owner，无公共 API/schema/Task/session 迁移。只有来源配对、原公开 probes/恢复协议、实际写集或兼容义务变化时重评。必要 RDT 整合/readback 只建立 integrated_pending_review；TaskCommit 后的完整独立 Review 和后续交付仍各有原 owner。
