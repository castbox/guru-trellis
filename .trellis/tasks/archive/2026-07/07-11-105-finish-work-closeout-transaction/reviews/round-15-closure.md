# Issue #105 Branch Review Round 15 问题闭环报告

## 审查身份

- 逻辑角色：问题闭环审查代理
- technical agent：`/root/final_release_review_105_round9`
- 复用依据：Round 14 finding owner，仅允许 closure，不得最终放行
- reviewed_head：`94d44d7d116c22824cf629cef9f4a4cea4a98c52`
- diff_range：`origin/main...HEAD`
- reuse_decision：`reuse-for-closure`
- findings_count：`0`
- 结论：`pass-for-closure-only`

## 审查范围

只读复核了 direct/archive basename 候选的 two-stage preflight、matching/unmatched alias、ordinary candidate 顺序、plan-only fallback，以及 Round 9-14 全部 post-archive、remote identity、raw locator、committed boundary 和恢复合同。

## 问题生命周期

### Round 14 P2：unmatched direct alias 误阻断后续真实候选

状态：`closed`

- direct 和 archive candidates 已统一调用 `preflight_finish_work_ordinary_candidate()`。
- helper 先保留 lexical/lstat symlink evidence，再使用普通 resolver 相同的 `is_dir + task.json.is_file` predicate。
- matching repo-root、active、ordinary archive 及恢复 `task.json` 后的 plan-only alias 继续 fail closed。
- unmatched repo-root、active 和 archive alias 不再遮蔽后续真实 active/archive 候选。
- 首个真实 ordinary candidate 仍立即胜出，顺序与普通 resolver 一致。
- path-like 输入仍在普通 resolver 前执行 raw lexical/symlink preflight。

### 前序生命周期

以下合同均未发现回退：

- Round 9-11 post-archive remote-only 与 exact committed fast-path
- strict incomplete archive recovery
- plan-only committed workspace boundary
- raw relative/absolute/ancestor/final/multilevel/dangling/loop alias 拒绝
- Darwin 固定 `/var -> /private/var` 映射
- active/普通 archive 优先、unique/exact plan-only fallback、多月份歧义阻断
- remote repo/head/base/title/body digest、bound PR、fork/multiple/mismatch
- active summary/body/ledger/readiness/marketplace 完整校验
- archive path/tree/blob/task.json/parent/HEAD 保护
- all-platform provenance、installed closeout 及前序 ledger 修复

## 验证证据

独立复跑：

- canonical tests：`404/404 pass`
- targeted closeout：`55/55 pass`
- WorkspaceBoundaryGuard：`21/21 pass`
- preset tests：`36/36 pass`
- overlay drift：pass
- canonical/dogfood Python 与 workflow equality：pass
- `git diff --check`：pass
- Phase 2 的 13 个 `dirty_paths` 与 `6177fe9..94d44d7` 非 metadata 路径精确一致
- Phase 2 共 24 项 finding，均为 resolved

## Docs SSOT

`companion-scripts.md`、`data-contracts.md`、`workflow-contract.md`、requirements、canonical/dogfood workflow 及 README 已统一表达：

- matching alias 在 ordinary resolve 前拒绝；
- unmatched alias 继续后续 candidate；
- ordinary task 优先，plan-only 仅作唯一 fallback；
- committed fast-path 和 strict incomplete recovery 分流。

Docs SSOT：`pass`。

## Ledger 与范围

- primary 与 close acceptance evidence 逐字一致。
- `404/404`、`55/55`、`21/21`、`36/36`、71 assets、initial #105、after-update #106 均唯一完整。
- close：`[105]`
- related：`[53,96,97,100]`
- follow-up：`[98,99,101]`

## 部署与安全

未修改 CI/CD、容器、Docker Compose、Kubernetes/Kustomize、migration 或 Makefile。未发现真实 secret、token、私钥、`.env`、客户数据或签名 URL。

dogfood 保持 `claude/codex/cursor`、`all_platforms=true`、71 assets，无 sidecar 或 backup。

## 观察与后续

- current-branch remote marketplace 与真实 GitHub E2E 仍由 publish-time fail-closed verifier 承接。
- 远端不存在 `v0.6.5-guru.3`，不得声明 stable tag 路径已验证。
- 当前未提交内容仅为 task metadata/reviews tail。
- follow-up candidate：0。

## 结论

Round 14 P2 已完整闭环，当前未发现新的 P0-P3，`findings_count: 0`。Round 15 仅通过问题闭环，`reuse_decision: reuse-for-closure`，不得作为最终 Branch Review Gate 放行依据；仍需派发新的 fresh final reviewer。
