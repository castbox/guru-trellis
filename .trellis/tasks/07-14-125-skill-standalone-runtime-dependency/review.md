# Issue #125 Branch Review 汇总

## 审查范围

- Task：`125-skill-standalone-runtime-dependency`
- Intake base：`origin/feat/122-guru-create-task-commit`
- 当前审查 HEAD：`93d9a416bd6b34a87844dde5d4d9da363af729c2`
- 完整范围：`origin/feat/122-guru-create-task-commit...93d9a416bd6b34a87844dde5d4d9da363af729c2`
- Issue scope：`close_issues=[125]`、`related_issues=[122]`、`followup_issues=[]`

## 审查轮次

| 轮次 | 角色 | 技术身份 | reviewed HEAD | Findings | 原始报告 | 结论 |
| --- | --- | --- | --- | ---: | --- | --- |
| 001 | 最终放行审查代理 | `/root/trellis_final_review_125` | `e4937dfe19c9e3d889144ca5ef9d7afd42a429b5` | 1 | [001-final-review.md](reviews/001-final-review.md) | blocked |
| 002 | 问题闭环审查代理 | `/root/trellis_final_review_125` | `93d9a416bd6b34a87844dde5d4d9da363af729c2` | 0 | [002-finding-closure.md](reviews/002-finding-closure.md) | closure passed |
| 003 | 最终放行审查代理 | `/root/trellis_final_review_125_r3` | `93d9a416bd6b34a87844dde5d4d9da363af729c2` | 0 | [003-final-review.md](reviews/003-final-review.md) | final passed |

## 问题生命周期

### F-001 Source validator 接受 dispatcher 自指 command mapping

- 严重度：`P2`
- 首次发现：Round 001
- Finding owner：`/root/trellis_final_review_125`
- 影响路径：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- 问题：source/installed validation 允许 `runtime_command=run-skill-command`，但 runtime resolver 明确拒绝 `runtime_command == dispatcher`，导致确定不可调用的 package 可以通过验证和分发后才在调用时 blocked。
- 修复：revision commit `93d9a416bd6b34a87844dde5d4d9da363af729c2` 新增共享 self-mapping 判定，由 source validator 与 runtime resolver 共用；永久 regression 精确断言 schema 合法、dispatcher published 且只返回唯一 self-mapping error。
- Phase 2：fresh 381 tests 与 source/installed/dogfood/static/sidecar gate 通过。
- Closure：Round 002 由 finding owner 复核，`findings_count=0`。
- 当前状态：closed。

## 最终审查

Round 003 由 fresh technical identity `/root/trellis_final_review_125_r3` 对完整两提交 diff 执行最终放行审查，`findings_count=0`。该身份此前未参与实现、Phase 2、finding、closure 或任何 review round；Round 001 finding owner 与 Round 002 closure agent 均未承担最终放行。

## 证据

- Round 001 raw report SHA-256：`38df040fd7307f94b0ce614aaa04607150f7a9b304970a9f26f460e7b60bc40d`
- Round 002 closure report SHA-256：`f4a77e4952fa02f6cc85ac1338c09f8a6326c5eab76dc0e7b7d8a2c4cc142e94`
- Round 003 final report SHA-256：`9236cf4ca35dd3e2eeb6c890b72e1aea1dfcc711aecd5dd04c8eef56ad49ce2e`
- Fresh Phase 2 report SHA-256：`b161422f35ee2bc4f1787bddc663711b042efd7c56033bee1603a5045a5126fe`
- Reviewer 独立复验：5 package tests、64 skill package tests、36 installer tests、275 runtime tests，共 380 tests passed。
- F-001 修复后独立复验：5 package tests、65 skill package tests、36 installer tests、275 runtime tests，共 381 tests passed。
- 通过项：JSON/Bash/Python static、canonical/platform copy 与 executable mode、sidecar scan、commit plan/tree/diff 审计。
- Docs SSOT：`ssot_first` 已完成，四份 `.trellis/spec/**`、durable requirements、workflow/package contract 与三份 public README 一致；F-001 是机器合同实现缺口。
- 安全与部署：未发现 secret/customer data 泄露；无服务、API、数据库 migration、容器、Kubernetes、CI/CD 或 Makefile 影响。
- Round 003 独立 canary：当前 reviewed HEAD 的 clean throwaway、初装 standalone probe、`trellis update`、workflow re-selection、preset reapply、二次 probe、source/installed validation 与 sidecar scan 通过。
- 未完成门禁：exact feature-ref remote marketplace verification 仍必须在 reviewed content push 后由 `trellis-finish-work` 完成。

## 观察项

1. `task-commit-plans/001.json` 的 post-commit result 与 `agent-assignment.json`、本 review 产物属于 task-local metadata tail。
2. Issue #125 的 `acceptance_evidence[]` 必须在 publish 前依据真实验证补齐。
3. #125 仍 stacked 于 PR #124；#124 合并后必须 retarget 到 `main` 并重跑 freshness-sensitive gates。

## 后续候选

无。F-001 属于当前批准范围，不能转为 follow-up issue。

## 结论

- 当前开放 findings：`P0=0, P1=0, P2=0, P3=0`
- Finding closure：`passed`
- Final review：`passed`
- Branch Review Gate：`ready to record pass`
- 下一路由：主会话运行 Branch Review recorder/validator；通过后停止 `trellis-continue`，等待显式 `trellis-finish-work`。
