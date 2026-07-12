# Issue #105 Branch Review Round 4 闭环报告

## 审查身份

- 逻辑角色：问题闭环审查代理
- technical agent：`/root/final_release_review_105`
- 复用依据：Round 3 finding owner，仅允许 closure，不得最终放行
- reviewed HEAD：`dbe3d4c496c28aea2b77f4e6d8bb510eac02e592`
- diff range：`origin/main...HEAD`
- Round 3 报告：`.trellis/tasks/07-11-105-finish-work-closeout-transaction/reviews/round-03-final-release-finding.md`
- findings_count：`1`
- 结论：`fail`

## 审查范围

复查了 Round 3 head repository P1、Phase 2 后续 effective remote URL P1、`fda16dd..dbe3d4c` 九文件修复、最新 Phase 2 artifact、ledger、assignment chain、canonical/dogfood Python、durable specs、requirements、workflow 和新增测试。

`phase2-check.json.head=fda16dd` 是修复提交前快照；其 9 个 `dirty_paths` 与 `fda16dd..dbe3d4c` 的 9 个非 metadata 文件精确相等，三个变更 spec 哈希与当前 HEAD 一致。当前仅剩允许的 task metadata tail。

## 问题生命周期

### Round 3 P1：head repository identity

状态：`partially-closed`

已确认闭环部分：

- PR query 已读取 `headRepository`、`headRepositoryOwner`、`isCrossRepository`。
- `headRepository.nameWithOwner` 与 owner 字段一致性、cross-repository 状态和 `plan.git.repo` 在 query、reuse/create、final projection、active/archive recovery、ready confirmation 全链校验。
- 同名 fork、字段缺失、target+fork 混合候选均在 summary/archive 前 fail closed。
- production fixture 验证 fork candidate 失败时 task 保持 active、无 summary/archive/错误 PR 绑定，解除注入后从生产入口成功重入。

未闭环部分见 P1-1。

### 前序问题

Round 1 四项 P1、实现阶段四项 P1以及 raw UTF-8 body、archive blob continuity、旧合同负向扫描、14 阶段真实 Git 状态/重入均未发现回退。

## 发现项

### P1-1：effective remote URL validator 仍接受本地相对路径，非法 URL 可绕过 repo identity

证据：

- `guru_team_trellis.py:2172` 的 `normalize_github_repository()` 同时用于 plan 的 `owner/repo` 标识和 Git effective remote URL。
- 该函数末尾的通配模式 `r"(.+)"` 会把裸值 `owner/repo` 或 `Owner/Repo.git` 规范化为合法的 `owner/repo`。
- `validate_github_remote_repository():2206` 对 `git remote get-url --all/--push --all` 的每一行直接调用同一函数，因此上述本地相对路径会通过。
- 独立只读调用已确认：当 fetch/push effective output 均为 `owner/repo` 时，validator 返回 `owner/repo`，没有 fail closed。
- Git 会把裸 `owner/repo` 当作相对文件系统路径，不是 GitHub remote URL。新增测试覆盖多 URL、rewrite、example.com、空集和命令失败，但未覆盖这个非法形式。

影响：

dry-run 会错误通过 repo identity gate；formal 的首次 `git push` 可把 reviewed branch 推送到本机或挂载目录，而非 immutable GitHub repo。随后流程可能在 verifier/PR 阶段失败，但错误副作用和潜在代码泄露已经发生，违反“首个副作用前校验全部 effective remote URL”和 #105 的 archive/publish 事务边界。

建议：

拆分 repo identifier normalizer 与 remote URL parser。plan 字段可接受 `owner/repo`；effective remote 只能接受明确的 GitHub transport，例如 `https://github.com/...`、`ssh://...github.com/...`、`git@github.com:...`。裸 `owner/repo`、`Owner/Repo.git`、无 scheme 的路径必须拒绝。补真实 Git remote 相对路径及 production 无 push/PR/archive/summary重入测试。

## Docs SSOT 判断

Docs 已加入 head repository 和全部 effective fetch/push URL 合同，旧 archive-first 合同未回退。但文档声明“全部有效 URL 必须绑定 GitHub repo”，当前实现仍把非法本地路径识别为有效，因此 Docs SSOT 与代码承接结论为 `fail`。

## Scope、部署与安全

Ledger 分类保持正确：close `[#105]`；related `[#53,#96,#97,#100]`；follow-up `[#98,#99,#101]`。本 finding 属于 #105 当前范围，不能转为 follow-up。

未发现 CI/CD、容器、K8s/Kustomize、DB migration、Makefile 或部署资产变化。现有错误路径不回显 effective URL/stderr 的脱敏实现有效，但错误 remote 可接收 reviewed source，本身构成发布安全风险。

## 验证证据

已审核 Phase 2 记录的 `371/371` canonical、`36/36` preset、`37/37` targeted、静态/schema/task/equality/drift/throwaway结果；`git diff --check` 通过。本轮通过直接函数证据确认裸相对 remote 绕过，不需要依赖测试推断。

## 观察项

- 当前分支尚未推送，remote marketplace 和真实 GitHub closeout E2E 仍未执行。
- 远端仍无 `v0.6.5-guru.3` tag，不能声称稳定 tag 路径已验证。

## 后续候选

0。本 P1 必须在当前 issue 内闭环。

## 结论

Round 4 问题闭环不通过。Round 3 的 PR head repository 绑定主体已修复，但 effective remote URL 的非法相对路径绕过使同一 repo identity P1 仍保持 open。修复并重新通过 Phase 2 和本 finding owner closure 后，仍需派发新的最终放行审查代理。
