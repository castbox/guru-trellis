# D1：Publish 公共异常边界修复需求

## 1. 整体来源与术语

本批 TaskId 为 `856-publication-error-boundary`，generation 为 0，DeliveryId 为 `5c91eb2e-d659-4221-a4c5-0d0b619f46b8`，profile 为 `pull_request`，当前 phase 为 `planning`。planning_root 为 `deliveries/5c91eb2e-d659-4221-a4c5-0d0b619f46b8`。

整体 accepted_scope 为 `.trellis/tasks/11-15-856-publication-error-boundary/prd.md`，revision 为 `sha256:14354858e0322a49d06bd7edfeb3d0f7e2dea9a228d2f9f9eee342f6727d3aae`；本批 scope_ref 选中 AC856-01至06。

| 来源 | 定位、角色与本批用途 |
| --- | --- |
| 整体Task PRD | 上述accepted_scope第1至8节；整体要求，承接R856-01至07、S856-01至06与全部验收，不重新选择范围 |
| Direct Source | https://github.com/castbox/guru-trellis/issues/856 的问题与目标、最小解决方案、验收、相关工作与范围；要求与已约定设计约束，定义异常接续、兼容、恢复、脱敏与验证 |
| 接受评论 | https://github.com/castbox/guru-trellis/issues/856#issuecomment-6894689222 ；审核证据与建议，采用仍适用的调查及只读复现，不代替本批验收 |
| 当前实现 | `trellis/skills/guru-team/packages/guru-publish-task-delivery/runtime/owner.py`、`runtime/invoke.py`、`errors/catalog.json`，及 `trellis/skills/guru-team/runtime/command.py`、`runtime/io.py`；定位原异常、consumer、公共错误合同与退出码 |

Publish、WorkflowError、CommandError与typed recovery沿用整体PRD第1节定义。公共错误是命令边界输出，内部必要payload不因此成为公开数据。

## 2. 整体与本批目标、非目标

当前原owner已分类的WorkflowError未接到共享CommandError边界，普通输入／状态失败被改报为internal_error。本批独立目标是修复该连接，完成实际直接入口、内部正常路线、未知异常及必要分发的定向验证。

D1承担整体R856-01至07及AC856-01至06，没有留给后继Delivery的已知实现要求。交付必须包含真实公共类别、依据充分的定位、安全提示和catalog退出码，不能只改变内部继承关系。

整体非目标全部保留：不实施#850，不恢复早期Draft，不改发布资格、Task／Delivery生命周期或CI／merge policy，不改业务仓库，不重构全局错误体系，不增DTO、异常协议、日志平台、恢复状态或长期账本。不得手工移动／删除历史checkpoint作为恢复，不真实重放发布／旧Draft／push／PR／Ready／merge，不扩张到攻击、锁、竞态、崩溃、额外fault injection或完整Release矩阵。

## 3. 本批起点、前序结果、依赖与剩余责任

这是首次Delivery，尚无前序交付。整体PRD已由原Clarify接受；本批尚无accepted Planning、candidate、Check、full_review、readiness、Publication或delivery结果。公共身份创建不表示门禁通过。

调查基线为 `4f3d9069e0720ec94e39d1079154d2f7a7058935`。当前WorkflowError继承RuntimeError，共享command只捕获CommandError；Issue两项公开只读复现依据仍适用。本轮未重放业务发布，Preview历史额外实验未到达目标行为。

本批依赖原抛错点、内部捕获、各直接入口及现有transaction／remote recovery fixture。技术设计须核其实际关系，不得因现有测试缺覆盖而删除兼容责任。具体方案已写入本批design.md第4至8节；实施顺序和命令集见implement.md第2、3节，仍须后续独立门禁判断。

本批全量范围不等于Task已完成；仍须原Delivery Review、实际交付及整体Completion判断。历史G10首次异常无traceback，旧Draft状态仅为有力解释；不将这一历史缺口变成真实重放义务，也不声称生产效果已验证。

## 4. 本批调用方、场景与流程

| 本批场景／整体场景 | 调用方、条件与动作 | 处理及可观察结果 |
| --- | --- | --- |
| D1-S1／S856-01 | Publish调用方从原生产invoke wrapper提交缺readiness_result_id的delivery_review_ready输入 | 在Task／Publication和Git／GitHub副作用前拒绝；schema_mismatch、依据充分的定位、安全提示、exit 2 |
| D1-S2／S856-02 | 同入口提交其余字段完整、PR body含Closes #435的输入 | 副作用前拒绝；closing_keyword_forbidden、对应定位、安全提示、exit 3 |
| D1-S3／S856-03 | 从原wrapper提交不完整JSON `{` | 共享读取器保invalid_json/input与exit 2，不被改写 |
| D1-S4／S856-04 | 正式invoke、Preview、record、check、execute的合法当前调用触发已分类失败或内部恢复 | 未消费失败接同一公共边界；已被owner合法消费的resume／stale／reprepare保出口和consumer |
| D1-S5／S856-05 | 同事务有已完成动作或未知外部结果，调用原恢复路径 | 先回读并续同事务，不自动重发已完成或未知结果的push、建PR、Ready或merge |
| D1-S6／S856-06 | 出现真正未知编程异常 | 安全internal_error及原维护路径，无原始异常／敏感回显，不伪装为已知业务失败 |

保留原输入校验、owner内部路线处理、共享边界序列化未消费失败的先后关系。公共接续不得提前截断合法恢复，也不改变原gate或执行资格。

## 5. 完整行为、条件与约束

- **D1-R1／R856-01、06，D1-S1、2、4：** 已分类失败保catalog code、客观定位、安全remediation与退出码。字段来自有依据的原抛错点；不足时只定位原步骤，不从message猜字段。
- **D1-R2／R856-02，D1-S4：** 优先在原WorkflowError定义处兼容接CommandError，保原构造、内部捕获及必要code／payload用途。仅在真实consumer证明继承不兼容时用package内单一适配点；不复制wrapper映射，不增协议或public DTO。必要未声明code按真实consumer补最小声明或映射既有类别，不按任意异常属性推断。
- **D1-R3／R856-03，D1-S4：** 原resume_publication、stale／reprepare等合法typed routes保条件和consumer。不改语义审核、scope、readiness、失败条件或发布资格；脚本只承载客观诊断。
- **D1-R4／R856-04，D1-S5：** 失败／未知结果回原owner，先回读并续同事务，不重复完成动作，不新增恢复状态、审计artifact或长期账本。
- **D1-R5／R856-05、06，D1-S6：** 真未知异常保安全internal_error及原维护路径；实际退出码符合本package catalog。公开输出不得含traceback、原始message、外部stderr、命令参数、PR正文、完整payload、环境或凭据；内部保留payload不授权公开它。
- **D1-R6／R856-07：** 原安装owner同步canonical、dogfood与受影响平台，执行定向package／runtime、reapply／drift及必要mode／sidecar检查。仅实际修改需要干净安装证明时至多一个代表throwaway，不做完整矩阵。

既定设计约束的retain／change／reject和具体落点只在本批design.md第3节维护。该矩阵与方案正文现已生成；文件存在不代表后续Wording、Architecture final_plan或Approval通过。

## 6. 本批验收、验证方式与未决项

| 本批验收／整体验收 | 要求／场景 | 入口、输入与必须观察 |
| --- | --- | --- |
| D1-AC1／AC856-01 | D1-R1；D1-S1 | 原生产invoke wrapper缺readiness_result_id；schema_mismatch、有据定位、安全提示、exit 2，拒绝先于发布副作用 |
| D1-AC2／AC856-02 | D1-R1；D1-S2 | 同wrapper PR body含Closes #435；closing_keyword_forbidden、对应定位、安全提示、exit 3及副作用前拒绝 |
| D1-AC3／AC856-03 | D1-R1、2、3；D1-S3、4 | 按真实直接入口补必要覆盖，保invalid_json/input／exit 2对照和合法typed route出口／consumer；不做错误×入口全排列 |
| D1-AC4／AC856-04 | D1-R3、4；D1-S4、5 | 原stateful fixture观察正常发布／同事务恢复，不接真实GitHub写入；已完成动作零重复、未知结果先回读、不绕gate |
| D1-AC5／AC856-05 | D1-R5；D1-S6 | 定向公共边界覆盖真未知异常与公开输出；安全internal_error、catalog退出码和无敏感原值均可观察 |
| D1-AC6／AC856-06 | D1-R6 | package／runtime与原安装owner验证实际分发、mode／sidecar及drift；仅声明实际层级，不声称历史业务发布或Release矩阵通过 |

独立行为期望检验原生产入口；修正输入后成功、直接assertRaises(WorkflowError)或读内部属性不代替D1-AC1／2。采用仍有效覆盖，新增用例须有独立缺陷检出价值。fixture只替代受测边界外依赖，不补偿生产者输出。

当前无须用户选择的需求未决项。继承接续、直接入口覆盖及命令集的规划见design.md第4至8节、implement.md第2、3节；实现与验证尚未执行。执行未到达目标行为时说明具体阻塞，不把设施失败当缺陷复现或验收通过。

## 7. Canonical 引用与本轮差额

| 类别 | Authority／章节 | 本轮承接与差额 |
| --- | --- | --- |
| Requirement／behavior | `docs/requirements/current/task-delivery-lifecycle.md` 的R713-03／BEH713-RECOVERY及R531-05；整体PRD第5至7节 | 保原owner诊断、receipt／typed exit和同事务恢复；补Publish自有WorkflowError接续，不改生命周期或发布许可 |
| Design | `docs/design/current/task-delivery-lifecycle.md` 的Delivery Review／Publish／Merge；`docs/design/current/json-input-carriers.md` 的D695-01、02、04 | 保共享CommandError和已读JSON语义，只增原异常到共享边界连接，不重做parser或恢复协议 |
| Test | `docs/test/current/task-delivery-lifecycle.md` 的T531-05、T713-03；`docs/test/current/json-input-carriers.md` 的T695-01、03、04；`.trellis/spec/workflow/quality-guidelines.md` 的Test And Validation Value、Validation Scope Ownership | 补原wrapper已知失败、适用入口与安全兜底观察；复用恢复fixture，不加全矩阵、固定样本数或真实发布 |
| Architecture | `.trellis/spec/architecture/index.md`及`baseline-usage.md`定位`docs/architecture/README.md`的FOUNDATION／CURRENT；原Adopted-mechanism review | 保共享runtime／package／分发边界；候选拟在原异常定义接共享合同，不增状态、额外I/O或协调层。影响由独立authority-first assessment决定，本PRD不预判pass |

本阶段只写本批需求，未改共享RDT／Architecture authority、根PRD或实现。实际知识差额与必要整合由后续原RDT／Architecture owners处理，不以本PRD直接晋升。
