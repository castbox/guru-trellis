# #338 修复 Finalizer 未绑定 equal-HEAD 恢复

## 1. Goal

补齐 `guru-finalize-task` 的同计划恢复合同：当当前 owner-private transaction 仍处于
`ordinary_publication/push_content`，但远端分支和唯一 Open PR 已由诚实操作提前推进到
`publication_head` 时，Finalizer 在完整身份校验后接管该 PR，收敛 Publication metadata，并从归档阶段继续。

Live authority：GitHub Issue #338，2026-09-02 当前正文。

## 2. Confirmed Facts

- 当前基线为 `main@107053f9ec18ef4df01d01c1871e7a798b0e3ae4`。
- `classify_existing_pr_recovery()` 在 remote/PR/publication HEAD 取值一致且调用方未传入
  `allow_equal=true` 时返回 `existing_pr_unbound_equal_head`。
- `finalization_existing_pr_recovery_context()` 仅处理无 transaction 的严格祖先接管，或已处于
  `existing_pr_recovery` 的 transaction；它不会接管
  `ordinary_publication/push_content` transaction。
- `finalization_pre_mutation_remote_preflight()` 在 Open PR 存在且 transaction 的 `pr` 为空时返回
  `pre_finalizer_pull_request_exists`。
- #208 已建立严格祖先 existing-PR adoption、PR metadata convergence、Draft/Ready 分支与重试零重复副作用 transition。
- #251 已建立 transaction 绑定后的 same-plan recovery 优先级。
- #333 / PR #337 提供真实拓扑：transaction 未绑定，remote HEAD、PR HEAD、Publication HEAD 均为
  `db49b964e72b4f59f9ef8285dce2b54d8917db10`，PR body 仅比 Publication body 多一个末尾 LF。
- Current transaction schema 已表达 `ordinary_publication`、`existing_pr_recovery`、`adopted_pr`、`pr`
  与 `push_content|bind_pr|archive|push_archive|mark_ready`，本任务不新增 public exit 或 transaction schema。

## 3. Requirements

### R338-01 精确恢复资格

Finalizer 仅在下列条件全部成立时识别 `unbound_equal_head_recovery`：

- current transaction 的 `mode=ordinary_publication`；
- `next_transition=push_content`；
- `pr` 与 `adopted_pr` 均不存在；
- transaction 的 task、repo、base、branch、Branch Review commit、Publication head、plan digest、
  Publication title/body 与 close scope 全部匹配 rebuilt current plan；
- 唯一 Open PR 属于同 repository、同 base/head branch、同 head repository，且不是 fork；
- remote branch HEAD、PR HEAD、Publication HEAD 三者取值一致；
- live PR close scope 精确匹配 Issue Scope Ledger 中已审核的 `close_issues`；
- archive、task locator 与其它 owner transaction 不存在冲突。

任一条件失败时保持现有 fail-closed 行为，不回退到 fresh adoption、普通首次发布或人工修复。

### R338-02 Side-effect-free preview

Preview 必须报告：

- `publication_mode=existing_pr_recovery`；
- 精确 PR number/URL；
- `ancestry=equal`、`push_required=false`；
- PR 原始 Draft/Ready 状态；
- live title/body 与 current Publication 的字节比较；
- `metadata_update_required` 与 `ready_action`；
- 剩余 mutation 顺序为 bind recovery transaction、metadata convergence、archive、archive push、
  Ready 保持或 Draft-to-Ready。

Preview 不执行 push、PR edit、archive、commit、Ready mutation 或 transaction 写入。

### R338-03 Transaction 转换与绑定

执行器在任何剩余外部 mutation 前，必须把 current ordinary transaction 原位转换为
`existing_pr_recovery`，并写入精确 `pr`、`adopted_pr`、一致 HEAD、原始 Draft/Ready 状态、
Publication payload、close scope、plan digest 与合法 next transition。

转换必须复用 current transaction identity，不创建第二个 transaction，不伪造 predecessor，不重复 push
Publication HEAD。

### R338-04 Metadata convergence

- live title/body 与 Publication 字节一致时，跳过 PR edit。
- 任一字段存在字节差异时，沿用 existing recovery metadata convergence，将 title/body 精确更新为 current
  Publication payload。
- 更新后重新读取 PR，验证 title/body 字节一致、close scope 未改变、PR/remote HEAD 未漂移。
- PR #337 的末尾 LF 差异必须触发一次 metadata update，且收敛后 body 字节一致。

### R338-05 剩余 transition 与重试零重复副作用

- transaction 绑定完成后从 `archive` 继续，不执行 publication push 或第二次 PR create。
- Ready PR 保持 Ready；Draft PR 沿用 current Draft-to-Ready transition。
- same-plan retry 从 transaction 的 exact next transition 恢复，不重复 metadata edit、archive move、archive
  commit、archive push 或 Ready mutation。
- terminal route 仍输出 current `ready_for_merge` DTO，公共 Skill id、六个 typed exits 与 Merge consumer 不变。

### R338-06 Fail-closed matrix

下列场景必须阻断且不产生 mutation：多个候选 PR、Closed/Merged PR、fork、repo/base/head/head-repository
不匹配、remote/PR/publication HEAD 取值不一致、close scope 漂移、preview 后 PR identity/HEAD/metadata 漂移、
metadata convergence 后仍有字节差异、stale plan/gate/Branch Review/Publication、已有不同 PR binding、archive
冲突、未知 transaction stage。

## 4. Acceptance Criteria

- [ ] AC-338-01：#333 / PR #337 拓扑 fixture 在 preview 中返回
  `existing_pr_recovery`、`ancestry=equal`、`push_required=false`、
  `metadata_update_required=true`。
- [ ] AC-338-02：首次执行在外部 mutation 前完成 ordinary-to-recovery transaction 转换，并绑定原始
  live PR metadata、一致 HEAD、Draft/Ready 状态与 current plan identity。
- [ ] AC-338-03：末尾 LF fixture 仅执行一次 PR metadata update；更新后 title/body 与 Publication 字节一致，
  close scope 不变。
- [ ] AC-338-04：metadata 字节一致路径不调用 PR edit。
- [ ] AC-338-05：Ready 与 Draft 两条路径均完成 archive、archive push 与 terminal
  `ready_for_merge`；Ready 路径不调用 Ready mutation，Draft 路径仅调用一次。
- [ ] AC-338-06：同计划重试不重复 push、PR create/edit、archive move/commit/push 或 Ready mutation。
- [ ] AC-338-07：R338-06 的每个负向场景均在首个 mutation 前返回稳定阻断事实。
- [ ] AC-338-08：canonical、dogfood installed、shared/Codex/Claude/Cursor 投影一致，零未知
  `.new`/`.bak` sidecar，overlay drift 为零。
- [ ] AC-338-09：Finalizer targeted source/installed tests、Finalizer workflow integration、preset reapply、
  ownership/parity、task validation 与 `git diff --check` 通过。
- [ ] AC-338-10：完整多平台 Throwaway/release matrix 未由本任务执行，最终结果明确记录该边界。

## 5. Docs SSOT Plan

策略：`delta_first`。

- Phase 2 先创建 `docs/requirements-design-test-contributions/338-finalizer-unbound-equal-head-recovery/`
  的 Requirements、Design、Test 与 traceability delta，绑定 current `.42` authority。
- Durable workflow contract 更新范围为
  `trellis/skills/guru-team/packages/guru-finalize-task/{SKILL.md,references/contract.md}`、
  `.trellis/spec/workflow/{data-contracts,companion-scripts,quality-guidelines}.md`。
- `skill-package-contract.md`、Interface、schema、registry、README 与 extension version 仅在实现证明公共合同或
  安装资产发生变化时更新；否则保留原字节。
- RDT contribution 必须在最终 Phase 2 check 前经 owner review 和 serialized promotion 合入 shared current。
- Full release/install matrix 保留给专门 Release Gate，不进入本 task 的 durable completion claim。

## 6. Architecture Planning Impact

预期 route：`baseline_current/no_architecture_impact`。

本任务修复现有 Finalizer owner 内部的 current-conforming recovery correctness，复用 #208 transaction、
metadata convergence、archive 与 Ready contract；不新增 architecture owner、公共 DTO、typed exit、依赖方向、
持久化类型、GAP 或 ADR。若实现发现必须新增 public schema、跨 package owner 或双路径 authority，则当前
Architecture 结论立即失效并重新进入 `task_impact_sync`。

## 7. Out Of Scope

- #333 的业务实现、task、transaction 与 archive。
- PR #337 的 merge、close、rebuild、远端分支删除或人工 metadata mutation。
- #208、#249、#251 的重新开放、修改或关闭。
- 任意 Open PR、任意手工 push、fork PR、scope mismatch 或跨计划状态的追认。
- release、deployment、production proof、tag、GitHub Release 与完整多平台 Throwaway matrix。
- 攻击模型、恶意 artifact、故意伪造、锁、TOCTOU、压力竞态与额外 crash-consistency 加固。
- commit、push、PR、merge、Issue closure 与 worktree cleanup。

## 8. Open Questions

无。Live Issue、真实复现与 current contract 已固定恢复资格、metadata convergence、验证范围和边界。
