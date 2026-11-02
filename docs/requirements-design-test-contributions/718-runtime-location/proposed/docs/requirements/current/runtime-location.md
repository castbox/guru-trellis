# Runtime、位置与明确Git基线

Identity：`RDT-REQ-RUNTIME-LOCATION`；状态：current。来源为[Issue #718](https://github.com/castbox/guru-trellis/issues/718)的完整行为与验收，适用前驱为Git `610a810d45bb30173906d55c77709389adf1cf31`。本单元只拥有本能力；设计由[对应Design](../../design/current/runtime-location.md)单写，验证由[对应Test](../../test/current/runtime-location.md)单写。知识定义与实际安装/交付/Release结果分别成立。

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
| R718-07 / BEH718-BASELINE | 只读基线明确repo/ref/固定commit，Git对象可读时不要求分支检出或其checkout干净。刷新时明确远端ref、采用提交和适用性。未提交/未跟踪内容单独作为候选；不得冒充已提交或已发布authority。 |
| R718-08 / BEH718-OPERATION | 基线读取、候选审核、实际Sync和发布各用自身前置。真实同步仍核目标checkout、dirty、可ff历史和identity。正式Branch Review要求已提交范围，发布要求真实远端候选，Task阶段要求保留原义；只读成功不制造任何正式gate。 |
| R718-09 / BEH718-DRAFT | 外部或已有worktree、无Task和正常草案组合可经实际公开入口读审。结果准确绑定来源与候选，普通变化刷新受影响结果；不能为入口资格要求草案先commit/push或隐式移动其他checkout分支。通用Issue创建仍核目标、最终正文、重复判断、当前审核和真实副作用。 |
| R718-10 / BEH718-CONSUMER | 错选基线提供准确诊断和原入口纠正，不因此取消所有门禁。Sync/Discovery至实际创建consumer成套承接相同来源语义，失败不能只移动到下一步。 |
| R718-11 / BEH718-MIGRATION | 现行指针、公开I/O、维护与rollback给出适用版本、原owner、切换和退出条件。单checkout工具更新不写peer工具/Task/session/用户配置/显式状态，增加cache不改变peer合法实际选择。旧格式来源未知时保留有效兼容选择、公开处理失效hint，不编造历史用户意图；真实显式类别可通过公开入口重表达。 |

## 验收与责任

A1—A8分别观察任意位置启动/物理复用、独立生命周期、稳定显式/默认及版本并存、真实只读consumer终点、必要拒绝/纠正、独立恢复、单目标维护/回滚/旧格式迁移、canonical/dogfood/installed/平台投影与reapply/drift/sidecar。真实正常before/after、正确正向结果及必要拒绝均由本仓准备，行为等价场景共享证据。Markdown路由变化须有代表性实际Agent行为；确定性链路不能冒充该观察。

本项完整性由本仓实现/文档/隔离验收自闭环，不要求业务仓重跑或发布产品Issue。完整多平台Release矩阵、业务采用、Unity pool、共享文档竞争、legacy归档和telemetry保持各自范围。honest正常模型、敏感数据保护和副作用权限保持；不引入恶意伪造/TOCTOU/锁/压力/crash加固。

## 前驱与替代范围

保留#219的隔离Python/真实wrapper、#231共享identity、#556解释器及失败保护、#566单目标维护/rollback。仅替代旧pointer作为启动必要前置以及只读来源继承Sync checkout/clean/三方相等的组合要求。#566其他Task维护和公共模型义务不迁移；其完整历史与仍适用合同仍由原来源拥有。本单元不宣称整个RDT旧语料已迁移。
