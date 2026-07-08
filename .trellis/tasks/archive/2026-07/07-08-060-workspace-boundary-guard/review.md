# #60 Branch Review Rollup

## 审查轮次

- 第 001 轮：最终放行审查代理，raw report：[`reviews/round-001-final.md`](reviews/round-001-final.md)
  - reviewed_head：`1e2e78ae1259165c61a5dfdb4826abd6edc730a5`
  - diff 范围：`origin/main...HEAD`
  - findings_count：1
  - 结论：发现 P2 release/version finding，未放行。
- 第 002 轮：问题闭环审查代理，raw report：[`reviews/round-002-closure.md`](reviews/round-002-closure.md)
  - reviewed_head：`ff59c2db866d0414b7a736205a26ed9da004eecf`
  - diff 范围：`origin/main...HEAD`
  - findings_count：0
  - 结论：作为 replacement closure reviewer，确认第 001 轮 P2 已闭环；该轮不是最终放行审查。
- 第 003 轮：最终放行审查代理，raw report：[`reviews/round-003-final.md`](reviews/round-003-final.md)
  - reviewed_head：`ff59c2db866d0414b7a736205a26ed9da004eecf`
  - diff 范围：`origin/main...HEAD`
  - findings_count：0
  - 结论：fresh final review 通过。
- 第 004 轮：最终放行审查代理，raw report：[`reviews/round-004-final.md`](reviews/round-004-final.md)
  - reviewed_head：`3af6ee1d99fcbae862ef993efa851111c9874a96`
  - diff 范围：`origin/main...HEAD`
  - findings_count：0
  - 结论：fresh final review 重新覆盖最新 replacement closure validator 提交后通过。

## 问题生命周期

- Phase 2 resolved finding：阶段二检查代理发现并修复 worktree mode 缺少当前 handoff 时的 fail-closed 缺口；当前无开放 Phase 2 finding。
- 第 001 轮 P2：新增 extension public API / managed asset 后仍使用已发布 `0.6.5-guru.1`，release tag 与安装/升级可观测性无法唯一表示 #60 guard 能力。
- 修复：分支已将 Guru Team extension revision 提升为 `0.6.5-guru.2`，并同步 canonical manifest、dogfood installed manifest、README / workflow README / preset README、`verify-throwaway-install.sh` 默认 source 和版本断言测试。
- 第 002 轮闭环：原第 001 轮 final reviewer 失败/中断且无法继续，replacement closure reviewer 通过完整 metadata 链闭环该 P2；旧 `0.6.5-guru.1` 引用只保留在 task 历史 evidence 中。
- 第 003 轮最终审查：在 `ff59c2db866d0414b7a736205a26ed9da004eecf` 未发现新的 P0/P1/P2/P3 finding。
- 第 004 轮最终审查：在最新 `3af6ee1d99fcbae862ef993efa851111c9874a96` 重新覆盖 replacement closure validator 支持后，未发现新的 P0/P1/P2/P3 finding。

## 最终审查

最终放行审查通过。当前 HEAD `3af6ee1d99fcbae862ef993efa851111c9874a96` 的完整 `origin/main...HEAD` diff 覆盖 #60 workspace boundary guard、release/version bump、replacement closure chain validator、tests、workflow/spec/docs、preset installer、canonical overlays 与 dogfood installed copies；未发现开放 finding。#76 保持 follow-up，不由本任务关闭。

## 证据

- 启动边界：worktree 为 `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/060-workspace-boundary-guard`；`HEAD=3af6ee1d99fcbae862ef993efa851111c9874a96`；`check-workspace-boundary.sh --json --task .trellis/tasks/07-08-060-workspace-boundary-guard` 返回 `status=ok`；source checkout `/Users/wumengye/Documents/GoProjects/guru-trellis` 为 `## main...origin/main` 且 clean。
- Diff：`git diff --stat origin/main...HEAD` 为 55 files changed, 1879 insertions(+), 195 deletions(-)；最新提交 `ff59c2db...HEAD` 为 18 files changed, 533 insertions(+), 48 deletions(-)。
- Phase 2：`phase2-check.json.head=ff59c2db866d0414b7a736205a26ed9da004eecf` 是当前 HEAD 的父提交；最新提交的 18 个非 metadata 文件全部被 `phase2-check.json.dirty_paths` 覆盖；当前 worktree 无非 metadata dirty path。
- Replacement closure：代码只验证 predecessor failed/unfinished、`replacement-started` + `supersedes_agent_id`、`reuse_decisions[] decision=replace from_round/to_round`、replacement closure round `findings_count=0` / `reuse_decision=replace`，并禁止 replacement closure reviewer 成为 final；是否应替换、审查是否充分仍由 AI/human review 判断。
- 验证：workflow helper tests 161 个通过；preset installer tests 27 个通过；dogfood drift check 通过；JSON validation、`bash -n`、`py_compile`、task manifest validation、`git diff --check` 均通过；无 `.bak` / `.new` 残留。
- 版本证据：`trellis/guru-team-extension.json` 与 `.trellis/guru-team/extension.json` 均为 `0.6.5-guru.2`，public API 均包含 `check-workspace-boundary`、`record-agent-assignment`、`check-agent-assignment`；旧 `0.6.5-guru.1` 引用在非 task evidence 路径中无匹配。
- 部署/安全影响：本 diff 未修改 CI/CD、container、K8s/Helm/Kustomize、DB migration、Makefile、runtime config template 或 schema 文件；diff 敏感词扫描只命中安全规则文字、literal token 文案、tokenization 代码和环境变量读取逻辑，未发现实际 token、secret、private key、签名 URL、`.env` 内容或数据库 URL。
- Docs SSOT：`README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、`docs/requirements/**`、`.trellis/spec/workflow/**` 与 canonical / dogfood workflow overlay 已同步 workspace boundary 与 replacement closure 规则。

## 观察项

- tag-pinned throwaway install 仍需在 PR merge 并创建 annotated tag `v0.6.5-guru.2` 后重跑；当前 review 不声称公开 release tag 已存在，也不声称完整开箱即用安装已通过。
- `.trellis/guru-team/extension.json` 的 `source_tree_state=dirty` 与 `source_commit=ff59c2db...` 是 dogfood apply 当时的 objective provenance，不是 release readiness 断言。
- `issue-scope-ledger.json` 正确保持 #60 为 `close_issues`、#76 为 `followup_issues`；#60 的 `acceptance_evidence` 仍为空，finish/publish 前主会话应补入本轮 review/gate 可引用的验收证据。
- 第 004 轮 raw report 已写入，但 `agent-assignment.json` 中第 004 轮 review round / raw report digest 仍需主会话在本报告完成后记录；本审查代理未运行 recorder。

## 后续候选

- #76 heartbeat / workspace-aware liveness 继续作为后续 issue；#60 只建立 workspace boundary fact layer。
- release tag 创建后运行 tag-pinned `trellis init` / `trellis workflow` / preset apply throwaway 验证，补齐公开开箱即用 release evidence。

## 结论

通过。当前 findings_count 为 0；第 001 轮 P2 已由第 002 轮 replacement closure 审查闭环，第 003 轮在上一 HEAD 通过，第 004 轮已重新覆盖最新 `3af6ee1d99fcbae862ef993efa851111c9874a96` 的完整 `origin/main...HEAD` diff。`review.md` 已链接全部 raw reports，可供主会话继续记录第 004 轮 fresh final review evidence 与 Branch Review Gate。
