# 技术设计

## 1. 设计结论

在现有 schema 2.0 closeout plan 内补充一个闭合的 reviewed tracked content binding 集合，并让 plan builder 每次从 live Git index 重建 tracked/untracked 分类。continuity、verification fallback、archive transaction 和 public wrapper 都消费同一 plan projection，不新增 public typed exit 或第二条迁移事务。

## 2. 现有数据流

```text
Publication reviewed facts
        |
        v
build_closeout_plan
  existing projection -> 复用历史 tracked/untracked 分类
        |
        +--> pre-move continuity -> transaction-parent blob / 固定 inputs
        |
        +--> verification fallback -> untracked outputs only
        |
        +--> public wrapper checker context
```

历史分类错误会同时污染三个直接 consumer；单独放宽其中任一 checker 会造成 plan 与 transaction 不一致。

## 3. 目标数据模型

### 3.1 Projection 分类

- `move_paths`：保留既有 immutable move set 和新增文件保护语义。
- `tracked_move_paths`：始终由 `git ls-files -- <active task locator>` 与 `move_paths` 求交得到。
- `untracked_archive_outputs`：始终由 `move_paths - tracked_move_paths` 推导。
- 既有 schema 2.0 plan 的上述两个字段只作为 migration 输入，不再作为 live 分类权威。

### 3.2 Reviewed tracked content bindings

在 `projection` 增加闭合数组，每个元素固定包含以下三个字段：

- `path`：task-relative path，必须属于 `tracked_move_paths`；
- `mode`：`100644` 或 `100755`；
- `sha256`：Finalizer 语义审核时当前工作树文件的精确 SHA-256。

集合覆盖所有与 transaction-parent blob 不同的 tracked move path。没有差异的 tracked path 不需要重复绑定；出现差异但无绑定、绑定重复、path 越界、mode 或 digest 不匹配均 fail closed。

这组绑定是 immutable plan 的私有 transaction 数据，不进入 public DTO，也不作为授权或 authenticity boundary。

### 3.3 Metadata intermediate

包括 `context-discovery.json`、`phase-0-disposition-ledger.tsv` 在内的非 durable metadata 仍由既有 archive pruning 删除。删除前它们必须：

1. 位于 `move_paths`；
2. 依据 Git index 正确分类；
3. 若相对 transaction parent 有变化，则匹配 reviewed tracked binding；
4. 进入同一 official `task.py archive --no-commit` transaction 后按现有 retained set 裁剪。

因此“可裁剪”不表示“跳过连续性校验”。

## 4. 行为设计

### 4.1 Plan 构建与迁移规范化

1. 读取并校验 existing schema 2.0 plan。
2. 保留 existing `move_paths`、archive locator 和 summary template 这三类不可随意扩张的 immutable 内容。
3. 读取 live Git index，重建 tracked/untracked 分类。
4. 对 tracked move paths 比较 transaction-parent blob 与当前工作树 bytes/mode，生成最小 reviewed binding 集合。
5. 重算 plan digest，并将“仅由已知 schema 2.0 migration normalization 引起的变化”与普通 protected-input drift 分开识别。
6. 仅当前 active task、相同 issue/repo/base/head/branch-review identity、相同 move set 和正常 metadata tail 可进入该迁移路径；其他 plan 差异继续阻塞。

迁移规范化由 Finalizer owner 重新审查当前 plan；不重新进入 Branch Review，不创建新 public route。

### 4.2 Pre-move continuity

对每个 tracked move path：

1. 验证 transaction-parent Git entry 为普通 blob，mode 合法；
2. 当前 bytes/mode 与 parent 一致时直接通过；
3. 否则要求 plan 中存在同 path binding，且当前 bytes/mode 精确匹配；
4. 原有固定 `inputs` 兼容逻辑可投影到同一内容校验，避免两套互相冲突的 allowlist。

### 4.3 Verification fallback

`finalization_uncommitted_output_paths` 返回：

- 当前存在的真实 untracked archive outputs；
- 当前存在且精确匹配 plan binding 的 tracked metadata paths。

verification owner artifact 仍按既有规则单独加入。任何额外 dirty path 或 binding drift 均产生原有 fail-closed error。

### 4.4 Public wrapper

public wrapper 必须用与 `cmd_check_finalization_gate` 相同的 plan-derived checker 参数和 gate path 调用同一个 objective checker。checker-passed 的 `blocked` / `evidence_ready` route 直接进入现有 blocked output schema；只有 checker 真正失败时才返回 `owner_result_not_checked`。

### 4.5 Existing Draft PR

迁移规范化完成后继续现有 unique Draft recovery：

- 复用相同 repo/head/base 的唯一 Draft；
- 如当前 plan 的 title/body 发生受控变化，按既有 convergence 逻辑更新同一 Draft；
- 不创建第二个 PR；
- 不调用 Branch Review；
- archive 后仍要求 local HEAD、remote HEAD、PR head 三方一致。

## 5. 修改面

### Canonical

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- `trellis/workflows/guru-team/schemas/closeout-plan.schema.json`
- `trellis/skills/guru-team/packages/guru-finalize-task/schemas/closeout-plan.schema.json`
- `trellis/skills/guru-team/packages/guru-finalize-task/references/contract.md`
- 当新增 binding 或 wrapper 规则无法仅由 Finalizer package contract 完整表达时，同步更新 `.trellis/spec/workflow/data-contracts.md` 与 `companion-scripts.md` 的共享 durable contract。

### 生成/安装副本

通过 `trellis/presets/guru-team/scripts/bash/apply.sh --repo .` 同步，不把 dogfood 副本作为源头：

- `.trellis/guru-team/scripts/python/guru_team_trellis.py`
- `.trellis/guru-team/skills/packages/guru-finalize-task/**`
- `.agents/skills/guru-finalize-task/**`
- `.codex/skills/guru-finalize-task/**`
- 其他 preset 声明的平台副本。

## 6. 兼容性

- public skill id、Interface 1.3 profiles、六个 typed exits 和 consumer mappings 不变。
- schema version 保持 `2.0`，新增字段必须由 builder 生成并由 validator 闭合校验；历史 schema 2.0 plan 通过专用 migration normalization 升级。
- 常规新 plan 仍将 `closeout-plan.json` 与 `finish-summary.json` 归为初始 untracked；只有 Git index 已跟踪 legacy plan 时才重新分类。
- unexpected path、stale content、ambiguous Draft 和 HEAD mismatch 四项现有阻塞条件保持不变。

## 7. Docs SSOT Plan

- 策略：`ssot_first`。
- 主 SSOT：`trellis/skills/guru-team/packages/guru-finalize-task/references/contract.md`，补充迁移 plan 分类、reviewed tracked binding、fallback 与 existing Draft resume 合同。
- 共享确定性规则：仅在现有文字不足时更新 `.trellis/spec/workflow/data-contracts.md` / `companion-scripts.md`，不复制完整 Finalizer 合同。
- `SKILL.md`、workflow markers、public interface 与 README 不改变语义时不修改。
- canonical 修改后由 preset installer 生成安装副本，drift checker 证明一致。

## 8. 失败处理

- Git index 无法读取、existing plan 不是合法 schema 2.0，或 migration delta 超出第 4.1 节列出的身份、分类和绑定变化：`blocked`。
- binding path/mode/digest 不闭合或当前内容漂移：`blocked`。
- Draft 缺失、closed、replaced 或 ambiguous：沿用现有 `blocked`。
- 网络验证失败：只有在 plan-owned dirty set 精确匹配时进入既有 evidence-ready/blocked route，不改变 verification owner 的语义责任。
