# #553 设计

## 当前对象与选择

Direct Source：[Issue #553](https://github.com/castbox/guru-trellis/issues/553)。当前 canonical Reconcile 的 `delivery_post_plan` 先整合再交 `delivery_activation`，普通 candidate 不解决冲突，普通 persistent executor 自行 merge。已有 `delivery_resolved_candidate` 属于实施后 Check。候选直接补齐原 post_plan owner 的 resolved baseline 消费，不改变这些 owner，也不创建 Skill、external exit、公共 handoff、gate store或第二状态机。

独立 candidate_assessment 已由完整旧 dogfood Planning 3.0 owner 实际返回 baseline_current/no_architecture_impact，baseline `current-main-0.6.17-guru.89`、constitution v1；只用于本 Task Author。canonical 产品验证使用已核对 tar 内容身份的 schema2/Delivery API组合，二者不跨模型借用 DTO/gate。无 owner、architecture决策、GAP或 compatibility exit改变，不制造 contribution/ADR。final_plan、Phase2、Branch Review仍独立调用原Architecture owner。

## 原 owner 与私有请求

原 `execute-base-candidate` 和 `execute-base-reconciliation` 请求增加闭合 `resolved_candidate={stage0_tree,integration_paths}`。这是同命令内的显式当前能力：省略字段仍执行原无冲突算法；persistent请求带该字段仅适用于 delivery_post_plan/delivery_activation。两个字段分别由 candidate preview与exact executor直接消费。原Skill输入、reconciled输出和recorder结果保持。

Reconcile AI读取同 Task/gen/DeliveryKey、live source、已批准规划和exact base delta；解决真实文档冲突，明确哪些路径属于基线整合，哪些属于pending planning/implementation。AI构造只含受审整合的 stage0 tree：在临时index复制当前stage0，再将未选路径恢复prior HEAD条目；真实index/worktree保持。此路径选择、authority/规划适用、内容充分性与validation选择全归AI。

复用candidate命令校验并对该tree运行显式argv-array validations，返回原candidate事实。脚本不解决冲突、不选路径、不审查内容。临时checkout加载tree，仅运行本轮AI选定的基线验证；未实现业务测试不属于基线前置。

AI完成基线语义Gate后，展示 branch、Task/Delivery、prior HEAD、operation pair、MERGE_HEAD、受审paths/tree/digest、message、父顺序与零remote effects，并消费当前对话的精确副作用确认。授权不写文件、请求、schema或结果。

## 确定性核验与提交

D553-01：原identity owner核对同Task/gen/DeliveryKey和C4/current branch；actual HEAD==prior_task_head，selected ref==new_base_head，old pair来自唯一live merge base。
D553-02：存在一个MERGE_HEAD且等于new base；无unmerged和其它sequencer。树对象可读；prior→candidate的全部差额必须包含在integration_paths，每个受审路径在真实stage0与受审tree中的mode/oid/stage完全一致。受审路径存在unstaged变化时停止；无关dirty/untracked继续保留。树digest复用原index_tree_digest；不创建新digest authority。
D553-03：临时GIT_INDEX_FILE加载受审tree，执行普通git commit。真实index不替换、不stash、不重置worktree；正常commit退休MERGE_HEAD。读回commit parents=[prior,new base]、tree/message/digest和parent ancestry；返回原delivery reconciliation receipt，原record/check/invoke验证committed tree并返回reconciled→delivery_activation。
D553-04：同请求结果丢失时，仅当当前HEAD就是原精确parents/tree/message且merge/sequencer终态已退休，返回同commit的原receipt；保留dirty允许。不重复commit、不amend、不从status推断Gate。其它HEAD/base/pair/tree变更停止，由原owner fresh reread/re-entry。
D553-05：若未解决、受审路径变化、base/HEAD变化或真实authority/planning变化，保留原状态，沿原blocked/planning/implementation/clarification owner；不把未实施业务缺陷改名base finding。
D553-06：只基线验证不创建Check/TaskCommit/full review/readiness结果。新公共Planning接受仍归Activation，后续实施和完整业务Check照常。

## 来源设计约束处分

| 来源承诺 | 处分 | 落点与依据 |
| --- | --- | --- |
| 目标：原Reconcile承接实施前候选，不预设新Skill/exit | retain | 原post_plan和原命令内闭合请求，无新owner/exit/store |
| 验收2：基线证据独立于业务Phase2 | retain | AI baseline Gate +原receipt；不进入Check profile |
| 验收3-4：身份/规划与无关内容保留，只提交受审候选 | retain | D553-01..03及same-key公开接续回归 |
| 验收5-6：exact live facts、原owner失效和同操作恢复 | retain | D553-01..05，不伪造旧Check或第二commit |
| #407与#530现有职责 | retain | 原实施后resolved和无冲突/committed-reentry代码及回归保持 |
| 验收7与非目标 | retain | implement定向安装/投影/reapply/drift；旧D2拒绝和业务/Release边界明确 |

Issue允许Planning选择具体机制，未引入规范性外部设计。上述约束保留，不改变产品goal或accepted scope。

## 差额与最小必要复杂度

现有无冲突executor不能消费active resolved merge，现有实施后executor的Check前置与全clean条件不能用于实施前pending规划。直接复用原owner、candidate验证、digest和receipt，比新增Skill、checkpoint、代理Check或手动制造输出更直接。新增代码只承担这一确定性Git能力；不为旧public格式增加dual reader，不升级旧dogfood，不处理攻击、竞态或crash。
