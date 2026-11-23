# D1：v0.7.0-guru.11 完整可分发源设计

## 1. 设计目标、需求承接与内容基线

本批承接 [PRD](prd.md) 的 D1-R1 至 D1-R7、D1-SC1 至 D1-SC5、D1-AC1 至 D1-AC4，以及 [Task PRD](../../prd.md) 的 R1 至 R4、R6 和 AC1 至 AC4。目标是生成可供 D2 消费的完整 `.11` 发布源；真实采用、准备收尾和正式发布由后继 owner 承接。

开发基线 B 为 `2acab7fadebf57c2f2560451b9ff2a050d8811f5`，来源是创建 Task 时固定的 main。Planning H0 同为该提交，只作起点观察。PR 目标是 `main`。实现后的完整 B..H 由原 constructor 构造，后续 main 推进不缩窄本批内容范围。

原 candidate assessment 的 `baseline_current / no_architecture_impact` 因遗漏 current consumers 已失效。修复后的独立 candidate assessment 现正式返回 `baseline_current / architecture_impact`，change path 为 `target_native`，decision refs 为 `ADR-POSTCOMMIT-INDEPENDENT-REVIEW`、`ADR-024`、`ADR-034`。基线 identity 为 `guru-trellis-architecture`，constitution 为 `guru-trellis-design-constitution-v1`，change contract 为 `guru-trellis-architecture-change-contract-v1`。该结论允许进入 solution planning，但不代替 final_plan、Approval、Activation 或后续 committed Review。

## 2. 当前系统、边界与目标差额

### 2.1 版本轴

当前 canonical extension、installed extension 和公开 README 均为 `0.7.0-guru.10`。`guru-upgrade-installation` 的 TARGET_GURU、输出 schema、两个 stop consumer 和 active example 也仍为 `.10`。Fork source lock 与 CLI 已独立固定，不需要随 Guru revision 改写。

目标状态统一为 Guru tag/revision `v0.7.0-guru.11` / `0.7.0-guru.11`，前驱明确为 `v0.7.0-guru.10`，Fork 保持 `e3793251fad8bd261d0c370d408c7675b9f6a140` / `0.7.0-castbox.6`。

### 2.2 当前发布链

当前 workflow 在 Branch Review `passed` 后进入 `guru-publication-entry-router`。该 router 获取发布 Architecture eligibility，再把当前 Review 和资格交给 `guru-publish-task-delivery:delivery_prepare_publication`。Publication 自己完成 readiness、中文 Refs-only PR payload 和精确预览；当前链不再存在 `guru-review-task-delivery`。

仓库私有 release contract 的 Stage 1 已指向当前 publication entry/readiness，但 Stage 2 的“丢弃 Delivery Review result”和 Reviewed-Content Freshness 的阶段清单仍沿用已退役名称；三个平台发现副本与 Shared 私有正文保持一致。私有 tests 已从当前 Interface/workflow 读取 owner/consumer，并明确断言 retired Skill 不进入当前 registry/workflow。

### 2.3 当前知识

公共 Requirements/Design/Test 已有 R900/D900/T900，但 `knowledge-maintenance.md`、`completion-closure.md`、lifecycle 正文、`T669-06` 和 `runtime-location#813` 仍保留旧的独立 Delivery Review 表述。Architecture 的 `ARCH-CUR-051`、`ARCH-DOM-036`、`ARCH-DOM-055`、`ARCH-DOM-059`、`ARCH-INT-015`、`ARCH-INT-020` 和 `ARCH-GOV-009` 也仍把独立 Delivery Review 声明为 current owner、payload 或 current gate。它们与当前 public registry/workflow 的可执行链不一致。修复必须由原 RDT/Architecture owners 在各自当前正文中同步；历史 contribution、roadmap 和已发布事实不追溯改写。

`docs/architecture/adr/postcommit-independent-review.md` 仍标记为 `proposed` 并声明不能作为 shared current，但多份 current Architecture/RDT 正文已经把它承载的一次独立 Review、Publication readiness 和审核前禁止 push/PR 顺序作为当前依据。这个 decision-authority 状态必须由原 Architecture owner 明确收敛，不能继续保留“当前依赖 proposed”的双重语义。

### 2.4 不改边界

本批不手工更新 `.trellis/guru-team/extension.json`、`.claude/skills/guru-*`、`.agents/skills/guru-*` 等公共受管 dogfood 投影。D1 只交付 canonical/private source 和来源样本；准备 checkout 的真实采用必须由 D2 通过 `guru-upgrade-tools(source_locked)` 完成。

## 3. 来源设计处置（唯一）

| 来源及原承诺 | 处置 | 具体落点、理由与影响 | 上游处置 |
| --- | --- | --- | --- |
| Issue #908：基于最新 main 准备下一正式版本，最终 candidate 必须在准备合并后重新冻结 | retain | 本批固定 B 只用于 D1；Stage 2 另行读取最新 main，不消费本批 H | 原 release owner |
| release contract / Complete Source Before Actual Adoption：D1 先独立交付完整源，失败不得延后 | retain | 第 4、6、8 节；D1 自己完成来源和消费者验证 | 当前 Contract |
| release contract / D1 delivered → Completion → D2 → source_locked | retain | 第 6、7、8 节；本批不建立 D2 | 原 Completion/Creation/tools owner |
| release contract 中 Stage 2 与 freshness 描述仍使用旧 Delivery Review result | change | 第 4.2、5、6 节；改为当前 Review 后的 Publication readiness/result，不复制 Publication 内部事务 | 当前 workflow、`guru-publish-task-delivery` contract |
| Public registry/workflow 的 `guru-publish-task-delivery` readiness owner | retain | 第 4.2、5 节；私有合同和回归消费实际 Interface | 当前 public owner |
| 当前版本 producer/consumer 的 `.10` 值 | change | 第 4.1 节成套更新为 `.11`，保持现有 shape 和来源家族 | 原 upgrade owner |
| 三份 README 的当前版本与安装条件 | change | 第 4.3 节更新 `.11`、前驱 `.10` 和 Release 存在条件，不宣称未发布版本已稳定 | 原 docs writer |
| `ARCH-CUR-051`、`ARCH-DOM-036`、`ARCH-DOM-055`、`ARCH-DOM-059`、`ARCH-INT-015`、`ARCH-INT-020`、`ARCH-GOV-009` 中把独立 Delivery Review 写成 current owner/payload/gate 的正文 | change | 第 4.5 节；改为当前 Review 后由 `guru-publish-task-delivery` 承接 readiness 与发布；旧 #435 阶段结果和相关 evidence 保持历史身份 | 原 Architecture owner |
| `ADR-POSTCOMMIT-INDEPENDENT-REVIEW` 的 `proposed` 状态、决定 4 的旧 Delivery Review 片段和 current consumers 之间的矛盾 | change | 第 4.5 节；修正决定 4 后晋升为 accepted/current，保留 #794 原 Task attribution、其他决定、证据和替代范围；完整复核其 current consumers | 原 Architecture owner |
| `docs/{requirements,design}/current/knowledge-maintenance.md`、`completion-closure.md` 与对应 Test current 单元中独立 Delivery Review 的旧正文 | change | 第 4.4 节；改为当前 R900 的 Publication readiness 表述；历史专项结果保持历史身份 | 原 RDT owner |
| D1/D2 顺序与 source_locked 采用边界 | retain | 第 6、7 节和唯一 Policy；准备 checkout 不在本批采用 | 当前 Architecture 与 tools owner |
| Stage 2 的 latest-main freeze、tag、smoke、Release、本地收敛 | retain | 第 7 节和后续责任；本批不执行 | 原 release owner |

## 4. 模块、职责与设计取舍

### 4.1 版本生产者与消费者

实施 owner 在 canonical source 中更新以下当前版本入口：

- `trellis/guru-team-extension.json` 的 `version`；
- `trellis/skills/guru-team/packages/guru-upgrade-installation/runtime/owner.py` 的 `TARGET_GURU`；
- 该包 `schemas/public-upgraded-output.schema.json`；
- 该包 `consumers/stop/production/upgrade-installation-upgraded.schema.json`；
- shared `trellis/skills/guru-team/consumers/stop/production/upgrade-installation-upgraded.schema.json`；
- 该包 active example `examples/public-upgraded-output.json`。

实际 producer 继续生成现有 upgraded result；所有 schema/active example 和 stop consumer 随同一 revision 演进。没有新增版本字段、双读、兼容 adapter 或第二 authority。历史 schema 和 fixture 保持原字节。

### 4.2 仓库私有发布消费者

Shared `.agents/skills/release-guru-trellis-version/references/contract.md` 和 `.codex`、`.claude`、`.cursor` 三份发现副本按字节一致修改：

- Stage 1 的发布责任流保持 `guru-review-branch -> publication Architecture eligibility -> guru-publish-task-delivery readiness/preparation`。
- Stage 2 不再声称丢弃不存在的“Delivery Review result”；改为丢弃 Preparation readiness/Publication result 等真实阶段事实。
- Reviewed-Content Freshness 的阶段清单改为当前 Phase 2、Branch Review、Publication readiness/execute、Merge、Completion 和 Finish，不再把 Delivery Review 写成 current stage。
- Publication 负责准确预览、确认后执行和同事务恢复；Contract 只链接该 owner，不复制 profile、schema 或状态机。
- `guru-publish-task-delivery` 后的 `ready_for_merge` 才进入原 Merge owner。
- D1/D2 顺序、Completion、reference-only Closure、Finish、Stage 2 和逐项确认边界保持不变。

Shared tests 从当前 Interface/workflow 取实际 consumer，验证 `guru-review-branch:passed -> guru-publication-entry-router`、Publication readiness/prepare/execute 和 `ready_for_merge -> guru-merge-task-delivery`，并明确断言 retired `guru-review-task-delivery` 不进入当前 registry/workflow。测试仍通过实际 Interface/workflow 读取图，不以固定文本自证。

私有 Skill 继续只存在于 `.agents`、`.codex`、`.claude`、`.cursor` 的项目发现路径，不进入 public registry、preset、marketplace 或 manifest。

### 4.3 公开说明

- 根 README：当前 canonical target 改为 `.11`，前驱改为 `.10`，安装示例的 `GURU_REF` 改为 `v0.7.0-guru.11`；只有对应正式 Release 存在时才执行。
- workflow README：更新当前 revision、`gh:castbox/guru-trellis/trellis#v0.7.0-guru.11` 示例和 `.10` 前驱。
- preset README：更新 canonical maintenance target、marketplace 示例和前驱。

三份文档保持各自职责，不复制私有发布流程。`.9` 和更早版本继续作为历史来源，不做全局替换。

### 4.4 当前知识维护

原 RDT owner 为 `docs/{requirements,design,test}/current/task-delivery-lifecycle.md`、`docs/{requirements,design}/current/knowledge-maintenance.md`、`docs/{requirements,design}/current/completion-closure.md`、`docs/test/current/completion-closure.md` 的 `T669-06` 和 `docs/test/current/runtime-location.md#813` 准备 task-local delta，将仍描述独立 Delivery Review 为 current owner/gate 的现行句子改为 `Publication` readiness 和当前 `guru-publish-task-delivery` owner，并沿用已有的稳定身份。历史专项结果和版本化贡献不重写。

本批在 TaskCommit 前由原 RDT owner 执行 final integration/readback，实际 current 正文进入 committed candidate，再由独立 Review 审核真实 after。Architecture contribution 按已通过的 `architecture_impact / target_native` 结论建立；final_plan 仍须重新评估完整 design、实际 contribution 和 ADR promotion，不能复用 candidate_assessment 作为最终通过。

### 4.5 当前 Architecture 同步

原 Architecture owner 在本批 task-local Architecture contribution 与必要 proposed targets 中同步以下当前单元：

- `ARCH-CUR-051` 删除“Delivery Review/readiness和终态不变”中的旧 owner 名称；保留 Planning、原维护单写、终态职责和 postcommit review 范围。
- `ARCH-DOM-036` 将“Delivery Review 审 payload、Publish 执行”改为“Publication readiness 审 payload 与剩余责任、Publish 执行”；保留 causal/Completion/Closure/Finish 责任。
- `ARCH-DOM-055` 将当前阶段列表中的 Delivery Review 改为 Publication readiness；保留 #154 原 Author/发现/来源/范围/规划职责与历史来源。
- `ARCH-DOM-059` 将当前 owner 列表中的 Delivery Review 改为 Publication readiness；`#637` 原 Architecture/Check/TaskCommit/Branch Review 覆盖、后继审查与 final decision 语义保持。
- `ARCH-INT-015` 将 repository-private release chain 的 `Delivery Review readiness` 改为 `Publication readiness`；保留 TaskCommit、固定 B..H、一次完整 Review、Merge 和 Completion 顺序。
- `ARCH-INT-020` 把旧 Delivery Review payload 投影改述为“Review 后的 Publication readiness/result 交给 Publish”；保留 `#900` 当前边、受控 Merge trailer 与 deferred 历史事实。
- `ARCH-GOV-009` 说明 Branch Review 通过后由 `guru-publish-task-delivery` 同时判断 readiness、真实 PR payload 和剩余责任，再执行独立确认后的 publication；保留 Publish/Merge/Completion/Closure/Finish/Cleanup 责任。

`ADR-POSTCOMMIT-INDEPENDENT-REVIEW` 采用明确晋升路径，不保持 proposed：

- 保留 #794 原 Task/Delivery attribution、问题、决策 1–3、5–6、证据、窄替代和重评边界。
- 把决定 4 中已退役的“Delivery Review 完成并记录 readiness、Publication 只消费 ready”改为当前“完整 Review 通过后由 `guru-publish-task-delivery` 完成 readiness、payload 和精确预览，独立确认后执行发布”；审核前不 push/不创建 PR 的当前顺序保持。明确来源为 R900/D900 与 #900 的后续窄替代，不把 Publication readiness 冒充 #794 原决定；#794 原文以历史/替代边界保留可追溯。
- 同步修正 ADR“窄替代与保持”中“Planning candidate/final、Delivery Review、Publication、Completion、Closure、Finish保持各自责任”旧句，改为 Planning candidate/final、Publication readiness/execute、Completion、Closure、Finish 的当前责任；其他 ADR-028/034/033 等保持范围逐项保留。
- 把“验证与重评”中“当前只有候选方案，无实现或发布 pass”改为带明确观察截止的 #794 历史事实，后续当前结果由 R900/D900、实际 committed Review、Publication 和 Release 原结果承接，不在 ADR 自写完成或最终 pass。
- 从 `proposed` 收敛为 shared Architecture ADR 的 accepted/current 状态，删除“不能作为 current authority”的自述，同时保留其历史 Task 来源。
- 原 Architecture owner实际写入、读回并检查 current applicability；该写入进入 `integrated_pending_review`，只有提交后同次独立完整 Review 才能确认 reviewed_promoted。

该 ADR 的完整 current consumers 为：`docs/architecture/README.md`、`docs/architecture/01-current/system.md`、`docs/architecture/03-domains/ownership.md`、`docs/architecture/03-domains/workflow-context.md`、`docs/architecture/04-integrations/distribution.md`、`docs/architecture/06-governance/change-contract.md`、`docs/architecture/06-governance/rules.md`、`docs/requirements/current/knowledge-maintenance.md`、`docs/design/current/knowledge-maintenance.md`、`docs/design/current/task-delivery-lifecycle.md` 和 `docs/test/current/knowledge-maintenance.md`。原 Architecture/RDT owners 必须完整读取这些消费者的实际语句；存在旧阶段或 proposed 自述的更新，纯引用消费者在 promotion 后复核仍准确即可。`ARCH-GOV-008`、`ARCH-CUR-070`、`ARCH-DOM-053` 和 `docs/architecture/04-integrations/distribution.md` 的 proposed-status 说明必须与晋升后的 ADR 一致。

历史 `ARCH-CUR-032`、旧 #435 阶段描述、contribution、roadmap 和 evidence 中保留历史专项结果的身份保持原样。本批 Architecture contribution 位于 `docs/architecture/contributions/908-release-v0.7.0-guru.11.md`，完整说明七个 current units、ADR promotion 和 11 个 consumer。最终 promotion 仍只由原 Architecture owner 在 final integration 写入/readback，并由 committed Review 判断。

## 5. 接口与数据

没有新增 public Skill、profile、schema id、typed exit、配置键、持久字段或状态。

- upgrade producer 保持现有 CLI/public wrapper 与 result shape，仅改变当前目标 revision 常量及其直接 schema/example。
- Branch Review 的 `passed` 输出保持现有 `guru-publication-entry-router` consumer。
- Publication 继续使用既有 prepare/execute profile、preview 和 recovery；私有合同只引用。
- D1 delivered source 的最小 handoff 是实际 commit/tree 与 Delivery result，由原完成和 tools owner 读取。

## 6. 状态、顺序、正常与失败流程

1. 完成本批 PRD/design/implement 和官方 context；独立 final Architecture 返回 current，Approval 通过，Activation 写入公共 Planning acceptance。
2. 实施版本消费者、私有合同四份、RDT delta、private tests 和三份 README；执行定向 package/private/docs 检查。
3. 原 Architecture/RDT owners 按 fresh candidate/final-plan 的承接准备 task-local contribution 或 direct delta 与完整 proposed targets；提交前在各自合法边界 final-integrate/readback，状态只能为 current 或 integrated_pending_review，不能预填 reviewed。
4. 运行 source validator 和声明平台根检查。用当前完整 after 建立来源样本，执行 focused Codex 安装/update/reapply，再在同一项目补齐 Claude、Codex、Cursor apply、installed validation 和完整投影核对。
5. TaskCommit 形成精确本地提交；原 constructor/begin_check 固定完整 B..H。新独立 reviewer 同次完成 Architecture before/after、九维 Check 和完整 Branch Review。
6. 通过后由 publication Architecture eligibility、Publication readiness、精确预览确认、推流/PR、expected-head Merge 完成 D1 Delivery。只有实际 delivered 才交整体 Completion。

版本 consumer 不一致、私有合同与 registry/workflow 不一致、required source validation、来源样本或知识 readback 失败时，停在本批实现/写作 owner。不得手改样本、放宽测试或把失败留给 D2。输出丢失通过原 owner 的同操作恢复继续。

## 7. 恢复、兼容、迁移与集成

本批没有业务数据、Task schema 或运行状态迁移。旧生产 Skill 的 schema/fixture 保持历史可读；当前 Interface 不恢复旧双读。私有 release Skill 的四份副本在正常源/平台变更中手工同步，并继续排除公共分发。

准备 checkout 暂时保留旧 installed extension/source 是刻意限制。原因是 D1 尚无已交付完整干净源；解除条件是 D1 实际 delivered。解除后原 Completion 返回 `additional_delivery_required`，原 Creation 建立 D2；D2 从真实 delivered source 执行 `source_locked`，不得用本批 dirty source 或来源样本代替。

同范围输出丢失采用各原 owner 的恢复合同，不创建第二 Task/Delivery/commit/PR。真实 source、scope、机制或验收变化分别回到 Clarify、Architecture 或 Author。

## 8. 验证设计

| 验证 | 对应要求/场景 | 入口与独立观察 | 证明限制 |
| --- | --- | --- | --- |
| D1-V1 | D1-R1、D1-AC1 | 运行 `guru-upgrade-installation` 中现有 upgraded producer/consumer/dirty-source 回归；实际输出通过 canonical、package、shared consumer 和 active example | 模块合同，不证明真实业务安装 |
| D1-V2 | D1-R3、D1-R4、D1-AC2/AC3 | 运行 Shared private `tests/test_contract.py`；核对四份字节、当前 registry/workflow Interface、map 和私有排除分发 | fixture 不证明真实独立 AI 判断或远端发布 |
| D1-V3 | D1-R5、D1-AC3 | source validator；声明 Shared/Codex/Claude/Cursor root 检查；一个 focused Codex 来源样本及同项目三平台 apply、own installed validator、完整 bytes/mode、manifest/workflow/lock/sidecar | `local_sample`，不是准备 checkout 的正式采用、前驱升级或完整矩阵 |
| D1-V4 | D1-R2、D1-AC2 | 完整阅读三份 README 改变章节；核对 `.11`/`.10`、Release 条件、同源 ref、命令和 anchors | 文档检查和 `git diff --check` 不证明 Release |
| D1-V5 | D1-R6、D1-AC4 | 原 Architecture owner 对七个命中 current 单元和 `ADR-POSTCOMMIT-INDEPENDENT-REVIEW` 做 contribution、promotion、final integration/readback，并复核其 11 个 current consumers；原 RDT owner 对 lifecycle 三层、Requirements/Design `knowledge-maintenance.md`、Requirements/Design/Test `completion-closure.md` 和 Test `runtime-location.md#813` 做 final integration/readback；以实际 reading 和语义搜索确认 current 正文不再把旧 Delivery Review 写成 owner，ADR 不再 proposed，fresh Architecture 结果由独立 Review 消费 | 文档字节一致、proposed/current 相等、字符串扫描或旧 no-impact 结论不代替独立 Review |
| D1-V6 | D1-R7、D1-AC4 | 实际 TaskCommit、constructor/begin_check、一次独立完整 Review、Publication、expected-head Merge | 只有真实 delivered 才允许 D2 |

执行顺序先便宜静态/定向回归，再完整来源样本，最后完整交付门禁。真实 Agent 的 Planning 和 Review 判断不进入确定性脚本结果；若来源样本限制导致某层不能验证，保留准确缺口，不写为通过。

## 9. Canonical 引用、本轮差额与实际未决项

- Requirements：`docs/requirements/current/task-delivery-lifecycle.md` 中 R531/R636/R637/R794/R900 相关职责，以及 `knowledge-maintenance.md`、`completion-closure.md` 的当前阶段读取与 Delivery 维度职责。
- Design：`docs/design/current/task-delivery-lifecycle.md` 中 D531/D636/D637/D794/D900 相关职责，以及 `knowledge-maintenance.md`、`completion-closure.md` 的当前 Review/Completion 承接。
- Test：`docs/test/current/task-delivery-lifecycle.md` 中 T531/T636/T637/T794/T900、`docs/test/current/completion-closure.md` 的 `T669-06`、`docs/test/current/runtime-location.md#813` 的当前阶段观察，以及 `docs/test/current/knowledge-maintenance.md` 对更新后 ADR 的引用。
- Distribution：`docs/requirements/current/codex-skill-distribution.md`、`docs/design/current/codex-skill-distribution.md` 和 `docs/test/current/codex-skill-distribution.md` 的 R724/D724/T724。
- Architecture：`docs/architecture/01-current/system.md` 的 `ARCH-CUR-051`/`ARCH-CUR-070`、`03-domains/ownership.md` 的 `ARCH-DOM-036`/`ARCH-DOM-053`/`ARCH-DOM-055`/`ARCH-DOM-059`、`03-domains/workflow-context.md`、`04-integrations/distribution.md` 的 `ARCH-INT-015`/`ARCH-INT-020`、`06-governance/rules.md` 的 `ARCH-GOV-008/009` 和 `06-governance/change-contract.md` 都必须与当前 Publication readiness owner 和晋升后的 ADR 一致。`ADR-POSTCOMMIT-INDEPENDENT-REVIEW` 是 decision authority；`ARCH-INT-009` 继续承接私有发布组合和 D1/D2。新的 impact/path 由 fresh candidate assessment 决定。

Docs SSOT 策略和原 writer/consumer 在 implement 第 6 节唯一展开。当前 planning 没有阻塞产品选择；冲突只涉及当前 Knowledge/Architecture 与真实 owner graph 不一致。fresh candidate、final_plan、Approval、Activation、实际工程结果和正式交付尚未完成，不预填通过。
