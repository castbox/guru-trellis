# Implementation Plan

## Current Contract

唯一 current authority 为 live Issue #247 `2026-09-13-r24`。本计划在现有 7 个提交之上增量修正，
只交付 ledger-free 的旧流程兼容版本；不实现 Refs-only、no-archive、active-task multi-Delivery、
future Completion owner、migration stop 或 #305 全局重构。

## Ordered Work

1. 从 fresh `origin/main`、完整 `origin/main...HEAD`、current working diff、official inventory、workspace
   mapping 与 ignored runtime 重新生成 ledger writer/reader/registration/consumer inventory。除当前 #247
   task 外，如存在依赖 ledger 继续执行的 active task 或无法归属的 in-flight ledger-bound invocation，
   停止并报告，不恢复兼容 reader。
2. 保留现有 7 个提交中已完成的 ledger 删除：Workspace 不再 author/write/register ledger；Clarification、
   Planning、qualification、Phase 2、Commit、Branch Review 不再消费 ledger path、`primary_issue` 或 Issue
   classification arrays；ledger-only schema/example/eval/DTO/runtime/script/test/registration 退出 active graph。
3. Publication 只删除 ledger 输入，保留 current Issue-backed completed closing keyword、reference-only
   empty close set、no-Issue 与 non-default-base 语义，并继续由 semantic gate fresh 形成本次 reviewed PR
   payload 和 expected close set。
4. Finalizer 只删除 ledger loader/binding，保留 local preparation、push、PR create/update、official archive、
   Ready、handoff、existing-PR、lost-result、reprepare 和 terminal recovery；`ready_for_merge` 继续携带 archive
   locator 与 exact reviewed body SHA-256。不得借 #247 改写 Finalizer public owner 或 exit semantics。
5. Merge 保留独立 semantic review、expected-head、merge confirmation、post-merge closure verification 与
   `merged`、`closure_mismatch`、`merge_blocked`、`phase2_reentry_required` 四个 exits；task-content finding
   继续通过 archived identity 路由到 `guru-restore-archived-task`。
6. Finish、Restore、Cleanup 与 release verifier 只删除 ledger reader/fixture，保留既有 task/archive/Git/
   provider owner facts、current terminal 与恢复路径。legacy ledger 作为 inert data 原字节保留，preset/
   update 不拥有、不打开、不迁移或删除它；不执行旧 task backfill。
7. 修订 task planning、#247 RDT contribution、Architecture contribution、accepted ADR 与唯一 active `.50`，
   全部绑定 r24，并使用 `dedicated_refactor_slice` 表达旧行为/API/graph 保持。明确披露提前归档、PR 冲突
   和同一 task 多 PR 接续局限仍由后续 Issue 处理。
8. 在 canonical manifest 声明 `guru-ledger-free-runtime@1.0.0`，由 preset 原样投影到 installed manifest；
   apply、installed runtime 与 compatibility matrix 严格校验 capability id/version 和 current extension/
   workflow projection identity，不写 source commit、tree state、selected platforms 或 manifest digest。
9. 同步 canonical、dogfood、installed、Shared/Codex/Claude/Cursor、workflow README/spec 与 preset 投影；
   使用 `apply.sh --repo . --all-platforms` reapply，逐项处理 `.new`/`.bak`，不覆盖无关用户修改。
10. 补齐 active-zero、legacy absent/present-A/present-B 等价、三类 Publication effect、Finalizer archive/
    Ready/recovery、Merge 四 exits、archived Restore、capability shape/parity，以及真实 production wrappers
    串联旧流程到 current terminal 的代表性 installed Git fixture。
11. 执行 fresh Phase 2 RDT/Architecture sync 与完整 task check；准备 corrective commit 的精确 stage 范围
    并等待单独授权。commit 后才执行覆盖完整 `origin/main...HEAD` 的独立 Branch Review。

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
python3 -m unittest trellis.presets.guru-team.scripts.python.test_apply_guru_team_trellis_preset
python3 -m unittest trellis.presets.guru-team.scripts.python.test_verify_trellis_upgrade_contract
python3 -m unittest trellis.skills.guru-team.runtime.tests.test_runtime
find trellis/skills/guru-team/runtime trellis/skills/guru-team/packages -name '*.py' -type f -print0 | xargs -0 python3 -m py_compile
python3 -m json.tool trellis/guru-team-extension.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
python3 ./.trellis/scripts/task.py validate .trellis/tasks/09-13-247-remove-issue-scope-ledger
git diff --check
```

具体 package wrapper、eval runner、source/installed validator 和代表性 installed old-flow fixture 使用
current README/interface 的真实入口，不手写中间 success DTO，也不调用后续 lifecycle owner。

## Test Matrix

| Scenario | Expected result |
| --- | --- |
| Issue-backed completed, default branch | Publication 写 closing keyword；Finalizer archive/Ready；Merge 验证 GitHub 自动关闭效果 |
| Issue-backed reference-only | reviewed close set 为空，PR 只引用，Merge 接受 empty expected close set |
| no-Issue | PR/commit 不制造 Issue identity、引用或关闭 effect |
| completed, non-default branch | 当前 PR 只引用；后续目标默认分支 Publication fresh 判断 |
| legacy ledger absent/present-A/present-B | current lifecycle 结果一致；runtime/preset/update 不打开或触碰 ledger |
| Finalizer recovery | archive-month、post-archive Ready、existing-PR、lost-result、reprepare 保持旧合同 |
| merge task-content finding | `phase2_reentry_required` 携带 archived identity，Restore 回到 Phase 2 |
| PR body edited after Finalizer | Merge 在 mutation 前发现 `publication_body_sha256` mismatch 并 fail closed |
| installed real-wrapper old-flow chain | 从无 task/无 ledger 起步，经真实 wrappers 到 current terminal |
| canonical/installed/platform | capability、interface/schema/runtime/examples/evals bytes/mode 一致，无 sidecar |
| active graph inventory | writer/reader/precondition/schema registration/aggregate consumer 均为零，23/97/78 graph 不变 |

## Review Focus

- ledger 删除不能误删 Publication closing、Finalizer archive/Ready、Merge closure verification 或 Restore。
- 修改前后 producer consumer kind/id、target/stop、行为时点与 23 Skills / 97 exits / 78 commands 一致。
- 没有 ledger alias、adapter、dual-read/write、隐藏 aggregate、通用 migration owner 或未来 lifecycle package。
- capability 仅证明 ledger-free runtime，不宣称新 Task lifecycle、多 Delivery 或 Release 已完成。
- 历史 archive、ADR、superseded/released RDT 保持 immutable；只修订 current `.50` 与 #247 contribution。

## Deferred Verification

完整多平台 exact-candidate Release matrix、tag、GitHub Release、生产业务仓验证不属于 #247。本任务只需
完成相关旧流程 E2E、canonical/dogfood/installed/declared-platform parity 和一个代表性 focused install/
update 场景，不得声称 Release Gate 已通过。

## Planning Re-entry And Remaining Gates

live Issue #247 `2026-09-13-r24` 替换 r19-r22。旧结论中关于 Refs-only、Finalizer 不归档、Merge 后 task
保持 active、多 Delivery 与 conservative consumer 的内容全部失效。r24 要求保留旧流程，因此 path 修订为
`dedicated_refactor_slice`；先前以 `target_native` 为前提的 Phase 2、qualification 与 Branch Review 结论 stale。

Serialized promotion 已建立 `.50` RDT/Architecture successor 与 accepted `ADR-009`；本次只更新 current
`.50` 和 #247 contribution，不改变 immutable `.49`。修订后须 fresh Phase 2、单独授权 Task Commit 与
independent full-diff Branch Review。Publication、push、PR、merge、tag、Release、Issue closure、Finish/archive
当前 task 与 Cleanup 均未授权。
