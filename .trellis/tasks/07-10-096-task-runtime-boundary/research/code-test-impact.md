# Research: Issue #96 代码与测试影响面

- Query: Issue #96 中移除 Guru Team 原 `handoff` 概念，重建 task-local 任务启动上下文与 gitignored 本机运行态边界；重点追踪 `handoff.json`、`handoff_path`、`workspace_path`、workspace boundary、`prepare-task`、finish/publish 的实现、schema、测试和配置引用。
- Scope: mixed
- Date: 2026-07-10

## Findings

### 1. Issue 合同与边界

Issue #96 明确要求：

- 删除 `.trellis/guru-team/handoff.json` 及 `handoff_path` 公共概念，不保留 legacy fallback。
- 新增 task-local、tracked、可移植的 `.trellis/tasks/<task-slug>/task-start-context.json`。
- 新增 local-only、gitignored 的 `.trellis/.runtime/guru-team/workspaces/<workspace-slug>.json` 与 `.trellis/.runtime/guru-team/tasks/<task-slug>.json`。
- `task-start-context.json` 只允许 task 可移植事实；绝对路径、`existing_worktrees`、完整 `preflight`、developer identity 路径、命令路径不得进入 tracked task artifact。
- workspace boundary 必须在每次命令运行时重算 checkout/branch/dirty/base freshness/worktree 状态，不能再依赖 committed absolute `workspace_path`。
- 本 issue 不修改官方 `.trellis/scripts/task.py`、`add_session.py` 的语义；workspace journal/`finish-summary.json` 属于后续 #97/#100/#98。

任务 PRD 已复述同一边界：`.trellis/tasks/07-10-096-task-runtime-boundary/prd.md`；最终实现必须以 live Issue #96 为验收源。

### 2. 当前数据流

#### 2.1 配置加载

- 默认配置把 `handoff_path` 固定为 `.trellis/guru-team/handoff.json`：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:39`。
- canonical config template 暴露 `handoff_path`：`trellis/workflows/guru-team/config-template.yml:52`。
- dogfood config 同样包含该键：`.trellis/guru-team/config.yml:52`。
- `load_config()` 合并默认值、`.trellis/guru-team/config-template.yml` 和 `.trellis/guru-team/config.yml`：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:557`。

#### 2.2 `prepare-task` planner/executor

- shell 入口只转发到 Python `prepare` 子命令：`trellis/workflows/guru-team/scripts/bash/prepare-task.sh:1`。
- `cmd_prepare()` 解析 issue、命名、base、worktree/task 创建参数：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:6275`。
- `prepare_workspace()` 根据 `workspace_mode` 返回当前 checkout 或 `<worktree_root>/<workspace_slug>`，必要时执行 `git worktree add`：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:1699`。
- payload 当前直接写入绝对 `workspace_path`、绝对 `handoff_path`、`workspace_slug`、`task_slug`、`task_dir`、branch/base/issue、issue scope seed 和完整 `preflight`：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:6426`、`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:6454`。
- `preflight` 当前包含 source checkout/repo root/worktree root、existing worktrees、dirty、developer identity、base freshness 等本机与一次性诊断状态。当前 dogfood 实例可实时确认这些字段存在于 `.trellis/guru-team/handoff.json`。
- `create_task()` 依赖 payload 的绝对 `workspace_path`，并在该 cwd 下调用官方 `task.py create`：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:6256`。
- 创建 task 后，`cmd_prepare()` 在 workspace 中调用 `task.py set-branch`、`set-base-branch`、`set-scope`，随后 `write_handoff()`：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:6526`。
- `write_handoff()` 将 `handoff_path` 回写 payload，并把整个 payload JSON 写到 workspace 固定路径；可选 mirror 到 source checkout：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:1836`。

结论：当前 `prepare-task` 的 planner payload、executor runtime state、task portable facts 没有分层；executor 通过一个 tracked fixed path 把三类数据合并持久化。

#### 2.3 后续命令读取 handoff

- `load_handoff()` 只从当前 root 的 configured fixed path 读取 JSON，并补默认 `handoff_path`：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:1936`。
- `resolve_task_dir()` 接受显式 `--task`，否则读取当前 task，最后可从 handoff 的 `task_dir` 回退：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:1985`。
- planning/phase2/assignment/review 等 recorder/checker 均先 `load_handoff()`，再 `resolve_task_dir()`，并调用 `assert_workspace_boundary()`；直接调用点见 `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:6544`、`:6694`、`:6796`、`:6852`、`:6912`、`:6941`、`:6985`、`:7011`、`:7066`、`:7088`。
- issue scope ledger loader 仍以 handoff 为 primary issue seed/fallback，因此任务启动上下文替换后需同步函数参数与字段读取，不能只改文件名。

#### 2.4 workspace boundary

- `workspace_boundary_context()` 从 handoff 读取绝对 `workspace_path` 作为 expected workspace，并使用 fixed `configured_handoff_path(root, config)`：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:2088`。
- `workspace_boundary_task_relative()` 从 handoff 的 `task_dir`/`task_slug` 推导 task 相对路径，并比较 `task_slug`、`workspace_slug`、`branch_name`、`workspace_path`：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:2049`。
- `collect_workspace_boundary_snapshot()` 会读取 source checkout 的 handoff，并把绝对 handoff path、source status、worktree 列表等加入 snapshot：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:2114`。
- `workspace_boundary_errors()` 在 worktree 模式下把“当前 checkout 缺少 handoff.json”作为阻塞，并用 `handoff.workspace_path` 判断 cwd 是否正确：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:2211`。
- `cmd_check_workspace_boundary()`/`assert_workspace_boundary()` 是所有 gate recorder/checker 的共同硬门禁：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:6221`、`:2279`。

结论：workspace boundary 是本次根因级重构点。新实现应以当前 `repo_root()`/cwd、repo-relative `task_artifact_dir`、当前 task context、`git worktree list --porcelain` 或 local runtime cache 重建 expected workspace；tracked task context 不应保存绝对 workspace path。

#### 2.5 finish / publish

- `finish-work.sh` 和 `publish-pr.sh` 都只是 Python 子命令包装器：`trellis/workflows/guru-team/scripts/bash/finish-work.sh:1`、`trellis/workflows/guru-team/scripts/bash/publish-pr.sh:1`。
- `cmd_finish_work()` 首先加载 handoff、解析 task、执行 workspace boundary，再检查 review gate/current HEAD/dirty/PR readiness：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:7437`。
- finish 正常路径仍调用官方 `task.py archive` 和 `add_session.py`，然后提交 metadata、迁移 archived review gate，最后构造 internal publish args：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:7505`。
- `cmd_publish_pr()` 同样加载 handoff、解析 task、执行 workspace boundary，再检查 gate、body、push/PR：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:7188`。
- publish 的 direct-call/recovery marker、finish 的 explicit entrypoint marker 与 Issue #96 无需改变；变化集中在任务上下文和 runtime workspace 的解析来源。
- archive 后 task 路径从 active 变 archived，当前逻辑会重写 review/body artifact path。新 `task-start-context.json` 若随 task 目录 archive，应允许 finish/publish 从 archived task dir 继续读取；local runtime task cache 的生命周期和 archived task key 需要显式定义。

### 3. 需要修改的 canonical 文件

#### 3.1 核心实现、schema、配置、manifest

1. `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
   - 删除 `DEFAULTS.handoff_path`、`METADATA_ONLY_FILES` 中 fixed handoff、`configured_handoff_path()`、`workspace_handoff_path()`、`write_handoff()`、`load_handoff()` 及 handoff 参数命名。
   - 新增 task start context 的构建/校验/读写，以及 workspace/task local runtime cache 的构建/读写。
   - `cmd_prepare()` 在 task 创建后写 task-local context；worktree 创建/复用过程写 gitignored runtime cache。
   - `create_task()` 不应通过 tracked payload 的绝对路径耦合；planner 输出可继续展示绝对 proposed workspace，但持久化必须拆分。
   - 重写 workspace boundary 的 context/snapshot/errors，运行时重算事实并仅把 local cache 当可重建提示。
   - 全部 recorder/check/finish/publish 调用签名从 handoff 改为 task context/runtime context。
   - metadata allowlist 与 source checkout drift 判定移除 fixed handoff 路径。

2. `trellis/workflows/guru-team/schemas/intake-handoff.schema.json`
   - 删除或重命名为 task start context schema（Issue 固定要求删除/重命名）。
   - 新 schema required 字段应与 Issue 固定字段一致，并通过 schema/额外 validator 禁止绝对路径、`.trellis/.runtime/**`、`existing_worktrees`、`preflight`、developer/command path。
   - 若 runtime cache 需要 schema，建议新增独立 local-runtime schema，避免与 tracked artifact 混用。

3. `trellis/workflows/guru-team/config-template.yml`
   - 删除 `handoff_path`。
   - 不应新增可任意配置的 tracked runtime path；Issue 已固定 runtime path。若保留配置，仅应是 team-level policy，不允许普通 task 静默修改。

4. `trellis/guru-team-extension.json`
   - `public_api.artifact_contracts` 删除 `.trellis/guru-team/handoff.json`，加入 `task-start-context.json`；是否公开 runtime cache schema/path需明确标为 local-only contract。
   - extension version/public API 变化应按仓库公共 API 规则升级并记录迁移语义。

5. `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
   - `MANAGED_WORKFLOW_FILES` 当前显式复制 `schemas/intake-handoff.schema.json`：文件清单必须同步新 schema 名。
   - 确保 install/update idempotent 管理 `.trellis/.runtime/` ignore；当前官方生成的 `.trellis/.gitignore` 已含 `.runtime/`，但 throwaway/upgraded repo 仍需验证。
   - 安装器需删除已管理的旧 installed handoff schema/旧 tracked handoff 文件，且遵循 `.new/.bak` 冲突语义，不能静默覆盖用户改动。

6. `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`
   - 增加普通 task prepare/create 不生成 `.trellis/guru-team/handoff.json`、不改 `.trellis/workspace/**`、不写共享配置的断言。
   - 增加 task-local context portable field allowlist、runtime cache ignored/untracked、双并行 task tracked metadata 路径不相交的断言。
   - 更新 extension manifest artifact contract 断言与新 schema 安装断言。

#### 3.2 canonical workflow/docs

7. `trellis/workflows/guru-team/workflow.md`
   - 全面用“任务启动上下文”“本机运行态”替代 intake provenance handoff；Phase 0、workspace machine boundary、planning/phase2/review/finish/publish 条款均有引用。
   - 保留 Issue Scope Ledger 是 close/ref/followup SSOT，但 seed 来源改为 task start context。

8. `trellis/workflows/guru-team/README.md`
9. `trellis/presets/guru-team/README.md`
10. `README.md`
11. `docs/requirements/guru-team-trellis-flow.md`
12. `docs/requirements/requirement-main.md`
13. `docs/requirements/README.md`
   - 更新 artifact contract、安装结果、prepare/create 流程、workspace boundary、finish/publish 数据来源和安全说明。
   - 历史说明可保留 `handoff` 作为被删除概念；运行路径/API 文档不应再指导读取旧文件。

#### 3.3 canonical overlays / skills / prompts

14. `trellis/presets/guru-team/overlays/**`
   - 当前 overlay source 的直接关键字检索结果很少/为空，但 overlay 管理的平台入口文件实际由 source 模板生成，必须逐一检查所有 `trellis-start`、`trellis-continue`、`trellis-finish-work` 以及 sub-agent prompt 的语义，不可只依赖字符串搜索。
   - `.trellis/spec/preset/overlay-guidelines.md:178` 当前明确要求把 `handoff.json` 作为 intake provenance，spec 需要由 update-spec 流程同步（本调研只读，不修改）。

15. `.trellis/spec/preset/installer.md`、`.trellis/spec/preset/overlay-guidelines.md`、`.trellis/spec/docs/public-docs.md`
   - 属于 related specs；实现 agent 不应直接随代码 patch 修改 spec，需按仓库规则使用 `trellis-update-spec` 做可执行合同更新。

### 4. dogfood / 生成副本

当前 canonical 与 dogfood 核心文件 hash 相同：

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` → `.trellis/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/workflows/guru-team/config-template.yml` → `.trellis/guru-team/config-template.yml`
- `trellis/workflows/guru-team/schemas/intake-handoff.schema.json` → `.trellis/guru-team/schemas/intake-handoff.schema.json`
- `trellis/workflows/guru-team/workflow.md` → `.trellis/workflow.md`

需要同步/删除的 dogfood 安装副本：

- `.trellis/guru-team/scripts/python/guru_team_trellis.py`
- `.trellis/guru-team/scripts/bash/{prepare-task,check-workspace-boundary,finish-work,publish-pr,...}.sh`（包装器通常不需逻辑变化，但安装结果和命名文案需核对）
- `.trellis/guru-team/config-template.yml`
- `.trellis/guru-team/config.yml`（用户配置迁移/删除 `handoff_path`，注意不能由普通 task 静默改共享配置；本 issue 是 config/workflow task，可显式迁移）
- `.trellis/guru-team/schemas/intake-handoff.schema.json`（删除）及新 schema 副本
- `.trellis/guru-team/extension.json`
- `.trellis/guru-team/handoff.json`（当前 tracked fixed runtime artifact，必须从 canonical/install contract 与 git tracked 集合移除）
- `.trellis/workflow.md`
- `.agents/skills/{trellis-start,trellis-continue,trellis-finish-work}/SKILL.md`
- `.codex/prompts/*.md`、`.codex/skills/**`
- `.cursor/commands/*.md`
- `.claude/commands/trellis/*.md`

同步方式必须走 canonical overlay/preset：

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

不得直接只改 dogfood 副本。同步后需检查并处理 `.new`/`.bak`。

### 5. 测试影响面

主测试文件：`trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`。

现有直接相关测试：

- `test_create_worktree_writes_handoff_only_in_workspace`：当前断言 workspace 写 `handoff.json`、source 不写、payload 暴露绝对 `workspace_path`/`handoff_path`：`test_guru_team_trellis.py:900`。应替换为 task context + runtime cache 分层断言。
- `test_create_task_runs_task_py_in_workspace`：当前 payload 直接携带绝对 `workspace_path`：`test_guru_team_trellis.py:945`。应改为 executor runtime 参数/解析结果，不把绝对路径写进 tracked context。
- `test_check_workspace_boundary_reports_ok_snapshot`：当前依赖 handoff absolute workspace：`test_guru_team_trellis.py:1379`。
- `test_check_workspace_boundary_blocks_worktree_mode_without_handoff`：旧概念应删除，替换为缺 task-start-context、缺 runtime cache 可重建/不可重建分支：`test_guru_team_trellis.py:1391`。
- `test_check_workspace_boundary_blocks_wrong_cwd`、`test_artifact_recorder_blocks_source_checkout_with_same_task_artifact`、`test_wrong_task_artifact_arguments_are_rejected`：保留行为目标，但重写 fixture/判据：`test_guru_team_trellis.py:1404`、`:1418`、`:1435`。
- `test_check_planning_approval_rejects_phase0_handoff_source`：artifact source taxonomy 中的 handoff 命名需改为 task-start-context：`test_guru_team_trellis.py:1946`。
- publish/finish 大量测试通过 fixture handoff 驱动 task/workspace 解析；`test_publish_pr_direct_call_is_blocked_before_repo_or_push` 起的 publish 组与 finish 组需要统一 fixture factory 重构：`test_guru_team_trellis.py:2700` 以后。
- metadata tests 当前把 `.trellis/guru-team/handoff.json` 作为唯一 fixed metadata-only 文件；需改为 task-local context（是否允许 post-gate mutation应谨慎，原则上启动事实应创建后稳定）与 local runtime ignored file。

Issue 要求新增的测试类别：

1. task-start-context schema/semantic validation：绝对路径、runtime path、`existing_worktrees`、`preflight`、developer identity、command path 均拒绝。
2. local runtime cache：固定路径、ignored/untracked、原子写、cache 缺失可重建、cache stale 时以实时 git 事实为准。
3. workspace boundary：从当前 checkout + task relative path + worktree mapping 重建；错误 cwd、错误 branch、task/workspace mismatch、archived task、current mode/worktree mode。
4. prepare-task write allowlist：普通 task 只改新 task dir；不得改 `.trellis/guru-team/**`、`.trellis/workspace/**`、`.trellis/config.yaml`、`.trellis/guru-team/config.yml`、workflow/schema/overlay/ignore。
5. 并行 task：同一 developer 创建两个 task 后 tracked Trellis metadata changed paths 不共享 fixed file。
6. finish/publish：active task archive 后仍可读取 archived task context；runtime cache 缺失时可恢复；不要求本 issue 替换 journal。
7. installer/update：新装、旧装升级、旧 schema/old tracked handoff 删除或冲突处理、`.runtime/` ignore 幂等。
8. 文档扫描：运行路径/API 不再出现 `handoff_path` 或指导读取 `.trellis/guru-team/handoff.json`；允许测试/迁移/历史说明中的否定性出现。

### 6. 高风险兼容点

1. **archive 路径迁移**：task start context 位于 active task dir，`task.py archive` 会移动目录。finish 在 archive 前后都需解析同一上下文；publish recovery 可能只看到 archived dir。
2. **source checkout vs worktree 判定**：旧边界以 committed absolute `workspace_path` 为核心。新算法必须防止在 source checkout 上误写同名 task artifact，同时允许 runtime cache 丢失后恢复。
3. **planner 输出与持久化混淆**：planner JSON 可以向用户展示绝对 proposed workspace，但该 payload 不能原样写进 tracked task context。建议使用两个独立 builder/type，避免再次把 runtime 字段序列化。
4. **task 创建时序**：task-start-context 必须写进 task dir，因此只能在 `task.py create` 返回 task dir 后落盘；但创建 task 前的 worktree runtime mapping 已存在，需要 workspace cache 先行、task cache 后补。
5. **current workspace mode**：`workspace_mode: current` 没有外部 worktree，runtime mapping与 boundary 不能假设 `.git` 是目录或必须存在 sibling worktree root。
6. **metadata gate 语义**：当前 `handoff.json` 被视为 post-commit metadata-only。新 task-start-context 若允许 gate 后变化，会使 portable启动事实失稳；更安全是创建后不可变/严格字段更新，而 local runtime 变化完全 ignored。
7. **Issue Scope Ledger seed**：多处 loader 从 handoff source_issue fallback。必须一次性切换为 task start context，否则 prepare 正常但 finish/publish 丢 primary issue/close semantics。
8. **installed config migration**：删除 config key 不能只改 template；`.trellis/guru-team/config.yml` 可能保留旧键。loader 应忽略/拒绝/报告 deprecated key，installer 要有明确迁移结果。
9. **public API/version**：manifest 将 artifact contract 暴露给安装验证和消费者；文件名变化属于公共 API 变更，需 version/release notes/upgrade evidence。
10. **官方 Trellis update 冲突**：`.trellis/.gitignore` 属于官方生成面；虽然当前已有 `.runtime/`，仍须验证 `trellis update` 后不丢失。不要依赖本 dogfood 历史状态。
11. **overlay 多平台一致性**：平台入口可能没有直接字符串命中，但其流程合同仍会提到 provenance/machine boundary。必须 apply all platforms + drift check，而非只改 `.agents`/Codex。
12. **不越界到 #97**：finish 当前仍 archive+journal；本 issue 只改它如何找 task/runtime，不应顺手替换 `add_session.py` 或 workspace journal。
13. **敏感路径泄漏**：测试 fixture、命令 JSON、PR evidence 不应把真实用户 home/worktree 绝对路径写进 tracked artifact；runtime output可以显示但必须 local-only/脱敏审查。
14. **删除旧 tracked 文件**：当前 `git ls-files` 明确包含 `.trellis/guru-team/handoff.json`。只停止写入不够，必须从 tracked contract 删除，否则并行分支仍可能携带 stale 内容。

### 7. 建议验证命令

#### 7.1 静态检索与生成漂移

```bash
rg -n 'handoff_path|\.trellis/guru-team/handoff\.json|intake-handoff' \
  trellis .trellis .agents .codex .cursor .claude docs README.md

trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
find . -name '*.new' -o -name '*.bak'
```

通过口径：运行路径/配置/API 无旧概念；仅测试旧文件不存在、迁移说明、历史背景可命中。

#### 7.2 单元测试

```bash
python3 -m unittest trellis.workflows.guru-team.scripts.python.test_guru_team_trellis
```

因目录名含连字符，若 module import 不适用，使用仓库现有直接入口：

```bash
python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
```

建议先运行新增的 Issue #96 test class/测试名，再跑全文件。

#### 7.3 schema / artifact 安全断言

```bash
python3 - <<'PY'
import json
from pathlib import Path
for path in Path('.trellis/tasks').glob('*/task-start-context.json'):
    data = json.loads(path.read_text())
    text = json.dumps(data)
    assert not Path(str(data.get('task_artifact_dir', ''))).is_absolute()
    for forbidden in ('workspace_path', 'handoff_path', 'existing_worktrees', 'preflight', '.trellis/.runtime/'):
        assert forbidden not in text, (path, forbidden)
PY
```

另需使用项目采用的 JSON Schema validator 校验正反 fixture。

#### 7.4 tracked write allowlist / 并行 task

在 throwaway repo 中：

```bash
git status --short
.trellis/guru-team/scripts/bash/prepare-task.sh --json '#<issue-a>' --short-name ... --workspace-slug ... --task-slug ... --branch ... --create-worktree --create-task
.trellis/guru-team/scripts/bash/prepare-task.sh --json '#<issue-b>' --short-name ... --workspace-slug ... --task-slug ... --branch ... --create-worktree --create-task

git -C <worktree-a> status --short
git -C <worktree-b> status --short
git -C <worktree-a> diff --name-only -- .trellis
git -C <worktree-b> diff --name-only -- .trellis
git ls-files '.trellis/guru-team/handoff.json' '.trellis/.runtime/**'
git check-ignore -v .trellis/.runtime/guru-team/workspaces/<slug>.json
```

通过口径：两个分支只各自新增 task dir 下 artifact；不共享 fixed tracked path；runtime cache ignored；workspace/config/shared workflow 不变。

#### 7.5 workspace boundary / finish / publish

```bash
.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task .trellis/tasks/<task>
.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work --task .trellis/tasks/<task> --dry-run --body-file .trellis/tasks/<task>/pr-body.md
```

需额外测试：删除 local runtime cache 后 boundary 可由实时 git/worktree 事实重建；切到错误 checkout/branch 时 fail closed；archive 后 publish recovery 可从 archived task context 恢复。

#### 7.6 throwaway 安装与 upgrade/update

```bash
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
```

并按 README 的真实命令执行：

```bash
trellis init -u <name> --workflow guru-team --workflow-source gh:castbox/guru-trellis/trellis
trellis workflow --marketplace gh:castbox/guru-trellis/trellis --template guru-team --create-new
```

还需在 throwaway repo 执行 `trellis update`（或当前官方等价命令），记录版本、diff、`.new/.bak`、重新 apply preset 后状态，确认新 artifact/runtime 边界不被回退。

### 8. Files found

- `AGENTS.md` — 仓库级官方优先、canonical/dogfood、开箱即用与 upgrade/update 门禁。
- `.trellis/workflow.md` — 当前 dogfood workflow 运行合同，和 canonical workflow hash 相同。
- `.trellis/tasks/07-10-096-task-runtime-boundary/prd.md` — 当前 task 的 Issue #96 需求摘录与验收边界。
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` — prepare/boundary/gates/finish/publish 的 canonical 单体控制器。
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` — canonical 单元测试全集。
- `trellis/workflows/guru-team/schemas/intake-handoff.schema.json` — 当前混合 payload schema。
- `trellis/workflows/guru-team/config-template.yml` — 当前 `handoff_path` 配置来源。
- `trellis/guru-team-extension.json` — public artifact contracts/companion scripts manifest。
- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py` — canonical 到 installed `.trellis/guru-team` 的文件清单与复制器。
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh` — 新仓库安装验收脚本。
- `trellis/workflows/guru-team/workflow.md` — canonical Guru Team AI 流程合同。
- `trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、`README.md` — marketplace/preset/public install 文档。
- `docs/requirements/guru-team-trellis-flow.md`、`docs/requirements/requirement-main.md` — 原 handoff 与 workspace boundary 的需求 SSOT。
- `.trellis/guru-team/**` — dogfood installed companion scripts/config/schema/manifest 与当前 tracked handoff 实例。
- `.agents/skills/**`、`.codex/**`、`.cursor/commands/**`、`.claude/commands/trellis/**` — 多平台 dogfood 入口副本。
- `.trellis/.gitignore` — 已包含 `.runtime/` ignore，但须验证新装/update 语义。

### 9. External references

- Trellis docs index（实时读取 2026-07-10）：`https://docs.trytrellis.app/index.md`。官方概念把 Task 放在 `.trellis/tasks/`、Workspace journal 放在 `.trellis/workspace/`；Guru Team 的新 task start/runtime artifact 必须明确是扩展，不得冒充官方原生 lifecycle。
- Custom workflow（实时读取 2026-07-10）：`https://docs.trytrellis.app/advanced/custom-workflow.md`。团队 workflow 应通过 marketplace Markdown workflow 分发，不修改 Trellis upstream。
- Custom spec template marketplace（实时读取 2026-07-10）：`https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md`。task/runtime 实例不属于可复用 spec template 内容。
- 当前 extension manifest 指定 Trellis CLI `0.6.5`，extension version `0.6.5-guru.3`：`trellis/guru-team-extension.json:5`、`:8`。

### 10. Related specs

- `.trellis/spec/preset/installer.md` — canonical 复制、安装器、managed files、throwaway 验证规则。
- `.trellis/spec/preset/overlay-guidelines.md` — 多平台流程入口、workspace boundary、finish/publish 入口规则；当前仍含旧 handoff provenance 约定。
- `.trellis/spec/docs/public-docs.md` — README/公共文档安装与发布流程一致性。
- `.trellis/spec/guides/cross-layer-thinking-guide.md` — 跨层 artifact/config/platform 同步检查方法。

## Caveats / Not Found

- 本调研严格只读业务代码；唯一写入是任务要求的 task-local research 文件。
- 未运行会产生副作用的 `prepare-task --create-worktree --create-task`、finish、publish、installer apply、throwaway install 或 `trellis update`；这些列为建议验证命令，不宣称已通过。
- `gh issue view 96` 已实时读取 Issue 正文；评论为空/未提供额外变更口径。
- 官方文档为 2026-07-10 实时 HTTP 内容；本报告未依赖旧记忆推断扩展方式。
- `trellis/presets/guru-team/overlays/**` 的旧关键词直接检索未发现明显命中，不代表无语义影响；installed 多平台入口有大量引用，实施时必须按 overlay 生成链逐文件核对。
- Issue 指定“当前系统没有需要兼容的老任务”，因此不建议实现 legacy handoff fallback；但 installer/update 对已安装旧文件的安全删除与冲突提示仍是发布兼容门禁。
