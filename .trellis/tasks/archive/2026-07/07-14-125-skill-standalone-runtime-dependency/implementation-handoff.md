# #125 实现交接

## 实现状态

`completed`

Issue #125 的批准范围已完成实现。未执行 commit、push、PR、Phase 2 recorder、
`phase2-check.json`、Branch Review 或 finish-work。

## Changed files

### Durable SSOT 与公开合同

- `.trellis/spec/workflow/skill-package-contract.md`
- `.trellis/spec/workflow/companion-scripts.md`
- `.trellis/spec/preset/installer.md`
- `.trellis/spec/docs/public-docs.md`
- `docs/requirements/README.md`
- `docs/requirements/requirement-main.md`
- `docs/requirements/guru-team-trellis-flow.md`
- `README.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`
- `trellis/workflows/guru-team/workflow.md`
- `.trellis/workflow.md`

### Canonical interface、runtime、installer 与 tests

- `trellis/guru-team-extension.json`
- `trellis/skills/guru-team/schemas/skill-interface.schema.json`
- `trellis/skills/guru-team/packages/guru-create-task-commit/{SKILL.md,interface.json,references/contract.md}`
- `trellis/skills/guru-team/packages/guru-create-task-commit/scripts/{check-task-commit-plan.sh,create-task-commit.sh}`
- `trellis/skills/guru-team/packages/guru-create-task-commit/tests/test_contract.py`
- `trellis/skills/guru-team/tests/test_skill_packages.py`
- `trellis/skills/guru-team/tests/fixtures/representative-active/extension.json`
- `trellis/skills/guru-team/tests/fixtures/representative-active/packages/guru-example-action/interface.json`
- `trellis/skills/guru-team/tests/fixtures/representative-active/schemas/skill-interface.schema.json`
- `trellis/workflows/guru-team/scripts/bash/run-skill-command.sh`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
- `trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`

### Preset 生成的 installed / discovery copies

- `.trellis/guru-team/extension.json`
- `.trellis/guru-team/scripts/bash/run-skill-command.sh`
- `.trellis/guru-team/scripts/python/guru_team_trellis.py`
- `.trellis/guru-team/skills/schemas/skill-interface.schema.json`
- `.trellis/guru-team/skills/packages/guru-create-task-commit/**`
- `.agents/skills/guru-create-task-commit/**`
- `.codex/skills/guru-create-task-commit/**`
- `.cursor/skills/guru-create-task-commit/**`
- `.claude/skills/guru-create-task-commit/**`

### Task-local evidence

- `.trellis/tasks/07-14-125-skill-standalone-runtime-dependency/implementation-handoff.md`

未修改 `.trellis/tasks/archive/2026-07/07-13-122-guru-create-task-commit/**`。

## 需求与设计承接

- 保留稳定 mode id `workflow` / `standalone` 与既有 typed exits。
- Interface schema 升级到 1.1：mode 增加闭集 `routing`，active interface 增加
  `runtime_dependency`，validator 增加 `runtime_command`。
- `workflow.routing=global_workflow`；
  `standalone.routing=direct_discovery`。Standalone invocation 使用完整 installed
  inventory，但显式不消费当前 global workflow route；普通 source/installed gate 仍验证
  canonical mandatory invoke 与 exit markers。
- Canonical extension 升级到 `0.6.5-guru.6`，发布
  `public_api.skill_runtime={api_version:1.0,dispatcher:run-skill-command,
  manifest_path:.trellis/guru-team/extension.json}`，并把 dispatcher 加入
  `companion_scripts`。
- 新增 shared `run-skill-command` dispatcher。它从 installed runtime 位置推导 repo，
  component-wise `lstat` 校验 package、manifest、interface、managed inventory、API、
  validator 与 runtime command，然后 `exec` 既有 shared companion command。
- 两个 package wrapper 只定位 audited installed/discovery layout，传 package root、固定
  validator id 和原参数；已删除旧 companion command 直连 fallback。
- Package-only copy、missing manifest/dispatcher、API/dependency/command mismatch、
  discovery drift 均在目标 companion command 和业务副作用前 exit 2，并输出 full preset
  install/upgrade、sidecar 处理和 source/installed validation remediation。
- Parser、task/gate 解析、Git snapshot、exact staging、transaction、rollback 与 result
  validation 继续只存在于 shared Guru Team runtime；package/platform copies 未复制这些能力。
- Preset 把 dispatcher 纳入 `MANAGED_ASSET_PATHS`、executable handling、installed
  manifest inventory、README installed-file list 和 throwaway upgrade/reapply probe。

## Docs SSOT

- Strategy：`ssot_first`。
- Durable implementation inputs：四份 `.trellis/spec/**`、三份
  `docs/requirements/**`、canonical workflow/package contract、三份 public README。
- Task delta 已回写：routing independence、runtime dependency、schema 1.1、non-portable
  边界、shared dispatcher、fail-closed remediation、installer/update/reapply 验证矩阵。
- Durable docs sync：完成，durable specs/requirements 先于 schema/runtime/installer 实现
  更新，最终与 canonical/generated copies 和 tests 一致。
- Task-history-only：stacked base 决策、Phase 0/1 输出、sub-agent liveness、首次
  throwaway exact-ref fail-closed 输出、`.bak` 逐项核对与临时验证日志。
- Middle-platform gate：不适用；未使用 go-guru/proto-guru/Unity/Flutter 中台能力。

## 验证结果

- `python3 trellis/skills/guru-team/packages/guru-create-task-commit/tests/test_contract.py`：
  5 tests passed。
- `python3 -m unittest discover -s trellis/skills/guru-team/tests -p 'test_*.py'`：
  64 tests passed。
- `python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：
  36 tests passed。
- `python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：
  275 tests passed。
- JSON：canonical/installed manifest、schema、production interface 全部 parse passed。
- Bash/Python static：`bash -n` 与 `py_compile` passed。
- `check-skill-packages --mode source`：passed。
- `check-skill-packages --mode installed`：passed，43 managed Skill files，0 sidecar、
  0 conflict、0 removal。
- Shared direct discovery：`.agents/.../check-task-commit-plan.sh --help` 经 dispatcher
  成功进入 shared `check-commit-messages`；unit test 另证明 unrelated active workflow 不会
  阻断 standalone resolver，而普通 installed gate 会拒绝该 workflow。
- Canonical package 与 audited/shared/Codex/Cursor/Claude 5 个受管副本：8 files 的 bytes
  与 executable mode 完全一致。
- `apply.sh --repo . --all-platforms`：最终幂等 apply passed；known managed `.bak` 已逐项
  与同步前/旧受管字节核对后清理；recursive `.new` / `.bak` 为 0。
- `check-dogfood-overlay-drift.sh`：passed。
- `task.py validate`：passed（implement 6 entries，check 8 entries）。
- workspace boundary / planning approval：passed。
- `git diff --check`：passed。
- `trellis --version`：`0.6.5`；Phase 3.4 context parse passed。
- `verify-throwaway-install.sh` 默认 exact-ref：按设计 exit 2，因为 feature branch 尚未
  commit/push，无法由官方 marketplace 解析 dirty current ref。
- `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 verify-throwaway-install.sh`：passed；覆盖 public
  marketplace discovery、当前 unpublished workflow/preset sample、初装 standalone probe、
  `trellis update`、workflow re-selection、preset reapply、第二次 standalone probe、
  source/installed validation、recursive sidecar scan 和 installed closeout smoke。

## Sidecar、升级与开箱状态

- 当前 repository recursive `.new` / `.bak`：0。
- Dogfood extension：`0.6.5-guru.6`，selected platforms 为 Claude/Codex/Cursor，
  `skill_packages.status=ok`，installed validation passed。
- 初装与 update/reapply canary 已通过；exact feature-ref remote marketplace verification
  必须在 reviewed content commit/push 后由 finish-work gate 执行。

## 安全与部署判断

- 错误信息只包含稳定 command/相对安装入口/remediation，不输出 token、secret、private
  key、签名 URL、`.env`、数据库 URL 或本机绝对路径。
- Runtime command 必须来自 closed interface validator id、extension published command
  inventory 和 managed executable path；禁止任意 runtime path 与 legacy fallback。
- 不新增服务、API、worker、schedule、queue、DB migration、容器、Kubernetes、CI/CD、
  Dockerfile、Compose、Kustomize 或 Makefile 变更；部署形态不变。

## Stacked PR limitation 与 remaining risks

- #125 仍 stacked 于 `feat/122-guru-create-task-commit` / PR #124。#124 merge 后必须把
  #125 PR retarget 到 `main`，重新检查 `origin/main...HEAD` diff，并重新运行 Phase 2、
  Branch Review 与 remote marketplace verification。
- Exact feature-ref marketplace 未在实现阶段验证，因为本代理不得 commit/push。Canary
  通过不能替代 push 后的 `verify-marketplace` immutable evidence。
- Trellis CLI 当前为 0.6.5，npm latest 在 throwaway update 输出中为 0.6.7；本任务按照已批准
  的 Guru Team 0.6.5 compatibility baseline 实现，未扩大为官方 CLI baseline upgrade。

## Trellis-check focus

- 独立核对 schema 1.1 digest/id、mode routing、runtime dependency 与 extension capability
  cross-field closure。
- 验证 standalone runtime 不读取 global workflow route，同时 ordinary source/installed gate
  仍要求 canonical markers。
- 重点审查 package-root/layout/component `lstat`、manifest/inventory drift、command mapping
  与 `os.execv` fail-closed 路径，确认任何失败发生在 target companion command 前。
- 搜索 package/platform wrappers，确认未复制 parser、task/gate、Git staging/transaction/
  rollback 逻辑，也没有旧 direct companion fallback。
- 复核 canonical、audited、shared、Codex、Cursor、Claude copies 与 installed manifest
  managed hashes/modes，确认 recursive sidecar 为零。
- 复核四份 spec、三份 durable requirements、canonical workflow/package contract、三份
  README 与实现的一致性。
- 明确记录 exact feature-ref remote marketplace 尚待 push 后 finish-work gate，不能把
  canary sample 提升为 remote pass evidence。
