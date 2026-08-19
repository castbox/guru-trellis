# CURRENT

以下事实只绑定 current source/release evidence，不推断未来能力。

- `ARCH-CUR-001`（`code_recovered`）：main baseline `c2b17846…` + #275 uncommitted task delta 包含 21 个 active Skill packages；registry 统一指向 interface/route/platform，20 个 integrated，`guru-verify-extension-installation` 为 `standalone_only`。
- `ARCH-CUR-002`（`code_recovered`）：global workflow 实现四 Phase，canonical package 位于 `trellis/**`，dogfood/installed 位于 `.trellis/**`，平台投影覆盖 Shared/Codex/Claude/Cursor。
- `ARCH-CUR-003`（`code_recovered`）：RDT、Architecture Baseline、Repository Bootstrap 三个 semantic package 已 active，分别源自 #263/#264/#265。
- `ARCH-CUR-004`（`source_confirmed`）：extension manifest 为 `0.6.5-guru.36`，target/tested Trellis CLI 为 `0.6.5`。
- `ARCH-CUR-005`（`source_confirmed`）：最新 stable Release 为 `v0.6.5-guru.9`，tag commit `56b5f411…`；它是 released history，不等于 current main。
- `ARCH-CUR-006`（`code_recovered`）：preset/overlay 管理 `.trellis/guru-team/`、Guru Skills、平台 skills 与 finish-work entries；unknown local changes 使用 `.new/.bak` 保护语义。
- `ARCH-CUR-007`（`code_recovered`）：Finalizer terminal projection 以精确 retired locator、六文件 archive summary 与 current local/remote/Ready PR/scope facts 共同构成 authority；archive 不替代 live provider，任何真实 drift fail closed。

当前不声明 Trellis `0.6.15` compatibility、#260/#267 完整多平台矩阵或 `v0.6.5-guru.10` 已发布；#275 candidate 在 exact gate、合并、tag、smoke 与 Release 完成前保持 unreleased。
