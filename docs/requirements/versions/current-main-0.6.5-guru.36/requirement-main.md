# Guru Team Trellis Extension 当前需求

版本：`current-main-0.6.5-guru.36`；状态：`superseded`；基线：main `c2b1784654a95b999bbff71daf1393c22aa01048` + #275 committed task-branch delta。

## 目标、角色与适用范围

- `REQ-001`：为采用 Trellis 的仓库提供 AI-first、Issue/task 可追踪、可审查且可恢复的完整开发生命周期。维护者、任务执行 Agent、reviewer 和发布操作者是主要角色。`source_confirmed`：Issue #266；`code_recovered`：workflow/registry。
- `REQ-002`：官方 Trellis workflow/spec marketplace 是上游扩展面；Guru Team 通过 Markdown workflow、step-local Skill、preset/overlay 与 companion runtime 扩展，不修改上游源码、全局 npm 或 `node_modules`。`source_confirmed`：仓库 AGENTS.md；`code_recovered`：canonical layout。
- `REQ-003`：全局 workflow 只拥有 phase 顺序、mandatory invocation、typed exit consumer 和 fail-closed stop；每个 Skill 独占内部 closed loop。`code_recovered`：`trellis/workflows/guru-team/workflow.md` 与 21 个 active interfaces。
- `REQ-004`：AI 负责 scope、充分性、finding、route 与发布判断；Python/shell 仅执行或校验确定性事实。只有真实选择或副作用才交互，授权不持久化。`source_confirmed`：仓库合同。
- `REQ-005`：Task、workspace、branch、history、archive、semantic naming 与 base/provider recovery 必须保持明确 ownership，且普通 mapped exit/recovery 不制造人类 handoff 文书。`code_recovered`：相关 active Skills。
- `REQ-006`：canonical、installed dogfood、Shared/Codex/Claude/Cursor 投影和 preset managed assets 必须保持同一 versioned contract；未知修改遵守 `.new/.bak` 语义。`code_recovered`：manifest、overlay、installer。
- `REQ-007`：Requirements/Design/Test 与 Architecture Baseline 是 repository authority；task 变更先做 impact/contribution，再 promotion，普通并行 task 不直接竞争 shared current 文件。`source_confirmed`：#263/#264/#265；`code_recovered`：三项 package。
- `REQ-008`：公共 Skill id、exit id、schema id、workflow id、preset path 与 command 是兼容 API，不能无迁移静默破坏。`source_confirmed`：仓库合同。
- `REQ-009`：安装、升级、release 结论必须由其责任 Issue 的 exact evidence 支持，skipped/static/package 证据不能冒充外部或 release proof。`source_confirmed`：Validation Scope Ownership。
- `REQ-010`：只处理 honest-but-fallible 正常路径；恶意伪造、对抗输入、未要求的锁/TOCTOU/竞态加固不属于当前产品范围。`source_confirmed`：仓库 AGENTS.md。
- `REQ-011`：task index/history query 必须能从 current task、archive 与 `finish-summary.json`
  找到任务最终结果；archive、acceptance、Finish 与 cleanup 只处理 exact task/resource，不覆盖
  其它并行任务。`code_recovered`：task scripts、Finalizer、Merge 与 finish contracts。
- `REQ-012`：task/branch/worktree 使用绑定 Issue 与语义动作的名称；base evolution、GitHub provider
  failure 与 partial recovery 返回唯一 owning route，不从 Phase 0 重建已存在的 task。
  `code_recovered`：workspace、reconcile、publication/finalization packages。
- `REQ-013`：install/update/upgrade/reapply 必须保留完整 capability inventory、managed path、
  executable mode 与声明平台入口；未处理 `.new/.bak`、版本或 projection drift 必须阻塞成功声明。
  `source_confirmed`：preset/upgrade contracts；`code_recovered`：installer 与 validators。
- `REQ-014`：Finalizer 完成 archive、Ready PR 与 terminal cleanup 后，public wrapper 只可从已归档 durable summary、精确 retired owner locator 与当前 Git/GitHub ready facts 重建 terminal authority；缺 locator、archive/head/PR/scope 漂移或未退休 owner state 必须 fail closed。`source_confirmed`：Issue #275；`code_recovered`：Finalizer owner/runtime。
- `REQ-015`：Throwaway verifier 的 active package、command 与 complete-package inventory 必须从 canonical registry/interface validation 派生；不得维护随新增 Skill 漂移的固定数量。`source_confirmed`：Issue #275；`code_recovered`：verifier inventory projection。

## 生命周期行为

| Behavior | 必需行为 | 当前 owner |
| --- | --- | --- |
| `BEH-001` Intake | mode selection 后，标准路径依序完成 base sync、context、clarification、wording、readiness、workspace | global workflow + Phase 0 Skills |
| `BEH-002` Planning | 三份 task planning、semantic approval 与一次 current plan review pause | `guru-approve-task-plan` |
| `BEH-003` Execute | worktree boundary、approved scope implementation、完整 Phase 2 semantic check | `guru-check-task` |
| `BEH-004` Review | exact commit、完整 branch range review、finding closure 与 fresh final review | commit/review Skills |
| `BEH-005` Publish | PR readiness、deterministic finalization、expected-head merge、Issue closure verification | publication/finalize/merge Skills |
| `BEH-006` Recovery | base evolution、provider recovery、stale/re-entry 保留唯一 mapped consumer，fail closed | reconcile 与 owning Skill |
| `BEH-007` SSOT | RDT、Architecture、Bootstrap 维护 version/status/freshness 与最小投影 | #263/#264/#265 packages |
| `BEH-008` History/Finish | acceptance 后产生唯一 archive/finish result，index/history 可查询并保护 exact retained refs | Finalizer/Merge/task history owners |
| `BEH-009` Distribution | marketplace install、official update/upgrade、workflow selection、preset reapply、sidecar/drift validation 按序执行 | marketplace/preset/verification owners |
| `BEH-010` Terminal projection | Finalizer terminal cleanup 后从 archive/live ready authority 投影 `ready_for_merge`，真实 stale 继续拒绝 | `guru-finalize-task` |

## 当前发布范围

`source_confirmed`：最新已发布 stable release 是 `v0.6.5-guru.9`，tag commit `56b5f411e533b200e4d8685ca7a2ffb0c778a7f5`；#275 replacement candidate 是 `v0.6.5-guru.10` / manifest `0.6.5-guru.36`，target/tested Trellis CLI 为 `0.6.5`。candidate 在 exact gate、合并、annotated tag、tag-pinned smoke 与 GitHub Release 完成前不得称已发布。

## 非目标

本 authority 不把未来 Trellis `0.6.15` 或 #260/#267 的完整多平台矩阵写成 CURRENT；不定义业务仓库私有 PRD；不把 task archive、PR body 或旧测试摘要当成 current intent。
