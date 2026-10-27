# D1设计：先诊断正常入口，再确定最小修复

## 1. 设计目标、需求承接与内容基线

本批覆盖整体R1–R7、AC1–AC7及S1–S7。当前可执行方案是有界诊断；首次不当停顿和直接owner未知，不能批准一个假定根因的源码修复。诊断完成后仍在同Task/generation/Delivery内，由原Author细化实际机制并刷新命中资格、Architecture、Wording和Approval；实质方案变化重新展示接受。诊断结果不代替修复、行为验证或整体Completion。

选择development baseline B=`13648ae7aff86f1aac6ebe522f206ac238aa06d4`，来源是本次Base Sync核验且本Task无前序Delivery的main。Planning H0当前同该提交，只是观察值；未来候选仍覆盖固定B..实际HEAD及全部dirty内容。PR目标是`castbox/guru-trellis:main`，不以移动的origin/main代替B，不为普通behind重放Reconcile。

独立Architecture已正式返回本candidate_assessment的`baseline_current / no_architecture_impact`。适用baseline为`guru-trellis-architecture`，constitution为`guru-trellis-design-constitution-v1`，project change contract见`docs/architecture/06-governance/change-contract.md`。它仅覆盖当前诊断设计事实；未知修复不继承该结论。当前首失败与因果仍未知，不能声明根因已识别或修复通过。

## 2. 当前系统、边界与目标差额

已有唯一continuation、typed-exit consumer、原Identity/Ensure/Bind/Selection和producer recovery；#419/#657/#679交付与test.md的具体边界保持。当前Task首次D1，无本Task前序Delivery。

本轮只增加可定位的正常入口观察及差额判断。原workflow/Skill/平台入口是待诊断对象，尚未选具体产品文件作改动。没有新增mode、公共DTO/schema、Skill、状态owner、授权存储、OS/process authority、监控或通用恢复机制。当前实施不改上游、全局npm或node_modules。

当前dogfood的10,210个声明package/overlay文件已观察到字节/执行位匹配canonical，sidecar为空；manifest保留e6c3b827 dirty-source来源。它是投影证据，不是完整来源或native行为通过。全局Trellis0.6.17不用于当前验证；source-lock对应Fork `79a97ed60fe19e8f287eaddfa74722b5250ced35` 的现成clean构建CLI/Core为0.7.0-castbox.5。

## 3. 来源设计处置（唯一）

| 来源/条款 | 原承诺 | 处置与本设计落点 | 理由、影响及上游处置 |
| --- | --- | --- | --- |
| #666 当前依据/AC1 | 先核matching安装、前序覆盖、首停及直接owner，证据前不预选机制 | retain；第2、4、6、8节 | 保留根因未知；无源要求变更 |
| #666 行为表/补充条件 | mapped consumer自动承接；真实选择/独立副作用/目标完成分别处理 | retain；第5、6、8节 | 观察实际调用及对话，不降低原门禁 |
| #666 提示可读性三段 | 用户识别动作/目标/影响/选择；必要技术值说明用途；精确绑定保留 | retain；第4、8节V3 | 原审核owner读实际提示与操作，不能用hash数或字数扫描代替 |
| #666 结果未知/部分完成条件 | 原owner先核实际原操作再恢复或stop，零重复mutation | retain；第5–8节 | 不新增操作身份/恢复协议/授权状态 |
| #666 AC2/AC6 | 真实Agent正常入口、等价before/after、不教路由、不外围预跑 | retain；第4、8节V1/V2/V5 | 原生不可运行记未验证，不制造测试通过 |
| #666 AC5/约束 | 同Task/generation/Delivery/规划/适用结果保持 | retain；第6、7节 | 样本恢复与当前Task都保对象；不删除重建或强换mode |
| #666 AC7/验证范围 | canonical/dogfood/installed/平台投影/reapply一致；普通修复不扩矩阵 | retain；第7、8节V6 | 最多一个代表clean安装；未覆盖层次单列 |
| 现行workflow、Interaction Budget、MIGRATION-679 | Markdown判断、脚本事实、原owner/唯一consumer和matching采用 | retain；第4–7节 | 复用现成原子能力；本阶段无公共接口或迁移变化 |

以上来源全部作为当前要求/约束读取；前序test.md仅为历史证据，不转成当前通过。没有change/reject项，不需要另行改外部authority。

## 4. 模块、职责与设计取舍

| 责任 | 输入、行为与产物 | 边界 |
| --- | --- | --- |
| 原实施/诊断owner | 读当前完整来源、实际安装及原记录；建立入口→上一步结果→原consumer→首次不当结束的因果观察 | 只诊断本scope；未有因果不改产品源码 |
| matching安装与确定性工具 | 使用source-lock Fork构建、固定Guru source及README的local workflow sample/full preset路径；核版本、provenance、bytes/mode、sidecar、installed wrapper | 工具不判断semantic pass，不接管下一owner |
| 原生Codex Agent | 在隔离样本经正常start/continue/当前请求入口读取自身安装，独立执行到实际下一owner、真实选择/独立副作用边界或目标结束 | prompt只有事实、目标、边界；不告知应走owner、恢复步骤或预期pass |
| 原Check/独立Review owner | 读原始实际提示、工具调用、精确操作及结果，判断四类行为/可读性/恢复是否满足 | 不以静态词表、runner摘要或自动评分替代判断 |
| 原Author/资格/Architecture | 有证据后形成同D1具体修复候选，做问题/必要性/机制/因果资格和实际影响评估 | 新设计实质变化走原门禁；不把诊断结论扩大为修复批准 |
| 原RDT/Architecture维护owner | 在后续真实修复形成后维护命中的完整当前定义及关系；无差额不造空贡献 | 晋升仍在candidate Check后的final_integration |

选择有界诊断的原因是当前根因未知，且AC1明确要求因果先于修复。直接补“自动继续”同义句不能证明修复，因此不采用。全生命周期文案重写、新wrapper或监控会扩大owner/状态和范围，亦不采用。当前诊断不删除或替换既有原子能力。

## 5. 接口与数据

本阶段无公共输入/出口/schema/API字段变化。生产者/消费者仍为实际Interface声明：上一步真实public DTO→唯一consumer；DTO丢失→原producer恢复或fresh语义重审。normal/stale/未知出口分别按原合同处理，不用测试driver重建producer私有结果或派生receipt。

测试事实包括本轮目标、入口、安装来源、显式TaskKey/DeliveryKey、真实当前phase、上一步实际结果及原操作引用。它们供Agent自己核对，不在prompt携带route选择或pass。原始执行结果保留其真实层次；长期文档只保必要去敏因果、结论、验证结果及直接来源，不建立授权/问题状态账本。

实际人类授权及本会话确认不进入测试文件或结果；模拟样本对话必须标明测试用途，不冒充生产授权。仅隔离样本内部的本地Git测试动作可由对应测试请求和原owner合同执行；不操作真实业务remote，不新增本Task提交或发布权限。

## 6. 状态、顺序、正常与失败流程

1. 固定原始目标/输入、matching来源及样本起点。核完整当前合同，先区分旧安装采用差额；不从旧版本结果归因当前源码。
2. 通过正常入口运行真实Agent，读其最初异常结束前的实际结果及应进入的原consumer。工具/子Agent/CI等待、合法副作用、真实选择、目标完成分别标注，不把正常stop判为缺陷。
3. 若存在当前失败，保留原对象和失败输入，检查入口是否加载、owner是否被调用、真实出口是否消费、普通调用错误/真实stale是否沿原路径处理。比较更近原因的解释，明确竞争解释与反事实。
4. 形成具体差额后回原资格/Author/Architecture，更新本D1实际方案及受影响门禁。当前诊断规划不执行未知源码修复。没有当前复现则继续可定位历史失败→实际修复因果→当前正向/必要停止的核验；记录不足留真实未完义务。
5. 对允许的具体修复，用原目标/入口和等价条件作after。保留同Task/generation/Delivery及适用规划/结果，不以重建身份获得成功。真实变化只刷新受影响原owner。
6. 按S1–S7和V1–V6收敛证据。当前阶段结束只表示诊断输出已形成；不提前进入Task Completion/Closure或宣称根因修复。

没有新增公共状态转换。正式Planning/Check/Review/Publication/Delivery/Completion阶段仍由原公开writer拥有；任何测试fixture预置数据不能冒充其当前语义通过。

## 7. 恢复、兼容、迁移与集成

同范围普通调用错误沿原owner完整重建/重审，不只补私有hash或改producer。丢失semantic结果回原语义producer；已经发起的commit/push/创建/merge先由原操作owner读实际状态及同操作引用，只补剩余结果。未知或不唯一时stop，不二次mutation，不因迟到/重复回复重做或绑定后续操作。

本阶段无安装目标版本切换或公共schema迁移。代表安装采用完整matching workflow/preset；已有样本更新/reapply沿原installer及冲突/sidecar合同，不手写manifest/lock/版本或裁掉validator。当前Task、并行worktree和前序#679资源保持。新源码修复的采用边界由具体候选补充，不把source parity当业务安装已升级。

失败时保留原样本和事实，回具体owner处理缺来源、环境、版本、归属或冲突；不删除重建Task、不切task-free、不重启Intake、不改上游。没有业务数据迁移、生产写入或部署，故不设计生产回滚协议。

## 8. 验证设计

| ID | 对应范围与实际入口/输入 | 必须观察及限制 |
| --- | --- | --- |
| V1 | R1/R2，S1/S5，AC1/AC2/AC6；一个matching安装的真实Agent从正常入口收到明确对象及本轮目标 | 实际逐步调用原owner/consumer，定位首个不当停顿及因果；无当前失败如实报告，不能凭关键词/fixture关闭 |
| V2 | R3/R5，S3/S5/S6，AC4/AC5；原owner已有的同操作结果丢失/部分完成及普通构造错误入口，真实可定位操作事实 | 原owner先核结果，恢复或准确stop，零重复mutation；保持对象/规划/适用结果；不加故障注入协议 |
| V3 | R3/R4，S2/S3，AC3；读取V1/V2实际生成的确认/方案提示及其精确执行对象 | 原审核owner判断动作、目标、影响、真实选择、推荐/取舍和技术值用途；简明不损精确性；不靠字数/hash/词表 |
| V4 | R6，S4/S7，AC4；真实请求限定仅某步/停止、已完成目标、正常等待及真实依赖/版本阻塞 | 正确结束或必要stop；不扩后续操作、不误判平台审批/等待、不伪造通过 |
| V5 | R1/R7，AC1/AC2/AC6；当前失败原目标/入口的before/after；或可定位前序历史修复与当前正常入口核验 | 逐项对应输入→首停→原因/实际改动→consumer/最终结果；无法成立等价或历史因果时保留缺口 |
| V6 | R7，AC7；受影响package/runtime、三声明平台投影、代表clean安装、reapply/drift/mode/sidecar | source/package、安装、native分层；完整多平台矩阵、其它客户端/mode、业务采用及生产未覆盖单列 |

当前尚未执行上述行为矩阵。原生运行目标使用用户指定的gpt-6.1-sol/high与实际Codex CLI；实际客户端、版本、mode、来源和失败如实记录。定向package用例由命中的实际差额决定，不先扩大成全仓套件。

## 9. Canonical 引用、本轮差额与实际未决项

命中RDT-REQ/DES/TST-LIFECYCLE的R531、R657、R679及candidate-applicability完整单元；这些原定义已读。精确合同仍由canonical workflow、对应packages与Interaction Budget单写。Architecture当前authority/constitution/change-contract及本次实际candidate结果见第1节；当前无contribution或ADR需要，不创建占位。

现有10,210文件一致与Fork构建定位仅支持诊断起点。完整来源和native证据、首次不当停顿及原owner仍待V1–V5；由原诊断/Author承担，不要求用户补技术设计。若形成真实修复，其RDT差额和Architecture影响需在原owner边界明确后才进入实施；当前stage不能据未知修复宣称整体验收。
