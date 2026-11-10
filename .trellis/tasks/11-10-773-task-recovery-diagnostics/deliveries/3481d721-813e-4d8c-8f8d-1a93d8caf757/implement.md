# #773 D1：实施与验证计划

## 1. 输入与引用

本批读取根 `prd.md` 的完整 accepted_scope，以及本目录 PRD 的 R1/R2、AC1–AC4。设计及唯一来源处置见 `design.md` 第3节；接口、恢复顺序与验证分别见第5、6、8节。没有前序 Delivery，起点为 B=`313d80215f65777fc70893a90c6d8dce8005d6dd`。

实施前读取 Branch 包 `SKILL.md`、`interface.json`、schemas、commands、runtime 和现有 tests，以及共享 `runtime/task_lifecycle/branch_resolution.py`、C4 store、C5 OwnershipPort/ledger 的适用条件。Identity、Ensure、Bind 的实际公开入口和原生 task.py 负责各自步骤。写作加载安装的 clear-technical-writing、Author planning-body 和两模板；验证方法加载 quality-guidelines 的 Test And Validation Value 与 Validation Scope Ownership。Architecture authority/constitution/change contract 和真实 candidate_assessment 见 design 第1节；本地贡献/ADR 仅为 proposed。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 依赖／原 owner 与文件 | 行为、产物及完成观察 |
| --- | --- | --- |
| I1 | Activation 后；实施 owner；Branch `tests/test_contract.py`、`runtime/invoke.py` | 补 V1，修复 discovery/recorder 共用 Task 解析转换；两个公开入口保留拒绝并返回准确诊断。 |
| I2 | I1；Branch 与共享 runtime owner；`runtime/task_lifecycle/branch_resolution.py`、包 runtime/schemas/interface/commands/examples | 实现 delivery_restored_checkout，复用原事务；保留 active profile 和 typed outputs。按 V2/V3 观察准入、补缺、匹配复用、普通失配和同身份历史保留。 |
| I3 | I2 接口明确；原 Branch/Identity/Ensure/Bind owners 的 `SKILL.md` 及 Branch 新 references；`MIGRATION-773.md` | 写完整公开恢复顺序、精确调用例和各自 stop；说明 HEAD/工作区差异、无隐含 commit、primary 支持和现有恢复。V4 核实际消费前提。 |
| I4 | I1–I3；原 RDT/Architecture writers；本目录隔离贡献和拟晋升 targets | 准备完整 R/D/T 叶子、C4/C5 ownership 关系 after、完整 ADR；含真实证据与未验证边界，保留 pre-promotion authority。尚不写 shared current。 |
| I5 | I1–I4 自检足够；原 tools owner；canonical/installed/dogfood projections | 通过 guru-upgrade-tools 完整源合同同步，保留本 Task/session；跑 V5 和受影响原回归，处理真实 sidecar。 |
| I6 | 完整实现及拟写；独立 Architecture + 原 Check | 构造 public candidate/begin_check，执行 phase2 与 delivery_candidate_check。仅 candidate_checked 合法回 implementation 后由原 owners final_integration/readback；再重绑实际 after，执行最终 Architecture/Check。 |
| I7 | 最终质量通过；原 TaskCommit、独立 Branch Review、Delivery Review、Publication | 分别展示精确 Git/GitHub 副作用；按原 owners 提交、完整 committed Review、readiness 与 PR 发布。发布后停止，不合并。Task Completion 保持后续实际职责。 |

本批没有跨 Delivery 临时限制或待后继解除的功能；验证尚未完成是当前工作，不是已接受豁免。所有实施均待当前规划接受及原 Activation。

## 3. 验证入口、输入与预期观察

按 design 第8节 V1→V2/V3→V4→V5 的依赖执行，不预填 pass。

- V1/V2：以 managed Python 运行 `trellis/skills/guru-team/packages/guru-establish-task-branch-binding/tests/test_contract.py`。使用实际公开 wrappers；正常缺失 Task 观察拒绝诊断。代表载体用 Git 固定原文件，恢复到 HEAD 不含 Task 的 checkout，再实际 invoke 新 profile。原公共 Bind 观察同身份；fixture 仅建立边界前有效 Task/Delivery 历史，不代替新关联 producer。
- V3：同一 managed runtime 的 unittest discovery 运行 `trellis/skills/guru-team/runtime/task_lifecycle/tests/test_branch_substrate.py`，复用既有事务/只读用例并补真实新准入分支。上游依赖使用已审核的 `.trellis/scripts`，运行源测试时设置 `GURU_UPSTREAM_DELIVERY_SCRIPTS="$PWD/.trellis/scripts"`；不能使用私有类调用充当公开恢复流程。
- V4：按指引实际列出的 Git、task.py、Branch、Identity、Ensure、Bind 和 current/continuation schema 核参数、时序与结果。复用 #773 正文的 #223 历史观察，不操作原业务仓库，不以静态文本声称 native Agent 已执行。
- V5：执行 package validator、受影响 distribution/installed 检查和 `bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`；具体受影响命令从当前质量规范/工具 owner 选取。同步前后读取 current 的相同 key、scope/root 和 phase，检查实际 `.new`/`.bak`、可执行位和 source/installed 差额。Python syntax 使用内存 compile，不写 pycache。

长期测试覆盖 V1 和新增关联行为；本次安装/文档核对单独报告。必要验收和受影响回归完成后停止；新增失败或尚未解决的因果疑问才追加实验。设施反复失败时重评复现方法，保留明确证据缺口，不改变行为断言来取得绿色。

## 4. 停止条件与适用回退点

原身份、scope/root、源要求或当前 candidate 假设不匹配时停止受影响步骤，交原 Identity/Clarify/Author/Architecture；机制实质变化刷新 candidate assessment 及后续规划，不沿用旧结论。真实目标、写集或 Git/GitHub 副作用变化回原对话边界。公开动作仍无法承接恢复时停在 Branch，不用内部调用补流程。

普通事务失败使用原 snapshot/rollback；本批不新增 crash/锁协议。安装冲突按原 tools owner 的同操作恢复处理，不覆盖本地内容。只回退本批已核差额，保留并行改动。没有数据库/服务部署或生产数据写入，因此不制定生产回滚或迁移协议。未解决 V1–V5 必需缺口不得声称 AC 通过。

## 5. Delivery Policy（唯一）

策略为 full：D1 独立覆盖 R1/R2、AC1–AC4，包括经确认的最小执行缺口、原 owner 指引、代表恢复和受管投影。没有延期到另一个 Delivery 的本批责任。完成条件为实际验证充分、RDT/Architecture 原 owners 晋升及最终质量链通过；PR 发布是本次委托停点，不代表已合并或整体 Task Completion。整体 Completion、Issue disposition、Finish/cleanup 仍由实际后续 owners 执行，不在本批伪造结果。

## 6. Docs SSOT Plan（唯一）

策略为 delta_first。RDT 原 writer 在本目录准备隔离 contribution，晋升三个独立完整单元：`docs/requirements/current/task-carrier-recovery.md` 规定正常缺失诊断、同身份恢复、历史缺口与非目标；`docs/design/current/task-carrier-recovery.md` 规定原 owners、HEAD/工作区边界、新 profile 和原事务；`docs/test/current/task-carrier-recovery.md` 写实际 V1–V5 及层次限制。直接 consumers 为后续实现、Check、Review 和恢复 Agent。既有 task-delivery-lifecycle 只作为关系来源，不复制其完整模型，不改共享导航。

Architecture 原 owner 消费 `architecture/contribution.md` 和 proposed ADR，准备 `docs/architecture/03-domains/ownership.md` 原 C4/C5 关系的完整拟写与 `docs/architecture/adr/task-recovery-association.md`；直接 consumers 为 Architecture/Check/Branch Review 和未来 Branch 修改。不得以登记主题方式向 ownership 添加无关行。九 concerns、target_native、原 portable decision 和完整拟写由独立评估及 candidate Check 审查。两体系原 writers 在 final_integration 重读各真实目标、整合写入并 readback；随后 implementation 重绑 after 走最终质量链。Planning 不晋升共享 authority，不新增 journal、索引、恢复 ledger 或授权状态。
