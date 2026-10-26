# D3：补齐 README 正式归档恢复说明

## 1. 整体来源与术语

本 Delivery 属于 Task `656-release-v070-guru6-preparation` 的 generation 2，公共 scope_ref 仅选择整体 `AC2`。整体 authority 为 [Task PRD](../../prd.md)，revision 为 `sha256:564f3c7d001c1728bba8a99cf7fab004c33f86139d480c6ea9bb59928f8dbcfc`；本批不修改它。

| 来源 | 章节、角色与本批用途 |
| --- | --- |
| [#656](https://github.com/castbox/guru-trellis/issues/656) | 安装来源与文档收敛、准备与发布行为；要求。公开说明须与当前已交付合同一致，准备结果与正式发布分开。 |
| Task PRD | R3/R4、AC2；要求。限定本批公开文案责任。R5–R8 的质量、收尾及证据边界继续适用。 |
| `README.md` | 已归档任务复审；当前待修正文案。 |
| `trellis/skills/guru-team/packages/guru-reactivate-task/SKILL.md` | Task2、selected formal schema1、共享归档与后继、公共操作及旧状态分流；设计约束。 |
| `trellis/workflows/guru-team/workflow.md` | 正常完成归档的 Reactivate 段；设计约束。指定正式 schema1 已属现行能力。 |
| `trellis/presets/guru-team/MIGRATION-669.md` | 明确入口与旧消费者、调用接续、安装验证边界；设计约束。保留原 clean-base profile 和原 owner。 |

Task2 指当前公共 Task schema 2.0；正式 schema1 只指原 Reactivate 合同明确支持的固定兼容 family，不包括任意旧格式或人工历史归档。

## 2. 整体与本批目标、非目标

当前 README 将正常归档恢复限定为符合当前上游 task schema 的对象，遗漏现行 workflow 和 Skill 已支持的正式 schema1。维护调用方可能据此把合法正式归档错误分流。

本批只修正顶层 README 的该段，准确说明两类正式归档沿原 Reactivate owner 和匹配公共 SDK 恢复；它不新增能力。保留退休人员字段、人工历史、未完成 closeout 和旧 Finalizer 的既有分流。没有 runtime、Fork、公共 I/O/schema、workflow、preset、其它 README 或历史数据改动；不执行业务安装、生产操作或完整安装矩阵。

## 3. 本批起点、前序结果、依赖与剩余责任

D1 版本与文档准备已由 [PR #672](https://github.com/castbox/guru-trellis/pull/672) 交付，D2 existing caller 修复已由 [PR #674](https://github.com/castbox/guru-trellis/pull/674) 交付；原公共 Delivery 结果及各自规划完整保留。gen1 正常归档由 [PR #675](https://github.com/castbox/guru-trellis/pull/675) 持久化。本批从该目标基线上的未修正文案开始，不把前序门禁当作本批通过。

本批依赖现行 Reactivate 和匹配公共操作的既有定义，不重新实现或验证其完整工程能力。#649 当前已关闭；原失败样本及未验证边界保留，不新增 #649 责任。本批交付后，整体准备仍须由原 Completion、reference-only Closure、Finish 和精确 Cleanup 收尾。最终新候选的完整 Stage 2 发布门禁仍归原 Release owner，准备与收尾不能代替它。

## 4. 本批调用方、场景与流程

| 场景 | 调用方、前置条件与触发 | 要求的说明与可观察结果 |
| --- | --- | --- |
| S1 正式归档恢复 | 维护 Agent 阅读 README 判断正常已完成归档的入口 | 当前 Task2 与原合同选定的正式 schema1 均指向原 Reactivate owner；优先核验并继续合法后继，无后继且资格满足时才经匹配公共操作保持同 TaskId 并严格增代一次，同操作恢复不重复增代。README 不要求为正式 schema1 伪造旧 Completion/Closure。 |
| S2 旧状态分流 | 同一读者遇到退役人员字段、人工历史、未完成 closeout 或旧 Finalizer residue | 原拒绝、独立 maintenance、原 Finish/pinned-old/逐案处置边界继续明确；没有“全部 schema1 可恢复”的扩大解释。 |

## 5. 完整行为、条件与约束

- R1 / S1：用最小文字补齐两类正常正式归档的准入说明，保留现有 Reactivate 合同链接。完整资格仍由原 owner 核准确历史、source、终态、当前后继和匹配 capability；README 不成为第二资格判定或公共 parser。
- R2 / S2：保留该段现有否定、例外与分流语义。人工历史、带退役人员字段的旧归档和未完成旧链不能借新句进入普通 current lifecycle；不改历史归档或数据。
- R3 / S1–S2：本批只改变顶层 README 的说明。既有 RDT、Architecture、workflow 和 Skill 已正确定义该能力，不为留下记录创建空 contribution、共享 promotion 或新测试。规范性来源的唯一设计处置由后续 design 第3节承接。
- R4：保留整体 R5–R8 的两个完整独立 Review 及原 owners。具体有界恢复顺序只在后续 design 第9节集中定义；既有代次的 pass、例外或第一轮恢复 carrier 不成为当前正式 full_review。

## 6. 本批验收、验证方式与未决项

| 验收 | 对应要求/场景、输入与入口 | 预期观察 |
| --- | --- | --- |
| D3-AC1 | R1/S1；对照 README、现行 Reactivate Skill 和 workflow 全段 | 两类正式归档均准确说明，原 owner/匹配公共操作/一次增代关系清楚；没有任意旧格式准入。 |
| D3-AC2 | R2/S2；逐条语义比较本段前后条件 | 退役人员字段、人工历史、未完 closeout、旧 Finalizer 分流与否定完整保留。 |
| D3-AC3 | R3；检查 Markdown 链接、完整 diff 和相关 source/installed/platform/docs 机械验证 | 链接指向原 Skill；除本批规划与生命周期资料外，交付差额只有顶层 README 文案，无代码、runtime 或公共合同变更；diff hygiene 通过。 |
| D3-AC4 | R4；后续原 Check、两轮独立 Review、readiness 和交付事实 | 各门禁覆盖本批真实候选与各自阶段；具体执行顺序在 design 第9节定义。 |

本批不新增镜像字面测试，不重复无关 heavy 安装矩阵。已有工程证据仅由后续 owner 按真实输入适用性使用，不声明本批已验证任何未执行工程链路。需求没有未决产品或来源选择；候选 Architecture assessment 是首次方案写作的前置。

## 7. Canonical 引用与本轮差额

| 权威与章节 | 本批用途与差额 |
| --- | --- |
| `docs/requirements/current/completion-closure.md`：跨 clone 的 Closure 输入与共享终态、R669 | current Task2 与指定正式 schema1 的既有要求；定义正确，本批只修 README 入口说明。 |
| `docs/design/current/completion-closure.md`：最小共享 Closure 载体与恢复、D669 | 原 reopen/formal operation、后继优先和原 owner 关系；无设计机制变化。 |
| `docs/test/current/completion-closure.md`：T635-06、T669 | 保留正式 family、人工/未完分流和实际证据层次；本批按 D3-AC1–3 语义/静态验证，不复制旧工程测试。 |
| `docs/architecture/03-domains/ownership.md`：ARCH-DOM-032、ARCH-DOM-060；`docs/architecture/04-integrations/distribution.md`：ARCH-INT-063 | 原 Reactivate 与 Trellis 公共 writer 各自单写，matching formal capability；本批不改 owner/API/state/shared authority。最终影响判断交原独立 Architecture owner。 |
