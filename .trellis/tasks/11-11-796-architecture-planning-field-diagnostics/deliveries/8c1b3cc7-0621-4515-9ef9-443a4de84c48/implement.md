# #796 D1 实施与验证计划

## 1. 输入与引用

读取整体 PRD、本批 PRD、design 第3节唯一来源设计处置及原 Architecture candidate_assessment。当前固定 B、无前序及完整范围沿用 design 第1—3节。
实施前加载 .trellis/spec/workflow/index.md、companion-scripts.md、skill-package-contract.md、quality-guidelines.md、subtraction-first-compatibility.md 和 .trellis/spec/guides/index.md 的适用正文。原 package 当前 Schema/runtime/tests/contract 为实际实现依据。

## 2. 有依赖顺序的步骤与文件责任

1. 原 Author 完成当前方案后经 Wording、独立 Architecture final_plan、Approval 与 Activation，才由 trellis-implement 子 Agent 写代码。
2. 实施 Agent 负责 canonical 规划 Schema 的 baseline_current 条件字段约束及 test_contract.py 的两项遗漏字段行为断言；若发现实际合同缺漏，先反馈当前 owner 判定后只修必要正文。
3. 通过 guru-upgrade-tools 的完整源 owner 将实际受影响工具投影同步到本 Task checkout，保留 Task/session/其它 peers；不手工覆盖受管副本，不走无关历史迁移。
4. 检查 Agent 对 approved scope、实际 diff、验证有效性和兼容边界完成质量审核；原 Architecture/RDT owners 做实现候选适用判断，原 Check 记录实际候选。
5. 原 TaskCommit、独立 Branch Review、Delivery Review、Publication、Merge、Completion/Closure/Finish 各按真实公共结果继续。

## 3. 验证入口、输入与预期观察

- V1：使用 package tests/test_contract.py 的真实 installed fixture 与 invoke wrapper，分别遗漏两个 identity；预期对应字段结构错误，没有成功出口。
- V2：复用同文件既有候选成功、final_plan 和其它合法出口回归，采用其真实输入/结果观察。按实际依赖运行相关 package 测试，不新增矩阵或语言声明扫描。
- V3：原工具同步 owner 的 installed/native 验证与 trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh 检查；git diff --check 核对格式。
命令通过已安装 resolver 使用其管理的 Python。测试夹具需要匹配的 Trellis CLI 0.7.0-castbox.6 scripts 源，通过 GURU_UPSTREAM_DELIVERY_SCRIPTS 提供；执行时核源码适用性，不能用依赖失败代替缺陷结果。
本计划不预填通过。上游完整 source lock、业务 #813 恢复及完整多平台安装升级/Release 不由本批定向验证证明。

## 4. 停止条件与适用回退点

范围/authority/机制发生真实变化时，回原 Clarify/Architecture/Author；不可为变绿放宽约束或静默补值。测试依赖失败先修复当前验证设施或说明证据缺口，不扩大业务修复。
工具更新冲突和 .new/.bak 由原安装 owner 处理；未解决不得声称同步完成。原恢复只作用于自己的冻结写集，保留其它任务和并行修改。
无数据库或生产部署副作用，不制造发布回滚协议。必要验收与回归充分后停止追加实验。

## 5. Delivery Policy（唯一）

policy=full。D1 完整覆盖整体 R1—R4 和 AC1/AC2，无剩余实现切片。
独立可交付条件为原规划入口对两个字段遗漏给明确诊断，合法调用及其它合法出口保持，必要受管副本一致。
验证边界为实际 package/runtime 和受影响投影；无业务 #813 环境恢复或完整安装矩阵承诺。
本 Delivery 合并后仍由 Task Completion 审查全部 accepted scope，再由 Closure/Finish 完成 Issue 和任务归档；合并不自动等同整体完成。

## 6. Docs SSOT Plan（唯一）

strategy=no_docs_update_needed。当前需求、职责、成功合同、恢复 owner 和架构边界不变；本次修复是既有字段要求在当前 Schema 中漏检。实现直接维护原 Skill 当前 schema/tests，只有实际文案缺漏才更新该 Skill 合同/示例。
原 RDT owner 在 Phase2 对当前完整定义与实际 diff 重新判断 no-change 是否成立，不预建空贡献、ADR、导航登记或审计账本；如果发现真实规范差额则沿原候选/最终整合晋升，不由实施 Agent 直接改共享 current。
直接 consumer 是原 Check、Branch Review 及当前 Skill 调用方；历史诊断与失败保持原观察。
