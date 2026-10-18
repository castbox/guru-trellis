# #548：显式 Task 的 D1 创建与原对象恢复

状态：`reviewed_promoted`；identity：`architecture-contribution-548-creation-recovery-v1`；path：`target_native`。按 expected `current-main-0.6.17-guru.88` 晋升至 `.89`，继承 constitution v1、project change contract v1、ADR-024，无新 ADR/GAP。首次独立完整实现审查范围为 `origin/main@901d4f5d3b153725b7bf928427dc8663f4c0a5f2...25ae20319fae2047747da70e3be5167bb39d9a27`；晋升新差异重新进入原 gates。

这是当前已晋升贡献。原 task-owned 规划贡献属于历史候选，[不可变原稿](https://github.com/castbox/guru-trellis/blob/25ae20319fae2047747da70e3be5167bb39d9a27/.trellis/tasks/10-14-548-creation-recovery/architecture-contribution.md)保留 planning preimage，不作为第二 current authority，也不依赖 Finish 后的 active Task 路径。

Before：C6 支持 explicit-task 无 context 创建；C7 保留 D1 后仍要求 session，后续 Planning consumers 同样要求 session。After：原 DeliveryProjection 仅在官方 resolver 无 context key、caller 已提供明确 DeliveryKey 时读取原 C4 与官方 parser/profile/applicability，投影 call-local current/terminal；无 key 查询不推断身份。存在 context 时完全保留官方 current/select；Creation 创建及自动恢复不覆盖另一合法 current，而明确 select 仍允许官方切换。

原 Creation owner 保留同 operation/UUID 恢复输入，原 Author 成功消费后只调用 producer retirement 端口。Producer 自核同 Task/gen/scope/profile/phase 并退休自己的匹配输入；原 Wording、Architecture、Approval、Activation 仍各自拥有 gate。Qualification 沿原 planning_paths，没有第二 selection store、writer、公共 DTO、exit 或通用恢复状态机。

| Concern | Applicability / 晋升依据 |
| --- | --- |
| authority-binding | applicable：expected .88、active successor .89、原 public model 与当前 generation |
| constitution-binding | applicable：薄显式读取与原 owner 退休满足最小必要复杂度；无原则例外 |
| boundary-and-decision | applicable：context 存在性由官方 resolver，明确 key 只作调用参数；ADR-024 适用 |
| owner-and-single-writer | applicable：官方 Task/Delivery/session authority；Creation 单写其 pending，Author 只调用生产者端口 |
| compatibility-and-exit | applicable：公共 I/O 不变、无 legacy reader；旧完整安装由原迁移 owner 成套切换 |
| gap-and-deviation | applicable：修正正常 D1 自阻塞，无既有 GAP 生命周期变化 |
| parallel-scope | applicable：只本任务与受控样本；不触业务仓或其它任务资源 |
| evidence-and-freshness | applicable：原失败 D1 与 operation 恢复；[唯一 Test](../../requirements-design-test-contributions/548-creation-recovery/test.md)拥有层级及边界 |
| review-and-promotion | applicable：首次完整 committed 独立 Review 后晋升；新增文档差额再走 Phase2/commit/完整 Review |

详细行为仍由 canonical Creation、Author 与原消费者的 step-local 合同独占；本贡献仅拥有 before/after、归属与晋升依据。固定软件四轴、Release 状态、旧主完整安装、原 CMS/业务恢复、native 自动注入及完整矩阵均不由此次知识晋升证明。
