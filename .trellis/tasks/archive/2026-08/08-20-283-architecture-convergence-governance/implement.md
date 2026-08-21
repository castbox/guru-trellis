# #283 实施计划

## 1. Architecture Baseline SSOT 生命周期闭环

- [ ] 先实现“Guru Team 方法论维度 + 项目 Architecture Baseline 语义维度”的交叉合同，确保每个标准 task mandatory 进入 Architecture owner，架构相关 task 缺任一 authority identity 时失败关闭。
- [ ] 先在 canonical workflow/Architecture owner 中闭合 Planning 读取 current baseline/设计宪法、implementation discovery re-entry、Phase 2 满足性检查、Branch Review 独立复核、Publication/Acceptance current 消费与 promotion 回补顺序。
- [ ] 明确 Architecture Baseline 是业务仓库唯一架构 SSOT；task-local planning/gate/contribution 只保存最小影响或候选变化，不复制 shared architecture 正文。
- [ ] 定义 ADR 触发边界：只有 architecture decision、原则权衡/例外、GAP 生命周期、owner/single-writer 或 compatibility exit 变化才形成 ADR candidate；no-impact/current-conforming task 不创建 ADR。
- [ ] 让 reviewed promotion 更新 current baseline/version/history/ADR/decision/GAP/owner，并验证新的 current identity 能被下一 task Planning 读取。

## 2. Contract 与 schema 2.0

- [ ] 在 canonical `guru-maintain-architecture-baseline` package 新增闭合 2.0 aggregate/profile/output、semantic owner、architecture contribution 与 project architecture check schemas。
- [ ] 保持 stable Skill、四 profile、七 exit 与 consumer ids；删除旧 1.0 schema/example/selector，新增 2.0 schema 并原子切换所有 producer、consumer 和 projection。
- [ ] 修正 current `SKILL.md`/contract，使其只描述 Architecture owner，不保留与 workflow mode selector 混杂的无关正文。
- [ ] 更新 Interface active selector、consumer contracts、authoring seed、examples、errors 和 eval inventory；公共图基数保持 21 Skills/89 exits。

## 3. Semantic owner 与 deterministic runtime

- [ ] 实现设计宪法 authority locator/version-or-content identity 读取、最小五原则 projection 与 authority separation gate。
- [ ] 实现 `target_native|legacy_boundary_convergence|dedicated_refactor_slice` 互斥判断，以及独立 `no_architecture_impact` 快速路径。
- [ ] 实现 architecture impact、single-writer/compatibility exit、parallel scope、GAP lifecycle 与 before/after convergence owner result。
- [ ] 实现 task-local Architecture change contract：同时绑定 Guru public identity、项目 baseline/change-contract identity、requirement/design/evidence、required concern set、applicability、contribution/ADR/review/promotion 与 expected current identity。
- [ ] 对适用项目字段 missing/empty/stale、无法证明 `not_applicable` 或与 requirement/design/code/diff/evidence 不一致的状态失败关闭；no-impact 只保留 baseline/task/stage/reason。
- [ ] runtime 只验证闭合 input/result/projection、locator、freshness、check result 和 unique consumer；不决定原则适用性、冲突、GAP 接受或 semantic pass。
- [ ] runtime 只接受 2.0；旧或缺失 schema identity 明确拒绝。current 2.0 constitution/baseline/contribution identity stale 稳定返回 `sync_required`。

## 4. Project architecture check integration

- [ ] 定义项目检查 descriptor/result 的通用 schema 和调用合同，不加入语言/框架 checker 或业务阈值。
- [ ] 覆盖 `pass|fail|unverified`、applicability、rule/decision/GAP refs、before/after、evidence/unavailable/freshness。
- [ ] mandatory applicable check 缺失/过期走 `contract_incomplete|sync_required`；新增/恶化偏移走 `fitness_regression`。

## 5. Workflow 与阶段消费者

- [ ] 在 canonical/dogfood workflow 明确 Planning、implementation discovery、Phase 2、Branch Review、Publication、Acceptance/Finish 的 Architecture invocation 顺序和唯一 typed router。
- [ ] 更新 `guru-approve-task-plan` 对 current 设计宪法/impact 的 Planning 消费。
- [ ] 更新 `guru-check-task` 对项目检查和 before/after 的 Phase 2 消费。
- [ ] 更新 `guru-review-branch` 对完整 committed diff 的独立设计宪法/收敛复核；不得复用 Phase 2 结论代替 review。
- [ ] Publication/Acceptance/Finish 仅由 workflow current/sync router 接入，不修改或吸收 #261/#248 owner 的业务语义。
- [ ] Publication 明确拒绝 missing/stale/`architecture_conflict`/`contract_incomplete`/`fitness_regression`；Finish 要求 reviewed promotion 或 current no-change proof。

## 6. Contribution、ADR、review、promotion 与 Docs SSOT

- [ ] 调用 Architecture `task_impact_sync`，创建 #283 隔离 contribution，绑定 `.37` baseline、设计宪法 projection、change path、GAP/owner/check 影响，以及本 task 引入的 architecture decision/ADR candidate。
- [ ] 调用 RDT `task_impact_sync`，创建 `docs/requirements-design-test-contributions/283-architecture-convergence-governance/` 五件套并完成 traceability。
- [ ] review 前不直接改 shared current；Branch Review pass 后由各 owner 执行 promotion，更新下一 current-main RDT/Architecture authority、ADR/history 边界，并以新的 current identity 重新执行一次下游 Planning 读取 smoke。
- [ ] Architecture promotion 绑定 expected current baseline identity，由唯一 owner 串行执行；live baseline 已推进时返回 `sync_required`，不得覆盖。
- [ ] promotion diff 进入最终 reviewed HEAD，并重新通过 Phase 2、task commit 与独立 Branch Review；实现测试通过但 contribution/ADR/promotion 未完成时禁止 Publication/Finish。
- [ ] 验证 task A promotion 后 task B 旧 identity 返回 `sync_required`，且两个 task 不竞争同一 GAP、owner 或 current authority。
- [ ] `.trellis/spec` 只同步 locator/identity/消费/freshness；不复制设计宪法或业务 Architecture 正文。

## 7. Canonical、dogfood、installed 与平台同步

- [ ] 修改 canonical package、workflow、spec、registry/manifest/preset/README source。
- [ ] 运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo .` 同步 `.trellis/guru-team` 和 Shared/Codex/Claude/Cursor projections。
- [ ] 运行 reapply、ownership、installed manifest、platform parity、overlay drift 与 recursive `.new/.bak` 检查，最终 sidecar 为零。

## 8. Tests 与 evals

- [ ] package tests 覆盖四 profile、七 exit、2.0 schema closure、旧 schema 零库存/旧输入拒绝、unique consumer 与 public/private 最小性。
- [ ] semantic eval 覆盖五项原则最小消费、三路径互斥、no-impact 零负担、冲突/不足/stale/regression 四类 route。
- [ ] project-check tests 覆盖 applicable pass/fail/unverified、fresh/stale、GAP/decision linkage、before/after regression。
- [ ] workflow tests 覆盖 Planning、Phase 2、Branch Review、Publication、Acceptance/Finish route closure 和 promotion 后复核。
- [ ] isolation tests 覆盖两个 task contribution locator 分离、shared current review 前不可写、single-writer 与 compatibility exit。
- [ ] lifecycle tests 覆盖 promoted baseline/ADR/decision/GAP/owner identity 被后续 task Planning 读取，以及 no-impact/current-conforming task 不创建 ADR/contribution。
- [ ] 使用项目中立 fixture 固定覆盖 10 场景：no-impact、target-native、legacy-boundary convergence、dedicated refactor slice、scope expansion、fitness regression、parallel stale、unpromoted contribution、next-task consumption、missing external evidence。
- [ ] 断言五项设计宪法只以 identity/short name 投影，不出现 required score/verdict checklist；断言 fixture 不包含 Afizzy 私有规则。

## 9. 验证命令与边界

- [ ] 运行 Architecture package `tests/test_contract.py`、runtime command/public wrapper 与 package eval。
- [ ] 运行 `check-skill-packages.sh`、`run-skill-evals.sh`、workflow/public graph/schema/consumer closure tests。
- [ ] 运行 preset apply/reapply、dogfood overlay drift、ownership/manifest/platform parity 及各自直接绑定的 Python tests。
- [ ] 运行 `bash -n`、Python compile/unit tests、JSON schema/example validation、`git diff --check` 与 `task.py validate`。
- [ ] 通过 `guru-verify-extension-installation` 完成一个代表性 clean standalone install 与 installed runtime/eval/workflow smoke；不执行 #267 完整多平台 Release matrix。

## 10. Phase 2 与收尾

- [ ] 用户对本计划进行后续明确确认后才执行 `task.py start`。
- [ ] `trellis-before-dev` 注入本 task 的 curated implement context；implementation sub-agent 仅实施 approved scope。
- [ ] `guru-check-task` 完成完整 Phase 2；finding 修复后全量重跑。
- [ ] `guru-create-task-commit` 只 stage #283 文件；独立 `guru-review-branch` 覆盖 `origin/main...HEAD` 完整 committed diff。
- [ ] Publication/Finalizer/PR 只关闭 #283；full merge gate 后仅询问 `合并PR`。
- [ ] merge 后验证 PR merged、Issue closed、reviewed head/merge 到达 live main，并完成 Finalizer/archive/history/worktree/branch cleanup 与四方 main convergence。

## 11. 受控文件分区与回滚点

- Canonical Architecture package：`trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/`。
- Global workflow/spec：`trellis/workflows/guru-team/`、`trellis/presets/guru-team/spec/` 与 dogfood `.trellis/workflow.md`、`.trellis/spec/`。
- 阶段消费者：只修改 `guru-approve-task-plan`、`guru-check-task`、`guru-review-branch` 的 Architecture 消费合同及其 projections；不扩张下游 Issue owner。
- Docs：#283 RDT/Architecture contribution；promotion 后的 current versioned docs/README/history。
- Installed/platform copies：只由 canonical preset apply 生成。
- 回滚以完整 2.0 schema/runtime/workflow/projection 和 Docs promotion 两个逻辑层为界；不得局部恢复旧 schema 或形成 dual contract，tag/Release 始终不在回滚范围。
