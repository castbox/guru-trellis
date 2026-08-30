# Requirements SSOT

本目录是 Guru Team Trellis Extension 的唯一 Requirements authority。运行时行为仍由 canonical workflow 与 Skill package 定义；task-local `prd.md` 只描述单次变更，不是产品需求 authority。

## 当前入口与版本矩阵

| 状态 | 版本 | Locator | Provenance |
| --- | --- | --- | --- |
| `active` | `current-main-0.6.5-guru.42` | [requirement-main.md at selected base](https://github.com/castbox/guru-trellis/blob/9f560ec191851f82768d5e7aa031e6d852c34f14/docs/requirements/versions/current-main-0.6.5-guru.42/requirement-main.md) | #267 reviewed release-authority alignment，绑定 task head `d3dca74b…` + expected `.41` serialized promotion delta；#305 已确认的 `EVO-001..007` 保持独立 target authority |
| `superseded` | `current-main-0.6.5-guru.41` | [requirement-main.md](./versions/current-main-0.6.5-guru.41/requirement-main.md) | #311 reviewed Architecture/RDT promotion |
| `superseded` | `current-main-0.6.5-guru.40` | [requirement-main.md](./versions/current-main-0.6.5-guru.40/requirement-main.md) | #295 reviewed Architecture/RDT promotion + #305 target delta |
| `superseded` | `current-main-0.6.5-guru.39` | [requirement-main.md](./versions/current-main-0.6.5-guru.39/requirement-main.md) | #290 reviewed Architecture/RDT promotion |
| `superseded` | `current-main-0.6.5-guru.38` | [requirement-main.md](./versions/current-main-0.6.5-guru.38/requirement-main.md) | #283 reviewed Architecture/RDT promotion |
| `superseded` | `current-main-0.6.5-guru.37` | [requirement-main.md](./versions/current-main-0.6.5-guru.37/requirement-main.md) | #260 verified compatibility；extension candidate 仍为 `0.6.5-guru.37` |
| `superseded` | `current-main-0.6.5-guru.36` | [requirement-main.md](./versions/current-main-0.6.5-guru.36/requirement-main.md) | #275 replacement release 后的 immutable before-state authority |
| `superseded` | `current-main-0.6.5-guru.35` | [requirement-main.md](./versions/current-main-0.6.5-guru.35/requirement-main.md) | #266 激活的历史 current snapshot |
| `released` | `v0.6.5-guru.9` | [requirement-main.md](./versions/v0.6.5-guru.9/requirement-main.md) | `source_confirmed`，tag commit `56b5f411…` |

当前 main 已验证 official Trellis `0.6.15` compatibility。current source candidate 为
extension `0.6.15-guru.39`，#267 successor Release target 固定为 tag
`v0.6.15-guru.3`；stable tag、GitHub Release、tag-pinned install 与 post-publish smoke
仍为 `unverified`，只能由 #267 exact-candidate Release lifecycle 晋升。#311 的正式 `.3`
业务仓安装与原错误路径重试保持独立 post-release proof。

Guru Trellis 下一阶段产品进化 Requirements 的唯一文档集位于
[`evolution/`](./evolution/README.md)，主定义为
[`evolution/requirement-main.md`](./evolution/requirement-main.md)，
其中 `EVO-001..007` 为 `user_confirmed` 目标；`REQ-REV-133..138` 已把 #311/#312 定义为 Evolution
Design/runtime 前置，并从 selected base 完成 `.41` RDT/Architecture/inventory rebind：#311 作为
`CUR-CAP-013/014/017/018/019` 的 current observable capability 承接，#312 作为 `CUR-CAP-012` 的
current base-continuity capability 承接。当前 candidate 已建立 52 UC / 83 REQ / 33 NFR / 23 current
capabilities / 13 target deltas / 50 normal-path fixtures 的零差集 closure，并针对同一 exact identity 通过
fresh Requirements semantic、Strict technical 与确定性闭包审核。Requirements 阶段状态为
`requirements_ready_for_design` / `requirements_trace_ready_for_design`；其后的 fresh Design 已分配全部
73 个 Design responsibilities 与 50 个 fixture mappings，并以全稿审核和确定性闭包单独放行 runtime
refactor。该文档集定义 target，不把 OPEN Issue、旧 snapshot 或尚未实现的方向冒充 current behavior；
pre-`REQ-REV-133` 的历史 `design_ready_for_delivery_planning` 结论仍然失效，`docs/design/evolution/` 当前为
`design_ready_for_delivery_planning` / `fresh_design_review_passed` / `evolution_refactor_eligible`。target
authority、Issue 链边界与阶段放行规则只在
Requirements 主定义第 0/10 章维护，README 不复制正文。

Evolution Requirements 的入口/API/CLI 适用性只在 target
[`README.md`](./evolution/README.md) 与主定义中维护。

target 读取顺序：`evolution/requirement-main.md` ->
`evolution/requirement-non-functional.md` -> `evolution/current-capability-inventory.md`；其中
inventory 只承接 current-to-target trace，不替代前两份 Requirements 主定义。current runtime 读取顺序：`requirement-main.md` ->
`requirement-non-functional.md` -> `traceability.md` -> `decisions.md`。Design、Test
与 Architecture 入口分别位于 `docs/design/README.md`、`docs/test/README.md`、
`docs/architecture/README.md`。

普通 task 不直接修改 shared current authority；先由 `guru-maintain-requirements-design-test-ssot:task_impact_sync` 判定 contribution/direct sync，再通过 `promotion` 激活。结构冲突或过期状态走 `repair`。

旧路径 `requirement-main.md` 与 `guru-team-trellis-flow.md` 仅保留迁移导航，不定义 current。
