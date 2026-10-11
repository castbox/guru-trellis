# Guru #521：实施与验证计划

## 顺序与写入范围
本节记录初始规划顺序：初始实施前只写当前 Task 规划文件与适用 JSONL context，规划通过 Wording、独立 Architecture、Planning Approval 并由用户接受后进入正式 activation。当前 Task 已为 in_progress；文末技术修订沿原规划门禁重入，不重新 activation。

1. 重读 live #521、current RDT/Architecture、源/安装 inventory、canonical mode/execution/workflow 与真实 binding/resolver/Task acquisition consumers。先完成 planning_scenario_set 的 normal、solution 和新保护机制 root qualification；未通过的机制回原 Planning remove/replace，不制造 scope 问题或新生命周期。
2. 修改 canonical selector、task-free execution SKILL/reference 及 workflow caller/no_task/re-entry；覆盖 first-write、复用/创建、只读、实际 binding、new-chat、no_current_task、partial evolution 与独立副作用边界。Task-free 不调用正式 Task APIs。
3. 在正式 Task creation acquisition 的最小边界限制 primary adoption；中立事实由现有 Git APIs 提供。保留 recover/base Sync/cleanup 自身责任及 supported 在途迁移边界，不全局放宽 clean 校验。阅读实际变化后决定是否需要最小 runtime/schema 修改；新增 consumer 字段或路径须回 Planning 审查。
4. 建立任务独有 RDT contribution 与 traceability。按独立 Architecture 结果维护 task contribution/必要 ADR；不直接修改 shared current authority。
5. 按正式 preset apply 更新 dogfood 和平台投影，检查 .new/.bak 逐个 disposition 与 upstream-owned 字节。不得修改 start/continue、extractor、hooks 来满足验收。
6. 完成定向客观验证和真实 native Agent 接续轨迹，保留 raw fixture/evidence 在当前已有 runtime/eval 位置，长期 contribution 只保留必要结果与未验证边界。
7. fresh Phase2 Architecture/Check、正式 Task Commit、独立 committed full-range Architecture/Branch Review；需要知识晋升时由 SSOT owner serialized promotion 后重新完整门禁。commit/push/PR/merge/install/release/cleanup 各自独立范围。

## 定向验收矩阵
| 测试 | 输入与触发 | 必须观测 |
| --- | --- | --- |
| T521-01/02 | 干净 primary、无合适 linked、合适 linked、只读、位置/授权缺失 | 首次修改只在 linked 非 base；Task 和 task-free 分离；只读零资源；缺失停止依赖写入 |
| T521-03 | 无 Task linked 中 start、普通继续、新聊天恢复、明确 continue | 无 Task 副作用，真实 upstream no_current_task -> Guru caller -> 合法轻量 owner；不能消费时单列依赖未验证 |
| T521-04 | common-dir 中其他聊天 Task、当前同/异范围 binding、stale/conflict | 不按 inventory 猜 Task；有效 Task 回原 owner；冲突拒绝；零静默覆盖 |
| T521-05 | primary/linked 无关 dirty/untracked、多 worktree、“修复”“提交 push” | 来源与无关内容完整；primary ref 不变；发布范围与实际获准候选一致 |
| T521-06 | 自动与显式 task-free 部分编辑后扩张 | 立即停止剩余目标写入；各走原 owner；收窄/standard 的承接精确且独立；无空 Task、无 primary fallback、无重复搬运 |
| T521-07 | 一个代表性 clean install、current update/reapply | 固定 source/core identity；upstream-owned 字节相同；平台投影一致；sidecar 真实处理 |
| T521-08 | 旧 current-checkout 安装与正式 Task/base Sync | 明确迁移支持/拒绝；Task creation linked 默认，原独立 owner 不被 Task-free 接管 |

新增测试必须验证正常错误与外部状态变化，不引入恶意伪造、TOCTOU/stress/fault-injection。Python pass、DTO pass、静态字符串和 source fixture 都不能替代上述真实 Agent 接续轨迹。

## 命令与 evidence
命令按实际改动确定：受影响 package runtime tests、workflow/consumer validators、Task lifecycle targeted tests、preset apply、dogfood drift/upstream projection checks，以及现有 native eval harness 和一个代表性安装。缺 jsonschema、模型/CLI、provider、真实新聊天执行能力或适用凭证时报告 SKIP/blocked 与精确 owner，不能制造 pass。
不重跑完整多平台 Release matrix 来证明普通局部变更；软件发布与业务 #120 安装回归分别由实际 owner 承接。本计划不自动执行业务仓安装、同步 main、关闭 Issue 或清理资源。

## 无 Issue 标准接管的最小输入兼容修订

当前 native T521-06 已重现原 Review 的 standalone_request/workflow 输入不兼容。先按现有 qualification、Planning wording/Architecture/approval 与 implementation-discovery Architecture owners 复核上述设计修订，TaskId/generation 与 accepted R521-07 不变，不重新创建或激活 Task。

实施范围仅为 canonical guru-review-change-request 的 standalone-request mode schema、最近合同及必要的现有 package/production producer-chain 回归；proposed_draft 和其余 source/consumer contracts 保持。实际 projection 由 preset apply 同步。必需验证为旧 standalone、workflow/no_issue 的实际生产 owner链和普通 mode mismatch拒绝；source/installed closure、affected projection parity与实际同聊天 native 重入按变化依赖执行，不重跑无关完整矩阵。

native 必须保留原 source/transition 与首次失败，完整 Review 成功后由原 create/acquisition owner 选择 clean linked位置、展示精确Task与Git计划，并另列partial carryover来源、目标、差额与独立动作；此轮不执行新Task/资源创建、绑定或承接。补齐真实证据后 fresh Phase2 Architecture/Check。仍缺原owner前置时准确blocked，不预填PASS。
