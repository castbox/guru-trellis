# qualifier 适用条件与调用需求

Identity：RDT-REQ-QUALIFIER-APPLICABILITY；aliases：REQ-793、normal/solution/root
conditional qualification。原语义 owner：guru-maintain-requirements-design-test-ssot。
来源 Issue #793；状态 current，适用源 Git e30c7bb5d4c24bc075dc14cfcd04c1da00fcf78e。
原 RDT owner 从 #793 隔离完整拟写于 final_integration 晋升并读回本单元。前驱是该 Git 中的三原包、
workflow/callers 和 #382 已晋升职责；窄替代范围见下文，其他职责保持。

## 完整要求

- REQ-793-01：normal、solution、root 各自在原职责内拥有可单独读取的简洁适用条件。
  原 caller 在全文加载前按 live authority、真实候选和变化判断是否触发；条件与完整
  Skill 合同一致。未触发不加载全文、不装配形式调用或输出空判定。
- REQ-793-02：条件不能用 OS 词匹配代替全部场景、机制、因果职责。真实故障/保护
  不能改名普通 feature。没有新资格 Skill、固定问卷或逐候选证明文件；原阶段保
  自己的完整判断，真实需求/重大取舍回原入口。
- REQ-793-03：触发时显式加载原 stable Skill，给真实非空适用集合并完成原闭环。
  拒绝、机制修订、诊断、范围选择与 blocked 保原意义和唯一 consumer；脚本成功
  不证明 semantic pass。未触发也不制造替代 classified/skipped 输出。
- REQ-793-04：新建/实质改变的诊断、缓解、修复、保护仍进入 root。不变机制采用
  仍适用结论；阶段/caller 变化本身不重判。authority、机制、条件、支持路径或因果
  证据实质改变刷新依赖判断；丢失必要结论回原 producer 恢复/重新判断。
- REQ-793-05：十类 lifecycle 与已有 Author profile 同步 caller、workflow 条件、包、
  上游前置、输入/出口消费、示例和诊断；不只删除 global mandatory。三 owner 保持
  独立，不重构未受影响算法。root 不要求正确未触发的上游制造实际 outcome。
- REQ-793-06：公共语义变化有 matching 迁移，保合法在途恢复；原安装 owner 同步
  canonical、dogfood 和真实受影响声明平台，包括 Claude Code、Codex。Markdown/AI
  判断，脚本仅确定性事实；不增加无 consumer DTO、资格账本或授权持久化。

## 替代、边界与关系

本单元替代前驱 REQ-382-01 和当前调用合同中固定三项顺序的普遍前置；#382 的
目标感知因果方法、原非通过、无状态、各阶段独立和共同完成边界继续由原包/spec
独占。旧完整安装采用前保原合同，成套采用后按同Task/key/实际阶段续接。

不承接 #736 其他拆分、#734、设备/预算/额度治理或事故重放。不要求固定案例数、
成本比例、评测框架、全阶段乘积或完整安装矩阵。设计见
[DES-793](../../design/current/qualifier-applicability.md)，验证见
[TST-793](../../test/current/qualifier-applicability.md)。实现、分发和目标业务效果
不能互相代证，结果以原 Test 及公共 Gate/Git 事实为准。

## explicit-task 完整身份（REQ-812）

来源为 [#812](https://github.com/castbox/guru-trellis/issues/812)，适用前驱为 Git
f16bb562e4ea844939786cebd5c6c20e686914b2。本节承接已接受目标，由原 RDT owner 在 #812 final_integration 整合；独立 committed Review 尚待执行。
它补充 REQ-793，保留三个资格 owner 的适用条件、语义与原出口。

- REQ-812-01：原 Identity/Ensure/Bind 确认官方 context key 不可得时，七类
  Task/Delivery 资格入口承接调用方真实完整 DeliveryKey。资格事实须验证当前
  Task/generation、C4/C5、唯一 registered checkout、公开 Delivery 关系、Planning
  与候选。成功输出由原 caller 消费并继续该阶段，不能省略既有检查取得成功。
- REQ-812-02：官方 context 存在时，必须校验其当前 Task/Delivery 选择与显式 key
  一致。缺失、错误、terminal 或冲突仍由原 owner 处理，不进入无 context 分支。
  正常 generation、checkout、Planning、候选变化造成的 stale/mismatch 继续拒绝。
- REQ-812-03：normal/solution/root 采用同一共享事实入口。AI 仍独占资格判断，
  classified、机制修订、诊断、范围选择、blocked 保留原唯一 consumer。同 caller
  保留自己当前调用对象，不新增 session writer、选择 authority、资格账本或授权记录。
- REQ-812-04：受影响公开输入采用显式版本迁移，旧发布 schema/id/示例字节保留为
  历史验证资产。原 caller、Interface、示例、runtime selector 与受管投影成套采用；
  旧在途操作通过固定完整原 provider 恢复，未执行的旧输入由原 caller 重装，不能猜 key。
- REQ-812-05：真实原身份 owner、三个适用 qualifier 的公开 wrapper 和 caller 后续
  动作共同证明合法显式路径；正式 context 使用真实官方来源。确定性测试、AI 行为、
  安装投影与交付终态分别陈述，不能互相代证。普通错误在接受范围内，恶意伪造、
  压力竞态、crash 加固及完整多平台 Release 矩阵不在本项范围内。

上述要求对应 [DES-812](../../design/current/qualifier-applicability.md#explicit-task-对象传递des-812)
与 [TST-812](../../test/current/qualifier-applicability.md#tst-812--显式身份与续接)。
整体交付、Closure 和必要归档仍由 Task 原 owners 判断，不以 qualifier success 代替。


## 资格确认 context 接续（REQ-811）

来源为[Issue #811](https://github.com/castbox/guru-trellis/issues/811)，适用前驱Git
ca0b21f0dfc754a6979f919be14deee696719a4b。本节由原 RDT owner 在 #811 final_integration 整合并读回，状态为 integrated_pending_review；独立 committed Review 尚待执行。
保REQ-793/812原职责，新增两类确认的真实context循环。

- REQ-811-01：normal和solution各自真实scope_confirmation_required进入原Clarify；分别处理匹配当前、缺失和正常过期context，
  经原producer完成后由正式clear回原caller。record/check、旧transition或示例不构成正式出口。
- REQ-811-02：全过程保candidate_refs、Task/Delivery、mode、target、continuation和resume consumer。
  Task目标与Task.source对应Issue authority分开；合法no_issue沿实际accepted_scope/draft/source，不能从inventory猜对象。
  官方选择、generation/checkout/Planning及普通stale/mismatch检查保持。
- REQ-811-03：缺失/普通过期context通过原Sync read、Clarify needs_context和Discovery获取；
  load_bearing Issue选择完成原source_actions/live reread后必须refresh，并保身份重读已变authority，
  核已生效选择而不重复mutation后再clear。accepted_scope改变仍回原whole-scope owner。
- REQ-811-04：mutation disposition使用Discovery公开的真实authority_duplicate_snapshot，绑定实际Issue/draft而非Task；
  原duplicate选择及payload/preimage/action校验保持。缺失/stale回原producer，不重做Discovery搜索、不跨读private或手填事实。
- REQ-811-05：旧四类context返回保原current/pinned边界，Skill/exit ID及fail-closed保持。
  公开I/O按明确matching版本成套迁移；旧发布字节仅验证保留，current无双reader、资格store或授权记录。
- REQ-811-06：原tools owner同步canonical、受管dogfood及声明平台并验证。完整回归不预填被测producer输出。
  使用本项独立、受支持的正常Task/Delivery场景验证同一工作接续，保持场景内真实身份；不指定发布Task、版本或发布时间，不为验收捏造未决范围选择。fixture语义输入与真实producer输出分开，原Check按当前验收判断充分性，不新增实际Agent/远端业务证明前置。

对应[DES-811](../../design/current/qualifier-applicability.md#资格确认-context-接续des-811)与
[TST-811](../../test/current/qualifier-applicability.md#tst-811--资格确认context与刷新)。
#812其余输入/输出、分类算法和caller义务保持；整体交付终态仍归原lifecycle owners。
