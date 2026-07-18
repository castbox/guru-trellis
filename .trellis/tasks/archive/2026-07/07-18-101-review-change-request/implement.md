# #101 实施计划：实现 change request readiness Skill

## 前置状态

- [x] 已读取 live #101、#98、#112 与 current main 上 #109、#111、#113、#114、#128 状态和实现。
- [x] Mandatory Phase 0 的 base sync、context discovery、requirements clarity、change-request wording review 均通过。
- [x] 已展示 handoff plan 并取得 branch/worktree/task side-effect confirmation。
- [x] 已创建 `feat/101-review-change-request`、指定 worktree 与 task。
- [x] 已确认 requirement clarity 无 open question，#101 是唯一 close unit。
- [ ] 完成 planning wording review，展示三份文档并取得 explicit post-planning confirmation。
- [ ] 记录/check schema 1.2 planning approval 后运行 `task.py start`。

## 实施步骤

### 1. 建立 canonical package 与 public interface

- 新增 `guru-review-change-request` package 的 Skill、interface、contract、schema、example、record/check wrappers 与 package tests。
- 在 `trellis/skills/guru-team/registry.json` 注册 active id、四平台支持与 workflow route id。
- 声明 semantic stage profile、workflow/standalone entry parity、schema id、artifact basename 与 five exits。
- 先运行 source package/schema tests，不修改旧 wording-pass route。

完成条件：source registry/interface/package tests 通过，scripts 只含 dispatcher 调用，example 不含 active task 或本机路径。

### 2. 实现 evidence linkage 与 runtime record/check

- 在 canonical shared runtime 增加 target normalization、prerequisite result validation、linkage projection、facts digest 和 freshness checker。
- 复用 #111/#113/#114 objective check functions；不复制 discovery、clarification 或 scanner。
- 增加 `record-change-request-review` 与 `check-change-request-review` CLI、bash wrappers、extension dispatcher command 与 tests。
- 固定 stdout-only pre-task path，拒绝 repo output locator。
- 增加 side-effect audit，证明调用前后 Git path set 不变。

完成条件：three target variants、current linkage、missing/stale/mismatch、facts digest 与 stdout-only tests 全部通过。

### 3. 实现 semantic evidence contract

- 固定 ten review dimension ids、finding shape、scope conclusion、AI Review Gate 与 human confirmation字段。
- Recorder 只接收完整 AI-authored payload；checker 只验证 shape、refs、hash、consumer 与 ready invariants。
- 增加 AI Gate 缺失/不完整 tests，证明 scanner/validator success 不能产生 `ready`。
- 增加 non-ready finding、reason、affected evidence/hash 与 exact consumer tests。

完成条件：semantic package tests 证明 AI 与 script boundary，runtime 没有 route/finding/readiness generator。

### 4. 接入 five-exit workflow route

- 把 `guru-review-contract-wording:change_request:pass` 改为 mandatory invoke `guru-review-change-request`。
- 增加 five exit markers、unique consumer 与 terminal stop target。
- 声明 `ready -> guru-create-task-workspace`，同时验证 #112 package 缺失时 fail closed。
- 保持 planning/explicit-path wording routes、context/clarity re-entry 与 Phase 1 routes不变。

完成条件：workflow marker tests覆盖 missing/unknown/multiple/unmapped exit，five exits 均只有一个 consumer。

### 5. Replacement verification 后删除旧 owner

- 先运行 package/runtime/workflow targeted suites，确认新 readiness path完整。
- 删除 `change_request:pass -> guru-full-task-intake-chain` 的旧 active route。
- 搜索 Guru-owned workflow/runtime/docs/platform source中的重复 readiness dimensions、route或 inline ownership并迁移为 stable Skill 引用。
- 对每个搜索 hit 分类为 active owner、prerequisite owner、#112 owner、archive history 或 frozen upstream overlay。
- 只删除 active owner；保留 prerequisites、#112 behavior、archive 与 frozen overlay。

完成条件：active Guru-owned source 只有 `guru-review-change-request` 一个 readiness semantic SSOT，replacement tests 仍通过。

### 6. 更新 durable Docs SSOT

- 更新 canonical package contract、workflow、requirements、workflow/preset README 与 workflow/data/script/quality/preset specs。
- Consumer docs 只记录 stable id、required evidence、schema/artifact、five exits、route 与 own obligation。
- 记录 pre-task stdout-only、#112 task-local persistence、ownership gate 与 legacy replacement boundary。
- 同步 dogfood `.trellis/workflow.md`。

完成条件：Docs SSOT 与 package/interface/runtime 一致，task artifact delta已合并，durable docs 不形成第二 semantic owner。

### 7. Preset、dogfood 与四平台同步

- 更新 extension manifest/public API、preset installer/inventory/tests 与 README。
- 运行 canonical preset apply 同步 `.trellis/guru-team/**` 和 shared/Codex/Cursor/Claude package copies。
- 校验 bytes、executable mode、managed hashes、registry entry 与 dispatcher command。
- 运行 upstream ownership gate与 dogfood drift，确认 frozen overlay identity未变化。
- 清点 `.new`、`.bak`、sidecar、removal、conflict，任一非零结果阻止继续。

完成条件：canonical、installed、four-platform copies 一致，dogfood与ownership gate通过，sidecar family为零。

### 8. Clean throwaway 与 update/reapply

- 创建 clean temporary Git repo，按 README 使用 workflow marketplace 安装 `guru-team` workflow。
- 应用 Guru Team preset，运行 installed package/runtime checks 与 three target/five exit smoke fixtures。
- 执行 `trellis update --force`，重新应用 workflow和preset。
- 再次检查 package、route、manifest、platform copies、mode、runtime commands 与 sidecar/removal/conflict zero。
- 记录 Trellis version、source ref、command exit、installed digests 与 residue audit。

完成条件：fresh install 与 update/reapply 后均通过；任一未执行项必须在 Phase 2、PR body 和 final report 标为未覆盖风险。

### 9. Phase 2、commit、Branch Review 与 finish

- Dispatch Trellis implement sub-agent 完成步骤 1-8 和 implementation handoff；主会话负责 scope 与冲突协调。
- Dispatch Trellis check sub-agent 完整执行 `trellis-check`，覆盖 specs、requirements、code/schema/runtime、tests、distribution、docs、ownership、deployment impact 与 task artifacts。
- 记录/check `phase2-check.json`；finding 修复后重跑受影响测试与完整 Phase 2 final round。
- 调用 `guru-create-task-commit` 精确 stage 本 task files并提交。
- Push branch 后 dispatch independent Branch Review sub-agent，覆盖 `origin/main...HEAD` 全 diff。
- P0-P3 finding 修复必须回到 implementation + full Phase 2，再创建 finding-fix commit并重跑 Branch Review。
- Branch Review closure 后准备中文 PR title/body；ledger 只关闭 #101，body 只含 `Closes #101`。
- 运行 `trellis-finish-work` dry-run，AI 审查 immutable closeout plan，再用同 digest formal finish。
- Formal finish 在 push 后、PR 创建前运行 remote branch-pinned marketplace verification，最终把同一 PR 标为 Ready，不执行 merge。

## 预计变更范围

### Canonical/public sources

- `trellis/skills/guru-team/registry.json`
- `trellis/skills/guru-team/packages/guru-review-change-request/**`
- `trellis/workflows/guru-team/workflow.md`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- `trellis/workflows/guru-team/scripts/bash/record-change-request-review.sh`
- `trellis/workflows/guru-team/scripts/bash/check-change-request-review.sh`
- `trellis/guru-team-extension.json`
- `trellis/presets/guru-team/scripts/**`

### Durable docs/spec

- `docs/requirements/requirement-main.md`
- `docs/requirements/guru-team-trellis-flow.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`
- `.trellis/spec/workflow/skill-package-contract.md`
- `.trellis/spec/workflow/workflow-contract.md`
- `.trellis/spec/workflow/data-contracts.md`
- `.trellis/spec/workflow/companion-scripts.md`
- `.trellis/spec/workflow/quality-guidelines.md`
- `.trellis/spec/preset/installer.md`
- `.trellis/spec/preset/overlay-guidelines.md`
- `.trellis/spec/preset/upstream-ownership.md`

### Generated installed copies

- `.trellis/guru-team/**`
- `.agents/skills/guru-review-change-request/**`
- `.codex/skills/guru-review-change-request/**`
- `.cursor/skills/guru-review-change-request/**`
- `.claude/skills/guru-review-change-request/**`
- `.trellis/workflow.md`

`trellis/presets/guru-team/overlays/**` 不新增、不修改、不删除。

## 验证命令计划

具体 test count 与 fixture 名在实现后从 current suite输出记录。最低命令集：

```bash
python3 trellis/workflows/guru-team/scripts/python/guru_team_trellis.py check-skill-packages --json --mode source --root .
python3 -m unittest trellis/skills/guru-team/packages/guru-review-change-request/tests/test_contract.py
python3 -m unittest trellis/skills/guru-team/tests/test_skill_packages.py
python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
python3 -m unittest trellis/presets/guru-team/scripts/python/test_upstream_ownership.py
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py .trellis/guru-team/scripts/python/guru_team_trellis.py
bash -n trellis/workflows/guru-team/scripts/bash/*.sh .trellis/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m json.tool trellis/skills/guru-team/registry.json
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-18-101-review-change-request
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode installed
git diff --check
```

Residue audit 固定覆盖：

```bash
find . -type f \( -name '*.new' -o -name '*.bak' \)
git status --short
git diff --name-status --diff-filter=D origin/main...HEAD
```

Active owner search 固定覆盖 stable id、legacy route、review dimensions 与 artifact basename。Archive/task history hits 保留并标为 non-active；frozen overlay hits不修改；Guru-owned active duplicate hit 使 gate失败。

## 测试矩阵

| 场景 | 期望 |
| --- | --- |
| Existing issue + current three prerequisites | AI-authored `ready` record/check通过 |
| Proposed draft + current three prerequisites | Side-effect-free `ready` record/check通过 |
| Standalone request + current three prerequisites | 与 workflow同强度通过 |
| Missing context | `ready`拒绝；AI route为 `refresh_context` |
| Missing clarity | `ready`拒绝；AI route为 `clarify_requirements` |
| Missing wording | `ready`拒绝；AI route为 `review_wording` |
| Context/base/live/history stale | `ready`拒绝；AI route为 `refresh_context` |
| Clarity target/content/scope mismatch | `ready`拒绝；AI route由AI记录 |
| Wording non-pass/unchecked/hash mismatch | `ready`拒绝；AI route为 `review_wording` |
| Target已完整实现且无独立 gap | terminal `blocked` |
| Gate missing或ten dimensions不全 | Recorder/checker fail closed |
| Scanner/validator success + empty AI Gate | 不能生成或验证 `ready` |
| Unknown/multiple/unmapped exit | Schema/workflow checker fail closed |
| Consumer mismatch | Checker fail closed |
| Pre-task recorder | stdout-only，repo path set不变 |
| `ready` consumer | 指向 #112 stable id，不创建 workspace |
| #112 package absent | Workflow fail closed，不回退旧 intake |
| Canonical/installed/four platforms | Bytes + mode一致 |
| Dogfood apply/drift | Ownership与drift通过，sidecar zero |
| Fresh throwaway install | Marketplace + preset + runtime可用 |
| `trellis update --force` + reapply | Package/route/runtime恢复且 residue zero |
| Remote branch marketplace | Push后、PR创建前验证通过 |

## Phase 2 与 Branch Review 范围

- Issue #101 每条 requirement 与本 task 三份 planning docs；
- semantic AI ownership 与 deterministic script boundary；
- target variants、prerequisite current/hash linkage、ten dimensions、findings、five exits；
- pre-task stdout-only 与 #112 task-local persistence boundary；
- replacement-first 删除与 #111/#113/#114/#112/#128 scope preservation；
- canonical/installed/platform/dogfood/throwaway/update/remote evidence；
- Docs SSOT reconciliation；
- secret、CI/CD、container、Kubernetes、DB migration、Makefile 和 deployment impact；
- full `origin/main...HEAD` committed diff、task metadata、ledger 与 PR close semantics。

## 回滚点

- Commit 前：新链路 tests未通过时不删除旧 active route，修订后重新验证。
- Commit 后：使用 PR revert 恢复 pre-#101状态；禁止引入长期 dual-owner flag。
- Publish 前：remote marketplace 或 closeout plan失败时保持 branch/PR未发布状态，修复后重新走 dry-run 与同 digest formal finish。
