# 必需正文完整读取

Identity：`RDT-REQ-REQUIRED-CONTRACT-READING`；检索别名：`R848`、长文读取、两层预算、截断补显。原语义 owner：`guru-maintain-requirements-design-test-ssot`。来源为 [Issue #848](https://github.com/castbox/guru-trellis/issues/848) 全文及其[接受评论](https://github.com/castbox/guru-trellis/issues/848#issuecomment-6891318170)；固定实施基线为 Git `0fb7dc9aac817a684c2f95bebb6570061a5ef868`。本单元描述该来源的已接受要求；实现、安装和审核状态由各自真实结果确定。

知识状态：已接受要求；本文的整合观察截止于提交前，正式质量状态读取原 Task/Delivery 结果，不由本文预填。

本文的 repository-relative locator 从仓库根解析。设计为 `docs/design/current/required-contract-reading.md` 的 D848，测试为 `docs/test/current/required-contract-reading.md` 的 T848。完整操作方法唯一位于 `trellis/presets/guru-team/spec/workflow/companion-scripts.md#reading-required-contracts-in-full`，运行副本为同源 provider 的 installed 小节；本单元不维护第二份工具示例。

## R848-01 / BEH848-FULL：确需范围和实际完整性

workflow、standalone、恢复及子 Agent 的当前 AI owner 必须实际获得并理解判断所需全文。先确认确需材料，再复用当前完整、适用的原生注入和已读正文；提高预算不扩大范围。父会话的已读标记不替代子 Agent 的正文。成功退出、raw stdout、路径、行数或参数存在不能独立证明模型可见完整。

## R848-02 / BEH848-BUDGET：两层请求和实际容量

工具能承载完整材料时，先显式配置足额预算直接读取。内层覆盖每条命令预计输出；外层覆盖同次编排全部输出及载体开销，不能只取最大一条。超过缺省10,000不自动强制拆分。

Codex 初始请求采用内层20,000、外层24,000，按实际材料调整。更大数值是调整示例，不是固定阈值、必经档位或宿主容量保证；不修改宿主全局配置，不假设其它工具提供相同参数。参数位置、原生 API 和示例由唯一短方法承载。

## R848-03 / BEH848-CARRIER：正文载体

`exec_command` 读取 Markdown 时显示 `.output` 正文，避免无必要的完整回执转印。其它工具消费其实际正文载体，不套用不存在的字段。载体选择不能替代预算；同次合并仅用于本次确需且总量能完整容纳的材料。当前 AI 检查实际返回和文件尾。

## R848-04 / BEH848-RECOVER：按缺失层恢复

超过实际容量、无法可靠预算或调整仍截断时，再按文件或连续相邻范围拆分，直到所需全文及实际文件尾，包括无末尾换行的正文。固定行数不证明完整。名义值已足而仍截断时保留事实，不盲目抬值或据参数宣称成功。

仅外层截断且完整原结果仍在平台既有跨调用 owner 内存中时，优先从原内存缩小批次补显，不重跑读取。结束隔离调用中的 `const` 不是跨调用内存。内层已缺失、原文丢失或内存不可用时补读缺失正文；范围不明则足额全文或连续覆盖。既有 `store/load` 只在真实暴露时使用，消费后释放；不新增服务、文件缓存、ledger 或持久读取状态。

## R848-05 / BEH848-ENTRY：短导航和同源 provider

原 AI-first、workflow 与受影响平台入口在首次必需长文前定位原短方法，不先要求整本 companion-scripts。直接独立 Review 入口先确定完整 source/installed provider，再读同源短节、写作规范及审核方法；target authority 单独读取。导航不复制方法，也不把 Task 创建或完整 workflow 变成独立操作前置。Python 仅分发导航，AI 保有读取充分性判断。

## R848-06 / BEH848-STDOUT：保留原结构化结果合同

producer JSON、recorder/checker receipt 和 typed exit 继续在原 owner 内存中消费完整原始 stdout。prose 的分段补显不能替代它们的原 owner 恢复，也不能按显示片段重建结果。显示不全不重放 mutation，原失败保留。

## R848-07 / BEH848-ADOPT：受管分发与行为证据

原安装 owner 同步 canonical 和必要 installed/dogfood/声明平台投影，验证引用、reapply、drift、mode、用户内容及 sidecar。实际新 Agent 从直接独立入口采用须另行观察；链接或静态通过不能替代。源码、安装及 Agent 行为各自限定结论层级。

本能力不新增读取器、公共 Skill/I/O/schema/出口或 gate，不改变原生命周期与审核职责。宿主内部显示限制原因、任意容量、业务付费调用、完整多平台升级/Release 矩阵及其它业务安装采用不属于本次完成声明。原共同审核充分性 R717 保持，详见 `docs/requirements/current/review-sufficiency.md`。
