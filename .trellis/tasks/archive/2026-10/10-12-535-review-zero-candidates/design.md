# #535 设计：原 Review 边界支持空候选集合

## 设计对象与现状

Branch `review-gate-7.0.schema.json` 和 `archived-review-gate-1.0.schema.json` 将candidate_classifications设为minItems1；`runtime/common.py:validate_gate`用 `not refs`再次拒空。Delivery `semantic-result.schema.json`同样minItems1，其validator已有unique refs与finding/proposal引用集合校验。

正常原Branch fixture在正式Task Commit后由fresh独立reviewer完整审查，真实空classifications在recorder schema validation阶段失败；无checkpoint或pass。旧no-defect示例只证明非空rejected，不表达真正零候选。

## 单一机制

原位演进现有owner，不新增路径或adapter：

1. 原完整语义审查先发生；AI形成实际candidate集合。没有候选时三个qualifier无合法输入，跳过其调用，完整dimensions、Architecture、Docs、truthfulness与route判断仍必需。
2. 有实际候选时按既有qualification顺序，root只接收eligible refs；所有witness/真实引用保持。
3. 两个current Branch schema与Delivery semantic schema删除该数组非空下界；required/type/items/unique与版本/出口不变。
4. Branch validator明确检查list类型及每行唯一ref，移除空refs拒绝；之后继续执行所有引用校验，不因空集提前return。空known集合下任何语义candidate disposition引用仍失败。
5. Delivery validator不新增自动route逻辑；既有schema+unique/ref+dimensions/conclusions/policy/payload/live facts充分性校验照常运行。空集合不赋予ready。
6. 示例中的正常无候选使用[]；真实非空rejected有具体观察而不是no-defect占位。test/eval调用原owner wrappers，避免仅mock/schema成功冒充语义或installed证明。

这是现有字段合法值域增加，非空payload继续有效；无public output更改、无新状态、无dual-read。Branch pinned5/6是historical inventory，current runtime原stale拒绝保持。archived1是current只读profile，因实际共享validator而同步，不能遗漏。

## Consumer inventory

| Surface | 原责任 |
| --- | --- |
| branch_review initial/fresh_final | 原完整range review；finding-fix后fresh final条件保持 |
| base_continuity | 原old/new base pair、candidate tree、bounded scope、continuity_passed保持 |
| archived_review | 原completed archive、live PR/base/head及read-only两出口保持 |
| Delivery semantic/gate | 十维、conclusions、真实findings/proposals、Refs-only payload与最小DTO保持 |
| Branch passed→Delivery input seed | 原task/commit/base投影，无classification字段外泄 |
| three qualifiers | 既有nonempty输入和内部owner不变，只实际候选调用 |
| preset/platform projections | canonical apply/reapply，thin discovery无第二内循环 |

## 方案取舍

选择原约束放宽并保留余下validator。单改schema无法解决Branch二次拒空；强塞no-defect混淆候选语义；空集qualifier出口会扩大三个公共API；新wrapper绕gate会丢freshness和原生命周期。均不采用。

## Authority、复杂度与持久化

起始current RDT `.86/active`，Architecture `.84/active`；设计constitution、change-contract与Guru public2.0由独立Architecture owner先读取。原语义责任与状态模型不更改；设计不预设其impact结论。

code_subtraction：去掉空集非空限制与虚构候选，保留真实引用、既有出口和current profiles。新增tests只检测不同正常路径，不增加生产机制。docs_ssot_subtraction：step-local canonical唯一行为源，RDT贡献及serialized successor保存实际delta；历史immutable。owner-private按原生命周期消费，不写审查账本、用户授权或qualification缓存。touched non-generated files超过3000行触发机械拆分评估。

## 验证设计与实际证明边界

定向unit/contract通过生产logic原wrapper验证真实committed fixtures：零候选、非空rejected、有finding、缺必需evidence、正常stale；Branch active/final/continuity/archive分别验证scope-specific结果。空集带孤立finding的普通owner construction mistake必须继续失败。

真实语义链路由各stage完整审查后提供AI authoring，original record→check→invoke结果才是formal出口。post_owner fixture与unit不是独立AI semantic proof。当前task的fresh最终完整Review和Delivery评估提供真实零候选正式链路；非空观察/有效finding使用可审阅的正常fixture与qualification，不改旧#292现场。

通过一个完整干净Codex installed环境安装canonical preset，使用原任务/branch/control与public wrappers。执行apply/reapply与drift，逐个报告.new/.bak。官方Trellis marketplace/preset为长期源头，更新冲突保护保留；本任务仅定向投影/可恢复性，不声称完整upgrade/Release矩阵。
