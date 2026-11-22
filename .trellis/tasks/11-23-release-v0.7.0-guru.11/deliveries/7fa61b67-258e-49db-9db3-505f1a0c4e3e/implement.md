# D1：v0.7.0-guru.11 完整可分发源实施与验证计划

## 1. 输入与引用

TaskId 为 `release-v0.7.0-guru.11` / generation 0；DeliveryId 为 `7fa61b67-258e-49db-9db3-505f1a0c4e3e`。整体范围见 [Task PRD](../../prd.md)，本批需求见 [PRD](prd.md)，唯一来源设计处置见 [design §3](design.md#3-来源设计处置唯一)。没有前序 Delivery；B 和 PR 目标见 design §1。

实施前实际加载：

- design §1 至 §9、PRD 第 1 至 §7；
- `.agents/skills/release-guru-trellis-version/references/contract.md` 的 Stage 1、Complete Source Before Actual Adoption、Whole Preparation Completion、Stage 2 和 Independent Mutation Confirmations；
- `.trellis/workflow.md` 的 Phase 1 至 Phase 3；
- `.trellis/spec/workflow/quality-guidelines.md` 的 Test And Validation Value 和 Validation Scope Ownership；
- `.trellis/spec/docs/public-docs.md`；
- 当前 `guru-publish-task-delivery` Interface 与 contract；
- 当前 RDT lifecycle 三份完整单元、Requirements/Design `knowledge-maintenance.md`、Requirements/Design/Test `completion-closure.md`、Test `runtime-location.md` 与 `current-knowledge.md`；
- 当前 Architecture Baseline、constitution、change contract，以及命中冲突的 `ARCH-CUR-051`、`ARCH-DOM-036`、`ARCH-DOM-055`、`ARCH-DOM-059`、`ARCH-INT-015`、`ARCH-INT-020`、`ARCH-GOV-009` 和 `ADR-POSTCOMMIT-INDEPENDENT-REVIEW`；
- Trellis 官方 index、custom workflow 和 custom spec template marketplace 页面。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置和 owner | 实际文件、动作、完成观察与后继 |
| --- | --- | --- |
| S1 完成规划 | Architecture candidate current；原 Author | 完成 PRD/design/implement、唯一 Policy/Docs Plan 和官方 context；执行独立 Architecture final_plan，随后 Approval/Activation |
| S2 更新版本生产者与消费者 | Activation；原 upgrade/docs owner | 更新 design §4.1 所列六类文件到 `.11`；保持 Fork/CLI 与输出 shape；D1-V1 观察实际 producer→consumer |
| S3 更新公开说明 | S2；原 docs writer | 更新根、workflow、preset README 的 `.11`、`.10` 前驱和 Release 条件；历史版本保留；D1-V4 完整读回 |
| S4 迁移私有发布链 | S2；原 private release writer | 修改 Shared release contract 为 current publication entry/readiness chain；同步 Codex/Claude/Cursor 三副本；更新 Shared `tests/test_contract.py` 当前 owner/consumer 断言；D1-V2 运行 |
| S5 更新当前 Knowledge 与 Architecture | 真实 S1–S4 内容及 fresh candidate/final-plan 结果；原 Architecture/RDT owners | 在合法 task-local contribution 或 direct delta 中同步七个命中 Architecture 当前单元；修正决定 4 后晋升 `ADR-POSTCOMMIT-INDEPENDENT-REVIEW`；同步 lifecycle R/D/T、Requirements/Design `knowledge-maintenance.md`、Requirements/Design/Test `completion-closure` 对应正文和 Test `runtime-location.md#813`；完整复核 ADR consumers；保留其他历史身份；原 owners final integration/readback；D1-V5 核对 |
| S6 来源验证 | 完整 S2–S5 after；原 verifier/tools owner | D1-V3 source、平台根、focused Codex 来源样本、同项目三平台 apply、installed validator、完整投影/sidecar 检查 |
| S7 提交与独立 Review | 完整工程与知识结果；原 TaskCommit/implementation/Review | 展示并执行精确本地 TaskCommit；constructor/begin_check 固定 B..H；新独立 reviewer 同次完成 Architecture、九维和完整 Branch Review |
| S8 D1 交付 | 通过 Review；publication Architecture eligibility | Publication 完成 readiness、准确中文 Refs #908 预览、确认后 push/PR 与 expected-head Merge；实际 delivered 后交 Completion |

S1 之后先写实际内容，不进行 Git/GitHub 副作用。S2–S5 按依赖执行；若 RDT delta 揭示新的需求或 Architecture 影响，停止本批并回对应原 owner。

## 3. 验证入口、输入与预期观察

以下为未来执行计划，不预填结果。

### D1-V1：upgraded 生产者和消费者

运行 `guru-upgrade-installation` 现有定向回归：

```bash
bash trellis/skills/guru-team/runtime/resolve-python.sh \
  "$PWD" "$PWD/trellis/skills/guru-team/runtime" \
  -m unittest discover \
  -s trellis/skills/guru-team/packages/guru-upgrade-installation/tests \
  -p test_contract.py
```

期望现有 producer 的 upgraded result 与 canonical manifest 的 `.11` 一致，并可通过 package schema、shared stop consumer 和 active example。普通 dirty/untracked formal source 仍拒绝。测试沿 manifest 读取目标，不新增固定 `.11` 自证断言。

### D1-V2：私有发布链与四副本

```bash
python3 .agents/skills/release-guru-trellis-version/tests/test_contract.py
```

基线已观察到两个正常失配：查询 `guru-review-task-delivery/interface.json` 报 `FileNotFoundError`，`guru-review-branch:passed` 的实际 consumer 是 `guru-publication-entry-router` 而不是旧 owner。修改后期望：

- 不要求已移除 Skill 的 Interface；
- Branch Review `passed` 由当前 publication entry router 承接；
- Private contract/四副本字节一致；
- incomplete private Skill 仍被 registry/preset/manifest 排除；
- D1 delivered 后才进入实际 adoption，Stage 2/tag/Release/本地收敛边界仍完整。

该测试只证明 Interface/workflow/private contract 结构与直接消费者一致，不证明真实 AI 独立审核或 GitHub 发布。

### D1-V3：source 与来源样本

先执行 source/package 与声明 roots：

```bash
bash trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json
for root in .agents/skills .claude/skills .cursor/skills; do
  bash trellis/workflows/guru-team/scripts/bash/check-skill-packages.sh \
    --root . --mode source --platform-root "$root" --json
done
```

再由现有 throwaway verifier 从完整 D1 after 建立一个 focused Codex 来源样本。实际 invocation 按脚本当时的 help/contract 选择；至少完成 clean install、existing-project update/reapply、native load、CLI/source lock、实际受管字节/mode、selected platforms 和 sidecar 观察。然后在同一项目补齐 Claude、Codex、Cursor apply，并执行目标自身 installed validator和完整项目映射比对。

证明边界：

- source/platform-root 检查证明声明结构，不证明完整安装；
- 来源样本证明当前 dirty/local candidate 的安装与重应用；
- 来源样本不证明准备 checkout 的正式 `source_locked` 采用、前驱升级、远端 `.11` 或客户端业务使用；
- 如果 verifier 的正式 profile 要求远端 candidate，而 D1 尚未交付，则按 local sample 的当前声明边界运行并明确记录限制，不修改 verifier 绕过。

### D1-V4：公开说明

完整读取三份 README 的相关章节，检查：

- canonical 当前版本为 `.11`；
- 前驱为 `.10`；
- `.11` 示例只在对应非 draft、非 prerelease GitHub Release 存在时使用；
- workflow marketplace 与 preset 使用同一 ref；
- source lock/CLI 仍为当前固定值；
- 历史版本和链接保持正确。

运行 `git diff --check` 和改动 Markdown 的链接/anchor/命令行检查。文档通过不证明 Release。

### D1-V5：RDT 与 Architecture

Knowledge delta 必须包含实际 lifecycle 三层、Requirements/Design `knowledge-maintenance.md`、Requirements/Design/Test `completion-closure.md` 和 Test `runtime-location.md#813` 的完整受影响正文，而不是只替换关键词。原 RDT owner 在 TaskCommit 前 final-integrate/readback 到 current units，并记录 `integrated_pending_review`。`T669-06` 与 `#813` 的观察边界只同步当前阶段名称，不改其历史结果、证据截止或未验证结论。

Architecture delta 使用已正式通过的 `architecture_impact / target_native` candidate assessment，contribution 位于 `docs/architecture/contributions/908-release-v0.7.0-guru.11.md`。必须覆盖 `ARCH-CUR-051`、`ARCH-DOM-036`、`ARCH-DOM-055`、`ARCH-DOM-059`、`ARCH-INT-015`、`ARCH-INT-020`、`ARCH-GOV-009` 的实际 after。`ADR-POSTCOMMIT-INDEPENDENT-REVIEW` 保留 #794 attribution、决策 1–3/5–6、证据和替代边界；决定 4 的旧 Delivery Review readiness 以历史/替代关系呈现，当前 Publication readiness 明确来自 R900/D900 与 #900。同步修正 ADR“窄替代与保持”阶段的 Delivery Review 责任句，并把“当前只有候选方案”改为带截止的历史观察，再从 `proposed` 晋升为 accepted/current。必须完整读取并核对 `docs/architecture/README.md`、system、ownership、workflow-context、distribution、change-contract、rules 和四份 RDT knowledge/task-lifecycle consumers；`ARCH-GOV-008`、`ARCH-CUR-070`、`ARCH-DOM-053` 与 distribution 的 proposed-status 说明在 promotion 后仍准确。历史 `ARCH-CUR-032`、旧 #435 阶段描述、contribution、roadmap 和 evidence 保留原身份。final_plan 必须独立评估更新后的完整 design、实际 contribution 和 ADR promotion，不能复用 candidate assessment 作为最终通过。原 Architecture owner 在 TaskCommit 前 final-integrate/readback，并只输出允许的 `integrated_pending_review` 或等价 pending 状态。

### D1-V6：完整交付

原 TaskCommit 形成精确待审 H，原 constructor/begin_check 固定完整 B..H。新独立 reviewer 在冻结候选上完成 Architecture before/after、九维、Docs、Cross-layer、Compatibility、Deployment/Operations 和 Verification Completeness。通过后由原 publication entry 获取 Architecture eligibility，再由 `guru-publish-task-delivery` 形成精确预览并执行；实际 delivered 才交整体 Completion。

## 4. 停止条件与适用回退点

- Task/key/phase/scope/root 不符：停在 Identity/Ensure/Bind/Selection 或当前 scope owner。
- 版本 producer/consumer 不一致：停在本批 upgrade/docs writer。
- 私有发布链与当前 registry/workflow 不一致：停在本批 private consumer writer。
- source validator、平台根、来源样本或 installed validation 失败：保留原始 stdout/stderr，修复本批源；不手改样本或留给 D2。
- Architecture 新事实或机制变化：停止实现，交原 Architecture candidate/conflict 路径。
- Architecture/RDT 发现需求、归属或行为变化超出当前 owner graph 同步：交原 Clarify/Author 或 Architecture 冲突路径，不把文档同步当业务变更。
- Review finding 或 content change：由原 writer 形成后继内容，TaskCommit/Review 的当前结果按原合同失效并刷新。
- Git/GitHub 输出丢失：由原 TaskCommit、Publication 或 Merge owner 回复同一操作/结果，不重复副作用。

先完成便宜定向检查，再跑完整来源样本；证据充分后停止追加实验。设施反复失败时重评当前入口/环境，保留具体缺口，不把未执行项写成通过。

## 5. Delivery Policy（唯一）

策略为 **staged**。

当前 D1 覆盖完整可分发源、版本直接消费者、公开说明、私有发布消费者和 RDT/来源验证。进入条件是 Planning final/Approval/Activation 通过；退出条件是完整实现、必要 RDT readback、精确 TaskCommit、固定 B..H、独立完整 Review、Publication readiness、PR 合并为 delivered。

真实临时限制对象是准备 checkout 的 `.11` 安装采用；原因是正式 `guru-upgrade-tools(source_locked)` 必须先有已 delivered 的完整干净源。解除条件是 D1 delivered；直接后继是 Completion 返回 `additional_delivery_required`，Creation 建立 D2，D2 独立 Planning/Activation 后由 tools owner 完成实际采用。

整体准备还需要 D2、whole-Task Completion、reference-only Closure、Finish 和 Task 外正式发布。D1 delivered 不表示这些完成。

## 6. Docs SSOT Plan（唯一）

strategy 为 **delta_first**。

实际受影响的长效 Knowledge 为：

- `docs/requirements/current/task-delivery-lifecycle.md`：R531/R636/R637/R794/R900 中仍把 readiness 描述为独立 Delivery Review 的现行句子；改由 R900 的 `guru-publish-task-delivery` readiness 统一承接。
- `docs/design/current/task-delivery-lifecycle.md`：D531/D636/D637/D794/D900 的对应 owner 描述。
- `docs/test/current/task-delivery-lifecycle.md`：T531/T636/T637/T794/T900 中过期的独立阶段表述和当前 Publication 场景。
- `docs/requirements/current/knowledge-maintenance.md` 与 `docs/design/current/knowledge-maintenance.md`：当前阶段读取和 Review result 消费中把独立 Delivery Review 写成 current owner 的正文。
- `docs/requirements/current/completion-closure.md`、`docs/design/current/completion-closure.md` 与 `docs/test/current/completion-closure.md` 的 `T669-06`：当前 Delivery Review 维度判断、后续 consumer 和观察边界中的旧阶段名称。
- `docs/test/current/runtime-location.md` 的 `#813`：当前观察边界中的 `Branch/Delivery Review` 旧阶段名称。
- `docs/{requirements,design,test}/current/codex-skill-distribution.md`：R724/D724/T724 已承载私有 Skill 排除公共分发、匹配安装与局部证据边界，本批只复核，不复制私有 release 规则。

实际受影响的长效 Architecture 为：

- `docs/architecture/01-current/system.md` 的 `ARCH-CUR-051`。
- `docs/architecture/03-domains/ownership.md` 的 `ARCH-DOM-036`、`ARCH-DOM-055`、`ARCH-DOM-059`。
- `docs/architecture/04-integrations/distribution.md` 的 `ARCH-INT-015`、`ARCH-INT-020`。
- `docs/architecture/06-governance/rules.md` 的 `ARCH-GOV-009`。
- `docs/architecture/adr/postcommit-independent-review.md` 的 decision-authority 状态。

上述正文中的旧独立 Delivery Review current owner/gate 描述必须改为 Branch Review 后由 `guru-publish-task-delivery` 承接 readiness 与发布。`ADR-POSTCOMMIT-INDEPENDENT-REVIEW` 必须修正决定 4 和“窄替代与保持”阶段句，把“验证与重评”的唯一候选断言改为带截止的历史观察，明确当前决定来源为 R900/D900 与 #900，再晋升为 accepted/current；完整核对 `docs/architecture/README.md`、system、ownership、workflow-context、distribution、change-contract、rules 与四份 RDT knowledge/task-lifecycle consumers，纯引用在 promotion 后复核，仍含旧阶段或 proposed 自述的正文实际更新。不得继续让 current 正文依赖 proposed 决定。历史 `ARCH-CUR-032`、旧 #435 阶段描述、contribution、roadmap 和 evidence 保留原身份。

Task-local Architecture contribution/proposed target 与原 RDT contribution 由各自 owner 在计划批准后建立，包含每份受影响 current 文件的完整 proposed after 或可唯一定位到完整 proposed target 的最小索引。最终整合前重新读取 live current、贡献和历史条件；由原 owners 写入/readback，状态只到 `integrated_pending_review`。直接 consumer 是 TaskCommit 和固定 committed candidate 的独立 Review。

旧 `no_architecture_impact` 已因冲突失效；fresh candidate 必须重新判断 impact/change path，final_plan 必须独立评估本设计。`ARCH-INT-009` 和修订后的 `ARCH-INT-015` 继续承接私有发布组合和 D1/D2，但不能替代上述 owner graph 同步与 ADR 身份收敛。

Docs Plan 不修改 public managed dogfood 副本、共享根索引或生成清单来制造完成；这些由 D2 的实际 tools 采用和适用验证承接。

## 7. Official Context Selection

完成规划后，通过当前 `task.py add-context ... --delivery 7fa61b67-258e-49db-9db3-505f1a0c4e3e` 为 implement/check 选择实际直接消费者所需的文件：

- Task PRD、D1 PRD、design、implement；
- Author `planning-body.md` 和适用模板；
- 当前 private release contract；
- `guru-publish-task-delivery` 当前 contract/Interface；
- RDT `current-knowledge.md`、lifecycle 三份 current units、Requirements/Design `knowledge-maintenance.md`、Requirements/Design/Test `completion-closure.md` 与 Test `runtime-location.md`；
- Architecture baseline contract/current-knowledge，以及 `README.md`、`system.md`、`ownership.md`、`workflow-context.md`、`distribution.md`、`change-contract.md`、`rules.md` 的命中 current units 和 `ADR-POSTCOMMIT-INDEPENDENT-REVIEW`；
- `quality-guidelines.md` 的适用验证章节；
- 实际会被实施的版本 producer/consumer 和 private test。

context 文件必须由官方脚本生成和验证。不为未来可能使用添加空泛条目；每个条目写明当前实现或查检查的直接用途。
