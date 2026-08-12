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
- [x] clean initial install、existing preset reapply、official update 矩阵。
- [x] 调用 `guru-check-task` 并处理所有 finding。

## Implementation Evidence

- `python3 -m unittest trellis.skills.guru-team.packages.guru-create-task-workspace.tests.test_contract trellis.skills.guru-team.tests.test_skill_packages`：27 tests，OK；除真实 Git 的默认/绝对/相对/current、exact reuse、conflict、missing/invalid/duplicate config、不可用父路径、stale mapping/checker mismatch 外，还覆盖 canonical/installed 文件入口、完整配置顶层列表与 shared dynamic-loader 模式。
- `python3 trellis/presets/guru-team/scripts/python/verify_installed_task_workspace.py --installed-repo . --work-root <temp>`：`status=ok`、`typed_exit=created`、`checker_status=passed`，验证 installed package 的新默认 `<source.name>-worktrees/<slug>`。
- `python3 -m unittest -v trellis.presets.guru-team.scripts.python.test_apply_guru_team_trellis_preset`：61 tests，106.104s，OK，覆盖 clean initial install、existing reapply、transaction/sidecar/managed-hash 行为的本地 installer 矩阵。
- `apply.sh --repo . --all-platforms --json`：最终 `status=ok`、Skill package `status=ok`、installed validation `passed`、0 conflict、0 sidecar；source/installed validators、canonical/installed/platform contract parity、dogfood drift、task validate 与 `git diff --check` 通过。
- `run-skill-evals.sh --mode source|installed --skill guru-create-task-workspace --adapter shared`：source 与 installed 的 `created`、`refresh_review`、`blocked` 三个 typed-exit case 全部通过。
- `TRELLIS_WORKFLOW_SOURCE='gh:castbox/guru-trellis/trellis#fix/212-worktree-config-path' verify-throwaway-install.sh <temp>`：远端 exact ref/commit `7eb30512570277e3661a02a94fb0c1eb4c9d19da`，source tree clean，退出码 0；fresh install 与 official update 后 reapply 均通过 15 个 installed packages、四个 public projections、Phase 0 transcript、Finish-family/closeout、workspace create/check、source/installed validators、ownership、平台 parity 和递归 zero-sidecar 检查，最终输出 `Verified throwaway Guru Team Trellis install`。
- Exact-ref 逐步验证发现并已修复三个正常路径缺陷：installed `prepare.py` 文件入口无法定位 shared runtime、完整合法配置的 `closeout_markers` 顶层列表触发字符串 `.append()`、Python 3.12 shared dynamic-loader 无 `sys.modules` 注册时 `@dataclass` 初始化失败；对应回归与 source/installed eval 均已通过。
- `guru-check-task`：对当前完整 task scope、committed diff、installed/upgrade evidence 与 Docs SSOT 完成 fresh semantic round，无未关闭 P0-P3 finding，typed exit 为 `passed`。

## 实现边界

- 不创建 `implementation-handoff.md`。
- 不创建 PR，除非获得后续独立确认。
- 不触碰 Issue #211 的任何对象或 Issue #152 的 pooled mode。
