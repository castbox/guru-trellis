# #530 设计职责

状态：promoted / current-main-0.6.17-guru.89。架构由[任务 contribution](../../architecture/contributions/530-clean-committed-reentry.md)拥有。Step-local SSOT 为 canonical TaskCommit contract，workflow 只编排。

| Design responsibility / contract | 唯一职责与直接 consumer |
| --- | --- |
| D530-01 / CON530-ENTRY | 原 TaskCommit public invoke 增加闭合且互斥的 `committed_reentry` 输入能力；原 dirty prepare/executor 和非空 exact_stage_paths 保留。 |
| D530-02 / CON530-CHECK | 原 Check checker 校验 reviewed content/capture；TaskCommit 核验其当前 receipt、adjacent anchor、HEAD、Task checkout、selected base 和 committed range。不复制内容算法。 |
| D530-03 / CON530-PROJECT | 核验成功后输出原 `task_ref/base_ref/branch_review_commit`。显式薄投影进入原 pair guard 和 Branch Review input；后者不读 Check 或 TaskCommit 私有状态。 |
| D530-04 / CON530-RECOVER | 新 base 返回 Reconcile/fresh Phase 2；dirty 返回原 exact commit；正常 stale 和 active Git operation 由原恢复 owner 处理。 |
| D530-05 / CON530-REVIEW | 接续只确立当前候选身份。fresh Architecture 和独立完整 Branch Review 仍由各原 owner 判断；不把 Check pass 当 Review pass。 |
| D530-06 / CON530-INSTALL | 使用现有 preset 安装和受管哈希更新，canonical/installed/shared/Codex/Claude/Cursor 与 managed spec 同步；不 patch upstream 或本机全局包。 |

无新 Skill、typed exit、state store 或长期 gate artifact。新增输入 profile 是兼容增加；旧输入语义不变，旧安装采用完整匹配 preset 后才调用新能力。
