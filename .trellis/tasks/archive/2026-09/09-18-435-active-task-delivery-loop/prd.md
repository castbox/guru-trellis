# #435 建立 Active Task Delivery Loop

合同版本：`2026-09-18-r3`。本任务停留在 Phase 1；本文不授权 task activation、实现、提交、push、PR、merge、发布或清理。

## 1. 目标与权威

建立 additive、尚未接入 production workflow 的业务 Delivery closed loop：

```text
guru-review-task-delivery
  -> guru-publish-task-delivery
  -> guru-merge-task-delivery
  -> delivery result
  -> #436 Task Completion
```

需求权威为 [`castbox/guru-trellis#435`](https://github.com/castbox/guru-trellis/issues/435)，父级全局切图权威为 [#434](https://github.com/castbox/guru-trellis/issues/434)，下游 Completion/Closure/Finish/Reactivate 权威为 [#436](https://github.com/castbox/guru-trellis/issues/436)。#405 与 #407 的真实复现是强制回归来源。

## 2. 范围

### R435-01 Delivery Review

新增 `guru-review-task-delivery`，使用 `judgment_mode=semantic`。它必须 fresh 读取 current requirement、approved Delivery policy、当前 slice、remaining work、验证、RDT/Docs、Architecture、base、完整 Branch Review 与 live Git/GitHub facts，并独占以下判断：

- 当前 slice 是否满足已批准的交付范围与独立交付条件；
- 当前 slice 内是否存在遗漏或缺陷；
- PR title/body、`Refs`、验证声明、remaining work 与未验证边界是否真实；
- 前序 authority 与 review 是否 current。

缺失或含糊的 Delivery policy 返回现有 Planning owner；task content finding 返回 Phase 2；scope authority 变化进入既有 clarification route。该 Skill 不执行 push、PR mutation、merge、Completion、Issue close、archive 或 cleanup。

### R435-02 Delivery Publish

新增 `guru-publish-task-delivery`，使用 `judgment_mode=semantic`，负责一个 reviewed Delivery 的唯一 remote publication transaction：

- push exact reviewed HEAD；
- 创建、更新或接管唯一 current same-repository PR；
- 执行 Draft/Ready transition；
- 从 #405 的 equal-head binding/output loss 恢复同一 PR；
- metadata 已一致时零重复 edit；
- same-plan recovery 中零重复 push、PR create、metadata mutation 或 Ready mutation。

它只消费 `guru-review-task-delivery` 的最小 ready DTO 与 live facts，不 archive task，不产生 completion，不使用 closing keyword。

### R435-03 Delivery Merge

新增 `guru-merge-task-delivery`，使用 `judgment_mode=semantic`，负责：

- fresh live readiness、expected head、base、merge method、subject/body、checks 与 mergeability 判断；
- 一次独立 merge confirmation；
- expected-head-bound merge mutation；
- merge result/output loss 的同一 mutation 恢复；
- 成功后产生一次最小 Delivery result，唯一 consumer 为 #436 Completion。

每次 Delivery merge 后 task、worktree 与 current binding 保持 active。Delivery result 不表达 task complete、Issue closure、archive、Finish 或 Cleanup。

### R435-04 分批交付 policy 与前置门禁适配

Planning/Approval 必须记录：task 总 scope、本次 Delivery slice、remaining work、独立交付条件、验证边界与后续 owner。Check、Task Commit、Branch Review 仍审查完整当前候选与影响，但满足性以本次已批准 slice 为边界：

- 尚未进入本次 slice 的工作保留为 remaining work，不阻断本次交付；
- 当前 slice 内遗漏、缺陷、不可独立交付或虚假验证声明必须阻断；
- task 总 scope 不缩减，remaining work 不得标记完成；
- 第一次 Delivery 不以整个 task 已完成为隐含前提；
- Completion 仅由 #436 判断。

本任务只调整这些 owner 的必要合同、public projection 与定向回归，不新增第二 Check、Commit、Branch Review 或 Acceptance owner。

### R435-05 多次 Delivery 与跨分支发现

同一 task 必须支持两个及以上顺序 Delivery PR。历史业务 Delivery 使用 immutable Git/GitHub identity 重建，禁止新增 Delivery ledger、解析 PR body、只查询 current branch 或覆盖初次 task creation branch/base 字段。

唯一 identity 机制为：`guru-merge-task-delivery` 在受控 merge commit body 写入闭合、机器可读、版本化 trailer，固定包含 schema version、stable task identity 与本 cycle 的 reviewed head identity；合并后再从 GitHub PR identity、merge commit identity、parents 与 trailer 重建 Delivery fact。该 trailer 是 Merge executor 已拥有的 commit-message payload，不新增 task-local history store。若仓库 policy 无法产生可控 merge commit，merge gate 在 mutation 前返回 blocked；不得回退到 ledger、PR body 或 branch-name 推断。

Remote branch 删除、重建或 Reactivate 后换 branch/worktree，不得改变已合并 Delivery identity。Finish bookkeeping PR 不携带 Delivery trailer，不进入业务 Delivery discovery。

### R435-06 Reactivate 后继续 Delivery

#436 完成同一 task 的 Reactivate 与 current workspace binding 后，本闭环只消费该 current active binding：

- 旧 merged PR、旧 remote branch 或旧 worktree 不构成阻塞；
- 新业务变更进入新的 PR，不重开或追加旧 merged PR；
- archive 到 active 的 tracked move 与必要 metadata 随新业务 Delivery 提交；
- 只补验证且无业务变更时不创建空 Delivery，由 #436 evidence-refresh 直达 Completion；
- 上一轮 Completion/Finish 仅为历史，不能证明本轮通过。

本任务不判断 Reactivate、不移动 archive、不准备 Reactivate workspace、不修改 Reactivate binding。

### R435-07 Base Reconciliation

吸收 #407 的正常路径：base conflict 经 `implementation_required` 回同一 active task，完成适配与 fresh Phase 2 后，由 `guru-reconcile-task-base` 消费 exact resolved tree，绑定 prior task head、new base、tree object、index-tree digest、parent order 与 semantic review，创建且只创建一个本地 reconciliation merge commit。stdout loss 只恢复同一 commit。该路径不 push、不改 PR/Issue、不绕过 Phase 2。

### R435-08 Additive migration 与分发

三个新 package、closed schemas、consumer declarations、canonical docs/spec、installed runtime、Shared/Codex/Claude/Cursor projections、preset manifest 与 package-local eval 必须完整交付。#434 激活前：

- current production workflow 与旧 Publication -> Finalizer -> Merge/Restore edges保持可运行；
- 新 package 不进入 production workflow mandatory graph；
- 禁止 old-output adapter、dual runtime graph、旧 output 到新 lifecycle result 的伪投影；
- 禁止提前删除旧 Finalizer、Merge 或 Restore assets。

#434 在 #435 与 #436 capability 均 ready 后独占原子激活、旧 edge retirement 与 graph count 更新。

## 3. 验收标准

- [ ] 首次 PR、existing PR、Draft/Ready 与 #405 equal-head binding/output loss 均收敛到唯一 current PR，零重复 remote mutation。
- [ ] 同一 task 完成两个顺序 Delivery PR；A/B 场景先交付 A，B 保持 remaining work，task 与 Issue 均未提前完成。
- [ ] Delivery Review、Publish、Merge 的 public input、每个 exit、唯一 consumer 与 private state 边界均闭合。
- [ ] 每个 Delivery PR 只使用 `Refs`；Merge 后 task 保持 active，Delivery result 只进入 #436 Completion。
- [ ] Merge result/output loss、provider blocker 解除与 exact terminal recovery 不重复 merge。
- [ ] 跨分支 discovery 从 merge commit trailer + GitHub/Git facts重建历史 Delivery；不读取 PR body，不依赖 current branch，不新增 ledger。
- [ ] Reactivate 后换 branch/worktree 继续新 Delivery；旧 merged PR 不阻塞，bookkeeping PR 不计入 Delivery。
- [ ] 只补验证的 Reactivate 不产生空业务 PR或 Delivery result。
- [ ] #407 conflict -> implementation -> Phase 2 -> exact resolved reconciliation commit 与 stdout-loss recovery 通过。
- [ ] 当前 slice 缺陷、remaining work 隐藏、Closing keyword、task premature completion、stale review/base/HEAD 与 identity drift 均 fail closed。
- [ ] source/installed package tests、Delivery/Merge integration、base-continuity integration、projection parity、preset reapply、dogfood drift、task validation 与 `git diff --check` 通过。
- [ ] #434 激活前 current production workflow 字节与旧 edge 行为不被新 package 提前切换。

## 4. 非目标

- 不实现或修改 #434 的 global graph activation、旧 edge retirement 或 atomic cutover。
- 不实现 #436 的 Completion、Issue Closure、Finish bookkeeping、Cleanup 或 Reactivate。
- 不关闭 Issue，不 archive task，不清理 branch/worktree/runtime。
- 不重构 Phase 0、完整 Planning、KDD、CI auto-merge、GitHub ruleset、Release 或业务仓生产操作。
- 不纳入 follow-up task，不新增独立 Acceptance。
- 不增加 Delivery ledger、PR-body identity inference、current-branch-only discovery、old-output adapter、dual runtime graph、锁、TOCTOU、攻击模型或通用 crash-recovery framework。

## 5. Open Questions

无。跨分支 identity、三 Skill owner 边界、#434/#436 分工、分批交付 policy、#405/#407 回归与 additive migration 已在本规划中固定。
