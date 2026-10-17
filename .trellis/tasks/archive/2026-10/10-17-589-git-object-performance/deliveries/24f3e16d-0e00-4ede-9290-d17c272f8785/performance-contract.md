# D4 实施前固定性能合同

全部before完成后固定，生产Cleanup仍为B=dc57fc6ed5d1229c50520d74a1f6390a52469604，源码sha256=426b142af8c486b1cae609e8e90f4113cce341dc31b4661b7427e09bcbb5a251，未改生产。原Fork 2a6f10b/CLI0.7.0-castbox.3与D3相同；managedCPython3.14.8，macOS27.0.1 arm64 build26A434，AppleGit2.54.0。原安装器每fixture生成installed，源码/目标Cleanup字节比较；安装准备在计时外。

## 完整wrapper基线：秒

| 来源/资源数 | preview | 实际delete | 同输入recovery |
| --- | ---: | ---: | ---: |
| source 10 | 0.842700937 | 1.586168854 | 0.266694771 |
| source 100 | 5.262397729 | 13.154659271 | 0.284067625 |
| installed 10 | 0.902736480 | 1.673065854 | 0.290685209 |
| installed 100 | 5.594065979 | 13.518200208 | 0.312892313 |

输入为原missing_ledger_fixture真实terminal结果，加正常同Task/generation旧快照分支；仅资源数10→100变化，唯一selected head1、Task路径1、Task blob481B，固定archive两对象总67B。preview、真实删除、同输入恢复各通过原public wrapper；不删除当前repo/业务资源。每组fresh等价Git仓库、两轮中位，串行，无主动预热，warm OS cache；不冷清系统cache。16组source/installed×两规模×timing/profile/RSS/volume均完成。

## 固定标准

- source及installed的preview和实际delete完整wrapper：10资源至少改善10%，100资源至少改善20%。before中hotspot约占总耗时25–40%，这些标准低于可消除占比且保留全部其他校验。
- 原manual_targets_current独立cProfile累计热点：同来源两种入口的10资源至少改善30%，100资源至少改善50%；不将嵌套函数累计相加。
- recovery不套加速倍数，中位不得超过max(before×1.30,before+0.10秒)，仍返回同cleaned结果且无再次删除。
- source/installed各wrapper单进程maxRSS≤64MiB，各Git单进程maxRSS≤16MiB。before wrapper约32–37MiB，Git约5.3MiB，保留普通批量解析/传输余量；不是同时进程组RSS总和，也不拆分parent/child。
- 一次操作统计全部Git，单列show/cat-file/ls-tree；同head内容请求应按唯一blob去重，原固定archive独立读取保留。没有规定总Git零增长；必要inspect/ref/ownership遍历必须保留并单列。

## 同方法与证据

完整计时含shell launcher/dispatcher、原客观校验、原inspect和delete/receipt；语义fixture输入及准备/安装、后续对象量probe、AI审查不入计时。三次操作分别计时/计数，完整链合计为三次自动化耗时之和。GitHub网络0秒（本地fixture），不代表live远端或nativeAI效果。profile、volume与BSDtime RSS独立pass，不把观测开销当timing。

before原始在/tmp/guru-589-diagnostics/d4-before-suite，冻结工具与版本sha在method.json。after必须相同依赖、输入规模、工具和计时，HEAD不是未提交after字节证据，另记录Cleanup源码hash。Scalar show在删除前成功，删除后ref不能probe；volume-analysis按预先记录的精确Task blob OID/481B补正，并验证trace成功exit，原误漏probe保留，timing/input不变。最初缺pytest、installed profile错误PYTHONPATH失败不计pass，补外部pytest依赖并修正installed runtime路径后的完整数据采信。

标准不得依据after放宽；不通过时修实现，不移除热点/验证责任。
