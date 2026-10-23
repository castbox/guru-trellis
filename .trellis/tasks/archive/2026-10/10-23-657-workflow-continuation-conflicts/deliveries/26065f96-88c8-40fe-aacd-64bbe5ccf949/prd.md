# D1：活动任务续接与迁移残余合同收敛

## 1. 整体来源与术语

唯一来源：https://github.com/castbox/guru-trellis/issues/657 完整F1–F6/R1–R7/V1–V12。整体范围为Task根prd.md的公共accepted_scope；本批scope_ref选R1–R7。planning_root由公共DeliveryKey 26065f96-88c8-40fe-aacd-64bbe5ccf949拥有。Task/Delivery、created、公共phase与semantic gate的区别按整体术语保留。

## 2. 整体与本批目标、非目标

本批全量收敛F1普遍created、F2退役identity/status文字、F3 Review旧status前置、F4 verifier退役owner、F5 Selection初始Author、F6 scope旧DTO/clear路径。目标是正常独立clone和既有阶段可由正确owner继续写入；初始创建精确恢复保持。

本批排除649阶段成果、656发布矩阵、业务留白与现场升级、任意legacy fallback、历史资产全量删除和未要求的加固。公共API变化只在当前consumer必要时提出并附迁移，不制造新状态authority。

## 3. 本批起点、前序结果、依赖与剩余责任

首次D1，无前序Delivery。固定main B=319202beab79c7666ecdb855291bf117e43d407e，PR目标main。匹配上游source-lock e9fb95fd2eb0fb8441153e77384a9dfd3ea3358f。六类差额均尚未实现，现有诊断不算修复通过。D1承担全部V1–V12及当前RDT/Architecture差额；合并后Completion还须审查整体范围与证据，不因Delivery合并自动结束Task。

## 4. 本批调用方、场景与流程

SC1 原Task owner在无created的独立clone，Identity/Establish/rebind/Ensure/Bind后进入实际阶段写入。
SC2 原Creation新建/初始结果丢失，保留精确generation、初始binding和ledger恢复。
SC3 以明确key选择或恢复已处于planning/implementing/checking/reviewing/publishing的Delivery，保留阶段和适用结果，交实际owner。
SC4 公开范围变化，pre-Author scope_ready→整体PRD Author→Clarify acceptance→post-Author scope_ready→同Delivery合法rework/stop；无Delivery则按义务Creation/Completion。
SC5 当前Discovery/Review/verifier读取同义合同；旧输入拒绝后给合法下一入口。
SC6 ref不可取、身份歧义或checkout不匹配，在错误写入前准确停止，不覆盖他人工作。

## 5. 完整行为、条件与约束



### R1. 区分初始创建与既有活动任务续接

明确 `guru-create-task:created` 对初始创建及其直接 consumer 的适用范围。既有活动任务应由当前身份、合法 binding、唯一 checkout 和实际阶段 owner 承接；原创建 DTO 不可得不能单独阻塞合法续接。

优先修订原 workflow 和原 owner 的合同。若确有必要调整 runtime、公共 I/O 或恢复接口，只修改承载本缺口的部分；公共 API 变化须提供明确兼容或迁移合同。不得放宽初始创建结果恢复的精确校验来模拟活动任务恢复，也不预设必须新增 Skill、DTO 或持久化证明。

### R2. 保留原任务并恢复正确写入 owner

对于已提交且可获取的活动 Task，以及存在时的 Delivery/必要代码，独立 clone 无原机私有 runtime 或创建 DTO，完成正式身份、绑定/rebind、checkout 及适用 session/explicit-task 解析后，应进入同一任务的实际 owner。

保留 TaskId、generation、source、合法当前绑定、已有业务工作、规划和交付历史。不重复创建 Task 或空 Delivery，不倒退旧状态，不补造 created、初始 binding、资源 ownership 或历史 semantic pass，不以复制原机隐藏 runtime 为解决办法。不可获取的必要输入或真实身份歧义，应准确报告具体缺口及原处理 owner。

### R3. 范围变化与正常续接均使用当前门禁

- 无范围变化时，沿同一 Task/Delivery 的当前阶段续接，按实际变化刷新受影响的原 owner；不得仅因缺少创建 DTO 重跑初始创建。
- 公开需求权威发生变化时，沿当前 Clarify → Author 及受影响阶段处理。整体范围由 Task 根 PRD 承接；Delivery 的 PRD、Design、Implement Plan 由对应 owner 在实际受影响时更新，不重新创建 Task 根 design/implement 或覆盖历史 Delivery。
- 重新执行实际受影响的范围、规划、Architecture、措辞、批准及激活/实施前门禁。身份、checkout 或公共 phase 通过不能代替语义批准。
- 每次 source、test 或 task artifact 写入前，仍执行现有 live checkout 边界校验。身份/绑定/checkout 不匹配时，在写入前停止，不改写原 checkout 或无关 Task。

### R4. 合同与分发一致

同步 canonical workflow、受影响 package/interface/recovery 合同、spec、dogfood 与声明平台投影。通过正式 marketplace/preset/overlay 机制分发，处理相关 sidecar 和漂移；不得只在业务仓库临时修改生成文件绕过限制。

### R5. 收敛同类旧前置与恢复路由

对 F1–F6 逐项对齐当前 producer、entry precondition、identity、typed exit 与唯一 consumer。AI 可读 workflow/Skill/Interface/spec 与当前执行路径必须表达同一合同；合法续接不能因缺少已退役字段、旧状态或旧 owner 而停止。历史/pinned-old 资产保持明确版本边界，不自动成为 current fallback。

若扫描后实施发现同一正常路径上的遗漏，须先提供真实 current caller/consumer、authority 和冲突证据，再由原 owner 判断是否属于本 Issue 必要收敛。该要求不授权借本 Issue 重构整个流程、删除所有历史资产、增加通用兼容层或扩展不相关缺陷。

### R6. 已有 Delivery 的选择与恢复保持实际阶段

新建 Delivery 仍按初始规划链进入 Author。选择明确的既有 Delivery，或在其已合法前进后恢复同一身份，必须重新读取当前公共阶段及适用结果，由原阶段 owner 续接。只有实际仍处于 planning 且符合当前 Author profile 前置时，才进入相应规划 owner。

不得以 `created` 名称推定对象刚创建、尚无规划或必须重做初始规划；不得将阶段本身当作 pass。源选择确实缺失、scope 变化或 gate 失效时，按原 owner 的真实恢复/返工义务处理，不丢失原阶段、历史和仍适用工程结果。公共 exit/schema/consumer 若需变化，提供明确版本及迁移合同，不静默改变既有 API；不预设必须新增 exit、Skill 或持久化阶段缓存。

### R7. 范围修订消费当前两阶段结果

正常 `revised`、`no_change`、`withdrawal_required` 都按原 owner 的实际输出和当前义务承接。先完成 scope-only Author 和 Clarify acceptance；只有 post-acceptance 结果才允许对应阶段 owner 执行范围返工或 stop/release。没有当前 Delivery 时按实际范围进入显式 Creation 或 Completion，不为了撤回创建空切片。

修订当前 workflow、managed spec 与分发投影中的旧 consumer/profile/DTO 指令，保留当前单写 owner 与公共 API。历史旧4.0/1.0段明确标为其适用版本，不重新解释旧 DTO，不恢复旧 Task status、activation writer 或跨 owner 私有状态读取。只有文本、schema和实际 consumer 一致后，才能宣称合同收敛；入口诊断或绿色结构检查不能代替完整接续验收。



## 6. 本批验收、验证方式与未决项



| 编号 | 场景与入口 | 可观察结果 |
| --- | --- | --- |
| V1 | 当前受支持的固定 Core/CLI/Guru 组合；已提交且可获取的活动 Task/Delivery 位于明确 ref；独立 common-dir clone 无原创建 DTO 和原机私有 runtime，从正式当前入口解析并续接 | 保留同一 TaskId/generation/source 和实际 Delivery，进入正确 owner，并完成一次该阶段合法规划或实施写入；不能只验证身份解析或手工拼接 DTO |
| V2 | 正式 rebind 后 binding revision 大于零，沿 V1 续接 | 使用真实当前 binding/checkout 完成对应 owner 写入；不调用初始创建恢复来冒充成功，不重复创建资源 |
| V3 | 公开权威发生真实范围修订，沿当前 scope-change 路径处理 | 原 owner 更新整体 PRD 及受影响 Delivery 规划；若三份 Delivery 规划均受影响则全部更新，重新执行受影响门禁后进入实施前校验；旧规划与交付历史保留 |
| V4 | 无范围变化的同阶段正常续接 | 不因缺少创建 DTO 被阻塞；保留仍适用工程结果，只刷新实际受影响的原 owner/检查，不继承失效 pass |
| V5 | 正常 stale/mismatch、身份歧义、checkout 不匹配或必要 ref/输入不可获取 | 返回具体停止原因及原处理 owner，在错误写入前停止；原 checkout、普通已有工作及无关 Task 不被覆盖 |
| V6 | 新 Task 初始创建，以及原始创建结果丢失后的恢复 | 原 created 准入及精确身份/绑定/资源校验继续有效；恢复同一结果，不重复创建或借用活动续接掩盖不完整创建 |
| V7 | 本次受影响的 canonical/runtime/package、dogfood/installed、声明平台及 reapply/drift/sidecar | 定向验证通过，报告实际覆盖层；至少一个代表性 installed/native 独立 clone 场景由真实 owner 消费并执行写入，不以源码测试或文本检查代替 |
| V8 | F2：schema2 活动 Task 经正常绑定/rebind 后，从 Discovery 正式入口及其当前 spec 承接 | AI 可读合同与原 validator 一致使用 TaskId/generation、common-dir binding 和唯一 checkout；不索取或恢复 `task.json.branch`，不以文本零命中替代实际 owner 接续 |
| V9 | F3：当前 schema2 Task 的真实 Delivery/full Review candidate 进入 Delivery Review，含现有 readiness refresh 正常路径 | Interface 与当前原 owner 同义，不额外要求 `in_progress` 字段；当前 identity、candidate 和适用 gate 校验保持。旧诊断 helper 与 current invoke 的边界明确，不为测试回写旧 status |
| V10 | F4：正常旧 caller 输入触发 verifier 的迁移诊断；另以合法 current standalone 输入验证目标入口 | 文档、实际诊断及 consumer 一致；返回合法 standalone 准备或明确旧在途原 owner，不指向不存在的 current Finalizer。诊断/输入路由定向验证不要求本 Issue 执行完整 verifier 安装矩阵或实际发布 |
| V11 | F5：明确选择当前已处于 implementing 的同一 Delivery；另对声明支持的 checking/reviewing/publishing 续接入口及 output-loss recovery 做受影响定向覆盖，并保留 planning 的正常选择路径 | 原 selection/result 的真实 consumer 按公共阶段进入原 owner；保留 key、phase、原规划及仍适用结果，不无条件调用 initial Author。至少一个完整 caller → selection/result → 实际阶段 owner 的隔离样本由真实 owner 消费；不能只比较 exit 名称或静态 marker |
| V12 | F6：真实范围修订的 revised/no_change/withdrawal_required，沿 pre-Author scope_ready2.0 → scope-only Author → Clarify acceptance → post-Author scope_ready2.0 → 原阶段 owner；包含当前 Delivery 和无当前 Delivery 的适用分支 | 当前正文、profile/schema 与唯一 consumer 一致；pre-Author 不直接发布 scope、推进阶段或 stop，post-Author 不重复根需求写入。原阶段 owner 保留身份并执行实际合法 rework/withdrawal；不调用旧 clear/profile，不补造旧 DTO，不创建空 Delivery。至少一个隔离原生 owner 闭环覆盖实际消费，另报告三种 disposition 的受影响定向证据 |

正常 rebind、结果丢失和外部 ref 变化使用正式操作或受控正常样本验证，不通过故意伪造 artifact 构造必测场景。历史旧 `in_progress` 样本按现有正式迁移合同进入当前模型，或给出具体 pinned-old/deferred/manual disposition；不得要求当前 writer 直接接受旧模型，也不得把停止处置称为恢复通过。

验证止于本 Issue 的写入准入及受影响门禁，不要求完整业务 Delivery 发布或 Task 再次 Finish。安装验证最多一个代表性样本，不承担完整多平台 Release 矩阵。原有 Reroll 回归通过不证明新增留白行为或本流程缺口已修复。



无待用户决定的需求问题。Selection输出兼容方案由独立Architecture候选审查后在design第3节唯一处置；未执行的验证不宣称通过。

## 7. Canonical 引用与本轮差额

实际读取 docs/requirements/current/task-delivery-lifecycle.md 的身份/唯一Planning/跨环境接续，docs/design/current/task-delivery-lifecycle.md 的公共owner与恢复，docs/test/current/task-delivery-lifecycle.md 的T531/T635；本批补created适用范围、选择阶段路由、scope两段实际消费与V1–V12。
Architecture读取 docs/architecture/00-foundation/design-constitution.md、01-current/system.md、06-governance/change-contract.md；复用单写与public API，收敛命中的旧scope投影。RDT与Architecture原owner在final_integration晋升真实完整单元，当前PRD不直接改共享导航。
