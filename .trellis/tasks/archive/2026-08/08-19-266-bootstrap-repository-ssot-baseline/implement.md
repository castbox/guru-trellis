# #266 实施计划

## 1. Fresh authority 与分析

- [ ] 重新 fetch 并确认 `origin/main`、Issue #266、#263/#264/#265、PR #280、release/tag/manifest。
- [ ] 读取 current workflow、registry/interface/schema/runtime/preset/overlay/installer/platform/tests。
- [ ] 读取现有 docs/spec、task archive、finish-summary/history，并建立 provenance 清单。
- [ ] 从 live registry/interface 派生 active capability/command/schema/exit/platform inventory。

## 2. 执行 existing_repository Bootstrap

- [ ] 按 upstream `trellis-spec-bootstrap` 完成 current codebase-backed spec analysis。
- [ ] 建立 versioned Requirements SSOT 与 README/version matrix/traceability/decisions。
- [ ] 建立 versioned Design SSOT 与 manifest/traceability/decisions/capability owner map。
- [ ] 建立 versioned Test Strategy/Test Plan 与 evidence classification/acceptance mapping。
- [ ] 建立 Architecture Baseline FOUNDATION/CURRENT/TARGET/DOMAIN/INTEGRATION/GAP/
  GOVERNANCE/PLAN/ADR/EVIDENCE。
- [ ] 吸收、引用化或历史化旧 requirements docs，消除双 current authority。
- [ ] 更新最小 `.trellis/spec/docs` 与 `.trellis/spec/architecture` projection。

## 3. Semantic reviews

- [ ] 分别 review Requirements/Design/Test 与 Architecture Baseline 的 completeness/status/provenance。
- [ ] review cross-SSOT behavior/version/CURRENT/TARGET/GAP/traceability consistency。
- [ ] 确认无 runtime/product/public identity diff，无 proposed future 机制冒充 CURRENT。
- [ ] 仅在 locator/status/link/freshness 有效且无 blocking finding 时激活。

## 4. Focused validation

- [ ] Markdown/path/link/placeholder/heading/structure checks。
- [ ] `.trellis/spec` index 与 `get_context.py` dogfood context loading。
- [ ] registry/interface/manifest/workflow marker 与 capability inventory consistency。
- [ ] fresh 回读 #263/#264/#265 focused evidence，记录 exact source/HEAD/result/unverified boundary。
- [ ] `git diff --check` 与 Issue-owned docs/spec scope check。
- [ ] 不运行 full multi-platform Throwaway、v0.6.15 upgrade 或 exact candidate Release Gate。

## 5. 完整交付门禁

- [ ] `guru-check-task` 完整审查本 task scope。
- [ ] 创建语义明确的 task commit，仅 stage 本 task 文件。
- [ ] 独立 `guru-review-branch` 覆盖 `origin/main...HEAD` 全量 docs/spec diff。
- [ ] 完成 publication readiness，PR 标题/正文为中文，仅 `Closes #266`。
- [ ] 通过 Finalizer/merge identity 后，向 coordinator 仅询问 `合并PR`。
- [ ] merge 后核对 Issue closure、finish/archive/history query 与 dedicated resource cleanup。

## 风险点

- 历史证据 stale：降级为 `unverified`，不得写 PASS。
- current/released version 混淆：README/version matrix 必须分开标记。
- 文档重复：以 canonical versioned path 为唯一正文，旧路径只做导航/历史。
- scope 膨胀：发现 runtime/API defect 立即停止该修复，仅记录 GAP/owner。
