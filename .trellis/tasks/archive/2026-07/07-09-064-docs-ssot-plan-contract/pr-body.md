## 变更摘要

本 PR 为 Guru Team workflow 增加 Phase 1 `Docs SSOT Plan` planning contract，要求每个实现前计划明确当前仓库长期文档状态、同步策略、证据路径和后续合并责任。该合同用于避免 Trellis task artifact 成为长期文档的平行来源。

新增合同包含：

- 文档状态枚举：`complete_docs`、`partial_docs`、`stale_docs`、`no_docs`。
- 同步策略枚举：`ssot_first`、`delta_first`、`bootstrap_or_repair_docs`、`no_docs_update_needed`。
- 必填计划字段：docs state 与 evidence paths、strategy 与 reason、affected durable docs、task artifact deltas、`delta_first` merge checkpoint、`bootstrap_or_repair_docs` repair/follow-up scope、`no_docs_update_needed` concrete reason。
- 推荐 artifact 分工：`design.md` 承载权威计划，`prd.md` 记录文档状态和需求影响，`implement.md` 记录执行 checklist/checkpoint。

Closes #64

## 影响范围

本次变更影响 Guru Team workflow 的 planning/readiness 语义和多平台入口说明：

- canonical workflow：`trellis/workflows/guru-team/workflow.md`。
- dogfood workflow：`.trellis/workflow.md`。
- durable requirements docs：`docs/requirements/guru-team-trellis-flow.md`、`docs/requirements/requirement-main.md`。
- workflow/preset specs：`.trellis/spec/workflow/*`、`.trellis/spec/preset/overlay-guidelines.md`。
- workflow/preset README：`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`。
- canonical overlays 与 dogfood installed copies：Codex、Claude、Cursor、Agents 的 `trellis-continue` 入口。

本 PR 未新增 companion script 或 schema，未修改 Trellis 上游源码、全局 npm 包或 `node_modules`，也未提前实现 #65 / #66 的后续消费和最终阻断语义。

## 验证结果

已执行并通过：

- `python3 -m json.tool trellis/index.json`
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-09-064-docs-ssot-plan-contract`
- `python3 ./.trellis/scripts/get_context.py --mode phase`
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 1.1`
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 2.1`
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5`
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
- `git diff --check`
- `find . -name '*.new' -o -name '*.bak'`
- `.trellis/guru-team/scripts/bash/check-review-gate.sh --json`

未执行完整 throwaway repo 安装验证，也未执行 Trellis `upgrade` / `update` replay。当前证据覆盖 dogfood overlay drift 和现有 worktree 的 workflow/preset 一致性；开箱即用安装链路和升级恢复链路仍需发布前或后续 release gate 继续验证。

## Review Gate

Branch Review Gate 已通过，reviewed HEAD 为 `51045439b5c6fea8aacd61d10446932e9de3c80e`，diff range 为 `origin/main...HEAD`。

最终放行审查代理 `019f4601-5551-7651-a903-6631725f1ab6` 覆盖了 committed diff、任务 planning artifacts、`phase2-check.json`、Issue Scope Ledger、canonical/dogfood workflow、durable docs、spec、README、canonical overlays 和 dogfood installed copies。审查结果为 0 个 P0/P1/P2/P3 finding。

## Issue 关闭范围

关闭：

- #64 Docs SSOT planning contract：Phase 1 必须选择同步策略。

不关闭：

- #65 和 #66。它们是 #64 明确拆出的后续消费/阻断语义，本 PR 没有提前实现。

## 安全说明

本次变更只调整 workflow、文档、spec、overlay 入口和 Trellis task metadata，不新增 secret、credential、private key、`.env`、签名 URL、客户数据或外部服务调用。diff 不改变 CI/CD、容器、Kubernetes/Kustomize、数据库 migration、Makefile、运行时配置或发布脚本行为，因此无部署资产同步需求。
