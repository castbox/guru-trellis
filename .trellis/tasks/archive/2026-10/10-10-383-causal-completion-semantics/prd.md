# #383 因果完成语义

## Current authority 与范围

唯一需求 authority：[castbox/guru-trellis#383](https://github.com/castbox/guru-trellis/issues/383)，合同 2026-10-10-r9。TaskId：383-causal-completion-semantics；本任务交付 Guru workflow 的判断能力，不证明业务生产故障已修复。RDT 与 Architecture 当前版本为 current-main-0.6.17-guru.79；旧 #248/Publication/Finalizer 安排是历史背景，不构成执行合同。

## 问题与目标

当前 root-cause qualification 已交付，但 qualification 只判断候选准入；下游仍缺共同因果完成 authority。绿色测试、完整 diff、merge 和 deploy 无法单独证明业务根因消失。已有 Completion pending/refresh transport 的 current-HEAD 定向 baseline 为 8 passed，这只证明原接口传输。

| Requirement | 本次行为 |
| --- | --- |
| R383-01 | 建立唯一 canonical causal-completion-semantics.md，声明 causal_semantics_version 与可复核 content identity；共同正文只定义证据、维度及 disposition 适用性。 |
| R383-02 | 每个阶段从 accepted scope 和实际行为区分 ordinary feature、diagnosis、mitigation、root-cause repair；消费 current #382 资格，不重复未变化机制的资格判断。 |
| R383-03 | Check 对照资格机制和真实 consumer 检查实现、first failure 与目标要求的证据；诊断/缓解不因未知根因单独回程；根因修复缺依据回 Planning，已证实症状抑制回实现。 |
| R383-04 | Branch Review 独立检查完整 committed diff、真实 consumer、失败样本与因果分布，识别实现期新增抑制和 stage/component/operation/time/classification 转移。 |
| R383-05 | Delivery Review 独占公开声明判断，分别报告实现、静态、集成、外部、生产效果、缓解与风险；保留 Refs-only。Publish 只执行已审 payload。 |
| R383-06 | Completion fresh 读取完整 accepted scope、live source、全部业务 Delivery 和当前证据。诊断/缓解/implementation-only 能完成自身范围，但不冒称根因闭环，不关闭仍要求修复的 source/parent。 |
| R383-07 | 要求生产修复而证据不足时，同一 task 保持 active，evidence_pending 等待新证据；Delivery exact merge_result 和 Reactivate current anchor 分别支持 evidence_refresh。 |
| R383-08 | 充分的严格等价生产证据能支持完成；等价性由 Completion 对原故障关键条件、状态、路径、运行条件和观察结果判断。不强制危险重放，不制造阈值/账本。 |
| R383-09 | 共同语义改变从最早受影响 owner fresh 重审；canonical、dogfood、installed、声明平台和 reapply/drift 一致。保留 current exits、唯一 consumer、合法 protection 与零资格持久化。 |

## 行为验收

下表是 requirement 派生的可观察结果，不是供 native evaluator 读取的答案。

| Case | 正常事实 | 必须观察的结果 |
| --- | --- | --- |
| C01 | 修复声称通过 admission/config gate 排除原合法输入 | Check 拒绝症状抑制，保留失败输入，回实现；不宣称 root_cause_fixed。 |
| C02 | 分类变成成功，但业务结果仍失败 | Check/Completion 不以 classification 单维度判修复。 |
| C03 | retry 只展示最后错误，first failure 被遮蔽 | Check/Branch 保留首个失败并要求机制修订，绿色 retry 不证明修复。 |
| C04 | fallback 返回不完整成功 | Delivery 不发布完整修复声明，回实现或公开真实 slice。 |
| C05 | 实现期新增 filter/default/fixture，使测试假绿 | 完整 Branch Review 发现当前缺陷，回实现。 |
| C06 | 原失败转移到其它 stage/component/operation/time window/classification | Branch/Completion 不给 root-cause 完成，分别说明移动维度与剩余影响。 |
| C07 | current authority、protected object、real harm、direct owner 支持合法 protection | 保留保护，不以禁止症状抑制为由删除。 |
| C08 | diagnosis-only 工具/调查满足自身 scope，根因仍未知 | Check、Branch、Delivery 能通过自身目标；Completion 能完成诊断，声明未知且不关闭 root-fix parent。 |
| C09 | mitigation 自身效果/风险、owner、期限、退出证据满足，根因仍未知 | 正常交付与完成缓解；保留剩余根因，parent 保持 Open。 |
| C10 | accepted diagnosis 明确要求定位根因，仍未知 | 不能完成该范围；按确切缺口返回 remaining_work 或实际 revision owner。 |
| C11 | root-fix 缺本阶段 first failure/causal/counterfactual 依据 | Check 返回 planning_stale；调查由现有 Planning 承接，不阻塞已合格独立诊断/缓解。 |
| C12 | dangerous replay 无法安全执行，已有严格等价证据充分 | Completion 能依据合法证据判断修复，无新增生产操作。 |
| C13 | 只有数量相同/失败率下降，等价关键条件未证明 | Completion evidence_pending，说明具体缺口。 |
| C14 | merge/deploy 完成但 accepted production evidence 未到达 | 同 task active，不 archive、不生成替代 task，也不即时循环重审。 |
| C15 | Delivery-based 新证据到达 | 使用同 generation 的 exact merge_result 进入 evidence_refresh，再判断根因是否消失。 |
| C16 | Reactivate-only 新证据到达 | 使用 current reactivation_anchor 与本代 evidence，旧 merge/Finish 不替代当前依据。 |
| C17 | 普通 feature 满足 RDT scope | 正常 completed，不要求业务生产根因证明。 |
| C18 | implementation-only scope 已验证实现 | 完成本范围，公开 production_effect_unverified，不关闭要求生产闭环的 parent。 |
| C19 | 正常外部变化使 authority/evidence/identity stale | fresh reread 或回最早受影响 owner；无伪造 stale 负例。 |
| C20 | 全部 accepted scope 和 closure disposition current | completed 只交给 guru-complete-task-closure，随后才进入 Finish。 |
| C21 | merge 后同 scope 尚需实现及第二次 Delivery | 同 task 经现有 implementation/additional-delivery 路径继续；merge 不是 Completion。 |

## Delivery policy 与非目标

一个 Delivery slice 覆盖 R383-01..09；remaining_work 为空时仍须全部验收完成才判断任务完成。该 slice 独立使用共同语义与原 owner，既不依赖 #468，也不接管业务生产效果。未取得 native 行为证据或声明投影证据时，本任务验收仍未完成，不能用确定性 checker 绿色替代。

不实施 #468、#464 或 #404，不重建 #382 qualification、Delivery discovery、Completion、Finalizer 或全局 graph。不新增 global causal DTO、数据库、永久 aggregate、review history、authorization state、固定生产阈值。不扩大攻击、篡改、竞态压力或 crash consistency；不访问/修改业务生产。完整累计 Upgrade/Release matrix 由专门 owner 承担。
