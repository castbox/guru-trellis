# D1：v0.7.0-guru.10 完整可分发源设计

## 1. 设计目标、需求承接与内容基线

本批承接[本批 PRD](prd.md)的 D1-R1～R6、D1-SC1～SC4 和 D1-AC1～AC4；整体定义见[Task PRD](../../prd.md)。公共 scope_ref 选择整体 R1、R2、R5、AC1。目标是完整交付 `.10` 可分发源，供后继真实采用。实际采用、终态收尾和正式发布仍有各自责任。

开发基线 B 为 `f52ebfdc6954543d88eca5837dc1bd4dcc9767ab`，来自原 Sync 完成后创建本 Task checkout 的 main。Planning H0 同为该提交，是起点观察，不是实现候选。PR 目标是 `main`。实现后原 constructor 构造完整 B..H，不用后续 main 推进缩窄内容范围。Stage 2 再从届时最新 main 冻结正式候选。

独立 Architecture 的实际 candidate_assessment 为 `baseline_current / no_architecture_impact`；baseline 是 `guru-trellis-architecture`，constitution 是 `guru-trellis-design-constitution-v1`。本批遵循 ARCH-INT-006/014/015、ARCH-GOV-008/009，没有新增 owner、状态或兼容链。该结果不代替当前正文的 final_plan、Approval、Activation。

## 2. 当前系统、边界与目标差额

这是首个 Delivery，没有前序 delivered 结果。canonical manifest、upgrade-installation 当前目标及实际安装均为 `.9`。Fork CLI 为 `0.7.0-castbox.6`，canonical lock 是 `e3793251fad8bd261d0c370d408c7675b9f6a140`。本批提升 Guru revision，保持 Fork 来源和版本轴。

版本生产者、三处输出消费者和 active example 成套改为 `.10`。三个 README 更新当前版本、正式前驱和安装条件，保留 `.8` 等历史来源与专项证据。私有 release 合同还把 Wording 写入准备链；本批按 current workflow 对齐原 Author、Architecture、Approval 的职责，取消默认独立节点，保留原内容 owner 的完整判断。

来源验证使用一个临时项目：focused Codex 后在同项目补齐 Claude/Codex/Cursor。真实 Task checkout 的旧 `.9` installed/discovery 保留给 D2，不手改受管副本。主目录发布后收敛属于 Stage 2。

## 3. 来源设计处置（唯一）

| 来源及原承诺 | 处置 | 具体落点、理由与影响 | 上游处置 |
| --- | --- | --- | --- |
| 私有 release contract / Complete Source Before Actual Adoption：D1 完整源及自身验证先交付 | retain | §2/4/8；临时项目覆盖本批自身安装与直接消费者，失败不得留给 D2 | current ARCH-INT-015，无偏离 |
| 同节：delivered → Completion additional_delivery_required → Creation → D2 Planning/Activation → source_locked | retain | §6/7；本批不建 D2、不从 TaskCommit 直接转 tools | 原 Completion/Creation/tools |
| 私有 contract / Stage 1 第1项中的 Wording 顺序 | change | §4/6；删除默认独立 Wording 文案，原 Author 自检后 candidate、solution、final_plan、Approval | current workflow Phase 1、R153-04/R850-01、D850-01 已承接退役；仅迁移私有消费者 |
| 同合同 Stage 1 第2～6项：工程、知识整合、TaskCommit、独立 Review 两槽、readiness、Publish/Merge | retain | §6/8；真实 producer/consumer 回归，无 early Draft、重复 Check 或 source-only commit | current owners 和 ARCH-INT-015 |
| Whole Preparation Completion And Reference-Only Closure | retain | §6/7；Refs #861，Closure no_mutation；采用未实施不能 Finish | 后继原 Completion/Closure/Finish |
| Stage 2、Local Installation Convergence、Independent Mutation Confirmations | retain | §7/8；最新 main、tag/smoke/Release、主目录安装、Issue close 各保留边界 | Task 外原发布 owner |
| current workflow Phase 1、Author planning-body：唯一 writer、独立 Architecture、Approval、Activation | retain | §5/6；当前 Delivery 正文及官方 context，不增公共 node/schema/runner | candidate 后展开，后续 gates 实际执行 |
| ARCH-INT-006/014、D724-01～04：固定 Fork、共享发现根、完整投影、证据分层 | retain | §4/8；原映射和 installed validator 核目标，Codex 公共根为 .agents/skills | 无新迁移或旧 .codex 公共根；私有副本仍私有 |

其余来源角色见 PRD；公开说明不自行授权发布，历史 Test 不作本候选 pass。

## 4. 模块、职责与设计取舍

### 4.1 版本生产者与消费者

实施 owner 修改以下六处当前目标，保持原 shape、来源家族、CLI 和 lock：

- `trellis/guru-team-extension.json` 的 version。
- `trellis/skills/guru-team/packages/guru-upgrade-installation/runtime/owner.py` 的 TARGET_GURU。
- 同包 `schemas/public-upgraded-output.schema.json`。
- 同包 `consumers/stop/production/upgrade-installation-upgraded.schema.json`。
- `trellis/skills/guru-team/consumers/stop/production/upgrade-installation-upgraded.schema.json`。
- 同包 `examples/public-upgraded-output.json`。

实际 upgraded 输出由原公开入口生成，三处 schema 消费同一结果。不增第二版本 authority、双读或 adapter；历史 fixture、普通 dirty/untracked 正式来源拒绝语义保持。

### 4.2 私有消费者和公开说明

Shared `.agents/skills/release-guru-trellis-version/references/contract.md` 是私有正文；同步 `.codex/skills`、`.claude/skills`、`.cursor/skills` 下同 Skill 的合同。入口含义实际变化才改四份 SKILL。必要回归在 Shared `tests/test_contract.py`，核当前公开链与私有排除分发；不加入公共 registry、preset 或 inventory。

三个 README 各守分工：根页面拥有产品入口/版本选择，workflow 页面拥有流程导航，preset 页面拥有安装/构建/验证。当前目标为 `.10`；前驱改为真实 `.9` 并核 peeled commit。历史 `.8` 配对及已发布事实保留，不能全局替换。`.10` 正式安装仍以非 draft、非 prerelease Release 存在为条件，不写预定成功。若需构建，使用当前 pnpm，不为执行另固定版本或修改 package-manager 声明。

### 4.3 来源样本

复用原 verifier 的 local sample 分支：一个明确临时目录跑 focused Codex，再在同目标原 apply 加三平台。marketplace main 只供 bootstrap；真正被测 workflow/preset 来自当前本地 canonical copy。保留原 update/reapply/native-load 检查，不修补样本产物。

证明分三层：source validator 的 platform-root 只核声明根结构/支持；样本 own installed validator 核实际安装合同；完整 `managed_source_projections` 映射逐项比 canonical bytes，按原 mode 规则核执行位，另核 manifest/provenance/workflow/lock/platform selection。根检查不能单独建立完整 parity。

复用单项目而不建新 installer/helper/累计矩阵，代价是本批不证明 immutable 远端 `.10`、前驱升级、真实 source_locked 或客户端业务使用；这些按 D2/Stage 2 和实际边界分别处理。

## 5. 接口与数据

无新增 public 字段、schema id、Skill id、typed exit 或持久状态。升级生产者的当前目标 Guru 值改为 `.10`，原输出 schema 和两个 stop consumer 同步。CLI 仍为 `0.7.0-castbox.6`，不将 Guru revision 写入 `.trellis/.version`。

规划接口保持 requirements_ready → Architecture candidate_assessment → Author delivery_solution_planning/plan_ready → Architecture final_plan → Approval → Activation。消费实际候选的薄 assessment，不复制其 private evidence。官方 implement/check JSONL 用原 task.py add-context --delivery 写当前 planning_root。

样本 manifest 由原 installer 产生，source provenance 如实保留 dirty/local_sample 观察，不声称 HEAD 包含未提交内容。本批没有数据迁移，不转换既有 Task/schema/安装。

## 6. 状态、顺序、正常与失败流程

1. 完成当前三正文和官方 context，经 Author plan_ready、独立 final_plan、Approval；展示完整计划，原 Activation 接受后才实现。
2. 修改完整版本消费者、私有合同与命中回归、三个 README；跑定向测试和来源样本完整投影比较。
3. 原 RDT/Architecture owners 判断实际差额，必要完整整合/readback；补受影响检查。原 TaskCommit 预览精确文件并提交，之后原 constructor/begin_check 固定 B..H。
4. 新独立且未参与实现 reviewer 同次完成 Architecture before/after、适用 Check、完整 Branch Review。真实 check/full_review 两槽齐全才可 ready。修复仍走原 writer、后继提交和受影响审查。
5. 原 Delivery Review 形成中文 Refs #861 payload；Publish/Merge 分别确认并读回。只有 delivered 才进入 whole Task Completion。

来源缺失、版本消费者不一致或样本失败，停在本批实施/规划 owner，不改断言制造 pass。正式 source_locked 前置未成立不调用真实 tools。main 正常推进不改 B，需要集成沿原 Reconcile；Stage 2 另承接最新 main。

## 7. 恢复、兼容、迁移与集成

保留原 stdout/stderr，通过原 producer 恢复已执行结果，不重复 Task/Delivery/commit/PR 创建。本批不建新恢复协议或 checkpoint。正文变化刷新受影响 final_plan/Approval；机制变化回 candidate；真实来源/范围变化回 Clarify。

公共 shape 和来源家族保持，当前目标版本的 producer/consumers 成套交付。历史版本事实保原时间和来源。私有 Wording 迁移跟随当前职责，不对旧 provider 在途操作改标签或启动双读。

Task checkout 暂留旧安装是局部限制，原因是 `.10` 尚无已交付完整干净来源。解除条件为 D1 实际 delivered。原 Completion/Creation 才建 D2，其独立规划/接受后由 tools source_locked 更新全部 installed after；D1 自身失败不满足解除条件。D2 完成后仍需 Completion、no_mutation Closure、Finish 簿记入 main，Stage 2 才冻结届时最新 main。

## 8. 验证设计

| 验证 | 要求/验收 | 入口与独立观察 | 证明限制 |
| --- | --- | --- | --- |
| V1 版本接口 | R1/R5、AC1 | upgrade-installation 现有三定向用例；实际 upgraded 输出通过三消费者；dirty/untracked 正式源仍拒绝 | 模块 fixture，不是业务迁移 |
| V2 私有链 | R3/R5、AC2 | 私有 test_contract.py 原公开包装链、D1→Completion→Creation、私有 inventory 排除和四份一致 | 不证明实际 AI 判断或远端成功 |
| V3 source/roots | R1/R4、AC3 | source validator；样本三公共 root 结构检查，无旧公共 .codex 根 | 根结构不是完整字节/mode parity |
| V4 来源样本 | R4、AC3 | 一个 focused Codex 项目安装/update/reapply；同项目三平台 apply；own installed validator、完整映射 bytes/mode、manifest/source、workflow/lock、sidecar/drift | local_sample，不是正式采用/前驱升级/完整矩阵 |
| V5 说明分发 | R2/R3/R6、AC2 | 改变后完整相关章节、同 ref 命令/链接/anchors、当前历史身份、四私有副本、diff hygiene | 静态文字不证明 Release |
| V6 完整交付 | AC4 | 实际 TaskCommit、constructor/begin_check、独立完整 Review、readiness、Publish/Merge | D1 不等于 Task Completion/Stage 2 |

现有升级用例随 manifest 读取目标，优先复用；仅真实覆盖缺口改测试，不加固定 `.10` 自证断言。fixture 不种被测 producer 应产生的结果。先实现直接差额，再跑便宜回归，最后一个完整样本；无惯例重复红绿/回退要求。证据充分即停止追加；未触及必需分支时保留缺口并回原 owner。

## 9. Canonical 引用、本轮差额与实际未决项

Architecture 从 `docs/architecture/README.md` 进入，关联 `04-integrations/distribution.md` ARCH-INT-006/014/015、constitution、change-contract。candidate 无影响，不预建 contribution/ADR，不改共享导航；final_plan 仍独立判断当前正文。

RDT 命中 `docs/{requirements,design,test}/current/codex-skill-distribution.md` 的 R724/D724/T724，及 `issue-content.md` 的 R153-04、R850/D850/T850。已有共享发现根、实际采用分层和 Wording 退役职责。本批沿既有能力提升版本及迁移私有消费者，没有新增业务定义；Docs 策略见 implement §6。公开版本条件写三个 README，不建知识版本登记/release ledger。

没有未决产品选择。工程验证、final_plan、Approval、Activation 和交付尚待实际执行，不预填结果。发现超出候选的实际差额，回原 owner 并刷新受影响规划。
