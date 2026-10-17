# D2 性能结果与交付边界

## 结论与方法

当前单向流式候选完成 source15组及 installed2组，每组重复两次。所有预先固定的完整链、纯热点、RSS与结构门槛通过；标准见同目录 performance-contract.md，未依after放宽。内容B为924f293821e1e3031b7efdbfc3b0868ef9d02011，包含D1及#588；本批不重复计算其收益。

raw及可复算汇总：/tmp/guru-589-diagnostics/d2-after-stream/comparison.json、summarize.py；每组summary.json、Trace2、独立profile/hash/RSS原始结果保留。源码冻结hash：common.py c817b09818bd35b1af8da8aa786e2479afac3f2d7c66e65ca630d8d432b42eca；record.py e7a4d24e37660672330fbb6f2e269d7e994941f194ebc9dc8d50ecd19f2043ab。

计时为实际支持的pull_request fixture：完整Review→main独立前进→实际merge→当前Check在准备阶段；操作timer内保留review-branch.sh recorder、check-review-gate.sh和invoke.sh及全部原validator/固定Git。provider/semantic为fixture，网络等待0；不是native语义审查或live GitHub发布证明。每组同候选两轮中位，不清OS cache、不选择最快轮。macOS27.0.1 arm64、Git2.54.0、matching Fork CLI/Core0.7.0-castbox.3、受测managed Python3.14.8。固定B纯profile clone默认3.12.8仅用于timer外准备，driver以sys.executable运行的受测dispatcher为3.14.8；不声称整个clone环境一致。

## 完整公开链耗时（秒）

| source输入 | before中位 | after两轮 | after中位 | 改善 / 最低要求 |
| --- | ---: | --- | ---: | --- |
| 1000-duplicates | 1.954266 | 1.734678 / 1.733967 | 1.734323 | 11.25% / 5.00% PASS |
| 10000-duplicates | 4.439208 | 2.855267 / 2.999660 | 2.927463 | 34.05% / 5.00% PASS |
| 10000-unique | 3.219038 | 2.945278 / 2.977320 | 2.961299 | 8.01% / 3.00% PASS |
| installed1000 duplicates | 2.366352 | 2.078735 / 2.143401 | 2.111068 | 10.79% / 5% PASS |

每次原wrapper耗时独立列出（recorder / checker / invoke，两轮；不与另一个pass相减或相加）：

- 1000-duplicates：0.737567 / 0.439886 / 0.557201；0.738539 / 0.431232 / 0.564188秒。
- 10000-duplicates：1.622850 / 0.515414 / 0.716988；1.743691 / 0.513042 / 0.742916秒。
- 10000-unique：1.641108 / 0.553417 / 0.750735；1.687762 / 0.539346 / 0.750202秒。
- installed1000duplicates：0.919192 / 0.505809 / 0.653677；0.944795 / 0.505494 / 0.693042秒。

## 读取和摘要热点

纯cProfile无hash探针，累计tree_identity包括其内部工作，不能再加嵌套validate累计；其余dispatcher/身份/客观校验保持，不把profile跨pass扣成plain耗时。before原始根为d2-before-plain；旧constructor observer混合profile不参与计时比较。

| 输入 | before纯热点中位 | after两轮 | after中位 | 改善 / 最低要求 |
| --- | ---: | --- | ---: | --- |
| 1000-duplicates | 0.320504 | 0.143106 / 0.152594 | 0.147850 | 53.87% / 20.00% PASS |
| 10000-duplicates | 1.677693 | 0.186524 / 0.182636 | 0.184580 | 89.00% / 20.00% PASS |
| 10000-unique | 0.490506 | 0.302808 / 0.302335 | 0.302571 | 38.31% / 10.00% PASS |

## 规模、Git与内容量

assets为1000/10000条4KiB，duplicates池64，另含一个16777216bytes blob。source实际blob路径1044/10044/10044，唯一OID105/105/10041；每次路径bytes21400795/59146795/59146795，唯一bytes17566885/18448885/59146741。

所有source操作由before每次62Git/cat-file4/ls-tree8/show0变为63Git/cat-file3/ls-tree7/show0。增加的immutable-tree解析如实保留；优化不是把所有Git降零。两轮volume是6个独立进程各读取一次唯一对象，before则8次逐路径全树读取：

| 输入 | before请求 / bytes | after请求 / 唯一OID / bytes |
| --- | --- | --- |
| 1000duplicates | 8352 / 171206360 | 630 / 105 / 105401310 |
| 10000duplicates | 80352 / 473174360 | 630 / 105 / 110693310 |
| 10000unique | 80352 / 473174360 | 60246 / 10041 / 354880446 |

以上为成功返回逻辑blob bytes，不是物理disk IO；scalar内容请求0。每份输入的Task/Delivery/Check、关系、祖先和期望摘要仍独立验证。record同进程validate复用内容事实，checker/invoke各自重读，不跨进程复用pass。

独立hashes pass覆盖constructor初始bytes、update和finalization，六次公开进程均按实际落点观察：每进程blob hash数量105/105/10041，内容bytes17566885/18448885/59146741，16MiB大对象各15次update；最终tree各1次hash，输入metadata bytes86671/824671/824671，update0（metadata join）。0 update不等于无hash。record内第二次tree调用命中memo而非第二轮内容计算。原raw path、顺序、每路径贡献及gitlink/symlink/mode/删除由真实Git oracle和原公开链保留。

## 内存（bytes）

BSD time记录各实际wrapper runtime及Git单进程最大RSS，不是同时进程组总和，不包含controller/安装/准备。

| 组 | before runtime最大 | after runtime最大 | before Git最大 | after Git最大 | 固定上限 |
| --- | ---: | ---: | ---: | ---: | --- |
| source1000dup | 111001600 | 61538304 | 6193152 | 6193152 | 128 / 24MiB PASS |
| source10000dup | 209633280 | 70500352 | 7815168 | 7831552 | 128 / 24MiB PASS |
| source10000unique | 210665472 | 71778304 | 23674880 | 23658496 | 128 / 24MiB PASS |
| installed10000unique | 284770304 | 97976320 | 32571392 | 32456704 | 160 / 48MiB PASS |

MiB=1048576bytes。stdin预写普通文件、stdout唯一单向pipe、stderr普通文件；blob内容<=1MiB分块，内存仅保存metadata/digest与有限块，不保留整批response。

## 真实失败与正式回程

最初双普通文件response候选在d2-after-final完整source15中unique全链慢1.25%、热点慢22.28%，未通过。后续1MiB响应buffer/首块SHA/metadata join的d2-after-repaired仅7组，热点仍慢17.54%；加Git --buffer的d2-after-buffered仅5组，unique完整链改善1.66%仍低于3%。这些失败及partial全部保留且不计验收；d2-after的安装重叠探索也不计。随后经同D2原rework→Author、独立candidate/final Architecture、Wording、Approval和Activation，采用本次单向流式候选；不更换门槛，不择优混合旧轮。

## 功能、投影与未完成边界

当前候选完整Review包54tests、原schema2 PR continuity1test通过、zero skip；原日志/tmp/guru-589-d2-stream-review-package-tests.log及/tmp/guru-589-d2-stream-schema2-pr-continuity-test.log。独立函数oracle之外保留真实record/check/invoke、整合后当前Check与既有完整Review义务；读取错误关闭/等待、解析错误drain有限输出、Git非零stderr优先及失败不写memo均有定向行为观察。

安装来自原guru-upgrade-tools local_candidate操作0b90a9af-b1db-421a-904b-230354ab5dc6，tools_upgraded recovery ab9ccfdf-d876-47e7-8184-1e1c97eeb3da；当前原结果根/tmp/guru-589-d2-tools-v4。canonical→dogfood及原apply/reapply生成/tmp/guru-589-installed-20261017；matching Fork+显式managed解释器，source/dogfood/installed package、声明平台drift、mode及sidecar均通过，未处理.new/.bak为0，.trellis/scripts无diff。installed actual tree：timing7163路径/2623OID/41653325路径bytes，RSS16163路径/12559OID/79399325路径bytes；与before差3434bytes来自本批受管源码/manifest变化，其余fixture/入口不变。不能将installed与source当作相同整树。

formal_fork_source_lock仍unverified；完整多平台/upgrade/Release矩阵归#575。工具交付、正式版本发布和业务仓采用是不同事实；本批未发布版本、未升级业务仓。D3生命周期/全流程计数及联合回归、官方task_store创建与delivery_store重复hash上游前置仍未完成；D2独立交付不关闭#589。
