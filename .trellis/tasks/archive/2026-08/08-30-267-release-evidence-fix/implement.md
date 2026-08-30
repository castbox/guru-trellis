# #267 post-merge lifecycle authority evidence 修复执行计划

## Phase 0：Recovery Workspace

- [x] Fresh fetch 并确认 `main`、`origin/main`、source HEAD 均为 `a41b8a34`。
- [x] Fresh reread live Issue #267 r19、PR #315、#311 与 GitHub Release/tag 状态。
- [x] 创建 branch `codex/267-release-evidence-fix`、独立 worktree 与 active planning task。
- [x] `issue-scope-ledger.json` 固定 `close_issues=[]`，#267/#311/#312 只作 authority reference。

## Phase 1：Planning

- [x] 编写 `prd.md`、`design.md`、`implement.md`。
- [ ] 完成 planning-artifacts wording review，所有 retained controlled-term hit 均有确定性分类。
- [ ] 完成 `guru-maintain-architecture-baseline:task_impact_sync(stage=planning)`。
- [ ] 完成 `planning_scenario_set` qualification。
- [ ] 完成 `guru-approve-task-plan` 八维语义审查。
- [ ] 展示 checked approved plan 与 task activation 副作用，取得确认后启动 task。

## Phase 2：Implementation And Check

- [ ] 只迁移以下两个 current authority 文件的 reviewed diff：
  - `docs/architecture/evidence/current-evidence.md`；
  - `docs/test/versions/current-main-0.6.5-guru.42/test-plan.md`。
- [ ] 验证 archived `implement.md` 与 `HEAD` blob identity 相同。
- [ ] 执行 exact-path、diff hygiene、live Issue/PR/main/tag/Release、ancestor 与 authority scan。
- [ ] 执行 preset `81/81`、canonical verifier `17/17`、installed verifier `17/17`。
- [ ] 完成 fresh Architecture Phase 2 与 `guru-check-task` 九维审查。

## Phase 3：Commit And Review

- [ ] 展示精确 stage paths 与中文 Conventional Commit message，取得确认后创建 task commit。
- [ ] 对 `origin/main...HEAD` 完整 committed range 执行 distinct independent Branch Review。
- [ ] 未关闭 P0/P1/P2/P3 finding 均为零后进入 Publication readiness。

## Publication Boundary

- [ ] 单独展示并确认 push。
- [ ] 单独展示并确认 PR create；PR body 只使用 `Refs #267`。
- [ ] 单独展示并确认 Finalizer 与 merge。
- [ ] merge 后重新同步 main、冻结 exact candidate SHA/tree，并重跑 #267 十三项 pre-tag gates。
- [ ] 本 task 不创建 tag、GitHub Release，不关闭 #267/#311，不清理旧 worktree。
