# Implementation Plan & Progress

## Phase 1: 配置解析与 runtime 修复

- [x] 读取 package-local runtime、错误 catalog 和当前 config helper。
- [x] 在 `runtime/common.py` 增加唯一 workspace 配置/path resolver。
- [x] 让 executor、checker 与 reuse/recovery 使用该 resolver。
- [x] 实现 `workspace_mode: current` 的零 worktree 行为与边界检查。

## Phase 2: 回归测试

- [x] 改造现有真实 Git 测试，使其显式写入并加载 workspace config。
- [x] 覆盖默认、绝对、相对、current、reuse/conflict、invalid、stale/mismatch。
- [x] 断言 public DTO 无本机绝对路径，ignored mapping 与 live workspace 一致。

## Phase 3: Canonical/installed 同步与文档

- [x] 更新 canonical Skill contract 与直接相关 README。
- [x] 用 preset apply 同步 dogfood installed/shared/Codex/Claude/Cursor copies。
- [x] 更新并校验 manifest/hash，不留下 sidecar。

## Phase 4: 验证

- [x] package-local tests。
- [x] source/installed Skill validators 与 canonical/installed parity。
- [x] dogfood overlay drift 与 `git diff --check`。
- [ ] clean initial install、existing preset reapply、official update 矩阵。
- [ ] 调用 `guru-check-task` 并处理所有 finding。

## Implementation Evidence

- `python3 -m unittest trellis.skills.guru-team.packages.guru-create-task-workspace.tests.test_contract trellis.skills.guru-team.tests.test_skill_packages`：19 tests，OK；其中 package-local 12 个真实 Git 用例覆盖默认/绝对/相对/current、exact reuse、conflict、missing/invalid/duplicate config、不可用父路径、stale mapping/checker mismatch。
- `python3 trellis/presets/guru-team/scripts/python/verify_installed_task_workspace.py --installed-repo . --work-root <temp>`：`status=ok`、`typed_exit=created`、`checker_status=passed`，验证 installed package 的新默认 `<source.name>-worktrees/<slug>`。
- `python3 -m unittest -v trellis.presets.guru-team.scripts.python.test_apply_guru_team_trellis_preset`：61 tests，106.104s，OK，覆盖 clean initial install、existing reapply、transaction/sidecar/managed-hash 行为的本地 installer 矩阵。
- `apply.sh --repo . --all-platforms --json`：最终 `status=ok`、Skill package `status=ok`、installed validation `passed`、0 conflict、0 sidecar；source/installed validators、canonical/installed/platform contract parity、dogfood drift、task validate 与 `git diff --check` 通过。
- `verify-throwaway-install.sh`：在任何安装副作用前按设计 fail closed；当前未 push 的 `fix/212-worktree-config-path` 没有可由 Trellis marketplace 拉取的 exact ref，脚本拒绝以 public `main` 冒充 current-branch evidence。因此 exact current-branch clean marketplace install + official `trellis update` + reapply 仍待有远端 ref 后执行，不能声称已通过。

## 实现边界

- 不创建 `implementation-handoff.md`。
- 不提交、push 或创建 PR，除非获得后续独立确认。
- 不触碰 Issue #211 的任何对象或 Issue #152 的 pooled mode。
