# 实现计划与 Docs SSOT Plan

## Ordered Checklist

1. 读取并锁定当前 `.trellis/spec/preset/installer.md`、`upstream-ownership.md`、`overlay-guidelines.md`、`.trellis/spec/workflow/{workflow-contract,companion-scripts,data-contracts,quality-guidelines}.md`；确认 canonical/installed ownership 和测试入口。
2. 在 canonical Guru runtime/preset source 新增 inventory schema、controlled-root resolver、run handle、exit cleanup 和 exact stale reaper；加入 `deletion_unverified` disposition，禁止 broad deletion。
3. 将 preset staging、throwaway install、extension verification、task commit、Phase 2/installed verifier 的 auto-created 对象接入统一 lifecycle；显式 `WORK_DIR` 保留。
4. 更新 canonical inventory、package manifests/schema、installer projections、dogfood/platform overlays；运行 `apply.sh --repo .`，逐项处理 `.new/.bak`，执行 drift/sidecar/ownership checks。
5. 编写 package/runtime/unit/integration tests：success/failure/SIGINT/SIGTERM/early validation、SIGKILL next-run stale、repeat、live/in-use/non-stale、explicit root、unknown/caller/other-app exclusion、unsafe root 和 local deletion-unverified。
6. 运行 targeted package/runtime tests、current preset apply/verify/reapply/drift，并运行一个 representative isolated/clean fixture；完整 #267 matrix 记录为 deferred，不冒充 PASS。
7. 更新 task Docs SSOT Plan 对应的 Requirements/Design/Test traceability；运行 RDT、Architecture impact、planning wording 与 `guru-approve-task-plan`，获得明确 implementation approval 后才执行 `task.py start`。
8. Phase 2 实现后运行 `trellis-before-dev`、targeted `trellis-check`、Architecture/check gates；完成 fresh committed full-diff Branch Review、PR readiness、Finalizer/merge/closure。仅在 full merge gate 后请求 `合并PR`，不创建 tag/Release。

## Docs SSOT Plan

- Requirements authority：Issue #286 的 temporary lifecycle acceptance 与 exclusions；在 task RDT 中记录 R1-R7 到测试证据映射。
- Design authority：`design.md` 的 inventory/root/prefix/cleanup/reaper contract；Architecture impact 仅覆盖 temporary runtime、preset projection 和 declared adapters。
- Test authority：新增 package/runtime/unit/integration cases 与 preset apply/verify/reapply/drift、isolated fixture 命令；每个验收项绑定一个 deterministic test 或明确 `deletion_unverified`/`#267 deferred` evidence。
- Projection authority：canonical source -> dogfood -> installed -> Shared/Codex/Claude/Cursor -> preset installer；以 installer manifest、drift checker 和 sidecar scan 为一致性证据。
- Change boundary：不修改 #287 staging、#267 matrix、业务仓库 cleanup、tag/Release；若新增 Finalizer prefix，#293 仅复用本合同并自行更新 inventory。

## Validation Commands

```bash
python3 -m pytest trellis/skills/guru-team/packages/<changed-package>/tests
python3 -m pytest trellis/skills/guru-team/runtime/tests
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
```

Use the repository-managed Python/runtime wrappers where required. Report any deletion policy restriction as `deletion_unverified`; never mark skipped deletion evidence as PASS.

## Risk and Stop Points

- Inventory/root mismatch: stop before any deletion and require semantic review.
- Projection drift or `.new/.bak`: stop and reconcile canonical source before tests.
- Local deletion blocked: retain exact fixture and record `deletion_unverified`.
- Any scope pressure toward #287/#267/business cleanup: stop and route to the owning Issue.
