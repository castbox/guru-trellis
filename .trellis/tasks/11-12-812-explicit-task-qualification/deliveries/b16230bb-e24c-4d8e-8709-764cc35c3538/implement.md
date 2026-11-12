# #812 D1：实施与验证计划

## 1. 输入与引用

本批输入为根 PRD 的真实 accepted_scope、本目录 PRD 的 DREQ812-01～05/DAC812-01～04、design 第1节固定 B 和第3节唯一来源设计判断。完整读取 design 第4～8节及关联条件后执行，不从摘要或文件存在推断足够。无前序 Delivery；#813 只作为已完成创建能力前置。

必要 canonical：三个 guru-qualify-* package 的短 applicability、SKILL/contract/Interface/公开 schema；共享 qualification_facts.py 和 delivery_projection/adapter.py；docs/{requirements,design,test}/current/qualifier-applicability.md；Architecture 完整 qualifier-applicability、design-constitution/change-contract。公共 I/O 按 skill-package-contract.md 的 Public Skill I/O And Private State，实际测试按 quality-guidelines.md 的 Test And Validation Value/Validation Scope Ownership。原安装路径用 guru-upgrade-tools 完整 canonical source 合同。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置、owner 与真实文件 | 完成观察 |
| --- | --- | --- |
| I812-01 | 已接受当前 Planning 后，实施 owner 再读 trellis-before-dev 的适用完整 specs 和清晰写作规范；每批 source/test/task 写入前运行 check-task-checkout-boundary.sh | 同 Task/gen/key、当前 C4/checkout；无 unrelated 改动被覆盖 |
| I812-02 | 三个 package：为 design 第5节七类 schema 新增版本2.0、aggregate3.0，更新 Interface schemas/public_contracts、runtime/common.py 的 PROFILE_SCHEMAS、公开示例与实际受控 eval/test 输入；四类非 Delivery 输入保持 | current 输入明确带完整 key，旧 path/id/bytes 和旧 aggregate 保持；current 不接旧 shape |
| I812-03 | 共享 runtime/qualification_facts.py 在原 verify_current_facts 内承接 key、原 active checkout/model 与 context 当前选择，统一规划目录/身份；不复制到三个包 | 原合法无 context 事实成功，有 context 冲突及真正 stale 仍失败；原输出/语义算法不变 |
| I812-04 | 原七类 caller 的 canonical SKILL/reference/示例、必要 workflow routing 说明、MIGRATION-812.md、package/spec/README 的实际受影响说明 | key 来源是实际原 owner/current；原 typed consumer 和调用期上下文有明确续接，phase2 recovery 不升级为新阶段 |
| I812-05 | 新 runtime/tests/test_qualification_identity.py 与三包既有 contract/runtime、受控 fixture/eval：采用真实 public owner 准备正式事实；单元夹具只证明其声明边界 | 覆盖 V812-01/02 的独立断言；不手工补被测 producer 的结果，不以字符串自证 |
| I812-06 | 原 tools owner 从完整 canonical source preview/prepare 后展示精确冻结写集并按原边界执行，更新本 checkout 受管 packages/runtime/workflow/spec/声明平台；不可手抄 | 目标自身 source/installed/parity/native 可用、必要 reapply/drift/sidecar 处理；Task/session/peer 与 common pointer 保持 |
| I812-07 | 实施协调者执行实际 explicit-task caller；正常子 Agent 经原 Identity/Ensure/Bind/Selection 用真实官方 context 执行适用 qualifier 与原 caller | V812-03 的真实 typed outputs、普通错误和后续动作可核；原始失败/边界保留，不设置环境键 |
| I812-08 | 原 RDT 和 Architecture owner 在完整实施/工程验证后整合第6节完整拟写并 readback；随后原 TaskCommit 形成本地 H、固定 B..H、begin_check | 内容含所有真实 after，无 precommit independent pass；独立完整 Review/Check 审实际已提交候选 |
| I812-09 | 原 Delivery Review/readiness→Publish→Merge，整体 Completion→Closure→acceptance_finish→Finish→资源 disposition | 逐个原出口和实际 Git/GitHub readback；每次 merge 前暂停，由协调方处置 |

必要的受管同步以原 installer 的输出为准，不直接编辑受管 manifest 声明的全部平台安装副本。原 public output 不增加仅供审计/恢复的字段；旧历史归档、其它任务和 #808 均不在写集。遇到真正大于3000行的非生成源码改动，先按原政策做有界机械拆分评估，不扩大到无关历史。

## 3. 验证入口、输入与预期观察

1. V812-01：用已解析 managed Python 执行三个 qualifier tests/test_contract.py、tests/test_runtime.py，以及新增共享身份集成测试；先定位各既有 fixture 的声明边界，再迁移其输入。新/旧 schema 各自独立有效、交叉替代拒绝，七类 current projection 正确，四类非 Delivery 行为保留；不新增全阶段笛卡尔乘积。
2. V812-02：共享集成测试经原 public Task Creation、Scope/Delivery 创建及 Identity/Ensure/Bind（无 context）建立真实对象，再从三个 scripts/invoke.sh 观察本次事实路径。Planning、generation 或选择发生正常变化后，旧输入预期返回原 stale 错误；断言要求的行为，而非重写目标算法或预填目标结果。这里证明确定性链，不冒充实际 AI 判定。
3. V812-03：协调者原 explicit-task 路径与正常子 Agent 的官方 context 分别跑真实适用集合。AI 自己读取当前 authority、候选和合同并选结果，再调用公开 wrapper 和消费唯一 router；观察三个 qualifier 的成功，以及原合同定义的非通过返回。非通过观察采用 design 第4节已拒绝的“跳过 Planning”替代：真实 Author/root 应返回机制修订，原 caller 移除该替代后继续完整显式身份方案；其余未变路由采用现有覆盖。普通 mismatch 的输入来自实际状态变化或对旧已知对象的普通调用失误，不能人工伪造 artifact/hash/context key。保留所用 Task/key/profile、真实 stdout、错误及 caller 的后续动作，结果只在原必要 Test 汇总，不制造资格 ledger。
4. V812-04：运行原 source/installed check-skill-packages.sh；本 checkout 更新后运行目标自己的 resolver 和原 public discovery/qualifier entry。运行 trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh 与适用 ownership/sidecar 检查。原 tools 操作恢复/reapply 沿同 frozen plan；不为本项跑完整 Throwaway/升级/Release 矩阵。
5. V812-05：内存 Python syntax、改变的 JSON/shell 校验、git diff --check 和必要 package/consumer 回归。原 docs integration/readback 后提交完整候选，独立 reviewer 先做 Architecture before/after，再覆盖 Check/Branch Review 全范围。main 的实际合并/终态是后续外部事实，不预填通过。

managed Python 入口和测试环境沿当前 provider 的 public resolver/说明，不能以系统依赖安装替代缺失完整 provider。实际命令、返回码和未验证边界由执行后 Test 记录。已有有效证据可采用，只补实际改变命中的缺口。长期回归与临时诊断分开；追加反事实实验只在尚有明确未解决因果/缺陷到达问题时做。

## 4. 停止条件与适用回退点

- 身份、generation、C4/C5、registered checkout、official selection 或 required upstream 输出失效：停在其原 owner，保留同 Task/Delivery，不重建映射或制造 key。
- 来源/范围或实质机制改变：回原 Clarify/Author/Architecture，刷新依赖判断；同机制已适用资格不因换阶段重跑。
- 旧输入缺 key：拒绝，原 caller 从其真实身份重装；不能从 inventory、digest 或邻近字段猜补。旧 schema 字节不改。
- source/installed/projection 或 sidecar 失败：原 tools owner 同操作恢复；不先手抄受管文件再补门禁。精确安装回退单独检查原 preimage 与 Task/session 兼容，不 reset Git 或纳入后续业务改动。
- 公开行为验收未触达、原 caller 没有消费结果、context 分支不可得或必要 mismatch 未证明：保留具体缺口，不宣称整体验收通过。设施反复失败时重评原复现方式，不无界修设施。
- 必要事实与行为证据充分后停止额外重复验证。无产品数据迁移或生产部署动作；本地 source 修订保并行改动，不能擅自回退用户内容。commit/push/PR/merge/Closure/Finish/cleanup 仍分别执行精确副作用边界。

## 5. Delivery Policy（唯一）

Policy 为 full：D1 覆盖本 Task 全部 R812-01～07 与 AC812-01～04，没有延期到 D2 的实现或兼容责任。独立交付条件是七类输入、共享事实、三 qualifier/原 caller、迁移、canonical/installed/平台投影与 V812-01～04 必要证据同批完成，能由 readiness 发布一个 Refs-only PR。

Delivery 合并后仍由同 Task Completion owner 判断整体 accepted_scope；Closure、Finish/目标 main 可达归档与资源 disposition 保留各原 owner。它们不是已完成的实现证据或新增 Delivery。#808 的发布和完整矩阵在本项之外；本项不得以其它任务代为兜底自己的明确公开验收。

## 6. Docs SSOT Plan（唯一）

strategy 为 delta_first。原 RDT owner 在 docs/requirements-design-test-contributions/812-explicit-task-qualification/ 准备 requirements.md、design.md、test.md 与 proposed/docs/{requirements,design,test}/current/qualifier-applicability.md 的完整 after。直接修改现有能力完整单元，保其 identity、REQ/DES/TST-793 与条件调用，补 R812/D812/T812 的显式对象、公开迁移、事实校验与实际验收边界；不新增第二 current 能力页或共享索引登记。Test 在执行后区分确定性、实际 AI/公开 caller、安装和未验证项，不能互相代证。

Architecture 使用本批真实隔离 contribution 和 proposed/docs/architecture/03-domains/qualifier-applicability.md，加 ADR-EXPLICIT-TASK-QUALIFICATION 的完整拟稿。保 ARCH-DOM-QUALIFIER-APPLICABILITY 原三 owner/调用职责，说明本次显式对象及 MIGRATION-812 如何窄替代旧输入承诺；不修改 root/system/ownership/ADR index。Planning final_plan 审真实候选文档和 contribution/ADR，不能提前晋升 shared current。

两原维护 owner 的直接 consumer 是实施候选与独立 committed reviewer：批准 Planning、完整实施及真实工程结果后，于本地 TaskCommit 前 final_integration 重读 actual targets、整合完整定义、处理真实重叠并 readback；只返回 integrated_pending_review。提交后独立完整 Review 判断真实 before/after，publication/Completion/Finish 只消费当前 reviewed_promoted 或合法 no_change。canonical Skill 精确接口规格继续为其唯一正文，RDT/Architecture 引用，不复制全部 schema。旧历史和其它贡献不重写。
