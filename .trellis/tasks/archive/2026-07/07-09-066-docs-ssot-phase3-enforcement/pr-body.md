## 变更摘要

- 收紧 Guru Team Phase 3 / Branch Review / finish-work 对 Docs SSOT 的放行语义：final reviewer 只验证 Phase 2 reconciliation，不首次执行 docs merge 或补救遗漏。
- 将 current-scope Docs SSOT inconsistency 明确为 blocking finding，并保持 review gate 后只允许 Trellis metadata tail 的规则。
- 增加 PR body `Docs SSOT` / `文档同步` 客观结构校验和回归测试，避免 validator 替代 AI 语义审查。

## 影响范围

- `trellis/workflows/guru-team/workflow.md` 与 dogfood `.trellis/workflow.md`
- Guru Team continue / finish-work / check overlays，以及 Codex / Claude / Cursor / shared skills 的 installed copies
- `guru_team_trellis.py` PR body quality validator 与单元测试
- README、requirements docs、workflow/preset specs 和 preset README

## Docs SSOT

- 策略：本任务使用 `ssot_first`，先更新 durable docs / spec / workflow，再由实现、测试和 gate 文案承接。
- Durable docs / 长期文档：已更新 canonical workflow、dogfood workflow、requirements docs、README、workflow/preset specs、platform overlays 和 installed copies。
- Task delta / 任务增量：`prd.md`、`design.md`、`implement.md`、`phase2-check.json` 中的当前范围 Docs SSOT 差异已同步 / 回写 / 合并到 durable docs 与 workflow/preset artifacts。
- Task history / 任务历史：planning、implementation、check、review 过程记录仅保留为 task-history-only 证据，不作为 publish 阶段首次 docs merge 的来源。
- Follow-up / 限制：未执行完整 throwaway public remote marketplace install，也未执行 `trellis update` 兼容 replay；本 PR 仅声明本地 canonical / dogfood / overlay / validator 范围的一致性。

## 验证结果

- `python3 -m json.tool trellis/index.json` 通过。
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh` 通过。
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py` 通过。
- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` 通过，189 tests OK。
- `python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py` 通过，27 tests OK。
- `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms --json` 通过，无 `.new` / `.bak`。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh` 通过。
- `git diff --check` 通过。

## Review Gate

- Branch Review Gate 已通过。
- Review source：independent-agent，reviewer `trellis-check:019f469c-8f0e-7a82-8bb0-8ca881d37694`。
- Reviewed HEAD：`8cd0b774b788fb965fd07e4843107e6eccc59d7c`。
- 审查范围：`origin/main...HEAD` 完整分支 diff，findings_count=0，blocking_findings_count=0。

## Issue 关闭范围

- Closes #66
- Refs #1

## 安全说明

- 未涉及 token、secret、private key、签名 URL、客户数据或 `.env`。
- 未修改 runtime config、部署资产、CI/CD workflow、Docker / Compose / K8s、数据库 migration 或 Makefile。
