# D5 实施前固定性能合同

生产source lock与工具尚未修改。正式before14组×2次均exit0；两档10/100，source及原installed完整create→ensure；source另有pure profile，RSS/volume与plain timing分别运行；recovery独立计时。旧Fork2a6、新Forkc7，固定Guru875bbd11、managed CPython3.14.8、AppleGit2.54.0、macOS27.0.1 arm64；refs2/worktrees2、existing active Task数为唯一规模因素。没有额外warmup/flush，不丢样。

工具benchmark SHA256 c5d04a9e6590e57d3ece464b7e54a049cd9ad4dd247341dc43d2ef46c116b075；profile ebaee25a6aef0f4a1f47ca7ac67b42433f059ff4b1ded4e9f1ec01c75d5941db。同一冻结/tmp工具与exact pool用于before/after；仅计时外pool校验支持原generation Fork与measured Fork分开，timed调用AST与canonical相同。全部工具/source/pool与raw trace/stdout、RSS/profile/volume位于owner工程测量目录；不把巨大hash bundle写public DTO。

|来源/Task数|before完整链秒|after最大中位秒|
|---|---:|---:|
|source/10|2.2922797709470615|2.1776657823997083|
|source/100|3.4061481045209803|2.554611078390735|
|installed/10|2.7817661035223864|2.642677798346267|
|installed/100|4.0825840414036065|3.061938031052705|

完整链10档≥5%、100档≥25%；依据before writer约.35/1.55秒、完整链约2.29/3.41秒及installed约2.78/4.08秒，不能将原owner倍数套总链。source官方writer profile墙钟（含同步等待，非CPU）10档≥30%、100档≥60%；ensure与recovery分别≤max(before×1.30,before+0.10秒)。wrapper单进程RSS≤64MiB、Git≤32MiB，包含installed原git status，其before约20–21MB，不沿用不适用的D4 Git16MiB。以上标准after不放宽。

正文请求before20/200=Guru预检查N+官方writerN，unique10/100、max575B；两个独立consumer保留，不要求跨owner合并或将总正文强降N。Git/show/cat-file/ls-tree按完整操作与writer分别报告，原mutable/归属检查不减。GitHub网络等待为0；fixture语义不是native AI/live GitHub证明。

上游c7的44项冻结门槛已用原evaluator重验，before资料与生产修改前3f48ebd逐字节一致；该证据仅属upstream owner，local_commit不是Guru pull_request链。snapshot残余同OID重复hash不计为修复，整体责任保留。
