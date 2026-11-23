# D2：source_locked 真实采用设计

## 1. 设计目标、需求承接与内容基线

本设计承接 D2 PRD 的 R1-R5、SC1-SC4 与 AC1-AC4。固定内容基线 B 是 D1 delivered candidate head `13d72b5425070fe841c1046d1e677d8323481eec`，来源为已合并 PR #909 / merge `df638d19d458bbab11642b5626d293df30075ea1`。本批 H 将由 installed after、知识复核和 TaskCommit 形成，PR 目标仍为 `main`。

Architecture candidate/final 结论将在本设计完成后独立产生；当前不预填 impact。

## 2. 当前系统、边界与目标差额

准备 checkout 的 canonical D1 源已为 `.11`，但 installed extension/source 和受管投影仍为 `.10`。目标差额主要由原 tools installer 通过 source_locked 更新产生，不手工复制到 `.trellis/guru-team/`、`.agents/skills/`、`.claude/skills/`、`.cursor/skills/` 或 managed specs。

Task 规划/runtime 和已归档任务允许保持现状；写入不得触碰 Task/archive/workspace/session 状态、用户配置、peer checkouts 和 common runtime pointers，除非原 tools owner明确声明所需的目标 local pointer。

## 3. 来源设计处置（唯一）

| 来源与原承诺 | 处置 | 落点与影响 | 上游处置 |
| --- | --- | --- | --- |
| Release contract：D1 delivered 后才进入真实采用 | retain | 本设计使用 D1 delivered source，不消费未交付或 dirty source | Completion/Creation 已完成 |
| Tools contract：source_locked、单目标、一次 prepare、原 owner recovery | retain | 全部采用和验证只通过原 tools public entry | 原 tools owner |
| Tools contract：Task/session/user/peer 保留 | retain | installed 写集之外内容保持；真实冲突停回原 owner | 原 tools owner |
| R724/D724/T724 与 ARCH-INT 系列：平台、来源与证据分层 | retain | 使用现有 managed projection 和验证入口，不新增规则 | 原 RDT/Architecture owners |
| 当前 `.10` installed 身份 | change | 由原 installer 更新为 `.11` 与 D1 source provenance | tools owner |

## 4. 模块、职责与设计取舍

唯一 source 与 target 是当前 Task checkout。原 `guru-upgrade-tools` 读取完整 clean canonical source、匹配 Fork build/API 和 exact target，生成 upstream 与 Guru 安装计划。后续 implementation/TaskCommit 不得绕过 tools owner 直接写受管副本。

平台选择从目标现状读取，默认已声明的 Claude、Codex、Cursor 投影完整更新。AGENTS 只由原 renderer 更新 Guru block；用户配置和未知本地修改按原冲突/保留语义处理。

## 5. 接口与数据

不新增公共接口。沿用 `source_ref=13d72b...`、`dependency_mode=source_locked`、当前 checkout，以及原 tools preview/prepare/invoke 输入。installed source provenance、CLI record、manifest 和 managed inventory 由 installer 生成。

## 6. 状态、顺序、正常与失败流程

1. Activation 后由原 tools owner刷新 preview，核来源、Fork、目标、平台、事务、保留项和真实差额。
2. prepare 一次，审查完整 frozen plan 和精确写删集合；没有 install 确认不得执行。
3. invoke 执行真实安装；partial failure 只沿原 recovery ref 续接。
4. 从目标自身 entry 验证 installed/native、source/CLI、完整投影、reapply/drift、保留和 sidecar。
5. 真实工程和知识结果齐备后，TaskCommit、constructor/begin_check、独立完整 Review、Publication 与 Merge。

来源失配、未知修改、未完事务、冲突、验证失败或恢复不确定均停回原 tools owner。

## 7. 恢复、兼容、迁移与集成

不使用普通 full apply、手工 manifest 或历史 Task 转换。操作前若发现 active maintenance/upgrade transaction，必须由原 owner判断。安装部分完成后只恢复同一 frozen operation；不准备第二计划或覆盖已完成写入。

managed source provenance 可以指向 D1 reviewed source，不要求自引 D2 HEAD。D2 installed after 与 D1 source 必须等价；真实 dirty 状态由原 source provenance 语义保留。

## 8. 验证设计

| 验证 | 要求/场景 | 入口与观察 | 证明边界 |
| --- | --- | --- | --- |
| D2-V1 | R1/R2 | tools preview/prepare：source、Fork、target、平台、事务、完整 plan | 只读事实，不证明安装 |
| D2-V2 | R2/R3 | tools invoke + recovery：`tools_upgraded` 和 installed provenance | 原 owner 结果不等于独立 Review |
| D2-V3 | R2/R4 | target resolver、installed/native、validator、完整 bytes/mode、reapply/drift | 不声称客户端或业务生产行为 |
| D2-V4 | R3 | Task/session/user/peer/common preserve 与 sidecar 扫描 | 保留事实不等于功能测试 |
| D2-V5 | R5 | TaskCommit、固定 B..H、独立 Review、Publication/Merge | D2 delivered 不等于 Task Completion |

## 9. Canonical 引用、本轮差额与实际未决项

RDT `codex-skill-distribution`、`native-compatibility` 与 Architecture `ARCH-INT-009/014/015` 提供现有采用合同。Docs SSOT Plan 预期为 `no_docs_update_needed`，除非真实 adopted bytes 暴露 current 指南差额；若有，先回 Author 更新本计划和原 writer。
