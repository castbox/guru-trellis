# #635 Architecture 隔离拟写

状态：已在原 final_integration 写入共享正文；本目录保留原拟写来源，正常读取使用下表实际目标。Task `635-portable-lifecycle` / generation `0`，Delivery `826d09cb-22d6-4950-90c8-3bbf8df8d8ea`。固定 before 为 `7a7b60743499653ffeb81f6b31e627a02c33f579:docs/architecture/`；authority、constitution、change contract 分别为 `guru-trellis-architecture`、`guru-trellis-design-constitution-v1`、`guru-trellis-architecture-change-contract-v1`。change path 为 `legacy_boundary_convergence`。

下表只定位完整拟写目标及关系，不是第二 current、gate 或实现证据。原 task-owned Architecture 贡献和必要 ADR 保留其已接受规划归属；此目录将其决定展开为完整正文供候选审查。

| 实际最终目标 | 完整 proposed 正文 | 变化范围 |
| --- | --- | --- |
| `docs/architecture/03-domains/ownership.md` | [DOMAIN](proposed/docs/architecture/03-domains/ownership.md) | 原 DOM028/030/032/043/044/054 原位收敛及 DOM060 完整跨环境职责 |
| `docs/architecture/04-integrations/distribution.md` | [INTEGRATION](proposed/docs/architecture/04-integrations/distribution.md) | INT033/060 精确历史/来源职责与 INT063 matching 分发 |
| `docs/architecture/06-governance/rules.md` | [GOVERNANCE](proposed/docs/architecture/06-governance/rules.md) | GOV009 最小共享 Closure、原恢复与 shared/local 边界 |
| `docs/architecture/adr/portable-shared-lifecycle.md` | [必要 ADR](proposed/docs/architecture/adr/portable-shared-lifecycle.md) | ADR-PORTABLE-SHARED-LIFECYCLE，具名窄替代与兼容退出 |
| `docs/architecture/adr/README.md` | [ADR 导航](proposed/docs/architecture/adr/README.md) | 只增加新决定 locator 及前驱关系 |

RDT 关系为 `docs/{requirements,design,test}/current/task-delivery-lifecycle.md` 与 `completion-closure.md`，其原 owner 的完整隔离正文位于 `docs/requirements-design-test-contributions/635-portable-lifecycle/proposed/`。实际验证和未验证边界唯一由同贡献的 `test.md` 持有；此目录不重复测试历史或宣布 V1–V8/安装通过。

shared CURRENT、总入口、宪法、GAP 与 project-check 协议在本次准备保持不变。普通 promotion 保留稳定 identities。完整候选先经独立 Architecture/候选 Check，原 Check 合法回 implementation 后，原 Architecture final_integration 重读 live targets/expected-current 并写入完整有效正文；随后 readback、刷新 candidate 和最终质量链。此提案存在不构成 Phase 2 pass、promotion 或授权。
