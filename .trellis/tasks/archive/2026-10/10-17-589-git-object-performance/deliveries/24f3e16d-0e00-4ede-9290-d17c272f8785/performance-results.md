# D4 性能与交付证据

## 实际候选与口径

内容B为dc57fc6ed5d1229c50520d74a1f6390a52469604，已含D1/D2/D3与#588；PR目标main。本批只改变Cleanup原owner，不计前三批/#588收益。after在提交前测量，Cleanup真实源码sha256=3c2fab2dbaf01f532f43c26f7c0d57e3c2eb9c830da05fc91261cd321152ad88，candidate.json同时记录当时HEAD=B，不能将HEAD冒充after内容；最终提交/PR由原TaskCommit和BranchReview精确绑定。

环境和固定门槛见performance-contract.md。source/installed×10/100×timing/profile/RSS/volume共16组，每组两轮fresh等价fixture；before与after的Python/依赖、Task blob/OID/481B、资源数、唯一head/路径、原wrapper/exit与冻结工具实际核对一致。comparison.json的28项数值检查全部通过，16组输入/exit一致，4份冻结工具hash保持。只证明数字与输入一致，不替代语义Check。

## 完整本地wrapper：秒与改善

| 来源/资源数 | preview before→after / 改善 | delete before→after / 改善 | hotspot preview/delete改善 |
| --- | --- | --- | --- |
| source 10 | 0.842701 → 0.715281 / 15.12% | 1.586169 → 1.288532 / 18.76% | 80.35% / 69.92% |
| source 100 | 5.262398 → 3.189822 / 39.38% | 13.154659 → 8.965692 / 31.84% | 97.89% / 77.84% |
| installed 10 | 0.902736 → 0.738774 / 18.16% | 1.673066 → 1.308480 / 21.79% | 80.40% / 69.48% |
| installed 100 | 5.594066 → 3.271440 / 41.52% | 13.518200 → 9.099326 / 32.69% | 97.87% / 78.59% |

preview和delete均达到10资源≥10%、100资源≥20%；hotspot达到≥30%/50%。source恢复0.274214/0.287089秒，installed恢复0.296144/0.293293秒，均在固定回归上限内，原cleaned结果与无再次删除保持。三次操作自动化耗时之和（preview+delete+recovery，不含操作间准备）source10约2.696→2.278秒、source100约18.701→12.443秒，installed10约2.866→2.343秒、installed100约19.425→12.664秒。GitHub网络均0秒；本地fixture不代表nativeAI或live远端/生产结果。

## 操作量、内容与内存

| 资源数/操作 | 全部Git before→after | show before→after | cat-file before→after | ls-tree before→after |
| --- | --- | --- | --- | --- |
| 10 preview | 63→46 | 12→2 | 0→1 | 10→2 |
| 100 preview | 513→316 | 102→2 | 0→1 | 100→2 |
| 10 delete | 143→106 | 22→2 | 0→1 | 20→2 |
| 100 delete | 1313→916 | 202→2 | 0→1 | 200→2 |
| 各档recovery | 3→3 | 0→0 | 0→0 | 0→0 |

source/installed数量相同。每次preview/delete的两次show用于原两个archive事实，独立用途与数量保持；一次batch只请求唯一Task blob；两次树读取分别保留原--name-only路径筛选和既有reader元数据准备。相同head多资源不再重复Git内容/树读取。逐资源ledger/binding/live ref/inspect/remove检查仍执行，故全部Git和总耗时并非常数，不将其必要遍历说成已消除。

合并统计preview+delete+recovery时，10/100资源成功blob请求34/304→6，唯一blob均3，Git逻辑返回内容14564/144434→1096字节，最大blob481B。每次operation内Task blob各请求一次；两次独立operation仍各读一次，两个archive不同事实固定保留。volume只计Git内容请求，不把-spool内部逐输入JSON读取解释成新Git请求，也不把metadata -e计为内容。删除后ref无法probe的原误漏结果保留，resolved-volume按trace成功exit与操作前精确OID/大小补正，未改计时/输入。

source最大wrapper/Git峰值34308096/5472256 bytes，installed为38141952/5472256 bytes；均满足64/16MiB。RSS为BSDtime单次wrapper调用中单进程最大值及各Git单进程峰值，不是同时进程组总和，也不拆parent/child归属。Task内容逐对象读取，元数据/offset驻留，response普通临时文件，run退出关闭；无双pipe或整批payload字典。

## 功能与分发

原Cleanup完整套件最终40passed、zero skip，日志/tmp/guru-589-d4-cleanup-final-tests.log。两项新测试验证多资源真实删除时对象命令不随resource放大，以及相邻正常ref前进后原owner阻止其他Task误删；旧测试继续覆盖正常/手动/remote/linked资源、current-use/代次/缺失/失败/部分删除/恢复、schema2 Closure读取。首轮39passed+1skip是缺显式TRELLIS_DELIVERY_API_COMMON环境，不计完整通过；补齐原matching common后整套40重跑。

source与installed基准各组均实际沿原公开preview→确认fixture删除→same-input恢复链，不以底层测试代替。原run主体做静态AST投影后与B相同，证明context缩进/reader参数之外的原控制分支未变；这是机械证据，不替代上述功能/semantic检查。

原tools-only已同步dogfood，version0.7.0-guru.4，recovery_ref=54796244-b67e-43df-b736-6cf65efbfb5a，保留formal_fork_source_lock未验证。211项上游action字节/mode无差额、Task/session与peer pointer由原owner保持；extension.json为原installer生成的当前源码hash/provenance。代表安装/tmp/guru-589-installed-20261017经原apply产生1bak，逐字节验证为B旧源码、当前为新canonical后移到本批外部备份；原reapply statusok、installed validation0、zero sidecar。source、dogfood validator和overlay drift通过；未改.trellis/scripts、upstream/npm/node_modules/hook。

## 可复现与失败边界

原数据：/tmp/guru-589-diagnostics/d4-before-suite与d4-after-suite；method.json/candidate.json/comparison.json/volume-analysis.json及每sample原stdout/stderr/trace/profile/RSS保留。source-private tests/benchmarks工具仅把Fork/helper定位改为可移植参数/相邻文件，并作AST等价格式展开；实际before/after始终使用冻结/tmp工具，不根据after改标准。初始pytest依赖缺失未进入wrapper、installed profile首次错误PYTHONPATH未加载runtime，不计通过；仅该profile定位修正，其他模式执行分支不变，之后完整组采信。

## 整体剩余责任

本批完成Guru Cleanup热点。全步骤现行优化/保留清单见workflow-inventory.md；D1/D2/D3证据按实际不变consumer继续适用，不重复收益。官方task_store创建逐路径show及delivery_store相同blob重复hash仍是不可分离上游前置，当前无公开precomputed注入口；未解决时本Task整体与#589不得记完成或关闭。完整多平台/upgrade/Release矩阵归#575；正式Fork lock、软件版本发布、同事/业务仓采用及生产效果均未验证。本批工具交付不代表这些边界完成。
