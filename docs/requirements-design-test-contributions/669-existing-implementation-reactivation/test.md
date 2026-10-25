# #669 Test：实际结果与观察边界

观察截止：当前源码候选及其代表安装。最终 Check、Review、Delivery 和 Completion 由后续原公共结果拥有，此文不预填这些通过。

## 源码与真实 Git

使用 source lock 对应的 Fixed Fork `79a97ed60fe19e8f287eaddfa74722b5250ced35` / `0.7.0-castbox.5`。初始 Reactivate 的 `python -B -m unittest discover -s trellis/skills/guru-team/packages/guru-reactivate-task/tests` 全套 30 项通过，包含真实 Git、公共 reopen 和 matching SDK 正式 schema1 归档恢复；原 rebind 3 项通过。以下当前新路径回归覆盖后续实际差额，未变的 clean-base/rebind 依赖采用原执行事实。

观察覆盖 staged/unstaged/untracked、`.trellis` 工具差额、逻辑 index refresh、文件类型/执行位、HEAD/branch/base/PR/ownership 失配、公共写入后本机失败、同操作输出丢失及无 receipt 的合法后继。旧 public/semantic/transaction 2.0 schema 相对固定 B 无变更。361 个 Guru Python 文件内存编译、wrapper `bash -n`、source package check（40 packages / 125 commands）及 `git diff --check` 通过。

## 当前候选的失败与修复

真实 matching SDK 的最小复现显示：`applyMaintenance` 实际写出后继后，调用方只收到 pending；首次返回 `resume_reactivation`、active 已存在，原输入重试却在调用公共 recovery 之前报 `implementation_state_changed`。这是自身 Task metadata 写入被错误地与完整前态比较，属于 AC3 的正常输出丢失路径。

当前只保存一个 `implementation_state`，由既有 stage 明确范围：`public_prepared` 从原 frozen public plan 推导准确 file-action 路径，完整比较 index、HEAD/branch 及写集外内容，再由原 SDK `previewMaintenance` 校验其精确写集并 recover 同操作；applied/bound 覆为完整 after-state。没有忽略整个 `.trellis`，也不再并存无 consumer 的完整 before 副本和第二个 pending 对象。重复 `implementation_head` 已删除，实现提交身份仍由 `implementation_state.head` 提供。

受影响的新路径套件 `test_existing_implementation.py` 当前 13 项通过（42.474s），含真实 public apply 后 pending 和 stdout 丢失的重试：同 generation、没有再次 prepare/apply、公共 Task 字节保持。另一回归在 pending 期间真实修改业务文件，确认调用 SDK 前即拒绝且现场保持。checkout substrate 27 项通过（14.730s）；最后仅收敛 Reactivate 的单一状态，其 Git facts/C3 消费函数没有改变，采用该原结果。source package check 仍为40 packages / 125 commands，通过。

## 代表安装与实际 AI 恢复

由匹配 Fork CLI `init -y --codex` 生成基础安装，再按 README 的本地 workflow 样本比较并应用当前 canonical workflow，执行完整 `apply.sh --repo <fixture> --python <python3.14>`。默认 Python 3.12 的首次依赖安装返回 `dependency_install_failed`；明确选择已验证的 Python 3.14 后完整安装成功。保留官方生成的空 bootstrap Task 到仓库外，再用 `tests/setup_native_fixture.py --repository <fixture> --directory <external-facts>` 建真实 Git/public 前驱与受控 gh。

当前 AI 完整读取安装后的清晰写作规范和 Reactivate Skill，审核归档 Task 的 source、generation0 Completion/Closure、准确 bookkeeping merge、base、实际实现提交及全部本地差额。安装后的 `scripts/observe.sh` 返回实际实现 HEAD `cec5aecb433ca6b26b1e414e10509e6b4e99f860`，与 base `1ffa49e3d95ca7db370a3f8ae0e8c17a20487807` 分离；受控原 Draft PR 的 repository/base/head 匹配。AI 随后独立形成 semantic result，并调用 installed `scripts/invoke.sh`。

实际返回 `session_binding_recovery_required`、`stable-id` generation1；同输入重试返回同一身份。比较恢复前后 HEAD、全部 refs、逻辑 index entries 和四个业务/工具差额文件，全部一致；generation0 Completion/Closure 保留，新代没有 Delivery 或质量 gate。受控 provider 的调用日志只有 auth/status 和 repository/PR 读取，没有远端写。原 Bind owner 随后核实际后继与资源，返回 `explicit_task_mode`；这不是当前业务 Planning/Check/Review 通过。

该实际 AI 样本使用 Task2 原 reopen 路径，观察发生在上述 formal-pending 修订前。当前修订保留这一原公共入口、完整默认内容比较和业务输出，仅退出重复私有字段；新增分段比较只用于 formal `public_prepared`，其当前行为由13项真实SDK回归覆盖。因此按实际依赖采用该原生样本，不将其改称 formal pending 或真实 GitHub 恢复证据。

同一完整安装再次 reapply 成功，installed package check 通过（40 packages / 125 commands），没有 `.new/.bak`。普通 source-checkout reapply 被历史 schema1 archive 前置校验阻塞；原 `guru-upgrade-tools` 使用独立 tools-only 路径更新投影。当前单值状态候选的真实操作为 `f667bc97-bf86-495a-8242-eb8557c8fbf4`，返回 `tools_upgraded`，recovery_ref=`8924c3e4-c8a5-4f04-9f98-3ef54aa0030b`。新来源使用新操作，没有恢复旧计划。这是 local_candidate 证据，保留 `formal_fork_source_lock` 未验证边界，不宣称正式来源维护通过。

当前 installed check（40 active / 125 commands / 10207 managed）及 `check-dogfood-overlay-drift.sh` 均通过，shared/Claude/Codex/Cursor 与 canonical 匹配，sidecar/conflict为0。2793个 Task/history/session 文件内容和模式保持；212项公共工具 actions、AGENTS、官方模板及307个 peer/common pointer 没有改变。未迁移或隐藏历史归档，也未修改 installer 来消除前置诊断。

## 边界

策略与 trace 仍是 `proposed/docs/test/current/completion-closure.md` 的 T669-01..06。源码/Git fixture、安装和实际 AI 恢复分别证明各自层次。受控 provider 不证明真实 GitHub、backend #802 或业务生产恢复；完整多平台 Release/upgrade 矩阵不在 #669 accepted scope。未对业务仓库、原业务 Issue/PR 或云服务执行写入。
