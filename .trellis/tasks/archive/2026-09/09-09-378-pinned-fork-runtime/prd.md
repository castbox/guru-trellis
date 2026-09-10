# #378 固定 Fork runtime 与会话隔离

## 状态与来源

状态：in_progress，当前进行 Branch Review finding 修复后的完整 Phase 2 复核。
需求来源：GitHub `castbox/guru-trellis#378` 当前正文。
前置修复：#388、#389 已由 PR #390 合入基线
`a2b32ea8dc730eecf0507e0adfb946ce9b8c7bc8`；本任务不关闭这两个 Issue。

## 目标

Guru 的新安装与后续更新实际消费带会话隔离补丁的 castbox/Trellis，
不再依赖原 Trellis 源码仓库或原 Trellis npm 发行包获取框架代码。
主会话缺少身份或身份不匹配时不能继承其他 session 的 task。

## 实施前缺口

- README 的安装命令与验证脚本仍选择原 npm 发行包。
- 当前 manifest 的 Trellis target 为 0.6.15，源码来源没有固定 Fork commit。
- 已合并的 Fork 修复不因配置 upstream remote 自动进入 installed runtime。
- 旧升级 stash 的 installed manifest 早于 #388/#389，不能整体覆盖新基线。

## 要求

| ID | 行为 |
| --- | --- |
| R1 | 框架源码固定到 castbox/Trellis 的完整 commit SHA，允许未发布源码构建；版本号不单独充当来源证明。 |
| R2 | 新安装与已有项目更新共用固定来源入口；构建或网络失败返回错误，不回退到原发行包、全局 CLI 或另一个 source ref。 |
| R3 | 主 Codex SessionStart、workflow-state 和普通 CLI 不借用 single-session fallback；仅显式支持的 child-agent 调用保留选择该能力的接口。 |
| R4 | 缺失身份、未匹配身份及 stale task 不引发其他 session 的读取接续或清理；原 session 内容保持不变。 |
| R5 | runtime 更新由 Fork CLI 执行；Guru preset 只维护 Guru namespace，保留已安装平台和本地定制。 |
| R6 | 当前安装说明、更新入口、来源记录与定向测试同步迁移；历史归档、第三方依赖和许可证归属保持真实。 |
| R7 | 分别报告源码、installed 与真实业务接续结果；本任务不把测试 fixture 成功宣称为业务交付或 Release Gate 成功。 |

## 验收

1. R1/R2：新安装和已有项目的第一次、第二次更新都使用锁定的 Fork SHA；命令追踪中不安装原 Trellis 发行包，不调用全局 trellis 替代固定 CLI。
2. R1/R5：构建输入、CLI 版本与 installed resolver/hook 字节有可核验对应关系；目标路径不记录机器私有绝对路径或用户授权。
3. R3/R4：canonical 与 installed 测试覆盖零个、一个、多个 session，缺失/未匹配/精确匹配身份、stale pointer、显式 child 路径和两个独立 worktree；非所属 session 内容与文件集合不变。
4. R5：Claude/Codex/Cursor 的现有平台集合保留；workflow、本地定制、#388/#389 runtime 不被旧 stash 覆盖。
5. R5/R6：source/installed 校验、reapply、drift 和 sidecar 检查通过。
6. R7：一个代表性 clean 安装及 existing/update 定向场景通过；累计多平台 Release matrix 和业务 #31/#127 接续单独列为未验证。

## 非目标

不发布 npm 或 tag/Release，不重构 session model，不修改 #377/#388/#389 的业务合同，
不执行真实业务部署，不清理历史 session、stash 或其他 worktree。
不增加攻击模型、锁、TOCTOU、压力或异常 crash 加固。

## 剩余门禁

修复后的 Phase 2、独立 committed Branch Review、Docs promotion 与发布门禁仍需完成。
本文件不构成发布放行。
