# D3 生命周期对象读取设计

## 内容范围

开发基线main@3676b9ee65834ef3720f2ff5cc0d8330afcea6ed；原content_base已选择最近实际已交付且属于当前HEAD祖先的D2 head c422692bca2d385a264da4db0030612b1b306fe1作为本批固定B。PR目标main，D1/D2及#588已在B，不重复收益，不自动追赶base。当前独立candidate_assessment为no_architecture_impact；不创建contribution/ADR。

## 最小共享传输

原Merge CandidateObjects继续拥有候选路径、支持mode/type、metadata分块、snapshot、原错误和历史/恢复规则。仅把它已经实现的有限唯一OID request/response spool传输移至runtime/git_object_batch.py，供Merge和生命周期两个真实consumer使用；不把业务身份、摘要、语义门禁或Stage状态移到shared。

实例固定实际repo并仅存续当前调用。完整唯一OID request预写普通临时文件，Git stdout写普通临时response文件，stderr保留原错误；Git完成后按OID/type/size/完整换行/EOF解析，内存只保留metadata和offset/size，内容按需单对象读出供原JSON解析，或<=1MiB复制快照。不同路径保留各自贡献，原Merge请求种类和no_lazy_fetch用途保持。合法missing响应必须由原caller按其原合同消费；生命周期原show失败且commit存在时返回None的兼容行为保留，tree/blob类型按原show的可读结果保持，不把传输截断当路径缺失。不能把截断/无效header/Git真实读取失败当完整成功；错误仍映射各自既有领域错误。无双pipe、线程、timeout、锁、跨调用cache或未来扩展策略。

## 生命周期事实与原调用者

在原task_lifecycle事实边界提供调用期reader（git_facts.py），不对外新增schema/CLI/API。metadata以实际repo、immutable commit和精确path绑定；成功ls-tree能证明该commit中路径缺失，无须对同commit再cat-file -e。可变ref每次解析，local refs/worktree/index不跨操作缓存。创建按unique head遍历Task子树，blob内容跨head按OID唯一取入spool；每branch/path仍由composition独立解析Task id、重复TaskRef及错误，原官方writer继续调用。

branch_resolution只对当前合法候选head及目标Task path取事实。原guru-establish-task-branch-binding首次invoke先resolve再establish内部再resolve，向这两个现有调用显式传同一个reader，复用仅不可变metadata/content；每次原worktree/ref/绑定/ownership/候选唯一性/expected head仍独立确认。普通direct调用无外部reader时自管调用期reader。不能以第一次candidate判断替代第二次当前输入检查。历史Issue候选在原identity owner收集各archive的Task/summary路径后批量取内容，每archive独立执行原source、seal、generation和唯一性规则。

其余commit_path_bytes的固定少量Reactivate/封存检查保留原合同；Cleanup的资源扫描需在最终全步骤清单中据真实增长和重复事实逐项判定，不因包含show自动扩张，也不将仍属目标的真实热点移出责任。

## 分发与源头

新shared文件必须进入既有skill_runtime_inventory.py，原apply的两处consumer负责装入；不新增installer旁路。canonical修改后由原tools-only及apply/reapply同步dogfood/代表性installed，核对runtime、packages、声明平台、mode、drift和逐个sidecar；.trellis/scripts保持零diff。对同事/业务现有安装无写入。

## 来源承接（唯一矩阵）

| 来源 | 原承诺与处置 | 当前落点/理由 |
| --- | --- | --- |
| #5893.3第三项、5.1/5.3 | retain：减少逐file show、重复对象/摘要，调用期真实repo/immutable绑定 | 原composition/branch/identity读取加最小技术reader，不复用semantic pass。 |
| #5893.2、6–8 | retain：全步骤盘点、真实增长两档、先before固定门槛、正式链量化 | 本D3性能合同/结果及最终清单；fixture/native/live分开，失败不记通过。 |
| #5895.2、#579 | retain：可结束有限传输与受限内容内存 | 普通request/response spool与<=1MiB复制，不构造双pipe互阻。 |
| #5895.4/5.6/5.8 | retain：每输入检查、原owner、摘要/类型/mode/path/缺失错误保持 | shared只技术字节，原caller业务解释不迁移，新旧对照和原完整链验证。 |
| #5895.7、#588/#567/#569/#557 | retain：canonical/原安装、固定base、历史截点、原恢复 | 不patch上游，不追赶base；D1/D2/#588联合回归保留不同场景的原consumer。 |
| #5895.7及AC15 | retain：不可分离上游前置未解决不计完成 | 官方task_store writer逐path读取及delivery_store重复hash仍完整保留和量化，不能用Guru改造或盘点声称完成。 |

原Clarify source_selection为空，没有另一个normative design；上述约束直接来自live Issue与整体scope。

## 验证策略

全部source16+installed6组before已完成；数值、资源与同口径方法已在performance-contract.md于生产修改前固定，Architecture结果不替代Approval/Activation。创建+ensure使用10/100个原官方writer生成的已有Task，固定其他主要规模；首次branch binding使用10/100个无目标Task的其他分支，固定Task/worktree/内容。每轮fresh等价fixture，恢复单列。源真实公开wrapper、全部validator及官方writer在timer内，准备/对象大小分析在外；timing、volume、RSS、纯profile分开，独立记录读内容/摘要与其他校验、必要遍历、GitHub网络/总时。BSDtime的wrapper/同步官方Python child不可分离max与Git单进程max明确边界。

after同before工具/输入/依赖口径，固定门槛失败就修当前实现，不降标准。覆盖Task重复/casefold/历史/归属、合法缺失与实际失败、特殊path/type/mode、移动ref/相邻worktree/index、OID去重/调用期复用与每input独立检查。最小共享提取触及D1传输，需原Merge历史/恢复与摘要等价回归；D2流式及#588后冲突resolved→当前Check→完整Review、无冲突实际整合bounded连续性各走原入口，不能互相替代。原正式根调用Trace与fixture补齐Closure/Finish/Cleanup计数，不把不可执行边界记通过。

本批完整Check/精确Commit/独立全B..HEAD Architecture与Review/Readiness/Publish/Merge后，原Completion仍必须检查全部AC及上游前置；未满足不得关闭#589。完整多平台/Release矩阵归#575，local_candidate不证明formal_fork_source_lock、正式版本发布或业务采用。
