# D1 需求歧义探索与分级确认实施计划

## 1. 输入与引用

先读整体 `../../prd.md`、本批 `prd.md` 全文及 `design.md`。来源设计唯一处置见 design 第3节，行为、逐项记录和恢复约束见第4至7节，验证边界见第8节。首次 D1，无前序交付；B 为 a4feadd99683e006580ef16b078c44e3ad3648a7。

实际独立 candidate_assessment 的 baseline_current/no_architecture_impact 支持当前候选，不代替后续 Wording、final_plan、Approval 或实施激活。实施前完整加载 AGENTS、trellis-before-dev 选出的 workflow/preset/docs 规范和必要工程合同。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置与责任 | 文件及行为 | 完成观察 |
| --- | --- | --- | --- |
| DEC-I1 | 原规划审核及激活后；Trellis implement worker | 共享 workflow-contract 的 Interaction Budget，定义需求/实现及轻度/重大确认边界 | 唯一共享原则明确，无新的副作用权限 |
| DEC-I2 | I1；同一 worker | Clarify SKILL/references、Author planning-body/authoring、必要 workflow/入口引用 | 问题发现与回答回写可执行；清单不与绝对单问题提示冲突，不改 upstream brainstorm |
| DEC-I3 | I2；同一 worker | Clarify package 教学例子与相关 package tests | 正反例标为教学；原 per-question recorder/checker 和 partial 规则有直接验证 |
| DEC-I4 | I2；同一 worker | source-only 对话评测案例、最小 native driver 及 driver tests | 后续合成回复在后续轮次才提供，真实 events/exit/session ID 可审核，脚本不打语义分 |
| DEC-I5 | I2至I4；主会话协调原 RDT writer | 隔离的 task-owned RDT 完整变更候选，覆盖行为、设计与测试；原时点再晋升 | shared current 在候选 Check 前保持原样；无平行 authority |
| DEC-I6 | I2至I5；主会话同步安装副本 | 原 apply 与 drift/package 验证，处理本次产生的 sidecar | canonical 与 dogfood/安装一致，无无关覆盖 |
| DEC-I7 | I3/I4/I6；独立 Trellis check 与原 Architecture/Check owners | 完整候选、真实对话结果及工程检查 | 区分语义、结构、分发证据，修复本范围 findings 后复核 |

所有 worker 不单独提交、暂存、推送或改业务项目；主会话不替代独立检查结论。无真实临时产品限制，不制造解除条件或后继切片。

## 3. 验证入口、输入与预期观察

DEC-V1：通过现有 managed Python 测试入口运行 Clarify `tests/test_contract.py` 及必要依赖；新增清单完整接受、逐项修正和部分回答案例。预期原 wrapper 保持逐项问题生命周期，不改 schema 或放宽关闭条件。

DEC-V2：扩展并执行 `trellis/presets/guru-team/scripts/python/test_planning_body_distribution.py` 或同机制的定向分发测试，实际安装并重复 apply 相关资产；核对源码与安装投影内容，保留用户文件。仅证明分发，不证明 Agent 提问。

DEC-V3：执行新增 source-only native 对话驱动的代表性案例。使用当前可用 Codex CLI 默认配置，不指定不同模型；第一轮只给需求和仓库事实，之后才给合成测试用户回答。AI reviewer 核对完整对话、实际调查、推荐、问题关闭及规划变化。未执行或失败不预填通过；方法试验不声称完整生命周期验证。

DEC-V4：使用 subprocess 双替身的本地 unittest 检查 driver 的分轮输入、真实 session ID、超时及退出码收集；这种测试不作为真实模型结果。native CLI 不可用时保留明确缺口。

DEC-V5：运行命中 package 的 source/installed validator、`trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`、`git diff --check`、相关 JSON 解析与 Bash 语法、quality-guidelines 要求的内存 Python syntax check。若修改 workflow 路由，额外读取 phase 及受影响 step。无需完整多平台 Release 矩阵；所有实际命令与结果在实施后报告。

## 4. 停止条件与适用回退点

需求或范围改变回原 Clarify；技术候选违背既有约束回 Author/Architecture；未解决问题停止依赖行为，不冻结独立调查。原 recorder 无法表达合法逐项清单时先修方案，不擅自增加公共字段。

出现非本次并行改动停止受影响编辑并报告，不恢复别人内容。测试失败先确认本次因果与受影响边界，不借机修历史无关问题。评测工具错误不算语义失败已修复，也不算通过。

无数据迁移、部署或发布，因此没有生产回滚操作。保留未提交本地 diff，按具体本次 hunk 修订；不执行 reset、checkout 恢复或自动清理。提交、推送、PR 与业务项目升级保持后续独立边界。

## 5. Delivery Policy（唯一）

Policy 为 full。本批覆盖 DEC-R1 至 R8 与 DEC-AC1 至 AC6，当前无计划延期功能。完成条件为规则、实际 consumer、教学、逐项记录检查、真实交互结果及分发证据共同覆盖；未验证项如实保留，不把本地绿测等同于整体完成。

本次执行范围不包含提交或发布；本地实现与检查结果不能冒充 Delivery 已交付或 Task Completion。后续发布仍由原 owners 承接相同 Task/Delivery，不新建身份绕过未完步骤。

## 6. Docs SSOT Plan（唯一）

Strategy 为 delta_first。实施 owner 在 task-owned 隔离候选中准备完整需求/设计/测试变更；原 RDT writer 为直接晋升 owner，原 Check/Architecture 审完整候选。候选 Check 后在原 final integration 维护实际 shared current，再重建实际候选并进行最终检查。

当前 authority 由 `docs/requirements/README.md`、`docs/design/README.md`、`docs/test/README.md` 解析；本轮差额为需求探索、分级确认、清单回答与 native 行为证据边界，不重写历史事实。共享规则源仍是 interaction-budget，步骤方法属于原 Skill；RDT 描述能力及关系，不复制第二套执行合同。

Architecture 预评估判断无架构影响，无贡献或 ADR；final_plan/实施若发现实际机制改变，返回原 Architecture 重新判断，不沿用旧无影响结果。规划阶段不修改共享导航或创建空 contribution。
