# D1 Planning union 字段诊断设计

## 1. 设计目标、需求承接与内容基线

本批承接 D1 PRD 的 D1-R1–R6、D1-S1–S5 与 D1-AC1–AC5，覆盖整体 R1–R7。目标是改变失败诊断的分支选择，不改变合法性或用途。

开发基线 B 与 Planning H0 均为 `0fb7dc9aac817a684c2f95bebb6570061a5ef868`，来自原 Sync 已固定的 `origin/main` Git object。PR 目标是 `main`。实施 Candidate 由原公开 constructor 绑定实际 H 和完整 B..H；B、H 与 PR target 不混用，不因 target 后来前进自行同步或重选 B。

阶段适用 Architecture identity 为 `guru-trellis-architecture`，constitution 为 `guru-trellis-design-constitution-v1/current`；change contract 为 `docs/architecture/06-governance/change-contract.md` 的 `guru-trellis-architecture-change-contract-v1`。真实独立 candidate_assessment 已返回 `baseline_current / no_architecture_impact`：共享确定性诊断内部修正，不改变 owner、single-writer、持久状态或架构决策，无贡献或 ADR。此结果不替代 Wording-current final_plan。

## 2. 当前系统、边界与目标差额

没有前序 Delivery。`runtime/schema.py:validate_json` 使用 Draft202012Validator 和既有 referencing registry 执行完整校验；`_diagnostic_error` 从失败错误树选择解释；`_constraint_diagnostic` 生成字段与约束提示。当前特殊分支只识别 `exit_id`，不能识别 Planning 的 `planning_purpose`。

实际 final-plan 错层错误树中，真实分支的 object-level 错误保留完整 properties const；另一用途分支只有用途 const 叶错误。已解析 union 的分支 schema 本身也有 const 声明。差额是直接复用这些声明定位分支，随后复用原字段解释。

本批只修改 `trellis/skills/guru-team/runtime/schema.py` 和 `runtime/tests/test_public_contract_diagnostics.py`，并由原 tools owner 生成受影响安装副本及 manifest。公共 schema、Skill Interface、workflow、业务 route、成功 DTO 和当前知识权威均不新增职责。

## 3. 来源设计处置（唯一）

| 来源/角色 | 原承诺 | 处置及落点 | 理由、影响与上游处置 |
| --- | --- | --- | --- |
| #847 根因与推荐方案；建议，本批采用 | 复用原共享诊断 owner 与既有 const 声明 | retain；第4/6节的同对象声明选择 | 直接作用于错误选择原因，未采纳 wrapper 或叶计数近似；无上游变更 |
| #847 兼容边界；技术约束 | 完整校验、错误结构、用途与闭对象不变 | retain；第5/6节 | 错误输入继续拒绝，消费者继续使用原接口 |
| #847 方案/已接受评论；明确条件 | 只有声明足以唯一定位时优先，否则原回退 | retain；第4/6节 | 不把未命中统一变成 union 提示，不按顺序猜测 |
| #847 方案/兼容边界；技术约束 | 不硬编码 Skill/用途，不新增注解、解析器或任意推断 | retain；第4节的有界提取 | 使用当前已解析 schema 与原错误 context；无第二来源 |
| #766 PRD 第5–7节；前驱约束 | 原 exit_id、相对引用、嵌套 union、歧义与不回显值 | retain；第7/8节 | 直接演进原实现并复用测试，不保留两套诊断路径 |
| #847 验收；交付约束 | 原 tools owner 同步 source/installed | retain；第7节 | 不手改受管副本；实际写入计划沿原 gate 确认 |

## 4. 模块、职责与设计取舍

**唯一实现 owner：共享 `_diagnostic_error`。** 保留现有 best_match/root/context 分组和最终回退，用通用 const 声明匹配替换 `exit_id` 专用匹配段。诊断匹配只对当前失败 union、同一 instance object 与实际 error groups 工作。

对每个 group，先读取当前 union 已解析的对应分支 object schema 的 `properties.<field>.const`。当分支通过既有相对引用或同对象嵌套 union 展开时，复用错误对象已解析的 `child.schema` 与原同对象 context，取得对应声明；不重新加载或解析引用。只检查当前对象的直接 properties，不遍历无关子对象，不推断 enum、if/then 或任意 schema 逻辑。

每个完整声明集合按该 object schema 的 const 条件一起比较；缺少输入字段不能算匹配。不同已解析备选各保留其自己的声明集合，不能把不同备选拼为一个签名。声明未知、不足或同一集合存在冲突时，不据其选择。只有这些声明足以排除其它 group 并唯一定位一个 group 时，才递归调用原 `_diagnostic_error` 解释该 group；否则直接执行原最少错误分支和 best_match 回退。既有 exit_id 被同一机制处理，不增加并行 special case。

当前真实 Planning aggregate 的 schema_version/profile/stage/planning_purpose const 是输入条件；实现不能写入这些值作为业务分支表。验证器仍拥有引用与合法性，诊断器只解释失败。

取舍：提醒调用方重读 schema 不能改变错误提示；叶计数仍近似用途；Architecture wrapper 改写复制职责；接受错层或删字段掩盖调用错误。此方案不新增 I/O、持久状态、重试或 coordination，只扩展原诊断器已具备的声明读取。

## 5. 接口与数据

原调用为 `validate_json(instance, schema_path, field_path)`。成功返回不变；失败继续抛出 CommandError，`code=schema_mismatch`、原退出码和 `field_path/remediation` 保持。remediation 仍定位原合同，不能回显提交值。字段定位继续由 `_constraint_diagnostic` 单写。

不新增 DTO、schema 字段、discriminator、分支 ID、注解、配置、artifact 或 public output。没有数据迁移。其它 G03 装配问题继续由 D1 PRD D1-R6 的原消费者合同纠正。

## 6. 状态、顺序、正常与失败流程

没有新增持久状态或生命周期转换。执行顺序为：

1. 原 loader/registry 解析 schema，完整 validator 产生错误列表。
2. 没有错误时正常返回，诊断选择不改变成功结果。
3. 有错误时保留原 best_match/root 寻找与 union context 分组。
4. 对可用同对象 const 声明作唯一定位；命中唯一 group 则沿原递归解释其真实字段。
5. 不能唯一定位时沿原唯一最少错误 group 递归；没有该 group 时保留原 best_match，包括真实 union 歧义。
6. 原字段解释生成三字段错误，调用方保持用途并修正真实字段后重试原命令。

final_plan 错层预期为 `input.candidate` 或 `input.design_locator`；candidate_assessment 反向错层同样必须定位实际布局，不能提示另一 planning_purpose。错误仍停在完整 schema 校验，不被转移到业务阶段。

## 7. 恢复、兼容、迁移与集成

失败输入由原调用方修正；不新增自动恢复器、fallback 输出或成功路线。原 exit_id 定位、嵌套 union、相对引用、真实歧义和普通字段约束保留，原 tests 直接检验其行为。旧安装支持不扩张；其它 worktree 不自动采用本次候选。

canonical 修改后加载完整 source-owned `guru-upgrade-tools` 合同，对本专用 checkout preview/prepare/invoke，保 Task/session、用户修改、平台选择与 peer。dirty source 只能使用其 isolated local_candidate 合同，明示 formal_fork_source_lock 未验证，不称 source_locked 或 Release。实际写集、源身份及 command 在执行前单独展示确认。不得绕过原 owner 手改 installed/managed hash。

同步后由目标自身 resolver、installed wrapper/validator 和 drift/mode/sidecar 检验实际结果。没有产品数据迁移、DB 或部署配置变化，不制造回滚协议；若受管更新中断，沿原 frozen operation 恢复，不重准备或清理他人资源。

## 8. 验证设计

| ID | AC/层级 | 入口、输入与独立观察 |
| --- | --- | --- |
| V1 | AC1/AC2；生产 schema 组件 | 从当前真实示例构造两种合法 Planning 布局，调用生产 validate_json 和 aggregate 4.0。合法通过；只移动路径产生错层时捕获非零/schema_mismatch及真实字段，拒绝另一用途提示；仅修层级再通过 |
| V2 | AC3；共享回归 | 运行现有 public_contract_diagnostics tests，保留 Author exit_id、Architecture 字段、嵌套 union、相对引用、真实歧义、缺失/多余字段及不回显值。const 未唯一命中时原 fallback 不退化 |
| V3 | AC4；实际安装 | 原 tools 同步后，目标自身 runtime.validate_json 加载 installed aggregate/示例执行相同双向场景；source/installed package checks、drift、受管 modes与递归 sidecar 检查 |
| V4 | AC5/质量 | Python 内存语法、Task validate、diff check；原工程自检和独立完整 B..H Review 核对全部 diff 与必要未改消费者，确认 R7 边界 |

V1 是长期行为回归，放入现有测试模块，不复制诊断算法计算期望。只新增两种真实错层的独立缺口。已有只读错误树调查已回答“声明能否从现有对象取得”，不再增加同目的实验、回退旧代码或固定红绿次数。对出现的新 reach/因果疑问才做有界实验。以上均是计划，未声称修复后通过；组件和本 checkout 安装不证明外部业务、完整生命周期或 Release。

## 9. Canonical 引用、本轮差额与实际未决项

需求、设计、测试 authority 的具体关系沿本批 PRD 第7节；此处不更改其 Intake、绑定诊断或分发职责。直接 schema 合同与 production runtime 是本轮差额，测试仅补双向缺口。Architecture 独立候选结果为 no impact，不创建 contribution/ADR；最终 Wording-current final_plan 仍待原 owner。

原 RDT owner 将在 Phase 2 验证 Docs Plan 的实际影响与 no-change 依据；不预建空贡献或直接编辑共享导航。没有阻塞性产品选择；实现中若发现已解析声明不足以承接本方案，停止该扩展并回 Author/Architecture，不转成任意推断框架。
