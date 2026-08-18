# #270 统一 reviewed-content identity 合同

## 目标

把四个阶段目前同名但实现漂移的 `guru-reviewed-content-1.0` 收敛为一个 durable SSOT 和一个 canonical helper，使 Branch Review、Publication、Finalizer、Verifier 在同一 Git commit 上得到同一 SHA-256，同时继续由独立门禁校验 base ref、base commit、review range 与 ancestry freshness。

## 背景与确认事实

- live Issue #270 是唯一 primary/close Issue，状态 OPEN；没有 accepted comments，也没有其它 open duplicate。
- 硬前置 #269 已由 PR #273 合并到 `main@6d00678166aa57df204872b3471dbd6d7684cb55`，Issue CLOSED；本 task 从该 remote-main commit 创建。
- 当前 Branch Review 在 `trellis/skills/guru-team/packages/guru-review-branch/runtime/common.py:263` 自有 `content_identity(repo, base_commit, commit, task_ref)`：digest 包含 `base_commit`，entry 包含 `kind`，metadata exclusion 也比其它阶段窄。
- Publication、Finalizer、Verifier 各自在 owner runtime 中复制 reviewed-content tree/worktree/gitlink 与 metadata exclusion 逻辑，存在再次漂移风险。
- 官方 Trellis 扩展边界仍是 Markdown workflow / Skill 定义流程，companion runtime 仅执行确定性 identity 与 freshness 校验；不修改上游 Trellis、全局 npm 或 `node_modules`。
- #270 是普通 workflow defect Issue。按 `.trellis/spec/workflow/quality-guidelines.md` 的 Validation Scope Ownership，只做证明 accepted scope 的 targeted validation，不执行完整多平台 Throwaway installer 矩阵。

## 需求

### R1 Durable SSOT 与 canonical helper

- 固定 algorithm id 为 `guru-reviewed-content-1.0`。
- identity 输入是 metadata-excluded Git entries，按 UTF-8 path bytes 排序。
- 每项只能包含 `path`、`mode`、`oid`；digest payload 不包含 `base_commit`、Git object `kind` 或阶段私有字段。
- metadata exclusion 必须统一覆盖 task/archive、workspace、runtime、provenance tail 与当前闭集 OS noise `.DS_Store`。
- Branch Review、Publication、Finalizer、Verifier 必须调用同一个 shared canonical helper，不保留阶段级算法副本。

### R2 独立 freshness 不弱化

- content identity 仅证明 reviewed business content continuity。
- base ref/commit、review range、review commit/current HEAD 和 ancestry 继续由各阶段现有独立 gate 校验。
- path、mode 或 oid 的任一业务内容变化必须改变 digest 并 fail closed。

### R3 Owner-private checkpoint 迁移

- Branch Review checkpoint 使用 current-only contract 绑定新的 canonical algorithm identity。
- 旧 checkpoint 不兼容读取、不重写、不迁移、不伪造；loader/checker 稳定返回 stale，并要求 fresh Branch Review。

### R4 分发和直接 consumer 同步

- 同步 canonical package/shared runtime、installed dogfood、`.agents`、Codex、Claude、Cursor 投影。
- 同步 Docs SSOT、schema、example、eval、direct consumers、runtime/extension inventory、ownership 与 executable modes。
- preset reapply 后 dogfood drift 为零，递归 `.new`/`.bak` 为零。

### R5 真实跨包 acceptance

- 在一个真实 Git fixture 和同一 HEAD 上，通过四个真实 package wrapper 建立/消费 identity。
- 测试不得复制 expected hash，不得调用测试专用替代算法，不得以 package-local helper 直测替代 wrapper acceptance。
- 覆盖正向、metadata-only、业务 path/mode/oid drift、base/range/ancestry drift、旧 checkpoint stale 与 re-entry。

## Docs SSOT Plan

- 更新 `.trellis/spec/workflow/data-contracts.md`：独占定义 `guru-reviewed-content-1.0` payload、排序、exclusion、identity/freshness 分层和旧 checkpoint stale 语义。
- 更新 `.trellis/spec/workflow/skill-package-contract.md`：四个直接 consumer 只依赖 canonical helper，Branch Review owner-private current-only migration 和 wrapper acceptance。
- 更新 `.trellis/spec/workflow/quality-guidelines.md`：加入真实跨包同 HEAD acceptance 与本 Issue targeted validation 边界。
- 如 public README 已描述 reviewed-content 算法细节，则只改其 SSOT 引用和升级行为；不复制完整算法定义。
- canonical specs 先改，preset reapply 生成/同步 installed 与平台投影；不把 dogfood copy 当源头。

## Acceptance Criteria

- [ ] AC1 同一 commit 经 Branch Review、Publication、Finalizer、Verifier 真实 wrapper 得到同一 reviewed-content SHA-256。
- [ ] AC2 task/archive/workspace/runtime/provenance tail 和当前闭集 OS noise `.DS_Store` 变化不改变 identity。
- [ ] AC3 任意 included path、mode 或 oid 变化改变 identity，并由 consumer fail closed。
- [ ] AC4 base commit/range/ancestry 变化由独立 freshness gate 捕获。
- [ ] AC5 旧 Branch Review checkpoint 稳定 stale，只能 fresh Branch Review 恢复。
- [ ] AC6 四阶段正向、stale、re-entry、负例 suite 通过，且跨包 acceptance 没有 expected-hash 复制或 test-only 算法。
- [ ] AC7 canonical、installed、shared/Codex/Claude/Cursor bytes 与 executable mode 一致。
- [ ] AC8 preset reapply、ownership、dogfood drift、package/runtime validation 通过，递归零 `.new`/`.bak`。
- [ ] AC9 PR 和最终报告明确未运行完整多平台 Throwaway installer 矩阵。

## Out Of Scope

- 不修改 Issue body，不重新打开 #262，不创建额外 repair Issue。
- 不声称本缺陷是 #264 历史 `publication_stale` 的确定根因。
- 不修改 immutable tag/Release，不发布 release。
- 不实现 #263 或链中任何后续 Issue。
- 不执行累计兼容性、upgrade/update 或 Release Gate 专属的完整多平台 Throwaway installer 矩阵。

## Open Questions

无。live Issue 已固定算法、兼容、验证与发布边界。
