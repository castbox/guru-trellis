# #778 新增范围的 Delivery 归属判断：整体需求

## 1. 来源与术语

| 来源 | 章节与角色 | 本 Task 用途 |
| --- | --- | --- |
| [Direct Source #778](https://github.com/castbox/guru-trellis/issues/778) | R1–R3、实施边界、最小验收；要求与约定约束 | 整体范围来源；当前正文无评论补充 |
| [#734](https://github.com/castbox/guru-trellis/issues/734) | 当前正文 R1 与责任边界；相关来源 | 核对归属要求的重叠；不承担其其它要求，不关闭或改写它 |
| [Task/Delivery 当前要求](../../../docs/requirements/current/task-delivery-lifecycle.md) | 身份、切片、唯一 Planning、返工、整体完成；current authority | 保留原生命周期和整体责任 |
| [需求决策当前要求](../../../docs/requirements/current/requirement-decisions.md) | R-DEC-01..04；current authority | 保留事实先查、真实选择才问、具体委托承接及无授权持久化 |
| `313d80215f65777fc70893a90c6d8dce8005d6dd` | 已选定的 origin/main 基线；实现证据 | 读取当前 Clarify、Author、Creation、workflow 和范围测试；PR 与完成验证目标为 main |

Task 拥有整体 accepted scope。Delivery 拥有一个独立切片的规划、实现、验收与交付。整体接受新增责任与分配到当前切片是两个判断。

## 2. 背景与问题

当前流程已有同片返工、后继 Delivery、撤回及 full/partial/staged Policy。Clarify 拥有来源与整体范围，Author 拥有规划正文。现有合同缺少新增差额进入当前切片前的集中归属判据，容易把 Task 扩围直接变成原片完成条件扩大。

#778 记录的历史案例是首页自动轮播被要求继续原 Task 后，执行者自行解释为同 Task/Delivery。该案例不证明旧提交已经可发布，也不证明拆片能够解决当时的锁文件接续阻塞。本次只修订流程合同，不验证历史事故修复或成本下降。

## 3. 目标与非目标

目标是在原 Clarify 中先判断新增差额归属，再由原阶段 owner 执行实际切片返工、撤回或后继接续。当前片不随整体范围自动膨胀，也不强制所有新增要求拆片。

范围包括原 Clarify、Author 的 step-local Markdown、必要的既有路由引用，以及受影响 canonical/dogfood/声明平台投影的原 owner 同步和差额验证。

不新增 Skill、公共 DTO 字段、typed exit、状态、分配账本、授权记录、自动切片算法或固定规模门槛。不修改 Trellis 上游或 Candidate 算法。不承担 #734 的预算、消息限额、规模、QA 分片、设备治理及整体效果重放；#765 的接续阻塞独立处理。不新增混合 Git 回归、真实 Agent 运行评测、完整流程重放或多平台升级/Release 矩阵。

## 4. 真实调用方、场景与流程

| 场景 | 调用方、前置与触发 | 行为与可观察结果 |
| --- | --- | --- |
| S1 独立新增能力 | 当前阶段 owner 接收到同 Task 的新增能力，来源允许分阶段，新增能力可独立后置 | Clarify 判断依赖和独立交付条件；新增能力保留在整体剩余责任。Author 只更新当前片必要来源、边界、依赖和 Policy；当前片实现/验收不自动加入该能力。后继实施时才由原 Creation 建立下一片 |
| S2 原合同缺陷 | 当前片实现或规划遗漏了原合同要求 | Clarify 按原合同修正判断；原阶段 owner 同片返工，Author 刷新受影响规划及原门禁，不误判为必须拆片的新功能 |
| S3 立即替换 | 新来源要求立即替换旧行为，旧片原行为已不再被接受 | Clarify 判断旧片有效性；原 owner 沿合法返工或撤回/重新规划接续，旧行为不能按旧合同发布 |

三个场景是合同语义审核输入，不是预写 Agent 行为结果。共同顺序是读取完整来源、判断差额和依赖、修改实际切片。

## 5. 行为要求

### R1 原 Clarify 判断新增差额

完整读取新增来源，以原已接受需求、行为与验收合同为比较基准。区分原合同缺陷/遗漏修正、替换旧行为的要求及独立新增能力。只要求同 Task 不能推断为必须同 Delivery；来源明确要求当批共同交付时保留该选择。

判断说明当前候选尚缺什么、新要求与其依赖，以及后置后是否保留合法的独立交付条件。只有存在真实业务范围或交付时序选择才询问。已有具体委托按原交互合同承接，不增加固定询问或审批轮次。

### R2 原阶段与 Author 承接

原合同修复、不可分依赖或必须立即替换的要求，沿原同片返工与受影响规划审核。可独立后置且来源允许分阶段的能力进入同一 Task 的剩余责任；当前片只刷新必要来源、边界、依赖与 Policy，不自动加入新增实现/验收。后继实施由原 Creation 创建下一片，不并行制造第二个 current。

新要求使旧片无效时，沿原撤回/重新规划，不能发布不再被接受的行为。Author 在现有 Delivery PRD 与 implement 的唯一 Policy 中承接结果。full 仅表示当前覆盖选择，不代表未来所有 Task 新要求自动加入原片；实际边界变化时用已有 partial/staged 语义说明剩余责任和整体 Completion 条件，不能只换标签。

### R3 内容与职责真实

新增内容进入实现前优先确定归属。内容已经混合时先判断实际可分离性；不能用新 Delivery 身份、少选路径或把未交付提交当作已交付前序规避完整范围。沿现有 Candidate/base 与 Review 合同检查当前内容及后继依赖。

Clarify 独占归属判断；当前阶段 owner 执行合法返工/撤回；Creation 拥有后继创建。workflow 只承接路由，Approval 和 Delivery Review 在原职责中核验独立交付，不新增拆片审核步骤。

## 6. 约束与依赖

复用现有 public input/output、typed exits、scope_ref、PRD、Policy 和固定 B..HEAD 范围。AI 判断充分性、依赖和归属，脚本只承担已有确定性执行、记录与校验。不得把归属规则编码为自动判定脚本。

受管副本经原安装/升级 owner 同步，保留当前 Task/session。按实际差额检查 package、投影和 dogfood drift，处理真实 sidecar；不手工覆盖受管副本。没有数据/schema/运行部署变更，因此没有相应迁移或部署要求。

#734 是范围归属的相关上游，其其它要求不构成本次前置。现有正常路径、普通错误和 stale/mismatch 约束保留，不扩张攻击、竞态或异常非功能加固。

## 7. 可观察验收与验证方式

| 验收 | 要求/场景 | 入口、输入与预期结果 | 证据边界 |
| --- | --- | --- | --- |
| AC1 | R1–R3 / S1–S3 | 原审核 owner 对修订合同逐场景判断：S1 留后继责任；S2 同片修复；S3 旧行为不能发布 | 证明合同承接，不证明真实 Agent 全程行为或历史事故已修复 |
| AC2 | R1–R3 | 对照 Clarify、原阶段、Author、Creation 和现有路由，确认当前片边界、唯一 Policy、剩余责任、整体 Completion 及真实选择才询问均有唯一 owner | 不新增生命周期、拆片审核或公共数据 |
| AC3 | R2–R3 / 分发约束 | 按实际修改运行 package/声明投影/原 owner 同步和 dogfood drift 检查；实际副本与 canonical 一致，无未处理差额 sidecar | 不等于完整多平台 upgrade/update/Release 验证 |

后续实现、Check、独立审核和 PR readiness 使用这组验收。业务 Delivery PR 仅引用 #778；合并后的整体 Completion/Closure 由原 owner 独立判断。本执行段发布 PR 后停止，等待协调器处置合并。

## 8. 实际未决项

没有阻塞整体需求写作的未决产品选择。技术落点、最小命中检查和 Docs/Architecture 影响由原 Author 与独立 Architecture 在 Delivery 规划中确定。上述验收尚未执行，不预填通过。
