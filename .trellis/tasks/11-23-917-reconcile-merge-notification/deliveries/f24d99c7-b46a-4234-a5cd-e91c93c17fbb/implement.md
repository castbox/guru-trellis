# D1 合并通知的 Reconcile 路由实施与验证计划

## 1. 输入与引用

读取 [整体需求](../../prd.md)、[本批需求](prd.md)、[设计](design.md) §3 的唯一来源处置、§4 的真实 owner 和 §8 的验证。工作起点 main@8604558695dfd9d8ea2181406a87ece70d9eea63。无前序交付。开始写入前用原边界命令核 Task、分支和工作树。实施时读取官方 Trellis workflow 与 marketplace 文档、项目 AGENTS.md、适用 spec、现有 canonical 和安装投影。

## 2. 有依赖顺序的步骤与文件责任

1. 核对原受影响入口与事实来源。读取 canonical workflow、已安装 workflow、共享 issue-orchestration、两协调 Skill 的入口和在途/接回路由，以及原 Reconcile actual integration entry。定位用户条件和核对事实在原派发中的传递点。
2. 修改 canonical 共享编排正文的 Minimal Child Prompt 和 Fresh Merge Gate And Integration。将默认同步指令替换为条件与事实的直接传递。保留仓库集成槽、目标和合并 eligibility 的原执行顺序。修改 canonical workflow 的在途与接回入口并引用原固定内容、实际集成判断正文。
3. 按原工具更新 owner 在本 Task checkout 同步 dogfood。同步整个受影响 managed workflow 与共享 spec。核声明的平台入口真实解析到该共享 spec。按原 owner 处理每个 .new 或 .bak。
4. 在现有源私有 native runner 旁落地通知场景的可重跑入口。复用其同源内容投影、隔离 Codex 进程及事实运输。测试载体负责创建本次临时仓库、生产真实 Git 事实、记录实际派发和命令输出。保留模型与执行设置以供重跑。只在私有测试目录放载体和脱敏固定输入。原始运行记录保留于隔离输出目录。
5. 跑完 §3，沿原 RDT owner 整合并回读命中的完整当前 RDT 单元。在本地 TaskCommit 前整理真实候选、必要验证和范围内文件。原独立 reviewer 审核固定已提交差额后，交原 Publication 准备并呈现精确 PR 计划。到原 Merge gate 等待协调指令。

## 3. 验证入口、输入与预期观察

- **V1、V2、V3。** 从独立临时仓库和本地 bare origin 起步。固定起始提交、当前候选和适用证据。用正常提交和更新推进目标。无阻塞样本可在同一文件不同位置形成差额。冲突样本改同一位置。以 Git 事实核对两种区别。用计划中的源私有入口 `python3 trellis/skills/guru-team/packages/guru-orchestrate-issue-dag/tests/run_native_merge_notification.py --root . --output <新建隔离输出目录>` 依次取得协调派发、直接通知和实际冲突证据。载体以真实 Agent 选出的动作为准，分别保存通知、轨迹、实际命令参数、退出状态和 stdout/stderr。冲突使用原 Reconcile 首个适用命令 `execute-base-candidate.sh`，参数含真实固定目标，不执行解冲突或持久整合。保留起点、目标、候选 SHA 和可重建输入。重跑后读取实际轨迹和 Git 关系，由当前 owner 判定满足 AC1–AC3。
- **V4。** 使用同源工具更新和目标支持的 Trellis 版本，定向检查 source/installed discovery、重应用和声明的 Codex 编排入口。核同源 workflow 与共享 spec 的安装 bytes、模式、改动集和 sidecar。执行 `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`、已安装 Skill package 校验和 `git diff --check`。记录具体版本、投影、验证和未运行的平台路径。
- **证据边界。** 以现有 #567 固定候选、公开 Reconcile 与隔离 runner 能力作为可复用工程事实。真实目标更新及冲突观察与 AI 派发/执行判断分别由实际轨迹证明。完整多平台升级和软件 Release 验证不在本批验收。来源业务仓和 Codex App 现场效果没有本批实测要求。

## 4. 停止条件与适用回退点

真实需求变化回原 Clarify。机制影响超过当前方案时，回原 Author/Architecture。发现本次夹具无法进入实际入口时先核可复用载体，随后修正仅影响本验证的设施。验收依赖的真实行为仍不可见时，记录具体缺口并停在受影响 gate。保留失败运行，迁移或并行内容冲突交原 owner。完成所需观察后停止本批验证。实际 GitHub 操作沿原 TaskCommit、Publication 和 Merge 的前置及授权边界执行。

## 5. Delivery Policy

策略 full。本切片覆盖 #917 全部 AC1–AC3。可交付条件为两个入口合同一致、临时仓库真实行为轨迹满足三个检查、定向受管验证和原独立审核通过。无计划分配给下一切片的工作。Task Completion 仍由原 owner 核对真实合并结果与全部 scope。

## 6. Docs SSOT Plan

策略 delta_first。将通知条件、两个入口和真实冲突调用的当前行为及验证方法纳入 [需求](../../../../../docs/requirements/current/issue-orchestration.md)、[设计](../../../../../docs/design/current/issue-orchestration.md) 和 [验证](../../../../../docs/test/current/issue-orchestration.md) 的既有单元。运行定义继续由 canonical workflow 和共享编排正文各在自己的职责内单写。原 guru-maintain-requirements-design-test-ssot 在提交前合入并回读，TaskCommit 纳入真实 after，独立 reviewer 审查提交后完整差额。Architecture 以 [ADR-028](../../../../../docs/architecture/adr/028-fixed-content-baseline.md) 为适用权威，按独立候选审核的无架构影响结论处理。
