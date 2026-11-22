# D2 实施与验证计划

## 1. 输入与引用

读取 Task 范围、本批 PRD 和 design 第3节。D1 实际交付为 PR #888。使用当前共用验证与独立审核方法、模板及原 RDT 和架构域。

## 2. 有依赖顺序的步骤与文件责任

1. 原 RDT 与 Architecture 负责人先准备本批隔离知识差额。
2. 实施负责人修改 canonical quality-guidelines 的验证选择段、Author 实施模板和已有去敏示例。现有 Phase 2、Approval 和 Check 已读取该共用方法。定向分发试验覆盖新方法和模板。
3. 先执行 V2，再使用 V3 和 V4 核对样本、替身和简单任务裁剪。V5 与 V6 核对实际投影、安装与工具采用。
4. 工程验证完成后，原知识负责人写入并回读本批 RDT 和 Architecture 目标。固定提交后走原独立 Check、Branch Review、Delivery Review 及发布与合并。

## 3. 验证入口、输入与预期观察

V2 用可运行入口和完整依赖的编辑旅程，在实际 Phase 2 方法观察中优先完整主线。V3 用当前媒体支持和新对象语义，先读来源再读候选。V4 用简单 trim 函数验证直接单测。真实原生材料、工具动作和结论由独立评价者核对。

V5 用匹配 Fork 脚本和受管 Python 运行现有定向安装/reapply 与受影响包校验。V6 用原 tools owner 同步本 worktree，核对受管投影、所有权、drift、当前 Delivery 和 sidecar。保留适用 D1 结果及本批材料的实际结论。

## 4. 停止条件与适用回退点

保留原素材、首轮结果和缺口。若模型或装配出现具体问题，先确认影响，再通过原入口恢复。范围或机制的实际变化返回原 owner。没有业务数据或部署回退。

## 5. Delivery Policy（唯一）

`full`。本批交付剩余 JQ-R3/R4、适用 R5/R6 与 AC3–AC8。没有后继实施切片。Task Completion 仍核对 D1、D2 的独立结果以及本 Issue 的证据。

## 6. Docs SSOT Plan（唯一）

`delta_first`。RDT 原负责人先在 `rdt-proposal/` 准备行为验证方法的三层完整单元。Architecture 贡献在 design 第9节。工程验证后由原维护者整合实际差额并回读，纳入后续固定提交。
