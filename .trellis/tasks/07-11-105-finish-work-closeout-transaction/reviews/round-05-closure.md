# Issue #105 Branch Review Round 5 闭环报告

## 审查身份

- 逻辑角色：问题闭环审查代理
- technical agent：`/root/final_release_review_105`
- 复用依据：Round 3/4 finding owner，仅允许 closure，不得最终放行
- reviewed HEAD：`533d9e54fb912a29e5a422219163afa9e2c3ec32`
- diff range：`origin/main...HEAD`
- Round 4 报告：`.trellis/tasks/07-11-105-finish-work-closeout-transaction/reviews/round-04-closure-finding.md`
- findings_count：`0`
- 结论：`pass-for-closure-only`

## 审查范围

复查了 strict GitHub transport parser、raw Git config gate、effective URL count/source binding、head repository 全链、production 无副作用重入，以及 `dbe3d4c..533d9e5` 九文件修复。

`phase2-check.json.head=dbe3d4c` 是修复提交前快照；其 9 个 `dirty_paths` 与 `dbe3d4c..533d9e5` 的 9 个非 metadata 文件精确相等，变更 spec 哈希与当前 HEAD 一致。当前仅有允许的 task metadata tail。

## 问题生命周期

### Round 4 P1：本地相对 remote 冒充 GitHub transport

状态：`closed`

- repo identifier 与 remote transport parser 已拆分。
- plan repo 仅接受规范化 `owner/repository`。
- effective remote 仅接受无凭据的 GitHub HTTPS、`ssh://git@github.com/...` 和 `git@github.com:...`。
- 裸 `owner/repo`、相对/绝对路径、`file://`、无 scheme、非 GitHub、HTTP、git protocol、userinfo、password、port、query、fragment、额外 path 均被拒绝。

### Phase 2 后续 P1：raw/effective URL 被 trim、split 或控制字符规范化

状态：`closed`

- strict parser 不执行 trim、replace 或补换行。
- raw url/pushurl 使用 `git config --null --show-origin --get-all` 读取；rewrite base/pattern 使用 NUL+origin `--get-regexp`。
- origin 文件存在 NUL 时直接 fail closed，覆盖 Git 输出在 NUL 处截断但返回合法前缀的场景。
- raw url、pushurl、rewrite base/pattern 拒绝边界 whitespace、C0/C1、DEL、NUL及全部 Unicode `C*` 类控制字符。
- 无显式 pushurl 时严格回退到 raw fetch source；effective fetch/push 项数分别绑定对应 raw source 数量。
- effective 输出要求唯一尾换行，不 trim、不 `splitlines()` 规范化，并逐项用 strict transport parser匹配 immutable repo。
- 错误 payload 不包含原始 URL、rewrite pattern或命令 stderr。

### 前序问题

headRepository/headRepositoryOwner/isCrossRepository、raw UTF-8 PR body、summary identity、archive blob continuity、partial recovery、旧合同负向扫描及前序十二项 P1 均未发现回退。

## 发现项

- P0：0
- P1：0
- P2：0
- P3：0

## 验证证据

独立复跑：

- targeted closeout tests：`39/39 pass`
- `git diff --check origin/main...HEAD`：pass
- canonical/dogfood Python 与 workflow equality：pass
- dogfood overlay drift：pass
- sidecar 扫描：无 `.new` / `.bak`
- Phase 2 三个变更 spec 哈希与当前 HEAD：逐项一致

已审阅 Phase 2 记录的 canonical `373/373`、preset `36/36`、schema/task/static/throwaway证据。真实 Git 测试覆盖多 url/pushurl、insteadOf/pushInsteadOf、边界空白、newline/tab、C0/DEL、NUL截断、rewrite base/pattern，以及 production 首个副作用前阻断。

Production fixture确认 raw remote、local transport和repo mismatch失败时：

- task 保持 active/in_progress
- local HEAD 保持 reviewed HEAD
- remote branch不存在
- dirty/staged path为空
- 无 PR、无 archive、无 finish-summary
- 修正配置后通过同一生产入口完成真实重入

## Docs SSOT 判断

`companion-scripts.md`、`data-contracts.md`、`workflow-contract.md`、canonical/dogfood workflow 与 requirements 已统一表达 raw/effective transport合同；未发现 archive-first、empty-summary或post-tail旧合同回退。Docs SSOT：`pass`。

## Scope、部署与安全

Ledger 分类保持正确：close `[#105]`；related `[#53,#96,#97,#100]`；follow-up `[#98,#99,#101]`。

未变更 CI/CD、容器、K8s/Kustomize、DB migration、Makefile或部署资产。错误路径不泄露 remote URL、credential-bearing stderr、rewrite内容或控制字符原文。部署与安全判断：`pass`。

## 观察项

- 当前分支尚未推送，remote marketplace 与真实 GitHub closeout E2E 仍由 publish-time fail-closed verifier承接。
- 远端仍不存在 `v0.6.5-guru.3` tag，不得声称稳定 tag 安装路径已验证。

## 后续候选

0。

## 结论

Round 4 strict transport finding及Phase 2发现的raw/effective normalization子问题均已闭环，当前 HEAD 未发现新的 P0-P3。本轮仅通过问题闭环审查；仍必须派发未参与本轮实现、Phase 2或closure的新 technical agent执行最终放行审查。
