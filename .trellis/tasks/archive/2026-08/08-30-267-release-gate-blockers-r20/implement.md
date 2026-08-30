# #267 r20 Release Gate blocker 修复实施计划

## Phase 1: Planning Gates

- [x] fresh 读取 live Issue #267 r20、Issue #311/#312、current `main@5650df47...` 与目标
  tag/Release absence。
- [x] 读取 standalone verifier failure evidence、`claude-clean` closeout log 与 diagnostic manifest。
- [x] 在 current matrix runner 与 provenance validators 上定位两个 blocker 的唯一执行路径。
- [x] 编写 `prd.md`、`design.md`、`implement.md` 与 Docs SSOT Plan。
- [x] 完成 `guru-review-contract-wording:planning_artifacts`。
- [x] 完成 `guru-maintain-architecture-baseline:task_impact_sync(stage=planning)` 并取得 fresh
  `baseline_current/no_architecture_impact`；其它 typed exit 自动返回其 owner。
- [x] 完成 `guru-approve-task-plan` 并取得 `approved`。
- [x] 展示完整 approved plan；用户确认前不运行 `task.py start`，不编辑 implementation surface。

## Phase 2: Exact Before-Tag Resolution

- [x] 在 canonical matrix runner 增加 before-tag local-resolve / exact-fetch / re-resolve helper。
- [x] 限制 fetch 为 `--no-tags --depth=1 origin refs/tags/X:refs/tags/X`。
- [x] 保持 failure stage 为 `pre-matrix`、cell id 为 null、matrix cell count 为零。
- [x] 增加 local bare remote fixtures，覆盖 remote-present、local-present、remote-missing 与 malformed tag。
- [x] 更新 standalone verifier focused test，证明 exact-SHA shallow source path能进入 canonical matrix
  precondition，而不是依赖 clone 自动携带 tag。
- [x] 运行 focused matrix/upgrade 与 verifier tests。

## Phase 2: Provenance Action Transition

- [x] 在 canonical Finalizer owner 增加 closed files-container comparator。
- [x] 在 canonical Publication owner 增加同语义 package-local comparator。
- [x] 只接受 `skill_packages.files` 与 `overlays.files` 中逐条 `installed -> unchanged`。
- [x] 删除 action 后要求条目身份、顺序、长度与其余字段完全相同。
- [x] 保持 `PROVENANCE_TAIL_ALLOWED_FIELDS` 的无条件 allowlist不包含 files container。
- [x] 更新两套 owning tests，覆盖 positive 双容器与 action/content/ordering/length negative matrix。
- [x] 保持 existing source binding、manifest-only path、clean checkout、direct parent 与 publication
  identity tests全部通过。

## Phase 2: Canonical Contracts And Projection

- [x] 更新 Finalizer contract 与 Publication contract，写明 closed action transition。
- [x] 更新 quality guidelines 与 companion scripts，写明 exact before-tag fetch 和 safe reapply action
  classification。
- [x] 运行 canonical focused tests。
- [x] 执行：

  ```bash
  trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms --json
  ```

- [x] 审查 generated name-only diff，只接受 PRD exact file boundary。
- [x] `.new`、`.bak`、未知 sidecar 与 owner-private residue 数量全部为 `0`。
- [x] 验证 canonical/installed Finalizer 与 Publication runtime/tests/contracts byte一致。
- [x] 运行 dogfood overlay drift、source/installed package validator、registry/consumer graph、mode、
  permission、managed-byte parity 与 platform projection checks。

## Phase 2: Task Check

- [x] 运行 matrix/upgrade contract tests、verifier tests、Finalizer tests、Publication tests 与 preset
  installer tests。
- [x] 运行 task validation、workspace boundary、secret/sensitive-path scan 与 `git diff --check`。
- [x] fresh 调用 Architecture `task_impact_sync(stage=phase2)`；implementation boundary 未扩张时应保持
  `baseline_current/no_architecture_impact`。
- [x] 调用 `guru-check-task`；只消费 checked typed exit。
- [ ] 任一 FAIL、SKIP、stale、unknown/multiple/unmapped exit 阻断 task commit。

## Phase 3: Commit And Independent Review

- [ ] 展示 exact stage paths、commit message 与预期 HEAD；取得独立确认后调用
  `guru-create-task-commit`。
- [ ] 对 fresh `origin/main...HEAD` 完整 committed range 执行 independent Branch Review；
  P0/P1/P2/P3 未关闭 finding 数量全部为 `0`。
- [ ] 完成 Publication readiness 与 Finalizer。
- [ ] push、PR create、merge 分别使用当前对话中的独立副作用确认；merge 只接受用户明确的
  `合并PR`。
- [ ] PR body 使用 `Refs #267`，不关闭 #267、#311 或 #312。

## Post-Merge: Fresh Exact Candidate

- [ ] fresh fetch 并验证 local `main`、`origin/main` 与 GitHub remote main 相同；记录 candidate
  SHA/tree。
- [ ] 验证 `5650df47...`、`5b3b7bef...`、`21c7da147...`、`3efcce72...` 均为 candidate
  ancestor。
- [ ] 验证 predecessor `v0.6.15-guru.2` identity 不变，`.3` tag/Release 仍不存在。
- [ ] 对 `.2` peeled commit 到 candidate 的完整 committed diff执行 fresh review。
- [ ] 从 exact candidate 运行 standalone verifier；确认不再返回
  `pre_matrix_before_tag_unavailable`。
- [ ] 运行六个 platform/scenario matrix cells；确认 `claude-clean` 与其余五个 cell 全部 PASS，
  且不再返回 `provenance_tail_manifest_fields_outside_allowlist`。
- [ ] 在不含 extension source tree 的 installed business repository 完成 Publication/Finalizer
  ready、reprepare、execute、Draft PR、archive、Ready 与 terminal chain。
- [ ] 完成 secret、credential、private-key、signed-URL、machine-path 与 residue-zero scans。

## Release Side-Effect Stops

- [ ] pre-tag gates 全部通过后，展示 candidate SHA/tree、annotated tag message 与 push refspec；
  取得独立确认后才创建并 push `v0.6.15-guru.3`。
- [ ] tag-pinned smoke PASS 后，展示 GitHub Release title/body/target/draft/prerelease/assets；取得独立
  确认后才创建 Release。
- [ ] Release live reread通过后，#267 closure 使用独立确认。
- [ ] 正式 `.3` 业务仓安装、原 #311 Finalizer failure path 与错误文件重试全部 PASS 后，#311
  才进入 closure review；证据不完整时保持 OPEN。

## Stop Conditions

- 实现需要修改 public Skill I/O、schema、typed exit、consumer 或 Release identity。
- before-tag fetch 不能绑定一个 exact immutable tag ref。
- safe action comparator 需要接受 `installed -> unchanged` 之外的 changed transition。
- RDT 或 Architecture owner 返回 requirement、decision、GAP、owner、single-writer、ADR 或
  compatibility change。
- preset apply 产生 exact file boundary 外的 tracked delta、`.new`、`.bak` 或未知 sidecar。
- source/target checkout 出现 extension manifest 之外的 mutation。
- live #267 authority、main、predecessor Release 或 target mapping 漂移。
- 任一 required check 返回 FAIL、SKIP、stale、unknown/multiple/unmapped exit。
