# #813 固定 Git 基线 Task 创建整体需求

## 1. 来源与术语

| 标识 | 来源及章节 | 角色与用途 |
| --- | --- | --- |
| SRC-813 | https://github.com/castbox/guru-trellis/issues/813 ，完整正文；2026-11-12 读取时无评论 | Direct Source、行为与验收要求 |
| SRC-USER | 当前会话的串行执行请求 | 集成基线 origin/main；#813 完成后才继续 #812 → #811 → #814 → #815 → #808；隔离 #808 停放内容 |
| EV-CREATE | `trellis/skills/guru-team/packages/guru-create-task/SKILL.md`，创建与恢复合同 | 当前 owner、acquisition、Task/session 边界证据 |
| EV-COMPOSE | `trellis/skills/guru-team/runtime/task_lifecycle/composition.py`，`prepare_creation_inputs` | 当前本地基线分支相等条件及校验顺序证据 |
| EV-TEST | `trellis/skills/guru-team/packages/guru-create-task/tests/test_contract.py`，stale/mismatch 与创建测试 | 当前测试安排证据，不代表已执行通过 |

固定审核对象是 Sync `operation=read` 选定的 Git commit。Delivery target 是未来交付的仓库和分支。固定对象不随同名本地分支的新旧状态改变。旧同步型来源是 Sync `operation=sync` 的原 provenance 与同步语义。

## 2. 背景与问题

Issue 记录 #792、#794 取得固定 origin/main OID 后，Creation 仍要求本地 refs/heads/main 等于 reviewed_base_head；#793 还观察到 base ref 装配与过期诊断混淆。这些是历史观察，不要求重写既有完成结果。

审核基线为 `5c6a4591db7165ece045e6b0eb789c21d06d7d38`。该版本的 `prepare_creation_inputs` 先比较本地基线分支 HEAD，再检查 acquisition 审核起点。现有测试会将 primary 快进到审核 HEAD，没有证明 primary 保持旧 main 和无关 dirty 时的完整创建链。本项自身创建时本地 main 与审核对象相同，已通过原入口建立身份；该事实不证明目标验收已满足。

## 3. 目标与非目标

目标是让固定 Git 对象来源的合法创建不依赖主目录本地同名分支同步，同时保留真实不一致的拒绝与恢复。交付包含创建合同和确定性校验、公共兼容迁移、必要文档与知识收敛、定向验证及受管分发同步。

不承担其它串行 Issue 的实现，不触碰 #808 的 Task 或未提交内容。不扩展恶意伪造、攻击、压力、锁、TOCTOU、crash consistency、并发加固或完整发布安装矩阵。保留 secret 脱敏、权限与原发布规则。

整体完成须具备全部验收、提交后独立完整 Review、readiness、PR 合并、Task Completion、源 Issue Closure 和必要 Finish 归档；合并结果须在 live main 可达。阶段通过或单个 Delivery 合并不能代替整体完成。

## 4. 真实调用方、场景与流程

| 场景 | 调用方与前置条件 | 触发、处理与可观察结果 |
| --- | --- | --- |
| S1 固定对象创建 | 原 Sync/Intake/Creation 调用方；已审核 origin/main 对象较本地 main 新，primary 有无关 dirty | 完整 Sync read → Intake → Creation，按审核对象和合法 acquisition 创建或采用独立 checkout；一个精确起点的 Task，primary refs/index/workfiles 不变 |
| S2 输出丢失恢复 | 原创建成功，调用方丢失结果 | 原 owner 回读原 Task、generation、branch binding 与 acquisition；返回原身份，不再创建 Task、branch 或 checkout |
| S3 真实不一致 | 审核对象不可用，或与 acquisition 的对象、仓库/common-dir、Task/generation、branch binding 不一致 | 原 validator 拒绝；字段级诊断指向原 owner 恢复，不产生错误 Task |
| S4 旧同步来源 | 既有合法同步型调用方 | 按明确兼容合同保留原同步语义，或在显式迁移边界拒绝并给出迁移路径；不得静默改义 |

## 5. 行为要求

- **R1**：原创建 owner 区分固定 Git-object 审核起点与 delivery target branch。固定来源的 freshness 不使用本地同名 branch HEAD 的新旧状态判定。（S1）
- **R2**：按已审核对象和适用 acquisition 创建或采用独立 checkout。保留 exact source、仓库/common-dir、Task identity、generation、branch binding 与 acquisition 校验。新 Task 不采用 primary；不得为满足创建而移动、重置、stash 或提交 primary 的无关内容。（S1、S3）
- **R3**：真实对象/acquisition mismatch 继续 fail closed，并给出字段级原 owner 恢复。基线来源装配错误与真实对象过期按实际失败字段区分。（S3）
- **R4**：结果丢失由原恢复入口读取原结果，不重复创建身份或资源；保留原 session 冲突与缺 context key 边界。（S2）
- **R5**：明确旧同步型来源兼容边界与公共 API 迁移。保留原 Skill 语义门禁、事实校验和已完成历史；不新增授权存储或审计 ledger。（S4）
- **R6**：canonical、受管 dogfood 与声明平台投影同步，经匹配的原安装 owner 更新及验证。Markdown 负责 AI 判断和路由，脚本只执行确定性动作与事实校验。（S1—S4）

## 6. 约束与依赖

沿用当前公共 workflow 与 Skill package 合同、官方 Task/schema2 与 Delivery API、现有 checkout/binding/ownership/session owners。输入迁移和实现机制由 Delivery Author、适用 qualifier 与 Architecture 按原流程细化。不得手造上游 transition、context key 或通过结果。

集成目标为 castbox/guru-trellis/main。正式发布 #808 依赖本项完整关闭、必要归档与 live main 可达；本项不执行 Release。普通定向验证不承担专门累计安装或发布矩阵职责。没有业务数据库或服务部署迁移。

## 7. 可观察验收与验证方式

| 验收 | 对应要求/场景 | 入口、输入与独立观察 |
| --- | --- | --- |
| AC1 | R1、R2 / S1 | 临时仓库保留落后 main 与 primary 无关 staged/unstaged 工作；真实 Sync read 和完整 Intake 输出进入 Creation。核对审核 commit、唯一 Task、checkout/binding/generation；比较 primary refs、index、workfiles 前后不变 |
| AC2 | R4 / S2 | 丢弃创建返回值，从原恢复入口取回同一 Task；核对 Task/branch/worktree 数量和身份不变，无重复副作用 |
| AC3 | R2、R3 / S3 | 用正常调用装配错误或真实对象/acquisition 不一致调用原入口；核对拒绝、字段级恢复和无错误 Task 创建。不得靠人为伪造内部 artifact/hash/state 扩展测试 |
| AC4 | R5 / S4 | 原同步来源调用与明确迁移样例验证兼容合同；合法调用保持原义，不能接受的旧输入给出明确迁移说明 |
| AC5 | R6 | 核对 canonical、实际受管安装、声明平台投影、drift/reapply 与 sidecar；原安装 owner 更新时保留 Task/session。执行相关 package/runtime 测试和所需代表性安装验证，不宣称完整发布矩阵通过 |
| AC6 | 整体完成 | 本项 PR merge OID 在 live main 可达；Completion、Closure、必要 Finish 有原 owner 的真实结果，#813 已关闭且整体归档准确 |

上述验收尚未执行。报告应区分源码检查、实际链路、安装投影及未验证边界。

## 8. 实际未决项

没有阻塞整体需求的未决用户选择。具体公共输入版本和兼容迁移、定向测试安排及安装动作由 Delivery 规划展开并审核；本 PRD 不提前批准机制或实现。
