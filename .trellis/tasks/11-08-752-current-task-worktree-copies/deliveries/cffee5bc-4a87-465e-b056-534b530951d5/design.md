# #752 D1 current-schema Task 副本迁移设计

## 1. 设计目标、需求承接与内容基线

本批覆盖 PRD D1-R1–R5 / D1-AC1–AC5；根 Task 保留全部完成责任。固定 development B 为 2ab135ed2d3908966785bb23ad42ada0790f0c81，来自用户选择 main 后实际 Sync baseline_ready。Planning H0 同 B，PR 目标为 main；内容范围是 B..实际 H 加本批 dirty，目标分支后续前进不改变 B。

真实独立 Architecture candidate_assessment 已返回 baseline_current / architecture_impact / target_native，freshness sha256:906a81de42280729867f019b52f92e1a384769abde49984d747183a12eb52610；authority 为 guru-trellis-architecture，constitution 为 guru-trellis-design-constitution-v1，change contract 为 guru-trellis-architecture-change-contract-v1。引用 ADR-024 与 ADR-017，不新增决定或第二 authority。

## 2. 当前系统、边界与目标差额

没有前序 Delivery。现有 Guru prepare_inventory 返回全部 roots、原 Task raw snapshot 和 branch_bindings。preview 调上游 migrate2，private migration 已只允许 selected workspace 的 current/convert_active/convert_archive。其 frozen-source、preimage、resume、rollback 和实际 target installed validation 保留。

当前 source lock 为 Fork ca0e8b9/.6。已存在上游 PR66，候选 501e7137e6d19c1eaa5793fa8887cb5702d228d6，base d9ffdf526988cad7b34da38d280fcbf893e77305；其五项 CI 已通过，但 Open PR 不等于正式采用。采用前需独立核准确源码差额、实际构建与 main 合并/CI 身份，再固定 source lock 的 commit、parents、tree、ci_run_id。CLI/Core 继续同源构建，不用已安装补丁或同版本号替代内容身份。

目标差额是 current peer 的上游语义、Guru 原 consumer 合同说明/回归和 source-locked 实际多 workspace 安装。当前实现若已能薄透传新 schema，复用它，不为制造代码差额新增分支。

## 3. 来源设计处置（唯一）

| 来源/承诺 | 处置与落点 | 理由、影响与上游处置 |
| --- | --- | --- |
| Issue #752：完整 registered inventory、原 binding/live checkout 唯一 authority | retain，第4–6节 | 不过滤 peer；由 Fork executor 验证 |
| Issue #752：合法 peer 保留，禁止额外生命周期/selection/Delivery/private authority | retain，第4–8节 | 原 current 与 defer 分工，不新增 Guru copy 模型 |
| Issue #752：内容/generation/source/binding/checkout mismatch 阻塞 | retain，第5、6、8节 | ordinary correctness，禁止静默合并 |
| Issue #752：dry-run/migrate/resume/rollback 与匹配 source pair installed 验证 | retain，第7、8节 | 源码、集成、实际安装分别证明 |
| 原 delivery-migration 合同：公共 Plan2 独占 group；原私有 owner 和 frozen backup/recovery | retain，第4、6、7节 | 将 current schema2 peer 加入原有合同，不扩大 private conversion |
| 上游 PR66：mixed + defer/source_task_schema2，public parser 和完整 parsed equality | retain，第5节作为配套实现合同 | 复用已存在候选；只有核准合并及匹配源码后采用，不 patch tag/npm |

## 4. 模块、职责与设计取舍

Fork CLI migration2-schema.ts 接受 mixed plan 的 defer row source_task_schema=2.0，禁止该 selector 用于转换或 current/history。migration2.ts 用 public parseTaskRecordV2 读取冻结 peer source，要求它与唯一 projected authority 的完整 parsed record 相等；原 group、branch snapshot 和实际 checkout 验证保持。peer 仅 prepare preserve，bytes/modes 不重写，不生成 migration/Delivery assets。

Guru 原 delivery_upgrade.py / delivery_upstream.py 透传完整 Plan2、原 binding、selected workspace 和 installed package roots。保留 private projected-list 边界，新增真实回归证明 peer 不能进入 owner_migrations。files.py 和原 rollback consumer 保存 peer preimages，不新增状态或 copy ledger。

canonical source lock、相关当前 source 说明和原受管投影采用已核 Fork successor。原 guru-upgrade-tools 维护 dogfood 工具/Skill/spec 副本且保留 Task/session；代表性 full Plan2 迁移继续归 guru-upgrade-installation。普通 apply 的历史 Task 阻塞不作为绕过理由。

方案比较：过滤 roots 或把 peer 当 legacy 会损失合法输入/语义，拒绝；在 Guru 复制 group/equality 会形成第二模型，拒绝；复用上游既有 defer 新 selector 能维持原 executor、session 和恢复路径，选择该方案。

## 5. 接口与数据

| 生产者 → 消费者 | 本批字段/约束与结果 |
| --- | --- |
| 原 Upgrade owner → Fork migrate2 | schema_version=2.0；source.task_schema=mixed；authority disposition=current、不带 source_task_schema；peer disposition=defer、source_task_schema=2.0、原 source RawSnapshot，不带 target record |
| prepare_inventory → 原 owner → migrate2 | 全部 registered roots、原 task/artifact/session snapshots 和 branch_bindings；不新增 target binding/path/action |
| Fork parser/group → executor/session projection | complete parsed Task 等价、同 ID/generation/source、唯一 authority 和唯一 live bound checkout；普通 mismatch 拒绝且零写入 |
| Guru private migration → 原 TaskCommit/Publish/Merge | 只允许 selected workspace 中 projected Task；defer peer 一律不进入，即使同 TaskId |
| source lock → 原 build/installer/validators | 精确 commit/parents/tree/main CI 与同源 CLI/Core；相同版本号本身不足 |

Plan schema 2.0、Task schema 2.0、Delivery API1.0 和公共 Guru DTO 不变。peer raw JSON 的合法格式/key顺序差异不影响 parsed equality，保留其原字节和 modes。业务字段或 lifecycle 内容差异不能被格式规范化掩盖。

## 6. 状态、顺序、正常与失败流程

1. 读取全部原 roots、Task/session/binding 和 source pair；原语义 owner 选择唯一 authority 与 peer dispositions。
2. 冻结同一 Plan2、source/fork candidates、原 owner inputs 及 write set；dry-run 验证 schema、完整 inventory、parsed equality、binding/live checkout、private exclusion 和 conflicts。
3. 任何内容、generation、source、binding、checkout 或唯一性不符，保持原数据并回原 prepare；不得刷新旧计划使其通过。
4. 原 Upgrade begin 冻结所有 upstream、Guru、private paths 和 raw preimages，随后依次 Core、原 private owners、旧 Guru retirement、完整 preset、实际 installed validation。
5. peer 仅 preserve，不被私有转换或 session 投影选作额外 authority。public query 验证的是原 binding 指定 Task 的实际 checkout。
6. 普通暂停返回同 recovery_ref；已完成阶段不重复执行。new business/topology drift 阻塞恢复或回滚，保持新工作。

不新增 Task/Delivery 阶段或业务状态机。保留脚本事实与 AI gate 判断分离。

## 7. 恢复、兼容、迁移与集成

旧闭合 schema executor 不理解 selector2。新计划必须由完整匹配 successor CLI/Core 消费；旧冻结计划/checkpoint 留在原 package pair 下同计划恢复，不换包续跑或扩大 anchors。不发布同版本 npm replacement，不修改不可变 tag。

回滚由原 Upgrade owner 审查并执行，检查当前 managed/business/topology 前后状态后恢复原 raw Task/session/Guru 文件与 modes，删除本次新增路径；不 reset Git 或重写远端。实际安装样本必须覆盖 current peers 的 dry-run、正常迁移、同计划重复/暂停恢复及 rollback。

source_locked 模式需要干净已提交 Guru source、精确 Fork build 与 lock 匹配。实施期 local_candidate 测试明确保留 formal_fork_source_lock 未验证边界；正式提交后用同内容的干净 source 进行匹配 source_locked 代表性多 workspace 验证，必要证据修订仍回原 Check/Review，不以 fixture 通过提前 Completion。

## 8. 验证设计

| ID | 要求与层次 | 入口、输入、独立断言及限制 |
| --- | --- | --- |
| V1 | R1/R2/R3，Fork public schema/executor 集成 | 采用 PR66 的 migrate2 integration：真实 worktrees、current/defer2、原 binding；断言唯一authority、peer raw/modes、无peer migration/Delivery、schema/mismatch/authority失败零写入；CI/源码结果不代替Guru实际安装 |
| V2 | R1–R4，Guru 原 Upgrade + 实际 Core/CLI 集成 | 扩展现有 test_delivery_upgrade.py 真实多 workspace fixture 为current authority/peer；preview零写入、session不变、private peer拒绝、原 resume/rollback保留；只替换preset/installer的既有组件测试仍标组件边界 |
| V3 | R4/R5，完整代表性安装 | 匹配完整source pair，经原delivery_upgrade公开preview/invoke与实际preset在至少两个registered roots升级；读取target own runtime及publicTask/session query，核peer bytes/modes/metadata、authority checkout、无peerDelivery/private转换，执行同plan恢复和rollback；不能用mock installed validation证明 |
| V4 | R5，来源/投影与回归 | 原source lock验证和真实Fork clean build、source/installed package validators、ownership、dogfood drift、递归sidecar/mode；改动命中的原Upgrade/package tests与Python语法、diff检查 |
| V5 | 全部，完整独立质量链 | 完整隔离RDT/Architecture proposed先经独立phase2与candidate Check，原owners晋升，actual after重绑最终Check、TaskCommit、完整固定B..H BranchReview和readiness |

长期回归覆盖 distinct 行为；临时安装验证只回答本批配对采用问题，执行事实写唯一 Test。现有 legacy/mixed group 与原恢复测试在输入/依赖仍适用时采用，补 current peer 的实际缺口；不复制实现计算期望，不增加无证据的压力/故障矩阵。证据足够后停止追加同质实验。真实业务仓、远端marketplace/tag及完整多平台Release矩阵不由本批样本证明。

## 9. Canonical 引用、本轮差额与实际未决项

PRD第7节的RDT native-compatibility单元保留source/build/installed分层和原owner。RDT原owner在隔离 contribution 中维护 current-copy完整能力与必要source引用，实际 Test单写执行观察；候选Check后由原 final_integration写current完整单元。

真实 Architecture contribution 为 docs/architecture/contributions/752-current-task-worktree-copies.md，同名目录 proposed 保存 distribution.md / ARCH-INT-046 和 ownership.md / ARCH-DOM-043 的完整拟写。保留#531历史观察和原ADR-024/017，不新增空ADR、不写根入口或全局版本。

没有待解需求问题。当前外部依赖是 PR66核准合并和成功main CI/source lock；未就绪只阻塞正式source_locked采用，先继续不依赖该结果的本批代码/测试工作，不以Open PR声称采用。
