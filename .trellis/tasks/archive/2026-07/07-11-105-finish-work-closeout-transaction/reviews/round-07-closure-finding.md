# Issue #105 Branch Review Round 7 闭环报告

## 审查身份

- 逻辑角色：问题闭环审查代理
- technical agent：`/root/final_release_review_105_round6`
- 复用依据：Round 6 三项 finding owner，仅允许 closure，不得最终放行
- reviewed HEAD：`4f634a73d887016f9b25dc07a98de8a94d171aa4`
- diff range：`origin/main...HEAD`
- findings_count：`1`
- 结论：`fail`

## 审查范围

复查 Round 6 三项 P1、Phase 2 新增的 ancestor/outer alias 与 ledger evidence 问题、`533d9e5..4f634a7` 的 16 个非 metadata 文件，以及前序 closeout、remote、archive、recovery、Docs、部署与安全合同。

Phase 2 `head=533d9e5`；其 16 个 `dirty_paths` 与修复提交的 16 个非 metadata 文件精确相等。Round 6 报告哈希和 6→7 `reuse-for-closure` 记录一致。

## 问题生命周期

### Round 6 P1-1：dogfood all-platform provenance

状态：`closed`

- manifest 已恢复 `claude/codex/cursor`、`all_platforms=true`。
- `managed_assets` 为排序去重后的 71 项，五个 Claude 资产恢复 ownership。
- 用户拥有的 `config.yml` 已排除，`config-template.yml` 仍受管理。
- `managed_backups=[]`，无 `.new/.bak`，overlay drift 通过。

### Round 6 P1-2：task-local raw reviewed body

状态：`closed`

- finish-work 使用专用 resolver，不再复用 legacy trim resolver。
- 仅接受当前 active task 的 direct `pr-body.md`，拒绝 `--body-artifact` 和 external source。
- 原始 bytes 逐字相等并 strict UTF-8 decode；空白、最终换行和 Markdown hard-break 差异被拒绝。
- 从 repo root 到 final file 逐 lexical component `lstat`，拒绝 task parent、ancestor、final、dangling、loop 和多层 symlink。
- 仅允许经 `/var` 自身 `lstat/readlink` 和 suffix 结构验证的 Darwin `/var -> /private/var` 固定映射。
- generic `publish-pr` 兼容路径未回退。

### Round 6 P1-3：installed closeout smoke

状态：`closed`

- helper 加载实际安装的 `.trellis/guru-team/scripts/python/guru_team_trellis.py` 并调用安装后的 `finish-work.sh`。
- 初装 #105 和 update/reapply 后 #106 均完成 digest、formal、draft、官方 archive、三方 HEAD、ready、summary URL/ref 和 clean tree。
- Git 使用真实 repo/bare remote；GitHub 使用受控 fake adapter，不产生外部发布。

## 发现项

### P1-1：Issue Scope Ledger 缺少 targeted `50/50` 验证证据

证据：

- `phase2-check.json` 明确记录 `targeted closeout tests = 50/50 pass`。
- `issue-scope-ledger.json` 的 primary issue 与 close issue 只记录 canonical `384/384`、preset `36/36`、71 assets 与两轮 installed smoke，没有 `targeted 50/50`。
- Round 7 指定核对口径为 ledger `384/50/36/71/two smoke`，当前 ledger 未形成完整证据组。

影响：

#105 的 Phase 2 已有 targeted 结果，但最终 issue close ledger 未承接该项，发布时关闭证据不完整。不能用 Phase 2 旁路记录替代 ledger acceptance evidence。

建议：

在 primary issue 和 close issue 的相同 acceptance evidence 中明确加入 `targeted closeout 50/50`，保持两处逐字一致；随后刷新 Phase 2 artifact digest并由 finding owner复核。

## 验证证据

- canonical tests：`384/384 pass`
- preset tests：`36/36 pass`
- 初装与 update/reapply 后 installed closeout：均 pass
- 两轮 local/remote/PR HEAD 相等，PR ready、summary URL/ref 和 clean tree通过
- `git diff --check origin/main...HEAD`、canonical/dogfood equality、overlay drift、sidecar扫描通过

## Docs、部署与安全

Round 6 三项修复的 durable specs、workflow 和 README 已同步，未发现旧事务语义回退。未变更 CI/CD、容器、K8s/Kustomize、DB migration、Makefile 或部署资产；未发现敏感信息泄露。

## 观察项

- 当前分支仍未推送，current-branch remote marketplace 与真实 GitHub closeout E2E 留待 publish-time verifier。
- throwaway workflow 使用 public `main` sample，preset/companion 来源为当前 `4f634a7`。
- 远端仍不存在 `v0.6.5-guru.3` tag。
- scope 分类正确：close `[#105]`；related `[#53,#96,#97,#100]`；follow-up `[#98,#99,#101]`。

## 后续候选

0。

## 结论

Round 6 三项 P1 实现均已闭环，但 ledger 缺少 targeted `50/50` acceptance evidence，Round 7 闭环不通过。修复后需再次 closure，并派发新的 fresh 最终放行审查代理。
