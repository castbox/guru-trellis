# Issue #111 独立 Branch Review 原始报告

## 审查身份

- 技术身份：`/root/issue111_branch_review`
- 逻辑角色：问题发现审查代理
- 审查方式：fresh independent review
- 行为边界：只读审查；未修改文件、未 stage、未 commit、未 push、未创建 PR、未运行 Branch Review recorder

## 审查范围

- Repository：`castbox/guru-trellis`
- Issue：[castbox/guru-trellis#111](https://github.com/castbox/guru-trellis/issues/111)
- Base：`origin/main`
- Base HEAD：`3395fad2a4049a33c4c679cd05452cfa45a85b92`
- Reviewed HEAD：`94d6126d75d7419e79a142f45d92b07dc8922241`
- Diff range：`origin/main...94d6126d75d7419e79a142f45d92b07dc8922241`
- Diff：113 files，24466 insertions，204 deletions
- Commit：`feat(trellis): #111 增加变更上下文发现闭环`
- 当前工作区仅存在并发产生的 task-local metadata tail 变更：`agent-assignment.json`、`task-commit-plans/001.json`；本报告只审查 committed diff。

覆盖内容：

- Live issue #111 的 R1-R10、AC1-AC16
- `prd.md`、`design.md`、`implement.md`
- `planning-approval.json`
- `implementation-handoff.md`
- `phase2-check.json`
- `issue-scope-ledger.json`
- canonical package、schema、runtime、workflow、preset 与 installer
- dogfood、Agents、Codex、Cursor、Claude 分发副本
- Docs SSOT、公开 README、upgrade/update 与 throwaway evidence
- refresh ordered ancestors、prior refresh receipts、Git trackability、部署和安全边界

## 审查证据

- Live issue #111 状态为 `OPEN`，范围与 task PRD 一致。
- 三份 approved planning artifact 的 committed SHA-256、size 与 `planning-approval.json`、`phase2-check.json` 全部一致：
  - `prd.md`：`b869afdb...aff7`
  - `design.md`：`05fe5822...8682`
  - `implement.md`：`b697c34d...91e0`
- `implementation-handoff.md`、`planning-approval.json`、`agent-assignment.json`、`issue-scope-ledger.json` 的 committed bytes 与 Phase 2 evidence 一致。
- canonical、installed、Agents、Codex、Cursor、Claude 六份 `guru-discover-change-context` package 逐文件 SHA-256 相同。
- canonical/dogfood workflow、runtime 和三个 Bash wrappers 字节一致。
- 未发现 `.new`、`.bak` 或 legacy overlay drift。
- 官方 Trellis 文档确认 workflow 行为应由 `.trellis/workflow.md` Markdown 定义，spec marketplace 不承载 task/runtime 私有状态；当前总体扩展方式符合官方扩展面。

## Fresh 验证

- `ChangeContextDiscoveryTests`：30 passed
- package/distribution tests：6 passed
- source Skill validator：passed，3 active skills / 9 exits / 6 targets
- installed validator：passed，128 managed files / 0 sidecar / 0 removal / 0 conflict
- upstream ownership：passed，43 active frozen entries / 13 managed claims
- dogfood overlay drift：passed
- `git diff --check origin/main...HEAD`：passed
- Phase 2 committed evidence 另记录：
  - full isolated pytest：606 passed in 179.37s
  - clean public marketplace throwaway：exit 0
- 未重新运行完整 606 tests 和完整 throwaway；本轮 fresh 验证聚焦 change-context、package、distribution 与静态门禁。

## Findings

### P1：Duplicate candidate 的 live facts 与 digest 可完全伪造

位置：

- `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/111-guru-discover-change-context/trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:18939`
- `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/111-guru-discover-change-context/trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:19266`

`duplicate_search.candidates` 当前只校验 identity 唯一性和 schema shape。Validator 没有：

- 从 candidate fields 重算 `facts_sha256`
- 约束 identity、URL、repo 与 issue number 一致
- live re-read candidate 并确认仍为 open
- 把 duplicate drift 纳入 `refresh_base`

最小复现向合法 snapshot 注入不存在的 `#999999`、任意 URL 和 `facts_sha256="f"*64` 后，结果为：

```text
duplicate_structural_errors= []
duplicate_live_errors= []
```

这违反 PRD R4 的 live facts digest、`implement.md` 第 37 行要求的 deterministic fact adapter，以及 duplicate evidence 交给 clarification/intake 前必须可信的边界。伪造、关闭或错仓库 candidate 可进入 `context_ready`，影响后续 reuse/new issue 判断。

修订要求：增加 deterministic duplicate fact projection/digest 校验和 live GitHub re-read；校验 repo、number、identity、URL、state、updated time 与 digest；drift 使用稳定 stale code 并进入 `refresh_base`；补充 forged digest、identity/URL mismatch、closed-after-review、cross-repo 与 unreadable candidate tests。

### P2：`blocked` typed exit 可以携带 `ai_review_gate.status=passed`

位置：

- `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/111-guru-discover-change-context/trellis/skills/guru-team/packages/guru-discover-change-context/schemas/context-discovery.schema.json:57`
- `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/111-guru-discover-change-context/trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:18977`

Schema 的 `blocked` conditional 只要求 `error`；runtime 只约束 `context_ready` 必须对应 passed Gate，没有约束 `blocked` 必须对应 blocked Gate。

最小复现把合法 snapshot 改为 `typed_exit=blocked`、补充合法 error、保留 passed Gate 后，结果为：

```text
blocked_gate_status= passed
blocked_structural_errors= []
```

这允许生成语义自相矛盾且 validator-passed 的 gate artifact，破坏 semantic 五阶段和 typed-exit 审计可信度。

修订要求：canonical schema 和 runtime 同时强制 `typed_exit=blocked -> ai_review_gate.status=blocked`，并增加正反向回归测试；随后同步所有 installed/platform copies。

## Docs SSOT 结论

Docs SSOT 的组织、stable ids、workflow/preset/public docs 分发整体一致，refresh ancestor/receipt、Git trackability、current-before-history、upgrade/update 与安全边界均已同步。

但当前存在两项 current-scope Docs/实现不一致：

- `implement.md` 要求 deterministic duplicate fact adapter，runtime 未实现。
- semantic Gate 与 `blocked` typed exit 的一致性未被 schema/runtime 封闭。

因此 Docs SSOT Gate 不通过，不能把当前 diff 视为 R1-R10/AC1-AC16 已闭环。

## Issue Scope 结论

`issue-scope-ledger.json` 分类正确：

- `close_issues`：仅 #111
- `related_issues`：#53、#96、#97、#98、#100、#101、#105、#109、#110、#112、#113
- `followup_issues`：空

未发现错误关闭语义。但由于上述 findings，#111 当前尚不能验收关闭。

## 部署与安全结论

- 无 Docker、K8s、数据库 migration、Makefile、业务配置或服务部署变更。
- 存在公共 workflow、preset、schema、runtime 与多平台安装面影响。
- Trellis CLI compatibility evidence 当前只覆盖 `0.6.5`；npm `0.6.7` 未验证，已在 handoff 中正确披露。
- Exact remote feature-ref marketplace verifier 尚未运行，按合同留给 finish-work。
- P1 finding 属于 intake evidence 完整性风险，必须在发布前修复。

## 最终结论

- P0：0
- P1：1
- P2：1
- P3：0
- 结论：`block`

当前 HEAD 不得通过 Branch Review Gate。两项 finding 修复后必须返回实现与完整 Phase 2，再创建新 commit，并由 finding owner 对新 HEAD 完整复审；closure 完成后还必须由新的 final reviewer 对完整 diff 独立放行。
