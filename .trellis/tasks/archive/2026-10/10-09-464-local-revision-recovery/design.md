# #464 设计：原 owner 的依赖复核与局部接续

## 设计选择
直接演进既有 Markdown owner 合同；不新增 skill、exit、schema、候选状态、cache 或通用 executor。workflow 只编排已存在的 owner/typed exit。脚本继续只校验当前内容、任务身份、base/range 和已完成判断。
Phase 2 完整当前 scope 的语义审查与 deterministic command 全量重跑是不同职责。每次 owner re-entry 必须当前语义 round；执行事实只在同 owner 当前合法持有、依赖可证明不变时复用。

## 当前入口及缺口
| 场景 | 当前事实 | 必要演进 |
| --- | --- | --- |
| A 修订、B 依赖未变 | Check 合同有 delta classification，真实 semantic change 与 full replay 的表述未给出逐检查复核/重新绑定步骤；private result 只有现有 validation summaries | 在 Check Semantic Loop 中明确当前适用检查集合与逐检查复核；不新增 checkpoint 字段或 registry |
| Publish private state 缺失 / Delivery output 丢失，同一 HEAD 的 BranchReview DTO 仍可用 | Publish 模块返回 review_stale；Delivery ready 的 producer 正常退休 private gate；Delivery Public Entry 要求 new complete Branch Review | Delivery 原 owner fresh review 前判断 checked anchor 的适用性；相同候选/range/合同且 DTO 可用时直接沿既有输入使用 anchor；内容/适用义务变化或 DTO 缺失时重新调用所需 owner |
| metadata/projection/promotion 变动 | Phase 2 content identity 覆盖 tracked/untracked，TaskCommit 校验 exact tree；workflow promotion 已返回 Phase2/commit/full review | 保持一致性算法和 consumer；原 semantic owner 判别真实影响、重新记录当前候选，不能仅用旧 token 通过 |
| base pair 未变 / 前进 | guard 已有 unchanged/new_pair/current_pair；bounded continuity 已存在 | 复用原路由；current schema 正常 fixture 验证；不新建 reconciliation authority |
| mutation output 丢失 | Commit receipt、Publish pre/postimage 与 ready recovery 已存在 | 只补齐原恢复文案及实际正常入口验证，未复现缺陷的 runtime 不修改 |

## Check 原 owner 的步骤
1. 读取当前计划、需求、diff、当前 Architecture 和当前工具链/environment；重新确定全部适用检查，新增检查不能从旧集合继承遗漏。
2. 判断此次 delta 对各结论和 check 的真实影响，不由 changed-path 白名单推导业务语义一致。shared identity 更新先由其原 owner 判断当前适用合同；无实质影响只刷新直接依赖结果。
3. 对每项旧执行事实检查：check id/version、真实依赖集、runtime/toolchain、environment profile、检查对象与结果可用性。检查时读取现有来源；这些维度是审查问题，不是待新增字段集合。
4. 上述依赖语义全部一致且事实仍合法可用：把执行事实作为当前候选 validation 结果的依据，通过既有 summary 明确实际执行对象及当前适用性。旧候选记录不被改写，当前 checkpoint 的内容 identity 由原 recorder 重新计算。
5. 任一维度改变、无法证明语义一致或结果不可用：执行该 check。不同 environment 合法值是重新运行理由，不是配置失败。业务可用性由实际运行结果决定。
6. 完成当前完整 semantic round，保留 findings/未验证边界，再走现有 recorder/check/invoke。TaskCommit 的 retained checkpoint、capture ancestry、exact candidate 校验不变。

检查结果更新仅写原 ignored runtime 或会话，不新增 tracked 证明。结果揭示行为/范围/验证义务变化时回最早依赖 owner。已退休结果不为命中率重新持久化；没有当前可用执行事实就重跑对应检查。

## Delivery / continuation 原 owner 的步骤
调用仍使用 `delivery_review` 输入和现有 `branch_review_commit`。
- 原 checked BranchReview DTO 仍可用，live candidate/base/range/适用合同均未变化：原 anchor 继续有效；fresh Delivery Review 当前十维判断，不重新 dispatch 无关 Branch Review。
- HEAD committed content 或适用审查义务改变：返回既有 Phase2/TaskCommit/完整 Branch Review 路径；base 演进沿 Reconcile/continuity 判断。不能从 Git shape 合成旧 pass。
- 只有 BranchReview 输出丢失且 checkpoint 已正常退休：重新执行 BranchReview 原 owner；不能从 receipt、旧摘要、TaskCommit tree 或 Phase2 checkpoint 恢复其语义 pass。
- DeliveryReview 输出丢失：重新执行 DeliveryReview 原 owner；沿上面条件使用仍有效 anchor，不机械重放 Planning、Check、Commit。
- mutation 输出丢失：优先原 owner 的 read-only result recovery / same transaction；live reread 确认原结果，不重复 mutation。payload 或副作用变化仍需当前独立边界。

continuation 只从原任务/session/route、live authority 和原 owner 当前合法状态提取紧凑输入，不增加持久化 handoff。多 Delivery、证据补齐和 terminal definition 保持既有 owners。

## 具体写集与边界
主写 canonical：
- `trellis/skills/guru-team/packages/guru-check-task/{SKILL.md,references/contract.md}`：逐检查复核、当前候选绑定与局部 re-entry。
- `trellis/skills/guru-team/packages/guru-review-task-delivery/{SKILL.md,references/contract.md}`：相同候选恢复时 current BranchReview anchor 的条件与 fresh DeliveryReview。
- `trellis/workflows/guru-team/workflow.md`：全局 continuation/typed recovery 路由的最小衔接，不复制 step-local 判断。
- `trellis/presets/guru-team/spec/workflow/{workflow-contract.md,skill-package-contract.md,quality-guidelines.md}`：只同步这些 durable boundary 及定向验证义务；不改 reviewed-content identity 算法。
- 上述 package 的 `evals/`、必要的 runtime tests，以及 `trellis/skills/guru-team/adapters/eval/` 中现有 fact-only fixture：正常行为 replay，不把测试 fixture 的格式变化当产品逻辑。只修改本 scope 直接调用的 fixture，不批量治理历史 tests。
- `trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`：导航/验证边界。
- `docs/requirements-design-test-contributions/464-local-revision-recovery/{requirements.md,design.md,test.md,manifest.yaml,traceability.md}`：按原 RDT contribution 合同形成唯一 isolated 三层增量及其 promotion/traceability 导航；不在并行 task 直接改 shared current。

派生写集由现有 apply 安装为 `.trellis/workflow.md`、`.trellis/spec/workflow/`、`.trellis/guru-team/skills/`、`.agents/skills/` 与所选平台 `.codex/skills/` 的对应文件；installer manifest/hash 更新按既有机制处理。其他声明平台用相同 canonical projection 定向验证。

预期无 production Python/schema/command/exit/public DTO 变更。若正常 replay 证明必要局部 runtime 修订，必须先具体定位受影响已有 owner、当前入口与 consumer，再通过现有 implementation qualification/Architecture re-entry 和规划修订；本计划不预留通用机制。
不修改身份 substrate、Completion/Closure/Finish、旧 Finalizer 或 pinned-old packages。没有新增兼容读路径或保留 deprecated asset；稳定输入/出口及原 mutation receipt 语义不变。

## Docs SSOT Plan
strategy：`ssot_first`。实现前把局部恢复与执行事实复用条件写入各 owner canonical contract；spec 只保留跨 owner 边界及测试策略，README 只导航，不复制步骤。RDT 增量引用 Issue/AC 与 owner contract，不复制全篇 PRD；Test 层是后续定向结果唯一 locator。
Architecture 判断为 existing-boundary current-conforming refinement：不改变 owner、writer、存储、public I/O、decision、GAP 或兼容退出；Planning 调原 owner 获取 fresh no-impact 结果。若实际修改触发架构边界变化，重新 task_impact_sync 并按 contribution/promotion 合同处理，不能沿旧 no-impact 继续。
共享 RDT promotion 留在既有独立 review/expected-current 串行边界；promotion 产生 committed diff 后仍 fresh Phase2/commit/full review，不能以效率优化跳过。

## 备选与取舍
全局 ValidationReceipt/cache 能强制命中，但新增公共字段、缓存生命周期和跨阶段 authority，违反本 Issue 明确边界，排除。
修改 content identity 来忽略 task metadata 会影响 exact-candidate 与真实 metadata 提交职责，本设计保留算法、由原 owner 重分类刷新当前结果。
总是重跑所有 command 容易执行，但违反依赖级复用验收；总是消费旧 pass 会漏新内容，两者都不采用。当前方案仍完整 semantic review，仅复用原 owner 可证明适用的执行事实。
保留所有历史 checkpoint 会扩大状态；当前方案保留 producer 既有退休规则，缺失结果重跑对应 owner。

## 验证与回滚
implementation 中先用 current schema 临时 Git fixture + 实际 owner 入口观察未修订合同的动作，再用修改后合同执行相同 replay：A-only/B dependency/new C；equivalent/material authority；same HEAD recovery/new HEAD；promotion/finding-fix；base unchanged/evolved；same mutation。外部命令 mock 只证明模块动作次序/次数，不声称 live PR 实效。
semantic 行为必须由 native/current AI owner 读合同判断，post-owner staged pass 只证明结构。用现有 eval carrier/fixture，不能写自动 script reviewer；不新增评分器、完整 transcript 或长期 test ledger。
定向 package/runtime/checker、canonical-installed/platform、apply/reapply/drift、sidecar/mode 验证在本 task 完成；累计安装/Upgrade/Release matrix 不在 scope。
回滚为恢复本次 canonical Markdown/fixture 变更并重新 apply；无业务数据迁移、DB、容器、K8s 或环境配置写入。未发布前只有 task-local工作；已经 commit 后回滚须遵循新的 Git 副作用确认，不改写未知历史。
