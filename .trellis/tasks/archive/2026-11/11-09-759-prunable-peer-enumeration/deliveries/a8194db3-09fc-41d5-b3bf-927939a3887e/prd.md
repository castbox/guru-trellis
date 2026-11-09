# 修复 tools-only peer 枚举对失效 prunable 注册的处理

## 1. 整体来源与术语

| 来源 | 章节 | 角色 | 本批用途 |
| --- | --- | --- | --- |
| Task 根 [prd.md](../../prd.md) | REQ-01 至 REQ-04、AC-01 至 AC-05 | 已接受的整体需求 | 定义切片覆盖范围、失败关闭和非目标 |
| [Issue #759](https://github.com/castbox/guru-trellis/issues/759) | 正文 | requirement | 定义失效注册判定及三类 peer 边界 |
| `trellis/skills/guru-team/packages/guru-upgrade-tools/runtime/tools_owner.py` | `peers`、`peer_pointers` | 当前实现事实 | 定位待修复的枚举和消费路径 |

本 Delivery 覆盖一个 `guru-upgrade-tools` tools-only 操作中的 peer 发现与 peer pointer 检查。`prunable` 指 Git 在 worktree porcelain 记录中明确输出的属性；`.git` 指被发现 checkout 根下的 Git 元数据连接文件或目录。

## 2. 整体与本批目标、非目标

整体目标是仅忽略 Git 明确标记为 `prunable` 且 checkout 的 `.git` 不存在的失效注册，同时保持所有其他 peer 的原有检查。

本批目标是保留 worktree porcelain 的 `prunable` 属性，并仅在该属性为真且 `.git` 缺失时跳过该注册后续的 `git rev-parse --absolute-git-dir`。本批包含正常 peer、未标 `prunable` 但 `.git` 缺失、标记 `prunable` 但 `.git` 存在三种对照回归。

本批不清理注册，不删除或改写残留目录和文件，不改写旧工具操作 checkpoint，不执行完整 Plan2，不迁移 Task/session 或创建 binding。

## 3. 本批起点、前序结果、依赖与剩余责任

这是首个 Delivery，尚无前序 Delivery。输入为已接受 Task 根 PRD、Issue #759、源码 `tools_owner.py` 和现有 `guru-upgrade-tools` 测试。当前代码中的 `peers()` 只返回路径，未保留 `--porcelain` 输出的注册属性；`peer_pointers()` 对枚举出的每个 peer 调用 `git rev-parse --absolute-git-dir`。现有 `test_contract.py`、`test_recovery.py` 和 `test_native_install.py` 尚未覆盖本 Issue 的 prunable 缺失 `.git` 条件。

本 Delivery 负责完成该缺陷的源码修复和直接回归验证。没有分配给后续 Delivery 的已知实现责任。Task Completion 仍须根据全部整体要求及交付证据另行判断。

## 4. 本批调用方、场景与流程

### SC-01 新 tools-only 操作检查 peer pointers

- 调用方：`guru-upgrade-tools` 的 tools owner。
- 前置条件：owner 从 `git worktree list --porcelain` 读取同一 common-dir 下的 registered worktrees。
- 触发动作：owner 为新的 tools-only 操作构建 peer pointers。
- 处理行为：对每个记录读取 Git 的 `prunable` 属性及其 checkout 的 `.git` 是否存在。仅跳过同时满足 `prunable=true` 与 `.git` 缺失的注册。其他注册继续执行原有 `rev-parse` 和适用的 peer runtime 检查。
- 可观察结果：失效 prunable 注册不触发其 `rev-parse`；其他 peer 仍经过原检查。目录和文件保持原样。

## 5. 完整行为、条件与约束

- REQ-01：枚举逻辑保留每个 worktree porcelain 记录的路径和 `prunable` 属性，传递给 peer 检查。
- REQ-02：仅当注册的 `prunable` 属性为真且 checkout 的 `.git` 不存在时，跳过其 `rev-parse --absolute-git-dir` 及依赖该有效 checkout 的后续检查。
- REQ-03：正常有效 peer 继续走原有 `rev-parse` 与 peer runtime 检查；`.git` 存在的 prunable peer 也继续原有检查。
- REQ-04：`.git` 不存在但 Git 未标记 prunable 的注册不得跳过，仍须执行原有检查并 fail closed。
- REQ-05：不执行 `git worktree prune`，不删除或改写任何 peer 路径内容，不触及旧 checkpoint，也不改变 Task/session、Plan2 或 binding 行为。

本批尚无规范性来源设计处置；Issue 明确的是行为合同，不是实现机制。具体机制由 Architecture 在收到当前 Candidate 后评估。任何无法确认 prunable 或 `.git` 状态的记录都不能因防御性假设被归为可跳过 peer。

## 6. 本批验收、验证方式与未决项

- AC-01（REQ-01、REQ-02、SC-01）：输入包含一个 Git 标记 prunable 且 `.git` 缺失的注册时，peer pointer 检查不得对该路径调用 `git rev-parse --absolute-git-dir`，并能继续处理其余 peer。
- AC-02（REQ-03、SC-01）：输入包含正常有效 peer 时，peer pointer 检查仍调用其原有 `git rev-parse`，并保留适用的 runtime 检查。
- AC-03（REQ-04、SC-01）：输入包含 `.git` 缺失但未标 prunable 的注册时，路径仍进入原有检查并产生失败关闭结果。
- AC-04（REQ-03、SC-01）：输入包含标记 prunable 且 `.git` 存在的注册时，路径仍进入原有检查。
- AC-05（REQ-05）：本 Delivery 的回归测试确认失效 peer 的残留目录及文件未被改写，没有执行 prune，旧 tools checkpoint 没有被触碰。

实施阶段使用真实 `git worktree list --porcelain` 记录或忠实的 Git 命令边界替身驱动被测 owner 逻辑，并直接观察 rev-parse 调用与失败结果。执行适用的 `guru-upgrade-tools` 定向测试以确认回归行为；通过范围限于源码与该测试入口，不代表新的目标仓 tools-only 安装已采用。

本阶段没有范围未决项。实现机制由后续 Architecture 候选评估决定。

## 7. Canonical 引用与本轮差额

- `docs/requirements/current/native-compatibility.md` R687-02 / BEH687-TOOLS：本批沿用完整匹配来源、原 tools-only preview→prepare→invoke owner 和已有恢复入口；本批新增仅限 peer porcelain `prunable` 属性与失效注册处理。
- `docs/requirements/current/json-input-carriers.md` R695-05 / BEH695-DISTRIBUTION：保持 source/runtime 与安装验证分离；本批源码及定向回归不宣称安装采用。
- `docs/design/current/codex-skill-distribution.md` 第 tools-only 更新边界：保留 Task/session、其它 checkout 和用户修改。本批不改变安装路径，只修正 peer 发现的输入事实。
- `docs/test/current/json-input-carriers.md` T695-04 / SC695-INSTALL：完整安装与投影采用仍由既有 owner 验证；本批仅覆盖本地源码行为。

以上引用的机制细节和实际差额由 Design 与 Implement 正文按各自职责展开；本 PRD 不将其升级为新增范围。
