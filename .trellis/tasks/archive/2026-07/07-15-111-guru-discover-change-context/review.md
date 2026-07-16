# Issue #111 Branch Review 汇总

## 审查范围

- Repository：`castbox/guru-trellis`
- Base：`origin/main@3395fad2a4049a33c4c679cd05452cfa45a85b92`
- 最终 Reviewed HEAD：`dc3e2e9a32b7b8db1dc7e5645f8599ddfa2700b7`
- 完整 diff：`origin/main...dc3e2e9`，114 files，24302 insertions，158 deletions
- Live scope authority：GitHub issue `#111`，含 2026-07-16 场景范围控制
- Docs SSOT strategy：`ssot_first`

本汇总覆盖 approved planning、planning approval、implementation handoff、Phase 2、精确 task
commit、Docs SSOT、canonical package/schema/runtime/workflow、tests、preset/installer、
ownership、dogfood、多平台分发、upgrade/update、open-box throwaway、部署影响及 issue scope。

## 审查轮次

| 轮次 | 逻辑角色 | 技术身份 | Reviewed HEAD | Findings | 决策 | 原始报告 |
| --- | --- | --- | --- | ---: | --- | --- |
| 001 | 问题发现审查代理 | `/root/issue111_branch_review` | `94d6126d75d7419e79a142f45d92b07dc8922241` | 2 | `not-applicable` | [001-findings-review.md](reviews/001-findings-review.md) |
| 002 | 问题闭环审查代理 | `/root/issue111_branch_review` | `dc3e2e9a32b7b8db1dc7e5645f8599ddfa2700b7` | 0 | `reuse-for-closure` | [002-closure-review.md](reviews/002-closure-review.md) |
| 003 | 最终放行审查代理 | `/root/issue111_final_release_review` | `dc3e2e9a32b7b8db1dc7e5645f8599ddfa2700b7` | 0 | `new-agent` | [003-final-review.md](reviews/003-final-review.md) |

Round 003 的 technical identity 未出现在 earlier review round，且既不是 finding owner，也不是
closure agent，满足最终审查 freshness 要求。

## 问题生命周期

| ID | Round 001 | 最新范围定性 | Round 002 闭环 | 最终状态 |
| --- | --- | --- | --- | --- |
| BR-001 | P1：duplicate facts/provenance 校验不足 | 只保留同一次 open duplicate search 字段投影、identity、canonical URL、open state、updated time 和 `facts_sha256` 重算；post-review reread、forged、closed-after-review、hostile-input 要求撤销 | Schema/runtime/test 已覆盖 deterministic projection 和 digest；未加入第二次 search/reread | closed |
| BR-002 | P2：`typed_exit=blocked` 与 Gate 可不一致 | 保留为普通状态机 correctness | Schema/runtime 双向强制 blocked exit 当且仅当 Gate blocked；正反向测试通过 | closed |

2026-07-16 的 live #111 明确排除 forged/tamper、攻击者或威胁模型、symlink/FIFO hostile
matrix、credential/signed URL 扫描、并发锁、fault injection、跨 OS 原子性等非常规加固。
Round 001 与旧 task metadata 中相关叙事仅作为历史审计记录保留，不再是当前 acceptance、finding
或 implementation 输入。

## 最终审查

最终放行审查代理对 `origin/main...dc3e2e9` 完整 diff 做了 fresh independent semantic
review，确认：

- live #111 当前 scope 与新版 `prd.md`、`design.md`、`implement.md`、
  `planning-approval.json` 一致；
- `ssot_first` Docs SSOT 已合并回 requirements、workflow/preset specs、README、package
  contract、schema、runtime 和 tests；
- `guru-discover-change-context` 保持 semantic profile、current-state-before-history、稳定
  query/digest/scoring、invalid isolation、zero candidate、task-local persistence 和三个唯一
  typed exit consumer；
- duplicate gate 只重算同一次搜索字段，blocked exit/Gate 双向一致；脚本未取代 AI 的
  relevance、sufficiency、finding 和 route 判断；
- `task-commit-plans/002.json` 与提交 `dc3e2e9` 的 59 个 stage paths、父提交和 tree
  `601b5e2c80a8ca3800e06eb31a60229afb4bb793` 精确一致，`hook_mutation=false`；
- Round 001 的两项 finding 已由同一 owner 在 Round 002 关闭，Round 003 使用 fresh final
  reviewer；
- 当前 P0/P1/P2/P3 均为 0。

## 证据

- Fresh targeted change-context suite：29 passed。
- Fresh full related suite：589 passed in 178.067s。
- Source Skill validator：3 active skills、3 invoke markers、9 exits、6 targets，passed。
- Installed Skill validator：128 managed files，0 sidecar/removal/conflict，passed。
- Canonical、installed、Agents、Codex、Cursor、Claude package SHA-256 一致。
- Canonical/dogfood workflow、runtime、wrappers 字节与 executable mode 一致。
- Upstream ownership：43 active、0 removed、13 managed claims，passed。
- Dogfood overlay drift、`python3 -m py_compile`、`bash -n`、`git diff --check`：passed。
- Phase 2 clean throwaway：`exit=0`，覆盖 init、workflow preview/switch、preset apply、direct
  discovery、candidate/zero-candidate、task-local record/check、`trellis update --force`、
  reapply 和 zero sidecar。
- 无 `.new`、`.bak`，source checkout clean，task worktree 无 non-metadata post-commit drift。

## 部署与安全

- 本次修改影响公共 workflow marketplace、preset、schema、runtime 与多平台安装面。
- 无 `.github/workflows`、Docker、Compose、K8s/Kustomize、Helm、DB migration、SQL、
  Makefile 或业务配置变更。
- 未发现 secret、private key、token、客户数据或本机绝对路径进入公共 package/example。
- 安全判断严格限定于 live #111；排除的攻击/威胁场景未被重新作为阻断项。

## 观察项

- 当前 dirty 内容仅为 task-local Branch Review / task commit metadata；没有实现资产脏改动。
- Exact current feature-ref marketplace 因分支尚未 push，当前未验证。

## 后续候选

无新增 follow-up issue。`issue-scope-ledger.json` 保持：

- `close_issues`：仅 `#111`
- `related_issues`：`#53/#96/#97/#98/#100/#101/#105/#109/#110/#112/#113`
- `followup_issues`：空

Publish 阶段必须在 push 后运行 exact feature-ref marketplace remote verifier；在该验证完成前，
PR readiness 不得声称当前分支远端安装已验证。

## 结论

- 最终 findings：P0=0、P1=0、P2=0、P3=0。
- Final reviewer：`/root/issue111_final_release_review`。
- Reviewed HEAD：`dc3e2e9a32b7b8db1dc7e5645f8599ddfa2700b7`。
- 结论：Branch Review semantic review 通过，可由主会话运行 Branch Review Gate recorder。
- 本结论不授权 push、创建 PR、归档或关闭 issue。
