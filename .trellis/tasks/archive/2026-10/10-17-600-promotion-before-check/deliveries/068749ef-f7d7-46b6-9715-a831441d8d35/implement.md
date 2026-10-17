# #600 D1 实施计划

## Delivery Policy

policy=full。D1 覆盖整体 AC1..AC8；remaining_work=[]。独立可交付条件为匹配的 canonical/runtime/consumer 合同、必要迁移和目标验证齐备，当前完整候选经正式 Check、Task Commit、独立 committed Architecture、完整 Branch Review 与 Delivery Review。Delivery merge 后由原 Completion 独立判断整体 scope；merge 不等于 Task 完成。无业务生产或完整 Release 矩阵义务。

## Docs SSOT Plan

strategy=delta_first。原 `guru-maintain-requirements-design-test-ssot` writer 拥有 `docs/requirements-design-test-contributions/600-promotion-before-check/` 的 manifest、requirements、design、test 和 traceability；Test 单写实际证据、首次失败/恢复及未验证边界，其余只引用。Requirement/Design/Test 适用起点为 `.103`，Architecture 为 `.95`。在最终 Phase2 前完成 reconciliation 和本次必须交付的知识晋升。Architecture promotion 只由其原 owner 执行，不能由 RDT writer 代替。

## 实施顺序

1. 演进 Architecture package 的 pre-Check promotion 版本、candidate/result 绑定、恢复与适用性合同及对应定向测试。Planning/无影响路径保留。同步受控 consumer 和 eval 调用，不保留失去支持用途的旧 current 入口。
2. 在 Branch Review package 实现窄引用/状态修订 profile、原完整 Review 及全部差额绑定、原正式 passed 结果与 Delivery consumer。保留 Git continuity 原语义与 finding lifecycle。
3. 更新 canonical workflow 和直接受影响的 Check、Commit、Delivery/Completion、Author/Approval 文案或路由，消除 post-Review 例行晋升及整体回退。原职责继续由 step-local skill 独占，workflow 只编排和消费 exits。
4. 写 MIGRATION-600、必要 README/受管 spec、Architecture contribution 与 ADR successor、RDT 增量。完成匹配 workflow 和完整 preset apply/reapply，逐项处理 sidecar，核对用户区块与其他任务不变。
5. 独立 Architecture reviewer 审查完整候选及拟晋升内容；原 owner expected-current 写入，核对实际差额并接最终 Check。实际状态不能因文档存在而预填通过。
6. 运行最小验证集，更新唯一 Test。正式 Check → Task Commit；提交后合法 Check 刷新/clean re-entry 按原合同执行。新的 fresh committed Architecture 与独立完整 Branch Review 覆盖全部实现、文档和晋升文件。
7. Delivery Review → Publish → Merge → 整体 Completion → Closure → Finish bookkeeping → Cleanup。PR 使用中文、Refs-only；只有整体 Completion 后原 Closure 执行来源 disposition。

## 验证与证据

| 验证对象 | 方法与可观察结果 |
| --- | --- |
| Architecture 新入口与实际绑定 | production wrapper/module 定向测试覆盖真实 worktree candidate、受审差额一致/变化、expected-current mismatch、partial/output-loss recovery、no-change；旧未发生 committed Review 不再是入口前置。 |
| Review 窄修订 | 原完整结果与全部 Git 差额经实际 recorder/checker/invoke，正式结果覆盖最终 candidate 和当前 Check；新事实或合同变化、不可恢复来源走原恢复/完整审查。普通文档修订不使用 Git continuity。 |
| 完整链 | 在同一真实候选上观察独立 reviewer、晋升前后状态、最终 Check/Commit/committed Review 和下游 consumer；预填 DTO、词匹配或 schema 通过只计客观合同证据。 |
| 消费者与分发 | 受影响 package/runtime tests、公共 graph/schema、canonical/installed/声明平台验证；必要的真实 Git cross-package fixture。 |
| 安装与漂移 | 完整 apply/reapply、drift、sidecar、manifest、用户区块保留。需要干净安装证明时最多一个代表性 throwaway；不执行完整矩阵。 |
| 文档与质量 | 当前 source AC1..8 到设计/测试逐项 trace；git diff --check、受影响 Python/Bash 语法和 official task validate。 |

未知、新增或变化的检查义务执行受影响检查。工程原始结果仅在真实输入、依赖、环境和期望仍适用且可核查时采用；当前语义判断和结果绑定始终由本轮 owner 完成。不得为数量新增镜像实现或固定声明自证测试。

## 修改边界与回滚

修改限于受影响 canonical workflow、原 Skill/public I/O/runtime/consumer、测试、Docs、受管 projection 与本 Task。主要职责和 exact API 约束见唯一 design.md。源码文件超过 3000 行时先由原 owner 判断机械拆分；不牵入无关历史大文件。

回滚为撤回本次匹配 source 改动，并沿原完整安装路径 reapply；无 DB、容器、K8s、CI/CD 或生产迁移。保留 TaskId、DeliveryKey、已经发生的 Git/GitHub 事实和旧版本历史。
