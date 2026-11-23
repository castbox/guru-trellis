# D1 独立架构单元晋升实施计划

## 1. 输入与引用

读取 [整体范围](../../prd.md)、[本批 PRD](prd.md) 和 [本批设计](design.md)，采用第 3 节的来源设计处置与第 8 节的复现边界。B 为 `8604558695dfd9d8ea2181406a87ece70d9eea63`，本批没有前序 Delivery。实际实施加载原 Architecture final integration 合同、#711 共用发现合同和仓库生效规范。

## 2. 有依赖顺序的步骤与文件责任

1. **I1 基点检查。** 已从同一临时提交执行三组正式晋升。两个独立样本保留根，合法例外更新查找合同。A、B 首次候选绑定失败，恢复和读回记录已保留。实际差异、起点、输入和重跑命令见[基线复现记录](research/baseline-evidence.md)。
2. **I2 定向修正。** 当前停点为基点未复现根误写，且当前入口核对没有找到目标选择遗漏。获得正常入口、触发输入和根误写结果后，交原 Author 定位修复点，再完成适用的架构评估、Approval 和计划确认。
3. **I3 分发。** 实际修复通过原规划后，原 tools owner 从完整匹配来源同步当前 checkout 的受管包与适用投影，保留本 Task 和会话。检查已装载版本、受管差额和可见 sidecar。实际验证选定匹配的安装或复用该测试 repo，保留文件差异。
4. **I4 复跑与原质量链。** 有实际修复候选后，在候选 provider 下以等价复现入口重跑 V1 和 V2。核对每项实际写入和原 wrapper 结果。运行受影响的包测试与分发检查。然后沿原工程自检、TaskCommit、独立 committed Check/Review、Publication 路径交付。Merge 保留协调决策。

## 3. 验证入口、输入与预期观察

- **V1/V2** 按 [design 第 8 节](design.md#8-验证设计) 从同一临时仓库固定基点开始。将原始触发输入、关键调用和真实 Git 结果留作可重复观察的证据。每份样本的真实根写集与合法条件分别核对。
- **V3** 使用锁定 Trellis Fork 的 templated scripts，在已配备 managed runtime 的源 checkout 执行 `GURU_UPSTREAM_DELIVERY_SCRIPTS=<matching-fork>/packages/cli/src/templates/trellis/scripts PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/tests -p test_promotion.py`。在匹配的 canonical 和 installed 布局运行各自 `check-skill-packages.sh`。实际应用影响受管平台时，按原 overlay 检查命令验证差异与 drift。
- 验收覆盖临时仓库原 owner 的普通根误列、无共享竞争的另一独立晋升与合法根修改。已完成的包装层诊断作为支持证据。生产采用、发布和完整多平台升级在该验证边界之外。

## 4. 停止条件与适用回退点

- 当前没有发现本 Issue 的修复对象。保留原范围和三个用例的观察。获得新证据后沿原 Author 重入，评估其正常性、当前适用性和修复必要性。
- 当前需求或范围变更回原 Clarify。机制或 Architecture 变化回 Author 和 Architecture。真冲突或读回不一致回原晋升 owner。
- 本地修改可在这一个 Task 工作树中按合法变更范围撤回。临时运行只清理本次专用资源并保留可重跑证据。发布或后续整合仍执行其各自原 owner 的动作。

## 5. Delivery Policy

`full`。本批覆盖 #916 完整范围。完成条件包括正式临时仓库三组验收、定向分发检查、独立完整审核和实际交付。Task Completion 另核对这些证据和 Delivery 结果。

## 6. Docs SSOT Plan

`no_docs_update_needed`。当前 R711/D711/T711 已规定稳定根、独立单元、真实必要关系、原维护入口及验证职责。计划的过程修正由 canonical Architecture package 单写并通过原 tools owner 投影。原 Architecture owner 的最终设计审核确认适用性。若实际差额改变本仓 requirement、design 或 test 权威正文，回原 Author 把确需的变化纳入同一计划，再由原对应 owner 在 TaskCommit 前写入和读回。
