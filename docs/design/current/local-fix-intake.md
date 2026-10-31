# 局部修复 Intake 的 owner 与诊断设计

Identity：`RDT-DES-LOCAL-FIX-INTAKE`；D692/CON692；适用基线 `6a65ec8afe6d180850760b3b2edf3f94be6e3b20`。本完整单元在原 final_integration 后为 current；精确内容由 Git revision 与 locator 定位。需求：[R692/BEH692](../../requirements/current/local-fix-intake.md)；测试：[T692/SC692](../../test/current/local-fix-intake.md)。原 [生命周期](task-delivery-lifecycle.md)、[JSON 载体](json-input-carriers.md) 和 [知识方法](knowledge-maintenance.md) 的通用职责保持。

## D692-01 / CON692-OWNERS：保留调用图，在原 owner 内减少重复

selector 依据实际行为影响选择原 route。Create Issue 读回正式 URL/完整正文后仍交原 Sync，再进入 Discovery→Clarify→Wording→Readiness；其 created DTO 不携带调查缓存。Discovery 核新身份、完整 live 正文、当前 base 与已有事实的 revision/差额/相关性，保留 fresh duplicate/history 和独立判断。它只在当前事实确实缺失或变化时补命中调查，不重新广搜仍适用内容。

Clarify 直接使用当前 Discovery public output 和可核验的完整来源，自行判断 intent、role、disposition、scope，不借读 producer 私有结果，不重复询问证据已回答的问题。Author 依现有模板区分整体要求、本批要求、design 与 implement，复用已接受定义的必要引用，完成当前正文责任；来源处置仅在 design 唯一位置维护。Wording、独立 Architecture、Approval、展示接受与 Activation 顺序保持，各阶段仍作自己的判断。真实事实失效回原 producer/最早 owner；同源普通装配恢复不新增确认。

这直接细化既有 step-local Markdown，避免新增恢复层、跨 Skill capsule 或统一缓存。成本限定为原合同与现有比较的维护；若真实调用图、公共 I/O 或恢复责任改变，必须回原规划及兼容合同，不能用本单元直接授权。

## D692-02 / CON692-BINDING：拆分已有确定性比较

Discovery `runtime/common.py` 在现有等价判断中定位首个差异。mode、change_input、base_observation、history_preview 和 result_identity 分开检查；嵌套对象/数组指到实际差异键/位置，派生摘要只能指到其绑定字段。base observer 保持 `current/refresh_base/blocked` 及原错误 code/status，只细化 mode/repository/selected-base/branch/ref 的字段与原 Sync 恢复说明。

context_request 目标失配保持 `stale_identity` 和 `return_identity.target_locator`，回原 Discovery/Clarify 的当前目标入口。pre_task 不增加固定目标比较；live body 没有新 provider 自动校验。JSON 读取先由原 shared reader 完成，不把载体/语法错误改称身份失配。

## D692-03 / CON692-ERROR：把诊断交给当前调用者

record 保留原 CommandError。check 的失败 receipt 保留 status/typed_exit/reason，仅 additive 放入三字段 diagnostic。invoke 在原被收窄为 blocked 的分支将三字段写 stderr，stdout 保留原唯一 typed DTO；成功/refresh 和原直接参数/schema/目标错误均保原形状。直接 consumer 是当前 Discovery AI，无新 public DTO、独立状态、持久诊断或跨 owner authority。

字段/恢复文本只含固定位置和操作说明，不输出正文、expected/actual 值、bytes 或 exception。读取命令输出时捕获完整 bytes 后一次解码，或用保持边界的 streaming decoder；绑定失配不证明某一种根因。当前 owner 重读实际 public input、Sync transition、history 与完整输出后重建最小 authoring，再原 record→check→invoke；不补改派生 digest、producer 或旧 pass。

## D692-04 / CON692-DISTRIBUTION：受管传播与质量责任

现有 canonical packages、commands/errors、README 定位与实际 consumers 同批演进，通过原完整 preset 同步 dogfood/选定平台。apply/reapply、source/installed、drift、mode 与 sidecar 证明本 checkout 的实际采用，外部安装和完整升级/Release 矩阵分别保留边界。无业务 API/数据/支付迁移，无新安装要求；Architecture 无影响时不造空 ADR。

原 RDT owner 先准备隔离完整 proposal，经原 candidate Check 后 final_integration 写入与读回；实施重绑全部 actual after，最终 Architecture/Check、精确 TaskCommit 和独立完整 B..H Review/readiness 覆盖实际内容。测试策略与实际结果保持各自单一来源。来源见 [追踪](../../requirements-design-test-contributions/692-local-fix-intake/traceability.md)，精确参数/接口仍由 [canonical packages](../../../trellis/skills/guru-team/packages) 独占。
