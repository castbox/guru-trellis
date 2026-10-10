# 实施计划

## 顺序与交付

仅在三份规划 current gates 通过、展示并取得 activation 接受后实施。保持唯一 #468 TaskId / generation / branch / registered checkout。当前任务本身的首次 activation 仍通过未修改的 current 正式 owner；候选行为在 isolated Git fixtures 中验证。

1. 完成 current-contract gap analysis 与 16 场景 owner mapping，核对 current Source、Clarification、Planning、Check、Delivery、Completion、Closure、Reactivate；已支持行为只补定向证明或必要说明。
2. 在 canonical guru-activate-task 与 shared lifecycle composition 上原地加入 resume_execution / recover_execution、最小 execution-result recovery/retirement；版本化 public schema aggregate，同步 interface、示例、唯一 consumer projection、registry 和 docs。保留 activate/recover_activation 原语义及已有真实 session/current-checkout 校验。
3. canonical workflow approved 唯一 consumer 增加 lifecycle 分支，唯一 continuation 增加活动重规划与正常输出丢失窗口。Planning owner 不新增批准/授权持久化；Check 只在实际 current passed handoff 后通过原 execution owner 删除 checkpoint。
4. 按 Docs SSOT Plan 写 isolated RDT delta、适用 Architecture contribution/ADR，不先修改 shared current。实现发现真实新边界先 qualification 与 fresh independent Architecture，禁止自行扩大范围。
5. 用 preset apply 同步 dogfood，逐项处理 .new/.bak；运行定向 tests、平台投影、installed、reapply/drift、sidecar/mode；完成 task validation 和 git diff --check。
6. fresh independent Phase2 Architecture + current guru-check-task；单独展示 commit 计划并确认后提交；fresh independent committed full-diff Architecture/Branch Review；按 existing SSOT promotion 切换 current 并对新增 promotion diff 再完成 Phase2/commit/Branch Review。Publication、merge、Closure、Finish、Cleanup 各自保持独立精确计划确认。

## 文件责任与影响范围

- workflow：trellis/workflows/guru-team/workflow.md、两个 README 与 dogfood .trellis/workflow.md。
- local owner：trellis/skills/guru-team/packages/guru-activate-task 的 SKILL/interface/schema/examples/consumer/runtime/tests；必要 Planning/Check/Clarification/Completion/Reactivate 文案不复制 global workflow。
- deterministic shared facts：trellis/skills/guru-team/runtime/task_lifecycle/composition.py 与最小 execution-result helper、tests/test_composition.py 和执行结果生产入口测试；不在脚本写 scope/Issue role/semantic pass 分类。
- preset/platform：canonical spec、必要平台入口 projection，以及 apply 后的 .agents/.codex/.trellis installed copies；不修改 upstream agents/hooks/node_modules。
- repository SSOT：docs/requirements-design-test-contributions/468-direct-source-replanning-compatibility/；Architecture task-owned路径由独立 owner 确认。
- 不编辑 Backend 安装、业务生产、无关任务、分支或 workspace journal；不执行 Issue mutation/push/PR/merge/cleanup，直到各自明确确认。

## 风险匹配验证

| 验证 | 正式入口与可观察结果 |
| --- | --- |
| 首次激活、首次结果丢失 | 当前 Planning recorder/checker/invoke 得到真实 approved；activate 改 status 一次；recover_activation metadata 字节保持 |
| active 重规划 | 修改合法 planning 内容、fresh Planning approved；resume_execution 返回 execution_resumed，TaskId/gen/branch/checkout/status/control ownership保持，status mutation 次数为零 |
| approved 丢失、展示等待接受、接受丢失 | 通过唯一 continuation 实际 current facts 回 producer fresh re-entry并重新展示，不缓存或重建接受；确认当前对话边界由 AI 判断 |
| 恢复执行完成后 stdout 丢失 | 丢弃真实 invocation stdout，保留原 owner 生成结果；recover_execution read-only 得到同一正式结果，metadata/checkpoint 字节不变，消费后 retire |
| 内容、TaskId/gen、branch/current checkout、session、base 正常变化 | 使用正式 task/session/rebind/base 操作或正常文件修订产生 stale/mismatch；观察拒绝/refresh/re-entry，无手工伪造 hash/state 负例 |
| Source/disposition/no-Issue 与重开分流 | existing source/completion/closure/reactivate wrappers与 current semantic owner 的定向 cases；分别证明 actual层次，不把固定 owner envelope 当作智能分类实现 |
| Repo SSOT | RDT trace requirement->responsibility->test 与 Architecture current consumer；必要更新/不适用有真实依据 |
| 分发 | canonical/dogfood drift；代表性 installed wrapper；声明平台文案 projection；preset reapply、sidecar/mode、task validation、diff hygiene |

不扩张为完整 Upgrade/Release 多平台 throwaway 矩阵；最多一个代表性 clean installed fixture，并明确实际安装入口与未验证的官方 init/update、远端版本、Backend 安装/业务重试和生产效果。包级绿色结果只证明其观察层。

## Docs SSOT Plan

strategy：delta_first。
durable_paths：
- docs/requirements-design-test-contributions/468-direct-source-replanning-compatibility/requirement.md
- docs/requirements-design-test-contributions/468-direct-source-replanning-compatibility/design.md
- docs/requirements-design-test-contributions/468-direct-source-replanning-compatibility/test.md
- docs/requirements-design-test-contributions/468-direct-source-replanning-compatibility/traceability.md
- docs/architecture/contributions/468-direct-source-replanning-compatibility.md；ADR 按独立 owner 的当前适用结果处理。

Required delta：R468-01 单一 Direct Source与用途边界；R468-02 actual authority earliest-owner/invalidation；R468-03 active replan execution/recovery；R468-04 no-Issue/disposition/reopen与repo SSOT；R468-05 canonical/installed/platform distribution。
对应 D468-01..04 设计 responsibility 与 T468-01..05 风险匹配证据；Test 层唯一记录真实结果和未验证边界，不复制 claims。Shared current 的 expected identity 为 current-main-0.6.17-guru.80 / active，promotion 前重新读取；漂移回 existing owner。

Completion 必须检验本任务全部 accepted scope、当前仓库必要 SSOT 和其真实证据；不能仅凭已 merge 或 package tests关闭需求。当前没有执行实现或候选验收测试。
