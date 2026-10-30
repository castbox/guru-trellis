# 发现阶段 fitness 出口：D1 设计

## 1. 设计目标、需求承接与内容基线

本批承接 slice PRD V1–V4、D1-S1..3；整体 V5 仍由业务 owner 后续验收。development baseline B 为显式选择的 main@00b1b6f29a5ad7f6591f0ef43573ef8ba798222b；首次 D1 无前序交付，Planning H0 与 B 相同。内容范围固定 B..实际 H，PR 目标为 main，后续不随 remote ref 变化移动 B。

阶段权威为 B 的 docs/architecture/README.md、00-foundation/design-constitution.md、06-governance/change-contract.md。独立 candidate_assessment 实际返回 baseline_current/no_architecture_impact：候选修复既有合法阶段遗漏，不改变决策、owner、持久化、路由及兼容退出。该结果只供本次方案写作；final_plan 仍需当前设计独立承接。

## 2. 当前系统、边界与目标差额

input/semantic-result 接受 implementation_discovery；runtime/invoke.py 保留 stage、身份和回归字段并选择 Delivery fitness output。该 output 的非 Planning 枚举以及 interface 当前 fitness-regression-5.0 consumer 缺此值，delivery-1.0 的相应 consumer 也缺少。聚合 output 通过 $ref 承接 Delivery schema。

目标仅在真实 output 和这两个受分发 consumer 的对应 Delivery 非 Planning 分支补入 implementation_discovery。保留原 Planning 分支、final_integration 分支、required/additionalProperties、字段及现有 router，不改运行时分类或绕过校验。

## 3. 来源设计处置（唯一）

| 来源 #690 条款 | 原承诺 | 处置与具体落点 | 理由、影响和上游处置 |
| --- | --- | --- | --- |
| 目标1/正常复现2 | 原发现阶段正式 fitness 出口 | retain；第2/6节原 stage 正式 wrapper | 直接修正拒绝位置，无 stage 替换 |
| 目标2/根因证据 | runtime output、interface aggregate/current consumer 完整承接 | retain；第2/4节三个 schema 及聚合 $ref | 当前接口直接演进，无长期 adapter |
| 目标2/5 | 身份/root/refs/route、公有 id 与原合法语义保持 | retain；第5/7节 additive enum | 无破坏 API，无迁移需求 |
| 目标3/验收V4 | canonical/dogfood/platform 同步 | retain；第4/8节现有 apply/reapply/drift | 不改 installer，不扩大 Release 矩阵 |
| 正常复现1/4/5 | 有效 fixture、原失败边界及受控 owner 证据限定 | retain；第8节 wrapper 回归 | 不依赖业务值，不冒充独立语义或现场证明 |
| 交付边界/V5 | 源码可先交付，业务 fresh 审核后整体验收 | retain；第8/9节及 implement Policy | 本批不写业务仓，不宣称现场恢复 |

全部为原要求的直接落点，没有 change/reject 或未决上游处置。PRD/implement 不复制本矩阵。

## 4. 模块、职责与设计取舍

产品改动 owner 为 guru-maintain-architecture-baseline package。修改 schemas/public-output-delivery-fitness-regression-1.0.schema.json、consumers/workflow/fitness-regression-5.0.schema.json 和 consumers/workflow/delivery-1.0/maintain-architecture-baseline-fitness-regression.schema.json 的目标枚举。检查 interface 聚合 $ref 与当前引用，必要差额仅限本次合同。

tests/test_contract.py 复用现有 installed_fixture、真实 Task/Delivery/candidate 和正式 invoke transport，增加可检错的正常组合回归。用现有 preset apply 同步完整 installed package 与 declared platform readable projections。主会话拥有规划和交付；实施 Agent 拥有上述 source/test 及必要受管投影。没有新的脚本、owner、双 reader、恢复状态或公共字段。

## 5. 接口与数据

原 delivery_task_impact_sync(stage=implementation_discovery) → runtime 输出 fitness_regression → interface 聚合输出 → fitness-regression-5.0 consumer → guru-architecture-baseline-check-router。保留 delivery_key、planning_root、task_locator、regression_refs、return_route；return_route 枚举仍为 implementation/check。新增值仅补齐原 stage，required 字段和普通 schema/身份错误保持。无业务持久化数据变化。

## 6. 状态、顺序、正常与失败流程

有效 fixture 的原输入、owner result、候选先通过原验证。正式 runtime 投影同一 stage 到 stdout；修复前枚举拒绝，修复后接受并保留回归信息。将实际 stdout 传给三个声明 schema，原 AI router 根据 return_route 交还实施或检查；自动化结构结果与 AI 消费说明分开。身份过期和缺失仍沿原 validator 返回原错误，不扩大负例矩阵。

本次没有新增状态转换。生产代码修改后，经 apply/reapply、候选 Architecture/Check、合法回 implementation、no-change final integration、重新绑定实际 candidate，再最终 Architecture/Check、commit、完整 committed Review、Refs-only PR 与合并。

## 7. 恢复、兼容、迁移与集成

这是当前公开合同的 additive enum 修正，直接更新真实受控 consumer。现有支持范围不缩窄；无新 API id、wrapper、fallback 或数据迁移。旧合法 Planning/phase2/final_integration 与 return_route 保持。delivery-1.0 文件按当前 interface/分发关系同步，不扩展历史 API。managed copy 由 canonical apply 恢复；sidecar 用实际 before/after 判断逐项处理，保留无关内容。

## 8. 验证设计

T1/V1：先新增有效 fixture 的 wrapper 回归并在修复前运行，记录 stdout schema_mismatch；再同样输入执行修复后 wrapper，两种 route 均原 stage 返回 fitness_regression。测试不跳过身份/候选/输出边界，不删除合法样本。

T2/V2：对该实际 stdout 验证 runtime 选中 Delivery schema、interface 聚合 schema 和当前 fitness-regression-5.0 consumer，同时验证受分发 delivery-1.0 consumer；断言 key/root/refs/route 原样。主会话明确消费输出路由含义，自动化 owner result 仅证明确定性承接，业务实际路由由 V5 复验。

T3/V3：运行当前 Architecture package contract suite，覆盖既有 Planning/phase2/final_integration 与 ordinary stale 样本；必要时在现有测试添加本次改变涉及的最小对照。失败按实际归因处理，不能弱化 assertion。

T4/V4：受管 Python 内存 syntax 检查；source/installed skill package validator；apply --repo . 后 reapply 和 check-dogfood-overlay-drift；核对受影响 schema bytes/mode、声明平台及 sidecar。现有真实 installed fixture 与 dogfood reapply 足以验证该 schema 分发，除非实际证据缺口需要，不新增 clean 安装或完整矩阵。

受控回归、静态/安装、独立 AI reviewer 与业务 V5 分层报告。V1–V4 结果不证明现场 block、业务 reconcile 或部署成功。

## 9. Canonical 引用、本轮差额与实际未决项

必要依据：Architecture distribution 的 ARCH-INT-001/006、当前 package interface/runtime/schema；RDT 的 docs/requirements/current/knowledge-maintenance.md、docs/design/current/knowledge-maintenance.md、docs/test/current/knowledge-maintenance.md 定义 canonical package 单写精确 API、no-change 和候选/最终 Check 责任。本次恢复既有合同承诺，无需变更这些共享能力单元、Architecture 决策或导航；无空 contribution/ADR。

必要工程规范为 .trellis/spec/workflow/skill-package-contract.md、data-contracts.md、quality-guidelines.md，以及 .trellis/spec/preset/installer.md。实际实施和审核先读取适用正文。源码范围没有待决项；V5 获取 owner/条件见根 PRD 第8节。
