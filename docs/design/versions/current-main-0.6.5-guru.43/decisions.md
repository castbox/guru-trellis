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
- `DDEC-011`（accepted）：`.39` current docs 可以记录 preparation/source proof，但 `v0.6.15-guru.3` stable tag/Release、tag-pinned install 与 post-publish smoke 只能由 #267 exact-candidate Release lifecycle 晋升。
- `DDEC-012`（accepted）：Architecture Baseline 与 Guru Team lifecycle 保持双维 authority，只在 task-local change contract 相交；项目 constitution/change contract 拥有具体语义，public package只拥有 shape、stage routes 与 deterministic validation。
- `DDEC-013`（accepted）：shared Architecture/RDT current 只由各自 semantic owner在 independent review 后串行 promotion；Architecture promotion 必须绑定 expected current 且强制 post-promotion Phase 2/commit/Branch Review。
- `DDEC-014`（accepted historical #267 contract）：`.42` 是 #267 完成时的 knowledge identity，extension candidate 为 `0.6.15-guru.39`；当前 `.43` 继承 knowledge/release identity separation，knowledge promotion 不隐式授权 push、tag、GitHub Release 或 Issue closure。
- `DDEC-015`（accepted historical #267 contract）：#267 promotion 由 Architecture owner 激活统一 `.42` baseline，随后由 RDT owner 建立完整 `.42` versioned authority；两步均绑定当时 expected `.41`，且 promotion-created diff 重新进入 Phase 2、commit 与 Branch Review。该 `.42` authority 现为 `.43` 的 superseded predecessor。
- `DDEC-016`（accepted）：`guru-sync-base` 以 selection -> authority binding 两阶段实现 detached normal path；worktree inventory 只服务 selected-base 后的 exact binding，不成为 base selection authority，也不引入 fallback、dual-read 或第二 resolver。
- `DDEC-017`（accepted）：Finalizer 使用独立 target/source checkout 与 closed mode binding，删除
  installed single-checkout 假设；verifier structured failure evidence 由 verifier 自治，不形成 shared
  resolver 或跨 lifecycle owner。
- `DDEC-018`（accepted）：`release-guru-trellis-version` 是 repo-private semantic orchestration，
  不新增公共 package/interface/schema/typed exit 或确定性发布脚本；它只按阶段调用既有 lifecycle
  owners，并保持每个外部 mutation 的独立确认与 live-fact recovery。
- `DDEC-019`（accepted）：preparation delivery content 与 lifecycle metadata 分离。最终内容提交后只需
  一次完整 Branch Review；Publication/Finalizer 的 owner-private checkpoint 不改变 reviewed-content
  identity，任何实际 delivery/durable/config/script/test bytes 变化仍使相应 gate stale。
