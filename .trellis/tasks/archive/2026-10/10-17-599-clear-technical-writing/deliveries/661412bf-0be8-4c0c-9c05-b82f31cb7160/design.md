# D1 详细方案

## D1. 范围与固定基线

Task 整体需求由 ../../prd.md 拥有。本方案承接 D1 全部 R1-R5/AC1-AC8。
开发基线 B = ea9998c36a188f3afae1d7d6e5746edc07fa003f，来源为显式 dev。PR 目标为 dev。规划 H0 与 B 相同；最终候选 HEAD 在实现后固定。PR 目标与内容基线独立。

## D2. 来源承诺处置矩阵

| 来源 | 原承诺 | 处置与落点 | 理由及上游处理 |
| --- | --- | --- | --- |
| #599 R1 | 明确 STE 版本、已核对采用内容、稳定规则编号及强度 | 保留；canonical clear-technical-writing.md 的来源、规则及例外表 | 采用官方公开 FAQ 已核对原则；未取得编号条款和完整词典不标采用；无上游变更 |
| #599 R2/R3 | 全自然语言范围、字面例外、授权功能修改及完整语义保留 | 保留；同一正文的范围、例外和双语示例 | 精简不削弱义务、否定、条件、顺序或未验证边界 |
| #599 R4 | 唯一 canonical 正文，复用 managed-spec，首次实质文本前完整读取 | 保留；显式受管映射、root AGENTS 区块、Phase Index、恢复合同、Guru Skill 与22个平台入口 | 不新增 wrapper Skill、hook 或上游文件 claim；用户区块逐字保留 |
| #599 R4 子 Agent | 不假设继承；说明原生注入与自行加载条件 | 保留；共享正文与 dispatch 读取合同，正式 manifest 引用同一安装文件 | 完整原生注入才直接消费；未注入、截断或不确定时 child 自行完整读取 |
| #599 R5 | 原写作 owner 自检；审核 owner 仅审原范围；wording 的固定合同保持 | 保留；公共 Guru Skill 只增加同一正文定位，原 contract/profile/exits 保持 | AI 判断语义；脚本只验证分发和已定义机械条件 |
| #57/#78 | 业务文档和审查报告中文；扩展公开源码的中英文分工 | 保留；正文语言政策引用现有 public-docs | 本次不重写历史文档和归档 |

## D3. 唯一正文与规则结构

canonical：trellis/presets/guru-team/spec/workflow/clear-technical-writing.md。
安装：.trellis/spec/workflow/clear-technical-writing.md。
直接 consumer：当前输出 Agent、写作 owner、原范围审核 owner和独立 child。
文档使用稳定 GTW 编号。每条写明强制/建议、适用内容、例外和来源。建议不产生阻塞 finding。不得把句长或关键词扫描当语义合规判断。

英文参考 ASD-STE100 Issue 9（2025-01-15）。正式来源为 ASD STEMG 官网、About、FAQ 与下载页；采用表精确引用已读取的 FAQ 问题。完整 PDF 和编号条款尚未取得，完整词典不实施。中文仅采用清晰表达原则，不声明符合 ASD-STE100；英文也不声明完整实施或认证。

规则覆盖单一主意、执行者/动作/对象、触发条件/结果、术语一致、表达强度/事实/计划/未验证状态。准确性高于简短。Task、Delivery、Check、Review 保留不同含义。

正文包含中英正反例与逐例理由。覆盖指令、条件、术语、要求/建议、未验证结论，以及复合条件、否定、例外、顺序、授权接口修改、用户原文/格式、敏感原始证据与脱敏摘录。示例显式给定真实语义或证据前提，不通过改写发明新事实。

## D4. 加载合同与入口装配

| 入口 | 加载路径 | 直接 consumer |
| --- | --- | --- |
| 无Task/正式Task/task-free/manual会话 | root AGENTS 有界区块 + workflow Phase Index | 当前主会话 Agent |
| 新会话与恢复/压缩接续 | 同一 Phase Index 与唯一 continuation 的短定位 | 接续 Agent |
| 独立 Guru Skill | canonical SKILL.md 中的同一安装正文定位 | 该 owner |
| 22个平台 Guru finish entry | descriptor 对应 overlay 的格式内短定位 | 平台入口 Agent |
| 子 Agent | dispatch 指定安装正文；implement/check manifest 纳入同路径；完整原生注入或 child 自读 | 当前 child |

完整正文读取前只输出短句进度或具体缺失诊断；明确当前动作或缺失项，不作未验证结论。不得在此前生成需求、方案、审查、Issue/PR 或任务答复正文，也不得声称已经执行完整规范。
读取失败只暂停依赖该规则的实质文本。规则恢复后，Agent 完整读取并继续原请求，不新增审批。

不修改官方 trellis-* Skill、原生 hooks、Agent definitions 或全局包。原生注入只在可证完整文本且未截断时替代直接读；否则自读。原生投影一致与实际执行分别验证。

## D5. 安装与演进

在现有 MANAGED_SPEC_PATHS 增加一个映射。复用 copy_managed_spec、既有受管 AGENTS block 和平台 descriptor。安装/reapply 不重写 AGENTS 用户区块。
完整匹配的 preset 安装后，引用均指向安装正文。canonical 修改后运行现有 apply 同步 dogfood；workflow 从其 canonical 源同步到当前已确认无用户差异的 dogfood 副本。检查每个 .new/.bak，按既有 provenance 处理，零未解决 sidecar 才通过。
旧安装需要匹配的 workflow 更新与 preset reapply。Trellis update/upgrade 后按官方 marketplace 预览/显式应用 workflow，再 reapply，保留用户冲突。源码改动不代表旧安装已采用。完整升级与 Release 矩阵仍由专门 Issue 承担。

## D6. 语义与机械职责

写作 owner 输出前自检。审核 owner 对原范围检查：歧义影响行为、漏条件或弱化义务按 correctness；适用强制规则违规要求修订；建议偏好或同样清晰的表达不阻塞。guru-review-contract-wording 不承担通用语言审核，其固定范围、前置和 typed exits 不变。
机械测试只验证安装路径、引用解析、格式、投影、保留用户内容、reapply/drift/sidecar。实际语言清晰度与语义保持由 AI 逐例审查，实际读取顺序由真实平台 trace 验证。

## D7. 维护边界

installer 既有文件超过3000行。本次只增加映射和有界区块内容，不新增分支或第二写入路径。已审查局部机械拆分：把单一常量或映射另建模块会增加跨文件耦合，无法降低本次控制流复杂度；保留原 owner 的直接装配。本结论不扩张为历史 installer 重构。

## D8. Architecture 与 Docs

独立 candidate_assessment 选择 architecture_impact / target_native；沿用既有 common-spec、single semantic owner 和 bounded installer 架构。贡献定位 docs/architecture/contributions/599-clear-technical-writing.md。不新增 ADR；沿用 ADR-005、ARCH-FND-001/002、ARCH-DOM-036/041。贡献仅为 task-owned candidate，shared promotion 在首次完整 committed Branch Review 后由原 owner 执行。
RDT 使用 docs/requirements-design-test-contributions/599-clear-technical-writing/ 的 requirements/design/test/traceability/manifest；只记录本次需求、设计、验收与正文定位，不复制规则。原 RDT owner 负责 contribution/promotion；唯一 test.md 记录实际结果和边界。
