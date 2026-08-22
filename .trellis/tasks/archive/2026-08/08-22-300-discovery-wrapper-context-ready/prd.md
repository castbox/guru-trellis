# #300 修复 Discovery public wrapper 与 throwaway workflow switch

## 1. Goal

修复 live Issue #300 中两个彼此独立、但共同阻塞 #287 representative clean
throwaway evidence 的正常路径缺陷：

1. 合法、fresh、schema-valid 的 Discovery owner 经声明的 public dispatcher wrapper
   被错误降级为无诊断 `blocked`；
2. verifier 在 managed `.trellis/workflow.md` 上执行 workflow switch 时没有完成明确的
   preview/replace 合同，因 local-edit protection 中止。

Live authority：<https://github.com/castbox/guru-trellis/issues/300>。

## 2. Confirmed Facts

- task 复用 `fix/300-discovery-wrapper-context-ready` 与既有 worktree；base 已从
  `1c2dbe908387576493afa5654a4d020bfa865f74` fast-forward 到 fresh
  `main@00f902803af36c14d024e1ff2ddcac78bbe0ee53`。
- `main` 已包含 #299 / PR #302；其 architecture fixture coverage 与 failure-cleanup
  修复不是本 task 的实现范围。
- 对同一 Discovery public input、`base_current` 与 owner，package-local binding 可通过，
  public wrapper 却可能仅返回 `{"exit_id":"blocked"}`；必须以真实 wrapper transcript
  定位首个分歧点。
- #287 当前 candidate 为 `356b90c8db9dd313dd715c8f680d0201a42fa457` / PR #298；
  其 workflow switch、clean fixture 与后续声明验证在 #300 解除前仍未通过。
- current Docs SSOT `current-main-0.6.5-guru.40` 与 #295 已定义 Sync -> Discovery ->
  Clarify 的 public I/O；#300 不迁移该 API。
- Trellis 官方文档确认 global `trellis workflow --template <id>` 会替换
  `.trellis/workflow.md`；当前 Trellis CLI 的 local-edit protection 仍是本仓库 verifier
  必须显式处理并验证的事实边界。

## 3. Requirements

### R1. Discovery public invocation 一致性

- 使用真实 `.agents/skills/guru-discover-change-context/scripts/invoke.sh --invocation -`
  或等价 installed public wrapper 重现差异并定位最早错误边界。
- 相同 current input、transition 与 checker-passed owner 必须在 package-local binding 与
  public wrapper 上得到一致结论；合法路径返回 schema-valid `context_ready` Clarify handoff。
- 不以 direct import production package runtime、绕过 dispatcher 或手工构造 public
  success 代替产品证据。

### R2. Discovery fail-closed 保持不变

- invalid schema、stale base、dirty/wrong/missing/ambiguous authority、owner mismatch 与
  unresolved managed runtime/package sidecar 继续返回当前声明的 `blocked` 或
  `refresh_base`。
- 修复不得新增 public field/schema/exit，也不得放宽 semantic gate、freshness、package
  inventory 或 managed Python resolver 门禁。
- 若补充诊断，只能使用现有 public contract 允许的稳定分类，不泄露 owner private
  payload、绝对路径、堆栈或完整 review evidence。

### R3. Managed workflow switch 正常路径

- verifier 先用 `--create-new` 取得 preview，并验证 preview 内容、当前 workflow
  ownership/provenance 与预期 candidate 一致，再执行明确的 active switch。
- 只有当前 `.trellis/workflow.md` 被证明是受管理且可替换的状态时，才允许显式
  `--force`；未知或用户修改必须保留并稳定阻塞，不得静默覆盖。
- preview `.new`、`.bak` 与其它 sidecar 必须在声明 consumer 完成后得到验证和清理；
  失败路径只报告原始错误，不产生二次 cleanup 异常或隐藏原始证据。

### R4. 回归与分发一致性

- 增加真实 public wrapper current/invalid/stale/mismatch transcript 回归。
- 增加 managed workflow preview/active switch、user-modified workflow、sidecar conflict
  与 failure-recovery 回归。
- canonical、dogfood installed copy、Shared/Codex/Claude/Cursor 投影、README 与声明测试
  保持 byte/mode/contract 一致；reapply 后不得留下未处理 `.new` / `.bak`。

### R5. #287 fresh revalidation

- #300 实现到达 reviewed live `main` 后，从 fresh base 重新验证 #287 / PR #298 的精确
  candidate 或由其 owner 明确接续后的新 candidate。
- 至少重新取得 workflow switch、representative clean/isolated throwaway 和 #287 当前
  声明验证项的完整 fresh evidence；任何未验证项继续阻塞并明确报告。
- 不使用 #299 的旧证据、#300 合并前的本地结果或 retry 后的局部通过冒充 #287
  post-merge evidence。

## 4. Acceptance Criteria

- [ ] A1：真实 public wrapper 对合法 current owner 返回 `context_ready`，并生成符合声明
  schema 的 Clarify handoff。
- [ ] A2：相同输入的 package-local binding、checker 与 public wrapper 结论一致。
- [ ] A3：invalid/stale/mismatched authority/owner 与 unresolved sidecar 仍按现有 typed
  route fail closed。
- [ ] A4：managed workflow 使用验证后的 `--create-new` preview 与显式 active switch；
  user-modified workflow 不被覆盖。
- [ ] A5：真实 wrapper transcript、workflow-switch、failure-recovery、targeted package/runtime、
  installed validation、preset reapply、dogfood drift、sidecar scan 与 `git diff --check` 通过。
- [ ] A6：representative clean/isolated throwaway 完整通过；本 task 不扩张为 #267 full
  Release matrix。
- [ ] A7：fresh committed full-diff review 无 blocking finding；PR 仅 `Refs #300`，不提前关闭。
- [ ] A8：合并到 live `main` 后重新验证 #287 / PR #298，并在完整 fresh evidence 通过后才
  允许单独关闭 #300；#287、#247 不由本 task 自动关闭。

## 5. Docs SSOT And Architecture

- Docs strategy：`delta_first`。实现同步修正
  `trellis/presets/guru-team/README.md` 与 canonical
  `trellis/presets/guru-team/spec/workflow/quality-guidelines.md` 中 workflow
  preview/显式 `--force`/用户修改保护的公开合同，并通过 preset reapply 同步
  `.trellis/spec/workflow/quality-guidelines.md`；#295 的 current RDT/public contract 不变，
  不创建共享 Requirements/Design/Test contribution。
- Planning Architecture classification：`no_architecture_impact`。若实现证明必须改变 public
  I/O、owner 或 workflow interaction direction，立即停止并回到 scope clarification。
- 官方 workflow 文档只作为 upstream 行为参考；当前 CLI/version、live Issue 与仓库 SSOT
  共同决定本 task 的精确兼容边界。

## 6. Out Of Scope

- 修改 #287 managed-path staging 产品实现或自动关闭 #287 / PR #298。
- 重新实现 #299 已完成的 architecture fixture coverage 或 temporary cleanup 修复；若回归，
  只记录为回归并关联 #299。
- #267 完整 Release matrix、#247 后续 convergence、Trellis upstream/global npm/node_modules。
- 新 public field/schema/exit、攻击模型、锁、压力竞态或对抗性 artifact 防御。

受支持的 `GURU_TEAM_THROWAWAY_SINGLE_REPO_COMPATIBILITY=1` verifier 路径不是
#267 full matrix，也不是 #287 产品实现；它属于本 Issue 已声明的 representative
throwaway/workflow-switch 正常路径，必须与默认 matrix verifier 使用相同的 managed-before、
preview-candidate、显式 `--force` 与 sidecar fail-closed 合同。

## 7. Open Questions

无。若定位证明 #295 contract 本身不充分，或 workflow switch 需要修改 Trellis upstream，
则停止实现并重新澄清范围。
