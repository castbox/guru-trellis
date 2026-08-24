# #304 Release readiness blockers 修复需求

## Goal

修复 exact candidate `9c5fe383a4ec4d85b6ee0958419f9cc2b88b30c9` 的两项 Release blocker，使后续重新冻结的 `v0.6.15-guru.1` candidate 在 tag 内提供正确安装入口，并让 current `.40` Requirements/Design/Test/Architecture authority 与 verifier 已实现的 capability-loss 边界一致。

## Authority And Confirmed Facts

- Authority：Issue #304 及 2026-08-24 Release-readiness amendment：<https://github.com/castbox/guru-trellis/issues/304#issuecomment-5397540565>。
- Branch Review verifier correction authority：2026-08-24 amendment：<https://github.com/castbox/guru-trellis/issues/304#issuecomment-5398166538>。
- 目标 stable identity：repo tag `v0.6.15-guru.1`、extension revision `0.6.5-guru.37`、official Trellis CLI `0.6.15`。
- Branch Review 已确认 `verify_trellis_compatibility_matrix.py::compare_capabilities` 仍把 `extension_identity` 放入 `blocking_differences` 并令 `capabilities_preserved=false`；本 task 必须最小修正该 stale classification。
- 内部 Skill API/schema、distribution 与 installed-file inventory 仍由 package、projection、consistency、installation、mode 和 sidecar gates 验证，但变化本身不构成 capability loss。
- `v0.6.5-guru.10` / extension `.36` / Trellis `0.6.5` 仍是 existing-upgrade cell 的 immutable before-state；此历史用途不能被批量替换。
- 当前 target tag 和 GitHub Release 尚不存在；本 task 不发布它们。

## Requirements

### R1 Release-facing installation identity

更新以下三份 README 的当前 stable identity、首要 install、workflow bootstrap/switch 与 clone 命令，使新 immutable tag 内的用户入口统一指向 `v0.6.15-guru.1` 和 CLI `0.6.15`：

- `README.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`

不得把尚未创建的 tag object、peeled commit 或 Release 状态写成已验证事实。

### R2 Historical before-state preservation

仅当文本明确描述 existing migration、replacement history 或 immutable before-state 时，保留 `v0.6.5-guru.10`、`.36` 与 CLI `0.6.5`。所有面向当前安装、切换或 clone 的命令不得继续指向旧 stable。

### R3 Capability-loss authority repair

修正 current `.40` RDT authority，使 capability-loss comparison 只拥有：

- `workflow`
- `task_data`
- `docs_authority`

`skill_api`、interface/schema/command projection、distribution、managed path/file inventory、mode、template hash、sidecar 与 extension identity/version binding 保持独立 consistency/installation blockers，不再被称为 capability loss。

### R4 Architecture authority repair

同步 Architecture current/integration/evidence 中同一边界。该修订只纠正验证分类，不改变系统边界、owner、public API、workflow、runtime、single-writer 或 compatibility exit；不创建 Architecture contribution 或 ADR。

### R5 Scope discipline

除 `compare_capabilities`、其 source/installed matrix consumer 与 owning test 的最小修正外，不修改其它 verifier、workflow 行为、public Skill API/schema/command、安装文件清单、manifest、preset overlay、candidate 功能代码或其它无关文档。`.trellis/spec` 只有在发现当前 projection 自身包含相反定义时才同步。

## Acceptance Criteria

- AC1：三份 README 的当前 stable identity 和当前 install/switch/clone 命令均指向 `v0.6.15-guru.1`、extension `.37`、CLI `0.6.15`。
- AC2：旧 stable 只出现在明确的历史/replacement/existing before-state 上下文，不再作为当前安装入口。
- AC3：`REQ-013`/`REQ-018`、`DES-010`/`DES-016`、`TST-015`/`SCN-013`、test plan/traceability 与 Architecture authority 对 capability loss 和 consistency/installation 的职责划分一致。
- AC4：verifier 的 `blocking_differences` 与 `capabilities_preserved` 只由 `workflow`、`task_data`、`docs_authority` 决定；extension identity before/after 与一致性结论独立表达，并由 source/installed matrix consumer 的独立错误路径继续 fail closed；API/schema/distribution 变化仍由独立 gate 覆盖。
- AC5：task validation、文档/链接定向检查、source package validation、dogfood drift 与 `git diff --check` 通过；未运行的完整 Release matrix 明确留给 #304 重新冻结后的 Release gates。
- AC6：diff 除授权的 verifier/owning-test 最小修正外，不包含 workflow、public Skill API/schema/command、manifest、installer inventory、overlay 或其它功能代码变化。

## Out Of Scope

- 修改 `compare_capabilities`、其两个直接 matrix consumer 和 owning test 之外的 verifier/runtime 实现。
- 新增、删除或迁移 Skill/API/schema/command/managed file。
- 执行完整 multi-platform Release matrix。
- commit、push、PR、merge、tag、GitHub Release、Issue closure 或资源清理。
- 修改 #247/#249/#250/#292/#293/#261/#248/#252/#267 或 Known Issues。

## Open Questions

无。Issue amendment、live source、official Trellis extension model 与 current verifier 已共同确定所需边界。
