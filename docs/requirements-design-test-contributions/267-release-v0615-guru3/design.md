# #267 Release authority alignment Design contribution

## Authority lifecycle

- `D267-AUTH-01`：当前 task worktree 是 contribution writer；RDT 与 Architecture
  serialized promotion owners 是 shared-current writers。两类 writer 不并行修改同一
  shared current 文件。
- `D267-AUTH-02`：RDT contribution 以 `.41` 为 source/expected current、`.42` 为唯一
  candidate successor；Architecture contribution 使用相同 before/after identity。
- `D267-AUTH-03`：contribution review 通过后，fresh owner dependency review 确定 Architecture
  先激活统一 `.42` baseline、RDT 后建立并继承该 current `.42` versioned authority；两者串行执行，任一
  owner 发现 live current 不再是 `.41` 时返回 `sync_required`，不得覆盖新 authority。
- `D267-AUTH-04`：promotion 只把已审核的 release/current fact delta 投影到
  Requirements、Design、Test、Architecture navigation/current/evidence；`.41` 的正文只
  接受 status/predecessor-successor 历史收敛，不原地改写为 `.42`。
- `D267-AUTH-05`：promotion-created shared-current diff 是新的 reviewed content，必须
  重新执行 Phase 2、task commit 与独立 Branch Review，不能复用 contribution review。
- `D267-AUTH-06`：promotion 将 task 已固定的
  `v0.6.15-guru.3 -> 0.6.15-guru.39 -> Trellis CLI 0.6.15` mapping 投影到 `.42`
  current facts，不修改 release identity owner 或 runtime source。
- `D267-AUTH-07`：authority alignment 不改变 Issue ledger；preparation PR 继续只引用
  `Refs #267`，#267 与 #311 的独立 closure 条件保持不变。

## Preserved contracts

- release mapping 仍是 `v0.6.15-guru.3 -> 0.6.15-guru.39 -> Trellis CLI 0.6.15`；
- #311/#312 implementation、Finalizer/Publication/runtime graph 与所有 public I/O 不变；
- design constitution、project change contract、architecture owner、GAP 与 compatibility
  exit 不变；
- preparation PR 仍只 `Refs #267`，`close_issues=[]`。

Architecture before/after、required concerns、project check 与 promotion state 由
`docs/architecture/contributions/267-release-v0615-guru3.md` 拥有；本文只承接 RDT
design responsibilities。Architecture 与 RDT serialized promotion 均已完成；post-promotion fresh
Phase 2/commit/Branch Review 仍是后续 mandatory route。
