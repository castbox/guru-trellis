# D1 实施与验证计划

## 1. 输入与引用

本批为 full D1，无前序 Delivery。实施前读取 [整体 PRD](../../prd.md)、[本批 PRD](prd.md) 全文及 [design](design.md)；design 第3节唯一维护来源设计处置，第5–7节定义本批接口、顺序及迁移。scope_ref 为整体 R1–R4、AC1–AC6，固定 B 为 `e6c3b8276d62ac174ab42cba5bca4d5784be2ca3`，实际候选由 implementation 原 owner 绑定。

必要引用为：`.trellis/workflow.md` 的唯一 continuation/Phase1、安装的五 Planning Skill 与各自 references、原 Bind/Selection、Readiness `references/contract.md` 的 identity/recipe/recovery，以及 design 第9节三个完整 RDT lifecycle 单元和 Architecture authority。Author 的 `references/planning-body.md`、design/implement templates 用于维护规划；清晰写作规范在实质输出前完整读取。历史 #548/#443/#396 只提供定位与兼容边界，不能替代本批证据。

候选 Architecture 已返回 no-impact；这不免除 Wording、final_plan、Approval、接受/Activation、Phase2、完整 committed Review。当前三文档及执行计划没有实现或验收通过声明。

## 2. 有依赖顺序的步骤与文件责任

每次写入前执行原 checkout boundary；只改当前 checkout 的明确文件。implementation 负责源码/测试和匹配投影，原 Author 负责规划变更，原 RDT 负责知识正文，独立 Architecture/Check/Review 保留原职责。子 Agent 若按现行流程使用，分配明确文件 ownership，不覆盖其他人的改动。

| 步骤 | 依赖、责任与文件 | 可审核产物及完成观察 |
| --- | --- | --- |
| I1 首失败与直接边盘点 | 当前计划经接受/Activation 后；implementation 读五 package entry/runtime、原 workflow created/continuation、projection、Readiness recipe和原 tests | 在正常隔离样本保存修复前首次失败与历史覆盖差额；明确五边实际命中，确认没有第二 writer 或正常能力回退 |
| I2 caller 衔接 | I1；canonical workflow、五 package SKILL/references；对应 README 及仅命中的平台入口 | 按 design 第4–6节补原 owner mandatory 调用、补缺后重读和原义务接续；Architecture first-read/独立性保持；不新建 wrapper/API |
| I3 客观诊断 | I1/I2；Author/Architecture 原 runtime、errors/tests及 `trellis/presets/guru-team/MIGRATION-679.md` | 拆原复合判断并报告首失败，保 code/DTO/exit及全部拒绝条件；列精确 diagnostic 前后映射。五边其余保护按 design 第5.2节核定 |
| I4 standalone recipe/回放 | I1；Readiness 原 `references/contract.md`、现有 ReadinessAdapterTests 与 formal_exit_boundary | 完整公开 recipe 可执行，双 mode合法/失配，distinct caller_locator；原 runner支持真实 standalone 失败consumer恢复，不替 Agent 写target或Gate |
| I5 Human artifacts | I1；canonical workflow展示、原 Approval artifacts测试、实际命中说明 | 真实 key 正向解析；Task-only 根 PRD；archive 实际 ref/key；缺文件准确返回。保留 helper API并实际执行命令 |
| I6 完整匹配分发 | I2–I5；原 preset apply、dogfood workflow/packages/overlay、声明入口 | 执行完整 apply和drift检查；逐项核 sidecar/mode/用户修改。必要 workflow同步沿官方当前机制，不靠一次性生成文件patch |
| I7 原生与兼容验证 | I6及V1–V6环境；implementation执行正常writer样本/真实CLI，独立原 Architecture完成语义审核 | 完整保留首失败与修复后正式stdout及实际mode；当前工作Task和并行会话不污染；缺项不能标passed |
| I8 RDT proposed与候选检查 | I2–I7；原 RDT按第6节写隔离贡献，原implementation candidate/begin_check，独立Architecture phase2及原Check candidate | 完整实现与全部拟写R/D/T正文先受审；candidate_checked不作为最终通过 |
| I9 最终整合与质量链 | I8；原RDT final_integration、implementation重新candidate/begin_check、最终Architecture/Check | 实际共享正文读回，最终Check覆盖真实全部after；再按各副作用边界进行TaskCommit、完整独立B..H Review、Delivery/Publication/Merge、整体Completion及后续closeout |

I2–I5 可在同一计划内按明确文件责任推进，但各测试使用匹配完整投影。若出现候选机制变化，先回原资格及Architecture，不以并行实现绕开依赖。

## 3. 验证入口、输入与预期观察

命令在本仓根执行。Python 测试使用当前已管理的解释器：`PYTHONPATH=trellis/skills/guru-team .trellis/guru-team/runtime/resolve-python.sh "$PWD" "$PWD/trellis/skills/guru-team/runtime" -m unittest discover -s <原tests目录> -p 'test_*.py'`。执行前核参数、依赖及当前测试实际范围，结果按本次候选记录，不填固定历史计数。

| ID | 入口与输入安排 | 预期与对应验收 |
| --- | --- | --- |
| V1a 原生主接收 | 正常writer在gitignored临时隔离repo建立Task/D1和真实创建输出；用Codex原生exec启动全新未绑定/未选接收会话。给实际对象/输出定位和目标，不给恢复答案或expected pass | 本会话自己执行原owner并到Author正式requirements_ready；保同Task/gen/key/root，修复前后首次条件对照。AC1/AC5 |
| V1b 原生独立审核 | 另一fresh Architecture真实子会话接收同隔离对象与候选；只给事实/目标/边界，按原prelude保持baseline-first，不注入PRD/验收/前序pass | 自行恢复自身事实并到candidate_assessment正式出口；人工预绑/预选样本不计。AC1/AC5 |
| V2 状态与已有进度 | `guru-create-task/tests/test_delivery_chain.py`、`guru-author-task-plan/tests/test_planning_chain.py`、projection/tests、Bind/tests和五Planning各原tests；正常owner形成缺Task/缺选择、不同选择、终态、phase/gen/scope真变。API/读取失败用现有边界测试，不手篡artifact；原生另运行已有Planning进度接续样本 | 覆盖design第5.2表全部事实，首失败具体，回原owner；无context单测不写session，匹配不重复写；保原进度/Git/并行会话。AC2/AC4 |
| V3 package recipe | `adapters/eval/test_stage0_fixtures.py` 的 ReadinessAdapterTests 和原package tests；实际执行更新后的公开 recipe，使用正常Clarify/Wording producer及真实completed review fixture | workflow/standalone两mode的standalone与proposed_draft合法到ready；mode失配/错误id被拒；distinct caller_locator合法。Fixture语义只作transport。AC3/AC4 |
| V3n 原生恢复 | 扩展原 `adapters/eval/formal_exit_boundary.py --root <隔离repo> --evidence <真实source/input/producer/error目录> --completed readiness-error --output <隔离运行输出>` 的profile支持；其中一条实际mode，自拟request_id首次正常失败后交原生Agent | Agent自行读合同重审十维，从原producer完整重建consumer，真实record/check/invoke到ready，producer/source保持；实际模式单列。AC3/AC5 |
| V4 定向兼容 | `guru-create-task` creation chain；`runtime/delivery_projection/tests/test_installed_projection.py` / `test_scope_revision.py`；`guru-bind-task-session/tests/test_runtime.py` / `test_portable_recovery.py`；五Planning package原tests与Readiness原suite | 保#548有/无context、#443隔离、#396proposed_draft原recipe/恢复及五直接消费者。只跑受影响scope所需集合，不扩全生命周期重写。AC4 |
| V5 真实展示调用 | 原 `guru-approve-task-plan/tests/test_contract.py` 对artifacts的package-owned回归；以正常schema2 Task/D1传真实key执行原resolver，另测缺文件、Task-only及archive | 三文档实际路径匹配root；缺文件保真实缺口；Task-only没有选择/创建；archive实际ref/key。canonical/dogfood/installed命令说明一致只是补充。AC4–AC6 |
| V6 分发与一个clean安装 | `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`；`.../check-dogfood-overlay-drift.sh`；按原README在一个干净临时repo正常安装matching workflow/preset，再完整reapply并运行命中owner/展示调用 | 核声明平台投影、mode、sidecar和保留用户区块；分开记录source/package、installed/native和真实Agent。不跑完整多平台Release/Upgrade矩阵，不更新业务安装。AC6 |
| V7 最终范围与知识 | 原RDT impact/promotion、独立Architecture、原Check、最终committed Review | 全部R1–R4/AC1–AC6对应实际证据，含历史边界/首失败/机制/正向与失配；候选与最终after分开。AC5及整体完成 |

原生执行使用本机已支持的 `codex exec --ignore-user-config --ephemeral --json -C <隔离repo> -s workspace-write -o <final文件> -` 或原runner封装。`--ephemeral` 不等于绑定状态，必须先观察真实未绑定起点。创建样本的writer会话和接收会话分开；不改真实会话环境身份、不手写session JSON。只记录受支持正常流程与常见错误；不做恶意篡改、锁/压力或crash注入。

## 4. 停止条件与适用回退点

- Task/gen/branch/checkout不符时，停止该写批次并回原Identity/Ensure；保留当前与并行改动。每次调用 `.trellis/guru-team/scripts/bash/check-task-checkout-boundary.sh --json --task .trellis/tasks/10-27-679-session-continuation`。
- Source/scope真实变化回Clarify与Author；新正常链路差额由R4原owner核定；机制变化重新资格和candidate Architecture，不能自动扩大实现。缺真实producer回原producer，不伪造输出/receipt或从phase猜pass。
- Package失败先定位首失败，修复后仅重跑受影响及必要直接consumer。原生工具、网络或安装依赖不可用，保留准确未验证项，相关AC不能关闭；继续独立不依赖工作。
- 新冲突、shared-current expected-current变化或拟写组合差额回原RDT/Architecture/Check，保仍有效完整条件；不覆盖其他任务贡献，不追赶无关main前进。
- 副作用继续按原边界展示精确目标后处理；当前计划不授权commit/push/PR/merge/cleanup。没有生产、数据库迁移或发布，因此无生产回滚协议；局部代码回退只撤本次明确差额，不revert无关工作。不自动清理caller-owned branch/worktree或隔离证据。

## 5. Delivery Policy（唯一）

Policy 为 `full`。本D1覆盖整体R1–R4与六项验收，无独立延期切片或临时功能限制。完成条件为：本批代码/合同/投影、全部必要package与安装验证、真实主/子接收和standalone恢复证据齐全，RDT最终整合及最终质量/交付链真实完成。原生未运行不算同等替代或部分默认通过。

完整Release/Upgrade多平台矩阵、未实际运行的平台Agent和已有业务安装升级属于明确非本批证明边界，不是把当前AC延期给未来切片。#666通用停顿问题仍由其原Issue拥有。Delivery合并后还须原Completion独立审查整体当前范围；Closure、Finish、Cleanup各自处理实际结果，不由此Policy预填完成。

## 6. Docs SSOT Plan（唯一）

Strategy 为 `delta_first`。原 `guru-maintain-requirements-design-test-ssot` 是唯一语义writer，隔离根为 `docs/requirements-design-test-contributions/679-session-continuation/`。本批不提前写共享README/index或全局版本，不创建空contribution。

当前需要修改的完整知识单元为：`docs/requirements/current/task-delivery-lifecycle.md`（RDT-REQ-LIFECYCLE，接收会话/恢复/展示行为）；`docs/design/current/task-delivery-lifecycle.md`（RDT-DES-LIFECYCLE，原owner和caller分工/诊断）；`docs/test/current/task-delivery-lifecycle.md`（RDT-TST-LIFECYCLE，V1–V6正常场景和证据边界）。Readiness精确接口/recipe仍由原package单写，lifecycle只维护真实关系和本批相关职责，不复制其JSON规格。历史#548/#396及archive证据保持原观察。

原RDT读取完整当前单元及必要关系，以固定B的完整Git来源准备真实requirements/design/test/traceability及唯一proposed-target完整正文；只复制确实受改的完整单元，保所有未被窄替代的条件。新R679/D679/T679身份连接本批行为→职责→场景；现有identity保留。执行结果仅在contribution test记录一次，包含首失败、package/installed/Agent真实结果及未验证边界，原始运行输出留适用runtime，不复制完整日志或授权。

阶段为：implementation完成后原RDT `task_impact_sync(stage=phase2)`准备完整proposed，直接consumer是独立Architecture和原完整candidate Check；实际candidate_checked之后原RDT `promotion(stage=final_integration)`固定真实target并reconcile、写入和readback，随后implementation重新绑定实际after，最终Architecture/Check/committed Review覆盖最终正文。导航只在定位/关系变化时维护，不为普通Issue制造全局版本。若shared-current已有相关变化，原owner合并有效条件并按真实差额补审。

Architecture候选为no-impact：不创建Architecture contribution、ADR或空ledger；后续实际候选边界变化回原Architecture判断。最终文档不得用source/parity冒称安装、原生、业务或Release通过。
