## 变更摘要

本 PR 解决 issue #65：把 #64 定义的 `Docs SSOT Plan` 纳入 Guru Team workflow 的 Phase 2 implementation/check 合同。

- Phase 2 实现入口现在要求实现代理读取并执行已批准的 `Docs SSOT Plan`，而不是在 Branch Review 或 finish-work 阶段才重新判断 docs 策略。
- 实现 handoff 必须说明 `ssot_first` / `delta_first` / `bootstrap_or_repair_docs` / `no_docs_update_needed` 策略、durable docs 同步结果、task delta 是否 merge、哪些内容只保留为 task history、以及实现输入来自 durable docs 还是确认过的临时 task delta。
- `trellis-check` / channel runtime check 现在必须按 plan strategy 复核 durable docs、task artifacts、code/API/schema/config/deploy/test 和验证覆盖一致性；如果发现长期合同 drift，必须回到 planning artifacts / `Docs SSOT Plan`，必要时重新 planning approval。
- 本 PR 只处理 Phase 2 implementation/check 消费 `Docs SSOT Plan`；Branch Review / finish-work / PR body 的最终 enforcement 仍留给后续 #66。

## 影响范围

- Canonical workflow：`trellis/workflows/guru-team/workflow.md`
- Dogfood workflow：`.trellis/workflow.md`
- Preset overlay：`.agents`、`.codex`、`.cursor`、`.claude`、`.trellis/agents` 的 continue / implement / check 入口
- Durable docs/spec：`docs/requirements/**`、`.trellis/spec/workflow/**`、`.trellis/spec/preset/**`
- Preset/workflow README：`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`

没有修改 Python / shell companion scripts、schema、Trellis upstream、全局 npm、`node_modules`、CI/CD、container、K8s、DB migration、Makefile 或 runtime config。

## 验证结果

- `python3 -m json.tool trellis/index.json`
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：186 tests OK
- `python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：27 tests OK
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-09-065-docs-ssot-phase2-sync-gate`
- `python3 ./.trellis/scripts/get_context.py --mode phase`
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 1.1`
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 2.1`
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5`
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
- `git diff --check`
- `check-review-gate.sh --json --allow-metadata-after-gate`

已覆盖 dogfood apply/drift 验证。未运行完整 throwaway marketplace install 和 `trellis update` replay，因此本 PR 不声称完整开箱即用或 upgrade/update 恢复链路已验证。

## Review Gate

Branch Review Gate 已通过：

- reviewed HEAD：`6c3497204c8ab02453d2383c69fbca04c167e63f`
- diff range：`origin/main...HEAD`
- review source：independent agent
- reviewer：`019f4652-6ce4-7772-8fb7-39feca8796d0`
- findings：0

Review Gate 覆盖 canonical workflow、dogfood workflow、canonical overlays、dogfood installed copies、durable requirements docs、`.trellis/spec`、Phase 2 evidence、部署/安全影响和 issue scope。

## Issue 关闭范围

Closes #65

不关闭后续 #66；#66 继续处理 Branch Review / finish-work / PR body 对 Docs SSOT reconciliation 的最终 enforcement。

## 安全说明

本 PR 只修改 AI workflow / overlay / docs / spec 合同，不引入新的运行时权限、外部服务调用、secret 读取、网络访问或数据处理路径。未发现 token、secret、private key、signed URL、`.env`、数据库 URL 或客户数据泄露。
