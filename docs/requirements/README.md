# Requirements SSOT

本目录是 Guru Team Trellis Extension 的唯一 Requirements authority。运行时行为仍由 canonical workflow 与 Skill package 定义；task-local `prd.md` 只描述单次变更，不是产品需求 authority。

## 当前入口与版本矩阵

| 状态 | 版本 | Locator | Provenance |
| --- | --- | --- | --- |
| `active` | `current-main-0.6.5-guru.35` | [requirement-main.md](./versions/current-main-0.6.5-guru.35/requirement-main.md) | `source_confirmed` + `code_recovered`，绑定 main `3c0d4a2f…` |
| `released` | `v0.6.5-guru.9` | [requirement-main.md](./versions/v0.6.5-guru.9/requirement-main.md) | `source_confirmed`，tag commit `56b5f411…` |
| `target` | Trellis `0.6.15` compatibility | [当前版本 gap](./versions/current-main-0.6.5-guru.35/requirement-non-functional.md#兼容与未验证边界) | `unverified`，由 #260/#267 验证 |

读取顺序：`requirement-main.md` -> `requirement-non-functional.md` -> `traceability.md` -> `decisions.md`。Design、Test 与 Architecture 入口分别位于 `docs/design/README.md`、`docs/test/README.md`、`docs/architecture/README.md`。

普通 task 不直接修改 shared current authority；先由 `guru-maintain-requirements-design-test-ssot:task_impact_sync` 判定 contribution/direct sync，再通过 `promotion` 激活。结构冲突或过期状态走 `repair`。

旧路径 `requirement-main.md` 与 `guru-team-trellis-flow.md` 仅保留迁移导航，不定义 current。
