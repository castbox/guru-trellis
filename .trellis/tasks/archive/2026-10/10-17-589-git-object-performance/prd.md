# #589 Guru 全流程 Git 对象读取性能治理

## 唯一来源与整体责任

Direct Source：[castbox/guru-trellis#589](https://github.com/castbox/guru-trellis/issues/589) 当前完整正文。开发基线 main@3676b9ee65834ef3720f2ff5cc0d8330afcea6ed 已含 #588 交付；#588/#579/#569/#567 的既有合同持续适用，不重做其范围。所有 Delivery 使用 Refs，整体完成后才由 Closure 处置 Issue。

## 整体验收

| ID | 当前责任与可观察完成结果 |
| --- | --- |
| AC01 | 全步骤盘点覆盖 Intake/创建、Planning/Activation、Implementation/Check、Commit/完整 Review、Delivery Review/Publish/Merge、Completion/历史查询、Closure/Finish/Cleanup。逐项记录入口、caller、对象、命令、增长因素、实际计数或明确不可执行边界。 |
| AC02 | 优化清单和保留清单处置全部盘点及第3.3节机制；仍存的同范围热点不得通过移出清单缩小责任。固定少量检查说明独立用途并实际计数。 |
| AC03 | 历史 Delivery 查询和手动恢复按用途批量取得元数据/内容，消除逐候选路径读取进程。保留候选重建、归属、固定截点、隔离和原恢复结果。 |
| AC04 | 实际整合后的 bounded continuity 按 blob OID 去重、限制内容处理内存，并消除同次调用同规则不可变树摘要重复计算；摘要字节和原 consumer 不变。 |
| AC05 | Guru Task 创建及 Task/branch/checkout 解析减少逐文件 show 和缺失后的重复检查；复用调用内不可变事实，保留重复身份、真实缺失、历史和归属判断。 |
| AC06 | 同批相同 blob 内容只请求一次，同算法/上下文的内容 hash 只算一次，保留不同路径贡献。每份输入独立检查结构、身份、关系、祖先、预期摘要和恢复结果。 |
| AC07 | 内容读取、解析与快照落盘策略固定；保持 #579 可结束的文件传输，禁止整批内容常驻内存或双管道互阻。复用只在调用内按实际仓库、不可变 OID 和计算规则绑定；可变 ref/index/worktree 每次刷新。 |
| AC08 | 以消除不必要读取、逐路径进程放大及同调用重复 hash 为完成目标，不设耗时改善百分比硬门槛。保留可比较的修复前基线、真实包装器/校验/固定命令、缓存条件及重复测量方法；记录必要依赖变化。耗时/RSS如实报告，资源有界，历史失败与旧指标未通过结果保留，不改写为通过。 |
| AC09 | 每热点按真实增长因素至少两档对照；上万路径覆盖高重复/大量不同内容和大对象；多 Delivery 改变数量且固定单候选规模；Task/branch 改变分支或历史 Task 数，固定其他规模。记录路径、唯一对象、读取字节、最大对象和分块依据。 |
| AC10 | 一次操作统计全部 Git 子进程，单列 cat-file/show/ls-tree、请求对象/唯一 blob/实际读取量；分列读取摘要、其他校验、网络和完整耗时。分别说明 Python/Git RSS 测量范围和单位，不冒充进程组内存。 |
| AC11 | 正式公开链验证普通完整流程、PR后冲突 resolved-candidate→当前 Check→完整 Review、无冲突实际整合 bounded continuity、手动合并与 stdout丢失恢复、本地完整/需准备历史、合法删除/缺失/读取失败、相邻操作可变输入刷新。不以底层测试替代正式链。 |
| AC12 | 保留受影响入口既有路径格式、文件类型、mode、删除、gitlink、摘要、typed exit、错误、归属和恢复；不以 tree OID 替换内容摘要。 |
| AC13 | canonical、dogfood、代表性 installed 原安装链通过；声明平台、mode、reapply/drift/sidecar定向验证，不扩大为完整Release矩阵。禁止改历史Task制造通过、修改上游脚本或其他现有业务安装。 |
| AC14 | 每份 Delivery 明确已完成热点、剩余工作与验证；整体完成报告实际候选提交、安装来源、性能证据和未验证边界，区分工具交付、正式发布和业务采用。 |
| AC15 | 上游前置只能由既有公开API或明确依赖承接；不可分离前置未解决时，对应范围和整体accepted scope不得计为完成。 |

## 有序切片

D1：全步骤盘点、测量合同与历史 Delivery/手动恢复热点。D2：实际整合后的连续性审查。D3：Guru 生命周期解析、全流程联合回归及整体证据收敛。各批取得其修复前基线并固定可比较测量方法；以冗余工作消除与兼容正确性验收，耗时/RSS为观测，不以预设改善数字驱动无关改造。每批独立 Planning、Check、完整 Branch Review、Delivery Review、Publish/Merge。

## 当前边界

仅优化 Guru 自有责任并按原安装机制投影；不新增通用 Git 框架、持久缓存、后台服务、公共schema/配置或审批链。AI语义门禁保持在原Markdown owner。当前发现 Fixed Fork task_store创建和delivery_store部分校验逐路径读取，需盘点和量化；没有上游公开能力时明确为缺失前置，不绕过、不隐藏或削减整体责任。
