## 变更摘要

本 PR 为 Guru Team workflow 增加 planning artifact ambiguity review gate，解决 `prd.md`、`design.md`、`implement.md` 在进入实现前可能承载无约束模糊表达的问题。

核心行为变更：

- Phase 1 planning 在展示三份 planning docs 给用户确认前，必须先完成 AI ambiguity review。
- 规范性条款不得无条件使用 `可以`、`允许`、`建议`、`尽量`、`视情况`、`类似`、`相关`、`等` 作为执行合同。
- 外部引用、历史记录或风险说明中的弱约束词必须标注来源，并且不得直接作为 task 执行合同。
- `planning-approval.json` 升级为 `schema_version=1.2`，新增结构化 `ambiguity_review` evidence。
- companion script 只校验客观结构、受控词表、checked dimensions、artifact digest 和 freshness，不替代 AI 语义审查。

## 影响范围

- `trellis/workflows/guru-team/workflow.md` 与 dogfood `.trellis/workflow.md`
- Guru Team preset overlay 中 Codex / Claude / Cursor / `.agents` / `.trellis/agents` 入口
- `.trellis/guru-team/scripts/python/guru_team_trellis.py` 与 canonical `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `record-planning-approval.sh` / `check-planning-approval.sh` 依赖的 planning approval data contract
- workflow / preset durable docs 与 `.trellis/spec/**`
- planning approval 相关单元测试

## 验证结果

已通过：

- `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
- `python3 -m json.tool trellis/index.json`
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`，194 tests OK
- `python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`，27 tests OK
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-09-083-planning-ambiguity-review`
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 1.4`
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 1.5`
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 2.1`
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5`
- `git diff --check`
- `check-review-gate.sh --json --allow-metadata-after-gate`

未验证：

- 未跑完整 throwaway repo 安装链路。
- 未跑 `trellis init -u <name> --workflow guru-team --workflow-source gh:castbox/guru-trellis/trellis` 对当前分支版本的安装验证。
- 未跑已有项目 `trellis workflow --marketplace gh:castbox/guru-trellis/trellis --template guru-team` 对当前分支版本的切换验证。
- 未跑完整 upgrade/update 抽样验证。

这些未验证项不会改变本 PR 的代码审查结论，但 reviewer 不应把本 PR 解读为已完成新仓库开箱即用或 upgrade/update 全链路验收。

## Review Gate

Branch Review Gate 已通过。

- 审查代理：`019f4728-e8f6-7a62-83ce-5f311f61e72a`
- reviewed_head：`50ffafb6eef69a22082c8048555e2a7570ef34f6`
- diff_range：`origin/main...HEAD`
- findings_count：0

审查覆盖 canonical/dogfood workflow、platform overlays、companion Python helper、Bash wrappers、unit tests、durable docs/specs、README、preset README、task artifacts、部署影响和安全影响。

## Docs SSOT

- strategy：`ssot_first`
- durable docs：已同步 durable docs / specs：

- `docs/requirements/guru-team-trellis-flow.md`
- `docs/requirements/requirement-main.md`
- `.trellis/spec/workflow/workflow-contract.md`
- `.trellis/spec/workflow/data-contracts.md`
- `.trellis/spec/workflow/companion-scripts.md`
- `.trellis/spec/workflow/quality-guidelines.md`
- `.trellis/spec/preset/overlay-guidelines.md`

- merged_delta：已合并回 durable docs 的 task delta：

- ambiguity review 定义与审查顺序
- 受控弱约束词表
- `planning-approval.json` 1.2 data contract
- 脚本 recorder / validator 边界
- overlay 与 Phase 2 / Branch Review 检查要求

- task_history：保留为 task history 的内容：

- issue #83 的具体 planning / design / implementation artifact
- sub-agent liveness 和 Branch Review raw report
- 本次验证命令记录与未验证项说明

- followup_or_limitation：未跑完整 throwaway install、当前分支版本 `trellis init --workflow-source gh:castbox/guru-trellis/trellis` 安装验证、已有项目 workflow 切换验证和 upgrade/update 抽样验证；Reviewer 不应把本 PR 解读为已完成开箱即用或 upgrade/update 全链路验收。

## Issue 关闭范围

Closes #83

本 PR 不关闭其他 issue，没有 `related_issues` 或 `followup_issues`。

## 安全说明

本 PR 不修改 `.github/workflows`、Docker / Compose、Kubernetes / Kustomize / Helm、数据库 migration、Makefile 或运行时部署资产。

本 PR 不读取或写入 token、private key、`.env`、签名 URL、数据库 URL 或客户数据。审查中未发现 secret 泄露。
