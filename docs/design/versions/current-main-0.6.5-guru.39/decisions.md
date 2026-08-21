# Design 决策

- `DDEC-001`（accepted）：文档只索引 registry/interface，不复制 schema 字段，避免 drift。
- `DDEC-002`（accepted）：current as-built 与 released tag 分开建模；manifest revision 不等于 release。
- `DDEC-003`（accepted）：Bootstrap 不合并 RDT 与 Architecture owner，只编排 minimal typed outputs。
- `DDEC-004`（accepted）：`.trellis/spec` 是 locator/usage projection，不是第三 authority。
- `DDEC-005`（inferred, not current）：未来 Phase owner 解耦可能改变 orchestration；在独立 Issue 接受前只列 GAP/TARGET。
- `DDEC-006`（accepted）：Finalizer terminal public projection 使用精确 retired locator、durable archive summary 与 current ready facts；不恢复已退休的进行中 gate/transaction/plan，也不放宽真实 stale 校验。
- `DDEC-007`（accepted）：verifier inventory 只消费 canonical registry/interface validation，不维护固定数量副本。
- `DDEC-008`（accepted）：完整 compatibility matrix 使用 live-derived declared platforms，每个 cell 同时安装 shared `.agents` public projection 与唯一 selected platform projection。
- `DDEC-009`（accepted）：existing migration 以 `v0.6.5-guru.10` 为 immutable before-state；official update 产生的已知 replacement `.bak` 必须逐项 reconciliation，最终 recursive sidecar count 为 0。
- `DDEC-010`（accepted）：A/B compatibility 与真实 GitHub A route 是验证 harness，不新增 #248 Acceptance 或 #252 cleanup public API。
- `DDEC-011`（accepted）：`.37` current docs 可以记录 `public_plus_local_candidate` proof，但 stable tag/Release 与 tag-pinned install conclusion 只能由 #267 晋升。
- `DDEC-012`（accepted）：Architecture Baseline 与 Guru Team lifecycle 保持双维 authority，只在 task-local change contract 相交；项目 constitution/change contract 拥有具体语义，public package只拥有 shape、stage routes 与 deterministic validation。
- `DDEC-013`（accepted）：shared Architecture/RDT current 只由各自 semantic owner在 independent review 后串行 promotion；Architecture promotion 必须绑定 expected current 且强制 post-promotion Phase 2/commit/Branch Review。
- `DDEC-014`（accepted）：`.39` 是 current knowledge identity，extension candidate 继续为 `0.6.5-guru.37`；knowledge promotion 不隐式授权 version bump、push 或 release。
- `DDEC-015`（accepted）：`guru-sync-base` 以 selection -> authority binding 两阶段实现 detached normal path；worktree inventory 只服务 selected-base 后的 exact binding，不成为 base selection authority，也不引入 fallback、dual-read 或第二 resolver。
