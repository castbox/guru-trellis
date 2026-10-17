# D6 固定 before/after 结果

本批采用 D5 已交付来源：Guru f70b64b026725b27d59fed17ed710cc2f831439f，Fork c7bd746b42d75f73534c85e263cd6b51fe0e5287。before Guru875bbd11/Fork2a6f10b；373个Guru Python逐字节相同，D5只改来源与文档，收益不混入D1–D4或#588。方法及预先门槛沿用D5 performance-contract.md，不放宽、不补选样本。

## 完整公开 create→ensure 链

14组串行×2次，各自全新fixture，同一exact pool；source10/100 timing/profile/rss/volume，installed10/100 timing/rss/volume。全部组与样本正常结束，无warmup、cache flush、丢样或重跑。安装/准备不计入计时，recovery单列。managed CPython3.14.8、macOS27.0.1 arm64、AppleGit2.54.0，refs2/worktrees2，existing active Tasks10/100为规模因素。

|来源/规模|before中位秒|after两次范围秒|after中位秒|改善|固定要求|
|---|---:|---|---:|---:|---:|
|source/10|2.292280|1.949805–2.023492|1.986648|13.33%|≥5%|
|source/100|3.406148|2.039713–2.116914|2.078313|38.98%|≥25%|
|installed/10|2.781766|2.501559–2.611281|2.556420|8.10%|≥5%|
|installed/100|4.082584|2.675813–2.737069|2.706441|33.71%|≥25%|

## Writer、恢复与资源

source官方writer profile wall（含同步子进程等待，非CPU）：10档before .359794/.347532，after .225152/.243777秒，中位改善33.70%（要求≥30%）；100档before1.574009/1.529785，after .247536/.250928秒，改善83.94%（要求≥60%）。profile是plain timing的伴随定位，不取代完整链。

|来源/规模|ensure before→after秒|recovery before→after秒|wrapper最大RSS bytes|Git最大RSS bytes|
|---|---|---|---:|---:|
|source/10|0.508846→0.473677|0.849630→0.802046|37994496|6832128|
|source/100|0.516220→0.500773|0.878656→0.848585|38273024|7077888|
|installed/10|0.634038→0.586328|0.978712→0.915511|39043072|14336000|
|installed/100|0.657485→0.655267|1.018784→0.946889|38961152|20299776|

ensure与独立原结果recovery均满足≤max(before×1.30,before+.10秒)；wrapper≤67108864、Git≤33554432 bytes，均通过。RSS为单进程最大值，不是同时进程组总量。以上22项固定数值比较通过，仅证明这些测量目标。

## 进程与对象量

两次样本计数相同。source/installed完整操作10档Git117→108，100档207→108；show10/100→0，ls-tree2→2，cat-file1→2。上游writer改用固定批量读取；Guru独立预检查保留，两consumer不跨owner合成一个。完整链仍包含必要Git身份/归属检查，未声称所有Git或遍历成本消失。

正文请求各样本before/after均20/200（Guru N+官方writer N），unique OIDs10/100；successful bytes11500/115000，unique bytes5750/57500，最大blob575 bytes，missing0、other对象0。两个独立consumer之间不强降为N。重复OID snapshot摘要残余不以该不同pool或链收益替代。

后验9工具、373GuruPython、224pool文件均与原冻结SHA相同；14组returncode全0。原始before/after summary、各sample stdout/trace/profile/rss/volume及固定方法仍在本会话工程测量目录，不将大hash bundle或过程流水写入公共DTO。

## 证明边界

计时使用真实公开Guru wrapper与原writer及原ensure/recovery，但语义输入由隔离fixture提供；不是native AI gate、live GitHub冲突或生产证明，GitHub网络等待为0。本Task真实Check/TaskCommit/fullReview/Publish/Merge另沿原owner执行，事实在发生后承接。

AC06仍未满足：manual_recovery.commit_candidate→CandidateObjects.snapshot(actual immutable head,paths)→public candidate_content_ref(snapshot,paths,'git') 对同blob物化路径重复read/hash。3路径4次、30路径31次SHA256构造（含aggregate），oracle字节一致。上游公开observation仅覆盖normal local_commit，不能代替Guru支持的pull_request。保留上游原owner，不导入private observation、不复制hash算法、不以inode作authority。整体Completion不得completed。
