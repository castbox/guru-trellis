# #118 guru-finalize-task 实施计划

## 1. Gate

- [ ] 运行 `guru-review-contract-wording:planning_artifacts` 并取得 current `pass`。
- [ ] 运行 `guru-approve-task-plan` 的九项 entry checks、provenance review、unusual-scenario
  review 与 AI Review Gate。
- [ ] 展示 `prd.md`、`design.md`、`implement.md` 链接与精确 digests，取得独立
  `post-planning-approval` confirmation。
- [ ] Recorder/checker 返回 `approved` 后才运行 `task.py start`。

## 2. Canonical package

- [ ] 新建 `trellis/skills/guru-team/packages/guru-finalize-task/`。
- [ ] 编写短 `SKILL.md` 与唯一完整 `references/contract.md`。
- [ ] 编写 Interface 1.3 `interface.json`，声明六 input profiles、six exits、consumer
  inputs、thin projections、private artifacts 与 production wrapper。
- [ ] 编写每个 input/output 的 closed schema、aggregate input schema、invocation error
  schema、private gate schema与完整 examples。
- [ ] 编写 package scripts：preview、record、check、execute、invoke。
- [ ] 编写 package contract tests 与 eval corpus/fixtures。

## 3. Transaction engine

- [ ] 从 current #105 closeout helpers 抽取单一 internal engine boundary，禁止复制
  plan/PR/projection/archive/ready 实现。
- [ ] 增加 side-effect-free preview command，并证明 dry-run/formal same bytes/digest。
- [ ] 增加 semantic gate recorder/checker，绑定 AI review、exact confirmation、plan、HEAD、
  actual exit 与 freshness。
- [ ] 增加 state-aware transition executor；machine state 只形成 facts，不选择 route。
- [ ] 在 content push 后、PR/archive 前停止并产生 verification facts。
- [ ] 消费 #117 owner-checked verified/not-required evidence 后恢复同一 plan。
- [ ] 保持 legacy `cmd_finish_work` 与 wrappers 的 current observable behavior，内部复用同一
  engine。

## 4. Interface graph 与 additive distribution

- [ ] 把 #116 `ready` consumer binding 从 planned seed 收敛到 #118 concrete profile 与
  target-owned authoring example。
- [ ] 把 #117 `verified`、`not_required` consumer bindings 收敛到 #118 concrete profiles。
- [ ] 把 #118 `verification_required`、`publication_review_stale`、self re-entry、published、
  blocked projections 绑定到唯一 consumers。
- [ ] 更新 canonical registry、extension inventory、dispatcher command inventory、schema
  inventories、active closure/cardinality assertions。
- [ ] 更新 preset installer 的 additive package/discovery copy 与 managed hash inventory。
- [ ] 不修改 global Finish route、upstream Finish assets、overlay cleanup surface。

## 5. Docs SSOT

- [ ] 逐项执行 `design.md` 的唯一 Docs SSOT Plan。
- [ ] 更新 package contract 与 durable spec ownership/I/O/eval 状态。
- [ ] 更新 repository/preset/workflow README 的导航、安装与 #119/#132 handoff。
- [ ] 对 global workflow 与 upstream Finish assets 执行 no-diff assertion。
- [ ] Phase 2 记录 durable docs 与 task delta 的 reconciliation evidence。

## 6. Tests

- [ ] 运行 `guru-finalize-task/tests/test_contract.py`。
- [ ] 运行 `trellis/skills/guru-team/tests/test_skill_packages.py`。
- [ ] 运行 `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` 全量测试。
- [ ] 运行 preset installer Python tests 与 ownership validator tests。
- [ ] 执行 source/installed contract discovery 并核对六 profiles、six exits、private assets。
- [ ] 执行 shared/Codex/Claude/Cursor production eval，核对 byte-identical corpus、trusted
  root、input protocol、unsupported/unavailable 与 adapter parsing。
- [ ] 核对 actual-exit schema selection 发生在 `expected_exit` assertion 之前。
- [ ] 运行 #105 failure/recovery matrix 与 2026-07-03、2026-07-04、#100 regressions。
- [ ] 禁止新增 current authority 排除的 fault/security/concurrency tests。

## 7. Dogfood 与 clean installation

- [ ] 运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`。
- [ ] 检查每个 `.new/.bak`，记录来源与处置，禁止静默覆盖用户内容。
- [ ] 运行 `check-dogfood-overlay-drift.sh` 并取得零 drift。
- [ ] 从 clean throwaway repo 验证 workflow marketplace index、init、preview、switch。
- [ ] 验证 preset initial install/reapply、Guru runtime、package、schemas、scripts executable、
  shared/Codex/Claude/Cursor discovery copies。
- [ ] 运行 Trellis update，核对 official files 保持 upstream ownership，Guru files 保持
  managed provenance。
- [ ] 构造 managed previous version 与 unknown local edit 两条正常升级路径，分别核对
  `.bak` 与 `.new`。
- [ ] 从 clean installed copy 执行 contract discovery、public wrapper eval 与 finalizer
  dry-run fixture，禁止用当前仓库已安装副本替代。

## 8. Phase 2 与 publication

- [ ] 使用 Trellis implement sub-agent 实施；主会话只协调 scope、spec、整合与提交。
- [ ] 使用 Trellis check sub-agent 执行 Phase 2 全量检查与 Docs SSOT reconciliation。
- [ ] 主会话复核所有 findings，修复后重复完整 affected validation。
- [ ] 运行 `guru-create-task-commit` semantic gate，展示 exact commit plan/digest并取得
  mandatory confirmation。
- [ ] 使用独立 Branch Review agent 覆盖 `origin/main...HEAD`，实现者身份不得复用。
- [ ] 关闭全部 P0-P3 current-scope findings，更新 review gate 与 scope ledger evidence。
- [ ] 运行 publication review，PR title/body 使用中文，只有 `Closes #118`。
- [ ] 正式 finalization 前展示 immutable closeout plan、exact digest 与全部副作用，取得
  mandatory confirmation。
- [ ] 完成 push、唯一 Draft PR、archive transaction、三方 HEAD 一致、draft-to-ready、
  Issue #118 closeout；保持 #115/#119/#132/#105 状态不变。

## 9. Checkpoint 与 rollback

- Planning checkpoint：`status=planning`，只含 task-local planning artifacts。
- Implementation checkpoint：`status=in_progress`，不得产生 GitHub/remote closeout 副作用。
- Pre-commit checkpoint：working tree 只含 task scope，full tests 与 clean install evidence
  current。
- Pre-publication checkpoint：task commit、Branch Review、publication review 全部绑定同一
  HEAD。
- Rollback：合并前只回退本 branch 的新 package、runtime delegate、inventory、docs 与
  generated dogfood copies；禁止触碰 main、#117 worktree、用户并行改动或外部 Issue state。

## 10. Completion record

实施过程中在本章节追加简短 checkpoint，禁止复制 test transcript 或 private runtime
facts。完整机器证据写入 task-local gate artifacts 与 JSONL。
