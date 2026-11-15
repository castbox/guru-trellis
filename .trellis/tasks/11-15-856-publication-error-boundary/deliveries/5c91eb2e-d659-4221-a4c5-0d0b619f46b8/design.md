# D1：Publish 公共异常边界修复设计

## 1. 设计目标、需求承接与内容基线

承接本批PRD的D1-R1至06、D1-S1至06及D1-AC1至06；完整scope_ref为根PRD的AC856-01至06。目标是使原已分类失败通过既有公共错误合同输出，并保持内部恢复、未知异常脱敏及原副作用边界。

development baseline B固定为 `4f3d9069e0720ec94e39d1079154d2f7a7058935`，来源为本Task实际Sync read及创建decision_head。Planning H0观察为同一commit；实施最终H由真实提交产生，不以H0代替。内容范围是该B至最终H及本次实际增量；PR目标另为castbox/guru-trellis的main。实施以原construct-delivery-candidate公开入口构造完整范围，不选Task/session/private-result为业务content。

实际Architecture candidate_assessment返回baseline_current、no_architecture_impact，baseline为guru-trellis-architecture、constitution为guru-trellis-design-constitution-v1，freshness为sha256:a7d09f83604ccca089e14272fd2a66893a6651aa1505b30bfe64fba896d5c49e。适用authority为 `docs/architecture/README.md`、`00-foundation/design-constitution.md`、`06-governance/change-contract.md`。不新增owner、公共DTO、状态、持久化、I/O或协调层；不建空Architecture contribution或ADR。该候选判断不是最终方案或实现通过，Wording后仍须原独立final_plan。

## 2. 当前系统、边界与目标差额

首次D1，无前序交付。canonical package为 `trellis/skills/guru-team/packages/guru-publish-task-delivery/`，shared command/io位于 `trellis/skills/guru-team/runtime/`。

当前owner.py的WorkflowError继承RuntimeError，仅带code和内部payload；command.main只捕获CommandError，未知兜底实际exit2。package catalog声明internal_error为70。migration.py已有局部转换，使用str(exc)并固定exit3，导致普通JSON/schema错误退出码与安全提示失真。

目标只改原Publish package异常定义、直接入口边界、必要catalog/commands与定向tests。shared command.py/io.py不改，其他package不获得新catalog读取关系或新行为。legacy维护只保持原能力及错误合同，不恢复退役Draft或重放历史动作。

## 3. 来源设计处置（唯一）

| 来源条款 | 原承诺 | 处置与落点 | 理由、影响及上游处置 |
| --- | --- | --- | --- |
| #856最小方案1：原异常类型 | 优先原WorkflowError接CommandError，保构造／捕获／code／payload | retain；第4节原定义继承 | 原内部caller可继续使用；无需改变继承方案或上游合同 |
| 同节：单点与直接入口 | 不在wrapper复制映射，不增协议／DTO | retain；第4、5节静态已知映射与单一私有unknown边界 | 各入口只引用同一helper，未引入全局exception协议 |
| 同节：定位与未声明code | 有据字段或原步骤，不猜message；按真实consumer补最小声明 | retain；第5节 | 保已知状态code，catalog/commands只补实际抛错和入口消费 |
| 最小方案2：typed recovery | 原resume/stale/reprepare及同事务回读保持 | retain；第6、7节 | wrapper在原owner完成内部处理后承接未消费异常，不夺取route |
| 最小方案3：未知异常／脱敏 | 安全internal_error、实际与catalog一致，不泄原message/payload | retain；第4节unknown边界与第5节 | 保catalog声明70；不改其它package或降为2 |
| 验收2、4 | 按真实入口覆盖、复用stateful、定向分发，不重放实际发布或完整矩阵 | retain；第8节与implement第3节 | 验证层级分开，不以内部assertRaises替代公共输出 |

## 4. 模块、职责与设计取舍

### 4.1 已知领域异常

在owner.py原WorkflowError定义处接入CommandError；保现有message、默认code=publication_stale、keyword payload及内部code/payload用途。保留原WorkflowError构造和except WorkflowError消费，不要求额外的RuntimeError继承身份；原message只供内部使用，不进入公共序列化。增加可选field_path仅供有依据的原抛错点使用，旧构造调用无需改动。

静态code表提供安全field/remediation/exit，不采用message、payload、外部stderr或任意异常属性生成公共数据。正常内部捕获仍是except WorkflowError，REPREPARE_REQUIRED_CODES不改。未知code不自动扩展声明；真实遗漏先核consumer再补最小映射，未建立分类依据时保安全internal_error。

### 4.2 真未知异常

owner.py内设置一个package私有public-command boundary，现有invoke.py、check.py、record.py、execute.py的run及recover.py暴露的legacy run共同引用。它先原样传播CommandError（含WorkflowError），仅把未分类Exception转换为静态安全CommandError：internal_error、field_path=runtime、catalog既有维护提示、exit70。不回显异常内容，不吞SystemExit/KeyboardInterrupt，不制造成功出口。

该helper承担本package已声明unknown70所需的直接命令边界，不是“继承不兼容时的第二种已知错误映射”。已知错误仍在原定义接续；两者职责不同。去掉该helper会使实际直接入口的真未知异常仍由shared fallback输出2，与本package原声明不符。五个现有entry是实际consumer；不复制错误表，不在各wrapper新增各自except映射。

替代方案：通用catalog读取会改变大量其它package的unknown行为并新增runtime读取，已排除；package名特判污染shared dispatcher，已排除；把catalog70改2弱化既有声明，已排除。当前方案无额外文件读取或状态成本。

### 4.3 局部适配与消费者

migration.py现有WorkflowError转换改为传播同一安全公共字段／原异常，移除str(exc)与fixed3；保LifecycleContractError已有明确field/remediation和stale语义。record.py是其真实command入口，未知异常由同一boundary承接。recover.py须适配其别名导入的legacy run，否则该声明internal_error的入口会漏掉unknown70；不改变legacy execute的范围、前置或副作用。invoke.py内的legacy分支已在其run boundary内。

## 5. 接口与数据

不增公共输入／成功DTO／状态。公共失败仍为 `{code,field_path,remediation}`，由shared fail序列化，exit_status由CommandError提供；内部payload不得传入response。原CLI参数、typed exit及consumer均不变。

| 实际code | exit | 定位／恢复依据 |
| --- | --- | --- |
| invalid_arguments、invalid_json、schema_mismatch、source_mismatch | 2 | 保原参数层／读取器／schema／source确定字段；原安全提示 |
| closing_keyword_forbidden | 3 | 原关闭关键词抛错点，input.pr_body；使用Refs，Closure保原职责 |
| publication_stale | 3 | 原publication步骤或实际identity字段；回原Review/reprepare |
| external_command_failed | 4 | 原执行步骤，不透传command/stderr；回读同事务恢复 |
| unsafe_path | 2 | 实际task/transaction locator抛错点，原有路径规则；补必要声明 |
| task_not_active、task_identity_stale、repository_identity_stale、remote_identity_stale、pr_identity_stale、private_state_invalid、private_state_missing | 3 | 保原code和内部route用途；只有未被合法内部route消费时输出，定位原步骤或有据字段；补实际catalog与command声明 |
| internal_error | 70 | runtime，静态原package维护指引；不推断具体原因 |

缺readiness_result_id通过原closed-profile检查明确定位input.readiness_result_id；其它集合失配按实际missing/extra或input步骤确定，不新增完整schema诊断框架。JSON `{`仍先由shared读取器给invalid_json/input，exit2。catalog最小新增项按实际抛错集合和commands entry校核，不为未来code预留。

## 6. 状态、顺序、正常与失败流程

没有公共状态迁移新增。顺序为run边界进入→原JSON/参数读取→原owner校验与内部try/except→已完成的正常输出或typed recovery直接返回→未消费WorkflowError由shared CommandError/fail输出→真未知Exception由package boundary转安全internal_error70。

invoke.plan阶段private_state_missing/invalid仍回review_stale；task/repository stale仍原reprepare_required；execute阶段external_command_failed存在同事务时仍resume_publication。它们先被原owner消费，boundary不抢先转换。record/check/execute没有该内部route时，原异常成为有据公共错误，不模拟invoke的业务路由。

## 7. 恢复、兼容、迁移与集成

旧构造和必要内部payload仍有效，当前合法输入、成功DTO、事务内容／digest、Task/Delivery记录与session均不变，无数据迁移、dual reader或额外恢复协议。唯一行为修复是已分类公共错误正确接续、migration不泄原message且退出码正确、真unknown符合本package原70声明。

恢复继续先读真实外部事实和同一事务；不新push/PR/Ready/merge，不移动旧checkpoint。不以G10历史猜测当已证实首次异常。canonical修改经原guru-upgrade-tools同步本checkout受管投影；真实旧业务安装另属原维护owner，不由source绿色推断已采用。

## 8. 验证设计

| ID／AC | 层、入口与输入 | 独立预期与边界 |
| --- | --- | --- |
| V856-1／D1-AC1、2 | 新长期wrapper回归，真实scripts/invoke.sh；原完整example分别缺readiness_result_id、PR body含Closes #435，review给当前合法形状 | code、field、安全remediation、exit2/3准确，拒绝先于Task/Publication读写及Git/GitHub动作；不是修正输入后成功 |
| V856-2／D1-AC3 | Preview、record、check、execute各真实entry必要一例；migration原入口的invalid_json/schema/stale；recover既有legacy入口仅测试错误边界 | 同一已知异常合同覆盖直接consumer；迁移不把2固定成3，不泄message；不做错误×入口全排列或legacy实际写入 |
| V856-3／D1-AC4 | 原test_transaction、test_early_draft、test_remote_recovery与migration stateful fixture；沿已有正常动作／输出丢失／route | review_stale/reprepare/resume仍在原分支，已完成动作零重复；fixture provider只替代边界外GitHub，不制造gate成功 |
| V856-4／D1-AC5 | 实际command/entry边界使下游出现普通未知编程异常，含敏感sentinel；已知external失败带内部payload作对照 | 五entry边界unknown70、三字段安全输出；已知exit4及payload不泄；原CommandError如invalid_json仍2，不输出traceback或sentinel |
| V856-5／D1-AC3、6 | 原shared test_io/test_command_receipts、package全套及source/installed validate、原tools reapply/drift | shared行为无改，合法正常发布/恢复适用覆盖保持；分发mode/sidecar与实际采用分别报告 |

优先补V856-1长期回归再实现；原Issue观察与源码足以建立已知断层，不额外回退旧实现重复红绿。只有新用例是否触达原缺陷仍有疑问时，追加有界旧版本对照。package全套覆盖实际相关consumer，不只跑两例；绿色fixture不证明真实发布／生产效果。完整多平台Release矩阵不执行。

## 9. Canonical 引用、本轮差额与实际未决项

R/D/T定位沿本批PRD第7节；错误确定性边界另读 `.trellis/spec/workflow/companion-scripts.md#Error Handling` 及JSON carriers、`.trellis/spec/workflow/skill-package-contract.md` 的Discovery/Invocation/Error Contract。current-knowledge完整单元与原owner整合规则已读，RDT差额仅补既有lifecycle错误与恢复职责，不新建Issue专属第二current。

无Architecture decision/GAP或owner变化，不制造contribution/ADR。RDT采用implement第6节唯一delta_first计划，由原RDT owner在实施自检后、TaskCommit前final_integration写完整current并读回；committed Review再审真实after。具体测试选择或安装provider缺口由实施时原owner判断，当前无产品未决项。若实际实现需要跨package协议、shared读取或新状态，停止并回Author/Architecture刷新，不借本设计授权。
