# #274 实施计划

## 1. Canonical producer 修复

- [ ] 在 `trellis/skills/guru-team/packages/guru-review-contract-wording/runtime/common.py` 增加唯一 title/body resolver 与 canonical digest helper。
- [ ] 在 `runtime/invoke.py` 删除 body-only `next(...)`，一次计算 target content digest，并写入 transition 顶层与内嵌 wording projection。
- [ ] 保持 public schema、Interface、typed exits、consumer mapping 和 readiness runtime 不变。

## 2. Focused package regression

- [ ] 扩展 `guru-review-contract-wording/tests/test_contract.py`，覆盖唯一 title/body 的 canonical 组合摘要。
- [ ] 分别覆盖 missing title、missing body、duplicate title、duplicate body，并断言 `stale_identity` 与 `owner_result.scope`。
- [ ] 保留 explicit-path、receipt、content drift、Gate/exit relation 和 package-local runtime 现有回归。

## 3. Cross-package Stage 0 regression

- [ ] 修改 `verify_installed_phase0_transcript.py`，readiness prerequisites 直接使用实际 wording public transition 的内容身份。
- [ ] 删除 caller 从 wording owner scope 手工重算 title/body digest 的路径。
- [ ] 证明原样 transition 通过 production readiness recorder/checker 与 public invoke。
- [ ] 增加 title-only 与 body-only drift 负例，证明旧 transition 不能匹配新 current source。

## 4. Durable docs 与 projection 同步

- [ ] 更新 wording package contract，明确唯一 title/body 与 canonical digest。
- [ ] 更新 canonical preset `data-contracts.md`，明确 `wording_current.target_content_sha256` 的 consumer-facing 语义。
- [ ] 运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`。
- [ ] 检查 `.new`、`.bak`、未知 sidecar 与非任务改动；有冲突立即停止，不覆盖用户内容。

## 5. 验证命令

Focused：

```bash
python3 trellis/skills/guru-team/packages/guru-review-contract-wording/tests/test_contract.py
python3 trellis/skills/guru-team/packages/guru-review-contract-wording/tests/test_runtime.py
python3 trellis/skills/guru-team/packages/guru-review-change-request/tests/test_contract.py
```

Package 与 projection：

```bash
trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --json --mode source
.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --json --mode installed
python3 trellis/skills/guru-team/tests/test_skill_packages.py
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
```

Cross-package installed transcript 使用 dedicated temporary work root，并传入：

```bash
python3 trellis/presets/guru-team/scripts/python/verify_installed_phase0_transcript.py \
  --installed-repo . \
  --work-root <dedicated-temporary-work-root> \
  --checkpoint issue-274 \
  --semantic-grading trellis/presets/guru-team/tests/semantic-retrieval-grading.json
```

文档检查使用仓库现有 Markdown link、code fence、whitespace 与 terminology gates。完整 throwaway install/update/reapply 与累计 release verifier 不在本 task 强制命令中。

## 6. Phase 2 与 Finish 边界

- [ ] Phase 2 由 `trellis-implement` 执行 approved plan，由独立 `trellis-check` 检查完整 current diff。
- [ ] `guru-check-task` 只在 focused、cross-package、source/installed、projection 与 docs 一致性全部满足后返回 `passed`。
- [ ] 任务 commit 前仅暂存本 task 文件；保留所有无关 dirty/untracked 内容。
- [ ] Branch Review 必须核对 public projection 无 private runtime、readiness consumer 未改、transcript 不再手工 rebind，以及未执行 release gate 的披露。
- [ ] 本 Phase 1 不授权实现、commit、push、PR、merge、release、业务仓升级或 Issue close。
