# D3 实施前固定性能合同

本合同在全部before自然完成、任何生产修改前固定。固定B为c422692bca2d385a264da4db0030612b1b306fe1，含D1/D2及#588；官方Fork固定2a6f10ba3c0a2f27e0587e49e6c2f9b6a1f9d9d0（CLI/Core 0.7.0-castbox.3）。source与installed均managed CPython3.14.8；Git、Darwin及硬件详细版本见原始summary。installed由原apply生成且显式--python，2371个映射文件逐字节核对，不等同source tree。

## 计时与规模

source使用原真实公开wrapper，create后ensure；binding为首次establish（保留内部两次resolve）。所有validator及原task.py writer在timer内。每组两轮fresh等价fixture取中位数，恢复单独计时；不丢弃慢样本。计时、纯cProfile、RSS和volume分别执行，不跨pass相减。准备/安装/对象大小分析在timer外，无额外预热；OS页缓存不清理，前后按同顺序串行执行。create只改变官方writer生成的已有合法Task池10/100（不是归档Task），refs2/worktrees2；binding只改变无目标Task其他分支10/100，unique heads2/worktree1/目标Task472B。原Task池每份575B，路径/内容前后固定，不复制binding/ledger或改当前Task历史。

| source workload | plain两轮秒 | 中位秒 | Git/show/cat-file/ls-tree | pure热点两轮秒 |
| --- | --- | --- | --- | --- |
| create10+ensure | 2.224438166 / 2.108525000 | 2.166481583 | 137/30/0/3 | .406392541/.486937375 |
| create100+ensure | 5.195395625 / 5.092601875 | 5.143998750 | 407/300/0/3 | 2.367737000/2.358530208 |
| binding10 | .977774458/.968992417 | .973383437 | 67/24/22/0 | .722436542/.704990333 |
| binding100 | 4.838150167/4.705982583 | 4.772066375 | 427/204/202/0 | 4.541567958/4.560661125 |

pure热点为create的prepare_creation_inputs累计，或binding两次discover_branch_candidates累计之和，不再叠加内部函数；这不是CPU时间。官方writer subprocess wait与Git trace另列，create100首轮wait1.286秒，112Git/100show，属于仍保留上游责任，不计Guru可消除收益。

installed代表性create100两轮5.813673458/5.603610500，中位5.708641979；binding100两轮4.931881709/4.909401125，中位4.920641417；命令数与source对应档相同。六组installed只测timing/RSS/volume，不编造installed纯profile。source16+installed6各两轮均完成，恢复独立记录，不混入首次中位数。

## 固定通过标准

改善率=(before中位-after中位)/before中位。source完整链create10>=5%、create100>=20%、binding10>=20%、binding100>=50%；source纯热点create两档均>=20%、binding两档均>=40%。installed完整链create100>=20%、binding100>=50%。create10两轮跨度约5.35%，5%改善只作为低置信度工程门槛，不声称统计显著；同时要求真实Git读取下降。小档保留wrapper固定成本，较大档反映可消除的重复Git读取；创建不能绕过原writer。固定门槛不依after放宽，失败修本批实现。

source和installed每个wrapper invocation RSS最大值<=64MiB；source每Git单进程<=16MiB，installed每Git单进程<=32MiB。单位1MiB=1048576bytes。source before wrapper最大38223872bytes/Git7012352bytes；installed wrapper最大39436288/Git20807680bytes，因此installed Git独立32MiB上限保留实际安装路径开销。BSDtime是各public-wrapper invocation单进程max（同步官方Python child保留），不是同时进程组总和；不能单独归属父Python与official child。Git单进程另测。受限spool/单对象解析和<=1MiB copy是结构要求；不能以小JSON RSS代替大对象受限策略或D1资源回归。

## 读取量与结构

before create10/100分别30/300成功blob请求、10/100 unique、17250/172500返回bytes、5750/57500 unique bytes，max575；binding10/100分别24/204内容尝试，均2成功/1unique/944返回bytes/472unique bytes/max472，missing22/202。metadata -e不算内容请求，missing不算成功。installed对应100档一致。after须保留原每输入检查，同时Guru同reader内相同OID仅一次内容请求、same-head metadata复用；官方writer独立调用仍按原入口统计，不能声称完整operation已全部OID唯一。

同口径统计所有Git及show/cat-file/ls-tree；区分metadata与内容、成功与missing。必要branch/Task遍历及官方writer逐path独立报告，不用改命令名掩盖进程。相邻正常操作移动ref/worktree/index必须重新读取；不复用跨调用结果。

## 原始事实与边界

原始before root为/tmp/guru-589-diagnostics/d3-before：aggregate.json、installed-aggregate.json、git-command-classification.json、method.json及每组summary/各sample。source harness SHA256 cb451ad3832b5a9f7649b0c72fc88f6b47ea0f5a31c5183bcff516245d617508，profile 1cd0af1e0b9cde8acc3ec46fb0224be7a98f0d9613225e1d7f85d2c17e184bda，installed variant 9b790dc06590c3ce80f6907ef862d6a8271d5a87f861f91611c7c21bff470e59。after保持这些工具/输入/依赖/拆分方法；工具纳入source-private时只能去机器路径、不能改变口径。失败smoke保留不计正式样本。

fixture语义输入不等于native AI/provider/live GitHub证明；根正式调用trace另列total与网络不可分离边界，不参与本地改善标准。完整矩阵与formal_fork_source_lock归#575。官方task_store/delivery_store前置未完成，不关闭#589。
