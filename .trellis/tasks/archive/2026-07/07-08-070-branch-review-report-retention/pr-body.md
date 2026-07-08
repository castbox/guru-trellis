## 变更摘要

- 为 Guru Team workflow 补齐多轮 Branch Review evidence retention 合同：每一轮独立 review 都保留 task-local raw Markdown 报告，最终 `review.md` 改为人类可读的汇总入口，并链接每轮 raw report。
- 让 `agent-assignment.json.review_rounds[]` 绑定每轮 report 的 path / digest / HEAD / agent 信息，并让 `review-gate.json` 记录最终 rollup 和 raw review reports 的 digest evidence。
- 修正 planning approval 校验的 stale 判定：有效性以用户确认后的 `prd.md` / `design.md` / `implement.md` 内容 digest 为准，HEAD、mtime 或无关 dirty path 变化不会单独使 approval 过期；规划文档内容变化仍会 fail closed，要求重新显式 review 确认。

## 影响范围

- Workflow / prompt / skill：更新 canonical Guru Team workflow、Codex / Claude / Cursor / agent overlays、dogfood installed copies，以及 `trellis-continue` / `trellis-finish-work` 的 review report retention 文案。
- Companion scripts：更新 `guru_team_trellis.py` 和单元测试，支持 raw review report digest 记录、gate 校验、archive metadata tail 迁移，以及 planning approval digest-based freshness。
- 文档与规范：同步 README、workflow README、preset README、`docs/requirements/guru-team-trellis-flow.md`、`docs/requirements/requirement-main.md` 和 `.trellis/spec/**`。
- 部署资产：未修改 GitHub Actions、Docker/Compose、Kubernetes/Kustomize/Helm、DB migration、Makefile 或运行时配置。

## 验证结果

- `check-review-gate.sh --json --allow-metadata-after-gate` 通过，reviewed HEAD 为 `294e79b847869622bab481b4da0030fcacc56197`。
- 最终 review agent 报告 `git diff --check`、`bash -n`、`python3 -m py_compile`、149 个 Python unittest、`json.tool`、`task.py validate`、`get_context` phase reads、dogfood overlay drift check、canonical/dogfood `cmp` 均通过。
- 本轮未重新跑完整 throwaway 新仓库安装，也未跑完整 upgrade/update 开箱验证；风险已记录在 review rollup 中。

## Review Gate

Branch Review Gate 已通过。round 1 发现 1 个 P3 durable docs SSOT finding；同一 technical agent 在 round 2 作为问题闭环审查代理确认修复；round 3 使用 fresh 最终放行审查代理审查 `origin/main...HEAD` 当前完整 diff，0 findings。最终 `review.md` 汇总了三轮 raw reports、finding lifecycle、验证证据、Docs SSOT、安全和部署影响判断。

## Issue 关闭范围

Closes #70

本 PR 不关闭其它 issue；planning approval 校验收紧作为本轮 workflow gate hardening 一并发布。

## 安全说明

本次变更不引入 secret、token、private key、签名 URL、`.env`、database URL 或客户数据。变更集中在 workflow Markdown、preset overlay、companion scripts、测试和文档，不新增网络调用、服务入口、数据库迁移或部署运行面。
