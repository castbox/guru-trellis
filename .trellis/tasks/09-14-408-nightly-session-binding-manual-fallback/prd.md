# #408 Nightly 会话绑定与手动 Git/GitHub 完成

## 目标与需求来源

唯一变更需求是 [castbox/guru-trellis#408](https://github.com/castbox/guru-trellis/issues/408)。
本任务吸收指定上游修复，使旧 Guru 生命周期在 linked worktree 场景中保持可用；自动流程异常时，用户明确指定的独立 Git/GitHub 操作仍有可执行路径。

当前产品基线为 `docs/requirements/README.md`、`docs/design/README.md`、`docs/test/README.md` 指向的 `current-main-0.6.5-guru.50`。继承 `R378-02..04`、`R329-02..10`、`R247-01..10`，本任务只记录其变更增量。

## 当前事实

- Guru source lock 位于 `trellis/presets/guru-team/source/trellis-source.json`，当前 commit 为 `a2003296b4c4ce46c50d72ead3b2ec9c317f69fc`，CLI 为 `0.6.17`。
- 上游 PR #5 已合并为 `db4ca1dfbb5abaf9be62b2a01b70dda3f80df0f0`；CI `34838784963` 对应相同 SHA，结论为 success。该结果不是 Guru candidate 的安装或生命周期验证。
- 当前正常链保持 Phase 2、Task Commit、Branch Review、Publication、Finalizer、Merge。Developer/workspace journal 与 Issue Scope Ledger 已退役。
- 当前任务的 Git branch、official task metadata 与两份 Guru mapping 一致；`get_context.py` 仍显示无 current session task。此现象不作为重复创建任务或修复上游的依据，根因由实施阶段正向集成复现确定。

## 需求与验收

| ID | 要求 | 可观察验收 |
| --- | --- | --- |
| R408-01 | 精确采用 `castbox/Trellis@db4ca1dfbb5abaf9be62b2a01b70dda3f80df0f0` 与 CI `34838784963`；CLI/core 均保持 `0.6.17` | source lock、构建来源验证、installed source record 与实际运行 CLI 对应相同 commit/CI；无 `v0.6.18` 依赖 |
| R408-02 | Trellis-owned 文件通过固定 Fork 的正式 build、update/init 生成；Guru-owned 文件从 canonical 同步 | source、dogfood、installed 模板与运行路径一致；preset reapply 与 drift 通过；未知用户改动保留 |
| R408-03 | 同一明确 session 从 primary 创建 linked-worktree task 后回到 primary，继续解析同一 active task | `task.py current`、`get_context.py`、SessionStart、workflow-state 均指向该 task，不错误注入 `no_task`；不读取 foreign session |
| R408-04 | 保留旧完整 lifecycle、现有 Skill/exit/Finalizer/Publication/Merge 与 task/worktree 语义 | 现有 package、finish-family 与 installed 链回归通过；无新节点、Skill、typed exit、recovery checkpoint；已退役依赖不重现 |
| R408-05 | workflow-state/session/task routing/hook/checkpoint/wrapper 普通异常导致自动流程停止时，准确报告现状 | 报告失败步骤、原始错误、已知 repo/task/worktree/branch/Issue/PR、未完成步骤；无法读取的事实标为 unknown；不转入新 Intake、不自修复、不虚报完成 |
| R408-06 | 用户明确要求手动 commit、push、PR 创建/更新、merge、Issue closure、tag/Release 或 cleanup 时，独立处理该操作 | 各操作前重读 live facts，展示精确目标、path、HEAD、命令、预期结果并取得该操作自己的确认；前项操作不触发后项操作 |
| R408-07 | 手动操作成功不改变 Guru 生命周期事实 | 分别报告 Git/GitHub 结果与 task/runtime/Finalizer/archive residue；不补写或伪造 Guru gate/archive；residue 不禁止已经独立确认的操作 |
| R408-08 | 验证与发布证据分层 | 执行 `implement.md` 的验证集合；缺失验证写为 `UNVERIFIED`，不能由上游 CI、mock 或文本断言替代真实 installed-mode 证据；Guru 发布沿用现有 release contract |

## 范围与限制

本任务覆盖 canonical source provenance、workflow/现有 Guru Skill 文案、三平台 Guru 入口、受影响脚本与测试、正式生成的 dogfood 文件、README 和任务隔离的 RDT/Architecture contribution。

不实现 #398 新生命周期或 #407 冲突提交恢复；不修改 `castbox/Trellis` 源码；不发布上游 npm、不创建上游 `v0.6.18`；不恢复全局 current task、developer/workspace journal、Issue Scope Ledger；不新增自动恢复编排、共享状态、锁、进程/FD authority 或对抗性测试。

现有 secret redaction、权限、破坏性操作确认、Git transaction 状态和远端规则继续有效。手动路径不代表跳过操作本身的正确性检查，也不自动成为 Guru lifecycle 的合法完成记录。

本任务没有未解决的产品范围问题。实现所需的本地 Fork build、模板升级与真实安装证据尚未产生，属于后续执行门禁；正式发布、Issue closure 与 cleanup 均为独立操作。
