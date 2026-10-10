# 完善 Direct Source 与活动重规划兼容性

## Requirement authority 与范围

唯一 Direct Source 为 castbox/guru-trellis#468，task source 为 portable IssueSource / exact_source；该 live Issue 的当前正文与权威 comments 是本任务需求 authority。当前 baseline 为 main@8dfa2a35bd2ccae236f7b8bc679f107f3ec1ffde，已交付 #454、#434/#435、#436、#464 必须复用。本 PRD 是当前任务 delta，不替代 repository current Requirements。

全部交付仍为一个独立 Delivery：现有 semantic owner 对 Direct Source 修订、明确必要外部事实、仓库 SSOT 与重开分流的兼容，以及活动重规划正式恢复执行。上游修复不证明 Backend #148 安装或业务重试成功。

## Current-contract gap analysis / 正常场景

| #468 场景 | Current owner / 正常承接 | 当前差额与验收层 |
| --- | --- | --- |
| 1、3 | Intake / Clarification / Planning reread live Direct Source | 已有支持；定向验证当前仓库 accepted scope 与 Planning 前普通修订 |
| 2、11、15 | #454 Source Relation 与各 stage 的 requirement authority | 已有单一 portable repo_ref；验证 Coordination/Related 链接不改 source 或拓扑，保留跨 repository Direct Source |
| 4、6 | Clarification、Planning、Check、Delivery、Completion；#464 dependency-scoped invalidation | 按实际依赖回最早受影响 owner；只补缺少说明和定向回归，不建立 revision binding |
| 5、8 | 同一 semantic owner 对必要依赖的适用性判断 | 明确信息性变化不自动失效；Coordination 未同步不自动改 task |
| 7、9 | accepted scope 的必要依赖/必要证据；Completion evidence_pending、remaining_work | 验证完成条件与事实不足的诚实路由，纯信息和 Follow-up 不成为阻塞 |
| 10 | Completion requirements_revision_required 或原阶段适用 owner | 复用原回程，不新增 Completion/Closure |
| 12 | #454 NoIssueSource 与 #436 no-mutation Closure | 完整 no-Issue 生命周期，不虚构 source、协调关系或 closure |
| 13 | active continuation、unfinished closeout 原 transaction、正常归档 Reactivate | 按 TaskId、生命周期和实际 closeout 事实分流；Issue 重开本身不改变 generation |
| 14 | 现有 RDT / Architecture maintenance 与 Completion | 验证仓库实际适用长期 authority 的必要更新或不适用；不要求通用 Baseline 类型 |
| 16 | Planning approved -> phase-1-task-activation -> guru-activate-task | 已确认真实行为缺口：新活动重规划不能再次 planning -> in_progress，也不是首次 activation 输出丢失；需在现有 owner 上正式接续 |

所有场景来自 #468 明确正常路径；不包含人为伪造 artifact、恶意 actor、竞态/锁、crash consistency 或额外攻击矩阵。必要外部事实只由 accepted scope 的明确用途决定，不根据仓库位置、链接方向、父子/上下游称谓推断。

## 结果与行为验收

1. 唯一 Direct Source 或合法 no-Issue 清晰；其他 Issue 不进入 task source、session、branch/resource identity 或 Closure authority。
2. current owner 逐阶段读取 live authority，判断真实语义依赖。material change 回最早受影响 owner；已证明语义等价的变化仅刷新直接依赖，遵守 #464。
3. 保持 exact_source / reference_only / follow_up / parent 已发布语义；只有经 current Closure owner 核对完成资格的 exact_source 进入 Closure mutation。
4. 首次 activation 经正式入口仍只写 planning -> in_progress，真实首次输出丢失使用原 read-only recovery。
5. 活动 task 在 current Clarification/Planning、展示和当前对话接受之后，消费正式 producer approved DTO，正式恢复执行；TaskId、generation、branch、registered checkout、in_progress 保持不变，零重复 status mutation、零新 task/branch/worktree。
6. 正常压缩或换会话：未完成恢复时，丢失/过期 semantic DTO 回原 producer fresh 重审；当前对话无法确认接受则重新展示并取得接受。完成恢复但输出丢失时，原 owner 的只读结果恢复返回实际 typed route，不冒用首次 activation recovery。身份、内容、base 不匹配回正确 owner 或拒绝。
7. 定向测试观察生产 wrapper 的 typed outputs、任务 metadata 字节与 Git/control-state before/after；不能以自构 DTO、文字包含或 canned pass 代替行为。
8. 必要 repository SSOT contribution、独立 review、promotion 和 fresh downstream gates 完成后才可 Publication/Completion。canonical/dogfood/installed、声明平台、适用 reapply/drift、sidecar/mode 保持一致。

## 单一 Delivery 与剩余边界

Delivery slice 覆盖以上全部 #468 accepted scope，不隐藏后续实现工作。独立交付条件：修订 runtime/control-plane 与 DR468-02/03 的 workflow、Planning、Lifecycle、Check consumers 一致，定向正常场景证据充分，SSOT 已按 implement.md 的 Docs SSOT Plan 完成治理，current Phase2 / exact-range Branch Review / Delivery Review 均通过。

Backend 安装、业务重试、业务生产效果、远端发布和完整 Upgrade/Release 多平台矩阵不由本任务验证；后者仍归专门 owner。它们不成为本任务虚假 passing 项，也不产生后台轮询或业务仓改动。

## 非目标

不实现 Initiative/项目拓扑/多仓同步，不新增第二 source authority、Completion、Closure 或 lifecycle substrate，不缩窄 portable repo_ref，不以 #292 为前置。不 patch Backend 安装或访问生产，不创建授权 artifact、跨 Skill digest 链、结果缓存、通用 dependency graph 或备用未来接口。
