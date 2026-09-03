# #350 技术设计：Finalizer 收敛正常 Publication payload 演进

## Design Boundary

在 canonical `guru-finalize-task` package 内修正 predecessor transaction rebind 的 identity predicate：保持 task/repository/branch/scope/HEAD 与 provenance topology 的严格校验，只将 Publication `title/body` 的比较和收敛责任交回现有 `classify_existing_pr_recovery()`。不新增 public profile、typed exit、transaction stage/schema 或第二套 PR recovery classifier。

## Classification

```text
current plan validation mismatch
  -> only unbound ordinary/push_content predecessor
  -> validate task/repo/base/head/scope/archive and legal base+tail topology
  -> allow publication title/body to differ as metadata candidate
  -> resolve predecessor remote/PR identity
  -> classify_existing_pr_recovery(current plan, PR, predecessor HEAD)
  -> preview strict-ancestor recovery and metadata comparison
```

`PROVENANCE_TAIL_INAPPLICABLE_ERRORS` 保持仅含原有两个 topology error。`publication` title/body mismatch 只有在 `provenance_tail_transaction_rebind_base_evolution_tail_parent()` 同时证明 exact base evolution 与单一合法 provenance tail 时才可组合；pure base evolution 与 direct-tail 路径继续要求 predecessor Publication payload 精确一致。其它 identity、scope、archive、current reviewed/publication HEAD 错误仍然阻断。随后必须调用现有 strict-ancestor classifier，继续由它校验 live PR scope、remote/PR HEAD、metadata comparison、Draft/Ready 和 ancestry。

## Execution And Retry

执行前重跑上述 predicate 与 existing-PR classifier并比较 preview facts。通过后先持久化 current-plan-bound `existing_pr_recovery/push_content` transaction，再 push current Publication HEAD；metadata convergence、archive、archive push、Ready 和 terminal DTO 继续使用现有 transaction engine。绑定后重试只读取 bound transaction，不能重新执行 rebind，也不能重复 push/edit/archive/Ready。

## Compatibility

- #342 direct-tail、#344 pure base evolution、#347 base evolution plus tail、#338 equal-HEAD recovery 保持原合同。
- close-Issue scope、Issue disposition、repository/branch、PR identity、remote/PR HEAD、business delta、非法 provenance tail 与 stale gate 不进入 metadata fallback。
- 若实现需要修改 public I/O、typed exit、transaction schema 或 owner 边界，立即停止并重新进入 Architecture/规划审查。

## Test Design

- 增加 real Git topology 与 fresh Publication body 演进 fixture，断言 preview metadata comparison 与 strict-ancestor recovery。
- 覆盖 title/body equal、LF/内容正常演进、scope/repo/branch/PR/HEAD drift、非 provenance 文件、非法 manifest、多 tail、额外 business delta、stale transaction。
- 复用现有 execution fixture 断言 transaction write 先于外部 mutation，push=1、PR create=0、metadata edit<=1，retry 不重复。
