## 变更摘要

- 将 Guru Team 收尾流程重构为由 `trellis-finish-work` 唯一编排的事务状态机：共享 dry-run/formal prepare、推送 reviewed content、远端 marketplace 验证、绑定唯一 draft PR、生成最终归档投影、执行官方 archive transaction、校验 local/remote/PR HEAD 后转 ready。
- 新增 immutable `closeout-plan.json` 与 `closeout_plan_digest` 握手，正式执行在首个副作用前校验 dry-run 计划未漂移；同一入口可从 active 或 archived 状态恢复中断。
- 把所有可预见的本地 artifact、schema、路径、ledger、PR body/readiness、hook 和 archive destination 校验前移到 archive 之前；archive 后只保留远端身份、HEAD 与 ready transition。
- 将 `publish-pr.sh` 收敛为兼容性 fail-closed 入口，删除旧 publish/recovery/summary-tail executor、无生产调用 helper、43 个 dormant 自证测试和 3 个无读取者配置。
- 保留 75 项 closeout failure matrix 与 605 行 installed closeout smoke；相对 `origin/main` 新增的 88 个 production top-level function 全部可从 `main()` 到达。

## 影响范围

- Canonical workflow：更新 `trellis/workflows/guru-team/workflow.md`、finish/continue 平台入口、closeout schema、companion Python 与回归测试。
- Guru Team preset 与 overlay：同步 Claude、Codex、Cursor 入口、installer、manifest、配置模板和 installed smoke；canonical/dogfood 保持一致且 overlay drift 为零。
- Durable docs：更新 README、requirements 以及 workflow/data/companion/preset/quality contracts，统一唯一 executor、PR body SSOT、恢复边界和发布顺序。
- Compatibility：`publish-pr.sh` 路径继续存在，但固定拒绝并指向 `trellis-finish-work`；不再提供第二套 publish 或 recovery 实现。
- 最终 `trellis/**` diff 为 24 files、`+10227/-4990`；减法提交自身在 `trellis/**` 中 `+101/-2862`，净删除 2761 行。

## 验证结果

- Deterministic 文档合同：3/3 通过。
- Closeout failure matrix：75/75 通过。
- Canonical tests：384/384 通过；direct tests：232/232 通过；preset tests：36/36 通过。
- Conventional commit messages：20/20 通过。
- Python compile、Bash syntax、JSON/JSONL、Draft 2020-12 schema、`git diff --check`、canonical/dogfood equality、overlay drift 与 sidecar 扫描通过。
- Installed initial #105 与 update/reapply #106 证据保持 fresh：后续提交未修改 runtime、installer、canonical workflow、overlay 或 605 行 smoke driver。
- 当前远端分支 marketplace verification 将在 finish-work 推送 reviewed content 后、创建 draft PR 前执行；固定 release tag `v0.6.5-guru.3` 不存在，本 PR 不声明 stable-tag 验证。

## Review Gate

- Branch Review Gate 已在 HEAD `3ca1847d70809a7530f59d1cb555388f70f65d47` 通过。
- Round 34 使用 fresh technical identity `/root/final_release_review_105_round34` 审查完整 `origin/main...HEAD`：20 commits、62 files，P0/P1/P2/P3 为 `0/0/0/0`。
- Round 30-33 已关闭 Docs SSOT、deterministic 文本合同与 Phase 2 lineage finding chain；最终 gate 绑定 34 轮 raw report digest、assignment digest 与当前 HEAD。
- 审查覆盖需求、设计、代码、测试、task artifacts、Docs SSOT、安装升级、远端身份、路径边界、安全与部署影响。

## Docs SSOT

- 状态与策略：`complete_docs / ssot_first`。
- Durable docs 已更新：`README.md`、`docs/requirements/`、`.trellis/spec/workflow/`、`.trellis/spec/preset/`、canonical workflow/README、preset README 与各平台入口。
- 已合并 task delta：唯一 publish/recovery executor、immutable closeout plan、draft PR identity、archive 前完整验证、archive 后恢复限制、task-local `pr-body.md` 唯一正文来源和 compatibility blocker。
- 仅保留为 task history：failure injection 明细、installed smoke 运行证据、Phase 2/Branch Review 轮次与 finding 生命周期。
- 后续限制：#98、#99、#101 保持独立交付；本 PR 不扩展通用 resolver、通用 symlink 框架、索引格式、schema 或时间框架。

## Issue 关闭范围

Closes #105

### 仅引用或相关

- Refs #53
- Refs #96
- Refs #97
- Refs #100

### 后续范围

- Follow-up #98
- Follow-up #99
- Follow-up #101

## 安全说明

- Closeout plan、readiness、summary 和错误 payload 不记录 token、secret、private key、签名 URL、`.env`、数据库 URL、客户数据或本机绝对 worktree 路径。
- Remote identity 对 raw/effective Git URL、rewrite、repo/head/base 与同名 fork 执行 fail-closed 校验，只接受无凭据的 GitHub HTTPS/SSH/scp transport。
- Task、PR body 和 archive locator 使用逐组件路径校验，拒绝 repo 内外、relative/absolute、ancestor/final、multi-level、dangling 与 loop symlink alias。
- 本次不修改 CI/CD、Docker/Compose、Kubernetes/Kustomize、Helm、database migration 或 Makefile，无部署拓扑、数据库迁移和运行时配置迁移影响。
