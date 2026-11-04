# 修复 resolved Check gitlink 身份整体需求

## 1. 来源与术语

本 Task 为 no_issue 独立工具修复请求，不创建或关闭 GitHub Issue。原请求要求修复合法 resolved merge 的 staged 子模块指针检查，并通过受支持的完整工具入口恢复调用方；下文完整承载该请求。

| 来源 | 定位 | 角色与用途 |
| --- | --- | --- |
| 当前独立请求 | 本文第2—7节 | 要求；定义修复和验收边界 |
| 当前 Check | `trellis/skills/guru-team/packages/guru-check-task/runtime/common.py` 的 `gitlink_entries`、`content` | 当前实现证据；普通 HEAD 与 index 绑定 |
| 当前 resolved consumer | `trellis/skills/guru-team/packages/guru-check-task/runtime/delivery.py` | 现行合同；专用 resolved profile 与原整合职责 |
| 原整合执行 | `trellis/skills/guru-team/packages/guru-reconcile-task-base/runtime/execute.py` | 现行实现；精确 tree、parents、message 的提交职责 |
| 历史 gitlink 修复 | `.trellis/tasks/archive/2026-08/08-08-186-uninitialized-gitlink-identity/prd.md`；`.trellis/tasks/archive/2026-09/09-12-397-fix-base-candidate-gitlink/prd.md` | 历史约束；保留 child root、clean、OID 与普通绑定 |
| 历史 Delivery 整合 | `.trellis/tasks/archive/2026-09/09-18-435-active-task-delivery-loop/design.md` 的 D435-08 | 历史约束；resolved Check 后由原 Reconcile 提交，再检查真实新 HEAD |

resolved merge 指 HEAD 尚未移动、单一 MERGE_HEAD 存在且 index 冲突已解决的合并候选。stage-0 gitlink 指 index 中 mode=160000、stage=0 的子模块目标提交。Check、Review 和 Reconcile 保持原 owner 含义。

## 2. 背景与问题

正常基线整合时，父仓库 HEAD 仍为整合前提交，stage-0 index 已包含新基线子模块指针。即使冲突已解决、子模块精确检出目标且 clean，正式 `delivery_resolved_reconciliation` Check 仍报 `Gitlink index and commit bindings differ`。当前共用捕获把尚未提交的合法 stage-0 与旧 HEAD tree 比较，阻断原精确整合提交。

## 3. 目标与非目标

完整解决上述 Check 捕获及其 record、check、invoke、projection、Reconcile 组合缺口。普通 Check 的 HEAD 绑定和子模块校验继续成立。交付包含 canonical 修复、正常 Git 回归、完整工具来源一致性和原调用方候选复跑。

不增加业务导航功能，不发布 release/tag，不扩展恶意输入、压力并发或完整多平台 Release 矩阵。工具源码通过合法 pull_request 交付；源码合并不替代受支持入口验证及真实调用方复跑责任。

## 4. 真实调用方、场景与流程

- S1：基线整合调用方持有已解决合并，HEAD、单一 MERGE_HEAD 和 stage-0 index 已确定，child clean 且 HEAD 精确匹配 stage-0 OID。调用专用 resolved Check 后，原 record→check→invoke→projection 接受同一候选，原 Reconcile 执行精确提交，再对真实新 HEAD 执行 Check/Review。
- S2：普通 Check 调用方暂存 gitlink 更新但 HEAD tree 未更新。普通入口继续拒绝 index/HEAD 绑定差异。
- S3：正常操作后 child dirty、child HEAD 不匹配、冲突未解决或被审候选改变。原明确诊断阻断过期通过；调用方修正实际内容后重走原入口。
- S4：原调用方使用完整匹配且被审的 canonical source，通过原 wrappers 的 --root 入口对实际在途候选复跑；须验证 target 已安装公共 API 与原 Reconcile consumer 的兼容。若该入口兼容不能成立，返回原安装 owner 处理。禁止直接修改业务 runtime 或排除被审路径。

## 5. 行为要求

- R1（S1）：专用 `delivery_resolved_reconciliation` 以被审 stage-0 gitlink 为目标，完整固定 HEAD、单一 MERGE_HEAD、stage-0 tree/index 与实际内容身份。
- R2（S2、S3）：普通 Check 保留原提交绑定。所有入口保留子模块 root、目标 OID、clean 状态和实际候选变化校验。未解决冲突、未暂存内容和候选变化不得获得过期通过。
- R3（S1）：record、checker、公共 invoke、projection 与 Reconcile 对同一真实候选一致。只有实际 resolved 检查结果进入原精确提交；不得先提交绕检查。提交后新 HEAD 仍需 fresh Check/full Review。
- R4（S4）：只在 canonical source 修复，通过已证实受支持的完整 matching reviewed source 执行入口或原安装路径恢复。禁止业务安装 runtime 热改、混合拷贝与路径排除。若公共输入演进，同批维护兼容和同步 consumer 合同。

## 6. 约束与依赖

复用现有 Check profile、Task/Delivery 身份、公共投影与原 Reconcile owner。具体最小机制由 Author/Architecture 细化，需求阶段不预判实现已通过。不存在产品数据模型迁移或新增外部服务。完整工具执行需要 source clean commit 与匹配 Fork；canonical wrappers 的 --root 路线须证明 source runtime、target公共API及target原Reconcile consumer兼容。实际候选复跑由原调用方 owner 承接，不把源码测试解释为该复跑成功。

## 7. 可观察验收与验证方式

- AC1（R1、R3）：以正常 Git 分支和 merge 构造 staged gitlink 更新的已解决候选，child clean 且 HEAD 精确匹配 stage-0 OID；正式 record→check→invoke→projection→精确 Reconcile 完成，提交 tree/parents/message 符合原合同。
- AC2（R2）：普通 staged gitlink 仍拒绝；正常 child dirty、HEAD 不匹配、未解决冲突与捕获后候选变化仍给出明确诊断。
- AC3（R1—R3）：定向回归覆盖无 gitlink、普通 gitlink、resolved gitlink 及真实命令组合，避免仅 mock 子函数证明整链。
- AC4（R4）：canonical/dogfood一致性通过；完整matching reviewed source 的原 --root 入口与target已安装API、原Reconcile consumer组合通过，原调用方真实候选重跑并记录实际结果。若必须安装，另由原安装owner验证完整匹配安装。源码测试不能替代受支持入口或调用方验收。

## 8. 实际未决项

整体需求没有待用户决定的问题。具体 capture 机制和兼容细节由 Delivery Author 与独立 Architecture 审查后落实；实施、受支持入口和真实候选复跑尚待执行。
