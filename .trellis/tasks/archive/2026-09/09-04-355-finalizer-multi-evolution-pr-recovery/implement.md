# #355 实施计划

## Phase 1: Planning Gates

- [x] 读取 live Issue #355、`origin/main` 和 Finalizer canonical contract/runtime。
- [x] 确认 #342/#344/#347/#350/#353 已在当前基线，不吸收其历史 task 实现。
- [ ] 完成 planning contract wording review 与 Docs SSOT Plan 检查。
- [ ] 完成 Architecture `task_impact_sync(stage=planning)`；验证
  `no_architecture_impact` 假设。
- [ ] 完成 normal-scenario 与 solution-mechanism qualification。
- [ ] 完成 `guru-approve-task-plan` 并激活 task 进入 Phase 2。

## Phase 2: Implementation

1. 通过 `trellis-before-dev` 重新读取 workflow、Finalizer contract、data-contract
   和 preset/投影规范。
2. 在 canonical Finalizer runtime 中追踪旧 transaction 的读取、provenance-tail
   分类、base-evolution 比较和 current-plan recovery 调用顺序。
3. 增加最窄的复合拓扑判定：先从当前 HEAD 获取唯一 direct parent，验证该 parent
   到当前 HEAD 是合法 provenance tail，再以该 parent 作为 base-evolution 比较端点。
4. 保持旧 transaction 非 HEAD 字段和 live PR/remote/Publication 事实的严格绑定；
   只在合法拓扑下复用现有 strict-ancestor recovery 或 reprepare route。
5. 在首个剩余 mutation 前持久化 current-plan transaction，并验证 interrupted
   retry 不重复 push、PR edit/create、archive 或 Ready。
6. 仅当行为合同真实变化时更新 canonical Finalizer references 和直接命中的
   workflow spec；保持 public schema/DTO/typed exit 不变优先。
7. 运行 preset apply，核对所有声明平台投影与 dogfood 无漂移。

## Validation

- canonical `guru-finalize-task` targeted tests。
- installed/preset Finalizer package tests与对应 runtime contract tests。
- real-topology composed base-evolution plus provenance-tail integration regression。
- invalid parent/path/manifest/business/multi-tail/identity/scope/remote negative cases。
- `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`。
- canonical、installed、dogfood 与平台投影的 byte/parity/ownership 检查。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`。
- `git diff --check`、`.new`/`.bak` 零残留、sidecar 边界和 Phase 2 `guru-check-task`。
- fresh full-diff Branch Review；未验证的外部 PR/Issue 变更明确列为边界。

## Stop Conditions

- 若必须改变 public DTO、typed exit、transaction schema/mode/stage 或跨 Skill owner
  contract，停止并重新走 scope/contract review。
- 若正向场景需要删除 transaction、放宽 provenance 校验、修改 PR #337 或触碰
  #333，停止。
- 若 canonical 到 installed/platform projection 无法收敛，或产生 `.new`/`.bak`
  残留，停止并修复投影链路。
- commit、push、PR、merge、Issue closure 和 cleanup 仍是独立后续授权。

## Deliverables

- canonical Finalizer runtime 与聚焦回归测试；
- 直接命中的 contract/spec/RDT 增量（如 Phase 1/2 判定需要）；
- 由 preset apply 生成的 installed/dogfood/platform projections；
- Phase 2 check、Branch Review 和未验证边界的完整记录。
