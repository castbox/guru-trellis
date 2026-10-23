# ADR-035：活动续接与scope两次承接

状态：accepted。来源：#657的[隔离贡献](../contributions/657-workflow-continuation-conflicts.md)；target_native。当前执行合同由canonical workflow/packages单写，采用边界见[MIGRATION-657](../../../trellis/presets/guru-team/MIGRATION-657.md)。知识接受不等于installed/native、Task完成、部署或Release通过。

## Context

官方Task2/Delivery API1及Guru原身份/阶段owners已经存在，普遍初始created写入前置、选择后无条件initial Author及旧scope DTO/profile却与其冲突。正式rebind后的活动任务不能使用原初始创建恢复取得资格；仅改clear名称也不能补上scope根写作及acceptance顺序。

## Decision

初始Task Creation和同创建区间输出恢复保留原checked created及精确identity/binding/ledger条件。既有活动Task通过明确来源、当前TaskId/generation、合法common-dir binding、唯一checkout及实际stage owner继续写入，不以原机created/private runtime为前置，不放宽初始validator或恢复原机ownership。

Delivery Creation/Selection的created DTO、schema和exit保持。其现有唯一consumer重读同key的公共current selection、generation/root与phase；仅planning中真实尚需初始requirements且符合Author入口才进入delivery_initial_review；其余均交唯一continuation的实际未完成义务，包括已有planning的适用Author/Wording/Architecture/Approval或当前approved到Activation。缺失/过期输出回原producer，不能从phase重启初始Author。保留key、phase、规划和适用结果；created与phase均不是Planning、Check、Review或readiness通过。真实缺口回原owner，不重置阶段或创建替代对象。

scope修订先由原Clarify判断，pre-Author scope_ready2.0交scope-only Author写根PRD；实际scope_requirements_ready locator及原selection进入Clarify acceptance。仅该owner审查AuthorityRef并accept_scope，含task_key的post-acceptance scope_ready才允许当前stage合法rework/stop。revised/no_change/withdrawal_required均保留顺序。无current Delivery根据义务显式Creation/Completion，不为withdrawal造空切片。

原Identity/Establish/rebind/Ensure/Bind、阶段语义门禁、公共writer和终态owner保持。Discovery/Review不要求退役metadata branch/status；standalone verifier旧输入拒绝后只给合法standalone准备或pinned旧在途owner，不恢复current Finalizer。

## 精确替代与历史边界

窄替代ADR-011内旧Task development-status activation、旧checkpoint/Finalizer恢复路由；保留workflow continuation唯一authority、原producer恢复及upstream入口ownership。窄替代ADR-023内private4/scope_ready1、固定旧Author profile和in_progress resume；保留先判断后写作及Author唯一writer。补全ADR-024下created consumer与scope两次承接，保留官方Task2/API1、独立Delivery、原语义门禁、Refs-only/Closure/Finish等责任。历史决策和frozen schema保留原字节意义，不作为current fallback或旧pass转换输入。

## Alternatives、迁移与后果

新增phase字段/store会重复公共事实；重置所有选择到planning破坏历史；放宽初始恢复掩盖不完整创建；仅重命名clear会跳过根PRD/acceptance。均不采用。没有新Skill、脚本router、DTO、状态机、授权记录或双读层。

matching workflow/preset/packages/consumers为唯一切换单位。旧在途已成副作用先由原producer恢复；真实scope/依赖/候选变化回最早owner，只刷新适用门禁。旧格式维护由原tools/upgrade owner处理，不批量变换无关历史或绕过apply预检。源码、deterministic、installed、actual Agent及外部边界分别记录在[#657唯一Test](../../requirements-design-test-contributions/657-workflow-continuation-conflicts/test.md)；最多一个代表clean安装不承担全平台Release矩阵。
