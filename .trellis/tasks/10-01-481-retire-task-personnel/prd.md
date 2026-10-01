# #481 退役任务人员身份

## 目标与来源

来源：`castbox/guru-trellis#481`，以 2026-10-01 重新读取的线上正文、无评论状态，以及 `castbox/Trellis#23`、已合并 PR #24、Guru #454/#292 为准。当前 base 为 `main@987635b025db3b5835317b7e7b5326baa83c275f`。

让 Guru Team 的当前运行与分发合同使用上游已退役任务人员身份后的 Trellis。任务身份只来自 TaskId、generation、结构化 source 与当前绑定事实；普通用户交互、GitHub assignee、Git author、AI owner 和资源 cleanup owner 保留各自原语义。

## 需求

- R481-01：采用包含上游 PR #24 的真实可安装精确 Fork ref，并同步 source lock、版本/来源投影、README 与安装 provenance。旧 `8336e78b...` 不得作为本 Issue 的安装验收来源。
- R481-02：移除所有活动任务人员身份询问、查询、推断、传递、保存、展示和恢复。`guru-create-task` public input/schema、AI gate、executor、示例和测试不再接受或传递 creator/assignee；不加入别名、隐式填充值、空占位或双格式执行。
- R481-03：保持 #454 的 TaskId/generation、source、path-free session 和 TaskBranchBinding、live checkout resolution、显式 rebind/switch、Finish 终态解绑及 caller/guru 资源归属。无 context key 时支持显式任务模式。
- R481-04：当前 clarify owner 加载的 `trellis-brainstorm` 只用于需求探索；任务创建、激活和完成仍由 Guru owner 承担。不实施 #292 的 `guru-author-task-plan` 或全局 Phase 1 切图。
- R481-05：带退役字段的旧 task、旧 public input 与旧安装明确拒绝，不自动改写历史。旧归档 TaskId 仅防复用；按 TaskId 或严格精确 Issue 线索定位时只读拒绝，不作为当前任务、Reactivate 或 Finish 候选。线索缺失不阻塞无关任务；冲突/不唯一明确报歧义。符合当前 schema 的归档维持正常恢复路径。
- R481-06：canonical、dogfood、installed、声明平台入口同步；preset reapply、drift、sidecar 和 update 后不残留活动人员参数或提示。公开破坏性接口提供明确迁移与版本边界，不提供兼容执行。

## 验收

- AC481-01：Issue-backed 与 no-Issue 创建无需人员字段；真实上游 CLI 与 Guru public input 均不传这些字段，旧输入被 schema 拒绝。
- AC481-02：新任务可完成 #454 的 session bind/switch/rebind/Finish retirement、branch establish/rebind/terminal retirement、checkout resolution 与 resource ownership 回归；旧归档存在不阻塞合法新任务。
- AC481-03：按 TaskId 或第 7 项精确 Issue 线索选择旧归档时返回旧格式不受支持；冲突/重复报歧义，reference_only/follow_up/parent 不误作原任务；符合当前 schema 的归档可 Reactivate。
- AC481-04：无任务 brainstorm 完成澄清且不创建/激活任务；#292 Phase 1 边界保持。
- AC481-05：受影响 package/runtime 定向测试、source/dogfood/installed、声明平台、代表性 clean install、reapply/drift、sidecar 与模式检查通过。完整多平台 Release/upgrade 矩阵由专门 Issue 承担，未跑时明确列为未验证。
- AC481-06：精确 Fork SHA 的构建、安装与 provenance 可验证；历史 task/归档字节不因本次实现而批量重写。

## 边界

不修改上游源码、全局 npm 或 `node_modules`；不修改业务仓库生产配置，不执行完整 Release Gate，不扩张到恶意输入或非常规并发加固。已有任务创建过程的临时引导不是产品兼容路径，也不进入公共接口。
