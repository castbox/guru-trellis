# #575 S5：同源 exact-provider clean 验证与最终准备文档收敛

## 来源与范围

继承根PRD R575-01..07 / A575-01..08；直接来源为 live castbox/guru-trellis#575「Stage 1」「正式依赖前置」「非目标与完成条件」，规范设计约束为私有 release-guru-trellis-version/references/contract.md 的 Two-Stage Lifecycle。WholeCompletion 的 additional_delivery_required 只定位根范围内未分配责任，不修改整体 accepted scope。TaskId、generation、reference_only及既有S1..S4身份保持。

本切片承接一个完整Codex clean样本、真实stable predecessor分离维护的最终适用性判断，以及最终唯一RDT收敛和必要晋升。S4的source helper修复、工具采用及平台/predecessor已有工程事实保留原执行来源，不能把它们重新命名为本切片执行或最终软件发布证明。

## R575-S5-01：从真实已提交修复源完成完整 focused

使用包含输出捕获修复的实际clean committed Guru来源，以及该同一提交的真实远端完整SHA marketplace provider、正式Fork `2a6f10ba3c0a2f27e0587e49e6c2f9b6a1f9d9d0`、CLI/Core `0.7.0-castbox.3` 和原受支持Codex focused profile；workflow provider固定为 `gh:castbox/guru-trellis/trellis#07884d05d746d398c290cd834a9a03192a0e7205`，不启用local-sample复制分支；其它平台、阶段、来源及超时参数保持，执行完整clean/update/reapply/native/session链。必须完成该profile要求的初始化、preset、existing-project update/reapply及当前入口/会话验证，按真实退出码与各阶段结果报告；仅同CLI init、helper回归或版本输出不满足本要求。

不得用dirty source、自建fixture commit、只跑前半段、缩小样本、quiet/过滤/替换解码、放宽timeout或绕过clean/source_locked校验求绿。原focused首次失败与后续捕获修复的原证据保留；新失败按原qualification/诊断/实现owner处理，不提前承诺不存在缺陷。临时样本由既有verifier正常建立，不把样本提交作为正式source_ref。该provider只对应准备提交07884，不是Stage2的最终main exact candidate；必须保留原local-sample/native-init路径的真实失败，不宣称该分支已被修复或通过。

## R575-S5-02：整体定向维护证据的最终判定

按照#578依赖感知工程事实合同，对根A575-01..05、S4工具采用/四平台/B-reapply及真实stable `.3` predecessor分离维护逐项独立判断当前依赖、来源、输入、工具链、参数和期望。可核实且未受影响的原执行事实可采用，说明实际执行来源与理由；缺失、变化或无法判定的必要事实补受影响检查，不重复全部矩阵。

predecessor要求仍包含真实`.3` tag来源、正式匹配旧Fork构建、工具与所选Task分离维护、规划/历史/用户定制保留、目标自身native及下一真实consumer、同operation resume和不兼容单侧tools rollback阻塞。DTO/静态解析不能替代实际目标入口；generic existing链不能冒充该联合证明。已有错误、FAIL/SKIP和证据限制如实保留，不将数量断言求绿维护引入本切片。

## R575-S5-03：唯一最终RDT与晋升门禁

原RDT owner在既有 docs/requirements-design-test-contributions/575-release-preparation/ 收敛全部准备责任和本切片结果，requirements/design/Test/traceability各单写职责，Test拥有真实结果与来源/未验证层次。保留S1独立source-adoption贡献及已经晋升的历史归属，不重写旧测试或归档。

完整准备候选的首次committed全范围独立Review通过且开放finding为零后，原owners以现场expected-current串行执行所需shared RDT/Architecture晋升。无Architecture影响时不制造贡献或ADR；晋升产生的实际diff重新执行fresh Phase2、TaskCommit及不同reviewer的完整Review，之后才能Delivery Review/Refs-only Publish/Merge。不得用S4 Review替代本切片完整候选Review，或以draft贡献冒充current authority。

## R575-S5-04：准备完成与软件发布分离

最终交付仍为中文Refs-only。WholeCompletion必须依据整个accepted scope及所有真实Delivery/验证事实判断；只有准备要求及必要晋升完整满足，才进入reference_only Closure no_mutation、正常Finish/archive/bookkeeping。当前规划、验证成功或PR合并均不提前证明Task完成。

Stage2的最终main exact-candidate、远端immutable provider、最终predecessor发布diff/tag-pinned smoke、annotated tag、GitHub Release和关闭#575独立；本切片不执行这些动作。完整累计多平台/native-host矩阵、真实业务安装升级、原始业务在途任务及生产效果均不声明已验证。

## 验收

| 验收 | 可观察条件 | 整体责任 |
| --- | --- | --- |
| A575-S5-01 | 原完整Codex focused基于实际clean committed修复源和正式Fork执行，各阶段及真实最终结果可核实 | R575-04 / A575-05 |
| A575-S5-02 | 根定向工程事实与真实predecessor维护证据完成当前依赖终审，必要补验无未处理缺口 | R575-01..04 / A575-01..05 |
| A575-S5-03 | 唯一RDT/Test/双向trace完整，必要shared晋升及前后完整独立门禁具备实际结果 | R575-05 / A575-06 |
| A575-S5-04 | 当前完整交付及后续Completion/Closure/Finish仍由原owners判断，Refs-only及Stage2边界保持 | R575-06..07 / A575-07..08 |

## 非目标与停止

不新增公共Skill/API/schema/owner/store/兼容reader/恢复框架，不修改upstream/global/node_modules，不扩张#577或上游#46，不迁移真实业务/生产，不同步caller/main/peer，不清理既有备份/样本/worktree。local-sample已观察到native init先生成legacy bootstrap、随后复制Guru workflow而触发current-only guard。当前机制改用已可寻址的同H direct provider，由CLI按真实Guru contract生成Task，不删除/转换bootstrap，不修改CLI、verifier或guard；未知与失败继续记录。当前要求不授权新增缺陷修复；发现新问题先走原资格与planning/rework，不把验证切片变为未审查的产品重构。PRD只定义要求，design独占来源处置及机制，implement独占DeliveryPolicy和DocsSSOTPlan；不持久化授权或动态发布账本。
