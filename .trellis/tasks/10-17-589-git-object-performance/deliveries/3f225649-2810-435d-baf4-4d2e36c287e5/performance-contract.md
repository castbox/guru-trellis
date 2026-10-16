# D1 修复前基线与固定验收合同

## 来源和计时口径

开发基线B=3676b9ee65834ef3720f2ff5cc0d8330afcea6ed，包含#588。canonical诊断在primary源码路径执行；期间main推进至486c4ae0e658b4a677a0bee61ac01a30d5391cdf（#592 Intake Markdown），本次实际被测Merge/runtime/官方API字节与B一致，未将#588收益计入本Issue。installed组来自本Task的B源码经匹配Fork真实init和原preset apply生成，再由原fixture在新Git上下文原reapply执行。

环境：macOS 27.0.1 arm64，CPython 3.14.8（受管venv），Apple Git 2.54.0。Fork为2a6f10ba3c0a2f27e0587e49e6c2f9b6a1f9d9d0，CLI/Core 0.7.0-castbox.3。PATH旧CLI0.6.17未用于本安装。

每组用新临时Git历史与相同资产生成法；不声称cold cache，不强制清OS cache。资产创建/提交/前置gate在prepare_seconds单列；原入口内的对象准备、wrapper、客观检查、公共store和固定调用均纳入operation timer。每组同一公开input执行两次：manual分别为初次记录和丢失stdout后的原结果恢复，固定差额单列；history两次为同一固定截点只读查询。以两次的中位数比较对应before/after，保持相同状态序列。没有并行性能压测。

Git计数来自PATH薄Git入口设置的Trace2，覆盖原入口全部Git子进程，包含官方子进程，即使官方清理GIT_*环境也保留观测。cat-file/show/ls-tree单列在raw summary；计数分析在timer外，不把controller读取trace的RSS冒充产品runtime。Git内容读取量以成功返回的blob字节定义，不声称磁盘物理IO。

GitHub响应使用原fixture的本地CLI provider：网络等待为0/未测live GitHub，fixture provider进程耗时属于本地automation，不能作为远端发布证据。真正native交付由本Task后续Delivery owner独立证明。

## 修复前重复测量

| 组 | 两次秒数 | 中位秒数 | Git进程数 | after最高中位秒数（20%改善） |
| --- | --- | --- | --- | --- |
| 1000-duplicates | 24.712171 / 25.020547 | 24.866359 | 2017 / 2012 | 19.893087 |
| 10000-duplicates | 255.818714 / 251.870248 | 253.844481 | 20017 / 20012 | 203.075585 |
| 10000-unique-recheck | 244.285301 / 263.385868 | 253.835584 | 20017 / 20012 | 203.068468 |
| 100-duplicates-history | 5.052449 / 5.120440 | 5.086445 | 416 / 416 | 4.069156 |
| 1000-duplicates-history | 46.853973 / 45.891777 | 46.372875 | 4016 / 4016 | 37.098300 |
| 10-paths-2-deliveries | 1.651072 / 1.702338 | 1.676705 | 109 / 109 | 1.341364 |
| 10-paths-4-deliveries | 2.850873 / 2.904260 | 2.877567 | 215 / 215 | 2.302053 |
| installed-before-1000-duplicates | 27.109085 / 26.845136 | 26.977111 | 2017 / 2012 | 21.581688 |

manual1000/10000均有app.txt和一个16MiB大blob：候选1002/10002路径；duplicate资产唯一blob65（含大blob），unique资产唯一blob10001；另有app blob1。路径blob总字节分别20873224/57737224，duplicate唯一内容17039368字节，unique大档57737224字节。multi组每Delivery固定12路径，资产唯一11 blob、16818176字节；每Delivery app内容独立。实际跨Delivery请求/唯一OID及读取量在after体积profiling中与before Trace2逐OID对照。

## 内容读取/摘要与其他校验拆分

另一个相同源码的dispatcher profiling pass保留全部objective consumers，用cProfile区分读取/快照和官方candidate_content_ref；原完整wrapper wall-time仍以表中plain pass为准，不将两个不同pass的耗时硬加总。

| 输入 | dispatcher总秒 | 候选可读性元数据秒 | 重建（含官方hash）秒 | 官方hash秒 | 本地provider秒 |
| --- | --- | --- | --- | --- | --- |
| manual 100 | 3.053960 | 0.000000 | 2.587935 | 0.026577 | 0.148869 |
| manual 1000 | 25.155117 | 0.000000 | 24.582535 | 0.227000 | 0.155865 |
| history 100 | 5.443097 | 2.524157 | 2.599515 | 0.029431 | 0.087610 |
| history 1000 | 69.166976 | 39.459463 | 29.298234 | 0.375965 | 0.107636 |

## 实施前固定标准

1. 表中每组原公开入口的本地automation中位耗时至少改善20%；对应读取/重建热点在同样profiling法的100/1000两档也至少改善20%。官方hash保留原算法，其重复hash上游缺口不冒充本批已优化。
2. canonical runtime最大单进程RSS<=100MiB、Git<=24MiB；installed/dogfood runtime<=128MiB、Git<=48MiB。MiB=1048576字节。依据独立BSD time profiling：canonical恢复runtime69517312/69238784字节、Git最大6094848；installed恢复runtime87261184字节、Git最大22052864。数值保留约25%加一个16MiB对象缓冲并向上取整，以支持必要元数据和原hash的大对象瞬时内存；并非生产拒绝阈值。
3. RSS由运行实际wrapper的单个Python runtime进程及各Git命令分别采集；wrapper最终exec Python，Git单独profile，最大值不相加，也不声称同时进程组总内存。fixture准备/controller/installer的峰值单列，不计作恢复runtime本身。内存profiling是独立pass，不混入wall-time对照。
4. 相同调用内相同blob只向Git请求一次内容；元数据按实际64KiB argv预算分块。相同候选输入保留路径/mode/删除和官方digest，正常缺失/读取失败、固定截点、隔离准备、原结果恢复和可变ref刷新维持原合同。
5. 先固定本合同，再写生产代码。after不放宽标准；失败按原owner修订实现或补齐真实证据。

## 原失败样本

首次unique大档初次操作249.980669秒成功，但第二次在upstream.delivery_api前置返回stale_identity，未作为通过组。新诊断在每次操作前检查六个官方API文件，完整重测244.285301/263.385868秒且两次都返回原delivered。没有修改生产代码、伪造通过或把重测声称为修复该安装前置错误；原失败独立保留。

## 被测源码内容身份

- trellis/skills/guru-team/packages/guru-merge-task-delivery/runtime/manual_recovery.py：a293b7579d3fa56d9d39d134457ba5b7557dbca9da510770a0e61dd3c377434e
- trellis/skills/guru-team/packages/guru-merge-task-delivery/runtime/history.py：e1b82b05ad7e5f92710723435f08f209fff4cd8ded9f39373c22126a342457a7
- trellis/skills/guru-team/runtime/delivery_projection/adapter.py：2ee9f2fd9d9e425ab7dfd835630ce99388e092be53a32ec24b43adbcbb39ea0a
- .trellis/scripts/common/delivery_store.py：7feea8298eea9b07f7910b9900b4232d8a38e26dbb5e5220bec7ce9b8fd5b663

## 剩余完成边界

D1只交付Guru历史/恢复读取与本批证据；全流程未测计数、continuity、生命周期及联合回归由D2/D3保留。当前Fork以及已读取的上游main b0d87f952043058e21001a002b661bf2db56b1fa仍有官方Task创建逐路径show与candidate_content_ref逐路径重复hash。原公开API没有预计算content hash或Task唯一性批量输入；不补丁官方副本。上游前置未交付时，对应范围和整体#589不能计完成。
