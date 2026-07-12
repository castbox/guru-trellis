# Issue #105 Branch Review Round 24 最终放行审查报告

## 审查身份

- 逻辑角色：最终放行审查代理
- technical agent：`/root/final_release_review_105_round24`
- reuse_decision：`new-agent`
- reviewed_head：`6b1932e716fc86d16e3a687a1dc42e49cdede78a`
- base：`3dec302206783fe4ac1296066e9a1789c995d58b`
- findings_count：`2`
- 结论：`fail`

本轮严格只读，未修改文件，未运行 recorder/gate，未 commit、push、创建 PR 或关闭 issue。

## 审查范围

独立读取 live Issue #105、规划/approval/Phase 2/ledger/assignment、Round 1-23 raw reports、15 个提交与 60 文件完整 diff，并覆盖 prepare、remote identity、draft PR、final summary、archive transaction、exact/incomplete recovery、resolver/path safety、hook、跨月、parent-child、history portability、install/update、scope、安全及部署影响。

## 最终审查

### P1-1：fresh archived recovery 会改绑新 PR，导致 committed summary 指向旧 PR

- `resume_archived_closeout()` 查询当前唯一 open PR，并把该候选作为 `bound_pr` 传给 ready。
- immutable plan 只保存 repo/head/base/title/body digest，没有 draft PR number/URL。
- fresh archive resolver 不从 archive commit 中提取 summary 的 canonical PR number/URL。
- probe 构造 committed summary 指向 PR #105、远端唯一候选为 PR #106；恢复成功把 #106 转 ready，而 summary 仍指向 #105。

影响：`finish-summary.json.github.pr_url` 与 `index.search_terms.pr_refs` 可指向错误 PR，破坏稳定 PR identity 和精确历史索引。

修复要求：fresh recovery 必须从不可变 Git 事实恢复已绑定 PR number/URL；原 PR 缺失或关闭时 fail closed，并增加 #105 被关闭、同身份 #106 出现的负向 production test。

### P1-2：incomplete recovery 未绑定 final summary bytes，可提交篡改历史索引

- `finish-summary.json` 属于 `untracked_archive_outputs`，不在 `tracked_move_paths`。
- pre-move 对 untracked final output 只验证 regular file 与路径集合，未冻结真实 PR 注入后的 bytes/digest。
- post-move layout 只比文件名，blob continuity 只遍历 tracked paths。
- incomplete recovery 在 dirty path set 正确且 index 为空时重新 `git add` 全部 archive path并提交。
- probe 模拟 official move 后、首次 `git add` 前中断，仅篡改 summary；恢复成功 commit/push/ready，篡改 summary 被纳入 archive commit。

影响：错误 PR URL/ref 或损坏检索数据可被提交发布，违反 final projection 不可变性与 exact commit 前 tamper fail-closed 合同。

修复要求：真实 PR identity 注入后冻结 final summary deterministic bytes/digest，并纳入 incomplete/exact continuity；恢复 commit 前验证 summary 是 plan template 加 bound PR runtime facts 的唯一结果，不重跑通用本地 validator。

## 问题生命周期

Round 1-23 既有 closure 未发现回退。本轮两项属于 #105 的 PR identity、final summary 与 archive recovery 核心合同；Round 24 成为 finding owner，后续只能 closure。

## 通过证据

- canonical `420/420`、preset `36/36`
- public marketplace sample + local preset initial #105/update #106 installed closeout 通过
- overlay drift、canonical/dogfood Python/workflow/schema equality、compile/Bash/diff 通过
- manifest 71 assets、backup/new/sidecar 为空
- 23 份 raw report digest/size 与 assignment 一致
- 15 个 commit body 合同通过

这些绿灯未覆盖 PR replacement 和 summary-only tamper 场景。

## Docs SSOT

`fail`。workflow 的 fresh archived reentry 接受唯一 matching candidate，与 canonical summary PR identity 冲突；文档声明 exact commit 前 tampered state fail closed，但实现未覆盖 untracked final summary。

## Scope、安全与部署

- close：`[105]`
- related：`[53,96,97,100]`
- follow-up：`[98,99,101]`

两项 finding 均属 #105 核心合同，没有扩展 hook、跨月迁移、时间框架或 resolver。未发现 secret；未修改 CI/CD、容器、K8s、Helm、migration 或 Makefile。

## 未验证边界

- current-branch remote marketplace 与真实 GitHub E2E 未验证。
- `v0.6.5-guru.3` 不存在，不得声明 stable-tag 验证完成。

## 结论

- P0：`0`
- P1：`2`
- P2：`0`
- P3：`0`
- findings_count：`2`
- reuse_decision：`new-agent`
- 最终结论：`FAIL，Branch Review Gate 阻塞`
