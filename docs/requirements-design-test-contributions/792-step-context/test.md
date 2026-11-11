# #792 验证观察

观察截止：本批实施中的当前候选，尚未形成最终Check或提交。完整拟写策略为[生命周期Test](proposed/docs/test/current/task-delivery-lifecycle.md)的T792-01..06；本文件记录真实执行，不用计划或目录存在证明通过。

## 已执行的行为与回归

| 验证 | 实际执行与观察 | 证明范围 |
| --- | --- | --- |
| V1/V2 | 原source公开wrapper的 `runtime.tests.test_discovery_exits.ExitDiscoveryTests` 11例通过；独立Check执行者又实际运行同组11例通过（17.303s）。包含Skill、条件workflow、stop、instruction-only、无exit、普通错误、合法映射演进及真实schema消费。 | 真实wrapper调用、Interface/图及consumer合同；不证明下游语义通过。 |
| V1/V2 installed | 第二次原tools更新后，managed interpreter执行 `runtime.tests.test_discovery_exits.InstalledExitDiscoveryTests`，2例通过（7.973s）。包含实际installed引用与shared consumer schema的直接读取。此前四类source/installed公开查询对照、unknown/repeated exit停止也已执行。 | 所测查询和schema定位，不是全平台Agent评测。 |
| V3 | `GURU_UPSTREAM_DELIVERY_SCRIPTS=/private/tmp/trellis-plan2-clean-aa898d09/packages/cli/src/templates/trellis/scripts`，由installed managed interpreter运行 `python -m unittest discover -s trellis/skills/guru-team/tests -p test_active_task_continuation_integration.py -v`，4例通过（4.037s）。实际native phase、step、continuation以及hook/public Task/Delivery转换均被执行。 | 原生提取/上下文，不把fixture公共状态转换当作真实业务Planning通过。 |
| V4 | 源workflow识别/转交、managed legacy reference及原维护合同已实际读取。原家族、转换、控制退役、人工归档恢复和准确历史来源仍归原package；#154/PR156终态例及旧provider边界保留。 | 合同可达及语义保持；未执行历史转换、批量维护或历史归档改写。 |
| V5 reader | `python3 -m unittest discover -s trellis/presets/guru-team/scripts/python -p test_step_context_routing.py -v`，5例通过；原verifier的local candidate、content-bound preview/force、用户内容/sidecar保留、坏preview及原错误保留4例通过。 | source/installed明确reference、inline仅显式before观察、缺新引用不fallback、local .new用matching候选source。fixture仅证明reader/preview层。 |
| V5安装 | 原 `guru-upgrade-tools` 三次真实返回tools_upgraded：初次matching采用、补schema locator、补跨layout定位。原owner执行实际目标installed/native/public-operation验证及Task/session/peer/common指针保留核验。最终dogfood drift通过，Claude/Codex/Cursor选择保持，sidecars为0；workflow和两个reference逐字匹配canonical。 | 本checkout的local_candidate维护；不声称完整正式来源安装。 |
| 静态/相关回归 | 原无exit/unknown Skill2例、integration-state图fixture2例、固定#434图fixture2例通过；当前230个active exit shape在模块层被检查。原397个Python文件内存compile、所有workflow/preset Bash的bash -n及upstream ownership通过。独立Check又编译12个变更Python并执行git diff --check，通过。 | 编译、图形状和原边界，不将230个shape称为230次公开或Agent执行。 |

## 实际AI消费与发现后的纠正

当前主Agent实际使用installed `get_context.py --mode phase`、`--mode phase --step 2.1`及`--mode continuation`，读取真实Task/D1选择后按implementing加载原实现入口。正常index没有要求全图或历史家族；continuation保留原producer恢复与phase非pass。原实现入口的边界、Docs及qualifier短适用合同由当前AI实际读取，不由脚本选择语义route。

本次确实在tools维护上下文中读取installed legacy reference和原 `guru-upgrade-tools` 完整合同。随后以真实tools_upgraded出口调用installed公开query，读取返回的原Skill入口、output/projection及consumer schema；其consumer为结果stop，当前AI保留installed_version、原owner的可选恢复引用和formal-source限制，结束该维护链，不把它转为Task/Check/Completion通过。

首次真实消费发现shared consumer schema不能拼在producer contract_root下。原runtime owner补最小 `consumer_schema_locator`，保持原consumer合同及package/shared查找规则；source11例与installed2例覆盖修正，主Agent已按新locator读取真实shared schema。

原native integration首次在旧正文标题断言失败；原hook/public-state两例当时通过。现有提取用例改为经原CLI检查当前入口、必要约束和恢复定位，并增加phase/step加载边界，最终4例通过。workflow搬移早期的临时breadcrumb闭合tag错误由原writer按完整行tag边界修正后，再核验native提取。不是产品行为的原fixture模块级PyYAML缺依赖，沿原测试责任局部延迟到实际使用函数导入，未削弱断言或更改依赖锁。

独立Architecture还观察到source相对Markdown链接在installed不同目录下会错误定位。原writer将workflow三处routing引用和routing返回Manual Git/GitHub的链接改为明确的source/installed repository-relative locators，保留单一marker、图及owner；没有增加alias、重复资产或renderer。该source差额已独立补读。第三次matching更新后，当前AI通过installed原step 2.1实际读取正确的installed路由section locator，并加载原Architecture stage和qualifier profiles章节；共享stop返回Manual操作的实际路径亦正确。随后又用真实tools_upgraded查询并按原合同消费结果stop。source闭合、installed采用和这次AI加载分别成立，不外推所有平台或其他业务入口。

## 尚待观察与未验证边界

V1–V6的本批命中观察已完成。正式Architecture、candidate Check、原知识晋升、after重绑、最终Check与完整committed Review由各原owner实际执行；本观察不预填这些结果，也不要求正文递归记录自己的最终pass或HEAD。

本项没有执行完整多平台安装/升级/Release矩阵。工具来源采用CLI/Core 0.7.0-castbox.6的完整本地开发配对，原owner返回 `unverified=[formal_fork_source_lock]`；不证明正式来源维护、其他仓库采用、生产效果或固定成本降幅。commit/push/PR和merge不属于本观察的已执行事实。
