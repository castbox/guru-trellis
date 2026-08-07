# #178 Implementation Plan

## 1. Ordered Checklist

- [x] I1. 建立 current consumer/asset inventory：定位 discovery artifact/profile/locator、Clarify/Readiness/Workspace reader、runtime recorder/checker/wrapper、manifest/overlay/platform copy和terminal owner checkpoint lifecycle；将历史 archive从修改集排除。
- [x] I2. 先修订 durable Docs SSOT：`skill-package-contract.md`、`data-contracts.md`、`companion-scripts.md`，固化 stdout正常路径、最小 DTO、lazy recovery与 consume-and-clean规则。
- [x] I3. 收敛 canonical `guru-discover-change-context` Interface 1.3：删除 tracked private artifact、`task_local_reentry`、snapshot locator/supersession assets，更新 SKILL/contract/interface/schema/example/eval/tests。
- [x] I4. 修改 shared runtime：支持 pre-task/standalone owner result通过 stdin/pipe完成 objective check与public invocation；删除 task-local context artifact写入、读取、trackability、replacement/supersession current路径。
- [x] I5. 修改 minimal handoff edge：从 `context_ready`、Clarify initial input与 projection删除 context locator；更新 Clarify owner validation，使其从 current AI/live authority承接，不读 discovery snapshot。
- [x] I6. 收敛后续 consumers：删除 Change Request Review与Workspace对 context locator/完整 discovery prerequisite artifact及 hash linkage的依赖，保持每个 Skill独立 semantic gate与live reread。
- [x] I7. 实现 lazy owner recovery与统一 consume-and-clean：仅为真实 active-task re-entry写 ignored current checkpoint；wrapper成功后删除；stale与terminal路径清理 input/checkpoint/result/temporary projection和空目录。
- [x] I8. 更新 extension manifest、managed assets、ownership checks、workflow/preset README、canonical workflow markers与 durable docs，删除current contract中的退役path/schema/profile/field。
- [x] I9. 使用 preset installer同步 `.trellis/guru-team/**`、`.trellis/workflow.md`、`.agents/skills/**`、`.codex/skills/**`、`.claude/skills/**`、`.cursor/skills/**`及manifest声明的其它平台入口；逐个处理 `.new`/`.bak`。
- [x] I10. 完成 source/runtime/package targeted tests：正常path zero-write、minimal projection、consumer live reread、真实recovery、wrapper consume-and-clean、stale restart、terminal zero-residue与unsafe cleanup fail-closed。
- [x] I11. 完成 installed/dogfood/throwaway/update验证；记录 remote branch marketplace install在push前不可执行的边界，不折算为通过。
- [x] I12. 运行 fresh current-only Phase 2 semantic check；修复所有 P0-P3 finding并重跑受影响证据。commit/Branch Review/push/PR不在本计划自动执行。

## 2. Primary Files and Rollback Points

- Shared runtime：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 及其 tests。风险最高，先以 targeted tests保护 transport/cleanup，再做大范围删除。
- Discovery package：`trellis/skills/guru-team/packages/guru-discover-change-context/**`。Interface/schema/example/eval必须同一次 current-contract修改闭合。
- Direct consumers：`guru-clarify-requirements/**`、`guru-review-change-request/**`、`guru-create-task-workspace/**`。任何残留 locator reader都视为未完成。
- Distribution：`trellis/guru-team-extension.json`、preset scripts/README、workflow README、overlays与 installed copies。只从 canonical同步，不反向修改 source。
- Durable docs：`.trellis/spec/workflow/{skill-package-contract,data-contracts,companion-scripts}.md`。

## 3. Validation Commands

Targeted first:

```bash
python3 -m unittest trellis/skills/guru-team/packages/guru-discover-change-context/tests/test_contract.py
python3 -m unittest trellis/skills/guru-team/packages/guru-clarify-requirements/tests/test_contract.py
python3 -m unittest trellis/skills/guru-team/packages/guru-review-change-request/tests/test_contract.py
python3 -m unittest trellis/skills/guru-team/packages/guru-create-task-workspace/tests/test_contract.py
python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
```

Distribution and complete gates:

```bash
python3 -m unittest trellis/skills/guru-team/tests/test_skill_packages.py
python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
python3 ./.trellis/scripts/task.py validate .trellis/tasks/08-07-178-ephemeral-context-runtime
git diff --check
```

Static current-contract scans must prove active canonical/installed/runtime files contain no retired `context-discovery.json`, `task_local_reentry`, `prior_snapshot_locator`, `handoff_context_locator`, `context_locator` discovery edge or superseded discovery chain. Archive hits are excluded and not edited.

## 4. Acceptance Mapping

- A1: I3-I4, targeted normal/standalone zero-write tests, throwaway fresh task.
- A2-A3: I5-I6, Interface projection validation, wrapper-to-consumer integration.
- A4-A5: I3-I4-I7, static scan, stale/recovery matrix tests.
- A6-A7: I7, terminal zero-residue and forbidden-persistence assertions.
- A8-A10: I8-I11, source/installed closure, overlay drift, platform parity, throwaway/update.
- A11: I1/I8 static scope checks; archive and Finalizer follow-up files remain unchanged.
- A12: I12 independent current-HEAD semantic check and later Branch Review gate.

## 5. Pre-Start Checks

- Planning wording review must classify this as current-contract-only #178 scope, not a generalized cleanup of every Finalizer artifact.
- `guru-approve-task-plan` must verify all three planning docs, Docs SSOT Plan, issue ledger and curated JSONL context.
- Task activation may proceed without another routine confirmation because the user has explicitly requested implementation and repeatedly confirmed continuation; commit/push/PR remain separate side effects.
