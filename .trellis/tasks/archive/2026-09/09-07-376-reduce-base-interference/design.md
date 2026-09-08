# #376 技术设计

## 1. 设计目标

把“基线已前进”拆成集成事实，把“任务是否仍可按原规划继续”保留为 authority/task-content 判断。这样并行任务可以记录新的 base，而不把无关集成变化升级为规划失效。

## 2. 影响边界

- Canonical：`trellis/workflows/guru-team/workflow.md`、`trellis/skills/guru-team/packages/guru-reconcile-task-base/`。
- Durable spec：`trellis/presets/guru-team/spec/workflow/{workflow-contract.md,skill-package-contract.md,data-contracts.md,quality-guidelines.md}`。
- Architecture：继续复用 current semantic owner、确认边界与 typed projection，不新增 domain、长期 owner、
  GAP 或 ADR；但新增 package-private deterministic executor 使 current command graph 从 77 变为 78，属于
  `target_native` architecture impact。task 先维护隔离 contribution，独立 committed review 后再由
  serialized Architecture/RDT owners 将 `.45` promotion 为 `.46`。
- Projection：`.trellis/workflow.md`、`.trellis/spec/workflow/quality-guidelines.md`、preset/Agents/Codex/Claude/Cursor 对应同步文件。
- Tests：reconcile package 的 contract/eval/runtime fixtures。

## 3. 状态模型

1. 读取旧 base 与新 base，形成 integration clock delta。
2. 独立比较 live Issue、approved planning assumption、accepted scope 与 task content，形成 authority/task-content clock 结果。
3. 若 authority/task-content 未变：返回既有 `reconciled`，保留原 `resume_target`，允许继续当前阶段。
4. 若 authority/task-content 变更：沿现有 `planning_stale` 或既定 owner route 处理，不由 integration delta 覆盖判断。
5. `post_plan` 只在第 4 步成立时回 Planning。

## 4. 兼容性与 SSOT

- 不新增 exit；沿用现有 typed exits 与 consumer。
- 不把 base digest 当作 planning authority；digest 只用于确定性 freshness/identity 校验。
- canonical Markdown 是流程语义来源，package runtime 仅实现确定性状态读取与结果校验。
- 生成/管理投影需保持字节或合同要求的一致性，避免只修 dogfood 副本。

## 5. 回滚与风险

- 主要风险是把真实 Issue/assumption 变化误判为无关 base delta，导致 stale 被吞掉；通过正反 fixture 同时断言避免。
- 若 projection 或 runtime contract 不一致，停止在 check/branch review，不通过局部绕过。
- 回滚边界为本任务新增/修改的 canonical contract、projection 和测试文件；不触碰其他 dirty 改动。

## 6. 基线演进兼容设计

- 2026-09-08 将 `origin/main@d95f875cc4751c4487444b942901bf5023e44acc` 集成到任务分支。新基线保留 #377 对 `guru-clarify-requirements` 调用与 eval staging 的收敛，不恢复被删除的旧 typed-output 注入路径。
- Branch Review finding `BR-376-NATIVE-ADAPTER-3000` 识别出 `base-unrelated-reconciled` 只是 task-local fixture 别名，没有独立生产消费者，却让 #376 修改 6798 行共享 adapter。按 subtraction-first 合同，`unrelated-base-delta-facts.json` 直接复用已有 `base-reconciled` recipe，并删除 canonical/installed adapter 中 #376 新增的 alias 行。
- `.trellis/guru-team/extension.json` 通过 canonical/installed 组合字节重建：同时承接 #376 reconcile 资产与 #377 clarify 资产，并绑定组合后的 native adapter 哈希。
- 新基线已存在但与 #376 无关的 #108 projection/sidecar 状态不纳入本任务，不通过 reapply 扩张为额外变更；完整 upgrade/reapply/Release 矩阵仍由专门 Issue 负责。

## 7. Branch Review Finding 修复

- Finding：`BR-376-NATIVE-ADAPTER-3000`。
- Replacement：保留无关 base delta 的独立 fixture 场景与 `reconciled` 断言，但 staging 复用现有 `base-reconciled`，不再扩展共享 native adapter recipe 表。
- Diff boundary：当前未提交 worktree candidate 相对 `origin/main` 已不再包含 `trellis/skills/guru-team/adapters/eval/native_adapter.py`；finding-fix commit 后的完整 `origin/main...HEAD` 也必须保持该结果。installed adapter 与 canonical 保持字节一致。
- Provenance：仅按当前 canonical/installed 字节更新 `.trellis/guru-team/extension.json` 的相关 managed file hash、package tree 和 source provenance，保留 #377 与其他基线记录。

## 8. Finalizer Base Reconciliation

- 2026-09-08 Finalizer 观察到 `origin/main` 从 `d95f875cc4751c4487444b942901bf5023e44acc` 前进到 `81657210f5508186ed0f09098fdc63c927fdc307`；新增 #384/#385 Discovery 修复不改变 Issue #376、approved planning assumptions、accepted scope 或 task behavior authority。
- 101 个 base delta 路径中，仅 `.trellis/guru-team/extension.json` 与 #376 路径相交；冲突限定为两侧 `installed_at` 与 `source.ref/commit` provenance preimage，package/file inventory 由 Git 三方合并保留。
- 组合结果保留 #376 当前 provenance preimage `0001af5875543c25b9119be5e4c48b4c93286493` 与 `tree_state=dirty`，并同时保留 #376 reconcile 和 #384 Discovery 的 package/file digest；publication provenance tail 仍由 Finalizer 独占。
- 该 reconciliation 不重新解释 #376 需求或实现，不新增 public exit、owner、持久化状态或兼容机制；tracked manifest 冲突解决按当前 workflow 重新执行 Phase 2、Task Commit、完整 Branch Review 与 Publication。

## 9. Post-Review Cross-Skill Continuity

### 9.1 已确认缺口

- `guru-reconcile-task-base:finalizer_base_mismatch` 可在 authority/task content 未变时返回 `reconciled/finalization_resume`。
- Publication 的 `guru-reviewed-content-1.0` 对完整非 metadata tree 绑定 identity；只要新 base 修改普通 source/spec，即使 task-relative delta 未变，旧 Branch Review commit 与当前 reconciled HEAD 的 identity 也必然不同。
- 现有 `guru-review-branch:base_continuity` public input 已同时携带 `task_head` 与 `branch_review_commit`，但 runtime 错误要求二者都等于当前 HEAD，无法表达“prior full review + current reconciled candidate”。
- 因此当前链路只能在 Publication fail closed 后回完整任务流程，或伪造 current HEAD 已完成完整 Branch Review；两者都不满足扩展后的 Issue authority。

### 9.2 直接演进方案

1. `guru-reconcile-task-base` 对 `post_branch_review`、`post_publication`、`finalizer_base_mismatch` 使用两个结果：
   - candidate reviewed-content identity 与 prior review identity 相同：`reconciled` 并恢复原 target；
   - task content 未变、integration compatible，但 current candidate 需要新的 reviewed-content identity：`review_continuity_required`。
2. 对第二种结果，reconcile owner 在完成语义判断后展示精确 task branch、expected task/base HEAD、candidate tree、merge/commit 范围和零 remote 副作用，取得当次确认后调用 package-private deterministic executor。executor 仅允许 clean branch-bound worktree，以 expected-head 合入精确 `new_base_head` 并创建一个 reconciliation commit；结果必须同时满足 prior review ancestor、new base ancestor 和 candidate tree identity，任一 stale/mismatch 在写入前失败，执行后不匹配则阻塞而不是猜测恢复。
3. `base_continuity` 输入语义固定为：
   - `branch_review_commit`：先前完整 Branch Review commit；
   - `task_head`：当前已提交的 reconciled HEAD；
   - old/new base、candidate tree、relevant paths 与 resume target：来自同一 reconciliation judgment。
4. recorder 要求 `task_head == HEAD`，并验证 prior `branch_review_commit` 是 current HEAD 祖先、新 base 是 current HEAD 祖先、current tree 与已审查 candidate tree 一致；bounded review 的 gate `review_commit` 绑定 current HEAD。
5. owner-private integration pair 增加 prior full-review identity 并纳入 freshness；旧 checkpoint 不迁移，按 stale 重新生成。
6. `continuity_passed` 输出中的 `branch_review_commit` 是 current reconciled HEAD，表示该 HEAD 已通过 bounded continuity review，供 Publication 计算当前 reviewed-content identity；它不是一次完整 Branch Review。
7. workflow 保持现有 public exit id 和 owner：continuity router 只恢复原 `resume_target`，不增加兼容 wrapper、双读或第二状态机。

### 9.3 Current-only schema evolution

- `guru-reconcile-task-base:review_continuity_required`、`guru-review-branch:base_continuity`、`continuity_passed` 升级为新的 current-only public schema version；字段保持最小，但明确区分 prior full-review commit 与 current reconciled HEAD。
- Branch Review aggregate input 与 owner-private review gate 升级到新的 current-only version，使 continuity gate 同时绑定 prior review、current review commit、exact pair 与 candidate tree。旧 public input 或旧 gate 直接 stale/fail closed，不做兼容分支或原地语义替换。
- Publication public input、readiness gate 与 `guru-reviewed-content-1.0` 不升级；它只消费 continuity 输出投影出的 current `branch_review_commit`，并按现有算法严格校验 current HEAD/content。
- Reconcile private checkpoint 若承载新增 executor/result identity，则同步升级 current-only schema；Git 执行 receipt 只保留 recorder/checker 的直接消费字段，不保存用户授权。

### 9.4 失败与回退

- prior review 不是 current HEAD 祖先、candidate tree/pair 不匹配、相关 base delta 未完整审查、验证不足或出现 task-content/authority 变化时 fail closed。
- worktree 非 clean、HEAD/base 漂移、candidate tree 与拟提交结果不同、merge 无法按已审查结果完成时，executor 不创建可继续消费的 reconciliation result；不得复用旧确认或自动改写解决方案。
- task-content、scope、authority 或实现变化继续走 `implementation_required`、`planning_stale`、scope clarification 或完整 Branch Review，不得降级为 bounded continuity。
- Publication 继续严格校验当前 continuity-reviewed HEAD；不放宽 `guru-reviewed-content-1.0`，也不接受 caller 自报的 review identity。

## 10. Architecture/RDT Authority Promotion

- finding：`candidate:architecture-command-graph-stale`。实现后的 live package graph 为 23 Skills / 97 exits /
  78 commands，`.45` current authority 的 77-command 声明已 stale。
- path：`target_native`；新增 command 是 Reconcile package-private deterministic executor，既有 semantic
  owner、public Skill/exit、single-writer、confirmation 与 Publication authority 均保持不变。
- contribution：`architecture-contribution-376-base-continuity-command-v1` 与
  `docs/requirements-design-test-contributions/376-base-continuity-command/`。
- promotion：贡献先经 Phase 2、Task Commit 与 independent committed review；随后 serialized owner 以
  expected `.45` 创建唯一 active `.46`，并对 promotion-created diff 再执行 fresh Phase 2、Task Commit 与
  完整 Branch Review。
- history：`.45` 的需求、设计、测试正文与 release facts 保持 immutable；promotion 只允许写 predecessor
  lifecycle locator（`superseded` / `successor=.46`），并把 `.45` Design manifest 的历史错误
  `command_count: 81` 校正为该版本真实的 `77`。不创建 ADR，不处理 Issue #108 sidecars 或完整矩阵。
