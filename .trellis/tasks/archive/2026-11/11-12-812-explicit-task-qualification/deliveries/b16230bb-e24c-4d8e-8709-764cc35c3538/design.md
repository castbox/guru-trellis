# #812 D1：显式资格对象与原 caller 续接设计

## 1. 设计目标、需求承接与内容基线

承接本批 PRD 的 DREQ812-01～05、DS812-01～04、DAC812-01～04，以及根 PRD 全部 R812/AC812。目标是让合法 explicit-task 对象经过真实事实校验和资格语义后回到原 caller。开发基线 B 固定为 f16bb562e4ea844939786cebd5c6c20e686914b2，来源是原 Sync read 的 Git object；Planning H0 同此 OID，后续提交 H 单独取真实 HEAD；PR 目标 main 不是 B 的别名。

独立 Architecture 原公开 invoke 已返回 baseline_current / candidate_assessment：architecture_impact、target_native，authority 为 guru-trellis-architecture / guru-trellis-design-constitution-v1，decision_refs 为 ARCH-DOM-QUALIFIER-APPLICABILITY、ADR-CONDITIONAL-QUALIFICATION、ADR-008、ADR-020。该结论只准许当前候选展开，不能代替 Wording 后的 final_plan 或实现 Review。authority locator 分别为 docs/architecture/README.md、00-foundation/design-constitution.md、06-governance/change-contract.md。

## 2. 当前系统、边界与目标差额

qualification_facts.py 是三个 qualifier 的共享确定性事实入口。现有 Planning 校验在 schema2 Task 下无参数调用 DeliveryProjection.current()。adapter 已支持 current(key)：无 context 时经原当前 generation/C4/C5/registered checkout 和公开 Delivery/profile 检查；context 存在时读取官方当前选择。因此根因位于 caller→公开 target→共享事实的对象传递，不能通过修改官方 context resolver 解决。

本 D1 无前序。差额只落在七类 Task/Delivery 输入、共享事实、原 caller 说明与当前受控示例/eval/test，以及必要迁移和分发。四类 task_free_pre_write、task_free_evolution、requirements_scope_set、change_request_candidate_set 不拥有显式 Delivery，保持现行输入。phase2_candidate_set 保留其既有 pinned-old/recovery 使用边界，新输入不恢复退休 Check 阶段。

## 3. 来源设计处置（唯一）

已完整读取 #812、当前 qualifier-applicability 的 R/D/T 和 Architecture 单元，以及公共 Skill I/O 兼容合同。来源规定完整身份、原 owner、事实校验、原返回和迁移边界，但没有独立的已约定实现方案；本批不存在需要 retain/change/reject 的来源方案矩阵。本设计保留这些要求并在第4～7节具体落地。#793 的短条件和三 owner 分工不变；其“输入保持”只描述当时变更，本项通过 MIGRATION-812 明确新输入边界，不倒改历史证据。

## 4. 模块、职责与设计取舍

| 模块/owner | 本轮职责与差额 |
| --- | --- |
| 七类原 caller | 从自己的真实原 Identity/Ensure/Bind/Selection/current 事实取得完整 key，放入原 qualifier target；调用期间保留实际 Task/key/profile/purpose，消费原输出后返回自己的当前义务 |
| 三个 qualifier package | 新版 closed profile 和 aggregate 被 Interface、runtime PROFILE_SCHEMAS 与示例实际选择；AI 语义、短条件、结果枚举、出口和 consumer 保持 |
| 共享 qualification_facts.py | 对含 delivery_key 的当前 Task profile 共用一次对象解析逻辑；重读 Task/gen、C4/C5/registered checkout 与原 projection.current(key)，比较完整 key 与 current kind，再取真实 planning_directory；继续原 Git/path/Planning/author/candidate 检查 |
| DeliveryProjection 与原 lifecycle/session owner | 复用既有能力，保持其唯一 authority；不增 writer、选择存储、fallback 或私有身份协议 |
| 原 tools owner | 同步 canonical 到此 checkout 的受管 runtime、Skill、workflow/spec/平台投影；保 Task、session、peer 与配置 |
| 原 RDT/Architecture owner | 按第9节的完整隔离拟写在 precommit final_integration 整合/readback；提交后独立 Review 判断实际 after |

选择显式参数加原 model 校验。直接改 current() 从 inventory 推断对象会引入隐式选择；新 session writer 会产生第二 authority；跳过 Planning 会取消有效一致性检查；复制 resolver 会产生三套易漂移事实入口。因此不采用这些方案。七个新版输入及一个共享解析职责有当前直接 consumer；不增加未来预留字段。

## 5. 接口与数据

三个 package 各自为七类 profile 新建 public-<profile-token>-input-2.0.schema.json，保留原 path/id/bytes；其 target 新增必填 delivery_key，类型保持上游 opaque object，由既有 API parser/adapter 校验完整 TaskId/generation/delivery_id 和关系，不在 Guru 重写 UUID/Task schema。新 aggregate 为 public-input-3.0.schema.json，id 由各包现有前缀加 aggregate-3.0；引用新七类与原四类 profile。旧 aggregate 1.0/2.0 继续原字节历史验证，Interface 只选新 3.0。

| profile | 固定 caller | 新输入事实与后续 |
| --- | --- | --- |
| author_candidate_set | guru-author-task-plan | 原 author_paths/identity 加完整 key；只要求当前存在的来源/候选文件，不要求未来 design/implement |
| planning_scenario_set | guru-approve-task-plan | 完整 key；planning_paths 与该 key 的真实 planning_root 三文件集合一致，identity 保原 raw-byte file-set 格式 |
| implementation_discovery | guru-phase2-implementation-coordinator | 完整 key，真实 checkout_head、Planning identity、diff_locator；返回原实施 caller |
| base_impact_candidate_set | guru-reconcile-task-base | 完整 key 与原固定 old/new base/task facts，保原 Reconcile 触发和返回 |
| phase2_candidate_set | guru-check-task | 完整 key 与原 facts；仅既有合法旧操作/恢复边界，不引入当前独立 Check 流程 |
| branch_review_candidate_set | guru-review-branch | 完整 key 与原固定 B/H/range facts；不缩小完整 committed review |
| publication_candidate_set | guru-review-task-delivery | 完整 key 与原 reviewed commit/payload facts；不改变 readiness 或 PR payload authority |

所有 profile 继续一套 candidate_refs/locators。author 身份仍只绑定已选 author_paths；Planning 身份从真实规划目录构造，显式 planning_paths 不得指向另一切片。完整 key 校验不替代当前 HEAD、路径、file-set 或候选检查。输出 DTO、唯一 consumer 和跨 owner 的最小投影不新增字段；同一 caller 在内存持有自己的输入对象，不靠资格状态文件续接。

## 6. 状态、顺序、正常与失败流程

1. 原 caller 按现行短条件判断适用性，复用仍适用结论；需新调用时，从原身份/选择 owner 取得当前完整 key，构造新版 public input。
2. qualifier 验证 closed schema；共享事实先核 TaskRef/key/当前 generation 与 branch/checkout，再查询原 current(key)。无 context 不写 session；有 context 必须是同一 current key，no_current/terminal/error/不同选择保留原诊断和恢复 owner，不能静默选中。
3. 从真实 key 解析 planning_root。需要 Planning identity 时读取该目录三文件；若 supplied planning_paths 与真实三文件集合不一致，拒绝并指明输入字段。author_candidate_set 校自己的实际 author_paths，不强求三文件已完成。
4. 继续既有 Git、locators、file-set 和候选检查。AI 读当前要求/机制/因果并选择原结果；原 recorder/checker/invoke 校验事实和投影。
5. 原 classified 或非通过 consumer 回到实际 caller/profile。诊断或修订只阻塞依赖该候选的工作，不换 Task/Delivery，不伪造完成。

普通 stale/mismatch 返回原 CommandError/LifecycleContractError 的字段和 remediation。不存在新 phase、状态存储、重试策略或事务协议。当前输入不支持的旧形状在 schema 阶段拒绝，回原 caller 重装；不得为缺失 key 猜补字段，也不得从 task.json 唯一 Delivery 推断。

## 7. 恢复、兼容、迁移与集成

采用直接演进与受控 consumer 同步，不新增 runtime 双读、旧 parser、适配 wrapper 或存储。MIGRATION-812 明确固定前驱 f16bb562e4ea844939786cebd5c6c20e686914b2：已执行完的旧资格结论在原适用条件内采用；历史不转当前 pass。尚未调用的旧输入回原 caller，从其真实 current/explicit identity 重装新输入；缺 key 或身份冲突由原 owner 处理。旧 provider 的未完成操作在完整固定旧 provider 下恢复，不将旧 public bytes 输给新 runtime，也不重复已发生副作用。

七类旧 profile/aggregate schema 是原发布验证资产，保原字节而无 current runtime consumer。新 Interface、schema inventory、runtime selectors、公开示例、受控 eval/fixture 和实际 caller 说明同批切换。保留历史归档、旧 evidence 和已完成 Delivery；没有 Task 数据格式迁移。

经 guru-upgrade-tools 的完整 canonical source 执行 preview→prepare→原语义 Gate→精确更新/原操作恢复，不用普通 apply 的旧 Task 阻塞作为迁移其他任务的理由，不手抄 managed 文件。此 checkout 只更新实际受管工具/投影，保配置、Task/gen/key/root/session、peer 和 common runtime pointer。产生 sidecar 按原 owner 逐项处理，未解决不得声称 installed 可用。local_candidate 的 formal_fork_source_lock 未验证边界单列，不声称发布矩阵通过。

## 8. 验证设计

| 验证 | 层与实际入口 | 输入、独立断言和范围 |
| --- | --- | --- |
| V812-01 公共合同 | 三包 contract/runtime 定向测试与 source package checker | 新版七类 profile 带实际完整 key；旧 schema 独立验证且 cross-version substitution 拒绝。四类非 Delivery 合同不变，输出投影仍进入原 consumer |
| V812-02 共享身份与 mismatch | 新定向集成测试，经原 public Creation/Identity/Ensure/Bind/Delivery 前提与三个 qualifier wrapper | 无 context 真实对象成功；key/gen、registered checkout、Planning/candidate 普通变化导致错误的独立断言失败。事实测试不假称 AI 语义通过；fixture 不补被测入口应产生的结果 |
| V812-03 原 caller 实际观察 | 根实施 caller 的真实 explicit_task_mode，以及正常子 Agent 的官方 context | 同一条件的候选经原适用 profile/公开 wrapper，观察 normal/solution/root 的实际输出和原 caller 后续动作；观察 classified 和原合同定义的非通过返回；具体采用第4节已拒绝的“跳过 Planning”替代，由真实 Author/root 消费机制修订出口并移除该替代，其余未变路由采用现有覆盖。context 由平台实际提供，经原 Bind/Selection，不给测试手工设置环境键。必要 context mismatch 由原选择/生命周期正常变化形成 |
| V812-04 安装采用 | 原 tools owner、source/installed package checker、overlay drift 和目标自身原入口 | canonical/受管 runtime/Skill/声明平台一致，Task/session/peer 保持；必要 reapply/sidecar 定向验证。安装一致不证明 V812-03 |
| V812-05 完整候选质量与终态 | 工程自检/Docs 整合→本地 TaskCommit→独立固定 B..H Check/full Review→readiness/交付→Completion/Closure/Finish | 检查完整受影响内容及必要 unchanged consumer；PR 为 Refs-only，merge 前暂停，由协调方处置；真实 main 可达终态才满足整体完成 |

V812-01 采用仍适用的语义枚举/聚合/consumer 测试；需更新旧 fixture 时明确其单元边界，不以私有调用证明公开事实链。V812-02 补原缺陷到达及身份一致性缺口；V812-03 分别证明真实执行与原 caller 消费，后测前不宣称根因修复。必要观察充分后停止重复实验；设施未触达目标先重评方法并保留证据缺口，不把设施失败称产品通过/失败。不跑完整多平台安装/升级或 Release 矩阵。

## 9. Canonical 引用、本轮差额与实际未决项

R/D/T 以 docs/{requirements,design,test}/current/qualifier-applicability.md 的现有完整单元整合本次显式身份行为，保 REQ/DES/TST-793 的条件调用和历史截止。Architecture 命中 docs/architecture/03-domains/qualifier-applicability.md，保原三 owner、无状态和唯一出口关系；原参考的 fixed-order/历史语义不恢复。

当前 Author 准备真实隔离 contribution：docs/architecture/contributions/812-explicit-task-qualification/contribution.md，完整 proposed 同镜像 qualifier-applicability.md 和 adr/explicit-task-qualification.md；ADR identity 为 ADR-EXPLICIT-TASK-QUALIFICATION。原 Architecture owner 于 final_integration 重读并写 shared targets/readback；不修改共享 root/system/ownership 或 ADR index 登记。RDT 的隔离完整拟写及晋升由原 RDT owner 按 implement 的唯一 Docs Plan 执行。

当前没有需求或技术方案未决选择。工具更新的精确冻结写集与真实入口运行观察仍是后续执行义务，不以本规划通过替代。
