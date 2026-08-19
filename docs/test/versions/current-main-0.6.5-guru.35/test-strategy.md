# 当前测试策略

版本：`current-main-0.6.5-guru.35`；状态：`active`。

## Evidence 分层

| ID | 层级 | 能证明 | 不能替代 |
| --- | --- | --- | --- |
| `TST-001` | static/docs | 格式、链接、结构、scope、context 可加载 | runtime 行为 |
| `TST-002` | package/unit | interface/schema/runtime 局部合同 | installed graph 与外部服务 |
| `TST-003` | semantic eval/review | normal-path 语义、finding 与 route 充分性 | deterministic side effect |
| `TST-004` | integration | producer -> consumer、task/history/recovery 数据流 | 多平台安装 |
| `TST-005` | distribution/throwaway | canonical/installed/platform/preset 实际一致 | 未执行的 upgrade/release candidate |
| `TST-006` | SSOT | RDT/Architecture/Bootstrap locator、traceability、freshness | 产品 runtime |
| `TST-007` | compatibility | public id/schema/exit/command closure | 未来版本兼容，除非 exact matrix |
| `TST-008` | live/external/release | GitHub、tag、Release、exact candidate 与目标环境 | static/unit 或 skipped test |
| `TST-009` | business parallel matrix | 两个 task 的 worktree/contribution/Finish/cleanup 隔离 | 单 task package test |
| `TST-010` | history/acceptance | task index、archive、finish-summary、retained ref 与查询可发现性 | PR body 声明 |
| `TST-011` | recovery | base/provider stale、partial recovery、re-entry 与零重复副作用 | happy-path static check |

## 核心场景

- `SCN-001`：标准 Intake 从 current base/context 到唯一 workspace，无 pre-task tracked residue。
- `SCN-002`：Planning/Phase 2/commit/review 对 content freshness fail closed，并支持 finding fix + fresh final review。
- `SCN-003`：Finalization/merge 使用 expected HEAD，archive/history 可发现且 close issues 精确。
- `SCN-004`：base/provider evolution 自动进入唯一 reconcile/recovery route，不复用 stale evidence。
- `SCN-005`：canonical、dogfood、installed、Shared/Codex/Claude/Cursor byte/mode/graph 一致；preset reapply 不留未知 sidecar。
- `SCN-006`：RDT 与 Architecture version/status/traceability 对齐；Bootstrap projection 最小且不形成第三 authority。
- `SCN-007`：同一 clean base 的 A/B task 使用独立 worktree、branch、task 与 contribution；
  Planning/Check/Review/Finish/cleanup 不读写对方 tracked state，也不要求合并对方 bookkeeping commit。
- `SCN-008`：provider failure、stale evidence 与 partial finalization 由 exact owner 恢复；已发生副作用
  不重复，unsupported/mismatch fail closed。
- `CASE-001`：每个 active interface 的 external exit 恰有唯一 consumer 或 stop，registry/interface/workflow 闭包。
- `CASE-002`：semantic gate 发生在 recorder/validator 前，脚本不接收或持久化授权。

## 选择规则

先读取 `.trellis/spec/workflow/quality-guidelines.md` 的 `Validation Scope Ownership`。普通 feature/docs/spec Issue 运行与 accepted scope 相关的最小可靠集合；完整多平台 Throwaway 只属于专项兼容/upgrade/release Issue。任何 SKIP、未配置 live 环境或历史 PR 声明都明确写成 `unverified`。

`SCN-007` 的 current-version business parallel matrix 与 `SCN-008` 的 live/provider variants 若未由
当前 focused evidence 覆盖，Test Plan 必须标记 `unverified` 并交给明确 consumer；不能用本次
docs link/structure PASS 代替。
