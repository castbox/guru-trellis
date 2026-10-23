# D1：活动任务续接与迁移残余合同收敛设计

## 1. 设计目标、需求承接与内容基线

本批承担 PRD 的全部 R1–R7、F1–F6 和 V1–V12。首次 D1 无前序 Delivery。目标是使既有 Task 的合法写入、Delivery 选择及范围修订消费同一 current 合同，保留初始创建精确恢复和全部仍适用门禁。

开发基线与固定内容基线 B 均为 `319202beab79c7666ecdb855291bf117e43d407e`。原 `DeliveryProjection.content_base` 在没有既有 candidate／前序 delivered head 时，以明确 development_base 投影得到此 B。Planning H0 同为该提交，只是写作起点；最终内容范围为 B..实际 H 加真实 dirty 增量。PR 目标为 main，目标前进不改变 B，也不自行触发 Reconcile。

已消费原 Architecture 的实际 candidate_assessment：`baseline_current`、`architecture_impact`、`change_path=target_native`，baseline 为 `guru-trellis-architecture`，constitution 为 current `guru-trellis-design-constitution-v1`，decision_refs 为 ADR-011/023/024 及 change-contract。该结果只允许本候选的 solution writing，不是 final_plan、Approval、晋升或实施通过。

## 2. 当前系统、边界与目标差额

公共 Task schema2、Delivery API1 和 planning_root 由真实 installed Trellis 拥有。Guru 的 Identity、Establish/rebind、Ensure 和 Bind 已支持当前 common-dir 内的身份与 checkout。独立 clone 不拥有原机绑定或私有恢复状态，但已提交且可获取的 Task/Delivery 是合法续接来源。

六类差额是：F1 全局写入仍普遍要求初始 created；F2 Discovery 的 spec/Skill 保留 metadata branch 和旧 Task development status；F3 Delivery Review Interface 要求 in_progress；F4 verifier 迁移指向退役 Finalizer；F5 Selection 与 Creation 共用 created，consumer 却无条件进 initial Author；F6 scope 修订仍混入旧 clear、scope_ready1.0 和 active_task_scope_change。

本批修改原 Markdown owner 合同和相应投影、必要 consumer 声明及定向测试。保留公共状态模型、TaskId/generation、source、DeliveryKey、规划历史、初始 Creation validator、已发生 Git/PR 事实及原语义门禁。没有业务代码、业务数据、发布或完整 Release 矩阵变更。#649 阶段成果及完成证据语义保持独立。

## 3. 来源设计处置（唯一）

| 来源／承诺 | 处置与具体落点 | 理由、影响与上游承接 |
| --- | --- | --- |
| #657 R1、R2：created 只服务初始创建；合法续接保留身份且实际写入 | retain；第4、6、7节 | 原身份与 checkout owner 已足够，不能放宽 recover_created_control_state 或复制原机 runtime |
| #657 R3：整体 scope 与 Delivery 规划分工、逐批边界、只刷新实际影响 | retain；第4、6节 | Clarify/Author/当前阶段各自保持单写；phase 不证明 gate |
| #657 R4：canonical 与 installed/platform 一致 | retain；第7、8节及 implement Docs Plan | 通过完整匹配 preset/overlay 分发，不直接补丁业务安装 |
| #657 R5、F2–F4：退役身份/status/owner 不再作为 current 前置 | retain；第4、5节 | 修订原可读合同；历史 pinned-old 不删除、不自动转 pass |
| #657 R6、F5：选择或恢复已有 Delivery 按真实阶段进入原 owner | retain；第5、6节 | 保留 created wire，consumer fresh query；没有新 DTO、phase cache 或状态机 |
| #657 R7、F6：pre-Author 与 post-acceptance scope_ready2.0 分开 | retain；第5、6节 | 只有原 Clarify acceptance 调用 accept_scope，不能仅重命名 clear 跳过发布 |
| ADR-011：workflow continuation 独占跨阶段恢复，原 producer 恢复副作用 | retain；第4、7节 | 窄替代其 Task development status、旧 activation/checkpoint/Finalizer 路由片段，原恢复职责保留 |
| ADR-023：Clarify 先判断、Author 唯一写作 | retain；第6节 | 窄替代 private4/scope_ready1、旧 Author profile 和 in_progress resume；按 ADR-024 当前两段 scope 发布 |
| ADR-024：官方公共模型、Guru 语义 owner、完整 matching 切换 | retain；第4–7节 | 补全 created consumer 与 scope 当前语义；不改变官方 API、阶段 ownership 或终态责任 |
| current change-contract：purpose、九 concerns、贡献/ADR和原晋升 owner | retain；第9节与隔离贡献 | 更新其中仍称 current 的旧 scope 段属于本批必要差额；Author 只写真实候选，不直接晋升 |

该矩阵不接受额外 scope。发现同族遗漏时先核 current caller/consumer 和正常触发，再由原 owner 判断必要性。

## 4. 模块、职责与设计取舍

| 模块／原 owner | 本批责任与边界 |
| --- | --- |
| canonical workflow、continuation、Workspace boundary | 划分 initial Creation 与 existing active continuation；统一 created consumer 和 scope 两段 consumer。global 只编排，内部判断仍归原 Skill |
| guru-create-task、shared task_lifecycle composition | 保留创建结果的初始 generation/binding/ledger 校验和正式恢复，不用它校验既有任务续接 |
| Identity/Establish/rebind/Ensure/Bind | 从明确 source ref 和公共身份解析同 Task；只建立当前 common-dir 的合法关系，不重建历史资源资格 |
| guru-create-delivery 和现有 created consumer | Creation/Selection 原 stdout 保持；consumer 读取当前公共 selection/Delivery phase 后接原 continuation；不把 created 名称当作 phase |
| Discovery、Delivery Review、standalone verifier | 分别修正当前身份文字、Interface status 前置和旧输入诊断。当前 validator 的真实严格约束保留 |
| Clarify、scope-only Author、当前 Delivery stage owner | 依次拥有范围判断、根 PRD、accept_scope、合法 rework/stop；不跨 owner 写 stage 或恢复私有证据 |
| 原 RDT／Architecture owner | 独立评估完整拟晋升差额，candidate Check 后在 final_integration 写共享 current；Author 只写 contribution/ADR 候选 |

采用现有 public query 与 workflow continuation，理由是同一事实和原 owner 已存在。新增通用 router Skill、phase 字段、状态缓存或双读兼容层会重复 authority。脚本只读事实及校验 shape，不能替 AI 决定语义 route、scope 或门禁充分性。

## 5. 接口与数据

`guru-create-task:created` 及初始恢复的输入、schema、exit 保持。既有 Task 写入准入使用 TaskId/generation、合法 current binding、唯一注册 checkout 和原阶段适用前置；原 created DTO 缺失本身不是拒绝理由。

`guru-create-delivery:created` 保留 `exit_id/delivery_key/task_ref/planning_root`。原 workflow consumer 收到后，使用 installed 公共 API 对同 key 查询 current selection 和真实 phase，校验 generation、scope、root 与实际对象相符。该结果是对象选择事实，没有 Approval 或新建保证。仅 planning 且满足 Author 当前 profile 前置时投影 delivery_initial_review；其它活跃 phase 进入原 continuation 表。delivered/stopped 或真实 stale/mismatch 交原 owner 精确停止/处置，不回初始规划。

这是已发布 created 输出对现有选择语义的 consumer 修正，不改变 wire 或新增出口。实施须在原 consumer/interface说明及 migration 文档明确旧 consumer 的无条件 Author 处理被完整 matching 版本替代；旧在途恢复先归原 producer，不静默混用新旧 reader。

scope_ready2.0 两种闭合 shape 保持：pre-Author 无 task_key，携 source_selection/revision_refs/scope_action 交 Author task_scope_requirements；scope_requirements_ready 的真实 requirements_locator 与原 selection 交 Clarify acceptance。只有 acceptance 核验实际 root PRD AuthorityRef 并执行 accept_scope，输出含真实 task_key 的 post-Author scope_ready。后者按当前义务进入原 stage 或显式 Creation/Completion。没有新 schema、授权字段、digest 链或持久化 stage token。

## 6. 状态、顺序、正常与失败流程

既有 Task：明确 source ref/commit → Identity → 当前 common-dir 的 Establish 或正式 rebind → Ensure → Bind／explicit-task → 公共 current query → 原 phase owner → 逐批 boundary → 合法写入。ref/必要代码不可获取、身份歧义、generation/binding/checkout 错配在写入前停止，不创建替代 Task 或空 Delivery。

Delivery selection 或 Creation output-loss：原 producer 恢复同 key/真实结果 → 原 created consumer fresh query。planning 按适用 Author 入口继续；implementing 进入实施；checking 由原 Architecture phase2/Check 消费实际 candidate；reviewing 先恢复 Check/TaskCommit binding 再完整 Review/readiness；publishing 交原 readiness/Publish/Merge 及原事务。所有分支都重新判断所需结果的适用性，不能从 phase 补造 pass。若 source selection 丢失，回原 Clarify；source 实际变化走下面范围链。

范围链：原 Clarify 判断 revised/no_change/withdrawal_required → pre-Author scope_ready → scope-only Author 写真实整体 PRD → Clarify acceptance 审查并 accept_scope → post-Author scope_ready → 当前 stage owner。revised 由最早受影响阶段合法 rework 后交同 Delivery Author 更新受影响规划；no_change 保留仍适用工程结果；withdrawal_required 仅由当前 stage owner stop/release并保留 PR/历史。无 current Delivery 时根据真实义务显式 Creation 或 Completion，不为撤回造空切片。post-Author 不重复写根 PRD。

新 Task/创建结果丢失继续走原精确 Creation 区间。binding revision 大于零的续接不调用初始恢复，不重置 ledger/binding。普通失效和输出丢失经原 producer、最早受影响语义 owner 自动重入；真实范围/authority变化按原门禁处理。

## 7. 恢复、兼容、迁移与集成

完整 matching workflow/preset/packages/consumers 是唯一切换单位。新增迁移说明定位 F1–F6 当前替代、created wire不变、原 producer 恢复和仍适用 gates；不修改 frozen 历史 schema 的字节来声称兼容。旧完整安装由原升级 owner显式切换，旧在途 Finalizer 保持 pinned-old 或已有 per-case disposition；standalone verifier 的旧输入诊断指向合法 standalone 准备或明确旧在途原 owner。

canonical workflow、package、managed spec 先修改，再通过原 apply/reapply 同步 dogfood 与声明平台。用户本地修改由原 .new/.bak/hash 机制保护，sidecar须逐项处置。没有数据迁移、新持久化或远端副作用，不设计额外回滚协议；普通源码回退只涉及本批文件，并保留并行改动。

Architecture 窄ADR只替代 ADR-011/023/024 中本批命中的旧恢复/route语义，保留唯一 continuation、scope单写、公共模型、终态及真实历史。RDT/Architecture 原 owner完成最终整合后，implementation重新绑定全部实际写入，再 final Check/commit/独立完整 Review。

## 8. 验证设计

| 验证ID／需求 | 层、入口与输入 | 必须观察与限制 |
| --- | --- | --- |
| V1、V2、V7／R1、R2、R4 | 最多一个 matching installed/native 独立 clone B；A提供已提交可获取Task/Delivery，B没有A私有runtime/created；实际Identity/Establish/rebind/Ensure/Bind与owner写入 | 同Task/generation/source/Delivery、revision>0及原owner一次真实合法写入；不是仅DTO或fixture成功 |
| V3、V12／R3、R7 | 原生scope owner闭环与定向fixtures；有/无current Delivery，三种scope_action | 实际pre/post两段消费及accept_scope顺序；受影响规划更新或原stage stop/release；无旧clear/profile及空切片 |
| V4、V5／R1–R3 | 原生命周期测试，正常同阶段续接、stale/mismatch、ref不可取或checkout错配 | 无created仍可正确续接；错误写前停且不覆盖无关环境；不故意篡改artifact造场景 |
| V6／R1 | 原Creation/composition定向suite，新建及同操作输出丢失恢复 | 初始精确校验、同结果恢复和零重复创建保持；不放宽validator |
| V8／F2 | 原Discovery正式入口、现有active identity fixture及native上下文 | TaskId/generation/binding/checkout一致，不索取旧branch/status；文本零命中不是实际接续 |
| V9／F3 | 原Delivery Review真实candidate，含readiness refresh定向suite | current identity/gate严格，Interface不增加旧in_progress |
| V10／F4 | verifier实际旧输入诊断与合法standalone输入校验 | 无current Finalizer误导，合法下一入口一致；无需跑完整verifier安装矩阵 |
| V11／R6 | 原Creation/Selection调用、真实consumer和原stage owner；planning及四个已前进phase/输出丢失定向覆盖 | key/phase/root/gates保持，至少一个完整隔离owner消费；不只比较exit标记 |
| V7／R4、R5 | source/installed、完整apply/reapply、drift、ownership、平台/mode/sidecar及diff检查 | 分发真实一致，零未处理sidecar；不宣称全平台native、现场采用或Release通过 |

规划时上述均未执行通过。具体命令、native工具链与实际证据层由implement第3节及后续唯一Test记录；缺实际Agent层不能以绿色fixture补足。

## 9. Canonical 引用、本轮差额与实际未决项

RDT命中 `docs/requirements/current/task-delivery-lifecycle.md` 的身份/唯一Planning/范围修订，`docs/design/current/task-delivery-lifecycle.md` 的owner与恢复，`docs/test/current/task-delivery-lifecycle.md` 的T531/T635。差额为R1–R7和V1–V12，原RDT owner维护隔离完整requirement/design/test/traceability贡献。

Architecture命中constitution五原则、`01-current/system.md`、`03-domains/ownership.md`、`04-integrations/distribution.md`、`06-governance/change-contract.md`及ADR-011/023/024。真实候选位于 `docs/architecture/contributions/657-workflow-continuation-conflicts.md` 与 `657-workflow-continuation-routing-adr.md`。九concern、无新增GAP、target_native和窄替代边界见该贡献。它们不是shared current，不在Planning直接promotion；原owner在完整候选Check后final_integration。

无待用户决定的要求问题。native入口和受影响测试选取属于实施细化；若实际工具链或来源不可用，停止对应证据层并报告具体依赖，不能删减V1–V12或预填pass。
