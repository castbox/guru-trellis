## 检查完成（Fail-fast；全量验证未完成）

本轮按独立 Phase 2 检查执行。已确认 Branch Review finding
`BR116-R02-P2-01` 的精确 task metadata / runtime input allowlist 修复在正常正、
负例与 finalization-only `closeout-plan.json` 用例中成立；但继续审查发现一个新的
P2 fail-closed 缺口。该缺口可在 honest-but-fallible 的正常 Git 状态读取失败中复现，
无需伪造、篡改或恶意输入。依主会话指令，本轮在固化该 finding 后停止进一步全量
pass 尝试，结论为 `implementation_required`。

### 已检查文件

- 任务与批准上下文：
  - `.trellis/tasks/07-24-116-review-task-publication/check.jsonl`
  - `.trellis/tasks/07-24-116-review-task-publication/prd.md`
  - `.trellis/tasks/07-24-116-review-task-publication/design.md`
  - `.trellis/tasks/07-24-116-review-task-publication/implement.md`
  - `.trellis/tasks/07-24-116-review-task-publication/implementation-handoff.md`
  - `.trellis/tasks/07-24-116-review-task-publication/planning-approval.json`
  - `.trellis/tasks/07-24-116-review-task-publication/issue-scope-ledger.json`
  - `.trellis/tasks/07-24-116-review-task-publication/review.md`
  - `.trellis/tasks/07-24-116-review-task-publication/review-gate.json`
  - `.trellis/tasks/07-24-116-review-task-publication/reviews/round-01-final-release.md`
  - `.trellis/tasks/07-24-116-review-task-publication/reviews/round-02-problem-discovery.md`
- `check.jsonl` 的 8 个 durable spec（均已完整读取）：
  - `.trellis/spec/workflow/quality-guidelines.md`
  - `.trellis/spec/workflow/skill-package-contract.md`
  - `.trellis/spec/workflow/workflow-contract.md`
  - `.trellis/spec/workflow/data-contracts.md`
  - `.trellis/spec/workflow/companion-scripts.md`
  - `.trellis/spec/preset/installer.md`
  - `.trellis/spec/preset/upstream-ownership.md`
  - `.trellis/spec/docs/public-docs.md`
- 本轮 finding 与修复候选的直接实现面：
  - `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
  - `.trellis/guru-team/scripts/python/guru_team_trellis.py`
  - `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
  - `trellis/skills/guru-team/packages/guru-review-task-publication/SKILL.md`
  - `trellis/skills/guru-team/packages/guru-review-task-publication/interface.json`
  - `trellis/skills/guru-team/packages/guru-review-task-publication/references/contract.md`
  - `trellis/skills/guru-team/packages/guru-review-task-publication/schemas/pr-readiness.schema.json`
  - `trellis/skills/guru-team/registry.json`
  - `trellis/workflows/guru-team/workflow.md`
- 完整变更范围清单：
  - `origin/main...HEAD` 的 committed diff（HEAD
    `aacb6e02e5386578bfe3d046511a0002a51cb581`）
  - 当前 dirty fix 的 15 个 tracked path 与历史 Branch Review task-local
    untracked artifacts
- 官方 Trellis 扩展面：
  - `https://docs.trytrellis.app/`
  - `https://docs.trytrellis.app/advanced/custom-workflow`
  - `https://docs.trytrellis.app/advanced/custom-spec-template-marketplace`

### 已修复问题

- 无。本轮权限只允许写本 raw report，不允许修改 source、planning、gate、
  assignment、commit、push 或 PR。

### 未修复问题

#### `PH2-116-R6-P2-01`：publication repository status 读取失败时 fail-open

- 严重级别：P2
- 状态：open
- route：`implementation_required`
- 正常复现前置：
  1. 一个普通 Git task worktree；
  2. task 下存在应被 exact allowlist 拒绝的真实 dirty path，例如
     `.trellis/tasks/fixture/debug-note.md`；
  3. `git diff`、`git rev-parse` 等 Git 读取正常，但本次 `git status` 因普通工具/
     仓库状态读取错误返回非零。
- 受影响代码：
  - `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:4103`
    的 `git_status_paths()` 已提供 `fail_closed=True`；
  - 同文件 `task_publication_repository_binding()` 当前在约
    `14117-14119` 行调用 `git_status_paths(root)`，未启用
    `fail_closed=True`；
  - `git_status_paths()` 在默认参数下遇到非零返回码会返回空列表，因此真实 dirty
    path 被投影为 `status_paths=[]`。
- 精确复现命令：

```bash
python3 - <<'PY'
import importlib.util
import subprocess
import tempfile
from pathlib import Path
from unittest import mock

module_path = Path(
    "trellis/workflows/guru-team/scripts/python/guru_team_trellis.py"
).resolve()
spec = importlib.util.spec_from_file_location("gtt_round6_probe", module_path)
gtt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gtt)
real_run = subprocess.run
with tempfile.TemporaryDirectory() as td:
    root = Path(td)
    task = root / ".trellis/tasks/fixture"
    task.mkdir(parents=True)
    real_run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
    real_run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=root,
        check=True,
    )
    real_run(
        ["git", "config", "user.name", "Test User"],
        cwd=root,
        check=True,
    )
    gtt.write_json(
        task / "task.json",
        {
            "id": "fixture",
            "status": "in_progress",
            "branch": "main",
            "base_branch": "main",
        },
    )
    real_run(["git", "add", "."], cwd=root, check=True)
    real_run(["git", "commit", "-qm", "base"], cwd=root, check=True)
    head = real_run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()
    real_run(
        ["git", "update-ref", "refs/remotes/origin/main", head],
        cwd=root,
        check=True,
    )
    (task / "debug-note.md").write_text("must be seen\n", encoding="utf-8")

    def selective_run(argv, *args, **kwargs):
        if list(argv[:2]) == ["git", "status"]:
            text_mode = kwargs.get("text") or kwargs.get("universal_newlines")
            empty = "" if text_mode else b""
            return subprocess.CompletedProcess(argv, 128, empty, empty)
        return real_run(argv, *args, **kwargs)

    with mock.patch.object(gtt.subprocess, "run", side_effect=selective_run):
        binding = gtt.task_publication_repository_binding(root, task)
    print(
        {
            "status_paths": binding["status_paths"],
            "debug_note_exists": (task / "debug-note.md").is_file(),
        }
    )
PY
```

- 精确结果：exit `0`，stdout：

```text
{'status_paths': [], 'debug_note_exists': True}
```

- 合同冲突：
  - package contract 要求任何不在 exact task metadata、current-command explicit
    runtime input 或 finalization-only exact `closeout-plan.json` 中的 status path
    都必须令 `review_range_and_working_tree` 失败；
  - Interface 将该 precondition 定义为当前 diff/status/metadata tail 的 fresh
    rebuild；
  - `skill-package-contract.md` 要求 status path 闭合且任何其他 path 阻止
    `ready`；
  - 当 status 扫描失败被折叠成空集合时，checker 既未证明 exact allowlist，也未
    证明 freshness，却可能继续形成 passed binding，属于正常失败路径上的
    fail-open。
- 建议最小修复：
  1. 在 `task_publication_repository_binding()` 中改为
     `git_status_paths(root, fail_closed=True)`；
  2. 同步 canonical / installed runtime；
  3. 新增回归：实际创建 dirty `debug-note.md`，模拟 `git status` 非零，断言
     `task_publication_repository_binding()` 抛出 `WorkflowError`，且
     `task_publication_entry_precondition_bindings()` 记录 failed
     `review_range_and_working_tree`；
  4. 覆盖 recorder、checker 与 finalization augmentation，证明三条路径均不能把
     status 读取失败解释为 empty status。
- 影响：
  - 当前实现不能证明 publication `ready` 的 working-tree exact allowlist；
  - 当前 round6 报告不能支撑 `phase2-check.json` 的 passed/complete 结论；
  - 必须修复后重新执行完整 Phase 2 语义检查与全量验证。

### 验证结果

- Workspace boundary：通过。expected workspace 与 actual repo root 均为
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/116-review-task-publication`；
  source checkout 无修改，`suspicious_source_artifacts=[]`。
- Planning approval：通过。`check-planning-approval.sh --json` 返回
  `status=ok`，当前 HEAD 与批准 HEAD 均为
  `aacb6e02e5386578bfe3d046511a0002a51cb581`，规划证据包含 passed
  `ambiguity_review`、fixed-scope scanner、零 unchecked normative hits 与当前
  durable authority digest。
- Lint：未完整执行；`git diff --check origin/main...HEAD` 与当前
  `git diff --check` 均 exit `0`。发现 P2 后按主会话指令停止全量 lint。
- TypeCheck：未执行；发现 P2 后按主会话指令停止。
- Tests：目标回归通过，全量测试未执行。
  - 首次命令：

```bash
python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py \
  TaskPublicationMetadataAllowlistTest \
  CloseoutTransactionContractTest.test_publication_finalization_augmentation_accepts_exact_plan_delta \
  CloseoutTransactionContractTest.test_publication_finalization_augmentation_rejects_other_metadata_delta
```

  - 首次结果：exit `1`，3 个加载项中 2 个通过、1 个
    `unittest.loader._FailedTest`；唯一错误是本轮调用使用了不存在的方法名
    `test_publication_finalization_augmentation_accepts_exact_plan_delta`。这是测试
    选择器名称错误，不是产品测试失败。
  - 校正命令：

```bash
python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py \
  TaskPublicationMetadataAllowlistTest.test_publication_status_allowlist_rejects_debug_note_and_accepts_contract_metadata \
  CloseoutTransactionContractTest.test_publication_finalization_augmentation_accepts_only_exact_closeout_plan \
  CloseoutTransactionContractTest.test_publication_finalization_augmentation_rejects_other_metadata_delta
```

  - 校正结果：exit `0`，`Ran 3 tests in 0.318s`，`OK`。
  - 已证明：
    - ordinary task-local `debug-note.md` 被拒绝；
    - Branch Review exact metadata、`issue-scope-ledger.json`、`pr-body.md`、
      `finish-summary-index.json` 与当前命令显式 regular runtime input 被接受；
    - recorder-owned `pr-readiness.json` 从自身 repository snapshot 排除；
    - 只有当前 task 的显式 regular `closeout-plan.json` 可作为
      finalization-owned delta；
    - 任意其他 `finalization_owned_paths` 参数不能扩张 allowlist。

### 证据交接

- 阶段二：
  - 已覆盖任务/规划/历史 gate、8 个 curated durable spec、完整 committed/dirty
    path inventory、publication active package、canonical runtime 与本轮 fix。
  - `BR116-R02-P2-01` 的精确 allow/reject/finalization 正常路径目标回归通过。
  - 新 finding `PH2-116-R6-P2-01` 阻止 pass；本报告只可支撑
    `implementation_required`，不可支撑新的 `phase2-check.json:passed`。
  - 发现阻塞 finding 后依主会话指令停止，尚未运行 runtime/skill/preset/
    ownership 全量 suites、source/installed validators、eval、dogfood drift、
    sidecar/parity、throwaway install/update/reapply。
- Docs SSOT：
  - 批准 strategy 为 `ssot_first`。
  - durable contract 与 package contract 已同步描述 closed task metadata、
    explicit runtime input 和 finalization-only closeout delta；task handoff 也记录
    相同边界。
  - 但 runtime 在 status 命令失败时未 fail closed，故 durable docs / task
    artifacts / code / tests 尚不一致，Docs SSOT reconciliation 不能判定完成。
- Branch Review：
  - 历史 `review-gate.json` 的 `typed_exit=implementation_required` 应继续保留为
    历史，不得当作 passed gate。
  - 本轮不是新的 Branch Review Gate，不修改 `review.md`、`review-gate.json`、
    assignment 或历史 raw reports。
  - 远程 exact-branch marketplace 仍未验证；本轮也未运行本地 throwaway
    install/update/reapply。不得声称 remote marketplace 或开箱即用已通过。

### 结论

`implementation_required`。

`BR116-R02-P2-01` 的原始宽前缀 allowlist 缺陷已由目标正/负例证明修复，但
`PH2-116-R6-P2-01` 表明 status 读取失败仍可被投影为空 status，导致
`review_range_and_working_tree` 与 freshness fail-open。当前实现、Docs SSOT 和
测试证据不足以支持 Phase 2 pass。修复并补充 fail-closed 回归后，必须重新执行完整
Phase 2 语义审查及全部验证矩阵。
