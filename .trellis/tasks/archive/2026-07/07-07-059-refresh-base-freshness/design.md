# 设计：planner 阶段刷新 base freshness

## 范围

本设计覆盖 Guru Team `prepare-task` 的 Phase 0 intake/preflight freshness 证据链，主要涉及：

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- `trellis/workflows/guru-team/schemas/intake-handoff.schema.json`
- `trellis/workflows/guru-team/workflow.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`
- dogfood 安装副本 `.trellis/guru-team/*` 与 `.trellis/workflow.md`

## 当前问题

`cmd_prepare()` 目前按是否创建 workspace 分流：

- executor 路径：`ensure_base_freshness()`，会 `git fetch origin <base>`，必要时安全 fast-forward，本地 base 分叉时 fail closed。
- planner-only 路径：`inspect_base_freshness()`，只比较本地 base 与本地 `origin/<base>` 缓存，并返回 `fetch_performed: false`。

这会让过期 remote-tracking ref 被当成真实远端证据，进而在 handoff review 中出现误导性的 `fresh: true`。

## 目标行为

### Planner-only

默认 planner-only 也必须刷新或确认远端状态。推荐实现是新增或调整一个只刷新 remote-tracking ref 的 helper：

1. 解析 base short name 与 remote ref。
2. 读取 `local_head_before`。
3. 执行 `git fetch origin <base>` 刷新 `origin/<base>`。
4. 读取刷新后的 `remote_head`。
5. 读取 `local_head_after`，但 planner-only 不 fast-forward 本地 base。
6. 根据关系输出状态：
   - `fresh`: local base 与 remote head 相同，或只有 remote head 且本地 base 不存在。
   - `stale`: local base 是 remote ref 的祖先，本地落后但可 executor 安全快进。
   - `diverged`: local base 与 remote ref 不是祖先关系。
   - `remote_ref_missing` / `fetch_failed`: 远端无法确认。
7. `base_ref_for_worktree` 对 planner-only 仍可给出后续 workspace 参考；实际创建必须继续走 executor 的 `ensure_base_freshness()`。

### Executor

保持现有 `ensure_base_freshness()` 作为创建 worktree/task 前的强校验入口：

- 先 `git fetch`。
- 如果 local base 落后且可 fast-forward，安全快进或 `branch -f`。
- 如果分叉或无法确认，fail closed。

Planner-only 的刷新不能替代 executor 刷新；两者都保留，是为了避免 handoff 与实际创建之间远端状态漂移。

## 数据合同

`preflight.base_freshness` 继续保持 permissive schema，新增字段必须向后兼容。建议字段：

- `fetch_performed: true`：planner-only 也已刷新 remote-tracking ref。
- `fast_forwarded: false`：planner-only 不修改本地 base。
- `fresh: bool`：仅在已刷新后计算。
- `status: fresh | stale | diverged | remote_ref_missing | fetch_failed | remote_only`。
- `base_ref_for_worktree`：后续创建的参考 ref；executor 会重新确认。

如果实现选择直接复用 `ensure_base_freshness()`，必须避免 planner-only 修改本地 base；因此不应让 planner-only 调用会 fast-forward 的 helper。

## 文档与同步

- workflow 文案要明确 planner-only `preflight.base_freshness` 也应来自已刷新或确认的远端状态。
- README/schema 要避免只说 executor 刷新 base。
- 修改 canonical 后同步 dogfood 安装副本，不把 `.trellis/guru-team/` 当作唯一源头。
- 本任务不修改 overlay 行为；若 overlay drift check 发现安装副本不一致，按 canonical 重新应用 preset 并处理 `.new/.bak`。

## 风险与回滚

- 风险 1：planner-only 从纯读本地缓存变成会执行 `git fetch`，需要网络与 remote 可用。失败时应 fail closed，而不是给出伪 fresh。
- 风险 2：测试中 mock 调用顺序会变化，需要精准断言 planner-only 调用刷新 helper。
- 回滚方式：撤回 helper 与文档/测试改动，恢复 planner-only 只 inspect 本地缓存；但这会重新暴露 #59 缺陷。

## Durable Docs SSOT

本任务会更新 durable workflow/preset 文档与 schema 描述。任务 artifact 仅记录本次实现证据，不作为长期唯一来源。
