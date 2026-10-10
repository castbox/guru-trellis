# #382 Phase 2 Architecture contribution candidate

状态：draft / 未晋升。TaskId：382-root-cause-qualification / generation 0；身份：382-root-cause-qualification:phase2-v1。本文是当前实现candidate的change contract，不预填独立评估结论。

## Authority 与对象

requirement authority：https://github.com/castbox/guru-trellis/issues/382（2026-10-10-r1）；共同完成owner边界：https://github.com/castbox/guru-trellis/issues/383（2026-10-10-r9）。设计对象：.trellis/tasks/10-10-382-root-cause-qualification/design.md。

Guru：guru-maintain-architecture-baseline:2.0；baseline：docs/architecture/README.md / current-main-0.6.17-guru.78 / active；expected current：同一 .78。
constitution：docs/architecture/00-foundation/design-constitution.md / guru-trellis-design-constitution-v1 / current；project contract：docs/architecture/06-governance/change-contract.md / guru-trellis-architecture-change-contract-v1；concern set：guru-trellis-architecture-change-concerns-v1。

候选path为target_native：新增独立根因准入owner，复用现有dispatcher、qualification facts与stage owners，无legacy root authority/adapter/双读写。最终impact/path由独立assessment选择。既有ADR-005、ADR-009和ARCH-GOV-006..009约束authority与promotion；ARCH-GAP-006/008是descriptor引用的继承证据，不改变生命周期。

## 九concerns候选适用性

| Concern | Applicability | 设计事实 |
| --- | --- | --- |
| authority-binding | applicable | 新包及caller绑定Guru 2.0、current baseline、change-contract与r1 live scope，任务不自封CURRENT。 |
| constitution-binding | applicable | 当前owner分层、最小public I/O、直接consumer和无持久缓存有必要性来源；只引用identity，不复制原则。 |
| boundary-and-decision | applicable | 当前两资格owner保持；root owner新增目标感知候选判断，#383/当前stage独占完成；ADR候选记录新增governance决定。 |
| owner-and-single-writer | applicable | AI root独占认知，runtime只校事实；原stage独占stage review；task checkout单写candidate，共享晋升只有原owner。 |
| compatibility-and-exit | applicable | 新skill/schema/router API直接新增，旧normal/solution API不变；受控caller同步迁移，零旧root路径与dual-read。 |
| gap-and-deviation | applicable | 计划补现有因果候选缺口，未实现不称closed；保留无关历史GAP，实际新增偏移由stage owner返回。 |
| parallel-scope | applicable | 允许task-isolated新包/caller/tests/docs contribution；禁止并行写shared current、accepted ADR、既有GAP/constitution、其它task/业务/生产。 |
| evidence-and-freshness | applicable | 当前Phase2对象为完整tracked/untracked worktree；Branch Review后续用exact committed range。实际native、wrapper、分发和只读历史回放执行结果由Test唯一来源承载。 |
| review-and-promotion | applicable | 当前贡献与ADR先由独立owner评估；实现贡献独立committed review后原owner按expected current晋升，晋升diff重跑freshgates。 |

## Before / candidate after

Before：normal owner证明场景、solution owner证明authority，caller缺独立root cause/counterfactual/symptom redistribution认知；无rootqualification包，无共同causal completion SSOT。
Candidate after：新owner按诊断/缓解/修复/保护实际目标做候选准入，four exits路由到现有ten-profile owners；unknown diagnosis继续、unknown合格缓解诚实交付，未证明root fix返诊断。stage变更不重复同资格；实质机制变化回owner，qualification结果不代completion。
candidate承接：本任务根因候选认知缺口（不以候选充当CURRENT/closed）；retained：#383共同完成语义待其owner交付，当前完成owner维持，完整Release/生产效果不在本任务；new：无计划新增authority或compatibility debt，实际结果由stage检查。

## Writer、兼容、删除与职责

task writer：382 dedicated checkout写candidate；shared current writer：既有Architecture/RDT promotion owner。准入正文属于新Skill，workflow只显式invoke/router；spec、README、RDT/Architecture仅拥有各自引用/事实，不复制完整认知。
无长期兼容例外。现有两资格包的真实caller继续消费已发布API；新能力在受控caller同步加载，不让旧路径充当root资格。任何任务新引入的重复cognition、缓存或completion规则在同task移除。current同步与所有安装投影验证后退出旧caller文案，不新增第二版本root runtime。

## Project-check、ADR与promotion接点

descriptor：guru-trellis-architecture-convergence:repository:1；check：guru-trellis-architecture-convergence@1；entrypoint：docs/architecture/06-governance/change-contract.md；result contract：guru-project-architecture-check-result-2.0。独立Architecture owner亲自执行协议并author result；本文不填check status。

ADR candidate locator：.trellis/tasks/10-10-382-root-cause-qualification/architecture-adr-candidate.md；候选理由：新增唯一根因qualification governance owner与接续边界，改变当前semantic decision graph；独立owner评required。当前实现位于trellis/skills/guru-team/packages/guru-qualify-root-cause/，caller/workflow/独立consumer schemas已接入。共享qualification_facts只提取Git/planning/路径事实，installer inventory机械拆出；两个既有qualification API不变。实际wrapper、native、分发、代表性安装/update/reapply与业务只读回放的唯一结果来源为docs/requirements-design-test-contributions/382-root-cause-qualification/test.md；业务native安装/生产效果与remote候选安装尚未验证。
committed review：尚未形成；promotion：尚未晋升，expected current为 .78，advance返回sync_required重读，不覆盖。后续独立committed full-diff review、expected-current晋升与promotion-created freshgates分别执行，不由Planning推定。
