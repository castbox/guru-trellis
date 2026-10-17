# D3 生命周期对象读取与全流程联合回归

Direct Source为#589第3.2/3.3第三项、第5–8节；整体责任仍以Task根prd.md AC01–15为准。D1/#593与D2/#594已交付，不重复收益；内容基线由原content_base选择当前已交付祖先c422692，PR目标main，不默认追赶。

本批消除Guru Task创建、Task/branch/checkout及历史身份解析中的逐文件show和路径缺失后的重复对象检查；同调用按实际repo/immutable对象复用元数据与唯一blob内容，保留每输入身份、代次、重复、历史和归属判断。仅当有原Merge与生命周期两个真实caller同技术职责时提取最小有限OID传输，不迁移业务摘要或判断，不建通用Git框架、持久缓存、新公共API/schema/config。内容读取/解析/落盘与内存策略在独立候选设计中固定。

先以现有真实公开wrapper测历史Task数和branch数两档before，包含官方writer与全部校验，随后固定热点/本地全链耗时及单进程RSS门槛，再改生产；相邻操作、缺失/读取失败、路径/类型/mode和归属保持。通过原安装同步canonical/dogfood/代表性installed，并完成完整流程实际计数及含#588的联合回归，区分fixture/native/live证据。

官方task_store创建逐路径读取及delivery_store重复hash的上游前置仍属整体未完成责任，不能以本批Guru优化或盘点代替；不得patch .trellis/scripts/全局npm/node_modules/hook、跳过唯一性检查或复制摘要算法。本批若独立交付，仅Refs #589；全Task未满足时不关闭，不自动做Release矩阵或业务仓升级。
