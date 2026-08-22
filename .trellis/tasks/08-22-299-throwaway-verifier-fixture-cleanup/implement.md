# #299 实施计划

## 1. Pre-Implementation

- [ ] 重读 Issue #299、task planning、installer/quality/companion-script contracts 与 current
  Architecture authority。
- [ ] 检查 `bootstrap_foundation`、`repair` profile 的真实 input/output contract 和现有去敏 eval
  结构，确认 fixture 不是仅补标签。
- [ ] Planning semantic review 通过并取得独立的实现启动确认后，运行 `task.py start`。

## 2. Implementation Steps

1. 为 `bootstrap_foundation` 与 `repair` 增加最小 canonical eval input/case，使四个 profile 集合精确
   覆盖且各自语义有效。
2. 在 `verify-throwaway-install.sh` 的最窄 cleanup owner 增加 macOS Bash 3.2 + nounset 兼容的
   零元素保护，并保留原始退出状态与现有路径 allowlist。
3. 增加 profile 集合、空数组原始失败、非空数组精确清理的 targeted regression tests。
4. 运行 Architecture Baseline package/eval 与 throwaway verifier targeted tests，修复本 task 引入的
   finding。
5. 按 changed paths 执行 preset reapply，同步 canonical/dogfood/installed/platform projection，并
   验证 mode、drift、sidecar 与 `.new/.bak`。
6. 执行一个代表性 clean throwaway；如遇 task 外阻塞，记录首个失败与未验证边界。
7. 完成 task validation、`git diff --check`、fresh full-diff semantic check。

## 3. Expected Surfaces

- `trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/evals/**`
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`
- 与上述行为直接对应的 canonical regression tests
- reapply 产生的受管理 dogfood/installed/platform projection（仅实际受影响者）
- 本 task planning、ledger 与 context manifests

若根因要求修改 public Skill API、profile 声明、validator 语义或上述范围外 owner，停止并重新澄清。

## 4. Validation

- Architecture Baseline package/eval schema 与 profile coverage targeted tests。
- macOS Bash/nounset empty 与 non-empty cleanup paired regression。
- throwaway Python routing/compatibility targeted tests。
- installed `check-skill-packages.sh --mode installed` 与受影响 projection reapply/drift checks。
- 一个代表性 clean throwaway。
- task/ledger validation、sidecar、mode、`git diff --check` 与 recursive `.new/.bak` scan。

## 5. Completion Boundary

本地实现和 check 通过后停止；本轮不执行 commit、push、PR、merge、Issue closure、发布或清理
#299/#300 资源。

