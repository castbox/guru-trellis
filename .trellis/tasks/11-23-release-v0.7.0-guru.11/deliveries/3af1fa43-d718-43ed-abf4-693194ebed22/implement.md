# D2：真实 source_locked 采用实施与验证计划

## 1. 输入与引用

整体范围见 [Task PRD](../../prd.md)，本批需求见 [PRD](prd.md)，设计与唯一来源处置见 [design](design.md)。D1 delivered source 为 `13d72b5425070fe841c1046d1e677d8323481eec`，PR #909 merge 为 `df638d19d458bbab11642b5626d293df30075ea1`。

实施前完整读取原 `guru-upgrade-tools` SKILL/contract、release contract、preset installer 与 workflow quality specs、当前 RDT/Architecture authority。

## 2. 有依赖顺序的步骤与文件责任

| 步骤 | 前置与 owner | 文件责任、行为与完成观察 |
| --- | --- | --- |
| S1 安装前预览 | Activation；tools owner | 从完整 D1 source 刷新 preview，核 source/Fork/CLI/API、target、平台、事务、保留和写删集 |
| S2 固定计划 | S1；tools owner | prepare 一次，审查完整 frozen plan、AGENTS renderer、平台和配置保留；展示精确动作 |
| S3 真实安装 | S2 安装确认；tools owner | invoke 执行原 public maintenance 与 Guru installer；失败只同 operation 恢复 |
| S4 目标验证 | S3；target owner | target resolver、installed/native、完整受管集合、source/CLI/lock、reapply/drift、保存、sidecar |
| S5 知识整合 | S3/S4；RDT/Architecture owner | 复核 adopted bytes 是否产生真实 current 差额；有则回原 writer |
| S6 交付 | S5；TaskCommit/Review/Publication | 精确 TaskCommit、constructor/begin_check、独立完整 Review、Refs-only PR、Merge |

## 3. 验证入口、输入与预期观察

原 tools 输入保持：

```json
{"profile":"install","source_ref":"13d72b5425070fe841c1046d1e677d8323481eec","dependency_mode":"source_locked","checkout":"/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/908-release-v0.7.0-guru.11"}
```

实际 preview/prepare/invoke 只通过完整 canonical source 中的原 tools owner 执行。Fork source 固定为 `/Users/wumengye/Documents/GoProjects/Trellis` 的 `e3793251...`，执行前核 clean/build marker/CLI/Core。

安装后从目标自身运行 installed validator、resolver/native entry、managed inventory bytes/mode、ownership、reapply/drift、sidecar 和 config/Task/session/peer preservation 检查。D1 source validator 与临时安装事实可沿用其适用范围，但不能替代本目标 actual after。

## 4. 停止条件与适用回退点

- D1 source dirty、Fork/build/API/lock 不匹配：停原 tools owner。
- target 有冲突、未知修改、sidecar 或相交事务：先由原 tools owner 返回具体处置。
- prepare 后输入、来源或目标变化：旧 frozen plan 失效，回原 owner 重新审查。
- 安装失败：只按原 recovery ref 恢复同一 operation。
- adopted bytes 暴露真实 RDT/Architecture 差额：回原 owner、Author Docs Plan 与受影响 Approval/Review。

## 5. Delivery Policy（唯一）

策略为 **staged**。

当前 D2 覆盖真实 source_locked 采用与完整 installed after。入口是 D1 delivered、D2 Planning/Approval/Activation；退出条件是原 tools 安装、目标验证、知识复核、TaskCommit、独立完整 Review、Publication 和 Merge 均完成。

后续仍有 whole-Task Completion、reference-only Closure、Finish/Cleanup，以及 Task 外 Stage 2 candidate/tag/smoke/Release/本地收敛/Issue closure。D2 delivered 不表示这些完成。

## 6. Docs SSOT Plan（唯一）

strategy 为 **no_docs_update_needed**。

现有 RDT/Architecture 与 tools/installer 合同完整定义 source_locked 采用、平台选择、保留和证据分层。D2 只更新 installed managed projections；若实际 adoption 发现 current 正文与 adopted bytes 不一致，先回 Author 更新本计划，再由原 RDT/Architecture owner整合/readback，不能静默修改历史或手改 managed copy。
