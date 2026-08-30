# #267 pre-tag findings 修复实施计划

## Phase 1: Planning Gates

- [x] fresh 读取 live Issue #267 r19、Issue #311/#312、current `main`、latest GitHub Release、
  `.2` tag object/peeled commit 与 released manifest。
- [x] 在 current code、active `.42` authority 与 archived #312 artifact 上复现三个 finding。
- [x] 编写 `prd.md`、`design.md`、`implement.md` 与 Docs SSOT Plan。
- [ ] 完成 planning-artifacts wording review、normal-scenario qualification、RDT/Architecture
  planning owner routes 与 `guru-approve-task-plan`。
- [ ] 展示完整 approved plan；取得后续明确批准前不运行 `task.py start`。

## Phase 2: Finalizer Platform Preservation

- [ ] 在 canonical Finalizer owner 中实现 manifest platform-selection pure helper。
- [ ] 对三个 selected-platform locators、`all_platforms` 与 canonical closed set 执行完整
  structural/semantic validation。
- [ ] 将 provenance apply argv 从固定 `--all-platforms` 改为 helper 输出。
- [ ] 保持 apply 前 fail-closed、source/target checkout isolation、manifest field allowlist 与
  direct-parent publication lineage 不变。
- [ ] 更新 canonical Finalizer owning tests：fixture parser、argv capture、五个 valid cells 与
  malformed/mismatch zero-call cases。
- [ ] 运行 canonical focused test，确认修复前 `claude` subset case 可复现、修复后 PASS。

## Phase 2: Authority And Historical Artifact Repair

- [ ] 通过 RDT `repair` 将 active `.42` latest-stable current fact 更新为
  `v0.6.15-guru.2` / `.38` / CLI `0.6.15` 与 live tag identities。
- [ ] 通过 Architecture `repair` 更新 `ARCH-CUR-005` 与 `EVD-002`，保留 #275/.10
  historical before-state。
- [ ] 将 #312 archived `implement.md` 的唯一机器绝对路径替换为
  `<business-repository-task-worktree>`。
- [ ] 运行 scoped scan，证明 exact current paths 不再把 `.10` 声明为 latest，且目标 archived
  file 不含 `/Users/`。

## Phase 2: Canonical Projection And Checks

- [ ] 运行：

  ```bash
  trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms --json
  ```

- [ ] 审查 generated name-only diff，只接受 PRD 的 exact file boundary；`.new/.bak` 与
  undeclared sidecar 数量必须为 `0`。
- [ ] 验证 canonical/installed Finalizer runtime 与 tests byte equality。
- [ ] 运行 canonical 与 installed Finalizer package tests。
- [ ] 运行 preset installer、package validator、ownership、registry/consumer graph、mode、
  permission、managed byte parity 与 dogfood overlay drift checks。
- [ ] 运行 task validation、workspace boundary、secret/sensitive-path scan 与
  `git diff --check`。
- [ ] 调用 fresh Architecture `task_impact_sync(stage=phase2)` 与 `guru-check-task`；只消费
  checked typed exit。

## Phase 3: Commit, Review And Publication Preparation

- [ ] 展示 exact stage paths、commit message 与预期 HEAD；取得独立确认后创建 task commit。
- [ ] 对 fresh `origin/main...HEAD` 完整 committed range 执行 independent Branch Review；
  P0/P1/P2/P3 未关闭 finding 必须全为 `0`。
- [ ] 完成 Publication readiness 与 Finalizer；push、PR create、merge 均使用独立副作用确认，
  merge 只接受用户明确的 `合并PR`。
- [ ] PR body 使用 `Refs #267`；不得关闭 #267 或 #311。

## Post-Merge: Exact Candidate Re-Freeze

- [ ] fresh fetch 并验证 local `main`、`origin/main`、GitHub remote main 完全相同；记录
  candidate commit/tree。
- [ ] 验证 `5b3b7bef...`、`21c7da147...`、`3efcce72...` 均为 candidate ancestor。
- [ ] 验证 predecessor `v0.6.15-guru.2` tag object 为 `641ed35e...`、peeled commit 为
  `d907fcc5...`，且 `.3` tag/Release 不存在。
- [ ] 对 `.2` peeled commit 到 candidate 的完整 committed diff 执行 fresh review。
- [ ] 运行 live-derived complete platform × clean/existing matrix，确认 `claude-clean` 与其它
  五个 cells 全部 PASS。
- [ ] 在无 extension source tree 的 installed business repository 完成 Publication/Finalizer
  provenance reprepare full chain，验证 parent platform set 保持不变且 metadata tail 仅改
  provenance。
- [ ] 完成 secret、credential、private-key、signed-URL、machine-path 与 residue-zero scans。

## Release Side-Effect Stops

- [ ] pre-tag gate 全部通过后，展示 candidate SHA/tree、annotated tag message 与 push refspec；
  取得独立确认后才创建/push `v0.6.15-guru.3`。
- [ ] tag-pinned smoke PASS 后，展示 GitHub Release title/body/target/draft/prerelease/assets；
  取得独立确认后才创建 Release。
- [ ] Release live reread通过后，#267 closure 仍使用独立确认。
- [ ] 正式 `.3` 业务仓安装、原 Finalizer 失败路径与错误文件重试全部 PASS 后，#311 才进入
  独立 closure review；任一缺口都保持 OPEN。

## Stop Conditions

- 实现需要修改 Finalizer public API/schema/typed exit/consumer。
- 合法 platform subset 无法由 current installed manifest 唯一恢复。
- RDT 或 Architecture owner 返回 scope、decision、GAP、owner、ADR 或 compatibility change。
- preset apply 产生 exact file boundary 外的 tracked delta、`.new`、`.bak` 或 sidecar。
- source/target checkout 出现 provenance manifest 之外的 mutation。
- `main`、Issue #267 current body、latest Release 或 predecessor tag identity 发生漂移。
- 任一 required check 返回 FAIL、SKIP、stale、unknown/multiple/unmapped exit。
