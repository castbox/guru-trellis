# #20 实施计划

## 执行清单

- [x] 读取 issue #20、官方 Trellis custom workflow / spec marketplace 文档、仓库 workflow/preset spec。
- [x] 创建新 worktree、分支和 Trellis task，关闭范围仅绑定 #20。
- [x] 修改 companion script，使 passed gate 强制 `--review-report` 并校验 digest 四字段。
- [x] 补充 focused unit tests 覆盖 review report 必填、旧 gate 拒绝、metadata-only tail 规则。
- [x] 更新 canonical workflow、dogfood workflow、platform overlays、README、spec，使 continue/finish-work 边界一致。
- [x] 运行 preset apply，同步 dogfood 安装副本，并检查 overlay drift。
- [x] 运行脚本、JSON、phase context、throwaway install、task validate、diff check 等验证。
- [ ] 提交 task work 和规划 artifact。
- [ ] 在 `trellis-continue` 阶段写 `review.md` 并记录 `review-gate.json`，不提交 metadata、不 push、不创建 PR。

## 验证计划

- `python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- `python3 -m json.tool trellis/index.json`
- `python3 -m json.tool trellis/workflows/guru-team/schemas/intake-handoff.schema.json`
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py .trellis/guru-team/scripts/python/guru_team_trellis.py`
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5`
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.6`
- `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-04-20-review-gate-report-metadata`
- `git diff --check`

## Docs SSOT Reconciliation

- 本任务改变长期 workflow/preset 行为，必须更新 README、workflow README、preset README、workflow spec、preset overlay spec、canonical workflow 与 dogfood workflow。
- `prd.md`、`design.md`、`implement.md` 只作为 task 历史证据；长期规则必须落回上述 durable docs/source。
