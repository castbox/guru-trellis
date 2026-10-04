# #490 Reference-only Creation Test Strategy

State: task-owned evidence; passing commands do not replace independent Phase 2/Branch Review or owner promotion.

- `T490-01`: Execute production create-task shell wrapper, official task writer, read-only result recovery and establish-task-identity shell wrapper in real Git fixtures for exact_source, reference_only and no_issue. Compare actual source identity and TaskId/generation/TaskRef; recovery preserves metadata bytes.
- `T490-02`: Current C6 composition accepts both Issue dispositions and still rejects follow_up/parent creation; current lifecycle session, branch, checkout/resource and source readers retain their regression behavior.
- `T490-03`: Closure regression uses official current metadata and proves reference-only/no-Issue no_mutation without provider calls; unsupported legacy source records remain unchanged and rejected. No runtime closure rule is weakened.
- `T490-04`: Exact-source validator proves HEAD/tree/parents, live successful CI, CLI/core versions and real normal-build marker. Official projection verifies actual scripts/platform bytes and hashes independently of Guru drift.
- `T490-05`: Canonical/source, installed and declared Claude/Codex/Cursor projections pass validation and dogfood drift. One Codex focused install proves clean init, initial preset, same-candidate update/reapply, source provenance, native projection load and zero sidecars.

## Evidence at implementation

- Public creator/source fixtures and create-task suite: 16 tests passed against merged Fork.
- Current task lifecycle regression: 152 tests passed.
- Dogfood behavior/projection unit tests: 9 passed, including actual reference_only creation.
- Source-backed official projection: 183 files, expected Fork identity and live main CI, status ok.
- Source package validation and dogfood drift: passed; selected native roots Claude/Codex/Cursor match canonical.
- Closure regression: 18 passed using official current task metadata; reference-only/no-Issue no_mutation and exact-source closure retained.
- Focused Codex installation: passed for local marketplace sample clean init, initial preset, two same-candidate update/reapply operations, session binding and zero sidecars; native_load is projection_parity. This does not establish remote marketplace or native-host execution.

Full multi-platform/native-host release matrix, predecessor 0.6.17 refusal/no-write proof, public remote marketplace, tag smoke, Release and production installation remain unverified here and owned by #489.

Promotion：current authority 为三层 `current-main-0.6.17-guru.71`，完整有效 `.70` 合同以薄继承保留；本贡献作为历史来源。promotion-created diff 须 fresh Phase2/commit/独立完整BranchReview；验证边界不变。
