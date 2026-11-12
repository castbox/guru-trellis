# #812 合法 explicit-task 资格判定与续接：整体需求

## 1. 来源与术语

| 来源 | 角色与用途 |
| --- | --- |
| [Direct Source #812](https://github.com/castbox/guru-trellis/issues/812)，背景、要求、验收、交付与兼容边界；已读取完整正文，当前无评论 | 本 Task 的要求和验收权威，source 为 exact_source |
| `docs/requirements/current/qualifier-applicability.md`、`docs/test/current/qualifier-applicability.md` | 已交付的条件调用和真实入口证据边界；本次保留原适用性判断 |
| `trellis/skills/guru-team/runtime/qualification_facts.py`、同级 `delivery_projection/adapter.py` | 当前实现事实，供规划定位差额；不替代需求 |
| #813 的 PR #816、归档 PR #817，当前创建起点 `f16bb562e4ea844939786cebd5c6c20e686914b2` | 已交付的固定 Git 来源创建能力；保留历史结果 |

explicit-task 指官方 context key 确实不可得、经原 Identity/Ensure/Bind 确认的显式 Task 执行模式。DeliveryKey 指上游公共的 TaskId、lifecycle_generation、delivery_id 完整身份。context 存在但绑定或选择错误，不属于无 context 模式。

## 2. 背景与问题

#812 记录 #794 原执行会话已取得 explicit_task_mode，Identity/Ensure 已确认 Task 与唯一 checkout。normal-scenario 的 implementation_discovery 经共享 qualification_facts 调用无 key 的 DeliveryProjection.current()，仍要求 context key，返回 stale_identity。当前基线的共享 Planning 校验保留此路径，adapter 已有显式 key 的解析入口。

期望合法显式模式能够完成适用资格判定，并回到原阶段。当前差额涉及完整身份从公开 qualifier 输入到共享事实入口及 caller 的承接。不能通过借用其他会话绑定、制造环境键或省略事实检查解决。

## 3. 目标与非目标

整体目标是贯通 normal、solution、root 的合法显式模式与原 caller 续接，并保留正式 context 模式的匹配和冲突检查。整体完成包含实现、真实入口验收、公共兼容迁移、受管分发、Delivery 交付、Completion、Closure 和必要归档。

不新增选择 authority、绑定存储、资格 ledger 或授权存储。不改变三个 qualifier 的独立语义职责及原分类/非通过含义。不实施其他排队 Issue，也不触碰 #808 的 checkout、Task、Delivery 或未提交内容。不增加攻击、压力锁、crash、并发加固或完整多平台发布矩阵验收。

## 4. 真实调用方、场景与流程

| 场景 | 前置、动作与可观察结果 |
| --- | --- |
| S812-01 合法显式资格判定 | 原 Identity/Ensure/Bind 确认无官方 context key 和当前 Task/checkout；原 caller 按真实适用条件调用 qualifier。完整显式 Task/Delivery 身份通过 generation、branch binding、registered checkout、Planning 和候选校验，取得原 typed exit，原 caller 消费后继续自己的实际义务 |
| S812-02 正式 context | 官方 context 存在且选择匹配时，公开入口成功；实际绑定或选择冲突时保留原拒绝及恢复 owner，不能以显式 key 隐藏错误 |
| S812-03 普通过期与不匹配 | 正常 generation、branch、checkout、Planning 或候选变化造成旧输入不适用时拒绝；原 caller 重读事实并构造新调用，不复播旧输入，也不新建身份 |
| S812-04 matching 采用 | 当前完整 provider 更新公共合同及调用方，经原安装 owner 更新受管安装；原 Task/generation/Delivery 与已完成历史保留，按实际阶段续接 |

## 5. 行为要求

- R812-01：对 S812-01，三个适用 qualifier 使用同一完整显式身份合同；无 context 时校验当前 generation、C4 branch binding、唯一 registered checkout、公开 Delivery 关系、Planning 和候选。
- R812-02：对 S812-02，有 context 时仍校验官方当前选择及冲突；不得从项目 inventory 猜 Task，不借其他会话状态，不制造 context key。
- R812-03：共享事实入口和实际 caller 成套采用合同。classified 和非通过出口保留其唯一 consumer，结果返回原 caller。脚本只检查确定性事实，AI 继续拥有资格语义和路由判断。
- R812-04：S812-03 的普通 stale/mismatch 仍拒绝并交原恢复 owner。修复不能以跳过 Planning、候选、generation、branch 或 checkout 检查换取成功。
- R812-05：对公共输入、schema、接口或命令的实质变化提供显式迁移及在途兼容合同。canonical、受管 dogfood 和实际受影响声明平台沿原安装 owner 同步；保留原门禁、事实校验和已完成历史。
- R812-06：以真实 Identity/Ensure/Bind、三个适用 qualifier 的公开入口和实际 caller 返回证明行为。私有函数测试、schema 校验或分发一致不能代替这项验收。
- R812-07：正式发布 #808 前完成本项交付、关闭和必要归档，且 merge result 在 live main 可达。未执行的验证逐项保留边界。

## 6. 约束与依赖

使用完整 matching Guru provider 和既有 Task/Delivery API；不修改上游 Trellis、全局安装或 hook 来实现资格判断。Markdown 拥有判断和路由，runtime 只执行确定性检查。公共 Skill package 兼容合同、正常场景边界与原安装 owner 约束适用。

固定创建起点与 PR 目标 main 分开；其他分支进展本身不触发默认同步。没有新持久化数据模型需求。具体输入演进、事实调用和回滚方式由 Delivery Author/Architecture 细化；若形成真实范围或重大方案选择，返回原 owner。

## 7. 可观察验收与验证方式

| 验收 | 对应要求 | 入口、输入与预期结果 |
| --- | --- | --- |
| AC812-01 | R812-01、03、06 | 原 Identity/Ensure/Bind 建立真实 explicit-task 前提；三个适用 qualifier 的公开输入携带完整实际身份并返回原出口，实际 caller 消费后回到原阶段 |
| AC812-02 | R812-02、04 | 正式 context 匹配输入成功；正常选择冲突、过期 generation、checkout/Planning/候选不匹配拒绝并保留原恢复路线，不以人工环境键模拟前提 |
| AC812-03 | R812-03、05 | 公共输入、输出 consumer、迁移、canonical/installed/平台投影和必要 drift/reapply/sidecar 定向验证一致；不产生第二绑定存储或资格账本 |
| AC812-04 | R812-07 | 正式 Check、独立完整 Branch Review、readiness、整体 Completion、Closure、Finish 取得真实结果，交付与终态归档在 live main 可达 |

具体长期回归与临时运行观察在 Delivery 的 design/implement 中按实际缺口选择。当前仅定义验收，不声明任何实现或安装行为已经通过。

## 8. 实际未决项

整体需求无未决选择。公开身份输入迁移细节、实际 caller 观察方法及原安装 owner 更新范围由 D1 Planning 展开；它们是当前技术规划义务，不是已通过的验证结果。
