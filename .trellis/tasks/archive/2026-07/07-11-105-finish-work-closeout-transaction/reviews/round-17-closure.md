# Issue #105 Branch Review Round 17 问题闭环报告

## 审查身份

- 逻辑角色：问题闭环审查代理
- technical agent：`/root/final_release_review_105_round16`
- 复用依据：Round 16 两项 P1 finding owner，仅允许 closure，不得最终放行
- reviewed_head：`d8bde831632c7e0e3141ae005fcea973092d8702`
- diff_range：`origin/main...HEAD`
- reuse_decision：`reuse-for-closure`
- findings_count：`0`
- 结论：`pass-for-closure-only`

## 审查范围

只读复核了：

- Round 16 的 commit message P1 与 continue overlay Docs SSOT P1
- rewrite 前 `1d3eab54` 和 rewrite 后 `d8bde83` 的完整 12-commit tree 序列
- 12 个 work commit 的 subject、body 与实际 path/tree delta
- 五份 canonical 与五份 dogfood `trellis-continue` surfaces
- 旧语义负向扫描和新事务正向断言
- Round 1-15、历史 24 项 Phase 2 finding 和核心 closeout/recovery 合同
- Phase 2、ledger、manifest、测试、同步、安全及部署证据

未修改文件，未运行 recorder，未 commit、push 或创建 PR。

## Round 16 问题闭环

### P1-1：12 个工作提交缺少合同 body

状态：`closed`

- 当前 `origin/main..HEAD` 共 12 个 work commits。
- 每个提交均包含唯一且有实质内容的 `背景：`、`变更：`、`边界：`、`验证：`，末行均为 `Refs #105`。
- 未发现 commit close keyword。
- 独立结构检查的 12 个结果均为 `errors=[]`。
- 每份 body 均与该提交的真实 path delta 对应：初始事务、schema、workflow、preset、failure matrix、recovery、PR/repo identity、strict remote、installed smoke、post-archive 分流、locator/resolver 各轮修复和最终十个平台入口同步。
- Phase 2 记录的 `check-commit-messages` 结果为 `12/12 pass, errors=[]`。

History rewrite 保真证据：

- rewrite 前 HEAD：`1d3eab54ff52bbf202ecba0513957ed05741cd71`
- rewrite 后 HEAD：`d8bde831632c7e0e3141ae005fcea973092d8702`
- 两条链均为 12 个 commit tree。
- 两条 tree hash 顺序逐项一致。
- 两条顺序 digest 均为 `49ffd792ddb48d41fd99e28e4a4ebcef01355d8a31f3351b3affac665aebc78d`。
- 两个 HEAD 的最终 tree 相同。
- `refs/original` 为空；未保留 rewrite backup ref。

### P1-2：continue 平台入口保留旧 archive-first/initial-summary 语义

状态：`closed`

以下五组 canonical/dogfood 文件逐字相等：

- shared Agent skill
- Claude command
- Codex prompt
- Codex skill
- Cursor command

十个 surfaces 现在统一说明：

- archive 前绑定 immutable plan 并完成本地 validator
- push reviewed content
- 执行 required remote verifier
- commit/push plan、readiness 与 evidence
- 绑定唯一 exact draft PR
- 只构建一次 final summary projection
- archive metadata transaction 完成后仅校验 remote HEAD/PR binding 并执行 draft-to-ready
- archive 后不重建或改写本地 artifact，不新增 commit，不再次 push

旧 `archive-first`、`initial finish-summary`、post-archive tail 相关语义在十个 surfaces 中均无命中。

回归测试现已：

- 扫描原五个 workflow/spec surfaces 及新增十个平台 surfaces
- 包含扩展后的旧语义 forbidden phrases
- 对每个 continue surface 执行七项新事务正向断言
- 聚焦测试 `1/1 pass`

## 历史问题生命周期

Round 1-15 与历史 24 项 finding 未发现回退：

- immutable plan/digest 与 final projection 保持一致
- raw PR body、summary PR URL/ref、archive blob continuity 保持绑定
- headRepository、fork/multiple candidate、raw/effective remote identity 保持 fail closed
- installed initial #105/update #106 closeout 保持完整
- post-archive exact committed fast-path 保持 remote-only
- incomplete archive recovery 保持严格 layout/dirty/staged/blob/lineage 验证
- plan-only committed boundary 与 raw locator 保护保持有效
- ordinary resolver priority、unique/exact fallback 和 ambiguity 规则保持不变
- matching alias 仍拒绝，unmatched alias 不遮蔽后续真实 candidate

## 验证证据

- commit body 结构检查：`12/12 errors=[]`
- history tree sequence：`12/12` 逐项一致
- tree sequence digest：rewrite 前后均为 `49ffd792...`
- focused legacy/new continue contract：`1/1 pass`
- `WorkspaceBoundaryGuard`：`21/21 pass`
- preset tests：`36/36 pass`
- Phase 2 canonical：`404/404 pass`
- Phase 2 targeted closeout：`55/55 pass`
- installed closeout initial #105 与 after-update #106：pass
- Python compile、Bash syntax、Draft 2020-12 schema `4/4`、JSON/task artifacts、`git diff --check`：pass
- canonical/dogfood Python、workflow、schema 及五组 continue byte equality：pass
- 71 个 managed assets 排序、唯一且全部存在
- `.new/.bak`、`new_copies`、`managed_backups`：均为空
- Phase 2：`head=d8bde83`、`dirty_paths=[]`

## Docs SSOT

`companion-scripts.md`、`data-contracts.md`、`workflow-contract.md`、requirements、canonical/dogfood workflow、finish entries 及全部 continue entries 当前表达同一事务顺序。

Round 16 发现的平台入口冲突已消除，负向扫描范围已覆盖该类运行面。Docs SSOT：`pass`。

## Ledger 与范围

- close：`[105]`
- related：`[53,96,97,100]`
- follow-up：`[98,99,101]`
- primary 与 close acceptance evidence 逐字一致
- `404/55/21/36/71/two-smoke` 证据完整
- scope 未发生变化

## 部署与安全

- 未修改 CI/CD、Dockerfile、Compose、K8s/Kustomize、Helm、migration 或 Makefile。
- 未发现真实 token、secret、private key、`.env`、客户数据或签名 URL。
- userinfo/token 文字仅存在于 strict remote rejection 测试。
- 远端 identity 错误脱敏、credential 拒绝、fork 保护未见回退。

## 观察项

- current-branch remote marketplace 与真实 GitHub closeout E2E 仍由 publish-time fail-closed verifier 承接。
- 远端尚无 `fix/105-finish-work-closeout-transaction` branch。
- 远端不存在 `v0.6.5-guru.3` tag，不得声明 stable-tag 安装已验证。
- 当前未提交内容仅为 task metadata/reviews tail。
- dogfood manifest 的 `source.commit=94d44d7`、`tree_state=dirty` 是 preset apply 时的观测事实；其合同明确不表示 manifest 自身包含于该 commit，不构成本轮 finding。

## 后续候选

0。

## 结论

Round 16 两项 P1 均已闭环，当前未发现新的 P0-P3。

- P0：`0`
- P1：`0`
- P2：`0`
- P3：`0`
- findings_count：`0`
- reuse_decision：`reuse-for-closure`

本轮仅为问题闭环通过，不能作为 Branch Review Gate 最终放行依据。仍需派发此前未参与任何实现、Phase 2 或 Round 1-17 的新 technical agent，对 `origin/main...d8bde83` 执行完整最终放行审查。
