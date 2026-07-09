## 变更摘要

- 为 Guru Team workflow 固化中文 Conventional Commits 合同：工作提交和 Trellis metadata 提交使用 `{type}({scope}): #{primary_issue} 中文描述`，merge commit 使用 `chore(merge): #{pull_request} 合并 #{primary_issue} 中文 PR 摘要`。
- 增加 `check-commit-messages` 与 `format-merge-commit` companion script，提供客观 commit message 校验和 merge commit payload 生成能力。
- 接入 finish/publish：metadata commit 使用 `chore(trellis): #<primary_issue> 固化任务收尾元数据`，publish dry-run/formal payload 输出合规 merge commit subject/body/命令，维护者不得依赖 GitHub 默认 `Merge pull request ...` subject。
- 补充 workflow helper 与 preset installer 测试，覆盖 issue #92 正反例、work body、metadata empty body、merge body、managed asset、extension public API 与 throwaway installer 断言。
- 修复 Branch Review Round 001 发现的缺口：commit subject 现在禁止 `Closes/Fixes/Resolves/Close/Fix/Resolve #xx`，PR body 才承载 issue close 语义。

## 影响范围

- `trellis/workflows/guru-team/workflow.md` 与 `.trellis/workflow.md`：新增并同步 commit subject/body、metadata commit、merge commit、Phase 2 check、Branch Review Gate、PR readiness、finish/publish 的提交规范合同。
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 与 `.trellis/guru-team/scripts/python/guru_team_trellis.py`：新增 commit message validator、merge payload formatter、metadata commit subject formatter，并接入 finish/publish。
- `trellis/workflows/guru-team/scripts/bash/check-commit-messages.sh`、`format-merge-commit.sh` 及 dogfood copy：新增 thin wrapper。
- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`、`trellis/guru-team-extension.json`、`.trellis/guru-team/extension.json`：将新增 wrapper 纳入 managed assets 与 public API。
- `README.md`、workflow README、preset README、`.trellis/spec/workflow/**`：同步团队长期提交规范、数据合同和质量检查要求。
- 不涉及 CI/CD、Docker/K8s、database migration、Makefile、runtime config 或 config template。

## 验证结果

- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：通过，243 tests。
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py .trellis/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`：通过。
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh .trellis/guru-team/scripts/bash/*.sh`：通过。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：通过。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-10-092-conventional-commits`：通过。
- `git diff --check`：通过。
- `.trellis/guru-team/scripts/bash/check-commit-messages.sh --task .trellis/tasks/07-10-092-conventional-commits --json`：通过，两个 work commit 均合规。
- `.trellis/guru-team/scripts/bash/format-merge-commit.sh --task .trellis/tasks/07-10-092-conventional-commits --pull-request 91 --summary '中文 Conventional Commits 提交规范' --head-branch codex/092-conventional-commits --base-branch main --json`：通过，生成合规 `chore(merge)` payload。
- `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 TRELLIS_WORKFLOW_SOURCE=gh:castbox/guru-trellis/trellis trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`：通过 public marketplace sample；当前分支/tag marketplace install 需要 push 或 tag 可解析后复验。

## Review Gate

- 结论：Branch Review Gate 通过，`review-gate.json` reviewed HEAD 为 `73a4985d07e4d2876c39a8ff53130cbdb1eb119e`。
- Round 001：发现 1 个 P2，commit subject validator 未禁止 close keyword。
- Round 002：同一 technical agent 作为 `问题闭环审查代理` 复核该 P2 已闭合，`findings_count=0`。
- Round 003：全新 `最终放行审查代理` 覆盖最新 `origin/main...HEAD` 完整 diff，`findings_count=0`。
- Gate evidence 覆盖 workflow/docs/spec、Python/bash companion scripts、preset installer、manifest、tests、dogfood copy、task artifacts、Phase 2 post-commit audit、commit message 合同、Docs SSOT、部署与安全影响。

## Issue 关闭范围

- Closes #92

### 仅引用或相关

- 无

### 后续范围

- 无新增 followup issue。当前分支或 release tag 可解析后，建议复验 `TRELLIS_WORKFLOW_SOURCE=gh:castbox/guru-trellis/trellis#<ref>` 的 marketplace install。

## 安全说明

- 本次变更未写入 token、secret、private key、`.env`、数据库 URL、signed URL 或敏感原始数据。
- 未新增服务、CLI runtime、worker、migration、container/K8s 资产或 CI/CD 入口；不需要部署资产同步。
- Companion script 仍只执行 objective validator / formatter / recorder / executor 行为，不把 review 充分性、issue close 判断或 PR readiness 判断下沉到脚本。

## Docs SSOT

- strategy：`ssot_first`。
- durable docs / 文档更新：已更新 `trellis/workflows/guru-team/workflow.md`、`.trellis/workflow.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、`README.md`、`.trellis/spec/workflow/workflow-contract.md`、`.trellis/spec/workflow/data-contracts.md`、`.trellis/spec/workflow/quality-guidelines.md`。
- task delta / merged delta：issue #92 的 subject/body/metadata/merge/publish 合同、forbidden close keywords、validator/formatter 入口和开箱验证限制已同步回写到 durable docs/spec。
- task history：Phase 0 handoff、planning approval、phase2-check、agent assignment、review lifecycle、review-gate、PR readiness 证据仅保留为任务历史。
- follow-up / limitation：当前分支 marketplace install 在未 push/tag 前无法通过 `gh:` source 验证；push 或 tag 可解析后应复验该安装路径。
