# #557：用户手动合并 Delivery 的正式恢复

状态：Phase 1 requirements candidate，尚未批准或激活。

## 来源与 authority

Direct Source：[castbox/guru-trellis#557](https://github.com/castbox/guru-trellis/issues/557)，exact_source，2026-10-15 Asia/Shanghai 重读正文与评论（OPEN、无评论，updatedAt=2026-10-14T11:53:57Z）。整体 accepted scope 以正文验收1..9为准。没有额外 introduced source selection。

工程载体是 main@ccf67ff157dc006f236870049dda9cba0fafa73f 的完整旧 dogfood；产品目标是 canonical Task2/Delivery API1 与完整 matching 安装。两者不得拼接 DTO 或提前切换旧安装。当前 RDT 为 current-main-0.6.17-guru.95/active，Architecture 为 current-main-0.6.17-guru.89/active，constitution/change contract 各归原项目 authority。

## 目标

原 Merge owner 根据真实 GitHub/Git 和当前公开 Task/Delivery/Publication 关联，唯一归属用户已手动合并的正式 Delivery，记录实际合入事实，然后交回原 Completion。恢复不证明 CI、Check、Review、部署、联合验收或整个 Task 完成。

## Accepted requirements

| Ref | 必须行为 |
| --- | --- |
| R557-01 | 仅承接已有正式创建、规划、检查、审查和发布的 Delivery PR。缺少 trailers/gate 不单独阻止 MERGED 恢复；身份来自公开稳定 Task/generation/Delivery/Publication 与真实 repo/PR/base/head/merge/content，不从 branch/worktree 名、标题或单个 trailer 猜测。 |
| R557-02 | 原 Merge owner 负责语义归属和确定性记录，不再次调用远端 merge。关联不足、歧义或普通 mismatch 给具体缺口并保留原 owner；用户选择不能替代客观关联。 |
| R557-03 | CI 全绿、pending、cancelled/missing、failed 都可记录可靠的实际 MERGED。不得先强制重跑 CI；失败不改 pass，未验证不改已验证，非必要 CI 不自动扩成 Task 验收。 |
| R557-04 | 原 Completion 根据当前 accepted scope、适用 Delivery 和真实证据选择 completed/evidence_pending/remaining_work/其它适用既有出口。缺证据、业务缺陷或 authority 变化仍由原 owner 处理。 |
| R557-05 | 实际内容与原受审候选一致时复用仍适用证据，不重复实现/提交/发布/审查。actual head/content/authority 变化时判断差额及受影响 owner；历史合入事实独立于当前验收，不追认未审内容。 |
| R557-06 | 基线推进、head branch 删除、跨回合/新会话、结果或公共 projection 输出丢失均恢复同一 PR/merge/Delivery；不要求当前 HEAD 等于 merge commit。 |
| R557-07 | Completion/history 稳定读取原 owner 已承接的无 trailers 事实。history 只读，不为 bookkeeping 或任意历史 PR 建业务 Delivery。 |
| R557-08 | 不重写基线/消息，不 amend/rebase 已合入历史，不重复 merge，不造空 Delivery/PR/commit，不改 TaskId/generation。Guru expected-head/trailers、schema1/2 合法历史与正式输出恢复保持；公共 API 变化必须有明确版本、成套兼容/迁移合同。 |
| R557-09 | 同步 canonical workflow/原 owner/runtime/schema/consumer/声明平台投影。执行定向 source/runtime、一个完整 matching installed 手动合并→恢复→Completion 公开链及 reapply/drift。源码、安装采用、原会话恢复分别报告；validator 单测不等于完整链。 |

## 验收与证据

A557-01：当前受支持组合下，同一正式 Delivery 经创建、规划、Check、Review、Publish后发生普通无 trailers/gate 手动 merge，正式原 Merge 返回 delivered 并接续正式 Completion。注明实际 provider、Git 和安装 candidate；fixture-only 或局部函数证据不能冒充完整链。

A557-02：分别覆盖四类 CI 状态，观察真实合入事实、验证状态与按 accepted scope 选择的后续出口，不能统一伪造 completed。

A557-03：验证 same-content 复用、actual head/content/authority 差额判断、基线推进、branch 删除、跨会话/输出丢失、稳定 history 与 bookkeeping 排除。缺关联、歧义和普通 mismatch 留在原 owner。

A557-04：Guru expected-head 正常路径、schema1/2 与已有正式恢复回归；公共 I/O/consumer、兼容迁移、canonical/平台、matching installed/reapply/sidecar/mode/drift 定向验证。旧 source dogfood 如因完整模型迁移前置拒绝 apply，保留真实失败和旧完整安装，不单拷新 writer，不把该状态宣称成功或静默降低验收。

实际结果只由本任务唯一 Test 增量文档拥有。源码、installed、provider fixture、真实 GitHub、原会话采用和完整升级/Release矩阵分别报告。

## 精确边界

只做 #557。不修改、升级、提交、发布、关闭、清理或通知 backend #149/PR#526 及任何相关业务资源/owner；来源现场仅作问题定位，不替代业务联合验收或其关联责任。

不做任意历史导入、第二公共模型/永久 ledger、授权持久化、CI/CD/ruleset 调整、完整多平台/Release矩阵、上游/全局 npm/node_modules 修改、恶意伪造/篡改防御、锁/TOCTOU/压力竞态/额外非常规 fault matrix。

具体 GitHub 合并方式、字段和局部机制由候选 Architecture/方案 Planning 对照真实公共接口确定，不预设新 Skill。来源规范性承诺唯一处置由 design.md 拥有，implement.md 只引用。
