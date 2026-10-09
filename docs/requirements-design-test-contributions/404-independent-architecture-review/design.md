# #404 Design 增量

状态：RDT 合同已晋升至 `current-main-0.6.17-guru.78`，实际实现和晋升后 gates 只由唯一 Test 记录。历史来源为 RDT/Architecture `.77`；current 两者均为 `current-main-0.6.17-guru.78` / `active`。设计对象来自已准备的 task design；实际实现与验证状态由唯一 [Test](./test.md) 记录。

| Design | 责任与消费接点 |
| --- | --- |
| D404-01 | 既有 [Architecture Skill](../../../trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/SKILL.md) 与其 [step-local contract](../../../trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/references/contract.md) 独占 reviewer 方法。新评估交给未参与当前候选编写/实现、未预载任务叙事的 fresh worker；调度方提供定位、stage、真实候选和必要 authority/约束来源。 |
| D404-02 | reviewer 依据 current 项目 authority、候选与真实消费者建立职责/default/状态/依赖影响模型，之后才核对必要解释；task design 是设计对象，贡献自述和完成叙事不成为 authority。缺候选或必要约束保留现有 incomplete/blocked 路径。 |
| D404-03 | Planning、两项 qualification、实施协调、Check 与 Branch Review 各原 semantic owner 消费架构事实并判断当前交付责任。必要局部迁移/旧路径退出由本次工作完成；独立历史债务及无关红测仅有限归因，不新增自动修复范围。 |
| D404-04 | 原配置及质量 authority 区分默认、推荐、合法范围和硬不变量。阶段 owner 消费已有合同并保留不确定性，不由测试失败或缺诊断字段发明业务准入条件。 |
| D404-05 | reviewer 自主 author 既有 semantic result 并亲自调用 formal wrapper。Phase2 覆盖完整工作区；Branch Review 新派 fresh worker 覆盖 exact committed range。合规 worker 可在专项完成后加载任务叙事执行整体 Skill；两个 public results 分别消费。 |
| D404-06 | 下游 Architecture owner 依据仍适用的独立判断及 live eligibility 亲自完成 matching-stage publication/acceptance_finish wrapper。主会话不 relabel Branch Review DTO；candidate/适用事实变化回对应 fresh 评估，promotion-created diff 回既有 Phase2/commit/full review。 |
| D404-07 | 现有 eval staging/native adapter 使用真实候选、消费者和最小约束；预期结论只在 grader 侧。移除主会话自填 Architecture 与预载 no-impact 叙事作为独立行为 proof 的旧路径，保留仍有 objective wrapper consumer 的机器验证。 |
| D404-08 | canonical 经现有 preset apply/reapply 同步 installed、Shared 和 descriptor-selected 平台投影，保持 upstream ownership。workflow 只 mandatory invocation 与 routing，平台入口只加载调度，README 导航到唯一 step-local contract。 |

直接演进保持 Architecture 2.0 public I/O、四 profiles、七 exits、promotion owner 与唯一 consumer；无新增 Skill、wrapper、ledger、第三状态机或授权持久化。实际平台 prelude 和 native 行为须验证，改 role 名称或字段校验不证明独立。

`docs_ssot_subtraction` 退役将主会话 authoring/预载叙事作为独立证据的当前说明；immutable 历史贡献、ADR 和发布证据保留为历史，不作为 current runtime 支持路径。RDT 由原 owner 经 `task_impact_sync` / `promotion` 串行收敛；[Architecture contribution](../../architecture/contributions/404-independent-architecture-review.md) 由其原 owner 处理，本增量不写 shared CURRENT。
