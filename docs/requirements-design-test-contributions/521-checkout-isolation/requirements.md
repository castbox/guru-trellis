# #521 隔离修改增量需求

状态：candidate；Direct Source：[Guru #521](https://github.com/castbox/guru-trellis/issues/521)。继承 current RDT `current-main-0.6.17-guru.84` 与 Architecture `.83/active`。本增量不替代 canonical workflow/Skill 的步骤定义，不证明安装或发布。

| Identity / behavior | 必须行为 |
| --- | --- |
| R521-01 / BEH521-FACTS | 写入和续接前读取真实 Git topology、registration、common-dir、branch/HEAD、完整 dirty 差额与当前 session binding；路径/分支名/其他聊天 inventory 不建立 Task 身份。 |
| R521-02 / BEH521-ISOLATE | 修改从首次写入起在适合当前范围的 linked non-base 工作树；只读零创建；无适合位置先取得位置。主 checkout 不被工作请求切换 ref，正常 Sync 和精确例外由原 owner 处理。 |
| R521-03 / BEH521-NO-TASK | task-free 位置选择不创建、激活、绑定 Task，不使用 Task 专用 API/位置校验，不生成 TaskId 或生命周期文件。 |
| R521-04 / BEH521-CONTINUE | start、普通继续、新聊天和显式 continue 的合法 task-free 回原 owner；Guru caller 消费 upstream no_current_task，不能将无 Task 转成建 Task 前置。 |
| R521-05 / BEH521-BINDING | 有效当前 Task 回原 owner，stale/conflict 停止；common-dir 跨工作树绑定可见性和其他聊天互不误选得到实测。 |
| R521-06 / BEH521-PRESERVE | 保留全部无关内容和已有候选；不自动 stash/reset/搬运/删除/混入提交；位置不足不回 primary 写入。 |
| R521-07 / BEH521-EVOLVE | 自动/显式扩张分别走 reselect_mode/explicit_choice_required；立即停止剩余写入；standard intake 仍独立创建 Task，clean acquisition 和精确承接共同保留候选。 |
| R521-08 / BEH521-CREATE | 正式新 Task 采用 linked non-base checkout；create-only 拒绝 primary，不全局破坏旧 Task recovery、Sync 或 Cleanup。canonical/安装投影同步，旧 current-checkout task-free 直接退出 current。 |
| R521-09 / BEH521-EVIDENCE | 真实 Agent 接续、客观 runtime 与目标安装分别证明；Guru 不修改 upstream-owned start/continue/extractor/hooks。未满足的 upstream 依赖不算显式 continue 通过。 |

[设计](design.md)、[验收及结果](test.md)、[双向 trace](traceability.md)分别拥有本层内容。业务 [#120](https://github.com/castbox/ai-chat-roleplay/issues/120) 保留实际安装和 PHX 正向输入验收；完整 Release 矩阵与发布不由源测试推定。

