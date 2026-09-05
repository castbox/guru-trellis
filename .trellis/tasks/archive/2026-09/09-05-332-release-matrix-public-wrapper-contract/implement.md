# Implementation Plan

## Checkpoint A. Contract And Architecture Alignment

- [ ] 修订 #332 task-local Requirements/Design/Test/Architecture impact，确认
  `dedicated_refactor_slice`、原入口 identity、Interface wrapper authority、兼容退出和无第二 authority。
- [ ] 保持 active `.44` shared current 不变；新增 task-owned RDT contribution
  `docs/requirements-design-test-contributions/332-release-wrapper-entry-correction/` 与 Architecture
  contribution `docs/architecture/contributions/332-release-wrapper-entry-correction.md`，绑定 expected `.44`、
  target `.45` 和 23 Skills / 97 exits / 77 commands。
- [ ] 更新 durable workflow specs，删除“新 facade 替代旧 invoke”表述，保留 invocation-local transaction、
  mapped recovery、terminal stop 和 operation budget。
- [ ] 生成 #332 Issue exact body diff，覆盖原入口纠正方向、successor `.45`、23 / 97 / 77 graph 与旧
  candidate evidence 作废；取得独立确认并 live reread 后，才进入 task activation。

## Checkpoint B. Four Original Public Entries

- [ ] `guru-create-task-commit`：把 Happy Path candidate transaction 合并到
  `invoke-guru-create-task-commit`，扩展原 command 的 closed arguments，保留旧 `--invocation` compatibility
  branch，删除 `invoke-guru-create-task-commit-happy-path-v1` 与 `invoke-happy-path-v1.sh`。
- [ ] `guru-review-task-publication`：把 semantic-result record/check/projection 合并到
  `invoke-guru-review-task-publication`，保留旧 owner-result compatibility branch，删除
  `review-task-publication` 与 `review-task-publication.sh`。
- [ ] `guru-finalize-task`：把 confirmed-preview transaction loop 合并到
  `invoke-guru-finalize-task`，保留旧 owner-result compatibility branch，删除
  `finalize-task-happy-path` 与 `finalize-task-happy-path.sh`、`legacy_public_invocation` 双 validator 模型。
- [ ] `guru-merge-task-pr`：把 pre/post snapshot、merge、recovery 与 projection 合并到
  `invoke-task-pr-merge`，保留旧 gate compatibility branch，删除
  `complete-task-pr-merge` 与 `complete-task-pr-merge.sh`；保留单一 watcher。
- [ ] 清理只服务被删除 command/wrapper 且无 consumer 的 schema/example/test/runtime adapter；保留原
  invoke Happy Path 直接消费的 transaction/recovery 能力。

## Checkpoint C. Generic Interface-Driven Consumers

- [ ] 修改 compatibility matrix `_assert_platform_projection()`，按 installed Interface 选择唯一 public
  wrapper并校验 exact bytes/mode/leak。
- [ ] 修改 throwaway `verify_package_projections()`、`verify_closeout_package_boundaries()` 和 publication
  projection smoke，
  把 generic wrapper 选择与 package-specific `invoke.sh` 调用分开。
- [ ] 推广 `runtime/validate.py` 的 platform launcher fallback 校验到 Interface-declared public wrapper。
- [ ] 审核 `native_adapter.py` 每处 `scripts/invoke.sh`：generic path 改为 Interface-derived；仅保留明确
  qualification-only 的固定路径，并补作用域测试。
- [ ] 增加 `guru-restore-archived-task` 非 `invoke.sh` positive regression，覆盖 source/installed/platform/
  actual-load/eval，不改变该 Skill 本身的公开合同。

## Checkpoint D. Distribution And Public Documentation

- [ ] 更新四个 canonical `SKILL.md`、references、interfaces、commands、evals/tests，使原 `invoke.sh` 是唯一
  Happy Path，compatibility mode 只由旧参数触发。
- [ ] 删除 preset README 中不存在的共享 facade paths，明确 shared/package-private/platform-public 三层。
- [ ] 通过 canonical preset apply 同步 `.trellis/guru-team/**`、`.agents/.codex/.claude/.cursor`；验证旧
  managed wrapper 进入 removals，不产生 `.new`/`.bak`。
- [ ] 重生成 extension manifest/managed inventories，并确认旧 candidate checkout 未被修改。

## Checkpoint E. Focused Tests And Operation Budgets

- [ ] 四个 package contract/runtime tests 覆盖 Happy mode、compatibility mode、参数冲突、stale/mismatch、
  stdout loss、mapped recovery、terminal stop。
- [ ] Closeout integration 直接调用四个原 `invoke.sh`，断言 Happy mode 不触发 compatibility branch，
  command invocation 下降至少 50%、重复完整事实读取下降至少 70%、terminal 后 operation 为 0。
- [ ] Commit 覆盖 hooks、dirty/staged drift、unrelated preservation、ref mutation recovery；Publication
  覆盖 ready/metadata/content/external/ledger；Finalizer 覆盖 reprepare/adoption/stale/recovery；Merge 覆盖
  watcher、head/base/policy/closure/Phase 2 re-entry/output loss。
- [ ] Installer/matrix/throwaway/runtime/eval tests 覆盖任意 Interface wrapper path 与 private leak rejection。

## Checkpoint F. Canonical, Installed And Release Preparation Validation

- [ ] 运行 affected Python compilation、shell syntax、JSON/schema、task validation 与 `git diff --check`。
- [ ] 运行四 package suites、restore suite、closeout/finish integration、runtime/eval、preset installer、
  matrix routing 与 representative clean installed/throwaway tests。
- [ ] 运行 source/installed package validator、all-platform projection equality、ownership、preset reapply、
  dogfood drift、managed removals 与 recursive sidecar-zero。
- [ ] 完成 Phase 2 Architecture project check、RDT/Docs SSOT check 与完整 task scope semantic check。
- [ ] 只在后续独立授权下执行初始 task commit 与独立完整 Branch Review；此时 shared current 仍为 `.44`。

## Checkpoint G. Serialized Authority Promotion And Re-entry

- [ ] 初始 Branch Review 通过后，由 serialized RDT/Architecture owner 绑定 expected `.44` 生成唯一 active
  successor `.45`，修订 `DES-019`、distribution evidence、#330 RDT 语义和 23 / 97 / 77 live graph。
- [ ] promotion-created diff 重新进入 fresh Phase 2、task commit 与独立 committed full-diff Branch Review；
  不复用 promotion 前的 check/review evidence。
- [ ] 只在后续独立授权下执行 Publication、Finalizer、PR merge；merge 后从 fresh `origin/main` 创建新的
  detached clean exact candidate，并从零执行 #332 Release Gate。

## Expected File Scope

- Canonical closeout packages：
  `trellis/skills/guru-team/packages/{guru-create-task-commit,guru-review-task-publication,guru-finalize-task,
  guru-merge-task-pr}/**`。
- Generic runtime/eval：`trellis/skills/guru-team/runtime/**`、
  `trellis/skills/guru-team/adapters/eval/native_adapter.py` 及其 tests/fixtures。
- Preset/verifier：`trellis/presets/guru-team/scripts/{python,bash}/**`、preset README、installer tests。
- Workflow/spec/docs：`trellis/workflows/guru-team/**`、`.trellis/spec/workflow/**`、preset spec copies、
  task-owned RDT/Architecture correction contributions；`.44` 只作为 source authority。
- Serialized promotion output：`docs/{requirements,design,test}/versions/current-main-0.6.5-guru.45/**`、
  三个 README、Architecture current authority/evidence/history 与 `.trellis/spec/{docs,architecture}` projection；
  仅在初始 committed review 通过后由 owner 生成。
- Generated projections：`.trellis/guru-team/**`、`.agents/skills/**`、`.codex/skills/**`、
  `.claude/skills/**`、`.cursor/skills/**` 和 extension manifest，仅由 preset apply 同步。
- Task artifacts：当前 `prd.md`、`design.md`、`implement.md`、`task.json`、ledger。

## Validation Commands

最终精确命令由 affected test discovery 收敛，最低集合包括：

```bash
python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-create-task-commit/tests -p 'test_*.py'
python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-review-task-publication/tests -p 'test_*.py'
python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-finalize-task/tests -p 'test_*.py'
python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-merge-task-pr/tests -p 'test_*.py'
python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-restore-archived-task/tests -p 'test_*.py'
python3 -m unittest trellis.skills.guru-team.tests.test_closeout_happy_path_integration
python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
./trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json
./.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode installed --json
./trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
./trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
./trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
python3 ./.trellis/scripts/task.py validate .trellis/tasks/09-05-332-release-matrix-public-wrapper-contract
git diff --check
```

还必须运行 compatibility matrix/throwaway 的 focused wrapper projection cases、runtime/eval generic wrapper
variation、managed removal 与 recursive sidecar checks。完整 #332 exact-candidate Release Gate 不在当前
planning/implementation checkout 冒充执行，只能在 preparation merge 后的新 candidate 上运行。

## Pre-Start Gate

- [ ] 三份 planning docs 已通过 requirement convergence 与 PRD convergence。
- [ ] Planning wording review 已通过，无未分类弱措辞或错误双入口假设。
- [ ] Architecture planning impact/path 与 RDT Docs SSOT Plan 已审查。
- [ ] `guru-approve-task-plan` 返回 `approved` current typed result。
- [ ] 已向用户展示本版最终规划摘要；其后的独立明确批准是 `task.py start` 和实现的必要前置。
- [ ] 该批准不授权 commit、push、PR、merge、tag、Release、Issue closure 或 cleanup。
