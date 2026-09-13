# Implementation Plan

## Ordered Work

1. 从实施开始时的 fresh `origin/main` 重新生成 ledger 名称、schema id、DTO 字段和 Issue-array
   aggregate 的 writer/reader/registration/consumer inventory；按 active canonical、managed
   projection、current docs、immutable history 四类标记，禁止机械删除历史证据。
2. 修改 `guru-create-task-workspace` canonical package：移除 ledger authoring、schema、plan/result
   字段、executor writer、checker reader、examples/evals/tests 与 interface/manifest registration。
3. 修改 Clarification/Readiness、Planning、normal-scenario/solution-mechanism qualification、Phase 2、
   Task Commit 与 Branch Review active contracts，删除 ledger path/precondition、`primary_issue` 和
   aggregate DTO；由 owner直接读取 current requirement/planning/source authority。
4. 修改 Publication、Finalizer 与 Merge：删除 ledger loader/validator/hash/recovery/closeout projection；
   Publication 成为唯一关闭意图判断 owner，按 Issue-backed completed 默认关闭、明确 remain-open
   例外和 no-Issue 形成 PR payload；Finalizer 只绑定发布事务，Merge 只做 readiness、expected-head、
   confirmation 与 live result verification。正常、existing-PR、terminal recovery 和 phase2-reentry
   均使用同一 current owner-native 数据流。
5. 修改 Finish、Restore、Cleanup、release verifier 与 installed closeout fixture，删除 ledger reader
   和 ledger 决策；只保留 current task/archive/Git/provider facts。删除旧 task continuation、转换和
   compatibility fixture，不新增 ledger migration verifier。
6. 删除所有只服务 ledger 的 current Skill Markdown、interface/consumer schema、eval/example JSON、
   DTO、runtime/script、fixture/test、commands、manifest/registry 内容。对共享文件逐 consumer 审查，
   只删除 ledger-owned 分支，避免破坏其它 active responsibility。
7. 创建 `docs/requirements-design-test-contributions/247-remove-issue-scope-ledger/`，提供 manifest、
   requirement、design、test 和 traceability；创建 task-owned Architecture contribution，记录
   dedicated refactor slice、before/after、project check、legacy preservation 与 promotion contract。
8. 更新 canonical workflow/README/spec/extension manifest/preset ownership 与 verifier；运行 preset
   apply 同步 dogfood 及 Shared/Codex/Claude/Cursor 投影，逐项处理 `.new`/`.bak`，不得覆盖用户改动。
9. 添加/调整 targeted tests 与 eval：active-zero inventory、task creation no-ledger、Publication
   completed/remain-open/no-Issue 判断、默认/非默认分支 closing-keyword 路径、Finalizer/Merge 不重判
   或手动关闭、owner re-entry、absent/present-A/present-B 对 current runtime 无影响、installed
   update/reapply、recursive sidecar、mixed package fail-closed。
10. 执行 Phase 2 RDT/Architecture sync、完整 task check、task commit 和独立 committed full-diff
    Branch Review；任何新发现的 owner/scope/architecture expansion 先回对应 semantic owner。

## Required Validation

```bash
python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-create-task-workspace/tests -p 'test_*.py'
python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-create-task-commit/tests -p 'test_*.py'
python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-review-branch/tests -p 'test_*.py'
python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-review-task-publication/tests -p 'test_*.py'
python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-finalize-task/tests -p 'test_*.py'
python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-merge-task-pr/tests -p 'test_*.py'
python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-restore-archived-task/tests -p 'test_*.py'
python3 -m unittest discover -s trellis/skills/guru-team/tests -p 'test_*.py'
python3 trellis/presets/guru-team/scripts/python/test_workspace_invocation_integration.py
python3 trellis/presets/guru-team/scripts/python/verify_installed_task_workspace.py --help
python3 trellis/presets/guru-team/scripts/python/verify_installed_closeout.py --help
find trellis/skills/guru-team/runtime trellis/skills/guru-team/packages -name '*.py' -type f -print0 | xargs -0 python3 -m py_compile
python3 -m py_compile trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
python3 ./.trellis/scripts/task.py validate .trellis/tasks/09-13-247-remove-issue-scope-ledger
git diff --check
```

具体 package wrapper、eval runner、source/installed validator 和代表性 clean/existing install/update
命令在实现 inventory 后使用当前 README/interface 的真实入口补全；不得凭旧命令名假设。

## Test Matrix

| Scenario | Expected result |
| --- | --- |
| fresh Issue-backed completed, default branch | Publication 默认判定关闭并在 PR body 写入 closing keyword；GitHub merge 后自动关闭；Merge 只验证 live facts |
| fresh Issue-backed remain-open | Publication 基于 live Issue 中明确的合并后验证、观测、发布或未完整交付条件，仅引用并记录原因 |
| fresh Issue-backed completed, non-default branch | 当前 PR 只引用且不宣称关闭；后续目标默认分支 Publication fresh 判断并写入 closing keyword |
| fresh no-Issue task | PR/commit 不制造 Issue reference 或关闭 effect |
| legacy ledger absent | lifecycle 使用 current authority 正常运行 |
| legacy ledger present-A / present-B | 不影响 current runtime；preset/update 不主动触碰且无 open/read |
| insufficient current intent | current lifecycle 返回既有 semantic owner，不读取 legacy；不作为旧 task continuation |
| existing PR / terminal recovery | 使用 live PR/Git/current reviewed payload，不重复副作用 |
| canonical/installed/platform package | interface/schema/runtime/examples/evals bytes/mode 一致，无 ledger sidecar |
| update/reapply | 不创建 ledger，不登记 ledger，保留已有 legacy 文件 |
| active graph inventory | writer/reader/precondition/schema registration/consumer 计数均为零 |

## Review Focus

- 确认删除的是 ledger-owned aggregate，不误删 Publication 唯一拥有的 current closure decision；
  Finalizer/Merge 不获得替代判断权。
- 确认没有新增 legacy migration/preservation 专用 reader；preset/update 通过 ownership 边界不主动
  触碰文件，而不是打开文件后再决定保留。
- 检查正常、existing-PR、terminal 和 re-entry 全部 producer path，避免只修 happy-path。
- 检查 Skill Markdown、schemas、examples、evals、DTO、scripts、tests、manifest/registry 和安装投影，
  不接受 dead file、nullable 壳或未注册但仍可达的隐藏路径。
- 检查 touched non-generated code file 的 3000 行阈值与净增长来源。

## Deferred Verification

完整多平台 exact-candidate Release matrix、tag、GitHub Release、生产业务仓验证不属于 #247。
本任务必须完成 touched package 的 canonical/dogfood/installed/declared-platform parity，以及一个
代表性 clean 或 existing install/update 场景；其余明确记录为 deferred，不得声称 Release Gate 已通过。
