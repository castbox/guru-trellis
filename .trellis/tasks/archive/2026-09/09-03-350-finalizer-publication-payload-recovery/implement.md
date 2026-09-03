# #350 实施计划

## Phase 1: Planning And Discovery

- [x] 读取 live Issue #350、当前 `main@1fd63dab`、#342/#344/#347 合同与 Finalizer spec。
- [x] 创建并激活独立 task/worktree；不触碰其它并行 worktree、PR #337 或 #333 transaction。
- [x] 完成 `trellis-before-dev`，确认 canonical Finalizer runtime/test/spec 的 authoring partition。

## Phase 2: Implementation

1. 先在 canonical `owner.py` 与 Finalizer tests 中固定现有失败：Publication body 正常演进被 `provenance_tail_transaction_rebind_invalid` 阻断。
2. 保持 provenance-tail rebind 原 topology allowlist；`publication` metadata mismatch 仅在 base evolution 加单一合法 tail 的 composed classifier 成立时进入既有 `classify_existing_pr_recovery()`，pure base evolution 与其它 identity/业务错误继续 fail-closed。
3. 增加/调整真实 topology 与 execution/retry 测试，验证 metadata equal/convergence、Ready/Draft、mutation 顺序和次数。
4. 若确认合同语义发生变化，更新 canonical Finalizer `SKILL.md`、`references/contract.md` 与命中的 workflow specs；保持 public I/O/schema 不变。
5. 创建 task-owned RDT contribution `docs/requirements-design-test-contributions/350-finalizer-publication-payload-recovery/`，不直接改 shared current authority。

## Phase 3: Projection And Validation

1. 运行 canonical 与 installed Finalizer targeted tests。
2. 运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`，同步 dogfood、Shared、Codex、Claude、Cursor projection。
3. 运行 package/task validation、ownership、dogfood drift、byte parity、`git diff --check` 与 recursive sidecar-zero。
4. 明确报告未执行的 commit、push、PR、merge、Issue closure、release、production 与完整 Throwaway matrix。

## Stop Conditions

需要新增 public DTO/exit/schema、改变 transaction mode/stage、修改 PR #337/#333、扩大到任意 Publication rewrite，或 projection 无法无 sidecar 收敛时停止并回报。
