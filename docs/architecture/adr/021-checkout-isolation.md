# ADR-021：隔离修改与 creation-only primary adoption

- 状态：`accepted`；来源：#521 已独立审查 contribution 与 ADR-521-CANDIDATE。
- predecessor：ADR-005 的 expected-current promotion、ADR-006 的 base authority checkout、ADR-011 的单一 continuation 和 ADR-014/016 的 Task/session/lifecycle owners 保持。

## Decision

修改类 task-free 在本仓 registered linked worktree 的 non-base 工作分支执行。原 execution owner 判断真实 topology、范围、完整候选及当前 binding，消费 `location_required`，沿原独立 Git 副作用边界取得位置后 fresh 重入；selector 不以位置需求自动升级为 standard Intake。task-free 不创建 TaskId、TaskBranchBinding、task.json、Task session binding、mapping 或第二生命周期。

正式新 Task 的 primary adoption 禁令只位于 C6 creation preparation；旧 primary Task 的现有 acquisition/result recovery、base Sync 和 Cleanup 保留其 current consumers、clean 前置和原 owner。旧对象逐例迁移必须依 live binding/control state 与精确动作处理，不自动搬运或宣称完成。主 checkout 不被普通修改请求切换 ref；明确主 ref 例外仍是独立精确 Git 操作。

Guru workflow 的单一 caller continuation 消费 upstream 实际 `no_current_task` 后 fresh 读取本轮范围、位置和真实 binding，回原 no-task selector/execution owner。有效正式 binding 回原 Task owner，stale/conflict 停止；其它聊天 inventory 不建立本聊天身份。Guru 不 patch/delete/接管 upstream start/continue/extractor/hooks；native caller 无法消费时停止依赖路径并真实报告。

partial expansion 保留已有候选并停止剩余写入，自动/显式沿原 selector/execution owner 回程；standard Intake 的 clean acquisition 和精确独立承接边界不放宽。无 Issue 来源 profile 与执行 mode 独立：原 Review 接受 workflow/standalone，同时保持原 producer/public/owner mode equality、source/target 和后续 Task gates。

## Alternatives and consequences

强制创建 Task、第二 acquisition/store、primary fallback、自动 stash/搬运、全局 resolver primary 禁令或 upstream patch 均不能保留当前职责。直接演进既有 owners 是本次最小充分机制；旧 current-checkout task-free 合同退出 current，无双模式兼容。无新 GAP lifecycle、授权存储、OS 权限隔离或不可绕过承诺。

原 Architecture owner 按 expected `.83` 晋升 `.84`；[唯一 Test](../../requirements-design-test-contributions/521-checkout-isolation/test.md)分别拥有定向 runtime、原生 Agent 接续和代表性 local-candidate 安装证据。晋升新 diff 必须 fresh Phase2/TaskCommit/独立完整 Branch Review；业务 #120 安装、完整 Release matrix、软件发布和生产效果尚未验证。
