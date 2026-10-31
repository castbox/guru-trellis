# 局部修复 Intake 与一致性诊断

Identity：`RDT-REQ-LOCAL-FIX-INTAKE`；定义 R692-01..04 / BEH692。来源：live [Issue #692](https://github.com/castbox/guru-trellis/issues/692)，适用基线 `6a65ec8afe6d180850760b3b2edf3f94be6e3b20`。隔离 proposed 经原最终整合后成为此完整 current 定义；精确内容由完整 Git revision 与 locator 定位。前驱有效合同为 [Task/Delivery](task-delivery-lifecycle.md)、[JSON 载体](json-input-carriers.md) 和 [知识方法](knowledge-maintenance.md)，本单元仅新增下述具体行为。

## R692-01 / BEH692-ROUTE：实际影响选路

对尚无相关 formal Task 的局部修复，原 selector 依据当前范围、受影响消费者、风险和所需验证选择现有 route。购买引导的资格或展示不自动等同价格、扣费或支付协议变更；UI 表象也不独立证明低风险。已有 Task 回其当前生命周期。高置信度有界低风险仍可按原合同自动选路；证据不足时只提出真正必要的问题。真实范围/风险变化回原 owner，不以新身份或换 mode 绕过。

## R692-02 / BEH692-REUSE：事实适用性与当前判断

草稿创建成正式 Issue 后，原 Sync/Intake 顺序保持。Create Issue 读回正式身份和完整正文；Discovery 读取该新 target、当前 base 及差额，并完成当前 duplicate/history、证据充分性和 Gate。已完整读过且当前内容仍可用的调查事实，经当前 owner 核 revision、base 差额和目标相关性后可继续使用；不因进入下一 owner 从零广搜同一事实。旧 target pass、producer 私有结果或摘要均不能替代当前结果。

Clarify 消费当前 Discovery output 与完整来源，先用证据解决可回答的问题。已清楚的同范围事实不重复访谈或重装配 producer 结果；仍亲自判断当前 intent、source role、disposition 与 scope。Author 以当前整体来源写 Task 要求，以已接受整体定义展开 Delivery 的目标、边界、起点、行为与验收；不重复访谈、从零调查同一代码，也不省略各自正文和方案责任。

每个原 owner 明确触发、须重读的差额、仍适用事实、须亲自重做的判断与下一 consumer。缺失完整内容、真实 source/target/base/scope 变化回最早受影响原 owner。相同范围且无新副作用的 mapped 修复自动继续；真实选择和资源、commit、发布、merge 等独立边界保持。授权仅在当前对话，不持久化。

## R692-03 / BEH692-DIAGNOSTIC：原 Discovery 入口

JSON 成功读取后，原 record/check/invoke 对当前输入、base 观察、history 和结果绑定的不一致，在确定性可判定范围定位首个实际字段或 evidence 类别。诊断说明重读对象、原恢复 owner 和支持的重入入口。base 前进回原 Sync；dirty/错误 branch/authority 缺失仍按原分类处理；context_request 目标失配保持原直接错误。普通 live Issue 正文仍由 AI 完整重读，本项不新增 provider 比较。

失败仍失败，公共 input、错误 code/status、typed exit 和成功 DTO 保持。check 失败保留原 status/typed_exit/reason，并 additive 提供 `diagnostic={code,field_path,remediation}` 给当前 Discovery AI；invoke 原收窄为 blocked 的错误在 stderr 给同一诊断，stdout 保持原 DTO。原参数/schema/直接目标错误保留原 error 形状。JSON 载体或解析失败继续由原读取层诊断。

payload/result digest 差异只证明绑定不一致，不能据此断定 UTF-8 根因。重新读取完整输出后由原 Discovery 重建其最小 authoring，再经原 record/check/invoke；不局部改 digest、producer 或旧 pass。诊断不回显 expected/actual 值、正文、原始 bytes 或 OS exception。

## R692-04 / BEH692-DISTRIBUTION：职责与证据边界

AI 拥有 scope、风险、充分性和恢复判断；脚本只验证事实。canonical 原 owner 是行为来源，匹配 preset 同步 dogfood 和实际选定声明平台。已有安装保留原 managed provenance、用户修改与 sidecar 规则；源码通过不证明外部采用。公共调用图与原子能力保持，无新 Skill、跨 Skill digest authority、通用审批链或长期审计缓存。

沿正常开发、Check、独立 Review/readiness 和适用 reapply 验证；失败/SKIP/环境阻塞不作通过。业务 #372 仅为脱敏历史案例，业务代码、测试、数据、Task/会话只读；当时安装、路线、根因和净节省时间保持未知。不开专项 replay/A-B/native eval、额外安装或完整矩阵，不新增恶意篡改与并发加固范围。

关系：[D692/CON692](../../design/current/local-fix-intake.md)、[T692/SC692](../../test/current/local-fix-intake.md)。精确 canonical 调用与数据定义由 [packages](../../../trellis/skills/guru-team/packages) 单写；来源/替代边界见 [追踪](../../requirements-design-test-contributions/692-local-fix-intake/traceability.md)。
