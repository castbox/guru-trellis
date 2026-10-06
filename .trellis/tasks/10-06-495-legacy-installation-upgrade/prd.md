# #495 旧业务仓原地升级 — 需求草稿

状态：实现中的同范围规划修订；本轮 Planning gates 待重新执行，不以先前规划通过替代当前修订审查。
需求 authority：[castbox/guru-trellis#495](https://github.com/castbox/guru-trellis/issues/495)，2026-10-06 live 正文及[混合库存范围说明](https://github.com/castbox/guru-trellis/issues/495#issuecomment-6014030676)；本文件只定义本任务的 accepted delta。验证顺序以已发布并 live 复读的[顺序澄清说明](https://github.com/castbox/guru-trellis/issues/495#issuecomment-6018378988)为依据。

## 问题与目标

旧业务仓 core `0.6.16` / Guru `0.6.16-guru.41` 无法采用当前无人员任务版本。当前 Fork 在 update 前拒绝不同 installed version，current task writer 拒绝旧字段；preset 也拒绝非当前 manifest。删除 creator/assignee 与禁止迁移是独立决策。本任务修订 #481 的迁移拒绝边界，提供独立、显式、一次性、单向迁移；正常 runtime 继续 current-only。

目标是保留业务仓、合法 TaskId 与有效业务事实，完成真实受管更新和任务转换，并证明可转换活动任务接续。已发布 `v0.7.0-guru.1` 不具备此能力，不修改该 tag，也不把其拒绝证据解释成升级成功。

## 支持边界

| 轴 | 本任务合同 |
| --- | --- |
| 最低旧来源 | core `0.6.16`，Guru `0.6.16-guru.41`；进一步校验旧 manifest、任务格式和 source provenance |
| 当前 before | Guru extension `0.7.0-guru.1`；固定 Fork `9c36002a324c16a09a85b6aa5a380b74aabf801f` / CLI `0.7.0-castbox.1` |
| 目标 | Guru `0.7.0-guru.2` 候选尚未正式交付；Fork CLI `0.7.0-castbox.2` 已经 PR #27 合并至 `8868c47c45fa1a9fa8f60fe30d641f70ff5c6ba1`，合并后 push CI `37473087582` 已成功，source lock 尚待同步；二者均未发布版本，不用当前 before 版本声称支持 |
| 运行模型 | 当前无人员 schema、当前 lifecycle owners；旧 parser 只存在于独立迁移入口 |
| 成功接续 | planning；尚未发布的 in_progress，经 fresh 当前规划审查进入开发/check |
| 单列诊断 | 已有 PR、已 merge、旧 Finalizer/Finish 在途、真实缺失或冲突状态 |
| 历史 | archives、.developer、journal、traces 原字节保留；旧 TaskId 防复用边界保留 |

下游真实仓仅供读取和隔离样本预演。升级真实 checkout、软件版本发布和远端业务交付不属于本任务执行权。

## 已验证来源差异

2026-10-06 读取业务 dev checkout：35 份任务，11 planning / 24 in_progress，均缺 generation/source，包含旧人员字段。33 份完整旧记录有 `subtasks`；另 2 份精简 in_progress 缺 description、dev_type、package、priority、createdAt、completedAt、worktree_path、commit、pr_url、children、parent、relatedFiles、notes、meta 当前必填字段。该清单是快照，不说明所有任务都有活动会话。

代表性普通失配：`media-model-tiers` 有 TAPD 来源、旧 branch/base 与已经消失的 worktree 路径；`limit-feedback-log-archive-to-3mib` 是 planning，branch 未建立。已知缺字段与失效旧路径不能一概归为不支持；需要使用当前 owner 重建。真正无法唯一关联的任务须具体报告。

## 行为与验收责任

| ID | 必须实现的行为 | 最低验收 |
| --- | --- | --- |
| MIG-495-01 | 写入前读取安装、受管清单、配置、平台修改、业务 spec、active/archive、Git 与 session 使用状态；AI 审查精确计划，用户确认后执行 | public preview 不写 repo；展示逐文件修改/保留、逐任务转换/处置及实际命令 |
| MIG-495-02 | 按 core / marketplace workflow / Guru preset ownership 更新；保护业务、有效配置、未知本地编辑与无关 dirty/untracked | 比较迁移前后 bytes/mode/Git 状态；逐项处置 .new/.bak；完成 update/reapply |
| MIG-495-03 | 保留合法非 UUID TaskId，初始化 generation，退役人员字段，转换已知 schema 差异，保留规划与业务事实 | 完整旧记录及两种精简记录进入 current schema；非空关系不丢失；未知字段逐项诊断 |
| MIG-495-04 | 由 AI 根据来源正文/live facts 明确 structured source；不猜测关闭意图；由 current owners 建立 branch/checkout/session | GitHub exact_source 与 reference_only 均明确审查；TAPD 事实保留且不虚构 GitHub source |
| MIG-495-05 | planning 接续当前 Planning；未发布 in_progress 保留 commit、未提交改动，经 fresh review 接续当前 dev/check | 两种任务实际 owner re-entry；不能只通过 schema 校验 |
| MIG-495-06 | 读取已有 PR/merge/旧在途事务 live facts，给出任务级支持或逐案处置；旧 gate 不转成 current pass | 已有 PR、merge、在途各 1 个代表性样本诊断；无重复 commit/push/PR/merge |
| MIG-495-07 | 更新前备份；部分写入的普通失败可识别并恢复；更新及 task 转换后、无新版业务工作时可回退 | 真实 post-write rollback 恢复旧安装可运行及旧数据；普通失败恢复后不重复转换 |
| MIG-495-08 | 固定候选 source lock、source/installed/canonical/dogfood、平台投影、inventory/runtime/reapply/drift/sidecar 验证 | 本 Issue 定向验证通过；累计多平台矩阵明确留给独立 owner |
| MIG-495-09 | 合法 current/已迁移任务与无关旧 active 共存时，创建、TaskRef/TaskId 解析、branch/checkout/session 正常接续；已诊断暂不能接续旧任务可原地保留 | 混合 current-installed 与 migration-continuation 样本；当前正式 creator/owners 成功，旧目标/占用/同身份冲突/坏当前记录仍拒绝；遗漏旧 active 阻塞迁移 |

## 数据保留与真实选择

人员字段只从 active current task 结构退役；迁移前副本由 private backup 保存。历史目录不进入新 personnel/index/恢复 authority。描述、notes、meta、业务规划不能改写为编造的当前 gate。精简记录缺失的 current 字段按 design.md 任务转换表补齐空值、P2 优先级或读取事实；source 与 branch 存在真实歧义时请求补充；日期不以目录推断真实创建事实。补全来源、分支映射、受管本地修改处置和 rollout/rollback 都由 AI 判断，不写成脚本 planner。

整仓安装成功与任务接续成功分别报告。仓库存在无关活动任务不阻塞安装；有实际共享写入会话时先协调。残余任务每项列出具体缺失事实、影响和 re-entry owner，不能藏在总体成功声明中。

混合库存继承 `R467-02` 的目标局部阻塞合同。仅正向识别已知旧记录，读取其 TaskId/TaskRef 作身份占用与诊断，不将其作为 current lifecycle candidate。直接旧目标、目标 TaskId/TaskRef 占用、同身份大小写冲突、current 自身坏 generation/source/额外未知字段、坏 JSON 或缺 id 仍 fail closed；不得笼统捕获 `unsupported_legacy_task` 后跳过全部错误。迁移对已诊断旧记录显式作 preserve/deferred 处置，原字节保留；未审查/遗漏旧记录仍阻塞，不宣称所有任务已转换。

MIG-495-07 的新工作保护覆盖部分迁移期间：core/task 已写而 Guru 因普通冲突停止后，正常 task writer 新增 meta 等业务事实必须阻止覆盖式回退，后续 resume 不得把这些工作吸收到可回退基线。MIG-495-02 保留有效配置与用户设置，允许官方必要的 additive 配置；历史/journal/业务/spec/规划继续要求原字节保留。MIG-495-05 必须使用真实脱敏项目 Architecture baseline、实际两类 qualifications 和语义 Planning gates，结构校验成功不等于 semantic pass。

## 不包含与完成定义

不恢复人员体系，不新增正常 runtime 双读、历史批量迁移、自动 Issue 关闭或任务完成，不改业务代码或生产配置，不 rewrite Git 历史，不引入锁、额外 fault injection 或攻击模型。普通 stale、mismatch、失配、部分写入与错误传播属于范围。

完成需要 MIG-495-01..09 的真实证据、已固定可复现目标候选与可执行升级/恢复/回退说明。正式 Fork source lock、混合库存修复、代表性迁移或语义接续证据尚未完成时必须明确未验证，不能宣称 #495 已解决。

验证顺序不改变完成定义：先证明本地候选与正式 Fork 来源，经 fresh gates 形成 Refs-only 候选 Delivery，再用固定且远端可读的同一 Guru commit 完成真实 `source_locked` public/provider 隔离验收。候选发布不代表 #495 完成；MIG-495-01..09 全部真实证据齐备后才允许合并与最终 Completion。MIG-495-06 的 live PR、merge、支持旧来源的真实在途样本仍逐项要求，不用历史终态或模拟状态替代。
