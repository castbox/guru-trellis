# #267 after_archive hook fail-closed Release Gate 修复实施计划

## Phase 1: Planning Gates

- [ ] fresh 核对 live #267/#311/#312、remote `main@59d25f1c...`、required ancestors 与 `.3`
  tag/Release absence。
- [ ] 核对 retained matrix failure evidence、current Finalizer runtime、tests 与 installed fixture。
- [ ] 完成 `prd.md`、`design.md`、`implement.md` 与 Docs SSOT Plan。
- [ ] 完成 `guru-review-contract-wording:planning_artifacts`，只接受 checked `pass`。
- [ ] 完成 `guru-maintain-architecture-baseline:task_impact_sync(stage=planning)`，只让 fresh
  `baseline_current` 进入 plan approval。
- [ ] 完成 `guru-approve-task-plan`，只让 checked `approved` 进入 workflow plan presentation。
- [ ] 展示 approved plan；下一条明确确认前不运行 `task.py start`，不编辑 implementation surface。

## Phase 2: Canonical Runtime And Tests

- [ ] 在 canonical `finalization_preview_context()` entry 调用
  `official_after_archive_hook_state(root)`，位置固定在 eval helper 之前。
- [ ] 保留 `prepare_closeout()` 中现有 preflight。
- [ ] 增加 eval-staging preview focused test，断言稳定 error payload、未返回 eval context、sentinel
  不存在。
- [ ] 增加 execute-path focused test，断言相同 payload 与 archive/push/PR/Ready mutation 零调用。
- [ ] 保持 hook missing/empty 与 direct caller regression 通过。
- [ ] 运行 canonical focused tests：

  ```bash
  python3 -m unittest \
    trellis.skills.guru-team.packages.guru-finalize-task.tests.test_contract
  ```

  若 package 路径不能作为 Python module 导入，则使用该 package current test runner 的语义一致精确命令，
  并记录实际命令与结果。

## Phase 2: Contract Check And Projection

- [ ] 更新 canonical Finalizer contract，写明 common preview/execute hook preflight 与 direct-path defense。
- [ ] 执行：

  ```bash
  trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms --json
  ```

- [ ] 审查 generated name-only diff；只接受 PRD/Design 定义的 exact file boundary。
- [ ] 验证 canonical 与 installed Finalizer runtime/test/contract projection 一致。
- [ ] `.new`、`.bak`、未知 sidecar 与 owner-private residue 数量全部为 `0`。

## Phase 2: Validation And Semantic Check

- [ ] 运行 canonical 与 installed Finalizer focused/full suites。
- [ ] 运行 `verify_installed_closeout.py` owning regression 或其 package test entry，证明现有 hook fixture
  不做语义放宽。
- [ ] 运行 preset installer、dogfood overlay drift、source/installed package validator、registry、
  consumer graph、managed-byte parity、mode、permission 与 recursive sidecar-zero checks。
- [ ] 运行 task validation、workspace boundary、secret/sensitive-path scan 与 `git diff --check`。
- [ ] fresh 调用 Architecture `task_impact_sync(stage=phase2)`；scope 未扩张时必须保持
  `baseline_current/no_architecture_impact`。
- [ ] 调用 `guru-check-task` 并只消费 checked typed exit。
- [ ] 任一 FAIL、SKIP、stale、unknown、multiple 或 unmapped exit 阻断 task commit。

## Phase 3: Commit And Independent Review

- [ ] 展示 exact stage paths、commit message 与预期 HEAD；取得独立确认后调用
  `guru-create-task-commit`。
- [ ] 对 fresh `origin/main...HEAD` 完整 committed range 执行 independent Branch Review；
  P0/P1/P2/P3 未关闭 finding 数量全部为 `0`。
- [ ] 完成 Publication readiness 与 Finalizer。
- [ ] push、PR create、merge 分别使用当前对话中的独立副作用确认；merge 只响应明确的
  `合并PR`。
- [ ] PR body 使用 `Refs #267`；不得关闭 #267、#311 或 #312。

## Post-Merge: Fresh Exact Candidate

- [ ] fresh 验证 local main、remote main 与 GitHub main 收敛后记录新 candidate SHA/tree。
- [ ] 验证新 candidate 含 `59d25f1c...`、`5b3b7bef...`、`21c7da147...` 与
  `3efcce72...` 祖先。
- [ ] 验证 predecessor `.2` 不变，`.3` tag/Release 仍不存在。
- [ ] 对 `.2` peeled commit 到新 candidate 的完整 committed diff执行 fresh review。
- [ ] 从新 candidate 重跑 standalone verifier 与六个 platform/scenario matrix cells；六个 cell 必须
  全部 PASS，`claude-clean` 不再返回 after-archive hook blocker。
- [ ] 在 installed business repository 完成 Publication/Finalizer full chain、#312 boundary regression、
  secret scan、sidecar 与 residue-zero checks。
- [ ] 任一失败使 candidate freeze 失效；修复后从新的 fresh remote main 重新开始。

## Release Side-Effect Stops

- [ ] pre-tag gates 全部通过后，展示 candidate SHA/tree、annotated tag message 与 exact push refspec；
  取得独立确认后才创建并 push `v0.6.15-guru.3`。
- [ ] tag identity 与 tag-pinned smoke PASS 后，展示 Release title/body/target/draft/prerelease/assets；
  取得独立确认后才创建正式 Release。
- [ ] Release live reread 通过后，#267 closure 使用独立确认。
- [ ] 正式 `.3` business-repository reinstall、#311 原错误路径与错误文件重试全部 PASS 后，#311
  才进入独立 closure review。

## Stop Conditions

- 实现要求改变 public Skill I/O、schema、typed exit、consumer、owner、Release identity 或 Issue closure
  语义。
- 修复要求删除 `prepare_closeout()` direct-path preflight、绕过 installed fixture 或接受非空 hook。
- RDT 或 Architecture owner 返回 requirement、decision、GAP、owner、single-writer、ADR、compatibility
  change、contract incomplete、conflict 或 regression。
- preset apply 产生 exact boundary 外的 tracked delta、`.new`、`.bak` 或未知 sidecar。
- live #267 authority、main、predecessor Release 或 target mapping 漂移。
- 任一 required check 返回 FAIL、SKIP、stale、unknown、multiple 或 unmapped exit。
