# EVIDENCE

| Evidence ID | Class | Locator / identity | Supports |
| --- | --- | --- | --- |
| `EVD-001` | current source | main `3c0d4a2ffe4799eb67f4c5b1c33d8f8a36f61875` | `ARCH-CUR-001..004,006` |
| `EVD-002` | stable release | `v0.6.5-guru.9`, commit `56b5f411e533b200e4d8685ca7a2ffb0c778a7f5` | `ARCH-CUR-005` only |
| `EVD-003` | RDT package | Issue #263 CLOSED；reviewed `d53335a7…`；archive `eaf955e0…`；PR #279 merge `891c2147…` | `ARCH-CUR-003` |
| `EVD-004` | Architecture package | Issue #264 CLOSED；reviewed `1cb2506b…`；PR #268 merge `37fdfe63…`；metadata head/merge `991080b6…` / `3b0f78c1…`；无 `finish-summary.json` | `ARCH-CUR-003` |
| `EVD-005` | Bootstrap package | Issue #265 CLOSED；reviewed `f2c67098…`；archive `de1c6e26…`；PR #280 merge `3c0d4a2f…`；archive/merge tree `45e8b402…` | `ARCH-CUR-003` |
| `EVD-006` | task authority | Issue #266 OPEN；task planning artifacts | this Bootstrap scope |

PR body、commit 与 task archive 中的 focused test 数字是 fresh 回读的 historical claims，
详见 `docs/test/**/test-plan.md`；相关 PR 无 GitHub review/check/status 记录，本 EVIDENCE
不把它们转化为 GitHub CI proof 或 #266 的重跑 PASS。#260/#267/#275 的矩阵证据均
`unverified`。
