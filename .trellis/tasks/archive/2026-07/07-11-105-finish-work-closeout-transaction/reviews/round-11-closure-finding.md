# Issue #105 Branch Review Round 11 问题闭环报告

## 审查身份

- 逻辑角色：问题闭环审查代理
- technical agent：`/root/final_release_review_105_round9`
- 复用依据：Round 9/10 同一 P1 finding owner，仅允许 closure
- reviewed_head：`c8ad047493414d58862281866a447c4f02fa0d4d`
- diff_range：`origin/main...HEAD`
- reuse_decision：`reuse-for-closure`
- findings_count：`1`
- 结论：`fail`

## 审查范围

只读复核了 exact committed archive fast-path、fresh archived recovery、plan-only locator、incomplete/mismatch fallback、remote PR identity、archive path/tree/blob/task.json/lineage、生产 failure matrix、Docs SSOT、Phase 2、ledger、部署与安全。

## 问题生命周期

### Round 9/10 P1：post-archive 恢复仍可能被本地 artifact 阻断

状态：`open，fast-path 已修复，但 plan-only 真实入口仍未闭环`

已确认关闭的部分：

- `resolve_committed_closeout_archive_transaction()` 只有在当前 HEAD 的 archive diff path set 精确匹配时才进入 fast-path。
- fast-path 继续校验 evidence parent、evidence commit path/tracked tree、archive commit完整 tree、tracked blob continuity和官方 `task.json.status/completedAt` 差异。
- 任一 HEAD/path/tree/blob/parent 不匹配都会返回 strict incomplete recovery。
- incomplete move 仍校验 archived working-tree layout、dirty/staged exact set、blob continuity、task.json、commit lineage。
- exact commit 已存在时，missing/tampered archived working tree 不再影响 Git fast-path和 remote ready。
- remote repo/head/base/title/body digest、bound number/URL、fork/multiple/missing/mismatch 保护未回退。

仍未关闭的入口缺口：

- `cmd_finish_work()` 在 `guru_team_trellis.py:12392` 已允许解析只剩 `closeout-plan.json` 的 archived directory。
- 但随后在 `12393-12394` 读取缺失的 task context 后立即执行普通 workspace boundary。
- 默认配置为 `workspace_mode: worktree`。
- `workspace_boundary_errors()` 在 `4073-4074` 对缺少 `task-start-context.json` 固定报错，发生在 archived recovery 和 committed fast-path之前。
- 实际只读探针确认返回：`workspace boundary 缺少 task-start-context.json，无法确认 task-local portable context。`

生产测试未覆盖该入口：

- production fixture 在 `test_guru_team_trellis.py:11080` 全程 mock `assert_workspace_boundary()`。
- 因此 missing-artifact 用例虽然真实调用 `cmd_finish_work()`、`resume_archived_closeout()` 和 metadata fast-path，却没有证明默认 worktree 项目中只剩 plan 的真实入口可达。
- durable docs 明确承诺 plan-only archived directory 可由 `trellis-finish-work` 恢复，当前实现仍与该合同不一致。

这仍属于 Round 9/10 同一 P1，不是新的功能范围。

## 验证证据

独立复跑：

- canonical tests：`388/388 pass`
- targeted closeout：`54/54 pass`
- preset tests：`36/36 pass`
- overlay drift：pass
- canonical/dogfood Python 与 workflow equality：pass
- `git diff --check origin/main...HEAD`：pass
- Phase 2 的 13 个 `dirty_paths` 与 `6b8e193..c8ad047` 非 metadata 路径精确一致
- Phase 2 记录 20 项 P1 为 resolved，但最后一项缺少未 mock workspace boundary 的 plan-only production evidence，本轮不接受其 resolved 结论

## Docs SSOT

durable specs、requirements、workflow 和 README 已同步区分：

- exact archive commit 前：严格 working-tree/layout/dirty/staged恢复；
- exact archive commit 后：Git parent/path/tree/blob + remote-only ready；
- plan-only archived directory：仅 finish-work 可解析。

代码中的 workspace boundary 前置顺序使第三项不可达，Docs SSOT closure 为 `fail`。

## Ledger 与前序合同

- primary 与 close evidence 逐字一致。
- `388/388`、`54/54`、`36/36`、71 assets、initial #105、after-update #106 各唯一出现。
- scope：close `[105]`、related `[53,96,97,100]`、follow-up `[98,99,101]`。
- Round 1-8 及 remote transport、raw body、all-platform provenance、installed smoke、archive lineage等前序修复未发现回退。

## 部署与安全

未修改 CI/CD、容器、Docker Compose、Kubernetes/Kustomize、migration 或 Makefile。未发现真实 secret、token、私钥、`.env`、客户数据或签名 URL。

## 观察与后续

- 当前仅 task metadata/reviews tail 未提交。
- dogfood 保持三个平台、71 assets、无 sidecar。
- current-branch remote marketplace 与真实 GitHub E2E 仍由 publish-time verifier 承接。
- 远端仍不存在 `v0.6.5-guru.3`。
- follow-up candidate：0。

## 结论

Round 11 closure 失败，`findings_count: 1`，`reuse_decision: reuse-for-closure`。需要为 archived plan-only recovery 提供受限且 fail-closed 的 workspace boundary：从 immutable plan、当前 branch/repo root和 archived locator校验边界，而不是要求已缺失的 task context；对应生产测试不得 mock boundary。
