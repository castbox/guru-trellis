# Round 2 问题闭环审查报告

## 审查身份

- 逻辑角色：问题闭环审查代理，Round 2；不得作为最终放行 reviewer
- Technical agent id：`issue114_closure_review_r2`
- Reuse decision：`new-agent`
- Reviewed HEAD：`6bfedae44d7636ef56850d7e187c2e11b0e1967b`
- Diff range：`origin/main...HEAD`
- 审查方式：只读独立语义审查；未修改文件、未提交、未 push，未调用 Guru Team recorder/validator

## 审查范围

- 完整读取 `prd.md`、`design.md`、`implement.md`、`planning-approval.json`、`contract-wording-review.json`、`phase2-check.json`、`issue-scope-ledger.json`、implement/check handoff、Round 1 原始报告与 rollup。
- 审查 `origin/main...HEAD` 全部 89 个 committed paths，以及 `dfde7dd...6bfedae` finding-fix 提交。
- 复核 canonical Skill、shared runtime、workflow、schema、registry、extension manifest、preset installer、四平台副本、durable requirements/spec/README。
- 实时刷新 GitHub Issue #114、Trellis custom workflow 与 spec marketplace 官方文档。
- 核对 legacy 删除、archive、排除 issue、部署资产和敏感信息边界。

## 关闭对象

Round 1 `P2-extension-artifact-contract` 已正确关闭：

- `trellis/guru-team-extension.json:44` 已登记 `contract-wording-review.json`。
- `.trellis/guru-team/extension.json:44` 已同步相同 artifact contract。
- `test_apply_guru_team_trellis_preset.py:1165` 同时读取并断言 canonical inventory。
- `test_apply_guru_team_trellis_preset.py:1172` 断言安装后 manifest inventory。
- `dfde7dd...6bfedae` 的语义代码变更仅为上述两份 manifest 和对应 preset regression；没有改变 Skill profile、schema、runtime 或 routing。
- `round 1 P2=closed`。

## Findings

### P1：真实 GitHub authoritative comment 缺少 runtime 所读取的 `updatedAt`，导致 live `change_request` 固定 profile 无法执行

- `guru_team_trellis.py:3058` 通过 `gh issue view --json comments` 读取评论。
- 该命令返回的真实 comment keys 为 `author`、`body`、`createdAt`、`id`、`url` 等，不包含 `updatedAt`。
- `guru_team_trellis.py:8099` 却只读取 `comment.get("updatedAt")`，并在 `:8100` 将其缺失判为错误。
- 正常路径复现：
  - `gh issue view 120 --repo castbox/guru-trellis --json comments --jq '.comments[0] | keys'` 不含 `updatedAt`。
  - 将该真实 comment id 作为 `selected_comments[]` 调用 `record-contract-wording-review --profile change_request --scan-only`，稳定返回 `change_request selected comment author or updated_at is missing.`。
  - 同一评论通过 GitHub REST API 可得到 `updated_at`，说明数据存在，但当前 adapter 未读取。
- 当前测试 `test_contract.py:242` mock 了一个带自造 `updatedAt` 的 `issue_view` payload，仅覆盖缺 author 的拒绝分支，没有覆盖真实 GitHub CLI comment shape 的成功路径。
- 影响：任何包含 AI 选定 authoritative comment 的 live issue review 都在 scope build 阶段失败，既不能扫描也不能产生 evidence。静默不选择该评论会违反 #114 的 fixed authoritative scope 语义。
- 该问题可在公开 live issue 的正常只读路径复现，不涉及伪造、篡改、对抗输入或非常规并发。
- Required fix：通过提供真实评论更新时间的 GitHub API/GraphQL adapter 构造 stable comment identity、author、updated time、body/hash，并增加与真实 adapter shape 一致的 live selected-comment 正向回归。修复后需重新执行 implementation、完整 Phase 2、task commit 和 fresh closure review。

Findings 统计：

- P0：0
- P1：1
- P2：0
- P3：0
- Findings count：`1`

## 验证

- Package tests：`14/14 passed`
- Runtime tests：`500/500 passed`
- Preset tests：`39/39 passed`
- Source package validation：5 active skills、17 exits，通过
- Installed validation：208 managed、0 sidecar、0 removal、0 conflict
- Canonical/installed/Agents/Codex/Cursor/Claude package trees 一致
- Canonical 与 dogfood workflow 一致；dogfood overlay drift check 通过
- `git diff --check origin/main...HEAD` 通过
- Legacy owner 搜索仅剩 `--normative-hit` 负向测试
- Archive、CI/CD、容器、K8s/Kustomize、Helm、DB migration、Makefile 均无 diff
- 审查命令未产生额外工作区文件；HEAD 始终为 `6bfedae`

## Docs SSOT 判断

Canonical package 仍是 vocabulary、classification 和 semantic loop 的唯一 owner；workflow、requirements、README 和 specs 只引用 stable Skill/profile/schema/exit，Round 1 manifest inventory 缺口已收敛。

但 durable docs 明确要求 selected authoritative comment 绑定 updated time，而真实 runtime adapter 无法提供该字段，因此 Docs SSOT 与正常 live implementation 尚未完成语义收敛。该不一致由上述 P1 阻塞。

## 部署与安全判断

- 不涉及服务部署、数据库迁移、CI/CD、容器或生产配置。
- 未发现 token、secret、`.env`、private key、签名 URL、客户数据或敏感原始记录。
- 未扩张 #101、#112、#129、#132，也未引入恶意 actor、对抗输入或非常规并发加固。
- 安全与部署范围无独立 finding。

## 观察项

- 官方 Trellis 文档本轮可读取，当前 Markdown workflow 与 deterministic script 分层符合官方扩展面。
- 分支未 push，因此真实 remote marketplace branch 安装仍须留待 publish gate。
- `issue-scope-ledger.json` 的 #114 `acceptance_evidence` 仍为空，须在 publish 前补齐。
- 当前 dirty paths 均为既有 review/assignment/commit-result metadata tail，不属于未审查 source 变更。

## 后续候选

无。P1 属于 Issue #114 已明确要求的 live `change_request` authoritative-comments 正常路径，必须在当前 issue 内修复，不应转为 follow-up。

## 结论

- Round 1 P2：`closed`
- Round 2 总体结论：不通过
- `reviewed_head=6bfedae44d7636ef56850d7e187c2e11b0e1967b`
- `findings_count=1`
- `reuse_decision=new-agent`
- 必须关闭上述 P1 后，再由 fresh closure reviewer 复核；本代理不得承担最终放行审查。
