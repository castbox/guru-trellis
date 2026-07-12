# Issue #105 Branch Review Round 10 问题闭环报告

## 审查身份

- 逻辑角色：问题闭环审查代理
- technical agent：`/root/final_release_review_105_round9`
- 复用依据：Round 9 finding owner，仅允许 closure，不得最终放行
- reviewed_head：`6b8e1938cc547a0279141566696304f776c60f1d`
- diff_range：`origin/main...HEAD`
- reuse_decision：`reuse-for-closure`
- findings_count：`1`
- 结论：`fail`

## 审查范围

只读复核了 Round 9 唯一 P1、`4f634a7..6b8e193` 的 13 个非 metadata 文件、active/post-archive validator 分层、remote-only PR identity、archive path/blob/task.json/commit lineage、ready 恢复、新增测试、durable Docs SSOT、canonical/dogfood、Phase 2、ledger、部署与安全影响。

## 问题生命周期

### Round 9 P1：official archive 后仍依赖本地 artifact validator

状态：`open，主体已修复但闭环不完整`

已确认关闭的部分：

- body、summary、ledger、readiness、marketplace 内容 validator 已从 post-archive ready 路径移除。
- active final projection 仍完整执行 summary schema/template、ledger、marketplace artifact 与 PR body 逐字校验。
- post-archive remote identity 直接校验 repo/head/base/title、remote body UTF-8 digest、draft/state 和 HEAD。
- normal invocation 通过 `bound_pr` 保留 number/URL；fresh archived reentry 只接受唯一匹配的 repo/head/base/title/body-digest 候选。
- fork、multiple、missing、title/body/repo/head/base mismatch 均保持 fail closed。
- archive move path set、tracked blob continuity、官方 `task.json.status/completedAt`、evidence/archive parent、staged/commit paths、push 和三方 HEAD 门禁未削弱。

仍未关闭的缺口：

- `resume_archived_closeout()` 在 `guru_team_trellis.py:12235` 无条件调用 `resume_archive_metadata_transaction()`。
- 该函数在 `12165` 首先调用 `validate_closeout_archive_move_layout()`，并在 `11994-12000` 枚举 archived working-tree 文件，要求完整等于 plan `move_paths`。
- archived artifact 内容被修改时，`git_status_paths()` 会产生 partial dirty set，并在 `12168` 被要求等于完整 archive transaction path set，同样在 remote HEAD/ready 前失败。
- 因此 exact archive commit 已存在甚至已 push 后，本地 archived 文件缺失或内容异常仍会阻断 draft-to-ready；恢复并非仅依赖 immutable plan、commit/remote facts。

测试没有覆盖生产路径：

- `test_archived_draft_reentry_uses_plan_remote_identity_and_ready_only` 在 `10551-10556` 删除除 plan 外的所有 archived artifacts。
- 但测试在 `10611-10616` mock 掉 `resume_archive_metadata_transaction()`，正好绕过真实代码中会因缺文件失败的 layout/dirty 检查。
- `test_post_archive_layout_and_ready_do_not_run_local_artifact_validators` 只分别调用 layout 和 ready；它没有通过真实 `resume_archived_closeout()` 验证 invalid archived content 的恢复。

这仍是 Round 9 同一 P1，而非新的范围。

## 验证证据

独立复跑：

- canonical tests：`386/386 pass`
- targeted closeout：`52/52 pass`
- preset tests：`36/36 pass`
- overlay drift：pass
- canonical/dogfood Python 与 workflow equality：pass
- `git diff --check origin/main...HEAD` 与 metadata dirty diff：pass
- Phase 2 的 13 个 `dirty_paths` 与 `4f634a7..6b8e193` 非 metadata 路径精确相同
- Phase 2 记录 20 项 P1 为 resolved，但最后一项的 missing/invalid production recovery 证据不足，本轮 closure 不接受其 resolved 结论

## Ledger 与前序合同

- primary 与 close acceptance evidence 逐字一致。
- `386/386`、`52/52`、`36/36`、71 assets、initial #105、after-update #106 各唯一出现。
- scope 保持 close `[105]`、related `[53,96,97,100]`、follow-up `[98,99,101]`。
- Round 1-8 已关闭的 plan、remote transport、head repository、raw body、all-platform provenance、installed smoke 和 ledger findings 未发现回退。

## Docs SSOT

durable specs、workflow 与 README 已统一声明：

- official move 后不再打开 archived body、summary、readiness、ledger 或 verifier；
- exact archive commit 后只使用 plan、Git/remote/PR facts恢复；
- ready 阶段为 remote-only。

但真实 archived reentry 仍依赖 archived working-tree 完整文件集和 dirty content，因此实现与 Docs SSOT 尚不一致。Docs SSOT closure：`fail`。

## 部署与安全

本轮未修改 CI/CD、容器、Docker Compose、Kubernetes/Kustomize、migration 或 Makefile。未发现真实 secret、token、私钥、`.env`、客户数据或签名 URL。部署与安全无新增 finding。

## 观察与后续

- 当前仅 task ledger、Phase 2、assignment 和 reviews metadata tail 未提交。
- dogfood 保持 `claude/codex/cursor`、`all_platforms=true`、71 assets，无 `.new/.bak`。
- current-branch remote marketplace 与真实 GitHub E2E 仍属于 publish-time verifier。
- 远端仍不存在 `v0.6.5-guru.3`。
- follow-up candidate：0。

## 结论

Round 10 问题闭环失败，`findings_count: 1`，`reuse_decision: reuse-for-closure`。必须让“archive commit 已存在”恢复分支先从 Git commit/remote facts识别完成状态，并跳过 archived working-tree layout/dirty artifact 检查；同时用不 mock `resume_archive_metadata_transaction()` 的 missing/invalid artifact 生产恢复测试证明 draft-to-ready 可继续。
