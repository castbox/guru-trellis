# Runtime、位置与明确Git基线

导航别名：`R718/D718/T718`；`R760/D760/T760`；`worktree配置路径`；`runtime与Git来源`。原语义 owner：`guru-maintain-requirements-design-test-ssot`。`R718/D718/T718` 与 `runtime与Git来源` 别名继承自 Git `f75f0f5dd078a0c2c4c9a54ac861383774162806:docs/requirements/current/README.md` 的原 current 条目；该来源定位原晋升状态及所属完整正文，不将知识状态扩大为实现/安装通过。原定义、来源与关系保持。

Identity：`RDT-REQ-RUNTIME-LOCATION`；状态：current。来源为[Issue #718](https://github.com/castbox/guru-trellis/issues/718)的完整行为与验收，适用前驱为Git `610a810d45bb30173906d55c77709389adf1cf31`。本单元只拥有本能力；设计由[对应Design](../../design/current/runtime-location.md)单写，验证由[对应Test](../../test/current/runtime-location.md)单写。知识定义与实际安装/交付/Release结果分别成立。

本单元 RDT 定义修订：`fixed-git-task-creation-813`。来源为[Issue #813](https://github.com/castbox/guru-trellis/issues/813)，适用 before 为 Git `5c6a4591db7165ece045e6b0eb789c21d06d7d38`。本次细化原 R718 固定来源贯通 Creation 的定义，保留稳定身份、#760/#769 条件和历史观察截止。该标识不是软件版本或最终 Git HEAD；独立 committed Review、Delivery 和 Completion 由其原 owner 建立。

## 概念与适用边界

worktree承载文件和执行位置，branch承载Git历史，Task承载accepted scope/Delivery/生命周期，Python环境提供解释器与锁定依赖。创建者、路径、分支名或环境能启动均不能建立Task/阶段资格。工具代码来自实际采用的安装/检出版本；source-loaded维护的来源、共享环境与目标分别验证。

## 当前行为

| Identity / Behavior | 完整行为与条件 |
| --- | --- |
| R718-01 / BEH718-DISCOVER | canonical/installed/platform公开入口依据实际assets的manifest、lock、runtime API/layout和平台/解释器类别发现并验证共享环境。自动local/gitdir/common指针缺失或失效不能单独阻塞已有兼容cache；启动不要求Task、特定分支或Guru创建的位置。各操作仍核自己的身份和权限。 |
| R718-02 / BEH718-IDENTITY | 同OS用户和平台，相同有效需求复用同物理环境；依赖/API/layout、implementation/major/minor、OS/architecture/ABI变化选择对应identity并允许并存。patch和可执行文件路径不进入identity；不按HEAD、Task、worktree数量建venv。不同解释器兼容类别不是同一有效需求。 |
| R718-03 / BEH718-CODE | 正常目标入口执行其实际assets代码；环境只供运行能力。不能借其他checkout新版代码证明目标安装成功。维护从明确完整matching来源启动，不依赖坏目标dispatcher，完成后调用目标自身入口。 |
| R718-04 / BEH718-SELECTION | 真实显式选择优先，类别不兼容或不可用时准确拒绝并指向恢复，不能静默换类别。无显式选择时使用公开稳定规则复用兼容cache；有效选择不因新增cache、PATH或无关分支变化而改变。初始化/apply/reapply未传解释器使用当时PATH python3；显式--python优先且失效不回退。日常不随PATH重建、不用global site-packages。 |
| R718-05 / BEH718-RECOVERY | 缺cache、损坏、旧自动hint失效及依赖失配须有独立公开check/resolve/repair和准确诊断。维护需要真实CPython3/锁来源时报告具体缺口；不以Task迁移或完整工具重装为前置。日常不安装，维护失败保留旧可用环境和合法选择。 |
| R718-06 / BEH718-LIFECYCLE | worktree/branch/Task创建、采用、切换、结束和位置删除不直接创建、迁移或删除共享环境。依赖需求变化才重新解析，确实缺环境时经独立维护构建。cache清理保留原独立边界，无GC或资源调度。 |
| R718-07 / BEH718-BASELINE | 只读基线明确 repo/ref/固定 commit，对象可读时不要求分支检出或其 checkout 干净。Creation 将固定来源 `{kind,selected_ref,commit}` 与 Task 的 `selected_base_ref`、未来 `delivery_target` 分开；固定对象不与本地同名 branch HEAD 比较，也不随后来 ref 前进改变。刷新时明确采用提交与适用性。未提交/未跟踪内容单独作为候选，不冒充已提交或已发布 authority。 |
| R718-08 / BEH718-OPERATION | 基线读取、候选审核、实际 Sync、Task 新建/恢复和发布各用自身前置。真实同步仍核目标 checkout、dirty、可 ff 历史和 identity；同步型 Creation 新建保留所选本地 base 与审核提交相等。正式 Branch Review 要求已提交范围，发布要求真实远端候选，Task 阶段要求保持原义；只读成功不制造正式 gate。 |
| R718-09 / BEH718-DRAFT | 外部或已有 worktree、无 Task 和正常草案组合可经实际公开入口读审。Creation 按已审核对象与合法 acquisition 建立或采用独立 linked checkout，不采用 primary；primary 的旧 main、index 与无关 staged/unstaged 文件保持，不移动、reset、stash 或代提交。结果绑定来源与候选，普通变化刷新受影响判断；通用 Issue 创建仍核目标、最终正文、重复判断、当前审核和真实副作用。 |
| R718-10 / BEH718-CONSUMER | Sync/Discovery 至实际创建、检查和恢复 consumer 成套承接同一来源。exact commit 必须存在且与 acquisition 起点一致；仓库/common-dir、TaskId/generation、branch binding、位置与 ownership 原校验保持。真实 mismatch 继续拒绝并定位失败字段，错选来源回原 owner 纠正。已完成结果恢复读取原 Task/资源，不重复创建或扫描新建唯一性；同 Task session 保持，缺 record 由原 owner attach，不同或无效 session 阻塞，缺 context 为 explicit-task。 |
| R718-11 / BEH718-MIGRATION | 现行指针、公开 I/O、维护与 rollback 给出适用版本、原 owner、切换和退出条件。Creation 当前调用方成套采用新版闭合来源合同，旧 schema/path/id/bytes 保留为历史验证；旧成功操作由固定完整旧 provider 恢复，旧待执行输入回原 Sync/Intake 重新审核，不猜来源或新增 current legacy reader/台账。单 checkout 工具更新保留 peer 工具、Task/session、用户配置与合法实际选择；旧 runtime 选择来源未知时不编造历史意图，真实显式类别经公开入口表达。 |

## 验收与责任

A1—A8分别观察任意位置启动/物理复用、独立生命周期、稳定显式/默认及版本并存、真实只读consumer终点、必要拒绝/纠正、独立恢复、单目标维护/回滚/旧格式迁移、canonical/dogfood/installed/平台投影与reapply/drift/sidecar。真实正常before/after、正确正向结果及必要拒绝均由本仓准备，行为等价场景共享证据。Markdown路由变化须有代表性实际Agent行为；确定性链路不能冒充该观察。

本项完整性由本仓实现/文档/隔离验收自闭环，不要求业务仓重跑或发布产品Issue。完整多平台Release矩阵、业务采用、Unity pool、共享文档竞争、legacy归档和telemetry保持各自范围。honest正常模型、敏感数据保护和副作用权限保持；不引入恶意伪造/TOCTOU/锁/压力/crash加固。

## 前驱与替代范围

保留#219的隔离Python/真实wrapper、#231共享identity、#556解释器及失败保护、#566单目标维护/rollback。仅替代旧pointer作为启动必要前置以及只读来源继承Sync checkout/clean/三方相等的组合要求。#566其他Task维护和公共模型义务不迁移；其完整历史与仍适用合同仍由原来源拥有。本单元不宣称整个RDT旧语料已迁移。

## 新建 worktree 的项目配置合同

来源：[Issue #760](https://github.com/castbox/guru-trellis/issues/760)完整行为及验收；
本次适用前驱为 Git `8c158381b5bdb61fd961cbb89e23c2d1f659c9aa` 的本完整单元。
以下行为已纳入本单元定义；实际实现、安装与验证状态由对应 Test 观察限定。

| Identity / Behavior | 完整行为与条件 |
| --- | --- |
| R760-01 / BEH760-ROOT | 新建配置生成位置以同一 Git common-dir 下 live topology 确证的 primary 为锚点，读取其 `.trellis/guru-team/config.yml`。空 root 为 primary.parent / (primary.name + '-worktrees')，相对 root 对 primary 解析，绝对 root 直接使用。同项目配置从 primary/linked/detached 调用结果一致；不能猜 common-dir.parent、调用 cwd.parent 或盲信 porcelain 首行。锚点、配置来源或位置真实冲突准确诊断，不覆盖各 checkout 配置。 |
| R760-02 / BEH760-CONSUME | AI 先读 topology/config，再判断新建或采用、命名和精确副作用。环境查询、计划、创建及直接后继消费同一解析事实。正式 Task 由原 acquisition/checker/binding创建；task-free 用普通 Git，创建后读回目录、注册和 linked/non-base 适用性，不创建 TaskId/binding/session/task.json/位置台账。 |
| R760-03 / BEH760-PRECHECK | 配置生成计划与 root/name 解析不符，在首次 branch/worktree/Task 创建副作用前诊断；原 owner 修正计划并重入，不能静默换位置。环境公开预检必须有两个新建入口的真实 consumer，脚本不决定策略或记录授权。 |
| R760-04 / BEH760-LOCATION | 配置生成、调用方真实显式新位置、已有采用/原 Task 恢复分别处理。生成 root 不是 allowlist；真实显式 root 外位置、合法外部 checkout 采用继续合法。AI 自填绝对路径不构成显式意图。恢复按原绑定找原位置，配置变化不重定位或改变 TaskId/generation/Delivery/session/资源归属。 |
| R760-05 / BEH760-MIGRATION | 公开输入加性支持策略，保留已发布省略字段的原绝对 checkout_root 调用；当前 AI 生成计划明确 configured。原 owner 说明实际旧consumer、切换与退出，完整 matching tools更新并核投影/drift/sidecar，保留用户配置与Task/session。不恢复primary写入，不改Codex清理/业务恢复/#759/暖池，不新增映射或长期路径证明。 |

R760-01—05 的设计与测试关系由对应完整单元 D760/T760 单写。原 R718 行为、前驱替代范围和
未迁移边界保持；#212仅提供历史配置承诺，不复用旧实现通过结论。

## R769 / tools peer 增长与既有事务

来源Issue #769；适用before为a5f3ceeabbaccddae65935d97763f5a798f71ca9。R769-01：单目标维护保原common/peer观测值，新增独立peer不因新增键误阻塞，且不进入原backup/write/delete集。R769-02：修复前schema1.0事务有明示同操作恢复；修复executor与原资产source区分，保持原root/source绑定、public pair/plan/ref、preimages和rollback anchor，不reprepare或吸收后续编辑。R769-03：原source/owned/peer真实不匹配仍阻塞，目标own resolver/installed/native独立验证；实际#766原操作恢复是本项验收，工具结果不代表Task完成。设计由D769承接，验证由T769承接。

## R769-D2 / 已核正常退出对象

来源仍为 Issue #769 原事务恢复责任，before 为 D1 delivered head `aaf7f939e83c5a5230ecbb9d9f0827fd5c2e97ff`。R769-04：原 owner 正常退出的位置不再作为存续 peer 改值处理；AI 必须先读原退出结果，缺失本身不证明正常退出。R769-05：只有 frozen 恢复的显式有限位置建立该例外；存续 peer、common/gitdir、原 source/owned 保持和 #759 精确 prunable 边界继续成立。省略/空数组及同源调用保持原义。R769-06：同 ref/action/source/public operation/plan/preimages/snapshot 续接，无重 prepare 或第二状态；retry 保持实际字段存在性和值，完整 matching I/O 配套。D769-D2/T769-D2 单写设计和验证；实际 #766 恢复仍是整体 AC3，工具成功不建立 Task 完成。

## 原生 context 的正常规模行为（#814）

本单元追加定义修订：`context-adoption-814`。来源为 [Issue #814](https://github.com/castbox/guru-trellis/issues/814)，适用 before 为 Git `ce4644392d1ed9815d59071388b9bff9978d1cee`。原 `fixed-git-task-creation-813` 修订及此前条款保持。本节补充原生 context 正常规模行为；设计由对应单元 D814 承接，验证由 T814 承接。

| Identity / Behavior | 完整行为与条件 |
| --- | --- |
| R814-01 / BEH814-CONTEXT | 实际安装的原生 context 入口在正常小规模及约169个合法注册 worktree 下，解析当前会话或显式 Task，返回正确 owner、Task/generation 和唯一 checkout。消除同一次解析内无关重复 Git 开销时，仍须校验全部 eligible peers，保留原 prunable 例外、选中分支独立查询，以及必要 stale/conflict/非唯一拒绝；不能以跳过校验、借用其他会话或只改 PATH 替代修复。 |
| R814-02 / BEH814-PROBES | 公开 tools 的真实 runtime-contract/context probes 保持两个10000ms预算。验证分别记录实际入口、拓扑、Git调用来源与耗时；单次样本不是所有机器或所有 native 命令的延迟保证。外层等待结束先核原 executor，未知终态继续跟随原执行；需要恢复时仍由原 tools owner 使用同一 operation/ref/candidate/plan/preimages。安全诊断、原失败与未自然复现边界须保留。 |

来源代码与目标自身成功仍遵循 R718-03/11；原事务与 peer/common 保持仍遵循 R769。上述条款不改变公开身份格式、Task/Delivery/session writer 或恢复 authority。正式来源采用和实际工程结果分别成立；完整 Release 矩阵及 Task 整体完成继续由原 owner 独立判断。
