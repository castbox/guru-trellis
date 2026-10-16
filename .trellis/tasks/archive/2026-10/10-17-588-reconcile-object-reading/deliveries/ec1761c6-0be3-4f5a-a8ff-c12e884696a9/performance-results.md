# #588 性能、资源与兼容结果

本报告由 Completion、Branch Review 和 Issue Closure 直接消费；记录真实测量与未验证边界，不作为 semantic gate。冻结判据见 design.md：两类树摘要/完整链中位数均至少5倍，逐阶段RSS中位数不超过原值+32MiB。

## 测量身份与口径

原实现：main `1b2c30b4b1a326f2276c96f0d155605bf2cb1775` 的未修改primary source。修复实现：同B上的本Delivery运行时工作树候选；下列common/invoke内容身份对应实际测量字节。TaskCommit后将对实际提交候选补跑同合同，结果交付到Issue，避免在本文件内自引用尚未产生的提交。

环境与fixture/history/缓存/次数/计时/RSS边界严格沿design冻结合同。原完整链由规划阶段原harness执行；保留的 tests/benchmark_object_reading.py 提供同fixture、同wrapper/time-l/trace边界的复现命令，并在计时外增加逐阶段trace计数。独立摘要由新Python子进程计时，SELF/CHILDREN分别采集。所有数字为本机对照，不是跨机SLA。

| 修复runtime文件 | 实测SHA256 |
| --- | --- |
| common.py | dfc26ee71837665f082f36304c2759c9ca18a7d0a3435dc0c4b737205ff5288c |
| invoke.py | 0b56822c456c0e5dd5afda48bd98f4237b3c685cd3638d5800cafeab4e0bf2d1 |

## 实际完整链与摘要结果

完整链每轮均实际创建整合提交，record/check/invoke返回reconciled且checkpoint已消费；两版对应树最终摘要完全相同。

| 树 | 原链两轮秒 | 修复链两轮秒 | 链中位加速 | 原摘要两轮秒 | 修复摘要两轮秒 | 摘要中位加速 |
| --- | --- | --- | --- | --- | --- | --- |
| duplicates | 786.230739, 717.176496 | 7.172920, 6.285831 | 111.70× | 100.147598, 97.898949 | 0.054246, 0.057359 | 1774.53× |
| unique | 734.966888, 775.650587 | 9.750570, 7.498145 | 87.58× | 98.762830, 104.824898 | 1.286319, 1.099653 | 85.33× |

duplicates：10001资产文件、65唯一资产blob、17,825,792唯一字节；unique：10001资产文件、10001唯一blob、180,617,216唯一字节；均另有3个原fixture文件，最大对象16MiB。重复比例约99.35%/0%。

每条原链Git进程总计70,197，其中cat-file70,028，七轮各10,004对象；修复每条链Git进程178，其中cat-file6、扫描6轮。修复duplicates每轮请求68个唯一blob，unique每轮10004个；独立预算测试观察实际stdin请求并确认每OID只哈希一次。gitlink不参与blob请求。

| 阶段 | 原cat-file | 修复cat-file | 原Git进程 | 修复Git进程 |
| --- | ---: | ---: | ---: | ---: |
| candidate | 10004 | 1 | 10014 | 11 |
| reconciliation | 20008 | 2 | 20042 | 37 |
| record | 10004 | 1 | 10056 | 54 |
| check | 10004 | 1 | 10025 | 23 |
| invoke | 20008 | 1 | 20060 | 53 |

原逐阶段进程数由正式链原trace的七次blob调用连续段及原确定性命令序列分组，并与实际trace总数70,197交叉核对；修复逐阶段直接按每wrapper trace字节区间计数。

## 逐阶段时间与资源

RSS为 /usr/bin/time -l 对每wrapper及后代的maximum high-water范围，不是Python+Git同刻RSS总和；单位MiB。

| 树/阶段 | 原秒1/2 | 修复秒1/2 | 原RSS1/2 MiB | 修复RSS1/2 MiB |
| --- | --- | --- | --- | --- |
| duplicates/execute-base-candidate.sh | 110.583/108.502 | 3.060/2.556 | 72.188/79.234 | 44.078/44.094 |
| duplicates/execute-base-reconciliation.sh | 217.484/201.301 | 1.037/0.944 | 73.875/80.250 | 43.391/45.062 |
| duplicates/record-base-reconciliation.sh | 109.424/98.726 | 1.117/1.040 | 74.656/80.547 | 45.250/45.453 |
| duplicates/check-base-reconciliation.sh | 114.878/100.295 | 0.752/0.674 | 72.391/74.719 | 43.969/43.125 |
| duplicates/invoke.sh | 233.862/208.353 | 1.207/1.072 | 71.516/73.469 | 43.406/43.000 |
| unique/execute-base-candidate.sh | 108.606/113.647 | 3.739/2.654 | 71.859/71.203 | 43.391/44.359 |
| unique/execute-base-reconciliation.sh | 202.673/231.818 | 2.077/1.464 | 73.734/72.891 | 46.688/45.828 |
| unique/record-base-reconciliation.sh | 100.601/110.128 | 1.582/1.261 | 80.297/72.359 | 44.938/43.453 |
| unique/check-base-reconciliation.sh | 105.332/98.484 | 1.003/0.877 | 74.391/72.328 | 44.641/45.484 |
| unique/invoke.sh | 217.756/221.573 | 1.350/1.243 | 72.484/72.031 | 45.578/43.578 |

| 摘要资源 | 原RSS1/2 MiB | 修复RSS1/2 MiB |
| --- | --- | --- |
| duplicates/python_maxrss | 60.766/61.094 | 36.359/36.531 |
| duplicates/git_child_maxrss | 6.156/6.172 | 6.172/6.172 |
| unique/python_maxrss | 71.328/60.625 | 37.062/36.922 |
| unique/git_child_maxrss | 20.641/20.609 | 6.141/21.344 |

摘要SELF为Python自身，CHILDREN为已结束Git子进程的单子进程最大RSS，不是所有Git RSS之和。输出存临时文件、1MiB分块，完整大体积unique两轮全部完成；没有全批内容常驻内存回退。逐阶段和摘要Python/Git均满足冻结+32MiB判据。

## 分解说明

摘要函数计时独立于正式wrapper，固定validation为git diff --quiet。以摘要中位数×trace扫描轮数估内容成本；其余为整链减该估计（包含其它客观校验、wrapper、启动与缓存/调度误差），不能当精确嵌套剖析。

- duplicates：原估内容693.163秒、其余58.541秒；修复估内容0.335秒、其余6.395秒。
- unique：原估内容712.557秒、其余42.752秒；修复估内容7.158秒、其余1.466秒。
- duplicates/原固定validation Git进程实测秒：1.025145, 0.27261；不含Python调用边缘。
- duplicates/修复固定validation Git进程实测秒：0.135658, 0.343357；不含Python调用边缘。
- unique/原固定validation Git进程实测秒：0.423464, 0.961523；不含Python调用边缘。
- unique/修复固定validation Git进程实测秒：0.207096, 0.122743；不含Python调用边缘。

## 回归与分发证据

- managed runtime suite 46项通过（82.962s），contract suite 8项通过；最终memo/error-field版本再跑2项通过；独立quality worker只读复核并跑新增5项通过。没有独立lint/type-check工具配置，未声称执行它们。
- 独立旧算法oracle覆盖普通/可执行/符号链接/空/二进制/重复内容、tab/newline/非ASCII路径与未初始化gitlink；mode-only不改变摘要。缺失对象保留candidate_failed/repository.index。
- 原套件实际覆盖普通pre/post整合与staged/unstaged/untracked保存、preimplementation resolved baseline、postreview continuity及原consumer、postimplementation resolved candidate/full-review projection、同原提交恢复。Reconcile成功不冒充Branch Review通过。
- source/installed package inventory passed；dogfood drift passed，覆盖shared及Claude/Codex/Cursor声明平台；关键runtime/contract/wrapper在canonical/dogfood/clean-installed字节和mode一致；递归无.new/.bak。
- dogfood常规apply在任何写入前被既有schema1历史archives阻止；使用既有guru-upgrade-tools原owner完成单checkout工具同步（tools_upgraded），原Task/session和其它worktree保留。CLI/Core实际maintenance API1.0来自现有本地候选，formal_fork_source_lock未验证；不作为正式发布证据。没有修改installer或迁移旧任务。
- 一个真实干净Codex target经匹配Fork0.7.0-castbox.3初始化guru-team marketplace（workflow固定B），实际preset apply/reapply成功，installed package validator与native runtime-contract通过。安装来自本Delivery当前源码。其unique 10004条索引完整installed链7.057014秒、6batch/178Git，reconciled且checkpoint已消费，摘要与原一致；dogfood完整链另已成功执行。

## 复现

使用managed Python并显式设置 GURU_UPSTREAM_DELIVERY_SCRIPTS=<fixture-source>/.trellis/scripts。执行当前 tests/benchmark_object_reading.py --source <原B或候选source> --output <新的临时目录> --kind duplicates|unique --repeats 2；加 --digest-only 测独立摘要。--package-root <clean-target>/.trellis/guru-team/skills/packages/guru-reconcile-task-base 使用真实installed包装器。原B源码保持不修改；新harness位于候选source且通过--source读取原fixture。所有计数分析在timer外，时间不包括fixture创建。

完整多平台Throwaway/upgrade/update/Release矩阵、正式版本发布与业务仓升级采用未执行，也不属于本Issue。工具实现交付、版本发布、业务采用分别报告。最终提交身份和merge/Closure事实以实际后续Git/GitHub结果为准。
