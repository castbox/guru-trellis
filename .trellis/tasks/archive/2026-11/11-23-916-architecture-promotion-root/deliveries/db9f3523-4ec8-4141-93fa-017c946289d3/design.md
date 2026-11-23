# D1 独立架构单元晋升设计

## 1. 设计目标、需求承接与内容基线

本批承接 [Delivery PRD](prd.md) 的 R1 至 R4、AC1 和 AC2。开发基线 B 是 Intake 从起始 `main` 正式读取的 `8604558695dfd9d8ea2181406a87ece70d9eea63`。规划时工作树 HEAD 与 B 一致。PR 目标是 `origin/main`，交付内容范围由实施时的固定 B 和候选 HEAD 确定。

架构权威为 [Architecture Baseline](../../../../../docs/architecture/README.md)、[Design Constitution](../../../../../docs/architecture/00-foundation/design-constitution.md) 和 [Architecture Change Contract](../../../../../docs/architecture/06-governance/change-contract.md)。本 Delivery 的独立 candidate_assessment 返回 `baseline_current`、`no_architecture_impact`。原 owner、共享权威、公开接口与候选绑定保持原合同。

## 2. 当前系统、边界与目标差额

原 Architecture owner 在 final_integration 读取完整拟写，使用文件工具写入和读回。包内 `runtime/promotion.py` 的 `check_promotion` 在写后绑定已审目标与实际内容、写前候选和写后候选。现有稳定根合同允许真实根变化，并要求独立单元留在所属路径。

既有规则在写前处理拟写目标。三个正式基点样本来自同一临时提交。两项独立晋升均保留根 README，合法查找合同变化写入根并读回。A、B 首次候选绑定失败，随后正式 wrapper 返回整合结果。具体边界和重跑材料见[基线复现记录](research/baseline-evidence.md)。写后诊断确认 fixture 预写的同身份目标可通过客观绑定。

## 3. 来源设计处置

| 规范性来源 | 原承诺 | 处置与落点 | 理由及上游 |
| --- | --- | --- | --- |
| #638 和原 promotion 合同 | 原维护 owner 读取真实目标，普通文件工具写入，读回后交原质量链 | retain；第 4 至 7 节复用原 profile 与手工写入职责 | 变更落在同一 owner 内，无上游机制变更 |
| #711 与 current-knowledge 的稳定发现条款 | 根入口保持身份，独立单元写所属正文和真实关系；根合同实际变化才维护根 | retain；第 4 节写前检查每项目标，第 8 节观察两类结果 | 继续使用责任目录、稳定 ID 和必要关系 |
| #916 期望行为 | 普通误列必须在实际写入前处理，合法根变化必须写入读回 | retain；第 6 节定义两条处理路径 | 沿原 owner 与现有顺序实施 |

## 4. 模块、职责与设计取舍

原 Architecture owner 在写入前判断每个实际目标的必要性。普通独立单元晋升保留稳定根。真正发生的身份、范围、状态、位置、查找合同或必要关系变化仍由同一 owner 写入。现有普通、恢复和合法根变更入口沿同一语义职责。逐项读取了目标选择、expected-current、目标文件和写后绑定路径。

三组实际结果未定位到根误写。规范的有效主体、目标和顺序已经具备，受管副本中没有发现遗漏。当前没有可提交的实现方案。若后续出现受支持的失败入口，先核对实际触发和写入记录，再定位原 Architecture owner 需要修订的决策位置。写后脚本继续按原职责检查实际文件和身份。

## 5. 接口与数据

原 `promotion` 6.0 或 `delivery_promotion` delivery-4.0 接收真实当期权威、候选和原 sync target。原 AI 的本轮拟写及修订保留在当前执行上下文。既有 `promotion_targets` 只描述经过审查并实际写入读回后的目标，保留原结构。正式入口保持 `baseline_current / integrated_pending_review` 和现有不通过出口。现有 consumer 继续使用实际 after 候选与 before authority。

## 6. 顺序、正常与失败流程

1. 读取基点、适用权威、完整贡献、各目标和必要关系。核对受影响的查找消费者。
2. 在第一项写入前审查完整拟写集。普通独立单元的摘要误列先裁掉。根自身存在实际变化时核对保留理由和受影响关系。修订后再检查整个写集。
3. 按当前入口重读 expected-current 和各目标，核对源条件未变化。仅写通过审查的完整内容。
4. 读回全部实际目标，重新检查适用性并用原入口绑定结果。普通独立样本另外对照根字节和身份。错配与冲突回原晋升 owner，必要条件变化回原规划或要求 owner。

## 7. 恢复、兼容、迁移与集成

复用原部分写入恢复。用当轮审查后的同一写集区分 pending、completed、conflict。非冲突 pending 才可继续。正式结果丢失时，从仍匹配的原意图和实际内容恢复。正常的根迁移保留既有 before/after 身份绑定。既有安装通过原 tools owner 用完整匹配来源更新受管副本。该更新无需迁移公共数据。

## 8. 验证设计

| 验证 | 入口与输入 | 预期观察 |
| --- | --- | --- |
| V1，AC1 | 同一固定临时仓库提交的两个独立 working copies。两次均从正式 delivery_promotion 走原 owner。一份拟写包含仅用于更新版本摘要的根 README，另一份仅含自己的独立单元与必要关系 | 首份可见原 owner 在写前修订拟写目标。两次实际 diff 分别包含各自单元和必要关系。根字节和身份与基点相同。两份执行互不读取对方写入 |
| V2，AC2 | 同一正式入口，拟写新增一个真实的职责发现范围及其中的完整单元 | 原 owner 确认可观察的查找合同变化，写入根和所属单元，读回且正式入口返回实际结果 |
| V3，支撑 V1/V2 | 目标包既有 promotion wrapper 测试，加匹配来源、受管副本和相关平台投影检查 | 文件字节、候选绑定和正常合法例外各按原合同观察。安装证据用于核对实际加载版本 |

在临时仓库固定 commit、输入、provider 版本、执行入口和可重跑命令。保留 Agent 的实际关键调用与 Git diff。host 仅准备上游 fixture、样本输入和观察，原 owner 形成当轮语义结论。现有定向测试可以证明写后包装层，原 owner 的写前执行仍由实际样本观察。正式样本覆盖指定正常场景。无需以全平台矩阵证明本次行为。

## 9. Canonical 引用、本轮差额与实际未决项

[R711 和既有知识组织约束](../../../../../docs/requirements/current/knowledge-maintenance.md)、[D711 的写入和定位合同](../../../../../docs/design/current/knowledge-maintenance.md)、[知识维护测试单元](../../../../../docs/test/current/knowledge-maintenance.md) 与 [Architecture 根权威](../../../../../docs/architecture/README.md) 是本批适用来源。差额限于把当前规则落到原 owner 的目标审查和结果读回。独立候选评估为 no_architecture_impact，后续由实际 final_plan 确认。三组基线样本与适用边界见[基线复现记录](research/baseline-evidence.md)。继续实施的前置证据是可重跑的当前根误写或有实际消费者受影响的当前遗漏。
