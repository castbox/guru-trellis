# Issue #97 Branch Review Gate 汇总

## 审查轮次

### Stale partial：前任问题发现审查

- 技术身份：`/root/issue97_branch_finding`
- 状态：`evt-0041-987e0ccea6` 记录 `stale-assessed`，`evt-0042-cf2b0928e1` 记录 `terminated-unfinished`。
- 报告：[round-001-finding.md](reviews/round-001-finding.md)
- 证据地位：该报告在 stale cutover 后写入，不登记为有效 review round，不用于 Gate 判断，仅保留审计轨迹。

### Round 1：替换问题发现审查

- 技术身份：`/root/issue97_branch_finding_replacement`
- 逻辑角色：`问题发现审查代理`
- Reviewed HEAD：`53f265f3949ca8374c7b534da309a4c924325450`
- 报告：[round-001-replacement-finding.md](reviews/round-001-replacement-finding.md)
- 结论：`FAIL`，P2 四项、P3 一项，共五项 current-scope finding。

### Round 2：新代理问题闭环审查

- 技术身份：`/root/issue97_closure_round2`
- 逻辑角色：`问题闭环审查代理`
- Reviewed HEAD：`0abdc0f97911c28b96439f2ba2c1dd3c1aa5bfaf`
- 复用决策：`new-agent`，从 Round 1 到 Round 2。
- 报告：[round-002-closure.md](reviews/round-002-closure.md)
- 结论：`FAIL`，Round 1 的四项及 Phase 2 两项 P3 已闭环，但发现一个新的 P2，因此该代理成为 finding owner。

### Round 3：同一 finding owner 闭环

- 技术身份：`/root/issue97_closure_round2`
- 逻辑角色：`问题闭环审查代理`
- Reviewed HEAD：`017b9f351bfbb90fcfca3a3935a9167de645b97c`
- 复用决策：`reuse-for-closure`，从 Round 2 到 Round 3。
- 报告：[round-003-closure.md](reviews/round-003-closure.md)
- 结论：`PASS`，`findings_count=0`；Round 2 的唯一 P2 已关闭，完整分支未发现新 current-scope finding。该代理不得转任最终放行审查代理。

### Round 4：最终放行审查

- 技术身份：`/root/issue97_final_round4`
- 逻辑角色：`最终放行审查代理`
- Reviewed HEAD：`017b9f351bfbb90fcfca3a3935a9167de645b97c`
- 复用决策：`new-agent`，从 Round 3 到 Round 4；该技术身份未参与任何 earlier review round。
- 报告：[round-004-final.md](reviews/round-004-final.md)
- 结论：`PASS`，`findings_count=0`；完整 `origin/main...HEAD`、前序 finding lifecycle、Phase 2、Docs SSOT、部署安全和 publish 边界均通过最终独立审查。
- 当前地位：仅对 `017b9f3` 有效；formal finish 后暴露新的 path identity P1，且当前 HEAD 已变为 `fd310e1`，本轮不再满足当前 Gate。

### Post-Gate：formal finish 真实路径碰撞

- 触发：显式 `trellis-finish-work` dry-run 通过，formal finish 在 archive 后生成 initial summary 时被 validator 阻断。
- 错误：`.trellis/guru-team/extension.json` 与 `trellis/guru-team-extension.json` 是两个合法路径，但 `index.search_terms.paths` 的 normalized duplicate 检查将其误判为同一项。
- 发布副作用：无 finish-summary、无 commit、无 push、无远端 branch、无 PR；task 已完整恢复到 active/in_progress。
- 修复提交：`fd310e15b08a2a29d253a1308b38816db7bc005d`。
- Fresh Phase 2：`/root/issue97_phase2_path_collision` 验证真实 collision build、Python validator 与 JSON Schema 均通过，P0/P1/P2/P3 均为 0。
- 下一步：由未参与 earlier review rounds 的 fresh `最终放行审查代理` 对 `origin/main...fd310e1` 完整 diff 做 Round 5 审查。

### Round 5：当前最终放行审查

- 技术身份：`/root/issue97_final_round5`
- 逻辑角色：`最终放行审查代理`
- Reviewed HEAD：`fd310e15b08a2a29d253a1308b38816db7bc005d`
- 复用决策：`new-agent`，从 Round 4 到 Round 5；该技术身份未参与任何 earlier review round。
- Liveness：一次 `status-requested` 后收到 `status-response-observed`，stale recorder 因新进展拒绝写入；代理随后正常 `completed`，不存在 stale/unfinished replacement 链。
- 报告：[round-005-final.md](reviews/round-005-final.md)
- 结论：`PASS`，`findings_count=0`；formal finish exact-path P1 与完整 `origin/main...HEAD` 均已闭环。

## 问题生命周期

| 来源 | 优先级 | 问题 | 关闭证据 | 状态 |
|---|---|---|---|---|
| Round 1 | P2 | Guru Team start/default context 与 Codex/Cursor session-start 仍读取或输出 workspace journal 元数据 | Round 2 验证 shared/Codex/Cursor no-workspace sentinel 与 installed behavior | 已关闭 |
| Round 1 | P2 | recovery 未绑定失败时的不可变 repo/base/head/title/body/draft 输入 | Round 2 验证 `pr-readiness.json.publish_inputs` 与 recovery command 只消费 immutable inputs | 已关闭 |
| Round 1 | P2 | Git path snapshot 失败未写双空 paths 与固定 unavailable fact | Round 2 发现 fixed fact 精确值仍有偏差，转为 Round 2 P2 | 已转交并关闭 |
| Round 1 | P2 | `guru-team-trellis-flow.md` 仍保留 journal/add_session 旧合同 | Round 2 验证 durable requirements 已收敛 | 已关闭 |
| Round 1 | P3 | throwaway verifier 缺最终 `.new`/`.bak` 清理与扫描 | Round 2 验证 preview cleanup、switch、update、workflow reapply、preset reapply、final scan | 已关闭 |
| Phase 2 | P3 | update 后未重新应用 marketplace workflow | Round 2 与 Round 3 的 public-main throwaway 到达最终 Gate | 已关闭 |
| Phase 2 | P3 | `py_compile` 后 public-surface test 会读取 `__pycache__` | Round 2 与 Round 3 验证排除 bytecode/cache，compile 后 canonical 仍为 302 | 已关闭 |
| Round 2 | P2 | snapshot-unavailable fixed fact 与批准 `design.md` 4.4 不一致，测试未锁完整对象 | Round 3 验证 canonical/dogfood 精确相等及三类失败路径完整对象断言 | 已关闭 |
| Formal finish | P1 | 合法 Git paths 被 normalized duplicate validator 折叠，导致 initial finish-summary 无法生成 | `fd310e1` 按 exact path identity 修复；fresh Phase 2 与 Round 5 验证真实 collision build/schema 通过 | 已关闭 |

## 最终审查

- 状态：`PASS`。
- 最终代理：`/root/issue97_final_round5`，fresh `最终放行审查代理`。
- 审查范围：`origin/main...fd310e15b08a2a29d253a1308b38816db7bc005d` 完整 diff。
- Findings：P0=0、P1=0、P2=0、P3=0。
- 充分性：代理独立复核 live #97、formal finish P1、path/semantic identity、完整五提交 diff、latest Phase 2、Docs SSOT、canonical/preset/overlay/dogfood、companion/schema/tests、issue scope、PR body、workspace tracking、部署安全与 publish 前 current-ref gate；全部 current-scope finding 已关闭且无新回归。

## 证据

- Round 1 有效报告 SHA-256：`32c2638c8715a4bbf6c838c87ec163761caecf1831c6dbfbe15ba23f86aecf4b`。
- Round 2 报告 SHA-256：`95f1dd1aec19f87a535114d0fda8896f9c8a643f10a739989d0bfbbac0e480f4`。
- Round 3 报告 SHA-256：`02c48eaab1b7de2e6853cc20e1bbeaceacf4170aab9cd226bd610414bebdc766`。
- Round 4 最终报告 SHA-256：`81800e0718be44f6e05f58eaf03b2e74d0500d39fc98adfd2a5a0cd14fef0bd2`。
- Round 5 当前最终报告 SHA-256：`7cefb69a8d4e3d0c33630f17ce10fee674a4e2f3f68aec8066260ffb9993b8d9`。
- 当前 HEAD：`fd310e15b08a2a29d253a1308b38816db7bc005d`；intake base：`ff8c03abb259c2a048626ea72e0bf57138db2c14`。
- Latest fresh Phase 2：P0/P1/P2/P3 均为 0；真实 collision build/schema、canonical 305、preset 36、定向 82、`python3 -S` 34 加 1 个 optional skip、251 tracked JSON 与 task-local JSON、compile、43 Bash、planning/workspace boundary、commit、drift/equality/sidecar 与 public-main throwaway 均通过。
- Git index 不跟踪 `.trellis/workspace/**`；`origin/main...HEAD` 保留三条预期删除记录。

## 观察项

- 默认 pinned tag `v0.6.5-guru.3` 尚未发布，当前分支也未 push；current-ref remote marketplace verifier 必须在正式 publish push 后执行，public-main sampling 不能替代该证据。
- 任务元数据保持未提交，符合 `trellis-continue` 在 Branch Review Gate 前后的约束。

## 后续候选

- #100 backfill CLI、#98 历史发现、#99 developer identity 均为明确非目标，不并入 #97。
- 当前没有需要新增 issue 的独立范围。

## Docs SSOT

- 当前 closure 结论：`PASS`。
- `requirement-main.md`、`guru-team-trellis-flow.md`、workflow/spec/README、canonical/overlay/dogfood 与 task design 已表达同一 finish-summary、no-workspace-read、immutable publish input 和 recovery 合同。
- `.trellis/spec/workflow/data-contracts.md` 已明确 path-bearing arrays 使用 exact string identity，非路径语义数组继续使用 normalized text identity。
- Task artifacts 仅保留规划、执行和审查证据，不替代 durable docs。

## 部署与安全

- 完整 diff 未修改 GitHub Actions/CI/CD、Dockerfile/Compose、Kubernetes/Kustomize、Helm、数据库 migration/seed/backfill 或 Makefile，也未新增 API、服务、worker、定时任务、队列、数据库结构或业务运行时部署入口。
- 未发现 token、secret、private key、签名 URL、`.env`、数据库 URL、客户数据或 workspace journal 内容迁移。
- 默认 tag 与 remote current-ref 验证属于 publish gate，不是业务部署资产变更。

## 结论

Branch Review 独立审查结论：`PASS`。前三轮 findings 与 formal finish path identity P1 已由实现、fresh Phase 2 和 Round 5 关闭；fresh final reviewer 对完整 `origin/main...fd310e1` 给出 `findings_count=0`，可由主会话重录并验证 current-HEAD Gate。真实 current-ref remote marketplace verifier 仍保留在正式 push 后、PR create 前的 publish gate。
