# Issue #105 Round 26 最终放行审查报告

## 审查身份

- 逻辑角色：最终放行审查代理
- technical agent：`/root/final_release_review_105_round26`
- reuse_decision：`new-agent`
- reviewed_head：`e241db688e03847c0dff028c6fd838b8bfbbafbd`
- findings_count：`1`
- 结论：`fail`

## Finding

### P2：合法 mixed-case GitHub 仓库在 final-summary 与恢复阶段永久阻塞

- repo identity 会统一为小写，PR URL helper 按大小写不敏感接受后保留 GitHub 返回的原始 URL。
- final-summary 与 exact recovery 随后使用小写 plan repo 做大小写敏感 regex 匹配。
- `canonical_pull_request_url("owner/repo", ..., ".../Owner/Repo/...")` 成功；final projection 随后报 repo identity mismatch，exact recovery 报 committed URL non-canonical。
- GitHub API 合法返回 mixed-case `full_name/html_url`，例如 `microsoft/PowerToys`。
- 当前 remote identity 测试要求 `Owner/Repo` 大小写归一化，但 summary/recovery 测试仅覆盖 lowercase URL。

影响：合法 mixed-case repository 的 draft PR 可创建，但 final projection 每次失败，task 无法 archive；既有 exact recovery 也可能无法恢复。该问题 fail closed，因此定为 P2。

修复要求：统一使用一个 PR URL parser；repo identity 比较大小写不敏感，并明确保留 GitHub URL 原始大小写或统一输出 normalized URL；补 mixed-case final projection、incomplete recovery、exact recovery 和 installed closeout 回归。

## 覆盖与证据

只读覆盖 live #105、planning/Phase2/ledger/assignment、Round1-25、16 commits/60 files，以及 transaction、PR identity、summary、archive/recovery、resolver、symlink、hook、跨月、parent-child、history portability、Docs/scope/security/deploy。

- canonical `423/423`
- preset `36/36`
- initial #105/update #106 throwaway closeout 通过
- compile、diff、overlay、canonical/dogfood equality、task/planning/assignment、25 reports、16 commit contract通过
- 无 CI/CD、容器、K8s、Helm、migration、Makefile 或 secret 变化
- scope：close `[105]`、related `[53,96,97,100]`、follow-up `[98,99,101]`

## 未验证边界

current-branch remote marketplace与真实GitHub E2E未验证；`v0.6.5-guru.3`不存在。

## 结论

- P0：`0`
- P1：`0`
- P2：`1`
- P3：`0`
- findings_count：`1`
- reuse_decision：`new-agent`
- 最终结论：`FAIL，Branch Review Gate 阻塞`
