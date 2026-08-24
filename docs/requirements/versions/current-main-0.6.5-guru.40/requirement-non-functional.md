# 非功能需求与边界

版本：`current-main-0.6.5-guru.40`；状态：`active`。

- `NFR-001`：canonical source 是长期源头；dogfood 与平台副本必须可从 preset/overlay 重建。
- `NFR-002`：public DTO 只携带唯一 consumer 必需的最小 identity/freshness；Git/live 可重建事实与授权不得持久化。
- `NFR-003`：unknown/multiple/unmapped exit、stale identity、缺失 mandatory Skill 必须 fail closed。
- `NFR-004`：验证按 Issue ownership 最小化；普通 docs/spec Bootstrap 不运行完整多平台或 exact release-candidate matrix。
- `NFR-005`：日志、Issue、PR、task、evidence 不得泄露 secret、token、数据库 URL、客户数据。

## 兼容与未验证边界

| 边界 | 当前状态 | Owner |
| --- | --- | --- |
| Trellis CLI `0.6.15` source/dogfood | `verified`：manifest、project version、ownership 与 drift gate | #260 current source |
| `0.6.5 -> 0.6.15` official migration | `verified`：三个 existing platform cell | #260 |
| replacement release `v0.6.5-guru.10` | `published`：annotated tag、zero-asset non-prerelease Release 与 consumer proof | #275 historical baseline |
| 完整多平台 Throwaway matrix | `verified`：`claude|codex|cursor × clean|existing` 6/6，sidecar/unknown drift 均为 0 | #260 |
| current candidate `v0.6.15-guru.1` / extension `0.6.5-guru.37` / Trellis `0.6.15` stable release | `unverified`，不得称已发布 | 独立的重构前稳定版 Release Issue |
| workflow source | `public_plus_local_candidate`；证明 public marketplace + exact local candidate compatibility，不证明 `.37` tag-pinned install | #260 / 重构前稳定版 Release boundary |

普通 task 的文档增量进入 `docs/requirements-design-test-contributions/<task-ref>/` 或经 semantic owner 判定的 narrow direct sync；两个并行 task 不写同一个 shared current 文件。Architecture 变化使用独立 impact/promotion route。该规则是维护责任边界，不是锁或并发协议。
