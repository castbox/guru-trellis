# #410 Release v0.6.17-guru.1 Requirements contribution

状态：`reviewed_promoted`；前序 released tag：`v0.6.16-guru.1`。

- `R410-01`: canonical extension manifest、dogfood projection 与 current public
  release-facing docs must converge on `0.6.17-guru.42`.
- `R410-02`: current stable installation instructions must target
  `v0.6.17-guru.1`; historical `v0.6.16-guru.1` facts remain immutable.
- `R410-03`: Trellis CLI/core remains `0.6.17` and the accepted framework source
  lock remains explicit and unchanged unless live authority requires otherwise.
- `R410-04`: existing Skill IDs, exits, schemas, commands, template IDs, and
  ownership boundaries remain compatible.
- `R410-05`: Stage 1 requires fresh post-promotion Phase 2, task commit, and
  complete `origin/main...HEAD` Branch Review before Publication.
- `R410-06`: Stage 2 freezes one fresh `origin/main` commit/tree; all release
  gates, tag, smoke, Release, and Issue closure must bind to that identity.
- `R410-07`: release mutations remain independently confirmed and no release
  lifecycle state, authorization, or dynamic gate history is tracked.

`BEH-018`: any required FAIL, SKIP, stale, cross-identity, or unmapped result
stops the release at its owning gate.
