# D1 union 出口诊断设计

## 1. 设计目标、需求承接与内容基线

本方案承接 [本批 PRD](prd.md) R1–R5、AC1–AC3，完整覆盖 [整体要求](../../prd.md)。固定开发/内容基线 B 为用户选定 `main@8d97fe5401345180ce294e2f729ec33071b37f62`；Planning H0 等于 B，PR 目标为 main。最终实现 H 由实施 owner 实测构造，不把基线与目标最新值混同。

独立 Architecture `candidate_assessment` 已正式返回 `baseline_current / no_architecture_impact`。阶段适用 authority 为 `docs/architecture/README.md`（guru-trellis-architecture）、`00-foundation/design-constitution.md`（guru-trellis-design-constitution-v1）、`06-governance/change-contract.md`（guru-trellis-architecture-change-contract-v1）。候选只细化共享确定性诊断，不迁移职责或创建新 authority。

## 2. 当前系统、边界与目标差额

`validate_json` 用 jsonschema Draft202012Validator 和现有 referencing Registry 完整校验；relative refs 由现有 retrieve 读匹配安装文件。`_diagnostic_error` 对 union 按直接错误数选唯一最近分支；`_constraint_diagnostic` 已负责具体字段及不回显值的提示。

本次仅让已声明固定 `exit_id` 的 union 优先使用该身份定位失败分支。没有前序 Delivery。完整校验、CommandError、Author 入口接线、schema 和 lifecycle 不改。

## 3. 来源设计处置（唯一）

来源为 [#766 解决方案及兼容边界](https://github.com/castbox/guru-trellis/issues/766)。

| 原承诺 | 处置 | 具体落点 | 理由、影响与上游处置 |
| --- | --- | --- | --- |
| 已有固定 exit_id 唯一匹配优先 | retain | 第4/6节共享诊断选择 | 直接修复已证实的错误数并列；无上游变更 |
| 使用 schema/相对 ref 已声明常量 | retain | 第4节现有引用上下文/已解析错误树 | 沿现有解析能力，不引入新声明或第二解析器 |
| 唯一匹配后复用字段诊断 | retain | 原 _constraint_diagnostic | 已能定位 mode，避免 Skill 复制 |
| 不能唯一匹配时保持原歧义处理 | retain | 第6节回退至原 best_match/最近分支逻辑 | 不按分支顺序或相似名称猜测 |
| 不改合法性、错误三字段、DTO 与闭合对象 | retain | 第5/7节 | 诊断不成为 route 或 success authority |
| 无新通用推断、自动修复或完整矩阵 | retain | 第8节有限验证 | 保持本项范围和维护成本 |

## 4. 模块、职责与设计取舍

唯一生产改动 owner 为 `trellis/skills/guru-team/runtime/schema.py`。在现有错误选择处加入针对 `exit_id` 常量的唯一匹配步骤。使用现有校验器已解析的 schema/错误上下文和引用能力，读取实际声明，不能按具体 package 或五个已知出口硬编码。必要的小 helper 留在同一中立模块，不增加共享状态、缓存或每个 Skill 的提示实现。

优先复用已经解析的错误树；若需取得引用声明，使用同一 validator/referencing 解析上下文，不另写 URI/path/ref 解析器。最终算法必须能解释真实生产 Author schema 的相对 ref 分支。常量是 schema 事实，只决定展示哪条错误，不证明输入合法或语义 Gate 通过。

保留当前错误数选择作为无唯一标识匹配时的既有路径。单纯展开叶错误后继续按数量排序虽能修复个例，但仍以错误数近似出口身份，故不选该替代。无需分发新 schema 注解、discriminator、branch ID 或通用推断器。

直接回归 owner 为 `runtime/tests/test_public_contract_diagnostics.py`；安装副本由完整源 `guru-upgrade-tools` 维护，不手工覆写受管文件/hash。

## 5. 接口与数据

公开入口仍是 `validate_json(instance, schema_path, field_path)`：有效输入返回，无效输入抛原 CommandError。错误结构固定为 code、field_path、remediation，code 仍为 schema_mismatch，退出码仍由原 command 层处理。

目标无效样例的 field_path 为 `owner_result.output.mode`；remediation 复用原未声明字段和合同定位说明。不输出提交值。成功输出、public input/output schemas 和 source/profile/typed exits 均无字段变更，无新持久数据。

## 6. 状态、顺序、正常与失败流程

1. 读取原 schema，使用同一 Registry 和校验器完整收集错误。没有错误时正常返回。
2. 对待展示 union 错误，按实例现有 exit_id 与分支已声明固定常量寻找唯一匹配。
3. 唯一匹配时进入该分支既有错误树，继续定位具体约束。不能唯一确定时执行原错误选择/歧义处理。
4. 原字段诊断生成位置及说明，抛原错误；不会修改输入或补造出口。
5. 调用方纠正额外字段后重试同一生产校验，只有完整 schema 通过才成功。

没有新状态转换或恢复协议。嵌套 union、无唯一身份及缺失字段继续由原校验与诊断处理。

## 7. 恢复、兼容、迁移与集成

无数据迁移、双读写、旧 API 兼容层或新增依赖。无效输入继续失败，合法输入继续通过。现有 caller 消费原三字段，只有字段位置更准确。

同范围普通输入错误按提示纠正后重试原命令。生产修复与 installed runtime 通过同一完整源 tools owner 同步；未知本地编辑和 sidecar 按原 owner 处理，不手改 manifest。升级/Release 仍是独立验证责任。

## 8. 验证设计

| ID | 要求与入口 | 独立观察与证据边界 |
| --- | --- | --- |
| V1 | AC1，生产 validate_json + 真实 Author semantic-result-2.0 | 先构造 schema 合法的 scope 输出；额外 mode 仍拒绝且准确定位，说明合同/未声明字段且不回显值；仅删除 mode 后通过。同一对象验证修复点，不复制诊断算法。 |
| V2 | AC2/AC3，既有 PublicContractDiagnosticsTests | 复用 nested union/tied alternatives、missing disposition 和不回显输入值回归；保持原三字段错误及拒绝语义。 |
| V3 | R5，原 source/installed validators、dogfood drift 与 sidecar 检查 | 证明本 checkout 的源码/安装投影一致，不能声称外部安装、native 链或 Release 矩阵已通过。 |
| V4 | 原基础检查 | 在内存 compile Guru Python、Bash syntax、marketplace JSON、Task validate、git diff --check；不写字节码。 |

长期回归只补真实生产 schema 的缺口。原回归仍适用，不复制等价样例；无具体未解问题时不追加回退实验或全矩阵。入口接线若改变，另补其实际入口验证。未运行验证不能写通过。

## 9. Canonical 引用、本轮差额与实际未决项

命中 companion-scripts 的 Error Handling/Shared Skill Runtime Dispatcher、quality-guidelines 的 Test And Validation Value/Validation Scope Ownership，以及本批 PRD 第7节来源。共享 RDT 的 local-fix-intake 三层单元描述 Discovery 私有绑定诊断，范围不同，保持其原定义；本次不扩写该能力。精确共享校验合同由 canonical schema.py、现有 public schemas 及回归拥有。

Architecture 已判定无影响，不创建空 contribution/ADR。没有阻塞性需求或设计未决项；实际实现细节须满足同一解析上下文和唯一常量语义。
