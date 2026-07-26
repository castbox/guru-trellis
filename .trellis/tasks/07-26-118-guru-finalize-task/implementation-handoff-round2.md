# Round 2 实现修复交接

## 1. 实现范围与结论

本轮只修复 Phase 2 Round 2 的两个 current-scope finding：

- `F-ROUTE-01`：`published` 在进入 committed recovery 前必须拥有当前同
  task/plan/reviewed HEAD 的 #117 owner-checker 结果，且 typed exit 只能是
  `verified` 或 `not_required`。只有 transaction engine 客观识别的
  `archived`、`ready` 两个 inherited committed recovery state 可以继续恢复；
  public input 不携带 transaction state，caller label 不能取得该例外。
- `F-DTO-02`：gate 的 `route.output` 不再使用 truthiness 判断。除
  `published` 可在 deterministic PR facts 尚不存在时使用唯一 closed private marker
  `{"materialization":"executor"}` 外，所有 route 在 gate record/check boundary
  都按实际 selected-exit public schema 校验。Executor 生成 `published` DTO 后再次
  按 public schema 校验。

没有修改 #105 compatibility transaction 的既有顺序或 failure/recovery matrix，
没有修改 global workflow、upstream `trellis-finish-work`、preset overlay 或官方
`task.py`，也没有承接 #119/#132。

## 2. 变更面

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 及其 dogfood
  runtime copy：增加 current #117 owner evidence 装载与 pre-archive published
  precondition；移除空 output bypass；限制并 materialize 唯一 published marker。
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：增加
  published evidence negative/positive、empty/missing/extra/wrong-exit、
  非 published marker rejection 与 published post-materialization regressions。
- `trellis/skills/guru-team/packages/guru-finalize-task/schemas/semantic-review-input.schema.json`
  与 `schemas/task-finalization-gate.schema.json`：marker/non-marker 使用互斥 closed
  branches；`{}` 不满足任一 branch。
- `trellis/skills/guru-team/packages/guru-finalize-task/tests/test_contract.py`：增加
  package-local schema regression，证明 exact marker 通过而空 object 失败。
- 上述 package 通过 supported all-platform preset apply 同步到 installed shared、
  Agents、Codex、Claude、Cursor；六份 package 当前逐文件 byte-identical。

## 3. Docs SSOT Handoff

- Strategy：`ssot_first`。
- Durable docs/spec：Round 1 已把
  `.trellis/spec/workflow/skill-package-contract.md`、
  `.trellis/spec/workflow/workflow-contract.md`、
  `.trellis/spec/workflow/quality-guidelines.md`、workflow/preset/public docs 与三份
  README 收敛为 active package `13/52`、target-owned authoring handoff `12`、
  deferred global `12/46/27`，并保留 #119/#132 ownership boundary。
- Task delta merged：已在 Round 1 合并到 durable docs；本轮 code/schema 修复使实现
  回到现有 SSOT，不产生新的 durable contract，因此没有再次改写 docs。
- Task-history-only content：Round 2 两个 finding 的复现、修复审计、sidecar 清理和
  terminal test/install evidence 保留在本交接与 Phase 2 历史报告中。
- Primary implementation inputs：上述 durable workflow/package contracts。
- Confirmed task-delta inputs：`prd.md` R6/R7/R10/R12、AC2/AC6/AC9，
  `design.md` 3.1、4、5、6、7 与 approved `implement.md`。

## 4. Sidecar 与同步

- 修复前共有精确 12 个 `.bak`：四个安装 root 各包含两个 private route schema
  与一个 package test 的 intermediate backup。
- 三类 backup digest 分别为
  `faf7287bd88ac65710b90317546683f0a6a5a27d96b14100a08cda8bad3c50c9`、
  `8dbd5d0f151d7ffa17386b770dab289b8da6742510c9b2a2f4a1ad5f4ee4ecaf`、
  `701d017b465df3c8f8cc6c8271384ccf09137423998680048457665a16fb244e`。
  每组四份 byte-identical；逐组 diff 只显示 canonical 后续增加的 branch-disjoint
  `not` 与 schema regression。删除了这 12 个已审核生成 sidecar，没有删除其它文件。
- `apply.sh --repo . --all-platforms`：exit 0，`installed=[]`、
  `updated_managed=[]`、`sidecars=[]`；source/installed package validator 与
  ownership validator 均通过。
- Dogfood overlay drift：exit 0，零漂移。

## 5. 验证结果

- Focused runtime：4 tests，exit 0。
- Runtime full：605 tests，13 skipped，exit 0。
- Skill package full：178 tests，exit 0。
- Preset full：45 tests，exit 0。
- Finalizer package：4 tests，exit 0。
- Installed shared real public wrapper：8/8 cases passed；六 actual exits 均先选择
  per-exit schema，再断言 expected exit。
- Source/installed package validation：均 passed；13 active、0 planned、0 legacy，
  global markers 12 invokes / 46 exits / 27 targets。
- Canonical/installed shared/Agents/Codex/Claude/Cursor：五次 `diff -qr` 均 exit 0。
- Upstream ownership：43 frozen / 43 active / 0 removed，exit 0。
- Bash syntax、Python compile、task validate、`git diff --check`：均 exit 0。
- No-write：相对
  `7820a9eeec2a2a75fb52fba156a7211d9f9fb09c` 的 global workflows、upstream
  Finish family、preset overlays 与 `.trellis/scripts/task.py` 均无 diff。
- Fresh clean throwaway：
  `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 ... verify-throwaway-install.sh`
  exit 0；覆盖 public marketplace discovery、local unpublished canonical sample、
  initial install/reapply、`trellis update`、managed hash、`.new/.bak` recovery、
  all-platform distribution、package discovery、production eval 与 real wrapper。
  Repo-external log 为
  `/tmp/guru-118-impl-round2-replacement/throwaway.log`，4,140,723 bytes，
  SHA-256
  `199285e38d288e0d673c2761d4a17a65f10799b1922e11874aa75aca43c2834c`。

## 6. 交给独立 Phase 2 Check

下一轮独立 `trellis-check` 应完整重跑 approved scope，不只重放 focused tests。重点：

1. 以正常 publication entry 从 `prepared` 且无 #117 evidence 尝试
   `published`，必须在 gate checker 阻断；current same-plan
   `verified|not_required` 与 objective `archived|ready` recovery 必须分别通过。
2. 对六 exits 重放 empty/missing/extra/wrong-exit output；只有 published exact
   private marker 可在 pre-execution gate 通过，并检查 post-execution public DTO。
3. 重新确认 #105 transaction/recovery suites、global/upstream/overlay/task.py
   no-write、package byte identity、zero sidecar/cache 与 fresh throwaway。
4. 重新判定 Docs SSOT accuracy、#118-only Issue Scope Ledger 与 #119/#132 exclusion。

实现阶段没有执行 Phase 2 recorder、Branch Review、commit、push、PR、GitHub mutation
或 finish。
