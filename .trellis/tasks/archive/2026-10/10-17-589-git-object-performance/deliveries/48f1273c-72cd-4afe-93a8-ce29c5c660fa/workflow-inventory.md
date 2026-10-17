# D3 全流程 Git 操作盘点与剩余责任

## 证据口径

本表承接D1 research/git-object-inventory.md，不覆盖其历史。native根Trace2为/tmp/guru-589-diagnostics/formal-chain/git.trace.jsonl，operations.json以字节边界和原命令标识一次操作；下列是截至D3测量完成时各原命令最近一次实际样本（索引从0）。D1/D2已交付门禁与D3规划样本混列但不冒称同一after候选；后续D3门禁会继续向原trace追加。native wall含未拆分provider等待，不作本地改善；此处只陈述实际计数。Git/show/cat-file/ls-tree以一次操作全部子进程为范围。

| 原native步骤/命令 | operation索引 | Git/show/cat-file/ls-tree | wall秒 |
| --- | --- | --- | --- |
| guru-review-task-delivery/scripts/invoke.sh | 72 | 17/0/0/0 | 0.773 |
| guru-publish-task-delivery/scripts/preview-task-delivery-publication.sh | 73 | 21/0/0/0 | 4.259 |
| guru-publish-task-delivery/scripts/invoke.sh | 74 | 69/0/0/0 | 27.609 |
| guru-merge-task-delivery/scripts/preview-task-delivery-merge.sh | 75 | 12/0/0/0 | 3.806 |
| guru-merge-task-delivery/scripts/invoke.sh | 76 | 27/0/0/0 | 12.191 |
| guru-review-task-completion/scripts/invoke.sh | 77 | 0/0/0/0 | 0.284 |
| guru-create-delivery/scripts/invoke.sh | 78 | 1414/0/0/0 | 16.026 |
| guru-qualify-normal-scenario/scripts/invoke.sh | 99 | 471/0/1/0 | 6.272 |
| guru-qualify-solution-mechanism/scripts/invoke.sh | 100 | 471/0/1/0 | 5.479 |
| guru-qualify-root-cause/scripts/invoke.sh | 81 | 1/0/0/0 | 0.245 |
| guru-author-task-plan/scripts/invoke.sh | 83 | 473/0/0/0 | 5.604 |
| guru-review-contract-wording/scripts/record-contract-wording-review.sh | 85 | 469/0/0/0 | 5.595 |
| guru-review-contract-wording/scripts/check-contract-wording-review.sh | 86 | 469/0/0/0 | 5.614 |
| guru-review-contract-wording/scripts/invoke.sh | 87 | 469/0/0/0 | 5.640 |
| guru-approve-task-plan/scripts/record-planning-approval.sh | 90 | 469/0/0/0 | 5.668 |
| guru-approve-task-plan/scripts/check-planning-approval.sh | 91 | 469/0/0/0 | 5.388 |
| guru-approve-task-plan/scripts/invoke.sh | 92 | 469/0/0/0 | 5.481 |
| guru-activate-delivery/scripts/invoke.sh | 93 | 469/0/0/0 | 5.734 |
| guru-check-task/scripts/record-phase2-check.sh | 68 | 6/0/0/1 | 1.766 |
| guru-check-task/scripts/check-phase2-check.sh | 69 | 7/0/0/1 | 0.801 |
| guru-check-task/scripts/invoke.sh | 70 | 21/0/0/1 | 1.229 |
| guru-create-task-commit/scripts/prepare-task-commit.sh | 66 | 38/0/0/0 | 0.980 |
| guru-create-task-commit/scripts/invoke.sh | 71 | 40/6/5/5 | 1.003 |

Planning native大量Git来自本机数百worktree/ref的当前live身份/拓扑/归属检查，不是数百次blob内容读取；当前样本show/cat-file/ls-tree为0。它们不作为D3的热点耗时改善证明。必要branch/worktree遍历与对象内容重复读分开，不能把计数下降等同删掉检查。

## 逐步骤处置

| 范围/入口 | caller、操作对象与增长 | 当前证据和处置 |
| --- | --- | --- |
| Intake/Sync/Discovery | live source/选择base、archive和Task身份；mutable refs/remote/worktree | 当前Task已进入执行，不能为补计数重做Intake、创建第二Task或同步共享base。原Intake未挂Trace，无法追溯精确计数，明确unverified boundary；其Task/branch/checkout读取由本D3真实公开fixture及功能回归承接，不把缺计数说通过。 |
| Task创建+ensure | composition按branch/head检查Task树和每Task JSON；官方writer另一个unique-head扫描 | source10/100：137→117、407→207Git；show30→10、300→100；ls-tree3→2，唯一OID batch1。ensure18Git固定。Guru热点已优化；official writer N次show仍是上游前置。 |
| Task/branch/checkout身份 | branch_resolution两次discover、原current worktree/ownership/expected head | 10/100分支67/427→24Git，show24/204→0，cat22/202→1、ls-tree2，内容只1unique472B。两次resolve每输入检查保留；当前worktree identity不能用committed cache替代。 |
| 历史Issue归属 | identity original archive candidate task/summary/source/seal/generation | 调用期批量事实+逐archive/对象解析，原每input归属/唯一性判断保持；当前Identity4+Lifecycle160测试含历史/缺失回归，不将两个固定Reactivate读取机械批量化。 |
| Planning/Activation | Author/Wording/Approval/Planning public writer，三份规划当前文件与身份 | 上表native逐条实际计数；文件内容在worktree，不能跨操作cache。保持所有semantic gates。 |
| Implementation/Check | 当前HEAD树、dirty index/worktree和content identity | 上表Check原记录/校验/invoke各1次树枚举；hash-object构建当前内容不是已知immutable重复读。source/private tools和功能验证不代替完整Check。 |
| TaskCommit | 原候选五份规划/上下文固定存在性、精确commit/message/parent/tree | 上表真实commit invoke40Git、6show、5cat、5tree；这些分别有精确候选及结果恢复consumer，固定小量不统一套加速要求。 |
| 完整BranchReview | 原全B..HEAD+当前Check、dirty/index/mode/gitlink | joint冲突链12真实wrapper含当前Check→projection→完整Review通过；原Review不被bounded pass替代。D3后续fresh committed Review仍独立执行。 |
| bounded continuity（D2） | 原tree_identity OID去重、逐path贡献、record-local tree memo | D2已交付固定门槛全部通过，详见D2 performance-results；D3原pull_request实际无冲突整合测试1项通过（5.406s），包括当前Check、bounded、不能替代fullReview及原Readiness consumer。 |
| DeliveryReview/Publish/Merge | exact reviewed head/PR/base/事务/恢复；少量commit及祖先 | 上表D2 native真实公开Readiness/Publish/Merge计数，PR594已真实合并。D3工具尚未发布，不借旧门禁声明当前pass。 |
| Completion/历史查询（D1） | 固定query截点，候选paths/多Delivery，原归属与重建 | D1原固定100/1000路径与2/4Delivery量化已交付；D3 Merge66回归及共享提取后4组RSS全部通过。当前native空查询的300个different first-parent message是必要H遍历，不能当同对象重复。 |
| Closure | 当前source Issue、Completion及精确disposition | 原公开retained-source fixture：首次/原结果恢复均3Git，show/cat/tree0；Issue保持OPEN。来自d3-terminal-counts-v3/operations.json第3/4操作。不是当前589实际Closure。 |
| Finish | 原archive task/summary/active消失与bookkeeping事务 | 原公开fixture：archive投影7Git，publish31Git；merge37Git/cat6；terminal recovery18Git/cat3；show/tree0。原live target/归属验证保留，三处检查固定。用本地bare remote及provider fixture，不是live GitHub bookkeeping；当前Task未Finish。 |
| Cleanup normal | 原sealed资源精确head/ownership/当前使用与结果恢复 | 原公开fixture preview6、实际cleanup11、结果恢复3Git，show/cat/tree0。只删除临时fixture资源，当前worktree/branch未清理。 |
| Cleanup manual | manual_targets_current按selected refs树及active Task读取，删除前原复核 | 新正常热点：10/100个same-head旧Task快照refs，public dry select实际63/513Git、12/102show、10/100tree，0cat。原normal资格classified；后续独立Delivery承接，未计已完成。 |
| 资格校验 | 少量明确commit身份存在性，当前事实和eligibility | 上表normal/solution各cat1固定，root0；身份与语义资格是独立用途，不要求cat清零。 |

## 优化清单

D1历史/手动恢复已交付；D2连续性已交付；D3 Guru生命周期读取已实现并达到固定性能/资源门槛，当前仍需本批完整gates。新Cleanup手动同head重复事实读取进入下一独立Delivery，不因本次slice结束而移出整体scope。

## 保留与未完成清单

1. 原每份输入结构/Task/Delivery/关联/祖先/摘要/恢复校验、移动ref/index/worktree刷新、固定少量存在性与结果确认全部保留，原caller仍拥有business/semantic判断。
2. 必要branch/Task/history遍历单独记录；标准流程外tools-only source/preimage维护计数不混作业务链加速。
3. 官方task_store创建逐pathshow与delivery_store.candidate_content_ref相同blob多path重复hash仍存在，当前公开API没有预计算hash注入口；本repo不得patch .trellis/scripts/npm/node_modules/hook或复制上游摘要。该不可分离前置未完成，对应整体范围仍未完成。
4. 当前Intake无追溯计数是明确边界，后续既有正常入口证据只能补当前事实，不能伪造当时计数。当前Closure/Finish不可执行，因为wholeTask未完成；上述fixture计数不把当前Task状态推进。
5. 完整多平台/Release矩阵、formal Fork lock、软件发布、业务仓采用/部署不在本批证明，分别由原owner承接。

后续原Completion直接消费本盘点的剩余工作与边界；本文件不是public Skill DTO，也不记录授权、reviewer身份、全过程审计或语义pass替代物。
