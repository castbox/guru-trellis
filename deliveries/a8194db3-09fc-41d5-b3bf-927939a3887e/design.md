# tools-only 失效 prunable peer 处理设计

## 1. 设计目标、需求承接与内容基线

本方案承接 Task REQ-01 至 REQ-04、AC-01 至 AC-05 和 Delivery PRD REQ-01 至 REQ-05。目标是从新 tools-only 操作的 peer 集合中只排除 Git 已标记 `prunable` 且 checkout 根 `.git` 路径项不存在的注册。其它 peer 保持原有路径与检查。

- Task：`TASK-759-PRUNABLE-PEER`，generation `0`。
- Delivery：`a8194db3-09fc-41d5-b3bf-927939a3887e`，phase `planning`。
- Development baseline B：`main@8c158381b5bdb61fd961cbb89e23c2d1f659c9aa`，来源为本 Task 创建时已审阅的 main HEAD；当前 checkout HEAD 与该 B 一致。
- PR target：`main`。B、当前内容范围和 PR target 是独立事实。
- 当前 Architecture assessment：`baseline_current`，`no_architecture_impact`；baseline identity `guru-trellis-architecture`，constitution identity `guru-trellis-design-constitution-v1`。该 assessment 不创建 Architecture contribution 或 ADR。

## 2. 当前系统、边界与目标差额

当前 `guru-upgrade-tools/runtime/tools_owner.py` 的 `peers()` 从 `git worktree list --porcelain` 只提取 `worktree` 路径，并丢弃同一记录的 `prunable` 属性。`isolated_layout()` 和 `peer_pointers()` 都消费这组路径。`peer_pointers()` 对每个 peer 调用 `git rev-parse --absolute-git-dir`，随后读取 pointer 状态并检查 peer 自身可用的 runtime。

目标是在 `peers()` 构造可检查路径时保留 porcelain 记录的 `prunable` 值，并仅排除同时满足 `prunable=true` 与 `os.path.lexists(checkout / '.git') == false` 的记录。使用路径项存在性判断，避免把仍存在但目标无效的 `.git` 符号链接当作“路径项不存在”。被排除的 peer 目录及其文件只读保留，不做清理。

`isolated_layout()` 与 `peer_pointers()` 继续消费同一过滤后 peer 集合。正常 peer、`.git` 仍存在的 prunable peer、以及未标 prunable 的损坏 peer都保留在集合中；后者继续由原 `git rev-parse` 路径失败关闭。

## 3. 来源设计处置（唯一）

Issue #759 与已接受 Task/Delivery PRD 定义行为条件、失败边界和非目标，没有提供规范性来源设计或实现机制。本 Delivery 不建立来源设计处置矩阵，不修改共享 Architecture authority。

## 4. 模块、职责与设计取舍

唯一生产改动位于 `trellis/skills/guru-team/packages/guru-upgrade-tools/runtime/tools_owner.py` 的 `peers()`。解析 `--porcelain` 输出时按每个空行分隔的 worktree 记录关联路径和 `prunable` 标志；若 `prunable` 行存在，且该路径下 `.git` 目录项确实不存在，则不加入 peers 返回值。其它记录以解析后的 `Path` 返回。

该判断属于 tools owner 的本地 Git registration 读取职责，不读取 peer Task、session 或业务索引。不得仅因 `rev-parse` 返回非零而忽略 peer；也不得仅因 prunable 标记就略过仍有 `.git` 项的 peer。解析后的每个非失效 peer 继续经过原有 isolation、pointer 与 runtime 读取。

测试改动位于 `trellis/skills/guru-team/packages/guru-upgrade-tools/tests/test_contract.py`。回归测试以明确的 porcelain 记录和独立 checkout 路径驱动真实被测 `peers()`/`peer_pointers()` 逻辑，断言 Git 检查调用集合、错误结果及残留目录保持。

## 5. 接口与数据

没有公共 Skill、CLI、DTO、配置或持久化 schema 变化。`peers()` 是 package 内部 helper；其调用者继续获得可迭代的 peer `Path` 集合。porcelain 的 `prunable` 属性只在本次调用内用于决定该路径是否属于可检查 peer 集合，不形成新的 owner、checkpoint 或记录。

## 6. 状态、顺序、正常与失败流程

1. tools owner 调用 `git worktree list --porcelain`。
2. owner 读取每个 worktree 记录的路径和 `prunable` 属性。
3. 若记录未标 `prunable`，或对应 `.git` 路径项存在，则保留路径，后续执行原检查。
4. 仅当记录标记 `prunable` 且 `.git` 路径项不存在时，过滤该路径；不对该路径调用 `rev-parse`，不检查其残留 runtime 内容，也不修改目录。
5. 若保留路径的 `rev-parse` 失败，操作保持原失败关闭行为。

普通 peer 与仍有效的 prunable peer 使用原成功路径。未标 prunable 但 `.git` 缺失的注册使用原错误路径。不存在并发或业务状态转换。

## 7. 恢复、兼容、迁移与集成

本修复只影响新 tools-only 操作的 peer 枚举。它不执行 `git worktree prune`，不删除或改写残留目录和文件，不触碰旧 tools 操作 checkpoint，不改变目标 checkout 的 Task/session、用户修改或有效 peers，也不引入 Plan2、binding 或批量迁移。无需数据迁移或回滚协议；移除本地过滤即可恢复旧枚举行为。

## 8. 验证设计

| 验证 | 对应验收 | 测试入口与观察 |
| --- | --- | --- |
| V-01 失效 prunable 注册 | AC-01、AC-05 | 调用 `peer_pointers()`，输入 Git 标记 `prunable` 且 `.git` 路径项不存在的注册；断言该路径未传给 `git rev-parse`，peer 检查可继续，残留目录和测试 marker 字节未变。 |
| V-02 正常与有效 prunable peers | AC-02、AC-04 | 输入正常 peer 与 `.git` 仍存在的 prunable peer；断言二者都传给原 `rev-parse`，其余 pointer/runtime 处理与当前路径一致。 |
| V-03 未标记但损坏的 peer | AC-03 | 输入 `.git` 缺失但没有 `prunable` 标记的 peer；断言路径仍传给原 `rev-parse`，模拟 Git 失败仍向调用方传播，不被跳过。 |
| V-04 package 回归 | AC-01 至 AC-05 | 运行 `guru-upgrade-tools` 定向 contract 测试及其 package tests，确认新断言和既有 profile/isolation/recovery 检查共同通过。测试结果只证明源码测试覆盖，不证明目标业务仓的安装采用。 |

V-01 至 V-03 是持久回归测试；不安排额外 rollback/red-green 实验。每项测试检查真实的被测 peer 逻辑及 `git` 调用结果，不以 fixture 自身状态替代生产函数观察。足够证据为失效 prunable 不再进入 peer 检查，同时三种非失效 peer 类别保持原路径；此后停止针对同一分支的重复实验。

## 9. Canonical 引用、本轮差额与实际未决项

- `docs/requirements/current/native-compatibility.md` R687-02 / BEH687-TOOLS：本修复保留合法 peer 与 Task/session，并使用既有 tools-only owner；新增边界只是跳过 Git 明确 prunable 且 `.git` 路径项缺失的失效注册。
- `docs/requirements/current/runtime-location.md` R718-06 / BEH718-LIFECYCLE：peer 注册元数据与 checkout 生命周期分离；本批不按注册数量建立或删除 runtime。
- `docs/design/current/native-compatibility.md` D687-02 / CON687-TOOLS：继续使用原 preview→prepare→invoke 和恢复路径，不增设 converter 或来源协议。
- `docs/design/current/codex-skill-distribution.md` D724-03 / CON724-MAINTAIN：沿完整目标 source 的 tools-only 路径并保留其它 checkout、用户修改和 Task/session。
- `docs/test/current/json-input-carriers.md` T695-04 / SC695-INSTALL：真实 source/installed 采用仍由原分发 owner 验证；本批仅进行源码 package 测试。
- Architecture 评估为 `no_architecture_impact`，不新增项目检查、共享贡献、ADR 或 Architecture 晋升步骤。
