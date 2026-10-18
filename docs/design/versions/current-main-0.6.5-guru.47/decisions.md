# Design 决策

当前 .47 来源：`castbox/Trellis@ad332e3fe5a19d7274cb03e7c2f3e2128f8de291` / CLI/core `0.6.16`；Guru manifest `0.6.15-guru.40`。Architecture public inheritance：`docs/architecture/README.md` / `current-main-0.6.5-guru.47` / `active`。
继承段落中的旧版本映射、矩阵及历史 promotion 只绑定其原版本，不声明当前 Fork 的完整兼容或 Release；当前 #378 增量见本文件末节及同版本 traceability。


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
- `DDEC-011`（accepted historical boundary）：`.39` docs 可以记录 #267 preparation/source proof，但
  `v0.6.15-guru.3` tag/Release、tag-pinned install 与 post-publish smoke 只能由其历史 exact-candidate
  lifecycle 晋升，不能替代 #332 `.5/.40` evidence。
- `DDEC-012`（accepted）：Architecture Baseline 与 Guru Team lifecycle 保持双维 authority，只在 task-local change contract 相交；项目 constitution/change contract 拥有具体语义，public package只拥有 shape、stage routes 与 deterministic validation。
- `DDEC-013`（accepted）：shared Architecture/RDT current 只由各自 semantic owner在 independent review 后串行 promotion；Architecture promotion 必须绑定 expected current 且强制 post-promotion Phase 2/commit/Branch Review。
- `DDEC-014`（accepted historical #267 contract）：`.42` 是 #267 完成时的 knowledge identity，extension
  candidate 为 `0.6.15-guru.39`；当前 `.44` 继承 knowledge/release identity separation，knowledge
  promotion 不隐式授权 push、tag、GitHub Release 或 Issue closure。
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
- `DDEC-020`（accepted）：#332 authority promotion 更新 current release facts、
  history/navigation/traceability 与 evidence，并把 #240/#348 已合入、已独立审查的 owner/RDT/ADR
  authority 串行提升到 `.44`；不新增实现、第二 current writer、GAP 或 compatibility path。#311 的正式
  release 安装态 proof 由 #332 exact candidate fresh 承接。
- `DDEC-021`（accepted）：Release Gate evidence 以 post-merge fresh main candidate 为唯一聚合 identity；
  preparation、historical focused 或 package evidence 只作定位，不可跨 SHA 晋升。tag、immutable-tag smoke、
  GitHub Release、Issue closure 与 cleanup 保持独立 mutation owner 和确认边界。
- `DDEC-022`（accepted）：#240 采用独立 scenario/mechanism semantic owners；机制 owner 禁止 OS primitive
  承接业务 authority，正式决策为 `ADR-008`。
- `DDEC-023`（accepted）：#348 在现有 lifecycle recovery model 内拆分 Merge classification 与 archived-task
  restoration owner；该缺失恢复边不改变既有 architecture decision，因此不新增 ADR。
- `DDEC-024`（accepted）：#332 使用 `dedicated_refactor_slice` 将 PR #341 的第二 public facade 层收敛
  回四个原 command；Interface 独占 wrapper path，compatibility 只由旧参数触发。该修正恢复既有设计宪法，
  不新增 ADR、owner、GAP 或第二 current writer。
- `DDEC-025`（accepted）：#376 使用 `target_native` 在既有 Reconcile owner 内增加 package-private
  expected-head executor，并由 Review Branch 承接 bounded continuity。prior full review 与 current reconciled
  HEAD 分离建模，Finalizer-to-Reconcile 使用显式 public projection；该直接演进不新增兼容分支、第二状态机、
  owner、GAP、ADR 或 remote writer。

- `DDEC-026`（accepted）：#378 复用 Fork 自身构建、Node CLI、原 verifier 和现有 snapshot promotion，不引入第二框架、launcher 或基础设施；source lock 单一拥有来源，installed record 仅为受管投影。构建标记只校验普通 source/build mismatch；#388/#389 和既有 semantic owners 不变。
