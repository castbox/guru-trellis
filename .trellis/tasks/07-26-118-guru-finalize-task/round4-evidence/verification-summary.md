# Issue #118 Phase 2 Round 4 验证摘要

## 审查边界

- Role：独立 `trellis-check`，只审查 working tree implementation，不执行 Phase 2
  recorder/checker。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/118-guru-finalize-task`。
- Task：`.trellis/tasks/07-26-118-guru-finalize-task`。
- Base / reviewed HEAD：`7820a9eeec2a2a75fb52fba156a7211d9f9fb09c`。
- Workspace boundary：`status=ok`，expected workspace 与 actual repo root 一致，source
  checkout clean，`suspicious_source_artifacts=[]`。
- Planning approval：`typed_exit=approved`，approval/current HEAD 一致；artifact SHA-256
  `1bcc7712aa1c8a74f72ecfa4a90d8384d77fbd7a6ed95f65714737ffa600c9c6`，facts SHA-256
  `9d0d14bada5d4990a3f62402bdb5b28275fd1c7bf20476cdd01f1145defbeb70`。

## Round 3 finding closure

| Finding | 结果 | Round 4 证据 |
| --- | --- | --- |
| `F-RECOVERY-03` | closed | Generic #117 checker 保持 strict；finalizer augmentation 精确绑定 immutable plan、repo、remote ref、allowlist、evidence commit 与 archive transaction。Recovery probe 的 control 通过，generic HEAD drift 被阻断。 |
| `F-MATERIALIZATION-04` | closed | Persisted `published` gate 只保存 private executor marker；public DTO 仅在 terminal `ready` 后内存物化。Public wrapper 不执行 transition，也不把 DTO 回写 gate。旧漏洞 probe 在 early DTO 路径 fail closed。 |
| `F-LOCATOR-05` | closed | `published.task_ref` 从 validated plan facts 投影 exact archive locator；active locator 不再泄漏到 terminal DTO。 |
| `F-IDENTITY-06` | closed | `verification_required.repo_ref` 必须等于 immutable closeout plan 的 repository identity。 |
| `F-STATE-07` | closed | `resume_finalization` 只允许声明的 post-content recovery states；`prepared` 与 terminal `ready` 均拒绝。 |

历史 `F-DOC-01`、`F-SCHEMA-02`、`F-ROUTE-01`、`F-DTO-02` 均保持 closed，无回归。

## 验证矩阵

| 检查 | 结果 |
| --- | --- |
| Round 3 recovery probe | exit 0；control passed；generic HEAD drift blocked |
| Round 3 published/materialization/locator probe | exit 1；在 early public DTO 路径由 exact private marker check 阻断，符合修复后预期 |
| Focused runtime regressions | 12 passed |
| Focused package regressions | 2 passed；首次 selector class 拼写错误造成 loader error，更正 selector 后通过，不是产品失败 |
| Runtime full | 611 passed，13 skipped |
| Skill package full | 178 passed |
| Preset full | 45 passed |
| Finalizer package | 4 passed |
| Installed shared production eval | 8/8 passed |
| Source/installed package validation | 13 active / 0 planned / 0 legacy；global markers 12 invokes / 46 exits / 27 targets |
| Contract discovery | 6 profiles / 6 exits / 2 private artifacts |
| Eval discovery | 8 cases / 4 adapters |
| Ownership | 43 frozen / 43 active / 0 removed |
| Static/hygiene | Bash syntax、Python compile、`git diff --check`、task validate、executable scan、no-deploy-impact assertions 均通过 |
| Byte identity | canonical/installed shared/Agents/Codex/Claude/Cursor package、runtime、adapter、consumer schemas 一致 |
| Fresh clean throwaway | exit 0；覆盖 marketplace discovery、initial install/reapply、`trellis update`、managed hash、`.new/.bak` recovery、developer/no-developer fixtures、all-platform distribution、wrapper/package/eval/closeout recovery |

Preset apply 曾以默认平台集运行并暂时移除 managed Claude copies。检查代理立即使用
`--all-platforms` 恢复并重复幂等 apply；最终三平台、2644 managed files、0 removal、0
conflict、0 sidecar，working diff 恢复到进入检查时的 39 files / 12760 insertions / 4791
deletions。由 validator 生成的两个精确 Python cache roots 已清理；最终 repo 内 `.pyc`、
`__pycache__`、`.new`、`.bak` 均为 zero-hit。

## Docs SSOT reconciliation

- Strategy：`ssot_first`。
- Step-local contract 与 durable workflow specs 均记录 finalizer-only #117 augmentation、private
  marker、terminal DTO materialization、exact archive locator、plan repo binding 与 legal resume
  states。
- README 维持 13/52 package/exit inventory 与 12/46/27 global marker counts；#119 仍拥有
  Finish-family global activation，#132 仍拥有 upstream overlay cleanup。
- Durable docs、task delta、runtime、schemas 与 tests 一致；无需新增 README 或 global workflow
  delta。

## 结论

Issue #118 current scope 的 implementation、tests、distribution、upgrade/update、Docs SSOT 与
task artifacts 已完整覆盖。Round 3 五项 finding 已关闭，历史四项无回归，没有 open P0-P3
finding。该证据足以支撑主会话生成 current `phase2-check.json`；本检查代理未运行 recorder
或 checker。
