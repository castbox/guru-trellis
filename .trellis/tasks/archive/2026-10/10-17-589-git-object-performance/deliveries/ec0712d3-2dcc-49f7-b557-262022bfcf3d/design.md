# D2 bounded continuity 内容摘要设计

## 基线与单一路径

开发基线沿Task的main@3676b9ee65834ef3720f2ff5cc0d8330afcea6ed；本Delivery内容基线B由原content_base选择前一实际已交付祖先head924f293821e1e3031b7efdbfc3b0868ef9d02011。PR目标仍main，Planning观察H0与目标前进不因目标前进而自动同步。B已含#588及D1，不重复实现或计入其收益。当前流式候选的独立candidate_assessment为no_architecture_impact，无contribution/ADR义务。

直接改原guru-review-branch/runtime/common.py的tree_identity，以及record/validate的同进程调用；不新建通用Git框架，不修改D1或Reconcile算法。源实现替换后不保留旧内容读取分支。

## 读取和摘要

按原ls-tree -r -z --full-tree顺序保留原始path bytes、blob OID与gitlink条目；内存保留metadata和digest，不保留整批内容。按blob OID建立唯一请求，全部写入普通request临时文件并seek0，再运行git cat-file --batch --buffer。Popen的stdin是该完整文件，stdout是唯一单向pipe（1MiB缓冲），stderr是普通临时文件；Python只读stdout，不写stdin pipe，没有两条pipe互相阻塞，也不落盘整批response。

沿原OID/type/size/完整换行检查解析stdout。首块最多1MiB直接初始化单个blob SHA256，剩余大blob每块最多1MiB update，只保留该OID十六进制digest；最终只拼路径/digest/gitlink metadata行，不拼blob内容。有限请求正常读至EOF并wait后检查Git返回码。解析失败先保留原CommandError，以最多1MiB块drain余下有限stdout后wait，Git非零时仍优先使用其stderr；stdout读取失败则关闭读端并wait收尾，返回原candidate_tree_sha256读取错误。仅全部解析与Git成功后写memo，不把截断当成功/删除，不增加线程、timeout、锁或后台reader。

逐原条目顺序计算整体SHA256：blob贡献path+NUL+content-hexdigest-ascii+NUL；gitlink贡献path+NUL+160000+NUL+OID+NUL。symlink仍作为blob，原普通文件executable mode不进入此算法；不统一其他owner的hash合同，不以tree OID替代内容摘要。相同blob只计算一次，但每条路径贡献保留。

## 同次调用复用

原record拥有调用期显式memo并传给同进程validate_gate。key绑定实际repo.resolve()、immutable tree以及本函数唯一原算法/上下文；若复用已确认的immutable commit→tree事实，只接受完整immutable OID，移动ref每次重新解析。memo不跨原wrapper调用、进程、repo、index/worktree或阶段存续。每份public input仍独立检查Task/Delivery/Check/关系/祖先/预期摘要；仅复用内容计算，不复用semantic pass。独立checker/invoke各自重新读取，其成本必须保留。

## 来源承接

| 来源/承诺 | 处置 | 落点/理由 |
| --- | --- | --- |
| #589 §3.3第二项、§5.1 | retain | 原tree_identity唯一OID请求/hash，record同调用tree memo；完整路径贡献保持。 |
| #579、#589 §5.2 | retain | 预写普通request、单向stdout有界hash及普通stderr；保留#579禁止双pipe互阻和整批内容常驻的承诺。 |
| #589 §5.3–5.4 | retain | 实际repo/immutable tree/原算法绑定，仅调用内技术事实；原每输入检查仍执行。 |
| #588 / #567 | retain | 不改Reconcile、不重复计收益、不因目标前进而追赶base；冲突后的完整Check/Review独立。 |
| #589 §5.7–5.8 | retain | 原canonical同步dogfood、原安装投影；保持所有路径bytes、blob/symlink/gitlink/mode/删除/错误合同。 |
| #589 §6–8 | retain | 先before再冻结固定performance-contract，再生产实现和相同方法after；结果不扩大为正式版本/业务采用。 |

原Clarify source_selection为空，没有另一个normative design；上述技术约束来自Issue正文。当前公开RDT/Architecture行为authority不变。

## 验证与剩余边界

正式测量使用实际支持的pull_request fixture，完整Review→base前进→实际merge→当前Check→bounded recorder/checker/invoke；semantic/provider仍是fixture，不冒充native AI或live发布。source旧local_commit探索数据和installed前置失败保留但不计验收，source/installed统一PR并经原安装链。timer、Trace2、volume、RSS、纯cProfile和hashes独立。原混合constructor observer的profile只保留为探索计数，不用于after时间比较；从固定B补纯cProfile before，以相同plain方法对比after，hashes另行观察实际update/finalization。原20%/10%热点、5%/3%完整链与RSS上限保持，不依after放宽。补证时实现已暂停，尚无after。

新旧摘要独立oracle、重复/大量唯一/大blob、symlink/gitlink/raw特殊path、正常缺失/读取失败、有限进程EOF/解析失败drain/读取失败收尾、调用内memo隔离与相邻ref变化需定向验证；原consumer不得用continuity替代当前完整Review。D3生命周期/全流程计数与联合回归及上游Task创建/重复hash仍待完成。