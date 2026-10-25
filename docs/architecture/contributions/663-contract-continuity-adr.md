# ADR-CONTRACT-CONTINUITY：固定 before 的缺失与维护回程

状态：proposed，待原 Architecture owner 在本 Task final_integration 晋升。正式目标：`docs/architecture/adr/contract-continuity.md`。来源：[当前修复要求 #663](https://github.com/castbox/guru-trellis/issues/663)；前序 ADR-028 与 ADR-KNOWLEDGE-FINAL-INTEGRATION 的适用性、固定候选及最终整合顺序保持。

## 问题与决定

固定内容基点 B 可能早于本 Delivery 首次建立 architecture authority。要求 B 上所有 authority 文件存在会使声明支持的首次 Bootstrap 后续审核无法执行。将 B 改为 H 或跳过原检查会丢失真实比较来源。

原 before_authority 使用其三个既有 locator，并以最小显式 absent_locators 表示 B 中真正不存在的路径。省略表示全部存在。Validator 在同一精确 Git revision 逐项核实；未列路径仍读取原文件。committed Review 仍固定 B..H，原 owner 审核当前新增文件、完整差额、受影响未改 consumer 和约束。缺失事实不是当前 authority 或 freshness 豁免。

final-integration 的 Bootstrap 维护使用现有 phase2 投影，保留原 promotion 的调用期 continuation，完成维护后 fresh 回原 promotion。维护结果不产生 reviewed_promoted、最终 Check 或业务阶段推进。Bootstrap repair seed 和 archived example 按其当前 consumer 合同直接纠正，不增 owner。

## 影响与边界

原 semantic/deterministic 分层、单写、typed exits、状态和兼容原则保持。成套更新当前 schemas/consumer/reference/平台，已有合法输入省略缺失集合的含义不变。无长期 adapter、公共恢复载荷或授权记录。

同样原失败样本与 B 已有 authority 对照、正式 final promotion 回程、只读 archived example 及原生安装样本用于验证。完整 Release 矩阵、旧业务安装和生产效果不由本决定证明。
