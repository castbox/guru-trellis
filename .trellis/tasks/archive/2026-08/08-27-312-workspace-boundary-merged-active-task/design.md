# #312 技术设计：workspace boundary 的 Git-aware task artifact 分类

## 1. Design Principles

1. 放行条件必须由 source checkout 的真实 Git path state 证明，不能由文件存在或全局 clean 推断。
2. 例外只覆盖普通 task planning/intake 文件；review/check gate metadata 保持无条件 fail closed。
3. 分类在 collector 完成，既有 blocker consumer 与 `--allow-source-clean` 语义保持不变。
4. `guru-finalize-task` 与 `guru-review-task-publication` 保留 package-local ownership，但实现和测试必须
   对称。
5. canonical source 先修改，installed/dogfood/spec/platform surface 只由 preset apply 投影。

## 2. Current To Target

```text
Current
source task path exists
  -> every configured artifact becomes same_task_artifact
  -> dirty paths are scanned separately
  -> clean tracked planning files still block

Target
source task path exists
  -> review metadata/reviews directory: always block
  -> ordinary task file:
       tracked by source HEAD/index AND path clean -> accepted base projection
       otherwise -> same_task_artifact blocker
  -> dirty-path scan remains fail closed
  -> existing identity/cwd/runtime/task guards run unchanged
```

## 3. Path-State Classification

### 3.1 Inputs

Collector 继续使用现有 `source_checkout`、`task_relative`、
`WORKSPACE_BOUNDARY_SUSPICIOUS_TASK_ARTIFACTS`、`WORKSPACE_BOUNDARY_REVIEW_METADATA` 与
`source_status`。新增的内部 helper 只读取 Git 状态，不写 cache/artifact/runtime mapping。

对每个候选 repo-relative path，分类器固定区分以下四种状态：

| 状态 | 普通 task 文件 | Review metadata |
| --- | --- | --- |
| current `HEAD`/index tracked + path clean | 接受，不加入 suspicious | 阻断 |
| untracked | 阻断 | 阻断 |
| staged/unstaged/deleted/renamed | 阻断 | 阻断 |
| Git 状态不可唯一读取 | 阻断 | 阻断 |

“path clean”要求该精确路径在 staged 与 worktree diff 中均无变化；不能只依赖 source checkout
整体 clean。候选路径由内部常量与 task locator 生成，Git 调用使用参数数组和 `--` 终止 revision
解析。

### 3.2 Current-base binding

放行项必须同时满足：

- source checkout 是现有 runtime/worktree identity 解析出的 source；
- source `HEAD` 含该路径的 tracked entry，index 与 `HEAD` 对该路径无漂移；
- working tree 对该路径无漂移；
- 文件不属于 `WORKSPACE_BOUNDARY_REVIEW_METADATA`，也不位于 `reviews/**`。

上述条件把“已通过上一轮 PR 合并到 base 的 task 投影”与“source checkout 新建/修改的 task
artifact”分开。wrong source/workspace mapping 仍由既有 identity guard 阻断，不由该 helper 修复。

### 3.3 Snapshot contract

保持 `suspicious_source_artifacts` 的现有 shape。合法 tracked-clean 普通 task 文件直接不进入该数组，
避免新增 public field、kind 或 consumer 分支。非合法文件继续使用现有
`same_task_artifact`/`same_task_dirty_path`；review metadata 与 `reviews/**` 继续使用既有 kind。

`blocking_suspicious_source_artifacts()` 无需感知例外；它仍对 collector 产出的每个 item fail
closed。`workspace_boundary_errors()` 与 `assert_workspace_boundary()` 不改变。

## 4. Duplicate Owner Strategy

两份 owner 当前拥有一致的常量、collector 和 blocker。为保持 #195 package-local ownership，本任务
不抽取新的 shared runtime helper；在两个 package 内落相同的小型 Git path-state helper与相同控制流：

1. review metadata 先无条件加入 suspicious；
2. 普通 artifact 仅在 `tracked && clean` 时跳过；
3. Git 查询失败按不满足放行条件处理；
4. 保留既有 dirty-path 与 reviews-dir 扫描。

测试通过共享 fixture 期望或对称 case matrix 锁定语义一致性，防止后续单边漂移。

## 5. Test Design

### 5.1 Real Git source/task fixture

建立临时 source repository、`main`、task worktree、ignored runtime mapping 与 task identity；不要仅 mock
`artifact.exists()` 或 `safe_git_status_paths()`。把同 task planning 文件提交到 source `HEAD`，并在
task worktree 保持 active task，验证真实跨轮路径。

矩阵：

- tracked-clean 普通文件全集通过；
- untracked 普通文件阻断；
- tracked staged、unstaged、deleted、renamed 分别阻断；
- tracked-clean review metadata 与 `reviews/**` 阻断；
- source/task 无关 dirty 文件不产生 same-task blocker；
- wrong cwd、missing/wrong mapping、wrong worktree、wrong task/branch 继续阻断；
- `--allow-source-clean` 对真实 artifact blocker 无效。

同一矩阵必须同时覆盖 Finalizer owner 的 CLI 实际入口与 Publication owner 的直接/package contract；两个
owner 对关键 snapshot 字段与 typed failure 结论一致。

### 5.2 Distribution regression

- canonical 两 package tests；
- source/installed package byte与 mode parity；
- all-platform preset apply 后 dogfood installed copy；
- preset spec/docs 与 `.trellis/spec` parity；
- extension manifest managed hashes/inventory；
- clean throwaway install、update/reapply、unknown sidecar zero。

### 5.3 Downstream live proof

在修复候选可安装后，仅更新 Chengtuo #252 当前 task worktree 的 Guru Team preset，并从该 worktree
运行原 checker。验收同时读取 source checkout status、runtime mapping、worktree list 与 task identity，
证明通过来自新分类而非删除文件或改 mapping。

## 6. Compatibility And Rollback

- 公共 CLI、JSON snapshot schema、error text prefix、typed exit 与 owner不变；只减少一个 false-positive
  blocker 集合。
- 未跟踪/dirty/review metadata/wrong identity 的既有拒绝路径保持严格，因此不需要迁移现有 runtime
  mapping 或 task artifact。
- 未提交时可回退本 task 的 runtime/test/spec/managed projection delta；不删除任何 task/worktree。
- 已发布候选若发现回归，停止安装/使用该候选并提交修复，不通过放宽 `--allow-source-clean` 临时绕过。

## 7. Docs SSOT Plan

Strategy：`ssot_first`。

1. 先修订 canonical `.trellis/spec/workflow/companion-scripts.md`：把“current-task artifacts fail
   closed”收敛为“非 current-base-tracked-clean 普通 artifact 以及所有 review metadata fail closed”，
   明确逐路径 Git 判定。
2. 修订 `.trellis/spec/workflow/quality-guidelines.md`，把 tracked-clean、untracked、dirty、review
   metadata、wrong identity 与 unrelated dirty 加入必测矩阵。
3. RDT 维持 `rdt_aligned`，Architecture 维持 no-impact；不创建 contribution/ADR，不修改 shared
   current `.40`。
4. 再修改两个 canonical owner 与 tests；由 all-platform preset apply 生成 dogfood installed package、
   preset spec/docs、manifest 与平台投影。
5. 若 runtime change 证明公共 snapshot/owner/route 必须改变，回到 Phase 1，不能在实现中静默扩张。

## 8. Expected Change Surface

- `trellis/skills/guru-team/packages/guru-finalize-task/runtime/owner.py`
- `trellis/skills/guru-team/packages/guru-finalize-task/tests/**`
- `trellis/skills/guru-team/packages/guru-review-task-publication/runtime/owner.py`
- `trellis/skills/guru-team/packages/guru-review-task-publication/tests/**`
- `.trellis/spec/workflow/{companion-scripts,quality-guidelines}.md`
- `trellis/presets/guru-team/spec/workflow/{companion-scripts,quality-guidelines}.md`
- 必要的 `trellis/{presets,workflows}/guru-team/README.md` 最小 operator wording
- preset apply 生成的 `.trellis/guru-team/**`、extension manifest 与声明平台投影
- `.trellis/tasks/08-27-312-workspace-boundary-merged-active-task/**`

任何 public schema/typed exit、runtime mapping schema、Finalizer transaction、Publication payload、
其它 Issue、tag/Release 或 Chengtuo 业务代码变更均超出本设计，需重新进入 owning route/授权。
