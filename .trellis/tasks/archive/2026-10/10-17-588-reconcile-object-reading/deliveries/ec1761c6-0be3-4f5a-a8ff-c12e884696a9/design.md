# D1 设计：保持原摘要的批量对象读取

## 当前 authority 与固定范围

Direct Source 为 castbox/guru-trellis#588 当前正文；整体 AC01–AC10 位于 ../../prd.md。本 Delivery 的固定 development/content baseline B 为 main 的 `1b2c30b4b1a326f2276c96f0d155605bf2cb1775`，来源为显式选定 development baseline；Planning H0 同 B，最终 H 由实际实现提交决定。PR target 单独为 main，不把最新 target 当内容范围。使用既有 DeliveryProjection.content_base 恢复同一 B。

独立 Architecture candidate_assessment 已正式返回 baseline_current：适用 Baseline current-main-0.6.17-guru.94、constitution guru-trellis-design-constitution-v1；判定 no_architecture_impact。修改仍由 Reconcile deterministic runtime 拥有；无 owner/authority/public contract/persistent state 变化，无 contribution/ADR。final_plan 与后续独立检查仍按原 workflow 执行。

## 唯一实现机制

1. common.index_tree_digest 保留 `ls-files --stage -z` 解析、stage0 验证、索引路径原字节和顺序。gitlink 行仍为 path/NUL/160000/NUL/OID/NUL，不读取该 OID 对象。
2. 普通、可执行和符号链接 entry 按首次出现收集唯一 blob OID；一个扫描只发起一个 cat-file --batch。临时文件作 stdin，请求写完并 seek(0) 后启动 Git；stdout 也为临时文件，Git 完成后从头按 header、声明字节数、分隔换行解析。以不超过 1 MiB 分块更新每个唯一 blob 的 SHA256，保留 OID→内容摘要，不保留对象完整内容。正常缺失对象、读取失败、非 blob 或不完整响应返回原 candidate_failed/repository.index 类错误。
3. 最终按原 entry 顺序组成 path/NUL/内容SHA256/NUL，并累积最终 SHA256；保持 mode-only 身份语义。禁止用 Git tree OID 取代业务内容摘要。
4. committed_tree_digest 每次 fresh resolve 实际 HEAD tree OID，以该不可变 tree 加载临时索引。invoke 创建仅本调用存在的 memo，键为实际 repository + tree OID，并传给两次 validate_result。第二份输入仍执行原 schema/facts/Task/Delivery/base/receipt/ancestry/expected digest 校验；只复用原内容计算。独立命令和可变索引不共享 memo；候选、整合前后校验保留。
5. 不新增通用 subprocess framework、跨包 private import、依赖、持久缓存、schema 或退出。临时输出占用磁盘与唯一 blob 总字节成正比，退出自动释放；内存与 entry/唯一摘要数量加固定读取块成正比。

## Source-design disposition（唯一表）

source_selection 没有额外 normative design 文档；以下保留 Issue 明确要求及其引述的既有约束。历史文档不是新的范围授权。

| 来源/原承诺 | disposition | 落点/影响/上游处理 |
| --- | --- | --- |
| #588 修复范围1–4：批量、去重、调用内不可变树复用 | retain | common.py 与 invoke.py；无公共 consumer 改动 |
| #588 修复范围5、#397 design：摘要字节/gitlink/正常恢复 | retain | 原路径行算法、gitlink pointer 及全部 execute/resolved/record/check/invoke；无合同降级 |
| #579 design：临时文件 stdin 避免双向管道阻塞 | retain | 新批量传输只用完成后读取的临时文件；不复制其它 package 的全量 stdout 缓冲 |
| #567 design：不新增追赶义务、固定 B | retain | 只优化原确有需要的整合，不添加 fetch/rebase/reconcile 路由 |
| #588 验收：性能、资源、完整正式入口及安装证据 | retain | 下列冻结合同与 implement 验证；Completion逐项核对 |
| #588 交付边界：工具/发布/业务采用独立 | retain | PR Refs #588；Completion/Closure 收尾，不声明版本或业务升级 |

所有承诺 retain，不存在 change/reject 或待处理上游需求变更。

## 实施前冻结的基准合同

原源码 B=1b2c30b4b1a326f2276c96f0d155605bf2cb1775；该未修改 primary checkout 作为原实现来源。修复后报告实际源码 commit、工作树内容及 installed 来源。环境 macOS 27.0.1 arm64、Apple Git 2.54.0、managed CPython 3.14.8；相同本机本地磁盘、同工具与 fixture。无清理 OS cache、无专门预热，各种树重复两次取中位数（两值均值）；报告两次原始数值。机器维持日常负载，明确这是本机 wall-clock 对照，不作跨机 SLA。

fixture 复用原 Reconcile RuntimeTest 的实际 Git history：old→new base 与从 old 分叉的 task；新增 assets 后实际整合 new base。10000 个 16 KiB 文件，bytes=SHA256(str(value))重复512次；duplicates 的 value=n%64，unique 的 value=n。再加一个16 MiB文件（bytes(range(256))重复65536次）。资产10001文件、加原fixture3文件，总索引10004；duplicates唯一资产blob65、17,825,792字节；unique唯一资产blob10001、180,617,216字节；最大blob16,777,216字节。重复资产比例分别约99.35%与0%。两版输入内容/历史拓扑/验证命令相同，提交日期差异不影响树内容。

完整自动化链计时分别包围实际 canonical wrapper candidate、reconciliation、record、check、invoke，包含包装器/机器校验；固定 candidate validation_commands=[[git,diff,--quiet]]。fixture semantic payload仅测试确定性传输，不声称原生AI审查。记录每阶段耗时、总和、GIT_TRACE2 Git进程/cat-file数及 checkpoint consumed、正式reconciled。AI审查、人类停顿、fixture创建和其它workflow阶段不进入计时。额外对子进程内的 index_tree_digest 计时，单独报告摘要阶段。完整链其余开销为整链时间减独立摘要测量所估内容时间，必须标为估计，不声称精确分解。

资源：完整链每wrapper用 /usr/bin/time -l 的 maximum RSS，作为该命令/后代的 high-water测量，非同时进程组RSS之和；摘要子进程使用 getrusage SELF与CHILDREN分别测Python本身及已结束Git子进程最大RSS。macOS数值单位bytes。相同口径前后对照。

**冻结通过标准**：duplicates 与 unique 各自，摘要阶段中位耗时与完整链中位耗时均须达到原实现/修复实现 >=5.0；每个完整wrapper峰值RSS中位数、摘要Python与Git各自峰值RSS中位数均须 <=对应原值+33,554,432 bytes。正常大树两轮均完整返回正确退出且checkpoint已消费。原duplicates完整链已测786.231/717.176秒（中位751.704），每轮70028 cat-file；阈值依据此完整基线及逐对象主导机制固定。unique原实现测量继续按此合同完成，不能按修复后结果改阈值。每轮扫描batch数最多1，同一唯一blob只请求/哈希一次，invoke两份验证同树只扫描一次；修复完整普通链预期6轮batch，不能以此代替耗时/资源标准。

## 兼容与分发验证

独立旧算法oracle覆盖普通/可执行/符号链接/空/二进制/重复blob、tab/newline/非ASCII路径与未初始化gitlink；正常缺对象保留错误。真实公共wrapper覆盖普通完整链、无关staged/unstaged/untracked恢复、preimplementation resolved baseline、postreview continuity、postimplementation resolved candidate和同提交恢复；保留原consumer区别。

canonical修改后 apply.sh 同步本worktree dogfood及声明平台副本，执行reapply、drift、package inventory、源/installed字节和mode核对、零遗留sidecar；在一个代表性干净安装target通过实际installed普通正式链与定向兼容检查。只验证本Issue投影，不执行完整Release多平台矩阵，也不升级业务仓。
