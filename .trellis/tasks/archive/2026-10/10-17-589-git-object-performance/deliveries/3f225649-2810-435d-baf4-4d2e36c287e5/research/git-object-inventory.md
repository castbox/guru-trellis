# Git 对象读取盘点（D1 已测，整体尚未完成）

源码基线为 main `3676b9ee65834ef3720f2ff5cc0d8330afcea6ed`，包含 #588。以下 canonical 路径省略共同前缀 `trellis/skills/guru-team/`。测试、dogfood 和 installed 投影不重复计为生产热点。

## 当前优化清单

| 步骤与入口 | caller / 对象 / 命令 | 增长因素与当前证据 | 责任切片 |
| --- | --- | --- | --- |
| Completion 历史查询 `guru-merge-task-delivery/scripts/discover-task-deliveries.sh` query2 | `runtime/history.py:HistoryContext.candidate`；候选 commit、paths 和 blob；commit `cat-file -e` 后逐路径 `ls-tree` / blob `cat-file -e`，随后重建内容 | 候选路径 P、Delivery 数 D；路径检查与重建合计约 4P 个 Git，重复 blob 未复用。局部诊断1001路径/65唯一blob两次均4005 Git，42.56–44.96秒；正式入口102/1002路径分别416/4016 Git，中位耗时5.086/46.373秒；完整数据见performance-contract.md。 | D1 |
| 手动合并恢复 `guru-merge-task-delivery/scripts/invoke.sh` / `delivery_merged_recovery` | `manual_recovery.commit_candidate`；候选树逐路径 `ls-tree` 和 `cat-file blob`；原 `candidate_content_ref` 消费快照 | P；1002路径完整入口两次为2017/2012 Git，24.71/25.02秒。第一轮记录、第二轮原结果恢复有固定进程差额，不能把差额算作优化。10002路径duplicate与unique两档完整before均已测，见performance-contract.md。 | D1 |
| 实际整合后 Review `guru-review-branch` / `delivery_base_continuity` | `common.tree_identity`；完整 commit 树 `ls-tree -r -z`，文件stdin batch，但按路径重复请求blob且整批stdout入内存；record→validate 重算摘要 | 路径 P、唯一blob U、内容量 B、同规则调用次数；保持原路径/内容/gitlink摘要字节。正式链计数待D2。 | D2 |
| Task创建 `guru-create-task` | `runtime/task_lifecycle/composition.prepare_creation_inputs`；各分支 `.trellis/tasks/**/task.json`；每ref `ls-tree` 后逐文件 `show` | 分支 R、历史Task T、重复commit/tree/blob；本仓357 refs、213不同heads。实际创建已执行原writer并恢复输出；无trace的创建耗时不冒充精确计数。规模基准待D3。 | D3 |
| branch/checkout/历史Task身份解析 | `branch_resolution._artifact_matches`、`identity` → `git_facts.commit_path_bytes`；逐branch/path `show`，缺失再 `cat-file -e commit` | R、查询路径、相同OID重复；必须保持独立归属与真实缺失判断。正式入口两档计数待D3。 | D3 |

| 官方候选快照内容摘要 `delivery_store.candidate_content_ref` | 原Merge快照消费步骤；逐路径read_bytes/SHA256，对同blob多路径重复内容hash | P与重复blob；当前公开API没有预计算hash注入口，不能复制或绕过其算法。before profile已单列官方hash耗时。 | 明确上游依赖，整体未完成责任 |

## 保留清单与计数责任

| 步骤/入口 | 已核查操作与增长 | 保留理由 / 必须补充的测量 |
| --- | --- | --- |
| Intake / Sync / Discovery | ref解析、fetch/ff、当前authority blob绑定和archive preview；固定提交/源文件数 | 移动ref与live authority必须刷新。身份解析共用热点归D3。按正式操作trace补全计数，不因存在cat-file追加修改义务。 |
| Planning / Author / Wording / Approval / Activation | 三份当前规划文件、root scope、C4/C5、当前branch/checkout和公共API；主要读取worktree文件 | 规划/摘要/身份不能相互替代。调用生命周期事实的重复部分归D3；mutable文件和每份输入校验保留。需真实入口计数。 |
| Implementation / Check | `guru-check-task/runtime/common.py`一次HEAD `ls-tree -r -z`；reviewed_content对dirty index/worktree读取与hash-object | 当前内容可变，不复用上次操作；hash-object写入内容身份不是已确认不可变对象读取热点。需区分必要遍历/dirty成本与重复事实。 |
| Task Commit | `delivery.py`读取当前task JSON并检查五份规划/上下文文件的提交存在性；execute读取固定提交parent/tree/message | 数量固定、各自有commit恢复/精确候选用途；不得预先判作缺陷。正式入口统计cat-file/show及全部Git。 |
| 完整 Branch Review | reviewed_content一次树枚举，当前dirty/index/gitlink验证；continuity独立路径归D2 | 完整Review不等同bounded continuity，不删检查或复用语义pass；正式链计数。 |
| Delivery Review / Publish / Merge | reviewed head / content range / PR / base、少量commit与祖先事实；history查询归D1 | 原publication/merge事务与恢复独立用途；网络耗时单列，不作热点加速门槛。需真实入口trace。 |
| Completion | 各历史Delivery的候选/归属、固定query截点及整体scope | 按每份输入独立校验；其历史读取热点归D1，不制造交付事实。2/4份真实Delivery分别109/215 Git，详见performance-contract.md。 |
| Closure | live源Issue与Completion结果、固定Task身份 | 不存在按候选文件枚举；不删live disposition校验。正式入口计数。 |
| Finish | `runtime/invoke.py`对archive task、finish-summary、active task三个位置 `cat-file -e`；固定message读取 | 三处各有archive落地/active消失的独立用途。正式入口实际计数待测。 |
| Cleanup | reviewed resources、commit存在性、一次树扫描查active artifacts | 分支/资源本身是检查对象；保留准确归属、预期HEAD和sealed generation。正式入口计数待测。 |
| Reconcile（#588） | `index_tree_digest`唯一OID batch，临时文件响应分块hash；同次invoke不可变树摘要复用 | 已交付源码与原PR证据存在，本Issue不能重复计收益；联合候选必须包含它。仍需本Issue正式链计数和兼容回归。 |
| 资格校验 | `runtime/qualification_facts.py`少量commit `cat-file -e` | 每个明确commit身份独立验证；固定小量检查需正式调用计数，不统一套倍数。 |

## 上游边界

Fixed Fork `.trellis/scripts/common/task_store.py:517–529` 的官方创建在唯一heads集合上逐Task路径 `git show`。当前Guru公开创建必须调用该writer。不得修改生成副本、跳过唯一性检查或伪造创建结果；需以现有公开能力或明确上游依赖承接，未解决时不计对应范围完成。

`.trellis/scripts/common/delivery_store.py:109–125` 的 `_verify_commit` 逐路径 `ls-tree/show` 属 `local_commit`；D1的pull_request恢复走 `_verify_pr`，不混算为D1热点。当前Guru只声明pull_request；上游具有某能力不表示它进入当前受支持业务路径。

## 当前验证界限

当前数字来自临时Git仓库、实际正式Merge wrapper与真实公共store，GitHub响应为本地fixture。fixture语义输入只证明确定性传输，不证明native AI Review或live GitHub发布。局部诊断、正式链、各次操作、Python/Git单进程RSS和最终完整矩阵将分别报告；待测不等于通过。

## D1 最终处置

历史查询与手动恢复的 Guru 逐候选路径对象读取已由原 caller 的 package-private CandidateObjects 替换：64KiB argv 元数据分块、按 OID 去重的普通文件 batch spool、1MiB 快照复制与调用内复用。完整结果见 ../performance-results.md；旧 per-path 实现不再保留。每份 Delivery 原检查与官方摘要仍独立执行。

命中 Delivery 的 commit_facts 还会重复读取 discover 已取得的同 SHA message，且字段无人消费；已删除此读。真实 query2 Trace2 回归由两次降为一次。真实当前 Task 的 native 空查询另观察到 300 个不同 first-parent merge message 读取（总 Git303，cat-file1/show300、wall7.59秒含未拆分 live GitHub）；这是按历史长度 H 增长的必要 trailer 遍历，不是同对象重复读取，也不以本次空结果证明多 Delivery 行为。

D2 continuity、D3 Task/branch 及未执行正式步骤计数仍待交付；官方逐路径重复 hash 和 task_store 创建读取仍是未解决上游前置，不计整体完成。
