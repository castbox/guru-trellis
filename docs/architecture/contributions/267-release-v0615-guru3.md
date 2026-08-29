# #267 Release authority alignment Architecture contribution

## Candidate identity and authority boundary

- candidate identity：`architecture-contribution-267-release-authority-alignment-v1`。
- requirement authority：live Issue #267 `2026-08-29-r18` 与 task `prd.md`。
- behavior authority：task `design.md`、`implement.md` 与 RDT contribution。
- source/expected current：`docs/architecture/README.md` /
  `current-main-0.6.5-guru.41` / `active`。
- candidate successor：`current-main-0.6.5-guru.42`。
- design constitution：`docs/architecture/00-foundation/design-constitution.md` /
  `guru-trellis-design-constitution-v1` / `current`。
- project change contract：`docs/architecture/06-governance/change-contract.md` /
  `guru-trellis-architecture-change-contract-v1` /
  `guru-trellis-architecture-change-concerns-v1`。
- change path：`target_native`；promotion state：`reviewed_promoted`；ADR：
  `required=false`。

该 task-owned candidate 已通过独立 committed full-diff Branch Review，并由 serialized
Architecture promotion owner 绑定 expected `.41` 激活为 shared current `.42`。promotion-created
diff 的 fresh Phase 2、commit 与 Branch Review 仍待执行。

## Boundary and decision

初始 release preparation commit 已将 canonical manifest 更新为 `0.6.15-guru.39`，但
active `.41` Architecture/RDT authority 仍将 current/canonical extension candidate 记录为
`0.6.5-guru.37`。这使 CURRENT fact 与 committed source evidence 冲突，并阻断 Branch Review。

目标边界只建立 `.42` successor knowledge authority，将 current release/candidate facts 对齐到
`.3/.39/CLI 0.6.15`，保留 `.41` 为 superseded history。它不改变 Architecture decision、
constitution、owner topology、single-writer、runtime boundary、GAP lifecycle 或 compatibility
exit，因此不创建 ADR。

## Required concern review

| Concern | Applicability | #267 contract |
| --- | --- | --- |
| `authority-binding` | `applicable` | 绑定 Architecture 2.0、active `.41`、r18 与 project change contract v1 |
| `constitution-binding` | `applicable` | 命中 concept completeness、cohesion/change isolation 与 one-way convergence；constitution identity 不变 |
| `boundary-and-decision` | `applicable` | `target_native` 只晋升 current knowledge facts，不新增运行时或公共合同路径 |
| `owner-and-single-writer` | `applicable` | task worktree 写 contribution；serialized promotion owner 单写 shared current |
| `compatibility-and-exit` | `applicable` | `target_native` 不引入 legacy/adapter/dual-read；runtime/public API 与既有 compatibility exit 保持不变，并由各阶段 fresh diff 复核 |
| `gap-and-deviation` | `applicable` | 关闭 `.39/.37` authority conflict，不关闭或改变现有 Architecture GAP |
| `parallel-scope` | `applicable` | contribution 阶段禁止 shared-current edit；promotion 绑定 expected `.41` |
| `evidence-and-freshness` | `applicable` | 绑定 live r18、committed manifest、active `.41`、contribution diff 与后续 exact ranges |
| `review-and-promotion` | `applicable` | contribution review 后 promotion；promotion-created diff 再走 Phase 2/commit/Branch Review |

## Before and after

- before：canonical manifest 为 `0.6.15-guru.39`；active `.41` CURRENT/RDT facts 仍声明
  current candidate `0.6.5-guru.37`。
- after：`.42` 是唯一 active Architecture/RDT knowledge authority，current/canonical candidate
  为 `0.6.15-guru.39`，CLI 为 `0.6.15`；`.41` 是 superseded history。
- preserved：release target `.3`、#311/#312 implementation、runtime graph、public Skill I/O、
  constitution、Architecture decision/owner/GAP/compatibility 与 Issue closure scope。

## Project check

- descriptor：`guru-trellis-architecture-convergence:repository:1` /
  `guru-trellis-architecture-convergence@1`。
- refs：`ARCH-GOV-006..008`、`ADR-005`、`ARCH-GAP-006`。
- Planning evidence：live Issue #267 r18、task planning、manifest `.39`、active `.41`
  Architecture/RDT authority、本 Architecture contribution 与 RDT contribution。
- Planning result：`pass / blocking=true`。一个 task writer、一个 serialized promotion writer、
  一个 `.42` successor、无 ADR、无 dual authority、无 compatibility layer；shared current 在
  contribution review 前保持不变。
- Phase 2 result：`pass / blocking=true`。完整 current worktree candidate 的 task/YAML、
  RDT traceability、shared-current boundary、secret/path/residue 与 diff 校验均通过；
  Architecture owner 返回 `baseline_current / architecture_impact / target_native /
  reviewed_candidate`，未发现新增或恶化 deviation、owner expansion、dual writer、公共 API
  或 compatibility 变化。该结果不替代后续独立 committed full-diff Branch Review。
- Phase 2、Branch Review、promotion 与 post-promotion review 必须分别使用 fresh candidate/
  committed-range evidence，不复用 Planning judgment。

## Review and promotion state

- review：`reviewed`；exact committed range 为
  `3efcce72a0d47e38ec725aa8c0f8498992f3416f...d3dca74b3a94569a095594477c15b032526f2381`，
  Architecture Branch Review 与 independent Branch Review 均 passed，open P0-P3 为零。
- ADR：`required=false`。
- expected current：`current-main-0.6.5-guru.41`。
- candidate successor：`current-main-0.6.5-guru.42`。
- promotion：`reviewed_promoted`；`shared_current_write=true`；promoted identity：
  `current-main-0.6.5-guru.42`。
- live current advance、finding、project-check failure 或 stale contribution 返回对应 owner route，
  不覆盖 shared current。
