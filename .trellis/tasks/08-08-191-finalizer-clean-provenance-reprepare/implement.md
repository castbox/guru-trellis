# 实施计划

## 1. 入口与 SSOT

- [x] 重新确认当前 worktree、task.json、Issue #191 scope ledger 与 clean base；保留 #179 隔离边界。
- [x] 更新适用 Docs SSOT 与 README 约定，并保持 canonical/dogfood/platform 生成副本一致。
- [x] 将本文件列出的 spec/docs 作为 `check.jsonl`/`implement.jsonl` 唯一 planning context，不写 implementation-handoff.md。

## 2. Runtime 与 contract 实现

- [x] 在 canonical runtime 增加 provenance-tail prepare/validate executor：detached clean checkout、canonical preset apply、唯一允许 manifest-field diff、sidecar/ownership/platform/drift/task-content checks、single tail guard、FF-only precondition。
- [x] 扩展 Finalizer closeout plan/preview/semantic input 的 reviewed/publication identity 与 pre-PR state machine；实现 supersede + cleanup 的 owner-private runtime 生命周期，保持授权只在当前对话。
- [x] 更新 Verifier source/target identity binding，区分 reviewed bytes 与 publication ref/PR head；保留 dirty/mutable/mismatch fail-close。
- [x] 检查 `guru-create-task-commit` 的 reviewed identity projection，确保 metadata-tail 不改 reviewed content token，也不触发重复 Phase 2/Branch Review/Publication semantic review。
- [x] 为 `reprepare_required` 增加 additive reason schema id 与迁移说明，保留 stable exit 和既有 `archive_month_changed` 值。

## 3. Canonical、安装与平台同步

- [x] 确认 canonical workflow 与 dogfood `.trellis/workflow.md` 无需改图，保持 thin markers/唯一 consumer。
- [x] 同步 registry、Skill interfaces/schemas/examples/tests、preset manifest/overlay 与 shared/Codex/Claude/Cursor copies。
- [x] 更新 README、workflow/preset docs、spec 与 config/schema，明确 update/upgrade/reapply 顺序、zero sidecar 与 remote exact-ref 证据。

## 4. 验证与受控回归

- [x] 运行 package contract/registry/interface tests、runtime unit/integration、`git diff --check`、JSON/schema/compile checks。
- [x] 用独立 throwaway repo 验证 marketplace init/workflow preview-switch、preset initial/reapply、platform equality、update/reapply、`.new/.bak`/sidecar zero。
- [x] 用受控 fixture 重演：reviewed HEAD push -> `verification_required` -> dirty/stale manifest rejection -> automatic `reprepare_required` -> clean metadata-tail -> new plan/confirmation -> exact-ref verification；未读取 #179 真实资源。
- [x] 重新生成 current-bytes Phase 2 evidence；执行 `guru-check-task` semantic gate，确认完整 diff、Docs SSOT、acceptance 与 non-goals。

## 5. Commit、独立 Review、Publication、Finalizer

- [ ] 仅 stage #191 task scope，运行 `guru-create-task-commit` 并绑定 reviewed content head。
- [ ] 由独立 Branch Review 覆盖完整 `origin/main...HEAD`，发现修复后重新 review；不复用旧 review 证据。
- [ ] 运行 Publication Review，确认中文 PR、只 `Closes #191`、验证/安全/部署影响真实完整；随后进入 Finalizer。
- [ ] Finalizer 执行 clean provenance tail、pre-PR reprepare、exact remote verification、Draft PR/archive/Ready；Issue #191 在 merge 前保持 open。
- [ ] Finalizer/Publication/Branch Review 最终证据均为当前 HEAD，记录未覆盖的外部门禁，不触碰 #179。

## 6. Required context/spec files

```text
.trellis/spec/workflow/index.md
.trellis/spec/workflow/workflow-contract.md
.trellis/spec/workflow/companion-scripts.md
.trellis/spec/workflow/data-contracts.md
.trellis/spec/workflow/quality-guidelines.md
.trellis/spec/workflow/skill-package-contract.md
.trellis/spec/preset/index.md
.trellis/spec/preset/installer.md
.trellis/spec/preset/overlay-guidelines.md
.trellis/spec/preset/upstream-ownership.md
.trellis/spec/docs/index.md
.trellis/spec/docs/public-docs.md
```
