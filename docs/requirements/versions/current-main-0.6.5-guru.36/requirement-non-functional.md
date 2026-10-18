# 非功能需求与边界

版本：`current-main-0.6.5-guru.36`；状态：`superseded`。

- `NFR-001`：canonical source 是长期源头；dogfood 与平台副本必须可从 preset/overlay 重建。
- `NFR-002`：public DTO 只携带唯一 consumer 必需的最小 identity/freshness；Git/live 可重建事实与授权不得持久化。
- `NFR-003`：unknown/multiple/unmapped exit、stale identity、缺失 mandatory Skill 必须 fail closed。
- `NFR-004`：验证按 Issue ownership 最小化；普通 docs/spec Bootstrap 不运行完整多平台或 exact release-candidate matrix。
- `NFR-005`：日志、Issue、PR、task、evidence 不得泄露 secret、token、数据库 URL、客户数据。

## 兼容与未验证边界

| 边界 | 当前状态 | Owner |
| --- | --- | --- |
| Trellis CLI `0.6.5` | `code_recovered`：manifest 标为 target/tested | current source |
| Trellis CLI `0.6.15` upgrade/update | `unverified` | #260/#267 |
| replacement release exact candidate | local-current representative Throwaway PASS；exact committed/remote candidate、tag-pinned smoke 与 live downstream 仍 `unverified` | #275 |
| 完整多平台 Throwaway matrix | `unverified` | #260/#267 |
| candidate `0.6.5-guru.36` / `v0.6.5-guru.10` release | `unverified`，不得称已发布 | #275 |

普通 task 的文档增量进入 `docs/requirements-design-test-contributions/<task-ref>/` 或经 semantic owner 判定的 narrow direct sync；两个并行 task 不写同一个 shared current 文件。Architecture 变化使用独立 impact/promotion route。该规则是维护责任边界，不是锁或并发协议。
