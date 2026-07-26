# #117 BR-117-F8 实现交接

## 1. 实现结论

本轮实现边界已完成 `BR-117-F8` 的 working-tree candidate：

- 只删除
  `.trellis/tasks/07-25-117-verify-extension-installation/reviews/002-closure.md`
  的一个 EOF 多余空行；
- 不改写 Round 3 的语义结论、验证声明或 closure recommendation；
- 更新 task-local `review.md`，真实记录 F1/F2/F7 已关闭，F8 为
  `resolved_pending_closure`；
- 未修改 canonical runtime、public Skill package、schema、workflow、preset、
  overlay、README 或 durable requirements。

实现代理未修改 `agent-assignment.json`、`review-gate.json` 或
`task-commit-plans/003.json`，未运行 `trellis-check`，未记录 Phase 2 或 Branch
Review Gate，未 commit、push、创建 PR、关闭 Issue 或调用 finish-work。

## 2. Changed paths

- `reviews/002-closure.md`：删除唯一 EOF 多余空行。
- `review.md`：补入 Round 5、F7 closure、F8 finding 与 working-tree candidate
  状态。
- `implementation-handoff.md`：新增本轮实现、验证、Docs SSOT 与 freshness 交接。

## 3. Requirement 与 design 承接

F8 直接承接：

- `implement.md:171` 对完整范围 `git diff --check` 的要求；
- `.trellis/spec/workflow/quality-guidelines.md` 的 required validation；
- Branch Review raw report 保持中文、可审计且不改写历史语义的合同。

本轮没有新增产品行为、public I/O、runtime route、安装或升级合同。F8 的
implementation candidate 只修正 task-local Markdown 格式；正式 finding 状态仍由后续
独立 closure reviewer 拥有，当前 reviewer-owned gate 继续为
`implementation_required`。

## 4. Docs SSOT Plan

策略：`ssot_first`。

### Durable docs 输入

实现以已批准的 `design.md` Docs SSOT Plan、`implement.md` validation contract 和
`.trellis/spec/workflow/quality-guidelines.md` 为主输入。前序 #117 实现已将
applicability、profile、adequacy、public I/O、private evidence、retry/stale、
redaction、remote clean install 与 update/reapply 的 task delta 合并到 canonical
package、workflow/spec、requirements 和 README owners。

### 本轮同步结果

- Durable docs update：无。
- No-update reason：F8 只删除 task-local raw report 的 EOF 空行，不产生新的稳定行为、
  API、schema、workflow、installer、ownership、部署或安全语义。
- Task delta merged to durable docs：本轮没有新的 durable delta；格式修复直接落在其
  task-local owner。
- Task-history-only：Round 3 原始 closure 内容、Round 5 对 F8 的发现、本轮候选验证、
  assignment digest stale 事实和本实现交接。
- `bootstrap_or_repair_docs`：不适用。
- Follow-up / current PR limit：exact pushed feature-ref clean install 仍必须在后续
  授权 push 后独立完成；当前 local-source throwaway 不替代该 publication gate。

### Durable docs 与 task delta 的实现输入

稳定质量标准来自 durable `quality-guidelines.md`；F8 的 affected path、qualification、
severity 与 required closure 来自已登记的 Round 5 raw report。Task delta 只限定本次
修复目标，不被提升为新的 durable contract。

## 5. Assignment digest freshness

Round 3 当前登记值：

- SHA-256：`d590a48a50686c067b0eb7466c8b9572bc8b11145a659e08fe2a6aa1ad612b26`
- Size：`10157`

删除一个 EOF newline 后的候选值：

- SHA-256：`67ea4c3edefd5ea9195ea19ca4f4f625cb14aaaa857101b573701dc06b9a204d`
- Size：`10156`

现有 deterministic `record-agent-assignment` 只支持：

- 追加 assignment；
- 追加唯一递增的 review round；
- 追加 reuse decision；
- liveness provenance correction 或 failed-to-termination recovery link。

它没有刷新、替换或 supersede 既有 `review_rounds[]` report digest 的模式。
Correction 只允许 `progress` / `status-request` liveness event，不能修订 review round；
重新追加 Round 3 又违反 round 唯一递增合同。因此本实现代理没有手改
`agent-assignment.json`。

当前 `check-agent-assignment.sh` 按预期返回 exit 2：

- `review_rounds[2]` raw report SHA-256 stale；
- `review_rounds[2]` raw report size stale。

这是进入 fresh Phase 2 前的确定性 blocker。主会话必须通过受支持的 assignment
artifact freshness 合同处理；在没有专用 recorder 的情况下，不应手工改写 ledger 或
用新的 review round 掩盖旧 round 的 stale digest。

## 6. 已运行验证

- `git diff --check origin/main`：exit 0，证明包含 working-tree candidate 的完整
  base-to-worktree diff 无 whitespace error。
- `git diff --check`：exit 0，证明当前未提交差异自身无 whitespace error。
- `git diff --check origin/main...HEAD`：exit 2，仍读取修复前
  `3bfbd100...`，唯一命中旧 committed report 的 EOF 空行；下一次 task work commit
  后必须重跑并通过。
- `python3 ./.trellis/scripts/task.py validate
  .trellis/tasks/07-25-117-verify-extension-installation`：通过。
- `check-agent-assignment.sh --json`：exit 2，精确命中上述 Round 3 SHA/size stale，
  没有其它 reported error。
- `check-review-gate.sh --json`：exit 2，按预期确认旧 gate 不是 pass，并检测到：
  - 旧 Phase 2 `implementation_handoff` 与 `agent_assignment` stale；
  - 新 `implementation-handoff.md` 尚未进入旧 Phase 2 的 exact allowlist；
  - `review.md`、gate 绑定的 assignment 与 Round 3 report SHA/size stale；
  - gate 仍有一个 open finding。
- `check-workspace-boundary.sh`：通过，expected workspace 与 actual repo root 均为
  当前 Issue #117 worktree。
- `check-planning-approval.sh`：编辑前通过；本轮未改 `prd.md`、`design.md`、
  `implement.md` 或 planning authority。

本次只修改 Markdown task evidence，没有 Python、shell、JSON、schema、runtime、
package、preset 或平台分发变化，因此不重复运行 repository-wide runtime、Skill、
preset、ownership、eval 或 throwaway suites；这些完整验证必须由后续 fresh
`trellis-check` 按 finding-fix full rerun 合同重新执行。

## 7. 交给 trellis-check 的输入与重点

Fresh Phase 2 只能在 assignment freshness blocker 消除且 assignment checker 通过后
开始。后续独立 `trellis-check` 应：

1. 将 `reviews/002-closure.md` 的新 digest/size 纳入 current implementation
   handoff，并验证其内容只少一个 EOF newline。
2. 对 base-to-working-tree candidate 运行 `git diff --check origin/main`，对下一次
   commit 后的最终范围运行 `git diff --check origin/main...HEAD`。
3. 完整重跑 #117 current-scope Phase 2，不能用本轮 targeted lint 替代 runtime、
   package、preset、ownership、production eval 与 full throwaway evidence。
4. 复核 `ssot_first` reconciliation：F8 没有 durable docs delta，前序 task delta
   已在 durable owners，新增内容仅为 task history。
5. 保持 exact pushed feature-ref clean install 为授权 push 后的独立 publication
   gate，不用 local-source throwaway 冒充。

## 8. 剩余风险与状态

- F8 的代码/文档候选已实现，但 reviewer-owned finding 仍是
  `open / resolved_pending_closure`，未正式关闭。
- Round 3 report digest stale 是当前唯一已知确定性 blocker。
- 当前 HEAD 尚未包含 F8 修复；提交前 `origin/main...HEAD` 仍会复现旧 lint finding。
- 未发现新的 runtime、public contract、Docs SSOT、部署或安全风险。
