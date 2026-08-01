# #119 实施计划：Finish family combined integration

## 1. 执行原则

- 所有实现基于 fresh worktree 与 live main base；冻结 donor只作只读语义参考。
- Canonical source先改，dogfood与平台 discovery copies只经 preset apply生成。
- PR #165 public I/O、semantic owners、typed exits与 mapped consumers保持不变。
- 每个阶段失败即停止，禁止带着 stale evidence进入下一阶段。
- Commit、push、PR、merge、Issue closure与cleanup均属于独立授权边界。

### 1.1 当前恢复覆盖规则

- 保留 `3fe71d7` 与 `15d957b` 失败链；`57e7d0d` 只恢复同一 task active locator。
- 旧 closeout plan、finalization gate、publication readiness 与 Branch Review 只作失败证据。
- 本轮实现只修改 finalizer runtime、对应 unit/integration tests 与 preset 生成的 installed copies。
- 既有 clean install、upgrade/update、全量 Skill suite 与无关 Phase 2 不因旧 digest 变化重放。
- PR #166 保持 Draft；push 与 public finalizer 原子事务须在后续分别取得明确授权。

## 2. 有序实施清单

### Phase A：Guru entry、workflow 与 durable SSOT

- [ ] 在 canonical overlay新增 Codex、Claude、Cursor 的 `guru-finish-work` 薄入口。
- [ ] 更新 canonical workflow，把日常 Finish entry改为 `guru-finish-work`，保留五个 legacy paths
  的 bounded compatibility说明。
- [ ] 更新 README、workflow README、preset README 与 Docs SSOT Plan列出的 durable specs。
- [ ] 更新 `upstream-ownership.json`：五个 legacy finish entries移除 #119 blocker，保留
  active migration state、现有 payload digest、replacement owners与 `removal_issue=132`。
- [ ] 扩展 ownership/installer tests，禁止 Guru entry被归入 transitional legacy。

### Phase B：Checked marketplace projection bridge

- [ ] 在 current runtime中把 `marketplace_verification` private projection显式传入
  pre-draft state、final projection与 active projection validators。
- [ ] 将同一 projection传入 normal `execute_archive_metadata_transaction`。
- [ ] 将同一 projection传入 `resume_active_archive_move` 的 validation与 archive call。
- [ ] 在 finalizer preview/retry path从 checker-passed #117 owner result构建 projection。
- [ ] 保持 legacy executor在没有外部 owner result时执行 current deterministic verifier。
- [ ] 新增 focused tests，断言 raw owner artifact不能被 legacy parser冒充 passed projection。
- [ ] immutable plan-owned pending/passed ledger machine evidence 是唯一可接受的 publication
  artifact/entry/working-tree bindings，保持 semantic review 与其余 bindings 不变。
- [ ] 新增真实顺序回归：publication 先绑定、content push 后写 pending、checked
  `verified` re-entry 自动续接；额外 ledger 语义或 artifact drift 仍 fail closed。

### Phase C：Terminal eval 与 combined integration

- [ ] 在 canonical finalizer corpus新增两个 `published` terminal cases与 facts fixtures。
- [ ] 在 current native adapter和 representative fixture中新增两个 staging recipes。
- [ ] 新增 dedicated combined integration suite，验证 13 exits、六组 routes、private/public
  boundary、Guru entries、legacy ownership与 corpus equality。
- [ ] 删除本 task触及面内被 dedicated suite替代的 duplicate assertions；不删除 package-local
  behavior tests。

### Phase D：Canonical apply 与 installer acceptance

- [ ] 运行 ownership pre-mutation checker。
- [ ] 运行 `apply.sh --repo . --all-platforms` 生成 dogfood workflow、Guru entries、runtime、
  eval corpus与 installed discovery copies。
- [ ] 检查并处理每个 `.new`/`.bak`；目标结果为无未解释 sidecar。
- [ ] 运行 dogfood overlay drift checker。
- [ ] 扩展并运行 clean throwaway verifier，覆盖 clean install、workflow preview/switch、
  CLI upgrade dry-run、`trellis update`、workflow reselect、preset reapply、Guru entries、legacy compatibility、
  normal/extension closeout transaction与 multi-platform discovery。

### Phase E：Full regression 与 Docs closure

- [ ] 运行完整 runtime suite，覆盖 #105 matrix与新增 projection recovery tests。
- [ ] 运行 Skill package、combined integration、preset apply、ownership与 schema validation suites。
- [ ] 运行 stale-term/duplicate-owner scan，确认 `guru-finish-work` 是日常入口，legacy naming只
  出现在 compatibility、migration history、script executable或 historical contract语境。
- [ ] 复核 Docs SSOT Plan，记录每个 durable owner的 update或 no-update结论。
- [ ] 运行 `git diff --check`、workspace boundary与 frozen donor invariant checks。

### Phase F：Independent Phase 2 check

- [ ] 由 Trellis check agent独立读取 current plans、specs、完整 diff与 test evidence。
- [ ] `guru-check-task` semantic gate逐项覆盖 #119 acceptance、#105 matrix、Docs SSOT、
  install/update/reapply、public/private boundary与 exclusions。
- [ ] Finding fix发生后重新运行受影响 tests与 fresh Phase 2 check。
- [ ] Gate通过后停止在 commit授权前。

### Phase G：当前 finalizer recovery correction

- [ ] 在 Ready executor 增加六次读取预算，保持 PR fact validator 单次检查。
- [ ] 覆盖 stale-then-converged 与 persistent-mismatch 两条 PR HEAD 回归。
- [ ] 把 finalizer preview 调整为 locator/plan/transaction classification 先于 publication owner 检查。
- [ ] 覆盖 compact 12-file archive 无 `pr-readiness.json` 的 same-plan Ready recovery。
- [ ] 覆盖 active pre-publication 缺少 readiness 仍 stale。
- [ ] 断言 recovery 不创建重复 PR、archive commit、evidence commit、recovery input 或 side effect，
  并唯一复用 PR #166 fixture。
- [ ] 运行 canonical apply，只同步 runtime 与 Finish-family installed integration test。
- [ ] 运行本节受影响验证与 current `guru-check-task`，不执行 Phase D 的 throwaway/upgrade 重放。

## 3. 验证命令与预期结果

```bash
python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 trellis/skills/guru-team/tests/test_skill_packages.py
python3 trellis/skills/guru-team/tests/test_finish_family_integration.py
python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
python3 trellis/presets/guru-team/scripts/python/test_upstream_ownership.py
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
target_cli="$(jq -r .target_trellis_cli trellis/presets/guru-team/ownership/upstream-ownership.json)"
trellis upgrade --dry-run --tag "$target_cli"
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
git diff --check
```

预期结果：Python suites零 failure/error；ownership与 drift返回 pass；apply后无未解释
`.new`/`.bak`；throwaway完成 clean install、update/reselect/reapply与两类 closeout；
CLI upgrade dry-run输出版本绑定的 install command且不改变 global Trellis；`git diff --check`无输出。

Native CLI未安装或未登录时，production adapter必须返回 contract声明的 `unsupported`，
不得伪装成 `passed`。Shared adapter与 deterministic corpus closure必须在本机执行通过。
Exact pushed-remote verification属于后续 push授权后的 `guru-verify-extension-installation` gate，
本阶段只声明 local candidate与 installed throwaway结果。

### 3.1 当前恢复增量命令

```bash
python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 trellis/skills/guru-team/tests/test_finish_family_integration.py -q
GURU_FINISH_INTEGRATION_MODE=installed GURU_FINISH_INTEGRATION_ROOT="$PWD" \
  python3 .trellis/guru-team/skills/tests/test_finish_family_integration.py -q
python3 -m unittest trellis/skills/guru-team/packages/guru-finalize-task/tests/test_contract.py
python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
git diff --check
```

预期结果：六项 recovery regression 全部通过；source 与 installed integration 结果一致；preset
apply test 和 dogfood drift 无差异；`git diff --check` 无输出。随后 public `guru-check-task`
只消费上述 current evidence 与未变的既有 task-scope evidence。

## 4. Review gates

### Gate 1：Scope 与 authority

- Current diff只实现 #119剩余 delta。
- #116/#117/#118 internal behavior、#132 cleanup与排除场景均未进入 implementation。
- Frozen donor未发生 HEAD、index、worktree或 runtime input mutation。

### Gate 2：Routing 与 public I/O

- Global workflow每个 exit只有一个 consumer或 stop。
- Mapped exits自动承接，happy path没有 generic continuation prompt。
- Public DTO、schema ids与 output fields零扩张；private projection没有 artifact化。

### Gate 3：Transaction 与 recovery

- Checked marketplace projection贯通 preview、retry、normal archive与 active-completed recovery。
- #105 full suite通过；existing failure matrix与 transaction order零删减。
- Archive前 failure保持 active state；archived exact recovery不重新读取 #117 private artifact。

### Gate 4：Distribution 与抗漂移

- Canonical/dogfood/installed bytes一致。
- Guru entries在 Codex、Claude、Cursor路径存在并由 preset管理。
- `trellis update`、workflow reselect、preset reapply、managed hashes与 sidecar contract通过。
- CLI upgrade dry-run精确绑定 ownership inventory 的 `target_trellis_cli`，host mutation为零。
- Legacy finish payload保持 current bytes，#119 blocker清除，#132 removal owner保持。

### Gate 5：Docs SSOT 与 independent check

- `design.md` §10的 durable paths完成更新或记录 no-update理由。
- Durable docs不保留冲突日常入口或重复 Skill内部步骤。
- Independent `guru-check-task`基于 current diff与 current test evidence返回 passed exit。

## 5. 授权停止点

Planning wording review与 semantic plan review完成后，展示 `prd.md`、`design.md`、
`implement.md` 三个 current链接，并暂停以索取 post-planning confirmation。收到该确认后才记录
planning approval、运行 `task.py start` 与进入实现。

实现与 Phase 2 check通过后停止。Stage/commit、push、PR creation、merge、Issue closure与
worktree/task cleanup分别重新展示 exact side effects并取得授权。

当前恢复已获得 recovery commit、规划修订、实现、受影响验证、current mandatory gate、一个
task-work commit 与 fresh Branch Review 的明确授权。完成 fresh Branch Review 后停止；普通 push、
新 finalizer plan 的原子事务、PR Ready、Issue mutation、merge 与 cleanup 均不在该授权内。

## 6. 回滚与恢复

- Planning gate失败：只修订 task planning files，重新执行完整 wording与 plan review。
- Implementation/test gate失败：保留 fresh worktree diff，修复后重跑受影响 suite与完整 check。
- Apply产生 sidecar：逐文件判定 recognized managed state，不提交未解释 sidecar。
- Public contract或 scope需要变化：停止实现，转入 `guru-clarify-requirements`。
- 发布动作未获授权：不创建 commit、remote ref、PR或 Issue mutation。

## 7. Docs SSOT checkpoint

实施使用 `design.md` §10 的 `ssot_first` 策略。Phase 2 handoff必须逐项记录 durable update、
audited no-update、task-history-only内容与 #132 limitation；finish/archive不承担首次 Docs merge。
