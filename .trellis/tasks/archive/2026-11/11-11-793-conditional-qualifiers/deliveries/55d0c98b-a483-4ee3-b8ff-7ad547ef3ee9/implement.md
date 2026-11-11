# D1：qualifier 条件加载与调用实施计划

## 1. 输入与引用

本批从固定 B=`e30c7bb5d4c24bc075dc14cfcd04c1da00fcf78e`、无前序 D1 开始，范围是整体 [PRD](../../prd.md) R1—R6/AC1—AC4 与切片 [PRD](prd.md)。[design 第3节](design.md#3-来源设计处置唯一)独占来源设计处置；第4—7节拥有精确条件、十一 caller、root 前置与迁移方案。

实施前加载实际三 qualifier/caller 完整命中合同、workflow 的 Mandatory qualification profiles 与第2.1节；加载 `.trellis/spec/workflow/{skill-package-contract,workflow-contract,quality-guidelines,companion-scripts}.md` 的公共 I/O、applicability/coverage、Test And Validation Value 和适用确定性边界。加载共享 Author `references/planning-body.md` 及 design/implement 模板，避免只用摘要派工。

Architecture 输入为原独立 candidate_assessment 与 [真实贡献](architecture-contribution.md)、[ADR 候选](adr-conditional-qualification.md)。当前 baseline/constitution/change-contract 身份见 design 第1节。原 RDT 单元、ADR-008/020、实际 consumer 与测试必须按第6节 Docs Plan 重读；引用存在不证明已读。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 依赖、原 owner 与文件 | 改动和完成观察 |
| --- | --- | --- |
| I1 适用条件 | 规划接受并实际 Activation 后；实施 owner；三 `trellis/skills/guru-team/packages/guru-qualify-*/references/applicability.md`、其 SKILL/contract/interface | owner 各自拥有短条件，全文引用同一条件；normal/solution reuse/refresh 与 root 前置共同收敛。无新脚本 classifier/字段/exit。Review 能分别定位触发、采用、刷新和加载动作 |
| I2 caller/consumer | I1；实施 owner；task-free、Clarify、readiness、Author、Approval、Reconcile、Check、Branch Review、Delivery Review 的原 SKILL/命中 references；canonical workflow | 十类及 Author 的实际落点按 design 第4.2节执行条件调用；保全部原出口/唯一consumer、完整阶段责任。核 root-only 正常入口不再要求虚构 upstream result，空候选原行为保持 |
| I3 示例与迁移 | I1/I2；实施 owner；三包 examples/必要 tests，`trellis/presets/guru-team/MIGRATION-793.md`、workflow/preset README | 示例、诊断及 native fixture prompt 不再把固定三连当必要前置；现有 wire 合法示例继续可用。明确 matching 切换与在途同Task/key/实际阶段恢复，不改未受影响算法 |
| I4 定向验证与隔离知识 | I1—I3；实施/验证 owner，RDT/Architecture 原维护方 | 执行 V1—V4；只补真实缺口。准备第6节完整 RDT 与 Architecture proposed，保写前 authority 与历史证据，不在此先晋升 shared current |
| I5 受管同步 | 完整 canonical 候选与适用验证后；原 guru-upgrade-tools owner | 加载其完整 source 合同，保 Task/session 同步 dogfood、Claude Code/Codex 等实际受影响投影，逐个处理 sidecar。执行 V5，不能手工覆盖安装文件 |
| I6 完整候选到最终质量链 | I4/I5；原实施协调、独立 Architecture、Check、RDT/Architecture owners | 构造固定B完整 Candidate，实际 begin_check；candidate Architecture/Check 后按原 route 回 implementing、原 final_integration 晋升/readback；重新构造 actual after、最终 Architecture/Check。原 TaskCommit 和独立完整 committed Review 后再 readiness/发布 |

每批 source/test/task 写入前运行原 `check-task-checkout-boundary.sh --json --task .trellis/tasks/11-11-793-conditional-qualifiers` 并要求实际 ok。派工如 workflow 要求子 Agent，明确互不重叠文件责任及其他协作者存在；最终协调 owner 负责跨 caller/root/迁移集成。

## 3. 验证入口、输入与预期观察

V1—V5 的行为输入/独立断言以 design 第8节为准，本节只定义执行安排和证据边界。

- V1：使用 matching managed Python 运行三个 qualifier 的 `tests/test_contract.py`、`tests/test_runtime.py`，并运行实际改变 caller/consumer 命中的既有测试。通过原 source/installed `check-skill-packages.sh --root . --mode <source|installed> --json` 核声明、schema和consumer graph。按实际 wrapper 提供真实 profile/候选及当前 facts；不以 static string match 宣称语义调用正确。
- V2/V3：采用现有 root `tests/run_behavior_validation.py` / `run_native_reuse.py` 的隔离 provider 方法，定向调整本批必要 fixture/入口；从完整实际原 caller 读取条件，保留工具 read/invoke/实际结果事件。新场景包含普通工作无 qualifier、真实 root-only 与触发非通过回原 consumer；若已有测试已实证同一未变边界，采用其明确观察，不重复全阶段矩阵。host 不预填 semantic verdict、上游结果或当前 pass。
- V4：在同机制适用结论可得的真实后续入口验证采用，再提供真实材料变化及结论丢失，观察原 owner 刷新/恢复；新 invocation 仍通过原 current facts 检查。原 runtime stale/error/projection 用例负责确定性边界，native trace 负责语义行为。raw trace 仓库外，不持久化授权或审计账本。
- V5：沿原 tools owner 完成同checkout安装后，运行 source/installed package、受影响投影和 `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`；读取实际 Task/Delivery current 和 context 验证 key/root/阶段保持，检查 `.new/.bak` 的真实处理结果。该 Task 不要求完整 clean/update/多平台矩阵。只有具体变更产生干净安装证据缺口时，最多追加一个代表性 clean throwaway；先说明该未决问题。

具体 managed Python 与 harness 参数以实施时读取到的原入口帮助/当前 source 合同为准，不手写 runtime 私有事实或绕过 fixture 前置。source/installed、确定性、native、外部链路各自报告；规划未运行这些命令，当前不记 pass。

## 4. 停止条件与适用回退点

来源/scope 实质变化回原 Clarify；方案机制改变回 Author/独立 candidate_assessment；wire/schema/consumer 真实差额超本方案时回原 Architecture 与规划，不静默扩大。必要结论丢失回原 producer，普通 stale/re-entry 不新增审批。原 nonpass/blocked/unknown出口只由其唯一 consumer 承接。

验证未触达声明边界时，不将设施错误记作产品失败或通过。设施连续失败须重评入口，采用回答同问题的有界观察或保留验收缺口；不能降低 assertion。原必要验收及相关回归仍须完成。V1—V5足以支持本次实际行为后停止额外实验，不因数量、执行者或阶段变化重做。

无数据格式或数据库迁移，不新增 rollback 协议。未发布源码可在本次确切文件范围修复；安装恢复按原 tools owner 的 matching/reapply/sidecar 路径，不覆盖用户并行改动。shared promotion 的部分写入按原 intent 恢复；commit/push/PR 前另展示精确计划，merge 不在本段执行。不得将 gate 或用户授权写成 tracked/ignored 证明。

## 5. Delivery Policy（唯一）

Policy：`full`。D1覆盖本 Task 整体 R1—R6、AC1—AC4，包括各自条件、实际十一 caller、原出口/root前置、采用刷新、迁移、定向证据和受管同步。没有为本 Task 留给 D2 的独立功能或临时能力限制；#736其他拆分、#734、完整矩阵及业务事故/费用效果不在本 Task。

本批完成条件是范围内实现、必要实际验证、完整 current knowledge reconciliation、最终 Check、独立完整 committed Review、readiness 与当前授权的 PR 发布均有实际结果。此执行段只发布 main PR，并在 merge 前停止；whole Task Completion/Closure/Finish 仍由未来真实 merge 与其原 owners 判断，不能把 PR 存在当完成。

## 6. Docs SSOT Plan（唯一）

strategy：`delta_first`。当前 design/贡献是隔离候选，实施形成完整拟写，最终 Phase2 前通过原维护方 reconciliation/final_integration 晋升。Author 不直接改 shared current、根导航或 spec projection。

| 命中单元/差额 | 原 writer、直接 consumer 与时点 |
| --- | --- |
| 新 `docs/requirements-design-test-contributions/793-conditional-qualifiers/{requirements,design,test}.md` 完整当前单元；保留R1—R6及V1—V5实际观察/未验证项 | 原 RDT owner；Check/Delivery/Completion读取当前要求与证据。candidate Check审完整 proposed，原 final_integration 晋升并readback |
| 旧 #382 REQ-382-01/DES-382-04 的“必须经过两上游 outcome”前置及真实必要引用 | 原 RDT owner；完整读取并窄替代当前条件，保旧Test历史观察和原归属；不得从历史已晋升内容删掉有效诊断/缓解/保护/完成边界 |
| 原三 qualifier/caller/workflow、Migration与README | 原实施 owner维护canonical，原 tools owner分发；下游caller、在途恢复与安装consumer读取。完整matching采用后验实际投影 |
| ADR-008/020、命中的 CURRENT/ownership 单元及新的条件调用决定 | 原 Architecture owner；独立final_plan、candidate/final Architecture、Check与committed Review消费[贡献](architecture-contribution.md)/[ADR候选](adr-conditional-qualification.md)。实施准备完整隔离proposed，final_integration才写shared targets |

只改真实受影响单元及必要引用，根 README/共享列表不登记独立 Issue。不新增账本、泛化 DTO 或用户授权记录。采用与刷新方法的可复用正文仍由原 skill/spec 独占，不在知识单元重复全部规则；实现/测试、源码/dogfood、目标项目采用和业务效果分别说明。
