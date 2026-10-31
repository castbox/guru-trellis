# #692 实际验证结果

观察截止：同 Task/D1 首次完整实施候选；代码、原 wrapper 和本 checkout 工具更新/reapply 已实际检查，candidate Check 与后续正式质量链尚待各原 owner 执行。固定 B 为 `6a65ec8afe6d180850760b3b2edf3f94be6e3b20`。本文是本项实际结果唯一 Test 落点；策略见 [T692/SC692](proposed/docs/test/current/local-fix-intake.md)。计数只说明本次命令结果，不替代语义覆盖。

## 代码与原公开链

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-discover-change-context/tests -p 'test_runtime.py'` 首次缺少 `GURU_UPSTREAM_DELIVERY_SCRIPTS`，记环境阻塞。显式提供已核对的匹配 Fork `.6` 源码 scripts 后，整套 10 项中 9 通过、1 项继承失败，不能报告整套通过。
- 通过的原 package-copy installed wrapper 回归实际执行 record→check→invoke，覆盖 workflow/standalone 正常配对及 genuine recorder 结果误配、中文逐块错误解码/完整解码对照、可见历史 summary 正常变化、base 前进/dirty/错误 branch、context_request 目标失配与 record authoring 字段。核对原失败/refresh classification、code/status、stdout DTO及直接错误形状；check diagnostic 与 invoke stderr 三字段一致，不回显正文/值。绑定失配没有被当成 UTF-8 根因。该层是原测试中的 package-copy wrapper，不是外部完整安装或 Agent 行为效果证明。
- 继承失败为 `test_active_task_uses_current_checkout_binding_without_legacy_branch`：错误 branch binding 断言预期 field `worktree`，当前 schema-2 resolver 先返回 `task_id`。从固定 B 的 Git 对象读取原测试方法，在相同完整 Fork `.6` scripts 环境对 B/current 两份方法均复现同失败；`common.active_task` 与 Task resolver 本批未改。未修历史 resolver、未改旧断言、未把此项计为通过。其归因不替代正式 Check 对本批适用性的判断。
- Discovery `test_contract.py` 8 项通过。Selector、Create Issue、Author 原 contract suites 分别 12、16、2 项通过。Selector 初次缺 `PYTHONPATH`，指定 `trellis/skills/guru-team` 后通过。
- Clarify contract 首次 17 项通过、1 项 fixture 依赖受阻。其 `installed_fixture` 实际消费 `GURU_UPSTREAM_DELIVERY_SCRIPTS`；本 checkout 的 `.trellis/scripts` 不具备该 fixture 所需完整 Fork package 布局。使用现有、只读的 Fork Git `07f31d83543581647ef7852d177c3dd16587049a` / CLI-Core `0.7.0-castbox.6` 的 `packages/cli/src/templates/trellis/scripts`，以相同 `PYTHONPATH`、`PYTHONDONTWRITEBYTECODE=1` 定向重跑 `test_contract.py -k active_scope_ready_and_historical_success_requires_fresh_producer`，1 项通过；其余已绿项未重复。未新增安装或修改 fixture。

## 实际工具采用与分发

- 首次 `trellis/presets/guru-team/scripts/bash/apply.sh --repo .` 被 `upstream_delivery_migration_required` 拒绝，exit 1；旧归档 preflight 尚需其独立迁移 owner。没有绕过普通 preflight、转换历史数据或手改 provenance。普通 apply 不能记为成功。
- 原 `guru-upgrade-tools` 从当前完整 dirty canonical source 执行 `local_candidate` tools-only install，仅选择本 Task checkout；使用上述已有匹配 Fork build。原 preview 未发现未知 Guru local edit，冻结 public tools 计划只同步 canonical `.trellis/workflow.md`，其余 upstream templates 内容一致；保留已有 Guru `claude/codex/cursor` 选择、用户 config/AGENTS 和 Task/session/history。
- 只读 preview 初次输出超过进程捕获上限；完整捕获后正确读取。prepare 初次误将上游 `claude-code` 标识用于 Guru selection，被拒绝；按实际 manifest 的 `claude` 修正后冻结原计划。约 5 MB 的 frozen plan 以 inline argv 启动时触发 `E2BIG`，进程未启动；改为原入口支持的普通文件后执行。以上为调用/承载恢复，未弱化任何 schema 或 gate。
- 实际原 public invoke 返回 `tools_upgraded`、installed version `0.7.0-guru.7`、`unverified=[formal_fork_source_lock]`。原 owner 使用 checkout-local Python pointer，验证实际 target native entry 与 peer/common pointers 保持；这是本地 development candidate 证据，不是正式锁定 source 或 Release。
- 在同一次工具维护的原 public maintenance proof 下，原 installer `install_assets(... tools_only=True, checkout_local=True, tools_maintenance=...)` 实际 reapply；目标自己的 resolver 执行，package/overlay 均 `ok`，installed validation returncode 0，native `passed`，peer/common pointers `preserved`。没有手改 manifest/hash、调用全量数据迁移或额外 clean installation。
- 原 source package validator 通过；实际 installed validator 已在 install/reapply 中执行通过。`check-dogfood-overlay-drift.sh --repo .` 通过，确认 Shared/Claude/Codex/Cursor 选定投影 bytes/mode、workflow 与 spec 对齐 canonical。`check-upstream-ownership.sh --repo . --json` 通过。受管根递归 `.new/.bak` 为零。
- 此次匹配更新同时投影固定 B 已合入的 #706 合同/技能；那部分能力是继承基线，不计为 #692 新实现。全部最终实际 diff 仍须由原质量 owner 审核。

## 基础检查与文档

原质量规范的 in-memory syntax 命令检查 Guru runtime/packages 与 preset installer，367 个 Python 文件通过；最终 Discovery 改动再核语法通过。`python3 -m json.tool trellis/index.json`、声明 Bash wrappers 的 `bash -n`、`git diff --check` 通过。隔离 proposed 相对文件链接按最终路径与未改仓库文件解析通过。原 `task.py validate` 的 manifests 通过，超注入上限规范保留 warning，并由各 Agent 实际完整补读；不以注入存在推断完整读取。

原 RDT impact 实际返回 `candidate_ready`，只证明完整隔离 proposal 可交候选 Check；共享 current 尚未在该观察点写入。原 independent Architecture、candidate Check、final_integration/readback、实际 after 重绑及最终质量结果，均由原公开结果与后续 Git/PR facts 承接；本文不循环记录自身最终 pass 或最终 HEAD。

## 未验证边界

未取得业务案例当时完整安装快照或原完整会话；当时实际选路、运行时根因和净节省时间未知。业务代码/测试/数据/Task/会话只读；外部安装采用、实际多平台 Agent 行为与完整升级/Release 矩阵未验证。不增加专项 replay、A/B、native eval、固定案例数、耗时测量或额外 clean installation。局部测试、知识晋升及 Delivery 合并均不替代整体 Completion/Closure/Finish。
