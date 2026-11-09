# 修复 tools-only 对失效 prunable peer 注册的处理

## 1. 来源与术语

| 来源 | 章节 | 角色 | 本 Task 用途 |
| --- | --- | --- | --- |
| [Issue #759](https://github.com/castbox/guru-trellis/issues/759) | 正文：修复条件、非目标和回归覆盖 | requirement | 定义唯一行为范围、保护边界和验收条件 |

- `peer`：由 Git worktree 注册表发现、并由 tools owner 检查的同一 common-dir 下的其他 worktree。
- `prunable`：Git 在 worktree porcelain 输出中明确提供的注册属性。
- `.git`：checkout 根目录下用于标识其 Git 元数据连接的文件或目录。

## 2. 背景与问题

`guru-upgrade-tools` 的 peer 枚举目前只保留 worktree 路径，并丢弃 `prunable` 属性。后续 `peer_pointers` 对每个注册路径调用 `git rev-parse --absolute-git-dir`。当 Git 已标记该注册为 `prunable`，而残留目录中的 `.git` 不存在时，命令返回 128，导致新的 tools-only 操作预览被阻止。

直接来源只描述这一类失效注册。目录和其中残留文件仍须保留。其他 peer 继续接受原有检查。

## 3. 目标与非目标

目标是让 tools-only peer 枚举跳过且仅跳过同时满足以下条件的注册：Git 明确标记为 `prunable`，并且对应 checkout 的 `.git` 不存在。该条件不成立时，沿用原有 peer 检查及失败关闭行为。

本 Task 不执行 `git worktree prune`，不删除、移动或改写残留目录和文件，不修改已存在的 tools 操作 checkpoint，不处理完整 Plan2，也不迁移 Task/session 或批量创建 binding。

## 4. 真实调用方、场景与流程

### SC-01 新 tools-only 操作发现 peers

- 调用方：`guru-upgrade-tools` 的 tools owner。
- 前置条件：owner 从 Git worktree porcelain 枚举同一 common-dir 下的注册。
- 触发动作：owner 为新的 tools-only 操作计算 peers 和 peer pointers。
- 处理行为：对每个注册读取其 `prunable` 属性和 checkout 的 `.git` 是否存在。仅对 `prunable` 且 `.git` 不存在的注册跳过后续 `git rev-parse`。其他注册进入原有检查。
- 可观察结果：所述失效注册不再以 Git 128 阻止新操作预览；残留目录及文件保持不变；有效 peer 继续被检查。

## 5. 行为要求

- REQ-01：peer 枚举必须保留 Git worktree porcelain 中每个注册的 `prunable` 属性，供后续 peer 检查作条件判断。来源：Issue #759 正文“修复应仅跳过……”。
- REQ-02：仅当同一注册同时满足 `prunable=true` 和 checkout 的 `.git` 不存在时，跳过该 peer 的 `git rev-parse --absolute-git-dir`。来源：Issue #759 正文“修复应仅跳过……”。
- REQ-03：未标记 `prunable` 的注册即使 `.git` 缺失，也必须继续原有检查并保持失败关闭。标记 `prunable` 但 `.git` 存在的注册也必须继续原有检查。正常 peer 必须继续检查。来源：Issue #759 正文“其它 peer 继续经过原检查”及“回归覆盖”。
- REQ-04：本变更不得 prune 注册、删除或改写残留目录和文件、修改旧 tools 操作 checkpoint，或引入完整 Plan2、Task/session 迁移及 binding 创建。来源：Issue #759 正文“本修复不……”。

## 6. 约束与依赖

- 修复位置限于 `guru-upgrade-tools` 的 peer 枚举与 `peer_pointers` 检查路径，以及直接验证这些行为所需的测试。
- Git worktree porcelain 的属性是判断某注册是否可跳过的来源。目录自身存在不能替代 Git 明确提供的 `prunable` 属性。
- `.git` 存在的 prunable 注册和未标记 prunable 的损坏注册都不能作为可忽略 peer。
- 不需要修改工具操作恢复资料，也不需要清理 Git 注册或 checkout 残留。
- 具体实现机制由当前 Delivery 的 Author 与 Architecture 流程决定；本 PRD 不预选实现方式。

## 7. 可观察验收与验证方式

- AC-01（REQ-01、REQ-02）：给定 Git 标记为 `prunable` 且 checkout 的 `.git` 不存在的注册，运行 peer 枚举后，该注册不会触发 `git rev-parse --absolute-git-dir`，tools-only 预览能够继续完成 peer 检查。
- AC-02（REQ-03）：给定正常有效 peer，运行 peer 枚举后，该 peer 仍触发原有 Git 检查。
- AC-03（REQ-03）：给定 `.git` 缺失但未被 Git 标记为 `prunable` 的注册，运行 peer 枚举后，系统仍执行原有检查并拒绝该损坏 checkout，不得静默跳过。
- AC-04（REQ-03）：给定被 Git 标记为 `prunable` 且 `.git` 仍存在的注册，运行 peer 枚举后，系统仍执行原有检查。
- AC-05（REQ-04）：回归验证前后，失效注册目录和其中文件均未被删除或改写；旧 tools 操作 checkpoint 未被修改；没有执行 prune、Task/session 迁移或批量 binding 创建。

验证入口和断言由当前 Delivery 的 Implement 规划确定。验收只记录可观察条件，不预填任何测试结果。

## 8. 实际未决项

本阶段没有未决的产品范围问题。peer 检查的具体实现与回归测试组织由 Delivery 的设计和实施阶段处理。
