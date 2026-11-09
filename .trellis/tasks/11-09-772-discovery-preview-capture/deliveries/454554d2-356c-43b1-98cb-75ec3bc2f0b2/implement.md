# Discovery 大预览捕获与恢复：D1 实施计划

## 1. 输入与引用

整体范围为 Task 根 prd.md 的 accepted_scope；本批 prd.md 全部 R1–R6/AC1–AC3，方案见本批 design.md 第3节唯一来源设计处置及第4–8节。当前起点 main@fd52fbd69a8161d037bf6d4548b04b7247b60c03，无前序 Delivery。

实施前完整读原 Discovery SKILL/contract、共享 companion-scripts 的 Reading Required Contracts In Full 与 Intermediate Command Stdout、clear-technical-writing 及适用 package/installer 规范。保留已验证机制因果依据；原 public 输入/输出和 fixed-tree reader 保持。实际读取设计引用的必要条件。

## 2. 有依赖顺序的步骤与文件责任

1. I1：原 Author 完成计划，经原 Wording→独立 Architecture final_plan→Approval→展示与 Activation 后改扩展源码。
2. I2：trellis-implement worker 负责 canonical Discovery SKILL.md、references/contract.md、examples/history-preview.md。前置直接执行路径，示例采用标准库完整 bytes 捕获和有限分页展示/补读；不改 runtime/schema/评分。不修改 Task 规划、受管投影或其它 Agent 文件。
3. I3：原实施 owner 核对完整差额并执行 V2。示例资源若需原 package 机制显式登记，仅做最小必要登记，不新增 API 或 wrapper。不手工复制受管投影。
4. I4：原 guru-upgrade-tools owner 从完整匹配 source 同步本 checkout 的 dogfood 及声明平台，保留 Task/session/peer；按 prepare/invoke 和实际恢复结果执行。源需先提交时走原早期 TaskCommit/Draft 职责，再继续同 Delivery。
5. I5：原 RDT owner 判断适用完整单元是否需差额；无差额不造空贡献。独立 Architecture Phase2 及原 Check 检查完整 candidate；若有隔离知识贡献，仅 candidate_checked 后由原 owner 最终整合、重绑 candidate 并 final Check。
6. I6：原 TaskCommit、完整独立 committed Review、Delivery Review/Publish/Merge、Completion/Closure/Finish/Cleanup 继续同 Task/Delivery；提交与 PR 只含本范围。

无临时限制和后继业务切片。工具验证的证据限制见第3、5节。

## 3. 验证入口、输入与预期观察

- V1：原语义 Check/Review 完整读取 I2 正文及必要未改 consumer，逐项核 R1–R6、S1–S4。预期先完整捕获再解析，全部候选 AI 判断、自动恢复和真实失败出口明确；文字扫描不代表语义通过。
- V2：按公开 examples/history-preview.md 在持久 Node REPL 实际执行，query 与 base_current 保持同固定 main，正常大归档 preview 超过本次展示预算。预期 exit0、完整 receipt.result 可解析；全部候选 ID 可定位；紧凑分页不截断，长字段按候选 ID/field/offset 全部可读。只保留调用内存，在会话报告结果，不加 tracked 预览证据。复用 Issue 两真实会话的失败/恢复证据，不重演业务会话、不新增 native 评测或完整 Intake/consumer 验收。
- V3：使用原 discover-skill-contract/validate-skill-contract 的 source 与 installed 模式及受影响 package/document 检查；原 tools owner 安装后运行 `bash trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .`，核 Shared/Claude/Cursor 和选择 Codex 后的实际投影、权限及 sidecar。按实际工具 help 使用原入口。
- V4：`git diff --check`；必要现有 package tests 和本 Task 公共模型校验。未改 runtime 行为复用适用既有证据；实际变更时补对应检查。

先实现说明，再执行公开大样本和分发检查。证据充分后停止；没有额外缺口不做反复红绿或旧版回退。完整多平台 clean/existing/update 矩阵、Release Gate 和生产 Agent 重验不在本 Issue 范围。

## 4. 停止条件与适用回退点

真实来源/范围变化回 Clarify；机制改变回 Author/Architecture；命令失败或 stale/mismatch 走原 owner 实际出口。展示截断只缩小批次补读，不作为业务阻塞。安装冲突和 sidecar 由原安装 owner 处置，不覆盖用户内容或改旧事务。检查失败先定位输入和归因；设施反复失败时评估同层观察或保留明确缺口，不能预填 pass。

无数据迁移、业务部署或服务配置变化，无新增回滚协议。本地修订仅改本范围；保留并行任务及历史。Git/GitHub 动作按原 owner 精确计划、语义审查和 live read 执行。

## 5. Delivery Policy（唯一）

Policy=full。D1 完整交付 R1–R6、AC1–AC3，无延期业务工作。可交付条件为完整主路径/示例、真实大预览示例观察、原安装投影和定向验证、无未解决本范围 finding。当前 scope 不要求完整 Release 矩阵或生产 native 重演，保持其未验证边界，不泛化兼容或效果结论。Task Completion 仍判断全部要求、验证与交付，合并 Delivery 不自动完成 Task。

## 6. Docs SSOT Plan（唯一）

Strategy=no_docs_update_needed，针对共享 RDT/Architecture 基线。本批原 Discovery package 合同和例子是运行指引，由 I2 原 owner 直接维护，不复制到共享 workflow/spec/README。共享预算只引用现行 companion-scripts。现行 RDT local-fix-intake/runtime-location 已定义当前 AI、完整命令输出、固定 tree 和原错误恢复；本批组织其执行路径，没有新 public 能力或数据合同。原 RDT writer 在 Phase2 读取完整命中单元及关系；若发现真实新差额，先形成隔离完整候选交 candidate Check，最终 Phase2 前由原 owner 晋升和追踪，不静默改共享导航。

Architecture 已返回 candidate_assessment no_architecture_impact，仍需 final_plan 与实际 Phase2/Review 判断；无真实差额不建 contribution/ADR。直接 consumer 是当前 Discovery AI 与原安装 owner；canonical/installed/平台一致由 V3 验证。规划和历史不作为共享 current。
