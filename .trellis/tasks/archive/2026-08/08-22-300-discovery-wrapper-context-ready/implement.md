# #300 实施计划

## 1. Pre-Implementation

- [x] 重读 live Issue #300、current workflow/package contract、官方 workflow 文档与
  current Architecture/RDT authority。
- [x] fresh `guru-sync-base` 验证 `main@00f902803af36c14d024e1ff2ddcac78bbe0ee53`。
- [x] 复用既有 #300 branch/worktree/task，并 fast-forward 到 current main。
- [x] 对首次修订后的 `prd.md`、`design.md`、`implement.md` 执行 fresh Planning semantic review。
- [x] 首次 Planning 批准后完成 Discovery 与默认 matrix verifier 实现；Phase 2 发现
  single-repository compatibility 入口和 quality-guidelines authority 遗漏，已按
  `requirements_scope_set` 资格化并取得 task-local planning 修订确认。
- [ ] 对当前 scope-corrected planning 执行 fresh Planning semantic review；批准后再修复
  shell compatibility 入口与 Docs SSOT。

## 2. Discovery Wrapper Implementation

1. 用相同合法 envelope、`base_current` 与 owner-result 建立真实 public wrapper regression。
2. 对照 recorder、checker、package-local binding、dispatcher/managed Python 与 public
   projection，定位首个分歧点。
3. 在最窄 canonical owner 修复参数、transport、validation、exception classification 或
   projection 错误，不改变 public I/O。
4. 增加 invalid/stale/dirty/wrong/missing/ambiguous/mismatch 配对回归，证明 fail-closed
   行为不回退。

## 3. Workflow Switch Implementation

1. 固定 verifier 当前 workflow ownership/provenance 与 marketplace candidate identity。
2. 使用 `--create-new` 生成 preview，并验证 `.new` 内容与预期 candidate。
3. 仅对已证明的 managed/replaceable workflow 执行显式 `--force` active switch；对未知或
   user-modified workflow 保留原文件并稳定阻塞。
4. 验证 preview/active bytes、markers、update/reapply 后状态和零 unresolved sidecars。
5. 增加 workflow-switch 与 failure-recovery 回归，并修正文档中与实际 `--force` 语义不一致
   的描述。

## 4. Expected Surfaces

- `trellis/skills/guru-team/packages/guru-discover-change-context/**`
- 若首个分歧点位于共享 dispatcher/runtime：`trellis/skills/guru-team/runtime/**`
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`
- `trellis/presets/guru-team/scripts/python/test_verify_trellis_upgrade_contract.py`
- `trellis/presets/guru-team/README.md`
- `trellis/presets/guru-team/spec/workflow/quality-guidelines.md` 与 dogfood
  `.trellis/spec/workflow/quality-guidelines.md`
- 受影响 canonical/dogfood/platform projection
- 本 task planning、ledger、check/implementation context manifests

实际根因若落在上述范围外、要求 public API 迁移或修改 Trellis upstream，停止并重新澄清。

## 5. Validation

- Discovery package contract/runtime tests 与真实 public wrapper transcript。
- workflow-switch managed/user-modified/sidecar/failure-recovery targeted tests。
- single-repository compatibility 入口的 managed-before、preview、explicit-force、
  user-modified 与 sidecar targeted regression。
- `check-skill-packages.sh --mode source` 与 `--mode installed`。
- 受影响 projection 的 preset reapply、dogfood overlay drift 与 recursive sidecar scan。
- `git diff --check`、task validation、一个 representative clean/isolated throwaway。
- fresh committed full-diff independent review。

## 6. Post-Merge Dependency Verification

1. #300 candidate 经 review、publication 与 merge gate 到达 live `main`。
2. 从 fresh live base 重新解析 #287 / PR #298 current candidate，不复用旧 HEAD 假设。
3. 重跑 workflow switch、representative clean fixture 与 #287 当前声明验证项。
4. 记录完整 fresh result；任一未验证项继续阻塞。
5. #300 PR 只使用 `Refs #300`；post-merge #287 evidence 完整后，Issue #300 的手动关闭
   需要独立授权。

## 7. Completion Boundary

本轮规划修订结束后进入 fresh Planning approval。实现/check 不授权 commit、push、PR、merge、
Issue closure 或 #287/#247 自动关闭；这些动作分别遵循后续门禁。
