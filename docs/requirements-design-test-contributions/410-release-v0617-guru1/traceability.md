# #410 Release v0.6.17-guru.1 Traceability

状态：`reviewed_promoted`；immutable superseded predecessor：
`current-main-0.6.5-guru.51`；promoted/current active successor：
`current-main-0.6.17-guru.52`。

| Requirement | Design | Test | Architecture refs |
| --- | --- | --- | --- |
| `R410-01` | `D410-01` | `T410-01`, `T410-05` | `ARCH-CUR-029` |
| `R410-02` | `D410-01`, `D410-02` | `T410-01` | `ARCH-CUR-029` |
| `R410-03` | `D410-02` | `T410-02` | `ARCH-CUR-029`, `ARCH-INT-014` |
| `R410-04` | `D410-01`, `D410-03`, `D410-05` | `T410-02`, `T410-05` | `ARCH-CUR-029`, `ARCH-INT-016` |
| `R410-05` | `D410-03` | `T410-03` | `ARCH-INT-015` |
| `R410-06` | `D410-04`, `D410-06` | `T410-04`, `T410-05`, `T410-07`, `T410-08` | `ARCH-CUR-029`, `ARCH-INT-015` |
| `R410-07` | `D410-05`, `D410-06` | `T410-06`, `T410-08` | `ARCH-CUR-029`, `ARCH-INT-015` |

`BEH-018` is covered by `D410-03..06` and `T410-03..08`. Requirements、Design
与 Test 定义分别位于 [requirements.md](./requirements.md)、[design.md](./design.md)
与 [test.md](./test.md)。Architecture public inheritance 以
[`README.md`](../../architecture/README.md) / `current-main-0.6.17-guru.52` /
`active` 为 authority。

本 contribution 的 `reviewed_promoted` identity 不证明 post-promotion gate、merge、
tag、GitHub Release 或 Issue closure；动态 candidate SHA、Gate/checkpoint、时间和用户授权
不进入本 authority。
