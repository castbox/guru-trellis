# Issue #111 Branch Review 问题闭环原始报告

## 审查身份

- 技术身份：`/root/issue111_branch_review`
- 逻辑角色：问题闭环审查代理
- 复用决策：`reuse-for-closure`
- 行为边界：只读审查；未编辑、stage、commit、push、创建 PR 或运行 recorder/validator。

## 审查范围

- Repository：`castbox/guru-trellis`
- Live issue：`#111`，状态 `OPEN`
- Base HEAD：`3395fad2a4049a33c4c679cd05452cfa45a85b92`
- Reviewed HEAD：`dc3e2e9a32b7b8db1dc7e5645f8599ddfa2700b7`
- 完整 diff：`origin/main...dc3e2e9`
- 修订 diff：`94d6126...dc3e2e9`
- 完整范围：114 files，24302 insertions，158 deletions
- 修订范围：59 files，3935 insertions，4053 deletions
- 修订提交：`fix(trellis): #111 收敛变更上下文发现范围`

工作区中的 `agent-assignment.json`、`task-commit-plans/002.json` 修改及未跟踪
review metadata 属于主会话后续记录，不在 committed diff 审查范围内。

## Live Scope Qualification

2026-07-16 更新后的 live issue 明确：

- 当前范围保留同一次 open duplicate search 返回字段的 deterministic projection、
  identity、URL、open state、updated time 与 `facts_sha256` 重算。
- 当前范围保留 `typed_exit` 与 AI Review Gate 的普通状态机一致性。
- post-review live re-read、closed-after-review、forged provenance、攻击者/威胁模型、
  hostile-input、fault injection、并发及类似非常规加固均排除。
- 排除项不得重新升级为 P0-P3 finding。

本轮按该范围重新定性 Round 001 的修订要求，没有把已排除场景作为闭环条件。

## Finding 生命周期

| ID | 原严重度 | 当前结论 | 状态 |
| --- | --- | --- | --- |
| BR-001 | P1 | deterministic duplicate projection/digest 缺口已修复；原报告要求的二次 live reread、关闭后漂移、cross-repo hostile-input 和 unreadable 场景在 scope update 后撤销 | closed |
| BR-002 | P2 | schema/runtime 已双向封闭 blocked exit 与 blocked Gate，正反向测试完整 | closed |

### BR-001

Runtime 在 `guru_team_trellis.py:18252` 建立候选事实投影，并在 `:18279` 校验：

- normalized `repo`
- positive non-boolean `number`
- `identity=#<number>`
- canonical issue URL
- `state=open`
- `updated_at`
- 从上述字段重算的 `facts_sha256`

Schema 在 `context-discovery.schema.json:279` 要求相同 closed shape。Runtime tests 在
`test_guru_team_trellis.py:16060` 覆盖合法候选、错误 digest、identity mismatch 和 URL
mismatch。

实现没有加入第二次 duplicate search 或 post-review candidate reread，符合更新后的明确范围。

### BR-002

Schema 在 `context-discovery.schema.json:57` 和 `:66` 双向约束：

- `typed_exit=blocked -> ai_review_gate.status=blocked`
- `ai_review_gate.status=blocked -> typed_exit=blocked`

Runtime 在 `guru_team_trellis.py:18557` 实施相同约束。Runtime 与 package tests 分别在
`test_guru_team_trellis.py:15376` 和 `test_contract.py:153` 覆盖 passed Gate + blocked exit、
blocked Gate + ready exit 及合法 blocked pair。

## Fresh 验证

- Targeted contract/runtime suite：29 tests passed
- Source Skill validator：3 active skills、3 invoke markers、9 exits、6 targets，passed
- Installed Skill validator：128 managed files，0 sidecar/removal/conflict，passed
- Canonical、installed、Agents、Codex、Cursor、Claude package：排除解释器缓存后逐字节一致
- Canonical/installed runtime SHA-256：一致
- Upstream ownership：43 active、13 managed claims，passed
- Dogfood overlay drift：passed
- `git diff --check origin/main...dc3e2e9`：passed

完整 589 tests 和 clean throwaway 未在闭环轮次重跑；fresh Phase 2 evidence 记录两者通过，
本轮针对两项 finding 重新运行了直接覆盖其行为的测试和分发门禁。

## Docs SSOT

Phase 2 指出的两处旧范围残留已在修订提交中更新：

- `docs/requirements/guru-team-trellis-flow.md`
- `docs/requirements/requirement-main.md`

Durable docs 现统一描述单次 duplicate search 投影重算、不进行二次 reread、普通 refresh
re-entry，以及 blocked exit/Gate 双向一致性。Canonical spec、package contract、public docs、
workflow/preset README 和多平台副本同步一致。

## Issue Scope

`issue-scope-ledger.json` 仍保持：

- `close_issues`：仅 `#111`
- `related_issues`：`#53/#96/#97/#98/#100/#101/#105/#109/#110/#112/#113`
- `followup_issues`：空

未发现错误关闭语义。

## 部署与安全

- 无 Docker、K8s、数据库 migration、Makefile 或业务配置变更。
- 存在公共 workflow、preset、schema、runtime 与多平台安装面变更。
- Source/installed、ownership 和 dogfood 门禁通过。
- Exact remote feature-ref marketplace verification 仍按合同留给 push 后的 publish
  readiness，不构成本轮 finding。
- 未发现当前 live scope 内的新增部署或安全阻塞项。

## 结论

- `findings_count: 0`
- P0：0
- P1：0
- P2：0
- P3：0
- `reuse_decision: reuse-for-closure`
- 结论：`closure-pass`

BR-001 与 BR-002 均已在新 HEAD 闭环。该结论只表示 finding owner 闭环通过，不得作为最终
放行；仍须由未参与既有轮次的独立最终审查代理覆盖完整
`origin/main...dc3e2e9` diff。
