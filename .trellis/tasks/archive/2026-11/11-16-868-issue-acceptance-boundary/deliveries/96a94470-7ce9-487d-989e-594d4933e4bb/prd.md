# D1 Issue 验收边界与持续去重需求

## 1. 整体来源与术语

本批公共 key 为 `868-issue-acceptance-boundary / generation 0 / 96a94470-7ce9-487d-989e-594d4933e4bb`，planning_root 为 `deliveries/96a94470-7ce9-487d-989e-594d4933e4bb`。整体 accepted_scope 定位 [根 PRD](../../prd.md)，authority revision 为 `sha256:a038296a32b5a78b474d5ac9dd1d8e9a381aff6ecd02679014120d927d67aad0`；本批 scope_ref 选择 AC1、AC2，覆盖全部 R1–R7。

Direct Source 为 [#868 完整正文](https://github.com/castbox/guru-trellis/issues/868)，角色为要求；旧创建评论仅为历史，不覆盖当前完整正文。当前 issue-content、quality-guidelines 和原 Skill 合同是实现与兼容依据，不自行扩大需求。验收切面、结果与支撑证据定义沿根 PRD 第1节，本批不另建范围 authority。

## 2. 整体与本批目标、非目标

D1 完整交付 #868：在所有受支持创建入口首次写入前形成合理精简验收，并在任意后续审核及正文写回前持续排除无依据、跨界或重复义务。验收止于提供方自身可独立证明的边界，不沿调用链升级为消费方 E2E。

本批覆盖共享规范、原 owner 薄引用与原门禁、必要入口一致性、去敏示例、现有 eval、实际 Agent 行为、受管采用和 RDT 必要差额。保留合法技术交付、明确失败/安全/兼容及自身合同真正需要的集成证据。

不恢复 Wording，不新建审核阶段、semantic script、wrapper、DTO/schema/账本、固定条数/测试层级，不重做全部生命周期，不执行完整多平台安装或发布矩阵；不将边界外消费方接入变为本批交付条件。

## 3. 本批起点、前序结果、依赖与剩余责任

本 Task 尚无前序 Delivery。开发基线 B 固定为 `b85ea7bdf80db97ba8aceb1298dd61ed5f1ebeec`，来自 main；PR 目标独立选择 `castbox/guru-trellis:main`。当前已有 #818 的最小充分规则和 #850 后的原 owner 路径，Create Issue executor 原样写入且只有隐藏 marker 差额。当前并未实现本次完整语义方法。

D1 计划覆盖整体全部范围，不安排后继切片。整体 Completion 仍须检查实际 AC1/AC2、交付结果与原关闭/归档职责；Planning、分发或 commit 不能代替。外部业务仓采用、正式发布和完整安装矩阵不在本批，不假称已验证。

## 4. 本批调用方、场景与流程

- **D1-S1 创建：**Agent 经普通、Issue-only、现成/复制草稿或已有 Task 阶段入口进入原 Clarify→Readiness→Create Issue。先明确边界、区分结果/证据、删除多余义务，再审核最终待写正文。不合规则回原 owner，首次创建动作之前保持未创建；正文实质变化只刷新受影响原判断。成功创建后的输出丢失只恢复原对象。
- **D1-S2 后续审核：**任意相关原 owner 在 workflow/standalone、独立审核、换 Agent 或恢复会话中面对当前有效范围与旧证据。先判断拟新增义务的依据和独立价值，不成立就在本轮输出前移除，不形成 Finding、风险、返工或 gate；每次写回前核完整正文，防止改名恢复。
- **D1-S3 技术交付：**对外合同可由组件入口及足够证据独立证明时，不要求真实消费者接入或 E2E；多个入口只补必要差异。源码、配置、协议、文档及数据状态均可作为合法结果。
- **D1-S4 真实遗漏：**已有充分覆盖复用，内部明确承诺仍有证据缺口时只补定向检查；原始范围真实遗漏和已确认联合交付仍能修复或安排必要集成，不能为精简删掉。

## 5. 完整行为、条件与约束

本批完整执行整体 R1–R7：
- 目标、消费者和权责决定最外沿有效切面；不能外推，也不能用粗糙结果遮蔽自身承诺。
- 验收对应目标且有独立判断价值；删除后不影响任何必要承诺的条目合并/删除。目标归属不是充分条件，替换实现启发也不能推翻来源约束。
- 单元/集成/E2E/联合验收只是备选证据，不逐层重复。有效证据不因阶段推进、换 reviewer 或信心不足而重跑。
- 不凭防御推断、未来用途、完整性偏好追加范围；消费方尚未接入不阻塞提供方，不能转成风险或强制 follow-up。
- 所有创建入口和后续原 owner 都实际消费原共享规范；待写正文未通过合理精简前不得创建，后续不先输出阻塞或写回再补救。
- 现有真实承诺缺口沿原 owner 最小修复；真正范围变更回原 Clarify，不让设计/测试/审核记录自行授权扩张。
- Issue 方法在 Clarify-owned issue-content 单写；跨阶段验证规则在 quality-guidelines 原小节单写，review-sufficiency 与原 owner 仅薄引用。
- 保留原 public API、typed exits、职责、只读边界、源权限、创建/刷新/恢复与 secret redaction；不把 AI 判断放进确定性脚本或固化为关键词扫描。
- 受管副本由原 tools/installer owner 匹配更新，不手抄；保留用户改动、Task/session 和原 sidecar 处理。

#868 中共享规则归属、既有 owner/出口及原执行器边界属于规范性约束；本批 design 第3节维护唯一来源设计处置，PRD 不重复矩阵。

## 6. 本批验收、验证方式与未决项

**D1-AC1（整体 AC1；D1-S1–S4）：**使用现有 Skill eval 与最少正常场景观察实际原 owner：两目标草稿含可归属目标的测试型条目、重复层级、无依据扩张及跨界 E2E，同时保留合法技术结果、既有有效证据和真实遗漏/联合交付。创建前先修订、回审最终正文；未通过时无创建。后续独立或恢复审核拒绝叠加及其阻塞后果，而真实缺口仍可定向修复。观察完整正文、动作顺序、原出口和回程，不凭条数或预填 pass 判断。不同路由作必要代表观察，等价入口复用路由证据，不构造乘积矩阵。

**D1-AC2（整体 AC2）：**canonical 规则、受影响 owner 引用、dogfood 和声明平台完整 matching 投影一致；经原 owner 完成采用及适用 drift/sidecar 定向验证。语义、静态、安装及外部效果分别报告，安装成功不代替 D1-AC1。未执行边界如实保留。

无必要未决范围选择。当前尚未实施或完成行为/采用验收，不将后续验证预填为通过。

## 7. Canonical 引用与本轮差额

- `docs/requirements/current/issue-content.md`：R153/BEH153、R818/BEH818、R819、R850 的当前内容/创建/只读/分层证明责任；本次补充验收边界、全入口写前及全轮持续约束。
- `docs/design/current/issue-content.md`：D153/CON153、D818/CON818、D819/D850 的单一方法、薄引用、原 executor 和受管采用；本次沿原归属扩展方法，不新建路径。
- `docs/test/current/issue-content.md`：T153、T818、T819、T850 的行为与分发证明边界；旧原生观察保留历史，本次增加自身实际结果，不能借旧 pass。
- `docs/architecture/README.md` 及其 constitution/change-contract：保持 Markdown 控制面、脚本事实边界与唯一 owner；实际影响由独立 Architecture candidate_assessment 和 final_plan 判断，PRD 不预填 no-impact。
- `trellis/skills/guru-team/packages/guru-clarify-requirements/references/issue-content.md` 与 `trellis/presets/guru-team/spec/workflow/quality-guidelines.md`：本次实际行为方法的两个责任源；Review/Skill 只定位原文。

Docs SSOT 的候选与晋升由原 RDT owner 承接，不由本 PRD 修改共享导航或制造空贡献。
