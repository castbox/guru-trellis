# D1 实施与验证计划

## 1. 输入与引用

使用本 Delivery [需求](prd.md) 和 [设计](design.md)，设计第 3 节给出来源处置。整体边界读取 [Task PRD](../../prd.md) 和 public accepted scope。原职责见 Merge contract「Manual MERGED recovery」、Completion SKILL、ADR-026 与现行 Task Delivery lifecycle 三层单元。D1 无前序结果。

## 2. 有依赖顺序的步骤与文件责任

1. Merge 实现 owner 修改 canonical Merge package。新增显式输入和评审合同、Interface profile、示例与 runtime。复用双父终态验证和现有 public fact writer。用已安装 API 解析原 Task 记录和构造 Git 内容，沿现有 inspected paths 合同排除元数据。
2. 更新 canonical workflow 的正常显式选择路由、Merge 与 Completion Skill 说明和采用指南。复用现有 `delivered`、`merge_blocked` 及 Completion、Closure、Finish 的消费。历史恢复不经过 pre-merge gate。
3. 验证 owner 在现有组件测试结构内使用真实 Git 与公开 wrappers 补齐 V1–V3。元数据由原 owner 或 installed public operation 建立。外部 fixture 只提供 GitHub 依赖事实，实际记录由已安装组件完成。保存真实错误与执行结果的最小证据。
4. 用选择的原工具更新 owner 同步 dogfood 与平台投影，观察冲突、侧车和保留的 Task/session。需要代表性安装时使用完整 matching source，检查 reapply 与工程质量。
5. RDT 和 Architecture 原 owners 在实际验证后整合并读回共享 authority。TaskCommit 固定真实 B..H 候选。原独立 Reviewer 审核整段差异和整合前后内容。随后沿原 Delivery Review、Publish、Merge、Completion、Closure、Finish 完成交付与归档。

## 3. 验证入口、输入与预期观察

- 首先跑设计 V1 的正常旅程。利用 Merge、Completion、Closure、Finish 公开 wrappers 和隔离 Git 目标。确认每个实际结果及最终 archive。#828 的 GitHub 和 Git 证据可作为独立现实样本读取。隔离验证用匹配正式链，报告 GitHub 替身界面与现场读回的区别。
- 用 Merge package 的 pytest/unittest runner 执行 V2/V3。观察非等同 merge/head 的真实差异、错误归属的未写入、重入同一事实、#557 回归及缺失或失败 CI 保持原义。
- 执行受影响的 source/installed package contract 检查和 `check-dogfood-overlay-drift.sh`。检查修改的 Python 及 JSON；运行 `git diff --check`，核对递归侧车及适用权限。一个代表性 matching install/reapply 验证本改动的分发。
- 完整多平台发布矩阵与软件 Release 属独立验证。目标分支与 PR head 的证据只在实际读到的对象上成立。验收例通过后停止重复验证。

## 4. 停止条件与适用回退点

缺原账号权限、公开身份、Git 对象或既有接受范围时保留缺口并回原事实 owner。业务实现失败回第 1–3 步，受管冲突由原工具 owner 处理。来源或真实机制变化回最早受影响的 Planning owner。记录前可移除本作业的变更；记录后由原恢复入口读回。不存在额外数据迁移。工程验证失败时先定位真实行为、测试设置或分发依赖，并按受影响范围重跑。

## 5. Delivery Policy

`full`。当前切片覆盖 Task 整体 R1–R3、AC1–AC3。成功条件是已有 Task/Delivery 缺原 Publication 时，真实合并可被归属、记录和接续收尾，重入返回相同事实，错误归属保留状态，#557 继续工作。没有计划后续 Delivery。原 #896 Completion 独立判断实际解决和证据范围。

## 6. Docs SSOT Plan

`delta_first`。维护 `docs/{requirements,design,test}/current/task-delivery-lifecycle.md` 中与合并恢复直接相关的需求、设计与验证条件。实际验证结果随本次最小可读 RDT 证据维护。原 RDT owner 在提交前整合和读回三层差额。原 Architecture owner 使用本 Task 的贡献维护 ADR-026 的责任演进，在提交前整合实际目标并保留 before/after。固定候选的同一次独立审核判断当前内容与真实测试证据，再交 Delivery Review。
