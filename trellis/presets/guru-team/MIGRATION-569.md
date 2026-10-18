# #569 固定截点历史查询迁移

`discover-task-deliveries` 仍由原 Merge owner 提供。query1 输入1.0保持
trailer-only 历史/迁移语义，query2 输入2.0保持 public Task/Delivery 与合法
schema1/2 trailers 的融合、归属及去重。当前输出统一直接演进为
`delivery-history-result-3.0`，新增唯一必要字段 `cutoff_commit`：本操作观察的
真实远端 repo/base commit。其余字段仍为 schema_version、status、task_identity、
repo_ref、base_ref、deliveries。旧result1/2 schema/example只保留历史验证用途；
没有当前输出选择、双读adapter、fallback、缓存或长期ledger。

安装 owner 必须以同一完整候选同步切换 Merge package/runtime/interface/commands、
result3.0 schema/example、Completion正文及声明平台投影。按原安装/迁移能力完成
官方匹配模型和 Guru preset，运行 package/installed validator、apply/reapply、
bytes/modes与drift检查，逐项处置.new/.bak；不得只替换history.py或schema。
旧开发Task继续使用自身完整carrier，源代码修改不等于已迁移。工具/旧Task采用
仍由原owner负责，本变更不操作#566资源或业务仓，也不证明Release矩阵通过。

直接 consumer 用 query identity 核对公开 repo/base/task/cutoff；query2 的 TaskRef
来自原输入。B1之后仅有无关Task/记账前进时直接消费B1。明确本Task新增Delivery
或所需证据变化时，由原owner再查询实际缺少事实并重判受影响结论，不重跑旧业务gate。
结果丢失从原producer正常重入，新操作返回自己的明确截点；不承诺复原未观察旧B1，
不从私有checkpoint恢复覆盖范围。Completion无需为已有充分公共事实额外查询。

只读指不写业务/Task/Delivery事实。原query owner优先复用完整caller Git数据；
缺对象或shallow截断时，在调用内temporary bare context取得固定B1及有限必要
immutable事实对象，扫描/候选校验均读取该context。获取无destination ref并使用
`--no-write-fetch-head --no-tags --no-recurse-submodules --no-auto-maintenance`。
实际写入临时Git初始化metadata/config/objects/pack及既有candidate临时快照，退出即删。
caller/peer HEAD、index、工作文件、共享refs/objects/shallow/FETCH_HEAD/tags和远端资源
不写。网络/权限、必要数据或身份失败具体返回，不能伪装合法空数组或要求人工fetch。

验证须分别证明真实Git组件、matching installed公共Merge→query→Completion、
独立/恢复/丢失输出、固定截点实际消费、query1/query2归属、隔离与投影；fixture
provider或语义结果不冒充实际AI consumer/外部live证据。query成功不授予Completion、
Closure、Finish或发布结论。
