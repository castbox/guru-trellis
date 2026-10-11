# Guru #521：主 checkout 保护与 task-free 隔离

## Authority 与交付目标
Direct Source：https://github.com/castbox/guru-trellis/issues/521 ，实施前重读正文与评论。业务采用边界：https://github.com/castbox/ai-chat-roleplay/issues/120 ，不在本任务直接升级业务仓或修改其产品合同。
当前基线：44a8b9c1f8495e2f811f892f248a1f2693a8bc80。Requirements/Design/Test 为 docs/{requirements,design,test}/README.md 指向的 current-main-0.6.17-guru.84；Architecture 为 docs/architecture/README.md 指向的 .83；设计原则以 docs/architecture/00-foundation/design-constitution.md 为唯一来源。

目标是修改类工作从第一处写入开始位于已注册 linked worktree 和非 base 工作分支；主 checkout 的 HEAD 所属 ref 不被工作请求改变。task-free 保持无 Task、无 activation/session bind、无生命周期文件。只读工作不创建资源。此能力是诚实 Agent 流程合同，不是 unrestricted shell 的权限隔离。

## 必须行为
- R521-01：写入、续接与发布前读取本仓 live topology、当前目录/branch/HEAD、dirty/untracked、目标完整差额与当前聊天真实 binding。其他聊天 inventory、路径或分支名不建立身份。
- R521-02：首次写入前复用适合当前范围的 linked worktree；没有合适位置时展示精确路径、branch、来源 ref/HEAD 和副作用并消费当前对话授权后创建。不得在主 checkout 原地 switch、创建工作分支或 detach。主分支切换只有精确授权例外；正常 Sync 保留原 owner。
- R521-03：task-free acquisition 不调用 Task 专用创建、激活、绑定和 Task 专用位置校验；不生成 TaskId、task.json、TaskBranchBinding 或 created DTO。
- R521-04：start、普通继续、workflow-state 与新聊天恢复 fresh 核对范围、位置和 binding，合法 task-free 回原 owner。显式 upstream continue 的 no_current_task 由 Guru workflow caller 消费，不能等价为必须建 Task；绑定 stale/conflict 准确拒绝。
- R521-05：同聊天有效 Task binding 按原身份/re-entry 合同处理，不静默清除或覆盖；无关聊天 Task 不阻塞本次工作。覆盖同一 Git common-dir 中跨 worktree 的绑定可见性。
- R521-06：保留全部无关 dirty/untracked、部分候选与现有资源。不自动 stash、搬运、reset、覆盖、删除或混入提交。输入/执行位置缺失只阻塞依赖动作，不回退主 checkout 写入。
- R521-07：自动 task-free 扩张回 reselect_mode 的 selector；显式 task-free 扩张回 explicit_choice_required 的原 owner。检测后立即停止剩余目标写入，保留真实部分修改。standard intake 不自动创建/绑定 Task；精确复用或另选隔离位置与承接差额各走原副作用边界。
- R521-08：正式 Task 创建也使用 linked worktree；保留独立 commit/push/PR/merge/release/install/cleanup 边界。同步 canonical、适用 runtime、模板、dogfood 和安装投影，旧 current-checkout 合同直接演进。
- R521-09：实际 Agent 轨迹、定向客观测试、目标安装行为分别报告；未执行不算通过。不修改 upstream-owned start/continue/extractor/hooks；无法消费返回时准确列出 upstream owner 和未交付依赖。

## 验收
T521-01：干净主 checkout 发起 Task 与 task-free 修改，写入位于 linked worktree 非 base 分支；主 checkout ref/HEAD 保持（独立 Sync 的正常快进单列）。
T521-02：合法复用、只读不创建、缺失位置与授权未取得不写入。
T521-03：无 Task start/普通继续/新聊天恢复/显式 continue caller 实际接续；零 Task 创建/激活/绑定副作用。
T521-04：其他聊天 Task、同聊天同范围/不同范围、stale/conflicting binding 正确分流；common-dir 可见性实测。
T521-05：主 checkout dirty/untracked、隔离候选与多个并行 worktree 保持原内容；“按建议修复”“提交 push”不原地 switch，发布只消费获准隔离候选。
T521-06：自动/显式 task-free 各自部分写入后扩张，剩余写入停止，真实原 owner 回程；收窄或 standard intake 后候选和无关内容完整，不重复承接或静默绑定。
T521-07：clean install/update/reapply 定向验证中 upstream-owned 入口字节不被 Guru 改写；若依赖未交付，不声称显式 continue 全链可用。
T521-08：旧 current-checkout 合同迁移与正式 Task/base Sync 回归；源验收不代替业务 #120 目标安装。完整多平台 Release matrix 和真实发布另列未验证。

## 非目标
无新长期 checkout mapping、授权/人员账本、第二生命周期、临时 adapter、Git hook 自动切回、OS 隔离或无消费者抽象；不认领其他 Issue 的独立交付，不实施业务安装、Release、清理或部署。

