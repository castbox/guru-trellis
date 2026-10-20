# #635 跨环境生命周期迁移

本合同覆盖 shared archive、最小 Closure 共享结果及显式既有 PR 恢复的 matching 迁移。当前 canonical 实施、目标安装与实际原生链是不同状态；本文不宣称全部 R1–R5/V1–V8 已完成。

## Current 入口与输出

原 guru-reactivate-task 使用 delivery_reactivate_shared_archive；独立输入包含 archived_lifecycle 与完整 archive_anchor。新 aggregate、semantic result 和 transaction 使用独立 schema identity。Planning output/consumer 3.0 返回实际非负 binding revision，其他仍适用的最小出口保持。新 profile 的 pending resume 继续使用 TransactionRef：generation 只定位已冻结公共 plan 的目标代，不声明 active；唯一 resume consumer 以 transaction_id/result_id 回原 operation，不能交 Planning/Bind。applied 后才消费真实 SDK key/ref。source_correction_required 从 current Interface、global workflow 和 executor 退出。

旧 delivery_reactivate_completed_task/bare-key、seal/correction 输入与 1.0 私有交易不被重解释。历史 schema 文件保留为非 current 定义，旧完整安装固定原版本；在途旧操作由匹配 pinned owner 或逐案原 owner 处置，不迁移授权、不补造 seal。

## 两仓与状态边界

matching provider 是 source-lock 指定 Trellis e9fb95fd2eb0fb8441153e77384a9dfd3ea3358f 的成对 CLI/Core。正式旧 schema1 只经其 formal_archive_reactivation SDK，TaskId/source/history 保留且首次只增代一次；Task2 继续公共 reopen。人工历史沿原 maintenance，未完成 closeout 回原 Finish。

该 matching provider 已采用上游 #56 的共享快照修复：`inspectFormalArchiveReactivation` 先验证所选 root 的唯一后继，再以同一 provenance、保留 source 和中间 Completion 校验 registered siblings。同一正式前驱的同代或较早快照不要求业务正文相同，查询仍只返回所选 root 的实际 key/ref；root 无后继而 sibling 独占、更高代 sibling 或关系不匹配仍具体阻塞。已有后继继续阻止再次 prepare，原固定 operation 的结果保持原输出代，公共 DTO 不变。Guru 继续调用该 SDK，不另建 formal successor parser。

上游真实 Git 回归已覆盖 linked apply 后提交、main 快进共享快照、receipt 丢失、同代 scope 前进及 root 后来合法 reopen 的组合。它们证明公共 API 的对应行为，不代替 Guru 目标安装、实际 session/Bind 或完整原生再次 Finish；精确来源和成功 main CI 见 source lock。

共享 Finish 从准确 Git、公共结果和 live bookkeeping PR 核验。原机 seal、退出和 Cleanup 仅服务原本机资源；同资源冲突、generation、repository/full remote ref/expected head 继续有效。

## Closure 与 Finish

Closure current Interface 1.8 选择 input aggregate `guru-complete-task-closure-input-3.0`。原 `completion_approved` 的独立 input 2.0 保持原义，新 `closure_shared_result_recovery` 使用独立 input 1.0，输入为 mode、TaskRef、ResultRef 和共享载体 AuthorityRef。原五个 typed exits 及唯一 consumers 保持；semantic aggregate 3.0 选择对应独立语义输入，不把旧输入重解释成共享恢复。

原 Closure 单写 `closeout/closure/<base64url-result-id>.json`，独立 schema `guru-closure-shared-result-1.0` 仅含原 result_ref、completion_result_id、source、action_set 及 schema_version。文件随 Task 提交/归档，由公共 Closure evidence 关联。它不是 terminal、授权或第二 Closure 模型。原 Finish reader 经公共 evidence 和原 authority resolver 读取，继续输出既有 snapshot2.0；schema2 归档使用官方 relocation helper 保留 artifact_origin，不能 raw move 后覆盖原 record。

私有交易缺失时，原 Closure 重新审查精确公共 Completion/source/scope/result、载体及 live required OPEN/CLOSED 状态后，只恢复原 public projection，零 provider close。真实剩余动作或外部漂移回原 Closure；载体不恢复授权。旧无载体的完整已完成 archive 仍按共享历史验证，不追补 carrier 或旧结果。旧在途结果的真实动作输入仍可核验时由原 Closure 逐案承接；输入确实不可获取时说明缺失及对应 consumer，不能按 CLOSED 或 aggregate terminal 猜原动作集。

## 已有 Open PR 恢复

Publish current input aggregate 使用 `guru-publish-task-delivery-input-delivery-aggregate-3.0`，新增两个独立闭合 input 1.0：`delivery_remote_draft_recovery` 与 `delivery_remote_ready_recovery`。原本地 profiles、typed exits 和 consumers 保持。两者显式选择 pr_ref、source_commit、TaskRef/DeliveryKey；各自剩余 payload、candidate 或 readiness 字段由 package profile 单写，不向原本地输入添加 nullable recovery 字段。

source commit 必须承载可获取的同一 Task/Delivery/必要代码，不要求先进入 main。原 Publish 核准确 repository/base/head/source/公共关系，区分远端 PR ref 与当前本地 binding，沿原 executor 只补剩余动作；两个入口不创建 PR。Ready 仍要求当前原 readiness 适用，历史 Ready 和 phase 不代表 pass；新未审修订保留 #636 的先退 Draft 顺序。MERGED 使用原 Merge 公共结果恢复，零第二次 merge。更新远端 ref 不授予清理原机或共享 ref 的 ownership。

## 分发与验证

本批只修改 canonical source。当前 installed/dogfood 不热迁移。P6/I07 由原 tools/installer owner preview 后成套更新官方 native reader、Guru packages、workflow/spec 和平台投影，保持 Task/session/历史字节并逐项处理 sidecar。不得用修改 .version、绕过旧档 preflight 或批量改档制造成功。

测试中的临时 Git/受控 provider 和 SDK fixture 分别只证明对应层。原环境 owners 的独立 clone/非 main ref、双 Task、同名 local branch、旧 pending 与推进 remote ref 定向测试不等于实际 Agent 完整链。真实独立 clone 原生两条再次 Finish、完整安装/reapply/drift 及 V1–V8 仍需原 owner 实际执行。source 测试通过不是整体验收或 Release 矩阵。
