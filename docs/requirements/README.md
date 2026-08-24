# Requirements SSOT

本目录是 Guru Team Trellis Extension 的唯一 Requirements authority。运行时行为仍由 canonical workflow 与 Skill package 定义；task-local `prd.md` 只描述单次变更，不是产品需求 authority。

## 当前入口与版本矩阵

| 状态 | 版本 | Locator | Provenance |
| --- | --- | --- | --- |
| `active` | `current-main-0.6.5-guru.40` | [requirement-main.md](./versions/current-main-0.6.5-guru.40/requirement-main.md) | #295 reviewed Architecture/RDT promotion，绑定 task head `51609250…` + #295 serialized promotion delta + `2026-08-24` 用户明确确认的 `EVO-001..007` target delta；精确 revision 由包含本 authority 的 Git commit/tree identity 绑定，正文不自引用可变 HEAD |
| `superseded` | `current-main-0.6.5-guru.39` | [requirement-main.md](./versions/current-main-0.6.5-guru.39/requirement-main.md) | #290 reviewed Architecture/RDT promotion |
| `superseded` | `current-main-0.6.5-guru.38` | [requirement-main.md](./versions/current-main-0.6.5-guru.38/requirement-main.md) | #283 reviewed Architecture/RDT promotion |
| `superseded` | `current-main-0.6.5-guru.37` | [requirement-main.md](./versions/current-main-0.6.5-guru.37/requirement-main.md) | #260 verified compatibility；extension candidate 仍为 `0.6.5-guru.37` |
| `superseded` | `current-main-0.6.5-guru.36` | [requirement-main.md](./versions/current-main-0.6.5-guru.36/requirement-main.md) | #275 replacement release 后的 immutable before-state authority |
| `superseded` | `current-main-0.6.5-guru.35` | [requirement-main.md](./versions/current-main-0.6.5-guru.35/requirement-main.md) | #266 激活的历史 current snapshot |
| `released` | `v0.6.5-guru.9` | [requirement-main.md](./versions/v0.6.5-guru.9/requirement-main.md) | `source_confirmed`，tag commit `56b5f411…` |

当前 main 已验证 official Trellis `0.6.15` compatibility。重构前稳定版发布目标固定为
tag `v0.6.15-guru.1`、extension `0.6.5-guru.37`、Trellis CLI `0.6.15`；stable tag、
GitHub Release、tag-pinned install 与 post-publish smoke 仍为 `unverified`，只由独立的
重构前稳定版 Release Issue 晋升。#267 与下一阶段重构链不属于该发布的前置或 owner。

Guru Trellis 下一阶段产品进化 Requirements 的唯一文档集位于
[`evolution/`](./evolution/README.md)，主定义为
[`evolution/requirement-main.md`](./evolution/requirement-main.md)，
其中 `EVO-001..007` 为 `user_confirmed` 目标，`REQ-UC-EVO-*`、`EVO-REQ-*`、
`EVO-NFR-*` 与 `EVO-CAP-*` 为待完成全稿审核的详细需求。它定义 target，不把尚未
实现的方向冒充 current behavior。target authority、现有 Issue 链边界与阶段放行规则只在
该主定义第 0 章维护，README 不复制正文。

Evolution Requirements 的入口/API/CLI 适用性只在 target
[`README.md`](./evolution/README.md) 与主定义中维护。

target 读取顺序：`evolution/requirement-main.md` ->
`evolution/requirement-non-functional.md`。current runtime 读取顺序：`requirement-main.md` ->
`requirement-non-functional.md` -> `traceability.md` -> `decisions.md`。Design、Test
与 Architecture 入口分别位于 `docs/design/README.md`、`docs/test/README.md`、
`docs/architecture/README.md`。

普通 task 不直接修改 shared current authority；先由 `guru-maintain-requirements-design-test-ssot:task_impact_sync` 判定 contribution/direct sync，再通过 `promotion` 激活。结构冲突或过期状态走 `repair`。

旧路径 `requirement-main.md` 与 `guru-team-trellis-flow.md` 仅保留迁移导航，不定义 current。
