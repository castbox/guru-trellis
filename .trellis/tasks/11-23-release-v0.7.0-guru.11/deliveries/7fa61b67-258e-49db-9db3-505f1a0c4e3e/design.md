# D1：v0.7.0-guru.11 完整可分发源设计

## 1. 设计目标、需求承接与内容基线

本批承接 [PRD](prd.md) 的 D1-R1 至 D1-R7、D1-SC1 至 D1-SC5、D1-AC1 至 D1-AC4，以及 [Task PRD](../../prd.md) 的 R1 至 R4、R6 和 AC1 至 AC4。目标是生成可供 D2 消费的完整 `.11` 发布源；真实采用、准备收尾和正式发布由后继 owner 承接。

开发基线 B 为 `2acab7fadebf57c2f2560451b9ff2a050d8811f5`，来源是创建 Task 时固定的 main。Planning H0 同为该提交，只作起点观察。PR 目标是 `main`。实现后的完整 B..H 由原 constructor 构造，后续 main 推进不缩窄本批内容范围。

独立 Architecture candidate assessment 已返回 `baseline_current / no_architecture_impact`。基线 identity 为 `guru-trellis-architecture`，constitution 为 `guru-trellis-design-constitution-v1`，change contract 为 `guru-trellis-architecture-change-contract-v1`。结论理由是：候选仅让私有 release consumer 与已生效的公共 owner graph 对齐，没有新增或改变 owner、状态、兼容路径、架构决定或验证义务。该结论不代替 final_plan、Approval 或 Activation。

## 2. 当前系统、边界与目标差额

### 2.1 版本轴

当前 canonical extension、installed extension 和公开 README 均为 `0.7.0-guru.10`。`guru-upgrade-installation` 的 TARGET_GURU、输出 schema、两个 stop consumer 和 active example 也仍为 `.10`。Fork source lock 与 CLI 已独立固定，不需要随 Guru revision 改写。

目标状态统一为 Guru tag/revision `v0.7.0-guru.11` / `0.7.0-guru.11`，前驱明确为 `v0.7.0-guru.10`，Fork 保持 `e3793251fad8bd261d0c370d408c7675b9f6a140` / `0.7.0-castbox.6`。

### 2.2 当前发布链

当前 workflow 在 Branch Review `passed` 后进入 `guru-publication-entry-router`。该 router 获取发布 Architecture eligibility，再把当前 Review 和资格交给 `guru-publish-task-delivery:delivery_prepare_publication`。Publication 自己完成 readiness、中文 Refs-only PR payload 和精确预览；当前链不再存在 `guru-review-task-delivery`。

仓库私有 release contract 仍要求 `guru-review-task-delivery`，三个平台发现副本与 Shared 私有正文保持一致，因此四份都携带同一处的旧链。私有 tests 也把旧 Skill 和旧 consumer 作为期望。

### 2.3 当前知识

公共 Requirements/Design/Test 的 task-delivery lifecycle 已有 R900/D900/T900，但正文仍保留多处旧的独立 Delivery Review 表述。它们与当前 public registry/workflow 的可执行链不一致。该差额属于现有能力正文的同步，不产生新的公共行为或 Architecture 决定。

### 2.4 不改边界

本批不手工更新 `.trellis/guru-team/extension.json`、`.claude/skills/guru-*`、`.agents/skills/guru-*` 等公共受管 dogfood 投影。D1 只交付 canonical/private source 和来源样本；准备 checkout 的真实采用必须由 D2 通过 `guru-upgrade-tools(source_locked)` 完成。

## 3. 来源设计处置（唯一）

| 来源及原承诺 | 处置 | 具体落点、理由与影响 | 上游处置 |
| --- | --- | --- | --- |
| Issue #908：基于最新 main 准备下一正式版本，最终 candidate 必须在准备合并后重新冻结 | retain | 本批固定 B 只用于 D1；Stage 2 另行读取最新 main，不消费本批 H | 原 release owner |
| release contract / Complete Source Before Actual Adoption：D1 先独立交付完整源，失败不得延后 | retain | 第 4、6、8 节；D1 自己完成来源和消费者验证 | 当前 Contract |
| release contract / D1 delivered → Completion → D2 → source_locked | retain | 第 6、7、8 节；本批不建立 D2 | 原 Completion/Creation/tools owner |
| release contract 中的旧独立 Delivery Review 节点 | change | 第 4.2、5、6 节；改为 Branch Review → publication Architecture eligibility → Publication readiness，不复制 Publication 内部事务 | 当前 workflow、`guru-publish-task-delivery` contract |
| Public registry/workflow 的 `guru-publish-task-delivery` readiness owner | retain | 第 4.2、5 节；私有合同和回归消费实际 Interface | 当前 public owner |
| 当前版本 producer/consumer 的 `.10` 值 | change | 第 4.1 节成套更新为 `.11`，保持现有 shape 和来源家族 | 原 upgrade owner |
| 三份 README 的当前版本与安装条件 | change | 第 4.3 节更新 `.11`、前驱 `.10` 和 Release 存在条件，不宣称未发布版本已稳定 | 原 docs writer |
| Task/Delivery lifecycle 中独立 Delivery Review 的旧正文 | change | 改为当前 R900 的 Publication readiness 表述；历史专项结果保持历史身份 | 原 RDT owner |
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

- Stage 1 的发布责任流由 `guru-review-branch -> guru-review-task-delivery -> guru-publish-task-delivery` 改为 `guru-review-branch -> publication Architecture eligibility -> guru-publish-task-delivery readiness/preparation`。
- Publication 负责准确预览、确认后执行和同事务恢复；Contract 只链接该 owner，不复制 profile、schema 或状态机。
- `guru-publish-task-delivery` 后的 `ready_for_merge` 才进入原 Merge owner。
- D1/D2 顺序、Completion、reference-only Closure、Finish、Stage 2 和逐项确认边界保持不变。

Shared tests 从当前 Interface/workflow 取实际 consumer。需要移除的旧期望包括 `guru-review-task-delivery` Interface 和 public `ready` 链；需要增加 `guru-review-branch:passed -> guru-publication-entry-router`，并继续验证 `guru-publish-task-delivery:ready_for_merge -> guru-merge-task-delivery` 等当前链。测试仍通过实际 Interface/workflow 读取图，不以固定文本自证。

私有 Skill 继续只存在于 `.agents`、`.codex`、`.claude`、`.cursor` 的项目发现路径，不进入 public registry、preset、marketplace 或 manifest。

### 4.3 公开说明

- 根 README：当前 canonical target 改为 `.11`，前驱改为 `.10`，安装示例的 `GURU_REF` 改为 `v0.7.0-guru.11`；只有对应正式 Release 存在时才执行。
- workflow README：更新当前 revision、`gh:castbox/guru-trellis/trellis#v0.7.0-guru.11` 示例和 `.10` 前驱。
- preset README：更新 canonical maintenance target、marketplace 示例和前驱。

三份文档保持各自职责，不复制私有发布流程。`.9` 和更早版本继续作为历史来源，不做全局替换。

### 4.4 当前知识维护

原 RDT owner 为 `docs/{requirements,design,test}/current/task-delivery-lifecycle.md` 准备 task-local delta，将仍描述独立 Delivery Review 的现行句子改为 `Publication` readiness 和当前 `guru-publish-task-delivery` owner，并沿用已有的 R900/D900/T900 身份。历史专项文档和版本化贡献不重写。

本批在 TaskCommit 前由原 RDT owner 执行 final integration/readback，实际 current 正文进入 committed candidate，再由独立 Review 审核真实 after。Architecture candidate 已判断 `no_architecture_impact`，本批不创建 Architecture contribution、ADR 或 project-check burden。

## 5. 接口与数据

没有新增 public Skill、profile、schema id、typed exit、配置键、持久字段或状态。

- upgrade producer 保持现有 CLI/public wrapper 与 result shape，仅改变当前目标 revision 常量及其直接 schema/example。
- Branch Review 的 `passed` 输出保持现有 `guru-publication-entry-router` consumer。
- Publication 继续使用既有 prepare/execute profile、preview 和 recovery；私有合同只引用。
- D1 delivered source 的最小 handoff 是实际 commit/tree 与 Delivery result，由原完成和 tools owner 读取。

## 6. 状态、顺序、正常与失败流程

1. 完成本批 PRD/design/implement 和官方 context；独立 final Architecture 返回 current，Approval 通过，Activation 写入公共 Planning acceptance。
2. 实施版本消费者、私有合同四份、RDT delta、private tests 和三份 README；执行定向 package/private/docs 检查。
3. 运行 source validator 和声明平台根检查。用当前完整 after 建立来源样本，执行 focused Codex 安装/update/reapply，再在同一项目补齐 Claude、Codex、Cursor apply、installed validation 和完整投影核对。
4. 原 RDT owner 将已审 delta final-integrate/readback 到 current units；Architecture 无变化，无新 contribution/ADR。
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
| D1-V5 | D1-R6、D1-AC4 | 原 RDT owner 对 lifecycle R/D/T delta 做 final integration/readback；原 Architecture owner 消费 no-impact 结论 | 文档字节一致不代替独立 Review |
| D1-V6 | D1-R7、D1-AC4 | 实际 TaskCommit、constructor/begin_check、一次独立完整 Review、Publication、expected-head Merge | 只有真实 delivered 才允许 D2 |

执行顺序先便宜静态/定向回归，再完整来源样本，最后完整交付门禁。真实 Agent 的 Planning 和 Review 判断不进入确定性脚本结果；若来源样本限制导致某层不能验证，保留准确缺口，不写为通过。

## 9. Canonical 引用、本轮差额与实际未决项

- Requirements：`docs/requirements/current/task-delivery-lifecycle.md` 中 R531/R636/R637/R794/R900 相关职责。
- Design：`docs/design/current/task-delivery-lifecycle.md` 中 D531/D636/D637/D794/D900 相关职责。
- Test：`docs/test/current/task-delivery-lifecycle.md` 中 T531/T636/T637/T794/T900 相关场景。
- Distribution：`docs/requirements/current/codex-skill-distribution.md`、`docs/design/current/codex-skill-distribution.md` 和 `docs/test/current/codex-skill-distribution.md` 的 R724/D724/T724。
- Architecture：`docs/architecture/04-integrations/distribution.md` 的 `ARCH-INT-009`、`ARCH-INT-015` 已承接私有发布编排和 D1/D2；candidate 判断为 no impact。

Docs SSOT 策略和原 writer/consumer 在 implement 第 6 节唯一展开。当前 planning 没有阻塞产品选择。final_plan、Approval、Activation、实际工程结果和正式交付尚未完成，不预填通过。
