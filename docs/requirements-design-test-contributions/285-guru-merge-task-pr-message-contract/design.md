# #285 Design contribution

- `DES-020`：Finalizer `ready_for_merge` output bytes 不变；其 target-owned authoring
  seed 只把 `reviewed_merge_message` 交给 Merge semantic owner 补全，避免扩大 Finalizer
  public DTO。
- `DES-021`：Merge package 显式选择 2.0 workflow/standalone/aggregate input 与 private
  gate；1.0 assets 留在 Interface inventory 中并由固定 hash 回归保护。
- `DES-022`：package-local `build_reviewed_merge_message` / validator 是 subject/body
  唯一实现；legacy formatter 调用同一实现。validator exact reconstruction，并拒绝
  summary、subject 或 body 任意位置可形成 GitHub Issue closure 的九种 close-keyword
  词形及 local / `owner/repository#issue` 引用，不误伤 `fix/...` 分支名。
  canonical body 不带尾随换行；executor 写入相同 bytes，post-merge verifier 不对 GitHub
  回读结果做 strip/normalize，而是直接精确比较。
- `DES-023`：live facts 增加 expected base ref 与 merged commit message/parents；gate
  保存 pre-merge base head 和 reviewed message digest，checker 同时校验 live facts digest
  与显式 base-head binding。
- `DES-024`：executor 在 gate identity 目录 materialize `merge-body.md`，以
  `try/finally`、terminal recovery 与 final consumer cleanup 保证零 residue；未知或错误
  residue fail closed。
- `DES-025`：post-merge success 要求
  `merge SHA == PR mergeCommit == remote base ref`、parents 精确等于
  `[pre-merge base head, expected head]`，并逐字节匹配 reviewed subject/body；现有 closure
  mismatch typed exit 继续独立承接 provider close 结果。

Architecture Baseline 判定为 `no_change`：workflow lifecycle、Merge owner、deterministic
runtime、distribution 与 repository knowledge 的 domain ownership 均未改变，只补全
`ARCH-DOM-002`、`ARCH-DOM-004`、`ARCH-DOM-005` 现有边界内的 correctness contract。
