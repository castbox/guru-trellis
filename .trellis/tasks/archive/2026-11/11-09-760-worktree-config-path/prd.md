# #760 worktree 配置路径承接：整体需求

## 1. 来源与术语

|来源|章节|角色与用途|
|---|---|---|
|https://github.com/castbox/guru-trellis/issues/760|完整正文，2026-11-09T04:55:00Z|唯一 Direct Source；下文按来源完整承接|
|trellis/workflows/guru-team/config-template.yml|workspace_mode/worktree_root|现行配置兼容合同|
|Issue #212 与 #718 归档 PRD|配置语义、资源身份解耦|历史证据；仅保留当前来源明确承诺|

primary 指同一 Git common-dir 下由 live Git topology 确认的主仓库；生成 root 是新位置策略，不是已有 checkout allowlist。

## 2. 背景与问题

消费者的正式 Task 从 Codex 已有 linked checkout 发起 Intake。Guru 另建 Task worktree 时，AI 把绝对 checkout_root 填为 Codex 托管目录下的另一个位置，没有按项目 worktree_root 配置解析。该新位置没有绑定到桌面 chat，被桌面自动清理视为 ownerless，实施期间及提交前各删除一次。第二次删除成功与提交命令启动相隔约 0.18 秒，命令因 cwd 不存在而未启动；不能归因于 commit wrapper。

现场来源：chat 01a1bb8b-4f72-7950-ab6e-1d9306f7cbec，castbox/ai-chat-roleplay-backend#1232。北京时间 2026-11-08 23:48:42 和 2026-11-09 00:54:42 两次删除日志均为 worktree_auto_cleanup / startup-cleanup，force=true，git-remove-result success=true。清理计划将同一 worktree 记为 ownerThreadId=null、reason=ownerless、isProtected=false。应用 chat 关联 c8de checkout，Task 使用另建的 1232 checkout。日志已确认删除前有 snapshot；本项不接管业务代码恢复。

### 根因与证据边界

本仓诊断基线为 main@8c158381b5bdb61fd961cbb89e23c2d1f659c9aa。

1. 配置模板仍声明 workspace_mode: worktree，worktree_root 为空时使用 ../<repo-name>-worktrees。历史 #212 明确覆盖默认、绝对与相对 root；本次是现行 acquisition 链路的配置承接回归，不能复用旧实现的通过结论。
2. guru-create-task 的 Markdown 要求审查绝对路径，但未要求新建路径先承接 worktree_root，也未明确 primary/linked/detached 调用采用哪个仓库锚点。现场 creation 输入在 executor 前已选错位置。
3. trellis/skills/guru-team/packages/guru-create-task/runtime/invoke.py 的 _plan 直接把 acquisition.checkout_root 解析为 target_path；runtime/task_lifecycle/checkout_acquisition.py 用该路径执行 git worktree add，未核对配置推导的新建位置。确定性配置解析没有成为创建前的实际 consumer。
4. guru-select-workflow-mode/runtime/environment.py 将空 worktree_root 回退为调用 root.parent，并原样返回显式配置值，与模板的目录规则不一致。此为已确认的接口语义差异；没有证据证明本次 AI 从该查询值推导了错误路径。
5. Task 创建测试中的新建场景直接指定 checkout_root；这些测试仍能证明其声明的创建/恢复行为，但没有证明“读取项目配置 → AI 生成新路径 → 公开创建 → Git 注册及后继绑定”的连续行为。不能据此宣称整个测试体系无效。
6. 已定位的历史断点：#434 的迁移提交 [a6b6d633c304dc5c51b0e24fbf0baf8e7a69df9a](https://github.com/castbox/guru-trellis/commit/a6b6d633c304dc5c51b0e24fbf0baf8e7a69df9a) 删除了旧 guru-create-task-workspace 包，包括 runtime/common.py 的 resolve_workspace。该 resolver 曾消费 worktree_root 并处理空、绝对、相对 root；当前新建链路没有承接这项能力。这里确认的是旧能力退出与当前缺口，不把 environment 查询差异的全部历史归因都归给此提交。
7. task-free 是独立入口。当前 guru-execute-task-free-change/references/contract.md 明确使用普通 Git 获取位置，不调用 Task acquisition wrappers。其问题是同样缺少新建位置配置承接，不是复用 Task executor 后产生同一代码缺陷。

不修改 Codex 自动清理规则。仅关闭清理、提高保留数或反复重建原错误目录不能修复 Guru 的路径选择偏差。



## 3. 目标与非目标

让 Guru 自行 provision 新 linked worktree 时遵守同一项目目录合同，从 primary、linked 或 detached checkout 发起都得到一致结果。范围覆盖 guru-create-task 的 provision_linked_worktree、guru-execute-task-free-change 的普通 Git 新建路径、环境查询及直接 consumer、配置说明和受管投影。两种入口承接同一配置语义，但保持各自原 owner 与执行边界；本项不要求 task-free 使用 Task acquisition。已有 checkout 的合法采用与原 Task 恢复保持各自身份与位置适用性合同；本项不把“位于配置 root 内”变成采用已有外部 worktree 的通用前置。


非目标：不恢复业务 #1232，不改 Codex 自动清理或上游 Trellis，不搬移或删除既有 worktree，不实施暖池、锁、竞态或 crash consistency。

## 4. 真实调用方、场景与流程

- S1：AI 从 primary、linked 或 detached 调用新建，先读主仓库配置和 topology，再审查命名与路径；同一配置产生同一 root。
- S2：正式 Task 由原 acquisition 创建并建立绑定；task-free 由原 owner 用普通 Git 创建并复核位置。计划路径、实际目录、Git 注册与后继读取一致。
- S3：配置生成计划与解析结果不符时，在 branch/worktree/Task 首次副作用前诊断；原 owner 修正计划再调用。
- S4：调用方显式新位置、采用外部 checkout 或恢复原 Task 时，沿原合法路径及身份检查；不受生成 root 位置限制，不重定位。

## 5. 行为要求

- 配置驱动的新建位置以同一 Git common-dir 下、由 live Git topology 确认的主仓库为项目锚点，读取该项目的 .trellis/guru-team/config.yml。空 worktree_root 使用 <主仓库父目录>/<主仓库名>-worktrees；绝对配置直接采用；相对配置相对主仓库根解析。未改变项目配置或显式位置选择时，从 primary、linked 或 detached checkout 调用得到同一生成 root。不能仅取调用 cwd.parent，也不能假设 common-dir 的父目录必然是主仓库。配置来源、项目锚点或位置选择有真实冲突时，给出原 owner 可处理的准确诊断，不自动覆盖各 checkout 的配置。
- AI 先读取该项目配置和 live Git topology，再在原 Skill 内判断新建或采用、命名、范围、冲突处置及副作用计划。脚本只负责确定性路径解析、创建前一致性验证与 Git 动作，不新增脚本语义规划器。
- 配置驱动的新建路径由生成 root 与本次已审命名形成。环境查询、计划中的路径、实际 Git 创建和后继 consumer 使用同一解析事实。正式 Task 继续通过原 acquisition/checker/binding；task-free 继续由自身 owner 使用普通 Git 并复核位置适用性，不创建 TaskId、TaskBranchBinding、Task session、task.json 或新位置映射。不得把 Codex 当前工作目录、相邻已有目录或示例路径当作配置替代。
- 区分三种位置来源：按配置生成新位置、调用方显式选择新位置、采用或恢复已有 checkout。worktree_root 是生成位置合同，不是所有 checkout 的目录 allowlist。现有 public input 允许显式绝对 checkout_root，不能仅因它在生成 root 外就悄然改成非法。Planning 必须说明生成策略、显式位置选择与路径参数的可机器验证合同及旧调用迁移；AI 负责读取实际意图、选择策略和展示精确副作用，脚本不判断或记录用户授权。
- 在配置驱动的新建路径中，普通调用方计划与解析结果不一致时，须在创建 branch/worktree/Task 前准确诊断并回到原 owner 修正计划，不能静默换路径。真实显式新位置沿原兼容合同处理，不能从 AI 自行填入绝对路径反推用户要求该位置；显式项目配置也不能被通用“更安全目录”规则覆盖。采用已有 checkout、原 Task 恢复不受生成 root 限制，仍检查各自真实身份、绑定和位置适用性。
- 新配置解析不得改变已存在 TaskId、generation、branch binding、Delivery、session 或资源归属。恢复已有 Task 时按已验证绑定找原位置，不因默认目录变化搬移或重新创建。
- 复用现有 Skill 和 runtime ownership；确定性配置解析应有真实 consumer，不能只新增查询而不接入两个创建入口。公开参数或输出若需收敛，须在本项规划中明确兼容/迁移与受影响调用方，不静默改变既有语义，也不为 task-free 强加 Task-specific validator。workspace_mode: current 的历史存在不授权恢复现已退役的 primary 写入路径。不新增映射台账、审批链、平台专用清理进程或长期路径证明 artifact。


## 6. 约束与依赖

保留两个入口的原 owner、Task/branch/worktree/runtime 独立身份。Markdown 由 AI 判断策略和范围；脚本只解析配置、验证一致性与执行 Git。公共输入兼容/迁移在 Delivery design 明确，不持久化授权或新增长期路径证明。

## 7. 可观察验收与验证方式

采用能检出本次配置承接缺陷的最小验证集；已有证据在输入、入口和依赖仍适用时直接复用。同一证据可以覆盖多项要求，不按下列条目重复建立完整生命周期样本。

1. **路径解析正确。** 定向测试覆盖空、相对、绝对 worktree_root 的既定规则，并用代表性 primary 与 linked/detached 调用证明同一项目配置不因调用位置而改变生成 root。不要求所有配置与 checkout 形态的组合矩阵。
2. **创建入口实际消费配置。** 正式 Task 与 task-free 分别沿自身原 owner 承接解析结果。用代表性真实 Git 创建验证计划路径、实际目录、Git 注册及直接后继的位置读取一致；另一入口只补尚未覆盖的自身差额。配置生成策略中的路径不一致在首个创建副作用前得到准确诊断，纠正后能沿原入口继续。不能只新增无人消费的查询或只测私有解析 helper。
3. **保留合法位置行为。** 针对本次改变的路径选择和校验补充或复用回归证据，确认合法显式新位置、已有外部 checkout 的采用、原 Task 恢复不被生成 root 规则误拒绝或重定位；task-free 不因此引入 Task 身份或绑定。原身份及位置适用性检查继续有效，无须为未变逻辑重复整套 Task/Delivery 生命周期。
4. **变更可交付。** 通过受影响 package/runtime 的定向验证；对实际修改的配置说明、Skill 和受管投影完成同步及漂移检查。报告验证入口、观察结果和未覆盖边界，不以文件存在或测试数量代替行为证据。

不单设完整真实 Agent 创建链、完整业务恢复演练或 clean throwaway 安装作为本项通过条件；仅在现有证据无法回答具体缺口时补最小验证。完整多平台安装、升级及 Release 矩阵仍由专门工作承担。无需触发 Codex 自动清理、删除业务 worktree，或要求业务 #1232 再次复现目录消失。


关联边界：#212 只作历史配置承诺，#718 保留独立身份；#759 prunable peer 与 #152 暖池独立。

## 8. 实际未决项

没有需求层未决问题。实现兼容策略和最小验证安排由 Delivery Author/Architecture 细化。未执行实现和验证，不预填通过。
