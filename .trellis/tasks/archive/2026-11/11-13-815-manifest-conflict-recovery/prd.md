# #815 受管 manifest Git 冲突恢复：整体需求

## 1. 来源与术语

| 来源 | 条款、角色与用途 |
| --- | --- |
| https://github.com/castbox/guru-trellis/issues/815 | Direct Source；要求 1–4、验收及交付兼容边界是整体需求权威。2026-11-13 重读，OPEN，无评论 |
| https://github.com/castbox/guru-trellis/issues/792 及 PR #806、#807 | 原冲突案例和已合并交付属于历史事实，不作为本 Task 的验收通过证据 |
| `trellis/skills/guru-team/packages/guru-reconcile-task-base/references/contract.md` | resolved candidate、同身份整合与 dirty metadata 保留的原 owner 合同 |
| `trellis/skills/guru-team/packages/guru-upgrade-tools/references/contract.md` | preview/prepare、逐路径 preserve/replace、installer 和同操作恢复的原 owner 合同 |
| `trellis/skills/guru-team/packages/guru-publish-task-delivery/runtime/owner.py` 的 `retire_completed` | 公共发布事实与已完成私有事务生命周期的原机制 |
| `AGENTS.md`、`.trellis/spec/workflow/skill-package-contract.md`、`.trellis/spec/preset/upstream-ownership.md` | AI/脚本分工、公共兼容、受管安装和 provenance 约束 |

临时前像指固定 Git 对象中已经由 installer 生成的完整旧安装 manifest blob。组合投影指合并后的 canonical 经原 installer 生成的最终 manifest、runtime 和声明平台副本。前像不是新 canonical，也不是最终候选。

## 2. 背景与问题

正常两分支分别修改 canonical 并同步受管文件后，整合时可能在 `.trellis/guru-team/extension.json` 产生冲突。tools inventory 首先解析该 JSON，冲突标记阻止 preview/prepare。#792 曾通过固定 H 的完整旧 manifest 前像、逐路径判断和组合 canonical 重建完成恢复，但公共合同没有明确有界接续。

开发基线为 `origin/main@cb8b4ce349b54cd832ff5b8f72602c5a721ce875`，集成和完成目标为 main。固定对象不要求移动主仓本地 main。

## 3. 目标与非目标

补齐现有 Reconcile/Git 冲突处理到原 tools owner 的正式有界恢复合同，证明正常两分支场景可到达最终组合安装和 resolved 整合提交。

整体责任包括合同、必要确定性动作、兼容迁移、定向验证、受管投影同步、独立交付、Completion/Closure 和必要归档；最终核实 merge result 在 live main 可达。

不创建通用恢复框架，不扩大完整安装矩阵，不绑定发布 Issue、版本或时间，不实施其它 Issue。不处理恶意篡改、绕过、压力、锁、偶发 crash 或额外并发加固，不修改上游源码、全局包或已完成历史。

## 4. 真实调用方、场景与流程

| 场景 | 调用方、前置、处理与可观察结果 |
| --- | --- |
| S815-01 | 原整合 owner 在同一 Task/Delivery 整合两个正常 canonical 分支时遇到 manifest 冲突。固定完整旧 blob 作为临时前像；原 tools owner 审查组合 canonical 的逐路径 preserve/replace，由原 installer 重建最终投影 |
| S815-02 | 原 tools owner 遇到正常失败或输出丢失时，检查实际事实并沿原事务恢复；不重放未知 mutation，不新建身份或资源 |
| S815-03 | 原 resolved owner 在组合安装验证后，保留当前 Task 的自然 dirty metadata 及无关 Task/session/peer；零未合并条目后按原 resolved 路径提交，临时前像不进入最终候选 |
| S815-04 | 原 Publication owner 对已完成私有事务执行原 `retire_completed`，公共发布事实保持；未完成或未知动作先恢复原操作 |

## 5. 行为要求

- **R815-01（S815-01）**：明确原 Reconcile/Git 冲突处理到 tools owner 的入口、职责、顺序和停止条件。只复用固定对象中已生成的完整 manifest blob 作为临时旧安装前像。
- **R815-02（S815-01）**：保留该 blob 原 provenance/hash，不改 hash 消除真实差异。合并后的受管路径由原 tools owner 逐路径判断 preserve/replace。最终 manifest 和投影必须由原 installer 生成。
- **R815-03（S815-02、03）**：保持同一 Task/Delivery、branch、worktree、PR。自然 dirty `task.json` 按原 resolved 路径保留。保留无关 Task/session/peer 和工作区内容，不以重建身份或清理无关状态恢复。
- **R815-04（S815-02、04）**：完成的私有 Publication 事务按原 `retire_completed` 退役，公共发布事实保留。未知 mutation 先恢复，不重放。失败复用原输入、事务和恢复材料，不刷新 rollback 前像。
- **R815-05**：通过原安装 owner 同步 canonical、受管 dogfood 和声明平台投影。保持原 Skill 语义门禁、事实校验及公共 API 兼容；真实接口变化提供明确迁移合同。不新增授权存储或审计 ledger。
- **R815-06**：本 Issue 独立完成交付、关闭及必要归档，核实 merge result 在 live main 可达，不依赖指定发布 Task 或版本。

## 6. 约束与依赖

Markdown/AI 判断前像适用性、逐路径处置、充分性和路由；脚本只执行固定字节恢复、安装、Git 动作及客观验证。Hash/digest 用于一致性和过期检测，不提供授权或语义批准。

沿用原 tools preview/prepare/invoke、installer、resolved candidate 和 Publication 事务。临时前像期间不声称组合安装完成。最终候选必须来自组合 canonical 的真实 installer 结果，满足零冲突与零未处理 sidecar。

只执行 accepted scope 所需定向验证。完整多平台安装/升级/Release 矩阵和其他 native host 保持未验证边界。需要更新已有安装时由原 tools owner 处理，不手工覆盖受管副本。

## 7. 可观察验收与验证方式

| 验收 | 对应要求 | 入口、输入与预期结果 |
| --- | --- | --- |
| AC815-01 | R815-01、02 | 真实 Git 两分支 canonical 修改及各自 installer 输出造成 manifest 冲突。经正式入口采用固定完整旧 blob，核对原字节和 provenance/hash 保持 |
| AC815-02 | R815-02、05 | 原 tools owner 逐路径审查并从组合 canonical 运行原 installer；installed/native/drift 检查通过，组合行为均存在，无临时前像进入最终候选，无未处理 `.new/.bak` |
| AC815-03 | R815-03 | 核对同一 Task/Delivery、branch、worktree、PR；无关 Task/session/peer 与 dirty metadata 保留；原 resolved 路径产生正确整合提交，`git ls-files -u` 为空 |
| AC815-04 | R815-04 | 定向检查原同操作恢复和已完成 Publication 事务退役；原恢复身份不变，未知动作不重放，公共发布事实保持 |
| AC815-05 | R815-05 | 受影响 package/runtime、canonical/installed、声明平台投影、drift、sidecar 和 mode 定向验证；公共变化有兼容说明 |
| AC815-06 | R815-06 | 原独立完整 committed review、Delivery、Completion、Closure 和必要 Finish；live main 可达性与 Issue 状态由原 owner 回读核实 |

以上均是待执行验收，不声明测试、安装、整合或交付已经通过。

## 8. 实际未决项

整体需求无未决项。技术细化、精确写集、验证命令和必要迁移由 Delivery Author 与独立 Architecture/Approval 在实施前收敛。当前委派要求在实施前停止并报告。
