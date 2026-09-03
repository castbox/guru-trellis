# #347 技术设计：base evolution 与 provenance tail 组合恢复

## 1. Design Boundary

在 canonical `guru-finalize-task` package 内扩展现有 provenance-tail transaction rebind 分类。新逻辑先判断当前
Publication HEAD 是否为一个合法 provenance tail；成立时，以 tail 的直接父提交作为 #344 base-evolution comparison
endpoint。完整组合资格通过后，继续调用现有 existing-PR strict-ancestor classifier 与 recovery transaction engine。

```text
predecessor ordinary/push_content/unbound transaction
  -> current plan identity mismatch
  -> preserve #342 direct-tail validation
  -> preserve #344 pure-base-evolution validation
  -> detect one legal current provenance tail
       -> validate tail against direct parent through existing validator
       -> compare predecessor..tail-parent with merge-base..current-base
  -> resolve unique same-repository Open PR at predecessor Publication HEAD
  -> existing-PR strict-ancestor classification against current Publication HEAD
  -> preview exact recovery
  -> execute: reread -> persist bound transaction -> push current Publication
  -> metadata -> archive -> archive push -> Ready -> ready_for_merge
```

## 2. Classification Composition

`classify_provenance_tail_transaction_rebind()` 保持现有候选入口：

1. transaction 必须为 unbound `ordinary_publication/push_content`。
2. `provenance_tail_transaction_rebind_errors()` 继续验证 task/repo/base/head/Publication/scope/archive 与 #342
   direct-tail 路径。
3. 若错误集只包含当前定义的 provenance-shape inapplicability errors，则 base-evolution classifier 依次评估：
   - pure #344：current Publication HEAD 本身作为 comparison endpoint；
   - #347 composition：current Publication HEAD 经现有 validator 证明是合法 tail 后，其直接父提交作为 endpoint。
4. 任一成功路径都进入同一个 live PR resolver 与 `classify_existing_pr_recovery()`。
5. identity、scope、archive、transaction 或 PR conflict 不进入 composition fallback。

该顺序保持三条路径互斥且共享同一后续 owner：#342 direct tail、#344 pure base evolution、#347 base evolution 加
single provenance tail。

## 3. Helper Shape

优先将现有 `provenance_tail_transaction_rebind_is_base_evolution()` 收敛为可接收明确 comparison endpoint 的
package-private helper，或增加一个只负责解析合法 current tail parent 的薄 helper。实现必须满足：

- tail parent 从 Git parent facts 取得，不由 caller 输入猜测；
- `provenance_tail_commit_errors(root, tail_parent, current_publication_head, ...)` 返回空错误集后才使用该 parent；
- pure #344 仍以 current Publication HEAD comparison；
- composition 以 tail parent comparison；
- binary delta equality、base ancestry 与 merge-base 规则保持字节级一致；
- helper 不写 transaction，不执行 remote read，不产生 public DTO。

不增加“忽略 manifest path 后比较”的通用 diff filter。先验证并移除完整合法 tail，可直接复用现有 provenance
authority，且不会把非法 manifest 内容从 base-delta comparison 中隐藏。

## 4. Exact Invariants

组合 classifier 在调用 strict-ancestor recovery 前证明：

- predecessor/current task、repo、base/head branch、Publication 与 close scope 精确一致；
- predecessor reviewed/publication continuity 继续满足现有合同；
- current tail 是 single-parent、manifest-only、allowlist-valid；
- tail parent 是合法 base-evolution endpoint；
- remote 与 PR HEAD 均满足 `== predecessor Publication HEAD`；
- current Publication HEAD 是 predecessor Publication HEAD 的严格后代；
- archive 未开始，transaction 未绑定其它 PR，current plan/gate/Publication 均 fresh。

后续 `classify_existing_pr_recovery()` 继续拥有 PR repository/base/head/head-repository、Open state、唯一性、scope、
metadata、Draft/Ready、remote equality 与 strict ancestry 判断。

## 5. Transaction And Mutation Order

Preview 只返回现有 `existing_pr_recovery` shape，不增加新 public 字段。组合 endpoint 只作为 owner 内部 classification
evidence 和 targeted test assertion。

执行阶段：

1. 重读 current plan、transaction、Git topology、remote 与 PR。
2. 重跑相同 composition 与 strict-ancestor classification。
3. 比较 checked preview 所绑定的现有 recovery facts。
4. 在首个外部 mutation 前写入 current-plan-bound `existing_pr_recovery/push_content` transaction。
5. push current Publication HEAD 一次，再进入现有 metadata、archive、archive push 与 Ready transitions。

中断后重试读取已绑定 transaction，由现有 transition engine 跳过完成步骤；不得再次执行 composition rebind。

## 6. Compatibility

- #342 direct-child provenance-tail classifier、error identity 与 strictness 不变。
- #344 pure base merge 与 multiple-base-commit exact binary-delta path 不变。
- #338 exact-plan equal-HEAD adoption 与 `push_required=false` 不变。
- fresh unbound equal-HEAD PR、非祖先 remote、fork、multiple/terminal PR 与 scope drift 继续阻断。
- transaction schema 3.0、mode、stage、public Skill Interface 与 typed exits 不变。
- 多 tail 链继续阻断，因为当前 provenance validator 的合同是一个 direct-child tail。

## 7. Test Design

### 7.1 Real Git topology

构造真实 repository：

1. main base commit；
2. task branch old Publication；
3. main 新增两个 base commits；
4. task branch merge main；
5. 基于 merge HEAD 生成并提交合法 manifest-only provenance tail。

断言 old Publication、base head、merge endpoint、tail HEAD 的 ancestry 和 changed paths，再执行真实 classifier。

### 7.2 Compatibility matrix

- #347 composition：base merge 加 single legal tail。
- #342 direct tail：无 base evolution。
- #344 pure base evolution：base merge 与 multiple base commits，无 tail。
- #338 equal HEAD：现有 transaction-bound equality。

### 7.3 Negative matrix

- tail 修改额外文件、非法 manifest 字段、错误 parent、merge tail、多 tail 链；
- tail parent 后存在额外 business commit，或 base binary delta comparison 返回 false；
- task/repo/base/head/title/body/scope/archive/transaction drift；
- remote/PR HEAD drift、multiple/fork/terminal PR、metadata preview drift、stale plan/gate/Publication。

### 7.4 Execution and retry

在现有 Finalizer execution fixture 中覆盖 Ready/Draft 与 metadata equal/convergence：

- transaction write 发生在首个 external mutation 前；
- current Publication push 计数 1，old push 与 PR create 计数 0；
- PR edit 计数 0 或 1；archive move/commit/push 各 1；Ready mutation 为 0 或 1；
- 每个 transition 中断后的 same-plan retry 不重复已完成 mutation。

## 8. Docs And Projection

采用 `delta_first`，创建 task-owned RDT contribution，更新 canonical Finalizer Skill/contract 与三个命中的 workflow
spec。随后运行 preset all-platform apply，同步 dogfood installed、Shared、Codex、Claude、Cursor，并验证 ownership、
drift、byte parity 与 sidecar-zero。

## 9. Architecture And Rollback

设计不改变 owner、public graph、persistence、transaction stage 或依赖方向，预期 Architecture route 为
`no_architecture_impact`。若实现发现必须改变任一边界，停止 Phase 2 并重新进入 qualification 与 Architecture impact。

回滚单位是本 task 的 canonical Finalizer runtime/tests/contract/spec/RDT delta，再运行 preset apply 恢复生成投影。
不得只回退生成副本，也不得 mutation #333、PR #337 或 #249。
