# D2 执行计划

## Delivery Policy

staged：本批独立交付原bounded continuity内容读取/摘要优化。入口为整体accepted scope、D2原Creation及独立candidate_assessment；出口为固定性能/内存标准、新旧摘要/原公开链/安装投影通过，随后正式Check、TaskCommit、独立完整BranchReview、DeliveryReview、Publish/Merge（Refs #589）。D1已交付；D3及上游缺口由整体Completion继续承接，不能关闭Issue。

## 次序

1. 使用现有正式schema2 PR fixture测source三档及代表性installed before；所有wrapper和校验保留，计时/volume/RSS/profile独立。
2. 依据全部before固定performance-contract.md数值门槛，写明热点与完整链边界、fixed wrapper成本，不依after放宽。
3. 原同D2实施已开始，混合profile方法已修订为固定B纯cProfile及独立hashes。双普通文件response方案在真实after的unique完整链未达3%，因此暂停并经同D2原Author及独立candidate_assessment改为当前单向流式候选；数值/RSS门槛不降。完成当前Wording/final Architecture/Approval/Activation后继续，不把旧失败计通过。
4. 原tree_identity采用design唯一的预写request文件+单向stdout pipe+stderr文件方案，替换response整批落盘路径；按<=1MiB解析/hash及有限EOF/drain/wait保持原错误。record与同次validate显式共享memo，独立wrapper保留各自验证；不增公共API/持久缓存。
5. 原真实Git测试改为观察Popen的stdin/stderr普通文件和stdout单向pipe，验证新旧摘要、唯一OID/hash、正常缺失/读取失败及进程收尾；其余原公开链完整保留。按同before方法统一测新candidate，失败修实现不降门槛。
6. 原tools-only/installer同步dogfood及代表性installed，逐项处理sidecar，检查mode、声明平台、reapply/drift、原生scripts零diff。
7. fresh Phase2/TaskCommit与独立完整B..HEAD Architecture/BranchReview、DeliveryReadiness和原Publish/Merge。后续D3覆盖全部正式入口计数与联合回归。

## Docs SSOT

no_docs_update_needed：只改变原技术内容读取/计算，不改变公开行为、schema、phase或Architecture/RDT authority。性能合同/结果由本Delivery唯一承接，design.md独占来源承接矩阵。若实际scope/owner/机制边界改变，回原Author/Architecture及资格owner。
