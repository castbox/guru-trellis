# D7 读取与计算去重结果

## 范围与实际来源

B=865f4a9576eabc85cb3b91e74ecd856785095510。before为该生产代码及Fork c7bd746/CLI-Core.3；after为本批未提交生产差额及Fork9f40ec7/CLI-Core.4。完整SHA/tree/parents/CI与包对照由source lock和validation.md拥有。测量时正式Task及原代表installed仍是D6来源；下列installed_template只指clean .4代表candidate，不表示两正式目标已升级。

当前验收引用Issue589§6和performance-contract.md首节，以冗余读取/计算消除、独立检查保留和资源有界判断。原冻结数字、初轮FAIL及counterfactual均保留，不改称PASS。

完整before/after各16cell、32次fresh plain。after另有64份volume/RSS/profile/hash观察，采集driver34操作全部exit0并实际结束。汇总missing0/errors0。全部cell的paths、完整mode/type/blob条目与content_ref逐份等于before；不要求或声称完整HEAD/tree相同。

计时使用相同冻结V2工具和真实原wrapper；缓存/预热、Python3.14.8、Git2.54与计时拆分方法保持。四项测量工具hash逐一等于before V2，当前消费者代码等于plain freeze。必要的.3→.4来源差额已独立说明。fixture网络等待为0，不能替代live GitHub/provider/native证据。

## 内容、hash与文件读取

before已经按OID去重Git body请求，本批不重复认领这项收益。本批消除Guru临时snapshot物化后的重复文件读取/hash，并移除history摘要前的预读。每份输入仍执行自己的结构/身份/关系/祖先/expected/cutoff/恢复检查。

| cell | after body请求/唯一OID | after body/hash输入bytes | 内容hash次数 before→after | 旧snapshot文件读取bytes before→after |
| --- | ---: | ---: | ---: | ---: |
| source-manual-128-duplicates-d1 | 66/66 | 17039368/17039368 | 130→66 | 17301512→0 |
| source-history-128-duplicates-d1 | 66/66 | 17039368/17039368 | 130→66 | 17301512→0 |
| source-history-128-duplicates-d4 | 69/69 | 17039401/17039401 | 520→69 | 69206057→0 |
| source-manual-128-unique-d1 | 130/130 | 17301512/17301512 | 130→130 | 17301512→0 |
| source-history-128-unique-d1 | 130/130 | 17301512/17301512 | 130→130 | 17301512→0 |
| source-history-128-unique-d4 | 133/133 | 17301545/17301545 | 520→133 | 69206057→0 |
| installed_template-manual-128-duplicates-d1 | 66/66 | 17039368/17039368 | 130→66 | 17301512→0 |
| installed_template-history-128-duplicates-d4 | 69/69 | 17039401/17039401 | 520→69 | 69206057→0 |
| source-manual-10000-duplicates-d1 | 66/66 | 17039368/17039368 | 10002→66 | 57737224→0 |
| source-history-10000-duplicates-d1 | 66/66 | 17039368/17039368 | 10002→66 | 57737224→0 |
| source-history-10000-duplicates-d4 | 69/69 | 17039401/17039401 | 40008→69 | 230948905→0 |
| source-manual-10000-unique-d1 | 10002/10002 | 57737224/57737224 | 10002→10002 | 57737224→0 |
| source-history-10000-unique-d1 | 10002/10002 | 57737224/57737224 | 10002→10002 | 57737224→0 |
| source-history-10000-unique-d4 | 10005/10005 | 57737257/57737257 | 40008→10005 | 230948905→0 |
| installed_template-manual-10000-duplicates-d1 | 66/66 | 17039368/17039368 | 10002→66 | 57737224→0 |
| installed_template-history-10000-duplicates-d4 | 69/69 | 17039401/17039401 | 40008→69 | 230948905→0 |

16cell均满足实际观察事实：body请求数等于唯一OID数，body bytes等于unique bytes，hash_blob实例/输入分别等于唯一blob数/bytes；failed、uncaptured、unavailable均0。snapshot文件读取为0仅指旧delivery_store候选快照读取，不声称Git传输没有必要临时文件I/O。D4保留四份不同app候选各自的aggregate；不同路径贡献完整。

公开context按最多4096项分块，首批commit info占1项；hash按64KiB流式消费regular temporary output。literal路径tree查询按64KiB参数预算分块，128路径为1次、10000路径为3次；D4分别为4/12次。batch数量由资源边界和每输入验证产生，不是逐路径进程。原Task/local_commit128批合同没有被替换。

同一操作内复用实际root和完整OID的内容摘要。history切换到原隔离bare root时关闭并重建context；每个输入的缓存blob仍由public API批量验证类型/可用性。manual同OID terminal endpoint只prepare一次。必要的PR/parent/first-parent/unfiltered delta及逐输入检查保留，既有功能测试与正式wrapper结果另见validation.md。

## 完整自动化耗时及Git操作量

时间是观测，不设最低改善门槛。每行after为两次fresh原wrapper，包含固定验证与本地provider进程；profile/hash/RSS时间不混入plain。Git顺序为git/show/cat-file/ls-tree，分别列出两样本。

| cell | before median s | after 两样本s → median s | after Git 两样本 |
| --- | ---: | --- | --- |
| source-manual-128-duplicates-d1 | 0.669697 | 0.621322, 0.624610 → 0.622966 | 13/0/3/1; 13/0/3/1 |
| source-history-128-duplicates-d1 | 0.535389 | 0.494944, 0.491556 → 0.493250 | 7/1/2/1; 7/1/2/1 |
| source-history-128-duplicates-d4 | 0.994267 | 0.834050, 0.830458 → 0.832254 | 22/4/8/4; 22/4/8/4 |
| source-manual-128-unique-d1 | 0.675595 | 0.676354, 0.734948 → 0.705651 | 13/0/3/1; 13/0/3/1 |
| source-history-128-unique-d1 | 0.543802 | 0.553075, 0.523038 → 0.538057 | 7/1/2/1; 7/1/2/1 |
| source-history-128-unique-d4 | 0.992414 | 0.929951, 0.808426 → 0.869188 | 22/4/8/4; 22/4/8/4 |
| installed_template-manual-128-duplicates-d1 | 0.715465 | 0.719092, 0.695594 → 0.707343 | 13/0/3/1; 13/0/3/1 |
| installed_template-history-128-duplicates-d4 | 1.061362 | 0.925165, 0.847255 → 0.886210 | 22/4/8/4; 22/4/8/4 |
| source-manual-10000-duplicates-d1 | 3.213828 | 1.361836, 1.411214 → 1.386525 | 15/0/3/3; 15/0/3/3 |
| source-history-10000-duplicates-d1 | 2.816496 | 1.047078, 0.993163 → 1.020120 | 9/1/2/3; 9/1/2/3 |
| source-history-10000-duplicates-d4 | 9.986937 | 2.854959, 2.683268 → 2.769114 | 30/4/8/12; 30/4/8/12 |
| source-manual-10000-unique-d1 | 3.309054 | 1.617974, 1.505724 → 1.561849 | 17/0/5/3; 17/0/5/3 |
| source-history-10000-unique-d1 | 3.033269 | 1.157355, 1.229138 → 1.193246 | 11/1/4/3; 11/1/4/3 |
| source-history-10000-unique-d4 | 10.116239 | 3.101305, 2.975178 → 3.038241 | 38/4/16/12; 38/4/16/12 |
| installed_template-manual-10000-duplicates-d1 | 3.193050 | 1.441448, 1.408148 → 1.424798 | 15/0/3/3; 15/0/3/3 |
| installed_template-history-10000-duplicates-d4 | 10.273913 | 2.662990, 2.625475 → 2.644233 | 30/4/8/12; 30/4/8/12 |

小档计时有波动，旧源码counterfactual也未复现最初median，不能据此替换baseline或选样。大档的实际耗时下降与snapshot重复读取/hash消除方向一致；本结果不把时间相关性当作独立因果分解。精确profile函数逐项cumulative见原汇总，不对嵌套行求和，也不与plain相减。

## 资源观察

RSS单位bytes。wrapper为BSD time观察的wrapper及其后代最大单进程，既非纯Python，也非同时进程组总量；Git另取逐进程最大。

| cell | wrapper before→after bytes | Git after bytes |
| --- | ---: | ---: |
| source-manual-128-duplicates-d1 | 41615360→37912576 | 5685248 |
| source-history-128-duplicates-d1 | 41435136→37617664 | 5767168 |
| source-history-128-duplicates-d4 | 41582592→38207488 | 5767168 |
| source-manual-128-unique-d1 | 40517632→37896192 | 5619712 |
| source-history-128-unique-d1 | 41697280→37863424 | 5767168 |
| source-history-128-unique-d4 | 41697280→38043648 | 5750784 |
| installed_template-manual-128-duplicates-d1 | 42893312→39108608 | 22085632 |
| installed_template-history-128-duplicates-d4 | 43450368→38879232 | 22085632 |
| source-manual-10000-duplicates-d1 | 55115776→58556416 | 9306112 |
| source-history-10000-duplicates-d1 | 56803328→51232768 | 11239424 |
| source-history-10000-duplicates-d4 | 87523328→81428480 | 11239424 |
| source-manual-10000-unique-d1 | 62210048→61030400 | 22446080 |
| source-history-10000-unique-d1 | 53313536→52953088 | 22446080 |
| source-history-10000-unique-d4 | 84901888→82198528 | 22429696 |
| installed_template-manual-10000-duplicates-d1 | 62701568→61751296 | 9486336 |
| installed_template-history-10000-duplicates-d4 | 80887808→80347136 | 11485184 |

source manual10000 duplicates的wrapper单进程峰值由55,115,776升至58,556,416bytes，差额如实保留。其他15cell低于对应before。结合4096有限batch、64KiB流式hash与只保留tree/hash事实的实现，未发现整批body常驻；不能仅凭该峰值把差额精确归因到某个分配点。after wrapper总范围37,617,664–82,198,528bytes，Git最大22,446,080bytes。

## 证据与剩余边界

before：/tmp/guru-589-d7/before-summary-final/summary.json。after：/tmp/guru-589-d7/after-summary-work-acceptance/summary.json及summary.md；跨before逐候选与读取/hash比较：/tmp/guru-589-d7/current-work-elimination-comparison.json。原始命令、stdout/stderr、trace、实际root probe及每pass文件保留在这两个汇总指向的目录。

最终源码Check、committed独立完整Review、适用知识晋升和D7交付仍须完成。最终Task/代表installed从clean source正式采用、native/live受影响链、最终库存和整体Completion由原后继负责。#575完整Release矩阵、Guru正式版本发布、业务仓采用均未声明通过。
