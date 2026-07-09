## 变更摘要

本 PR 解决 #56：Guru Team `prepare-task` 在未显式传入 `--branch` 时，不再固定生成 `codex/<slug>`，改为从 issue 标题、issue 正文或手写需求文本中确定性推断分支类型，并生成 `<branch-type>/<issue-slug>`。

- 支持的自动分支类型限定为 `feat`、`fix`、`refactor`、`perf`、`test`、`docs`、`style`、`build`、`ci`、`chore`、`revert`。
- 支持显式类型标记和关键词规则；识别不到合法类型时使用 `branch_type_default`，默认值为 `chore`。
- 显式 `--branch` 仍然优先，不受自动推断影响。
- `branch_prefix` 保留为 legacy 兼容字段，但默认置空，且不再驱动自动分支命名。
- `naming_quality.suggested_override_flags` 改为建议 `--branch <type>/<slug>`，不再建议 `--branch codex/...`。

## 影响范围

- 修改 canonical Guru Team helper、测试和配置模板：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`、`test_guru_team_trellis.py`、`config-template.yml`。
- 同步 dogfood 安装副本：`.trellis/guru-team/scripts/python/guru_team_trellis.py`、`.trellis/guru-team/config-template.yml`、`.trellis/guru-team/config.yml`。
- 同步流程和使用文档：`trellis/workflows/guru-team/workflow.md`、`.trellis/workflow.md`、`README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、`docs/requirements/requirement-main.md`。
- 修正 `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh` 中对 workflow 规划文档强制要求的旧精确字符串断言，使 throwaway install 验证继续检查当前 canonical workflow 合同。
- 未涉及 CI/CD workflow、Docker/Compose、K8s/Kustomize/Helm、DB migration、Makefile 或生产部署配置。
- Runtime 影响限定在 Guru Team `prepare-task` companion runtime 的默认分支命名；已有显式 `--branch` 用法保持兼容。

## 验证结果

- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：通过，203 tests OK。
- `python3 -m json.tool trellis/index.json`：通过。
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh .trellis/guru-team/scripts/bash/*.sh`：通过。
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py .trellis/guru-team/scripts/python/guru_team_trellis.py`：通过。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-09-056-auto-branch-type-prefix`：通过。
- `python3 ./.trellis/scripts/get_context.py --mode phase`：通过。
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 0.4`：通过。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：通过，dogfood overlay copies match canonical Guru Team overlays。
- `git diff --check` 和 `git diff --check origin/main...HEAD`：通过。
- canonical/dogfood helper、config template、workflow 逐字节 parity 检查：通过。
- 行为探针覆盖 11 个合法分支类型、unknown fallback 到 `chore`、显式 `--branch` 覆盖自动推断、legacy `branch_prefix` 不影响自动分支、`suggested_override_flags` 不再包含 `codex/`。
- `TRELLIS_WORKFLOW_SOURCE='gh:castbox/guru-trellis/trellis#fix/056-auto-branch-type-prefix' trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`：通过，验证当前 PR 分支 marketplace workflow 可安装，preset installer 可安装 `.trellis/guru-team/`、Codex/Cursor overlay、脚本可执行权限、入口阻断、`check-env` / `version`、语言规则归一化和 stale planning hint 检查。

当前 PR body 生成前已额外执行：

- `.trellis/guru-team/scripts/bash/check-review-gate.sh --json --allow-metadata-after-gate`：通过；当前 HEAD 仅比 reviewed head 多 review/gate metadata。

## Review Gate

- Branch Review Gate 已通过，gate artifact：`.trellis/tasks/07-09-056-auto-branch-type-prefix/review-gate.json`。
- reviewed head：`65d053a7592dd6bfc6c5407c2c20acf8ece853a5`。
- finish-work reviewed metadata head：`9fae97fba1967bbe80c44a97b6cc80354a5baa67`，相对 reviewed head 仅新增 review/gate metadata。
- 第 1 轮 final review 发现 P1 F-001：dogfood installed runtime/config 未同步，active runtime 仍会输出旧 `codex/<slug>`。
- 第 2 轮 F-001 closure review 确认 canonical/dogfood helper、config template、`.trellis/guru-team/config.yml` 和 active wrapper 行为已同步。
- 第 3 轮 fresh final review 覆盖完整 `origin/main...HEAD` diff，findings_count=0，可放行。
- PR 发布后补充的 `verify-throwaway-install.sh` 断言修正只影响开箱即用验证脚本本身，不改变 `prepare-task` runtime 行为；该后续改动已用当前 ref throwaway install 和 bash syntax 覆盖。

## Issue 关闭范围

Closes #56。

`issue-scope-ledger.json` 中 `close_issues` 只包含 #56，`related_issues` 和 `followup_issues` 为空。关闭依据是：默认分支已从固定 `codex/<slug>` 改为确定性 `<branch-type>/<slug>`；测试覆盖 11 个合法类型、fallback、显式覆盖和 legacy 字段兼容；F-001 dogfood 同步问题已闭环；Branch Review Gate 已覆盖当前 scope。

## 安全说明

本次变更不新增 secret、credential、token、private key、签名 URL、`.env`、数据库 URL 或客户数据处理逻辑。变更内容为本地 companion runtime、配置默认值、文档和 Trellis task/review artifact；PR body 与 gate artifact 不包含敏感凭据。

## Docs SSOT / 文档同步

- 计划策略：`ssot_first`。issue scope 先落到 task-local `prd.md`、`design.md`、`implement.md`，实现后将稳定行为同步回 canonical workflow/helper/config/docs。
- durable docs 已同步：`README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、`docs/requirements/requirement-main.md`、`trellis/workflows/guru-team/workflow.md`、`.trellis/workflow.md`、canonical/dogfood config template。
- `.trellis/spec/` 已检查，本轮未发现需要更新的 stale `codex/` 行为合同，因此没有修改 spec。
- task delta 已合并回 durable source 的部分：默认分支命名合同、合法 branch type 清单、fallback 规则、legacy `branch_prefix` 兼容语义、dogfood 同步要求和验证口径。
- task-history-only 内容：`agent-assignment.json`、`phase2-check.json`、`review.md`、`reviews/*.md`、`review-gate.json` 和本 `pr-body.md` 仅作为当前 #56 审计证据，不作为可复用 workflow 行为源头。
- 当前 PR 限制：Branch Review Gate 发生时当前 ref 的完整 throwaway install 尚未验证；PR 发布后已补跑并通过，验证证据保留在本 PR body 中。
