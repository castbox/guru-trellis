# EVIDENCE

| Evidence ID | Class | Locator / identity | Supports |
| --- | --- | --- | --- |
| `EVD-001` | current source baseline | main `c2b1784654a95b999bbff71daf1393c22aa01048` + #275 uncommitted task delta | `ARCH-CUR-001..004,006..007` |
| `EVD-002` | stable release | `v0.6.5-guru.9`, commit `56b5f411e533b200e4d8685ca7a2ffb0c778a7f5` | `ARCH-CUR-005` only |
| `EVD-003` | RDT package | Issue #263 CLOSED；reviewed `d53335a7…`；archive `eaf955e0…`；PR #279 merge `891c2147…` | `ARCH-CUR-003` |
| `EVD-004` | Architecture package | Issue #264 CLOSED；reviewed `1cb2506b…`；PR #268 merge `37fdfe63…`；metadata head/merge `991080b6…` / `3b0f78c1…`；无 `finish-summary.json` | `ARCH-CUR-003` |
| `EVD-005` | Bootstrap package | Issue #265 CLOSED；reviewed `f2c67098…`；archive `de1c6e26…`；PR #280 merge `3c0d4a2f…`；archive/merge tree `45e8b402…` | `ARCH-CUR-003` |
| `EVD-006` | Bootstrap closeout | Issue #266 CLOSED；PR #281 merge `c2b1784654a95b999bbff71daf1393c22aa01048`；archive/merge tree `cb68fead327cc2cfb6ea03b8e81affcb9b7ad0e9` | active RDT/Architecture baseline |
| `EVD-007` | replacement task | Issue #275 OPEN；exact `v0.6.5-guru.9` regression log、focused tests 与 local-current representative Throwaway | `ARCH-CUR-007`；exact committed release gate仍待执行 |

PR body、commit 与 task archive 中的 focused test 数字是 fresh 回读的 historical claims，
详见 `docs/test/**/test-plan.md`；相关 PR 无 GitHub review/check/status 记录，本 EVIDENCE
不把它们转化为 GitHub CI proof。#275 当前只有 focused/local-current representative proof；其 exact committed candidate、tag-pinned smoke、GitHub Release 与 downstream gate，以及 #260/#267 的完整矩阵，均保持 `unverified`。
