# CURRENT

以下事实只绑定 current source/release evidence，不推断未来能力。

- `ARCH-CUR-001`（`code_recovered`）：main baseline `5c059f49…` + #260 compatibility task delta（精确 revision 为当前 Git HEAD）包含 21 个 active Skill packages；registry 统一指向 interface/route/platform，20 个 integrated，`guru-verify-extension-installation` 为 `standalone_only`。
- `ARCH-CUR-002`（`code_recovered`）：global workflow 实现四 Phase，canonical package 位于 `trellis/**`，dogfood/installed 位于 `.trellis/**`，平台投影覆盖 Shared/Codex/Claude/Cursor。
- `ARCH-CUR-003`（`code_recovered`）：RDT、Architecture Baseline、Repository Bootstrap 三个 semantic package 已 active，分别源自 #263/#264/#265。
- `ARCH-CUR-004`（`source_confirmed` + `verified`）：current extension candidate 为 `0.6.5-guru.37`，target/tested Trellis CLI 为 `0.6.15`。
- `ARCH-CUR-005`（`source_confirmed`）：最新 stable Release 为 annotated tag `v0.6.5-guru.10`，tag object `b5fd47e9…`，peeled commit `5c059f49…`；它是 `.36` / Trellis `0.6.5` released history，不等于 current main candidate。
- `ARCH-CUR-006`（`code_recovered`）：preset/overlay 管理 `.trellis/guru-team/`、Guru Skills、平台 skills 与 finish-work entries；unknown local changes 使用 `.new/.bak` 保护语义。
- `ARCH-CUR-007`（`code_recovered`）：Finalizer terminal projection 以精确 retired locator、六文件 archive summary 与 current local/remote/Ready PR/scope facts 共同构成 authority；archive 不替代 live provider，任何真实 drift fail closed。
- `ARCH-CUR-008`（`verified`）：current source 与 dogfood 的 official Trellis target/project version 为 `0.6.15`；canonical extension candidate 为 `0.6.5-guru.37`。
- `ARCH-CUR-009`（`verified`）：compatibility verifier 从 live registry/interface/manifest/ownership 生成 capability projection；六个 cell 的 active ids、interfaces、schemas、exits、commands、consumers、routes、managed paths、modes、template hashes 与 Docs locators 没有未审查 loss。
- `ARCH-CUR-010`（`verified_external`）：经单独确认的 disposable GitHub A route 以 source head `6a7b721a…` 完成 PR #2 expected-head rebase merge与 Issue #1 closure；provider failure 在同一 Finalizer transaction 恢复，remote branch/repository cleanup 后 retained-ref reachability 仍通过。

当前不声明 `.37` 已发布、tag-pinned `.37` install 或 release smoke 已通过；这些发布事实仍由 #267 独占。
