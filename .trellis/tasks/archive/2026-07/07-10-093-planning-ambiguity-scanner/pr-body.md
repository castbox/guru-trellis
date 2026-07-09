## 变更摘要

- 将 planning artifact 弱约束词检查升级为 v2 受控词表，覆盖 `可以`、`允许`、`建议`、`推荐`、`可选`、`尽量`、`应该`、`默认` 等 35 个触发词。
- 将扫描范围固定为 `prd.md`、`design.md`、`implement.md`，并在 `planning-approval.json` 中记录 `controlled_terms`、`scan_scope`、`hits[]` 和 `unchecked_normative_hits[]`。
- 新增 `--normative-hit "path|line|term|classification|reason"` 记录入口，要求每个命中都有分类和理由；未分类命中或 `contract_violation` 会失败并阻塞。
- 强化 `check-planning-approval`：重新扫描当前 planning artifacts，并与 artifact 中记录的扫描结果对比，防止 approval evidence 与当前文档漂移。

## 影响范围

- 影响 Guru Team workflow 的 planning approval gate、Branch Review / Phase 2 相关说明、preset overlay、平台入口文案、canonical helper 与 dogfood helper。
- 同步更新 durable docs/spec：`docs/requirements/*`、`.trellis/spec/workflow/*`、`.trellis/spec/preset/overlay-guidelines.md`、`trellis/workflows/guru-team/workflow.md`、`.trellis/workflow.md`、preset README 与各平台 overlay。
- 不改变 Trellis 上游源码、全局 npm 包、`node_modules`、hook 旁路逻辑或业务仓库私有规则。

## 验证结果

- `check-planning-approval.sh --json --task .trellis/tasks/07-10-093-planning-ambiguity-scanner` 通过；新版 scanner 记录 65 条 hits，`unchecked_normative_hits[]` 为空。
- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` 通过，209 tests OK。
- `python3 -m py_compile` 覆盖 canonical helper、dogfood helper、测试和 preset installer，结果通过。
- `bash -n` 覆盖 workflow / dogfood / preset bash wrappers，结果通过。
- `python3 -m json.tool` 覆盖 `trellis/index.json`、intake-handoff schema 和 planning approval artifact，结果通过。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-10-093-planning-ambiguity-scanner` 通过。
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 1.4` 和 `--step 1.5` 通过。
- `git diff --check` 通过。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh` 通过。

## Review Gate

- Phase 2 检查代理 `019f4885-521a-7090-86fe-a7bef2141553` 完成 PASS，覆盖 requirements、design、code、tests、spec_sync、cross_layer、docs_ssot、deployment，无 findings。
- 最终放行审查代理 `019f488e-0591-70a3-9257-9d08bd1cb33c` 审查 `origin/main...HEAD` 到 `a70374094f869637561cdc677efbff8af3c1368f`，结论 pass，无 findings。
- Branch Review Gate 已记录 `review.md` 和 raw review report digest，`check-review-gate.sh --json --allow-metadata-after-gate` 通过。

## 文档同步

- strategy：Docs SSOT strategy 为 `ssot_first`。
- durable docs updated：本次已把 task delta 合并回 durable docs/spec/workflow/overlay：受控词表、固定扫描范围、命中记录字段、未分类与 `contract_violation` 阻塞、以及 #83 的 AI 语义审查边界均已同步。
- task history only：保留为 task history 的内容包括本轮 `planning-approval.json` 具体 65 条命中、Phase 2 check 证据、Branch Review raw report、review gate 证据和 sub-agent liveness 记录。
- followup_or_limitation：未执行完整 throwaway repo install，也未执行完整官方 `trellis update` / `upgrade` 后端到端验证；本 PR 不声称完整开箱即用验证，仅记录已完成 dogfood apply、overlay drift、canonical/dogfood helper 与 workflow 一致性验证。

## Issue 关闭范围

Closes #93

本 PR 只关闭 #93；没有 related issues 或 followup issues 被纳入关闭范围。

## 安全说明

- 未触及 `.env`、secret、token/private key、签名 URL、数据库 URL 或客户数据。
- 未改变 DB migration、container/K8s、CI/CD、Makefile 或部署资产。
- 本次变更只影响 Guru Team workflow / preset / overlay / helper / docs / test 语义，不需要生产部署或运行时配置变更。
