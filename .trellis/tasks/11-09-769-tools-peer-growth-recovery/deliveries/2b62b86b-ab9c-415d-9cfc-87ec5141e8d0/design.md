# D2 显式退出位置与冻结源恢复设计

## 1. 设计目标、需求承接与内容基线

承接[本批 PRD](prd.md) 的 R2–R6、D2-AC1–3及整体 AC2–4，补齐实际 #766 原操作恢复。B/H0 为 D1 实际 delivered head `aaf7f939e83c5a5230ecbb9d9f0827fd5c2e97ff`；构造器按真实前序 Delivery 优先选它，不重复 D1。PR 目标仍为 main。

独立 candidate_assessment 已正式返回 `architecture_impact / target_native`。阶段 authority 为 B 的 `guru-trellis-architecture`、`guru-trellis-design-constitution-v1`、ARCH-RUNTIME-LOCATION、ADR-TOOLS-FROZEN-SOURCE-RECOVERY，以及本批待写的窄后继 ADR-TOOLS-RETIRED-PEER-OBSERVATIONS。候选已由 normal、solution 和 root 原 owners 准入；实现、最终规划和现场成功尚未成立。

## 2. 当前系统、边界与目标差额

D1 已交付增长处理及修复 executor/原资产源分离。原 `unchanged_peers` 对冻结字典逐键要求当前枚举仍有同值；#759 正常 Cleanup 后，该位置的五项键整体不再枚举，实际 #766 仍 blocked。

目标是在现有 `recover_frozen_source` 中显式定位已由 AI 核实退出的位置。AI 使用原退出 owner 的实际结果判断正常退出；机器仅校验有限对象关联及当前状态，再沿原 engine 处理。保留同源模式、存续 peer、common/gitdir、原 source/owned freshness 和原 public compatibility 检查。无新 Task、状态机、备份或 C5 平台依赖。

## 3. 来源设计处置（唯一）

| 来源与原承诺 | 处置和具体落点 | 理由、影响与原 owner |
| --- | --- | --- |
| 整体 R2/AC2、R769：原 common/peer 保持，真实变化拒绝 | retain，第4/6节；无新退出例外的调用保持原检查 | 不能把其它真实变化藏到退出位置中。 |
| D1 contract/ADR：所有原观测键保持 | 窄 change，第4–7节；只对 AI 已核正常退出、且机械条件满足的显式位置承接对象终止 | 原当前检查把对象消失当存续值变化；原 Architecture 以完整贡献及新 ADR 维护适用边界，不改 D1 历史。 |
| 整体 R3/R4/AC3：同一操作、原资产/plan/preimages/snapshot | retain，第5–8节 | 原输入不刷新，新 roots 只在本次调用与必要 retry 中流转。 |
| D1 frozen profile、同源 profile 及最小 typed exits | retain 并加性扩展，第5/7节 | 只有当前 frozen profile 接收新定位字段；不新增出口、通用 DSL 或常驻空字段。 |
| #759 精确 prunable 双条件 | retain，第4节 | 新退出校验要看完整 Git 注册，不能把 prunable 过滤结果当正常退出依据。 |

## 4. 模块、职责与设计取舍

canonical `guru-upgrade-tools/SKILL.md` 与 contract 独占 AI 适用性判断：读取原退出 owner 结果、准确位置和原观测，确认该正常退出属于当前恢复边界。此次已实际恢复 #759 原 Cleanup 的同一个 `cleaned`，不是仅从目录缺失推论。没有该依据时，owner 报具体缺口，不自动增加 roots。

`runtime/tools_owner.py` 只接收这批位置事实。对非空 roots：核绝对位置与冻结观测中的 checkout-local pointer marker 对应、不是目标、完整 Git 注册中没有该位置，且该位置路径项本身不存在。完整注册包含 prunable 记录；保留 `peers()` 默认的原 #759 过滤，可窄增一个仅供此校验读取完整注册的内部参数，复用原 parser，不接 C4/C5 或上游新平台。

只把该 root 的已知 checkout-local active/selection 与 installed/source runtime 观测识别为已退出对象。不得凭任意前缀跳过公共状态。对于该模式下未被当前枚举覆盖的其它原文件观测，读取其原路径 state 核同值；原 common/gitdir 真正变化仍拒绝。未被显式退出覆盖的 runtime 观测缺失仍阻塞。原字典与备份不改，比较中只使用调用期集合。

省略或空 roots 不建立退出例外，继续原检查；同源 install/resume/rollback 不获得该例外。新参数薄传原 resume/rollback 的前后保持检查，不复制 public/guru/preset/complete 阶段或原资产 helper。原 `isolated_write_set` 仍核实际 live peer，退出位置不入写集。

选择显式有限 roots，是为了把正常退出判断留给 AI，同时让脚本验证对象事实。自动忽略缺键或以路径消失认定正常退出会混淆职责；接入跨 Task 退出台账增加无关依赖；重建 #759、刷新原 snapshot 或新 prepare 会改变原问题和恢复承诺。

## 5. 接口与数据

`recover_frozen_source` 输入加性支持 `retired_peer_roots: string[]`：省略与 `[]` 都表示没有退出例外；非空项为已核退出的准确绝对 checkout 位置，不能是当前目标或不在原观测中的新位置。该字段不是授权、确认或语义通过状态，不接收退出证明 bundle 或其它 owner 的 checkpoint。

`frozen_recovery_required` 仍携同 profile/action/recovery_ref。只有本次输入实际提供该字段时，retry 才原样携 roots，包括显式 `[]`；省略字段的旧 retry 不新增常驻 `[]`。其唯一 consumer 在存在该字段时复制它；不存在时省略，使用现有 presence-select 语义，不新增 projection DSL。`tools_upgraded`/`rolled_back` 终态无需 roots。

同源 profile 的 schema/含义不变。新 frozen 输入/输出 schema、Interface mapping、consumer schema、examples 和 MIGRATION 成套更新。原 checkpoint schema1.0、`cp.public`、source identity、plan、preimages 和 peer snapshot 均不增加或替换字段。

## 6. 状态、顺序、正常与失败流程

1. AI 读取原失败、原 owner 退出结果、准确 root 和冻结输入，完成当前适用性判断，形成原 frozen input 加必要 roots。
2. executor 读取同一 ref；验证原 root/source/pair/plan、隔离及当前 owned 状态。核新参数所指对象及完整注册/路径事实，不从这些事实生成正常退出判断。
3. 原前后保持检查使用同一调用期 roots。其它原观测保持不变或按真实原路径核同值；不关联的变化继续阻塞。
4. resume/rollback 沿原 engine。`preset` 仍 pending，继续原资产 installer 与原 public operation；`complete` 只验证。rollback 仍先公共兼容，再原 Guru restore。
5. 可恢复失败保 action/ref 及实际提供的 roots 返回同一 frozen consumer；永久 mismatch 返回原 blocked。失败不清空原观测或增加新操作。
6. 目标自身 resolver/installed/native 与 peer 保持通过后才返回工具终态；本批和 #766 的正式阶段由各自原 owner 判断。

## 7. 恢复、兼容、迁移与集成

实际旧 consumer 是 #766 的 schema1.0 原操作。D2 修复 executor 仍从 `cp.source` 加载完整原资产及 helper；原 Source HEAD、内容绑定和 public operation 不变。新字段是一次调用对象定位，retry 由原 consumer 承接，不持久化第二 checkpoint 或重新构造恢复计划。

旧输入省略字段继续原行为。使用新字段的 caller 必须使用含该 schema/Interface/runtime/consumer 的完整 matching 修复包；D1 旧闭合 schema 不被宣称接受新字段。MIGRATION-769 明确切换及既有保留期限：原操作终态且原恢复保留责任结束后，才由原 owner 的明确迁移移除此兼容能力。

D1 已晋升贡献及 ADR 保留。D2 在 Task-owned 子目录制作完整 current proposal 与窄后继 ADR；原 owners 在 candidate Check 后 final_integration 写回/readback，再重绑完整候选执行最终 Check/commit/独立 Review。实际 #766 恢复在 D2 交付后进行，不改其冻结源来安装修复。

## 8. 验证设计

| ID | 条件、入口与独立观察 | 范围 |
| --- | --- | --- |
| V2-1 | 真实 Git peer 在原观测/原 owner begin 后正常移除；公开 frozen 入口携有限 roots 续接，核原 ref/public operation/source/plan/preimages/snapshot 不变 | D2-AC1；SDK/preset/native 若在模块边界隔离须明说，不能代替实际现场。 |
| V2-2 | 省略/[]不建立退出例外；当前仍注册、位置仍在或不关联冻结观测的普通选错准确拒绝；其它存续 peer/common 的原变化回归继续拒绝 | 保留 D1 和 #759 回归；不构造伪造/攻击或压力样本。 |
| V2-3 | 原 frozen retry 的有/无 roots 与显式空数组分支，经真实 producer/声明 projection 消费后都满足 consumer schema，action/ref/字段存在性保持 | 验证接口和直接 consumer，不为修测试新增 DSL、exit 或默认字段。 |
| V2-4 | 原 tools owner 更新本 Task checkout，目标自身 source/installed/native、drift、mode/sidecar 与 Task/config/AGENTS 保持 | D2-AC3；无完整 Release 矩阵。 |
| V2-5 | D2 交付后实际恢复 #766 原 ref/action，核原冻结输入及 public operation，目标自身 resolver/installed/native 可用 | D2-AC2/整体 AC3；原失败保留，未发生不得预写通过。 |

采用未变 D1 工程事实，新增/受影响 guard、入口、retry 与恢复回归实际执行。按质量规范从行为派生断言，足够覆盖后停止追加实验；实际现场失败继续由原 owner 调查，不改样本或把缺口称完成。

## 9. Canonical 引用、本轮差额与实际未决项

沿 PRD 第7节完整 current RDT 与 Architecture 单元；D2 贡献位于 `docs/requirements-design-test-contributions/769-tools-peer-growth-recovery/d2-retired-peer-observations/` 和 `docs/architecture/contributions/769-tools-peer-growth-recovery/d2-retired-peer-observations/`。目标为原 runtime-location 完整单元及 `docs/architecture/adr/tools-retired-peer-observations.md`，不登记共享根索引。

目前没有产品选择或设计阻塞。实际实现仍须证明这条有限输入能贯穿原前后 checks 与 consumer；若复用前提或机制实质改变，回原 Author/qualification/Architecture，不扩大字段或状态。
