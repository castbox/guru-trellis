# Design

## Boundary

本任务是公开文档 projection 的等价 owner 修正。active Requirements 已持有正确
authority，不创建新的 RDT/Architecture contract，也不改变运行时行为。

## Wording Mapping

三个目标句子保持各自语言与上下文，仅替换 owner 主体：

| Path | Current owner | Target owner |
| --- | --- | --- |
| `README.md` | `#267` | 独立的重构前稳定版 Release Issue（#304） |
| `trellis/workflows/guru-team/README.md` | `#267` | 独立的重构前稳定版 Release Issue（#304） |
| `trellis/presets/guru-team/README.md` | `Issue #267` | the independent pre-refactor stable Release Issue (#304) |

owner 替换不改写版本、验证结果、provenance classification、stable-source 状态或
安装示例。英文句子使用 `exclusively owns`，中文句子使用“只由...拥有”，两者表达
同一排他归属。

## Docs SSOT Plan

- Strategy：`direct_sync` 到三个公开 README projection。
- Durable authority：`docs/requirements/README.md` 保持不变，继续作为 current
  Requirements 入口和 owner 依据。
- Task-local evidence：`prd.md`、`design.md`、`implement.md` 与
  `issue-scope-ledger.json`。
- RDT impact：`no_change`，不新增 contribution 或 promotion。
- Architecture impact：`no_architecture_impact`，不新增 contribution 或 ADR。

## Compatibility And Rollback

- 无 public API、schema、CLI、installer、manifest、managed asset 或 runtime 变化。
- 无数据、配置或状态迁移。
- 回滚点是三个独立句子；任一位置不一致时整项文案修正不通过。
