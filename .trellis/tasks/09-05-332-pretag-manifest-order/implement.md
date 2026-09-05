# #332 pre-tag manifest Skill 顺序修复实施计划

## 激活前门禁

1. 重读 live #332、fresh `origin/main`、task identity 与三份 planning artifacts，确认基线仍为
   `d4d9c07945786b50411fe900a9056f4444128e62`。
2. 修订 `issue-scope-ledger.json`：`primary_issue=#332`、`close_issues=[]`、
   `related_issues=[#332]`、`followup_issues=[]`，随后运行 task validator。
3. 完成 planning wording review、task-plan semantic approval、Architecture impact 与 RDT impact owner。
4. 只有用户在最终 planning summary 之后明确批准实施，才运行 `task.py start`。

## Phase 2 修改

1. 搜索 canonical manifest、installed manifest、registry、focused preset test 与 validator 中所有
   `active_skill_ids` 读取或断言，确认没有第三个顺序 owner。
2. 修改 `trellis/guru-team-extension.json`，把 `guru-restore-archived-task` 移到
   `guru-reconcile-task-base` 之后；其余 Skill ID 与 manifest 字段保持字节级不变。
3. 修改
   `trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`，从 installed
   registry 派生 active Skill ID 升序列表并与 installed public API 比较。
4. 运行：

   ```bash
   trellis/presets/guru-team/scripts/bash/apply.sh --repo .
   ```

5. 审查 apply 的完整 diff、文件 mode 与 sidecar。输出存在 `.new` 或 `.bak` 时停止并处理冲突；
   输出仅含预期 projection 时继续。

## 定向验证

1. 运行 focused preset test 中覆盖 public API contract 的测试类或精确测试方法。
2. 运行项目现有 canonical source manifest validator 与 installed extension validator。
3. 运行 managed byte/mode parity、declared platform projection 与 dogfood overlay drift 检查。
4. 用 `jq` 或项目现有 validator 证明：
   - active Skill ID 数量为 23；
   - canonical manifest 序列与 registry active ID 升序列表完全一致；
   - installed manifest 序列与同一 registry-derived 列表完全一致。
5. Corrective PR 合并后 fetch `origin/main`，冻结 `CANDIDATE_SHA`，再运行：

   ```bash
   CANDIDATE_SHA="$(git rev-parse refs/remotes/origin/main)"
   GURU_TEAM_THROWAWAY_SINGLE_REPO_COMPATIBILITY=1 \
   TRELLIS_WORKFLOW_SOURCE="gh:castbox/guru-trellis/trellis#${CANDIDATE_SHA}" \
   ./trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
   ```

6. 运行 `git diff --check`，检查 recursive `.new`、`.bak`、`__pycache__`、`.pyc`、未声明 sidecar
   与 owner-private residue，确认零残留。
7. 完成 `guru-check-task` semantic check。任一 required command 的 FAIL、SKIP、stale、cross-SHA、
   unknown、multiple 或 unmapped exit 立即停止，不进入 task commit 或 tag gate。

## 提交与发布边界

- task commit 前展示精确 staged paths、commit message 与预期结果，并取得独立确认。
- push、PR、merge 分别展示目标 ref 与副作用，并分别取得独立确认。
- Corrective PR 仅使用 `Refs #332`；不得使用 `Closes #332`。
- PR 合并后从 fresh `origin/main` 重新冻结 release candidate，并重跑受本修复影响的 pre-tag gate。
- Annotated tag、tag-pinned smoke、GitHub Release、Issue #332 closeout 与 cleanup 各自保留独立确认。

## 风险与回滚点

- 风险：focused test 若继续手写 manifest 顺序，后续 registry 新增或重排仍会形成双重 owner。
  控制：测试期望只从 installed registry 派生。
- 风险：直接编辑 `.trellis/guru-team/extension.json` 会绕过 installer ownership。
  控制：只修改 canonical source，再运行 preset apply。
- 风险：当前 ledger 会让 corrective PR 提前关闭 #332。
  控制：task 激活前完成 ledger 修订并重新验证。
- 回滚点：任何 validation 失败均保留在 task branch；不触碰 `origin/main` 或 immutable release state。
