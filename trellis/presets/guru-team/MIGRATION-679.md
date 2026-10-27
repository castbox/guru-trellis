# #679：接收会话前置检查、首失败诊断与请求构造

## 采用范围

本版本在原 Task schema 2.0 / Delivery API 1.0 上直接修正调用合同。workflow 的
created consumer、唯一 continuation 和五个 Planning owner 先检查接收会话自己的
事实。明确同一 Task/generation/key 时，只经原 Identity/Ensure/Bind/Selection 补缺，
重读公共 key、phase、scope 和 planning_root 后继续原未完 profile/purpose。
匹配事实复用；不同选择、终态、真实 stale 或 error 留在对应原 owner。显式 key
不能代替有 context 的会话绑定；只有原 resolver 确认无 context 才走既有 explicit-task。

独立 Architecture 在完整 baseline/constitution/change-contract 首读后补自己的
会话事实，再评估实际候选。恢复不注入 Task PRD、验收、实现摘要或旧 pass，不继承
父会话，不制造阶段通过。原公共 writer、阶段、Skill id、输入/出口 schema、DTO、
helper 参数及 adapter 的 current/select 边界保持；没有新映射、状态、兼容读路径或
绑定脚本。普通同对象恢复不重启初始规划，也不重复要求用户手动绑定或确认继续。

## 首失败诊断的直接演进

Author 与 Architecture 的原 Planning validator 保留 `stale_identity` code 和退出码 3。
原复合错误 `field_path=delivery_key` 细化如下；消息指出真实条件及原 owner，不再把
缺绑定解释为规划过期。表按本地可得条件的检查顺序排列。原公共解析器/resolve 若先
拒绝身份、generation 或安装事实，保留该原始首失败，不用后续推测覆盖。
Author 在 Delivery guard 之前的 Task 解析也保留原 LifecycleContractError 的
field_path/remediation，并在消息中保留原 code；外层仍为 `stale_identity`，不再把
`unsupported_delivery_api` 一类安装错误改写为泛化 Task 身份指令。

| 首失败条件 | 当前 field_path | 恢复 owner |
| --- | --- | --- |
| `no_current_task` | `session.task` | 原 Identity/Ensure/Bind |
| `no_current_delivery` | `session.delivery` | 原 `guru-create-delivery:delivery_selection` |
| `terminal_delivery` | `delivery.phase` | 原 terminal/release owner |
| 公共 current 返回 `error` | `current.error` | 消息保留实际 query code/message，回原 identity/session 或 installation owner |
| 不支持的 current kind | `current.kind` | 原 installation owner；不能当成缺 Task |
| 当前已选 key 不同 | `current.key` | 原选择/生命周期 owner，不覆盖 |
| key generation 不符 | `delivery_key.lifecycle_generation` | 原 Identity owner |
| 目标 phase 不为 planning | `delivery.phase` | 实际 stage owner 合法 rework |
| slice scope authority 不等于整体 accepted_scope | `delivery.scope_ref.authority` | 原 Clarify 与当前 stage 的 scope-revision owner |

每次只报告首先失败条件；原 owner 恢复后重新读取其它条件。全部原拒绝条件保留。
五个 Planning caller 都执行自身的原 owner 前置检查；Wording、Approval、Activation
原 runtime 保护保持，不由 validator 自动选择对象、绑定或决定语义 route。

## standalone 与文档展示

Readiness 原可执行 recipe 增加 `standalone_request` 变体：实际 Wording 的
`transition.target_locator` 同时定位当前 source.draft_id 和 consumer.request_id。
caller_locator 保留真实调用方身份且可与请求不同；profile 与 mode 独立，mode 来自
实际 producer transition。完整 authority digest、recorder 派生、真实 checker receipt
及原 normalization 保持。普通构造错误由原 Agent 重读未改 producer/source，重审
消费者十维并完整重建，不改 producer 或补算私有 linkage/receipt。原回放入口按真实
来源 profile 读取样本，不将 package 两 mode 结果冒称为两 mode 原生通过。

Human artifacts 的原 resolver 继续要求实际 `--delivery-key`。明确切片时，workflow
向它传真实 TaskRef/key 并展示返回的存在文件；Task-only 停点只展示精确 TaskRef
内存在的整体根 PRD，不猜选、伪造 key 或创建空切片。归档切片使用实际 archive
TaskRef 和对应 key。缺文件按真实结果报告，不改变 helper API。

## 匹配安装、在途接续与验证边界

已有安装须从同一受审来源成套更新 marketplace workflow、完整 preset、五个 Planning
packages、Readiness package 及声明平台投影。按官方 marketplace 先 `--create-new`
预览，核目标原文和 sidecar，再从同 provider 显式 `--force` 应用 workflow，最后
完整 preset apply/reapply。保留用户修改与现有受管 hash、`.new/.bak` 冲突机制，逐项
核真实 sidecar、mode、installed 调用及 drift。源码修改不会自动更新既有业务安装。

旧完整安装在显式成套采用前保留原版本；不能把某一新诊断字段或一段提示单独应用到
旧 caller。没有持久 schema 迁移或运行期双读。当前 Task/Delivery 身份、原规划、
适用 producer 输出和已发生的 Git/GitHub 事实保留；真实前序失效回原 producer，
不转换旧 semantic pass，也不为恢复另建 Task/Delivery。

定向验证覆盖正常原 owners 补缺和原义务接续、首失败与真实失配、无 context、
standalone 正向/构造错误恢复、实际展示命令与缺文件/Task-only/archive，并保留
#548/#443/#396 的原能力。源码/package、安装投影及真实原生 Agent 结果分别报告。
一个代表 clean 安装及 reapply 不代表完整多平台 Release/Upgrade 矩阵；未运行的
平台、已有业务安装和外部现场不得由文本、parity、fixture 或人工恢复推定通过。
