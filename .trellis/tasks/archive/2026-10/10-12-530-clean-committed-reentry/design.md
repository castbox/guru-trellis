# #530 设计候选

状态：Planning candidate。对象：当前 TaskCommit/Phase2/Reconcile/BranchReview 接续。Direct Source：https://github.com/castbox/guru-trellis/issues/530。

## 现状与职责

Workflow Phase2 passed 的 post_check pair guard unchanged 返回 TaskCommit；TaskCommit prepare 仅支持实际 dirty exact stage 集合。post_commit Reconcile 已创建整合提交，fresh Phase2 不制造 dirty，因此当前输入域缺少已提交候选。
ARCH-DOM-021 已将 exact committed candidate 交给 TaskCommit，整合提交交给 Reconcile，完整审查交给 Branch Review。保留这些 owner；Markdown 判断是否进入接续，脚本只验证当前事实和输出投影。

## 选择的机制

直接扩展 guru-create-task-commit 的现有 public invoke，新增闭合 committed_reentry 输入 profile，通过独立互斥参数 --committed-reentry - 接收一个 stdin JSON envelope。public_input 只含 profile、mode、task_ref、source_exit=passed、phase2_commit_anchor；owner_result 只承接本轮 TaskCommit owner 的最小语义结论（status、summary、evidence），不接受 selected exit、替换 Git facts 或授权字段。
此入口只核验已有 commit，不进入 prepare、exact executor、hooks 或任何 Git ref/index写入。成功继续返回既有 committed DTO 的 task_ref/base_ref/branch_review_commit；不新增 exit。它不是旧 --invocation compatibility projection，也不从 caller.result 构造成功。

Phase2 passed→post_check pair guard unchanged 后，TaskCommit AI owner读取实际完整 Git 状态：
- 有 dirty：执行原 prepare/exact commit 路径，原非空 exact_stage_paths invariant 不变；
- 完全 clean 且存在当前任务已提交差额：执行本 profile 的完整 semantic gate 与正式 invoke；
- 不明确或条件不满足：沿原 stale/blocked/re-entry，禁止人为 dirty、空提交或手工 DTO。

## 核验边界

D530-01 TaskCommit 读取唯一 TaskId/generation branch binding/registered checkout，要求 current in_progress 与当前 symbolic branch 一致；使用 task 当前 selected base，不能由 caller 指定替代 base。
D530-02 通过 Phase2 owner 既有检查端口验证 retained checkpoint 的当前 reviewed-content、typed_exit=passed、task_ref 和 capture ancestry，再要求 passed DTO anchor、checkpoint capture_commit 与 HEAD 完全相等。必要的代码抽取仅为复用原事实验证，不转移 semantic owner，不建立另一 reviewed-content 算法。
D530-03 核验完整 clean 工作区及 index、无 active merge/cherry-pick/revert/rebase/sequencer/am 状态。selected base 必须为 HEAD ancestor；HEAD 不能等于 base，完整 task range 必须真实存在。要求当前 task 元数据已在 committed candidate，不能以无任务 branch 接续。
D530-04 TaskCommit owner语义核对当前 task范围、完整 base...HEAD、当前 Phase2 和已有提交事实；脚本不判断任务范围或 full review 是否充分。formal output 成功后按现有 TaskCommit consumption 规则退休已消费的 Phase2 checkpoint，不产生新的候选或 receipt。
D530-05 committed DTO仍进入 post_commit pair guard；若 base 再演进，正式 Reconcile→fresh Phase2 重建当前证据。unchanged 才进入 fresh Architecture(branch_review)及独立完整 Branch Review。finding-fix/fresh-final intent 由既有 caller恢复矩阵选择，本入口不宣布 review passed。
D530-06 同步 current public schema、interface、command参数、examples/evals、Workflow callers 与 managed projections。旧非空 dirty profile、executor和其实际 supported diagnostic/recovery消费者保留；不增加新旧双读来支持此新能力。

## 备选与取舍

放宽 empty exact_stage_paths 会让提交 executor承担无提交职责，产生空提交风险，拒绝。
Workflow直接制造 committed DTO 会绕过 TaskCommit candidate owner，拒绝。
Phase2输出代替 full BranchReview、或用 bounded continuity 作为首次 review 会丢失独立完整审查，拒绝。
新增 Skill/状态/store无独立新职责；原 TaskCommit的 read-only profile足以承接，拒绝。
选择新增一项具名输入能力，换取同 owner明确区分 dirty mutation 与 committed verification；保留原 committed output和下游流程，避免扩大长期状态。

## Architecture 与 Docs SSOT Plan

Architecture 以 docs/architecture/README.md 的 active current-main-0.6.17-guru.84、唯一 constitution 和 change-contract 为依据。候选路径为 target_native；最终 impact/path/ADR由独立 Architecture owner判定，不预填 baseline_current。
拟写 task-owned contribution：docs/architecture/contributions/530-clean-committed-reentry.md。current/target owner与single-writer不变；无已有 GAP关闭/重开；公共 candidate输入域扩展与 Phase2消费规则需在贡献中绑定 before/after。是否需 ADR由原 owner判断。
允许：本 Task checkout 的 canonical packages/workflow、定向规范、贡献与受管副本；禁止：shared current提前晋升、其他 Task/仓库、upstream Fork源码/hooks/global安装。

Docs策略 delta_first：
- docs/requirements-design-test-contributions/530-clean-committed-reentry/requirements.md：R530与 BEH530 行为合同。
- 同目录 design.md：D530职责/CON530输入输出与 consumer。
- 同目录 test.md：唯一实际测试结果、首次失败/恢复、外部未验证边界；不得把计划当通过。
- 同目录 traceability.md：双向连接 Requirement/Behavior→Design/Contract→Test→changed canonical实现。
- 上述 Architecture contribution持有适用 concerns和promotion边界。独立 committed full review后，由既有 RDT/Architecture owner按当时 expected current串行晋升，再fresh Phase2/commit/fullreview。
不可变历史记录与 #444证据保持原含义，不批量改写。
