# #569：交付历史查询的数据准备与固定截点接续

本文件定义 Planning 阶段需求；不作为规划批准、激活、实现或验收通过的证明。

## 来源与范围

Direct Source：[castbox/guru-trellis#569](https://github.com/castbox/guru-trellis/issues/569)，正文 updated_at 为 2026-10-15T12:27:54Z，当前评论为空。正文“必须满足的行为”“验收”“关联与范围边界”为 requirement authority；原查询 owner、完整性、隔离和兼容约束为规范性约束。具体 Git 获取机制和最小公共接口版本由当前设计选择。source_selection 的最终设计处置仅在 design.md 单写。

当前 Architecture：docs/architecture/README.md 的 current-main-0.6.17-guru.92；RDT：docs/requirements/README.md、docs/design/README.md、docs/test/README.md 的 current-main-0.6.17-guru.98。ADR-026 保有公开 Delivery 归属和 query1/query2，ADR-028 保有固定内容与原阶段 owner；本项是原历史查询能力内的增量。

仅处理 #569。不操作 #566 原会话、Task、Delivery、worktree 或业务仓。#567 已交付是当前事实，不是本项产品前置。旧安装开发 carrier 和 current canonical/matching-installed 产品验证分开，不在此项顺带迁移开发 Task。

## 用户和正常流程

历史查询 caller 包括 Merge 后的 Completion、独立查询与会话恢复。远端真实 Delivery 已合入，而 caller 的 origin/base 落后或必要对象缺失，是受支持的普通状态。当前 discover 在比较 local/remote base HEAD 后直接返回 stale_identity/history.base_ref，使 caller 另行 fetch；当前 public result 也未显式携带 cutoff。不能以移除检查、返回空列表或同步任务分支修复。

期望：一次 query 固定 repo/base 的真实远端 commit，原 history owner 在同一操作内准备所需对象，扫描、核验并返回完整至该截点的实际历史；实际 consumer 根据公开截点和任务身份继续原阶段。

## 需求与可观察结果

| Identity | 来源 | 当前需求 |
| --- | --- | --- |
| R569-01 | 行为1/6 | 查询取得一次远端 repo/base/commit 截点，数据准备、first-parent 扫描、PR/merge/父提交/reviewed head/trailers/public fact 校验均绑定同一 commit。 |
| R569-02 | 行为2/3 | 原 query1/query2 owner 在 local ref 落后或缺所需对象时自动有界准备；已具备必要历史直接复用；不新增同步 Skill、用户 fetch 步骤或共享缓存/状态库。 |
| R569-03 | 行为4/5 | 只读不写业务、Task、Delivery 与交付事实；如实声明实际必要 Git 数据写入。caller/其他 worktree 的 HEAD、index、工作文件和共享远端跟踪 refs 保持原状；无 merge/rebase/Reconcile/同步提交。 |
| R569-04 | 行为7 | 远端从 B1 前进 B2 后，本 query 完成 B1，不追赶或重新开始；public result/调用上下文让 consumer 明确识别 repo/base/cutoff 与适用 Task 身份。 |
| R569-05 | 行为8/11 | 网络/权限、获取失败、必要历史不完整、身份不一致或不可核验具体失败；完整扫描且没有匹配 Delivery 才能成功返回空数组。 |
| R569-06 | 行为9 | query1 既有历史/迁移语义及 schema1/2 trailers 保留；query2 融合已记录实际 Delivery 与合法 trailers，核验归属和截点内可达性，保持真实顺序与去重，不创建事实。 |
| R569-07 | 行为9 | 截点后的实际 public Delivery 不使 B1 结果失败；本次应覆盖但无法验证的事实仍具体失败，不静默漏报。不按记录时间或本地 ref 猜测归属。 |
| R569-08 | 行为10 | 复用现有 public I/O。真实 consumer 必需的最小截点字段有明确 schema 与成套迁移合同；无长期审计 aggregate/ledger，既有 API 不静默破坏。 |
| R569-09 | 行为11 | Markdown/AI owners 判断适用性与路由；脚本只读取事实、准备对象及验证客观一致性。无关 B2 直接消费，明确本任务新增交付或所需证据变化由原 owner 有界补取，保留旧事实含义，不回退业务阶段。 |
| R569-10 | 验收1/2/3/7 | 真实或代表性 matching installed 公共 Merge→Completion、独立/恢复、结果丢失恢复与 fixed-cutoff consumer 链必须实际执行；schema/unit 成功不能替代。 |
| R569-11 | 验收6/7 | canonical、dogfood/installed、Skill/contracts/runtime/schema和声明平台投影一致，完成定向回归、reapply/drift 与影响隔离；不扩完整多平台 Release 矩阵。 |

## 验收与验证边界

| Test group | 来源验收 | 证据与预期 |
| --- | --- | --- |
| T569-01 | 1 | matching installed 原 Merge 返回 delivered，local origin/base 停在合入前且缺新对象，原 query 自动取齐，原 Completion 消费该结果；无人工 fetch、任务同步或新业务 gate。 |
| T569-02 | 2 | 没有邻近 Merge stdout 的独立与恢复 query 同样工作；已具备必要历史不获取，公共结果中 repo/base/task/cutoff 完整。 |
| T569-03 | 3 | B1 后远端变 B2。B2 无关增量直接消费；明确同 Task 新 Delivery 时只补缺少事实。原 query 不重启/追赶，结果丢失由原 owner 正常重新取得公开结果，consumer 不读私有 checkpoint。 |
| T569-04 | 4 | query1/query2、多次合法 Delivery、schema1/2 trailers、public manual fact、去重、bookkeeping 排除和合法空列表。截点后真实记录与本次应覆盖但缺验证的事实有不同可观察结果。 |
| T569-05 | 5 | 正常网络/权限获取失败、必要历史不完整及真实身份 mismatch 返回定位原因，不伪装空结果/成功，不触发重规划重实现。 |
| T569-06 | 6 | 对比操作前后 caller/其他 worktree HEAD、index、工作文件、Task/Delivery 字节和共享 refs；枚举实际 Git metadata 变化。 |
| T569-07 | 7 | source/installed 公共 wrapper、实际 consumer、canonical/platform bytes/modes、reapply/drift、sidecars 定向验证；逐层报告实际结果与未验证边界。 |

独立的 Phase 2 semantic Check、首次完整 committed Branch Review、Architecture/RDT promotion 后新差额的 fresh gates、PR readiness/expected-head merge、Completion/Closure/Finish/Cleanup 仍由各原 owner 执行。查询成功不授予这些结论。生产原始现场/业务仓采用、完整多平台 Release 矩阵、软件版本发布不是本项验收。
