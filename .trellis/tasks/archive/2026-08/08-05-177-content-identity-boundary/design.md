# #177 Technical Design

## 1. 设计结论

本变更采用“统一内容指纹 + Git commit anchor + owner-private gate”三层模型：

1. `reviewed_content_identity()` 负责唯一内容集合与指纹算法。
2. Git HEAD 只定位 review range、commit parent、finding ancestry 和 remote verification commit。
3. Phase 2、Branch Review、Publication、Finalizer 的 recorder/checker 直接重算内容指纹；digest 不进入跨 Skill 公共 DTO，也不替代 semantic gate。

该模型保留现有 Git 因果链，同时取消“HEAD 变化代表内容变化”和“metadata basename allowlist 代表 freshness”的错误耦合。

## 2. Shared Reviewed-Content Engine

### 2.1 API

在 `guru_team_trellis.py` 增加以下共享函数：

```text
reviewed_content_metadata_path(path) -> bool
reviewed_content_tree_entries(root, commit) -> map[path, entry]
reviewed_content_worktree_overlays(root) -> list[overlay]
reviewed_content_identity(root, commit="HEAD", include_worktree=True) -> {
  algorithm: "guru-reviewed-content-1.0",
  sha256: <64 hex>
}
```

所有 freshness owner 只能调用该 API，不再维护各自的 metadata allowlist 或内容 hash 算法。

### 2.2 Tree 与 worktree 合成

1. 使用 `git ls-tree -r -z --full-tree <commit>` 读取完整 commit tree。
2. 过滤 `.trellis/tasks/**`、`.trellis/workspace/**`、`.trellis/.runtime/**` 与 AI-first OS noise。
3. 使用现有 `capture_task_commit_snapshot()` 读取 staged、unstaged、rename、copy、delete、untracked 状态。
4. 删除 overlay 移除旧 path；rename 同时移除 `renamed_from`；copy 保留 source。
5. regular file 与 symlink 使用 `git hash-object --stdin` 计算未来 commit 一致的 blob id；mode 取 `100644`、`100755`、`120000`。
6. gitlink 复用现有 clean worktree identity，条目绑定 mode `160000` 与 gitlink HEAD。
7. 对 `{algorithm, entries:[{path,mode,oid}]}` 做 canonical JSON SHA-256。

异常路径、unmerged index、未初始化或 dirty gitlink、无法读取 object、非法 UTF-8 path 均 fail closed。并发写入、hostile path 和 crash recovery 不进入本 Issue。

## 3. Current-only Gate 合同

### 3.1 Phase 2

- `guru-phase2-check-4.0` 使用 `reviewed_content_sha256` 和 `phase2_capture_commit`；不保留旧字段或旧 schema reader。
- `materialize_phase2_check_payload()` 在 semantic review 后记录统一 identity。
- `validate_phase2_check()` 不再要求 HEAD 一致；它验证当前 identity、dirty reviewed path coverage、schema、semantic result 和 consumer。
- schema 不匹配走统一 invalid-input fail-closed，不实现版本特定 re-entry。

### 3.2 Task Commit

- Phase 2 passed DTO 与 Task Commit input 升级 public schema id，使用 `phase2_commit_anchor`。
- entry precondition 接受 `phase2_commit_anchor` 为当前 HEAD 或当前 HEAD 的 ancestor，但必须满足：Phase 2 checker pass、anchor commit identity 与当前 worktree identity 完全一致、当前 dirty reviewed paths 仍被 Phase 2 覆盖。
- candidate 的 `pre_commit_head` 取执行时当前 HEAD；commit parent 与 `pre_commit_head` 一致。
- task metadata-only descendant 不进入 exact staged reviewed-content 集合；本 task 自身 task docs 仍由 task commit 的 scope/staging contract独立管理。

### 3.3 Branch Review

- `guru-review-gate-3.0` 使用 owner-private `reviewed_content_sha256` 与 `review_commit`。
- recorder 在完整 current range semantic review 后计算 identity。
- checker 对比 gate identity、review commit identity与当前 worktree identity。
- 删除 metadata descendant allowlist、旧 schema 分支和版本特定 re-entry。

### 3.4 Publication 与 Finalizer

- Branch Review wrapper 在当前 checker 和 typed-output schema 均通过后删除自己的
  private checkpoint。Publication entry 只消费 `passed` DTO 的
  `branch_review_commit`，以该 commit 的 reviewed-content identity 为 anchor 并校验
  live continuity；不重开 Branch Review checker 或 private checkpoint。
- Branch Review passed DTO、Publication input/output 与 Finalizer input 升级 public schema id，统一使用 `branch_review_commit` 作为当前 Git anchor。
- Finalizer 初次进入从 Publication `ready` DTO 取 anchor；已有 immutable closeout
  plan 的 re-entry/recovery 从 plan 取 anchor。无 DTO 且无 plan 时 fail closed；两条
  路径均不读取 Branch Review private checkpoint。
- Finalizer 的 `review_branch_content_continuity_errors()` 改为统一 identity 比较；remote verification、review range 和 finding ancestry 继续使用 commit anchor。
- metadata commit 后 current HEAD 变化不会改变 content identity；任一纳入路径变化会返回现有 stale/task-work 路由。

## 4. Scope-only Ledger 2.0

### 4.1 Schema

在 `guru-create-task-workspace` package 增加 `issue-scope-ledger.schema.json`：

```json
{
  "schema_version": "2.0",
  "primary_issue": {"number": 177, "url": "...", "title": "...", "reason": "..."},
  "close_issues": [],
  "related_issues": [],
  "followup_issues": []
}
```

schema 关闭 additional properties，数组按 issue number 唯一，primary issue 必须出现在 close/related/followup 中的恰当单一 disposition。

### 4.2 Runtime

- `issue_entry()` 不再生成 `acceptance_evidence`。
- task workspace executor 只写 schema 2.0 scope Ledger。
- `load_issue_scope_ledger()` 只接受 schema 2.0；其它 shape 走统一 invalid-input fail-closed。
- publish validation 用 Phase 2、Branch Review 和 Publication gate 判断验收，不再调用 `issue_has_evidence()`。
- `record_marketplace_machine_evidence()` 及 ledger augmentation 路径退出 active flow；marketplace 结果只保留在 `marketplace-verification.json` 和 verification owner result。
- closeout plan 绑定 scope-only Ledger bytes；verification artifact 单独绑定其 repo、branch、reviewed commit 和 command result。

## 5. Breaking Current Contract

- 受影响 public/private schema 使用新 id；`checked_head`、`reviewed_content_head` 由 `phase2_commit_anchor`、`phase2_capture_commit`、`review_commit`、`branch_review_commit` 取代。
- 删除旧 artifact reader、projection、re-entry、allowlist、alias、fixture、eval 和专用测试；旧输入由当前 schema 校验统一拒绝。
- Ledger 只存在 2.0 active contract，不读取或投影 1.0。
- stable Skill id、external exit id 和 workflow target id 保持不变；受影响 public schema id 明确升级。
- 升级说明只要求重新运行当前 owner 生成新 artifact；不提供 migration executor 或 compatibility test。
- Finalizer transaction 顺序不重构，只移除 Ledger verification 写入并改用独立 artifact。

## 6. Canonical 与生成面

先修改：

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 与 unit tests；
- `trellis/skills/guru-team/packages/{guru-check-task,guru-create-task-commit,guru-review-branch,guru-review-task-publication,guru-finalize-task,guru-create-task-workspace}`；
- `trellis/skills/guru-team/tests/test_finish_family_integration.py`；
- canonical workflow/spec/README 与 preset manifest/source。

随后运行 preset `apply.sh --repo .` 生成 `.trellis/guru-team/**`、`.agents/skills/**`、`.codex/skills/**`、`.claude/skills/**`、`.cursor/skills/**` 和 overlay-owned入口。任何 `.new`、`.bak` 必须逐项处理。

## 7. Docs SSOT Plan

| SSOT | 修订内容 | 派生消费者 |
| --- | --- | --- |
| `.trellis/spec/workflow/data-contracts.md` | reviewed-content identity、Ledger 2.0、verification ownership | Skill contract、schema、runtime tests |
| `.trellis/spec/workflow/companion-scripts.md` | shared identity calculator、recorder/checker 边界 | runtime implementation、wrapper tests |
| `.trellis/spec/workflow/quality-guidelines.md` | metadata/content freshness regression matrix | Phase 2、Branch、finish integration tests |
| `.trellis/spec/workflow/skill-package-contract.md` | private identity、current-only public commit anchors 与 breaking schema ids | package interfaces、examples、evals |
| `.trellis/spec/workflow/workflow-contract.md` | Phase 2 到 Finalizer 的 freshness route | canonical/dogfood workflow 文案 |
| `.trellis/spec/preset/installer.md` | 新 schema/package 分发与 update/reapply | extension manifest、throwaway verifier |
| `trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md` | 用户可见 identity 与 scope Ledger 行为 | 安装与维护说明 |

不新增独立结果文档；task planning docs 只承接本次需求、设计和测试计划。

## 8. 风险与控制

- 大仓库性能：tree 只读取一次，worktree 只 hash dirty/untracked bytes；测试固定 subprocess 数量与稳定输出。
- path 分类遗漏：单一 classifier 单测覆盖根路径、嵌套路径、相似前缀和纳入的 `.trellis/workflow.md`、`.trellis/spec/**`。
- 旧输入混入：当前 schema 统一拒绝，active runtime 不包含任何旧版本识别或迁移分支。
- Finalizer 回归：finish-family integration 覆盖 marketplace required/not-required、metadata commit、reviewed content drift 和 archive projection。
